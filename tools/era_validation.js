// era_validation.js — FULL decoder era-validation of pcg_9_3_5 terrain.bnt vs JUL 50.bnt
// M1-E CLEAN_RUNTIME_FOUNDATION START R2 — ITER 019 SECTION 2 (mandatory first step)
//
// Questions answered (field-by-field, evidence JSON):
//  Q1 footer magic + dir/index offset layout (terrain.bnt vs 50.bnt)
//  Q2 entry count + full index walk
//  Q3 name convention census (patterns, lengths, grid-addressability)
//  Q4 record framing at payload offsets (marker/decompressedSize/zlib)
//  Q5 size-field semantics: does the iter005i trailing-8-bytes quirk hold,
//     or is size exact? (sampled empirical test: zlib stream length)
//  Q6 sample decode: full inflate + TDF shape check (32x32 u16 @ offset 64)
//  Q7 50.bnt reference parse with the same probes (BUNT path, for diff)
//
// READ-ONLY on both originals. No decoder mutated here; this is the measurement.
'use strict';
const fs = require('fs');
const zlib = require('zlib');
const crypto = require('crypto');

const RESULTS = { iter: '019', phase: 'era_validation', created: new Date().toISOString() };

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex').toUpperCase(); }

// ---------- generic index walkers ----------
function parseBuntIndex(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const magic = buf.toString('latin1', buf.length - 4);
  const indexOffset = dv.getUint32(buf.length - 8, true);
  const count = dv.getUint32(indexOffset, true);
  const entries = [];
  for (let i = 0; i < count; i++) {
    const p = indexOffset + 4 + i * 21;
    let name = '';
    for (let j = 0; j < 13; j++) { const c = buf[p + j]; if (c === 0) break; name += String.fromCharCode(c); }
    name = name.replace(/[\r\n\0]+$/, '');
    entries.push({ name, packedSize: dv.getUint32(p + 13, true), offset: dv.getUint32(p + 17, true) });
  }
  const indexEnd = indexOffset + 4 + count * 21;
  return { footerMagic: magic, indexOffset, count, entries, indexEnd, exact: indexEnd === buf.length - 8 };
}

function parseBnt2Index(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const magic = buf.toString('latin1', buf.length - 4);
  const dirOffset = dv.getUint32(buf.length - 8, true);
  const count = dv.getUint32(dirOffset, true);
  const entries = [];
  let p = dirOffset + 4;
  for (let i = 0; i < count; i++) {
    const nameStart = p;
    while (p < buf.length && buf[p] !== 0x0a) p++;
    const name = buf.toString('latin1', nameStart, p);
    p++; // 0x0A
    const size = dv.getUint32(p, true), offset = dv.getUint32(p + 4, true),
          crc32 = dv.getUint32(p + 8, true), pad = dv.getUint32(p + 12, true);
    p += 16;
    entries.push({ entryIndex: i, name, size, offset, crc32, pad });
  }
  return { footerMagic: magic, dirOffset, count, entries, indexEnd: p, exact: p === buf.length - 8 };
}

// ---------- census helpers ----------
function nameCensus(entries) {
  const pat = new Map();
  const lenHist = new Map();
  for (const e of entries) {
    const base = e.name.replace(/\.[a-z]+$/i, '');
    const shape = base.replace(/\d/g, 'N');
    pat.set(shape, (pat.get(shape) || 0) + 1);
    lenHist.set(e.name.length, (lenHist.get(e.name.length) || 0) + 1);
  }
  return {
    distinct_names: new Set(entries.map(e => e.name)).size,
    name_shapes: Object.fromEntries([...pat.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20)),
    name_length_hist: Object.fromEntries([...lenHist.entries()].sort((a, b) => a[0] - b[0])),
  };
}

// ---------- 9.3.5 terrain.bnt ----------
const TERRAIN = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
const terrainBuf = fs.readFileSync(TERRAIN);
const terrain = parseBnt2Index(terrainBuf);

console.log('== terrain.bnt (PCG 9.3.5) ==');
console.log('  footer magic:', terrain.footerMagic, 'dirOffset:', terrain.dirOffset,
  'count:', terrain.count, 'indexEndExact:', terrain.exact);
console.log('  first 3 entries:', JSON.stringify(terrain.entries.slice(0, 3)));
console.log('  last 3 entries:', JSON.stringify(terrain.entries.slice(-3)));
const tc = nameCensus(terrain.entries);
console.log('  name census:', JSON.stringify(tc));

// pad + crc sanity over all entries
let padNonZero = 0, crcSamples = [];
for (const e of terrain.entries) { if (e.pad !== 0) padNonZero++; }
console.log('  pad!=0 count:', padNonZero, '/', terrain.count);

// ---------- Q5/Q6: record framing + size semantics (sampled) ----------
const samples = [];
const sampleIdx = [];
for (let i = 0; i < 7; i++) sampleIdx.push(Math.floor(i * terrain.count / 7));
sampleIdx.push(terrain.count - 1);
for (const i of sampleIdx) {
  const e = terrain.entries[i];
  const dv = new DataView(terrainBuf.buffer, terrainBuf.byteOffset, terrainBuf.byteLength);
  const marker = dv.getUint32(e.offset, true);
  const decSize = dv.getUint32(e.offset + 4, true);
  // try exact-size slice first, then size-8 (JUL quirk), record which inflates cleanly
  const trials = {};
  for (const [label, len] of [['exact_size', e.size], ['size_minus_8', e.size - 8]]) {
    try {
      const comp = terrainBuf.subarray(e.offset + 8, e.offset + 8 + len);
      const out = zlib.inflateSync(comp);
      trials[label] = { ok: true, inflated: out.length, matchesHeader: out.length === decSize, sha256: sha256(out) };
    } catch (err) {
      trials[label] = { ok: false, error: String(err.message).slice(0, 80) };
    }
  }
  samples.push({
    entryIndex: i, name: e.name, offset: e.offset, size: e.size,
    marker: '0x' + marker.toString(16).padStart(8, '0'),
    markerOk: marker === 0xff000002, decompressedSize: decSize,
    trials,
  });
  console.log(`  sample ${i} "${e.name}" size=${e.size} dec=${decSize} markerOk=${marker === 0xff000002} ` +
    `exact:${trials.exact_size.ok ? trials.exact_size.matchesHeader ? 'MATCH' : 'LEN-MISMATCH' : 'FAIL'} ` +
    `size-8:${trials.size_minus_8.ok ? trials.size_minus_8.matchesHeader ? 'MATCH' : 'LEN-MISMATCH' : 'FAIL'}`);
}

// TDF shape check on first sample that inflates
let tdfShape = null;
for (const s of samples) {
  const key = s.trials.exact_size.ok && s.trials.exact_size.matchesHeader ? 'exact_size'
            : s.trials.size_minus_8.ok && s.trials.size_minus_8.matchesHeader ? 'size_minus_8' : null;
  if (!key) continue;
  const e = terrain.entries[s.entryIndex];
  const len = key === 'exact_size' ? e.size : e.size - 8;
  const out = zlib.inflateSync(terrainBuf.subarray(e.offset + 8, e.offset + 8 + len));
  const dv = new DataView(out.buffer, out.byteOffset, out.byteLength);
  const heights = [];
  for (let j = 0; j < 8; j++) heights.push(dv.getUint16(64 + j * 2, true));
  tdfShape = {
    sample: s.name, payload_len: out.length, data_size_2100: out.length === 2100 || out.length >= 2112,
    first8_heights_u16le_at64: heights,
  };
  console.log('  TDF shape:', JSON.stringify(tdfShape));
  break;
}

// ---------- Q3: name pattern analysis (grid addressability) ----------
const names = terrain.entries.map(e => e.name);
const numeric = names.filter(n => /^(\d+)\.tdf$/i.test(n));
const numVals = numeric.map(n => parseInt(n.match(/^(\d+)\.tdf$/i)[1], 10));
const min = Math.min(...numVals), max = Math.max(...numVals);
console.log(`  numeric .tdf names: ${numeric.length}/${terrain.count}, id range ${min}..${max}`);
// deltas census
const sortedVals = [...numVals].sort((a, b) => a - b);
const deltas = new Map();
for (let i = 1; i < sortedVals.length; i++) {
  const d = sortedVals[i] - sortedVals[i - 1];
  deltas.set(d, (deltas.get(d) || 0) + 1);
}
console.log('  id delta histogram (top):', JSON.stringify(Object.fromEntries([...deltas.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10))));
const nonNumeric = names.filter(n => !/^(\d+)\.tdf$/i.test(n));
console.log('  non-numeric names:', JSON.stringify(nonNumeric.slice(0, 10)), 'count:', nonNumeric.length);

// ---------- Q7: 50.bnt reference parse ----------
const B50 = 'C:\\Entropia Universe\\Data\\Terrain\\50.bnt';
const b50Buf = fs.readFileSync(B50);
const b50 = parseBuntIndex(b50Buf);
const b50c = nameCensus(b50.entries);
console.log('== 50.bnt (JUL 2003 reference) ==');
console.log('  footer magic:', b50.footerMagic, 'count:', b50.count, 'indexEndExact:', b50.exact);
console.log('  first 3:', JSON.stringify(b50.entries.slice(0, 3)));
console.log('  name census:', JSON.stringify(b50c));

// ---------- evidence JSON ----------
RESULTS.sources = {
  terrain_bnt: { path: TERRAIN, size: terrainBuf.length, sha256: sha256(terrainBuf) },
  b50: { path: B50, size: b50Buf.length, sha256: sha256(b50Buf) },
};
RESULTS.terrain_935 = {
  footer_magic: terrain.footerMagic,
  dir_offset: terrain.dirOffset,
  count: terrain.count,
  index_end_exact: terrain.exact,
  first_entries: terrain.entries.slice(0, 3),
  last_entries: terrain.entries.slice(-3),
  pad_nonzero_count: padNonZero,
  ...tc,
  numeric_tdf_names: numeric.length,
  numeric_id_range: [min, max],
  id_delta_histogram_top: Object.fromEntries([...deltas.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10)),
  non_numeric_names: nonNumeric.slice(0, 20),
  non_numeric_count: nonNumeric.length,
};
RESULTS.jul_50bnt = {
  footer_magic: b50.footerMagic,
  count: b50.count,
  index_end_exact: b50.exact,
  first_entries: b50.entries.slice(0, 3),
  ...b50c,
};
RESULTS.record_framing_samples = samples;
RESULTS.tdf_shape = tdfShape;
RESULTS.field_by_field_vs_50bnt = {
  footer_magic: { jul: 'BUNT', pcg: 'BNT2', diverged: true },
  index_offset_field: { jul: 'u32 LE at len-8', pcg: 'u32 LE at len-8', diverged: false },
  entry_layout: {
    jul: 'fixed 21 bytes: 13-byte name (XXXXXXXX.tdf\\n) + u32 packedSize + u32 offset',
    pcg: 'variable: 0x0A-terminated name + u32 size + u32 offset + u32 crc32 + u32 pad',
    diverged: true,
  },
  name_convention: {
    jul: 'XXXXXXXX.tdf — 8 hex chars = grid xy (filename-xy addressing, 220x236)',
    pcg: 'N+.tdf — sequential numeric ids (grid addressability UNRESOLVED this probe)',
    diverged: true,
  },
  record_framing: {
    jul: '02 00 00 FF + u32 decompressedSize + zlib',
    pcg: '02 00 00 FF + u32 decompressedSize + zlib (SAME, sample-verified)',
    diverged: false,
  },
  packed_size_trailing_8_quirk: {
    jul: 'packedSize counts 8 bytes MORE than the zlib stream (iter005i, all 51921 entries)',
    pcg: 'per-sample empirical result below (samples[].trials)',
    diverged: 'see samples',
  },
};
fs.writeFileSync(__dirname + '\\era_validation_partial.json', JSON.stringify(RESULTS, null, 2));
console.log('\npartial evidence written: era_validation_partial.json');
