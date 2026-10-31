# WORLD_PIPELINE — Eudoria continuous terrain world (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031 · 2026-10-31.
End-to-end pipeline from the game's own containers to rendered pixels. No 2003-era (ISO/PE42) sources are used anywhere in this chain.

## 1. Versioning (which build serves which Three)

| Runtime | URL | Three | Code root |
|---|---|---|---|
| LIVE 8163 (production baseline, never restarted during the campaign) | http://127.0.0.1:8163/world | **0.185.0** | pe-world-continuous-r2 worktree (BASE, read-only) |
| Staging 8171 (this campaign's NEW_WORK) | http://127.0.0.1:8171/world | **0.187.0** (exact pin + lockfile, fail-closed verify `threePinnedVersion`) | pe-world-8163-biome-player-r1 (this worktree) |

Both serve the same PCG_9_3_5 data and the same world semantics; pixel-diff fa (ground close walk) = 0.00/0% between them — the terrain/material/vegetation core is bit-stable across the r185→r187 upgrade (f0/fc/fd wider-view diffs are explained COMBINED_CHANGE: LOD/horizon + async capture state, see TROUBLESHOOTING).

## 2. Data chain (per-tile, all from PCG_9_3_5 `pcg_install` containers)

```
terrain.bnt (PESourceMount, SHA 95841761… pinned fail-closed)
  → GET /api/world/tile/<gx>/<gy>          — TDF record: 32x32 uint16 height samples, 2 m/sample
  → GET /api/world/tile/<gx>/<gy>/materials — TDF material tail: mask@record+56 (RAW u8 or RLE count,value),
                                              material id@+16, 16x16 = 256 B mask per layer
  → client fetchTile/fetchMaterials (LRU 512, identity refusal on era/SHA change)
  → buildRegionSplatData: base64→bytes strict len 256, exact-dup dedupe,
     resolved slot (cap 48), RAW weights — NO normalization
  → decodeTga2 (strict TGA2 24bpp) → RGBA → LRU 64 → DataArrayTexture (GPU upload)
  → sampler: 128x128 nearest DataTexture per region; SPLAT_FRAG:
     sequential lerp mask/255 in RECORD ORDER, worldUV = worldPos.xz/32 m
  → pixel
```

**Cell size = 4.0 m**: tile = TILE_M 64 m (32 samples × 2 m), mask = 16×16 cells → 64/16 = 4.0 m per mask cell (2×2 height samples). This matches `MATERIAL_CELL_M=4`. The visible ~4 m blockiness of the splat masks is **FAITHFUL source resolution**, not a rendering defect — the source stores one u8 weight per 4 m cell, often RLE-constant; smoothing it would be an invention.

## 3. Render: near / mid / far

- **near**: 8×8 tile window around focus, full material splat, 2.03 M triangles, 583 material layers resolved in the home window (0 missing, 0 decode failures, 0 fetch errors).
- **mid/far LOD**: measured denominator 51,920 tiles (regular census 51,920/51,920 on the pinned terrain.bnt); LOD built asynchronously — the far census is PENDING right after start/teleport and becomes READY seconds later (see TROUBLESHOOTING).
- **height query**: shared triangle-exact `queryHeightAtWorld` (PEHeightField) used by camera, foliage and the player alike.

## 4. Run it (see QUICKSTART.md)

- LIVE: `http://127.0.0.1:8163/world` (BASE worktree `compat/server-world.mjs`).
- Staging: from this worktree `node compat/server-world-r187.mjs` with `PEWORLD_PORT` (campaign lease used 8171); requires `npm install` (three 0.187.0 exact pin).

## Sources (file + SHA256)

- terrain.bnt pinned by PESourceMount, SHA256 95841761… (fail-closed, see `/api/world/status`).
- MATERIAL_CHAIN_TRACE.md, MATERIAL_CHAIN_COUNTS.json, W1-3/MASK_RESOLUTION_EVIDENCE.json, W1-2/GATE_RESULTS.json — campaign SCI (99_Audits/PE_WORLD_8163_..._6H_R1_20261031/W1_TERRAIN_MATERIALS/).
- QC_ROLLING_R1/QC_REPORT.md (SHA256 76F2DB60CB88EE2363840A3C18D188D4EACD1CAF655083F1291495D351574ED8) — independent re-derivation of counts 583/105/583.
