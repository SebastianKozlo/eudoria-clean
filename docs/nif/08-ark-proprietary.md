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
Extension internals: **DECODED (ITER-3+8 census)** — structure =
`[u8 class byte][flags][variable payload]`:

| Ext len | Blocks | Content |
|---|---|---|
| 13 | 2,304 | `0x03 + 12×00` (deterministic; class byte 0x03) |
| 21 | 752 | `0x03 + zeros + u32 flag=1 + zeros` (1 distinct value) |
| 35 | 18 | all zeros (deterministic) |
| 39 | 11 | zeros + flags + `1.0f` + small floats |
| 45 | 80 | class byte 0x02 + flags + zeros (32 variants) |
| 49 | 255 | class 0x03 + flags (pos4: 1×187/0×68; pos7: 0x40×162) + zeros |
| 85 | 592 | class 0x03 + flags + **float parameter block** (fov≈2.0, positions -0.5757/-0.382/-1.539, 19.55, 0.6969...; 556 DISTINCT = per-file camera/viewport params) |
| 121 | 79 | same family, longer (78 distinct, per-file params) |

Semantic: the 85/121 B classes carry **per-file viewport/camera parameters**
(floats CONFIRMED; exact field semantics PLAUSIBLE — likely fov/near/far/
position). Full census:
`99_Audits\PE_NIF_VIEWPORT_DECODE_R8_20260904_125635\02_results\VIEWPORT_CENSUS.json`.

## NiVertexMorphExtraData — 354× (9.3.5) — record model DECODED (ITER-4)

```
0x01 (constant)
u32  vertex count N (= the morph-target mesh vertex count; CONFIRMED when
     the correct mesh is paired: 592572.nif 1294 == 1294)
u16  tag (constant per block; values 0,1,3,14,16,24,64,384,512,1024,1536;
     0x0000 requires special handling)
payload = N per-vertex records + tail:
  record = [u16 tag][W × f32]         W ∈ {10, 11} per block
  the LAST record carries one EXTRA f32 (terminator/final weight — UNKNOWN)
```

CONFIRMED (exact tag-first walk, byte-exact to block end; cross-check:
records == N for every fully-walked block; R61 block boundary = ground truth;
independent decoder = non-circular):
- W=10 records: `[1.0, ...9 delta floats]` (e.g. 591782: all-identity
  `[1, 0×9]`; 591807: real deltas)
- W=11 records: `[w0, w1, ...9 floats]` with **w0 + w1 = 1.0 exactly**
  (blend weights of two morph states)
- values quantized on a 2⁻¹⁸ grid (3.8147e-06 = exactly 2⁻¹⁸, recurring)
- morph files carry NO NiKeyframeController (0/354) — morph data is a
  standalone animation channel

OPEN (339/354 blocks): variable/sparse record layout (large records with
embedded sub-arrays, e.g. 2796..20,156 B) — structure UNKNOWN.
Provenance: `99_Audits\PE_NIF_MORPH_DECODE_R4_20260904_122056\`
(probes 1–6, driver hashes recorded; MORPH_PROBE6_FINAL.json).

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

### Variant UNIFICATION (ITER-9) — the whole family is ONE record format

Census of the stored `ark_extension` payloads
(`99_Audits\PE_NIF_FIXED_DECODE_R9_20260904_131247\`):

| Variant | n | distinct | Content — ALL share the binary record family |
|---|---|---|---|
| V10_BASE_0B | 2,270 | 1 | empty (no behavior) |
| FIXED_A_57 | 347 | **2** | `[7×00][02][000000][ffffffff][-1.0×5][00]` — **null behavior record** (X=-1, params -1.0) |
| FIXED_B_61 | 190 | **1** | same null record + `[01][u32 29]` size prefix |
| SHORT28 | 35 | **1** | 8×00 (empty) |
| V10_BASE_33B | 125 | 92 | **the SAME 33B record as G3B** (X ∈ {5,4,0xff,...}) |
| G9_RTTI (v4) | 10 | 4 | same record embedded after a small v4 prefix |
| G3D | 348 | 348 | **index lists**: 6-byte records `[u8 00][u8 02\|03][u16 index][u16 0]` (40 records per 245 B) — the 02/03 byte matches the G3B behavior-enum space |

**Conclusion: NiArkAnimationExtraData has ONE binary record grammar
(`[u32 29][02][01/02][X][Y][5×f32]`) + TEXT records + G3D index lists.
The FIXED variants are simply "default/empty behavior" (null record with
X=-1, all params -1.0). The variant zoo = framing differences, not different
data.** Remaining open: G3D header/record semantics (what the indices
reference) and the G3C_BOUNDARY long-text field parse.

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

### TEXT node record semantics — DECODED (ITER-5 census, 2026-09-04)

Each "NodeDataStart" record is a readable, CRLF-delimited **per-node
procedural behavior/animation config** for the MindArk engine:

```
NodeDataStart
<node name>            scene node / bone (Bip01_item ×85, Geo_Flame ×36,
                       Spray ×21, Bip01_Door_001 ×15, GeoGlower,
                       GeoTexanim01, Geo_Lampshade, Asteroid, Moon1...)
<int>                  (UNKNOWN flag)
<float> <float>        (start time / offset — UNKNOWN)
activeIdle             default behavior/state (714 of 887 records)
<channel type>         derivatives (453) | Controllers (197) | cyclic (131)
                       | ParticleSystem (54) | Texture (13) | NodeUpdate (3)
<channel target>       position (367) | rotation (170) | velocity (86)
                       | All (197) | single (3)
<numeric params...>    rotation axis (0/1/2; larger values for cyclic),
                       speeds (e.g. 120.0 = asteroid rotation deg/s), ranges
LOOP | (other mode)    play mode (LOOP ×155)
```

Confirmed examples: scene rotators (`Bip01_rotator1..4`, `Asteroid` 120.0,
`Spacestation` 150.0, `Moon1/Moon2` — rotating world objects), item bones
(`Bip01_item ... Controllers All LOOP`), texture-animated geometry
(`GeoTexanim01`, `Texture` channel). 887 records extracted from 480 blocks
(172 TEXT_CRLF + 308 G3C); full corpus in
`99_Audits\PE_NIF_TEXTCRLF_DECODE_R5_20260904_123415\02_results\TEXTCRLF_RECORDS.jsonl`.

**Conclusion: NiArkAnimationExtraData (one per file) is the file's behavior
metadata carrier; the TEXT variants hold human-readable per-node directives
for procedural animation (rotators, flames, sprays, particle systems,
texture animation, loop modes).**

### G3B binary record — DECODED (ITER-6)

The dominant binary variant (1,685 blocks; u4=0x01000000 marker in 1,682)
carries the SAME behavior metadata in a compact binary record:

```
per 33-byte record (ext is 33 B or 66 B = 2 records; 82 multi-record blocks):
  u32 size = 29 (constant — CONFIRMED)
  u8  02   (constant — CONFIRMED)
  u8  01   (constant — CONFIRMED)
  u32 X    behavior/channel enum (values 1..15; top: 5×356, 4×184, 10×174,
           3×147, 7×109, 1×99, 6×90, 12×77 ...)
  u8  Y    flag (1 ×1,376 / 0 ×70 — enable/loop)
  f32 ×5   animation params — ALWAYS the symmetric pattern
           (A, A/2, 0, 0, A): (3.333,1.667,0,0,3.333) ×140, (2,1,0,0,2) ×84,
           (1.333,0.667,0,0,1.333) ×75, (1,0.5,0,0,1) ×61, (0,0,0,0,0) ×56
  pad      2–3 zero bytes
```

Parse coverage: 1,446/1,628 33-multiple blocks parse byte-exact
(`99_Audits\PE_NIF_G3B_DECODE_R6_20260904_123703\`). Semantics
STRONGLY_SUPPORTED: binary cousin of the TEXT records — behavior enum +
symmetric oscillation/rotation parameters. OPEN: variable-length G3B exts
(49–95 B, 182 blocks) and FIXED_A/B + Mode2 + G3D layouts.

### Variable G3B records + the animation EVENT REGISTRY (ITER-7)

Variable exts (57 blocks, 49–95 B) = the same binary record **plus embedded
null-terminated ASCII strings — the named animation-event system**:

```
[u32 rest_size][02][01][u32 X][u8 Y][5 × f32][strings...]
```

Embedded name census (468 blocks carry strings;
`99_Audits\PE_NIF_ANIM_REMAINDER_R7_20260904_124614\G3B_EMBEDDED_STRINGS.json`):

| Event name | Count | Meaning |
|---|---|---|
| `morph: left` / `morph: right` (+ case variants) | 160+ | morph-channel triggers → NiVertexMorphExtraData targets |
| `sound:hit_01` / `hit_02` / `hit_03` | 12+ | sound-cue triggers |
| `start_usetool: effect_01` | 11 | tool-use effect trigger |
| `start_usetool: sound_01` | 2 | tool-use sound trigger |

**This closes the loop with ITER-4: the behavior records drive vertex
morphs by NAME ("morph: left/right") and fire sound/effect events.**

Other variant findings (ITER-7, same run dir):
- **G3C_BOUNDARY (92 blocks)**: long text configs (1482–2152 B) — particle
  systems (`PCloud01-Emitter ... ParticleSystem values NOR...`)
- **G3E (4)**: `[binary header incl. u32 text_len]` + the same TEXT records
- **G9_RTTI v4 (10)**: binary record family with all -1.0 float params
- **G3D (348)**: index-list binary (dominant lens 245/240 B; entries look
  like index lists 5..55). **PARSER BUG FOUND**: the frozen G3D size formula
  `byte[1]×5` is WRONG (e.g. 9×5=45 ≠ 245) — the boundary search compensates
  today; formula correction is a bounded R61 follow-up (frozen-baseline
  rules apply: 5426+5596 regression before any change).

### TEXT_CRLF grammar (31/31 CONFIRMED) — the record framing

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
