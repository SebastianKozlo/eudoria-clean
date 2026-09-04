// TgaDecoder.js — PE MILESTONE 1 ITER 012 (PE_WORLD_SURFACE_FIDELITY_R1)
// FORMAT LAYER: TGA 2.0 texture payload decoder for the terrain material
// textures resolved from the ORIGINAL era containers (Gate B).
//
// Evidence basis (iter011, corpus-wide for the 175 terrain material textures):
//   CONFIRMED: TGA 2.0 — classic 18-byte header + image data + 8 bytes of
//   u32 offsets (extension area offset + developer directory offset) + the
//   18-byte "TRUEVISION-XFILE.\0" signature block = a 26-byte TGA2 FOOTER;
//   256x256; 24bpp (BGR); uncompressed (imageType=2); bottom-up origin
//   (descriptor top-down bit = 0); constant payload size 196,652 bytes
//   (18 + 196,608 + 8 + 18) in BOTH era containers.
//
// This decoder supports EXACTLY that validated subset and throws loudly on
// anything else (no silent guessing, no partial fallbacks). Renderer-neutral:
// returns raw RGBA bytes; the caller decides what to do with them.

const TGA2_FOOTER = 'TRUEVISION-XFILE.\0';

/**
 * Decode a TGA 2.0 payload to RGBA.
 * @param {Uint8Array} payload — raw texture payload from the container entry.
 * @returns {{ width: number, height: number, rgba: Uint8Array, header: object, footerOk: boolean }}
 */
export function decodeTga2(payload) {
  if (!(payload instanceof Uint8Array)) throw new Error('[TgaDecoder] payload must be Uint8Array');
  const sz = payload.length;
  if (sz < 26 + 18) throw new Error(`[TgaDecoder] payload too small for TGA2 (${sz})`);

  const idLength = payload[0];
  const colorMapType = payload[1];
  const imageType = payload[2];
  const headerSize = 18 + idLength;
  const width = payload[12] | (payload[13] << 8);
  const height = payload[14] | (payload[15] << 8);
  const bpp = payload[16];
  const descriptor = payload[17];

  // Validated subset (iter011 CONFIRMED) — anything else fails LOUDLY.
  if (colorMapType !== 0) throw new Error(`[TgaDecoder] colorMapType ${colorMapType} unsupported (CONFIRMED subset: 0)`);
  if (imageType !== 2) throw new Error(`[TgaDecoder] imageType ${imageType} unsupported (CONFIRMED subset: 2 = uncompressed true-color)`);
  if (bpp !== 24) throw new Error(`[TgaDecoder] bpp ${bpp} unsupported (CONFIRMED subset: 24)`);
  if (width <= 0 || height <= 0) throw new Error(`[TgaDecoder] invalid dimensions ${width}x${height}`);

  const dataStart = headerSize;
  // TGA 2.0 footer = 8 bytes (extension-area u32 offset + developer-directory
  // u32 offset) + 18-byte signature block. iter011 CONFIRMED the signature at
  // the last 18 bytes; the 8 offset bytes sit immediately before it.
  const expected = 18 + idLength + width * height * (bpp / 8) + 8 + 18;
  if (sz !== expected) throw new Error(`[TgaDecoder] payload size ${sz} != expected TGA2 size ${expected}`);

  const footer = String.fromCharCode(...payload.subarray(sz - 18, sz));
  const footerOk = footer === TGA2_FOOTER;
  if (!footerOk) throw new Error('[TgaDecoder] TGA2 footer signature missing (TRUEVISION-XFILE.\\0)');
  const extAreaOffset = payload[sz - 26] | (payload[sz - 25] << 8) | (payload[sz - 24] << 16) | (payload[sz - 23] << 24);
  const devDirOffset = payload[sz - 22] | (payload[sz - 21] << 8) | (payload[sz - 20] << 16) | (payload[sz - 19] << 24);

  const topDown = (descriptor & 0x20) !== 0; // CONFIRMED corpus: always 0 (bottom-up)
  const bpr = width * 3;
  const rgba = new Uint8Array(width * height * 4);
  for (let y = 0; y < height; y++) {
    // bottom-up storage: file row 0 is the BOTTOM image row
    const srcRow = topDown ? y : height - 1 - y;
    const src = dataStart + srcRow * bpr;
    const dst = y * width * 4;
    for (let x = 0; x < width; x++) {
      const s = src + x * 3;
      const d = dst + x * 4;
      rgba[d] = payload[s + 2];     // R (stored BGR)
      rgba[d + 1] = payload[s + 1]; // G
      rgba[d + 2] = payload[s];     // B
      rgba[d + 3] = 255;            // A (opaque — 24bpp has no alpha)
    }
  }
  return {
    width, height, rgba,
    header: { idLength, colorMapType, imageType, width, height, bpp, descriptor, headerSize,
      tga2ExtensionAreaOffset: extAreaOffset, tga2DeveloperDirOffset: devDirOffset },
    footerOk,
  };
}
