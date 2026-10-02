# FIELD_TO_DESTINATION_TRACE — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY. All instruction VAs byte-pinned. Correction state: DESKTOP_CORRECTION_R1
(this file is the CORRECTED state; the branch-selection correction is recorded in
06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md; the BEFORE copy of the pre-correction
state is 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md).

- Historical pins of the FALLBACK reader (FUN_00412540) remain byte-correct evidence in
  01_RAW\CLIENT_READ_BYTES.json (immutable) — re-classified by this correction as
  BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH (see §9a).
- The SELECTED-path pins live in 01_RAW\DESKTOP_CORRECTION_R1\
  (BRANCH_SELECTION_TRACE.json 96/96; FALLBACK_PATH_RECORD.json 25/25;
  CURSOR_PROOF_CORRECTION_R1.json; DESTINATION_PROOF_CORRECTION_R1.json 23/23).

## The anchored record (ANCHOR_PRIMARY = record 0; per FORMALIZER_NOTES FN-2 the singular §18 keys carry ANCHOR_PRIMARY)

| FIELD | VALUE |
|---|---|
| RECORD_ORDINAL_OR_PHYSICAL_ID | 0 (zero-indexed; record header id = 0x05B80001) |
| RECORD_FRAME_START | 16 (0x10) |
| RECORD_PAYLOAD_START | 32 (0x20) |
| RECORD_PAYLOAD_LENGTH | 56 (0x38) |
| FIELD_FILE_OFFSET | 80 (0x50) = payload_start + 0x30 |
| FIELD_BYTE_RANGE | [80, 84) file bytes |
| FIELD_WIDTH | 4 (pinned by the selected client read instruction: dword load) |
| FIELD_ENDIANNESS | little-endian (x86 native dword load; RAW_MEASUREMENT from the pinned selected-read instruction) |
| RAW_BYTES | BB 2E 00 00 |
| DECODED_NUMERIC_VALUE (LE u32) | 11963 |

Bounds assertions (machine-checked in 01_RAW\FIELD_BYTE_ANCHOR.json):
`FIELD_FILE_OFFSET >= RECORD_PAYLOAD_START` (80 >= 32 TRUE) and
`FIELD_FILE_OFFSET + 4 <= RECORD_PAYLOAD_START + RECORD_PAYLOAD_LENGTH` (84 <= 88 TRUE).
All 1,366 records satisfy the bounds (1366/1366, denominator = record count).

## Payload structure of 20002.vfs records (byte facts; S1 census + client-semantics walk)

```
+0x00 u32 class id   = 20002 (all 1366 records)
+0x04 u32 record id  = (u16 A << 16) | u16 B  (all 1366 records verified; A groups: 37 distinct)
+0x08 u16 flags      = 0x0080 (all 1366 records)
+0x0A u16 entry count= 6 (all 1366 records)
+0x0C TLV entries {u16 tag, value} x 6 (identical tag shape in all 1366 records):
       tag 0x01, value 8 bytes {u32, u32}   (descriptor type 4)
       tag 0x0C, value 4 bytes (float)      (descriptor type 2)
       tag 0xD, value 4 bytes               (descriptor type 1)
       tag 0x0E, value 4 bytes              (descriptor type 1)
       tag 0x10, value 4 bytes              (descriptor type 1)
       tag 0x11, value 4 bytes               (descriptor type 1)  <-- VALUE AT +0x30
+0x34 u32 mode-1 tail size = 0 (all 1366 records; no nested blob)
+0x38 payload end (size 56)
```
Verified by 03_SCRIPTS\s5_tlv_walk_census.py: 1366/1366 records walk clean with the
client-derived semantics; tag 0x11's value offset == 0x30 in 1366/1366 records.
Independently re-derived for the SELECTED reader by
03_SCRIPTS\desktop_correction_r1\s4_cursor_walk.py (01_RAW\DESKTOP_CORRECTION_R1\
CURSOR_PROOF_CORRECTION_R1.json): 1366/1366 records, tag-0x11 value offset == 0x30,
full consumption (final offset == 56 == limit) in 1366/1366.

## THE BRANCH-SELECTION PROOF (why the virtual branch is the SELECTED path for tag ID 17)

Byte-pinned chain (full pins: 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json, 96/96):

1. **Registration** (FUN_00761570 schema ctor, inside the
   ArkObjectClassImpl<class_ArkParameterArmor,20002> class object):
   `CALL FUN_00977a50 @0x76170F` -> EAX = the reader object; `PUSH EAX @0x761714` (arg5);
   `PUSH 0 @0x761715` (arg4); `PUSH 0xC0 @0x761717` (flags, arg3); `PUSH 1 @0x76171C`
   (type, arg2); `PUSH 0x11 @0x76171E` (TAG, arg1); `MOV ECX,ESI @0x761720` (this);
   `CALL FUN_0070cbc0 @0x761722`.
2. **Factory return behavior** (FUN_00977a50): lazy-init flag byte at 0x00BA9380
   (`TEST byte [0xBA9380],1 @0x977A55`); on first call: set the flag, store the vtable
   0x00A9C670 into the static .data object 0x00BA937C
   (`MOV dword [0xBA937C],0xA9C670 @0x977A68`), register the exit-destructor 0x00A744B0
   (which resets that vtable at exit) via the atexit-style helper 0x95D4DB
   (`PUSH 0xA744B0 @0x977A63; CALL @0x977A72`). **BOTH paths return EAX = 0x00BA937C**
   (`MOV EAX,0xBA937C @0x977A7A`) — a non-NULL static .data address; no NULL-return path exists.
3. **Descriptor+0 dataflow**: FUN_0070cbc0 loads entry-arg5 (the object) @0x70CBE3 and
   pushes it through FUN_0075f5c0, which stores it at **descriptor+0**
   (`MOV [EAX],ECX @0x75F5CA`); FUN_0070c980 appends the descriptor into the class-object
   vector at [classObj+0x88] via FUN_0070c7b0 — copying ALL FOUR dwords including the
   object pointer (`MOV ESI,[EDX] / MOV [EAX],ESI @0x70C7C1/0x70C7C3`), preserving
   descriptor+0 in the table at begin + tag*0x10.
4. **Lookup** (FUN_0070c180): descriptor = classObj->[0x88] + tag*0x10
   (`SHL EAX,4 @0x70C1D3; ADD EAX,[ECX+0x88] @0x70C1D6`).
5. **Dispatch conditional** (FUN_0075f660): `MOV ECX,[EAX] @0x75F662` loads
   [descriptor+0]; `TEST ECX,ECX @0x75F664`; `JZ @0x75F66E -> 0x75F687` (the fallback).
   For tag ID 17, descriptor+0 = 0x00BA937C != NULL (steps 1-3), so **the JZ is NOT taken
   — the VIRTUAL BRANCH IS SELECTED** (control-flow reachability from the proven
   descriptor state, not instruction presence).
6. **Selected virtual slot**: `MOV EAX,[ECX] @0x75F674` -> [0x00BA937C] = the vtable
   0x00A9C670 (stored by the factory's lazy-init); `MOV EAX,[EAX+0x14] @0x75F676` -> the
   dword at 0x00A9C684 = **0x009777F0** (static .rdata read); `CALL EAX @0x75F67B`.
7. **RTTI identity of the reader object**: [vtable-4] @0xA9C66C = COL 0x00AB8360;
   COL+0xC = TypeDescriptor 0x00B9F10C; name `.?AUArkRTTraitsInt@@` — the reader object's
   class is **ArkRTTraitsInt** (the Int runtime-traits reader).

## THE TRACE (payload+0x30 -> client read -> destination field) — SELECTED PATH

1. **Payload buffer arrival**: FUN_00971ad0 (seek @0x971B14; read into the cursor) puts
   the record payload in the 0x80-byte-capacity cursor {+0 base, +4 capacity 0x80,
   +8 limit = 56 (FUN_0040e260 max-rule), +0xC offset, +0x11 flag}. FUN_0070dcf0
   consumes the first 8 bytes (class id + record id):
   `PUSH 8 @0x70DDA2; LEA ECX,&cursor @0x70DDA4; CALL FUN_0040de60 @0x70DDA8`
   (bounds offset+8<=limit @0x70DD95..0x70DDA0).
2. **TLV loop** FUN_00726900(instance, mode=1, cursor):
   - reads u16 flags @+0x08 (`MOVZX EDI,word [ECX+EAX] @0x72692F`; advance 2) and
     u16 count @+0x0A (`MOVZX EDI,word [EAX+ECX] @0x72699E`; advance 2);
   - per entry: reads the u16 **tag** (@0x7269E7 `MOVZX EDI, word [EAX+ECX*1]`);
   - loads the class object from instance+0x04 (@0x7269FC `MOV ECX,[EBP+4]`);
   - **descriptor lookup**: `FUN_0070c180(classObj, tag)` @0x726A03 -> descriptor at
     `classObj->[0x88] + tag*0x10`;
   - type validity check @0x726A08 (`CMP [EAX+4],0`; tag 0x11 descriptor type = 1, set by
     the byte-pinned schema registration);
   - **field index** = descriptor[+8] = tag + 4 (@0x70CBF6 `ADD ECX,4`; tag 0x11 -> 0x15 = 21);
   - **value-array pointer** = instance+0x40 (@0x726A11 `MOV EDX,[EBP+0x40]`; the array of
     22 u32 slots is allocated by FUN_0070d990: descriptor_count(18)+4 slots — the
     count+4 arithmetic byte-pinned @0x70D9B8/0x70D9BB; the instance+0x40 slot @0x70D9BF);
   - **destination address** = value_array + field_index*4 (@0x726A14 `LEA ECX,[EDX+ECX*4]`;
     slot 21 -> value_array + 0x54);
   - **value read dispatch**: FUN_0075f660 @0x726A1B -> **[descriptor+0] != NULL -> the
     VIRTUAL branch** -> the slot dword at vtable+0x14 (@0x75F674/0x75F676) ->
     **FUN_009777F0** (the ArkRTTraitsInt reader).
3. **THE CLIENT READ (SELECTED)**: FUN_009777F0(this = the ArkRTTraitsInt object, cursor, dest):
   - cursor flag check (`CMP byte [ECX+0x11],0 @0x9777F4`; flag-clear -> the ERROR path);
   - bounds check (`LEA EDX,[EAX+4] @0x9777FD; CMP EDX,[ECX+8] @0x977800; JA @0x977803`
     -> the ERROR path: dest = 0 and the cursor flag is CLEARED — a SEPARATE path, NOT
     the successful parse path);
   - `MOV EAX, dword ptr [EDX + EAX*1]` **@ VA 0x00977807** (RVA 0x00577807,
     FILE_OFFSET 0x00577807, bytes `8B 04 10`) — a native x86 32-bit little-endian load
     from cursor.base + cursor.offset; at the tag-0x11 iteration cursor.offset == 0x30,
     cursor.base == the record payload start -> **this instruction reads the 4 bytes at
     file offset payload_start+0x30** (record 0: bytes `BB 2E 00 00`, value 11963);
   - **THE STORE**: `MOV dword ptr [EDX], EAX` **@ VA 0x00977810** (bytes `89 02`) —
     stores the value at the destination = the instance's value-array slot 21
     (value_array+0x54);
   - advance cursor by 4 (`PUSH 4 @0x97780E; CALL FUN_0040de60 @0x977812`).
4. **Post-parse**: `instance->[+0x30] |= flags (0x80)` (@0x726A4B region); mode-1 tail:
   reads u32 at payload+0x34 = 0 for all 1,366 records -> nested-reader virtual call skipped.
5. **Registration**: FUN_0070dc20 registers the instance in the class instance map
   (`FUN_0092b660({id, instance})` -> classObj+0xC map); the finalize virtual
   (`classObj+0x80` trait object, vtable slot [+0x24]) is called with the instance.

Cursor provenance re-derived for the SELECTED reader in
01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json: the full increment table
(entry offset 8 -> flags u16 -> count u16 -> tag u16 + width per descriptor type:
tag 1 width 8 via the type-4 selected reader FUN_00409ed0->FUN_004099c0; tags 0xC/0xD/0xE/0x10/0x11
width 4 via the type-2/type-1 selected readers FUN_00977840/FUN_009777F0) — at the
tag-0x11 iteration the cursor offset == 0x30 over the record payload for record 0, record
1014 (ANCHOR_ZERO) and 1366/1366 records (own framing walk: exact EOF
16 + 1366*128 == 174,864; full consumption offset 0 -> 56 in 1366/1366; the
error/bounds-failure paths distinguished from the successful parse path by the
cursor-flag clearing + negative simulations).

## §9a — THE FALLBACK PATH (BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH)

The pre-correction trace asserted the SELECTED reader as FUN_00412540 reached via
"flags bit0 test @0x75F687 -> scalar path". **That reasoning was wrong about PATH
SELECTION, not about BYTES**: the flags-bit0 test lives INSIDE the fallback, reachable
only after the `JZ @0x75F66E` is TAKEN — i.e. conditional on **descriptor+0 == NULL**,
which is NOT the tag-ID-17 state (descriptor+0 = 0x00BA937C, non-NULL, proven above).

Fallback chain (byte-pinned; full record: 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json, 25/25):
`JZ @0x75F66E -> 0x75F687` (TEST byte [EAX+0xC],1 — flags bit0; 0xC0 & 1 == 0) ->
`JZ @0x75F694 -> 0x75F6AA` -> `CALL FUN_004129c0` (type switch; jump table @0x412A68,
entry 0 -> case-1 body 0x004129D8) -> `CALL FUN_00412540 @0x4129DF` -> READ @0x00412553
(bytes `8B 04 10`), STORE @0x0041255A (bytes `89 02`), advance 4, RET 4.

- Corrected fallback FILE OFFSETS (independently recomputed via this run's own PE32
  section-table parse): READ @ **0x12553**, STORE @ **0x1255A** (VA-RVA=0x400000; .text
  raw_pointer 0x1000 == virtual_address 0x1000, so FO == RVA).
- The prior REPORT transcription `READ_INSTRUCTION_FILE_OFFSET = 0x00125553` was a
  **digit-shift error** (0x00125553 is a 7-hex-digit value = 1194067, not the correct
  75173 = 0x12553); it is SUPERSEDED. The run's own pin JSON (01_RAW\CLIENT_READ_BYTES.json,
  immutable) always recorded the correct file_offset 0x12553.
- The fallback reader's own error path (@0x412569..0x41257D: dest = 0 + cursor flag
  cleared, RET 4) mirrors the selected reader's error path — both are failure paths,
  NOT the successful parse path.

## DESTINATION STRUCTURE FIELD (§9 fields — SELECTED reader values)

| KEY | VALUE |
|---|---|
| READ_FUNCTION | FUN_009777F0 (the SELECTED type-1 scalar value reader — the ArkRTTraitsInt virtual at vtable+0x14; reached via FUN_00726900 -> FUN_0075f660 @0x726A1B -> the VIRTUAL branch selected because descriptor+0 != NULL) |
| READ_INSTRUCTION_VA | 0x00977807 |
| READ_INSTRUCTION_RVA | 0x00577807 |
| READ_INSTRUCTION_FILE_OFFSET | 0x00577807 |
| READ_INSTRUCTION_BYTES | 8B 04 10 (MOV EAX, dword ptr [EDX+EAX*1]) |
| SOURCE_CURSOR_OR_BASE | the record cursor: base = in-memory copy of the 56-byte record payload (read from the opened 20002.vfs); limit = 56; offset at this point = 0x30 |
| SOURCE_DISPLACEMENT | payload+0x30 (record 0: file offset 0x50 = 80) |
| WIDTH | 4 (dword) |
| ENDIANNESS | little-endian (x86 native load) |
| DEST_REGISTER | EAX (transient) |
| DEST_OBJECT_OR_STRUCTURE | the ArkParameterArmor instance (0x58 bytes, allocated by FUN_0070d990 via the class-object factory; ArkParameterArmor::vftable 0xA878BC store @0x761556) — specifically its **value array**: 22 u32 slots, pointer at instance+0x40 |
| DEST_FIELD_OFFSET | slot 21 (value_array + 0x54) — the tag-ID-17 descriptor field index (tag+4 = 0x15) |
| STORE_INSTRUCTION_VA | 0x00977810 |
| STORE_INSTRUCTION_BYTES | 89 02 (MOV dword ptr [EDX], EAX) |

(Fallback field values, superseded as the §9 chain but byte-correct:
READ_FUNCTION = FUN_00412540 via FUN_004129c0 case 1; READ @ VA 0x00412553 /
FILE_OFFSET 0x12553 / `8B 04 10`; STORE @ VA 0x0041255A / `89 02` —
non-selected for tag ID 17 because its branch requires descriptor+0 == NULL.)

Width/endianness provenance note (V2-009, unchanged in substance): the S1 census labeled
the 4-byte LE reading HYPOTHESIS_DERIVED; with the SELECTED client read instruction
pinned (native dword load @0x00977807), the width/endianness are RAW_MEASUREMENT. The
upgrade applies to all census rows (they were extracted with the identical byte rule
that the client instruction uses).

## Anchor-zero (secondary keys; FORMALIZER_NOTES FN-2)

ANCHOR_ZERO = record 1014 (lowest-ordinal record with decoded +0x30 value == 0; record 1015 is the only other zero):
| KEY | VALUE |
|---|---|
| ANCHOR_ZERO_RECORD_ORDINAL | 1014 (header id 0x22A50001) |
| ANCHOR_ZERO_FRAME_START | 129,808 (0x1FB70) |
| ANCHOR_ZERO_PAYLOAD_START | 129,824 (0x1FB80) |
| ANCHOR_ZERO_PAYLOAD_LENGTH | 56 |
| ANCHOR_ZERO_FIELD_FILE_OFFSET | 129,824 + 0x30 = 129,872 (0x1FBB0) |
| ANCHOR_ZERO_RAW_BYTES | 00 00 00 00 |
| ANCHOR_ZERO_DECODED_VALUE | 0 |

The same parse path covers it: record 1014's TLV shape is identical (tags 1, 0xC, 0xD,
0xE, 0x10, 0x11; count 6; tail 0) — the tag-0x11 value (0) flows through the same
SELECTED instructions (read @0x00977807 at cursor offset 0x30; store @0x00977810) into
slot 21 of its instance. Walk state re-derived in
01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (record_1014_walk).
