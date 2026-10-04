# PRODUCER_PROVIDER_CHAIN — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 (PHASES D + E)

## Where the audited value lives (CONFIRMED)

The LOOKUP KEY consumed by FUN_0072F880 is the u32 at:

    *(u32*)( [class_obj+0x40] + 10*4 )

i.e. entry 10 (attribute id 10 = property tag 6, int-typed) of the
per-receiver 20006-class component's VALUE TABLE. The table is a 12-entry
(= 8 slots + 4 fixed members) vector created with the class_obj.

## Provenance layers established this run

| Layer | Producer | Evidence | Provenance class |
|---|---|---|---|
| Attribute SCHEMA (slot 6 exists; kind=1 int; id=10; flags=0; int-traits obj) | FUN_007374F0 @0x00737598 (SLOT_ADD(factory, 6, 1, 0, 0, traits_int)) inside the factory lazy-init @0x0073E312 | byte-pinned args `50 6A 00 6A 00 6A 01 6A 06` @0x73758D; slot field layout FUN_0075F5C0; appender FUN_0070C980 | CONSTANT_INITIALIZATION |
| Traits object (int) | FUN_00977A50: vtable 0x00A9C670 stored into static 0x00BA937C @0x00977A68 (20002_PAYLOAD30 canon corroboration: ArkRTTraitsInt, lazy-init, never NULL) | byte-pinned | CONSTANT_INITIALIZATION (static singleton) |
| Value-table INITIAL value | creation loop in FUN_0070D990: `MOV EAX,[slot+8]; LEA EAX,[table+id*4]; CALL FUN_0075F6D0` → traits->vtable[1] = FUN_009777E0 → `MOV DWORD [EAX],0` | byte-pinned @0x0070DA36/0x0070DA3E/0x0070DA42; vtable 0x00A9C670 slot 1 = 0x009777E0 | CONSTANT_INITIALIZATION (initial 0) |
| The ACTUAL runtime value (any nonzero id2 the builder consumes) | **NOT IDENTIFIED within this run's function budget** — see candidates below | bounded | UNKNOWN |

The initial 0 can never be a consumed key: FUN_004C5580 aborts at
TEST EAX,EAX / JE 0x004C5AB6 @0x004C55BD/0x004C55C3 when the getter returns 0.
Therefore any REAL lookup key on the audited path was written into
table[10] AFTER class_obj creation, by a per-instance value writer.

## Candidate value-writers (bounded; NOT decoded to conclusion)

### Candidate A — the record-read early creator (STRONG lead, byte-pinned shell)

FUN_0070DE10 (cache-miss creator) early path:
manager mode (=[FUN_00415470 singleton]->field0) ∈ {1,2} AND factory+0x84
non-NULL → `MOV EAX,[ESP+0x1C]; PUSH EAX; MOV ECX,EDI; CALL FUN_0070DCF0`
(@0x0070DE37, RET 8).

FUN_0070DCF0(factory, receiver) decodes (byte-pinned):
1. factory+0x84 == NULL → return 0 (@0x0070DD17/1D).
2. vector ctor FUN_0040E160(&cursor, 0x80, 1) @0x0070DD39; alloc a 0x80-byte
   record buffer (PUSH 0x80 @0x0070DD28; allocator thunk 0x0095D3BE family);
   MOV [ESP+0x1C],0x80.
3. **CALL FUN_00971AD0 @0x0070DD75** — thiscall this=[factory+0x84], args
   (receiver, &cursor, &size): **THE PER-RECORD READER of the templates.vfs
   parser chain (R1 canon: reader FUN_0072FA30 → per-record read
   FUN_00971AD0 → parse FUN_00730C90)**. Machine-verified target.
4. FUN_00971650([factory+0x84]) @0x0070DD84 (advance/verify); size check
   (record+8 ≤ 0x80 @0x0070DD95-A0); cursor advance by 8 via FUN_0040DE60
   @0x0070DDA8 (the C1-canon cursor helper).
5. **CALL FUN_0070DC20(factory, receiver, &cursor, 2) @0x0070DDBD** — apply
   the read record to the receiver; its return becomes the class_obj.
6. Failure → buffer cleanup, return 0.

So candidate A reads ONE RECORD from a stream attached at factory+0x84 and
applies it to the receiver. The stream is NULL at factory init
(FUN_0070CF80 zeroes +0x84 @0x0070D013); its setter/backing data (file-backed
VFS? network buffer? embedded class data?) is **NOT identified** — that is the
next missing edge. Because FUN_00971AD0 is the SAME reader family used over
templates.vfs records, a physical-record source is PLAUSIBLE, but NOTHING in
this run ties factory+0x84's stream to templates.vfs or any other file.

### Candidate B — the delegate bind (weak, byte-pinned shell)

FUN_0070DE10 else-path: factory+0x80 (a delegate object, NULL at init,
setter NOT identified) → ESI = FUN_0070D990(factory, receiver, 0) (class_obj
with DEFAULT-0 table) → `factory+0x80->vtable[1](ESI, &out)` virtual bind
(@0x0070DE6F: `8B 11; 8B 52 04; ...; FF D2`) → on success insert into the
cache map (FUN_0092B660) and notify via `factory+0x80->vtable[9](ESI, 2)`
(@0x0070DEDC-E2). The concrete delegate class and its bind implementation
are NOT identified (polymorphic call, statically unresolvable without the
delegate object's provenance).

## PHASE E — setter/provider identity search (bounded)

- The symmetric mechanism found: SLOT_ADD (FUN_0070CBC0) is the SCHEMA setter
  (writes slot definitions; used only by the factory init chain per its
  call census: 8 sites, all in FUN_007374F0). It writes the DEFINITION
  (traits/kind/id/flags), never the runtime VALUE of table[id].
- The runtime VALUE setter must write [class_obj+0x40]+id*4. No direct writer
  was identified within the budget (the class_obj vtable 0x00A86F2C is the
  natural home of the setter virtuals — slot enumeration of that vtable and
  its per-instance "set value" path is the designed-not-executed next
  experiment). FUN_0070DC20 (the record-apply in candidate A) is the only
  byte-pinned function that both runs after creation and receives
  (receiver, cursor) — it is the leading candidate value-writer.
- Per the contract's preferred bounded control, the SETTER SIDE is
  discriminated from the getter side by CONTROL-A (CONTROL_CASE.md): tags
  2/4 use the SAME SLOT_ADD mechanism with the SAME int traits but produce
  DIFFERENT table indices (6/8) — the mechanism does not collapse into a
  single shared value source.

## Per-candidate record (contract format)

| Field | Candidate A (record-read creator) | Candidate B (delegate bind) |
|---|---|---|
| FUNCTION/VA | FUN_0070DCF0 / 0x0070DCF0 (gated @0x0070DE27-37) | FUN_0070DE10 else-path / 0x0070DE43-0x0070DF09 |
| RECEIVER | the entity's 20006 class_obj (created fresh from the record) | the entity's 20006 class_obj (FUN_0070D990) |
| TAG/FIELD/OFFSET | value-table entries of the new class_obj (via FUN_0070DC20 apply) | value-table entries (via the +0x80 delegate's vtable[1] bind) |
| SOURCE VALUE | ONE record (≤0x80 bytes + 8-byte framing) read from factory+0x84 stream | unknown (delegate-internal) |
| SOURCE OBJECT | factory+0x84 STREAM (identity/backing UNKNOWN; NULL at factory init) | factory+0x80 DELEGATE (identity UNKNOWN; NULL at factory init) |
| CALLER | FUN_0070DE10 early path (manager mode ∈ {1,2}) | FUN_0070DE10 else-path |
| BRANCH CONDITIONS | mgr mode 1/2 AND factory+0x84 != 0 | otherwise AND factory+0x80 != 0 |
| PROVENANCE CLASS | UNKNOWN (reader family shared with templates.vfs parser — physical source PLAUSIBLE, NOT ESTABLISHED) | UNKNOWN |
| EVIDENCE STATUS | shell byte-pinned; internal semantics (FUN_0070DC20, stream source) NOT decoded | shell byte-pinned; delegate NOT identified |

## Terminal statement

GETTER_RESULT_PROVENANCE = UNKNOWN (the actual runtime value's origin).
PRODUCER_PROVIDER_IDENTITY = UNRESOLVED for the actual value (the schema
producer, storage, and initial value are CONFIRMED — see above).
The function budget (28 detailed functions > MAX 20) stopped the backward
trace at FUN_0070DC20 / the factory+0x84 stream identity /
the factory+0x80 delegate identity.
