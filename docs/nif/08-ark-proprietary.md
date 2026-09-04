# 08 — MindArk proprietary blocks (NiArk*)

**These block types do NOT exist in any public NIF documentation** (not in
niflib, nif.xml, jnif, OpenMW). This knowledge was reverse-engineered from
the PE corpus itself — it is the most valuable part of this wiki.

## NiArkImporterExtraData — one per file (5,596×)

```
v4:  ExtraData base(link) + unkInt1 i32 + unkInt2 i32 + importerName SS
     + 13 raw bytes + 28 raw bytes
v10: ExtraData base(name = "ArkImporter" or empty) + int32 (value 8)
     + SizedString version ("Gamebryo_1_1", "4.0.0.0", "4.0.0.2", "4.1.0.12")
     + ALWAYS 38 raw trailing bytes (all 2,330 v10 files — Mode1 AND Mode2)
```
The 38 trailing bytes (ITER-3 census): first byte 00/01 (matches Mode1/Mode2),
then a repeating pattern `ffffff 00000000 ffffffff ffffff` + ~20 B per-file
data (float-like values in the ±20..54 range) + 00 terminator; 4,017 distinct
values across 5,596 files; zero-density ≈ 15%. Exact field semantics UNKNOWN.
The version string = the exporter/Gamebryo version that produced the file.

## NiArkTextureExtraData — one per file (5,596×); THE texture binding block

```
v10 (R6 unified grammar, H1 CONFIRMED 2330/2330):
  3 unknown zero bytes
  Name SizedString = "ArkTexture"
  num_tex i32        <- ALWAYS 3 in corpus; NOT the entry count (semantics UNKNOWN)
  field1 i32
  field2 i32         <- PACKED: (u32 >> 8) & 0x00FFFFFF = ENTRY COUNT; low 8 bits = flags (UNKNOWN)
  padding u8 = 0
  per texture entry:
    name_len i32 (1..256 validated) + name (ASCII)
    f1 i32
    f2 i32 (typically -1)
    ref i32 (texture index)
    9 trailing bytes
```
**The 9 trailing bytes = DECODED (iteration 24 canon correction):**
`anim_flag u8 + frame_index u32 + bnt2_id u32`
(the old u16 read truncated IDs ≥ 0x10000 — this was a real bug).
The `bnt2_id` is the texture ID in Textures.bnt — see 09-semantics.

ITER-3 census facts (9.3.5):
- **Entry names follow a `<material>_<SLOT>` convention** — decoded examples:
  `Box01_0_BASE` (427×), `head_up_BUMP`, `Nameless0_ENVIRONMENT` (483×),
  `comp_0_BASE`, `Cylinder01_0_BASE`; 8,430 distinct names.
- field1 has exactly two classes: `1` (3,042 files) / `-256` (0xFFFFFF00,
  1,796 files) — semantics UNKNOWN.
- field2 low-8: `0` (3,800) / `255` (1,796 — correlates with field1=-256).
- entry f1 top values: 0 (10,724), 3, 9, 1, 4, 5 — small enum/index-like.
- entry f2: `-1` (17,421) / `0` (2,216).
- entry ref: range 4..454 (slot/purpose index — NOT the bnt2_id, which lives
  in the 9-byte trailing).

v4 layout (different!): base(link) + 2×i32 + u8 + i32 + numTextures i32 +
per texture: name SS + i32 + i32 + texturingPropRef + 9 raw bytes.

## NiArkViewportInfoExtraData — 4,095× (9.3.5)

```
v10: Name SS + VARIABLE extension (0..121 B observed), boundary via
     next-block search (printable_ratio_80 chain; NiStringED00 pattern
     pre-pass; last-block rule; 200 B guard)
v4:  Name SS + link + variable extension, boundary via known-type RTTI search
```
Extension internals: partially decoded (ITER-3): the dominant 13-byte
extension (2,304 files) = **`03 + 12×00`**; length histogram is quantized to
odd sizes: 13 (×2,304), 21 (×752), 85 (×592), 49 (×255), 45 (×80), 121 (×79),
35, 39, 43. Max 121 B. Longer extensions: raw-kept + SHA256, layout UNKNOWN.

## NiVertexMorphExtraData — 354× (9.3.5) — header DECODED (ITER-3)

```
0x01 (constant)
u32  vertex-count of the morph-target mesh (CONFIRMED when the correct
     mesh is paired: 592572.nif 1294 == 1294; other samples need correct
     mesh pairing — the file can contain several meshes)
u16  flags/params (values 0, 64, 1024 observed; semantics UNKNOWN)
[variable payload 765..205,125 B — float-bearing morph/weight data,
 ends with 1.0f terminators in sampled targets]
```
Internal record layout: UNKNOWN (raw-kept).

## NiArkShaderExtraData — 2,084× — SEMANTICS DECODED (ITER-3 census 2026-09-04)

```
ExtraData base + unknownInt i32 (ALWAYS 0 — 2,084/2,084) + unknownString SizedString
```
The string is a CRLF-delimited shader effect assignment:

```
0\r\n
<line count>\r\n
effectfile <effect name>\r\n
[optional parameter lines]
```

Observed directives (9.3.5 corpus, 577 distinct configs):
- `effectfile 1024_BaseBSRSkinIndoors` (527×), `1022_BaseBSRIndoors`,
  `1021_BaseBSR`, `1011_Base`, `Vegetation`
- `CullMethod 2`
- `AlphaTreshold 0|128` (the typo "Treshold" is AUTHENTIC MindArk)
- `EnableAnimation 0.0|1.0`
- `reflectionMapCube SE_Reflection_Cubemap_Indoor.dds` /
  `SE_Reflection_Cubemap_Outdoors.dds`
- `EnvMapCube SE_Reflection_Cubemap_Outdoors.dds`

**This block is the era's per-material shader/effekt assignment** — it names
the engine effect file applied to the material. Layout CONFIRMED by 3
external sources + traces; semantics CONFIRMED by corpus census.

## NiArkBillboardNode — 293×

**Proven alias**: v4 = plain NiNode (0 extra bytes); v10 = NiNode +
BillboardMode u16 (M1D-20/22/23). Not a real distinct layout.

## NiArkAnimationExtraData — one per file (5,596×) — MindArk's anim metadata

Canonical header (all files): base + u1 i32 (+4) + u2 (+8) + u3 (+12) +
u4 (+16), extension starts at +20.

### v4 variants (P0-verified, 760-file corpus):
| Variant | Files | Extension |
|---|---|---|
| FIXED_A_57 | 346 | fixed 37 B |
| FIXED_B_61 | 192 | fixed 41 B (selector: peek[7]==0x01) |
| SHORT28 | 35 | fixed 8 B (all zeros / peek[7]==0x00) |
| BINARY | 4 | self-terminating: sentinel 0xFFFFFFFF then float trailer -1.0×n |
| TEXT_CRLF | 183 | self-terminating text grammar (below) |
| G9_RTTI | 10 | v4 known-type RTTI boundary search |

Selector: peek 8 bytes + header fields:
`u3==0xFFFFFFFF && u2<4` → FIXED_A; `peek[7]==0` → SHORT28; `peek[7]==1` →
FIXED_B; `u2==3 && u3==5` → BINARY; 7-zero prefix → FIXED_A; all-zero →
SHORT28; else TEXT_CRLF (fallback G9).

### v10 variants — 9.3.5 census (ITER-3):
| Variant | Count | Note |
|---|---|---|
| V10_BASE_0B | 2,270 | u2=FFFFFFFF, u4=0 |
| G3B | 1,685 | binary → boundary search |
| G3D | 348 | u3≠0, byte0=0x01, size=byte[1]×5 |
| FIXED_A_57 | 347 | 37 B |
| G3C | 308 | text-like → TEXT_CRLF grammar |
| FIXED_B_61 | 190 | 41 B |
| TEXT_CRLF | 172 | full text grammar |
| V10_BASE_33B | 125 | u4=0x01000000 |

u-field census (9.3.5): u1 = **5 in ALL v10 files** (0 in v4 — an
era/version marker); u2 ∈ {2, -1, 4, 3} (2,621 / 2,395 / 313 / 267 —
variant selector); u3 ∈ {0, -1, 0x3101, 0x3001} (packed); u4 ∈ {0,
0x01000000} (the Mode2 marker).

### TEXT_CRLF grammar (31/31 CONFIRMED) — the crown jewel

```
1. binary header → first CRLF (\r\n)     [CRCRLF also occurs]
2. node_count: ASCII decimal digits → CRLF
3. node_count × node records, each delimited by the ASCII marker
   "NodeDataStart" (followed by CRLF)
4. trailer (starts with ≥5 zero bytes):
     byte[5] == 0x00 → 6-byte trailer
     byte[5] == 0x02 → 35-byte trailer
     byte[5] == 0x01 → 39-byte trailer
```
Guard: the grammar may consume the next block's 4-byte preamble as part of
the trailer → if computed_end−4 is a valid v10 boundary and computed_end is
NOT, seek back 4 bytes (C14-A fix). Forward re-search if the grammar
terminates early (false trailer).

Extension semantics: per-node animation channel data (names + float arrays
in the text records). Field-by-field semantics: UNKNOWN beyond the grammar
(raw-kept + SHA256 per file).
