# HANDOFF — PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003 -> PE-MASTER

```text
BASE_SHA     = abc3f8f6f9e35dd8aebbe2cfe525d710e4338acd (verified: local HEAD = local origin/master = actual remote master at dispatch)
HEAD_SHA     = <discoverable via git log -1 -- docs/audits/PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003; the base was NOT changed by third parties — re-verified before push>
PACKAGE      = docs/audits/PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003/
RUN_STATUS   = COMPLETED (F1 scope closed; bounded; hard stop after this handoff)
```

## Verdicts

```text
F1_RTTI_TABLE_SOURCE_ORDER = FIXED_AND_VERIFIED
F2_TO_F7                   = NOT_ADDRESSED_IN_THIS_RUN
QC_SCOPE                   = SELF_CHECK_F1
QC_VERDICT                 = SELF_CHECK_QC_PASS_WITH_FINDINGS
GENERAL_ORACLE_FAIL_CLOSED = NOT_ESTABLISHED
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
T3_COMPLETION_EXECUTED     = NO
NEW_PCG_TRACE_EXECUTED    = NO
WORLD_PLACEMENT_RECOVERED  = NO
CANONICAL_GATE_EFFECT      = NONE
NEXT_RUN_EXECUTED          = NO
PLACEMENT_CONTEXT_IMPORT   = NOT_USED (optional import not exercised; nothing from the R2 placement research is transferred)
PERSISTENCE                = path-limited commit + fast-forward push (details below)
```

## Changed paths (complete change set)

- `tools/gamebryo_oracle/gb12core.py` — the F1 fix: source-order RTTI table
  scan (name -> factory check -> next name; first unregistered entry =
  fail-closed verdict before any later name / any object index / groups /
  bodies); unused entries validated; RTTI_TABLE_VALIDATION separated from
  OBJECT_REFERENCE_HISTOGRAM/CENSUS; --full-decode keeps
  SOURCE_PREDICTED_VERDICT=REJECTED + table-order FIRST_RTTI_MISS, labels
  the extension, never masks the source verdict on extension failure; doc
  blocks updated. Legacy < 5.0.0.1 inline-RTTI layout NOT migrated.
- `tools/gamebryo_oracle/schemas/oracle_result.schema.json` — three new
  optional keys (rtti_table_validation, object_reference_histogram,
  object_reference_census).
- `tools/gamebryo_oracle/tests/test_gb12.py` — permanent F1 regression
  battery (8 controls, s18 discipline).
- `tools/gamebryo_oracle/README.md` — F1 section + --full-decode/Tests/
  Schemas honesty updates.
- `AUDIT_ENTRYPOINT.md` — one honest F1 row.
- `docs/audits/PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003/` — this
  package (fixtures, raw before/after/QC records, derivation, reports,
  manifest).

Registry `adapters/gb12/registry.py`: UNCHANGED. Foreign untracked paths:
untouched. No SDK or proprietary game payload committed (fixtures are our
own synthetic bytes; REPO POLICY: the six synthetic .nif fixtures are NOT
committed — the repo-wide `*.nif` gitignore keeps zero NIF files tracked,
matching the published run's convention; the committed
`01_FIXTURES/build_fixtures.py` regenerates them byte-identically, SHA
pins in INPUT_IDENTITIES.md; physical copies at
`D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003\sandbox\01_FIXTURES\`).
The T1 payload was only READ from the published run's sandbox and its
identity is recorded by hash, never copied into the repo.

## Evidence spine

- Independent pre-fix derivation: `04_ANALYSIS/SOURCE_ORDER_DERIVATION.md`
- Pre-fix counterexample reproduction (the Desktop bug, pinned code):
  `02_RAW_TESTS/BEFORE_FIX_*.RECORD.json` (B: accepted=true,
  unregistered_types=[], exit 0)
- Post-fix mandatory tests A-G: `02_RAW_TESTS/AFTER_FIX_*.RECORD.json`
- QC re-execution of the counterexamples (final code):
  `03_QC_SELF_CHECK/QC_REEXECUTION_COUNTEREXAMPLES.json`
- Full battery outputs: `03_QC_SELF_CHECK/FINAL_self_and_f1_battery.stdout`
  (0 failures), `03_QC_SELF_CHECK/FINAL_payload_battery_T1_copy.stdout`
  (2 PRE-EXISTING failures, identical under the pre-fix code)
- T1 regression: 66/66 objects deep-identical vs the published artifact;
  only the F1-justified metadata changed (FINAL_REPORT §6)

## Remaining F2-F7 backlog (all still OPEN, untouched by this run)

- F2/P1 — accepted/partial/exit ignore coverage and link failures (the
  counterexamples registered_unsupported_class + known_node_invalid_child
  still produce accepted=true; G-TOOL-3 PASS and general fail-closed PASS
  remain retracted).
- F3/P2 — compare does not enforce input identity or comparison validity.
- F4/P2 — structured exception result not guaranteed (truncated header
  traceback; presolver index boundary). NEW PRECISION FROM THIS RUN: the
  presolver crash is localized to `presolve_runs`/`assemble` ->
  `decode_block_at(b, run_end)` with `run_end == n_obj` when the LAST
  unknown run extends to EOF (minimal regression input preserved in the
  package: `01_FIXTURES/fx_C1_trailing_unknown_run.nif`, SHA
  F9BFA6A6...; exits 1 both pre- and post-F1-fix; the E3 fixture with a
  single registered-but-unsupported block reproduces the same class).
- F5/P2 — report claim-matrix wording (REJECTED-at-original-execution,
  66/66 boundaries, placement-in-file categorical) — report-layer wording
  in the PREVIOUS run's package; this run's own package wording is
  SOURCE_PREDICTED-only.
- F6/P2 — process ledger underestimates executions / dispatch-session
  confusion.
- F7/P2 — HUMAN ORDER VERBATIM mismatch vs the recorded human message.
- O1/P3 — comparator float policy (bit-exact claim vs `==` on +0.0/-0.0).

## Notes for the next correction cycle (proposals only — NOT executed)

- F2 is the natural next focused scope (acceptance/coverage/link
  predicate + the two pre-existing battery controls that can only fire on
  registered-class payloads: `object_count_mismatch_detected`,
  `link_failure_detected` — their failure on RTTI-failing payloads is
  expected behavior under the fixed F1 semantics and needs a
  battery-expectation update, which is F2-adjacent and was NOT done here).
- F4 can reuse `fx_C1_trailing_unknown_run.nif` as the minimal
  presolver-boundary regression case (external sandbox copy +
  byte-regenerable via the committed `01_FIXTURES/build_fixtures.py`;
  SHA pin F9BFA6A6227F78E027B34EA7D3D89FA52FBBEDC9DF6A369BD7FED40301952F0E).
- The F1 fix does NOT change the T1-T5 published byte values (66/66
  deep-identical); any future re-baselining of oracle artifacts must
  account only for the metadata deltas in FINAL_REPORT §6.
