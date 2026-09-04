// overview_probe.js — decode the 9.3.5 sentinel overview (237x237 u8) and
// correlate overview cells with per-tile u16 height stats.
'use strict';
const fs = require('fs');
const zlib = require('zlib');
const buf = fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt');
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const dirOffset = dv.getUint32(buf.length - 8, true);
const count = dv.getUint32(dirOffset, true);
const byName = new Map();
let p = dirOffset + 4;
for (let i = 0; i < count; i++) {
  const ns = p; while (buf[p] !== 0x0a) p++;
  const name = buf.toString('latin1', ns, p); p++;
  byName.set(name, { size: dv.getUint32(p, true), offset: dv.getUint32(p + 4, true) });
  p += 16;
}
function inflate(name) { const e = byName.get(name); return zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size)); }

// overview
const ov = inflate('7ffe7ffe.tdf');
const odv = new DataView(ov.buffer, ov.byteOffset, ov.byteLength);
console.log('overview payload:', ov.length, 'data_size:', odv.getUint32(8, true), 'dim:', odv.getUint32(12, true));
const DIM = odv.getUint32(12, true); // 237
const dataOff = 64;
const dataLen = DIM * DIM;
console.log('data region:', dataOff, '..', dataOff + dataLen, ' (payload len', ov.length, ') leftover:', ov.length - dataOff - dataLen);
const ovData = ov.subarray(dataOff, dataOff + dataLen);
let omin = 255, omax = 0, osum = 0;
for (const b of ovData) { if (b < omin) omin = b; if (b > omax) omax = b; osum += b; }
console.log(`overview u8 range: ${omin}..${omax}, mean ${(osum / dataLen).toFixed(2)}`);
// sample rows
console.log('overview row y=0 first 40:', Array.from(ovData.subarray(0, 40)).join(','));
console.log('overview row y=118 mid 40 (x 108..148):', Array.from(ovData.subarray(118 * DIM + 108, 118 * DIM + 148)).join(','));

// correlation: for sample tiles, tile u16 stats vs overview cell candidates.
// overview 237 = 236 + 1: cell (x, y) with x in 0..236? try cell (x, y), (x+1, y+1) offsets.
const rng = (() => { let s = 777 >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; })();
const rows = [];
for (let t = 0; t < 400; t++) {
  const x = Math.floor(rng() * 220), y = Math.floor(rng() * 236);
  const nm = x.toString(16).padStart(4, '0') + y.toString(16).padStart(4, '0') + '.tdf';
  if (!byName.has(nm)) continue;
  const pl = inflate(nm);
  const pdv = new DataView(pl.buffer, pl.byteOffset, pl.byteLength);
  let mn = 65535, mx = 0, sum = 0;
  for (let j = 0; j < 1024; j++) { const v = pdv.getUint16(64 + j * 2, true); if (v < mn) mn = v; if (v > mx) mx = v; sum += v; }
  const mean = sum / 1024;
  const c00 = ovData[y * DIM + x], c11 = ovData[(y + 1) * DIM + (x + 1)];
  rows.push({ x, y, u16min: mn, u16max: mx, u16mean: Math.round(mean), ov00: c00, ov11: c11 });
}
// report a spread table sorted by u16mean
rows.sort((a, b) => a.u16mean - b.u16mean);
for (const r of rows.filter((_, i) => i % 40 === 0)) {
  console.log(`tile(${r.x},${r.y}) u16 min=${r.u16min} max=${r.u16max} mean=${r.u16mean} | ov(x,y)=${r.ov00} ov(x+1,y+1)=${r.ov11}`);
}
// linear fits: u16mean vs ov00 (is overview = u8 of mean/256? min? base?)
let n = 0, sxy = 0, sxx = 0, syy = 0, sx = 0, sy = 0;
for (const r of rows) { const a = r.ov00, b = r.u16mean; n++; sx += a; sy += b; sxy += a * b; sxx += a * a; syy += b * b; }
const cov = sxy / n - (sx / n) * (sy / n);
const sdA = Math.sqrt(sxx / n - (sx / n) ** 2), sdB = Math.sqrt(syy / n - (sy / n) ** 2);
console.log(`corr(ov(x,y), u16mean) = ${(cov / (sdA * sdB)).toFixed(4)}`);
// also min/max fits
function corr(f) { let n = 0, sxy = 0, sxx = 0, syy = 0, sx = 0, sy = 0;
  for (const r of rows) { const a = r.ov00, b = f(r); n++; sx += a; sy += b; sxy += a * b; sxx += a * a; syy += b * b; }
  return ((sxy / n - (sx / n) * (sy / n)) / (Math.sqrt(sxx / n - (sx / n) ** 2) * Math.sqrt(syy / n - (sy / n) ** 2))).toFixed(4); }
console.log('corr(ov, u16min) =', corr(r => r.u16min), ' corr(ov, u16max) =', corr(r => r.u16max));
// ratio: u16max / ov?
let ratioSum = 0, rc = 0;
for (const r of rows) if (r.ov00 > 0) { ratioSum += r.u16mean / r.ov00; rc++; }
console.log('mean(u16mean/ov00) =', (ratioSum / rc).toFixed(2));
// check all-zero tiles vs ov==0
const zeroTiles = rows.filter(r => r.u16max === 0);
console.log('tiles with u16max==0:', zeroTiles.length, 'their ov00 values:', [...new Set(zeroTiles.map(r => r.ov00))].slice(0, 20));
const ov0 = rows.filter(r => r.ov00 === 0);
console.log('tiles with ov00==0:', ov0.length, 'their u16max range:', ov0.length ? [Math.min(...ov0.map(r => r.u16max)), Math.max(...ov0.map(r => r.u16max))] : null);
