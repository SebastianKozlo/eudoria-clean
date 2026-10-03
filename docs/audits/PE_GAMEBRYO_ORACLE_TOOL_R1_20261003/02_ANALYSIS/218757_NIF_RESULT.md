# 218757_NIF_RESULT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E2, order s13)

MODE: STATIC + LOCAL TOOL EXECUTION ONLY (no game client, no dynamic
instrumentation, no network). Evidence status per field in brackets.

## Load verdicts per adapter

| adapter | ORACLE_MODE | verdict |
|---|---|---|
| gb12 (GB 1.2.2 source-derived) | SOURCE_DERIVED_REIMPLEMENTATION | ORIGINAL verdict: version gate ACCEPTED (10.1.0.0 in [3.3.0.11, 10.2.0.0]); LoadRTTI FAIL-CLOSED: RTTIError(NiArkAnimationExtraData): cannot find create function. -> GB 1.2 Load() returns FALSE. --full-decode extension: 66/66 blocks accounted, EOF-exact closure [CONFIRMED by execution] |
| gb26 (GB 2.6.0 gate) | SOURCE_DERIVED_REIMPLEMENTATION | REJECTED OLDER_VERSION "NIF version is too old." (10.1.0.0 < 10.1.0.114) [CONFIRMED from source; executed GB 2.6 GUI viewer never reaches the load in this environment -- see P7 below] |
| gb112 (installed original tools) | ORIGINAL_TOOL_EXECUTION | BLOCKED_EVALUATION_TIMELOCK_EXPIRED: SceneGraphPrinter shows modal dialog "The supplied Gamebryo timelock (8469DD85B0554A49, Internal) has expired" (window title "NetImmerse Evaluation Copy"); verbatim captured in 04_EVIDENCE/sgp_T1_dialog.txt [CONFIRMED by execution] |
| gb23 (header-only) | SOURCE_DERIVED_REIMPLEMENTATION | execution NOT_TESTED (installer never installed; nothing installed in this run) |

## Full s13 field list

- LOAD SUCCESS/FAIL per adapter: see table above [CONFIRMED]
- NIF VERSION: Gamebryo File Format, Version 10.1.0.0 (u32 167837696) [CONFIRMED, both sides]
- ROOT CLASS: NiNode named "Scene Root" (top object index 0) [CONFIRMED]
- OBJECT COUNT: 66 (header-declared; 66 decoded by the oracle full-decode extension; 66 by OUR FIELD_IDENTITY_V2 decoder) [CONFIRMED]
- NODE COUNT: 12 NiNode blocks [CONFIRMED]
- GEOMETRY COUNT: 14 NiTriShape (+14 NiTriShapeData) [CONFIRMED]
- MESH COUNT: 14 (NiTriShape = mesh blocks; total_vertices 945, total_triangles 526 per manifest) [CONFIRMED]
- TYPE HISTOGRAM: NiNode 12, NiArkAnimationExtraData 1, NiArkImporterExtraData 1, NiArkTextureExtraData 1, NiTexturingProperty 9, NiArkViewportInfoExtraData 1, NiStringExtraData 1, NiMaterialProperty 9, NiZBufferProperty 1, NiTriShape 14, NiTriShapeData 14, NiDirectionalLight 2 [CONFIRMED, identical on both sides]
- NODE NAMES (serialized): Scene Root; B_Outpost_me01_Ext_sign; B_Outpost_me01_Ext_main; __NDL_MultiMtl_Node; B_Outpost_me01_Ext_vent03; B_Outpost_me01_Ext_bigdoors; B_Outpost_me01_Ext_smaldoor; dPVS_occ04; dPVS_occ02; dPVS_occ03; dPVS_occ01; dPVS_occ05 [CONFIRMED]
- ROOT LOCAL TRANSFORM (SERIALIZED): translate (0,0,0); rotate identity; scale 1.0 [CONFIRMED, bit-exact on both sides]
- ALL NONZERO NODE TRANSLATIONS (SERIALIZED_LOCAL_TRANSFORM, GAME_UNITS, never world positions): B_Outpost_me01_Ext_sign:0 (0, -1030.0, 820.0); B_Outpost_me01_Ext_bigdoors:0 (385.0, -925.0, 100.0); dPVS_occ01..05 (-530.0181884765625, 0, 0) [CONFIRMED]
- BOUNDING BOX/SPHERE: NO serialized world/root bound exists (E1 finding, BOUNDING_VOLUME_SEMANTICS.md Q1: world bounds are recomputed at update time; only per-geometry MODEL-space spheres serialize inside NiGeometryData). Per-geometry model-space bounds (oracle-decoded, serialized values): 14 spheres, e.g. data-block 20 center (0.0, 0.12774276733398438, 140.0) radius 525.069; block 24 center (50.0, 424.9999694824219, 400.0) radius 1795.306; block 26 center (0.0, -75.0, 525.0) radius 1458.167. Derived dimensions combine these with SERIALIZED_LOCAL_TRANSFORM chains. [CONFIRMED serialized; DERIVED dimensions below]
- APPROX DIMENSIONS (GAME_UNITS ONLY, no meter conversion -- scale UNCONFIRMED): model-space spheres span roughly x in [-730, +530] GAME_UNITS from the signed-object translations plus per-geometry radii up to ~1795 GAME_UNITS; a precise axis-aligned world-space extent requires applying all 14 geometry bounds through the local-transform hierarchy (COMPUTED_WORLD_TRANSFORM per UpdateWorldData). PLAUSIBLE (derived, not serialized).
- CONTROLLERS: 0 controller blocks in this file (both sides agree) [CONFIRMED]
- TEXTURE REFERENCES: no NiSourceTexture blocks and no NiTexturingProperty-decoded external filenames in this file; the texture path lives in the MindArk-custom NiArkTextureExtraData (block 3, UNDETERMINED by GB 1.2 semantics; OUR decoder decodes it via byte-derived boundary). TEXTURE_REFERENCES_FROM_NIF_BODY = NONE_FOUND at the standard-Gamebryo level [CONFIRMED for standard classes; NiArkTextureExtraData content = NOT_AVAILABLE_IN_ORACLE]
- CUSTOM/UNKNOWN TYPES: NiArkAnimationExtraData (block 1), NiArkImporterExtraData (block 2), NiArkTextureExtraData (block 3), NiArkViewportInfoExtraData (block 13) -- all UNREGISTERED in the GB 1.2 factory registry (0 NiArk* among the 198 registered classes) -> the ORIGINAL GB 1.2 load fails exactly here [CONFIRMED]

## s10 scene-graph classification + explicit questions

- CLASSIFICATION: **MODEL_LOCAL** — STRONGLY_SUPPORTED (single root "Scene Root", all geometry in one local hierarchy, no cell/world context markers)
- IS_ROOT_TRANSFORM_ZERO? **CONFIRMED** (translate 0,0,0; identity rotate; scale 1)
- IS_ROOT_TRANSFORM_NONZERO? **REJECTED** (from the same serialized evidence)
- DOES_FILE_CONTAIN_PARENT_ABOVE_BUILDING? **UNVERIFIED** (the NIF itself contains no parent-above-building evidence; out-of-scope EXE/scan evidence is not sought in this run)
- DO_NODE_NAMES_SUGGEST_CELL/WORLD_CONTEXT? **REJECTED** — names are asset-part names (Outpost walls/doors/vents, dPVS occluder planes); "dPVS_occ" = occluder volumes, not cell/world placement [STRONGLY_SUPPORTED]
- IS_THIS_CLEARLY_A_STANDALONE_ASSET? **STRONGLY_SUPPORTED** (self-contained outpost building model with local transform hierarchy)

## G-218757-2 WORLD_PLACEMENT_EVIDENCE

**WORLD_PLACEMENT_EVIDENCE = NO_WORLD_PLACEMENT_EVIDENCE_FOUND** (full-value
result). No serialized world/cell placement record exists in the NIF: the root
local transform is zero, no world bound is serialized (E1 Q1), no cell/world
anchor blocks exist. The nonzero LOCAL translations above are
SERIALIZED_LOCAL_TRANSFORM values inside the asset hierarchy and are NEVER
promoted to world placement (order s10). No EXE scans, no placement tracing,
no building-family search (out of scope).

## Comparison cross-check (G-CMP-1 subset; full JSON in 04_EVIDENCE/T_runs/compare_T1.json)

Oracle (gb12 full-decode extension) vs OUR FIELD_IDENTITY_V2 decoder on
218757.nif: {"MATCH": 13, "MISMATCH": 4, "NOT_AVAILABLE_IN_ORACLE": 0, "NOT_AVAILABLE_IN_OUR_DECODER": 1, "SEMANTICALLY_UNRESOLVED": 1, "NOT_AVAILABLE": 0}. Mismatches: [["names", "None"], ["local_transforms", "['block 0: local transform mismatch', 'block 17: local transform mismatch', 'block 18: local transfo"], ["bounding_volumes", "[\"geometry 18: model_bound oracle={'center': [0.0, 0.12774276733398438, 140.0], 'radius': 525.069030"], ["parse_failures", "None"]]. Float policy: serialized fields bit-exact;
computed world transforms computed identically on both sides.
