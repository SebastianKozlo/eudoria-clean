# SUPERSESSION_LEDGER — PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004

Scope: corrections of the historical package
docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004 (published at
BASE 4627d385) per the independent Desktop post-audit findings W1/W2/W3
and the P3 hygiene. Historical files are READ-ONLY and are NOT edited; every
supersession lives in THIS package. Every ORIGINAL_EXCERPT / OLD_LOGICAL_
CONTENT below is machine-verified by the QC (AUX quotecheck,
01_RAW/QC_VALUE_SCOPE.json) to be a real substring of its named SOURCE_FILE
at the BASE commit; NEW_LOGICAL_CONTENT values are verified present in the
corrected CSVs.

### S-1: historical S5 Q10 hard-coded function count (never derived from the ledger)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/03_SCRIPTS/s5_qc_battery.py`
- SOURCE_FIELD_OR_EXCERPT: Q10_function_budget result dict, literal NEW_FUNCTION_COUNT
- ORIGINAL_EXCERPT: `"NEW_FUNCTION_COUNT": 7,`
- OLD_CLAIM: the S5 machine record emitted NEW_FUNCTION_COUNT as the hard-coded literal 7 with FUNCTION_BUDGET_PRECHECK = PASS if 7 <= 8; it never parsed FUNCTION_LEDGER.csv, and its value contradicts the historical FINAL_REPORT's own stated count of 8.
- NEW_CLAIM: the corrected gate (this package, Q5 in 03_SCRIPTS/qc_table10_writer_c1.py) parses CORRECTED_FUNCTION_LEDGER.csv FROM DISK and DERIVES LEDGER_DECLARED_COUNT (measured 8) from the final count_after column; no count literal exists in the corrected validator.
- STATUS: SUPERSEDED
- WHY: a hard-coded literal is not a measurement of the ledger; the 7-vs-8 internal inconsistency was undetectable by the historical gate.
- BLAST_RADIUS: the historical S5 Q10 record (01_RAW/S5_QC_BATTERY.json) and the Q10 gate text; the underlying 8-function decode evidence itself is untouched (its per-function pins stand as historical physical evidence).

### S-2: historical Q10 gate claim of ledger-validated pre-check discipline

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/QC_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: gate Q10 body
- ORIGINAL_EXCERPT: `FUNCTION_LEDGER.csv complete: 8 entries, each with count_before recorded`
- OLD_CLAIM: the historical QC_REPORT Q10 PASS asserted the ledger was complete and that each entry's count_before was recorded before its detailed analysis, implying the gate had machine-validated the ledger and the execution-time pre-check discipline.
- NEW_CLAIM: the corrected validator proves only the LEDGER-DECLARED facts: LEDGER_DECLARED_SEQUENCE_VALID (measured), LEDGER_DECLARED_COUNT (measured 8), LEDGER_DECLARED_WITHIN_BUDGET (measured). EXECUTION_TIMING_PRECHECK_INDEPENDENTLY_ESTABLISHED = NO — no independent chronological evidence exists that the executor physically performed each pre-check before each analysis, and a post-hoc static validator cannot manufacture it.
- STATUS: SUPERSEDED
- WHY: the historical gate validated nothing about the ledger (see S-1) and a static validator cannot establish chronological discipline.
- BLAST_RADIUS: the historical Q10 verdict wording and any statement that S5 machine-proved the pre-check timing; NOT the ledger's declared content itself (which the corrected validator now genuinely measures), NOT the historical run's actual decode work.

### S-3: historical "12/12 gates PASS" rollup insofar as Q10 was not a real ledger-derived gate

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/QC_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: QC_RESULT terminal line
- ORIGINAL_EXCERPT: `QC_RESULT = PASS (92/92 machine pins; 12/12 gates PASS; self-check scope).`
- OLD_CLAIM: 12/12 QC gates meaningful and PASS.
- NEW_CLAIM: the 92/92 machine pin checks remain valid historical physical evidence; the Q10 gate was a hard-coded PASS (S-1), so the "12/12 meaningful gates" rollup is superseded for Q10's part (11 pin-evidence gates stand). The corrected targeted QC battery for the correction package is Q1-Q14 + AUX (03_SCRIPTS/qc_table10_writer_c1.py).
- STATUS: SUPERSEDED
- WHY: a rollup counting a non-validating gate overstates the QC coverage.
- BLAST_RADIUS: the rollup line in QC_REPORT.md and the matching HANDOFF sentence; no physical pin evidence affected.

### S-4: historical machine-readable status of FUNCTION_LEDGER.csv as valid CSV

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/HANDOFF.md`
- SOURCE_FIELD_OR_EXCERPT: "Function budget" audit pointer
- ORIGINAL_EXCERPT: `Function budget: FUNCTION_LEDGER.csv (8 entries, pre-checks recorded).`
- OLD_CLAIM: FUNCTION_LEDGER.csv was treated as a complete, machine-usable record (implicitly valid CSV).
- NEW_CLAIM: the historical FUNCTION_LEDGER.csv is NOT valid strict CSV (measured: 7-column header, 8 data rows, 5 malformed-width rows — unquoted embedded commas); its LOGICAL 8-row content is preserved unchanged in CORRECTED_FUNCTION_LEDGER.csv (strict csv serialization; measured CORRECTED_VALID) except the authorized F-1 change.
- STATUS: SUPERSEDED (machine-readable status); logical content PRESERVED.
- WHY: any standard CSV parser mis-splits 5 of 8 rows; downstream machine consumption of the historical file is unreliable.
- BLAST_RADIUS: machine consumers of the historical CSV; the human-readable logical content (and its evidence role) is unaffected and now also available in corrected serialized form.

### S-5: historical machine-readable status of WRITER_CHAIN.csv as valid CSV

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FINAL_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: Evidence index listing
- ORIGINAL_EXCERPT: `WRITER_CHAIN.csv, HANDOFF.md.`
- OLD_CLAIM: WRITER_CHAIN.csv was published as a package evidence artifact (implicitly machine-usable).
- NEW_CLAIM: the historical WRITER_CHAIN.csv is NOT valid strict CSV (measured: 6-column header, 26 data rows, 22 malformed-width rows); its LOGICAL 26-row content is preserved unchanged in CORRECTED_WRITER_CHAIN.csv (strict csv serialization; measured CORRECTED_VALID) except the authorized F-2 change.
- STATUS: SUPERSEDED (machine-readable status); logical content PRESERVED (except F-2).
- WHY: same serialization defect class as S-4; 22 of 26 rows mis-split under a standard parser.
- BLAST_RADIUS: machine consumers of the historical CSV; the writer-chain evidence itself (byte pins per row) is unaffected.

### S-6: historical WRITER_CHAIN row-26 getter-value wording

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/WRITER_CHAIN.csv`
- SOURCE_FIELD_OR_EXCERPT: step 26, structural_identity field
- ORIGINAL_EXCERPT: `the audited getter reads table[10] = the value WRITTEN at step 20`
- OLD_CLAIM: the audited getter reads table[10] AS the value written at step 20 of the same chain — an unqualified identity between the step-20 write and the getter's read.
- NEW_CLAIM: the audited getter reads the CURRENT value of table[10] of the SAME storage entry the audited writer mechanism can write; storage identity is CONFIRMED_STATIC_CONDITIONAL; whether the value written by a particular apply event persists unchanged until this getter event is NOT_ESTABLISHED by the static run (SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED; WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED; NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED; RUNTIME_EVENT_ORDER = NOT_ESTABLISHED; RUNTIME_CACHE_BINDING_AT_SPECIFIC_GETTER_EVENT = NOT_OBSERVED).
- STATUS: SUPERSEDED (corrected in CORRECTED_WRITER_CHAIN.csv row 26 = record F-2; historical file untouched)
- WHY: a static mechanism run cannot establish that the value written by one apply event remains unchanged until a later getter event: no runtime observation exists, and published-but-undecoded clobber-capable surfaces exist (class_obj->vtable[3] typed blob reader @0x00726A9D; factory delegate->vtable[9] notify @0x0070DCAB; delegate->vtable[10] @0x0070DCC8; the second caller's re-apply of records to cached components @0x00704704).
- BLAST_RADIUS: the row-26 wording and the same interpretation of the getter-producer statement (S-7); the writer mechanism, the storage identity chain, and all byte pins are unaffected.

### S-7: historical getter-producer key read as provenance of a specific later runtime getter value

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FINAL_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: Success level section
- ORIGINAL_EXCERPT: `GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL`
- OLD_CLAIM: the immediate producer of the value the audited getter returns is confirmed — when read as the provenance of the SPECIFIC runtime value returned by a later getter event, this claims more than the static evidence supports.
- NEW_CLAIM: scoped to the writer-mechanism/storage-identity level only: WRITER_MECHANISM = CONFIRMED_STATIC_CONDITIONAL; ATTRIBUTE10_WRITER_MECHANISM = CONFIRMED; SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL; the writer mechanism CAN write record value data into the table[10] storage entry the getter addresses, and the getter reads the CURRENT value of that entry; SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED (which u32 the getter returns at any particular runtime event is not statically established).
- STATUS: SUPERSEDED (interpretation narrowed; the writer identification itself is PRESERVED science)
- WHY: same epistemic boundary as S-6; the historical statement was ambiguous and, in its unconditional reading, unsupported.
- BLAST_RADIUS: the historical FINAL_REPORT/HANDOFF success-level wording; NOT the writer-function/VA identification (preserved: FUN_009777F0 @0x00977810).

### S-8: historical fail-path zero-store VA (P3-A)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FUNCTION_LEDGER.csv`
- SOURCE_FIELD_OR_EXCERPT: ordinal 7 (FUN_009777F0), reason_entered field
- ORIGINAL_EXCERPT: `(fail-path zero store @0x0097781A + advance-by-4 call)`
- OLD_CLAIM: the fail-path zero store is at VA 0x0097781A.
- NEW_CLAIM: FAILPATH_ZERO_STORE_VA = 0x0097781E (byte re-read this run from the pinned EXE: C7 00 00 00 00 00 at 0x0097781E; the superseded VA is NOT the C7 store start; the historical S5 machine pin was already 0x0097781E and the historical QC_REPORT Q6 already stated 0x0097781E — the defect existed only in the ledger row). Corrected in CORRECTED_FUNCTION_LEDGER.csv row 7 (record F-1).
- STATUS: SUPERSEDED
- WHY: VA hygiene — 0x0097781A is not the C7 zero store; PE-MASTER byte-verified and re-verified by this run's Q10.
- BLAST_RADIUS: the historical ledger row's documentation only; no verdict depended on the wrong VA.

### S-9: historical component-vtable-store VA (P3-B)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/QC_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: gate Q4 creation path line (the same wrong VA also appears in the historical INPUT_IDENTITIES.md, ATTRIBUTE10_WRITE_CHAIN.md and SAME_COMPONENT_IDENTITY.md prose)
- ORIGINAL_EXCERPT: `store 0x00A86F2C @0x007374DC; factory->class_obj+4 @0x0070D9A5; 12-entry`
- OLD_CLAIM: the component-ctor vtable store instruction is at VA 0x007374DC.
- NEW_CLAIM: COMPONENT_VTABLE_STORE_VA = 0x007374D6 — the C7 06 2C 6F A8 00 store starts at 0x007374D6 (byte re-read this run); the superseded prose VA measures 8B C6 = mid-stream operand bytes, NOT a C7 store start. The historical S5 machine pin was already 0x007374D6 (disclosed: the defect was prose-only). Component-vtable identity (0x00A86F2C) unchanged; corrected in this package's active documentation.
- STATUS: SUPERSEDED
- WHY: VA hygiene — the historical prose pointed at mid-instruction bytes; PE-MASTER byte-verified and re-verified by this run's Q11.
- BLAST_RADIUS: historical prose documentation (QC_REPORT Q4 line, INPUT_IDENTITIES, ATTRIBUTE10_WRITE_CHAIN, SAME_COMPONENT_IDENTITY); no machine pin and no verdict affected.

### S-10: historical one-run provenance-closure promise (P3-C)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FINAL_REPORT.md`
- SOURCE_FIELD_OR_EXCERPT: FIRST_MISSING_EDGE / next-experiment section (the same promise appears in the historical HANDOFF next-experiment section)
- ORIGINAL_EXCERPT: `convert ULTIMATE_VALUE_SOURCE from UNKNOWN to a physical/message class or`
- OLD_CLAIM: the single bounded factory+0x84 stream-setter experiment would close the ULTIMATE_VALUE_SOURCE provenance edge (physical/message class or controlled rejection).
- NEW_CLAIM: the next experiment asks ONLY: WHO ASSIGNS factory+0x84 AND WHAT EXACT OBJECT/VALUE IS ASSIGNED THERE? Outcome taxonomy: ASSIGNMENT_FOUND_AND_OBJECT_IDENTIFIED | ASSIGNMENT_FOUND_OBJECT_SOURCE_UNRESOLVED | NO_ASSIGNMENT_FOUND_WITHIN_BOUND | MULTIPLE_CANDIDATES_UNRESOLVED. Full backing provenance (file/network/cache/embedded source class) is a LATER separately authorized question; no source-class closure is promised by that future run. Do not prejudge.
- STATUS: SUPERSEDED
- WHY: one bounded assignment-site experiment cannot promise full value-source provenance closure; the wording overstated the deliverable.
- BLAST_RADIUS: next-experiment planning wording only; no completed science affected.

### F-1: authorized corrected-ledger field change (P3-A)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FUNCTION_LEDGER.csv`
- ROW_ID/ORDINAL: 7 (FUN_009777F0)
- FIELD_NAME: reason_entered
- OLD_LOGICAL_CONTENT: `canon function (20002_PAYLOAD30) - COUNTED conservatively because this run derived NEW semantics beyond the reverified canon pins (fail-path zero store @0x0097781A + advance-by-4 call)`
- NEW_LOGICAL_CONTENT: `canon function (20002_PAYLOAD30) - COUNTED conservatively because this run derived NEW semantics beyond the reverified canon pins (fail-path zero store @0x0097781E + advance-by-4 call)`
- AUTHORIZED_REASON: P3
- OLD_CLAIM: the row's reason field cited the fail-path zero store at the superseded VA (record S-8).
- NEW_CLAIM: the corrected row cites FAILPATH_ZERO_STORE_VA = 0x0097781E.
- STATUS: APPLIED (AUTHORIZED)
- WHY: P3-A VA hygiene correction; the only semantic delta is the VA inside the reason text.
- BLAST_RADIUS: CORRECTED_FUNCTION_LEDGER.csv row 7 only; all other 7 rows byte-preserved logically; verified by QC gate Q3 (diffs == exactly this one authorized change).

### F-2: authorized corrected-chain field change (W3)

- SOURCE_FILE: `docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/WRITER_CHAIN.csv`
- ROW_ID/ORDINAL: 26 (getter side, canon re-pinned)
- FIELD_NAME: structural_identity
- OLD_LOGICAL_CONTENT: `the audited getter reads table[10] = the value WRITTEN at step 20`
- NEW_LOGICAL_CONTENT: `the audited getter reads the CURRENT value of table[10] of the SAME storage entry the audited writer mechanism can write (storage identity CONFIRMED_STATIC_CONDITIONAL; whether the value written by a particular apply event persists unchanged until this getter event is NOT_ESTABLISHED by this static run)`
- AUTHORIZED_REASON: W3
- OLD_CLAIM: the unqualified write-to-read value identity (record S-6).
- NEW_CLAIM: the storage-identity-scoped wording (SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL; preservation NOT_ESTABLISHED).
- STATUS: APPLIED (AUTHORIZED)
- WHY: W3 claim-scope correction; the only semantic delta in the chain CSV.
- BLAST_RADIUS: CORRECTED_WRITER_CHAIN.csv row 26 only; all other 25 rows byte-preserved logically; verified by QC gate Q4 (diffs == exactly this one authorized change).
