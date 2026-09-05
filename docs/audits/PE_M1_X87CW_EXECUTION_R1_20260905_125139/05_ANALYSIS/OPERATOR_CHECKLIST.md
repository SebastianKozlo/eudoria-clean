# OPERATOR_CHECKLIST — the MANUAL x87 CW measurement session
# PE_M1_X87CW_EXECUTION_R1_20260905_125139 | composed from the APPROVED design
# (EXPERIMENT_DESIGN.md, SHA 56D6101D44FED255..., PE-MASTER DESIGN APPROVED +
# the human GO RUNTIME relayed 2026-09-05). YOU (the human operator) execute this
# in ONE x32dbg GUI session. Bounded window: 30 minutes. Print this file or keep
# it open beside the debugger.

## PRE-FLIGHT (before opening x32dbg; ~3 min)

- [ ] P1. Run the fail-closed sandbox verify:
      `python D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\00_CONTROL\verify_sandbox.py`
      **MUST print "verdict": "PASS"** (exit 0). ANY mismatch => STOP — do NOT launch
      anything (the W4.7 abort class; report the record).
- [ ] P2. Confirm the 30-minute wall-clock window start (you will record the window
      actually used in SESSION_LOG).
- [ ] P3. Open (do not launch yet): `...\04_RUNTIME\cw_capture.jsonl` (you will append
      one JSON line per hit) + `...\04_RUNTIME\SESSION_LOG.txt` (you fill the header
      + every step marked [SL]).
- [ ] P4. Screenshot destination: `...\04_RUNTIME\screenshots\` (one per hit:
      `hit_<nn>_<site-short>.png`).

## THE SPAWN (design W3.2, step 6-7)

- [ ] S1. Launch the debugger WITH the working-directory context:
      open a terminal in `...\04_RUNTIME\sandbox\wd\` and run
      `..\x32dbg\x32\x32dbg.exe Entropia.exe`
      (or drag Entropia.exe from the wd onto x32dbg.exe). The debuggee spawns PAUSED
      at the initial system breakpoint.
      [SL] Record: the debuggee PID (the x32dbg title/status bar), the time.
- [ ] S2. **Module-base check** (Memory Map): find the Entropia.exe module base.
      - If base == **0x00400000** → use the canon VAs verbatim (below).
      - If different → delta = actual_base − 0x00400000; add delta to EVERY VA below.
      [SL] Record: the observed base + your delta decision.
- [ ] S3. **Auxiliary read C (the init CW):** press F9 (run to the module entry
      breakpoint). View → FPU: read the Control Word. Write ONE JSONL line:
      `{"hit_index": 0, "attempt": 1, "site": "PROCESS_ENTRY", "bp_va": "aux",
      "eip": "<entry>", "pid": <PID>, "cw_hex": "0x....", "pc_bits": "..",
      "pc_decoded": "...", "rc_bits": "..", "rc_decoded": "...",
      "exception_masks_bits": "......", "cw_full_binary": "................",
      "capture_method": "fpu_panel", "screenshot": "hit_00_entry.png",
      "timestamp": "<ISO>"}` + one screenshot.

## THE BREAKPOINTS (design W3.3, step 8-9) — place BEFORE running on

- [ ] B1. **BP1 = 0x0098CE5A** — HARDWARE, on Execution (right-click the address →
      Breakpoint → Hardware → Execute). BEFORE arming: go to the address in the
      disassembler and VERIFY the bytes read **`DC 35 A8 D7 A7 00`**
      (FDIV qword ptr [0x00A7D7A8]). MISMATCH => DO NOT PROCEED (record the observed
      bytes; that is DEBUGGER_SESSION_FAILURE per W4.3 — stop and report).
- [ ] B2. **BP2 = 0x0095B2BC** — same discipline; expected bytes **`DD 05 58 C7 A8 00`**
      (FLD qword ptr [0x00A8C758]).
- [ ] B3. Conditions: NONE (unconditional — every hit is a capture event).
      BP3/BP4 (the fallbacks 0x0095B180 / 0x0098FE00) are NOT armed this attempt.
      [SL] Record: the bp addresses, the byte pre-verify results, the time.

## THE CAPTURE — N = 10 HITS PER SITE (design W3.4, steps 10-13)

- [ ] C1. Press F9 (run). At each breakpoint hit the debugger pauses; EIP = the bp VA.
- [ ] C2. At EVERY hit: View → FPU → read the Control Word (16-bit value). Fill ONE
      JSONL line (the schema from the design step 13 — copy the field set from
      S3's line; site = `FDIV_0x0098CE5A` or `FLD_0x0095B2BC`; hit_index = 1..10 per
      site; attempt = 1; eip MUST equal the bp VA). Decode helps (validator recomputes
      anyway — do your best): bits 8-9 of the CW (00=24-bit single / 10=53-bit double
      / 11=64-bit extended); bits 10-11 (00=nearest-even / 01=down / 10=up / 11=trunc);
      bits 0-5 = the exception masks; `cw_full_binary` = the 16 bits.
      - The x32dbg FPU panel typically shows the decoded fields — transcribe them +
        the hex value; the VALIDATOR will recompute and reject any inconsistency.
      - **Fallback capture (last resort only):** if the FPU panel is unreadable, use
      the command bar: `FSTCW AX` — then read AX; mark that line
      `"capture_method": "fstcw_ax_fallback"` (the disclosed register-only deviation;
      AX content changes, nothing else).
- [ ] C3. ONE screenshot per hit (F2 or your screenshot tool) → `screenshots\`.
- [ ] C4. Repeat until **10 hits at BP1 AND 10 hits at BP2** (or the window closes —
      whichever comes first; the window rule below).
- [ ] C5. **Cross-site agreement:** compare the BP1 series and the BP2 series (PC
      and RC). Disagreement or an unstable mid-series change => record it as-is
      (CW_READ_AMBIGUITY — the validator flags it; NO silent resolution).

## THE WINDOW (design W3.6 step 20 — honest bound)

The attempt closes at whichever comes first: (a) 10+10 hits captured; (b) the debuggee
reaches a steady state / exits; (c) 30 minutes from S3. NOT_OBSERVED within the window
≠ never-reaches. [SL] Record which condition closed the window + the client's observed
state at close (the login screen? the world load? etc.).

## THE SHUTDOWN (design W3.5, steps 15-17 — the §14 liveness discipline)

- [ ] D1. Save the JSONL + the screenshots.
- [ ] D2. **Terminate the debuggee FROM the debugger** (the client is a network game —
      do not leave it running).
- [ ] D3. **The independent exit proof:** run `Get-Process -Id <PID>` (or tasklist)
      → the process must be GONE. [SL] Record the command output.
- [ ] D4. **The ACTIVE_ORPHANED check:** verify NO session-spawned processes remain
      (the debuggee, x32dbg, any launcher/patcher/child processes the client spawned —
      ClientLoader/CLDLLPatcher/CLUpdater observed => each checked dead).
      [SL] Record every PID + the proof.
- [ ] D5. Close x32dbg. Fill the SESSION_LOG footer (the window used, the total hits,
      anything anomalous).

## FAILURE QUICK-MAP (design W4 — what each situation means)

| What you see | Class | What to do |
|---|---|---|
| The debuggee terminated | TARGET_PROCESS_EXIT | Need the debugger event + the OS query BOTH; keep captured lines; classify honestly |
| x32dbg hangs/crashes | CONTROLLER_FAILURE | NOT target state; kill the debuggee w/ proof; the captured lines stand as RAW |
| The spawn/bp placement fails; the bytes mismatch | DEBUGGER_SESSION_FAILURE | Record the error/bytes; do NOT proceed on a byte mismatch |
| 0 hits at window close, client provably ran | BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW | Stop attempt 1; ask pe-master-auditor for the fallback ladder (attempt 2 = BP3/BP4) |
| The CW series unstable / sites disagree / panel-vs-FSTCW disagree | CW_READ_AMBIGUITY | Record EVERYTHING; no averaging, no silent pass |
| Attach denied (only if spawn failed) | ATTACH_PERMISSION_FAILURE | Record the OS error |
| Any hash check fails | SANDBOX_HASH_MISMATCH | IMMEDIATE ABORT before launch |

## AFTER THE SESSION (KROK B — the handoff back)

Tell pe-master-auditor "cw capture done" + confirm: the JSONL line count, the
screenshots count, SESSION_LOG filled. The validator + the report build + the
commit + the PE-MASTER report = KROK B (NOT your job).
