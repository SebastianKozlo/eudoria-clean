# TWO_MODEL_COMPARISON.md — 296445 vs 218757 (PE 2003 campaign R3)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024 | JOB: PE2003R3-A1 | Date: 2026-10-24
Assembly of existing R3 artifacts; every row carries an evidence path. Rule honored: COMMON mechanism results do NOT close model-specific joins (R3 0H — no cross-model promotion).

## 1. Identity vs variant

| Aspect | 296445 | 218757 | Evidence |
|---|---|---|---|
| Models.ark member | index 1720, 108 876 B, SHA 656795D8…, CRC CFAC1D3B, NIF 4.1.0.12, 155 blocks | index 1189, 56 535 B, SHA C13D0873…, CRC C40B12CA, NIF 4.1.0.12, 62 blocks | `TARGET_MODEL_IDENTITY.json` |
| SAME_MODEL_2003_vs_935 | **IDENTICAL_BYTES** (3-way: ARK == manifest row == M1B3 legacy) | **VARIANT_SAME_ID** (9.3.5 = 57 316 B / 3E8A22C2 / 10.1.0.0; manifest row = the 9.3.5 payload, CS06) | `TARGET_ASSET_PAIR.json`; `CLAIM_SUPERSESSION.csv` CS06/CS08 |
| Standalone file on disk before run | existed (06 + M1B3 copies) | MISSING anywhere; recreated by re-extraction, bit-exact with prior pin | `TARGET_MODEL_IDENTITY.json` comparison_vs_935 |
| Payload identity scope | payload only, NOT world-instance identity | no build/instance/placement transfer between variants (CS08) | same |

## 2. Asset roles (distinct)

| Aspect | 296445 | 218757 |
|---|---|---|
| CO-NAMED role | B_Eu_Slum_Building_b047_01 + lens-flare effect rig | B_Outpost_me01 (plain exterior mesh) |
| Effect inventory | 7× NiArkBillboardNode, NiTextureEffect (sphere-map), NiUVController + NiUVData (U-scroll loop), ArkScript-like extra data ("activeIdle", "LOOP") | NONE (no billboards, no UV controller, no texture effect) |
| Geometry | 30 shapes / 2415 vtx / 1030 tri; world AABB inflated by flare quads | 14 shapes / 1130 vtx / 526 tri; sane extents |
| Materials | Flare ×4, Flare2, Effekt 1, Bajs | "19 - Default", main_doors |
| Semantic class | building-class PLAUSIBLE (naming only, CS07) | outpost-building-exterior PLAUSIBLE (naming only) |
| Evidence | `09_Research\I1_asset_role_296445_218757_20261024.md`; both `MODEL_*_NIF_STRUCTURE.json`; `REPRODUCE_MODEL_*.md` | same |

## 3. Definitions (distinct carriers, identical grammar)

| Aspect | 296445 | 218757 |
|---|---|---|
| Definition | Scripts.ark 4508.obj (dec 3640 B, SHA B6C96E9C…) | Scripts.ark 4057.obj (dec 2688 B, SHA EA93FCA9…) |
| ID constants (E18) | 296445 @0x298 + 296446 @0x244 | 218757 @0x1C8 + 218758 @0x174 (pair NEW in W1) |
| Macro | identical `7700FEDE 00000014 <ID> 7700FDAC 00000014 7700FEEB 00000008` attach-resource-pair macro | same |
| Paired volume | 296446.bvi (1008 B = 21×48 B, CRC 27EE4229) | 218758.bvi (864 B = 18×48 B, CRC 5DD32B83) |
| 9.3.5 oracle | template 4508 A=296445/B=296446 (CS01, QC_PASS history) | templates.vfs 4057 → 218757/218758 (CS09, PRIOR_DESKTOP_MEASUREMENT, primary source MISSING) |
| Evidence | `RESOURCE_INSTANCE_JOIN_2003.csv` E18; `W1\dlob_*_struct.txt`; `KNOWLEDGE_935_SYNTHESIS.md` | same |

## 4. COMMON mechanism (identical for both — same code, same censuses)

| Edge | Status | Evidence |
|---|---|---|
| Archive mount / manager vtable 0x5E7974 / 4 open slots (E01/E02) | CONFIRMED | JOIN E01, E02 |
| open_nif_by_id / open_bvi_by_id / member reader FUN_00464F30 (E03/E04/E05) | CONFIRMED | JOIN E03-E05 |
| NIF deserializer 0x522010→0x5B7170 NetI → wrapper 0x5EBC1C (E06) | CONFIRMED | JOIN E06 |
| ArkScript ingest/DLOB/linker/VM engine machinery (E07/E13/E14/E15/E16/E17) | CONFIRMED | JOIN E07, E13-E17 |
| type-id→definition lookup FUN_00441230 (W3-08) | CONFIRMED | JOIN W3-08 |
| Spawn: frame 0x06 → FUN_00528a40 (BE envelope, LE f32 ×3) → FUN_004688d0 avatar 0x118B → FUN_005030c0 ×100.0 (W3-01/02/03/10) | CONFIRMED | JOIN W3-* |
| Orientation format 3×3 row-major v·M + consumers FUN_004193f0/FUN_00419090 (R3-05) | CONFIRMED (live source UNVERIFIED) | JOIN W3-11, R3-05 |
| definition→open_nif static opener (E08/E20) | **CONFIRMED-NEGATIVE (static)**; dynamic-only next edge; SFO/0x415xxx candidate REJECTED-PRECISELY | JOIN E20, W3-09, R3-01..R3-06 |
| 0x7700xxxx interpreter in client (E19) | UNVERIFIED→negative with full denominators (server-side suspected); partial revision: 0x7fffec7x ARE consumed | JOIN E19, W3-07 |
| Local placement source | NEGATIVE_WITH_DENOMINATOR (install 5 containers + 650 sounds + data.ini; Volumes 831; Scripts 1936 decoded; Models local-only) | `TRANSFORM_DATAFLOW_2003.csv` local_seed; `PLACEMENT_SOURCE_MATRIX.csv` |

## 5. Separate per-model statuses (COMMON does not close model-specific joins)

- The definition→open edge negative (E20) was tested with model-agnostic censuses; it holds for both definitions, but each model's join (4508→296445, 4057→218757) is tracked per-model in `MODEL_*_LOAD_TRACE.json` / `MODEL_*_PLACEMENT_VERDICT.json` — no promotion of one model's evidence to the other (R3 0H).
- SAME_MODEL outcomes differ (IDENTICAL_BYTES vs VARIANT_SAME_ID) and are NOT interchangeable evidence.
- Role-specific downstream expectations differ: 296445 = possibly effect-asset (instance roster may be flare/particle anchors, CS07); 218757 = possibly prefab (roster would be per-outpost instances). Both expectations UNVERIFIED; recorded in `METHOD_935_TO_2003_REPLAY.csv` P19 rows.
- 218757 carries additional model-specific open items absent for 296445: cross-variant structural diff (NOT EXECUTED); 9.3.5 float 21.2574 semantics; CS22 fingerprint negative ceiling.
- 296445 carries model-specific open items absent for 218757: none beyond the COMMON open edges (orientation live source, dynamic open, id-writer slot).

## 6. Per-model verdict blocks

| Status | 296445 | 218757 |
|---|---|---|
| SAME_MODEL_STATUS | IDENTICAL_BYTES | VARIANT_SAME_ID |
| MODEL_ROLE | CO-NAMED B_Eu_Slum_Building_b047_01 (+flare rig); building PLAUSIBLE | CO-NAMED B_Outpost_me01; outpost-exterior PLAUSIBLE |
| MODEL_INSTANCE_JOIN | def 4508; type-id→def CONFIRMED; def→open static-negative; spawn CONFIRMED | def 4057; same split |
| TRANSFORM_SOURCE | NETWORK_RUNTIME_ONLY (local NEGATIVE_WITH_DENOMINATOR) | same |
| AUTHENTIC_INSTANCE_COUNT (offline) | 0 | 0 |
| PLACEMENT_VERDICT | MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS | same |
| Evidence | `MODEL_296445_PLACEMENT_VERDICT.json` | `MODEL_218757_PLACEMENT_VERDICT.json` |
