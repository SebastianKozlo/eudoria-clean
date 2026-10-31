// NifModelReader41.js — JOB W09_NIF41_ADAPTER (attempt W09_a1, 2026-10-30).
//
// THE DEDICATED NIF 4.1.0.12 ADAPTER — a SEPARATE format module (the W09 CEL:
// NIF 4.1.0.12 treated as its own format; shared semantics with the 10.1
// reader ONLY where proven). NifModelReader.js (the 10.1.0.0 witness reader)
// is NOT modified — its version gate stays untouched and 4.1 still
// LOUD-FAILs there BY DESIGN (negative control preserved in the W09 unit
// test).
//
// METHOD BASIS (proven, read-only): the frozen R61 corpus (private local
//   audit baseline PE_R61_FROZEN_BASELINE_20260828, module 01_source):
//     pe_header.py / pe_stream.py / pe_version.py / pe_block_reader.py /
//     pe_standard_blocks.py
// — the SAME oracle-lineage method already engine-validated 22/22 on
// 218757_stripped (W08 COMPARE_218757.json, R61 peReader vs stock Gamebryo
// 1.2 engine oracle). Semantics were PORTED to JS here and the block
// boundaries were re-validated per fixture (218757_stripped,
// 296445_stripped): every block's blockEnd must equal the next block's
// rttiStart (unit test gate B5), i.e. NO carry/underflow anywhere.
//
// v4.1.0.12 FORMAT (R61 canon, frozen M1B4 truth matrix):
//   header: HeaderText (up to first \n) + Version(u32) + NumBlocks(u32)
//           [NO userVersion, NO type table — inline RTTI per block]
//   blocks: per block: SizedString RTTI type name + class payload
//           [NO v10 u32=0 preamble]
//   boolean: 1 byte (4.1.0.12 >= 0x04010000; 4-byte booleans are 4.0.0.2 only)
//   NiObjectNET v4 (< 5.0.0.11): Name(SizedString) + ExtraData(Ref, SINGLE
//           i32 — NOT the v10 u32-count array) + Controller(Ref)
//   NiAVObject v4 (< 10.0.1.0): Flags(u16) + Translation(vec3) +
//           Rotation(mat33) + Scale(f32) + Velocity(vec3 — v4 ONLY) +
//           NumProperties(u32) + Properties(Ref[]) + HasBoundingBox(bool)
//           [+ BoundingBox: u32 + vec3 + mat33 + f32 if set]
//           [NO v10 CollisionObject ref]
//   NiTriShape v4: NET + AV + DataRef + SkinRef [NO v10 hasShader]
//   NiTriShapeData v4 (C9-B CONFIRMED): NumVertices(u16) + HasVertices(bool)
//           + vertices + HasNormals(bool) + normals + center + radius +
//           HasVertexColors(bool) + colors + NumUvSets(u16 — LATE, after
//           colors; NO hasUv for 0x0401000C) + uvSets[NumUvSets & 63] +
//           NumTriangles(u16) + NumTrianglePoints(u32) + triangles
//           (UNCONDITIONAL — no v10 hasTriangles flag) + NumMatchGroups +
//           matchGroups. [NO v10 keepFlags/compressFlags/consistencyFlags;
//           numUvSets is EARLY in v10, LATE in v4]
//   NiMaterialProperty v4: NET + Flags(u16 — PRESENT for 0x0401000C <=
//           0x0A000102; the v10 reader emits no flags field) + ambient +
//           diffuse + specular + emissive + glossiness + alpha
//   NiZBufferProperty v4: NET + flags(u16) + function(u32, >= 0x0401000C)
//   NiTexturingProperty v4 (C5-B G1 CONFIRMED 693/693): name + extraData +
//           controller + texFlags(u16) + applyMode(u32) + textureCount(u32)
//           + per slot: has(u8); if 1: source(i32) + clamp(u32) +
//           filter(u32) + uvSet(u32) + ps2L(i16) + ps2K(i16) + unk1(u16)
//           [TexDesc = 22B; v10 instead has tail_A/tail_B/transform_present
//           and bump/trailing payloads]
//   NiStringExtraData v4: NiExtraData base = next_link(i32, NO name — name
//           is a v10 10.0.1.0 addition) + stringData(SizedString)
//   NiTextureEffect v4 (M1D-11 niflib-confirmed): NET + AV + [EMPTY
//           NiDynamicEffect layer for 0x0401000C] + mat33 + vec3 +
//           filtering(u32) + clamping(u32) + type(u32) + coordGen(u32) +
//           sourceRef(i32) + clippingPlane(u8) + unknownVec(vec3) +
//           unknownFloat(f32) + ps2L(i16) + ps2K(i16) + unknownShort(i16 —
//           v4 boundary-exact; NOT in v10)
//   NiUVController (C19): NiTimeController(nextController i32 + flags u16 +
//           frequency/phase/startTime/stopTime f32 + target i32) +
//           unknownShort(u16) + dataRef(i32)
//   NiUVData (C20): 4 x KeyGroup<float> (numKeys u32 [+ interpolation u32
//           if nonzero] + keys {time f32, value f32 [+ forward/backward f32
//           if QUADRATIC] [+ tension/bias/continuity f32 if TBC]};
//           CONST(5) treated as LINEAR)
//
// TYPED IR CONTRACT (shared with NifModelReader.js 10.1 — SAME names and
// the SAME FILE-ORDER byte-hex f32 convention for extraction fields, so
// the inspector consumes BOTH readers with one code path):
//   header: { text, versionRaw, versionString, numBlocks, dataStartOffset }
//           [10.1 additionally: userVersion, blockTypes, blockTypeIndex,
//            numGroups, groups — 4.1 has none of these]
//   blocks[i]: { index, type, rttiStart, payloadStart, blockEnd, fields }
//   shared fields: name, extraData, controller, flags, translation,
//           rotation, scale, numProperties, properties, numChildren,
//           children, numEffects, effects, dataRef, skinRef, ambient,
//           diffuse, specular, emissive, glossiness, alpha, alphaFlags,
//           alphaThreshold, textureCount, textures[].{has,source,clamp,
//           filter,uv_set}
//   4.1-ONLY fields (documented differences): velocity, hasBoundingBox,
//           boundingBox, materialFlags (NiMaterialProperty.flags),
//           texFlags/applyMode (vs 10.1 fieldA/fieldB), textures[].ps2_l/
//           ps2_k/unk1 (vs 10.1 tail_A/tail_B/transform_present), extraData
//           is a SINGLE int ref (not an array), numUvSets position LATE in
//           NiTriShapeData, unknownShort/uvGroups on UV blocks,
//           nextExtraData on NiStringExtraData (v4 link, no name).
//
// UNKNOWN BLOCK POLICY (W09 CEL — deliberately NOT the R61 FAIL_CLOSED):
//   an unknown RTTI type is recorded OPAQUE with offset + span + raw hex;
//   the boundary is found by a KNOWN-RTTI-ANCHORED search only (u32 length
//   + exact byte match against the known 4.1 type-name set) — NEVER a
//   printable-string guess. If no anchored boundary exists, the opaque
//   block spans to EOF and parsing stops (recorded, not silently skipped).
//   Both fixtures parse with ZERO opaque blocks (unit test gate).

const NIF_V4_1_0_12 = 0x0401000C;

// Block types implemented by this adapter (the union needed by the two W09
// fixtures + the R61-confirmed v4 standard set they exercise). Anything
// else hits the OPAQUE path above.
const KNOWN_V41_TYPES = new Set([
  'NiNode', 'NiTriShape', 'NiTriShapeData', 'NiTexturingProperty',
  'NiMaterialProperty', 'NiAlphaProperty', 'NiZBufferProperty',
  'NiVertexColorProperty', 'NiStringExtraData', 'NiTextureEffect',
  'NiUVController', 'NiUVData',
]);

// Anchored-boundary candidate set: the implemented types plus the other
// standard 4.x type names (R61 _VIEWPORT_KNOWN_TYPES lineage) — used ONLY
// to find the END of an unknown opaque block (exact byte match, no
// interpretation, no printable-string heuristics).
const ANCHOR_RTTI_NAMES = [
  'NiNode', 'NiTriShape', 'NiTriShapeData', 'NiTriStripsData',
  'NiMaterialProperty', 'NiAlphaProperty', 'NiZBufferProperty',
  'NiBillboardNode', 'NiStringExtraData', 'NiSourceTexture',
  'NiKeyframeController', 'NiStencilProperty', 'NiTexturingProperty',
  'NiArkAnimationExtraData', 'NiArkImporterExtraData',
  'NiArkTextureExtraData', 'NiArkViewportInfoExtraData',
  'NiArkShaderExtraData', 'NiArkBillboardNode', 'NiTextureEffect',
  'NiTextKeyExtraData', 'NiFlipController', 'NiTextureTransformController',
  'NiVertexColorProperty', 'NiUVController', 'NiVisController',
  'NiKeyframeData', 'NiBSAnimationNode', 'NiFloatData', 'NiUVData',
  'NiSpecularProperty', 'NiShadeProperty', 'NiDitherProperty', 'NiFogProperty',
  'NiSortAdjustNode', 'NiSkinInstance', 'NiSkinData', 'NiSkinPartition',
  'NiVisData', 'NiPointLight', 'NiSpotLight', 'NiDirectionalLight',
  'NiAmbientLight', 'NiCollisionData', 'NiLookAtController',
  'NiIntegerExtraData', 'NiBooleanExtraData', 'NiPosData', 'NiColorData',
  'NiKeyframeData', 'NiCamera',
];

class NifStream41 {
  constructor(bytes, sourceName = 'model41.nif') {
    this.bytes = bytes;
    this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.pos = 0;
    this.source = sourceName;
  }
  get size() { return this.bytes.length; }
  get remaining() { return this.size - this.pos; }
  _check(n) {
    if (this.pos + n > this.size) {
      throw new Error(`[NifModelReader41] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[NifModelReader41] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  /** f32 as IEEE-754 bit pattern — FILE-ORDER byte hex (8 chars), the SAME
   * convention as NifModelReader.js (struct.pack('<f', v).hex() parity). */
  f32bits() { this._check(4); let h = ''; for (let i = 0; i < 4; i++) h += this.bytes[this.pos + i].toString(16).padStart(2, '0'); this.pos += 4; return h; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  boolean() { return this.u8() !== 0; } // 4.1.0.12: 1-byte booleans (>= 0x04010000)
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[NifModelReader41] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3bits() { return [this.f32bits(), this.f32bits(), this.f32bits()]; }
  mat33bits() { return [this.vec3bits(), this.vec3bits(), this.vec3bits()]; }
  rawHex(n) { this._check(n); let s = ''; for (let i = 0; i < n; i++) s += this.bytes[this.pos + i].toString(16).padStart(2, '0'); this.pos += n; return s; }
}

const bitsToF32 = (hex) => {
  const u = new Uint32Array(1);
  const b = new Uint8Array(u.buffer);
  for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
  return new Float32Array(u.buffer)[0];
};

// ---- v4 base layers (R61 pe_standard_blocks parity, bit-hex IR emission) ----

function readObjectNetV4(s) {
  const name = s.sizedString();
  const extraData = s.i32();   // v4: SINGLE extra-data link (NOT the v10 array)
  const controller = s.i32();
  return { name, extraData, controller };
}

function readAVObjectV4(s) {
  const flags = s.u16();
  const translation = s.vec3bits();
  const rotation = s.mat33bits();
  const scale = s.f32bits();
  const velocity = s.vec3bits();         // v4 ONLY (< 10.0.1.0)
  const numProperties = s.u32();
  if (numProperties > 10000) throw new Error(`[NifModelReader41] impossible numProperties ${numProperties}`);
  const properties = [];
  for (let i = 0; i < numProperties; i++) properties.push(s.i32());
  const hasBoundingBox = s.boolean();    // v4 ONLY
  let boundingBox = null;
  if (hasBoundingBox) {
    boundingBox = {
      unknownInt: s.u32(),
      translation: s.vec3bits(),
      rotation: s.mat33bits(),
      radius: s.f32bits(),
    };
  }
  // NO v10 collisionObject ref in 4.1
  return { flags, translation, rotation, scale, velocity, numProperties, properties, hasBoundingBox, boundingBox };
}

function parseNiNode(s) {
  const net = readObjectNetV4(s);
  const av = readAVObjectV4(s);
  const numChildren = s.u32();
  const children = [];
  for (let i = 0; i < numChildren; i++) children.push(s.i32());
  const numEffects = s.u32();
  const effects = [];
  for (let i = 0; i < numEffects; i++) effects.push(s.i32());
  return { ...net, ...av, numChildren, children, numEffects, effects };
}

function parseNiTriShape(s) {
  const net = readObjectNetV4(s);
  const av = readAVObjectV4(s);
  const dataRef = s.i32();
  const skinRef = s.i32();
  // NO hasShader (v10-only, 0x0A000100..0x14010003)
  return { ...net, ...av, dataRef, skinRef };
}

function parseNiTriShapeDataV4(s) {
  const numVertices = s.u16();
  const hasVertices = s.boolean();
  const verticesBits = [];
  if (hasVertices) for (let i = 0; i < numVertices; i++) verticesBits.push(...s.vec3bits());
  const hasNormals = s.boolean();
  const normalsBits = [];
  if (hasNormals) for (let i = 0; i < numVertices; i++) normalsBits.push(...s.vec3bits());
  const center = s.vec3bits();
  const radius = s.f32bits();
  const hasVertexColors = s.boolean();
  const vertexColorsBits = [];
  if (hasVertexColors) for (let i = 0; i < numVertices; i++) vertexColorsBits.push(...s.vec3bits(), s.f32bits()); // Color4 = 4 x f32
  const numUvSets = s.u16();             // LATE in v4 (after colors)
  // NO hasUv for 0x0401000C (> 0x04000002)
  const uvCount = numUvSets & 63;
  if (uvCount > 8) throw new Error(`[NifModelReader41] impossible uvCount ${uvCount} (numUvSets=0x${numUvSets.toString(16)})`);
  const uvSetsBits = [];
  for (let set = 0; set < uvCount; set++) {
    const bits = [];
    for (let i = 0; i < numVertices; i++) bits.push(s.f32bits(), s.f32bits());
    uvSetsBits.push(bits);
  }
  const numTriangles = s.u16();
  const numTrianglePoints = s.u32();
  if (numTrianglePoints > 5_000_000) throw new Error(`[NifModelReader41] impossible numTrianglePoints ${numTrianglePoints}`);
  const triangles = [];
  for (let i = 0; i < numTriangles; i++) triangles.push([s.u16(), s.u16(), s.u16()]); // UNCONDITIONAL in v4
  const numMatchGroups = s.u16();
  if (numMatchGroups > 65535) throw new Error(`[NifModelReader41] impossible numMatchGroups ${numMatchGroups}`);
  const matchGroups = [];
  for (let g = 0; g < numMatchGroups; g++) {
    const count = s.u16();
    const indices = [];
    for (let j = 0; j < count; j++) indices.push(s.u16());
    matchGroups.push({ count, indices });
  }
  return {
    numVertices, hasVertices, hasNormals, center, radius, hasVertexColors,
    numUvSets, uvCount, numTriangles, numTrianglePoints, numMatchGroups, matchGroups,
    verticesBits, normalsBits, vertexColorsBits, uvSetsBits, triangles,
  };
}

function parseNiMaterialProperty(s) {
  const net = readObjectNetV4(s);
  const materialFlags = s.u16(); // 4.1-ONLY (0x0401000C <= 0x0A000102)
  const ambient = s.vec3bits();
  const diffuse = s.vec3bits();
  const specular = s.vec3bits();
  const emissive = s.vec3bits();
  const glossiness = s.f32bits();
  const alpha = s.f32bits();
  return { ...net, materialFlags, ambient, diffuse, specular, emissive, glossiness, alpha };
}

function parseNiAlphaProperty(s) {
  const net = readObjectNetV4(s);
  const alphaFlags = s.u16();
  const alphaThreshold = s.u8();
  return { ...net, alphaFlags, alphaThreshold };
}

function parseNiZBufferProperty(s) {
  const net = readObjectNetV4(s);
  const flags = s.u16();
  const fn = s.u32(); // function (>= 0x0401000C: PRESENT in 4.1)
  return { ...net, flags, function: fn };
}

function parseNiVertexColorProperty(s) {
  const net = readObjectNetV4(s);
  const flags = s.u16();
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32(); // PE-specific extension (M1D-32: always consumed)
  return { ...net, flags, vertexMode, lightingMode, unknownPeField };
}

function parseNiTexturingPropertyV4(s) {
  const net = readObjectNetV4(s);
  const texFlags = s.u16();
  const applyMode = s.u32();
  const textureCount = s.u32();
  if (textureCount > 32) throw new Error(`[NifModelReader41] impossible textureCount ${textureCount}`);
  const textures = [];
  for (let i = 0; i < textureCount; i++) {
    const has = s.u8();
    if (has !== 0 && has !== 1) throw new Error(`[NifModelReader41] texprop slot ${i}: invalid Has=${has} — LOUD FAIL`);
    if (has === 1) {
      const source = s.i32();
      const clamp = s.u32();
      const filter = s.u32();
      const uv_set = s.u32();
      const ps2_l = s.i16(); // 4.1-ONLY TexDesc fields
      const ps2_k = s.i16();
      const unk1 = s.u16();
      textures.push({ has: 1, source, clamp, filter, uv_set, ps2_l, ps2_k, unk1 });
    } else {
      textures.push({ has: 0 });
    }
  }
  return { ...net, texFlags, applyMode, textureCount, textures };
}

function parseNiStringExtraDataV4(s) {
  const nextExtraData = s.i32(); // v4 NiExtraData base: link, NO name
  const stringData = s.sizedString();
  return { nextExtraData, stringData };
}

function parseNiTextureEffectV4(s) {
  const net = readObjectNetV4(s);
  const av = readAVObjectV4(s);
  // NiDynamicEffect layer for 0x0401000C: EMPTY
  // (0x0401000C > 0x04000002: no list pointers; < 0x0A010000: no affected nodes)
  const modelProjectionMatrix = s.mat33bits();
  const modelProjectionTransform = s.vec3bits();
  const textureFiltering = s.u32();
  const textureClamping = s.u32();
  const textureType = s.u32();
  const coordinateGenerationType = s.u32();
  const sourceTextureRef = s.i32();
  const clippingPlane = s.u8();
  const unknownVector = s.vec3bits();
  const unknownFloat = s.f32bits();
  const ps2_l = s.i16();
  const ps2_k = s.i16();
  const unknownShort = s.i16(); // 4.1-ONLY (<= 0x0401000C, boundary-exact)
  return {
    ...net, ...av, modelProjectionMatrix, modelProjectionTransform,
    textureFiltering, textureClamping, textureType, coordinateGenerationType,
    sourceTextureRef, clippingPlane, unknownVector, unknownFloat, ps2_l, ps2_k, unknownShort,
  };
}

function parseNiUVController(s) {
  // NiTimeController (NOT NiObjectNET — no name/extraData/controller fields)
  const nextController = s.i32();
  const flags = s.u16();
  const frequency = s.f32bits();
  const phase = s.f32bits();
  const startTime = s.f32bits();
  const stopTime = s.f32bits();
  const target = s.i32();
  const unknownShort = s.u16();
  const dataRef = s.i32();
  return { nextController, flags, frequency, phase, startTime, stopTime, target, unknownShort, dataRef };
}

function readFloatKeyGroup(s) {
  const numKeys = s.u32();
  if (numKeys > 100000) throw new Error(`[NifModelReader41] impossible numKeys ${numKeys}`);
  const group = { numKeys, interpolation: 0, keys: [] };
  if (numKeys !== 0) {
    let interp = s.u32();
    group.interpolation = interp;
    if (interp === 5) interp = 1; // CONST -> LINEAR
    if (interp !== 1 && interp !== 2 && interp !== 3) {
      throw new Error(`[NifModelReader41] unsupported key interpolation ${interp} — LOUD FAIL`);
    }
    const keys = [];
    for (let i = 0; i < numKeys; i++) {
      const key = { time: s.f32bits(), value: s.f32bits() };
      if (interp === 2) { key.forward = s.f32bits(); key.backward = s.f32bits(); }
      else if (interp === 3) { key.tension = s.f32bits(); key.bias = s.f32bits(); key.continuity = s.f32bits(); }
      keys.push(key);
    }
    group.keys = keys;
  }
  return group;
}

function parseNiUVData(s) {
  const uvGroups = [readFloatKeyGroup(s), readFloatKeyGroup(s), readFloatKeyGroup(s), readFloatKeyGroup(s)];
  return { uvGroups };
}

const V41_PARSERS = {
  'NiNode': parseNiNode,
  'NiTriShape': parseNiTriShape,
  'NiTriShapeData': parseNiTriShapeDataV4,
  'NiMaterialProperty': parseNiMaterialProperty,
  'NiAlphaProperty': parseNiAlphaProperty,
  'NiZBufferProperty': parseNiZBufferProperty,
  'NiVertexColorProperty': parseNiVertexColorProperty,
  'NiTexturingProperty': parseNiTexturingPropertyV4,
  'NiStringExtraData': parseNiStringExtraDataV4,
  'NiTextureEffect': parseNiTextureEffectV4,
  'NiUVController': parseNiUVController,
  'NiUVData': parseNiUVData,
};

// ---- unknown-block OPAQUE boundary (KNOWN-RTTI-ANCHORED only) ----
// Scans forward for: u32 len (1..256) + len bytes that EXACTLY equal one of
// the ANCHOR_RTTI_NAMES. This is an exact-match structural anchor, NOT a
// printable-string heuristic; nothing inside the opaque span is interpreted.
function findKnownRttiBoundary(s, searchStart) {
  const fileEnd = s.size;
  const anchors = [];
  for (const name of ANCHOR_RTTI_NAMES) {
    const nb = new Uint8Array(name.length);
    for (let i = 0; i < name.length; i++) nb[i] = name.charCodeAt(i);
    anchors.push(nb);
  }
  let pos = searchStart;
  outer: while (pos + 8 <= fileEnd) {
    const nl = s.dv.getInt32(pos, true);
    if (nl >= 1 && nl <= 256 && pos + 4 + nl <= fileEnd) {
      for (const nb of anchors) {
        if (nb.length !== nl) continue;
        let ok = true;
        for (let i = 0; i < nl; i++) { if (s.bytes[pos + 4 + i] !== nb[i]) { ok = false; break; } }
        if (ok) return pos; // next block's RTTI start
      }
    }
    pos++;
    continue outer;
  }
  return -1;
}

/**
 * parseModel41 — parse a NIF 4.1.0.12 payload into the typed IR.
 * @param {Uint8Array} payload raw NIF bytes (fixture / era container entry)
 * @param {string} sourceName
 * @returns {{ extraction: object, renderModel: object }}
 *   extraction: canonical 4.1 extraction (header, blocks with per-block byte
 *     spans, tail) — same typed contract as the 10.1 witness extraction.
 *   renderModel: multi-shape render model (4.1 assets carry many shapes):
 *     shapes[] with geometry arrays + resolved material/alpha/texture
 *     properties + numeric local/world TRS, plus the decoded controller
 *     blocks (NiUVController/NiUVData are implemented 4.1 controller types).
 */
export function parseModel41(payload, sourceName = 'model41.nif') {
  const s = new NifStream41(payload, sourceName);

  // ---- header ----
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new Error('[NifModelReader41] no newline in header — LOUD FAIL');
  const headerText = String.fromCharCode(...payload.subarray(0, nl));
  s.seek(nl + 1);
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V4_1_0_12) {
    throw new Error(`[NifModelReader41] version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — this adapter implements ONLY NIF 4.1.0.12 (0x0401000c); LOUD FAIL`);
  }
  const numBlocks = s.u32();
  if (numBlocks > 100000) throw new Error(`[NifModelReader41] impossible numBlocks ${numBlocks}`);
  const dataStartOffset = s.pos;

  const extraction = {
    schema: 'w09-nif41-canonical-extraction-v1',
    adapter: 'NifModelReader41 (src/pesource/NifModelReader41.js — dedicated NIF 4.1.0.12 adapter; R61-frozen-method semantics port, per-fixture boundary-validated)',
    formatFamily: 'NIF 4.1.0.12 (inline RTTI, no type table, no block preamble, 1-byte booleans)',
    source: { entryName: sourceName },
    header: {
      text: headerText,
      versionRaw: `0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`,
      versionString: '4.1.0.12',
      numBlocks,
      dataStartOffset,
    },
    blocks: [],
    opaqueBlocks: [],
    fileTailBytesHex: null,
    fileTailBytesLen: null,
  };

  // ---- blocks (inline RTTI dispatch) ----
  for (let blockIndex = 0; blockIndex < numBlocks; blockIndex++) {
    const rttiStart = s.pos;
    const type = s.sizedString();
    const parser = V41_PARSERS[type];
    if (!parser || !KNOWN_V41_TYPES.has(type)) {
      // UNKNOWN BLOCK -> OPAQUE (W09 CEL): record offset + span + raw hex via
      // the known-RTTI-anchored boundary; NO printable-string guessing, NO
      // interpretation of the span, parsing continues at the anchored boundary.
      const opaqueStart = rttiStart;
      const boundary = findKnownRttiBoundary(s, s.pos);
      const opaqueEnd = boundary >= 0 ? boundary : s.size;
      const span = opaqueEnd - opaqueStart;
      let rawCapped = '';
      for (let i = 0; i < Math.min(span, 4096); i++) rawCapped += s.bytes[opaqueStart + i].toString(16).padStart(2, '0');
      extraction.blocks.push({
        index: blockIndex, type, rttiStart, payloadStart: rttiStart, blockEnd: opaqueEnd,
        opaque: true, offset: opaqueStart, span,
        boundaryMethod: boundary >= 0 ? 'known_rtti_anchored' : 'eof_no_anchor',
        rawHexCapped: rawCapped,
        rawHexTruncated: span > 4096,
        fields: null,
      });
      extraction.opaqueBlocks.push({ index: blockIndex, type, offset: opaqueStart, span, boundaryMethod: boundary >= 0 ? 'known_rtti_anchored' : 'eof_no_anchor' });
      s.seek(opaqueEnd);
      if (boundary < 0) {
        // No anchored boundary: the rest of the file is this opaque block.
        // Record loudly and stop (no silent skip, no invented structure).
        extraction.parseStatus = 'STOPPED_OPAQUE_NO_BOUNDARY';
        extraction.stoppedAtBlock = blockIndex;
        break;
      }
      continue;
    }
    const payloadStart = s.pos;
    const fields = parser(s);
    extraction.blocks.push({
      index: blockIndex, type, rttiStart, payloadStart, blockEnd: s.pos,
      opaque: false, fields,
    });
  }

  // ---- tail (bytes after the last block — recorded raw, semantics unknown) ----
  const tailLen = s.size - s.pos;
  let tailHex = '';
  for (let i = 0; i < tailLen; i++) tailHex += payload[s.pos + i].toString(16).padStart(2, '0');
  extraction.fileTailBytesHex = tailHex;
  extraction.fileTailBytesLen = tailLen;
  if (!extraction.parseStatus) extraction.parseStatus = 'PASS';

  const renderModel = buildRenderModel41(extraction);
  return { extraction, renderModel };
}

/** NiTransform compose parity (niTransformAdapter.mjs compose()):
 * (P o C).s = Ps*Cs, .R = P.R*C.R, .t = Pt + P.R(Ps*Ct) — row-dot rotate,
 * NO transpose (the repo's corrected semantics). */
function composeTRS(P, C) {
  const R = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
    R[i][j] = P.rotation[i][0] * C.rotation[0][j] +
              P.rotation[i][1] * C.rotation[1][j] +
              P.rotation[i][2] * C.rotation[2][j];
  }
  const ct = C.translation;
  const t = [
    P.translation[0] + P.scale * (P.rotation[0][0] * ct[0] + P.rotation[0][1] * ct[1] + P.rotation[0][2] * ct[2]),
    P.translation[1] + P.scale * (P.rotation[1][0] * ct[0] + P.rotation[1][1] * ct[1] + P.rotation[1][2] * ct[2]),
    P.translation[2] + P.scale * (P.rotation[2][0] * ct[0] + P.rotation[2][1] * ct[1] + P.rotation[2][2] * ct[2]),
  ];
  return { translation: t, rotation: R, scale: P.scale * C.scale };
}

const AV41_TYPES = new Set(['NiNode', 'NiTriShape']);

/** Derive the multi-shape render model + decoded controllers from the
 * canonical extraction. Numeric (render-ready) geometry arrays; local/world
 * TRS per shape resolved through the AVObject parent chain. */
function buildRenderModel41(extraction) {
  const blocks = extraction.blocks;
  const byIndex = new Map(blocks.map(b => [b.index, b]));

  // parent map from NiNode children refs (NULL refs -1 are legal — skipped)
  const childOf = new Map();
  for (const b of blocks) {
    if (b.type === 'NiNode' && b.fields && Array.isArray(b.fields.children)) {
      for (const c of b.fields.children) if (c >= 0 && byIndex.has(c)) childOf.set(c, b.index);
    }
  }

  // local TRS (numeric) per AV block
  const localTRS = new Map();
  for (const b of blocks) {
    if (AV41_TYPES.has(b.type) && b.fields) {
      localTRS.set(b.index, {
        translation: b.fields.translation.map(bitsToF32),
        rotation: b.fields.rotation.map(r => r.map(bitsToF32)),
        scale: bitsToF32(b.fields.scale),
      });
    }
  }
  // world TRS (compose up the chain)
  const worldTRS = new Map();
  function worldOf(idx) {
    if (worldTRS.has(idx)) return worldTRS.get(idx);
    const local = localTRS.get(idx);
    const parent = childOf.get(idx);
    const world = parent === undefined ? local : composeTRS(worldOf(parent), local);
    worldTRS.set(idx, world);
    return world;
  }
  for (const idx of localTRS.keys()) worldOf(idx);

  // shapes: NiTriShape -> its NiTriShapeData + resolved property blocks
  const shapes = [];
  for (const b of blocks) {
    if (b.type !== 'NiTriShape' || !b.fields) continue;
    const data = b.fields.dataRef >= 0 ? byIndex.get(b.fields.dataRef) : null;
    if (!data || data.type !== 'NiTriShapeData' || !data.fields) {
      throw new Error(`[NifModelReader41] NiTriShape #${b.index}: dataRef ${b.fields.dataRef} does not resolve to a NiTriShapeData block — LOUD FAIL`);
    }
    const f = data.fields;
    const n = f.numVertices;
    const positions = new Float32Array(n * 3);
    for (let i = 0; i < n * 3; i++) positions[i] = bitsToF32(f.verticesBits[i]);
    const normals = f.hasNormals ? (() => { const a = new Float32Array(n * 3); for (let i = 0; i < n * 3; i++) a[i] = bitsToF32(f.normalsBits[i]); return a; })() : null;
    const colors = f.hasVertexColors ? (() => { const a = new Float32Array(n * 4); for (let i = 0; i < n * 4; i++) a[i] = bitsToF32(f.vertexColorsBits[i]); return a; })() : null;
    const uvSets = f.uvSetsBits.map(bits => { const a = new Float32Array(bits.length); for (let i = 0; i < bits.length; i++) a[i] = bitsToF32(bits[i]); return a; });
    const index = new Uint16Array(f.triangles.length * 3);
    f.triangles.forEach((t, i) => { index[i * 3] = t[0]; index[i * 3 + 1] = t[1]; index[i * 3 + 2] = t[2]; });
    // resolve property blocks (NiMaterialProperty / NiAlphaProperty / NiTexturingProperty)
    const props = (b.fields.properties || []).filter(p => p >= 0).map(p => byIndex.get(p)).filter(Boolean);
    const mat = props.find(p => p.type === 'NiMaterialProperty');
    const alpha = props.find(p => p.type === 'NiAlphaProperty');
    const texprop = props.find(p => p.type === 'NiTexturingProperty');
    shapes.push({
      shapeName: b.fields.name,
      shapeIndex: b.index,
      dataIndex: data.index,
      dataRef: b.fields.dataRef,
      skinRef: b.fields.skinRef,
      numVertices: n,
      numTriangles: f.numTriangles,
      positions, normals, colors, uvSets, index,
      center: f.center.map(bitsToF32),
      radius: bitsToF32(f.radius),
      localTRS: localTRS.get(b.index),
      worldTRS: worldTRS.get(b.index),
      material: mat ? {
        blockIndex: mat.index,
        name: mat.fields.name,
        materialFlags: mat.fields.materialFlags,
        ambient: mat.fields.ambient.map(bitsToF32),
        diffuse: mat.fields.diffuse.map(bitsToF32),
        specular: mat.fields.specular.map(bitsToF32),
        emissive: mat.fields.emissive.map(bitsToF32),
        glossiness: bitsToF32(mat.fields.glossiness),
        alpha: bitsToF32(mat.fields.alpha),
      } : null,
      alphaProp: alpha ? { blockIndex: alpha.index, flags: alpha.fields.alphaFlags, threshold: alpha.fields.alphaThreshold } : null,
      textureProp: texprop ? { blockIndex: texprop.index, texFlags: texprop.fields.texFlags, applyMode: texprop.fields.applyMode, textures: texprop.fields.textures } : null,
      controllerRef: b.fields.controller,
    });
  }

  // decoded controller blocks (the implemented 4.1 controller types)
  const controllers = [];
  for (const b of blocks) {
    if (b.type === 'NiUVController' && b.fields) {
      const target = b.fields.target >= 0 ? byIndex.get(b.fields.target) : null;
      controllers.push({
        blockIndex: b.index, type: 'NiUVController',
        targetType: target ? target.type : null,
        targetName: target && target.fields ? target.fields.name : null,
        targetIndex: b.fields.target,
        nextController: b.fields.nextController,
        flags: b.fields.flags,
        frequency: bitsToF32(b.fields.frequency),
        phase: bitsToF32(b.fields.phase),
        startTime: bitsToF32(b.fields.startTime),
        stopTime: bitsToF32(b.fields.stopTime),
        dataRef: b.fields.dataRef,
      });
    }
    if (b.type === 'NiUVData' && b.fields) {
      controllers.push({
        blockIndex: b.index, type: 'NiUVData',
        uvGroups: b.fields.uvGroups.map(g => ({
          numKeys: g.numKeys, interpolation: g.interpolation,
          keys: g.keys.map(k => ({ time: bitsToF32(k.time), value: bitsToF32(k.value) })),
        })),
      });
    }
  }

  const roots = [...localTRS.keys()].filter(idx => !childOf.has(idx));
  return {
    adapter: 'NifModelReader41',
    shapes,
    controllers,
    roots,
    counts: {
      blocks: blocks.length,
      shapes: shapes.length,
      controllers: controllers.filter(c => c.type === 'NiUVController').length,
      opaque: extraction.opaqueBlocks.length,
    },
  };
}

export { NIF_V4_1_0_12, KNOWN_V41_TYPES };
