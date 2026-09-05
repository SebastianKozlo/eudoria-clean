# iter033 — Clean-runtime foliage wiring (M1 ITER_047, Gate C)

Date: 2026-09-04 (session slot 15:15). Ledger: `ITER_033` (M1_LEDGER.md).
P0: does the clean runtime deterministically GENERATE and RENDER foliage
instances per the CONFIRMED iter032 algorithm over the proven region, with the
era-bounded choices explicit and every stage byte-anchored to the RE evidence?

**Verdict: P0 PASS** (all five PASS-gate items closed; see the session report
and `iter033_manifest.json` in the M1 audit tree).

## What landed (this repo)

- `src/pesource/VegetationClimateDecoder.js` — the canonical `.vcl` TSV decoder
  (FUN_0083a7d0 semantics: a flat 12-value numeric token stream, 12 values per
  record = the engine's 0x30/48-byte row; loud failures, no silent skips).
- `PESourceMount.getVegetationClimate({ era, climateIndex })` — the Gate C
  mount interface, implemented: ORIGINAL VegetationClimates.bnt (BNT2 framing,
  32 entries, SHA-pinned 7B858401...) -> canonical records + provenance.
- `src/peworld/PEFoliageCore.js` — the CONFIRMED instance generator, every
  stage address-cited: the subdivision switch (FUN_0098fe00: level 0..4 ->
  step 1/2/4/8/16; the spawn-loop default = level 1 from FUN_0095b180's
  settings+4), the {u16 x, u16 y, u32 model_id} triples (FUN_00990810 layout),
  the position-keyed RNG (FUN_0098cdf0 seed `((p4*16+p5)*16+p1+p2+p3)*0x5CC7
  +0x6D7`, `state = x*8^x`; FUN_0098ce30 MSVC rand() `*0x343FD+0x269EC3`,
  `>>16 &0x7FFF`), the sampler lerp (FUN_0095ac30, per-model min/max), and the
  spawn fields (FUN_0095b180: `pos = u16/K`, `scale = |lerp*2.0|`, model id
  bind; rotation = identity, RE-faithful — the spawn loop sets position +
  scale + model id only).
- `terrain/foliage_system.html` + `.js` — the foliage page: the proven 9-tile
  region (grid 56..58 x 112..114, the P0 region) rendered through the clean
  chain + the generated instances standing on it (heights bilinear-sampled
  from the SAME canonical region tiles). `?foliage-off` = the audit variant
  (hides only the instance group before the single deterministic render).
- `assets/foliage_glb/` — the GENERATED_CACHE model cache (10 GLBs = the
  distinct col0 ids of climate 0 + MANIFEST.json with per-file SHA256; the
  page verifies every loaded GLB against the manifest — loud NOT_FOUND, no
  silent fallback). The clean pesource NIF path (a JS NIF parser over
  Models.bnt) remains the preferred future path.

## Era-bounded placeholders (ALL labeled in code + page legend)

- `[P-CLIMATE]` climate index 0 (0.vcl) — the per-location climate input is
  PLAUSIBLE-UNVERIFIED (the shared-selector hypothesis, iter032); documented
  choice following the constant-byte-0 convention of the terrain material page.
- `[P-CELLSTREAM]` the per-cell record CONTENT (positions/model selection/
  counts = `max(0, round(col1))` per record per sub-cell) — a local
  deterministic stand-in; the historical cell byte-stream origin is NOT closed
  (iter032 bound 3). The record FORMAT and the spawn semantics are CONFIRMED.
- `[P-RNG-DIV]` `32768.0` (the `_DAT_00a7d7a8` runtime divisor candidate).
- `[P-RNG-P3]` `0` (the `*(impl+0x24)` seed input UNVERIFIED); p2 = the view
  band 10 (STRONGLY_SUPPORTED: the +0x2c 10/20/30 field pattern).
- `[P-POS-SCALE]` `2.0` (the `_DAT_00a8c758` u16->world divisor; the u16 space
  then covers 65,536 half-units, admitting the historical client coordinates).
- `[P-SCALE-FIELDS]` lerp min/max = VCL col2/col3 (census min/max reading;
  field-level direction STRONGLY_SUPPORTED).
- `[P-WINDOW]` the generation window = the proven region (the historical grid
  extents are settings-scaled, not statically pinneable).
- `[P-UNITS]` the GLB cache preserves NIF centimeters; render bridge 0.01
  (the m->cm x100 evidence: FUN_0082b790).
- `[P-MATERIALS]` FX technique 0x3EC ("Vegetation", vertex-shaded,
  materials.vfs, both eras) INFORMS the lighting only; per-model materials =
  the GENERATED_CACHE GLBs; fixed deterministic lights.

## Measured results (the audit evidence, prefix iter033_*)

- 76 instances generated over 4 sub-cells (level 1 -> step 2) from the 12
  climate-0 records; 4 distinct models instantiated; 28 record-per-cell
  counts of 0 recorded honestly (density < 0.5 under the era-bounded
  mapping); 0 NOT_FOUND models; region heights 16.3..487.3 m; the
  elevation-band diagnostic measured WITHOUT filtering (62 within / 14
  outside — the filter semantics are UNVERIFIED, so the census measures
  instead of assuming).
- RNG cross-check: an INDEPENDENT python implementation (written from the
  Ghidra decompiles, not from the JS) recomputes ALL 76 instances — EXACT
  agreement (state0, samplerValue, scale), 0 mismatches.
- Determinism: identical render sha256 `A79CB65C1852E8893E1346905D2F29BCBA
  C0C076D3EA6491AC1E2A7BDD92929F` across 5 fresh page loads (raw-CDP headless
  Chromium; the Playwright MCP tooling failed loudly — the documented
  fallback route). Visibility proof: the `?foliage-off` variant renders a
  DIFFERENT stable hash (`A3339D4A...`) — the instances contribute pixels;
  the render is never terrain-only.
