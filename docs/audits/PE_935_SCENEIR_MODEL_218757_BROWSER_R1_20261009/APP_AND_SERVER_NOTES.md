# APP_AND_SERVER_NOTES — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Phase APP_SERVER_TESTS (phase 3). The compat app, its loopback server, the
API surface and the path-denial design. All measured values in this document
come from `raw/TESTS_APP_MACHINE_SUMMARY.json` (13/13 PASS) and its raw
transcripts.

## 1. Start / stop commands + URL

The server and app live entirely in the worktree:

- Start (from the worktree root
  `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1`):

  ```
  npm run serve:sceneir            # = node compat/server-sceneir.mjs
  ```

  Optional env overrides:
  - `PORT` — bind port (default **8140**). A busy port is a LOUD failure
    (`exit 1`); the server never replaces or stops another process.
  - `PECOMPAT_MODELS_BNT` — pinned Models.bnt path (default
    `D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt`).
  - `PECOMPAT_THREE_ROOT` — three package root (default the canonical
    checkout `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\node_modules\three`,
    version-pinned to **0.185.0** and verified at every start).
  - `SCENEIR_LOG_REQUESTS=1` — per-request log line (diagnostics only).

- Startup output (measured, see `raw/HTTP_TRANSCRIPTS.json`):

  ```
  sceneir server http://127.0.0.1:<PORT>/ pid=<PID>
  [server-sceneir] ready in <startup> ms — model 218757 regenerated from the pinned container (fail-closed SHA verified; adapter load <load> ms)
  [server-sceneir] cacheKey=218757:3e8a22c2...12cf36:pec-nif101-adapter-v1:pec-sceneir-v1
  [server-sceneir] payloadSha256=3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36 containerSha256=c950a8c2...d3bee0
  [server-sceneir] blocks=66 meshes=14 supported=62 partiallyUnderstood=2 opaque=2
  [server-sceneir] three 0.185.0 from the configured private root; static surface = allowlist maps; STOP = terminate pid <PID>
  ```

- URL: **http://127.0.0.1:8140/** (default port; loopback ONLY — the bind
  address `127.0.0.1` is not configurable).

- Stop: terminate the printed PID — `Stop-Process -Id <PID>` (PowerShell),
  Ctrl+C in the owning console, or `child.kill()` from a harness. Graceful
  shutdown closes the listener and exits; a bounded harness additionally
  verifies the port is FREED by a rebind probe (see the T7 lifecycle record).

- Port verification method (measured, both directions): a bind/close probe
  BEFORE `listen` (busy → LOUD exit 1), plus the OS `EADDRINUSE` error handler;
  after stop, a fresh bind/close probe of the same port proves release
  (T7_SERVER_LIFECYCLE: portFreed=true).

- Measured load time: the SceneIR is REGENERATED from the pinned container at
  server startup through PecAssetAdapter — container + payload SHA256
  verified fail-closed on EVERY start (measured adapter load ≈ 480–640 ms,
  total startup ≈ 525–653 ms; exact per-run values in the raw artifacts).
  No stale exported JSON exists in the product path; the in-memory cache is
  keyed by the SceneIR cacheKey = asset SHA + adapter/schema version.

## 2. API surface (read-only; GET/HEAD only)

| Route | Content |
|---|---|
| `/` , `/index.html`, `/compat/` | `compat/index.html` (the ONE app) |
| `/compat/<allowlisted file>` | the six app files: index.html, app.js, api.js, asset-mode.js, scene-mode.js, compat.css (EXACT allowlist map) |
| `/src/pecompat/<allowlisted module>` | the four client-needed modules: PecTransform.js, PecSceneIR.js, PecInstanceBuilder.js, PecRenderConvert.js (the server-side extraction chain PecNif10Reader/PecAssetAdapter is deliberately NOT routed) |
| `/node_modules/three/<subpath>` | the pinned three 0.185.0 package subtree from the CONFIGURED PRIVATE ROOT (jail-checked; version pin verified at startup) |
| `/api/status` | bounded status: bind/port/pid, three pin, cacheKey, modelId, block/mesh counts, read-only flag |
| `/api/sceneir/218757` | the bounded index-derived wire SceneIR (identity + per-block TRS/links + geometry arrays + fingerprints + diagnostics), with `X-PE-Payload-Sha256` / `X-PE-Container-Sha256` / `X-PE-Cache-Key` headers |
| anything else | 404 ROUTE_NOT_FOUND (explicit JSON) |

The wire payload is regenerated per server start (fail-closed SHA). Geometry
arrays in it are runtime loopback-only data — never a committed fixture.

## 3. Path-denial design (measured: 22/22 SYNTHETIC denials, all explicit)

Denial is BY CONSTRUCTION, not by filtering:

1. **Static routes are exact allowlist maps** — the request URL is used as a
   map KEY only; it NEVER becomes a filesystem path. Traversal keys
   (`/compat/../server.mjs`, `/compat/%2e%2e/server.mjs`,
   `/compat/..%2f..%2f...`) simply miss the map → 404
   `STATIC_FILE_NOT_ALLOWEDLISTED`.
2. **The only prefixed filesystem route** (the three package) is jail-checked:
   decoded subpath must contain no `..`, no backslash, no `%`, no NUL; the
   resolved absolute path must start with the package root → escapes hit
   403 `PATH_TRAVERSAL_BLOCKED` / 400 `BACKSLASH_IN_URL`.
3. **Unconfigured roots are unreachable**: `/src/pesource/*`, `/docs/*`,
   `/tools/*`, the server file itself, absolute Windows drive paths
   (`/D:/...`, `//D:/...`) and raw `/..` / `/../` all fall to 404
   `ROUTE_NOT_FOUND`. The whole BNT and the source trees have NO route — the
   `/pcg/`-style aliases of the base server are deliberately NOT replicated.
4. **Malformed URLs** (bad percent `%zz`, NUL byte `%00`) → 400
   `MALFORMED_URL` / `NULL_BYTE_IN_URL`.
5. **Read-only API**: POST/PUT → 405 `METHOD_NOT_ALLOWED_READ_ONLY`.
6. **Unknown asset** (`/api/sceneir/999999`) → 404 `UNKNOWN_ASSET_ID`; the
   nonexistent archive/entry route class (`/api/archive/Models.bnt/entry/...`)
   → 404.

Full request+response transcript: `raw/HTTP_TRANSCRIPTS.json` (6 positive +
22 denial entries — 18 in the traversal/unknown-route battery + 4 malformed/
method; each with status, explicit error class, payload-leak check against
NIF/BNT markers — all negative).

## 4. The app (one page, two modes — capabilities implemented)

`compat/index.html` + `compat/app.js` + `compat/api.js` +
`compat/asset-mode.js` + `compat/scene-mode.js` + `compat/compat.css`
(zero-framework vanilla JS + three 0.185.0 via the importmap; no CDN; no new
dependencies).

- **ASSET MODE**: 218757 loaded through the asset API (fail-closed client pin
  check); OrbitControls (LMB-drag orbit / RMB-drag pan / wheel zoom);
  fit-bounds (`[F]` / button); reset camera (`[R]` / button); solid/wireframe
  (`[W]` / button); axes helper; hierarchy inspector — per block: type:name,
  supported/PARTIALLY_UNDERSTOOD/OPAQUE status, ORIGINAL serialized local TRS
  vs COMPUTED FILE_SCENE_SPACE world TRS; click a mesh or a row to select.
- **AUTHORED SCENE MODE**: TWO separate instances of the SAME shared 218757
  resource with independent authored transforms (AUTHOR_PLACED_LAB); per
  instance select/inspect (instance ID, asset ref/cacheKey, authored TRS,
  composed scene TRS); editing the selected instance's transform applies only
  to it — an explicit on-screen INDEPENDENCE line reports that the other
  instance is bit-identical before/after; reset-to-authored-default per
  instance; the grid is an EXPLICITLY AUTHORED lab GridHelper (no Eudoria
  terrain claim).
- **DIAGNOSTICS panel** (data-load-status attribute + fields): original asset
  identity (era/container/entry/payload SHA256/cacheKey/NIF version + pin
  verified), block coverage 62+4=66 (62 SUPPORTED, 2 PARTIALLY_UNDERSTOOD,
  2 OPAQUE — ceiling preserved), imported vs currently visible meshes with
  the exclusion ledger, material/texture status per mesh (9
  TEXTURE_NAME_BOUND + 5 UNTEXTURED_NO_TEXPROP; container resolution
  NOT_ESTABLISHED), transforms as distinct spaces + the RENDER_ADAPTER_CHOICE
  (x,z,-y)×0.01 / PE_UNITS_NOT_CONFIRMED label, measured load timings,
  client-side fingerprint re-hash result.
- **dPVS policy**: meshes with dPVS/occluder-like names (5 in 218757) stay
  ADDRESSABLE — selectable and inspectable at all times; the
  "dPVS-name-hint: hide (heuristic)" toggle is clearly labeled as a name-hint
  heuristic (runtime role NOT proven) and the ledger reports imported 14 /
  visible 9 with a reason per excluded mesh. The app never claims 14 rendered
  when some are hidden.
- **Observable surface** `window.__pecApp` for automation: boot, loadStatus,
  mode, modeSwitches, selectedBlock, selectedInstance, visibleLedger,
  instances (authored + composed translates per instance), lastApplied
  (before/after translate + otherTranslateUnchanged), wireframe,
  diagnostics counts, fingerprintCheck, errors. The diagnostics root carries
  `data-load-status` (PENDING → READY / ERROR_*).
- **Viewer policy label** (rendered in the UI): the instance wrapper owns the
  scene transform while the imported asset hierarchy retains its serialized
  root/child transforms — NOT a reproduction of every SDK 2.6
  root-replacement branch or the original PE placement mechanism.

## 5. Headless evidence (T9 PREP — measured)

`msedge --headless=new --user-data-dir=<temp> --virtual-time-budget=30000
--dump-dom http://127.0.0.1:<port>/` (Edge
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`, dedicated temp
profile — the user's browser profiles are never touched):

- exit code 0; DOM 21064 B; `data-load-status="READY"`; the request log shows
  the full module chain + `/api/sceneir/218757` all 200; the dump contains the
  rendered diagnostics (payload SHA256 3e8a22c2…12cf36, blocks 66, imported
  14/visible 14, 9+5 texture statuses). Evidence: `raw/HEADLESS_DOM_DUMP.html`
  + `raw/HEADLESS_RUN.json`.
- The ONE-SHOT dump-dom proves a real-browser boot-to-READY (renderer, fetch,
  pin checks, fingerprint re-hashes, mode mount). Interactive behaviors
  (orbit, select, transform change, independence, reset/fit, wireframe, dPVS
  toggle) are NOT exercised by the one-shot dump — they are listed for
  PE-MASTER in `SMOKE_CHECKLIST.md`.
- Additional one-shot diagnostic (temp script, same headless recipe, recorded
  in the ledger INT-4): `http://127.0.0.1:<port>/#scene` also boots to
  `data-load-status="READY"` with the scene panel visible, the instance list
  populated (author-instance-A/B) and the scene-mode ledger reporting
  imported 28 (2x14 per-instance mesh objects) — the AUTHORED SCENE MODE
  mounts in the real browser; the independence line populates only AFTER an
  apply action (not asserted at boot).

## 6. Test gates of this phase (13/13 PASS)

`node tests/pecompat/run_app_tests.mjs --models <pinned Models.bnt>` —
T7 (6 records), T8 (6 records), T9 (1 record); every suite owns its bounded
server lifecycle (PID/port/lifetime/port-freed recorded; nothing left
running). Full machine summary: `raw/TESTS_APP_MACHINE_SUMMARY.json`;
curated results: `TEST_RESULTS_APP.json`.

## 7. Honest repair history (this phase)

1. T8 initial crash: `authored2.asset` — createAuthoredScene returns
   `{registry, instances}`; fixed to read the shared asset record directly.
2. The app boot function was defined but never invoked — the headless DOM
   stayed PENDING and the request log proved the SceneIR fetch never
   happened; the `boot()` call (with honest ERROR status on rejection) was
   added and the headless evidence re-measured (READY).
3. A PowerShell `Set-Content` round-trip double-encoded four compat/*.js
   files (CP1252 mojibake); reversed by byte-accurate re-decode and
   normalized to pure ASCII; re-measured green.

All three repairs are preserved here (per the contract's honest-failure
discipline); the phase's final state is the re-measured 13/13.
