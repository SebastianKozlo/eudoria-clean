# CATALOG_UI_NOTES.md — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (CATALOG_MODE_SERVER_TESTS)

The /catalog browser mode (contract §5), its bounded server, and how to view
everything. All numbers below are the phase-4 measured values (sources: the
raw records under `raw/CATALOG/`, the gate summaries, and the run's own
regeneration at server startup).

## 1. What the user can view — URL, start/stop commands

- **URL:** `http://127.0.0.1:8161/catalog` (loopback only; `/` also serves the
  catalog page). Deep link: `http://127.0.0.1:8161/catalog#model=193313` (any
  of 192374 / 193207 / 193313 / 193684) opens that primary's preview directly.
- **START:** `npm run serve:catalog` (or `node compat/server-catalog.mjs`).
  The port is configurable via env: `PECATALOG_PORT` (then `PORT`) — default
  **8161**. Port **8140 is REFUSED BY CONSTRUCTION** (the foreign standing
  reference server owns it and is never touched or replaced; a busy port is a
  LOUD failure — this server never replaces a running process).
- **STOP:** terminate the printed PID (`Ctrl+C` in the owning console, or
  `Stop-Process -Id <PID>`). The startup line is
  `catalog server http://127.0.0.1:<PORT>/ pid=<PID>`.
- Startup regenerates BOTH era catalogs from the pinned READ_ONLY originals
  (fail-closed container SHAs incl. the REQUIRED Models.bnt pin; per-entry
  CRC32 + payload SHA256 recomputed; ~2 s warm). Nothing is served from stale
  hand-edited JSON: the only cached inputs are the phase-2/3 MEASURED artifacts
  attached strictly by identity key (era + container SHA + entry + payload SHA;
  mismatches dropped and counted).

## 2. The catalog panel (left) — columns and controls

Table columns (era label on every row; the same entry name in both eras is TWO
distinct assets): **era | ID / entry name (+PREVIEWABLE flag) | file size
(bytes, uncompressed) | scene extent maxAxisExtent (+footprintX/Z; FILE_SCENE_SPACE,
ORIGINAL file units — never called meters) | geometry tri / vert / shapes |
decode coverage (+reason) | texture coverage | role hypothesis (Desktop names)
+ evidence**.

Controls: era filter (ALL/CD_2003/PCG_9_3_5), decode-coverage filter
(DECODED_FULL_CLOSURE / DECODED / DECODED_NO_MESH / FAILED / VERSION_GATED /
CATALOG_ONLY), sort per metric (payload size, scene extent, triangles,
vertices, shapes), ID/name search (matches BOTH eras; era-separated rows stay
distinct — try `65678`), paging (100/page).

**Sort/UNKNOWN rule (stated in the UI):** measured values largest→smallest;
UNKNOWN rows are always LAST with an UNKNOWN badge — UNKNOWN is never treated
as 0. REAL measured zeros (the 17 DECODED_NO_MESH rows) render as 0 — measured
0 ≠ UNKNOWN. Every table is LARGEST-MEASURED (the coverage box shows:
rows TOTAL 8,088 = CD_2003 2,492 + PCG_9_3_5 5,596; extent MEASURED 1,555 /
UNKNOWN 6,533; decode distribution CATALOG_ONLY 2,488 | FAILED 3,270 | DECODED
1,551 | VERSION_GATED 758 | DECODED_NO_MESH 17 | DECODED_FULL_CLOSURE 4).

Rows that are NOT the four primaries show their honest state on click
(CATALOG_ONLY / VERSION_GATED / FAILED with the reason) — no fake previews.

## 3. The preview (right) — the four pinned CD_2003 primaries only

Open by clicking a PREVIEWABLE row or the deep link. Features:
- **Original hierarchy tree** (roots/children names, per node/shape with block
  numbers) with **part isolation** (per-shape visibility checkboxes);
- **wireframe toggle** [W], **fit bounds** [F], **reset camera** [R];
- **bounds/origin display** (min/max/extents/maxAxisExtent/footprintX/Z,
  FILE_SCENE_SPACE, ORIGINAL units; label: SOURCE_FILE_SCENE_SPACE ≠
  WORLD_PLACEMENT; the file-space origin axes are drawn at (0,0,0));
- **UV/texture diagnostics**: per mesh `0 UV sets`, `ArkTexture numTex=0`,
  `UNTEXTURED_PROXY_MESH — no texture applied (no fake textures)`; the preview
  applies ONLY the verified NiMaterialProperty diffuse colors (material
  preview; the applied materials are listed per shape in the diagnostics);
- **view modes:** `View: original coords [C]` toggles ORIGINAL file
  coordinates (wrapper identity — the CAMERA moves; NO centering applied)
  beside the default fit-to-view CENTERED mode (centering applied EXACTLY ONCE
  at the presentation wrapper; NO unit conversion, NO axis swap — original
  vertex values intact in both modes; the wrapper offset is printed in the
  diagnostics);
- **fail-closed client checks** (printed in diagnostics): served-wire pin check
  (payload+container SHA vs the app pins), client-side world-transform
  composition + bounds cross-check vs the shipped values, geometry
  fingerprint re-hash (crypto.subtle; honest NOT_PERFORMED_SUBTLE_UNAVAILABLE
  when unavailable); a mismatch refuses the render loudly.

## 4. API surface (bounded, loopback-only, read-only GET/HEAD)

- `GET /api/catalog/status` — identity/coverage snapshot: both container pins
  (incl. the REQUIRED Models.bnt pin verified at load), per-era entry counts,
  CRC verification counts, decode-coverage distribution, extent measured/unknown,
  the same-name-both-eras census (2,177), the identity-key cache attach stats,
  the sort rule.
- `GET /api/catalog/rows?era=&status=&q=&sort=&page=&pageSize=` — server-side
  sorted/filtered/searched rows (pageSize max 500, default 100; unknown
  filter/sort values → 400 DENIED_EXPLICIT). Response carries the coverage
  block + the sort rule.
- `GET /api/catalog/model/CD_2003/<id>` — the bounded PREVIEW WIRE for exactly
  the four pinned primaries (lazy build + identity-keyed cache; pins in headers
  + body). Any other id → 404 `PREVIEW_NOT_ESTABLISHED` with that entry's honest
  decode state; the route only accepts `CD_2003/<digits>`.

## 5. Denial design (BY CONSTRUCTION — extends the sceneir server design)

- **Reuse label:** the deny()/serveBytes() shape, exact-allowlist static maps,
  the jailed three-subtree reader (path-jail + traversal/encoded/absolute
  refusal), the NUL/backslash/malformed-URL refusals, the GET/HEAD-only 405,
  the verified-free-port probe and the fail-closed startup are EXTENDED from
  `compat/server-sceneir.mjs` (the sceneir server itself stays byte-identical —
  NOT a fork of its serving role: this server serves only the catalog app).
- Static surface = exact allowlist maps: `catalog.html` (at /catalog), the four
  catalog JS/CSS files, shared `compat.css`, the two client-needed
  `src/pecompat` modules (PecSceneIR.js, PecTransform.js), and the pinned
  three 0.185.0 package subtree (jail-checked). The server-side extraction
  chain (ArkArchive/Bnt2Archive/nif41_deep/catalog_data) is NOT publicly routed.
- Measured denial battery (13 negatives + POST, all DENIED_EXPLICIT with named
  errors — raw transcript `raw/CATALOG/CATALOG_HTTP_TRANSCRIPTS.json`):
  relative traversal, absolute path, encoded traversal, src-tree traversal,
  backslash, unconfigured root, whole-corpus attempts, unknown asset id, a REAL
  non-previewable entry (65678 — honest CATALOG_ONLY state), PCG id (no preview
  route by design), the SceneIR route (NOT served by this server — 404
  ROUTE_NOT_FOUND), unknown route, unallowlisted compat static (app.js — the
  218757 app belongs to its own server).
- No arbitrary filesystem path endpoint; no whole-corpus static route; the
  containers are never exposed over HTTP (only index-derived metadata + the
  four primary wires).

## 6. Reuse vs new (phase 4)

REUSED UNCHANGED: `src/pesource/ArkArchive.js`, `src/pesource/Bnt2Archive.js`,
`tools/pecompat/catalog_sniff.mjs` + `png_nontrivial.mjs`, the phase-3 reader
`nif41_deep.mjs` (+ its PHASE-4 ADDITIVE export of `ir`/`worldTransforms` for
the wire builder — no analysis value changed), `src/pecompat/PecSceneIR.js`
composition (reached through the reader), the FIXED T9 gate
(`evaluateLoadGate` imported from `tests/pecompat/headless_load.test.mjs` —
identical gate semantics), the app-server lifecycle helper patterns
(`_app_server_helpers.mjs` generic exports), the PIXEL_RENDER capture
pattern (`t9_pixel_render.mjs`).

NEW (allowlist): `tools/pecompat/catalog_data.mjs` (era-aware data model,
bounded index readers, pure sort/filter, wire builder),
`tools/pecompat/texture_chain.mjs` (era-scoped resolution/dispositions),
`compat/server-catalog.mjs` + `catalog.html` + `catalog-app.js` +
`catalog-table.js` + `catalog-preview.js` + `catalog.css`,
`tests/pecompat/_catalog_server_helpers.mjs` + 7 gate suites +
`run_catalog_tests.mjs`, `tools/pecompat/catalog_pixel_render.mjs` +
`phase4_texture_dispositions_update.mjs`, the `serve:catalog` /
`test:pecompat:catalog` package.json scripts (three stays pinned 0.185.0; NO
new dependencies).

## 7. Honest limits

- The preview exists ONLY for the four primaries (the bounded reader's scope);
  PCG_9_3_5 models have NO /catalog preview route by design (218757's viewer is
  the separate SceneIR app — untouched, regression-free 24+22 gate PASS).
- INTERACTIVE = NOT_PERFORMED (the automation daemon is down — ECONNREFUSED on
  127.0.0.1:9222 and [::1]:9222, and the session's browser automation connects
  to the same downed daemon; recorded honestly, never faked). LOAD (2 real
  headless-browser loads through the FIXED 5-conjunct gate) and PIXEL_RENDER
  (5 calibrated, verified screenshots incl. all four previews) were both
  executed and PASSED.
- No city/place identification, no world coordinates, no historical placement
  anywhere in the UI (SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT);
  node names are byte-level reproduced hypotheses, never game classes.
