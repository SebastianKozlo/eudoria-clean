# HANDOFF — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

## MANDATORY HANDOFF BLOCK

- **AUDIT_OUTPUT_ROOT**:
  `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009\`
- **FINAL_REPORT_PATH**:
  `docs\audits\PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009\FINAL_REPORT.md`
- **PRIMARY_EVIDENCE_PATHS**:
  - `ARGUMENT_PROVENANCE.json` (anchor rel32 recompute + 6-slot table + cdecl proof + contract VA-annotation correction)
  - `BODY_CFG_AND_ACCESS_CENSUS.json` (10-block CFG, 17-row access census with base provenance, arg6 machine scan, FPU/SSE scan)
  - `VALUE_DISPOSITION.json` (per-value final dispositions + container dataflow summary)
  - `ANCHOR_008BD720_CLASSIFICATION.json` (identity class = CALL_TARGET; quarantined 0x18-thunk body-shape hypothesis)
  - `FALSIFIER_RESULTS.json` (8/8 falsifiers, 4-part requirement each)
  - `INPUT_IDENTITIES.json` (EXE/git/predecessor/toolchain identities before+after)
  - `01_RAW\OWN_DECODER_WINDOWS.json` (own decoder output, all 4 windows; F7 gate 0/105; F3 scan 0/0)
  - `01_RAW\ESP_SLOT_MAP.json` (CFG-worklist depth sim, asserted merges/RETs, both G/L split variants)
  - `01_RAW\KEY_REGION_LISTINGS.md` (dual-verified annotated listings)
  - `01_RAW\ANCHOR_008BD720_16B_DUMP.json` (raw 16 B at the anchor, NO decode)
  - `01_RAW\GHIDRA_HYPOTHESIS_EXPORT.json` (quarantined hypotheses only)
  - `01_RAW\OBJDUMP_LISTINGS\` (independent GNU objdump listings, 4 files)
- **RUN_STATUS**: **COMPLETE** (all preregistered windows decoded within budget — 253 B code + 16 B data; all 7 gates PASS; no scope expansion; the contract's negative-result branch applies and is reported explicitly)
- **HARD_STOP_REASON**: NONE (EXE SHA256 identical before/after — 3 checks; anchor identity recomputed and confirmed — CALL 0x006C3FCD rel32 → 0x006C3640; no budget exhaustion)
- **EXE SHA256 before**: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B)
- **EXE SHA256 after**: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (identical; size unchanged)
- **Git**: HEAD == origin/master == live ls-remote master == BASE fbb6e958ab8b950406a3c34364662925bca75a4e before AND after; zero tracked files modified; zero commits/pushes; only this package (untracked) created.

## ARGUMENT-SLOT TABLE (machine-verified from BOTH sides; cdecl, caller-cleans ADD ESP,0x18)

| Slot | Push @VA | Source chain (byte-pinned) | Value |
|---|---|---|---|
| arg1 | 0x006C3FCC | ECX ← LEA [ESP+0x30] @0x006C3FC8 | &caller's param_2 slot (out-slot address) |
| arg2 | 0x006C3FC7 | EAX ← [EAX] @0x006C3FC1 ← CALL 0x0040B070 (W-DEP1 `LEA EAX,[ECX+0x14]; RET`) | [P+0x14] |
| arg3 | 0x006C3FC6 | EDX ← [EAX+4] @0x006C3FBE (same EAX = P+0x14) | [P+0x18] |
| arg4 | 0x006C3FC5 | ESI ← [ESP+0x1C] @0x006C3F79 = caller's param_2 | caller-owned vector (container) |
| arg5 | 0x006C3FC4 | EBX ← MOV EBX,0x008BD720 @0x006C3FB0 | 0x008BD720 (code address) |
| arg6 | 0x006C3FC3 | ECX ← [ESP+0x10] @0x006C3FBA ← local @0x006C3F83 ← CALL 0x007CE1E0 (W-DEP2 `MOV EAX,[ECX+8]; RET`) | [P+8] |

Contract VA-annotation correction (F1 catch): push@0x006C3FC3 carries [P+8] (arg6), NOT [P+0x14];
[P+0x14] is pushed @0x006C3FC7 (arg2). Slot attributions themselves CONFIRMED as the contract stated.

## PER-VALUE DISPOSITION (arg2 / arg3 / arg6 / 0x008BD720)

- **arg2 = [P+0x14]**: consumed in-register as the loop BEGIN pointer of a 0x20-stride element
  range and as the per-element callback receiver source (ECX := EDI @0x006C3658). Never
  dereferenced, never stored, never forwarded as data. STRUCTURE: range begin.
- **arg3 = [P+0x18]**: consumed in-register as the loop END/limit (compared only @0x006C364A/
  0x006C368D). Never dereferenced, never stored. The pair ([P+0x14],[P+0x18]) is consumed as a
  RANGE — NOT promoted to vector/coordinate (0 FPU/SSE, machine-measured).
- **arg6 = [P+8]**: DEAD ARGUMENT in this consumer — NEVER READ (machine-verified: 0 of the
  window's 17 census rows (16 accesses + 1 LEA; 8 of them esp-relative) resolve to entry
  offset 0x18); discarded by the caller's ADD ESP,0x18.
  [P+8]'s real consumer in the chain is the caller-side (0x66, [P+8]) vector insert
  (@0x006C3F8D/F; growth @0x006C3FA9) — predecessor-established, re-pinned as caller context.
- **arg5 = 0x008BD720**: consumed as the INDIRECT CALL TARGET — `CALL EBX` @0x006C365A (FF D3),
  once per 0x20-stride element, thiscall (ECX = element), no stack args; the callback's return
  EAX is the 8-byte pair source appended to the arg4 container. IDENTITY CLASS = CALL_TARGET
  (function pointer, .text code address) from BEHAVIOR + BYTES; NOT a transform, NOT a
  world-object reference. Its body stays CLOSED; the byte-shape hypothesis (4-byte interior-
  pointer thunk returning ECX+0x18, same family as the byte-proven W-DEP1 `8D 41 14 C3`) is
  quarantined UNVERIFIED — needs a new bounded contract.

## CONSUMER CLASSIFICATION PER THE 6 CONTRACT QUESTIONS (FUN_006C3640, 105 B, STATIC_ONLY)

1. **Direct memory writes**: YES — pair stores @0x006C366A/0x006C366F into the container buffer
   (cursor from [arg4+0x4]); out-slot store *arg1 := container @0x006C3695 (loop) / @0x006C36A5 (empty).
2. **Object construction/initialization**: NO in-window (no allocation, no vtable write; the
   growth helper 0x006C2E00 MAY allocate internally — edge CLOSED, unresolved, recorded).
3. **Registration or callback dispatch**: YES — per-element indirect callback dispatch
   @0x006C365A (CALL EBX = arg5 = 0x008BD720, ECX = element); no other dispatch in-window.
4. **Data validation or container management**: YES — cursor/end compare @0x006C365F,
   null-cursor check @0x006C3664, 8-byte append + cursor advance @0x006C3672, growth delegation
   @0x006C3685, out-slot stores on both paths.
5. **Additional value forwarding**: YES — callback result pair → container/growth helper
   (@0x006C3681); container pointer → *arg1; &arg1-slot → growth helper (@0x006C367C);
   arg6 forwarded in but never consumed.
6. **Transform-relevant operation**: NOT_ESTABLISHED — zero FPU/SSE in all 105 instructions;
   only pointer arithmetic; no geometric evidence; NO promotion.

**VERDICT (explicit negative result per contract): FUN_006C3640 is a UTILITY — a generic
range-collect/map function (0x20-byte elements → per-element thiscall callback → 8-byte result
pairs appended to an output vector) — NOT a world-placement consumer. The placement question,
if any, lives inside the CLOSED callee 0x008BD720; it was NOT chased.**

## ALL FALSIFIERS — OUTCOMES (FALSIFIER_RESULTS.json for the 4-part requirements)

1. **F1 (argument slot swapped)**: EXECUTED, PASS — 6/6 slots dual-side machine-verified;
   CAUGHT the contract's VA-annotation imprecision (push@0x006C3FC3 = [P+8]/arg6).
2. **F2 (wrong base register)**: EXECUTED, PASS — 17-row census, all base provenance byte-pinned;
   tracked values never dereferenced; callback-result reads kept out of the template census.
3. **F3 (float misclassified as coordinate)**: EXECUTED, PASS by discipline — 0 FPU/SSE
   (machine scan); the [P+0x14],[P+0x18] pair classified as a RANGE by operation evidence.
4. **F4 (call destroys assumed-preserved register)**: EXECUTED, PASS with recorded conditions —
   all loop-carried state is callee-saved-class across the two CLOSED calls; ABI-assumption
   conditions recorded explicitly (not waived); frame-balance derivations independent.
5. **F5 (return value misattributed)**: EXECUTED, PASS — per-path last-writer-wins census;
   growth-call return machine-verified UNUSED; subject returns EAX = arg1, caller ignores it.
6. **F6 (Ghidra-only claim)**: EXECUTED, PASS — zero load-bearing Ghidra claims; 3 artifacts
   quarantined (5-param signature hiding the dead arg6; FUN_008bd720 name; corroborating
   decompile excluded from gates).
7. **F7 (boundary/target error)**: EXECUTED, PASS — 0 disagreements over 105 instructions
   (own decoder vs GNU objdump); anchor rel32 recomputed == 0x006C3640; defect history
   disclosed (4 defects, all caught before conclusions, fixed, re-run, re-measured).
8. **F8 (wrong-object negative control)**: EXECUTED, PASS — container (caller's param_2 chain)
   and template P (lookup chain) provenance DISJOINT; only the closed-callee callback's result
   pair flows into the container, never the tracked template values.

## EVERY NOT_CHECKED ITEM (with reason)

- 0x008BD720 body (would confirm/refute the quarantined `LEA EAX,[ECX+0x18]; RET` hypothesis):
  NOT_CHECKED — callee CLOSED per preregistration; 16 raw bytes recorded only; needs a new
  bounded contract (4-byte dual decode).
- 0x006C2E00 body (would prove the growth append semantics internally): NOT_CHECKED — edge
  CLOSED; append inferred from in-window cursor arithmetic + the caller's parallel growth
  pattern (cross-callsite analogy, labeled as such).
- Getter/lookup cleanup split (which callee consumed the 4-byte key): split-invariance PROVEN
  for all downstream slot maps; the split itself is inherited context (predecessor byte-proof),
  NOT load-bearing, not re-adjudicated.
- Runtime behavior of any kind (element contents, callback results, container state, sentinel
  reachability): NOT_CHECKED — STATIC_ONLY (the client never ran).
- P's pointee contents / registry population path: NOT_CHECKED — UNRESOLVED_UPSTREAM as in the
  predecessors.
- 0x0085B1B0 / 0x0095D3C4 bodies: NOT_CHECKED — contract-FORBIDDEN; no in-window edges to them.
- sids-4057 namespace label: NOT_CHECKED — untouched, UNRECONCILED.

## INTERVENTION LEDGER (expected NONE — STATIC_ONLY; disclosed truthfully)

- **Pre-declared, NOT interventions** (PREREGISTRATION §6/§11): Ghidra LANDMARK4057 project
  reuse (-noanalysis + postScript; sandbox re-hashed = physical, PASS; the callee 0x008BD720
  was NOT decompiled — identity query only); objdump slice extraction into SCRATCH.
- **Tooling defects caught and fixed BEFORE any analysis conclusion (all disclosed in
  FALSIFIER_RESULTS F7)**: (1) PE parser VA-vs-RVA mapping defect in Phase-0 extraction (caught
  by the .rdata/.text inconsistency; fixed; slices re-extracted; re-hashed); (2) first decoder
  draft's grp1-imm dispatch design error (caught by self-review before first execution;
  rewritten); (3) ESP-depth sim v1 sign-convention + successor-depth bugs (caught by its own
  merge assertion at 0x006C368A; fixed; re-run; all assertions PASS); (4) a Jython
  Address-vs-int comparison bug in the Ghidra postScript (quarantine-side tooling; fixed;
  re-exported). No analysis conclusion was drawn from any defective intermediate state.
- **In-run script failures (honest)**: two PowerShell-inline-Python patch attempts failed on
  quoting (the known L23 trap); both were replaced by proper file edits. No analysis impact.
- **No other interventions**: no runtime/network experiments (the only network-adjacent
  operation was the contract-ordered read-only `git ls-remote` verification; nothing pushed);
  no package installations (capstone checked-absent, none installed); no tracked-file
  modification; no commits; no foreign untracked paths touched; no AUDIT_ENTRYPOINT.md touch;
  python -B throughout; final residue scan 0/0.

## CLAIM LIMITS (verbatim, unchanged)

- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- A negative result is acceptable and is reported without optimization toward a positive finding.

## 12-LINE SCIENTIFIC SUMMARY

1. FUN_006C3640 @0x006C3640 (105 B, dual-verified byte-for-byte) is a GENERIC RANGE-COLLECT/MAP UTILITY — NOT a world-placement consumer; that negative verdict is the contract's explicit negative-result branch, reported without optimization.
2. It receives (cdecl, caller-cleans): arg1 = &caller's param_2 slot (out-slot), arg2 = [P+0x14] (range begin), arg3 = [P+0x18] (range end), arg4 = the caller's vector (container), arg5 = 0x008BD720 (callback), arg6 = [P+8] (DEAD — never read; machine-verified 0 accesses to its slot).
3. [P+0x14] and [P+0x18] are consumed IN-REGISTER as the begin/end of a 0x20-stride element loop (CMP/JE @0x006C364A/0x006C364C; ADD EDI,0x20 @0x006C368A; CMP/JNE @0x006C368D/0x006C368F) — a RANGE, explicitly NOT promoted to vector/coordinate (0 FPU/SSE in all 105 instructions).
4. 0x008BD720's identity class = CALL_TARGET (function pointer, .text, called via `FF D3` CALL EBX @0x006C365A with ECX = the current element, thiscall, once per element) — from BEHAVIOR + BYTES; NOT a transform, NOT a world-object reference, NOT named.
5. The callback's return EAX is treated as an 8-byte pair source: [EAX] and [EAX+4] are copied into the arg4 container at its cursor ([arg4+0x4], pair stores @0x006C366A/0x006C366F, cursor += 8 @0x006C3672) or delegated to the growth helper 0x006C2E00 (CALL @0x006C3685; edge CLOSED; derived callee cleanup 20 B, frame-balance-proven).
6. Only the CLOSED-callee callback's result pair flows into the container — the tracked template values never reach memory as data; the container's provenance (caller's param_2) is machine-proven DISJOINT from the template pointer P's chain (falsifier F8).
7. Both paths end with *arg1 := container (@0x006C3695 loop-exit / @0x006C36A5 empty path — taken when [P+0x14] == [P+0x18], incl. the predecessor's sentinel case where both read 0); FUN_006C3640 returns EAX = arg1, which the caller ignores.
8. [P+8]'s real consumer in this chain is the caller's own (0x66, [P+8]) pair insert into its vector (@0x006C3F8D/F; growth @0x006C3FA9) — predecessor-established, re-pinned here as caller context; its forwarding as arg6 adds nothing.
9. The anchor call's rel32 recomputes from its own bytes (E8 6E F6 FF FF @0x006C3FCD → 0x006C3640) and the 6-argument slot table is machine-verified from BOTH sides (caller pushes × callee read offsets under the asserted ESP-depth sim); the contract's VA annotations were corrected (push@0x006C3FC3 = [P+8], not [P+0x14]) with slot attributions confirmed.
10. QUARANTINED HYPOTHESIS (no promotion, callee not decoded): the anchor's 4 leading bytes (8D 41 18 C3 + 12×CC) share the shape of the byte-proven W-DEP1 thunk family (8D 41 14 C3 = LEA EAX,[ECX+0x14]; RET) — IF decoded as that family, the container would collect the dwords at element+0x18/+0x1C (last 8 bytes of each 0x20-byte element); a 4-byte dual decode at 0x008BD720 needs a NEW bounded contract.
11. All 8 falsifiers executed PASS (F1 slot swap — caught the contract's VA imprecision; F2 wrong-object; F3 float discipline; F4 ABI-assumption conditions recorded; F5 return attribution incl. growth-return-unused; F6 Ghidra quarantined; F7 dual-decode 0/105; F8 container ≠ template); 4 tooling defects were caught pre-conclusion by the discipline machinery, fixed, re-run, disclosed.
12. Claim limits preserved verbatim (MODEL_218757_TO_CMO_JOIN / WORLD_INSTANCE_IDENTITY / HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO); all findings era-labeled PCG/EU 9.3.5, STATIC_ONLY, at BYTE_OBSERVATION/STRUCTURE/RELATION maturity; the client never ran.
