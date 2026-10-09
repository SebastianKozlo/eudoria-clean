# PREREGISTRATION — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

```text
RUN_ID            = PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009
RUN_CLASS         = MACHINERY_AND_CONTROL_CORRECTION
EXPECTED_BASE_SHA = 2ac7cfa1dcb2e53e9c86985c18377de811d5b485
AUTHORIZATION     = separate human message (2026-10-09) naming this exact
                    contract (SHA256 B30E807BFA24BC37A8FFC015D37B42EC96F72F47D
                    8B6956AFA9512D09CDC1CE3, 18566 B), authorizing this one
                    correction-only run plus its allowlisted commit/fast-forward
                    push. NEXT_EXPERIMENT_AUTHORIZED=NO.
SESSION           = OpenCode agent pe-reconstruction, model nask-glm/glm-5-3,
                    python3 -B under WSL PE-AI (Debian, kernel
                    6.18.33.2-microsoft-standard-WSL2) for all gate/matrix
                    execution.
```

This preregistration is written BEFORE any PRE reproduction, any POST gate
correction, and any control execution of this correction run. It is never
rewritten to match POST results.

## P1. Correction target (the demonstrated defect, from the Desktop post-audit)

The predecessor package PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009 at
BASE_SHA 2ac7cfa1 persisted two ordinary artifact-fact gates
(03_SCRIPTS/run_frame_bridge.py gate_artifacts(), 03_SCRIPTS/
qc_frame_bridge.py gate()). The independent Desktop post-audit (first pass +
second pass, both audit attachments SHA256 34E049BEF9303EBAFFDBE3397A8AC314
40271F565C03059710CBF230273E3B38, byte-identical) demonstrated that the gates
compare the persisted facts of only a subset of the four BR-C1 relations:

- BR1 (exported CALL target -> 0x00528E51 with bridge_valid=false): both gates
  PASS — the production 6f / QC 6e call-target checks compare their own
  rel32/expected tables, never reading phase_b.nonnull_path.call.target /
  target_recomputed / bridge_valid from the JSON under test.
- BR2 (arg1 slot -16 -> -12 in all three slot representations): both gates
  PASS — slot_delta_T0, arg_slot_deltas.arg1 and bridge.b_arg1_slot are never
  compared to the ESP-walk-derived slot.
- BR3 (bridge summary claims STACK_READ / MEM(T+0x8) while the first arg1
  representation stays ADDRESS(T+0x8)): both gates PASS — the kind/expr
  checks fall back (or-trick) to the first representation; the parallel
  bridge summary fields are never individually compared.
- BR4 (null path claims call_reached=true / je_taken=false): both gates PASS —
  null_path facts are never read.

AC1 (arg1 value provenance) and AC2 (entry slot) ARE rejected by both gates.
Baseline clean artifacts PASS in both gates. 8 false-PASS outcomes (BR1-BR4 x
2 gates) is the demonstrated defect (BR_C1 = CONFIRMED_OPEN_P2).

## P2. Hypothesis and expected PRE outcome (recorded before running PRE)

HYPOTHESIS: re-running the ACTUAL predecessor gate_artifacts()/gate() (imported
unmodified from the source package at BASE_SHA, via their normal provenance
override on deep-copied BRIDGE_PROVENANCE.json) reproduces exactly:
- CLEAN: PASS in both gates (21/21 baseline checks pass);
- AC1: REJECTED in both gates (arg1 value provenance);
- AC2: REJECTED in both gates (entry slot);
- BR1, BR2, BR3, BR4: PASS in both gates (8 false-PASS) — the defect.

If PRE does not reproduce, the result is recorded as NOT_REPRODUCED /
REQUIRE_CORRECTIONS without any PRE rewrite and the run finalizes under the
publication-safety rules.

## P3. Planned POST correction (narrow, before writing it)

Correct COPIES of both scripts under this package 03_SCRIPTS/ (byte decoders,
symbolic derivations, CASE_ORDER, original mutation definitions preserved):

1. BR-C1.1 CALL identity: add checks comparing the persisted
   phase_b.nonnull_path.call.target, target_recomputed and bridge_valid (each
   individually, native JSON types enforced: target strings; bridge_valid JSON
   boolean true) to the rel32-derived target of the instruction at the pinned
   callsite 0x004C47C1 and to the derived bridge predicate (actual target ==
   window-A entry 0x00528E50). JSON boolean false is not a valid positive
   bridge predicate; no string->boolean coercion.
2. BR-C1.2 argument-slot identity: compare arg1.slot_delta_T0,
   arg_slot_deltas.arg1, bridge.b_arg1_slot, bridge.a_source_slot_from_T (kept)
   and bridge.E_delta_from_T to the ESP-walk-derived slot (-16 / "[T-0x10]") and
   E delta (-20); cross-check the exported esp_before_call_delta_T0 (-16) and
   callee_entry_esp_delta_T0 (-20); derive the relation [E+4] == [T-0x10]
   (E_delta + 4 == slot_delta) rather than comparing duplicate claims to each
   other only. Integer fields reject JSON booleans.
3. BR-C1.3 pointer value and duplicate bridge summary: compare
   arg1.{value_kind,value_expr,value_delta}, arg_slots.arg1.{kind,expr,delta}
   (explicitly normalizing the finite documented "T0+0x8 (computed)" form),
   bridge.{b_arg1_value_kind,b_arg1_value_expr,cross_call_value_expr} each
   individually (OR-fallbacks removed) against the LEA/opcode-derived facts
   (ADDRESS, ADDRESS(T+0x8), 8) and against each other. A's STACK_READ
   (phase_a.delivery / bridge.a_delivered_value_kind) is validated as the
   argument-slot load of the joined slot [E+4], never reclassified as a B-side
   pointee read.
4. BR-C1.4 null path: compare null_path.{je_taken,call_reached} (native JSON
   booleans) and the exported branch/exit identity facts (exit_va ==
   decoded JE target 0x004C47C8; exit_inside_window false, derived from the
   window interval; unconditional_exit false, derived from opcode 0x74 vs 0xEB)
   to the B-window branch derivation. No claim about 0x004C47C8's later
   behavior.
5. Named diagnostics for missing fields (MISSING_FIELD:<path>), wrong native
   JSON types (WRONG_TYPE), malformed supported expressions (MALFORMED_EXPR)
   and mismatches (VALUE_MISMATCH); no uncaught exception from these four
   relations' fields; no silent auto-repair; no eval; no general schema engine.
6. QC gate: same coverage, derived from the QC's OWN walk/parse (no import of
   or delegation to the production verdict).

## P4. Planned controls (fixed matrix, before running it)

7 fixed artifact cases x 2 gates = 14 outcomes, on deep-copied
BRIDGE_PROVENANCE.json through each gate's normal provenance override,
baseline first, all through the same corrected gates used for clean final
validation. Exact mutations per contract §4: CLEAN (none, PASS), AC1
(arg1.value_kind=STACK_READ; value_expr=MEM(T+0x8), REJECTED for value
provenance), AC2 (source_slot [E+4]->[E+0x8], slot_delta_from_E=8, REJECTED
for entry slot), BR1 (call target + target_recomputed -> 0x00528E51,
bridge_valid=false, REJECTED for persisted CALL identity), BR2 (slot -16 ->
-12 in the three slot representations, REJECTED for slot identity), BR3
(bridge summary -> STACK_READ / MEM(T+0x8) in b_arg1_value_kind +
b_arg1_value_expr + cross_call_value_expr, REJECTED for contradictory bridge
value), BR4 (null_path call_reached=true, je_taken=false, REJECTED for
null-path facts). A rejection caused by a hash/manifest-side failure, missing
fixture, crash or unrelated predicate failure does NOT count as the required
rejection; per rejected case the failing predicate names must include the
expected BR-C1 fact predicate(s).

Additional single-field controls: each FIELD_CHECK_COVERAGE representation
mutated individually at least once (all other fields/duplicates left clean),
plus representative missing-field and wrong-native-type cases for these four
relations. Counts reported dynamically, separately from the fixed 14.

## P5. Planned regression

Re-execute the unchanged existing 12-case production byte matrix (run_case,
EXPECTED, MUTATIONS, derive_a/derive_b, build_fixture — preserved in the
corrected copies) and the unchanged existing 12-case QC byte matrix
(run_matrix, EXP, MUT, its own derive_a/derive_b) through the existing
bounded helpers, all writes redirected into this run's SCRATCH. Required:
24/24 discriminating outcomes CONTROL_PASS; M5/M7 arg1 (kind/expr/slot)
unchanged while the changed other channels (arg3/arg4 order; receiver) are
reported.

## P6. Preserved science (verbatim; no semantic promotion)

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

J3 supersessions kept; no ACLD/CMO identity transfer; no new RE/pointee/
region research; EXE inspection limited to the two existing windows
A [0x00528E50,0x00528E92) and B [0x004C4792,0x004C47C6) (replay/verify of
already-derived facts only; whole-file hashing/PE headers allowed).

## P7. Supersession plan

Supersede ONLY the predecessor's overbroad artifact-gate adequacy claim
(its "21/21 fact checks PASS" baseline statement and ARTIFACT_CONSISTENCY_PASS
adequacy for the four BR-C1 relations, as qualified by the Desktop
post-audit finding BR_C1 = CONFIRMED_OPEN_P2). Preserve the predecessor's
authentic required controls, clean science and failed negative-test history.
No historical file or commit rewrite; corrections/PRE/POST are new records.

## P8. Publication-safety plan (terminal order)

CORRECTION/REGRESSION -> internal QC (executor SELF_REVIEW only in this run;
a fresh-context QC is a separate later agent) -> FINAL_REPORT / REVIEW /
SUPERSESSION / EVIDENCE_INDEX / HANDOFF -> one truthful AUDIT_ENTRYPOINT.md
row -> FINAL MANIFEST LAST (package physical files minus manifest + the
changed AUDIT_ENTRYPOINT.md; repo-relative paths/sizes/SHA256; full bijection
+ independent re-hash) -> recheck BASE/remote/source/allowlist -> stage
EXPLICIT allowlisted paths only -> normal commit -> fast-forward push ->
verify LOCAL_HEAD == origin/master == remote. If the remote advanced: STOP.
If push fails after commit: LOCAL_COMMIT_CREATED=YES, PUSH_STATUS reported
accurately, no replacement commit. No resulting-commit-SHA embedded in its own
commit content.

Allowlist: OUTPUT_ROOT (local) +
docs/audits/PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009/
+ one AUDIT_ENTRYPOINT.md row.

## P9. Honest scope statements

- The author of this correction is the executor; internal QC inside this run
  is a SELF_REVIEW, not a fresh-context QC. FRESH_CONTEXT_INTERNAL_QC is
  performed by a separate later agent and recorded honestly if absent.
- INDEPENDENT_DESKTOP_POST_AUDIT of the resulting commit: NOT_PERFORMED in
  this run (BR_C1_DESKTOP_CLOSURE = PENDING_POST_AUDIT).
- The two gates share GNU objdump 2.44 as the single disassembler (honest;
  the same objdump is NOT two independent disassemblers).
- Contracted fix scope: at most one focused repair/recheck round for defects
  within these four relations; other findings are recorded residuals.
