# SUPERSESSION_AND_STANDING — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Documentary supersession record per contract section 8. The historical source
package `PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009` remains
IMUTABLE — no historical file is edited, rewritten or re-manifested by this
correction; supersession is recorded ONLY in THIS package's new records.
Measured this run: all four mandatory source inputs and the contextual inputs
re-hashed unchanged after the correction work (see INPUT_IDENTITIES.md and
00_POST/POST_COUNTEREXAMPLES.json `source_package_unchanged`).

## 1. CMO-C1 / P2 (the finding this run corrects)

Historical byte-register clobber coverage was insufficient: both historical
x86-32 decoders mapped register-direct `MOV r/m8,r8` (opcode 0x88) high-byte
destinations into the WRONG writes-set parent (CH → EBP, BH → EDI, AH → ESP,
DH → ESI), so the ECX-clobber scan returned a FALSE EMPTY list on the
synthetic `mov ch, bl` (88 DD) counterexample at VA 0x0085B24D — the
component-level false PASS reproduced by this run's PRE in BOTH historical
implementations (executor: `writes=["ebp"]`, scan `[]`; QC: `writes=["ebp"]`,
scan `[]`).

The corrected successor (03_SCRIPTS/corrected_executor_decoder.py) now
detects the high-byte alias counterexample, and the tests pass (measured,
00_POST/POST_COUNTEREXAMPLES.json):

- C2 CH mutant 88 DD: OPERAND=CH, WRITES_PARENT=ECX, dst bits [8,16),
  CLOBBER_SCAN=DETECTED @0x0085B24D, VALUE_PROVENANCE_GATE=FAIL via
  ECX_REACHING_DEF_BROKEN alone (every pin, the rel32 recomputation and the
  accessor check still PASS on the mutant).
- C3 CL control 88 D9: same detection and same single-cause gate FAIL.
- C1 clean: NO false positive (ECX_CLOBBER_AT_MUTATION_SITE=NO; gate PASS;
  CORE_VALUE_SOURCE=[arg1+8]).
- C4: the complete 8×8 alias matrix (64 cases, all eight destinations × all
  eight sources) passes 64/64 on the corrected executor implementation;
  destination coverage 8/8, source coverage 8/8. The corrected QC
  implementation's 64 outcomes are the fresh-QC worker phase
  (corrected_qc_decoder.py — NOT written in this executor phase); the full
  128-outcome two-implementation total completes there.
- C5: unrelated-parent negatives (mov bh,bl → EBX; mov ah,bl → EAX;
  mov dh,cl → EDX; mov bh,bh → EBX) do NOT report ECX as modified and the
  gate stays PASS.
- C6: the historical scientific regression holds — all pins, both rel32
  targets, both RTTI identities, the 64-instruction clean decode ending
  exactly 0x0085B290, field-level equality with the re-executed historical
  decoder on the physical window, and
  CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL.

This correction does NOT establish GENERAL_X86_DECODER_CORRECTNESS or
GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED (the decoder remains a bounded window
decoder, fail-closed on unsupported opcodes — demonstrated controlled
failure in POST AUX-1).

## 2. DOC-1 / P3 (documentary backlog — no historical rewrite)

`C3 + CC CC CC` (terminal ret of the previous thunk plus int3 padding at
0x0085B1AC..0x0085B1AF) is useful CONTEXTUAL boundary evidence but is not
independently sufficient to identify an ARBITRARY function start. For the
examined function (FUN_0085B1B0) the boundary is supported by the actual
direct-call target (the rel32 recomputation of the call @0x00528E8D →
0x0085B1B0, re-verified this run) and by earlier committed disassembly.
Status: BACKLOG (documented; authorizes no broader science; this run re-used
the boundary only as an existing pinned pin inside the approved windows).

## 3. DOC-2 / P3 (documentary backlog — no historical rewrite)

Historical M1–M6 of the source package comprises THREE byte mutations
(M1 opcode, M3 displacement, M5 accessor), TWO expectation/address controls
(M2 VA shift, M4 width) and ONE receiver comparison (M6 SF-object
distinction). Do NOT describe all six as separate semantic mutation tests.
Status: BACKLOG (documented wording discipline; the source records remain
untouched; this run's own mutation language follows the same discipline —
the PRE/POST counterexamples here are component-level decoder controls, not
semantic mutation tests, and establish CONTROL outcomes only).

## 4. Standing preserved VERBATIM (carried, not re-derived, not reinterpreted)

```
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE =
  MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN =
  NOT_QUALIFIED_BY_ORIGINAL_SCOPE

ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL
WORLD_XYZ_RECOVERED = NO
```

Source of the carried standing: J3 SUPERSESSION.md (docs/audits/
PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/
SUPERSESSION.md, 8339 B / SHA256 DD11137A0E79491511A7688B7C1DE9252DB7BA443FA
31892C345CA76CE136845, identity re-verified in this run's preflight) and the
source FINAL_REPORT section 8.

No reinterpretation or restoration of historical J3 standing is made by this
run: `SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC` remains SUPERSEDED
as an active, run-qualified conclusion; no prior human authorization is
claimed; this machinery-correction run used ZERO new edges, ZERO new bodies
and adds nothing to the historical edge accounting.

## 5. Scope confirmation (contract section 9)

```
NEW_PCG_FUNCTION_BODIES = 0
NEW_PCG_SCIENCE_EDGES = 0
NEW_FIELD_SEMANTIC_INTERPRETATIONS = 0
NEW_RUNTIME_WORK = 0
NEW_NETWORK_RE = 0
NEW_PLACEMENT_RE = 0
NEW_MODEL_RE = 0
NEW_GAMEBRYO_OPENMW_RESEARCH = 0
```

Measured process facts: the EXE was read only within the already-approved
windows (W1 / W2 accessor / W3 caller / the two RTTI chains) and re-hashed
unchanged after all work (E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F
753765D5280F31); the tracked tree changed nowhere except this OUTPUT_ROOT;
the upstream arg1 chain was not followed; the sibling stores +0x48/+0x4C
were byte-pinned only (no analysis); no world coordinates, position units,
building identities, coordinate frames or placement messages were
investigated; no Gamebryo/OpenMW research was performed.

## 6. Phase boundaries of THIS record (delegation)

This executor phase wrote only: PREREGISTRATION.md, INPUT_IDENTITIES.md,
ROOT_CAUSE.md, 00_PRE/*, 03_SCRIPTS/run_pre_counterexamples.py,
03_SCRIPTS/corrected_executor_decoder.py, 03_SCRIPTS/run_alias_controls.py,
00_POST/*, CONTROL_MATRIX.csv, SUPERSESSION_AND_STANDING.md (this file) and
REGRESSION_RESULTS.json. The corrected QC implementation
(03_SCRIPTS/corrected_qc_decoder.py), QC_RESULTS.json and QC_REPORT.md are
the fresh-QC worker's phase; PE_MASTER_REVIEW.md, FINAL_REPORT.md,
EVIDENCE_INDEX.md, HANDOFF.md, MANIFEST_SHA256.csv and any
AUDIT_ENTRYPOINT.md annotation are the parent phases. No stage/commit/push
was performed in this phase.
