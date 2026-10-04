# FUN_0070DC20_DECODE — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

MODE: STATIC-ONLY (raw byte reads from the pinned EXE + manual x86 decode +
machine call-target/byte/branch verification; the client never ran). Every
pin below is machine-verified in 01_RAW/S1..S5 (92/92 pin checks PASS).

## FUN_0070DC20_EXTENT

- START = 0x0070DC20 (prologue `83 EC 10 53` = SUB ESP,0x10; PUSH EBX).
- END   = 0x0070DCF0 (exclusive). Two epilogues, both `C2 0C 00` (RET 0xC):
  - fail epilogue  @0x0070DCE2 (returns EAX=0, destroys class_obj on the way),
  - success epilogue @0x0070DCED (returns EAX=EDI = the class_obj).
- The next function FUN_0070DCF0 begins at 0x0070DCF0 (`6A FF 68 28 C7 A0 00`
  SEH prologue). No padding between (0x0070DCF0 directly follows the RET).

## FUN_0070DC20_ARGUMENTS (structural identities, from bytes)

Calling convention: THISCALL, `this` = ECX = the FACTORY, 3 stack args,
RET 0xC:

| Arg | Structure | Evidence |
|---|---|---|
| this | the 20006 FACTORY (same object FUN_0070DCF0 was entered with) | `8B F1` MOV ESI,ECX @0x0070DC2D; caller sets `8B CE` MOV ECX,ESI @0x0070DDBB |
| arg1 [esp+0x18] | RECEIVER (the entity pointer) | `8B 5C 24 18` MOV EBX,[ESP+0x18] @0x0070DC24; NULL check TEST EBX,EBX @0x0070DC2A |
| arg2 [esp+0x24] | &CURSOR (the record-buffer cursor object: {+0 base,+8 end,+0xC pos,+0x11 flag}) | `8B 44 24 24` MOV EAX,[ESP+0x24] @0x0070DC46; consumed by FUN_00726900 as its cursor arg |
| arg3 [esp+0x28] | mode immed (2 from FUN_0070DCF0; 1 from the second caller @0x00704704) | `8B 54 24 28` MOV EDX,[ESP+0x28] @0x0070DCA0; forwarded to the factory+0x80 delegate notify |

Caller-side argument construction @0x0070DDB3-0x0070DDBD (machine-verified):
`6A 02` PUSH 2; `8D 44 24 18` LEA EAX,[ESP+0x18]; `50` PUSH EAX (&cursor);
`57` PUSH EDI (receiver); `8B CE` MOV ECX,ESI; `E8 5E FE FF FF`
CALL → 0x0070DC20 (rel32 machine-computed = pinned target ✓).

## FUN_0070DC20_RETURN (structural representation)

- SUCCESS: EAX = the created class_obj pointer (a per-receiver 0x58-B
  class-20006 component, vtable 0x00A86F2C) — `8B C7` MOV EAX,EDI @0x0070DCE5.
  FUN_0070DCF0 captures it (`8B D8` MOV EBX,EAX @0x0070DDC2) and returns it
  as its own result (RET 4 @0x0070DDFF) — the class_obj of candidate A.
- FAILURE: EAX = 0; the class_obj is destroyed first (delegate vtable slot
  [vt+0x28] loaded @0x0070DCC8, called @0x0070DCCE; then class_obj
  ->vtable[0](1) destructor call @0x0070DCD0-38), unless class_obj==NULL in
  which case NULL is returned directly.

## Full decode (all branch targets machine-computed; S1/S2 pins)

```text
0x0070DC20  SUB ESP,0x10 ; PUSH EBX
0x0070DC24  MOV EBX,[ESP+0x18]        ; arg1 = RECEIVER
0x0070DC28  XOR EAX,EAX
0x0070DC2A  TEST EBX,EBX              ; receiver == NULL?
0x0070DC2C  PUSH ESI
0x0070DC2D  MOV ESI,ECX               ; this = FACTORY
0x0070DC2F  SETNE CL
0x0070DC32  TEST CL,CL
0x0070DC34  JE 0x0070DCE8             ; receiver NULL -> pop esi/ebx epilogue, EAX=0
0x0070DC3A  PUSH EDI
0x0070DC3B  PUSH EAX                  ; 0
0x0070DC3C  PUSH EBX                  ; receiver
0x0070DC3D  MOV ECX,ESI               ; this = factory
0x0070DC3F  CALL FUN_0070D990         ; class_obj = CreateDefaultComponent(factory, receiver, 0)
0x0070DC44  MOV EDI,EAX               ; EDI = class_obj (0x58-B, vtable 0x00A86F2C,
                                      ;   value table 12 entries at [class_obj+0x40],
                                      ;   factory stored at class_obj+4, DEFAULT 0 entries)
0x0070DC46  MOV EAX,[ESP+0x24]        ; arg2 = &cursor
0x0070DC4A  PUSH EAX                  ; cursor (stays on the stack: FUN_0075D8D0 is cdecl)
0x0070DC4B  CALL FUN_0075D8D0         ; mov ax,1; ret  -> AX = apply MODE WORD = 1
0x0070DC50  MOV ECX,EDI               ; this = class_obj
0x0070DC52  PUSH EAX                  ; arg1 = mode word (1)
                                      ;   arg2 = cursor (the still-pushed pointer)
0x0070DC53  CALL FUN_00726900         ; APPLY THE RECORD: writes table[slot->id] entries
0x0070DC58  TEST AL,AL
0x0070DC5A  JE 0x0070DCB3             ; apply failed -> destroy path
0x0070DC5C  PUSH EBP
0x0070DC5D  LEA EBP,[ESI+0x24]        ; factory+0x24 = CRITICAL_SECTION
0x0070DC60  MOV ECX,EBP
0x0070DC62  CALL FUN_00413440         ; EnterCriticalSection(factory+0x24)
0x0070DC67  LEA ECX,[ESP+0x10]        ; &out slot
0x0070DC6B  PUSH ECX
0x0070DC6C  LEA EDX,[ESP+0x1C]        ; &value slot (built below)
0x0070DC70  PUSH EDX
0x0070DC71  LEA ECX,[ESI+0x0C]        ; this = factory+0x0C  THE PER-RECEIVER CACHE MAP
0x0070DC74  MOV [ESP+0x18],EBX        ; key slot   = RECEIVER
0x0070DC78  MOV [ESP+0x1C],EDI        ; value slot = CLASS_OBJ
0x0070DC7C  CALL FUN_0092B660         ; map insert (receiver -> class_obj)
0x0070DC81  MOV BL,[ESP+0x1C]         ; result byte
0x0070DC85  MOV ECX,EBP
0x0070DC87  CALL FUN_00413450         ; LeaveCriticalSection(factory+0x24)
0x0070DC8C  TEST BL,BL
0x0070DC8E  POP EBP
0x0070DC8F  JE 0x0070DCB3             ; insert failed -> destroy path
0x0070DC91  CMP DWORD [ESI+0x80],0    ; factory+0x80 delegate present?
0x0070DC98  JE 0x0070DCAF             ; no delegate -> success
0x0070DC9A  MOV ECX,[ESI+0x80]        ; delegate
0x0070DCA0  MOV EDX,[ESP+0x28]        ; arg3 (mode: 2 here)
0x0070DCA4  MOV EAX,[ECX]             ; delegate vtable
0x0070DCA6  MOV EAX,[EAX+0x24]        ; vtable slot 9
0x0070DCA9  PUSH EDX                  ; mode
0x0070DCAA  PUSH EDI                  ; class_obj
0x0070DCAB  CALL EAX                  ; delegate->vtable[9](class_obj, mode)
0x0070DCAD  MOV BL,AL
0x0070DCAF  TEST BL,BL
0x0070DCB1  JNE 0x0070DCE5            ; -> return class_obj
0x0070DCB3  TEST EDI,EDI              ; destroy path
0x0070DCB5  JE 0x0070DCE5             ; class_obj==NULL -> return NULL
0x0070DCB7  CMP DWORD [ESI+0x80],0
0x0070DCBE  JE 0x0070DCD0
0x0070DCC0  MOV ESI,[ESI+0x80]
0x0070DCC6  MOV EDX,[ESI]
0x0070DCC8  MOV EAX,[EDX+0x28]        ; delegate vtable slot 10
0x0070DCCB  PUSH EDI
0x0070DCCC  MOV ECX,ESI
0x0070DCCE  CALL EAX                  ; delegate->vtable[0x28](class_obj)
0x0070DCD0  MOV EDX,[EDI]             ; class_obj vtable
0x0070DCD2  MOV EAX,[EDX]             ; vtable slot 0
0x0070DCD4  PUSH 1
0x0070DCD6  MOV ECX,EDI
0x0070DCD8  CALL EAX                  ; class_obj->vtable[0](1)  destructor+delete
0x0070DCDA..E2  pop edi/esi; XOR EAX,EAX; pop ebx; ADD ESP,0x10; RET 0xC   ; return 0
0x0070DCE5  MOV EAX,EDI               ; return class_obj
0x0070DCE7..ED  pop edi/esi/ebx; ADD ESP,0x10; RET 0xC
0x0070DCE8  (NULL-receiver entry into the shared epilogue: pop esi/ebx;
             EAX was zeroed @0x0070DC28; ADD ESP,0x10; RET 0xC)
```

## ROLE

FUN_0070DC20 = the create-and-apply orchestrator of the record path:
it (1) creates the per-receiver component with the DEFAULT-0 value table
(FUN_0070D990 — canon), (2) applies the record read by FUN_0070DCF0 through
FUN_00726900 — WHICH WRITES THE ATTRIBUTE VALUES into the component's value
table (bounded subordinate chain: FUN_00726900 -> FUN_0075F660 ->
traits->vtable[5] = FUN_009777F0 store @0x00977810), (3) inserts
(receiver -> class_obj) into the SAME factory+0x0C cache map the getter-side
lookup (FUN_0070E100) reads, and (4) notifies the factory+0x80 delegate.
FUN_0070DC20_ROLE = ATTRIBUTE_VALUE_WRITER (the store executes through the
bounded subordinate setter chain; FUN_0070DC20 itself contains no table
store instruction — see ATTRIBUTE10_WRITE_CHAIN.md for the exact writer).

## Genericity (bounded context, no deep decode of other callers)

FUN_0070DC20 has exactly TWO E8 call sites in .text (S1 xref census):
- 0x0070DDBD (FUN_0070DCF0 — candidate A, arg3=2), and
- 0x00704704 (a factory-method context: FUN_0073C870(?,1) resolves the
  factory, FUN_0070E100(factory,receiver) looks up the cache; on HIT it
  RE-APPLIES a record to the EXISTING component through the same
  FUN_0075D8D0+FUN_00726900 pair; on MISS it calls
  FUN_0070DC20(factory; receiver, cursor, 1)).
So the same write mechanism serves BOTH creation (FUN_0070DC20) and
re-application to an already-cached component (caller2 HIT path), and
FUN_0070DC20 is a generic per-factory helper (factory layout: +0x0C cache
map, +0x24 CS, +0x80 delegate, +0x84 stream, +0x88 slot array).
