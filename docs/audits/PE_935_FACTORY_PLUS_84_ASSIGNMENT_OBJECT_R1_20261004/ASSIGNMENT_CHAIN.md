# ASSIGNMENT_CHAIN.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004

PHASES B, C, E, F. All instruction identities are machine-verified byte reads from
the pinned Entropia.exe (SHA256 E7785430..., S1 pin battery 0 failures; every rel32
target machine-computed). STATIC-ONLY — the client never ran.

## THE ANSWER IN ONE PARAGRAPH

factory+0x84 is assigned by exactly TWO confirmed mechanisms within the census bound:

1. **INITIALIZATION_NULL**: the factory base constructor FUN_0070CF80 stores
   `MOV [ESI+0x84],EBX` with EBX=0 (`89 9E 84 00 00 00` @0x0070D013; XOR EBX,EBX
   @0x0070CFBC) during the construction of EVERY factory class — including the 20006
   factory, whose derived ctor FUN_0073B820 calls it
   (`PUSH 0x4E26` @0x0073B871 + `CALL FUN_0070CF80` @0x0073B87D, target
   machine-verified) — so the member starts NULL.

2. **NONNULL_ASSIGNMENT (THE SETTER)**: FUN_0070C680 — the factory-class
   stream-attach method — stores `MOV [ESI+0x84],EAX` (`89 86 84 00 00 00`
   @0x0070C71E) with ESI = this and EAX = a **new(0xA4) heap object constructed by
   FUN_00972380** (CALL @0x0070C715), or 0 if the allocation fails
   (`XOR EAX,EAX` @0x0070C71C). The store executes ONLY when the member is NULL at
   entry (guard `CMP [ESI+0x84],EDI` @0x0070C6BE / `JE` @0x0070C6C4 → return TRUE if
   already attached) — a guarded, idempotent lazy attach.

## PHASE B — FACTORY IDENTITY AT THE ASSIGNMENT (identity-preserving chain)

The setter's `this` is NOT statically a singleton load — it is a manager-list
element. The identity chain that ties the store to THE consumer's factory:

```text
[0x00BA590C] THE 20006 factory singleton
   |  (the ONLY 9 .text references to 0x00BA590C are: the getter 0x0073C8D8,
   |   the lazy-init chain @0x0073E2B1..0x0073E348, and the class_obj ctor
   |   read @0x007374C4 — S1 census, count machine-measured = 9)
   |
   v  e1: FUN_0073C870 dispatcher (jump table @0x0073C9FC, entry 5 for selector
   |      0x4E26=20006 -> 0x0073C8D8 -> MOV EAX,[0x00BA590C]; RET)
   |      THE SAME RESOLVER serves BOTH sides:
   |        consumer side: FUN_00703D70 CALL FUN_0073C870 @0x00703D7D
   |                       (prior canon chain -> FUN_0070E100 -> FUN_0070DE10
   |                        -> FUN_0070DCF0 reads [factory+0x84])
   |        registration: FUN_00707FB0 CALL FUN_0073C870 @0x00707FDF
   v  e2: FUN_00707FB0 (THE REGISTER): factory = dispatcher(class_id, 1);
   |      EDI = EAX (MOV EDI,EAX @0x00707FE4) — pointer used UNMODIFIED;
   |      vector push into the manager's factory list:
   |        MOV EAX,[EBX+0x7C]     (list end)   @0x00708065
   |        CMP EAX,[EBX+0x80]      (capacity)  @0x00708068
   |        LEA ECX,[EBX+0x78]      (list begin)@0x0070806E
   |        MOV [EAX],EDI           (*end = factory) @0x00708077
   |        ADD [ECX+4],4           (end += 4)  @0x00708079
   |      EBX = the manager (MOV EBX,ECX @0x00707FD6; the manager comes from
   |      FUN_00415470 — new(0x100) + ctor FUN_00707E50 + store [0x00BA12E4];
   |      its ctor zeroes the list triple +0x78/+0x7C/+0x80)
   v  e3: FUN_007080C0 (THE MANAGER-MODE INIT + CLASS ENUMERATION):
   |      arg1 -> [this+0] = THE MANAGER MODE (MOV [EDI],EAX @0x007080CA);
   |      enumerates class ids 0x4E20..0x4E4B (20000..20043) and 0x5DC1..0x5DD1
   |      (24001..24017), calling FUN_00707FB0 per id (CALLs @0x007080E3 /
   |      @0x007080FB) — 20006 (0x4E26) is INSIDE the first range;
   |      sole caller 0x00417524 passes arg=2 (mode 2)
   v  e4: FUN_004B0980 (THE DRIVER): builds locals with the string constants
   |      "Cache\" (PUSH @0x004B09CD) and "Parameters\" (PUSH @0x004B09F3);
   |      sets locals {EBX, 0x80, 8} (@0x004B0A42/46/4E); CALL FUN_00415470
   |      @0x004B0A56; MOV ECX,EAX; CALL FUN_00703E80 @0x004B0A5D with four
   |      pointers into its local frame
   v  e5: FUN_00703E80 (THE BULK-ATTACH LOOP): iterates [this+0x78]..[this+0x7C]
   |      stride 4 (MOV ESI,[ECX+0x78] @0x00703E87; ADD ESI,4 @0x00703EF5);
   |      per element: MOV EDI,[ESI] @0x00703EA7; MOV ECX,EDI @0x00703EB0 —
   |      the CONDITION battery (byte-pinned):
   |        CALL FUN_00703CD0 @0x00703EA9  -> manager mode in {1,3}?
   |        if yes: PUSH 0x40; CALL FUN_0070CC80 @0x00703EB6
   |                (slot-array predicate scan over [+0x88..+0x8C), callback
   |                 0x0070BEF0 — callback internal rule NOT decoded, disclosed)
   |        if no:  PUSH 0x20;  CALL FUN_0070BF40 @0x00703EC5 (14-byte helper,
   |                transcription-level, internal rule not load-bearing)
   |                else PUSH 0x2000; CALL FUN_0070BF40 @0x00703EE3
   |      on pass: MOV ECX,[ESI] (@0x00703EDC / @0x00703EEC); PUSH EBX (arg2);
   |      PUSH EBP (arg3); CALL FUN_0070C680 @0x00703EF0
   v  e6: FUN_0070C680 (THE SETTER): this = the list element;
          MOV ESI,ECX @0x0070C6BA; guard CMP [ESI+0x84],EDI @0x0070C6BE;
          ... new(0xA4) @0x0070C6F9; CALL FUN_00972380 @0x0070C715;
          MOV [ESI+0x84],EAX @0x0070C71E  *** THE ASSIGNMENT ***
```

**FACTORY_IDENTITY_AT_ASSIGNMENT = CONFIRMED** (identity-preserving): the pointer
stored at *list_end is the SAME dispatcher-resolved singleton object the consumer
chain resolves (both call FUN_0073C870 with selector 20006 → the same
`[0x00BA590C]` object; the registration stores the resolved pointer without
substitution; the loop passes the list element into ECX without substitution; the
setter stores through ESI = that ECX). This is the contract's "same singleton
resolved+propagated without substitution" chain, with the byte-pinned conditional
resolution (mode ∈ {1,3} → slot-predicate-0x40; else element-flag 0x20; else 0x2000)
fully pinned at instruction level. WHETHER the condition passes for any particular
factory at any particular runtime event is RUNTIME STATE (STATIC-ONLY run; the same
discipline as the predecessor's "WHEN this path runs..." verdicts).

## PHASE C — WRITE CLASSIFICATION (measured counts)

| Count field | Value | Rows |
|---|---|---|
| FACTORY_PLUS_84_NULL_INIT_COUNT | **1** | 0x0070D013 (FUN_0070CF80, base ctor, EBX=0) |
| FACTORY_PLUS_84_CLEAR_RESET_COUNT | **0** | no clear/reset store of the member found within the census bound |
| FACTORY_PLUS_84_NONNULL_ASSIGNMENT_COUNT | **1** | 0x0070C71E (FUN_0070C680, EAX = new(0xA4)+FUN_00972380 object, or 0 on alloc-fail) |
| FACTORY_PLUS_84_UNRESOLVED_WRITE_COUNT | **129** | census rows classified UNRESOLVED at window level (see QC_REPORT Q9 for the exact split: non-stack dword candidates unresolved + partial-width + linked-LEA candidates) |

Census totals (01_RAW/S2_CENSUS.json): 2,604 raw hits; 483 dword-write-form hits;
74 with non-stack base (70 boundary-verified); 2 CONFIRMED_FACTORY_PLUS_84_WRITE;
the rest mechanically rejected (reads 598, wrong-object 1,488 incl. all stack-based
SIB forms, unrelated-offset 387, unresolved 129). The two confirmed rows are the
ONLY +0x84 writes inside the factory-family code region (0x0070BF00..0x0073F600).

## PHASE E — ASSIGNMENT → CONSUMER FIELD IDENTITY (member relationship only)

FACTORY_PLUS_84_CONSUMER_FIELD = **CONFIRMED**: the consumer FUN_0070DCF0 receives
the factory as this (`MOV ESI,ECX` @0x0070DD16) and addresses the SAME member:
- gate: `CMP [ESI+0x84],EBX` @0x0070DD1A / `JE` @0x0070DD20 (NULL → return 0)
- `MOV ECX,[ESI+0x84]` @0x0070DD6A → `CALL FUN_00971AD0` @0x0070DD75 (the
  per-record reader, this = the member's object)
- `MOV ECX,[ESI+0x84]` @0x0070DD7E → `CALL FUN_00971650` @0x0070DD84 (advance)

FACTORY_PLUS_84_CONSUMER_FUNCTION = **FUN_0070DCF0** (contract-expected value,
machine re-pinned; the prior prose pins "@0x0070DD17/1D" were 3 bytes early —
S1 measured the exact instruction starts 0x0070DD1A/0x0070DD20; the raw windows are
byte-identical to the predecessor's S7 evidence, so this is a pin precision
correction, not a contradiction).

ASSIGNMENT_TO_CONSUMER_FIELD_IDENTITY = **CONFIRMED** (static member identity:
the setter writes and the consumer read address the same statically identified
member — this+0x84 of the same factory object, under byte-pinned conditions).
Per the dispatch clarifications this means NOTHING about runtime value flow:

```text
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED
WRITE_TO_CONSUMER_VALUE_PRESERVATION    = NOT_ESTABLISHED
NO_CLOBBER_BETWEEN_WRITE_AND_READ        = NOT_ESTABLISHED (out of scope; the only
  in-scope fact: the setter's own entry guard makes the store skip when the member
  is already non-NULL — an idempotence property of the setter, NOT a lifetime
  no-clobber proof)
```

## PHASE D boundary (what is inside OBJECT_IDENTITY.md)

The assigned value's IMMEDIATE identity is established (a 0xA4-byte
non-polymorphic record-stream object, ctor FUN_00972380 — see OBJECT_IDENTITY.md).
Per the contract this run STOPS at object identity: the object's backing data
source (file/VFS/network/cache/embedded) is NOT identified; the "Cache\" /
"Parameters\" driver strings are recorded as bounded context only.
ULTIMATE_VALUE_SOURCE = UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED = NO.

## PHASE F — INIT/RESET/LIFETIME SCOPE

| Field | Value | Basis |
|---|---|---|
| FACTORY_PLUS_84_INITIAL_STATE | **ZERO_AT_EXAMINED_INIT_PATH** | the base-ctor NULL store executes for every factory construction incl. 20006 |
| Multiple write sites? | YES (2 confirmed: ctor NULL + conditional attach) | census |
| Lazy assignment? | YES (guarded, idempotent attach) | the setter's entry guard |
| Constructor assignment? | YES (the NULL init) | FUN_0070CF80 |
| Manager-init assignment? | YES — the attach is driven through the manager (mode store + list + loop) | FUN_007080C0/FUN_004B0980/FUN_00703E80 |
| FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT | **NOT_ESTABLISHED** (default) | a direct-write census cannot close lifetime; broad alias/indirect mutation analysis is OUT OF SCOPE per contract |

## ANTI-SUCCESS-THEATER (required disclosures)

- **MEASURED_QUANTITY**: the exact writer instruction(s) of the member
  [this+0x84] for the factory class family, found by a full-.text raw-form census
  (2,604 hits) + boundary verification + base-provenance, NOT by starting from the
  known consumer and assuming a setter.
- **INDEPENDENT_SOURCE_OF_TRUTH**: pinned-EXE bytes (SHA E7785430... re-hashed in
  S1/S2/S3); every rel32 target machine-computed; the S1 battery caught and forced
  correction of 31 real executor pin slips + 1 comparison bug before publication
  (0 failures after correction — the battery demonstrably fails).
- **WHY_NON_CIRCULAR**: the setter was found from the WRITE side (displacement
  census), then its `this` provenance was derived upward (loop → list → register →
  dispatcher) WITHOUT using the consumer's chain; the two sides meet only at the
  dispatcher's `[0x00BA590C]` getter and the shared member expression this+0x84.
  The factory identity of the setter's `this` does NOT rest on "same family" — it
  rests on the identity-preserving registration (same resolved pointer, stored
  unmodified, iterated unmodified).
- **FAILURE_CASE_DETECTED**: multiple natural controls inside the census bound:
  (a) 0x0074955A — a sibling-class ctor whose window writes +0x88/+0x89 as BYTES
  (class-layout mismatch vs the factory's dword +0x88 vector) → REJECTED_WRONG_OBJECT;
  (b) 0x006D4F88 — a different class ctor storing the integer 4 at its +0x84 →
  REJECTED_WRONG_OBJECT; (c) 0x0075138F — a class with a synchronization object at
  its +0x88 (factory has the slot vector there) → REJECTED_WRONG_OBJECT;
  (d) 0x007196AA — static globals copied into +0x84/+0x88/+0x8C (different init
  grammar) → REJECTED_WRONG_OBJECT; (e) 598 read-form rows incl. the consumer's own
  reads classified REJECTED_READ_NOT_WRITE; (f) all 401 stack-based SIB forms
  rejected mechanically.

## FORBIDDEN-SHORTCUT checklist (each explicitly NOT used as proof)

- No claim rests on "displacement 0x84 appears" — the two confirmed rows required
  full base-identity chains (ctor-this via the derived-ctor call; setter-this via
  the registration/list/loop chain).
- Same factory family alone is NOT the identity basis (the chain is
  identity-preserving through the same dispatcher-resolved pointer).
- NULL initialization alone is NOT presented as provider identity.
- Proximity to FUN_0070DCF0/FUN_00707E50, same manager region, same class layout,
  use of FUN_00971AD0, "stream" naming, templates.vfs historical reuse, and
  model/resource ID correspondence were NOT used as proof of anything.
- The templates.vfs-region ctor call site (0x0072FA76) is recorded as a LEAD ONLY.
