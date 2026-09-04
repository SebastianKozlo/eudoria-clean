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
The 38 trailing bytes — **DECODED (ITER-10): the MODEL'S LOCAL BOUNDING BOX**
(CONFIRMED 3,020/3,020 mesh-bearing files — the bounds contain the raw mesh
geometry in 100% of cases; exactly equal in 1,786; where larger, they cover
skinned/transformed extents):

```
[u8 mode (00/01 — Mode1/Mode2 marker)]
[12 B header: ffffff-pattern + flag u32 at offset 3 — only 10 distinct
  headers in 4,838 files: {00000000 x3807, 00000001 x312, 01000000 x72,
  01000001 x34} + pattern variants (ffffff / 00ff); flag bits UNKNOWN]
[f32 min.x][f32 min.y][f32 min.z]
[f32 max.x][f32 max.y][f32 max.z]
[u8 pad = 0]
```
Examples: 505775 bounds ±1906 vs mesh ±1835 (skinning margin); 508854
bounds == mesh (-50..50, 0..142.3); 505813 z 0..11528.7 (a 115 m tower);
505007 y up to 19483 (large structure). These are the engine-side model
bounds (culling/DPVS-relevant). First byte 00/01 matches Mode1/Mode2.
Validation:
`99_Audits\PE_NIF_IMPORTER_DECODE_R10_20260904_132004\02_results\IMPORTER_BOUNDS_VALIDATION.json`.

**Header patterns — DECODED (ITER-29,
`PE_NIF_IMPORTER_HEADER_R29_20260904_150900`)**: the header (before the
38B bbox tail) has exactly **14 distinct byte patterns (4 v10 + 10 v4),
10 after masking the file-specific v4 link u32** — reproducing ITER-11's
count with the delta documented. Layout is **version-routed (CONFIRMED)**:
v10 `[u32 11]"ArkImporter"[u32 8][u32 str_len]<exporter_string>` in
4,838/4,838 10.1.0.0 files; v4
`[i32 link][i32 0][i32 8][u32 str_len]<string>[3 flag bytes]` in 758/758
4.x files. The varying bytes are:
1. **The exporter/toolchain version string — ERA PROVENANCE
   (STRONGLY_SUPPORTED)**: `Gamebryo_1_1` ×4,004 | `4.1.0.12` ×1,113 |
   `4.0.0.2` ×352 | `4.0.0.0` ×127 (sum 5,596). The string survives NIF
   version up-conversion (834/4,838 v10 files carry 4.x-era strings —
   re-export history; e.g. 139 4.1.0.12-NIF files carry a 4.0.0.2
   string). Era matrix (nif_version × exporter_string) in
   `02_results\PATTERNS.json`.
2. **The v4 next-extra-data link**: 38/38 in-range targets =
   NiStringExtraData; −1 terminator ×720.
3. **A 3-byte flag region** with only 3 observed states (558/128/72 —
   `000000`/`0000ff`/`00ffff`) — semantics UNVERIFIED (kept out of claims).

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
- **Entry names follow a `<material>_<SLOT>` convention — FULLY CONFIRMED
  (ITER-32, `PE_NIF_MATERIAL_CENSUS_R32_20260904_160538`): 24,508/24,508
  entries conform, ZERO exceptions. The complete SLOT vocabulary = 40 slots**:
  BASE ×14,307 (58.4%, f1=0) | GLOSS ×2,791 (f1=3) | DARK ×1,816 (f1=1) |
  ENVIRONMENT ×1,694 (f1=9, f2=0 always — count == NiTextureEffect count,
  cross-block linkage) | GLOW ×1,524 (f1=4) | BUMP ×970 (f1=5) |
  DETAIL ×199 (f1=2) | DECAL0 ×50 (f1=6) | ANIM0–31 ×1,157 (f1=11 in 985) —
  **f1 is a PERFECT slot-type enum**. The ANIM entries' trailing
  `frame_index` == slot number (1,157/1,157 verified —
  02_results\ANIM_FRAME_CHECK.json). 8,430 distinct names (ITER-3).
- field1 has exactly two classes: `1` (3,042 files) / `-256` (0xFFFFFF00,
  1,796 files) — semantics UNKNOWN.
- field2 low-8: `0` (3,800) / `255` (1,796 — correlates with field1=-256).
  The packed entry-count formula `(u32>>8)&0x00FFFFFF` re-validated
  corpus-wide by independent decode + exact consumption (4,838/4,838).
- entry f1 = slot-type enum (above); f2: `-1` (17,421) / `0` (2,216).
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
| 43 | 11 | **DECODED (ITER-28, `PE_NIF_VIEWPORT_43B_R28_20260904_145342`)**: marker `00 00 01 00` (class byte at offset 2 = 0x01) + either all-zero defaults (sub-class A) or camera floats (B: 1.0, -0.2083, -0.2710, -16.32, -48.65, 0.747) — the same viewport/camera family. (ITER-8 census said ×4 — the narrower inline byte-class count; R61-derived ext census = 11; both kept.) |

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

OPEN (339/354 blocks): variable/sparse record layout — status after
ITER-14/17/18/19 (external post-audit corrected):
- ITER-13/14: the `[u16 idx][f32][f32]` entry hypothesis **REJECTED at
  exact-consumption level (48/51 remainders NOFIT; 3 fit a
  `[u32 count][f32]...` length check only — not a full validation)**.
- ITER-17's 446/10,274 (4.34%) negative is **REJECTED — invalid predicate**
  (unit bug: `Wm` in bytes treated as a float count; external post-audit
  P0 finding, confirmed independently in R18-run1 and corrected).
- The morph big-span population is **MULTI-FORMAT** (ITER-19 union run):
  - **Family A (r18, 6,167 spans exact-fit — CONSUMPTION MODEL ONLY)**:
    entry-stream `[uniform W floats][[u16 id][4×f32] entries + pad floats + 2B zero tail]`;
    51,250 entries. **ITER-33 (`PE_NIF_MORPH_IDS_R33_20260904_162507`) shows this is
    NOT the true record grammar for the majority**: the u16 ids have NO single
    corpus-wide semantics — T1 id<N REJECTED corpus-wide (nonzero in-range 23.53%);
    T2 float-half REJECTED as clean f32-array; T3 not contiguous (steps 128/32/64/16);
    T4 even-32 clusters NOT N-related (id/N 3.11–256; 5-bit-quantized weight band);
    T6 no cross-block partition (disjoint only 5/64 files). **The REAL sparse morph
    records = 10.8% of entries** (id<N, 49.8% weight-pairs f0+f1=1.0, 99.0% clean
    floats, 4-aligned starts → **vertex-index STRONGLY_SUPPORTED**, consistent with
    ITER-4's W=11 model); **the dominant 89.2% (incl. all id=0 ×35,087 — 87.96% carry
    non-zero float content, NOT padding) are greedy-walk artifacts: fragments of a
    quantized float payload whose precise encoding remains UNVERIFIED**.
  - **Family B (r19, H-KEY42 — 1,915 spans STRICT exact-fit)**:
    `[tag][W×f32 first record]` + k × units
    `[u32 n][f32 w][(W-2)×f32]` (unit_len = 6+(W-2)×4; W=11 ×1,025 /
    W=10 ×890; dominant unit headers (0,0.0) ×19,702, (1,0.0) ×3,293;
    the hex-visible `01 00 00 00 80 3f` = (1,1.0) variant). Length
    arithmetic exact (e.g. 214=46+4×42).
  - **Residual (ITER-21 — chain CLOSED at this depth)**: 325 spans
    (3.16%, 56 files, top 551564.nif ×84) are a **heterogeneous sliver** —
    weight-pair w0+w1=1.0 only in 12.3%, entry-density 0.42, f32-sanity
    0.81 (min 0.36); some units carry n≠0/1 headers (`08 00 00 00 80 3f`
    = KEY42-style n=8). No clean third family; most plausibly misaligned
    data of families A/B (unreliable Wm estimate for heterogeneous
    blocks). Full hex on disk
    (`PE_NIF_MORPH_UNKNOWN325_R21_20260904_144453\02_results\HEX_UNKNOWN.txt`)
    for any future deep dive. Per-entry semantics (ids/weights/headers)
    remain OPEN.
- Provenance: `99_Audits\PE_NIF_MORPH_DECODE_R4_20260904_122056\` +
  `PE_NIF_MORPH_SPARSE_CLOSURE_R14_20260904_133726\` +
  `PE_NIF_MORPH_KEYFRAME_R18_20260904_141009\` +
  `PE_NIF_MORPH_NOFIT_STRUCT_R19_20260904_143755\`
  (HEX_SAMPLES.txt 459 spans; KEY42_VALIDATION.json; UNION_CLASSIFICATION.json).

## NiArkShaderExtraData — 2,084× — SEMANTICS FULLY DECODED (ITER-3 → completed ITER-32)

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

**COMPLETE directive vocabulary = 17 names (ITER-32,
`PE_NIF_MATERIAL_CENSUS_R32_20260904_160538`; the prior "577 distinct
configs" was a 120-char truncation artifact — true count 623, prior
method reproduced exactly):**

| Directive | n | Values |
|---|---|---|
| `effectfile` | 2,049 | 11 effect files in 2 families: **Vegetation-animation** (`Vegetation`) vs **10xx_Base/BSR-reflection** (`1024_BaseBSRSkinIndoors` ×527, `1022_BaseBSRIndoors`, `1021_BaseBSR`, `1011_Base`, ...) |
| `effectFile` | 35 | case variant (same values) |
| `CullMethod` | 1,065 | 2 ×713 / 1 ×352 |
| `AlphaTreshold` | 1,058 | **110 distinct values** (0 ×293, 128 ×154, 110 ×63, 80 ×26, ...) — per-material alpha threshold (typo "Treshold" is AUTHENTIC MindArk) |
| `EnableAnimation` / `ModelAmpPlanar` / `ModelAmpHeight` / `ModelFreqScale` | 1,058 each | **the atomic Vegetation wind-animation clique** (with AlphaTreshold) |
| `reflectionMapCube` | 181 | `SE_Reflection_Cubemap_Indoor/Outdoors.dds` + 6 more |
| `softwareBitmap` | 120 | ALWAYS `"undefined"` |
| `effectFilename` | 72 | **8 authentic MindArk exporter source paths**: `C:\CVS\BRANCH_T\MindArk\resource\Materials\1004_Vegetation.fx` ×32, `C:\Source\Mindark\cpp\Ark\Shared\Model\Vegetation.fx` ×28, `C:\3dsmax7\maps\fx\Vegetation.fx`, `R:\_PE Work Directory\...` |
| `EnvMapCube` | 63 | `SE_Reflection_Cubemap_Outdoors.dds` + 5 more |
| `ambientMapCube` | 58 | `SE_Ambient_Cubemap...` ×4 |
| `globalWind` | 8 | wind params |
| `MAX_CullMethod` / `MAX_UseAlpha` | 5 each | MAX-export variants |
| `BaseTexture` | 2 | — |

**This block is the era's per-material shader/effect assignment** — it names
the engine effect file applied to the material, its cull/alpha/wind-animation
parameters, and (via `effectFilename`) the exporter's original source path.
Layout CONFIRMED by 3 external sources + traces; semantics CONFIRMED by
corpus census (full per-effectfile parameter profiles + co-occurrence in
the run's `02_results\SHADER_DIRECTIVES.json` / `SHADER_CONFIGS.json`).

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
| SHORT28 | 35 | fixed 8 B = **8×00, verified 35/35 (ITER-31)** ("28" = block payload length, not ext length) |
| BINARY | 4 | **CONFIRMED (ITER-31)**: `[2B lead][N×5B groups][9B tail][FFFFFFFF][00][-1.0×5][00]`; N=u4>>8, 5N+37=len (4/4); the 30 B closing section = the FIXED_A ext minus its 7-zero prefix |
| TEXT_CRLF | 183 | self-terminating text grammar (below) |
| G9_RTTI | 10 | **CONFIRMED (ITER-31)**: `[2B lead][degtext?][N×5B groups, N=u4>>8][pad][[01]+33B REC33]` — the 33 B G3B record grammar embedded (incl. the ultra-rare flag=02); R7/R9's published hexes were LINK-SHIFTED views (v4 exts sliced from the 2-byte link field) — corrected in `PE_NIF_RARE_VARIANTS_R31_20260904_154509` |

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
| G9_RTTI (v4) | 10 | 4 | same record embedded after a small v4 prefix (link-shift corrected in ITER-31) |
| G3E (v10) | 4 | — | **CONFIRMED (ITER-31)**: `[m×5B groups][00 02 01][u32 text_len][text][00 00]`; text_len == actual 4/4; the text parses with the NodeDataStart grammar 4/4 |
| G3A_PREAMBLE | 6 | — | **CONFIRMED (ITER-31)**: ext = 0 B; valid v10 preamble at ext_start, next block = NiNode 6/6 |
| G3D | 348 | 348 | **CONFIRMED**: node-reference list — 5-byte records `[00][class 01\|02\|03][u16 NiNode block_index][00]`; 100% of 15,885 indices point at NiNode blocks in-file (post-audit + R15-COR) |

**Conclusion — CONFIRMED (byte-exact closure by ITER-30/31): the whole
NiArkAnimationExtraData family (5,596 blocks, one per file; the earlier
"5,521" was an arithmetic text error) is ONE record grammar
`[u32 size][02][flag][u32 X][u8 Y][5×f32][u8 class][u8 N][N×(string+u32)]`
+ TEXT records + G3D index lists + null/empty variants. The FIXED variants
are "default/empty behavior" (null record with X=-1, params -1.0). The
variant zoo = framing differences, not different data.** Every family now
has a byte-exact grammar: G3B 1,682/1,682, G3D 348/348, FIXED_A/B null
records, SHORT28/G3A empty, G3E 4/4, BINARY 4/4, G9_RTTI 10/10 (ITER-31);
TEXT records censused 1,274/1,274 with the branched suffix schema.
Evidence packages: ITER-15/16 + R15-COR/R16-COR + `PE_NIF_G3B_VARIABLE_R30_20260904_152304`
+ `PE_NIF_RARE_VARIANTS_R31_20260904_154509`. Remaining open in the family:
G3D class-byte role semantics (01/02/03) and the per-channel TEXT param
semantic labels.

### v10 variants — 9.3.5 census (ITER-3):
| Variant | Count | Note |
|---|---|---|
| V10_BASE_0B | 2,270 | u2=FFFFFFFF, u4=0 |
| G3B | 1,685 | binary → boundary search |
| G3D | 348 | u3≠0, byte0=0x01, size=u3_byte1×5 |
| FIXED_A_57 | 347 | 37 B |
| G3C | 308 | text-like → TEXT_CRLF grammar |
| FIXED_B_61 | 190 | 41 B |
| TEXT_CRLF | 172 | full text grammar |
| V10_BASE_33B | 125 | u4=0x01000000 |

u-field census (9.3.5): u1 = **5 in ALL v10 files** (0 in v4 — an
era/version marker); u2 ∈ {2, -1, 4, 3} (2,621 / 2,395 / 313 / 267 —
variant selector); u3 ∈ {0, -1, 0x3101, 0x3001} (packed); u4 ∈ {0,
0x01000000} (the Mode2 marker).

### TEXT node record semantics — DECODED (ITER-5/16 census, 2026-09-04)

Each "NodeDataStart" record is a readable, CRLF-delimited **per-node
procedural behavior/animation config** for the MindArk engine. Full field
grammar (unified across TEXT_CRLF / G3C / G3C_BOUNDARY; confirmed by
direct readability on machinery models — shaft machines, hydraulic pumps,
pistons, rotating fins, particle clouds):

```
NodeDataStart
<node name>         scene node / bone (Bip01_item, Geo_Flame, Spray,
                    Bip_Coord_1, Geo_Pist_001, PCloud01-Emitter, Asteroid...)
<count: 0|1|2>      channel count
<start: float>      start time / initial state
<offset: float>     
<mode>              activeIdle (looping idle) | single (play-once) |
                    Single | active | activeIdle/single
<channel>           derivatives | ParticleSystem | Controllers | cyclic |
                    Texture | NodeUpdate
<target>            position | velocity | rotation | values | All
[<subtype>]         translation | NORMAL | ...
<axis: 0|1|2>       rotation/translation axis
<params>            CHANNEL-DEPENDENT (see branched schema below)
```

**Param tail is BRANCHED, not fixed-6** (correction run
`PE_NIF_G3CB_SCHEMA_R16_COR_20260904_142550`, per external post-audit —
records have 7..24 fields total):

| channel | n | fields | params after prefix | typical params |
|---|---|---|---|---|
| derivatives | 605 | 13–16 | 7–10 | amplitude, phase, period, ... |
| ParticleSystem | 257 | 20–24 | 14–18 | 15/15, 3/3, 30/30, 0/0, 13.33/13.33, 0/0 = rate, size, lifetime, spread, ... |
| Controllers | 237 | 7–22 | 1–16 | **FULLY MAPPED (ITER-24,
`PE_NIF_CONTROLLERS_GRAMMAR_R24_20260904_144839`)**: positions 00–07 =
`[node][count][start 0.0][offset][mode][Controllers][All][play-mode
LOOP/DONOTCHANGE/SINGLE]` (237/237), then OPTIONAL NAMED SUB-RECORDS:
`Target:` + 6 floats (attachment position+rotation — the ITEM ATTACHMENT
system: Bip01_item ×107, the item bone), `Camera:` + 2 (camera params —
loops with the ITER-8 viewport findings), `IconSize:` + 1,
`ViewportSettings:` + params, texture-anim triple (GeoTexanim01). |
| cyclic | 157 | 14–16 | 8–10 | oscillation params |

Param SEMANTICS per channel remain partially mapped (ITER-23,
`PE_NIF_TEXT_PARAM_SEM_R23_20260904_144748` — per-position OBSERVED
distributions in TEXT_PARAM_SEMANTICS.json). Two structural facts
(OBSERVED): **Controllers records carry a named `Target:` param
(236/236)** — the Controllers suffix is not purely numeric; and the
axis slot is channel-dependent in meaning (position → 0/1/2 axis;
velocity → mostly 2; cyclic → 1/2/3; Texture → UV speeds 0.02/0.05;
ParticleSystem → mixed). Numeric positions (amplitude/phase/period)
remain INFERRED — value distributions do not prove semantic roles
without runtime consumer paths.

**The named-directive vocabulary is exactly FOUR (ITER-25,
`PE_NIF_TEXT_NAMED_DIRECTIVES_R25_20260904_144944`)**: `ViewportSettings:`
(+13) | `Target:` (+11) | `Camera:` (+4) | `IconSize:` (+1) — each ×26,
ALWAYS as a suite in that order (29 params), in derivatives ×23 /
Controllers ×2 / ParticleSystem ×1. This is the **viewport/camera suite —
the TEXT-twin of the binary NiArkViewportInfoExtraData ext** (ITER-8:
85B/121B per-file camera params; 121 = 85 + 36, the suite's extra
params): the engine has BOTH a binary and a text serialization of the
same viewport/camera data.

Confirmed behavior examples: rotating asteroids (`Asteroid` 120.0 deg/s,
`Spacestation` 150.0), industrial machinery (shaft machine fins rotation
1400.0, pistons `Geo_Pist_001/002/004` translation amplitude 100.0,
hydraulic pump, translator −100.0), particle emitters (`PCloud01-Emitter`,
`PArray01..05-Emitter` — steam/smoke clouds), flames, sprays, doors,
texture-animated geometry (`GeoTexanim01`), item bones
(`Bip01_item ... Controllers All LOOP`). 887 records censused in ITER-5 +
the G3C_BOUNDARY long configs (92 blocks, 10–14 records each) in ITER-16;
full corpus in `99_Audits\PE_NIF_TEXTCRLF_DECODE_R5_20260904_123415\02_results\TEXTCRLF_RECORDS.jsonl`.

**Conclusion: NiArkAnimationExtraData (one per file) is the file's behavior
metadata carrier; the TEXT variants hold human-readable per-node directives
for procedural animation (rotators, flames, sprays, particle systems,
texture animation, loop modes).**

### G3B binary record — GRAMMAR CONFIRMED 100% (ITER-6 → refined ITER-30)

The dominant binary variant (1,685 blocks; u4=0x01000000 Mode2 marker in
1,682; 3 text-degenerate 7 B exts are G3C-signature, see below). **Every
parseable G3B ext holds EXACTLY ONE record** (ITER-30, `PE_NIF_G3B_VARIABLE_R30_20260904_152304`;
byte-exact on 1,682/1,682 binary-family blocks — 54/54 variable + all
33 B/66 B):

```
record = [u32 size][u8 02 marker][u8 flag {01,00,02}][u32 X behavior/channel
          enum][u8 Y flag/loop][5 x f32 params][u8 class {00,01}]
          [u8 count N][N x (ASCII event-name string \0 + u32 value)]
size   = len(record) - 4 = 29 + Σ(len_i+1) + 4N     (H1-refined: 54/54 exact)
strings: printable + CRLF allowed inside; each null-terminated + 4 value bytes.
count=0 -> record is exactly 33 B (the two "pad" tail bytes = [class][count])
```

Corrections of prior readings (ITER-30, evidence-decomposed):
- **flag byte is an ENUM, not a const**: {0x01 ×1,559 | 0x00 ×120 | 0x02 ×3}
  — ITER-6's "u8 01 const" was its own filter's artifact; the 182 non-fits
  of the old 33 B rule decompose exactly: 97 flag=00 + 82 66 B + 3 flag=02.
- **"66 B = 2 records" REJECTED**: all 82 66 B exts are ONE record (size=62)
  with 2 embedded strings (overwhelmingly "morph: left"/"morph: right").
- **class byte (offset 31)** ∈ {0x00 ×1,663 | 0x01 ×19}; class=01 always
  with count=0 (fail-closed rule).
- The old wiki "182 variable-length (49–95 B)" was a MISLABEL — the true
  variable population is **57** (54 binary 48–392 B + 3 text-degenerate).
- The float quintets remain symmetric (A, A/2, 0, 0, A); ITER-6's value
  census stands.

Semantics STRONGLY_SUPPORTED: binary cousin of the TEXT records —
behavior enum + symmetric oscillation/rotation parameters + the named
event triggers.

### Embedded string registry — the animation EVENT system (ITER-7 → corrected ITER-30)

Corpus-wide: **263 strings in 136 string-bearing records** (incl. the 66 B
exts). ITER-7's "468 blocks with strings" is corrected: **136 real grammar
string records + 332 float-byte scan artifacts** (records with count=0 whose
floats coincidentally looked like ASCII) — fully reconciled, intersection
136/136, 0 grammar-strings missed.

| Event name | Count | Meaning |
|---|---|---|
| `morph: left` / `morph: right` (+ variants incl. authentic typo `morph: rifgt`) | dominant | morph-channel triggers → NiVertexMorphExtraData targets |
| `sound:hit_01/02/03` | 8/8/4 | sound-cue triggers |
| `start_usetool: effect_01` | 15 | tool-use effect trigger |
| `start_usetool: effect_01\r\nstart_usetool: sound_01` (multi-line) | 2 | combined tool-use trigger |
| 500078.nif 392 B record: `end`, `morph: 1`, + 11× `start -name <anim> -loop` (DUNGMASTER_Run/Walk/Trott, Idle_02, attack_01, die, fighting, gethit, idle_01, stand, staydead) | 13 strings | named animation-command set |

Per-string u32 value: float-interpretable 263/263; 113/263 = 0.0; non-zero
examples 0.8, 0.35, 0.0667, 20.83 (semantics UNVERIFIED).

**This closes the loop with ITER-4: the behavior records drive vertex
morphs by NAME ("morph: left/right") and fire sound/effect/animation
events.**

Other variant findings (ITER-7, same run dir):
- **G3C_BOUNDARY (92 blocks)**: long text configs (1482–2152 B) — particle
  systems (`PCloud01-Emitter ... ParticleSystem values NOR...`)
- **G3E (4)**: `[binary header incl. u32 text_len]` + the same TEXT records
- **G9_RTTI v4 (10)**: binary record family with all -1.0 float params
- **G3D (348)**: **DECODED — CONFIRMED (post-audit 2026-09-04 + correction
  run `PE_NIF_G3D_CLASS_R15_COR_20260904_142037`)**: ext = k × 5-byte
  records `[u8 00][u8 class 01|02|03][u16 block_index][u8 00]`
  (k = 47–49 typical; ext 245 B = 49 records EXACTLY). Class census:
  **02 ×15,150 | 03 ×718 | 01 ×17 (7 files: 146709, 137260, 459889, ...)**.
  **All 15,885 indices (100%) are in-bounds and point at NiNode blocks in
  the same file** — G3D is the binary node-reference list (the set of scene
  nodes covered by the behavior), the index-based counterpart of the TEXT
  records' named directives. The frame (348/348), in-bounds (15,885/15,885)
  and NiNode-target (15,885/15,885) claims were independently reproduced in
  the correction run and match the external post-audit exactly. **OPEN: the
  class-byte semantics (01/02/03; 01 is rare — 17 records in 7 files).**
  **Size formula — RETRACTION of the old "WRONG formula" claim
  (ITER-27, `PE_NIF_G3D_FORMULA_RETRACTION_R27_20260904_145244`)**: the
  frozen parser's formula `u3_byte1 × 5` (its internal comment calls it
  "byte[1]×5" — byte 1 **of u3**, which is header byte 9) was **ALWAYS
  CORRECT: u3_byte1×5 == ext_len for 348/348 blocks** (e.g. 591990.nif:
  hdr `05 00 00 00 02 00 00 00 01 31 00 00 …` → u3=0x00003101 →
  u3_byte1=0x31=49 → 49×5=245 ✓). The ITER-7 example "9×5=45≠245" was a
  MISREADING (actual b1=0; no such block exists) — claim REJECTED and
  RETRACTED; the ITER-26 report repeated it without checking the census
  (documented anti-pattern: overclaim-from-prior-text). NO frozen-baseline
  amendment needed; the designed regression is CANCELLED. The parser
  validates the formula end against the next-block preamble and only
  falls back to boundary search when that validation fails.
  **Class semantics (ITER-22, `PE_NIF_G3D_CLASS_SEM_R22_20260904_144632`)**:
  ALL three classes target SKELETON nodes (class 2: bone ×14,429 + other
  ×721; class 3: bone ×666 + other ×52; class 1: bone ×15 + other ×2 —
  names overlap: Bip01/Scene Root/Pelvis in classes 2 AND 3). The class
  is NOT a node-kind flag; it is a per-record ROLE flag in the animated-
  node list (exact 01/02/03 meaning OPEN; per-file record tables in
  the run dir enable interleaving/depth analysis).

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
