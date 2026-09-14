# SLOT17 ERRATA — W6 (GB12 vtable prose-table erratum + NiRTTI precision statement)

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY.
The historical SLOT17 commit 5290e79, its branch, worktree and package files are NEVER
modified. All errata below live in THIS cleanup package only (append-only annotation of
the historical record).

## §1 GB12 NiNode vtable — the raw JSON is the source of truth (re-verified this run)

This run re-verified the GB12 NiNode vtable sequence directly from the SLOT17 package's
raw relocation dump `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json` (READ-ONLY; parsed by
this run's own script):

| slot | symbol in the raw JSON (verbatim) | short name |
|---|---|---|
| 13 | ?GetGroup@NiObject@@UBEPAVNiObjectGroup@@XZ | GetGroup |
| 14 | ?SetGroup@NiObject@@UAEXPAVNiObjectGroup@@@Z | SetGroup |
| 15 | ?UpdateControllers@NiNode@@UAEXM@Z | UpdateControllers |
| 16 | ?UpdateNodeBound@NiNode@@UAEXXZ | UpdateNodeBound |
| 17 | ?ApplyTransform@NiNode@@UAEXABVNiMatrix3@@ABVNiPoint3@@_N@Z | ApplyTransform |
| 18 | ?GetObjectByName@NiNode@@UAEPAVNiAVObject@@PBD@Z | GetObjectByName |
| 19 | ?SetSelectiveUpdateFlags@NiNode@@UAEXAA_N_N0@Z | SetSelectiveUpdateFlags |

(slot_count 34; symbol spelling as recorded in the raw JSON.)

**THE PROSE-TABLE DEFECT (02_ANALYSIS/CLASS_HIERARCHY_AND_VTABLE_MAP.md, GB12 table rows
for slots 13-16, NiAVObject/NiNode columns) is CONFIRMED:** the prose rows show
UpdateControllers at slot 13 AND slot 15, and UpdateNodeBound at slot 14 AND slot 16,
misplacing the inherited GetGroup (13) and SetGroup (14). The raw JSON proves
13=GetGroup, 14=SetGroup, 15=UpdateControllers, 16=UpdateNodeBound.

**The headline results are CORRECT and unchanged:** GB12 slot 17 = ApplyTransform,
GetObjectByName @ 18, SetSelectiveUpdateFlags @ 19 — all three re-verified from the raw
JSON this run. The RAW JSON was never wrong and is untouched; this is an append-only
erratum for the prose table.

## §2 NiRTTI precision statement (three parts, per the G5 pin — with the bounded-probe upgrade)

1. **0x00BA7218 = NiNode NiRTTI — CONFIRMED** (static-initializer call-site proof;
   SLOT17 03_EVIDENCE/ENTROPIA_NIRTTI_STATIC_INIT.txt: the thunk at 0x00A6C200 does
   `push 0x00BA7270; push 0x00A8CE00 ("NiNode" literal); mov ecx, 0x00BA7218;
   call 0x007199E0; ret`). Corroborated this run by an INDEPENDENT second static use:
   the E1 dispatch wrapper FUN_007EB210 walks an NiRTTI base chain comparing against the
   immediate 0x00BA7218 (`cmp eax, 0xba7218` @0x007EB260, bytes 3D 18 72 BA 00) — see
   01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt.
2. **The base pointer VALUE 0x00BA7270 — CONFIRMED** (the pushed immediate in the NiNode
   initializer).
3. **0x00BA7270 semantic identity = NiAVObject NiRTTI — CONFIRMED (UPGRADED from
   STRONGLY_SUPPORTED by this run's bounded probe).** The optional bounded probe
   (RUN_CONTRACT.md W6.4; generator 00_CONTROL/nirtti_bounded_probe.py; raw output
   01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt) scanned the whole file for the byte pattern
   `B9 70 72 BA 00` (mov ecx, 0x00BA7270): EXACTLY ONE occurrence, at VA 0x00A6C33A
   (.text). The surrounding static-initializer thunk (standalone, int3-padded, same ctor
   call 0x007199E0 as the NiNode initializer) is:

   ```
   0x00A6C330  push 0x00BA7224        ; base RTTI pointer
   0x00A6C335  push 0x00A8D8BC        ; .rdata literal -> 'NiAVObject'
   0x00A6C33A  mov  ecx, 0x00BA7270   ; this = the NiRTTI object
   0x00A6C33F  call 0x007199E0        ; the NiRTTI ctor (same as NiNode's)
   0x00A6C344  ret
   ```

   i.e. `*(NiRTTI*)0x00BA7270 = NiRTTI("NiAVObject", (const NiRTTI*)0x00BA7224)` —
   **DIRECT STATIC-INITIALIZER CALL-SITE PROOF (own bytes, STATIC-ONLY, this run)** that
   the object at 0x00BA7270 is the NiRTTI named "NiAVObject" (with base 0x00BA7224,
   the next class up the chain). The probe stayed within its declared bound (one pattern
   + one context window; no seam expansion). This upgrades the semantic identity from
   STRONGLY_SUPPORTED to CONFIRMED while the supporting MSVC RTTI chain
   (.?AVNiNode@@ -> .?AVNiAVObject@@) and NiImplementRTTI pattern remain consistent.

## §3 AUD-F4 docstring erratum (PE optional header)

The SLOT17 `00_Control/entropia_rtti_probe.py` docstring claim that "this binary's
optional-header standard-fields region reads +4 shifted relative to the winnt.h
IMAGE_OPTIONAL_HEADER32 layout" is **factually wrong** (REJECTED_WITH_EVIDENCE, AUD-F4).
This run's own byte derivation (01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt): e_lfanew
0x120; optional header at e_lfanew+0x18 = 0x138; Magic 0x10B; ImageBase dword @
OptionalHeader+0x1C = 0x00400000; SectionAlignment @+0x20 = 0x1000; DllCharacteristics
@+0x46 = 0x0000 — the standard IMAGE_OPTIONAL_HEADER32 layout holds exactly (the "+28
convention" the docstring cites IS the standard +0x1C offset). Every future adapted
script must use the standard wording.

## §4 AUD-F1/F7 temporal-scope errata (git chronology)

The SLOT17 HANDOFF/REPORT equality statements ("...= origin/master = live remote master...
no drift", "BASE_SHA 3644e5ac (= origin/master = live remote master = isolated worktree
HEAD, re-verified)") lack temporal scoping. Corrected statement (this run's git evidence):
local master == 3644e5ac == BASE_SHA at SLOT17 RUN START (session start 14:31 local);
local master advanced to a7a6c756 at 14:40:54 -0700, BEFORE the SLOT17 branch commit at
15:11:43 -0700, so AT PUBLICATION local master was a7a6c756. The isolated-worktree
HEAD == branch parent 3644e5ac pin is unaffected. REMOTE_HEAD_CHRONOLOGY = UNRESOLVED
(local git evidence cannot date the remote's master ref change).

## §5 AUD-F2 census erratum (FILES_CHANGED split)

The SLOT17 HANDOFF FILES_CHANGED per-directory split "03_EVIDENCE 15, 06_REPORT 5" is
wrong; the physical tree census of commit 5290e79 is 03_EVIDENCE 16, 06_REPORT 4
(00_CONTROL 6, 01_RAW 3, 02_ANALYSIS 6). TOTAL 35 stands.
