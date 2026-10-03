# FINAL_REPORT — PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003

```text
RUN_ID = PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003
RUN_CLASS = LOAD_BEARING
RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION (finding F2/P1 ONLY)
EXECUTOR = pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)
BASE_SHA = ee60930a2b1094588ab3be490eefd3cce291c9d1 (verified at run start:
  local HEAD == local origin/master == actual remote master)
AUDITED_FINDING = F2/P1 of the Desktop post-audit
  C:\Users\User\Documents\ChatGPT\PE\
  PE_GAMEBRYO_ORACLE_TOOL_DESKTOP_POST_AUDIT_20261003\REPORT.md
SCOPE GUARD = F3, F4, F5, F6, F7, O1, T3 NOT addressed; no Gamebryo class
  loaders added; no corpus-wide decode; no PCG EXE RE; no placement trace;
  probe-version/compare/capabilities exit semantics UNCHANGED
STATIC-ONLY: the client never ran; the original GB 1.2 toolchain never ran

F2_ACCEPTANCE_COVERAGE_LINK = FIXED_AND_VERIFIED
RUN_STATUS = PASS (bounded to the F2 mission; commit is not scientific PASS)
```

## 1. The defect (Desktop F2/P1, re-measured PRE-FIX on BASE)

The final success predicate of `gb12core.py` promoted `accepted=true` (CLI
`inspect` exit 0) whenever (a) no unregistered RTTI TABLE entry existed and
(b) every `objects[]` slot was non-NULL. A
REGISTERED_BUT_NOT_DECODED_BY_ADAPTER boundary-only placeholder is non-NULL
but is NOT a semantic decode, and a LINK_FAILURE / out-of-range link was
only a warning that did not participate in the predicate.

Both false-success classes were REPRODUCED PRE-FIX on OUR OWN fixtures on
the pristine BASE worktree (raw records in `02_RAW_TESTS/`):

| fixture | PRE-FIX measured | verdict |
|---|---|---|
| fx_REGNOTDEC (NiNode / NiCamera-registered-no-loader / NiNode; the unsupported block is MID-file, NOT a trailing unknown run — the known F4 presolver defect is deliberately not exercised) | `accepted=true partial=false exit 0`, 3/3 slots non-NULL incl. the NiCamera boundary-only block (status REGISTERED_BUT_NOT_DECODED_BY_ADAPTER, bytes 173..189), zero warnings | FALSE SUCCESS reproduced |
| fx_INVALID_LINK (fully supported NiNode, children=[9999], num_blocks=1, structurally closed) | `accepted=true partial=false exit 0`, LINK_FAILURE warning present, children resolved `["LINK_ERROR_OUT_OF_RANGE"]` | FALSE SUCCESS reproduced |
| fx_VALID (positive control) | `accepted=true exit 0` | correct, must stay |

## 2. The fix (four explicit, separate axes — never conflated)

`gb12core.py` now derives FOUR axes on EVERY return path; TOOL_VERDICT is
derived in ONE place; the ONLY removed logic line in the whole diff is the
pre-F2 false-success predicate (`git diff` census: 1 removed line in
gb12core.py; all else additions).

1. **SOURCE_PREDICTED_ORIGINAL_VERDICT** ∈ {ACCEPTED, REJECTED, UNRESOLVED}
   — what the ORIGINAL GB 1.2 Load() would do, predicted ONLY from pinned
   source evidence (all source SHA256s re-verified this run; see
   INPUT_IDENTITIES §2):
   - REJECTED (unambiguous, source-proven): header "File Format" test
     (NiStream.cpp L311-316); version gate (L320-332); RTTI table factory
     miss (L421-433 → LoadStream L524-525); legacy inline factory miss
     (LoadObject L457-462 → L557-561).
   - UNRESOLVED (evidence insufficient): registered-but-not-decoded classes
     (the factory KNOWS the class — registration is NOT an original
     rejection; the class's LoadBinary/link/postlink path on the bytes is
     not traced in the pinned evidence, and NO new broad source RE was done
     to reach ACCEPTED); detected out-of-range links — pinned proof:
     GetObjectFromLinkID L245-256 carries only a DEBUG-only
     `assert(uiLinkID < m_kObjects.GetSize())` and NiTArray::GetAt
     (NiTArray.inl L136-139) is an UNCHECKED raw `m_pBase[uiIndex]` read
     (release = undefined behavior; debug = assert); LinkObject is void and
     its return is discarded at LoadStream L576, and L634 returns true
     unconditionally — no unambiguous propagated rejection exists (per the
     contract's SOURCE LINK SEMANTICS rule); the object-index stage
     (L441 assert is DEBUG-only; release calls `ppfnCreate[usRTTI]` OOB);
     closure failures (OUR closure search is OUR extension); unreadable
     header line (GetLine-at-EOF not pinned).
   - ACCEPTED only when the full pinned LoadStream path (L506-635) is
     content-valid for the stream: every block decoded by a
     pinned-citation loader, every link NULL or in range, closure exact.
     Proof chain for the traced paths: LoadBinary loop L538-564; link loop
     L569-578 and postlink loop L581-590 call VOID methods whose returns
     are DISCARDED (NiNode.cpp L872-905 blind-casts and STORES resolved
     pointers; NiNode/NiAVObject do NOT override PostLinkObject — only the
     empty NiObject::PostLinkObject and the legacy NiObjectNET::PostLinkObject
     exist); CheckConsistency is a Win32 no-op (NiStream.inl L193-196);
     return true at L634 is unconditional.
2. **ADAPTER_DECODE_COVERAGE** ∈ {COMPLETE, INCOMPLETE, NOT_MEASURED} with
   `adapter_decode_coverage_counters` (header_num_blocks,
   semantically_decoded_blocks, boundary_only_blocks,
   registered_but_not_decoded_blocks, unregistered_blocks,
   unresolved_blocks, registered_but_not_decoded_classes): every counter
   is an integer when actually measured, else null with an explicit
   per-counter `not_measured_reasons` entry (a measured ZERO is never a
   substitute for unknown). After an early RTTI halt (ordinary factory
   rejection or F1-C1 STOP_AT_TABLE_FAILURE) the object-level counters
   are NOT derived from RTTI table names (a table entry is NOT an object
   reference) and no extra object indices are read just to count coverage.
   On closure-failure paths the per-block state comes from ABANDONED
   search branches and is reported as NOT_MEASURED, not as counts.
3. **ADAPTER_INTEGRITY** ∈ {PASS, FAIL, UNRESOLVED, NOT_MEASURED}
   (`adapter_integrity_checks`: object_count_consistency,
   structural_closure, link_integrity, link_failure_count,
   link_measured_blocks): an out-of-range link ⇒ LINK_INTEGRITY=FAIL ⇒
   ADAPTER_INTEGRITY=FAIL (no longer a warning). FAIL dominates the
   aggregation.
4. **TOOL_VERDICT** ∈ {PASS, FAIL, UNRESOLVED}, derived in one place:
   PASS only if coverage=COMPLETE AND integrity=PASS AND no
   source-predicted REJECTED; FAIL if integrity=FAIL OR source=REJECTED
   (a known detected invalid link must NEVER end UNRESOLVED); UNRESOLVED
   otherwise. `load_result.accepted` is exactly (TOOL_VERDICT == PASS)
   (explicit `load_result.accepted_semantics` note; never a claim about
   the original runtime), and the CLI `inspect` exit is 0 ONLY on
   TOOL_VERDICT=PASS. Adapters without the F2 axes (gb26/gb112/gb23) keep
   their accepted-based exit semantics (verified: gb26 inspect exit 2
   unchanged). probe-version / compare / capabilities are UNCHANGED
   (byte-identical outputs pre/post — 5 snapshot pairs).

## 3. POST-FIX measured results (raw records in `02_RAW_TESTS/`)

| fixture | exit | accepted | SOURCE | COVERAGE | counters (hdr/sem/bnd/rnd/unreg/unres) | INTEGRITY | TOOL |
|---|---|---|---|---|---|---|---|
| fx_VALID (positive control) | 0 | true | ACCEPTED | COMPLETE | 1/1/0/0/0/0 | PASS | PASS |
| fx_REGNOTDEC ordinary | 2 | false | UNRESOLVED | INCOMPLETE | 3/2/1/1/0/0; classes=[NiCamera] | UNRESOLVED (links 2/3 measured; boundary block contributes no link list) | UNRESOLVED |
| fx_REGNOTDEC --full-decode | 2 | false | UNRESOLVED | INCOMPLETE | 3/2/1/1/0/0 | UNRESOLVED | UNRESOLVED |
| fx_INVALID_LINK ordinary | 2 | false | UNRESOLVED | COMPLETE | 1/1/0/0/0/0 | FAIL (link_integrity=FAIL, link_failure_count=1) | FAIL |
| fx_INVALID_LINK --full-decode | 2 | false | UNRESOLVED | COMPLETE | 1/1/0/0/0/0 | FAIL | FAIL |
| fx_C1A full (F1-C1 pin) | 2 | false | REJECTED | NOT_MEASURED | 1/null×5 + reasons | NOT_MEASURED | FAIL |
| fx_C1B full (F1-C1 pin) | 2 | false | REJECTED | NOT_MEASURED | 1/null×5 + reasons | NOT_MEASURED | FAIL |
| T1/218757 full | 2 | false | REJECTED | INCOMPLETE | 66/62/4/0/4/0 | UNRESOLVED (links 62/66 measured, 0 failures) | FAIL |
| T1/218757 ordinary | 2 | false | REJECTED | NOT_MEASURED | 66/null×5 + reasons | NOT_MEASURED | FAIL |

Required POST-FIX predicates — ALL MET:
- Counterexample A: factory_registration=YES (independently verified:
  NiCamera IS in the 198-class SDM registry census and NOT in the 39
  adapter LOADERS); ADAPTER_DECODE_COVERAGE=INCOMPLETE;
  registered_but_not_decoded_blocks=1 ≥ 1; TOOL_VERDICT != PASS
  (UNRESOLVED); CLI inspect exit != 0; SOURCE_PREDICTED=UNRESOLVED (no
  new broad source RE was done to reach ACCEPTED; NiCamera.cpp was read
  only as a read-only existence check, NO loader was added).
- Counterexample B: ADAPTER_DECODE_COVERAGE=COMPLETE; LINK_INTEGRITY=FAIL;
  ADAPTER_INTEGRITY=FAIL; TOOL_VERDICT=FAIL (never UNRESOLVED for a known
  detected invalid link); CLI inspect exit != 0; SOURCE_PREDICTED=UNRESOLVED
  (the pinned source proves only debug-assert/release-UB dependence — the
  contract's rule for no unambiguous propagated failure).
- Positive control: COMPLETE / PASS / PASS / exit 0 — no over-fail-closed
  (additionally verified in-run: a fully-valid 2-NiNode scene with a real
  in-range children link also reaches TOOL PASS with edges + links
  resolved).

## 4. F1 / F1-C1 regression (MANDATORY battery + pinned bytes)

- Full battery `tests/test_gb12.py --self`: **42 checks, 0 failures**
  (count from actual execution/enumeration: 11 self + 8 F1 + 11 F1-C1 +
  12 new F2 checks). The whole earlier F1 battery remains PASS; both
  F1-C1 counterexamples remain PASS on byte-regenerated pinned bytes
  (C1A 94 B / SHA256 928A1447A3F6911DAD96495307AAA97340133186223AA3B4288CFB
  4E493A5FCF; C1B 196 B / SHA256 719A7EB36E9D2B80E648A03C39C1D5A164586D4A
  C1532F6F0ACE681FB1C382D6): STOP_AT_TABLE_FAILURE preserved, earlier
  RTTIError(NiDesktopFirstMissing) preserved, objects=[], no
  histogram/census/groups, structured JSON, CLI exit != 0 — semantics
  unchanged. Their object-level coverage counts are NOT_MEASURED/null
  (never derived from the RTTI table).
- Payload battery (T1 sandbox copy, mutating controls): 7 PASS + the
  **2 PRE-EXISTING control failures** (`object_count_mismatch_detected`,
  `link_failure_detected` — controls that cannot fire on RTTI-failing
  payloads in ordinary mode) — failure set IDENTICAL pre/post (both
  batteries raw-captured in the package).
- F1 fixture A (registered-only baseline, == the byte-identical
  fx_VALID positive control): accepted=true preserved.

## 5. T1 targeted regression (04_REGRESSION/)

- Input identity re-verified: SIZE 57316, SHA256 3E8A22C2... (PINNED
  MATCH; no BLOCKED_T1_IDENTITY). T1 is read-only, never committed.
- `compare_t1_regression.py`: **9/9 PASS**. complete `objects[]` 66/66
  DEEP-IDENTICAL vs the accepted baseline state (the PRE-FIX ee60930
  full-decode result; every field recursively compared: values,
  transforms, links, byte_start/end/size, status, type/name, all others).
  The whole-JSON delta vs BASE is EXACTLY the 9 new F2 metadata keys
  (SOURCE_PREDICTED_ORIGINAL_VERDICT, source_predicted_reason,
  ADAPTER_DECODE_COVERAGE, adapter_decode_coverage_counters,
  ADAPTER_INTEGRITY, adapter_integrity_checks, TOOL_VERDICT,
  tool_verdict_reason, load_result.accepted_semantics) — zero
  non-F2 metadata differences, zero objects[] differences.
- Interpretation label preserved exactly: 62 known semantically decoded
  records + 4 opaque/boundary-only records — NOT promoted to 66 semantic
  decodes. FIRST_RTTI_MISS=NiArkAnimationExtraData@1 preserved;
  SOURCE_PREDICTED=REJECTED; TOOL_VERDICT != PASS (FAIL);
  WORLD_PLACEMENT_RECOVERED=NO. Deterministic run1==run2.
- Ordinary-mode T1: FIRST_RTTI_MISS + SOURCE_PREDICTED=REJECTED preserved;
  object-level coverage NOT_MEASURED (never derived from the RTTI table
  on the ordinary early-rejection path); exit 2 unchanged.

## 6. SELF_CHECK_F2 QC (executor self-check; NOT independent QC)

`03_QC_SELF_CHECK/qc_reexecution.py` — **22/22 PASS** (`qc_reexecution.stdout`
+ `QC_REEXECUTION_COUNTEREXAMPLES.json`):
- QC re-executed through the CLI with input identity + command + stdout +
  stderr + exit code for the mandatory set: VALID_SUPPORTED,
  REGISTERED_BUT_NOT_DECODED, INVALID_LINK, C1A, C1B (ordinary + full
  where applicable); all fixtures regenerated from the COMMITTED generator
  into the EXTERNAL sandbox and pin-verified (incl. battery-fixture byte
  identity and the C1A/C1B historical pins).
- 0 vs NOT_MEASURED/null never conflated (measured zeros are int 0;
  unknown counters are None with explicit per-counter reasons).
- Early RTTI halt creates NO object-level coverage census (objects=[],
  no histogram/census/groups keys, counters null).
- ADAPTER_INTEGRITY=FAIL always ⇒ TOOL_VERDICT=FAIL (BADLINK; plus the
  battery-wide law check `f2_integrity_fail_implies_tool_fail_and_
  accepted_eq_pass` over all battery results).
- inspect exit semantics changed per F2: for EVERY re-executed record,
  exit==0 ⇔ TOOL_VERDICT==PASS (no default-success fallback).
- probe-version / compare / capabilities UNCHANGED: byte-identical
  outputs pre/post (probe on fx_VALID; capabilities all + gb12; compare
  with the pinned --oracle-result pair AND the internal-inspect pair).
- Determinism: double re-execution identical on all three core fixtures.

P3 hygiene (explicitly ordered by the human):
- FINAL verification pass on the exact published code state
  (`03_QC_SELF_CHECK/FINAL_battery_with_payload.stdout`: 49 PASS + exactly
  the 2 pre-existing payload control failures; `qc_reexecution.stdout`
  final re-run 22/22; `04_REGRESSION/T1_REGRESSION_FINAL.stdout`: 9/9).
- Synthetic .nif fixtures are repo-gitignored (`*.nif`) and are kept
  OUTSIDE the published package root (external sandbox
  `C:\Users\User\AppData\Local\Temp\opencode\
  PE_GAMEBRYO_ORACLE_F2_20261003\sandbox\01_FIXTURES\`); the committed
  generator reproduces them byte-identically with SIZE/SHA256 pins and a
  reproduction command. The package root contains NO ignored/runtime-local
  inputs (verified: zero *.nif under the package) — the committed package
  manifest bijection is verified WITHOUT a separate LOCAL_RUNTIME_INVENTORY
  (none exists under the package root).
- P3 TEST COUNT: all test counts in this report are from actual
  execution/enumeration, never hand-hardcoded: 42 battery checks
  (11 self + 8 F1 + 11 F1-C1 + 12 F2) + 9 payload controls (7 PASS + 2
  pre-existing failures) + 22 QC re-execution checks + 9 T1 regression
  checks.

## 7. Honest NOT_CHECKED / out-of-scope observations (NOT fixed)

- OPTIONAL OBJECT-COUNT CONTROL not separately exercised: no small existing
  fixture reaches an object-count mismatch without entering other failure
  classes (on RTTI-failing payloads the mutation control hits the
  pre-existing control failure). The wiring is in place (object-count
  consistency is an integrity sub-check; mismatch ⇒ FAIL ⇒ TOOL FAIL; the
  closure-failure path FAILs via structural_closure) — per the contract,
  the run was NOT expanded for it.
- Top-object root IDs (LoadTopLevelObjects links) are reported as read and
  are not separately range-checked (out of F2 scope; the detail field of
  adapter_integrity_checks states this explicitly).
- OUT-OF-SCOPE OBSERVATION (era-labelled, NOT fixed, NOT a new finding
  claim): the original user-defined version gate is
  ms_uiNifMinUserDefinedVersion = ms_uiNifMaxUserDefinedVersion =
  0.0.0.0 (NiStream.cpp L47-50) — the original LoadHeader L340-352 would
  REJECT a file whose user-defined version is nonzero; OUR adapter reads
  the user version but does not gate it. No battery/T1/corpus input of this
  run has a nonzero user version. Recorded for a future bounded fix; F2
  did not touch it.
- Legacy (< 5.0.0.1) streams: the adapter has no link-resolution phase, so
  ADAPTER_INTEGRITY can never be PASS for legacy files (honest fail-closed:
  the tool cannot VERIFY what it does not implement) — TOOL never PASS for
  legacy. Raw link IDs are still range-checked for the SOURCE prediction.
- The 2 pre-existing payload battery control failures remain (identical
  pre/post). The F4 presolver trailing-run IndexError remains (not
  touched; counterexample A deliberately places the unsupported block
  MID-file). The pre-first-miss DecodeError behavior remains (F4).
- F3 (compare same-input/comparison validity), F5 (report wording beyond
  the required F2 metadata), F6, F7, O1 (float bit-exact), T3: NOT
  addressed in this run.
- This is a SOURCE_DERIVED_REIMPLEMENTATION; the original compiled GB 1.2
  toolchain never executed in this run. SOURCE_PREDICTED_* verdicts are
  source-derived predictions, never claims of original execution.

## 8. Terminal fields (exact)

```text
F1_RTTI_TABLE_SOURCE_ORDER = PRESERVED
F1_C1_EXTENSION_TABLE_FAILURE_HALT = PRESERVED
F2_ACCEPTANCE_COVERAGE_LINK = FIXED_AND_VERIFIED
SOURCE_PREDICTED_ORIGINAL_VERDICT_SEPARATED = YES
ADAPTER_DECODE_COVERAGE_ENFORCED = YES
ADAPTER_INTEGRITY_ENFORCED = YES
REGISTERED_BUT_NOT_DECODED_FALSE_SUCCESS = REJECTED
INVALID_LINK_FALSE_SUCCESS = REJECTED
VALID_POSITIVE_CONTROL = PASS
CLI_SUCCESS_SEMANTICS = INSPECT_TOOL_PASS_ONLY
NON_INSPECT_CLI_SEMANTICS = PRESERVED
COVERAGE_NOT_MEASURED_DISTINCT_FROM_ZERO = YES
INTEGRITY_FAIL_IMPLIES_TOOL_FAIL = YES
F3_TO_F7 = NOT_ADDRESSED_IN_THIS_RUN
QC_SCOPE = SELF_CHECK_F2 (expected)
QC_VERDICT = SELF_CHECK_QC_PASS
GENERAL_ORACLE_FAIL_CLOSED = ESTABLISHED_FOR_F1_F2_SCOPE_ONLY
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
T3_COMPLETION_EXECUTED = NO
NEW_PCG_TRACE_EXECUTED = NO
WORLD_PLACEMENT_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_RUN_EXECUTED = NO
```
