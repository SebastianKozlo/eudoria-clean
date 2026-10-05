# HANDOFF — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

Executor handoff to the PE-MASTER persistence phase. This run is a
correction+QC+package-freeze run ONLY: PE_MASTER_REVIEW_PERFORMED_BY_THIS_RUN
= NO; AUDIT_ENTRYPOINT_MODIFIED = NO; COMMIT_OR_PUSH_PERFORMED = NO;
MANIFEST_PREPARED_FOR_PERSISTENCE_PHASE = YES (generated LAST, bijection
verified; covers AUDIT_ENTRYPOINT.md at its CURRENT BASE state - the
persistence phase MUST regenerate and re-verify the manifest after adding
the run row).

## THE CORRECTION IN FIVE LINES

1. **D1**: the reserved `0F 73 /4` sub-encoding is REJECTED in both MMX and
   SSE2 forms by PER-OPCODE legal-reg tables (0F 71/72: {2,4,6}/{2,4,6};
   0F 73: {2,6}/{2,3,6,7}); /4 stays legal for 71/72; 66 0F 73 /3,/7 stay
   legal (PSRLDQ/PSLLDQ); all carried H2/H1/P2-2/P2-1 fixes preserved.
   Oracle (GNU objdump Binutils 2.44, captured BEFORE decoder evaluation):
   both negatives (bad); six legal controls at true lengths; unit battery
   72/72.
2. **D1 downstream falsifier** `0F 73 E0 02 E8 05 00 00 00 C3` (synthetic
   strong entry at +0): corrected machinery UNRESOLVED / NOT_VERIFIED / no
   promotion; the committed BASE modules reproduce the defect (CONFIRMED /
   PASS / target 0x00A0000E) in-run via a READ-ONLY import; .text census:
   zero occurrences of the affected pattern (so no real stream changed).
3. **D2**: gate Q2 binds the expected pin universe to the BASE-pinned
   c1_pin_ledger.py::PINS roster (Git blob 5a7b642f..., ast literal
   extraction, re-derived IN-RUN): JSON == CSV == roster multiset (133/133/133,
   each exactly once), per-claim va+role agreement, declared-totals
   agreement, EA applicability from the EXPECTED role (kind mutation FAILS
   the role check AND cannot disable EA validation), registry tamper check,
   and an EXE-vs-roster expect_ea spec cross-check; Q3 additionally verifies
   every CSV operand_kind against the EXE-derived kind.
4. **D2 controls**: 8/8 new mutations CAUSAL_PASS (compound kind+EA removals
   x2, whole-pin deletions x2, duplicate claim, extra claim JSON, extra
   claim CSV, synchronized JSON+CSV omission with adjusted totals); the 7
   retained controls (M1-M4, AF3/Q8 compound, M5, M6) reproduce 7/7.
5. **Regression vs the exact BASE package** (REGRESSION_DIFF.json): census
   CSV + pin CSV + AF3 ledger BYTE-IDENTICAL (2612/133/5 rows, 0 changes);
   C1/C2/C3 JSONs identical after excluding the declared `run` label; every
   content change is a declared D1/D2 addition. All 13 data gates + Q14
   PASS; 15/15 mutations causal; 72 unit entries; 14 boundary cases; 80
   oracle fixtures; supersession ledger 9 records, quotecheck-verified.
   Process honesty: three pre-first-full-pass construction fixes + the ONE
   authorized targeted QC repair round (two docs-mode Q14
   instrument/report-alignment findings, fixed; round exhausted) are
   disclosed in QC_REPORT.md / GENERATION_RECORD.md.

## Provenance

RUN_ID = PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
RUN_CLASS = LOAD_BEARING; RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
DISPATCH_AUTHORITY = PE-MASTER direct dispatch of 2026-10-05 (contract file
OPENCODE_F84_C2_C1_D1_D2_CORRECTION_COMPLETE_20261005.md read in full from
disk; STATIC-ONLY; NO_NESTED_TASKS).
NO_NESTED_TASKS = YES (absolute). CLIENT_EXECUTION = FORBIDDEN (none
occurred; static byte reads only). CANONICAL_GATE_EFFECT = NONE;
NEXT_EXPERIMENT_AUTHORIZED = NO.

## Baseline identity (measured at preflight and still true at package freeze)

BASE_SHA = 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92
HEAD_SHA_AT_PACKAGE_FREEZE = 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92
COMMIT_SHA = NOT_AVAILABLE_AT_PACKAGE_FREEZE (this run does not commit; the
resulting commit's own SHA is reported only AFTER the persistence phase's
push and remote verification; no committed artifact embeds its own commit
SHA; this HANDOFF is NOT modified after manifest generation).

## Package contents (37 package files + AUDIT_ENTRYPOINT.md row = 38 manifest rows)

- 8 root documents: INPUT_IDENTITIES.md, GENERATION_RECORD.md,
  FINAL_REPORT.md, QC_REPORT.md, EVIDENCE_INDEX.md, PE_MASTER_REVIEW.md
  (explicit placeholder), HANDOFF.md, SUPERSESSION_LEDGER.md (9 records).
- 2 root JSON artifacts: EXPECTED_PIN_REGISTRY.json (the D2 expected
  roster), REGRESSION_DIFF.json (the regression vs the exact BASE package).
- 5 root CSV artifacts/matrices: CORRECTED_PIN_LEDGER.csv (133 rows),
  CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv (2612 rows),
  AF3_PROVENANCE_LEDGER.csv (5 rows), AF1_MUTATION_MATRIX.csv (15 rows),
  AF2_BOUNDARY_TEST_MATRIX.csv (14 cases).
- 01_RAW/ (11 files): C1_PIN_EVIDENCE.json, C2_CENSUS.json,
  C3_OBJECT_SCOPE.json, CQC_FINAL.json (data+docs, LAST full run),
  CQC_MUTATION_RESULTS.json (7 retained), CQC_BOUNDARY_COUNTEREXAMPLES.json
  (14 cases), CQC_DECODER_UNIT_TESTS.json (72 entries),
  D1_INDEPENDENT_ORACLE_RECORDS.json (80 fixtures),
  D1_BOUNDARY_FALSIFIER.json, D2_MUTATION_RESULTS.json (8 controls),
  BASE_COMMIT_MESSAGE_VERBATIM.txt.
- 03_SCRIPTS/ (11 instruments): x86dec.py (D1 fix), pebnd.py (carried),
  c1_pin_ledger.py, c2_census.py, c3_object_scope.py (regenerators),
  cqc_battery.py (D1/D2 battery), capture_independent_evidence.py (oracle),
  pin_roster.py + extract_expected_pins.py (D2 roster),
  diff_vs_base.py (regression), make_manifest.py (manifest LAST).

MANIFEST_ROW_COUNT = 38 (measured by make_manifest.py's rule: every file
under this package except the manifest itself + AUDIT_ENTRYPOINT.md at its
CURRENT BASE state = 37 package files + 1 entrypoint file = 38 rows).

## Explicit NON-actions of THIS run (verified)

- AUDIT_ENTRYPOINT.md untouched (proposed row below; the persistence phase
  adds it - 1 insertion, 0 deletions, LF endings preserved - and then
  regenerates the manifest).
- No git add/commit/push; nothing staged; nothing written outside
  OUTPUT_ROOT; the six foreign untracked paths untouched; historical
  packages (C1/C2/THREE-P2) READ ONLY (verified by the byte-identity
  measurements in REGRESSION_DIFF.json).
- Temporary mutation/oracle trees under
  C:\Users\User\AppData\Local\Temp\opencode\d1d2_* deleted after use; no
  untracked writer left running.

## Persistence-phase checklist (for the PE-MASTER phase; NOT executed here)

1. Perform/persist the PE-MASTER internal pre-publication review verdict
   into PE_MASTER_REVIEW.md (replacing the placeholder).
2. Add exactly ONE NEW newest-first AUDIT_ENTRYPOINT.md row (the proposed
   row below; 1 insertion, 0 deletions, LF endings preserved).
3. Re-verify the BASE triple immediately before commit (LOCAL_HEAD ==
   ORIGIN/master == ACTUAL_REMOTE_MASTER == 9d31a82...; any divergence =
   BLOCKED_BASE_MOVED with an honest stop; no rebase, no merge, no force
   push).
4. Regenerate the manifest via 03_SCRIPTS/make_manifest.py (the entrypoint
   hash changes when the row is added) + re-verify the bijection and the
   HANDOFF MANIFEST_ROW_COUNT.
5. Path-limited staging of EXACTLY the 38 authorized paths below; commit
   once; push normally; no force push; never `git add .` (the six foreign
   untracked paths must stay untouched and unstaged).
6. Verify the exact remote SHA and report it (LOCAL_HEAD == ORIGIN_MASTER
   == ACTUAL_REMOTE_MASTER == the resulting commit SHA).

## Proposed AUDIT_ENTRYPOINT.md row (fragment; to be inserted at the top of
the LATEST RUNS table by the persistence phase; one line, LF-preserved)

| (this commit; discover with `git log -1 -- docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005`) | PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005 (RUN_CLASS LOAD_BEARING; RUN_TYPE DESKTOP_POST_AUDIT_FOCUSED_CORRECTION; the D1/D2 correction of the THREE-P2 package per the independent Desktop post-audit PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005 (BASE 9d31a82b; machinery repair ONLY -- NO new science; STATIC_ONLY -- the client never ran; EXE E7785430.../8,015,872 B re-verified in every instrument incl. every mutated execution; executor pe-reconstruction, targeted SELF_CHECK QC QC_SCOPE=SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION - no independent-QC claim; PE-MASTER direct dispatch, NO_NESTED_TASKS; persistence by the PE-MASTER phase): (D1) x86dec.py 0F 71/72/73 immediate-shift validity now uses PER-OPCODE legal-reg tables (71: {2,4,6}/{2,4,6}; 72: {2,4,6}/{2,4,6}; 73: {2,6}/{2,3,6,7} without/with 66) - the reserved 0F 73 /4 REJECTS in BOTH forms (oracle GNU objdump Binutils 2.44: (bad) for 0F 73 E0 02 and data16 (bad) for 66 0F 73 E0 02, captured BEFORE decoder evaluation); /4 stays legal for 71/72 (PSRAW/PSRAD), 66 0F 73 /3,/7 stay legal (PSRLDQ/PSLLDQ), mod=3/memory-form/F2-F3/0F BA behaviour unchanged; unit battery 72/72 (8 D1 entries); MANDATORY downstream falsifier 0F 73 E0 02 E8 05 00 00 00 C3 with a synthetic strong entry at +0: corrected machinery UNRESOLVED/NOT_VERIFIED/no promotion (the invalid initial instruction stops justified sequential decoding) while the committed BASE modules reproduce the defect CONFIRMED/PASS/target 0x00A0000E through an in-run READ-ONLY import (module identities recorded); .text census: ZERO occurrences of the affected pattern; (D2) gate_q2 binds the expected pin universe to the BASE-pinned c1_pin_ledger.py::PINS roster (Git blob 5a7b642f, ast literal extraction, re-derived IN-RUN from the BASE Git blob; EXPECTED_PIN_REGISTRY.json must EQUAL the git re-derivation): JSON claim multiset == CSV claim multiset == roster multiset (133/133/133, each exactly once), per-claim claim_id+VA+kind(role) agreement, declared-totals agreement (total_pins==roster==measured; status_tally==CSV-recomputed; fail_count==0), EA applicability derived from the EXPECTED role (kind mutation FAILS the role check AND cannot disable EA validation; 46/46 mem pins EXE-re-derived incl. the NEW roster expect_ea spec cross-check), Q3 additionally verifies every CSV operand_kind against the EXE-derived kind; 8/8 NEW D2 mutations CAUSAL_PASS (THE_STORE_plus_84 + stream_ctor_buffer_store: compound kind mem->code_entry + EA removal, and whole-pin deletion, each PASS->FAIL; duplicate claim; extra claim JSON; extra claim CSV; synchronized JSON+CSV omission with internally consistent adjusted totals - all caught by the gate's OWN predicates, no manifest/Git-baseline/other-gate substitute); the 7 retained controls M1-M4+AF3/Q8(compound)+M5/M6 reproduce 7/7; NEW-F (cached+uncached+permutation proofs)/NEW-G/H1/AF2 A1-A-E/REAL-REFUTE x2/3 real positive CALLs all reproduced; regression vs the exact BASE package: census CSV + pin CSV + AF3 ledger BYTE-IDENTICAL (2612/133/5 rows, 0 changes), C1/C2/C3 JSONs identical after the declared run label, all content changes are declared D1/D2 additions (unit battery 64->72, boundary cases 13->14, oracle fixtures 71->80, +EXPECTED_PIN_REGISTRY.json +D1_BOUNDARY_FALSIFIER.json +D2_MUTATION_RESULTS.json +BASE_COMMIT_MESSAGE_VERBATIM.txt); supersession ledger S-D1-01..03 + S-D2-01..04 + S-CM-01 + S-AUD-01 (9 records, quotecheck-verified; the BASE 'complete repair'/'H2 family closure'/'46/46 Q2 coverage' wordings retracted with exact quotes); PRESERVED CORE re-measured unchanged (FUN_0070C680 / 0x0070C71E / 89 86 84 00 00 00 / 0xA4=164 B / FUN_00972380); NEW_BACKING_SOURCE_RE_EXECUTED=NO, TEMPLATES_VFS_OPENED=NO, RECORD_A_ANALYZED=NO, MODEL_194013_TRACE_EXECUTED=NO, PLACEMENT_XYZ_RE_EXECUTED=NO, CLIENT_EXECUTED=NO, CANONICAL_GATE_EFFECT=NONE, NEXT_EXPERIMENT_AUTHORIZED=NO; executor SELF_CHECK QC = QC_PASS (Q1-Q14 gates + 15/15 causal mutations; three pre-first-full-pass construction fixes + the ONE authorized targeted QC repair round (two Q14 instrument/report-alignment findings, fixed) disclosed in QC_REPORT.md); package = 8 root docs + 2 root JSON + 5 root CSV + 11 raw + 11 scripts + manifest generated LAST (38 rows, self-excluded; scope = every file under this package + AUDIT_ENTRYPOINT.md; bijection verified: no missing/extra/duplicate, all sizes/SHA256 match; HANDOFF-declared MANIFEST_ROW_COUNT = 38 cross-checked); foreign untracked paths untouched | (pending -- PE-MASTER review not yet performed; no independent verdict exists) |

## Proposed commit message (for the persistence phase; corrected wording per
ledger record S-CM-01; the phase may adapt it - the BASE commit message and
history are immutable either way)

PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005: the D1/D2 correction of the THREE-P2 package per the independent Desktop post-audit PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005 (BASE 9d31a82; machinery repair ONLY -- NO new science; STATIC_ONLY -- the client never ran; EXE E7785430.../8,015,872 B re-verified in every instrument): (D1) x86dec.py per-opcode legal-reg tables for the 0F 71/72/73 immediate-shift family -- the reserved 0F 73 /4 REJECTS in both MMX and SSE2 forms (oracle GNU objdump Binutils 2.44: (bad); captured before decoder evaluation), /4 stays legal for 71/72, 66 0F 73 /3,/7 stay legal (PSRLDQ/PSLLDQ); downstream falsifier 0F 73 E0 02 E8 05 00 00 00 C3: corrected machinery stops justified sequential decoding at the invalid first instruction (UNRESOLVED/NOT_VERIFIED/no promotion) while the committed BASE modules reproduce the unearned CONFIRMED/PASS/target 0x00A0000E (in-run READ-ONLY import); .text census: zero occurrences of the affected pattern, so no census/pin row changed; (D2) gate_q2 binds the expected pin universe to the BASE-pinned c1_pin_ledger.py::PINS roster re-derived in-run from the BASE Git blob: JSON == CSV == roster claim multisets (133/133/133, each exactly once), per-claim VA+role agreement, declared-totals agreement, EA applicability from the EXPECTED role (a mutated kind FAILS the role check and cannot disable EA validation; 46/46 EXE-re-derived + the new expect_ea spec cross-check; registry tamper = FAIL), Q3 verifies every CSV operand_kind against the EXE-derived kind; 8/8 new D2 mutations causal (compound kind+EA removals, whole-pin deletions, duplicate claim, extra claims, synchronized JSON+CSV omission with adjusted totals) + 7/7 retained controls; regression vs BASE: census CSV + pin CSV + AF3 ledger byte-identical, C1/C2/C3 JSONs run-label-only, all content changes are declared D1/D2 additions; supersession ledger 9 records (the BASE 'complete repair'/H2-family-closure/Q2-coverage wordings retracted with exact quotes); executor SELF_CHECK QC = QC_PASS (Q1-Q14 + 15/15 causal mutations; 72 unit entries; 14 boundary cases; 80 oracle fixtures); PRESERVED CORE unchanged (FUN_0070C680 / 0x0070C71E / 89 86 84 00 00 00 / 0xA4=164 B / FUN_00972380); CANONICAL_GATE_EFFECT=NONE; NEXT_EXPERIMENT_AUTHORIZED=NO; persistence by the PE-MASTER phase within the authorized allowlist (entrypoint row + regenerated manifest + commit/push + remote verification)

## Staging allowlist for the persistence phase (EXACTLY these 38 paths;
never `git add .`; the six foreign untracked paths must NOT be staged)

```text
AUDIT_ENTRYPOINT.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/C1_PIN_EVIDENCE.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/C2_CENSUS.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/C3_OBJECT_SCOPE.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/CQC_DECODER_UNIT_TESTS.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/CQC_FINAL.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/CQC_MUTATION_RESULTS.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/D1_BOUNDARY_FALSIFIER.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/D2_MUTATION_RESULTS.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/c1_pin_ledger.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/c2_census.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/c3_object_scope.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/capture_independent_evidence.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/cqc_battery.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/diff_vs_base.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/extract_expected_pins.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/make_manifest.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/pebnd.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/pin_roster.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/03_SCRIPTS/x86dec.py
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/AF1_MUTATION_MATRIX.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/AF2_BOUNDARY_TEST_MATRIX.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/AF3_PROVENANCE_LEDGER.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/COMMITTED_PACKAGE_MANIFEST_SHA256.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/CORRECTED_PIN_LEDGER.csv
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/EVIDENCE_INDEX.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/EXPECTED_PIN_REGISTRY.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/FINAL_REPORT.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/GENERATION_RECORD.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/HANDOFF.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/INPUT_IDENTITIES.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/PE_MASTER_REVIEW.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/QC_REPORT.md
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/REGRESSION_DIFF.json
docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/SUPERSESSION_LEDGER.md
```

(The manifest itself is the 38th package path; the 37 package files above
plus AUDIT_ENTRYPOINT.md are exactly the manifest's bijection scope. After
the entrypoint row is added, regenerate the manifest so its AUDIT_ENTRYPOINT
row matches the updated file.)

## Terminal states (exact strings in FINAL_REPORT.md)

D1_H2_0F73_4_STATUS = CORRECTED_PER_OPCODE_LEGAL_REG_TABLES;
D1_INVALID_FIXTURES = 2/2_REJECTED;
D1_DOWNSTREAM_CALL_STATUS = CORRECTED_NO_PASS_NO_PROMOTION_NOT_VERIFIED;
D2_PINSET_STATUS = CORRECTED_ROSTER_BOUND_BIDIRECTIONAL_MULTISET;
D2_ROLE_APPLICABILITY_STATUS = CORRECTED_EXPECTED_ROLE_DRIVEN_EA;
H2_GROUP_OPCODES = CORRECTED_PER_OPCODE_VALIDITY_TABLES;
P2_1_BOUNDARY_CACHE = PRESERVED_CORRECTED_SORTED_EXTENTS (REPRODUCED_THIS_RUN);
P2_2_66_0F8X_NEAR_JCC = PRESERVED_CORRECTED_BRANCH_A_REL16 (REPRODUCED_THIS_RUN);
P2_3_Q2_EFFECTIVE_ADDRESS = PRESERVED_CORRECTED_RE_DERIVED_FROM_EXE (D2_EXTENDS);
H1_REG16_RM7 = PRESERVED_CORRECTED_BX_TABLE (REPRODUCED_THIS_RUN);
QC_VERDICT = QC_PASS (SELF_CHECK; gates Q1-Q14 PASS; 15/15 mutations causal);
RUN_STATUS = PACKAGE_FROZEN_AWAITING_PE_MASTER_PERSISTENCE_PHASE.
