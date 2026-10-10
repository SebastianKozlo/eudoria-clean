// DdsDecoder.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §6.6)
// THE STRICT DDS subset decoder for the TWO real same-era texture formats the
// vegetation/model chains actually encounter (measured on the REAL inputs of
// this run — see docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010):
//   - DDS DXT1 (fourcc "DXT1"): witnesses 518860.dat, 518862.dat (256x256),
//     516807.dat (128x128) — the BASE slots of the Asset Lab witness 519316;
//   - DDS DXT5 (fourcc "DXT5"): witness 166881.dat (256x256) — the texture of
//     the profile-0 models 166878/166897 (the two R1-untextured trees).
//
// SCOPE (STRICT — anything outside fails LOUDLY; a refusal is the honest
// UNSUPPORTED status, never a fallback texture):
//   - magic "DDS " + dwSize==124 + pixel-format flags DDSPF_FOURCC (0x4);
//   - fourcc EXACTLY "DXT1" or "DXT5" (DXT2/3/4, ATI*, uncompressed and every
//     other variant are REFUSED — not silently reinterpreted);
//   - the TOP-LEVEL mip ONLY (any additional chained mips stay UNREAD in the
//     payload — documented; the chain is not silently decoded);
//   - dimensions are decoded with standard edge-block clamping (any width/
//     height >= 1; the block grid is ceil(w/4) x ceil(h/4)).
//
// PROVENANCE: the decompression arithmetic is the PUBLIC documented S3TC
// block scheme (color565 endpoints + the 4-point interpolant rows; DXT5 the
// 8-point alpha interpolant with the two 3-bit endpoints + 16x2-bit codes).
// It contains NO SDK source and NO game bytes; it is a decoder of the REAL
// payloads served through the pinned same-era Textures.bnt chain.
'use strict';

export const DDS_DECODER_VERSION = 'dds-dxt-strict-v1';
export const DDS_SUPPORTED_FOURCC = Object.freeze(['DXT1', 'DXT5']);

const DDS_MAGIC = 0x20534444; // "DDS "
const DDSD_WIDTH = 0x4, DDSD_HEIGHT = 0x2, DDSD_MIPMAPCOUNT = 0x20000;
const DDSPF_FOURCC = 0x4;

function loud(msg) {
  throw new Error(`[DdsDecoder] ${msg}`);
}

function decodeColorTable(u16) {
  // color565 -> [r,g,b] full-range (the standard 5/6/5 expansion)
  const r5 = (u16 >> 11) & 0x1f, g6 = (u16 >> 5) & 0x3f, b5 = u16 & 0x1f;
  return [(r5 << 3) | (r5 >> 2), (g6 << 2) | (g6 >> 4), (b5 << 3) | (b5 >> 2)];
}

/** Strict header gate + the ONE supported payload family. Returns the decoded
 * RGBA (Uint8Array, RGBA byte order, row 0 = FIRST stored row) — identical
 * output contract to decodeTga2/decodeTga2A32Image (top-first RGBA). */
export function decodeDds(payload) {
  if (!(payload instanceof Uint8Array) || payload.length < 128) {
    loud(`payload too small for a DDS header (${payload?.length ?? payload} B; the strict subset requires >= 128 B)`);
  }
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const magic = dv.getUint32(0, true);
  if (magic !== DDS_MAGIC) loud(`magic 0x${magic.toString(16)} is not "DDS " (the strict DDS subset refuses anything else)`);
  const size = dv.getUint32(4, true);
  if (size !== 124) loud(`dwSize ${size} != 124 (the strict subset serves the standard DDS header only)`);
  const flags = dv.getUint32(8, true);
  if (!(flags & DDSD_HEIGHT) || !(flags & DDSD_WIDTH)) {
    loud(`dwFlags 0x${flags.toString(16)} misses DDSD_HEIGHT/DDSD_WIDTH (the strict subset refuses)`);
  }
  const height = dv.getUint32(12, true);
  const width = dv.getUint32(16, true);
  if (height === 0 || width === 0) loud(`dimensions ${width}x${height} invalid (zero)`);
  if (height > 4096 || width > 4096) loud(`dimensions ${width}x${height} beyond the bounded subset (<= 4096)`);
  const pfFlags = dv.getUint32(80, true); // DDSPIXELFORMAT { dwSize@76, dwFlags@80, dwFourCC@84 }
  if (!(pfFlags & DDSPF_FOURCC)) loud(`pixel-format flags 0x${pfFlags.toString(16)} lack DDSPF_FOURCC (uncompressed/other DDS variants are NOT the strict subset)`);
  const fourcc = String.fromCharCode(payload[84], payload[85], payload[86], payload[87]);
  if (!DDS_SUPPORTED_FOURCC.includes(fourcc)) {
    loud(`fourcc ${JSON.stringify(fourcc)} outside the strict subset ${JSON.stringify([...DDS_SUPPORTED_FOURCC])} (the payload fails LOUDLY — honest UNSUPPORTED, never a fallback texture)`);
  }
  const mipmaps = (flags & DDSD_MIPMAPCOUNT) ? dv.getUint32(28, true) : 1;
  const blockBytes = fourcc === 'DXT1' ? 8 : 16;
  const blocksX = Math.ceil(width / 4), blocksY = Math.ceil(height / 4);
  const topBytes = blocksX * blocksY * blockBytes;
  const dataStart = 128; // pfSize(4)+pfFlags(4)+fourcc(4)+bitcount(4)+rmask... header ends at 128
  if (payload.length < dataStart + topBytes) {
    loud(`payload ${payload.length} B too small for the top-level ${fourcc} image (${topBytes} B needed after the 128 B header — truncated input refused)`);
  }
  const rgba = new Uint8Array(width * height * 4);
  let o = dataStart;
  for (let by = 0; by < blocksY; by++) {
    for (let bx = 0; bx < blocksX; bx++, o += blockBytes) {
      // ---- the alpha plane (DXT5 only; DXT1 carries 1-bit alpha == opaque) ----
      let alphas = null;
      if (fourcc === 'DXT5') {
        const a0 = payload[o], a1 = payload[o + 1];
        const codes = new Uint8Array(16);
        for (let i = 0; i < 16; i++) {
          const byte = payload[o + 2 + (i >> 2)];
          const shift = (i & 3) * 2;
          const code = (byte >> shift) & 3;
          // the standard 8-point interpolant (a0 > a1) vs the 6+2 form (a0 <= a1)
          if (a0 > a1) {
            codes[i] = code === 0 ? a0 : code === 1 ? a1
              : Math.round(a0 + ((a1 - a0) * (code - 1)) / 5) & 0xff;
          } else {
            codes[i] = code === 0 ? a0 : code === 1 ? a1
              : code === 6 ? 0 : code === 7 ? 255
                : Math.round(a0 + ((a1 - a0) * (code - 1)) / 4) & 0xff;
          }
        }
        alphas = codes;
      }
      // ---- the color plane ----
      const cOff = fourcc === 'DXT5' ? o + 8 : o;
      const c0 = dv.getUint16(cOff, true), c1 = dv.getUint16(cOff + 2, true);
      const [r0, g0, b0] = decodeColorTable(c0);
      const [r1, g1, b1] = decodeColorTable(c1);
      let rows;
      if (fourcc === 'DXT1' && c0 <= c1) {
        // the 3-color form (one transparent code — decoded with alpha 0)
        rows = [
          [r0, g0, b0, 255], [r1, g1, b1, 255],
          [Math.round((r0 + r1) / 2), Math.round((g0 + g1) / 2), Math.round((b0 + b1) / 2), 255],
          [0, 0, 0, 0],
        ];
      } else {
        rows = [
          [r0, g0, b0, 255], [r1, g1, b1, 255],
          [Math.round((2 * r0 + r1) / 3), Math.round((2 * g0 + g1) / 3), Math.round((2 * b0 + b1) / 3), 255],
          [Math.round((r0 + 2 * r1) / 3), Math.round((g0 + 2 * g1) / 3), Math.round((b0 + 2 * b1) / 3), 255],
        ];
      }
      for (let py = 0; py < 4; py++) {
        const codeBits = payload[cOff + 4 + py]; // 4 code BYTES total: one per row (4 px x 2 bits)
        for (let px = 0; px < 4; px++) {
          const x = bx * 4 + px, y = by * 4 + py;
          if (x >= width || y >= height) continue; // standard edge-block clamping
          const code = (codeBits >> (px * 2)) & 3;
          const row = rows[code];
          const i = (y * width + x) * 4;
          rgba[i] = row[0]; rgba[i + 1] = row[1]; rgba[i + 2] = row[2];
          rgba[i + 3] = alphas ? alphas[py * 4 + px] : row[3];
        }
      }
    }
  }
  return {
    fourcc, width, height,
    mipmapsDeclared: mipmaps,
    mipsDecoded: 1, // TOP-LEVEL ONLY — the chain stays unread in the payload (documented)
    bytesAfterTopMip: payload.length - dataStart - topBytes,
    rgba,
  };
}
