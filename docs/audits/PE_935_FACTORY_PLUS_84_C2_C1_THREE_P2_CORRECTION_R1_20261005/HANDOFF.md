# HANDOFF — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

Phase-1 (machinery-repair) handoff to the PE-MASTER internal
pre-publication review. Phase 2 (a separate dispatch) will persist the
review verdict, add the AUDIT_ENTRYPOINT.md row, generate the manifest
LAST, and only then commit/push within the authorized allowlist.

## THE CORRECTION IN FIVE LINES

1. **P2-1**: the boundary cache's coverage scan is now SORTED and
   order-independent (it sorts its input; the anchor-conflict policy is
   unchanged). NEW-F proves UNRESOLVED/ANCHOR_CONFLICT with no promotion
   across 56 synthetic permutations + 50 randomized real-stream orders;
   the two real driver pins re-derive REFUTED_MID_INSTRUCTION with
   refuted_by=0x004B0980 (the only pin changes the correction produced).
2. **P2-2**: `66 0F 8x` near Jcc decodes as rel16 (BRANCH A; oracle GNU
   objdump Binutils 2.44: `66 0f 84 00 00` = je rel16, 5 B). NEW-G: the
   E8 at +7 is interior data - REFUTED, FAIL_MID_INSTRUCTION,
   INTERNAL_E8_PROMOTED=NO (the C2 decoder fabricated a CALL edge there).
3. **P2-3**: gate Q2 re-derives the JSON pins' effective_address object
   from the pinned EXE (46/46 mem pins; base/index/scale/displacement/
   segment/width-state/provenance). M5 (base_register ESI->EAX) and M6
   (fake provenance) flip the SAME gate from clean PASS to mutated FAIL;
   the historical Q2 coverage wordings are superseded (ledger S-P2-01..03).
4. **H1/H2**: the 16-bit addressing rm=7 entry is [BX] (full table
   oracle-checked; lengths unchanged), and grouped opcodes 0F BA / 0F
   71-73 reject reserved/invalid sub-opcodes fail-closed (validity =
   opcode + reg + mod + mandatory prefix; the legal PSRLDQ/PSLLDQ register
   forms decode).
5. **Regression vs C2**: exactly 16 boundary-field changes (the two
   declassified driver pins x 4 fields x JSON+CSV), 7 new boundary-test
   cases; census (2612 rows), quantities, C3 and AF3 REGENERATED and
   BYTE-IDENTICAL to C2 (measured, not copied). All 13 data gates + Q14
   PASS; 7/7 mutations causal; 64 unit vectors; 13-case boundary matrix;
   71 oracle fixtures.

## Provenance

RUN_ID = PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005
RUN_CLASS = LOAD_BEARING; RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
DISPATCH_AUTHORITY = HUMAN + PE-MASTER (human authorization 2026-10-05,
verbatim: "Autoryzuję wykonanie
PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005 zgodnie z
pełną specyfikacją dispatchu, z przepływem dwufazowym: correction +
targeted QC → wewnętrzny PE-MASTER review przed finalnym manifestem →
manifest LAST → commit/push w granicach zdefiniowanej allowlisty →
weryfikacja dokładnego remote SHA → HARD STOP.")
NO_NESTED_TASKS = YES (absolute; task:deny in the worker config).
CLIENT_EXECUTION = FORBIDDEN (none occurred; static byte reads only).
CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO.

## Baseline identity (phase-1 semantics)

BASE_SHA = c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd
HEAD_SHA_AT_PACKAGE_FREEZE = c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd
COMMIT_SHA = NOT_AVAILABLE_AT_PACKAGE_FREEZE

(The BASE triple - LOCAL_HEAD == ORIGIN/master == ACTUAL_REMOTE_MASTER ==
c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd - was measured at this run's
preflight after `git fetch origin`; in phase 1 the HEAD still equals BASE
by design. The resulting phase-2 commit's own SHA is reported only in the
final executor response AFTER push and remote verification; no committed
artifact embeds its own commit SHA; this HANDOFF is NOT modified after
manifest generation.)

## Package contents (phase 1)

- 7 root documents: FINAL_REPORT.md, QC_REPORT.md, SUPERSESSION_LEDGER.md,
  INPUT_IDENTITIES.md, EVIDENCE_INDEX.md, HANDOFF.md,
  PE_MASTER_REVIEW.md (placeholder).
- 3 root CSV artifacts: CORRECTED_PIN_LEDGER.csv (133 rows),
  CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv (2612 rows),
  AF3_PROVENANCE_LEDGER.csv (5 rows).
- 3 root matrices: AF1_MUTATION_MATRIX.csv (7 rows),
  AF2_BOUNDARY_TEST_MATRIX.csv (13 cases),
  CHANGED_BOUNDARY_FIELDS_VS_C2.csv (23 rows).
- 01_RAW/: C1_PIN_EVIDENCE.json, C2_CENSUS.json, C3_OBJECT_SCOPE.json,
  CQC_DECODER_UNIT_TESTS.json, CQC_BOUNDARY_COUNTEREXAMPLES.json,
  CQC_MUTATION_RESULTS.json, CQC_FINAL.json (data+docs),
  ORACLE_INDEPENDENT_RECORDS.json (71 fixtures),
  C2_COMMIT_MESSAGE_VERBATIM.txt, CHANGED_FIELDS_VS_C2.json.
- 03_SCRIPTS/: pebnd.py, x86dec.py, c1_pin_ledger.py, c2_census.py,
  c3_object_scope.py, cqc_battery.py, capture_independent_evidence.py,
  diff_vs_c2.py, make_manifest.py (defaults updated to THIS run; the
  C2-era inherited defaults were never allowed to write into historical
  packages).

## Phase-1 explicit NON-actions (verified)

- No manifest file generated (PHASE_1_MANIFEST_GENERATED = NO).
- AUDIT_ENTRYPOINT.md untouched (PHASE_1_ENTRYPOINT_MODIFIED = NO; no row
  added in phase 1).
- No git add/commit/push (PHASE_1_COMMIT_OR_PUSH_PERFORMED = NO).
- Nothing written outside OUTPUT_ROOT; the six foreign untracked paths
  untouched and unstaged; historical packages C1/C2 READ ONLY (verified by
  the byte-identity measurements in 01_RAW/CHANGED_FIELDS_VS_C2.json).
- Temporary mutation trees deleted; no untracked writer left running.

## Phase-2 checklist (for the separate dispatch; NOT executed here)

1. Persist the PE-MASTER internal pre-publication review verdict into
   PE_MASTER_REVIEW.md (replacing the placeholder).
2. Add exactly one NEW AUDIT_ENTRYPOINT.md row (1 insertion, 0 deletions,
   LF endings preserved).
3. Re-verify the BASE triple immediately before commit.
4. Generate the manifest LAST via 03_SCRIPTS/make_manifest.py (scope =
   every file under this package + the updated AUDIT_ENTRYPOINT.md;
   self-excluded; bijection verified; this HANDOFF's MANIFEST_ROW_COUNT
   declared at that time to match the measured count).
5. Path-limited staging of exactly the authorized paths; commit; push; no
   force push.
6. Verify the exact remote SHA and report it.

MANIFEST_ROW_COUNT = 33 (measured in phase 2 by the same rule
make_manifest.py uses: every file under this package except the manifest
itself + the updated AUDIT_ENTRYPOINT.md = 32 package files + 1 entrypoint
file = 33 rows; the manifest is generated LAST and its bijection +
HANDOFF-consistency check verify this declared count against the measured
count).

## Phase-2 execution record

Phase 2 (this dispatch) executed, in order:

1. PE-MASTER internal pre-publication review verdict persisted into
   PE_MASTER_REVIEW.md, replacing the phase-1 placeholder:
   ACCEPTED_WITH_TWO_P3_NOTES (advisory/pre-qualification; both P3 notes
   recorded there; CANONICAL_GATE_EFFECT = NONE).
2. Exactly one NEW AUDIT_ENTRYPOINT.md row added at the top of the LATEST
   RUNS table (1 insertion, 0 deletions; LF endings preserved).
3. Manifest generated LAST via 03_SCRIPTS/make_manifest.py + bijection
   verified (missing=0, extra=0, duplicates=0, size mismatches=0, SHA256
   mismatches=0) with this HANDOFF's declared MANIFEST_ROW_COUNT verified
   against the measured count.
4. BASE triple re-verified immediately before commit (LOCAL_HEAD ==
   ORIGIN/master == ACTUAL_REMOTE_MASTER ==
   c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd; any divergence would mean
   BLOCKED_BASE_MOVED with an honest stop, no rebase, no merge, no force
   push).
5. Path-limited staging of exactly the authorized paths (the full
   OUTPUT_ROOT tree including the new manifest + AUDIT_ENTRYPOINT.md;
   never `git add .`; the 6 foreign untracked paths untouched and
   unstaged); commit once; push normally to master (no force push).
6. After push the exact remote SHA verified independently (LOCAL_HEAD ==
   ORIGIN_MASTER == ACTUAL_REMOTE_MASTER == the resulting commit SHA); the
   resulting commit's own SHA is NEVER written into any committed file — it
   is reported only in the final executor response after push and remote
   verification.

(The Phase-2 checklist above remains the phase-1 record of the plan; this
section records its execution. Per the phase-2 contract this HANDOFF is NOT
modified after manifest generation.)

## Terminal states (exact strings in FINAL_REPORT.md)

P2_1_BOUNDARY_CACHE = CORRECTED_SORTED_EXTENTS;
P2_2_66_0F8X_NEAR_JCC = CORRECTED_BRANCH_A_REL16;
P2_3_Q2_EFFECTIVE_ADDRESS = CORRECTED_RE_DERIVED_FROM_EXE;
H1_REG16_RM7 = CORRECTED_BX_TABLE;
H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY;
QC_VERDICT = QC_PASS (SELF_CHECK; gates Q1-Q14 PASS; 7/7 mutations);
RUN_STATUS = PHASE_1_COMPLETE_AWAITING_PE_MASTER_PRE_PUBLICATION_REVIEW.
