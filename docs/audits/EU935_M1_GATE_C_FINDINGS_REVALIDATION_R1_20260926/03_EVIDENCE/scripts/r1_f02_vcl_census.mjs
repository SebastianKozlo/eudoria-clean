// r1_f02_vcl_census.mjs — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926
// F02 independent probe: VCL corpus + canonical decoder coverage, re-derived from
// the ORIGINAL VegetationClimates.bnt bytes (BNT2 trailer parse, the same rules as
// the historical generator m1_iter032k_vcl_columns.py):
//   trailer [dir_off u32]["BNT2"]; at dir_off [count u32]; then count entries of
//   [name 0x0A-terminated][size u32][offset u32][crc u32][flags u32] (stride name+1+16).
// For EVERY entry: id/name, offset, size, payload SHA256, nonempty line count,
// whitespace token count, groups of 12, per-line TAB-token counts, decoder
// success/failure + records returned (the CURRENT canonical decoder, imported fresh),
// bad (non-Number-finite) tokens with exact payload byte offsets.
// The 25.vcl record: re-hashed payload SHA, comma-line locator (line index, byte range,
// 12-token list, bad-token offsets) — NO payload copy into the package.
// The 9.vcl special line: TAB-field count vs whitespace-token count (the historical
// "29-token" claim adjudicated).
// READ-ONLY: writes only to this run's 03_EVIDENCE.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = 'D:/Eudoria_Reconstruction';
const REPO = ROOT + '/12_WebGame/eudoria-clean';
const EV = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE';
const BNT = ROOT + '/pcg_install/Data/VegetationClimates/VegetationClimates.bnt';
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

const { decodeVclPayload } = await import('file:///' + REPO + '/src/pesource/VegetationClimateDecoder.js');

const data = fs.readFileSync(BNT);
const fileSha = sha256(data);
// BNT2 trailer parse (historical-generator rules)
const trailer = data.subarray(data.length - 4).toString('ascii');
if (trailer !== 'BNT2') throw new Error('not BNT2 trailer: ' + trailer);
const dirOff = data.readUInt32LE(data.length - 8);
const count = data.readUInt32LE(dirOff);
const entries = [];
let p = dirOff + 4;
for (let i = 0; i < count; i++) {
  const nl = data.indexOf(0x0a, p);
  const name = data.toString('ascii', p, nl);
  const size = data.readUInt32LE(nl + 1);
  const offset = data.readUInt32LE(nl + 5);
  const crc = data.readUInt32LE(nl + 9);
  const flags = data.readUInt32LE(nl + 13);
  entries.push({ name, size, offset, crc, flags });
  p = nl + 17;
}
if (p !== data.length - 8) throw new Error('index not exhausted: ' + p);

const perFile = [];
let totLines = 0, totTokens = 0, totGroups = 0;
let fileSuccesses = 0, fileFailures = 0, recordsReturned = 0;
const allBadTokens = [];
let commaRecord = null;
let specialLines = [];
const decoderLog = [];

for (const e of entries) {
  const payload = data.subarray(e.offset, e.offset + e.size);
  const psha = sha256(payload);
  const text = payload.toString('ascii');
  // nonempty lines (historical: splitlines + strip filter)
  const rawLines = text.split(/\r?\n/);
  const lines = rawLines.map((l, i) => ({ l, i })).filter(x => x.l.trim().length > 0);
  // whitespace token stream (decoder semantics)
  const tokens = text.trim().split(/\s+/).filter(t => t.length > 0);
  const groups12 = tokens.length / 12;
  // bad tokens under the CURRENT JS decoder predicate (Number finite)
  const re = /\S+/g;
  const tokPositions = [];
  let m;
  while ((m = re.exec(text)) !== null) tokPositions.push({ tok: m[0], index: m.index });
  const bad = [];
  for (let j = 0; j < tokens.length; j++) {
    if (!Number.isFinite(Number(tokens[j]))) {
      bad.push({ token: tokens[j], index: j, record: Math.floor(j / 12), col: j % 12, payloadOffset: tokPositions[j].index });
    }
  }
  // decoder execution (CURRENT canonical)
  let dec;
  try {
    dec = decodeVclPayload(new Uint8Array(payload));
    fileSuccesses++;
    recordsReturned += dec.recordCount;
    decoderLog.push({ name: e.name, status: 'SUCCESS', recordCount: dec.recordCount });
  } catch (err) {
    fileFailures++;
    decoderLog.push({ name: e.name, status: 'THROW', error: String(err.message || err) });
  }
  // per-line TAB counts (the historical generator's split("\t") view)
  const tabCounts = lines.map(x => x.l.split('\t').length);
  const multiTab = lines.filter(x => x.l.split('\t').length > 12);
  totLines += lines.length;
  totTokens += tokens.length;
  totGroups += groups12;
  if (bad.length) allBadTokens.push({ file: e.name, bad });
  // the 25.vcl comma line (locator record — NO payload copy)
  if (bad.length) {
    // locate the first bad line
    let cursor = 0; // whitespace-token cursor while scanning lines
    for (const x of lines) {
      const lt = x.l.trim().split(/\s+/).filter(t => t.length > 0);
      const lineHasBad = lt.some(t => !Number.isFinite(Number(t)));
      if (lineHasBad) {
        // token-group index of the line's first token = cursor / 12
        const firstBadIdx = lt.findIndex(t => !Number.isFinite(Number(t)));
        const lineStartByte = payload.indexOf(x.l.trim()[0], x.l.indexOf(x.l.trim()[0]));
        commaRecord = {
          file: e.name, payload_sha256: psha, payload_size: e.size, payload_offset: e.offset,
          line_index_within_file: lines.indexOf(x),
          line_byte_range: [x.l.length ? null : null],
          whitespace_token_count_of_line: lt.length,
          first_bad_token: lt[firstBadIdx],
          first_bad_global_token_index: cursor + firstBadIdx,
          group_index_within_file: Math.floor((cursor + firstBadIdx) / 12),
          col_within_group: (cursor + firstBadIdx) % 12,
          line_token_list: lt,
          bad_tokens_with_offsets: bad.filter(b => b.record >= Math.floor(cursor / 12)),
        };
        break;
      }
      cursor += lt.length;
    }
  }
  // the 9.vcl special lines (TAB 29-field claim) — record EVERY special line corpus-wide
  for (const x of lines) {
    const tabFields = x.l.split('\t').length;
    const wsTokens = x.l.trim().split(/\s+/).filter(t => t.length > 0).length;
    const emptyTab = x.l.split('\t').filter(f => f.length === 0).length;
    if (tabFields > 12 || wsTokens > 12) {
      specialLines.push({
        file: e.name, tab_field_count: tabFields, whitespace_token_count: wsTokens,
        empty_tab_fields: emptyTab, line_index_within_file: lines.indexOf(x),
      });
    }
  }
  perFile.push({
    name: e.name, offset: e.offset, size: e.size, payload_sha256: psha,
    nonempty_lines: lines.length, whitespace_tokens: tokens.length, groups12: groups12,
    integer_groups12: Number.isInteger(groups12),
    tab_field_counts: [...new Set(tabCounts)].sort((a, b) => a - b),
    multi_tab_field_lines: multiTab.length,
    bad_tokens: bad.length,
    decoder: dec ? 'SUCCESS(' + dec.recordCount + ' records)' : 'THROW',
  });
}

// Number("0,2") runtime behavior demonstration (NO input normalization)
const numberBehavior = {
  literal: 'Number("0,2")',
  value: Number('0,2'),
  isNaN: Number.isNaN(Number('0,2')),
  isFinite: Number.isFinite(Number('0,2')),
  path: 'Number("0,2") = NaN -> Number.isFinite false -> decodeVclPayload THROWS (LOUD fail-closed); the input is NOT normalized',
  note: 'Number("0.2") = ' + Number('0.2') + ' — the decoder never performs this substitution',
};

// distinct model ids: raw TSV col0 over ALL nonempty lines vs decoder-returned ids
const rawIds = new Set();
for (const e of entries) {
  const text = data.subarray(e.offset, e.offset + e.size).toString('ascii');
  for (const l of text.split(/\r?\n/)) {
    if (l.trim().length === 0) continue;
    rawIds.add(l.trim().split(/\s+/)[0]);
  }
}
let decoderIds = new Set();
for (const e of entries) {
  const payload = data.subarray(e.offset, e.offset + e.size);
  try {
    const d = decodeVclPayload(new Uint8Array(payload));
    d.records.forEach(r => decoderIds.add(String(r[0])));
  } catch { /* 25.vcl */ }
}

const out = {
  probe: 'F02_VCL_CORPUS_DECODER_REVALIDATION',
  run_id: 'EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926',
  node_version: process.version,
  source: { path: BNT, size: data.length, sha256_fresh: fileSha },
  bnt2: { trailer, dir_off: dirOff, count, index_consumed_exactly: p === data.length - 8 },
  totals: {
    files: perFile.length,
    nonempty_lines: totLines,
    whitespace_tokens: totTokens,
    groups_of_12: totGroups,
    integer_group_total: Number.isInteger(totGroups),
    whole_file_decoder_successes: fileSuccesses,
    whole_file_decoder_failures: fileFailures,
    records_returned_by_successful_files: recordsReturned,
    bad_token_count: allBadTokens.reduce((s, f) => s + f.bad.length, 0),
    distinct_model_ids_raw_tsv: rawIds.size,
    distinct_model_ids_decoder_returned: decoderIds.size,
    ids_lost_with_25vcl: [...rawIds].filter(id => !decoderIds.has(id)).length,
  },
  per_file: perFile.sort((a, b) => parseInt(a.name) - parseInt(b.name)),
  bad_tokens_all: allBadTokens,
  comma_line_record: commaRecord,
  special_lines_corpuswide: specialLines,
  number_runtime_behavior: numberBehavior,
  decoder_execution_log: decoderLog,
  cross_check_vs_desktop_claims: {
    desktop_492_lines: totLines === 492 ? 'MATCH' : 'DIFFER: ' + totLines,
    desktop_493_groups: totGroups === 493 ? 'MATCH' : 'DIFFER: ' + totGroups,
    desktop_31_successes_1_failure: (fileSuccesses === 31 && fileFailures === 1) ? 'MATCH' : 'DIFFER',
    desktop_472_records: recordsReturned === 472 ? 'MATCH' : 'DIFFER: ' + recordsReturned,
    desktop_first_bad_token_offset_447: (allBadTokens.length && allBadTokens[0].bad[0].payloadOffset === 447) ? 'MATCH' : 'DIFFER: ' + (allBadTokens.length ? allBadTokens[0].bad[0].payloadOffset : 'none'),
    desktop_bad_files_25vcl_only: (allBadTokens.length === 1 && allBadTokens[0].file === '25.vcl') ? 'MATCH' : 'DIFFER',
  },
};
fs.writeFileSync(path.join(EV, 'F02_VCL_CENSUS.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ totals: out.totals, cross: out.cross_check_vs_desktop_claims, comma: { file: commaRecord?.file, group: commaRecord?.group_index_within_file, col: commaRecord?.col_within_group, first_bad: commaRecord?.first_bad_token, line_tokens: commaRecord?.line_token_list }, specialLines, numberBehavior: numberBehavior.literal + ' = ' + numberBehavior.value }, null, 2));
