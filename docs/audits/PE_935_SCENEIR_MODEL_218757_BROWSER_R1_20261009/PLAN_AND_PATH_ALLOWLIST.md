# PLAN_AND_PATH_ALLOWLIST — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Written BEFORE implementation (contract §3). This names the ACTUAL planned
files and commands for the whole run. The allowlist (contract §3) is included
VERBATIM below as the boundary. Deviations beyond it are not authorized.

## 0. Boundary — contract §3 allowlist (VERBATIM)

> Before implementation, write PLAN_AND_PATH_ALLOWLIST.md in REPORT_REPO_PATH
> naming the actual files and commands. Allowed worktree areas:
> - src/pecompat/ (IR, asset adapter, instance builder, render conversion);
> - compat/ (one local app and its read-only asset API);
> - tools/pecompat/ and tests/pecompat/;
> - .opencode/skills/pe-gamebryo-rosetta/ and docs/pecompat/;
> - REPORT_REPO_PATH;
> - src/pesource/ only for a necessary compatible fix, with existing witness regression;
> - package.json/package-lock.json only for justified scripts/dependencies.
>
> No AUDIT_ENTRYPOINT, governance, milestones, auditor profiles or master
> modifications. Publish on the named feature branch. Do not launch unrelated
> experiments or an exhaustive engine port.

REPORT_REPO_PATH = `docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/`.
Primary implementation is one model (218757), one app, one instance/transform
path. SDK examples are controls only.

## 1. Adapter path choice — EXTENDED JS READER (decision)

Two options were inspected against the actual code before choosing:

**(a) Extended JS reader** (page/Node-side, NEW code under `src/pecompat/`):
the base already contains an era-validated JS extraction chain —
`Bnt2Archive.js` (BNT2 index + raw payload read), `PESourceMount.getModelResource`
(`<id>.nif` entry read + provenance) — plus `NifModelReader.js`, a v10.1.0.0
reader whose 14 supported block types are EXACTLY the types 218757 needs
(NiNode, NiTriShape, NiTriShapeData, NiTexturingProperty, NiMaterialProperty,
NiAlphaProperty, NiZBufferProperty, NiVertexColorProperty, NiStringExtraData,
NiArkTextureExtraData, NiArkAnimationExtraData, NiArkImporterExtraData,
NiArkShaderExtraData, NiArkViewportInfoExtraData), with loud failures and
file-order bit-exact float conventions. The old compat app proves the whole
page-side chain (entry API → parse → THREE.BufferGeometry) works in the browser.

**(b) Local Python-to-SceneIR adapter** (extract → JSON → app loads JSON): would
add a Python runtime dependency to the runnable product and create a stale-JSON
risk; contract §7 requires the Python command/API to be part of the runnable
product and regenerated from the original container if this path is taken.

**DECISION: (a) extended JS reader — the smallest safe path.** One language and
one reader implementation serve the app AND the tests AND the 14-fingerprint
verification (no cross-language drift); extraction is regenerated from the
pinned Models.bnt container on every load (no stale exports); cache keys include
asset hash + adapter/schema version. Honest labels carried with it:
- `src/pesource/NifModelReader.js` is a 457485 SINGLE-WITNESS reader; its
  first-mesh path does NOT support 218757. It will NOT be modified. The new
  reader is separate code that adopts the SAME documented parsing discipline
  (R61/iter037 lineage conventions: u32-per-block preamble, sized strings,
  file-order f32 bit hex, loud failure on unknown types/variants); the reuse of
  these documented conventions and their boundary assumptions is labeled in the
  code headers. Existing parser outputs remain REFERENCE EVIDENCE only — the
  adapter validates against input identity + source-bound byte ranges +
  recomputed fingerprints.
- Per contract §7 the SDK loader is NOT invoked and no NiArk factories are
  fabricated; the four opaque Ark blocks stay partially understood/opaque per
  actual field coverage (62-supported/4-opaque ceiling preserved).

## 2. Planned files (the whole run)

### src/pecompat/ — SceneIR + adapter + instances + render conversion
- `src/pecompat/PecTransform.js` — the GB-contract transform math
  (world = parentWorld * local; TRS<->matrix; point application; tolerance
  compare). Pure ES module, no THREE import (Node-testable).
- `src/pecompat/PecSceneIR.js` — the IR: asset record (era/build,
  container/entry/hash, serialized block ids, supported types, decode status),
  node record (serialized local TRS, children, separate resource/property/
  extra-data links), instance record (unique instanceId, asset ref, authored
  transform, scene parent), diagnostics (opaque count, unresolved
  binding/dependency, unsupported feature), computed state (model/file-root
  transform, scene transform, render transform, bounds as DISTINCT quantities).
  Versioned schema id; cache keys = asset hash + adapter/schema version.
- `src/pecompat/PecNif10Reader.js` — extended v10.1.0.0 reader (version gate
  10.1.0.0 exactly, loud otherwise): full hierarchy (all NiNode/NiTriShape
  links validated: dangling/cycle/multi-parent REJECTED + reported), ALL mesh
  blocks preserved (14 for 218757, helper candidates included), serialized TRS
  kept bit-exact, per-block byte ranges recorded, opaque Ark blocks recorded
  with boundaries + decode status, unknown bytes never interpreted.
- `src/pecompat/PecAssetAdapter.js` — Models.bnt pinned entry → payload SHA
  check (pin `3e8a22c2...12cf36`, loud fail) → reader → SceneIR asset record;
  texture binding resolution ONLY via independently reproduced name/property/
  container bindings and explicitly supported slots; unknown/missing → labeled
  untextured material + diagnostic.
- `src/pecompat/PecInstanceBuilder.js` — authored instances: instance wrapper
  OWNS its scene transform while the imported asset hierarchy retains its
  serialized root/child transforms (the viewer policy — explicitly labeled as
  NOT a reproduction of every SDK2.6 root-replacement branch or the original PE
  placement mechanism); attachment/source-transform dependencies kept separate
  from scene parents; resource geometry shareable, transforms/instance ids not.
- `src/pecompat/PecRenderConvert.js` — THREE r185 conversion: render-axis/unit
  conversion applied EXACTLY ONCE, labeled RENDER_ADAPTER_CHOICE /
  PE_UNITS_NOT_CONFIRMED (candidate: (x,z,-y) + ×0.01, same labeled class the
  old compat app used — decision recorded in code + diagnostics), BufferGeometry
  building, wireframe/solid support, bounds fit computation.

### compat/ — ONE local app + its read-only asset API
- `compat/index.html` — single entry (importmap: three 0.185.0 from
  /node_modules, no CDN), mode switch (Asset / Authored scene), diagnostics
  panels, AUTHOR_PLACED_LAB labeling.
- `compat/app.js` — shell: WebGLRenderer, modes, orbit camera + free camera,
  discoverable reset/fit action, HUD.
- `compat/api.js` — read-only asset API client: bounded entry fetches +
  client-side SHA256 cross-check vs server header + provenance display
  (pattern reviewed from eudoria-compat-threejs-r1, rewritten for this app).
- `compat/asset-mode.js` — 218757 asset mode (orbit, fit bounds,
  solid/wireframe, axes, hierarchy inspector, dPVS-name heuristic visibility
  toggle clearly labeled heuristic; total imported vs visible meshes with
  exclusion reasons).
- `compat/scene-mode.js` — authored scene mode: TWO instances of 218757 on an
  EXPLICITLY AUTHORED grid (no terrain integration claimed), change one
  transform without moving the other, per-instance select/inspect.
- `compat/compat.css` — styling.
- `compat/server-sceneir.mjs` — the app's bounded loopback server: static repo
  root (with traversal blocking) for app/three modules + bounded index-derived
  entry endpoints (model/texture entries from the CONFIGURED roots only).
  NO whole-BNT/source-tree static route (the base /pcg/ alias is NOT
  replicated). Binds 127.0.0.1 only.

### tools/pecompat/
- `tools/pecompat/extract_218757.mjs` — CLI extraction + identity print
  (size/SHA vs pin) from the pinned Models.bnt path.
- `tools/pecompat/sceneir_dump.mjs` — CLI SceneIR build + bounded diagnostics
  dump (counts, block coverage, recomputed fingerprints) — no payloads.
- `tools/pecompat/controlB_compare.mjs` — Control B comparison runner:
  fixture NIF → IR → composed probe world position vs native expected values
  (96,202,306)/(58,221,363), tolerance-based.

### tests/pecompat/
- `tests/pecompat/run_tests.mjs` — zero-dependency Node harness (repo style:
  each control prints MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
  WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED).
- `tests/pecompat/transform_composition.test.mjs` — T1 native controls vs IR
  math + T2 nonidentity root + T3 reparenting.
- `tests/pecompat/instance_separation.test.mjs` — T4 two instances, shared
  resource geometry, independent transforms.
- `tests/pecompat/invalid_links.test.mjs` — T5 invalid/missing links, cycles,
  multi-parent (authored synthetic IR cases).
- `tests/pecompat/model_218757.test.mjs` — T7 pinned extraction + ALL 14
  mesh/data association + fingerprint checks (vertex/index SHA256 recomputed
  vs predecessor MODEL_218757_RELATION_RESULTS.json).
- `tests/pecompat/missing_texture.test.mjs` — T6 missing/unknown texture →
  labeled untextured + diagnostic, no false binding.
- `tests/pecompat/witness_457485_regression.test.mjs` — T8: compares
  src/pesource/NifModelReader.js against its BASE hash; if UNCHANGED the test
  reports NOT_APPLICABLE_UNTOUCHED (planned outcome); if changed it runs the
  witness regression battery MANDATORILY.

### .opencode/skills/pe-gamebryo-rosetta/ and docs/pecompat/
- `.opencode/skills/pe-gamebryo-rosetta/SKILL.md` + `references/source-locations.md`
  + `references/integration-rules.md` — adapted from the seed at
  `C:\Users\User\Documents\ChatGPT\PE\OPENCODE_GAMEBRYO_SKILL_RUNTIME_R1_20261009\SEED_SKILL\pe-gamebryo-rosetta`
  (inspected this phase; concise: source/SDK distinctions, transform/instance
  contracts, version gates, commands, limitations; updated with THIS run's
  measured control outcomes).
- `docs/pecompat/SCENEIR.md` — the IR schema + coordinate contract + viewer
  policies (compact, non-proprietary).

### REPORT_REPO_PATH (this package; final files per contract §9)
`AUTHORIZATION_AND_PREFLIGHT.md`, `PLAN_AND_PATH_ALLOWLIST.md` (this file),
`PREREGISTRATION.md`, `INPUT_IDENTITIES.json`, `SOURCE_IDENTITIES.json`,
`CONTROLS_A.json`, `CONTROLS_B.json`, `INTERVENTION_LEDGER.md`, plus in later
phases: `TEST_RESULTS.json`, `COVERAGE_AND_LIMITS.md`, `FINAL_REPORT.md`,
`REVIEW.md`, `EVIDENCE_INDEX.md`, `HANDOFF.md`, `MANIFEST_SHA256.csv`
(generated LAST, self-excluded, physical-file/row bijection verified);
`raw/CONTROL_B/` raw printer logs (not proprietary).

### package.json / package-lock.json
NO dependency changes planned (three 0.185.0 retained). A scripts entry
(e.g. `"test:pecompat"`) is the ONLY anticipated package.json edit, justified
as a script addition; if no edit is needed, package.json stays untouched.

### src/pesource/
NOT modified (no compatible fix currently needed). If a necessary fix becomes
unavoidable, it happens only with the T8 witness regression battery green.

## 3. Planned commands

- Tests (later phases): `node tests/pecompat/run_tests.mjs` (optional
  `--models "D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"`
  to enable T7 against the pinned container; without it T7 reports
  NOT_PERFORMED_CONTAINER_UNAVAILABLE loudly, never silently skipped).
- Control B comparison: `node tools/pecompat/controlB_compare.mjs <fixture.nif> <expected x,y,z>` (later phase, after the IR exists).
- Extraction identity check: `node tools/pecompat/extract_218757.mjs` (later phase).
- Server (later phases; NO server started in THIS phase):
  - Start: `node compat/server-sceneir.mjs` — prints
    `sceneir server http://127.0.0.1:<PORT>/ pid=<PID>`; PORT = env override,
    default 8140, verified FREE at bind (busy → LOUD failure; the user's other
    servers on 8000/8124/8126/8132 are NEVER touched or replaced).
  - Stop: terminate the recorded PID (`Stop-Process -Id <PID>` or Ctrl+C in the
    owning console). PID + liveness recorded in the handoff; no untracked
    writer left behind.
- Publication (final phase ONLY, on the feature branch):
  path-limited `git add` of exactly the planned paths; normal commit; push
  `codex/pe-sceneir-218757-r1-20261009` only (never master, no force, no
  history rewrite); verify local HEAD == origin/BRANCH == remote BRANCH ==
  RESULTING_SHA; master recorded separately.

## 4. Reference inspection (what is reusable vs what must be written fresh)

- `eudoria-compat-threejs-r1` (READ_ONLY; three 0.185.0): REUSE as reviewed
  patterns only — entry-by-entry API + provenance + client-side SHA cross-check
  (api.js), OrbitControls wiring, [P-UNITS]/[P-AXIS] labeled conversion
  discipline, DataTexture flipY=false conventions, loud-failure load UX. Its
  model mode renders the SINGLE witness mesh only — the multi-mesh hierarchy,
  instance wrapper, inspector and authored scene are WRITTEN FRESH (its
  chain is the proven pattern, not a drop-in).
- `tools/pe_asset_viewer_v4` (READ_ONLY; vendored Three.js r169): inspector UI
  patterns only. Its GLB/catalog data path is from the historical
  nif_parser lineage and is NOT automatically PCG-byte-equivalent (contract
  warning) — 218757 comes from the pinned Models.bnt bytes; nothing from its
  GLB exports is reused. r169-specific APIs brought across would need
  reviewed differences vs 0.185.0.
- `eudoria-web` (READ_ONLY; vendored Three.js REVISION '169'): legacy game
  runtime; NOT compatible with the base's 0.185.0 stack without broad work.
  Terrain integration is optional per contract §7 — the app uses an
  EXPLICITLY AUTHORED grid; no Eudoria terrain/placement success is
  manufactured.
- Base repo test setup (inspected): zero-dependency Node probe scripts
  (`tools/*.js`) + Python control batteries
  (`tools/gamebryo_oracle/tests/test_gb12.py --self`) are the established
  style; `tests/pecompat/` follows the Node-script style so NO new package
  dependency is introduced.

## 5. Honest-boundary notes carried into the implementation

- No historical placement: scene coordinates labeled AUTHOR_PLACED_LAB;
  HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
- Camera bound centers (96,202,306)/(58,221,363) are control-only values; not
  generalized to geometry pivots.
- dPVS/occluder-like names are hints, not proven runtime roles; meshes stay
  addressable with a clearly labeled heuristic visibility toggle.
- The nine-byte Ark texture tail is used ONLY through the already-canon
  name/property/container binding; NO new tail semantics derived.
- Unsupported attachment/animation/LOD execution is surfaced as diagnostics,
  not silently dropped.
