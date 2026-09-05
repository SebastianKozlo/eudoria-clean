// generate_artifact_index_r2.cjs — emits artifact_index.csv with REAL SHA256 for
// every run file (hash computed at emit time) and the read-only input sources,
// plus a claim-aware claims_supported column (existing convention + claim metadata).
// Documented exclusions (cannot contain a hash of a file written after it / itself):
//   artifact_index.csv itself (SELF_EXCLUDED — R1 precedent),
//   02_LOGS/TEST_RESULTS.json (FINAL_GATE_OUTPUT — written by the final gate pass),
//   STAGE_ACCEPTANCE_GATES.csv (FINAL_GATE_LEDGER — generated from TEST_RESULTS.json).
// The byte identity of the excluded trio is pinned by the Git publication (blob parity).
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const PROJECT = 'D:/Eudoria_Reconstruction';
const AUDITS = PROJECT + '/99_Audits';
const RUN = AUDITS + '/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054';
const R1 = AUDITS + '/PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119';
const POST = AUDITS + '/PE_NIF_CLAIM_LOCK_POST_AUDIT_20260905_020054';
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const esc = s => '"' + String(s).replace(/"/g, '""') + '"';

const rows = [];
function add(p, role, claims, scope) {
  rows.push({ p, role, claims, scope });
}
// ---- run package files (dynamic enumeration; exclusions handled explicitly) ----
const CLAIMS_BY_FILE = {
  '00_CONTROL/PLAN.md': [],
  '00_CONTROL/control_r2.cjs': ['C2-A-01..06', 'C2-B-01..05', 'C2-C-01..04', 'C2-E-02'],
  '00_CONTROL/emit_r2_csvs.cjs': ['C2-* emitter'],
  '00_CONTROL/run_gates.py': ['C2-E-01', 'C2-E-02'],
  '00_CONTROL/generate_gates_r2.cjs': ['C2-E-02'],
  '00_CONTROL/generate_artifact_index_r2.cjs': [],
  '00_CONTROL/SHA256_CONTROL.txt': ['C2-D-04a'],
  '00_CONTROL/FIXTURES/synthetic_original.csv': ['C2-E-02'],
  '00_CONTROL/FIXTURES/synthetic_sidecar.csv': ['C2-C-01', 'C2-E-02'],
  '01_RAW/RECOUNTS.json': ['C2-A-01..06', 'C2-B-01..05', 'C2-C-01..04', 'C2-D-01..05', 'C2-E-02'],
  '02_LOGS/LOGS.md': ['C2-D-04a', 'C2-E-02'],
  '03_STATIC/SOURCE_QUOTES.md': ['all (quote evidence)'],
  '04_RUNTIME/NOT_RUN.md': [],
  '05_ANALYSIS/CLAIM_MATRIX.csv': ['all 24 claims'],
  '05_ANALYSIS/FINDING_DISPOSITIONS.csv': ['F1-F5, F-PUB, R2-NEW-1'],
  '05_ANALYSIS/SUPERSESSION_MAP.csv': ['all supersessions'],
  '06_REPORT/00_FINAL_REPORT.md': ['all'],
  '06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md': ['C2-D-01..05', 'P1R2..P8R2'],
  'REPORT.md': [],
  'HANDOFF.md': []
};
for (const rel of Object.keys(CLAIMS_BY_FILE)) {
  const p = RUN + '/' + rel;
  if (!fs.existsSync(p)) { console.error('MISSING package file: ' + rel); process.exit(1); }
  add(p, 'R2 run artifact (' + rel + ')', CLAIMS_BY_FILE[rel], 'this run (PE-NIF-CLAIM-EVIDENCE-LOCK-R2, 2026-09-05)');
}
for (const f of fs.readdirSync(RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS')) {
  add(RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS/' + f, 'lossless sidecar (RAW_BYTES_CONTRACT v1: base64 raw row bytes + row SHA256 + terminators + strict-only field mapping) of the named historical manifest; originals immutable', ['C2-C-01..04'], 'this run (PE-NIF-CLAIM-EVIDENCE-LOCK-R2, 2026-09-05)');
}
// ---- excluded trio (documented; no hash by construction) ----
rows.push({ p: RUN + '/artifact_index.csv (THIS FILE)', role: 'this manifest itself — SELF_EXCLUDED_BY_CONSTRUCTION (R1 precedent: a file cannot contain its own SHA-256; all other rows carry real in-run hashes)', claims: [], scope: 'this run', nohash: true });
rows.push({ p: RUN + '/02_LOGS/TEST_RESULTS.json', role: 'FINAL_GATE_OUTPUT — written by the final run_gates.py pass that verifies this manifest; a manifest cannot contain the hash of the checker output written after it; byte identity pinned by the Git publication', claims: ['C2-E-01', 'C2-E-02'], scope: 'this run', nohash: true });
rows.push({ p: RUN + '/STAGE_ACCEPTANCE_GATES.csv', role: 'FINAL_GATE_LEDGER — generated from TEST_RESULTS.json after the final gate pass (no hand-written results); hash not embeddable upstream; byte identity pinned by the Git publication', claims: ['C2-E-02'], scope: 'this run', nohash: true });
// ---- read-only input sources (real hashes) ----
const INPUTS = [
  [POST + '/00_CONTROL/OPENCODE_R2_PROMPT.md', 'execution prompt (SHA verified pre-execution: 46A2A99A...)', []],
  [POST + '/06_REPORT/00_FINAL_REPORT.md', 'independent post-audit report (input, read-only; findings re-derived, not copied)', ['F1-F5 dispositions']],
  [POST + '/01_RAW/verification.json', 'auditor verification output (input, read-only)', []],
  [POST + '/00_CONTROL/verify.py', 'auditor method (input, read-only; probe SHA 6ff50e0b...)', []],
  [R1 + '/01_RAW/CONTROL_R1_RESULTS.json', 'R1 raw control output (input, read-only; fixture reference for the counter defects)', ['C2-A-04', 'C2-D-05a']],
  [R1 + '/05_ANALYSIS/CLAIM_MATRIX.csv', 'R1 claim matrix (input, read-only; C-R35-04/C-R36-05 defect sites)', ['C2-A-05', 'C2-B-03']],
  [R1 + '/STAGE_ACCEPTANCE_GATES.csv', 'R1 gate ledger (input, read-only; G7/G8 defect sites)', ['C2-B-03', 'C2-E-01']],
  [R1 + '/06_REPORT/00_FINAL_REPORT.md', 'R1 final report (input, read-only; Control 3 defect site)', []],
  [R1 + '/06_REPORT/PROPOSED_DOC_CORRECTIONS.md', 'R1 proposals (input, read-only; P1-5/P4-3/P6 defect sites)', ['C2-D-01..03', 'C2-C-03']],
  [R1 + '/05_ANALYSIS/DENOMINATORS.json', 'R1 denominator inventory (input, read-only; family-witness defect site)', ['C2-A-06']],
  [R1 + '/05_ANALYSIS/COUNTEREXAMPLES.json', 'R1 counterexamples (input, read-only; CE-5(c)/CE-6 defect sites)', ['C2-B-03']],
  [R1 + '/00_CONTROL/generate_gates.cjs', 'R1 gate emitter (input, read-only; fixed-array evidence, quote S11)', ['C2-E-01']],
  [R1 + '/00_CONTROL/SHA256_CONTROL.txt', 'R1 execution hash record (input, read-only; TWO recorded executions)', ['C2-D-04a']],
  [R1 + '/02_LOGS/LOGS.md', 'R1 logs (input, read-only; control exec-1/exec-2 + generator iterations)', ['C2-D-04a']],
  [R1 + '/05_ANALYSIS/NORMALIZED_MANIFESTS/PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.normalized.csv', 'R1 R39 sidecar (input, read-only; lossy role fixture "per-file gaps [priorities]")', ['C2-C-02', 'C2-C-03']],
  [AUDITS + '/PE_NIF_FIELD_D_R36_20260904_171903/02_results/FIELD_D_TESTS.json', 'R36 raw evidence (T4 candidate counts; historical agreement)', ['C2-B-01..03']],
  [AUDITS + '/PE_NIF_FIELD_D_R36_20260904_171903/01_source/field_d_r36.py', 'R36 driver source (candidate definitions; read-only)', ['C2-B-01']],
  [AUDITS + '/PE_NIF_CROSS_ERA_R35_20260904_170224/02_results/GRAMMAR_VALIDATION.json', 'R35 raw evidence (corpus-level validator aggregates; no per-file join)', ['C2-A-05', 'C2-A-06']],
  [AUDITS + '/PE_NIF_WIKI_AUDIT_R39_20260904_180213/artifact_index.csv', 'R39 original manifest (immutable; BOM + GAP row source bytes; SHA 6a007dbb...)', ['C2-C-02']],
  [PROJECT + '/pcg_install/Data/Models/Models.bnt', 'PCG 9.3.5 ORIGINAL container (read-only; direct re-parse this run)', ['C2-A-01..06', 'C2-B-01..05']],
  [PROJECT + '/01_Original_Files/BNT_Models/Models.bnt', '2003-era ORIGINAL container (read-only; separately hash-pinned comparison corpus; direct re-parse this run)', ['C2-A-01..06', 'C2-B-01..05']]
];
for (const [p, role, claims] of INPUTS) add(p, role, claims, p.startsWith(R1) || p.startsWith(AUDITS) ? 'historical run (immutable)' : (p.startsWith(POST) ? 'external audit 2026-09-05 (immutable)' : (p.includes('pcg_install') ? 'pcg_install corpus (read-only)' : 'original game file (immutable)')));

const head = ['source_path_full', 'role', 'sha256', 'snapshot_time_scope', 'claims_supported'];
const out = [head.map(esc).join(',')].concat(rows.map(r => [r.p, r.role, r.nohash ? '' : hash(r.p), r.scope, r.claims.join('; ')].map(esc).join(','))).join('\r\n') + '\r\n';
fs.writeFileSync(RUN + '/artifact_index.csv', out);
console.log('artifact_index.csv written: ' + rows.length + ' rows (' + rows.filter(r => r.nohash).length + ' documented no-hash exclusions, ' + (rows.length - rows.filter(r => r.nohash).length) + ' real hashes)');
