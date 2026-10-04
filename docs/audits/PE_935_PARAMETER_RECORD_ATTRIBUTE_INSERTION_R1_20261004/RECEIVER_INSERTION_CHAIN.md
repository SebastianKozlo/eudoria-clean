# RECEIVER_INSERTION_CHAIN — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 (PHASE E)

## One-line statement

RECORD_A's parsed key (id2=16083) and value-object (the 0x30-byte template object) are
INSERTED as the pair {key@node+0x10, value@node+0x14} into the client's RB-tree REGISTRY
(root pointer DAT_00BA1824, lazy singleton FUN_0043A550) by FUN_0072F8D0 → FUN_0072F7F0
→ FUN_0072F740 → FUN_005670A0. RECEIVER_IDENTITY = CONFIRMED;
CONTAINER_ROLE = DEFINITION_REGISTRY; PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED.

## Receiver pointer provenance

- The registry root: `MOV EAX,[0x00BA1824]` @0x0043A571 inside FUN_0043A550
  (lazy singleton: if NULL → `PUSH 0x18` @0x0043A57A → allocation → ctor FUN_0052A260
  → `MOV [0x00BA1824],EAX`). Byte-verified this run (QC-8).
- [C1/P3-corrected receiver provenance — SUPERSEDES the prior claim "The reader loop
  fetches the registry via FUN_0043A550 and keeps it at [ESP+0x3C]", which was WRONG:
  the loader FUN_0072FA30 does NOT itself call the singleton.] The registry pointer
  ARRIVES as the loader's incoming ECX from the wrapper FUN_00452490:
  `CALL FUN_0043A550` @0x00452490 → `MOV ECX,EAX` @0x00452495 → tail
  `JMP FUN_0072FA30` @0x00452497 (all byte-verified from the pinned EXE). The loader
  PRESERVES the incoming ECX (`MOV [ESP+0x38],ECX @0x0072FA6B`, bytes 89 4C 24 38 —
  byte-verified; the Desktop post-audit report cited @0x0072FA6C, which is the ModRM
  byte of this instruction, not its start) and recovers it before the insert
  (`MOV ECX,[ESP+0x3C]` @0x0072FBD4; insert call @0x0072FBE5). The whole-.text E8
  census of FUN_0043A550 contains NO call site inside FUN_0072FA30.
- The same singleton feeds every OTHER consumer censused this run (35 call sites of
  FUN_0043A550; every FUN_0072F580/FUN_0072F880 call is preceded by one — pairing
  verified in the census JSON).

## Container class/structure (byte-decoded this run)

- STL-style RB-tree (map<u32 id2, template_object>):
  - node size **0x44 bytes** (`MOV [EBP-0x14],0x44` @0x0072F822 in FUN_0072F7F0 before
    the allocation call; C1/P3-corrected instruction start — @0x0072F825 was
    mid-instruction; the R1 QC script's byte check already read C7 45 EC 44 at
    0x0072F822) = 0x10 node header + pair {key 4B, value 0x30B};
  - **key at node+0x10** (mapfind FUN_004D1430 compares the searched key against
    node+0x10 — established E2, window re-verified);
  - **value at node+0x14** (lookup FUN_0072F580 returns `node+0x14` —
    `ADD EAX,0x14` @0x0072F59E; miss default `MOV EAX,0x00BA5800` @0x0072F5A5 —
    C1/P3-corrected instruction start; @0x0072F5A8 was the operand byte).
- Insert function: FUN_0072F8D0 (exactly 1 call site: the reader loop @0x0072FBE5);
  new node from FUN_0072F7F0 (established E1, re-verified).

## Insertion function (the attribute insertion/update — byte-decoded this run)

`FUN_0072F7F0` → `FUN_0072F740(&node_pair, src_pair)`:
```
0x0072F775: MOV ECX,[ESP+0x1C]     ; src pair
0x0072F779: MOV EDX,[ECX]          ; src.key = id2
0x0072F77B: ADD ECX,4              ; &src.value
0x0072F77E: PUSH ECX
0x0072F77F: LEA ECX,[EAX+4]        ; this = &node_pair.value (node+0x14)
0x0072F782: MOV [EAX],EDX         ; node_pair.key (node+0x10) = id2   ← THE KEY STORE
0x0072F784: CALL FUN_005670A0     ; copy src.value → node_pair.value (node+0x14)
```
`FUN_005670A0(this, src)` — the canonical template-object copy (this run's full decode):
```
[this+0x00] = [src+0x00]   (id2)     0x005670CD/0x005670CF
[this+0x04] = [src+0x04]   (B)       0x005670D1/0x005670D4
[this+0x08] = [src+0x08]   (A)       0x005670D7/0x005670DA
[this+0x0C] = [src+0x0C]   (C)       0x005670DD/0x005670E3
[this+0x10] = f32 [src+0x10] (D_f32) FLD @0x005670E6; FSTP @0x005670EA
[this+0x14] = vector<string> copy of src+0x14 (list1)  CALL FUN_00566F80 @0x005670F0
[this+0x20] = vector<u32> copy of src+0x20 (list2)      CALL FUN_00552DA0 @0x00567104
[this+0x2C] = [src+0x2C]   (f11)     0x00567109/0x0056710C
```
The identical copy exists as FUN_0072F7A0 (this+…, RET 4) — used by the lookup-with-copy
FUN_0072F880 (see PLACEMENT_CONSUMER_EDGE.md).

## Key representation / value representation

- KEY: u32 `id2` == the record's header id == payload[0] (echo invariant; RECORD_A: 16083);
  stored at node+0x10; the mapfind compares raw u32 values.
- VALUE: the 0x30-byte canonical template object {id2@+0x00, B@+0x04, A@+0x08, C@+0x0C,
  D_f32@+0x10, list1 vector<string>@+0x14, list2 vector<u32>@+0x20, f11@+0x2C} at
  node+0x14 — populated field-by-field from RECORD_A's parsed payload by
  FUN_005670A0/FUN_0072F740 (the object copy includes the id2 again at value+0x00,
  consistent with the lookup-consumer getter anchor [value+0x08]=A=296445 for
  RECORD_B — E3 anchor re-verified in QC-7).

## CONTAINER_ROLE classification

**DEFINITION_REGISTRY.** Grounds: (a) the tracked BRIDGE R1 FINAL_SEMANTIC_ROLE
("templates.vfs is the static template registry ... consumed as a DEFINITION source");
(b) the loader loads ALL records at container-open time (no per-instance keying);
(c) the value layout is a shared template definition, not a runtime-instance record;
(d) per the contract's warning, INSTANCE_VALUE_MAP was NOT inferred from class names —
the registry is keyed by definition id2, and no world-instance identity is carried.

## Verdict

PARSER_TO_RUNTIME_VALUE_SEAM = **CONFIRMED**
(RECORD_A → reader → parser → key 16083 + value {B=0, A=410620, C=0, D_f32=0.4995,
list1=[], list2=[], f11=0} → receiver registry DAT_00BA1824 → insert {16083 → value}).
This does NOT mean PLACEMENT_CARRIER_CONFIRMED (see PLACEMENT_CONSUMER_EDGE.md).
