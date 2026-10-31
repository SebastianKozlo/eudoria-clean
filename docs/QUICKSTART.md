# QUICKSTART — run the world (LIVE 8163 / staging 8171)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031. Windows, Node.js ≥ 20.

## A. LIVE production (read-only baseline, three 0.185.0)

The LIVE server should already be running (PID recorded in the campaign RECEIPT; it was never restarted during the campaign):

```
http://127.0.0.1:8163/launcher   # era/source badge page
http://127.0.0.1:8163/world       # continuous textured world
http://127.0.0.1:8163/assetlab   # asset viewer
http://127.0.0.1:8163/api/world/status   # era + container SHAs + three version
```

If you must start it yourself (only with ownership — never kill a foreign PID):
`node compat/server-world.mjs` in the BASE worktree `D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2` with the campaign-agreed port env; stop scripts must be identity-checked (PID + exe + creation time), never a bare `Stop-Process -Id`.

## B. Staging NEW_WORK (this worktree, three 0.187.0 exact pin + player)

```powershell
cd D:\Eudoria_Reconstruction\12_WebGame\pe-world-8163-biome-player-r1
npm install                        # three@0.187.0 exact pin + lockfile
$env:PEWORLD_PORT = 8171           # free loopback port; server verifies pin fail-closed
node compat/server-world-r187.mjs
# console line: staging lease; /api/world/status reports three 0.187.0 + pinned node_modules root
```

Open `http://127.0.0.1:8171/world`.

## C. Player mode (staging only)

1. In `/world`, the GAME_CHARACTER_REF (textured, skinned, 2 m) spawns at the camera focus.
2. Click the page to get pointer lock / focus (in a normal browser; headless runs skip this — see TROUBLESHOOTING).
3. **WASD** — move; the character yaws to the movement direction; idle↔walk switches on input speed (threshold 0.2, crossfade 0.25 s — ENGINEERING runtime policy).
4. Mouse drag — orbit the 3rd-person camera around the character (cooperating OrbitControls: `controls.target = character`).
5. Debug handles (console): `window.__pePlayer` (activeClip, bindReport: world bbox 1.78×2.00×1.76 m), `window.__peR2Debug.queryHeightAt` (shared height query), `window.__peR2Debug.windowOrigin` (current tile window).

## D. What to expect on the first frame

Detail of the ground near spawn is immediate (near window 8×8, 583 material layers, vegetation), while mid/far LOD is **PENDING for a few seconds after start or teleport** — the horizon completes after the async LOD build. That is expected asynchronous streaming, not a defect (see TROUBLESHOOTING).

## Sources

- compat/server-world-r187.mjs (allowlist + staging pin; worktree), package.json (`"three": "0.187.0"`).
- STAGING_LEASE.md — SCI W1_TERRAIN_MATERIALS\W1-2\ (port 8171 lease, PID).
- W4_REPORT.md §4–5 — SCI W4_ANIMATIONS\ (player mode, gates G1–G5).
