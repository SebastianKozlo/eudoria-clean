# RECORD_B — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 (negative/control record)

## Identity

| Field | Value |
|---|---|
| File | same as RECORD_A (`Data\Parameters\templates.vfs`, SHA256 BE57818C...) |
| Record key (header id = payload id2) | **4508** (0x119C) |
| Walk index | 1340 (of 5,438) |
| File offset | **96,496** (0x17930) |
| Header | {id=4508, size=28, ver=1, crc32=0xAFF5797C} |
| Payload hex (28 B, machine-measured) | `9c 11 00 00 fd 85 04 00 fe 85 04 00 00 00 00 00 cb e1 f9 42 00 00 00 00 00 00 00 00` |
| Payload SHA256 | 890A50E5DDE3942A59E171659025C2F518057466161945471CDDF0FFB339004B |
| Record window SHA256 (44 B) | 4345305B0A8598EC3FBB41831E7C7DD255401092B9B22D3C6E459BDAD57D155E |

Decoded (same grammar/parse as RECORD_A — STRUCTURAL_PARSE, raw↔decoded QC PASS):
id2=4508, A=296445 (0x000485FD), B=296446, C=0, D_f32=124.94100189208984 (bits 0x42F9E1CB),
list1_count=0, list2_count=0, f11=0; consumed == 28 == header size.

## Why this is the control (contract-preferred class: different key / different receiver path)

1. **Different key**: 4508 vs RECORD_A's 16083; same file, same grammar, same insertion
   path (the reader loop inserts ALL records into the same registry).
2. **Different established receiver path**: the tracked BRIDGE R1 package byte-pinned
   record 4508's consumer as the MODEL-REQUEST EMITTER (E3: FUN_006C3F50 — registry
   lookup at 0x006C3F62, A-read via FUN_007CE1E0 @0x006C3F74, request pair {0x66, A}) —
   the model-resource path, NOT the placement-construction lookup path of RECORD_A.
   This run re-verified the emitter's lookup call site (0x006C3F62 → FUN_0072F580) and
   the A-getter [ECX+8] reading the same registry value layout.
3. **No static key**: an all-encodings imm32 scan of the whole .text for 0x119C (4508)
   found exactly 3 occurrences, ALL of which are displacement constants, NOT key values:
   - 0x0053270C and 0x00532769: inside `LEA ECX,[ESP+0x119C]` (a 4,508-byte local
     buffer offset);
   - 0x0083427E: inside `MOV [ESI+0x119C],EBX` (a struct field displacement).
   The PUSH-imm32 scan found ZERO `PUSH 0x119C` sites. No placement-construction
   function looks up key 4508 statically — the discriminating contrast with
   RECORD_A's byte-pinned `PUSH 0x3ED3` @0x005B6597.

## Control verdict

RECORD_B (4508) reaches the same insertion (registry {4508 → its template object}) but,
within the censused machinery, is read on the model-request path (runtime-keyed) and NOT
by any placement-construction lookup with a static key — the control distinguishes
"inserted into the registry" (all records) from "looked up by the placement-construction
static-key set" (RECORD_A's key 0x3ED3; plus FUN_00567170's key set, see
PLACEMENT_CONSUMER_EDGE.md).

No third record was analyzed. The file-side id-set existence checks for the code-side
key values {16082, 14912, 14919, 15321, 15322, 15323} are container-level census facts
(no bytes decoded, no fields parsed) and are not record analyses.
