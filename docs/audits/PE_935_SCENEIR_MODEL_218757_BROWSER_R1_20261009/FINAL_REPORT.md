# FINAL_REPORT — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Phase: PERSISTENCE_PUBLISH (final). Written by the pe-master-auditor
persistence worker under the PE-MASTER PERSIST_PUBLISH dispatch. No new science
in this phase; every measured value below is carried from the run's phase
artifacts (cited per field), the fresh internal QC (REVIEW.md / QC_RESULTS.json)
and PE-MASTER's own audited re-executions (PE_MASTER_REVIEW.md, persisted
verbatim in this package).

RUN_ID     = PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
RUN_CLASS  = BOUNDED_ENGINE_REFERENCE_AND_BROWSER_IMPLEMENTATION
BASE_SHA   = 3fbe93eec04759395223e6677b5040273d29222a
BRANCH     = codex/pe-sceneir-218757-r1-20261009 (worktree
             D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1)
REPORT_DATE = 2026-10-10

## 0. Human decision block (read this first)

**Nothing is needed from the human to close this run.** The authorized scope is
executed to the runnable slice; the single publication commit is prepared and
pushed on the feature branch; master is untouched.

- DESKTOP_POST_AUDIT = PENDING (a standing, separate human gate; nothing here
  claims it).
- The ONE optional future action: run `SMOKE_CHECKLIST.md` interactively in a
  session with a working automation browser. That is the single open gate
  between the honest label below and ACCEPTED_RUNNABLE_VERIFIED. It is optional
  follow-up work, not a defect of this run.
- NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES. No agent of this loop may
  start the next experiment without a new explicit authorization.

## 1. State delta (publication)

- Audit start: canonical checkout (eudoria-clean) LOCAL == origin/master ==
  fresh remote master == BASE 3fbe93eec04759395223e6677b5040273d29222a; worktree
  on the feature branch at BASE; the 2 foreign audit worktrees intact; 6 known
  foreign untracked groups in the canonical checkout untouched.
- Publication: ONE normal commit on the feature branch
  `codex/pe-sceneir-218757-r1-20261009` containing exactly the §3-allowlist
  paths of this run (see CHANGED_PATH_CENSUS below); the branch is pushed with
  `-u`; master is never pushed, merged or rewritten.
- RESULTING_SHA (discovery instruction — a file cannot contain its own commit
  SHA): `git log -1` on the branch
  `codex/pe-sceneir-218757-r1-20261009` after publication; the verified value
  is recorded in the terminal handoff block of this persistence phase
  (local HEAD == origin/BRANCH == fresh remote BRANCH == RESULTING_SHA).
- ACTUAL_REMOTE_MASTER (recorded SEPARATELY from the branch identity, per the
  publication rule): `3fbe93eec04759395223e6677b5040273d29222a` — measured by
  this persistence phase (git ls-remote origin refs/heads/master) BEFORE the
  commit and re-verified AFTER the push; master must remain (and does remain)
  the BASE commit. The feature branch identity is never conflated with it.
- REMOTE_FEATURE_BRANCH_SHA: verified after the push (git ls-remote origin
  refs/heads/codex/pe-sceneir-218757-r1-20261009); recorded in the terminal
  handoff block.

## 2. Package phases summarized (with counts)

1. **SETUP_PREFLIGHT_AND_CONTROLS** (phase 1; artifacts:
   AUTHORIZATION_AND_PREFLIGHT.md, PLAN_AND_PATH_ALLOWLIST.md,
   PREREGISTRATION.md, INPUT_IDENTITIES.json, SOURCE_IDENTITIES.json,
   CONTROLS_A.json, CONTROLS_B.json, INTERVENTION_LEDGER.md):
   governing contract identity re-verified (18,739 B / SHA256 1C7FC42F…14DB3);
   BASE/worktree/branch preflight clean; path allowlist written BEFORE
   implementation; all 5 pinned input identities MATCH (Models.bnt 395,412,868 B
   / c950a8c2…d3bee0; 218757 payload pin 57,316 B / 3e8a22c2…12cf36;
   printer fd693af2…; both fixtures); Control A = 10/10 pillar instance→master
   links with 10 distinct instance LinkIDs, master `.\..\NIFs\smallpillar.nif`
   path inherited by all 10 instance components (0 own NIF paths), exactly TWO
   instance transforms emitted (pillar 04 / pillar 05), smallpillar.nif
   recorded as NIF 20.5.0.4 (header line only; NO 20.5 reader attempted);
   Control B = 2/2 native GB 1.2 SceneGraphPrinter runs (exit 0/0) with verbatim
   probe world bound centers `C <96,202,306>, R 0` and `C <58,221,363>, R 0`.
2. **IR_ADAPTER_UNIT_TESTS** (phase 2; artifacts: IMPLEMENTATION_NOTES.md,
   TEST_RESULTS_UNIT.json, raw/TESTS_MACHINE_SUMMARY.json,
   raw/TESTS_CONSOLE_OUTPUT.txt, raw/extract_218757.stdout.txt,
   raw/sceneir_dump_218757.json, raw/sceneir_dump.stdout.txt,
   raw/controlB_compare_*.json, raw/FILE_SCENE_SPACE_TRANSFORMS_218757.json):
   NEW code under src/pecompat/ (6 modules) + tools/pecompat/ (3 CLI tools) +
   tests/pecompat/ (13 files — 9 test files + 2 harnesses + 2 helper modules,
   zero new dependencies; three 0.185.0 retained);
   unit suite 24 PASS / 0 FAIL / 0 NOT_PERFORMED with the pinned container, plus
   the no-models negative control 17 PASS / 1 loud NOT_PERFORMED
   (NOT_PERFORMED_CONTAINER_UNAVAILABLE — never silently skipped). Gate detail:
   T1 2/2 native parity (tol 1e-4, dual-engine IR+THREE), T2a–d transform
   composition incl. conversion-applied-exactly-once with a structural counter
   and a double-conversion negative control, T3 instance separation, T4
   invalid/missing-link battery (cycle / dangling child / dangling data ref /
   multi-parent full-report / missing master / dangling scene parent / duplicate
   instanceId / instance cycle) + missing-texture diagnostics, T5a–g pinned
   extraction + 66-block census (62 SUPPORTED + 2 PARTIALLY_UNDERSTOOD +
   2 OPAQUE) + 14/14 mesh/data associations + 28/28 vertex/index fingerprints
   vs the predecessor's independent Python parser + hierarchy/closure decisions
   + FILE_SCENE_SPACE bounds + texture binding census + bounded transform
   artifact, T6 witness-457485 untouched (byte-identical to BASE). One honest
   in-phase repair: the T2d analytic control caught a z-row bug in
   PecRenderConvert.conversionMatrix; fixed; suite re-run green.
3. **APP_SERVER_TESTS** (phase 3; artifacts: TEST_RESULTS_APP.json,
   APP_AND_SERVER_NOTES.md, SMOKE_CHECKLIST.md, raw/TESTS_APP_MACHINE_SUMMARY.json,
   raw/HTTP_TRANSCRIPTS.json, raw/HEADLESS_RUN.json, raw/HEADLESS_DOM_DUMP.html,
   raw/APP_INTEGRATION_MEASURED.json): ONE compat app (7 files) + a bounded
   loopback server (compat/server-sceneir.mjs); app suite 13 PASS / 0 FAIL /
   0 NOT_PERFORMED. T7 = real-HTTP server start + status + static surface +
   SceneIR endpoint (fail-closed regenerated from the pinned container; cache
   key 218757:3e8a22c2…:pec-nif101-adapter-v1:pec-sceneir-v1) + path-denial
   battery 22/22 explicit denials (18 traversal/unconfigured-root/unknown +
   4 malformed/method; every body checked for NIF/BNT payload markers — none)
   + server lifecycle with port-freed proof; T8 = app-integration through the
   app's own builder path (pinned asset load, wire→asset rebuild with client
   pin + cross-checks, tampered-wire REFUSED negatives, client-side 14/14
   fingerprint re-hash, two-instance independence with trsDeepEqual bit-identity
   + shared-geometry object identity, honest diagnostics/ledger incl. the dPVS
   heuristic ledger 14→9 with 5 explicit exclusions); T9 = real headless Edge
   boot-to-READY (DOM evidence). Three honest repairs preserved (T8 authored2
   crash; missing boot() invocation; a Set-Content double-encoding reversed
   byte-accurately) with the final state re-measured 13/13.
4. **Fresh internal QC** (00_CONTROL_INTERNAL_QC/, REVIEW.md, QC_RESULTS.json,
   AMEND_LOG.md): QC_ORIGIN = FRESH_INTERNAL_REVIEW; verdict
   PASS_WITH_FINDINGS — 0 P0, 0 P1, 1 P2 (F-QC-1, repaired in the single
   authorized QC repair round AMEND-1 and revalidated; PE-MASTER adjudicated
   REPAIR_ACCEPTED with its own hash verification of both the corrected JSON
   (POST 13,527 B / CE2DD4E2…D35B25CC) and the tool file (16,614 B /
   d80a908a…4168b4)), 5 P3 documented (F-QC-2 … F-QC-6; F-QC-6 resolved by
   PE-MASTER — see §4). QC re-executed: unit 24/24, app 13/13 (raw redirected;
   executor raw untouched), 10/10 denial subset on its own server instance, own
   headless Edge load READY, third-implementation raw-byte fingerprint
   spot-check 2/2, FILE_SCENE_SPACE artifact byte-identical re-run, witness
   byte-identity, proprietary-content census CLEAN, allowlist census compliant.
5. **PE-MASTER audit** (PE_MASTER_REVIEW.md, verbatim in this package):
   own re-execution of the unit suite (24/24 + 17 PASS/1 loud NOT_PERFORMED
   negative control in the worktree), own headless Edge loads of BOTH modes
   (asset READY + scene READY; scene ledger 28 = 2×14; labels
   AUTHOR_PLACED_LAB / RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED present in
   the DOM), own server lifecycle (loopback 8140, api/status verified, log in
   PRIVATE_ROOT), own git censuses (package.json scripts-only diff;
   src/pesource/ zero diff; witness untouched), REPAIR_ACCEPTED adjudication,
   MASTER_ACCEPTED (advisory) verdict, and the resolution of finding F-QC-6
   (see §4). VERDICT = MASTER_ACCEPTED (advisory); CANONICAL_GATE_EFFECT =
   NONE.
6. **PERSISTENCE_PUBLISH** (this phase): final report package files
   (FINAL_REPORT.md, TEST_RESULTS.json, COVERAGE_AND_LIMITS.md,
   PE_MASTER_REVIEW.md, HANDOFF.md, EVIDENCE_INDEX.md), MANIFEST_SHA256.csv
   generated LAST (self-excluded), staged-diff proprietary review, one branch
   commit, branch push only, remote verification.

## 3. Section 9 measured fields block (contract §9)

```text
RUN_ID     = PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
BASE_SHA   = 3fbe93eec04759395223e6677b5040273d29222a
ACTUAL_REMOTE_MASTER = 3fbe93eec04759395223e6677b5040273d29222a
             (recorded separately from the branch identity; measured by
             git ls-remote before the commit and re-verified after the push;
             master remains the BASE commit — never pushed/merged by this run)
RESULTING_SHA = discover: `git log -1` on branch
             codex/pe-sceneir-218757-r1-20261009 after publication (a file
             cannot contain its own commit SHA); the verified value is in the
             terminal handoff block of this persistence phase.
REMOTE_FEATURE_BRANCH_SHA = verified after push (git ls-remote origin
             refs/heads/codex/pe-sceneir-218757-r1-20261009); recorded in the
             terminal handoff block.
BRANCH     = codex/pe-sceneir-218757-r1-20261009

SDK_INSTANCE_LINK_CONTROL =
    10/10 pillar instances (04/05/06/07/08/10/14/16/18/20) resolved to the one
    master [TerrainSample]pillar; 10/10 template-id matches; 10 distinct
    instance LinkIDs (TemplateID is a DEFINITION identifier, NOT instance
    identity); 0/10 instances with their own NIF path (master
    .\..\NIFs\smallpillar.nif inherited via NiSceneGraphComponent); TWO
    distinct instance transforms inspected (pillar 04 / pillar 05); scene
    dependency .\Palettes\TerrainSample.pal explicit; smallpillar.nif recorded
    as NIF 20.5.0.4 (header line only — NO 20.5 reader attempted; the GB 1.2
    stock tool does not support it). Control class:
    SERIALIZED_METADATA_LINK_CONTROL_NOT_NATIVE_SCENE_LOAD; values are GB26 SDK
    sample authoring values — NOT PE coordinates.
SDK_NATIVE_TRANSFORM_CONTROLS =
    2/2 native runs (original stock GB 1.2 SceneGraphPrinter, byte-identical
    local copy, VC7.1 runtime via sandbox-local PATH prepend, argv
    `-in "<fixture>" -bs`, 30 s timeout, both EXITED 0):
    ROTATED_SCALED_PARENT.nif (327 B / 56fe7fec…4d5a19) → verbatim
    `C <96,202,306>, R 0`; THREE_LEVEL_SOCKET.nif (430 B / 0c71d5fd…441873) →
    verbatim `C <58,221,363>, R 0`. Probe-value caveat: camera bound centers
    source-qualified for these two controls only — NOT geometry pivots, NOT
    generalized.
IR_TRANSFORM_TESTS =
    T1 2/2 PASS tol 1e-4 vs the native ground truth (dual-engine: PecTransform
    IR compose AND THREE.Matrix4 compose both equal (96,202,306) and
    (58,221,363); fixture SHA verified before compare). T2a–d PASS: nonidentity
    asset root (analytic (4,3,9)); parent rotate/scale/translate (analytic
    (96,202,306)); reparent-without-compensation (local TRS unchanged, world
    recomposed, compensating engine would FAIL the after-value check);
    conversion-applied-EXACTLY-ONCE — structural application counter = 1,
    original serialized TRS intact, double conversion differs (negative
    control), choice labeled RENDER_ADAPTER_CHOICE (x,z,-y)×0.01 /
    PE_UNITS_NOT_CONFIRMED. Suite negative control without --models: 17 PASS /
    1 loud NOT_PERFORMED.
INSTANCE_SEPARATION_TEST =
    T3 PASS (two instances of one shared asset: unique instanceIds, shared
    geometry object/array identity, wrapper separation, mutating A leaves B
    exactly unchanged, asset IR unmutated) + T8 bit-identity re-verified through
    the app's own builder path (trsDeepEqual on the OTHER instance's authored
    AND composed TRS before/after; BufferGeometry === shared; conversion count
    1 per instance; scene-mode ledger 28 = 2×14 in the real-browser DOM).
MODEL_218757_INPUT_SHA256 =
    3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36
    (57,316 B; fail-closed pins at the adapter, the server and the app client;
    extracted by the independently checked BNT index entry — ordinal 781 /
    offset 116223520 / size 57316 as CROSS-CHECKS; container
    c950a8c2…d3bee0 verified on every load).
IMPORTED_MESH_COUNT = 14 (all 14 NiTriShape/NiTriShapeData associations
    preserved, incl. the 5 dPVS-named helper candidates)
VISIBLE_MESH_COUNT = 14 (default ledger: 14 imported / 14 visible / none
    excluded; the clearly-labeled dPVS-name-hint heuristic toggle changes the
    ledger to 14/9 with 5 explicit per-mesh exclusions — HIDDEN_BY_USER_DPVS_
    HEURISTIC_TOGGLE; meshes remain addressable/inspectable; the app never
    claims 14 rendered when hidden)
SUPPORTED_BLOCKS = 62
OPAQUE_BLOCKS = 4 (2 PARTIALLY_UNDERSTOOD: NiArkImporterExtraData,
    NiArkTextureExtraData; 2 OPAQUE: NiArkAnimationExtraData,
    NiArkViewportInfoExtraData) — the 62+4=66 ceiling of contract §1 is
    preserved; no Ark content is silently turned into semantic decodes
TEXTURE_BINDING_STATUS =
    9 TEXTURE_NAME_BOUND + 5 UNTEXTURED_NO_TEXPROP (the 5 dPVS-named meshes
    carry material-only refs); container resolution NOT_ESTABLISHED everywhere
    (names/property bindings only — no texture bytes bound in this run); the
    nine-byte Ark texture tail recorded RAW only
    (RAW_ONLY_UNRESOLVED_FOR_218757) — no new tail semantics derived.
BROWSER_VERIFICATION =
    REAL_BROWSER_LOAD_VERIFIED__INTERACTIVE_NOT_PERFORMED
    (3 independent real-browser loads, all data-load-status=READY: executor T9
    one-shot ×2 incl. the #scene deep-link scene-mode mount; PE-MASTER headless
    Edge loads of BOTH modes — asset READY + scene READY with ledger 28 = 2×14
    and the labels AUTHOR_PLACED_LAB / RENDER_ADAPTER_CHOICE /
    PE_UNITS_NOT_CONFIRMED present in the DOM; QC's own headless Edge load.
    Interactive automation was NOT performed — the playwright daemon is
    unavailable in this environment (QC's own retry failed:
    ECONNREFUSED ::1:9222); orbit/pan/zoom/fit/reset/wireframe/dPVS-toggle/
    instance-select/apply are covered only INDIRECTLY by the Node
    app-integration suite through the app's own builder path plus the exposed
    automation surface window.__pecApp.)
    ACCEPTED_RUNNABLE_VERIFIED = NO (SMOKE_CHECKLIST.md remains the open
    interactive gate).
APP_URL = http://127.0.0.1:8140/ (local only; loopback bind 127.0.0.1 is
    hardcoded/not configurable; start: `npm run serve:sceneir` in the worktree)
SERVER_LIFECYCLE = loopback-only bind; free-port bind/close probe BEFORE
    listen + loud exit(1) on EADDRINUSE (never replaces another process);
    PID printed at startup; stop = terminate the printed PID; port-freed
    rebind probe verified after stop in the T7 lifecycle record
QC_ORIGIN = FRESH_INTERNAL_REVIEW (pe-master-auditor, fresh session, direct
    PE-MASTER dispatch; internal to PE-MASTER — NOT an independent Desktop
    post-audit)
OPEN_FINDINGS = F-QC-2 (66× duplicate NULL_CHILD_SLOTS warnings — nested loop
    in src/pecompat/PecSceneIR.js; fix at next code touch: dedent; gate:
    exactly 1 warning, suite green), F-QC-3 ("bytes"/"B" fields are JS
    character counts — relabel chars/Content-Length in future artifacts),
    F-QC-4 (scene-mode independence-line wording — reword at next code touch;
    full TRS bit-identity is genuinely proven by T8), F-QC-5 (UTF-16LE raw
    stdout artifacts — capture future stdout as UTF-8), plus the OPEN
    INTERACTIVE SMOKE GATE (SMOKE_CHECKLIST.md not executed — automation
    daemon unavailable). None load-bearing. F-QC-1 REPAIRED (AMEND-1;
    REPAIR_ACCEPTED). F-QC-6 RESOLVED (see §4).
MANIFEST_BIJECTION = PASS — the package manifest (MANIFEST_SHA256.csv) is
    generated LAST, self-excluded, over the report package only; full
    physical-file/row bijection verified programmatically at persistence with
    an independent re-hash pass on a separate code path (duplicate/missing/
    extra/size/SHA). If any package file is edited later, the manifest MUST be
    regenerated (contract §9).
CHANGED_PATH_CENSUS =
    compat/ 7 files; src/pecompat/ 6; tools/pecompat/ 3; tests/pecompat/ 13
    (tests/ contains ONLY tests/pecompat: 9 test files + 2 harnesses + 2
    helper modules); .opencode/skills/pe-gamebryo-rosetta/
    3; REPORT_REPO_PATH 68 files (61 phase-1…QC artifacts + 7 final-phase
    files incl. the manifest); package.json 1 MODIFIED — scripts-only diff
    (three npm scripts added; dependencies untouched; three 0.185.0 RETAINED).
    Total = 101 committed files (staged census verified). All inside the
    contract §3 allowlist; src/pesource/ ZERO diff (witness untouched);
    docs/pecompat/ (allowed, optional) NOT used.
    (Census note: QC REVIEW.md §1 prose says "14 files" for tests/pecompat;
    the actual disk census is 13 files, consistent with QC's own 29-file code
    pin (compat 7 + src/pecompat 6 + tools/pecompat 3 + tests/pecompat 13)
    and with the staged census. The machine pin and the staged census are
    authoritative; the QC prose count is a census-side slip, non-load-bearing.)
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## 4. Findings summary (dispositions)

- **F-QC-1 (P2) — stale self-tool SHA256 in INPUT_IDENTITIES.json — REPAIRED
  (AMEND-1; adjudicated REPAIR_ACCEPTED by PE-MASTER).** The single authorized
  QC repair round: the row for parse_gsa_controlA.py was corrected to the true,
  physically re-measured hash (d80a908a…4168b4, matching CONTROLS_A.json), with
  the old stale value preserved inline in a `qc_provenance_correction` note.
  PRE-EDIT INPUT_IDENTITIES.json: 13,101 B / 00201BBC…F3FCCE → POST-EDIT:
  13,527 B / CE2DD4E2…D35B25CC (PE-MASTER verified both identities on disk).
  Revalidation gate: re-hash equals the corrected row; INPUT_IDENTITIES.json and
  CONTROLS_A.json agree. CLOSED for this run.
- **F-QC-2 (P3, OPEN)** — 66× duplicate NULL_CHILD_SLOTS warnings from an
  accidentally nested loop in src/pecompat/PecSceneIR.js:250. Cosmetic;
  validation.ok/errors/composition unaffected (QC re-ran the suite green).
  For pe-reconstruction at the next code touch: dedent the loop; gate: exactly 1
  warning in sceneir_dump validation.warnings; suite green.
- **F-QC-3 (P3, OPEN)** — "bytes"/"B" fields in evidence records are JS
  character counts (TEST_RESULTS_APP positive_requests, raw/HEADLESS_RUN
  domBytes, raw/sceneir_dump stdout "(42148 B)"). Content identity verified;
  unit label only. Future artifacts: label chars or record Content-Length.
- **F-QC-4 (P3, OPEN)** — scene-mode UI independence-line wording overstates
  the in-page runtime check (compat/scene-mode.js:173–178). The load-bearing
  full-TRS bit-identity IS proven by T8_TWO_INSTANCES_INDEPENDENT (re-verified
  by QC and PE-MASTER). Reword at next code touch; gate: SMOKE_CHECKLIST 2.4
  alignment.
- **F-QC-5 (P3, OPEN)** — UTF-16LE-with-BOM raw stdout artifacts
  (raw/extract_218757.stdout.txt, raw/sceneir_dump.stdout.txt,
  raw/controlB_compare_*.json) in an otherwise UTF-8 package; QC decoded and
  parsed all four. Future captures: UTF-8.
- **F-QC-6 (P3) — RESOLVED (PE-MASTER).** The QC-notified foreign orphan
  (node pid 13724 running compat\server-sceneir.mjs, port 8145, created
  2026-10-10T01:15:25) was identified as PE-MASTER's OWN first-attempt server
  from its browser-audit window (the QC dispatch descriptor had labeled it by
  a wrong path); it has been KILLED by PE-MASTER. The
  pm_server_run.log descriptor pointed one directory too deep — the log EXISTS
  at `PRIVATE_ROOT\pm_server_run.log` (701 B); the full evidence chain is
  intact. Not an executor defect; the executor's "no server running at handoff"
  claim was true at their handoff time.
- **Interactive smoke gate (OPEN, by design of contract §8)** —
  SMOKE_CHECKLIST.md (boot/panels, asset-mode orbit/pan/zoom/fit/reset/
  wireframe/select/dPVS toggle, scene-mode instance select/apply/independence/
  reset, fail-closed reload) has NOT been executed: the automation daemon is
  unavailable in this environment. This is the single gate to
  ACCEPTED_RUNNABLE_VERIFIED.
- **CODE_FINDINGS = NONE material** (PE-MASTER). No P0/P1 anywhere in the run.
- **RETRACTIONS = NONE required** (this run created no superseded claims; it is
  a new implementation slice; the predecessor package is cited read-only and
  remains standing). **CANON_CONFLICTS = NONE** (standing limits of contract §1
  preserved verbatim in every artifact).

## 5. Honest limits (NOT_CHECKED — from REVIEW.md §10, carried forward)

- Control A parser NOT re-executed by QC (structure/hash/internal consistency
  verified; comparison evidence only, not load-bearing for the 218757 chain).
- MSVCP71/MSVCR71 DLL hashes not re-hashed by QC (printer runtime; raw
  Control-B outputs re-read verbatim instead).
- Native printer NOT re-executed by QC (raw logs re-read; the IR-comparison
  side re-executed through the suite + controlB_compare tool).
- The nine SDK source files (SOURCE_IDENTITIES) not re-hashed by QC
  (architectural references; implemented transform contracts re-verified via
  math review + tests).
- INTERACTIVE browser behaviors NOT performed by anyone in this environment
  (executor, PE-MASTER, QC): playwright daemon down (QC's own attempt failed
  ECONNREFUSED ::1:9222). Indirect coverage only (Node app-integration suite
  through the app's own builder path + the window.__pecApp automation surface).
- TESTS_MACHINE_SUMMARY / TESTS_APP_MACHINE_SUMMARY parsed and spot-verified,
  not field-by-field re-diffed (curated counterparts fully read + backed by
  QC's own re-runs).
- compat.css read at the structural level only (styling; not load-bearing).
- Predecessor SCENE_STRUCTURE_RESULTS.json read at the referenced-field level,
  not to EOF. Historical BASE packages: pattern-greps only (out of QC scope).
- PE-MASTER NOT_CHECKED: Control-A parser re-execution; interactive browser
  behaviors; DLL re-hashes; 12 of 14 fingerprint hashes not spot-recomputed by
  PE-MASTER itself (covered by executor + QC independent re-runs + QC's own
  raw-byte spot-check 2/2).
- Scope limits of the slice itself: COVERAGE_AND_LIMITS.md (no historical
  placement; no texture container resolution; no Ark tail semantics; NIF
  20.5.0.4 not supported; terrain not integrated — authored grid; single-model
  scope; three 0.185.0 retained).

## 6. How to run (commands)

From the worktree `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1`
(requires the pinned local Models.bnt at
`D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt`):

```text
npm run serve:sceneir
    -> prints: sceneir server http://127.0.0.1:8140/ pid=<PID>
    -> URL: http://127.0.0.1:8140/   (local only)
    -> stop: terminate the printed PID (Stop-Process -Id <PID>, or Ctrl+C)

npm run test:pecompat [--models "D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"]
    -> unit suite (24 tests; WITHOUT --models: 17 PASS + 1 loud NOT_PERFORMED)
npm run test:pecompat:app
    -> app/server suite (13 tests; owns its bounded server lifecycle)
```

Optional env overrides: PORT (default 8140), PECOMPAT_MODELS_BNT,
PECOMPAT_THREE_ROOT, SCENEIR_LOG_REQUESTS=1.

## 7. Manifest scope statement (exact)

**The report package manifest (MANIFEST_SHA256.csv) covers ONLY the report
package** — every physical file under
`docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/` except the
manifest itself. **Code/skill/test changes (compat/, src/pecompat/,
tools/pecompat/, tests/pecompat/, .opencode/skills/pe-gamebryo-rosetta/,
package.json) are listed in the CHANGED_PATH_CENSUS (§3) and the commit
census, NOT hashed by the report manifest.** A report-only manifest does not
hash the implementation; bijection is enforced at package scope. EVIDENCE_INDEX.md
lists every package file (self-excluded) plus local-only/private artifacts BY
MANIFEST REFERENCE ONLY.

## 8. Terminal result

RUN_STATUS = COMPLETED_WITH_MASTER_ACCEPTED_ADVISORY__INTERACTIVE_SMOKE_OPEN.
The run is honestly runnable and load-verified (24/24 + 13/13 gates; 3
independent real-browser loads READY), NOT interactively verified
(ACCEPTED_RUNNABLE_VERIFIED = NO). HISTORICAL_PLACEMENT = NOT_ESTABLISHED;
WORLD_XYZ_RECOVERED = NO; CANONICAL_GATE_EFFECT = NONE; DESKTOP_POST_AUDIT =
PENDING; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.
