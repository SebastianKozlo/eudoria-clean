# F03 — TERRAIN vs NIF TEXTURE DENOMINATORS (SCOPE CORRECTION)

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. THE TWO MEASUREMENTS TRACED TO THEIR GENERATORS

### 1a. 24,474/24,508 = 99.8613%

- GENERATOR: PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021 (eabf6cf),
  01_RAW/SUMMARY.json (committed; read in-repo).
- MEASURED OBJECT: the K1 ARKTEXTURE ID TABLE — the texture-binding entries of
  NIF models in Models.bnt (BNT2 index 5,596 entries; parse closure 5596/5596;
  arktexture_entries = 24,508 = v10 19,637 + v4 4,871).
- METHOD (the run's own field): "M3-4.5 V2 (mesh -> texturing-property slot ->
  ArkTexture; controller via NiTexturingProperty.controller; effect via
  NiNode.effects[])".
- NUMERATOR: resolved = 24,474 (BNT2 '<id>.dat' resolution in Textures.bnt,
  tex_id_set_size = 8,381); dangling = 34 (classified).
- POPULATION / DENOMINATOR: 24,508 K1 ArkTexture entries across 5,596 NIF model
  files (era PCG_9_3_5; Models.bnt c950a8c2...; Textures.bnt 61acd13b...).
- ERA: PCG_9_3_5.
- RESOURCE CLASS: NIF mesh -> NiTexturingProperty slot -> NiArkTextureExtraData /
  texture ID / name anchor.
- SEMANTIC DOMAIN: MODEL (mesh) TEXTURE RESOURCE BINDING.
- WHAT IT PROVES: 99.8613% of the NIF models' texture-binding entries resolve to
  a Textures.bnt entry in the same era (a strong resolution-layer fact).
- WHAT IT DOES NOT PROVE: ANYTHING about terrain texels, terrain material
  layers, the terrain material palette, detail texture IDs, blend inputs, the
  432502/459344 selector grids, TDF masks, or the HISTORICAL TERRAIN TEXTURE
  LAYOUT. It is not terrain-layout coverage of any kind.

### 1b. 80.40% (19,705/24,508)

- GENERATOR: PE_935_TEXANCHOR_CENSUS_R1_20260906_175500 (c380a26), 06_REPORT/
  00_FINAL_REPORT.md (committed; read in-repo; standing sentence: "correlation/
  association outputs are OBSERVED-level evidence; semantic roles remain
  runtime-gated; no semantic claims").
- MEASURED OBJECT: own-file NAME-ANCHORING of the same 24,508 K1 ArkTexture
  entries (anchored = mesh-part resolves to a mesh/material name present in the
  SAME file AND the slot field equals the name's slot suffix; the colon-bridge
  dual-spelling rule; cross-file negative control 67/10,000 = 0.67%).
- POPULATION / DENOMINATOR: 24,508 K1 entries (same corpus as 1a).
- ERA: PCG_9_3_5. RESOURCE CLASS / SEMANTIC DOMAIN: NIF MODEL TEXTURE name
  association — OBSERVED class, CI [79.90, 80.90], slot-consistency 100%.
- WHAT IT PROVES: a 120x file-specific association strength between K1 texture
  entries and their own file's mesh names (an OBSERVED statistical structure).
- WHAT IT DOES NOT PROVE: terrain texture layout (same exclusions as 1a).

## 2. ADJUDICATION

Desktop GC-F03 REPRODUCED: the two figures were TRANSFERRED into terrain-texture
positions they do not measure — M1_DOWNSTREAM_OUTPUT_CONTRACT.md §6 "TERRAIN
TEXTURE INPUTS" L45-46 (the binding contract for later milestones);
TERRAIN_WORLD_SURFACE_AUDIT.md §TEXTURE RESOLUTION; the coverage matrix row-5
implementation column. The measurements THEMSELVES are valid (frozen methods,
pre-registered, negative controls; not discarded — they were MIS-SCOPED).
Disposition: RETAINED as a clearly-labeled NIF/MODEL TEXTURE CROSS-REFERENCE;
REMOVED from any terrain-layout-coverage position in the successor contract
corrections (02_ANALYSIS/DOWNSTREAM_CONTRACT_CORRECTIONS.md). TERRAIN TEXTURE
LAYOUT = NOT RECOVERED (unchanged).

## 3. §7.1 THE TERRAIN TEXTURE CONTRACT TABLE (successor-correct content)

| CLAIM | ORIGINAL SOURCE | DENOMINATOR | IMPLEMENTATION | HISTORICAL INPUT STATUS |
|---|---|---|---|---|
| Terrain container data (terrain.bnt TDF payloads; 58,451 entries; 51,920 regular tiles) | iter019/iter008b era-validation + walks | 58,451 entries / 51,920 tiles | PESourceMount BNT2_TERRAIN VERSIONED decoder | BYTE-EXACT from original bytes (CONFIRMED) |
| TDF material info (tail records; 175 material ids; masks RAW+RLE; 838/838 consumer census = LOD vertex-color bake + zone shadow paint, NOT the texel source) | iter008b/iter020/iter021/iter030 | 51,920 tiles exact consumption; 838/838 terrain functions | TdfMaterialTailDecoder (format layer, RAW/UNVERIFIED labels) | BYTE-EXACT (grammar both eras); consumer role CONFIRMED 9.3.5 |
| Terrain material palette (17 palettes 64x256x32bpp; materials_confirmed uses palette 421318) | iter027 (96/96 climate system textures exist in PCG Textures.bnt) | 96/96 manager ids | resolveTexture + TgaDecoder, provenance per payload | LOCAL + era-correct; byte-exact payloads |
| Detail texture IDs (C[0]=D[0]=458791, E[0]=458792; [P2] selector byte 0) | V4 registry P2 + iter027 | the engine tables' byte-0 entries | materials_confirmed DETAIL_IDS = [458791, 458791, 458792] | MISSING GRID (see below); the byte-0 DEFAULTS are the real engine entries — RECONSTRUCTION-ONLY defaults |
| Blend inputs (the factor texture; one-hot band selection by palette-ALPHA; noise operands binary-locked iter036) | iter024 Terrain_14 HLSL + iter036 | 2048 noise-table entries + 13 fail-closed controls | materials_confirmed (the CONFIRMED architecture) | era-9.3.5 CONFIRMED; the noise SEED = [P4] FIXED reconstruction seed 0x30303030 |
| 432502 selectors (65x65 climate grid) | iter029 + iter028 canon | 178 known-ID containers (89 BNT + 82 VFS + 7 ARK) + 27 Parameters + 8,381 Textures entries + 26 containers/179,774 entries (size predicate) | [P1] constant byte 0 -> palette A[0]=0x66DC6 | MISSING locally (patcher-delivered; NOT_DETECTED_UNDER_THESE_PREDICATES for other encodings — F04) |
| 459344 selectors (129x129 detail grids) | iter029 + iter028 | same lines as 432502 | [P2] constant byte 0 -> C[0]=D[0]=458791, E[0]=458792 | MISSING locally (patcher-delivered; same scope note) |
| WAVES/SKY (waves01/02.tga, sky0/1.tga plane textures) | iter023/iter031 (name-registered type-1000 family; 178-container census) | 0 hits in any local container | [P-WAVES]/[P-SKY] SYNTHETIC stand-ins (labeled) | MISSING locally; never claimed historical |
| Historical terrain texture layout recovery | — | NO_DEFINED_DENOMINATOR | the reconstruction renders from palette + details + TDF masks + noise | NOT RECOVERED (the mis-scoped NIF figures do NOT change this) |
| NIF/MODEL TEXTURE CROSS-REFERENCE (24,474/24,508 = 99.8613% binding-chain; 19,705/24,508 = 80.40% name-anchor OBSERVED) | eabf6cf + c380a26 | 24,508 K1 ArkTexture entries over 5,596 NIF models | NOT a terrain input; recorded as the model-texture resolution/association layer | VALID MEASUREMENTS, NIF/MODEL domain only |

## 4. §7.2 HEIGHT REPRESENTATION CONTRACT (A/B separation; no "variants" language)

A. GLOBAL RGB HEIGHT FIELD MODEL
- PHYSICAL RESOURCE: Textures.bnt entry 429259.dat (LOCAL both 9.x eras; absent
  from 2003 corpora; re-hashed 0BADB42E... this lineage; 257x257, 24bpp).
- FRAME: the GLOBAL height field — origin -65,536, 512-unit texels, span 131,072
  (FUN_009478e0; georef run 8b8b106 world-datum pin; +50.0 slot datum
  byte-locked: FADD [0x00A81D20], 2 .text sites 0x00948378/0x00949162).
- SAMPLE DIMENSIONS: 257 x 257 samples.
- UNITS: the (t-128)x5 m model — STRONGLY_SUPPORTED at data level (land
  79.606% = 52,579/66,049 reproduced; min -639.43 m, max +638.91 m).
- SCALE-CALIBRATION / OFFSET-DATUM: the +50.0 slot datum is engine-byte-locked;
  the field-vs-TILE datum mapping remains UNPINNED ([P3b]/open #5).
- DECODE EVIDENCE: Desktop + this lineage decodes; era-bounded (the 2003-era
  loader absence recorded).
- CONSUMER EVIDENCE: the ArkHeightTree leaf recursion reads global-field samples
  (iter027 bound 1; the quadtree construction NOT RE'd — [P3a]).
- HISTORICAL RECOVERY STATUS: the ORIGINAL payload is present and decoded; its
  ENGINE consumption chain is partially RE'd; recovery = DATA-LEVEL, not
  full-consumer-level.

B. TDF u16 HEIGHT REPRESENTATION
- PHYSICAL RESOURCE: the TDF payload height blocks (32x32 uint16 LE at payload
  offset 64) in terrain.bnt/50.bnt.
- FRAME: PER-TILE (the 220x236 filename-xy grid; tile = 128 world units).
- SAMPLE DIMENSIONS: 32x32 u16 per tile. TOTAL = 53,166,080 u16 SAMPLE SLOTS
  across the 51,920 regular 32x32 tile blocks (correction by
  EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927; the historical "1,664,000
  samples" printed here was derivable from NO valid arithmetic over these
  denominators — 51,920 x 32 = 1,661,440 — and is superseded). Two independent
  arithmetic paths, both machine-executed: 51,920 x 1,024 = 53,166,080 and
  (220x32) x (236x32) = 7,040 x 7,552 = 53,166,080. The 53,166,080 count is
  SAMPLE SLOTS, NOT unique height values, NOT unique world points, NOT
  historical rendering coverage, NOT terrain-texture coverage, NOT
  original-client parity, NOT proof of the RGB-TDF bridge (BRIDGE_STATUS
  below = UNKNOWN, unchanged; all calibration/unknown labels preserved).
- UNITS: u16 x 1/128 m = the CURRENT_RUNTIME_CALIBRATION (heightScale 128 u16/m
  = STRONGLY_SUPPORTED calibration, NOT an engine-extracted constant); the PE2003
  decode FUN_0047fb20 = min + (max-min)*u16/65535 (identity + operation CONFIRMED
  at VA; the 9.3.5 sibling FUN_00989e70 = clamp-65535; the full-lerp form in 9.3.5
  itself open #9; the per-tile min/max source open #1).
- DECODE EVIDENCE: 9/9 region tiles byte-faithful vs an independent parser;
  9216/9216 samples identical vs the frozen oracle; 773/51,920 PCG-vs-JUL
  era-divergent tiles recorded.
- CONSUMER EVIDENCE: the terrain patch consumer chain (MaTerrainMapPatch;
  FUN_00934970 serializer match; LOD ring builder consumers).
- HISTORICAL RECOVERY STATUS: BYTE-EXACT heights from original bytes both eras.

BRIDGE_STATUS = UNKNOWN: no evidence in the bounded set proves the conversion
between the global RGB field (A) and the TDF u16 tiles (B) — the historical
downstream contract's "the two models are reconciled as DECODE-MODEL VARIANTS"
language is CORRECTED to: TWO SEPARATE REPRESENTATIONS with UNPROVEN BRIDGE;
consumers must state which representation they consume and MUST NOT treat them as
interchangeable; both evidence lines are PRESERVED (neither is discarded).

## 5. RESULT

Desktop GC-F03 REPRODUCED (the figures traced to their NIF-binding generators;
the terrain-side mis-scope confirmed in the contract/audit/coverage-matrix
locations). The successor downstream content (DOWNSTREAM_CONTRACT_CORRECTIONS.md)
carries the corrected §6 table + the §5 A/B separation. The historical files are
NOT mutated; the correction edges are recorded (FINDINGS.csv F03; V4_1_DELTA
rows 5).
