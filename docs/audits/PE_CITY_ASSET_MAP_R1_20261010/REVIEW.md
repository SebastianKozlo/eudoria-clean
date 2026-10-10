# REVIEW.md — FRESH INTERNAL QC — PE_CITY_ASSET_MAP_R1_20261010 (phases 1–4)

RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
QC_RUN_ID = PE_CITY_ASSET_MAP_R1_20261010_INTERNAL_QC_R1_20261010
QC_ORIGIN = **FRESH_INTERNAL_REVIEW** (pe-master-auditor, fresh session, no prior context; internal to
PE-MASTER — this is **NOT** an independent Desktop post-audit and does not replace one; it is the
contract §7 "fresh internal QC" layer).

Scope: the completed executor work for phases 1–4 in worktree
`D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1` (branch
`codex/pe-city-asset-map-r1-20261010`, HEAD `59641caa1b14ade84e1842ca36b395842deb241e`,
NO commits — uncommitted tree). Audit executed from disk; all my re-executions were read-only
against the originals; my scripts and raw outputs live under
`00_CONTROL_INTERNAL_QC/` inside this report package (QC scripts qc1–qc16 + JSON results +
raw captures). One targeted repair round was authorized — NOT used (no QC-scoped mechanical
defect found in my own outputs; executor-evidence defects are reported as findings only, per
the QC assignment).

---

## 1. QC verdict

**QC_VERDICT = PASS_WITH_FINDINGS** (0 P0, 0 P1, 1 P2, 3 P3; dispositions below).

**BROWSER verdict state:** LOAD = EXECUTED AND VERIFIED (my fresh real-headless-Edge `/catalog`
load through the FIXED 5-conjunct production gate: all five conjuncts PASS, data-load-status
READY, 98,906 B DOM; plus the battery's two real-browser loads in my re-run). PIXEL_RENDER =
EXECUTED AND VERIFIED (executor's calibrated 5-shot PIXEL gate PASS + my fresh screenshot
capture: PNG 121,320 B, 1,096 unique colors, luma stddev 41.8 — non-triviality spot-check PASS;
PNG in PRIVATE_OUTPUT only). **INTERACTIVE = NOT_PERFORMED** (automation daemon down —
ECONNREFUSED on 127.0.0.1:9222 and [::1]:9222; honest, never faked). The contract §5 promotion
rule is therefore **NOT satisfied: no BROWSER_VERIFIED claim** — and the executor's
TEST_RESULTS.json summaryVerdicts explicitly does NOT claim it. Correct.

No scientific claim of the run was invalidated by this QC. Every load-bearing numeric claim I
re-tested was reproduced exactly (see §3). The findings are documentation / machine-readability
defects to be repaired at persistence.

## 2. Findings (severity ladder P0/P1/P2/P3)

### P2-1 — TEXTURE_LINK_DISPOSITIONS.csv schema violation: unquoted comma in `container_entry`

- **Location:** every PCG_9_3_5 aggregated row (1,545 of 1,587 data rows), field
  `container_entry` — the literal value `Textures.bnt (8,381 entries)` contains a thousands
  separator comma that is NOT quoted.
- **Counter-check:** QC2 full RFC-style parse → field counts per row: `{ "7": 42, "8": 1545 }`
  against the 7-field header (`model_id,era,edge,slot,texture_name,container_entry,dispositions`).
  The 1,545 aggregated rows mis-split (`container_entry` torn into `Textures.bnt (8` +
  `381 entries)`); the CD_2003 rows (42) are clean.
- **Skutek (effect):** a strict CSV consumer (persistence manifest join, CLAIM_MATRIX
  generation, any spreadsheet re-export) mis-parses 97% of the artifact's rows at schema level.
  The information itself is unambiguous and all aggregates verified (QC3: NAME_NOT_FOUND sum
  3,357 ✓, material refs 794 ✓, 3,357+794 = 4,151 = the JSONL row count ✓, distinct models
  1,545 ✓) — a machine-readability defect (L10: "no malformed quoting"), not a data defect.
- **Required correction (persistence phase):** re-emit the aggregated rows with the
  `container_entry` field properly quoted, or write the count without the thousands separator
  (`Textures.bnt (8381 entries)`). Do not alter any disposition value.
- **Revalidation gate:** strict RFC4180 parse of the fixed file → every row exactly 7 fields;
  data-row count still 1,587; QC2/QC3 sums unchanged (3,357 / 794 / 4,151 / 1,545 / 19+19+4).

### P3-1 — INTERVENTION_LEDGER.md F12 data-row count off by one

- **Location:** INTERVENTION_LEDGER.md, phase-3 filesystem table F12: "…TEXTURE_LINK_DISPOSITIONS.csv
  (NEW, ASCII-only, **1,588 data rows**)".
- **Counter-check:** QC2 — actual data rows = **1,587** (42 CD_2003 + 1,545 PCG_9_3_5; header
  excluded; file ends with a newline). The batch artifacts independently support 1,545 aggregated
  rows (PCG935_NAME_BATCH_SUMMARY: 1,545 models with ≥1 edge), so the correct total is 1,587 and the
  ledger number is a miscount (most likely counted the header or a post-write state).
  Note: the file is UTF-8 and is NOT ASCII-only — 19 material rows updated in phase 4 carry a
  UTF-8 em-dash (E2 80 94; 19 sites, matching the "19 material rows updated" claim). Valid UTF-8,
  display-safe; the earlier "�?" rendering seen in a PowerShell-5.1 console was a console decoding
  artifact, not a file defect.
- **Required correction:** at persistence, append a one-line ledger correction (the ledger is
  append-only: add the correction, do not rewrite history) — "TEXTURE_LINK_DISPOSITIONS.csv data
  rows: 1,587 (42 + 1,545), not 1,588; file is UTF-8 (19 em-dashes in the phase-4 material rows)".
- **Revalidation gate:** recounted data rows = 1,587; the correction line present.

### P3-2 — skill chapter example name does not exist in either container

- **Location:** `.opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md` §1:
  "2,177 entry names exist in BOTH era model containers (e.g. 656865.nif, 65678.nif)".
- **Counter-check:** QC14/QC15 — `656865.nif` exists in NEITHER the CD_2003 Models.ark catalog
  NOR the PCG_9_3_5 Models.bnt catalog (0 hits; no near-miss 6568* names exist). The overlap
  count 2,177 is CORRECT (I recomputed the intersection from the two phase-2 catalogs:
  exactly 2,177). Verified real examples: `266865.nif`, `65678.nif` (both present in BOTH eras).
- **Required correction:** replace the example "656865.nif" with a verified overlap example
  (e.g. `266865.nif`, or keep only `65678.nif`).
- **Revalidation gate:** the named example(s) must each exist in BOTH phase-2 model catalogs.

### P3-3 — private run_records.json carries a UTF-8 BOM (strict JSON.parse fails)

- **Location:** `PRIVATE_OUTPUT/PHASE3_NativeControl/run_records.json` (3,500 B) — starts with
  EF BB BF.
- **Counter-check:** QC5 private-JSON BOM census — 21 JSON artifacts scanned; exactly ONE has a
  BOM and exactly ONE fails strict `JSON.parse` (this file). PowerShell-written artifact (the
  native run script phase3_native_run.ps1 used PowerShell text output), consistent with the
  host's .ps1-encoding convention but a machine-readability defect for a .json artifact.
  Content itself parses after BOM strip; all four native runs confirmed: outcome EXITED,
  exit=1, stderr first line "Error loading stream." (verbatim, re-read by me; stdout 0 B each).
- **Required correction:** at persistence, either re-emit without BOM (content byte-identical
  after the BOM strip) or record the BOM limitation in EVIDENCE_INDEX/LIMITATIONS; do not alter
  the record content.
- **Revalidation gate:** strict `JSON.parse(readFileSync(...))` succeeds on the fixed artifact.

### Observations (recorded, no defect)

- **OBS-1:** Models.bnt has 150,133 B of unaccounted slack between the last payload end
  (395,262,727) and the directory start (395,412,860). The phase-2 claims "0 overlaps, 0 gaps,
  monotonic offsets, no payload crosses the directory or EOF" all hold (verified by my own
  sorted-offset boundary census: 0 overlaps, 0 gaps BETWEEN payloads). The tail slack is not
  claimed by the catalog and its semantics stay UNKNOWN — recommend recording it as an UNKNOWN
  boundary note at persistence (do not interpret).
- **OBS-2:** the six raw console captures (`raw/T9/*CONSOLE.txt`) are UTF-16LE+BOM (PowerShell
  redirect class). Human-readable; the authoritative machine records are the UTF-8 JSONs. No
  repair required.
- **OBS-3 (reproducibility):** denial probes issued through WHATWG `fetch` get client-side
  dot-segment normalization, so my first traversal probes landed as 404 ROUTE_NOT_FOUND;
  RAW-socket probes (no normalization) confirmed the server's own refusals: three-subtree
  traversal → 403 PATH_TRAVERSAL_BLOCKED, compat traversal → 404 STATIC_FILE_NOT_ALLOWEDLISTED
  (exact-allowlist map lookup — the URL never becomes a filesystem path). All 18 denial probes
  (12 fetch + 6 raw) were refused; none leaked.
- **OBS-4:** rows-API default size sort returns the CROSS-era largest first (225492.nif,
  10,029,720 B, PCG_9_3_5); the UI note's "CD_2003 largest payload = 212124.nif 936,544" is
  era-scoped and also correct. No contradiction; recorded to prevent a future misreading.
- **OBS-5:** `assets/cd2003` of pe_asset_viewer_v4 contains EXACTLY 16 GLBs (claim precise);
  zero GLB for 192374/193207/193313/193684 anywhere in the v4 tree (my bounded re-search). The
  executor's wider depth-6 search was not re-executed by this QC.

## 3. Re-execution / re-verification table (all mine, from disk)

| # | Duty | Check | Result |
|---|---|---|---|
| 1 | Governance | worktree HEAD / branch / no commits | HEAD = 59641caa… ✓, branch codex/pe-city-asset-map-r1-20261010 ✓, no commits ✓ |
| 2 | Governance | master local / origin / FRESH remote (ls-remote) | all = 3fbe93eec0… ✓ |
| 3 | Governance | old SceneIR worktree | at 59641ca, clean ✓ |
| 4 | Governance | foreign server port 8140 / PID 21288 at QC START and END | alive, node, LISTENING, untouched ✓✓ (my servers used 8161/8188/8197/8199 only) |
| 5 | Governance | changed-path census vs §8 allowlist | 4 modified (SKILL.md, package.json, headless_load.test.mjs, run_app_tests.mjs) + new files ONLY in compat/, tools/pecompat/, tests/pecompat/, .opencode/skills/pe-gamebryo-rosetta/, REPORT_PACKAGE ✓ — no out-of-allowlist path |
| 6 | Governance | package.json justified-scripts-only | exactly two new scripts (serve:catalog, test:pecompat:catalog); three 0.185.0 unchanged; NO new dependencies ✓ |
| 7 | Governance | 218757 app + src/ byte-identity | empty `git diff HEAD` for compat/app.js, index.html, asset-mode.js, scene-mode.js, api.js, server-sceneir.mjs, src/… ✓; NifModelReader.js git-blob 7d926fb3… == 59641ca blob ✓ |
| 8 | Governance | AUDIT_ENTRYPOINT / governance / foreign untracked | untouched ✓ (canonical status: only foreign PE_935_* / experiments) |
| 9 | Phase-1 | Desktop post-audit read | SCENEIR-T9-C1/P2 defect definition confirmed as implemented ✓ |
| 10 | Phase-1 | fixed gate predicate | 5 conjuncts, each separately named in evaluateLoadGate ✓ (read to EOF) |
| 11 | Phase-1 | PRE raw false-PASS on disk | PRE: node.exe stand-in exit 9 / 0 B DOM / NOT_PRESENT → old gate PASS; 13 PASS/0 FAIL/exit 0 ✓ |
| 12 | Phase-1 | POST/POST_STANDIN on disk | POST 22/0 (real Edge, all conjuncts); POST_STANDIN 20/2/0, all five named conjuncts + STAND_IN_PROCESS, exit 1 ✓ |
| 13 | Phase-1 | MY stand-in negative re-execution | 20 PASS / 2 FAIL / 0 NOT_PERFORMED, exit **1**; both modes FAIL naming all five conjuncts; 3 attempts each recorded ✓ (reproduces the executor's POST_STANDIN exactly) |
| 14 | Phase-1 | MY fail-closed side-error probe | wrong --three-root → T9_SERVER_STARTUP FAIL (side-error record) + loads NOT_PERFORMED + harness exit 1 ✓ (separation of concerns works) |
| 15 | Phase-2 | container identities re-measured | Models.ark 128,742,137 B / f660d055… ✓; Models.bnt 395,412,868 B / c950a8c2… (REQUIRED pin) ✓ |
| 16 | Phase-2 | MY own ARK sequential walk | 2,492 entries; chain ends EXACTLY at CD offset (128,603,536); EOCD total 2,492; EOCD+22 == file size; 0 duplicate names ✓ |
| 17 | Phase-2 | MY own BNT2 directory walk | magic BNT2; 5,596 entries; directory ends EXACTLY at footer-8; 0 overlaps / 0 payload gaps / monotonic; 0 duplicates ✓ |
| 18 | Phase-2 | re-hash bounded sample | 16 ARK entries (4 primaries + 12) + 15 BNT entries (incl. entry 781 = 218757.nif): offset/size/CRC32/SHA256 ALL MATCH the phase-2 catalogs ✓; 218757 SHA 3e8a22c2… reproduced ✓ |
| 19 | Phase-2 | four primary pins vs physical ARK payloads | sizes + SHA256 MATCH ✓ (08d80c67…/220f549b…/02fc860a…/4cc5f920…) |
| 20 | Phase-2 | counts & arithmetic | 2,492 / 4,833 / 5,596 / 8,381 vs catalog artifacts ✓; 1,815+440+237 = 2,492 ✓; 4,838+757+1 = 5,596 ✓; 1,551+17+3,270+758 = 5,596 ✓ (also from raw batch-state JSONL: 4,838 rows = 3,270 FAILED + 1,551 DECODED + 17 NO_MESH ✓, 0 parse errors, 0 duplicates) |
| 21 | Phase-2 | census | CD 4 files / 424,407,359 B ✓; PCG 1,818 files / 2,384,417,861 B ✓ |
| 22 | Phase-3 | reader re-run (nif41_deep CLI) | 4/4 DECODED; regenerated block dumps BYTE-IDENTICAL to PHASE3_BlockDumps ✓ |
| 23 | Phase-3 | names / blocks / complexity / extents / placement / components | 26/38/22/14 blocks ✓; all Desktop names reproduced ✓; 1192/1340/1200/864 tri, 2384/2680/2400/1698 vert ✓; maxAxis 31765.85/33739.21/32789.15/26940.91 (raw 31765.8515625/33739.205078125/32789.1484375/26940.9072265625) ✓; placement VERTICES ✓; components 596/670/600/419 ✓; validation ok/0 warnings ✓ |
| 24 | Phase-3 | **MY independent bounds countercheck** (own minimal raw-byte NIF-4.1 reader; ZERO executor imports) | COUNTERCHECK_PASS ×4: full closure (EOF exact), block/vertex/triangle counts match, per-axis vertex min/max within 0.01 of published, identity TRS independently confirmed ✓ |
| 25 | Phase-3 | texture discipline | 0 texture bindings / UNTEXTURED_PROXY_MESH on all 19 shapes ✓; 19 material edges MATERIAL_APPLIED=YES + BROWSER_OBSERVED=PIXEL_RENDER (per-model PNG SHA recorded) ✓; no Ark-tail interpretation transfer (RAW_ONLY labels; no textureId claims — grep clean) ✓ |
| 26 | Phase-3 | PCG935 batch numbers | 1,551 processed / 0 parse errors / 3,357 NAME_NOT_FOUND / 794 material refs / 4,151 edges / 6 edge-less — ALL verified from CSV aggregates + raw JSONL (4,151 rows, 0 parse failures) + batch summary ✓ |
| 27 | Phase-3 | native control re-read | 4× EXITED exit=1, stdout 0 B, stderr "Error loading stream." verbatim ✓; full provenance records (argv/cwd/env-delta/exe SHA fd693af2…/timeout 30 s) ✓ |
| 28 | Phase-4 | catalog battery re-run | **33 PASS / 0 FAIL / 0 NOT_PERFORMED, exit 0** ✓ (my console: 00_CONTROL_INTERNAL_QC/raw/QC_CATALOG_CONSOLE.txt) |
| 29 | Phase-4 | unit + app regression re-runs | 24 PASS / exit 0 ✓; 22 PASS / exit 0 ✓ |
| 30 | Phase-4 | MY catalog server lifecycle (port 8188) | startup regeneration ✓; status coverage EXACT (8,088 = 2,492+5,596; extent 1,555/6,533; decode distribution CATALOG_ONLY 2,488 / FAILED 3,270 / DECODED 1,551 / VERSION_GATED 758 / DECODED_NO_MESH 17 / DECODED_FULL_CLOSURE 4) ✓; rows paging math ✓ (81 pages); four-preview wire pins ✓ (payload+container SHA headers MATCH); stop + port freed (32 ms) ✓ |
| 31 | Phase-4 | denial battery (mine) | 18 synthetic denials (12 fetch + 6 raw-socket): ALL refused with named JSON errors (PREVIEW_NOT_ESTABLISHED, UNKNOWN_ASSET_ROUTE, STATIC_FILE_NOT_ALLOWEDLISTED, PATH_TRAVERSAL_BLOCKED, BACKSLASH_IN_URL, ROUTE_NOT_FOUND, DENIED_EXPLICIT, METHOD_NOT_ALLOWED_READ_ONLY) ✓ — includes wrong-ID, non-previewable REAL entry 65678, PCG id, server-side module, traversal ×4, unknown route, bogus sort, POST |
| 32 | Phase-4 | real-browser /catalog through FIXED gate | headless Edge: ALL FIVE conjuncts PASS, READY, 98,906 B DOM, both era labels present ✓ |
| 33 | Phase-4 | screenshot spot-check | fresh PNG 121,320 B → PRIVATE_OUTPUT only; non-triviality PASS (1,096 unique colors, lumaStdDev 41.8, 1280×800) ✓ |
| 34 | Proprietary | census of 99 changed text files | 0 embedded PNG/DDS/TGA payload bytes; 0 bulk NIF headers; 0 long base64; 0 long hex payload runs; 0 binary files; the 5 "BNT2" hits are format-knowledge prose/comments (my threshold's false positives) ✓ — report package is metadata-only ✓ |
| 35 | Proprietary | private artifact identities | **20/20** referenced private artifacts verified by path+size+SHA256 (CATALOG_COVERAGE privateArtifactReferences) ✓; render spot-check decodes OK (1,536×257, non-blank) ✓ |
| 36 | Skill | chapter review | concise; every claim source+scope labeled; era discipline; no "engine 100%"; version gates; honest negatives (NAME_NOT_FOUND as measured fact); proxy-vs-render role ✓ — EXCEPT the P3-2 example defect |
| 37 | Skill numeric claims | overlap 2,177 ✓ (recomputed); 65678.nif dual-existence ✓; "656865.nif" nonexistent (P3-2) |
| 38 | Hygiene | JSON validity | 33/33 report-package JSONs strict-parse OK (UTF-8) ✓; TEXTURE_LINK_DISPOSITIONS.csv parse → P2-1 |
| 39 | Hygiene | era labels / UNKNOWN-never-zero | era labels on every checked record ✓; UNKNOWN visible as UNKNOWN (17 DECODED_NO_MESH = REAL measured 0, extent UNKNOWN) ✓ |
| 40 | Hygiene | INTERVENTION_LEDGER completeness | all four phases with PIDs/ports/lifetimes/port-freed proofs + honest deviations (orphan self-kill, flake retry, Start-Process block, UI calibration fix) ✓ |

## 4. Package hygiene — files present vs missing (persistence TODOs)

Present (read/verified): PLAN_AND_ALLOWLIST.md, PREREGISTRATION.md, INPUT_IDENTITIES.json,
CATALOG_COVERAGE.json, CATALOG_METHOD.md, CATALOG_UI_NOTES.md, DEEP_ANALYSIS.md,
PRIMARY_MODEL_ROWS.json, TEXTURE_LINK_DISPOSITIONS.csv, TEST_RESULTS.json,
INTERVENTION_LEDGER.md, raw/** (T9 PRE/POST/POST_STANDIN/POST_RUN1/PIXEL + T9_PHASE4(+_FINAL) +
CATALOG gate summaries/DOM dumps/transcripts/PIXEL calibration), 00_CONTROL_INTERNAL_QC/** (this QC).

**Missing (persistence-phase TODOs):**
- **REPORT.md** (final report; persistence phase).
- **CLAIM_MATRIX.csv — ABSENT.** Required schema (one row per load-bearing claim):
  `claim_id, phase, era, subject, claim_text, status (CONFIRMED/STRONGLY_SUPPORTED/PLAUSIBLE/UNVERIFIED/REJECTED), evidence_class (original bytes / independently generated / project derivative), evidence_ref (path+SHA256), countercheck_ref (path+SHA256 of the independent check), negative_control (falsifier + result), coverage_mode (FULL_READ/RECOMPUTED/CENSUS_ONLY/BOUNDED_INSPECTION/NOT_CHECKED), revalidation_gate (exact predicate), notes`.
  Suggested first rows: the four primary decodes (countercheck = this QC's QC8 + CAT_BOUNDS_COUNTERCHECK), catalog counts (countercheck = this QC's QC4 own-walk rehash), T9 gate fix (countercheck = my stand-in re-run), texture dispositions (countercheck = QC3 sums).
- **LIMITATIONS.md** (bounded reader scope; 3,270 FAILED with loud errors; 758 VERSION_GATED; CD_2003 2,488 CATALOG_ONLY; pad-field UNKNOWN; tail slack OBS-1; the 41/19 tga stubs UNKNOWN; INTERACTIVE NOT_PERFORMED; the P2-1/P3 findings and their repairs).
- **EVIDENCE_INDEX.md** (index of every artifact incl. private references by path+SHA).
- **HANDOFF.md**.
- **MANIFEST (last, report-package only, self-excluded, bijection-verified)** — persistence phase.

## 5. Honest NOT_CHECKED / bounded inspection

- **NOT full-read to EOF** (outputs verified by execution + independent counterchecks instead):
  `tools/pecompat/catalog_data.mjs` (39.7 KB — pins/sort/wire verified behaviorally via my server
  probes), the 7 catalog suite implementations EXCEPT catalog_bounds_countercheck.test.mjs (read
  fully — genuinely independent scanner confirmed), `compat/catalog-app.js / catalog-table.js /
  catalog-preview.js / catalog.html / catalog.css` (verified by battery + my real-browser load),
  phase-2 tool bodies (ark_index, bnt_index, catalog_census, catalog_sniff, catalog_rankings,
  vfs_inspect, nif_batch_extent — outputs independently re-derived by my own readers QC4),
  phase-3 tools other than nif41_deep (extract/renders/pcg935_name_batch/collect/texture_dispositions
  — outputs re-verified), phase-4 tools (catalog_pixel_render, texture_chain, phase4_*), full body
  of t9_pixel_render.mjs (its behavior verified via PIXEL_RUN raw + my own replication of the
  --screenshot pattern) and png_nontrivial.mjs (used by me; analysis results sanity-checked).
- NOT re-executed: the cross-era candidate probe (9 PCG935 candidates; honest PROBE_FAILED
  records retained — not load-bearing for the four-primary claims); the executor's 5-shot PIXEL
  gate as-is (replaced by my fresh single-shot capture + non-triviality analysis per the QC
  assignment); the full depth-6 GLB search (bounded v4-tree re-search instead, OBS-5).
- The 4,151-row JSONL and 4,838-row batch state: full parse + count + histogram (no per-row
  semantic re-derivation).
- The historical SceneIR packages, the EU2008-era copies, the canonical eudoria-clean tree
  beyond the recorded status, and all original containers beyond bounded reads: not touched.

## 6. Witness state (at QC end)

- Port 8140 / PID 21288 (foreign SceneIR reference): ALIVE, node, LISTENING, never touched —
  verified at QC start AND end; still the ONLY server-sceneir process; zero leftover processes
  of mine (node/Edge censuses clean); all my ports freed (8160/8161/8188/8197/8199).
- Canonical master 3fbe93e (local/origin/fresh-remote); worktree HEAD 59641ca; no commits,
  no pushes, no staging by this QC.

## 7. Disposition

- REPAIRS_PERFORMED = NONE (the one authorized targeted repair round was not needed for QC
  scope; executor-evidence defects → findings above with exact corrections for the persistence
  phase).
- The persistence phase may proceed: fix P2-1 (CSV quoting) + append the P3-1 ledger correction
  + fix the P3-2 skill example + resolve P3-3 (BOM) at persistence; then REPORT.md / CLAIM_MATRIX.csv
  / LIMITATIONS.md / EVIDENCE_INDEX.md / HANDOFF.md / manifest-last.
- QC verdict stands separate from MASTER_ACCEPTED and from milestone closure per the worker
  contract. HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO;
  CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES (unchanged).

— pe-master-auditor, FRESH_INTERNAL_REVIEW, 2026-10-10. QC artifacts: `00_CONTROL_INTERNAL_QC/QC1…QC16_*.json` + `raw/QC_*` captures + this REVIEW.md + QC_RESULTS.json.
