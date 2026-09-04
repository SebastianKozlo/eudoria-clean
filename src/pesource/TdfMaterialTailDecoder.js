// TdfMaterialTailDecoder.js — MILESTONE 1-E ITER 020 (CLEAN-PATH MATERIALS)
// FORMAT LAYER: TDF material-tail decoder for the CLEAN runtime (r185).
//
// CONFIRMED TAIL STRUCTURE (iter008/iter008b, corpus-proven 51,920/51,920
// exact consumption on JUL_2003 50.bnt; era-validated on PCG_9_3_5
// terrain.bnt in ITER 019 — 448,384 records / 0 failures):
//   TAIL starts at payload offset 2112 (payload-relative offset space).
//   Record = [u32 size][u32 dim][size-4 bytes]; stride = size+4; the size
//   field counts ALL bytes AFTER itself. Exact end-consumption is REQUIRED
//   (any residual byte = LOUD failure).
//   Record-relative layout (offsets from the size field):
//     size   @0      u32
//     dim    @4      u32
//     unk    @8      u32   (1 on named material records)
//     bps    @12     u32   (record-format enum: 2 = material-16; others UNVERIFIED)
//     id     @16     u32   material/texture resource id
//     res    @20     u32   (0 or 2)
//     name   @24..51 28 B  NUL-terminated material name
//     extra4 @52..55       (record char 32/pad region; UNVERIFIED)
//     mask   @56..size+3   dim*dim weights; RAW u8[dim^2] when the region
//                          length == dim^2, else RLE (count,value) u8 pairs
//                          summing EXACTLY dim^2 and consuming the region
//                          EXACTLY (16_rle_cv class; iter008 CONFIRMED).
//
// SEMANTICS CARRIED (iter009, corpus-proven — labels kept honest):
//   - Named dim=16 records are per-tile material layers.
//   - Stone04 full-coverage base rule: position-0 named record is the BASE
//     (all-255 mask in 99.45% of tiles); normalization (sum==255 partition)
//     is REJECTED — masks are INDEPENDENT per-layer weights; sums>255 are
//     ORIGINAL DATA and are tolerated, never renormalized.
//   - dim=2/4/8/32/256 records are SYSTEM records — carried RAW with
//     UNVERIFIED labels (roles per iter016 census), never interpreted.
//
// NO renderer semantics here. Loud failures only — no silent fallbacks.

export const MATERIAL_TAIL_START = 2112; // payload-relative (TDF payload offset space)

/**
 * Decode a mask region. dim=16 (named material records): RAW u8[dim^2] or
 * RLE (count,value) pairs — LOUD failure if neither. Other dims (system
 * records, iter016 census): the region is carried RAW with an honest label
 * (dim=4/8 regions are 2*dim^2 — u16-per-pixel structure, UNVERIFIED
 * semantics; dim=32 mostly RAW; dim=256 fine-grain candidates). System
 * record regions are NEVER interpreted here.
 */
export function decodeMaskRegion(region, dim) {
  const target = dim * dim;
  if (region.length === target) {
    return { mask: new Uint8Array(region), encoding: 'raw' };
  }
  if (region.length % 2 !== 0) {
    return { mask: null, encoding: `raw_region_${region.length}B`, regionLength: region.length };
  }
  const mask = new Uint8Array(target);
  let wp = 0, rp = 0, ok = true;
  while (rp < region.length) {
    const count = region[rp++];
    const value = region[rp++];
    if (wp + count > target) { ok = false; break; }
    mask.fill(value, wp, wp + count);
    wp += count;
  }
  if (ok && wp === target) return { mask, encoding: 'rle_cv' };
  return { mask: null, encoding: `raw_region_${region.length}B`, regionLength: region.length };
}

function readName(dv, base, off) {
  // 28-byte NUL-terminated field @ record+24
  const bytes = new Uint8Array(28);
  for (let i = 0; i < 28; i++) bytes[i] = dv.getUint8(off + i);
  let end = bytes.indexOf(0);
  if (end === -1) end = 28;
  let s = '';
  for (let i = 0; i < end; i++) {
    const c = bytes[i];
    s += (c >= 0x20 && c < 0x7f) ? String.fromCharCode(c) : `\u0000${c}`; // non-printables stay LOUD
  }
  return { name: s, printable: /^[\x20-\x7e]*$/.test(s) && s.length > 0, raw: bytes };
}

/**
 * Decode the full material tail of a TDF payload.
 * @param {Uint8Array} tail raw tail bytes (payload.subarray(2112))
 * @returns {{records: Array, namedMaterials: Array, systemRecords: Array, consumed: number}}
 *   namedMaterials: [{position, id, name, mask: Uint8Array(dim*dim), encoding,
 *                     unk, bps, res, size, dim, recordOffset (tail-relative)}]
 */
export function decodeMaterialTail(tail) {
  if (!(tail instanceof Uint8Array)) throw new Error('[TdfMaterialTail] tail must be Uint8Array');
  const dv = new DataView(tail.buffer, tail.byteOffset, tail.byteLength);
  const records = [];
  let p = 0;
  while (p < tail.byteLength) {
    const recordOffset = p;
    const remaining = tail.byteLength - p;
    if (remaining < 4) throw new Error(`[TdfMaterialTail] residual ${remaining}B at tail+${p} (< 4B size field)`);
    const size = dv.getUint32(p, true);
    if (size < 8 || size > remaining) {
      throw new Error(`[TdfMaterialTail] implausible size ${size} at tail+${p} (remaining ${remaining})`);
    }
    const dim = dv.getUint32(p + 4, true);
    const bodyStart = p + 8;                    // after size+dim
    const maskStart = p + 56;                  // record-relative mask @56
    const maskEnd = p + 4 + size;              // record consumes [p, p+4+size)
    if (maskEnd > tail.byteLength) {
      throw new Error(`[TdfMaterialTail] record overrun at tail+${p} (size ${size})`);
    }
    if (maskStart > maskEnd) {
      throw new Error(`[TdfMaterialTail] size ${size} too small for 52-byte pre-mask (dim=${dim})`);
    }
    const unk = dv.getUint32(p + 8, true);
    const bps = dv.getUint32(p + 12, true);
    const id = dv.getUint32(p + 16, true);
    const res = dv.getUint32(p + 20, true);
    const nameInfo = readName(dv, tail, p + 24);
    const region = tail.subarray(maskStart, maskEnd);
    const decoded = decodeMaskRegion(region, dim);
    if (dim === 16 && nameInfo.printable && nameInfo.name.length > 0 && decoded.mask === null) {
      // named material records must decode (RAW or RLE) — LOUD failure otherwise
      throw new Error(
        `[TdfMaterialTail] named dim=16 record "${nameInfo.name}" mask region not RAW/RLE (len ${region.length})`);
    }
    records.push({
      recordOffset,
      size, dim, unk, bps, id, res,
      name: nameInfo.name,
      namePrintable: nameInfo.printable,
      maskEncoding: decoded.encoding,
      mask: decoded.mask,          // Uint8Array(dim*dim) or null (system raw region)
      maskRegionLength: decoded.mask === null ? region.length : null,
      extra4: Array.from(tail.subarray(p + 52, p + 56)),
    });
    p = maskEnd; // stride = size + 4
  }
  const namedMaterials = records.filter((r) => r.dim === 16 && r.namePrintable && r.name.length > 0 && r.mask !== null);
  const systemRecords = records.filter((r) => !(r.dim === 16 && r.namePrintable && r.name.length > 0 && r.mask !== null));
  return { records, namedMaterials, systemRecords, consumed: p };
}

/** Per-pixel sum statistics across a tile's named 16x16 masks (audit aid). */
export function maskSumStats(namedMaterials) {
  const n = namedMaterials.length;
  if (n === 0) return null;
  const sums = new Uint32Array(256);
  for (const m of namedMaterials) {
    for (let i = 0; i < 256; i++) sums[i] += m.mask[i];
  }
  let min = 0xffffffff, max = 0, constSum = -1, exceeds255 = 0;
  for (let i = 0; i < 256; i++) {
    if (sums[i] < min) min = sums[i];
    if (sums[i] > max) max = sums[i];
    if (sums[i] > 255) exceeds255++;
  }
  constSum = (min === max) ? min : null;
  return { namedCount: n, min, max, constantSum: constSum, cellsExceeding255: exceeds255 };
}
