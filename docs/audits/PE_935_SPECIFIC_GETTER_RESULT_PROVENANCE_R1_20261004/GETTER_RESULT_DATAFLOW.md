# GETTER_RESULT_DATAFLOW — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 (PHASE C)

## Claim

**GETTER_RESULT_TO_LOOKUP_KEY = CONFIRMED** — the exact u32 read from the
class component's value-table entry 10 flows to FUN_0072F880's mapfind key
with NO conversion of any kind (no zero/sign extension, no mask, no
dereference chain, no field extraction, no fallback substitution on the
audited normal branch).

## The data flow (every edge byte-pinned; see GETTER_CHAIN.md)

```
table[10]                         ; 4-byte entry at [class_obj+0x40] + 10*4
  └─ MOV EAX,[EAX] @0x004C554E    ; EAX = table[10]  (8B 00)
      MOV ESI,EAX @0x004C5550
  └─ return: MOV EAX,ESI @0x004C5563   ; FUN_004C5480 returns the u32
  └─ FUN_004C5580:
       TEST EAX,EAX @0x004C55BD        ; only a NONZERO value proceeds
       MOV [ESP+0x18],EAX @0x004C55BF  ; saved (same value)
       PUSH ESI  @0x004C55D0           ; FUN_0072F880 p2 = OUT buffer
       PUSH EAX  @0x004C55D1           ; FUN_0072F880 p1 = THE KEY
  └─ FUN_0072F880(this=registry, p1=KEY, p2=OUT):
       MOV EAX,[ESP+8] @0x0072F881     ; EAX = p1
       MOV [ESP+0x14],EAX @0x0072F894  ; rewrites the p1 slot with the SAME
                                       ; value (no-op rewrite; keeps the key
                                       ; at a stable stack address)
       LEA ECX,[ESP+0xC] @0x0072F888   ; = &p1 (the stack slot holding p1)
       PUSH ECX @0x0072F88C            ; mapfind key POINTER = &p1
       CALL FUN_004D1430 @0x0072F898    ; generic mapfind
         MOV ESI,[ESP+0xC] @0x004D143A  ; ESI = key ptr
         MOV ESI,[ESI]        @0x004D143E (8B 36)   ; key = *(u32*)&p1
         walk: CMP [node+0x10],ESI @0x004D1440      ; node id2 vs key (u32)
```

## Identity argument (why CONFIRMED and not just numeric equality)

- The value stored at table[10] is a raw u32 (SCALAR representation — the int
  traits slot-1 writes raw dwords; see GETTER_CHAIN.md).
- The same 32 bits pass through registers/stack verbatim:
  table[10] → EAX → ESI → (return EAX=ESI) → [ESP+0x18]/EAX → p1 slot →
  *(u32*)&p1. There is exactly ONE dereference creating the value
  (MOV EAX,[EAX] @0x004C554E, from the table ENTRY ADDRESS computed by
  LEA ECX,[ECX+EAX*4] @0x004C553F + the identity helper FUN_004926E0), and
  exactly ONE dereference consuming it as a key (MOV ESI,[ESI] @0x004D143E,
  where [ESI] is the p1 STACK SLOT — the same bits, at a stack address).
- No arithmetic is applied between acquisition and key use: the SELECTED_VALUE
  (slot6+8 = 10) is used only as the table INDEX; the KEY is the table ENTRY.
- The only branch between them is the null check TEST EAX,EAX @0x004C55BD
  (key==0 aborts before the lookup; it never substitutes another value).

## The table-entry addressing (machine-verified idiom match)

The getter's index computation `MOV ECX,[ESI+0x40]; LEA ECX,[ECX+EAX*4]`
(@0x004C553C/0x004C553F) matches, instruction-for-instruction, the value-table
population loop in the class_obj creator `MOV EAX,[ECX+EBX+8]; LEA
EAX,[EDX+EAX*4]` (@0x0070DA36/0x0070DA3E) — the SAME table, the SAME
4-byte-element layout, the SAME id-keyed addressing on both the writer side
(creation defaults) and the reader side (the audited getter). This is the
byte-level evidence that the getter reads the entry whose initialization this
run decoded (attribute id 10 ← slot 6), i.e. the storage identity is
established, not inferred from numeric coincidence.

## Boundary statements

- SELECTED_VALUE = slot6+8 = 10 is the ATTRIBUTE ID at creation; no later
  writer of slot+8 was identified (the appender FUN_0070C980 treats slot+8-4
  as the immutable tag). Whether any runtime path mutates slot+8 is NOT
  excluded by a dedicated census; the claim "SELECTED_VALUE == 10 at
  creation" is CONFIRMED, the "always 10" reading is the default expectation,
  not an exhausted negative.
- The VALUE at table[10] is runtime-mutable per-instance state; its actual
  producer is the subject of PRODUCER_PROVIDER_CHAIN.md (UNRESOLVED within
  this run's budget). CONFIRMED here is only the IDENTITY of the data flow,
  not the value's origin.
- Numeric-equality discipline: no claim in this chain relies on any integer
  matching any other integer; every edge is an instruction/dataflow identity.
