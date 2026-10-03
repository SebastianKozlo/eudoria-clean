# CALLSITE DATAFLOW — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY. All code claims byte-anchored against
the physical EXE (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe, 8,015,872 B,
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — re-hashed
this run; 01_RAW/RAW_BYTE_PINS.json). Ghidra 11.2.1 (fresh project LANDMARK4057 on a
hash-verified sandbox copy); every instruction of the containing function verified
byte-identical to the physical EXE: **951/951** (01_RAW/RAW_BYTE_PINS.json
g1_byte_crosscheck; method = own PE mapper, no Ghidra involved on the physical side).

## 1. PHASE 2 — RAW PIN (contract §9)

```text
ANCHOR VA              = 0x0059AB12
RVA                    = 0x0019AB12 (image base 0x00400000, ASLR OFF — own PE parse)
FILE OFFSET            = 1,682,194
CONTAINING SECTION     = .text
BYTES AT ANCHOR        = 68 D9 0F 00 00
INSTRUCTION            = PUSH imm32 0x00000FD9 = 4057
IMMEDIATE_4057_RAW_PIN = CONFIRMED
IMMEDIATE_4057_AT_0x0059AB12 = CONFIRMED
```

Mapper calibrations (both PASS, 01_RAW/RAW_BYTE_PINS.json):
(a) canon string anchor "Parameters\templates.vfs" @VA 0x00A86D30 → file offset
6,843,696 (.rdata), bytes identical; (b) canon code anchor PUSH 0x3ED3 @VA
0x005B6597 → bytes 68 D3 3E 00 00 identical (record-bridge E9 pin).

Raw window: 01_RAW/CALLSITE_WINDOW.json (VA 0x0059A992..0x0059AD92, 0x400 B,
per-row VA/file-offset/hex).

## 2. PHASE 3 — CONTAINING FUNCTION (contract §10)

```text
FUNCTION_START   = 0x00599D30 (Ghidra-defined function entry; prologue verified in listing)
FUNCTION_END     = 0x0059AC88 (body max address)
SIZE             = 3,929 B (951 instructions)
CALLERS          = 1: FUN_0059BE70 @ call site 0x0059BF11 (isCall-filtered xref census)
CALLEES          = 177 call sites, 49 unique direct targets, 7 indirect (01_RAW/CALL_XREF_CENSUS.json)
CALLING CONVENTION: Ghidra labels it "unknown" (fastcall-shaped, param_1 on stack per
  decompiler; the function builds stack-local objects and dispatches thiscalls with
  ECX = &stack-local — evidence per instruction below)
NAME             = kept as FUN_00599D30 until dataflow; after RTTI evidence from its
                  sole caller (below) the bounded working label is
                  "ArkRepairUI component builder" — RTTI-anchored in the CALLER, not
                  an assumption about FUN_00599d30's own body.
```

Sole caller FUN_0059BE70 (g3 dump, 01_RAW/G3_DECOMPILE_E05_caller_0059be70_0059BE70.c):
performs `FUN_008df860(0x411)`, stores `ArkRepairUI::vftable` in its unwind local,
type-checks the object's RTTI Type Descriptor against
`ArkRepairUI_Impl::RTTI_Type_Descriptor` (binary RTTI symbols, Ghidra RTTI analyzer),
and on match calls FUN_00599d30() → the anchored function is invoked inside the
RTTI-gated ArkRepairUI initialization path. (Ghidra-RTTI-labeled; independent
vtable-4 chain walk NOT performed this run — see NOT_CHECKED. R1 AMEND NOTE:
QC's independent RTTI chain walks now CONFIRM the chain-walk facts — gate Type
Descriptor 0x00B7DDE8 = '.PAVArkRepairUI_Impl@@', unwind vtable 0x00A80704 ->
COL 0x00AA276C -> TD 0x00B7DED8 = '.?AVArkRepairUI@@', store vtable 0x00A7A948
-> COL 0x00A9EDD4 -> TD 0x00B6E084 = '.?AVComponent@ArkUI@@' (04_QC/
TARGETED_QC_REPORT.md Q6). Executor + QC agree on the chain-walk facts; class
BEHAVIORAL identity remains exactly as before, NOT upgraded.)

## 3. PHASE 4 — WHAT PUSH 4057 EXACTLY IS (contract §11)

Anchor window (byte-anchored listing, 01_RAW/G1_FUNCTION_DUMP.json; cross-check 951/951):

```text
VA          BYTES                 INSTRUCTION
0x0059AAF1  6A 01                 PUSH 0x1
0x0059AAFB  6A 02                 PUSH 0x2
0x0059AB05  50                    PUSH EAX
0x0059AB06  8D 8C 24 D0 00 00 00  LEA ECX,[ESP + 0xd0]
0x0059AB0D  E8 DE 48 34 00        CALL 0x008df3f0        ; guard helper (getter->act)
0x0059AB12  68 D9 0F 00 00        PUSH 0xfd9             ; THE ANCHOR: 4057
0x0059AB17  8D 8C 24 C8 00 00 00  LEA ECX,[ESP + 0xc8]   ; this = stack-local UI object
0x0059AB1E  E8 AD 51 34 00        CALL 0x008dfcd0        ; thiscall, 1 stack arg, RET 4
0x0059AB23  8D 8C 24 8C 00 00 00  LEA ECX,[ESP + 0x8c]
0x0059AB2A  51                    PUSH ECX
0x0059AB2B  8D 8C 24 C8 00 00 00  LEA ECX,[ESP + 0xc8]   ; same this
0x0059AB32  E8 49 D0 34 00        CALL 0x008e7b80        ; produces EAX (a new sub-object)
0x0059AB37  68 76 03 00 00        PUSH 0x376             ; 886
0x0059AB3C  8B C8                 MOV ECX,EAX            ; this = the produced object
0x0059AB46  E8 35 5C 35 00        CALL 0x008f0780        ; sibling consumer of 886
```

**Argument/dataflow role of 4057**: PUSH 4057 @0x0059AB12 is the ONLY stack
argument (arg1, [ESP+4] at callee entry) of the thiscall
`this->FUN_008DFCD0(4057)` with `this = LEA ECX,[ESP+0xC8]` (a stack-local UI
object of FUN_00599D30), consumed by CALL @0x0059AB1E (`RET 4` cleanup at
0x008DFD61). The value 4057 is neither copied to a local register first nor
passed through a wrapper on the caller side; it goes directly onto the stack
for the callee.

Full identity-preserving chain of 4057 (every step VA + bytes + source/dest;
listings: 01_RAW/G2_CALLEE_DEEPDIVE.json, G3_FALSIFIER_PATH.json,
G4_TERMINAL_CONSUMER.json, G5_LOOKUP_CLOSURE.json, G6_SIDS_PARSER.json):

```text
STEP 1  0x0059AB12  68 D9 0F 00 00   PUSH 0xFD9
        src: immediate | dst: stack ([ESP] at 0x0059AB17)
STEP 2  0x0059AB1E  E8 AD 51 34 00   CALL FUN_008DFCD0
        arg1 ([ESP+4] at entry) = 4057; this = [ESP+0xC8] object
STEP 3  0x008DFD05  8B 4C 24 40      MOV ECX,[ESP+0x40]   ; 4057 -> ECX
STEP 4  0x008DFD0E  51               PUSH ECX             ; re-push 4057 as arg2 for FUN_00821BB0
        (0x008DFD0D PUSH EAX = arg3 = &12-B zeroed struct;
         0x008DFD13 PUSH EDX = arg1 = &out basic_string)
STEP 5  0x008DFD18  E8 53 44 B3 FF   CALL FUN_00414170    ; 0x1C-singleton getter (plain RET,
        returns string-table singleton @DAT_00BA124C; the pushed args stay on the stack)
STEP 6  0x008DFD1D  8B C8            MOV ECX,EAX          ; this = singleton
        0x008DFD1F  E8 8C 1E F4 FF   CALL FUN_00821BB0(&out_str, 4057, &struct)  RET 0xC
STEP 7  0x00821C23  8B 4C 24 50      MOV ECX,[ESP+0x50]   ; 4057 -> ECX (arg2 of 00821bb0)
STEP 8  0x00821C2D  6A 00            PUSH 0x0             ; arg1 = 0 (section selector)
        0x00821C2C  51 / 0x00821C2B 50  PUSH ECX / PUSH EAX ; 4057 = arg2; &local = arg3
        0x00821C2F  8B CF            MOV ECX,EDI          ; this = singleton
        0x00821C31  E8 2A FB FF FF   CALL FUN_00821760(0, 4057, &out_local)  RET 0xC
STEP 9  inside FUN_00821760 (g4):
        0x008217CE  E8 7D 52 00 00   CALL FUN_00826A50    ; key part 1 = table getter
        0x008217F3  E8 78 3E BF FF   CALL FUN_00415670    ; 0x98-manager singleton getter
        0x008217FA  E8 11 24 00 00   CALL FUN_00823C10    ; mgr->extract(key{part1, 4057})
        inside FUN_00823C10 (g5):
        0x00823C57  E8 D4 D7 CA FF   CALL FUN_004D1430    ; GENERIC STL RB-tree mapfind on
                                                          ; the mgr's map @[this+4]
        0x00823C64  8D 78 14          LEA EDI,[EAX+0x14]   ; entry = node+0x14 (value slot)
        -> virtual dispatch on [entry+0x24]; result string at result+0x10
STEP 10 0x0082183B..  TEST ESI,ESI / MOV [..+0x10] copy: out_local = *(result+0x10); return 1
        (miss path in FUN_00821BB0: 0x00821C3A PUSH 0xba8218 -> copy of global fallback
         string DAT_00BA8218)
STEP 11 back in FUN_008DFCD0:
        0x008DFD24  50               PUSH EAX             ; &result string
        0x008DFD25  8B CE            MOV ECX,ESI         ; this = the [ESP+0xC8] UI object
        0x008DFD2C  E8 3F FE FF FF   CALL FUN_008DFB70   ; thiscall store, RET 4
        inside FUN_008DFB70 (g3): 0x008DFBD0 MOV [ESP+0x3C],0xA7A948 = store of the
        RTTI-labeled ArkUI::Component::vftable (0x00A7A948) into a temp component that
        receives the string item — the resolved string is stored into an
        ArkUI::Component-family sub-object of the [ESP+0xC8] owner.
```

The chain is straight-line (no branch between the PUSH and the store except the
lookup success/fallback pair, both of which deliver a string to the SAME store
call). Identity preservation of the VALUE 4057 is complete from immediate to
its terminal use as the second element of the composite map key
{section_object, 4057}.

## 4. THE VALUE'S TERMINAL IDENTITY — sids.vfs STRING ID

The string-table singleton's initializer (FUN_00821FB0, g5 dump) opens the
physical file `"parameters\\sids.vfs"` (VFS reader family incl. FUN_00971AD0 per
canon E1), and FUN_00821E70 (g6 dump) parses the record payload as
**u16 count; count x (string, u32 id)** into the singleton's map.

Data-side verification (01_RAW/SIDS_ENTRY_PARSE.json; sids.vfs 129,040 B, SHA256
D58EF1D2E49FD52C093AA37E8FAE4A2653A163728DDAE52048B40512CFF0FB6E, single
container record id=1, payload 128,996 B): the payload closes EXACTLY under the
measured layout with **3,887 entries / 3,887 unique u32 ids** (R1 data nuance,
QC-confirmed — 04_QC: the first payload entry is an empty string with id 2021;
the layout still closes exactly with 3,887 entries) and:

```text
0xFD9 (4057) -> 'S_REPAIR_UI_CLEAR_TOOLTIP'
```

So at this call-site, immediate 4057 = the sids.vfs string-table entry id whose
string is `S_REPAIR_UI_CLEAR_TOOLTIP`, resolved through the string-table
singleton and stored on an ArkUI::Component-family object built by
FUN_00599D30 — the ArkRepairUI construction path. The identical-twin sequence
in the same function (s4 census, 01_RAW/CALLSITE_DATAFLOW_WINDOWS.json):

```text
FUN_008dfcd0 sites: 0xFD4 S_REPAIR_UI_ADD_EQUIPPED_TOOLTIP
                  0xFD5 S_REPAIR_UI_ADD_WEAPONS_TOOLTIP
                  0xFD6 S_REPAIR_UI_ADD_ARMOR_TOOLTIP
                  0xFD7 S_REPAIR_UI_ADD_TOOLS_TOOLTIP
                  0xFD8 S_REPAIR_UI_ADD_ALL_TOOLTIP
                  0xFD9 S_REPAIR_UI_CLEAR_TOOLTIP   <- anchor
FUN_008f0780 sites: 0xFAB S_REPAIR_UI_ADD_EQUIPPED, 0xFAE..0xFB1 S_REPAIR_UI_ADD_*
                  0xFB2 S_REPAIR_UI_DRAG_ITEMS_HERE, 0x376 (886) S_GENERIC_CLEAR
```

## 5. PHASES 6-11 — NOT EXECUTED (STOP S2)

The mandatory falsifier fired (see 02_ANALYSIS/TEMPLATE_ROLE_TEST.md): 4057 does
NOT reach FUN_0072F580 or any proven template-id consumer. Per contract §12/§24
the landmark construction path (template→model bridge, resource request, object
identity, transform source, scene/world edge, XYZ recovery) was NOT continued.
The [ESP+0xC8] object is a UI-side object on a measured UI path; no world
instance, transform producer, or scene edge was traced (and none is claimed).
