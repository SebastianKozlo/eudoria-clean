# SUPERSESSION — PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011

BASE: 28e91eb67511a3022a911ab6d4e02e68119b1f68 (SOURCE_REF research/pe935-placement-probe-census-postaudit-r1-20261011)
This run: BOUNDED_CORRECTION_ONLY per CONTRACT.md (29207 B / SHA256 6E4B0B029DBD082451A6F0E432AA66124FCC5E3299260AC3E330A59DED4F4E23).
Protected files and historical packages are READ_ONLY and byte-identical vs BASE; this file records the narrow, explicit supersessions.

## 1. PA2-RC1/P2 — the full-POST receipt acceptance condition is SUPERSEDED

Superseded (predecessor, BASE 28e91eb):

- Code: `docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/run_post.mjs`
  (48995 B, SHA256 3BBDC404E40B0ED2135BA74D5C978E5DB810AAD0A962C45D23FBE04D4B25C3BB, preserved READ_ONLY).
- Acceptance condition (PA2_LIVE_GATE case): the archived receipt qualified on
  `gate.verdict === 'PASS' && gate.matched === 16 && mode === 'REAL_SEQUENCE'` ONLY.
- External measurement (Desktop post-audit of 28e91eb, `RECEIPT_MUTATION_RESULTS.json`
  E0B61A041F5C5BA1D75DFFD5A058E1799D2F2000D66B92B21999D4CC2101A717): receipts with
  `perPin[0].MEASURED.sha256` zeroed (M1) and `moduleIdentity.gateModule.sha256` zeroed (M2)
  both passed the UNCHANGED full POST with QUALIFICATION_PASS/exit0 — a false-PASS of the
  load-bearing PA2 gate. Reproduced in this run's PRE (PRE/BASELINE_REPRODUCTIONS.json):
  CLEAN/M1/M2 all QUALIFICATION_PASS/exit0, suite 53/53 in each case.

Superseding (this run, canonical authority for receipt qualification):

- Code: `tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs`
  (shared validator) used by the CANONICAL_POST
  `tools/placement_probe/qualification/pa2_r1/run_post.mjs`
  (adapted from the predecessor POST; original required cases and source mapping preserved;
  diff summary recorded in FINAL_REPORT.md section 4 and AMENDMENT_LOG.md).
- The PA2_RECEIPT_QUALIFICATION case validates the receipt-under-test through the
  corrected predicates (contract §4.2): trusted BASE gate-module+runner SHA verification
  BEFORE loading the 16 frozen pins; exact-16 distinct pin names with strict types
  (no coercion; hex case normalization only); EXPECTED vs trusted pins;
  MEASURED.exists===true + size/SHA vs the same pins; independent recomputation of
  compareResult/match/total/matched/blockedCount/blockedPins/gate.verdict/
  EFFECTIVE_GATE_RESULT with consistency required; exact historical
  runId/stage/mode context; module identity paths (slash normalization only) and SHAs
  vs trusted source files; the unchanged verifyAllInputs as a LIVE remeasurement of the
  16 evidence paths required to PASS as well; fail-closed with preserved diagnostics;
  PA2 as a required conjunct (missing/FAIL/ERROR/NOT_PERFORMED => overall REFUSED).
- Four separate recorded quantities: INPUT_BYTES_REMEASURED, RECEIPT_INTERNAL_CONSISTENCY,
  MODULE_CODE_IDENTITY, RECEIPT_QUALIFICATION.
- Evidence: POST/RECEIPT_MUTATION_MATRIX.json — CLEAN PASS/QUALIFICATION_PASS/exit0;
  M1..M9 all PA2 FAIL/QUALIFICATION_REFUSED/exit4 with per-case semantic refusal reasons,
  recomputed values, other cases still passing, suite 64/64 in every case.
- The CLEAN whole-file hash is NOT a validator rule (self-QC probe QC-C: a re-serialized
  semantically identical receipt with a different whole-file SHA still qualifies); mutant
  rejection arises from the corrected semantics (self-QC probe QC-B: a self-authority
  attempt where EXPECTED==MEASURED but both differ from the trusted pins is refused).

NOT superseded (preserved confirmed):

- PA2_INPUT_COMPARISON = PRESERVED_CONFIRMED — the gate's frozen-pin comparison semantics
  (verify_inputs.mjs, unchanged) remain exactly as audited.
- PA2_RUNNER_EXIT3_ON_MISMATCH = PRESERVED_CONFIRMED — the predecessor runner's
  wrong-SHA/wrong-size/missing refusals with exit 3 remain exactly as audited
  (re-verified inside every canonical POST run through the staged-runner mutant
  counterchecks; see POST/RAW/{clean,m1..m9}/IDENTITY_GATE_COUNTERCHECKS.json).

## 2. PA2-RC2/P3 — the downstream spy claim is SUPERSEDED (records-only)

```ini
PA2_INPUT_COMPARISON = PRESERVED_CONFIRMED
PA2_RUNNER_EXIT3_ON_MISMATCH = PRESERVED_CONFIRMED
HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM = RETRACTED
PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT = NOT_ESTABLISHED
```

- Retracted: any reading of the predecessor runner's spy counters as PROOF that
  downstream work is automatically protected/enforced. The four counters
  (`analysis`, `correction`, `refReservation`, `postQualification`) are an AUTHENTIC
  observation: THIS runner's downstream callbacks are never invoked — on clean runs
  either (the counters are zero by construction: downstream work runs after the gate,
  not inside it). Zero counters do not prove that any other or future runner stops
  downstream work after a BLOCKED verdict, and the callback-replacement experiment of
  the external Desktop post-audit (RECEIPT_MUTATION section 5) showed the zeros are
  insensitive to whether downstream code would throw.
- The historical runner strings `GATE_PASS__DOWNSTREAM_AUTHORIZED` and
  `DOWNSTREAM_AUTHORIZED` remain in the frozen modules as LEGACY LABELS — they are not
  this run's authorization and not renewed proof of downstream integration.
- The exit-3 refusal itself is unaffected: PA2_RUNNER_EXIT3_ON_MISMATCH is preserved
  confirmed.
- No additional integration/orchestrator work is required or performed for this claim
  correction. Corrected active wording:
  - `tools/placement_probe/tests/pa2_identity_gate.test.mjs` — header comment and one
    assert MESSAGE corrected (assertions and test count unchanged; exact diff in
    AMENDMENT_LOG.md; updating wording does not erase the historical wording preserved
    in the BASE commit and this package's record).
  - New code and this package carry the corrected framing.
- The protected frozen file `tools/placement_probe/verify_inputs.mjs` still contains the
  historical line "the runner enforces this with a spy" — it CANNOT be edited (protected);
  this section supersedes that wording.

## 3. DA2-COV/P3 — aggregation coverage claim (no retraction; gap CLOSED by regression)

The predecessor B5 control used cap4, under which the second declared input is never
opened — cap4 does not prove two contributing sources. This run adds the permanent
regression `tools/placement_probe/tests/da2_two_source.test.mjs` reproducing the
externally measured cap32 case THROUGH THE ACTUAL SCAN of the UNCHANGED scanner:
SOURCE_1_CONTRIBUTION=29, SOURCE_2_CONTRIBUTION=3, TOTAL_CANDIDATE_ROWS=32, per-phase
distinct-live peaks 29/32/32 (<= 32), both inputs opened (sources.json parseStatus OK),
four ordinary/instrumented outputs byte-identical, budgets identical, WeakMap
scalar-identity observer storing no candidate objects (auditObjectsRetained=0), plus a
cap29 negative control in which the second input is never opened and the
two-contributing-sources predicate is provably violated. Evidence:
POST/TWO_SOURCE_AGGREGATION.json. cap4/cap256 and the forced-copy detection control
remain in the unchanged `tools/placement_probe/tests/da2_retained.test.mjs`.

## 4. Standing

- DA1, DA2, DA3, PA1: preserved CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES — no new
  counterexample; the predecessor closures are untouched and re-verified inside every
  full-POST case of this run.
- The historical literal-PASS generator supersession (gen_pre_identity.mjs) from the
  predecessor package remains in force.
- GENERAL_TOOL_CORRECTNESS = NOT_ESTABLISHED (unchanged).
