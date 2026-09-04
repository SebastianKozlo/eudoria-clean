# 01 — File format: header, primitives, block framing, version gates

Status: CONFIRMED (byte-level, full corpus both eras; R61 parser + independent
byte-decoder agreement; external cross-check niflib/nif.xml/jnif).

## Endianness & primitives

All integers little-endian.

| Type | Size | Encoding |
|---|---|---|
| u8 / i8, u16 / i16, u32 / i32 | 1/2/4 | LE |
| f32 | 4 | IEEE 754 |
| Vec3 | 12 | 3×f32 |
| Mat33 | 36 | 9×f32 row-major (rotation) |
| Color3 / Color4 | 12 / 16 | f32×n |
| TexCoord | 8 | 2×f32 |
| SizedString | var | i32 length + that many bytes (ASCII, but names may contain Latin-1 bytes ≥ 0x80 — see boundary search) |
| Ref (link) | 4 | i32 block index; **-1 (0xFFFFFFFF) = NULL** |
| Boolean | **version-dependent** | see gates below |

## Boolean size gate (the Morrowind trap)

```
boolean_4bytes = (version < 0x04010000)
```
- v4.0.0.2 (0x04000002): booleans are **4-byte i32** (Morrowind convention)
- v4.1.0.12 (0x0401000C) and all v10: booleans are **1-byte u8**

This single gate caused the famous 52555.nif failure (1-byte read leaves 3
garbage bytes → stream desync). It is handled centrally in the stream reader
(`set_boolean_mode`), not per call site.

## File header

```
v4 (4.0.0.2, 4.1.0.12):
  HeaderText   — bytes up to first '\n' (e.g. "NetImmerse File Format...")
  Version      — u32 (0x04000002 / 0x0401000C)
  NumBlocks    — u32
  [blocks follow, each preceded by INLINE RTTI: SizedString type name]

v10 (10.1.0.0):
  HeaderText   — bytes up to first '\n' ("Gamebryo File Format, Version 10.1.0.0")
  Version      — u32 (0x0A010000)
  UserVersion  — u32 (since 10.0.1.8; PE: 0)
  NumBlocks    — u32
  NumBlockTypes — u16 (since 5.0.0.1)
  BlockTypes   — SizedString[NumBlockTypes]          <- the TYPE TABLE
  BlockTypeIndex — u16[NumBlocks]                    <- per-block type index into the table
  NumGroups    — u32 (since 5.0.0.6)
  Groups       — u32[NumGroups]
  [blocks follow; each block payload preceded by a 4-byte preamble u32 == 0]
```

## Block framing

- **v4**: inline RTTI — every block starts with `SizedString type_name`,
  then the block payload. No preamble.
- **v10**: the block's type comes from the header type table
  (`BlockTypeIndex[i]`); the payload is preceded by a **preamble u32 which
  MUST be 0** (record separator, present for 0x0A000000 ≤ v < 0x0A020000).
  A non-zero preamble means parser desynchronization → fail-closed.

Example (first block of 9.3.5 Models.bnt at offset 0):
`"Gamebryo File Format, Version 10.1.0.0\n" | 00 00 01 0A (version) | 00 00 00 00 (user ver) | 67 00 00 00 (103 blocks) | 0D 00 (13 types) | 06 00 00 00 "NiNode" ...`

## Version gates master table (CONFIRMED; source: niflib line refs + corpus byte traces)

| Gate | Condition | Effect in PE corpora |
|---|---|---|
| Boolean 4-byte | v ≤ 0x04010001 | only v4.0.0.2 |
| Inline RTTI → type table | boundary 5.0.0.1 (0x05000001) | v4 inline; v10 table |
| NiExtraData link → name | boundary 5.0.0.11 (0x0500000B) | v4 extra data = linked list (next link, NO name); v10 = name only (NO link) |
| NiObjectNET single extra → array | v ≥ 5.0.0.11 | v4: one i32 extra ref; v10: u32 count + refs[] |
| NiBillboardNode separate flags | v ≥ 10.0.1.2 (0x0A000102) | v10: extra u16 mode; v4: none |
| NiAVObject velocity/bbox | v < 10.0.1.0 | v4 HAS velocity+bbox; v10 HAS collisionObject ref instead |
| ZBuffer function | v ≥ 0x0401000C | v4.1.0.12 & v10 have u32 function; v4.0.0.2 does NOT |
| hasUv (geometry) | v ≤ 0x04000002 | only v4.0.0.2 (4-byte bool) |
| MaterialProperty flags | 0x03000000 ≤ v ≤ 0x0A000102 | v4 has u16 flags; PE v10 does NOT |
| Block preamble u32 | 0x0A000000 ≤ v < 0x0A020000 | all PE v10 |
| NiGeometry hasShader | 0x0A000100 ≤ v ≤ 0x14010003 | PE v10: u8, followed by shaderName+u32 if set |
| DynamicEffect affectedNodes | v ≥ 0x0A010000 (v10); list-ptr only ≤ 0x04000002 | v4.1.0.12: NOTHING |

## Boundary-search heuristics (for blocks with variable unknown extensions)

Some blocks (NiArkViewportInfoExtraData, NiVertexMorphExtraData, v4 Ark
variants) carry extensions of unknown size. The proven-safe method is to scan
forward for the next block start and validate candidates:

v10 next-block candidate must satisfy ALL:
1. preamble u32 == 0
2. name length i32 in [0, 256]
3. name bytes ≥ 80% printable (32–126 range; allows Latin-1 like 0xF6,
   rejects binary 0x80) — the `printable_ratio_80` rule (9280.nif fix)
4. NumExtraData u32 ≤ 10000
5. controller i32 == -1 or 0..10000
6. (near EOF) truncated validation is acceptable

v4 next-block candidate: a SizedString matching a known NIF type name
(RTTI search), length 5–50.

Known caps from corpus: viewport extensions ≤ 121 B (guard 200 B);
last-block rule: if search fails and remaining ≤ 200 B → consume rest.
