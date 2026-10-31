# KNOWLEDGE_COVERAGE + CAPABILITY_MATRIX — per-domain honest coverage (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.
Legend: **decoded** (format readable from source), **bound** (semantic binding to runtime), **rendered** (visible in the world), **source-verified** (independently verified vs source SHA/census), **historical recovered** (original historical meaning/inputs recovered).

## Capability matrix

| Domain | decoded | bound | rendered | source-verified | historical recovered |
|---|---|---|---|---|---|
| Terrain (heights, TDF, streaming, LOD) | ✓ | ✓ | ✓ | ✓ (terrain.bnt pin, census 51,920/51,920; pixel-stable across r185→r187) | ✗/n-a (height data IS the historical data — nothing external to recover) |
| Materials (TDF tails, masks, textures, slots) | ✓ | ✓ | ✓ | ✓ (583/959/105 counters, 0 missing; 448,384 tail records 0 fail) | ✗ (which slot the 9.3.5 client bound = UNRESOLVED; first-resolvable slot = RENDER_RECONSTRUCTION) |
| Biome palettes (.vcl species) | ✓ (31/32; 25.vcl UNSUPPORTED) | ✓ (to runtime palettes) | ✓ (species in scenes) | ✓ (VegetationClimates.bnt SHA-pinned census) | ✗ — biome ASSIGNMENT is upstream/unknown (see below) |
| Biome assignment (region→climate) | ✗ | ✗ (stand-in `tile>>5→profile`) | ✓ (stand-in, badged) | ✗ (no client-side selector found; 432502 NOT_FOUND_LOCALLY, 178 containers searched) | ✗ — UPSTREAM_ORIGIN_UNKNOWN; P-CLIMATE/P-CELLSTREAM open |
| Player mesh + skin (546608) | ✓ | ✓ (bind law 38/38, weights max 3 no truncation) | ✓ (textured skinned body) | ✓ (member SHAs vs CORPUS_METADATA_CENSUS) | ✗ (identity = GAME_CHARACTER_REF; species name UNRESOLVED; not claimed player avatar) |
| Player clips (546617 idle / 546613 walk) | ✓ (closure-exact parser, known-answer 11/11) | ✓ (44 tracks each, oracle-verified) | ✓ (idle↔walk from WASD, gates G1–G5) | ✓ (container+member SHAs, gb12 oracle 0.094°/0.135°, negative fired 4.50°) | ✗ (clip NAMES do not exist in the data — KINEMATIC_CLASSIFICATION labels; no historical binding) |
| Building placement (296445/218757) | ✗ (resource bytes present, definition→resource edge OPEN in-build) | ✗ | ✗ | ✗ (no world instances; NO_CARRIER_IN_CLIENT_DATA bounded) | ✗ — HISTORICAL_PLACEMENT=NOT_ESTABLISHED |

## Standing honesty canons (verbatim)

- **HISTORICAL_PLACEMENT=NOT_ESTABLISHED** — for buildings and for vegetation instance positions alike; no original tree/building layout is claimed anywhere.
- **WORLD_XYZ_RECOVERED=NO** — no historical world XYZ frame has been recovered for placement consumers.
- **CANONICAL_GATE_EFFECT=NONE** — no milestone promotion is implied by this coverage table.
- **GAME_ANIMATIONS_ONLY=YES** — both activated clips (idle 546617, walk 546613) have source certs; zero synthetic clips (a bindpose would be NOT_DEMONSTRATED; here both clips are real and played).

## Coverage arithmetic honesty

- File/record counts are per-domain and are NOT summed into any "FULLY_RECOVERED" claim: e.g. materials 583/583 = the active window's layers (not the map); 12/12 material fixture = fixture only; 51,920/51,920 = the terrain tile census (data containers, not recovered history).
- Vegetation: species palettes VERIFIED ≠ forest layout recovered. The rendered layout is a deterministic LAB stand-in (PEFoliageLabSeed), explicitly NOT_HISTORICAL.

## Sources (file + SHA256)

- QC_ROLLING_R1/QC_REPORT.md — SHA256 76F2DB60CB88EE2363840A3C18D188D4EACD1CAF655083F1291495D351574ED8 (all domain verdicts re-derived).
- Domain evidence: SCI W1..W5 trees (W1 MATERIAL_CHAIN_COUNTS.json, W2 VCL_CENSUS.json + VEGETATION_PROVENANCE_GRAPH.json, W3_PLAYER\*, W4 ANIMATION_MANIFEST + ORACLE, W5 BUILDING_PLACEMENT_STATUS.md).
- VEGETATION_INSTANCE_SOURCE_CERTS.md / FIRST_MISSING_EDGE.md — SCI 04_REPORT\ (per-actor stand-in certs, open edges).
