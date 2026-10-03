# CORRECTION BUDGET (PREREGISTRATION) — PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

PREREGISTERED 2026-10-03T09:16:45Z (UTC) BEFORE ANY CORRECTION EDIT, CORRECTION MEASUREMENT, OR SOURCE VERIFICATION. Written by the formalizer (pe-master-auditor) in PHASE A, dispatched by PE-MASTER, before the executor phase. Any later change to these numbers is a budget-discipline violation (NO SILENT BUDGET EXPANSION).

Timestamp note (honest provenance): 2026-10-03T09:16:45Z is the timestamp of the last verified tool measurement immediately preceding this file's write (the AUTHORIZATION.md byte-identity verification, recorded in 00_CONTROL/PREFLIGHT.md section 7). No correction edit, correction measurement or source verification has occurred at any point up to and including this write.

## 1. New budgets — status

```text
NEW_CORRECTION_CYCLE_BUDGETS = YES
```

These NEW budgets do NOT retroactively establish anything about the historical run. HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED stays a separate finding (F-D4; see 01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md when written). Per order §3, on the basis of these budgets it is forbidden to write back historically HISTORICAL_QC_BUDGET_PRE_REGISTERED = YES; the historical state remains a separate finding.

## 2. Hard caps (verbatim from the human order §3)

```text
CORRECTION_EXECUTOR_MAX_TOOL_CALLS = 80
CORRECTION_EXECUTOR_MAX_WALL_MINUTES = 120

FRESH_TARGETED_QC_MAX_TOOL_CALLS = 70
FRESH_TARGETED_QC_MAX_WALL_MINUTES = 90

QC_REPAIR_ROUNDS_MAX = 1
```

QC_REPAIR_ROUNDS_MAX = 1 (ONLY to repair a defect produced by THIS correction; NEVER for new science — order §3: "Repair round może zostać użyty WYŁĄCZNIE do naprawy defektu wytworzonego przez tę korektę. Nie może służyć do nowego science.")

## 3. PE-MASTER phase allocation INSIDE the executor-phase budget (transparent sub-budgets; stricter reading always wins)

```text
PHASE A FORMALIZE + PREREGISTER (pe-master-auditor):
  MAX 15 tool calls / <=25 min
  00_CONTROL only; NO corrections; NO RE; NO instrumentation.
```

PHASE A output set = exactly the three 00_CONTROL files authorized by the dispatch (AUTHORIZATION.md, PREFLIGHT.md, CORRECTION_BUDGET.md). PHASE A usage is self-reported in PREFLIGHT.md section 9 and in the PHASE A handoff.

```text
PHASE B CORRECTIONS (pe-reconstruction):
  MAX 65 tool calls / <=95 min
  Content: 01_ANALYSIS records for F-D1..F-D4
           + order §8 A/B/C non-blocking precisions
             (only where present in ACTIVE/current state)
           + order §11 deferred-lead record
             (RECORD ONLY; §12 candidate experiment = DESIGN ONLY, NOT_AUTHORIZED).
```

The ONLY permitted new physical measurements in PHASE B:

1. F-D3 static source identity verification of `CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp` (exact path, file size, SHA256, line-22 function locator) — labeled POST_AUDIT_SOURCE_CHECK = YES and MEASURED_DURING_CORRECTION = YES; no backdating as primary-executor knowledge; no new oracle mechanism (ORACLE_MECHANISMS = 3); no Gamebryo inventory, no SDK build, no runtime Gamebryo, no cross-version searches.
2. Bounded recounts of EXISTING historical artifacts (C3_DECOMP.json decompilation records vs unique function entries; grep censuses of live surfaces for the order §8 items).
3. A bounded session-store census attempt for F-D4 (<=5 tool calls; if the store is unavailable or not reconstructable → INHERITED_FROM_DESKTOP_POST_AUDIT with the exact source; never a faked measurement).

NO other new measurement; NO Ghidra; NO client; NO placement trace; NO 4057/0x0059AB12 RE.

```text
Sub-budget transfer is FORBIDDEN; A + B <= 80 in all cases.
```

## 4. Additional authorized-phase envelopes

PE-MASTER preregistration for order-authorized work the order does not numerically cap; declared here BEFORE work; these can never be used to exceed the 80/70 caps of section 2:

```text
PHASE C PE_MASTER_MASTER_AUDIT (supervisory audit by the PE-MASTER parent;
read-only + own counter-checks):
  MAX 80 tool calls / <=90 min

PHASE D ADMIN_PERSISTENCE (pe-master-auditor):
  FINAL_REPORT.md, HANDOFF.md, FINDING_DISPOSITION.md,
  PE_MASTER_REVIEW.md persistence, AUDIT_ENTRYPOINT.md correction row,
  final MANIFEST_SHA256.csv + bijection verification,
  staging + staged-blob verification, commit, push, fetch/remote verification:
  MAX 60 tool calls / <=60 min
```

## 5. COUNTING_RULE (verbatim from the human order §3)

```text
1 explicit tool invocation = 1 tool call.

A single tool invocation containing multiple shell/analysis commands
still counts as 1 tool call.

Internal reasoning without a tool invocation = 0.

Failed calls count.

Retries caused by auditor/executor instrument errors count.

Subagent/nested context calls, jeśli w ogóle dozwolone,
muszą być rozliczane jawnie w budżecie właściwej fazy.

Counters start at zero independently for:
A. correction executor
B. fresh targeted QC

No silent budget expansion.

When the cap is reached:
STOP and report PARTIAL / REVALIDATION_REQUIRED honestly.
```

## 6. Usage-measurement protocol

- Every phase self-reports used tool calls + wall minutes in its final handoff AND the number is persisted in the phase's own record:
  - PHASE A → `00_CONTROL/PREFLIGHT.md` (section 9) + PHASE A handoff;
  - PHASE B (correction executor) → the `01_ANALYSIS` execution-log section + PHASE B handoff;
  - FRESH TARGETED QC → `02_QC/TARGETED_QC_REPORT.md` + QC handoff;
  - PHASE D → `03_REPORT/FINAL_REPORT.md` (planned-vs-used fields per order §20) + PHASE D handoff.
- The fresh targeted QC verifies planned vs used for the executor and QC phases (order §13 Q5). If a cap is exceeded: `CORRECTION_RE_QC_FAIL` or an honest bounded partial — never a retroactive limit change (order §13 Q5; COUNTING_RULE: "When the cap is reached: STOP and report PARTIAL / REVALIDATION_REQUIRED honestly.").
- Counters start at zero independently for: A. correction executor, B. fresh targeted QC (order §3).

## 7. Historical budgets — unchanged (explicit closing statement)

The historical executor budgets remain PREREGISTERED_MAX_30 / PREREGISTERED_MAX_90 / PREREGISTERED_MAX_30 as recorded in the historical package 00_CONTROL/RUN_PLAN.md; the historical QC budget remains NOT_ESTABLISHED (F-D4).

```text
EXECUTOR_ENUM_BUDGET = PREREGISTERED_MAX_30
EXECUTOR_DEEP_TRACE_BUDGET = PREREGISTERED_MAX_90
EXECUTOR_CONTROLS_ORACLE_BUDGET = PREREGISTERED_MAX_30
HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED
```

(F-D4 required final statuses per order §7: HISTORICAL_TOOL_CALL_CENSUS = MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE; HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED; FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN. Closure only by honest process record, never by retroactive PASS.)

END OF PREREGISTRATION.
