# CORRECTED_STATUS_ALGEBRA — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

The ACTIVE status algebra of the corrected lineage after the independent Desktop post-audit
(PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007, verdict REQUIRE_CORRECTIONS,
findings J1/J2/J3) and this records/QC-machinery correction. Section A lists the ACTIVE
statuses; section B lists the SUPERSEDED source-run interpretations (with their historical
values preserved for the record); section C lists what the correction deliberately did NOT
change. Historical source-run files are immutable — supersession lives HERE and in
SUPERSESSION.md only.

## A. ACTIVE statuses (corrected lineage)

# --- preserved science (contract §3; MUST NOT change) ---
SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED
PARENT_CALLSITE_BYTES = CONFIRMED_IN_EXAMINED_ACLD_SCOPE
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE
JOIN_OPERATION = STRONGLY_SUPPORTED
CHILD_MODEL_PROVENANCE = UNRESOLVED                                   # proof A
CHILD_VISUAL_ROLE = UNRESOLVED                                        # proof D
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED                            # status algebra does not average up
RUNTIME_JOIN_OBSERVED = NO
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO

Identity boundary (preserved verbatim from the source run): the join parent is the SF of the
examined ArkClientLocalDynamic+0x18 holder — the same SF class (vtable 0x00A7D458) and the
same creation chain as the SF island, but a DIFFERENT instance from the CMO+0xC0 holder. The
SF+0x30 parent identity and the CMO-path transform are NOT transferable between holders; no
identity/CMO-transform transfer into the ACLD chain is made by this correction.

# --- J1 corrected statuses ---
QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY
REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED (policy of the corrected gate; no exception in
  this correction grants general positive semantic authority)
QUALIFICATION_GATE_ACTIVE = QUALIFICATION_GATE_CORRECTED.py (this package); the historical
  source gate at BASE is READ-ONLY and carries no positive-semantic-qualifier authority
SCIENCE_PASS = NOT_ISSUED_BY_ANY_TOOL_OF_THIS_CORRECTION (no code path yields it)

# --- J2 corrected statuses ---
MINIMUM_ANALYZED_EDGE_COUNT = 22   # distinct new (caller,callee) pairs semantically analyzed
                                   # by the source run per its own records (census:
                                   # EDGE_BUDGET_RECONSTRUCTION.csv; re-derived 20 -> 22 by
                                   # the internal-QC F-QC-1 records amendment: 6 ledger +
                                   # 16 summary-semantic-new distinct pairs; includes the
                                   # mandated 0x0050A3AF -> FUN_006C66D0 edge (row R01))
ACTUAL_ANALYZED_EDGE_COUNT = NOT_REPORTED (the semantic-analysis boundary is
  definition-sensitive at the lower census classes; an exact total would require adjudicating
  rows this correction only documents — see EDGE_BUDGET_RECONSTRUCTION.csv header)
MAX_NEW_INTERPROCEDURAL_EDGES = 6  # source PRE_REGISTERED_ANCHORS.md; NOT retroactively changed
ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL   # 22 > 6 (pre-amend 20 already exceeded 6; conclusion
                                         # unchanged by the F-QC-1 amendment); recorded honestly
RETROACTIVE_PRIOR_AUTHORIZATION = NO     # no fabricated prior authorization; no present
                                         # human-exception adjudication created by this correction
SOURCE_LEDGER_ROWS = 6 (E1–E6; the ledger measured list length, not performed scope)
PROCESS_COMPLIANCE_INTERPRETATION_OF_SOURCE_RUN = SUPERSEDED (see section B)

# --- J3 corrected statuses ---
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED   # all FUN_00509850 raw windows/measurements
                                             # unchanged; re-hashed == BASE blobs by QC
CONTRACTUAL_PROMOTION_STATUS = SUPERSEDED_AS_ACTIVE_RUN_QUALIFIED_CONCLUSION
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
   # NOT described as inherited/re-pinned; NO prior human authorization claimed for the
   # promotion; future acceptance requires a NEW explicit present human decision (none exists)

# --- run/correction bookkeeping ---
RUN_CLASS = RECORDS_AND_QC_MACHINERY_CORRECTION
BASE_SHA = 064b7f4aa4f3961f1a44212b2423e298eb51c291
RESULTING_SHA = NONE (this executor phase; persistence = PE-MASTER after its own audit)
SUPERSESSION_STATUS = ACTIVE (five interpretations superseded; six items preserved — §7)
NEW_SCIENCE_EXECUTED_BY_THIS_CORRECTION = NO
NEW_RE_EXECUTED_BY_THIS_CORRECTION = NO   # only re-verification of already-published pins
INDEPENDENT_DESKTOP_POST_AUDIT_OF_THIS_CORRECTION = NOT_PERFORMED (pending)
PE_MASTER_REVIEW_OF_THIS_CORRECTION = NOT_PERFORMED (pending; placeholder record in
  PE_MASTER_REVIEW.md to be filled by the persistence phase after the PE-MASTER audit)

## B. SUPERSEDED source-run interpretations (historical values kept for the record)

Each entry: the source-run ACTIVE interpretation -> its superseding status. The underlying
BYTE EVIDENCE and partial science are NOT falsified (§3 preserved).

1. Whole-package advisory MASTER_ACCEPTED (source PE_MASTER_REVIEW.md "RUN_VERDICT =
   MASTER_ACCEPTED (advisory)") -> SUPERSEDED as a whole-package interpretation of 064b7f4 by
   the independent Desktop REQUIRE_CORRECTIONS verdict; superseded as ACTIVE acceptance; the
   historical advisory text remains immutable.
2. "Qualification gate: reads proof-chain structure ... a trustworthy positive semantic
   qualifier" (source PE_MASTER_REVIEW.md line 22; HANDOFF CTRL block; commit message) ->
   SUPERSEDED: the production gate is NOT a trustworthy positive semantic qualifier; the
   corrected gate (this package) has REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED and issues no
   SCIENCE_PASS (Desktop J1 + counterexamples M1–M5).
3. "Budget census: ... 6/6 edges ... exhausted NOT exceeded" (source commit message 064b7f4;
   PE_MASTER_REVIEW.md line 18/22; FINAL_REPORT §2 header; HANDOFF "BUDGET USED") ->
   SUPERSEDED: MINIMUM_ANALYZED_EDGE_COUNT = 22 > MAX 6 (re-derived by the internal-QC
   F-QC-1 amendment; the pre-amend census minimum 20 already exceeded MAX 6); the ledger
   measured list length, not performed scope (Desktop J2 + EDGE_BUDGET_RECONSTRUCTION.csv).
4. "ZERO after-the-fact exceptions" (same source records) -> SUPERSEDED: at least 16 distinct
   uncharged analyzed interprocedural pairs exist beyond the 6 charged edges (22 - 6;
   re-derived by the F-QC-1 amendment from the pre-amend 14); no after-the-fact
   exception adjudication is claimed; RETROACTIVE_PRIOR_AUTHORIZATION = NO.
5. Transform "SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC" as an authorized result of the
   source run -> SUPERSEDED (historical quotes: source PE_MASTER_REVIEW.md line 14 —
   "SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC (SEPARATE status; ...)", source
   FINAL_REPORT.md §1.5/§3, source CLAIM_MATRIX.csv CL-08 — "CONFIRMED (NEW #5) — recorded as
   SAME_INSTANCE_TRANSFORM_RELATION=CONFIRMED_STATIC (path-conditional)", source HANDOFF.md
   line 34, source FUNCTION_BUDGET.csv row #5 with PRIOR_SCOPE_NOTE=none) -> SUPERSEDED as an
   ACTIVE run-qualified conclusion: NEW_TRANSFORM_TRACE =
   MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN
   = NOT_QUALIFIED_BY_ORIGINAL_SCOPE (Desktop J3). The raw measurements stay PRESERVED.

## C. What this correction deliberately did NOT change (contract §3/§10)

- The 24 raw windows / 25 pins / 17 rel32 targets of the source run were NOT re-executed as new
  science; existing persisted physical evidence was only re-hashed / parsed / replayed as
  correction QC (allowed by §3).
- PARENT_FOUND_CHILD_UNRESOLVED, EXACT_PARENT, JOIN_OPERATION, CHILD_MODEL_PROVENANCE,
  CHILD_VISUAL_ROLE, INSTANCE_MODEL_NODE_JOIN, WORLD_XYZ_RECOVERED, STATIC_BUILDING_CHANNEL,
  HISTORICAL_INSTANCE_DATA_RECOVERED — all unchanged (machine-verified by the correction QC §10
  check against the BASE CLAIM_MATRIX.csv).
- No new model/resource/visual conclusion appears anywhere in this package (machine-checked:
  no overclaim token; every historical CONFIRMED_STATIC mention inside this package occurs
  ONLY inside supersession/historical context).
- FUN_006C66D0, FUN_007BF470, FUN_007B5A00 and every other source-run NOT_CHECKED callee
  remain undecoded; no new EXE region was opened; no runtime; no payload reads.
- The historical source package, its ledgers, its PE_MASTER_REVIEW.md and its manifest remain
  immutable (re-hashed unchanged before and after this work).
