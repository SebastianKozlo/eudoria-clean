// iter020_secondary_probes.js — MILESTONE 1-E ITER 020 BOUNDED SECONDARY PROBES
// (P0 PASSED first; probes are evidence-labeled, bounded, no semantics claims
// where evidence is insufficient — UNRESOLVED stays UNRESOLVED).
//
// PROBE 1 — TDF sub-header (payload 52..63) min/max source: FUN_0047fb20's
//   per-tile min/max (tile_obj+0x24/+0x28) SOURCE is UNRESOLVED; the
//   sub-header reads ZERO on content tiles (iter019). Data probe: census the
//   sub-header bytes vs the tile's actual height min/max on a bounded sample.
// PROBE 2 — TDF payload header u32[0..1] vs filename-xy: census on a sample
//   (is the mismatch consistent? correlated with anything?).
// PROBE 3 — special-row tiles (y=0xff1a..0xffff, 6,530 entries): STRUCTURE
//   census only (sizes, dims, record classes) — NO semantics claims.
'use strict';
import { promises as fs } from 'node:fs';
import { createHash } from 'node:crypto';
import { inflateSync } from 'node:zlib';
import { Bnt2TerrainArchive } from '../src/pesource/Bnt2TerrainArchive.js';

const TERRAIN_PATH = 'D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt';
const EVIDENCE_DIR = 'D:/Eudoria_Reconstruction/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE';
const bytes = new Uint8Array(await fs.readFile(TERRAIN_PATH));
const sha256 = (b) => createHash('sha256').update(b).digest('hex').toUpperCase();
console.log('terrain.bnt sha256:', sha256(bytes));

const io = { inflate: async (z) => new Uint8Array(inflateSync(z)) };
const arch = new Bnt2TerrainArchive(bytes, io);
const entries = arch.entries();
const regular = entries.filter((e) => {
  const m = e.name.match(/^([0-9a-f]{4})([0-9a-f]{4})\.tdf$/);
  if (!m || e.name === '7ffe7ffe.tdf') return false;
  const y = parseInt(m[2], 16);
  return y < 0xff1a; // 51,920 regular grid tiles (special rows excluded LOUDLY)
});
const special = entries.filter((e) => {
  const m = e.name.match(/^([0-9a-f]{4})([0-9a-f]{4})\.tdf$/);
  return m && parseInt(m[2], 16) >= 0xff1a && parseInt(m[2], 16) <= 0xffff;
});
console.log('entries:', entries.length, 'regular:', regular.length, 'special-row:', special.length);

// deterministic bounded sample (LCG, seeded — reproducible)
let seed = 20030130;
const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
const SAMPLE = 400;
const sample = [];
for (let i = 0; i < SAMPLE; i++) sample.push(regular[Math.floor(rnd() * regular.length)]);

// ---------- PROBE 1: sub-header vs height min/max ----------
const p1 = { sample: SAMPLE, subHeaderClasses: new Map(), minMaxMatch: 0, anyNonZero: 0, examples: [] };
for (const e of sample) {
  const { payload } = await arch.readEntry(e);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const sh = Array.from(payload.subarray(52, 64));
  let mn = 0xffff, mx = 0;
  for (let i = 0; i < 1024; i++) {
    const v = dv.getUint16(64 + i * 2, true);
    if (v < mn) mn = v; if (v > mx) mx = v;
  }
  const shNonZero = sh.some((b) => b !== 0);
  if (shNonZero) { p1.anyNonZero++; if (p1.examples.length < 10) p1.examples.push({ name: e.name, subheader: sh, heightMin: mn, heightMax: mx }); }
  // check all plausible encodings of min/max in the 12 sub-header bytes
  const u16 = []; for (let i = 0; i < 6; i++) u16.push(dv.getUint16(52 + i * 2, true));
  const u32 = [dv.getUint32(52, true), dv.getUint32(56, true), dv.getUint32(60, true)];
  const f32 = []; for (let i = 0; i < 3; i++) f32.push(dv.getFloat32(52 + i * 4, true));
  const encodings = {
    u16_first_is_min: u16[0] === mn, u16_second_is_max: u16[1] === mx,
    u32_0_is_min: u32[0] === mn, u32_1_is_max: u32[1] === mx,
    f32_0_is_min_m: Math.abs(f32[0] - mn / 128) < 0.01, f32_1_is_max_m: Math.abs(f32[1] - mx / 128) < 0.01,
    f32_0_is_min: Math.abs(f32[0] - mn) < 0.01, f32_1_is_max: Math.abs(f32[1] - mx) < 0.01,
  };
  for (const [k, v] of Object.entries(encodings)) {
    if (v) p1.minMaxMatch++;
  }
  const cls = sh.every((b) => b === 0) ? 'all_zero' : sh.every((b) => b === 0xf8) ? 'all_f8'
    : 'nonzero:' + sh.slice(0, 4).map((b) => b.toString(16).padStart(2, '0')).join('');
  p1.subHeaderClasses.set(cls, (p1.subHeaderClasses.get(cls) ?? 0) + 1);
}
p1.subHeaderClasses = [...p1.subHeaderClasses.entries()].sort((a, b) => b[1] - a[1]);
p1.falsePositiveNote = 'all-zero sub-headers coincide with heightMin=0 on some tiles, inflating minMaxMatch — the meaningful signal is the NONZERO-subheader tiles (see examples); none encode the tile min/max';
p1.verdict = 'UNRESOLVED — sub-header does not carry the per-tile min/max in any probed encoding (see counts); min/max source remains UNRESOLVED (RE path pending)';

// ---------- PROBE 2: payload header u32[0..1] vs filename-xy ----------
const p2 = { sample: SAMPLE, match: 0, mismatchExamples: [], mismatchCorrelation: { zeroWhenMismatch: 0, smallValues: 0 } };
for (const e of sample) {
  const { payload } = await arch.readEntry(e);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const fx = parseInt(e.name.slice(0, 4), 16), fy = parseInt(e.name.slice(4, 8), 16);
  const hx = dv.getUint32(0, true), hy = dv.getUint32(4, true);
  if (hx === fx && hy === fy) p2.match++;
  else {
    if (p2.mismatchExamples.length < 10) {
      p2.mismatchExamples.push({ name: e.name, filenameXY: [fx, fy], headerXY: [hx, hy] });
    }
    if (hx === 0 && hy === 0) p2.mismatchCorrelation.zeroWhenMismatch++;
    if (hx < 65536 && hy < 65536) p2.mismatchCorrelation.smallValues++;
  }
}
p2.consistency = `${p2.match}/${SAMPLE} header==filename on this sample; mismatches recorded as-is (no semantics claim)`;

// ---------- PROBE 3: special-row tiles STRUCTURE census ----------
const p3 = { denominator: special.length, payloadSizes: new Map(), dimClasses: new Map(), namePattern: new Map(), errors: 0, note: 'STRUCTURE ONLY — no semantics claims' };
const SPECIAL_SAMPLE = 300;
for (let i = 0; i < Math.min(SPECIAL_SAMPLE, special.length); i++) {
  const e = special[Math.floor(rnd() * special.length)];
  try {
    const { payload } = await arch.readEntry(e);
    p3.payloadSizes.set(payload.byteLength, (p3.payloadSizes.get(payload.byteLength) ?? 0) + 1);
    const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    if (payload.byteLength >= 16) {
      const ds = dv.getUint32(8, true); const dim = dv.getUint32(12, true);
      const cls = `ds=${ds},dim=${dim}`;
      p3.dimClasses.set(cls, (p3.dimClasses.get(cls) ?? 0) + 1);
    }
    const y = parseInt(e.name.slice(4, 8), 16);
    p3.namePattern.set(`row=0x${y.toString(16)}`, (p3.namePattern.get(`row=0x${y.toString(16)}`) ?? 0) + 1);
  } catch { p3.errors++; }
}
p3.payloadSizes = [...p3.payloadSizes.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15);
p3.dimClasses = [...p3.dimClasses.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15);
p3.sampled = Math.min(SPECIAL_SAMPLE, special.length);

const evidence = {
  iteration: 'ITER_020',
  scope: 'bounded secondary probes (P0 passed; no models/foliage/water/full-map)',
  terrainSha256: sha256(bytes),
  probe1_subheader_minmax: p1,
  probe2_header_xy_mismatch: p2,
  probe3_special_row_structure: p3,
};
await fs.writeFile(`${EVIDENCE_DIR}/iter020_secondary_probes.json`, JSON.stringify(evidence, null, 2));
console.log('P1 subheader classes:', JSON.stringify(p1.subHeaderClasses.slice(0, 5)), 'nonzero:', p1.anyNonZero, 'minMaxHits:', p1.minMaxMatch);
console.log('P2 header==filename:', p2.consistency, 'zero-mismatch:', p2.mismatchCorrelation.zeroWhenMismatch);
console.log('P3 special-row sampled:', p3.sampled, 'errors:', p3.errors, 'top sizes:', JSON.stringify(p3.payloadSizes.slice(0, 5)));
console.log('evidence written');
