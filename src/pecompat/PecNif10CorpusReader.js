// PecNif10CorpusReader.js — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 2)
// THE FULL NIF 10.1.0.0 CORPUS READER for the PCG_9_3_5 Models.bnt container.
// Extends the PecNif10Reader lineage (218757 browser run) to EVERY block type
// physically present in the 4,838 NIF 10.1.0.0 entries of the corpus (72 types
// per the re-measured census). PecNif10Reader.js itself stays BYTE-IDENTICAL
// (its 218757 witness regressions are preserved); this is a NEW module.
//
// LAYOUT AUTHORITY (documented lineage, labeled per the run contract §7):
//   - The frozen project Rosetta at docs/nif/ (02-block-registry, 03-geometry,
//     04-properties, 05-controllers-data, 06-lights-camera-particles,
//     07-skinning, 08-ark-proprietary, 09-semantics) — CONFIRMED layouts for
//     THIS corpus (R61 parsed all 5,596 files with zero failures; per-type
//     citations inside those files). This module re-implements those layouts
//     in JS; no proprietary SDK text is copied.
//   - The local Gamebryo 1.2 SDK sources (Gb12_Source; READ_ONLY architectural
//     reference for the particle/animation LoadBinary field orders — cited per
//     type below where it was consulted).
//   - The PecNif10Reader.js stream/backtracking conventions (REUSE LABEL: the
//     s2 closure method with documented-seed-first candidate ordering).
//
// VERSION GATE: NIF 10.1.0.0 EXACTLY (0x0A010000). Other versions fail LOUDLY
// (dispatch to PecNif41Reader/PecNif40Reader happens in the version-aware
// adapter, never here).
//
// DECODE CEILING (honest labels, per block family):
//   - NiArkViewportInfoExtraData / NiArkAnimationExtraData / NiVertexMorphExtraData:
//     OPAQUE extension bytes recorded RAW (boundary + raw hex only; semantic
//     decode NOT claimed — DETECTION_UNRESOLVED for their channels).
//   - NiArkTextureExtraData: PARTIALLY_UNDERSTOOD (entry fields decoded; the
//     per-entry 9-byte tail is recorded RAW + parsed as animFlag/frameIndex/
//     textureId ONLY where both independent controls pass, in the texture
//     chain module — never here).
//   - NiArkImporterExtraData: PARTIALLY_UNDERSTOOD (name/int/version decoded;
//     the documented 38-byte tail recorded RAW).
//   - All standard Gamebryo blocks (geometry/properties/controllers/keys/
//     skins/lights/particles): SUPPORTED field coverage per the Rosetta.
//
// CLOSURE CONTRACT (unchanged from the lineage): a parse is accepted ONLY on
// full-file closure — all numBlocks blocks + TopObjects footer + EOF EXACT.
// Variable-ext boundaries: documented exact sizes are seeded FIRST, then the
// bounded boundary scan; every decision is recorded in closure.decisions.

export const PEC_NIF10_CORPUS_READER_VERSION = 'pec-nif10-corpus-reader-v1';

const NIF_V10_1_0_0 = 0x0A010000;

export const DECODE_STATUS = {
  SUPPORTED: 'SUPPORTED',
  PARTIALLY_UNDERSTOOD: 'PARTIALLY_UNDERSTOOD',
  OPAQUE: 'OPAQUE',
};

class LoudError extends Error {
  constructor(msg) { super(`[PecNif10Corpus] ${msg}`); this.name = 'PecNif10CorpusLoudError'; }
}

class NifStream {
  // REUSE LABEL: documented stream conventions from PecNif10Reader.js (R61 lineage).
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
      throw new Error(`[PecNif10Corpus] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[PecNif10Corpus] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  boolean() { return this.u8() !== 0; }
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[PecNif10Corpus] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3() { return [this.f32(), this.f32(), this.f32()]; }
  mat33() { return [this.vec3(), this.vec3(), this.vec3()]; }
  color4() { return [this.f32(), this.f32(), this.f32(), this.f32()]; }
  ref() { return this.i32(); } // NIF link id; -1 = null
  refList(maxCount = 65536) {
    const count = this.u32();
    if (count > maxCount) throw new Error(`[PecNif10Corpus] implausible ref-list count ${count} @${this.pos - 4}`);
    const out = [];
    for (let i = 0; i < count; i++) out.push(this.ref());
    return out;
  }
  rawHex(n) {
    this._check(n);
    let s = '';
    for (let i = 0; i < n; i++) s += this.bytes[this.pos + i].toString(16).padStart(2, '0');
    this.pos += n;
    return s;
  }
  /** KeyType per the Rosetta (05): 1=LINEAR 2=QUADRATIC 3=TBC 4=XYZ_EULER 5=CONST(→LINEAR keys). */
  static isTbc(t) { return t === 3; }
}

// ---- common bases (v10.1.0.0 shapes; Rosetta 02) ----

function readObjectNet(s) {
  const name = s.sizedString();
  const numExtraData = s.u32();
  if (numExtraData > 65536) throw new Error(`[PecNif10Corpus] implausible numExtraData ${numExtraData} in "${name}" @${s.pos - 4}`);
  const extraDataRefs = [];
  for (let i = 0; i < numExtraData; i++) extraDataRefs.push(s.ref());
  const controllerRef = s.ref();
  return { name, numExtraData, extraDataRefs, controllerRef };
}

function readAVObject(s) {
  const flags = s.u16();
  const translation = s.vec3();
  const rotation = s.mat33();
  const scale = s.f32();
  const numProperties = s.u32();
  if (numProperties > 65536) throw new Error(`[PecNif10Corpus] implausible numProperties ${numProperties} @${s.pos - 4}`);
  const propertyRefs = [];
  for (let i = 0; i < numProperties; i++) propertyRefs.push(s.ref());
  const collisionObjectRef = s.ref();
  return { flags, translation, rotation, scale, numProperties, propertyRefs, collisionObjectRef };
}

// NiExtraData base v10: Name SizedString only (no link).
function readExtraDataBase(s) { return { name: s.sizedString() }; }

// NiTimeController base (05; 30 bytes): NOT NiObjectNET.
function readTimeController(s) {
  const nextControllerRef = s.ref();
  const flags = s.u16();
  const frequency = s.f32();
  const phase = s.f32();
  const startTime = s.f32();
  const stopTime = s.f32();
  const targetRef = s.ref();
  return { nextControllerRef, flags, frequency, phase, startTime, stopTime, targetRef };
}

// KeyGroup<T> (05): numKeys u32; if != 0: interpolation u32; per key: time + value
// (+QUAD: forward T + backward T — SAME TYPE as the value; +TBC: 3×f32 params).
function readKeyGroup(s, valueReader, valueName) {
  const numKeys = s.u32();
  if (numKeys > 1_000_000) throw new Error(`[PecNif10Corpus] implausible numKeys ${numKeys}`);
  if (numKeys === 0) return { numKeys: 0, interpolation: null, times: [], values: [] };
  const interpolation = s.u32();
  const tbc = NifStream.isTbc(interpolation);
  const quad = interpolation === 2;
  const times = new Float32Array(numKeys);
  const values = [];
  for (let i = 0; i < numKeys; i++) {
    times[i] = s.f32();
    const value = valueReader(s);
    if (quad) { valueReader(s); valueReader(s); } // forward + backward (value-typed)
    else if (tbc) { s.f32(); s.f32(); s.f32(); } // tension/bias/continuity
    values.push(value);
  }
  return { numKeys, interpolation, times, values, valueKind: valueName };
}

// ---- per-type parsers (fixed layouts; Rosetta + SDK citations) ----

function parseNiNode(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const children = s.refList();
  const effects = s.refList();
  return { ...net, ...av, children, effects };
}

function parseNiBillboardNode(s) {
  const fields = parseNiNode(s);
  fields.billboardMode = s.u16(); // v10 only (Rosetta 02)
  return fields;
}

function parseNiSortAdjustNode(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const sortingMode = s.u32(); // Rosetta 02 (1 instance; closure-validated)
  return { ...net, ...av, sortingMode };
}

function parseNiTriShape(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dataRef = s.ref();
  const skinRef = s.ref();
  const hasShader = s.u8(); // v10.1 shader byte (03)
  if (hasShader > 1) throw new Error(`[PecNif10Corpus] NiTriShape hasShader=${hasShader} invalid @${s.pos - 1}`);
  let shaderName = null;
  let shaderUnknownInt = null;
  if (hasShader) {
    shaderName = s.sizedString();
    shaderUnknownInt = s.i32();
  }
  return { ...net, ...av, dataRef, skinRef, hasShader, shaderName, shaderUnknownInt };
}

// NiGeometryData v10 COMMON base (Rosetta 03: the v10 read order up to and
// including consistencyFlags; the triangle/matchGroups section belongs to
// NiTriShapeData ONLY — NiPSysData's base stops here and continues with the
// NiParticlesData/NiRotatingParticles/NiPSysData layers).
function readGeometryDataBaseV10(s) {
  const numVertices = s.u16();
  const keepFlags = s.u8();
  const compressFlags = s.u8();
  const hasVertices = s.u8();
  if (hasVertices > 1) throw new Error(`[PecNif10Corpus] hasVertices=${hasVertices} invalid`);
  let positions = null;
  let vertexRange = null;
  if (hasVertices) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    positions = arr;
    vertexRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const numUvSets = s.u16();
  const uvSetCount = numUvSets & 63;
  const tangentFlag = (numUvSets & 0xF000) !== 0;
  const hasNormals = s.u8();
  if (hasNormals > 1) throw new Error(`[PecNif10Corpus] hasNormals=${hasNormals} invalid`);
  let normals = null;
  let normalRange = null;
  let tangentRange = null;
  let bitangentRange = null;
  if (hasNormals) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
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
  if (hasVertexColors > 1) throw new Error(`[PecNif10Corpus] hasVertexColors=${hasVertexColors} invalid`);
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
  return {
    numVertices, keepFlags, compressFlags, hasVertices,
    numUvSets, uvSetCount, tangentFlag, hasNormals, center, radius, hasVertexColors,
    consistencyFlags,
    geometry: {
      positions, normals, colors, uvSets,
      vertexRange, normalRange, colorRange, uvRanges, tangentRange, bitangentRange,
      numVertices, numTriangles: 0, indices: null, indexRange: null,
    },
  };
}

function parseNiTriShapeData(s) {
  // Rosetta 03 (v10 read order) = the geometry base + the triangle section.
  const g = readGeometryDataBaseV10(s);
  const numTriangles = s.u16();
  const numTrianglePoints = s.u32();
  if (numTrianglePoints > 1_000_000) throw new Error(`[PecNif10Corpus] impossible numTrianglePoints ${numTrianglePoints}`);
  const hasTriangles = s.u8();
  if (hasTriangles > 1) throw new Error(`[PecNif10Corpus] hasTriangles=${hasTriangles} invalid`);
  let indices = null;
  let indexRange = null;
  if (hasTriangles) {
    if (numTriangles > 0 && numTrianglePoints !== numTriangles * 3) {
      throw new Error(`[PecNif10Corpus] numTrianglePoints ${numTrianglePoints} != numTriangles*3 ${numTriangles * 3}`);
    }
    const start = s.pos;
    const arr = new Uint16Array(numTriangles * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.u16();
    indices = arr;
    indexRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const numMatchGroups = s.u16();
  const matchGroups = [];
  for (let gI = 0; gI < numMatchGroups; gI++) {
    const count = s.u16();
    const groupIndices = [];
    for (let i = 0; i < count; i++) groupIndices.push(s.u16());
    matchGroups.push({ count, indices: groupIndices });
  }
  return {
    ...g,
    numTriangles, numTrianglePoints, hasTriangles, numMatchGroups, matchGroups,
    geometry: { ...g.geometry, indices, indexRange, numTriangles },
  };
}

function parseNiTexturingProperty(s) {
  // Rosetta 04 (v10): field_A/B u16 pair (the lineage's applyMode u32) + TexCount.
  const net = readObjectNet(s);
  const fieldA = s.u16();
  const fieldB = s.u16();
  const textureCount = s.u32();
  if (textureCount > 16) throw new Error(`[PecNif10Corpus] texprop "${net.name}" textureCount=${textureCount} beyond bounded slot table`);
  const slotNames = ['Base', 'Dark', 'Detail', 'Gloss', 'Glow', 'Bump', 'Decal0'];
  if (textureCount >= 8) slotNames.push('Decal1');
  if (textureCount >= 9) slotNames.push('Decal2');
  if (textureCount >= 10) slotNames.push('Decal3');
  if (textureCount > 11) {
    // beyond the documented slot vocabulary — loud (ArkTexture census: 40 slots
    // live in ENTRIES, not in this v10 TexDesc loop; >11 map slots are unseen)
    throw new Error(`[PecNif10Corpus] texprop "${net.name}" textureCount=${textureCount} beyond the documented v10 slot loop`);
  }
  const slots = [];
  for (const slotName of slotNames.slice(0, textureCount)) {
    const has = s.u8();
    if (has > 1) throw new Error(`[PecNif10Corpus] texprop "${net.name}" slot ${slotName}: invalid Has=${has}`);
    if (has) {
      const sourceRef = s.ref();
      const clampMode = s.u32();
      const filterMode = s.u32();
      const uvSet = s.u32();
      const tailA = s.i16();
      const tailB = s.i16();
      const transformPresent = s.u8();
      if (transformPresent > 1) throw new Error(`[PecNif10Corpus] texprop slot ${slotName}: invalid transform flag ${transformPresent}`);
      let transformHex = null;
      if (transformPresent) transformHex = s.rawHex(32);
      slots.push({ slotName, has, sourceRef, clampMode, filterMode, uvSet, tailA, tailB, transformPresent, transformHex });
    } else {
      slots.push({ slotName, has });
    }
  }
  const bumpSlot = slots.find((x) => x.slotName === 'Bump' && x.has);
  if (bumpSlot) {
    bumpSlot.bumpLumaScale = s.f32();
    bumpSlot.bumpLumaOffset = s.f32();
    bumpSlot.bumpMat = [s.f32(), s.f32(), s.f32(), s.f32()];
  }
  const trailingU32 = s.u32(); // always 0 (Rosetta 04)
  return { ...net, fieldA, fieldB, textureCount, slots, trailingU32 };
}

function parseNiMaterialProperty(s) {
  // v10.1.0.0 > 10.0.1.2: NO flags (04).
  const net = readObjectNet(s);
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  const emissive = s.vec3();
  const glossiness = s.f32();
  const materialAlpha = s.f32();
  return { ...net, ambient, diffuse, specular, emissive, glossiness, materialAlpha };
}

function parseNiAlphaProperty(s) {
  const net = readObjectNet(s);
  const alphaFlags = s.u16();
  const alphaThreshold = s.u8();
  return { ...net, alphaFlags, alphaThreshold };
}

function parseNiZBufferProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  const zFunction = s.u32(); // >= 4.1.0.5
  return { ...net, flags, zFunction };
}

function parseNiVertexColorProperty(s) {
  // Rosetta 04: PE extension u32 AFTER lightingMode (always consumed).
  const net = readObjectNet(s);
  const flags = s.u16();
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32();
  return { ...net, flags, vertexMode, lightingMode, unknownPeField };
}

function parseNiStencilProperty(s) {
  // Rosetta 04: v10 (>= 0x0A000102): NO flags; the 29-byte body (< 0x14000005).
  const net = readObjectNet(s);
  const stencilEnabled = s.u8();
  const stencilFunction = s.u32();
  const stencilRef = s.u32();
  const stencilMask = s.u32();
  const failAction = s.u32();
  const zFailAction = s.u32();
  const passAction = s.u32();
  const drawMode = s.u32();
  return { ...net, stencilEnabled, stencilFunction, stencilRef, stencilMask, failAction, zFailAction, passAction, drawMode };
}

function parseOneFlagProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  return { ...net, flags };
}

function parseNiFogProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  const fogDepth = s.f32();
  const fogColor = s.vec3();
  return { ...net, flags, fogDepth, fogColor };
}

function parseNiStringExtraData(s) {
  const base = readExtraDataBase(s);
  const stringData = s.sizedString();
  return { ...base, stringData };
}

function parseNiIntegerExtraData(s) {
  const base = readExtraDataBase(s);
  const value = s.i32();
  return { ...base, value };
}

function parseNiBooleanExtraData(s) {
  const base = readExtraDataBase(s);
  const value = s.u8() !== 0;
  return { ...base, value };
}

function parseNiTextKeyExtraData(s) {
  // Rosetta 05 (v10): ExtraData base (name) + numTextKeys + time+text pairs.
  const base = readExtraDataBase(s);
  const numTextKeys = s.u32();
  if (numTextKeys > 65536) throw new Error(`[PecNif10Corpus] implausible numTextKeys ${numTextKeys}`);
  const keys = [];
  for (let i = 0; i < numTextKeys; i++) {
    const time = s.f32();
    const text = s.sizedString();
    keys.push({ time, text });
  }
  return { ...base, numTextKeys, keys };
}

function parseNiArkShaderExtraData(s) {
  const base = readExtraDataBase(s);
  const unknownInt = s.i32();
  const unknownString = s.sizedString();
  return { ...base, unknownInt, unknownString };
}

// ---- animation data (05) ----

function parseNiKeyframeData(s) {
  // Rosetta 05 (CONFIRMED; 72,552 blocks in the corpus):
  const numRotationKeys = s.u32();
  if (numRotationKeys > 1_000_000) throw new Error(`[PecNif10Corpus] implausible numRotationKeys ${numRotationKeys}`);
  let rotationType = null;
  let rotationKeys = null;
  let eulerAxes = null;
  let eulerUnknownFloat = null;
  if (numRotationKeys !== 0) {
    rotationType = s.u32();
    if (rotationType === 4) {
      // XYZ euler path; v <= 0x0A010000: PE-specific extra float BEFORE axis groups.
      eulerUnknownFloat = s.f32();
      eulerAxes = [0, 1, 2].map(() => readKeyGroup(s, (st) => st.f32(), 'f32'));
    } else {
      // Quaternion path (LINEAR/QUAD forced linear — no tangents; TBC: + t,b,c).
      const tbc = NifStream.isTbc(rotationType);
      const times = new Float32Array(numRotationKeys);
      const quats = new Float32Array(numRotationKeys * 4);
      for (let i = 0; i < numRotationKeys; i++) {
        times[i] = s.f32();
        quats[i * 4 + 0] = s.f32();
        quats[i * 4 + 1] = s.f32();
        quats[i * 4 + 2] = s.f32();
        quats[i * 4 + 3] = s.f32();
        if (tbc) { s.f32(); s.f32(); s.f32(); }
      }
      rotationKeys = { numKeys: numRotationKeys, interpolation: rotationType, times, quats };
    }
  }
  const translationKeys = readKeyGroup(s, (st) => st.vec3(), 'vec3');
  const scaleKeys = readKeyGroup(s, (st) => st.f32(), 'f32');
  return { numRotationKeys, rotationType, rotationKeys, eulerAxes, eulerUnknownFloat, translationKeys, scaleKeys };
}

function parseNiFloatData(s) {
  return { floatKeys: readKeyGroup(s, (st) => st.f32(), 'f32') };
}

function parseNiPosData(s) {
  return { posKeys: readKeyGroup(s, (st) => st.vec3(), 'vec3') };
}

function parseNiColorData(s) {
  return { colorKeys: readKeyGroup(s, (st) => st.color4(), 'color4') };
}

function parseNiUVData(s) {
  // 4 × KeyGroup<f32> (U offset, V offset, U tiling, V tiling).
  const uvGroups = [
    readKeyGroup(s, (st) => st.f32(), 'f32'),
    readKeyGroup(s, (st) => st.f32(), 'f32'),
    readKeyGroup(s, (st) => st.f32(), 'f32'),
    readKeyGroup(s, (st) => st.f32(), 'f32'),
  ];
  return { uvGroups };
}

function parseNiVisData(s) {
  const numKeys = s.u32();
  if (numKeys > 65536) throw new Error(`[PecNif10Corpus] implausible vis numKeys ${numKeys}`);
  const keys = [];
  for (let i = 0; i < numKeys; i++) {
    const time = s.f32();
    const value = s.u8();
    keys.push({ time, value: value !== 0 });
  }
  return { numKeys, keys };
}

function parseNiPSysEmitterCtlrData(s) {
  // SDK NiPSysEmitterCtlrData.cpp: birth-rate float KeyGroup + active vis keys.
  const floatKeys = readKeyGroup(s, (st) => st.f32(), 'f32');
  const numVisibilityKeys = s.u32();
  if (numVisibilityKeys > 65536) throw new Error(`[PecNif10Corpus] implausible numVisibilityKeys ${numVisibilityKeys}`);
  const visibilityKeys = [];
  for (let i = 0; i < numVisibilityKeys; i++) {
    const time = s.f32();
    const value = s.u8();
    visibilityKeys.push({ time, value: value !== 0 });
  }
  return { floatKeys, numVisibilityKeys, visibilityKeys };
}

// ---- controllers (05 registry) ----

function parseNiKeyframeController(s) {
  const tc = readTimeController(s);
  const dataRef = s.ref();
  return { ...tc, dataRef };
}

function parseNiUVController(s) {
  const tc = readTimeController(s);
  const unknownShort = s.u16();
  const dataRef = s.ref();
  return { ...tc, unknownShort, dataRef };
}

function parseNiTextureTransformController(s) {
  const tc = readTimeController(s);
  const unknown2 = s.u8();
  const textureSlot = s.u32();
  const operation = s.u32();
  const dataRef = s.ref();
  return { ...tc, unknown2, textureSlot, operation, dataRef };
}

function parseNiFlipController(s) {
  const tc = readTimeController(s);
  const textureSlot = s.u32();
  const unknownInt2 = s.u32();
  const delta = s.f32();
  const numSources = s.u32();
  if (numSources > 4096) throw new Error(`[PecNif10Corpus] implausible numSources ${numSources}`);
  const sourceRefs = [];
  for (let i = 0; i < numSources; i++) sourceRefs.push(s.ref());
  return { ...tc, textureSlot, unknownInt2, delta, numSources, sourceRefs };
}

function parseNiVisController(s) {
  const tc = readTimeController(s);
  const dataRef = s.ref();
  return { ...tc, dataRef };
}

function parseNiAlphaController(s) {
  const tc = readTimeController(s);
  const dataRef = s.ref();
  return { ...tc, dataRef };
}

function parseNiMaterialColorController(s) {
  const tc = readTimeController(s);
  const targetColor = s.u16(); // v10 (05 registry)
  const dataRef = s.ref();
  return { ...tc, targetColor, dataRef };
}

function parseNiLightColorController(s) {
  const tc = readTimeController(s);
  const targetColor = s.u16();
  const dataRef = s.ref();
  return { ...tc, targetColor, dataRef };
}

function parseNiLookAtController(s) {
  const tc = readTimeController(s);
  const unknown1 = s.u16(); // v10 (05 registry)
  const lookAtNodeRef = s.ref();
  return { ...tc, unknown1, lookAtNodeRef };
}

function parseNiPSysEmitterCtlr(s) {
  const tc = readTimeController(s);
  const modifierName = s.sizedString();
  const emitterLink = s.ref(); // v <= 0x0A010000 (our version exactly)
  return { ...tc, modifierName, emitterLink };
}

function parseNiPSysUpdateCtlr(s) {
  return readTimeController(s);
}

function parseNiPSysResetOnLoopCtlr(s) {
  return readTimeController(s);
}

function parseNiPSysModifierActiveCtlr(s) {
  const tc = readTimeController(s);
  const modifierName = s.sizedString();
  const unknownLink = s.u32(); // v <= 0x0A010000 (05 registry: u32)
  return { ...tc, modifierName, unknownLink };
}

// ---- skinning (07) ----

function parseNiSkinInstance(s) {
  // 07: for 10.1.0.0 (< 0x0A020000): NO skinPartition link here (it lives in NiSkinData).
  const dataRef = s.ref();
  const skeletonRootRef = s.ref();
  const numBones = s.u32();
  if (numBones > 4096) throw new Error(`[PecNif10Corpus] implausible numBones ${numBones}`);
  const boneRefs = [];
  for (let i = 0; i < numBones; i++) boneRefs.push(s.ref());
  return { dataRef, skeletonRootRef, numBones, boneRefs };
}

function parseNiSkinData(s) {
  // 07: overall transform + numBones + [skinPartition link u32 (0x04000002 ≤ v ≤ 0x0A010000 — YES for 10.1)]
  // + [hasVertexWeights u8 (v ≥ 0x04020100 — YES for v10)] + per-bone records.
  const overallRotation = s.mat33();
  const overallTranslation = s.vec3();
  const overallScale = s.f32();
  const numBones = s.u32();
  if (numBones > 4096) throw new Error(`[PecNif10Corpus] implausible skin numBones ${numBones}`);
  const skinPartitionLink = s.u32(); // read as u32 per 07 (both PE versions read it in this range)
  const hasVertexWeights = s.u8();
  const bones = [];
  for (let i = 0; i < numBones; i++) {
    const boneRotation = s.mat33();
    const boneTranslation = s.vec3();
    const boneScale = s.f32();
    const boundingSphereOffset = s.vec3();
    const boundingSphereRadius = s.f32();
    const numVertices = s.u16();
    const vertexWeights = [];
    if (hasVertexWeights) {
      for (let j = 0; j < numVertices; j++) {
        const vertexIndex = s.u16();
        const weight = s.f32();
        vertexWeights.push({ vertexIndex, weight });
      }
    }
    bones.push({ boneRotation, boneTranslation, boneScale, boundingSphereOffset, boundingSphereRadius, numVertices, vertexWeights });
  }
  return {
    overallRotation, overallTranslation, overallScale, numBones,
    skinPartitionLink, hasVertexWeights, bones,
  };
}

function parseNiSkinPartition(s) {
  // 07 (v10 ≥ 0x0A010000 path).
  const numPartitions = s.u32();
  if (numPartitions > 1024) throw new Error(`[PecNif10Corpus] implausible numPartitions ${numPartitions}`);
  const partitions = [];
  for (let p = 0; p < numPartitions; p++) {
    const numVertices = s.u16();
    const numTriangles = s.u16();
    const numBones = s.u16();
    const numStrips = s.u16();
    const numWeightsPerVertex = s.u16();
    const bones = [];
    for (let i = 0; i < numBones; i++) bones.push(s.u16());
    const hasVertexMap = s.u8();
    if (hasVertexMap > 1) throw new Error(`[PecNif10Corpus] partition hasVertexMap=${hasVertexMap} invalid`);
    const vertexMap = [];
    if (hasVertexMap) for (let i = 0; i < numVertices; i++) vertexMap.push(s.u16());
    const hasVertexWeights = s.u8();
    if (hasVertexWeights > 1) throw new Error(`[PecNif10Corpus] partition hasVertexWeights=${hasVertexWeights} invalid`);
    const vertexWeights = [];
    if (hasVertexWeights) {
      for (let v = 0; v < numVertices; v++) {
        const row = [];
        for (let w = 0; w < numWeightsPerVertex; w++) row.push(s.f32());
        vertexWeights.push(row);
      }
    }
    const hasFaces = s.u8();
    if (hasFaces > 1) throw new Error(`[PecNif10Corpus] partition hasFaces=${hasFaces} invalid`);
    const stripLengths = [];
    for (let i = 0; i < numStrips; i++) stripLengths.push(s.u16());
    let faces = null;
    if (numStrips > 0) {
      faces = [];
      for (let st = 0; st < numStrips; st++) {
        const strip = [];
        for (let i = 0; i < stripLengths[st]; i++) strip.push(s.u16());
        faces.push(strip);
      }
    } else if (hasFaces) {
      faces = [];
      for (let t = 0; t < numTriangles; t++) {
        faces.push([s.u16(), s.u16(), s.u16()]);
      }
    }
    const hasBoneIndices = s.u8();
    if (hasBoneIndices > 1) throw new Error(`[PecNif10Corpus] partition hasBoneIndices=${hasBoneIndices} invalid`);
    const boneIndices = [];
    if (hasBoneIndices) {
      for (let v = 0; v < numVertices; v++) {
        const row = [];
        for (let w = 0; w < numWeightsPerVertex; w++) row.push(s.u8());
        boneIndices.push(row);
      }
    }
    partitions.push({ numVertices, numTriangles, numBones, numStrips, numWeightsPerVertex, bones, vertexMap, vertexWeights, stripLengths, faces, boneIndices });
  }
  return { numPartitions, partitions };
}

// ---- lights (06) ----

function readDynamicEffect(s) {
  const numAffectedNodeRefs = s.refList();
  return { numAffectedNodeRefs: numAffectedNodeRefs.length, affectedNodeRefs };
}
const affectedNodeRefsCache = null; // (documented readDynamicEffect returns the list directly)
function readDynamicEffectLayer(s) {
  const affectedNodeRefs = s.refList();
  return { affectedNodeRefs };
}

function readLightFields(s) {
  const dimmer = s.f32();
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  return { dimmer, ambient, diffuse, specular };
}

function parseNiPointLight(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dyn = readDynamicEffectLayer(s);
  const light = readLightFields(s);
  const constantAttenuation = s.f32();
  const linearAttenuation = s.f32();
  const quadraticAttenuation = s.f32();
  return { ...net, ...av, ...dyn, ...light, constantAttenuation, linearAttenuation, quadraticAttenuation };
}

function parseNiSpotLight(s) {
  const fields = parseNiPointLight(s);
  fields.cutoffAngle = s.f32();
  fields.exponent = s.f32();
  return fields;
}

function parseNiDirectionalLight(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dyn = readDynamicEffectLayer(s);
  const light = readLightFields(s);
  return { ...net, ...av, ...dyn, ...light };
}

function parseNiAmbientLight(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dyn = readDynamicEffectLayer(s);
  const light = readLightFields(s);
  return { ...net, ...av, ...dyn, ...light };
}

function parseNiTextureEffect(s) {
  // Rosetta 06 (v10 layout; 20/20 traces).
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dyn = readDynamicEffectLayer(s);
  const modelProjectionMatrix = s.mat33();
  const modelProjectionTransform = s.vec3();
  const textureFiltering = s.u32();
  const textureClamping = s.u32();
  const textureType = s.u32();
  const coordinateGenerationType = s.u32();
  const sourceTextureRef = s.ref();
  const clippingPlane = s.u8();
  const unknownVector = s.vec3();
  const unknownFloat = s.f32();
  const ps2L = s.i16();
  const ps2K = s.i16();
  return {
    ...net, ...av, ...dyn, modelProjectionMatrix, modelProjectionTransform,
    textureFiltering, textureClamping, textureType, coordinateGenerationType,
    sourceTextureRef, clippingPlane, unknownVector, unknownFloat, ps2L, ps2K,
  };
}

function parseNiCollisionData(s) {
  // Rosetta 06: NiCollisionObject chain (v10).
  const targetRef = s.ref();
  const propagationMode = s.u32();
  const collisionMode = s.u32(); // v10
  const useAbv = s.u8();
  let boundingVolume = null;
  if (useAbv) {
    const collisionType = s.u32();
    let volume;
    if (collisionType === 0) {
      volume = { kind: 'SPHERE', center: s.vec3(), radius: s.f32() };
    } else if (collisionType === 1) {
      volume = {
        kind: 'BOX', center: s.vec3(),
        axis: [s.vec3(), s.vec3(), s.vec3()],
        extent: [s.f32(), s.f32(), s.f32()],
      };
    } else if (collisionType === 2) {
      volume = { kind: 'CAPSULE', center: s.vec3(), origin: s.vec3(), lengths: [s.f32(), s.f32()] };
    } else if (collisionType === 5) {
      volume = { kind: 'HALF_SPACE', normal: s.vec3(), center: s.vec3() };
    } else {
      throw new LoudError(`collision bounding volume type ${collisionType} NOT implemented (LOUD FAIL)`);
    }
    boundingVolume = { collisionType, ...volume };
  }
  return { targetRef, propagationMode, collisionMode, useAbv, boundingVolume };
}

// ---- particle systems (06 + SDK NiParticle LoadBinary citations) ----

function parseNiParticleSystem(s) {
  // = NiGeometry (net+av+dataRef+skinRef+hasShader) + worldSpace + modifiers (SDK NiParticleSystem).
  const geo = parseNiTriShape(s);
  const worldSpace = s.u8();
  const modifierRefs = s.refList();
  return { ...geo, worldSpace, modifierRefs };
}

function parseNiMeshParticleSystem(s) {
  return parseNiParticleSystem(s); // pure passthrough (SDK)
}

function parseNiPSysData(s) {
  // Chain: NiGeometryData(v10 common base — NO triangle section) → NiParticlesData
  // (hasRadii + numActive + hasSizes) → NiRotatingParticles (hasRotations; the
  // rotations2 layer is v ≤ 0x04020200 only — NOT PE v10) → NiPSysData
  // (NiParticleInfo per vertex + numAddedParticles/addedParticlesBase).
  const g = readGeometryDataBaseV10(s);
  const numVertices = g.numVertices;
  const hasRadii = s.u8();
  if (hasRadii > 1) throw new Error(`[PecNif10Corpus] PSysData hasRadii=${hasRadii} invalid`);
  let radii = null;
  if (hasRadii) {
    radii = new Float32Array(numVertices);
    for (let i = 0; i < numVertices; i++) radii[i] = s.f32();
  }
  const numActive = s.u16();
  const hasSizes = s.u8();
  if (hasSizes > 1) throw new Error(`[PecNif10Corpus] PSysData hasSizes=${hasSizes} invalid`);
  let sizes = null;
  if (hasSizes) {
    sizes = new Float32Array(numVertices);
    for (let i = 0; i < numVertices; i++) sizes[i] = s.f32();
  }
  const hasRotations = s.u8();
  if (hasRotations > 1) throw new Error(`[PecNif10Corpus] PSysData hasRotations=${hasRotations} invalid`);
  let rotations = null;
  if (hasRotations) {
    rotations = new Float32Array(numVertices * 4);
    for (let i = 0; i < rotations.length; i++) rotations[i] = s.f32();
  }
  // NiPSysData: NiParticleInfo per vertex (SDK NiParticleInfo.h: velocity vec3 +
  // rotationAxis vec3 + age/lifeSpan/lastUpdate f32 + generation/code u16) +
  // numAddedParticles u16 + addedParticlesBase u16.
  const particleInfo = [];
  for (let i = 0; i < numVertices; i++) {
    const velocity = s.vec3();
    const rotationAxis = s.vec3();
    const age = s.f32();
    const lifeSpan = s.f32();
    const lastUpdate = s.f32();
    const generation = s.u16();
    const code = s.u16();
    particleInfo.push({ velocity, rotationAxis, age, lifeSpan, lastUpdate, generation, code });
  }
  const numAddedParticles = s.u16();
  const addedParticlesBase = s.u16();
  return {
    ...g,
    hasRadii, radii, numActive, hasSizes, sizes, hasRotations, rotations,
    particleInfo, numAddedParticles, addedParticlesBase,
  };
}

function parseNiMeshPSysData(s) {
  // NiMeshPSysData extends NiPSysData with mesh-referencing arrays (SDK);
  // bounded: after the PSysData chain, read the mesh arrays closure-validated.
  const base = parseNiPSysData(s);
  // SDK NiMeshPSysData::LoadBinary: numBoundMeshes? The 3 instances are rare;
  // boundary-safe approach: record remaining bytes of this block RAW and let
  // the boundary search decide the block end (this type joins the search set).
  return base;
}

function readPSysModifierBase(s) {
  // SDK NiPSysModifier: name CString + order u32 + target link + active u8.
  const name = s.sizedString();
  const order = s.u32();
  const targetRef = s.ref();
  const active = s.u8();
  return { name, order, targetRef, active };
}

function parseNiPSysAgeDeathModifier(s) {
  const base = readPSysModifierBase(s);
  const spawnOnDeath = s.u8();
  const spawnModifierRef = s.ref();
  return { ...base, spawnOnDeath, spawnModifierRef };
}

function parseNiPSysSpawnModifier(s) {
  const base = readPSysModifierBase(s);
  const numSpawnGenerations = s.u16();
  const percentageSpawned = s.f32();
  const minNumToSpawn = s.u16();
  const maxNumToSpawn = s.u16();
  const spawnSpeedChaos = s.f32();
  const spawnDirChaos = s.f32();
  const lifeSpan = s.f32();
  const lifeSpanVar = s.f32();
  return { ...base, numSpawnGenerations, percentageSpawned, minNumToSpawn, maxNumToSpawn, spawnSpeedChaos, spawnDirChaos, lifeSpan, lifeSpanVar };
}

function parseNiPSysPositionModifier(s) {
  return readPSysModifierBase(s);
}

function parseNiPSysBoundUpdateModifier(s) {
  const base = readPSysModifierBase(s);
  const updateSkip = s.u16(); // v <= 10.1.0.100 (SDK)
  return { ...base, updateSkip };
}

function parseNiPSysColorModifier(s) {
  const base = readPSysModifierBase(s);
  const dataRef = s.ref();
  return { ...base, dataRef };
}

function parseNiPSysGrowFadeModifier(s) {
  const base = readPSysModifierBase(s);
  const growTime = s.f32();
  const growGeneration = s.u16();
  const fadeTime = s.f32();
  const fadeGeneration = s.u16();
  return { ...base, growTime, growGeneration, fadeTime, fadeGeneration };
}

function parseNiPSysGravityModifier(s) {
  const base = readPSysModifierBase(s);
  const gravityObjectRef = s.ref();
  const gravityAxis = s.vec3();
  const decay = s.f32();
  const strength = s.f32();
  const forceType = s.u32();
  // SDK: turbulence/scale only when fileVersion >= 10.0.1.14 — 10.1.0.0 YES.
  const turbulence = s.f32();
  const turbulenceScale = s.f32();
  return { ...base, gravityObjectRef, gravityAxis, decay, strength, forceType, turbulence, turbulenceScale };
}

function parseNiPSysRotationModifier(s) {
  const base = readPSysModifierBase(s);
  const rotationSpeed = s.f32();
  const randomInitialAxis = s.u8();
  const initialAxis = s.vec3();
  return { ...base, rotationSpeed, randomInitialAxis, initialAxis };
}

function parseNiPSysMeshUpdateModifier(s) {
  const base = readPSysModifierBase(s);
  const meshRefs = s.refList();
  return { ...base, meshRefs };
}

function parseNiPSysColliderManager(s) {
  const base = readPSysModifierBase(s);
  const colliderRef = s.ref();
  return { ...base, colliderRef };
}

function parseNiPSysDragModifier(s) {
  const base = readPSysModifierBase(s);
  const dragObjectRef = s.ref();
  const dragAxis = s.vec3();
  const percentage = s.f32();
  const range = s.f32();
  const rangeFalloff = s.f32();
  return { ...base, dragObjectRef, dragAxis, percentage, range, rangeFalloff };
}

function parseNiPSysPlanarCollider(s) {
  // SDK NiPSysCollider base (NiObject): bounce + spawnOnCollide/dieOnCollide NiBool
  // + spawnModifier/manager/next links; Planar adds colliderObj link + width/height + axes.
  const bounce = s.f32();
  const spawnOnCollide = s.u8();
  const dieOnCollide = s.u8();
  const spawnModifierRef = s.ref();
  const managerRef = s.ref();
  const nextColliderRef = s.ref();
  const colliderObjectRef = s.ref();
  const width = s.f32();
  const height = s.f32();
  const xAxis = s.vec3();
  const yAxis = s.vec3();
  return { bounce, spawnOnCollide, dieOnCollide, spawnModifierRef, managerRef, nextColliderRef, colliderObjectRef, width, height, xAxis, yAxis };
}

function readPSysEmitterBase(s) {
  // SDK NiPSysEmitter::LoadBinary.
  const base = readPSysModifierBase(s);
  const speed = s.f32();
  const speedVar = s.f32();
  const declination = s.f32();
  const declinationVar = s.f32();
  const planarAngle = s.f32();
  const planarAngleVar = s.f32();
  const initialColor = s.color4();
  const initialRadius = s.f32();
  const lifeSpan = s.f32();
  const lifeSpanVar = s.f32();
  return { ...base, speed, speedVar, declination, declinationVar, planarAngle, planarAngleVar, initialColor, initialRadius, lifeSpan, lifeSpanVar };
}

function parseNiPSysBoxEmitter(s) {
  const e = readPSysEmitterBase(s);
  const emitterObjectRef = s.ref(); // NiPSysVolumeEmitter::LoadBinary link
  const width = s.f32();
  const height = s.f32();
  const depth = s.f32();
  return { ...e, emitterObjectRef, width, height, depth };
}

function parseNiPSysSphereEmitter(s) {
  const e = readPSysEmitterBase(s);
  const emitterObjectRef = s.ref();
  const radius = s.f32();
  return { ...e, emitterObjectRef, radius };
}

function parseNiPSysMeshEmitter(s) {
  // SDK NiPSysMeshEmitter: NiPSysEmitter (NOT volume) + mesh links + enums + axis.
  const e = readPSysEmitterBase(s);
  const emitterMeshRefs = s.refList();
  const initialVelocityType = s.u32();
  const emissionType = s.u32();
  const emissionAxis = s.vec3();
  return { ...e, emitterMeshRefs, initialVelocityType, emissionType, emissionAxis };
}

function parseNiSourceTexture(s) {
  // Rosetta 04 (v10 layout).
  const net = readObjectNet(s);
  const useExternal = s.u8();
  let fileName = null;
  let unknownLink = null;
  let pixelDataRef = null;
  let extraU32 = null;
  if (useExternal) {
    fileName = s.sizedString();
    unknownLink = s.u32();
  } else {
    fileName = s.sizedString();
    pixelDataRef = s.u32();
  }
  const pixelLayout = s.u32();
  const useMipmaps = s.u32();
  const alphaFormat = s.u32();
  const isStatic = s.u8();
  if (!useExternal) extraU32 = s.u32(); // v10 && internal: extra u32 (value 0)
  return { ...net, useExternal, fileName, unknownLink, pixelDataRef, pixelLayout, useMipmaps, alphaFormat, isStatic, extraU32 };
}

function parseNiPixelData(s) {
  // Rosetta 04 (v10; 1 instance — layout closure-validated).
  const pixelFormat = s.u32();
  const masks = [s.u32(), s.u32(), s.u32(), s.u32()];
  const bitsPerPixel = s.u8();
  const unknown3 = s.rawHex(3);
  const unknown8 = s.rawHex(1);
  const paletteRef = s.u32();
  const numMipmaps = s.u32();
  const bytesPerPixel = s.u32();
  const mipmaps = [];
  for (let m = 0; m < numMipmaps; m++) {
    mipmaps.push({ width: s.u32(), height: s.u32(), offset: s.u32() });
  }
  const numPixelsByteSize = s.u32(); // TOTAL BYTE SIZE (Rosetta 04 note)
  const pixelsHex = s.rawHex(numPixelsByteSize);
  return { pixelFormat, masks, bitsPerPixel, unknown3, unknown8, paletteRef, numMipmaps, bytesPerPixel, mipmaps, numPixelsByteSize, pixelsHex };
}

// ---- NiArkTextureExtraData (08; v10 unified grammar, exact consumption) ----

function parseNiArkTextureExtraData(s, variant) {
  let header3BytesHex = null;
  if (variant === 'PREFIX3') header3BytesHex = s.rawHex(3);
  const name = s.sizedString();
  const numTex = s.i32();
  const field1 = s.i32();
  const field2 = s.i32();
  const field2u = field2 >>> 0;
  const entryCount = (field2u >>> 8) & 0x00ffffff;
  const field2Low8 = field2u & 0xff;
  if (entryCount > 4096) {
    throw new Error(`[PecNif10Corpus] ArkTexture "${name}" entryCount ${entryCount} implausible (LOUD FAIL)`);
  }
  const padU8 = s.u8();
  const entries = [];
  for (let i = 0; i < entryCount; i++) {
    const entryName = s.sizedString();
    if (entryName.length < 1 || entryName.length > 256) {
      throw new Error(`[PecNif10Corpus] ArkTexture entry ${i}: implausible name length ${entryName.length}`);
    }
    const f1 = s.i32();
    const f2 = s.i32();
    const texturingPropertyRef = s.ref();
    // The per-entry 9-byte tail: RAW bytes here; the byte-shape + reference
    // controls (animFlag/frameIndex/textureId) are applied in the texture chain
    // module ONLY where both independent controls pass (contract §5).
    const bytes9Hex = s.rawHex(9);
    entries.push({ entryName, f1, f2, texturingPropertyRef, bytes9Hex });
  }
  return {
    name, numTex, field1, field2, field2Low8, entryCount, padU8,
    header3BytesHex, entries, variantLayout: variant,
    bytes9TailPolicy: 'RAW in the reader; textureId interpretation only via the tail controls in PecTextureChain (never here)',
  };
}

// ---- boundary-search prefixes (variable-ext Ark blocks; prefix before raw ext) ----

function parseBoundaryPrefix(s, type) {
  if (type === 'NiArkViewportInfoExtraData') {
    return { name: s.sizedString() };
  }
  if (type === 'NiArkAnimationExtraData') {
    // 08: canonical header = base(name SS) + u1..u4 (extension starts at +20 after u4).
    const name = s.sizedString();
    const u1 = s.i32();
    const u2 = s.i32();
    const u3 = s.i32();
    const u4 = s.i32();
    return { name, u1, u2, u3, u4 };
  }
  if (type === 'NiArkImporterExtraData') {
    const name = s.sizedString();
    const int1 = s.u32();
    const versionString = s.sizedString();
    return { name, int1, versionString };
  }
  if (type === 'NiMeshPSysData') {
    // The full PSysData chain IS the fixed prefix; the undocumented mesh
    // arrays follow and stay RAW (boundary search).
    return parseNiPSysData(s);
  }
  if (type === 'NiVertexMorphExtraData') {
    // v10 ExtraData base = Name SizedString FIRST (measured on 591842.nif:
    // "NiVertexMorphExtraData"), then the 0x01 magic + u32 vertex count N +
    // the FIRST record's u16 tag; payload records follow (08/ITER-4).
    const name = s.sizedString();
    const magic = s.u8();
    if (magic !== 1) throw new Error(`[PecNif10Corpus] VertexMorph magic byte ${magic} != 1 (LOUD FAIL)`);
    const vertexCount = s.u32();
    if (vertexCount > 1_000_000) throw new Error(`[PecNif10Corpus] VertexMorph vertexCount ${vertexCount} implausible`);
    const tag = s.u16();
    return { name, magic, vertexCount, tag };
  }
  throw new LoudError(`parseBoundaryPrefix: unhandled type ${type}`);
}

// documented ext-size seeds per variable type (08; the closure decides, the
// seeds stay FIRST in candidate order — the s2 discipline).
function documentedExtSeeds(type, prefix, remaining) {
  if (type === 'NiArkImporterExtraData') return [38]; // ALWAYS 38 raw (R29 census)
  if (type === 'NiArkAnimationExtraData') {
    const { u2, u3, u4 } = prefix;
    const seeds = [];
    if (u4 === 0 && (u2 >>> 0) === 0xffffffff) seeds.push(0); // V10_BASE_0B
    if (u4 === 0x01000000) seeds.push(33); // V10_BASE_33B
    const u3b1 = ((u3 >>> 0) >> 8) & 0xff; // G3D: u3_byte1 × 5
    if (u3b1 > 0 && u3b1 * 5 <= remaining) seeds.push(u3b1 * 5);
    return seeds;
  }
  if (type === 'NiVertexMorphExtraData') {
    // Uniform record model (08/ITER-4): N records of [u16 tag][W×f32] with
    // the FIRST record's tag absorbed by the block prefix; W ∈ {10, 11}.
    // Measured on 591842.nif: ext = N×W×4 + (N-1)×2. Seed both W variants
    // (+ small tail variants recorded in the lineage); closure decides.
    const N = prefix.vertexCount;
    if (!N || N > 1_000_000) return [];
    const seeds = [];
    for (const W of [10, 11]) {
      const base = N * W * 4 + (N - 1) * 2;
      for (const t of [0, 2, 4, 6]) {
        if (base + t <= remaining && base + t >= 0) seeds.push(base + t);
      }
    }
    return seeds;
  }
  return [];
}

// ---- the per-type registry ----

const TYPE_PARSERS = {
  NiNode: parseNiNode,
  NiTriShape: parseNiTriShape,
  NiTriShapeData: parseNiTriShapeData,
  NiTexturingProperty: parseNiTexturingProperty,
  NiMaterialProperty: parseNiMaterialProperty,
  NiAlphaProperty: parseNiAlphaProperty,
  NiZBufferProperty: parseNiZBufferProperty,
  NiVertexColorProperty: parseNiVertexColorProperty,
  NiStencilProperty: parseNiStencilProperty,
  NiSpecularProperty: parseOneFlagProperty,
  NiDitherProperty: parseOneFlagProperty,
  NiShadeProperty: parseOneFlagProperty,
  NiFogProperty: parseNiFogProperty,
  NiStringExtraData: parseNiStringExtraData,
  NiIntegerExtraData: parseNiIntegerExtraData,
  NiBooleanExtraData: parseNiBooleanExtraData,
  NiTextKeyExtraData: parseNiTextKeyExtraData,
  NiArkShaderExtraData: parseNiArkShaderExtraData,
  NiBillboardNode: parseNiBillboardNode,
  NiArkBillboardNode: parseNiBillboardNode, // proven alias (08)
  NiSortAdjustNode: parseNiSortAdjustNode,
  NiKeyframeController: parseNiKeyframeController,
  NiKeyframeData: parseNiKeyframeData,
  NiFloatData: parseNiFloatData,
  NiPosData: parseNiPosData,
  NiColorData: parseNiColorData,
  NiUVData: parseNiUVData,
  NiVisData: parseNiVisData,
  NiPSysEmitterCtlrData: parseNiPSysEmitterCtlrData,
  NiTextureTransformController: parseNiTextureTransformController,
  NiFlipController: parseNiFlipController,
  NiVisController: parseNiVisController,
  NiAlphaController: parseNiAlphaController,
  NiMaterialColorController: parseNiMaterialColorController,
  NiLightColorController: parseNiLightColorController,
  NiUVController: parseNiUVController,
  NiLookAtController: parseNiLookAtController,
  NiPSysEmitterCtlr: parseNiPSysEmitterCtlr,
  NiPSysUpdateCtlr: parseNiPSysUpdateCtlr,
  NiPSysResetOnLoopCtlr: parseNiPSysResetOnLoopCtlr,
  NiPSysModifierActiveCtlr: parseNiPSysModifierActiveCtlr,
  NiSkinInstance: parseNiSkinInstance,
  NiSkinData: parseNiSkinData,
  NiSkinPartition: parseNiSkinPartition,
  NiPointLight: parseNiPointLight,
  NiSpotLight: parseNiSpotLight,
  NiDirectionalLight: parseNiDirectionalLight,
  NiAmbientLight: parseNiAmbientLight,
  NiTextureEffect: parseNiTextureEffect,
  NiCollisionData: parseNiCollisionData,
  NiParticleSystem: parseNiParticleSystem,
  NiMeshParticleSystem: parseNiMeshParticleSystem,
  NiPSysData: parseNiPSysData,
  NiMeshPSysData: parseNiMeshPSysData,
  NiPSysAgeDeathModifier: parseNiPSysAgeDeathModifier,
  NiPSysSpawnModifier: parseNiPSysSpawnModifier,
  NiPSysPositionModifier: parseNiPSysPositionModifier,
  NiPSysBoundUpdateModifier: parseNiPSysBoundUpdateModifier,
  NiPSysColorModifier: parseNiPSysColorModifier,
  NiPSysGrowFadeModifier: parseNiPSysGrowFadeModifier,
  NiPSysGravityModifier: parseNiPSysGravityModifier,
  NiPSysRotationModifier: parseNiPSysRotationModifier,
  NiPSysMeshUpdateModifier: parseNiPSysMeshUpdateModifier,
  NiPSysColliderManager: parseNiPSysColliderManager,
  NiPSysDragModifier: parseNiPSysDragModifier,
  NiPSysPlanarCollider: parseNiPSysPlanarCollider,
  NiPSysBoxEmitter: parseNiPSysBoxEmitter,
  NiPSysSphereEmitter: parseNiPSysSphereEmitter,
  NiPSysMeshEmitter: parseNiPSysMeshEmitter,
  NiSourceTexture: parseNiSourceTexture,
  NiPixelData: parseNiPixelData,
};

const TYPE_DECODE_STATUS = {
  NiArkViewportInfoExtraData: DECODE_STATUS.OPAQUE,
  NiArkAnimationExtraData: DECODE_STATUS.OPAQUE,
  NiVertexMorphExtraData: DECODE_STATUS.OPAQUE,
  NiArkTextureExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiArkImporterExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
};
for (const t of Object.keys(TYPE_PARSERS)) TYPE_DECODE_STATUS[t] = TYPE_DECODE_STATUS[t] ?? DECODE_STATUS.SUPPORTED;

// variable-ext blocks: prefix parsed, ext RAW to a closure-derived boundary.
const BOUNDARY_SEARCH_TYPES = new Set([
  'NiArkViewportInfoExtraData',
  'NiArkAnimationExtraData',
  'NiArkImporterExtraData',
  'NiVertexMorphExtraData',
  'NiMeshPSysData', // PSysData chain + undocumented mesh arrays (3 instances): RAW tail via search
]);

const MAX_ATTEMPTS = 200000;

// ---- closure-constrained boundary candidates (the s2 method, mirrored from
// PecNif10Reader.js; documented seeds FIRST) ----

// Per-type scan windows for the boundary search (documented ext bounds; 08):
// small-ext Ark blocks get tight windows (their exts are bounded and every
// corpus file carries them — a full-file scan per file was the batch's slow
// path); the morph payload is unbounded (measured up to ~200 KB) and scans
// the remaining file.
const BOUNDARY_SCAN_WINDOW = {
  NiArkImporterExtraData: 4096,      // documented ALWAYS-38B tail (seeded)
  NiArkAnimationExtraData: 16384,   // documented exts ≤ ~2.2 KB (G3C_BOUNDARY)
  NiArkViewportInfoExtraData: 8192, // documented exts ≤ 121 B + slack
  NiVertexMorphExtraData: Infinity, // unbounded (measured ~200 KB payloads)
  NiMeshPSysData: 16384,
};

function boundaryCandidates(bytes, dv, start, numBlocks, fileSize, seedSizes = [], scanWindow = Infinity) {
  const cands = [];
  const seen = new Set();
  const push = (rank, pos, method) => {
    if (pos < start || pos > fileSize || seen.has(pos)) return;
    seen.add(pos);
    cands.push({ rank, pos, method });
  };
  for (const sz of seedSizes) push(0, start + sz, `documented_size_${sz}B`);
  const window = Math.min(fileSize, start + scanWindow);
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
              scored.push({ rank: (ln >= 4 && ln <= 64) ? 0 : 1, pos, method: 'next_block_preamble' });
            }
          }
        }
      }
    }
    pos++;
  }
  const footerScanEnd = Math.min(fileSize - 4, start + scanWindow);
  for (let p = start; p <= footerScanEnd; p++) {
    const c = dv.getUint32(p, true);
    if (c <= numBlocks && p + 4 + 4 * c === fileSize) {
      scored.push({ rank: 0, pos: p, method: 'top_objects_footer' });
    }
    // NOTE: no "footer with tail" candidate class — scanning for [c][refs]
    // shapes anywhere in the tail flooded the candidate list (the 353595-class
    // tails are handled by the footer reader's recorded-tail fallback, which
    // applies whenever the LAST block ends at a valid footer).
  }
  scored.sort((a, b) => (a.rank - b.rank) || (a.pos - b.pos));
  for (const c of scored.slice(0, 8192)) push(c.rank, c.pos, c.method);
  return cands;
}

// ---- the parse with bounded backtracking (mirrors PecNif10Reader) ----

function parseHeader(s, payload) {
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new LoudError('no newline in header — LOUD FAIL');
  const text = String.fromCharCode(...payload.subarray(0, nl));
  s.seek(nl + 1);
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V10_1_0_0) {
    throw new LoudError(`version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — this reader implements ONLY NIF 10.1.0.0 (LOUD FAIL; version dispatch belongs to the adapter)`);
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
    versionRaw: '0x0A010000',
    versionString: '10.1.0.0',
    userVersion, numBlocks, numBlockTypes, blockTypes, blockTypeIndex, numGroups, groups,
    dataStartOffset: s.pos,
  };
}

function hexOfRange(bytes, start, end) {
  let h = '';
  for (let i = start; i < end; i++) h += bytes[i].toString(16).padStart(2, '0');
  return h;
}

function makeBlockRecord(index, type, decodeStatus, blockStart, blockEnd, fields) {
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
  }
  if (fields && 'children' in fields) {
    rec.children = fields.children;
    rec.effects = fields.effects;
  }
  if (fields && 'extraDataRefs' in fields) {
    rec.extraDataRefs = fields.extraDataRefs;
    rec.controllerRef = fields.controllerRef;
  }
  if (fields && 'propertyRefs' in fields) {
    rec.propertyRefs = fields.propertyRefs;
    rec.collisionObjectRef = fields.collisionObjectRef;
  }
  if (fields && 'dataRef' in fields) {
    rec.dataRef = fields.dataRef;
    rec.skinRef = fields.skinRef;
  }
  if (fields && 'geometry' in fields && fields.geometry) rec.geometry = fields.geometry;
  rec.fields = fields;
  return rec;
}

function decodeFrom(s, ctx, blockIndex, out) {
  const { header, payload, dv, state } = ctx;
  if (blockIndex === header.numBlocks) {
    try {
      const startPos = s.pos;
      const ntop = s.u32();
      if (ntop > header.numBlocks) return null;
      const tops = [];
      for (let i = 0; i < ntop; i++) {
        const t = s.i32();
        if (t < 0 || t >= header.numBlocks) return null; // top objects are real block refs
        tops.push(t);
      }
      if (s.pos === s.size) {
        return { topObjects: tops, numTopObjects: ntop, eofExact: true, tailStart: null, tailBytes: 0 };
      }
      // FALLBACK CLOSURE (measured corpus class — e.g. 353595.nif): a valid
      // TopObjects footer followed by TRAILING BYTES. The tail is recorded
      // RAW (length + range); its semantics are UNKNOWN and NOT interpreted
      // (observed content: v4-inline-style block data in some files). The
      // closure records eofExact=false with the measured tail; a strict
      // EOF-exact candidate always wins when it exists.
      void startPos;
      return {
        topObjects: tops, numTopObjects: ntop, eofExact: false,
        tailStart: s.pos, tailBytes: s.size - s.pos,
      };
    } catch { return null; }
  }
  // MEMOIZATION (sound: the decode from (blockIndex, s.pos) is a pure function
  // of the bytes ahead — the same position can never succeed in one branch and
  // fail in another; out[] content never influences parsing). This converts
  // the nested-boundary-block candidate product from exponential to linear.
  const memoKey = blockIndex * 4294967296 + s.pos;
  if (state.failedMemo?.has(memoKey)) return null;
  const result = decodeFromInner(s, ctx, blockIndex, out);
  if (result === null) (state.failedMemo ??= new Set()).add(memoKey);
  return result;
}

function decodeFromInner(s, ctx, blockIndex, out) {
  const { header, payload, dv, state } = ctx;
  if (++state.attempts > MAX_ATTEMPTS) {
    throw new LoudError(`backtracking attempts exceeded ${MAX_ATTEMPTS} — aborting (input does not close under the documented layouts)`);
  }
  const start = s.pos;
  let preamble;
  try { preamble = s.u32(); } catch { return null; }
  if (preamble !== 0) {
    if (ctx.debugTrace) ctx.debugTrace.push({ blockIndex, type: header.blockTypes[header.blockTypeIndex[blockIndex]] ?? '?', start, preambleFail: true, preamble });
    return null;
  }
  ctx.state.maxBlock = Math.max(ctx.state.maxBlock ?? 0, blockIndex);
  const typeIdx = header.blockTypeIndex[blockIndex];
  const type = header.blockTypes[typeIdx];
  if (!type || !(type in TYPE_PARSERS || type === 'NiArkTextureExtraData' || BOUNDARY_SEARCH_TYPES.has(type))) {
    throw new LoudError(`block ${blockIndex}: UNKNOWN type "${type}" (index ${typeIdx}) — no parser registered (LOUD FAIL; context: offset ${start})`);
  }
  const decodeStatus = TYPE_DECODE_STATUS[type] ?? DECODE_STATUS.SUPPORTED;

  if (BOUNDARY_SEARCH_TYPES.has(type)) {
    let prefix;
    try { prefix = parseBoundaryPrefix(s, type); } catch { return null; }
    const extStart = s.pos;
    const seeds = documentedExtSeeds(type, prefix, s.size - extStart);
    const cands = boundaryCandidates(payload, dv, extStart, header.numBlocks, s.size, seeds, BOUNDARY_SCAN_WINDOW[type] ?? 16384);
    // The NEXT block's expected shape — a cheap structural pre-filter that
    // rejects float-noise candidates inside large opaque payloads (the
    // NiVertexMorphExtraData payloads reach ~200 KB of quantized floats whose
    // random [u32 0 + name-shape] collisions flooded the candidate list).
    const nextTypeIdx = header.blockTypeIndex[blockIndex + 1];
    const nextType = nextTypeIdx != null ? header.blockTypes[nextTypeIdx] : null;
    const nextTypeParsable = nextType && TYPE_PARSERS[nextType]
      && !BOUNDARY_SEARCH_TYPES.has(nextType) && nextType !== 'NiArkTextureExtraData';
    for (const cand of cands) {
      if (cand.pos < extStart || cand.pos > s.size - 4) continue;
      // pre-filter 1: the next block's preamble must be u32 0 (also validates seeds).
      if (dv.getUint32(cand.pos, true) !== 0) continue;
      // pre-filter 2: the next FIXED block must parse structurally at cand.pos+4.
      // The peek is WINDOWED (≤2048 B): array-heavy next blocks (e.g. NiTriShapeData
      // with hundreds of thousands of vertices) throw early instead of costing a
      // full-geometry parse per candidate; small structural blocks validate fully.
      if (nextTypeParsable && cand.pos + 4 < s.size) {
        const windowLen = Math.min(payload.length - (cand.pos + 4), 2048);
        const peek = new NifStream(payload.subarray(cand.pos + 4, cand.pos + 4 + windowLen), s.source);
        try { TYPE_PARSERS[nextType](peek); } catch {
          // Rejection ONLY on structural failure INSIDE the window; a parse that
          // consumed the whole window is inconclusive (the full recursion decides).
          if (peek.pos < windowLen) continue;
        }
      }
      s.seek(cand.pos);
      state.decisions.push({
        block: blockIndex, type, extStart, extEnd: cand.pos,
        extLength: cand.pos - extStart, method: cand.method,
      });
      out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, cand.pos, {
        ...prefix,
        opaque: {
          extHex: hexOfRange(payload, extStart, cand.pos),
          extStart, extEnd: cand.pos, extLength: cand.pos - extStart,
          boundaryMethod: cand.method,
          note: 'extension bytes recorded RAW — content UNDETERMINED beyond the boundary (DETECTION_UNRESOLVED for this channel)',
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
    for (const variant of ['PREFIX3', 'NOPREFIX']) {
      s.seek(start + 4);
      let fields;
      try { fields = parseNiArkTextureExtraData(s, variant); } catch { continue; }
      const end = s.pos;
      state.decisions.push({ block: blockIndex, type, variantLayout: variant });
      out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, end, fields);
      const sub = decodeFrom(s, ctx, blockIndex + 1, out);
      if (sub) return sub;
      state.decisions.pop();
      out[blockIndex] = null;
    }
    return null;
  }

  s.seek(start + 4);
  let fields;
  try {
    fields = TYPE_PARSERS[type](s);
  } catch (e) {
    if (e instanceof LoudError) throw e; // fail-closed conditions are never backtracked
    if (ctx.debugTrace) {
      ctx.debugTrace.push({ blockIndex, type, start, err: String(e?.message ?? e).slice(0, 200), pos: s.pos });
    }
    s.seek(start);
    return null;
  }
  const end = s.pos;
  if (ctx.debugTrace) ctx.debugTrace.push({ blockIndex, type, start, end });
  out[blockIndex] = makeBlockRecord(blockIndex, type, decodeStatus, start, end, fields);
  const sub = decodeFrom(s, ctx, blockIndex + 1, out);
  if (sub) return sub;
  out[blockIndex] = null;
  return null;
}

/**
 * readNif10Corpus — parse a NIF 10.1.0.0 payload to FULL closure or fail loudly.
 * Emits the same reader-result shape as readNif10 (PecSceneIR-compatible).
 */
export function readNif10Corpus(payload, opts = {}) {
  const sourceName = opts.sourceName ?? 'input.nif';
  const s = new NifStream(payload, sourceName);
  const header = parseHeader(s, payload);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ctx = {
    header, payload, dv, state: { attempts: 0, decisions: [] },
    debugTrace: Array.isArray(opts.debugTrace) ? opts.debugTrace : (opts.debugTrace === true ? [] : null),
  };
  const out = new Array(header.numBlocks).fill(null);
  const footer = decodeFrom(s, ctx, 0, out);
  if (!footer) {
    const lastType = header.blockTypes[header.blockTypeIndex[Math.min(state_lastIndex(out), header.numBlocks - 1)] ?? 0];
    const err = new LoudError(
      `CLOSURE_FAIL: no candidate set closed ${sourceName} under the documented layouts ` +
      `(attempts=${ctx.state.attempts}, decisionsTried=${ctx.state.decisions.length}, lastUnclosedContext=${lastType ?? '?'}, maxBlockReached=${ctx.state.maxBlock ?? -1}) — LOUD FAIL`);
    if (ctx.debugTrace) err.debugTrace = ctx.debugTrace;
    throw err;
  }
  if (out.some((b) => b == null)) {
    throw new LoudError('internal: closure returned but some blocks are unset — LOUD FAIL');
  }
  return {
    readerVersion: PEC_NIF10_CORPUS_READER_VERSION,
    sourceName,
    sourceBytes: payload,
    header,
    blocks: out,
    footer,
    closure: {
      eofExact: footer.eofExact,
      numBlocksDecoded: out.length,
      attempts: ctx.state.attempts,
      decisions: ctx.state.decisions,
      tailBytes: footer.tailBytes,
      tailStart: footer.tailStart,
      tailNote: footer.tailBytes > 0
        ? 'TRAILING_BYTES_RECORDED_RAW: the TopObjects footer closed the block stream but ' +
        `${footer.tailBytes} bytes follow it (range [${footer.tailStart},${payload.length})); ` +
        'content recorded RAW — semantics UNKNOWN (observed in some corpus files as v4-inline-style data); NOT parsed, NOT claimed'
        : null,
    },
  };
}

function state_lastIndex(out) {
  for (let i = out.length - 1; i >= 0; i--) if (out[i] == null) return i + 1;
  return 0;
}

/** Geometry fingerprints (REUSE LABEL: identical contract to PecNif10Reader's
 * attachGeometryFingerprints — round-trip proof of decoded arrays). */
export function attachGeometryFingerprints(readerResult, sha256) {
  if (typeof sha256 !== 'function') {
    throw new LoudError('attachGeometryFingerprints requires an injected sha256(bytes) function');
  }
  const perMesh = [];
  for (const b of readerResult.blocks) {
    if (!b.geometry) continue;
    const g = b.geometry;
    const rec = { dataBlock: b.index, type: b.type, numVertices: g.numVertices, numTriangles: g.numTriangles };
    if (g.vertexRange && g.positions) {
      const rangeBytes = readerResult.sourceBytes
        ? readerResult.sourceBytes.subarray(g.vertexRange.start, g.vertexRange.end)
        : null;
      const repacked = new Uint8Array(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength);
      rec.vertexPositionsF32leSha256 = sha256(repacked);
      g.vertexPositionsF32leSha256 = rec.vertexPositionsF32leSha256;
      if (rangeBytes) {
        rec.vertexRangeSha256 = sha256(rangeBytes);
        rec.vertexRoundtripExact = rangeBytes.byteLength === repacked.byteLength && sha256(rangeBytes) === rec.vertexPositionsF32leSha256;
      }
    }
    if (g.indexRange && g.indices) {
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
