# FINAL_REPORT — PE_M1_X87CW_AUTOMATION_R1_20260905_140126
# (AUTOMATION_FEASIBILITY per the PE-MASTER order; the manual-operator path REVOKED
#  by the human decision; backends B→D bake-off + the qualification + the measurement)

**RUN_CLASS:** the automation feasibility bake-off + the qualified measurement
attempts. ZERO human labor used (HUMAN-LABOR-LAST-RESORT honored: the machine did it).
**AUTHORIZATION:** the PE-MASTER AUTOMATION_FEASIBILITY order (relayed by the human
2026-09-05; the prompt-with-3-deltas) + the standing HUMAN GO RUNTIME for the x87 CW
kit execution.

## THE ONE P0 ANSWER

**TAK — pomiar CW jest dostępny programowo** (Backend E: the Win32 Debug API
harness, QUALIFIED_10_10), **ale łańcuch foliage nie wykonuje się w fazie login**
(attempts 1+2: 0 hits at both the instruction sites AND the chain entries) →
the honest verdict: **OPEN-BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW** —
the chain requires the world-load phase (the design's own anticipated W4.4/W3.7
class; a next-design input, not a failure).

## THE BAKE-OFF (B→D + E/F per the order's ladder) — the verdicts with causes

| Backend | Verdict | The empirical cause |
|---|---|---|
| B: x64dbg-mcp (MCP) | **BLOCKED** | The repo (SetsunaYukiOvO/x64dbg-mcp, 455 stars) requires BUILDING: VS2022 C++ + CMake 3.15+ + vcpkg; NO prebuilt x86 `.dp32` ships (probed: the README + the repo tree). This host: cl/gcc/clang/mingw32-gcc/cc ALL NOT FOUND; cmake NOT FOUND; msbuild NOT FOUND; C:\vcpkg absent; C:\Program Files\CMake absent. The full toolchain install = a heavy environment change (human-gated, outside a bounded run). |
| C: the x32dbg plugin SDK | **BLOCKED** | No C++ compiler on PATH (the same probe). A plugin needs compiling. |
| D: x32dbg built-in scripting | **INSUFFICIENT (headless)** | The scripting language EXISTS (the in-tree evidence: `try3_script.txt` = log/run — a prior session's script) but (i) NO headless/autorun channel in this build's ini surface (probed: no autorun key; the script actions = GUI hotkeys Ctrl+O/Space; the `headless\headless.ini` = a prior config experiment, not an autorun mechanism), (ii) the FPU CW expression operand = undocumented/unproven in the script expression system. In-GUI scripting still requires a human at the GUI = HUMAN-ONLY → violates DEBUGGER-AUTOMATION-FIRST. |
| **E: the Win32 Debug API harness** | **QUALIFIED_10_10** | BUILT + QUALIFIED in this run (Python 3.12 ctypes, headless, zero GUI, zero target-code execution, zero code patches). The qualification: 10/10 spawn-cycles against C:\Windows\SysWOW64\notepad.exe — each cycle: the DR hardware-execute breakpoint at (loaded_base+entry), the trap fired, the CW read from CONTEXT_FLOATING_SAVE_AREA (cw=0x027F, PC=53-bit double, RC=nearest-even), the clean termination + the exit proof + zero orphans. |

### The empirical facts learned building E (the diag1-4 series; the recorded lessons)

1. **FACT1** — the 32-bit CW/EIP read from the 64-bit host MUST use
   `Wow64GetThreadContext` with the 32-bit CONTEXT layout (the plain
   GetThreadContext = ERROR_NOACCESS 998 / zeroed data).
2. **FACT2** — the DR register write on a WOW64 thread MUST use the 64-bit
   CONTEXT route (`GetThreadContext`/`SetThreadContext` with CONTEXT_AMD64 |
   CONTEXT_DEBUG_REGISTERS); the WOW64 32-bit set silently ignores the DR group
   (empirically: the write "succeeded", the readback = zeros; the x64 route:
   the readback Dr0 matches).
3. **FACT3** — the DR trap delivery under WOW64 was observed with VARYING
   exception codes (0x80000004 AND 0x4000001e) — **the hit discriminator must be
   the ADDRESS (ExceptionAddress/EIP == the armed VA), never the exception code.**
4. **FACT4** — arming at the initial breakpoint has a timing race (one run trapped,
   the next did not); **arming at CREATE_PROCESS (the earliest, the event's own
   hThread) = deterministic.**
5. **FACT5** — after a hit, continuing without RF+DR6-clear re-traps the same
   instruction (the observed storm); the fix = set EFlags|RF (verified by
   readback) + clear DR6.
6. **FACT6** — after TerminateProcess the debug port holds the process until the
   debugger drains the EXIT_PROCESS event (the observed 10s hang + the
   process_gone=False) → the post-terminate event drain (bounded 5s) = the
   clean exit proof.
7. **ASLR discipline** — the synthetic target WAS relocated (the file base
   0x400000 → the loaded base 0x00EE0000): the bp VA must come from
   CREATE_PROCESS_DEBUG_EVENT.lpBaseOfImage + the entry RVA (never the file base).

## THE MEASUREMENT (the qualified backend E; the design's W3 sites; 300s windows)

### Attempt 1 — the instruction sites (DR0=0x0098CE5A, DR1=0x0095B2BC)
- The sandbox pre-verify: PASS 20/20 (the fail-closed gate honored before launch).
- **The runtime module base = 0x00400000, NO relocation** (the canon's
  image-base claim CONFIRMED LIVE; the debug-event start address 0x0095DA11 —
  the 0x0095xxxx region consistent with the canon layout).
- **The aux init-CW read (the design's W2.3 comparison datum): 0x027F**
  (PC=53-bit double, RC=nearest-even, all exceptions masked).
- The client ran the full window CLEANLY (the exception census: ONLY the initial
  breakpoint; no other exceptions), **spawned NO children**, zero orphans, the
  clean exit proof. **0 hits at BOTH sites** (the FDIV/rand01 site included →
  rand01 is not consumed in the login phase either).
- window_closed_by = timeout_no_events (the bounded 300s window; per §14:
  NOT_OBSERVED_IN_CAPTURE ≠ never-reaches).

### Attempt 2 — the chain-entry fallbacks (DR0=0x0095B180, DR1=0x0098FE00)
- A fresh spawn (the design's W3.7 ladder; the attempt-1 evidence stands).
- The identical clean profile: the init CW 0x027F again, the base 0x400000 again,
  zero children, zero orphans, the clean exit. **0 hits at BOTH fallbacks.**

### The honest verdict (the design's exact strings; NO silent pass)

**OPEN-BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW** — the foliage chain (both the
instruction sites and the chain entries) does not execute in the client's
login/connect phase within the bounded windows; the chain requires the
world-load phase (the game-state condition the design itself anticipated at
W3.7 Attempt-3). The init-CW datum (0x027F, PC=53) is recorded as the W2.3
COMPARISON DATUM ONLY — it is NOT the site measurement and closes NOTHING.

## THE NEXT-DESIGN PROPOSALS (separate designs; NOT executed here)

1. **The login-phase FPU-state probe (bounded, reachable):** a DR breakpoint at
   a hot login-phase render/message-loop address (a login-phase executing site)
   → the CW read there. This would measure the FPU state AFTER the login UI's
   D3D8 device creation — directly testing the canon-flagged candidate mechanism
   (D3D8 FPU-mode change without D3DCREATE_FPU_PRESERVE) on the LIVE build.
   Combined with the chain-level no-FLDCW fact, it would TIGHTEN (but not
   site-measure) the foliage-chain CW answer. A new design + a PE-MASTER review.
2. **The world-load path (out of M1 scope):** reaching the world-load requires
   the login-server path (the server emulation = the M7-class track) — recorded
   as the structural blocker for any site-local foliage measurement.

## WHAT THIS RUN DID **NOT** DO

- NO manual GUI session (the revoked path; zero human labor used).
- NO target-code execution (the harness reads contexts only; the single
  disclosed deviation class — FSTCW — was NEVER needed: the context read
  delivers the CW directly).
- NO code patches, NO memory writes, NO Frida, NO injection.
- The original pcg_install NEVER launched (the sandbox copy only; the pre-verify
  PASS recorded before every launch).
- NO payloads committed (the sandbox + the client = local-only).

## THE HANDOFF BLOCK

```text
AUDIT_OUTPUT_ROOT      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126
FINAL_REPORT_PATH      = <ROOT>\06_REPORT\00_FINAL_REPORT.md (this file)
PRIMARY_EVIDENCE_PATHS = <ROOT>\00_CONTROL\x87cw_harness.py + x87cw_harness_v2.py
                          + diag_one_cycle.py + diag2_dr_route.py + diag3_entry_timing.py
                          + diag4_control_and_bytes.py (the empirical fact series)
                          + 04_RUNTIME\qualification_notepad_v2\ (the 10/10 record)
                          + 04_RUNTIME\measurement_attempt1\ + measurement_attempt2\
                          (the raw session records + the empty cw_capture.jsonl
                          + the harness_session.json each)
BASE_SHA / HEAD_SHA    = 0e64dec... / <filled at commit>   PUSH_STATUS = <filled>
RUN_STATUS             = AUTOMATION_QUALIFIED_10_10 + MEASUREMENT_OPEN-BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW
HARD_STOP_REASON       = NONE (the ladder exhausted honestly per W3.7; the item stays OPEN)
NEXT GATE              = the PE-MASTER review: the next-design choice
                          (the login-phase FPU probe vs accepting the item OPEN
                          until the server track exists) -> the human decision
INTERVENTION_LEDGER    = OBSERVATION-ONLY (DR registers + the context reads;
                          zero target-code execution, zero patches, zero writes)
```
