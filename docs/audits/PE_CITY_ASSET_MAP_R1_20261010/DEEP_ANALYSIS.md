# DEEP_ANALYSIS.md — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (FOUR_MODELS_DEEP_ANALYSIS)

RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
PHASE = FOUR_MODELS_DEEP_ANALYSIS (contract §3 four models + §4 texture edges + GLB comparison + cross-era candidates)
ERA LABELS: `CD_2003` = corpus of the 2003 CD installer (Models.ark/Textures.ark); `PCG_9_3_5` = the newer PCG installation (Models.bnt/Textures.bnt). Never mixed.

## 0. Scope, inputs and identity re-verification

- Worktree `pe-city-asset-map-r1` @ `59641ca`; no commits, no pushes, no master changes. Foreign server port 8140 / PID 21288 untouched (verified at phase end).
- The four primary payloads were re-extracted from the READ_ONLY CD_2003 `Models.ark` (container SHA `f660d055...` re-verified fail-closed) into PRIVATE_OUTPUT; each entry's size + SHA256 matched the phase-2 catalog AND the dispatch pins:
  - `192374.nif` (idx 888, 66,759 B, `08d80c67...`) — `193207.nif` (idx 908, 47,167 B, `220f549b...`)
  - `193313.nif` (idx 910, 66,726 B, `02fc860a...`) — `193684.nif` (idx 913, 75,805 B, `4cc5f920...`)
- All four: NIF 4.1.0.12 (0x0401000C), header `NetImmerse File Format, Version 4.1.0.12`.

## 1. The bounded NIF-4.1 reader (READER_VALIDATION)

`tools/pecompat/nif41_deep.mjs` — a BOUNDED NIF 4.1.0.12 reader for THESE FOUR MODELS ONLY (no general format claim). Validation layers:

1. **SDK-source derivation (authority A).** Standard block layouts were derived from the pinned local Gamebryo 1.2 SDK sources (READ_ONLY architectural reference; no SDK code copied). Per-type citations are recorded in the tool header (NiObjectNET.cpp:553-570, NiAVObject.cpp:546-665, NiNode.cpp, NiGeometry.cpp:620-630, NiTriShapeData.cpp, NiGeometryData.cpp, NiProperty.cpp, NiTexturingProperty.cpp:238-372/838-864/931-940, NiMaterialProperty.cpp, NiAlphaProperty.cpp, NiZBufferProperty.cpp, NiVertexColorProperty.cpp, NiSourceTexture.cpp:162-313, NiExtraData.cpp:109-130; stream conventions: NiBool.h (1-byte), NiStream.inl NiStreamLoadEnum (4-byte), NiStream.cpp LoadCString (i32+bytes), NiGeometryData.h TEXTURE_SET_MASK 0x3F).
2. **Documented historical lineage (authority B, for the MindArk NiArk\* classes only).** Class fields from `nif_parser_v2.py` (PCG935 NIF 4.1.0.12 corpus), placed on the SDK NiExtraData base. The per-entry 9-byte ArkTexture tail is recorded RAW ONLY — the PCG935-era textureId interpretation is explicitly NOT transferred to CD_2003 (no new derivation).
3. **Full-file closure.** A parse is accepted ONLY on: all numBlocks blocks decoded + TopObjects footer + EOF EXACT. All four files close exactly. One bounded correction was made (the run's single reader repair, documented in the tool header): the initial Ark layouts over-read by 4 bytes per block; the SDK-conformant split (nextRef+uiSize base) was reconciled with the historical lineage and MEASURED from raw bytes (animation 57 B total, importer 65 B for the 8-char name, ArkTexture 21 B + entries; both reader splits consume identical totals — the historical parser omits the base uiSize and absorbs it into its class fields; recorded in the READER_VALIDATION NOTE, NOT claimed as an era difference).
4. **Independent second decoder (dual-decode).** The historical Python parser `nif_parser_v2.py` was executed on all four payloads (ORIGINAL_NATIVE layer is unavailable — see §4 — so the dual-decode is the cross-check): AGREEMENT on block-type census, every node/shape name, shape→data pairing, all vertex/triangle counts, UV/normals flags, on all four files. Deltas: the Python parser lacks `NiVertexColorProperty` (unknown-type for it; SDK-derived here) and does not parse the TopObjects footer (its last-block "-8 B misalign" IS the footer, which this reader closes exactly).
5. **Transform composition reuse.** Composed world transforms and scene bounds are computed by the UNCHANGED `src/pecompat/PecSceneIR.js` + `PecTransform.js` (world = parentWorld * local; p → (R*p)*s + t) — the law verified against NATIVE stock-printer controls in the predecessor SceneIR run. Shape→data pairing uses REAL block references (`dataRef`), never order; parent/child from verified `children` refs; roots from the TopObjects footer cross-checked against unclaimed scene blocks (agreement recorded per model).

## 2. Per-model deep analysis

Units/axes discipline (ALL measurements): FILE_SCENE_SPACE — the file's own serialized x/y/z labels, NO axis swap, NO unit conversion; axis semantics (e.g. up-axis) NOT established by the reader; ORIGINAL file units everywhere, NEVER called meters; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT. Footprint = x/z extents per the contract.

### 2.1 193313.nif (CD_2003; first deep case)

- **Status class:** DECODED_FULL_CLOSURE (26/26 blocks; TopObjects footer [0]; EOF exact; scene-graph validation PASS, 0 warnings).
- **Block census:** NiNode 6, NiTriShape 5, NiTriShapeData 5, NiMaterialProperty 5, NiArkAnimationExtraData 1 (OPAQUE), NiArkTextureExtraData 1 (PARTIALLY_UNDERSTOOD, numTex=0), NiArkImporterExtraData 1 (PARTIALLY_UNDERSTOOD, name "4.1.0.12"), NiZBufferProperty 1, NiVertexColorProperty 1. Decode census: 23 SUPPORTED / 2 PARTIALLY_UNDERSTOOD / 1 OPAQUE.
- **Hierarchy:** root `Scene Root` (block 0) with 5 children: `Outpost39_proxymesh`→shape `Outpost39_proxymesh:0`, `MSC`→`MSC:0`, `signs`→`signs:0`, `build`→`build:0`, `MAC`→`MAC:0` (2-level tree, depth 2).
- **Names:** the Desktop name hypotheses (Outpost39_proxymesh, MSC, signs, build, MAC) are REPRODUCED from the original bytes as NiNode names (byte-level names — NOT game classes, NOT city names; MSC/MAC are not promoted to any class without proof).
- **TRS coverage:** 11 AVObjects; ALL local TRS identity (0 non-identity, maxAbsLocalTranslate 0, 0 non-identity rotations, 0 non-unit scales). Root world == local.
- **SCENE_EXTENT (FILE_SCENE_SPACE, original units):** min [-12508.28, -11570.41, 0], max [19257.57, 16369.40, 5308.88]; extents [31765.85, 27939.80, 5308.88]; **maxAxisExtent 31765.85**; footprintX 31765.85, footprintZ 5308.88; 5 meshes.
- **COMPLEXITY:** 1192 triangles / 2384 vertices / 5 shapes / 6 nodes / 26 blocks; 0 invalid indices. Per mesh (verified dataRef): `Outpost39_proxymesh:0` 1928v/964t, `MSC:0` 96v/48t, `signs:0` 96v/48t, `build:0` 240v/120t, `MAC:0` 24v/12t. All meshes: hasNormals=true, **0 UV sets, no vertex colors**.
- **Placement finding: VERTICES** — vertex local extents equal the composed scene extents exactly (spread growth 1.0 on all axes) and every TRS is identity: the layout is stored entirely in vertex coordinates (absolute file-scene positions); transforms contribute nothing.
- **Connected components:** 482+24+24+60+6 = 596 (triangle-index graph per mesh; each component ≈ a 2-triangle pair). **Connected components are NOT building counts.**
- **Texture edges (§4):** ZERO texture bindings in the researched 4.1 scope (0 NiTexturingProperty, 0 NiSourceTexture, ArkTexture numTex=0, 0 UV sets) → **UNTEXTURED_PROXY_MESH** (explicit visual-fallback label; NOT a textured PASS). Material edges REFERENCE_CONFIRMED: each shape → 1 NiMaterialProperty (verified refs 8/12/16/20/24; colors recorded — e.g. Outpost39_proxymesh material diffuse [0.345, 0.561, 0.882]). Root state properties [5,4] = NiVertexColorProperty + NiZBufferProperty. MATERIAL_APPLIED=NOT_YET; BROWSER_OBSERVED=0.
- **Native control:** NATIVE_LOAD_REJECTED (§4).
- **GLB comparison:** no GLB exists (§5).

### 2.2 193684.nif (CD_2003)

- **Status class:** DECODED_FULL_CLOSURE (38/38 blocks; footer [0]; EOF exact; validation PASS).
- **Block census:** NiNode 9, NiTriShape 8, NiTriShapeData 8, NiMaterialProperty 8, + the same 3 Ark/2 state-property blocks as 193313 (NiArkAnimation 1 OPAQUE, NiArkTexture 1 numTex=0, NiArkImporter 1 "4.1.0.12", NiZBuffer 1, NiVertexColor 1). Decode census: 35 SUPPORTED / 2 PARTIALLY_UNDERSTOOD / 1 OPAQUE.
- **Hierarchy:** root `Scene Root` with 8 named children: `signs`, `mlti`, `wall`, `signs01`, `mac`, `build`, `cont`, `forts` (lowercase `mac` here vs `MAC` elsewhere — byte-level names, no class claim).
- **Names:** Desktop hypothesis (signs, mlti, wall, signs01, mac, build, cont, forts) REPRODUCED exactly.
- **TRS coverage:** 17 AVObjects, ALL identity TRS.
- **SCENE_EXTENT:** min [-12830.90, -15486.04, -74.67], max [19238.37, 18253.16, 3687.61]; extents [32069.27, 33739.21, 3762.27]; **maxAxisExtent 33739.21** (the y-axis — largest of the four models); footprintX 32069.27, footprintZ 3762.27; 8 meshes. (Only model with a negative min-z: -74.67.)
- **COMPLEXITY:** 1340 triangles / 2680 vertices / 8 shapes / 9 nodes / 38 blocks; 0 invalid indices. Largest mesh `signs:0` 1600v/800t; smallest `mac:0` 24v/12t. All meshes: normals, 0 UV sets, no colors.
- **Placement finding: VERTICES** (identity TRS; spread growth 1.0).
- **Connected components:** 400+24+48+36+6+42+90+24 = 670 (NOT building counts).
- **Texture edges:** same as 193313 — UNTEXTURED_PROXY_MESH; 8 material edges REFERENCE_CONFIRMED.
- **Native control:** NATIVE_LOAD_REJECTED. **GLB:** none (§5).

### 2.3 192374.nif (CD_2003)

- **Status class:** DECODED_FULL_CLOSURE (22/22 blocks; footer [0]; EOF exact; validation PASS).
- **Block census:** NiNode 5, NiTriShape 4, NiTriShapeData 4, NiMaterialProperty 4, NiArk* 3, NiZBuffer 1, NiVertexColor 1. Decode census: 19 SUPPORTED / 2 PARTIALLY_UNDERSTOOD / 1 OPAQUE.
- **Hierarchy:** root `Scene Root` with 4 children: `Box01`, `MSC`, `MAC`, `signs`.
- **Names:** Desktop hypothesis (Box01, MSC, MAC, signs) REPRODUCED exactly.
- **TRS coverage:** 9 AVObjects, ALL identity TRS.
- **SCENE_EXTENT:** min [-10230.58, -9733.57, 0], max [22558.57, 16306.27, 5952.57]; extents [32789.15, 26039.84, 5952.57]; **maxAxisExtent 32789.15** (largest footprintX of the four); footprintX 32789.15, footprintZ 5952.57; 4 meshes.
- **COMPLEXITY:** 1200 triangles / 2400 vertices / 4 shapes / 5 nodes / 22 blocks; 0 invalid indices. `Box01:0` 2208v/1104t; `MSC:0` 72v/36t; `MAC:0` 24v/12t; `signs:0` 96v/48t. All meshes: normals, 0 UV sets, no colors.
- **Placement finding: VERTICES.**
- **Connected components:** 552+18+6+24 = 600 (NOT building counts).
- **Texture edges:** UNTEXTURED_PROXY_MESH; 4 material edges REFERENCE_CONFIRMED.
- **Native control:** NATIVE_LOAD_REJECTED. **GLB:** none (§5).

### 2.4 193207.nif (CD_2003)

- **Status class:** DECODED_FULL_CLOSURE (14/14 blocks; footer [0]; EOF exact; validation PASS).
- **Block census:** NiNode 3, NiTriShape 2, NiTriShapeData 2, NiMaterialProperty 2, NiArk* 3, NiZBuffer 1, NiVertexColor 1. Decode census: 11 SUPPORTED / 2 PARTIALLY_UNDERSTOOD / 1 OPAQUE.
- **Hierarchy:** root `Scene Root` with 2 children: `Box06`, `Object01`.
- **Names:** Desktop hypothesis (Box06, Object01) REPRODUCED exactly.
- **TRS coverage:** 5 AVObjects, ALL identity TRS.
- **SCENE_EXTENT:** min [-8620.09, -9269.01, 0], max [18320.81, 7643.05, 1570.07]; extents [26940.91, 16912.07, 1570.07]; **maxAxisExtent 26940.91**; footprintX 26940.91, footprintZ 1570.07; 2 meshes.
- **COMPLEXITY:** 864 triangles / 1698 vertices / 2 shapes / 3 nodes / 14 blocks; 0 invalid indices. `Box06:0` 1290v/660t; `Object01:0` 408v/204t. All meshes: normals, 0 UV sets, no colors.
- **Placement finding: VERTICES.**
- **Connected components:** 317+102 = 419 (NOT building counts; `Box06:0` is the only mesh whose components are not pure 2-triangle pairs: 317 components for 660 triangles).
- **Texture edges:** UNTEXTURED_PROXY_MESH; 2 material edges REFERENCE_CONFIRMED.
- **Native control:** NATIVE_LOAD_REJECTED. **GLB:** none (§5).

## 3. Cross-cutting findings (all four)

1. **Common structure:** every model is `Scene Root` + N named NiNodes, each with exactly one NiTriShape `<name>:0`; every shape has exactly one verified NiMaterialProperty ref; every model carries the SAME 3-block Ark extra-data chain from `Scene Root` (NiArkAnimationExtraData → NiArkTextureExtraData (numTex=0) → NiArkImporterExtraData (name "4.1.0.12")) + NiVertexColorProperty + NiZBufferProperty on the root. This is a uniform PROXY-MESH asset class by structure — the byte-level name `Outpost39_proxymesh` on 193313 is consistent with that reading, but NO city/role identification is claimed.
2. **"No Ark classes expected" hypothesis REFUTED by measurement:** the dispatch's working hypothesis (CD_2003 = standard property chain, no Ark classes) is FALSE — all four contain the three MindArk NiArk* classes. The standard NiTexturingProperty/NiSourceTexture chain is entirely ABSENT. The 9-byte-tail non-transfer rule was verified the honest way: there are no Ark texture entries at all (numTex=0), so no tail exists to interpret.
3. **Placement is in VERTICES, uniformly:** all TRS identity; vertices are absolute file-scene coordinates spanning tens of thousands of original units.
4. **Proxy-hull geometry:** ~2 vertices per triangle on nearly every mesh (unshared vertices), components ≈ triangle pairs — consistent with convex-hull/box-proxy exports; NO claim beyond structure.
5. **Coverage delta (phase-2 rankings unchanged):** CD_2003 SCENE_EXTENT/COMPLEXITY coverage moves from 0 measured to **4 of 2,492 measured** (the four primaries); every other CD_2003 model remains UNKNOWN (never 0). Largest-measured-CD_2003 = 193684 (maxAxisExtent 33739.21 original units) — a coverage-limited statement, NOT "largest of all" (2,488 unmeasured).

## 4. NATIVE_CONTROL comparison (ORIGINAL_NATIVE_EXECUTION layer)

Stock Gamebryo 1.2 `SceneGraphPrinter.exe` (SHA `fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c`, copied into the private sandbox; sandbox-local MSVCP71/MSVCR71 via CHILD process PATH — CHILD_PROCESS_PATH_DLL_EXPOSURE class, same as the SceneIR controlB provenance capture; 30 s per-process timeout; argv/cwd/env-delta/exit/stdout/stderr recorded in `PHASE3_NativeControl/run_records.json`):

- All four files: **NATIVE_LOAD_REJECTED** — exit 1, `Error loading stream.`, 0 B stdout (verbatim outcome; no timeout, no crash). The "plausibly loadable by the stock printer" hypothesis is REFUTED by measurement: the NiArk* content makes the stock loader refuse these NIF 4.1.0.12 files exactly as it refuses PCG935 Ark content.
- Consequence (recorded honestly): the vendor-tool cross-check layer is UNAVAILABLE for these four; the independent cross-check executed instead is the PYTHON DUAL-DECODE (§1.4) — full agreement on every standard block, name, ref and geometry count.

## 5. GLB comparison (contract §3)

- Searched: the whole `pe_asset_viewer_v4` tree and `D:\Eudoria_Reconstruction` (depth 6). **NO GLB exists for 192374/193207/193313/193684 anywhere.** The v4 tool's `assets/cd2003/` contains only 16 OTHER CD2003 GLBs (11676, 13078, ... dated 2026-09-04), produced by the M2-3 exporter family (`nif_glb_exporter_uvc_v1.py` — NIF IR → GLB 2.0, Z-up→Y-up (X,Z,-Y), raw UVs) — lineage inspected, but the four primaries were never exported.
- Result: **NO_GLB_PRESENT_FOR_THESE_IDS — numeric comparison SKIPPED** (nothing to compare; no guessed numbers). Their missing textures/textures-in-GLB prove nothing about the originals (flat gray-material GLBs), and the originals' own zero-texture finding (§2) is independent of the GLB question.

## 6. TEXTURE_CHAIN_COVERAGE (contract §4)

- **CD_2003 four primaries:** per model — NAME_FOUND 0 / REFERENCE_CONFIRMED = shape count (4/2/5/8 material edges) / CONTAINER_ENTRY_RESOLVED 0 / IMAGE_DECODED 0 / MATERIAL_APPLIED 0 (NOT_YET — no render this phase) / BROWSER_OBSERVED 0 (phase 4 pending). Texture chains terminate: UNTEXTURED_PROXY_MESH (explicit visual fallback; never a false textured PASS). No image decoding was needed (nothing referenced).
- **PCG_9_3_5 bounded batch (era-labelled):** the 1,551 phase-2-DECODED models (218757 included, verified) re-parsed with the EXISTING PecNif10Reader (no new decode): 1,551/1,551 processed, 0 parse errors; **all 1,551 carry ArkTexture descriptive names**; 4,151 edges extracted: 3,357 texture-name edges ALL `NAME_NOT_FOUND` (the 8,381-entry Textures.bnt catalog is named `NNNNNN.dat` numeric; model names are descriptive like `B_Outpost_me01_Ext_main_0_BASE`) + 794 material-reference edges; 0 NiSourceTexture blocks in the whole decoded set; **NAME_FOUND_EXACT 0, NAME_BASE_MATCH 0** — honest negative, visible; the 9-byte Ark tail stays RAW_ONLY (218757 retraction stands; no new interpretation); 1,382 distinct texture names. (1,545 of 1,551 models carry at least one edge; the 6 edge-less models have ArkTexture blocks but no shape-bound entries — they appear in the batch summary, not the per-model CSV aggregates.) Full per-edge list: `PHASE3_PCG935_BATCH/PCG935_NAME_EDGES.jsonl` (private); aggregates in TEXTURE_LINK_DISPOSITIONS.csv.
- Cross-era discipline: no CD_2003 texture entry ever resolved a PCG935 reference or vice versa (no resolution existed to mix — by measurement).

## 7. CROSS_ERA_CANDIDATES (bounded pointers only; NO identification)

The phase-2 literal ID search was negative (4× NO_LITERAL_ID_MATCH). Candidates (CANDIDATE_ONLY — size proximity within the same NIF version class is NOT identification; no city names, no silhouette matching as proof):

- `192374.nif` (66,759 B) → PCG935 4.1.0.12 candidates: `333375.nif` (66,737 B, Δ22), `131688.nif` (66,927 B, Δ168), `129311.nif` (66,964 B, Δ205)
- `193313.nif` (66,726 B) → `333375.nif` (Δ11), `131688.nif` (Δ201), `129311.nif` (Δ238)
- `193207.nif` (47,167 B) → `65678.nif` (47,229 B, Δ62), `129375.nif` (47,093 B, Δ74), `192811.nif` (47,092 B, Δ75)
- `193684.nif` (75,805 B) → `129281.nif` (75,993 B, Δ188), `335388.nif` (75,346 B, Δ459), `311193.nif` (74,626 B, Δ1,179)
- Bounded name probe (9 unique candidates parsed as a CANDIDATE probe with the phase-3 reader — explicitly NOT a general PCG935 parser claim): 2 decoded (`333375.nif`: names `Scene Root`/`default`/`__NDL_MultiMtl_Node`/`Object01`/`dVPS_no`; `311193.nif`: `Scene Root`/`Cylinder01`/`__NDL_MultiMtl_Node`) — **no name kinship with the primaries**; 7 exceeded the bounded reader (loud failures recorded verbatim: unknown types e.g. `NiTextureEffect`, or PCG935 ArkTexture layout variants — honest PROBE_FAILED outcomes). One textual-pattern pointer (no claim): PCG935 `218757.nif` carries ArkTexture names in the `B_Outpost_me01_Ext_*` family while CD2003 `193313.nif` has the byte-level node name `Outpost39_proxymesh` — different evidence classes, listed only as a candidate pointer.

## 8. Private artifacts (referenced by path; NEVER committed)

- `PHASE3_MODELS/` — the four extracted .nif payloads (SHAs in §0).
- `PHASE3_BlockDumps/` — `<model>_blocks.json` (full semantic dump), `<model>_parts.csv` (part listing with block numbers/names/TRS/vertex+triangle counts).
- `PHASE3_Renders/` — per model: `_topdown_xz_filled.png`, `_topdown_xz_wireframe.png` (file x/z plane; image x=file x, image y=file z; z-buffer over file y; axis semantics NOT established), `_iso3d_wireframe.png` (isometric reading aid over file x/y/z; NOT a world-space claim), + `RENDER_MANIFEST.json` (per-mesh color legend; original origin preserved, image maps the composed AABB 1:1).
- `PHASE3_NativeControl/` — exe+DLL copies, run_records.json, per-model stdout/stderr captures.
- `PHASE3_PCG935_BATCH/` — `PCG935_NAME_EDGES.jsonl` (4,151 era-labelled edges), `PCG935_NAME_BATCH_SUMMARY.json`, `CROSS_ERA_CANDIDATE_PROBE.json`.

## 9. Honest limits

- The reader is bounded to these four files' needs; unknown types loud-fail (PCG935 probes demonstrated this honestly — 7/9).
- NiArkAnimationExtraData tail (33 B) and importer tail (13 B + 7 f32) remain OPAQUE/PARTIALLY_UNDERSTOOD (raw bytes recorded).
- The CD2003 models' Ark classes carry NO texture entries; nothing here establishes any CD2003 name→container mapping, and none is needed for these four.
- MATERIAL_APPLIED and BROWSER_OBSERVED remain 0 everywhere until a real browser render (phase 4+); nothing here is a textured PASS.
- No city/place identification, no world coordinates, no client execution, no milestone/canonical-gate effect.
