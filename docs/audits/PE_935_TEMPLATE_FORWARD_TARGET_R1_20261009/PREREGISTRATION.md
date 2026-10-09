# PREREGISTRATION — PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

- **RUN_ID**: PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009
- **RUN_CLASS**: BOUNDED_STATIC_FORWARD_TARGET_MICRO
- **Executor**: pe-reconstruction, dispatched by PE-MASTER under the human-authorized
  frozen contract delivered in-session 2026-10-09.
- **NO_NESTED_TASKS**: no agent launches. No commit/push (publication is a separate
  later phase). No MANIFEST/QC_REPORT (fresh QC + persistence are later phases).
  No AUDIT_ENTRYPOINT.md modification.
- **RECORDS**: STATIC_ONLY — the client never runs. Every finding is labeled with an
  evidence maturity level (IDENTITY / BYTE_OBSERVATION / STRUCTURE / RELATION).
  No MECHANISM and no RUNTIME claims anywhere in this package.
- **Binary**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — EXPECTED 8,015,872 B /
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
  ERA: PCG/EU 9.3.5 client. Addresses are VAs (image base 0x00400000 hypothesis,
  re-verified from the PE header this run). Re-hash BEFORE all work (done, PASS,
  measured = expected) and AFTER all work.
- **Git**: repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; BASE_SHA
  cea10e9cfcaa2e814f5cfe4269fd2a6a409d54da; live ls-remote re-verified this run
  (HEAD == remote master == BASE). No tracked-file modification by this run.
- **This file is written BEFORE any of the science below is executed.**

## 1. THE PRE-REGISTERED QUESTION (from the frozen contract, verbatim intent)

Trace the next bounded step in the template-registry consumer chain. Primary subjects:
FUN_007CE1E0 and FUN_0040B070. Relevant caller anchors: FUN_00511070 / CALL 0x00511259;
FUN_006C3F50 / CALL 0x006C3F74; FUN_006C3F50 / CALL 0x006C3FB5; subsequent reads
0x006C3FBE and 0x006C3FC1. The objective is NOT to recover coordinates at any cost.
The objective is to establish whether the template pointer is:
(1) dereferenced; (2) converted to another object; (3) used as a key or handle;
(4) stored or forwarded; (5) connected to a runtime object identity;
(6) connected to a demonstrable transform-relevant operation.

NO runtime claims; NO XYZ recovery claims. All previously established science statuses
remain unchanged unless new independent evidence justifies promotion (none is presumed).

### Prior-evidence hypothesis status (to be RE-VERIFIED from physical bytes, never inherited)
- FUN_0072F580 = template-registry lookup returning the template object in EAX from the
  registry map; not-found sentinel = 0x00BA5800 — HYPOTHESIS from predecessor package
  PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009. Byte re-pin REQUIRED (W-E1).
- FUN_0043A550 = lazy registry singleton getter — HYPOTHESIS. Byte re-pin REQUIRED (W-E2).
- FUN_00511070 window bounds 0x00511070–0x0051152B and callsite triple
  0x0051124B (getter) / 0x00511252 (lookup) / 0x00511259 (subject CALL to FUN_007ce1e0) —
  HYPOTHESIS. Byte re-pin REQUIRED (W-A).
- FUN_006C3F50 window bounds 0x006C3F50–0x006C3FDB and the callsites
  0x006C3F5B / 0x006C3F62 / 0x006C3F74 / 0x006C3FB5 + reads 0x006C3FBE / 0x006C3FC1 —
  HYPOTHESIS. Byte re-pin REQUIRED (W-B).
- FUN_007CE1E0 and FUN_0040B070 bodies = the primary subjects of THIS run — no prior
  byte analysis exists (predecessor kept both bodies CLOSED). Bounds UNKNOWN at
  pre-registration; determined under the pre-registered body-end rule + cap.

## 2. DEFINITIONS / DISTINCTIONS (preserved VERBATIM all run)

- template definition 4057 -> model 218757 is a definition/resource relation,
  NOT a world instance.
- sids string-table id 4057 is a DIFFERENT namespace (label UNRECONCILED between prior
  records; do not cite either label as resolved).
- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED.
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED.
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED.
- WORLD_XYZ_RECOVERED = NO.
- No XYZ/placement/building-instance promotion. A negative result is acceptable and
  MUST be reported without optimization toward a positive finding.
- POINTER VALUE identity (same address in a register) and POINTEE CONTENTS identity
  (same object) are distinguished all run.
- 0x0085B1B0 / 0x0095D3C4 bodies remain CLOSED this run (contract FORBIDDEN).

## 3. PRE-REGISTERED PASS/FAIL GATES

- **G1 ANCHORS_REPINNED**: every subject and anchor VA re-pinned from physical bytes at
  its exact VA (function entry prologue present; each named callsite instruction is a
  CALL-class instruction whose rel32 target recomputes to the claimed target).
  Any identity mismatch = HARD_STOP.
- **G2 EDGES_CLASSIFIED**: each of the 3 subject callsites has a Phase-1
  POINTER_IDENTITY classification in {POINTER_IDENTITY_CONFIRMED, _CONDITIONAL,
  _UNKNOWN, _REJECTED} with byte-anchored evidence, register-state trace, and
  intervening-call census.
- **G3 CALLEE_CENSUSED**: FUN_007CE1E0 and FUN_0040B070 analyzed within the
  pre-registered windows; EVERY access to template-derived memory recorded with the
  11-field census row (instruction VA / original opcode bytes / effective address /
  base pointer provenance / offset / access width / read-write direction / consumer
  operation / control-flow dependencies / confidence / evidence status). No field is
  named position/rotation/scale/transform/world-coordinate without independent
  geometric evidence — UNKNOWN preserved.
- **G4 DERIVED_OBJECT_ADJUDICATED**: the FUN_0040B070 result @0x006C3FB5 tracked to
  reads 0x006C3FBE ([EAX+4]) and 0x006C3FC1 ([EAX]); DERIVED_OBJECT_IDENTITY and
  TRANSFORM_SEMANTICS adjudicated honestly (UNKNOWN / UNVERIFIED are acceptable).
- **G5 FALSIFIERS_EXECUTED**: all 8 contract falsifiers designed, executed, recorded
  (FALSIFIER_RESULTS.json); every meaningful PASS has MEASURED_QUANTITY /
  INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.
- **G6 IDENTITY**: EXE SHA256 unchanged before/after; predecessor package
  PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009 byte-unchanged (all 25 package files
  re-hashed before AND after against its persisted MANIFEST_SHA256.csv rows); no
  tracked repo file modified; zero .pyc residue created by this run (python -B;
  final scan of this run's own locations).
- **G7 NO_PROMOTION**: zero XYZ/placement/building-instance claims; every finding
  labeled with its evidence maturity level; claim limits preserved verbatim.

Non-pass classes: BUDGET_EXHAUSTED (honest stop), WINDOW_TRUNCATED (honest label,
analysis continues within the cap), NOT_CHECKED (explicit + reason only).

## 4. PRE-REGISTERED WINDOWS + BYTE BUDGETS (declared BEFORE analysis)

| # | Window | Entry VA | Purpose | Cap | Rule |
|---|--------|----------|---------|-----|------|
| W-A | FUN_00511070 (caller 1) | 0x00511070 | Phase 1 edge 0x00511259 (+lookup chain 0x0051124B/0x00511252) | 0x600 B from entry | body-end rule §5 |
| W-B | FUN_006C3F50 (caller 2) | 0x006C3F50 | Phase 1 edges 0x006C3F74, 0x006C3FB5; Phase 3 reads 0x006C3FBE/0x006C3FC1 | 0x200 B from entry | body-end rule §5; +16 B padding context past end |
| W-C | FUN_007CE1E0 (PRIMARY SUBJECT 1) | 0x007CE1E0 | Phase 2 callee field-access census | 0x1000 B from entry | body-end rule §5 |
| W-D | FUN_0040B070 (PRIMARY SUBJECT 2) | 0x0040B070 | Phase 2 census + Phase 3 derived-object identity | 0x1000 B from entry | body-end rule §5 |
| W-E1 | FUN_0072F580 (lookup — bounded dependency) | 0x0072F580 | Phase 1 load-bearing assertion: what EAX holds at lookup return (template pointer vs sentinel 0x00BA5800) | 0x80 B from entry | body-end rule §5 |
| W-E2 | FUN_0043A550 (getter — bounded dependency) | 0x0043A550 | Phase 1 load-bearing assertion: source of ECX (getter returns registry singleton) | 0xC0 B from entry | body-end rule §5; FUN_0095d3c4 call edge recorded, its body stays CLOSED (contract FORBIDDEN) |
| W-F | sentinel datum 0x00BA5800 | 0x00BA5800 | Falsifier-2 support: static byte content of the sentinel location | 16 B data dump | PE-mapped data read (if beyond raw size, record zero-initialized-tail honestly) |

**Bounded-dependency justification (W-E1/W-E2)**: the Phase-1 POINTER_IDENTITY
classifications are load-bearing on (a) EAX content at the lookup CALL's return and
(b) ECX provenance one instruction earlier. Without re-opening these two small bodies
(predecessor sizes 46 B / 119 B) inside their caps, the identity chain would rest on
inherited decompiler output — exactly what the contract forbids. No other callee body
is opened.

**All other callees visible in any window stay CLOSED** (call edges recorded only;
callee names in decompiler output are NOT identity evidence). No new decode beyond the
windows above. No recursive opening.

Total decode budget: <= 0x29D0 B (~10.7 KB) of instruction bytes + 16 B data.

## 5. BODY-END RULE (documented BEFORE analysis; trap L24 respected)

For each function window: decode forward from the entry following the actual
instruction stream. The window END is the first RET-family instruction (C3 / C2 imm16)
that terminates the function body, established by requiring the bytes after it to be
alignment padding (90 / CC / int3) or the next function's prologue at a plausible
function boundary. NEVER end a window at the last observed use (L24). If control flow
jumps beyond the cap, or the end cannot be established within the cap, the window is
labeled WINDOW_TRUNCATED and the analysis continues only within the decoded prefix —
recorded honestly, never silently extended.

## 6. PRE-REGISTERED METHODS

- **Own decoder (primary truth)**: a fresh pure-Python x86-32 decoder written in
  SCRATCH (no external disassembly library; capstone NOT installed, none installed).
  Reads physical bytes through my own PE parser (VA→file-offset mapping from the PE
  header). Every window decoded byte-exactly. Instruction-boundary calibration:
  any disagreement with objdump = decoder defect to be fixed BEFORE analysis
  proceeds (agreement then re-measured).
- **objdump (independent verification)**: GNU objdump 2.44 (WSL Debian binutils),
  `objdump -D -b binary -m i386 -M intel --adjust-vma=<window VA>` on raw byte slices
  extracted at PE-mapped file offsets from the PHYSICAL EXE. Independent instruction
  boundaries + call targets.
- **Ghidra (hypothesis generator ONLY)**: REUSE of the existing LANDMARK4057 project
  at D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\proj
  (disclosed; its imported sandbox Entropia.exe re-hashed this run:
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 = expected, PASS).
  -noanalysis processing + postScripts exporting decompile + listing for W-A..W-E.
  Ghidra decompiler types/signatures/names are HYPOTHESES, never identity evidence.
  Physical bytes outrank pseudocode (contract Phase 4).
- **Dataflow reconstruction**: manual register-state tracing over the dual-verified
  instruction stream, with x86 ABI discipline (EAX/ECX/EDX volatile; EBX/ESI/EDI/EBP
  callee-saved) — applied to every intervening call.

## 7. PRE-REGISTERED FALSIFIERS (Phase 4 — each designed before execution)

| # | Falsifier (contract) | Design (pre-registered) |
|---|----------------------|--------------------------|
| F1 | ECX does not contain the lookup result at the subject CALL | byte-trace every instruction between the lookup CALL return and each subject CALL; enumerate every write to ECX and every intervening CALL (volatility audit). FAIL confirmed if any ECX producer other than the lookup-return chain exists unaccounted. |
| F2 | the pointer equals the not-found sentinel | re-pin the lookup's not-found path; identify where the sentinel value 0x00BA5800 enters EAX; classify each edge CONDITIONAL on the sentinel case unless the not-found path is unreachable in-window. |
| F3 | a supposed field access actually belongs to another object | for every [reg+off] operand in W-C/W-D, track the base register's provenance to its producing instruction; a base that is NOT the template-derived register = different object — recorded. |
| F4 | a float value is misclassified as a coordinate | NO field is named position/rotation/scale/transform/world-coordinate on float-or-vector-shape evidence alone; every float/vector-shaped structure in the census keeps semantics UNKNOWN unless independently evidenced. This falsifier PASSES by demonstrating the discipline, not by finding coordinates. |
| F5 | a call destroys a register value assumed preserved | for every dataflow hop that crosses a CALL: check whether the carried register is volatile (EAX/ECX/EDX) — if yes, the hop is INVALID unless reloaded after the call; callee-saved registers audited against the callee prologue/epilogue. |
| F6 | a return value is incorrectly attributed to the template | where multiple CALLs exist between producer and consumer, attribute EAX uses to the most recent CALL with no intervening EAX writer; byte-anchored. |
| F7 | a claim depends only on Ghidra's inferred type | every load-bearing claim must cite my own decoder + objdump agreement; Ghidra-only claims are downgraded to HYPOTHESIS and excluded from gates. |
| F8 | a call target or instruction boundary is incorrect | dual-decoder agreement requirement: my decoder vs objdump on every window (boundary-by-boundary); every CALL rel32 target recomputed from its own opcode bytes and cross-checked; disagreement = defect fixed + re-measured before analysis proceeds. |

Every meaningful PASS requires: MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.

## 8. PRE-REGISTERED OUTPUTS (deliverables)

PREREGISTRATION.md (this file) / INPUT_IDENTITIES.json / CALL_EDGE_PROVENANCE.json /
POINTER_DATAFLOW.json / CALLEE_FIELD_ACCESS_CENSUS.json / FALSIFIER_RESULTS.json /
FINAL_REPORT.md / EVIDENCE_INDEX.md / HANDOFF.md; raw evidence under 01_RAW\
(own decoder outputs, objdump listings with bytes, Ghidra exports labeled as
hypotheses). No proprietary original game payloads in the package (text/metadata
only). No MANIFEST, no QC_REPORT (later phases).

## 9. HARD STOPS (pre-registered)

- EXE SHA256 mismatch at any check (before/after) — HARD_STOP.
- Identity mismatch of any pinned anchor (G1) — HARD_STOP.
- Budget exhaustion (a required window cannot be decoded within its cap) — honest
  stop class BUDGET_EXHAUSTED (recorded; never silently exceeded).

## 10. FORBIDDEN (acknowledged)

Runtime/network experiments; opening 0x0085B1B0 / 0x0095D3C4; physical
NIF/GLB/ARK/VFS/BNT reads; modifying historical packages or AUDIT_ENTRYPOINT.md;
new decode beyond the pre-registered windows; .pyc residue (python -B discipline);
any XYZ/placement/building-instance promotion; commits/pushes.

## 11. INTERVENTION LEDGER (expected NONE — STATIC_ONLY)

Any deviation (tool restart, decoder repair, Ghidra project reuse details, file
operations beyond declared) is disclosed here and in HANDOFF.md. Ghidra project reuse
is pre-declared (§6) and is NOT counted as an intervention; everything else must be
recorded truthfully.
