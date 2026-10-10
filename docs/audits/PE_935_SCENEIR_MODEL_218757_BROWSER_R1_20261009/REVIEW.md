# REVIEW.md — Internal QC of PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

QC_ORIGIN = FRESH_INTERNAL_REVIEW (pe-master-auditor, fresh session, dispatched directly by
PE-MASTER; internal to PE-MASTER — **NOT an independent Desktop post-audit**).

RUN_ID = PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
WORKTREE = D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1
AUDITED EXECUTOR WORK = phase 1 (SETUP_PREFLIGHT_AND_CONTROLS) + phase 2 (IR_ADAPTER_UNIT_TESTS) +
phase 3 (APP_SERVER_TESTS) artifacts on disk at the worktree, BASE 3fbe93eec04759395223e6677b5040273d29222a.
QC DATE = 2026-10-10. QC WORK AREA = `00_CONTROL_INTERNAL_QC/` inside this package (all QC scripts,
console captures, re-run raw outputs and AMEND_LOG.md live there).

---

## 1. Governance / boundary re-verification (duty 1) — all CONFIRMED

- Governing contract identity re-verified by QC:
  `C:\Users\User\Documents\ChatGPT\PE\OPENCODE_SCENEIR_218757_BROWSER_R1_20261009\OPENCODE_SCENEIR_218757_BROWSER_R1.md`
  = 18,739 B / SHA256 1C7FC42F3023B9A2F37FE6E6F3830B217E35DF35D91A48F0455F57CD06D14DB3 — MATCHES the dispatch pin.
- Worktree HEAD = `3fbe93eec04759395223e6677b5040273d29222a` on branch
  `codex/pe-sceneir-218757-r1-20261009` == BASE (no drift; the only tracked modification is
  `package.json`).
- Canonical master `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` still at
  `3fbe93eec04759395223e6677b5040273d29222a` on `master`, with EXACTLY the 6 known foreign untracked
  groups (PE_935_FC1_P2_CLOSURE..., PE_935_MODEL_218757_PLACEMENT_SEARCH..., PE_935_NINODE_SLOT17...,
  PE_935_P1_CLOSURE..., PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN..., experiments/) — untouched.
- Other worktrees intact: `worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1` (5290e79) +
  `worktrees\WORK_AUDIT_REPORTS` (1312f89).
- CHANGED-PATH CENSUS vs contract §3 allowlist — FULLY COMPLIANT: `package.json` (scripts-only diff:
  three npm scripts added, dependencies untouched, three 0.185.0 retained); untracked new groups
  `.opencode/skills/pe-gamebryo-rosetta/**` (3 files), `compat/**` (7), `src/pecompat/**` (6),
  `tools/pecompat/**` (3), `tests/pecompat/**` (tests/ contains ONLY tests/pecompat; 14 files),
  `docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/**` (REPORT_REPO_PATH).
  `src/pesource/**` = ZERO diff vs HEAD (git diff HEAD -- src/pesource/ empty) and the witness test
  confirms. **No out-of-allowlist path found.** docs/pecompat/ was NOT used (allowed but optional).

## 2. Phase-1 re-verification (duty 2) — CONFIRMED

- Contract identity: see above. Controls A/B exist and are non-vacuous and internally consistent:
  - CONTROLS_A.json: 10 pillar instances (04/05/06/07/08/10/14/16/18/20), all resolving to master
    `[TerrainSample]pillar`, 10/10 template-id matches, 10 distinct instance LinkIDs, 0/10 instances
    with own NIF path (master `.\..\NIFs\smallpillar.nif` inherited), TWO distinct instance transforms
    (pillar 04 / pillar 05), smallpillar.nif recorded as NIF **20.5.0.4** with NO reader attempted.
  - CONTROLS_B.json + raw logs RE-READ BY QC: `raw/CONTROL_B/ROTATED_SCALED_PARENT.stdout.txt`
    contains verbatim `World Bound: C <96,202,306>, R 0`; `THREE_LEVEL_SOCKET.stdout.txt` contains
    `C <58,221,363>, R 0`; both exit 0; structure counts (2/2 and 3/3) match the JSON records.
  - INPUT_IDENTITIES spot re-hashes (QC, own Get-FileHash): Models.bnt (395412868 B /
    c950a8c2...d3bee0) MATCH; 218757 pin copy (57316 B / 3e8a22c2...12cf36) MATCH; both fixtures
    (327 B 56fe7fec...; 430 B 0c71d5fd...) MATCH; SceneGraphPrinter.exe (663552 B / fd693af2...)
    MATCH. 5/5 required identities CONFIRMED. One stale self-tool hash row found → F-QC-1 (below),
    repaired via AMEND-1 (see 00_CONTROL_INTERNAL_QC/AMEND_LOG.md).

## 3. Phase-2 re-verification (duty 3) — the load-bearing core: CONFIRMED

**QC RE-EXECUTION RESULTS TABLE (all QC's own executions; console + machine records under
00_CONTROL_INTERNAL_QC/):**

| Check | Executor claim | QC re-execution | Result |
|---|---|---|---|
| Unit suite with pinned container | 24 PASS / 0 FAIL / 0 NOT_PERFORMED | `node tests/pecompat/run_tests.mjs --models <Models.bnt>` (QC run, incl. `--json-out` machine record) | **24 / 0 / 0 — MATCH** |
| Unit suite negative control (no --models) | 17 PASS / 1 loud NOT_PERFORMED | QC run without `--models` | **17 PASS / 1 NOT_PERFORMED (T5 loud) — MATCH** |
| T1 native controls | IR+THREE == (96,202,306)/(58,221,363) | QC machine record: irCompose=threeCompose=[96,202,306] / [58,221,363] | **MATCH (both engines, tol 1e-4)** |
| controlB_compare tool | PASS maxDiff 0 both | QC re-ran the tool on both fixtures | **PASS maxDiff 0 both** |
| T5 14/14 associations + 28/28 fingerprints | assoc 14, finger 14, roundtrip true | QC re-run machine record | **MATCH** |
| T5 fingerprint spot-check (QC OWN reader over raw payload bytes) | vertex/index SHA256 values | QC's own NiTriShapeData cursor parser (00_CONTROL_INTERNAL_QC/QC_fingerprint_spotcheck.mjs) over the pin-copy payload (SHA-verified) and the dump's claimed block ranges: block 20 (92v/56t) and block 47 (30v/10t) | **2/2 SPOTCHECK_PASS — QC cursor lands EXACTLY on the claimed block ends; QC-recomputed hashes match BOTH the executor dump AND the predecessor's independent Python parser (3869b16b.../56854059... and f8848efe.../c933b00a...)** |
| FILE_SCENE_SPACE artifact | 66 bounded entries | QC re-ran with `--artifact-out` to its own dir | **BYTE-IDENTICAL SHA256 227B2783... — deterministic recomputation** |
| 62+4 opaque accounting | 62 SUPPORTED + 2 PARTIALLY_UNDERSTOOD + 2 OPAQUE | QC re-run census + dump re-parse | **MATCH (arkStatuses 1:OPAQUE, 2:PU, 3:PU, 13:OPAQUE)** |
| Texture discipline | 9 TEXTURE_NAME_BOUND + 5 UNTEXTURED_NO_TEXPROP; container NOT_ESTABLISHED | QC re-run T5f + dump parse + code read | **MATCH; no cross-era substitution; per-entry 9-byte tail recorded RAW ONLY (rawHex(9)); every "textureId" occurrence in package+code is a NEGATION ("no textureId interpretation")** |
| Witness | WITNESS_UNTOUCHED | QC own byte-compare: worktree `src/pesource/NifModelReader.js` SHA256 = BASE blob SHA256 = `2c2199545fa6ae62873a3227c6fa1394cd13c8508bd1e0cdb515926079612359` (git blob 7d926fb3...); `git status -- src/pesource/` clean | **BYTE-IDENTICAL — CONFIRMED** |

Full-read coverage: QC read EVERY changed source/test/tool/app file to EOF (all 29 code files under
src/pecompat, compat, tools/pecompat, tests/pecompat + package.json + the 3 skill files + all 13
package phase artifacts + all raw evidence files). The reader (PecNif10Reader.js, 899 lines), SceneIR,
adapter, instance builder, render convert, server, app shell, both modes, api client and all 9 test
files are genuine implementations with loud fail-closed behavior and honest labels — no dead code
reported as wired, no default-success flags found (the harness counts FAIL on crash; NOT_PERFORMED is
distinct and loud; T7's denial predicates require explicit error classes; T8's negatives prove the
client fail-closed gates fire).

## 4. Phase-3 re-verification (duty 4) — CONFIRMED

- **QC server lifecycle (own instance)**: first bind attempt on 8145 failed LOUDLY (EADDRINUSE —
  itself a live demonstration of the never-replace-another-process path); QC server then started on
  **port 8146, pid 13356** (startup line + fail-closed SHA verified; blocks=66 meshes=14
  supported=62 PU=2 opaque=2), used for the QC denial battery + headless load, then stopped with
  port-freed verified; a second QC instance (pid 24128) was started for the playwright attempt and
  likewise stopped with port freed.
- **T7 denial subset (QC, own requests against its own instance)**: 10/10 DENIED_EXPLICIT
  (../, %2e%2e, absolute /D:/..., unconfigured /src/pesource, unknown asset 999999, %00 NUL, POST
  method, unknown route, three-jail ../ and encoded-backslash) — every denial carried an explicit
  error class and NO NIF/BNT payload markers in the body. Positives: app HTML 200 (canvas +
  diagnostics root), /api/status 200 (bind 127.0.0.1, port, pid, 66/14/62+2+2, three 0.185.0),
  /api/sceneir/218757 200 (payload SHA header 3e8a22c2..., 66 blocks, 14 associations, 62/2/2).
  **3/3 positives + 10/10 denials = QC_T7_SUBSET PASS.**
- **T8 app-integration suite re-run (QC)**: `node tests/pecompat/run_app_tests.mjs --models ...`
  with `--raw-dir` REDIRECTED to 00_CONTROL_INTERNAL_QC/raw_qc/ (the executor's raw/ evidence was
  NOT overwritten — verified: all executor raw mtimes remain 2026-10-10 00:10–01:05).
  **13 PASS / 0 FAIL / 0 NOT_PERFORMED — MATCH.**
- **T9 headless (QC's OWN independent execution)**: one-shot headless Edge
  (`--headless=new --user-data-dir=<dedicated QC temp profile> --virtual-time-budget=30000
  --dump-dom http://127.0.0.1:8146/`): **data-load-status=READY, canvas present, diagnostics
  present, payload SHA256 3e8a22c2... rendered, imported 14 / visible 14**. QC's DOM differs from
  the executor's committed dump in EXACTLY ONE line — the dynamic timing value
  (`server adapter load 454 ms` vs `485 ms`); 156 lines otherwise identical (structurally the same
  READY document). The app suite's in-suite T9 headless also passed inside QC's 13/13 run.
- **PE-MASTER browser evidence re-verified by QC (own parse of both files)**:
  `pm_asset_dom.html` (21,079 B): READY, canvas, payload SHA, blocks 66=62+2+2, 9+5 textures,
  imported 14/visible 14, AUTHOR_PLACED_LAB + RENDER_ADAPTER_CHOICE + PE_UNITS_NOT_CONFIRMED
  labels present. `pm_scene_dom.html` (9,324 B): READY, canvas, both instances
  (author-instance-A t(30,0,-10) / author-instance-B t(-30,0,10)), scene ledger
  **imported 28 (2x14) / visible 28 — 28-ledger consistency CONFIRMED**; the #independence line is
  empty at boot, which matches APP_AND_SERVER_NOTES §5's honest statement (it populates only after
  an apply action). Both parses PASS.
- **Server allowlist (QC read compat/server-sceneir.mjs to EOF)**: loopback-only bind hardcoded
  (`bind: '127.0.0.1'`, not configurable, line 51; `server.listen(CONFIG.port, CONFIG.bind)` line
  419); static routes are EXACT allowlist maps (COMPAT_FILES lines 62–69; PEC_MODULES 72–74; the
  request URL is used as a MAP KEY at 267–289 — it never becomes a filesystem path); the only
  prefixed fs route (three package) is jail-checked (no `..`/backslash/NUL/`%`; resolve+startsWith
  the package root; lines 215–231); GET/HEAD only (241–244); malformed %→400, NUL→400,
  backslash→400 (245–259); unknown → 404 ROUTE_NOT_FOUND (323–325); SceneIR regenerated fail-closed
  at startup (356–375). **No traversal route; no fs.readFile on user-supplied paths. CONFIRMED.**

## 5. Standing-limits compliance (duty 5) — CONFIRMED

- Greps over the report package + all committed code of this run: every `WORLD_XYZ_RECOVERED`
  occurrence is `= NO`; every `HISTORICAL_WORLD_INSTANCE` is `NOT_ESTABLISHED`; no historical
  placement claim; no "decoded Ark"/"textureId"/"Ark semantics known" overclaim (all mentions are
  negations); no milestone/gate/MASTER_ACCEPTED language in this run's changed paths (the hits are
  in BASE-committed historical packages, which this run did not touch). AUTHOR_PLACED_LAB +
  RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED labels verified in code (app.js, scene-mode.js,
  PecRenderConvert.js, index.html) AND in all three real-browser DOM captures.
- The 9-byte Ark texture tail: recorded via `rawHex(9)` only, `bytes9Semantics:
  'RAW_ONLY_UNRESOLVED_FOR_218757'`; no interpretation attempted anywhere (grep clean).
- NifModelReader.js: byte-identical to BASE (see §3).
- Canonical master / AUDIT_ENTRYPOINT / governance: untouched (see §1).

## 6. Proprietary-content census (duty 6) — CLEAN

QC scanner (00_CONTROL_INTERNAL_QC/QC_proprietary_census.mjs) over ALL changed text files: NO NIF
header strings in data context, NO long f32 vertex-array sequences, NO base64 blobs, NO long hex
dumps, NO BNT byte markers. `raw/sceneir_dump_218757.json`: 0 blocks with geometry-array fields
(byte ranges/counts/hashes only). `raw/FILE_SCENE_SPACE_TRANSFORMS_218757.json`: 66 entries, 0
array fields. `raw/HEADLESS_DOM_DUMP.html`: 0 float-array sequences (app UI text + per-block TRS —
the same bounded transform class the predecessor published). The only flagged strings are the
smallpillar.nif version-header LINE FACT ("Gamebryo File Format, Version 20.5.0.4") in
AUTHORIZATION_AND_PREFLIGHT/CONTROLS_A/SOURCE_IDENTITIES — a bounded control value explicitly
permitted by the plan (the header line was the recorded fact; no body bytes committed).
The served wire SceneIR (with geometry arrays) exists only in loopback memory — regenerated per
server start, never a committed fixture. **No proprietary payload committed.**

## 7. Skill check (duty 7) — CONFIRMED

`.opencode/skills/pe-gamebryo-rosetta/`: exactly 3 files (SKILL.md 6,567 B + 2 references, 3,502 +
3,213 B). Concise; honest limitations section (NOT_ESTABLISHED ceilings, tail UNRESOLVED, witness
single-reader warning); version gates stated (NIF 10.1.0.0 supported; 20.5.0.4 NOT supported —
"record, don't pretend"; 4.1.0.12/4.0.0.2 unsupported; stock GB 1.2 rejects PE Ark content); command
names verified against the actual package.json scripts and tools (serve:sceneir / test:pecompat /
test:pecompat:app / extract_218757 / sceneir_dump — all exist and work; QC executed them); no
overclaim ("not a claim of completed engine research", "does not establish historical placement or
complete PE compatibility"). Arithmetic consistent (4838+757+1=5596).

## 8. Package hygiene (duty 8) — CONFIRMED with notes

- All 13 phase artifacts present and non-vacuous (PLAN_AND_PATH_ALLOWLIST, AUTHORIZATION_AND_PREFLIGHT,
  PREREGISTRATION, INPUT_IDENTITIES, SOURCE_IDENTITIES, CONTROLS_A, CONTROLS_B, IMPLEMENTATION_NOTES,
  TEST_RESULTS_UNIT, TEST_RESULTS_APP, APP_AND_SERVER_NOTES, SMOKE_CHECKLIST, INTERVENTION_LEDGER).
  The FINAL-phase files (FINAL_REPORT.md, TEST_RESULTS.json, COVERAGE_AND_LIMITS.md, REVIEW.md ← this
  file, EVIDENCE_INDEX.md, HANDOFF.md, manifest) are correctly the final phase's; REVIEW.md now exists
  (this QC document) per the dispatch.
- All 13 UTF-8 JSON files parse (QC ConvertFrom-Json pass); the 4 UTF-16LE PowerShell-redirect raw
  files decode and parse with the Unicode encoding (see F-QC-5).
- INTERVENTION_LEDGER covers all execution classes: INT-1 native printer ×2 (phase 1, argv/env/timeout
  class, byte-identical local copies), INT-2 node test/tool runs (incl. the in-phase z-row repair),
  INT-3 server runs with PIDs/ports/lifetimes incl. the honest orphan record (pid 6620 stopped before
  phase end), INT-4 headless Edge executions with dedicated temp profiles + the three honest repairs.
  COMPLETE.
- Foreign untracked in the worktree = only this report package + the allowed code dirs (§1). The QC
  additions live under 00_CONTROL_INTERNAL_QC/ inside the package.
- Orphan processes at QC end: QC's OWN server instances (13356, 24128) stopped with port-freed
  verified; QC's headless Edge exited (no msedge with QC's temp profile or --headless remains).
  ONE foreign orphan pre-existed at QC start: node pid 13724 running `compat\server-sceneir.mjs` on
  port 8145, created 2026-10-10T01:15:25 with a dead parent — NINE MINUTES AFTER the executor's last
  package write (01:06:33), i.e. inside PE-MASTER's browser-audit window, NOT the executor's and NOT
  QC's. Per the kill-only-your-own discipline QC did NOT touch it; flagged to PE-MASTER (F-QC-6).

## 9. Findings (ordered by severity)

**P0 BLOCKER: none.**

**P1 MATERIAL: none.**

**P2 CORRECTNESS — F-QC-1: stale self-tool SHA256 in INPUT_IDENTITIES.json. REPAIRED (AMEND-1).**
- Location: `INPUT_IDENTITIES.json` → `controls_own_tools` → `parse_gsa_controlA.py`.
- Contradicted record: sha256 `530c3cee...967574d` vs the physical file (16,614 B) =
  `d80a908a91da932e1a2054fc686a511b91cd78b6853cb5f438b9e7dd3c4168b4` (the value CONTROLS_A.json
  already recorded). Counter-check: QC re-hash of the physical file == CONTROLS_A.json — MATCH.
- Skutek/impact: two package artifacts disagreed on one tool's identity (provenance defect; the
  parser is PRIVATE_ROOT-only, not committed; no Control-A measurement value is affected).
- Mechanism: parser edited between INPUT_IDENTITIES (00:11:31) and CONTROLS_A finalization
  (00:13:00); the row was never refreshed.
- Correction performed (the ONE targeted QC repair round, PRE/POST documented in
  `00_CONTROL_INTERNAL_QC/AMEND_LOG.md`): row corrected to the true hash with an inline
  `qc_provenance_correction` note preserving the old value for the audit trail.
  PRE-EDIT: 13,101 B / SHA256 00201BBCF65D2335C6BBB0785DEC26FA9CC0E172DD284CA001B37BA611F3FCCE;
  POST-EDIT: 13,527 B / SHA256 CE2DD4E2F70CA4F14CC8164279186042A61150C840FD21612AE84B10D35B25CC
  (JSON re-parsed OK).
- Revalidation gate: any re-hash of parse_gsa_controlA.py must equal the corrected row;
  INPUT_IDENTITIES.json and CONTROLS_A.json must agree.

**P3 HYGIENE — F-QC-2: duplicate NULL_CHILD_SLOTS warnings (66×) from an accidentally nested loop.**
- Location: `src/pecompat/PecSceneIR.js` line 250 (the NULL-child-slot warning loop sits INSIDE the
  outer `for (const b of ir.blocks)` loop, shadowing `b`); effect: the single true warning for block
  0 (19 legal NIF null child links) is emitted once per outer iteration → 66 duplicate warnings in
  `validation.warnings` (visible in `raw/sceneir_dump_218757.json` and recorded as
  `nullChildSlotWarnings: 66` in TEST_RESULTS_UNIT T5d).
- Impact: cosmetic noise in a committed raw artifact; `validation.ok`/errors/composition UNAFFECTED
  (QC re-verified the full suite green with the current code). No false claim is made (each warning
  is accurate; the count could be misread as 66 distinct issues).
- Correction (for pe-reconstruction, next code touch): dedent the inner loop one level; expected
  result: exactly 1 NULL_CHILD_SLOTS warning. NOT repaired by QC (executor code — QC does not edit
  implementation files).
- Revalidation gate: re-run the suite; sceneir_dump validation.warnings contains exactly 1
  NULL_CHILD_SLOTS entry; all tests stay green.

**P3 HYGIENE — F-QC-3: "bytes"/"B" fields in evidence records are JS CHARACTER counts, not byte counts.**
- Locations: TEST_RESULTS_APP.json positive_requests `bytes` (5296/3477/11878/13389/650153/209552),
  raw/HEADLESS_RUN.json `domBytes: 21064`, raw/sceneir_dump.stdout.txt "(42148 B)".
- Counter-check: the on-disk files measure 5323/3479/11910/13389 B and the DOM dump 21,079 B — the
  recorded values equal the UTF-16 code-unit (character) lengths exactly (QC verified each). Content
  identity is NOT in question; only the unit label is wrong.
- Impact: imprecise provenance labels; no data mismatch (QC verified the char↔file correspondence).
- Correction: relabel the fields as `chars` (or record Content-Length) in future artifacts. Not
  repaired (would ripple through multiple committed records for a cosmetic label; disclosed here).
- Revalidation gate: future T7/T9 records state chars or actual byte lengths.

**P3 HYGIENE — F-QC-4: scene-mode UI independence-line wording overstates its runtime check.**
- Location: `compat/scene-mode.js` line 173–178 — the on-screen line claims "(authored + composed
  TRS bit-identical before/after)" while the UI-level check compares only the OTHER instance's
  composed translate. The full authored+composed TRS bit-identity IS genuinely verified by
  T8_TWO_INSTANCES_INDEPENDENT (trsDeepEqual on both) through the app's own builder path.
- Impact: wording-level; no functional defect; the load-bearing separation proof is in the Node
  suite (QC re-ran it green).
- Correction: reword to "composed translate unchanged (full TRS identity verified by the
  app-integration suite)" at the next code touch.
- Revalidation gate: SMOKE_CHECKLIST step 2.4 text alignment.

**P3 HYGIENE — F-QC-5: heterogeneous encoding + one char-vs-byte line in raw stdout artifacts.**
- Locations: `raw/extract_218757.stdout.txt`, `raw/sceneir_dump.stdout.txt`,
  `raw/controlB_compare_*.json` are UTF-16LE with BOM (PowerShell `>` redirect artifacts) while the
  rest of the package is UTF-8; the sceneir_dump stdout line records "(42148 B)" for a 42,152-byte
  file (same class as F-QC-3).
- Impact: parse friction (QC decoded and verified all four; machine-parseable with the right
  encoding); no data loss.
- Correction: write future stdout captures with UTF-8 (e.g. `--json-out` / Set-Content -Encoding
  utf8). Revalidation: files decode as UTF-8 without BOM.

**P3 HYGIENE — F-QC-6 (notification, no executor defect): pre-existing foreign orphan server + one
descriptor mismatch in the QC dispatch.**
- node pid 13724 running `compat\server-sceneir.mjs`, port 8145, created 2026-10-10T01:15:25,
  parent dead — post-dates the executor's final write (01:06:33); consistent with PE-MASTER's
  browser-audit window (pm_asset_err shows a 01:09 Edge run). NOT the executor's and NOT QC's;
  left untouched per kill-only-your-own. PE-MASTER should stop it (Stop-Process -Id 13724) or adopt
  it deliberately. The executor's ledger claim "no server-sceneir process listening at handoff" was
  TRUE at their handoff time (ports 8140/8141/8142/8264 verified; 8145 never theirs).
- Additionally, the dispatch described `pm_browser_audit\pm_server_run.log`; that file does NOT
  exist on disk (the dir contains pm_asset_dom.html / pm_scene_dom.html / pm_asset_err.txt /
  pm_scene_err.txt / five 1-byte profile_* marker files). Both DOM evidence files themselves parse
  and verify (see §4). Not the executor's work; noted for the parent.

## 10. Honest NOT_CHECKED list (QC)

- Control A parser NOT re-executed by QC (its artifact structure, hash and internal consistency
  were verified; it is comparison evidence for SDK metadata, not load-bearing for the 218757
  adapter chain, whose whole path QC re-executed).
- MSVCP71.DLL/MSVCR71.DLL hashes not re-hashed by QC (runtime for the already-verified printer;
  raw Control-B outputs re-read verbatim instead).
- Native printer NOT re-executed by QC (Control-B raw logs re-read; the IR-comparison side was
  re-executed by QC through the suite + controlB_compare tool).
- The nine SDK source files (SOURCE_IDENTITIES) not re-hashed by QC (architectural references; the
  implemented transform contracts were re-verified by QC's own math review + tests).
- INTERACTIVE browser behaviors NOT performed by QC: QC's own playwright attempt failed
  (`ECONNREFUSED ::1:9222` — daemon down), CONFIRMING the dispatch's honest state. Orbit/pan/zoom/
  fit/reset/wireframe/dPVS-toggle/instance-apply/independence-line remain covered only indirectly
  by the Node app-integration suite (T8) through the app's own builder path + the automation surface
  (`window.__pecApp`), which QC re-ran green.
- TESTS_MACHINE_SUMMARY.json / TESTS_APP_MACHINE_SUMMARY.json: parsed, totals + spot-fields
  verified; not field-by-field re-diffed (their curated counterparts were fully read and are backed
  by QC's own re-runs).
- compat.css read at the structural level only (styling; not load-bearing).
- Predecessor SCENE_STRUCTURE_RESULTS.json read at the referenced-field level (roots/bounds/
  ArkTexture reference), not to EOF.
- Historical BASE packages: pattern-grepped only (out of QC scope; not this run's changes).

## 11. QC verdict

**QC_VERDICT = PASS_WITH_FINDINGS** (1×P2 — REPAIRED and revalidated via AMEND-1; 5×P3 — documented,
none load-bearing; 0×P1; 0×P0).

Every load-bearing claim of phases 1–3 was independently re-measured by QC and CONFIRMED: 24/24
unit suite, 13/13 app suite, T7 denial semantics by construction + wire, T1 native-control parity
(both engines), 14/14 + 28/28 fingerprints (with QC's own third-implementation raw-byte spot-check),
62+4/9+5 accounting, witness byte-identity, allowlist and proprietary-content cleanliness, standing
limits preserved.

### ACCEPTED_RUNNABLE_VERIFIED recommendation (contract §8 browser rule)

**The slice may NOT yet be called ACCEPTED_RUNNABLE_VERIFIED.** Honest state:

- REAL-BROWSER LOAD: verified INDEPENDENTLY THREE TIMES (executor T9 one-shot ×2 runs incl. the
  #scene deep-link scene-mode mount; PE-MASTER asset + scene DOM captures; QC's own headless Edge
  load) — all data-load-status=READY with canvas, pin checks, 14/14 client fingerprint re-hashes.
- INTERACTIVE AUTOMATION: **NOT_PERFORMED** — the playwright daemon is unavailable in this
  environment (QC's own retry attempt failed: `ECONNREFUSED ::1:9222`); orbit/free-camera/reset,
  wireframe, dPVS toggle, instance select/apply and the on-screen independence line were NOT
  observed interactively. Interactive behaviors are covered only INDIRECTLY by the Node
  app-integration suite through the app's own builder path plus the exposed automation surface.
- Recommended label for the final report:
  **BROWSER_VERIFICATION = REAL_BROWSER_LOAD_VERIFIED__INTERACTIVE_NOT_PERFORMED**
  (with SMOKE_CHECKLIST.md remaining the open interactive gate for any session with a working
  automation browser); **ACCEPTED_RUNNABLE_VERIFIED = NO** until that smoke is executed and recorded.
  The run may honestly be called: runnable, load-verified slice with 24/24 + 13/13 gates,
  HISTORICAL_PLACEMENT = NOT_ESTABLISHED, WORLD_XYZ_RECOVERED = NO, CANONICAL_GATE_EFFECT = NONE.

## 12. Machine record

Machine-readable QC results: `QC_RESULTS.json` (this directory). QC scripts, console captures and
re-run raw outputs: `00_CONTROL_INTERNAL_QC/`. The single QC amendment: `00_CONTROL_INTERNAL_QC/AMEND_LOG.md`.

**QC_VERDICT = PASS_WITH_FINDINGS**
**ACCEPTED_RUNNABLE_VERIFIED = NO (real-browser LOAD verified 3× independently; INTERACTIVE
automation NOT_PERFORMED — playwright daemon unavailable, QC's own retry confirmed)**
