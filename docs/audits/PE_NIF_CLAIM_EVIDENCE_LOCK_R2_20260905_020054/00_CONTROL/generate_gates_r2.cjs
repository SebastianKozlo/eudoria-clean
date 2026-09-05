// generate_gates_r2.cjs — emits STAGE_ACCEPTANCE_GATES.csv GENERATED FROM
// 02_LOGS/TEST_RESULTS.json (no hand-written results; R1's fixed-array defect class
// is superseded). Human-reviewed gates are carried with gate_type=HUMAN_REVIEWED.
'use strict';
const fs = require('fs'), crypto = require('crypto');
const RUN = 'D:/Eudoria_Reconstruction/99_Audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054';
const TR = JSON.parse(fs.readFileSync(RUN + '/02_LOGS/TEST_RESULTS.json', 'utf8'));
const esc = s => '"' + String(s).replace(/"/g, '""') + '"';
const head = ['gate_id', 'gate_name', 'gate_type', 'expected', 'result', 'measured_quantity', 'denominator',
  'independent_source_of_truth', 'why_non_circular', 'failure_case_detected', 'fixtures', 'evidence'];
const rows = [];
for (const g of TR.gates) {
  const res = g.pass === null ? 'HUMAN_REVIEW_REQUIRED' : (g.pass ? 'PASS' : 'FAIL');
  rows.push([g.gate_id, g.gate_name, g.gate_type, 'invariant holds', res,
    g.measured_quantity, g.denominator, g.independent_source_of_truth, g.why_non_circular,
    g.failure_case_detected,
    (g.fixtures || []).map(f => f.fixture ? (f.fixture + ' -> ' + f.result) : JSON.stringify(f)).join(' | '),
    '02_LOGS/TEST_RESULTS.json']);
}
const execFail = TR.executable_failures.length;
rows.push(['OVERALL', 'RUN STATUS (executable suite; human-reviewed gates tracked separately)', 'EXECUTABLE',
  'all EXECUTABLE gates PASS (exit 0)', execFail === 0 ? 'PASS' : 'FAIL',
  TR.gates.filter(g => g.pass === true).length + ' executable PASS of ' + TR.gates.filter(g => g.gate_type === 'EXECUTABLE').length + ' executable gates',
  TR.gates.filter(g => g.gate_type === 'EXECUTABLE').length + ' executable gates (4 HUMAN_REVIEWED rows tracked separately)',
  'run_gates.py fresh computation over the physical containers + original manifests',
  'independent Python implementation; Node results used only as compared counterpart',
  'the suite failed intermediate R2 outputs during development (documented in 02_LOGS/LOGS.md) and fails the R1 fixtures by design',
  'old-fixture FAIL demonstrations recorded per gate', '02_LOGS/TEST_RESULTS.json; 02_LOGS/LOGS.md']);
fs.writeFileSync(RUN + '/STAGE_ACCEPTANCE_GATES.csv', [head.map(esc).join(',')].concat(rows.map(r => r.map(esc).join(','))).join('\r\n') + '\r\n');
console.log('STAGE_ACCEPTANCE_GATES.csv written: ' + rows.length + ' rows (' + TR.gates.filter(g => g.gate_type === 'EXECUTABLE').length + ' EXECUTABLE + ' + TR.gates.filter(g => g.gate_type === 'HUMAN_REVIEWED').length + ' HUMAN_REVIEWED + OVERALL)');
