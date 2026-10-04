# HANDOFF — PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004

To: PE-MASTER. From: pe-reconstruction (bounded worker; NO_NESTED_TASKS).
This package is the REPORT/CSV/QC/CLAIM-SCOPE correction of the historical
PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004 package (BASE 4627d385) per
the independent Desktop post-audit findings W1/W2/W3 + P3 hygiene ONLY. NO
new reverse engineering was performed: no callback decode, no factory+0x84
trace, no source-stream trace, no templates.vfs access, no RECORD_A
analysis, no Model 194013 trace, no world placement/XYZ, no model join, no
NIF work, no client execution. The only EXE byte reads are the four tiny P3
pin windows inside the QC script.

## One-paragraph result

All three P2 findings are corrected and the physically confirmed core
writer science is preserved. (W1) The historical S5 function-budget gate
hard-coded its count literal and never parsed the ledger — SUPERSEDED by a
corrected gate that parses CORRECTED_FUNCTION_LEDGER.csv from disk and
DERIVES LEDGER_DECLARED_COUNT = 8 (measured; structure/row-count/budget kept
as three SEPARATE predicates; EXECUTION_TIMING_PRECHECK_INDEPENDENTLY_
ESTABLISHED = NO recorded honestly). (W2) The historical CSVs were not valid
strict CSV (5/8 and 22/26 malformed-width rows measured) — corrected files
now serialize the same logical content with standard csv quoting
(FUNCTION_LEDGER_CSV = CORRECTED_VALID; WRITER_CHAIN_CSV = CORRECTED_VALID,
measured; the QC re-derives the logical content from the historical files
and verifies EXACTLY the two authorized field changes). (W3) The getter
wording is scoped to storage identity: the writer mechanism can write the
table[10] entry the getter addresses and the getter reads the CURRENT value;
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED;
WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED;
NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED. (P3-A) the corrected
fail-path zero-store VA is 0x0097781E (byte re-verified; the ledger row was
the only wrong location historically). (P3-B) COMPONENT_VTABLE_STORE_VA =
0x007374D6 (byte re-verified; the defect was prose-only — the historical S5
machine pin was already correct). (P3-C) the next experiment is narrowed to
the factory+0x84 assignment/object question only. The 9-row negative control
is structurally VALID and fails SPECIFICALLY on the budget (count 9 > 8) —
its budget failure does not depend on the row-count mismatch (separate
predicates). PACKAGE_CORRECTION_STATUS = CORRECTED because every
load-bearing QC gate succeeded; on any failure the honest value would be
PARTIAL with the measured failure recorded.

## What is preserved (no science downgraded)

The complete writer mechanism: record cursor -> tag -> schema descriptor
(id = tag+4; tag 6 -> id 10) -> [class_obj+0x40]+10*4 -> FUN_0075F660 ->
FUN_009777F0 -> MOV [EDX],EAX @0x00977810 (value read from the record
cursor @0x00977807). ATTRIBUTE10_WRITER_MECHANISM = CONFIRMED;
WRITER_FUNCTION = FUN_009777F0; WRITER_VA = 0x00977810; TAG6_TO_ID10 =
CONFIRMED; TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD;
ULTIMATE_VALUE_SOURCE = UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED = NO;
RECORD_A_RELATION = NOT_ESTABLISHED; WORLD_INSTANCE_SEMANTIC =
NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO. The same factory/receiver/cache
identity chain is preserved in its static-conditional form
(SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL). The historical
S1-S5 raw byte evidence stands untouched and is not rerun.

## What THIS package adds/changes

- CORRECTED_FUNCTION_LEDGER.csv + CORRECTED_WRITER_CHAIN.csv (W2; logical
  content preserved except F-1/F-2, each recorded in SUPERSESSION_LEDGER.md).
- SUPERSESSION_LEDGER.md: 12 records (S-1..S-10 + F-1/F-2); every
  ORIGINAL_EXCERPT and OLD_LOGICAL_CONTENT is machine-verified a real
  substring of its named source at BASE; NEW_LOGICAL_CONTENT verified
  present in the corrected CSVs.
- 03_SCRIPTS/qc_table10_writer_c1.py: the targeted correction QC battery
  (Q1-Q14 + AUX quotecheck) producing 01_RAW/QC_LEDGER_BUDGET.json,
  QC_CSV_STRICT.json, QC_VALUE_SCOPE.json, QC_NEGATIVE_CONTROLS.json.
- The corrected terminal state and the bounded next experiment
  (factory+0x84 assignment/object ONLY; outcome taxonomy recorded; no
  provenance-closure promise).

## Deviations (honest record)

- None in scope. The two authorized content changes (F-1 = P3-A,
  F-2 = W3) are the ONLY logical content deltas in the corrected CSVs —
  verified by the QC's logical-content diff, which re-derives the historical
  rows from the historical files with byte-accounting join round-trips.
- The historical S5 battery's own machine records already contained both
  correct P3 VAs (disclosed in S-8/S-9): the historical defects were the
  ledger row (P3-A) and prose documentation (P3-B), not the machine pins.

## Next experiment (DESIGN ONLY — NOT executed)

After this correction is independently accepted: WHO ASSIGNS factory+0x84
AND WHAT EXACT OBJECT/VALUE IS ASSIGNED THERE? Outcomes:
ASSIGNMENT_FOUND_AND_OBJECT_IDENTIFIED | ASSIGNMENT_FOUND_OBJECT_SOURCE_
UNRESOLVED | NO_ASSIGNMENT_FOUND_WITHIN_BOUND | MULTIPLE_CANDIDATES_
UNRESOLVED. Full backing provenance remains a separate later, separately
authorized question. NEXT_EXPERIMENT_EXECUTED = NO.

## Audit pointers

- Corrected terminal state: FINAL_REPORT.md.
- Gate-by-gate measured results: QC_REPORT.md + 01_RAW/QC_*.json.
- Supersessions: SUPERSESSION_LEDGER.md.
- Input identities (baseline/EXE/historical sources): INPUT_IDENTITIES.md.
- Repo state: BASE 4627d385...; publication = this package + one
  AUDIT_ENTRYPOINT.md row (path-limited; historical packages READ-ONLY).
