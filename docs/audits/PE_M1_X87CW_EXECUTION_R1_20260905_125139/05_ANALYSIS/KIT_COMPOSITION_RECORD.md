# KIT_COMPOSITION_RECORD — PE_M1_X87CW_EXECUTION_R1_20260905_125139 (KROK A)

## What this kit composes (every element + its source)

| Kit element | Composed from | Pointer |
|---|---|---|
| The read points (FDIV 0x0098CE5A / FLD 0x0095B2BC; the fallbacks 0x0095B180 / 0x0098FE00; the aux PROCESS_ENTRY) | The approved design W2 | EXPERIMENT_DESIGN.md SHA 56D6101D44FED255... (PE-MASTER DESIGN APPROVED) |
| The byte pre-verify patterns (DC 35 A8 D7 A7 00 / DD 05 58 C7 A8 00) | The design W3.3 step 8 + CONSTANT_ADDRESS_LOCK | the pinned input SHA 6F4A9A6E... |
| The N=10/site policy + the series semantics | The design W3.4 step 12 | same |
| The JSONL schema (16 fields; raw + decoded) | The design W3.4 step 13 | same |
| The cross-site agreement check | The design W3.4 step 14 | same |
| The liveness discipline (the terminate + the independent proof + ACTIVE_ORPHANED) | The design W3.5 + the profile §14 | same |
| The failure classes (7) | The design W4 | same |
| The verdict strings (MEASURED-PC53 / MEASURED-PC64 / MEASURED-PC24-DEFECT / OPEN-<class> + the RC bound) | The design W5 | same |
| The 30-min window + the attempt ladder | The design W3.6-W3.7 | same |

## The sandbox build (mechanical; verified)

- The client working copy: Entropia.exe (SHA E7785430... verified post-copy) +
  the sibling DLL set (12 DLLs) + the launcher/patcher family (ClientLoader.exe,
  CLDLLPatcher.exe, CLUpdater.exe, PE.exe) + ClientFiles.txt + Download.data +
  the Data\ tree (1818 files / 2.22 GB — the exact source census) into
  04_RUNTIME\sandbox\wd\. EXCLUDED (documented decision): the installer
  entropia_9.3.5-NX4NMX8E.exe (1.49 GB — never a runtime prerequisite),
  dxwebsetup.exe, vcredist_x86_sp1.exe, Uninstall.exe, the .url shortcuts, the
  EULA/policy text files (none is loaded by the client at runtime; the game
  launches identically without them). The exclusion set is recorded so the
  operator/auditor can re-derive the sandbox composition.
- The debugger: the x32dbg portable tree copied + the post-copy pin verify:
  x32dbg.exe = 822028F0755DBA773E445EAF57FDB3DBA84C9550AC7BDAD2AFA449912B5FBA41
  (the design W3.1.2 pin) — MATCH.
- **The x32dbg SOURCE-LOCATION NOTE (the pin is the binding identity):** the
  design's literal source path (D:\x64dbg\release\x32\) does not exist on this
  disk; the pin-identical portable was located at
  99_Audits\PE_FORENSIC_TOOLCHAIN_BOOTSTRAP_R1_20260904_080000\04_CALIBRATION\C3_X32DBG\x32dbg_local\
  (the historical C3 calibration tree) and verified against the pin hash BEFORE
  the copy; the copy re-verified after. The SHA pin — not the historical path —
  is the identity authority (the standing rule: re-hash everything personally).

## The tool proofs

- verify_sandbox.py: PASS, 20/20 checks, exit 0 (the record: 01_RAW\sandbox_verify_record.json).
- validate_cw_capture.py: the fail-closed SELF-TEST — 3 invalid fixture lines
  (an eip mismatch, a vacuous field, a non-JSON line) ALL caught + the
  N-incompleteness flagged; exit 1 (the record: 00_CONTROL\selftest_output.json).
  No valid capture was simulated (the design prohibition; NOT_EXECUTED_BY_WORKER.md).

## The authorization chain (for the record)

The PE-MASTER verdict (RUN-1..4 MASTER_ACCEPTED + the x87 CW DESIGN APPROVED,
G1 fulfilled) relayed by the human 2026-09-05, INCLUDING the explicit
"HUMAN GO RUNTIME (this relay = the human's explicit GO)" — cited verbatim.
KROK A = this kit; the MANUAL measurement = the human operator (the x32dbg
automation blocker is a measured fact of this environment); KROK B (the ingest,
the report, the exact verdict string, the path-limited commit) follows the
operator's completion signal.
