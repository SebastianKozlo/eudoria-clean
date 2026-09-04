// header_minmax_probe.js — correlate TDF header floats with per-tile height min/max
// Read-only. Q: where do FUN_0047fb20's per-tile min/max come from?
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
function inflate(name) {
  const e = byName.get(name);
  return zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size));
}
// pick tiles with real relief: sample 3000 tiles, keep 12 with widest u16 range
const rng = (() => { let s = 12345 >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; })();
const cands = [];
for (let t = 0; t < 3000; t++) {
  const x = Math.floor(rng() * 220), y = Math.floor(rng() * 236);
  const nm = x.toString(16).padStart(4, '0') + y.toString(16).padStart(4, '0') + '.tdf';
  if (!byName.has(nm)) continue;
  const pl = inflate(nm);
  const pdv = new DataView(pl.buffer, pl.byteOffset, pl.byteLength);
  let mn = 65535, mx = 0;
  for (let j = 0; j < 1024; j++) { const v = pdv.getUint16(64 + j * 2, true); if (v < mn) mn = v; if (v > mx) mx = v; }
  cands.push({ nm, mn, mx, range: mx - mn });
}
cands.sort((a, b) => b.range - a.range);
for (const c of cands.slice(0, 12)) {
  const pl = inflate(c.nm);
  const pdv = new DataView(pl.buffer, pl.byteOffset, pl.byteLength);
  const f = []; for (let o = 16; o <= 44; o += 4) f.push(`@${o}=${pdv.getFloat32(o, true).toPrecision(8)}`);
  const u = []; for (let o = 16; o <= 44; o += 4) u.push(`@${o}=${pdv.getUint32(o, true)}`);
  console.log(`${c.nm} u16min=${c.mn} u16max=${c.mx}`);
  console.log(`   f32: ${f.join(' ')}`);
  console.log(`   u32: ${u.join(' ')}`);
}
