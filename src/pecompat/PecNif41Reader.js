// PecNif41Reader.js — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 3)
// THE NIF 4.1.0.12 CORPUS READER for the PCG_9_3_5 Models.bnt container (757
// entries per the re-measured census). Extends the nif41_deep lineage
// (PE_CITY_ASSET_MAP phase 3, SDK-derived field gates for the four CD_2003
// primary models) to the FULL type set of the PCG v4 corpus (33 types per the
// census), with the project Rosetta v4 layouts (docs/nif) as the field
// authority and the closure contract enforced per file.
//
// LAYOUT AUTHORITY (labeled):
//   - docs/nif/01-file-format.md version gates (v4: inline RTTI type strings;
//     NO preamble; 1-byte NiBool; NiObjectNET = name + single extraDataRef +
//     controllerRef; NiAVObject has velocity + HasABV, NOT collision ref).
//   - docs/nif/02..08 per-type v4 layouts (ArkTexture v4 = base(link) + 2×i32
//     + u8 + i32 + numTextures(entry count) + entries; ArkImporter v4 = base +
//     u1(0) + u2(8) + name SS + 3 flag bytes + 38 B tail; ArkAnimation v4 =
//     base + u1..u4 + variant ext; ArkViewportInfo v4 = name SS + link + ext).
//   - The nif41_deep.mjs SDK-derived bases (NiCollisionData ABV NOT
//     implemented — loud; measured on the CD four models).
//   - The local GB 1.2 SDK sources for the modifier/emitter orders (same as
//     the 10.1 reader; citations in PecNif10CorpusReader.js).
//
// CLOSURE: all numBlocks blocks (inline RTTI) + TopObjects footer + EOF EXACT,
// with the recorded-tail fallback (the 10.1 corpus measured real tailed files).
// Boundary search (ArkAnimation variants + ViewportInfo): documented ext sizes
// seeded first + v4 RTTI-shaped candidates (a SizedString KNOWN TYPE NAME — the
// 01-file-format v4 rule) + the same memoized backtracking as the 10.1 reader.

export const PEC_NIF41_CORPUS_READER_VERSION = 'pec-nif41-corpus-reader-v1';

const NIF_V4_1_0_12 = 0x0401000C;
const NIF_V4_0_0_2 = 0x04000002;

export const DECODE_STATUS = {
  SUPPORTED: 'SUPPORTED',
  PARTIALLY_UNDERSTOOD: 'PARTIALLY_UNDERSTOOD',
  OPAQUE: 'OPAQUE',
};

class LoudError extends Error {
  constructor(msg) { super(`[PecNif41] ${msg}`); this.name = 'PecNif41LoudError'; }
}

class Nif41Stream {
  constructor(bytes, sourceName = 'input.nif', bool4 = false) {
    this.bytes = bytes;
    this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.pos = 0;
    this.source = sourceName;
    this.bool4 = bool4; // v4.0.0.2: 4-byte i32 booleans (01-file-format gate)
    this.version = 0; // set by readNif41Corpus after the header parse
  }
  get size() { return this.bytes.length; }
  get remaining() { return this.size - this.pos; }
  _check(n) {
    if (this.pos + n > this.size) {
      throw new Error(`[PecNif41] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[PecNif41] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  boolean() { return this.bool4 ? this.u32() !== 0 : this.u8() !== 0; }
  // version gate carrier (set by readNif41Corpus after the header parse)
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[PecNif41] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3() { return [this.f32(), this.f32(), this.f32()]; }
  mat33() { return [this.vec3(), this.vec3(), this.vec3()]; }
  color4() { return [this.f32(), this.f32(), this.f32(), this.f32()]; }
  ref() { return this.i32(); }
  refList(maxCount = 65536) {
    const count = this.u32();
    if (count > maxCount) throw new Error(`[PecNif41] implausible ref-list count ${count} @${this.pos - 4}`);
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
  static isTbc(t) { return t === 3; }
}

// ---- v4 bases (01-file-format gates) ----

function readObjectNet(s) {
  const name = s.sizedString();
  const extraDataRef = s.ref(); // < 5.0.0.11: SINGLE extra-data link
  const controllerRef = s.ref();
  return { name, extraDataRef, controllerRef };
}

function readAVObject(s) {
  const flags = s.u16();
  const translation = s.vec3();
  const rotation = s.mat33();
  const scale = s.f32();
  const velocity = s.vec3(); // < 5.0.0.19: serialized (raw; semantics not needed)
  const numProperties = s.u32();
  if (numProperties > 65536) throw new Error(`[PecNif41] implausible numProperties ${numProperties} @${s.pos - 4}`);
  const propertyRefs = [];
  for (let i = 0; i < numProperties; i++) propertyRefs.push(s.ref());
  const hasABV = s.boolean(); // 4.1.0.12: 1-byte NiBool; 4.0.0.2: 4-byte bool
  if (hasABV) {
    throw new LoudError('AVObject HasABV=true — bounding volume stream NOT implemented in this reader (LOUD FAIL; 0 expected in the PCG v4 corpus per the lineage)');
  }
  return { flags, translation, rotation, scale, velocity, numProperties, propertyRefs, hasABV };
}

function readPropertyBase(s) {
  const net = readObjectNet(s);
  const propertyFlags = s.u16(); // NiProperty < 10.0.1.2
  return { ...net, propertyFlags };
}

function readExtraDataBase(s) { // v4: next link only — NO name
  const nextExtraDataRef = s.ref();
  return { nextExtraDataRef };
}

function readTimeController(s) { // same 30-byte shape as v10 (05)
  const nextControllerRef = s.ref();
  const flags = s.u16();
  const frequency = s.f32();
  const phase = s.f32();
  const startTime = s.f32();
  const stopTime = s.f32();
  const targetRef = s.ref();
  return { nextControllerRef, flags, frequency, phase, startTime, stopTime, targetRef };
}

function readKeyGroup(s, valueReader, valueName) {
  const numKeys = s.u32();
  if (numKeys > 1_000_000) throw new Error(`[PecNif41] implausible numKeys ${numKeys}`);
  if (numKeys === 0) return { numKeys: 0, interpolation: null, times: [], values: [] };
  const interpolation = s.u32();
  const tbc = Nif41Stream.isTbc(interpolation);
  const quad = interpolation === 2;
  const times = new Float32Array(numKeys);
  const values = [];
  for (let i = 0; i < numKeys; i++) {
    times[i] = s.f32();
    const value = valueReader(s);
    if (quad) { valueReader(s); valueReader(s); } // forward + backward (value-typed)
    else if (tbc) { s.f32(); s.f32(); s.f32(); }
    values.push(value);
  }
  return { numKeys, interpolation, times, values, valueKind: valueName };
}

// ---- per-type parsers ----

function parseNiNode(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const children = s.refList();
  const effects = s.refList();
  return { ...net, ...av, children, effects };
}

function parseNiTriShape(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dataRef = s.ref();
  const skinRef = s.ref(); // < 5.0.0.21: NO shader byte
  return { ...net, ...av, dataRef, skinRef };
}

function parseNiTriShapeData(s) {
  // Rosetta 03 (v4 read order): numUvSets LATE; triangles UNCONDITIONAL.
  // 4.0.0.2 gates: booleans are 4-byte (bool4) and hasUv sits between
  // numTextureSets and the uvSets (01-file-format / 03-geometry).
  const numVertices = s.u16();
  const hasVertices = s.boolean();
  let positions = null;
  let vertexRange = null;
  if (hasVertices) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    positions = arr;
    vertexRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const hasNormals = s.boolean();
  let normals = null;
  let normalRange = null;
  if (hasNormals) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    normals = arr;
    normalRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const center = s.vec3();
  const radius = s.f32();
  const hasColors = s.boolean();
  let colors = null;
  let colorRange = null;
  if (hasColors) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 4);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    colors = arr;
    colorRange = { start, end: s.pos, byteLength: s.pos - start };
  }
  const numTextureSetsRaw = s.i16(); // < 5.0.0.10: short
  const uvSetCount = numTextureSetsRaw & 0x3f;
  let hasUv = null;
  if (s.version === NIF_V4_0_0_2) hasUv = s.boolean(); // ONLY 4.0.0.2 (4-byte bool)
  const uvSets = [];
  const uvRanges = [];
  for (let set = 0; set < uvSetCount; set++) {
    const start = s.pos;
    const arr = new Float32Array(numVertices * 2);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    uvSets.push(arr);
    uvRanges.push({ start, end: s.pos, byteLength: s.pos - start });
  }
  const numTriangles = s.u16();
  const triListLength = s.u32();
  if (triListLength > 1_000_000) throw new Error(`[PecNif41] impossible triListLength ${triListLength}`);
  let indices = null;
  let indexRange = null;
  if (triListLength > 0) {
    if (triListLength !== numTriangles * 3) {
      throw new Error(`[PecNif41] triListLength ${triListLength} != numTriangles*3 ${numTriangles * 3}`);
    }
    const start = s.pos;
    const arr = new Uint16Array(triListLength);
    for (let i = 0; i < arr.length; i++) arr[i] = s.u16();
    indices = arr;
    indexRange = { start, end: s.pos, byteLength: s.pos - start };
  } else if (numTriangles !== 0) {
    throw new Error(`[PecNif41] triListLength 0 but numTriangles ${numTriangles}`);
  }
  const numMatchGroups = s.u16();
  const matchGroups = [];
  for (let g = 0; g < numMatchGroups; g++) {
    const count = s.u16();
    const groupIndices = [];
    for (let i = 0; i < count; i++) groupIndices.push(s.u16());
    matchGroups.push({ count, indices: groupIndices });
  }
  return {
    numVertices, hasVertices, hasNormals, hasColors, hasUv, center, radius,
    numTextureSetsRaw, uvSetCount, numTriangles, triListLength, numMatchGroups, matchGroups,
    geometry: {
      positions, normals, colors, uvSets, indices,
      vertexRange, normalRange, colorRange, uvRanges, indexRange,
      numVertices, numTriangles,
    },
  };
}

function parseNiTexturingProperty(s) {
  // Rosetta 04 (v4): property base + Apply u32 + TextureCount u32 + slots with
  // the 22-byte TexDesc; BUMP slot extras after the loop when its map exists.
  const base = readPropertyBase(s);
  const applyMode = s.u32();
  const textureCount = s.u32();
  if (textureCount > 16) throw new Error(`[PecNif41] texprop "${base.name}" textureCount ${textureCount} beyond bounded slot table`);
  const slotNames = ['Base', 'Dark', 'Detail', 'Gloss', 'Glow', 'Bump', 'Decal0'];
  if (textureCount >= 8) slotNames.push('Decal1');
  if (textureCount >= 9) slotNames.push('Decal2');
  if (textureCount >= 10) slotNames.push('Decal3');
  const slots = [];
  for (let i = 0; i < textureCount && i < slotNames.length; i++) {
    const hasMap = s.u8() !== 0;
    if (!hasMap) { slots.push({ slotIndex: i, slotName: slotNames[i], hasMap }); continue; }
    const sourceRef = s.ref();
    const clampMode = s.u32();
    const filterMode = s.u32();
    const uvSet = s.u32();
    const ps2L = s.i16();
    const ps2K = s.i16();
    const unknownU16 = s.u16(); // abManual NiBool[2] (< 4.1.0.16) — 22-byte TexDesc
    slots.push({ slotIndex: i, slotName: slotNames[i], hasMap, sourceRef, clampMode, filterMode, uvSet, ps2L, ps2K, unknownU16 });
  }
  const bumpSlot = slots.find((x) => x.slotName === 'Bump' && x.hasMap);
  if (bumpSlot) {
    bumpSlot.bumpLumaScale = s.f32();
    bumpSlot.bumpLumaOffset = s.f32();
    bumpSlot.bumpMat = [s.f32(), s.f32(), s.f32(), s.f32()];
  }
  return { ...base, applyMode, textureCount, slots };
}

function parseNiMaterialProperty(s) {
  const base = readPropertyBase(s);
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  const emissive = s.vec3();
  const glossiness = s.f32();
  const materialAlpha = s.f32();
  return { ...base, ambient, diffuse, specular, emissive, glossiness, materialAlpha };
}

function parseNiAlphaProperty(s) {
  // readPropertyBase consumed the u16 flags; only the u8 threshold remains.
  const base = readPropertyBase(s);
  const alphaThreshold = s.u8();
  return { ...base, alphaThreshold };
}

function parseNiZBufferProperty(s) {
  // readPropertyBase already consumed the u16 property flags (the NiProperty
  // base layer); the u32 z-function exists only >= 4.1.0.5 — 4.0.0.2 has NONE.
  const base = readPropertyBase(s);
  const zFunction = s.version >= NIF_V4_1_0_12 ? s.u32() : null;
  return { ...base, zFunction };
}

function parseNiVertexColorProperty(s) {
  // Rosetta 02 split (u16 vertexMode + u16 lightingMode + PE u32 = 8 bytes;
  // the u16 flags live in the property base). Closure decides per file.
  const base = readPropertyBase(s);
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32();
  return { ...base, vertexMode, lightingMode, unknownPeField };
}

function parseOneFlagProperty(s) {
  // readPropertyBase consumed the u16 flags — nothing further.
  return readPropertyBase(s);
}

function parseNiStringExtraData(s) {
  const base = readExtraDataBase(s);
  const stringData = s.sizedString();
  return { ...base, stringData };
}

function parseNiTextKeyExtraData(s) {
  // Rosetta 05 (v4): base(link) + unknownInt1 u32 + numTextKeys + time+text keys.
  const base = readExtraDataBase(s);
  const unknownInt1 = s.u32();
  const numTextKeys = s.u32();
  if (numTextKeys > 65536) throw new Error(`[PecNif41] implausible numTextKeys ${numTextKeys}`);
  const keys = [];
  for (let i = 0; i < numTextKeys; i++) {
    const time = s.f32();
    const text = s.sizedString();
    keys.push({ time, text });
  }
  return { ...base, unknownInt1, numTextKeys, keys };
}

// ---- animation (05) ----

function parseNiKeyframeData(s) {
  const numRotationKeys = s.u32();
  if (numRotationKeys > 1_000_000) throw new Error(`[PecNif41] implausible numRotationKeys ${numRotationKeys}`);
  let rotationType = null;
  let rotationKeys = null;
  let eulerAxes = null;
  let eulerUnknownFloat = null;
  if (numRotationKeys !== 0) {
    rotationType = s.u32();
    if (rotationType === 4) {
      eulerUnknownFloat = s.f32(); // v ≤ 0x0A010000: PE-specific extra
      eulerAxes = [0, 1, 2].map(() => readKeyGroup(s, (st) => st.f32(), 'f32'));
    } else {
      const tbc = Nif41Stream.isTbc(rotationType);
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

function parseNiFloatData(s) { return { floatKeys: readKeyGroup(s, (st) => st.f32(), 'f32') }; }
function parseNiPosData(s) { return { posKeys: readKeyGroup(s, (st) => st.vec3(), 'vec3') }; }

function parseNiUVData(s) {
  return { uvGroups: [0, 1, 2, 3].map(() => readKeyGroup(s, (st) => st.f32(), 'f32')) };
}

function parseNiVisData(s) {
  const numKeys = s.u32();
  if (numKeys > 65536) throw new Error(`[PecNif41] implausible vis numKeys ${numKeys}`);
  const keys = [];
  for (let i = 0; i < numKeys; i++) {
    const time = s.f32();
    const value = s.u8();
    keys.push({ time, value: value !== 0 });
  }
  return { numKeys, keys };
}

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

function parseNiFlipController(s) {
  const tc = readTimeController(s);
  const textureSlot = s.u32();
  const unknownInt2 = s.u32();
  const delta = s.f32();
  const numSources = s.u32();
  if (numSources > 4096) throw new Error(`[PecNif41] implausible numSources ${numSources}`);
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
  const dataRef = s.ref(); // v4: NO targetColor u16 (05 registry)
  return { ...tc, dataRef };
}

// ---- skinning (07) ----

function parseNiSkinInstance(s) {
  const dataRef = s.ref();
  const skeletonRootRef = s.ref();
  const numBones = s.u32();
  if (numBones > 4096) throw new Error(`[PecNif41] implausible numBones ${numBones}`);
  const boneRefs = [];
  for (let i = 0; i < numBones; i++) boneRefs.push(s.ref());
  return { dataRef, skeletonRootRef, numBones, boneRefs };
}

function parseNiSkinData(s) {
  // 07: v4 — skinPartition link read (0x04000002 ≤ v ≤ 0x0A010000);
  // hasVertexWeights NOT read (v < 0x04020100); per-bone weights ALWAYS read.
  const overallRotation = s.mat33();
  const overallTranslation = s.vec3();
  const overallScale = s.f32();
  const numBones = s.u32();
  if (numBones > 4096) throw new Error(`[PecNif41] implausible skin numBones ${numBones}`);
  const skinPartitionLink = s.u32();
  const bones = [];
  for (let i = 0; i < numBones; i++) {
    const boneRotation = s.mat33();
    const boneTranslation = s.vec3();
    const boneScale = s.f32();
    const boundingSphereOffset = s.vec3();
    const boundingSphereRadius = s.f32();
    const numVertices = s.u16();
    const vertexWeights = [];
    for (let j = 0; j < numVertices; j++) {
      const vertexIndex = s.u16();
      const weight = s.f32();
      vertexWeights.push({ vertexIndex, weight });
    }
    bones.push({ boneRotation, boneTranslation, boneScale, boundingSphereOffset, boundingSphereRadius, numVertices, vertexWeights });
  }
  return { overallRotation, overallTranslation, overallScale, numBones, skinPartitionLink, bones };
}

// ---- lights (06) ----
// 4.0.0.2 (<= 0x04000002): dynamic-effect base = numAffectedNodeListPointers
// u32 + RAW ptr u32[] BEFORE the colors, plus a trailing f32 AFTER specular
// (verified byte-exact on 52555.nif: 3 lights, ptr=0x0a91c9d8, trailing 1.0/1.0/0.0).
// 4.1.0.12: NO dynamic-effect layer — Dimmer f32 + ambient + diffuse + specular
// (verified on 353832.nif NiAmbientLight @58065: dimmer=1.0, colors, then the
// [ntop=1][ref=0] footer at EOF; 25-file regression caught the wrong merge).

function readDynamicEffectBase40(s) {
  const numAffectedNodeListPointers = s.u32();
  if (numAffectedNodeListPointers > 1024) throw new Error(`[PecNif41] implausible numAffectedNodeListPointers ${numAffectedNodeListPointers}`);
  const affectedNodeListPointers = [];
  for (let i = 0; i < numAffectedNodeListPointers; i++) affectedNodeListPointers.push(s.u32()); // RAW heap ptrs (post-load meaningless)
  return { numAffectedNodeListPointers, affectedNodeListPointers };
}

function readLightFields(s) {
  if (s.version === NIF_V4_0_0_2) {
    const dynamicEffect = readDynamicEffectBase40(s);
    const ambient = s.vec3();
    const diffuse = s.vec3();
    const specular = s.vec3();
    const trailingF32 = s.f32(); // measured 1.0/1.0/0.0 — semantics UNRESOLVED
    return { ...dynamicEffect, ambient, diffuse, specular, trailingF32, dimmer: null };
  }
  const dimmer = s.f32();
  const ambient = s.vec3();
  const diffuse = s.vec3();
  const specular = s.vec3();
  return { dimmer, ambient, diffuse, specular };
}

function parseNiAmbientLight(s) {
  // v4.1.0.12 dynamic-effect layer: NOTHING (06).
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const light = readLightFields(s);
  return { ...net, ...av, ...light };
}

function parseNiDirectionalLight(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const light = readLightFields(s);
  return { ...net, ...av, ...light };
}

function parseNiTextureEffect(s) {
  // Rosetta 06 (v4): NET + AV + (NO dynamic-effect layer) + effect fields +
  // the v4-only unknownShort.
  const net = readObjectNet(s);
  const av = readAVObject(s);
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
  const unknownShort = s.i16(); // v4 only (≤ 0x0401000C)
  return {
    ...net, ...av, modelProjectionMatrix, modelProjectionTransform,
    textureFiltering, textureClamping, textureType, coordinateGenerationType,
    sourceTextureRef, clippingPlane, unknownVector, unknownFloat, ps2L, ps2K, unknownShort,
  };
}

// ---- NiArk* (08; v4 layouts) ----

function parseNiArkTextureExtraData(s) {
  // Rosetta 08 (v4): base(link) + 2×i32 + u8 + i32 + numTextures i32 (the
  // entry count 0..51) + entries. VERIFIED byte-by-byte on 223534.nif:
  // link=3, i32a=0, i32b=3, u8=1, i32=0, numTex=1, entry "Scene_Root_0_BASE"
  // + f1 + f2(-1) + texpropRef(4) + 9-byte tail [00 FFFFFFFF 08690300].
  const base = readExtraDataBase(s);
  const ui1a = s.i32();
  const ui1b = s.i32();
  const ub = s.u8();
  const unknownI32 = s.i32(); // the documented-but-unnamed 4th i32 (value 0 measured)
  const numTex = s.i32();
  if (numTex < 0 || numTex > 4096) {
    throw new Error(`[PecNif41] ArkTexture numTex ${numTex} implausible (LOUD FAIL)`);
  }
  const entries = [];
  for (let i = 0; i < numTex; i++) {
    const entryName = s.sizedString();
    if (entryName.length < 1 || entryName.length > 256) {
      throw new Error(`[PecNif41] ArkTexture entry ${i}: implausible name length ${entryName.length}`);
    }
    const f1 = s.i32();
    const f2 = s.i32();
    const texturingPropertyRef = s.ref();
    const bytes9Hex = s.rawHex(9); // RAW — tail controls in the texture chain module only
    entries.push({ entryName, f1, f2, texturingPropertyRef, bytes9Hex });
  }
  return {
    ...base, ui1a, ui1b, ub, unknownI32, numTex, entries,
    bytes9TailPolicy: 'RAW in the reader; textureId interpretation only via the tail controls in PecTextureChain',
  };
}

function parseNiArkImporterExtraData(s) {
  // 08 v4: base(link) + u1 (=0) + u2 (=8) + importerName SS + 3 flag bytes + 38 B tail.
  const base = readExtraDataBase(s);
  const u1 = s.i32();
  const u2 = s.i32();
  const importerName = s.sizedString();
  const flagBytesHex = s.rawHex(3);
  const tail38Hex = s.rawHex(38);
  return { ...base, u1, u2, importerName, flagBytesHex, tail38Hex, tailPolicy: 'RAW (38 B; DECODED-as-bbox in the Rosetta but not re-interpreted here)' };
}

const TYPE_PARSERS = {
  NiNode: parseNiNode,
  NiArkBillboardNode: parseNiNode, // proven alias: v4 = plain NiNode (08)
  NiTriShape: parseNiTriShape,
  NiTriShapeData: parseNiTriShapeData,
  NiTexturingProperty: parseNiTexturingProperty,
  NiMaterialProperty: parseNiMaterialProperty,
  NiAlphaProperty: parseNiAlphaProperty,
  NiZBufferProperty: parseNiZBufferProperty,
  NiVertexColorProperty: parseNiVertexColorProperty,
  NiSpecularProperty: parseOneFlagProperty,
  NiDitherProperty: parseOneFlagProperty,
  NiStringExtraData: parseNiStringExtraData,
  NiTextKeyExtraData: parseNiTextKeyExtraData,
  NiKeyframeController: parseNiKeyframeController,
  NiKeyframeData: parseNiKeyframeData,
  NiFloatData: parseNiFloatData,
  NiPosData: parseNiPosData,
  NiUVData: parseNiUVData,
  NiVisData: parseNiVisData,
  NiUVController: parseNiUVController,
  NiFlipController: parseNiFlipController,
  NiVisController: parseNiVisController,
  NiAlphaController: parseNiAlphaController,
  NiMaterialColorController: parseNiMaterialColorController,
  NiSkinInstance: parseNiSkinInstance,
  NiSkinData: parseNiSkinData,
  NiAmbientLight: parseNiAmbientLight,
  NiDirectionalLight: parseNiDirectionalLight,
  NiTextureEffect: parseNiTextureEffect,
  NiArkTextureExtraData: parseNiArkTextureExtraData,
  NiArkImporterExtraData: parseNiArkImporterExtraData,
};

const TYPE_DECODE_STATUS = {
  NiArkViewportInfoExtraData: DECODE_STATUS.OPAQUE,
  NiArkAnimationExtraData: DECODE_STATUS.OPAQUE,
  NiArkTextureExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiArkImporterExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
};
for (const t of Object.keys(TYPE_PARSERS)) TYPE_DECODE_STATUS[t] = TYPE_DECODE_STATUS[t] ?? DECODE_STATUS.SUPPORTED;

// The RTTI candidate vocabulary: v4 blocks start with an inline SizedString
// type name — the boundary-search prime (01-file-format "v4 next-block
// candidate: a SizedString matching a known NIF type name, length 5-50").
const RTTI_TYPES = new Set(Object.keys(TYPE_PARSERS).concat(['NiArkViewportInfoExtraData', 'NiArkAnimationExtraData']));

const BOUNDARY_SEARCH_TYPES = new Set(['NiArkViewportInfoExtraData', 'NiArkAnimationExtraData']);
const MAX_ATTEMPTS = 200000;

// variable-ext prefixes (v4)
function parseBoundaryPrefix(s, type) {
  if (type === 'NiArkViewportInfoExtraData') {
    const name = s.sizedString();
    const link = s.ref(); // 08 v4: name SS + link + variable extension
    return { name, link };
  }
  if (type === 'NiArkAnimationExtraData') {
    const base = readExtraDataBase(s);
    const u1 = s.i32();
    const u2 = s.i32();
    const u3 = s.i32();
    const u4 = s.i32();
    return { ...base, u1, u2, u3, u4 };
  }
  throw new LoudError(`parseBoundaryPrefix: unhandled type ${type}`);
}

// documented v4 ext seeds (08 selector table)
function documentedExtSeeds(type, prefix, remaining) {
  if (type === 'NiArkAnimationExtraData') {
    const { u2, u3, u4 } = prefix;
    const seeds = [];
    if ((u3 >>> 0) === 0xffffffff && (u2 >>> 0) < 4) seeds.push(37); // FIXED_A
    if ((u2 >>> 0) === 3 && (u3 >>> 0) === 5) {
      const n = (u4 >>> 0) >> 8;
      if (n > 0 && 5 * n + 37 <= remaining) seeds.push(5 * n + 37); // BINARY
    }
    const u3b1 = ((u3 >>> 0) >> 8) & 0xff;
    if (u3b1 > 0 && u3b1 * 5 <= remaining) seeds.push(u3b1 * 5); // G3D
    return seeds;
  }
  return [];
}

function boundaryCandidates41(bytes, dv, start, fileSize, seedSizes = []) {
  // v4 candidates: the NEXT block starts with an inline RTTI SizedString that
  // matches a KNOWN type name (the 01-file-format v4 rule) — a very strong
  // shape; plus the EOF footer shape. Seeds first.
  const cands = [];
  const seen = new Set();
  const push = (rank, pos, method) => {
    if (pos < start || pos > fileSize || seen.has(pos)) return;
    seen.add(pos);
    cands.push({ rank, pos, method });
  };
  for (const sz of seedSizes) push(0, start + sz, `documented_size_${sz}B`);
  for (let p = start; p <= fileSize - 8; p++) {
    if (dv.getUint32(p, true) !== 0) continue; // v4 blocks are u32-preamble-free; the RTTI len follows a u32==0? NO —
    void p;
  }
  // v4 RTTI scan: position p where [i32 len 5..50][type-name bytes matching RTTI_TYPES]
  for (let p = start; p <= fileSize - 8; p++) {
    const len = dv.getInt32(p, true);
    if (len < 5 || len > 50) continue;
    if (p + 4 + len > fileSize) continue;
    let s = '';
    let printable = true;
    for (let i = 0; i < len; i++) {
      const b = bytes[p + 4 + i];
      if (b < 32 || b > 126) { printable = false; break; }
      s += String.fromCharCode(b);
    }
    if (printable && RTTI_TYPES.has(s)) {
      push(0, p, 'v4_rtti_next_block');
    }
  }
  for (let p = start; p <= fileSize - 4; p++) {
    const c = dv.getUint32(p, true);
    if (c <= 100000 && p + 4 + 4 * c === fileSize) {
      push(0, p, 'top_objects_footer');
    }
  }
  return cands;
}

function makeBlockRecord(index, type, decodeStatus, typeOffset, dataOffset, dataEnd, fields) {
  const rec = {
    index,
    type,
    decodeStatus,
    preambleOffset: typeOffset,
    payloadStart: dataOffset,
    blockEnd: dataEnd,
    name: fields?.name ?? null,
  };
  if (fields && 'translation' in fields) {
    rec.localTrs = { translate: fields.translation, rotate: fields.rotation, scale: fields.scale };
  }
  if (fields && 'children' in fields) {
    rec.children = fields.children;
    rec.effects = fields.effects;
  }
  if (fields && 'extraDataRef' in fields) {
    rec.extraDataRefs = fields.extraDataRef != null && fields.extraDataRef >= 0 ? [fields.extraDataRef] : [];
    rec.controllerRef = fields.controllerRef;
  }
  if (fields && 'propertyRefs' in fields) rec.propertyRefs = fields.propertyRefs;
  if (fields && 'dataRef' in fields) {
    rec.dataRef = fields.dataRef;
    rec.skinRef = fields.skinRef;
  }
  if (fields && 'geometry' in fields && fields.geometry) rec.geometry = fields.geometry;
  rec.fields = fields;
  return rec;
}

function decodeFrom41(s, ctx, blockIndex, out) {
  const { header, state } = ctx;
  if (blockIndex === header.numBlocks) {
    try {
      const ntop = s.u32();
      if (ntop > header.numBlocks) return null;
      const tops = [];
      for (let i = 0; i < ntop; i++) {
        const t = s.i32();
        if (t < 0 || t >= header.numBlocks) return null;
        tops.push(t);
      }
      if (s.pos === s.size) {
        return { topObjects: tops, numTopObjects: ntop, eofExact: true, tailStart: null, tailBytes: 0 };
      }
      return {
        topObjects: tops, numTopObjects: ntop, eofExact: false,
        tailStart: s.pos, tailBytes: s.size - s.pos,
      };
    } catch { return null; }
  }
  const memoKey = blockIndex * 4294967296 + s.pos;
  if (state.failedMemo?.has(memoKey)) return null;
  const result = decodeFromInner41(s, ctx, blockIndex, out);
  if (result === null) (state.failedMemo ??= new Set()).add(memoKey);
  return result;
}

function decodeFromInner41(s, ctx, blockIndex, out) {
  const { header, payload, dv, state } = ctx;
  if (++state.attempts > MAX_ATTEMPTS) {
    throw new LoudError(`backtracking attempts exceeded ${MAX_ATTEMPTS} — aborting`);
  }
  const typeOffset = s.pos;
  // The inline RTTI read is DATA-DERIVED: a misaligned candidate produces a
  // garbage length — BACKTRACKABLE, never a loud kill.
  let typeName;
  try { typeName = s.sizedString(); } catch { return null; }
  const decodeStatus = TYPE_DECODE_STATUS[typeName] ?? DECODE_STATUS.SUPPORTED;
  if (BOUNDARY_SEARCH_TYPES.has(typeName)) {
    let prefix;
    try { prefix = parseBoundaryPrefix(s, typeName); } catch { return null; }
    const extStart = s.pos;
    const seeds = documentedExtSeeds(typeName, prefix, s.size - extStart);
    const cands = boundaryCandidates41(payload, dv, extStart, s.size, seeds);
    for (const cand of cands) {
      if (cand.pos < extStart || cand.pos > s.size - 4) continue;
      s.seek(cand.pos);
      state.decisions.push({
        block: blockIndex, type: typeName, extStart, extEnd: cand.pos,
        extLength: cand.pos - extStart, method: cand.method,
      });
      out[blockIndex] = makeBlockRecord(blockIndex, typeName, decodeStatus, typeOffset, extStart - 0, cand.pos, {
        ...prefix,
        opaque: {
          extStart, extEnd: cand.pos, extLength: cand.pos - extStart,
          boundaryMethod: cand.method,
          note: 'extension bytes recorded RAW — semantics UNDETERMINED beyond the boundary (DETECTION_UNRESOLVED for this channel)',
        },
      });
      const sub = decodeFrom41(s, ctx, blockIndex + 1, out);
      if (sub) return sub;
      state.decisions.pop();
      out[blockIndex] = null;
      s.seek(extStart);
    }
    return null;
  }
  const parser = TYPE_PARSERS[typeName];
  if (!parser) {
    // v4 RTTI is DATA-DERIVED: a garbage type name means the current boundary
    // candidate is wrong — BACKTRACKABLE (return null), never a loud kill.
    // The closure failure message still names the deepest unknown type.
    state.unknownTypesSeen ??= new Set();
    state.unknownTypesSeen.add(`${blockIndex}:${typeName.slice(0, 40)}`);
    if (ctx.debugTrace) ctx.debugTrace.push({ blockIndex, type: typeName, start: typeOffset, err: 'unknown-rtti', pos: s.pos });
    s.seek(typeOffset);
    return null;
  }
  const dataOffset = s.pos;
  let fields;
  try {
    fields = parser(s);
  } catch (e) {
    if (e instanceof LoudError) throw e;
    if (ctx.debugTrace) ctx.debugTrace.push({ blockIndex, type: typeName, start: typeOffset, err: String(e?.message ?? e).slice(0, 200), pos: s.pos });
    s.seek(typeOffset);
    return null;
  }
  if (ctx.debugTrace) ctx.debugTrace.push({ blockIndex, type: typeName, start: typeOffset, end: s.pos });
  out[blockIndex] = makeBlockRecord(blockIndex, typeName, decodeStatus, typeOffset, dataOffset, s.pos, fields);
  const sub = decodeFrom41(s, ctx, blockIndex + 1, out);
  if (sub) return sub;
  out[blockIndex] = null;
  return null;
}

/**
 * readNif41Corpus — parse a NIF 4.1.0.12 payload to closure or fail loudly.
 * Emits the same reader-result shape as readNif10Corpus (SceneIR-compatible).
 */
export function readNif41Corpus(payload, opts = {}) {
  const sourceName = opts.sourceName ?? 'input.nif';
  const s = new Nif41Stream(payload, sourceName);
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new LoudError('no newline in header — LOUD FAIL');
  const text = String.fromCharCode(...payload.subarray(0, nl));
  s.pos = nl + 1;
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V4_1_0_12 && versionRaw !== NIF_V4_0_0_2) {
    throw new LoudError(`version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — this reader implements NIF 4.1.0.12 and 4.0.0.2 (LOUD FAIL)`);
  }
  const isV40 = versionRaw === NIF_V4_0_0_2;
  s.bool4 = isV40; // 4.0.0.2: 4-byte i32 booleans
  s.version = versionRaw;
  const numBlocks = s.u32();
  if (numBlocks > 100000) throw new LoudError(`implausible numBlocks ${numBlocks}`);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ctx = {
    header: {
      text,
      versionRaw: isV40 ? '0x04000002' : '0x0401000C',
      versionString: isV40 ? '4.0.0.2' : '4.1.0.12',
      numBlocks, numBlockTypes: 0, blockTypes: [], blockTypeIndex: [], numGroups: 0, groups: [],
      dataStartOffset: s.pos,
    },
    payload, dv,
    state: { attempts: 0, decisions: [], failedMemo: new Set(), maxBlock: 0 },
    debugTrace: Array.isArray(opts.debugTrace) ? opts.debugTrace : (opts.debugTrace === true ? [] : null),
  };
  const out = new Array(numBlocks).fill(null);
  const footer = decodeFrom41(s, ctx, 0, out);
  if (!footer) {
    const unknowns = [...(ctx.state.unknownTypesSeen ?? [])].slice(0, 6);
    throw new LoudError(
      `CLOSURE_FAIL: no candidate set closed ${sourceName} under the documented v4 layouts ` +
      `(attempts=${ctx.state.attempts}, maxBlock=${ctx.state.maxBlock}` +
      (unknowns.length ? `, deepestUnknownTypes=${JSON.stringify(unknowns)}` : '') + ') — LOUD FAIL');
  }
  if (out.some((b) => b == null)) throw new LoudError('internal: closure returned but some blocks are unset');
  const blockTypes = [...new Set(out.map((b) => b.type))];
  return {
    readerVersion: PEC_NIF41_CORPUS_READER_VERSION,
    sourceName,
    sourceBytes: payload,
    header: {
      ...ctx.header,
      numBlockTypes: blockTypes.length,
      blockTypes,
      blockTypeIndex: out.map((b) => blockTypes.indexOf(b.type)),
    },
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
        ? `TRAILING_BYTES_RECORDED_RAW: ${footer.tailBytes} bytes follow the TopObjects footer (range [${footer.tailStart},${payload.length})); semantics UNKNOWN`
        : null,
    },
  };
}

/** Geometry fingerprints (same contract as the 10.1 reader). */
export function attachGeometryFingerprints41(readerResult, sha256) {
  const perMesh = [];
  for (const b of readerResult.blocks) {
    if (!b.geometry) continue;
    const g = b.geometry;
    const rec = { dataBlock: b.index, type: b.type, numVertices: g.numVertices, numTriangles: g.numTriangles };
    if (g.vertexRange && g.positions) {
      const rangeBytes = readerResult.sourceBytes.subarray(g.vertexRange.start, g.vertexRange.end);
      const repacked = new Uint8Array(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength);
      rec.vertexPositionsF32leSha256 = sha256(repacked);
      rec.vertexRoundtripExact = sha256(rangeBytes) === rec.vertexPositionsF32leSha256;
    }
    if (g.indexRange && g.indices) {
      const rangeBytes = readerResult.sourceBytes.subarray(g.indexRange.start, g.indexRange.end);
      const repackedIdx = new Uint8Array(g.indices.buffer, g.indices.byteOffset, g.indices.byteLength);
      rec.triangleIndicesU16leSha256 = sha256(repackedIdx);
      rec.indexRoundtripExact = sha256(rangeBytes) === rec.triangleIndicesU16leSha256;
    }
    g.fingerprint = rec;
    perMesh.push(rec);
  }
  return perMesh;
}
