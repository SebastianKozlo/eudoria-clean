// NifModelReader.js — PE MILESTONE 1 ITER 051 (ledger ITER_037).
// THE CLEAN MINIMAL NIF READER — ONE MODEL scope (the ORIGINAL-DIRECT
// single-model witness, architect decision #3).
//
// Scope contract (NEXT_PROMPT ITER_051): this reader parses the ONE witness
// model (457485.nif, VCL climate-0 col0 id 457485, the foliage page's most
// frequent rendered model) from the era PCG_9_3_5 Models.bnt ORIGINAL bytes.
// It is NOT a corpus parser. Version gate: NIF 10.1.0.0 ONLY (the witness
// model's version; other versions fail LOUDLY — extending them is a later
// iteration, era-validated per ledger ENTRY #3).
//
// FORMAT KNOWLEDGE BASIS (the R61 frozen python parser = the ORACLE, the
// documented layout canon; this reader derives everything from the NIF
// bytes itself and is cross-validated BIT-EXACTLY against the R61 output
// by m1_iter037_crosscheck.py — the ORACLE is never an input here):
//   header v10 (pe_header.py): header text line + u32 version + u32
//   userVersion + u32 numBlocks + u16 numBlockTypes + SizedString types +
//   u16 blockTypeIndex[numBlocks] + u32 numGroups + u32 groups[].
//   blocks v10 (pe_block_reader.py): per block a u32 preamble (MUST be 0 —
//   non-zero = parser desynchronization = LOUD FAIL), type from the header
//   type table, then the class payload.
//   boolean mode: v10.1.0.0 >= 0x04010000 -> 1-byte booleans.
//
// LOUD-FAILURE CONTRACT: no silent fallbacks. Unknown block type = LOUD
// FAIL (the R61 FAIL-CLOSED parity: the reader aborts with the block index,
// type name and offset recorded). Unknown VARIANT inside a known block =
// LOUD FAIL with the discriminator values. Unknown bytes inside a known
// partial block (the Ark extension blocks) are recorded RAW + labeled
// (never interpreted) — the boundary method is recorded per block exactly
// as the ORACLE records it.
//
// THE ERA TEXTURE BINDING (a loud finding of the witness census, 10/10
// foliage climate-0 candidates): these PCG-era v10 models carry NO
// NiSourceTexture block; the base texture binds via the PE-specific
// NiArkTextureExtraData (entry -> ref to the NiTexturingProperty block;
// trailing 9 bytes = [0x00][0xFFFFFFFF][u32 LE textureId] — the canon rule
// CONFIRMED on 347937 + all 21 ArkTextures, nif_parser_v2) and the
// NiTexturingProperty BASE slot (slot 0) supplies clamp/filter/uvSet with
// source = -1 (NULL). The textureId resolves against the era Textures.bnt
// ('<id>.dat' entry, PESourceMount.resolveTexture — era-explicit).
//
// UV CONVENTION (r185 calibration-gate E discipline): NIF uv values are
// used RAW (no V flip) and sample an image whose row 0 = the visual TOP
// (see TgaDecoder.decodeTga2A32Image). Evidence: the legacy UVConv v1
// byte-probe (runtime_flipY_probe.json, r169 runtime: v=0 samples the image
// top with flipY=false upload) + the witness model's own structure (the
// card top vertices carry v≈0.104, the bottom v≈0.940 — v increases DOWNWARD
// on the height axis; the bottom vertices carry the dark ground-shadow
// vertex colors at z=0). Documented choice; a future D3D8 runtime capture
// can falsify it.

const NIF_V10_1_0_0 = 0x0A010000;

const KNOWN_V10_TYPES = new Set([
  'NiNode', 'NiArkAnimationExtraData', 'NiArkImporterExtraData',
  'NiArkTextureExtraData', 'NiTexturingProperty', 'NiArkViewportInfoExtraData',
  'NiMaterialProperty', 'NiZBufferProperty', 'NiVertexColorProperty',
  'NiArkShaderExtraData', 'NiStringExtraData', 'NiTriShape', 'NiAlphaProperty',
  'NiTriShapeData',
]);

// The NIED pattern pre-pass of the viewport boundary search (R61 M1D-31R).
const NIED_PATTERN = [0x00, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x00, 0x00,
  ...['N', 'i', 'S', 't', 'r', 'i', 'n', 'g', 'E', 'D', '0', '0'].map(c => c.charCodeAt(0))];

class NifStream {
  constructor(bytes, sourceName = 'witness.nif') {
    this.bytes = bytes;
    this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.pos = 0;
    this.source = sourceName;
  }
  get size() { return this.bytes.length; }
  get remaining() { return this.size - this.pos; }
  _check(n) {
    if (this.pos + n > this.size) {
      throw new Error(`[NifModelReader] read(${n}) at ${this.pos} exceeds size ${this.size} (source=${this.source})`);
    }
  }
  seek(p) {
    if (p < 0 || p > this.size) throw new Error(`[NifModelReader] seek(${p}) out of bounds [0,${this.size}]`);
    this.pos = p;
  }
  u8() { this._check(1); return this.bytes[this.pos++]; }
  u16() { this._check(2); const v = this.dv.getUint16(this.pos, true); this.pos += 2; return v; }
  i16() { this._check(2); const v = this.dv.getInt16(this.pos, true); this.pos += 2; return v; }
  u32() { this._check(4); const v = this.dv.getUint32(this.pos, true); this.pos += 4; return v; }
  i32() { this._check(4); const v = this.dv.getInt32(this.pos, true); this.pos += 4; return v; }
  /** f32 as IEEE-754 bit pattern — FILE-ORDER byte hex (8 chars), the exact
   * parity of Python struct.pack('<f', v).hex() (the oracle's convention):
   * the bytes in stream order, NOT the big-endian numeric display. */
  f32bits() { this._check(4); let h = ''; for (let i = 0; i < 4; i++) h += this.bytes[this.pos + i].toString(16).padStart(2, '0'); this.pos += 4; return h; }
  f32() { this._check(4); const v = this.dv.getFloat32(this.pos, true); this.pos += 4; return v; }
  boolean() { return this.u8() !== 0; } // v10.1.0.0: 1-byte booleans
  sizedString() {
    const len = this.i32();
    if (len < 0 || len > 1_000_000) throw new Error(`[NifModelReader] bad string length ${len} at ${this.pos - 4}`);
    this._check(len);
    const s = String.fromCharCode(...this.bytes.subarray(this.pos, this.pos + len));
    this.pos += len;
    return s;
  }
  vec3bits() { return [this.f32bits(), this.f32bits(), this.f32bits()]; }
  mat33bits() { return [this.vec3bits(), this.vec3bits(), this.vec3bits()]; }
  color4bits() { return [this.f32bits(), this.f32bits(), this.f32bits(), this.f32bits()]; }
  texcoordbits() { return [this.f32bits(), this.f32bits()]; }
  rawHex(n) { this._check(n); let s = ''; for (let i = 0; i < n; i++) s += this.bytes[this.pos + i].toString(16).padStart(2, '0'); this.pos += n; return s; }
}

/** The R61 _find_v10_boundary parity (pe_standard_blocks.py C8-H-R1):
 * search forward for the next v10 block preamble (u32=0 + valid SizedString
 * + numExtraData <= 10000 + controller -1 or 0..10000). */
function findV10Boundary(bytes, dv, searchStart, fileEnd, acceptControllerZero = false) {
  let pos = searchStart;
  while (pos + 8 <= fileEnd) {
    if (dv.getUint32(pos, true) === 0) {
      const nl = dv.getInt32(pos + 4, true);
      if (nl >= 0 && nl <= 256 && pos + 8 + nl <= fileEnd) {
        if (nl === 0) {
          if (pos + 16 <= fileEnd) {
            const numExtra = dv.getUint32(pos + 8, true);
            if (numExtra <= 10000) {
              const controller = dv.getInt32(pos + 12, true);
              if (controller === -1 || (acceptControllerZero && controller === 0)) return pos;
            }
          } else if (pos + 12 <= fileEnd) {
            if (dv.getUint32(pos + 8, true) <= 10000) return pos;
          }
        } else {
          const nameStart = pos + 8;
          let printable = 0;
          for (let i = 0; i < nl; i++) { const b = bytes[nameStart + i]; if (b >= 32 && b <= 126) printable++; }
          if (printable >= nl * 0.8) {
            const afterName = nameStart + nl;
            if (afterName + 8 <= fileEnd) {
              const numExtra = dv.getUint32(afterName, true);
              if (numExtra <= 10000) {
                const controller = dv.getInt32(afterName + 4, true);
                if (controller === -1 || (controller >= 0 && controller <= 10000)) return pos;
              }
            } else if (afterName + 4 <= fileEnd) {
              if (dv.getUint32(afterName, true) <= 10000) return pos;
            } else if (afterName >= fileEnd) {
              return pos;
            }
          }
        }
      }
    }
    pos++;
  }
  return -1;
}

function bytesIndexOf(haystack, needle, from, to) {
  outer: for (let i = from; i <= to - needle.length; i++) {
    for (let j = 0; j < needle.length; j++) {
      if (haystack[i + j] !== needle[j]) continue outer;
    }
    return i;
  }
  return -1;
}

// ---- v10 block payload parsers (one per witness chain type) ----
// Each returns the canonical `fields` object (the extraction schema; the
// ORACLE emits the identical shape).

function readObjectNet(s) {
  const name = s.sizedString();
  const numExtraData = s.u32();
  const extraData = [];
  for (let i = 0; i < numExtraData; i++) extraData.push(s.i32());
  const controller = s.i32();
  return { name, numExtraData, extraData, controller };
}

function readAVObject(s) {
  const flags = s.u16();
  const translation = s.vec3bits();
  const rotation = s.mat33bits();
  const scale = s.f32bits();
  // v10: NO velocity, NO bounding box (v4-only per the R61 canon)
  const numProperties = s.u32();
  const properties = [];
  for (let i = 0; i < numProperties; i++) properties.push(s.i32());
  const collisionObject = s.i32(); // v10: collision object ref (>= 10.0.1.0)
  return { flags, translation, rotation, scale, numProperties, properties, collisionObject };
}

function parseNiNode(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const numChildren = s.u32();
  const children = [];
  for (let i = 0; i < numChildren; i++) children.push(s.i32());
  const numEffects = s.u32();
  const effects = [];
  for (let i = 0; i < numEffects; i++) effects.push(s.i32());
  return { ...net, ...av, numChildren, children, numEffects, effects };
}

function parseNiArkAnimationExtraData(s) {
  const name = s.sizedString();
  const u1 = s.i32(), u2 = s.i32(), u3 = s.i32(), u4 = s.i32();
  const u2u = u2 >>> 0;
  let variant = null, extSize = 0, extRawHex = '', boundaryMethod = null;
  if (u2u === 0xFFFFFFFF) {
    const u4u = u4 >>> 0;
    if (u4u === 0x01000000) {
      variant = 'V10_BASE_33B'; extSize = 33; extRawHex = s.rawHex(33); boundaryMethod = 'fixed_size';
    } else if (u4u === 0x00000000) {
      variant = 'V10_BASE_0B'; extSize = 0; boundaryMethod = 'fixed_size';
    } else {
      throw new Error(`[NifModelReader] NiArkAnimationExtraData u4=0x${u4u.toString(16)} has no P0-verified extension size — LOUD FAIL (witness scope)`);
    }
  } else {
    // u2=2 family (G3A/G3A_PREAMBLE simple sub-cases only — the boundary-search
    // sub-families are NOT implemented in the witness reader; LOUD FAIL if hit)
    const u3u = u3 >>> 0, u4u = u4 >>> 0;
    if (u3u === 0 && u4u === 0x00000000 && s.remaining === 0) {
      variant = 'G3A'; extSize = 0; boundaryMethod = 'fixed_size';
    } else if (u3u === 0 && u4u === 0x00000000 && s.pos + 12 <= s.size &&
               s.dv.getUint32(s.pos, true) === 0) {
      const nameLen = s.dv.getInt32(s.pos + 4, true);
      if (nameLen >= 0 && nameLen <= 256) {
        variant = 'G3A_PREAMBLE'; extSize = 0; boundaryMethod = 'preamble_detected';
      }
    }
    if (variant === null) {
      throw new Error(`[NifModelReader] NiArkAnimationExtraData u2=2 u3=${u3} u4=${u4} sub-family NOT implemented in the witness reader — LOUD FAIL`);
    }
  }
  return { name, u1, u2, u3, u4, variant, extSize, extRawHex, boundaryMethod };
}

function parseNiArkImporterExtraData(s) {
  const name = s.sizedString();
  const int = s.i32();
  const versionString = s.sizedString();
  if (s.remaining < 38) throw new Error('[NifModelReader] importer trailing < 38B — LOUD FAIL');
  const trailing38BHex = s.rawHex(38);
  return { name, int, versionString, trailing38BHex };
}

function parseNiArkTextureExtraData(s, extraction) {
  const header3BytesHex = s.rawHex(3);
  const name = s.sizedString();
  const numTex = s.i32();
  const field1 = s.i32();
  const field2 = s.i32();
  const field2u = field2 >>> 0;
  const entryCount = (field2u >>> 8) & 0x00FFFFFF;
  const field2Low8 = field2u & 0xFF;
  s.u8(); // padding byte
  const entries = [];
  for (let i = 0; i < entryCount; i++) {
    const nameLen = s.i32();
    if (nameLen < 1 || nameLen > 256) {
      throw new Error(`[NifModelReader] ArkTexture entry ${i}: invalid name length ${nameLen} — LOUD FAIL`);
    }
    s._check(nameLen);
    const eName = String.fromCharCode(...s.bytes.subarray(s.pos, s.pos + nameLen));
    s.pos += nameLen;
    const f1 = s.i32();
    const f2 = s.i32();
    const ref = s.i32();
    const unkHex = s.rawHex(9);
    const unkBytes = [];
    for (let j = 0; j < 9; j++) unkBytes.push(parseInt(unkHex.substr(j * 2, 2), 16));
    // The canon rule (CONFIRMED on 347937, all 21 ArkTextures, nif_parser_v2):
    // unk[0]=0x00, unk[1..4]=0xFFFFFFFF, unk[5..8]=u32 LE Textures.bnt entry ID.
    const textureId = (unkBytes[5] | (unkBytes[6] << 8) | (unkBytes[7] << 16) | (unkBytes[8] << 24)) >>> 0;
    entries.push({
      name: eName, f1, f2, ref, unkHex, textureId,
      textureIdDecodeRule: 'unk[0]=0x00, unk[1..4]=0xFFFFFFFF, unk[5..8]=u32 LE Textures.bnt entry ID (canon CONFIRMED on 347937, all 21 ArkTextures, nif_parser_v2)',
    });
  }
  if (entryCount > 0) extraction._arkTextureId = entries[0].textureId;
  return { header3BytesHex, name, numTex, field1, field2, entryCount, field2Low8, entries };
}

function parseNiTexturingProperty(s) {
  const net = readObjectNet(s);
  const fieldA = s.u16();
  const fieldB = s.u16();
  const textureCount = s.u32();
  const textures = [];
  let slot5Has = 0;
  for (let i = 0; i < textureCount; i++) {
    const has = s.u8();
    if (has !== 0 && has !== 1) throw new Error(`[NifModelReader] texprop slot ${i}: invalid Has=${has} — LOUD FAIL`);
    if (has === 1) {
      const source = s.i32();
      const clamp = s.u32();
      const filter = s.u32();
      const uvSet = s.u32();
      const tailA = s.i16();
      const tailB = s.i16();
      const transformPresent = s.u8();
      let transformPayloadHex = '';
      if (transformPresent === 1) transformPayloadHex = s.rawHex(32);
      else if (transformPresent !== 0) {
        throw new Error(`[NifModelReader] texprop slot ${i}: invalid transform_present=${transformPresent} — LOUD FAIL`);
      }
      textures.push({ has: 1, source, clamp, filter, uv_set: uvSet, tail_A: tailA, tail_B: tailB, transform_present: transformPresent });
    } else {
      textures.push({ has: 0 });
    }
    if (i === 5) slot5Has = has;
  }
  const bumpPayloadHex = slot5Has === 1 ? s.rawHex(24) : '';
  const trailingU32 = s.u32();
  return { ...net, fieldA, fieldB, textureCount, textures, bumpPayloadHex, trailingU32 };
}

function parseNiArkViewportInfoExtraData(s, extraction) {
  const name = s.sizedString();
  const extStart = s.pos;
  const fileEnd = s.size;
  // R61 parity: NIED pattern pre-pass (M1D-31R), then the strict boundary
  // search (C8-H-R1), then the relaxed pass (M1D-30), then the last-block
  // guard (C13-A). The method label mirrors the ORACLE's.
  let boundaryMethod = null;
  let foundEnd = bytesIndexOf(s.bytes, NIED_PATTERN, extStart + 13, Math.min(extStart + 70, fileEnd));
  if (foundEnd >= 0) {
    boundaryMethod = 'v10_nied_pattern';
  } else {
    foundEnd = findV10Boundary(s.bytes, s.dv, extStart + 13, fileEnd, false);
  }
  const VP_MAX_EXT = 200;
  if (foundEnd < 0 || (foundEnd - extStart) > VP_MAX_EXT) {
    const relaxedEnd = findV10Boundary(s.bytes, s.dv, extStart + 13, fileEnd, true);
    if (relaxedEnd >= 0 && (relaxedEnd - extStart) <= VP_MAX_EXT) {
      foundEnd = relaxedEnd;
      boundaryMethod = 'v10_relaxed_ctrl0';
    }
  }
  if (foundEnd < 0) {
    if (fileEnd - extStart <= 200) {
      foundEnd = fileEnd;
      boundaryMethod = 'v10_last_block';
    } else {
      throw new Error('[NifModelReader] NiArkViewportInfoExtraData: no block boundary found — LOUD FAIL');
    }
  }
  const extSize = foundEnd - extStart;
  const extRawHex = extSize > 0 ? (() => { let h = ''; for (let i = 0; i < extSize; i++) h += s.bytes[extStart + i].toString(16).padStart(2, '0'); return h; })() : '';
  s.seek(foundEnd);
  if (boundaryMethod === null) boundaryMethod = 'v10_boundary_search';
  return { name, extStart, extEnd: foundEnd, extSize, extRawHex, boundaryMethod };
}

function parseNiMaterialProperty(s) {
  const net = readObjectNet(s);
  // v10 (10.1.0.0 > 10.0.1.2): NO flags field (niflib version gate)
  const ambient = s.vec3bits();
  const diffuse = s.vec3bits();
  const specular = s.vec3bits();
  const emissive = s.vec3bits();
  const glossiness = s.f32bits();
  const alpha = s.f32bits();
  return { ...net, ambient, diffuse, specular, emissive, glossiness, alpha };
}

function parseNiZBufferProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  const fn = s.u32(); // >= 0x0401000C
  return { ...net, flags, function: fn };
}

function parseNiVertexColorProperty(s) {
  const net = readObjectNet(s);
  const flags = s.u16();
  const vertexMode = s.u16();
  const lightingMode = s.u16();
  const unknownPeField = s.u32(); // PE-specific extension (always consumed)
  return { ...net, flags, vertexMode, lightingMode, unknownPeField };
}

function parseNiArkShaderExtraData(s) {
  const name = s.sizedString(); // NiExtraData base v10: name only
  const unknownInt = s.i32();
  const unknownString = s.sizedString();
  return { name, unknownInt, unknownString };
}

function parseNiStringExtraData(s) {
  const name = s.sizedString();
  const stringData = s.sizedString();
  return { name, stringData };
}

function parseNiTriShape(s) {
  const net = readObjectNet(s);
  const av = readAVObject(s);
  const dataRef = s.i32();
  const skinRef = s.i32();
  let hasShader = 0;
  if (0x0A000100 <= NIF_V10_1_0_0 && NIF_V10_1_0_0 <= 0x14010003) {
    hasShader = s.u8();
    if (hasShader) {
      // NOT hit by the witness; loud if ever encountered (shaderName +
      // shaderUnknownInt would be required — the R61 canon)
      const shaderName = s.sizedString();
      const shaderUnknownInt = s.i32();
      return { ...net, ...av, dataRef, skinRef, hasShader, shaderName, shaderUnknownInt };
    }
  }
  return { ...net, ...av, dataRef, skinRef, hasShader };
}

function parseNiAlphaProperty(s) {
  const net = readObjectNet(s);
  const alphaFlags = s.u16();
  const alphaThreshold = s.u8();
  return { ...net, alphaFlags, alphaThreshold };
}

function parseNiTriShapeData(s) {
  const numVertices = s.u16();
  if (numVertices > 65535) throw new Error(`[NifModelReader] impossible numVertices ${numVertices}`);
  const keepFlags = s.u8();
  const compressFlags = s.u8();
  const hasVertices = s.boolean();
  const verticesBits = [];
  if (hasVertices) for (let i = 0; i < numVertices; i++) { verticesBits.push(...s.vec3bits()); }
  const numUvSets = s.u16();
  const uvCount = numUvSets & 63;
  const tangentFlag = numUvSets & 0xF000;
  const hasNormals = s.boolean();
  const normalsBits = [];
  if (hasNormals) {
    for (let i = 0; i < numVertices; i++) normalsBits.push(...s.vec3bits());
    if (tangentFlag !== 0) {
      // NOT hit by the witness; loud support would be required (the R61 canon)
      for (let i = 0; i < numVertices; i++) s.vec3bits(); // tangents
      for (let i = 0; i < numVertices; i++) s.vec3bits(); // bitangents
    }
  }
  const center = s.vec3bits();
  const radius = s.f32bits();
  const hasVertexColors = s.boolean();
  const vertexColorsBits = [];
  if (hasVertexColors) for (let i = 0; i < numVertices; i++) vertexColorsBits.push(...s.color4bits());
  const uvSetsBits = [];
  for (let set = 0; set < uvCount; set++) {
    const bits = [];
    for (let i = 0; i < numVertices; i++) bits.push(...s.texcoordbits());
    uvSetsBits.push(bits);
  }
  const consistencyFlags = s.u16();
  const numTriangles = s.u16();
  const numTrianglePoints = s.u32();
  if (numTrianglePoints > 200000) throw new Error(`[NifModelReader] impossible numTrianglePoints ${numTrianglePoints}`);
  const hasTriangles = s.boolean();
  const triangles = [];
  if (hasTriangles) {
    if (numTriangles === 0) throw new Error('[NifModelReader] hasTriangles=true but numTriangles=0 — LOUD FAIL');
    for (let i = 0; i < numTriangles; i++) triangles.push([s.u16(), s.u16(), s.u16()]);
  }
  const numMatchGroups = s.u16();
  const matchGroups = [];
  for (let i = 0; i < numMatchGroups; i++) {
    const count = s.u16();
    if (count > 65535) throw new Error(`[NifModelReader] impossible matchGroup count ${count}`);
    const indices = [];
    for (let j = 0; j < count; j++) indices.push(s.u16());
    matchGroups.push({ count, indices });
  }
  return {
    numVertices, keepFlags, compressFlags, hasVertices,
    numUvSets, uvCount, tangentFlag, hasNormals,
    center, radius, hasVertexColors,
    consistencyFlags, numTriangles, numTrianglePoints, hasTriangles,
    numMatchGroups, matchGroups,
    verticesBits, normalsBits, vertexColorsBits, uvSetsBits, triangles,
  };
}

/**
 * parseWitnessModel — parse the ONE witness model's NIF payload (v10.1.0.0).
 * @param {Uint8Array} payload raw NIF bytes from Models.bnt (via PESourceMount.getModelResource)
 * @returns {{ extraction: object, renderModel: object }}
 *   extraction: the canonical bit-exact extraction (compared against the R61 oracle)
 *   renderModel: the render-ready arrays (Float32Array positions/normals/uvs/colors + index)
 */
export function parseWitnessModel(payload, sourceName = 'witness.nif') {
  const s = new NifStream(payload, sourceName);

  // ---- header ----
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new Error('[NifModelReader] no newline in header — LOUD FAIL');
  const headerText = String.fromCharCode(...payload.subarray(0, nl));
  s.seek(nl + 1);
  const versionRaw = s.u32();
  if (versionRaw !== NIF_V10_1_0_0) {
    throw new Error(`[NifModelReader] version 0x${versionRaw.toString(16).padStart(8, '0')} NOT implemented — the witness reader implements ONLY NIF 10.1.0.0 (ONE-MODEL scope); LOUD FAIL`);
  }
  const userVersion = s.u32();
  const numBlocks = s.u32();
  const numBlockTypes = s.u16();
  const blockTypes = [];
  for (let i = 0; i < numBlockTypes; i++) blockTypes.push(s.sizedString());
  const blockTypeIndex = [];
  for (let i = 0; i < numBlocks; i++) blockTypeIndex.push(s.u16());
  const numGroups = s.u32();
  const groups = [];
  for (let i = 0; i < numGroups; i++) groups.push(s.u32());
  const dataStartOffset = s.pos;

  // ---- blocks ----
  const extraction = {
    schema: 'iter037-witness-canonical-extraction-v1',
    oracle: {
      parser: 'clean JS NifModelReader (eudoria-clean/src/pesource/NifModelReader.js)',
      role: 'the page-side derivation — cross-validated BIT-EXACTLY against the R61 frozen python oracle (m1_iter037_crosscheck.py); this reader derives everything from the NIF bytes',
    },
    source: { entryName: sourceName },
    header: {
      text: headerText,
      versionRaw: `0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`,
      versionString: '10.1.0.0',
      userVersion, numBlocks,
      blockTypes, blockTypeIndex, numGroups, groups,
      dataStartOffset,
    },
    blocks: [],
    fileTailBytesHex: null,
    fileTailBytesLen: null,
  };

  for (let blockIndex = 0; blockIndex < numBlocks; blockIndex++) {
    const preambleOffset = s.pos;
    const preambleU32 = s.u32();
    if (preambleU32 !== 0) {
      throw new Error(`[NifModelReader] block ${blockIndex}: non-zero preamble u32=${preambleU32} @${preambleOffset} — parser desynchronization, LOUD FAIL`);
    }
    const typeIdx = blockTypeIndex[blockIndex];
    const type = blockTypes[typeIdx];
    if (!type || !KNOWN_V10_TYPES.has(type)) {
      throw new Error(`[NifModelReader] block ${blockIndex}: UNKNOWN type "${type}" (index ${typeIdx}) — no parser registered (LOUD FAIL; the ORACLE fails closed here too)`);
    }
    const payloadStart = s.pos;
    let fields;
    switch (type) {
      case 'NiNode': fields = parseNiNode(s); break;
      case 'NiArkAnimationExtraData': fields = parseNiArkAnimationExtraData(s); break;
      case 'NiArkImporterExtraData': fields = parseNiArkImporterExtraData(s); break;
      case 'NiArkTextureExtraData': fields = parseNiArkTextureExtraData(s, extraction); break;
      case 'NiTexturingProperty': fields = parseNiTexturingProperty(s); break;
      case 'NiArkViewportInfoExtraData': fields = parseNiArkViewportInfoExtraData(s, extraction); break;
      case 'NiMaterialProperty': fields = parseNiMaterialProperty(s); break;
      case 'NiZBufferProperty': fields = parseNiZBufferProperty(s); break;
      case 'NiVertexColorProperty': fields = parseNiVertexColorProperty(s); break;
      case 'NiArkShaderExtraData': fields = parseNiArkShaderExtraData(s); break;
      case 'NiStringExtraData': fields = parseNiStringExtraData(s); break;
      case 'NiTriShape': fields = parseNiTriShape(s); break;
      case 'NiAlphaProperty': fields = parseNiAlphaProperty(s); break;
      case 'NiTriShapeData': fields = parseNiTriShapeData(s); break;
      default: throw new Error(`[NifModelReader] block ${blockIndex}: type ${type} known-listed but unimplemented — LOUD FAIL`);
    }
    extraction.blocks.push({
      index: blockIndex, type,
      preambleOffset, preambleU32,
      payloadStart, blockEnd: s.pos,
      fields,
    });
  }

  // ---- the file tail (bytes after the last block; recorded raw, semantics UNKNOWN) ----
  const tailLen = s.size - s.pos;
  let tailHex = '';
  for (let i = 0; i < tailLen; i++) tailHex += payload[s.pos + i].toString(16).padStart(2, '0');
  extraction.fileTailBytesHex = tailHex;
  extraction.fileTailBytesLen = tailLen;

  // ---- the render model (derived from the parsed blocks; loud if the chain is absent) ----
  const renderModel = buildRenderModel(extraction);
  return { extraction, renderModel };
}

/** Derive the render-ready structure from the canonical extraction:
 * the NiTriShape chain (shape -> data) + the NiTexturingProperty BASE slot +
 * the Ark texture binding + the alpha/material properties. Loud on any
 * missing chain link (NO fallback). */
function buildRenderModel(extraction) {
  const byType = (t, n = 1) => extraction.blocks.filter(b => b.type === t).slice(0, n);
  const shape = byType('NiTriShape')[0];
  const data = byType('NiTriShapeData')[0];
  const texprop = byType('NiTexturingProperty')[0];
  const arkTex = byType('NiArkTextureExtraData')[0];
  const material = byType('NiMaterialProperty')[0];
  const alpha = byType('NiAlphaProperty')[0];
  if (!shape || !data || !texprop || !arkTex) {
    throw new Error('[NifModelReader] witness chain incomplete (NiTriShape/NiTriShapeData/NiTexturingProperty/NiArkTextureExtraData) — LOUD FAIL');
  }
  if (shape.fields.dataRef !== data.index) {
    throw new Error(`[NifModelReader] NiTriShape dataRef ${shape.fields.dataRef} != the NiTriShapeData block ${data.index} — LOUD FAIL`);
  }
  const slot0 = texprop.fields.textures[0];
  if (!slot0 || slot0.has !== 1) {
    throw new Error('[NifModelReader] NiTexturingProperty slot 0 (BASE) missing — LOUD FAIL');
  }
  const arkEntry = arkTex.fields.entries.find(e => e.ref === texprop.index);
  if (!arkEntry) {
    throw new Error(`[NifModelReader] no NiArkTextureExtraData entry references the NiTexturingProperty block ${texprop.index} — LOUD FAIL`);
  }
  const bitsToF32 = (hex) => {
    // FILE-ORDER byte hex -> u32 (little-endian) -> f32 (the struct.pack parity)
    const u = new Uint32Array(1);
    const b = new Uint8Array(u.buffer);
    for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
    return new Float32Array(u.buffer)[0];
  };
  const bitsToArray = (bits, stride) => {
    const out = new Float32Array(bits.length);
    for (let i = 0; i < bits.length; i++) out[i] = bitsToF32(bits[i]);
    return out;
  };
  const n = data.fields.numVertices;
  const positions = bitsToArray(data.fields.verticesBits);
  const normals = data.fields.hasNormals ? bitsToArray(data.fields.normalsBits) : null;
  const colors = data.fields.hasVertexColors ? bitsToArray(data.fields.vertexColorsBits) : null;
  const uvSets = data.fields.uvSetsBits.map(bits => bitsToArray(bits));
  const index = new Uint16Array(data.fields.triangles.length * 3);
  data.fields.triangles.forEach((t, i) => { index[i * 3] = t[0]; index[i * 3 + 1] = t[1]; index[i * 3 + 2] = t[2]; });
  return {
    shapeName: shape.fields.name,
    shapeIndex: shape.index,
    dataIndex: data.index,
    texpropIndex: texprop.index,
    dataRef: shape.fields.dataRef,
    numVertices: n,
    numTriangles: data.fields.numTriangles,
    positions, normals, colors, uvSets, index,
    center: data.fields.center.map(bitsToF32),
    radius: bitsToF32(data.fields.radius),
    textureBinding: {
      arkEntryName: arkEntry.name,
      slotType: arkEntry.f1,          // 0 = BASE (canon)
      textureId: arkEntry.textureId,  // the era Textures.bnt entry id (the Ark binding)
      texpropRef: arkEntry.ref,
      baseSlot: {
        has: slot0.has, source: slot0.source, clamp: slot0.clamp,
        filter: slot0.filter, uvSet: slot0.uv_set,
        transformPresent: slot0.transform_present,
        note: 'source=-1 (NULL) is the ERA BINDING: the texture comes from the NiArkTextureExtraData id, NOT a NiSourceTexture block',
      },
    },
    material: material ? {
      name: material.fields.name,
      ambient: material.fields.ambient.map(bitsToF32),
      diffuse: material.fields.diffuse.map(bitsToF32),
      specular: material.fields.specular.map(bitsToF32),
      emissive: material.fields.emissive.map(bitsToF32),
      glossiness: bitsToF32(material.fields.glossiness),
      alpha: bitsToF32(material.fields.alpha),
    } : null,
    alpha: alpha ? { flags: alpha.fields.alphaFlags, threshold: alpha.fields.alphaThreshold } : null,
    shapeFlags: shape.fields.flags,
    shapeTransform: {
      translation: shape.fields.translation.map(bitsToF32),
      rotation: shape.fields.rotation.map(r => r.map(bitsToF32)),
      scale: bitsToF32(shape.fields.scale),
    },
  };
}
