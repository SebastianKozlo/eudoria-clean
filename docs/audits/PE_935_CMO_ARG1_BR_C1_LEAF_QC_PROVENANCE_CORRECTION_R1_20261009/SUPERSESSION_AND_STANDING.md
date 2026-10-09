# SUPERSESSION_AND_STANDING — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

## 1. What this correction SUPERSEDES (narrowly)

Exactly TWO claim classes of the predecessor package
PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009
(commit a7b1dc0317af6a33b185481cd9559160188cfb24), both identified by the
independent Desktop post-audit of that commit:

1. **SUPERSEDED (BR-C1-R1)**: the predecessor's implicit leaf-field
   handling-adequacy claim for the two `phase_a.source_slot` leaves —
   FIELD_CHECK_COVERAGE rows F-C2-8/F-C2-9 presented those leaves as
   covered persisted-fact representations while the underlying PROV-A-SLOT
   check still used direct dict indexing and an untyped `==` on
   `slot_delta_from_E` (Desktop counterexamples: `4.0` accepted —
   false-PASS on the declared integer type; deleting either leaf raised
   KeyError in both gates). This run REPRODUCED that residual through the
   ACTUAL predecessor gates (PRE_LEAF_RESULTS.json: PRE-FLOAT PASS 50/50 in
   both gates; PRE-DELETE-EXPR / PRE-DELETE-DELTA KeyError in both gates)
   and corrected the two leaf checks in both gates (typed leaf predicates
   PROV-A-SLOT-EXPR / PROV-A-SLOT-DELTA and QC-A-SLOT-EXPR /
   QC-A-SLOT-DELTA + the preserved aggregate conjunction; LF matrix
   16/16 correct rejections with the named leaf diagnostics).
   The predecessor's AUTHENTIC coverage value is preserved: its PROV-A-SLOT
   check did enforce both the expression and the delta on the clean input
   (value-level), and its F-C2-8/F-C2-9 rows correctly described the
   evidence derivation — what was inadequate was the type/missing-field
   handling, not the clean-value validation.
2. **SUPERSEDED (BR-C1-R2)**: the predecessor run's final-response claim
   that the later fresh-context internal QC performed a full independent
   re-execution of 14+86+24 outcomes. The direct fresh-QC record documents
   re-execution of 14 + 18 + 24 = 56 outcomes and machine-parsing of all 86
   additional outcomes; the corrected statement is in
   ERRATUM_QC_PROVENANCE.md. The fresh QC record itself, the historical
   final answers and all committed files are preserved unchanged.

Also superseded incidentally: the predecessor's clean-gate check COUNT
(50 per gate) as a fixed expectation — the corrected gates measure 52
checks per gate (the two typed leaf checks); the count was never a
scientific claim, and no check is hidden to force the old count.

## 2. What is NOT superseded (preserved verbatim)

- All predecessor SCIENCE (unchanged, no semantic promotion):

```text
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
CONDITIONS = AS1-AS5 plus EAX!=0, unchanged
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
```

- The predecessor's authentic PRE (8 false-PASS outcomes for BR1-BR4
  through the OLDER 21-check gates) and its POST (fixed 14/14, additional
  86/86, regression 24/24 through the a7b1dc0 corrected gates) — all
  re-verified this run through the new corrected copies with UNCHANGED
  case definitions (fixed 14/14, additional 86/86, regression 24/24).
- The predecessor's required controls: the 12-case production + 12-case QC
  byte matrices (re-executed 24/24 CONTROL_PASS, M5/M7 arg1-retention
  verified on both sides), AC1/AC2 (still rejected by both gates), the
  clean baseline (still PASS, now 52/52 checks per gate).
- The predecessor's failed negative-test history, in-run repair disclosure
  (its F-QC-1 driver CSV-writer defect) and its residuals F-QC-2/F-QC-3.
  F-QC-2 (the F-C2-9 DERIVED_EXPECTED_VALUE display artifact) is RESOLVED
  in THIS package's coverage CSV by construction (the delta row now
  references the typed delta-leaf check, whose derived value column shows
  the measured delta 4); the historical file is not edited. F-QC-3
  (predecessor EXEC_CLAIMS adjudication design, unused by the corrected
  gates) remains a carried residual.
- The actual late-QC history of the predecessor run (fresh QC after
  commit; ORIGINAL_FRESH_QC_BEFORE_PUBLICATION = NOT_MET;
  RETROACTIVE_ORDER_COMPLIANCE = NO; publication integrity passed
  independently of that process deviation). No retroactive repair, no
  invented human exception.
- J3 supersession records — kept (no restoration); no ACLD/CMO identity
  transfer; no reinterpretation of the [arg1+8] -> MovableObject+0x44
  store; no CMO+0x44 -> X promotion.

## 3. What this run ADDS (machinery + records only)

- Corrected copies of both ordinary gates (03_SCRIPTS/run_frame_bridge.py
  gate_artifacts(), 03_SCRIPTS/qc_frame_bridge.py gate() + the QC-local
  qc_eslot_expr / qc_check_eslot_expr helpers): the two source_slot leaves
  are checked individually with safe typed helpers, named diagnostics
  (MISSING_FIELD / WRONG_TYPE / MALFORMED_EXPR / VALUE_MISMATCH), no
  uncaught exception on a missing tested leaf, no acceptance of a wrong
  native JSON type; the aggregate PROV-A-SLOT is the conjunction of both
  typed leaf comparisons; both leaves are evaluated even if one fails.
  Proven minimal: AST comparison (only gate_artifacts()/gate() changed +
  the two new QC helpers; all top-level constants identical) +
  CODE_DIFF.patch (mechanical apply test reproduces both corrected files
  exactly) + regression preservation checks (EXPECTED/MUTATIONS/
  CASE_ORDER/EXP/MUT identical to the predecessor).
- The new LF matrix: 8 cases x 2 gates = 16/16 correct outcomes (LF-CLEAN
  PASS; LF-FLOAT/LF-BOOL WRONG_TYPE delta; LF-MISSING-DELTA/LF-MISSING-EXPR
  MISSING_FIELD; LF-NULL-EXPR WRONG_TYPE expr; LF-WRONG-DELTA/LF-WRONG-EXPR
  VALUE_MISMATCH) — every rejection carries the named typed-leaf
  predicate, the correct diagnostic on the exact leaf path, zero
  hash-side failures, zero unrelated failures, zero exceptions.
- FIELD_CHECK_COVERAGE.csv (34 rows; the two leaf rows now reference the
  named typed-leaf predicates) + the re-executed matrices (fixed 14/14,
  additional 43 cases/86 outcomes, byte regression 24/24) through the SAME
  final corrected ordinary gates (clean PASS 52/52 per gate, measured).
- ERRATUM_QC_PROVENANCE.md (the BR-C1-R2 records correction) and
  MODEL_218757_CONTINUITY.md (records-only building-case continuity map;
  no new asset/function/instance opened).

## 4. Scope fences of this correction

- EXE reads: whole-file hashing + PE headers for the existing mapping +
  ONLY the two EXISTING windows A/B replay/verification (unchanged from
  the predecessor; 0x004C47C8 unopened; no new bodies, xrefs, pointees;
  STATIC_ONLY — the client never ran; no physical NIF/GLB/ARK/VFS/BNT/SDK
  reads).
- No T+0x10 producer investigation, no placement/XYZ work, no upstream
  producer trace, no new caller/receiver/getter/transform RE, no model or
  instance research (the continuity file is records-only), no
  Gamebryo/OpenMW research, no runtime/client/network experiments, no
  milestone/qualification/governance change, no next experiment.
- No general schema engine, no eval, no universal JSON/decoder hardening —
  the finite FIELD_CHECK_COVERAGE of the four BR-C1 relations plus the two
  typed leaf checks only.
- This executor did NOT commit, push or edit AUDIT_ENTRYPOINT.md; the
  package is returned to the orchestrator before publication. The
  fresh-context QC (QC_RESULTS.json / QC_REPORT.md), PE_MASTER_REVIEW.md
  and MANIFEST_SHA256.csv are NOT created at executor stage (PENDING /
  orchestrator-supplied; never fabricated).

## 5. Standing after this correction (executor stage; final acceptance is
      the orchestrator's)

```text
BR_C1_R1_LEAF_FIELD_HANDLING   = CORRECTED_IN_TESTED_SCOPE (LF 16/16;
                                 internal acceptance of the tested scope
                                 only — NOT Desktop closure)
BR_C1_R2_QC_COVERAGE_PROVENANCE= ERRATUM_RECORDS_ONLY (the corrected
                                 evidence bound is recorded; the frozen
                                 historical records are unchanged)
BR_C1_DESKTOP_CLOSURE          = PENDING_POST_AUDIT (a later independent
                                 Desktop post-audit of the resulting
                                 published commit remains the closure gate)
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL (unchanged)
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL (unchanged)
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM (unchanged)
FIELD_SEMANTICS = UNVERIFIED (unchanged)
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED (unchanged)
HISTORICAL_PLACEMENT = NOT_ESTABLISHED (unchanged)
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED (unchanged; records-only)
WORLD_XYZ_RECOVERED = NO
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## 6. Incidental contradiction check

No contradiction with preserved science emerged incidentally during this
correction: every clean persisted value re-validated by the corrected
gates matched the evidence-derived expectation (52/52 checks per gate),
all 86 additional controls and all 24 byte-matrix outcomes were unchanged,
and the LF rejections are machinery behavior, not new facts about the
client. Had a contradiction appeared, it would have been recorded with
REQUIRE_CORRECTIONS without silent reinterpretation.

## 7. Phase boundaries of this record

This correction run wrote only under OUTPUT_ROOT (PACKAGE/ publishable +
SCRATCH/ local-only) and, at package-preparation completion, the mirrored
OUTPUT_REPO_PATH. The predecessor packages (20 + 35 files), the EXE and all
historical files are byte-unchanged (re-verified before and after all
work). Canonical publication (one AUDIT_ENTRYPOINT.md row, manifest last,
allowlisted commit + fast-forward push) is the orchestrator's terminal step
after the separate fresh-context QC; it is NOT performed by this executor.
