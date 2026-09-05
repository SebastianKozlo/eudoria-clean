// probe_r2_helpers.cjs — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3 stage-local probe.
//
// WHAT THIS EXECUTES: ONLY the literal pure helper declarations extracted from
// the HASH-PINNED R2 source (00_CONTROL/control_r2.cjs of
// PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054, SHA256 pinned below). The
// historical R2 script itself is NOT executed; no other line of it is loaded.
// The two defect-relevant declarations (adler32, fnv1a) plus the crc32
// declaration and its CRC_T table construction are evaluated inside a fresh
// vm context (no filesystem/network inside the context).
//
// Corrected cross-language primitives (independent of Python):
//   adlerCorrected : s1=1, s2=0, mod 65521, (s2<<16)|s1 — plain Number
//                    arithmetic (exact: all intermediates < 2^53).
//   fnvCorrected   : BigInt exact multiply mod 2^32 (float Number is
//                    insufficient — that insufficiency is the R2 defect).
//
// READ-ONLY sources: the two Models.bnt containers + the R2 source file.
// WRITES: only 01_RAW/R2_HELPER_PROBE.json (path passed as argv[2]).
'use strict';
const fs = require('fs'), crypto = require('crypto'), vm = require('vm');

const R2_SRC = 'D:/Eudoria_Reconstruction/99_Audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/00_CONTROL/control_r2.cjs';
const R2_SRC_SHA256 = '666c378da43dd23b961252bdc091baf9b2c7df6b32268d002ed916b20018b59e';
const BNT_953 = 'D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt';
const BNT_2003 = 'D:/Eudoria_Reconstruction/01_Original_Files/BNT_Models/Models.bnt';
const OUT = process.argv[2];
const sha = b => crypto.createHash('sha256').update(b).digest('hex');

// ---------- 1. hash-pin verification + literal extraction ----------
const srcBuf = fs.readFileSync(R2_SRC);
const srcSha = sha(srcBuf);
if (srcSha !== R2_SRC_SHA256) {
  console.error('FATAL: R2 source hash-pin mismatch: ' + srcSha);
  process.exit(2);
}
const lines = srcBuf.toString('utf8').split(/\r?\n/);
function extractBlock(prefix) {
  // unique line-prefix start; accumulate lines until braces balance (handles the
  // multi-line crc32 declaration); abort if the prefix is not unique
  const starts = [];
  for (let i = 0; i < lines.length; i++) if (lines[i].startsWith(prefix)) starts.push(i);
  if (starts.length !== 1) { console.error('FATAL: prefix not unique: ' + prefix + ' at ' + starts); process.exit(2); }
  let acc = lines[starts[0]];
  let depth = (acc.match(/{/g) || []).length - (acc.match(/}/g) || []).length;
  let j = starts[0];
  while (depth > 0) {
    j += 1;
    if (j >= lines.length) { console.error('FATAL: unbalanced block for ' + prefix); process.exit(2); }
    acc += '\n' + lines[j];
    depth += (lines[j].match(/{/g) || []).length - (lines[j].match(/}/g) || []).length;
  }
  return acc;
}
const decl = {
  crc32_fn: extractBlock('function crc32('),
  crc_table_const: extractBlock('const CRC_T = new Uint32Array(256);'),
  crc_table_fill: extractBlock('for (let n = 0; n < 256'),
  adler32: extractBlock('function adler32('),
  fnv1a: extractBlock('function fnv1a('),
};
const extracted = [decl.crc32_fn, decl.crc_table_const, decl.crc_table_fill, decl.adler32, decl.fnv1a];

// ---------- 2. execute ONLY the extracted literals in a fresh vm context ----------
const ctx = {};
vm.createContext(ctx);
for (const snippet of extracted) vm.runInContext(snippet, ctx, { timeout: 1000 });
const r2Adler = b => ctx.adler32(b);
const r2Fnv = b => ctx.fnv1a(b);
const r2Crc32 = b => ctx.crc32(b);

// ---------- 3. corrected Node primitives (cross-language oracle legs) ----------
function adlerCorrected(b) { // RFC1950: s1=1, s2=0, mod 65521, (s2<<16)|s1
  let s1 = 1, s2 = 0;
  for (let i = 0; i < b.length; i++) {
    s1 = (s1 + b[i]) % 65521;
    s2 = (s2 + s1) % 65521;
  }
  return ((s2 << 16) | s1) >>> 0;
}
function fnvCorrected(b) { // RFC9923: exact BigInt multiply mod 2^32
  let h = 0x811C9DC5n;
  for (let i = 0; i < b.length; i++) h = ((h ^ BigInt(b[i])) * 0x01000193n) & 0xFFFFFFFFn;
  return Number(h);
}

// ---------- 4. KAT vectors (same set as r3_primitives.py) ----------
const KAT = [
  ['V01_empty', ''],
  ['V02_a', '61'],
  ['V03_hello', '68656c6c6f'],
  ['V04_foobar', '666f6f626172'],
  ['V05_wikipedia', '57696b697065646961'],
  ['V06_123456789', '313233343536373839'],
  ['V07_name_548296', '3534383239362e6e6966'],
  ['V08_zero_byte', '00'],
  ['V09_ff_byte', 'ff'],
  ['V10_range256', Array.from({ length: 256 }, (_, i) => i.toString(16).padStart(2, '0')).join('')],
  ['V11_ff4096', 'ff'.repeat(4096)],
  ['V12_zero4096', '00'.repeat(4096)],
  ['V13_a10', '61'.repeat(10)],
  ['V14_incremental_split', '68656c6c6f'],
];
const kat = KAT.map(([id, hx]) => {
  const b = Buffer.from(hx, 'hex');
  return { id, len: b.length,
    r2_adler: r2Adler(b), r2_fnv: r2Fnv(b) >>> 0, r2_crc32: r2Crc32(b) >>> 0,
    corrected_adler: adlerCorrected(b), corrected_fnv: fnvCorrected(b) };
});

// ---------- 5. BNT2 parse (read-only, bounds-checked) ----------
function parseBnt(p) {
  const b = fs.readFileSync(p);
  const start = b.readUInt32LE(b.length - 8);
  if (!(start > 0 && start < b.length - 8)) throw new Error('bad index start ' + p);
  const count = b.readUInt32LE(start);
  let pos = start + 4;
  const entries = [];
  const seen = new Set();
  for (let i = 0; i < count; i++) {
    const end = b.indexOf(10, pos);
    if (end < 0 || end >= b.length - 8) throw new Error('bad name terminator at ' + i);
    const name = b.subarray(pos, end).toString('ascii');
    const size = b.readUInt32LE(end + 1), off = b.readUInt32LE(end + 5);
    const c = b.readUInt32LE(end + 9), d = b.readUInt32LE(end + 13);
    if (seen.has(name)) throw new Error('duplicate name ' + name);
    seen.add(name);
    if (off + size > start) throw new Error('payload overruns index ' + name);
    entries.push({ name, size, off, c, d, nameBytes: b.subarray(pos, end), bytes: b.subarray(off, off + size) });
    pos = end + 17;
  }
  if (pos !== b.length - 8) throw new Error('index consumption not exact ' + p);
  if (seen.size !== count) throw new Error('count mismatch ' + p);
  return { sha256: sha(b), size: b.length, count, entries };
}

// ---------- 6. per-entry value computation across both corpora ----------
function censusEntries(container) {
  const rows = [];
  for (const e of container.entries) {
    const nb = e.nameBytes;
    const szLe = Buffer.alloc(4); szLe.writeUInt32LE(e.size, 0);
    const nameLf = Buffer.concat([nb, Buffer.from([0x0A])]);
    const nameSz = Buffer.concat([nb, szLe]);
    const szName = Buffer.concat([szLe, nb]);
    const payload = e.bytes;
    rows.push([
      e.name,
      r2Adler(nb) >>> 0,              // 1: R2 literal adler32(name)
      r2Fnv(nb) >>> 0,                // 2: R2 literal fnv1a(name)
      r2Crc32(nb) >>> 0,              // 3: R2 literal crc32(name)
      r2Adler(payload) >>> 0,         // 4: R2 literal adler32(payload)
      r2Crc32(payload) >>> 0,        // 5: R2 literal crc32(payload)
      r2Crc32(nameLf) >>> 0,          // 6: R2 literal crc32(name+0x0A)
      r2Crc32(nameSz) >>> 0,          // 7: R2 literal crc32(name+u32size_le)
      r2Crc32(szName) >>> 0,          // 8: R2 literal crc32(u32size_le+name)
      adlerCorrected(nb),             // 9: corrected Node adler32(name)
      adlerCorrected(payload),        // 10: corrected Node adler32(payload)
      fnvCorrected(nb),               // 11: corrected Node BigInt fnv1a(name)
      e.size, e.off, e.c, e.d,        // 12-15: size/off/c/d (identity join)
    ]);
  }
  return rows;
}

const t0 = Date.now();
const c953 = parseBnt(BNT_953);
const c2003 = parseBnt(BNT_2003);
const t1 = Date.now();
const rows953 = censusEntries(c953);
const t2 = Date.now();
const rows2003 = censusEntries(c2003);
const t3 = Date.now();

const result = {
  provenance: {
    script: '00_CONTROL/probe_r2_helpers.cjs',
    run: 'PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627',
    r2_source: R2_SRC, r2_source_sha256: srcSha,
    r2_source_sha_pin_verified: srcSha === R2_SRC_SHA256,
    extraction: extracted,
    extraction_method: 'unique line-prefix match on the hash-pinned source; executed ONLY these literal pure declarations inside a fresh vm context (no fs/net in context); the historical R2 script was NOT executed',
    executed_declarations: ['function crc32', 'const CRC_T', 'CRC_T fill loop', 'function adler32', 'function fnv1a'],
    corrected_node_primitives: {
      adlerCorrected: 's1=1, s2=0, mod 65521, (s2<<16)|s1 — Number arithmetic (exact, intermediates < 2^53)',
      fnvCorrected: 'BigInt exact multiply mod 2^32 (float Number multiply is the R2 defect — insufficient)',
    },
    read_only_sources: [BNT_953, BNT_2003, R2_SRC],
    writes: [OUT],
  },
  physical_sources: [
    { path: BNT_953, size: c953.size, sha256: c953.sha256, entries: c953.count },
    { path: BNT_2003, size: c2003.size, sha256: c2003.sha256, entries: c2003.count },
  ],
  kat_vectors: kat,
  census: {
    column_order: ['file', 'r2_adler_name', 'r2_fnv_name', 'r2_crc32_name', 'r2_adler_payload',
      'r2_crc32_payload', 'r2_crc32_name_lf', 'r2_crc32_name_szle', 'r2_crc32_szle_name',
      'node_adler_name_corrected', 'node_adler_payload_corrected', 'node_fnv_name_bigint_corrected',
      'size', 'off', 'c', 'd'],
    pcg_953: { n: rows953.length, rows: rows953 },
    era_2003: { n: rows2003.length, rows: rows2003 },
  },
  timing_ms: { parse: t1 - t0, census_953: t2 - t1, census_2003: t3 - t2, total: t3 - t0 },
};
fs.writeFileSync(OUT, JSON.stringify(result));
console.log(JSON.stringify({
  output: OUT, r2_source_sha_pin_verified: true,
  entries: { pcg_953: rows953.length, era_2003: rows2003.length },
  kat_fail_examples: kat.filter(k => k.r2_adler !== k.corrected_adler || k.r2_fnv !== k.corrected_fnv).slice(0, 6),
  timing_ms: result.timing_ms,
}));
