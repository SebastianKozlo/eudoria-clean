# QC_REPORT — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

SELF-CLASSIFICATION: this is the executor's own fresh-context internal QC (SELF_CHECK) of
the correction package. It is NOT an independent external Desktop post-audit and NOT a
PE-MASTER qualification. Machine record: 03_SCRIPTS/qc_correction.py ->
03_SCRIPTS/qc_correction_results.json (OVERALL = QC_PASS; 30/30 checks). The QC was executed
twice: pass 1 validated the package as built; after the QC report and the handoff record were
written, pass 2 regenerated the machine record so that its sweeps cover the COMPLETE package
(both passes QC_PASS; the QC does not repair executor records in place — it only records
findings and re-verifies).

AMENDMENT RECORD (2026-10-07): AFTER the executor's SELF_CHECK, the PE-MASTER-dispatched
fresh-context INDEPENDENT internal QC of this package (00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md,
QC_RUN_ID PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007) returned
QC_PASS_WITH_FINDINGS (F-QC-1 P1 / F-QC-2 P3 / F-QC-3 P3 / F-QC-4 P3-observation), and the
F-QC-1/F-QC-2 records-only amendment was executed IN this package per PE-MASTER adjudication
AMEND_REQUIRED_BEFORE_PERSISTENCE — see §8 (F-QC-4 record-note) and §9 (the full amend
record). The 03_SCRIPTS machine record above (30/30) remains the TRUE record of the
PRE-AMEND census arithmetic; the POST-AMEND verification is the machine re-derivation in §9
and the internal QC's own independent results (00_CONTROL_INTERNAL_QC/results_*.json).

## 1. What the QC independently measured (fresh reads; no executor trust)

- Pinned EXE re-verified: 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  (fail-closed inside the QC; used ONLY to replay already-published pin/target arithmetic —
  no new RE, no new EXE regions).
- SOURCE_RUN_PACKAGE re-hash: all 49 BASE blobs re-derived from disk bytes — 49/49 git-blob
  identity match, package aggregate SHA256
  ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b == the pre-work value
  (zero diff; the source package is immutable and was neither edited nor absorbed).
  01_RAW/FUN_00509850_FULL.txt (the J3 physical transform record) additionally re-verified
  against its BASE blob — byte-identical.

## 2. J1 checks (contract §9)

- Corrected-gate machine record OVERALL = PASS with all self-checks true.
- M1–M5 (recreated independently from contract §4): ALL NOT QUALIFIED.
- M4 and M5 additionally FAIL MECHANICAL predicates on the same checker (P_CONNECT declared
  provenance connectivity; SCHEMA synthetic-marking consistency) — clean PASS -> mutated FAIL.
- M1/M2/M3 PASS mechanically and are rejected BY POLICY — disclosed honestly as the absence
  of automatic science promotion, NOT as detection of specific wrong opcodes/endpoints
  (their substituted byte pins are real EXE bytes at the pinned VAs; PIN_CHECK is
  byte-equality only).
- Original CTRL-A/B/C retained: causal mechanical FAILs on their proper predicates.
- Clean synthetic fixture: machinery PASS only, science verdict SYNTHETIC_MACHINERY_TEST_ONLY.
- Real CAND-4 remains NOT QUALIFIED (A and D unresolved); its 5 published byte pins were
  independently re-read from the EXE by the QC — ALL MATCH.
- No case anywhere receives SCIENCE_PASS.
- Renamed-chain probes return identical verdicts — no candidate-ID/mutation-ID rejection
  branch exists in the gate.

## 3. J2 checks (contract §9)

- EDGE_BUDGET_RECONSTRUCTION.csv parses: 70 census rows; COUNTED_IN_MINIMUM rows = 21
  (E1–E6 + R01–R15); distinct counted (caller,callee) pairs = 20. [PRE-AMEND measurement —
  true at measurement time; the independent internal QC then machine-proved the census
  INCOMPLETE (F-QC-1). POST-AMEND: 83 rows / 23 counted rows / 22 distinct counted pairs —
  machine re-derivation in §9; the internal QC's own 12-callsite table re-runs to zero
  absent pairs over the amended census.]
- The mandated 0x0050A3AF -> FUN_006C66D0 edge is present as row R01 (SUMMARY_SEMANTIC_NEW).
- Independent reconstruction basis re-read from the source records: the BASE
  EDGE_LEDGER.csv contains exactly E1–E6 (the ledger measured list length); the BASE
  FUNCTION_BUDGET row #7 itself records the uncharged getter edge ("child=FUN_006C66D0(manager)
  @0x0050A3AF"); the BASE PRE_REGISTERED_ANCHORS.md carries MAX_NEW_INTERPROCEDURAL_EDGES = 6.
- Mechanical replay: the rel32 target of every DIRECT_E8 census row and the vtable-slot
  target of every VTABLE_SLOT census row were recomputed by the QC from the pinned EXE —
  ALL MATCH (replay of already-published arithmetic; not new RE).
- ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL is recorded (20 > 6);
  RETROACTIVE_PRIOR_AUTHORIZATION = NO is recorded; the forbidden-token sweep
  (retroactive-authorization claim patterns) is CLEAN across the whole package
  (the QC script and its own results file excluded — they contain the tokens as check
  literals).

## 4. J3 checks (contract §9)

- The source evidence still exists unchanged (see §1: full source-package re-hash zero diff).
- The corrected records label the transform trace incidental/out-of-scope: NEW_TRANSFORM_TRACE
  = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION and
  SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE and
  PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED are all present.
- No active source-run transform promotion survives: the ACTIVE section of
  CORRECTED_STATUS_ALGEBRA.md contains no CONFIRMED_STATIC promotion (the historical value
  appears only in superseded/historical context — machine-checked).

## 5. §10 NO-UNINTENDED-SCIENCE-DIFF checks

- The 9 preserved statuses are identical in the source records (BASE CLAIM_MATRIX.csv /
  CANDIDATE_LEDGER.csv / FINAL_REPORT.md, re-read by the QC) and in the corrected ACTIVE
  status algebra — no unintended science diff.
- Overclaim-token sweep (new model/resource/visual conclusion patterns) CLEAN across the
  package (self-excluded).
- Every CONFIRMED_STATIC occurrence in the package sits in a supersession/historical context
  (line or +/-4 lines of context around it) — machine-checked CLEAN.

## 6. Governance/process checks

- Repo state: HEAD == 064b7f4aa4f3961f1a44212b2423e298eb51c291 (BASE unchanged); zero tracked
  modifications; untracked roots exactly = the 6 known foreign roots (untouched) + this
  run's OUTPUT_ROOT.
- No __pycache__ under OUTPUT_ROOT.
- Encoding: every package file UTF-8 no-BOM with LF-only line endings (machine-verified).

## 7. QC verdict

QC_VERDICT = QC_PASS (SELF_CHECK) — 30/30 checks, zero findings. Honest residual: the QC
does not adjudicate the census boundary classes (documented per row in
EDGE_BUDGET_RECONSTRUCTION.csv); it does not constitute an external Desktop post-audit of
this correction (NOT_PERFORMED) nor a PE-MASTER qualification (NOT_PERFORMED — placeholder
record pending the persistence phase). [Pre-amend verdict, kept as the true historical
record of the pre-amend package state. POST-AMEND STATUS: the independent internal QC of
this package returned QC_PASS_WITH_FINDINGS (F-QC-1 P1 / F-QC-2 P3 / F-QC-3 P3 / F-QC-4
P3-observation); F-QC-1/F-QC-2 are amended per §9 (records-only); F-QC-3 is resolved by the
manifest-regeneration discipline (final closure at persistence); F-QC-4 is recorded in §8.
The pre-amend SELF_CHECK's census-completeness limitation is exactly what F-QC-1 proved:
the executor's checks verified the arithmetic of the counted set, not its completeness.]

## 8. J1 strengthening note (internal QC F-QC-4 — record-note only; gate UNCHANGED)

The independent internal QC executed its own falsifiers against the shipped corrected gate
(hash-pinned source; 00_CONTROL_INTERNAL_QC/qc_j1_independent.py ->
00_CONTROL_INTERNAL_QC/results_j1_independent.json, 23/23 checks PASS): (a) PIN_CHECK FAIL
falsifier — one mutated expect byte produces PIN_CHECK = FAIL + mechanical FAIL (the byte
predicate fires; the executor's own pre-amend 10-case suite never exercised a PIN FAIL);
(b) SCHEMA duplicate-edge-id falsifier -> SCHEMA FAIL; (c) unknown-edge-type falsifier ->
SCHEMA FAIL. All three fire correctly on the shipped checker, and the executor's "PIN_CHECK
is byte-equality only" claim is CONFIRMED (strengthened, not weakened). GATE UNCHANGED by
this amendment: QUALIFICATION_GATE_CORRECTED.py is NOT modified (SHA256
B07B64FF2E3771E6CF728C03BB990C8A815B3ADB1FCCB06DBED0FE3B784F6517 — identical in the
regenerated manifest); no gate check, verdict, or policy changes; the J1 corrected statuses
(QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY; SCIENCE_PASS =
NOT_ISSUED_BY_ANY_TOOL_OF_THIS_CORRECTION) stand unchanged.

## 9. RECORD-REPAIR AMEND (records-only; executed 2026-10-07 after the independent internal QC)

Origin = the fresh-context independent internal QC of THIS package
(00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md, QC_RUN_ID
PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007, QC_VERDICT =
QC_PASS_WITH_FINDINGS), adjudicated by PE-MASTER: AMEND_REQUIRED_BEFORE_PERSISTENCE
(records-only; ZERO new RE — every EXE byte the internal QC touched was at an
already-published VA, and this amendment opens NO new EXE region and decodes NO new body).

- F-QC-1 (P1) AMENDED — EDGE_BUDGET_RECONSTRUCTION.csv extended by 13 rows with per-row
  SOURCE_RECORDS and four-part-criterion adjudication: R16 (FUN_0050A310 ->
  FUN_006C0F90 @0x0050A3B9) and R17 (FUN_0050A310 -> FUN_006C10B0 @0x0050A3CF) COUNTED as
  SUMMARY_SEMANTIC_NEW (the four-part criterion is met on the same record depth as the
  counted R09/R10 — internal-QC adjudication); X28 (FUN_00509330 -> FUN_0095D3C4
  @0x005093A0), X29 (FUN_00509330 -> FUN_0064B1E0 @0x0050948B), X30 (FUN_0050A050 ->
  FUN_007B5390 vtable slot 17 @0x0050A064), X31 (FUN_006A3930 -> FUN_0095D3C4
  @0x006A3A4D) = REPIN_PRIOR_SCOPE (NOT counted; re-pin convention); V11–V15 (the five
  contextual FUN_006A3930-window entry-aligned E8s: FUN_00401360 x2 / FUN_00485050 /
  FUN_0048CBB0 / FUN_00733340) = RAW_VISIBLE_ONLY (NOT counted; no summary semantic
  record); O05 (FUN_0050A310 -> FUN_005095C0 @0x0050A43A, the undecoded-tail call) and O06
  (the CH1b window-continuation call 0x006C3FFC -> FUN_006C3F50) = OUT_OF_ANALYZED_EXTENT
  (NOT counted). All 12 internal-QC-machine-verified callsites
  (results_j2_j3_package.json missing_recorded_callsites_verified) are now census rows;
  every COUNTED=NO row (pre-amend and added) carries an explicit NOT_COUNTED_REASON.
- MINIMUM_ANALYZED_EDGE_COUNT re-derived: 20 -> 22 (METHOD: 23 counted rows - the single
  counted same-pair callsite duplicate R12 (SAME_PAIR_AS R11) = 22 distinct pairs =
  6 ledger + 16 summary-semantic-new distinct pairs; equals the internal QC's own
  'minimum_if_omitted_pairs_counted' = 22). ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL
  UNCHANGED (22 > 6; the pre-amend 20 already exceeded MAX 6);
  RETROACTIVE_PRIOR_AUTHORIZATION = NO UNCHANGED; ACTUAL_ANALYZED_EDGE_COUNT remains
  NOT_REPORTED (the RAW_VISIBLE / REPIN boundary classes are documented per row and NOT
  adjudicated by this amendment).
- The false 4x 'every/full census' scope claim re-stated honestly (the QC's exact list):
  EDGE_BUDGET_RECONSTRUCTION.csv header line 1; FINAL_REPORT.md §1 J2; HANDOFF.md
  DESKTOP_FINDINGS J2; DESKTOP_FINDINGS_DISPOSITION.md J2 — plus the same-family "ALL 70"
  wording in FINAL_REPORT.md §5 SELF_CHECK. The census scope is now the honest
  defined-classes statement (census header line 1) with the known non-enumerated residue
  (the FUN_007BF500 raw-byte-only window continuation) disclosed in the census header.
- F-QC-2 (P3) AMENDED — the header's F-QC-5 exclusion note corrected to the actual X-class
  listing practice (X02/X04/X09/X10/X11 are raw E8-scan-list targets of the prior-decompiled
  caller, NOT prior-canon pins); the O-class enumeration completed for every window with
  instruction-level-recorded out-of-extent continuation callsites (O05/O06 added;
  FUN_008BD720 O01/O02 and FUN_00528E50_CONTINUATION O03/O04 unchanged); the FUN_007BF500
  window's raw-byte-only continuation residue disclosed as explicit incompleteness
  (census header line 6).
- F-QC-3 (P3): no package repair required; resolved by the manifest-regeneration
  discipline — this amendment REGENERATED MANIFEST_SHA256.csv LAST with full bijection and
  an INDEPENDENT post-generation re-hash (performed and disclosed here and in the terminal
  handoff); final closure at the persistence phase (which regenerates the manifest again
  with the entrypoint row over the final physical package).
- F-QC-4 (P3 observation): record-note only (see §8).
- Files amended (7): EDGE_BUDGET_RECONSTRUCTION.csv, FINAL_REPORT.md, HANDOFF.md,
  DESKTOP_FINDINGS_DISPOSITION.md, QC_REPORT.md (this section + the header amendment record
  + §3/§7 annotations + §8), CORRECTED_STATUS_ALGEBRA.md (MINIMUM 20 -> 22; FAIL '22 > 6';
  section-B items 3/4 numbers), SUPERSESSION.md (S-3/S-4 numbers). NOT modified:
  00_CONTROL_INTERNAL_QC/ (read-only QC layer), AUDIT_ENTRYPOINT.md (not edited by this
  executor), 03_SCRIPTS/ (the pre-amend machine records qc_correction.py /
  qc_correction_results.json are TRUE historical records of the PRE-AMEND census
  verification — not re-run against the amended census), GATE_COUNTEREXAMPLES.json,
  GOVERNANCE_DECISION.md (verbatim human instruction), INPUT_IDENTITIES.md (preflight
  record), PE_MASTER_REVIEW.md (placeholder), QUALIFICATION_GATE_CORRECTED.py (gate
  unchanged; see §8).
- Post-amend machine verification (this executor; records-only): the amended census parses
  to 83 data rows / 23 COUNTED_IN_MINIMUM rows / 22 distinct counted pairs; class counts
  LEDGER_COUNTED 6 / SUMMARY_SEMANTIC_NEW 17 / RAW_VISIBLE_NOTED 3 / RAW_VISIBLE_ONLY 15 /
  PROTOCOL_SHAPE_ONLY 5 / REPIN_PRIOR_SCOPE 31 / OUT_OF_ANALYZED_EXTENT 6; all 12
  internal-QC-verified callsites present (zero absent pairs); all 13 added rows' cited
  source-record lines verified present in the cited source artifacts (26 record-presence
  checks incl. the cited raw-window display lines, the CAND-4 PATH_CONDITIONS quotes, the
  PA anchor quotes, the source internal-QC tail-bytes record and the source HANDOFF/QC
  NOT_CHECKED lists); every COUNTED=NO row carries a NOT_COUNTED_REASON; all amended files
  UTF-8 no-BOM with LF-only line endings. The internal QC's revalidation predicate (its
  12-callsite machine table re-runs to zero absent pairs; the recounted distinct-pairs
  figure matches the re-derived minimum) is thereby satisfied.
- Preserved statuses UNCHANGED (contract §3/§10): SCIENCE_OUTCOME =
  PARENT_FOUND_CHILD_UNRESOLVED; EXACT_PARENT / JOIN_OPERATION / CHILD_MODEL_PROVENANCE /
  CHILD_VISUAL_ROLE / INSTANCE_MODEL_NODE_JOIN and every §10 status identical on both
  sides; no new model/resource/visual conclusion added anywhere; the historical source
  package untouched (read-only throughout this amendment); RETROACTIVE_PRIOR_AUTHORIZATION
  = NO; NEXT_EXPERIMENT_AUTHORIZED = NO.
