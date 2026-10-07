# DESKTOP_FINDINGS_DISPOSITION — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

RUN_CLASS = RECORDS_AND_QC_MACHINERY_CORRECTION (J1/J2/J3 only; zero new science, zero new RE).
External authority: the independent Desktop post-audit
`PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007` (REPORT.md 12,030 B /
SHA256 9A97EE46B84E81A1ADDB659CEAE8F95F9CBFF0738FAFD5A265B3D50227614C79; PRODUCTION_GATE_COUNTEREXAMPLES.json
23,166 B / SHA256 6632C6D11F712DBFD61FD3EE13875B4DB90910BE9D0CCE063955BE379F066D16) of the
audited commit 064b7f4aa4f3961f1a44212b2423e298eb51c291. Desktop verdict: REQUIRE_CORRECTIONS
(3×P2). The findings are handled below WITHOUT reinterpretation and without new physical
counterexample invention — the M1–M5 counterexamples were recreated independently from the
contract §4 text and replayed against the corrected gate (see QUALIFICATION_GATE_CORRECTED.py,
GATE_COUNTEREXAMPLES.json, 03_SCRIPTS/gate_corrected_results.json).

## J1 / P2 — production qualification gate accepts declarations without physical evidence

DESKTOP FINDING (verbatim substance): the production gate (SOURCE 03_SCRIPTS/qualification_gate.py,
gate() lines 106–164; PE_MASTER_REVIEW.md line 22) accepted a real chain on the strength of
declared fields alone: M1 (textual child provenance + identity=True + visual proof string) PASS,
M2 (parent-identity pin pointed at the correct bytes of the SF+0x20 STORE while the declaration
still claimed the SF+0x30 parent load) PASS, M3 (join-operation pin replaced with the 4-byte
accessor/RET @0x008BD720) PASS, M4 (provenance endpoints explicitly broken) PASS, M5 (synthetic
fixture relabelled top-level is_synthetic=False) PASS — five false positives.

DISPOSITION = CORRECTED (machinery rebuilt under this package; the historical gate at BASE is
READ-ONLY and unchanged).

- QUALIFICATION_GATE_CORRECTED.py implements the contract §4 policy:
  REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED. The tool returns SEPARATE checks — SCHEMA_CHECK,
  PIN_CHECK, STRUCTURAL_CONSISTENCY_CHECK — each PASS/FAIL/NOT_CHECKED strictly per what was
  actually checked; NO PASS of any of them is a SCIENCE_PASS. No code path yields SCIENCE_PASS.
- A synthetic fixture may PASS only as a SYNTHETIC_MACHINERY_TEST (the baseline does; it is
  never PCG evidence and never promotes INSTANCE_MODEL_NODE_JOIN).
- A real chain NEVER receives automatic science qualification from declarative fields; where
  the tool cannot bind every required semantic assertion to physical evidence records and
  exact endpoints, it returns NOT_QUALIFIED + MANUAL_PHYSICAL_EVIDENCE_REQUIRED.
- The real CAND-4 chain REMAINS NOT QUALIFIED (A and D unresolved) — verified by machine run.
- M1–M5 recreated independently (contract §4 mutation text; the Desktop JSON was an input
  identity only) and replayed against the corrected gate: ALL FIVE = NOT QUALIFIED.
  Honest rejection-mechanism split (recorded in GATE_COUNTEREXAMPLES.json):
  - M4: additionally caught by the mechanical P_CONNECT structural predicate (declared
    provenance to_object != the join child argument) — clean PASS -> mutated FAIL on this checker.
  - M5: additionally caught by the mechanical SCHEMA synthetic-marking-consistency predicate
    (a real-declaring chain may not contain edge-local synthetic=True edges) — clean PASS ->
    mutated FAIL on this checker.
  - M1/M2/M3: NOT caught by any mechanical predicate (M1's added edges carry no byte claims;
    M2's substituted pin is a REAL EXE STORE at the pinned VA; M3's substituted pin is a REAL
    accessor/RET at the pinned VA — PIN_CHECK is byte-equality only and never claims semantic
    binding). Their NOT QUALIFIED is produced BY POLICY (REAL_SCIENCE_AUTO_QUALIFICATION=DISABLED,
    applied uniformly to every real chain including the UNMUTATED real CAND-4). This run
    therefore establishes THE ABSENCE OF AUTOMATIC SCIENCE PROMOTION, not validator detection
    of a specific wrong opcode/endpoint.
- Original CTRL-A/B/C retained and replayed: causal mechanical FAIL on their proper predicates.
- No candidate-ID/mutation-ID hard-coding anywhere in the verdict logic — proven by renamed-chain
  probes returning identical verdicts (gate_corrected_results.json id_hard_coding_probes).
- Required corrected status recorded: QC_POSITIVE_CHAIN_QUALIFICATION =
  NOT_ESTABLISHED_AS_GENERAL_AUTHORITY. The schema/pin/structure validations of this tool have
  ONLY the declared mechanical scope; this correction grants no general positive semantic
  authority to anything.
- STILL OPEN (honest): a future general semantic verifier for the EXE is NOT built (contract
  forbids it in this correction); binding declared semantics to physical evidence remains a
  manual physical-evidence adjudication outside this tool.

## J2 / P2 — edge budget undercount: minimum analyzed interprocedural edges >= 7 despite ledger 6/6

DESKTOP FINDING (verbatim substance): the ledger's "6/6 edges" measured the length of the
ledger list, not the performed scope. The interprocedural edge 0x0050A3AF -> FUN_006C66D0 was
analyzed semantically in caller function #7 (receiver = manager, CALL target, return EAX->EDI,
role of the result as the CAND-4 child argument) but was never charged; not decoding the
callee body does not remove the edge from the budget. A single missing row already gives
>= 7 against the contractual maximum of 6. The source-run QC check S9 only verified
len(ed)==6 and could not detect a missing row.

DISPOSITION = CORRECTED (records-only reconstruction; no new RE; no new callgraph/xref census —
the reconstruction reads ONLY already-persisted source-run materials).

- EDGE_BUDGET_RECONSTRUCTION.csv (AMENDED per the internal QC of this correction package —
  findings F-QC-1 (P1) / F-QC-2 (P3), PE-MASTER adjudication AMEND_REQUIRED_BEFORE_PERSISTENCE;
  records-only, zero new RE): a records-only census of the defined evidence classes over the
  EXISTING source-run artifacts — every interprocedural callsite recorded at instruction
  level or summary level in the persisted source materials (83 rows = 70 pre-amend + 13
  amendment rows), classified LEDGER_COUNTED (E1–E6) / SUMMARY_SEMANTIC_NEW (R01–R17) /
  RAW_VISIBLE_NOTED (N01–N03) / RAW_VISIBLE_ONLY (V01–V15) / PROTOCOL_SHAPE_ONLY (P01–P05) /
  REPIN_PRIOR_SCOPE (X01–X31) / OUT_OF_ANALYZED_EXTENT (O01–O06), with per-row SOURCE_RECORDS
  citations and an explicit NOT_COUNTED_REASON on every uncounted row; the known
  non-enumerated residue (the FUN_007BF500 window's raw-byte-only continuation calls) is
  disclosed in the census header — this is NOT a claim that every interprocedural callsite
  of the EXE is enumerated. The mandated 0x0050A3AF -> FUN_006C66D0 edge is row R01.
- Counting convention: an interprocedural edge = a distinct (CALLER, CALLEE) pair. Distinct
  newly-analyzed pairs = 6 (ledger) + 16 (summary-semantic-new: R01–R17 rows minus the
  R11/R12 same-pair callsite duplicate) = 22 (re-derived by the F-QC-1 amendment — the
  internal QC adjudicates the FUN_006C0F90/FUN_006C10B0 manager-method pairs as meeting the
  census's own four-part criterion on the same record depth as R09/R10; equals the internal
  QC's machine re-derivation of 22; the pre-amend value 20 was understated).
  ACTUAL_ANALYZED_EDGE_COUNT is deliberately NOT
  reported (the semantic-analysis boundary is definition-sensitive at the RAW_VISIBLE / REPIN
  classes — documented per row with explicit NOT_COUNTED_REASON, not adjudicated); the
  defensible minimum is reported instead:
  MINIMUM_ANALYZED_EDGE_COUNT = 22 (>= 7 as independently established by the Desktop).
- MAX_NEW_INTERPROCEDURAL_EDGES = 6 (source PRE_REGISTERED_ANCHORS.md) is NOT retroactively
  changed. 22 > 6 therefore requires:
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL (recorded in CORRECTED_STATUS_ALGEBRA.md).
- RETROACTIVE_PRIOR_AUTHORIZATION = NO. No present-human-exception adjudication is created by
  this correction; no fabricated prior authorization (see SUPERSESSION.md for the retraction
  of the "zero after-the-fact exceptions" interpretation).
- Retracted/superseded source-run interpretations: "6/6 edges, exhausted not exceeded";
  "zero after-the-fact exceptions"; any whole-run process-compliance interpretation depending
  on those statements (incl. the published PE_MASTER_REVIEW.md line 18/22 wording — superseded
  as ACTIVE interpretation by SUPERSESSION.md; the historical file itself remains immutable).
- The technical byte evidence and the preserved partial science do NOT become false merely
  because the execution contract was exceeded: every source-run record was re-hashed unchanged
  by this correction (QC J3/S-hash checks).
- STILL OPEN (honest): the census boundary at the lower classes is documented (per-row
  NOT_COUNTED_REASON) but not adjudicated as "analyzed"; a full CALLSITE-level count would
  add the same-pair duplicate callsites (R12, N03, V02/V03, V15) — the pair-level minimum
  of 22 is the strongest defensible lower bound on ANALYZED NEW EDGES; the FUN_007BF500
  window's raw-byte-only continuation calls remain a disclosed non-enumerated residue
  (enumerating them would require new body decoding — outside records-only scope).

## J3 / P2 — new transform semantics promoted outside the contractually permitted transform scope

DESKTOP FINDING (verbatim substance): the contract permitted SAME_INSTANCE_TRANSFORM_RELATION
to be recorded ONLY as an existing, re-pinned evidence note; a separate new transform trace was
excluded. The source run nevertheless derived new semantics from a full FUN_00509850 decode
(flags, x87/stack lineage, scale, nine dwords, the x100 multiplier); FUNCTION_BUDGET row #5
carries PRIOR_SCOPE_NOTE=none and CLAIM_MATRIX CL-08 is marked CONFIRMED (NEW #5) — the ledger
itself classifies it as NEW, not an inherited/re-pinned pin. The physical records may be
correct; the finding concerns the scope and provenance of the qualification, not fabricated
bytes.

DISPOSITION = CORRECTED (records-only; no new transform RE; no re-analysis).

- PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED: every raw byte window and measurement of
  FUN_00509850 in the source package is unchanged (re-hashed: 01_RAW/FUN_00509850_FULL.txt and
  the whole source package are byte-identical to their BASE blobs — QC J3 checks). The
  measurements remain true physical evidence: the SF pos x100 (translate -> NiNode+0x5C/+0x60/
  +0x64, [0x00A7A618]=100.0), rotation 9 dwords SF+0x4C -> NiNode+0x38, scale |SF+0x70| ->
  NiNode+0x68, flags SF+0x24..0x2C gates.
- CONTRACTUAL_PROMOTION_STATUS (separated from the measurements): the source run's
  SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC is SUPERSEDED as an ACTIVE run-qualified
  conclusion of the corrected lineage (SUPERSESSION.md; CORRECTED_STATUS_ALGEBRA.md).
- NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION (recorded).
- SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE (recorded).
- The promotion is NOT described as an inherited/re-pinned result, and NO claim is made that
  prior human authorization for the new transform-semantic promotion existed. Any future
  acceptance of this measured relation as a standing conclusion requires a NEW, explicit,
  present human decision — none exists in this correction.
- STILL OPEN (honest): the measured physical relation itself is neither confirmed nor
  falsified as science by this records correction; it is simply NOT a run-qualified conclusion
  of the corrected lineage.

## Cross-cutting honesty notes

- This correction does NOT close the underlying science: SCIENCE_OUTCOME remains
  PARENT_FOUND_CHILD_UNRESOLVED; A (CHILD_MODEL_PROVENANCE) and D (CHILD_VISUAL_ROLE) remain
  UNRESOLVED; INSTANCE_MODEL_NODE_JOIN remains NOT_ESTABLISHED; FUN_006C66D0 and FUN_007BF470
  remain undecoded and undecoded-by-this-run; no next experiment is authorized.
- The source package at BASE 064b7f4 (including its PE_MASTER_REVIEW.md and its manifest)
  remains IMMUTABLE; all supersession is recorded in THIS package's new records.
- Corrections are not "closed" merely by this execution: the independent PE-MASTER audit of
  THIS correction package is pending; publication decisions belong to the persistence phase.
