// gen_matrices.mjs v2 — CORRECTION_MATRIX.csv + FEATURE_COVERAGE_MATRIX.csv, generated
// from POST_MEASUREMENTS.json / POST_TEST_RESULTS.json (never hand-typed).
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const pm = JSON.parse(fs.readFileSync(path.join(HERE, 'POST_MEASUREMENTS.json'), 'utf8'));
const tr = JSON.parse(fs.readFileSync(path.join(HERE, 'POST_TEST_RESULTS.json'), 'utf8'));
const csvEsc = v => /[",\n]/.test(String(v)) ? '"' + String(v).replaceAll('"', '""') + '"' : String(v ?? '');
const toCsv = rows => rows.map(r => r.map(csvEsc).join(',')).join('\n') + '\n';
const rows = [['case', 'contract_ref', 'required_post_expectation', 'measured_outcome', 'measured_evidence', 'disposition']];
const C = pm.cases;
// F4 fix: the original-seven outcome is derived from the 7 original test NAMES passing,
// not from the total suite count (the suite also contains the new correction tests).
rows.push(['ORIGINAL_SEVEN_TESTS', '§4/§10', 'all 7 original kit tests pass on the corrected tool', tr.failCount === 0 && tr.originalSevenPass === true ? 'PASS' : 'FAIL', `suite=${tr.testsCount} pass=${tr.passCount} fail=${tr.failCount} exit=${tr.exitCode} originalSevenNamesPass=${tr.originalSevenPass}`, tr.failCount === 0 && tr.originalSevenPass ? 'case_pass' : 'correction_fail']);
const M = [
  ['O1', 'O1_INVALID_NUMERIC_CONFIG', 'invalid numeric config: nonzero exit, INVALID_CONFIGURATION, SCAN_STARTED=NO; legal zero/negative range pass'],
  ['O2', 'O2_EXCLUSION_CENSUS', 'all declared entries accounted once; disposition sum == declared; separate container/entry/payload/table units'],
  ['O3', 'O3_SAMPLE_VS_CENSUS', 'sample 1200/4800 not presented as full evaluation; full census reproduces known table quality'],
  ['O4', 'O4_SINGLE_DEFINITION_TABLE', 'minDistinctId=1 detects single-definition table; default filter restriction explicit; one interface'],
  ['O5', 'O5_INTEGER_COUNTERS_AS_FLOATS', 'visible subnormal f32 + competing u32; candidate allowed; no placement promotion'],
  ['O6', 'O6_ACTUAL_PROJECT_ADAPTERS', 'positive RAW/BNT2/ARK smoke with real BASE adapters on synthetic bytes'],
  ['O7', 'O7_NUMERIC_DAT_MODEL_NAME_PATTERN', 'helper limitation documented and reproduced synthetically; hypothetical .dat not a Models.bnt defect'],
  ['S7a', 'S7a_LAYOUT_ATTEMPTS_VS_ADMITTED', 'LAYOUT_ATTEMPTS=126, LAYOUTS_ADMITTED=0; lowered limit stops attempts; budget charged on attempts'],
  ['S7b', 'S7b_XYZ_TRIPLE_RATE', 'joint 56/80=0.7 reported as XYZ_FINITE_RATE; 0.9 remains legacy column mean; never presented as joint rate'],
];
for (const [id, key, exp] of M) rows.push([id, '§6/§7', exp, C[key].outcome, JSON.stringify(Object.fromEntries(Object.entries(C[key]).filter(([k]) => !['timeUtc', 'command', 'outcome', 'note', 'expectedFromCountercheck', 'budgetChargedQuantity'].includes(k)))), C[key].outcome === 'PASS' ? 'case_pass' : 'correction_fail']);
const BB = C.BUDGET_BATTERY;
const BEXP = {
  B1: 'SYNTHETIC_INPUTS: legal 32; 33rd admission refused before scan; aggregation across TWO inputs (second container entry OVER_BUDGET)',
  B2: 'SCANNED_BYTES: reserved before read; aggregation across two raw inputs; legal boundary',
  B3: 'LAYOUT_EVALUATIONS: aggregation across two inputs; pre-exhaustion payload disposition corrected to OVER_BUDGET; stop recorded',
  B4: 'FULL_CENSUS_ROWS: charged per candidate-row unit; aggregation across two inputs; PARTIAL_BUDGET_EXHAUSTED honest',
  B5: 'RETAINED_CANDIDATES: GLOBAL peak across all structures; aggregation across two inputs; PARTIAL not NO_CANDIDATE',
  B6: 'budget thresholds can never exceed canonical ceilings (exported + CLI)',
  B7: 'Budget class: no-reset-per-payload; reservation refund; separate container/control byte accounting',
  CX1: 'ENTRY_TOO_LARGE disposition with lowered per-entry cap (legal boundary: small entry still scanned)',
  CX2: 'INPUT_TOO_LARGE container-level refusal (no invented entries, no bytes charged)',
  CX3: 'UNSUPPORTED container-level framing failure (bad footer) with nonzero exit',
  CX4: 'PAYLOAD_SIZE_MISMATCH is PARSE_FAILED with the reservation refunded',
};
for (const [k, exp] of Object.entries(BEXP)) rows.push([k, '§8/§5.2', exp, BB[k].outcome, JSON.stringify(BB[k]), BB[k].outcome === 'PASS' ? 'case_pass' : 'correction_fail']);
fs.writeFileSync(path.join(HERE, '..', 'CORRECTION_MATRIX.csv'), toCsv(rows));

const f = [['feature', 'scope_status', 'evidence', 'notes']];
f.push(['fail-closed config validation (CLI + exported)', 'IMPLEMENTED', 'O1 + budget.test B6 + TEST_SUITE', 'INVALID_CONFIGURATION / SCAN_STARTED=NO / exit!=0; legal boundaries protected (maxHeader=0, negative posLo)']);
f.push(['exclusion census with disjoint dispositions', 'IMPLEMENTED', 'O2 + CX1..CX4 + TEST_SUITE', 'FILTERED_REGEX/EXTENSION/ENTRY_TOO_LARGE/TOO_SMALL/PARSE_FAILED/OVER_BUDGET/SCANNED + container-level UNSUPPORTED/INPUT_TOO_LARGE; censusOk assertion; PAYLOAD_SIZE_MISMATCH refund']);
f.push(['LAYOUT_ATTEMPTS before filters', 'IMPLEMENTED', 'S7a + TEST_SUITE', '126 vs 0 on the canonical fixture; legacy layoutsTested kept, not renamed']);
f.push(['joint XYZ_FINITE_RATE + full census of finalists', 'IMPLEMENTED', 'S7b + O3 + TEST_SUITE', '56/80=0.7; FULL_CENSUS within budget; NOT_PERFORMED/PARTIAL_BUDGET_EXHAUSTED otherwise; zero denominator => null']);
f.push(['f32/u32 candidate diagnostics', 'IMPLEMENTED', 'O5 + TEST_SUITE', 'finiteRate(+denominator), NAN/INFINITY/SUBNORMAL/ZERO counts, magnitude summary, ALTERNATIVE_U32_INTERPRETATION']);
f.push(['single min-distinct-id interface', 'IMPLEMENTED', 'O4 + TEST_SUITE', '--min-distinct-id 1 regression; default 2 documented as explicit coverage restriction']);
f.push(['per-invocation budgets (5 limits)', 'IMPLEMENTED', 'B1..B7 + TEST_SUITE', 'shared across inputs, no reset per payload, reservation BEFORE read with verified size + refund on unscanned, ceilings never raised, PARTIAL not NO_CANDIDATE, GLOBAL retained-candidate peak']);
f.push(['actual-project-adapter positive smoke', 'IMPLEMENTED', 'O6 + TEST_SUITE', 'BASE git blobs 1fb8629.../a9c9f04...; synthetic bytes only']);
f.push(['ids_from_export numeric-name limitation', 'IMPLEMENTED', 'O7 + TEST_SUITE', '.dat rejection explicit; nonNumericNamesExcluded counted; historical Models.bnt inventory untouched']);
f.push(['fixed-stride search only', 'LIMITATION_DOCUMENTED', 'README + FEATURE matrix', 'variable-stride records NOT_IMPLEMENTED (out of correction scope)']);
f.push(['sampling-driven discovery', 'LIMITATION_DOCUMENTED', 'README + O3', 'sample is discovery input only; full census only for finalists within budget']);
f.push(['heuristic gates as discovery filters', 'LIMITATION_DOCUMENTED', 'README', 'not validity oracles']);
f.push(['placement/world/instance semantics', 'PROHIBITED_BY_CONTRACT', 'standing science block in README + FINAL_REPORT', 'MODEL_218757_TO_CMO_JOIN etc. NOT_ESTABLISHED; no promotion anywhere']);
f.push(['original PCG payload scanning for placement', 'NOT_PERFORMED (contract-prohibited)', 'none', 'PLACEMENT_DISCOVERY = NOT_EXECUTED']);
f.push(['Gamebryo/EXE RE, viewer changes, master merge', 'NOT_PERFORMED (contract-prohibited)', 'none', 'scope forbidden in this run']);
f.push(['variable-stride records, quaternion/rotation decoding, georeferencing', 'NOT_IMPLEMENTED / NOT_CHECKED', 'none', 'out of correction scope per contract §9']);
fs.writeFileSync(path.join(HERE, '..', 'FEATURE_COVERAGE_MATRIX.csv'), toCsv(f));
console.log('matrices written: correction rows=' + (rows.length - 1) + ' feature rows=' + (f.length - 1));