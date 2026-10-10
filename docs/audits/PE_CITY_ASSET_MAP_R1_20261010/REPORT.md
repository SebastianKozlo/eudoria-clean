# REPORT.md — PE_CITY_ASSET_MAP_R1_20261010 — FINAL REPORT

RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
BASE_FEATURE_SHA = 59641caa1b14ade84e1842ca36b395842deb241e
BRANCH = codex/pe-city-asset-map-r1-20261010 (worktree D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1)
GOVERNING_CONTRACT = C:\Users\User\Documents\ChatGPT\PE\OPENCODE_CITY_ASSET_MAP_R1_20261010.md (13,212 B, SHA256 9EED1A48F88F5F01744AB4D27527BADF6B3D5DCA8B74B6C16D25398DDD85B080 — identity re-verified at persistence)
DATE = 2026-10-10 (phases 1–4 executed same day; this file written by the §8 persistence phase)
QC = fresh internal QC PASS_WITH_FINDINGS (0 P0 / 0 P1 / 1 P2 / 3 P3 — all four fixed at persistence, see 00_CONTROL_INTERNAL_QC/AMEND_LOG.md); PE-MASTER audit verdict = MASTER_ACCEPTED (advisory), persisted verbatim in PE_MASTER_REVIEW.md.

## 0. Human decision block (read this first)

- **Nothing is needed from the human to use anything in this run.** The branch is published; the
  four QC-mandated fixes were applied before the manifest; no open blocker depends on a human
  choice.
- **DESKTOP_POST_AUDIT = PENDING** — the fresh internal QC (REVIEW.md) is NOT an independent
  Desktop post-audit; the human may order one at will. Until then the run's science stands at
  "internally QC-verified + PE-MASTER-accepted (advisory)".
- **What you can open right now (catalog viewer):**
  - START (in the worktree): `npm run serve:catalog` (default port 8161, configurable via
    `PECATALOG_PORT`).
  - OPEN: `http://127.0.0.1:8161/catalog` — full 8,088-row catalog of both eras. Deep links:
    `http://127.0.0.1:8161/catalog#model=193313` (any of 192374 / 193207 / 193313 / 193684)
    opens that primary's 3D preview directly (hierarchy tree, per-part isolation, wireframe [W],
    fit [F], reset [R], original-coordinates view [C], bounds/origin + UV/texture diagnostics).
  - STOP: terminate the printed PID (Ctrl+C in the owning console or `Stop-Process -Id <PID>`;
    the startup line prints `catalog server http://127.0.0.1:<PORT>/ pid=<PID>`).
  - The server never binds 8140: **the OLD 218757 SceneIR viewer remains at
    `http://127.0.0.1:8140/` as the untouched foreign READ_ONLY reference** (PID 21288, alive
    and verified untouched at run end).
- Standing scope flags (unchanged): HISTORICAL_PLACEMENT = NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED = NO; no city/place identification anywhere in this run; node names are
  byte-level reproduced hypotheses, never game classes.

## 1. State delta (git, all measured)

- Start: worktree HEAD == 59641ca on the new branch, created from BASE_FEATURE_SHA; master
  local == origin == fresh remote == 3fbe93eec04759395223e6677b5040273d29222a
  (EXPECTED_MASTER_AT_DISPATCH confirmed); old SceneIR worktree untouched at 59641ca; foreign
  server 8140/PID 21288 alive and untouched throughout (re-verified at persistence).
- This run = a SINGLE feature-branch commit of only §8-allowlist paths + this report package.
- **RESULTING_SHA** (discover instruction): in the worktree run `git rev-parse HEAD` — the
  single run commit on branch codex/pe-city-asset-map-r1-20261010.
- **REMOTE_FEATURE_SHA** (after push): `git ls-remote origin refs/heads/codex/pe-city-asset-map-r1-20261010`
  — equals RESULTING_SHA (verified at push; see HANDOFF.md for the measured triple).
- **ACTUAL_MASTER = 3fbe93eec04759395223e6677b5040273d29222a — UNTOUCHED** (local == origin ==
  fresh remote, verified again at persistence; no merge, no master push).
- CANONICAL_GATE_EFFECT = NONE; no milestone closure; no governance/AUDIT_ENTRYPOINT change.

## 2. Phase summaries (counts; sources: the phase artifacts, all QC-reverified)

### Phase 1 — SETUP_T9_FIX_BROWSER_LOAD (T9 gate repair + browser load separation)

- T9 PRE (defective gate, preserved raw): 13 PASS / 0 FAIL / harness exit 0 **including the
  reproduced false-PASS** — stand-in `node.exe` exit 9, 0 B DOM, no markers → old gate PASS.
- T9 fix: `tests/pecompat/headless_load.test.mjs` rewritten around the production 5-conjunct
  gate `evaluateLoadGate`: exitCode===0 AND DOM_NONEMPTY AND CANVAS_PRESENT AND
  DIAGNOSTICS_PRESENT AND STATUS_READY — every conjunct separately named; per-conjunct synthetic
  negatives through the SAME gate; side-errors (server startup, raw persistence, server
  lifecycle) separated from load results; STAND_IN_PROCESS labeling for env-override binaries;
  bounded flake retry (max 3, all recorded); aggregator exits nonzero on any FAIL.
- T9 POST: 22 PASS / 0 FAIL / exit 0 (real Edge, asset + #scene, all five conjuncts each).
- T9 POST_STANDIN: 2 FAIL (both modes; all five named missing conjuncts + STAND_IN_PROCESS),
  harness exit 1. QC independently reproduced this run (20 PASS / 2 FAIL / exit 1) and the
  fail-closed side-error probe (startup error → FAIL record + loads NOT_PERFORMED + exit 1).
- Browser interaction separation (contract §0/§5): LOAD = EXECUTED AND VERIFIED;
  PIXEL_RENDER = EXECUTED AND VERIFIED; INTERACTIVE = NOT_PERFORMED (automation daemon down —
  ECONNREFUSED on 127.0.0.1:9222 and [::1]:9222; honest, never faked). Therefore
  **no BROWSER_VERIFIED claim** (the §5 promotion rule needs all three).
- Regression green throughout: unit 24/24, app 22/22.

### Phase 2 — METADATA_CATALOG (both eras; inventory + rankings, no forced decoding)

- Input identities re-measured fail-closed (INPUT_IDENTITIES.json): CD_2003 Models.ark
  128,742,137 B / f660d055…; Textures.ark 289,585,581 B / d611d125…; PCG_9_3_5 Models.bnt
  395,412,868 B / c950a8c2… (**REQUIRED pin MATCH**); Textures.bnt 973,942,771 B / 61acd13b…;
  3 × ArkVFS02 (textures/materials/templates .vfs).
- File censuses: CD_2003 4 files / 424,407,359 B; PCG_9_3_5 1,818 files / 2,384,417,861 B
  (100% measured; a census, not format understanding).
- Container catalogs (per-entry CRC32 + payload SHA256 recomputed 100%): CD_2003 Models.ark
  **2,492 entries** (all NIF: 4.1.0.12 × 1,815 + 4.0.0.2 × 440 + 4.0.0.0 × 237); CD_2003
  Textures.ark **4,833** (DDS 1,359 / TGA_HEADER 3,433 / OTHER 41 tiny stubs — content UNKNOWN);
  PCG_9_3_5 Models.bnt **5,596** (Gamebryo 10.1.0.0 × 4,838 + NetImmerse 4.1.0.12 × 757 +
  4.0.0.2 × 1); PCG_9_3_5 Textures.bnt **8,381** (explicitly NOT the 8,095-entry EU2008-era
  copy). 0 duplicate names, 0 overlaps/gaps, 0 read failures anywhere; boundary checks exact
  (ARK chain ends at CD offset, EOCD+22 == file size; BNT2 directory ends at footer-8).
- Dual-index verification: standard-ZIP-layout central directory == sequential local-header scan
  (0 mismatches). **Skill correction observed:** the pe-ark-vfs skill's alternative central-
  directory layout FAILED 100% on the real files (recorded for future skill maintenance; not a
  retraction of run evidence).
- Pad-field honesty: BNT2 trailing u32 == crc32 for only 3,435/5,596 Models.bnt entries —
  MEASURED_PARTIAL, semantics UNKNOWN where unequal (never called "CRC stored twice").
- VFS: bounded header/string inspection only — **record layouts NOT established** (textures.vfs
  1 string; materials.vfs 2,668 strings incl. HLSL shader text; templates.vfs mostly binary).

### Phase 3 — FOUR_MODELS_DEEP_ANALYSIS (the four CD_2003 primaries)

- All four DECODED_FULL_CLOSURE with the bounded NIF-4.1 reader (all blocks + TopObjects footer +
  EOF exact; the run's single reader repair documented in the tool header). Python dual-decode
  (`nif_parser_v2.py`, independent second decoder) AGREES on every standard block, name, ref and
  geometry count. All Desktop name hypotheses reproduced byte-level from the originals.
- **Placement finding: VERTICES** — every local TRS identity on all four (0 non-identity; spread
  growth 1.0); the layout lives entirely in vertex coordinates. Connected components
  (596/670/600/419) are NOT building counts.
- Native control (stock Gamebryo 1.2 SceneGraphPrinter, provenance-captured): **4 ×
  NATIVE_LOAD_REJECTED** — exit 1, stdout 0 B, stderr verbatim `Error loading stream.`
  (the "plausibly loadable by the stock printer" hypothesis is refuted by measurement; the
  executed cross-check layer is therefore the dual decode + QC's independent bounds countercheck).
- GLB comparison: **NO_GLB_PRESENT_FOR_THESE_IDS** — no GLB exists for 192374/193207/193313/193684
  anywhere in the searched trees (v4 `assets/cd2003/` holds only 16 OTHER GLBs); numeric
  comparison SKIPPED honestly (nothing to compare).
- PCG_9_3_5 texture-name batch (1,551 phase-2-decoded models re-parsed with the EXISTING reader):
  1,551/1,551 processed, 0 parse errors; 4,151 edges: **3,357 NAME_NOT_FOUND** + 794
  material-reference edges; NAME_FOUND_EXACT 0 — an honest negative (the same-era Textures.bnt
  catalog is numeric `NNNNNN.dat`; model-side ArkTexture names are descriptive). Cross-era
  resolution: NONE (refused by construction; no edge ever crossed eras).
- Cross-era candidates: bounded pointers only (size-proximate 4.1.0.12 candidates; 2 probe-
  decoded with generic names — no name kinship; 7 PROBE_FAILED loud, preserved). NO
  identification of any city/place.

### Phase 4 — CATALOG_MODE_SERVER_TESTS (the /catalog viewer + gates)

- New `/catalog` mode + bounded loopback server (extends the proven sceneir server design,
  labeled; the 218757 app files byte-identical). Startup regenerates both era catalogs from the
  pinned originals (fail-closed pins incl. the REQUIRED Models.bnt pin); status coverage exact:
  8,088 rows = 2,492 + 5,596; extent measured 1,555 / UNKNOWN 6,533; decode distribution
  CATALOG_ONLY 2,488 | FAILED 3,270 | DECODED 1,551 | VERSION_GATED 758 | DECODED_NO_MESH 17 |
  DECODED_FULL_CLOSURE 4.
- Catalog battery: **33 PASS / 0 FAIL / 0 NOT_PERFORMED, exit 0** (archive safety incl.
  wrong-magic/truncated/CRC-tamper; Models.bnt wrong-pin refusal; bounded reads 0.038%/0.16% of
  file sizes; duplicate-ID era separation (2,177 same-name pairs stay TWO distinct assets);
  independent bounds countercheck; texture gates incl. wrong-ID/wrong-era/missing-image; UNKNOWN
  sort/filter/badge; preview math + known-vertex no-accidental-centering; T7-style server +
  denials; T9-style real-browser loads through the FIXED gate; raw persistence + lifecycles).
- PIXEL_RENDER gate (calibrated 5 shots: table + all four previews): PASS — e.g. table PNG
  121,319 B / 1,095 unique colors / lumaStdDev 41.82; per-model preview PNGs with SHA256
  recorded (PRIVATE_OUTPUT only).
- Denials: exact-allowlist statics, jailed three-subtree reads, traversal/encoded/absolute/
  backslash refusals, GET/HEAD-only 405, no whole-corpus route, containers never exposed.
  Battery transcripts preserved (raw/CATALOG/CATALOG_HTTP_TRANSCRIPTS.json); QC's independent
  18-probe denial battery (12 fetch + 6 raw-socket): ALL refused with named JSON errors
  (fetch dot-segment normalization documented as OBS-3 — raw sockets confirmed the server's OWN
  PATH_TRAVERSAL_BLOCKED / STATIC_FILE_NOT_ALLOWEDLISTED refusals).
- Regression 218757 at phase end: unit 24/24 + app 22/22, exit 0 (raw/T9_PHASE4_FINAL).
- Material observation update: the four primaries' 19 material edges updated to
  MATERIAL_APPLIED=YES + BROWSER_OBSERVED=PIXEL_RENDER after the real-browser preview renders
  (texture classes stay 0 — UNTEXTURED_PROXY_MESH is the measured fact; per-model PNG SHA256 in
  TEXTURE_LINK_DISPOSITIONS.csv).

### Fresh internal QC (REVIEW.md; QC artifacts 00_CONTROL_INTERNAL_QC/)

- QC_VERDICT = PASS_WITH_FINDINGS (0 P0 / 0 P1 / 1 P2 / 3 P3). Every load-bearing numeric claim
  re-tested was reproduced exactly: own ARK/BNT boundary walks; 31-entry re-hash (ALL match);
  4/4 deep-analysis rerun byte-identical block dumps; OWN independent bounds countercheck ×4
  (minimal raw-byte reader, zero executor imports, agreement ≤ 0.01); batch sums from raw JSONL;
  catalog battery 33/33 + unit 24/24 + app 22/22 fresh re-runs; fresh real-browser LOAD (all
  five conjuncts READY, 98,906 B DOM) + fresh PIXEL (121,320 B PNG, 1,096 unique colors, luma
  41.8 — non-triviality PASS); proprietary census of 99 changed text files (0 payload bytes);
  20/20 private artifacts verified by path+size+SHA256.
- Findings → fixed at THIS persistence phase (PRE/POST hashes in 00_CONTROL_INTERNAL_QC/AMEND_LOG.md):
  - **P2-1** TEXTURE_LINK_DISPOSITIONS.csv RFC4180 quoting (1,545 aggregated rows; sums
    unchanged — strict parse revalidated: 1,587 data rows × 7 fields; 3,357/794/4,151/1,545/6).
  - **P3-1** INTERVENTION_LEDGER F12 count 1,588 → 1,587 (append-only correction C1; F12
    historical row preserved byte-identically).
  - **P3-2** skill example `656865.nif` (exists in NEITHER catalog) → replaced with verified
    `266865.nif` (+ kept `65678.nif`); re-verified against BOTH phase-2 catalogs before the edit.
  - **P3-3** private PHASE3_NativeControl/run_records.json UTF-8 BOM stripped (choice made:
    strip; content byte-identical after the 3-byte removal; strict JSON.parse now succeeds;
    limitation note kept in LIMITATIONS.md).
- Observations OBS-1..OBS-5 recorded (Models.bnt 150,133 B tail slack UNKNOWN; UTF-16LE console
  captures class; fetch dot-segment normalization; cross-era vs era-scoped largest rows; 16
  cd2003 GLBs / 0 primary GLBs).

## 3. The §8 measured return block

- **RESULTING_SHA:** the single run commit — `git rev-parse HEAD` in the worktree (written
  after this file; see HANDOFF.md for the measured value).
- **REMOTE_FEATURE_SHA:** equals RESULTING_SHA — `git ls-remote origin
  refs/heads/codex/pe-city-asset-map-r1-20261010` (verified at push).
- **ACTUAL_MASTER:** 3fbe93eec04759395223e6677b5040273d29222a (local == origin == fresh remote;
  UNTOUCHED by this run).
- **URL / start / stop:** catalog = `http://127.0.0.1:8161/catalog`; `npm run serve:catalog`;
  stop = terminate the printed PID (details §0). The OLD 218757 viewer remains at
  `http://127.0.0.1:8140/` (READ_ONLY foreign reference, untouched).
- **T9 disposition:** PRE false-PASS reproduced and preserved; POST clean→PASS through the
  5-conjunct production gate; every removable conjunct has its own negative (each FAIL names
  its conjunct); stand-in process class labeled and can never be a positive control; aggregator
  nonzero on FAIL; QC independently re-executed the negatives (exit 1) and the fail-closed
  side-error probe. LOAD verified ×2 real Edge + QC fresh; PIXEL_RENDER 5/5 + QC fresh;
  INTERACTIVE NOT_PERFORMED → **no BROWSER_VERIFIED claim**.
- **Model counts per era / rows:** CD_2003 Models.ark 2,492 entries; PCG_9_3_5 Models.bnt 5,596
  entries; catalog rows total **8,088** (2,492 + 5,596). Texture containers: CD_2003
  Textures.ark 4,833; PCG_9_3_5 Textures.bnt 8,381 (era-separated always; 2,177 same-name
  overlaps = two distinct assets each).
- **Ranking coverage:** PAYLOAD_SIZE FULL both eras (2,492 / 5,596 — index metadata).
  SCENE_EXTENT: CD_2003 **4 of 2,492** measured (the four primaries; 2,488 UNKNOWN) + PCG_9_3_5
  **1,551 (+4) of 5,596** — extent measured 1,555 / UNKNOWN 6,533. COMPLEXITY: same
  measured/UNKNOWN discipline (PCG 1,568 measured = 1,551 with geometry + 17 genuinely-zero
  rows [REAL zeros, never UNKNOWN-as-0]; CD 4 measured). All tables LARGEST-MEASURED with
  coverage lines; "largest of all" never claimed; UNKNOWN sorts last with a badge.
- **The four model statuses (each DECODED_FULL_CLOSURE; FILE_SCENE_SPACE, ORIGINAL units):**
  - `192374.nif` (66,759 B; 22 blocks; names Box01, MSC, MAC, signs): maxAxisExtent
    32,789.148; footprint X 32,789.148 / Z 5,952.574; 1,200 tri / 2,400 vert / 4 shapes /
    5 nodes; components 600; placement VERTICES; **UNTEXTURED_PROXY_MESH** (0 texture
    bindings, numTex=0, 0 UV sets — explicit visual fallback, NOT a textured PASS); native
    control NATIVE_LOAD_REJECTED "Error loading stream."; GLB comparison
    NO_GLB_PRESENT_FOR_THESE_IDS; 4 material edges REFERENCE_CONFIRMED (post-phase-4:
    MATERIAL_APPLIED=YES + BROWSER_OBSERVED=PIXEL_RENDER).
  - `193207.nif` (47,167 B; 14 blocks; names Box06, Object01): maxAxisExtent 26,940.907;
    footprint X 26,940.907 / Z 1,570.065; 864 tri / 1,698 vert / 2 shapes / 3 nodes;
    components 419; placement VERTICES; UNTEXTURED_PROXY_MESH; NATIVE_LOAD_REJECTED;
    NO_GLB_PRESENT_FOR_THESE_IDS; 2 material edges REFERENCE_CONFIRMED (phase-4 update same).
  - `193313.nif` (66,726 B; 26 blocks; names Outpost39_proxymesh, MSC, signs, build, MAC):
    maxAxisExtent 31,765.852; footprint X 31,765.852 / Z 5,308.884; 1,192 tri / 2,384 vert /
    5 shapes / 6 nodes; components 596; placement VERTICES; UNTEXTURED_PROXY_MESH;
    NATIVE_LOAD_REJECTED; NO_GLB_PRESENT_FOR_THESE_IDS; 5 material edges REFERENCE_CONFIRMED
    (phase-4 update same).
  - `193684.nif` (75,805 B; 38 blocks; names signs, mlti, wall, signs01, mac, build, cont,
    forts): maxAxisExtent 33,739.205 (largest measured of the four — the y-axis); footprint X
    32,069.273 / Z 3,762.275; 1,340 tri / 2,680 vert / 8 shapes / 9 nodes; components 670;
    placement VERTICES; UNTEXTURED_PROXY_MESH; NATIVE_LOAD_REJECTED;
    NO_GLB_PRESENT_FOR_THESE_IDS; 8 material edges REFERENCE_CONFIRMED (phase-4 update same).
  - Extents counterchecked independently (suite raw-byte scanner + QC's own zero-import
    reader; agreement 0.01 tolerance; identity-TRS precondition measured, not assumed).
    Connected components are NOT building counts. No city/role identification claimed.
- **Texture chain coverage (dispositions frozen before measurement):**
  - Four primaries: NAME_FOUND 0 / REFERENCE_CONFIRMED 19 material edges (4+2+5+8) /
    CONTAINER_ENTRY_RESOLVED 0 / IMAGE_DECODED 0; after phase 4: MATERIAL_APPLIED=YES +
    BROWSER_OBSERVED=PIXEL_RENDER on those 19 (per-model PNG SHA256 recorded); texture classes
    remain 0 — the measured negative is the finding (UNTEXTURED_PROXY_MESH).
  - PCG_9_3_5 batch: 1,551 processed; 3,357 NAME_NOT_FOUND texture-name edges; 794 material
    refs; 4,151 edges total; 1,545 models with ≥1 edge; 6 edge-less (ArkTexture blocks present,
    no shape-bound entries — in the batch summary, not the per-model CSV rows); Ark tails
    RAW_ONLY (the 218757 textureId retraction stands; nothing transferred between models/eras).
  - Cross-era texture resolution: NONE (refused by construction; verified).
- **Browser interaction results:** LOAD = EXECUTED_AND_VERIFIED (×2 real Edge through the FIXED
  gate + QC fresh); PIXEL_RENDER = EXECUTED_AND_VERIFIED (5 calibrated shots + QC fresh
  non-triviality PASS); INTERACTIVE = NOT_PERFORMED (automation daemon down — ECONNREFUSED
  127.0.0.1:9222 and [::1]:9222; honestly never promoted to BROWSER_VERIFIED).
- **Unresolved findings (open backlog, none blocking this publication):**
  - P3-class QC findings: FIXED at persistence (AMEND_LOG.md); no product-source defect found
    (the 218757 app files byte-identical).
  - Ark animation/importer tails OPAQUE / PARTIALLY_UNDERSTOOD (raw bytes recorded).
  - The 41 tiny CD_2003 TGA stubs (4–96 B): content UNKNOWN (no image header; CRC-verified only).
  - VFS record layouts NOT established (bounded header/string inspection only).
  - TEXTURES name-catalog reconciliation: NAME_FOUND_EXACT=0 is a measured gap; resolving it
    likely needs textures.vfs/materials.vfs layouts (NOT established this run).
  - 3,270 PCG_9_3_5 FAILED decode rows preserved with loud verbatim errors (parser surface
    deliberately not expanded); 758 VERSION_GATED never attempted; 2,488 CD_2003 CATALOG_ONLY.
  - Models.bnt 150,133 B tail slack between last payload and directory: boundary census exact
    (0 overlaps/gaps between payloads), slack semantics UNKNOWN (do not interpret).
  - Automation daemon down → INTERACTIVE open gate (future interactive SMOKE of catalog +
    preview remains the standing path to BROWSER_VERIFIED — NOT authorized by this run).
  - Cross-era candidate probe: 2 decoded (generic names — no kinship), 7 PROBE_FAILED loud;
    no identification (by design).
- **Manifest + changed paths:** report package manifest = `MANIFEST_SHA256.csv` (LAST, written
  after every package file, self-excluded, bijection-verified by an independent code path);
  full disk census incl. private references in EVIDENCE_INDEX.md. Changed paths (outside the
  report package): 4 MODIFIED files — `.opencode/skills/pe-gamebryo-rosetta/SKILL.md`,
  `package.json` (two new scripts `serve:catalog` / `test:pecompat:catalog`; three stays pinned
  0.185.0; NO new dependencies), `tests/pecompat/headless_load.test.mjs` (the T9 gate fix),
  `tests/pecompat/run_app_tests.mjs` (safe default raw dir + honest relabel); NEW files —
  `compat/` × 6 (catalog mode + server), `tools/pecompat/` × 20, `tests/pecompat/` × 9,
  `.opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md` × 1, plus this
  report package. **No `src/pesource` change; the 218757 app files byte-identical; no path
  outside the §8 allowlist.** (Exact staged census in HANDOFF.md.)

## 4. Standing flags (frozen)

HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES

(Designed-but-not-executed next-experiment candidates, by measured value, are listed in
PE_MASTER_REVIEW.md NEXT_EXPERIMENT — none started, none authorized by this run.)
