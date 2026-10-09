# HANDOFF — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

## Contract §8 handoff block (verbatim, as executed)

```text
RUN_ID = PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009
EXPECTED_BASE_SHA = 2ac7cfa1dcb2e53e9c86985c18377de811d5b485
RESULTING_SHA = (see PERSISTENCE below — the resulting commit SHA is
                 returned in the executor's final message and must never be
                 embedded in its own commit content)
REMOTE_SHA = (measured in the persistence section below)
PERSISTENCE_STATUS = (see below)
PRE_REPRODUCTION = REPRODUCED (CLEAN PASS both predecessor gates; AC1/AC2
                    REJECTED both; BR1-BR4 PASS both = 8 false-PASS
                    outcomes, matching the Desktop BR-C1/P2 finding)
BR_C1_IMPLEMENTATION = CORRECTED_IN_TESTED_SCOPE
BR_C1_DESKTOP_CLOSURE = PENDING_POST_AUDIT
CLEAN_ARTIFACT_GATES = PASS in both corrected gates (50/50 checks each;
                       the same gates used for every control)
AC1_AC2 = 4/4 (rejected in both gates, both PRE and POST)
BR1_BR4 = 8/8 (POST; 0/8 in PRE — the defect)
FIXED_ARTIFACT_MATRIX = 14/14
FIELD_CHECK_COVERAGE = 34 rows (32 field representations + 2 derived
                        relation/consistency rows; BR-C1.1: 4, BR-C1.2:
                        10, BR-C1.3: 13, BR-C1.4: 7); every representation
                        has an individual single-field control rejected in
                        BOTH gates (32 cases -> 64/64), plus 4 missing-field
                        (8/8), 5 wrong-native-type (10/10) and 2
                        malformed-expression (4/4) controls; total
                        additional 43 cases / 86 outcomes -> 86/86
REQUIRED_BYTE_MATRIX = 24/24 (production 12/12 + QC 12/12 CONTROL_PASS;
                       M5/M7 arg1 unchanged while the changed other
                       channels are reported, both sides)
INTERNAL_QC_ORIGIN = SELF_REVIEW (executor's own mechanical re-inspection,
                     43/43 checks PASS; fresh-context internal QC is a
                     separate LATER agent)
INTERNAL_QC_VERDICT = NOT_PERFORMED (fresh-context internal QC not performed
                      in this run; no internal QC_PASS issued)
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
SCIENTIFIC_CLAIMS = PRESERVED (no semantic promotion; no incidental
                    contradiction; CROSS_CALL_POINTER_VALUE_IDENTITY =
                    CONFIRMED_STATIC_CONDITIONAL and all standing science
                    unchanged)
SOURCE_PACKAGE_UNCHANGED = YES (predecessor package 35/35 files identical
                          before/after; EXE re-hashed unchanged every
                          phase)
MANIFEST_ROWS = (see persistence section)
PHYSICAL_PACKAGE_FILE_COUNT = (see persistence section)
ENTRYPOINT_ROWS = 1
MANIFEST_BIJECTION = (see persistence section)
CHANGED_PATH_CENSUS = (see persistence section)
OPEN_FINDINGS = F-QC-1 (driver CSV-writer variable-shadowing defect,
                caught by self-check, fixed, ALL phases re-executed with
                the final driver bytes, stray files removed — disclosed in
                QC_REPORT.md); F-QC-2 (FIELD_CHECK_COVERAGE.csv row F-C2-9
                displays the PROV-A-SLOT display value "[E+0x4]" in the
                DERIVED_EXPECTED_VALUE column; the check enforces both the
                expression and the delta); F-QC-3 (predecessor EXEC_CLAIMS
                adjudication design remains the predecessor's; not used by
                the corrected QC gate)
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Key measured results

- **PRE (ACTUAL predecessor gates, unmodified, module hashes recorded)**:
  CLEAN PASS (21/21 both); AC1 REJECTED (production: PROV-B-ARG1-KIND,
  PROV-B-LEA-EXPR; QC: PROV-B-KIND, PROV-B-LEA); AC2 REJECTED (PROV-A-SLOT
  both); BR1/BR2/BR3/BR4 PASS in BOTH gates — 8 false-PASS outcomes. The
  Desktop divergence: NONE (results identical to the Desktop
  counter-reproduction).
- **POST (corrected gates)**: fixed matrix 14/14; BR1 failing =
  PROV-BR11-CALL-TARGET + PROV-BR11-TARGET-RECOMPUTED +
  PROV-BR11-BRIDGE-VALID (QC names prefixed QC-); BR2 failing =
  PROV-BR12-ARG1-SLOT-DELTA + PROV-BR12-ARG-SLOT-DELTAS-ARG1 +
  PROV-BR12-B-ARG1-SLOT + PROV-BR12-SLOT-RELATION; BR3 failing =
  PROV-BR13-B-ARG1-VALUE-KIND + PROV-BR13-B-ARG1-VALUE-EXPR +
  PROV-BR13-CROSSCALL-VALUE-EXPR + PROV-BR13-PARALLEL-CONSISTENCY; BR4
  failing = PROV-BR14-NULL-JE-TAKEN + PROV-BR14-NULL-CALL-REACHED; AC1/AC2
  failing = value provenance / entry slot predicates; every rejection with
  zero hash-side failures and zero exceptions; clean final validation
  PASS 50/50 per gate.
- **Regression**: production 12/12 + QC 12/12 = 24/24 CONTROL_PASS; M5
  (arg1 ADDRESS(T+0x8) slot -0x10 unchanged; arg3/arg4 swapped) and M7
  (arg1 unchanged; receiver changed) verified on both sides; unchanged
  helper preservation proven (EXPECTED/MUTATIONS/CASE_ORDER/EXP/MUT
  identical to the predecessor).

## Preserved science (verbatim; unchanged by this correction)

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

J3 supersessions kept; no ACLD/CMO identity transfer; no new RE; EXE
inspection limited to the two existing windows (replay/verify); 0x004C47C8
unopened.

## Supersession summary

Supersedes ONLY the predecessor's overbroad artifact-gate adequacy claim
(its "21/21 fact checks PASS" presented as adequate persisted-fact
validation for the four BR-C1 relations). Preserves the predecessor's
authentic required controls (24 byte-matrix outcomes, AC1/AC2, clean
baseline), its clean science and its failed negative-test history. See
SUPERSESSION_AND_STANDING.md.

## Outputs (exact paths)

Local package root:
`D:\Eudoria_Reconstruction\99_Audits\PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009\`

- Package (published copy):
  `docs/audits/PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009/`
  in the canonical repo (D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean)
- PRE: PACKAGE\PRE_ARTIFACT_RESULTS.json
- POST: PACKAGE\POST_ARTIFACT_RESULTS.json
- Coverage: PACKAGE\FIELD_CHECK_COVERAGE.csv
- Regression: PACKAGE\REGRESSION_RESULTS.json
- QC: PACKAGE\QC_RESULTS.json + PACKAGE\QC_REPORT.md
- Diff: PACKAGE\CODE_DIFF.patch
- Supersession: PACKAGE\SUPERSESSION_AND_STANDING.md
- Final report: PACKAGE\FINAL_REPORT.md
- Manifest: PACKAGE\MANIFEST_SHA256.csv (generated LAST)
- SCRATCH (local-only, never in the repo): OUTPUT_ROOT\SCRATCH\

## Persistence (terminal order, executed as contracted)

CORRECTION/REGRESSION -> SELF_REVIEW QC -> FINAL_REPORT/REVIEW/
SUPERSESSION/EVIDENCE_INDEX/HANDOFF -> one truthful AUDIT_ENTRYPOINT.md row
-> FINAL MANIFEST LAST (published package physical files minus the manifest
itself + the changed AUDIT_ENTRYPOINT.md; full bijection + independent
re-hash) -> recheck BASE/remote/source/allowlist -> stage EXPLICIT
allowlisted paths only -> normal commit -> fast-forward push -> verify
LOCAL_HEAD == origin/master == actual remote -> HARD STOP.

The measured RESULTING_SHA / REMOTE_SHA / PERSISTENCE_STATUS / manifest
counts / changed-path census are reported in the executor's final message
(they cannot be embedded here: any write after manifest verification would
invalidate the manifest, and the commit SHA must not be embedded in its own
commit content).

## What the next agents do

1. Fresh-context internal QC (separate agent): re-inspect the changed
   gates, field coverage, PRE/POST and control causality of THIS package.
2. Independent Desktop post-audit of the resulting commit SHA: verify the
   14-outcome fixed matrix, the single-field causality (especially
   target/target_recomputed individual coverage), the 24/24 regression and
   publication safety. BR_C1_DESKTOP_CLOSURE remains PENDING_POST_AUDIT
   until that audit closes it.

No automatic follow-up RE or correction cycle. HARD_STOP = YES.
