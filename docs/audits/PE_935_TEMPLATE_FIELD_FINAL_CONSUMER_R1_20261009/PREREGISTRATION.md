# PREREGISTRATION — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

- **RUN_ID**: PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009
- **RUN_CLASS**: BOUNDED_STATIC_FIELD_CONSUMER_MICRO (STATIC_ONLY — the client never runs)
- **Executor**: pe-reconstruction, dispatched by PE-MASTER under the HUMAN-AUTHORIZED frozen
  contract delivered in-session 2026-10-09. NO_NESTED_TASKS. No commit/push; no MANIFEST/QC_REPORT
  (fresh QC + persistence are later phases owned by others); no AUDIT_ENTRYPOINT.md modification.
- **RECORDS**: STATIC_ONLY. Every finding carries an evidence maturity level
  (IDENTITY / BYTE_OBSERVATION / STRUCTURE / RELATION). No MECHANISM and no RUNTIME claims.
- **Binary**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (PCG/EU 9.3.5). EXPECTED
  8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
  Re-hash BEFORE all work (done in Phase 0, PASS, measured = expected) and AFTER all work.
  Addresses are VAs; image base 0x00400000 re-measured from the PE header this run (my own
  parser: machine 0x014C, opt magic 0x010B, .text RVA 0x1000/roff 0x1000, .rdata RVA 0x675000,
  .data RVA 0x76C000, .tls RVA 0x7AA000, .rsrc RVA 0x7AB000 — all re-measured, none copied).
- **Git**: repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; BASE_SHA
  fbb6e958ab8b950406a3c34364662925bca75a4e == HEAD == origin/master == live ls-remote master
  (all four re-verified this run). No tracked-file modification by this run.
- **This file is written BEFORE the dual-verified science (Phases 1–3) is executed.**

## 1. THE PRE-REGISTERED QUESTION (from the frozen contract, verbatim intent)

PRIMARY SUBJECT: FUN_006C3640. ANCHOR CALL: 0x006C3FCD (in FUN_006C3F50). Determine the ACTUAL
operations performed on the three forwarded values arg2=[P+0x14], arg3=[P+0x18], arg6=[P+8]
(their P+… provenance labels are the predecessor's byte-proven chain, re-verified this run via
the bounded dependencies W-DEP1/W-DEP2); ALSO classify arg5 = 0x008BD720 WITHOUT assuming it is
a transform, callback or world-object reference. Determine whether the consumer performs:
(1) direct memory writes; (2) object construction/initialization; (3) registration or callback
dispatch; (4) data validation or container management; (5) additional value forwarding;
(6) any independently evidenced transform-relevant operation.

**If FUN_006C3640 is a utility, callback or registry handler rather than a world-placement
consumer — REPORT THAT NEGATIVE RESULT EXPLICITLY. Do NOT recursively chase the chain.**

NO runtime claims; NO XYZ recovery claims. A negative result is acceptable and MUST be reported
without optimization toward a positive finding.

### Recon-derived working hypotheses (Phase-0 boundary scan; to be dual-verified, NEVER trusted)

The Phase-0 preflight (contract-ordered anchor re-pin + body-extent determination under the
documented body-end rule) produced raw objdump listings of the two windows. From those raw
bytes ONLY, these working hypotheses are declared BEFORE analysis; every one of them is subject
to dual-decode + falsifier execution and may be corrected by the science:

- H1: FUN_006C3640 is a small (~105 B) loop body over a range [arg2, arg3) with stride 0x20.
- H2: an indirect call `CALL EBX` (arg5 = 0x008BD720) is executed per element with ECX = element.
- H3: an 8-byte pair from the callback result is appended to a container derived from arg4
  ([esi+4] cursor / [esi+8] end; growth via a call to 0x006C2E00 when cursor == end).
- H4: arg6 ([P+8]) is pushed by the caller but never read by the callee.
- H5: FUN_006C3640 returns with EAX = arg1 and writes the container pointer to *arg1 on both paths.
- H6: the consumer is a generic range-collect/map utility — the NEGATIVE result (not a
  world-placement consumer) is the expected honest outcome.

NONE of these hypotheses names any field a position/rotation/scale/coordinate/transform.

## 2. DEFINITIONS / DISTINCTIONS (preserved VERBATIM all run)

- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED.
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED.
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED.
- WORLD_XYZ_RECOVERED = NO.
- P = the template-registry lookup return (FUN_0072F580), inherited from the predecessor chain;
  its POINTEE IDENTITY vs the registry node is UNRESOLVED_UPSTREAM and is NOT re-adjudicated
  this run. "[P+0x14]" etc. denote the byte-proven pointer-arithmetic chain (lookup result + 0x14),
  not a resolved object semantics.
- P may be the not-found sentinel 0x00BA5800 (predecessor byte-fact: static all-zero .data tail);
  every consumer claim carries this condition explicitly (the zero-filled sentinel makes
  [P+0x14] == [P+0x18] == 0, i.e. the empty path — recorded as the conditional branch outcome).
- 0x0085B1B0 / 0x0095D3C4 bodies remain CLOSED (contract FORBIDDEN).
- Template definition 4057 → model 218757 is a definition/resource relation, NOT a world instance.

## 3. PRE-REGISTERED PASS/FAIL GATES

- **G1 ANCHORS_REPINNED**: the anchor CALL @0x006C3FCD rel32 recomputes to 0x006C3640 from its
  own opcode bytes; every argument-setup instruction re-pinned at its exact VA from physical
  bytes; W-DEP1/W-DEP2 bodies re-pinned; window body-ends established by the documented rule.
  Any identity mismatch = HARD_STOP.
- **G2 ARGUMENT_PROVENANCE**: full argument table for the anchor call (slot #, push VA, source
  register/instruction chain, value, width, push order) + calling convention evidence
  (who cleans the stack: callee RET imm16 vs caller ADD ESP,imm) + width/order verification
  from the actual pushes. Inherited arg numbering is NOT trusted; slots are re-derived.
- **G3 BODY_CENSUSED**: full CFG of FUN_006C3640 within W-SUBJ; EVERY access to the four
  tracked values (arg2/arg3/arg6/arg5) recorded with the full field set: VA / opcode bytes /
  effective address / base provenance / offset / width / direction / consumer operation /
  control-flow dependency / evidence status. Census runs over the FULL window incl. the
  empty path (L24 discipline).
- **G4 DISPOSITIONS**: each tracked value tracked to its final in-window disposition
  (written to memory / forwarded to a callee (edge CLOSED) / compared / discarded),
  with evidence; what 0x008BD720 IS classified from BEHAVIOR + bytes.
- **G5 FALSIFIERS_EXECUTED**: all 8 contract falsifiers designed, executed, recorded with
  MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.
- **G6 IDENTITY**: EXE SHA256 unchanged before/after; predecessor package
  PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009 byte-unchanged (all 27 manifest rows re-hashed
  BEFORE and AFTER, 0 mismatches); zero tracked repo file modified; zero .pyc residue
  (python -B; final scan of this run's own locations).
- **G7 NO_PROMOTION**: zero XYZ/placement/building-instance claims; all findings era-labeled
  (PCG 9.3.5); claim limits preserved verbatim; the utility/negative verdict reported honestly.

Non-pass classes: BUDGET_EXHAUSTED (honest stop), WINDOW_TRUNCATED (honest label),
NOT_CHECKED (explicit + reason only).

## 4. PRE-REGISTERED WINDOWS + BYTE BUDGETS (declared BEFORE the dual-verified decode)

| # | Window | Bounds (VA) | Purpose | Byte budget | Rule |
|---|--------|------------|---------|-------------|------|
| W-SUBJ | FUN_006C3640 (PRIMARY SUBJECT) | 0x006C3640–0x006C36A8 (105 B) | Phase 2 body analysis, CFG, census | 105 B, cap 64 instructions | body-end rule §5 |
| W-CALLER | FUN_006C3F50 (anchor caller) | 0x006C3F50–0x006C3FDB (140 B) | Phase 1 argument provenance + anchor identity | 140 B, cap 64 instructions | body-end rule §5 |
| W-DEP1 | FUN_0040B070 body (bounded dependency) | 0x0040B070–0x0040B073 (4 B) | load-bearing for arg2/arg3 value provenance (EAX = P+0x14) | 4 B | body-end rule §5 |
| W-DEP2 | FUN_007CE1E0 body (bounded dependency) | 0x007CE1E0–0x007CE1E3 (4 B) | load-bearing for arg6 value provenance (EAX = [P+8]) | 4 B | body-end rule §5 |
| W-ANCHOR | 0x008BD720 datum (bounded dependency) | 16 B data read at VA 0x008BD720 | arg5 identity classification (code vs data) from BYTES; NO decode of any body at/after this VA | 16 B data | PE-mapped data read only |

- Body-end rule verification (Phase-0 boundary scan, to be re-confirmed by dual decode):
  W-SUBJ ends at RET C3 @0x006C36A8 followed by 6×CC padding (0x006C36A9–0x006C36AF) and the
  next function prologue at 0x006C36B0. W-CALLER ends at RET C3 @0x006C3FDB followed by 4×CC
  and the next function prologue at 0x006C3FE0.
- **Bounded-dependency justifications**: W-DEP1/W-DEP2 — the contract requires re-deriving
  which stack slot carries which VALUE; the value chains cross two 4-byte callee bodies
  (predecessor byte-proved them; 4 bytes each — the minimal necessary re-verification).
  W-ANCHOR — the contract's primary mandate classifies 0x008BD720 from BEHAVIOR + bytes;
  behavior is established in-window; 16 raw bytes distinguish code-entry from data.
  All three are explicitly preregistered bounded dependencies; NO other callee is opened.
- **Total decode budget: 253 B of code + 16 B of data. No decode beyond these windows.**
  Budget exhaustion is recorded honestly (BUDGET_EXHAUSTED), never silently exceeded.

## 5. BODY-END RULE (documented BEFORE analysis; trap L24 respected)

For each function window: decode forward from the entry following the actual instruction
stream. The window END is the first RET-family instruction (C3 / C2 imm16) that terminates
the function body, established by requiring the bytes after it to be alignment padding
(90 / CC / int3) or the next function's prologue at a plausible function boundary. NEVER end
a window at the last observed use (L24). Censuses run over the FULL window. If control flow
jumps beyond the window, or the end cannot be established within the cap, the window is
labeled WINDOW_TRUNCATED and analysis continues only within the decoded prefix.

## 6. PRE-REGISTERED METHODS

- **Own decoder (primary truth)**: a fresh pure-Python x86-32 decoder written this run in
  SCRATCH (no external disassembly library; capstone NOT installed, none installed). Reads
  physical bytes through my own PE parser (VA→file-offset from the PE header — including the
  ImageBase/RVA distinction, after my Phase-0 extraction defect (comparing VA against section
  RVA ranges) was caught and fixed BEFORE any science). Instruction-boundary calibration:
  any disagreement with objdump = decoder defect to be fixed BEFORE analysis proceeds
  (agreement then re-measured). All defects disclosed in the intervention ledger.
- **objdump (independent verification)**: GNU objdump (Debian binutils) via WSL,
  `-D -b binary -m i386 -M intel --adjust-vma=<window VA>` on raw byte slices extracted at
  PE-mapped file offsets from the PHYSICAL EXE (slice SHA256s recorded). Independent
  instruction boundaries + call/jump targets.
- **Ghidra (hypothesis generator ONLY)**: REUSE of the existing LANDMARK4057 project at
  D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\proj
  (disclosed; its imported sandbox Entropia.exe re-hashed this run = physical, PASS).
  -noanalysis processing + postScript exporting decompile/listing for the windows.
  Ghidra decompiler types/signatures/names are HYPOTHESES, never identity evidence.
  Physical bytes outrank pseudocode (contract Phase 4).
- **Dataflow reconstruction**: manual + machine-assisted register-state tracing over the
  dual-verified instruction stream, with x86 ABI discipline (EAX/ECX/EDX volatile;
  EBX/ESI/EDI/EBP callee-saved) — applied to every intervening call; every callee-saved
  assumption is recorded as an explicit ABI-assumption condition (callee bodies CLOSED).

## 7. PRE-REGISTERED FALSIFIERS (Phase 3 — designed before execution)

| # | Falsifier (contract) | Design (pre-registered) |
|---|----------------------|--------------------------|
| F1 | an argument slot attribution is wrong (value swapped between slots) | re-derive every slot from BOTH sides: the caller's push order/registers AND the callee's actual [esp+disp] read offsets (slot arithmetic under the live push depth); a swap breaks the callee-side read map — machine cross-check required to agree on all 6 slots. |
| F2 | a supposed field access belongs to another object (wrong base register) | for every memory operand in W-SUBJ: base register provenance chain back to its producer; accesses derived from the container (ESI/arg4) or the callback result (EAX) must not be attributed to the tracked template values; the tracked values themselves must not be dereferenced by an access whose base is not their carrying register. |
| F3 | a float-shaped value is misclassified as a coordinate (discipline check) | machine scan for FPU (D8–DF) / SSE (0F 10/11/28/29…, F2/F3-prefixed) opcodes in W-SUBJ and W-CALLER; NO field named position/rotation/scale/transform/world-coordinate regardless of value shape; this falsifier PASSES by demonstrating discipline, not by finding coordinates. |
| F4 | a call destroys a register assumed preserved | for every dataflow hop crossing CALL EBX (0x008BD720) or CALL 0x006C2E00: volatile (EAX/ECX/EDX) vs callee-saved (EBX/ESI/EDI/EBP) audit; the callee-saved assumption is recorded as an explicit ABI-assumption condition (bodies CLOSED); compiler corroboration sought in-window (spill/reload pairs, symmetric prologue/epilogue). |
| F5 | a return value is incorrectly attributed | EAX-writer census between every producer and consumer (last-writer-wins); the growth-call (0x006C2E00) return must be machine-verified UNUSED before the next EAX writer; FUN_006C3640's own return value and its caller's use of it must be byte-verified. |
| F6 | a claim depends only on Ghidra's inferred type | every load-bearing claim cites own-decoder + objdump agreement; Ghidra-only statements are quarantined HYPOTHESES and excluded from gates. |
| F7 | instruction boundary error | byte-exact dual decode over every window; 0 boundary disagreements + 0 call/jump-target disagreements required (both recomputed from opcode bytes, not from labels); disagreement = defect fixed + re-measured before analysis proceeds. |
| F8 | wrong-object negative control (container ≠ template) | if any tracked value flows into a container/registration, verify the container's base provenance chain differs from the template pointer P's chain (P = lookup return; container = caller's param_2 vector / arg4) — machine-checked. |

Every meaningful PASS requires: MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.

## 8. PRE-REGISTERED OUTPUTS (deliverables)

PREREGISTRATION.md (this file) / INPUT_IDENTITIES.json / ARGUMENT_PROVENANCE.json /
BODY_CFG_AND_ACCESS_CENSUS.json / VALUE_DISPOSITION.json / ANCHOR_008BD720_CLASSIFICATION.json /
FALSIFIER_RESULTS.json / FINAL_REPORT.md / EVIDENCE_INDEX.md / HANDOFF.md; raw evidence under
01_RAW\ (own decoder output, objdump listings, Ghidra export quarantined as hypothesis).
No game payloads in the package (text/metadata only; raw .bin slices stay in SCRATCH).
No MANIFEST, no QC_REPORT (later phases).

## 9. HARD STOPS (pre-registered)

- EXE SHA256 mismatch at any check (before/after) — HARD_STOP.
- Anchor/callsite identity mismatch (G1) — HARD_STOP.
- Budget exhaustion (a required window cannot be decoded within its cap) — honest stop class
  BUDGET_EXHAUSTED (recorded; never silently exceeded).

## 10. FORBIDDEN (acknowledged, per contract)

Runtime/network experiments; opening 0x0085B1B0 / 0x0095D3C4 or any callee of FUN_006C3640
beyond the preregistered dependencies (W-DEP1/W-DEP2/W-ANCHOR — and W-ANCHOR is a 16 B data
read, NOT a body decode); physical NIF/GLB/ARK/VFS/BNT reads; modifying historical packages or
AUDIT_ENTRYPOINT.md; decode beyond the preregistered windows; .pyc residue (python -B);
ANY XYZ/placement/transform promotion; recursively chasing the chain past this consumer;
commits/pushes.

## 11. INTERVENTION LEDGER (expected NONE — STATIC_ONLY)

Any deviation (tool restart, decoder repair, Ghidra project reuse details, file operations
beyond declared) is disclosed here and in HANDOFF.md. Pre-declared and NOT counted as
interventions: the Phase-0 extraction defect (caught and fixed before science, disclosed in
§6), Ghidra project reuse (§6), objdump slice extraction into SCRATCH. Everything else must
be recorded truthfully.
