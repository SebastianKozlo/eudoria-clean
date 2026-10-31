# README_QUICKSTART — pe2003-world (ISO 5.1.0.0 reconstruction preview)

This is a **documentation-honest** reconstruction runtime: it renders recovered Project
Entropia (PE 5.1.0.0, "PC Gamer Nov 2003" ISO era) data through the Rosetta pipeline.
Everything you see on screen is labelled with its evidence mode — nothing is presented as
"the original game" unless it was actually recovered from era data. See
`CAPABILITY_MATRIX.json` for what is implemented vs. knowledge-only.

## Prerequisites

- **Node.js** v22+ (tested on v22.22.0)
- **The recovered ISO-era terrain archive** (`50.bnt`, PE 5.1.0.0):
  - Size: 118,016,977 bytes
  - SHA256: `A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00`
  - Place it anywhere readable and point the server route at it (step 2).
  - The hash is **verified at mount boundary** — a mismatched file is refused, by design.
- **(Optional, REFERENCE mode only)** the CD Jan-2003 `Textures.ark`
  (SHA256 `D611D1257D2E5433B6DF218D671AA60D003C5C6587858757C7AF3219BB739B80`).
  The ISO corpus ships **no texture container** (documented missing edge), so material
  textures are joined in REFERENCE mode from this archive. Without it you still get the
  diagnostic-color terrain.

## 1. Install

```bash
npm install
```

Installs `three` (pinned exact, currently **0.187.0 / r187**). No other runtime
dependencies.

## 2. Configure the data route

`server.mjs` serves data files through an exact-path allowlist (`EXACT_ROUTES`). Point
the `/iso/50.bnt` route at your copy:

```js
const EXACT_ROUTES = {
  '/iso/50.bnt': '<PE2003_DATA_DIR>/recovered/50.bnt',
  // '/assets/<NAME>': '<PE2003_DATA_DIR>/<NAME>',   // optional NIF fixtures
};
```

Replace `<PE2003_DATA_DIR>` with the directory holding your recovered files. Routes are
loopback-only (127.0.0.1) and traversal-safe.

## 3. Run

```bash
node server.mjs
```

- Default port **8140** (env `PORT` overrides); falls back to **8141** if occupied.
- The chosen port/PID is written to a lease file (`server lease`), including the stop
  command.

## 4. Open

| URL | What it is |
|---|---|
| `http://127.0.0.1:8140/terrain/world_iso.html` | ISO terrain with **explore window (W25)**: a Chebyshev radius-2 (5×5) tile window follows the camera grid cell, replanned on every cell change; streamed-tile cache limit 40 with farthest-from-camera eviction; HUD shows the live camera grid position (x,y), window range vs the 220×236 map, cache size/limit and eviction count. Material splat + environment layers; frustum culling on by default — KeyC toggles |
| `http://127.0.0.1:8140/terrain/inspector.html` | NIF model inspector (block graph / TRS / materials / 3D viewport) |
| `http://127.0.0.1:8140/terrain/character_preview.html` | 2003 avatar preview (REFERENCE asset stage): real avatar 208861 + hair meshes 32498 (MALE) / 32509 (FEMALE) with era textures — gender pairing **byte-proven** (CHAR_G slot-45 GetSex 1=MALE/2=FEMALE + 6052 gender tables; W25 re-paired the previously crossed textures: 32498+216257 MALE, 32509+216302 FEMALE) — **read-only engineering preview, NOT a playable creator** (see `CHARACTER_CREATION.md` for what is/isn't recovered) |

Inspector accepts query params: `?asset=<name>&era=<era>`.
Examples: `?asset=457485&source=models_bnt` (full original-direct chain), or a fixture
name routed via `/assets/…`.

**Data routes are env-supplied** (`server.mjs` reads its exact-path allowlist at
startup; the file itself needs no edits — restart the server after changing routes).
The character preview needs the avatar/hair payload routes from the W18 lease
(`/assets/avatar/…`, `/assets/hair/…`) plus the existing `/iso/50.bnt` route; point
every entry at your own local copies of the recovered files (placeholder example
above — **no absolute paths are prescribed here**).

## 5. Controls (world_iso)

| Input | Action |
|---|---|
| **W A S D** | move |
| **mouse drag** | look |
| **R / F** | up / down |
| **Shift** | ×3 speed |
| **M** (KeyM) | material mode toggle: splat ↔ diagnostic flat-color |
| **N** (KeyN) | sky layer on/off |
| **B** (KeyB) | fog layer on/off |
| **L** (KeyL) | light layer on/off |
| **C** (KeyC) | frustum culling on/off (W22; HUD shows the live culled-tile count) |

Console hooks: `__w05SetMaterialMode`, `__w14SetEnv`, `__w14EnvStats` (used by the
browser-proof probes), plus W22: `__w22SetCulling`, `__w22Stats`,
`__w22StartPerf`/`__w22StopPerf`, `__w22SetOrbit`.

## 5b. Controls (character_preview)

OrbitControls **drag = rotate, wheel = zoom**; per-hair toggle buttons show/hide each
hair mesh. The panel is read-only knowledge (labels + statuses) — there are
deliberately **no sliders** (0 input/range elements, DOM-gated).

## 6. Stop the server

Use the stop command from the lease file, or:

```powershell
Get-Process node | Where-Object { $_.Id -eq <PID-from-lease> } | Stop-Process
```

## The three evidence modes (read this before trusting what you see)

| Mode | Meaning | Used for |
|---|---|---|
| **STRICT_ISO** | Bytes decoded from the verified ISO-era `50.bnt`, rendered as-is (seams/zero-tiles kept as ORIGINAL DATA) | terrain heights, tile grid, material tail masks |
| **REFERENCE** | Data from a *different but documented* source, joined by proven id; explicitly **not** ISO truth | material textures (CD Jan-2003 `Textures.ark`, 12/12 TexIDs) |
| **ENGINEERING_PREVIEW** | Made-up-but-explicit preview values so the scene is readable; **no** recovered original behind them | sky gradient, fog values, light params |

The on-screen badge and HUD state the mode per layer. If a claim is not on the HUD, it is
not claimed. Details: `FORMAT_SUPPORT.md`, `ENVIRONMENT.md`, `NIF_BINDINGS.md`,
`CHARACTER_CREATION.md`, `TROUBLESHOOTING.md`.
