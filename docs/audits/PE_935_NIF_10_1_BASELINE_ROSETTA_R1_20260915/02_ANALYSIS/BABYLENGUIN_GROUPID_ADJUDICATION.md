# BABYLENGUIN_GROUPID_ADJUDICATION — C1/C1A (2026-09-16)

RUN: PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (correction of
PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915).

METHOD: independent byte reproduction with a FRESH minimal walker
(00_CONTROL/scripts/s15_babylenguin_boundary_walker.py) whose field
sequences are HAND-TRANSCRIBED from the pinned Gamebryo 1.2 engine
source (SRC-06) — no s04/s06 schema machinery, no external audit
offsets, no external scripts, no display-name dedup. Negative controls
executed (truncated input / corrupted string length / wrong version —
all fail as designed). Evidence: 01_RAW/BABYLENGUIN_BOUNDARY_
REDERIVATION.csv (351 rows) + 01_RAW/FIELD_IDENTITY_V2_NEGATIVE_
CONTROL.csv (s16 executed old-vs-v2 comparison).

## Inputs (independently hashed)
- BABYLENGUIN.NIF (SRC-08): 1,737,966 B; SHA256
  A86C49384E62DF41339101B62E48BE6DCAE10E06B5F7CAC39DC627CF89635EA9
  (recomputed; the external comparator's "A86C4938..." prefix was NOT
  inherited — this is the full own measurement).
- Version 10.1.0.0 (0x0A010000), UserVersion 0, 121 blocks, 35 types,
  NumGroups 0, block 0 GroupID offset 1009.

## REQUIRED STATUSES

```text
BABYLENGUIN_BLOCK7_REAL_OFFSET
    = 1517 (block 6 ends at 1517; block 7 NiPixelData GroupID u32 is
      read at 1517-1520)
BABYLENGUIN_BLOCK7_REAL_GROUPID
    = 0
VALUE_479309_REAL_OWNER
    = bytes 1498-1501 = block 6 NiSourceTexture File Name interior
      bytes[13..14] ('M','P' - the tail of 'LEN-SKIN_02.BMP') followed
      by bytes[0..1] of block 6's Pixel Data link u32 (value 7 -> LE
      bytes 07 00 00 00; link target = block 7 NiPixelData, type-table
      consistent)
OLD_XPU_CLAIM_STATUS
    = REJECTED (RETRACTED)
```

## DERIVATION (frozen before any comparator comparison)

Engine-truth block walk (s15): block 5 NiTexturingProperty
start=1408 (GroupID 0) end=1464; block 6 NiSourceTexture start=1464
(GroupID 0) end=1517; block 7 NiPixelData GroupID @1517 = 0.

Block 6 field trace (owner: engine NiSourceTexture::LoadBinary
v>=10.0.1.4 path — filename and pixel-data link are read
UNCONDITIONALLY):

| offset | len | field | value |
|---|---|---|---|
| 1464 | 4 | GroupID | 0 |
| 1468 | 4 | Name.len | 0 |
| 1472 | 4 | NumExtraData | 0 |
| 1476 | 4 | Controller | -1 (0xFFFFFFFF) |
| 1480 | 1 | Use External | 0 (INTERNAL pixel data) |
| 1481 | 4 | File Name.len | 15 |
| 1485 | 15 | File Name | 'LEN-SKIN_02.BMP' |
| 1500 | 4 | Pixel Data link | 7 -> block 7 = NiPixelData (consistent) |
| 1504 | 4 | Pixel Layout | 6 |
| 1508 | 4 | Use Mipmaps | 1 |
| 1512 | 4 | Alpha Format | 3 |
| 1516 | 1 | Is Static | 1 |
| 1517 | - | BLOCK 6 END / block 7 GroupID @1517 = 0 |

The old claim's value 479309 (0x0007504D) occurs at exactly ONE offset
in the whole 1,737,966-byte file: 1498. Bytes there (4D 50 07 00) are
the filename tail 'MP' plus the low 2 bytes of the pixel-data link 7.
They are NOT a GroupID of any block.

## MECHANISM (reproduced by s16, executed negative control)

The frozen s06 SchemaDecoder._fields_for deduplicates effective schema
fields by BARE FIELD NAME. For NiSourceTexture the HIST schema declares
two conditional alternatives with the same display name —
`File Name` [cond "Use External == 1"] and `File Name`
[cond "Use External == 0", ver1=10.1.0.0]. Both are version-applicable
at 10.1.0.0; the dedup keeps the FIRST (cond == 1) and LOSES the
second (cond == 0). For BABYLENGUIN block 6 (Use External == 0) the
frozen decoder therefore never consumed the filename: it read the
filename LENGTH (15) as the "Pixel Data" ref, then 'LEN-', 'SKIN',
'_02.' as Pixel Layout / Use Mipmaps / Alpha Format enums and 'B'
(0x42) as Is Static, ending block 6 at 1498 and reading the next u32
(4D 50 07 00 = 479309) as "block 7 GroupID" — the s08
sequential_decode failure `block 7 GroupID=479309`.

s16 FIELD_IDENTITY_V2 executed comparison (both models on the same
bytes):
- OLD model: block 6 end=1498; "block 7 GroupID"=479309@1498
  [REPRODUCED]; effective list contains ONE File Name occurrence.
- V2 model (s14): block 6 end=1517; block 7 GroupID=0@1517 [PASS];
  File Name read = 'LEN-SKIN_02.BMP'; Use External=0; effective list
  contains BOTH File Name occurrences.

## C1A — conditional parse trap

Block 5 NiTexturingProperty (start=1408, end=1464): TextureCount=7;
slot[5] = BUMP_INDEX had HasMap=0, so the BumpMap extras (LumaScale,
LumaOffset, BumpMat00/01/10/11 = 24 bytes) were NOT read — the VALUE
condition (`Has Bump Map Texture`) was honored exactly as the engine
(NiTexturingProperty::LoadBinary). Reading them unconditionally would
have shifted the block 5 boundary to 1488 and produced a FALSE
boundary BEFORE NiSourceTexture. No false boundary occurred: block 5
ends at 1464 exactly (engine truth).

## COMPARATOR CHECK (performed AFTER the freeze above)

The external prompt-audit's independently-derived comparator sequence:
block 5 end ~1464; block 6 start = 1464; block 6 end = 1517; block 7
GroupID @1517; 479309 candidate @1498; Is Static = 1. My derivation
matches ALL six points with ZERO discrepancy. The first external
audit's hexdump typo (IsStatic) is corrected to 1 in the second
external audit — matches my own measurement.

## RE-ADJUDICATION (C7)

- A. Gamebryo GroupID framing exists: CONFIRMED (engine NiObject.cpp
  L134-143; physically read at every BABYLENGUIN block boundary).
- B. Entropia GroupID framing exists: CONFIRMED (unchanged; all
  PE-corpus blocks read per-block GroupID==0 across 2,343 closures +
  45 NiSourceTexture blocks under V2).
- C. EE2 demonstrates standard 10.1 framing: CONFIRMED (lodtest.nif
  CLOSURE_OK under BOTH old and V2 decoders — the file contains no
  NiSourceTexture, so the field-identity defect could not contribute;
  retest evidence 01_RAW/CROSS_PUBLISHER_RETEST_FIELDIDENTITY.csv).
- D. BABYLENGUIN has non-zero GroupID=479309: REJECTED — the value is
  filename+link bytes misread after the boundary shift caused by the
  field-identity defect. Real block 7 GroupID = 0 @1517 (consistent
  with F-03's "SDK samples: GroupID present (=0)").

FUNCTION/FORMAT EXISTENCE (A/B/C framing) vs ONE POSITIVE SAMPLE VALUE
(D): the D retraction does NOT downgrade A/B/C — the GroupID field's
existence rests on engine source + physical slot reads, not on the
retracted nonzero sample.
