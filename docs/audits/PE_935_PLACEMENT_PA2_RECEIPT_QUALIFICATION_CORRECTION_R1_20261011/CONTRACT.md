# PE-MASTER — PA2 Receipt Qualification Correction R1

## 0. Contract and execution authority

```ini
RUN_ID = PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
RUN_CLASS = SUPPORTING
RUN_TYPE = BOUNDED_CORRECTION_ONLY
REPOSITORY = SebastianKozlo/eudoria-clean
EXPECTED_BASE_SHA = 28e91eb67511a3022a911ab6d4e02e68119b1f68
SOURCE_BRANCH = research/pe935-placement-probe-census-postaudit-r1-20261011
SOURCE_REF = refs/heads/research/pe935-placement-probe-census-postaudit-r1-20261011
RESULT_BRANCH = research/pe935-placement-pa2-qualification-correction-r1-20261011
RESULT_REF = refs/heads/research/pe935-placement-pa2-qualification-correction-r1-20261011
OBSERVED_MASTER_SHA = 3fbe93eec04759395223e6677b5040273d29222a
LOCAL_RUN_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
WORKTREE_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011\workspace\eudoria-clean
OUTPUT_REPO_PATH = docs/audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
QUALIFICATION_CODE_ROOT = tools/placement_probe/qualification/pa2_r1
CANONICAL_POST = tools/placement_probe/qualification/pa2_r1/run_post.mjs
MAX_CORRECTION_ROUNDS = 2
NEW_EXE_ACCESS = NO
NEW_GAME_PAYLOAD_SCANS = 0
NEW_SCIENCE_EDGE_INTERPRETATIONS = 0
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

This document is a complete proposed work order, not execution authorization by itself. Execute only after a separate human message identifies this contract by its measured size/SHA256 and authorizes this single correction-only run and commit/push to RESULT_REF. Creating this document or reading it does not authorize a run. The companion START_OPENCODE.txt is the prepared human dispatch message.

Mission: close PA2-RC1/P2 by making the actual canonical POST refuse inconsistent identity receipts; correct the PA2-RC2/P3 downstream claim through records only; add the DA2-COV/P3 two-contributing-source regression. Preserve DA1, DA2, DA3 and PA1 in their externally audited scope. Do not redesign the scanner or build a general provenance framework.

No fixed duration or hours target. Scope and the two repair rounds bound this work. Complete implementation, evidence, internal QC and safe persistence; do not stop at research or a proposal. A negative scientific/tooling outcome is reportable and can be published under section 10. It does not authorize another run.

## 1. Preflight and trusted inputs

Read this entire document before dispatch or modification. Verify its bytes against the separate dispatch pin. A mismatch, missing required input, wrong source ref, pre-existing result ref/worktree/run root, or inability to establish baseline integrity is BLOCKED_PREFLIGHT: no correction, ref reservation or commit/push. Report exact failed checks. Do not silently adapt the base, names, pins or paths. Use existing suitable repository object storage to create the specified isolated worktree; never reset, clean or switch a checkout belonging to other work.

Fetch/read live source and master refs. SOURCE_REF, its fresh remote-tracking ref, the selected source commit object and the new worktree HEAD must resolve to EXPECTED_BASE_SHA. Master is a separately observed ref, not this run's base: measure it before/after and do not modify it. If master moves through unrelated work, record that external change without rebasing this run. RESULT_REF must be absent locally and remotely. Reserve only RESULT_REF create-only at EXPECTED_BASE_SHA after input preflight; verify that reservation. No overwrite, force push or reuse of a pre-existing branch. Worktree and private staging must stay under LOCAL_RUN_ROOT.

Required external Desktop evidence root (READ_ONLY):

`C:\Users\User\Documents\ChatGPT\PE\PE_PLACEMENT_PROBE_POSTAUDIT_28E91EB_20261011`

| File | Expected bytes | Expected SHA256 |
| --- | ---: | --- |
| REPORT.md | 12180 | C5763BBF458FE0E724EBAB2BB5B5D6B457F697B82E4788EEA236BCB61820A4FB |
| ADVERSARIAL_RESULTS.json | 12117 | AEB19E89DE9CB474DFC0AB3337B4B551D060FAF8A4E9DDD6F2A348E62E06F246 |
| RECEIPT_MUTATION_RESULTS.json | 2073 | E0B61A041F5C5BA1D75DFFD5A058E1799D2F2000D66B92B21999D4CC2101A717 |
| FINDINGS.json | 1601 | BDE2BEAD1993DE37080A42BA88A23DA072796E8CBE5B65B22F0FBDC6EBEA1B65 |

Measure each physical file separately and compare to the constants above. Read the report and relevant raw results. Expected pins are supplied here, not generated from measured values. Timestamps are contextual metadata, not proof of authorship or execution order. No unpublished REPORT.md or invented evidence is required.

Frozen predecessor package prefix:

`docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011`

The following BASE files are load-bearing. Resolve each from EXACT EXPECTED_BASE_SHA; verify bytes/SHA and Git blob identity independently of any receipt. Here PP means the full predecessor prefix above.

| BASE path | Expected bytes | Expected SHA256 |
| --- | ---: | --- |
| tools/placement_probe/verify_inputs.mjs | 9019 | 568CE3F29F68EBDDF5AA40E7550278717CD6E9F868A239FB132AE2C623A2B43D |
| tools/placement_probe/placement_probe.mjs | 54156 | 0D69AAFEBC908E7B6677B4F676BBB378BBF7417CC0C44715917FBEAE5006FA6E |
| tools/placement_probe/tests/pa2_identity_gate.test.mjs | 8739 | 5FC89BC093BCB9C76FB88F4F84101737129B8B180BC6F79AA6B3258BBB8F14B0 |
| tools/placement_probe/tests/da2_retained.test.mjs | 12988 | 0927352F5E91B7BF57BF3FB97A8E089397A295CC4CA39030609056F902312896 |
| PP/POST/run_post.mjs | 48995 | 3BBDC404E40B0ED2135BA74D5C978E5DB810AAD0A962C45D23FBE04D4B25C3BB |
| PP/PRE/verify_inputs_runner.mjs | 4783 | A4733B0DCF17C669E564232FE3E6663DE08B0093E66F30A9D5F3B502BF6C2FDC |
| PP/POST/IDENTITY_GATE_LIVE_RECEIPT.json | 8251 | 837030AB901D7E2D3CA72C89D555F0C75D06B4CC04E0A71B1793841D52A1DA88 |

Read the BASE gate, runner, full POST, preregistered configuration, relevant tests and adapters. Verify the 16 frozen EXPECTED_INPUT_PINS using the hash-verified gate module; do not take expected values from the receipt. These 16 inputs are documents/code/kit evidence, not permission to scan game data. Remeasure those existing pinned files and record each result. Missing/mismatched required evidence blocks preflight. Read and verify the original ZIP through its existing frozen pin, extract only into private staging, and verify its FILE_HASHES.json members for replay of the original seven tests.

The CLEAN receipt hash above identifies the exact baseline fixture. It MUST NOT become a validator rule that simply rejects any changed receipt hash: mutant rejection must arise from the corrected PA2 semantics. Record mutant hashes/diffs without enforcing the CLEAN whole-file hash on them.

Record baseline identities and inventories before edits: all historical docs/audits tracked blobs, protected tool/adapters, source and result refs, master, selected worktree state, Node/Git versions, existing foreign changes. Preserve foreign files/worktrees/servers and untracked content. Read applicable repository AGENTS.md instructions. If a required skill applies, read it and record its identity; do not use it to expand this contract.

## 2. Standing and allowed work

```ini
DA1 = CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES
DA2 = CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES
DA3 = CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES
PA1 = CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES
PA2_INPUT_COMPARISON = CONFIRMED
PA2_POST_QUALIFICATION = OPEN_P2
PA2_DOWNSTREAM_SPY_PROOF = NOT_ESTABLISHED
GENERAL_TOOL_CORRECTNESS = NOT_ESTABLISHED
```

Exact changed-path allowlist:

```text
tools/placement_probe/qualification/pa2_r1/**
tools/placement_probe/tests/**
docs/audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011/**
AUDIT_ENTRYPOINT.md
```

AUDIT_ENTRYPOINT.md: append exactly one new physical Markdown line linking the new package and qualification entrypoint, with measured disposition and external post-audit PENDING. Preserve all existing bytes; do not insert/delete/rewrite historical entries. Verify additions=1/deletions=0.

Do not modify placement_probe.mjs, verify_inputs.mjs, ids_from_export.mjs, archive adapters, package.json, SDKs, original payloads, private Desktop evidence or historical audit packages. Tests may gain bounded regressions and correct active misleading descriptions; do not weaken existing assertions or drop coverage. Preserve an exact BASE replay of the original 53 tests separately from the new test set. Updating a title/comment does not erase its historical wording.

Protected historical packages remain READ_ONLY. Historical scripts may write relative to their own location: execute only private byte-identical copies, never scripts inside the source package or Desktop snapshot. Canonical new code lives at CANONICAL_POST. The new package references predecessor code by exact Git SHA/path/hash and documents the narrow supersession; avoid competing copies of current qualification authority.

## 3. PRE: reproduce the actual defect

Before correction, execute the unchanged BASE full POST in three isolated private copies: CLEAN, M1 (measured SHA zeroed), M2 (gate-module SHA zeroed). Use the original normal JSON loader and full battery. Record commands, input/output/harness hashes, exit codes, PA2 case and final aggregator result; preserve stdout/stderr and raw JSON. Expected historical observation: all three QUALIFICATION_PASS/exit0, with 53/53 suite passing. Any unexpected baseline result must be investigated within existing evidence and recorded; do not rewrite PRE to match an expectation.

Mutate only the specified receipt field. The harness, source pins, gate/runner modules and real evidence inputs remain unchanged. Record exact before/after field diffs. Separate PRE reproductions from POST fixtures/results; never overwrite or regenerate PRE after a repair.

## 4. PA2-RC1/P2: new canonical receipt qualification

Implement a small shared validator at QUALIFICATION_CODE_ROOT, used by CANONICAL_POST. Adapt the predecessor POST into the new canonical entrypoint while preserving its original required cases and documented source mapping. Do not merely place a failing side-check next to an overall PASS. Do not change the scanner or frozen original gate. Record the patch/diff from the predecessor and explain changes in imports, output/staging paths and the PA2 acceptance condition.

Required CLI contract for CANONICAL_POST:

```text
node tools/placement_probe/qualification/pa2_r1/run_post.mjs --worktree <isolated-checkout> --runroot <private-case-root> --kitdir <verified-extracted-kit> --receipt <receipt-under-test.json> --out <private-output-dir>
```

Every case must parse --receipt through the SAME normal JSON loader, execute the SAME corrected validator and aggregate the SAME required results. Outputs must stay in --out/private runroot, not alongside historical scripts. Path arguments select files, never the verdict. Persist the actual executed command and module identities.

### 4.1 Exact historical receipt compatibility

The baseline CLEAN receipt is the predecessor's artifact:

```ini
EXPECTED_RECEIPT_RUN_ID = PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011
EXPECTED_RECEIPT_STAGE = PA2_LIVE_IDENTITY_GATE
EXPECTED_RECEIPT_MODE = REAL_SEQUENCE
RECEIPT_CONTEXT_BASE = 28e91eb67511a3022a911ab6d4e02e68119b1f68
```

It has NO top-level schema field and NO perPin inputMatch field. Its actual per-pin representation is pin, compareResult, EXPECTED.sizeBytes/sha256 and MEASURED.exists/sizeBytes/sha256. Validate this exact legacy shape through an explicit trusted format profile; do not require absent fields or the NEW run's RUN_ID. Do not edit or embellish CLEAN to make it pass. Compute per-pin match from evidence. The new validator/output envelope may have its own versioned schema and NEW RUN_ID; keep that metadata separate from the untouched historical receipt.

This is a context-specific requalification of archived evidence, not proof that its old timestamp represents new execution. Validate its run/stage/mode against the frozen predecessor context. Do not impose an arbitrary age limit or claim authenticity from timeUtc. Current physical input remeasurement is a separate result with a current timestamp, command and measured code identity.

### 4.2 Required predicates

1. Verify the trusted BASE gate-module and predecessor-runner SHA against section 1 before loading expected pins. Freeze their 16 expected pin names, sizes and SHA values from that trusted source. Never derive expected values from the tested receipt or observed mutants.
2. Require exactly the expected 16 distinct pin names: no missing/extra/duplicate entry. Require proper object/array/boolean/integer/hash types; do not coerce strings to integers or truthy strings to booleans. SHA comparisons may normalize hex case; never ignore differing bytes.
3. Check receipt EXPECTED against trusted pins; check MEASURED.exists === true and measured size/SHA against the same pins. Independently derive compareResult and match for every pin. Validate compareResult instead of trusting it. Do not require a nonexistent legacy inputMatch field.
4. Recompute total/matched/blockedCount/blockedPins, gate.verdict and EFFECTIVE_GATE_RESULT. Require consistency of all these fields. A PASS needs all 16 matching, zero blocked and an empty blockedPins array. A contradictory summary or per-pin comparison refuses qualification.
5. Validate exact historical runId/stage/mode. Validate both module identity paths, allowing only Windows/POSIX slash normalization, and both recorded SHA values against the trusted source files. No path alias to an unrelated module, no self-authority from receipt-declared hashes.
6. Run the unchanged verifyAllInputs against the 16 original evidence paths and record live remeasurement. The new qualifier requires that current input identity check to pass as well as the receipt validator. A clean live run must not overwrite, replace or repair the supplied receipt-under-test; M1/M2 remain failures even when original files are currently clean.
7. Fail closed on missing/malformed/incomplete/contradictory receipt or wrong context with a controlled PA2 failure and nonzero final exit, preserving diagnostics. Do not turn an exception into an omitted case, default PASS or successful empty result.
8. Missing/FAIL/ERROR/NOT_PERFORMED PA2 makes overall qualification REFUSED. All original required cases remain conjunctive. Only explicitly documented success statuses count; do not accept any arbitrary truthy result.

Record four separate quantities: INPUT_BYTES_REMEASURED, RECEIPT_INTERNAL_CONSISTENCY, MODULE_CODE_IDENTITY, RECEIPT_QUALIFICATION. Source and independence limitations must be explicit. Hash consistency is not historical execution proof, a signature, or proof of authorship. No signing service or universal receipt framework is requested.

## 5. Mandatory full-POST matrix and causality

The following is a fixed integration matrix. Each mutant starts from a fresh exact CLEAN copy and changes only the listed fields. Use the same new full POST entrypoint; freeze its code/pins for a matrix batch. Any repair invalidates that batch and requires the full fixed matrix to be rerun, with old results retained.

| Case | Change | Required PA2 | Required overall | Required exit |
| --- | --- | --- | --- | --- |
| CLEAN | Unmodified archived valid receipt | PASS | QUALIFICATION_PASS | 0 |
| M1 | perPin[0].MEASURED.sha256 = 64 zeroes | FAIL | QUALIFICATION_REFUSED | nonzero |
| M2 | moduleIdentity.gateModule.sha256 = 64 zeroes | FAIL | QUALIFICATION_REFUSED | nonzero |
| M3 | perPin[0].MEASURED.sizeBytes increased by 1 | FAIL | QUALIFICATION_REFUSED | nonzero |
| M4 | perPin[0].compareResult = SHA_MISMATCH while measured bytes still match | FAIL | QUALIFICATION_REFUSED | nonzero |
| M5 | Remove exactly one perPin entry | FAIL | QUALIFICATION_REFUSED | nonzero |
| M6 | Append a duplicate of one perPin entry | FAIL | QUALIFICATION_REFUSED | nonzero |
| M7 | gate.matched = 15 and gate.blockedCount = 1 while all perPin entries match | FAIL | QUALIFICATION_REFUSED | nonzero |
| M8 | moduleIdentity.runner.sha256 = 64 zeroes | FAIL | QUALIFICATION_REFUSED | nonzero |
| M9 | One perPin MEASURED.exists=false, sizeBytes=null, sha256=null and compareResult=MISSING; corresponding blockedCount/blockedPins/matched report that blocked pin, but verdict/effective result still claim PASS | FAIL | QUALIFICATION_REFUSED | nonzero |

M1/M2 must independently demonstrate closure of the Desktop findings. For every M1..M9: record the PA2 refusal reason, actual recomputed values, final qualifier outcome and exit, and confirm other normal required cases still passed. An earlier manifest/file hash failure, missing dependency, unrelated test failure or thrown process startup error is NOT an adequate mutant detection result.

Use bounded unit controls for the validator's header/profile checks: wrong historical runId, wrong stage, wrong mode and an unreadable/truncated JSON receipt. All must yield controlled refusal; CLEAN stays unchanged. These four are unit controls, separately counted from the ten full-POST cases.

Test the ACTUAL aggregator with three mutations of its required PA2 result: missing, FAIL and NOT_PERFORMED. Each must refuse; do not test a hand-copied toy conjunction. Record affected gate, code path and final outcome. Keep these three aggregation controls separate from receipt cases and from test counts.

The integration-matrix driver is outside the canonical POST recursion. CANONICAL_POST must not recursively invoke a test that launches the same full matrix. Retain predecessor cases inside each full POST; run new unit/two-source regressions there or as explicit required conjuncts. Run the full-POST matrix only from its bounded outer driver.

## 6. PA2-RC2/P3: records-only correction

Publish a limited supersession and correct new/current explanatory wording and relevant active test comments/titles:

```ini
PA2_INPUT_COMPARISON = PRESERVED_CONFIRMED
PA2_RUNNER_EXIT3_ON_MISMATCH = PRESERVED_CONFIRMED
HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM = RETRACTED
PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT = NOT_ESTABLISHED
```

The historical callbacks are not reached on clean runs either. Zero counters remain an authentic observation but prove no downstream integration. Do not require additional integration/orchestrator work to close this claim correction. No real ref reservation, analysis or GitHub writes in mutant/control tests. Unchanged historical runner strings such as DOWNSTREAM_AUTHORIZED are legacy labels, not this run's authorization or renewed proof.

## 7. DA2-COV/P3: two contributing sources

Add one permanent regression using the unchanged scanner and synthetic fixtures, matching the externally measured cap32 case. Generate the values through the actual scan, not a fabricated 29+3 array.

```ini
RETAINED_CAP = 32
SOURCE_1_CONTRIBUTION = 29
SOURCE_2_CONTRIBUTION = 3
TOTAL_CANDIDATE_ROWS = 32
PEAK_DISTINCT_CREATION <= 32
PEAK_DISTINCT_FORWARD <= 32
PEAK_DISTINCT_SERIALIZATION <= 32
```

Both input files must be opened and contribute actual output candidates, proved by per-source provenance in the result. Use a bounded identity observer over creation/forward/serialization collections, not just production budget counters. Reusing prior observer patterns is allowed with attribution; it is not a second implementation merely because it was rerun. The observer must not retain extra candidate objects across phases as its own audit roots. Scalar identities/WeakMap are suitable. An alias counts once; an actual copied object counts separately.

Compare four ordinary/instrumented output files byte-for-byte and compare budgets. Record observer code identity. Preserve cap4/cap256 and the existing forced-copy detection control; cap4 still does not prove two contributing sources. If 29+3 cannot be reproduced within the unchanged scanner/configuration, record FAIL rather than changing scanner limits or substituting arithmetic. Commit the regression and evidence, with negative protection against a missing second contribution.

## 8. Budgets, replay and internal QC

Preserve the unchanged scanner's actual per-invocation ceilings:

```ini
syntheticInputs = 32
scannedBytes = 67108864
layoutEvaluations = 100000
fullCensusRows = 50000
retainedCandidates = 256
```

These are execution ceilings, not required targets. Lowered fixture limits are allowed and must be recorded. Never raise a ceiling. Original payload scans, new EXE bodies, Gamebryo/OpenMW/SDK research, runtime, model joins and placement discovery remain zero. Identity hashing of the pinned evidence/ZIP is permitted. Each test invocation gets its documented fixture budget; repeated full POST cases are separately counted, never disguised as one scan.

One initial implementation/evaluation, then at most TWO repair rounds in total. A round is an edit batch responding to recorded failed checks/findings followed by revalidation; count executor and QC-driven repairs in the same ledger. Keep all failed iterations and PRE/POST identities. Do not reset the counter on context changes or label repairs as persistence to evade the cap. No endless fuzzing or automatic search for a passing threshold.

Replay the exact BASE 53 tests from a private byte-identical stage: expected 53/53, exit0. Replay the original seven kit tests from verified ZIP members. Run the new current suite and required qualifier controls, recording generated counts, names, tests vs cases vs outcomes, and exact commands. A PASS from the historical suite does not qualify the corrected receipt validator. Current wording changes must map to preserved original assertions.

Perform fresh-context INTERNAL_QC after executor evidence is frozen. It is internal to this run, not an external Desktop post-audit. QC must independently inspect actual input identities, receipt shape, trusted pin source, code identity checks, the new canonical acceptance/aggregation path, mutation causality, two-source contributions, observer effect, source freeze and manifest scope. Rerunning executor scripts is replay; label additional independently derived checks accurately. If fresh context is unavailable, record NOT_PERFORMED and do not claim full qualification PASS.

Record every finding, actual severity, fix disposition, repair round and raw outcome. Preserve the predecessor closed findings unless a real new counterexample appears; a material unexpected issue outside authorized repair scope remains open, not silently fixed by broader work.

## 9. Required package and qualification gate

At OUTPUT_REPO_PATH publish at least:

```text
CONTRACT.md
PRE/INPUT_IDENTITIES.json
PRE/SOURCE_IDENTITIES.json
PRE/BASELINE_REPRODUCTIONS.json
PRE/RAW/**
POST/RECEIPT_MUTATION_MATRIX.json
POST/FULL_POST_RESULTS.json
POST/AGGREGATOR_CONTROLS.json
POST/VALIDATOR_PROFILE_CONTROLS.json
POST/LIVE_INPUT_REMEASUREMENT.json
POST/TWO_SOURCE_AGGREGATION.json
POST/REGRESSION_RESULTS.json
POST/RAW/**
QC/INTERNAL_REVIEW.md
QC/FINDINGS.json
BUDGET_ACCOUNTING.json
AMENDMENT_LOG.md
SUPERSESSION.md
EVIDENCE_INDEX.md
FINAL_REPORT.md
HANDOFF.md
MANIFEST_SHA256.csv
```

CONTRACT.md is byte-identical to the dispatched contract. Supporting runnable code, tests and matrix driver live in the authorized code/tests roots; link them exactly. Persist small synthetic receipts/builders and raw machine results sufficient for replay, without proprietary game/SDK payload. Do not publish copies of private documents just to satisfy pins. If logs contain secrets, omit/redact only those values with an explicit record; preserve measurements and relevant failures.

Every essential outcome must record MEASURED_QUANTITY, EXPECTED, ACTUAL, UNIT/DENOMINATOR, SOURCE_OF_TRUTH, WHY_NON_CIRCULAR, FAILURE_CASE_DETECTED, RESULT, code/input identities and the command. Generate counts from raw records. Independently recompute totals; do not copy prose counters.

Final QUALIFICATION_PASS requires conjunction of: preflight/source integrity; preserved historical regression; CLEAN PASS; M1..M9 PA2-caused full-POST refusal; four profile unit controls; three actual aggregator controls; cap32 two-source regression; required internal QC; source freeze; no material unresolved P0/P1/P2 in this correction scope. Expected refusals count as control successes, not product failures. A missing required result or unexpected exception blocks PASS. P3 backlog may remain if explicitly nonblocking and adjudicated.

## 10. Persistence and honest negative publication

Separate SCIENCE/TOOLING_QUALIFICATION from SAFE_PUBLICATION. A completed all-pass correction or an honest PARTIAL/REQUIRE_CORRECTIONS after the two repair rounds may be published when ALL safe-publication gates pass: authorized scope, preflight/input identity, valid source/base lineage, no foreign edits, no proprietary original payload, truthful complete evidence, frozen PRE, source preservation, clear open findings, manifest integrity and safe target-ref state. PARTIAL publication MUST NOT mark PA2 closed or authorize a pilot.

A preflight failure has no correction to publish. If an integrity/scope/ref safety gate fails later, stop publication and preserve local evidence with PERSISTENCE_BLOCKED. Never publish an unsafe/misrepresented result just to return a SHA. Do not run a third repair round. Publishable negative tooling outcomes are not, by themselves, integrity failures.

Before staging, freeze final artifact content and generate the manifest LAST. Scope: EVERY changed tracked path relative to EXPECTED_BASE_SHA, including tools/tests, package/CONTRACT and AUDIT_ENTRYPOINT; self-exclude only OUTPUT_REPO_PATH/MANIFEST_SHA256.csv. List exact repository-relative paths, byte sizes and SHA256; include a scope/unit declaration. Full bijection must equal changed paths minus this one manifest. Physical package file count is a different unit; do not force it equal to manifest rows. Reject missing/extra/duplicate/path-escape entries and size/SHA mismatch.

Verify all historical packages and protected source files byte-identical vs BASE. Verify allowlist and entrypoint 1/0. Verify staged blob size/SHA for every manifest row before commit. No .pyc, caches, temp stage files or foreign content. Any in-round artifact change requires final manifest regeneration; no manual hash substitutions.

Immediately before commit/push, fresh-read SOURCE_REF == EXPECTED_BASE_SHA and RESULT_REF == reserved EXPECTED_BASE_SHA; confirm worktree has no unexpected commits. If either guard differs or network prevents verifying them, stop persistence without forcing/rebasing/adapting. Record master separately. Create exactly ONE ordinary commit with sole parent EXPECTED_BASE_SHA. No amend, force push, master merge or history rewrite. Push only the explicit RESULT_REF through normal fast-forward from its BASE reservation.

After commit verify committed blobs against every manifest row, exact changed-path census and one-parent lineage. Then publish and verify LOCAL_HEAD == fresh remote-tracking RESULT_REF == actual live RESULT_REF == RESULTING_SHA. Read back remote file/blob identities and manifest bijection; label any sampling as sampling, not full verification. Record the observed master and confirm this run performed no write to it.

Store post-commit/push command receipts privately under LOCAL_RUN_ROOT, outside the already committed manifest. The committed report may state publication PENDING_AT_COMMIT; terminal handoff supplies actual remote verification. Never amend the commit merely to put its own SHA/remote receipt inside its hash. If commit exists but push/network verification fails, report LOCAL_COMMIT_ONLY or REMOTE_VERIFICATION_PENDING accurately and stop; do not create another commit or pretend PUBLISHED.

## 11. Science ceiling and terminal handoff

```ini
PLACEMENT_DISCOVERY = NOT_EXECUTED
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
GENERAL_TOOL_CORRECTNESS = NOT_ESTABLISHED
PCG_PHYSICAL_PAYLOAD_SCAN = NO
EXE_RE = NO
GAMEBRYO_RE = NO
CANONICAL_GATE_EFFECT = NONE
PILOT_SCAN_AUTHORIZED = NO
NEXT_EXPERIMENT_AUTHORIZED = NO
NEXT_MILESTONE_AUTHORIZED = NO
EXTERNAL_DESKTOP_POST_AUDIT = PENDING
HARD_STOP = YES
```

Return an explicit terminal report with RUN_ID, contract size/SHA, exact BASE, source/result refs, RESULTING_SHA or NOT_CREATED, parent or N/A, local/tracking/live SHA, publication status, canonical POST command, PA2-RC1 disposition, PA2-RC2 supersession, DA2-COV status, CLEAN/M1..M9 outcomes, profile/aggregator controls, exact historical/current test counts and units, cap32 29+3 measurements, repair rounds, internal QC origin/results, open P0/P1/P2/P3, manifest scope/rows/bijection and staged/committed/remote verification, source preservation, changed paths, entrypoint 1/0, private receipt paths, deviations, limitations and science ceiling.

Then HARD STOP. No pilot, new science or self-authorized continuation. The next action is external Desktop review of the exact published SHA and a separate human decision.
