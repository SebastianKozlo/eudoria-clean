# SAME_COMPONENT_IDENTITY — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

PHASE B — proof that the write target is the SAME structural class-20006
component family the audited getter reads. All pins machine-verified
(01_RAW/S2..S5).

## The identity chain (writer side -> shared storage -> getter side)

### 1. Writer side: the component is created and filled INSIDE FUN_0070DC20

- FUN_0070DC20 calls the CANON default creator:
  `E8 4C FD FF FF` @0x0070DC3F -> FUN_0070D990(factory, receiver, 0).
- FUN_0070D990 is the SAME creation function the R1 canon decoded
  (class_obj with DEFAULT-0 value table). Its product is byte-pinned:
  - component ctor FUN_007374C0 stores vtable 0x00A86F2C
    (`C7 06 2C 6F A8 00` @0x007374DC) — THE canon component vtable;
  - factory stored at class_obj+4 (`89 73 04` @0x0070D9A5) — the canon
    "getter receiver [class_obj+4] IS the factory" object;
  - value table = slot_count+4 = 12 entries (`83 C1 04` @0x0070D9BB +
    vector ctor @0x0070D9C9 -> 0x00412C50), pointer field at class_obj+0x40;
  - the ctor takes its factory from the lazy singleton
    `8B 0D 0C 59 BA 00` ([0x00BA590C]) in FUN_007374C0 — every component is
    bound to THE one 20006 factory singleton.
- FUN_00726900's apply loop receives this exact object as `this`
  (`8B E9` MOV EBP,ECX @0x00726905) and writes into ITS value table
  (`8B 55 40` @0x00726A11 reads [class_obj+0x40] of THIS object).

### 2. The shared binding: the factory+0x0C per-receiver cache map

FUN_0070DC20 inserts the object it just created and filled:

```text
0x0070DC71  LEA ECX,[ESI+0x0C]     ; this = factory+0x0C  (THE cache map)
0x0070DC74  MOV [ESP+0x18],EBX     ; key slot   = RECEIVER (arg1)
0x0070DC78  MOV [ESP+0x1C],EDI     ; value slot = CLASS_OBJ (the created object)
0x0070DC7C  CALL FUN_0092B660      ; RB-tree insert (canon; node key @+0x10, value @+0x14)
```

### 3. Getter side: the SAME map + SAME key resolve to that object

The getter-side component acquisition (canon FUN_0070E100, re-pinned):

```text
0x0070E11E  LEA EDI,[ESI+0x0C]     ; the SAME factory+0x0C map
0x0070E124  CALL FUN_004D1430      ; the canon generic mapfind (key = receiver)
0x0070E131  MOV EBP,[EAX+0x14]     ; node+0x14 = VALUE = the cached class_obj
```

and the audited getter chain (R1 canon, independently re-pinned this run)
reads that object's value table:

```text
0x004C5523  CALL FUN_0070C180      ; slot getter (factory, property tag)
0x004C5539  MOV EAX,[EAX+8]        ; id = slot->id (slot 6 -> 10)
0x004C553C  MOV ECX,[ESI+0x40]     ; table = [class_obj+0x40]
0x004C553F  LEA ECX,[ECX+EAX*4]   ; &table[id]
0x004C554E  MOV EAX,[EAX]          ; the current u32 -> the FUN_0072F880 key
```

### 4. Why this is identity-preserving (not numeric coincidence)

- SAME MAP OBJECT: writer inserts into factory+0x0C of the SAME factory
  singleton (0x00BA590C) that the getter-side chain resolves (the factory
  enters FUN_0070DC20 as `this` from FUN_0070DCF0, which received it from
  FUN_0070DE10 — the canon cache-miss creator of the SAME factory).
- SAME KEY: the receiver pointer — FUN_0070DC20 writes it into the insert
  key slot (@0x0070DC74) from its own arg1; the getter-side mapfind
  (FUN_004D1430 inside FUN_0070E100) looks up the same map with the same
  receiver key.
- SAME VALUE OBJECT: the inserted value (@0x0070DC78) IS the object the
  apply loop wrote into (EDI from FUN_0070D990, EBP inside FUN_00726900).
- CROSS-CHECK: FUN_0092B660's tree comparison loads the key through the
  slot pointer (`8B 03` = receiver-pointer value) and compares with
  node+0x10 (the canon key field) — pointer identity, not value equality.
- The second call site of FUN_0070DC20 (@0x00704704) demonstrates the same
  map discipline from the other side: it calls FUN_0070E100(factory,
  receiver) FIRST (the same lookup), and only on MISS calls
  FUN_0070DC20 — i.e. creation and lookup are mutexed around one map.

SAME_COMPONENT_IDENTITY = CONFIRMED
(chain form (B)/(C): the exact per-receiver cache lookup keyed by the
receiver resolves to the same class_obj the writer chain created, filled,
and inserted).

## Scope honesty

- STATIC-ONLY: whether the candidate-A path executes at runtime (manager
  mode in {1,2} + factory+0x84 stream non-NULL) is runtime state (R1 canon
  gate, not reopened). The identity claim is structural: WHEN this path
  runs, the written object IS the object the getter-side map returns for
  the same receiver.
- The component vtable/factory/table-layout pins are canon reverifications
  (R1), re-pinned by this run's battery; no new semantic claim is derived
  from them beyond the identity chain above.
