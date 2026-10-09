# QC_REPORT — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

## QC origin (honest)

- **QC_ORIGIN = EXECUTOR_SELF_REVIEW.** The internal QC available inside
  this run is the executor's own mechanical re-inspection of the completed
  correction evidence (SCRATCH/self_review.py, 43 checks, executed against
  the recorded PRE/POST/regression results and the package artifacts).
- **FRESH_CONTEXT_INTERNAL_QC = NOT_PERFORMED_IN_THIS_RUN.** Per the
  contract's own taxonomy and NO_NESTED_TASKS, a fresh-context internal
  review is performed by a SEPARATE LATER agent; it is recorded honestly as
  absent here, and **no internal QC_PASS is issued on the self-review
  basis**.
- **INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED** (BR_C1_DESKTOP_CLOSURE
  = PENDING_POST_AUDIT; closure requires the later independent audit of the
  resulting commit).
- Independence dimensions, honestly stated: the two corrected gates derive
  their expected facts independently (production: persisted objdump text +
  independent_esp_walk over the decoded stream; QC: its own objdump
  invocations + its own esp_walk/parse/opcode bytes; the QC imports nothing
  from the production verdict). The self-review itself is performed by the
  executor's session — it CANNOT substitute for a fresh-context or
  independent Desktop review. GNU objdump 2.44 is shared with the
  predecessor run (the same objdump is NOT two independent disassemblers).

## Self-review method (mechanical, 43 checks, all PASS)

SCRATCH/self_review.py re-parsed PRE_ARTIFACT_RESULTS.json,
POST_ARTIFACT_RESULTS.json, REGRESSION_RESULTS.json,
DRIVER_RUN_SUMMARY.json and FIELD_CHECK_COVERAGE.csv and verified:

1. **PRE defect reproduction and PRE/POST separation (SR-PRE-\*)**: the
   predecessor clean gate has exactly 21 checks in both gates; AC1/AC2 are
   rejected (predecessor predicates PROV-B-ARG1-KIND/PROV-B-LEA-EXPR /
   PROV-A-SLOT); BR1–BR4 PASS in both predecessor gates (8 false-PASS); PRE
   results carry the PREDECESSOR module hashes (0db331d8…/ec9f3fbe…),
   proving PRE was never rewritten to match POST.
2. **POST fixed matrix (SR-POST-\*)**: 14/14 correct outcomes; each of
   AC1/AC2/BR1–BR4 is REJECTED in BOTH corrected gates with the expected
   named BR-C1 predicate(s) among the failing checks, zero hash-side
   failures, zero exceptions; CLEAN passes both corrected gates with 50/50
   checks; the clean FINAL validation (same gates, no override) is PASS in
   both gates.
3. **Additional controls (SR-POST-ADDITIONAL, SR-POST-ADD-CAUSALITY)**:
   43 cases / 86 outcomes, 86/86 correct; every one rejected via the
   expected predicate with named diagnostics; the diagnostic taxonomy is
   observed in the production gate: MISSING_FIELD (MISS-1..4),
   WRONG_TYPE (TYPE-1..5, including boolean-rejected-as-integer TYPE-5 and
   int-rejected-as-boolean TYPE-3), MALFORMED_EXPR (MALF-1/2),
   VALUE_MISMATCH (BR1–BR4).
4. **FIELD_CHECK_COVERAGE (SR-COV-\*)**: 34 rows (32 field representations
   + 2 derived-relation/consistency rows); spans BR-C1.1 (4), BR-C1.2 (10,
   incl. the slot relation), BR-C1.3 (13, incl. parallel consistency),
   BR-C1.4 (7); all rows PASS in the clean gates; every row's single-field
   control shows REJECTION_OK in BOTH gates; every coverage check name
   exists in the clean gate check lists.
5. **Regression (SR-REG-\*)**: 24/24 CONTROL_PASS; M5/M7 arg1
   kind/expr/slot unchanged while the other channels changed (arg3/arg4
   swapped; receiver changed) on BOTH sides; unchanged-helper preservation
   proven mechanically (production EXPECTED/MUTATIONS/CASE_ORDER and QC
   EXP/MUT/CASE_ORDER identical to the predecessor); tool unchanged
   (GNU objdump 2.44, rc 0).
6. **Run-level safety (SR-RUN-\*)**: EXE SHA256 unchanged across all
   phases (E7785430…); predecessor source package 35/35 unchanged; clean
   provenance SHA matches the pinned ADBA8BF8…; corrected module hashes
   recorded.

**SELF_REVIEW_VERDICT = SELF_REVIEW_PASS (mechanical re-inspection only;
NOT internal QC_PASS).**

## Residuals and honest limits

- F-QC-1 (residual, carried): the driver's FIELD_CHECK_COVERAGE writer
  initially contained a variable-shadowing defect (the CSV was written to a
  stray relative-path file); it was caught during self-check, fixed, all
  stray files removed, and ALL driver phases re-executed from scratch with
  the final driver bytes (identical outcomes; PRE/POST/regression all
  re-measured). The published result files are those of the final
  re-execution.
- F-QC-2 (residual): the FIELD_CHECK_COVERAGE row F-C2-9
  (phase_a.source_slot.slot_delta_from_E) shows the DERIVED_EXPECTED_VALUE
  as "[E+0x4]" — the PROV-A-SLOT check's display column — while the
  persisted delta (4) appears in ACTUAL_PERSISTED_VALUE. The check itself
  enforces BOTH the expression and the delta equality; the CSV column is a
  display artifact only.
- F-QC-3 (residual, carried from the predecessor): the QC's EXEC_CLAIMS
  adjudication table and the prod_compare function remain the predecessor's
  fixed-transcription design (flagged by the Desktop post-audit as a
  limitation of the predecessor's fresh QC). This correction run's scope is
  the four BR-C1 persisted-fact relations in the artifact GATES; the QC
  gate now reads the live JSON under test (prov_override) — the fixed
  EXEC_CLAIMS table is not used by the corrected gate().
- This run did NOT attempt to qualify the correction beyond the four
  relations: no general JSON/decoder hardening, no new RE, no pointee or
  region research.
