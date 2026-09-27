// r1_f04_negative_search.mjs — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926
// F04 independent probe: bounded re-derivation of the negative-search denominators
// + SYNTHETIC DETECTOR CONTROLS (they test the PREDICATE; they are NOT evidence
// that historical resources of these encodings exist).
//   (1) Parameters .vfs count (the cellstream run's denominator);
//   (2) Textures.bnt entry count + the historical cellstream_census.py size
//       predicate {4225,16641,4225+18,16641+18};
//   (3) the expanded_negatives.py predicate over ALL local 9.3.5 .bnt containers:
//       containers, total entries, hits at {4225,16641}+{0,12,16,18};
//   (4) the iter029 known-ID search-line corpora census (BNT/VFS/ARK);
//   (5) synthetic fixtures vs BOTH historical predicates (DETECTED/MISSED).
// READ-ONLY: the only writes are this run's 03_EVIDENCE synthetic fixtures + JSON.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';

const ROOT = 'D:/Eudoria_Reconstruction';
const REPO = ROOT + '/12_WebGame/eudoria-clean';
const EV = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE';
const FIXDIR = path.join(EV, 'synthetic_detector_controls');
fs.mkdirSync(FIXDIR, { recursive: true });
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

// ---------- BNT2 index reader (the expanded_negatives.py framing) ----------
function bntIndex(fileBytes) {
  const fsz = fileBytes.length;
  if (fsz < 16) return null;
  const istart = fileBytes.readUInt32LE(fsz - 8);
  if (!(istart > 0 && istart < fsz)) return null;
  const count = fileBytes.readUInt32LE(istart);
  if (count <= 0 || istart + 4 + count * 21 > fsz) return null;
  const entries = [];
  let pos = istart + 4;
  for (let i = 0; i < count; i++) {
    let ne = pos;
    while (ne < fsz && fileBytes[ne] !== 0x0a) ne++;
    const name = fileBytes.toString('ascii', pos, ne);
    const sz = fileBytes.readUInt32LE(ne + 1);
    const off = fileBytes.readUInt32LE(ne + 5);
    entries.push({ name, size: sz, offset: off });
    pos = ne + 17;
  }
  return entries;
}

const out = { probe: 'F04_NEGATIVE_SEARCH_SCOPE', run_id: 'EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926', node_version: process.version };

// ---------- (1) Parameters ----------
const PAR = ROOT + '/pcg_install/Data/Parameters';
const parFiles = fs.readdirSync(PAR).filter(f => f.toLowerCase().endsWith('.vfs'));
out.parameters = { corpus: PAR, vfs_files: parFiles.length };

// ---------- (2) Textures.bnt entry census ----------
const TEX = ROOT + '/pcg_install/Data/Textures/Textures.bnt';
const texBytes = fs.readFileSync(TEX);
const texEntries = bntIndex(texBytes);
const cellstreamPredicate = new Set([4225, 16641, 4225 + 18, 16641 + 18]);
const texHits = texEntries.filter(e => cellstreamPredicate.has(e.size));
out.textures_entry_census = {
  path: TEX, sha256_fresh: sha256(texBytes), entries: texEntries.length,
  historical_predicate_sizes_bytes: [4225, 16641, 4243, 16659],
  predicate_source: 'cellstream_census.py line ~103: sz in (4225,16641,4225+18,16641+18)',
  hits: texHits.length, hit_names: texHits.map(e => e.name),
};

// ---------- (3) expanded_negatives.py over ALL local 9.3.5 containers ----------
const DATA = ROOT + '/pcg_install/Data';
const wanted = new Set([4225, 16641].flatMap(g => [0, 12, 16, 18].map(v => g + v)));
let containers = 0, totalEntries = 0;
const hits = [];
function walk(p) {
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    const a = path.join(p, e.name);
    if (e.isDirectory()) walk(a);
    else if (a.toLowerCase().endsWith('.bnt')) {
      containers++;
      const b = fs.readFileSync(a);
      const es = bntIndex(b);
      if (!es) { out.stub_note = out.stub_note || []; out.stub_note.push({ path: a, size: b.length, note: '12-byte BNT2 stub -> 0 entries (predicate: fs<16 skip in expanded_negatives; entry count 0 here)' }); continue; }
      totalEntries += es.length;
      for (const e2 of es) if (wanted.has(e2.size)) hits.push({ container: path.basename(a), name: e2.name, size: e2.size });
    }
  }
}
walk(DATA);
const hitKinds = {};
for (const h of hits) hitKinds[h.size] = (hitKinds[h.size] || 0) + 1;
out.expanded_negatives_reproduction = {
  script: 'docs/audits/PE_NIGHT_AGGREGATE_20260905_160000/expanded_negatives.py',
  corpus: DATA, containers, entries: totalEntries,
  predicate_sizes: { grids: { '65x65': 4225, '129x129': 16641 }, variants: [0, 16, 18, 12], tested_set: [...wanted].sort((a, b) => a - b) },
  hits: hits.length, hits_by_size: hitKinds,
  hits_by_kind: {
    compressed_tdf_terrain_bnt: hits.filter(h => h.container === 'terrain.bnt' && h.name.endsWith('.tdf')).length,
    nif_models_bnt: hits.filter(h => h.container === 'Models.bnt' && h.name.endsWith('.nif')).length,
    other: hits.filter(h => !((h.container === 'terrain.bnt' && h.name.endsWith('.tdf')) || (h.container === 'Models.bnt' && h.name.endsWith('.nif')))).length,
  },
};

// ---------- (4) iter029 known-ID search-line corpora census ----------
const IDSCAN = ROOT + '/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter029_idscan.json';
const idscan = JSON.parse(fs.readFileSync(IDSCAN, 'utf8'));
const kinds = { BNT2: 0, VFS: 0, ARK: 0, OTHER: 0 };
for (const s of idscan.scanned) {
  if (s.kind === 'BNT2') kinds.BNT2++; else if (s.kind === 'VFS') kinds.VFS++; else if (s.kind === 'ARK') kinds.ARK++; else kinds.OTHER++;
}
out.iter029_idscan_census = {
  path: IDSCAN, sha256: sha256(fs.readFileSync(IDSCAN)),
  question: idscan.question,
  scanned_total: idscan.scanned.length, by_kind: kinds,
  found_429259_containers: (idscan.found['429259'] || []).length,
  found_432502: (idscan.found['432502'] || []).length,
  found_459344: (idscan.found['459344'] || []).length,
  note: 'The known-ID/provider search (iter029) and the size-coincidence scan (expanded_negatives/N-8) are SEPARATE methods with separate coverage.',
};

// ---------- (5) SYNTHETIC DETECTOR CONTROLS ----------
function rampBytes(n, bpp) {
  const b = Buffer.alloc(n);
  for (let i = 0; i < b.length; i++) b[i] = (i * 7) & 0xff;
  return b;
}
const fixtures = [];
function fixture(name, bytes, spec) {
  const fp = path.join(FIXDIR, name);
  fs.writeFileSync(fp, bytes);
  const sizeHit = wanted.has(bytes.length);
  const cellHit = cellstreamPredicate.has(bytes.length);
  fixtures.push({
    fixture: name, label: 'SYNTHETIC DETECTOR CONTROL — tests the PREDICATE, NOT evidence that historical resources of this encoding exist',
    encoding: spec, size_bytes: bytes.length, sha256: sha256(bytes),
    expanded_negatives_predicate_result: sizeHit ? 'DETECTED' : 'MISSED',
    cellstream_textures_predicate_result: cellHit ? 'DETECTED' : 'MISSED',
  });
}
const H = 18; // the TGA-like 18-byte header variant used by the historical VARIANTS list
fixture('synthetic_raw_u8_65x65.bin', rampBytes(65 * 65), 'raw u8 65x65 = 4225 B');
fixture('synthetic_raw_u8_129x129.bin', rampBytes(129 * 129), 'raw u8 129x129 = 16641 B');
fixture('synthetic_rgb_65x65_tgalike.bin', Buffer.concat([Buffer.alloc(H), rampBytes(65 * 65 * 3)]), 'RGB 65x65 + 18B header = 12693 B');
fixture('synthetic_rgb_129x129_tgalike.bin', Buffer.concat([Buffer.alloc(H), rampBytes(129 * 129 * 3)]), 'RGB 129x129 + 18B header = 49941 B');
fixture('synthetic_rgba_65x65_tgalike.bin', Buffer.concat([Buffer.alloc(H), rampBytes(65 * 65 * 4)]), 'RGBA 65x65 + 18B header = 16918 B');
fixture('synthetic_rgba_129x129_tgalike.bin', Buffer.concat([Buffer.alloc(H), rampBytes(129 * 129 * 4)]), 'RGBA 129x129 + 18B header = 66582 B');
const zfix = zlib.deflateSync(rampBytes(65 * 65));
fixture('synthetic_zlib_65x65_u8.bin', zfix, 'zlib-compressed 65x65 u8 RAMP payload = ' + zfix.length + ' B');
const zfix0 = zlib.deflateSync(Buffer.alloc(65 * 65));
fixture('synthetic_zlib_65x65_u8_zeros.bin', zfix0, 'zlib-compressed 65x65 u8 ZERO payload = ' + zfix0.length + ' B (Desktop\'s control size)');
out.synthetic_detector_controls = {
  directory: '03_EVIDENCE/synthetic_detector_controls/',
  disclaimer: 'SYNTHETIC fixtures — they calibrate the PREDICATE detection boundary only; they are NOT evidence that historical resources of these encodings exist in any corpus.',
  fixtures,
};
// The reconstructed wider PE-MASTER review-time Textures predicate (32 classes)
const wide = new Set();
for (const g of [4225, 8450, 12675, 16900, 16641, 33282, 49923, 66564]) for (const v of [0, 12, 16, 18]) wide.add(g + v);
out.synthetic_detector_controls.wider_review_predicate_check = {
  note: 'Reconstruction of the PE-MASTER review-time Textures.bnt 32-size-class predicate (65x65/129x129 x u8/u16/24bpp/32bpp x {0,+12,+16,+18}); the review recorded 32 classes, 0/8,381 hits.',
  fixtures_detected_under_wider_predicate: fixtures.map(f => ({ fixture: f.fixture, detected: wide.has(f.size_bytes) })),
};

fs.writeFileSync(path.join(EV, 'F04_NEGATIVE_SEARCH_CONTROLS.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({
  parameters: out.parameters.vfs_files,
  textures: { entries: out.textures_entry_census.entries, hits: out.textures_entry_census.hits },
  expanded: { containers: out.expanded_negatives_reproduction.containers, entries: out.expanded_negatives_reproduction.entries, hits: out.expanded_negatives_reproduction.hits, by_kind: out.expanded_negatives_reproduction.hits_by_kind },
  iter029: { total: out.iter029_idscan_census.scanned_total, by_kind: out.iter029_idscan_census.by_kind, found429259: out.iter029_idscan_census.found_429259_containers, found432502: out.iter029_idscan_census.found_432502, found459344: out.iter029_idscan_census.found_459344 },
  fixtures: out.synthetic_detector_controls.fixtures.map(f => ({ n: f.fixture, size: f.size_bytes, n8: f.expanded_negatives_predicate_result, cs: f.cellstream_textures_predicate_result })),
}, null, 2));
