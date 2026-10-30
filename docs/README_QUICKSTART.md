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
| `http://127.0.0.1:8140/terrain/world_iso.html` | ISO terrain patch (3×3 tiles) with material splat + environment layers |
| `http://127.0.0.1:8140/terrain/inspector.html` | NIF model inspector (block graph / TRS / materials / 3D viewport) |

Inspector accepts query params: `?asset=<name>&era=<era>`.
Examples: `?asset=457485&source=models_bnt` (full original-direct chain), or a fixture
name routed via `/assets/…`.

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

Console hooks: `__w05SetMaterialMode`, `__w14SetEnv`, `__w14EnvStats` (used by the
browser-proof probes).

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
