// NifModelReader40.js — JOB AV-4 (PE_ISO_ASSET_VIEWER loop 8ee81e37, era
// ISO_5_1_0_0, 2026-10-31). Dedicated NIF 4.0.0.0 / 4.0.0.2 adapter.
//
// THE DEDICATED NIF 4.0 FORMAT MODULE (same CEL as NifModelReader41: a version
// family = its own format module; NifModelReader41.js untouched — 4.0 LOUD-FAILs
// there BY DESIGN). NOT integrated into the viewer server (AV-3 owns
// server.mjs/assets.js; PE-MASTER integrates in the next wave — this module
// exports parseModel40() with the same typed-IR contract shape as parseModel41).
//
// LAYOUT DIFF 4.0 vs 4.1 (OBSERVED from Models.ark bytes + gb12 SDK NiStream):
//   header: "NetImmerse File Format, Version 4.0.0.0" / "...4.0.0.2" line +
//           Version(u32) + NumBlocks(u32)  [identical shape to 4.1; NO
//           userVersion, NO type table — blocks carry INLINE RTTI SizedStrings]
//   blocks: inline RTTI per block (NiStream::LoadObject path, < 5.0.0.1)
//   tail:   AFTER all blocks: LoadTopLevelObjects = u32 count + u32 refs
//           (OBSERVED on every sample: `01 00 00 00 00 00 00 00` = 1 top obj,
//           root ref 0; the 41 reader records this as opaque tail bytes).
//   THE KEY DIFFERENCE (< 4.1.0.0 == 0x04010000, gb12 SDK canon):
//     1. "booleans" are 4-BYTE POINTER-PRESENCE FIELDS (NiStreamLoadBinary of a
//        void*), NOT 1-byte NiBool: NiGeometryData hasVertices/hasNormals/
//        hasColors, NiTexturingProperty per-slot hasMap, NiAVObject bounding
//        volume. 4.1 reads 1-byte NiBool for the same fields.
//     2. NiGeometryData texture coords: numTextureSets(i16) is followed by
//        ANOTHER pointer field (m_pkTexture u32) before the UV data (4.1 has
//        no second flag; hasUv gate is 0x0401000C-era).
//     3. NiAVObject bounding volume: pointer flag u32 ONLY — NO bounding box
//        content bytes (SDK reconstructs collision data in memory, reads
//        nothing; 4.1 reads a 1-byte bool + 48B box when set).
//     4. NiZBufferProperty: NO function/test field (< 4.1.0.5) — NET + flags.
//     5. NiTexturingProperty: slot 5 (BUMP_INDEX) carries a BumpMap =
//        Map(22B) + 6 x f32 when present; apply is u32; texture list size u32.
//        4.1 reads the same Map but a 1-byte has + ps2_l/ps2_k/unk1 (the
//        abManual[2] pair) — identical 22B Map span, different presence width.
//   4.0.0.0 vs 4.0.0.2 (OBSERVED: NO LAYOUT DIFFERENCE in the standard block
//   set — the only SDK gates between them are NiSkinData >= 4.0.0.1 and
//   NiGeomMorpherController >= 4.0.0.2, exotic blocks treated OPAQUE here).
//   NiArk blocks: NONE OBSERVED in any sampled 4.0.x file (4.0.0.0 predates
//   the MindArk Ark extension set; any RTTI string starting "NiArk" would hit
//   the OPAQUE anchored path — the census records it loudly if present).
//
// UNKNOWN BLOCK POLICY (same W09 CEL): unknown RTTI = OPAQUE with offset +
// span; boundary ONLY via known-RTTI-anchored search; else span to EOF and
// STOPPED_OPAQUE_NO_BOUNDARY.
//
// IR CONTRACT: mirrors NifModelReader41 (header/blocks/fields names, FILE-ORDER
// byte-hex f32 convention) with documented 4.0-only fields: boundingVolumePtr
// (no hasBoundingBox/boundingBox), texSlotHasPtr (u32, not u8), bumpMapSlots,
// topLevelObjects (decoded tail), no materialFlags difference (NiProperty
// flags u16 present in BOTH 4.0 and 4.1 — SDK NiProperty < 10.0.1.2).

const NIF_V4_0_0_0 = 0x04000000;
const NIF_V4_0_0_2 = 0x04000002;

const KNOWN_V40_TYPES = new Set([
  'NiNode', 'NiTriShape', 'NiTriShapeData', 'NiMaterialProperty',
  'NiAlphaProperty', 'NiZBufferProperty', 'NiVertexColorProperty',
  'NiTexturingProperty',   'NiStringExtraData', 'NiSourceTexture',
  // NiArk* OBSERVED in every 4.0.x file but the 4.1-era layouts do NOT fit
  // (ArkAnimation tail differs; ArkTexture parser threw on most files) —
  // they stay on the OPAQUE anchored path, recorded loudly per census.
]);

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
  'NiCamera', 'NiGeomMorpherController', 'NiGeomMorpherData',
  'NiMorphData', 'NiSwitchNode',
];

class NifStream40 {
  constructor(bytes, sourceName = 'model40.nif') {
    this.bytes = bytes;
    this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.pos = 0;
    this.source = sourceName;
  }
  get size() { return this.bytes.length; }
  get remaining() { return this.size - this.pos; }
  _check(n) {
    if (this.pos + n > this.size) {
      throw new Error(`[NifModelReader40] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[NifModelReader40] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  /** f32 as FILE-ORDER byte hex (same convention as NifModelReader41). */
  f32bits() { this._check(4); let h = ''; for (let i = 0; i < 4; i++) h += this.bytes[this.pos + i].toString(16).padStart(2, '0'); this.pos += 4; return h; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[NifModelReader40] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3bits() { return [this.f32bits(), this.f32bits(), this.f32bits()]; }
  mat33bits() { return [this.vec3bits(), this.vec3bits(), this.vec3bits()]; }
  rawBytes(n) { this._check(n); const b = this.bytes.subarray(this.pos, this.pos + n); this.pos += n; return b; }
}

const bitsToF32 = (hex) => {
  const u = new Uint32Array(1);
  const b = new Uint8Array(u.buffer);
  for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
  return new Float32Array(u.buffer)[0];
};

// ---- v4.0 base layers (gb12 SDK canon, < 4.1.0.0) ----

function readObjectNetV4(s) {
  const name = s.sizedString();
  const extraData = s.i32();   // single extra-data link (< 5.0.0.11)
  const controller = s.i32();
  return { name, extraData, controller };
}

function readAVObjectV40(s) {
  const flags = s.u16();
  const translation = s.vec3bits();
  const rotation = s.mat33bits();
  const scale = s.f32bits();
  const velocity = s.vec3bits();         // v4 only (< 5.0.0.19)
  const numProperties = s.u32();
  if (numProperties > 10000) throw new Error(`[NifModelReader40] impossible numProperties ${numProperties}`);
  const properties = [];
  for (let i = 0; i < numProperties; i++) properties.push(s.i32());
  // < 4.1.0.0: bounding volume is a POINTER-presence u32; NO content bytes.
  const boundingVolumePtr = s.u32();
  const hasBoundingBox = boundingVolumePtr !== 0;
  return { flags, translation, rotation, scale, velocity, numProperties, properties, boundingVolumePtr, hasBoundingBox };
}

function parseNiNode(s) {
  const net = readObjectNetV4(s);
  const av = readAVObjectV40(s);
  const numChildren = s.u32();
  if (numChildren > 100000) throw new Error(`[NifModelReader40] impossible numChildren ${numChildren}`);
  const children = [];
  for (let i = 0; i < numChildren; i++) children.push(s.i32());
  const numEffects = s.u32();
  if (numEffects > 10000) throw new Error(`[NifModelReader40] impossible numEffects ${numEffects}`);
  const effects = [];
  for (let i = 0; i < numEffects; i++) effects.push(s.i32());
  return { ...net, ...av, numChildren, children, numEffects, effects };
}

function parseNiTriShape(s) {
  const net = readObjectNetV4(s);
  const av = readAVObjectV40(s);
  const dataRef = s.i32();
  const skinRef = s.i32(); // NiGeometry < 5.0.0.21: no shader field
  return { ...net, ...av, dataRef, skinRef };
}

function parseNiTriShapeDataV40(s) {
  const numVertices = s.u16();
  if (numVertices > 65535) throw new Error(`[NifModelReader40] impossible numVertices ${numVertices}`);
  // < 4.1.0.0: presence flags are 4-byte POINTER fields, not 1-byte NiBool.
  const vertexPtr = s.u32();
  const hasVertices = vertexPtr !== 0;
  const verticesBits = [];
  if (hasVertices) for (let i = 0; i < numVertices; i++) verticesBits.push(...s.vec3bits());
  const normalPtr = s.u32();
  const hasNormals = normalPtr !== 0;
  const normalsBits = [];
  if (hasNormals) for (let i = 0; i < numVertices; i++) normalsBits.push(...s.vec3bits());
  const center = s.vec3bits();
  const radius = s.f32bits();
  const colorPtr = s.u32();
  const hasVertexColors = colorPtr !== 0;
  const vertexColorsBits = [];
  if (hasVertexColors) for (let i = 0; i < numVertices; i++) vertexColorsBits.push(...s.vec3bits(), s.f32bits());
  const numTextureSets = s.i16();
  if (numTextureSets < 0 || numTextureSets > 8) throw new Error(`[NifModelReader40] impossible numTextureSets ${numTextureSets}`);
  const uvPtr = s.u32(); // second presence pointer BEFORE uv data (< 4.1.0.0)
  const hasUv = uvPtr !== 0;
  const uvSetsBits = [];
  if (numTextureSets > 0 && hasUv) {
    for (let set = 0; set < numTextureSets; set++) {
      const bits = [];
      for (let i = 0; i < numVertices; i++) bits.push(s.f32bits(), s.f32bits());
      uvSetsBits.push(bits);
    }
  }
  const numTriangles = s.u16();
  if (numTriangles > 65535) throw new Error(`[NifModelReader40] impossible numTriangles ${numTriangles}`);
  const numTrianglePoints = s.u32();
  if (numTrianglePoints > 5_000_000) throw new Error(`[NifModelReader40] impossible numTrianglePoints ${numTrianglePoints}`);
  const triangles = [];
  // < 10.0.1.17: bHasList always true — trilist UNCONDITIONAL
  for (let i = 0; i < numTriangles; i++) triangles.push([s.u16(), s.u16(), s.u16()]);
  const numMatchGroups = s.u16();
  if (numMatchGroups > 65535) throw new Error(`[NifModelReader40] impossible numMatchGroups ${numMatchGroups}`);
  const matchGroups = [];
  for (let g = 0; g < numMatchGroups; g++) {
    const count = s.u16();
    const indices = [];
    for (let j = 0; j < count; j++) indices.push(s.u16());
    matchGroups.push({ count, indices });
  }
  return {
    numVertices, hasVertices, vertexPtr, hasNormals, normalPtr, center, radius,
    hasVertexColors, colorPtr, numTextureSets, hasUv, uvPtr,
    numTriangles, numTrianglePoints, numMatchGroups, matchGroups,
    verticesBits, normalsBits, vertexColorsBits, uvSetsBits, triangles,
  };
}

function parseNiMaterialProperty(s) {
  const net = readObjectNetV4(s);
  const materialFlags = s.u16(); // NiProperty base flags (< 10.0.1.2)
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
  const alphaFlags = s.u16();   // NiProperty base flags (bits shifted at link time)
  const alphaThreshold = s.u8();
  return { ...net, alphaFlags, alphaThreshold };
}

function parseNiZBufferPropertyV40(s) {
  const net = readObjectNetV4(s);
  const flags = s.u16();
  // NO function/test field (< 4.1.0.5) — 4.0-only difference vs 4.1
  return { ...net, flags };
}

function parseNiVertexColorProperty(s) {
  const net = readObjectNetV4(s);
  const flags = s.u16();
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32(); // PE-specific extension (observed on 4.0.0.2)
  return { ...net, flags, vertexMode, lightingMode, unknownPeField };
}

const BUMP_INDEX = 5; // gb12 NiTexturingProperty.h enum

function readTexPropMapV40(s, isBump) {
  const source = s.i32();
  const clamp = s.u32();
  const filter = s.u32();
  const uv_set = s.u32();
  const ps2_l = s.i16();
  const ps2_k = s.i16();
  const abManual = [s.u8(), s.u8()]; // < 4.1.0.16: 2 x NiBool
  const map = { source, clamp, filter, uv_set, ps2_l, ps2_k, abManual };
  if (isBump) {
    map.bump = {
      lumaScale: s.f32bits(), lumaOffset: s.f32bits(),
      bumpMat00: s.f32bits(), bumpMat01: s.f32bits(),
      bumpMat10: s.f32bits(), bumpMat11: s.f32bits(),
    };
  }
  return map;
}

function parseNiTexturingPropertyV40(s) {
  const net = readObjectNetV4(s);
  const texFlags = s.u16(); // NiProperty base flags
  const applyMode = s.u32();
  const textureCount = s.u32();
  if (textureCount > 32) throw new Error(`[NifModelReader40] impossible textureCount ${textureCount}`);
  const textures = [];
  for (let i = 0; i < textureCount; i++) {
    const hasPtr = s.u32();  // < 4.1.0.0: POINTER presence, 4 bytes (not u8)
    const has = hasPtr !== 0 ? 1 : 0;
    if (has === 1) {
      const map = readTexPropMapV40(s, i === BUMP_INDEX);
      map.has = 1;
      textures.push(map);
    } else {
      textures.push({ has: 0 });
    }
  }
  return { ...net, texFlags, applyMode, textureCount, textures };
}

function parseNiStringExtraDataV4(s) {
  const nextExtraData = s.i32(); // NiExtraData < 5.0.0.11: m_spNext link, NO name
  const stringData = s.sizedString();
  return { nextExtraData, stringData };
}

function parseNiSourceTextureV40(s) {
  const net = readObjectNetV4(s);
  const fileName = s.sizedString();
  const pixelLayout = s.u32();
  const mipMapped = s.u32();
  const alphaFormat = s.u32();
  const isStatic = s.u8(); // NiBool
  return { ...net, fileName, pixelLayout, mipMapped, alphaFormat, isStatic };
}

// ---- MindArk NiArk extra-data blocks (4.1-era canon, nif_parser_v2.py;
// layout OBSERVED byte-identical in the 4.0.x corpus — closure-validated here).
// NiExtraData < 5.0.0.11 base = single "next" ref (i32, NO name). ----

function parseArkTextureExtraDataV40(s) {
  const nextExtraData = s.i32();
  const unknownInt1a = s.i32();
  const unknownInt1b = s.i32();
  const unknownByte = s.u8();
  const unknownInt2 = s.i32(); // ver2=4.1.0.12 present; observed in 4.0 too
  const numTextures = s.i32();
  if (numTextures < 0 || numTextures > 64) throw new Error(`[NifModelReader40] impossible numTextures ${numTextures}`);
  const arkTextures = [];
  for (let i = 0; i < numTextures; i++) {
    const textureName = s.sizedString();
    const slotType = s.i32();       // 0=BASE, 3=GLOSS, 4=GLOW (era-4.1 canon)
    const unknownInt4 = s.i32();
    const texturingPropertyRef = s.i32();
    const unknownBytes = s.rawBytes(9); // [0]=0, [1..4]=0xFFFFFFFF, [5..8]=texture_id u32 LE
    const textureId = (unknownBytes[1] === 0xff && unknownBytes[2] === 0xff &&
                       unknownBytes[3] === 0xff && unknownBytes[4] === 0xff)
      ? (unknownBytes[5] | (unknownBytes[6] << 8) | (unknownBytes[7] << 16) | (unknownBytes[8] << 24)) >>> 0 : -1;
    arkTextures.push({ textureName, slotType, unknownInt4, texturingPropertyRef, textureId, unknownBytesHex: Array.from(unknownBytes).map(b => b.toString(16).padStart(2, '0')).join('') });
  }
  return { nextExtraData, unknownInt1a, unknownInt1b, unknownByte, unknownInt2, numTextures, arkTextures };
}

function parseArkAnimationExtraDataV40(s) {
  // 4.0.x OBSERVED: payload = next(4) + 4 x i32 (proven prefix) + a
  // variable RAW tail (contains -1.0f patterns; 4.1-era canon 37 x u8 does
  // NOT fit the observed spans). The tail end is found by the SAME
  // known-RTTI-anchored search as the opaque path — fields stay raw.
  const nextExtraData = s.i32();
  const unknownInts = [s.i32(), s.i32(), s.i32(), s.i32()];
  const tailStart = s.pos;
  const boundary = findKnownRttiBoundary(s, s.pos);
  const tailEnd = boundary >= 0 ? boundary : s.size;
  const span = tailEnd - tailStart;
  const rawTail = s.rawBytes(span);
  return {
    nextExtraData, unknownInts,
    tailLen: span, tailEnd,
    tailHexCapped: Array.from(rawTail.subarray(0, Math.min(span, 256))).map(b => b.toString(16).padStart(2, '0')).join(''),
    tailTruncated: span > 256,
    boundaryMethod: boundary >= 0 ? 'known_rtti_anchored' : 'eof_no_anchor',
  };
}

function parseArkImporterExtraDataV40(s) {
  const nextExtraData = s.i32();
  const unknownInt1 = s.i32();
  const unknownInt2 = s.i32();
  const importerName = s.sizedString();
  const unknownBytes = s.rawBytes(13);
  const unknownFloats = [s.f32bits(), s.f32bits(), s.f32bits(), s.f32bits(), s.f32bits(), s.f32bits(), s.f32bits()];
  return { nextExtraData, unknownInt1, unknownInt2, importerName, unknownBytesLen: 13, unknownFloats };
}

function parseNiKeyframeControllerV40(s) {
  // NiTimeController base (no NET fields) + data ref — 4.x layout
  const nextController = s.i32();
  const flags = s.u16();
  const frequency = s.f32bits();
  const phase = s.f32bits();
  const startTime = s.f32bits();
  const stopTime = s.f32bits();
  const target = s.i32();
  const dataRef = s.i32();
  return { nextController, flags, frequency, phase, startTime, stopTime, target, dataRef };
}

const V40_PARSERS = {
  'NiNode': parseNiNode,
  'NiTriShape': parseNiTriShape,
  'NiTriShapeData': parseNiTriShapeDataV40,
  'NiMaterialProperty': parseNiMaterialProperty,
  'NiAlphaProperty': parseNiAlphaProperty,
  'NiZBufferProperty': parseNiZBufferPropertyV40,
  'NiVertexColorProperty': parseNiVertexColorProperty,
  'NiTexturingProperty': parseNiTexturingPropertyV40,
  'NiStringExtraData': parseNiStringExtraDataV4,
  'NiSourceTexture': parseNiSourceTextureV40,
};

// ---- unknown-block OPAQUE boundary (KNOWN-RTTI-ANCHORED only) ----
function findKnownRttiBoundary(s, searchStart) {
  const fileEnd = s.size;
  const anchors = [];
  for (const name of ANCHOR_RTTI_NAMES) {
    const nb = new Uint8Array(name.length);
    for (let i = 0; i < name.length; i++) nb[i] = name.charCodeAt(i);
    anchors.push(nb);
  }
  let pos = searchStart;
  while (pos + 8 <= fileEnd) {
    const nl = s.dv.getInt32(pos, true);
    if (nl >= 1 && nl <= 256 && pos + 4 + nl <= fileEnd) {
      for (const nb of anchors) {
        if (nb.length !== nl) continue;
        let ok = true;
        for (let i = 0; i < nl; i++) { if (s.bytes[pos + 4 + i] !== nb[i]) { ok = false; break; } }
        if (ok) return pos;
      }
    }
    pos++;
  }
  return -1;
}

function versionToString(v) {
  if (v === NIF_V4_0_0_0) return '4.0.0.0';
  if (v === NIF_V4_0_0_2) return '4.0.0.2';
  return `0x${v.toString(16).padStart(8, '0')}`;
}

/**
 * parseModel40 — parse a NIF 4.0.0.0 / 4.0.0.2 payload into the typed IR.
 * Same return contract shape as parseModel41: { extraction, renderModel }.
 */
export function parseModel40(payload, sourceName = 'model40.nif') {
  const s = new NifStream40(payload, sourceName);

  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new Error('[NifModelReader40] no newline in header — LOUD FAIL');
  const headerText = String.fromCharCode(...payload.subarray(0, nl));
  s.seek(nl + 1);
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V4_0_0_0 && versionRaw !== NIF_V4_0_0_2) {
    throw new Error(`[NifModelReader40] version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — this adapter implements ONLY NIF 4.0.0.0 (0x04000000) and 4.0.0.2 (0x04000002); LOUD FAIL`);
  }
  const numBlocks = s.u32();
  if (numBlocks > 100000) throw new Error(`[NifModelReader40] impossible numBlocks ${numBlocks}`);
  const dataStartOffset = s.pos;

  const extraction = {
    schema: 'av4-nif40-canonical-extraction-v1',
    adapter: 'NifModelReader40 (src/pesource/NifModelReader40.js — dedicated NIF 4.0.0.0/4.0.0.2 adapter; gb12-SDK-canon semantics, per-file boundary-validated)',
    formatFamily: `NIF ${versionToString(versionRaw)} (inline RTTI, pointer-presence u32 flags, top-level object list tail)`,
    source: { entryName: sourceName },
    header: {
      text: headerText,
      versionRaw: `0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`,
      versionString: versionToString(versionRaw),
      numBlocks,
      dataStartOffset,
    },
    blocks: [],
    opaqueBlocks: [],
    topLevelObjects: null,
    fileTailBytesHex: null,
    fileTailBytesLen: null,
  };

  for (let blockIndex = 0; blockIndex < numBlocks; blockIndex++) {
    const rttiStart = s.pos;
    const type = s.sizedString();
    const parser = V40_PARSERS[type];
    if (!parser || !KNOWN_V40_TYPES.has(type)) {
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
        rawHexCapped: rawCapped, rawHexTruncated: span > 4096, fields: null,
      });
      extraction.opaqueBlocks.push({ index: blockIndex, type, offset: opaqueStart, span, boundaryMethod: boundary >= 0 ? 'known_rtti_anchored' : 'eof_no_anchor' });
      s.seek(opaqueEnd);
      if (boundary < 0) {
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

  // ---- tail: LoadTopLevelObjects (u32 count + refs) + any leftover bytes ----
  if (!extraction.parseStatus && s.remaining >= 4) {
    const topCount = s.u32();
    if (topCount <= 1000) {
      const refs = [];
      let ok = true;
      for (let i = 0; i < topCount; i++) {
        if (s.remaining < 4) { ok = false; break; }
        refs.push(s.i32());
      }
      if (ok) {
        extraction.topLevelObjects = { count: topCount, refs };
        const tailLen = s.size - s.pos;
        let tailHex = '';
        for (let i = 0; i < tailLen; i++) tailHex += payload[s.pos + i].toString(16).padStart(2, '0');
        extraction.fileTailBytesHex = tailHex;
        extraction.fileTailBytesLen = tailLen;
        extraction.parseStatus = 'PASS';
      }
    }
  }
  if (!extraction.parseStatus) {
    // No top-level tail decoded (truncated or stopped) — record raw tail.
    const tailLen = s.remaining;
    let tailHex = '';
    for (let i = 0; i < tailLen; i++) tailHex += payload[s.pos + i].toString(16).padStart(2, '0');
    extraction.fileTailBytesHex = tailHex;
    extraction.fileTailBytesLen = tailLen;
    if (!extraction.parseStatus) extraction.parseStatus = 'STOPPED_NO_TOPLEVEL_TAIL';
  }
  // closure audit: every consecutive known block must be byte-tight
  let closureViolations = 0;
  for (let i = 1; i < extraction.blocks.length; i++) {
    const a = extraction.blocks[i - 1], b = extraction.blocks[i];
    if (!a.opaque && !b.opaque && a.blockEnd !== b.rttiStart) closureViolations++;
  }
  extraction.closureViolations = closureViolations;

  const renderModel = buildRenderModel40(extraction);
  return { extraction, renderModel };
}

/** Same compose semantics as NifModelReader41 (row-dot, no transpose). */
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

const AV40_TYPES = new Set(['NiNode', 'NiTriShape']);

function buildRenderModel40(extraction) {
  const blocks = extraction.blocks;
  const byIndex = new Map(blocks.map(b => [b.index, b]));

  const childOf = new Map();
  for (const b of blocks) {
    if (b.type === 'NiNode' && b.fields && Array.isArray(b.fields.children)) {
      for (const c of b.fields.children) if (c >= 0 && byIndex.has(c)) childOf.set(c, b.index);
    }
  }

  const localTRS = new Map();
  for (const b of blocks) {
    if (AV40_TYPES.has(b.type) && b.fields) {
      localTRS.set(b.index, {
        translation: b.fields.translation.map(bitsToF32),
        rotation: b.fields.rotation.map(r => r.map(bitsToF32)),
        scale: bitsToF32(b.fields.scale),
      });
    }
  }
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

  const shapes = [];
  for (const b of blocks) {
    if (b.type !== 'NiTriShape' || !b.fields) continue;
    const data = b.fields.dataRef >= 0 ? byIndex.get(b.fields.dataRef) : null;
    if (!data || data.type !== 'NiTriShapeData' || !data.fields) {
      throw new Error(`[NifModelReader40] NiTriShape #${b.index}: dataRef ${b.fields.dataRef} does not resolve to a NiTriShapeData block — LOUD FAIL`);
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
    const props = (b.fields.properties || []).filter(p => p >= 0).map(p => byIndex.get(p)).filter(Boolean);
    const mat = props.find(p => p.type === 'NiMaterialProperty');
    const alpha = props.find(p => p.type === 'NiAlphaProperty');
    const texprop = props.find(p => p.type === 'NiTexturingProperty');
    // resolve texture file names through NiSourceTexture blocks
    const textures = texprop ? texprop.fields.textures.map(slot => {
      if (!slot || slot.has !== 1) return slot || { has: 0 };
      const src = slot.source >= 0 ? byIndex.get(slot.source) : null;
      return { ...slot, sourceType: src ? src.type : null, sourceFileName: src && src.fields ? src.fields.fileName : null };
    }) : [];
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
        blockIndex: mat.index, name: mat.fields.name,
        materialFlags: mat.fields.materialFlags,
        ambient: mat.fields.ambient.map(bitsToF32),
        diffuse: mat.fields.diffuse.map(bitsToF32),
        specular: mat.fields.specular.map(bitsToF32),
        emissive: mat.fields.emissive.map(bitsToF32),
        glossiness: bitsToF32(mat.fields.glossiness),
        alpha: bitsToF32(mat.fields.alpha),
      } : null,
      alphaProp: alpha ? { blockIndex: alpha.index, flags: alpha.fields.alphaFlags, threshold: alpha.fields.alphaThreshold } : null,
      textureProp: texprop ? { blockIndex: texprop.index, texFlags: texprop.fields.texFlags, applyMode: texprop.fields.applyMode, textures } : null,
      controllerRef: b.fields.controller,
    });
  }

  const roots = [...localTRS.keys()].filter(idx => !childOf.has(idx));
  return {
    adapter: 'NifModelReader40',
    shapes,
    controllers: [],
    roots,
    counts: {
      blocks: blocks.length,
      shapes: shapes.length,
      controllers: 0,
      opaque: extraction.opaqueBlocks.length,
    },
  };
}

export { NIF_V4_0_0_0, NIF_V4_0_0_2, KNOWN_V40_TYPES };
