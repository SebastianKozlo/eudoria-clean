# RUN CONTRACT - EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916

- RUN_ID: `EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916`
- ASSIGNMENT_MODE: FULL_MILESTONE_AUDIT (Gate-B pre-check over the standing V4.1 deliverable lineage)
- TARGET: EU935-M1 WORLD SURFACE FIDELITY
- EXECUTOR-OF-RECORD: PE-MASTER in-session audit. This package is persisted by
  pe-master-auditor under a bounded PERSIST_PUBLISH contract: PE-MASTER's
  adjudication is persisted verbatim; NO new science; no verdict text altered.
- EXPECTED_START_SHA: `0187e18455081e58fc1f38ee36d974206483093d` - VERIFIED:
  HEAD == origin/master == `git ls-remote origin refs/heads/master` at audit start
  (PE-MASTER) and re-verified at this persistence (pe-master-auditor): all three
  read `0187e18455081e58fc1f38ee36d974206483093d`.
- GIT STATUS AT START: tracked tree clean; exactly 2 pre-existing untracked
  roots, untouched by this run: `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
  and `experiments/`.
- PROJECT_STATE.json: ABSENT in the repository -> recorded as
  GOVERNANCE_SOURCE_ABSENT (recorded, not invented; finding F3, P3).
- NO_NESTED_TASKS: YES (the persistence contract's own flag; zero Task
  dispatches were made in this run).
- PERMITTED PERSISTENCE ROOTS:
  `docs/audits/EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916/**` and
  `AUDIT_ENTRYPOINT.md` ONLY (the §19 housekeeping touch).
- FORBIDDEN to stage (contract §20/§21):
  `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/**`, `experiments/**`,
  anything else. Historical packages READ-ONLY.
- TEXT FILE RULES: strict UTF-8 (no BOM); LF or CRLF consistent per file; CSV
  files carry header rows.
- STOP CONDITION: this run stops at MILESTONE_CANDIDATE_FOR_DEEP_AUDIT max
  (advisory pre-qualification; no milestone closure; nothing authorizes M2).

## §19 ENTRYPOINT HOUSEKEEPING AUTHORIZATION (exactly one cell + one row)

- Target row: the PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 row of the
  LATEST RUNS table.
- Cell replacement (the ONLY cell modified):
  - OLD: `PENDING (PE-MASTER supersession adjudication; G16R/G17R/G18R; persistence by pe-master-auditor)`
  - NEW: `MASTER_ACCEPTED (advisory; supersession R2; G16R/G17R/G18R PASS — AMEND-019 persistence)`
- Row addition (the ONLY row added): the new top row of the LATEST RUNS table
  for this audit (RUN_ID EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916).
- rows_added=1, rows_removed=0, rows_modified=1 - verified:
  `git diff --numstat AUDIT_ENTRYPOINT.md` = 2 insertions / 1 deletion;
  LATEST RUNS rows 58 -> 59; the 57 untouched original rows byte-identical;
  the 1 modified row = the authorized NIF-correction row (differs from its
  original only by the authorized verdict-cell replacement).

## PRE/POST EDIT EVIDENCE

- PRE_EDIT SHA256 (AUDIT_ENTRYPOINT.md, before the edit):
  `D5F61F383E80FC0C375BDA244146A918612971EC986097E488D0C0952286DA94`
- Byte-identical pre-edit copy preserved at:
  `00_CONTROL/AUDIT_ENTRYPOINT.md.pre`
  (SHA256 `D5F61F383E80FC0C375BDA244146A918612971EC986097E488D0C0952286DA94`,
  verified equal to the pre-edit file).
- POST_EDIT SHA256 (AUDIT_ENTRYPOINT.md, after the edit):
  `09DA50660376ED6363282CE10549EEFCB8D872DF4C932E68892D131349C52CA7`
- Verification probes at edit time: old-cell text occurrences 0 (was exactly 1
  before the edit); new verdict text occurrences 1; LATEST RUNS table anchor
  (header + separator) occurrences 1; total file lines 115 -> 116; CR count 0
  (the file stays LF-only); UTF-8 written without BOM.
