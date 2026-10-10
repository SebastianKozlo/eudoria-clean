# INTERNAL_REVIEW — PE_WORLD_LAUNCHER_R1_20261010 (phases 1–5)

```text
RUN_ID            = PE_WORLD_LAUNCHER_R1_20261010
PHASE             = INTERNAL_QC (fresh internal QC of the completed executor work, phases 1–5)
QC_ORIGIN         = FRESH_INTERNAL_REVIEW (pe-master-auditor, own session, no prior context;
                    internal to PE-MASTER — NOT a Desktop post-audit, NOT independent external QC)
QC_PERFORMED_AT   = 2026-10-10
GOVERNING_CONTRACT= OPENCODE_PE_WORLD_LAUNCHER_R1_20261010.md (27507 B,
                    SHA256 30ACECDF063D7CBCF6BFC9FD2169236783BEA60052B850CE613BC6330C4C5B63 — re-verified MATCH by QC)
WORKTREE          = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1 @ e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c
                    (branch codex/pe-world-launcher-r1-20261010; HEAD verified == the dispatch requirement;
                    the run work is the uncommitted tree delta; no commit/push performed by QC)
QC_OUTPUTS        = 00_CONTROL_INTERNAL_QC/ (this directory; all QC re-executions read-only
                    against the originals, my outputs stored ONLY here + the private PNG under
                    99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER_QC_R1\)
```

## 0. Verdict summary

```text
QC_VERDICT                    = PASS_WITH_FINDINGS
PRODUCT_VERDICT_RECOMMENDATION= PASS_IN_IMPLEMENTED_SCOPE
                                (with the two standing qualifiers the contract itself separates:
                                 INTERACTION = NOT_PERFORMED (honest, daemon 9222 down);
                                 U-19 splat-appearance OPEN — see P2-1; never present as "all green")
FINDINGS                      = 0 P0 / 0 P1 / 1 P2 (OPEN, executor-recorded as U-19; QC CONFIRMED its
                                root cause at code level) / 3 P3 (1 REPAIRED by QC with PRE/POST +
                                live revalidation; 2 REPORT-only)
REPAIRS_PERFORMED             = 1 targeted repair round (one mechanical transcription defect class,
                                4 occurrences, PRE/POST hashes below; SELF-CHECK — PE-MASTER must
                                independently audit this change per the QC contract)
```

## 1. Governance / boundary verification (duty 1)

| Check | Measured by QC | Result |
|---|---|---|
| Worktree HEAD | git rev-parse | e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c == dispatch requirement |
| Branch | git branch --show-current | codex/pe-world-launcher-r1-20261010 |
| Master triple (read-only) | local master == origin/master == `git ls-remote origin` | ALL == 3fbe93eec04759395223e6677b5040273d29222a (never written by this run) |
| Remote source branch | git ls-remote | codex/pe-city-asset-map-r1-20261010 == e9bb1f5… (the BASE_DECISION head) |
| RESULT_BRANCH on remote | git ls-remote | NOT PRESENT (persistence pending — expected; no push has happened) |
| BASE_DECISION disclosure | AUTHORIZATION_AND_PREFLIGHT.md §3 read | PRESENT + ACCURATE: e9bb1f5 vs f71eb30a, delta = EXACTLY ONE commit (CAMERA_UX_FIX, compat/catalog-app.js + catalog-preview.js, +169/−14); `e9bb1f5^` == f71eb30a re-verified by QC; the disclosure is prominent, cited in CAM_C1_C2_C3_DISPOSITION §0, and the executor's own verification steps are reproducible |
| Staged paths | git diff --cached | NONE (staged_lines=0) |
| Changed-path census vs §9 allowlist | full `git status --porcelain` (33 entries) | ALL within the allowlist: compat/ (1 M + 9 new), src/peworld/PEFoliageLabSeed.js (new), tools/pecompat/ (2 M + 3 new), tests/pecompat/ (5 M + 9 new), package.json (M — exactly 2 new scripts: serve:world + test:pecompat:world; justified), the skill (1 M + 1 new reference), docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (OUTPUT_REPO_PATH). **src/pesource: ZERO changes** (all 12 enumerated pesource modules byte-identical to HEAD). NOTHING in historical docs/audits, AUDIT_ENTRYPOINT, PROJECT_STATE, milestone/gates, the old viewer, or any other worktree |
| Witness modules byte-identity | `git hash-object` vs `HEAD:<path>` for 18 files | ALL MATCH: NifModelReader.js, PEFoliageCore.js, VegetationClimateDecoder.js, TgaDecoder.js (the 4 declared witnesses) + PESourceMount, TdfDecoder, TdfMaterialTailDecoder, TerrainTile, PETerrainCore, PEProvenance, Bnt2Archive, Bnt2TerrainArchive + the 218757 app files (index.html, app.js, asset-mode.js, scene-mode.js, api.js, server-sceneir.mjs) + catalog-app.js, catalog-preview.js |
| Other worktrees | read-only status | pe-sceneir-218757-r1 @ 59641ca CLEAN; pe-city-asset-map-r1 @ e9bb1f5 CLEAN (its earlier local modifications are the committed CAMERA_UX_FIX); eudoria-clean @ 3fbe93e with only the pre-existing foreign untracked groups (PE_935_* packages + experiments/) — untouched |
| Standing servers | Get-NetTCPConnection | 8140/PID 21288 + 8161/PID 9588 foreign-standing ALIVE and untouched before AND after every QC suite; 8162/PID 24964 = the run's own standing server (left RUNNING at QC end per the dispatch); 9222 automation daemon DOWN (re-measured by my own QC once) |

## 2. Input pins re-hash (duty 2) — ALL re-measured by QC itself

| Input | Size | SHA256 (QC's own Get-FileHash) | vs pin |
|---|---:|---|---|
| terrain.bnt | 125,064,817 | 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 | MATCH |
| VegetationClimates.bnt | 25,346 | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 | MATCH |
| Textures.bnt | 973,942,771 | 61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393 | MATCH |
| Models.bnt | 395,412,868 | C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 | MATCH |
| Models.ark | 128,742,137 | F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62 | MATCH |
| Textures.ark | 289,585,581 | D611D1257D2E5433B6DF218D671AA60D003C5C6587858757C7AF3219BB739B80 | MATCH |
| Desktop REPORT.md | 12,694 | 5F007CDB359E0C19A7C061D4C96EB66E1B3C5CA904CEDD4F36851D2384D9A307 | MATCH |
| GLB 192374 / 193207 / 193313 / 193684 | 94,484 / 66,476 / 94,644 / 108,192 | 8AF713E0… / 4F8C7C5B… / DA1A15BF… / 6B96C127… | 4/4 MATCH |

PINS_REHASH = **11/11 MATCH** (7 contract inputs + 4 GLB pins; sizes also all match).

## 3. CAM-C1/C2/C3 re-verification (duty 3)

- **CAM-C1 (re-execution + independent numbers)**: my own run of `tools/pecompat/cam_c1_glb_compare.mjs` → **4/4 EXACT_AGREEMENT** (bit-exact position multisets + unoriented triangle multisets after the explicit (x,z,-y); bounds identical; 0 mismatch keys on all four). All 4 GLB pins + all 4 NIF payload pins re-verified MATCH inside the tool run. 193313: 5 geoms / 2384 verts / 1192 tris — matches the disposition table. The tool performs its own fresh re-decode from the pinned Models.ark payloads (independent of historical artifacts). The DISPOSITION's explicit limits (unoriented ≠ winding/materials/lineage; `_textured.glb` filename not proof; UNTEXTURED_PROXY; images census 0 measured) are present verbatim. Raw: `00_CONTROL_INTERNAL_QC/raw/CAM/CAM_C1_GLB_COMPARE_QC_RERUN.json`.
- **CAM-C2 (baseline recomputed through the REAL production build)**: my own run of the full catalog battery (executor's exact arg set incl. both private caches) → the CAM_C2_C3_CLEAN_BASELINE gate PASS: measured complexity **1572** (PCG 1568 + CD 4; baseline control MATCH), unknown 6516, measuredByStatus {DECODED_FULL_CLOSURE:4, DECODED:1551, DECODED_NO_MESH:17}, FAILED 3270 rows honest-UNKNOWN with reason, no "decoded but" wording. `complexityFromBatchRow`/`isComplexityMeasured` verified by my FULL READ of tools/pecompat/catalog_data.mjs (the shared status model is the single definition; **no hardcoded 1572 anywhere in production code** — the number is a test control only).
- **CAM-C3 (mutants through the REAL loader — re-run)**: the focused QC A suite inside my catalog battery re-run → M1 ROW_ERA_MISMATCH / M2 ROW_CONTAINER_SHA_MISMATCH / M3 EDGE_ERA_MISMATCH all REFUSED with named reasons; the no-envelope default REFUSED whole (CACHE_IDENTITY_ENVELOPE_MISSING, measured falls to 4); clean PASSES the same gate (batch attached 4838, edges 1545, 0 drops); physical cache JSONLs byte-identical before/after (hash witness inside the suite). My full read of the CAM-C3 code (envelope verify + per-row reason + per-model all-or-nothing + full wire key) confirms the implementation matches the description.
- Catalog battery totals (my run): **41 PASS / 0 FAIL / 0 NOT_PERFORMED** — identical to the executor's claim (raw: `00_CONTROL_INTERNAL_QC/raw/CAM/CATALOG_TESTS_SUMMARY_QC_RERUN.json`).

## 4. Terrain gates re-verification (duty 4)

- **World battery re-run (my own execution, suite-owned free ports)**: **44 PASS / 0 FAIL / 0 NOT_PERFORMED** — identical to the executor's final battery (world_terrain 9, world_server 11, world_materials 9, world_vegetation 11, world_headless_load 4). Every suite server stopped with port-freed proof; the standing 8140/8161/8162 untouched. Raw: `00_CONTROL_INTERNAL_QC/WORLD_TESTS_SUMMARY_QC_RERUN.json` + raw/WORLD/ (my console transcript preserved there).
- **INDEPENDENT byte reads (my own fresh reader — zero production imports)**: my own BNT2-footer/directory walker + zlib inflate + DataView read of terrain.bnt: dir count 58,451; range-restricted census **51,920 regular + 6,530 special + 1 sentinel + 0 other; special-row gridY min 0xff5a, max 0xffff** (my own enumeration — matches the run's measured correction exactly). Three physical tiles decoded at payload offset 64..2111 and cross-checked **bit-exact** against the STANDING server's `/api/world/tile/<gx>/<gy>` wire: 00350072.tdf (53,114 — spawn; min 40877/max 63325/mean 56925), **006e00b6.tdf (110,182 — NOT in the executor's sample set; min 3199/max 6901/mean 4398)**, 00db00eb.tdf (219,235 — corner). The **offset-52 negative still discriminates** on all three (my own sub-header reads differ from the true heights; e.g. 006e00b6 true first 6 = 6144,6142,6141,6137,6133,6127 vs garbage at 52). Sentinel handling, NODATA≠0, reverse-order invariance, calibration-once/reversibility and the terrain.bnt hash witness (pin before AND after the battery) all re-measured green inside my battery re-run.

## 5. Materials chain re-verification (duty 5)

- **mask@record+56 on sampled records — my own bytes**: my own tail walker (fresh code, own RLE expansion, exact stride walk) on 00350072.tdf (9 named records) and 0032006f.tdf (12 named records): every served base64 mask is **bit-exact** my walk; all RAW records measured wrong-52 region length 260 (= 4+size−52 → NOT 256 → refuses as RAW, RLE fails on raw content) — **12/12 RAW records discriminating**; RLE records with extra4=[0,0,0,0] are value-degenerate at 52 (consistent with the run's documented measured boundary); tails consumed EXACTLY.
- **id → `<id>.dat` resolution cross-check (my own index read)**: my own bounded lazy parse of Textures.bnt (footer + directory only): **8,381 entries** (count field == parsed). 13382.dat (Stone04, 196,652 B) and 457490.dat (262,188 B, 32bpp A32) read physically by me and compared **bit-exact** against the standing server's `/api/world/texture/<id>` wire.
- **Wrong-era refusal through the REAL route**: `?era=CD_2003`, `?era=CD_JAN_2003`, `?era=JUL_2003` → **403 ERA_REFUSED_WRONG_ERA** on the texture route AND the materials route (measured by my own HTTP against the standing 8162; the era gate runs BEFORE any data access — verified in my full read of server-world.mjs).
- **Raw weights preservation**: re-measured inside my battery re-run (WORLD_MAT_WIRE_BITEXACT: 42 records / 10,752 weight bytes bit-exact; per-cell layer sums 255..1431 — above-255 sums preserved UNNORMALIZED; WORLD_MAT_SPLAT_RAW_WEIGHTS: GPU-bound weights == served masks, slot order = record order).

## 6. Vegetation re-verification (duty 6)

- **25.vcl controlled UNSUPPORTED — my own raw read**: my own VegetationClimates.bnt dir walk (32 entries) + raw payload read of 25.vcl + my own whitespace tokenization: **252 tokens; exactly 6 non-numeric tokens; the first is token index 109 = record 9, col 1, "0,2"** — the claimed comma tokens confirmed from the physical bytes. The production refusal re-measured through the REAL route: `/api/world/climate/25` → status UNSUPPORTED, `records: null` (asserted by absence), the strict decoder error verbatim. Profile 0: API records == my own 0.vcl decode (12×12-value records), **witness 457485 present** in the record set.
- **Default-profile justification (via the server API)**: /api/world/status .vegetation verified in full: defaultProfile 0 DECODED, 12 records, 10 distinct models, MEASURED-choice justification text (forbids the "historical biome" claim), support census **10 / 8 textured / 2 honest-untextured / 0 parse-unsupported** with per-model details (per-model entry bytes match MY OWN physical reads: 457485=2547 B, 436293=6640 B, …; the two untextured = the DDS payload 166881 refused loudly outside the strict {24,32}bpp subset), p3=0 shown SEPARATELY, cap 5000, three-way separation labels verbatim.
- **Determinism (my own execution of the production generator + my own canonical serialization)**: `generateTileInstances` (profile 0 records via the API, tile 53,114, density 50) run twice with labSeed 0 → **identical SHA-256** over my own key-sorted serialization of (key|modelId|u16|world|f32 scale bits|f32 sampler bits|rngState0); labSeed 1 → **different hash AND different u16 positions** (a real placement change). QC honesty note: my FIRST determinism script version produced a false "diffSeed identical" reading — my own serialization bug (nonexistent field names), caught by cross-check vs the suite's recorded hashes, fixed, re-run green. The false reading never left this review.
- **The cap case (recomputed by me)**: profile 1 records (my own 1.vcl decode, 14 records) at density 100 over the 8×8 window origin (50,111): **requested 6144 / rendered 5000 / limited 1144; per-tile counts ALL 96** — exactly the suite's measured numbers (min(requested,5000) in deterministic order). WORLD_VEG_CAP_5000 re-measured green in my battery re-run; WORLD_VEG_RESOURCE_DISCIPLINE re-measured green (window A→B→A no-refetch + texture object identity, profile-change disposals, toggle cycle, teardown empties caches).
- **The REAL model chain (bit-exact)**: `/api/world/model/457485` (standing server) == my own lazy physical read of Models.bnt entry `457485.nif` **bit-exact** (2547 B, SHA256 72479a7f4eebe934… — matching the suite's payloadSha); my own Models.bnt dir walk: **5,596 entries** (== the measured corpus census); missing id 999999 → 404 MODEL_ENTRY_NOT_FOUND (never a substitute model); texture 457490 wire == my own Textures.bnt read (bit-exact, above).

## 7. Browser QC (duty 7) — against the STANDING server 8162 (the final code)

- **LOAD /launcher**: real headless Edge (`--headless=new`, dedicated temp profile) against http://127.0.0.1:8162/launcher → the FIXED imported 5-conjunct gate (evaluateLoadGate — the same production predicate the run's T9 gates use): **PASSED** (EXIT_CODE_ZERO, DOM_NONEMPTY, CANVAS_PRESENT, DIAGNOSTICS_PRESENT, STATUS_READY). Page markers: entry button label EXACT **„Uruchom podgląd świata”**, era PCG_9_3_5, denominator **51 920**, coverage line, **VEGETATION_MODE = RECONSTRUCTION_PREVIEW**, three-way separation labels, UNSUPPORTED-25 visible, no „oryginalne XYZ” claim — **8/8**.
- **LOAD /world** (#tile=53,114&profile=0&seed=0&density=50&veg=1): gate **PASSED**; markers: 64-tile window census line, adapter-units position, no original-XYZ readout claim, raw u16 readout, **the census line żądane/wyrenderowane/ograniczone**, VEGETATION_MODE, profile/seed labels, p3 separate, three-way separation — **9/9**.
- **PIXEL (PRIVATE)**: my own CDP capture (remote-debugging on a QC-owned free port, Runtime.evaluate readiness poll on the page's own honest markers, Page.captureScreenshot after a real-time settle — the run's corrected method): /launcher PNG 118,779 B, **1,425 unique colors, lumaStdDev 40.61, most-common 56.3%** → NON_TRIVIAL. Stored ONLY at `D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_LAUNCHER_R1_20261010\BROWSER_QC_R1\qc_pixel_launcher.png` (SHA256 cacb72a9a20eeff73adb988837744a3c77e3ad9b3808e4b1587c58f1bf3e74c0). No proprietary rendered payload in the repo.
- **INTERACTION**: automation daemon (port 9222) re-measured DOWN by my own QC → **NOT_PERFORMED** (honest; matches the executor's status and the preregistration).
- QC honesty note: my first browser-marker run showed 2 marker FAILs that were **my own tooling defect** — my PowerShell `Set-Content` edit corrupted the UTF-8 literals of my own QC script (the EXACT ENCODING INCIDENT failure class the executor recorded in I-17; the lesson "file edits through the edit tool ONLY" is thereby independently validated). Fixed via \u escapes; re-run fully green. No product defect existed.

## 8. Proprietary census (duty 8)

My own scanner over **all 32 changed/new text files + the ENTIRE report package** (incl. all raw/ HTML dumps and JSONs): PNG magic, TGA footer-at-start, DDS magic, bulk "NetImmerse File Format" headers, base64 runs ≥4000 chars, bulk f32 arrays >300 — **ZERO findings**. The mask base64 inside the materials TEST evidence is bounded per-record 256-B material masks (legitimate decoded-data evidence, not payload redistribution) — the scanner's ≥4000-char base64 check found none even in the raw dumps. **PNGs/screenshots are PRIVATE-ONLY**: all 5 PNGs referenced by TEST_RESULTS (path+SHA) verified to exist in the private root with EXACTLY matching size + SHA256 (pixel_launcher 144,264 B / 2295CE7D…; pixel_world-on 327,229 B / E6A20B9A…; pixel_world-off 422,215 B / 226EA4DA…; pixel_world-veg-on 327,229 B / E6A20B9A…; pixel_world-veg-off 168,977 B / 519DBC27…). 5/5 spot-check MATCH.

## 9. Skill check (duty 9)

The pe-gamebryo-rosetta extensions meet the contract criteria: concise; every source claim carries path+size+SHA256; scope labels present (SDK knowledge is NEVER PE knowledge; samples = other apps' examples); CURRENT_RUNTIME_CALIBRATION labels carried (never historical meters/axes); NO "engine known 100%" anywhere; era discipline section; explicit UNKNOWNs ([P-CELLSTREAM], [P-CLIMATE], [P-RNG-P3], materialId==textureId, special rows, VCL cols 6..11). TWO stale-phase observations recorded as P3-2/P3-3 below (one transcription half of them REPAIRED — see P3-1).

## 10. Package hygiene (duty 10)

- All 9 phase artifacts required "non-vacuous" by the dispatch EXIST and are non-vacuous (all read to EOF by QC): INPUT_IDENTITIES, PREREGISTRATION, CAM_C1_C2_C3_DISPOSITION, GAMEBRYO_MECHANISM_MAP, IMPLEMENTATION_MAP, WORLD_DATA_PROVENANCE, CALIBRATION_AND_UNKNOWNS, TEST_RESULTS, INTERVENTION_LEDGER (+ AUTHORIZATION_AND_PREFLIGHT).
- **JSON validity: 41/41 VALID** (every .json in the package incl. raw/).
- INTERVENTION_LEDGER completeness: server restarts old→new PIDs recorded (I-10: PID 13556; I-18: 13556→24412; I-24: 24412→24964 — the current standing server), Edge runs recorded, the honest failed-first corrections recorded in detail (I-4/I-5 tool + harness defects; I-13 six FAILs incl. the all-zero-tile offset-52 refinement + the accidental historical-package raw writes cleaned; I-17 the ECONNRESET header bug + THE ENCODING INCIDENT + the IdentityCache envelope bug; I-23 the double-conversion 1/50-size tree defect + the capture-method correction), the orphan debug-server cleanup (PID 14820) recorded with the process-liveness lesson. The ledger is complete and honest.
- **U-19 is properly recorded as an OPEN finding** in four places (TEST_RESULTS.json etapE_vegetation.openFindings, CALIBRATION_AND_UNKNOWNS.md U-19, WORLD_DATA_PROVENANCE ETAP_E openFindings, INTERVENTION_LEDGER I-25) with the interactive-appearance-UNVERIFIED caveat tied to INTERACTION NOT_PERFORMED.
- MISSING_FINAL_FILES (the FINAL phase's — for persistence): REPORT.md, BROWSER_SMOKE.md, RUN_AND_STOP.md, HANDOFF.md, EVIDENCE_INDEX.md, MANIFEST_SHA256.csv, PE_MASTER_REVIEW.md (persistence) + the terminal handoff block. (INTERNAL_REVIEW.md is delivered by THIS QC.)

## 11. Findings

### **P2-1 — U-19 CONFIRMED: the Etap D splat shader samples the sampler2DArray with the NORMALIZED idx byte instead of the LAYER NUMBER (OPEN — must survive persistence, never "all green")**
- **Location**: compat/world-app.js, SPLAT_FRAG (lines ~339-354): `texture(uMats, vec3(uv, i0.x))` (and the i1/i2/i3 variants) — `i0.x` is the texel value of the idx DataTexture (UnsignedByteType → normalized [0,1] in the shader), used directly as the third (array-layer) coordinate. The slot indices are 0..47; the layer coordinate must be the LAYER NUMBER (e.g. `float(i0.x*255.0+0.5)` or an integer-format texture), not the normalized byte.
- **Contradicted claim**: none as-worded — the executor already reports this as OPEN finding U-19 ("SPLAT TERRAIN APPEARANCE IN HEADLESS CAPTURES… root-cause candidates: the sampler2DArray layer coordinate uses the NORMALIZED idx byte…"). QC's contribution: the root cause is CONFIRMED at code level (not merely a candidate).
- **Effect**: every cell samples layer ≈0 of the DataArrayTexture → the per-color result of the textured terrain is wrong (the observed near-black headless render); the Etap D toggle gate remains valid (it measures CHANGE — 48.89% of canvas pixels differ — and QC re-read the toggle wiring: the material swap is real).
- **Skutek/blast radius**: the /world textured-terrain appearance only. The chain evidence (resolved/decoded/applied/browser-observed counters), the raw weights, the masks, the toggle mechanics are unaffected.
- **Required correction (follow-up phase; NOT silently closed)**: pass the layer number in the shader (or use an integer idx texture) + pixel-verify the #textures=1 render PER-COLOR against expected blended weights for known cells (e.g. the spawn window's Stone04-dominant cells) in a real GPU session.
- **Revalidation gate**: per-color pixel comparison of #textures=1 (not merely toggle-vs-palette change) + the interactive appearance re-check once INTERACTION becomes performable.

### **P3-1 — STALE special-row transcription `0xff1a..0xffff` in 4 delivered texts — REPAIRED by QC (PRE/POST documented; SELF-CHECK)**
- **Location**: compat/launcher.js line 424 (the evidence-panel text), compat/launcher.html lines 29 (header comment) and 56 (visible UI label), .opencode/skills/pe-gamebryo-rosetta/references/terrain-foliage-integration.md line 93.
- **Contradicted fact**: the run's OWN measured correction — special-row gridY range is **0xff5a..0xffff** (WORLD_DATA_PROVENANCE.specialRowRangeCorrection: "the phase-2 map's '0xff1a' was a transcription artifact"; the server's GRID_OUT_OF_RANGE message already carries the corrected range; my OWN independent census measured specYmin=0xff5a).
- **Failure mechanism**: the phase-2 transcription artifact survived into phase-3-born UI texts (launcher.js was created AFTER the correction was measured).
- **Repair (the one targeted QC repair round)**: `0xff1a` → `0xff5a` in all 4 occurrences.
  - PRE: launcher.js 8B5437608216DDDA08057EC69F521291EFD13B14D584742BF60602F8BAE654FA (== ledger Appendix D), launcher.html 0E61B26AB286819DBA02EDB9BF8553BE25E53DEF8430CAB7B025179555F292F8 (== Appendix D), terrain-foliage-integration.md 1A4112D258B371A1CB7E72D1F1F1EC53B2530D4A973984D705B9B97C69C77D97.
  - POST: launcher.js 3C58E5A6104A4F692170547AE4585CAE6D760BE873792D5B02643CA5391F6C5D, launcher.html 3B8FA15279FF846632E99DB97FD5DEFB163E49ECDE5D68C3AE7DEB2B9EDF335D, terrain-foliage-integration.md 0C5C78E04B3310DB5B92CB1A07DEB907C3084B95472E649E0FA1ABBEEA922E15.
  - **Revalidation (executed)**: a fresh headless LOAD of /launcher through the standing server → gate PASSED, entry button + markers all present, `0xff1a` GONE from the live DOM, `0xff5a` present. Residual `0xff1a` in changed paths: NONE.
  - **NOTE**: the ledger Appendix D hashes for launcher.js/launcher.html are thereby superseded (POST hashes above); persistence must re-measure all identities anyway (MANIFEST is generated last). This repair is a QC change under audit — **PE-MASTER must independently audit it** (my verification of these files is SELF-CHECK).

### **P3-2 — skill phase-status staleness: "serve:world … is PLANNED, not yet built" (REPORT-only)**
- **Location**: .opencode/skills/pe-gamebryo-rosetta/SKILL.md (Terrain/materials/foliage pointer section, the `serve:world` sentence); terrain-foliage-integration.md §5 ("It does NOT exist yet as of Etap B" — this one is explicitly phase-scoped and honest).
- **Problem**: after Etaps C–E the launcher/world server IS delivered; a future session loading the skill is told it does not exist. The terrain-foliage-integration.md §3 "Launcher-phase controls are PLANNED… NOT executed in Etap B" is likewise phase-scoped but the executed controls now exist in the run package.
- **Required correction (executor, at persistence — editorial skill content, NOT a mechanical fix)**: a short status update marking the world-launcher lineage DELIVERED (Etap C/D/E) with the run pointer; keep the Etap-B wording as the historical phase record if preferred, but the top-level SKILL.md pointer should not instruct future sessions that serve:world does not exist.
- **Revalidation gate**: the skill text no longer contradicts the repo state (serve:world resolvable in package.json + the standing server).

### **P3-3 — draft remnant in CAM_C1_C2_C3_DISPOSITION.md §2 (REPORT-only, cosmetic)**
- **Location**: CAM_C1_C2_C3_DISPOSITION.md line ~128: "FAILED rows: 3270/3274? no — 3270/3270 all complexity.unknown=true…".
- **Problem**: an in-line self-correction remnant ("3270/3274? no —") in a delivered report — transparent and the final value is correct (3270/3270), but it is editing residue. Executor-evidence file → findings only (no QC repair).
- **Required correction**: the FINAL phase's REPORT.md should carry the clean number (3270/3270 FAILED rows, all UNKNOWN-complexity with reason).

### QC-process incidents (recorded honestly; no product impact)
1. My first determinism check produced a FALSE "changed-seed identical" reading — my own canonical serialization used nonexistent instance field names (all-undefined lines). Caught by cross-check against the suite's recorded hashes; fixed to serialize the REAL shape (key|modelId|u16|world|f32 bits|rngState0); re-run: repeat-identical + diff-seed-different + positions-differ all TRUE.
2. My own PowerShell `Set-Content` edit corrupted the UTF-8 literals of my browser-QC script (the CP1252-mis-read failure class the executor recorded as the ENCODING INCIDENT — the lesson is thereby independently validated); fixed via the edit tool with \u escapes; re-run fully green.

## 12. QC re-execution table (my own executions; originals read-only)

| # | Re-execution | Result |
|---|---|---|
| 1 | Governing contract SHA256 + size re-hash | MATCH (30ACECDF…C5B63, 27507 B) |
| 2 | 11 input pins re-hash (7 contract + 4 GLB) | 11/11 MATCH |
| 3 | Full world battery re-run (`run_world_tests.mjs`, my raw-dir/json-out) | **44 PASS / 0 FAIL / 0 NOT_PERFORMED** (matches the executor's claim exactly) |
| 4 | Full catalog battery re-run (executor's exact arg set; incl. Focused QC A) | **41 PASS / 0 FAIL / 0 NOT_PERFORMED** (CAM_C2 baseline 1572 MATCH; CAM_C3 mutants REFUSED; caches unchanged) |
| 5 | CAM-C1 tool re-run (`cam_c1_glb_compare.mjs`) | 4/4 EXACT_AGREEMENT; all pins MATCH |
| 6 | My own BNT2 census (terrain.bnt) | 58,451 = 51,920 + 6,530 + 1 + 0; specialY ff5a..ffff |
| 7 | My own terrain byte reads vs the STANDING server wire (3 tiles incl. 1 fresh tile) | bit-exact ×3; offset-52 discriminates ×3 |
| 8 | My own material-tail walk (2 tiles) vs the served masks | bit-exact; RAW wrong-52 region len 260 ×12/12 |
| 9 | My own Textures.bnt lazy index + physical reads vs the wire | 8,381 entries; 13382.dat + 457490.dat bit-exact |
| 10 | Wrong-era refusals through the REAL route (standing server) | 403 ×4 (CD_2003/CD_JAN_2003/JUL_2003 + materials route) |
| 11 | My own 25.vcl raw read + tokenization | comma tokens at record 9 col 1 confirmed ("0,2" @ token 109); API UNSUPPORTED records=null |
| 12 | Profile 0 vs my own 0.vcl decode; witness 457485 | records equal; witness present; support census 10/8/2/0 via the API |
| 13 | Production `generateTileInstances` determinism (my serialization) | sameSeed identical; diffSeed different hash AND positions |
| 14 | The 5000-cap recomputation (profile 1 @100%, window 50,111) | requested 6144 / rendered 5000 / limited 1144; perTile ALL_96 |
| 15 | Model chain bit-exactness (457485 wire vs my own Models.bnt read; my index census) | bit-exact (2547 B, sha 72479a7f…); my census 5,596 entries; 999999 → 404 |
| 16 | Headless Edge LOAD /launcher + /world vs the STANDING 8162 through the FIXED gate | gate PASS ×2; 8/8 + 9/9 markers |
| 17 | My own CDP pixel capture (/launcher, PRIVATE) | 118,779 B; 1,425 colors; lumaStdDev 40.61 → NON_TRIVIAL |
| 18 | INTERACTION daemon check (9222) | DOWN → NOT_PERFORMED (honest) |
| 19 | Proprietary census (32 changed files + whole package) | ZERO findings |
| 20 | Private artifacts spot-check (5 PNGs, path+SHA) | 5/5 EXIST, size+SHA match |
| 21 | JSON validity sweep | 41/41 VALID |
| 22 | Witness/app module byte-identity (18 files vs HEAD blobs) | ALL MATCH |
| 23 | Master triple + other worktrees + standing servers | 3fbe93e triple MATCH; worktrees clean; 8140/8161/8162 alive as required |
| 24 | The repair (0xff1a→0xff5a ×4) + live revalidation | applied; launcher gate + markers re-PASS; stale text gone from the live DOM |

## 13. NOT_CHECKED (honest)

- **Unit battery (24 gates) + app battery (22 gates): NOT re-executed by this QC.** Coverage relied upon: (a) the byte-identity of the whole 218757 app + src/pesource/peworld/pecompat trees to HEAD (my git hash-object sweep — the strongest form of the "regression-free" claim), (b) the executor's raw summaries (raw/UNIT_TESTS_SUMMARY_ETAPE.json, raw/APP_ETAPE/ — read, JSON-valid), (c) my catalog battery re-run which re-executed 33 prior catalog gates + the fixed-gate browser LOADs green.
- **The ETAP_D/ETAP_E PIXEL TOGGLE GATES not re-executed by this QC** (my pixel work = one launcher CDP capture + the code reads confirming the toggle wiring). Verified by: the executor's raw/WORLD/PIXEL_RENDER_ETAPE.json + TEST_RESULTS numbers, my full read of world-splat.js/world-app.js (the toggle really swaps the material; the shader defect documented as P2-1), and my LOAD census showing both pages render non-trivially with textures+veg ON.
- **Full file reads NOT performed (verified by other means)**: PEFoliageCore.js, NifModelReader.js, PESourceMount.js, TgaDecoder.js, PETerrainCore.js, TerrainTile.js, PEProvenance.js, ArkArchive.js (all byte-identical to HEAD — pre-existing, prior-run-qualified, unchanged by this run; verified by hash + the battery's WORLD_VEG_CORE_UNTOUCHED + witness gates); the four world test suite sources + catalog_cam_fixes.test.mjs (their assertions/measured values verified through my own re-run transcripts + my independent re-implementations of the key predicates — the file texts were not read end-to-end); cam_c1_glb_compare.mjs beyond the header (the tool was fully RE-EXECUTED); world_pixel_render.mjs beyond the header (its method re-implemented independently by my QC script); png_nontrivial.mjs (imported + executed); world_collect_test_results.mjs; _world_server_helpers.mjs; headless_load.test.mjs (only the evaluateLoadGate import); server-catalog.mjs (diff stat only: +16/−6); the 4 modified catalog test files (diff stat only: +3/−1 each — the envelope declaration); launcher.css/world.css/compat.css (styling); launcher.html full read (targeted sections + byte/marker checks); world.html full read (targeted marker checks).
- The private cache JSONLs' internal row schemas were not re-parsed record-by-record by this QC (they are READ_ONLY attach targets; the CAM_C3 gates exercised them through the production loader in my battery re-run; their file identities were pinned by the suite's hash witness).

## 14. Verdict

```text
QC_VERDICT              = PASS_WITH_FINDINGS
                          (0 P0 / 0 P1 / 1 P2 OPEN — U-19, executor-recorded, QC-confirmed root cause;
                          3 P3 — one REPAIRED+revalidated, two REPORT-only with corrections for persistence)
PRODUCT_VERDICT_RECOMMENDATION = PASS_IN_IMPLEMENTED_SCOPE
                          per the contract §8 list, measured:
                            LAUNCHER_HEIGHTMAP          = original-data-backed + selectable (VERIFIED)
                            TERRAIN_REGION              = rendered from original u16 samples (VERIFIED —
                                                         44-gate battery re-run + my independent byte reads)
                            TERRAIN_TEXTURE_CHAIN      = proven + rendered + toggle-measured; per-color
                                                         appearance carries the OPEN U-19 defect and stays
                                                         UNVERIFIED interactively (P2-1 — must survive
                                                         persistence as OPEN, never "all green")
                            VEGETATION_PREVIEW          = deterministic + honest labels (VERIFIED — my own
                                                         determinism/cap/order executions + the census line)
                            ORIGINAL_VEGETATION_MODEL   = witness 457485 textured, bit-exact chain (VERIFIED)
                            CAM_C1_C2_C3                = corrected + verified in examined scope (VERIFIED)
                            BROWSER_INTERACTION         = NOT_PERFORMED (honest — daemon down; the §8
                                                         acceptance line itself allows this status)
                          The recommendation is conditional on: U-19 kept OPEN at persistence; INTERACTION
                          kept NOT_PERFORMED (never PASS-by-default); the final REPORT/BROWSER_SMOKE/
                          RUN_AND_STOP/HANDOFF + manifest bijection at persistence; the QC repair (P3-1)
                          independently audited by PE-MASTER; P3-2/P3-3 handled by the executor at persistence.
```

QC worker: pe-master-auditor (fresh session, FRESH_INTERNAL_REVIEW — internal to PE-MASTER; NOT a Desktop post-audit). All QC re-executions were read-only against the originals; QC outputs live in 00_CONTROL_INTERNAL_QC/ + the private BROWSER_QC_R1/ PNG. The standing world server http://127.0.0.1:8162/ (PID 24964) was verified ALIVE and left RUNNING at QC end; the foreign standing servers 8140/8161 untouched.
