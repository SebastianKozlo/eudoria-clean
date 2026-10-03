# QC-F2 RAW — F-D2 ABI correction verified against existing raw evidence (my own decode)

DATE = 2026-10-03 (UTC) | BINARY TOUCH = NONE (the C9 L01 window covers the pre-call bytes, so the bounded EXE re-read was NOT needed; no EXE byte was read by this QC)

## Sources used (existing historical raw evidence, READ-ONLY)
- 01_RAW/C9_LISTING_WINDOWS.json — windows L01 (emitter FUN_006C3F50), L02 (lookup impl FUN_0072F580), L03 (mapfind FUN_004D1430), L08 (place_constr_00567170 — a parallel caller)
- 01_RAW/C10V2_BYTE_CROSSCHECK.json — exe_sha256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; windows 962/962 instructions byte-identical; 113/113 call/imm targets match
- 02_ANALYSIS/TRACE_EDGE_BLOCKS.md — E1 (lines 46-52: registry RB-tree, root DAT_00BA1824, lazy singleton init in FUN_0043A550 — X11: if DAT_00BA1824==0 -> new(0x18) -> FUN_0052A260), E2 (71-104), E3 (106-134)

## My own decode of window L01 (emitter FUN_006C3F50; start=0x006C3F50, end=0x006C3FC0)
Byte-encoding note: the window JSON renders bytes >0x7F as negative hex (byte−0x100), e.g. "-75" = 0x8B, "-38" = 0xC8, "-3E" = 0xC2. Decoded by me:

```text
0x006C3F50: 83 EC 08        SUB ESP,0x8
0x006C3F53: 8B 44 24 0C     MOV EAX,dword ptr [ESP+0x0C]   ; id2 (emitter's incoming arg1; after SUB ESP,8 the
                                                              pre-push [ESP+0xC] = entry [ESP+4])
0x006C3F57: 53              PUSH EBX                       ; (register saves between the MOV and the PUSH —
0x006C3F58: 56              PUSH ESI                        ;  prologue pushes; do not change the argument
0x006C3F59: 57              PUSH EDI                        ;  analysis)
0x006C3F5A: 50              PUSH EAX                       ; id2 remains stack argument
0x006C3F5B: E8 F0 65 D7 FF  CALL 0x0043A550                ; rel32 0xFFD765F0 -> 0x006C3F60+(-0x289A10)=0x0043A550 ✓ (c10v2: match)
0x006C3F60: 8B C8           MOV ECX,EAX                    ; ECX = EAX = RETURN of FUN_0043A550
0x006C3F62: E8 19 B6 06 00  CALL 0x0072F580                ; rel32 0x0006B619 -> 0x006C3F67+0x6B619=0x0072F580 ✓ (c10v2: match)
0x006C3F67: 8B F8           MOV EDI,EAX                     ; EAX = template pointer; EDI = template pointer
0x006C3F69: BB 66 00 00 00  MOV EBX,0x66                    ; MODEL type
0x006C3F6E: 8B CF           MOV ECX,EDI                     ; ECX = template
0x006C3F74: E8 67 5E 10 00  CALL 0x007CE1E0                ; getter A (c10v2: match)
... 0x006C3F8D: MOV [ECX],EBX (store 0x66); 0x006C3F8F: MOV [ECX+4],EAX (store A)
```

WINDOW COVERAGE CHECK (my QC instruction): the C9 L01 window starts at 0x006C3F50 and its instruction list contains the instructions at 0x006C3F53 (MOV EAX,[ESP+0x0C]) and 0x006C3F5A (PUSH EAX) — the pre-call id2 argument load IS covered by the window → the bounded physical EXE re-read was NOT required and was NOT performed.

## My own decode of window L02 (lookup impl FUN_0072F580; start=0x0072F580, end=0x0072F5B0)
```text
0x0072F580: 51           PUSH ECX            ; saves incoming ECX (this) — later reused as mapfind's result slot
0x0072F581: 56           PUSH ESI
0x0072F582: 8B F1        MOV ESI,ECX         ; ESI = this (the registry/container)
0x0072F584: 8D 44 24 0C  LEA EAX,[ESP+0xC]    ; = &lookup_arg1 (address of the id2 stack argument)
0x0072F588: 50           PUSH EAX
0x0072F589: 8D 4C 24 08  LEA ECX,[ESP+0x8]   ; = &saved-ECX slot (mapfind writes its result node here)
0x0072F58D: 51           PUSH ECX
0x0072F58E: 8B CE        MOV ECX,ESI          ; thiscall: ECX = the registry
0x0072F590: E8 ...       CALL 0x004D1430      ; mapfind (c10v2: target match)
0x0072F595: 8B 44 24 04  MOV EAX,[ESP+0x4]    ; the result node (written by mapfind into the saved slot)
0x0072F599: 3B C6        CMP EAX,ESI         ; found node == this (RB-tree end/sentinel) -> miss
0x0072F59B: 5E           POP ESI
0x0072F59C: 74 07        JZ 0x0072F5A5
0x0072F59E: 83 C0 14     ADD EAX,0x14         ; node -> template (value at node+0x14)
0x0072F5A1: 59           POP ECX
0x0072F5A2: C2 04 00     RET 0x4             ; ONE 4-byte stack argument (both return paths; also RET 0x4 @0x0072F5AB)
```

## Verification chain for ECX = registry_this (NOT id2)
1. E1/X11: FUN_0043A550 = lazy registry-singleton getter (root DAT_00BA1824; if 0 -> new(0x18) -> FUN_0052A260) — it RETURNS the registry singleton in EAX.
2. L01: at 0x006C3F60, EAX holds that return; MOV ECX,EAX ⇒ ECX = registry_this. id2 was PUSHed to the stack at 0x006C3F5A BEFORE the getter call (the classic argument pre-push for the subsequent stdcall lookup: the pushed value survives the getter call and is consumed by FUN_0072F580's RET 4).
3. L02: the lookup treats ECX as the container `this` (MOV ESI,ECX; mapfind called with ECX=ESI; tree walk from [ESI+4]/[ESI+8]; sentinel CMP EAX,ESI) and reads its KEY from the single stack argument via LEA EAX,[ESP+0xC] -> mapfind arg2 = &id2 (mapfind L03 derefs it: MOV ESI,[ESI] then CMP [node+0x10],ESI).
4. Physical absurdity of the old wording: if ECX were id2 (e.g. 4508), MOV ESI,ECX + the mapfind walk from [ESI+4] would read absolute address 0x1194 — impossible; the lookup's own body proves ECX = the container.
5. Corroborating parallel caller L08 (FUN_00567170): PUSH ESI @0x00567365; CALL FUN_0043A550 @0x00567366; MOV ECX,EAX @0x0056736B; CALL FUN_0072F580 @0x0056736D — same pattern (c10v2 matches both targets), i.e. "ECX = getter return, id2 = stack argument" is the family-wide ABI, exactly as the corrected model states.
6. Historical Ghidra decompilation D01 renders the lookup as "__fastcall FUN_0072f580(int param_1)" — an ABI-approximate rendering that made the stack argument look like the only parameter; this explains (mechanism) how the historical "ECX = id2" misreading arose. Raw bytes (L01/L02, c10v2-verified) settle it.

## New-package wording verification (full reads)
- CURRENT_CLAIM_STATE.md §3: lookup model = registry_this.FUN_0072F580(id2); ECX = registry_this; id2 = stack argument; corrected flow block verbatim per order §5; "ECX = id2" RETRACTED (forbidden as current); MAIN_MAPPING_IMPACT = NONE; ABI_DESCRIPTION_CORRECTED = YES ✓
- DESKTOP_FINDINGS.md F-D2: same corrected model; old wording quoted ONLY as preserved historical artifacts (TRACE_EDGE_BLOCKS.md:86-87, 115-117) and explicitly RETRACTED as current ✓
- CORRECTION_MATRIX.csv row F-D2: original wording in the historical-quote column only ✓
- Post-lookup ECX=EDI -> getter A stays correct (L01 window confirms: MOV EDI,EAX @0x006C3F67; MOV ECX,EDI @0x006C3F6E; CALL FUN_007CE1E0 @0x006C3F74) ✓
- Main mapping chain unchanged in CURRENT_CLAIM_STATE.md §7: record -> registry -> lookup -> A @ template+0x08 -> {0x66, A=296445}; separately A=296445 <-> "296445.nif" ✓
- Package-wide grep for "ECX = id2" as a CURRENT claim: only retraction/quote contexts (see TARGETED_QC_REPORT).

## Precision note (non-blocking)
The physical instruction stream contains three prologue register saves (PUSH EBX/ESI/EDI @0x006C3F57-59) between MOV EAX,[ESP+0x0C] and PUSH EAX. The order §5 flow block (and therefore the package's verbatim quote of it) omits them — a semantic simplification inherited from the order's own text, not a package defect. The ABI analysis is unaffected (the pushed value is still the id2 stack argument).

## CONCLUSION
Q2 = VERIFIED FROM EXISTING RAW EVIDENCE. The corrected ABI model (registry_this.FUN_0072F580(id2)) is byte-confirmed; the old "ECX = id2" is physically impossible; MAIN_MAPPING_IMPACT = NONE.
