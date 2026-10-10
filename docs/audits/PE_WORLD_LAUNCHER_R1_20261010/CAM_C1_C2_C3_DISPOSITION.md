# CAM_C1_C2_C3_DISPOSITION — PE_WORLD_LAUNCHER_R1_20261010, Etap A

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = SETUP_AND_ETAP_A
FINDING SOURCE = the pinned Desktop post-audit
`C:\Users\User\Documents\ChatGPT\PE\CITY_ASSET_MAP_F71_POST_AUDIT\REPORT.md`
(12694 B / SHA256 5F007CDB… — pin verified) + its evidence files
(RUNTIME_CHECKS.json / CACHE_IDENTITY_CONTROLS.json — hashes in INPUT_IDENTITIES.json).
CORRECTION PACKAGE = THIS run (branch codex/pe-world-launcher-r1-20261010, built from
e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c per the recorded BASE_DECISION — see
AUTHORIZATION_AND_PREFLIGHT.md §3, cited here as required: the RESULT_BRANCH is built from
the current authorized head e9bb1f5, which contains the contract's EXPECTED_BASE f71eb30a in
ancestry; the single-commit delta is the human-authorized CAMERA_UX_FIX).
HISTORICAL f71eb30 PACKAGES = READ_ONLY (repo docs/audits/PE_CITY_ASSET_MAP_R1_20261010 and
private 99_Audits/PE_CITY_ASSET_MAP_R1_20261010) — the retraction/corrections live HERE.

## 0. Summary

| Finding | Old standing claim (f71eb30) | Correction | Measured result |
|---|---|---|---|
| CAM-C1 | NO_GLB_PRESENT_FOR_THESE_IDS — comparison SKIPPED | RETRACTED; the four pinned GLBs exist; comparison executed | 4/4 EXACT_AGREEMENT (positions + unoriented triangles, after explicit (x,z,-y)) |
| CAM-C2 | FAILED rows counted as measured complexity (4842) | Shared status model; FAILED never measured | measured 1572 / unknown 6516 (baseline control MATCH) |
| CAM-C3 | "identity-keyed cache" promise not enforced (3 mutants accepted) | Full envelope + per-row/per-model identity gates in the production path | 3/3 mutants REFUSED with named reasons; clean passes the SAME gate |

ALL THREE corrections verified by the Focused QC A suite
(tests/pecompat/catalog_cam_fixes.test.mjs) through the REAL production paths; the full
regression batteries are green (catalog 41 PASS incl. the prior 33; unit 24 PASS; app 22
PASS — see §4).

## 1. CAM-C1 — GLB availability and comparison (P2 → CORRECTED)

**Old claim (historical, read-only):** `NO_GLB_PRESENT_FOR_THESE_IDS` — "no GLB exists for
192374/193207/193313/193684 anywhere in the searched trees; numeric comparison SKIPPED"
(DEEP_ANALYSIS.md §5, REPORT.md, LIMITATIONS.md). The f71eb30 executor's depth-6 tree search
missed the files in `tools/pe_asset_viewer_v4/assets/converted/static/` (it reported only the
16 GLBs of `assets/cd2003/`).

**Correction:** the standing claim is RETRACTED in this package. The four GLB comparison
inputs exist and are PIN-VERIFIED (own measurement, fail-closed in the tool):

| ID | GLB size B | GLB SHA256 | pin |
|---|---:|---|---|
| 192374 | 94,484 | 8af713e0af150b3edab69affbb0121c55685f883054a0db692c4838d0982e3ea | MATCH |
| 193207 | 66,476 | 4f8c7c5ba652fbcca6c01a02f4ac76a3cdc56eed5314aa1044f4fcf870c19b85 | MATCH |
| 193313 | 94,644 | da1a15bf8d7a04be006b5804b12dff2c282123562cd00189561b0d160e6c1243 | MATCH |
| 193684 | 108,192 | 6b96c12763c80bc693361924e1eaa1bab16b5bd2daba7908e3fcb86c62ec2efc | MATCH |

**Method (preregistered in PREREGISTRATION.md §1):**
- ORIGINAL side: fresh re-decode of the four CD_2003 primaries from the pinned READ_ONLY
  Models.ark payloads with the EXISTING production phase-3 reader
  (tools/pecompat/nif41_deep.mjs readNif41/analyzeNif41Model), after fail-closed container
  (f660d055…) + payload (PRIMARY_PINS) verification. (The alternative — reusing the prior
  run's stored decoded arrays — was not taken: a fresh decode keeps this package independent
  of historical private artifacts.)
- GLB side: independent bounded glTF 2.0 binary parse (tools/pecompat/cam_c1_glb_compare.mjs;
  JSON+BIN chunks; Draco refused loudly — not present; POSITION float32 VEC3 + u16/u32
  indices per primitive; generator "PE ArkVFS Exporter" recorded).
- Conversion: the EXPLICIT `(x,y,z) -> (x,z,-y)` applied ONCE to the original NIF vertex
  positions (no scaling, no further axis arithmetic; `-y` negated in float space).
- Comparison unit: multiset of float32 vertex positions (bit-exact keys) + multiset of
  UNORIENTED geometric triangles (3 sorted position keys; winding/orientation deliberately
  ignored). Original file units everywhere (never meters).
- Tolerance: bit-exact float32 equality expected for a pure axis shuffle; mismatch counts +
  max abs delta reported as measured, never massaged.

**Results (measured, 2026-10-10, raw/CAM_C1_GLB_COMPARE.json):**

| Model | NIF geoms/verts/tris | GLB prims/verts/tris | positions multiset | unoriented triangles | verdict |
|---|---|---|---|---|---|
| 192374 | 4 / 2400 / 1200 | 4 / 2400 / 1200 | EXACT (0 mismatch keys) | EXACT | EXACT_AGREEMENT |
| 193207 | 2 / 1698 / 864 | 2 / 1698 / 864 | EXACT | EXACT | EXACT_AGREEMENT |
| 193313 | 5 / 2384 / 1192 | 5 / 2384 / 1192 | EXACT | EXACT | EXACT_AGREEMENT |
| 193684 | 8 / 2680 / 1340 | 8 / 2680 / 1340 | EXACT | EXACT | EXACT_AGREEMENT |

Supporting measurements: converted-NIF bounds == GLB POSITION bounds on all four (identical
min/max per component); all local TRS identity (9/9, 5/5, 11/11, 17/17 — matches the Desktop
table); 0 invalid indices; per-geometry/per-primitive counts match 1:1.

**EXPLICIT LIMITS OF THIS COMPARISON (standing, must accompany any use of the result):**
1. Unoriented triangle agreement does NOT confirm winding, materials, or the converter
   execution lineage (which script produced the GLBs is NOT established by agreement — the
   generator string alone proves nothing).
2. The `_textured.glb` FILENAME is NOT proof of textures. The ORIGINAL NIFs have **0 UV
   sets** (measured per geometry) and 0 texture bindings; the four models remain
   **UNTEXTURED_PROXY**. NO random textures may be attached.
3. The GLBs carry exporter-side TEXCOORD_0/NORMAL attributes on every primitive (measured) —
   artifacts of the GLB export, NOT evidence of original-texture binding; the GLBs' `images`
   census is **0** on all four (measured — agrees with the Desktop observation).

**Residuals:** none open for CAM-C1 in this scope. The historical files stating the old
claim remain untouched (READ_ONLY) — this disposition is the standing correction.

## 2. CAM-C2 — FAILED is not a measurement (P2 → CORRECTED)

**Old defect (f71eb30, tools/pecompat/catalog_data.mjs):** the mere presence of an
identity-attached `_batch` cache row yielded `complexity.unknown=false` even for status
FAILED (all metrics null), FAILED rows received the text "NO_RECORDED_EDGES (decoded but
…)", and the coverage counted them as measured: 4842 "measured" complexity = 1572 real +
3270 FAILED (Desktop RUNTIME_CHECKS.json reproduction).

**Correction (tools/pecompat/catalog_data.mjs, same shared data model for API/UI/tests):**
- ONE shared status model, exported: `complexityFromBatchRow(row)` builds the canonical
  complexity object; `isComplexityMeasured(complexity)` is the shared predicate.
  - `FAILED` → `{ unknown: true, note: 'decode FAILED — not a measurement …; reason: <the
    loud-failure reason>' }` — never counted, never "decoded".
  - `DECODED` with COMPLETE numeric metrics (triangles/vertices/shapes/nodes/blocks all real
    numbers) → measured; incomplete numerics → UNKNOWN (defensive, no promotion).
  - `DECODED_NO_MESH_GEOMETRY` with REAL zeros → measured (a real zero is NOT UNKNOWN).
  - no cache row → UNKNOWN (VERSION_GATED, unchanged).
- textureCoverage follows the same model: FAILED → "UNKNOWN (decode FAILED — texture edges
  were never produced; not decoded)"; DECODED without edges → "NO_RECORDED_EDGES (decoded;
  …)"; DECODED_NO_MESH → "NO_RECORDED_EDGES (decoded, no mesh geometry blocks — …)".
  The "decoded but …" wording no longer exists for FAILED rows.
- Coverage is recomputed from the records through `isComplexityMeasured` (no separate
  definition) and gains `measuredByStatus` so no aggregate hides a class.
- The censuses stay SEPARATE: 21,302 = total entries of the four archives (models 2492 +
  5596; textures 4833 + 8381 — entry-level, cross-checkable in the container stats);
  8,088 = model catalog rows; complexity measured is a THIRD census.

**Measured result (unchanged pinned inputs, REAL production build, suite
CAM_C2_C3_CLEAN_BASELINE + CAM_C2_SHARED_STATUS_MODEL):**

```text
coverage.complexity.measured   = 1572  (baseline control 1572 — MATCH; PCG 1568 = DECODED 1551 + DECODED_NO_MESH 17, + CD 4)
coverage.complexity.unknown    = 6516  (baseline control — MATCH)
measuredByStatus               = { DECODED_FULL_CLOSURE: 4, DECODED: 1551, DECODED_NO_MESH: 17 }
byDecodeCoverage.FAILED        = 3270  (unchanged — FAILED rows still exist, honestly FAILED)
FAILED rows: 3270/3274? no — 3270/3270 all complexity.unknown=true, null metrics, FAILED reason kept
FAILED rows texture coverage   = "UNKNOWN (decode FAILED — …)" on all 3270
```

The 1572 baseline is a CONTROL (Desktop RUNTIME_CHECKS.json), NOT hardcoded anywhere in
production code — the number is recomputed from records at every build; the Focused QC gate
compares the recomputed value against the control and would FAIL on disagreement.

**Where the shared status definition is used:** row building (buildCatalogData), the
coverage count (same module), the UI (compat/catalog-table.js renders `complexity.unknown`
→ UNKNOWN badge; nulls → UNKNOWN badge — no UI change needed, verified by
CAT_UNK_BADGE_RENDER), and the tests (both the prior gates and the new focused QC import
the same predicate). UI regression: FAILED rows now render as UNKNOWN complexity — the
honest rendering the UNKNOWN discipline always intended.

**Residuals:** none open. The false 4842 and the "decoded, no texture edges" for FAILED are
gone from the production path, the API and the UI.

## 3. CAM-C3 — full cache identity (P2 → CORRECTED)

**Old defect (f71eb30):** the policy comment promised
`era + container SHA + entry name + payload SHA`, but the batch attach key was only
`name|payloadSha256`, the original batch schema carries NO per-row containerSha256, and the
texture-edge aggregate keyed on model name + `_batch` presence without era verification.
Three in-memory mutants (wrong batch era; wrong batch containerSha256 = 64 zeros; wrong
edges era) were all ACCEPTED by the f71eb30 gate (Desktop CACHE_IDENTITY_CONTROLS.json).

**Correction (tools/pecompat/catalog_data.mjs — the PRODUCTION data model consumed by
compat/server-catalog.mjs, the API, the UI and the tests; NOT a side script):**
1. **Envelope, declared + verified:** the cache attach requires a caller-DECLARED identity
   envelope (`cacheIdentity` opt; `productionCacheIdentity()` exported for the production
   caller), verified against the regenerated catalog: era must be PCG_9_3_5; containerSha256
   must equal the fail-closed-pinned PCG Models.bnt SHA (c950a8c2…); readerVersion must equal
   PEC_NIF10_READER_VERSION ('pec-nif10-reader-v1'); schemaVersion must equal
   PEC_SCENEIR_SCHEMA_VERSION ('pec-sceneir-v1').
   - cache path WITHOUT a declared envelope → the whole cache is REFUSED
     (state `REFUSED: CACHE_IDENTITY_ENVELOPE_MISSING`, attached=0, disclosed in
     /api/catalog/status — fail-closed default, never a crash, never a silent attach);
   - declared envelope failing verification → REFUSED with the named reason
     (CACHE_ENVELOPE_ERA_MISMATCH / _CONTAINER_MISMATCH / _READER_VERSION_MISMATCH /
     _SCHEMA_VERSION_MISMATCH).
2. **Per-row identity (batch state):** era, readerVersion, schemaVersion, name+payloadSha256
   must match; a row-level containerSha256 (absent in the original schema) if PRESENT must
   match the envelope. Any violation or missing mandatory field → the row is DROPPED with a
   named, counted reason (ROW_ERA_MISMATCH, ROW_CONTAINER_SHA_MISMATCH,
   ROW_READER_VERSION_MISMATCH, ROW_SCHEMA_VERSION_MISMATCH, ROW_IDENTITY_FIELD_MISSING:*,
   ROW_NOT_IN_REGENERATED_CATALOG, ROW_UNPARSEABLE_JSON). Documented: rows lacking the
   per-row containerSha256 inherit the container identity from the VERIFIED envelope; the
   per-row payload-SHA agreement with the regenerated pinned-container rows is the 256-bit
   per-row proof, so a deleted field cannot cause cross-container contamination.
3. **Per-model identity (texture edges):** edge rows' era must match the envelope; the
   per-model aggregate is ALL-OR-NOTHING (a single identity-violating edge row refuses the
   model's whole aggregate with reason EDGE_ERA_MISMATCH / EDGE_CONTAINER_SHA_MISMATCH /
   … — a partial aggregate would be a contaminated measurement); edges attach only to models
   whose batch row passed identity with status DECODED (EDGE_MODEL_BATCH_ROW_MISSING /
   EDGE_MODEL_NOT_DECODED otherwise).
4. **Model-wire cache identity:** `primaryWireCacheKey(id)` is the single source of truth —
   era | container SHA | entry name | payload SHA | reader version | wire version
   (CATALOG_WIRE_VERSION bumped to pec-catalog-wire-v2); the server's lazy wire cache keys on
   the wire's OWN full key (the old server key was a partial `catalog-wire-v1|era|payloadSha`).
5. `CATALOG_DATA_VERSION` bumped to 'pec-catalog-data-v2-camfixes' (schema change); the
   server version string discloses the corrections; startup log prints the cache envelope
   states + attach/drop counters, and flags REFUSED caches loudly (Cam-A errors must not be
   masked by rendering success).

**Measured results (Focused QC A, through the REAL production buildCatalogData; mutants =
in-memory metadata mutations ONLY, physical caches proven byte-identical before/after by
hash witness — the same method as the Desktop control):**

| Gate | Input | Expected | Measured |
|---|---|---|---|
| clean | production envelope, unmutated caches | attach 4838 / 1545, 0 drops, measured 1572 | PASS — batch attached 4838, edges 1545, drops 0, envelopes VERIFIED, measured 1572 |
| M1 | subject 508854.nif batch row era → CD_2003 | REFUSED | PASS — droppedIdentityMismatch=1, reason ROW_ERA_MISMATCH, subject → VERSION_GATED (extent/complexity UNKNOWN), no crash |
| M2 | subject batch row containerSha256 → 64 zeros | REFUSED | PASS — drop reason ROW_CONTAINER_SHA_MISMATCH, subject → VERSION_GATED |
| M3 | ALL edges of subject → era CD_2003 | REFUSED | PASS — modelsDropped=1 reason EDGE_ERA_MISMATCH, subject textureCoverage = EDGE_AGGREGATE_REFUSED; the DECODED extent/complexity stay attached (only the contaminated aggregate refused) |
| default | cache paths, NO envelope declared | REFUSED whole | PASS — both caches REFUSED: CACHE_IDENTITY_ENVELOPE_MISSING, attached 0, catalog still builds from the pinned originals, measured complexity falls to 4 (the live-decoded primaries) |
| witness | physical cache hashes before/after | unchanged | PASS — byte-identical |

**EXPLICIT STATEMENT (standing):** these synthetic counterexamples are NOT proof of
historical contamination of the f71eb30 published run — the Desktop audit proved only that
the declared fail-closed gate was false (no actual cross-era use was observed). The corrected
gates prevent such use going forward; they do not rewrite history.

**Residuals:** none open in this scope. The envelope is caller-declared (the historical
cache files are READ_ONLY and carry no containerSha field); its verification against the
regenerated fail-closed-pinned catalog is the enforcement point — recorded here as a
documented design decision, not hidden.

## 4. Focused QC A + regression spot (measured 2026-10-10)

Focused QC A = tests/pecompat/catalog_cam_fixes.test.mjs (8 gates) — ALL PASS after the
two test defects found by the FIRST battery run were fixed (see INTERVENTION_LEDGER.md):
CAM_C1_GLB_COMPARISON (fresh tool execution, 4/4), CAM_C2_SHARED_STATUS_MODEL (unit),
CAM_C2_C3_CLEAN_BASELINE (1572 control), CAM_C3_M1/M2/M3 (mutants refused),
CAM_C3_NO_ENVELOPE_REFUSED (fail-closed default), CAM_C3_PHYSICAL_CACHES_UNCHANGED
(hash witness).

Regression spot (the standing batteries, unweakened):

| Battery | Result | Note |
|---|---|---|
| catalog battery (`run_catalog_tests.mjs`, full inputs, raw dir = THIS package) | **41 PASS / 0 FAIL / 0 NOT_PERFORMED** | 33 prior gates all PASS + 8 new CAM gates; 2 real-browser T9 LOAD gates through the fixed 5-conjunct gate; suite servers stopped + ports freed |
| unit battery (`run_tests.mjs --models <Models.bnt>`) | **24 PASS / 0 FAIL / 0 NOT_PERFORMED** | matches the f71eb30-era baseline exactly |
| app battery (`run_app_tests.mjs --models <Models.bnt>`) | **22 PASS / 0 FAIL / 0 NOT_PERFORMED** | the 218757 viewer regression-free |

Standing servers untouched and alive: 8140/PID 21288, 8161/PID 9588 (plus pre-existing
8000/PID 6040); port 8162 remains free for the launcher phases; no test process left
running (port-freed proofs in the summaries).

Cam-A masking policy (for the later launcher phases): the corrected gates make cache
refusals visible in /api/catalog/status (envelope states, attach/drop counters, named
reasons) and the server startup log — the phases that consume the catalog must surface
these, not swallow them; the focused QC gates assert exactly that visibility.

## 5. Changed-path census (this phase; pre/post hashes in INPUT_IDENTITIES.json + ledger)

```text
M  tools/pecompat/catalog_data.mjs            (CAM-C2 shared status model + CAM-C3 envelope/row/model gates + wire key + version bump)
M  compat/server-catalog.mjs                  (declare the production envelope; full wire cache key; honest cache-state startup log; version label)
M  tests/pecompat/run_catalog_tests.mjs       (battery gains the Focused QC A suite)
M  tests/pecompat/catalog_unknown_sort.test.mjs     (declare the production envelope in the live build; no assertion weakened)
M  tests/pecompat/catalog_bounds_countercheck.test.mjs (same)
M  tests/pecompat/catalog_preview_math.test.mjs      (same)
M  tests/pecompat/catalog_archive_safety.test.mjs    (same)
A  tools/pecompat/cam_c1_glb_compare.mjs      (CAM-C1 comparison tool; pinned inputs; fail-closed)
A  tests/pecompat/catalog_cam_fixes.test.mjs  (Focused QC A suite)
A  docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (this package: preflight, disposition, ledger, raw evidence)
```

src/pesource, src/pecompat, src/peworld: UNTOUCHED (the corrections required no reader
changes — recorded per the minimal-touch rule). The 218757 app files: UNTOUCHED (app
battery green). Historical packages: READ_ONLY (the harnesses were run with --raw-dir into
THIS package; nothing was written into PE_CITY_ASSET_MAP_R1_20261010).
