# INTERVENTION_LEDGER — PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009

**This ledger is APPEND-ONLY.** Later phases (SDK qualification, native SDK controls,
DLL PATH exposure, PE native execution, scene inspection) append their own entries
here. Nothing already recorded may be edited or removed.

## Entry 1 — Phase 1: PREFLIGHT ARTIFACTS + WORK PACKAGE A (records correction)

**Date:** 2026-10-09 (executed 19:20Z–20:10Z UTC)

**RUNTIME INTERVENTIONS THIS PHASE: NONE.**

This phase was records work only. Specifically:

- The PE client was **never executed** (PCG_CLIENT_EXECUTION = NO for this phase).
- **No new EXE function bodies were opened** (NEW_PCG_EXE_FUNCTION_BODIES = 0). The
  only Entropia.exe accesses were: whole-file hashing; re-hashing the five
  ALREADY-PUBLISHED window slices (105 + 140 + 4 + 4 B code + 16 B anchor data —
  the exact slices the f99febe package had already opened and published); and byte
  spot-checks strictly INSIDE those same two open windows. The closed bodies
  0x008BD720 (beyond its published 16 B data dump), 0x006C2E00, 0x0085B1B0 and
  0x0095D3C4 were never opened.
- **No native execution of any SDK tool or DLL** — SceneGraphPrinter.exe, MSVCP71.DLL,
  MSVCR71.DLL, gb12_oracle.exe were only hashed (identity metadata). **DLL PATH
  exposure classes and any native execution belong to LATER phases and will be
  recorded HERE when they occur** (child-process PATH only, per contract section 6).
- No Models.bnt parsing, no NIF extraction, no PE asset execution (Package C is a
  later phase).
- No SDK tree, tool, profile, OpenMW fork, Three.js app, original game file, or
  historical audit package was modified. The historical f99febe package was READ_ONLY
  (22/22 manifest rows re-verified MATCH after this phase's reads — byte-unchanged).
- No AUDIT_ENTRYPOINT.md edit (later phase). No commit, no push, no git history
  operation.
- Countermodel executions: five locally authored Python scripts run with `python -B`
  on this machine (no network, no binaries instrumented, no packages installed);
  zero `__pycache__` residue (verified).
- Tooling disclosure (honest): the first attempt at in-memory slice hashing in a
  PowerShell verification snippet returned the empty-buffer SHA256 for all five
  slices (a defect in the executor's own hashing snippet — PowerShell array
  unrolling fed an empty stream to Get-FileHash); it was replaced by a temp-file
  extraction + Get-FileHash path, which verified all 5/5 slices MATCH. One byte
  spot-check row requested 6 bytes against a 5-byte expected string (executor
  check-spec defect); the actual bytes matched the 5-byte expectation exactly. Both
  defects were in this executor's VERIFICATION tooling, caught immediately, disclosed
  here, and never fed any scientific conclusion; the underlying data was unaffected.

**Phase-1 disposition:** no interventions to declare; the records package stands on
documents + captured countermodel outputs only.

*(Later phases append below.)*

## Entry 2 — Phase: SDK_QUALIFICATION (Work Package B; contract sections 5, 6, 7)

**Date:** 2026-10-09 (executed after the phase-1 records correction)

**INTERVENTION CLASS: CHILD_PROCESS_PATH_DLL_EXPOSURE** — applied to EVERY native
execution of this phase (16 executions total; per-run argv/cwd/env-delta/raw-log
records in `01_SDK/SDK_EXECUTION_RESULTS.json` and
`01_SDK/synthetic_control_details_internal.json`):

- **What was exposed:** the directory `D:\gamebyroengine\extracted\Gb112_tools_setup`
  (containing MSVCP71.DLL df96156f…23b, 499712 B and MSVCR71.DLL 8094af5e…fefe,
  348160 B) was PREPENDED to the PATH of each child process only. The parent
  environment (this executor's shell, the machine) was NOT modified: no global PATH
  change, no installer, no file association, no registry change, no SDK-original
  patch, no persistent environment change of any kind.
- **Effective resolution recorded (measured):** the pinned printer
  SceneGraphPrinter.exe (fd693af2…41c7c) imports MSVCP71.dll and MSVCR71.dll
  (ASCII import strings present in the executable image), and NEITHER DLL exists
  in C:\Windows\System32 or C:\Windows\SysWOW64 → the child-PATH prepend is the
  effective resolution mechanism for both DLLs in every run. No other environment
  variable was changed for the children.
- **Executions covered by this class (all headless, `CREATE_NO_WINDOW`):**
  - `probe_sdk_tools_r1.py` (adapted Desktop reused code, lineage in
    SOURCE_AND_BUILD_IDENTITIES.json): 4 positive SDK controls (DT.NIF,
    DT_Ground.NIF, WORLD.nif, OBJECT.NIF — all flags
    `-trans -extra -prop -geom -bs -mem`), 4 negative mutated LOCAL_ONLY copies of
    OBJECT.NIF (unknown class / user version 1 / version 20.2.0.7 / bad header
    text), 1 missing-file case, 1 own synthetic empty scene. 10 runs.
  - `probe_native_transforms_r1.py` (adapted Desktop reused code): 6 synthetic NIF
    10.1.0.0 transform controls, flags `-trans -bs -mem`. 6 runs.
- **Operational controls (not environment changes):** per-process timeout 30 s
  (hang detection; never triggered — no run timed out); launcher
  SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOOPENFILEERRORBOX|SEM_NOGPFAULTERRORBOX)
  on the Python launcher process (inherited by children) to keep failures headless
  (no crash-dialog GUI); cwd of every child = the LOCAL_ONLY fixtures directory
  (writable); raw stdout/stderr captured per run under `01_SDK/raw/`.
- **Verified NON-mutation:** after all 16 executions the printer exe, both DLLs and
  all four SDK sample inputs were re-hashed UNCHANGED (7/7 identities, verified by
  an independent process outside the probe scripts). The SDK trees, Desktop frozen
  directories and historical run directories were READ_ONLY throughout; all
  mutated fixtures were created as fresh copies under this run's LOCAL_ONLY_ROOT
  (`D:\Eudoria_Reconstruction\99_Audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\01_SDK_fixtures\`).
- **No PE client execution, no PE asset access, no new EXE bodies, no GUI tools,
  no commit/push, no AUDIT_ENTRYPOINT edit in this phase.**

**Phase-2 disposition:** all native executions are accounted for by this single
exposure class; no other interventions occurred. One executor tooling defect
disclosed: the first execution of `probe_native_transforms_r1.py` failed with
FileNotFoundError because the script did not create its synthetic fixtures
subdirectory; the directory-creation line was added and the probe re-run — no
scientific result was affected (the failing run produced no fixture and no printer
execution; the preregistration predates all successful runs and is unchanged).

*(Later phases append below.)*

## Entry 3 — Phase: 02_PE PE INPUT CENSUS, MECHANICAL SELECTION, NATIVE PE EXECUTION AND SCENE INSPECTION (Work Package C; contract sections 8–14)

**Date:** 2026-10-09 (executed after the SDK qualification phase; preregistration 02_PE/PREREGISTRATION_PE_PHASE.md written BEFORE the census/selection/native runs)

### 3a. Native PE executions on the stock printer

**INTERVENTION CLASS: CHILD_PROCESS_PATH_DLL_EXPOSURE** (same class as
Package B, entry 2) — applied to EVERY native execution of this phase (4
executions total; per-run argv/cwd/env-delta/input-SHA/exe-SHA/exit/raw-log
records in `02_PE/NATIVE_EXECUTION_RESULTS.json`):

- **What was exposed:** `D:\gamebyroengine\extracted\Gb112_tools_setup`
  (MSVCP71.DLL df96156f…23b / MSVCR71.DLL 8094af5e…fefe) prepended to each
  child process PATH only; no global PATH/registry/installer/association
  change; no SDK-original or game-original modification.
- **Executions covered (all headless, CREATE_NO_WINDOW, 30 s per-process
  timeout, never triggered):** the qualified stock printer
  SceneGraphPrinter.exe (fd693af2…41c7c, identity re-verified unchanged
  BEFORE and AFTER all runs) with flags `-trans -extra -prop -geom -bs -mem`
  on the four fresh LOCAL_ONLY extractions (218757.nif, 496633.nif,
  512126.nif, 423020.nif; container Models.bnt identity re-verified
  C950A8C2…BEE0 before and after; payload copies re-hashed unchanged after
  the runs). All four: exit 1, `Error loading stream.` on stderr, stdout
  empty → recorded NATIVE_LOAD_REJECTED (populated-scene rule applied; exit 0
  alone never sufficient — not applicable here since none exited 0).

### 3b. The ONE optional native helper (contract section 11)

**INTERVENTION CLASS: CUSTOM_SDK_SOURCE_HELPER_EXECUTION** — the EXISTING
custom gb12_oracle.exe (dd7112a4…046c, 594944 B, identity re-verified against
the contract pin; source oracle.cpp AD1F5DED…E591A inspected BEFORE
invocation; NOT the unmodified vendor printer; NOT newly built this run).
7 executions total (CREATE_NO_WINDOW, 60 s per-process timeout, never
triggered; per-run records in `02_PE/NATIVE_HELPER_RESULTS.json`):

- 3 QUALIFICATION CONTROLS first (all PASS): SDK positive OBJECT.NIF
  (exit 0, 60 blocks, 2 top objects), missing-factory control
  SYNTH_UNKNOWN_CLASS.nif (exit 1, SPECIFIC lastErrorMessage
  `QzNode: cannot find create function.` — the exact capability the stock
  printer lacks), empty-scene control (exit 0, 0/0).
- 4 PE payload runs: all exit 1, load FAIL, observed native lastError=5
  (NO_CREATE_FUNCTION), lastErrorMessage
  `NiArkAnimationExtraData: cannot find create function.` for all four.
- **Behavior differences from the unmodified printer DISCLOSED in
  NATIVE_HELPER_RESULTS.json** (6 items; among them: prints the SPECIFIC
  NiStream last error the stock printer never calls; tree-dump Update(0,false)
  skips controllers while the stock printer runs them; OracleStream snapshot
  hook via the PUBLIC RegisterPostProcessFunction — zero engine changes; no
  NiArk loaders, no dummy factories).
- The helper qualifies as the contract's AT MOST ONE helper; its observed
  error is labeled as its own native-execution subclass in
  02_PE/PARSER_NATIVE_COMPARISON.json, always separate from
  SOURCE_PREDICTED results.

### 3c. Non-native tooling (disclosure, no exposure class)

- gamebryo_oracle COPY executions (TOOLS/gamebryo_oracle_r1; canonical
  tools/gamebryo_oracle READ_ONLY, byte-identical per-file copies recorded in
  02_PE/ORACLE_RUN_PROVENANCE.json): pure Python, no DLL exposure, no
  environment change. Two full-decode runs initially exceeded the runner's
  300 s operational bound (recorded as measured events); both were rerun
  with longer operational bounds (496633: 1011 s, 423020: 210 s) and
  completed — the rerun records are in ORACLE_RUN_PROVENANCE.json
  (long_bounded_full_decode_reruns).
- Corpus census + selection (Python; documented s01 walker COPY —
  byte-identical, negative-control battery 4/4 — plus s02/s03-lineage
  adapted copies; all outputs under this run's paths). One 218757
  Rosetta-lineage s2 parse COPY (canonical s2 READ_ONLY in the historical
  placement-search package; only output paths redirected; output LOCAL_ONLY).
- No PE client execution, no GUI tools, no new EXE bodies, no NIF
  version/user-version alteration, no block removal, no class replacement,
  no guessed-length padding, no Load-failure suppression, no NifConvert, no
  convert/save of originals, no commit/push, no AUDIT_ENTRYPOINT edit in
  this phase.

### 3d. Executor tooling defects (disclosed; none fed a scientific conclusion)

1. First census execution had a 4-byte shift in the 10.1 header scan
   (parse_header_line returned the position AT the version u32 while the
   s03-lineage scan expects to start at the user-version field) — 5,595
   E_TYPE_SCAN failures; caught from the failure reasons, fixed, re-run
   before ANY use of the outputs; the wrong intermediate CSV/JSON were
   deleted and regenerated.
2. A transcription defect in probe_gb12_oracle_r1.py (the oracle.cpp SHA
   constant mistyped with a leading extra character) aborted that script's
   first execution BEFORE any helper invocation; fixed and re-run.
3. Two geometry-extraction cursor bugs in s17 (f32 not advancing; int-vs-str
   dict key in the cross-check) produced vacuous EXTRACTION_FAILED /
   empty-cross-check states; caught by the built-in validation (bound
   center/radius + counts vs BOTH parsers' measured values), fixed, re-run —
   final extraction 14/14 + 102/102 EXTRACTED_VALIDATED.
4. An inline Python quoting failure and a harness-blocked background
   Start-Process attempt produced no process and no scientific output;
   replaced by synchronous bounded runs.

**Phase-3 disposition:** all native executions accounted for by 3a/3b; all
selection, census and analysis scripts are this run's own copies with
redirected outputs; originals untouched (Models.bnt, SDK trees, canonical
tools, historical packages all re-hashed unchanged after the phase).

*(Later phases append below.)*
