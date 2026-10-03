# HANDOFF — PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003

Single compact handoff to PE-MASTER. Full detail: `FINAL_REPORT.md`.
Raw evidence: `02_RAW_TESTS/` (PRE/POST CLI records),
`03_QC_SELF_CHECK/` (battery + QC re-execution + pre/post non-inspect CLI
snapshots), `04_REGRESSION/` (T1 deep-identity). Identities:
`INPUT_IDENTITIES.md`.

```text
BASE_SHA = ee60930a2b1094588ab3be490eefd3cce291c9d1 (verified: local HEAD
  == local origin/master == actual remote master at run start; re-verified
  before push)
HEAD_SHA = (this run's commit; discover with
  git log -1 -- docs/audits/PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003)
CHANGED_PATHS = tools/gamebryo_oracle/{gb12core.py, oracle.py,
  tests/test_gb12.py, schemas/oracle_result.schema.json, README.md} (5
  files; ONLY ONE removed logic line in gb12core.py — the pre-F2
  false-success predicate; everything else additions) + the new package
  docs/audits/PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003/
  + one AUDIT_ENTRYPOINT.md row
PACKAGE = docs/audits/PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003/
F2_VERDICT = FIXED_AND_VERIFIED (both false-success classes reproduced
  PRE-FIX on OUR OWN fixtures on BASE and rejected POST-FIX)

REGISTERED_BUT_NOT_DECODED PRE -> POST:
  PRE  = accepted=true / partial=false / CLI inspect exit 0, 3/3 slots
         non-NULL incl. the NiCamera boundary-only placeholder (raw:
         PRE_FIX_REGNOTDEC_A_*.RECORD.json)
  POST = accepted=false / exit 2; SOURCE=UNRESOLVED; COVERAGE=INCOMPLETE
         (counters 3 hdr / 2 semantic / 1 boundary / 1 registered-not-
         decoded / classes=[NiCamera]); INTEGRITY=UNRESOLVED (links 2/3
         measured); TOOL=UNRESOLVED (never PASS)
  factory_registration = YES (independent registry census: NiCamera in
  the 198 classes, absent from the 39 LOADERS — re-verified in-run)
  source-predicted verdict for A = UNRESOLVED (registered != original
  rejection; no new broad source RE done to reach ACCEPTED)

INVALID_LINK PRE -> POST:
  PRE  = accepted=true / exit 0, LINK_FAILURE warning only, children
         resolved ["LINK_ERROR_OUT_OF_RANGE"] (raw:
         PRE_FIX_INVALID_LINK_B_*.RECORD.json)
  POST = accepted=false / exit 2; COVERAGE=COMPLETE; LINK_INTEGRITY=FAIL
         (link_failure_count=1); ADAPTER_INTEGRITY=FAIL; TOOL=FAIL (never
         UNRESOLVED for a known detected invalid link)
  source-predicted verdict for B = UNRESOLVED (pinned proof: NiStream.cpp
  L245-256 DEBUG-only assert + NiTArray.inl L136-139 unchecked raw GetAt +
  LinkObject void/discarded at LoadStream L576 + unconditional return
  true L634 -> debug/release dependent, no unambiguous propagated
  rejection)

VALID_POSITIVE = PASS (fx_VALID: COMPLETE / PASS / TOOL PASS / accepted
  true / exit 0; byte-identical to the F1 battery fixture A; additionally
  a valid 2-node scene with a real in-range link also reaches TOOL PASS)

ADAPTER_COVERAGE_RESULT = axis implemented with measurable counters
  (integer when measured, null + explicit per-counter reason otherwise;
  measured ZERO never substitutes unknown); early RTTI halts (ordinary
  + F1-C1 STOP_AT_TABLE_FAILURE) leave object-level counters NOT_MEASURED
  (never derived from RTTI table names)
ADAPTER_INTEGRITY_RESULT = axis implemented (object-count consistency +
  structural closure + link integrity); out-of-range link => FAIL =>
  TOOL FAIL unconditionally
TOOL_VERDICT + INSPECT_CLI_EXITS:
  fx_VALID exit 0 (PASS); REGNOTDEC exit 2 (UNRESOLVED); INVALID_LINK
  exit 2 (FAIL); C1A/C1B exit 2 (FAIL); T1 ordinary+full exit 2 (FAIL);
  for every re-executed record: exit==0 <=> TOOL_VERDICT==PASS
COVERAGE_ZERO_VS_NOT_MEASURED = distinct (measured zeros are int 0;
  unknown counters are None with reasons; QC-checked)
NON_INSPECT_CLI_REGRESSION = NONE (probe-version / capabilities all+gb12 /
  compare pinned-pair + internal-inspect-pair: byte-identical outputs
  pre/post; compare/probe logic files untouched; gb26/gb112/gb23 inspect
  keep accepted-based exits — verified gb26 exit 2 unchanged)
F1_F1C1_REGRESSION = PASS (full battery 42 checks 0 failures: 11 self +
  8 F1 + 11 F1-C1 + 12 new F2; C1A 94B/928A1447... and C1B
  196B/719A7EB3... byte-regenerated pinned fixtures both PASS with
  STOP_AT_TABLE_FAILURE + earlier RTTIError + objects=[] + exit 2
  preserved; payload battery: the 2 PRE-EXISTING control failures
  identical pre/post)
T1_66_RECORD_DEEP_REGRESSION = PASS (identity re-verified 57316 B /
  3E8A22C2...; objects[] 66/66 DEEP-IDENTICAL vs the ee60930 baseline;
  whole-JSON delta = exactly the 9 new F2 metadata keys; 62 semantic +
  4 opaque/boundary-only NOT promoted; FIRST_RTTI_MISS=
  NiArkAnimationExtraData@1 + SOURCE_PREDICTED=REJECTED preserved;
  TOOL != PASS; WORLD_PLACEMENT_RECOVERED=NO; run1==run2)
QC_VERDICT = SELF_CHECK_QC_PASS (SELF_CHECK_F2 scope: 22/22 QC
  re-execution checks incl. the mandatory set VALID_SUPPORTED /
  REGISTERED_BUT_NOT_DECODED / INVALID_LINK / C1A / C1B with input
  identity, command, stdout, stderr, exit; NO independent reviewer — not
  claimed as independent QC)
PERSISTENCE = path-limited commit of the 5 tool files + the new package +
  the AUDIT_ENTRYPOINT row; fast-forward push after re-verifying actual
  remote master == ee60930a...; post-push fetch + identity re-measurement
  recorded below in PUBLICATION STATUS
REMAINING_BACKLOG = F3 (compare same-input/comparison validity), F4
  (structured exception result + presolver trailing-run IndexError),
  F5 (historical report wording beyond F2 metadata), F6 (process ledger),
  F7 (HUMAN ORDER verbatim), O1 (float bit-exact vs == policy), T3
  (solver completion) — ALL untouched this run
DEVIATIONS = none from the assigned contract. In-run notes: the OPTIONAL
  OBJECT-COUNT CONTROL was not separately exercised (no small fixture
  reaches it without other failure classes; wiring in place; run not
  expanded per contract). One run-tooling fix (run_test.py cross-drive
  relpath) was made in OUR OWN package runner before any base-code
  change; no PRE-FIX measurement depended on it. One out-of-scope
  OBSERVATION recorded (original user-version gate [0.0.0.0, 0.0.0.0]
  not implemented in the adapter — NOT fixed, era-labelled).

QC_SCOPE = SELF_CHECK_F2
GENERAL_ORACLE_FAIL_CLOSED = ESTABLISHED_FOR_F1_F2_SCOPE_ONLY
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
CANONICAL_GATE_EFFECT = NONE
T3_COMPLETION_EXECUTED = NO
NEW_PCG_TRACE_EXECUTED = NO
WORLD_PLACEMENT_RECOVERED = NO
NEXT_RUN_EXECUTED = NO
HARD_STOP = YES (no F3/F4 started, no placement RE, no PCG client, no
  milestone changes)
```
