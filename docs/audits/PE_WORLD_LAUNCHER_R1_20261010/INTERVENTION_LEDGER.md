# INTERVENTION_LEDGER — PE_WORLD_LAUNCHER_R1_20261010

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
LEDGER_OPENED = 2026-10-10 (PHASE 1: SETUP_AND_ETAP_A)
FORMAT = append-only per phase; every intervention gets an ID, the touched path, the
reason, and the measured outcome. Interventions that were found-and-fixed DURING the phase
(failed first attempts) are recorded as such — they are evidence of the QC working, not
things to hide.

## I-1 — worktree + branch creation (Task 1)

- PATHS: none in-repo (git worktree metadata in the canonical repo
  D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean — the ONLY write to that repo this
  phase, exactly the authorized `git worktree add`).
- ACTION: created D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1 on new branch
  codex/pe-world-launcher-r1-20261010 from e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c
  (BASE_DECISION — recorded + independently verified in AUTHORIZATION_AND_PREFLIGHT.md §3;
  f71eb30a ancestry confirmed; delta = exactly one commit, the human-authorized
  CAMERA_UX_FIX).
- OUTCOME: HEAD e9bb1f5, branch correct, status clean, prior stack present. No foreign
  worktree, untracked file or server touched (port census before/after identical).

## I-2 — CAM-C2 + CAM-C3 corrections in the production data model

- PATHS: tools/pecompat/catalog_data.mjs (M), compat/server-catalog.mjs (M).
- REASON: Desktop post-audit §4/§5 (CAM-C2 FAILED-as-measured; CAM-C3 unenforced cache
  identity) — contract §2b/§2c.
- SUBSTANCE: shared status model (complexityFromBatchRow / isComplexityMeasured /
  MEASURED_COMPLEXITY_BATCH_STATUSES); honest FAILED texture wording; measuredByStatus
  coverage; cacheIdentity envelope (productionCacheIdentity /
  verifyCacheIdentityEnvelope) + per-row (batchRowIdentityReason) and per-model
  all-or-nothing edge gates with named/counted drop reasons; primaryWireCacheKey (full
  identity); CATALOG_DATA_VERSION → v2-camfixes; CATALOG_WIRE_VERSION → v2; server declares
  the envelope, keys the wire cache on the full wire key, logs cache states honestly
  (REFUSED flagged).
- OUTCOME: measured — clean build: measured complexity 1572 / unknown 6516 (baseline
  control MATCH), batch attached 4838, edges 1545, drops 0, envelopes VERIFIED. Full
  batteries green (see I-5).

## I-3 — test files updated to declare the production envelope (+ battery wiring)

- PATHS: tests/pecompat/catalog_unknown_sort.test.mjs (M),
  tests/pecompat/catalog_bounds_countercheck.test.mjs (M),
  tests/pecompat/catalog_preview_math.test.mjs (M),
  tests/pecompat/catalog_archive_safety.test.mjs (M),
  tests/pecompat/run_catalog_tests.mjs (M).
- REASON: CAM-C3 makes the identity envelope a REQUIRED production input — the tests that
  build the catalog with cache paths must declare the SAME envelope the server declares
  (fail-closed default would otherwise refuse the caches and defeat the gates' purpose).
  run_catalog_tests.mjs gains the new Focused QC A suite in its suite list.
- DISCIPLINE: NO existing assertion was weakened or removed; each edit adds
  `cacheIdentity: productionCacheIdentity()` (one line) + import. All 33 prior gates PASS
  unchanged (measured).

## I-4 — CAM-C1 comparison tool (NEW)

- PATHS: tools/pecompat/cam_c1_glb_compare.mjs (A).
- REASON: contract §2a — reproduce the original-vs-GLB geometry comparison from MY OWN
  reader outputs against the pinned GLBs.
- FAILED-FIRST ATTEMPT (recorded honestly): the first execution produced 4/4 MISMATCH.
  Root cause: MY tool bug — the conversion code computed (x, y, -z) while the comment and
  the preregistration said (x, z, -y) (a variable-naming transposition: `nz = y,
  nny = -z` written for the (z, -y) target slots). The mismatch pattern itself exposed it:
  every GLB-only key equaled exactly (x, z, -y) of the paired NIF-only key's original
  vertex. Fixed the conversion to the preregistered (x, z, -y) — NOT the other way around
  (the expectation was preregistered and the Desktop independently reported exact agreement
  under (x, z, -y), so the defect was in my tool, not in the preregistration).
- OUTCOME (after fix): 4/4 EXACT_AGREEMENT (bit-exact position multisets + unoriented
  triangle multisets; bounds identical; 0 mismatch keys). Raw: raw/CAM_C1_GLB_COMPARE.json
  (+ private-root copy).

## I-5 — Focused QC A suite (NEW)

- PATHS: tests/pecompat/catalog_cam_fixes.test.mjs (A).
- REASON: contract §2d/§8 — prove the three corrections hold through the REAL production
  paths (CAM-C1 fresh execution; CAM-C2 shared model + 1572 baseline control; CAM-C3
  3 mutants + clean + no-envelope refusal; physical-cache hash witness).
- FAILED-FIRST ATTEMPTS (recorded honestly — caught by the FIRST battery run, 4 FAIL):
  1. CAM_C2_SHARED_STATUS_MODEL: my gate regex `/FAILED decode/` did not match the correct
     note text "decode FAILED" (test-string bug; the measured outputs were all correct).
     Fixed the regex to `/decode FAILED/`.
  2. CAM_C3_M1/M2/M3: my io-mutation helper MEMOIZED the clean cache bytes, so the mutant
     builds silently read the clean copy and the mutations never reached the production
     gate (clean-vs-clean comparisons — a false "ACCEPTED" reading). Fixed the helper to
     never memoize the cache paths (each build reads + mutates them fresh); container
     memoization kept (byte-identical; the fail-closed pin checks still run per build).
  These were defects of the TEST HARNESS, not of the production gate — and the first run
  proving them FAIL is the honest negative control working.
- OUTCOME (after fixes): full battery 41 PASS / 0 FAIL / 0 NOT_PERFORMED (33 prior + 8
  CAM gates; summary raw/CAM_TESTS_SUMMARY.json). Mutants REFUSED with named reasons;
  clean passes the same gate; physical caches byte-identical (witness PASS).

## I-6 — evidence + artifacts

- PATHS: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (A: preflight, preregistration,
  disposition, this ledger, raw/ evidence), private root
  D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_LAUNCHER_R1_20261010\ (A: copies of the
  CAM-C1 report + battery summaries + CATALOG raw captures).
- REASON: contract §10 + the phase task list. Historical packages untouched; the battery
  harnesses were run with --raw-dir INTO THIS package (the harness default would have
  written into the historical PE_CITY_ASSET_MAP_R1_20261010 package — explicitly avoided).

## Standing interventions NONE

No commit/push in this phase (persistence is a later phase; not yet authorized to execute).
No src/pesource, src/pecompat, src/peworld, tools/gamebryo_oracle, or 218757 app file was
modified. No package installed. No standing server touched.

## Appendix A — post-edit identities (measured at phase end, 2026-10-10)

Pre-edit hashes: INPUT_IDENTITIES.json (modulesTouchedOrReused_preEdit).

```text
tools/pecompat/catalog_data.mjs                     55118 B  fc4969728b8f217cccb5afe69082a61d1f3964ed78d6b37c0546c18fef2842a5
compat/server-catalog.mjs                           22434 B  a1c17a41c46f5be8e9e067e87d0d59abda31c7a0d89d86f5584fcbb3c69b8aac
tools/pecompat/cam_c1_glb_compare.mjs (NEW)         22818 B  fdf2b7b819d0054d47388e8aa306a649adeef79188687c6b151fe5029d8b0986
tests/pecompat/catalog_cam_fixes.test.mjs (NEW)     23376 B  d6c4331b080a3a5c2f356d23928429de40dde1e186dcbe620c0ebf3082160540
tests/pecompat/run_catalog_tests.mjs                 6841 B  e8d76eb9de4ce66cc5c109e29f938586a8b739fc06b7ea00c4fdd8c24aee7ec9
tests/pecompat/catalog_unknown_sort.test.mjs        13434 B  7326b720821c895c539d18db6b3d128d3ff3d416e685b2c7ccc4d111b4819340
tests/pecompat/catalog_bounds_countercheck.test.mjs 11450 B  3892fd2660953be6ffc617a12f753697297e68bb57eecf2cbd967ef1cbb4f7de
tests/pecompat/catalog_preview_math.test.mjs        10303 B  9d2379cbc359ec95f8702684aca4b9ecddb05f56490754885b355915d684212c
tests/pecompat/catalog_archive_safety.test.mjs     22654 B  318ea14c070cfa38d93ab032dd8e13b2a9305edab9937a77c5efd4a48241f68a
```

Unchanged-by-verification (read-only witnesses this phase, hashes unchanged — see
INPUT_IDENTITIES.json): src/pecompat/PecNif10Reader.js, src/pecompat/PecSceneIR.js,
tools/pecompat/nif41_deep.mjs, src/pesource/ArkArchive.js, both physical cache JSONLs
(hash witness also asserted inside the Focused QC suite), the four GLBs, all seven contract
inputs.

---

# PHASE 2 — ETAP B: GAMEBRYO MECHANISM RESEARCH SUBORDINATED TO IMPLEMENTATION
(2026-10-10; governing contract §3; no launcher implementation started — hard constraint)

## I-7 — phase-1 handoff observation CORRECTED (skill existence)

- PATHS: none (evidence correction only).
- REASON: phase 1 recorded (AUTHORIZATION_AND_PREFLIGHT §7, INPUT_IDENTITIES
  skillsAndDocsRead) that pe-gamebryo-rosetta was "NOT FOUND at any .opencode skills
  root" — it checked C:\Users\User, D:\TESTAI and D:\Eudoria_Reconstruction roots.
  PE-MASTER verified against e9bb1f5 that the skill EXISTS in THIS WORKTREE at
  `.opencode/skills/pe-gamebryo-rosetta/` (git ls-tree e9bb1f5: SKILL.md + 3 references,
  clean). Phase 1's observation stands as an honest record of the roots it checked; the
  correction is recorded here per append-only discipline. Phase 1's IMPLEMENTATION work
  is unaffected (it touched no skill).
- OUTCOME: the skill was EXTENDED (I-9), not created from scratch.

## I-8 — Etap B SDK research (READ_ONLY; 0 native executions)

- PATHS: none written. 23 SDK files read from D:\gamebyroengine\extracted\
  (identities + examined-line census in INPUT_IDENTITIES.json etapB_sdkSourcesRead +
  GAMEBRYO_MECHANISM_MAP.md §1): Gb12 core (NiStream.cpp, NiTransform.inl,
  NiAVObject_Win32.cpp, NiAVObject.inl, NiAVObject.cpp, NiNode.cpp,
  NiTexturingProperty.cpp, NiSourceTexture.cpp, NiGeometry.cpp, NiVersion.h), Gb12
  samples (SceneAttachment, BackgroundLoad + CallbackStream, MOUT TerrainManager/.h/.inl
  + WorldManager.cpp), Gb26 comparison (NiExternalAssetNIFHandler.cpp/.h), Gb112 docs
  (2 pages, one consulted, one located).
- NATIVE EXECUTIONS THIS PHASE: **NONE**. No stock tool, no SDK binary, no Entropia.exe,
  no printer. All SDK findings are source reads; all PE-side facts cite prior executed
  runs (sceneir/inspection/catalog lineages + M1 clean-path iterations). The contract's
  "native tools only if a concrete safe test is needed" clause was not triggered — no
  mechanism in scope required a new native control this phase.
- SCOPE BOUNDS HELD: no whole-SDK read, no new atlas, no new EXE RE, no SDK
  source/doc/binary text copied into the repo (own summaries + identities only).
- OUTCOME: GAMEBRYO_MECHANISM_MAP.md written (5 mechanisms, each
  source/SHA → behavior → PE evidence-or-gap → decision → control status EXECUTED-prior
  vs PLANNED-later-phase).

## I-9 — module API verification + skill extension + implementation map

- PATHS WRITTEN (this phase, all new files; NO source code changed):
  - docs/audits/PE_WORLD_LAUNCHER_R1_20261010/GAMEBRYO_MECHANISM_MAP.md (A)
  - docs/audits/PE_WORLD_LAUNCHER_R1_20261010/IMPLEMENTATION_MAP.md (A, DRAFT)
  - docs/audits/PE_WORLD_LAUNCHER_R1_20261010/INPUT_IDENTITIES.json (M — Etap B
    sections appended; phase-1 content unchanged)
  - docs/audits/PE_WORLD_LAUNCHER_R1_20261010/INTERVENTION_LEDGER.md (M — this section)
  - .opencode/skills/pe-gamebryo-rosetta/references/terrain-foliage-integration.md (A)
  - .opencode/skills/pe-gamebryo-rosetta/SKILL.md (M — one short pointer section;
    existing references untouched)
- VERIFIED APIs (read-only): the 9 contract-named modules + PEProvenance/Bnt2Archive/
  ArkArchive/BuntArchive/NifModelReader + server.mjs + terrain/p0.js +
  tools/iter020_material_audit.js (identities in INPUT_IDENTITIES.json
  etapB_modulesApiVerified). KEY FINDINGS (recorded in the mechanism/implementation
  maps + skill): PETerrainRegion lives inside PETerrainCore.js;
  BrowserSourceAdapter/NodeSourceAdapter DO NOT EXIST (comment-only; minimal adapters
  planned per the established in-tree patterns); the ACTIVE TdfMaterialTailDecoder uses
  mask@record+56 (contract pin) while TdfDecoder.TDF_MATERIAL_RECORD_LAYOUT.MASK16
  (record+52) is a STALE constant that must never supply mask offsets;
  PESourceMount.getSentinelInfo is 50.bnt-bound (JUL-only in practice — PCG sentinel
  handling is an explicit Etap C decision); PEFoliageCore.generateInstances has NO
  LAB_SEED input (a documented [P-CELLSTREAM] wrapper is planned for Etap E; the locked
  RNG arithmetic stays untouched); PETerrainRegion.buildGeometry emits positions+indices
  only (no UV/normals — Etap D renderer-side UVs or a bounded extension).
- SKILL EXTENSION (contract §3): a SHORT terrain/materials/foliage integration index
  added as references/terrain-foliage-integration.md (verified source locations with
  SHA256; executed controls incl. the CURRENT_RUNTIME_CALIBRATION facts; explicit
  UNKNOWNs: cell-stream source, climate→region mapping, p3, materialId==textureId NOT
  established, PCG special rows, 25.vcl; commands incl. the PLANNED serve:world; era
  discipline) + a 16-line pointer section in SKILL.md. Every claim carries source+scope;
  no "engine 100% known" anywhere; no SDK text copied.
- OUTCOME: all four Etap B task artifacts delivered; the launcher architecture is
  drafted (IMPLEMENTATION_MAP.md) with reuse-first module map, the 8162 server plan
  (bounded server-side PESourceMount; NO whole-container browser downloads) and the
  C/D/E/exploration phase breakdown.

## Standing interventions NONE (phase 2)

No commit/push in this phase. No src/pesource, src/pecompat, src/peworld,
tools/pecompat, compat/ or tests/ file was modified. No package installed. No standing
server touched (8140/8161 alive and untouched; 8162 still free). No SDK file modified
(reads only). Historical docs/audits packages untouched. The five mechanism controls
marked PLANNED are pointed at Etap C/D/E per the contract — none was claimed executed.

---

# PHASE 3 — ETAP C: WORLD SERVER + LAUNCHER + TERRAIN FROM THE REAL HEIGHTMAP
(2026-10-10; governing contract §4 (first paragraph + terrain invariants) + §7; no commit/push in this phase — persistence is a later phase)

## I-10 — world server (NEW; extends the proven catalog/sceneir server design)

- PATHS: compat/server-world.mjs (A); package.json (M — `serve:world` + `test:pecompat:world` scripts only).
- DESIGN (REUSE LABEL): deny()/serveBytes()/exact allowlists/jailed three-subtree/verified-free-port/
  fail-closed pins/GET-HEAD-only — the server-catalog.mjs design, extended; catalog + sceneir servers
  byte-identical and untouched.
- SUBSTANCE: loopback 127.0.0.1:8162 (PEWORLD_PORT override; 8140/8161 refused explicitly); explicit PID +
  READY startup line + own-process stop; routes /launcher /world / (302->launcher); bounded index-derived
  APIs ONLY (status, overview binary 363,440 B = 51,920×7, overview/progress, tile/<gx>/<gy>[+/meta],
  climates, climate/<0..31>, gaps); NO arbitrary path reads, NO whole-container downloads (measured by
  WORLD_T7_NO_WHOLE_CONTAINER); server-side PESourceMount (era PCG_9_3_5, fail-closed SHA pins); full
  per-regular-tile census from ORIGINAL bytes (async with progress, ~1.9 s); tile cache with the CAM-C3
  full-identity gate on every hit (era+container+containerSha256+entryName+payloadSha recomputed over the
  cached bytes+decoderVersion; mismatch = controlled refusal + regeneration); Models.bnt/Textures.bnt
  stream-hash VERIFICATION ONLY (bounded memory; never mounted/decoded/served).
- MEASURED CORRECTION: the special-row gridY range is 0xff5a..0xffff (measured; the phase-2 map's
  "0xff1a" was a transcription artifact — recorded in WORLD_DATA_PROVENANCE.json).
- SERVER LIFECYCLE (dev instance, this phase): PID 10320 started 8162 (first boot; census 51,920/51,920
  in 1,932 ms; models+textures VERIFIED) -> killed (my own process) after the deny-message fix ->
  restarted as PID 13556 on 8162 (final code; census 1,911 ms) and LEFT RUNNING for the user.
  STOP = Stop-Process -Id 13556 (only this process).
- TEST SERVERS: every suite-owned instance started/stopped with port-freed proof (PIDs/ports in the
  battery lifecycle records: e.g. T7 pid 24264 port 8429, T9 pid 11372 port 8512, pixel-render instance);
  standing 8140 (PID 21288) + 8161 (PID 9588) never touched (verified busy before/after).

## I-11 — launcher UI (NEW)

- PATHS: compat/launcher.html (A), compat/launcher.js (A), compat/launcher.css (A).
- SUBSTANCE: 5 panels per contract §4 — (1) original-data connection state: era PCG_9_3_5, the FOUR
  pinned containers with SHA256 + state (terrain+veg MOUNTED_VERIFIED; models+textures stream-hash
  verified in background), loading stages with the census progress bar; (2) heightmap from the REAL
  terrain.bnt index: per-regular-tile overview (1 px = 1 tile = mean of 1024 raw u16 — EXPLICIT
  DOWNSAMPLE label), legend (raw u16 -> palette; meters = u16/128 labeled CURRENT_RUNTIME_CALIBRATION),
  coverage with denominators (measured/total/NODATA %; special rows + sentinel listed as excluded),
  highlighted 4×4 selection, tile/region click selection, hover = RAW uint16 tile stats, selected-tile
  32×32 per-sample preview with exact per-sample RAW uint16 hover (real decoded bytes via the tile API),
  async overview refresh with progress (poll + partial re-render), manual refresh button; (3) vegetation
  profile picker 0..31 from /api/world/climates (honest UNSUPPORTED rows kept; default = MEASURED choice:
  most records among decoded — never "historical biome"), LAB_SEED input, preview-density slider,
  VEGETATION_MODE = RECONSTRUCTION_PREVIEW note, entry button labeled EXACTLY "Uruchom podgląd świata"
  -> /world#tile=..&profile=..&seed=..&density=..; (4) catalog link (8161 standing server) + honest
  gaps/unsupported panel from /api/world/gaps; (5) "ORYGINALNE DANE" vs "USTAWIENIA REKONSTRUKCJI"
  separation boxes + collapsible evidence panel (hashes/offsets/decoders/calibration — outside the main
  flow). T9 markers present (id="view-canvas", id="diagnostics" data-load-status).

## I-12 — world view (NEW)

- PATHS: compat/world.html (A), compat/world-app.js (A), compat/world.css (A).
- SUBSTANCE (contract §4 + §7): terrain from ORIGINAL u16 samples — /api/world/tile (2048 B raw) ->
  canonical client-side TerrainTile (provenance via makeProvenance from the response headers) ->
  PETerrainRegion (8×8 window = AT MOST 64 ACTIVE TILES) -> buildGeometry (positions+indices only; the
  u16->meters conversion applied EXACTLY ONCE inside buildGeometry; u16/128 + 2 m/sample +
  identity min/max = CURRENT_RUNTIME_CALIBRATION preset, shown in the evidence panel); renderer-side
  normals + RECONSTRUCTION_PREVIEW height palette (labeled, never source claims); inter-tile topology =
  documented choice (quads across tile borders from ADJACENT ORIGINAL samples; no seam repair; no height
  changes for jump masking); streaming window re-centered on the camera with bounded client LRU
  (512 tiles) + identity-checked cache; missing data NEVER builds a mesh over void (movement stopped +
  boundary banner); wireframe + tile-bounds toggles live, textures/vegetation toggles present but
  disabled with NOT_YET (Etap D/E) labels; orbit/fly/walk modes (WASD; pointer lock ONLY after a
  conscious click; ESC frees), fit [F]/reset [R], return-to-launcher button; position display in
  adapter units + tile key + raw u16 (NEVER "oryginalne XYZ"); spawn = the launcher selection or the
  measured max-mean tile (no city-name guessing); loading/errors + profile/seed + memory/instance
  census panels; scene transforms (mesh.position = origin×64 m, scale 1) separate from viewer
  fit/centering (camera-controller only — the camera-UX lesson applied).

## I-13 — world gate battery + browser gates (NEW tests/tools)

- PATHS: tests/pecompat/_world_server_helpers.mjs (A), world_terrain.test.mjs (A), world_server.test.mjs
  (A), world_headless_load.test.mjs (A), run_world_tests.mjs (A); tools/pecompat/world_pixel_render.mjs
  (A), world_collect_test_results.mjs (A).
- GATES: terrain (offset-64 negative incl. the measured degenerate all-zero tile; 1024 heights;
  INDEPENDENT test-local byte reader bit-exact on 6 tiles; sentinel loud refusals; NODATA census;
  reverse-order invariance; hash witness; bounds/calibration-once/reversibility), server (routes/statics,
  status pins, tile wire == production decode, denials incl. raw-socket traversal/NUL/backslash,
  no-whole-container, overview binary layout + cross-check, climates honesty incl. 25 UNSUPPORTED,
  gaps honesty, CAM-C3 cache mutants), browser (T9 5-conjunct LOAD of /launcher + /world via the
  imported fixed gate; PIXEL_RENDER 2 shots into the PRIVATE root).
- FAILED-FIRST ATTEMPTS (recorded honestly; see TEST_RESULTS.json failedFirstRuns):
  1. First battery run 18 PASS / 6 FAIL — (a) offset-52 preregistration falsified on the all-zero tile
     000a0014.tdf (sub-header also zero -> the two byte ranges coincide; refinement documented in the
     suite header; control KEPT with 5/6 discriminating); (b) MY bounds-test indexing typo; (c) MY
     "/"-expected-200 harness bug; (d) MY case-strict SHA compare; (e) server deny-message gap for
     non-allowlisted /src/* modules (FIXED IN THE SERVER); (f) MY naive "oryginalne XYZ" substring
     marker tripping on the REQUIRED honest negation labels (refined to target the readout claim).
  2. First catalog-battery invocation without container args -> 37 PASS / 4 honest NOT_PERFORMED;
     re-run with the phase-1 arg set -> 41 PASS / 0 FAIL / 0 NOT_PERFORMED (both recorded).
  3. First app-battery invocation (no args) wrote 4 raw dumps into the HISTORICAL
     PE_CITY_ASSET_MAP_R1_20261010/raw/ (the harness default — the exact trap phase 1 documented);
     MY OWN accidental untracked writes: DELETED; historical package re-verified clean
     (0 tracked modifications, 0 untracked residue); re-run with correct args into raw/APP_ETAPC.
- OUTCOME (final code): world battery 24 PASS / 0 FAIL / 0 NOT_PERFORMED; PIXEL_RENDER 2/2 NON_TRIVIAL
  (launcher 164,886 B / 185 canvas-region colors; world 330,734 B / 7,335 canvas-region colors; PNGs in
  99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER only); INTERACTION = NOT_PERFORMED (automation daemon
  port 9222 measured DOWN — honest).

## I-14 — evidence + artifacts (this phase)

- PATHS: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (A: WORLD_DATA_PROVENANCE.json,
  CALIBRATION_AND_UNKNOWNS.md, TEST_RESULTS.json, this ledger section, raw/WORLD/* incl. the two DOM
  dumps + WORLD_TESTS_SUMMARY.json + PIXEL_RENDER.json, raw/UNIT_TESTS_SUMMARY_ETAPC.json,
  raw/APP_TESTS_SUMMARY_ETAPC.json + raw/APP_ETAPC/, raw/CATALOG/CATALOG_TESTS_SUMMARY_ETAPC.json);
  private root 99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER\ (A: pixel_launcher.png, pixel_world.png).
- REGRESSION: unit 24 PASS / 0 FAIL / 0 NOT_PERFORMED; app 22 PASS / 0 FAIL / 0 NOT_PERFORMED; catalog
  41 PASS / 0 FAIL / 0 NOT_PERFORMED; the 218757 viewer + all src/pesource|peworld|pecompat code
  byte-identical to HEAD (git diff empty).

## Standing interventions (phase 3)

- ONE standing server of MY OWN is deliberately left running for the user: world server
  http://127.0.0.1:8162/ pid=13556 (final code; census complete; standing 8140/8161 untouched).
- No commit/push in this phase. No src/pesource, src/peworld, src/pecompat, tools/pecompat (pre-existing),
  compat (pre-existing), tests (pre-existing) file was modified. No package installed (three 0.185.0
  unchanged; pinned at the configured eudoria-clean node_modules root). No SDK file touched. Historical
  docs/audits packages clean (the accidental raw writes were removed — I-13.3). No original container
  modified (terrain.bnt hash witness PIN before AND after).

## Appendix B — post-edit identities (measured at phase end, 2026-10-10)

```text
compat/server-world.mjs                                47764 B  3ee30425867e3b45d1027675b223f6f6e0405e9298fbfe815502b244c741dd07
compat/launcher.html                                    9170 B  a17621c9b37b165761310d567a96cbdbcda55fe7ff412965f038ce49938710a1
compat/launcher.js                                     23892 B  b05b66b0968a9036824f4ba0b97f564b3b15038808da5cbd0fc35b4288946501
compat/launcher.css                                     3973 B  3fbf9be4563db1343d5dcc7c1990c0a26c9660333d31194877bdf535dbce9f86
compat/world.html                                       6166 B  e2fc48a45e032616154cb6e27e11e79815c4561c174b75f445f97da21d6a3ac0
compat/world-app.js                                    27789 B  16d8d4afc63e111b7c5228ae081775c3c2cad39ad35ee707931dc4092c3b7025
compat/world.css                                        1390 B  a035c84a0549346505a111c2d7764b8a09598379a946f62f10149851d2cb4362
package.json (M)                                          528 B  aeff0c69a383b75e73f4bab11e999d811ce446923c8f5a66c68b536703994249
tests/pecompat/_world_server_helpers.mjs                6358 B  f38f997cf387b2dfac19d583970b6075d5671c385dbceed0b1ceb43f364f136c
tests/pecompat/world_terrain.test.mjs                  24610 B  bba5b40e2f5f9d6f45946134e3e0f9941e71c877280c71957c53d4c6dc253f55
tests/pecompat/world_server.test.mjs                   24954 B  59ed7328cd380edcc0f6910884cc359773bf88e29d44e4c83aa0937473350976
tests/pecompat/world_headless_load.test.mjs            11332 B  88fc62f9cfa07ba0a413ed862ad10995e048270168d4908d77d065e9fb7f9811
tests/pecompat/run_world_tests.mjs                      4678 B  4f819d94021e03226326a51e87c714a1529cf4c4c6dd58f257c17d991c5a385d
tools/pecompat/world_pixel_render.mjs                   9470 B  1877b40b58caf616fd69b20e565fa03cc8c296ed4dd31ae2881cba5cc087bf1a
tools/pecompat/world_collect_test_results.mjs           9468 B  0275bf59eb83719204f6cf71bd1e43c8cf3faea22a846adb651f19e37e38d3eb
```

Unchanged-by-verification (read-only witnesses this phase): all four pinned containers (terrain.bnt
hash witness asserted before AND after the battery), src/pesource/* + src/peworld/* + src/pecompat/*
modules (imported, never modified), compat/index.html/app.js/asset-mode.js/scene-mode.js/api.js/
server-sceneir.mjs (218757 app — byte-identical), compat/server-catalog.mjs + catalog test files
(Etap A uncommitted work — present in the tree, NOT touched by this phase), the standing 8140/8161
servers (never touched).

---

# PHASE 4 — ETAP D: ORIGINAL TERRAIN TEXTURES (THE PROVEN CHAIN)
(2026-10-10; governing contract §5 + §8 materials gates; no commit/push in this phase — persistence is a later phase)

## I-15 — server extensions: the material-tail + texture routes (NEW endpoints on the Etap C server)

- PATHS: compat/server-world.mjs (M — the ONLY pre-existing production file touched this phase; all
  changes additive: routes/caches/stages, the Etap C surface unchanged).
- SUBSTANCE: /api/world/tile/<gx>/<gy>/materials (named records in RECORD ORDER with the RAW 16x16
  masks @ record+56 as base64, per-material resolved `<id>.dat` entries, system records with
  UNVERIFIED labels, sums, provenance) + /api/world/texture/<id> (ONE bounded payload read through
  the new LazyTextureArchive — footer + 225,602 B directory parse after the FAIL-CLOSED stream-hash
  pin verifies; 8,381 entries; per-entry reads with an 8 MiB guard; NEVER the whole 974 MB container;
  NO whole-container route BY CONSTRUCTION) + the era gate (?era= other than PCG_9_3_5 → 403
  ERA_REFUSED_WRONG_ERA on every /api route, BEFORE any data access) + the identity-checked caches
  (IdentityCache: materials keyed with payload SHA over the cached TAIL bytes; textures with payload
  SHA over the cached bytes; every HIT re-verified — a mismatch = controlled refusal + regeneration
  with named reasons) + status/gaps sections (terrainMaterials: maskOffset 56, the chain relation,
  the preset; the gaps row terrain_textures → ETAP_D_DELIVERED with the honest scope; a NEW measured
  gap row for the 12 B Textures/Terrain.bnt non-atlas) + the measured special-row range fix
  (0xff1a → 0xff5a in the GRID_OUT_OF_RANGE message — the recorded phase-3 correction finally
  applied to this message too).
- RELATION EVIDENCE (the chain, not an assumption): id@+16 → `<id>.dat` — engine-RE CONFIRMED
  (M1_TSFS_BINARY_FORENSICS_20260906 iter015e/f decompiles: the 9.3.5 record parse reads sub@+16 as
  the material TEXTURE id; consolidated iter030; EU935 census GROUND_TEXTURES §3 CONFIRMED with
  probe05) + re-measured on THIS RUN's samples (WORLD_MAT_CHAIN_RESOLVE: 29/29 distinct sampled ids
  resolved; entry metadata == the independent index parse; wire bytes bit-exact the physical file
  reads). The historical extract_material_textures_from_textures_bnt_v1.py used the same relation
  (lineage, not evidence). Name match is NEVER the resolver (id↔name measured MANY-TO-MANY:
  37944 = Test3|Snow).

## I-16 — client modules (NEW/EXTENDED)

- PATHS: compat/world-splat.js (A — the PURE splat builder: per-cell layer slots in RECORD ORDER,
  RAW weights bit-exact, exact-duplicate dedupe, unresolved bindings SKIPPED with explicit
  diagnostics — never a fallback texture; the RENDER_RECONSTRUCTION_PRESET single source of truth;
  the documented GPU sampling convention sampleTexelImageOrder + worldUV) + compat/world-app.js (M —
  the materials subsystem: materials grid fetch, texture payload fetch + the PRODUCTION decodeTga2
  IN THE BROWSER (the same module the server gates use — no second decoder), the DataArrayTexture +
  idx/weight DataTextures GPU build, the splat shader (sequential lerp per layer by RAW mask/255 in
  slot order; idx=255 = empty; GLOBAL world uv /32 m; SRGB passthrough — no output colorspace
  chunk), the REAL texture toggle (ON = splat, OFF = height palette; #textures=0|1 URL state),
  window-move dispose/rebuild, the bounded RGBA LRU (64) + the materials census/evidence panels)
  + compat/world.html (M — toggle enabled + the honest Etap D labels) + the server allowlists
  (world-splat.js + src/pesource/TgaDecoder.js added as served client modules).
- ROLE HONESTY: the 9.3.5 engine used these masks for the LOD vertex-COLOR tint bake + zone shadow
  paint (iter030, 838/838 census); the ground albedo was the climate palette pipeline (MISSING local
  inputs 432502/459344). The /world textured terrain is therefore labeled RENDER_RECONSTRUCTION:
  era-evidenced blend FORM applied to albedo + reconstruction-chosen UV repeat/cell sampling/color
  space (documented in world-splat.js + surfaced in the evidence panel; raw weights never changed).

## I-17 — tools + tests (NEW/EXTENDED)

- PATHS: tools/pecompat/png_nontrivial.mjs (M — ADDED decodePngRaw export; analyzePng behavior
  unchanged) + tools/pecompat/world_pixel_render.mjs (M — the world captured TWICE: #textures=1 and
  #textures=0; the ETAP_D_TEXTURE_TOGGLE_CHANGES_PIXELS gate compares the two canvas regions
  pixel-by-pixel with preregistered thresholds) + tools/pecompat/world_collect_test_results.mjs
  (M — the Etap D sections) + tests/pecompat/world_materials.test.mjs (A — the 9 materials gates)
  + tests/pecompat/_world_server_helpers.mjs (M — waitForWorldReady also waits for the texture
  index READY) + tests/pecompat/world_server.test.mjs (M — the T7 gaps/status gates track the
  ETAP_D delivered state + the new statics; NO assertion weakened: the delivered item must carry
  its honest scope labels) + tests/pecompat/run_world_tests.mjs (M — the materials suite wired in;
  --textures arg).
- GATES (9, preregistered in the suite header BEFORE execution):
  WORLD_MAT_MASK56_NEGATIVE (mask@56 on physical samples; the wrong 52 REFUSES on 100% of RAW
  records; RLE-with-zero-extra4 degenerate cases documented as measured boundaries — the same
  pattern as the phase-3 all-zero tile) / WORLD_MAT_WIRE_BITEXACT (served masks bit-exact
  independent reads; sums>255 preserved) / WORLD_MAT_CHAIN_RESOLVE (29/29 ids; wire bit-exact;
  decode subset; missing id 404; double-fetch HIT) / WORLD_MAT_ERA_REFUSAL (route 403s + the
  verifyTextureCacheIdentity/verifyMaterialsCacheIdentity mutants: ERA/CONTAINER_SHA/ENTRY_NAME/
  PAYLOAD_SHA/WIRE_VERSION each refused by name; clean passes) / WORLD_MAT_SPLAT_RAW_WEIGHTS (the
  REAL window through the pure builder; an independent re-walk proves the GPU-bound weights ==
  the served raw masks, slot order = record order) / WORLD_MAT_MALFORMED_CONTROLLED (RLE overrun,
  odd region, implausible size, residual bytes → LOUD throws; TGA 32bpp/footer/truncated → LOUD;
  clean controls decode) / WORLD_MAT_UNRESOLVED_BINDING (synthetic missing relation → layer
  SKIPPED + listed, no slot, resolved layers applied; decode-failure path same) /
  WORLD_MAT_UV_FLIP_CONTROL (PATTERN + REAL: decodeTga2 IMAGE order vs the A32 FILE-row convention
  distinguished on the same payload shape; the documented GPU sampling consistent on both) +
  the suite lifecycle (port-freed proof).
- FAILED-FIRST ATTEMPTS (recorded honestly; also in TEST_RESULTS.json failedFirstRuns):
  1. WORLD_MAT_HTTP_GATES ECONNRESET — MY server bug: the provenance HEADERS carried em-dashes
     (ERR_INVALID_CHAR kills the route); fixed with ASCII-safe header constants.
  2. THE ENCODING INCIDENT (my tooling mistake): the first header fix went through a PowerShell
     5.1 Get-Content/-replace round-trip that MISREAD the UTF-8 server file as ANSI and corrupted
     every non-ASCII string (Polish diacritics, dashes). REPAIRED deterministically (a CP1252
     reversal script with a validated round-trip; samples verified; the whole battery re-run green
     after). LESSON RECORDED: file edits through the edit tool ONLY — never PS text cmdlets on
     these files.
  3. WORLD_MAT_MALFORMED first FAIL — MY synthetic record builder wrote the size field 4 bytes off
     (a TEST bug; the production decoder refused the bogus record loudly, exactly as designed);
     builder fixed (size at offset 0; size = 52 + region.length).
  4. WORLD_MAT_CHAIN_RESOLVE first FAIL (doubleFetchCacheHit=false) — a REAL production bug caught
     by the preregistered HIT expectation: IdentityCache.set OVERWROTE the entry's identity
     envelope with the bare key identity, so every HIT failed verification (WIRE_VERSION_MISMATCH)
     → REFUSED_REGENERATED. FIXED (the entry envelope takes precedence; entryName enforced). The
     CAM-C3 discipline worked exactly as specified: a broken cache identity is REFUSED, never used.
- OUTCOME (final code): world battery 33 PASS / 0 FAIL / 0 NOT_PERFORMED (24 Etap C gates re-run
  green + 9 materials gates); regression: unit 24 PASS, app 22 PASS, catalog 41 PASS (the Etap D
  re-runs with the phase-3 arg sets; the first unit/app invocations without --models measured
  honest NOT_PERFORMED container gates — re-run, recorded). PIXEL_RENDER: launcher + world-on +
  world-off all NON_TRIVIAL PASS + ETAP_D_TEXTURE_TOGGLE_CHANGES_PIXELS PASS (58.77% of the canvas
  pixels differ; meanAbsΔ 90.71; meanLumaΔ 55.10 — the toggle REALLY changes the render). The
  real-browser world LOAD with textures ON shows the chain census in the DOM (615/615 layers
  resolved, 28 textures decoded, 114,019 slots applied, 2 window rebuilds — the window-move
  rebuild path exercised and observed).

## I-18 — STANDING SERVER RESTART (my own process only; API changes)

- OLD: world server 127.0.0.1:8162 pid=13556 (the phase-3 final code) — STOPPED (Stop-Process -Id
  13556; only this process; port freed verified).
- NEW: world server 127.0.0.1:8162 pid=24412 (the Etap D final code; started with the documented
  `npm run serve:world` command shape from the worktree root) — READY measured: census
  51,920/51,920; textures VERIFIED + index READY (8,381 entries); /api/world/tile/53/114/materials
  → 9 named materials (Stone04 id=13382 resolved); /api/world/texture/13382 → 196,652 B
  (MISS → HIT on the second fetch); ?era=CD_JAN_2003 → 403 ERA_REFUSED_WRONG_ERA. LEFT RUNNING for
  the user. STOP = Stop-Process -Id 24412 (only this process).
- LEFTOVER CLEANUP (found + killed at the phase-end orphan scan): pid=14820, my own debug instance
  of compat/server-world.mjs on port 8477 — a Start-Process attempt whose tool-wrapper reported an
  error while the process HAD started (the tool error was NOT proof of termination); killed + port
  freed verified. Lesson recorded: task-wrapper errors are never process-liveness evidence.
- The foreign standing servers 8140 (pid 21288) + 8161 (pid 9588) were NEVER touched (verified
  listening before AND after every suite/lifecycle/standing operation).

## I-19 — evidence + artifacts (this phase)

- PATHS: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (M: TEST_RESULTS.json regenerated with the
  Etap D sections by the collect tool; WORLD_DATA_PROVENANCE.json extended with
  ETAP_D_MATERIAL_CHAIN — per-step chain evidence + the separate resolved/decoded/applied/
  browser-observed counters with denominators + the relation provenance + the preset;
  CALIBRATION_AND_UNKNOWNS.md updated (U-7 RESOLVED for the sampled scope; new U-13..U-16);
  this ledger section; raw/WORLD/WORLD_TESTS_SUMMARY.json (the final 33-gate run — supersedes the
  phase-3 24-gate summary; the phase-3 raw evidence files remain on disk) + raw/WORLD/
  PIXEL_RENDER_ETAPD.json + the refreshed WORLD_DOM_DUMP_WORLD.html (textures ON) +
  raw/UNIT/UNIT_TESTS_SUMMARY_ETAPD.json + raw/APP_ETAPD/ + raw/CATALOG/CATALOG_TESTS_SUMMARY_
  ETAPD.json) + private root 99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER\ (A:
  pixel_world-on.png, pixel_world-off.png — PRIVATE ONLY; the phase-3 captures remain).
- INTERACTION: the automation daemon (port 9222) re-measured DOWN (once, honest); INTERACTION =
  NOT_PERFORMED (never PASS-by-default).
- PRE-EXISTING-DEFECT REPAIR (found during this phase's artifact pass, recorded honestly):
  INPUT_IDENTITIES.json (a phase-2 artifact of THIS run's package) carried 20 mojibake sites
  ('—' where '—' belonged — the same CP1252-mis-read signature as the server-world incident;
  MEASURED with a package-wide scan: the ONLY corrupted file in the package; the Polish text in
  all artifacts was measured LEGITIMATE UTF-8). REPAIRED deterministically (selective sequence
  replacement only — wholesale byte reversal was impossible because the file legitimately mixes
  correct Polish diacritics with the corrupted dashes; JSON validity verified post-repair). The
  phase-2 CONTENT is unchanged apart from the 20 restored em-dashes.

## Standing interventions (phase 4)

- ONE standing server of MY OWN is deliberately left running for the user: world server
  http://127.0.0.1:8162/ pid=24412 (the Etap D final code; census + texture index READY;
  standing 8140/8161 untouched).
- No commit/push in this phase. src/pesource, src/pecompat, src/peworld: NO file modified (the
  material/tail + TGA decoders were IMPORTED, never edited; verified: git diff empty for those
  trees). The 218757 app + catalog/sceneir servers byte-identical and untouched. No package
  installed (three 0.185.0 unchanged). No SDK file touched. No original container modified
  (terrain.bnt + Textures.bnt hash/pin witnesses verified through every battery).

## Appendix C — post-edit identities (measured at phase end, 2026-10-10)

```text
compat/server-world.mjs                                (M)  79848 B  1862bfdeb131aa6bb58dc1603f30ef7905affc99d28ad6373958ba5014be3d0f
compat/world-splat.js (NEW)                            13045 B  94d4e40be2c31c2ce299a8a74b4a7ae7f1e607dc5b73c9c1233d4fe5703c9bde
compat/world-app.js (M)                                53224 B  0a9f8a796a5e006be293e0c06d2944fd8c4e9c624bbeb8ff3544a6412146c4ed
compat/world.html (M)                                   6865 B  554c0e062310b8795862483e68d1c7de38368ae83c97d843bd881e38d4d8bd5d
tools/pecompat/png_nontrivial.mjs (M)                   8935 B  3dc0c07aecd4c0dbbcd3ddc1f176d8eaf2e03711c97fa01bdef69457f116cc7b
tools/pecompat/world_pixel_render.mjs (M)              14158 B  041f2210863023472590322656f754e25f4875c261117ba6e3a9a4026d36c415
tools/pecompat/world_collect_test_results.mjs (M)      17291 B  4d7aaa55d5cd3ba61938f0a47f28bf06774e5c57aa959df77f36912e5f0a9a5f
tests/pecompat/world_materials.test.mjs (NEW)          50554 B  f216331532a7fafcffc9405bcc2f34762c22f722910fd7c0864c47e4851e73d5
tests/pecompat/_world_server_helpers.mjs (M)            6575 B  f944b341f6e0d9a23f6ead6db381676ad88b233608a70a3408b9554f406f3c8c
tests/pecompat/world_server.test.mjs (M)               27183 B  53df7ed3af8e755de89017a51d0ff3fa4e0a79991797993b8cbb38c51e2898b2
tests/pecompat/run_world_tests.mjs (M)                  5417 B  88e8fe1ff0841ebc16d118470f9783316ead383764b61f53ec4b3ef4261985e4
```

Unchanged-by-verification (read-only witnesses this phase): terrain.bnt + Textures.bnt
(pins verified fail-closed at every server start; the stream-hash witness covers the whole
container), all src/pesource/* + src/peworld/* + src/pecompat/* modules (imported, never
modified), the 218757 app files, the Etap A catalog work (uncommitted, untouched), the standing
8140/8161 servers.

---

# PHASE 5 — ETAP E: VEGETATION (.VCL CLIMATE PROFILES, LAB_SEED DETERMINISM, PEFOLIAGECORE INTEGRATION, REAL MODELS)
(2026-10-10; governing contract §6 + §8 vegetation gates; no commit/push in this phase — persistence is a later phase)

## I-20 — the DOCUMENTED LAB_SEED wrapper (NEW; PEFoliageCore untouched)

- PATHS: src/peworld/PEFoliageLabSeed.js (A — the ONLY new src/peworld file; PEFoliageCore.js byte-identical to HEAD, verified by WORLD_VEG_CORE_UNTOUCHED + the unit battery's witness gate).
- SUBSTANCE: generateTileInstances({records, labSeed, gx, gy, level=1, viewBand=10, p3=0, densityPercent, tileWorldMeters=64, u16PerWorldMeter=2.0}) — the per-tile deterministic generation. THE THREE-WAY SEPARATION is the module's binding contract: ORIGINAL_CLIMATE_RECORDS consumed READ-ONLY; RECOVERED_RNG_ARITHMETIC = the PEFoliageCore exports (VegetationRNG.seed/next01 via sampleModelScale, subdivisionStep, packedQueryPosition, NODE_POS_DIVISOR) imported AS-IS; INSTANCE_DISTRIBUTION = the LAB_SEED-keyed [P-CELLSTREAM] stand-in (labPlacementHash — the same splitmix shape as PEFoliageCore's internal placementHash with the seed mixed in; the wrapper REPLACES that reconstruction component, never the byte-locked chain). LAB_SEED is NEVER equated with the unestablished p3 (p3 = 0 shown separately). The [P-WINDOW] calibration: tile u16 box = [gx×128,(gx+1)×128) (u16 = world×2.0 — the deployed foliage-page family), world box = the 64 m adapter tile; edge ownership BY CONSTRUCTION (positions strictly inside the half-open tile box).
- GATES (determinism): repeat-seed identical SHA-256 / changed-seed different; 16-tile order invariance (per-tile + key-sorted union); unique keys + in-box positions + the camera-return regenerate proof; the 5000 cap on the measured high-density case (profile 1 @100%: requested 6,144 → rendered 5,000 → limited 1,144).

## I-21 — server extensions: the bounded model route + the measured support census (NEW endpoints on the Etap D server)

- PATHS: compat/server-world.mjs (M — additive: LazyModelArchive (the LazyTextureArchive design on the pinned Models.bnt), /api/world/model/<id> (bounded single-entry RAW NIF reads + provenance headers + the CAM-C3 identity cache with verifyModelCacheIdentity), decodeModelTextureStrict (the strict 24/32bpp dispatch), buildVegetationSupportCensus (the MEASURED default-profile justification), the /api/world/status vegetation section (the three-way labels + defaultProfile + support census + p3=0 + the 5000 cap), the climates per-record MODEL SUMMARIES, the gaps row vegetation → ETAP_E_DELIVERED with the honest scope, 4 new client-module allowlist entries).
- MEASURED SUPPORT CENSUS (the default profile 0, run at boot once BOTH lazy indexes are READY): 10 distinct models — 8 SUPPORTED with their textures resolved (436293/436300/436223/457579→436225 A32; 457485→457490 A32 — THE WITNESS; 457699→457700 A32; 457523/457532→457525 24bpp), 2 SUPPORTED_UNTEXTURED (166878/166897→166881 = a DDS payload — OUTSIDE the strict subset, honest untextured class), 0 parse-unsupported. Non-visual shapes (the untextured Bip01/Box candidates) counted, never rendered (457523: 1/2; 166878: 3/12; 166897: 1/4 visual).

## I-22 — the client vegetation subsystem (NEW/EXTENDED)

- PATHS: compat/world-vegetation.js (A — WorldVegetation: the per-window deterministic rebuild through PEFoliageLabSeed; the per-model cache + the SHARED texture cache (one fetch+decode per textureId across model entries — object identity measured); per-shape renderables from the extraction (shape→texprop via properties refs→Ark entry→textureId; the Ark 9-byte tail RAW-ONLY); decodeModelTextureStrict; the InstancedMesh builds with REAL per-instance transforms; the 5000 cap in deterministic order; the marker path for UNSUPPORTED models — a MARKER, explicitly NOT an original tree model; the prune discipline) + compat/world-app.js (M — the veg wiring: fetchVegBinary with the client identity check, the bilinear height sampler, rebuildVegetation on window moves + the awaited initial build, the toggle handler, the census/evidence/veg panels, the #veg URL param) + compat/world.html (M — the veg toggle enabled + the honest labels) + compat/launcher.js/launcher.html (M — the profile picker with the per-profile REAL model ids/scales + the MEASURED default justification from the server status + the census-refresh on the late support census landing).
- THE DOUBLE-CONVERSION DEFECT (found by the ETAP_E pixel gate, FIXED): the instance matrices applied the cm→m ×0.01 bridge a SECOND time on top of the per-shape geometry bridge — the trees rendered at 1/50 size (a 1.79 m card → ~5 cm; the gate measured 3/313,900 differing pixels = a no-op toggle). FIXED: the unit bridge applies EXACTLY ONCE (the geometry); the instance scale carries ONLY the node-scale bridge (lerpValue × 2.0 — the deployed foliage-page ratio, labeled CURRENT_RUNTIME_CALIBRATION). After the fix the gate measured 19,621/313,900 differing (6.25%), meanAbsΔ 31.72 — the trees visibly render.

## I-23 — tests + tools (NEW/EXTENDED)

- PATHS: tests/pecompat/world_vegetation.test.mjs (A — the 11 preregistered WORLD_VEG_* gates incl. the headless THREE resource-discipline census through the REAL routes) + world_server.test.mjs (M — the status/gaps/climates/statics gates track the ETAP_E delivered state; waitForWorldReady also waits for BOTH lazy indexes + the support census) + world_headless_load.test.mjs (M — the /world LOAD with #veg=1 + the vegetation DOM markers: the census line żądane/rendered/ograniczone, the VEGETATION_MODE label, the profile/seed labels, p3 separately, the three-way separation) + run_world_tests.mjs (M — the vegetation suite wired in) + tools/pecompat/world_pixel_render.mjs (M — THE CAPTURE-METHOD CORRECTION: the CDP capture replacing the legacy compositor capture; the ETAP_E_VEGETATION_TOGGLE_CHANGES_PIXELS gate; the veg-on/veg-off shots) + world_collect_test_results.mjs (M — the Etap E sections).
- THE CAPTURE-METHOD DEFECT (pre-existing, measured + FIXED in the tool): the LEGACY --screenshot + --virtual-time-budget compositor capture starved late-boot WebGL frames — proven with an in-page toDataURL probe (the vegetation meshes + the splat terrain rendered in the LIVE buffer but were absent/near-black in the compositor capture; the phase-4 world-on pixel profile — 272 unique colors — carries the same signature). FIXED: a CDP capture (remote-debugging on a suite-owned free port — NEVER 9222; a Runtime.evaluate readiness poll on the page's OWN honest census markers + Page.captureScreenshot after a 3 s real-time settle). Both toggle gates re-measured PASS with the corrected method. FAILED-FIRST: the first CDP readiness marker fired at boot (before the streaming window's second rebuild settled) and caught the palette/splat swap in flight (veg-off 370 colors); fixed by polling for the SETTLED state (the 'origin okna: 53,114' census line + the vegetation census line).
- WORKTREE CONVENIENCE (local, gitignored): a node_modules JUNCTION pe-world-launcher-r1/node_modules → eudoria-clean/node_modules (the pinned three 0.185.0 — the package.json dependency; .gitignore already excludes node_modules/) so the Node-side vegetation suite can import the REAL world-vegetation.js with its bare 'three' specifier (the same module instance the browser importmap serves). No repository content changed.
- POST-BATTERY COSMETIC-LABEL EDIT (recorded honestly): after the final battery run, compat/launcher.html's veg-note was reworded to spell the THREE-WAY SEPARATION labels explicitly (ORIGINAL_CLIMATE_RECORDS / RECOVERED_RNG_ARITHMETIC / INSTANCE_DISTRIBUTION — the substance was already there; the explicit English labels now match the /world panel + the artifacts). The final launcher DOM was re-verified against the STANDING server after the edit (8/8 markers: the measured default justification, the per-record model list, the support census counts, the 25-UNSUPPORTED visibility, the LAB_SEED label, VEGETATION_MODE, the three-way labels, the entry button). No gate assertion was affected (the T9 launcher markers are unchanged by the note text; the appendix hash reflects the FINAL file).
- OUTCOME (final code): world battery 44 PASS / 0 FAIL / 0 NOT_PERFORMED (33 Etap C+D gates re-run green + 11 vegetation gates); PIXEL: 5/5 NON_TRIVIAL (CDP) + ETAP_D_TEXTURE_TOGGLE PASS (48.89% differing, re-measured with the corrected capture) + ETAP_E_VEGETATION_TOGGLE PASS (6.25% differing, meanAbsΔ 31.72); regression: unit 24 PASS (the witness-457485 UNTOUCHED guard green), app 22 PASS, catalog 41 PASS; INTERACTION = NOT_PERFORMED (the automation daemon 9222 measured DOWN once — honest).

## I-24 — STANDING SERVER RESTART (my own process only; API changes)

- OLD: world server 127.0.0.1:8162 pid=24412 (the Etap D final code) — STOPPED (Stop-Process -Id 24412; port freed verified).
- NEW: world server 127.0.0.1:8162 pid=24964 (the Etap E final code; started with the documented `npm run serve:world` command shape from the worktree root) — READY measured: census 51,920/51,920; models VERIFIED + index READY (5,596 entries); textures VERIFIED + index READY (8,381 entries); the vegetation support census READY (default profile 0: 8 textured / 2 honest-untextured / 0 unsupported); /api/world/model/457485 → 2,547 B (MISS); /api/world/climates → 31 decoded + 25 UNSUPPORTED with the per-record model summaries. LEFT RUNNING for the user. STOP = Stop-Process -Id 24964 (only this process).
- EDGE RUNS this phase: the battery DOM dumps + the CDP pixel captures (suite-owned Edge instances with dedicated temp profiles + the exact profile-mark leftover cleanup; the 9222 automation daemon was never used or started).

## I-25 — evidence + artifacts (this phase)

- PATHS: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (M: TEST_RESULTS.json regenerated with the Etap E sections by the collect tool — world 44/44, unit 24/24, app 22/22, catalog 41/41, the vegetation gates + the three-way separation + the open findings; WORLD_DATA_PROVENANCE.json extended with ETAP_E_VEGETATION — the profile-selection provenance, the determinism chain, the per-model support census with the same-era import evidence, the render calibration; CALIBRATION_AND_UNKNOWNS.md updated — §2b the vegetation calibration, U-1/U-2/U-12 RESTATED still-UNRESOLVED, U-17..U-20 added; this ledger section; raw/WORLD/WORLD_TESTS_SUMMARY.json (the final 44-gate run) + raw/WORLD/PIXEL_RENDER_ETAPE.json (the CDP captures + both toggle gates) + raw/WORLD_DOM_DUMP_WORLD.html (the vegetation-ON DOM with the veg census) + raw/UNIT/UNIT_TESTS_SUMMARY_ETAPE.json + raw/APP_ETAPE/ + raw/CATALOG/CATALOG_TESTS_SUMMARY_ETAPE.json) + private root 99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER\ (A: pixel_world-veg-on.png, pixel_world-veg-off.png + the refreshed 5-shot set — PRIVATE ONLY).
- OPEN FINDING RECORDED (not fixed — out of Etap E scope): the Etap D splat terrain renders near-black in headless GPU captures (U-19 in CALIBRATION_AND_UNKNOWNS.md; the Etap D toggle gate remains valid — it measures CHANGE; the interactive appearance stays UNVERIFIED while INTERACTION is NOT_PERFORMED).

## Standing interventions (phase 5)

- ONE standing server of MY OWN is deliberately left running for the user: world server
  http://127.0.0.1:8162/ pid=24964 (the Etap E final code; census + both lazy indexes + the
  vegetation support census READY; standing 8140/8161 untouched, verified listening
  before/after).
- No commit/push in this phase. src/pesource + src/peworld/PEFoliageCore.js + NifModelReader.js:
  NO file modified (imported, never edited; verified byte-identical to HEAD by the
  WORLD_VEG_CORE_UNTOUCHED gate + the unit-battery witness guard). The 218757 app +
  catalog/sceneir servers byte-identical and untouched. No package installed (three 0.185.0
  unchanged; the worktree node_modules JUNCTION is a gitignored local convenience). No original
  container modified (terrain.bnt/Textures.bnt/Models.bnt/VegetationClimates.bnt pins verified
  fail-closed at every server start).

## Appendix D — post-edit identities (measured at phase end, 2026-10-10)

```text
src/peworld/PEFoliageLabSeed.js (NEW)                 17385 B  8203950db250a9d28b405e88af297f0bbbb99eb36737d11fee3c64e0024dd2a9
compat/world-vegetation.js (NEW)                      33933 B  2775202149bf3fcce573cf0a8c9fb8448bcb25586cf8864c18400d04ca570a55
compat/server-world.mjs (M)                          110025 B  21fec5c01f355fcc66f0ab474c39108f5635859fbe36c627e135ad6e0e1644cb
compat/world-app.js (M)                               66176 B  7667ec58fcbe5fd1497e215cf969287f9e7cb7a5d6c299d2515cfd4ba2aa71f6
compat/world.html (M)                                 8193 B  207323920a159805bf8770ed08cc69a2299cea1758bab1440b6b0a260e42449f
compat/launcher.js (M)                               26920 B  8b5437608216ddda08057ec69f521291efd13b14d584742bf60602f8bae654fa
compat/launcher.html (M)                              9623 B  0e61b26ab286819dba02edb9bf8553be25e53def8430cab7b025179555f292f8
tests/pecompat/world_vegetation.test.mjs (NEW)       42954 B  fbb967922e5d579738a3b0186a5fa4ac4e85516329b0420ec9e8272b8ffff502
tests/pecompat/world_server.test.mjs (M)             30324 B  109e11ba478f80fa4ff5c3afa1ad579b9c3de1c9b530f607be4b0dc6ba2374bb
tests/pecompat/world_headless_load.test.mjs (M)      12434 B  3374266d027e1c73eb542056add6b2cc5693be8dd8e816afe9c7e36ecc1a1cd4
tests/pecompat/_world_server_helpers.mjs (M)          6755 B  14881aeb0742e071536bb92aa5ba2df8fb0a6afb08c2e5577fd312bbde45428b
tests/pecompat/run_world_tests.mjs (M)                 6071 B  5b9f02ad9f766bf1d7da5d570d931477c9308c84cf5576fba0137e1ac713c404
tools/pecompat/world_pixel_render.mjs (M)             23687 B  4779f613e8fcbbbe5268a9cd6cdff2c9204dfd7288338ac40f30a3acdae6760c
tools/pecompat/world_collect_test_results.mjs (M)    31882 B  6a2bd5fec86778add9c3f27c112da6ee78c98d0294bb1f8974d5b238fa6e243d
```

Unchanged-by-verification (read-only witnesses this phase — verified byte-identical to HEAD by
the WORLD_VEG_CORE_UNTOUCHED gate inside the final battery):

```text
src/peworld/PEFoliageCore.js                          23649 B  300be9137cc1d52c095a0ebecc3741c60041f77ab11eeb0dc100121bea62692f
src/pesource/NifModelReader.js                        29910 B  2c2199545fa6ae62873a3227c6fa1394cd13c8508bd1e0cdb515926079612359
src/pesource/VegetationClimateDecoder.js               6011 B  8dbce904f7d9a2edf72af70c3854a4a24f50b1dc198d22654fdc7a6f9daa6015
src/pesource/TgaDecoder.js                            9067 B  4b6b4baa0fd1529bc876cf915a4078e7b0bae951411b572f78686d788caf6760
```

The four pinned containers: pins verified fail-closed at every server start (terrain.bnt
95841761…; Textures.bnt 61ACD13B…; Models.bnt C950A8C2…; VegetationClimates.bnt 7B858401…) —
originals READ_ONLY. The standing servers 8140 (PID 21288) + 8161 (PID 9588) never touched.

---

# PHASE 6 — U-19 CORRECTION ROUND: THE SPLAT LAYER-COORDINATE + BLEND-FACTOR FIX (post-QC)
(2026-10-10; the bounded correction assigned after the fresh internal QC PASS_WITH_FINDINGS —
QC P2-1 (U-19) + P3-2; no commit/push — persistence stays a later phase.)

## I-26 — the U-19 fix: BOTH splat-shader defects found + fixed (the QC P2-1 root cause + a SECOND, dominant defect the QC had only listed as a candidate)

- PATHS: compat/world-app.js (M — SPLAT_FRAG ONLY; everything else in the file untouched).
- DEFECT (a) — the QC P2-1 root cause, confirmed at code level: the sampler2DArray layer
  coordinate used the NORMALIZED idx byte (texelFetch on the RGBA8 idx DataTextures returns
  byte/255 in [0,1]) — every layer sampled array layer ~0. FIXED with the EXACT decode
  vec4 s0..s3 = floor(i*255.0+0.5): byte k -> array layer k (the idx bytes ARE the texture
  slot numbers; the DataArrayTexture is filled in textureIds order); the empty-slot guard
  (< 254.5) now evaluates the DECODED value (pre-fix it compared the normalized byte against
  254.5 and was always-true, harmless only because empty slots also carry w=0).
- DEFECT (b) — found by THIS round (the DOMINANT cause of the near-black symptom; NOT the
  DataArrayTexture-upload candidate): the sequential-lerp blend factor was DOUBLE-DIVIDED —
  texelFetch on the RGBA8 weight texture ALREADY returns the RAW mask NORMALIZED (mask/255,
  the preset's documented factor), and the shader divided by 255 AGAIN (w0.x / 255.0 =
  mask/65025), collapsing every blend to ~tex*0.004 = the near-black [0..3] pixels. FIXED:
  the factor is the as-fetched normalized weight (w0.x — bit-exact the RAW served byte).
- THE DIAGNOSTIC TRAIL (honest, measured — every probe ran against the standing server from
  the temp dir, none of it in the repo): after fix (a) the per-color gate STILL failed (36
  valid samples, meanDeltaFixed 140.91 — the read pixels still near-black), proving a second
  independent defect (exactly the QC's anticipated "and/or" candidate class). A ~20-variant
  in-page GPU bisection on the real mesh + real data then RULED OUT: the uploads
  (texStorage3D/texSubImage3D measured 256x256x23/28 with the real Stone04 bytes — the
  probe4 "1x1x1" reading was MY OWN spy's mislabeled field mapping), the texture-unit
  bindings (unit 0 = array, units 1-8 = idx/w, uniform1i [0..8] correct, no conflicts), the
  sampler2DArray sampling itself (a fixed-layer-3 sample renders the exact Rock03d colors
  [139,137,129]), texelFetch on the idx/w textures (reads 255/0 as expected), the
  browser-side decodeTga2 (mean [102,92,74] — identical to Node), the floor/decode
  arithmetic, the wrap/large-uv handling (fract(uv) identical), the 'any' variable name,
  textureLod, and a padded-2D-atlas restructure (built + measured — rendered the same
  near-black while the factor bug remained, which finally exposed it). Probe-side defects
  found and fixed during the bisection: a y-flipped readRenderTargetPixels readback, an
  unsubstituted template-literal shader extraction, the spy field mapping — all confined to
  the temp dir, never the repo. LESSON RECORDED: normalized-byte readbacks carry the value
  ONCE in normalized form — an extra /255 silently rescales; the QC's P2-1 layer-coordinate
  diagnosis was CORRECT but INCOMPLETE — the same 16 lines carried a second defect that only
  a per-color pixel gate could catch (the CHANGE-based toggle gate cannot).
- OUTCOME (measured, all green): see I-27/I-28.

## I-27 — the per-color revalidation gate (NEW tool) + the pixel/battery re-runs

- PATHS: tools/pecompat/world_splat_per_color.mjs (A — the NEW WORLD_U19_* gate tool; the
  QC-required per-color revalidation: raycast-expected vs read-capture-pixel comparison with
  the layer-mapping control + the pre-fix-rejection negative control + the pre/post canvas
  census) + tools/pecompat/world_pixel_render.mjs (UNCHANGED this round — re-run as-is) +
  the four battery harnesses (UNCHANGED — re-run as-is).
- GATES (raw/WORLD/WORLD_SPLAT_PER_COLOR_U19FIX.json): WORLD_U19_PER_COLOR_EXACT PASS —
  36 valid samples / 36 distinct cells, EVERY read capture pixel within the INDEPENDENTLY
  recomputed exact shader-math color span (Node: the same wire payloads through
  PETerrainRegion/buildRegionSplatData/decodeTga2 + the bilinear/lerp replication at the
  ray-hit world position; the camera pose cross-checked against the page's live position
  HUD; the page's applied-splat chain census cross-checked against the independent build):
  meanDeltaFixed 0.55/255, max 1.39/255 (the fp32 bilinear rounding floor).
  WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED PASS — the pre-fix expectation does NOT match the
  read pixels (34 discriminating samples, mean max-channel delta 65.95; every
  discriminating sample closer to the fixed expectation) — a still-broken shader FAILS
  this control. WORLD_U19_LAYER_MAPPING_CONTROL PASS — 0 bad slot bytes; layer k maps to
  texture slot k proven BY THE RENDER. WORLD_U19_HEADLESS_NOT_NEAR_BLACK PASS — the
  canvas-region census pre->post: uniqueColors 370 -> 65,240, lumaMean 12.2 -> 90.67,
  lumaMax 253 (real TGA-derived colors; the pre-fix Etap E private capture kept as the
  comparison baseline).
- PIXEL RE-RUNS (raw/WORLD/PIXEL_RENDER_U19FIX.json; private root BROWSER\U19FIX\): 5/5
  shots NON_TRIVIAL; the ON captures now show the REAL texture colors (world-veg-off canvas
  65,240 colors vs 370 pre-fix; world-on 73,224 vs 10,824 pre-fix); ETAP_D_TEXTURE_TOGGLE
  re-measured PASS (48.86% differing, meanAbsD 62.43); ETAP_E_VEGETATION_TOGGLE re-measured
  PASS (6.26% differing, meanAbsD 58.86).
- FULL REGRESSION with the fixed shader: world 44/44, catalog 41/41, unit 24/24, app 22/22
  (raw/U19FIX/*; the Etap E raw summaries remain on disk as the pre-fix provenance).
- EDGE RUNS this round: the per-color tool (1 suite-owned CDP instance) + the pixel tool
  (5 suite-owned CDP instances) + the world battery's T9 headless loads + the app/catalog
  battery browser loads — all suite-owned Edge instances with dedicated temp profiles,
  killed + port-freed proofs inside each lifecycle record; the 9222 automation daemon was
  never used; INTERACTION remains NOT_PERFORMED (honest).

## I-28 — the artifacts + the skill status (P3-2)

- PATHS: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (M: CALIBRATION_AND_UNKNOWNS.md — the
  U-19 row OPEN -> RESOLVED with the full fix description + the per-color gate evidence +
  the honest INTERACTION caveat kept; TEST_RESULTS.json REGENERATED by the extended
  world_collect_test_results.mjs (the u19SplatLayerFix section + the etapERecord/
  u19FixRecord provenance split + the correction-round failedFirstRuns entry); this ledger
  section) + tools/pecompat/world_collect_test_results.mjs (M — the U19FIX sections;
  prefers the correction-round summaries for the CURRENT state, keeps the Etap E raws as
  provenance) + .opencode/skills/pe-gamebryo-rosetta/SKILL.md (M — the P3-2 correction:
  "serve:world is PLANNED, not yet built" -> DELIVERED with the npm run serve:world
  command reference + the run pointer; the terrain-foliage-integration.md Etap-B wording
  kept as the historical phase record).
- STANDING SERVER 8162: NOT RESTARTED — PID 24964 unchanged; the server serves the static
  compat/world-app.js FROM DISK per request (measured: the served bytes byte-identical to
  the fixed disk file after BOTH fix stages); the raw-data caches are untouched by the fix.
  The foreign standing servers 8140 (PID 21288) + 8161 (PID 9588) never touched (verified
  listening before and after every suite).

## Standing interventions (phase 6)

- ONE standing server of MY OWN remains running for the user: world server
  http://127.0.0.1:8162/ pid=24964 (the Etap E final code + the fixed world-app.js served
  from disk; census + both lazy indexes + the vegetation support census READY; standing
  8140/8161 untouched).
- No commit/push in this phase. No src/pesource, src/peworld, src/pecompat, compat (other
  than world-app.js), tests, server or 218757 file modified. No package installed. No SDK
  file touched. No original container modified (the batteries' hash/pin witnesses all
  green through the re-runs). The temp-dir diagnostic probes were deleted after use.

## Appendix E — post-edit identities (measured at phase end, 2026-10-10)

```text
compat/world-app.js (M — SPLAT_FRAG only)              67532 B  15113b26b1f2aa53997bd5bfde1d7b56ef53ccaf410426bb8bab31bed599db6a
tools/pecompat/world_splat_per_color.mjs (NEW)       42105 B  2e3af98be08fa07ea47840f975f17630ed328d35dfe9e14d6786bc524b71ca59
tools/pecompat/world_collect_test_results.mjs (M)    43137 B  0a8b79831bc27a27be447ddffaa8e0dd47b325f9c26f746f76e9da6bea3631d2
.opencode/skills/pe-gamebryo-rosetta/SKILL.md (M)     8145 B  2127a9918bc03d580b891834ec295c6da3f2d6c5c79f66c1c60318b840652b78
```

Unchanged-by-verification (this phase): compat/world-splat.js (94d4e40b… — the pure builder
and the preset stay byte-identical), compat/server-world.mjs (21fec5c0… — untouched), the
four pinned containers (the battery witnesses green), the 218757 app + the catalog/sceneir
servers, the standing 8140/8161 servers.
