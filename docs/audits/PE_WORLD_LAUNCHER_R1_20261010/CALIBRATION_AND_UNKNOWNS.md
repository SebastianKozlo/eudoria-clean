# CALIBRATION_AND_UNKNOWNS — PE_WORLD_LAUNCHER_R1_20261010 (ETAP C + D + E)

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = ETAP_C_LAUNCHER_TERRAIN + ETAP_D_TERRAIN_TEXTURES + ETAP_E_VEGETATION
SCOPE = the CURRENT_RUNTIME_CALIBRATION preset used by the /launcher + /world
apps (contract §4 invariants), documented WITH PROVENANCE, every UNKNOWN that
bounds what this phase can honestly claim, AND the Etap D terrain-texture
preset (RENDER_RECONSTRUCTION) + the Etap E vegetation preset with their own
provenance.

## 1. The CURRENT_RUNTIME_CALIBRATION preset (what it IS and is NOT)

| Property | Value | Source / status |
|---|---|---|
| Height scale | u16 / 128 → meters | deployed runtime calibration (historical eudoria-web heightScale = 1/128); **CURRENT_RUNTIME_CALIBRATION**, STRONGLY_SUPPORTED — NOT a proven historical engine fact |
| Spatial step | 2.0 adapter units per height sample | deployed runtime world scale 2 (EudoriaWorldTransform legacy scale); CURRENT_RUNTIME_CALIBRATION — NOT a proven historical engine fact |
| Min/max lerp | identity (min=0, max=65535 in u16 space) | FUN_0047fb20 form `min + (max-min) * u16 * (1/65535)` is CONFIRMED; the per-tile min/max source is **UNRESOLVED** (TDF sub-header payload 52..63 reads ZERO on sampled content tiles) — the identity lerp is equivalent to raw u16 until resolved |
| Adapter axes | +X = grid-x (meters), +Y = height (meters), +Z = grid-y (south) | PETerrainRegion.buildGeometry world convention; PE axes beyond this calibration are UNRESOLVED |
| Tile size | 32×32 samples = 64×64 adapter m | TDF tileDim=32 (CONFIRMED); the 64 m is the preset step × 32 |

**Application discipline (verified by gate):** the conversion is applied
EXACTLY ONCE — inside `PETerrainRegion.buildGeometry` via
`worldHeightMeters(u16)`. The world app adds NO further scale to the terrain
mesh (scene transform = mesh.position = windowOrigin × 64 m, scale 1; viewer
fit/centering happens ONLY in the camera controller — the camera-UX lesson:
correct world matrices before any fit, no double centering). Reversibility is
measured: `meters × 128 == raw u16` exactly for every vertex
(WORLD_TERRAIN_BOUNDS_CALIBRATION_ONCE; 128 = 2^7 so u16/128 is
binary-exact). The NIF viewer's `.01` model conversion is NOT applied to
terrain (never transferred without control); model/terrain conversion
consistency is an Etap E concern (no models are mounted in the world view in
this phase).

**Why it is a PRESET:** every number above is a runtime calibration of OUR
reconstruction, carried in configuration + provenance. It makes NO claim
about the historical PE engine's meters, axes, world size or camera
conventions. Position readouts in /world are labeled
"jednostki adaptera" (adapter units) + tile key + raw u16 — never
"oryginalne XYZ".

## 2. Terrain data facts this phase BUILDS on (measured, not assumed)

- TDF: 32×32 uint16 LE per tile; heights at payload offset 64..2111 (2048 B);
  bytes 52..63 are a SEPARATE sub-header, not heights (WORLD_TERRAIN_OFFSET_
  64_NEGATIVE — discriminating on 5/6 sampled tiles; the all-zero tile
  000a0014.tdf is a measured degenerate case where both byte ranges are
  zero; recorded in the gate).
- Sentinel `7ffe7ffe.tdf` is NOT a regular tile (measured header: payload
  56,233 B, data_size=56,221, tileDim=237); production decode refuses it;
  regular addressing range 0..219/0..235 excludes it and the 6,530 special
  rows (gridY measured 0xff5a..0xffff).
- The regular grid is FULLY populated: 51,920/51,920 names present in the
  index (measured); NODATA (missing/failed) = 0; raw u16 = 0 tiles
  (22,481 = 43.3%) are DATA, not NODATA.
- Inter-tile topology (documented RENDERER choice, contract §4): the active
  window is ONE 8×8-tile `PETerrainRegion`; `buildGeometry` emits quads across
  tile borders derived from the ADJACENT ORIGINAL samples of the two
  neighboring tiles. Tiles are DISJOINT 32×32 sample blocks — no vertex
  sharing/overlap, NO seam repair, NO height changes for jump masking; the
  measured border differences are ORIGINAL DATA (seam diagnostic recorded in
  the world battery). One region mesh per window → no inter-region cracks
  inside the active set; the window edge is the streaming boundary.
- Renderer-side reconstruction aids (explicitly labeled, never source-data
  claims): computeVertexNormals() + the height-preview palette
  (RECONSTRUCTION_PREVIEW), the walk-mode eye offset 1.7 m, camera speeds,
  fog/background choices.
- **Etap D terrain-texture facts (measured, not assumed)** — the chain
  proven in WORLD_DATA_PROVENANCE.json ETAP_D_MATERIAL_CHAIN:
  - named material records: mask @ record+56 (fields 52..55 = extra4 =
    measured `[0,0,0,0]` on every sampled record — NOT mask); RAW or RLE
    (count,value) with EXACT consumption; INDEPENDENT per-layer u8 weights;
    per-cell layer sums in the sampled windows range FAR above 255 (e.g.
    653..1298 per cell in the spawn window) — sums>255 are ORIGINAL DATA and
    are NEVER normalized anywhere in the pipeline (WORLD_MAT_WIRE_BITEXACT
    proves the served weights are the raw tail bytes).
  - the material→texture relation: **id@+16 → "`<id>.dat`"** — engine-RE
    CONFIRMED (the 9.3.5 record parse reads sub@+16 as the material TEXTURE
    id: M1_TSFS iter015e/f, iter030; EU935 census GROUND_TEXTURES §3) and
    re-measured per sample THIS RUN (every sampled id resolved; wire bytes
    bit-exact the physical container reads). This is NOT a
    materialId==textureId *assumption* — it is the carried-forward
    engine-derived relation, re-verified; resolution is BY ID (names are
    display metadata; the id↔name relation is measured MANY-TO-MANY:
    id 37944 = "Test3" in most sampled tiles, "Snow" in others).
  - the 9.3.5 engine's OWN use of these masks: the LOD **vertex-color
    (lighting tint) bake** `lerp(vertexColor, materialTexture(u,v),
    mask/255)` + the zone shadow-paint carrier (iter030, 838/838 consumer
    census) — the ground ALBEDO in 9.3.5 was the climate palette pipeline
    (its per-location inputs 432502/459344 are MISSING locally). Therefore
    the /world textured terrain is the labeled **RENDER_RECONSTRUCTION
    preset**: era-evidenced blend FORM (sequential lerp by RAW mask/255 in
    record order) applied to albedo, with reconstruction-chosen UV repeat
    (32 m, by analogy to the era-evidenced 32/32/16 detail density), nearest
    16×16 cell sampling, SRGB passthrough, caps 16 layers/cell + 48 texture
    slots (measured window max: 12 active layers/cell, 28 distinct textures).
    The full preset text lives in compat/world-splat.js
    (RENDER_RECONSTRUCTION_PRESET — the single source of truth, surfaced in
    the /world evidence panel).
  - `Data\Textures\Terrain.bnt` in the PCG install is **12 bytes** (8 zero
    bytes + "BNT2" — measured) — it is NOT a texture atlas; the real corpus
    is Textures.bnt (8,381 entries, pinned SHA 61ACD13B…).

## 2b. The Etap E vegetation calibration (RECONSTRUCTION_PREVIEW — contract §6)

| Property | Value | Source / status |
|---|---|---|
| Vegetation u16 window | u16 = world meters × 2.0; tile (gx,gy) → u16 box [gx×128, (gx+1)×128) × [gy×128, (gy+1)×128) | **CURRENT_RUNTIME_CALIBRATION** — the same documented page-calibration family as the deployed foliage page (terrain/foliage_system.js); the historical grid extents are settings-scaled and NOT statically pinneable ([P-WINDOW]) |
| Instance cell stream | LAB_SEED-keyed deterministic stand-in (PEFoliageLabSeed.generateTileInstances) | **RECONSTRUCTION-ONLY** ([P-CELLSTREAM]) — the historical cell-stream source is NOT closed (iter032 bound 3); the record FORMAT {u16,u16,u32} + the spawn arithmetic are the CONFIRMED parts |
| RNG chain | PEFoliageCore (seed FUN_0098cdf0 / LCG FUN_0098ce30 / lerp FUN_0095ac30 / node01=÷65535 f32; FLOAT64 operand lock iter035) | **RECOVERED** — imported UNTOUCHED (verified byte-identical to HEAD + reproduced against an independent formula reimplementation); LAB_SEED is NOT equated with the unestablished p3 (p3 = 0, shown separately) |
| Per-record count | max(0, round(col1 × densityPercent/100)) — at 100% the exact PEFoliageCore rule round(col1) | the preview-density filter is a RECONSTRUCTION knob; the .vcl col1 values are ORIGINAL data (role PLAUSIBLE, iter032) — never edited |
| Model unit bridge | NIF cm → m ×0.01, applied EXACTLY ONCE (in the per-shape geometry) | the era m→cm ×100 evidence (FUN_0082b790); a SECOND ×0.01 in the instance matrices was measured and removed (the trees rendered at 1/50 size — caught by the pixel toggle gate) |
| Model axis bridge | NIF Z-up → Three Y-up (x, z, −y) | the deployed legacy-exporter + model_witness.js mapping; the engine's own transform NOT decompiled ([P-AXIS]) |
| Model scale bridge | instance scale = binary node scale (f32, bit-exact on every instance) × (2.0 / NODE_SCALE_MUL) = lerpValue × 2.0 | the EXACT deployed foliage-page ratio ("preserves the previously-deployed effective tree sizes") — **CURRENT_RUNTIME_CALIBRATION**, NOT historical truth |
| Placement | terrain height sampled from the SAME active window region (bilinear over the raw u16 → adapter meters) | RECONSTRUCTION (the historical heightfield-client attach semantics are not reproduced 1:1) |
| Material | fixed MeshBasicMaterial (vertex-shaded: texture × vertex colors; alpha from the shape's NiAlphaProperty); DoubleSide; no wind animation | the era technique FX 0x3EC 'Vegetation' is vertex-shaded (iter032 stage 9); the exact D3D8 technique is NOT reproduced ([P-MATERIAL]) |
| Visible-instance cap | 5000 — a HARD display limit; census requested/rendered/limited in the UI | contract §6.7; the limited subset is a deterministic prefix of the generation order; never fake full coverage |

**The three-way separation (contract §6, binding — surfaced in the launcher +
world UI + every artifact):** ORIGINAL_CLIMATE_RECORDS (strict .vcl decode;
25.vcl stays UNSUPPORTED — never comma-converted) | RECOVERED_RNG_ARITHMETIC
(the untouched byte-locked PEFoliageCore chain) | INSTANCE_DISTRIBUTION (the
documented LAB_SEED wrapper — reconstruction-only). VEGETATION_MODE =
RECONSTRUCTION_PREVIEW. The default profile (0) is a MEASURED choice (12
non-empty records; contains the witness 457485 whose NIF the EXISTING
qualified importer was cross-validated for) — never "the historical biome of
this place".



## 3. UNKNOWNs (honest boundaries — each blocks the claims listed)

| # | UNKNOWN | Status | What it blocks in THIS product |
|---|---|---|---|
| U-1 | Vegetation CELL-STREAM SOURCE — the original per-cell instance stream that fed the historical tree placement is NOT established (PEFoliageCore documents [P-CELLSTREAM]) | UNRESOLVED — **RESTATED in Etap E: still UNRESOLVED**; the delivered vegetation keeps INSTANCE_DISTRIBUTION = reconstruction-only (the LAB_SEED-keyed PEFoliageLabSeed stand-in) | Etap E delivered the deterministic preview, but "historyczna liczba drzew / rozmieszczenie" may NOT be claimed; LAB_SEED is a preview knob over a documented wrapper, NEVER the historical seed |
| U-2 | CLIMATE→REGION MAPPING — which .vcl index applies to which world region is UNRESOLVED (no recovered mapping) | UNRESOLVED — **RESTATED in Etap E: still UNRESOLVED**; the delivered default profile (0) is the MEASURED choice (DECODED + 12 non-empty records + the witness-model 457485 support census) | never "the historical biome of this place"; profile→terrain binding stays a reconstruction setting |
| U-3 | HISTORICAL METERS/AXES — the historical PE engine's units, axis conventions, world size and origin are UNVERIFIED from the engine | UNVERIFIED | all readouts labeled adapter units; WORLD_XYZ_RECOVERED = NO; no claim that u16/128 or 2 units/sample was PE's runtime scale |
| U-4 | Per-tile min/max source for the height query (FUN_0047fb20 form) | UNRESOLVED (identity lerp used — equivalent to raw u16) | any future "true elevation" readout; current meters are preset meters |
| U-5 | PCG special rows (6,530 entries, gridY 0xff5a..0xffff) semantics | UNRESOLVED | excluded LOUDLY from regular addressing; never rendered, never counted as NODATA |
| U-6 | Sentinel tile role beyond "overview/NOT-a-regular-tile" | UNRESOLVED (semantics beyond classification not claimed) | not used as terrain data; only census metadata |
| U-7 | Terrain material→texture binding (materialId == textureId NOT established) | **RESOLVED for the sampled scope in Etap D** (engine-RE CONFIRMED relation id@+16 → `<id>.dat` + per-sample re-measurement; see ETAP_D_MATERIAL_CHAIN) — the standing "NOT established" applied to the ASSUMPTION; the proven relation is carried with full provenance; an id with no entry stays an explicit UNRESOLVED binding (diagnostic, never a fallback) | the /world texture toggle is LIVE (Etap D); no name-match-driven binding anywhere |
| U-8 | Water system (original) | NOT_RECOVERED (PESourceMount.getWaterResource fails loudly) | no water rendering claims; raw-0 tiles are not labeled "water" |
| U-9 | Historical building/instance placement | NOT_ESTABLISHED | no models are placed in the world; HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED; catalog models stay in the catalog app |
| U-10 | .vcl profile 25 (comma tokens at record 9 col 1) | UNSUPPORTED_BY_CURRENT_DECODER (strict refusal kept) | profile 25 is listed UNSUPPORTED and is NOT selectable/comma-converted |
| U-11 | TDF material-tail system records (dim 2/4/32/256) roles | ROLE_UNVERIFIED (labels carried) | Etap D consumption only of named records with verified semantics |
| U-12 | LAB_SEED / p3 relationship — p3 (RNG input) semantics and whether LAB_SEED maps to any original input | UNVERIFIED ([P-RNG-P3]) — **RESTATED in Etap E: still UNVERIFIED**; the delivered UI/census shows p3 = 0 SEPARATELY; LAB_SEED keys only the [P-CELLSTREAM] stand-in | LAB_SEED is never called "the original seed"; the unestablished p3 is never equated with LAB_SEED |
| U-13 | Material-texture UV repeat — no PE evidence pins the repeat of the `materialTexture(u,v)` sampling in the 9.3.5 vertex-tint bake (the 32/32/16 world-unit repeats are the CLIMATE DETAIL textures, a different texture class) | UNVERIFIED (reconstruction choice: 32 m global world uv, by analogy) | the /world textured terrain's repeat is labeled RENDER_RECONSTRUCTION — never claimed as the historical density |
| U-14 | Material-mask "edge-extended at load" semantics (iter030) — the exact extension rule of the 16×16 masks over the 32×32 tile is not pinned | UNRESOLVED | the preview samples the nearest 16×16 cell (flat within a 4×4 m cell; documented choice); the engine's edge extension is not claimed |
| U-15 | Material-texture role beyond the 9.3.5 vertex-tint bake — whether any 9.3.5 path also splats these textures into albedo (the census says NO for base/factor/detail; an exhaustive 838/838 consumer census exists, but the albedo reconstruction is OUR choice) | ROLE_RECONSTRUCTED (the /world albedo splat = RENDER_RECONSTRUCTION) | no claim that the historical 9.3.5 ground looked like this render; the historical albedo (climate palette pipeline) needs the MISSING inputs 432502/459344 |
| U-16 | id↔name many-to-many — id 37944 = "Test3"/"Snow" (measured, Etap D); the per-record name field is display metadata with no 1:1 id mapping | MEASURED (does not affect the id-driven texture chain) | names are never used for resolution; the chain resolves by ID |
| U-17 | MODEL-TEXTURE decoder subset — the vegetation model texture space contains payloads OUTSIDE the strict TGA subset (measured: 166881.dat is a DDS payload, bound by the profile-0 models 166878/166897) | MEASURED (Etap E): the strict decoders refuse LOUDLY; the models render in the honest-untextured class with a diagnostic — NEVER a fallback texture | no claim that every profile model renders textured; the per-model support census is the honest count (8 textured / 2 untextured / 0 parse-unsupported for profile 0) |
| U-18 | NON-VISUAL NIF shapes — the untextured Bip01/Box 24v/12t shapes in multi-shape models (457523: 1/2; 166878: 3/12; 166897: 1/4) have NO texprop→Ark chain | ROLE_UNVERIFIED (collision/bounds candidates — the BVI local-collision corpus finding; carried + counted, never rendered as visual geometry) | no claim that the collision candidates are visual; the per-model visual-shape counts are the honest render scope |
| U-19 | SPLAT TERRAIN APPEARANCE IN HEADLESS CAPTURES — the Etap D splat terrain rendered near-black in the headless GPU captures (canvas uniqueColors ~370 for #textures=1&veg=0 vs ~21,593 for the palette preview) while the palette material, the vegetation meshes and ALL DOM-side census data rendered/verified correctly | **RESOLVED in the U-19 correction round (2026-10-10, post-QC)** — TWO defects in SPLAT_FRAG (compat/world-app.js), both fixed: (a) the sampler2DArray layer coordinate used the NORMALIZED idx byte (texelFetch on the RGBA8 idx textures returns byte/255) instead of the LAYER NUMBER — the QC P2-1 root cause, confirmed at code level; fixed with the EXACT decode floor(b*255.0+0.5): byte k -> array layer k (the empty-slot guard < 254.5 now evaluates the DECODED value — pre-fix it compared the normalized byte against 254.5 and was always-true); (b) THE BLEND FACTOR was DOUBLE-DIVIDED: `w0.x / 255.0` where the texelFetched weight is ALREADY the normalized RAW mask/255 — a factor 1/255x too small, collapsing every blend to ~tex*0.004 = the near-black render — found in THIS correction round (the DOMINANT cause of the observed near-black; (a) alone would have produced wrong-but-visible layer-0 colors on a healthy GPU). EVIDENCE (real headless GPU session — ANGLE/Microsoft Basic Render Driver): the NEW per-color gate WORLD_U19_PER_COLOR_EXACT — 36 valid raycast samples over 36 distinct cells, every read capture pixel within the INDEPENDENTLY recomputed exact shader-math color span (mean max-channel delta 0.55/255, max 1.39/255 — the fp32 bilinear rounding floor; expected colors recomputed in Node from the same wire payloads through PETerrainRegion/buildRegionSplatData/decodeTga2 + the camera pose cross-checked against the page's own position HUD); WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED — the pre-fix expectation does NOT match the read pixels (34 discriminating samples, mean max-channel delta 65.95 — a still-broken shader FAILS this control); WORLD_U19_LAYER_MAPPING_CONTROL — every slot byte indexes a REAL texture slot and the render itself proves layer k maps to texture layer k; the canvas-region census pre->post: uniqueColors 370 -> 65,240, lumaMean 12.2 -> 90.67, lumaMax 253 (real TGA-derived colors). FULL REGRESSION GREEN with the fix: world 44/44, catalog 41/41, unit 24/24, app 22/22; both PIXEL toggle gates re-measured PASS (texture 48.86% of canvas pixels differing, meanAbsΔ 62.43; vegetation 6.26%, meanAbsΔ 58.86); the RAW weights stay bit-exact the served masks, the RECORD-ORDER sequential lerp and the RENDER_RECONSTRUCTION preset labels are UNCHANGED (the fix implements the documented "RAW mask/255 lerp" correctly). | the interactive-browser appearance remains UNVERIFIED (INTERACTION = NOT_PERFORMED — the automation daemon is down; the headless per-color proof is NOT interactive verification, and a real-GPU/non-WARP session is separate future evidence); the per-color proof covers the SETTLED spawn window (#tile=53,114, 36 cells) |
| U-20 | .vcl column semantics beyond col0..col3 — col4/col5 (the "elevation band" candidates) and cols 6..11 | UNVERIFIED (carried RAW on every instance; NO filtering applied; col1 density role PLAUSIBLE, iter032) | no elevation-band filtering claim; the profile picker shows col0..col3 with explicit col-semantics labels |

## 4. Standing honesty labels (surfaced in the UI, never removed)

- era świata = **PCG_9_3_5** (CD-era label in the source layer = CD_JAN_2003,
  explicit mapping, never identified with JUL_2003);
- the launcher overview is an EXPLICIT DOWNSAMPLE (1 px = 1 tile = mean of
  1,024 raw u16); hover shows raw u16 per tile; the selected tile preview
  shows the exact per-sample RAW uint16 (fetched from the tile API — real
  decoded bytes);
- NODATA ≠ height 0 (both visible distinctly);
- terrain textures (Etap D) = ORIGINAL payloads from the pinned PCG
  Textures.bnt through the proven chain (id@+16 → `<id>.dat` → decodeTga2
  → GPU splat with RAW weights); the blend FORM is era-evidenced, the
  ALBEDO ROLE, the UV repeat and the cell sampling are the labeled
  RENDER_RECONSTRUCTION preset; unresolved bindings are explicit diagnostics
  (never a fallback texture);
- vegetation (Etap E, LIVE) = RECONSTRUCTION_PREVIEW: ORIGINAL_CLIMATE_
  RECORDS (strict .vcl decode; 25.vcl stays UNSUPPORTED) + the RECOVERED
  byte-locked RNG chain (PEFoliageCore, untouched) + the DOCUMENTED LAB_SEED
  wrapper (PEFoliageLabSeed); the INSTANCE_DISTRIBUTION is reconstruction-only
  — no historical seed/count/biome/placement claims; models are ORIGINAL
  same-era NIF payloads through the EXISTING qualified importer with their
  original textures where the binding resolves (unresolved texture chains
  render honestly untextured — never a stock pine under the same id); the
  5000 visible-instance cap is a HARD display limit with honest
  requested/rendered/limited counts; VEGETATION_MODE = RECONSTRUCTION_PREVIEW;
- position readouts = adapter units + tile key + raw u16 — never
  "oryginalne XYZ";
- spawn = data-derived (user selection or the highest measured mean tile) —
  no city-name guessing.
