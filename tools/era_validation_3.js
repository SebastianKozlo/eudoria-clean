// era_validation_3.js — material-record walk on 9.3.5 regular tiles + extra-tile census
// M1-E ITER 019 era-validation part 3. READ-ONLY.
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
const entries = [];
let p = dirOffset + 4;
for (let i = 0; i < count; i++) {
  const ns = p; while (buf[p] !== 0x0a) p++;
  const name = buf.toString('latin1', ns, p); p++;
  entries.push({ name, size: dv.getUint32(p, true), offset: dv.getUint32(p + 4, true) });
  p += 16;
}
const byName = new Map(entries.map(e => [e.name, e]));
function inflate(e) { return zlib.inflateSync(buf.subarray(e.offset + 8, e.offset + e.size)); }

// ---- classify tiles: regular (x<=219,y<=235), sentinel (7ffe7ffe), extra ----
const regular = [], extra = [];
let sentinel = null;
for (const e of entries) {
  const x = parseInt(e.name.slice(0, 4), 16), y = parseInt(e.name.slice(4, 8), 16);
  if (e.name === '7ffe7ffe.tdf') sentinel = e;
  else if (x <= 219 && y <= 235) regular.push(e);
  else extra.push({ ...e, x, y });
}
console.log(`regular: ${regular.length}, extra: ${extra.length}, sentinel: ${sentinel ? 1 : 0}, total: ${count}`);
// extra census by y
const yHist = new Map();
for (const e of extra) yHist.set(e.y, (yHist.get(e.y) || 0) + 1);
console.log('extra y histogram:', JSON.stringify([...yHist.entries()].sort((a, b) => a[0] - b[0])));
const xHist = new Map();
for (const e of extra) xHist.set(e.x, (xHist.get(e.x) || 0) + 1);
console.log('extra x histogram (top):', JSON.stringify([...xHist.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10)));
// regular grid completeness 220x236 = 51,920?
console.log('regular count == 220*236 =', regular.length === 51920);

// ---- material record walk on a deterministic sample of regular tiles ----
// JUL CONFIRMED semantics (iter008 winning walk, 51920/51920 exact on 50.bnt):
//   record = [u32 size][u32 dim][body of (size-4) bytes]; STRIDE = size + 4;
//   size counts ALL bytes after itself. header48: unk@+8, bps@+12 (2=material),
//   id@+16, res@+20, name[28]@+24..51, extra4@+52..55, mask@+56..(size+3),
//   len = size-52; RAW u8 when len==dim*dim else RLE (count,value) pairs.
function walkRecords(payload) {
  const pdv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  let off = 2112; const recs = [];
  while (off < payload.length) {
    if (off + 8 > payload.length) return { ok: false, error: `truncated tag @${off}`, recs };
    const size = pdv.getUint32(off, true);
    const dim = pdv.getUint32(off + 4, true);
    if (size < 52 || (dim & (dim - 1)) !== 0 || dim === 0 || dim > 256) {
      return { ok: false, error: `bad record tag @${off} (size=${size},dim=${dim})`, recs };
    }
    if (off + 4 + size > payload.length) return { ok: false, error: `record @${off} size ${size} overruns payload`, recs };
    const bps = pdv.getUint32(off + 12, true);
    const id = pdv.getUint32(off + 16, true);
    const name = payload.toString('latin1', off + 24, off + 52).replace(/\0.*$/, '');
    const maskLen = size - 52;
    let maskMode = null;
    if (maskLen === dim * dim) maskMode = 'raw_u8';
    else if (maskLen % 2 === 0) {
      // validate RLE (count,value) sums exactly to dim*dim
      let total = 0, okRle = true;
      for (let q = 0; q + 1 < maskLen; q += 2) {
        total += payload[off + 56 + q];
        if (total > dim * dim) { okRle = false; break; }
      }
      if (okRle && total === dim * dim) maskMode = 'rle_cv';
    }
    recs.push({ off, size, dim, bps, id, name, maskLen, maskMode });
    off += size + 4;
  }
  return { ok: true, recs };
}

// sample: deterministic 60 regular tiles spread across the grid
const regByName = new Map(regular.map(e => [e.name, e]));
const sampleNames = [];
for (let t = 0; t < 60; t++) {
  const x = Math.floor((t * 37) % 220), y = Math.floor((t * 61) % 236);
  const nm = x.toString(16).padStart(4, '0') + y.toString(16).padStart(4, '0') + '.tdf';
  if (regByName.has(nm)) sampleNames.push(nm);
}
let walkOk = 0, walkFail = [];
const sizeCensus = new Map(), nameCensus = new Map(), idCensus = new Map();
const walkDetails = [];
for (const nm of sampleNames) {
  const e = regByName.get(nm);
  const payload = inflate(e);
  const w = walkRecords(payload);
  if (w.ok) {
    walkOk++;
    walkDetails.push({ name: nm, records: w.recs.map(r => ({ size: r.size, id: r.id, name: r.name })) });
    for (const r of w.recs) {
      sizeCensus.set(r.size, (sizeCensus.get(r.size) || 0) + 1);
      nameCensus.set(r.name, (nameCensus.get(r.name) || 0) + 1);
      idCensus.set(r.id, (idCensus.get(r.id) || 0) + 1);
    }
  } else walkFail.push({ name: nm, error: w.error });
}
console.log(`record walk on regular tiles: ${walkOk}/${sampleNames.length} ok`);
console.log('  walk failures:', JSON.stringify(walkFail.slice(0, 5)));
console.log('  record size census:', JSON.stringify([...sizeCensus.entries()].sort((a, b) => b[1] - a[1])));
console.log('  material name census (top):', JSON.stringify([...nameCensus.entries()].sort((a, b) => b[1] - a[1]).slice(0, 25)));
console.log('  material id census (top):', JSON.stringify([...idCensus.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15)));

// FULL-GRID walk on ALL regular tiles (bounded: 51,920 inflates ~ acceptable)
let fullOk = 0; const fullFail = []; const fullNameCensus = new Map(); const fullSizeCensus = new Map();
let totalRecords = 0;
const t0 = Date.now();
for (const e of regular) {
  const payload = inflate(e);
  const w = walkRecords(payload);
  if (w.ok) {
    fullOk++; totalRecords += w.recs.length;
    for (const r of w.recs) {
      fullNameCensus.set(r.name, (fullNameCensus.get(r.name) || 0) + 1);
      fullSizeCensus.set(r.size, (fullSizeCensus.get(r.size) || 0) + 1);
    }
  } else fullFail.push({ name: e.name, error: w.error });
  if (fullFail.length > 10) break;
}
console.log(`FULL regular-tile walk: ${fullOk}/${regular.length} ok, ${totalRecords} records, ${((Date.now() - t0) / 1000).toFixed(1)}s`);
console.log('  full failures:', JSON.stringify(fullFail.slice(0, 10)));
console.log('  full record size census:', JSON.stringify([...fullSizeCensus.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10)));
console.log('  distinct material names:', fullNameCensus.size);
fs.writeFileSync(__dirname + '\\era_validation_material_names.json',
  JSON.stringify([...fullNameCensus.entries()].sort((a, b) => b[1] - a[1]), null, 2));

// heights semantics probe for P0: check header u32@8 data_size and @12 dim across regular tiles (sample 200)
let stdCount = 0, nonStd = [];
const rng = (() => { let s = 0x20030130 >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; })();
for (let t = 0; t < 200; t++) {
  const e = regular[Math.floor(rng() * regular.length)];
  const payload = inflate(e);
  const pdv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ds = pdv.getUint32(8, true), dim = pdv.getUint32(12, true);
  if (ds === 2100 && dim === 32) stdCount++; else nonStd.push({ name: e.name, ds, dim });
}
console.log(`standard-tile header check (200 random): ${stdCount}/200; nonStd:`, JSON.stringify(nonStd.slice(0, 5)));

// sentinel decode
if (sentinel) {
  const sp = inflate(sentinel);
  const sdv = new DataView(sp.buffer, sp.byteOffset, sp.byteLength);
  console.log('sentinel payload len:', sp.length, 'data_size:', sdv.getUint32(8, true), 'dim:', sdv.getUint32(12, true));
}

// ---- save part-3 evidence ----
fs.writeFileSync(__dirname + '\\era_validation_partial3.json', JSON.stringify({
  iter: '019', phase: 'era_validation_part3',
  tile_classification: { regular: regular.length, extra: extra.length, sentinel: sentinel ? 1 : 0, total: count,
    regular_equals_220x236: regular.length === 51920,
    extra_y_histogram: [...yHist.entries()].sort((a, b) => a[0] - b[0]),
    extra_x_histogram_top: [...xHist.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10) },
  record_walk_sample60: { ok: walkOk, of: sampleNames.length, failures: walkFail.slice(0, 5),
    size_census: [...sizeCensus.entries()].sort((a, b) => b[1] - a[1]),
    name_census_top: [...nameCensus.entries()].sort((a, b) => b[1] - a[1]).slice(0, 40) },
  record_walk_full: { ok: fullOk, of: regular.length, total_records: totalRecords, failures: fullFail.slice(0, 10),
    size_census: [...fullSizeCensus.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10),
    distinct_material_names: fullNameCensus.size },
  standard_header_check_200: { ok: stdCount, of: 200, non_std: nonStd.slice(0, 5) },
  sentinel: sentinel ? { name: sentinel.name, size: sentinel.size, dec: inflate(sentinel).length,
    data_size: new DataView(inflate(sentinel).buffer).getUint32(8, true) } : null,
  sample_walk_details: walkDetails.slice(0, 5),
}, null, 2));
console.log('part3 evidence written');
