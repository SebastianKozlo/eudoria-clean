# HANDOFF — PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

Contract §19 terminal fields (persistence/publication phase). RESULTING_SHA and REMOTE_SHA
are governed by the one-commit + manifest-LAST constraints: their post-push values are
recorded in the terminal handoff returned by the persistence worker to PE-MASTER (which
reports them to the human); the committed package points to that record via the literal
field values below. No second commit exists or is permitted for this run.

## §19 TERMINAL FIELDS BLOCK

```text
RUN_ID =
PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

EXPECTED_BASE_SHA =
57ecf3506481e73ca27548ea02e4864904d9883a

RESULTING_SHA =
RECORDED_AT_TERMINAL_HANDOFF_(post-push;_one_commit_contract)

REMOTE_SHA =
RECORDED_AT_TERMINAL_HANDOFF_(post-push;_one_commit_contract)

SOURCE_DESKTOP_POST_AUDIT =
PERFORMED (Desktop post-audit of 57ecf3506481e73ca27548ea02e4864904d9883a)

NEW_CORRECTION_DESKTOP_POST_AUDIT =
NOT_PERFORMED (the fresh independent internal QC of this run is NOT the future Desktop
post-audit of the new published correction SHA)

SOURCE_PACKAGE_UNCHANGED =
YES (git diff 57ecf350 -- docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 = empty; git status clean for that path; 27 physical files unchanged; verified before commit)

NC1_SHARED_SIB_FALSE_PASS =
CORRECTED_AND_REVALIDATED

REAL_RECORDED_CLEAN:
  PRODUCTION = PASS
  INDEPENDENT_QC = PASS

HISTORICAL_EDI_CLOBBER:
  PRODUCTION = FAIL
  INDEPENDENT_QC = FAIL

FINAL_PUSH_ESI:
  PRODUCTION = FAIL
  INDEPENDENT_QC = FAIL

FINAL_PUSH_NOP:
  PRODUCTION = FAIL
  INDEPENDENT_QC = FAIL

NC1_SIB_HIDDEN_EDI_WRITE:
  PRODUCTION = FAIL (fail-closed SIB guard: rejected before any displacement/length computation)
  INDEPENDENT_QC = FAIL (fail-closed SIB guard: rejected before any displacement/length computation)

CTRL4_BOUNDARY_VALIDATION =
SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS
(NOT GENERAL_X86_DECODER_PROVEN)

C4_C1_RECORDS =
ACCEPTED_IN_EXAMINED_RECORDS_SCOPE

MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32
EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED

MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7
EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED

ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL
ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL
ORIGINAL_SCOPE_COMPLIANCE = FAIL
RETROACTIVE_PRIOR_AUTHORIZATION = NO

WRAPPER_DEPTH = UNRESOLVED
HISTORICAL_LINEAGE_BUDGET_CHARGE =
NEW_WRAPPER_HOPS = 2
MAX_NEW_WRAPPER_HOPS = 3

CHILD_RESOURCE_PROVENANCE =
STRONGLY_SUPPORTED_MODEL_DERIVED

MODEL_ROOT_RELATION =
UNKNOWN

CHILD_VISUAL_ROLE =
UNRESOLVED

CHILD_TO_JOIN_IDENTITY =
STRONGLY_SUPPORTED

EXACT_PARENT =
CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
scoped to examined ACLD path

JOIN_OPERATION =
STRONGLY_SUPPORTED

CAND4_CHILD_ROOT_CLOSURE =
NOT_ESTABLISHED_WITHIN_BOUND

WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO

QC_ORIGIN =
FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR

QC_VERDICT =
PASS (gate: ALL 10 rows (5 cases x production/independent) match the required results
AND production-authenticity establishment succeeds AND clean-window boundary regression
holds; measured ten_rows_ok=TRUE, authenticity=SUCCEEDED, regression=HOLDS)

PACKAGE_PHYSICAL_FILE_COUNT =
14 (13 package files + MANIFEST_SHA256.csv; per the physical census)

MANIFEST_ROWS =
14 (13 package rows — every physical file under OUTPUT_REPO_PATH except the manifest
itself — + 1 AUDIT_ENTRYPOINT.md row; AUDIT_ENTRYPOINT.md listed repo-relative)

MANIFEST_BIJECTION =
PASS (missing=0, extra=0, duplicate=0, size mismatch=0, SHA256 mismatch=0;
generator self-check + independent persistence-phase full re-hash)

CHANGED_PATH_CENSUS =
exactly 15 paths, all inside the REPO_WRITE_ALLOWLIST
(OUTPUT_REPO_PATH/** = 14 package files + AUDIT_ENTRYPOINT.md);
staged census clean — zero foreign, zero historical-package files, zero .pyc;
pre-existing untracked foreign paths untouched (5x PE_935_* packages + experiments/)

OPEN_FINDINGS =
NONE material.
Disclosed (not defects of the corrected machinery):
1. QC self-correction 1 — self-referential counting defect in the QC's own structural
   self-check, fixed before the final measured run (honest negative intermediate of the
   QC's own tooling; QC_REPORT.md §9).
2. QC self-correction 2 — QC engine grp1-imm8 operand text initially rendered the raw byte
   0xfd instead of the sign-extended 0xfffffffd, fixed before the final measured run;
   lengths and verdicts unaffected (QC_REPORT.md §9).
3. P3_TOOLING_CLEANUP note — production grp1-imm8 operand-text rendering fixed in the same
   decoder-only edit; lengths regression-tested unchanged; no science status affected.
4. Historical records wording backlog (Desktop §5.2 "69 x 9" vs 69x10 original fields; the
   "fourth" recurrence ordinal) — documented, NOT reopened by this run.

CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Notes

- NC1 changes validation machinery only; it does NOT create or retract historical
  placement data.
- Publication is NOT acceptance: the PE-MASTER verdict is advisory
  (ADVISORY_PRE_QUALIFICATION; Q1 absent, PROVISIONAL_UNTIL_QUALIFIED;
  CANONICAL_GATE_EFFECT=NONE), and the independent Desktop post-audit of the NEW published
  correction SHA (NEW_CORRECTION_DESKTOP_POST_AUDIT) remains pending.
- Persistence: exactly ONE normal commit at BASE 57ecf350 (no amend, no force push, no
  history rewrite), normal fast-forward push; MANIFEST_SHA256.csv generated LAST.
