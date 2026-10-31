# TROUBLESHOOTING — known states and how to read them (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031. Every item below was physically reproduced and root-caused in W1/W4 (see ROOT_CAUSE in the SCI seal package).

## 1. Far census PENDING right after start / teleport

- Symptom: after READY of the near window (or a teleport), the far LOD census still shows PENDING; the horizon is missing in the first frame(s).
- Cause: mid/far LOD builds are asynchronous; a full far-window rebuild without cache hits takes seconds.
- Correct reading: NOT a defect. Wait for far READY (f0 baseline: 80.5% flat first frame → after settle fc flatFrac 0.36, far READY, 1.61 M tris). A spawn re-frame proposal (camera mid-height + HUD-first) exists but is deliberately NOT implemented (would invalidate campaign baselines; needs MASTER sign-off).

## 2. Pointer-lock in headless / automation

- Headless Edge+CDP gate runs never take pointer lock; player input (WASD) is injected as key events instead. If you drive the page from automation, don't expect lock state — use the debug handles (`__pePlayer.activeClip`) to assert state.

## 3. fb tool choreography (camera under terrain at top-down)

- Symptom: the fb (top-down multi-tile) capture frame looked like an untextured dark flat scene.
- Root cause (measured, FB_ROOT_CAUSE.md): the capture tool's camera ended at y=641.5 m vs walk-eye surface ≈716 m — the camera was **~73 m UNDER the terrain** at capture time (fog excluded, drawcalls=2, clear color 0x0c1018). It was a **tool capture defect, not a product defect**; the corrected choreography (fb2, drag +220) yields cam y=705.4 m and a fully textured terrain PNG (889,031 B).
- How to frame it: "capture tooling camera-under-terrain defect; product verified by corrected fb2 + identical fa pixel diff". Never quote the bad fb as a render regression.

## 4. Stale diagnostic panels (fixed in staging)

- world-evidence / world-census panels used to show the OLD window after a move/teleport (583/583 vs 959/959 mismatch). FIXED in NEW_WORK: `updateCensusPanel()` now also refreshes `updateEvidencePanel()`. If you see evidence/census disagreeing on an old worktree — it is the pre-fix BASE behavior; the scene itself was coherent (coherence GOTOWA).

## 5. LRU re-fetch on return (fixed in staging)

- Returning to a visited window used to re-fetch ~100 tiles despite LRU 512 (identityOf wiped by status refresh + dead LRU duplicates). FIXED: `refreshWorldStatus()` re-derives identityOf; `cachePut()` keeps the order queue a bijection of the cache. Post-fix gate: terrain re-fetch delta 0 (pre-fix historical negative control: +100). CAM-C3 identity refusal on real era/SHA change is still active — one full re-fetch after a source change is CORRECT behavior.

## 6. Mask blockiness ~4 m

- Not a bug: 4.0 m = TILE_M 64 / 16 mask cells — FAITHFUL source resolution (u8 per cell, often RLE-constant). Do not "fix" by smoothing (would be ENGINEERING invention without source proof).

## 7. f0/fc/fd pixel diffs between LIVE r185 and staging r187

- fa (ground close) = 0.00/0% and fb = 0.01/0% — the core stack is bit-stable. The f0 9.23/50.8% diff is COMBINED_CHANGE (wider-view LOD/horizon + async capture state), NOT render non-determinism: the staging f0 noise control is 3× byte-identical (SHA 842FDBFF…C6F474; diff 0.00/0% persisted in F0_NOISE_CONTROL_RESULT.json).

## 8. Idle loop seam

- The idle clip (546617) is NOT perfectly cyclic (first/last key delta 0.6006 — OBSERVED in source data). A small seam at the loop wrap is honest source behavior; walk (546613) is seamless (0.0). Do not "repair" the seam by synthesizing keys.

## 9. Vegetation absent in fb/teleport frames

- Vegetation rebuilds asynchronously after window changes — NOT_OBSERVED ≠ absent. Drawcalls 2 in fb was partly this. Wait for the veg drain (latest-request ownership) before census.

## Sources

- FB_ROOT_CAUSE.md, GATE_RESULTS.json, PIXEL_DIFF.json, F0_NOISE_CONTROL_RESULT.json — SCI W1_TERRAIN_MATERIALS\W1-2\.
- W1-3_REPORT.md — SCI W1_TERRAIN_MATERIALS\W1-3\ (mask blockiness verdict FAITHFUL).
- W4_REPORT.md — SCI W4_ANIMATIONS\ (idle seam, gates).
- QC_ROLLING_R1/QC_REPORT.md — SHA256 76F2DB60CB88EE2363840A3C18D188D4EACD1CAF655083F1291495D351574ED8.
