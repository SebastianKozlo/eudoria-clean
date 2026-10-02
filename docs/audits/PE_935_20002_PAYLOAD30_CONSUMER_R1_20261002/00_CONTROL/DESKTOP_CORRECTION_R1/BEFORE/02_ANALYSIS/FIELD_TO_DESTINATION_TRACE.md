# FIELD_TO_DESTINATION_TRACE — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY. All instruction VAs byte-pinned in 01_RAW\CLIENT_READ_BYTES.json (45/45 OK).

## The anchored record (ANCHOR_PRIMARY = record 0; per FORMALIZER_NOTES FN-2 the singular §18 keys carry ANCHOR_PRIMARY)

| FIELD | VALUE |
|---|---|
| RECORD_ORDINAL_OR_PHYSICAL_ID | 0 (zero-indexed; record header id = 0x05B80001) |
| RECORD_FRAME_START | 16 (0x10) |
| RECORD_PAYLOAD_START | 32 (0x20) |
| RECORD_PAYLOAD_LENGTH | 56 (0x38) |
| FIELD_FILE_OFFSET | 80 (0x50) = payload_start + 0x30 |
| FIELD_BYTE_RANGE | [80, 84) file bytes |
| FIELD_WIDTH | 4 (pinned by the client read instruction: dword load) |
| FIELD_ENDIANNESS | little-endian (x86 native dword load; RAW_MEASUREMENT after the client-read pin, upgrading the S1 HYPOTHESIS_DERIVED label per V2-009) |
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
       tag 0x0D, value 4 bytes              (descriptor type 1)
       tag 0x0E, value 4 bytes              (descriptor type 1)
       tag 0x10, value 4 bytes              (descriptor type 1)
       tag 0x11, value 4 bytes              (descriptor type 1)  <-- VALUE AT +0x30
+0x34 u32 mode-1 tail size = 0 (all 1366 records; no nested blob)
+0x38 payload end (size 56)
```
Verified by 03_SCRIPTS\s5_tlv_walk_census.py: 1366/1366 records walk clean with the
client-derived semantics; tag 0x11's value offset == 0x30 in 1366/1366 records.

## THE TRACE (payload+0x30 -> client read -> destination field)

1. **Payload buffer arrival**: FUN_00971ad0 (seek @0x971B14; ReadFile 56 bytes) puts the record payload in the 0x80-byte cursor {base, +4 capacity, +8 limit=56, +0xC offset, +0x11 flag}. FUN_0070dcf0 advances offset by 8 (FUN_0040de60(8)).
2. **TLV loop** FUN_00726900(instance, mode=1, cursor):
   - reads u16 flags @+0x08 and u16 count @+0x0A;
   - per entry: reads the u16 **tag** (@0x7269E7 `MOVZX EDI, word [EAX+ECX*1]`);
   - loads the class object from instance+0x04 (@0x7269FC `MOV ECX,[EBP+4]`);
   - **descriptor lookup**: `FUN_0070c180(classObj, tag)` @0x726A03 -> descriptor at `classObj->[0x88] + tag*0x10` (@0x70C1D3 `SHL EAX,4`; @0x70C1D6 `ADD EAX,[ECX+0x88]`);
   - type validity check @0x726A08 (`CMP [EAX+4],0`; tag 0x11 descriptor type = 1, set by the byte-pinned schema registration `PUSH 0xC0; PUSH 0x1; PUSH 0x11; CALL FUN_0070cbc0` @0x761717..0x761722);
   - **field index** = descriptor[+8] = tag + 4 (@0x70CBF6 `ADD ECX,4`; tag 0x11 -> 0x15 = 21);
   - **value-array pointer** = instance+0x40 (@0x726A11 `MOV EDX,[EBP+0x40]`; the array of 22 u32 slots is allocated by FUN_0070d990: count+4 = 18+4 = 22);
   - **destination address** = value_array + field_index*4 (@0x726A14 `LEA ECX,[EDX+ECX*4]`; slot 21 -> value_array + 0x54);
   - **value read dispatch**: FUN_0075f660 @0x726A1B -> flags bit0 test @0x75F687 (0xC0 & 1 == 0 -> scalar path) -> FUN_004129c0 (type switch; type 1 -> FUN_00412540 @0x4129DF).
3. **THE CLIENT READ**: FUN_00412540:
   - cursor flag + bounds check (offset+4 <= limit);
   - `MOV EAX, dword ptr [EAX + EDX*1]` **@ VA 0x00412553** (RVA 0x12553, FILE_OFFSET 0x12553, bytes `8B 04 10`) — a native x86 32-bit little-endian load from cursor.base + cursor.offset; at the tag-0x11 iteration cursor.offset == 0x30, cursor.base == the record payload start -> **this instruction reads the 4 bytes at file offset payload_start+0x30** (record 0: bytes `BB 2E 00 00`, value 11963);
   - **THE STORE**: `MOV dword ptr [EDX], EAX` **@ VA 0x0041255A** (bytes `89 02`) — stores the value at the destination = the instance's value-array slot 21 (value_array+0x54);
   - advance cursor by 4 (FUN_0040de60).
4. **Post-parse**: `instance->[+0x30] |= flags (0x80)` (@0x726A4B region); mode-1 tail: reads u32 at payload+0x34 = 0 for all 1,366 records -> nested-reader virtual call skipped.
5. **Registration**: FUN_0070dc20 registers the instance in the class instance map (`FUN_0092b660({id, instance})` -> classObj+0xC map); the finalize virtual (`classObj+0x80` trait object, vtable slot [+0x24]) is called with the instance.

## DESTINATION STRUCTURE FIELD (§9 fields)

| KEY | VALUE |
|---|---|
| READ_FUNCTION | FUN_00412540 (reached via FUN_00726900 -> FUN_0075f660 -> FUN_004129c0, case type 1) |
| READ_INSTRUCTION_VA | 0x00412553 |
| READ_INSTRUCTION_RVA | 0x00012553 |
| READ_INSTRUCTION_FILE_OFFSET | 0x00125553 |
| READ_INSTRUCTION_BYTES | 8B 04 10 (MOV EAX, dword ptr [EAX+EDX*1]) |
| SOURCE_CURSOR_OR_BASE | the record cursor: base = in-memory copy of the 56-byte record payload (ReadFile'd from the opened 20002.vfs at node.frame_pos+0x10); limit = 56; offset at this point = 0x30 |
| SOURCE_DISPLACEMENT | payload+0x30 (record 0: file offset 0x50 = 80) |
| WIDTH | 4 (dword) |
| ENDIANNESS | little-endian (x86 native load) |
| DEST_REGISTER | EAX (transient) |
| DEST_OBJECT_OR_STRUCTURE | the ArkParameterArmor instance (0x58 bytes, allocated by FUN_0070d990 via the class-object factory FUN_0073a490 -> FUN_00761540 -> ArkObject base FUN_00726e70 + `ArkParameterArmor::vftable` 0xA878BC store @0x761556) — specifically its **value array**: 22 u32 slots, pointer at instance+0x40 |
| DEST_FIELD_OFFSET | slot 21 (value_array + 0x54) — the tag-0x11 descriptor field index (tag+4 = 0x15) |
| STORE_INSTRUCTION_VA | 0x0041255A |
| STORE_INSTRUCTION_BYTES | 89 02 (MOV dword ptr [EDX], EAX) |

Width/endianness provenance note (V2-009): the S1 census labeled the 4-byte LE reading
HYPOTHESIS_DERIVED; with the client read instruction pinned (native dword load), the
width/endianness are now RAW_MEASUREMENT. The upgrade applies to all census rows
(they were extracted with the identical byte rule that the client instruction uses).

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

The same parse path covers it: record 1014's TLV shape is identical (tags 1, 0xC, 0xD, 0xE, 0x10, 0x11; count 6; tail 0) — the tag-0x11 value (0) flows through the same instructions into slot 21 of its instance.
