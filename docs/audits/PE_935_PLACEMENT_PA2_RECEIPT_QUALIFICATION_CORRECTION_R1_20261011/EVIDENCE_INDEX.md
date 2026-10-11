# EVIDENCE_INDEX — PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011

Every essential outcome in this package records MEASURED_QUANTITY, EXPECTED, ACTUAL,
UNIT/DENOMINATOR, SOURCE_OF_TRUTH, WHY_NON_CIRCULAR, FAILURE_CASE_DETECTED, RESULT,
code/input identities and the command. All sizes/SHA256 of the package files are in
MANIFEST_SHA256.csv (generated LAST from this exact content). Paths below are relative
to `docs/audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011/`.

## Governing contract

| File | Content |
| --- | --- |
| CONTRACT.md | Byte-identical copy of the dispatched contract (29207 B / SHA256 6E4B0B029DBD082451A6F0E432AA66124FCC5E3299260AC3E330A59DED4F4E23; dispatch pin file is the source) |

## PRE (frozen; never rewritten after execution)

| File | Content |
| --- | --- |
| PRE/SOURCE_IDENTITIES.json | Preflight identities: contract SHA/size, refs (SOURCE_REF/RESULT_REF/master), worktree HEAD/branch, node/git versions, Desktop evidence (4 files MATCH), 7 BASE load-bearing files (MATCH), allowlist, protected files |
| PRE/INPUT_IDENTITIES.json | The 16 frozen EXPECTED_INPUT_PINS verified live through the hash-verified gate module (PASS 16/16, exit 0); kit ZIP pin + 7 FILE_HASHES members verified |
| PRE/BASELINE_REPRODUCTIONS.json | §3 defect reproduction: the UNCHANGED BASE full POST in three isolated private copies — CLEAN, M1 (MEASURED.sha256 zeroed), M2 (gateModule.sha256 zeroed): all three QUALIFICATION_PASS/exit0 with suite 53/53 (the externally measured false-PASS), commands/hashes/exit codes/receipt diffs recorded |
| PRE/RAW/clean/** | Raw PRE outputs of the CLEAN case (POST_TEST_RESULTS/POST_MEASUREMENTS/IDENTITY_GATE_COUNTERCHECKS/OBJECT_IDENTITY_OBSERVATIONS + stdout/stderr + receipt_under_test.json) |
| PRE/RAW/m1/** | Same for M1 (perPin[0].MEASURED.sha256 zeroed) |
| PRE/RAW/m2/** | Same for M2 (moduleIdentity.gateModule.sha256 zeroed) |
| PRE/RAW/gate_live_report.txt | The live 16-pin gate verification report (node tools/placement_probe/verify_inputs.mjs; PASS 16/16, exit 0) |
| NOTE | raw-evidence directories use SHORT names (clean/m1/m2, clean/m1..m9, b1) to keep every package path under the Windows MAX_PATH limit for auditor tooling; the full case names are recorded in PRE/BASELINE_REPRODUCTIONS.json and POST/RECEIPT_MUTATION_MATRIX.json |

## POST (correction evidence; final matrix batch 3 unless noted)

| File | Content |
| --- | --- |
| POST/RECEIPT_MUTATION_MATRIX.json | The fixed 10-case full-POST matrix (CLEAN + M1..M9): PA2 verdict, overall verdict, exit code, refusal reason, recomputed-vs-claimed values, module-identity check, live remeasurement, per-case suite counts, other-case results, receipt-untouched proof, frozen batch code identity (freezeOk=true) |
| POST/FULL_POST_RESULTS.json | One line per full-POST case (verdicts + exits) |
| POST/AGGREGATOR_CONTROLS.json | Three ACTUAL aggregator controls (PA2 missing/FAIL/NOT_PERFORMED) over the real measured CLEAN outcomes via the shared computeQualification + EXPECTED_OUTCOMES |
| POST/VALIDATOR_PROFILE_CONTROLS.json | Four unit profile controls (wrong runId, wrong stage, wrong mode, unreadable/truncated JSON) + the CLEAN-unchanged control; separately counted from the ten full-POST cases |
| POST/LIVE_INPUT_REMEASUREMENT.json | INPUT_BYTES_REMEASURED: the unchanged verifyAllInputs live remeasurement of the 16 evidence paths inside the CLEAN canonical POST (per-pin exists/size/SHA/compareResult) |
| POST/TWO_SOURCE_AGGREGATION.json | DA2-COV cap32 two-contributing-source evidence: contributions 29+3, total 32, peaks 29/32/32, both inputs opened, four outputs byte-identical, budgets identical, WeakMap observer phases + code identity, negative protection reference |
| POST/REGRESSION_RESULTS.json | BASE 53 replay (53/53), original seven kit tests (7/7 from the verified ZIP), current suite 64/64 (53 BASE + 11 new), required-prefix presence, commands |
| POST/RAW/{clean,m1..m9}/** | Per-case raw POST outputs (POST_TEST_RESULTS/POST_MEASUREMENTS/IDENTITY_GATE_COUNTERCHECKS/OBJECT_IDENTITY_OBSERVATIONS + stdout/stderr) |
| POST/RAW/receipts/** | The receipt-under-test files: CLEAN.json + M1..M9.json mutants + unit-control receipts (wrong_runId/wrong_stage/wrong_mode/truncated/CLEAN_control) |
| POST/RAW/driver/** | Raw driver outputs: matrix_receipt_mutations.json, full_post_results.json, aggregator_controls.json, validator_profile_controls.json, two_source_raw.json |
| POST/RAW/b1/** | Retained essentials of invalidated matrix batch 1 (driver extraction crash at M5; CLEAN..M4 had succeeded): BATCH1_NOTE.json + per-case essentials + receipts |

## QC

| File | Content |
| --- | --- |
| QC/INTERNAL_REVIEW.md | EXECUTOR-SELF-QC review (origin/limitations labeled; FRESH_CONTEXT_INTERNAL_QC=NOT_PERFORMED_IN_EXECUTOR_SESSION assigned to the separate later pe-master-auditor pass) |
| QC/FINDINGS.json | 7/7 self-QC probes PASS + findings ledger (SELF-QC-F1..F4, all P3; no P0/P1/P2 in this correction scope) |

## Records and accounting

| File | Content |
| --- | --- |
| BUDGET_ACCOUNTING.json | Unchanged scanner ceilings (never raised), lowered fixture limits, full execution census (each full-POST case separately counted), identity hashing of pinned evidence, secrets statement |
| AMENDMENT_LOG.md | Full iteration chronology: PRE, initial implementation, matrix batches 1 (invalidated) / 2 (superseded) / 3 (FINAL), wording corrections, round accounting (correction rounds against the tool: 0/2), the pa2_identity_gate.test.mjs wording diff record |
| SUPERSESSION.md | §6 records-only supersession (PA2_INPUT_COMPARISON / PA2_RUNNER_EXIT3_ON_MISMATCH preserved-confirmed; HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM retracted; PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT not-established) + the PA2-RC1 acceptance-condition supersession + DA2-COV closure |
| MANIFEST_SHA256.csv | Generated LAST: repository-relative path, byte size, SHA256 of every changed tracked path vs BASE (self-excluding only this manifest); scope/unit declaration; bijection = changed paths minus this one manifest |

## Supporting runnable code (outside the package, in the authorized code roots)

| Path (repo-relative) | Identity |
| --- | --- |
| tools/placement_probe/qualification/pa2_r1/run_post.mjs | CANONICAL_POST (SHA256 in manifest; batch identity 301e081d…) |
| tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs | shared receipt validator + computeQualification + EXPECTED_OUTCOMES (37e679b3…) |
| tools/placement_probe/qualification/pa2_r1/two_source.mjs | DA2-COV WeakMap observer + measurement (bf6ae49d…) |
| tools/placement_probe/qualification/pa2_r1/run_matrix.mjs | outer bounded matrix driver (f2026073…) — never invoked by the canonical POST |
| tools/placement_probe/tests/pa2_receipt_qualification.test.mjs | permanent PA2-RQ regression (11 tests) |
| tools/placement_probe/tests/da2_two_source.test.mjs | permanent DA2-COV regression (2 tests, incl. the cap29 negative control) |
| tools/placement_probe/tests/pa2_identity_gate.test.mjs | BASE file with ONLY the §6 comment/assert-message corrections (recorded diff; assertions unchanged) |
