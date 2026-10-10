// nif41_deep.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (W3, contract §3)
// BOUNDED NIF 4.1.0.12 (0x0401000C) READER for the FOUR PRIMARY CD_2003 MODELS
// (192374.nif, 193207.nif, 193313.nif, 193684.nif) ONLY.
//
// *** THIS IS NOT A GENERAL FORMAT CLAIM. Every field layout below is gated to
// version 4.1.0.12 exactly and was derived for these four files; no other
// corpus is claimed readable. ***
//
// FIELD-LAYOUT AUTHORITY (documented lineage, dual-source):
//  A) STANDARD TYPES — derived from the pinned local Gamebryo 1.2 SDK sources
//     (D:\gamebyroengine\extracted\Gb12_Source; READ_ONLY architectural
//     reference; NO SDK source is copied into this file). Per-type citations
//     (file:line of the LoadBinary actually read by this executor):
//       - NiObjectNET.cpp:553-570  (< 5.0.0.11): Name(CString=i32 len+bytes),
//         ExtraData SINGLE ref, Controller ref — NOT a num+list (that is
//         >= 5.0.0.11).
//       - NiAVObject.cpp:546-665   (< 5.0.0.19): u16 flags; Translate vec3;
//         Rotate mat33 (row-major, p' = R*p); Scale f32; Velocity vec3 (<
//         5.0.0.19); Properties u32+refs; HasABV NiBool (>= 4.1.0.0);
//         ABV (if true) via NiCollisionData::Initialize →
//         NiBoundingVolume::CreateFromStream (NiBoundingVolume.cpp: enum i32
//         type + type-specific body). NOT implemented here — LOUD FAIL if
//         encountered (none expected in the four models; measured honestly).
//       - NiNode.cpp: NiAVObject + ReadMultipleLinkIDs children + effects
//         (u32 count + i32 refs each).
//       - NiGeometry.cpp:620-630: NiAVObject + Data ref + SkinInstance ref;
//         NO shader byte (< 5.0.0.21).
//       - NiTriShapeData.cpp: NiGeometryData + numTriangles u16 + triListLen
//         u32 + triList u16[] (< 10.0.1.17: no HasList bool — always present)
//         + sharedNormals u16 count + per-group u16 count + u16 indices.
//       - NiGeometryData.cpp:568-700: numVertices u16; HasVertices NiBool
//         (>= 4.1.0.0); vertices vec3[]; HasNormals NiBool + normals vec3[]
//         (NO dataFlags < 10.0.0.2); bound (center vec3 + radius f32);
//         HasColors NiBool + colors ColorA(f32x4)[]; numTextureSets i16
//         (< 5.0.0.10); NO m_pkTexture flag byte (>= 4.1.0.0); UV sets =
//         (numTextureSets & 0x3F) × numVertices × vec2 (TEXTURE_SET_MASK 0x003F,
//         NiGeometryData.h; SetNumTextureSets asserts < 64); NO dirtyFlags
//         (< 5.0.0.10).
//       - NiProperty.cpp:60-75 (< 10.0.1.2): u16 flags after NiObjectNET.
//       - NiTexturingProperty.cpp:238-372: NiProperty + Apply enum(u32);
//         uiListSize u32; per-slot HasMap NiBool (>= 4.1.0.0) + Map::LoadBinary
//         (ref + Clamp enum + Filter enum + TexCoord u32 + sL i16 + sK i16 +
//         abManual NiBool[2] < 4.1.0.16); slot BUMP_INDEX(=5) with map →
//         BumpMap extras (lumaScale, lumaOffset, mat00, mat01, mat10, mat11 —
//         6 f32); NO shader maps (< 5.0.0.17). Slot names by SDK index enum:
//         0=BASE 1=DARK 2=DETAIL 3=GLOSS 4=GLOW 5=BUMP 6+=DECALn.
//       - NiMaterialProperty.cpp: NiProperty + ambient/diffuse/specular/
//         emissive Color3(f32x3) + shine f32 + alpha f32.
//       - NiAlphaProperty.cpp: NiProperty flags (u16, already read) +
//         alphaTestRef u8.
//       - NiZBufferProperty.cpp: NiProperty flags + (>= 4.1.0.5) test enum u32.
//       - NiVertexColorProperty.cpp: NiProperty flags + Source enum u32 +
//         Lighting enum u32.
//       - NiSourceTexture.cpp:162-313 (< 10.0.1.4): NiObjectNET (via NiTexture:
//         adds nothing) + bSaveName NiBool + [Filename CString | bSavePixel
//         NiBool + pixelData ref] + PixelLayout enum u32 + MipMapped enum u32 +
//         AlphaFmt enum u32 + bStatic NiBool.
//       - NiExtraData.cpp:109-130 (< 5.0.0.11): NextExtraData ref + uiSize u32
//         (+ uiSize RAW bytes ONLY for exact-kind NiExtraData → BinaryExtra;
//         derived classes do NOT read raw bytes here).
//       - NiStringExtraData.cpp: base + CString.
//       - NiIntegerExtraData.cpp: base + i32. (NiFloatExtraData: base + f32;
//         NiBooleanExtraData: base + NiBool — same base pattern.)
//  B) NiArk* TYPES (MindArk custom — NOT in the SDK): class fields from the
//     DOCUMENTED HISTORICAL LINEAGE — nif_parser_v2.py (10_Scripts/python/
//     asset_tools, PCG_9_3_5 NIF 4.1.0.12 corpus) — placed on the SDK
//     NiExtraData base (nextRef+uiSize). Byte totals MEASURED on the four
//     CD_2003 payloads and verified per-file by full-file closure +
//     dual-decode (see the Ark READER_VALIDATION NOTE); per-entry 9-byte
//     ArkTexture tail is recorded RAW ONLY (NO textureId interpretation —
//     the PCG935-era interpretation is explicitly NOT transferred to CD_2003
//     in this run).
//
// STREAM CONVENTIONS (same as PecNif10Reader/ArkArchive reuse): little-endian;
// SizedString/CString = i32 length + bytes; NiBool = 1 byte; enum = 4 bytes.
//
// CLOSURE CONTRACT: a parse is accepted ONLY on full-file closure — all
// numBlocks blocks parsed + TopObjects footer (u32 count + i32 refs) +
// EOF EXACT. Any unknown type or desync is a LOUD failure (never a silent
// partial parse).
//
// REUSE: the composed world transform + scene bounds are computed by the
// UNCHANGED src/pecompat/PecSceneIR.js + PecTransform.js (buildAssetIR /
// validateSceneGraph / composeWorldTransforms / computeSceneBounds) — the
// transform law verified against NATIVE stock-printer controls in the
// predecessor SceneIR run (world = parentWorld * local; p → (R*p)*s + t).
// This reader emits the SAME reader-result shape readNif10 produces, so the
// reuse is by import, not by copy.

import fs from 'node:fs';
import crypto from 'node:crypto';
import {
  buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds,
} from '../../src/pecompat/PecSceneIR.js';
import { applyTrsPoint } from '../../src/pecompat/PecTransform.js';

export const PEC_NIF41_READER_VERSION = 'pec-nif41-deep-reader-v1-phase3';
const NIF_V4_1_0_12 = 0x0401000C;

export const DECODE_STATUS = {
  SUPPORTED: 'SUPPORTED',                       // full SDK-derived field coverage
  PARTIALLY_UNDERSTOOD: 'PARTIALLY_UNDERSTOOD', // documented fields; some raw
  OPAQUE: 'OPAQUE',                             // boundary + raw bytes only
  SUPPORTED_HISTORICAL_LINEAGE: 'SUPPORTED_HISTORICAL_LINEAGE', // Ark: historical parser lineage, closure-verified here
};

// per-type decode status (4.1.0.12 scope only)
const TYPE_STATUS = {
  NiNode: DECODE_STATUS.SUPPORTED,
  NiTriShape: DECODE_STATUS.SUPPORTED,
  NiTriShapeData: DECODE_STATUS.SUPPORTED,
  NiTexturingProperty: DECODE_STATUS.SUPPORTED,
  NiMaterialProperty: DECODE_STATUS.SUPPORTED,
  NiAlphaProperty: DECODE_STATUS.SUPPORTED,
  NiZBufferProperty: DECODE_STATUS.SUPPORTED,
  NiVertexColorProperty: DECODE_STATUS.SUPPORTED,
  NiSourceTexture: DECODE_STATUS.SUPPORTED,
  NiStringExtraData: DECODE_STATUS.SUPPORTED,
  NiIntegerExtraData: DECODE_STATUS.SUPPORTED,
  NiFloatExtraData: DECODE_STATUS.SUPPORTED,
  NiBooleanExtraData: DECODE_STATUS.SUPPORTED,
  NiArkTextureExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
  NiArkAnimationExtraData: DECODE_STATUS.OPAQUE,
  NiArkImporterExtraData: DECODE_STATUS.PARTIALLY_UNDERSTOOD,
};

class LoudError extends Error {
  constructor(msg) { super(`[nif41] ${msg}`); this.name = 'Nif41LoudError'; }
}

class Nif41Stream {
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
      throw new LoudError(`read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  boolean() { return this.u8() !== 0; } // NiBool = unsigned char (NiBool.h)
  sizedString() { // CString/SizedString: i32 length + bytes (NiStream.cpp LoadCString)
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new LoudError(`bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3() { return [this.f32(), this.f32(), this.f32()]; }
  mat33() { return [this.vec3(), this.vec3(), this.vec3()]; }
  ref() { return this.i32(); } // NIF 4.1 link id, -1 = null
  refList() { // ReadMultipleLinkIDs: u32 count + i32 refs
    const count = this.u32();
    if (count > 65536) throw new LoudError(`implausible ref-list count ${count} @${this.pos - 4}`);
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
}

// ---- common prefixes (4.1.0.12; SDK citations in the file header) ----

function readObjectNet(s) {
  const name = s.sizedString();
  const extraDataRef = s.ref();
  const controllerRef = s.ref();
  return { name, extraDataRef, controllerRef };
}

function readAVObject(s) {
  const flags = s.u16();
  const translation = s.vec3();
  const rotation = s.mat33();
  const scale = s.f32();
  const velocity = s.vec3(); // < 5.0.0.19: serialized (raw; SDK converts to collision data — semantics not needed here)
  const propertyRefs = s.refList();
  const hasABV = s.u8() !== 0; // >= 4.1.0.0: NiBool
  if (hasABV) {
    // NiBoundingVolume::CreateFromStream: enum i32 type + type-specific body.
    // NOT implemented for these four models (none expected) — LOUD FAIL.
    throw new LoudError(`AVObject "${'current'}" has HasABV=true @${s.pos - 1} — bounding volume stream layout NOT implemented in this bounded reader (LOUD FAIL)`);
  }
  return { flags, translation, rotation, scale, velocity, propertyRefs, hasABV };
}

function readPropertyBase(s) {
  const net = readObjectNet(s);
  const flags = s.u16(); // NiProperty < 10.0.1.2
  return { ...net, propertyFlags: flags };
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
  const skinRef = s.ref();
  return { ...net, ...av, dataRef, skinRef };
}

function parseNiTriShapeData(s) {
  const numVertices = s.u16();
  if (numVertices > 65535) throw new LoudError(`impossible numVertices ${numVertices}`);
  const hasVertices = s.u8() !== 0;
  let positions = null;
  if (hasVertices) {
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    positions = arr;
  }
  const hasNormals = s.u8() !== 0;
  let normals = null;
  if (hasNormals) {
    const arr = new Float32Array(numVertices * 3);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    normals = arr;
  }
  const center = s.vec3();
  const radius = s.f32();
  const hasColors = s.u8() !== 0;
  let colors = null;
  if (hasColors) {
    const arr = new Float32Array(numVertices * 4);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    colors = arr;
  }
  const numTextureSetsRaw = s.i16(); // < 5.0.0.10: short; NO m_pkTexture flag (>= 4.1.0.0)
  const uvSetCount = numTextureSetsRaw & 0x3F; // TEXTURE_SET_MASK 0x003F
  const uvSets = [];
  for (let set = 0; set < uvSetCount; set++) {
    const arr = new Float32Array(numVertices * 2);
    for (let i = 0; i < arr.length; i++) arr[i] = s.f32();
    uvSets.push(arr);
  }
  const numTriangles = s.u16();
  const triListLength = s.u32(); // numTrianglePoints
  if (triListLength > 400000) throw new LoudError(`impossible triListLength ${triListLength}`);
  // < 10.0.1.17: no HasList bool — list present when triListLength > 0
  let indices = null;
  if (triListLength > 0) {
    if (triListLength !== numTriangles * 3) {
      throw new LoudError(`triListLength ${triListLength} != numTriangles*3 ${numTriangles * 3} — LOUD FAIL (4.1 layout check)`);
    }
    const arr = new Uint16Array(triListLength);
    for (let i = 0; i < arr.length; i++) arr[i] = s.u16();
    indices = arr;
  } else if (numTriangles !== 0) {
    throw new LoudError(`triListLength 0 but numTriangles ${numTriangles} — LOUD FAIL`);
  }
  const numMatchGroups = s.u16();
  const matchGroups = [];
  for (let g = 0; g < numMatchGroups; g++) {
    const count = s.u16();
    const groupIndices = [];
    for (let i = 0; i < count; i++) groupIndices.push(s.u16());
    matchGroups.push({ count, indices: groupIndices });
  }
  // index validation (real data check, never assumed)
  let invalidIndices = 0;
  if (indices) {
    for (let i = 0; i < indices.length; i++) if (indices[i] >= numVertices) invalidIndices++;
  }
  return {
    numVertices, hasVertices, hasNormals, center, radius, hasColors,
    numTextureSetsRaw, uvSetCount, numTriangles, triListLength, numMatchGroups,
    matchGroups, invalidIndices,
    geometry: { positions, normals, colors, uvSets, indices, numVertices, numTriangles },
  };
}

function parseNiTexturingProperty(s) {
  const base = readPropertyBase(s);
  const applyMode = s.u32();
  const uiListSize = s.u32();
  if (uiListSize > 16) throw new LoudError(`texprop "${base.name}" uiListSize ${uiListSize} beyond bounded slot table (LOUD FAIL)`);
  const slots = [];
  for (let i = 0; i < uiListSize; i++) {
    const hasMap = s.u8() !== 0; // >= 4.1.0.0
    if (!hasMap) { slots.push({ slotIndex: i, hasMap }); continue; }
    const sourceRef = s.ref();
    const clampMode = s.u32();
    const filterMode = s.u32();
    const texCoord = s.u32();
    const sL = s.i16();
    const sK = s.i16();
    const manualFlagsHex = s.rawHex(2); // abManual NiBool[2] (< 4.1.0.16)
    const slot = { slotIndex: i, hasMap, sourceRef, clampMode, filterMode, texCoord, sL, sK, manualFlagsHex };
    if (i === 5) { // BUMP_INDEX (SDK enum)
      slot.slotName = 'BumpMap';
      slot.bumpLumaScale = s.f32();
      slot.bumpLumaOffset = s.f32();
      slot.bumpMat = [s.f32(), s.f32(), s.f32(), s.f32()];
    }
    slots.push(slot);
  }
  // slot naming by SDK index enum (BASE=0..BUMP=5, 6+=DECALn)
  for (const slot of slots) {
    if (slot.slotName) continue;
    slot.slotName = ['Base', 'Dark', 'Detail', 'Gloss', 'Glow'][slot.slotIndex] ?? `Decal${slot.slotIndex - 6}`;
  }
  return { ...base, applyMode, uiListSize, slots };
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
  const base = readPropertyBase(s);
  const alphaThreshold = s.u8();
  return { ...base, alphaThreshold };
}

function parseNiZBufferProperty(s) {
  const base = readPropertyBase(s);
  const testFunc = s.u32(); // >= 4.1.0.5
  return { ...base, testFunc };
}

function parseNiVertexColorProperty(s) {
  const base = readPropertyBase(s);
  const sourceMode = s.u32();
  const lightingMode = s.u32();
  return { ...base, sourceMode, lightingMode };
}

function parseNiSourceTexture(s) {
  const net = readObjectNet(s);
  const bSaveName = s.u8() !== 0; // < 10.0.1.4
  let filename = null;
  let pixelDataRef = null;
  if (bSaveName) {
    filename = s.sizedString();
  } else {
    const bSavePixelData = s.u8() !== 0;
    if (bSavePixelData) pixelDataRef = s.ref();
  }
  const pixelLayout = s.u32();
  const mipMapped = s.u32();
  const alphaFmt = s.u32();
  const bStatic = s.u8() !== 0;
  return { ...net, bSaveName, filename, pixelDataRef, pixelLayout, mipMapped, alphaFmt, bStatic };
}

function parseExtraDataBase(s) { // NiExtraData < 5.0.0.11
  const nextExtraDataRef = s.ref();
  const uiSize = s.u32();
  return { nextExtraDataRef, uiSize };
}

function parseNiStringExtraData(s) {
  const base = parseExtraDataBase(s);
  const stringData = s.sizedString();
  return { ...base, stringData };
}

function parseNiIntegerExtraData(s) {
  const base = parseExtraDataBase(s);
  const value = s.i32();
  return { ...base, value };
}

function parseNiFloatExtraData(s) {
  const base = parseExtraDataBase(s);
  const value = s.f32();
  return { ...base, value };
}

function parseNiBooleanExtraData(s) {
  const base = parseExtraDataBase(s);
  const value = s.u8() !== 0;
  return { ...base, value };
}

// ---- NiArk* (CD_2003-measured layouts; 9-byte tail RAW ONLY) ----
// READER_VALIDATION NOTE (dual-decode reconciliation, measured on the four
// CD_2003 payloads, 2026-10-10): the SDK NiExtraData base (< 5.0.0.11,
// NiExtraData.cpp:109-130) reads nextRef + uiSize for EVERY extra data block.
// The historical nif_parser_v2.py lineage OMITS the uiSize in its Ark base and
// compensates by absorbing those 4 bytes into its following class fields
// (its NiStringExtraData DOES read the u32 — internally inconsistent with its
// own Ark classes). Both splits consume IDENTICAL byte totals on all four
// files (animation 57 B, importer 65 B for the 8-char name, ArkTexture 21 B +
// entries — both readers close exactly at the same boundaries). This reader
// adopts the SDK-conformant split (uiSize present); the historical parser
// agrees on every standard block, name, ref and geometry count (dual-decode
// cross-check executed on all four files). This is NOT an era difference.
// The per-entry 9-byte ArkTexture tail stays RAW ONLY (no interpretation).

function parseNiArkTextureExtraData(s) {
  const base = parseExtraDataBase(s);
  const ui1a = s.i32();
  const ui1b = s.i32();
  const ub = s.u8();
  const numTex = s.i32();
  if (numTex < 0 || numTex > 4096) {
    throw new LoudError(`NiArkTextureExtraData numTex ${numTex} implausible @${s.pos - 4} (LOUD FAIL — CD2003 layout may not hold for this file)`);
  }
  const entries = [];
  for (let i = 0; i < numTex; i++) {
    const entryName = s.sizedString();
    if (entryName.length < 1 || entryName.length > 256) {
      throw new LoudError(`ArkTexture entry ${i}: implausible name length ${entryName.length}`);
    }
    const slotType = s.i32();   // historical lineage label: 0=BASE 3=GLOSS 4=GLOW (kept as raw int here)
    const unk4 = s.i32();
    const texturingPropertyRef = s.ref();
    const bytes9Hex = s.rawHex(9); // RAW ONLY — NO interpretation in this run (era discipline)
    entries.push({ entryName, slotType, unk4, texturingPropertyRef, bytes9Hex });
  }
  return {
    ...base, ui1a, ui1b, ub, numTex, entries,
    layoutNote: 'SDK-conformant split (nextRef+uiSize base) — see READER_VALIDATION NOTE',
    bytes9TailPolicy: 'RAW_ONLY — the PCG935-era textureId interpretation is explicitly NOT transferred to CD_2003 in this run',
  };
}

function parseNiArkAnimationExtraData(s) {
  const base = parseExtraDataBase(s);
  const ints = [s.i32(), s.i32(), s.i32(), s.i32()];
  const tail33Hex = s.rawHex(33); // CD_2003 measured (PCG935 lineage = 37B — era difference); OPAQUE
  return { ...base, ints, tail33Hex, layoutNote: 'SDK-conformant split; 33B tail measured' };
}

function parseNiArkImporterExtraData(s) {
  const base = parseExtraDataBase(s);
  const int1 = s.i32();
  const name = s.sizedString(); // measured "4.1.0.12" on all four (int1 == string length on all four — recorded as observed equality, semantics not claimed)
  const tail13Hex = s.rawHex(13);
  const floats = [s.f32(), s.f32(), s.f32(), s.f32(), s.f32(), s.f32(), s.f32()];
  return { ...base, int1, name, tail13Hex, floats, layoutNote: 'SDK-conformant split: int1 then name SS (int1 == string length on all four — observed equality only)' };
}

const BLOCK_PARSERS = {
  NiNode: parseNiNode,
  NiTriShape: parseNiTriShape,
  NiTriShapeData: parseNiTriShapeData,
  NiTexturingProperty: parseNiTexturingProperty,
  NiMaterialProperty: parseNiMaterialProperty,
  NiAlphaProperty: parseNiAlphaProperty,
  NiZBufferProperty: parseNiZBufferProperty,
  NiVertexColorProperty: parseNiVertexColorProperty,
  NiSourceTexture: parseNiSourceTexture,
  NiStringExtraData: parseNiStringExtraData,
  NiIntegerExtraData: parseNiIntegerExtraData,
  NiFloatExtraData: parseNiFloatExtraData,
  NiBooleanExtraData: parseNiBooleanExtraData,
  NiArkTextureExtraData: parseNiArkTextureExtraData,
  NiArkAnimationExtraData: parseNiArkAnimationExtraData,
  NiArkImporterExtraData: parseNiArkImporterExtraData,
};

function makeBlockRecord(index, type, typeOffset, dataOffset, dataEnd, fields) {
  const rec = {
    index,
    type,
    decodeStatus: TYPE_STATUS[type] ?? DECODE_STATUS.OPAQUE,
    typeOffset, dataOffset,
    preambleOffset: typeOffset, // 4.x: block starts at its INLINE type string
    payloadStart: dataOffset,
    blockEnd: dataEnd,
    name: fields?.name ?? fields?.stringData ?? null,
    fields: null,
  };
  if ('translation' in fields) {
    rec.localTrs = { translate: fields.translation, rotate: fields.rotation, scale: fields.scale };
  }
  if ('children' in fields) { rec.children = fields.children; rec.effects = fields.effects; }
  if ('dataRef' in fields) { rec.dataRef = fields.dataRef; rec.skinRef = fields.skinRef; }
  if ('propertyRefs' in fields) { rec.propertyRefs = fields.propertyRefs; }
  if ('extraDataRef' in fields) { rec.extraDataRef = fields.extraDataRef; rec.controllerRef = fields.controllerRef; }
  if (fields?.geometry) rec.geometry = fields.geometry;
  const { geometry, translation, rotation, scale, ...rest } = fields;
  void geometry; void translation; void rotation; void scale;
  rec.fields = rest;
  return rec;
}

/**
 * readNif41 — parse a NIF 4.1.0.12 payload to FULL closure or fail loudly.
 * Emits the same reader-result shape as readNif10 (PecSceneIR-compatible).
 */
export function readNif41(payload, opts = {}) {
  const sourceName = opts.sourceName ?? 'input.nif';
  const s = new Nif41Stream(payload, sourceName);
  // header: text line + version u32 + numBlocks u32 (NO user version, NO type table)
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new LoudError('no newline in header — LOUD FAIL');
  const text = String.fromCharCode(...payload.subarray(0, nl));
  s.pos = nl + 1;
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V4_1_0_12) {
    throw new LoudError(`version 0x${versionRaw.toString(16)} NOT implemented — this reader implements ONLY NIF 4.1.0.12 for the four primary CD_2003 models (LOUD FAIL)`);
  }
  const numBlocks = s.u32();
  if (numBlocks > 100000) throw new LoudError(`implausible numBlocks ${numBlocks}`);
  const blocks = [];
  const decisions = [];
  for (let i = 0; i < numBlocks; i++) {
    const typeOffset = s.pos;
    const type = s.sizedString(); // INLINE block type string (4.x layout)
    const parser = BLOCK_PARSERS[type];
    if (!parser) {
      throw new LoudError(`block ${i}: UNKNOWN type "${type}" — no parser registered in this bounded 4.1 reader (LOUD FAIL)`);
    }
    const dataOffset = s.pos;
    const fields = parser(s);
    blocks.push(makeBlockRecord(i, type, typeOffset, dataOffset, s.pos, fields));
  }
  // footer: u32 numTopObjects + i32 refs; EOF EXACT
  const numTopObjects = s.u32();
  if (numTopObjects > numBlocks) throw new LoudError(`numTopObjects ${numTopObjects} > numBlocks ${numBlocks} — LOUD FAIL`);
  const topObjects = [];
  for (let i = 0; i < numTopObjects; i++) topObjects.push(s.ref());
  if (s.pos !== s.size) {
    throw new LoudError(`CLOSURE_FAIL: parse ended at ${s.pos} != file size ${s.size} — LOUD FAIL`);
  }
  const header = {
    text,
    versionRaw: '0x0401000C',
    versionString: '4.1.0.12',
    numBlocks,
    blockTypes: [...new Set(blocks.map((b) => b.type))],
    blockTypeIndex: blocks.map((b) => b.type), // 4.x: inline per-block (kept for SceneIR metadata compat)
  };
  return {
    readerVersion: PEC_NIF41_READER_VERSION,
    sourceName,
    header,
    blocks,
    footer: { topObjects, numTopObjects },
    closure: { eofExact: true, numBlocksDecoded: blocks.length, decisions },
  };
}

// ---- deep analysis (per-model row; all FILE_SCENE_SPACE, original units) ----

export function analyzeNif41Model(r, meta) {
  const ir = buildAssetIR(r, meta);
  const validation = validateSceneGraph(ir);
  const worldTransforms = composeWorldTransforms(ir);
  const bounds = computeSceneBounds(ir, worldTransforms);
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));

  // block census
  const blockCensus = {};
  for (const b of ir.blocks) blockCensus[b.type] = (blockCensus[b.type] ?? 0) + 1;
  const decodeCensus = {};
  for (const b of ir.blocks) decodeCensus[b.decodeStatus] = (decodeCensus[b.decodeStatus] ?? 0) + 1;

  // complexity
  let triangles = 0, vertices = 0, shapes = 0, nodes = 0, invalidIndexTotal = 0;
  const meshRows = [];
  for (const b of ir.blocks) {
    if (b.type === 'NiTriShape') {
      shapes++;
      const data = b.dataRef != null ? byIndex.get(b.dataRef) : null;
      const g = data?.geometry;
      if (g) {
        triangles += g.numTriangles ?? 0;
        vertices += g.numVertices ?? 0;
        invalidIndexTotal += data.fields?.invalidIndices ?? 0;
      }
      // real mesh→data pairing by dataRef (verified ref, NOT order)
      meshRows.push({
        shapeBlock: b.index, shapeName: b.name, dataBlock: b.dataRef,
        dataOk: !!data && data.type === 'NiTriShapeData',
        numVertices: g?.numVertices ?? null, numTriangles: g?.numTriangles ?? null,
        uvSets: data?.fields?.uvSetCount ?? null,
        hasNormals: data?.fields?.hasNormals ?? null,
        hasColors: data?.fields?.hasColors ?? null,
        propertyRefs: b.propertyRefs,
        extraDataRef: b.fields?.extraDataRef ?? b.extraDataRef ?? null,
      });
    }
    if (b.type === 'NiNode') nodes++;
  }

  // hierarchy summary (verified parent/child by REAL refs)
  const parentOf = new Map(validation.parentOf);
  const depthOf = (idx) => { let d = 0, cur = idx; while (parentOf.has(cur)) { cur = parentOf.get(cur); d++; } return d; };
  let maxDepth = 0;
  const hierarchyRows = ir.blocks
    .filter((b) => b.type === 'NiNode' || b.type === 'NiTriShape')
    .map((b) => {
      const d = depthOf(b.index);
      if (d > maxDepth) maxDepth = d;
      return {
        block: b.index, type: b.type, name: b.name, parent: parentOf.get(b.index) ?? null,
        depth: d, children: b.children ?? null,
      };
    });

  // names census (byte-level names; NOT game classes)
  const nodeNames = ir.blocks
    .filter((b) => b.type === 'NiNode' || b.type === 'NiTriShape' || b.type === 'NiSourceTexture')
    .map((b) => ({ index: b.index, type: b.type, name: b.name }));

  // TRS coverage: non-identity locals
  let nonIdentityTrs = 0;
  const trsRows = [];
  for (const b of ir.blocks) {
    if (!b.localTrs) continue;
    const t = b.localTrs.translate;
    const R = b.localTrs.rotate;
    const isIdent = t[0] === 0 && t[1] === 0 && t[2] === 0 && b.localTrs.scale === 1 &&
      R[0][0] === 1 && R[1][1] === 1 && R[2][2] === 1 &&
      R[0][1] === 0 && R[0][2] === 0 && R[1][0] === 0 && R[1][2] === 0 &&
      R[2][0] === 0 && R[2][1] === 0;
    if (!isIdent) nonIdentityTrs++;
    trsRows.push({
      block: b.index, type: b.type, name: b.name,
      local: { t, r: R, s: b.localTrs.scale },
      world: worldTransforms.has(b.index) ? worldTransforms.get(b.index) : null,
      isIdentityLocal: isIdent,
    });
  }
  const maxAbsLocalTranslate = Math.max(0, ...trsRows.map((r) => Math.max(...r.local.t.map(Math.abs))));
  const maxAbsWorldTranslate = Math.max(0, ...trsRows.map((r) => r.world ? Math.max(...r.world.translate.map(Math.abs)) : 0));
  const nonUnitScaleCount = trsRows.filter((r) => r.local.s !== 1).length;
  const nonIdentityRotateCount = trsRows.filter((r) => !(r.local.r[0][1] === 0 && r.local.r[0][2] === 0 && r.local.r[1][0] === 0 && r.local.r[1][2] === 0 && r.local.r[2][0] === 0 && r.local.r[2][1] === 0)).length;

  // placement analysis: transforms vs vertices (evidence per model)
  let vertexLocalExtents = null;
  {
    let min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
    let any = false;
    for (const b of ir.blocks) {
      if (!b.geometry?.positions) continue;
      any = true;
      const p = b.geometry.positions;
      for (let i = 0; i < p.length; i += 3) {
        for (let k = 0; k < 3; k++) {
          if (p[i + k] < min[k]) min[k] = p[i + k];
          if (p[i + k] > max[k]) max[k] = p[i + k];
        }
      }
    }
    if (any) vertexLocalExtents = { min, max, extents: [max[0] - min[0], max[1] - min[1], max[2] - min[2]] };
  }

  // texture chain extraction (era-labelled; Ark chain only where present)
  const textureEdges = [];
  const standardChainPresent = { NiTexturingProperty: 0, NiSourceTexture: 0 };
  for (const b of ir.blocks) {
    if (b.type === 'NiTexturingProperty') standardChainPresent.NiTexturingProperty++;
    if (b.type === 'NiSourceTexture') standardChainPresent.NiSourceTexture++;
  }
  // Ark texture extra data blocks (by REAL extra-data chains from scene blocks)
  const walkExtraChain = (headRef, depth = 0) => {
    const chain = [];
    let cur = headRef;
    const seen = new Set();
    while (cur != null && cur >= 0 && !seen.has(cur) && depth < 32) {
      seen.add(cur);
      const b = byIndex.get(cur);
      if (!b) break;
      chain.push(b);
      cur = b.fields?.nextExtraDataRef ?? null;
    }
    return chain;
  };
  for (const b of ir.blocks) {
    if (b.type !== 'NiTriShape' && b.type !== 'NiNode') continue;
    const head = b.fields?.extraDataRef ?? null;
    if (head == null || head < 0) continue;
    for (const eb of walkExtraChain(head)) {
      if (eb.type !== 'NiArkTextureExtraData') continue;
      for (const entry of eb.fields?.entries ?? []) {
        textureEdges.push({
          sceneBlock: b.index, sceneBlockName: b.name, extraDataBlock: eb.index,
          textureName: entry.entryName, slotTypeRaw: entry.slotType,
          texturingPropertyRef: entry.texturingPropertyRef,
          bytes9Hex: entry.bytes9Hex,
          binding: 'EXTRA_DATA_CHAIN_REF (verified ref chain)',
        });
      }
    }
  }

  // connected components per mesh (triangle-index graph; NOT a building count)
  const components = [];
  let totalComponents = 0;
  for (const b of ir.blocks) {
    if (!b.geometry?.indices || !b.geometry?.positions) continue;
    const idx = b.geometry.indices;
    const parent = new Int32Array(b.geometry.numVertices).map((_, i) => i);
    const find = (x) => { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; };
    for (let i = 0; i < idx.length; i += 3) {
      const a = find(idx[i]), c = find(idx[i + 1]), d = find(idx[i + 2]);
      if (a !== c) parent[a] = c;
      if (c !== d) parent[c] = d;
    }
    const roots = new Set();
    for (let i = 0; i < b.geometry.numVertices; i++) roots.add(find(i));
    // count only components touched by triangles
    const touched = new Set();
    for (let i = 0; i < idx.length; i++) touched.add(find(idx[i]));
    const comps = [...touched].length;
    components.push({ dataBlock: b.index, numVertices: b.geometry.numVertices, connectedComponents: comps });
    totalComponents += comps;
  }

  // compact per-block dump rows: index/type/name/status/local TRS/world TRS/
  // semantic fields — geometry replaced by counts + byte ranges (no raw arrays
  // in the dump; positions/indices remain derivable from the .nif payload).
  const blockDump = ir.blocks.map((b) => {
    const w = worldTransforms.has(b.index) ? worldTransforms.get(b.index) : null;
    let geometrySummary = null;
    if (b.geometry) {
      geometrySummary = {
        numVertices: b.geometry.numVertices,
        numTriangles: b.geometry.numTriangles,
        hasPositions: !!b.geometry.positions,
        hasNormals: !!b.geometry.normals,
        hasColors: !!b.geometry.colors,
        uvSetCount: (b.geometry.uvSets ?? []).length,
        hasIndices: !!b.geometry.indices,
      };
    }
    const { geometry, ...fieldsNoGeometry } = b.fields ?? {};
    void geometry;
    return {
      index: b.index, type: b.type, name: b.name, decodeStatus: b.decodeStatus,
      localTrs: b.localTrs ?? null,
      worldTrs: w ? { t: w.translate, r: w.rotate, s: w.scale } : null,
      children: b.children ?? null, effects: b.effects ?? null,
      dataRef: b.dataRef ?? null, propertyRefs: b.propertyRefs ?? null,
      extraDataRef: b.fields?.extraDataRef ?? null, controllerRef: b.fields?.controllerRef ?? null,
      geometry: geometrySummary,
      fields: fieldsNoGeometry ?? null,
    };
  });

  const hasMeshGeometry = bounds.meshCount > 0 && Number.isFinite(bounds.min[0]);
  // PHASE-4 ADDITIVE EXPORT (PE_CITY_ASSET_MAP_R1_20261010 phase 4, contract §5):
  // the /catalog wire builder (tools/pecompat/catalog_data.mjs buildPrimaryWire)
  // needs the IR blocks (typed geometry arrays + refs) and the composed world
  // transforms. NO analysis value above changed; the phase-3 CLI dumps read
  // explicit fields and are unaffected. Single code path preserved.
  return {
    ir,
    worldTransforms,
    schemaVersion: ir.schemaVersion,
    readerVersion: PEC_NIF41_READER_VERSION,
    asset: ir.asset,
    roots: ir.roots,
    validationOk: validation.ok,
    validationErrors: validation.errors,
    validationWarnings: validation.warnings,
    blockCensus,
    decodeCensus,
    meshRows,
    hierarchyRows,
    hierarchyMaxDepth: maxDepth,
    nodeNames,
    trsRows,
    trsCoverage: {
      avObjectCount: trsRows.length,
      nonIdentityLocalTrs: nonIdentityTrs,
      nonIdentityRotateCount,
      nonUnitScaleCount,
      maxAbsLocalTranslate,
      maxAbsWorldTranslate,
    },
    vertexLocalExtents,
    complexity: { triangles, vertices, shapes, nodes, blocks: ir.blocks.length, invalidIndexTotal },
    bounds: hasMeshGeometry ? {
      min: bounds.min, max: bounds.max, extents: bounds.extents,
      maxAxisExtent: Math.max(...bounds.extents),
      footprintX: bounds.extents[0], footprintZ: bounds.extents[2],
      meshCount: bounds.meshCount,
    } : null,
    placementFinding: null, // filled by the caller tool with the analysis below
    standardChainPresent,
    textureEdges,
    connectedComponents: { perMesh: components, total: totalComponents, note: 'connected components of the triangle-index graph per mesh — NOT a building count' },
    blockDump,
    space: 'FILE_SCENE_SPACE',
    axisConvention: 'file-serialized x/y/z labels; NO axis swap; NO unit conversion; axis semantics (e.g. up-axis) NOT established by this reader; ORIGINAL file units everywhere — never called meters; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT',
  };
}

/** Placement finding: is the layout in node transforms, in vertices, or BOTH?
 * Evidence: (a) vertex-local spread vs composed-scene spread; (b) non-identity
 * local TRS count/magnitude; (c) per-mesh composed-offset vs vertex-origin. */
export function placementAnalysis(analysis) {
  const vle = analysis.vertexLocalExtents;
  if (!vle || !analysis.bounds) return { finding: 'UNKNOWN', evidence: 'no geometry to compare' };
  const vx = vle.extents[0], vy = vle.extents[1], vz = vle.extents[2];
  const bx = analysis.bounds.extents[0], by = analysis.bounds.extents[1], bz = analysis.bounds.extents[2];
  const spreadGrowth = {
    x: bx > 0 ? vx / bx : null,
    y: by > 0 ? vy / by : null,
    z: bz > 0 ? vz / bz : null,
  };
  const tc = analysis.trsCoverage;
  const e = {
    vertexLocalExtents: vle.extents,
    composedExtents: [bx, by, bz],
    spreadGrowth: spreadGrowth,
    nonIdentityLocalTrs: tc.nonIdentityLocalTrs,
    nonIdentityRotateCount: tc.nonIdentityRotateCount,
    nonUnitScaleCount: tc.nonUnitScaleCount,
    maxAbsLocalTranslate: tc.maxAbsLocalTranslate,
    maxAbsWorldTranslate: tc.maxAbsWorldTranslate,
  };
  // classification (bounded, explicit):
  // VERTICES: vertices already span the scene; local TRS ~identity.
  // TRANSFORMS: vertices tiny/local; scene spread comes from TRS offsets.
  // BOTH: vertex span AND transform offsets both contribute.
  const vertexSpanRatio = Math.max(
    spreadGrowth.x ?? 0, spreadGrowth.y ?? 0, spreadGrowth.z ?? 0);
  const transformsMoveThings = tc.nonIdentityLocalTrs > 0 &&
    (tc.maxAbsWorldTranslate > 1e-6 || tc.nonIdentityRotateCount > 0 || tc.nonUnitScaleCount > 0);
  const verticesSpanScene = vertexSpanRatio > 0.5; // vertices alone cover ≥50% of scene span on ≥1 axis
  if (verticesSpanScene && transformsMoveThings) return { finding: 'BOTH', evidence: e };
  if (verticesSpanScene) return { finding: 'VERTICES', evidence: e };
  if (transformsMoveThings) return { finding: 'TRANSFORMS', evidence: e };
  return { finding: 'AMBIGUOUS', evidence: e };
}

// ---- CLI ----

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv);
  const modelsDir = args['models-dir'];
  const outDir = args['out-dir'];
  if (!modelsDir || !outDir) throw new Error('--models-dir <dir> --out-dir <dir> required');
  const models = (args.models ?? '192374.nif,193207.nif,193313.nif,193684.nif').split(',');
  fs.mkdirSync(outDir, { recursive: true });

  const rows = [];
  for (const name of models) {
    const t0 = Date.now();
    const payload = new Uint8Array(fs.readFileSync(`${modelsDir}\\${name}`));
    const payloadSha256 = crypto.createHash('sha256').update(payload).digest('hex');
    let status = 'DECODED';
    let errorMessage = null;
    let analysis = null;
    try {
      const r = readNif41(payload, { sourceName: name });
      analysis = analyzeNif41Model(r, {
        assetId: parseInt(name.replace(/\.nif$/i, ''), 10) || name,
        era: 'CD_2003',
        build: 'CD_2003_Models_ark_primary_phase3',
        container: 'Models/Models.ark',
        entryName: name,
        payloadSha256,
        sizeBytes: payload.length,
        adapterVersion: PEC_NIF41_READER_VERSION,
        physicalSource: `PRIVATE_OUTPUT/PHASE3_MODELS/${name} (extracted from CD_2003 Models.ark, READ_ONLY original)`,
      });
      analysis.placementFinding = placementAnalysis(analysis);
    } catch (err) {
      status = 'FAILED';
      errorMessage = String(err?.message ?? err);
    }
    // full block dump (private only) + parts CSV
    if (analysis) {
      const dump = {
        artifact: 'PHASE3_BLOCK_DUMP', runId: 'PE_CITY_ASSET_MAP_R1_20261010', era: 'CD_2003',
        model: name, payloadSha256, readerVersion: PEC_NIF41_READER_VERSION,
        header: analysis.asset, roots: analysis.roots,
        blockCensus: analysis.blockCensus, decodeCensus: analysis.decodeCensus,
        meshRows: analysis.meshRows, hierarchyRows: analysis.hierarchyRows,
        nodeNames: analysis.nodeNames, trsRows: analysis.trsRows,
        trsCoverage: analysis.trsCoverage,
        complexity: analysis.complexity, bounds: analysis.bounds,
        placementFinding: analysis.placementFinding,
        standardChainPresent: analysis.standardChainPresent,
        textureEdges: analysis.textureEdges,
        connectedComponents: analysis.connectedComponents,
        validation: { ok: analysis.validationOk, errors: analysis.validationErrors, warnings: analysis.validationWarnings },
        // per-block semantic dump (no raw vertex arrays — counts+flags retained)
        blocks: analysis.blockDump,
      };
      fs.writeFileSync(`${outDir}\\${name.replace('.nif', '')}_blocks.json`, JSON.stringify(dump, null, 1), 'utf8');
      const csv = ['block_index,type,name,decode_status,parent,children_count,num_vertices,num_triangles,local_tx,local_ty,local_tz,local_scale,world_tx,world_ty,world_tz'];
      const byIndexDump = new Map(dump.blocks.map((b) => [b.index, b]));
      for (const hr of analysis.hierarchyRows) {
        const b = byIndexDump.get(hr.block);
        const data = b?.dataRef != null ? byIndexDump.get(b.dataRef) : null;
        csv.push([
          hr.block, hr.type, `"${(hr.name ?? '').replace(/"/g, '""')}"`,
          b?.decodeStatus ?? '', hr.parent ?? -1,
          (hr.children ? hr.children.filter((c) => c != null && c >= 0).length : 0),
          data?.geometry?.numVertices ?? '', data?.geometry?.numTriangles ?? '',
          b?.localTrs ? b.localTrs.translate.join('|') : '',
          b?.localTrs ? b.localTrs.scale : '',
          b?.worldTrs ? b.worldTrs.t.join('|') : '',
        ].join(','));
      }
      fs.writeFileSync(`${outDir}\\${name.replace('.nif', '')}_parts.csv`, csv.join('\r\n') + '\r\n', 'utf8');
    }
    rows.push({
      era: 'CD_2003', model: name, payloadSha256, sizeBytes: payload.length,
      status, error: errorMessage, elapsedMs: Date.now() - t0,
      ...(analysis ? {
        blockCensus: analysis.blockCensus,
        decodeCensus: analysis.decodeCensus,
        complexity: analysis.complexity,
        bounds: analysis.bounds,
        placementFinding: analysis.placementFinding.finding,
        textureEdgeCount: analysis.textureEdges.length,
        standardChainPresent: analysis.standardChainPresent,
        roots: analysis.roots,
      } : {}),
    });
  }
  process.stdout.write(JSON.stringify({ artifact: 'NIF41_DEEP_ANALYSIS_SUMMARY', rows }, null, 1) + '\n');
}

// run CLI only when executed directly (not when imported as a module)
const isDirectRun = process.argv[1] && import.meta.url === new URL(`file:///${process.argv[1].replace(/\\/g, '/')}`).href;
if (isDirectRun) {
  main().catch((err) => {
    console.error('[nif41_deep] FATAL:', err?.stack ?? err);
    process.exitCode = 1;
  });
}
