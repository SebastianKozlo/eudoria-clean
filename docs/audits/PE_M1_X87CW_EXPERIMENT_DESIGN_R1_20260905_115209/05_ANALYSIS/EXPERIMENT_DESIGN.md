# EXPERIMENT DESIGN — the x87 CONTROL WORD measurement of the PCG_9_3_5 client

**RUN_ID:** PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209
**RUN CLASS:** DESIGN-ONLY (offline; ZERO client launches, ZERO x32dbg sessions, ZERO Ghidra runs)
**DELIVERABLE STATUS:** the design for the deferred, separately-gated runtime execution (the PE-MASTER design review → the human's "GO runtime" → THEN this procedure executes)
**COMPOSITION BASIS:** the EXISTING locked static canon ONLY (see `03_STATIC\CANON_EXTRACTS.md` + `05_ANALYSIS\COMPOSITION_RECORD.md`; every canon fact carries its file+SHA pointer). This document makes **ZERO new static claims**.

---

## 0. THE ONE P0 QUESTION (the design's purpose)

**Czy eksperyment pomiaru rzeczywistego x87 CONTROL WORD klienta PCG_9_3_5 da się zaprojektować tak, żeby JEDNO uruchomienie runtime (odrębne, odroczone) rozstrzygnęło warunkowość modelu arytmetyki M1?**

- **CW@chain-entry ∈ {PC=53, PC=64}** → the M1 conditional model's PC=24 branch is **EMPIRICALLY EXCLUDED** for this build → the 14,104/229,376 lerp mismatches are really NOT present in the original → the x87-CW open item **closes as MEASURED** (W5).
- **CW@chain-entry = PC=24** → the conditional model **BECOMES a real defect** of the reconstruction (a 6.15% divergence on the REAL lerp domain) → a correction run is REQUIRED before any closure (W5).

The design below makes exactly ONE runtime execution sufficient to resolve this, with pre-declared failure classes (W4) so that no outcome becomes a silent pass.

**Why a runtime measurement at all** (the canon's own words, X3.4/X4.4): "the ACTUAL client CW is UNMEASURED — the falsifier = a runtime capture". Statically the canon holds: the documented Win32 default (0x027F, PC=53, RC=nearest-even) — explicitly "the PLATFORM DOCUMENTED DEFAULT, NOT a measurement of the original client" — plus the chain-level fact that the 17 audited foliage-chain functions (51 FPU instructions) contain **no FLDCW/FLDENV/FRSTOR**. What static analysis cannot decide is what the CW actually is on the live FPU hot path (the canon's `unmeasured` field names the exact outside-the-chain mechanism candidate: possible D3D8 FPU-mode changes if the device was created without D3DCREATE_FPU_PRESERVE). The measurement reads the CW at the arithmetic sites themselves — under either init condition the site-local value is the one that governed the arithmetic, so ONE execution answers the P0.

---

## W1. TARGET ADDRESSES (from the locked static canon; provenance cited per address)

### W1.1 — The FDIV site (the RNG divisor path)

| Field | Value | Provenance |
|---|---|---|
| Instruction VA | **0x0098CE5A** | CONSTANT_ADDRESS_LOCK `three_qword_constants[0].instruction_va` (X1.1); V4 row 11 `implementation` "FDIV QWORD @0x0098CE5A" (X3.3) |
| Instruction bytes | `DC 35 A8 D7 A7 00` | CONSTANT_ADDRESS_LOCK (X1.1) — the breakpoint-placement pre-verify pattern (see W3 step 6) |
| Opcode decode | `FDIV qword ptr [0x00A7D7A8]` | CONSTANT_ADDRESS_LOCK (X1.1) |
| Consumed constant | _DAT_00a7d7a8 = **32767.0 f64** (bytes `00 00 00 00 C0 FF DF 40`), .rdata, file-backed, file offset 0x67D7A8 | CONSTANT_ADDRESS_LOCK (X1.1) + PE_SECTION_MAP (X2: .rdata raw_offset == rva, so VA − 0x400000 = file offset) |
| Role in the chain | **the rand01 divisor**: `rand01 = f32(r / 32767.0) → [0,1] INCLUSIVE`, with the f32 rounding at `FSTP DWORD @0x0098CE60` (the f32 rounding BEFORE return) | V4 row 11 `knowledge` (X3.2) |
| Path assignment | the RNG-next function family: the row's evidence set carries `iter032_re_dec_0098cdf0_rng_seed.c` + `iter032_re_dec_0098ce30_rng_next.c`, and the row names FUN_0098ce30 as containing the adjacent dead-code FADD idiom of this arithmetic (0x0098CE30 < 0x0098CE5A < 0x0098CE60) | V4 row 11 `knowledge` + `evidence` (X3.2/X3.3) |
| Feed-forward | rand01 → the sampler `value = f32(rand01*(max-min)+min)` (FUN_0095ac30 FSTP DWORD @0x0095ACF0) → the spawn-loop nodeScale | V4 row 11 `knowledge` (X3.2) |

### W1.2 — The FLD site (the position divisor path)

| Field | Value | Provenance |
|---|---|---|
| Instruction VA | **0x0095B2BC** | CONSTANT_ADDRESS_LOCK `three_qword_constants[1].instruction_va` (X1.2); V4 row 11 `implementation` "FLD QWORD @0x0095B2BC" (X3.3) |
| Instruction bytes | `DD 05 58 C7 A8 00` | CONSTANT_ADDRESS_LOCK (X1.2) |
| Opcode decode | `FLD qword ptr [0x00A8C758]` | CONSTANT_ADDRESS_LOCK (X1.2) |
| Consumed constant | _DAT_00a8c758 = **65535.0 f64** (bytes `00 00 00 00 E0 FF EF 40`), .rdata, file-backed, file offset 0x68C758 | CONSTANT_ADDRESS_LOCK (X1.2) + PE_SECTION_MAP (X2) |
| Role in the chain | **the u16 position divisor**: `nodeX/Y = f32(u16 / 65535.0 f64)` = node-local fractions [0,1], stored at node+0x5C/0x60 | V4 row 10 `knowledge` (X3.1) |
| Path assignment | the **FUN_0095b180 spawn loop** (the position divisor path executes inside the spawn function: 0x0095B180 < 0x0095B2BC < 0x0095B347; the same function's nodeScale FMUL follows at 0x0095B347) | V4 row 10 `knowledge` (X3.1) |

### W1.3 — The chain functions (EXACTLY what the static record states)

**FUN_0098fe00 — the GRID path** (V4 row 10 `knowledge`, verbatim content in X3.1): the procedural grid generation — subdivision levels 0..4 → cell steps 1/2/4/8/16, **INTEGER-ONLY per the iter035 census**, 24-byte cells, density = `*(cell+8)>>3`. Its companion FUN_00990810 stores the cell records as {u16 x, u16 y, u32 id} triples. *The two pinned constant-consumption sites (W1.1/W1.2) do not belong to this function — the canon places both arithmetic sites on the RNG and spawn paths below; FUN_0098fe00's role in the experiment is the chain-entry fallback read point for the grid half of the chain* (W2.2).

**FUN_0095b180 — the SPAWN path** (V4 row 10 `knowledge`, verbatim content in X3.1): the instance spawn loop — consumes the stored records, computes nodeX/Y = f32(u16/65535.0) (the FLD site W1.2, node+0x5C/0x60), nodeScale = f32(|value × 0.00007812499825377017|) (the FMUL @0x0095B347, _DAT_00a980d0, node+0x68), binds the u32 model at node+0x64; rotation IDENTITY = the RE-faithful absence; spawn default level 1; six binary FSTP-DWORD f32 rounding points (Math.fround in the reconstruction); 76/76 instances bit-exact against the binary-derived reference. *The FLD site W1.2 executes inside this function; the rand01 that feeds its scale comes from the RNG path (W1.1) — the two sites share one arithmetic chain (the sampler lerp between them), which is why the two sites' CW reads must agree (the N-hit policy + the cross-site agreement check, W3 step 8).*

**Callers:** the canon states the chain roles and the data flow (grid → stored records → spawn loop consuming the RNG + position arithmetic); it does not state a caller census for these functions, and this design does not need one (the breakpoints are at the canon-VAs themselves; no caller claims are made).

### W1.4 — What the FDIV/FLD sites have in common (why they are the right probes)

Both are **f64 QWORD-consuming x87 instructions on the same FPU hot path** whose results are immediately rounded to f32 at adjacent FSTP-DWORD points (0x0098CE60; the six spawn-path points incl. 0x0095ACF0). The M1 conditional model is precisely about the precision (PC) the x87 unit uses for these intermediates: PC=53/64 → the f64/f80 intermediates the reconstruction models; PC=24 → the 24-bit intermediate that breaks 14,104/229,376 real lerp values (X5). Reading the CW at the exact sites that perform this arithmetic is therefore the direct measurement of the model's condition.

---

## W2. THE CW READ POINT(S) — where the control word gets read and why that answers the P0

### W2.1 — The PRIMARY read points: the two instruction sites themselves

**Read point A = the FDIV site @0x0098CE5A** (hardware breakpoint); **read point B = the FLD site @0x0095B2BC** (hardware breakpoint). At the FIRST hit of each (and then at each of the first N hits — W3 step 8), the operator reads the FPU control word from the **x32dbg FPU register panel** (View → FPU: the CW is part of the thread's FloatSave context, which the debugger displays; this is the debugger's own context read — **zero target modification**).

**Why the sites themselves (and not merely the process default):** the P0 question is what precision governed THE ACTUAL ARITHMETIC at these instructions. A site-local read needs no inference chain: whatever the init CW was, and whatever any outside code did to the FPU mode, the CW value live at the FDIV/FLD is definitionally the one that governed the operand load and the division. This closes the init-vs-hotpath question in ONE execution instead of leaving a inferential gap.

### W2.2 — The FALLBACK read points (armed only on the bounded-window expiry — W3 step 10)

- **Fallback A = the chain-entry of the spawn path: FUN_0095b180 entry (VA 0x0095B180)**; **Fallback B = the chain-entry of the grid path: FUN_0098fe00 entry (VA 0x0098FE00)**. If the instruction-site breakpoints are NOT_OBSERVED_IN_CAPTURE within the bounded window, the re-attempt reads the CW at the function entries instead.
- **Carry-over logic (canon-grounded):** the chain-entry CW equals the in-function site CW **because the audited chains contain no control-word modification** — the frozen iter035 operand census "lists every FPU instruction of the 17 audited foliage-chain functions (51 instructions); NONE is FLDCW/FLDENV/FRSTOR — the audited chains do not modify the control word themselves" (oracle_battery `text_cw_bytepair_scan.chain_level_static_fact`, X4.3). A CW read at the entry of an audited chain function therefore transfers to the chain's FPU sites **within the audited chains** — this is the canon's own chain-level static fact, not a new scan.
- **Limit honestly bounded:** the 910 raw d9/dd byte-pair count in .text is (per the canon's own caveat, X4.3) "a raw byte-pair sensitivity count, NOT an instruction census" — the canon does NOT claim the whole binary is FLDCW-free, and this design does not either. That is exactly why the site-local read (W2.1) is primary and the entry-local read is fallback.

### W2.3 — The DISAMBIGUATION read: process-entry CRT-init CW vs the site-local CW

**Auxiliary read point C = the thread's CW at the debugger's entry breakpoint** (the process entry, after the initial system breakpoint → run to the module entry; read the FPU panel CW once). Purpose: a comparison datum, not the answer.

**The disambiguation logic:**

1. The CW can legitimately differ between process init and the FPU hot path **only if some code changes it between the two points** (the CW has no other dynamics — it is thread state).
2. The canon answers the between-the-chain portion: no FLDCW/FLDENV/FRSTOR inside the 17 audited chain functions (X4.3). Any init-vs-site difference must therefore originate **outside the audited chains** — and the canon itself names the candidate mechanism: "possible D3D8 FPU-mode changes if the device was created without D3DCREATE_FPU_PRESERVE" (oracle_battery `unmeasured`, X4.4).
3. **Resolution rule:** the SITE-LOCAL value (W2.1) is authoritative for the P0 in every case. If site == init: one consistent answer, recorded, closed. If site != init: the difference is recorded as an OBSERVED init→site transition — the candidate mechanism is noted as the canon-flagged D3D8 possibility (a hypothesis, §16.4-labeled, NOT a conclusion), and the P0 is still answered by the site-local value, because the model's condition is about the arithmetic at the sites.
4. **The FLDCW-presence question** (does ANY code on the init→site path modify the CW?): the canon answers it at the chain level (X4.3) but not binary-wide (the 910-pair scan is explicitly not a census). The design therefore includes a **bounded execution-phase check instead of any new static claim**: (a) the site CW is captured at EACH of the first N hits (W3 step 8) — CW variation across hits is direct evidence that a CW-modifying event occurs upstream of some hits; (b) CW stability across N hits + equality with the entry-breakpoint CW bounds the answer without any binary-wide census. If the series is unstable, the outcome is the CW_READ_AMBIGUITY class (W4.5) — never a silent pass, never an invented static fact.

---

## W3. THE x32dbg PROCEDURE (step-by-step, executable verbatim on the GO)

**Scope note:** this procedure is the deferred execution. It is written to be run by the human operator (manual GUI session — the x32dbg automation blocker is a measured fact of this environment, W3.11). Every step is composed from the locked canon + the verified tool recipes; nothing below requires new static analysis.

### W3.0 — Preconditions (the GO-gate items; see also DESIGN_CHECKLIST.md)

- G1. The PE-MASTER design review of THIS package returned MASTER_ACCEPTED.
- G2. The human's explicit "GO runtime" for the execution run.
- G3. The execution run gets its OWN fresh RUN_ID + tree (the RUN_ID reuse rule, profile §16.7); this design package is the input, not the execution record.
- G4. The pinned inputs re-hashed at the execution run's start (every pin re-hashed personally — the standing rule): Entropia.exe = E7785430... (8,015,872 B); the x32dbg tool pin = 822028F0....

### W3.1 — The sandbox copy discipline (NO original-file launches)

1. Create the execution run's sandbox inside the execution run tree: `<RUN_ROOT>\04_RUNTIME\sandbox\` (all debugger writes stay in-tree — the portable-copy discipline).
2. Copy the **x32dbg portable tree** from `D:\x64dbg\release\x32\` into `sandbox\x32dbg\` (the full tree, so ini/db writes land in-tree). Re-hash `sandbox\x32dbg\x32dbg.exe` → MUST equal `822028F0755DBA773E445EAF57FDB3DBA84C9550AC7BDAD2AFA449912B5FBA41` (x32dbg 0.0.2.5, the skill pin).
3. Copy the **target binary** `Entropia.exe` from `D:\Eudoria_Reconstruction\pcg_install\` into the sandbox working directory `sandbox\wd\` — TOGETHER WITH the client's runtime prerequisites mirrored from the same install tree (the pcg_install layout: the sibling DLL set + the `Data\` tree + the client's configuration files, so the working copy launches as the install would). The **original** `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` is NEVER launched (the read-only identity pin).
4. **The binary hash pre-verify (BEFORE launch, fail-closed):** `Get-FileHash sandbox\wd\Entropia.exe` → MUST equal `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` AND the size MUST be 8,015,872 B. ANY mismatch → **IMMEDIATE ABORT before any launch** (the sandbox-hash-mismatch failure class, W4.7). Record the verification in the execution run's 01_RAW.
5. Record in SESSION_LOG.txt: the sandbox paths, the copy timestamps, the hash values verified, the operator identity.

### W3.2 — The spawn (attach is fallback-only)

6. Launch: `sandbox\x32dbg\x32dbg.exe sandbox\wd\Entropia.exe` (the working-directory context = `sandbox\wd\`). The debuggee spawns paused at the **initial system breakpoint** (the verified spawn recipe; window-title evidence recorded — the debuggee PID from the x32dbg title/status bar goes into SESSION_LOG.txt).
   - **Module-base verification (a bounded runtime check, not a static claim):** open the Memory Map and verify the Entropia.exe module base. The canon VAs (0x0098CE5A, 0x0095B2BC, 0x0095B180, 0x0098FE00) are image VAs with image_base 0x00400000 (PE_SECTION_MAP, X2). **If the loaded base == 0x00400000: use the canon VAs verbatim. If it differs (relocation): compute delta = actual_base − 0x00400000 and shift every breakpoint VA by delta before placement.** The design makes no claim about whether relocation occurs; this check makes the procedure correct either way.
7. **Auxiliary read C (the init CW):** run to the module entry breakpoint (F9 from the system breakpoint); at the entry, open View → FPU and record the Control Word value (one JSONL line, capture_method=`fpu_panel`, site=`process_entry`). This is the disambiguation datum of W2.3.

### W3.3 — The breakpoints (placed BEFORE running on; conditions)

8. Place **hardware breakpoints** (Set Hardware → on Execution at the address; hardware preferred on a networked client to avoid self-checksumming/byte-patch interactions — the debugger does not modify code bytes with hardware bps):
   - **BP1 = 0x0098CE5A** (the FDIV site; expected bytes at the site `DC 35 A8 D7 A7 00` — the operator verifies the disassembly line at the address matches the canon decode before running; a mismatch = DO NOT PROCEED, the module-base/bytes assumption failed → DEBUGGER_SESSION_FAILURE with the observed bytes recorded).
   - **BP2 = 0x0095B2BC** (the FLD site; expected bytes `DD 05 58 C7 A8 00` — same pre-verify).
   - Conditions: **none** (unconditional; every hit is a capture event). The fallback breakpoints BP3 = 0x0095B180 and BP4 = 0x0098FE00 are NOT armed in the first attempt (W3.10 arms them only on the bounded-window expiry).
9. Record in SESSION_LOG.txt: the bp addresses, the byte pre-verify results, the time.

### W3.4 — The CW capture (per hit; the JSONL; the N-hit policy)

10. **Run (F9).** The client proceeds; when BP1/BP2 hits the debugger pauses with EIP at the site.
11. **The capture action at each hit:** open View → FPU; read the **Control Word** (the panel renders the CW; the underlying source is the thread context FloatSave.ControlWord — the debugger's read, zero target modification). Also record EIP (must equal the bp VA; a conditional self-check), the hit index, the timestamp. **Fallback capture (disclosed, last resort only):** if the FPU panel is unreadable/unavailable in the session, execute `FSTCW AX` via the debugger's command bar (injecting one instruction) — this writes the CW to AX. **Disclosure:** FSTCW AX does not touch the CW, memory, or the code path, but it DOES modify the AX register content — the single, disclosed, register-only deviation from strict observation-only, used only if the panel read fails; each such line is marked `capture_method=fstcw_ax_fallback` in the JSONL. The preferred capture is always the panel/context read.
12. **The N-hit policy: N = 10 per site** (10 hits at BP1 + 10 at BP2 per attempt). **Why 10:**
    - (a) the canon says the chains do not modify the CW (X4.3), so the site CW is expected to be a per-thread constant — N > 1 guards against a **transient early value** (e.g., a hit before the thread's final FPU configuration settles, or before the canon-flagged D3D8 device-creation FPU mode change, X4.4, if it occurs at all);
    - (b) a series of 10 lets the design **observe stability vs variation** cheaply (the spawn loop is expected to be hot during world load; 10 hits are quick);
    - (c) N = 10 bounds the session (each hit is a manual panel read + transcription; the bounded window is the N, not wall-clock alone).
    **Series semantics:** all hits' CW values are logged (the full series is RAW evidence); a stable series → the stable value is the measurement; a mid-series change → the transition point + both values are recorded, the steady-state (later) value answers the P0 for the steady-state arithmetic, AND the transition itself is recorded as the observed CW-change event (feeding the W2.3 disambiguation); an oscillating/unclear series → CW_READ_AMBIGUITY (W4.5), no silent pass.
13. **The JSONL log format** (`04_RUNTIME\cw_capture.jsonl` — one JSON object per line, operator-transcribed at each hit; syntax-validated line-by-line at ingestion per §14 rule 6):
    ```json
    {"hit_index": 1, "attempt": 1, "site": "FDIV_0x0098CE5A", "bp_va": "0x0098CE5A", "eip": "0x0098CE5A", "pid": <debuggee PID>, "cw_hex": "0x027F", "pc_bits": "10", "pc_decoded": "53-bit double", "rc_bits": "00", "rc_decoded": "nearest-even", "exception_masks_bits": "111111", "cw_full_binary": "0000001001111111", "capture_method": "fpu_panel", "screenshot": "hit_01_fdive.png", "timestamp": "ISO-8601"}
    ```
    Field notes: `pc_bits` = CW bits 8-9 (00=24-bit single / 01=reserved / 10=53-bit double / 11=64-bit extended — the decode table the canon itself uses, X4.1); `rc_bits` = bits 10-11 (00=nearest-even / 01=down / 10=up / 11=truncate); `exception_masks_bits` = bits 0-5. **Every line carries the decoded PC/RC fields** (the decode is mechanical from the 16-bit value; the JSONL records both raw and decoded so the decode is re-checkable). One screenshot per hit (the verified screenshot pattern) is the corroborating artifact; a null screenshot is honestly marked, never assumed.
14. **Cross-site agreement check (after the captures):** the FDIV-site series and the FLD-site series must agree on PC (and RC). They are the same FPU hot path (W1.4); a cross-site disagreement = CW_READ_AMBIGUITY (W4.5), recorded — not averaged away.

### W3.5 — The process-liveness discipline (§14) + the graceful detach

15. **During the session:** the debuggee PID is recorded at spawn (SESSION_LOG). A controller-side event (x32dbg hang, crash, dialog) is NEVER classified as target state (§14 rule 1) — the target's state is only ever asserted from the debugger's own process view + an OS-level query.
16. **Graceful detach (the end of a completed capture):** after the N hits per site are captured: (a) save `cw_capture.jsonl` + the screenshots; (b) **Terminate the debuggee from the debugger** (the client is a network game; letting it run on serves nothing — terminate, do not detach-and-leave-running); (c) **the independent exit proof (§14 rule 2):** query the OS for the recorded PID (`Get-Process -Id <pid>` / tasklist) — the process must be GONE (or exit code captured via the debugger's termination event + the OS query both); (d) close x32dbg; (e) **the ACTIVE_ORPHANED check (§14 rule 14):** verify no session-spawned processes remain (the debuggee, x32dbg, any children the client spawned during the session — the launcher/patcher processes observed during the run are enumerated in SESSION_LOG as encountered and each is checked dead); (f) record the liveness verification in SESSION_LOG with the PIDs + the verification command outputs.
17. **If the session must abort mid-run** (a failure class fires): save what exists (the JSONL lines so far are RAW evidence — keep them, marked with the abort reason), then the same terminate + independent-proof + orphan check sequence. The captured-but-incomplete state is a PARTIAL per §16.1 (split verdict by layer), never silently promoted.

### W3.6 — Honest notes the procedure carries by construction

18. **The automation blocker (measured, C3):** x32dbg in this environment has NO programmatic channel for breakpoint-setting or log export. The session is a MANUAL GUI session with operator transcription; the design does not promise, and the report must not claim, automated capture. Anything not achieved is recorded honestly (the skill's checklist discipline).
19. **No other instrumentation:** no PEFrida hooks, no DLL injection beyond the debugger itself, no D3D8 wrappers — the captured CW is from the ORIGINAL code path (W5's observation-only contract).
20. **The bounded window definition (honest):** the attempt window closes at whichever comes first — (a) N hits captured at both sites, (b) the debuggee reaches a quiescent/steady state or exits (observed via the debugger's status), or (c) a 30-minute wall-clock bound from the run-to-entry step (the operator-declared bound; NOT_OBSERVED_IN_CAPTURE within this window ≠ never-reaches, §14 rules 9-10). The window actually used is recorded in SESSION_LOG.

### W3.7 — The fallback attempt ladder (each a FRESH spawn; the previous session's evidence stands)

- **Attempt 1:** BP1+BP2 (the instruction sites) — the primary (W2.1).
- **Attempt 2 (only if W4.4 fired for both sites):** BP3 = FUN_0095b180 entry + BP4 = FUN_0098fe00 entry (the chain-entry fallbacks, W2.2) — N = 10 hits each, same capture discipline; the canon's no-FLDCW-in-chains fact (X4.3) carries the entry CW to the sites.
- **Attempt 3 (only if Attempt 2 also 0-hit AND the debuggee provably reached its steady state):** STOP — the item stays OPEN with BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW; the next-attempt proposal is a separate design (the chain may require a game-state condition to execute — e.g., reaching the world-load phase — which is a next-design INPUT to investigate, not a claim this design makes).

---

## W4. FAILURE CLASSES (pre-declared; the detection signature + the disposition for each)

Per the §14 taxonomy + the x32dbg skill's documented failure modes. **No outcome is a silent pass** — every class has a recorded disposition and the run status reflects it.

### W4.1 — TARGET_PROCESS_EXIT
- **Signature:** the debugger reports the debuggee terminated; **independent proof required** (§14 rule 2): the debugger's termination event PLUS the OS-level PID query (process gone / exit code captured). One signal alone is insufficient.
- **Disposition:** if AFTER the N captures → the captures stand (the exit does not invalidate the CW record; the run completes with the exit noted); if BEFORE any hit → the attempt ends; the exit is the window-close event; classify honestly (the capture result is NOT_OBSERVED_IN_CAPTURE, never "failed to reach"); go to the fallback ladder if the exit is a documented early-exit behavior of the build, else the item stays OPEN with this class recorded.

### W4.2 — CONTROLLER_FAILURE
- **Signature:** the operator/debugger side fails while the target state is UNKNOWN — x32dbg crashes/freezes, the transcription tooling fails, the operator session is interrupted. **A controller-side event is NOT evidence of target state (§14 rule 1).**
- **Disposition:** the JSONL lines captured so far are RAW evidence (kept, provenance-marked DERIVED_BY_POSTPROCESSOR/none per rule 15); the debuggee's actual state is then established by the independent OS query (kill it if alive, with the proof); the session verdict = split per §16.1 (OVERALL PARTIAL; the captured layer PASS-if-complete); a fresh attempt may follow as a new session with the evidence preserved.

### W4.3 — DEBUGGER_SESSION_FAILURE
- **Signature:** the session never becomes debuggable — the spawn fails (the debuggee doesn't start under the debugger), the module doesn't load, the memory map is unreadable, a breakpoint cannot be placed, or the W3.3 byte pre-verify fails (the disassembly at the VA doesn't match the canon bytes).
- **Disposition:** BLOCKED for the attempt; the exact mechanical failure recorded (error text, observed bytes); a bounded retry with the W3.6 corrections; if persistent → the item stays OPEN with this class + the retry record; the byte-pre-verify failure additionally quarantines the site assumption (module-base or build mismatch — re-verify the identity pin, never proceed).

### W4.4 — BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW
- **Signature:** the W3.6 window closes with 0 hits at BP1/BP2 while the debuggee provably ran (liveness observed during the window; TARGET_PROCESS_EXIT ruled out by the independent proof).
- **Disposition:** **NOT_OBSERVED_IN_CAPTURE ≠ never-reached** (§14 rules 9-10): record the window, the observed client state at window-close, the liveness proof; go to Attempt 2 (the chain-entry fallbacks); if Attempt 2 also 0-hits → the item stays OPEN with this class + the W3.7 Attempt-3 boundary (a separate next-design proposal; the design does NOT speculate here on what game state gates the chain).

### W4.5 — CW_READ_AMBIGUITY
- **Signature:** (a) the CW series is unstable across the N hits (a mid-series change with no clean steady state, or an oscillation); (b) the read point hit before the FPU path's final configuration (the early hits show a value that later changes — e.g., a pre-D3D8-device-creation hit, W2.3); (c) the primary panel read and the FSTCW fallback disagree; (d) the cross-site agreement check (W3.4 step 14) fails.
- **Disposition:** record the FULL series as RAW evidence (every hit, timestamps, screenshots); the steady-state answer is accepted ONLY on a clean observed transition to stability (the transition point recorded); otherwise the item stays OPEN with CW_READ_AMBIGUITY + the series + the bounded next-attempt design (e.g., a wider N with per-hit game-state annotation — a next-design input); **never averaged, never silently resolved**.

### W4.6 — ATTACH_PERMISSION_FAILURE
- **Signature:** the attach fallback (spawn failed first) cannot open the process for debugging — access denied / insufficient privilege / the OS debug-object error.
- **Disposition:** BLOCKED with the exact OS error recorded; the spawn path remains the primary (this class only matters when spawn already failed — the DEBUGGER_SESSION_FAILURE record from the spawn attempt is kept as context); the item stays OPEN with this class.

### W4.7 — SANDBOX_HASH_MISMATCH (the abort class)
- **Signature:** the W3.1 pre-launch hash check fails — the sandbox copy's SHA256 ≠ E7785430... (or the size ≠ 8,015,872 B), or the x32dbg copy's SHA ≠ 822028F0....
- **Disposition:** **IMMEDIATE ABORT before any launch** (fail-closed); NO session proceeds on an unverified copy (the skill anti-pattern "debugging the original binary path instead of a hash-verified sandbox copy" is the rejected behavior); the mismatch values recorded; BLOCKED with this class; the run does NOT silently re-copy-and-continue — a fresh sandbox build + re-verify is an explicitly recorded restart.

---

## W5. PASS / FAIL SEMANTICS (the falsifiable outcomes; OBSERVATION-ONLY)

**The measurement classification:** breakpoints + register-panel/context reads = **observation**. **ZERO value modification** (no register writes, no memory writes, no FLDCW, no code patches; the single disclosed register-only exception is the FSTCW-AX fallback, W3.4 step 11, marked per-line). **ZERO hooked-runtime claims:** no D3D8 hooks, no injected instrumentation beyond the debugger's standard debug-interrupt mechanism — the captured CW is from the ORIGINAL code path.

**The decode (mechanical, from the canon's own PC-mode table, X4.1):** CW bits 8-9: `00`=PC24 (single), `10`=PC53 (double), `11`=PC64 (extended); bits 10-11: `00`=RC nearest-even.

### W5.1 — Outcome PASS-A (the PC closure): site CW decodes to PC=53 or PC=64
- The M1 conditional model's **PC=24 branch is EMPIRICALLY EXCLUDED for this build**: the 14,104/229,376 real-lerp mismatches (and 103,073/1,245,184 synthetic) are really **NOT present in the original** → the x87-CW open item **CLOSES as MEASURED-PC53/64**; the conditional-model wording in the V4 matrix (rows 10/11 `limitations`, the known-open item, `honest_limits_binding` item 2) is superseded BY THE MEASURED VALUE in the next bounded matrix edit (a separate, ordered composition — the V4 matrix is a pinned input THIS design does not touch); **the M1 fidelity claim is UNCHANGED** (it was conditional on PC ∈ {53,64}; the condition is now measured TRUE).
- **The RC dimension (captured in the same CW read, honestly stated):** the conditional model is also conditional on RC=nearest-even (X3.4/X4.4). If the measured RC = nearest-even (bits `00`) → the full condition set is measured met; the closure is complete. If the measured RC ≠ nearest-even → the PC dimension closes (per the above) but the RC condition is NOT met and the canon holds **no measured RC-sensitivity** for the lerp domains — the item CANNOT close as MEASURED alone: it stays OPEN (a NEW sub-item: the RC≠nearest sensitivity measurement — a separate-run proposal, exactly like a canon gap; **no silent pass**).

### W5.2 — Outcome FAIL (the defect branch): site CW decodes to PC=24
- The conditional model **BECOMES a real defect**: the reconstruction's f32-lerp path diverges from the original on **14,104 / 229,376 real-domain values (6.15%)** (X5) → the M1 matrix row updates + **a correction run is REQUIRED before any closure** (the correction scope is not designed here — it is the next P0 after the measurement; what closes NOTHING is proceeding as if nothing changed).

### W5.3 — Outcome AMBIGUOUS/UNREACHABLE
- The item **stays OPEN** with the exact failure class (W4.x) + the bounded next-attempt design. **NO outcome is a silent pass.** The report strings are exact: `MEASURED-PC53` / `MEASURED-PC64` / `MEASURED-PC24-DEFECT` / `OPEN-<CLASS>`.

### W5.4 — What the measurement does NOT claim (the honesty bounds)
- The measurement covers the **observed execution window and thread(s)** of the audited chain path (bounded capture ≠ complete lifetime, §14 rule 10): the closure statement is "the CW at the chain sites, in the observed sessions, is X" — with the N-hit series + the cross-site agreement as the stability evidence, not a binary-wide or all-threads claim.
- No new static facts: the closure edits reference the MEASUREMENT + the EXISTING canon facts only.

---

## W6. FORECAST HEDGING (per profile §16.4 — the labels, never a pre-commitment)

| Forecast | Label | Basis (canon-cited; the measurement decides) |
|---|---|---|
| Site CW = 0x027F-style, **PC=53 (double), RC=nearest-even, all exceptions masked** | **MOST_LIKELY** | the documented Win32 process-default CW 0x027F (the canon's own assumed basis, X4.4) + the chain-level no-FLDCW fact (X4.3): nothing in the audited chains changes the thread default, and the MSVC CRT convention is the platform default the canon cites |
| Site CW = PC=64 (extended; e.g., 0x037F — the FINIT/x87-reset default) | **PLAUSIBLE** | the canon's own PC-mode table includes the FINIT default (X4.1); a thread whose CW was reset outside the chains would show this; harmless to the model (PC=64 is inside the {53,64} PASS set) |
| Site CW = **PC=24 (single)** | **LOW_PROBABILITY** | would require a CW change to single-precision somewhere on the init→site path — the canon's `unmeasured` field names the one candidate mechanism (the D3D8 FPU-mode change without D3DCREATE_FPU_PRESERVE, X4.4); the chains themselves contain no FLDCW (X4.3) and the 910-pair raw count is not a census (X4.3) — so it is possible, it is the load-bearing risk, and it is exactly what the measurement exists to decide |
| The RC field measures nearest-even | **MOST_LIKELY** (subordinate to the PC=53 forecast) | same documented-default basis; captured simultaneously — the design records it either way (W5.1's RC honesty bound) |

**No pre-commitment:** these are §16.4-labeled forecasts. The measurement — a single 16-bit register read at the sites — decides. Neither the design nor the execution may treat a forecast as fact before the capture (the profile's own wording).

---

## W7 — THE PACKAGE (cross-reference)

- **This document** (W1-W6) = `05_ANALYSIS\EXPERIMENT_DESIGN.md`.
- **The design checklist** (the pre-flight steps + the GO-gate items) = `05_ANALYSIS\DESIGN_CHECKLIST.md`.
- **The composition record** (which canon facts compose the design + their evidence pointers) = `05_ANALYSIS\COMPOSITION_RECORD.md`.
- **The canon extracts** (verbatim, with pointers) = `03_STATIC\CANON_EXTRACTS.md`.
- **The not-executed record** = `04_RUNTIME\NOT_EXECUTED.md` (this run executes NO runtime).
- **The lock record** = `01_RAW\pre_run_locks_hashes.json`; **the manifest** = `00_CONTROL\RUN_MANIFEST.json`.
- **The report + handoff** = `06_REPORT\00_FINAL_REPORT.md` + `06_REPORT\HANDOFF.md`; **the index** = `artifact_index.csv`.
- **The repo mirror** = `docs\audits\PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209\** in eudoria-clean (the ONLY commit scope; AUDIT_ENTRYPOINT.md out of scope).
