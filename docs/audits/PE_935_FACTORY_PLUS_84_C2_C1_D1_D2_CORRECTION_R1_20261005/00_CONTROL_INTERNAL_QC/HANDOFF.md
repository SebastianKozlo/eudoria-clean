# HANDOFF — 00_CONTROL_INTERNAL_QC (independent internal QC of the D1/D2 correction package)

RUN_ID = PE_935_QC_INTERNAL_20261005
ASSIGNMENT_MODE = INTERNAL_QC (fresh context; STATIC-ONLY; NO_NESTED_TASKS)
AUDITED_RUN_ID = PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
BASE_SHA = 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92 (HEAD unchanged; nothing
committed/staged by the executor run or by this QC; the package remains
untracked exactly as dispatched)

## VERDICT

QC_VERDICT = QC_PASS_WITH_FINDINGS

- All load-bearing D1/D2 scientific claims were independently reproduced or
  re-verified from physical evidence (own in-memory execution of the
  corrected decoder + boundary machinery; own execution of the committed
  BASE modules for the defect reproduction; own full-.text pattern census;
  own full-field PINS/registry comparison; own manifest re-hash; own
  supersession quotecheck; own byte-identity compares vs BASE blobs).
- 2 findings P2 (record/provenance, NOT scientific-result defects):
  - F1: `01_RAW/CQC_FINAL.json` field `qc_scope` carries the BASE
    THREE-P2 scope name (stale literal at 03_SCRIPTS/cqc_battery.py:2745);
    contradicts the QC_SCOPE declared in QC_REPORT.md/FINAL_REPORT.md/
    INPUT_IDENTITIES.md.
  - F2: `REGRESSION_DIFF.json` reports[...CQC_MUTATION_RESULTS.json].
    sha256_new = A83B0B71... != actual committed file EB2707AF...
    (diff_vs_base ran before the final docs-mode battery; the mutation
    records embed random mkdtemp paths — observation O1).
- All other 15 recorded SHA identities in REGRESSION_DIFF verified true;
  the package manifest itself is 38/38 correct.

## CORRECTION_REQUEST (to PE-MASTER, for pe-reconstruction)

Single bounded record-hygiene fix inside D1/D2 (no new science):
1. cqc_battery.py:2745 -> "SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION";
   re-run the battery --mode data + --mode docs (fresh outputs; gates must
   re-verify 14/14 + 15/15).
2. Re-run diff_vs_base.py AFTER that final battery (repairs F2), then
   regenerate the manifest (already mandatory for the persistence phase due
   to the entrypoint row) and re-verify the 38-row bijection.
Alternative (if PE-MASTER prefers no instrument re-run): publish with the
two findings disclosed as open P2 record defects in the PE-MASTER review and
the package handoff. They do not invalidate the D1/D2 results.

## COVERAGE / NOT_CHECKED

- FULL_READ: all 38 package files (16 root + 11 raw + 11 scripts); all
  load-bearing sources read to EOF (x86dec.py 671 l., cqc_battery.py 2787 l.,
  pebnd/c1/c2/c3/capture/make_manifest via full unified diffs vs BASE blobs,
  pin_roster/extract_expected_pins/diff_vs_base in full); contract file read
  in full.
- NOT_CHECKED: battery not re-executed (would overwrite executor evidence —
  forbidden for the QC worker; replaced by independent in-memory
  counter-executions of the same predicates); objdump not re-invoked (oracle
  records verified for internal consistency and set composition); mutation
  temp trees not re-created (verified from persisted hashes/predicates +
  harness code); process-timing disclosures accepted as consistent records;
  Desktop post-audit REPORT.md hash-verified only (content not re-audited —
  requirements taken from the dispatch contract).
- Full details, measurements table (26 own gates) and finding mechanics:
  see QC_INTERNAL_REPORT.md and STAGE_ACCEPTANCE_GATES.csv in this directory.

## BLAST-RADIUS NOTE FOR THE PERSISTENCE PHASE

This QC directory (00_CONTROL_INTERNAL_QC) and its files were created INSIDE
OUTPUT_ROOT after the executor's manifest was generated. The executor
manifest remains internally valid (38/38) but does not cover the QC files.
The persistence phase must decide: either regenerate the manifest with the QC
directory included in scope, or keep the QC directory outside the committed
allowlist (its inclusion in the published package was not part of the
executor's 38-path allowlist; my artifacts here are working QC records, all
listed in ARTIFACT_INDEX.csv). No executor file was touched.

## TERMINAL RETURN (compact)

ASSIGNMENT_MODE=INTERNAL_QC / RUN_ID=PE_935_QC_INTERNAL_20261005 /
PARENT_LOOP_ID=PE-MASTER dispatch 2026-10-05 / MILESTONE=PE_935 F84 chain
(D1/D2 correction) / QC_VERDICT=QC_PASS_WITH_FINDINGS /
FINDINGS=F1 P2 (CQC_FINAL qc_scope stale THREE-P2 label; cqc_battery.py:2745),
F2 P2 (REGRESSION_DIFF stale sha256_new for CQC_MUTATION_RESULTS.json;
mechanism: pre-final-run diff + nondeterministic mkdtemp fields O1) /
FULL_READ_LOG=00_CONTROL_INTERNAL_QC (this directory; see ARTIFACT_INDEX.csv)
/ NOT_CHECKED=battery re-execution; objdump re-invocation; temp-tree
recreation; Desktop-report content audit; process-timing re-derivation /
FINAL_REPORT_PATH=00_CONTROL_INTERNAL_QC/QC_INTERNAL_REPORT.md /
GATES_PATH=00_CONTROL_INTERNAL_QC/STAGE_ACCEPTANCE_GATES.csv /
MANIFEST_PATH=00_CONTROL_INTERNAL_QC/ARTIFACT_INDEX.csv /
BASE_SHA=9d31a82 / HEAD_SHA=9d31a82 (unchanged) / PUSH_STATUS=NOT_PERFORMED
(QC worker; no commit/push authorized or performed) /
FILES_CHANGED=only new files under 00_CONTROL_INTERNAL_QC/ /
UNRELATED_WORK_EXCLUDED=executor package fully read-only; six foreign
untracked paths untouched; AUDIT_ENTRYPOINT.md untouched /
NEXT_PARENT_ACTION=route the CORRECTION_REQUEST (F1+F2, both inside the
already-planned persistence phase) to pe-reconstruction, or accept
publication with the two P2 findings explicitly disclosed in the PE-MASTER
review; then proceed with the persistence-phase checklist in the package
HANDOFF.md (review persistence, entrypoint row, manifest regeneration,
path-limited commit/push, remote verification, hard stop for the Desktop
post-audit).
