# HANDOFF_QC — PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007

Executor of THIS QC: pe-master-auditor (PE-MASTER direct dispatch, NO_NESTED_TASKS,
RECORDS/QC-MACHINERY ONLY). Fresh-context independent internal QC of the correction
package PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007
(pre-persistence, untracked, HEAD == BASE 064b7f4aa4f3961f1a44212b2423e298eb51c291).
This QC wrote ONLY under 00_CONTROL_INTERNAL_QC/. No commit, no push, no entrypoint
edit, no executor-record edits, no new RE/EXE regions.

## TERMINAL BLOCK (actual measured)

```text
QC_RUN_ID = PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007
ASSIGNMENT_MODE = INTERNAL_QC (independent, fresh context, LOAD_BEARING depth)
AUDITED_RUN = PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007
BASE_SHA = 064b7f4aa4f3961f1a44212b2423e298eb51c291 (HEAD unchanged; zero tracked mods)
EXE = 8,015,872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (own re-hash)
QC_VERDICT = QC_PASS_WITH_FINDINGS
FINDINGS =
  F-QC-1 (P1) EDGE_BUDGET_RECONSTRUCTION.csv omits >=7 recorded callsite pairs
    (12 callsite occurrences, each machine-verified from the pinned EXE at its
    already-published VA); the 4x-repeated "EVERY recorded callsite" census claim is
    FALSIFIED; under the census's own four-part criterion the omitted
    FUN_006C0F90/FUN_006C10B0 pairs are SUMMARY_SEMANTIC_NEW candidates (same record
    depth as the counted R09/R10), so MINIMUM_ANALYZED_EDGE_COUNT = 20 is understated
    (defensible minimum >= 22). J2 headline conclusions (R01 present; exceedance;
    ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL vs MAX 6; RETROACTIVE_PRIOR_AUTHORIZATION
    = NO) all STAND. Records-only amendment required before J2 closure.
  F-QC-2 (P3) census boundary-documentation imprecision (header exclusion-note vs
    actual X-class practice; O-class rows enumerated for only 2 of >=4 windows with
    out-of-extent continuation calls). Fold into the same amendment.
  F-QC-3 (P3) executor's independent post-generation manifest re-hash exists only in
    its un-persisted terminal handoff; my own independent bijection re-hash (zero
    mismatch over all 16 rows) covers the ground.
  F-QC-4 (P3, observation) executor's gate suite never exercised PIN_CHECK=FAIL /
    duplicate-id / unknown-type paths; my own falsifiers prove all three fire
    correctly. No gate defect.
J1 = CORRECTED (independently verified: my own M1-M5 fixtures ALL NOT QUALIFIED on
  the shipped gate; CTRL-A/B/C causal; synthetic clean = machinery test only; real
  CAND-4 NOT QUALIFIED; no bare-declaration acceptance; no synthetic->real relabel
  bypass incl. my perfect-relabel probe; no unrelated-byte pin bypass; no
  broken-connectivity bypass; REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED confirmed
  in code (598 lines, read to EOF) and at runtime; NO code path yields SCIENCE_PASS;
  PIN_CHECK byte-equality-only; M4/M5 mechanical vs M1-M3 policy split exactly per
  contract §4; renamed chain_id AND edge ids -> identical verdicts (no ID
  hard-coding). 23/23 own checks PASS.)
J2 = reconstruction replicated (70 rows; 21 counted; 20 distinct pairs — arithmetic
  replicates; R01 = 0x0050A3AF -> FUN_006C66D0 present and counted; all 64 declared
  E8/vtable targets replay MATCH via my own engine; ledger E1-E6 == census E-rows;
  MAX_NEW_INTERPROCEDURAL_EDGES = 6 in source PRE_REGISTERED_ANCHORS; FAIL + NO
  retroactive authorization recorded) — WITH the F-QC-1 census-completeness defect.
J3 = CORRECTED (source package 49/49 BASE-blob identical, aggregate
  ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b unchanged;
  FUN_00509850_FULL.txt byte-identical; incidental/out-of-scope labels present;
  no active transform promotion in the ACTIVE algebra; CONFIRMED_STATIC only in
  superseded/historical context — my own sweep over all 17 files).
SUPERSESSION/§7 = PASS (exactly the 5 contract-listed interpretations superseded with
  accurate historical quotes; exactly the 6 items preserved; historical
  PE_MASTER_REVIEW.md + source package immutable).
§10 = PASS (nine preserved statuses identical on both sides — my own parser; no new
  model/resource/visual conclusion; token sweeps CLEAN after literal-hit
  adjudication (all hits = sweep-literals inside the executor's own qc_correction.py)).
GOVERNANCE = PASS (verbatim human instruction matches the received dispatch text;
  contract-reference resolution annotation present; phase split ORCHESTRATOR_PHASE_
  SPLIT matches observed repo state; entrypoint untouched by the executor).
PACKAGE = PASS (17 files; manifest 16 rows self-excluded, entrypoint
  excluded-do-persistence noted in header; bijection zero mismatch by my independent
  re-hash; UTF-8/no-BOM/LF 17/17; no __pycache__; PE_MASTER_REVIEW.md = honest
  NOT_PERFORMED placeholder).
COUNTERS (mine vs executor claims) = 17 files ✓; 16 manifest rows ✓; 70 census rows ✓;
  21 counted rows ✓; 20 distinct pairs ✓ (arithmetic) but understated as a MINIMUM
  (F-QC-1); executor self-QC = exactly 30 checks, all ok, "30/30" consistent
  package-wide, ZERO "31/31" residue.
NEXT_PARENT_ACTION = PE-MASTER disposition of F-QC-1: recommended bounded
  records-only amendment (add the missing census rows with per-row class
  adjudication; re-derive the minimum (22 if FUN_006C0F90/FUN_006C10B0 count under
  the census's own criterion); re-state the census scope honestly; regenerate the
  manifest + bijection) BEFORE declaring the J2 correction closed and BEFORE
  persistence; alternatively persist with the finding explicitly open in the
  entrypoint row and order the amendment as a follow-up. NEXT_EXPERIMENT_AUTHORIZED
  = NO (this QC adds no authorization). This QC is internal only — not
  MASTER_ACCEPTED, not external Desktop post-audit, not PE-MASTER qualification.
HARD_STOP = YES (QC worker returns to PE-MASTER; no commit/push performed).
```

## Machine records of this QC (all under 00_CONTROL_INTERNAL_QC/)

- qc_source_immutable.py -> results_source_immutable.json (49/49 blob identity;
  aggregate ab21cbc3…; gate EF2D8E1F…; FUN_00509850_FULL.txt identical)
- qc_j1_independent.py -> results_j1_independent.json (23/23 checks; 16 gate cases
  incl. my M5B perfect-relabel, CONNECTED falsifier counterpart, PIN/SCHEMA/type
  falsifiers, ID-rename probes)
- qc_j2_j3_package.py -> results_j2_j3_package.json (census recount; 64-target
  replay ALL MATCH; 12/12 missing-callsite verifications; 7 absent pairs; §10
  nine-status both-sides; sweeps + adjudication notes; manifest bijection;
  UTF-8/LF scan)
- QC_REPORT_INTERNAL.md (full findings with exact paths/lines and the correction +
  revalidation predicate for each)
- FULL_READ_LOG.md (coverage algebra; NOT_CHECKED explicit)
- ARTIFACT_INDEX_QC.csv (artifact/generator/executed-command map)

Executed commands (Python 3.12.10): `python qc_source_immutable.py`,
`python qc_j1_independent.py`, `python qc_j2_j3_package.py` (all from
00_CONTROL_INTERNAL_QC/). EXE reads in this QC are exclusively at already-published
pin VAs (see QC_REPORT_INTERNAL §2/§3); no FUN_006C66D0/FUN_007BF470 decoding; no
new EXE regions; no runtime; no payloads.
