# NIGHT ORDER #2 — THE ITEM #2 LIVE-TEST RECORD (BLOCKED, the exhaustive negative)

**RUN:** PE_M1_X87CW_AUTOMATION_R1_20260905_140126 (continued per the order; append-only)
**ITEM:** #2 LIVE TEST WITHOUT DEBUGGER (the gate before any measurement)
**VERDICT:** **BLOCKED after the 3-iteration ladder** — the client cannot reach
a live state on THIS machine (the diagnosis corpus recorded below). Items #3
and #4 are consequently DEFERRED (both need a live client). Per the order:
"potem honest BLOCKED + exhaustive negative i przejdź do #4" — #4's design
inputs are recorded; its EXECUTION is blocked with #2.

## THE REPAIR LADDER (3 iterations, all recorded)

**Iteration 1 — THE SANDBOX REPAIR (item #1, DONE):**
- mac3r.dll copied to wd\ (143,360 B, SHA256 C53AD78F52E4C5C2F101811DC89555CF8F28DAF13ADCDBE63646C7BA01CB33E8;
  the provenance: D:\Entropia Universe\mac3r.dll — the PE-MASTER-verified source;
  identical copies exist at 01_Original_Files\EntropiaUniverse_Runtime\DLLs\PE_Specific\
  + the TMF1 dynamic sandbox).
- MSVCR80.dll: NOT copied (correctly): the ProcMon trace PROVES the resolution
  via the exe's embedded VC80.CRT manifest + WinSxS
  (x86_microsoft.vc80.crt_1fc8b3b9a1e18e3b_8.0.50727.9680 — the CreateFile
  rows in the trace; the local-copy refusal = the documented SxS behavior).
- d3dx9_30.dll: NOT copied (correctly): resolved from C:\Windows\SysWOW64
  (d3dx9_24..31 present; the trace shows SysWOW64\d3dx9_30.dll Load Image SUCCESS).
- The import-table walk of mac3r.dll: WS2_32, RPCRT4, KERNEL32, ADVAPI32, ole32
  — ALL system-resolvable. **THE IMPORT SET CLOSED** (the walk, not a dir diff —
  the QC lesson applied).
- RESULT: the death class CHANGED: 0xC0000135 (loader DLL death) → **-1
  (0xFFFFFFFF) at ~40ms** — the imports now ALL load (the trace: stlport,
  wmvcore, binkw32, ijl15, dpvs, NxCooking, PhysXLoader, wmasf, mac3r, d3dx9_30
  Load Image SUCCESS).

**Iteration 2 — THE LAUNCH ARGS (refuted):** ClientLoader's strings show the
loader passes -col32/-col16. Entropia.exe -col32 → DEAD at 10s, exit -1 (no change).

**Iteration 3 — THE COMPATIBILITY LAYER (refuted):** HKCU AppCompatFlags\Layers
per-exe entry WINXPSP2 (a bounded, reversible, user-level, sandbox-path-specific
key) → DEAD at 10s, exit -1 (no change). (The registry entry remains set for
the sandbox path; harmless.)

## THE DIAGNOSIS CORPUS (the ProcMon trace, 2193 Entropia rows; the CSV+PML kept
LOCAL-ONLY: 04_RUNTIME\live_test\entropia_death_trace.csv [50,053,186 B] + .pml)

- The full timeline: the imports load → the CRT init → **the client's WinMain
  starts** (the log rotation attempt: CreateFile wd\Entropia.log with the DELETE
  disposition, NAME NOT FOUND — no old log; the new log NEVER created) → the
  WinSock registry init → **the display enumeration begins
  (HKLM\HARDWARE\DEVICEMAP\VIDEO; Device\Video1 queried SUCCESS)** →
  QueryNameInformationFile(sandbox dir) → the thread exits → **Process Exit
  -1** (User Time 0.0 — microseconds of client code ran).
- NO WER, NO crash dialog, NO client log, NO network ops (zero TCP/UDP/DNS by
  the client), NO MindArk registry reads, NO pcg_install reads.
- **The machine datum: the display adapters = "Microsoft Hyper-V Video" +
  "Microsoft Remote Display Adapter" (DriverVersion 10.0.22621.x)** — this is
  a Microsoft eval VM (the hostname WinDev2407Eval). The death correlates with
  the display-adapter data processing: the client's own early display/GPU
  validation path fails on the virtual adapter (the exact check is not in the
  static canon — recorded as a canon gap, NOT speculated further).

## THE REFUTED HYPOTHESES (the exhaustive negative)

| # | Hypothesis | The refutation evidence |
|---|---|---|
| 1 | The missing imports | FIXED (iteration 1); the death class moved |
| 2 | MSVCR80/SxS failure | REFUTED: the WinSxS msvcr80 loads SUCCESS in the trace |
| 3 | mac3r = a mixed-mode .NET DLL needing the 2.0 CLR | REFUTED STRUCTURALLY: NO COM descriptor (rva=0, size=0); the ".NET Runtime" string = the static CRT boilerplate; the NetFx3 state (DisabledWithPayloadRemoved) = irrelevant |
| 4 | The registry config absent | REFUTED: the client never reads MindArk keys before death (the keys exist anyway: HKLM\...\MindArk\Project Entropia (default)=pcg_install) |
| 5 | The missing launch args | REFUTED (iteration 2: -col32 = no change) |
| 6 | The OS-version check | REFUTED (iteration 3: WINXPSP2 compat = no change) |
| 7 | The network dependence | REFUTED: zero network ops before the death |
| 8 | The loader-phase death | REFUTED: the client code RUNS (the log rotation + the display enumeration = the WinMain phase) |

**THE REMAINING BLOCKER (honest):** the client's own early display/GPU
validation on the VM's virtual adapters (the Hyper-V Video / the Remote
Display Adapter). The fix candidates beyond this machine: a physical-GPU
machine, a GPU-paravirtualization change, or the static identification of
the exact check (a NEW Ghidra analysis = a next-design input, NOT in the
existing canon).

## THE CONSEQUENCES + THE NEXT-DESIGN INPUTS

- **#3 (the x87 CW measurement): DEFERRED** — needs the live client. The
  harness v3 pre-work recorded: (a) never overwrite the session close marker
  (the F-B4 sub-bug); (b) decode + prominently record every exit code; (c) the
  in-session process-liveness check (never spin on a dead PID); (d) the DR7
  2-site fallback re-arm fix (the fallback disarm currently kills both sites).
- **#4 (the login-phase FPU probe): DEFERRED** — needs the live client; the
  design input = the 9.3.5 D3D9 callsites are NOT in the existing static canon
  (the D3D8 canon = the PE2-era binary) → the probe-address identification =
  a new static run (the next-design input).
- **#5 (georef/P-DATUM): the parallel-session check DONE** — the parallel
  session executed the WITNESS-MATRIX MAP (8c037c0) + the falsification
  execution (59b5b63, with the MILD-2 refutation ledger entry bd6d86b) + the
  census revalidation (16c551b) tonight — NOT duplicated by this session. The
  georef/P-DATUM was NOT started by them; my offline design = DEFERRED to the
  next session (the night context exhausted — recorded honestly, no silent
  scope drop).

## THE NIGHT'S PROVEN-FACTS LEDGER (the additions)

- FACT7: the 9.3.5 client's full static import set resolves on this machine
  (mac3r local + MSVCR80 via WinSxS-manifest + d3dx9_30 via SysWOW64 + the
  rest) — the loader phase is NOT a blocker anymore.
- FACT8: the 9.3.5 client's WinMain begins (~40ms: the log rotation → the
  display enumeration) and exits -1 BEFORE: any log write, any network op,
  any MindArk registry read, any d3d9 LoadLibrary.
- FACT9: the death correlates with the display-adapter processing on a
  Hyper-V/Remote-Display VM; refuted: the args, the OS-version compat, the
  .NET hypothesis, the registry config.

## THE ARTIFACT MAP (LOCAL unless noted)

- 04_RUNTIME\live_test\live_test_record.json (the #2 monitor record)
- 04_RUNTIME\live_test\entropia_death_trace.pml (50MB) + .csv (50MB) — LOCAL-ONLY
  (identity: SHA256 recorded in the artifact index; not committed)
- 00_CONTROL\live_test.py + trace_wd_network.py + trace_decision_window.py +
  trace_client_own_reads.py (the analysis scripts)
- The sandbox deltas: wd\mac3r.dll (the provenance recorded); the verify_sandbox.py
  CONTINUATION_NIGHT note (the 20→21-check census change).
- The git: ONE path-limited commit (this record + the analysis scripts + the
  live-test record + the index delta) — the night's one-commit-per-package rule.
