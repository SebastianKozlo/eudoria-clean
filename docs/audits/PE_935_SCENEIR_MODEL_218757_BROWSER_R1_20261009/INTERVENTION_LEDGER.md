# INTERVENTION_LEDGER — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Append-only. Every intervention class actually executed during the run is
recorded here per phase. No entry is ever edited after being appended.

## Phase: SETUP_PREFLIGHT_AND_CONTROLS (2026-10-09/10)

### INT-1 — NATIVE_TOOL_EXECUTION (CHILD_PROCESS_PATH_DLL_EXPOSURE)
- Class: CHILD_PROCESS_PATH_DLL_EXPOSURE — the ORIGINAL stock Gamebryo 1.2
  SceneGraphPrinter (fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c,
  byte-identical LOCAL copy) was executed headlessly as a child process on
  byte-identical LOCAL copies of the two synthetic fixtures; the VC7.1
  runtimes (MSVCP71.DLL df96156f..., MSVCR71.DLL 8094af5e...) were exposed to
  the child via a PATH prepend of the sandbox work dir ONLY
  (`...controlB_work`); no system PATH or System32 copy was touched.
- Executions: 2 (ROTATED_SCALED_PARENT.nif, THREE_LEVEL_SOCKET.nif), argv
  `-in "<fixture>" -bs`, cwd = the sandbox work dir, per-process timeout 30 s
  (both EXITED well within it), exits 0/0.
- Raw evidence: `raw/CONTROL_B/ROTATED_SCALED_PARENT.stdout.txt` (+ empty
  .stderr), `raw/CONTROL_B/THREE_LEVEL_SOCKET.stdout.txt` (+ empty .stderr);
  structured record: CONTROLS_B.json. Private runner:
  `...controlB_work\controlB_run.ps1`.
- Inputs untouched: originals (fixtures, printer, DLLs, SDK trees) SHA-verified
  unchanged by construction of byte-identical copies; no original file written.
- No other process was started, replaced or stopped. No server started in this
  phase. No client execution. No new EXE bodies (the runner is a PowerShell
  script; the printer is the original vendor binary).

### Other interventions this phase: NONE
- Git: ONE `git worktree add` in the canonical checkout (the single authorized
  write; canonical HEAD/branch untouched, re-verified). No commits, no pushes
  in this phase (publication happens only in the final persistence phase).
- File writes: only the new worktree (report package), PRIVATE_ROOT (work
  copies + own tools), and the 99_Audits PRIVATE_ROOT for this run. No
  original/foreign path modified.

## Phase: IR_ADAPTER_UNIT_TESTS (2026-10-10)

### INT-2 — BOUNDED_NODE_PROCESS_EXECUTION (tests/tools only)
- Class: BOUNDED_NODE_PROCESS_EXECUTION — the phase's own test suite and CLI
  tools were executed as ordinary child Node processes
  (`node tests/pecompat/run_tests.mjs`, `node tools/pecompat/*.mjs`), each
  invocation bounded by the caller's timeout (longest run ~seconds; whole
  suite wall-clock 832 ms measured, excluding the 395 MB container hash in
  the adapter path). All processes EXITED (harness exit 0; tools exit 0/0/0/0).
  No server, no browser, no client execution, no network access, no native
  binary execution in this phase.
- Inputs READ_ONLY: Models.bnt (container SHA re-verified against the pin on
  every adapter load), the Control B fixture copies in this run's
  PRIVATE_ROOT controlB_work (SHA-verified against the phase-1 pins at test
  time), and the predecessor measurement files committed at BASE. No original
  or private file was modified.
- File writes: ONLY the allowed worktree areas (src/pecompat/**,
  tools/pecompat/**, tests/pecompat/**, REPORT_REPO_PATH/**). package.json /
  package-lock.json / src/pesource/ untouched (verified by git diff and the
  T6 witness test). One scratch generator script was written to the host temp
  dir (C:\Users\User\AppData\Local\Temp\opencode) — outside the repo, not
  committed, not part of the changed-path census.
- No Git operations in this phase (no add/commit/push; publication is the
  final persistence phase per the dispatch).
- One in-phase code repair (preserved honestly): the T2d conversion-once test
  caught a z-row bug in PecRenderConvert.conversionMatrix (z'=-u*x instead of
  z'=-u*y); fixed, suite re-run green. The failing intermediate state is
  documented in IMPLEMENTATION_NOTES.md §4.5 and TEST_RESULTS_UNIT.json
  honest_notes.

## Phase: APP_SERVER_TESTS (2026-10-10)

### INT-3 — LOCAL_LOOPBACK_SERVER_EXECUTIONS (own bounded processes only)
- Class: OWN_LOOPBACK_SERVER_EXECUTION — the app's bounded loopback server
  (`node compat/server-sceneir.mjs`) was executed repeatedly in this phase:
  every instance bound 127.0.0.1 ONLY, regenerated the 218757 SceneIR from the
  pinned Models.bnt at startup (container+payload SHA256 fail-closed verified
  EVERY start; measured adapter load 480–640 ms), and was stopped by this
  phase's own code with a port-freed rebind probe (T7_SERVER_LIFECYCLE:
  portFreed=true measured after every stop).
- Formal harness executions (tests/pecompat/run_app_tests.mjs, THREE runs —
  the THIRD is the final recorded evidence, generated with the exact final
  code state incl. the #scene deep-link initial-mode feature):
  - Run 1 (honest partial: T8 crashed — preserved in TEST_RESULTS_APP.json
    honest_notes): T7 server port 8140 (own child, lifecycle record PASS,
    stopped, freed); T9 server port 8141 pid 4500 (stopped, freed; headless
    dump captured the pre-repair PENDING boot state honestly).
  - Run 2 (13/13 PASS after the targeted repair pass): T7 server port 8264
    (8140 was momentarily held by the orphan below) pid 20948, startup 624 ms,
    stopped, portFreed=true after 750 ms; T9 server port 8141 pid 12404
    (exit 0, loadStatus READY), stopped, freed.
  - Run 3 (FINAL — recorded evidence in raw/*, after the app.js initial-mode
    deep-link addition): T7 server port 8140 pid 2340, startup 624 ms,
    stopped, portFreed=true; T9 server port 8141 pid 7424 (exit 0,
    data-load-status READY, DOM 21064 B), stopped, freed. 13/13 PASS.
- Manual/diagnostic server instances (all this phase's own; all stopped and
  verified freed unless noted): pid 21856 port 8140 (first manual smoke,
  killed, freed); diag runs pids 22184 / 13408 / 21308 / 12172 / 21900
  (port 8140; the wrapper-killed runs' children were killed manually in a
  follow-up command with port-freed verification); Node-diag runs pid 20204
  (port 8140) and pid 22640 (port 8142) with in-script cleanup + freed
  verification; scene-mode headless verification server pid 21844 (port 8143,
  in-script cleanup + freed verification).
- ONE orphan honestly recorded: pid 6620 (port 8140, parent already dead)
  was left behind by a host-wrapper-interrupted diagnostic invocation; it was
  IDENTIFIED (command line = compat\server-sceneir.mjs) and STOPPED with
  port-freed re-verification BEFORE phase end. At phase end NO
  server-sceneir.mjs process is listening on 8140/8141/8142/8264 (verified
  twice: process census + port probes); the server is deliberately NOT
  running at handoff (PE-MASTER starts it per SMOKE_CHECKLIST.md).
- No foreign process was started, replaced or stopped: the user's legacy
  node servers (ports 8000/8124/8126/8132 class), the user's Edge sessions,
  and the host tooling (Codex runtime, Playwright MCP) were never touched;
  every kill in this phase was verified by command line to be an own PID.
- Inputs READ_ONLY: the pinned Models.bnt (SHA re-verified on every server
  start), the canonical checkout's pinned three 0.185.0 package (version
  verified at every start), and the worktree's own files. No original file
  was modified.

### INT-4 — HEADLESS_BROWSER_EXECUTIONS (real browser, dedicated temp profiles)
- Class: HEADLESS_BROWSER_EXECUTION — `msedge.exe` (real Edge binary,
  C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe) was executed
  headless (`--headless=new --dump-dom --virtual-time-budget=30000/45000
  --disable-extensions --no-first-run`) against the app URL, ALWAYS with a
  DEDICATED temp `--user-data-dir` under
  C:\Users\User\AppData\Local\Temp\opencode — the user's Edge profiles and
  running browser sessions were never touched (verified: no msedge process
  matching the temp profiles remains; the user's own msedge processes were
  identified and left alone).
- Executions: formal T9 (harness run 1: exit 0, DOM dump at boot-PENDING —
  the honest intermediate that led to the missing-boot() repair; harness
  run 2 FINAL: exit 0, elapsed 1188 ms, DOM 21064 B, data-load-status=READY,
  server pid 12404 / port 8141, both stopped+freed) plus diagnostic
  executions during the PENDING→READY investigation (all exited 0 or were
  killed via `taskkill /T /F` on their own PID tree; none left running).
- The captured DOM evidence (raw/HEADLESS_DOM_DUMP.html) is the app's own
  rendered DOM (canvas + diagnostics + authored labels) — not a proprietary
  asset screenshot; no screenshots were taken (private screenshots: none).
- One targeted repair pass (documented in TEST_RESULTS_APP.json
  honest_notes + APP_AND_SERVER_NOTES.md §7): (1) T8 authored2.asset crash
  fix; (2) the missing boot() invocation (request-log-proven; fixed; the
  honest PENDING intermediate is preserved in run-1 evidence); (3) a
  PowerShell Set-Content round-trip double-encoded four compat/*.js files —
  reversed byte-accurately and normalized to ASCII, re-measured green.

### Other interventions this phase: NONE
- Git: NO add/commit/push in this phase (publication is a later, separately
  assigned phase; the dispatch says No commit/push yet). Worktree writes
  ONLY in the allowed areas: compat/**, tests/pecompat/** (additions),
  package.json (scripts entry only — documented), REPORT_REPO_PATH/**,
  .opencode/skills/pe-gamebryo-rosetta/**. src/pesource/ untouched
  (witness hash re-verified by the phase-2 T6-style regression at BASE —
  the file was never opened for writing; git diff confirms).
- Server left running at phase end: NO (verified; PE-MASTER starts it per
  SMOKE_CHECKLIST.md).
- No client execution, no new EXE bodies, no corpus expansion, no new Ark
  tail semantics, no VM access, no network beyond 127.0.0.1.
