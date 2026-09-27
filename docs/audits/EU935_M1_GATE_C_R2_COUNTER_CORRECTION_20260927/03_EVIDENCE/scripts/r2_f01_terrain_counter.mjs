// R2-F01 TERRAIN SAMPLE COUNTER — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// READ-ONLY probe on the pinned terrain.bnt (PCG_9_3_5). Writes ONLY into this
// R2 package (03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json). No repo mutation.
// Method: BNT2 trailer parse — trailer [dir_off u32]["BNT2"]; at dir_off
// [count u32]; entries [name 0x0A-terminated][size u32][offset u32][crc u32]
// [flags u32]; verify the index is consumed exactly (p == filesize - 8).
import fs from 'node:fs';
import crypto from 'node:crypto';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const SRC = 'D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt';
const EXPECTED_SHA = '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990';
const EXPECTED_SIZE = 125064817;
const HEX_TDF = /^[0-9A-Fa-f]{8}\.tdf$/;

const buf = fs.readFileSync(SRC); // READ-ONLY: the file is never opened for writing
const sha = crypto.createHash('sha256').update(buf).digest('hex').toUpperCase();
if (buf.length !== EXPECTED_SIZE) throw new Error(`SIZE PIN MISMATCH: ${buf.length} != ${EXPECTED_SIZE}`);
if (sha !== EXPECTED_SHA) throw new Error(`SHA PIN MISMATCH: ${sha}`);

// --- BNT2 trailer parse ---
const n = buf.length;
const magic = buf.toString('latin1', n - 4, n);
if (magic !== 'BNT2') throw new Error(`TRAILER MAGIC MISMATCH: ${JSON.stringify(magic)}`);
const dirOff = buf.readUInt32LE(n - 8);
const count = buf.readUInt32LE(dirOff);
let p = dirOff + 4;
const entries = [];
for (let i = 0; i < count; i++) {
  const nameStart = p;
  while (p < n && buf[p] !== 0x0A) p++;
  if (p >= n) throw new Error(`INDEX OVERRUN at entry ${i}`);
  const name = buf.toString('latin1', nameStart, p);
  p++; // consume 0x0A terminator
  const size = buf.readUInt32LE(p); p += 4;
  const offset = buf.readUInt32LE(p); p += 4;
  const crc = buf.readUInt32LE(p); p += 4;
  const flags = buf.readUInt32LE(p); p += 4;
  entries.push({ name, size, offset, crc, flags });
}
const indexConsumedExactly = (p === n - 8);

// --- census over ALL names ---
const nameCounts = new Map();
for (const e of entries) nameCounts.set(e.name, (nameCounts.get(e.name) || 0) + 1);
const duplicates = [...nameCounts.entries()].filter(([, c]) => c > 1).map(([k, c]) => ({ name: k, count: c }));

const eightHexTdf = [];
let nonHexTdf = 0;
for (const e of entries) {
  if (HEX_TDF.test(e.name)) eightHexTdf.push(e.name);
  else nonHexTdf++;
}

const regular = [];
const special = [];
const sentinel = [];
const unclassified = [];
for (const e of entries) {
  const m = e.name.match(/^([0-9A-Fa-f]{4})([0-9A-Fa-f]{4})\.tdf$/);
  if (!m) { unclassified.push(e.name); continue; }
  const x = parseInt(m[1], 16);
  const y = parseInt(m[2], 16);
  if (e.name === '7ffe7ffe.tdf') { sentinel.push({ name: e.name, x, y }); continue; }
  if (y >= 0xff1a && y <= 0xffff) { special.push({ name: e.name, x, y }); continue; }
  if (x >= 0 && x <= 219 && y >= 0 && y <= 235) { regular.push({ name: e.name, x, y }); continue; }
  unclassified.push(e.name);
}
const distinctX = new Set(regular.map(t => t.x));
const distinctY = new Set(regular.map(t => t.y));
const xVals = [...distinctX].sort((a, b) => a - b);
const yVals = [...distinctY].sort((a, b) => a - b);
const specialX = [...new Set(special.map(t => t.x))].sort((a, b) => a - b);
const specialY = [...new Set(special.map(t => t.y))].sort((a, b) => a - b);

// --- two independent arithmetic paths (machine-executed, never hand-typed) ---
const pathA = regular.length * 1024;                 // 51920 * 32 * 32
const pathB = (220 * 32) * (236 * 32);               // 7040 * 7552
const falsifier = regular.length * 32;               // 51920 * 32 (the old printed total 1,664,000 is NOT this either)
const oldPrintedTotal = 1664000;

const result = {
  probe: 'R2_F01_TERRAIN_SAMPLE_COUNTER',
  run_id: 'EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927',
  node_version: process.version,
  MEASURED_QUANTITY: 'regular-tile census of the BNT2 index of terrain.bnt (PCG_9_3_5) + the two independent sample-slot arithmetic paths',
  SOURCE: SRC,
  SOURCE_HASH: sha,
  SOURCE_SIZE: buf.length,
  METHOD: 'BNT2 trailer parse: trailer [dir_off u32]["BNT2"]; at dir_off [count u32]; entries [name 0x0A-terminated][size u32][offset u32][crc u32][flags u32]; index consumed exactly p == filesize-8; census over ALL entry names',
  bnt2: {
    trailer_magic: magic,
    dir_off: dirOff,
    count: count,
    index_consumed_exactly: indexConsumedExactly,
    index_end_position: p,
    expected_end_position: n - 8,
  },
  census: {
    total_entries: entries.length,
    eight_hex_tdf_names: eightHexTdf.length,
    non_hex_tdf_names: nonHexTdf,
    regular: regular.length,
    special: special.length,
    sentinel: sentinel.length,
    unclassified: unclassified.length,
    duplicates: duplicates.length,
    regular_plus_special_plus_sentinel: regular.length + special.length + sentinel.length,
    distinct_x_regular: distinctX.size,
    distinct_y_regular: distinctY.size,
    regular_x_range: [xVals[0], xVals[xVals.length - 1]],
    regular_y_range: [yVals[0], yVals[yVals.length - 1]],
    regular_x_contiguous_0_219: (xVals.length === 220 && xVals[0] === 0 && xVals[219] === 219),
    regular_y_contiguous_0_235: (yVals.length === 236 && yVals[0] === 0 && yVals[235] === 235),
    special_x_range: specialX.length ? [specialX[0], specialX[specialX.length - 1]] : null,
    special_y_range: specialY.length ? [specialY[0], specialY[specialY.length - 1]] : null,
    sentinel_names: sentinel.map(s => s.name),
    duplicate_names: duplicates,
  },
  EXCLUSION_SET: {
    description: 'entries EXCLUDED from the regular-tile sample-slot total',
    special_y_in_ff1a_ffff: special.length,
    sentinel_7ffe7ffe: sentinel.length,
    total_excluded: special.length + sentinel.length,
  },
  arithmetic: {
    per_tile_sample_slots: 32 * 32,
    path_A_regular_times_1024: { expression: `${regular.length} * 1024`, value: pathA },
    path_B_grid_dimensions: { expression: '(220*32) * (236*32) = 7040 * 7552', value: pathB },
    both_paths_equal: pathA === pathB,
    both_paths_value: pathA,
    falsifier_regular_times_32: { expression: `${regular.length} * 32`, value: falsifier, equals_old_printed_total: falsifier === oldPrintedTotal },
    old_printed_total: oldPrintedTotal,
    old_total_derivable_from_no_valid_arithmetic: falsifier !== oldPrintedTotal && pathA !== oldPrintedTotal,
  },
  per_tile_denominator_evidence: {
    tdf_format: '32x32 uint16 LE at payload offset 64 (R1 F03 section 7.2 B; HEIGHT_DATA_OFFSET=64, 64+2048=2112)',
    region_tiles_samples: '9216/9216 samples identical for 9 region tiles = 9 * 1024 (internal consistency of the 1024-per-tile denominator)',
    committed_canon: 'M1 gate matrix "220x236 = 51,920 regular" + docs/audits/CORRECTION_LEDGER.md PE-MASTER physical name census',
  },
  expected_vs_measured: {
    total_58451: entries.length === 58451,
    regular_51920: regular.length === 51920,
    distinct_x_220: distinctX.size === 220,
    distinct_y_236: distinctY.size === 236,
    special_6530: special.length === 6530,
    sentinel_1: sentinel.length === 1,
    duplicates_0: duplicates.length === 0,
    both_paths_53166080: pathA === 53166080 && pathB === 53166080,
  },
  RESULT: null, // filled below
};
const allExpected = result.expected_vs_measured;
result.RESULT = (indexConsumedExactly && Object.values(allExpected).every(v => v === true))
  ? 'REPRODUCED: 51,920 regular tiles; 53,166,080 u16 sample slots via BOTH independent arithmetic paths; the old printed total 1,664,000 is derivable from NO valid arithmetic over these denominators (51,920*32 = 1,661,440 != 1,664,000)'
  : 'MISMATCH — HARD STOP';

fs.writeFileSync(PKG + '/03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json', JSON.stringify(result, null, 2) + '\n');
console.log('R2_F01 RESULT: ' + result.RESULT);
console.log(JSON.stringify(result.census, null, 2));
console.log(JSON.stringify(result.arithmetic, null, 2));
