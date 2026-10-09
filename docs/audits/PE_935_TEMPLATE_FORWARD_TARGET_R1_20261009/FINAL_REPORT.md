# FINAL_REPORT — PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

- **RUN_ID**: PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009
- **RUN_CLASS**: BOUNDED_STATIC_FORWARD_TARGET_MICRO (STATIC_ONLY — the client never ran)
- **Executor**: pe-reconstruction, dispatched by PE-MASTER under the human-authorized frozen
  contract (delivered in-session 2026-10-09). NO_NESTED_TASKS. No commit/push; no
  MANIFEST/QC_REPORT (later phases); AUDIT_ENTRYPOINT.md untouched.
- **Binary**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (PCG/EU 9.3.5), 8,015,872 B,
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 —
  re-hashed BEFORE (PASS) and AFTER (PASS) all work, unchanged.
- **Git**: BASE cea10e9cfcaa2e814f5cfe4269fd2a6a409d54da == HEAD == origin/master ==
  live ls-remote master (re-checked this run); zero tracked files modified; only this
  package (untracked) created.
- **Method**: own fresh pure-Python x86-32 decoder + PE parser (primary truth);
  GNU objdump 2.44 (WSL) independent cross-verification — **F8 gate: 0 disagreements over
  all 451 body instructions, 0 call-target disagreements**; Ghidra 11.2.1 (reused LANDMARK4057
  project, disclosed; sandbox EXE = physical hash, PASS) used ONLY as a hypothesis
  generator (falsifier F7). PREREGISTRATION.md written BEFORE all science; all windows and
  byte budgets pre-registered and respected.

---

## 1. The question and the answer in one paragraph

The contract asked: what happens to the template-registry lookup result P at the three
subject callsites — CALL 0x00511259 (FUN_00511070→FUN_007CE1E0), CALL 0x006C3F74
(FUN_006C3F50→FUN_007CE1E0), CALL 0x006C3FB5 (FUN_006C3F50→FUN_0040B070) — and inside the
two primary subject bodies. **The answer: P is dereferenced as a plain this-object — at +0x8
inside FUN_007CE1E0 (a 4-byte getter), and at +0x14/+0x18 through FUN_0040B070 (a 4-byte
interior-pointer thunk returning P+0x14, which the caller then reads at [P+0x14] and
[P+0x18] at 0x006C3FBE/0x006C3FC1). The loaded dwords are forwarded — to FUN_006C3640
(args 2/3/6: [P+0x14], [P+0x18], [P+8]) and to the caller-owned vector as the pair
(0x66, [P+8]) — but nothing in-window converts P into another object, uses it as a key or
handle, stores P itself, or performs any transform-relevant operation. Zero FPU/SSE
instructions exist anywhere in the six bodies. No field is named; no claim is promoted.**

## 2. Primary subjects re-pinned at exact VAs (G1 PASS — new science, bodies were CLOSED in the predecessor)

| Subject | Body (byte-pinned, pre-registered body-end rule) | Bytes | Semantics |
|---|---|---|---|
| **FUN_007CE1E0** | 0x007CE1E0–0x007CE1E3 (**4 B**) + 12×CC + next prologue (53 55 8B E9) | `8B 41 08` MOV EAX,[ECX+0x8]; `C3` RET | receiver-only thiscall getter: **returns the dword at this+0x8 BY VALUE**. GENERIC: also called at 0x0051115B inside FUN_00511070 with receiver = result of CALL 0x0041B3A0 (NOT template-derived) — an object-type-agnostic accessor ("getter family" per the predecessor's follow-up list, now byte-anchored in-window). |
| **FUN_0040B070** | 0x0040B070–0x0040B073 (**4 B**) + 12×CC + next function at 0x0040B080 | `8D 41 14` LEA EAX,[ECX+0x14]; `C3` RET | receiver-only thiscall thunk: **returns the interior pointer this+0x14**. NO memory access, NO dereference, NO allocation, NO vtable read — pure address arithmetic. |

## 3. Anchors re-pinned (pre-registered bounded dependencies W-E1/W-E2)

- **FUN_0072F580** (lookup), body 0x0072F580–0x0072F5AD (46 B, RET 0x4 @0x0072F5AB, +2×CC,
  next prologue 55 8B EC) — thiscall(this = registry map, 1 stack arg = key, callee cleans).
  Flow byte-pinned: result local via PUSH ECX; `LEA EAX,[ESP+0xC]`(&key)/`LEA ECX,[ESP+0x8]`
  (&result); `CALL 0x004D1430` (mapfind; body CLOSED — call edge recorded);
  `MOV EAX,[ESP+0x4]` (result slot); `CMP EAX,ESI` (result vs map); `JE` not-found;
  **found: `83 C0 14` ADD EAX,0x14 → returns mapfind_result+0x14**; **not-found: `B8 00 58
  BA 00` MOV EAX,0x00BA5800 → returns the sentinel**. NEW BYTE FACT: the +0x14 address
  arithmetic is inside the lookup; what FUN_004D1430's result slot holds (node vs other) is
  UNRESOLVED at window level (body CLOSED per the no-recursive-opening rule), so the
  predecessor's "P = the template object pointer" label is preserved as the inherited
  hypothesis with this refinement, NOT re-promoted.
- **FUN_0043A550** (getter), body 0x0043A550–0x0043A5C6 (119 B, RET C3, +9×CC; adjacent
  thunk at 0x0043A5CF `8B 09 E9 C9 0B 42 00` = MOV ECX,[ECX]; JMP 0x0085B1B0 — a SEPARATE
  function after the padding; **0x0085B1B0 body contract-FORBIDDEN, only these adjacent bytes
  recorded as body-end context**). Reads [0x00BA1824]; if 0: PUSH 0x18 → `CALL 0x0095D3C4`
  (operator new; **body contract-FORBIDDEN**, edge recorded) → ADD ESP,4 → on success
  `CALL 0x0052A260` (ctor; body CLOSED) → store singleton; on alloc-fail XOR EAX,EAX →
  store NULL → return 0. **KEY FINDING (falsifier F7 catch): the getter NEVER reads its
  first stack argument** — the pending lookup key sits below its frame and is consumed
  later by the lookup's RET 0x4. Ghidra's signature `FUN_0043a550(param_1)` is an
  inferred-type artifact.
- **Caller bodies**: FUN_00511070 0x00511070–0x0051152B (1212 B — predecessor claim
  CONFIRMED); FUN_006C3F50 0x006C3F50–0x006C3FDB (140 B — CONFIRMED). Body-end rule
  applied per PREREGISTRATION §5 (RET + padding/prologue, L24 respected).

## 4. Phase 1 — pointer identity at the three subject callsites (G2 PASS)

| Edge | Chain lookup-return → subject CALL (every intervening instruction) | Intervening calls | Classification |
|---|---|---|---|
| **E1** 0x00511259 (→FUN_007CE1E0) | `E8 29 E3 21 00` CALL 0x0072F580 @0x00511252; `8B C8` MOV ECX,EAX @0x00511257 (the ONLY ECX writer) | none | **POINTER_IDENTITY_CONFIRMED** |
| **E2** 0x006C3F74 (→FUN_007CE1E0) | CALL 0x0072F580 @0x006C3F62; `8B F8` MOV EDI,EAX @0x006C3F67 (EDI's only body writer); `BB 66…` MOV EBX,0x66; `8B CF` MOV ECX,EDI @0x006C3F6E (only ECX writer); `89 5C 24 0C` local store | none | **POINTER_IDENTITY_CONFIRMED** |
| **E3** 0x006C3FB5 (→FUN_0040B070) | EDI:=P @0x006C3F67; …fast path: vector writes + `EB 16` JMP; `8B CF` MOV ECX,EDI @0x006C3FAE. Growth path crosses `E8 52 EE FF FF` CALL 0x006C2E00 @0x006C3FA9 (body CLOSED) | both paths: CALL 0x006C3F74 (byte-proven EDI-safe — the chain anchor 0x006C3F67 precedes the E2 subject call; the callee's open 4-byte body `8B 41 08 C3` never writes EDI); growth additionally: CALL 0x006C2E00 @0x006C3FA9 (the ABI-assumption crossing, body CLOSED) [crossings census completed per QC finding P3-2, records correction 2026-10-09 — classification and condition unchanged] | **POINTER_IDENTITY_CONFIRMED_CONDITIONAL** (EDI survival across the closed callee rests on standard x86 callee-saved discipline — recorded as the condition, not waived; falsifier F5) |

Pointer-VALUE identity (ECX == EAX_lookup) is machine-proven at all three edges by
exhaustive register-writer tracing. POINTEE-CONTENTS identity of P remains at the
inherited-hypothesis level with the new byte facts (§3).

Incoming state and arguments at each CALL: **no stack arguments at any of the three
subject calls** (both callees are receiver-only thiscalls — proven by their 4-byte bodies);
E1 caller context: ESI=param_1 ([ESP+0x168] @0x0051109D), EBP=param_3 ([ESP+0x170]
@0x0051137), branch-selected id 0x2DFA @0x0051121C / 0x2DF9 @0x00511245 (11770/11769;
**neither is 4057=0xFD9**), or NO lookup (JE @0x00511243). E2/E3 caller context:
param_1 = the lookup key (provenance LEAVES WINDOW — UNKNOWN, never guessed), param_2 =
vector-like object; post-body raw context (outside the window, labeled as such): the
adjacent function 0x006C3FE0 loops over an id array calling FUN_006C3F50(id, vector)
cdecl with caller-side `ADD ESP,0x8`.

Sentinel and NULL cases (recorded separately, falsifier F2): P may be the not-found
sentinel 0x00BA5800 (statically all-zero .data tail; callers never test it in-window);
the getter may return NULL on alloc-failure (the lookup would then run on this=NULL —
error path, not further analyzed).

## 5. Phase 2 — callee field-access census (G3 PASS)

Complete census in CALLEE_FIELD_ACCESS_CENSUS.json. Template-pointer memory accesses
(4 direct rows, all BYTE_OBSERVATION):
1. **[ECX+0x8] READ** @0x007CE1E0 (`8B 41 08`) — inside FUN_007CE1E0; consumer: return
   value. On the not-found path this reads [0x00BA5808] = static 0.
2. **LEA [ECX+0x14]** @0x0040B070 (`8D 41 14`) — NO memory access (computed address only).
3. **[EAX+0x4] READ = [P+0x18]** @0x006C3FBE (`8B 50 04`) — base EAX = P+0x14 (the
   FUN_0040B070 return, sole EAX producer, no intervening writer); → EDX → arg3 of
   FUN_006C3640.
4. **[EAX] READ = [P+0x14]** @0x006C3FC1 (`8B 00`) — → arg2 of FUN_006C3640.

Plus 7 store/forward rows ([P+8] saved to frame local @0x006C3F83; the (0x66,[P+8])
vector-pair stores @0x006C3F8D/F into the CALLER-OWNED vector; the 3 pushes
@0x006C3FC3/C6/C7 → FUN_006C3640 args 6/3/2; EDI capture @0x0051125E and the two
PUSH EDI forwards @0x00511293 (arg2) / 0x005112E4 (arg3) → FUN_00414670,
path-conditional ([P+8] or 0), liveness ended by XOR EDI,EDI @0x0051133F). 11 rejection
classes enumerate
every OTHER memory operand in the windows (proving census completeness): param_2's
vector header; frame locals; the 0x50CAF0/0x50D8C0 struct-copy SOURCE reads (falsifier
F3 catch); the CALL 0x00843DD0-result read @0x005111A5; the EAX=ESP stack-write
regions @0x005113DC-0x005113E5 / @0x00511455-0x0051145D (base EAX = ESP after
SUB ESP,0xC; MOV EAX,ESP); the struct-copy STACK destinations (ECX=ESP); param_3's
struct; the GS cookie/SEH frames; [0x00BA2CE4]; the lookup's stack locals; the getter's
cookie/SEH/stack slots. *(Records correction 2026-10-09, QC finding P2-1: the former
single "0x50CAF0/0x50D8C0 result structs" rejection class over-labeled 7 non-template
W_A [EAX] operands, which now carry their true base provenance; the corrected
classifier was re-run over ALL 135 memory-form operands (126 modrm-form incl. 42 LEA
forms + 9 A0-A3 moffs forms) and yields unclassified=[] — see
CALLEE_FIELD_ACCESS_CENSUS.json census_completeness_revalidation.)*

**NO field is named position/rotation/scale/transform/world-coordinate anywhere. Zero
FPU/SSE instructions exist in all six bodies (machine-measured). All dword semantics =
UNKNOWN.** The [P+0x14],[P+0x18] consecutive pair shape was explicitly NOT promoted to
"vector" or "coordinate" (falsifier F4 discipline).

## 6. Phase 3 — the derived object test (G4 PASS, honest outcome)

- FUN_0040B070's result at CALL 0x006C3FB5 is **EAX = P + 0x14 — an INTERIOR POINTER of
  the receiver object** (byte-proven LEA; no allocation, no indirection, no wrapper
  table read in the callee). It is NOT a separate object, NOT a conversion, NOT a handle.
- The reads 0x006C3FBE ([EAX+4]) and 0x006C3FC1 ([EAX]) are therefore **actual field reads
  of the SAME object P at offsets +0x18 and +0x14** — not reads of a wrapper or a
  different object. This resolves the predecessor's UNKNOWN-identity note: the "derived
  object" is the receiver's own field region at +0x14, reached through the returned
  interior pointer.
- **DERIVED_OBJECT_IDENTITY = INTERIOR_POINTER_SAME_OBJECT** (relative to the lookup
  return P; P's own pointee identity vs the registry node remains UNRESOLVED at window
  level — see §3). **TRANSFORM_SEMANTICS = UNVERIFIED** — zero float ops, zero geometric
  evidence; the two dwords could be anything including non-coordinate data; this is the
  honest outcome the contract pre-declared acceptable.

## 7. Phase 4 — adversarial validation (G5 PASS)

All 8 contract falsifiers designed pre-execution (PREREGISTRATION §7), executed, and
recorded in FALSIFIER_RESULTS.json with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED:

- **F1** (ECX ≠ lookup result): traced; E1/E2 clean single-writer chains; E3's
  growth-path condition produced the honest _CONDITIONAL down-grade.
- **F2** (sentinel): not-found path byte-pinned; sentinel = static-zero .data tail;
  callers never test it; all classifications carry the condition.
- **F3** (field belongs to another object): complete provenance census; the 5-dword
  struct-copy near-miss (base = 0x50CAF0/0x50D8C0 results) caught and rejected; the
  second FUN_007CE1E0 use @0x0051115B (non-template receiver) identified.
- **F4** (float misclassification): 0 FPU/SSE in all six bodies; no coordinate naming;
  pair-shape not promoted. PASS by demonstrated discipline.
- **F5** (call destroys assumed-preserved register): E3 condition recorded; the
  in-window save/reload pair `89 44 24 10`@0x006C3F83 / `8B 4C 24 10`@0x006C3FBA proves
  the shipped code itself treats EAX as volatile across the branch that crosses the
  growth-path call.
- **F6** (return value misattributed): last-writer-wins attribution machine-verified;
  **caught and corrected the inherited "FUN_0040b070(0x8BD720)" reading — FUN_0040B070
  takes NO stack argument; 0x8BD720 (`BB 20 D7 8B 00` @0x006C3FB0) is prepared for the
  LATER FUN_006C3640 call as arg5** (a .text-range immediate, semantics UNRESOLVED,
  never called in-window; the Ghidra name "FUN_008bd720" is a name artifact).
- **F7** (claim depends only on Ghidra): zero load-bearing claims rest on Ghidra;
  concrete catches: the getter-signature artifact (§3), the 0x8BD720 name artifact (F6),
  and the corroborating-but-non-load-bearing agreement of the 4-byte-body decompiles.
- **F8** (boundary/target incorrect): dual-decoder agreement over 451 body instructions =
  0 boundary + 0 call-target disagreements; 3 defects in MY OWN decoder were caught by
  the objdump cross-check during calibration, fixed, and the whole pipeline re-run and
  re-measured BEFORE analysis (defect history disclosed in FALSIFIER_RESULTS.json).

## 8. The 6 contract questions — adjudicated per subject

For the template lookup result P at the three subject callsites:

1. **Dereferenced?** YES — [P+8] inside FUN_007CE1E0 (E1@0x00511259, E2@0x006C3F74);
   at E3 the callee does NOT dereference, but the caller immediately reads [P+0x14] and
   [P+0x18] through the returned interior pointer (@0x006C3FBE/0x006C3FC1).
2. **Converted to another object?** NO. FUN_007CE1E0 loads a dword (identity UNKNOWN —
   a pointer-shaped value, never instantiated in-window); FUN_0040B070 performs pure
   address arithmetic (P+0x14 — an interior view of the SAME object, not a new object).
3. **Key or handle?** NO in-window evidence: P is never compared, never looked up,
   never hashed. (The registry key is the id — the INPUT side.)
4. **Stored or forwarded?** P itself is NEVER stored (no [mem]:=P anywhere in the
   windows) — receiver-only, register-resident. Its FIELDS are forwarded: [P+8] →
   frame local → vector pair (0x66,·) → FUN_006C3640 arg6 (W_B) and → EDI → FUN_00414670
   (arg2 at the 3-arg call @0x0051129C; arg3 at the 5-arg call @0x005112F7; W_A,
   path-conditional); [P+0x14],[P+0x18] → FUN_006C3640 args 2,3 (W_B).
5. **Runtime object identity?** NOT_ESTABLISHED (STATIC_ONLY; preserved claim limit).
6. **Transform-relevant?** NOT_ESTABLISHED — zero FPU/SSE anywhere; no geometric
   operation; all forwarded dwords keep UNKNOWN semantics. NO promotion.

## 9. Science status (claim limits preserved verbatim; no change without genuinely independent load-bearing evidence)

- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- sids-4057 namespace label remains UNRECONCILED (untouched this run).
- The definition/resource vs world-instance distinction is preserved (template ids
  0x2DF9/0x2DFA and the window-unresolved key of FUN_006C3F50 are DEFINITION ids; no
  instance/placement claim is made).

## 10. Not checked (honest list, with reasons)

- FUN_004D1430 body (mapfind result semantics — node vs object; would settle P's pointee
  identity): NOT CHECKED — outside pre-registered windows (no recursive opening; needs a
  new bounded contract).
- FUN_006C2E00 body (would byte-verify EDI preservation on the E3 growth path): NOT
  CHECKED — outside windows; the callee-saved ABI assumption is recorded as E3's condition.
- FUN_006C3640 body (the final consumer of [P+0x14],[P+0x18],[P+8]): NOT CHECKED —
  outside windows; edge + exact argument mapping recorded.
- FUN_00414670 body (W_A consumer of [P+8]): NOT CHECKED — same discipline.
- 0x0085B1B0 and 0x0095D3C4 bodies: contract-FORBIDDEN — only edges/adjacent bytes recorded.
- Runtime object identity / any runtime behavior: NOT CHECKED — STATIC_ONLY (the client
  never ran).
- Whether the mapfind result is a std::map node (and thus whether P=node+0x14=&pair or an
  object pointer): NOT CHECKED (would require FUN_004D1430).
- The pointee CONTENTS of P (what the template object IS): UNRESOLVED_UPSTREAM — the
  registry POPULATION path (VFS reader cluster) remains out of scope as in the predecessor.

## 11. Gates summary

| Gate | Result |
|---|---|
| G1 ANCHORS_REPINNED | PASS — all 6 windows re-pinned from physical bytes; all callsite identities recomputed (0 disagreements) |
| G2 EDGES_CLASSIFIED | PASS — 3/3 subject callsites classified (2 CONFIRMED, 1 CONFIRMED_CONDITIONAL with byte-documented reason) |
| G3 CALLEE_CENSUSED | PASS — 4 direct access rows + 7 store/forward rows + 11 rejection classes (class split per QC finding P2-1, records correction 2026-10-09; corrected classifier re-run over all 135 memory-form operands: unclassified=[]); no field named; UNKNOWN preserved |
| G4 DERIVED_OBJECT_ADJUDICATED | PASS — INTERIOR_POINTER_SAME_OBJECT; TRANSFORM_SEMANTICS = UNVERIFIED |
| G5 FALSIFIERS_EXECUTED | PASS — 8/8 executed with the 4-part requirement each |
| G6 IDENTITY | PASS — EXE SHA unchanged before/after; predecessor package 25/25 byte-unchanged before AND after; zero tracked-file modifications; zero .pyc residue (python -B) |
| G7 NO_PROMOTION | PASS — zero XYZ/placement/instance claims; all findings STATIC_ONLY at BYTE_OBSERVATION/STRUCTURE/RELATION maturity |

RUN_STATUS = COMPLETE (all pre-registered windows within budget; no HARD_STOP).
