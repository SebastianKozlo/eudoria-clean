# HANDOFF — PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011

Terminal handoff of the executor to PE-MASTER (persistence is a SEPARATE LATER phase
performed by pe-master-auditor after the PE-MASTER master audit; this run froze the
final artifact content and generated MANIFEST_SHA256.csv content but committed nothing).

```ini
RUN_ID = PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
RUN_CLASS = SUPPORTING
RUN_TYPE = BOUNDED_CORRECTION_ONLY
CONTRACT_SIZE_BYTES = 29207
CONTRACT_SHA256 = 6E4B0B029DBD082451A6F0E432AA66124FCC5E3299260AC3E330A59DED4F4E23
EXPECTED_BASE_SHA = 28e91eb67511a3022a911ab6d4e02e68119b1f68
SOURCE_REF = refs/heads/research/pe935-placement-probe-census-postaudit-r1-20261011 (== BASE, local+remote verified)
RESULT_REF = refs/heads/research/pe935-placement-pa2-qualification-correction-r1-20261011 (local create-only at BASE, reserved before dispatch; ABSENT on remote; NO push performed)
OBSERVED_MASTER = 3fbe93eec04759395223e6677b5040273d29222a (separate; NOT modified; NO write performed to master)
RESULTING_SHA = NOT_CREATED (no commit/push performed by the executor; persistence is the separate later phase)
WORKTREE = D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011\workspace\eudoria-clean (HEAD = BASE, branch = RESULT_REF)
LOCAL_RUN_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
OUTPUT_REPO_PATH = docs/audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
PUBLICATION_STATUS = PUBLICATION_PENDING (content frozen; MANIFEST_SHA256.csv generated uncommitted)
```

## Canonical POST command (the exact executed form)

node tools/placement_probe/qualification/pa2_r1/run_post.mjs
  --worktree D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011\workspace\eudoria-clean
  --runroot <private-case-root> --kitdir <verified-extracted-kit>
  --receipt <receipt-under-test.json> --out <private-output-dir>

Matrix driver (outer, bounded; never invoked by the canonical POST):
node tools/placement_probe/qualification/pa2_r1/run_matrix.mjs

## Dispositions

- PA2-RC1/P2: CLOSED_FOR_AUDITED_STATE_IN_EXAMINED_CASES — the canonical POST refuses
  every inconsistent identity receipt (CLEAN PASS/0; M1..M9 FAIL/QUALIFICATION_REFUSED/4;
  4 profile unit controls + 3 actual aggregator controls all refuse; PRE reproduced the
  original false-PASS on the unchanged BASE POST before correction).
- PA2-RC2/P3: records-only supersession PUBLISHED (see SUPERSESSION.md):
  PA2_INPUT_COMPARISON=PRESERVED_CONFIRMED; PA2_RUNNER_EXIT3_ON_MISMATCH=PRESERVED_CONFIRMED;
  HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM=RETRACTED;
  PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT=NOT_ESTABLISHED.
- DA2-COV/P3: CLOSED as a permanent regression — cap32 29+3 through the actual scan,
  peaks 29/32/32, both inputs opened, negative protection (cap29 second-input-never-opened
  control), observer stores only scalar identities.

## Counts (units explicit)

- PRE: 3 full-POST executions of the unchanged BASE harness (CLEAN/M1/M2 all
  QUALIFICATION_PASS/exit0 — the defect; suite 53/53 each).
- Full-POST matrix: 10 cases (1 CLEAN + 9 mutants), each a complete battery;
  suite 64/64 in every case; all CONTROL_SUCCESS (batch 3, frozen identity, freezeOk=true).
- Unit profile controls: 4 (+ CLEAN-unchanged control) — separately counted.
- Aggregator controls: 3 — separate from receipt cases and test counts.
- Tests: BASE 53/53 replay (10 BASE files, exact); original kit 7/7 (verified ZIP
  members); current suite 64/64 = 53 BASE + 9 PA2-RQ + 2 DA2-COV.
- Repair rounds against the tool after its first green suite: 0/2 (harness bring-up
  iterations disclosed and classified in AMENDMENT_LOG.md).

## Open findings

- P3 SELF-QC-F2: FRESH_CONTEXT_INTERNAL_QC NOT_PERFORMED_IN_EXECUTOR_SESSION — assigned
  to the separate later pe-master-auditor pass; the executor does NOT claim the full
  §9 QUALIFICATION_PASS conjunction (technical gates PASS; full qualification withheld
  pending that pass).
- P3 SELF-QC-F3: frozen verify_inputs.mjs legacy "spy" wording (protected file) —
  superseded by SUPERSESSION.md.
- P3 SELF-QC-F4: pre-existing BASE accounting limitation (containerReadBytes before
  RAW refusal) — preserved, out of scope.
- No P0/P1/P2 open in this correction scope. Predecessor closed findings preserved.

## Manifest scope (content generated, uncommitted)

MANIFEST_SHA256.csv covers EVERY changed tracked path vs EXPECTED_BASE_SHA (code +
tests + this package + AUDIT_ENTRYPOINT.md), self-excluding only
OUTPUT_REPO_PATH/MANIFEST_SHA256.csv; bijection = changed paths minus this one manifest;
physical package file count is a different unit. Generated LAST from the final artifact
content; not committed by the executor.

## Private receipts (LOCAL_RUN_ROOT layout, paths only)

- pre\ : PRE defect reproduction (case_clean, case_m1_measured_sha_zeroed,
  case_m2_gate_module_sha_zeroed; private harness copies + runroots) + PRE_REPRODUCTIONS.json
- stage_kit\ : verified extracted kit (ZIP pin verified; FILE_HASHES 7/7)
- matrix\receipts\ : receipts-under-test (CLEAN, M1..M9, unit controls, CLEAN_control)
- matrix\case_*\ : per-case runroots + out dirs + stdout/stderr
- posts\ : driver raw results (matrix/profile/aggregator/two_source) +
  batch1_crashed_partial\
- qc\ : executor-self-QC probes + QC_PROBE_RESULTS.json
- scratch\ : throwaway cap32 hypothesis probe
- workspace\eudoria-clean : the isolated worktree (HEAD=BASE, branch=RESULT_REF)

## Deviations from the contract

None material. Recorded notes: (1) the contract's "fresh-context internal QC" is
reassigned by the governing human dispatch to a separate later pe-master-auditor pass;
recorded NOT_PERFORMED_IN_EXECUTOR_SESSION with the full qualification honestly withheld
(not claimed). (2) Matrix batch 1 was invalidated by a driver result-extraction crash and
fully rerun (batches 2/3; chronology and both round-classification readings in
AMENDMENT_LOG.md). (3) The staged BASE 53 replay uses the 10 BASE test files as they
stand in the worktree, of which pa2_identity_gate.test.mjs carries only the §6-authorized
comment/assert-message corrections (recorded diff; 53/53 still passing; 9/10 files
byte-identical to BASE).

Then HARD STOP. No pilot, new science or self-authorized continuation. The next action is
the PE-MASTER master audit, the fresh-context internal QC pass, external Desktop review
of the exact published SHA, and a separate human decision.
