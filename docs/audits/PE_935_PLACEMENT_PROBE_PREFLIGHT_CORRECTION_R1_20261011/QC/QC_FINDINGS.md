# QC_FINDINGS — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011

Fresh internal QC by a separately-dispatched pe-master-auditor context (read-only; no project
file modified). Every finding below was reproduced or measured by QC-owned scripts in this
directory; none is speculative. Severities: P0 (blocks run/persistence), P1 (material unmet
contract requirement in the corrected deliverable), P2 (real defect requiring a narrow
correction), P3 (hygiene/documentation/provenance).

---

## F1 (P1) — RETAINED_CANDIDATES does not bound the peak across all structures; global overshoot demonstrated (261 > 256)

- **File/lines:** `tools/placement_probe/placement_probe.mjs` — main loop lines 439-443
  (`budget.trackPeak(rows.length); if (rows.length >= budget.limits.retainedCandidates) { markExhausted(...); break; }`)
  — the only global `allRows` enforcement, executed **after each file**; per-blob enforcement
  only at line 292 (`budget.tryRetain(found.length)`, `found` is per-analyzeBlob); within-file
  per-payload guard only at line 397 and only **after** exhaustion is already marked.
- **Contradicted claim:** contract §8 — "RETAINED_CANDIDATES ogranicza peak jednocześnie
  przechowywanych rekordów kandydatów we wszystkich strukturach, również found/allRows/kolejkach
  i niezależnych kopiach. Nie ograniczaj tylko końcowego top." Also §8 test requirement
  "dla wspólnych limitów także agregacja przez co najmniej dwa wejścia" for this limit.
- **Evidence (measured):** QC probe `qc_retained_gap_probe.mjs`: 9 raw `records80` inputs, default
  ceilings (`retainedCandidates: 256`, `top: 100`), single invocation →
  `candidateCount: 261`, `peakRetainedCandidates: 261`, `exhausted: ["RETAINED_CANDIDATES"]`
  only **after** the 9th file, refusal detail `"global rows retention at 261"`, status
  `BUDGET_EXHAUSTED_COVERAGE_PARTIAL`. The global allRows list simultaneously held 261 candidate
  records — 5 above the canonical ceiling — before enforcement fired. Mid-file combinations
  (rows of earlier files + current blob's `found`) can reach roughly ceiling+top.
- **Failure mechanism:** `tryRetain` charges per-blob `found` only; `rows` (allRows) is checked
  only at file boundaries, so retention across payloads/files accumulates unchecked between
  checks. `budget.test.mjs` B5 (lines 107-121) exercises a **single input**, so neither the
  cross-input aggregation nor the global peak property is tested.
- **Affected:** §8 RETAINED_CANDIDATES semantics; POST/BUDGET_ACCOUNTING B5 claim ("peak across
  all structures capped") as a general property; SUMMARY `peakRetainedCandidates` may exceed
  the ceiling (honestly reported, defectively enforced).
- **Skutek:** the limit bounds per-blob `found` and stops growth only after a file boundary; the
  stated peak-across-all-structures property does not hold. Bounded overshoot (≤ `top`-1 per
  crossing file), no science corruption (tool is CANDIDATE_ONLY on synthetic inputs).
- **Required narrow correction:** charge every retained record (per-blob `found` pushes AND
  `allRows` pushes) against one global budget counter checked BEFORE the push
  (e.g. `budget.tryRetainGlobal()` in both sites), so `rows.length + found.length` never
  exceeds the ceiling; add a B5 variant with ≥2 inputs asserting the peak stays ≤ ceiling.
- **Revalidation gate:** re-run the 9-input probe (or new test): `peakRetainedCandidates <= 256`
  with exhaustion marked at the 256th retention; B5 multi-input test green.

## F2 (P2) — SCANNED_BYTES reservation happens AFTER the payload read; README/POST claim "reservation before read"

- **File/lines:** `tools/placement_probe/placement_probe.mjs` — raw path: line 347
  `budget.containerReadBytes += size; const bytes = fs.readFileSync(file)` executes **before**
  line 387/388 `budget.admitPayload(bytes.length, ...)`; container path: line 374
  `p = arch.readEntry(e).payload` (extraction) executes **before** line 378
  `budget.admitPayload(payload.length, ...)`.
- **Contradicted claim:** contract §8 — "Rezerwuj budżet przed dopuszczeniem/odczytem payloadu,
  wykorzystując zweryfikowany rozmiar, i kontroluj wynik rozpakowania."; README.md lines 55-56
  "reserved before payload read using the verified size"; POST/BUDGET_ACCOUNTING B2 title
  "reservation before read"; budget.test.mjs B2 test name.
- **Evidence (code order + behavior):** in the B2 exceed case the refused raw input is fully
  read into memory and charged to `containerReadBytes` before the SCANNED_BYTES refusal; in B1
  the 33rd container entry is extracted by `readEntry` before `admitPayload` refuses it. The B2
  test asserts refusal + OVER_BUDGET disposition (true), not non-read.
- **Failure mechanism:** the implemented ordering is read→verify→reserve→admit; only
  "refused before admission/scan" holds. An over-budget payload still costs a full read
  (bounded by `maxInputMiB`/`maxPayloadMiB`, e.g. up to 650 MiB per raw input).
- **Affected:** §8 SCANNED_BYTES ordering requirement; README/POST/B2 wording (report/code
  drift); B1's 33rd-entry extraction cost.
- **Required narrow correction (either):** (a) reserve before the read using the verified
  pre-read size (`statSync` for raw; declared `e.size` for entries, with the existing post-read
  mismatch check converting to PARSE_FAILED without scan), or (b) correct the wording in
  README/POST/test-title to "reserved before payload admission (scan)" and keep the separate
  container-read accounting. Do not leave the "before read" claim as-is.
- **Revalidation gate:** order-sensitive test (e.g. a fixture whose read is observable/bounded
  by the budget) or wording sweep with grep showing no "reservation before read" claim
  remains for the unimplemented ordering.

## F3 (P2) — B3 exceed case does not aggregate across inputs; input 2 labeled SCANNED but never analyzed; wrong test message

- **File/lines:** `tools/placement_probe/tests/budget.test.mjs` lines 68-85 (B3 test);
  `placement_probe.mjs` lines 396-402 (admitted-but-unanalyzed skip) and 387-390 (SCANNED
  disposition at admission); `POST/run_post.mjs` B3 record; CORRECTION_MATRIX.csv row B3.
- **Contradicted claim:** test title "B3: LAYOUT_EVALUATIONS — aggregation across two inputs
  in one invocation; boundary at exactly the cap" and assertion message "second input was
  admitted and partially scanned before the layout stop"; CORRECTION_MATRIX B3 expectation
  "aggregation across >=2 inputs" stamped PASS.
- **Evidence (measured):** `qc_micro_probes.mjs`: one `records80` input at `--max-stride 512`
  (default maxHeader=64) consumes **2142** layout attempts (17 headers × 126 strides). The B3
  cap of 700 therefore stops during **input 1** at attempt 701 (POST B3 refusal itself records
  `syntheticInputs: 1, scannedBytes: 2576`). Input 2 is admitted (disposition SCANNED at line
  390) and then skipped without any analysis (line 397-401, skip row BUDGET_EXHAUSTED) — it was
  never "partially scanned". The cross-input aggregation of the layout counter is only shown by
  the unasserted default-case measurement 4284 = 2×2142.
- **Failure mechanism:** test design used a cap below a single input's natural attempt count;
  the exceed predicate therefore never reaches the second input. The census marks
  admission-time SCANNED for a payload the probe then refuses to analyze, contradicting §5.2's
  disposition meaning and its rule that known remaining entries after exhaustion are
  OVER_BUDGET (the honest skip row exists but the disposition label is wrong).
- **Affected:** §8 test requirement (aggregation across ≥2 inputs for shared limits); §5.2
  disposition truthfulness in SUMMARY exclusionCensus; POST B3 record; CORRECTION_MATRIX B3 row.
- **Required narrow correction:** set the B3 exceed cap so the refusal occurs during input 2
  (e.g. 2142 = exactly input 1's total, or 2500); record admitted-but-unanalyzed payloads with
  an honest disposition (OVER_BUDGET per §5.2, or a new defined+tested category such as
  ADMITTED_NOT_ANALYZED); fix the test message; regenerate POST/matrix.
- **Revalidation gate:** B3 exceed refusal shows `syntheticInputs: 2, scannedBytes: 5152` with
  the stop inside input 2; no census row labels an unanalyzed payload SCANNED.

## F4 (P2) — CORRECTION_MATRIX.csv ORIGINAL_SEVEN_TESTS row self-contradictory (FAIL outcome from a wrong predicate)

- **File/lines:** `POST/gen_matrices.mjs` line 12 (predicate
  `tr.failCount === 0 && tr.testsCount === 7 ? 'PASS' : 'FAIL'`); generated
  `CORRECTION_MATRIX.csv` row 2: `measured_outcome=FAIL`, evidence `suite=23 pass=23 fail=0
  exit=0`, `disposition=case_pass`.
- **Contradicted claim:** the row's own expectation "all 7 original tests pass on the corrected
  tool" — which is TRUE (the original 7 test files are byte-identical to the kit pins and pass
  inside the 23-test suite; QC re-executed 23/23).
- **Evidence:** the predicate tests the TOTAL suite count (23 ≠ 7), so the generated outcome is
  FAIL regardless of the original tests passing; the same row's disposition is `case_pass`
  (`failCount === 0`). Internal contradiction inside one published row.
- **Failure mechanism:** generator predicate conflated "the suite consists of exactly the 7
  original tests" with "the 7 original tests pass" after new tests were added to the same suite.
- **Affected:** CORRECTION_MATRIX.csv (published report artifact); any reader/automated check
  consuming measured_outcome.
- **Required narrow correction:** predicate on the 7 original tests passing (e.g. assert the 7
  known original subtest names appear as `ok` in the TAP stdout), regenerate the matrix.
- **Revalidation gate:** regenerated row shows a consistent PASS/case_pass (or an explicitly
  reworded expectation); no row in the matrix contradicts its own evidence cell.

## F5 (P3) — POST B6 stored error message silently truncated (slice(0,80))

- **File/lines:** `POST/run_post.mjs` line 252 (`message: e.message.slice(0, 80)`); stored in
  `POST_MEASUREMENTS.json` B6 and replicated in `BUDGET_ACCOUNTING.json` B6.
- **Claim affected:** provenance fidelity of the stored INVALID_CONFIGURATION text.
- **Evidence (measured):** full message is `"INVALID_CONFIGURATION: budgetThresholds.layoutEvaluations
  out of range [1, 100000] (ceiling 100000): 100001"`; the stored slice is exactly
  `"INVALID_CONFIGURATION: budgetThresholds.layoutEvaluations out of range [1, 10000"` — cut
  mid-number, losing the ceiling and the offending value (`qc_micro_probes.mjs`).
- **Required narrow correction:** store the full message (or mark truncation explicitly);
  regenerate POST/BUDGET_ACCOUNTING.
- **Revalidation gate:** stored string equals the live message byte-for-byte.

## F6 (P3) — dangling test-file reference in ids_from_export.mjs header

- **File/lines:** `tools/placement_probe/ids_from_export.mjs` lines 5-7 — "reproduced
  synthetically in tests/dat-helper.test.mjs". No such file exists; the reproduction is O7 in
  `tests/correction_matrix.test.mjs` (verified executed, 23/23 suite).
- **Required narrow correction:** point the comment at tests/correction_matrix.test.mjs (O7).
- **Revalidation gate:** grep shows no dangling test path in the tool's comments.

## F7 (P3) — POST outcome labels are hardcoded literals; CONTROL_PASS class unused

- **File/lines:** `POST/run_post.mjs` — every `rec(...)` call stamps `outcome: 'PASS'` as a
  literal; counter loop lines 274-281 counts those labels; `generated.controlPass` is 0.
- **Claim affected:** §10 "Generuj liczniki z wyników i oddzielaj cases od outcomes" and the
  CONTROL_PASS semantics ("Oczekiwane odrzucenie negatywnego wejścia jest CONTROL_PASS").
- **Evidence:** O1 (CLI bad config, exit 3 expected), B6 (CLI raised threshold, exit 3
  expected) and O7 (.dat rejection, exit 1 expected) are expected-rejection cases labeled PASS;
  no harness predicate evaluates any case condition. QC found no false PASS (all stamped values
  independently verified), but nothing in the harness would catch one.
- **Required narrow correction:** derive `outcome` from explicit per-case predicates inside
  run_post.mjs; label expected-rejection cases CONTROL_PASS; keep the counter generated.
- **Revalidation gate:** a deliberately broken fixture in a dry run flips the outcome label
  (demonstrated sensitivity), and O1/B6-CLI/O7 appear under controlPass.

## F8 (P3) — FEATURE_COVERAGE_MATRIX cites FINAL_REPORT.md before it exists

- **File/lines:** `FEATURE_COVERAGE_MATRIX.csv` row 14 ("placement/world/instance semantics",
  evidence "standing science block in README + FINAL_REPORT").
- **Evidence:** FINAL_REPORT.md is not on disk at QC time (§11 pipeline generates it after QC).
- **Required narrow correction:** re-verify (or regenerate the matrix) after FINAL_REPORT.md is
  written; if its standing-science block is omitted, the evidence cell is false.
- **Revalidation gate:** at publication time both cited artifacts exist and contain the
  standing-science statuses.

## F9 (P3) — "aggregation across ≥2 inputs" letter only partially exercised (§8)

- **File/lines:** `tests/budget.test.mjs` B1 (33 entries of ONE input file), B5 (single input);
  B3 exceed stops inside input 1 (F3).
- **Evidence:** B2/B4 cover two inputs; the shared-counter mechanics are additionally shown by
  B7 (class-level no-reset) and the B3 default-case measurement 4284=2×2142 (recorded, not
  asserted). The strict §8 letter (≥2 inputs per shared limit) is unmet for SYNTHETIC_INPUTS
  (payload-level aggregation within one container is shown instead) and RETAINED_CANDIDATES
  (no cross-input case at all; see F1).
- **Required narrow correction:** add two-input variants for SYNTHETIC_INPUTS (e.g. two
  containers whose summed payloads cross 32) and RETAINED_CANDIDATES, or document explicitly in
  the matrix why payload-level aggregation subsumes the input-level letter for SYNTHETIC_INPUTS.
- **Revalidation gate:** new tests assert the exhaustion moment with inputs=2 for both limits.

## F10 (P3) — additional census categories defined but untested (§5.2)

- **File/lines:** `placement_probe.mjs` lines 341-346 (INPUT_TOO_LARGE), 371
  (ENTRY_TOO_LARGE), 376 (PAYLOAD_SIZE_MISMATCH → PARSE_FAILED), 360-363 (container-level
  UNSUPPORTED + CONTAINER_PARSE_FAILED skip). README defines the full disposition order.
- **Claim affected:** §5.2 "Ewentualna dodatkowa kategoria wymaga definicji i testu."
- **Evidence:** no test in the suite or POST battery drives a >4 MiB payload, a >650 MiB input,
  a size-mismatched entry, or a bad-framing container; those dispositions are implemented but
  never observed. (Not evidence of malfunction — recorded as untested.)
- **Required narrow correction:** one small synthetic test per category (they are cheap:
  bad-magic container, tiny-but-declared-mismatch entry, lowered `--max-payload-mib` /
  `--max-input-mib` thresholds for the size caps).
- **Revalidation gate:** each additional disposition appears in a test's exclusionCensus with a
  reconciled sum.

---

## Verified-not-defective (explicitly checked, no finding)

- PRE artifacts preserved and truthful; PRE not overwritten by POST (§4 ✓).
- The 7 original test files byte-identical to the kit pins; 23/23 suite pass re-executed by QC.
- S7a/S7b/O3 values independently reproduced from raw fixture bytes by a QC-owned
  implementation (see QC_RECOMPUTATION.json); fixture SHA256s byte-identical to POST
  fixtureIdentity.
- POST measurements match the corrected code's actual computed behavior on every value QC
  re-executed (S7a, S7b, O1, O2 real-adapter census, O3, O4, B6 rejection).
- No placement/world-XYZ/join/milestone over-claims anywhere; standing science statuses
  preserved verbatim; no trivially-true test assertions (the round-1 weak assertion verifiably
  removed).
- Budget exhaustion → BUDGET_EXHAUSTED + COVERAGE=PARTIAL, never NO_CANDIDATE; ceilings never
  raised (B6, both exported and CLI paths); container-read/control-work bytes accounted
  separately (B7 + QC's O2 run: containerReadBytes 7847 / controlWorkBytes 148352).
- FULL_CENSUS_ROWS charged per candidate-row unit and aggregated across inputs (B4 verified:
  input 1's finalists consume 160 rows, input 2's finalists → PARTIAL_BUDGET_EXHAUSTED).
