# DRAFT FINAL REPORT — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction (science phase). STATIC_ONLY — the client never ran.
This is the executor's DRAFT report for the fresh QC child and the PE-MASTER
audit; persistence-phase artifacts (FINAL_REPORT.md, HANDOFF.md,
PE_MASTER_REVIEW.md, MANIFEST_SHA256.csv, AUDIT_ENTRYPOINT row, commit/push)
are NOT this executor's work.

```text
RUN_ID = PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
RUN_TYPE = BOUNDED_STATIC_LANDMARK_CALLSITE_TRACE
RUN_CLASS = LOAD_BEARING
PRIMARY_TARGET = PCG_9_3_5 / Entropia Universe 9.3.5
MILESTONE = EU935-M1 — OPEN
BASE_SHA = a4992788982f8ff7f59866fa46aad1176897c69d (verified: HEAD == origin/master == live remote at preflight; re-verified below)
INPUT_BUILD_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
MODE = STATIC_ONLY
CANONICAL_GATE_EFFECT = NONE
```

---

## PART A — THE 18 REQUIRED ANSWERS (contract §28)

**1. Czy 0x0059AB12 naprawdę zawiera PUSH 4057?**
TAK. Physical bytes at the mapped file offset 1,682,194 (section .text, RVA
0x0019AB12, image base 0x00400000, ASLR off): `68 D9 0F 00 00` = PUSH imm32
0x00000FD9 = 4057. Own PE mapper calibrated on two independent canon anchors
before reading (01_RAW/RAW_BYTE_PINS.json); Ghidra's independent listing shows
`PUSH 0xfd9`; the whole containing-function listing is byte-identical to the
physical EXE 951/951.

**2. Czy ten 4057 jest argumentem do konkretnego calla?**
TAK. It is the sole stack argument (arg1) of the thiscall `CALL 0x008dfcd0`
@0x0059AB1E, with `this = LEA ECX,[ESP+0xC8]` (a stack-local UI object of the
containing function), callee cleanup `RET 4` @0x008DFD61.

**3. Jaka jest jego dokładna rola ABI/dataflow?**
thiscall arg1 of `this->FUN_008DFCD0(4057)`. Inside FUN_008DFCD0: 4057 is
re-pushed @0x008DFD0E as arg2 of `singleton->FUN_00821BB0(&out_str, 4057,
&struct12)` (the 0x1C string-table singleton @DAT_00BA124C from lazy getter
FUN_00414170 — plain RET, args belong to the next call); inside FUN_00821BB0 it
becomes arg2 of `FUN_00821760(0, 4057, &out)`; terminal use: the second element
of the composite map key {section_object, 4057} resolved by
mgr->FUN_00823C10 (0x98-manager singleton @DAT_00BA12F4) through the GENERIC
STL RB-tree mapfind FUN_004D1430 on the manager's own map; the resolved string
is stored on the caller object via `this->FUN_008DFB70(&str)` @0x008DFD2C
(ArkUI::Component-family store; temp vtable 0x00A7A948 store @0x008DFBD0).
Every step VA+bytes+source+destination: 02_ANALYSIS/CALLSITE_DATAFLOW.md §3.

**4. Czy dochodzi do proven template-id consumer?**
NIE. The mandatory falsifier FIRED. Reach-check over all 18 measured functions
against the fixed canon machinery VA set: ZERO calls to FUN_0072F580,
FUN_0043A550, FUN_0072FA30, FUN_00730C90, FUN_007CE1E0, FUN_006C3F50,
FUN_008BD720 anywhere on the path. The single machinery-adjacent call is
FUN_004D1430 (generic STL mapfind) inside FUN_00823C10 @0x00823C57 — on a
different singleton, a composite key, string values; NOT the template registry
(01_RAW/FALSIFIER_REACH_CHECK.json; TEMPLATE_ROLE_TEST.md).

**5. Czy immediate 4057 jest semantycznie template id?**
NIE — REJECTED_FOR_THIS_CALLSITE. At this call-site 4057 is a sids.vfs
string-table entry id. The string-table singleton is initialized from the
physical file "parameters\sids.vfs" (FUN_00821FB0) and parses
u16 count + count x (string, u32 id) (FUN_00821E70); the payload closes exactly
with 3,887 entries and id 0xFD9 = `S_REPAIR_UI_CLEAR_TOOLTIP` (R1 data nuance,
QC-confirmed — 04_QC: the first payload entry is an empty string with id 2021;
the layout still closes exactly with 3,887 entries)
(01_RAW/SIDS_ENTRY_PARSE.json; code side 01_RAW/G4/G5/G6). The containing
function FUN_00599D30 builds the ArkRepairUI (sole caller FUN_0059BE70 is
RTTI-gated on ArkRepairUI_Impl), pushing the consecutive series
0xFD4..0xFD9 = the six S_REPAIR_UI_*_TOOLTIP sids. The numeric equality with
templates.vfs id2=4057 is a cross-subsystem coincidence: only 2 of the 6 series
members (0xFD6, 0xFD9) exist as templates id2.

**6. Czy template 4057 fizycznie mapuje się do A=218757?**
Data-side TAK (record CONFIRMED: file offset 88,792, size 28, ver 1, CRC match,
{id2=4057, A=218757, B=218758, C=0, D_u32=1101664040/f32 21.2574, lists 0/0,
f11=0}) — but this mapping is NOT connected to VA 0x0059AB12 by any code path
measured. The call-site never reads the template registry.

**7. Czy 218757.nif jest obecny w Models.bnt index?**
TAK — PRESENT @name_file_offset 395,283,797 (calibrations reproduced:
index_start 395,262,727; count 5,596; anchor 296445.nif @395,268,773;
01_RAW/RESOURCE_INDEX_PINS.json).

**8. Czy B=218758 i 218758.bvi są potwierdzone?**
B=218758 CONFIRMED from the record payload; "218758.bvi" PRESENT in Volumes.bnt
@3,712,726 (calibration "296446.bvi" @3,701,937; index_start 3,696,320; count
1,865). Index presence only; no collision semantics claimed.

**9. Czy ten path wykonuje tylko resource request, czy tworzy concrete runtime instance?**
Ani jedno, ani drugie w sensie model/resource: the path resolves a STRING from
the sids.vfs string table and stores it on a UI component. No {0x66,A} request,
no model provider, no runtime NIF open, no instance creator for 218757 appears
anywhere on the path. (MODEL_218757_RESOURCE_REQUEST = NOT_ESTABLISHED.)

**10. Jeżeli instance istnieje — jaka jest jej identity?**
No landmark instance exists on the path. The measured objects are UI-side and
are documented as observed operations only (02_ANALYSIS/OBJECT_IDENTITY_TRACE.md):
the ArkRepairUI stack-local owner, the two string-table singletons, and the
ArkUI::Component-family temp receiving the string. No world instance, no
construction→transform identity chain.

**11. Skąd bierze transform?**
There is no transform on this path. No transform producer exists to classify;
WORLD_TRANSFORM_SOURCE = UNKNOWN (and not applicable to this UI path).

**12. Czy transform ma independently proven spatial semantics?**
Nie — no spatial semantics and no float triples exist anywhere on the 18
measured functions (integer ids, pointers, strings only). E10 discipline
applied; nothing was promoted from data shape.

**13. Czy jest połączony z tą samą instancją?**
Not applicable — no transform and no landmark instance. The VALUE-identity
chain of 4057 is continuity-verified end-to-end (step table in
CALLSITE_DATAFLOW.md §3).

**14. Czy dochodzi do scene/world structure?**
NIE — no scene/world edge. The terminal store writes into an ArkUI::Component
UI container (no NiNode/AttachChild/UpdateWorldData/scene-root shape in any
measured function; CONTROL-5 in NEGATIVE_CONTROLS.md).

**15. Czy XYZ zostało odzyskane?**
NIE. PLACEMENT_XYZ_RECOVERED = NO; X/Y/Z = UNKNOWN; no coordinates exist on
the path.

**16. Jaka jest rola 886?**
Mechanically established (same call sequence, needed for 4057's value-class
determination): PUSH 0x376 @0x0059AB37 → arg1 of `this->FUN_008F0780(886)`
(call @0x0059AB46, this = EAX from FUN_008E7B80) → identical
singleton→FUN_00821BB0→FUN_00821760 resolution chain → store via
`this->FUN_008F01C0(&str)`. Data side: sids.vfs entry id 0x376 =
`S_GENERIC_CLEAR`. Its FINAL semantic label beyond the measured mechanics
remains UNKNOWN; no zone/instance/location/class/variant guess was made.

**17. Jaki LANDMARK_TRACE_LEVEL osiągnięto?**
**LANDMARK_TRACE_LEVEL = 0** (falsified/unresolved: the 4057 immediate exists
and its template-numeric counterpart exists in templates.vfs, but the
call-site is NOT related to template 4057; the template bridge was never
established). MANDATORY_FALSIFIER_RESULT = FAIL_NUMERIC_COINCIDENCE. STOP
CONDITION S2 FIRED.

**18. Co pozostało UNKNOWN?**
See 02_ANALYSIS/NOT_CHECKED.md (N-01..N-16): the landmark placement question as
a whole (this call-site cannot answer it); other 4057 call-sites (not searched
— contract §9/§31); the sids section/localization display layer beyond the
identifier string; the composite-key part-1 semantics; the [ESP+0xC8] owner's
exact class; independent RTTI chain walks by the executor (labels are Ghidra RTTI readings;
R1 note: QC's independent walks CONFIRM the chain-walk facts — 04_QC Q6;
behavioral identity not upgraded);
the 0x008D-0x008F family beyond measured callees; whether model 218757 is a
static building anywhere (untouched; the human recollection remains
HUMAN_HISTORICAL_RECOLLECTION, probe-selection only).

---

## PART B — BUDGET LEDGER (contract §6; preregistered in 00_CONTROL/RUN_BUDGET.md BEFORE science)

```text
                              PLANNED   USED (final)
EXECUTOR_TOOL_CALLS            120      84  (self-counted per tool invocation;
                                            includes preflight, canon reads,
                                            all writes/bash/glob/grep/skill loads)
EXECUTOR_WALL_MINUTES          180      ~130 (self-reported session clock;
                                            declared-not-machine-measured)
NEW_PCG_FUNCTIONS_DETAILED       60      18  (FUN_00599d30 + g2 x5 + g3 x5 +
                                            g4 x2 + g5 x4 + g6 x1; see
                                            NOT_CHECKED.md)
NEW_PHYSICAL_RECORDS_DETAILED    2      2   (templates record 4057; sids.vfs payload
                                            + entry 4057; 4508 was calibration re-pin)
NEW_MODEL_RESOURCE_INDEX_RECORDS 4      4   (2 calibration + 2 target names)
NEW_GAMEBRYO_ORACLE_MECHANISMS   0      0   (existing canon context only)
QC_BUDGET                       —      (fresh QC child's own budget; not consumed
                                            by this executor)
QC_REPAIR_ROUNDS_MAX            1      0 consumed by executor (QC child's call)
RESULT = FULL COVERAGE of the authorized question; no limit exceeded; no
STOP-by-budget fired (S5 not reached). STOP S2 fired (science-branch terminal).
```

## PART C — SELF-CHECK (executor's own; explicitly NOT an independent audit)

```text
1. PREFLIGHT re-verified below (Part D): BASE_SHA match; clean tree; 5 foreign
   untracked groups untouched; all four input hashes match the pins.
2. Phase order honored: budget preregistered (mtime/content in 00_CONTROL)
   before Phase 1; Phase 1 before Phase 2; Phases 6-11 NOT executed after the
   Phase-5 falsifier (S2); 886 treated only mechanically within the same
   sequence.
3. Every load-bearing raw pin carries VA/offset/bytes/measured-quantity/tool/
   provenance/failure-case metadata (01_RAW provenance blocks; contract §26).
4. Byte integrity: 951/951 listing instructions vs physical EXE (own mapper,
   no Ghidra on the verification side); Ghidra Jython signed-byte artifact
   fixed + documented (RETRACTIONS R-4).
5. Calibrations before trust: VFS walker (5,438/0-CRC/EOF + record 4508
   anchor), BNT2 parsers (index_start/count/anchor), PE mapper (2 canon
   anchors), sids layout (exact closure + count).
6. Full raw census of the measured set committed in 01_RAW (no
   console-only load-bearing results; all scripts committed in 03_SCRIPTS with
   SCRIPT_SHA256.csv hash ledger, hash-after-final-edit discipline).
7. Negative controls 1-5 executed (NEGATIVE_CONTROLS.md); the negative result
   is reported as the run's value (contract §31) with no rescue attempt.
8. Era discipline: PCG 9.3.5 paths only; 2003-era corpus untouched.
9. No git state created (verified in Part D); proprietary payloads LOCAL_ONLY
   (sandbox EXE copy + Ghidra project live OUTSIDE the repo; only identity
   metadata, hashes, offsets, bounded byte windows, scripts, reports entered
   the repo).
10. Known limitations (honest): Ghidra decompiler argument displays for
   untyped callees are mangled in places — the ASM listings are the authority
   and all interpretations were cross-checked against them; wall-minute counts
   are self-reported; the "ArkUI::Component"/"ArkRepairUI" class labels are
   Ghidra RTTI-analyzer readings of binary RTTI symbols (STRONGLY_SUPPORTED,
   not independently chain-walked — NOT_CHECKED N-07; R1: QC's independent chain walks CONFIRM the chain-walk facts — 04_QC Q6; behavioral identity not upgraded).
```

## PART D — PREFLIGHT RE-VERIFICATION (final)

Re-verified at end of the science phase:

```text
git rev-parse HEAD          : (see Part E verification line — unchanged
                             through all phases; no commit/stage/push performed
                             by this executor)
git status --porcelain      : tracked modifications/staged = 0; the only
                             untracked additions are THIS package
                             (docs/audits/PE_935_STATIC_LANDMARK_4057_CALLSITE_
                             TRACE_R1_20261003/) plus the 5 known foreign
                             untracked groups (untouched)
INPUT HASHES                : all four re-pinned at preflight (Part E of
                             00_CONTROL/PREFLIGHT.md); EXE additionally
                             re-verified byte-level by the 951/951 crosscheck
```

## PART E — REQUIRED FINAL STATUS BLOCK (contract §29, filled with measured values)

```text
RUN_ID =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

BASE_SHA =
a4992788982f8ff7f59866fa46aad1176897c69d

INPUT_BUILD_SHA256 =
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31

TEMPLATE_4057_REPIN =
CONFIRMED

TEMPLATE_4057_A =
218757

TEMPLATE_4057_B =
218758

MODEL_INDEX_218757 =
PRESENT

COLLISION_INDEX_218758 =
PRESENT

IMMEDIATE_4057_RAW_PIN =
CONFIRMED

IMMEDIATE_4057_AT_0x0059AB12 =
CONFIRMED

IMMEDIATE_4057_IS_TEMPLATE_ID =
REJECTED_FOR_THIS_CALLSITE

HARDCODED_TEMPLATE_REFERENCE_4057 =
NOT_ESTABLISHED

IMMEDIATE_4057_TO_MODEL_218757 =
NOT_ESTABLISHED

MODEL_218757_RESOURCE_REQUEST =
NOT_ESTABLISHED

RUNTIME_NIF_OPEN_218757 =
NOT_ESTABLISHED

CONCRETE_RUNTIME_INSTANCE =
NOT_ESTABLISHED

STATIC_BUILDING_INSTANCE =
UNVERIFIED

WORLD_TRANSFORM_SOURCE =
UNKNOWN

TRANSFORM_SEMANTIC_ROLE =
UNVERIFIED

INSTANCE_TO_SCENE_EDGE =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO

PLACEMENT_X =
UNKNOWN

PLACEMENT_Y =
UNKNOWN

PLACEMENT_Z =
UNKNOWN

ROTATION_RECOVERED =
NO

IMMEDIATE_886_SEMANTIC_ROLE =
MECHANICALLY_SIDS_STRING_TABLE_ENTRY_ID_S_GENERIC_CLEAR (PUSH 0x376 @0x0059AB37 ->
FUN_008F0780 -> store FUN_008F01C0; same resolution chain as 4057); deeper
semantics UNKNOWN

LANDMARK_TRACE_LEVEL =
0

MANDATORY_FALSIFIER_RESULT =
FAIL_NUMERIC_COINCIDENCE

PRIOR_RESULT_LEVEL =
B (UNCHANGED)

CANONICAL_GATE_EFFECT =
NONE

M1_CLOSED =
NO

M2_AUTHORIZED =
NO

M3_AUTHORIZED =
NO

NEXT_EXPERIMENT_AUTHORIZED =
NO
```
