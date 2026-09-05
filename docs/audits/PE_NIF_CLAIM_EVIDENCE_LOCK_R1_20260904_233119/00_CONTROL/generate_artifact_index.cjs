// generate_artifact_index.cjs â€” emits artifact_index.csv with REAL SHA-256 of every
// run artifact (excluding the manifest itself â€” documented self-hash impossibility).
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const RUN = 'D:/Eudoria_Reconstruction/99_Audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119';
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const q = s => '"' + String(s).replace(/"/g, '""') + '"';
function walk(p) { return fs.readdirSync(p, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(p, e.name)) : [path.join(p, e.name)]); }
const rows = [];
const SCOPE_RUN = 'this run (PE-NIF_CLAIM_EVIDENCE_LOCK_R1, 2026-09-05)';
const roles = {
  '00_CONTROL/control_r1.cjs': 'one-time control instrumentation (final exec hash 5AD889D3...; exec-1 6A296CC7...) â€” read-only on sources',
  '00_CONTROL/PLAN.md': 'execution plan (mandate, controls, outputs, hash-lock discipline, deviations)',
  '00_CONTROL/SHA256_CONTROL.txt': 'control-script hash provenance (hash-after-last-edit, both executions)',
  '00_CONTROL/generate_claim_matrix.cjs': 'CLAIM_MATRIX emitter (analysis instrumentation)',
  '00_CONTROL/generate_artifact_index.cjs': 'artifact_index manifest emitter (this manifest self-excludes by construction)',
  '00_CONTROL/generate_gates.cjs': 'STAGE_ACCEPTANCE_GATES.csv emitter (strict quoting)',
  '01_RAW/CONTROL_R1_RESULTS.json': 'RAW control output: f1 recount, morph denominators/k=1, BNT era join + CRC/d checks, witness scan, R29/R37/R38 re-reads, R39/R40 apply verification, manifest validation',
  '02_LOGS/LOGS.md': 'commands, tool versions, execution history, error dispositions, writer-lock analysis',
  '03_STATIC/SOURCE_QUOTES.md': 'verified source quotes with file+lines+SHA256 (S1-S19)',
  '04_RUNTIME/NOT_RUN.md': 'runtime out-of-scope declaration',
  '05_ANALYSIS/CLAIM_MATRIX.csv': 'core deliverable: 43 atomic claims, 14 columns, single knowledge status per row',
  '05_ANALYSIS/ALLEGATION_DISPOSITIONS.csv': '23 auditor allegations with ACCEPTED/REFUTED/UNRESOLVED + evidence',
  '05_ANALYSIS/DENOMINATORS.json': '21 explicit denominators with definitions and non-interchangeability warnings',
  '05_ANALYSIS/COUNTEREXAMPLES.json': '12 bounding counterexamples (CE-1..CE-12)',
  '06_REPORT/00_FINAL_REPORT.md': 'primary final report',
  '06_REPORT/PROPOSED_DOC_CORRECTIONS.md': 'document-scope corrections â€” PROPOSALS ONLY (P1-P7), not applied',
  'REPORT.md': 'pointer to the primary report',
  'STAGE_ACCEPTANCE_GATES.csv': '16 gates + OVERALL (all PASS)',
  'HANDOFF.md': 'handoff with the mandatory final block'
};
for (const rel of Object.keys(roles)) {
  const full = RUN + '/' + rel;
  if (!fs.existsSync(full)) throw new Error('missing artifact: ' + rel);
  rows.push([full.replace(/\//g, '\\'), roles[rel], hash(full), SCOPE_RUN].map(q).join(','));
}
// normalized sidecars (12)
const nmDir = RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS';
for (const f of fs.readdirSync(nmDir).sort()) {
  const full = nmDir + '/' + f;
  rows.push([full.replace(/\//g, '\\'), 'normalized sidecar of the named historical manifest (original path + SHA + row-exact recovery + hash verification + scope class)', hash(full), SCOPE_RUN].map(q).join(','));
}
// read-only source references (full paths + current SHA + snapshot scope)
const srcs = [
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_ITER29_40_EXTERNAL_AUDIT_20260904_233119\\NEXT_OPENCODE_PROMPT.md', 'this round prompt (SHA verified pre-execution)', 'prompt of this run'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_ITER29_40_EXTERNAL_AUDIT_20260904_233119\\06_REPORT\\00_FINAL_REPORT.md', 'external audit report (input, read-only)', 'external audit 2026-09-04 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_ITER29_40_EXTERNAL_AUDIT_20260904_233119\\01_RAW\\probe.json', 'auditor probe (input, read-only; NOT copied â€” all its allegations re-derived)', 'external audit 2026-09-04 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_ITER29_40_EXTERNAL_AUDIT_20260904_233119\\00_CONTROL\\probe.cjs', 'auditor method (input, read-only)', 'external audit 2026-09-04 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_MATERIAL_CENSUS_R32_20260904_160538\\02_results\\ANIM_FRAME_CHECK.json', 'R32 raw evidence (f1 recount source)', 'historical run R32 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_MORPH_QUANT_R34_20260904_164538\\02_results\\REAL_SPARSE_GRAMMAR.json', 'R34 raw evidence (denominators + k=1 examples)', 'historical run R34 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_MORPH_QUANT_R34_20260904_164538\\01_source\\morph_quant_r34.py', 'R34 driver source (parse_variable inspection)', 'historical run R34 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_CROSS_ERA_R35_20260904_170224\\02_results\\FORMAT_EVOLUTION.json', 'R35 raw evidence (21 claims)', 'historical run R35 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_CROSS_ERA_R35_20260904_170224\\02_results\\GRAMMAR_VALIDATION.json', 'R35 raw evidence (per-family 2003 results)', 'historical run R35 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_CROSS_ERA_R35_20260904_170224\\02_results\\ERA_CENSUS.json', 'R35 raw evidence (era census)', 'historical run R35 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_FIELD_D_R36_20260904_171903\\02_results\\FIELD_D_TESTS.json', 'R36 raw evidence (T1-T5, formula range)', 'historical run R36 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_IMPORTER_HEADER_R29_20260904_150900\\02_results\\PATTERNS.json', 'R29 raw evidence (patterns + era matrix)', 'historical run R29 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625\\02_results\\CLASS_SEQUENCES.json', 'R37 raw evidence (root-last)', 'historical run R37 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_TEXT_MODES_R38_20260904_175053\\02_results\\MODE_ANALYSIS.json', 'R38 raw evidence (mode census + twin pair)', 'historical run R38 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_WIKI_AUDIT_R39_20260904_180213\\02_results\\EDIT_PROPOSALS.json', 'R39 raw evidence (45 proposals)', 'historical run R39 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016\\02_results\\README_PROPOSALS.json', 'R40 raw evidence (README proposals)', 'historical run R40 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016\\02_results\\SEMANTICS_PROPOSALS.json', 'R40 raw evidence (ch09 proposals)', 'historical run R40 (immutable)'],
  ['D:\\Eudoria_Reconstruction\\01_Original_Files\\BNT_Models\\Models.bnt', '2003 ORIGINAL container (read-only; direct re-parse this round)', 'original game file (immutable)'],
  ['D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt', '9.3.5 container (read-only; direct re-parse this round)', 'pcg_install corpus (read-only)'],
  ['D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\docs\\nif\\README.md', 'wiki target (post-apply @ 077b8a4 == HEAD 8cd0bc3; READ-ONLY)', 'wiki @ commit 077b8a4 (reference == current)'],
  ['D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\docs\\nif\\09-semantics.md', 'wiki target (post-apply @ 077b8a4 == HEAD 8cd0bc3; READ-ONLY)', 'wiki @ commit 077b8a4 (reference == current)'],
  ['D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\docs\\nif\\10-containers-corpus.md', 'wiki chapter (READ-ONLY; iff + never-GRAMMAR sites)', 'wiki @ commit 077b8a4 (reference == current)'],
  ['D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\docs\\nif\\11-open-problems.md', 'wiki chapter (READ-ONLY; iff + completeness sites)', 'wiki @ commit 077b8a4 (reference == current)'],
  ['D:\\Eudoria_Reconstruction\\00_PROJECT_CONTEXT\\PE_AUTO_LOOP.json', 'loop state (READ-ONLY; +236-lines site; WRITER-scope - not written)', 'mutable live state (hash valid at read time only)']
];
for (const [p, role, scope] of srcs) {
  if (!fs.existsSync(p)) throw new Error('missing source: ' + p);
  rows.push([p, role, hash(p), scope].map(q).join(','));
}
const head = ['source_path_full', 'role', 'sha256', 'snapshot_time_scope'].map(q).join(',');
const note = [q('D:\\Eudoria_Reconstruction\\99_Audits\\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\\artifact_index.csv (THIS FILE)'),
  q('this manifest itself â€” intentionally NOT hash-listed: a file cannot contain its own SHA-256 (documented exclusion, NOT a placeholder; all other rows carry real in-run hashes)'),
  q('SELF_EXCLUDED_BY_CONSTRUCTION (documented)'), q(SCOPE_RUN)].join(',');
const out = [head, note].concat(rows).join('\r\n') + '\r\n';
fs.writeFileSync(RUN + '/artifact_index.csv', out);
console.log('artifact_index.csv written: ' + (rows.length + 1) + ' entries incl. the self-exclusion row; manifest self-hash impossibility documented.');
