// R2-F02 VCL REVIEW ARITHMETIC ERRATUM — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// Recomputes the pasted-review BAD equation, re-derives the valid relations from
// the R1 census artifact PER_FILE rows (never trusting the totals block), and
// runs the bounded repo search for the bad-equation text variants.
// Modifies NOTHING: original payloads, the decoder, the census JSON, comma
// behavior are untouched. No original-client comma semantics are inferred.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { execSync } from 'node:child_process';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const R1 = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926';
const CENSUS_PATH = R1 + '/03_EVIDENCE/F02_VCL_CENSUS.json';
const ITER032K_PATH = R1 + '/03_EVIDENCE/F02_ITER032K_RERUN_vcl_columns.json';

const census = JSON.parse(fs.readFileSync(CENSUS_PATH, 'utf8'));
const iter = JSON.parse(fs.readFileSync(ITER032K_PATH, 'utf8'));

// --- re-derive from PER_FILE rows (raw rows; the totals block is NOT trusted) ---
const perFile = census.per_file;
const sumLines = perFile.reduce((a, f) => a + f.nonempty_lines, 0);
const sumTokens = perFile.reduce((a, f) => a + f.whitespace_tokens, 0);
const sumGroups = perFile.reduce((a, f) => a + f.groups12, 0);
const sumSuccessRecords = perFile.reduce((a, f) => {
  const m = /^SUCCESS\((\d+) records\)$/.exec(f.decoder);
  return a + (m ? parseInt(m[1], 10) : 0);
}, 0);
const successFiles = perFile.filter(f => f.decoder.startsWith('SUCCESS')).length;
const throwFiles = perFile.filter(f => f.decoder === 'THROW').length;

// cross-check the decoder_execution_log (independent second source for 472)
const logRecords = census.decoder_execution_log.reduce((a, e) => a + (e.recordCount || 0), 0);
const logSuccess = census.decoder_execution_log.filter(e => e.status === 'SUCCESS').length;
const logThrow = census.decoder_execution_log.filter(e => e.status === 'THROW').length;

const v25 = perFile.find(f => f.name === '25.vcl');
const v25Lines = v25.nonempty_lines, v25Tokens = v25.whitespace_tokens, v25Groups = v25.groups12;
// 25.vcl has exactly ONE non-numeric (comma) line: its bad-token rows are all
// record 9; the census bad_tokens_all shows all 6 bad tokens in one line.
const v25BadTokenRows = new Set(census.bad_tokens_all[0].bad.map(b => b.record));
const v25CommaLines = v25BadTokenRows.size; // = 1
const v25NumericLines = v25Lines - v25CommaLines; // = 20

// the continuation line: 9.vcl has groups12 > nonempty_lines (12 vs 11)
const continuationFiles = perFile.filter(f => f.groups12 > f.nonempty_lines);
const extraGroups = sumGroups - sumLines; // continuation extra groups beyond one-per-line

// numeric_rows_12cols from the historical census re-run artifact
const numericRows = iter.measured.numeric_rows_12cols;
const totalRows = iter.measured.total_rows_alltokens;

// --- the relations (all machine-executed) ---
const badLHS = 491 * 12 + 24 + 252;                       // the pasted-review LHS
const relGroup = (491 + 1 + 1) * 12;                      // group-level correct total
const relRecords = sumGroups - v25Groups;                 // 493 - 21 = 472
const relFile = 472 * 12 + 252;                           // file-level correct total
const overcount = badLHS - 5916;
const decomp240 = v25NumericLines * 12;                   // 20 * 12 = 240
const decomp12 = 12;                                      // continuation first group
const decompSum = decomp240 + decomp12;

// --- bounded repo search for the bad-equation text variants ---
const tracked = execSync('git ls-files', { cwd: REPO, maxBuffer: 1e8 }).toString().split('\n').filter(Boolean);
const variants = ['491x12 + 24 + 252', '491*12 + 24 + 252', '491 \u00d7 12 + 24'];
const flexRe = /491\s*[x*\u00d7]\s*12\s*\+\s*24/;
const hits = [];
let scanned = 0, bytes = 0, skipped = [];
for (const rel of tracked) {
  let b;
  try { b = fs.readFileSync(REPO + '/' + rel); } catch (e) { skipped.push(rel); continue; }
  scanned++; bytes += b.length;
  const s = b.toString('latin1');
  for (const v of variants) {
    const idx = s.indexOf(v);
    if (idx !== -1) hits.push({ file: rel, variant: v, index: idx, context: s.slice(Math.max(0, idx - 80), idx + 120) });
  }
  const m = flexRe.exec(s);
  if (m) hits.push({ file: rel, variant: 'REGEX ' + flexRe.source, index: m.index, context: s.slice(Math.max(0, m.index - 80), m.index + 120) });
}

const result = {
  probe: 'R2_F02_VCL_REVIEW_ARITHMETIC_ERRATUM',
  run_id: 'EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927',
  node_version: process.version,
  sources: {
    census: { path: '03_EVIDENCE/F02_VCL_CENSUS.json (R1 predecessor package)', sha256: crypto.createHash('sha256').update(fs.readFileSync(CENSUS_PATH)).digest('hex').toUpperCase() },
    iter032k: { path: '03_EVIDENCE/F02_ITER032K_RERUN_vcl_columns.json (R1 predecessor package)', sha256: crypto.createHash('sha256').update(fs.readFileSync(ITER032K_PATH)).digest('hex').toUpperCase() },
  },
  per_file_rederivation: {
    method: 'sums computed from the per_file array rows; the JSON totals block was NOT used',
    files: perFile.length,
    sum_lines: sumLines,
    sum_tokens: sumTokens,
    sum_groups: sumGroups,
    sum_success_records: sumSuccessRecords,
    success_files: successFiles,
    throw_files: throwFiles,
    cross_check_decoder_execution_log: { records: logRecords, success: logSuccess, throw: logThrow, records_match: logRecords === sumSuccessRecords },
    v25: { lines: v25Lines, tokens: v25Tokens, groups: v25Groups, comma_lines: v25CommaLines, numeric_lines: v25NumericLines },
    continuation_line: {
      files_with_groups_gt_lines: continuationFiles.map(f => ({ name: f.name, lines: f.nonempty_lines, groups: f.groups12 })),
      extra_groups_beyond_one_per_line: extraGroups,
      note: '9.vcl line 1 (29 tab fields = 12 numeric + 5 empty + 12 numeric) = 24 whitespace tokens = 2 groups; its FIRST group is one of the 491 numeric rows, its SECOND is the +1 extra',
    },
    numeric_rows_12cols: { value: numericRows, total_rows_alltokens: totalRows, excluded_rows: totalRows - numericRows, only_excluded_row: 'the 25.vcl comma line (float() ValueError path silently skips it)' },
  },
  relations: {
    bad_equation: { statement: '491x12 + 24 + 252 = 5916 (the human-pasted PE_MASTER_REVIEW relay)', LHS: badLHS, RHS_claimed: 5916, LHS_equals_RHS: badLHS === 5916, verdict: 'FALSE — the LHS is ' + badLHS },
    correct_group_level: { expression: '(491+1+1)*12', value: relGroup, equals_sum_tokens: relGroup === sumTokens, decomposition: '491 numeric lines (the continuation line counted once via its first 12 tokens) + 1 continuation extra group + 1 comma group = 493 groups' },
    correct_records: { expression: '493 - 21', value: relRecords, equals_sum_success_records: relRecords === sumSuccessRecords },
    correct_file_level: { expression: '472*12 + 252', value: relFile, equals_sum_tokens: relFile === sumTokens },
    double_count_decomposition: {
      overcount: overcount,
      overcount_equals_252: overcount === 252,
      term_240: { value: decomp240, meaning: "25.vcl's 20 numeric lines x 12 = 240 tokens, ALREADY inside 491x12 (25.vcl's 20 numeric lines are among the 491) — the +252 term re-adds ALL 21 of 25.vcl's groups" },
      term_12: { value: decomp12, meaning: "the 9.vcl continuation line's FIRST group = 12 tokens, ALREADY inside 491x12 (the continuation line is one of the 491 numeric rows) — the +24 term re-adds BOTH its groups (only the second is new)" },
      sum: decompSum,
      sum_equals_overcount: decompSum === overcount,
    },
    population_identities: {
      lines_492: sumLines === 492,
      tokens_5916: sumTokens === 5916,
      groups_493: sumGroups === 493,
      records_472: sumSuccessRecords === 472,
      numeric_rows_491: numericRows === 491,
      groups_eq_numeric_plus_extra_plus_comma: (numericRows + extraGroups + v25CommaLines) === sumGroups,
    },
  },
  repo_search: {
    search_space: 'ALL tracked repo files (git ls-files) at HEAD cc747df worktree, read as bytes, latin1-decoded for literal search',
    tracked_files: tracked.length,
    files_scanned: scanned,
    bytes_scanned: bytes,
    files_unreadable: skipped,
    variants: variants,
    flexible_regex: flexRe.source,
    hits: hits,
    hits_count: hits.length,
    result: hits.length === 0 ? '0 hits — the bad equation existed ONLY in the human-pasted PE_MASTER_REVIEW chat relay, never in a repo file' : 'HITS FOUND — review before any correction',
  },
  unaffected_claims: 'the raw census 32 files / 492 lines / 5,916 tokens / 493 groups / 6 bad tokens / 31 successes / 1 THROW / 472 records and ALL R1 package contents are UNCHANGED and valid; no comma normalization, no parser change, no original-client comma-semantics inference',
  RESULT: null,
};
const ok = result.relations.population_identities && Object.values(result.relations.population_identities).every(v => v === true);
result.RESULT = (ok && badLHS === 6168 && overcount === 252 && decompSum === 252 && hits.length === 0)
  ? 'REPRODUCED: the pasted-review equation LHS = 6,168 != 5,916 (FALSE); the correct relations (491+1+1)x12 = 5,916 and 472x12+252 = 5,916 both verified; the raw census 492/5,916/493/472 UNCHANGED and valid; 0 repo hits for the bad equation'
  : 'MISMATCH — review required';

fs.writeFileSync(PKG + '/03_EVIDENCE/R2_F02_VCL_ARITHMETIC.json', JSON.stringify(result, null, 2) + '\n');
console.log('R2_F02 RESULT: ' + result.RESULT);
console.log('sums: lines=' + sumLines + ' tokens=' + sumTokens + ' groups=' + sumGroups + ' successRecords=' + sumSuccessRecords + ' (log cross-check ' + logRecords + ')');
console.log('25.vcl: lines=' + v25Lines + ' tokens=' + v25Tokens + ' groups=' + v25Groups + ' numericLines=' + v25NumericLines);
console.log('bad LHS=' + badLHS + ' ; (491+1+1)*12=' + relGroup + ' ; 472*12+252=' + relFile + ' ; overcount=' + overcount + ' (240+12=' + decompSum + ')');
console.log('repo search: scanned=' + scanned + ' files / ' + bytes + ' bytes / hits=' + hits.length);
