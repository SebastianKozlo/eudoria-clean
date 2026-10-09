# HANDOFF — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Contract §13 terminal handoff, populated from REAL measurements. If a check
had not passed, its actual result would be reported here instead of the
expected value.

```
RUN_ID = PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009
BASE_SHA = 34fc34749464de3e05527088ed46be9e215f1964
RESULTING_SHA = recorded at the terminal handoff per contract §12 — not embedded in this commit's files
REMOTE_SHA = recorded at the terminal handoff per contract §12 — not embedded in this commit's files

PRE_EXECUTOR_FALSE_PASS_REPRODUCED = TRUE
PRE_QC_FALSE_PASS_REPRODUCED = TRUE

POST_CH_PARENT = ECX
POST_EXECUTOR_CH_CLOBBER_DETECTED = TRUE
POST_QC_CH_CLOBBER_DETECTED = TRUE

POST_CH_PROVENANCE_GATE = FAIL
POST_CL_PROVENANCE_GATE = FAIL

CLEAN_PROVENANCE_GATE = PASS

BYTE_ALIAS_MATRIX = 8x8 complete
ALIAS_CASES_PER_DECODER = 64
ALIAS_DECODER_OUTCOMES = 128/128 PASS
DESTINATION_ALIAS_COVERAGE = 8/8
SOURCE_ALIAS_COVERAGE = 8/8
UNRELATED_PARENT_NEGATIVE_CONTROLS = 6/6 PASS
REGRESSION_VERDICT = PASS

QC_VERDICT = QC_PASS
CORRECTION_VERDICT = PASS
MANIFEST_BIJECTION = PASS (measured)
SOURCE_PACKAGE_UNCHANGED = YES

NEW_P0_P1_P2 = 0
UNRESOLVED_FINDINGS = the disclosed process items (non-material: 3 executor process repairs + 5 QC own-tooling bring-up steps + 1 key-name cosmetics note in QC_RESULTS.json, all adjudicated/disclosed, none altering any measured value) + DOC-1/DOC-2 P3 backlog
DOCUMENTARY_BACKLOG = DOC-1/P3, DOC-2/P3

CORE_RECEIVER_VALUE_CHAIN =
  PRESERVED_CONFIRMED_STATIC_CONDITIONAL

FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO

CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Value provenance (each terminal value -> its evidence)

- `PRE_EXECUTOR_FALSE_PASS_REPRODUCED = TRUE` / `PRE_QC_FALSE_PASS_REPRODUCED = TRUE`: `00_PRE/PRE_COUNTEREXAMPLES.json` (both historical decoders AST-extracted, top-level never executed; CH mutant 88 DD @0x0085B24D → writes ["ebp"], verbatim historical ECX scan [] — false empty in BOTH); independently re-measured field-by-field by the QC (`QC_RESULTS.json` duty A).
- `POST_CH_PARENT = ECX`: `00_POST/POST_COUNTEREXAMPLES.json` C2 (dst ch, writes ['ecx'], bits [8,16)); QC duty C agrees; PE-MASTER own execution counter-check agrees.
- `POST_EXECUTOR_CH_CLOBBER_DETECTED = TRUE` / `POST_QC_CH_CLOBBER_DETECTED = TRUE`: POST C2 scan DETECTED @0x0085B24D (executor decoder); QC duty C own decoder DETECTED @0x0085B24D.
- `POST_CH_PROVENANCE_GATE = FAIL` / `POST_CL_PROVENANCE_GATE = FAIL`: gate failure_reasons exactly ['ECX_REACHING_DEF_BROKEN'] in both cases, both implementations — every pin, the rel32 recomputation and the accessor check still PASS on the mutants (the same production predicate as clean; no hard-coded assertion; single-cause decomposition recorded).
- `CLEAN_PROVENANCE_GATE = PASS`: POST C1 (64 insns; end exact 0x0085B290; D9 E8 @0x0085B24D; scan []; CORE_VALUE_SOURCE=[arg1+8]); QC duty B agrees; PE-MASTER counter-check agrees.
- `BYTE_ALIAS_MATRIX = 8x8 complete` / `ALIAS_CASES_PER_DECODER = 64` / `ALIAS_DECODER_OUTCOMES = 128/128 PASS` / `DESTINATION_ALIAS_COVERAGE = 8/8` / `SOURCE_ALIAS_COVERAGE = 8/8`: POST C4 (executor 64/64 vs the independent REF_BYTE8 table) + QC duty E (own decoder + own explicit reference table, 64/64) = 128 decoder outcomes, all PASS; each alias exercised as destination AND as source; 2-byte register-direct cases; partial-write-vs-full-32-bit distinction preserved.
- `UNRELATED_PARENT_NEGATIVE_CONTROLS = 6/6 PASS`: POST C5.1–C5.4 (88 DF→EBX; 88 DC→EAX; 88 CE→EDX; 88 FF→EBX) + QC's own 88 D4→EAX, 88 FB→EBX — correct parents, ECX scans [], gates PASS.
- `REGRESSION_VERDICT = PASS`: `REGRESSION_RESULTS.json` (23/23 pins; rel32 → 0x0085B1B0 / 0x00746560; both RTTI identities; 64-insn clean decode + exact boundary 0x0085B290; field-level equality with the re-executed historical decoder on all 64 instructions; CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL; c6_verdict = PASS); QC duty G re-measured everything independently.
- `QC_VERDICT = QC_PASS`: `QC_RESULTS.json` / `QC_REPORT.md` — 11/11 acceptance gates with the QC's own measurements; QC_ORIGIN = pe-master-auditor fresh-context internal QC, internal to PE-MASTER (NOT an independent Desktop post-audit, NOT executor self-review).
- `CORRECTION_VERDICT = PASS`: all 11 contract §11 acceptance gates hold (see FINAL_REPORT.md section 10; PE_MASTER_REVIEW.md).
- `MANIFEST_BIJECTION = PASS (measured)`: `MANIFEST_SHA256.csv` generated LAST over the final persistence scope (every physical file under this package except the manifest itself + the updated AUDIT_ENTRYPOINT.md; repo-relative; measured census 22 physical package files → 21 package rows + 1 entrypoint row = 22 rows; zero missing/extra/duplicate/size/SHA mismatches; LF, UTF-8 no BOM, lowercase hex).
- `SOURCE_PACKAGE_UNCHANGED = YES`: all four mandatory source inputs + contextual inputs re-hashed unchanged after the correction work (`00_POST/POST_COUNTEREXAMPLES.json` `source_package_unchanged` all true; QC own re-hash + `git diff HEAD` over the source package empty); re-verified at persistence by `git diff 34fc347 -- <historical packages>` (empty).
- `NEW_P0_P1_P2 = 0`: no material finding against the correction; the process disclosures were adjudicated (5 QC own-tooling bring-up steps: NOT a QC_REPAIR_ROUNDS violation — no correction defect was found or repaired; 3 executor process repairs: HONEST).
- Standing: carried VERBATIM, not re-derived (`SUPERSESSION_AND_STANDING.md` section 4; `REGRESSION_RESULTS.json` `j3_statuses_carried_verbatim`): PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED; NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE; ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL; WORLD_XYZ_RECOVERED = NO. No J3 restoration.
- `CANONICAL_GATE_EFFECT = NONE` / `NEXT_EXPERIMENT_AUTHORIZED = NO` / `HARD_STOP = YES`: PE-MASTER advisory standing (ADVISORY_PRE_QUALIFICATION; PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED); no new experiment is authorized by this correction run.

## Persistence facts (this phase)

- Persistence scope: OUTPUT_ROOT (`docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/`) + ONE new newest-first LATEST RUNS row in `AUDIT_ENTRYPOINT.md` (no other row modified — the source run's science claims stand; C6 regression preserves them; CMO-C1 is machinery-level and carried by the new row + this package's SUPERSESSION_AND_STANDING.md).
- Changed-path census of the commit: 23 paths expected (22 package files incl. the manifest + AUDIT_ENTRYPOINT.md); measured at staging.
- Allowlist gates: git status/diff limited to OUTPUT_ROOT/** + AUDIT_ENTRYPOINT.md; no proprietary payload (no EXE bytes); no residue (python -B; no __pycache__/.pyc); SOURCE_PACKAGES and all historical packages unchanged; LOCAL_HEAD == origin/master == actual remote master == 34fc347… re-verified live immediately before commit; one normal fast-forward commit + push (no amend/rebase/force).
- Per contract §12: a push/remote-verification failure would be a persistence failure, not a scientific PASS — the actual local/remote status would be preserved and the run would stop without a follow-up run.
- SOURCE_DESKTOP_POST_AUDIT (CMO provenance run) = PERFORMED (the CMO-C1 finding's origin); NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED (pending the external Desktop post-audit of the exact published SHA, if the human orders one).

**WORKS != UNDERSTOOD. STOP BEFORE SCOPE EXCEED. ONE CORRECTION RUN ONLY.**
