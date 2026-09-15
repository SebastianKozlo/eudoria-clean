# RUN_CONTRACT — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915

## Identity
- RUN_ID: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915
- RUN_CLASS: LOAD_BEARING (declared by PE-MASTER); RUN_TYPE: FORENSIC_REFERENCE_BASELINE
- ROLE: PE-RECONSTRUCTION executor under PE-MASTER governance (parent = PE-MASTER session; human ordered this run directly)
- TARGET: PCG_9_3_5 / Entropia Universe 9.3.5
- REPO: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean, branch master
- BASE_SHA (expected, verified S0): f3a3d401f1f254f32cee072260fdc15a6549d378
- PRIMARY CORPUS: D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt
- PHYSICAL PIN (contract): size=395412868, SHA256=C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0
- CONTRIBUTES_TO: EU935-M2 NIF/Models/Materials/Animation; EU935-M10 Original Client Fidelity; EU935-M11 PE Rosetta Completeness
- PARSER POLICY: REPORT-ONLY (no src/ edits; no parser fixes in this run)
- NO commit/push by executor (persistence by pe-master-auditor after QC + adjudication)

## S0 environment snapshot (executor-measured 2026-09-15)
- HEAD == f3a3d401f1f254f32cee072260fdc15a6549d378 == BASE_SHA (PASS)
- Dirty tree (pre-existing untracked, NEVER staged/touched): docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/, experiments/
- Models.bnt measured: size=395412868 (PASS), SHA256=C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 (PASS)
- Output root did not exist pre-run (clean). Local heavy-work root: D:\Eudoria_Reconstruction\99_Audits\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\
- Host: WinDev2407Eval (VM, local python 3.12.10)

## Scope bounds (binding)
- This run does NOT open M2, does NOT close M1, does NOT change roadmap, does NOT run further runs, does NOT run Entropia.exe, does NOT do runtime intervention.
- No edits: src/, package.json, runtime/, docs/nif/* (live), old audits (READ-ONLY), existing 99_Audits run dirs.
- Files NOT produced by executor (later phases): 06_REPORT/QC_AUDIT.md (fresh-context QC auditor), 06_REPORT/PE_MASTER_REVIEW.md (PE-MASTER adjudication, persisted by pe-master-auditor). G16/G17/G18 = PENDING_LATER_PHASE.
- Proprietary payload: original NIFs / Models.bnt contents NEVER enter the repo. Repo receives only derived CSV/JSON/MD + SHA manifests.

## Anti-circularity (binding, G2)
- Physical version/type census produced ONLY from own minimal BNT2 walk + own NIF header/type-table scanner (00_CONTROL/scripts/).
- pcg953_nif_manifest.csv = PARSER OUTPUT = CROSS-CHECK ONLY. R61, NifModelReader.js never used as census oracle.
- BNT2 structural knowledge from docs/nif/10-containers-corpus.md treated as PRIOR HYPOTHESIS; walker has own fail-closed invariants (EOF-exact consumption, offset+size bounds, name checks, negative controls: truncation / corrupt-count / wrong-endian).

## Provenance order (§21)
After final executor edits, one final pass: 1. SCRIPT_SHA256.csv → 2. 03_EVIDENCE/README.md → 3. 03_EVIDENCE/EVIDENCE_INDEX.csv → 4. 06_REPORT/MANIFEST_SHA256.csv (self-exclusion: MANIFEST_SHA256.csv does not hash itself; SCRIPT_SHA256.csv rows hashed in MANIFEST). Then rehash everything listed; zero missing rows; zero stale hashes; no __pycache__/.pyc.

## AMEND policy (§20)
If any post-QC correction edits an existing file: snapshot BEFORE to 00_CONTROL/PRE_EDIT/*.pre, record OLD SHA256, bounded edit, NEW SHA256, append entry to AMEND_LOG_R1.md (append-only, never overwrite earlier entries or snapshots). Regeneration of provenance after QC amendments = disclosed AMEND.

## STOP conditions (§25)
Models.bnt pin mismatch; unexplained census mismatch; contradictory 10.1 baseline sources; type boundary depending on parser assumptions; holdout failure; heuristic-matched custom layout; parser output used as physical oracle; docs-derived denominator; arbitrary world-slice narrowing to 1-2 types; UNKNOWN renamed to recovered semantic without proof. Conflict disclosed != failure; hidden conflict = failure.
