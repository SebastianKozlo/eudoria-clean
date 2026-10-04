# RECORD_A — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

## Identity

| Field | Value |
|---|---|
| File | `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs` (SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77, 560,788 B) |
| Record key (header id = payload id2) | **16083** (0x3ED3) |
| Walk index | 5430 (of 5,438) |
| File offset (header start) | **560,212** (0x88CD4) |
| Header {id u32, size u32, ver u32, crc u32} | {16083, 28, 1, crc32 = 0x82A125AB} |
| Payload byte length | **28** |
| Payload hex (28 B, machine-measured) | `d3 3e 00 00 fc 43 06 00 00 00 00 00 00 00 00 00 98 be ff 3e 00 00 00 00 00 00 00 00` |
| Payload SHA256 | 9E22B8AF3A7B63CECFA41B7D3C46775BBBE0C7A8B505B7635214EDE89898D74B |
| Record window SHA256 (header+payload, 44 B) | 1987B5C48724FC5BDA2D752928479CCFDF2879230D41068F02BC6046EEAB46B5 |

## Independently established record boundary

Bases INDEPENDENT of this run's decoder implementation:
1. **Container framing**: each record = a 16-byte header whose `size` field (28) defines
   the payload length; the next record header follows at `ceil((16+size)/36)*36` — the
   36-byte block quantum (matches the prior census "base=36").
2. **Echo invariant**: payload[0..3] (u32) == header id in 5,438/5,438 records (this
   record: payload id2 = 16083 = header id ✓).
3. **Next-record check**: the record at the next block offset 560,284 parses as
   {id=16084, size=28, ver=1} with payload id2 echoing 16084 ✓ — the boundary is
   confirmed by the successor's own framing.
4. **Slack invariant**: the 28 trailing padding bytes of the 72-byte block are all zero ✓.
5. **EOF-exactness**: the whole-file walk stops exactly at 560,788 = file size with
   5,438 records ✓ (and reproduces the prior C1 census: count 5,438, record 4508 at
   96,496 index 1340, record 11963 at 315,916 index 3243).
A Python parser written this run CANNOT validate its own boundaries — the bases above
(header size field, echo invariant, successor framing, slack, EOF) are of the
container/framing class, and the prior census is an independent cross-check.

## Decoded fields (STRUCTURAL_PARSE; semantic labels per established canon; raw↔decoded QC PASS)

Payload layout (28 B) — this run's own byte-decode of the client parser FUN_00730C90:

| Raw offset (file abs) | Raw bytes | Type/width | Decoder instruction (pinned) | Destination field | Decoded value |
|---|---|---|---|---|---|
| +0 (560,228) | d3 3e 00 00 | u32 LE | MOV [EDI],EAX @0x00730CB6 (fast path) | template+0x00 | id2 = 16083 |
| +4 (560,232) | fc 43 06 00 | u32 LE | MOV [EDI+0x08],EAX @0x00730CE6 | template+0x08 (A) | A = 410620 (0x0643FC) |
| +8 (560,236) | 00 00 00 00 | u32 LE | MOV [EDI+0x04],EAX @0x00730D16 | template+0x04 (B) | B = 0 |
| +12 (560,240) | 00 00 00 00 | u32 LE | MOV [EDI+0x0C],EAX @0x00730D36 | template+0x0C (C) | C = 0 |
| +16 (560,244) | 98 be ff 3e | f32 LE | FLD [EDX+EAX]; FSTP [EDI+0x10] @0x00730D6F | template+0x10 (D_f32) | D_f32 = 0.49950098991394043 (bits 0x3EFFBE98) |
| +20 (560,248) | 00 00 | u16 LE | list1 parser FUN_00730B70 (called @0x00730D8D) | template+0x14 (vector<string>) | list1_count = 0 |
| +22 (560,250) | 00 00 | u16 LE | list2 parser FUN_00730970 (called @0x00730D97) | template+0x20 (vector<u32>) | list2_count = 0 |
| +24 (560,252) | 00 00 00 00 | u32 LE | MOV [EDI+0x2C],EDX @0x00730DB6 | template+0x2C (f11) | f11 = 0 |

- Parse consumes exactly 28 bytes = the header `size` field (consumed == size ✓).
- FIELD_SEMANTIC labels A/B/C/D_f32/list1/list2/f11 follow the established BRIDGE R1 E1
  semantic role ("templates.vfs = the static template registry {id2 → A (model nif id),
  B (collision bvi id), C, D_f32, name-list1, u32-list2}") — STRUCTURAL_PARSE is this
  run's own; no new semantics assigned.
- A=410620: recorded as the decoded value ONLY. The model/resource identity join
  (410620 → any .nif) is OUT OF SCOPE and was NOT executed.
- Registry-validity predicate (FUN_0072FCE0, this run's decode): template != NULL &&
  (A != 0 || B != 0 || C != 0) → for RECORD_A: TRUE (A = 410620 ≠ 0) — the object
  returned by the lookup passes the consumer-side validity gate on the FUN_0072F880 path.

## Position-like values

D_f32 = 0.49950098991394043 appears in the record. POSITION_RECOVERY_GOAL = OUT_OF_SCOPE;
no coordinate semantics were investigated or claimed.
