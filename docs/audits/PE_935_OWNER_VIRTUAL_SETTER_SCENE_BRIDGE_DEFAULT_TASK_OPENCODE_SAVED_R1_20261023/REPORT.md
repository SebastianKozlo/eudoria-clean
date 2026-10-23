# REPORT — OWNER VIRTUAL SETTER / SCENE BRIDGE (DEFAULT/MEDIUM, NATIVE TASK)
RUN_ID=PE_935_OWNER_VIRTUAL_SETTER_SCENE_BRIDGE_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023
ERA=PE_EU_9_3_5_SAVED_ONLY (saved evidence only; no original EXE/assets access, no runtime, no new Ghidra exports)
TASK_ACTUAL_COUNT = 10

## Verdicts
SCIENCE_VERDICT = PARTIAL_PASS (VT+0xC chain closed conditionally; VT+4 setter side remains data-barred; receiver identity not established)
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT (INC-QC-OVERRUN-1: QSCIENCE 381 vs 320 cap; INC-PROMPT-DECIMAL-1: master prompt decimal defect; both disclosed, no evidence defect)
EVIDENCE_INTEGRITY = SEALED (see MANIFEST_SHA256.csv; INPUT_RECHECK machine result)
PUBLICATION = sanitized projection published; publication is transport, not canon acceptance
CANONICAL_GATE_EFFECT = NONE
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION (no human Q1 PASS recorded; new findings reported for external postaudit)

## Science results (all era PE_EU_9_3_5_SAVED_ONLY; full claims with confidence/scope/QC in CLAIMS.json)
1. SAVED SLOT DATA (S01, CONFIRMED): VTABLE_INVENTORY.csv (saved projection, sha EFBA7978..., calibrated in-corpus against pinned GA3 by exact ArkPortalCellGraph slot3 join and slot_count<4=>slot3=0 rule) holds literal VT+0xC cell values: base table 0x00A91E4C (.?AVMovableObject@@, col 0x00AB33D0, 13 slots) cell 0xA91E58 = 0x0085B6A0; derived table 0x00A7DCB0 (.?AVClientMovableObject@@, col 0x00AA17CC, 13 slots) cell 0xA7DCBC = 0x005278A0. VT+4 cells (0xA7DCB4/0xA91E50): DATA_BARRIER — zero literal occurrences in 22 searched files, all representation forms (bounded negative, denominators in S01 RESULT s3).
2. RECEIVER LINKAGE (S01+QSCIENCE C7, STRONGLY_SUPPORTED negative): receiver B (EDI) of 0085B3E0's calls is NOT linked to either table in the searched space; no vptr install inside 0085b3e0..0085b5d6. Both tables remain CONDITIONAL FAMILY CANDIDATES; no promotion from ctor-installs of other instances.
3. ACTUAL SLOT TARGETS (V01/V01D/V02, CONFIRMED mechanically, conditional on linkage): base VT+0xC target 0085B6A0 is a virtual out-vector method (thiscall, out-pointer arg, RET 0x4, EAX=out-ptr) emitting (0.0, 0.0, z), z = min(00861320([this+0x10]), const@0x00A81D40) — const is UPPER bound (corrected per QC F1); type gate [this+8] in {3,4,5,6,7}; D==NULL path emits (0,0,const). Derived 005278A0 gates on dword [this+0xBC] + byte [this+0xB0], then copies global 12-byte triple 0x00BA921C/20/24 or delegates to base. 00861320 = FLD dword [ECX+0x40]; RET — pure ST0 getter; X=[D+4] NOT read. Z value source = float at [[B+0x10]+0x40] (conditional chain); its writer was NOT found.
4. CALLER BINDING (V01, STRONGLY_SUPPORTED): consistent necessary-condition match (one dword push, 3-float FLD/FADD consumption, receiver EDI); ABI-compatible alternatives NOT excluded — consistency is not identity proof.
5. EMPTY-BUCKET BRANCH (M01, CONFIRMED): 00854E11 = create-first-entry path: opaque 00851610 (ECX=this-map, args &arg2_slot/EDX-unknown/arg2), node from [EAX], out-pair {node, flag=1}; no direct node-field writes; no visible count increment. Payload window: EAX=[found+0x8] hit / 0 miss, RET 0x4. Key caller 004C484E..004C4863: key = opaque 004154f0([ESP+0x10]) + pre-window stack arg; equality to [B+0x74] NOT_PROVEN_IN_PACKET; result stored to [ESI] at 0x004C4861. All five same-owner premises remain OPEN.
6. HELPER 0085B190 (L01, CONFIRMED): null-safe acquire wrapper (ECX=[recv+4], JMP 00413440), ZERO writes — writer candidate REJECTED; caller receiver = [found+0x8]; no deallocator chain developed.
7. GAMEBRYO REFERENCE (G01, ENGINEERING REFERENCE ONLY): against pinned SDK 1.2.2.6 (11/11 SHA PASS, 783/800 source lines), the anchor pattern most resembles PROPAGATE_WORLD of the six classes; reference analogy only, no PE identity/slot/offset transfer; type-gate {3..7} has no pinned-SDK counterpart (certainty capped INSUFFICIENT_DATA beyond closest-of-six).
8. WRITER/SOURCE STATUS: WRITER_OBSERVED=NO for R/D/X and the VT+4 setter effect; indirect callee effects remain UNKNOWN (OFL-A01 standing). FIRST_MISSING_EDGE = receiver-B dynamic-type -> actual vtable -> VT+4 cell -> setter body -> store/out-value (see FIRST_MISSING_EDGE.json).

## Standing baseline (unchanged)
WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN. OFL-A01..A06 accepted additively into CORRECTION_LEDGER.json; no historical building placement claimed.

## Process, QC and accounting
- Native Task discipline: 10 tasks (8 workers + 2 fresh auditors), depth 1, zero grandchildren, max 2 active, all prompt parity PASS, all finishes stop (census from read-only DB in NATIVE_TASK_CENSUS.json; terminal_consistency PASS).
- QSCIENCE (fresh pe-master-auditor): QC_PARTIAL — C1..C7 PASS as worded; findings F1 (P1 clamp direction) F2/F3/F4 (P2) corrected by bounded R1 run with independent re-derivation; F5 = QC's own 381>320 exposure cap overrun recorded as INCIDENT (process violation stands even after disclosure).
- Accounting: see BODY_AND_BUDGET_LEDGER.json (packet metrics separate from exposure totals; LOW_BOUND never promoted to exact bound); UNMEASURED: REQUEST_EFFORT=NOT_OBSERVED, SERVER_EFFECTIVE_EFFORT=UNKNOWN.
- Incidents: INC-QC-OVERRUN-1 (P2), INC-PROMPT-DECIMAL-1 (P3; wrong decimal in master's S01 prompt, caught and corrected by worker).
- Events: SOURCE_ADMISSION_EVENTS.jsonl (append-only, tool-written seq/utc); ADMIT before semantic reads; extraction mechanical without display.

## Coverage / NOT checked
Opened: the five packets' ranges (00854DC4:00854F00, 008544F1:00854519, 004C484E:004C4863, 0085B6A0:0085B7EF, 0085B440:0085B4A0, 005278A0:00527A00, 0085B190:0085B1AF, 00854520:00854564, 00861320:00861400) + 22 saved representations + 11 SDK files. NOT opened: opaque callees (00851610, 00854260, 00413450, 004154f0, 00861330, 00861360, 00861390-continuation, 00413440, 00976770, 0040b980, 008542a0, 004134f0, 0085c330, 00734230/50/70), 00856090/00971780 (per contract), 004C48D4 miss branch, consts' values, VTABLE_INVENTORY.csv generating script, model reasoning, original EXE (prohibited). Negative claims are bounded to enumerated search spaces.

## Terminal
SCIENCE_STOP recorded before seal; census + terminal consistency + INPUT_RECHECK + validate_active_artifacts before seal; sanitized publication per PUBLICATION_ALLOWLIST; PUBLICATION_RESULT.json canonical receipt in RECEIPT_ROOT. No new experiment after this report. HARD STOP.
