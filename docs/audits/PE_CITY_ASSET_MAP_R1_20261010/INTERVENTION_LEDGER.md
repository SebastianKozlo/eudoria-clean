# INTERVENTION_LEDGER.md — PE_CITY_ASSET_MAP_R1_20261010

APPEND-ONLY ledger of every process/filesystem intervention by this executor (phase 1: SETUP_T9_FIX_BROWSER_LOAD; phase 2: METADATA_CATALOG — see the phase-2 section at the bottom). Foreign work is NEVER touched. Times are local 2026-10-10 (phase-1 session window ≈ 01:45–02:40; phase-2 session later the same day).

## Foreign processes — explicitly NEVER touched (verified before AND after all work)

- **Standing reference server: port 8140, PID 21288** (`node.exe compat/server-sceneir.mjs` — belongs to the old SceneIR worktree's standing server). READ_ONLY reference; never written to, never killed, never bound over. Verified LISTENING before work, after the PRE run, after all POST runs, and at phase end (final census: it is the ONLY `server-sceneir` process alive).
- Old SceneIR worktree `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1` — never entered for writes.
- Canonical checkout `eudoria-clean` foreign untracked paths (`docs/audits/PE_935_*`, `experiments/`) — untouched.
- Playwright automation daemon port 9222 — down (see INTERACTIVE below); nothing to touch.
- Temp profile dirs `pec-sceneir-headless-profile-*` created 00:47–01:39 (BEFORE this session) — not created by this executor's runs (my PRE stand-in run never launched a real browser and created no profile); left untouched as foreign material.

## Filesystem interventions

| # | Time | Action | Path | Notes |
|---|---|---|---|---|
| F1 | ~01:47 | git worktree add | `D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1` from `59641ca` on new branch `codex/pe-city-asset-map-r1-20261010` | the SINGLE allowed write in the canonical checkout; worktree clean at creation |
| F2 | ~01:50–02:35 | report package + raw evidence writes | `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/**` (in the new worktree) | PRE/POST/POST_STANDIN/PIXEL raw evidence, console captures, summaries, this ledger + docs |
| F3 | ~02:15–02:35 | PRIVATE_OUTPUT writes | `D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\PIXEL_RENDER\T9_PIXEL_RENDER_ASSET_MODE.png` + PIXEL_RUN metadata | private only — never in the repo |
| F4 | 01:52–01:55 | probe scripts (temp) | `C:\Users\User\AppData\Local\Temp\opencode\city_asset_probe\edge_probe.mjs`, `edge_modes_probe.mjs` + results + 2 full-mode DOM captures | exploratory Edge-behavior probes (before finalizing the fix); kept as evidence |
| F5 | ~02:38 | cleanup of MY probe temp profile dirs | `7 × city-asset-edge-*` dirs in `%TEMP%\opencode` | removed, 0 remaining |

## Process interventions — every spawned process bounded, tracked, stopped, port-freed-verified

| # | Run | Server child (pid/port/lifetime/freed) | Browser/other child (pid/lifetime/exit) | End state |
|---|---|---|---|---|
| P1 | PRE harness (OLD defective code; `PECOMPAT_BROWSER_BIN=node.exe`) | T7: pid 24260, port 8753, 745 ms, freed. T9: pid 15928, port 8141, ~10 s, freed (old code freed via stopServer) | stand-in `node.exe` (spawned by OLD code): 57 ms, exit 9, empty DOM | harness exit 0, 13 PASS incl. the reproduced false-PASS; nothing left |
| P2 | blocked `Start-Process` attempt (probe server) | MY OWN ORPHAN node pid 16536, port 8160 | — | the tool policy blocked the detached spawn; orphan detected and **killed by me** (Stop-Process), port verified freed — honest self-cleanup of my own writer |
| P3 | Edge behavior probe #1 (`edge_probe.mjs`) | server pid 15604, port 8160, ~28 s, killed at script end, freed | Edge A (about:blank): timeout 75 s → killed; B/C/D (`--dump-dom`): ~0.9–1.0 s, exit 0, full 21064 B DOM; E (`--screenshot`): 75 s timeout → killed, FILE WRITTEN (112588 B) | 0 leftover Edge (cmdline census), port freed |
| P4 | Edge modes probe (`edge_modes_probe.mjs`) | server pid 10792, port 8160, ~7 s, killed at script end, freed | Edge asset mode: 1067 ms exit 0 (21064 B); Edge #scene mode: 828 ms exit 0 (9309 B) | port freed, no leftovers |
| P5 | POST harness run 1 (FIXED code, intermediate) | T7: pid 11672, port 8631, 724 ms, freed. T9: pid 15224, port 8160, 93096 ms, freed | Edge asset mode: clean exit, PASS. Edge #scene mode: **timed out at 90 s AFTER a complete valid 9309 B READY capture** → killed (flaky Edge exit; recorded; bounded retry added afterward) | 2 FAIL (1 = my defective synthetic NO_DIAGNOSTICS input caught by its own control; 2 = the flake) — run preserved as `raw/T9/POST_RUN1_INTERMEDIATE*` |
| P6 | POST harness run (FIXED code, final) | T7: pid 19516, port 8275, 758 ms, freed. T9: pid 24324, port 8160, 3759 ms, freed | 2 × Edge (`/` and `/#scene`): both clean exits, exit 0, full DOM, all 5 conjuncts each | harness exit 0, 22 PASS / 0 FAIL |
| P7 | POST_STANDIN harness run (FIXED code; `PECOMPAT_BROWSER_BIN=node.exe`) | T7: pid 20772, port 8893, 747 ms, freed. T9: pid 6072, port 8160, 2414 ms, freed | 6 × node.exe stand-in (3 attempts × 2 modes): each exit 9, 0 B DOM | harness exit 1 (nonzero on FAIL), 2 FAIL records with all five named missing conjuncts + STAND_IN_PROCESS labels |
| P8 | PIXEL_RENDER tool (`t9_pixel_render.mjs`) | server pid 13504, port 8160, 2542 ms, killed by tool, port freed after 33 ms | Edge `--screenshot`: file written after ~14 s, process did NOT exit on its own (known measured quirk) → killed by tool + profile-mark Edge census: 0 leftovers | tool exit 0, PNG → PRIVATE_OUTPUT only |
| P9 | Unit regression (`run_tests.mjs --models …`) | none (in-process model load only) | none | 24 PASS / 0 FAIL, exit 0 |
| P10 | INTERACTIVE availability check | — | 2 × bounded `fetch` to `127.0.0.1:9222` and `[::1]:9222` | both ECONNREFUSED → INTERACTIVE = NOT_PERFORMED |

## End-of-phase census (bounded verification, no assumptions)

- Edge processes carrying ANY of my profile marks (`pec-city-asset-map-headless`, `pec-city-asset-map-pixel`, `city-asset-edge-probe`, `city-asset-edge-modes`): **0**.
- `node.exe` running `server-sceneir.mjs`: **exactly 1 — PID 21288 (the FOREIGN 8140 reference — untouched, still LISTENING)**. All MY server processes are stopped.
- Ports: 8160 free; 8753/8631/8275/8893 (random fallback ports used by T7) all freed per per-run port-freed proofs; 8140 still owned by PID 21288 (foreign).
- No untracked writer of mine remains.

## Honest deviations / self-corrections recorded

1. P2: my first attempt to start a probe server as a detached process was blocked by the tool policy and left an orphan (pid 16536); I detected and killed it myself before any subsequent work — the correct pattern (single bounded driver process per command) was used for every later run.
2. P5: my first synthetic NO_DIAGNOSTICS negative input removed two conjuncts at once (diagnostics marker and status attribute shared one element); the control itself caught the error ("WRONG conjunct set") — fixed by separating the synthetic markers; the intermediate run preserved as evidence.
3. P5: real Edge once refused to exit after a complete valid #scene capture (flaky host/browser behavior, not a page defect); handled by a bounded transparent retry (max 3 attempts, all recorded per attempt; the strict per-attempt predicate unchanged).

---

## PHASE 2 � METADATA_CATALOG (both eras + rankings; same day 2026-10-10)

No servers, no ports, no browsers were started in this phase: every run below was a SINGLE bounded `node` process with an explicit tool-level timeout, reading only READ_ONLY originals + writing only PRIVATE_OUTPUT / the report package / `tools/pecompat/` (allowlist).

### Filesystem interventions (all inside the allowlist or designated temp)

| # | Action | Path | Notes |
|---|---|---|---|
| F6 | NEW phase-2 tools (7 files) | `tools/pecompat/catalog_census.mjs`, `catalog_sniff.mjs`, `ark_index.mjs`, `bnt_index.mjs`, `vfs_inspect.mjs`, `nif_batch_extent.mjs`, `catalog_rankings.mjs` | non-proprietary code only; REUSED era-validated readers imported UNCHANGED from `src/pesource/` + `src/pecompat/` (labels in CATALOG_METHOD.md) |
| F7 | PRIVATE_OUTPUT phase-2 dirs + 20 artifacts | `D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\PHASE2_{CENSUS,CATALOGS,VFS,EXTENT,RANKINGS}\` | full censuses/catalogs/rankings/batch-state/vfs-inspections � never the repo; each referenced by path+SHA256 in CATALOG_COVERAGE.json |
| F8 | report package writes | `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/CATALOG_COVERAGE.json`, `CATALOG_METHOD.md`, this ledger append | metadata only � NO proprietary payloads |
| F9 | temp probe scripts (kept as evidence) | `C:\Users\User\AppData\Local\Temp\opencode\city_asset_phase2\err_census.mjs`, `nomesh_probe.mjs` | small read-only analysis scripts over my own private outputs; no processes left running |

### Process interventions (each row = one bounded `node` run; all exited on their own; 0 leftovers)

| # | Run | Wall clock | End state |
|---|---|---|---|
| P11 | `catalog_census.mjs --era CD_2003` | 373 ms | 4/4 files OK, exit 0 |
| P12 | `catalog_census.mjs --era PCG_9_3_5` | 6.6 s | 1818/1818 files OK (2.38 GB streamed+hashed), exit 0 |
| P13 | `ark_index.mjs` Models.ark (pin verified) | 481 ms | 2492 entries catalogued, CRC 100%, exit 0 |
| P14 | `ark_index.mjs` Textures.ark (pin verified) | 1.2 s | 4833 entries catalogued, CRC 100%, exit 0 |
| P15 | `bnt_index.mjs` Models.bnt (PIN MATCH) | 1.4 s | 5596 entries catalogued, CRC 100%, exit 0 |
| P16 | `bnt_index.mjs` Textures.bnt (pin verified) | 3.8 s | 8381 entries catalogued, CRC 100%, exit 0 (peak RAM = one 974 MB buffer, bounded single process) |
| P17 | `vfs_inspect.mjs` (3 vfs files) | <1 s | all 3 identity MATCH, ArkVFS02 confirmed, exit 0 |
| P18 | `nif_batch_extent.mjs --limit 100` (probe) | 0.6 s | 100 candidates processed (16 DECODED / 84 FAILED � loud unregistered block types), state JSONL appended per file, exit 0 |
| P19 | `nif_batch_extent.mjs` (full, resumed from state) | 2.9 s | 4738 more processed ? totals 4838 = 1551 DECODED + 17 no-mesh + 3270 FAILED; max single file 19 ms; exit 0 |
| P20 | `catalog_rankings.mjs` (4 runs: 1 syntax-fix, 1 label-fix after reclassification, 2 final) | <2 s each | CATALOG_COVERAGE.json built + rebuilt; final run verified below |
| P21 | ephemeral `node -e` / temp-script probes (5) | ms-scale | read-only checks over my own outputs (218757 pin cross-check, no-mesh census, error census); all exited 0 |

### Phase-2 end census

- Foreign reference server port 8140 / PID 21288: verified STILL LISTENING and untouched (final `netstat`+process census at phase end — same single `server-sceneir` process as phase 1).
- My own `node.exe` processes: NONE left running (all runs single-shot, exit-verified).
- No ports bound by this phase at any point.
- Git worktree state: only allowlisted paths touched (see FINAL HANDOFF for the changed-path census).

---

## PHASE 3 — FOUR_MODELS_DEEP_ANALYSIS (2026-10-10, same worktree)

No web servers, no browsers, no ports were started in this phase. One NATIVE third-party tool was executed headless (the stock GB 1.2 printer — the ORIGINAL_NATIVE_EXECUTION control layer, CHILD_PROCESS_PATH_DLL_EXPOSURE class, identical provenance capture to the SceneIR controlB run: sandbox-local MSVCP71/MSVCR71 resolved via the CHILD process PATH only, 30 s per-process timeout, argv/cwd/env-delta/exe-SHA/exit/stdout/stderr captured per run).

### Filesystem interventions

| # | Action | Path | Notes |
|---|---|---|---|
| F10 | NEW phase-3 tools (6 files, allowlist `tools/pecompat/`) | `nif41_deep.mjs`, `phase3_extract_primaries.mjs`, `phase3_renders.mjs`, `phase3_pcg935_name_batch.mjs`, `phase3_collect_rows.mjs`, `phase3_texture_dispositions.mjs` | bounded NIF-4.1 reader (for the four primaries only) + extraction/renders/texture-batch/collectors; REUSED unchanged: `src/pesource/ArkArchive.js`, `src/pesource/Bnt2Archive.js`, `src/pecompat/PecNif10Reader.js`, `src/pecompat/PecSceneIR.js` (buildAssetIR/validateSceneGraph/composeWorldTransforms/computeSceneBounds), `src/pecompat/PecTransform.js` |
| F11 | PRIVATE_OUTPUT phase-3 dirs + artifacts | `PHASE3_MODELS/` (4 extracted .nif payloads), `PHASE3_BlockDumps/` (4 block-dump JSON + 4 parts CSV), `PHASE3_Renders/` (12 PNG + RENDER_MANIFEST.json), `PHASE3_NativeControl/` (exe+DLL copies, run_records.json, 8 stdout/stderr captures, the run script), `PHASE3_PCG935_BATCH/` (NAME_EDGES.jsonl 4,151 rows, batch summary, candidate probe JSON), under `D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\` | never the repo; proprietary payloads stay private |
| F12 | report package writes | `DEEP_ANALYSIS.md` (NEW), `PRIMARY_MODEL_ROWS.json` (NEW), `TEXTURE_LINK_DISPOSITIONS.csv` (NEW, ASCII-only, 1,588 data rows), `CATALOG_COVERAGE.json` (phase-3 extension: primaryModels rows measured, CD_2003 coverage 0→4, phase-2 ranking tables untouched), this ledger append | metadata only — no proprietary payloads |
| F13 | temp verification file | `$env:TEMP\p3_redump.json` | my own tool output re-parsed for verification; leftover in TEMP, harmless |

### Process interventions (each bounded, tracked, stopped)

| # | Run | Class | End state |
|---|---|---|---|
| P22 | `phase3_extract_primaries.mjs` (Ark read + SHA fail-closed) | node, single-shot | 4/4 extracted, all pins MATCH, exit 0 |
| P23 | `nif41_deep.mjs` — first run (pre-correction) | node | 4× LOUD FAIL at the Ark blocks (measured first systematic failure; honest, recorded) |
| P24 | `nif41_deep.mjs` — corrected reader (the ONE bounded repair; SDK NiExtraData base reconciled with the historical lineage; READER_VALIDATION NOTE in the tool header) | node, 3 executions (regenerate dumps) | 4/4 DECODED full closure; exit 0 |
| P25 | `nif_parser_v2.py` × 4 payloads (PYTHON DUAL-DECODE cross-check; the historical parser is READ_ONLY reference material, executed from its own location, never modified) | python, single-shot | agreement on all standard blocks/names/refs/geometry (see DEEP_ANALYSIS.md §1.4); its NiVertexColorProperty unknown-type + footer omission recorded |
| P26 | `phase3_native_run.ps1` → stock `SceneGraphPrinter.exe` × 4 models (ORIGINAL_NATIVE_EXECUTION; CHILD_PROCESS_PATH_DLL_EXPOSURE) | native child processes, 30 s timeout each | 4× EXITED exit=1 `Error loading stream.` (NATIVE_LOAD_REJECTED — measured honestly; no timeouts, no crashes, no leftover processes; stdout 0 B each) |
| P27 | `phase3_renders.mjs` | node | 12 PNG + manifest written to PRIVATE_OUTPUT; exit 0 |
| P28 | `phase3_pcg935_name_batch.mjs` (Models.bnt PIN verified; 1,551 models re-parsed with the EXISTING reader — no new decode) | node, ~9 s | 1,551/1,551 processed, 0 parse errors, 4,151 edges; exit 0 |
| P29 | `phase3_collect_rows.mjs` + `phase3_texture_dispositions.mjs` | node × 2 | PRIMARY_MODEL_ROWS.json + TEXTURE_LINK_DISPOSITIONS.csv written; exit 0 |
| P30 | cross-era candidate probe (9 PCG935 4.1 models, bounded CANDIDATE probe with the phase-3 reader) | node -e (in-process, no files written to originals) | 2 DECODED (generic names — no kinship), 7 PROBE_FAILED loud (recorded verbatim); CROSS_ERA_CANDIDATE_PROBE.json written |
| P31 | `png_nontrivial.mjs` (module import) render verification | node -e | renders decode OK, correct dimensions, non-blank content |

### Phase-3 end census

- Foreign reference server port 8140 / PID 21288: still the ONLY `server-sceneir` process; never touched (re-verified at phase end).
- My own `node.exe`/`python.exe` processes: NONE left running; the 4 native printer children all exited on their own (exit 1); no ports bound by this phase at any point; no untracked writer remains.

---

## PHASE 4 -- CATALOG_MODE_SERVER_TESTS (2026-10-10, same worktree)

No web servers of others, no browsers of others, no foreign ports touched. The foreign reference server **port 8140 / PID 21288 was re-verified LISTENING and untouched before AND after every work item below** (final census at phase end: still the ONLY `server-sceneir` process; the catalog server refuses 8140 BY CONSTRUCTION).

### Filesystem interventions (all inside the allowlist or designated temp)

| # | Action | Path | Notes |
|---|---|---|---|
| F14 | NEW phase-4 server + app (7 files, `compat/`) | `compat/server-catalog.mjs`, `catalog.html`, `catalog-app.js`, `catalog-table.js`, `catalog-preview.js`, `catalog.css` | the /catalog mode + bounded loopback server (extends the sceneir design, labeled); the EXISTING app files byte-identical (git diff empty: app.js, index.html, asset-mode.js, scene-mode.js, api.js, server-sceneir.mjs, src/) |
| F15 | NEW phase-4 tools (5 files, `tools/pecompat/`) | `catalog_data.mjs`, `texture_chain.mjs`, `catalog_pixel_render.mjs`, `phase4_texture_dispositions_update.mjs`, `phase4_collect_test_results.mjs` + ONE additive export in `nif41_deep.mjs` (ir/worldTransforms for the wire builder; no analysis value changed) | REUSED unchanged: ArkArchive, Bnt2Archive, catalog_sniff, png_nontrivial, the phase-3 reader, PecSceneIR composition |
| F16 | NEW phase-4 tests (9 files, `tests/pecompat/`) | `_catalog_server_helpers.mjs`, 7 gate suites, `run_catalog_tests.mjs` | REUSED unchanged: the FIXED T9 gate (`evaluateLoadGate` imported from headless_load.test.mjs), `_app_server_helpers.mjs` generic exports |
| F17 | package.json | `serve:catalog` + `test:pecompat:catalog` scripts | three stays pinned 0.185.0; NO new dependencies |
| F18 | PRIVATE_OUTPUT | `PIXEL_RENDER_CATALOG/` (5 PNGs incl. all four primary previews; calibration captures overwritten by the gate captures) | never the repo; SHA256 + stats recorded in the raw JSON |
| F19 | report package | `CATALOG_UI_NOTES.md`, `TEST_RESULTS.json`, `raw/CATALOG/**` (gate summaries, DOM dumps, HTTP transcripts, PIXEL calibration + run records), `TEXTURE_LINK_DISPOSITIONS.csv` (19 material rows updated per the real-render observation), this ledger append | metadata only -- no proprietary payloads |
| F20 | temp debug scripts (kept as evidence) | `$TEMP\opencode\pec_catalog_domprobe.mjs`, `pec_catalog_pixelprobe.mjs`, 2 headless Edge DOM dumps + temp profiles `pec-catalog-debug-*` (removed after use) | read-only diagnostics over MY OWN outputs |
| F21 | skill update (contract SS6) | `.opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md` (NEW) + SKILL.md pointer | concise catalog/era-identity/texture-provenance chapter; source+scope per claim; no "engine 100% known" claims |

### Process interventions (every spawn bounded, tracked, stopped; port-freed proofs recorded in the gate records)

| # | Run | Server child (pid/port/lifecycle) | Browser/other child | End state |
|---|---|---|---|---|
| P32 | catalog battery development runs (`run_catalog_tests.mjs` x4 full + 2 partial) | per run: suite-owned catalog server (~11 s lifetime each, ports 8161/8160 fallback; killed by suite, port-freed verified per record) | 2 x headless Edge per T9-style run (table + preview loads; dedicated `pec-city-asset-map-catalog-headless-*` temp profiles; profile-mark leftover cleanup each attempt) | final run: 33 PASS / 0 FAIL / 0 NOT_PERFORMED; no leftovers |
| P33 | 218757 regression (phase-end re-run) | T7/T9 suite-owned sceneir servers (ports random 82xx/8160; killed, freed) | 2 x Edge (asset + #scene; all 5 conjuncts each) | unit 24 PASS exit 0; app 22 PASS exit 0 |
| P34 | PIXEL calibration runs x2 | suite-owned catalog server (pid per run; killed by tool; port freed) | 5 x Edge `--screenshot` per run (poll-file + size-stability; killed by tool on the measured hang-quirk; profile-mark Edge census 0 leftovers) | calibration stats measured + recorded; thresholds frozen |
| P35 | PIXEL gate run | catalog server (pid, port 8161, killed by tool, port freed after 11 ms) | 5 x Edge `--screenshot` (table + all four primary previews) | STATUS PASS (5/5 shots, all thresholds) |
| P36 | my DEBUG server for live-page inspection | `cmd start /B node compat\server-catalog.mjs` -- **detached spawn (PID 24116, port 8161)**: my own process, tracked from creation | -- | **killed by me** (Stop-Process -Id 24116), port verified released (no LISTENING remains; only TIME_WAIT sockets) |
| P37 | debug DOM dumps x2 (1280x800, preview deep link) | (against the P36 server) | 2 x headless Edge (temp profiles `pec-catalog-debug-1/2`) | both exited; profiles removed |
| P38 | INTERACTIVE availability checks | -- | bounded TCP probes to 127.0.0.1:9222 + [::1]:9222; plus ONE session browser-automation navigation attempt | ALL ECONNREFUSED (daemon down) -> INTERACTIVE = NOT_PERFORMED honestly |

### Honest deviations / self-corrections recorded (phase 4)

1. A `Start-Process` attempt for the debug server was BLOCKED by the tool policy (same class as phase-1 P2); the command never ran (no orphan). The bounded `cmd start /B` spawn was used instead, the PID tracked, and the process explicitly killed by me at the end (P36) -- the only detached process of this phase, start/stop both by me, port-release verified.
2. UI defect found + fixed by measurement (the pixel-render calibration caught it): the first preview screenshots showed a nearly-solid canvas region (2 unique colors). Root cause: `#catalog-layout` had a height but NO `grid-template-rows` -- the implicit row grew to content (document scrollHeight 6,970 px; canvas 4538 px tall) pushing the preview below the fold. Fixed with the proven pattern (`flex:1` + `grid-template-rows: minmax(0,1fr)` + `min-height:0` flex/grid items); re-measured: document scrollHeight == viewport, canvas region 373-403 unique colors, all four previews render. The two calibration runs are preserved (raw/CATALOG/PIXEL_CALIBRATION{,2}.json) as PRE evidence.
3. A cosmetic boot-order defect found by the DOM probe: the final `hud(...)` call overwrote the preview hud after the deep link -- fixed (conditional); re-verified in the final battery.


---

## PERSISTENCE-PHASE CORRECTIONS AND INTERVENTIONS (append-only; 2026-10-10, the SS8 persistence session)

This section was appended by the SS8 persistence phase (pe-master-auditor worker; NOT the executor).
Every historical row above — including the F12 row corrected below — is preserved UNCHANGED
(append-only discipline; no history rewrite). Corrections follow the fresh internal QC REVIEW.md
findings (QC verdict PASS_WITH_FINDINGS; PE-MASTER-confirmed) and are fully documented with
PRE/POST SHA256 hashes in 00_CONTROL_INTERNAL_QC/AMEND_LOG.md.

| # | Corrects / records | Correction text | Authority / evidence |
|---|---|---|---|
| C1 | F12 (phase-3 filesystem table row) | TEXTURE_LINK_DISPOSITIONS.csv data rows: **1,587** (42 CD_2003 + 1,545 PCG_9_3_5; header excluded), not 1,588 as F12 stated. The file is UTF-8, not ASCII-only: the 19 phase-4 material rows carry a UTF-8 em-dash (U+2014; 0x2014). The F12 count was most likely a header-inclusive miscount. F12 itself stays unchanged. | QC REVIEW.md P3-1 (strict recount); re-verified at persistence after the P2-1 quoting fix: strict RFC4180 parse, 1,587 data rows, every row exactly 7 fields, sums unchanged (3,357 NAME_NOT_FOUND / 794 material refs / 4,151 edges / 1,545 models with edges / 6 edge-less). |
| C2 | F12-created file TEXTURE_LINK_DISPOSITIONS.csv (machine-readability; QC P2-1) | At persistence the 1,545 PCG_9_3_5 aggregated rows' container_entry values were RFC4180-quoted ("Textures.bnt (8,381 entries)"); NO disposition value altered; row count and all aggregate sums unchanged (strict parse revalidation PASS: 7 fields x 1,587 data rows). | QC REVIEW.md P2-1; AMEND_LOG.md entry 1. |
| C3 | PRIVATE_OUTPUT PHASE3_NativeControl/run_records.json (QC P3-3) | The UTF-8 BOM (EF BB BF) was stripped; content bytes otherwise identical (3,497 B after strip). Strict JSON.parse now succeeds. The file is PRIVATE (never the repo); no record content altered. | QC REVIEW.md P3-3; AMEND_LOG.md entry 4. |
| C4 | .opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md (QC P3-2) | The nonexistent overlap example "656865.nif" was replaced with the verified overlap example "266865.nif" (both 266865.nif and 65678.nif verified present in BOTH era model catalogs; 656865.nif present in NEITHER). | QC REVIEW.md P3-2 + QC14/QC15; persistence-phase independent re-verification against both phase-2 catalogs. |
