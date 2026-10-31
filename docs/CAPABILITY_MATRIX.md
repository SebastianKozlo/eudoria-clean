# CAPABILITY_MATRIX — machine-usable per-domain capability table (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.
Companion to KNOWLEDGE_COVERAGE.md (same verdicts; this file is the flat table for tooling).

| domain | decoded | bound | rendered | source_verified | historical_inputs_recovered | note |
|---|---|---|---|---|---|---|
| terrain | YES | YES | YES | YES | NO (n/a — source data is the historical data) | terrain.bnt pin 95841761…; census 51,920/51,920; fa pixel-stable r185→r187 |
| materials | YES | YES | YES | YES | NO | 583 home / 959 post-move / 105 far layers, 0 missing; slot binding UNRESOLVED (RE 9.3.5) — first-resolvable = RENDER_RECONSTRUCTION |
| biome_palettes (.vcl) | YES (31/32) | YES | YES | YES | NO | 32 text profiles, SHA 7B858401…; 25.vcl UNSUPPORTED (comma tokens) |
| biome_assignment | NO | NO (stand-in) | YES (badged stand-in) | NO | NO | `tile>>5→profile` = ENGINEERING stand-in; climate 432502 NOT_FOUND_LOCALLY (178 containers); UPSTREAM_ORIGIN_UNKNOWN; P-CLIMATE/P-CELLSTREAM OPEN |
| player_mesh_skin | YES | YES | YES | YES | NO | GAME_CHARACTER_REF 546608 (MOB_FAMILY); bind law 38/38; weights max 3, 0 truncation; species name UNRESOLVED |
| player_clips | YES | YES | YES | YES | NO (names don't exist in data) | 546617 idle / 546613 walk; KINEMATIC_CLASSIFICATION labels; gb12 oracle 0.094°/0.135°, negative 4.50°; GAME_ANIMATIONS_ONLY=YES |
| building_placement | NO | NO | NO | NO | NO | definition→resource edge OPEN in-build (296445/218757); NO_CARRIER_IN_CLIENT_DATA (bounded); HISTORICAL_PLACEMENT=NOT_ESTABLISHED |

Standing canons (verbatim, apply to every row): HISTORICAL_PLACEMENT=NOT_ESTABLISHED · WORLD_XYZ_RECOVERED=NO · CANONICAL_GATE_EFFECT=NONE · GAME_ANIMATIONS_ONLY=YES (both activated clips certified).

Counts are per-domain; never summed into FULLY_RECOVERED.

Sources: see KNOWLEDGE_COVERAGE.md (full source list with SHAs).
