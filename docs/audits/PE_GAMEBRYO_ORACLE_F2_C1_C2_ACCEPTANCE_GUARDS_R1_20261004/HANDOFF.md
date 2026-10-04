# HANDOFF — PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004

Compact handoff to PE-MASTER. Verdict: **FIXED_AND_VERIFIED** for the two
bounded findings F2-C1 and F2-C2 (SELF_CHECK_F2_C1_C2 executor QC;
advisory; awaiting PE-MASTER/external audit). Publication performed under
the standing explicit publication assignment in the dispatch contract;
actual remote master re-verified == d497b44d... immediately before the
push (no PERSISTENCE_BLOCKED).

## Result summary

- BASE_SHA = d497b44d85570b8bf94153ba0c08634d0992b302 (HEAD == local
  origin/master == actual remote master, verified at start and again
  immediately before the push).
- F2-C1 (user-defined version gate): FIXED_AND_VERIFIED — a source-proven
  invalid user-defined version (nonzero; gate [0.0.0.0, 0.0.0.0],
  NiStream.cpp L46-50/L334-352) now ends SOURCE_PREDICTED=REJECTED +
  TOOL_VERDICT=FAIL + accepted=false + inspect exit != 0 in BOTH ordinary
  and --full-decode, with NOT_MEASURED coverage/integrity and null
  object-level counters with explicit reasons (the rejection precedes the
  uiObjects read L355-357; --full-decode cannot bypass a source-proven
  LoadHeader rejection). The valid user-version-0 positive control stays
  PASS/exit 0 (no over-fail-closed).
- F2-C2 (top-level root link integrity): FIXED_AND_VERIFIED — parsed
  top-level root IDs participate in overall link-integrity with RAW
  provenance preserved (scene_graph.roots) + u32 normalization; measured
  fields top_level_root_link_integrity / _failure_count / _checked_count /
  _raw / _normalized_u32 inside adapter_integrity_checks; root 9999 and
  root 0xFFFFFFFE (raw -2) => TOP_ROOT=FAIL => LINK_INTEGRITY=FAIL =>
  ADAPTER_INTEGRITY=FAIL => TOOL=FAIL + exit != 0 in BOTH modes; SOURCE
  stays UNRESOLVED (never auto-REJECTED); root 0xFFFFFFFF (raw -1, the
  source NULL_LINKID sentinel) is NOT an out-of-range failure (verified by
  fixture execution); root 0 stays PASS.
- Mandatory wording fix applied: SOURCE=ACCEPTED reasons now cite the
  MEASURED root/user-version-gate evidence and cannot claim
  "LoadTopLevelObjects in range" / "every link NULL or in range" / complete
  LoadHeader content-validity unless actually measured/checked.
- PRE-fix defects reproduced on pristine BASE raw CLI records (captured
  BEFORE any code change): C1 and root-9999 fixtures are byte-identical to
  the Desktop auditor's independent fixtures (C643F2D2... / D0E2A035...).
- Regressions: F1/F1-C1 PRESERVED (battery 42 historical checks all still
  PASS, POST 59/0; C1A/C1B STOP_AT_TABLE_FAILURE + earlier RTTIError +
  NOT_MEASURED counters + exit 2 preserved in both modes); original F2
  cases PRESERVED_FIXED (REGNOTDEC UNRESOLVED/INCOMPLETE/UNRESOLVED/exit 2;
  INVALID_LINK UNRESOLVED/COMPLETE/FAIL/FAIL/exit 2; VALID PASS/exit 0);
  T1 66/66 objects[] deep-identical vs two independent d497b44 baselines,
  62 semantic + 4 boundary NOT promoted, FIRST_RTTI_MISS=
  NiArkAnimationExtraData@1 + SOURCE=REJECTED + TOOL=FAIL preserved;
  whole-JSON delta confined to the F2-C1/C2 metadata keys; non-inspect CLI
  (probe-version/compare/capabilities) byte-identical pre/post on all 5
  pairs; payload battery 2 pre-existing placeholder-control failures
  identical pre/post (documented, NOT fixed — out of scope).

## Evidence map (all inside the package)

| what | where |
|---|---|
| Terminal verdicts + full result tables | FINAL_REPORT.md |
| Fixture + source + T1 identities | INPUT_IDENTITIES.md |
| Deterministic fixture generator (byte-regeneration source) | 01_FIXTURES/build_fixtures_f2c1c2.py |
| 16 PRE-fix + 20 POST-fix raw CLI records (identity/command/stdout/stderr/exit) | 02_RAW_TESTS/*.RECORD.json (+ run_test.py runner) |
| QC matrix re-execution (58/58 PASS) + raw QC record set | 03_QC_SELF_CHECK/qc_reexecution.py, qc_reexecution.stdout, QC_REEXECUTION_GUARDS.json |
| Non-inspect CLI byte-identity (5 pairs) | 03_QC_SELF_CHECK/qc_noninspect_cli.py + noninspect_records/*.json |
| Battery pre/post outputs | 03_QC_SELF_CHECK/PRE_FIX_*battery*.stdout / POST_FIX_*battery*.stdout |
| T1 deep-identity regression (two baselines) | 04_REGRESSION/t1_deep_regression.py + T1_REGRESSION_FINAL.stdout |
| Committed-package manifest (header row) | COMMITTED_PACKAGE_MANIFEST_SHA256.csv |

Tool changes: `tools/gamebryo_oracle/gb12core.py` (C1 gate + C2 root
validation + verdict/reason corrections), `schemas/oracle_result.schema.json`
(user_version_gate, user_defined_version_u32, top_level_root_* docs),
`tests/test_gb12.py` (new F2-C1/C2 battery, 17 checks), `README.md`
(guard documentation). Historical packages F1 / F1-C1 / F2 untouched.

## Remaining backlog (unchanged)

F3 (compare validity), F4 (presolver), F5-F7, O1, T3 completion — NOT
addressed. GENERAL_ORACLE_FAIL_CLOSED and GENERAL_SOURCE_EQUIVALENCE
remain NOT_ESTABLISHED. No milestone change; no new PCG trace;
WORLD_PLACEMENT_RECOVERED = NO.

## Next recommended action

PE-MASTER audit of the pushed commit (focused external Desktop post-audit
of this exact SHA recommended), then the F3-F7 backlog per the standing
order. NEXT_RUN_EXECUTED = NO (HARD STOP honored).
