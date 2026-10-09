# FINAL_REPORT — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

```text
RUN_ID      = PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009
RUN_CLASS   = MACHINERY_AND_CONTROL_CORRECTION
BASE_SHA    = 2ac7cfa1dcb2e53e9c86985c18377de811d5b485 (EXPECTED == LOCAL_HEAD
              == origin/master == actual remote at preflight)
SCOPE       = one correction only: repair the persisted-fact checks of the four
              BR-C1 relations in both ordinary artifact gates; preserve the
              scientific result and the original packages; NO new RE
OUTCOME     = BR_C1_IMPLEMENTATION = CORRECTED_IN_TESTED_SCOPE
              BR_C1_DESKTOP_CLOSURE = PENDING_POST_AUDIT
```

## 1. Identity and authorization

- Authoritative contract: `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_BR_C1_CORRECTION_PROMPT_REVIEW_20261009\OPENCODE_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009.md`
  — 18566 B, SHA256 `B30E807BFA24BC37A8FFC015D37B42EC96F72F47D8B6956AFA9512D09CDC1CE3`
  — verified byte-for-byte and read in full BEFORE any action.
- Execution authorization: the separate human message (2026-10-09) naming
  this exact contract and authorizing this correction-only run plus its
  allowlisted commit/fast-forward push. NEXT_EXPERIMENT_AUTHORIZED = NO.
- Executor: OpenCode agent pe-reconstruction (model nask-glm/glm-5-3).
  Single session; no nested agents (NO_NESTED_TASKS). Internal QC inside
  this run: EXECUTOR SELF_REVIEW only (a fresh-context QC is a separate
  later agent; recorded NOT_PERFORMED — see QC_REPORT.md).

## 2. Preflight (measured)

- Git triple: LOCAL_HEAD == origin/master == `2ac7cfa1dcb2e53e9c86985c18377de811d5b485`
  == EXPECTED_BASE_SHA. Tracked worktree/index clean; the six foreign
  untracked paths inventoried by the dispatching PE-MASTER were re-verified
  present-and-untouched and remain so.
- Both proposed output paths (OUTPUT_ROOT and OUTPUT_REPO_PATH) ABSENT
  before the run.
- All pinned inputs re-verified physically (contract, revised predecessor
  contract, Desktop REPORT.md / AUDIT_COUNTERCHECKS.json /
  SECOND_PASS_VERIFICATION.json, predecessor package files incl. the four
  contract-pinned ones, Entropia.exe). Predecessor package: 35/35 physical
  files EQUAL their committed Git blobs at BASE_SHA; full before/after
  hash inventory identical (see INPUT_IDENTITIES.md).
- EXE: 8015872 B / `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`;
  re-hashed before and after every driver phase: UNCHANGED.

## 3. PRE — the demonstrated defect, reproduced through the ACTUAL predecessor gates

The actual predecessor `gate_artifacts()` / `gate()` were imported UNMODIFIED
from the source package (module hashes recorded in PRE_ARTIFACT_RESULTS.json:
run_frame_bridge.py `0DB331D85526333EB91B12E480B4D57A7C32BE6FE0B0611B20E4938FA038268B`,
qc_frame_bridge.py `EC9F3FBE152E7694B0E2540E1BB4F399994BBAB81CE8B33B64495B25A3CE1688`),
deep-copied BRIDGE_PROVENANCE.json loaded through their normal provenance
override (PREDECESSOR gates; the predecessor CLI mains were never invoked;
all writes redirected to SCRATCH):

| Case | Exact mutation (deep copy) | Production | QC |
|---|---|---|---|
| CLEAN | none (package original) | **PASS** (21/21 checks) | **PASS** (21/21 checks) |
| AC1 | arg1.value_kind=STACK_READ; value_expr=MEM(T+0x8) | **REJECTED** (PROV-B-ARG1-KIND, PROV-B-LEA-EXPR) | **REJECTED** (PROV-B-KIND, PROV-B-LEA) |
| AC2 | source_slot [E+4] -> [E+0x8], delta 8 | **REJECTED** (PROV-A-SLOT) | **REJECTED** (PROV-A-SLOT) |
| BR1 | call target + target_recomputed -> 0x00528E51; bridge_valid=false | **PASS (false-PASS)** | **PASS (false-PASS)** |
| BR2 | arg1 slot -16 -> -12 (all three slot representations) | **PASS (false-PASS)** | **PASS (false-PASS)** |
| BR3 | bridge summary -> STACK_READ / MEM(T+0x8) (3 fields) | **PASS (false-PASS)** | **PASS (false-PASS)** |
| BR4 | null_path call_reached=true; je_taken=false | **PASS (false-PASS)** | **PASS (false-PASS)** |

**PRE_REPRODUCTION = REPRODUCED**: CLEAN PASS both gates; AC1/AC2 rejected
in both (4 expected outcomes); BR1–BR4 passed in both gates — **8
false-PASS outcomes**, matching the Desktop post-audit finding exactly
(BR_C1 = CONFIRMED_OPEN_P2). The predecessor clean gate has exactly 21
checks; none covers the four BR-C1 relations' persisted fields. PRE was
recorded as measured and NEVER rewritten to match POST. The Desktop
findings were used only as a map; no Desktop verdict entered any gate
derivation.

## 4. POST — the corrected gates (narrow machinery repair)

Corrected COPIES under 03_SCRIPTS/ (predecessor -> corrected, SHA256):

| File | Predecessor SHA256 | Corrected SHA256 |
|---|---|---|
| run_frame_bridge.py (103544 B) | `0DB331D8...` | `1b11b3a152696c0090c51f3c4507dc575ef87cd6eb0caf7bd99e6b461772b6b3` (123758 B) |
| qc_frame_bridge.py (83103 B) | `EC9F3FBE...` | `1d6e168cb290923a855f2f9f41cc30ab40c01464ba128dbd50fd24b594b8be73` (102397 B) |

Changes are confined to ordinary artifact-gate logic, small
field-reading/type/expression comparison helpers, the test driver and
isolated path routing (CODE_DIFF.patch; all hunks in the gate sections —
production lines ~1690–2260, QC lines ~860–1400). PRESERVED UNCHANGED:
byte decoders (parse_objdump/parse_dump), symbolic engines
(exec_instr/exec1), derivations (derive_a/derive_b), CASE_ORDER, original
MUTATIONS/EXPECTED/EXP definitions — mechanically proven by the
regression's preservation checks (all six dict/list comparisons
IDENTICAL).

The corrections (both gates, each gate deriving from its own evidence —
production: persisted objdump text + independent_esp_walk; QC: its own
objdump invocations + esp_walk/parse/opcode bytes; the QC imports nothing
from the production verdict):

1. **BR-C1.1 CALL identity**: the persisted `call.va`, `call.target`,
   `call.target_recomputed` and `call.bridge_valid` are each read from the
   JSON under test and compared to the rel32-derived target of the
   instruction at the pinned callsite 0x004C47C1 and the derived bridge
   predicate (target == window-A entry 0x00528E50). Native types enforced:
   target VA strings in 0xXXXXXXXX form; bridge_valid a JSON boolean
   (string "true" rejected; false is not a valid positive predicate).
   The existing pinned-role rel32 checks are retained as ADDITIONAL checks.
2. **BR-C1.2 argument-slot identity**: `arg1.slot_delta_T0`,
   `arg_slot_deltas.arg1`, `bridge.b_arg1_slot`, `bridge.E_delta_from_T`,
   the exported `esp_before_call_delta_T0` (-16) and
   `callee_entry_esp_delta_T0` (-20) compared to the walk-derived slot/E
   deltas; the entry-slot relation [E+4] == [T-0x10] is DERIVED
   (E delta + A entry delta == B slot delta; -20 + 4 == -16) and the
   persisted claims must satisfy it — duplicate claims are not merely
   compared to each other. `bridge.a_source_slot_from_T` and the A-side
   source-slot fields remain covered by the existing PROV-BRIDGE-SLOT /
   PROV-A-SLOT checks (the former now field-presence-safe). JSON booleans
   are rejected as integers.
3. **BR-C1.3 pointer value and duplicate bridge summary**:
   `arg1.{value_kind,value_expr,value_delta}`,
   `arg_slots.arg1.{kind,expr,delta}` (the documented "T0+0x8 (computed)"
   form explicitly normalized), `bridge.{b_arg1_value_kind,
   b_arg1_value_expr,cross_call_value_expr}` — each compared INDIVIDUALLY
   to the opcode/LEA-derived facts; the previous OR-fallbacks (which let a
   contradictory parallel bridge summary hide behind the first
   representation) are REMOVED. A parallel-consistency check requires the
   three kind representations and three value expressions to agree with
   each other AND with the derivation. A's STACK_READ
   (`bridge.a_delivered_value_kind`, `phase_a.delivery.arg1_value_kind/expr`)
   is validated as the argument-slot load of the joined slot [E+4] —
   MEM(E+0x4)@0x00528E84 — never reclassified as a B-side pointee read; the
   clean pointer remains ADDRESS(T+8), never MEM(T+8).
4. **BR-C1.4 local null path**: `null_path.{branch_va,branch_mnemonic,
   exit_va,exit_inside_window,je_taken,unconditional_exit,call_reached}`
   compared to the B-window branch derivation (decoded JE instruction,
   target 0x004C47C8 outside the window interval, opcode 0x74 conditional;
   TEST EAX,EAX -> ZF=(EAX==0) with no intervening flag writer -> JE taken
   for EAX==0; the taken path exits the window before CALL 0x004C47C1).
   Native JSON booleans enforced. 0x004C47C8 remains UNOPENED; no claim
   about its later behavior.
5. Named diagnostics for every failure class — MISSING_FIELD:<path>,
   WRONG_TYPE:<path>:expected/got, MALFORMED_EXPR:<path>:reason,
   VALUE_MISMATCH:<path>:derived/got — with no uncaught exception, no
   silent auto-repair, no eval, and no general-purpose schema engine.

Clean final validation through the SAME corrected gates (no override):
production PASS 50/50 checks, QC PASS 50/50 checks (21 predecessor checks +
29 new per gate).

## 5. Controls

### 5.1 Fixed artifact matrix (7 cases x 2 gates = 14 outcomes; POST)

| Case | Production | QC | Expected | Result |
|---|---|---|---|---|
| CLEAN | PASS | PASS | PASS | OK |
| AC1 | REJECTED | REJECTED | value provenance | OK (PROV-B-ARG1-KIND/PROV-B-LEA-EXPR/PROV-BR13-PARALLEL-CONSISTENCY; QC: PROV-B-KIND/PROV-B-LEA/QC-BR13-PARALLEL-CONSISTENCY) |
| AC2 | REJECTED | REJECTED | entry slot | OK (PROV-A-SLOT both) |
| BR1 | REJECTED | REJECTED | persisted CALL identity | OK (PROV-BR11-CALL-TARGET/TARGET-RECOMPUTED/BRIDGE-VALID; QC equivalents) |
| BR2 | REJECTED | REJECTED | slot identity | OK (PROV-BR12-ARG1-SLOT-DELTA/ARG-SLOT-DELTAS-ARG1/B-ARG1-SLOT/SLOT-RELATION) |
| BR3 | REJECTED | REJECTED | contradictory bridge value | OK (PROV-BR13-B-ARG1-VALUE-KIND/B-ARG1-VALUE-EXPR/CROSSCALL-VALUE-EXPR/PARALLEL-CONSISTENCY) |
| BR4 | REJECTED | REJECTED | null-path facts | OK (PROV-BR14-NULL-JE-TAKEN/NULL-CALL-REACHED) |

**FIXED_ARTIFACT_MATRIX = 14/14. AC1_AC2 = 4/4 rejected. BR1_BR4 = 8/8
rejected.** For every rejection: zero hash/identity-side failures
(WID-/EFL-/CSL- checks all PASS), zero exceptions, and the expected named
BR-C1 predicate(s) among the failing checks (a hash-side failure, crash or
unrelated predicate failure would NOT have counted). Only the isolated
mutated provenance copies (SCRATCH/prov/, outside Git) bypass
hash/manifest-side checks.

### 5.2 FIELD_CHECK_COVERAGE + additional single-field controls

FIELD_CHECK_COVERAGE.csv: 34 rows — 32 field representations (BR-C1.1: 4;
BR-C1.2: 10 incl. the relation row; BR-C1.3: 13 incl. the consistency row;
BR-C1.4: 7) with PERSISTED_FIELD_PATH, ACTUAL_PERSISTED_VALUE,
DERIVED_EXPECTED_VALUE, EVIDENCE_SOURCE, WHY_NON_CIRCULAR, both gates'
check names, the single-field FAILURE_CASE_DETECTED and GATE_VERDICT
(PASS in the clean gates).

Each representation was additionally mutated INDIVIDUALLY (leaving its
clean duplicates and all other evidence unchanged), proving every corrected
comparison live — including target (SF-C1-2) and target_recomputed
(SF-C1-3) individually, since a bridge_valid-only rejection cannot prove
their coverage. Dynamic counts, kept separate from the fixed matrix:

```text
single-field controls        = 32 cases  -> 64/64 correct rejections
missing-field controls       =  4 cases  ->  8/8   (MISSING_FIELD diagnostics)
wrong-native-type controls  =  5 cases  -> 10/10  (incl. boolean-as-integer,
                                                   int-as-boolean, string "true")
malformed-expression cases  =  2 cases  ->  4/4   (MALFORMED_EXPR diagnostics)
TOTAL additional            = 43 cases / 86 outcomes -> 86/86 correct
```

### 5.3 Regression (unchanged existing byte matrices, existing bounded helpers)

Re-executed through the corrected copies' PRESERVED helpers (all writes
redirected to SCRATCH; python3 -B; tool GNU objdump 2.44, rc 0 recorded):

- Production 12-case matrix: 12/12 CONTROL_PASS (A_CLEAN, B_CLEAN_NONNULL,
  B_CLEAN_NULL, M1–M9).
- QC 12-case matrix: 12/12 CONTROL_PASS (its own expected-fact encodings).
- **REQUIRED_BYTE_MATRIX = 24/24.**
- M5/M7 arg1-retention reported alongside the changed channels:
  production M5 — arg1 kind ADDRESS / expr ADDRESS(T+0x8) / slot -0x10
  UNCHANGED while arg3/arg4 swapped (each verified to equal the clean
  other's value); production M7 — arg1 unchanged while receiver changed
  (OPAQUE_RET -> UNKNOWN_REG); QC M5/M7 — arg1 kind/slot unchanged, arg3/4
  swapped / receiver changed. All verified true on both sides.
- The same corrected gates were used for the clean final validation and
  every artifact control; no test-only validator exists (the gates are the
  package scripts; the driver only orchestrates and records).

## 6. Fresh internal QC (honest scope) and preserved science

- INTERNAL_QC_ORIGIN = SELF_REVIEW (43 mechanical checks, 43/43 PASS —
  PRE/POST separation, control causality, coverage liveness, regression,
  run-level safety; see QC_RESULTS.json / QC_REPORT.md). A fresh-context
  internal QC is a SEPARATE LATER agent: FRESH_CONTEXT_INTERNAL_QC =
  NOT_PERFORMED and no internal QC_PASS is issued. One in-run defect was
  found by self-check and repaired within the four-relation scope: the
  driver's coverage-CSV writer had a variable-shadowing defect (the CSV was
  written to a stray file); after the fix ALL phases were re-executed from
  scratch with the final driver bytes (identical outcomes); stray files
  removed (disclosed in QC_REPORT.md as F-QC-1).
- Preserved WITHOUT semantic promotion (see SUPERSESSION_AND_STANDING.md):
  CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL;
  BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL;
  CONDITIONS = AS1-AS5 + EAX!=0 unchanged; POINTEE_CONTENTS_PROVENANCE =
  UNRESOLVED_UPSTREAM; FIELD_SEMANTICS = UNVERIFIED;
  WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT =
  NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO; CANONICAL_GATE_EFFECT = NONE.
  J3 supersessions kept; no ACLD/CMO identity transfer. No contradiction
  with preserved science emerged incidentally (the corrected gates
  re-validated every clean persisted value: 50/50 per gate).

## 7. Scope census (measured)

```text
AUTHORIZED_PARTIAL_CODE_WINDOWS     = 2 (EXISTING A 66 B, B 52 B; replay/verify only)
NEW_CODE_REGIONS / CALLEES / XREF   = 0 (0x004C47C8 unopened; no pointee research)
SCIENCE_REDERIVATION                = 0 new science (gates re-validate existing facts)
FIXED_ARTIFACT_MATRIX               = 14/14
ADDITIONAL_CONTROLS                 = 43 cases / 86 outcomes, 86/86
FIELD_CHECK_COVERAGE_ROWS           = 34 (32 fields + 2 derived checks)
REQUIRED_BYTE_MATRIX                = 24/24
PREDECESSOR_SOURCE_PACKAGE_CHANGED  = 0 of 35 files
EXE_CHANGED                         = NO (re-hashed every phase)
RUNTIME / NETWORK / MODEL / VFS_BNT_NIF / GAMEBRYO-OPENMW = 0
```

## 8. Terminal status

```text
BR_C1_IMPLEMENTATION          = CORRECTED_IN_TESTED_SCOPE
BR_C1_DESKTOP_CLOSURE          = PENDING_POST_AUDIT
INTERNAL_QC_ORIGIN             = SELF_REVIEW
INTERNAL_QC_VERDICT            = NOT_PERFORMED (fresh QC = separate later agent)
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
SOURCE_PACKAGE_UNCHANGED       = YES (35/35)
SCIENTIFIC_CLAIMS              = PRESERVED
WORLD_XYZ_RECOVERED            = NO
CANONICAL_GATE_EFFECT          = NONE
NEXT_EXPERIMENT_AUTHORIZED     = NO
HARD_STOP                      = YES
```

Publication (package + one truthful AUDIT_ENTRYPOINT.md row, allowlisted
normal commit + fast-forward push) is performed as the contracted terminal
step; the resulting commit SHA is the audit target for the later
independent Desktop post-audit. No automatic follow-up RE or correction
cycle follows this report.
