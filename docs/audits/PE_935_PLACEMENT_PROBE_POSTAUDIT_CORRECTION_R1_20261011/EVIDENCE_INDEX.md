# EVIDENCE_INDEX.md — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011

All evidence of this run, with exact repo-relative paths. Package files = 33
(including this index and MANIFEST_SHA256.csv); tools changes = 9 (3 modified + 6 new);
AUDIT_ENTRYPOINT.md = exactly one appended table row; total changed paths vs BASE =
43 (manifest covers all except MANIFEST_SHA256.csv itself: 42 rows).

## PRE (PRESERVED PRE — recorded BEFORE any correction; harnesses ran only in isolated stage copies)

- `PRE/BOOT_INPUT_IDENTITIES.json` — fail-closed BOOT: contract (23496 B / 38205CE5…)
  and INPUT_PINS (4550 B / F3954132…) identity PASS; 16/16 pinned inputs MATCH;
  4/4 Git blob pins at BASE MATCH; ZIP pin + 7 FILE_HASHES.json members verified;
  SOURCE_REF == BASE 938aa946, RESULT_REF absent (local+remote), master 3fbe93ee
  separate, worktree HEAD == BASE.
- `PRE/BASELINE_FILE_HASHES.csv` — SHA256/size of every tools/adapters/entrypoint file
  at BASE before the correction (12 rows).
- `PRE/SOURCE_PACKAGE_FREEZE.json` — the frozen historical package
  `PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011`: 37/37 Git blobs listed,
  READ_ONLY policy stated.
- `PRE/BASE_TEST_RESULTS.json` — original 7 kit tests from the pinned ZIP (7/7 pass,
  exact names matched) + the BASE 27-test suite (27/27) — both in isolated stages,
  stage identities recorded.
- `PRE/BASE_POST_REPLAY.json` — replay of the frozen historical POST battery on
  unchanged BASE: 47 PASS / 0 FAIL (20 named outcomes + 27-suite), from a private
  byte-identical copy of the frozen harness.
- `PRE/PRE_MEASUREMENTS.json` — factual PRE of every defect on unchanged BASE:
  DA-1 (e2/e3 false SCANNED, scannedPayloadCount=4), DA-2 (cap4: tracker 4 vs
  distinct 8/8; cap256: 256 vs 280/512; byte-identical outputs), DA-3 (injected
  Budgets 100001/NaN/512 accepted; control refused), layout-61 semantics, the
  independent XYZ arithmetic (56/80=0.7), PA-1 (A/B/C pins byte-exact + production
  baseline on BASE), PA-2 (the literal `verdict: 'PASS'` lines of the frozen
  historical generator).
- `PRE/BRANCH_RESERVATION.json` — GitHub REST Create-a-reference receipt: HTTP 201,
  ref/sha match, follow-up GET 200, create-only policy, transport note (gh CLI
  unauthenticated; direct REST via the credential-manager token in-memory only),
  no tokens stored.
- `PRE/verify_inputs_runner.mjs` — the PA-2 live gate runner (REAL_SEQUENCE mode),
  with the downstream spy; actually invoked before POST (receipt below).
- `PRE/reproduce_pre.mjs` — the PRE reproducer harness (adapted from the pinned
  Desktop adversarial_checks.mjs; documented diff = paths only).
- `PRE/gen_pre.mjs` — extra harness (censused): regenerates BOOT_INPUT_IDENTITIES /
  BASELINE_FILE_HASHES / SOURCE_PACKAGE_FREEZE with node:crypto against frozen pins.

## POST (preregistered battery; executed AFTER the correction on isolated stage copies)

- `POST/PREREGISTERED_CONFIG.json` — written BEFORE POST: every case's config,
  fixture identity, expected result, denominator, negative control, and the planned
  invocation counts (2 suites, 14 tool CLI, 3 gate-runner mutants, 1 live gate already
  run).
- `POST/POST_TEST_RESULTS.json` — 13 named cases, each with CASE_ID,
  CODE/FIXTURE_IDENTITY, EXPECTED, ACTUAL, MEASURED_QUANTITY, UNIT/DENOMINATOR,
  SOURCE_OF_TRUTH, NEGATIVE_CONTROL, FAILURE_CASE_DETECTED, TEST_RESULT:
  12 PASS + 1 CONTROL_PASS (DA2_MUTANT_COPY) + 0 FAIL; suite 53/53; final
  QUALIFICATION_PASS; aggregator refuses on any single required-result removal.
- `POST/POST_MEASUREMENTS.json` — the same battery as measurements
  (code identity, stage copies, per-case measured values, generated counters).
- `POST/IDENTITY_GATE_LIVE_RECEIPT.json` — the REAL-sequence live gate invocation
  (before POST): PASS 16/16, exit 0, call path + module identities recorded.
- `POST/IDENTITY_GATE_COUNTERCHECKS.json` — the three mutant gate runs (private
  copies, unchanged expected pins): all BLOCKED_INPUT_IDENTITY, exit 3,
  downstreamCalls all zero; no real GitHub write.
- `POST/OBJECT_IDENTITY_OBSERVATIONS.json` — the DA-2 identity observer: full
  per-phase records for cap4/cap256 (creation/forward/serialization), the
  forced-copy mutant detection, the aliasing positive control, PRE-vs-POST
  reference values, instrumentation markers.
- `POST/run_post.mjs` — the POST harness itself (reproducible; stage-isolated).

## QC (fresh-context internal QC — a distinct phase with its own probes)

- `QC/INTERNAL_REVIEW.md` — what the QC phase PERSONALLY MEASURED (5 fresh probes,
  different fixtures/instrument points/pins) vs only READ; the porcelain-trim
  harness bug it caught; the counter-semantics statement; independence honesty
  (internal QC ≠ external Desktop post-audit; EXTERNAL_DESKTOP_POST_AUDIT=PENDING).
- `QC/FINDINGS.json` — the findings ledger: 3 closed P2 + 2 closed earlier
  observations; 0 open P0/P1/P2; 4 open P3 (historical SHA-typo record, preserved
  61-request semantics, superseded historical reservation, R2-4 accounting
  limitation); standing science block.
- `QC/GATE_MATRIX.csv` — G1..G8 + QUALIFICATION, each with its question, evidence
  and verdict (all PASS).
- `QC/FINAL_GATE.json` — FINAL_GATE=QUALIFICATION_PASS with the science freeze,
  fix-round accounting and scope facts.
- `QC/qc_fresh_probes.mjs` — extra harness (censused): the five fresh probes
  (census tail on fresh 6-entry bytes; object collections at a different instrument
  point; effective Budget on a fresh mutated instance; live gate on a fresh private
  mutant; scope/frozen-package git probes).
- `QC/QC_FRESH_PROBE_OUTPUT.json` — the probe results: INTERNAL_QC_PASS 5/5.

## Package-level documents

- `AMENDMENT_LOG.md` — the full change chronology with honest bring-up vs fix-round
  classification.
- `SUPERSESSION.md` — the PA-2 supersession statement (historical literal-PASS
  generator; old manual check UNVERIFIED).
- `CORRECTED_STATUS_ALGEBRA.md` — the DA-1 disposition/state algebra, the census
  gate rules, the request/refusal algebra, the distinct-record algebra.
- `CORRECTION_MATRIX.csv` — defect → PRE → correction → POST → tests → verdict.
- `FEATURE_COVERAGE_MATRIX.csv` — every required feature mapped to its covering
  tests and POST cases.
- `BUDGET_ACCOUNTING.json` — the five canonical limits (unchanged), per-limit
  legal-boundary/refusal/aggregation coverage, distinct-record accounting,
  invocation plan vs actual, fix-round accounting.
- `FINAL_REPORT.md` — the run's terminal report (all contract section P fields;
  commit SHAs recorded as NOT_CREATED at freeze time — the actual values are in the
  post-publication receipts and the terminal report to PE-MASTER).
- `HANDOFF.md` — what the next session must know, must NOT inherit as established,
  and the exact resume instruction if anything were PARTIAL/blocked.
- `EVIDENCE_INDEX.md` — this index.
- `MANIFEST_SHA256.csv` — generated LAST: path,sizeBytes,sha256 for every changed
  path vs BASE except itself (42 rows; bijection verified, zero mismatches).

## Changed paths outside the package (allowlist)

- `tools/placement_probe/placement_probe.mjs` (modified — DA-1/DA-2/DA-3)
- `tools/placement_probe/verify_inputs.mjs` (new — PA-2 gate)
- `tools/placement_probe/README.md` (modified — documentation)
- `tools/placement_probe/tests/fixtures.mjs` (modified — PA-1 pinned builders)
- `tools/placement_probe/tests/da1_census.test.mjs` (new)
- `tools/placement_probe/tests/da2_retained.test.mjs` (new)
- `tools/placement_probe/tests/da3_budget.test.mjs` (new)
- `tools/placement_probe/tests/pa1_regression.test.mjs` (new)
- `tools/placement_probe/tests/pa2_identity_gate.test.mjs` (new)
- `AUDIT_ENTRYPOINT.md` (exactly one appended table row; 1 insertion / 0 deletions)
