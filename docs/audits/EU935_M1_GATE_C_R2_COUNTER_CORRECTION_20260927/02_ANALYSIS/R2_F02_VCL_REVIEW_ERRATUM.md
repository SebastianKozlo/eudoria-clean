# R2-F02 — VCL REVIEW-ARITHMETIC ERRATUM RECORD

RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (02_ANALYSIS)
Desktop finding: R2-F02 (GATEC_REAUDIT_R2_REPORT_20260927 section 5, the
review-arithmetic erratum). Verdict: INDEPENDENTLY REPRODUCED.

## 1. OLD_STATEMENT

The human-pasted PE_MASTER_REVIEW relay carried the equation:

    491x12 + 24 + 252 = 5916

## 2. WHY_WRONG

The LHS is 491x12 + 24 + 252 = 5,892 + 24 + 252 = 6,168 — NOT 5,916. The
equation is arithmetically FALSE as stated (machine-recomputed; JSON:
03_EVIDENCE/R2_F02_VCL_ARITHMETIC.json).

## 3. CORRECT_ARITHMETIC (both machine-executed over the R1 census per_file rows)

- Re-derived sums (the totals block of the census JSON was NOT trusted; the
  per_file rows were re-summed): lines = 492; tokens = 5,916; groups = 493;
  success records = 472 (cross-checked against the census
  decoder_execution_log: 472). 25.vcl = 21 lines / 252 tokens / 21 groups
  (1 comma line + 20 numeric lines). Continuation extra groups = 1 (9.vcl:
  11 lines but 12 groups).
- GROUP-LEVEL relation: (491+1+1) x 12 = 5,916. Decomposition: 491 numeric
  lines (each contributing 1 group; the 9.vcl continuation line is ONE of the
  491 via its first 12 tokens — the comma line is the only float-failing row)
  + 1 continuation extra group (the continuation line's second 12 tokens) +
  1 comma group (25.vcl record 9's own group) = 493 groups; 493 x 12 = 5,916.
- RECORDS relation: 493 - 21 = 472 (the decoder returns one record per group
  for every file except 25.vcl, which THROWS — its 21 groups are excluded).
- FILE-LEVEL relation: 472 x 12 + 252 = 5,916 (the 472 success records' tokens
  plus ALL of 25.vcl's 252 tokens).
- numeric_rows_12cols = 491 verified from the predecessor
  03_EVIDENCE/F02_ITER032K_RERUN_vcl_columns.json (the comma line is the only
  excluded row; total_rows_alltokens = 492).

## 4. POPULATION_OVERLAP (the exact double-count decomposition)

6,168 - 5,916 = 252 = 240 + 12:

- 240 = 25.vcl's 20 numeric lines x 12 tokens — these 20 lines are ALREADY
  inside 491x12 (25.vcl's numeric lines are among the 491). The +252 term of
  the bad equation re-adds ALL 21 of 25.vcl's groups/lines, so only the comma
  group (12) is genuinely new; 240 is double-counted.
- 12 = the 9.vcl continuation line's FIRST group — the continuation line is
  ALREADY inside 491x12 (one of the 491 numeric rows). The +24 term of the bad
  equation re-adds BOTH of the continuation line's groups, so only the second
  group (12) is genuinely new; 12 is double-counted.

The overlapping populations: (a) 25.vcl's 20 numeric lines are a subset of the
491 numeric lines; (b) the continuation line's first group is a subset of the
491 numeric rows' groups.

## 5. AFFECTED_CLAIMS

The pasted-review arithmetic ONLY. Repo-wide search record: all 2,594 tracked
repo files (133,463,531 bytes) scanned for the variants "491x12 + 24 + 252",
"491*12 + 24 + 252", "491 × 12 + 24" plus a whitespace-flexible regex
(/491\s*[x*×]\s*12\s*\+\s*24/) — 0 HITS. Search timing: Phase 1 (pre-edit
worktree, 133,463,531 bytes; the R2 entrypoint row and this package's own
records did not yet exist); post-run, the equation string appears ONLY in
this run's own correction records — inside THIS package (its erratum,
self-check, blast-radius, report, raw/control and evidence records) and in
the new AUDIT_ENTRYPOINT.md R2 row — always quoted AS the corrected-false
OLD_STATEMENT; no repo file asserts it. The defect existed only in the
human-pasted chat relay, never in a repo file. No repo edit was required or
made for this edge (this package's erratum record + the entrypoint row are the
correction).

## 6. UNAFFECTED_CLAIMS

The raw census 32 files / 492 lines / 5,916 tokens / 493 groups / 6 bad
tokens / 31 successes / 1 THROW / 472 records and ALL R1 package contents are
UNCHANGED and valid. No payload was modified; the decoder was not touched;
comma behavior was not modified; NO original-client comma semantics were
inferred (TOKENIZATION_SEMANTICS / NUMERIC_CONVERSION / LOCALE /
COMMA_DECIMAL / FAILURE_HANDLING for the original client remain UNVERIFIED —
unchanged statuses).

## 7. BLAST_RADIUS

Zero: the bad equation never entered the repo (0/2,594 tracked files). The
erratum is documentation-only.
