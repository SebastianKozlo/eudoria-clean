# FINAL_REPORT — PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004

RUN_ID: PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004
RUN_CLASS: LOAD_BEARING | RUN_TYPE: DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
(REPORT/CSV/QC/CLAIM-SCOPE CORRECTION ONLY — NO new reverse engineering) |
MODE: STATIC-ONLY (the client never ran; the only EXE byte reads in this run
are the two P3 VA-correction pin windows + the two superseded-VA probe
windows, all inside 03_SCRIPTS/qc_table10_writer_c1.py) | Executor:
pe-reconstruction (PE-MASTER bounded worker contract; NO_NESTED_TASKS;
publication authorized in-contract).

## MISSION AND OUTCOME

This package corrects EXACTLY the three P2 findings of the independent
Desktop post-audit of 4627d38 (the historical package
PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004) plus the P3 VA hygiene,
while PRESERVING the physically confirmed core writer science. No new
science was performed or is claimed: no callback decode, no factory+0x84
trace, no source-stream trace, no templates.vfs access, no RECORD_A
analysis, no Model 194013 trace, no world placement/XYZ, no model join, no
NIF work, no client execution.

- W1 (function-budget QC): corrected. The historical S5 validator hard-coded
  NEW_FUNCTION_COUNT as a literal 7 (also inconsistent with the historical
  report's own 8) and never parsed FUNCTION_LEDGER.csv; that gate is
  SUPERSEDED. The corrected Q5 parses CORRECTED_FUNCTION_LEDGER.csv FROM
  DISK and DERIVES LEDGER_DECLARED_COUNT (measured 8) with the three
  SEPARATE predicates (LEDGER_STRUCTURE_STATUS / EXPECTED_CANONICAL_
  ROW_COUNT_STATUS / BUDGET_LIMIT_CHECK) and the epistemic scope boundary:
  the validator proves the LEDGER-DECLARED sequence/count/budget only; it
  does NOT independently establish the chronological pre-check discipline
  of the historical executor (EXECUTION_TIMING_PRECHECK_INDEPENDENTLY_
  ESTABLISHED = NO).
- W2 (strict CSV serialization): corrected. The historical
  FUNCTION_LEDGER.csv (8 data rows, 5 malformed-width rows measured) and
  WRITER_CHAIN.csv (26 data rows, 22 malformed-width rows measured) were
  not valid strict CSV. CORRECTED_FUNCTION_LEDGER.csv and
  CORRECTED_WRITER_CHAIN.csv are written with Python csv.writer
  (encoding="utf-8", newline="", LF line terminator) and preserve ALL
  logical field contents EXCEPT the two authorized changes (F-1 = P3-A,
  F-2 = W3), each recorded in SUPERSESSION_LEDGER.md. The QC re-derives the
  logical content from the historical files (byte-accounting join
  round-trips) and verifies the corrected CSVs differ by EXACTLY the
  authorized changes.
- W3 (storage identity vs specific value provenance): corrected. The
  writer mechanism remains CONFIRMED at the static-conditional mechanism
  level; the getter structurally addresses the SAME storage entry through
  the same factory/receiver/cache discipline. The corrected taxonomy does
  NOT claim that a particular u32 written during one apply event remains
  unchanged until a later getter event: SPECIFIC_RUNTIME_GETTER_VALUE_
  PRODUCER = UNVERIFIED; WRITE_TO_LATER_GETTER_VALUE_PRESERVATION =
  NOT_ESTABLISHED; NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED.
- P3-A: the historical FUNCTION_LEDGER row 7 fail-path zero-store VA is
  corrected to FAILPATH_ZERO_STORE_VA = 0x0097781E (bytes C7 00 00 00 00
  00 re-read from the pinned EXE this run; the superseded VA is NOT the C7
  store start; the historical S5 machine pin was already 0x0097781E — the
  defect was the ledger row only; record S-7 / F-1).
- P3-B: the historical prose component-vtable-store VA is corrected to
  COMPONENT_VTABLE_STORE_VA = 0x007374D6 (the C7 06 2C 6F A8 00 store
  instruction starts there; the superseded prose VA measures 8B C6 =
  mid-stream operand bytes, NOT a C7 store start; the historical S5
  machine pin was already 0x007374D6 — the defect was prose-only; record
  S-8). The component-vtable identity (0x00A86F2C) is unchanged.
- P3-C: the next-experiment wording is narrowed (record S-9) — see the
  section below; no one-run provenance-closure promise.

## THE PRESERVED SCIENCE (unchanged, from the physically confirmed base)

The audited writer mechanism: record cursor -> tag u16 @0x007269E7 ->
schema descriptor (FUN_0070C180; slot->id = tag+4 via 83 C1 04
@0x0070CBF6 in the SLOT_ADD writer) -> tag 6 / id 10 ->
[class_obj+0x40]+10*4 -> traits dispatch FUN_0075F660 (vtable slot 5 =
FUN_009777F0, dword @0x00A9C684) -> MOV [EDX],EAX 89 02 @0x00977810
(value READ 8B 04 10 @0x00977807 from the record cursor). WRITER_FUNCTION =
FUN_009777F0; WRITER_VA = 0x00977810; TAG6_TO_ID10 = CONFIRMED. The
component insert (receiver -> class_obj into the factory+0x0C cache map,
FUN_0092B660 @0x0070DC7C) and the getter-side lookup of the SAME map
(FUN_0070E100 -> FUN_004D1430 -> node+0x14 @0x0070E131; audited getter
chain @0x004C5523..0x004C554E) establish the SAME storage identity.

## W3 CORRECTED SCOPE STATEMENT (the exact corrected wording)

The audited writer mechanism can write record value data into table[10] of
the same structural component/cache identity later addressed by the getter.
The getter reads the CURRENT value of that entry. This static run does not
establish that the exact value written by a particular apply event remains
unchanged until any particular later getter event.

Supporting scope facts (already-published, undecoded clobber-capable
surfaces whose existence alone sustains the NOT_ESTABLISHED states without
any new decode): the mode-1 typed blob reader (class_obj->vtable[3]
@0x00726A9D), the delegate notify (factory delegate->vtable[9]
@0x0070DCAB) and release (delegate->vtable[10] @0x0070DCC8), and the
second caller's re-apply of records to already-cached components
(@0x00704704 context) are published shells whose bodies were NOT decoded
in the historical run and are NOT decoded here.

## NEXT EXPERIMENT (DESIGN ONLY — NOT EXECUTED; narrowed per P3-C)

NEXT_EXPERIMENT_EXECUTED = NO. After this correction is independently
accepted, the next science question is ONLY: WHO ASSIGNS factory+0x84 AND
WHAT EXACT OBJECT/VALUE IS ASSIGNED THERE? This is NOT combined with full
backing-source provenance, templates.vfs, Model 194013, world placement or
XYZ. The single bounded experiment asks only for the assignment site(s) and
the exact object/value identity assigned at factory+0x84. Do not prejudge
the outcome; the possible outcomes are:

- ASSIGNMENT_FOUND_AND_OBJECT_IDENTIFIED
- ASSIGNMENT_FOUND_OBJECT_SOURCE_UNRESOLVED
- NO_ASSIGNMENT_FOUND_WITHIN_BOUND
- MULTIPLE_CANDIDATES_UNRESOLVED

If the assignment/object identity is established, full backing provenance
(physical file / network / cache / embedded) remains a separate later
question, to be separately authorized, unless it falls out directly from
the assignment decode without additional RE. No source-class closure is
promised by that future run.

## CORRECTED TERMINAL STATE

All values below are MEASURED by 03_SCRIPTS/qc_table10_writer_c1.py
(01_RAW/QC_*.json), not pre-filled; they are valid only because the
corresponding QC measurements succeeded at execution time.

```text
--- TERMINAL_STATE_BEGIN ---
BASE_SHA = 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5
CORE_WRITER_VERDICT = ACCEPTED_IN_STATIC_CONDITIONAL_MECHANISM_SCOPE
WRITER_MECHANISM = CONFIRMED_STATIC_CONDITIONAL
ATTRIBUTE10_WRITER_MECHANISM = CONFIRMED
WRITER_FUNCTION = FUN_009777F0
WRITER_VA = 0x00977810
TAG6_TO_ID10 = CONFIRMED
SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED
WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED
NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED
RUNTIME_EVENT_ORDER = NOT_ESTABLISHED
RUNTIME_CACHE_BINDING_AT_SPECIFIC_GETTER_EVENT = NOT_OBSERVED
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
ULTIMATE_VALUE_SOURCE = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED = NO
RECORD_A_RELATION = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
FAILPATH_ZERO_STORE_VA = 0x0097781E
COMPONENT_VTABLE_STORE_VA = 0x007374D6
FUNCTION_LEDGER_CSV = CORRECTED_VALID
WRITER_CHAIN_CSV = CORRECTED_VALID
LEDGER_DECLARED_COUNT = 8
LEDGER_DECLARED_SEQUENCE_VALID = YES
LEDGER_DECLARED_WITHIN_BUDGET = YES
FUNCTION_BUDGET_LEDGER_VALIDATION = PASS
EXECUTION_TIMING_PRECHECK_INDEPENDENTLY_ESTABLISHED = NO
NINE_ROW_MUTANT_STRUCTURE_STATUS = PASS
NINE_ROW_MUTANT_NEW_FUNCTION_COUNT = 9
NINE_ROW_MUTANT_BUDGET_LIMIT_CHECK = FAIL
HISTORICAL_Q10_HARDCODE_DEFECT = SUPERSEDED
PACKAGE_CORRECTION_STATUS = CORRECTED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_EXECUTED = NO
NEW_RE_EXECUTED = NO
--- TERMINAL_STATE_END ---
```

Measured derivation notes (each verified by the QC gates):
- FUNCTION_LEDGER_CSV / WRITER_CHAIN_CSV: strict-CSV battery (csv.reader
  parse, exact header widths 7/6, 8/26 data rows, zero width mismatches,
  DictReader no None-key/no missing fields, ordinal/step uniqueness, UTF-8
  round trip, write->read->write round trip) + logical-content preservation
  vs the historical files with EXACTLY the two authorized field changes.
- LEDGER_DECLARED_COUNT = 8: DERIVED from the parsed corrected ledger
  (final count_after; ordinals 1..8; count_before 0..7; count_after 1..8;
  per-row count_after == count_before+1; every count_before < 8). The
  historical S5 hard-coded literal is superseded (record S-1).
- NINE_ROW_* : the private synthetic 9-row mutant (canonical rows + one
  synthetic 9th entry) is structurally VALID (LEDGER_STRUCTURE_STATUS =
  PASS, VALID_CSV = YES, unique functions, ordinals 1..9, coherent
  counts) and fails SPECIFICALLY on the budget: derived count 9 > MAX 8
  (BUDGET_LIMIT_CHECK = FAIL, FUNCTION_BUDGET_PRECHECK = FAIL). The
  canonical-row-count mismatch (9 vs 8) is reported as a SEPARATE
  predicate and is NOT the budget failure's cause.
- PACKAGE_CORRECTION_STATUS = CORRECTED holds only because ALL load-bearing
  QC gates succeeded (see QC_REPORT.md); on any load-bearing failure the
  honest value is PARTIAL with the measured failure recorded.

## W1 EPISTEMIC SCOPE (function-budget)

The corrected static validator proves: LEDGER_DECLARED_SEQUENCE_VALID
(measured), LEDGER_DECLARED_COUNT (measured 8), LEDGER_DECLARED_WITHIN_
BUDGET (measured). It MUST NOT and DOES NOT claim that a post-hoc static
validator independently proves the chronological fact that the historical
executor physically performed each pre-check before beginning each
analysis. No independent chronological evidence for that exists in this
run; the historical S5 statement that its own gate established the
execution-time pre-check discipline is SUPERSEDED (records S-1, S-2).

## SUPERSESSION SUMMARY (full ledger: SUPERSESSION_LEDGER.md)

11 records: S-1 historical Q10 hard-code/ledger claim; S-2 12/12
meaningful-gates claim; S-3 historical FUNCTION_LEDGER.csv machine-readable
validity; S-4 historical WRITER_CHAIN.csv machine-readable validity; S-5
the historical WRITER_CHAIN row-26 getter-value wording; S-6 the historical
getter-producer key when read as specific-value provenance; S-7 the
fail-path zero-store VA; S-8 the component-vtable-store VA; S-9 the
one-run provenance-closure promise; F-1 the authorized ledger field change
(P3-A); F-2 the authorized chain field change (W3). Every ORIGINAL_EXCERPT
is machine-verified a real substring of its named source file at BASE
4627d38 (quotecheck in 01_RAW/QC_VALUE_SCOPE.json).

## Historical evidence standing

The historical package remains READ-ONLY and its physical byte evidence
(01_RAW/S1..S5 pins, 92 machine pin checks) stands as historical physical
evidence. This correction does not rerun S1-S5 and does not replace their
records; it supersedes the Q10 gate LOGIC (hard-code defect), the CSV
machine-readable status, the row-26 wording, the two P3 VAs, and the
overconfident next-experiment wording. The historical core writer verdict
is preserved in the static-conditional mechanism scope stated above.

## PERSISTENCE

Before the first canonical write: output root verified non-existent, then
created fresh; git fetch; local HEAD == local origin/master == actual
remote master == 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 (rev-parse +
ls-remote; recorded in INPUT_IDENTITIES.md); foreign untracked paths
untouched. Immediately before commit: actual remote master re-verified ==
4627d385 (else BASE_DIVERGENCE, no push, HARD STOP). Path-limited staging
of exactly this package + one new AUDIT_ENTRYPOINT.md row; no `git add .`;
no force push; historical packages READ-ONLY.
COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST (self-excluded;
scope = all physical files of this package + the updated AUDIT_ENTRYPOINT.md;
bijection verified: no missing/extra/duplicate, all sizes and SHA256 match).
After push: local HEAD == origin/master after fetch == actual remote
master, all identical.

## HONEST BOUNDARIES

1. STATIC-ONLY: no runtime observation; the corrected taxonomy explicitly
   does not establish runtime event order, cache binding at any specific
   getter event, or value preservation between a write event and a later
   read event.
2. This correction changes REPORTING, CSV SERIALIZATION, QC LOGIC and VA
   HYGIENE only. No byte-level scientific claim of the historical run is
   upgraded or downgraded beyond the wording scoping recorded in
   SUPERSESSION_LEDGER.md; the writer mechanism science is preserved.
3. The 9-row mutant is a PRIVATE synthetic negative control; it is never
   committed as a canonical artifact (only its measured validation metadata
   is recorded in 01_RAW/QC_NEGATIVE_CONTROLS.json).
4. All PASS/CORRECTED_VALID terminal values are TARGET OUTCOMES that hold
   only because the corresponding QC measurement succeeded; none is a
   constant. On failure the measured result is reported (INVALID /
   NOT_VERIFIED / FAIL / PARTIAL) and never coerced.
