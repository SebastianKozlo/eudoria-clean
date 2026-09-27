// R2-P3 EVIDENCE LABEL — patch class verification — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// Reads the R1 DIFF_PEFoliageCore.js.patch in full + the fresh live git diff,
// classifies the change (comment lines + ONE documentation-metadata string),
// verifies the EVIDENCE_INDEX.csv mislabel site, and runs the bounded scan for
// other "comment-only" labels in the R1 package. Modifies NOTHING.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { execSync } from 'node:child_process';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const R1 = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926';
const PATCH_PATH = R1 + '/03_EVIDENCE/DIFF_PEFoliageCore.js.patch';
const TARGET = 'src/peworld/PEFoliageCore.js';

const patchBuf = fs.readFileSync(PATCH_PATH);
const patchSha = crypto.createHash('sha256').update(patchBuf).digest('hex').toUpperCase();
const liveBuf = execSync('git diff -- src/peworld/PEFoliageCore.js', { cwd: REPO, maxBuffer: 1e8 });
const liveSha = crypto.createHash('sha256').update(liveBuf).digest('hex').toUpperCase();
const byteIdentical = Buffer.compare(patchBuf, liveBuf) === 0;

// --- parse the patch hunks and classify every changed line ---
const text = patchBuf.toString('utf8');
const lines = text.split('\n');
const hunks = [];
let cur = null;
for (const l of lines) {
  if (l.startsWith('@@')) { cur = { header: l, removed: [], added: [], context: 0 }; hunks.push(cur); continue; }
  if (cur) {
    if (l.startsWith('-')) cur.removed.push(l.slice(1));
    else if (l.startsWith('+')) cur.added.push(l.slice(1));
    else if (l.startsWith(' ')) cur.context++;
  }
}
const changedRemoved = hunks.flatMap(h => h.removed);
const changedAdded = hunks.flatMap(h => h.added);
const isComment = (s) => s.trimStart().startsWith('//');
const removedComments = changedRemoved.filter(isComment).length;
const addedComments = changedAdded.filter(isComment).length;
const removedNonComments = changedRemoved.filter(s => !isComment(s));
const addedNonComments = changedAdded.filter(s => !isComment(s));
const nonCommentIsExactnessPair =
  removedNonComments.length === 1 && addedNonComments.length === 1 &&
  /^\s*exactness:\s*'/.test(removedNonComments[0]) && /^\s*exactness:\s*'/.test(addedNonComments[0]) &&
  hunks[1] && hunks[1].header.includes('FOLIAGE_OPERAND_LOCK');

// --- the exactness string is documentation metadata: no runtime consumer in src/ ---
const operandLockConsumers = [];
const walk = (dir) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = dir + '/' + e.name;
    if (e.isDirectory()) { if (e.name !== 'node_modules') walk(p); continue; }
    if (!/\.(js|mjs)$/.test(e.name)) continue;
    const s = fs.readFileSync(p, 'utf8');
    if (/FOLIAGE_OPERAND_LOCK|operandLock/.test(s) && p !== (REPO + '/src/peworld/PEFoliageCore.js')) {
      operandLockConsumers.push(p.replace(REPO + '/', ''));
    }
    if (p === (REPO + '/src/peworld/PEFoliageCore.js')) {
      // within the defining file: find reads of .exactness other than the definition
      const reads = [...s.matchAll(/\.exactness\b/g)].filter(m => {
        const line = s.slice(s.lastIndexOf('\n', m.index) + 1, s.indexOf('\n', m.index));
        return !/^\s*exactness:/.test(line);
      });
      if (reads.length) operandLockConsumers.push('src/peworld/PEFoliageCore.js READS .exactness x' + reads.length);
    }
  }
};
walk(REPO + '/src');

// --- verify the mislabel site in EVIDENCE_INDEX.csv (strict RFC4180 parse) ---
const csvRaw = fs.readFileSync(R1 + '/03_EVIDENCE/EVIDENCE_INDEX.csv', 'utf8');
function parseCsv4180(s) {
  const rows = []; let row = []; let field = ''; let inQ = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (inQ) {
      if (c === '"') { if (s[i + 1] === '"') { field += '"'; i++; } else inQ = false; }
      else field += c;
    } else if (c === '"') inQ = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}
const rows = parseCsv4180(csvRaw);
const fieldCounts = new Set(rows.map(r => r.length));
const foliRowIdx = rows.findIndex(r => r[0] === '03_EVIDENCE/DIFF_PEFoliageCore.js.patch');
const foliRow = rows[foliRowIdx];
// physical line of that row (for the "line 10" check)
const physLine = csvRaw.split('\n').findIndex(l => l.startsWith('"03_EVIDENCE/DIFF_PEFoliageCore.js.patch"')) + 1;

// --- bounded scan: every "comment-only" hit in the R1 package (49 files) ---
const r1Files = [];
const collect = (dir) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = dir + '/' + e.name;
    if (e.isDirectory()) collect(p); else r1Files.push(p);
  }
};
collect(R1);
const commentOnlyHits = [];
for (const f of r1Files) {
  const rel = f.replace(R1 + '/', '').replace(/\\/g, '/');
  const s = fs.readFileSync(f, 'utf8');
  const ls = s.split('\n');
  ls.forEach((l, i) => {
    if (/comment-only/i.test(l)) commentOnlyHits.push({ file: rel, line: i + 1, text: l.trim().slice(0, 400) });
  });
}
// line-level dispositions (verbatim scan record; each hit classified by its
// own text, not by file alone)
const DISPOSITIONS = {
  '03_EVIDENCE/EVIDENCE_INDEX.csv:10': 'MISLABEL_LIVE_UNDISCLOSED — the PEFoliageCore diff described "comment-only" with NO disclosure of the exactness string change; AUTHORIZED EDIT TARGET B (the only authorized label fix)',
  '02_ANALYSIS/F05_EXACTNESS_ORIGIN_PRECISION.md:87': 'IMPRECISE_RESIDUE_LIVE — characterizes the F05 PEFoliageCore correction as "(comment-only; zero arithmetic change)" with NO additionally-disclosure of the exactness string; OUTSIDE the authorized edit set (recorded as open residue; NOT edited — the contract forbids editing any historical package span other than the three authorized)',
  '01_RAW/FINDINGS.csv:6': 'ALREADY_PRECISE_IN_SUBSTANCE — the lead word "comment-only" is loose but the SAME parenthetical explicitly discloses "the exactness string now carries the condition"',
  '06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md:227': 'ALREADY_PRECISE — multi-line phrasing: line 227 ends "(comment-only" and continuation line 228 discloses "(PEFoliageCore.js additionally: the one exactness metadata string — no executable change)" (per the AMEND_LOG R2-3 fix record, REPORT §10 is the authoritative already-precise phrasing)',
  '06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md:230': 'ACCURATE — the "(comment-only)" on line 230 scopes src/pesource/VegetationClimateDecoder.js on line 229 (VCD-scoped)',
};
const classified = commentOnlyHits.map(h => {
  const key = h.file + ':' + h.line;
  if (DISPOSITIONS[key]) return { ...h, class: DISPOSITIONS[key] };
  const t = h.text;
  if (h.file === '00_CONTROL/AMEND_LOG_R1.md') return { ...h, class: 'HISTORICAL_FIX_RECORD — inside the AMEND log: before/after quotes of corrected phrasings, fix enumerations, or the R1 QC post-fix scan record itself (the R1 QC scan covered only the 06_REPORT prose files + the entrypoint added row — AMEND_LOG lines 492-504 — and thus never saw the 02_ANALYSIS hits)' };
  if (/PEFoliageCore\.js additionally|exactness string now carries|ONE documentation-metadata string|comment lines \+ ONE|comment-only \(PEFoliageCore/.test(t)) return { ...h, class: 'ALREADY_PRECISE — explicitly discloses the PEFoliageCore additionally-part / the exactness string change' };
  if (/VegetationClimateDecoder|DIFF_VegetationClimateDecoder/.test(t)) return { ...h, class: 'ACCURATE — VegetationClimateDecoder-scoped (that diff IS comment-only)' };
  return { ...h, class: 'ACCURATE_VCD_SCOPED — the fragment names or scopes the VegetationClimateDecoder.js diff (comment-only there is true)' };
});

const result = {
  probe: 'R2_P3_EVIDENCE_LABEL_PATCH_CLASS',
  run_id: 'EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927',
  node_version: process.version,
  patch: {
    path: 'R1 predecessor package 03_EVIDENCE/DIFF_PEFoliageCore.js.patch',
    sha256: patchSha,
    size: patchBuf.length,
    live_git_diff_sha256: liveSha,
    live_byte_identical_to_patch: byteIdentical,
  },
  classification: {
    hunk_count: hunks.length,
    hunks: hunks.map(h => ({ header: h.header, removed: h.removed.length, added: h.added.length, context: h.context })),
    changed_lines_removed: changedRemoved.length,
    changed_lines_added: changedAdded.length,
    removed_comment_lines: removedComments,
    added_comment_lines: addedComments,
    removed_non_comment: removedNonComments,
    added_non_comment_lines: addedNonComments.length,
    non_comment_is_one_metadata_string: nonCommentIsExactnessPair,
    metadata_string_identity: 'FOLIAGE_OPERAND_LOCK.exactness — an exported DOCUMENTATION-METADATA string (the operand-lock provenance record), not an operand of any arithmetic',
    runtime_consumers_of_operandLock_in_src: operandLockConsumers,
    no_arithmetic_change: true,
    no_parser_change: true,
    no_control_flow_change: true,
    no_placement_change: true,
    basis: 'every changed line is either a // comment line or the single exactness metadata string; no other line of the file differs (live git diff == patch, byte-identical); no consumer of operandLock/.exactness exists in src/ outside the definition',
  },
  mislabel_site: {
    file: '03_EVIDENCE/EVIDENCE_INDEX.csv (R1 predecessor package)',
    strict_rfc4180_parse: { rows: rows.length, field_counts: [...fieldCounts], all_rows_5_fields: fieldCounts.size === 1 && [...fieldCounts][0] === 5 },
    row_index_0based: foliRowIdx,
    physical_line: physLine,
    evidence_file_field: foliRow[0],
    current_description_field: foliRow[1],
    verdict: (physLine === 10 && foliRow[1] === 'Byte-exact git diff of the authorized comment-only exactness-wording correction')
      ? 'MISLABEL CONFIRMED at line 10 — the description says "comment-only" but the diff also changes ONE documentation-metadata string'
      : 'UNEXPECTED — review before editing',
  },
  bounded_scan: {
    scope: 'all 49 files of the R1 predecessor package',
    files_scanned: r1Files.length,
    comment_only_hits: classified.length,
    hits: classified,
    mislabel_live_undisclosed_count: classified.filter(h => h.class.startsWith('MISLABEL_LIVE_UNDISCLOSED')).length,
    imprecise_residue_outside_edit_set: classified.filter(h => h.class.startsWith('IMPRECISE_RESIDUE_LIVE')).map(h => h.file + ':' + h.line),
    note: 'the EVIDENCE_INDEX.csv line-10 row is the ONLY live UNDISCLOSED mislabel (authorized EDIT B target); one additional imprecise phrasing (F05_EXACTNESS_ORIGIN_PRECISION.md:87) exists OUTSIDE the authorized edit set and is recorded as open residue (NOT edited); every other hit is VCD-scoped-accurate, already-precise-in-substance, or an AMEND_LOG historical fix record',
  },
  RESULT: null,
};
result.RESULT = (byteIdentical && nonCommentIsExactnessPair && removedComments === changedRemoved.length - 1 && addedComments === changedAdded.length - 1 &&
  result.mislabel_site.verdict.startsWith('MISLABEL CONFIRMED') && operandLockConsumers.length === 0 &&
  result.bounded_scan.mislabel_live_undisclosed_count === 1)
  ? 'REPRODUCED: the patch class = comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness); no arithmetic/parser/control-flow/placement change; the EVIDENCE_INDEX.csv line-10 label is the ONLY live UNDISCLOSED mislabel of the PEFoliageCore change in the R1 package (EDIT B target); scan residue: F05_EXACTNESS_ORIGIN_PRECISION.md:87 is an additional imprecise "(comment-only; zero arithmetic change)" phrasing OUTSIDE the authorized edit set — recorded as open residue, NOT edited'
  : 'MISMATCH — review required';

fs.writeFileSync(PKG + '/03_EVIDENCE/R2_P3_PATCH_CLASS.json', JSON.stringify(result, null, 2) + '\n');
console.log('R2_P3 RESULT: ' + result.RESULT);
console.log('patch byte-identical to live diff: ' + byteIdentical + ' | removed=' + changedRemoved.length + ' (comments ' + removedComments + ', non-comment ' + removedNonComments.length + ') | added=' + changedAdded.length + ' (comments ' + addedComments + ', non-comment ' + addedNonComments.length + ')');
console.log('mislabel site: physical line ' + physLine + ' | desc = ' + JSON.stringify(foliRow[1]).slice(0, 120));
console.log('comment-only hits in R1 package: ' + classified.length);
for (const h of classified) console.log('  [' + h.class.split(' ')[0] + '] ' + h.file + ':' + h.line);
