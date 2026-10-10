# PREREGISTRATION — PE_WORLD_LAUNCHER_R1_20261010

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = SETUP_AND_ETAP_A (worktree setup + preflight + CAM-C1/C2/C3 corrections + Focused QC A)
WRITTEN_AT = 2026-10-10 (BEFORE the CAM corrections and the focused QC executions)
REGISTRATION_DISCIPLINE = expectations recorded BEFORE the work; not corrected to match obtained results. Predictions that fail at execution are reported as failures with their measured values.

## 0. Scope gate of this phase

- This phase implements contract §2 (Etap A: CAM-C1, CAM-C2, CAM-C3) + Focused QC A + the
  preflight artifacts. Etapy B–E (launcher, terrain, textures, vegetation, browser smoke)
  are LATER phases of this run — NOT executed here.
- No commit/push in this phase (persistence is a later phase, explicitly not authorized yet
  beyond the branch-scoped implementation authorization recorded in
  AUTHORIZATION_AND_PREFLIGHT.md).
- Historical f71eb30 packages (repo docs/audits/PE_CITY_ASSET_MAP_R1_20261010 + private
  99_Audits/PE_CITY_ASSET_MAP_R1_20261010) are READ_ONLY inputs. Corrections live in THIS
  package (docs/audits/PE_WORLD_LAUNCHER_R1_20261010/).

## 1. CAM-C1 — GLB comparison expectations (the retraction)

Standing claim RETRACTED: `NO_GLB_PRESENT_FOR_THESE_IDS` (f71eb30 package:
DEEP_ANALYSIS.md §5, REPORT.md, LIMITATIONS.md — historical, read-only). The four GLB
comparison inputs physically exist at
`D:\Eudoria_Reconstruction\12_WebGame\tools\pe_asset_viewer_v4\assets\converted\static\<id>_complete_textured.glb`
(READ_ONLY comparison inputs; pins re-verified by me — see INPUT_IDENTITIES.json).

Registered BEFORE the work — method and expectations:

- METHOD: re-decode the four CD_2003 primaries from the pinned Models.ark payloads with the
  EXISTING production reader (tools/pecompat/nif41_deep.mjs readNif41/analyzeNif41Model,
  fail-closed PRIMARY_PINS + container pin), then compare against the GLB
  POSITION/indices accessors after the EXPLICIT conversion `(x,y,z) -> (x,z,-y)` applied
  exactly ONCE to the original NIF vertex positions.
- COMPARISON UNIT: multiset of float32 vertex positions; multiset of UNORIENTED geometric
  triangles (each triangle = its 3 position keys, canonicalized — orientation/winding
  deliberately ignored). Original file units everywhere (never meters).
- TOLERANCE: bit-exact float32 equality is EXPECTED for a pure axis shuffle (no arithmetic);
  the measured mismatch counts and max abs delta are reported whatever they are. A
  non-zero result is NOT massaged into a pass.
- EXPECTED (from the independent Desktop post-audit, pinned REPORT.md §2/§3): for all four
  models, converted position multisets and unoriented triangle multisets are EXACTLY equal.
- EXPECTED counts (Desktop post-audit table, to be re-measured by my own reader, not
  assumed): 192374: 4 geoms / 2400 verts / 1200 tris; 193207: 2 / 1698 / 864;
  193313: 5 / 2384 / 1192; 193684: 8 / 2680 / 1340; all local TRS identity; 0 UV sets per
  geometry in the ORIGINAL NIF.
- REGISTERED LIMITS OF THE COMPARISON (must appear in the disposition verbatim):
  1. Unoriented triangle agreement does NOT confirm winding, materials, or the converter
     execution lineage (which script produced these GLBs is NOT established by agreement).
  2. The `_textured.glb` FILENAME is NOT proof of textures. The ORIGINAL NIFs have 0 UV
     sets and 0 texture bindings; the four models remain UNTEXTURED_PROXY. No random
     textures may be attached.
  3. The GLB JSON carries exporter-side TEXCOORD_0/NORMAL attributes; that is a property of
     the GLB artifacts, not evidence of original-texture binding. The GLBs' `images` count
     is expected 0 (Desktop: "Wszystkie GLB mają zero images") — re-measured per file.
- PASS GATE (CAM-C1): 4/4 GLB pins verified; 4/4 comparisons executed with method/tolerance/
  unit recorded; per-model verdicts recorded; the retraction recorded in
  CAM_C1_C2_C3_DISPOSITION.md; NO claim made about winding/materials/lineage.

## 2. CAM-C2 — FAILED is not a measurement (expected schema + baseline CONTROL)

Defect (Desktop post-audit §4, RUNTIME_CHECKS.json): in
tools/pecompat/catalog_data.mjs the mere presence of a `_batch` cache row yields
`complexity.unknown=false` (even for status FAILED with null triangles/vertices/…) and the
row text says "NO_RECORDED_EDGES (decoded but …)". Coverage counted those 3270 FAILED rows
as measured complexity (4842 instead of 1572).

Registered corrections (implemented in the SAME shared data model used by API/UI/tests):

1. A SHARED decode-status model: metrics (`complexity.unknown=false`) require a genuinely
   successful proper decode with real values. Specifically:
   - `DECODED` (identity-verified cache row) with COMPLETE numeric metrics → measured.
   - `DECODED_NO_MESH_GEOMETRY` with REAL zeros → measured (real zero ≠ UNKNOWN).
   - `FAILED` → complexity UNKNOWN, with the failure reason (never counted as measured).
   - `VERSION_GATED` / no cache row → UNKNOWN (unchanged).
   - Defensive: any status whose numeric fields are missing/null → UNKNOWN with reason
     (no promotion).
2. textureCoverage for FAILED rows → UNKNOWN/not-decoded wording (never "decoded but …").
3. Coverage recomputed from the records through the SAME shared status definition; the
   coverage object gains a per-status measured breakdown so no aggregate hides a class.
4. Entries/models/textures/extent/complexity stay SEPARATE: 21,302 = total entries of the
   four archives (models 2492+5596; textures 4833+8381); 8,088 = model catalog rows;
   complexity measured is a THIRD, separate census.

BASELINE CONTROL (registered BEFORE re-measurement; NOT a hardcode): on UNCHANGED inputs
(the pinned containers + the pinned private caches + the same primary decode) the corrected
complexity-measured count is expected to equal the Desktop baseline 1572 = PCG 1568
(1551 DECODED + 17 DECODED_NO_MESH) + CD 4; unknown 6516; FAILED 3270 stays 3270 in the
decode-coverage census (FAILED rows still EXIST as rows with honest FAILED status — the
fix changes their metrics/texture wording and the measured count, not their existence).
The production code must NOT hardcode 1572 anywhere; the number is recomputed from records.
My focused QC recomputes it and compares to 1572 as a CONTROL (a mismatch is a FAIL, not a
tuning knob).

Expected effect on the coverage object: `complexity.measured` 4842 → 1572 (measured);
`complexity.unknown` 3246 → 6516. UI regression note: compat/catalog-table.js renders
`complexity.unknown` rows as UNKNOWN badges and nulls as UNKNOWN — the FAILED rows moving
to `unknown:true` is UI-compatible by construction (registered expectation).

## 3. CAM-C3 — full cache identity in the PRODUCTION load path

Defect (Desktop post-audit §5, CACHE_IDENTITY_CONTROLS.json): the policy comment promised
`era + container SHA + entry name + payload SHA`, but the batch attach key was only
`name|payloadSha256`, the original batch schema has NO containerSha256, and the texture
edges aggregate keyed on model name + `_batch` presence without era verification. Three
in-memory mutants (wrong batch era; wrong batch containerSha256=64 zeros; wrong edges era)
were all ACCEPTED by the f71eb30 gate.

Registered corrections (all in tools/pecompat/catalog_data.mjs — the PRODUCTION data model
consumed by compat/server-catalog.mjs, the API, the UI and the tests; NOT a side script):

1. The cache attach gains a REQUIRED identity ENVELOPE declared by the production caller
   (`cacheIdentity` opt) and VERIFIED against the regenerated catalog:
   - `era` must equal PCG_9_3_5 (the only era the pinned phase-2/phase-3 caches belong to);
   - `containerSha256` must equal the fail-closed-pinned PCG Models.bnt container SHA
     (verified against the regenerated catalog, which itself re-verifies the pin at load);
   - `readerVersion` must equal PEC_NIF10_READER_VERSION ('pec-nif10-reader-v1');
   - `schemaVersion` must equal PEC_SCENEIR_SCHEMA_VERSION ('pec-sceneir-v1').
   A cache path provided WITHOUT a declared envelope → CONTROLLED REFUSAL of that cache
   (attached=0, state=REFUSED, disclosed reason — never a crash, never a silent attach).
   A declared envelope that fails verification → same controlled refusal with the named
   reason. (Missing-envelope refusal is fail-closed and preserves the REGENERATION-FIRST
   property: the catalog itself is always rebuilt from the pinned originals.)
2. PER-ROW identity checks (batch state): row `era`, `readerVersion`, `schemaVersion` must
   match the verified envelope values; a row-level `containerSha256` field (absent in the
   original schema) if PRESENT must match the envelope container SHA; `name`+`payloadSha256`
   must match the REGENERATED catalog (existing check, kept). Any violation or missing
   mandatory field → that row is DROPPED with a counted, named reason (never silently
   used). Rows lacking per-row containerSha256 inherit the container identity from the
   VERIFIED envelope — documented: per-row payload-SHA agreement with the regenerated
   pinned-container rows is the 256-bit per-row proof, so a deleted field cannot cause
   cross-container contamination.
3. PER-MODEL identity checks (texture edges): the edge rows' `era` must match the envelope
   era; the per-model aggregate is attached ONLY IF the model's batch row passed identity
   (existing) AND EVERY edge row of that model passes identity — any identity-violating
   edge row refuses that model's whole aggregate (all-or-nothing per model; a partial
   aggregate would be a contaminated measurement).
4. The four primary MODEL caches stay REGENERATION-FIRST (live decode from pinned
   payloads; container+payload pins re-verified at every read) — unchanged; the wire
   cacheKey gains the missing containerSha256 + entryName identity components.
5. `CATALOG_DATA_VERSION` is bumped (schema change) so downstream consumers can detect the
   corrected data model.

Registered mutant expectations (Focused QC A, through the REAL production
buildCatalogData with in-memory io mutation of cache metadata ONLY — physical caches
unchanged, proven by hash before/after; method mirroring the Desktop control):

- M1 wrong_batch_era (subject row era → CD_2003): EXPECT REFUSED — the subject row is
  dropped with reason ROW_ERA_MISMATCH; its extent/complexity become UNKNOWN; the identity
  mismatch counters increment; NO crash.
- M2 wrong_batch_container_sha (subject row containerSha256 → 64 zeros): EXPECT REFUSED —
  dropped with reason ROW_CONTAINER_SHA_MISMATCH.
- M3 wrong_edges_era (all edge rows of the subject model → CD_2003): EXPECT REFUSED — the
  subject model's edge aggregate is dropped (modelsDroppedIdentityMismatch increments);
  the model's textureCoverage becomes EDGE-REFUSED/UNKNOWN wording, not a name-edge census.
- CLEAN (no mutation, production envelope): the SAME gate must PASS — caches attach with
  the known-good counts (batch attached 4838; edges modelsAttached 1545; both
  droppedIdentityMismatch 0).
- Explicitly registered: these synthetic counterexamples are NOT proof of historical
  contamination of the f71eb30 published run (the Desktop audit itself proved only the
  false fail-closed claim; no actual cross-era use was observed). This must be stated in
  the disposition.

## 4. Terrain/materials/vegetation invariants (registered for the LATER phases; the
phase-1 code I touch must NOT regress them)

- TDF: 32x32 uint16 LE; heights at payload offset 64..2111; bytes 52..63 are a separate
  sub-header (offset 52 is the KNOWN-WRONG variant; any later terrain test must include
  64-vs-52 as a negative control); 1024 raw heights per tile; raw u16 preserved (no 8-bit
  normalization, no smoothing, no seam hiding); sentinel `7ffe7ffe.tdf` is NOT a regular
  tile; NODATA ≠ height 0.
- CURRENT_RUNTIME_CALIBRATION labels (u16/128, 2 spatial units/sample, identity min/max,
  adapter axes) are runtime calibration labels, NOT historical engine facts — they stay
  explicitly labeled wherever used.
- Materials: named material record mask at record+56 (fields 52..55 are NOT mask); raw/RLE
  sizes, order, exact consumption, independent weights preserved; layer sums >255 do NOT
  authorize normalizing source masks.
- Vegetation: `.vcl` strict decoder rejects 25.vcl comma tokens → controlled UNSUPPORTED
  (never comma-converted to force a PASS); deterministic seed hashing; same
  source+era+profile+seed+calibration+tile key → identical instance set.

## 5. Browser-smoke gate classes (registered for the LATER phases)

- DATA_VALIDATED / APP_LOAD / PIXEL_RENDER / INTERACTION_VERIFIED are SEPARATE classes.
- INTERACTION is expected NOT_PERFORMED while the playwright automation daemon (port 9222)
  is DOWN (measured in the preflight census); honest NOT_PERFORMED, never PASS-by-default.
- Etap A note (registered): Cam-A failures must NOT be masked by later rendering success —
  the launcher phases that consume the catalog must surface catalog/cache errors honestly;
  the corrected gates make cache refusal visible in the API status (state + counters +
  reasons), which later phases must display, not swallow.

## 6. Focused QC A — registered pass/fail predicate (this phase)

FOCUSED_QC_A passes iff ALL of:
1. CAM-C1: 4/4 GLB pins verified + 4/4 comparisons executed + verdicts recorded (regardless
   of the comparison OUTCOME, which is reported as measured — but a mismatch vs the
   Desktop's exact-agreement result would be a finding to report, not to hide).
2. CAM-C2: coverage recomputed from records through the shared status definition; measured
   count on unchanged inputs == 1572 baseline CONTROL; FAILED rows are unknown-complexity
   with reason; no "decoded but" wording on FAILED.
3. CAM-C3: the three mutants REFUSED through the REAL production loader with named reasons
   and incremented counters; clean passes the SAME gate with known-good attach counts.
4. Regression spot: catalog battery (33 prior gates) + unit battery (24) + app battery (22)
   green after the corrections (the corrected tests updated only where the corrections
   require them to declare the production envelope; NO assertion weakened).
5. No catalog error is masked downstream: the /api/catalog/status snapshot shows the cache
   state honestly (spot-checked through the real server in the battery).

A failure in any of these is a finding — reported honestly as PARTIAL/BLOCKED with the
measured values, never smoothed into a pass.
