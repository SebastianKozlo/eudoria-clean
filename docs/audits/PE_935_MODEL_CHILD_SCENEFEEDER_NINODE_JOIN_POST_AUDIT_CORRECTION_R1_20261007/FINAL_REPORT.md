# FINAL_REPORT — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION (Desktop post-audit findings J1/J2/J3 only —
ZERO new science, ZERO new RE). Executor: pe-reconstruction (PE-MASTER direct dispatch,
NO_NESTED_TASKS). BASE_SHA 064b7f4aa4f3961f1a44212b2423e298eb51c291 (== origin/master ==
actual remote master, verified at preflight 2026-10-07T01:32:46-07:00). EXE pinned
D:\Eudoria_Reconstruction\pcg_install\Entropia.exe = 8,015,872 B / SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (re-verified; used ONLY to
re-verify already-published pins — no new EXE analysis, no new regions, no runtime, no
payload reads). The historical source package at BASE remains immutable and was re-hashed
unchanged (49/49 git-blob identity match, aggregate SHA256
ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b, before AND after work).

---

## 1. What this correction did (records and QC machinery only)

### J1 — corrected qualification gate (finding: the original gate accepted declarations
without physical evidence; five Desktop counterexamples M1–M5 all PASSed it as false
positives)

- The historical source gate (03_SCRIPTS/qualification_gate.py at BASE, SHA256
  EF2D8E1F01D63BD004CC8F4087BDBC8194F51EACC38579DC0B2AC2FCDCC400AD — the same identity the
  Desktop executed) is READ-ONLY and unchanged; it carries no positive-semantic-qualifier
  authority in the corrected lineage.
- QUALIFICATION_GATE_CORRECTED.py (this package) implements the contract §4 policy:
  REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED. It returns SEPARATE SCHEMA_CHECK / PIN_CHECK /
  STRUCTURAL_CONSISTENCY_CHECK (each PASS/FAIL/NOT_CHECKED strictly per the checks actually
  performed; NO PASS is a SCIENCE_PASS; no code path yields SCIENCE_PASS at all). A real
  chain NEVER receives automatic science qualification from declarative fields; where
  semantic assertions cannot be bound to physical evidence, the verdict is NOT_QUALIFIED +
  MANUAL_PHYSICAL_EVIDENCE_REQUIRED. A synthetic fixture may PASS only as
  SYNTHETIC_MACHINERY_TEST_ONLY.
- Machine result (03_SCRIPTS/gate_corrected_results.json, OVERALL = PASS): the real CAND-4
  chain REMAINS NOT QUALIFIED (A and D unresolved); M1–M5 are ALL NOT QUALIFIED. Honest
  rejection-mechanism split: M4 (broken provenance connectivity) and M5 (synthetic→real
  top-level relabel) additionally FAIL MECHANICAL predicates (P_CONNECT; SCHEMA
  synthetic-marking consistency) — clean PASS → mutated FAIL on the same checker; M1/M2/M3
  are NOT caught by any mechanical predicate (their substituted byte pins are REAL EXE bytes
  at the pinned VAs — PIN_CHECK verifies byte equality only and never semantic binding) and
  are rejected BY POLICY, uniformly applied to every real chain including the UNMUTATED
  real CAND-4. This establishes THE ABSENCE OF AUTOMATIC SCIENCE PROMOTION, not validator
  detection of specific wrong opcodes/endpoints (disclosed in GATE_COUNTEREXAMPLES.json).
- Original CTRL-A/B/C retained: causal mechanical FAILs on their proper predicates.
- No candidate-ID/mutation-ID hard-coding: renamed-chain probes return identical verdicts.
- Corrected status: QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY.
  No general semantic verifier for the EXE was built (contract §4 forbids it here).

### J2 — edge-budget reconstruction (finding: "6/6 edges" measured list length, not
performed scope; minimum analyzed edges >= 7 despite the ledger)

- EDGE_BUDGET_RECONSTRUCTION.csv (amended per internal QC F-QC-1/F-QC-2 — see §1a and
  QC_REPORT.md §9): a records-only census of the defined evidence classes over the EXISTING
  source-run artifacts — it enumerates every interprocedural callsite recorded at instruction
  level or summary level in the persisted source materials (83 rows: 70 pre-amend + 13
  amendment rows), classified LEDGER_COUNTED (E1–E6) / SUMMARY_SEMANTIC_NEW (R01–R17) /
  RAW_VISIBLE_NOTED (N01–N03) / RAW_VISIBLE_ONLY (V01–V15) / PROTOCOL_SHAPE_ONLY (P01–P05) /
  REPIN_PRIOR_SCOPE (X01–X31) / OUT_OF_ANALYZED_EXTENT (O01–O06), each row citing its
  SOURCE_RECORDS with an explicit per-row NOT_COUNTED_REASON on every uncounted row; the
  known non-enumerated residue (the FUN_007BF500 window's raw-byte-only continuation calls)
  is disclosed in the census header — this is a census of the defined classes over existing
  artifacts, NOT a claim that every interprocedural callsite of the EXE is enumerated. The
  mandated edge
  0x0050A3AF -> FUN_006C66D0 (receiver = manager; return EAX -> EDI @0x0050A3B7; used as the
  CAND-4 child argument; callee body not decoded — which does NOT remove the edge) is row
  R01.
- Counting convention: edge = distinct (CALLER, CALLEE) pair. Minimum analyzed NEW pairs =
  6 (ledger) + 16 (summary-semantic-new; R01–R17 minus the R11/R12 same-pair callsite
  duplicate) = 22 (re-derived by the F-QC-1 amendment — the internal QC adjudicates the
  FUN_006C0F90/FUN_006C10B0 manager-method pairs as meeting the census's own four-part
  record criterion on the same record depth as R09/R10; equals the internal QC's machine
  re-derivation of 22; the pre-amend value 20 was understated).
  ACTUAL_ANALYZED_EDGE_COUNT is deliberately NOT reported — the
  semantic-analysis boundary is definition-sensitive at the lower census classes (documented
  per row with explicit NOT_COUNTED_REASON; NOT adjudicated by this correction or by the
  amendment); 22 is the strongest defensible lower bound (and 22 >= 7 as the Desktop
  independently established).
- MAX_NEW_INTERPROCEDURAL_EDGES = 6 is NOT retroactively changed (source
  PRE_REGISTERED_ANCHORS.md). Therefore:
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL — recorded honestly.
  RETROACTIVE_PRIOR_AUTHORIZATION = NO — no fabricated prior authorization; no
  present-human-exception adjudication is created by this correction.
- Retracted/superseded interpretations (new records only; historical files immutable):
  "6/6 edges, exhausted not exceeded"; "ZERO after-the-fact exceptions"; every whole-run
  process-compliance interpretation depending on them (including the source
  PE_MASTER_REVIEW.md line 18/22 wording — superseded as ACTIVE interpretation; see
  SUPERSESSION.md). The source run's technical byte evidence and preserved partial science
  are NOT falsified by the exceedance — the whole source package re-hashed unchanged.

### J2a — F-QC-1/F-QC-2 records amendment of the census (internal QC of this package; records-only)

The fresh-context independent internal QC of this correction package
(00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md, QC_RUN_ID
PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007, verdict QC_PASS_WITH_FINDINGS)
machine-verified that the pre-amend census was NOT a census of "every recorded callsite"
(its F-QC-1, P1): 12 recorded callsite occurrences (7 absent pairs + 5 contextual
FUN_006A3930-window E8s) plus window-continuation records were missing, and the pre-amend
MINIMUM_ANALYZED_EDGE_COUNT = 20 was understated. PE-MASTER adjudication:
AMEND_REQUIRED_BEFORE_PERSISTENCE. Executed as a records-only amendment of this package
(zero new RE; every EXE byte the QC touched was at an already-published VA; this amendment
opens NO new EXE region and decodes NO new body): 13 census rows added (R16/R17 counted
SUMMARY_SEMANTIC_NEW per the four-part criterion; X28–X31 REPIN_PRIOR_SCOPE; V11–V15
RAW_VISIBLE_ONLY; O05/O06 OUT_OF_ANALYZED_EXTENT), MINIMUM re-derived 20 -> 22 (method:
23 counted rows - the single counted same-pair callsite duplicate R12 = 22 distinct pairs),
the 4 false "every/full census" claims re-stated honestly (census header; FINAL_REPORT §1
J2; HANDOFF J2; DESKTOP_FINDINGS_DISPOSITION J2 — plus the same-family "ALL 70" wording in
FINAL_REPORT §5), the F-QC-2 boundary-documentation imprecision corrected (the actual X-class
listing practice; O-class completed; the FUN_007BF500 raw-byte-only continuation residue
disclosed as explicit incompleteness), and the consequential numbers propagated to
CORRECTED_STATUS_ALGEBRA.md / SUPERSESSION.md / HANDOFF.md / DESKTOP_FINDINGS_DISPOSITION.md /
QC_REPORT.md. ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL is UNCHANGED (22 > 6; the pre-amend 20
already exceeded MAX 6); RETROACTIVE_PRIOR_AUTHORIZATION = NO UNCHANGED; every preserved
science status UNCHANGED. Full amend record with per-row adjudications: QC_REPORT.md §9.

### J3 — transform-scope correction (finding: new transform semantics promoted outside the
contractually permitted transform scope)

- PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED: every FUN_00509850 raw window and
  measurement in the source package is unchanged (re-hashed == BASE blobs; the QC verifies
  01_RAW/FUN_00509850_FULL.txt specifically and the whole package generally). No new
  transform RE, no re-analysis.
- CONTRACTUAL_PROMOTION_STATUS is now separated from the measurements: the source run's
  SAME_INSTANCE_TRANSFORM_RELATION (historical value CONFIRMED_STATIC — superseded context)
  is NOT an active run-qualified conclusion of the corrected lineage.
- NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION.
- SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE. It is
  NOT described as inherited/re-pinned, and NO prior human authorization for the promotion
  is claimed. Future acceptance of the measured relation as a standing conclusion requires a
  NEW, explicit, present human decision — none exists.

## 2. Preserved science (unchanged — contract §3/§10)

SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED ·
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (PARENT_SCOPE =
EXAMINED_ACLD_PLUS_18_SF_INSTANCE; the CMO+0xC0 holder is a different instance; no
identity/CMO-transform transfer into the ACLD chain) ·
JOIN_OPERATION = STRONGLY_SUPPORTED (not promoted) ·
CHILD_MODEL_PROVENANCE = UNRESOLVED · CHILD_VISUAL_ROLE = UNRESOLVED ·
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED · RUNTIME_JOIN_OBSERVED = NO ·
WORLD_XYZ_RECOVERED = NO · STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED ·
HISTORICAL_INSTANCE_DATA_RECOVERED = NO · CANONICAL_GATE_EFFECT = NONE ·
NEXT_EXPERIMENT_AUTHORIZED = NO.
No new model/resource/visual conclusion appears anywhere in this package (machine-checked).
The 24 windows / 25 pins / 17 rel32 targets were NOT re-executed as new science; persisted
physical evidence was only re-hashed / parsed / replayed as correction QC.

## 3. What remains OPEN (honest; corrections are not closed by this execution)

- A (CHILD_PROVENANCE) and D (CHILD_VISUAL_ROLE) remain UNRESOLVED; FUN_006C66D0 and
  FUN_007BF470 remain undecoded (and were not decoded by this correction); the next material
  RE anchor remains the getter FUN_006C66D0 / its result provenance on the ACLD path — NOT
  authorized by this run.
- The census boundary at the RAW_VISIBLE / REPIN classes is documented but not adjudicated;
  an ACTUAL total would require adjudication this correction does not perform (also not
  performed by the F-QC-1/F-QC-2 amendment). The known non-enumerated residue (the
  FUN_007BF500 window continuation calls — raw-byte level only, no persisted instruction
  decode) is disclosed in the census header (F-QC-2 disposition).
- The measured transform relation is neither confirmed nor falsified as science by this
  records correction; it is simply not a run-qualified conclusion of the corrected lineage.
- The independent PE-MASTER audit of THIS package is pending; the independent Desktop
  post-audit of THIS correction is NOT_PERFORMED. Publication decisions belong to the
  persistence phase; publication != acceptance.

## 4. Package, QC and phase boundary

- Package = the records listed in MANIFEST_SHA256.csv (generated LAST and REGENERATED after
  the F-QC-1/F-QC-2 records amendment per the every-write-after-the-manifest rule; scope =
  the same executor-phase scope as before the amendment — every physical correction-package
  file (the J1/J2/J3 correction records, 03_SCRIPTS/ tools+results) minus the manifest
  itself and minus the read-only 00_CONTROL_INTERNAL_QC/ QC records, which were never in
  the executor-phase manifest scope; the AUDIT_ENTRYPOINT.md row is EXPLICITLY OUT of this
  phase's manifest scope — excluded pending persistence, noted in the manifest header; the
  persistence phase regenerates the manifest over the final physical package). This
  executor does NOT edit AUDIT_ENTRYPOINT.md (proposed newest-first
  row in HANDOFF.md) and does NOT commit/push (the verbatim human authorization for
  commit/push in the contract allowlist is executed by the PE-MASTER persistence phase after
  its own audit; RESULTING_SHA = NONE in this phase).
- Fresh-context internal QC = 03_SCRIPTS/qc_correction.py ->
  03_SCRIPTS/qc_correction_results.json (SELF_CHECK; NOT independent Desktop post-audit; NOT
  PE-MASTER qualification): J1/J2/J3 + §10 + governance/encoding checks — see QC_REPORT.md.
- All package files are UTF-8 no-BOM with LF endings; no __pycache__; foreign untracked
  groups untouched; no tracked changes; HEAD unchanged at BASE.

## 5. SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Full raw census where claimed: the J2 census enumerates the defined evidence classes
      over the existing source-run artifacts (83 rows after the F-QC-1 amendment; every
      uncounted row carries an explicit NOT_COUNTED_REASON; the FUN_007BF500 window's
      raw-byte-only continuation residue is disclosed in the census header — NOT a claim
      that every interprocedural callsite of the EXE is enumerated); every DIRECT_E8 and
      VTABLE_SLOT row's target arithmetic was mechanically replayed against the pinned EXE
      by the QC — ALL MATCH (replay of already-published arithmetic, not new RE); the 12
      internal-QC-machine-verified amendment callsites are all present as census rows
      (machine re-derivation in QC_REPORT.md §9).
- [x] All gates honestly evaluated: the corrected gate's self-checks all PASS; the QC
      independently re-derives the M1–M5/CTRL/real-chain verdicts and the 5 real-chain pins.
- [x] Meaningful negative controls: M1–M5 + CTRL-A/B/C + synthetic clean + real CAND-4 +
      renamed-chain ID probes (no ID hard-coding); J2: ledger==6, mandated edge present,
      max==6, compliance FAIL recorded, no retroactive-authorization token; J3: source
      re-hash zero diff, incidental labels present, no active promotion in the ACTIVE
      algebra.
- [x] Correct source/generator hashes: contract, Desktop report + counterexamples, BASE
      blobs, source package aggregate (before AND after), EXE — all re-measured, MATCHING.
- [x] No default-success fallback: M1–M3's policy rejection is disclosed as policy (not
      detection); the ACTUAL edge count is NOT claimed (only the defensible minimum 22);
      corrections are NOT claimed closed by this execution (including the F-QC-1/F-QC-2
      amendment — the PE-MASTER audit of the amended package remains pending).
- [x] Limits respected: no new RE; no new EXE regions; no FUN_006C66D0/FUN_007BF470
      decoding; no runtime; no payload reads; no ExtraData readback; no new transform
      analysis; historical files untouched; foreign untracked untouched.
- [x] Manifest LAST + bijection: manifest generated last AND regenerated after the
      F-QC-1/F-QC-2 records amendment (every write after the manifest = regeneration +
      re-verification — honored), self-excluded, entrypoint excluded pending persistence,
      same executor-phase scope as before the amendment; bijection zero
      missing/extra/duplicate/size/SHA mismatch (generator self-check + independent
      post-generation re-hash recorded in QC_REPORT.md §9 and the terminal handoff).
