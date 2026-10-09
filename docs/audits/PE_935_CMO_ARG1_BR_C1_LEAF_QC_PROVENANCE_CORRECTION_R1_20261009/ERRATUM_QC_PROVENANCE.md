# ERRATUM_QC_PROVENANCE — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

Subject: the QC-coverage provenance overstatement identified by the
independent Desktop post-audit of commit a7b1dc0317af6a33b185481cd9559160188cfb24
as **BR-C1-R2 / OPEN_P2**, and its corrected evidence bound. Records-only
correction: this erratum changes NO historical file, NO historical final
answer and NO science; it corrects a claim about what the earlier
fresh-context internal QC actually re-executed.

## 1. The measured source (read DIRECTLY, not from summaries)

The original later fresh-QC record
`C:\Users\User\Documents\ChatGPT\PE\PE_CMO_BR_C1_DESKTOP_POST_AUDIT_A7B1DC0_20261009\QC_RECORD_FRESH_CONTEXT_INTERNAL_QC_20261009.md`
(19614 B / SHA256 `0C6B691294438D5FBCF8CB411FFAEC632816D16F4674E32C12982944AB3A1F48`,
re-hashed MATCH this run) was read IN FULL and its coverage was measured by
evidence type:

```text
QC_PERFORMER  = pe-master-auditor worker session (model nask-glm/glm-5-3),
                a DISTINCT FRESH reviewer; explicitly NOT the independent
                Desktop post-audit and NOT executor self-review
QC_DATE_UTC   = 2026-10-09 (after the a7b1dc0 commit at 14:01:51 UTC)
AUDITED_STATE = commit a7b1dc0317af6a33b185481cd9559160188cfb24 at BASE
                2ac7cfa1dcb2e53e9c86985c18377de811d5b485
VERDICT       = PASS (0 x P0, 0 x P1, 0 x P2, 4 x P3 residuals)
```

## 2. Measured coverage by evidence type (from the record itself)

Contract section 4's EXPECTATION table was verified against the direct
record. **MATCH — the direct record agrees with the expectations; the
expectations were not copied in place of the measurement:**

```text
ORIGINAL_FRESH_QC_REEXECUTED:
  fixed          = 14 outcomes   (record section 2: "14/14 identical verdicts
                                   + identical failing-predicate sets (my
                                   own driver, contract-built mutations)";
                                   CLEAN final "PASS 50/50 both
                                   (re-executed)"; AC1_AC2 "4/4
                                   (re-executed)"; BR1_BR4 "8/8
                                   (re-executed)")
  additional    = 9 cases / 18 outcomes  (record section 2: "9/9 selected
                                   re-executed (SF-C1-2, SF-C1-3, SF-C2-9,
                                   SF-C3-9, SF-C4-5, TYPE-1, TYPE-5, MISS-2,
                                   MALF-1) — identical outcomes +
                                   diagnostics")
  byte_regression= 24 outcomes    (record section 2: "24/24 re-executed;
                                   M5/M7 arg1-retention verified live on
                                   BOTH sides")
  TOTAL re-executed = 14 + 18 + 24 = 56 outcomes

ORIGINAL_FRESH_QC_MACHINE_PARSED:
  additional     = all 43 cases / 86 outcomes ("machine parse of all 43
                   records"; all recomputed from raw rows, never from the
                   handoff prose), INCLUDING the 68 outcomes not
                   documented as re-executed there
  coverage       = 34-row FIELD_CHECK_COVERAGE machine cross-check
                   (0 violations; 32 field rows <-> 32 unique SF cases)

DESKTOP_POST_AUDIT_REEXECUTED (a7b1dc0 post-audit, independent of the fresh
QC): fixed = 14; additional = 86; byte_regression = 24 (its own REPORT.md
section 2, plus its own 145-case/290-outcome construction and a helper-free
minimal second pass). This evidence is INDEPENDENTLY ATTRIBUTABLE TO THE
DESKTOP audit and is NOT credited retroactively to the earlier fresh QC.

NEW_CORRECTION_QC_REEXECUTED = measured separately by the fresh-context QC
of THIS new package (PENDING at executor stage; not fabricated here).
```

## 3. The overstatement being corrected

The final terminal response of the source correction run
PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009 stated that
the fresh-context internal QC performed a full independent re-execution of
`14 + 86 + 24` outcomes. The direct fresh-QC record documents
**re-execution of 14 + 18 + 24 = 56 outcomes**; the remaining 68 additional
outcomes (43 cases x 2 gates minus the 9 re-executed cases x 2 gates) have
documented MACHINE-PARSED verification (recomputation from the recorded raw
rows), not documented re-execution.

Corrected statement (supersedes ONLY the overbroad coverage claim of that
final response):

> The earlier fresh-context internal QC of the a7b1dc0 package re-executed
> 56 outcomes (fixed matrix 14; 9 of the 43 additional cases in both gates =
> 18; byte regression 24) and machine-parsed all 86 additional outcomes
> from raw records. A claim that it re-executed the full 14+86+24 is
> superseded. The later independent Desktop post-audit separately
> re-executed the full 14+86+24; that is Desktop evidence, not fresh-QC
> evidence.

No double counting: parsed and re-executed outcomes are not counted as
unique tests. The 18 re-executed additional outcomes are a SUBSET of the 86
machine-parsed ones; the unique documented verification set of the fresh QC
is "86 machine-parsed (of which 18 also re-executed) + 14 fixed re-executed
+ 24 regression re-executed".

## 4. What is NOT changed by this erratum

- The fresh QC record itself (0C6B6912...) is preserved byte-unchanged; this
  erratum is a NEW record, not an edit of it.
- The historical final answers of the source correction run, its
  PRE/POST/regression results, its manifest and its committed files.
- The authentic value of the fresh QC: its verdict (PASS on what it
  measured) and its findings stand as written; the record itself honestly
  distinguished its re-executed rows from its machine-parsed rows — the
  overstatement was in the terminal summary's compression of that record.
- The Desktop post-audit's own results and attribution.
- Any science: CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_
  CONDITIONAL and all standing science are unchanged (see
  SUPERSESSION_AND_STANDING.md). No automatic science or governance
  retraction follows from this records correction.

## 5. Process ordering (recorded, unchanged)

```text
ORIGINAL_FRESH_QC_BEFORE_PUBLICATION = NOT_MET
   (the fresh QC of the a7b1dc0 package ran AFTER its commit/push; the
    committed files honestly recorded SELF_REVIEW and the fresh QC as
    NOT_PERFORMED at publication time; the later record is what it is)
RETROACTIVE_ORDER_COMPLIANCE = NO
   (the old contract section 6 did not itself authorize moving the fresh
    QC after commit; no human exception is invented here)
PUBLICATION_INTEGRITY = PASSED INDEPENDENTLY OF THIS PROCESS DEVIATION
   (the Desktop post-audit measured PUBLICATION_INTEGRITY = PASS; the
    ordering deviation does not invalidate the published evidence, and no
    automatic retraction follows)
```

The corrected gates of THIS run do not retroactively repair the earlier
chronology: the new evidence (PRE 8, LF 16, fixed 14, additional 86, byte
regression 24 — all executor-measured this run) is attributable to THIS
run, and the fresh-context QC of THIS package is arranged by the
orchestrator as a separate later review (its coverage will be measured
separately and recorded in QC_RESULTS.json / QC_REPORT.md by that reviewer;
PENDING at executor stage — not fabricated here).
