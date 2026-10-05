# QC REPORT — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION
Author/origin: pe-reconstruction worker session (executor self-QC), run under
the PE-MASTER direct dispatch of 2026-10-05. This is NOT an independent
audit; the independent Desktop post-audit of the eventually published commit
remains a separate human-relayed step, and the PE-MASTER internal review is
the persistence-phase gate (advisory/pre-qualification;
CANONICAL_GATE_EFFECT = NONE).

## Battery

Instrument: 03_SCRIPTS/cqc_battery.py (the D1/D2-corrected battery; every
status derived from measured inputs on disk; no hard-coded PASS).
Executions: `--mode data` then `--mode docs` (the committed record is the
LAST full run; both runs re-hash the pinned EXE
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 /
8,015,872 B at every execution, clean and mutated alike).

## Data-mode result (01_RAW/CQC_FINAL.json)

- Gates Q1-Q13: 13/13 PASS.
  - Q1 baseline: EXE pinned-match + LOCAL_HEAD == origin/master ==
    actual-remote == 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92 (pre-commit
    state; the persistence-phase commit moves the HEAD BY DESIGN).
  - Q2 (D2-corrected): the expected roster re-derived in-run from the
    BASE-pinned c1_pin_ledger.py::PINS Git blob (133 claims; roles
    bytes=38/mem=46/imm32=14/call=29/imm8=4/declassified=2);
    EXPECTED_PIN_REGISTRY.json == the git-derived roster; JSON claim
    multiset == CSV claim multiset == roster multiset (133/133/133, each
    exactly once, 0 duplicates/extra/missing); per-claim va + kind(role)
    agreement; declared totals agree (total_pins=133, fail_count=0,
    status_tally == CSV-recomputed); EA applicability from the EXPECTED
    role: 46 mem-role pins checked, 46 re-derived from the EXE, 0
    mismatches, 0 JSON<->CSV EA inconsistencies; the EXE-derived EA also
    cross-checked against the roster's pinned expect_ea spec (0 mismatches).
  - Q3: all 133 CSV rows re-derived full-row; NEW: every row's claim
    membership + VA checked against the roster and every operand_kind
    verified against the EXE-derived kind (0 mismatches).
  - Q4: decoder unit battery 72/72 entries (measured count; +8 D1 entries
    incl. 2 byte-duplicates of carried patterns with D1 notes), census
    re-decode 2612/2612 rows clean, coverage windows sane.
  - Q5: boundary matrix 14/14 cases (A1, A2, B, C, D, E, NEW-F incl. the
    cached+uncached crosscheck and the order-permutation proofs, NEW-G,
    D1_0F73_4_DOWNSTREAM_FALSIFIER, 2x REAL-REFUTE, 3x REAL positive
    controls) + non-E8 control + census discipline sweep + anchor registry
    complete. The D1 falsifier: corrected machinery UNRESOLVED /
    NOT_VERIFIED / no promotion; BASE modules (READ-ONLY import)
    reproduce the defect CONFIRMED/PASS/target 0x00A0000E; .text census:
    zero occurrences of the affected pattern.
  - Q6: all 2227 positive census rows boundary-re-derived; 0 mismatches.
  - Q7: AF3 discipline (manager PROVEN chain physically re-verified; the
    four downgraded layout controls stay UNRESOLVED); ledger<->census
    consistent.
  - Q8: C3 store collection re-derived (3 stores, 2 FS:[0] segment stores
    excluded from this+0 eligibility); DIRECT_VPTR status match.
  - Q9: census arithmetic re-summed from the emitted CSV - all consistency
    predicates true; RAW_PATTERN_ROWS regression 2612 MATCH.
  - Q10: both known stores re-pinned (bytes + CONFIRMED boundary +
    THIS_OF_KNOWN_FUNCTION provenance).
  - Q11: enumeration membership derived from measured bounds; CONTROL B
    mutant fails.
  - Q12: object structural identity checks (incl. THE_STORE_plus_84
    VALIDATED).
  - Q13: declared family count agreement (9, derived from len(FAMILIES)).
- Mutations: 15/15 CAUSAL_PASS - OLD_MUTATION_TOTAL = 7 (M1, M2, M3, M4,
  AF3/Q8 compound, M5, M6 - each UNMUTATED=PASS -> MUTATED=FAIL through the
  SAME production gate function object) + D2_NEW_MUTATION_TOTAL = 8
  (D2-M1..M8 - each an isolated temp copy of the ACTUAL regenerated C1
  JSON/CSV through the SAME gate_q2, with per-case input-hash censuses
  proving the unrelated inputs byte-identical; exact failing predicates,
  semantic deltas and before/after artifact hashes in
  01_RAW/D2_MUTATION_RESULTS.json).
- QC_VERDICT (data): QC_PASS.

## Docs-mode result (the LAST full run; the committed CQC_FINAL.json)

- Q14: required-string battery over FINAL_REPORT.md (all preserved-core,
  D1/D2 correction-status and phase-semantics strings present);
  forbidden/overclaim phrase sweep over the active claim surfaces (0 hits;
  the retracted BASE claims appear only as ledger ORIGINAL_EXCERPT quotes);
  supersession quotecheck - all ORIGINAL_EXCERPTs machine-verified verbatim
  in their named READ-ONLY sources, 9 records = declared
  NEW_SUPERSESSION_RECORD_COUNT; commit-message verbatim fidelity
  (01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt == `git log -1 --format=%B
  9d31a82...`); required-files battery over the contract package list (0
  missing); P3-C identity hygiene (C1 historical typo count 1; new identity
  present; typo absent from this package); forbidden-input census over the
  instruments (no .vfs/.bnt/.nif/.ark opened; no http literals).
- QC_VERDICT (full, data+docs): QC_PASS. Final console line of the
  committed record:
  `CQC done (docs). gates: {"Q1": "PASS", ..., "Q14": "PASS"} mutations_causal=15/15 verdict=QC_PASS`

## In-run construction fixes (disclosed; items 1-3 are BEFORE the first full
battery pass - NOT QC repair rounds)

1. The first data-mode invocation crashed in `run_d2_mutations` (a
   format-string argument misplacement in the temp-input census
   construction; TypeError; NO artifact written by the aborted run). Fixed
   and re-run; the committed battery is the fixed version.
2. The Q14 record-header regex updated from the BASE S-P2-* prefix to this
   ledger's S-D1/S-D2/S-CM/S-AUD prefixes (pre-docs-run).
3. Cosmetic stdout denominator fix only (no artifact content).

## THE ONE authorized targeted QC repair round (USED; within D1/D2)

The first `--mode docs` execution FAILED Q14 with exactly two findings,
both instrument/report alignment items inside the correction scope:

1. the Q14 required-string battery still demanded the BASE-form core status
   string `FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL`
   while this package (per the dispatch contract) carries the
   `PRESERVED_CONFIRMED_STATIC_CONDITIONAL` form - the battery's required
   list was corrected to the contract form (FINAL_REPORT was already
   correct; no evidence artifact was touched);
2. the supersession ledger's S-AUD-01 summary line restated a
   retracted-claim phrase from the forbidden list (the audited state's
   blocker-free-for-dependent-reuse implication) outside an
   ORIGINAL_EXCERPT context - the wording was rephrased to describe the
   retracted implication without restating it as a claim (the ledger
   record's quotes and semantics are unchanged).

After the two fixes the full `--mode docs` run passed:
`CQC done (docs). gates: {"Q1": "PASS", ..., "Q14": "PASS"} mutations_causal=15/15 verdict=QC_PASS`
(the committed CQC_FINAL.json is the LAST full run, executed after these
document updates). No further material defect remains; the repair-round
budget is now exhausted by design.

## Outcome-conditional statement

QC PASS means the corrected claims accurately match evidence and stated
uncertainty; it does NOT mean all census candidates were solved (the 2218
unresolved census rows and every NOT_ESTABLISHED/UNVERIFIED state in
FINAL_REPORT.md are the corrected honest states, not failures). No defect
known to this run remains open INSIDE the D1/D2 correction scope; the
machinery's validity boundary is the measured fixture/mutation set, not a
general x86/QC claim.

## Record-repair mention (2026-10-05; internal-QC follow-up — record hygiene, NOT a new QC round)

Author/origin: pe-reconstruction worker session under the PE-MASTER
record-repair dispatch of 2026-10-05; the two findings originate from the
internal QC worker run PE_935_QC_INTERNAL_20261005 (00_CONTROL_INTERNAL_QC/,
read-only for this executor), which independently reproduced the D1/D2
results and returned verdict QC_PASS_WITH_FINDINGS with two P2
record/provenance findings. Both were fixed as record repair:

1. F1 (fixed): the committed 01_RAW/CQC_FINAL.json carried the BASE
   THREE-P2 qc_scope value from a stale instrument literal
   (03_SCRIPTS/cqc_battery.py:2745). The literal was corrected to this run's
   declared QC_SCOPE and the battery re-executed (`--mode data` then
   `--mode docs`; the committed record is the LAST full run of the repaired
   sequence). The record now self-identifies as
   SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION with the SAME measured
   verdict as before the repair: 14/14 gates PASS (Q1-Q14) + 15/15 mutations
   CAUSAL_PASS (7/7 retained + 8/8 D2), QC_VERDICT = QC_PASS. Final console
   line of the repaired committed record:
   `CQC done (docs). gates: {"Q1": "PASS", ..., "Q14": "PASS"} mutations_causal=15/15 verdict=QC_PASS`
2. F2 (fixed): REGRESSION_DIFF.json had recorded the SHA256 of an
   intermediate data-mode 01_RAW/CQC_MUTATION_RESULTS.json (the original
   diff_vs_base execution predated the final docs-mode battery; the
   mutation records' mkdtemp temp-path fields — internal-QC observation O1 —
   make the two runs differ bit-wise while semantically identical).
   diff_vs_base.py was re-executed AFTER the final battery re-run; every
   sha256_new declaration in the committed REGRESSION_DIFF.json now
   re-hashes true against the final physical artifacts (9/9 + 9/9
   sha256_base, re-validated by the executor outside the package; the
   CQC_MUTATION_RESULTS.json row declares 0981403799355FC32E555C045D19C38B84165B2BDCD32563874FAB79D8B77E30
   == the file on disk).

Both fixes are record/provenance repairs only. No D1/D2 measured result,
PIN, CORE status, or supersession-ledger record changed: the 9 existing
ledger records are unedited, and this section is an explicit record-repair
mention, NOT a new supersession record. The refreshed battery outputs whose
content changed are exactly: CQC_FINAL.json (F1), CQC_MUTATION_RESULTS.json
and D2_MUTATION_RESULTS.json and AF1_MUTATION_MATRIX.csv (fresh runs; the
observation-O1 mkdtemp temp-path fields only — ids, causality and failing
predicates identical), and REGRESSION_DIFF.json (F2); the generation
commands, console lines and the full repaired-file census are recorded in
GENERATION_RECORD.md (steps 11-13). The manifest regeneration remains
assigned to the persistence phase (manifest LAST), so
COMMITTED_PACKAGE_MANIFEST_SHA256.csv is stale for the repaired artifacts by
design until that phase.
