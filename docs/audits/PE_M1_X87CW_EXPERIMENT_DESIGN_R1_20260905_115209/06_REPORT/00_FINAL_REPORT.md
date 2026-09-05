# 00_FINAL_REPORT — PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209

**RUN_STATUS: DESIGN_COMPLETE**
**HARD_STOP_REASON: NONE**

## 1. What this run is

RUN-3 of the PE-MASTER loop directive: **P0-1 PREP — the x87 CONTROL WORD experiment design** (DESIGN-ONLY, OFFLINE). The deliverable = the experiment design for the deferred runtime measurement of the actual x87 CW of the PCG_9_3_5 client at its foliage/grid arithmetic sites — the one deferred execution that resolves the M1 arithmetic model's conditionality (PC ∈ {53,64} → the PC=24 branch empirically excluded, the 14,104/229,376 lerp mismatches really absent; PC=24 → a real 6.15% defect requiring a correction run).

## 2. What was executed (offline only)

- The prompt SHA256 verified (4F33C0E6... = expected).
- ALL 9 pinned inputs personally re-hashed — **ALL MATCH** (`01_RAW\pre_run_locks_hashes.json`): the V4 matrix json/md, EVIDENCE_MANIFEST_V4, CONSTANT_ADDRESS_LOCK, PE_SECTION_MAP, Entropia.exe (E7785430..., 8,015,872 B — read-only identity pin, NEVER launched), oracle_battery, domain_reproof, offline_rechecks. Plus: the x32dbg tool pin (822028F0... MATCH) and the pc24_synthetic_measurement citation (01B96D25... MATCH).
- The output root verified FREE; the tree created. BASE_SHA = 642bc12 (origin in sync; clean worktree).
- The locked canon read (the V4 matrix rows 10/11 + registry + open list + honest limits; the CONSTANT_ADDRESS_LOCK three_qword_constants; PE_SECTION_MAP; oracle_battery pcrc_conditional_model; domain_reproof domains; the pe-master-auditor profile §14/§16; the pe-x32dbg-runtime skill).
- The design composed: **W1** the target addresses (FDIV @0x0098CE5A consuming 32767.0 f64 @0x00A7D7A8; FLD @0x0095B2BC consuming 65535.0 f64 @0x00A8C758; the chain functions FUN_0098fe00 grid / FUN_0095b180 spawn — stated EXACTLY per the static record, each with provenance); **W2** the CW read points (the site-local primary + the chain-entry fallbacks + the init-vs-site disambiguation + the FLDCW-presence bounded check built on the canon's own chain-level no-FLDCW fact); **W3** the step-by-step x32dbg procedure (the sandbox-copy + hash pre-verify discipline, the spawn, the hardware bps + byte pre-verify, the FPU-panel CW capture, the N=10-hit policy with reasons, the JSONL schema, the §14 liveness discipline, the graceful detach, the honest GUI-automation-blocker note); **W4** the 7 pre-declared failure classes with detection signatures + dispositions; **W5** the PASS/FAIL semantics (MEASURED-PC53/64 closure / MEASURED-PC24-DEFECT / OPEN-\<class>, the RC honesty bound, OBSERVATION-ONLY); **W6** the §16.4-labeled forecast (PC=53 MOST_LIKELY; PC=64 PLAUSIBLE; PC=24 LOW_PROBABILITY — no pre-commitment).

## 3. Compliance (the prohibitions — all honored)

- **ZERO client launches, ZERO x32dbg sessions, ZERO Ghidra analysis runs, ZERO runtime of any kind** (`04_RUNTIME\NOT_EXECUTED.md`).
- **ZERO new static claims** — every design fact maps to a canon pointer in `05_ANALYSIS\COMPOSITION_RECORD.md` (22 canon compositions + 5 execution-phase bounded checks).
- **ZERO edits to frozen/completed files** — the V3/V4 matrices were pinned inputs (re-hashed, untouched); no completed run dir, no shared tool/skill, no src/, no AUDIT_ENTRYPOINT.md, no PE_AUTO_LOOP.json.
- **Entropia.exe** = read-only identity pin (hash-verified; never launched; never committed).
- **No original proprietary payloads committed**; **no nested agents**.

## 4. The GAP CHECK (the CANON_GAP rule)

Every design need was checked against the locked canon BEFORE composition (COMPOSITION_RECORD.md §GAP CHECK, items 1-6): **CANON_GAPS_FOUND: NONE.** The one question the canon does not answer statically (the binary-wide FLDCW census — the canon's own 910-pair caveat) is handled as a bounded execution-phase check, NOT as new static analysis — consistent with both the design mandate and the execution-run scope.

## 5. The state delta

- The x87-CW open item (V4 known_open item 7) **remains OPEN — now with a complete, canon-grounded, PE-MASTER-reviewable experiment design attached** (this package).
- No canonical file changed. No matrix edited. The V4 conditionality wording stands until the MEASURED outcome supersedes it (W5.1; a separate, ordered composition after the execution run).
- M1 remains PARTIAL / MILESTONE_CANDIDATE_FOR_DEEP_AUDIT per the governance state; nothing here authorizes M2.

## 6. The next gate

**The PE-MASTER design review of this package → the human's explicit "GO runtime" → the execution run** (a fresh RUN_ID, the W3 procedure, the W5 outcome classification). The design requires exactly ONE successful runtime execution to resolve the P0, with pre-declared failure classes ensuring no outcome is a silent pass.
