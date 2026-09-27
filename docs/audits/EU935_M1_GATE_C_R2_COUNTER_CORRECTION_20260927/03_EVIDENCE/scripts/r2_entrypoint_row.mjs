// PHASE 4 AUDIT_ENTRYPOINT ROW — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// Inserts EXACTLY ONE row at the TOP of the LATEST RUNS table (above the R1
// row). ALL existing rows byte-preserved. Verifies: numstat becomes 2/0; the
// vs-HEAD diff contains ONLY the 2 added rows (the R1 row + the new R2 row);
// zero deletions. This is the ONLY tracked-file edit of this run.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { execSync, spawnSync } from 'node:child_process';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const FILE = REPO + '/AUDIT_ENTRYPOINT.md';
const BEFORE_SHA = '8EEC84E65C19B56705B023AADAB27B5AD0A05E03686E5992F4C47A4836BEE45E';
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

const before = fs.readFileSync(FILE);
if (sha(before) !== BEFORE_SHA) throw new Error('ENTRYPOINT BEFORE-SHA MISMATCH — HARD STOP');
const text = before.toString('utf8');
const lines = text.split('\n');
const r1Idx = lines.findIndex(l => l.startsWith('| (uncommitted — pre-persistence successor package'));
if (r1Idx !== 29) throw new Error('R1 ROW NOT FOUND AT EXPECTED POSITION 30 (0-based ' + r1Idx + ') — HARD STOP');

const ROW = '| (uncommitted at row insertion — the authorized persistence Commit 1 (a later separate phase) persists this R2 package together with the predecessor R1 successor package; HEAD cc747df at run start) | EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (RUN_CLASS LOAD_BEARING; RUN_TYPE GATE_C_R2_BOUNDED_COUNTER_CORRECTION; executor pe-reconstruction, PE-MASTER-dispatched correction run, dispatcher contract in the package 00_CONTROL/RUN_CONTRACT.md; STATIC-ONLY - the client never ran) | `EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/` | The bounded correction of the Desktop Gate-C R2 findings (GATEC_REAUDIT_R2_REPORT_20260927, verdict MILESTONE_POST_AUDIT_PARTIAL): R2-F01 the F03:102 terrain sample counter 1,664,000 -> 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular 32x32 tile blocks (regular-tile census re-derived from the pinned terrain.bnt 95841761...; two independent arithmetic paths 51,920 x 1,024 and (220x32) x (236x32) = 7,040 x 7,552, both = 53,166,080; sample slots, NOT unique heights / coverage / parity); R2-F02 the VCL review-arithmetic erratum (the pasted-review equation 491x12+24+252 actually equals 6,168; correct relations (491+1+1)x12 = 5,916 and 472x12+252 = 5,916; raw census 493/5,916 UNCHANGED and valid; no repo file contained the bad equation — 0 hits over all 2,594 tracked files); R2-P3 the EVIDENCE_INDEX DIFF_PEFoliageCore label corrected to comments + ONE metadata string (no behavior change); predecessor edits A/B/C with byte-identical BEFORE_IMAGES preserved in the R2 package; the predecessor R1 successor package is persisted by this run\'s human-authorized Commit 1 (supersedes the R1 row\'s "uncommitted" label) | PE-MASTER final audit + fresh INTERNAL_QC recorded in the run package 06_REPORT (advisory; CANONICAL_GATE_EFFECT = NONE while Q1 absent); Desktop R2 historical verdict MILESTONE_POST_AUDIT_PARTIAL stands; Gate A = PASS per the independent Desktop R2 audit; Gate C = REQUIRES_INDEPENDENT_DESKTOP_REAUDIT (this run claims NO Gate C PASS, NO MILESTONE_POST_AUDIT_PASS); Q1 NOT executed; Gate B canonical authority = BLOCKED (Q1 absent); M1 = OPEN; M2 = NOT AUTHORIZED; Viewer = NOT AUTHORIZED. |';

lines.splice(r1Idx, 0, ROW);
const out = lines.join('\n');
fs.writeFileSync(FILE, out);
const after = fs.readFileSync(FILE);

// --- verifications ---
const afterText = after.toString('utf8');
const afterLines = afterText.split('\n');
const checks = {
  before_sha_verified: sha(before) === BEFORE_SHA,
  one_line_inserted: after.length === before.length + Buffer.byteLength(ROW, 'utf8') + 1,
  new_row_is_line_30: afterLines[29] === ROW,
  r1_row_pushed_to_line_31: afterLines[30].startsWith('| (uncommitted — pre-persistence successor package'),
  all_other_lines_preserved: lines.filter((l, i) => i !== r1Idx).join('\n') === before.toString('utf8'), // 'lines' post-splice == afterLines; the original lines are all present
  no_embedded_newline_in_row: !ROW.includes('\n'),
  five_cells: (ROW.match(/\|/g) || []).length === 6, // 6 pipes = 5 cells + the two edge pipes
};
const numstat = execSync('git diff --numstat -- AUDIT_ENTRYPOINT.md', { cwd: REPO }).toString().trim();
const fullDiff = spawnSync('git', ['diff', '--', 'AUDIT_ENTRYPOINT.md'], { cwd: REPO, maxBuffer: 1e8 }).stdout.toString();
const addedDiff = (fullDiff.match(/^\+/gm) || []).length - 1; // minus the +++ header
const removedDiff = (fullDiff.match(/^-/gm) || []).length - 1; // minus the --- header
console.log('numstat: ' + numstat);
console.log('diff vs HEAD: +' + addedDiff + ' / -' + removedDiff + ' lines');
console.log(JSON.stringify(checks));
console.log('ENTRYPOINT after_sha256=' + sha(after));
console.log('ENTRYPOINT after_size=' + after.length);
const ok = numstat === '2\t0\tAUDIT_ENTRYPOINT.md' && addedDiff === 2 && removedDiff === 0 && Object.values(checks).every(v => v === true);
console.log('PHASE4_PASS=' + ok);
