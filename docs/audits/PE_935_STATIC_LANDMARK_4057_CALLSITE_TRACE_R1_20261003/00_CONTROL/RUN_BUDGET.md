# RUN BUDGET — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

PREREGISTERED BEFORE ANY SCIENCE (contract §6; supervisory addition 2).
Written and saved before Phase 1 execution began.

## Hard limits (verbatim from the frozen contract)

```text
EXECUTOR_MAX_TOOL_CALLS = 120
EXECUTOR_MAX_WALL_MINUTES = 180

FRESH_QC_MAX_TOOL_CALLS = 80
FRESH_QC_MAX_WALL_MINUTES = 120

QC_REPAIR_ROUNDS_MAX = 1

NEW_PCG_FUNCTIONS_DETAILED_MAX = 60

NEW_PHYSICAL_RECORDS_DETAILED_MAX = 2

NEW_MODEL_RESOURCE_INDEX_RECORDS_MAX = 4

NEW_GAMEBRYO_ORACLE_MECHANISMS_MAX = 0
```

Scope-expansion rule (contract §6): if answering requires >60 new functions or
tracing multiple independent subsystems: STOP; RESULT = PARTIAL_COVERAGE.
Limits are NOT expanded after seeing results.

## Executor plan / usage ledger (updated at phase boundaries; final values in
DRAFT_FINAL_REPORT.md; tool calls counted per tool invocation incl. reads,
writes, bash, glob, grep, skill loads; wall minutes self-reported from session
clock — declared-not-machine-measured, per the F-D4 discipline)

```text
PLANNED (per contract)          USED (final, self-reported)
EXECUTOR_TOOL_CALLS   120       <final>
EXECUTOR_WALL_MINUTES 180      <final>
NEW_PCG_FUNCTIONS_DETAILED 60   <final: count of functions first detailed this run>
NEW_PHYSICAL_RECORDS_DETAILED 2 <final: templates.vfs record 4057 (+ at most 1 more if strictly needed)>
NEW_MODEL_RESOURCE_INDEX_RECORDS 4 <final>
NEW_GAMEBRYO_ORACLE_MECHANISMS 0 <final: 0 — existing Gamebryo canon read as context only>
```

## Phase plan (contract §8-§19; each phase gated on the previous)

```text
P1  templates.vfs record 4057 re-pin (own walker; cross-check vs canon 5,438/0-CRC/EOF + record 4508 anchor)
P2  raw byte pin at VA 0x0059AB12 (own PE mapper; opcode/immediate/file offset/section)
P3  containing function (Ghidra 11.2.1 fresh project; entry/end/size/callers/callees/ABI evidence)
P4  PUSH 4057 argument/dataflow role (byte-anchored per-instruction chain)
P5  template-id consumer test (FUN_0072F580 or independently proven consumer) — MANDATORY FALSIFIER
P6  (only if P5 PASS) template -> A bridge
P7  (only if P6 PASS) resource request/construction separation
P8  (only if P7 progresses) object identity
P9  (only if P8 ESTABLISHED) transform source + E10 lesson discipline
P10 (only if P9) scene/world edge
P11 (only if all) XYZ recovery
886 : mechanical dataflow only if in the same function/call sequence and needed for 4057; else NOT_CHECKED_FURTHER
CONTROLS-1..5 (contract §20)
```

## Budget-tracker rows (append-only during the run)

```text
2026-10-03 BOOT/PREFLIGHT+CANON: tool_calls_used=19, wall_minutes_used≈20
2026-10-03 CONTROL FILES WRITTEN (AUTHORIZATION/PREFLIGHT/BUDGET/SELECTION): tool_calls_used=23
2026-10-03 PHASE 1 (s1 template re-pin + BNT2 index): CONFIRMED (record 4057 A=218757 B=218758; 218757.nif/218758.bvi PRESENT); calls≈31
2026-10-03 PHASE 2 (s2 raw pin): CONFIRMED (PUSH 4057 @0x0059AB12, .text, offset 1682194); calls≈33
2026-10-03 PHASE 3 (Ghidra g1 + s3/s4 curate + 951/951 crosscheck): FUN_00599D30 0x00599D30-0x0059AC88, 3929 B, 951 ins, 1 caller; calls≈45
2026-10-03 PHASE 4 (s4 windows + immediate census): 4057 = arg1 of thiscall FUN_008DFCD0; series 0xFD4..0xFD9; calls≈48
2026-10-03 PHASE 5 falsifier chain (g2,g3,g4,g5,g6 + s5-s8 curate + reach-check): ZERO template-registry hits; terminal consumer = sids.vfs string table; calls≈70
2026-10-03 DATA-SIDE CLOSURE (s9,s10,s11): sids.vfs 129,040 B parsed, 3,887 entries; 0xFD9 = S_REPAIR_UI_CLEAR_TOOLTIP; RESOURCE_INDEX_PINS written; calls≈78
2026-10-03 ANALYSIS/REPORT WRITES (02_ANALYSIS x8 + DRAFT_FINAL_REPORT): calls≈84
2026-10-03 FINAL LEDGER: EXECUTOR_TOOL_CALLS used=84/120; wall≈130/180 min (self-reported);
  NEW_PCG_FUNCTIONS_DETAILED=18/60; NEW_PHYSICAL_RECORDS_DETAILED=2/2;
  NEW_MODEL_RESOURCE_INDEX_RECORDS=4/4; NEW_GAMEBRYO_ORACLE_MECHANISMS=0/0.
  STOP S2 (falsifier) fired as the science-branch terminal condition; S5 (budget) NOT reached.
```
