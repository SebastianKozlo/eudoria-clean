# HANDOFF — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009

## Mandatory handoff block

- **AUDIT_OUTPUT_ROOT**: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\`
- **FINAL_REPORT_PATH**: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\FINAL_REPORT.md`
- **PRIMARY_EVIDENCE_PATHS**:
  - `CALLER_CENSUS.json` (master machine-readable census: per reference class, per caller)
  - `01_RAW\S1_REPIN_RAW_CENSUS.json` (subject byte re-pins + raw E8/E9/absolute scans, own PE mapper)
  - `01_RAW\C2_SUBJECT_REPINS.json` (FUN_0072F580 / FUN_0043A550 listings + decompiles + all refs; DAT_00BA1824 refs)
  - `01_RAW\CENSUS_AGREEMENT.json` (dual-method agreement: raw ↔ Ghidra, VA-identical)
  - `01_RAW\C2_CALLER_WINDOWS\c2_caller_00..11_*.json` (12 per-caller windows: listing + decompile + callsites + body-end context)
  - `01_RAW\CALLSITE_CONTEXTS.json` (byte-anchored context slices around every getter/lookup callsite)
  - `01_RAW\ID_TABLE_DUMPS.json` (.rdata id-table dword dumps)
- **RUN_STATUS**: **COMPLETE**
- **HARD_STOP_REASON**: NONE (no hard stop fired)
- **Measured EXE SHA256 before**: `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
- **Measured EXE SHA256 after**: `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (identical; 8,015,872 B)
- **Caller count found + analyzed**:
  - FUN_0072F580: **25 direct CALL callsites found / 23 unique caller functions; 12 analyzed in depth** (the pre-registered priority consumed all 12 windows on lookup callers), 11 IDENTIFIED_NOT_ANALYZED.
  - FUN_0043A550: **35 direct CALL callsites found / 32 unique caller functions; 12 analyzed in depth** (the same 12 windows — all 12 lookup callers also call the getter; pair pattern), 20 IDENTIFIED_NOT_ANALYZED (11 shared lookup callers + 9 getter-only callers).
  - Union: 32 unique caller functions; 12/12 budget windows classified; 20 recorded honestly as IDENTIFIED_NOT_ANALYZED.
- **Gates**:
  - **G1 CENSUS_COMPLETE: PASS** — 10/10 reference classes (C1..C10) enumerated for 2/2 functions with method + result; the only NOT_CHECKED element is the statically non-enumerable register-computed-only indirect-call sub-class (explicitly listed with reason).
  - **G2 CALLER_CLASSIFIED: PASS** — 12/12 in-budget callers have (VA, window bounds, id-source class, returned-object role class) with byte-anchored evidence; 3/3 UNKNOWN-provenance cases explicitly marked; 0 guessed.
  - **G3 IDENTITY: PASS** — EXE SHA unchanged before/after (2/2 checks); historical landmark package 84/84 files byte-unchanged (baseline before + re-verify after); reused-project sandbox EXE unchanged; 0 .pyc residue created by this run in its own locations (run scratch, package, historical landmark package; all `python` invocations used `-B`) — pre-existing foreign untracked .pyc/__pycache__ artifacts elsewhere in the repo tree (cwd) predate this run and are out of scope of the residue claim.
  - **G4 NO_PROMOTION: PASS** — 0 XYZ/placement/building-instance claims; 0 runtime claims; all findings STATIC_ONLY with maturity labels (IDENTITY/BYTE_OBSERVATION/STRUCTURE/RELATION only).
- **Every NOT_CHECKED class**: register/computed-only indirect-call targeting (target VA never appearing as a static immediate) — statically non-enumerable; measured 0 absolute-VA hits anywhere, so no static evidence of any indirect path exists. No other class NOT_CHECKED.
- **Intervention ledger**: expected NONE (STATIC_ONLY) — actual: (1) one C2 Ghidra postscript bugfix cycle (Jython `Data.hasValue()` overload quirk); script re-hashed after final edit BEFORE the successful run; failed attempt logged, discarded, re-measured; no scientific result depends on it. (2) Ghidra project reuse disclosure: the reused LANDMARK4057 scratch project DB was re-saved by Ghidra on open/process (99_Audits scratch, not a historical package; historical packages byte-verified unchanged). No other interventions; no input file modified.

## 15-line census summary

1. Census subjects re-pinned at exact VAs: FUN_0072F580 (46 B, thiscall map lookup over the 0x18-byte singleton), FUN_0043A550 (119 B, lazy singleton getter), DAT_00BA1824 (undefined4, zero-init .data tail) — all prior labels re-verified, none inherited.
2. DAT_00BA1824 has exactly 3 references in the whole binary, ALL inside FUN_0043A550 (1 read @0x0043A571, 2 writes @0x0043A59B/0x0043A5B2) — dual-method confirmed.
3. FUN_0072F580: 25 direct CALL sites / 23 unique callers; FUN_0043A550: 35 / 32; raw E8 scan and Ghidra agree VA-identically (0 disagreements); every candidate is a defined instruction.
4. Zero E9 (no thunks/tail calls), zero absolute-VA occurrences (no address-taken/vtable/callback/jump-table/data refs), zero Ghidra computed refs — both functions are reachable only by direct CALL from defined code (statically).
5. Consumer-pair pattern: all 23 lookup callers also call the getter immediately before the lookup (singleton passed as `this`).
6. 12/12 in-budget windows classified (priority = lookup callers; 20 remaining functions recorded IDENTIFIED_NOT_ANALYZED with callsites).
7. (a) YES — static/persisted id sources confirmed: 7 accessor windows read ids from .rdata id tables (0x00A855D0/0x00A85608/0x00A85778/0x00A857C8/0x00A85804/0x00A858B4/0x00A858BC), indexed by object state, bounds-checked.
8. Two more windows feed branch-selected immediate ids: FUN_00511070 (0x2DF9/0x2DFA @0x00511245/0x0051121C) and FUN_00567170 (0x3BDA @0x00567338 + 0x3BDB/0x3BD9/0x3A40/0x3A47 branches).
9. Three windows carry UNKNOWN-provenance ids honestly marked (FUN_006c3f50 caller-arg @0x006C3F53; FUN_00733490 function-return @0x0073350A; FUN_006baa20 object-field @0x006BAB25).
10. No in-window id equals 4057; the registry POPULATION path (VFS reader cluster) was out of scope and untouched.
11. (b) NO transform-relevant access ESTABLISHED — zero direct field accesses on the returned template in ALL 12 windows; consumption = pointer-store into caller structures or pointer-forward; one read pattern on an UNKNOWN-identity derived object recorded (FUN_006c3f50: [EAX]/[EAX+4] @0x006C3FBE/C1 of the FUN_0040b070 result, forwarded to FUN_006c3640; transform relevance UNKNOWN).
12. Byte-anchored stores (caller-owned fields, not template fields): FUN_006baa20 `89 7E 0C` @0x006BAB60 (this+0xC); FUN_00733490 `89 37` @0x00733529 (3×0x18 record slots).
13. Byte-anchored forwards: FUN_007ce1e0 @0x00511259/@0x006C3F74 (with 0x66), FUN_0040b070 @0x006C3FB5 (with 0x8BD720), FUN_0072fce0 @0x006BAB4F/@0x00733520, FUN_005670a0 @0x0056737A — all callee bodies CLOSED this run.
14. FUN_00567170's window contains float ops (FLD [0x00a7d688] @0x00567324, float+100 reads) but none target the template — recorded to prevent over-claiming.
15. Follow-up candidates (not done): decode FUN_0072fce0 (template validity method, called in 2 windows), the FUN_007ce1e0 getter family, and FUN_0040b070 (its result is field-read in-window in FUN_006c3f50); the 20 IDENTIFIED_NOT_ANALYZED callers; registry population path — each needs a new bounded contract.

## Package file paths (all created this run)

- `PREREGISTRATION.md`
- `CALLER_CENSUS.json`
- `01_RAW\S1_REPIN_RAW_CENSUS.json`
- `01_RAW\C2_SUBJECT_REPINS.json`
- `01_RAW\CENSUS_AGREEMENT.json`
- `01_RAW\CALLSITE_CONTEXTS.json`
- `01_RAW\ID_TABLE_DUMPS.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_00_00511070.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_01_006BAA20.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_02_00733490.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_03_006C26B0.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_04_006C2700.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_05_006C2750.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_06_006C27A0.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_07_006C27F0.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_08_006C3F50.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_09_00567170.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_10_006C2840.json`
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_11_006C2870.json`
- `FINAL_REPORT.md`
- `HANDOFF.md`
- `EVIDENCE_INDEX.md`

SCRATCH (local-only, outside the package):
`D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\SCRATCH\`
(scripts\, logs\, ghidra_out\, 01_RAW\S1 working copy, HISTORICAL_BASELINE_BEFORE.txt).
No MANIFEST (persistence phase is the orchestrator's). No commit, no push; no
docs\audits\AUDIT_ENTRYPOINT.md exists and no entrypoint row was created
(persistence pending) — the repo-root AUDIT_ENTRYPOINT.md is untouched.
