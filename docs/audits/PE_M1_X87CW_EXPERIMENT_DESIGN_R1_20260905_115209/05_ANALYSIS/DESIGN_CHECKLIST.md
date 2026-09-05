# DESIGN CHECKLIST — PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209

Two checklists: (A) what THIS design run completed before handing off; (B) what the EXECUTION run must verify before/at the GO. Item sources are the prompt (§), the EXPERIMENT_DESIGN.md sections (W), the profile (§14/§16), and the x32dbg skill.

## A. THIS DESIGN RUN (complete-before-handoff)

- [x] A1. Prompt SHA256 verified (4F33C0E6... = expected; MATCH — 01_RAW/pre_run_locks_hashes.json).
- [x] A2. ALL 9 pinned inputs personally re-hashed; ALL MATCH; zero HARD_STOP triggers (§2).
- [x] A3. Output root verified FREE (no collision; the tree created by this run) (§1).
- [x] A4. BASE_SHA recorded = 642bc12 (full 642bc123fe036a4cda1d08fafcbbabecb646a160; origin in sync; worktree clean at start).
- [x] A5. W1 complete: both target addresses with per-field provenance (EXPERIMENT_DESIGN.md W1; the chain functions stated EXACTLY per the canon — no new static claims).
- [x] A6. W2 complete: the primary site-local read points + the chain-entry fallbacks + the init-vs-site disambiguation + the bounded FLDCW-presence check composed FROM the canon's own chain-level fact (W2).
- [x] A7. W3 complete: the step-by-step x32dbg procedure (sandbox-copy discipline, the binary hash pre-verify, spawn, the bp placement + byte pre-verify, the CW capture, N=10-hit policy with the reason, the JSONL format, the §14 liveness discipline, the graceful detach, the honest automation-blocker note) (W3).
- [x] A8. W4 complete: the 7 failure classes, each with the detection signature + the disposition (W4).
- [x] A9. W5 complete: the PASS/FAIL semantics (PC=53/64 → MEASURED closure; PC=24 → the defect branch; ambiguous → OPEN with the class; the RC honesty bound; OBSERVATION-ONLY) (W5).
- [x] A10. W6 complete: the forecast table with §16.4 labels; no pre-commitment (W6).
- [x] A11. The composition record cites every canon fact with its evidence pointer (COMPOSITION_RECORD.md).
- [x] A12. GAP CHECK performed: every design need mapped to a canon fact or a bounded execution-phase check; NO CANON_GAP found (COMPOSITION_RECORD.md §GAP CHECK).
- [x] A13. 04_RUNTIME\NOT_EXECUTED.md present (zero runtime executed by THIS run).
- [x] A14. ZERO client launches / x32dbg sessions / Ghidra runs / new static claims / edits to frozen files / original payloads / nested agents (RUN_MANIFEST prohibitions_compliance).
- [x] A15. The package complete: design + checklist + composition record + extracts + locks + manifest + report + handoff + artifact_index.
- [x] A16. The repo mirror committed + pushed (ONLY the mirror tree; AUDIT_ENTRYPOINT.md untouched) — recorded in HANDOFF.md.

## B. THE EXECUTION RUN (verify at the GO; from EXPERIMENT_DESIGN.md W3)

### B1. GO-gate (before ANY launch)
- [ ] G1. The PE-MASTER review of THIS design package = MASTER_ACCEPTED.
- [ ] G2. The human's explicit "GO runtime" recorded in the execution run's control record.
- [ ] G3. A FRESH execution RUN_ID + tree (the RUN_ID reuse rule §16.7; this package = the input, not the execution record).
- [ ] G4. Every pin re-hashed personally at execution start: Entropia.exe = E7785430... (8,015,872 B); x32dbg.exe = 822028F0...; the design package itself re-hashed against its committed SHAs.

### B2. Sandbox pre-flight (W3.1)
- [ ] The x32dbg portable copy inside the execution run tree; re-hashed (822028F0...).
- [ ] The sandbox working copy of Entropia.exe + the mirrored runtime prerequisites; the copy re-hashed = E7785430... (ANY mismatch → W4.7 ABORT, fail-closed).
- [ ] The original pcg_install\Entropia.exe NEVER launched.
- [ ] SESSION_LOG.txt opened (paths, timestamps, hash values, operator).

### B3. Session (W3.2-W3.6)
- [ ] Spawn (not attach); the debuggee PID recorded; window-title evidence captured.
- [ ] Module base verified (== 0x00400000 → canon VAs verbatim; else delta-shift all bp VAs).
- [ ] Auxiliary read C: the entry-breakpoint CW recorded (the disambiguation datum).
- [ ] BP1 = 0x0098CE5A + BP2 = 0x0095B2BC placed (hardware); the byte pre-verify passed (`DC 35 A8 D7 A7 00` / `DD 05 58 C7 A8 00`; a mismatch → DO NOT PROCEED, W4.3).
- [ ] The capture: FPU-panel CW read per hit; N = 10 per site; the JSONL one-line-per-hit (the schema per W3.4 step 13); per-hit screenshots; the cross-site agreement check performed.
- [ ] The bounded window recorded (N hits / steady state / the 30-minute bound — whichever first).
- [ ] Failure classes dispositioned per W4 (no silent pass; NOT_OBSERVED ≠ never-reached).

### B4. Closure (W3.5)
- [ ] The JSONL + screenshots saved BEFORE any termination.
- [ ] The debuggee terminated from the debugger; the INDEPENDENT exit proof (OS PID query) captured.
- [ ] x32dbg closed; the ACTIVE_ORPHANED check over all session-spawned PIDs (§14 rule 14).
- [ ] The liveness verification recorded in SESSION_LOG.
- [ ] The outcome classified per W5 (MEASURED-PC53 / MEASURED-PC64 / MEASURED-PC24-DEFECT / OPEN-<class>); the RC dimension recorded per W5.1.

### B5. Honest reporting (the §14/§16 rules + the skill's checklist)
- [ ] Anything not achieved recorded honestly (the automation blocker note; a null screenshot marked; the FSTCW-AX fallback lines labeled).
- [ ] The JSONL syntax-validated line-by-line before it is cited as evidence (§14 rule 5/6).
- [ ] ZERO value-modification claims beyond the disclosed FSTCW-AX fallback (if used); zero hooked-runtime claims.
- [ ] The report uses the exact verdict strings (W5.3); the split-verdict discipline (§16.1) if any layer partially failed.
