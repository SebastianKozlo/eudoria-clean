# ITER-37 — The ORIGINAL-DIRECT single-model witness (decision #3 chain)

**Milestone:** M1 PE_WORLD_SURFACE_FIDELITY_R1 — ITER 051 / ledger ITER_037
**Repo:** eudoria-clean (Three.js r185, WebGLRenderer)
**Scope:** ONE model. NO corpus parser. NO witness matrix (per architect decision #3/#4: one model FIRST, the matrix after).

## The witness model (documented choice)

**457485** — one of the 10 foliage climate-0 (`0.vcl`) col0 model ids ALREADY rendered on the
foliage page (the most frequent rendered model, x20 in the ITER_033/035 census), and the SMALLEST
NIF of the 10 candidates (2,547 bytes, 16 blocks, ONE `NiTriShape` + ONE ArkTexture BASE entry —
selection census `iter037_witness_select.json`, all 10 candidates R61-parse PASS). This directly
serves the foliage page's future switch from the GENERATED_CACHE GLB fallback to original-direct
assets.

## The demonstrated chain (decision #3)

```
ORIGINAL PCG_9_3_5 Models.bnt bytes (SHA-verified at mount: C950A8C2…)
  -> PESourceMount.getModelResource(457485)      [BNT2 framing; entry 457485.nif @315,186,289, 2,547 B, crc32]
  -> NifModelReader.parseWitnessModel           [clean v10.1.0.0 NIF reader; loud failures]
  -> header: "Gamebryo File Format, Version 10.1.0.0" (0x0A010000), 16 blocks
  -> NiNode "Scene Root" -> NiNode "default624" -> NiTriShape "default624:0"
  -> NiTriShapeData: 16 vertices / 8 triangles / 2 UV sets / normals / vertex colors (bit-exact)
  -> NiTexturingProperty BASE slot: clamp=3, filter=2, uv_set=0, source=-1
  -> NiArkTextureExtraData "default624_0_BASE" (ref=4): the ERA texture binding —
     trailing 9 bytes = [0x00][0xFFFFFFFF][u32 LE textureId] -> 457490
  -> PESourceMount.resolveTexture(457490, PCG_9_3_5:Textures.bnt)   [era-explicit]
  -> Textures.bnt entry 457490.dat @389,949,379, 262,188 B (SHA-verified container)
  -> TgaDecoder.decodeTga2A32Image: TGA 2.0, 256x256, 32bpp BGRA -> RGBA (image order)
  -> THREE.DataTexture (flipY=false, colorSpace=NoColorSpace) + MeshBasicMaterial
     (vertex-shaded: texture x vertex colors; alphaTest 111/255 from NiAlphaProperty)
  -> deterministic render 381A80C4795450D8B532B122FABC7684FC369BBDC82BE26FBB92952800EF5318
```

## The loud finding: the era texture binding is the ARK system, not NiSourceTexture

The NEXT_PROMPT's expected chain listed `NiSourceTexture`. The census found **NONE of the 10
foliage climate-0 candidates contains a NiSourceTexture block** — in this era the base texture
binds via the PE-specific `NiArkTextureExtraData` (entry -> ref to the NiTexturingProperty block;
the trailing 9 bytes carry the Textures.bnt entry id; the NiTexturingProperty BASE slot has
`source = -1` NULL). The reader implements the Ark binding path (the canon rule CONFIRMED on
347937 + all 21 ArkTextures, `nif_parser_v2`); the NiSourceTexture parser is NOT implemented
because it is absent from the witness chain — recorded loudly, never silently assumed.

## Anti-circular cross-validation (the ITER 049/050 method)

- **Oracle:** the frozen R61 python parser (PE_R61_FROZEN_BASELINE_20260828, READ-ONLY import)
  extracted the SAME model INDEPENDENTLY from the ORIGINAL Models.bnt bytes
  (`iter037_oracle_extract.json`): 16/16 blocks, geometry/UV/vertex-color arrays as file-order
  f32 byte hex, the Ark texture id decoded from the raw trailing bytes, the texture payload
  decoded by its own manual TGA decode.
- **Page:** the clean JS reader (`src/pesource/NifModelReader.js`) derived everything from the
  NIF bytes itself in the browser; the oracle JSON was NEVER an input to the page.
- **Crosscheck** (`iter037_crosscheck.json`): deep structural compare — **575 leaves, 281
  float-hex bit patterns, 16/16 blocks, 0 mismatches -> PASS**, including the byte-level
  identity of the mounted payload (SHA 72479A7F…), the texture entry (offset/size), the texture
  payload SHA, and the decoded RGBA IMAGE-ORDER SHA (D34BCFD6… — the python manual decode ==
  decodeTga2A32Image, byte-exact).

## Determinism + visibility (anti-success-theater)

- 3/3 fresh headless loads: identical in-page render hashes AND byte-identical screenshots
  (`381A80C4…` / PNG SHA `EC7791BB…`), in-page double-render deterministic.
- `?model-off` negative control: `2084DB5A…` DIFFERS from the model-on hash — the model
  demonstrably contributes pixels.
- Regression sweep 5/5 MATCH: heights `50BD7F9E…`, materials `5F4677E6…`, materials_confirmed
  `EA4411B5…` (proves the TgaDecoder A32 refactor behavior-identical), water `D7C13F1F…`,
  foliage `8770AAA0…` — zero deltas.

## UV orientation (r185 calibration-gate E discipline)

Convention: **NIF uv used RAW (no V flip); texture rows top-first (image order);
DataTexture flipY=false -> v=0 samples the image TOP.**
Evidence: (1) the legacy UVConv v1 byte-probe (runtime_flipY_probe.json, the r169 deployed
runtime: v=0 samples the image top with flipY=false upload); (2) the witness model's own
structure — card top vertices carry v≈0.104, card bottom v≈0.940 (v increases DOWNWARD along
the height axis), the dark ground-shadow vertex colors sit at z=0; (3) the texture's alpha
structure (top-half mean 27.2, bottom-half 66.8 — sparse top, dense base). A D3D8 runtime
capture can falsify this — documented choice, no historical-truth overclaim.

## Honest bounds (labeled on the page + in the result JSON)

- `[P-UNITS]` NIF cm -> render m x0.01 (the era m->cm x100 evidence, FUN_0082b790).
- `[P-AXIS]` NIF Z-up -> Three Y-up via (x, z, -y) — the legacy-exporter-documented mapping
  (nif_glb_exporter_uvc_v1); the engine's own NIF->world transform for vegetation models is
  NOT decompiled (iter032 bound 5) — CURRENT_RUNTIME_CALIBRATION.
- `[P-UV]` see above — documented choice.
- `[P-MATERIAL]` fixed MeshBasicMaterial (vertex-shaded — the era technique 'Vegetation' = FX
  0x3EC is vertex-shaded, and the model's own NiArkShaderExtraData carries "effectfile
  Vegetation, CullMethod 2, AlphaTreshold 111, EnableAnimation 1.0, ModelAmpPlanar 5.0,
  ModelAmpHeight 5.0, ModelFreqScale 2.86" verbatim); DoubleSide (CullMethod 2's exact D3D8
  mapping UNVERIFIED); no wind animation — CURRENT_RUNTIME_CALIBRATION.
- `[P-MIPS]` filter=2 (trilinear enum) rendered as LinearFilter + mip generation OFF
  (deterministic subset) — CURRENT_RUNTIME_CALIBRATION.
- `FILE-TAIL` 8 bytes after the last NIF block (`0100000000000000`) — recorded raw, semantics
  UNKNOWN (labeled, not interpreted).

## New/changed repo files

- `src/pesource/NifModelReader.js` (NEW) — the clean minimal v10.1.0.0 NIF reader (ONE-MODEL
  scope; unknown block type = LOUD FAIL — the R61 fail-closed parity; partial Ark blocks carry
  their boundary method + raw bytes, never silent).
- `src/pesource/PESourceMount.js` — `getModelResource({era, modelId})` (BNT2 framing via
  Bnt2Archive; NOT_FOUND loud; provenance on the result).
- `src/pesource/PEProvenance.js` — KNOWN_HASHES + `PCG_9_3_5:Models/Models.bnt` (C950A8C2…).
- `src/pesource/TgaDecoder.js` — `decodeTga2A32Image()` (image-order A32; the A32 logic shared
  via one raw core — the palette path behavior-identical, regression-proven).
- `terrain/model_witness.html` + `terrain/model_witness.js` (NEW) — the witness page
  (era + provenance labeled; `?model-off` audit variant).

## Next steps BEFORE the witness matrix (NOT executed this iteration)

1. The v4 model path (NIF 4.1.0.12/4.0.0.2 — inline RTTI, 4-byte booleans for 4.0.0.2, the
   hasUv field) era-validated on a v4 witness; then the v10 known-good/mild/severe classes.
2. The scrambled-texture FALSIFICATION set (the U1 census SEVERE cases, e.g. peobj_11708 /
   173464 / 423020 / 505591) through the SAME reader — the decision-#3 falsification target.
3. The character/clothing class witness (matrix member).
4. The foliage page switch: the 10 climate-0 col0 ids from the GLB cache to original-direct
   (the witness page is the comparison bed; the legacy GLB stays the regression oracle).
5. The engine's NIF->world transform (the visualizer path, iter032 bound 5) to close [P-AXIS].
