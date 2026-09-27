# F01 — PRIMARY_DEVICE REVALIDATION

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. ORIGINAL CLAIM AND SOURCE

Desktop claim (GC-F01, P1): `display_env_measurement.py:73` uses `StateFlags & 2`
for the PRIMARY label; Microsoft defines DISPLAY_DEVICE_PRIMARY_DEVICE as 0x4 while
0x2 is DISPLAY_DEVICE_MULTI_DRIVER; the raw first record (DISPLAY1) has
StateFlags 0x04000005, so PRIMARY=True for 1/6 adapters — NOT zero. The error
propagates into the load-bearing x87 blocker record.

Historical sources (READ-ONLY; pinned in 00_CONTROL/SOURCE_INDEX.md):
- `99_Audits/PE_NIGHT_AGGREGATE_20260905_160000/display_env_measurement.py`
  (SHA256 E9C3F1B4...) — line 73 verbatim:
  `f"PRIMARY={bool(dd.StateFlags & 2)}, "`
- `99_Audits/PE_NIGHT_AGGREGATE_20260905_160000/DISPLAY_ENV_MEASUREMENT.txt`
  (SHA256 295E9E9C...) — raw StateFlags: DISPLAY1 = 0x04000005; DISPLAY2..DISPLAY6
  = 0x04000000. The file's own printed line 5 carries the WRONG decode:
  "(ATTACHED=True, PRIMARY=False, ...)".

## 2. SDK CONSTANT VERIFICATION (independent source class)

Desktop cited the win32metadata wingdi.h + DISPLAY_DEVICEA docs (web class). This
run found a STRONGER existing source: the LOCAL INSTALLED Windows SDK header
`C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\um\wingdi.h`
(SHA256 D3A5E8BFFBF9AAAB40886705212949459373C90C3B70755980270669E3C06E21). The
probe (03_EVIDENCE/scripts/r1_f01_primary_device.mjs) parses the #defines directly:

```
wingdi.h:2762: DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 0x00000001
wingdi.h:2763: DISPLAY_DEVICE_MULTI_DRIVER      = 0x00000002
wingdi.h:2764: DISPLAY_DEVICE_PRIMARY_DEVICE    = 0x00000004
wingdi.h:2765: DISPLAY_DEVICE_MIRRORING_DRIVER  = 0x00000008
wingdi.h:2768: DISPLAY_DEVICE_REMOVABLE         = 0x00000020
wingdi.h:2771: DISPLAY_DEVICE_ACC_DRIVER        = 0x00000040
wingdi.h:2773: DISPLAY_DEVICE_MODESPRUNED       = 0x08000000
wingdi.h:2776: DISPLAY_DEVICE_REMOTE            = 0x04000000
```

ADJUDICATION: DISPLAY_DEVICE_PRIMARY_DEVICE = 0x4 CONFIRMED from a local installed
authoritative header; the historical `& 2` mask = MULTI_DRIVER. Desktop's constant
claim REPRODUCED with a stronger source class.

## 3. PER-ADAPTER RECOMPUTATION (both predicates; raw flags only)

Recomputed from DISPLAY_ENV_MEASUREMENT.txt raw StateFlags (probe output
03_EVIDENCE/F01_PRIMARY_DEVICE_REVALIDATION.json):

| iDev | Device | raw flags | OLD (&2) PRIMARY | CORRECTED (&4) PRIMARY | ATTACHED | REMOTE | MIRRORING |
|---|---|---|---|---|---|---|---|
| 0 | \\.\DISPLAY1 (Microsoft Remote Display Adapter) | 0x04000005 | false | **TRUE** | true | true | false |
| 1 | \\.\DISPLAY2 | 0x04000000 | false | false | false | true | false |
| 2 | \\.\DISPLAY3 | 0x04000000 | false | false | false | true | false |
| 3 | \\.\DISPLAY4 | 0x04000000 | false | false | false | true | false |
| 4 | \\.\DISPLAY5 | 0x04000000 | false | false | false | true | false |
| 5 | \\.\DISPLAY6 | 0x04000000 | false | false | false | true | false |

PRIMARY_DEVICE count: OLD = 0/6 (the historical "ZERO"); CORRECTED = **1/6**
(DISPLAY1 = ATTACHED + PRIMARY + REMOTE). REPRODUCED — not zero.

MASK CONTROLS (all as predicted):

| input | ATTACHED | MULTI_DRIVER | PRIMARY(&4) | OLD output (&2) | classification |
|---|---|---|---|---|---|
| 0x0 | false | false | false | false | both false — correct |
| 0x1 | true | false | false | false | both false — correct |
| 0x2 | false | true | false | true | OLD = FALSE-POSITIVE (0x2 is MULTI_DRIVER) |
| 0x4 | false | false | true | false | OLD = false-NEGATIVE for PRIMARY |
| 0x5 | true | false | true | false | OLD = false-NEGATIVE for PRIMARY |
| 0x04000005 | true | false | true | false | the actual DISPLAY1 flags — OLD missed the primary |

Also observed (all 6 adapters): REMOTE flag set (0x04000000 base) — the environment
is a Microsoft Remote Display Adapter session on every device, which is an
OBSERVED FACT independent of the PRIMARY decode.

## 4. §5.1 DEPENDENCY TRACE (the false premise walk-through)

For every dependent claim, the classification (UNAFFECTED / WORDING_ONLY /
NARROWED / REVALIDATION_REQUIRED / REJECTED):

1. `display_env_measurement.py:73` (the measurement code) — REJECTED (the
   predicate is wrong; the file preserved byte-identical as evidence of the error).
2. `DISPLAY_ENV_MEASUREMENT.txt` (raw output) — the RAW FLAGS UNAFFECTED (they are
   the measurement); the printed "PRIMARY=False" label REJECTED.
3. Night-aggregate N-3 (the display-enum canon; "StateFlags = 0x04000005
   ATTACHED=1, PRIMARY=0") — the label REJECTED; the environment observations
   (remote adapter, degenerate mode lists, empty DeviceKey) NARROWED (kept as
   observed facts, with the primary correction).
4. Night-aggregate N-13 final honest state ("6x Remote Display Adapter, ZERO
   PRIMARY_DEVICE, empty DeviceKeys, single-mode lists...") — the ZERO-PRIMARY
   phrase REJECTED; the rest (exit after display enum before graphics DLLs;
   debugger route closed as contaminating; remaining bound = exact in-module
   predicate) NARROWED and kept.
5. M1-CL-20 (CLAIM_LEDGER; "degenerate RDP display measured 6x Remote Display
   Adapter / 0 PRIMARY_DEVICE / HardwareInformation.MemorySize missing") —
   REVALIDATION_REQUIRED: the row's premise basis is false; its other content
   (PC24 sensitivity; conditional model) UNAFFECTED.
6. X87_RUNTIME_AUDIT item 3 (BLOCKER description) — REVALIDATION_REQUIRED (same
   false premise); items 5-8 (load-bearing conditionality, Gate-A allowance)
   UNAFFECTED as contract text.
7. CLOSURE_GATE_MATRIX GATE A evidence cell — REVALIDATION_REQUIRED (the cell
   carries "0 PRIMARY_DEVICE"; the Gate-A PASS built on it is not inherited).
8. PE_MASTER_M1_FULL_AUDIT.md §14 (Gate-A result), §16 (X87 DISPOSITION
   "UNMEASURED / ENVIRONMENT_BLOCKED"), §11 — REVALIDATION_REQUIRED for the
   ENVIRONMENT_BLOCKED cause label; the CONDITIONAL-model documentation
   UNAFFECTED.
9. UNRESOLVED C7 / OPEN_LIMITS OL-05 — STATUS_REVALIDATION (the honest
   BLOCKED-UNKNOWN survives, but only on the corrected basis).
10. AUDIT_ENTRYPOINT.md IMMEDIATE BLOCKER cell ("ZERO PRIMARY_DEVICE flags") —
    WORDING (stale carried field): recorded here + in the successor row; NOT
    edited in the historical cell (row-survival scope).
11. X87_CW_M1_CLOSURE_BLOCKER = CONDITIONAL — UNAFFECTED (the conditionality
    never depended on the primary decode).
12. PC=24 sensitivity measurements (14,104/229,376 + 103,073/1,245,184) —
    UNAFFECTED (no physical dependency).
13. The georef/witness/cellstream queue verdicts — UNAFFECTED.

## 5. §5.2 CORRECTED X87 DISPOSITION (the A-E variable split)

- A. ORIGINAL FOLIAGE-SITE CW (the value of the x87 control word at the foliage
  chain-execution site) = **UNMEASURED** (no valid contrary evidence found in the
  bounded evidence; the f0906b9 retracted run is not a measurement; the
  qualification_notepad is a harness artifact).
- B. CLIENT EXIT = **CONFIRMED**, independently reproduced from the existing
  ProcMon trace (this run re-derived it): `entropia_death_trace.csv`
  (SHA256 2BFA1F7C...) — 1 distinct Entropia.exe PID (12976); 2,193
  Process-Name=Entropia.exe rows; exactly ONE Process Exit row:
  "Exit Status: -1, User Time: 0.0000000, Kernel Time: 0.0937500"; ZERO
  ddraw/d3d8/d3d9 Load Image rows (77 Load Image rows total, d3dx9_30 x2 but no
  D3D runtime). The HardwareInformation.MemorySize query = "NAME NOT FOUND"
   (registry class key {4d36e968...}\0000). TRACE TOTAL-ROW DELTA — ROOT-CAUSED
   (AMEND_R1, 03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json): the historical quote
   "282,059 rows" is CORRECT (282,060 LF bytes = header + 282,059 data rows; also
   confirmed by a quote-aware RFC4180 parse of the same bytes). This run's fresh
   count reported 282,192 data rows only because its line reader was
   CR-SENSITIVE: 133 lone CR bytes (CR not followed by LF, embedded inside
   quoted Detail fields) were each counted as an extra line boundary
   (282,060 + 133 = 282,193 counted lines -> 282,192 "data rows"). The delta is
   a LINE-COUNTING ARTIFACT, NOT a data discrepancy; the per-client
   load-bearing facts (1 PID / 2,193 Entropia.exe rows / exactly one
   "Exit Status: -1" / 0 ddraw-d3d8-d3d9 loads) are UNAFFECTED (all re-verified
   under the CR-correct parse; byte census LF = 282,060 / lone CR = 133, both
   matching PE-MASTER's independent counts). (Provenance note:
   live_test_record.json records pid=10824 while the trace's only client PID is
   12976 — a historical-package provenance inconsistency, recorded; not
   load-bearing for the exit fact.)
- C. DISPLAY ENVIRONMENT OBSERVED FACTS = **STAND**: 6 adapters, all
  "Microsoft Remote Display Adapter" (RdpIdd_IndirectDisplay), all REMOTE
  (0x04000000), DISPLAY1 ATTACHED+PRIMARY (corrected decode), single-mode lists
  (j=1), empty DeviceKey fields (a RESERVED field per the DISPLAY_DEVICEA
  documentation — not malfunction evidence).
- D. CAUSAL BLOCKER = **UNKNOWN**: ProcMon temporal ordering (MemorySize miss
  then exit) is not causality; the exact in-module predicate the client rejects
  (EXACT_BOOT_REJECTION_PREDICATE) = UNKNOWN; "ENVIRONMENT_BLOCKED" as a
  CONFIRMED cause class is NOT established and is corrected to a HYPOTHESIS
  (plausible; unproven). The safest current cause class = UNKNOWN, described by
  the observed boot/display failure.
- E. AV/EAX = supersession PRESERVED: N-9 withdrew the EAX-residue theory
  (DEBUG_EVENT union artifact); N-13 retracted the H5 AV mechanism as a
  debugger-interaction artifact and closed the debugger route as contaminating.
  This run does NOT resurrect AV/EAX as proof.

EXACT_BOOT_REJECTION_PREDICATE = UNKNOWN. No new client/GPU experiment was run
(STATIC-ONLY).

## 6. RESULT

Desktop GC-F01 REPRODUCED in full (constants from a stronger local source; 1/6
primary; all carried-field dependencies confirmed). The ZERO-PRIMARY premise is
RETRACTED (RETRACTION_SUPERSESSION_DELTA.csv NEW-F01). The x87 P0's supporting
record must be rebuilt on the true premises (A-E above) — see
01_RAW/GATE_REVALIDATION.csv GATE A.
