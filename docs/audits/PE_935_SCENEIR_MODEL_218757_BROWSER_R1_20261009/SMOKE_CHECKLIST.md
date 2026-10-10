# SMOKE_CHECKLIST — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Full interactive verification checklist for PE-MASTER (real automation
browser, AFTER this phase). Start the app first:

```
cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1
npm run serve:sceneir        # default port 8140; prints: sceneir server http://127.0.0.1:8140/ pid=<PID>
```

App URL: **http://127.0.0.1:8140/**

Stop at the end: terminate the printed PID (`Stop-Process -Id <PID>`); verify
the port is freed (rebind probe). Do NOT leave the server running.

Observable surface: `window.__pecApp` (see `compat/app.js`) and the
diagnostics root `#diagnostics[data-load-status]`. Every step below names the
exact expected observable. A step FAILS if the observable does not change as
described — record honestly either way.

## 0. Boot + honest panels

| # | Interaction | Expected observable outcome |
|---|---|---|
| 0.1 | Load `http://127.0.0.1:8140/` | `__pecApp.boot === 'ready'`; `#diagnostics[data-load-status="READY"]`; no `#error-banner` content (hidden). |
| 0.2 | Diagnostics: identity | `#diag-identity` shows era `PCG_9_3_5`, container `Models/Models.bnt`, entry `218757.nif`, payload SHA256 `3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36`, and `pin verified: YES (fail-closed client check)`. |
| 0.3 | Diagnostics: coverage | `#diag-blocks` shows `blocks 66 = 62 supported + 2 PARTIALLY_UNDERSTOOD + 2 OPAQUE` (62+4=66 ceiling). |
| 0.4 | Diagnostics: meshes | `#diag-meshes` shows `imported 14 / currently visible 14 — none excluded`. `__pecApp.visibleLedger === {imported:14, visible:14, exclusions:0}`. |
| 0.5 | Diagnostics: textures | `#diag-textures` shows `bound texture NAMES 9 + UNTEXTURED_LABELED 5 of 14`; `#diag-textures-per-mesh` lists all 14 per-mesh statuses (9 TEXTURE_NAME_BOUND with names; 5 UNTEXTURED_NO_TEXPROP). |
| 0.6 | Diagnostics: transforms | `#diag-transforms` shows the four-space distinction + `RENDER_ADAPTER_CHOICE (x,z,-y) ×0.01 / PE_UNITS_NOT_CONFIRMED` + the VIEWER_INSTANCE_WRAPPER_POLICY and AUTHOR_PLACED_LAB policy lines. |
| 0.7 | Diagnostics: fingerprints + timing | `#diag-fingerprints` shows client re-hash status OK 14/14; `#diag-timing` shows nonzero server adapter load ms / wire fetch bytes / client rebuild ms. `__pecApp.fingerprintCheck.verified === 14`. |
| 0.8 | Hierarchy inspector | `#inspector-body` renders 66 rows (block idx/type:name/status/serialized local TRS/FILE_SCENE world TRS); exactly 5 rows carry the `[dPVS-name-hint]` marker. |
| 0.9 | WebGL canvas | The canvas (`#view-canvas`) shows the model (14 meshes; dPVS-named meshes included and visible). |

## 1. ASSET MODE interactions

| # | Interaction | Expected observable outcome |
|---|---|---|
| 1.1 | Orbit: LMB drag on the canvas | The camera orbits (model orientation changes); no console errors in `__pecApp.errors`. |
| 1.2 | Pan: RMB drag; zoom: wheel | Camera pans/zooms (view changes). |
| 1.3 | Click button `Fit bounds [F]` (or press F) | Camera frames the model bounds; `#hud-line` shows `camera fit to current visible bounds`. |
| 1.4 | Click button `Reset camera [R]` (or press R) | Camera returns to the lab default pose; HUD shows `camera reset (lab default pose)`. |
| 1.5 | Click `Wireframe [W]` | All visible meshes switch to wireframe; `__pecApp.wireframe === true`; click again → solid (`false`). |
| 1.6 | Click a MESH in the viewport (e.g. a B_Outpost part) | `#selection-body` shows the selected block (index/type:name/status/serialized local TRS/FILE_SCENE world TRS); the inspector row with `data-block` matching gets the `sel` class; `__pecApp.selectedBlock` equals that block index. |
| 1.7 | Click an inspector ROW (e.g. a dPVS row) | Same selection observables as 1.6 — dPVS meshes are ADDRESSABLE while visible. |
| 1.8 | Click `dPVS-name-hint: hide (heuristic)` | The 5 dPVS-named meshes disappear from the view; `#diag-meshes` + `#ledger-body` show `imported 14 / currently visible 9 — excluded 5 (HIDDEN_BY_USER_DPVS_HEURISTIC_TOGGLE)` with per-mesh reasons; `__pecApp.visibleLedger === {imported:14, visible:9, exclusions:5}`. The meshes remain SELECTABLE via inspector rows (addressability under the heuristic). |
| 1.9 | Click `dPVS-name-hint` again | Back to visible 14/14; ledger shows none excluded. |

## 2. AUTHORED SCENE MODE interactions

| # | Interaction | Expected observable outcome |
|---|---|---|
| 2.1 | Click button `2 — Authored scene mode (two instances)` | `__pecApp.mode === 'scene'`, `modeSwitches` increments; `#scene-panel` becomes visible; the view shows TWO separate instances on the authored lab grid; HUD line mentions the two authored instances. |
| 2.2 | Instance panel | `#instance-list` shows two buttons: `author-instance-A` and `author-instance-B`, each with its composed scene translate (A: t(30,0,-10), B: t(-30,0,10) — AUTHOR_PLACED_LAB defaults). |
| 2.3 | Select instance A | `__pecApp.selectedInstance === 'author-instance-A'`; `#selection-body` shows instance A with asset ref (cacheKey), authored TRS, composed scene TRS and the VIEWER_INSTANCE_WRAPPER_POLICY line; editor inputs reflect A's authored values. |
| 2.4 | Change A's authored transform: set t.x = 55.5, uniform scale = 1.25, rotate-Z = 90, click `Apply to selected instance` | A visibly moves/scales/rotates; `__pecApp.lastApplied === { instanceId:'author-instance-A', afterTranslate containing 55.5..., otherInstanceId:'author-instance-B', otherTranslateUnchanged:true }`; `#independence` shows `independence check: changing author-instance-A left author-instance-B unchanged: YES ...`; `__pecApp.instances['author-instance-B'].composedSceneTranslate` is STILL (-30,0,10) — B DID NOT MOVE. |
| 2.5 | Select instance B and inspect | `#selection-body` shows B; its authored + composed TRS are the AUTHORED DEFAULTS (unchanged by step 2.4). |
| 2.6 | Change B's transform too (e.g. t.z = 40) | B moves; A keeps the values from 2.4; `lastApplied.otherInstanceId === 'author-instance-A'` with `otherTranslateUnchanged: true` (A's composed translate still reflects 55.5). |
| 2.7 | Click `Reset this instance to authored default` (B selected) | B returns to t(-30,0,10) scale 1; A untouched. |
| 2.8 | Click a MESH belonging to B in the viewport | The instance selection switches to `author-instance-B` (the picker resolves the owning instance-wrapper). |
| 2.9 | Resource sharing evidence | Both instances render the SAME 218757 resource — diagnostics identity unchanged (one asset, payload SHA pinned); the visible ledger in scene mode reports `imported 28 (2x14 per-instance mesh objects) / visible 28`; wireframe/dPVS toggles apply to BOTH instances per the same rules. |
| 2.10 | Switch back to `1 — Asset mode` | `__pecApp.mode === 'asset'`; scene objects are disposed; the asset mode works exactly as in section 1 (fresh mount). |

## 3. Fail-closed honest errors (negative controls in the browser)

| # | Interaction | Expected observable outcome |
|---|---|---|
| 3.1 | Stop the server, reload the page | `data-load-status="ERROR_ASSET_LOAD..."`, `#error-banner` visible with the fetch failure, `__pecApp.boot === 'asset-load-error'`; the app does NOT render any stale asset. |

## 4. After the check

Stop the server (terminate the PID); verify the port is freed. Record results
honestly per step (PASS / FAIL with the observed values). The phase-3 one-shot
headless evidence (boot-to-READY DOM dump) is in `raw/HEADLESS_DOM_DUMP.html`;
this checklist covers everything the one-shot could not interact with.
