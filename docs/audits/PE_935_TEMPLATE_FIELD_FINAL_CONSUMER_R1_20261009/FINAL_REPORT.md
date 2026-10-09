# FINAL_REPORT — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

- **RUN_ID**: PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009
- **RUN_CLASS**: BOUNDED_STATIC_FIELD_CONSUMER_MICRO (STATIC_ONLY — the client never ran)
- **Executor**: pe-reconstruction, dispatched by PE-MASTER under the HUMAN-AUTHORIZED frozen
  contract delivered in-session 2026-10-09. NO_NESTED_TASKS. No commit/push; no MANIFEST/QC_REPORT
  (later phases); no AUDIT_ENTRYPOINT.md modification.
- **Binary**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (PCG/EU 9.3.5), 8,015,872 B,
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — re-hashed BEFORE
  (PASS), at Phase 0 (PASS) and AFTER all work (PASS), unchanged.
- **Git**: BASE fbb6e958ab8b950406a3c34364662925bca75a4e == HEAD == origin/master == live
  ls-remote master (all re-verified this run); zero tracked files modified; only this package
  (untracked) created; no commits, no pushes.
- **Method**: own fresh pure-Python x86-32 decoder + PE parser (primary truth) + CFG-worklist
  ESP-depth slot sim (merge- and RET-asserted); GNU objdump (Debian binutils, WSL) independent
  cross-verification — **F7 gate: 0 disagreements over all 105 window instructions, 0
  call/jump-target disagreements**; Ghidra 11.2.1 (reused LANDMARK4057 project, disclosed;
  sandbox EXE = physical hash, PASS) used ONLY as a hypothesis generator, fully quarantined.
  PREREGISTRATION.md written BEFORE the dual-verified science; all windows/budgets
  preregistered and respected (253 B code + 16 B data decoded, under the declared caps).

---

## 1. The question and the answer in one paragraph

The contract asked: what does FUN_006C3640 — the consumer of the anchor CALL 0x006C3FCD in
FUN_006C3F50 — actually DO with the three forwarded template-field values arg2=[P+0x14],
arg3=[P+0x18], arg6=[P+8], and what IS arg5=0x008BD720? **The answer: FUN_006C3640 is a
GENERIC RANGE-COLLECT/MAP UTILITY — a small (105 B) loop that iterates the 0x20-byte-element
array whose begin/end it receives in arg2/arg3, dispatches the per-element thiscall callback
it receives in arg5 (the indirect `CALL EBX` @0x006C365A, ECX = element), appends the
callback's 8-byte result pair to the output container it receives in arg4, and writes the
container pointer back to *arg1. arg2/arg3 are consumed in-register as loop bounds and are
NEVER dereferenced or stored; arg6 ([P+8]) is a DEAD ARGUMENT — pushed by the caller, NEVER
read by the callee (machine-verified); and 0x008BD720 is an INDIRECT CALL TARGET (code
address in .text), NOT a transform or a world-object reference. FUN_006C3640 is therefore
NOT a world-placement consumer — the contract's negative-result branch applies, and it is
reported explicitly. No recursive chain-chasing was performed: the callback body stays
CLOSED.**

## 2. Anchor and dependencies re-pinned (G1 PASS)

| Subject | Body (byte-pinned, preregistered body-end rule) | Bytes | Re-pinned facts |
|---|---|---|---|
| **CALL 0x006C3FCD** (anchor, in FUN_006C3F50) | — | `E8 6E F6 FF FF` | rel32 recomputed from its own bytes: 0x6C3FD2 − 0x992 = **0x006C3640** == subject entry (both decoders agree) |
| **FUN_006C3640** (primary subject) | 0x006C3640–0x006C36A8 (**105 B**, 47 insns) + 6×CC + next prologue @0x006C36B0 | dual-verified | RET C3 @0x006C36A8; both epilogues RET C3 (no imm16) → callee cleans nothing |
| **FUN_006C3F50** (anchor caller) | 0x006C3F50–0x006C3FDB (**140 B**, 54 insns) + 4×CC + next prologue @0x006C3FE0 | dual-verified | predecessor's 140 B claim CONFIRMED from physical bytes |
| **FUN_0040B070** (W-DEP1) | 0x0040B070–0x0040B073 (4 B) | `8D 41 14 C3` | `LEA EAX,[ECX+0x14]; RET` — interior-pointer thunk re-verified (arg2/arg3 value provenance) |
| **FUN_007CE1E0** (W-DEP2) | 0x007CE1E0–0x007CE1E3 (4 B) | `8B 41 08 C3` | `MOV EAX,[ECX+0x8]; RET` — getter re-verified (arg6 value provenance) |

Trap L24 respected: both windows end by the documented ret/padding rule and the censuses run
over the FULL window including the empty path.

## 3. Phase 1 — argument provenance (G2 PASS)

Calling convention (byte-derived): **cdecl, 6 dword stack args, caller-cleans** — callee RET C3
(no imm16) at both epilogues; `ADD ESP,0x18` @0x006C3FD2 (24 B = 6×4) immediately after the call.

Machine-derived slot table (caller pushes × callee read-offsets, joined by the asserted
ESP-depth sim; full chains in ARGUMENT_PROVENANCE.json):

| Slot | Push @VA | Bytes | Source | Value |
|---|---|---|---|---|
| arg1 | 0x006C3FCC | `51` | ECX ← `LEA [ESP+0x30]` @0x006C3FC8 | **&caller_param_2_slot** (out-slot address) |
| arg2 | 0x006C3FC7 | `50` | EAX ← `[EAX]` @0x006C3FC1 ← CALL 0x0040B070 (= P+0x14) | **[P+0x14]** (loop begin) |
| arg3 | 0x006C3FC6 | `52` | EDX ← `[EAX+4]` @0x006C3FBE (same EAX) | **[P+0x18]** (loop end) |
| arg4 | 0x006C3FC5 | `56` | ESI ← `[ESP+0x1C]` @0x006C3F79 (caller's param_2) | **caller-owned vector** (container) |
| arg5 | 0x006C3FC4 | `53` | EBX ← `MOV EBX,0x008BD720` @0x006C3FB0 | **0x008BD720** (code address) |
| arg6 | 0x006C3FC3 | `51` | ECX ← `[ESP+0x10]` @0x006C3FBA (local ← CALL 0x007CE1E0 = [P+8]) | **[P+8]** (dead in callee) |

- **Callee-side cross-check (independent)**: FUN_006C3640 reads arg1 @[esp+0x14]/d16 @0x006C3691
  and @[esp+0xC]/d8 @0x006C369C, arg2 @0x006C3646, arg3 @0x006C3641, arg4 @0x006C3654/@0x006C36A0,
  arg5 @0x006C364F — all under the live push depths — agreeing with the caller's push order.
- **Contract VA-annotation correction** (F1 catch): the frozen contract text said
  "arg2 = [P+0x14] @0x006C3FC3" — the push at 0x006C3FC3 carries [P+8] (arg6); [P+0x14] is
  pushed at 0x006C3FC7. SLOT attributions CONFIRMED as stated; the VA annotations were
  imprecise. The contract itself ordered byte re-derivation; no analysis impact.
- Frame-balance derivations (in-window only, asserted): growth helper 0x006C2E00 cleans 20 B
  (5 stack args; both callsites); the callback cleans 0; getter+lookup consume exactly the
  pushed 4-byte key (split inherited-context only — both splits give identical downstream
  slot maps, PROVEN by running both variants).

## 4. Phase 2 — body analysis of FUN_006C3640 (G3 PASS)

Full CFG in BODY_CFG_AND_ACCESS_CENSUS.json (10 basic blocks, 12 edges, all branch targets
in-window). Structure (all VAs dual-verified):

```
FUN_006C3640(arg1=&out_slot, arg2=begin, arg3=end, arg4=container, arg5=callback, arg6=UNUSED)
  if (begin == end) { *arg1 = container; return; }          // empty path @0x006C369C-0x006C36A8
  for (cur = begin; cur != end; cur += 0x20) {              // loop @0x006C3658-0x006C368F
      result = (*callback)(cur);                            // CALL EBX @0x006C365A, ECX=cur (thiscall)
      cursor = container->cursor;                           // [arg4+0x4] @0x006C365C
      if (cursor == container->end)                          // [arg4+0x8] @0x006C365F
          growth_append(container, cursor, result, &arg1, 1, 1);   // CALL 0x006C2E00 @0x006C3685 (CLOSED)
      else {
          if (cursor != 0) { [cursor]=result[0]; [cursor+4]=result[1]; }  // @0x006C3668-0x006C366F
          container->cursor += 8;                           // @0x006C3672
      }
  }
  *arg1 = container;                                          // @0x006C3691-0x006C3695
```

Complete access census: **16 memory accesses + 1 LEA**, every one enumerated with base
provenance (7 esp-frame/args + 1 LEA; 3 container-from-arg4; 2 callback-result; 2
cursor-from-container; 2 arg1-slot). The tracked template values are NEVER dereferenced.
**Zero FPU/SSE instructions in all four windows (machine-measured).** No field is named;
all dword semantics remain UNKNOWN.

## 5. Phase 2 — the four tracked values' dispositions (G4 PASS; VALUE_DISPOSITION.json)

1. **arg2 = [P+0x14]** — consumed in-register as the loop BEGIN pointer and as the per-element
   callback receiver source (ECX := EDI @0x006C3658); stride 0x20 @0x006C368A. Never written
   to memory, never dereferenced, never forwarded as data.
2. **arg3 = [P+0x18]** — consumed in-register as the loop END/limit (compared only). Never
   dereferenced, never stored. The consecutive-pair shape is consumed as a RANGE — explicitly
   NOT promoted to vector/coordinate.
3. **arg6 = [P+8]** — **DEAD ARGUMENT in this consumer**: zero window accesses resolve to its
   slot (machine scan). Its real consumer in the chain is the caller-side (0x66, [P+8]) pair
   insert into the caller-owned vector (@0x006C3F8D/F fast path; growth @0x006C3FA9) —
   predecessor-established, re-pinned here as caller context.
4. **arg5 = 0x008BD720** — consumed as the INDIRECT CALL TARGET (`FF D3` @0x006C365A), once
   per element, thiscall, no stack args; its return EAX is the 8-byte pair source that fills
   the container.

**What actually flows into the container**: NOT the template values — only the CLOSED-callee
callback's result pair. The container (arg4) provenance chain (caller's param_2) is DISJOINT
from the template pointer P's chain (falsifier F8: container ≠ template object,
machine-proven).

## 6. What 0x008BD720 IS (ANCHOR_008BD720_CLASSIFICATION.json)

**IDENTITY CLASS = CALL_TARGET (function pointer, code address in .text)** — from BEHAVIOR
(called per element via CALL EBX; executed as an instruction pointer) + BYTES (VA inside the
measured .text range 0x00401000–0x00A745E5, file-mapped at 0x4BD720; the 16 preregistered
raw bytes are `8D 41 18 C3` + 12×CC, non-zero). It is NOT a transform (zero FPU/SSE
anywhere), NOT a world-object reference (never dereferenced as data, only called), NOT
named (Ghidra's "FUN_008bd720" is a name artifact).

**Quarantined hypothesis (NOT a gate claim; callee CLOSED, not decoded this run)**: the four
leading bytes share the exact shape of the W-DEP1 interior-pointer thunk family byte-proven
this run (`8D 41 14 C3` = LEA EAX,[ECX+0x14]; RET) with displacement 0x18; IF decoded as that
family, the callback would return element+0x18 and the container would collect the dwords at
element+0x18/+0x1C (the last 8 bytes of each 0x20-byte element). Verifying or refuting this
needs a NEW bounded contract (4-byte dual decode at 0x008BD720). **No promotion.**

## 7. The six contract questions — adjudicated (STATIC_ONLY, era PCG 9.3.5)

1. **Direct memory writes?** YES — pair stores [cursor]←[result+0], [cursor+4]←[result+4]
   @0x006C366A/0x006C366F (destination = container buffer via [arg4+0x4] cursor) and
   *arg1 := container @0x006C3695/@0x006C36A5 (destination = the caller's param_2 slot).
2. **Object construction/initialization?** NO in-window constructor/init: no allocation, no
   vtable write; the growth helper MAY allocate internally (edge CLOSED, unresolved — recorded,
   not chased).
3. **Registration or callback dispatch?** YES — indirect per-element callback dispatch:
   CALL EBX @0x006C365A with ECX = element, once per 0x20-stride element; no other dispatch.
4. **Data validation or container management?** YES — container management: cursor/end
   compare @0x006C365F, null-cursor check @0x006C3664, 8-byte append + cursor advance
   @0x006C3672, growth delegation @0x006C3685, out-slot store on both paths.
5. **Additional value forwarding?** YES — callback result pair → container (fast path) or
   growth helper (arg2 = result pointer @0x006C3681); container pointer → *arg1; &arg1-slot →
   growth helper (arg3 @0x006C367C). arg6 forwarded INTO the callee is never consumed.
6. **Transform-relevant operation?** NOT_ESTABLISHED — zero FPU/SSE (machine-measured); only
   pointer arithmetic (range iteration, cursor management); no geometric evidence. NO
   promotion of any value to coordinate/transform.

## 8. Consumer verdict (the contract's explicit negative-result branch)

**FUN_006C3640 is a UTILITY — a generic range-collect/map function (iterate 0x20-byte
elements → per-element thiscall callback → append 8-byte result pair to an output vector),
NOT a world-placement consumer.** The world-placement question, if any, would live inside the
CLOSED callee 0x008BD720 (the per-element converter) — it was NOT chased, per the contract's
no-recursive-expansion rule.

## 9. Adversarial validation (G5 PASS — FALSIFIER_RESULTS.json)

All 8 falsifiers executed with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED:

- **F1 (slot swap)**: PASS — 6/6 slots machine-verified from BOTH sides; CAUGHT the contract's
  VA-annotation imprecision (push@0x006C3FC3 = [P+8]/arg6, not [P+0x14]).
- **F2 (wrong base register)**: PASS — 17-row census, every base provenance byte-pinned; the
  callback-result reads kept out of the template census; tracked values never dereferenced.
- **F3 (float→coordinate)**: PASS by discipline — 0 FPU/SSE in 105 instructions; the pair
  [P+0x14],[P+0x18] classified as a RANGE from cmp/add-0x20/jne operations, refuting the
  coordinate reading by operation evidence.
- **F4 (clobbered register)**: PASS with recorded conditions — all loop-carried state is
  callee-saved-class (EBX/ESI/EDI/EBP) across the two CLOSED calls; explicit ABI-assumption
  conditions recorded (not waived); frame-balance derivations independent of preservation.
- **F5 (return misattribution)**: PASS — per-path last-writer-wins EAX census; growth-call
  return machine-verified UNUSED; FUN_006C3640 returns EAX = arg1 and the caller ignores it;
  the per-path subtlety (mov eax,[eax+4] only on the fast path) machine-resolved.
- **F6 (Ghidra-only claim)**: PASS — zero load-bearing Ghidra claims; 3 artifacts quarantined
  (5-param signature missing the dead arg6; the FUN_008bd720 name; the corroborating-but-
  excluded decompile agreement).
- **F7 (boundary/target error)**: PASS — 0 disagreements over 105 instructions, both decoders;
  anchor rel32 recomputed == 0x006C3640; defect history disclosed (PE VA/RVA extraction bug,
  decoder ALU-dispatch draft bug, ESP-sim sign/successor bug — all caught pre-conclusion by the
  discipline machinery, fixed, re-run, re-measured).
- **F8 (container ≠ template)**: PASS — disjoint machine-proven provenance chains.

## 10. Science status (claim limits preserved VERBATIM; no change without genuinely independent load-bearing evidence)

- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- P's pointee identity vs the registry node: UNRESOLVED_UPSTREAM (inherited, untouched).
- sids-4057 namespace label: UNRECONCILED (untouched this run).
- NEW era-labeled structural findings (BYTE_OBSERVATION/STRUCTURE maturity only, this run):
  the pair ([P+0x14],[P+0x18]) is consumed as a 0x20-stride element RANGE by this consumer;
  [P+8] is paired with the dword 0x66 in the caller's vector insert; the container collects
  per-element callback results. NO runtime semantics promoted.

## 11. Not checked (honest list, with reasons)

- FUN_006C3640's callees 0x008BD720 and 0x006C2E00 bodies: NOT_CHECKED — CLOSED per the
  preregistration (the 16 B anchor read is raw bytes only; the 0x18-thunk reading is a
  quarantined hypothesis, not a verified claim). A 4-byte dual decode needs a new bounded contract.
- Whether the growth helper actually appends the pair (its internals): NOT_CHECKED — edge
  CLOSED; the append is inferred from in-window cursor arithmetic + the caller's parallel
  growth pattern (cross-callsite analogy, labeled as such).
- The getter/lookup cleanup SPLIT (which of the two consumed the 4-byte key): split-invariant
  proven for all downstream slot maps; the split itself is inherited context (predecessor's
  byte-proof), not load-bearing here.
- Runtime behavior of any kind (element contents, callback results, container state):
  NOT_CHECKED — STATIC_ONLY (the client never ran).
- P's pointee contents / registry population: NOT_CHECKED — UNRESOLVED_UPSTREAM as in the
  predecessors.
- 0x0085B1B0 / 0x0095D3C4: contract-FORBIDDEN — never opened, no edges exist to them in-window.

## 12. Gates summary

| Gate | Result |
|---|---|
| G1 ANCHORS_REPINNED | PASS — anchor rel32 recomputed == 0x006C3640; both windows + both 4-byte dependencies re-pinned from physical bytes; body-ends by the documented rule |
| G2 ARGUMENT_PROVENANCE | PASS — 6/6 slots dual-side machine-verified; cdecl caller-cleans proven (RET C3 + ADD ESP,0x18); contract VA-annotation correction recorded |
| G3 BODY_CENSUSED | PASS — 10-block CFG; 16 accesses + 1 LEA all classified with base provenance; full-window census (L24); 0 FPU/SSE |
| G4 DISPOSITIONS | PASS — arg2/arg3 loop-bounds consumption; arg6 dead (machine-verified); arg5 call target; container ≠ template |
| G5 FALSIFIERS_EXECUTED | PASS — 8/8 with the 4-part requirement each |
| G6 IDENTITY | PASS — EXE SHA unchanged before/after (3 checks); predecessor package 27/27 rows byte-unchanged before AND after; zero tracked-file modifications; zero .pyc residue (python -B, scan 0/0) |
| G7 NO_PROMOTION | PASS — zero XYZ/placement/transform/instance claims; utility verdict reported as the explicit negative result; claim limits preserved verbatim |

RUN_STATUS = COMPLETE (all preregistered windows within budget; no HARD_STOP; no scope expansion).
