// PHASE 3d EXACT UNIFIED DIFFS — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// Produces EDIT_A_F03.diff / EDIT_B_EVIDENCE_INDEX.diff / EDIT_C_MANIFEST.diff
// into 03_EVIDENCE by `git diff --no-index BEFORE_IMAGE CURRENT` and verifies
// each edited file changed EXACTLY the authorized span (structural checks).
import fs from 'node:fs';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const R1 = 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926';
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

const PAIRS = [
  { diff: 'EDIT_A_F03.diff', before: PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_F03_TERRAIN_TEXTURE_SCOPE.md', after: REPO + '/' + R1 + '/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md', label: 'EDIT_A (F03 line 102: the incorrect sample-total statement)' },
  { diff: 'EDIT_B_EVIDENCE_INDEX.diff', before: PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_EVIDENCE_INDEX.csv', after: REPO + '/' + R1 + '/03_EVIDENCE/EVIDENCE_INDEX.csv', label: 'EDIT_B (EVIDENCE_INDEX.csv line 10: the DIFF_PEFoliageCore.js.patch description field)' },
  { diff: 'EDIT_C_MANIFEST.diff', before: PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_MANIFEST_SHA256.csv', after: REPO + '/' + R1 + '/06_REPORT/MANIFEST_SHA256.csv', label: 'EDIT_C (MANIFEST_SHA256.csv: the two edited files\' rows — sha256+size refresh)' },
];

for (const p of PAIRS) {
  const r = spawnSync('git', ['diff', '--no-index', '--', p.before, p.after], { cwd: REPO, maxBuffer: 1e8 });
  if (r.status !== 1 && r.status !== 0) throw new Error('git diff --no-index failed: ' + r.stderr.toString());
  let d = r.stdout.toString();
  // label the provenance at the top (the a/ b/ paths follow in the diff header)
  d = '# ' + p.label + '\n# a = the byte-exact BEFORE_IMAGE preserved before the edit; b = the post-edit repository file\n' + d;
  fs.writeFileSync(PKG + '/03_EVIDENCE/' + p.diff, d);
  // count removed/added from the hunk bodies (lines after @@ markers, excluding the ---/+++ headers)
  let removed = 0, added = 0, inHunk = false;
  for (const l of d.split('\n')) {
    if (l.startsWith('@@')) { inHunk = true; continue; }
    if (!inHunk) continue;
    if (l.startsWith('---') || l.startsWith('+++')) continue;
    if (l.startsWith('-')) removed++;
    else if (l.startsWith('+')) added++;
  }
  console.log(p.diff + ': ' + removed + ' removed / ' + added + ' added lines; before_sha=' + sha(p.before).slice(0, 16) + '... after_sha=' + sha(p.after).slice(0, 16) + '...');
}

// --- structural span verification ---
const beforeF03 = fs.readFileSync(PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_F03_TERRAIN_TEXTURE_SCOPE.md', 'utf8').split('\n');
const afterF03 = fs.readFileSync(REPO + '/' + R1 + '/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md', 'utf8').split('\n');
const f03Checks = {
  old_statement_was_line_102: beforeF03[101] === '- SAMPLE DIMENSIONS: 32x32 u16 per tile (1,664,000 samples over 51,920 tiles).',
  old_statement_gone: !afterF03.some(l => l.includes('1,664,000 samples over 51,920 tiles')),
  new_total_present: afterF03.some(l => l.includes('53,166,080 u16 SAMPLE SLOTS')),
  both_paths_present: afterF03.some(l => l.includes('51,920 x 1,024 = 53,166,080')) && afterF03.some(l => l.includes('(220x32) x (236x32) = 7,040 x 7,552 = 53,166,080')),
  attribution_present: afterF03.some(l => l.includes('EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927')),
  not_list_present: afterF03.some(l => l.includes('NOT unique height values, NOT unique world points, NOT')) && afterF03.some(l => l.includes('original-client parity, NOT proof of the RGB-TDF bridge')),
  bridge_status_line_unchanged: (beforeF03.find(l => l.startsWith('BRIDGE_STATUS = UNKNOWN')) || 'MISSING') === (afterF03.find(l => l.startsWith('BRIDGE_STATUS = UNKNOWN')) || 'MISSING'),
  lines_before_101_unchanged: beforeF03.slice(0, 101).join('\n') === afterF03.slice(0, 101).join('\n'),
  new_statement_is_11_lines: afterF03.slice(101, 112).join('\n').startsWith('- SAMPLE DIMENSIONS: 32x32 u16 per tile. TOTAL = 53,166,080') && afterF03[111].includes('all calibration/unknown labels preserved).'),
  lines_after_the_statement_unchanged: beforeF03.slice(102).join('\n') === afterF03.slice(112).join('\n'),
  section_7_2_B_offset_line_unchanged: beforeF03.find(l => l.includes('32x32 uint16 LE at payload')) === afterF03.find(l => l.includes('32x32 uint16 LE at payload')),
};
console.log('F03 structural checks: ' + JSON.stringify(f03Checks));

function parseCsv4180(s) {
  const rows = []; let row = []; let field = ''; let inQ = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (inQ) { if (c === '"') { if (s[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
    else if (c === '"') inQ = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}
const beforeEI = fs.readFileSync(PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_EVIDENCE_INDEX.csv', 'utf8');
const afterEI = fs.readFileSync(REPO + '/' + R1 + '/03_EVIDENCE/EVIDENCE_INDEX.csv', 'utf8');
const eiBefore = parseCsv4180(beforeEI), eiAfter = parseCsv4180(afterEI);
const foliAfter = eiAfter.find(r => r[0] === '03_EVIDENCE/DIFF_PEFoliageCore.js.patch');
const eiChecks = {
  line_count_equal_27: beforeEI.split('\n').filter(Boolean).length === afterEI.split('\n').filter(Boolean).length && afterEI.split('\n').filter(Boolean).length === 27,
  all_rows_5_fields: eiAfter.every(r => r.length === 5) && eiBefore.every(r => r.length === 5),
  only_row_10_changed: eiBefore.length === eiAfter.length && eiBefore.every((r, i) => i === 9 || r.join('\u0001') === eiAfter[i].join('\u0001')),
  new_description_exact: foliAfter[1] === 'Byte-exact git diff of the authorized correction: comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness) - no arithmetic/parser/control-flow/placement change (label corrected by EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927)',
  row_stays_one_line: afterEI.split('\n').filter(Boolean)[9] === ['03_EVIDENCE/DIFF_PEFoliageCore.js.patch', foliAfter[1], 'git diff (repo state)', 'VCS_DIFF', 'computed at manifest time'].map(v => '"' + v + '"').join(','),
  other_fields_unchanged: foliAfter[0] === '03_EVIDENCE/DIFF_PEFoliageCore.js.patch' && foliAfter[2] === 'git diff (repo state)' && foliAfter[3] === 'VCS_DIFF' && foliAfter[4] === 'computed at manifest time',
};
console.log('EVIDENCE_INDEX structural checks: ' + JSON.stringify(eiChecks));

const beforeMan = fs.readFileSync(PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_MANIFEST_SHA256.csv', 'utf8').split('\n');
const afterMan = fs.readFileSync(REPO + '/' + R1 + '/06_REPORT/MANIFEST_SHA256.csv', 'utf8').split('\n');
const manChecks = {
  line_count_49: afterMan.filter(Boolean).length === 49,
  header_unchanged: beforeMan[0] === afterMan[0],
  only_two_rows_changed: beforeMan.filter(Boolean).length === afterMan.filter(Boolean).length && beforeMan.every((l, i) => [15, 22].includes(i) || l === afterMan[i]),
  row16_new_values: afterMan[15] === 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md,72e1e22149405f4921ca69d36c8adb2e5a776b4de3acba2db5f67f0e82662ffb,10534',
  row23_new_values: afterMan[22] === 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE/EVIDENCE_INDEX.csv,67bfee8c15fac242ec079bba85f752c5b47a80b64a764cf3b0e6f5dece910443,7710',
  order_preserved: beforeMan.map(l => l.split(',')[0]).join('|') === afterMan.map(l => l.split(',')[0]).join('|'),
  self_excluded: !afterMan.some(l => l.startsWith('docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/06_REPORT/MANIFEST_SHA256.csv,')),
  data_rows_48: afterMan.slice(1).filter(Boolean).length === 48,
};
console.log('MANIFEST structural checks: ' + JSON.stringify(manChecks));

const all = [...Object.values(f03Checks), ...Object.values(eiChecks), ...Object.values(manChecks)];
console.log('ALL_SPAN_CHECKS_PASS=' + all.every(v => v === true));
