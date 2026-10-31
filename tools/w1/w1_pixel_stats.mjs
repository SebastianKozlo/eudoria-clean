#!/usr/bin/env node
// w1_pixel_stats.mjs — machine pixel forensics of the baseline PNGs (this
// session has NO image input, so defects are qualified by MEASURED pixel
// statistics: grid periodicity, seam lines, blockiness, flatness).
// Read-only on the PNGs; writes PIXEL_STATS.json next to the report.
import { readFileSync, writeFileSync } from 'node:fs';
import zlib from 'node:zlib';
import path from 'node:path';

const DIR = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\\W1_TERRAIN_MATERIALS\\baseline';

function decodePng(buf) {
  // minimal PNG decoder: RGBA8 non-interlaced only (CDP screenshots qualify)
  if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('not PNG');
  let pos = 8, w = 0, h = 0, bitDepth = 0, colorType = 0, idat = [];
  while (pos < buf.length) {
    const len = buf.readUInt32BE(pos); const type = buf.toString('ascii', pos + 4, pos + 8);
    const data = buf.subarray(pos + 8, pos + 8 + len);
    if (type === 'IHDR') { w = data.readUInt32BE(0); h = data.readUInt32BE(4); bitDepth = data[8]; colorType = data[9]; }
    else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    pos += 12 + len;
  }
  if (bitDepth !== 8 || (colorType !== 6 && colorType !== 2)) throw new Error(`unsupported PNG: depth=${bitDepth} color=${colorType}`);
  const bpp = colorType === 6 ? 4 : 3;
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = w * bpp;
  const out = Buffer.alloc(h * stride);
  let inPos = 0;
  for (let y = 0; y < h; y++) {
    const filter = raw[inPos++];
    const row = raw.subarray(inPos, inPos + stride); inPos += stride;
    const prev = y > 0 ? out.subarray((y - 1) * stride, y * stride) : null;
    const cur = out.subarray(y * stride, (y + 1) * stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? cur[x - bpp] : 0, b = prev ? prev[x] : 0, c = (x >= bpp && prev) ? prev[x - bpp] : 0;
      let v = row[x];
      if (filter === 1) v += a; else if (filter === 2) v += b; else if (filter === 3) v += (a + b) >> 1;
      else if (filter === 4) { const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c); v += (pa <= pb && pa <= pc) ? a : (pb <= pc ? b : c); }
      cur[x] = v & 0xff;
    }
  }
  return { w, h, bpp, px: out };
}
const lum = (img, x, y) => { const i = (y * img.w + x) * img.bpp; return 0.299 * img.px[i] + 0.587 * img.px[i + 1] + 0.114 * img.px[i + 2]; };

function analyze(file) {
  const img = decodePng(readFileSync(path.join(DIR, file)));
  const { w, h } = img;
  // 1) per-row and per-col mean |gradient| — seam/grid spike detection
  const rowG = new Float64Array(h), colG = new Float64Array(w);
  let flat = 0, tot = 0;
  for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
    const g = Math.abs(lum(img, x + 1, y) - lum(img, x - 1, y)) + Math.abs(lum(img, x, y + 1) - lum(img, x, y - 1));
    rowG[y] += g; colG[x] += g;
    if (g === 0) flat++;
    tot++;
  }
  const norm = (a, n) => { const m = a.reduce((s, v) => s + v, 0) / n; const sd = Math.sqrt(a.reduce((s, v) => s + (v - m) ** 2, 0) / n); return { mean: +m.toFixed(2), sd: +sd.toFixed(2) }; };
  const spikes = (a, n, m, sd) => { const out = []; for (let i = 1; i < n - 1; i++) if (a[i] > m + 6 * sd) out.push(i); return out; };
  const rowStats = norm(rowG, h), colStats = norm(colG, w);
  const rowSpikes = spikes(rowG, h, rowStats.mean, rowStats.sd).slice(0, 40);
  const colSpikes = spikes(colG, w, colStats.mean, colStats.sd).slice(0, 40);
  // 2) periodicity (autocorrelation of colG) — periodic vertical structures (grid/cells)
  const periodicity = (a, n, maxLag) => {
    const m = a.reduce((s, v) => s + v, 0) / n; let best = { lag: 0, r: -1 };
    for (let lag = 4; lag < maxLag; lag++) {
      let s = 0; for (let i = 0; i < n - lag; i++) s += (a[i] - m) * (a[i + lag] - m);
      const r = s / (n - lag); if (r > best.r) best = { lag, r: +r.toFixed(0) };
    }
    return best;
  };
  // 3) color stats (fog/flatness/height-palette suspicion)
  let rSum = 0, gSum = 0, bSum = 0, lumMean = 0, lumSd = 0; const hist = new Array(256).fill(0);
  const lums = [];
  for (let y = 0; y < h; y += 2) for (let x = 0; x < w; x += 2) {
    const i = (y * w + x) * img.bpp; rSum += img.px[i]; gSum += img.px[i + 1]; bSum += img.px[i + 2];
    const l = 0.299 * img.px[i] + 0.587 * img.px[i + 1] + 0.114 * img.px[i + 2];
    lums.push(l); lumMean += l; hist[Math.min(255, l | 0)]++;
  }
  lumMean /= lums.length;
  for (const l of lums) lumSd += (l - lumMean) ** 2; lumSd = Math.sqrt(lumSd / lums.length);
  return {
    file, size: { w, h }, gradientRows: rowStats, gradientCols: colStats,
    rowSpikes, colSpikes,
    colPeriodicity: periodicity(colG, w, 160), rowPeriodicity: periodicity(rowG, h, 160),
    flatFrac: +(flat / tot).toFixed(4),
    color: { r: Math.round(rSum / lums.length), g: Math.round(gSum / lums.length), b: Math.round(bSum / lums.length) },
    lumMean: +lumMean.toFixed(1), lumSd: +lumSd.toFixed(1),
  };
}

const files = ['f0_world_ready.png', 'fa_ground_close_walk.png', 'fb_topdown_tiles.png', 'fc_low_horizon.png', 'fd_near_mid_far.png', 'fe1_teleport_far.png', 'fe2_return_home.png'];
const out = {};
for (const f of files) { try { out[f] = analyze(f); } catch (e) { out[f] = { error: String(e?.message ?? e) }; } }
writeFileSync(path.join(DIR, '..', 'PIXEL_STATS.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify(Object.fromEntries(files.map((f) => [f, out[f].error ? out[f] : {
  rowSD: out[f].gradientRows.sd, rowSpikes: out[f].rowSpikes.length, colSpikes: out[f].colSpikes.length,
  colPer: out[f].colPeriodicity, rowPer: out[f].rowPeriodicity, flat: out[f].flatFrac,
  rgb: [out[f].color.r, out[f].color.g, out[f].color.b], lumSD: out[f].lumSd,
}]))));
