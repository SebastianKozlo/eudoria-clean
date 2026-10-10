---
name: pe-gamebryo-rosetta
description: Interpret and implement PE NIF scene behavior using local versioned Gamebryo SDK sources and PE Rosetta evidence. Use for scene loading, hierarchy, transforms, instance sharing and renderer integration for Project Entropia assets. Carries the MEASURED outcomes of PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009 (218757 adapter + SceneIR + local viewer). This skill does not establish historical placement or complete PE compatibility.
---

# PE Gamebryo Rosetta

Use this skill to turn a specific SDK mechanism and PE evidence into a tested
client behavior. It is a starting reference, not a claim of completed engine
research — and (since 2026-10) it carries TWO fully executed implementation
lineages: the 218757 SceneIR adapter + local Three.js viewer, and the
PE_CITY_ASSET_MAP_R1 two-era asset catalog + /catalog viewer (phase 2-4).
For era identity, catalog coverage classes, proxy-vs-render role and texture
provenance read [catalog-era-identity](references/catalog-era-identity.md)
BEFORE writing any catalog, container or texture-resolution code — every claim
in it is source- and scope-labeled and the reuse map at its end lists the
existing modules to reuse.

## Select sources

Read [source-locations](references/source-locations.md) to locate local
primary sources and existing client modules. Preserve SDK generation, PE era
and file identities separately. Do not load the whole SDK into context; follow
the mechanism currently needed.

## Terrain / materials / foliage (world launcher lineage, 2026-10)

For ANY terrain, terrain-texture or vegetation launcher work read
[terrain-foliage-integration](references/terrain-foliage-integration.md)
BEFORE writing code: it carries the Etap-B-verified SDK source identities
(paths + SHA256), the reuse-first module map (PESourceMount getTerrainTile/
getTerrainMaterials/resolveTexture/getVegetationClimate, the ACTIVE
TdfMaterialTailDecoder mask@56 convention — the TdfDecoder MASK16@52 constant
is STALE —, PETerrainRegion inside PETerrainCore, PEFoliageCore with NO
LAB_SEED input), the CURRENT_RUNTIME_CALIBRATION facts (u16/128, 2
units/sample, identity min/max — never historical meters/axes), the explicit
UNKNOWNs (cell-stream source, climate→region mapping, p3, materialId==
textureId NOT established, PCG special rows, 25.vcl) and the era discipline.
`serve:world` is DELIVERED (Etap C/D/E of PE_WORLD_LAUNCHER_R1_20261010; `npm run serve:world` — bounded loopback server on port 8162 with /launcher + /world and the full terrain/materials/vegetation API; the launcher and world apps are built and gate-tested in that run's package).

## Continuous world + shared height (R2 lineage, 2026-10-10, PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010)

The R2 run FIXED the WORLD LAUNCHER R1 Desktop findings (WL-1..WL-5) and
delivered the continuous world on the `codex/pe-world-continuous-r2-20261010`
branch. Reuse the R2 modules before writing new code (all gate-tested in that
run's package; per-use SDK records with SHAs in
docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010/GAMEBRYO_IMPLEMENTATION_LINKS.md):

- **SHARED HEIGHT QUERY** (contract §3.2): `src/peworld/PEHeightQuery.js` —
  PEHeightField reproduces EXACTLY the rendered-triangle planes of
  PETerrainRegion.buildGeometry (quad split (a,c,b),(b,c,d)); the 1-tile
  REAL-sample HALO resolves the 256-samples/0..510 vs generator-0..512
  boundary; missing tiles → null (never y=0, never a duplicated height);
  instance status vocabulary PLACED_ON_AVAILABLE_SURFACE /
  DEFERRED_NO_SURFACE / UNSUPPORTED_MODEL / LOD_LIMITED.
- **LATEST-REQUEST SCENE IDENTITY** (contract §3.1, the BackgroundLoad
  poll-then-attach adaptation): requestScene(origin, {forceNew}) with
  generation ids; a same-origin repeat request does NOT invalidate the
  running build (dedupe — otherwise the ~400 ms streaming tick perpetually
  supersedes in-flight rebuilds, measured); stale results abort BEFORE
  apply with disposal; coherence (terrain+textures+vegetation of the SAME
  request) is what the page calls READY.
- **FAIR CAP + FRACTIONAL DENSITY** (contract §6.2/§6.3):
  compat/world-vegetation.js fairCapQuota (largest remainder + ≥1 guarantee
  for every non-empty tile; a PURE function of per-tile counts) +
  PEFoliageLabSeed v2 (recIndex MIXED INTO the placement hash — duplicate
  model rows are SEPARATE records; fractional density floor+stable-hash
  keyed on tile/cell/record/model — NEVER the LAB_SEED, so the seed moves
  positions only while density controls counts; density=0 → exactly 0;
  monotone growth). PEFoliageCore stays byte-locked (verified per run).
- **DISTANT LOD** (contract §4, the MOUT-pattern GAP case — our own policy):
  compat/world-lod.js — mid ring (8×8-decimated REAL samples per tile over
  /api/world/lod8/<bx>/<by> blocks) + far whole-world mesh (4×4-decimated,
  census-gated /api/world/far, collected by the server's OWN census pass);
  boundary grid lines MATCH across levels (the same ORIGINAL samples on the
  cut lines — no cracks, no skirts); missing tiles are explicit holes
  (status bytes, never zero surface); preallocated index buffers + drawRange
  (no per-move allocation churn; far normals computed once — positions are
  static).
- **QUALIFIED DDS DXT1/DXT5** (contract §6.6 — the two real same-era
  formats measured on this run's inputs: 518860/518862/516807 DXT1 +
  166881 DXT5): src/pesource/DdsDecoder.js (strict magic/size/fourcc gates,
  TOP-LEVEL mip only, loud refusals; negative controls in
  world_r2_gates.test.mjs). The default profile is now FULLY textured
  (166878/166897 were the R1-untextured DDS models).
- **ASSET LAB** (contract §7): /assetlab — the PCG witness 519316 through
  the live chain (parseWitnessModel → shape→texprop→Ark slot order →
  decodeModelTextureStrict; the SIX texture names resolve to REAL same-era
  entries 518860/518862/516807/519227) + the four CD_JAN_2003 proxies
  (192374/193207/193313/193684) as CONTROLS from the PINNED Models.ark
  (SEPARATE era/cache identity; SOURCE-UNTEXTURED per the established
  catalog finding; the bounded nif41 reader runs SERVER-side — it imports
  node:fs — the browser renders the served wire).
- **REGional preview** (contract §6.4): REGIONAL_PREVIEW in
  compat/world-vegetation.js — OUR deterministic map (region = tile >> 5,
  profiles 0/2/7/19, all DECODED; version regional-preview-v1) —
  RECONSTRUCTION_PREVIEW, never a historical biome
  (ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED).

## Apply a mechanism

1. State the behavior to reproduce and its input/output identities.
2. Trace the relevant source and, when needed, its caller or sample. Record
   file/hash and actual source range.
3. Separate SDK behavior, evidence for PE use, our implementation and
   assumptions.
4. Build a control with an expectation derived independently from the
   implementation under test. Exercise the production data path.
5. Retain unresolved fields and unsafe decode boundaries as explicit
   limitations. Successful rendering does not establish source semantics or
   historical placement.

Read [integration-rules](references/integration-rules.md) before implementing
transforms, instance sharing or source→renderer mapping. Extend this skill
with compact, source-grounded mechanism notes and executed-control records as
work proceeds. Never label inventories or inherited test results as newly
executed verification.

## Executed lineage (measured, PE_935_SCENEIR_MODEL_218757_BROWSER_R1)

The whole slice below is implemented and tested in the repo (feature branch
`codex/pe-sceneir-218757-r1-20261009`); reuse it before writing new code:

- **Adapter**: `src/pecompat/` (PecNif10Reader → PecSceneIR → PecAssetAdapter →
  PecInstanceBuilder → PecRenderConvert). Version gate NIF 10.1.0.0 exactly;
  loud failure otherwise. Model 218757 = 66 blocks (62 SUPPORTED +
  2 PARTIALLY_UNDERSTOOD + 2 OPAQUE Ark blocks), 14/14 NiTriShape↔
  NiTriShapeData associations with recomputed vertex/index SHA256 fingerprints;
  9 TEXTURE_NAME_BOUND + 5 UNTEXTURED_NO_TEXPROP meshes (name/property
  bindings only — container resolution NOT_ESTABLISHED; NO nine-byte-tail
  semantics derived).
- **Composition law (verified vs NATIVE controls)**: world = parentWorld ×
  local; root world = local; point p → (R·p)·s + t. Native GB 1.2 stock-printer
  probe world bound centers (96,202,306) and (58,221,363) for
  ROTATED_SCALED_PARENT / THREE_LEVEL_SOCKET reproduced by BOTH the IR math and
  THREE.Matrix4 independently (tolerance 1e-4). NEVER flatten by summing
  positions. Reparenting does NO local compensation (measured native trait).
- **Instance contract**: resource identity (asset) is separate from runtime
  instance identity (authored instanceId). The viewer's instance WRAPPER owns
  the scene transform while the imported asset hierarchy keeps its serialized
  root/child transforms — VIEWER_INSTANCE_WRAPPER_POLICY, explicitly NOT a
  reproduction of every SDK 2.6 root-replacement branch or the original PE
  placement mechanism. Resource geometry (BufferGeometry per NiTriShapeData)
  is SHARED between instances; transforms and instance IDs are not.
- **Render conversion**: (x,z,-y)×0.01 applied EXACTLY ONCE at a render-space
  root group, labeled RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED
  (PE_AXES_AND_UNITS = UNVERIFIED_FROM_ENGINE). Serialized values never
  mutated.
- **Local viewer app**: `compat/` (zero-framework vanilla JS + three 0.185.0
  from the pinned package; importmap, no CDN) served by
  `compat/server-sceneir.mjs` — loopback-only, allowlist statics, bounded
  regenerated SceneIR API. ASSET MODE + AUTHORED SCENE MODE (two independent
  instances, AUTHOR_PLACED_LAB coordinates), OrbitControls, fit/reset,
  solid/wireframe, dPVS-name-hint heuristic visibility toggle with an honest
  imported-vs-visible ledger, full diagnostics panel (identity/coverage/
  texture status/transforms/timings), observable surface `window.__pecApp`.
- **Commands**: `npm run serve:sceneir` (server; env PORT, default 8140;
  prints `sceneir server http://127.0.0.1:<PORT>/ pid=<PID>`);
  `node tools/pecompat/extract_218757.mjs` (identity print);
  `node tools/pecompat/sceneir_dump.mjs` (bounded dump);
  `npm run test:pecompat` (unit battery T1–T6);
  `npm run test:pecompat:app` (T7 API/path-denial, T8 app-integration,
  T9 headless load).

## Version gates (measured)

- PE Models.bnt (PCG 9.3.5): 5596 NIF entries; 4838 NIF 10.1.0.0 all declare
  NiArk* (stock-only readers are corpus-proven unusable); 757 × 4.1.0.12 +
  1 × 4.0.0.2 unsupported by the current reader.
- GB 1.2.2 stock tools: REJECT PE 10.1.0.0 Ark content ("Error loading
  stream." / NiArkAnimationExtraData no-create-function). Do NOT invoke SDK
  loaders for PE assets; do not fabricate NiArk factories.
- NIF 20.5.0.4 (smallpillar.nif in the flattened Gb26 sample extraction): NO
  reader attempted; GB 1.2 tools do not support it — record, don't pretend.

## Limitations (standing)

- MODEL_218757_TO_CMO_JOIN / HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED = NO. Nothing rendered, authored or labeled in the
  viewer is a historical Eudoria position (AUTHOR_PLACED_LAB).
- Texture binding for 218757 is name/property-level ONLY; the per-entry
  9-byte Ark texture tail semantics stay UNRESOLVED (no new derivation).
- Attachment/animation/LOD execution is outside the slice; requesting
  attachment resolution surfaces an explicit UNSUPPORTED diagnostic.
- `src/pesource/NifModelReader.js` is a 457485 SINGLE-WITNESS reader — never
  widened without its witness regression.

## Output

Return implemented scope, source identities, actual controls, limitations
and the next concrete missing edge. Reuse the existing adapter/app and
decoders above before writing parallel code. Do not publish proprietary SDK
source, documents or game payloads with this skill. Skill loading conveys
guidance, not execution or publication authority.
