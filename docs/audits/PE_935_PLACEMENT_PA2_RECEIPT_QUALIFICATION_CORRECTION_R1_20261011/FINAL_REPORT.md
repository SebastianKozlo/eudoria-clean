# FINAL_REPORT — PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011

RUN_CLASS: SUPPORTING. RUN_TYPE: BOUNDED_CORRECTION_ONLY.
Contract: OPENCODE_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_COMPLETE.md — 29207 B /
SHA256 6E4B0B029DBD082451A6F0E432AA66124FCC5E3299260AC3E330A59DED4F4E23 (byte-identical
as CONTRACT.md).
BASE = EXPECTED_BASE_SHA = 28e91eb67511a3022a911ab6d4e02e68119b1f68
(SOURCE_REF research/pe935-placement-probe-census-postaudit-r1-20261011, local +
remote-tracking + live remote all equal; RESULT_REF
research/pe935-placement-pa2-qualification-correction-r1-20261011 reserved create-only
locally at BASE, absent on remote; observed master 3fbe93eec04759395223e6677b5040273d29222a
separate, untouched, no write performed to it).

## 1. Mission and outcome

Close PA2-RC1/P2 by making the actual canonical POST refuse inconsistent identity
receipts; correct the PA2-RC2/P3 downstream claim through records only; add the
DA2-COV/P3 two-contributing-source regression. Preserve DA1, DA2, DA3 and PA1 in their
externally audited scope. No scanner redesign, no general provenance framework.

**Outcome: the PA2-RC1 defect is CLOSED in the audited cases.** The externally measured
false-PASS (CLEAN/M1/M2 all QUALIFICATION_PASS/exit0 on the unchanged BASE POST,
reproduced in PRE) is eliminated: with the corrected canonical POST, CLEAN still passes
(QUALIFICATION_PASS/exit0) while every M1..M9 receipt is refused by the corrected PA2
semantics (QUALIFICATION_REFUSED/exit4, all other 14 required cases still passing,
64-test suite green in every case). PA2-RC2 supersession published (records only);
DA2-COV cap32 29+3 regression reproduced through the actual scan and committed as a
permanent regression.

**Honest qualification status:**

- All technical §9 gates PASS (preflight/source integrity; preserved historical
  regression — BASE 53/53 and kit 7/7; CLEAN PASS; M1..M9 PA2-caused full-POST
  refusal; four profile unit controls; three actual aggregator controls; cap32
  two-source regression; source freeze; no material unresolved P0/P1/P2 in this
  correction scope).
- The "required internal QC" element is satisfied by an EXECUTOR-SELF-QC (7/7 probes,
  QC/INTERNAL_REVIEW.md) while the FRESH-CONTEXT internal QC is
  NOT_PERFORMED_IN_EXECUTOR_SESSION (no fresh context available to the executor; per
  contract §8 recorded as such). Per §8, the executor therefore does NOT claim the full
  final QUALIFICATION_PASS conjunction as closed: **TECHNICAL_GATES_PASS;
  FULL_QUALIFICATION_PASS_WITHHELD_PENDING_FRESH_CONTEXT_INTERNAL_QC** (assigned to the
  separate later pe-master-auditor pass per the governing dispatch).
- Publication of this package content is a separate later phase (pe-master-auditor);
  this run performed no commit/push/ref write. EXTERNAL_DESKTOP_POST_AUDIT = PENDING.

## 2. PRE — the defect, reproduced and frozen (§3)

The UNCHANGED BASE full POST (predecessor harness, private byte-identical copies, SHA
3BBDC404E40B0ED2135BA74D5C978E5DB810AAD0A962C45D23FBE04D4B25C3BB; source scripts never
executed in place; original normal JSON loader; full battery) in three isolated private
copies:

| Case | Only change | PA2_LIVE_GATE | Final | Exit | Suite |
| --- | --- | --- | --- | --- | --- |
| CLEAN | none | PASS | QUALIFICATION_PASS | 0 | 53/53 |
| M1 | perPin[0].MEASURED.sha256 := 64 zeroes | PASS | QUALIFICATION_PASS | 0 | 53/53 |
| M2 | moduleIdentity.gateModule.sha256 := 64 zeroes | PASS | QUALIFICATION_PASS | 0 | 53/53 |

Matches the external Desktop RECEIPT_MUTATION_RESULTS.json exactly (the historical
observation). PRE/RAW/** preserves commands, harness/receipt hashes, stdout/stderr and
raw JSON. PRE was never rewritten after execution.

## 3. The corrected PA2 acceptance condition (PA2-RC1, §4)

New canonical code (allowlist root tools/placement_probe/qualification/pa2_r1/):
`validate_receipt.mjs` (shared validator + the ACTUAL aggregator `computeQualification`
+ frozen `EXPECTED_OUTCOMES`), `run_post.mjs` (CANONICAL_POST), `two_source.mjs`
(DA2-COV observer), `run_matrix.mjs` (outer bounded driver, outside the canonical POST
recursion).

CLI (executed exactly as specified):
`node tools/placement_probe/qualification/pa2_r1/run_post.mjs --worktree <isolated-checkout> --runroot <private-case-root> --kitdir <verified-extracted-kit> --receipt <receipt-under-test.json> --out <private-output-dir>`

All eight §4.2 predicates implemented: (1) trusted BASE gate-module+runner SHA verified
against the contract constants BEFORE the 16 pins load from the verified module; (2)
exactly 16 distinct pins, strict types, no coercion, hex-case-only normalization;
(3) EXPECTED vs trusted pins, MEASURED.exists===true, measured size/SHA vs the same
pins, independent compareResult/match re-derivation (claimed compareResult validated,
never trusted; no legacy inputMatch required — QC-A proves absent fields tolerated);
(4) total/matched/blockedCount/blockedPins/verdict/EFFECTIVE_GATE_RESULT recomputed and
consistency required (PASS = all 16 matching, zero blocked, empty blockedPins); (5)
exact historical runId PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011, stage
PA2_LIVE_IDENTITY_GATE, mode REAL_SEQUENCE, contextBase 28e91eb; module identity paths
with slash normalization only and SHAs vs trusted sources; (6) unchanged verifyAllInputs
as live remeasurement of the 16 evidence paths, required to PASS, never writing the
receipt (M1/M2 stay failures even though the current files are clean); (7) fail-closed
with preserved diagnostics (every computable quantity computed, ALL refusal reasons
collected, any exception = controlled failure); (8) PA2 is a required conjunct —
missing/FAIL/ERROR/NOT_PERFORMED => QUALIFICATION_REFUSED.

Four separate quantities recorded per case: INPUT_BYTES_REMEASURED,
RECEIPT_INTERNAL_CONSISTENCY, MODULE_CODE_IDENTITY, RECEIPT_QUALIFICATION.
Limitations: context-specific requalification of archived evidence; hash consistency is
not historical-execution proof, a signature, or proof of authorship; no signing service
or universal receipt framework.

## 4. Predecessor diff (supersession record)

`run_post.mjs` is adapted from the predecessor POST (BASE SHA 3BBDC404…): its required
cases and source mapping are preserved verbatim (ORIGINAL_SEVEN, FULL_SUITE, DA1_CENSUS,
DA1_NOT_OPENED, DA2_CAP4, DA2_CAP256, DA2_MUTANT_COPY, DA2_SMALL_FIXTURE, DA3_REFUSALS,
DA3_POSITIVES, PA1_REGRESSION, AGGREGATOR_CONTROL; same fixtures, same stage-copy
discipline, same predicates per case). Changes:
1. CLI gains `--receipt` and `--out`; ALL outputs go to `--out` (never alongside
   historical scripts); the executed command is recorded.
2. PA2_LIVE_GATE's three-field acceptance (the defect) is superseded by
   PA2_RECEIPT_QUALIFICATION (§3 above); the three staged-runner mutant counterchecks
   (same-size/missing/wrong-size => exit 3, zero downstream) are preserved inside the
   case; receipt-untouched verified by hash before/after.
3. New required cases: BASE_53_REPLAY (exact BASE 53-test replay, separate from the new
   suite) and DA2_TWO_SOURCE (cap32 29+3 through the actual scan).
4. FULL_SUITE runs the 12-file current suite with required prefixes + PA2-RQ:/DA2-COV:.
5. The aggregator is imported from the shared module; expectations frozen in
   EXPECTED_OUTCOMES; every case records WHY_NON_CIRCULAR.
No scanner, gate-module, adapter or historical-package change (git diff vs BASE: only
pa2_identity_gate.test.mjs — comment/assert-message only — among tracked files, plus
new files in the allowlist roots and this package).

## 5. Full-POST matrix (§5; final batch 3; frozen code identity, freezeOk=true)

| Case | Change | PA2 | Overall | Exit | Refusal reason (semantic) |
| --- | --- | --- | --- | --- | --- |
| CLEAN | unmodified archived receipt | PASS | QUALIFICATION_PASS | 0 | — (matched 16/16; module identity ok; live remeasurement PASS) |
| M1 | perPin[0].MEASURED.sha256 zeroed | FAIL | QUALIFICATION_REFUSED | 4 | MEASURED.sha256 differs from the trusted pin (claimed MATCH) |
| M2 | gateModule.sha256 zeroed | FAIL | QUALIFICATION_REFUSED | 4 | moduleIdentity.gateModule.sha256 does not match the trusted gate module file |
| M3 | MEASURED.sizeBytes +1 | FAIL | QUALIFICATION_REFUSED | 4 | MEASURED.sizeBytes 11362 != trusted pin 11361 |
| M4 | compareResult=SHA_MISMATCH (bytes match) | FAIL | QUALIFICATION_REFUSED | 4 | claimed compareResult SHA_MISMATCH contradicts the independently derived MATCH |
| M5 | one perPin removed | FAIL | QUALIFICATION_REFUSED | 4 | perPin count is 15 != expected 16 |
| M6 | one perPin duplicated | FAIL | QUALIFICATION_REFUSED | 4 | perPin count is 17 != expected 16 |
| M7 | gate.matched=15, blockedCount=1 (pins match) | FAIL | QUALIFICATION_REFUSED | 4 | gate.matched 15 != recomputed 16 |
| M8 | runner.sha256 zeroed | FAIL | QUALIFICATION_REFUSED | 4 | moduleIdentity.runner.sha256 does not match the trusted predecessor runner file |
| M9 | one pin exists=false/nulls/MISSING + summary reports it but verdict PASS | FAIL | QUALIFICATION_REFUSED | 4 | MEASURED.exists is not true …; gate.verdict PASS != recomputed BLOCKED_INPUT_IDENTITY |

Every case: other 14 required cases still passing, suite 64/64, receipt untouched,
recomputed-vs-claimed values recorded. M1/M2 independently demonstrate closure of the
two Desktop findings. Unit profile controls (separately counted): wrong runId / wrong
stage / wrong mode / unreadable-truncated JSON — all controlled refusals;
CLEAN-unchanged control still PASS. Aggregator controls (separate from receipt cases
and test counts): the ACTUAL computeQualification over the REAL measured CLEAN outcomes
with PA2 missing / FAIL / NOT_PERFORMED — each QUALIFICATION_REFUSED/exit4 with the
affected gate PA2_RECEIPT_QUALIFICATION.

## 6. PA2-RC2 records-only correction (§6)

See SUPERSESSION.md:
PA2_INPUT_COMPARISON=PRESERVED_CONFIRMED; PA2_RUNNER_EXIT3_ON_MISMATCH=PRESERVED_CONFIRMED;
HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM=RETRACTED;
PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT=NOT_ESTABLISHED. Zero counters remain an authentic
observation (never reached on clean runs either) but prove no downstream integration.
Historical DOWNSTREAM_AUTHORIZED strings are legacy labels. Active test wording corrected
(pa2_identity_gate.test.mjs comment + one assert message; assertions unchanged; recorded
diff in AMENDMENT_LOG.md). No scanner change, no integration work, no real ref/GitHub
writes in any test.

## 7. DA2-COV two contributing sources (§7)

Through the ACTUAL scan of the UNCHANGED scanner (ordinary tool SHA 0D69AAFE… = BASE
placement_probe.mjs), two records80() synthetic inputs at cap 32:
SOURCE_1_CONTRIBUTION=29, SOURCE_2_CONTRIBUTION=3, TOTAL_CANDIDATE_ROWS=32,
peaks creation/forward/serialization = 29/32/32 (<= 32), both inputs opened
(sources.json parseStatus OK), per-source provenance from the scan outputs plus
forward-phase observer provenance (29 and 3), serialization walks the live rows
(allSerializedAreLiveRows=true, auditObjectsRetained=0 — WeakMap scalar-identity
observer, marker-injection pattern attributed to da2_retained.test.mjs BASE), four
ordinary/instrumented outputs byte-identical, budgets identical. Permanent regression:
tools/placement_probe/tests/da2_two_source.test.mjs (cap32 case + cap29 negative
control where the second input is never opened and the predicate provably fails).
cap4/cap256 and the forced-copy detection control preserved unchanged in
da2_retained.test.mjs. Evidence: POST/TWO_SOURCE_AGGREGATION.json.

## 8. Budgets, replay and counts (§8)

Ceilings unchanged and never raised (syntheticInputs 32, scannedBytes 67108864,
layoutEvaluations 100000, fullCensusRows 50000, retainedCandidates 256); lowered
fixture limits recorded in BUDGET_ACCOUNTING.json; every full-POST case separately
counted. Replays: exact BASE 53 tests 53/53 exit0 (from the isolated stage, in every
POST run); original seven kit tests 7/7 (byte-pinned ZIP members verified); current suite 64/64 (53 BASE + 11 new: pa2_receipt_qualification.test.mjs 9 tests,
da2_two_source.test.mjs 2 tests).
Correction rounds against the tool after its first green suite: 0/2 (harness bring-up
iterations disclosed in AMENDMENT_LOG.md; both classifications recorded).

## 9. Internal QC (§8)

EXECUTOR-SELF-QC 7/7 probes PASS (QC/INTERNAL_REVIEW.md, QC/FINDINGS.json);
FRESH_CONTEXT_INTERNAL_QC = NOT_PERFORMED_IN_EXECUTOR_SESSION (assigned to the separate
later pe-master-auditor pass; therefore full final QUALIFICATION_PASS is not claimed).
Open findings: SELF-QC-F2 (fresh-context QC pending — see status), SELF-QC-F3 (frozen
verify_inputs.mjs legacy wording, superseded by records), SELF-QC-F4 (pre-existing BASE
accounting P3, preserved) — all P3, nonblocking; no P0/P1/P2 in this correction scope.

## 10. Standing and science ceiling (§11)

PLACEMENT_DISCOVERY=NOT_EXECUTED; MODEL_218757_TO_CMO_JOIN=NOT_ESTABLISHED;
MODEL_218757_TO_WORLD_INSTANCE=NOT_ESTABLISHED; WORLD_INSTANCE_IDENTITY=NOT_ESTABLISHED;
HISTORICAL_PLACEMENT=NOT_ESTABLISHED; WORLD_XYZ_RECOVERED=NO;
GENERAL_TOOL_CORRECTNESS=NOT_ESTABLISHED; PCG_PHYSICAL_PAYLOAD_SCAN=NO; EXE_RE=NO;
GAMEBRYO_RE=NO; CANONICAL_GATE_EFFECT=NONE; PILOT_SCAN_AUTHORIZED=NO;
NEXT_EXPERIMENT_AUTHORIZED=NO; NEXT_MILESTONE_AUTHORIZED=NO;
EXTERNAL_DESKTOP_POST_AUDIT=PENDING; HARD_STOP=YES.
DA1/DA2/DA3/PA1 preserved CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES.
