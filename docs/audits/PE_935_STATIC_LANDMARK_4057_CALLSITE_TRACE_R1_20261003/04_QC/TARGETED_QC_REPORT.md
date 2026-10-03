# TARGETED QC REPORT — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

```text
RUN_ID            = PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
QC_MODE           = FRESH_TARGETED_INTERNAL_QC (fresh context, NO_NESTED_TASKS)
QC_EXECUTOR       = pe-master-auditor child (independent of the science executor)
PACKAGE_UNDER_QC  = docs/audits/PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003/ (64 files)
BASE_SHA (parent pin) = a4992788982f8ff7f59866fa46aad1176897c69d
QC_DATE          = 2026-10-03
```

## 0. QC BUDGET (preregistered in-session before measurements; contract §6)

```text
FRESH_QC_MAX_TOOL_CALLS = 80   PLANNED ~35-45   USED 52
FRESH_QC_MAX_WALL_MINUTES = 120  PLANNED ~90-110  USED ~85 (session clock; self-reported)
Method: own PE parser (pure struct), own whole-.text call/immediate/absolute-ref
censuses, own byte dumps at every load-bearing VA, own independent VFS/BNT walkers
(byte-derived stride rule), own sids payload parser, own RTTI chain walks, own
hash recomputation. Executor scripts were NEVER used as oracles; s1's stride rule
was read ONLY as a format-knowledge guide and then re-derived and re-validated
from raw bytes (see Q2). Ghidra was not used by the QC.
```

## 1. VERDICT SUMMARY

```text
QC_VERDICT = QC_PASS_WITH_FINDINGS
(1x P2 evidence-indexing defect; 5x P3 documentation/hygiene defects;
 ZERO P0/P1; every load-bearing science claim independently CONFIRMED
 from raw bytes / own measurements)
```

**Central result of this QC**: the executor's mandatory falsifier — immediate 4057
@0x0059AB12 does NOT reach FUN_0072F580 or any proven template-id consumer — is
**SUPPORTED** by my fully independent, byte-level, whole-.text census. The
data-side repins (templates.vfs record 4057 {A=218757, B=218758}; 218757.nif and
218758.bvi index presence) are **SUPPORTED** by my own walkers and full-file
searches. The negative result is cleanly reported with no success theater.

---

## 2. Q1..Q16 — INDEPENDENT VERIFICATION (each from MY OWN measurement)

### Q1 — Input EXE identity: **CONFIRMED (mine)**
My `Get-FileHash`: Entropia.exe 8,015,872 B, SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 = pin.
All 4 pinned inputs re-hashed by me and match (templates.vfs BE57818C...,
Models.bnt C950A8C2..., Volumes.bnt 6AD8BA3C...). sids.vfs own identity
recorded: 129,040 B, SHA256 D58EF1D2E49FD52C093AA37E8FAE4A2653A163728DDAE5204
8B40512CFF0FB6E. My own PE parse: IMAGE_BASE 0x00400000, DllCharacteristics
0x0000 (ASLR OFF), 5 sections; section table matches RAW_BYTE_PINS.json
field-for-field (my values: .text RVA 0x1000/VSZ 0x6735E5/RSZ 0x674000,
.rdata 0x675000/0xF6569/0xF7000, .data 0x76C000/0x3D6E4/0x34000, .tls,
.rsrc). Era discipline: only pcg_install paths touched by me; 2003 corpus not opened.

### Q2 — Physical templates.vfs record id2=4057: **CONFIRMED (mine)**
My own walker (04_QC/raw/qc4_final_walks.py): magic "ArkVFS02"; container
header = magic[8] + u32 base=36 (@8) + u32 (@12); records from offset 16;
record header {u32 id, u32 size, u32 ver, u32 crc32} 16 B; **advance =
ceil((16+size)/base)*base** — I derived this rule from raw bytes myself
(observed advances: 72/180/576 for size 28/130/536; my first walk with a
wrong 72-constant desynced @175,480, the byte-derived base-36 rule closed
the file exactly — a real falsification-and-correction cycle, recorded in
qc3/qc4 outputs). Results: **5,438 records, end_pos=560,788 = EOF EXACT,
0 CRC32 failures (zlib.crc32 recomputed by me on ALL 5,438 payloads),
5,438 unique ids, no duplicates** — all walk-census claims confirmed.
Record 4057: offset **88,792** (= claim), size 28, ver 1, crc field
0x79E7AC62 == my recomputation; payload hex `d9 0f 00 00 85 56 03 00 86 56
03 00 00 00 00 00 28 0f aa 41 00 00 00 00 00 00 00 00`. Calibration record
4508 @96,496: {id2=4508, A=296445, B=296446} ✓. Record 11963 @315,916
size 382, list1_count u16@payload+20 = 16 ✓.

### Q3 — A/B mapping from MY parse: **CONFIRMED (mine)**
From my qc4 walker output (not the executor's JSON): payload+4 = 85 56 03 00
= **A=218757**; payload+8 = 86 56 03 00 = **B=218758**; C=0 @+12;
D_u32=1101664040 @+16 (f32 21.257400512695312); l1=0, l2/f11=0. All equal
the executor's claims.

### Q4 — Index presence: **CONFIRMED (mine)**
My full-file binary searches (chunked, 04_QC/raw/qc2 PART D3):
Models.bnt `"218757.nif"` → **exactly 1 hit @395,283,797** (= claim);
calibration `"296445.nif"` → 1 hit @395,268,773 ✓. Volumes.bnt
`"218758.bvi"` → **1 hit @3,712,726** (= claim); calibration `"296446.bvi"`
→ 1 hit @3,701,937 ✓. Index headers byte-verified by me: u32 @395,262,727 =
**5,596** (= claimed count); u32 @3,696,320 = **1,865** (= claimed count);
entry shape (name+\x0A+offset+hash) consistent. No NIF/BVI payload decoded
(bounded, as authorized).

### Q5 — Raw immediate at 0x0059AB12: **CONFIRMED (mine)**
My own VA→offset mapper (built from my own section table): RVA 0x19AB12 →
file offset **1,682,194**, section **.text** (= claims). Bytes at anchor:
**`68 D9 0F 00 00` = PUSH imm32 0x00000FD9 = 4057** ✓. Instruction boundary:
the preceding instruction is `E8 DE 48 34 00` (CALL → 0x008DF3F0, target
recomputed by me) at 0x0059AB0D, ending EXACTLY at 0x0059AB12 ✓. Following:
`8D 8C 24 C8 00 00 00` (LEA ECX,[ESP+0xC8]) @0x0059AB17 + `E8 AD 51 34 00`
(CALL → 0x008DFCD0) @0x0059AB1E. Mapper calibrations also reproduced by me:
VA 0x00A86D30 → file 6,843,696 = "Parameters\templates.vfs" (my own string
search found exactly 1 site @file 0x686D30 ✓). The claimed
preceding_16B/following_16B in RAW_BYTE_PINS.json are byte-identical to my dump.

### Q6 — Containing function boundaries, single caller, RTTI gate: **CONFIRMED (mine)**
- Entry **0x00599D30**: prologue `6A FF 68 26 26 9D 00 64 A1 ... 81 EC 08 01
  00 00` (SEH frame setup) at 0x00599D30; preceded by the previous function's
  RET (C3 @0x00599D21) + CC padding (0x00599D22..0x00599D2F) ✓ prologue/padding
  boundary rule satisfied.
- End **0x0059AC88**: my bytes: POP EBP/EBX, ADD ESP,0x114, **RET (C3) AT
  0x0059AC88**, CC padding 0x0059AC89..0x0059AC8F, next function prologue
  @0x0059AC90 ✓. Body [0x00599D30..0x0059AC88] inclusive-of-RET = **3,929 B**
  (= claim; end-inclusive convention is byte-consistent).
- 951-instruction claim: plausibility only (3,929 B/951 ≈ 4.13 B/instr; my
  byte-level E8 census in the body = 182 sites ≥ 170 claimed direct calls;
  65 unique computed targets ≥ 49 claimed unique — supersets with false
  positives, consistent). The full 951/951 listing crosscheck was NOT re-run
  by me (see §6 NOT_CHECKED); the boundary rule and every load-bearing window
  instruction were verified byte-level.
- Single caller: my whole-.text census (E8 recomputation): **exactly ONE**
  call site targeting 0x00599D30 = **0x0059BF11** (`E8 1A DE FF FF`, target
  recomputed = 0x00599D30 ✓); zero E9 tail-jumps ✓.
- Caller RTTI gate (my bytes): FUN_0059BE70: PUSH 0x411 @0x0059BEB3;
  `C7 44 24 08 04 07 A8 00` @0x0059BEC7 (store of vtable **0x00A80704** in
  unwind local); gate @0x0059BEF2..0x0059BF0A: MOV EDX,[EAX] (vtable);
  MOV ECX,EAX; **MOV EAX,[EDX+0x64]** (vtable slot +100 ✓ decompile's "+100");
  **PUSH 0x00B7DDE8** (TypeDescriptor); CALL EAX (virtual type fetch); MOV
  ECX,EAX; `FF 15 20 53 A7 00` (type_info::operator!=); TEST AL,AL; **JNZ
  skips** the block; fall-through → CALL FUN_00599D30 @0x0059BF11 ✓.
- **My independent RTTI chain walks** (qc2/qc5): TD @0x00B7DDE8 name =
  **".PAVArkRepairUI_Impl@@"** (pointer-form TypeDescriptor of
  ArkRepairUI_Impl; vftable_ptr 0x00A98110, spare 0); vtable 0x00A80704 →
  COL @0x00AA276C → TD @0x00B7DED8 → **".?AVArkRepairUI@@"**. The
  "RTTI-gated ArkRepairUI_Impl path" claim is CONFIRMED beyond the
  package's own conservative Ghidra-label scope (package said
  STRONGLY_SUPPORTED / N-07 not chain-walked — my walk closes it).

### Q7 — Exact argument/dataflow role of 4057: **CONFIRMED (mine, every link)**
All 12 claimed call links recomputed from my own byte dumps (qc1 §S7 link
table: 12/12 MATCH): PUSH 4057 @0x0059AB12 → sole stack arg of thiscall
`this->FUN_008DFCD0(4057)` (this = LEA ECX,[ESP+0xC8]; callee cleanup
**RET 4 @0x008DFD61** ✓ = 1 stack arg) → inside: MOV ECX,[ESP+0x40]
@0x008DFD05; PUSH EAX @0x008DFD0D (&struct, arg3); **PUSH ECX @0x008DFD0E
(re-push 4057, arg2)**; PUSH EDX @0x008DFD13 (&out, arg1); CALL
FUN_00414170 @0x008DFD18 (**lazy getter byte-verified**: MOV EAX,
[0x00BA124C] @0x00414192; PUSH 0x1C + new-thunk 0x0095D3C4; ctor
FUN_008221C0 @0x004141B6; store @0x004141BB — plain-RET getter, pushed
args remain for the next call ✓); MOV ECX,EAX; CALL FUN_00821BB0
@0x008DFD1F (RET 0xC = 3 args) → inside: MOV ECX,[ESP+0x50] @0x00821C23
(4057 again); PUSH EAX/PUSH ECX/PUSH 0 → CALL FUN_00821760(0, 4057, &out)
@0x00821C31 → inside: CALL FUN_00826A50 @0x008217CE (key part 1; body
`8B 44 24 04 8B 04 85 54 59 B9 00 C3` = table[4*param] @0x00B95954 ✓);
CALL FUN_00415670 @0x008217F3 (**mgr getter byte-verified**: MOV EAX,
[0x00BA12F4] @0x00415692; PUSH 0x98; ctor FUN_00824C70 @0x004156B9; store
@0x004156BE); MOV ECX,EAX; CALL FUN_00823C10 @0x008217FA → inside:
**LEA ESI,[EDI+4] @0x00823C4D (mgr's own map @[this+4])**; CALL
FUN_004D1430 @0x00823C57 (generic RB-tree mapfind; shape verified:
`8B 41 04 85 C0 ... 39 70 10 ...` classic tree walk); **LEA EDI,[EAX+0x14]
@0x00823C64 (value slot node+0x14)**; virtual dispatch on [EDI+0x24]
(`8B 4F 24; 8B 01; 8B 50 04; FF D2`) ✓ → back: PUSH EAX @0x008DFD24;
MOV ECX,ESI @0x008DFD25 (this = original object, ESI=ECX saved at entry);
**CALL FUN_008DFB70 @0x008DFD2C (string store)** → inside FUN_008DFB70:
**`C7 44 24 3C 48 A9 A7 00` @0x008DFBD0** (store of vtable 0x00A7A948
into the temp) ✓; my chain walk: 0x00A7A948 → COL @0x00A9EDD4 → TD
@0x00B6E084 → **".?AVComponent@ArkUI@@"** — the terminal store is an
ArkUI::Component-family store ✓. The 4057 VALUE is preserved unchanged
through the whole chain (immediate → [ESP+0x40] → ECX re-push → composite
key element); no wrapper, no transformation.

### Q8 — MANDATORY FALSIFIER: **CONFIRMED (mine) — the negative result stands**
(a) **Singleton identities from bytes**: my absolute-ref scan of .text:
0x00BA124C referenced ONLY at 0x00414192/0x004141BC/0x004141D3 (all inside
FUN_00414170, the string-table getter); 0x00BA12F4 ONLY at
0x00415692/0x004156BF/0x004156D6 (all inside FUN_00415670, the 0x98-mgr
getter); **registry singleton 0x00BA1824 found by MY OWN scan** —
referenced ONLY at 0x0043A572/0x0043A59C/0x0043A5B3 (all inside
FUN_0043A550, the registry getter; getter byte-verified: MOV EAX,
[0x00BA1824], PUSH 0x18, new, ctor, MOV [0x00BA1824],EAX). **Three
disjoint globals with disjoint reference sets** — "string-table manager is
NOT the registry singleton" byte-confirmed.
(b) **No machinery call anywhere on the measured path**: my whole-.text
byte-level census (E8 recomputation) of the full machinery VA set
{0x0072F580, 0x0043A550, 0x0072FA30, 0x00730C90, 0x007CE1E0, 0x006C3F50,
0x008BD720, 0x0072F8D0, 0x0072FE30, 0x004D1430, 0x006CB6F0} intersected
with ALL 18 measured-function windows (containing function at its
body-verified range + 17 chain functions with generous windows):
**machinery in-window hits total = EXACTLY 1: FUN_004D1430 @0x00823C57
inside FUN_00823C10** — precisely the single classified generic-mapfind
hit. ZERO registry_lookup / registry_getter / templates_reader /
template_parse / A_getter / request_pair_emitter / scheduler_callback /
rbtree_insert / template_list2_out / instance_creator hits. FUN_0072F580's
own bytes (my dump): thiscall (MOV ESI,ECX), calls FUN_004D1430 @0x0072F590
(the registry lookup also uses the generic mapfind — canon-consistent),
RET 4 (ABI claim consistent).
(c) **4057 terminates in a string store** ✓ (Q7 chain end-to-end; resolved
string → FUN_008DFB70 ArkUI::Component store).
(d) **Methodology check**: FALSIFIER_REACH_CHECK.json's machinery set =
fixed canon VAs (matches contract §12 ABI list) ✓; per-function direct-callee
scope is the contract's scope ✓; the artifact itself covers only 13 functions
(g1..g4 + containing; see FINDING P2-1) — the G5/G6 rows exist machine-readably
in G5_LOOKUP_CLOSURE.json (H03_extract_00823c10.template_machinery_direct_hits
= [{target: 0x004D1430, from: 0x00823C57}] — verified by my read) and
G6_SIDS_PARSER.json (empty hits for FUN_00821E70) ✓. Indirect calls (7
claimed in FUN_00599D30; my FF-call byte-shape census: 18 candidates ⊇ real)
do not carry the 4057 value — its path is the closed direct chain; no
completeness gap affecting the verdict. **My census closes the coverage
question at byte level for all 18 functions.**

### Q9 — 4057→A bridge claim: **NOT_ESTABLISHED — no overclaim (verified)**
CLAIM_MATRIX C4057-09 status "NOT_ESTABLISHED / coincidence CONFIRMED as
classification"; DRAFT Part E HARDCODED_TEMPLATE_REFERENCE_4057 =
NOT_ESTABLISHED, IMMEDIATE_4057_TO_MODEL_218757 = NOT_ESTABLISHED;
TEMPLATE_ROLE_TEST §6 keeps the data-side facts explicitly disconnected from
the call-site. No promotion anywhere. My evidence independently SUPPORTS
NOT_ESTABLISHED (no registry call on the path). The coincidence structure is
byte-confirmed on both sides: my id2 census 4052..4057 → only 4054 (0xFD6)
and 4057 (0xFD9) exist as templates id2, while ALL SIX 0xFD4..0xFD9 are sids
string ids (my sids parse) — 4 of 6 not templates id2 ✓.

### Q10 — Object identity claim: **NOT_ESTABLISHED — no overclaim (verified)**
OBJECT_IDENTITY_TRACE documents only measured UI-side objects as observed
operations (O1 stack-local owner, O2/O3 singletons, O4 temp); no
SAME_RUNTIME_OBJECT_IDENTITY / world-instance claim. O1's exact class honestly
NOT identified (N-08). O4's RTTI label independently chain-walk-verified by
me (see Q6). STATIC_BUILDING_INSTANCE = REJECTED_FOR_THIS_CALLSITE (scoped
negative, honest).

### Q11 — Transform source claim: **UNKNOWN — no overclaim (verified)**
WORLD_TRANSFORM_SOURCE = UNKNOWN; TRANSFORM_PROVENANCE.md: no transform
producer exists on the path (vacuous after falsifier, correctly reasoned);
nothing promoted.

### Q12 — Spatial-semantic/XYZ claim: **NO — no overclaim (verified)**
PLACEMENT_XYZ_RECOVERED = NO; X/Y/Z = UNKNOWN; ROTATION_RECOVERED = NO —
consistent across DRAFT Part E, CLAIM_MATRIX C4057-15, TRANSFORM_PROVENANCE.
No XYZ values stated as recovered anywhere in the package. My own immediate
census of FUN_00599D30 (49 unique imm32 values — ids, sizes, VAs, table
pointers) is consistent with "no float triples on the path".

### Q13 — Scene/world edge claim: **NOT_ESTABLISHED — no overclaim (verified)**
INSTANCE_TO_SCENE_EDGE = NOT_ESTABLISHED; CONTROL-5 executed as a shape
negative (no NiNode/AttachChild/UpdateWorldData shape in any measured
function — consistent with my dumps: the chain is STL-map + string + UI
vtable store).

### Q14 — Immediate 886: **CONFIRMED mechanically; semantic role honestly UNKNOWN (mine)**
(a) bytes @0x0059AB37 = **`68 76 03 00 00` = PUSH 0x376 = 886** ✓ (my read);
(b) chain from my bytes: MOV ECX,EAX @0x0059AB3C; CALL FUN_008F0780
@0x0059AB46 ✓; FUN_008F0780 body is **shape-identical to FUN_008DFCD0**
(MOV ECX,[ESP+0x40] @0x008F07B5; PUSH chain; CALL FUN_00414170 @0x008F07C8;
MOV ECX,EAX; CALL FUN_00821BB0 @0x008F07CF; PUSH EAX; MOV ECX,ESI; **CALL
FUN_008F01C0 @0x008F07DC**; RET 4 @0x008F0812) — same singleton →
FUN_00821BB0 → FUN_00821760 resolution chain ✓; (c) no overclaim: DRAFT
answer 16 + Part E keep the FINAL semantic label UNKNOWN ("no
zone/instance/location/class/variant guess") — contract §19-conformant
(the measured string-table id is a mechanical data fact, same treatment as
4057); (d) **sids entry 0x376 = "S_GENERIC_CLEAR" from MY OWN parse** ✓
(qc4: all 13 target entries MATCH, incl. 0xFD9 = S_REPAIR_UI_CLEAR_TOOLTIP).
Bonus context (mine): FUN_008F01C0's own RTTI gate TD = ".PAVArkUITextField@@"
— consistent with a UI field store; not claimed by the executor, no conflict.

### Q15 — Budget compliance: **PASS with one count defect (P3-2)**
RUN_BUDGET.md preregistration EXISTS (hard limits verbatim from contract §6,
phase plan P1-P11 + 886 rule + controls), written before science (declared);
phase ledger rows monotonic and consistent (19→23→31→33→45→48→70→78→84).
Final: 84/120 calls (self-counted), ~130/180 min (honestly labeled
"declared-not-machine-measured"), NEW_PCG_FUNCTIONS_DETAILED=**19**/60,
physical records 2/2, index records 4/4, Gamebryo 0/0, STOP S2 (not S5).
Package-internal consistency: **18** functions are actually enumerated
(18 G-decompile .c files; NOT_CHECKED.md's own enumeration lists 18 names
under the "19" heading) — off-by-one count (FINDING P3-2; limit 60 not
exceeded either way). The 2/2 physical records and 4/4 index records are
exactly the ones I independently confirmed (Q2-Q4). Absolute tool-call
counts are self-reported (not machine-verifiable by me — flagged honestly
by the executor). Note: the parent dispatch paraphrased "86/120"; the
package consistently says 84/120 (no package-internal inconsistency).

### Q16 — No unauthorized work: **PASS (mine)**
(a) STATIC_ONLY: my grep of all 17 committed scripts — **zero**
subprocess/os.system/Popen/socket/urllib/requests/http/win32/CreateProcess/
frida/ctypes primitives; no client launch, no dynamic instrumentation, no
network, no runtime capture anywhere in the package; Ghidra headless ran on
a hash-verified sandbox COPY outside the repo (static file analysis —
authorized by contract §0 "użycie Ghidry"). (b) No proprietary payloads in
the repo package: my 64-file census — all files are .md/.json/.csv/.py/.c
text artifacts; no .exe/.vfs/.bnt/.nif/.bvi binaries (largest file:
G1_FUNCTION_DUMP.json 193KB, a derived listing). (c) Git: HEAD =
**a4992788982f8ff7f59866fa46aad1176897c69d** = BASE_SHA (my rev-parse);
`git diff --cached` EMPTY (zero staged); the package is untracked-only
(64 ?? entries); the 5 known foreign untracked groups present and untouched
(FC1_P2_CLOSURE, NINODE_SLOT17, P1_CLOSURE, PLACEMENT_INSTANCE_RESOURCE_JOIN,
experiments/); HEAD commit = the pre-run PLACEMENT_BRIDGE_DESKTOP_CORRECTION
commit → zero commits/stages by the executor ✓.

---

## 3. ADDITIONAL PROJECT-STANDARD CHECKS

- **CLAIM_MATRIX.csv (C4057-01..16)**: all 16 rows present; all 10 required
  fields present in every row (claim_id, claim_text, status, source, method,
  independent_countercheck, why_non_circular, falsifier, failure_case_detected,
  blast_radius); statuses consistent with the raw evidence — every row's
  substance independently confirmed or honest-negative per §2. Vocabulary
  note: 8/16 rows use §29 gate values / compound statuses outside the strict
  §23 five-word epistemic set (FINDING P3-3).
- **Success theater scan (contract §30)**: my grep over all package .md —
  ZERO INVALID_INFERENCE patterns in the executor's analysis/report; the only
  pattern matches are inside AUTHORIZATION.md's own §30 quotation of the
  forbidden examples. The negative result is stated cleanly per §31
  (TEMPLATE_ROLE_TEST §6: FULL-VALUE negative; N-02 documents the no-rescue /
  no-other-call-site discipline).
- **RTTI label honesty**: all class labels consistently marked as Ghidra
  RTTI-analyzer readings / STRONGLY_SUPPORTED with N-07 (no independent chain
  walk by the executor). My independent walks CONFIRM all three load-bearing
  RTTI facts (gate TD = ArkRepairUI_Impl [.PAV form]; unwind vtable 0x00A80704
  = ArkRepairUI; store vtable 0x00A7A948 = ArkUI::Component) — conservative
  labeling, no overclaim.
- **sids.vfs container CRC=0 nuance**: reproduced by me — container record
  {id=1, size=128,996, ver=1, crc field=0x00000000}; validation by exact
  payload closure + 3,887/3,887 count (my parse: entries=3,887, end_pos =
  payload end EXACTLY, unique ids 3,887, no duplicates; first entry = ("",
  2021) — a data nuance not documented in SIDS_ENTRY_PARSE, harmless).
  The documented layout (u16 count; count × (string[u16len], u32 id)) closes
  exactly; I falsified my own alternative layout hypothesis (qc3: LayoutA
  yields 3,886 ≠ count; LayoutB = the claimed layout closes with 3,887).
- **Supersessions R-1..R-6**: field-level consistency checked. R-1 (sids
  container-census superseded by entry parse) — no retracted claim cited as
  standing anywhere ✓. R-2 — INACCURATE about FALSIFIER_REACH_CHECK.json's
  content (FINDING P2-1). R-3 (working-label correction, honest) ✓. R-4
  (Jython signed-byte artifact: curated listings carry proper hex; my byte
  reads match the physical bytes) ✓. R-5 (deferred-lead disposition;
  HUMAN_HISTORICAL_RECOLLECTION untouched as probe-selection only) ✓. R-6
  (prior canon not retracted; PRIOR_RESULT_LEVEL = B UNCHANGED in DRAFT Part E
  ✓).
- **NOT_CHECKED.md (N-01..N-16)**: honest bounds; none load-bearing-
  undermining (N-02 contract-mandated; N-07 now independently covered by my
  walks; N-13 matches my script scan; N-10 matches my CRC=0 finding).
- **DRAFT_FINAL_REPORT.md**: 18 questions answered separately (Part A 1-18) ✓;
  §29 status block filled with exact contract strings (Part E — every field
  within its allowed value set) ✓; budget ledger present (Part B) ✓; self-check
  honestly labeled non-independent (Part C) ✓.
- **Repo hygiene**: 64 files = my census (4+33+8+18+1) ✓; only the new package
  added; 5 foreign groups untouched; zero git state ✓ (Q16).
- **Script hash ledger**: my re-hash of all 17 scripts vs SCRIPT_SHA256.csv —
  **17/17 match, 0 mismatches** (qc5). CSV has a UTF-8 BOM + one blank line
  (FINDING P3-5c).

---

## 4. FINDINGS

**F-P2-1 (P2, material evidence-indexing) — FALSIFIER_REACH_CHECK.json coverage
and summary misdescribe the run's reach-check.**
Location: 01_RAW/FALSIFIER_REACH_CHECK.json (fields `total_functions_checked:
13`, `interpreted.TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS: 0`), vs
02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md R-2 ("s8_curate_g5.py regenerated the
same file ... over g1..g5") and 02_ANALYSIS/TEMPLATE_ROLE_TEST.md §4 (cites the
file for "all 19 measured functions").
Contradicted claim: no SCIENCE claim is contradicted (all are true per my
census) — the defect is that the central machine-readable artifact covers only
13 functions (g1..g4 + containing), its TOTAL=0 is true only for that subset
(the single recorded hit FUN_004D1430@0x00823C57 lives only in
G5_LOOKUP_CLOSURE.json), and R-2/§4 describe the file more widely than it is.
Independent evidence: my read of the JSON (13 per_function keys, no G5/G6
rows); G5_LOOKUP_CLOSURE.json H03 row with the hit; my whole-.text census over
all 18 measured-function windows (exactly 1 hit, the classified one).
Skutek (effect): a future audit consuming only FALSIFIER_REACH_CHECK.json would
undercount coverage and could misread TOTAL=0 as "zero machinery hits anywhere".
Narrow correction required: regenerate FALSIFIER_REACH_CHECK.json (schema-
compatible) over all 18 measured functions with
TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS = 1 (classified generic mapfind) plus a
pointer to the G5/G6 rows — or amend R-2 + C4057-08's method field to name the
actual artifact distribution. Revalidation predicate: the regenerated JSON must
list 18 per_function entries and its hits must equal my census (only
{FUN_00823C10: FUN_004D1430 @0x00823C57}).

**F-P3-1 (P3, correctness) — one sub-address label off by 5 in the step table.**
Location: 02_ANALYSIS/CALLSITE_DATAFLOW.md §3 STEP 8: "0x00821C27 51 / 0x00821C2B
50 PUSH ECX / PUSH EAX". Physical bytes (my dump): 0x00821C27 = `8D 44 24 20`
(LEA EAX,[ESP+0x20]); PUSH EAX (0x50) is @0x00821C2B (correct in their text);
PUSH ECX (0x51) is @0x00821C2C, not 0x00821C27. The semantics
(FUN_00821760(0, 4057, &out)) are byte-correct; only the PUSH ECX address label
is wrong. Correction: relabel to 0x00821C2C. Revalidation: byte table row must
read `0x00821C2C 51`.

**F-P3-2 (P3, correctness) — budget function count off by one.**
Location: 00_CONTROL/RUN_BUDGET.md final ledger row + 05_REPORT/DRAFT_FINAL_
REPORT.md Part B + 02_ANALYSIS/NOT_CHECKED.md §Budget-relevant counts — all say
NEW_PCG_FUNCTIONS_DETAILED = 19; the package's own enumeration lists 18
functions (18 G-decompile .c files: G1×1 + G2×5 + G3×5 + G4×2 + G5×4 + G6×1).
Correction: set 18, or enumerate the 19th explicitly (I found none).
Revalidation: count of enumerated functions == ledger value. No limit impact
(60).

**F-P3-3 (P3, hygiene) — CLAIM_MATRIX status column mixes vocabularies.**
Location: 02_ANALYSIS/CLAIM_MATRIX.csv, column `status` (8/16 rows use §29
gate values or compounds: PRESENT (C4057-03/04), NOT_ESTABLISHED (09/10-part/
11-part/12-part/14), NO (15), compounds (09/10/11/16)). Each row's epistemic
content is recoverable and correct (my measurements confirm each row's
substance), and the contract itself defines those gate values (§8-§18/§29) —
but a strict §23 five-word validation of the column is impossible as written.
Correction (future runs): split into EPISTEMIC_STATUS (§23 set) +
GATE_RESULT (§29 value set) columns.

**F-P3-4 (P3, wording) — two analysis-wording imprecisions.**
(a) 02_ANALYSIS/TEMPLATE_ROLE_TEST.md §5 "byte-identical call shapes": the six
series sites are NOT byte-identical — 0xFD4..0xFD8 use LEA ECX,[ESP+0x2C]
while the 0xFD9 anchor uses LEA ECX,[ESP+0xC8] (same callee FUN_008DFCD0, same
arg1 class, different this-slot). (b) 02_ANALYSIS/NEGATIVE_CONTROLS.md
CONTROL-2 "62 unique PUSH imm32 values": the 62 Ghidra-decoded PUSHes include
imm8 (6A) forms (small ints 0..0x16, 0x3C); my imm32-only byte census found 49
unique imm32 values — consistent as a superset, but "PUSH imm" would be the
correct wording. Corrections: qualify (a) as "same callee/pattern, differing
this-slot"; reword (b) to "PUSH imm values".

**F-P3-5 (P3, hygiene) — SCRIPT_SHA256.csv parseability defects.**
Location: 03_SCRIPTS/SCRIPT_SHA256.csv — UTF-8 BOM (header becomes
"\ufeffscript" for naive consumers; my first DictReader pass returned 0 rows)
+ one blank line (row 5). Hashes themselves: all 17 verified correct by my
re-hash. Correction: re-save without BOM/blank line. Revalidation: csv module
DictReader yields 17 rows with a clean `script` key.

No P0 or P1 findings. No finding contradicts any load-bearing claim of the run.

---

## 5. EXPLICIT STATEMENTS REQUIRED BY THE DISPATCH

(a) **The negative result (IMMEDIATE_4057_IS_TEMPLATE_ID =
REJECTED_FOR_THIS_CALLSITE) is SUPPORTED** by my independent measurements:
my own byte-level whole-.text census found ZERO calls from any of the 18
measured functions to FUN_0072F580 or any machinery VA (registry getter
0x00BA1824 referenced only inside FUN_0043A550, which is called from none of
the measured windows); the 4057 value chain terminates in the sids string-table
resolution + ArkUI::Component string store; the three singletons are physically
disjoint. The measured positive identification (4057 = sids entry id
"S_REPAIR_UI_CLEAR_TOOLTIP") is likewise confirmed by my own sids parse +
the code-side chain bytes.

(b) **The data-side repins are SUPPORTED**: templates.vfs record id2=4057
@88,792 {A=218757, B=218758} (my walker, my CRC recompute, my census
5,438/EOF/0-fail); Models.bnt "218757.nif" @395,283,797 and Volumes.bnt
"218758.bvi" @3,712,726 (my full-file searches); calibration anchors 4508 /
296445.nif / 296446.bvi all reproduced exactly.

(c) **For PE-MASTER to adjudicate personally**:
1. Whether F-P2-1 (+ the P3 corrections) justifies the single bounded executor
   repair round — my recommendation: YES, but ONLY as a documentation/evidence-
   index repair (regenerate FALSIFIER_REACH_CHECK.json over 18 functions; fix
   R-2 wording; 19→18 count; STEP-8 address; CSV BOM; the two wording notes).
   NO science re-measurement is needed — every science fact was independently
   confirmed by this QC.
2. The RTTI-label upgrade: my chain walks confirm the three RTTI facts the
   package conservatively marks STRONGLY_SUPPORTED/N-07. PE-MASTER may record
   this as a QC-side confirmation (the executor's N-07 remains an honest
   statement of the executor's own work).
3. The dispatch paraphrase "86/120 calls" vs the package's consistent 84/120 —
   no package-internal inconsistency; recorded for the loop ledger.
4. sids.vfs data nuance (not documented in SIDS_ENTRY_PARSE, no claim affected):
   the first payload entry is an empty string with id 2021; the payload closes
   exactly under the documented layout with 3,887 entries.

---

## 6. FULL_READ_LOG and NOT_CHECKED (this QC's own)

FULL_READ (package, in full): DRAFT_FINAL_REPORT.md; CLAIM_MATRIX.csv;
RAW_BYTE_PINS.json; TEMPLATE_4057_PHYSICAL_RECORD.json; FALSIFIER_REACH_
CHECK.json; SIDS_ENTRY_PARSE.json; RESOURCE_INDEX_PINS.json; RUN_BUDGET.md;
AUTHORIZATION.md (1726 lines); PREFLIGHT.md; SELECTION.md; TEMPLATE_ROLE_
TEST.md; NOT_CHECKED.md; RETRACTIONS_SUPERSESSIONS.md; NEGATIVE_CONTROLS.md;
CALLSITE_DATAFLOW.md; OBJECT_IDENTITY_TRACE.md; TRANSFORM_PROVENANCE.md;
SCRIPT_SHA256.csv; G2_DECOMPILE_D01; G3_DECOMPILE_E05; G4_DECOMPILE_F01;
G5_LOOKUP_CLOSURE.json (targeted: lines 320-349 + grep hits).
NOT_CHECKED by this QC (none load-bearing-undermining):
- The executor's full 951/951 listing crosscheck was NOT re-executed (boundary
  rule + every load-bearing window instruction verified byte-level; 951-count
  treated as plausibility per the dispatch).
- G1_FUNCTION_DUMP.json / G2_CALLEE_DEEPDIVE.json / G3_FALSIFIER_PATH.json /
  G4_TERMINAL_CONSUMER.json / G6_SIDS_PARSER.json / CALL_XREF_CENSUS.json /
  CALLSITE_WINDOW.json / CALLSITE_DATAFLOW_WINDOWS.json / SIDS_REPINS.json —
  targeted reads/greps only; their load-bearing content was re-measured
  independently from raw bytes by me (superseding spot-checks of executor
  derivatives).
- G2 decompiles D02-D05 and G3 decompiles E01-E04 read as guides only; their
  load-bearing links were verified from my own dumps.
- Bodies of FUN_008E7B80 / FUN_008DF3F0 / FUN_008DF310 beyond entry windows —
  their machinery-hit freedom is nevertheless established by my whole-.text
  census over their windows.
- Live remote git equality: HEAD == BASE_SHA verified by me; cached
  origin/master ref checked; live-remote verification remains the parent's
  pre/post-executor measurement (per dispatch).

## 7. RAW EVIDENCE (04_QC/raw/) — my own instruments and outputs

- qc1_exe_bytes.py + qc1_exe_bytes_output.txt — own PE parse; anchor/886 byte
  reads; prologue/epilogue/padding boundaries; caller rel32 recomputation;
  whole-.text E8/E9 censuses (single-caller; machinery; chain); absolute-ref
  scan of the three singletons + vtables; string searches; FUN_00599D30
  immediate census + series verification; 12/12 chain-link recomputation MATCH;
  FUN_00414170/FUN_00415670/FUN_008DFCD0/FUN_008F0780/FUN_008DFB70/FUN_00823C10/
  FUN_00821760/FUN_004D1430/FUN_0072F580/FUN_0043A550 byte dumps.
- qc2_windows_rtti_vfsdiag.py + qc2_output.txt — machinery-in-window filter
  census (exactly 1 hit); FUN_00599D30 E8 census; RTTI TD/vtable chain walks;
  templates/sids/BNT diagnostic dumps (BNT hits + index headers).
- qc3_vfs_walks.py + qc3_output.txt — first walk attempt (72-stride desync
  documented) + sids layout falsification test (LayoutA/LayoutB).
- qc4_final_walks.py + qc4_output.txt — FINAL independent walks: templates
  5,438/EOF/0-CRC/unique + records 4057/4508/11963 + id2 census 4052..4057;
  sids 3,887/3,887 exact closure + all 13 target entries.
- qc5_hashes_rtti.py + qc5_output.txt — 17/17 script hash re-verification;
  completed vtable COL chain walks (ArkRepairUI / ArkUI::Component names).
- QC_RAW_INVENTORY.csv — SHA256 of my own QC raw evidence (generated after
  this report).

Anti-circularity statement for my own load-bearing PASSes:
MEASURED_QUANTITY: physical bytes/hashes/censuses listed above;
INDEPENDENT_SOURCE_OF_TRUTH: Entropia.exe / templates.vfs / sids.vfs /
Models.bnt / Volumes.bnt / the git object store — read by my own parsers;
WHY_NON_CIRCULAR: no executor script, JSON, or Ghidra output was used as an
oracle (the s1 stride comment was used only as a format hint and then
re-derived + falsification-tested from bytes); all PASS predicates were
computed by my own code from raw inputs;
FAILURE_CASE_DETECTED: each check had a concrete falsifier (wrong stride →
desync/EOF/count failure — actually exercised and corrected in qc3→qc4; wrong
immediate → byte mismatch; missed machinery call → census hit; wrong singleton
→ reference-set overlap; wrong entry → closure/string mismatch).

## 8. OUTPUT BLOCK

```text
QC_VERDICT = QC_PASS_WITH_FINDINGS

FINDINGS:
  F-P2-1  01_RAW/FALSIFIER_REACH_CHECK.json (total_functions_checked=13,
          TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS=0) + R-2/TEMPLATE_ROLE_TEST §4
          describe the artifact wider than it is; G5/G6 rows live in
          G5_LOOKUP_CLOSURE.json/G6_SIDS_PARSER.json. Science unaffected (my
          census confirms zero registry hits over ALL 18 functions; the one
          classified hit is machine-recorded). Correction: regenerate the JSON
          over 18 functions with TOTAL=1 (classified), or amend R-2/C4057-08
          method text. P2 (material evidence-indexing).
  F-P3-1  CALLSITE_DATAFLOW.md §3 STEP 8: "0x00821C27 51" — PUSH ECX is at
          0x00821C2C (semantics byte-correct). P3.
  F-P3-2  NEW_PCG_FUNCTIONS_DETAILED=19 vs 18 enumerated functions
          (RUN_BUDGET.md ledger, DRAFT Part B, NOT_CHECKED.md). P3.
  F-P3-3  CLAIM_MATRIX status column mixes §29 gate values with §23 epistemic
          set (8/16 rows). P3.
  F-P3-4  Wording: "byte-identical call shapes" (series this-slots differ:
          0x2C vs 0xC8); "62 unique PUSH imm32" (includes imm8 forms).
          P3.
  F-P3-5  SCRIPT_SHA256.csv UTF-8 BOM + blank line (hashes 17/17 correct).
          P3.

Q1  = PASS (EXE 8,015,872 B / E778...F31 = pin; my hash; PE header verified)
Q2  = PASS (my walker: 5,438 rec / EOF exact / 0 CRC fail / rec 4057 @88,792
      {size 28, ver 1, crc match}; stride rule byte-derived, falsification-
      tested; census context confirmed)
Q3  = PASS (A=218757, B=218758 from MY parse of payload+4/+8)
Q4  = PASS ("218757.nif" @395,283,797; "218758.bvi" @3,712,726 — my searches;
      calibrations + index_start/counts byte-verified)
Q5  = PASS (file offset 1,682,194 mine; bytes 68 D9 0F 00 00 = PUSH 4057;
      boundary: preceding CALL ends exactly at 0x0059AB12; .text)
Q6  = PASS (prologue @0x00599D30 after CC padding; RET @0x0059AC88 + CC + next
      fn @0x0059AC90; 3,929 B; single caller @0x0059BF11 — exactly 1 in whole
      .text; RTTI gate byte-verified incl. my TD chain walk ArkRepairUI_Impl)
Q7  = PASS (all 12 links recomputed from my bytes 12/12 MATCH; thiscall RET 4;
      this=[ESP+0xC8]; re-push @0x008DFD0E; composite key via mgr map @[this+4];
      store FUN_008DFB70 @0x008DFD2C; ArkUI::Component vtable store @0x008DFBD0)
Q8  = PASS (falsifier INDEPENDENTLY CONFIRMED: machinery in-window census over
      18 functions = exactly 1 hit, the classified generic mapfind
      FUN_004D1430@0x00823C57; registry singleton 0x00BA1824 found by me,
      referenced only in FUN_0043A550, never called on the path; singletons
      disjoint; 4057 terminates in string store)
Q9  = PASS (NOT_ESTABLISHED claim honest; no bridge overclaim anywhere;
      coincidence structure confirmed both sides)
Q10 = PASS (no world-instance claim; UI objects documented as observed ops only)
Q11 = PASS (UNKNOWN; no transform producer; nothing promoted)
Q12 = PASS (PLACEMENT_XYZ_RECOVERED=NO; no recovered XYZ anywhere)
Q13 = PASS (NOT_ESTABLISHED; no scene claim; CONTROL-5 consistent)
Q14 = PASS (bytes 68 76 03 00 00 @0x0059AB37; chain identical to 4057's
      (FUN_008F0780→FUN_00414170→FUN_00821BB0→store FUN_008F01C0);
      sids 0x376=S_GENERIC_CLEAR from my parse; deeper semantics honestly
      UNKNOWN)
Q15 = PASS_WITH_COUNT_DEFECT (preregistration exists; ledger consistent
      except 19-vs-18 function count = F-P3-2)
Q16 = PASS (STATIC_ONLY: zero launch/network primitives in all 17 scripts;
      no payloads in repo; zero git state; 5 foreign groups untouched;
      HEAD == BASE_SHA)

BUDGET: planned 80 calls / 120 min -> used 52 calls / ~85 min
```

END OF TARGETED QC REPORT.
