# AMEND LOG R1 — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

One documentation-only repair round (QC_REPAIR_ROUNDS_MAX=1), executed by the
executor on the fresh-QC findings P2-1 / P3-1 / P3-2
(docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/07_QC/QC_AUDIT_R1.md,
owned by QC and untouched by this round).

Scope guard for every entry below: ZERO evidence changes, ZERO gate changes,
ZERO status changes, ZERO claim changes, ZERO new science, ZERO scope
expansion. Only the exact text fragments listed here were modified; no file
outside this package (and no file inside 07_QC/) was touched. No commit /
push / stage; AUDIT_ENTRYPOINT.md untouched.

Pre-edit verification performed by the executor (own measurements, not
faith-in-QC):
- P2-1: census-target caller enumerations recounted directly from the RAW
  JSON artifacts: C2=19 (targets), C4=10 (census), C5=4 (census), C6=8
  (census), C8=4 (census) => 45. AGREE with QC finding.
- P3-1: raw EXE bytes re-read at VA 0x005B6597 (own PE mapper):
  `68 D3 3E 00 00` = PUSH 0x3ED3; next instruction @0x005B659C
  `E8 ...` rel32 -> 0x005B5F90 (recomputed). AGREE with QC finding (my
  earlier "68 2D" was a signed-hex transcription residue; C10V2 raw data was
  already correct).
- P3-2: R08 (FUN_00848EA0) decompile re-read from C3_DECOMP.json: the
  id2 -> lookup -> FUN_0072FE30 -> FUN_006C1F90 lerp -> slot+0x00 chain
  executes in the `else` branch of `FUN_00745540(1)` (flag 1 TRUE); the
  per-slot {u16@+0xC, float@+0x10} stores execute under `FUN_00745540(2)`
  (flag 2). AGREE with QC finding (my E9(c)/E10 wording swapped the flag
  numbers).

Repair UTC: 2026-10-03T09:04:00Z (measurements + edits + this log written in
one round; per-entry exact BEFORE/AFTER below, each verifiable by diff).

---

## AMEND-1 (finding P2-1)

- FILE: 06_REPORT/DRAFT_FINAL_REPORT.md — COVERAGE line (~line 29-30)
- BEFORE (exact):
  ```
  COVERAGE = own machine census: 19+10+8+4+4+8+4+12 = 69 census-target caller
    enumerations (denominators reported per target in the C2/C4/C6/C8 JSONs);
  ```
- AFTER (exact):
  ```
  COVERAGE = own machine census: 45 = 19+10+4+8+4 census-target caller
    enumerations (C2=19, C4=10, C5=4, C6=8, C8=4; denominators reported per
    target in the C2/C4/C5/C6/C8 JSONs);
  ```
- REASON: QC P2-1 — the "69" figure (and its breakdown string) did not
  reconstruct from any RAW census; the RAW census-target count is 45
  (19+10+4+8+4), consistent with 02_ANALYSIS/NOT_CHECKED.md line 65 ("45
  census target lookups"). My error: I had summed mixed census + decompile
  target lists. Corrected to the single consistent package-wide figure with
  breakdown.
- VERIFY: own recount from 01_RAW JSONs (see above) — AGREE with QC.

## AMEND-2 (finding P2-1, second occurrence of the same wrong figure)

- FILE: 06_REPORT/DRAFT_FINAL_REPORT.md — INDEPENDENT_CROSSCHECKS line
  (~line 117-118)
- BEFORE (exact):
  ```
  INDEPENDENT_CROSSCHECKS = own census caller enumerations (69 target
    enumerations with denominators) vs the decompile chains; C1 file walk (own
  ```
- AFTER (exact):
  ```
  INDEPENDENT_CROSSCHECKS = own census caller enumerations (45 target
    enumerations with denominators = 19+10+4+8+4) vs the decompile chains; C1 file walk (own
  ```
- REASON: same P2-1 defect (the same wrong "69" repeated in the second place).
  Corrected to 45 with the same breakdown so the package carries ONE
  consistent census-target figure.
- VERIFY: same own recount — AGREE with QC.

## AMEND-3 (finding P3-1)

- FILE: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md — E9(a) hardcoded-immediate line
  (~line 333)
- BEFORE (exact):
  ```
        - FUN_005B6597: 68 2D 3E 00 00  PUSH 0x3ED3 (16083) -> CALL FUN_005B5F90
  ```
- AFTER (exact):
  ```
        - FUN_005B6597: 68 D3 3E 00 00  PUSH 0x3ED3 (16083) -> CALL FUN_005B5F90
  ```
- REASON: QC P3-1 — the byte string "68 2D" was a signed-hex transcription
  residue (Ghidra Jython prints 0xD3 as "-2D"); the physical EXE bytes at
  VA 0x005B6597 are `68 D3 3E 00 00` = PUSH 0x3ED3, followed by
  CALL -> 0x005B5F90 (rel32 recomputed from raw bytes). Only the hex digit
  "2D" -> "D3" changed; the claim (PUSH 0x3ED3 hardcoded id2 driver) is
  unchanged and remains byte-pinned.
- VERIFY: own raw read at 0x005B6597 + rel32 target recomputation — AGREE
  with QC (C10V2 data was already correct; only this prose line was wrong).

## AMEND-4 (finding P3-2)

- FILE: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md — E9(c) attribute-path lines
  (~lines 345-346)
- BEFORE (exact):
  ```
    (c) ATTRIBUTE path: FUN_00848EA0 (R08) reads per-slot {u16@+0xC, float@+0x10}
        and for flag-2 slots: id2 from property machinery (Q05: class 20006
  ```
- AFTER (exact):
  ```
    (c) ATTRIBUTE path: FUN_00848EA0 (R08) reads per-slot {u16@+0xC, float@+0x10}
        under flag 2, and for flag-1 slots: id2 from property machinery (Q05: class 20006
  ```
- REASON: QC P3-2 — inverted flag numbering. Per the R08 decompile: the
  id2 -> lookup -> FUN_0072FE30 -> FUN_006C1F90 lerp -> slot-position chain
  executes under FUN_00745540(1) != 0 (flag 1), while the per-slot
  {u16@+0xC, float@+0x10} stores execute under FUN_00745540(2) (flag 2).
  The minimal flag-number correction ("flag-2 slots" -> "flag-1 slots") is
  accompanied by the explicit "under flag 2" attribution for the
  u16/float slot stores, so the corrected sentence does not silently
  re-attach them to flag 1. Mechanism description, offsets (+0xC/+0x10/
  +0x00), and all other content of E9(c) unchanged.
- VERIFY: own re-read of R08 in C3_DECOMP.json — AGREE with QC.

## AMEND-5 (finding P3-2, second occurrence of the same inversion)

- FILE: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md — E10 SELECTED_PATH line (~line 399)
- BEFORE (exact):
  ```
    flag-2 branch executes lookup -> FUN_0072FE30 -> lerp -> store.
  ```
- AFTER (exact):
  ```
    flag-1 branch executes lookup -> FUN_0072FE30 -> lerp -> store.
  ```
- REASON: same P3-2 defect in the E10 edge block. Only the flag number
  changed; the reachability proof (R08 loop over 3 slots; the id2/lerp store
  to slot+0x00) is unchanged.
- VERIFY: same own re-read of R08 — AGREE with QC.

---

## Post-repair consistency verification (executor's own)

- Grep sweep of the executor-owned files (00_CONTROL, 01_RAW, 02_ANALYSIS,
  03_SCRIPTS, 04_CONTROLS, 05_ORACLE, 06_REPORT): no remaining "69
  census"/"= 69"/"68 2D"/"flag-2 slots"/"flag-2 branch" occurrences;
  the census-target figure now appears consistently as 45 (with breakdown
  19+10+4+8+4) in DRAFT_FINAL_REPORT.md (COVERAGE and INDEPENDENT_CROSSCHECKS)
  and NOT_CHECKED.md line 65.
- No claim/status/gate/denominator load-bearing was altered by these
  repairs: the corrected items are (a) a wrong census count figure in prose
  (the load-bearing denominators 962/962, 113/113, 88/120, 3/3, 45 census
  are untouched and now stated consistently), (b) one wrong hex digit in a
  prose byte string (the pinned evidence C10V2 was already correct), (c) two
  flag-number words in prose (mechanism/offsets unchanged). RESULT_LEVEL,
  all CLAIM statuses, all CONTROL statuses, RUN_CLASS, budgets and all
  01_RAW evidence artifacts are byte-unchanged.
- 07_QC/ untouched (QC-owned). No other files created or modified besides
  the two repaired files, this AMEND_LOG_R1.md, and the regenerated
  artifact_index.csv (which by design carries the post-repair hashes of the
  repaired files plus this new log file).
