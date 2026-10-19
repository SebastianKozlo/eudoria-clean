# P09 HANDOFF — to PE-MASTER

run_id: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | package: P09_EXEC_R1 | front C | run_status: COMPLETED_IN_WINDOW

## 1. Result in one paragraph

0x006C3640 = generic per-element enqueue loop (body prefix; continues out-of-window). Queue object = 4th stack DWORD (ESI): `[+4]` write/tail cursor (ONLY object field written in-window, `+=8` per entry), `[+8]` limit compared for equality (read-only), `[+0]` untouched in-window. Entry = 8 bytes = 2 DWORDs copied from callback-result pair `[EAX]`,`[EAX+4]`. Semantics: callback per element (ECX=element, ABI inference) -> capacity-event branch when cursor==limit (out-of-window 0x006C3678; CAND-A grow vs CAND-B lazy-alloc/flush, UNVERIFIED) -> NULL-skip count-only advance -> else in-place pair store + cursor advance. NO count update, NO head update, NO entry-pointer store into object fields in-window. Exactly 2 call sites target it (006c3fcd, 006d4501 — the P07 clusters 006C3F98/006D44A4). Corpus-coverage data barrier independently re-verified: 0x0040B070 / 0x0043E5B0 / 0x0043C700 have ZERO body rows in the saved main listing (only CALL operands: 17/1/10 sites).

## 2. Out-of-window VAs — recorded, NOT read (per contract)

- 0x006C3678 — JZ target (006c3662), capacity-event path. Incidentally displayed in the boundary read block; NOT analyzed, NO claims.
- 0x006C368A — JMP target (006c3676), loop tail (rows up to the back-edge at 006c368f were incidentally displayed; NOT analyzed).
- 0x006C369C — JZ target (006c364c), empty-range exit. NOT analyzed.
- 0x006C2E00 — observed only as a call operand inside incidentally-displayed out-of-window rows; NOT analyzed.
- 0x0040B070, 0x0043E5B0, 0x0043C700 — transport callees; bodies ABSENT from saved listing (data barrier, P09-B1); navigation census of their call sites only.
- 0x008BD720 — callback per cited P07; body out of scope here.
- Caller bodies: 0x006C3F98 cluster, 0x006D44A4 cluster — call sites enumerated by navigation only (006c3fcd, 006d4501; 40B070 sites 006c3fb5, 006d44ed).
- GHIDRA_GATE_00407270.txt (separate saved corpus file with decompiled FUN_0040b070) — incidentally matched by grep; NOT read/analyzed; backlog P09-B3.

## 3. Precise remaining edge (one per this front-closure)

FIRST_MISSING_EDGE for the transport close-out: the **capacity-event handler at 0x006C3678** (plus loop tail 0x006C368A-0x006C369A) — it decides CAND-A (grow/extend) vs CAND-B (lazy-alloc/flush), carries the element stride and the function epilogue (RET width -> caller arg count). Second-order, behind data barrier P09-B1: bodies of 40B070/43E5B0/43C700 are absent from the main listing; P09-B3 offers a saved decompiled 0040B070 in GHIDRA_GATE_00407270.txt pending admission. The queue CONSUMER (who drains the 8-byte pair entries; queue class identity; role of [+0]) remains unmapped (P09-B4).

## 4. Data barrier (as instructed to record)

**0x0040B070, 0x0043E5B0, 0x0043C700 are NOT in the saved listing** (no body rows; CALL operands only: 17 / 1 / 10 sites). Parent's navigation-level finding independently re-verified in this run (working Grep tool; first rg attempt failed and its outputs were discarded). Consequence: transport-chain callee semantics cannot be closed from GHIDRA_H5_VTABLE2.txt; needs another corpus source (e.g., GHIDRA_GATE_00407270.txt for 0040B070, pending admission) or remains a permanent corpus gap.

## 5. Counters and compliance

Actual: 1 body (prefix) / 23 rows / 1 CALL (indirect) / 4 edges / 2 candidates / 0 unforeseen bodies / 0 incidents. Reserved: 1/23/4/2 — full match (prose "4 CALL" reconciled to contract field edges=4; actual CALL=1 matches the question's "1 call"). Package hard stop 2026-10-19T00:20:00Z respected; all writes confined to packages\P09_EXEC_R1; RUN_STARTED.json materialized first (2026-10-18T23:07:05Z); MANIFEST.json written LAST self-excluded. No forbidden operations performed.

## 5. Artifacts

CONTRACT.json (copy, SHA-verified), RUN_STARTED.json, EXTRACT_006C3640_006C3678.txt (23 verbatim rows + metadata), NAVIGATION_CENSUS.txt, SOURCE_PINS.json, CLAIMS.json (8 claims with evidence/premises/countermodel/evidence_level), MEMORY_AND_IDENTITY.json, COUNTERS.json, BARRIER_BACKLOG.json (B1-B4), REPORT.md, HANDOFF.md, GATES.json, artifact_index.csv, MANIFEST.json (self-excluded).
