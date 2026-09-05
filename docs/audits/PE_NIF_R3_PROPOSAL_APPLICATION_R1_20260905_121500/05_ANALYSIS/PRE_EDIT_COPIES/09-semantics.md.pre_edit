# 09 — Semantics beyond parsing

## Coordinate system & units

- NIF data is **Z-up**; render conversion (Y-up): `(x, z, -y)` — position
  AND quaternion axes. CONFIRMED (museum/era math, viewer-verified).
- Units ≈ centimeters (buildings ~2,000 NIF units ≈ 21 m at 0.01 GLB scale).
- NIF local transforms (translation Vec3 + rotation Mat33 + scale f32 on
  NiNode/NiTriShape) are **model-local hierarchy transforms ONLY**.

## REJECTED — NIF local transform is NOT world placement

Tested extensively (placement census, 23 encodings × 29 anchors × 5 corpora
= 1,975 files): no tested encoding of static placement exists in client
files. Canonical status:
- DIRECT_STATIC_PLACEMENT_IN_TESTED_ENCODINGS = REJECTED
- SERVER_DELIVERED_PLACEMENT = STRONGLY_SUPPORTED (NOT CONFIRMED — origin
  trace pending)
- PLACEMENT_ORIGIN = UNRESOLVED / OPEN_FOR_FALSIFICATION
- The 29-anchor teleport table in scripts (3078) = the ONLY local
  coordinate table (Port Atlantis 6055, 8442 / PA 6055, 22278 era variants).
Never use NIF transforms as world coordinates.

## Texture binding chain (M3, CONFIRMED)

How a NIF mesh finds its textures in PE (NOT the standard Gamebryo path —
the era uses Ark blocks):

```
NiTriShape → properties → NiTexturingProperty (slot 0 = BASE, ...)
mesh → NiArkTextureExtraData entries
  entry name (e.g. "Stone04") + ref + bnt2_id (9 trailing bytes)
  bnt2_id → Textures.bnt (BNT2) payload = TGA 2.0 uncompressed 256×256×24
ArkTexture bytes[5:8] u32 LE = BNT2 texture ID (99.86% — 23,488 entries,
23,455 resolved; 33 dangling = 18 SuperSpray particle slots (3 ids ×6)
+ 15 unshipped individual slots; 14 unique missing IDs — M3-4 R2,
refined in PE_ASSET_CENSUS_R1)
```
Binding edges (M3-4.5 V2, machine-validated; 2003 corpus — denominators
match the R35 2003 census): 20,427 static (Jaccard
1.000000 vs builder; negative control 0.0), 148 controller edges (125
NiFlipController), 1,749 effect edges (1,646 NiTextureEffect). 200/200
witnesses field-matched. **STATIC binding = CONFIRMED.**

Per-mesh binding tiers (viewer-proven, 167/167 exact on 12 multi-mesh
buildings): mesh_block data_id → geometry-name sanitizeNodeName+BB →
traversal order → bbox+vertex-count.

## Material IR (M3-5A, CONFIRMED)

16,080 material records; slots: BASE=13,928, DARK=1,785, DETAIL=199,
GLOSS=2,707, GLOW=1,531, BUMP=636, DECAL=0.
**Enum identity ≠ modern semantics**: GLOSS ≠ roughness, BUMP ≠ normalMap
(REJECTED as overclaims). The slot VOCABULARY itself is now closed — 40
slots with a perfect f1 enum (ITER-32, next section) — while the RUNTIME
meaning of the non-BASE slots stays OPEN (M3-5B — needs runtime/D3D8
evidence).

## ArkTexture slots & shader directives (ITER-32, CONFIRMED)

The semantic layer of the material pipeline — what the ArkTexture
ENTRIES mean (a different denominator from the M3-5A material records
above). Byte grammar, field tables and the full directive census:
[08-ark-proprietary.md](08-ark-proprietary.md). Denominators (9.3.5):
24,508 texture entries in 5,596 files (v10 19,637 + v4 4,871
name-recovered), 11,083 distinct names, ZERO `<material>_<SLOT>`
convention exceptions; era-stable on 2003 (23,488/23,488 entries, all
40 slots shared; 16 of 17 directive names — `BaseTexture` absent — R35).

**SLOT = the texture's role in the mesh's material**, encoded twice — in
the entry-name suffix AND in entry f1 (a perfect 1:1 enum): BASE=0,
DARK=1, DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6, ENVIRONMENT=9,
ANIM=11. What the slots mean (evidence-graded):

- **BASE** — the primary diffuse layer (14,307 entries; 93.5% indexed
  mesh-material names, the `Box01_0` convention).
- **ENVIRONMENT** — dynamic environment/reflection maps: the slot count
  equals the NiTextureEffect block count (1,694 == 1,694) and f2=0 in
  1,694/1,694 — the ArkTexture ↔ NiTextureEffect pairing is
  STRONGLY_SUPPORTED.
- **BUMP** — avatar body-part materials (`head_up`, `torso`,
  `upperarm`...; skin-detail on skinned bodies — NOT a modern normal
  map; v10 only, 970 entries).
- **ANIM0–31** — flipbook frames: each entry's trailing frame index
  EQUALS its slot number (1,157/1,157 auxiliary-verified); materials are
  effect names (`Geo_Flame_0_NONE`, `Cloud01_Emitter_0_NONE`).
- **DECAL0 / DARK / GLOSS / GLOW / DETAIL** — auxiliary layers (50 /
  1,816 / 2,791 / 1,524 / 199 entries); runtime roles still M3-5B OPEN.

**NiArkShaderExtraData = the shader-side CRLF config language**
(`0\r\n<N>\r\n<param>...`; effectfile ALWAYS param 0; declared count ==
actual in 2,084/2,084). Its 17 directives split into two effect families
with different MEANINGS:

- **Vegetation wind animation** (`Vegetation` 977 blocks +
  `1004_Vegetation` 81): the atomic 6-param clique `CullMethod` +
  `AlphaTreshold` (authentic MindArk typo) + `EnableAnimation` +
  `ModelAmpPlanar` + `ModelAmpHeight` + `ModelFreqScale` (co-occurring
  1,058×, never a partial subset; + occasional `globalWind`) =
  per-material wind amplitude/frequency — the era's vegetation wind
  animation system.
- **10xx_Base/BSR reflection effects** (9 effect files): NO animation
  parameters at all — only the environment binding varies
  (`reflectionMapCube` / `ambientMapCube` / `EnvMapCube` →
  `SE_Reflection_Cubemap_*.dds` and kin).

Authentic exporter provenance survives inside the config strings (see
also the build-lineage section below): effectFilename values are raw
exporter-machine paths, e.g. `C:\CVS\BRANCH_T\MindArk\resource\Materials\1004_Vegetation.fx`
(a CVS branch checkout), `C:\Program Files\3dsmax7\maps\fx\Vegetation.fx`,
`R:\_PE Work Directory\...`, plus exporter casing idiosyncrasies
(`effectfile`/`effectFile`, the `default_reclection_cube` misspelling) —
the strings are raw exporter output, NOT normalized.

## Skinning & animation semantics

- LBS formula: `v' = Σ w · W_bone(t) · X_b · S · v` — CONFIRMED empirically.
- Era pattern: mesh NIF + separate ANIMATION_SKELETON NIF, paired
  cross-file **by bone NAME**; only 7 models (2003) carry in-file keyframes
  AND skinning.
- Timing: NiFlipController delta = seconds/frame (30/15 fps corpus);
  keyframe era window e.g. doors [0, 26.67] s @ 30 Hz.

### Engine behavior directives (ITER-5/16/24/25/38 — what the behaviors MEAN)

NiArkAnimationExtraData (exactly 1 per file) is the file's behavior
metadata: each record binds a procedural behavior to a named scene node —
"this node rotates / swings / emits particles, at this rate, in this
object state". Field grammar + variant census:
[08-ark-proprietary.md](08-ark-proprietary.md).

- **Controllers channel = the item/FX ATTACHMENT system (ITER-24,
  237/237 records mapped)**: the record names the holding node
  (Bip01_item — the item bone, ×107), the play mode (LOOP ×151 /
  DONOTCHANGE ×35 / SINGLE ×22), and optional named placement
  sub-records: `Target:` = attachment position + rotation (6 floats;
  exact axis mapping INFERRED), `Camera:`, `IconSize:`,
  `ViewportSettings:`.
- **The viewport suite (ITER-25)**: the four named directives ALWAYS
  occur together, in the order ViewportSettings (+13 params) → Target
  (+11) → Camera (+4) → IconSize (+1), appended to 26 records — the TEXT
  serialization of the same camera/viewport data the binary
  NiArkViewportInfoExtraData ext carries (121 B = 85 B + 36 B, the
  suite's params — ITER-8/28): the engine has BOTH a binary and a TEXT
  encoding of viewport/camera settings.
- **Mode = a STATE-BINDING label, orthogonal to the parameters
  (ITER-38)**: 41076.nif registers Bip01_rotator_1 TWICE with
  byte-identical params — once `activeIdle`, once `single`. Readings:
  `activeIdle` = the default idle loop (996/1,274 records); `active` =
  the FIRE state of one weapon family (Geo_Flame01–04 in
  542418/542466/542520 — the same files bind aftersmoke + Bip01_item to
  `activeIdle`); `single` ≈ one-shot (count=1 in 87%); `Single` (capital
  S) = a one-file orthography (386359.nif); `activeIdle/single` = a
  single contaminated compound (the corpus token is a slash — the
  "activeIdle-single" hyphen spelling was a transcription artifact).
- **The binary variants carry an EVENT REGISTRY (ITER-7/30)**: embedded
  null-terminated ASCII strings with a per-string u32 — `morph: left` /
  `morph: right` (drive vertex-morph channels BY NAME),
  `sound:hit_01/02/03`, `start_usetool: effect_01`, and
  `start -name <anim> -loop` command sets (run/walk/attack/die/idle...):
  behavior records trigger morphs, sounds and effects.
- **G3D = the per-file animated-node list (ITER-15/37)**: 5-byte records
  `[00][class 01/02/03][u16 block index][00]`; all 15,885 targets are
  NiNodes (skeleton/scene nodes) — the index counterpart of the TEXT
  named directives. The class byte's ENGINE semantics are UNVERIFIED —
  structure CONFIRMED: classes interleave (not sections), the Scene-Root
  reference is always LAST (348/348), and the class byte is
  file-configuration dependent, NOT node-intrinsic (identical rigs carry
  uniform-02 vs uniform-03 lists).

## Morph channels & precision model (ITER-4/33/34)

NiVertexMorphExtraData = the era's standalone vertex-morph animation
channel (354 blocks in 118 files on 9.3.5; morph files carry 0
NiKeyframeController — morphs are triggered by behavior events
"morph: left/right", see above). Structure:
[08-ark-proprietary.md](08-ark-proprietary.md). What the data MEANS:

- Uniform blocks = per-vertex morph records: `[u16 tag][k × f32 blend
  weights summing to 1.0][9 × f32 position deltas]` — each vertex blends
  morph states with normalized weights (ITER-4).
- The delta floats are **quantized f32s**: ≤7-bit mantissas (≥16
  trailing zero mantissa bits — the LE "00 00" low-byte signature in
  99.4% of small-profile 12-byte groups) on per-magnitude power-of-2
  grids spanning **2^-14..2^-21** (gridk spikes at 15–21; the earlier
  single-2^-18 claim is REFINED — one grid per magnitude, not one global
  grid). NOT f16 (TESTED, REJECTED), NOT 5-bit u16 weights (TESTED,
  REJECTED): the R18 walk's u16 "ids" are high-half fragments of these
  quantized floats plus record heads (ITER-34 T-F16/T-5BIT).
- Real sparse records (10.8% of entries) = `[u16 vertex_index < N][k ×
  f32 weights ≈1.0][9 × f32 delta triples]` with k per-record ∈ {2,3,4} —
  byte-exact on 86.2% of real-record spans (ITER-34); the fixed-W
  `[u16 idx][W×f32]` form holds only on the k+9==W subset (132/6,167
  spans).
- Residual: 325 heterogeneous spans (3.16%, 56 files) fit no single
  grammar (ITER-21) — dumped to disk for any future deep dive.

## Build lineage & exporter provenance (ITER-29/32/36)

What the archive index fields and header strings MEAN for provenance
(byte layouts: [08-ark-proprietary.md](08-ark-proprietary.md),
[10-containers-corpus.md](10-containers-corpus.md)):

- **BNT2 field_c / field_d = the archive's registration checksum pair
  (ITER-36)**. c = CRC32(current payload), recomputed at every pack
  (CONFIRMED 5,596/5,596 + 5,426/5,426). d = the CRC32 the payload had
  at its LAST REGISTERING event in the build lineage, carried forward
  VERBATIM across non-registering repacks: **d==c ⟺ the file has not
  changed since registration** (61.42% in 9.3.5 / 60.80% in 2003); a
  stale d preserves the CRC of a historical version that no longer
  exists on disk (0/4,288 stale-d values match ANY observable payload
  CRC — the packer write path itself was not observed, hence
  STRONGLY_SUPPORTED). d is stable across eras for 5,205/5,208
  byte-identical files and rewrites exactly on registering updates:
  46/46 size-changing re-exports; the 165 equal-size era changes are
  mostly 1-ULP float32 reprocessing with d STABLE (161/165). Lineage
  classes track d==c: v4 files 99.87% / 953-new files 79.89% / native
  Gamebryo_1_1 65.56% / pre-2003 up-converted v10 files 6.35%.
- **The importer exporter-string = the ORIGINAL toolchain version
  (ITER-29)** — an era hint that SURVIVES NIF version up-conversion (4
  distinct strings; no 10.1.0.0-era string exists): the two string
  families are `Gamebryo_1_1` (the current-era exporter: 4,004 files in
  9.3.5 / 3,826 in 2003) vs the 4.x-era strings `4.1.0.12` / `4.0.0.2` /
  `4.0.0.0` (834 v10 files in 9.3.5 carry one = pre-2003 content
  up-converted WITHOUT re-registration — the field_d 6.35% class above).
  Old-era strings correlate with meshless texture/property assets (88.7%
  zero-geometry vs 26.9%) and higher block counts; ALL 118 morph files
  are Gamebryo_1_1 (morph support = the newer exporter).

## Known exporter quirks (for anyone rebuilding assets)

- v10 NiTriShape hasShader u8 sits between skinRef and shaderName —
  missing it shifts every following boundary by 1 byte.
- NiVertexColorProperty has a PE-only u32 after lightingMode.
- NiArkTexture v10 `num_tex` is always 3 — the real entry count is packed in
  field2 bits 8..31; v4 blocks instead store the entry count directly in
  `num_tex` (0..51, exact-consumption-validated — ITER-32).
- BNT/BUNT archives: every entry's packedSize spans 8 bytes into the next
  entry's zlib stream (trailing 8 = next header) — strict decompressors
  (Chromium DecompressionStream) reject the stream; Node zlib tolerates.
- ArkTexture names ↔ texture IDs are many-to-many (id ↔ name ≠ 1:1).
