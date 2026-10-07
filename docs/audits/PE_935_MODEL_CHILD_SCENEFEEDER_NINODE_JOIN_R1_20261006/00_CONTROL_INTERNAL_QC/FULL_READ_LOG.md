# FULL_READ_LOG — INDEPENDENT INTERNAL QC — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

QC_SCOPE = INDEPENDENT_INTERNAL_QC_MODEL_CHILD_SF (LOAD_BEARING depth, fresh context).
QC worker: pe-master-auditor (PE-MASTER direct dispatch, NO_NESTED_TASKS, STATIC-ONLY,
zero runtime). Read mode: FULL_READ (complete file contents, no heading-skipping).
Read start: after identity preflight (contract/handout/EXE/git all hash-verified first).

## Governing inputs (read IN FULL before the package)

| file | size | SHA256 (my own measurement) | verdict |
|---|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_PROMPT_REVIEW_20261006\OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md | 15,348 | F929D2C03B1D078BD69BDD206B0CF51DE5F393A0CE6D39618ED87819D043F3C8 | MATCH dispatch pin; §0–§7 read in full |
| C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_MODEL_JOIN_COMPARISON_RESEARCH_R2_20261006\HANDOFF_NOTES.md | 1,641 | D531B56AB0C1FD180A31DABC5DACAAE289372CA7B8FD8EC8BAAC565FAB0E4355 | MATCH dispatch pin; items 1–10 read in full |
| D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH pinned target (read-only byte source) |
| git HEAD (repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean) | — | 24f45e0108b922c26ff584fee9ef7749de0390b6 | == BASE; no tracked modifications; package untracked |

## Package files — ALL 32 read in full

Root (14): GOVERNANCE_DECISION.md, INPUT_IDENTITIES.md, INPUT_IDENTITIES.json,
PRE_REGISTERED_ANCHORS.md, FUNCTION_BUDGET.csv, EDGE_LEDGER.csv, CANDIDATE_LEDGER.csv
(incl. the full CAND-4 row, cross-checked against the build_ledgers.py row definition and
against my own regenerated copy — byte-identical), CLAIM_MATRIX.csv, QC_REPORT.md,
FINAL_REPORT.md, PE_MASTER_REVIEW.md, EVIDENCE_INDEX.md, HANDOFF.md, MANIFEST_SHA256.csv.

01_RAW (11): REPIN_ANCHOR_WINDOWS.txt, FUN_008BD720_DECODE.txt,
FUN_00528E50_CONTINUATION.txt, FUN_509x_SF_METHODS.txt, FUN_00509850_FULL.txt,
FUN_007BF500_DECODE.txt, SF20_WRITER_CENSUS.txt, SF20_EXTERNAL_WRITER_SCAN.txt,
FUN_006A3930_CHAIN_REPIN.txt, FUN_0050A310_DECODE.txt,
FUN_007B5810_ORACLE_BYTE_PROOF.txt.

03_SCRIPTS (7): build_ledgers.py, ledger_build_results.json, make_manifest.py,
qc_reverify.py, qc_reverify_results.json, qualification_gate.py,
qualification_results.json.

## My measurement coverage over what was read

- 61 independent checks in qc_independent_repins.py (own PE mapper, own raw byte reads,
  own subset x86 decoder for instruction boundaries, own rel32 arithmetic, own data reads):
  ALL 61 PASS (qc_independent_repins_results.json).
- 23 raw windows re-read from the EXE and compared byte-for-byte with the 01_RAW BYTES
  records: ZERO mismatches (check I1).
- 31 manifest rows fully re-hashed + size-checked: zero missing/extra/duplicate/mismatch
  (checks K1/K2; 32nd file = the self-excluded manifest).
- All 4 CSVs regenerated from the pinned build_ledgers.py (redirected to a temp dir) and
  compared byte-for-byte with the on-disk CSVs: IDENTICAL (ledger_regeneration_check.json).
- qualification_gate.py replayed (OUT redirected): results byte-identical to the package's
  qualification_results.json; 3 own falsifier variants executed (byte mutation, +A, +A+D):
  gate_tests_summary.json OVERALL=PASS.
- Oracle sources re-hashed (NiNode.cpp 38C7A1DE…/33,897; NiAVObject.cpp 72E08371…/33,215):
  both MATCH. 3 private research reports re-hashed: all MATCH. Contract + HANDOFF_NOTES
  re-hashed: MATCH.
- §2 source packages spot-check: both prior packages unmodified vs HEAD; their
  FINAL_REPORT.md files hash-match their own committed manifests
  (MICRO_R1 39DA4D86…/14,656; POST_AUDIT_CORRECTION B0C7987B…/9,541).
- AUDIT_ENTRYPOINT.md: zero mentions of this RUN_ID; git diff vs HEAD empty (untouched).
- Write-time (mtime) ordering of all 31 pre-QC package files captured (timing evidence).

## NOT_CHECKED by this QC (explicit — see QC_REPORT_INTERNAL.md for the boundary reasons)

- 3 private research reports' CONTENT (hash-verified only — they are executor inputs, not
  package evidence; their content was not re-audited by me).
- The 10 BASE prior package files' content (identity via (BASE_SHA, path); spot-check of
  2 packages' FINAL_REPORTs vs their manifests only).
- Foreign untracked dirs: byte-level untouchedness NOT verifiable (no baseline hashes
  exist); verified at inventory level only (6 roots, consistent with INPUT_IDENTITIES and
  git status).
- The private scratch dir (outside the repo; registered by the executor; not inventoried
  by the QC).
- All functions the executor left undecoded (FUN_006C66D0, FUN_007BF470, FUN_0050A1E0,
  FUN_005246E0, FUN_00509670, FUN_005095C0, FUN_007B5A00, FUN_006C0EC0/ED0/FA0/FB0/F90/
  10B0, FUN_006C3640, FUN_007B55E0/788570/7790D0, FUN_006C8B20/BB0, FUN_006C0D50,
  FUN_0072FCE0, FUN_0048BAC0, FUN_0096CDD0, FUN_007BF900/007BF630, FUN_007B6000 beyond
  the boundary decode, FUN_00509330 beyond the prologue+vtable store, the resource
  completion chain, FUN_007B68B0) — QC performed NO new RE semantics on them (QC-RE
  boundary of the dispatch: my measurements verify existing pins/claims only).
- Runtime anything (STATIC-ONLY; no client execution by the executor and none by the QC).
