# PUBLICATION_SCOPE — PE_935_PROVIDER_PROVENANCE_APPLIER_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261023

Published here: 9 own sanitized files (REPORT.md, HANDOFF.md, DERIVED_CLAIMS.json, RESOURCE_INSTANCE_TRANSFORM_MATRIX.csv, QC_FINDINGS.json, FIRST_MISSING_EDGE.json, STAGE_ACCEPTANCE_GATES.csv, PUBLICATION_SCOPE.md, EXTERNAL_POSTAUDIT_SUMMARY.md) + additive POSTAUDIT_NOTICE_R1.md in the predecessor MINCAP folder + one newest-first AUDIT_ENTRYPOINT.md row (12 diff paths with the publication manifest).

SANITIZATION (explicit transforms, no false byte-parity claimed):
- REPORT.md, HANDOFF.md, RESOURCE_INSTANCE_TRANSFORM_MATRIX.csv, QC_FINDINGS.json, FIRST_MISSING_EDGE.json, STAGE_ACCEPTANCE_GATES.csv: byte-identical copies of the sealed local artifacts (already sanitized; verified no raw cells, no EXE header, no H5 row listings, no SDK source, no packets, no prompts, no model answers, no DB dumps, no secrets).
- DERIVED_CLAIMS.json: public projection of the sealed CLAIMS.json (claim id/text/status/scope/era/qc_scope/premises/notes; no transformation of wording).
- EXTERNAL_POSTAUDIT_SUMMARY.md: VERBATIM copy of the current MSC postaudit PUBLIC_SUMMARY (PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_DEEP_POSTAUDIT_R1_20261023), per contract.
- All files UTF-8 (local sealed copies already UTF-8; no BOM changes).

NOT published (local-only, per contract): CONTROL/ (run-local packets, tickets, events log), JOBS/ (worker QC/raw artifacts), DISPATCH_READY/, ledgers with full internal accounting (BODY_AND_BUDGET_LEDGER, ROLE_LEDGER, DISPATCH_RECONCILIATION, NATIVE_TASK_CENSUS, TERMINAL_CONSISTENCY, INPUT_RECHECK, FINAL_ACCOUNTING_DRAFT, CORRECTION_LEDGER), POINTER_TIME_MAP.json, PROVIDER_PROVENANCE.json, APPLIER_DESTINATION.json, BRANCH_RELEVANCE.json, IDENTITY_AND_TIME_MAP.json, SELF_REVIEW_1/2.md.

PUBLICATION IS NOT SCIENTIFIC ACCEPTANCE. CANONICAL_GATE_EFFECT = NONE. DESKTOP_POST_AUDIT = PENDING.
