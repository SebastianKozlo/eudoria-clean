# MATERIAL_BINDINGS — how a terrain pixel gets its textures (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.

## 1. The measured, countable chain (W1-1, LIVE 8163)

Every stage of the binding chain is counted separately in a live frame; missing is never masked by a one-color fallback:

| Stage | home window (50,111) | after move (59,120) | far (176,36) | return home |
|---|---|---|---|---|
| expected layers (server) | **583** | (server census not collected — open item) | **105** | **583** |
| resolved (server `texture.resolved`) | **583** | — | **105** | **583** |
| missing (binding/fetch) | **0** | **0** | **0** | **0** |
| client splat resolved/total | 583/583 | 959/959 | 959/959 | 959/959 |
| decoded RGBA (LRU 64) | 23 | 47–48 | 47 | 47 |
| fetch materials (errors) | 128 (0) | 192 (0) | 192 (0) | 192 (0) |
| fetch textures (errors) | 42 (0) | 74 (0) | 74 (0) | 74 (0) |

`missingDetail` in MATERIAL_CHAIN_COUNTS.json is an **empty list** — no tileID-based missing entries exist for the active window. The 12/12 material fixture is only a fixture: full-region counters above are the real coverage statement (see MATERIAL_COVERAGE in the SCI seal package).

## 2. Slot policy — first resolvable slot = RENDER_RECONSTRUCTION

- For each (tile, layer) the server enumerates candidate texture entries; the client takes the **first slot that resolves to a real Textures.bnt member** (`r.texture.resolved === true`, cap 48 slots per region).
- This is a **RENDER_RECONSTRUCTION decision**: which slot the original 9.3.5 client bound per layer is **UNRESOLVED** — the slot-binding evidence (the RE link) is still open (see FIRST_MISSING_EDGE: texture-slot = RE 9.3.5). We render with the first resolvable slot and do not claim it is the historical choice.
- Weights are bound **RAW** (no normalization); blend is sequential lerp in record order inside SPLAT_FRAG; sampler is nearest-filtered 128×128 (per 4.0 m mask cell — the source resolution).

## 3. Fix history (W1-2, staging 8171, three 0.187.0)

- Stale diag panel (`world-evidence`/`world-census`) after window change — FIXED: `updateCensusPanel()` now also calls `updateEvidencePanel()`; gate teleport 180,40 → panel origin 176,36 == state windowOrigin PASS; evidence vs census 583==583 PASS.
- LRU identity-refusal (return re-fetched ~100 tiles despite LRU 512) — FIXED: `refreshWorldStatus()` re-derives `identityOf`, `cachePut()` removes dead duplicates from the LRU order queue; gate terrain re-fetch delta = **0** (historical negative control pre-fix: +100).
- Both fixes verified with headless Edge+CDP gates (GATE_RESULTS.json); LIVE 8163 was never touched.

## 4. Change a material/texture source (end-to-end example)

1. The era pin is fail-closed: `PESourceMount` refuses to serve any container whose SHA256 differs from the pin (check `http://127.0.0.1:8171/api/world/status` → `identity.era/sha256`).
2. To point the world at a different era's Textures.bnt you must change the pin AND the era label together — a relabel without a pin change is forbidden and will not boot.
3. After any source change, the client cache refuses old entries (identity refusal) — expect one full re-fetch of the visible window; watch `world-census` panel for resolved==expected and missing==0.

## Sources (file + SHA256)

- MATERIAL_CHAIN_COUNTS.json / MATERIAL_CHAIN_TRACE.md / W1-2 GATE_RESULTS.json / W1-3 MASK_RESOLUTION_EVIDENCE.json — campaign SCI W1_TERRAIN_MATERIALS\ (raw evidence trees).
- QC_ROLLING_R1/QC_REPORT.md — SHA256 76F2DB60CB88EE2363840A3C18D188D4EACD1CAF655083F1291495D351574ED8 — re-derivation 583/583, 105, 0 missing confirmed.
