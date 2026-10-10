// png_nontrivial.mjs — OWN bounded PNG non-triviality check (no external image
// library; node:zlib only). PE_CITY_ASSET_MAP_R1_20261010 PIXEL_RENDER gate.
// Verifies a screenshot PNG is a REAL rendered image and NOT a blank
// single-color page: PNG signature + IHDR parse + IDAT inflate + scanline
// unfilter (filters 0..4) + per-region unique-color census + luminance
// statistics. HONEST LABEL: this is a bounded pixel-content heuristic, not a
// perceptual/semantic render check.
import { inflateSync } from 'node:zlib';

export function analyzePng(buffer, { regions = {} } = {}) {
  const out = { signatureOk: false, chunks: [], dimensions: null, colorType: null, bitDepth: null, interlace: null, rows: null, stride: null, channels: null, decodeOk: false, stats: null, error: null };
  const SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (!buffer.subarray(0, 8).equals(SIG)) { out.error = 'PNG signature mismatch'; return out; }
  out.signatureOk = true;

  let off = 8;
  const idat = [];
  while (off + 8 <= buffer.length) {
    const len = buffer.readUInt32BE(off);
    const type = buffer.subarray(off + 4, off + 8).toString('ascii');
    const data = buffer.subarray(off + 8, off + 8 + len);
    out.chunks.push({ type, len });
    if (type === 'IHDR') {
      out.dimensions = { width: data.readUInt32BE(0), height: data.readUInt32BE(4) };
      out.bitDepth = data[8];
      out.colorType = data[9];
      out.interlace = data[12];
    } else if (type === 'IDAT') {
      idat.push(data);
    } else if (type === 'IEND') {
      break;
    }
    off += 12 + len;
  }
  if (!out.dimensions) { out.error = 'no IHDR'; return out; }
  if (out.bitDepth !== 8) { out.error = `unsupported bit depth ${out.bitDepth} (CHECK_PARTIAL: only file-size/IHDR verified)`; return out; }
  if (out.colorType !== 6 && out.colorType !== 2) { out.error = `unsupported color type ${out.colorType} (CHECK_PARTIAL)`; return out; }
  if (out.interlace !== 0) { out.error = `interlaced PNG unsupported (CHECK_PARTIAL)`; return out; }

  const { width, height } = out.dimensions;
  const channels = out.colorType === 6 ? 4 : 3;
  out.channels = channels;
  const stride = width * channels;
  out.stride = stride;
  out.rows = height;

  let raw;
  try {
    raw = inflateSync(Buffer.concat(idat));
  } catch (e) {
    out.error = `IDAT inflate failed: ${e.message}`;
    return out;
  }
  if (raw.length !== height * (stride + 1)) { out.error = `unfiltered length mismatch: ${raw.length} != ${height * (stride + 1)}`; return out; }

  // unfilter scanlines into a row-major RGB(A) image
  const img = Buffer.alloc(height * stride);
  const bpp = channels;
  let p = 0;
  for (let y = 0; y < height; y++) {
    const filter = raw[p++];
    const rowStart = y * stride;
    const prevStart = (y - 1) * stride;
    for (let x = 0; x < stride; x++) {
      const b = raw[p + x];
      const a = x >= bpp ? img[rowStart + x - bpp] : 0; // left (Sub)
      const c = y > 0 ? img[prevStart + x] : 0;          // up (Up)
      const d = y > 0 && x >= bpp ? img[prevStart + x - bpp] : 0; // up-left (Paeth)
      let v;
      switch (filter) {
        case 0: v = b; break;
        case 1: v = (b + a) & 0xff; break;
        case 2: v = (b + c) & 0xff; break;
        case 3: v = (b + ((a + c) >> 1)) & 0xff; break;
        case 4: {
          const pa = Math.abs(c - d), pb = Math.abs(a - d), pc = Math.abs(a + c - 2 * d);
          const pred = (pa <= pb && pa <= pc) ? a : (pb <= pc ? c : d);
          v = (b + pred) & 0xff; break;
        }
        default: out.error = `unknown filter ${filter} at row ${y}`; return out;
      }
      img[rowStart + x] = v;
    }
    p += stride;
  }
  out.decodeOk = true;

  // per-region statistics (bounded sampling: step so at most ~200k samples/region)
  const regionStats = (x0, y0, x1, y1) => {
    x0 = Math.max(0, Math.floor(x0)); y0 = Math.max(0, Math.floor(y0));
    x1 = Math.min(width, Math.ceil(x1)); y1 = Math.min(height, Math.ceil(y1));
    const px = Math.max(1, x1 - x0), py = Math.max(1, y1 - y0);
    const total = px * py;
    const step = Math.max(1, Math.floor(Math.sqrt(total / 200000)));
    const colors = new Map();
    let n = 0, sumL = 0, sumL2 = 0, minL = 255, maxL = 0, alphaNon255 = 0;
    for (let y = y0; y < y1; y += step) {
      const row = y * stride;
      for (let x = x0; x < x1; x += step) {
        const i = row + x * channels;
        const r = img[i], g = img[i + 1], b = img[i + 2];
        const a = channels === 4 ? img[i + 3] : 255;
        if (a !== 255) alphaNon255++;
        const key = (r << 16) | (g << 8) | b;
        colors.set(key, (colors.get(key) ?? 0) + 1);
        const l = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        sumL += l; sumL2 += l * l;
        if (l < minL) minL = l;
        if (l > maxL) maxL = l;
        n++;
      }
    }
    let mostCommon = 0;
    for (const c of colors.values()) if (c > mostCommon) mostCommon = c;
    const mean = n ? sumL / n : 0;
    const std = n ? Math.sqrt(Math.max(0, sumL2 / n - mean * mean)) : 0;
    return {
      region: [x0, y0, x1, y1], samples: n, uniqueColors: colors.size,
      mostCommonColorFraction: n ? mostCommon / n : null,
      lumaMean: Math.round(mean * 100) / 100, lumaStdDev: Math.round(std * 100) / 100,
      lumaMin: Math.round(minL), lumaMax: Math.round(maxL),
      alphaNon255Fraction: n ? alphaNon255 / n : null,
    };
  };

  out.stats = { full: regionStats(0, 0, width, height) };
  for (const [name, [x0, y0, x1, y1]] of Object.entries(regions)) {
    out.stats[name] = regionStats(x0, y0, x1, y1);
  }
  return out;
}
