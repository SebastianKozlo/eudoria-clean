# SUPERSESSION_AND_STANDING — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

## 1. What this correction SUPERSEDES (narrowly)

Exactly ONE claim of the predecessor package
PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009 (commit 2ac7cfa1):

- **SUPERSEDED**: the predecessor's overbroad artifact-gate adequacy claim —
  the FINAL_REPORT §9 statement that the persisted artifacts were re-read
  through the ordinary final gate with "21/21 fact checks PASS" and the
  resulting "ARTIFACT_CONSISTENCY_PASS" presented as adequate validation of
  the persisted-fact consistency of BRIDGE_PROVENANCE.json. The independent
  Desktop post-audit (two passes, BR_C1 = CONFIRMED_OPEN_P2) demonstrated
  that the 21-check gates do NOT compare the persisted facts of the four
  BR-C1 relations (8 false-PASS outcomes for BR1–BR4 x 2 gates), and this
  run REPRODUCED that defect mechanically through the ACTUAL predecessor
  gates (PRE_ARTIFACT_RESULTS.json: BR1–BR4 PASS in both gates; 8
  false-PASS outcomes). The 21-check coverage is adequate for window
  identity, ledger rows, ESP pivots, the A source slot, the arg1
  kind/expr of the FIRST representation and the entry-slot identity — it
  is NOT adequate for the exported CALL identity, the argument-slot
  representations, the parallel bridge summary, or the null-path facts.

## 2. What is NOT superseded (preserved verbatim)

- All predecessor SCIENCE (unchanged, no semantic promotion):

```text
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
CONDITIONS = AS1-AS5 plus EAX!=0, unchanged
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
```

- The predecessor's authentic required controls: the 12-case production and
  12-case QC byte matrices (re-executed unchanged this run: 24/24
  CONTROL_PASS, M5/M7 arg1-retention preserved), the AC1/AC2 artifact
  controls (still rejected by both gates, now with more failing predicates),
  the clean baseline (still PASS, now 50 checks per gate).
- The predecessor's clean science derivation chain (windows, ledgers,
  BRIDGE_PROVENANCE.json content — every value re-validated by the
  corrected gates against the physical evidence; zero contradictions
  found).
- The predecessor's failed negative-test history and crash/continuation
  record (PREREGISTRATION P10, two-session origin) — untouched.
- Standing records preserved verbatim (from the predecessor's
  SUPERSESSION_AND_STANDING): `S = ESP at 0x00528E76, not function-entry
  ESP`, `0x00528E84: EDI := DWORD [S+0x3C]`, `0x00528E8A: PUSH EDI`,
  `0x00528E8D: CALL 0x0085B1B0`, `ARG1_DIRECT_SOURCE =
  CONFIRMED_STATIC_CONDITIONAL`, `UPSTREAM_PROVENANCE =
  UNRESOLVED_UPSTREAM (prior bounded result)`, `CMO_C1 =
  CLOSED_FOR_AUDITED_STATE`, `CORE_RECEIVER_VALUE_CHAIN =
  PRESERVED_CONFIRMED_STATIC_CONDITIONAL`.
- J3 supersession records — kept (no restoration); no ACLD/CMO identity
  transfer; no reinterpretation of the [arg1+8] -> MovableObject+0x44 store.

## 3. What this run ADDS (machinery only)

- Corrected copies of both ordinary artifact gates (03_SCRIPTS/
  run_frame_bridge.py gate_artifacts(), 03_SCRIPTS/qc_frame_bridge.py
  gate()) that compare the persisted facts of the four BR-C1 relations —
  BR-C1.1 CALL identity, BR-C1.2 argument-slot identity, BR-C1.3 pointer
  value + duplicate bridge summary, BR-C1.4 local null path — to the
  evidence-derived facts (rel32 recompute, ESP walks, opcode bytes,
  decoded branch target/window interval), each representation individually
  (OR-fallbacks removed), with native JSON type enforcement and named
  diagnostics (MISSING_FIELD / WRONG_TYPE / MALFORMED_EXPR /
  VALUE_MISMATCH). See CODE_DIFF.patch and FIELD_CHECK_COVERAGE.csv (34
  rows).
- The fixed 7-case x 2-gate matrix (CLEAN/AC1/AC2/BR1-BR4): 14/14 correct
  outcomes; BR1-BR4 now REJECTED (8/8) with the expected named predicates;
  AC1/AC2 still rejected (4/4).
- Additional controls: 32 single-field mutations (every coverage
  representation mutated individually with clean duplicates — proving each
  comparison live; a bridge_valid-only rejection does NOT prove
  target/target_recomputed coverage, so those carry their own individual
  controls), 4 missing-field, 5 wrong-type (including JSON
  boolean-as-integer and int-as-boolean), 2 malformed-expression cases:
  86/86 correct rejections through the same gates.
- Regression: the unchanged byte matrices re-executed 24/24 with M5/M7
  arg1-retention verified.

## 4. Scope fences of this correction

- No new RE: EXE inspection limited to the two EXISTING windows
  ([0x00528E50,0x00528E92), [0x004C4792,0x004C47C6)) — replay/verify of
  already-derived facts; whole-file hashing; no new region/function/
  callee/xref/pointee exploration; 0x004C47C8 remains unopened.
- No Gamebryo/OpenMW research, VFS/BNT/NIF, runtime/client/network
  experiments, upstream pointee tracing, milestone/qualification/governance
  change.
- No general schema engine, no eval, no universal JSON/decoder hardening —
  the finite FIELD_CHECK_COVERAGE of the four relations only.
- The seven historical intermediates were NOT recovered by this
  correction; chronology claims of the predecessor run are unchanged.

## 5. Standing after this correction

```text
BR_C1_IMPLEMENTATION = CORRECTED_IN_TESTED_SCOPE
BR_C1_DESKTOP_CLOSURE = PENDING_POST_AUDIT
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL (unchanged)
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL (unchanged)
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM (unchanged)
FIELD_SEMANTICS = UNVERIFIED (unchanged)
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED (unchanged)
HISTORICAL_PLACEMENT = NOT_ESTABLISHED (unchanged)
WORLD_XYZ_RECOVERED = NO
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED (later audit of the resulting commit)
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## 6. Incidental contradiction check

No contradiction with preserved science emerged incidentally during this
correction: every clean persisted value re-validated by the corrected gates
matched the evidence-derived expectation (50/50 checks per gate), and all
24 byte-matrix outcomes were unchanged. Had a contradiction appeared, it
would have been recorded with REQUIRE_CORRECTIONS without silent
reinterpretation.

## 7. Phase boundaries of this record

This correction run wrote only under OUTPUT_ROOT: PACKAGE/ (the publishable
package) and SCRATCH/ (local-only fixtures and mutated provenance copies,
never published). The predecessor package, the EXE and all historical files
are byte-unchanged (verified 35/35 before/after). Canonical publication of
this package + one AUDIT_ENTRYPOINT.md row happens under the human-authorized
allowlist with a normal commit and fast-forward push, performed by this same
executor session as the contracted terminal step.
