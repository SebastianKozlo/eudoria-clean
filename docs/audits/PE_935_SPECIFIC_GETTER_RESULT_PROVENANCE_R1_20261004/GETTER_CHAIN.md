# GETTER_CHAIN — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 (PHASE B)

MODE: STATIC-ONLY. All instruction identities are byte reads from the pinned
Entropia.exe (SHA256 E7785430..., verified in 01_RAW/S11_QC_BATTERY.json;
45/45 call-target checks PASS, 33/33 instruction pins PASS). Every rel32 call
target in this chain is machine-verified (03_SCRIPTS/s11_qc_battery.py).

## The audited path (byte-pinned end-to-end)

```
FUN_00567770 (placement builder)
  └─ CALL FUN_004C5580 @0x005678BA           (args: entity, &out_template)
      ├─ PUSH EDI; CALL FUN_004C5480 @0x004C55B5   (arg = entity)
      │   ├─ MOV EDI,[ESP+0x30] @0x004C54A5          ; entity = arg1
      │   ├─ (1) RECEIVER RESOLVE
      │   │    resolved = FUN_00843DD0(entity, &L) @0x004C54B2
      │   │      = [entity+4] ? *FUN_00747970([entity+4], &L) : 0
      │   │      (FUN_00747970 surface-identified only — not decoded within budget)
      │   ├─ (2) CLASS_SELECTOR PAIR
      │   │    MOV [ESP+0x1C],0x4E26 @0x004C54C2   (C7 44 24 1C 26 4E 00 00)
      │   │    MOV [ESP+0x20],EAX   @0x004C54CA   (the resolved receiver)
      │   ├─ (3) CLASS-SELECTOR RESOLVE
      │   │    class_obj = FUN_00703B80(&result, &pair) @0x004C54CE
      │   │      ├─ mgr = FUN_00415470() @0x00703B88   (lazy singleton 0x100 B
      │   │      │    at 0x00BA12E4; ctor FUN_00707E50)
      │   │      └─ FUN_00703D70(mgr, &pair) @0x00703B8F
      │   │           ├─ factory = FUN_0073C870(20006, 1) @0x00703D7D
      │   │           │    CMP ECX,0x4E20 @0x0073C876; JA→selector>20000 path
      │   │           │    ADD ECX,-0x4E21 @0x0073C8A5; JMP [ECX*4+0x0073C9FC]
      │   │           │    → entry 5 (selector 20006) → 0x0073C8D8:
      │   │           │      MOV EAX,[0x00BA590C]; RET   ← THE 20006 FACTORY
      │   │           │      (lazy singleton: alloc 0x118 @0x0073E2CC →
      │   │           │       ctor FUN_0073B820 @0x0073E2EB → store
      │   │           │       @0x0073E303 (A3) → FUN_0070E2F0(f,8,0) →
      │   │           │       FUN_007374F0(f) @0x0073E312 → FUN_0070C150 →
      │   │           │       FUN_0070BF10; zero-on-fail @0x0073E348)
      │   │           └─ class_obj = FUN_0070E100(factory, receiver) @0x00703D8F
      │   │                = get-or-create PER-RECEIVER component:
      │   │                  lock factory+0x24 critsec; mapfind factory+0x0C
      │   │                  keyed by &receiver (FUN_004D1430 @0x0070E124);
      │   │                  hit → node+0x14; miss → FUN_0070DE10 (see
      │   │                  PRODUCER_PROVIDER_CHAIN.md) → cache insert
      │   ├─ (4) NULL CHECK + BRANCH PREDICATE
      │   │    CMP [ESP+0x0C],ESI; JE 0x004C5552 @0x004C54D3/DB (no class_obj
      │   │    → return 0)
      │   │    PUSH 0xD82 @0x004C54DD; MOV ECX,EDI; CALL FUN_00844020 @0x004C54E4
      │   │    TEST AL,AL; JE 0x004C5518 @0x004C54EB
      │   │    → flag 0xD82 NOT set on the entity = THE AUDITED NORMAL BRANCH
      │   │      (the flag-set alternative is bounded in ALTERNATIVE_BRANCH.md)
      │   ├─ (5) PROPERTY_TAG 6 GETTER (normal branch @0x004C5518)
      │   │    MOV EAX,[ESP+0x0C] @0x004C5518            ; class_obj
      │   │    MOV ECX,[EAX+4]   @0x004C551C (8B 48 04)  ; getter receiver
      │   │      ★ [class_obj+4] == THE FACTORY (pinned by MOV [EBX+4],ESI
      │   │        @0x0070D9A5 in the class_obj creator FUN_0070D990)
      │   │    PUSH 6            @0x004C551F (6A 06)     ; PROPERTY_TAG 6
      │   │    CALL FUN_0070C180 @0x004C5523
      │   │      = &((BYTE*)[factory+0x88])[6*16]        ; 16-byte slot address
      │   │      count = ([factory+0x8C]-[factory+0x88])>>4; out-of-range →
      │   │      static default slot 0x00BA5108 (permanently ZERO — no writers)
      │   │      0x8000-masked tags → fixed members &factory+0xD8/E8/F8/108
      │   ├─ (6) DESCRIPTOR VALIDITY + SELECTED_VALUE
      │   │    MOV ECX,[EAX+4]   @0x004C5528            ; slot.kind
      │   │    TEST ECX,ECX; JE 0x004C5549 @0x004C552B/D (kind 0 → fallback)
      │   │    CMP ECX,1; JNE 0x004C5549  @0x004C552F/32 (kind != 1 → fallback)
      │   │    TEST [EAX+0xC],CL @0x004C5534 (84 48 0C) ; flags bit 0
      │   │    JNE 0x004C5549      @0x004C5537          ; bit set → fallback
      │   │    MOV EAX,[EAX+8]   @0x004C5539 (8B 40 08) ; SELECTED_VALUE =
      │   │                                                  slot6+8 = attr ID
      │   ├─ (7) VALUE-TABLE LOOKUP (the class component's current values)
      │   │    MOV ECX,[ESI+0x40] @0x004C553C           ; table begin (ESI=class_obj)
      │   │    LEA ECX,[ECX+EAX*4] @0x004C553F          ; &table[attr_id]
      │   │    CALL FUN_004926E0 @0x004C5542            ; MOV EAX,ECX; RET (identity)
      │   │    MOV EAX,[EAX]    @0x004C554E (8B 00)     ; ★ THE KEY = table[id]
      │   │    MOV ESI,EAX      @0x004C5550
      │   │    (fallback @0x004C5549: CALL FUN_00977780 → MOV EAX,0x00BA9374;RET
      │   │     → [0x00BA9374] = 0 (no writers, .data virtual tail) → returns 0)
      │   └─ epilogue: FUN_00703BC0 cleanup @0x004C555E; return EAX = ESI
      ├─ TEST EAX,EAX @0x004C55BD; JE 0x004C5AB6 @0x004C55C3 (key==0 → abort)
      ├─ PUSH ESI (out buffer); PUSH EAX (the u32 key)
      ├─ CALL FUN_0043A550 @0x004C55D2 (registry root DAT_00BA1824 singleton)
      └─ CALL FUN_0072F880 @0x004C55D9 (thiscall: this=registry, p1=KEY, p2=OUT)
           ├─ FUN_004D1430(registry, &L, &p1) @0x0072F898  (generic mapfind)
           │    key = *(u32*)&p1 @0x004D143E (8B 36)     ← THE KEY DEREF
           │    walk: CMP [node+0x10],key; node+0x10 = id2 (R1 canon)
           ├─ found → ESI = node+0x14; miss → ESI = 0x00BA5800 (default template)
           ├─ FUN_0072FCE0 @0x0072F8AF (validity: id2≠0 && (A≠0||B≠0||C≠0))
           └─ FUN_0072F7A0(out, template) @0x0072F8BD (full-field copy) → AL=1
```

## The four identities (explicitly separated, per contract)

| Identity | Value | Evidence |
|---|---|---|
| GETTER_RETURN_OBJECT | the class_obj's 0x40 value-table ENTRY SLOT at index slot6+8 (i.e., &table[attr_id 10]) | LEA ECX,[ECX+EAX*4] @0x004C553F + identity helper |
| GETTER_RETURN_DESCRIPTOR | the 16-byte factory slot 6 at &[factory+0x88]+6*16: {+0: traits obj (int), +4: kind=1, +8: attr id=10, +0xC: flags=0} | FUN_0070C180 decode + FUN_0075F5C0 field layout + SLOT_ADD call @0x00737598 |
| SELECTED_VALUE | slot6+8 = the attribute ID = tag+4 = 10 (at creation; no later writer of slot+8 identified) | MOV EAX,[EAX+8] @0x004C5539; FUN_0075F5C0 MOV [EAX+8],ECX with ECX=tag+4; appender FUN_0070C980 re-derives tag as slot+8-4 |
| LOOKUP_KEY | the CURRENT u32 stored at class_obj value-table entry 10 = table[10] | MOV EAX,[EAX] @0x004C554E → returned → FUN_0072F880 p1 → *(u32*)&p1 |

GETTER_RETURN_REPRESENTATION = SCALAR (raw u32; the int traits' slot-1 method
FUN_009777E0 writes `MOV DWORD [EAX],0` — a raw u32, not a pointer; the
no-traits fallback in FUN_0075F6D0 allocates a 12-byte object, but slot 6
always has the int traits object, so the int representation is the live one).

## Slot 6 provenance (the attribute definition — CONSTANT_INITIALIZATION)

The factory's 8-slot array is built by FUN_007374F0 (called from the factory
lazy-init @0x0073E312) via 8 SLOT_ADD (FUN_0070CBC0) calls, machine-verified:

| tag | kind | traits factory | attr id (tag+4) | call site |
|---|---|---|---|---|
| 0 | 4 | FUN_0040A290 | 4 | 0x0073751A |
| 1 | 3 | FUN_00977CE0 | 5 | 0x0073752F |
| 2 | 1 (int) | FUN_00977A50 | 6 | 0x00737544 |
| 3 | 4 | FUN_0040A290 | 7 | 0x00737559 |
| 4 | 1 (int) | FUN_00977A50 | 8 | 0x0073756E |
| 5 | 2 | FUN_00977AD0 | 9 | 0x00737583 |
| **6** | **1 (int)** | **FUN_00977A50** | **10** | **0x00737598** |
| 7 | 2 | FUN_00977AD0 | 11 | 0x007375AD |

The AUDITED slot-6 add arguments are byte-pinned @0x73758D:
`50 6A 00 6A 00 6A 01 6A 06` = PUSH traits_int; PUSH 0; PUSH 0; PUSH 1 (kind);
PUSH 6 (tag). FUN_00977A50 = the ArkRTTraitsInt factory (20002_PAYLOAD30
canon: lazy-init, never NULL, vtable 0x00A9C670 stored @0x00977A68 into the
static object 0x00BA937C). SLOT_ADD → FUN_0075F5C0 writes the slot fields
{+0: traits, +4: kind, +8: tag+4, +0xC: p3=0}; FUN_0070C980 appends it
(sequential-tag check: slot+8-4 must equal current count).

## The value table ([class_obj+0x40])

Populated at class_obj creation (FUN_0070D990): vector init
FUN_00412C50(&class_obj+0x40, slotcount+4 = 12 entries); table[0..3] ←
traits-default copies of the factory's four fixed members (+0xD8/+0xE8/
+0xF8/+0x108); then a loop over the factory's slots:
`MOV EAX,[ECX+EBX+8]` @0x0070DA36 (slot+8 = attr id) →
`LEA EAX,[EDX+EAX*4]` @0x0070DA3E (&table[id]) →
CALL FUN_0075F6D0 @0x0070DA42 (dispatch: traits->vtable[1](this=traits,
arg=&table[id]) — tail JMP @0x0075F6E8). For the int traits the slot-1 method
FUN_009777E0 writes `MOV DWORD [EAX],0` — the INITIAL VALUE 0.

So: the audited getter reads table[10] = the class component's CURRENT VALUE
of attribute id 10 — NOT a constant, NOT the slot payload itself.
