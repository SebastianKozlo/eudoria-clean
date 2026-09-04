// era_validation_2.js — follow-up: grid extent, size-semantics discriminators, TDF payload structure
// M1-E ITER 019 era-validation part 2. READ-ONLY.
'use strict';
const fs = require('fs');
const zlib = require('zlib');
const crypto = require('crypto');
function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex').toUpperCase(); }

const TERRAIN = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
const buf = fs.readFileSync(TERRAIN);
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const dirOffset = dv.getUint32(buf.length - 8, true);
const count = dv.getUint32(dirOffset, true);

// re-walk index, collect entries + grid coords
const entries = [];
let p = dirOffset + 4;
for (let i = 0; i < count; i++) {
  const ns = p; while (buf[p] !== 0x0a) p++;
  const name = buf.toString('latin1', ns, p); p++;
  entries.push({ name, size: dv.getUint32(p, true), offset: dv.getUint32(p + 4, true), crc32: dv.getUint32(p + 8, true), pad: dv.getUint32(p + 12, true) });
  p += 16;
}

// Q3b: grid coords from names (first 4 hex = x, next 4 = y — same as JUL convention)
let max = 0, xs = new Set(), ys = new Set(), badNames = [];
for (const e of entries) {
  const m = e.name.match(/^([0-9a-fA-F]{4})([0-9a-fA-F]{4})\.tdf$/);
  if (!m) { badNames.push(e.name); continue; }
  const x = parseInt(m[1], 16), y = parseInt(m[2], 16);
  xs.add(x); ys.add(y); if (x > max) max = x; if (y > max) max = y;
}
console.log('grid: distinct x:', xs.size, 'distinct y:', ys.size, 'max coord:', max.toString(16));
console.log('bad names:', badNames.length, badNames.slice(0, 5));
// completeness: is the x-set contiguous 0..maxX? y-set?
const xmax = Math.max(...xs), ymax = Math.max(...ys), xmin = Math.min(...xs), ymin = Math.min(...ys);
console.log(`x range ${xmin}..${xmax} (${xs.size} distinct), y range ${ymin}..${ymax} (${ys.size} distinct)`);
const xArr = [...xs].sort((a, b) => a - b), yArr = [...ys].sort((a, b) => a - b);
let xGaps = [], yGaps = [];
for (let i = 1; i < xArr.length; i++) if (xArr[i] !== xArr[i - 1] + 1) xGaps.push([xArr[i - 1], xArr[i]]);
for (let i = 1; i < yArr.length; i++) if (yArr[i] !== yArr[i - 1] + 1) yGaps.push([yArr[i - 1], yArr[i]]);
console.log('x gaps:', JSON.stringify(xGaps.slice(0, 10)), 'y gaps:', JSON.stringify(yGaps.slice(0, 10)));
console.log('expected tiles if full rect:', (xmax - xmin + 1) * (ymax - ymin + 1), 'actual:', count - badNames.length);
// sentinel-like entries (7ffe7ffe)?
const sent = entries.filter(e => /7ffe/i.test(e.name));
console.log('7ffe entries:', JSON.stringify(sent.map(e => e.name)));

// Q5b: contiguity discriminator — offset_{i+1} == offset_i + size_i for ALL entries?
let contiguous = true, breaks = 0;
for (let i = 0; i < entries.length - 1; i++) {
  if (entries[i].offset + entries[i].size !== entries[i + 1].offset) { breaks++; if (breaks <= 5) console.log(`  contiguity break @${i} "${entries[i].name}": ${entries[i].offset}+${entries[i].size} != ${entries[i + 1].offset}`); }
}
console.log('contiguity breaks:', breaks, '/', entries.length - 1, '=> records span [offset, offset+size), 8B header INSIDE size');
// Therefore true zlib stream length = size - 8 (same trailing-8 semantics as JUL BUNT).

// Q5c: exact-stream inflation test with STRICT slicing on random 25 entries
let strictOk = 0, strictFail = [];
const rng = (() => { let s = 0x20030130 >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; })();
for (let t = 0; t < 25; t++) {
  const i = Math.floor(rng() * entries.length);
  const e = entries[i];
  try {
    const out = zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size));
    const dec = dv.getUint32(e.offset + 4, true);
    if (out.length !== dec) throw new Error(`len ${out.length} != header ${dec}`);
    strictOk++;
  } catch (err) { strictFail.push({ name: e.name, error: String(err.message) }); }
}
console.log(`strict size-8 inflation: ${strictOk}/25 ok; fails:`, JSON.stringify(strictFail.slice(0, 3)));

// Q6b: TDF payload structure census — dec sizes histogram, and structure of a few payloads
const decHist = new Map();
for (let i = 0; i < count; i++) {
  const d = dv.getUint32(entries[i].offset + 4, true);
  decHist.set(d, (decHist.get(d) || 0) + 1);
}
const top = [...decHist.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15);
console.log('decompressed-size histogram (top 15):', JSON.stringify(top.map(([d, n]) => [d, n])));
console.log('distinct dec sizes:', decHist.size, 'min:', Math.min(...decHist.keys()), 'max:', Math.max(...decHist.keys()));

// structure probe: pick one dec=3652 and one dec=2386 and one large, dump header + regions
function dumpEntry(name) {
  const e = entries.find(x => x.name === name);
  const out = zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size));
  console.log(`--- ${name} dec=${out.length} ---`);
  console.log('  header[0..52):', out.subarray(0, 52).toString('hex').match(/../g).join(' '));
  console.log('  subhdr[52..64):', out.subarray(52, 64).toString('hex').match(/../g).join(' '));
  const hdv = new DataView(out.buffer, out.byteOffset, out.byteLength);
  const h = []; for (let i = 0; i < 16; i++) h.push(hdv.getUint16(64 + i * 2, true));
  const nonzero = [...out.subarray(64, 2112)].some(b => b !== 0);
  console.log('  heights[64..2112): first16 u16le =', JSON.stringify(h), 'any-nonzero:', nonzero);
  console.log('  tail[2112..2112+48):', out.subarray(2112, 2160).toString('hex').match(/../g).join(' '));
  console.log('  tail len:', out.length - 2112, 'mod 308:', (out.length - 2112) % 308, 'mod 16:', (out.length - 2112) % 16);
  return { name, dec: out.length, header_hex: out.subarray(0, 52).toString('hex'), subheader_hex: out.subarray(52, 64).toString('hex'), heights_nonzero: nonzero, tail_len: out.length - 2112, tail_mod308: (out.length - 2112) % 308 };
}
const dumps = [];
// find representative names of several dec sizes
const byDec = {};
for (const [d, n] of decHist) if (n > 100) byDec[d] = true;
const targets = top.slice(0, 4).map(([d]) => d);
for (const d of targets) {
  const e = entries.find(x => dv.getUint32(x.offset + 4, true) === d && x.size < 20000);
  if (e) dumps.push(dumpEntry(e.name));
}

// heights sanity across a spatial sample: decode 20 random tiles, report height min/max at 64..2112
let hmin = 65535, hmax = 0;
for (let t = 0; t < 20; t++) {
  const i = Math.floor(rng() * count);
  const e = entries[i];
  const out = zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size));
  if (out.length < 2112) continue;
  const hdv = new DataView(out.buffer, out.byteOffset, out.byteLength);
  for (let j = 0; j < 1024; j++) { const v = hdv.getUint16(64 + j * 2, true); if (v < hmin) hmin = v; if (v > hmax) hmax = v; }
}
console.log('height u16 range over 20 random tiles:', hmin, '..', hmax);

// save part-2 evidence
fs.writeFileSync(__dirname + '\\era_validation_partial2.json', JSON.stringify({
  iter: '019', phase: 'era_validation_part2',
  terrain: { count, dir_offset: dirOffset, footer: 'BNT2' },
  grid: { x_range: [xmin, xmax], y_range: [ymin, ymax], distinct_x: xs.size, distinct_y: ys.size, x_gaps: xGaps, y_gaps: yGaps, expected_full_rect: (xmax - xmin + 1) * (ymax - ymin + 1), bad_names: badNames.slice(0, 10) },
  contiguity_breaks: breaks,
  strict_size_minus_8_inflation: { ok: strictOk, of: 25, fails: strictFail.slice(0, 3) },
  dec_size_hist_top: top, dec_size_distinct: decHist.size,
  dec_size_min: Math.min(...decHist.keys()), dec_size_max: Math.max(...decHist.keys()),
  structure_dumps: dumps,
  height_range_sample20: [hmin, hmax],
}, null, 2));
console.log('part2 evidence written');
