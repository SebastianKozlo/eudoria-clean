# SUPERSESSION — f99febe record overclaims corrected
## RUN_ID: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 (Work Package A)

**WHAT THIS DOCUMENT DOES:** It explicitly and loudly SUPERSEDES four record defects
of the published f99febe package
`docs/audits/PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009/` (commit
f99febeca9498011fc49f3aef932ecfac4244475): the three P2 overclaims identified by the
Desktop post-audit (FC-C1, FC-C2, FC-C3) and the P3 "callee reads all six arguments"
sentence. **The historical package itself is READ_ONLY and remains byte-unchanged**
(22/22 manifest rows re-verified MATCH this run). The corrected standing lives HERE,
in this run's records package. Any consumer of the f99febe conclusions must read them
through this supersession.

**WHAT THIS DOCUMENT DOES NOT DO:** It does not reject the historical run's
measurements, its physical pins, its dual-verified decode, its publication integrity,
or any of its retained facts listed in section 6. It does not open any closed body
(0x008BD720 beyond its published 16 B data dump, 0x006C2E00, 0x0085B1B0,
0x0095D3C4). It does not execute the client. It grants no qualification of any kind
(CANONICAL_GATE_EFFECT = NONE).

**EVIDENCE BASE (all re-verified this run, see INPUT_IDENTITIES.json):** physical
Entropia.exe `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — 8,015,872 B /
SHA256 `e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31` (MATCH);
its five already-published window slices re-hashed 5/5 MATCH; 17/17 FC-relevant
instruction bytes inside the two already-open windows MATCH; the historical package
22/22 manifest rows MATCH. Era/build label for every claim below: **PCG/EU 9.3.5,
STATIC_ONLY** (the client never ran; all maturity at BYTE_OBSERVATION / STRUCTURE /
RELATION level).

---

## 1. FC-C1 — SUPERSEDED: arg6 was identified with the initial getter value on ALL paths

### 1.1 OLD claim wording (published, now superseded)

- `ARGUMENT_PROVENANCE.json` (f99febe), argument_table slot arg6 — value:
  *"the dword at P+0x8 - inherited label '[P+8]'"*, provenance *"saved from EAX =
  CALL 0x007CE1E0 @0x006C3F74 return … ECX=P from 0x006C3F6E"* — i.e., the later
  arg6 is stated to BE the getter return, with no fast/growth separation.
- `FINAL_REPORT.md` §3 slot table row: *"arg6 | 0x006C3FC3 | 51 | ECX ← [ESP+0x10]
  @0x006C3FBA (local ← CALL 0x007CE1E0 = [P+8]) | [P+8] (dead in callee)"* and §5.3:
  *"arg6 = [P+8] — DEAD ARGUMENT in this consumer"*.
- `HANDOFF.md` slot table (line 37), PER-VALUE DISPOSITION (line 50) and 12-line
  summary item 2 (line 158): *"arg6 = [P+8] (DEAD …)"*.
- `AUDIT_ENTRYPOINT.md` f99febe row: *"arg6=[P+8] DEAD ARGUMENT in this consumer
  (machine-verified 0 of 17 census rows resolve to entry offset 0x18; the real
  consumer = the caller's (0x66,[P+8]) vector insert @0x006C3F8D/F)"*.

**Defect:** the later arg6 was equated with the initial getter value on ALL paths. On
the caller's GROWTH path this is NOT established: the getter-return copy sits in a
frame local whose ADDRESS ESCAPES into the closed growth helper BEFORE the reload that
produces the later arg6.

### 1.2 The byte-verified escape chain (already-open caller window, re-verified 17/17 this run)

```text
0x006C3F83  89 44 24 10   mov [esp+0x10],eax     ; save getter return into LOCAL_1 (pair+4)
0x006C3F87  74 0f         je 0x006C3F98         ; cursor==end -> GROWTH path
0x006C3F8D  89 19         mov [ecx],ebx         ; fast path: [cursor]   <- 0x66
0x006C3F8F  89 41 04      mov [ecx+4],eax      ; fast path: [cursor+4] <- getter value
0x006C3F92  83 46 04 08   add [esi+4],8        ; cursor += 8  (fast + fast-null)
0x006C3F96  eb 16          jmp 0x006C3FAe      ; skip growth
0x006C3F98  6a 01 / 6a 01  push 1 / push 1     ; growth args
0x006C3F9C  8d 54 24 24   lea edx,[esp+0x24]   ; &param_2 (out-slot arg)
0x006C3FA1  8d 44 24 18   lea eax,[esp+0x18]   ; &LOCAL_2 = the PAIR BASE —
                                               ;   the address that ESCAPES
0x006C3FA9  e8 52 ee ff ff call 0x006C2E00    ; CLOSED growth helper gets the pair
                                               ;   address; LOCAL_1 = pair+4 is IN range
0x006C3FBA  8b 4c 24 10   mov ecx,[esp+0x10]   ; RELOAD of LOCAL_1 = later arg6 source
0x006C3FC3  51             push ecx             ; the later arg6
```

With B = ESP after the caller's prologue, the pair lies at B+0x0C and its second
DWORD (LOCAL_1, the saved getter value) at B+0x10; at LEA @0x006C3FA1 ESP = B−12, so
`[ESP+0x18]` = B+0x0C — the helper receives the address COVERING the slot of the
later arg6. (Cross-checked against the package's own ESP_SLOT_MAP W_CALLER labels:
LOCAL_2 @entry_offset −8 = pair base, LOCAL_1 @entry_offset −4 = the reloaded slot.)

### 1.3 NEW corrected wording (the standing claim)

1. **Initial value (VALID, BYTE_OBSERVATION):** the frame local LOCAL_1 receives the
   getter return — the initial `[P+8]` read (CALL 0x007CE1E0 → save @0x006C3F83).
2. **Fast-path provenance (VALID, PRESERVED):** on the caller's fast paths
   (fast-store @0x006C3F8D/F and fast-null @0x006C3F8B→0x006C3F92) there is NO call
   between the save and the reload — the later arg6 equals the initial getter value
   on those paths.
3. **Growth path (CORRECTED):** on the growth path the pair address escapes into the
   closed helper CALL 0x006C2E00 @0x006C3FA9 before the reload @0x006C3FBA; the
   later arg6 is the DWORD re-read from the ESCAPED local. **Equality of the later
   arg6 with the initial getter value on the growth path =
   NOT_ESTABLISHED_WITHIN_BOUND.** Nonvolatile-register preservation and the
   stack-cleanup balance are ABI facts about REGISTERS and stack DEPTH — they do NOT
   preserve escaped stack MEMORY and were never evidence about that slot's contents.
   (Countermodel CM-1: a stub helper can mutate the escaped local while preserving
   every observable ABI condition.)
4. **Subject-side same-class precision (CORRECTED):** FUN_006C3640 passes the address
   of its OWN arg1 slot (LEA @0x006C367C, entry_offset 4) to the growth helper and
   LATER re-reads that slot @0x006C3691 before `*arg1 := container` @0x006C3695.
   The store is byte-correct for the RE-READ pointer; the identity of the re-read
   value with the INITIAL arg1 (the caller's &param_2 out-slot) on the growth path is
   NOT established — **the initial out-pointer's survival through the helper is NOT
   established** by the late read. (Countermodel CM-4.) The subject's LATE READ of
   arg1 remains a byte fact; it is distinguished from proof of survival.
5. **Consequently** the flat shorthand "arg6 = [P+8]" (and "the callee receives [P+8]"
   as a value claim) is superseded by: *"arg6 = the reloaded frame local whose
   initial content was the getter return; equal to the initial getter value on the
   fast paths; equality NOT_ESTABLISHED_WITHIN_BOUND on the growth path"*.

### 1.4 What stays valid vs what becomes UNRESOLVED/NOT_ESTABLISHED (FC-C1)

- **STAYS VALID:** the subject's direct arg6-slot non-use (0 of 17 census rows
  resolve to entry_offset 0x18 — machine scan, re-verified) — a separate, independent
  fact, unaffected by the value-provenance correction; the fast-path provenance; the
  initial-save byte facts; the (0x66, [P+8]-initial) pair construction
  (@0x006C3F70/0x006C3F83); the fast-path insert stores @0x006C3F8D/F; the
  physical pins.
- **BECOMES NOT_ESTABLISHED:** growth-path equality of the later arg6 to the initial
  [P+8]; survival of the subject's initial arg1 out-pointer across the growth helper;
  (already-labeled) whether the growth helper appends the pair at all — the append
  remains INFERRED (cross-callsite analogy), now with the explicit note that the
  pair contents at the growth call are also subject to helper-side effects through
  the escaped address.

---

## 2. FC-C2 — SUPERSEDED: producing-chain disjointness was read as an address-inequality proof

### 2.1 OLD claim wording (published, now superseded)

- `FALSIFIER_RESULTS.json` F8 outcome: *"PASS (container != template object,
  machine-proven disjoint provenance)"* — an object-inequality verdict.
- `FINAL_REPORT.md` §5: *"The container (arg4) provenance chain (caller's param_2)
  is DISJOINT from the template pointer P's chain (falsifier F8: container ≠
  template object, machine-proven)"*; §9 F8: same wording; §12 G4 row: *"…
  arg6 dead (machine-verified); arg5 call target; container ≠ template"*.
- `VALUE_DISPOSITION.json` container_provenance_vs_template: *"The two chains are
  DISJOINT (falsifier F8: container is NOT the template object)"*.
- `HANDOFF.md` F8 line and 12-line summary item 6: *"the container's provenance
  (caller's param_2) is machine-proven DISJOINT from the template pointer P's chain
  (falsifier F8)"*; entrypoint row: *"container provenance DISJOINT from the template
  chain (F8 wrong-object control)"* — read as inequality.
- Absolute dereference wording (`FINAL_REPORT` §4/§5, `FALSIFIER_RESULTS` F2, `HANDOFF`
  per-value dispositions): *"The tracked template values are NEVER dereferenced"* /
  *"the tracked values never reach memory as data"*.

### 2.2 NEW corrected wording (the standing claim)

1. **The two origins stay (VALID):** the container chain (ESI ← the caller's
   incoming param_2 @0x006C3F79, entry_offset 8; provenance leaves the window at the
   caller's caller) and the template chain (P ← lookup return @0x006C3F62 → EDI) are
   byte-proven **distinct static producing chains** — 0 shared producing
   instructions.
2. **CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED.** Different producing chains are NOT
   proof of different addresses. Distinct SSA/provenance sources can resolve to the
   same runtime address; no in-window instruction establishes or excludes
   param_2 == P, and the callers that establish param_2 were not reconstructed.
   (Countermodel CM-2: two distinct chains, same address, with the examined window's
   field usage — container roles +4/+8 vs range roles +0x14/+0x18 — fully compatible
   on one aliased object.)
3. **The callback return can alias its receiver:** the closed callback receives
   ECX = element (an address derived from the tracked range chain) and its return EAX
   is dereferenced ([EAX]/[EAX+4] @0x006C3668/0x006C366C). A callback returning its
   receiver makes those reads touch element memory. **No direct EDI-based memory
   operand does not prove that the same address is never read through EAX.**
   (Countermodel CM-5.)
4. **The census fact stays, the absolute does not:** 0 direct memory operands with
   the tracked carriers (EDI/EBP/EBX) as base — VALID as a direct-operand count. The
   absolute "the tracked template values are NEVER dereferenced" is superseded by:
   *"no DIRECT dereference of the tracked values occurs in-window; indirect
   dereference through the closed callback's return is NOT EXCLUDED"*.
5. **F2/F8 and gate corrections (per the correction mandate):**
   - **F8 re-classed:** from a PASS-as-address-inequality proof to a
     **producing-chain-disjointness observation** (countercheck class). Its measured
     content (0 shared producing nodes) is retained; its inference ("container ≠
     template object") is withdrawn as unproven.
   - **F2 narrowed:** the 17-row base-provenance census stays; the
     "tracked values never dereferenced" outcome clause is narrowed per 2.2.4.
   - **G4 (DISPOSITIONS) corrected:** the "container ≠ template" cell becomes
     "producing chains distinct; CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED"; all
     other G4 cells unchanged.
   - **G5 (FALSIFIERS_EXECUTED) corrected:** the "8/8" aggregate is replaced by the
     per-control honest classes (section 4.2 below); no gate flips to FAIL — the
     corrections narrow interpretations; the honest aggregate label is
     CORRECTED_WITH_INTERPRETATION_NARROWING.

### 2.3 What becomes UNRESOLVED/NOT_ESTABLISHED (FC-C2)

- CONTAINER_VS_P_ALIAS_RELATION = **UNRESOLVED** (neither aliasing nor distinctness
  is established within the examined bound).
- Whether the callback's return aliases its receiver at runtime = **NOT_ESTABLISHED**
  (body CLOSED; the quarantined 16 B dump `8D 41 18 C3` + 12×CC thunk-family
  hypothesis — which would return element+0x18, an interior alias of the receiver —
  remains an UNVERIFIED QUARANTINED HYPOTHESIS, not evidence).
- Any type/allocation/unique-identity claim about the container object vs the
  template pointee = **NOT_ESTABLISHED** (would need new bounded evidence; not to be
  resolved by opening bodies in a records-only round).
- "The tracked template values never reach memory as data" = **narrowed** to
  direct in-window evidence only (2.2.4).

---

## 3. FC-C3 — SUPERSEDED: a categorical placement exclusion was derived from a local container operation

### 3.1 OLD claim wording (published, now superseded)

- `FINAL_REPORT.md` §1: *"FUN_006C3640 is therefore NOT a world-placement consumer —
  the contract's negative-result branch applies"*; §8: *"FUN_006C3640 is a UTILITY —
  a generic range-collect/map function (…), NOT a world-placement consumer. The
  world-placement question, if any, would live inside the CLOSED callee 0x008BD720
  (the per-element converter) — it was NOT chased"*.
- `HANDOFF.md` verdict (line 80–83): *"… a generic range-collect/map function (…)
  — NOT a world-placement consumer. The placement question, if any, lives inside the
  CLOSED callee 0x008BD720"*; 12-line summary item 1 (line 157): *"… GENERIC
  RANGE-COLLECT/MAP UTILITY — NOT a world-placement consumer; that negative verdict
  is the contract's explicit negative-result branch"*.
- `AUDIT_ENTRYPOINT.md` f99febe row: *"… = GENERIC RANGE-COLLECT/MAP UTILITY - NOT a
  world-placement consumer (the contract's explicit negative result, reported without
  optimization)"* — plus, in the row, the mechanism is juxtaposed with 0 FPU/SSE and
  the closed-callee confinement, reading as an exclusion of the placement branch.

**Defect:** from a window containing only generic range/callback/container
operations and zero FPU/SSE, the package excluded the function from world placement
categorically, and confined any placement question to the single closed callback.
That inference exceeds the evidence: absence of FPU/SSE does not exclude float BIT
copies (two DWORDs can carry IEEE-754 bits through the generic copy — countermodel
CM-3), and a generic range-collect utility CAN be a stage of a placement pipeline;
additionally, the element-producer context and the downstream consumer of the
collected pairs are separate unexplored unknowns — the placement question is not
confined to the callback.

### 3.2 NEW corrected wording (the standing claim)

1. **GENERIC_RANGE_CALLBACK_CONTAINER_MECHANISM = CONFIRMED_IN_EXAMINED_WINDOW** —
   all retained (see section 6).
2. **DIRECT_TRANSFORM_OPERATION = NOT_ESTABLISHED** — in-window there is no direct
   transform/world-placement operation: 0 FPU/SSE (machine scan, 105 instructions),
   pointer arithmetic and container management only. This negative is valid FOR THE
   EXAMINED WINDOW.
3. **ROLE_IN_PLACEMENT_PIPELINE = UNRESOLVED** — the examined window cannot decide
   whether this utility participates in a placement pipeline. Absence of FPU/SSE
   does not exclude float bit copies or participation in a placement pipeline; the
   semantic content of the elements, of the callback results and of the collected
   pairs remains UNKNOWN.
4. **PLACEMENT_BRANCH_EXCLUDED = NO.**
5. **The callback-confinement sentence is withdrawn:** the placement question is NOT
   established to "live inside" the single closed callee; the element-producer
   context and the downstream container consumer are separate unknowns, and no
   location is established.
6. The justified maximum is the package's own §7.6 wording — *"Transform-relevant
   operation? NOT_ESTABLISHED"* — which this supersession restores as THE claim;
   the categorical sentences are superseded to match it.

### 3.3 What becomes UNRESOLVED/NOT_ESTABLISHED (FC-C3)

- ROLE_IN_PLACEMENT_PIPELINE = **UNRESOLVED**; PLACEMENT_BRANCH_EXCLUDED = **NO**.
- Element/pair value semantics (floats? identifiers? structure fragments?) =
  **UNKNOWN** (STATIC_ONLY; elements never read in-window).
- The quarantined callback hypothesis (container collects element+0x18/+0x1C per
  the thunk-family byte shape) remains **UNVERIFIED QUARANTINED HYPOTHESIS** — it is
  recorded as an illustration of a plausible bit-copy mechanism, NOT as a claim.

---

## 4. P3 SENTENCE — SUPERSEDED: "the callee reads all six arguments from the stack"

### 4.1 OLD wording (published, now superseded)

`ARGUMENT_PROVENANCE.json` (f99febe), calling_convention.register_arguments:
*"NONE - the callee reads all six arguments from the stack ([esp+disp] at entry push
depths; machine slot map in 01_RAW/ESP_SLOT_MAP.json); no this-register argument is
used by FUN_006C3640 itself"*.

### 4.2 NEW corrected wording

**The callee's DIRECT stack-slot usage is arg1–arg5, NOT arg6**: arg2 @0x006C3646,
arg3 @0x006C3641, arg4 @0x006C3654/@0x006C36A0, arg5 @0x006C364F, arg1
@0x006C3691/@0x006C369C (+ the &arg1 address computation LEA @0x006C367C);
**arg6's slot (entry_offset 0x18) has ZERO direct accesses** (0 of 17 census rows;
machine scan — the package's own core census, and its per-value disposition, already
say exactly this). The old sentence's register part ("no this-register argument…")
stays valid; the "all six" part is superseded. (Six slots are PUSHED by the caller
and cleaned by ADD ESP,0x18 — that fact is unchanged; what is corrected is what the
callee itself directly reads.)

### 4.3 The "8/8 falsifiers PASS" label — corrected classification

The old aggregate ("All 8 falsifiers executed PASS"; G5 "8/8 with the 4-part
requirement each"; HANDOFF "ALL FALSIFIERS — OUTCOMES … EXECUTED, PASS"; 12-line
summary item 11) mixed different kinds of control. The honest per-control classes
(no old denominator forced):

| ID | What it actually was (measured content retained) | Honest class | Disposition after correction |
|---|---|---|---|
| F1 | dual-side slot-derivation cross-join; caught the contract's VA-annotation imprecision | COUNTERCHECK (detected a failure case) | VALID (unchanged) |
| F2 | 17-row memory-operand base-provenance census | METHODOLOGICAL CENSUS | VALID as census; "never dereferenced" clause NARROWED by FC-C2 |
| F3 | 0-FPU/SSE opcode-family scan + naming-discipline audit | METHODOLOGICAL DISCIPLINE CHECK | VALID as scan; NOT a semantic proof — its interpretation is bounded by FC-C3 (bit copies) |
| F4 | register-preservation expectation audit with explicit ABI-assumption conditions | CONDITION RECORD | VALID; NOT an executed preservation test (bodies CLOSED) |
| F5 | per-path EAX writer/reader census (last-writer-wins; growth-return unused) | COUNTERCHECK | VALID (unchanged) |
| F6 | Ghidra-quarantine audit (0 load-bearing Ghidra claims) | METHODOLOGICAL QUARANTINE CHECK | VALID (unchanged) |
| F7 | own decoder vs GNU objdump cross-verification, 0/105 disagreements, defect history disclosed | CROSS-IMPLEMENTATION DECODE COUNTERCHECK (reproducibility) | VALID (unchanged) |
| F8 | container-vs-template provenance comparison (0 shared producing nodes) | NEGATIVE CONTROL | measured content VALID; its ADDRESS-INEQUALITY interpretation SUPERSEDED by FC-C2 |

**None of the 8 was a mutation test on an actual helper body.** The mutation-class
evidence in THIS package is the logical countermodel reproduction
(COUNTERMODEL_RESULTS.json) — explicitly NOT actual execution of FUN_006C2E00 and
NOT an opened callback/helper body.

---

## 5. Science standing — unchanged and restated (no promotion anywhere)

```text
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
P's pointee identity vs the registry node = UNRESOLVED_UPSTREAM (inherited, untouched)
sids-4057 namespace label = UNRECONCILED (untouched)
CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED            (FC-C2)
DIRECT_TRANSFORM_OPERATION = NOT_ESTABLISHED           (FC-C3)
ROLE_IN_PLACEMENT_PIPELINE = UNRESOLVED               (FC-C3)
PLACEMENT_BRANCH_EXCLUDED = NO                        (FC-C3)
GROWTH_PATH_ARG6_EQUAL_INITIAL = NOT_ESTABLISHED_WITHIN_BOUND   (FC-C1)
SUBJECT_ARG1_INITIAL_OUT_POINTER_SURVIVAL = NOT_ESTABLISHED     (FC-C1)
CANONICAL_GATE_EFFECT = NONE
```

No XYZ, placement, transform, instance or world claim is made or promoted by this
supersession. All findings remain era-labeled PCG/EU 9.3.5, STATIC_ONLY.

---

## 6. RETAINED FACTS — explicitly NOT superseded (the correction preserves these)

1. **Physical pins:** anchor CALL 0x006C3FCD rel32 recomputed → 0x006C3640; subject
   window 0x006C3640–0x006C36A8 (105 B, 47 insns, dual-verified); caller window
   0x006C3F50–0x006C3FDB (140 B, 54 insns); W-DEP1 `8D 41 14 C3`
   (LEA EAX,[ECX+0x14]; RET); W-DEP2 `8B 41 08 C3` (MOV EAX,[ECX+8]; RET); the 16 B
   anchor data dump `8D 41 18 C3` + 12×CC (raw bytes only). All re-verified 5/5
   slices + 17/17 instruction bytes MATCH this run.
2. **Range begin/end role:** arg2/arg3 consumed IN-REGISTER as the begin/end of a
   0x20-stride element loop (CMP/JE @0x006C364A/4C; ADD EDI,0x20 @0x006C368A;
   CMP/JNE @0x006C368D/8F) — a RANGE, not promoted to vector/coordinate.
3. **Stride 0x20** (element stride, byte-proven).
4. **Indirect call target:** arg5 = 0x008BD720 consumed as the per-element thiscall
   callback target (CALL EBX @0x006C365A, ECX = element, no stack args) — identity
   class CALL_TARGET from behavior + bytes; NOT a transform, NOT a world-object
   reference, NOT named.
5. **Fast-path two-DWORD copy:** [cursor]←[EAX], [cursor+4]←[EAX+4]
   @0x006C366A/0x006C366F; cursor += 8 @0x006C3672; growth delegation @0x006C3685
   (edge CLOSED, derived cleanup 20); out-slot stores *arg1 := container on both
   paths @0x006C3695/@0x006C36A5.
6. **The subject's direct arg6-slot non-use** (0 of 17 census rows → entry_offset
   0x18) — VALID and UNAFFECTED by FC-C1's value-provenance correction.
7. **The two distinct producing chains** (container from the caller's param_2; P from
   the lookup return) — VALID as static provenance (FC-C2 corrects only the
   address-inequality inference).
8. **Generic range/callback/container operations** (loop, dispatch, append, growth
   delegation, out-slot write) = CONFIRMED_IN_EXAMINED_WINDOW (FC-C3 corrects only the
   categorical exclusion).
9. **cdecl caller-cleans** (RET C3 both epilogues; ADD ESP,0x18 @0x006C3FD2; push
   depths 24/28/32/36/40/44; callee read-offset join 6/6 — arg1–arg5 directly read).
10. **0 FPU/SSE in all 105 instructions** (machine scan) — valid measurement; its
    interpretive scope is bounded by FC-C3 (does not exclude float bit copies).
11. The sentinel condition (P = 0x00BA5800 → [P+0x14] == [P+0x18] == 0 → empty path)
    and all conditional framing of the historical package.

---

## 7. How this supersession was validated

- Every OLD wording above was read from the historical package's own artifacts
  (byte-pinned files, 22/22 manifest MATCH) and the f99febe AUDIT_ENTRYPOINT row —
  no wording is invented.
- Every instruction byte relied on was re-verified from the physical EXE inside the
  two already-open windows (17/17 MATCH) — no new body was opened, no closed callee
  was touched.
- The corrections' mutation-class sufficiency arguments were reproduced by five
  independently written logical countermodels (CM-1…CM-5), all REPRODUCED — see
  COUNTERMODEL_RESULTS.json. **LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual
  execution of FUN_006C2E00; NO callback/helper body opened.**
- The corrected claim set is stated machine-readably in CORRECTED_CLAIM_MATRIX.json
  with evidence sources, era labels, non-circularity reasoning and detected failure
  cases.
