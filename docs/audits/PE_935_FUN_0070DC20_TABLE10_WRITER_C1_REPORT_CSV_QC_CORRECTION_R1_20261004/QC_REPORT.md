# QC_REPORT — PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004

QC_SCOPE = SELF_CHECK_TABLE10_WRITER_C1 (targeted correction SELF_CHECK; no
independent-QC claim). MODE: STATIC-ONLY (no new reverse engineering; the
client never ran). Battery: 03_SCRIPTS/qc_table10_writer_c1.py ->
01_RAW/{QC_LEDGER_BUDGET, QC_CSV_STRICT, QC_VALUE_SCOPE,
QC_NEGATIVE_CONTROLS}.json. Every gate status below is COMPUTED FROM
MEASURED INPUTS at execution time; no target PASS state was copied into the
output. The battery was executed in two passes: pass A (all corrected claim
surfaces present; QC_REPORT.md not yet written) and pass B (final; the
absence sweep then also covers QC_REPORT.md). The committed 01_RAW records
are the pass-B outputs. Honest in-run battery defects caught and fixed
during pass A (recorded here as the error-detection record): (1) an
INPUT_IDENTITIES.md transcription error in one historical-source SHA256 row
was DETECTED by the Q1 input-identity cross-check and corrected (the gate
failed honestly first); (2) the Q13 script self-census originally counted
its own census string literal as an EXE read call (5 vs 4) — fixed to count
assignment call-sites only; (3) two wording-presence checks (Q7 scope
statement, Q12 bounded question) originally used raw substring matching
that failed on the report's line wrapping — fixed to whitespace-normalized
matching (the established repo quotecheck convention).

## Gate-by-gate verdicts (pass B, measured)

### Q1 — baseline + input identities: PASS
- local HEAD == local origin/master == actual remote master ==
  4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 (rev-parse after fetch +
  ls-remote; re-verified again immediately before commit).
- All 8 declared historical-source identities (INPUT_IDENTITIES.md) re-
  measured byte-identical at QC time (0 mismatches); corrected CSV
  identities recorded in 01_RAW/QC_LEDGER_BUDGET.json.

### Q2 — historical core writer science preserved: PASS
- Historical FINAL_REPORT measured to contain the core writer claims
  (writer FUN_009777F0 @0x00977810; TABLE10_WRITE/SAME_COMPONENT_IDENTITY/
  ATTRIBUTE10_SELECTION CONFIRMED; CONTROL_CASE PASS; RECORD_FIELD source
  representation; ULTIMATE_VALUE_SOURCE UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED
  NO; RECORD_A_RELATION/WORLD_INSTANCE_SEMANTIC NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED NO).
- Corrected FINAL_REPORT measured to preserve them all in the corrected
  taxonomy (WRITER_MECHANISM/SAME_STORAGE_IDENTITY
  CONFIRMED_STATIC_CONDITIONAL; TAG6_TO_ID10 CONFIRMED; all preserved
  UNKNOWN/NO states).

### Q3 — CORRECTED_FUNCTION_LEDGER.csv strict CSV: PASS
- csv.reader parse OK; header exactly 7 columns; 8 data rows; every row
  exactly header width (CSV_WIDTH_MISMATCHES=0, CSV_EXTRA_FIELDS=0);
  DictReader: no rows with a None key, no missing fields; ordinals unique
  1..8; UTF-8 round trip OK; write->read->write semantic round trip OK;
  embedded separators preserved as field content in all 8 rows.
- Historical measurement (READ-ONLY, preserved): 7-column header, 8 data
  rows, 5 malformed-width rows.
- Logical content: re-derived from the historical file with byte-accounting
  join round-trips; diffs vs the corrected CSV == EXACTLY the one authorized
  change (F-1, P3-A fail-path VA). FUNCTION_LEDGER_CSV = CORRECTED_VALID
  (measured; declared value cross-checked equal).

### Q4 — CORRECTED_WRITER_CHAIN.csv strict CSV: PASS
- Same battery: 6-column header; 26 data rows; all exact width; steps
  unique 1..26; UTF-8 + write->read->write round trips OK; embedded
  separators preserved.
- Historical measurement (READ-ONLY, preserved): 6-column header, 26 data
  rows, 22 malformed-width rows.
- Logical content: diffs == EXACTLY the one authorized change (F-2, W3
  storage-identity scope wording). WRITER_CHAIN_CSV = CORRECTED_VALID
  (measured; declared value cross-checked equal).

### Q5 — ledger-derived canonical function-count/budget check: PASS
- CORRECTED_FUNCTION_LEDGER.csv parsed FROM DISK; all values DERIVED:
  HEADER_COLUMN_COUNT=7; DATA_ROW_COUNT=8; ORDINAL_SEQUENCE=1..8;
  ORDINAL_UNIQUE=YES; FUNCTION_FIELD_NONEMPTY=YES; COUNT_BEFORE_SEQUENCE=
  0..7; COUNT_AFTER_SEQUENCE=1..8; every row count_after==count_before+1;
  every count_before < MAX(8); final count_after == LEDGER_DECLARED_COUNT == 8.
- THREE SEPARATE predicates (never collapsed): LEDGER_STRUCTURE_STATUS =
  PASS; EXPECTED_CANONICAL_ROW_COUNT_STATUS = PASS; BUDGET_LIMIT_CHECK =
  PASS (derived count 8 <= 8). FUNCTION_BUDGET_LEDGER_VALIDATION = PASS;
  FUNCTION_BUDGET_PRECHECK = PASS (both derived).
- W1 epistemic scope enforced: EXECUTION_TIMING_PRECHECK_INDEPENDENTLY_
  ESTABLISHED = NO (the validator proves the LEDGER-DECLARED facts only; no
  chronological pre-check evidence is manufactured).
- The historical S5 hard-code defect (its NEW_FUNCTION_COUNT literal 7 that
  never parsed the ledger and contradicted the report's 8) is SUPERSEDED
  (records S-1/S-2); HISTORICAL_Q10_HARDCODE_DEFECT = SUPERSEDED.

### Q6 — structurally-valid 9-row ledger mutant (negative control): PASS
- PRIVATE synthetic mutant (canonical 8 rows + one synthetic 9th entry),
  written to a TEMP path OUTSIDE the repo, validated from disk with the SAME
  generic validator, then deleted (temp file removal verified).
- Measured: VALID_CSV=YES; HEADER_WIDTH_CORRECT=YES; UNIQUE_FUNCTIONS=YES;
  ORDINAL 1..9; COUNT_BEFORE 0..8; COUNT_AFTER 1..9; per-row
  count_after==count_before+1; LEDGER_STRUCTURE_STATUS = PASS;
  NINE_ROW_MUTANT_NEW_FUNCTION_COUNT = 9 (derived); BUDGET_LIMIT_CHECK =
  FAIL (9 > 8); FUNCTION_BUDGET_PRECHECK = FAIL;
  EXPECTED_CANONICAL_ROW_COUNT_STATUS = NOT_APPLICABLE_TO_MUTANT (the
  9-vs-8 canonical row mismatch is reported as a SEPARATE predicate and is
  NOT the budget failure's cause — the budget predicate uses only the
  derived count vs MAX). TEST_VALIDITY = VALID (the failure is specifically
  the budget excess, not a structural mismatch).

### Q7 — value-identity wording correctly scoped: PASS
- The corrected scope statement is present in FINAL_REPORT.md
  (whitespace-normalized match).
- CORRECTED_WRITER_CHAIN.csv row 26 measured to contain the scoped wording
  (reads the CURRENT value of table[10]; storage identity
  CONFIRMED_STATIC_CONDITIONAL; preservation NOT_ESTABLISHED; SAME storage
  entry) and NOT the superseded wording.
- Superseded-phrase absence sweep over ALL active claim surfaces
  (FINAL_REPORT.md, HANDOFF.md, INPUT_IDENTITIES.md, QC_REPORT.md,
  CORRECTED_FUNCTION_LEDGER.csv, CORRECTED_WRITER_CHAIN.csv): ZERO hits.
  SUPERSESSION_LEDGER.md is the designated record of old claims (its quotes
  are verified against BASE by the AUX quotecheck instead); the historical
  package is READ-ONLY.
- Terminal state declares SAME_STORAGE_IDENTITY and WRITER_MECHANISM =
  CONFIRMED_STATIC_CONDITIONAL (measured present).

### Q8 — SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER: PASS
- Declared in the corrected terminal state == UNVERIFIED and present in the
  FINAL_REPORT text (measured).

### Q9 — WRITE_TO_LATER_GETTER_VALUE_PRESERVATION: PASS
- Declared == NOT_ESTABLISHED and present (measured).

### Q10 — fail-path zero-store VA (P3-A): PASS
- CORRECTED_FUNCTION_LEDGER.csv contains 0x0097781E and does NOT contain the
  superseded VA (measured).
- FAILPATH_ZERO_STORE_VA = 0x0097781E declared in the corrected terminal
  state (measured present).
- EXE identity re-verified (8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312
  414B17BC9FCE61389689A22F753765D5280F31 — the ONLY EXE reads in this run
  are the four P3 pin windows).
- Byte re-read: 0x0097781E = C7 00 00 00 00 00 (the fail-path zero store);
  the superseded VA (record S-7) measures 8B 44 = operand bytes mid-stream,
  NOT a C7 store start.
- Disclosure: the historical S5 machine pin was already at 0x0097781E
  (measured from the historical S5_QC_BATTERY.json) — the historical defect
  was the ledger row only.

### Q11 — component vtable store VA (P3-B): PASS
- COMPONENT_VTABLE_STORE_VA = 0x007374D6 declared in the corrected terminal
  state (measured present); component-vtable identity 0x00A86F2C unchanged.
- Byte re-read: 0x007374D6 = C7 06 2C 6F A8 00 (the store start); the
  superseded prose VA (record S-9) measures 8B C6 = mid-stream operand
  bytes, NOT a C7 store start.
- Disclosure: the historical S5 machine pin was already at 0x007374D6
  (measured from the historical S5_QC_BATTERY.json) — the historical defect
  was prose-only.

### Q12 — next-experiment wording bounded: PASS
- The bounded question (WHO ASSIGNS factory+0x84 AND WHAT EXACT
  OBJECT/VALUE IS ASSIGNED THERE?) is present (whitespace-normalized
  match); the four-outcome taxonomy is present; no source-class-closure
  promise (the superseded closure phrases are absent — measured);
  NEXT_EXPERIMENT_EXECUTED = NO declared; the separately-authorized-later-
  question boundary is stated.

### Q13 — forbidden-new-science census: PASS
- Declared census all NO: factory+0x84 trace, source-stream trace, callback
  decode, templates.vfs access, RECORD_A analysis, Model 194013 trace,
  world placement/XYZ, model join, NIF work, client execution, network
  trace, new RE beyond the P3 pins — none executed (enforced by
  construction: the QC instrument contains no such code paths).
- Physical package census: no forbidden payload file types (.vfs/.nif/.glb/
  .exe/.dll/.bnt/.ark/.tga) anywhere in the package; EXE byte reads bounded
  to exactly 4 windows (16 bytes total) — counted from the script source.
- No new-science claim keys in the corrected docs (measured).

### Q14 — preserved UNKNOWN/NOT_ESTABLISHED states: PASS
- All 11 preserved states measured present and equal in the corrected
  terminal state: SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED;
  WRITE_TO_LATER_GETTER_VALUE_PRESERVATION=NOT_ESTABLISHED;
  NO_CLOBBER_BETWEEN_WRITE_AND_READ=NOT_ESTABLISHED;
  RUNTIME_EVENT_ORDER=NOT_ESTABLISHED;
  RUNTIME_CACHE_BINDING_AT_SPECIFIC_GETTER_EVENT=NOT_OBSERVED;
  ULTIMATE_VALUE_SOURCE=UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED=NO;
  RECORD_A_RELATION=NOT_ESTABLISHED; WORLD_INSTANCE_SEMANTIC=NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED=NO; TABLE10_SOURCE_VALUE_REPRESENTATION=RECORD_FIELD.

### AUX — supersession quotecheck: PASS
- 12 records counted (S-1..S-10 + F-1/F-2; minimum 11 satisfied).
- 14 excerpt checks (10 ORIGINAL_EXCERPT + 2 OLD_LOGICAL_CONTENT verified
  as real substrings of their named SOURCE_FILEs at BASE 4627d38 via
  git show; 2 NEW_LOGICAL_CONTENT verified present in the corrected CSVs):
  14/14 verified.

## Rollup

QC_RESULT = PASS: 14/14 gates PASS + AUX quotecheck PASS (pass B; measured;
SELF_CHECK scope — no independent-QC claim). PACKAGE_CORRECTION_STATUS =
CORRECTED holds because every load-bearing gate succeeded; the two authorized
CSV content changes are the ONLY logical deltas (Q3/Q4 diff measurements);
the 9-row negative control failed exactly on the budget (Q6); the historical
S1-S5 physical evidence was NOT rerun and NOT replaced.
