# PREREGISTRATION — PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
## Phase: PREFLIGHT ARTIFACTS + WORK PACKAGE A (records correction)

**This document was written and frozen BEFORE the Package A science (the countermodel
executions and the claim adjudication).** Preflight (BASE verification, input hashing,
published-pin re-verification, census, governance reading) was already complete and
is recorded in AUTHORIZATION_AND_PREFLIGHT.md / INPUT_IDENTITIES.json. Nothing in
this preregistration was written after seeing a countermodel result.

## 1. Scope registered for this phase

Contract sections 1, 2 and 4 (plus the section-15 file requirements for these
outputs). Records-only science: **no** SDK execution, **no** PE asset execution,
**no** new EXE body access, **no** commit/push, **no** AUDIT_ENTRYPOINT edit.

- Findings sources (NOT preaccepted truth): the Desktop post-audit
  `PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009` (REPORT.md,
  verdict REQUIRE_CORRECTIONS, 3× P2 + supporting P3s) and its
  CLAIM_SUFFICIENCY_COUNTERMODELS.json. Both re-measured and identity-MATCH.
- Adjudication target: the historical f99febe package
  `docs/audits/PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009/` (READ_ONLY,
  22/22 manifest rows re-verified MATCH) **and its raw evidence**
  (01_RAW listings, slot maps, own-decoder windows) **and the physical binary**
  (Entropia.exe E7785430…F31; 5/5 published slices re-verified MATCH;
  17/17 FC-relevant instruction bytes inside the two already-open windows MATCH).
- The historical package is NOT edited. All corrections live in this run's
  `00_RECORDS_CORRECTION/`.

## 2. The three FC corrections to be adjudicated (exact corrected semantics, contract section 4)

### FC-C1 — arg6 value provenance vs the escaped local

**Old claim shape (to be superseded):** arg6 is identified flatly as `[P+8]`
(the getter return) on ALL paths (ARGUMENT_PROVENANCE.json:88 value field + slot
table; FINAL_REPORT §3/§5; HANDOFF slot table + dispositions + 12-line summary;
AUDIT_ENTRYPOINT f99febe row "arg6=[P+8] DEAD ARGUMENT …").

**Corrected semantics to adjudicate (registered BEFORE checking):**

1. **Separate the initial getter value from the later arg6 after the escaped-local
   call (CALL 0x006C2E00 @0x006C3FA9).** The save @0x006C3F83 (89 44 24 10) stores
   the getter return ([P+8] initial read) into the frame local; the later arg6 is the
   RELOAD @0x006C3FBA (8B 4C 24 10) pushed @0x006C3FC3.
2. **Preserve fast-path provenance.** On the caller's fast paths (fast-store
   @0x006C3F8D/F and fast-null @0x006C3F92) there is NO call between the save and the
   reload — the later arg6 equals the initial getter value on those paths
   (in-window BYTE_OBSERVATION, stays valid).
3. **Growth-path equality to the initial [P+8] = NOT_ESTABLISHED_WITHIN_BOUND.** On
   the growth path (je @0x006C3F87 → 0x006C3F98) the address of the local pair
   (&LOCAL_2, LEA @0x006C3FA1 = 8D 44 24 18; LOCAL_1 = pair+4 is the saved getter
   value) ESCAPES into the closed helper CALL @0x006C3FA9 BEFORE the reload
   @0x006C3FBA. **Nonvolatile-register preservation does NOT preserve escaped
   memory** — ABI conformance (callee-saved registers, stack-cleanup balance) is not
   evidence about the contents of a stack slot whose address was handed to the callee.
4. **Preserve the subject's direct arg6-slot non-use as a separate, valid fact** —
   FUN_006C3640's body never directly accesses entry_offset 0x18 (0 of 17 census
   rows; machine scan). This fact is UNAFFECTED by the value-provenance correction.
5. **Distinguish the subject's late read of arg1 from proof that its initial
   out-pointer survived the helper.** The subject passes &arg1 (LEA @0x006C367C) to
   the growth helper and later re-reads the arg1 slot @0x006C3691 before storing
   *arg1 := container @0x006C3695. The store is byte-correct for the RE-READ
   pointer; identity of the re-read value with the INITIAL arg1 (the caller's
   &param_2 out-slot) is NOT established on the growth path — that survival is
   NOT established by the re-read itself.

### FC-C2 — producing-chain disjointness vs address identity

**Old claim shape (to be superseded):** "container ≠ template object,
machine-proven" (F8's PASS as an object-inequality proof; FINAL_REPORT §5/§9/§12;
VALUE_DISPOSITION container_provenance_vs_template; HANDOFF; entrypoint row
"container provenance DISJOINT from the template chain (F8 wrong-object control)"
read as an address-inequality claim); plus the absolute "the tracked template
values are NEVER dereferenced".

**Corrected semantics to adjudicate (registered BEFORE checking):**

1. **Keep the two origins (producing chains).** The container chain (ESI ← caller
   param_2 @0x006C3F79, entry_offset 8, provenance leaves the window) and the
   template chain (P ← lookup return → EDI) are byte-proven DISTINCT STATIC
   PRODUCING CHAINS — 0 shared producing instructions. This stays valid.
2. **CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED.** Different producing chains are
   NOT proof of different addresses. Distinct SSA/provenance sources can resolve to
   the same runtime address; no in-window instruction establishes or excludes
   param_2 == P. The alias countermodel's compatible-field example (+4/+8 container
   roles vs +0x14/+0x18 range roles — disjoint offsets) shows the examined window's
   field usage is compatible with a single aliased object.
3. **The callback return can alias its receiver.** The callback receives ECX =
   element (an address derived from the tracked range chain) and its return EAX is
   then dereferenced ([EAX]/[EAX+4] @0x006C3668/0x006C366C). A callback that returns
   its receiver makes those reads touch element memory. **No direct EDI-based
   memory operand does not prove that the same address is never read through EAX.**
   The census fact (0 direct EDI/EBP/EBX-based memory operands) stays valid; the
   absolute "never dereferenced" is narrowed to "no DIRECT dereference in-window;
   indirect dereference through the closed callback's return is NOT EXCLUDED".
4. **Correct the dependent F2/F8 and gate conclusions accordingly** — F8 is
   re-classed from an address-inequality proof to a producing-chain-disjointness
   observation (countercheck class); F2's "never dereferenced" is narrowed; G4's
   "container ≠ template" cell and G5's aggregate are re-labeled (§5 below).

### FC-C3 — local container operation vs categorical placement exclusion

**Old claim shape (to be superseded):** "FUN_006C3640 … is therefore NOT a
world-placement consumer" / "NOT a world-placement consumer. The world-placement
question, if any, would live inside the CLOSED callee 0x008BD720" (FINAL_REPORT §1/
§8; HANDOFF verdict + 12-line summary #1; entrypoint row "GENERIC RANGE-COLLECT/MAP
UTILITY - NOT a world-placement consumer") — a categorical exclusion of the function
(and, in the entrypoint summary, of the placement branch) derived from a window with
generic range/callback/container operations and 0 FPU/SSE.

**Corrected semantics to adjudicate (registered BEFORE checking):**

1. **Retain the generic range/callback/container operations** — range begin/end role
   of arg2/arg3, stride 0x20, per-element thiscall callback dispatch, fast-path
   two-DWORD copy, cursor/end container management, growth delegation, out-slot
   store: GENERIC_RANGE_CALLBACK_CONTAINER_MECHANISM = CONFIRMED_IN_EXAMINED_WINDOW.
2. **Replace the categorical placement exclusion with
   DIRECT_TRANSFORM_OPERATION = NOT_ESTABLISHED** (in-window: 0 FPU/SSE
   machine-measured, pointer arithmetic only — this negative is valid FOR THE
   EXAMINED WINDOW) **and ROLE_IN_PLACEMENT_PIPELINE = UNRESOLVED** and
   **PLACEMENT_BRANCH_EXCLUDED = NO**.
3. **Absence of FPU/SSE does not exclude float bit copies** (two DWORDs can carry
   float/identifier/structure-fragment bits through the generic copy) **or
   participation in a placement pipeline** (a generic range-collect utility can be
   a stage of one). The quarantined callback hypothesis (16 B dump
   `8D 41 18 C3` + 12×CC — same thunk family shape as the byte-proven W-DEP1
   `8D 41 14 C3`) explicitly illustrates a mechanism by which the container could
   collect the last 8 bytes of each 0x20-byte element — it stays a QUARANTINED
   HYPOTHESIS, not a claim.
4. **The old confinement of the placement question to the single callback is too
   strong:** the element-producer context (who fills the 0x20-stride range) and the
   downstream consumer of the collected pairs remain SEPARATE unknowns.
5. The package's own more careful §7.6 wording ("Transform-relevant operation?
   NOT_ESTABLISHED") is the justified maximum; the categorical sentences are
   superseded to match it.

### P3 sentence — "callee reads all six arguments"

**Old (ARGUMENT_PROVENANCE.json:20, calling_convention.register_arguments):** "NONE -
the callee reads all six arguments from the stack ([esp+disp] at entry push depths…)".
**Corrected:** the callee's DIRECT stack-slot usage is **arg1–arg5** (arg2 @0x006C3646,
arg3 @0x006C3641, arg4 @0x006C3654/@0x006C36A0, arg5 @0x006C364F, arg1
@0x006C3691/@0x006C369C + &arg1 LEA @0x006C367C); **arg6's slot (entry_offset 0x18)
has ZERO direct accesses** — the callee does NOT read all six arguments. The
register-argument part of the old sentence ("no this-register argument…") stays
valid; the "all six" part is superseded.

### Falsifier-label correction (Desktop §5)

The old aggregate "8/8 falsifiers executed PASS" mixed different control classes.
Corrected classification to adjudicate (each of the 8 labeled with its honest class;
the old single denominator is not forced):

| ID | What it actually was | Honest class |
|---|---|---|
| F1 | dual-side slot-derivation cross-join (caller pushes × callee read offsets); caught the contract's VA-annotation imprecision | COUNTERCHECK (detected a failure case) |
| F2 | enumeration of all 17 memory operands with base provenance | METHODOLOGICAL CENSUS (completeness; its "never dereferenced" absolute narrowed by FC-C2) |
| F3 | opcode-family scan (0 FPU/SSE) + naming discipline audit | METHODOLOGICAL DISCIPLINE CHECK (not a semantic proof) |
| F4 | register-preservation expectation audit across the two closed calls, with explicit ABI-assumption conditions | CONDITION RECORD (no mutation test was executed; bodies CLOSED) |
| F5 | per-path EAX writer/reader census (last-writer-wins) | COUNTERCHECK |
| F6 | Ghidra-quarantine audit (0 load-bearing Ghidra claims) | METHODOLOGICAL QUARANTINE CHECK |
| F7 | own decoder vs GNU objdump cross-verification (0/105 disagreements), defect history disclosed | CROSS-IMPLEMENTATION DECODE COUNTERCHECK (reproducibility) |
| F8 | container-vs-template provenance comparison | NEGATIVE CONTROL whose ADDRESS-INEQUALITY interpretation is SUPERSEDED by FC-C2; retains value only as a producing-chain-disjointness observation |

**None of the 8 was a mutation test on an actual helper body.** The mutation-class
evidence for the corrections is the LOGICAL countermodel reproduction below —
which is NOT actual execution of FUN_006C2E00.

## 3. Countermodel reproduction plan (registered BEFORE execution)

Reproduce the supplied logical countermodels from
CLAIM_SUFFICIENCY_COUNTERMODELS.json (attribution preserved) with
**INDEPENDENTLY WRITTEN short Python checks** — this executor's own small logic
demonstrations, written fresh for this run, not derived from or executed against any
Desktop script. **Explicit labels for every result:**
`LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00; NO
callback/helper body opened.`

| ID | Countermodel | Script (in-package path) | Expected shape (values = Desktop-supplied) |
|---|---|---|---|
| CM-1 | escaped-local: 3 cases (FAST_PATH; GROWTH_PRESERVES_LOCAL; GROWTH_MUTATES_ESCAPED_LOCAL) — a stub helper honoring the ABI conditions (nonvolatile registers preserved; expected stack cleanup preserved) can still mutate the escaped pair slot, changing the later arg6 | 00_RECORDS_CORRECTION/countermodels/cm1_escaped_local.py | later_arg6 = 305419896 / 305419896 / 2271560481; equal_initial true/true/false; stub_preserves_nonvolatile_registers true ×3; stub_preserves_expected_stack_cleanup true ×3 |
| CM-2 | alias: distinct producing chains (lookup-return vs incoming param_2) resolve to the same address; container-role fields (+4/+8) and range-role fields (+0x14/+0x18) are compatible disjoint offsets on one object | 00_RECORDS_CORRECTION/countermodels/cm2_alias_model.py | lookup_return == incoming_container == 2097152; same_address true; compatible field values +4=3145728, +8=3145984, +0x14=4194304, +0x18=4194336; no offset overlap |
| CM-3 | DWORD-copy-carries-float-bits: two floats survive a pure integer DWORD copy bit-identically (no FPU in the copy mechanism) | 00_RECORDS_CORRECTION/countermodels/cm3_dword_float_copy.py | 1234.5 → 0x449a5000 → 1234.5 bit_identical true; -42.25 → 0xc2290000 → -42.25 bit_identical true |
| CM-4 | escaped subject out-slot: the subject's &arg1 escapes to a stub helper that rewrites the slot; the late store then targets the REWRITTEN pointer, initial preservation false | 00_RECORDS_CORRECTION/countermodels/cm4_escaped_subject_outslot.py | initial_out_pointer 5242880; stub_rewritten 6291456; late_store_destination 6291456; initial_pointer_preservation false; lea_entry_offset 4 |
| CM-5 | callback-return-aliases-receiver (Desktop REPORT §3 prose shape): a stub callback returning its ECX receiver makes the subject's [EAX]/[EAX+4] reads touch element memory even though the DIRECT EDI-based operand count is 0 | 00_RECORDS_CORRECTION/countermodels/cm5_callback_return_alias.py | direct_edi_based_memory_operands = 0 (census-consistent); yet the copied pair == element[0:8] (the alias route reads the element) |

Expected values are embedded in each script as the Desktop-supplied constants
(sources cited in-script); each script self-checks measured vs expected and prints a
machine-readable result; raw stdout is captured under
`00_RECORDS_CORRECTION/countermodels/raw/`; each script's SHA256 is recorded in
COUNTERMODEL_RESULTS.json. If any countermodel fails to reproduce, it is recorded
honestly — not forced.

## 4. Expected artifacts of this phase

```text
AUTHORIZATION_AND_PREFLIGHT.md
INPUT_IDENTITIES.json
PREREGISTRATION.md                       (this file — written before the science)
00_RECORDS_CORRECTION/SUPERSESSION.md
00_RECORDS_CORRECTION/CORRECTED_CLAIM_MATRIX.json
00_RECORDS_CORRECTION/COUNTERMODEL_RESULTS.json
00_RECORDS_CORRECTION/countermodels/cm1_escaped_local.py
00_RECORDS_CORRECTION/countermodels/cm2_alias_model.py
00_RECORDS_CORRECTION/countermodels/cm3_dword_float_copy.py
00_RECORDS_CORRECTION/countermodels/cm4_escaped_subject_outslot.py
00_RECORDS_CORRECTION/countermodels/cm5_callback_return_alias.py
00_RECORDS_CORRECTION/countermodels/raw/*.json (captured stdout, one per countermodel)
INTERVENTION_LEDGER.md
```

(Packages B/C artifacts — 01_SDK/*, 02_PE/* and the publication-phase documents —
belong to LATER phases and are NOT created here.)

## 5. Pass/fail shape of this phase (registered BEFORE execution)

- **PASS** when: (a) the corrected claim matrix is **internally consistent** (every
  corrected status is compatible with the retained valid facts, with the raw
  evidence, and with the physical pins); (b) **every supersession is explicit**
  (OLD wording → NEW wording, with what stays valid and what becomes
  UNRESOLVED/NOT_ESTABLISHED, per correction); (c) **every countermodel reproduces**
  (or any non-reproduction is recorded honestly with its cause).
- **Material contradictions that cannot be resolved from existing evidence** (the
  Desktop findings vs the historical package's raw bytes, or an internal
  inconsistency of the corrected matrix) → **STOP subsequent science** (the SDK and
  PE phases do not proceed from a contradictory records state), write what exists
  with honest dispositions, and report the blocker to PE-MASTER. No silent
  adaptation; no opening of closed bodies to resolve a records question.
- This phase awards **no** Q1/PE-MASTER/M1/gate/placement qualification of any kind;
  CANONICAL_GATE_EFFECT = NONE regardless of outcome.
