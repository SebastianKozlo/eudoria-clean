# HANDOFF — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004

To: PE-MASTER. From: pe-reconstruction (bounded worker; NO_NESTED_TASKS).
This package is the human-ordered POINT CORRECTION of the R1 package
`PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004` (Desktop post-audit
verdict REQUIRE_CORRECTIONS_IN_REPORT_QC_HANDOFF_SCOPE — findings GP1, GP2,
GP3 and the FUNCTION_BUDGET_OVERRUN wording). The terminal sequence
(targeted QC → actual final report/ledger/handoff/entrypoint → manifest LAST
→ complete bijection → path-limited commit/push → remote verification) was
executed as required.

## One-paragraph result

The R1 science is PRESERVED unchanged (GETTER_RESULT_TO_LOOKUP_KEY =
PRESERVED_CONFIRMED; CLASS_SELECTOR_20006 = CONFIRMED; PROPERTY_TAG_6 =
CONFIRMED; the audited normal path tag6 → descriptor id 10 → per-receiver
value table[10] → current u32 → FUN_0072F880 key;
GETTER_RESULT_PROVENANCE = UNKNOWN;
PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED; C1/C2
preserved closed), and the four defective WORDINGS are corrected on my own
re-verified bytes: (GP1) the audited value's IMMEDIATE STORAGE is the
per-receiver component value table, but its ULTIMATE SOURCE is UNKNOWN — no
file/static source is excluded (FILE_DERIVED_VALUE_EXCLUDED = NO), and only
the DEFAULT creation path is established to initialize the audited int value
to 0 (FUN_009777E0 `MOV DWORD [EAX],0` re-verified); the nonzero producer and
its timing are UNRESOLVED — the universal after-creation claim is superseded.
(GP2) the 0xD82 alternative's FALSE sub-outcome BYPASSES the tag-6
getter/value-table segment but RETURNS to the SHARED caller FUN_004C5580,
which aborts on zero and otherwise uses the result as the SAME FUN_0072F880
lookup key (ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT;
FUN_00843340_RESULT_SEMANTIC = UNKNOWN — not a template object).
(GP3) both fallback statics (0x00BA5108, 0x00BA9374) read as ZEROS AT IMAGE
MAPPING (.data virtual tail) and the direct-literal census found NO store
forms — but lifetime immutability is NOT_ESTABLISHED (the census excludes
only literal/direct-address forms; both statics are returned as pointers, so
indirect writes are not excluded); zero→abort is CONFIRMED_CONDITIONAL.
(Budget) FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED — the R1 run's
authorized 20-function budget was violated at 28; the later stop did not
cure it; no result is upgraded by out-of-budget work; future contracts need
a hard pre-check BEFORE entering function N+1.

## What was superseded (23 ledger rows — SUPERSESSION_LEDGER.md)

- GP1_SOURCE_EXCLUSION_AND_CREATION_TIMING: rows S-GP1-1..S-GP1-5 — the
  external review's source-exclusion wording ("NOT from static data"; "NOT
  the static 16083 / not from RECORD_A") and the R1 published universal
  creation-timing claims (FINAL_REPORT.md:39-42,
  PRODUCER_PROVIDER_CHAIN.md:22-25, entrypoint row "later" wording).
- GP2_ALTERNATIVE_BRANCH_LOOKUP_BYPASS: rows S-GP2-1..S-GP2-4 —
  ALTERNATIVE_BRANCH.md:41-46 ("a DIFFERENT template source that NEVER
  consults ... FUN_0072F880") and :57-58 ("directly as the 'template
  object'"), HANDOFF.md:44-46 ("a different template source entirely"), the
  entrypoint row's incomplete flow wording.
- GP3_STATIC_FALLBACK_LIFETIME_IMMUTABILITY: rows S-GP3-1..S-GP3-9 — the
  lifetime-zero wording across FINAL_REPORT.md:90, GETTER_CHAIN.md:58-59 and
  75-76, ALTERNATIVE_BRANCH.md:62-68, CONTROL_CASE.md:40-44 and 49-55,
  HANDOFF.md:43, PROVENANCE_CHAIN.csv rows 31/41 (with their CONFIRMED
  status), and the entrypoint row.
- PROCESS_BUDGET: rows S-BUDGET-1..S-BUDGET-5 — FINAL_REPORT.md:164-165,
  QC_REPORT.md:94-96, HANDOFF.md:19-21 and 61-64, entrypoint row.
- Every ORIGINAL_EXCERPT was machine-verified as a real substring of its
  named source file at BASE_SHA 25335a2 (quotecheck 23/23) — no fabricated
  quote, no misattribution. No historical file was edited.

## What is preserved (no science reopened)

All the R1 canonical results listed above; the R1 byte evidence, raw S1-S11
records, scripts and manifest (READ-ONLY; the historical S11 PASS covers
pins/call targets, NOT lifetime immutability); CONTROL A and the narrowed
CONTROL C; sub-outcome-1 convergence; candidates A/B as unresolved leads;
all non-claims (WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED;
WORLD_XYZ_RECOVERED = NO; no model join, no position recovery).

## Machine verification of THIS package

- Byte battery 27/27 PASS (input identities 2, EXE identity 2, GP2 flow 11,
  GP3 statics/census 6, GP1 scoped pins 6) + forbidden-actions census all NO
  (no decode of FUN_0070DC20/FUN_00843340, no factory+0x84 trace, no RECORD_A
  analysis, no templates.vfs access, no alias-closure search, no placement
  science, no client launch) — 01_RAW/QC_CORRECTION_BATTERY.json.
- Ledger quotecheck 23/23 PASS — 01_RAW/QC_LEDGER_QUOTE_CHECKS.json.
- Doc gates PASS (required corrected strings present; forbidden superseded
  wording absent from the ACTIVE docs) — 01_RAW/QC_DOC_GATES.json.
- Targeted correction QC: Q1-Q8 all PASS — QC_REPORT.md
  (QC_SCOPE = SELF_CHECK_GETTER_PROVENANCE_REPORT_SCOPE_CORRECTION).

## Next experiment (unchanged recommendation — NOT executed)

The narrowest next science experiment remains the one designed by R1 and
echoed by the Desktop audit: decode FUN_0070DC20 (the record-apply candidate
writer of value-table entry 10) + FUN_00971650 + identify the factory+0x84
stream setter — resolving GETTER_RESULT_PRODUCER. It is NOT executed by this
correction (NEXT_EXPERIMENT_EXECUTED = NO) and requires separate human
authorization. Per this run's contract: HARD STOP — do NOT execute the
FUN_0070DC20 experiment.

## Deviations (honest record)

- One in-run battery fix: the E4 check width was corrected from 8 to the
  published 9-byte pin (`50 6A 00 6A 00 6A 01 6A 06`); the first run's FAIL
  and the fix are recorded in INPUT_IDENTITIES.md. No other deviation; no
  document written after the manifest; foreign untracked paths untouched.

## Audit pointers

- Verdict terminal fields: FINAL_REPORT.md.
- Supersession record: SUPERSESSION_LEDGER.md (23 rows).
- Raw machine records: 01_RAW/QC_CORRECTION_BATTERY.json,
  01_RAW/QC_LEDGER_QUOTE_CHECKS.json, 01_RAW/QC_DOC_GATES.json.
- Instruments: 03_SCRIPTS/qc_correction_c1.py (modes: bytes | docgates |
  quotecheck).
- Repo state: BASE 25335a28...; publication = this package + ONE new
  AUDIT_ENTRYPOINT.md row (path-limited; historical packages and the
  historical entrypoint rows READ-ONLY).

RUN_STATUS = COMPLETED (correction scope; GP1/GP2/GP3 = CORRECTED;
FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED; QC 8/8 PASS).
