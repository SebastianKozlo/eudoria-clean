# BROWSER_SMOKE.md — PE_WORLD_LAUNCHER_R1_20261010 — browser evidence (honest)

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
SCOPE = what was REALLY exercised in a browser vs what was NOT (the contract §8 separation)

## 0. Status separation (DATA_VALIDATED / APP_LOAD / PIXEL_RENDER / INTERACTION_VERIFIED)

```text
DATA_VALIDATED     = CONFIRMED (independent byte reads: terrain tiles, material tails,
                     texture payloads, model payloads — bit-exact vs the served wire;
                     separate evidence: TEST_RESULTS.json + WORLD_DATA_PROVENANCE.json)
APP_LOAD           = PASS  (real headless Edge; the FIXED imported 5-conjunct gate; below)
PIXEL_RENDER       = PASS  (real headless GPU session ANGLE/Microsoft Basic Render Driver;
                     per-color proof + toggles + PNG censuses; PNGs PRIVATE ONLY)
INTERACTION_VERIFIED = NOT_PERFORMED (automation daemon port 9222 DOWN through the whole
                     run — honest status, never PASS-by-default; the open gate is §3 below)
```

## 1. LOAD gates (real browser, DOM dumps preserved)

Method: real headless Edge (`--headless=new`, dedicated temp profile) against the REAL
served pages; the FIXED imported 5-conjunct gate `evaluateLoadGate` (the same production
predicate the run's T9 suites use): EXIT_CODE_ZERO + DOM_NONEMPTY + CANVAS_PRESENT +
DIAGNOSTICS_PRESENT + STATUS_READY, with per-conjunct records.

- **/launcher** (suite server 8207 + re-verified on the STANDING server 8162): gate PASS.
  Page markers 8/8: entry button label EXACT „Uruchom podgląd świata”; era PCG_9_3_5;
  denominator 51 920; coverage line; VEGETATION_MODE = RECONSTRUCTION_PREVIEW; three-way
  separation labels; UNSUPPORTED-25 visible; no „oryginalne XYZ” claim anywhere.
  Raw: raw/WORLD/WORLD_DOM_DUMP_LAUNCHER.html (+ QC's own: 00_CONTROL_INTERNAL_QC/raw/).
- **/world#tile=53,114&profile=0&seed=0&density=50&veg=1**: gate PASS. Page markers 9/9:
  64-tile window census line; adapter-units position readout; no original-XYZ readout
  claim; raw u16 readout; the census line „zadane 2304 / wyrenderowane 2304 / ograniczone
  0 (twardy limit 5000)”; VEGETATION_MODE; profile/seed labels; p3 shown SEPARATELY;
  three-way separation lines. Raw: raw/WORLD/WORLD_DOM_DUMP_WORLD.html.
- Standing-server probe (the user-facing 8162, final code): launcher gate passed +
  entry-button label present + coverage line present; world gate passed + active-window-64
  present + raw-u16 readout present (TEST_RESULTS.json .browser.standingServerProbe).
- QC's OWN independent LOAD re-execution against the STANDING 8162: both gates re-PASSED
  (8/8 + 9/9) — 00_CONTROL_INTERNAL_QC/raw/QC_BROWSER_CHECK.json.

## 2. PIXEL_RENDER (real GPU session; PNGs PRIVATE ONLY — metadata here)

Capture method (the corrected one): CDP remote-debugging on a suite-owned free port +
`Runtime.evaluate` readiness poll on the page's OWN honest census markers +
`Page.captureScreenshot` after a real-time settle. (The LEGACY `--screenshot +
--virtual-time-budget` compositor capture starved late-boot WebGL frames — the vegetation
meshes rendered in the live buffer but were absent from the compositor capture; measured,
recorded in failedFirstRuns, method corrected in Etap E. This was a capture-method defect,
never presented as a product result.)

Honest label: **pixel-content heuristic + the U-19 per-color proof — NOT a semantic render
check and NOT interactive verification.**

### U-19 per-color revalidation (the load-bearing appearance gate; raw/WORLD/WORLD_SPLAT_PER_COLOR_U19FIX.json)

- **WORLD_U19_PER_COLOR_EXACT: PASS — 36/36** valid raycast samples over 36 distinct
  cells; every read capture pixel within the INDEPENDENTLY recomputed exact shader-math
  color span (expected colors recomputed in Node from the same wire payloads through
  PETerrainRegion/buildRegionSplatData/decodeTga2; camera pose cross-checked against the
  page's own position HUD; settled window cross-checked = 53,114).
  Mean max-channel delta **0.55/255** (max 1.39/255 — the fp32 bilinear rounding floor).
- **WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED: PASS** (negative control): the PRE-fix
  expectation (every layer samples array layer 0) does NOT match the read pixels —
  34 discriminating samples, mean max-channel delta **65.95**. A still-broken shader
  renders the pre-fix expectation and this control FAILS; it can only pass when the fix
  is real.
- **WORLD_U19_LAYER_MAPPING_CONTROL: PASS** (structural: every slot byte is a real
  texture slot 0..27; 0 bad slot bytes).
- **WORLD_U19_HEADLESS_NOT_NEAR_BLACK: PASS** (census over the two private captures):
  canvas region pre-fix **370 unique colors / lumaMean 12.2 / lumaStdDev 18.55** →
  post-fix **65,240 unique colors / lumaMean 90.67 / lumaStdDev 78.53**
  (uniqueColorsGain 64,870; lumaMeanGain 78.47). The near-black profile is GONE.

### Toggle gates (raw/WORLD/PIXEL_RENDER_U19FIX.json; final post-fix numbers)

- **ETAP_D_TEXTURE_TOGGLE_CHANGES_PIXELS: PASS** — #textures=1 vs #textures=0:
  **48.86%** of canvas pixels differ (153,375/313,900; meanAbsChannelDelta 62.43 over the
  differing; meanLumaDelta 29.03). A no-op toggle would FAIL.
- **ETAP_E_VEGETATION_TOGGLE_CHANGES_PIXELS: PASS** — #veg=1 vs #veg=0: **6.26%** of
  canvas pixels differ (19,646/313,900; meanAbsChannelDelta 58.86 over the differing;
  meanLumaDelta 3.07). The trees measurably render.
- PNG shots (5: launcher / world-on / world-off / world-veg-on / world-veg-off + the
  per-color world capture): stored ONLY under the PRIVATE root
  `D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER\`
  (U19FIX subtree + BROWSER_QC_R1 for QC's own) — path+bytes+SHA256 recorded in
  TEST_RESULTS.json / PIXEL_RENDER_U19FIX.json / 00_CONTROL_INTERNAL_QC; NEVER committed.

## 3. INTERACTION = NOT_PERFORMED (the standing open gate)

The automation daemon (port 9222) was DOWN at preflight, at QC and at persistence —
measured each time. The contract §8 interactive smoke was therefore NOT performed:

```text
OPEN GATE (interactive smoke, NOT executed here — the user or a session with a working
automation browser can run it):
  launcher -> heightmap map -> tile/region selection -> "Uruchom podgląd świata"
  -> real terrain visible -> texture toggle -> profile/seed change -> camera move / walk
  (WASD, mouse after a deliberate click, ESC frees the cursor) -> back to launcher
  -> re-enter
```

Consequences kept honest everywhere:

- `INTERACTION_VERIFIED = NOT_PERFORMED` (never PASS-by-default; the contract's §8
  acceptance line itself allows this status).
- The **interactive appearance** of the textured terrain stays **UNVERIFIED**: the
  per-color proof is a HEADLESS ANGLE/Microsoft Basic Render Driver session — real GPU
  output, but not an interactive real-GPU browser session.
- No console/network-error record from an interactive session exists; the headless LOAD
  runs carry the only stderr excerpts (Edge identity-service noise, recorded in the raw
  summaries; no page-originated errors).

## 4. Where the browser evidence lives

- raw/WORLD/ (DOM dumps + PIXEL_RENDER*.json + WORLD_SPLAT_PER_COLOR_U19FIX.json +
  WORLD_TESTS_SUMMARY.json) — committed (text/JSON only).
- 00_CONTROL_INTERNAL_QC/raw/ — QC's own browser re-executions (DOM dumps + QC browser
  check) — committed.
- Private PNGs + the private captures: 99_Audits\PE_WORLD_LAUNCHER_R1_20261010\
  (BROWSER\, BROWSER\U19FIX\, BROWSER_QC_R1\) — NEVER committed (path+SHA references only).
