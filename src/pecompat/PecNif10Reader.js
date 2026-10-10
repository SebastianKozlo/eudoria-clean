// PecNif10Reader.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// THE EXTENDED NIF 10.1.0.0 READER for the PE compatibility adapter
// (src/pecompat). NEW code — src/pesource/NifModelReader.js (the 457485
// single-witness reader) is NOT imported, NOT modified and NOT pretended to
// support 218757 (14-mesh hierarchy); it stays untouched with its regression
// preserved (tests/pecompat/witness_457485_regression.test.mjs).
//
// REUSE LABEL (documented parser lineage, contract §7 "acceptable to reuse the
// documented parser lineage, but label the reuse and its boundary assumptions"):
//   - Framing/parsing conventions from src/pesource/NifModelReader.js (the R61
//     lineage): header text line + u32 version gate + per-block u32==0
//     preamble + SizedStrings + 1-byte v10 booleans + file-order f32 bit-hex +
//     LOUD failure on unknown types/variants. That reader's first-mesh render
//     path does NOT support 218757; only its documented stream conventions are
//     adopted here.
//   - The 218757-corpus field layouts from the predecessor run's s2 Rosetta
//     parser (PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
//     TOOLS/s2_parse_nif101_r1.py — itself the documented copy of the
//     PE_935_MODEL_218757_PLACEMENT_SEARCH s2): NiDirectionalLight (net+av+
//     affected+dimmer+ambient/diffuse/specular), NiTexturingProperty HIST
//     0.7.1.1 slot order, NiArkTextureExtraData entry list layout
//     (count=(field2>>8)&0xFFFFFF), the closure-constrained boundary search
//     for variable-ext Ark blocks, and the TopObjects footer + EOF-exact
//     closure. These are BOUNDARY ASSUMPTIONS verified per-file by full
//     downstream closure — not claimed as universal NIF semantics.
//
// VERSION GATE: NIF 10.1.0.0 EXACTLY (0x0A010000). Other versions fail LOUDLY.
//
// DECODE CEILING (contract §1): the four Ark blocks (NiArkAnimationExtraData,
// NiArkImporterExtraData, NiArkTextureExtraData, NiArkViewportInfoExtraData)
// are NOT fully semantic decodes. Per actual field coverage:
//   - NiArkTextureExtraData: PARTIALLY_UNDERSTOOD — documented entry-list
//     fields (name, f1, f2, texprop ref) decoded; the per-entry 9-byte tail is
//     recorded RAW ONLY. Its semantics are UNRESOLVED for 218757 (the
//     predecessor retracted the 'BNT2 id' reading for this model); NO
//     textureId interpretation is performed in this run.
//   - NiArkImporterExtraData: PARTIALLY_UNDERSTOOD — name/int/version string
//     decoded; tail recorded RAW (boundary closure-derived; documented tail
//     sizes 41B (218757 corpus) and 38B (457485 witness corpus) are BOTH
//     seeded as candidates — the file's own closure decides, decision recorded).
//   - NiArkAnimationExtraData / NiArkViewportInfoExtraData: OPAQUE — name +
//     closure-derived extension bytes recorded RAW, never interpreted.
//   - NiCamera (the synthetic Control B fixtures only): PARTIALLY_UNDERSTOOD —
//     TRS decoded (the probe quantity); frustum/viewport fields recorded RAW
//     (NOT decoded in this run).
//
// CLOSURE CONTRACT: a parse is accepted ONLY on full-file closure — all
// numBlocks blocks decoded + TopObjects footer + EOF EXACT. Variable-ext
// boundaries are chosen by bounded backtracking over structural candidates
// (the s2 method); every decision is recorded in `closure.decisions`. A
// closure failure is a LOUD error (never a partial silent parse).

export const PEC_NIF10_READER_VERSION = 'pec-nif10-reader-v1';

const NIF_V10_1_0_0 = 0x0A010000;

export const DECODE_STATUS = {
  SUPPORTED: 'SUPPORTED',
  PARTIALLY_UNDERSTOOD: 'PARTIALLY_UNDERSTOOD',
  OPAQUE: 'OPAQUE',
};

const TYPE_DECODE_STATUS = {
  NiNode: DECODE_STATUS.SUPPORTED,
  NiTriShape: DECODE_STATUS.SUPPORTED,
  NiTriShapeData: DECODE_STATUS.SUPPORTED,
  NiTexturingProperty: DECODE_STATUS.SUPPORTED,
  NiMaterialProperty: DECODE_STATUS.SUPPORTED,
  NiZBufferProperty: DECODE_STATUS.SUPPORTED,
  NiAlphaProperty: DECODE_STATUS.SUPPORTED,
  NiVertexColorProperty: DECODE_STATUS.SUPPORTED,
  NiStringExtraData: DECODE_STATUS.SUPPORTED,
  NiArkShaderExtraData: DECODE_STATUS.SUPPORTED,
  NiDirectionalLight: DECODE_STATUS.SUPPORTED,
  NiArkTextureExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiArkImporterExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiCamera: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiArkViewportInfoExtraData: DECODE_STATUS.OPAQUE,
  NiArkAnimationExtraData: DECODE_STATUS.OPAQUE,
};

// Blocks whose payload length is NOT fully documented in this run's lineage:
// parsed fixed-prefix + RAW bytes to a closure-derived boundary.
const BOUNDARY_SEARCH_TYPES = new Set([
  'NiArkViewportInfoExtraData',
  'NiArkAnimationExtraData',
  'NiArkImporterExtraData',
  'NiCamera',
]);

// Documented importer tail sizes from the two lineages, seeded as first
// candidates (the 218757 corpus measured 41B; the 457485 witness corpus
// measured 38B). The closure decides; the decision is recorded.
const IMPORTER_DOCUMENTED_TAIL_SIZES = [41, 38];

const MAX_ATTEMPTS = 200000;

class LoudError extends Error {
  constructor(msg) { super(`[PecNif10Reader] ${msg}`); this.name = 'PecNif10LoudError'; }
}

class NifStream {
  // REUSE LABEL: documented NifStream conventions adopted from
  // src/pesource/NifModelReader.js (R61 lineage) — see the file header.
  constructor(bytes, sourceName = 'input.nif') {
    this.bytes = bytes;
    this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.pos = 0;
    this.source = sourceName;
  }
  get size() { return this.bytes.length; }
  get remaining() { return this.size - this.pos; }
  _check(n) {
    if (this.pos + n > this.size) {
      throw new Error(`[PecNif10Reader] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[PecNif10Reader] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  /** f32 as IEEE-754 bit pattern — FILE-ORDER byte hex (8 chars), the exact
   * parity of Python struct.pack('<f', v).hex() (the R61 lineage convention). */
  f32bits() {
    this._check(4);
    let h = '';
    for (let i = 0; i < 4; i++) h += this.bytes[this.pos + i].toString(16).padStart(2, '0');
    this.pos += 4;
    return h;
  }
  boolean() { return this.u8() !== 0; } // v10.1.0.0: 1-byte booleans
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[PecNif10Reader] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3bits() { return [this.f32bits(), this.f32bits(), this.f32bits()]; }
  mat33bits() { return [this.vec3bits(), this.vec3bits(), this.vec3bits()]; }
  vec3() { return [this.f32(), this.f32(), this.f32()]; }
  mat33() { return [this.vec3(), this.vec3(), this.vec3()]; }
  rawHex(n) {
    this._check(n);
    let s = '';
    for (let i = 0; i < n; i++) s += this.bytes[this.pos + i].toString(16).padStart(2, '0');
    this.pos += n;
    return s;
  }
  /** Contiguous byte range [start,end) as a subarray view (no copy). */
  sliceRange(start, end) {
    if (start < 0 || end > this.size || end < start) {
      throw new Error(`[PecNif10Reader] bad range [${start},${end}) size=${this.size}`);
    }
    return this.bytes.subarray(start, end);
  }
}

// ---- common field groups (documented lineage layouts) ----

function readObjectNet(s, warn) {
  const name = s.sizedString();
  const numExtraData = s.u32();
  if (numExtraData > 65536) {
    throw new Error(`[PecNif10Reader] implausible numExtraData ${numExtraData} in "${name}" @${s.pos - 4}`);
  }
  const extraDataRefs = [];
  for (let i = 0; i < numExtraData; i++) extraDataRefs.push(s.i32());
  const controllerRef = s.i32();
  return { name, numExtraData, extraDataRefs, controllerRef };
}

function readAVObject(s, warn) {
  const flags = s.u16();
  const translationBits = s.vec3bits();
  const translation = [bitsToF32(translationBits[0]), bitsToF32(translationBits[1]), bitsToF32(translationBits[2])];
  const rotationBits = s.mat33bits();
  const rotation = rotationBits.map((r) => r.map(bitsToF32));
  const scaleBits = s.f32bits();
  const scale = bitsToF32(scaleBits);
  const numProperties = s.u32();
  if (numProperties > 65536) {
    throw new Error(`[PecNif10Reader] implausible numProperties ${numProperties} @${s.pos - 4}`);
  }
  const propertyRefs = [];
  for (let i = 0; i < numProperties; i++) propertyRefs.push(s.i32());
  const collisionObjectRef = s.i32();
  return {
    flags, translation, rotation, scale,
    translationBits, rotationBits, scaleBits,
    numProperties, propertyRefs, collisionObjectRef,
  };
}

function bitsToF32(hex) {
  const u = new Uint32Array(1);
  const b = new Uint8Array(u.buffer);
  for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
  return new Float32Array(u.buffer)[0];
}

// ---- fixed block parsers (one per type; loud on desync) ----

function parseNiNode(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const numChildren = s.u32();
  if (numChildren > 65536) throw new Error(`[PecNif10Reader] implausible numChildren ${numChildren}`);
  const children = [];
  for (let i = 0; i < numChildren; i++) children.push(s.i32());
  const numEffects = s.u32();
  if (numEffects > 65536) throw new Error(`[PecNif10Reader] implausible numEffects ${numEffects}`);
  const effects = [];
  for (let i = 0; i < numEffects; i++) effects.push(s.i32());
  return { ...net, ...av, numChildren, children, numEffects, effects };
}

function parseNiTriShape(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dataRef = s.i32();
  const skinRef = s.i32();
  // v10.1: hasShader byte (0x0A000100..0x14010003 gate — always inside for 10.1.0.0)
  const hasShader = s.u8();
  if (hasShader > 1) throw new Error(`[PecNif10Reader] NiTriShape hasShader=${hasShader} invalid @${s.pos - 1}`);
  if (hasShader) {
    // NOT present in this run's inputs; would be a loud unimplemented variant.
    throw new Error(`[PecNif10Reader] NiTriShape "${net.name}" has a shader — shader blocks NOT implemented in this run (LOUD FAIL)`);
  }
  return { ...net, ...av, dataRef, skinRef, hasShader };
}

function parseNiTriShapeData(s) {
  const numVertices = s.u16();
  if (numVertices > 65535) throw new Error(`[PecNif10Reader] impossible numVertices ${numVertices}`);
  const keepFlags = s.u8();
  const compressFlags = s.u8();
  const hasVertices = s.u8();
  if (hasVertices > 1) throw new Error(`[PecNif10Reader] hasVertices=${hasVertices} invalid`);
  let positions = null;
  let vertexRange = null;
  if (hasVertices) {
    const start = s.pos;
    const n = numVertices * 3;
    const arr = new Float32Array(n);
    for (let i = 0; i < n; i++) arr[i] = s.f32();
    positions = arr;
    vertexRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  // 2 bytes of UV-set info. BOUNDARY ASSUMPTION (labeled): the 218757-corpus
  // lineage (s2) reads numUvSetsLo u8 + extraVectorsFlags u8; the 457485
  // witness lineage (NifModelReader) reads the SAME two bytes as one u16
  // (numUvSets, tangentFlag = numUvSets & 0xF000). Both consume 2 bytes; the
  // tangent trigger used here is the witness's broader 0xF0 nibble of the
  // second byte (a superset of s2's & 0x10 condition). 218757 measures
  // extraVectorsFlags == 0 (no tangents).
  const numUvSetsLo = s.u8();
  const extraVectorsFlags = s.u8();
  const numUvSetsRawU16 = numUvSetsLo | (extraVectorsFlags << 8);
  const uvSetCount = numUvSetsLo & 63;
  const tangentFlag = (extraVectorsFlags & 0xf0) !== 0;
  const hasNormals = s.u8();
  if (hasNormals > 1) throw new Error(`[PecNif10Reader] hasNormals=${hasNormals} invalid`);
  let normals = null;
  let normalRange = null;
  let tangentRange = null;
  let bitangentRange = null;
  if (hasNormals) {
    const start = s.pos;
    const n = numVertices * 3;
    const arr = new Float32Array(n);
    for (let i = 0; i < n; i++) arr[i] = s.f32();
    normals = arr;
    normalRange = { start, end: s.pos, byteLength: s.pos - start };
    if (tangentFlag) {
      const tStart = s.pos;
      for (let i = 0; i < numVertices * 3; i++) s.f32();
      tangentRange = { start: tStart, end: s.pos, byteLength: s.pos - tStart };
      const bStart = s.pos;
      for (let i = 0; i < numVertices * 3; i++) s.f32();
      bitangentRange = { start: bStart, end: s.pos, byteLength: s.pos - bStart };
    }
  }
  const center = s.vec3();
  const radius = s.f32();
  const hasVertexColors = s.u8();
  if (hasVertexColors > 1) throw new Error(`[PecNif10Reader] hasVertexColors=${hasVertexColors} invalid`);
  let colors = null;
  let colorRange = null;
  if (hasVertexColors) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 4);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    colors = arr;
    colorRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const uvSets = [];
  const uvRanges = [];
  for (let set = 0; set < uvSetCount; set++) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 2);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    uvSets.push(arr);
    uvRanges.push({ start, end: s.pos, byteLength: s.pos - start });
  }
  const consistencyFlags = s.u16();
  const numTriangles = s.u16();
  const numTrianglePoints = s.u32();
  if (numTrianglePoints > 200000) throw new Error(`[PecNif10Reader] impossible numTrianglePoints ${numTrianglePoints}`);
  const hasTriangles = s.u8();
  if (hasTriangles > 1) throw new Error(`[PecNif10Reader] hasTriangles=${hasTriangles} invalid`);
  let indices = null;
  let indexRange = null;
  if (hasTriangles) {
    if (numTriangles === 0) throw new Error('[PecNif10Reader] hasTriangles=true but numTriangles=0 — LOUD FAIL');
    const start = s.pos;
    const arr = new Uint16Array(numTriangles * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.u16();
    indices = arr;
    indexRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const numMatchGroups = s.u16();
  const matchGroups = [];
  for (let g = 0; g < numMatchGroups; g++) {
    const count = s.u16();
    if (count > 65535) throw new Error(`[PecNif10Reader] impossible matchGroup count ${count}`);
    const groupIndices = [];
    for (let i = 0; i < count; i++) groupIndices.push(s.u16());
    matchGroups.push({ count, indices: groupIndices });
  }
  return {
    numVertices, keepFlags, compressFlags, hasVertices,
    numUvSetsLo, extraVectorsFlags, numUvSetsRawU16, uvSetCount, tangentFlag,
    hasNormals, center, radius, hasVertexColors,
    consistencyFlags, numTriangles, numTrianglePoints, hasTriangles,
    numMatchGroups, matchGroups,
    geometry: {
      positions, normals, colors, uvSets,
      vertexRange, normalRange, colorRange, uvRanges,
      tangentRange, bitangentRange,
      indices, indexRange,
      numVertices, numTriangles,
    },
  };
}

function parseNiTexturingProperty(s) {
  // BOUNDARY ASSUMPTION (labeled): HIST 0.7.1.1 field order per the 218757
  // corpus lineage (s2 / BASELINE_TYPE_TABLE.csv rows 13-47): Apply Mode u32;
  // Texture Count u32; Has+TexDesc pairs Base..Decal0 (7 unconditional slots),
  // Decal1/2/3 when Texture Count >= 8/9/10; Bump luma scale/offset/matrix
  // (24B) only when Has Bump; Num Shader Textures u32. For textureCount==7
  // this consumes the same bytes as the witness lineage's slot loop.
  const net = readObjectNet(s);
  const applyModeU32 = s.u32();
  const textureCount = s.u32();
  if (textureCount > 10) {
    throw new Error(`[PecNif10Reader] NiTexturingProperty textureCount=${textureCount} beyond the documented slot table (LOUD FAIL)`);
  }
  const slotNames = ['Base', 'Dark', 'Detail', 'Gloss', 'Glow', 'Bump', 'Decal0'];
  if (textureCount >= 8) slotNames.push('Decal1');
  if (textureCount >= 9) slotNames.push('Decal2');
  if (textureCount >= 10) slotNames.push('Decal3');
  const slots = [];
  for (const slotName of slotNames) {
    const has = s.u8();
    if (has > 1) throw new Error(`[PecNif10Reader] texprop "${net.name}" slot ${slotName}: invalid Has=${has}`);
    if (has) {
      const sourceRef = s.i32();
      const clampMode = s.u32();
      const filterMode = s.u32();
      const uvSet = s.u32();
      const ps2L = s.i16();
      const ps2K = s.i16();
      const hasTextureTransform = s.u8();
      if (hasTextureTransform > 1) {
        throw new Error(`[PecNif10Reader] texprop slot ${slotName}: invalid transform flag ${hasTextureTransform}`);
      }
      let transformHex = null;
      if (hasTextureTransform) transformHex = s.rawHex(32);
      slots.push({ slotName, has, sourceRef, clampMode, filterMode, uvSet, ps2L, ps2K, hasTextureTransform, transformHex });
    } else {
      slots.push({ slotName, has });
    }
  }
  const bumpSlot = slots.find((x) => x.slotName === 'Bump' && x.has);
  if (bumpSlot) {
    bumpSlot.bumpLumaScale = s.f32();
    bumpSlot.bumpLumaOffset = s.f32();
    bumpSlot.bumpMapMatrix = [s.f32(), s.f32(), s.f32(), s.f32()];
  }
  const numShaderTextures = s.u32();
  if (numShaderTextures > 0) {
    throw new Error('[PecNif10Reader] NiTexturingProperty has shader textures — NOT implemented in this run (LOUD FAIL)');
  }
  return { ...net, applyModeU32, textureCount, slots, numShaderTextures };
}

function parseNiMaterialProperty(s) {
  const net = readObjectNet(s);
  // v10 (10.1.0.0 > 10.0.1.2): NO flags field (documented lineage gate)
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  const emissive = s.vec3();
  const glossiness = s.f32();
  const alpha = s.f32();
  return { ...net, ambient, diffuse, specular, emissive, glossiness, alpha };
}

function parseNiZBufferProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  const fn = s.u32();
  return { ...net, flags, function: fn };
}

function parseNiAlphaProperty(s) {
  const net = readObjectNet(s);
  const alphaFlags = s.u16();
  const alphaThreshold = s.u8();
  return { ...net, alphaFlags, alphaThreshold };
}

function parseNiVertexColorProperty(s) {
  const net = readObjectNet(s);
  // R61/witness convention (not present in this run's inputs; labeled):
  const flags = s.u16();
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32();
  return { ...net, flags, vertexMode, lightingMode, unknownPeField };
}

function parseNiStringExtraData(s) {
  const name = s.sizedString();
  const stringData = s.sizedString();
  return { name, stringData };
}

function parseNiArkShaderExtraData(s) {
  const name = s.sizedString();
  const unknownInt = s.i32();
  const unknownString = s.sizedString();
  return { name, unknownInt, unknownString };
}

function parseNiDirectionalLight(s) {
  // 218757-corpus lineage (s2) layout: net + av + affected list + dimmer +
  // ambient/diffuse/specular. NO attenuation fields (directional light).
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const numAffected = s.u32();
  if (numAffected > 65536) throw new Error(`[PecNif10Reader] implausible numAffected ${numAffected}`);
  const affectedNodeRefs = [];
  for (let i = 0; i < numAffected; i++) affectedNodeRefs.push(s.i32());
  const dimmer = s.f32();
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  return { ...net, ...av, numAffected, affectedNodeRefs, dimmer, ambient, diffuse, specular };
}

function parseNiArkTextureExtraData(s, variant) {
  // BOUNDARY ASSUMPTION (labeled, decision recorded): two documented layout
  // variants exist in the lineage — NOPREFIX (the 218757 corpus / baseline
  // spec: name SS first) and PREFIX3 (the 457485 witness corpus: 3 raw header
  // bytes before the name). The closure decides; the chosen variant is
  // recorded in the decision log.
  let header3BytesHex = null;
  if (variant === 'PREFIX3') header3BytesHex = s.rawHex(3);
  const name = s.sizedString();
  const numTex = s.u32();
  const field1 = s.u32();
  const field2 = s.u32();
  const field2u = field2 >>> 0;
  const entryCount = (field2u >>> 8) & 0x00ffffff;
  const field2Low8 = field2u & 0xff;
  if (entryCount > 4096) {
    throw new Error(`[PecNif10Reader] NiArkTextureExtraData "${name}" entryCount ${entryCount} implausible (LOUD FAIL)`);
  }
  const padU8 = s.u8();
  const entries = [];
  for (let i = 0; i < entryCount; i++) {
    const entryName = s.sizedString();
    if (entryName.length < 1 || entryName.length > 256) {
      throw new Error(`[PecNif10Reader] ArkTexture entry ${i}: implausible name length ${entryName.length}`);
    }
    const f1 = s.i32();
    const f2 = s.i32();
    const texturingPropertyRef = s.i32();
    // The per-entry 9-byte tail: recorded RAW ONLY. Its semantics are
    // UNRESOLVED for 218757 (predecessor retracted the 'BNT2 id' reading for
    // this model). NO textureId interpretation is performed in this run —
    // this is NOT the 457485 witness corpus rule.
    const bytes9Hex = s.rawHex(9);
    entries.push({
      entryName, f1, f2, texturingPropertyRef, bytes9Hex,
      bytes9Semantics: 'RAW_ONLY_UNRESOLVED_FOR_218757 (no textureId interpretation in this run)',
    });
  }
  return {
    name, numTex, field1, field2, field2Low8, entryCount, padU8,
    header3BytesHex, entries,
    bytes9TailPolicy: 'recorded raw; semantics UNRESOLVED for 218757 (no new 9-byte-tail semantics derived in this run)',
  };
}

// ---- boundary-search block prefixes (fixed part before the raw tail/ext) ----

function parseBoundaryPrefix(s, type) {
  if (type === 'NiArkViewportInfoExtraData' || type === 'NiArkAnimationExtraData') {
    return { name: s.sizedString() };
  }
  if (type === 'NiArkImporterExtraData') {
    const name = s.sizedString();
    const int1 = s.u32();
    const versionString = s.sizedString();
    return { name, int1, versionString };
  }
  if (type === 'NiCamera') {
    const net = readObjectNet(s);
    const av = readAVObject(s);
    return { ...net, ...av };
  }
  throw new LoudError(`parseBoundaryPrefix: unhandled type ${type}`);
}

// ---- closure-constrained boundary candidates (the s2 method, mirrored) ----
// A candidate is a position where the NEXT structure plausibly starts:
//  (a) a next-block preamble shape: u32==0 followed by a plausible SizedString
//      name (length 0..256, >=80% printable-or-NUL; rank 0 if len 4..64);
//  (b) a TopObjects footer shape: u32 ntop with 0<=ntop<=numBlocks and
//      p+4+4*ntop == fileSize (rank 0).
// Sorted by (rank, pos); first 1024 kept. The full downstream closure decides.

function boundaryCandidates(bytes, dv, start, numBlocks, fileSize, seedSizes = []) {
  const cands = [];
  const seen = new Set();
  const push = (rank, pos, method) => {
    if (pos < start || pos > fileSize || seen.has(pos)) return;
    seen.add(pos);
    cands.push({ rank, pos, method });
  };
  for (const sz of seedSizes) push(0, start + sz, `documented_size_${sz}B`);
  const window = Math.min(fileSize, start + 8192);
  const scored = [];
  let pos = start;
  while (pos < window) {
    if (pos + 8 <= fileSize) {
      if (dv.getUint32(pos, true) === 0) {
        const ln = dv.getUint32(pos + 4, true);
        if (ln <= 256 && pos + 8 + ln <= fileSize) {
          if (ln === 0) {
            scored.push({ rank: 1, pos, method: 'next_block_preamble_empty_name' });
          } else {
            let printable = 0;
            for (let i = 0; i < ln; i++) {
              const b = bytes[pos + 8 + i];
              if ((b >= 32 && b < 127) || b === 0) printable++;
            }
            if (printable / ln >= 0.8) {
              scored.push({
                rank: (ln >= 4 && ln <= 64) ? 0 : 1,
                pos,
                method: 'next_block_preamble',
              });
            }
          }
        }
      }
    }
    pos++;
  }
  for (let p = start; p <= Math.min(start + 8192, fileSize - 4); p++) {
    const c = dv.getUint32(p, true);
    if (c <= numBlocks && p + 4 + 4 * c === fileSize) {
      scored.push({ rank: 0, pos: p, method: 'top_objects_footer' });
    }
  }
  scored.sort((a, b) => (a.rank - b.rank) || (a.pos - b.pos));
  // Documented seed sizes stay FIRST in the try order (they are the lineage
  // measurements; the scan only adds further candidates after them). A final
  // position sort must NOT reorder the documented seeds ahead of evidence.
  for (const c of scored.slice(0, 1024)) push(c.rank, c.pos, c.method);
  return cands;
}

// ---- the parse with bounded backtracking ----

function parseHeader(s, payload) {
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new LoudError('no newline in header — LOUD FAIL');
  const text = String.fromCharCode(...payload.subarray(0, nl));
  s.seek(nl + 1);
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V10_1_0_0) {
    throw new LoudError(
      `version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — this reader implements ONLY NIF 10.1.0.0 (LOUD FAIL)`);
  }
  const userVersion = s.u32();
  const numBlocks = s.u32();
  if (numBlocks > 100000) throw new LoudError(`implausible numBlocks ${numBlocks}`);
  const numBlockTypes = s.u16();
  if (numBlockTypes > 1024) throw new LoudError(`implausible numBlockTypes ${numBlockTypes}`);
  const blockTypes = [];
  for (let i = 0; i < numBlockTypes; i++) blockTypes.push(s.sizedString());
  const blockTypeIndex = [];
  for (let i = 0; i < numBlocks; i++) {
    const idx = s.u16();
    if (idx >= numBlockTypes) throw new LoudError(`block ${i}: type index ${idx} >= numBlockTypes ${numBlockTypes}`);
    blockTypeIndex.push(idx);
  }
  const numGroups = s.u32();
  if (numGroups !== 0) throw new LoudError(`numGroups=${numGroups} — nonzero groups NOT supported (documented convention; LOUD FAIL)`);
  const groups = [];
  for (let i = 0; i < numGroups; i++) groups.push(s.u32());
  return {
    text,
    versionRaw: `0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`,
    versionString: '10.1.0.0',
    userVersion,
    numBlocks,
    numBlockTypes,
    blockTypes,
    blockTypeIndex,
    numGroups,
    groups,
    dataStartOffset: s.pos,
  };
}

function decodeFrom(s, ctx, blockIndex, out) {
  const { header, payload, dv, state } = ctx;
  if (blockIndex === header.numBlocks) {
    // TopObjects footer + EOF-exact. A failing candidate must return null
    // (backtrackable), never crash the recursion.
    try {
      const ntop = s.u32();
      if (ntop > header.numBlocks) return null;
      const tops = [];
      for (let i = 0; i < ntop; i++) tops.push(s.i32());
      if (s.pos !== s.size) return null;
      return { topObjects: tops, numTopObjects: ntop };
    } catch {
      return null;
    }
  }
  if (++state.attempts > MAX_ATTEMPTS) {
    throw new LoudError(`backtracking attempts exceeded ${MAX_ATTEMPTS} — aborting (input does not close under the documented boundary assumptions)`);
  }
  const start = s.pos;
  let preamble;
  try { preamble = s.u32(); } catch { return null; }
  if (preamble !== 0) return null; // desync at this boundary candidate
  const typeIdx = header.blockTypeIndex[blockIndex];
  const type = header.blockTypes[typeIdx];
  if (!type || !(type in TYPE_DECODE_STATUS)) {
    // Unknown type is fail-closed (witness parity): NOT a backtrackable condition.
    throw new LoudError(`block ${blockIndex}: UNKNOWN type "${type}" (index ${typeIdx}) — no parser registered (LOUD FAIL)`);
  }
  const decodeStatus = TYPE_DECODE_STATUS[type];

  if (BOUNDARY_SEARCH_TYPES.has(type)) {
    let prefix;
    try { prefix = parseBoundaryPrefix(s, type); } catch { return null; }
    const extStart = s.pos;
    const seed = type === 'NiArkImporterExtraData' ? IMPORTER_DOCUMENTED_TAIL_SIZES : [];
    const cands = boundaryCandidates(payload, dv, extStart, header.numBlocks, s.size, seed);
    for (const cand of cands) {
      if (cand.pos < extStart || cand.pos > s.size) continue;
      s.seek(cand.pos);
      state.decisions.push({
        block: blockIndex, type, extStart, extEnd: cand.pos,
        extLength: cand.pos - extStart, method: cand.method,
      });
      out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, cand.pos, prefix, {
        opaque: {
          extHex: hexOfRange(payload, extStart, cand.pos),
          extStart, extEnd: cand.pos, extLength: cand.pos - extStart,
          boundaryMethod: cand.method,
          note: type === 'NiCamera'
            ? 'frustum/viewport fields NOT decoded in this run (TRS is the probe quantity; camera-specific semantics out of scope)'
            : 'extension bytes recorded RAW — content UNDETERMINED beyond the boundary (no silent Ark semantic decode)',
        },
      });
      const sub = decodeFrom(s, ctx, blockIndex + 1, out);
      if (sub) return sub;
      state.decisions.pop();
      out[blockIndex] = null;
      s.seek(extStart);
    }
    return null;
  }

  if (type === 'NiArkTextureExtraData') {
    for (const variant of ['NOPREFIX', 'PREFIX3']) {
      s.seek(start + 4); // after preamble
      let fields;
      try { fields = parseNiArkTextureExtraData(s, variant); } catch { continue; }
      const end = s.pos;
      state.decisions.push({ block: blockIndex, type, variantLayout: variant, extStart: null, extEnd: null });
      fields.variantLayout = variant;
      out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, end, fields);
      const sub = decodeFrom(s, ctx, blockIndex + 1, out);
      if (sub) return sub;
      state.decisions.pop();
      out[blockIndex] = null;
    }
    return null;
  }

  // fixed-layout block
  s.seek(start + 4); // after preamble
  let fields;
  try {
    switch (type) {
      case 'NiNode': fields = parseNiNode(s); break;
      case 'NiTriShape': fields = parseNiTriShape(s); break;
      case 'NiTriShapeData': fields = parseNiTriShapeData(s); break;
      case 'NiTexturingProperty': fields = parseNiTexturingProperty(s); break;
      case 'NiMaterialProperty': fields = parseNiMaterialProperty(s); break;
      case 'NiZBufferProperty': fields = parseNiZBufferProperty(s); break;
      case 'NiAlphaProperty': fields = parseNiAlphaProperty(s); break;
      case 'NiVertexColorProperty': fields = parseNiVertexColorProperty(s); break;
      case 'NiStringExtraData': fields = parseNiStringExtraData(s); break;
      case 'NiArkShaderExtraData': fields = parseNiArkShaderExtraData(s); break;
      case 'NiDirectionalLight': fields = parseNiDirectionalLight(s); break;
      default: throw new LoudError(`block ${blockIndex}: type ${type} listed but unimplemented — LOUD FAIL`);
    }
  } catch (e) {
    if (e instanceof LoudError) throw e; // fail-closed conditions are never backtracked
    s.seek(start);
    return null;
  }
  const end = s.pos;
  out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, end, fields, { fields });
  const sub = decodeFrom(s, ctx, blockIndex + 1, out);
  if (sub) return sub;
  out[blockIndex] = null;
  return null;
}

function makeBlockRecord(index, type, decodeStatus, blockStart, blockEnd, fields, extras = {}) {
  const rec = {
    index,
    type,
    decodeStatus,
    preambleOffset: blockStart,
    payloadStart: blockStart + 4,
    blockEnd,
    name: fields?.name ?? null,
  };
  if (fields && 'translation' in fields) {
    rec.localTrs = { translate: fields.translation, rotate: fields.rotation, scale: fields.scale };
    rec.localTrsBits = {
      translation: fields.translationBits,
      rotation: fields.rotationBits,
      scale: fields.scaleBits,
    };
  }
  if (fields && 'children' in fields) {
    rec.children = fields.children;
    rec.effects = fields.effects;
  }
  if (fields && 'extraDataRefs' in fields) {
    rec.extraDataRefs = fields.extraDataRefs;
    rec.controllerRef = fields.controllerRef;
    rec.propertyRefs = fields.propertyRefs;
    rec.collisionObjectRef = fields.collisionObjectRef;
  }
  if (fields && 'dataRef' in fields) {
    rec.dataRef = fields.dataRef;
    rec.skinRef = fields.skinRef;
  }
  if (fields && fields.geometry) rec.geometry = fields.geometry;
  if (extras.opaque) rec.opaque = extras.opaque;
  rec.fields = sanitizeFields(fields);
  return rec;
}

/** Semantic fields retained in the IR record (bounded; no raw payload arrays):
 * geometry lives top-level, TRS lives top-level (localTrs), the bit-hex TRS
 * trace fields are stripped. Everything else (property slots, material
 * colors, extra-data strings, ArkTexture entry lists, light fields) is kept. */
function sanitizeFields(fields) {
  if (!fields) return null;
  const {
    translation, rotation, scale, translationBits, rotationBits, scaleBits, geometry,
    ...rest
  } = fields;
  void translation; void rotation; void scale;
  void translationBits; void rotationBits; void scaleBits; void geometry;
  return rest;
}

function hexOfRange(bytes, start, end) {
  let h = '';
  for (let i = start; i < end; i++) h += bytes[i].toString(16).padStart(2, '0');
  return h;
}

/**
 * readNif10 — parse a NIF 10.1.0.0 payload to FULL closure or fail loudly.
 * @param {Uint8Array} payload raw NIF bytes
 * @param {object} opts { sourceName?: string }
 * @returns {{ header, blocks: Array, footer, closure: {eofExact, numBlocksDecoded,
 *             attempts, decisions: Array}, sourceName, readerVersion }}
 */
export function readNif10(payload, opts = {}) {
  const sourceName = opts.sourceName ?? 'input.nif';
  const s = new NifStream(payload, sourceName);
  const header = parseHeader(s, payload);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ctx = { header, payload, dv, state: { attempts: 0, decisions: [] } };
  const out = new Array(header.numBlocks).fill(null);
  const footer = decodeFrom(s, ctx, 0, out);
  if (!footer) {
    throw new LoudError(
      `CLOSURE_FAIL: no candidate set closed ${sourceName} under the documented boundary assumptions ` +
      `(attempts=${ctx.state.attempts}, decisionsTried=${ctx.state.decisions.length}) — LOUD FAIL`);
  }
  if (out.some((b) => b == null)) {
    throw new LoudError(`internal: closure returned but some blocks are unset — LOUD FAIL`);
  }
  return {
    readerVersion: PEC_NIF10_READER_VERSION,
    sourceName,
    sourceBytes: payload,
    header,
    blocks: out,
    footer,
    closure: {
      eofExact: true,
      numBlocksDecoded: out.length,
      attempts: ctx.state.attempts,
      decisions: ctx.state.decisions,
    },
  };
}

/**
 * attachGeometryFingerprints — recompute the exact serialized f32-LE vertex
 * and u16-LE triangle fingerprints from the DECODED arrays and cross-check
 * them against the exact serialized byte ranges (round-trip proof).
 * @param {object} readerResult — readNif10 output (mutated: geometry records
 *        gain vertexPositionsF32leSha256 / triangleIndicesU16leSha256 +
 *        roundtripExact flags)
 * @param {(bytes: Uint8Array) => string} sha256 — injected hash function
 *        (environment-neutral: node:crypto in tests/tools; the page supplies
 *        its own when needed)
 */
export function attachGeometryFingerprints(readerResult, sha256) {
  if (typeof sha256 !== 'function') {
    throw new LoudError('attachGeometryFingerprints requires an injected sha256(bytes) function');
  }
  const perMesh = [];
  for (const b of readerResult.blocks) {
    if (b.type !== 'NiTriShapeData' || !b.geometry) continue;
    const g = b.geometry;
    const rec = { dataBlock: b.index, numVertices: g.numVertices, numTriangles: g.numTriangles };
    if (g.vertexRange) {
      const rangeBytes = readerResult.sourceBytes
        ? readerResult.sourceBytes.subarray(g.vertexRange.start, g.vertexRange.end)
        : null;
      // re-pack from DECODED arrays — the fingerprint source of truth:
      const repacked = new Uint8Array(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength);
      rec.vertexPositionsF32leSha256 = sha256(repacked);
      g.vertexPositionsF32leSha256 = rec.vertexPositionsF32leSha256;
      if (rangeBytes) {
        rec.vertexRangeSha256 = sha256(rangeBytes);
        rec.vertexRoundtripExact = rangeBytes.byteLength === repacked.byteLength &&
          sha256(rangeBytes) === rec.vertexPositionsF32leSha256;
      }
    }
    if (g.indexRange) {
      const repackedIdx = new Uint8Array(g.indices.buffer, g.indices.byteOffset, g.indices.byteLength);
      rec.triangleIndicesU16leSha256 = sha256(repackedIdx);
      g.triangleIndicesU16leSha256 = rec.triangleIndicesU16leSha256;
      const rangeBytes = readerResult.sourceBytes
        ? readerResult.sourceBytes.subarray(g.indexRange.start, g.indexRange.end)
        : null;
      if (rangeBytes) {
        rec.indexRangeSha256 = sha256(rangeBytes);
        rec.indexRoundtripExact = sha256(rangeBytes) === rec.triangleIndicesU16leSha256;
      }
    }
    g.fingerprint = rec;
    perMesh.push(rec);
  }
  return perMesh;
}
