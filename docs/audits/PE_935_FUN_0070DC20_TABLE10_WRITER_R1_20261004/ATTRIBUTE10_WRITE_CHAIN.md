# ATTRIBUTE10_WRITE_CHAIN — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

The bounded record-apply write chain, byte-pinned end to end. Every pin
below is machine-verified (01_RAW/S2..S5; 92/92 PASS). All VAs are pinned-EXE
VAs (image base 0x00400000).

## THE CHAIN

```text
CALL FUN_0070DC20 @0x0070DDBD            (E8 5E FE FF FF -> 0x0070DC20, machine-verified)
  this = ECX = the 20006 factory; args (receiver, &cursor, 2)
    |
    v
FUN_0070DC20 @0x0070DC3F  CALL FUN_0070D990 (canon creator)
    -> class_obj (EDI): 0x58-B component, vtable 0x00A86F2C
       (ctor store `C7 06 2C 6F A8 00` @0x007374DC in FUN_007374C0),
       factory at class_obj+4 (`89 73 04` @0x0070D9A5),
       value table = 12 entries, pointer field at class_obj+0x40
       (count = slotcount+4 `83 C1 04` @0x0070D9BB; vector ctor call
       @0x0070D9C9 -> 0x00412C50), DEFAULT value 0 per entry
       (creation loop `8B 44 19 08` @0x0070DA36 + `8D 04 82` @0x0070DA3E
       + CALL FUN_0075F6D0 @0x0070DA42 -> traits->vtable[1]=FUN_009777E0
       `MOV DWORD [EAX],0` — canon).
    |
    v
FUN_0070DC20 @0x0070DC4B  CALL FUN_0075D8D0(&cursor)   [mov ax,1; ret]
    -> AX = 1 (apply-mode WORD); the pushed cursor REMAINS as arg2
    |
    v
FUN_0070DC20 @0x0070DC53  CALL FUN_00726900(class_obj; mode=1, cursor)
    |
    v
FUN_00726900  EnterCriticalSection(class_obj+8) @0x00726912 (FUN_00413440)
  read value1 = u16 @0x00726948..54      (0xFFFF sentinel @0x0072694B)
  if value1 == 0xFFFF: read value2 = u16 (stored [ESP+0x1C] @0x00726986)
  read count  = u16 -> [ESP+0x18] @0x007269BC      ; i = 0 @0x007269C0
  if count == 0 -> skip (JBE @0x007269C8)
  APPLY LOOP 0x007269D0..0x00726A35:
    cursor flag ok? (@0x007269D0)  previous iter ok? (@0x007269D6)
    TAG = u16 from cursor @0x007269E7 (`0F B7 3C 08`)
    advance cursor by 2 (FUN_0040DE60 @0x007269EF)
    slot = FUN_0070C180(factory, tag) @0x00726A03    <- CANON SLOT GETTER
        factory = [class_obj+4] `8B 4D 04` @0x007269FC
        tag     = `0F B7 D7` @0x007269FF ; PUSH tag @0x00726A02
    slot->kind == 0 ? skip (CMP [EAX+4],0 @0x00726A08 / JE @0x00726A0C)
    ID  = slot->id  = [slot+8]   `8B 48 08` @0x00726A0E   <- ATTRIBUTE ID
    TABLE = [class_obj+0x40]    `8B 55 40` @0x00726A11   <- VALUE TABLE PTR
    DEST  = TABLE + ID*4        `8D 0C 8A` @0x00726A14   <- &table[id]
    PUSH DEST @0x00726A17 ; PUSH cursor @0x00726A18 ; MOV ECX,EAX (slot) @0x00726A19
    CALL FUN_0075F660 @0x00726A1B                          <- TRAITS DISPATCH
    |
    v
FUN_0075F660(slot; cursor, &dest)
    traits = [slot+0] `8B 08` @0x0075F662 (TEST @0x0075F664)
    if traits != NULL (audited slot 6: ArkRTTraitsInt 0x00BA937C,
       vtable 0x00A9C670 — lazy-init, never NULL, canon):
       vtable = [traits] `8B 01` @0x0075F674
       fn = [vtable+0x14] `8B 40 14` @0x0075F676   <- VTABLE SLOT 5
       PUSH &dest @0x0075F679 ; PUSH cursor @0x0075F67A
       CALL fn @0x0075F67B  ->  FUN_009777F0 (int traits slot 5)
    (traits == NULL fallback: kind/flags-based readers 0x00412D80 /
     0x004129C0 — NOT decoded; out of scope for the audited attribute)
    |
    v
FUN_009777F0(traits; cursor, &dest)   (vtable dword @0x00A9C684 = 0x009777F0,
                                      machine-verified; RET 8)
    cursor flag + bounds checks @0x009777F4 / @0x00977803
    VALUE = u32 at [cursor.base + cursor.pos]   `8B 04 10` @0x00977807  <- READ
    MOV EDX,[ESP+8] (&dest)                     @0x0097780A
    ***  MOV [EDX],EAX   `89 02` @0x00977810   ***  <- THE EXACT WRITE
    advance cursor by 4 (FUN_0040DE60 @0x00977812); RET 8
    (bounds-fail path: writes 0 to *(&dest) `C7 00 00 00 00 00` @0x0097781E
     and clears the cursor flag — still a write to the same table entry)
  loop: i++ @0x00726A26..31; JB back @0x00726A35 -> 0x007269D0
  post-loop: bl &= cursor flag @0x00726A37; JE fail @0x00726A3A
  tail: class_obj+0x30 |= value1/value2 @0x00726A4B/0x00726A50
        (mode==1 word compare `66 83 7C 24 24 01` @0x00726A53)
        mode-1 tail: read u32 length, class_obj->vtable[3](cursor, value1)
        @0x00726A98 (`8B 52 0C`) + CALL EDX @0x00726A9D — the typed blob
        read (NOT decoded; NOT needed for the attribute-10 verdict)
  LeaveCriticalSection @0x00726AB7 (FUN_00413450)
    |
    v
FUN_0070DC20 @0x0070DC7C  insert (receiver -> class_obj) into factory+0x0C
  `8D 4E 0C` @0x0070DC71 (this = factory+0x0C THE CACHE MAP)
  `89 5C 24 18` @0x0070DC74 (key slot = receiver)
  `89 7C 24 1C` @0x00726A78-..=0x0070DC78 (value slot = class_obj)
  CALL FUN_0092B660 @0x0070DC7C (canon RB-tree insert; node key @+0x10,
  value @+0x14; getter-side lookup reads node+0x14 — see
  SAME_COMPONENT_IDENTITY.md)
```

## PHASE C — HOW THE DESTINATION ATTRIBUTE IS SELECTED

The record payload contains a per-entry PROPERTY TAG (u16 read from the
cursor @0x007269E7). The tag is converted to the ATTRIBUTE ID through the
factory's schema descriptor: FUN_0070C180(factory, tag) returns
&factory->slot_array[tag] (array at factory+0x88, 16-byte slots, canon;
default 0x00BA5108 out of range — pins @0x0070C1D3/@0x0070C1DF), and the id
is slot+8. The SCHEMA WRITER sets id = TAG+4 (`83 C1 04` ADD ECX,4
@0x0070CBF6 inside FUN_0070CBC0, the SLOT_ADD appender; slot-6 call site
args `50 6A 00 6A 00 6A 01 6A 06` @0x0073758D = (traits_int, 0, 0, kind=1,
tag=6), CALL @0x00737598 — machine-verified). Therefore:

```text
tag 6  -> slot 6  -> slot->id = 6+4 = 10 -> dest = [class_obj+0x40] + 10*4 = &table[10]
```

This is a RECORD-CONTAINS-TAG + DESCRIPTOR-SUPPLIES-ID selection. The tag
values carried by any actual runtime record are runtime data (STATIC-ONLY
run); the mechanism deterministically targets &table[10] whenever the
record carries tag 6 (tag 6 is inside the hardcoded schema range 0..7).
ATTRIBUTE10_SELECTION = CONFIRMED (mechanism level).

## PHASE D — THE EXACT WRITE (terminal fields)

| Field | Value |
|---|---|
| WRITER_FUNCTION | FUN_009777F0 (int traits "read-from-cursor-and-store"; ArkRTTraitsInt vtable 0x00A9C670 slot 5) |
| WRITER_VA | 0x00977810 |
| WRITE_INSTRUCTION | `89 02` = MOV [EDX],EAX — a DIRECT byte-pinned store (not a virtual call at the write itself; the virtual dispatch [vtable+0x14] @0x0075F676 selects FUN_009777F0, and the store inside it is direct) |
| TARGET_OBJECT | the class-20006 component created inside FUN_0070DC20 by FUN_0070D990 (the same per-receiver component the audited getter later reads — SAME_COMPONENT_IDENTITY.md) |
| TABLE_BASE | [class_obj+0x40] (loaded `8B 55 40` @0x00726A11) |
| TABLE_INDEX | slot->id = tag+4 = 10 for tag 6 (loaded `8B 48 08` @0x00726A0E; +4 add @0x0070CBF6) |
| SOURCE_VALUE | u32 read from the record cursor: `8B 04 10` @0x00977807 = [cursor.base + cursor.pos] |
| SOURCE_REPRESENTATION | RECORD_FIELD (the attribute's value field inside the record payload read into the 0x80-B buffer by FUN_00971AD0; accessed through the record cursor) |
| BRANCH_CONDITIONS | receiver != NULL (@0x0070DC2A); FUN_0070D990 returns class_obj; apply-mode word = 1 (constant, from FUN_0075D8D0); count > 0 (@0x007269C8); per-iteration: cursor flag (@0x007269D0), previous-iteration success (@0x007269D6), tag-read bounds (@0x007269E3); slot->kind != 0 (@0x00726A08); traits != NULL (@0x0075F664 — audited slot 6: always per canon); cursor flag + bounds in FUN_009777F0 (@0x009777F4/@0x00977803 — else the fail-path zero-store @0x0097781E executes) |

TABLE10_WRITE = CONFIRMED.
CANDIDATE_A_WRITER_ROLE = CONFIRMED_ATTRIBUTE10_WRITER.
GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL (the immediate
writer of the value the audited getter reads from table[10] is identified:
this chain; the ULTIMATE source of the record value is NOT determined — see
Phase E).

## PHASE E — SOURCE BOUNDARY (STOPPED AS CONTRACTED)

The immediate source operand of the write is identified structurally: the
u32 at the record cursor ([cursor.base + cursor.pos], READ @0x00977807) —
i.e. a RECORD_FIELD of the payload that FUN_00971AD0 read into the 0x80-B
buffer from the factory+0x84 stream. Per the contract THIS RUN STOPS HERE:
no factory+0x84 stream setter trace, no templates.vfs / VFS / file /
network / cache / embedded-static provenance was performed or claimed.

```text
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
ULTIMATE_VALUE_SOURCE               = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED         = NO
```

## ANTI-SUCCESS-THEATER (required disclosures)

- MEASURED_QUANTITY: the writer-side destination expression
  &[class_obj+0x40] + (tag+4)*4 for tag 6, measured from the pinned-EXE
  bytes at 0x00726A11/0x00726A14/0x00726A0E/0x0070CBF6/0x00977810 — not
  inferred from the getter-side claim.
- INDEPENDENT_SOURCE_OF_TRUTH: raw byte reads of the pinned EXE
  (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe, SHA256 E7785430...,
  re-verified at S5 time), each pin machine-recomputed from the rel32 /
  opcode bytes at the exact VA.
- WHY_NON_CIRCULAR: the writer-side id 10 derives from the SCHEMA WRITER
  path (FUN_007374F0 SLOT_ADD(tag=6) -> FUN_0070CBC0 id=tag+4), which is
  upstream of and independent from the getter-side table[10] read
  (@0x004C5539..0x004C554E — independently re-pinned in S5). The two sides
  meet only at the shared storage expression [class_obj+0x40]+id*4.
- FAILURE_CASE_DETECTED: the machine battery caught and forced correction
  of multiple executor hand-analysis errors during the run (guard-pair
  rel32 slip 0x0040D440->0x00413440; a 4-byte tokenization drift inside the
  FUN_00726900 window that displaced loop call VAs; the traits-dispatch
  target hand-slip 0x0075F65C->0x0075F660; several pin-VA off-by-1/2/4
  slips; an 8-byte-stride import-walk bug) — every failure was a REAL
  mismatch reported by the battery and corrected before publication. The
  battery is demonstrably capable of failing.

## FORBIDDEN-SHORTCUT checklist (each explicitly NOT used as proof)

- "seeing integer 10 somewhere" — NOT used: the id is loaded from the
  schema descriptor at runtime ([slot+8]), pinned to tag+4 by the schema
  writer's add, not by a literal 10 on the write path.
- "+0x68 numeric equality with +0x40+10*4" — NOT used: the destination is
  computed as base+index scaling from the object's own +0x40 field, with
  object identity established separately (SAME_COMPONENT_IDENTITY.md).
- "generic table writer / same factory different component / same
  component different id / numeric 16083 / use of FUN_00971AD0 /
  templates.vfs-fun-00971AD0 / model-resource ID match" — NONE used; the
  verdict rests only on the byte-pinned chain above.
