# RETRACTED_MEASUREMENT_VERDICT — the corrective append (NIGHT ORDER #2, item #0)

**THE RETRACTED CLAIM** (from 06_REPORT\00_FINAL_REPORT.md, commit f0906b9):
"Attempt 1/2: the client ran the full window CLEANLY ... 0 hits at BOTH sites ...
the honest verdict: OPEN-BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW (the
world-load gating)."

**WHY RETRACTED (falsified by the run's own artifacts):**
- target_exit_code (both attempts) = 3221225781 = **0xC0000135 STATUS_DLL_NOT_FOUND**
  — the client DIED in the loader phase ~20 ms post spawn.
- target_exit_recorded = **True** in BOTH raw session records — the EXIT_PROCESS
  debug event DID arrive; the harness v2 timeout branch then OVERWROTE
  window_closed_by to "timeout_no_events", and the report misread that as
  "the client ran the full window". The session was a spin on a dead process.
- The cause: the sandbox wd\ was missing **three** statically imported DLLs
  (the import-table walk, recorded in the run's control evidence):
  **mac3r.dll, MSVCR80.dll, d3dx9_30.dll** (the pcg_install root never contained
  them; the sandbox exclusion set covered only the installers — the SOURCE itself
  lacks these three; the real install D:\Entropia Universe\ provides them).

**WHAT STANDS:** Backend E (the Win32 harness) QUALIFIED_10_10 (the notepad
qualification is untouched by this defect — a synthetic target with a closed
import set). The six empirical facts of the diag series stand. The runtime
base confirmation (0x00400000, no relocation) stands (recorded at
CREATE_PROCESS before the death). The init-CW datum 0x027F stands as the
W2.3 comparison datum.

**WHAT IS UNMEASURED:** the entire site question (the world-load gating
hypothesis included) — pending a LIVE client (the sandbox repair, item #1).

**THE QC LESSONS (recorded for the standing discipline):**
1. Decode every status/exit code BEFORE interpreting a session (0xC0000135
   was in the artifact and was passed over).
2. Never overwrite the session's close marker (target_exit must be terminal).
3. Close the WHOLE import set when building a runtime sandbox (an import-table
   walk, not a directory diff).

Issued by PE-MASTER night audit 2026-09-05; the corrective append by
pe-master-auditor per NIGHT ORDER #2 item #0. The f0906b9 history NOT rewritten.
