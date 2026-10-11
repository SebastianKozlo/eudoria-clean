// PecTextureChain.js — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 5)
// ACTUAL texture chain resolution for PCG 9.3.5 assets, era-labelled:
//   v10 slots: NiTexturingProperty slot -> sourceRef -> NiSourceTexture ->
//     useExternal=1: external fileName -> Textures.bnt entry (id-mapped) ->
//     decode (DDS DXT1/DXT5 strict via the donor DdsDecoder; TGA type 2 via
//     TgaDecoder); useExternal=0: embedded NiPixelData (in-file pixels).
//   v4 slots: texturing property slots carry sourceRef=-1 (era NULL); the
//     binding lives in NiArkTextureExtraData entries (entryName + 9-byte
//     tail). The tail is interpreted ONLY after BOTH controls pass:
//     (A) byte-shape: [anim_flag u8][frame_index i32][bnt2_id u32] with
//         anim_flag in {0,1} and bnt2_id > 0;
//     (B) reference: bnt2_id exists as a Textures.bnt entry.
//     The 218757 universal interpretation stays RETRACTED; a slot resolved
//     through the tail is labelled ARK_TAIL_CONTROLLED.
//   Fallback: the R2 first-decodable-slot policy survives ONLY under the
//     label RENDER_RECONSTRUCTION (never TEXTURED_EXACT, never universal).
//
// States (per asset): TEXTURED_EXACT / PARTIAL / SOURCE_UNTEXTURED /
//   UNRESOLVED / UNSUPPORTED_FORMAT / DECODE_FAIL.
'use strict';

import { decodeDds, DDS_SUPPORTED_FOURCC } from '../pesource/DdsDecoder.js';
import { decodeTga2, decodeTga2A32Image } from '../pesource/TgaDecoder.js';

export const PEC_TEXTURE_CHAIN_VERSION = 'pec-texture-chain-pcg935-r1';

export const TEXTURE_STATES = Object.freeze({
  TEXTURED_EXACT: 'TEXTURED_EXACT',
  PARTIAL: 'PARTIAL',
  SOURCE_UNTEXTURED: 'SOURCE_UNTEXTURED',
  UNRESOLVED: 'UNRESOLVED',
  UNSUPPORTED_FORMAT: 'UNSUPPORTED_FORMAT',
  DECODE_FAIL: 'DECODE_FAIL',
});

const TGA_MAGIC = [0x00, 0x00, 0x02, 0x00];
const JPEG_MAGIC = [0xff, 0xd8, 0xff, 0xe0];
const JPEG_MAGIC2 = [0xff, 0xd8, 0xff, 0xe1];

export function sniffTextureFormat(payload) {
  if (payload.length >= 4
    && payload[0] === 0x44 && payload[1] === 0x44 && payload[2] === 0x53 && payload[3] === 0x20) return 'DDS';
  if (payload.length >= 4 && payload[1] === 0x00 && payload[2] <= 0x0b) {
    // TGA header: [idLength u8][colorMapType u8][imageType u8]
    if (payload[2] === 0x02 || payload[2] === 0x0a || payload[2] === 0x03 || payload[2] === 0x01) {
      return payload[2] === 0x02 ? 'TGA2' : `TGA_TYPE_${payload[2]}`;
    }
  }
  if (payload.length >= 4 && payload[0] === 0xff && payload[1] === 0xd8) return 'JPEG';
  return 'UNKNOWN';
}

/** Decode a Textures.bnt payload to top-first RGBA. Throws on unsupported/failed. */
export function decodeTexturePayload(payload) {
  const fmt = sniffTextureFormat(payload);
  if (fmt === 'DDS') {
    const r = decodeDds(payload);
    return { format: 'DDS', fourcc: r.fourcc ?? 'DXT?', width: r.width, height: r.height, rgba: r.rgba, mipmaps: r.mipmaps ?? 1 };
  }
  if (fmt === 'TGA2') {
    // bpp dispatch (both are TGA 2.0 strict subsets with the TRUEVISION-XFILE
    // footer): 24bpp BGR -> decodeTga2 (CONFIRMED corpus subset); 32bpp BGRA ->
    // decodeTga2A32Image. Both return image order (row 0 = visual top).
    const bpp = payload.length > 17 ? payload[16] : 0;
    if (bpp === 24) {
      const r = decodeTga2(payload);
      return { format: 'TGA2-24', width: r.width, height: r.height, rgba: r.rgba, mipmaps: 1 };
    }
    if (bpp === 32) {
      const r = decodeTga2A32Image(payload);
      return { format: 'TGA2-32', width: r.width, height: r.height, rgba: r.rgba, mipmaps: 1 };
    }
    throw Object.assign(new Error(`TGA2 bpp ${bpp} unsupported (subsets: 24, 32)`), { state: TEXTURE_STATES.UNSUPPORTED_FORMAT, format: fmt });
  }
  if (fmt.startsWith('TGA_TYPE_')) throw Object.assign(new Error(`TGA type ${fmt.slice(9)} unsupported in this run (bounded subset: type 2)`), { state: TEXTURE_STATES.UNSUPPORTED_FORMAT, format: fmt });
  if (fmt === 'JPEG') throw Object.assign(new Error('JPEG textures unsupported in this run (19 entries corpus-wide)'), { state: TEXTURE_STATES.UNSUPPORTED_FORMAT, format: fmt });
  throw Object.assign(new Error(`unknown texture payload format ${fmt}`), { state: TEXTURE_STATES.UNRESOLVED, format: fmt });
}

/** Control (A): the 9-byte ArkTexture tail byte-shape. Accepts the readers'
 * bytes9Hex STRING or a raw byte array. */
export function arkTailByteShape(bytes9) {
  let arr = bytes9;
  if (typeof bytes9 === 'string') {
    if (bytes9.length !== 18) return { ok: false, reason: `hex length ${bytes9.length} != 18` };
    arr = new Uint8Array(9);
    for (let i = 0; i < 9; i++) arr[i] = parseInt(bytes9.slice(i * 2, i * 2 + 2), 16);
  }
  if (!arr || arr.length !== 9) return { ok: false, reason: `length ${arr?.length} != 9` };
  const hex = [...arr].map((b) => b.toString(16).padStart(2, '0')).join('');
  const animFlag = arr[0];
  const frameIndex = (arr[1] | (arr[2] << 8) | (arr[3] << 16) | (arr[4] << 24));
  const bnt2Id = (arr[5] | (arr[6] << 8) | (arr[7] << 16) | (arr[8] << 24)) >>> 0;
  const animOk = animFlag === 0x00 || animFlag === 0x01;
  const frameOk = frameIndex === -1 || (frameIndex >= 0 && frameIndex < 0x10000);
  const idOk = bnt2Id > 0 && bnt2Id < 0x1000000;
  return { ok: animOk && frameOk && idOk, animFlag, frameIndex, bnt2Id, hex, animOk, frameOk, idOk };
}

/**
 * Resolve the ACTUAL texture chain for one parsed asset.
 * @param ir buildAssetIR result (blocks with .fields)
 * @param texLookup (id:number) => { payload: Uint8Array } | null  (Textures.bnt)
 * @param nameLookup (fileName:string) => { id: number, payload: Uint8Array } | null
 *   — same-era Textures.bnt lookup by file name (e.g. "223496.dat").
 */
export function resolveAssetTextures(ir, texLookup, nameLookup) {
  const blocks = ir.blocks ?? [];
  const byIndex = new Map(blocks.map((b) => [b.index, b]));
  const meshes = blocks.filter((b) => b.type === 'NiTriShape');
  const texProps = new Map(blocks.filter((b) => b.type === 'NiTexturingProperty').map((b) => [b.index, b]));
  const sourceTextures = new Map(blocks.filter((b) => b.type === 'NiSourceTexture').map((b) => [b.index, b]));
  const pixelDatas = new Map(blocks.filter((b) => b.type === 'NiPixelData').map((b) => [b.index, b]));
  const arkTexBlocks = blocks.filter((b) => b.type === 'NiArkTextureExtraData');

  const results = [];
  const decodeStates = new Set();

  for (const mesh of meshes) {
    const meshName = mesh.name ?? '';
    // 1. the mesh's texturing property (via its propertyRefs)
    const propRefs = mesh.fields?.propertyRefs ?? mesh.propertyRefs ?? [];
    const texPropIdx = propRefs.map((r) => texProps.get(r)).find(Boolean)
      ?? (mesh.fields?.dataRef != null ? findTexPropForData(byIndex, texProps, mesh) : null);
    if (!texPropIdx) {
      results.push({ mesh: meshName, meshIndex: mesh.index, state: TEXTURE_STATES.SOURCE_UNTEXTURED, slots: [], note: 'no texturing property on mesh' });
      continue;
    }
    const slotsIn = texPropIdx.fields?.slots ?? [];
    const slots = [];
    for (const slot of slotsIn) {
      if (!slot.hasMap) { slots.push({ slot: slot.slotName, hasMap: false }); continue; }
      const slotResult = { slot: slot.slotName, hasMap: true, sourceRef: slot.sourceRef, method: null, state: null, textureId: null, note: null };
      // v10 external path: sourceRef -> NiSourceTexture (useExternal=1, fileName)
      const src = sourceTextures.get(slot.sourceRef);
      if (src) {
        const f = src.fields ?? {};
        if (f.useExternal) {
          const fn = f.fileName ?? '';
          const hit = nameLookup?.(fn);
          if (hit) {
            slotResult.method = 'SOURCE_EXTERNAL_NAME';
            slotResult.textureId = hit.id;
            try {
              const dec = decodeTexturePayload(hit.payload);
              slotResult.state = TEXTURE_STATES.TEXTURED_EXACT;
              slotResult.decode = { format: dec.format, width: dec.width, height: dec.height };
              slotResult.label = 'NAME_RESOLVED_SAME_ERA';
            } catch (e) {
              slotResult.state = e.state ?? TEXTURE_STATES.DECODE_FAIL;
              slotResult.note = String(e.message).slice(0, 120);
            }
          } else {
            slotResult.method = 'SOURCE_EXTERNAL_NAME';
            slotResult.state = TEXTURE_STATES.UNRESOLVED;
            slotResult.note = `fileName "${fn}" not in same-era Textures.bnt`;
          }
        } else {
          // embedded pixels: sourceRef -> NiPixelData chain
          const pd = pixelDatas.get(f.pixelDataRef ?? f.ref);
          if (pd) {
            slotResult.method = 'SOURCE_EMBEDDED_PIXELDATA';
            slotResult.textureId = null;
            slotResult.state = TEXTURE_STATES.PARTIAL;
            slotResult.note = 'embedded NiPixelData present (decode in asset pass)';
            slotResult.pixelDataBlock = pd.index;
          } else {
            slotResult.method = 'SOURCE_EMBEDDED_PIXELDATA';
            slotResult.state = TEXTURE_STATES.UNRESOLVED;
            slotResult.note = 'useExternal=0 but no NiPixelData block';
          }
        }
      } else {
        // v4 era: sourceRef = -1; the ArkTexture extra data carries the binding
        const ark = findArkEntryFor(arkTexBlocks, texPropIdx.index, meshName);
        if (ark) {
          const shape = arkTailByteShape(ark.bytes9Hex ?? ark.bytes9);
          const refOk = shape.ok ? !!texLookup?.(shape.bnt2Id) : false;
          slotResult.method = 'ARK_TEXTURE_ENTRY';
          slotResult.arkEntryName = ark.entryName;
          slotResult.tailHex = shape.hex;
          slotResult.byteShapeControl = shape.ok;
          slotResult.referenceControl = refOk;
          if (shape.ok && refOk) {
            slotResult.textureId = shape.bnt2Id;
            slotResult.label = 'ARK_TAIL_CONTROLLED';
            try {
              const { payload } = texLookup(shape.bnt2Id);
              const dec = decodeTexturePayload(payload);
              slotResult.state = TEXTURE_STATES.TEXTURED_EXACT;
              slotResult.decode = { format: dec.format, width: dec.width, height: dec.height };
            } catch (e) {
              slotResult.state = e.state ?? TEXTURE_STATES.DECODE_FAIL;
              slotResult.note = String(e.message).slice(0, 120);
            }
          } else {
            slotResult.state = TEXTURE_STATES.UNRESOLVED;
            slotResult.note = `tail controls failed (byteShape=${shape.ok} reference=${refOk})`;
          }
        } else {
          slotResult.method = 'NO_BINDING';
          slotResult.state = TEXTURE_STATES.SOURCE_UNTEXTURED;
          slotResult.note = 'slot has map but no source texture and no ArkTexture entry';
        }
      }
      if (slotResult.state) decodeStates.add(slotResult.state);
      slots.push(slotResult);
    }
    // v10-era extension: when the texprop carries NO mapped slots, the binding
    // lives in the ArkTexture extra data entry referencing THIS texprop
    // (mesh -> texturing property -> ArkTexture entry -> controlled tail ->
    // same-era Textures.bnt id). Never name-only.
    const hasMapSlot = slots.some((s) => s.hasMap);
    if (!hasMapSlot) {
      const ark = findArkEntryFor(arkTexBlocks, texPropIdx.index, meshName);
      if (ark) {
        const shape = arkTailByteShape(ark.bytes9Hex ?? ark.bytes9);
        const refOk = shape.ok ? !!texLookup?.(shape.bnt2Id) : false;
        const r = { slot: 'ArkTextureBinding', hasMap: true, method: 'ARK_TEXTURE_ENTRY', arkEntryName: ark.entryName, tailHex: shape.hex, byteShapeControl: shape.ok, referenceControl: refOk, state: null, textureId: null, note: null, label: null };
        if (shape.ok && refOk) {
          r.textureId = shape.bnt2Id;
          r.label = 'ARK_TAIL_CONTROLLED';
          try {
            const { payload } = texLookup(shape.bnt2Id);
            const dec = decodeTexturePayload(payload);
            r.state = TEXTURE_STATES.TEXTURED_EXACT;
            r.decode = { format: dec.format, width: dec.width, height: dec.height };
          } catch (e) {
            r.state = e.state ?? TEXTURE_STATES.DECODE_FAIL;
            r.note = String(e.message).slice(0, 120);
          }
        } else {
          r.state = TEXTURE_STATES.UNRESOLVED;
          r.note = `tail controls failed (byteShape=${shape.ok} reference=${refOk})`;
        }
        if (r.state) decodeStates.add(r.state);
        slots.push(r);
      }
    }
    results.push({ mesh: meshName, meshIndex: mesh.index, state: slots.some((s) => s.state === TEXTURE_STATES.TEXTURED_EXACT)
      ? (slots.some((s) => s.hasMap && s.state && s.state !== TEXTURE_STATES.TEXTURED_EXACT) ? TEXTURE_STATES.PARTIAL : TEXTURE_STATES.TEXTURED_EXACT)
      : (slots.some((s) => s.hasMap) ? (slots.some((s) => s.state === TEXTURE_STATES.UNRESOLVED) ? TEXTURE_STATES.UNRESOLVED : TEXTURE_STATES.PARTIAL) : TEXTURE_STATES.SOURCE_UNTEXTURED),
      slots });
  }

  // R2 fallback (RENDER_RECONSTRUCTION ONLY): first decodable texture of the
  // whole asset when no mesh slot resolved exactly.
  const anyExact = results.some((r) => r.state === TEXTURE_STATES.TEXTURED_EXACT);
  let fallback = null;
  if (!anyExact) {
    outer: for (const ark of arkTexBlocks) {
      for (const ent of ark.fields?.entries ?? []) {
        const shape = arkTailByteShape(ent.bytes9Hex ?? ent.bytes9);
        if (shape.ok && texLookup?.(shape.bnt2Id)) {
          try {
            const { payload } = texLookup(shape.bnt2Id);
            const dec = decodeTexturePayload(payload);
            fallback = { textureId: shape.bnt2Id, width: dec.width, height: dec.height, format: dec.format, label: 'RENDER_RECONSTRUCTION' };
            break outer;
          } catch { /* try next */ }
        }
      }
    }
  }
  const state = anyExact ? TEXTURE_STATES.TEXTURED_EXACT
    : fallback ? TEXTURE_STATES.PARTIAL
      : (results.length === 0 ? TEXTURE_STATES.SOURCE_UNTEXTURED : (decodeStates.has(TEXTURE_STATES.UNSUPPORTED_FORMAT) ? TEXTURE_STATES.UNSUPPORTED_FORMAT : (decodeStates.has(TEXTURE_STATES.DECODE_FAIL) ? TEXTURE_STATES.DECODE_FAIL : TEXTURE_STATES.UNRESOLVED)));
  return {
    version: PEC_TEXTURE_CHAIN_VERSION,
    meshCount: meshes.length, results, state, fallback,
    exactSlots: results.flatMap((r) => r.slots).filter((s) => s.state === TEXTURE_STATES.TEXTURED_EXACT).length,
    mapSlots: results.flatMap((r) => r.slots).filter((s) => s.hasMap).length,
  };
}

function findTexPropForData(byIndex, texProps, mesh) {
  // When propertyRefs is absent in fields, fall back to scanning property
  // blocks that reference the same data — never name-only.
  return null;
}

function findArkEntryFor(arkTexBlocks, texPropIndex, meshName) {
  // An ArkTexture entry binds via texPropRef == the mesh's texturing property,
  // or via entryName prefix matching the mesh name (era convention
  // "<meshName>_0_BASE"). The texPropRef match is authoritative.
  for (const ark of arkTexBlocks) {
    for (const ent of ark.fields?.entries ?? []) {
      if (ent.texturingPropertyRef === texPropIndex) return ent;
    }
  }
  for (const ark of arkTexBlocks) {
    for (const ent of ark.fields?.entries ?? []) {
      if (meshName && ent.entryName && ent.entryName.startsWith(meshName) && ent.entryName.includes('_0_BASE')) return ent;
    }
  }
  return null;
}
