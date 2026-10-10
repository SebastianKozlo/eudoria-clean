# PLAN_AND_ALLOWLIST.md — PE_CITY_ASSET_MAP_R1_20261010

Phase 1 (SETUP_T9_FIX_BROWSER_LOAD). This document states the run-wide path allowlist (contract §8), the planned files/commands for ALL phases, and an honest reuse-vs-new declaration. Later phases must not write outside this allowlist without a CORRECTION_REQUEST to PE-MASTER.

## 1. Path allowlist (contract §8) — the ONLY paths this run may create/modify

| Allowed path | Role | Phase-1 status |
|---|---|---|
| `compat/` | viewer app (product source) | READ_ONLY in phase 1 (untouched — verified by git diff) |
| `src/pecompat/` | PE compat library (product source) | READ_ONLY in phase 1 (untouched — verified by git diff) |
| `tools/pecompat/` | bounded tooling (test/analysis; NO corpus extraction without phase authorization) | written: `t9_pixel_render.mjs`, `png_nontrivial.mjs` |
| `tests/pecompat/` | test harness | written: T9 fix in `headless_load.test.mjs` + `run_app_tests.mjs` |
| `.opencode/skills/pe-gamebryo-rosetta/` | project skill (contract §6 update) | READ_ONLY in phase 1; update in later phase |
| `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/` (REPORT_PACKAGE) | this report package | written |
| `package.json` | ONLY justified scripts/deps; three 0.185.0 UNCHANGED | untouched in phase 1 |

NOT in the allowlist and NEVER touched: master, AUDIT_ENTRYPOINT.md/governance, the old SceneIR worktree `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1` and its standing server (port 8140, PID 21288 — foreign READ_ONLY reference, verified still running at phase end), historical report packages (incl. `docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/` — the harness default raw dir was changed precisely so a default invocation can never write into it), foreign untracked paths of the canonical checkout (`docs/audits/PE_935_*` + `experiments/`), all original containers/inputs (READ_ONLY), the VM.

Private outputs (never committed, never in the repo, never base64/JSON-encoded): `D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\` — pixel render PNGs, later top-view/wireframe projections, part summaries and any other derived images/geometry exports.

## 2. Planned files per work item (whole run)

### W1 — T9 gate fix (THIS PHASE — DONE)
- `tests/pecompat/headless_load.test.mjs` — REWRITTEN: production 5-conjunct gate `evaluateLoadGate()` (exitCode===0 AND DOM_NONEMPTY AND CANVAS_PRESENT AND DIAGNOSTICS_PRESENT AND STATUS_READY), per-conjunct named missing, two real-browser mode loads (asset + #scene), six synthetic per-conjunct negatives through the SAME gate, side-error separation (T9_RAW_PERSISTENCE, T9_SERVER_LIFECYCLE, T9_SERVER_STARTUP), STAND_IN_PROCESS labeling for env-override binaries, bounded flake retry (max 3 attempts, all recorded).
- `tests/pecompat/run_app_tests.mjs` — MINIMAL: safe default raw dir (this run's package; never the predecessor's READ_ONLY package), honest run relabel, exit code unchanged-by-design (nonzero on any FAIL — verified by execution: stand-in run exited 1).
- `tools/pecompat/t9_pixel_render.mjs` — NEW: PIXEL_RENDER gate tool (headless Edge `--screenshot` → PRIVATE_OUTPUT; poll-file+kill for the measured host quirk (Edge writes the file but may not exit); own bounded PNG analysis; suite-owned bounded server).
- `tools/pecompat/png_nontrivial.mjs` — NEW: own bounded PNG check (signature+IHDR+IDAT inflate+unfilter+region color/luminance census; node:zlib only — NO new dependency).
- Commands: `node tests/pecompat/run_app_tests.mjs --models <Models.bnt> --three-root <three> --raw-dir <raw> --json-out <json>` (PRE with `PECOMPAT_BROWSER_BIN=node.exe`; POST clean; POST stand-in), `node tools/pecompat/t9_pixel_render.mjs --out <PRIVATE png> --raw-out <raw json> ...`, `node tests/pecompat/run_tests.mjs --models <Models.bnt>`.

### W2 — Metadata catalog, both eras (later phases)
- `tools/pecompat/catalog_census.mjs` (planned NEW): Data-directory physical-file census per era (relative path, size, extension, era, SHA256) — an inventory, NOT a claim of format understanding.
- `tools/pecompat/ark_index.mjs` + `tools/pecompat/bnt_index.mjs` (planned NEW): full entry catalogs with boundaries, original names, stored/unpacked sizes, compression method, entry SHA where safely readable; index verification (boundaries + duplicates). REUSE of format knowledge: pe-ark-vfs/pe-bnt-tdf/pe-kaitai-struct skills + historical parsers as REFERENCE implementations (each decoder claim re-validated by dual decode where the skill mandates it).
- Identity key everywhere: ERA + CONTAINER_SHA + ENTRY_NAME + PAYLOAD_SHA (an ID alone is never globally unique). All entries kept incl. unsupported/failed, with field-level coverage and explicit error/unknown — never invented zeros.
- Outputs: `CATALOG_COVERAGE.json` (report package, metadata only), full private catalogs in PRIVATE_OUTPUT.

### W3 — Four-model deep analysis (later phases; PRIMARY_IDS 192374/193207/193313/193684, ERA=CD2003; first deep case 193313)
- `tools/pecompat/` deep-analysis tools (planned NEW): original-hierarchy recovery (roots, typed links, parent/child, names, local TRS, composed FILE_SCENE transforms, shape→data, geometry, properties, opaque blocks) with explicit PARTIAL marking (no identity-transform fallback without a label); reproduce the Desktop name reads (193313: Outpost39_proxymesh, MSC, signs, build, MAC; 193684: signs, mlti, wall, signs01, mac, build, cont, forts; 192374: Box01, MSC, MAC, signs; 193207: Box06, Object01) from the ORIGINALS — names and hypotheses only, never confirmed collision/dPVS/LOD roles or city names.
- GLB comparison against `pe_asset_viewer_v4` output: geometry compared only after explicitly established axis/transform conversion; lineage established, not assumed; flat-GLB missing textures prove nothing about originals.
- Private projections (top view, wireframe, part summaries) → PRIVATE_OUTPUT only. Connected components ≠ building counts. Original origin/bounds preserved; any centering only in a presentation wrapper.
- Output: per-model status in `CLAIM_MATRIX.csv` + report.

### W4 — Texture-chain tooling (later phases)
- `tools/pecompat/texture_chain.mjs` (planned NEW): provenance-edge cataloging for the 4 models + already-correctly-read models: shape → property → texture reference/name/Ark binding → container entry → decoded image; disposition classes exactly as preregistered (NAME_FOUND / REFERENCE_CONFIRMED / CONTAINER_ENTRY_RESOLVED / IMAGE_DECODED / MATERIAL_APPLIED / BROWSER_OBSERVED); slot/UV/alpha/wrap only where proven; NO 9-byte-tail interpretation transfer between models; missing texture = explicit visual fallback, never a fake textured PASS; era separation on every edge.
- Output: `TEXTURE_LINK_DISPOSITIONS.csv` (metadata only).

### W5 — /catalog viewer mode + server (later phases)
- `compat/` — planned: a separate `/catalog` viewer MODE (era/ID/source-name panel, size, scene extent, geometry counts, decode coverage, texture coverage, role hypothesis + evidence; sort desc per metric; era/status filters; ID/name search; UNKNOWN visible, never 0; original-coordinates view beside fit-to-view; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT always labeled). Existing asset/scene 218757 modes preserved with ZERO regression.
- `compat/server-sceneir.mjs` or a sibling bounded server (planned modification/extension): loopback only, free-port probe (never 8140/foreign processes), specific assets/indexed reads only — no whole-corpus static route, no arbitrary paths.
- `package.json`: ONLY justified scripts (e.g. a `serve:catalog`/`catalog` script) — three stays pinned at 0.185.0; NO new dependencies.

### W6 — Tests + QC/reports (later phases)
- `tests/pecompat/` — planned: catalog regression tests (UNKNOWN sort/filter, units, coverage counts), 218757 regression (14 associations, two-instance independence, no double-centering/conversion), texture-chain controls (wrong-ID, wrong-era, missing image), archive negative controls (truncation, corrupt input, duplicate IDs), gate preservation for the fixed T9.
- Report package (final): REPORT.md, INPUT_IDENTITIES.json (this file exists; grows as inputs are actually read), CATALOG_COVERAGE.json, CLAIM_MATRIX.csv, TEXTURE_LINK_DISPOSITIONS.csv, TEST_RESULTS.json, LIMITATIONS.md, REVIEW.md, EVIDENCE_INDEX.md, HANDOFF.md + MANIFEST last, self-excluded, bijection-verified.

## 3. Honest reuse-vs-new declaration

REUSED UNCHANGED (inherited from BASE 59641ca — zero product-source changes in phase 1, verified by git diff):
- the whole SceneIR viewer stack (`compat/index.html, app.js, api.js, asset-mode.js, scene-mode.js, compat.css, server-sceneir.mjs`);
- `src/pecompat/` reader/adapter/builder/convert modules (PecNif10Reader, PecAssetAdapter, PecSceneIR, PecInstanceBuilder, PecRenderConvert, PecTransform);
- `tests/pecompat/_app_server_helpers.mjs`, the unit harness `run_tests.mjs` + its 24 controls, T7 `api_path_denial.test.mjs`, T8 `app_integration.test.mjs`;
- Node 22 + three 0.185.0 from the canonical checkout's node_modules (passed via `--three-root`; read-only).

NEW in phase 1 (all inside the allowlist):
- the fixed T9 gate predicate + per-conjunct evaluation/naming (`evaluateLoadGate`) — new logic in the test harness;
- the two-mode real-browser load records, six synthetic per-conjunct negatives, side-error record separation, STAND_IN labeling, bounded flake retry;
- `tools/pecompat/t9_pixel_render.mjs` + `png_nontrivial.mjs` (own bounded PNG analysis — no new dependency);
- this report package.

PLANNED NEW in later phases: W2/W3/W4/W5/W6 tools, viewer mode, server extension, tests and reports as itemized above. One targeted repair round is budgeted for later phases; remaining errors are recorded and closed with an honest PARTIAL/REQUIRE_CORRECTIONS.

## 4. Era discipline

Every catalog record, ranking, preview and comparison carries an explicit `era` field: `CD_2003` (Models.ark/Textures.ark) or `PCG_9_3_5` (Models.bnt/Textures.bnt/vfs). No cross-era texture/asset attribution without an explicit provenance edge; a missing texture/container is a LOCAL status for that asset+era, never a global BLOCKED; era mismatches are controlled negatives (wrong-era → controlled FAIL).

## 5. Phase-1 execution summary (commands actually run)

- `git worktree add "D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1" -b codex/pe-city-asset-map-r1-20261010 59641caa1b14ade84e1842ca36b395842deb241e` (the single allowed write in the canonical checkout).
- PRE: `PECOMPAT_BROWSER_BIN=C:\Program Files\nodejs\node.exe node tests/pecompat/run_app_tests.mjs --models <Models.bnt> --three-root <three> --raw-dir <pkg>/raw/T9/PRE --json-out <pkg>/raw/T9/PRE_APP_SUMMARY.json` → 13 PASS / 0 FAIL / exit 0 WITH the stand-in false-PASS (raw preserved).
- POST: same without env override → 22 PASS / 0 FAIL / exit 0 (real Edge, both modes, all conjuncts).
- POST_STANDIN: same with env override → 2 FAIL with all five named missing conjuncts / exit 1.
- PIXEL: `node tools/pecompat/t9_pixel_render.mjs --out <PRIVATE>\PIXEL_RENDER\T9_PIXEL_RENDER_ASSET_MODE.png --raw-out <pkg>/raw/T9/PIXEL_RENDER/PIXEL_RUN.json ...` → PASS (7/7 checks).
- Unit regression: `node tests/pecompat/run_tests.mjs --models <Models.bnt>` → 24 PASS / 0 FAIL / exit 0.
