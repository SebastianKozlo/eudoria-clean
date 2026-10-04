# INPUT_IDENTITIES — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004

## Corpus (read-only inputs; identities re-verified by this run)

| Input | Path | Size (bytes) | SHA256 | Role |
|---|---|---|---|---|
| Desktop post-audit REPORT.md | C:\Users\User\Documents\ChatGPT\PE\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_20261004\REPORT.md | (hashed) | B433828F8DF5C8EFF80A81303BD9A8CA88258E985A4ADB4760B1E6DEE3E670CD | the findings source (GP1/GP2/GP3 + FUNCTION_BUDGET_OVERRUN); battery A1 PASS |
| PE_MASTER_REVIEW_INPUT.txt | same directory \PE_MASTER_REVIEW_INPUT.txt | (hashed) | 61A0DB5CBD4F52C806107A76811C9B13D0A83679F053556F91D2FC9781608AC9 | the external review echoed by the R1 wording (source-exclusion wording lives HERE, not in the repo); battery A2 PASS |
| Entropia.exe (pinned) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | the ONLY binary read; all byte pins of this correction are reads from it; battery B1/B2 PASS |

Both Desktop input SHA256s match the dispatch pins exactly. A missing or
mismatching source would have been BLOCKED_INPUT; no made-up paths were used.

## Base / repo

- BASE_SHA (dispatch pin, re-verified before the first canonical write):
  25335a28ee61fc2a8c7763f41552df85af45d067.
- At run start: local HEAD == origin/master == actual remote master ==
  25335a2 (git rev-parse HEAD, origin/master + git ls-remote origin master —
  all three measured; recorded in the session and re-verified again
  immediately before commit, see FINAL_REPORT PERSISTENCE).
- Pre-existing untracked paths at start (FOREIGN — not touched, not staged,
  not absorbed): docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
- Output root docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_
  REPORT_SCOPE_CORRECTION_R1_20261004/ verified NON-EXISTENT at start
  (Test-Path False) and created fresh by this run.
- `git status --porcelain` at start: ONLY the foreign untracked entries above
  — zero tracked-file modifications; therefore every repository excerpt in
  the supersession ledger was read from the EXACT BASE_SHA 25335a2 tree.

## Corrected target (READ-ONLY; historical — not modified)

| Package | Status this run |
|---|---|
| PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 (published at 25335a2) | read-only source of every superseded ORIGINAL_EXCERPT (FINAL_REPORT.md, PRODUCER_PROVIDER_CHAIN.md, GETTER_CHAIN.md, GETTER_RESULT_DATAFLOW.md, ALTERNATIVE_BRANCH.md, CONTROL_CASE.md, HANDOFF.md, PROVENANCE_CHAIN.csv); its 01_RAW/S5_CREATOR_DECODE.json is the published measured census this run re-measured at the SAME scope; its S1-S11 records were NOT rerun and NOT replaced |
| AUDIT_ENTRYPOINT.md (R1 LATEST RUNS row) | read-only; superseded by THIS run's ONE NEW row (no old row edited) |
| PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004 + PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004 | format precedent for the supersession ledger / ORIGINAL_EXCERPT-vs-verbatim discipline (P3 lesson S-P3-1) — read only, not reopened |

templates.vfs was NOT opened, re-measured or used this run. No model/NIF/
Gamebryo/network work. No placement RE.

## Instruments (all in 03_SCRIPTS/, all READ-ONLY vs originals)

| Script | Output | Purpose |
|---|---|---|
| qc_correction_c1.py `bytes` | 01_RAW/QC_CORRECTION_BATTERY.json | 27 bounded checks: input identities (A1-A2), EXE identity (B1-B2), GP2 alternative-flow pins (C1-C11), GP3 statics placement + fallback addressing + direct-literal census re-measurement (D1-D6), GP1 scoped default-creation pins (E1-E6) + the forbidden-actions census (all NO) |
| qc_correction_c1.py `docgates` | 01_RAW/QC_DOC_GATES.json | textual gates over THIS package's own docs (required + forbidden strings; Q1-Q8 mapping) |
| qc_correction_c1.py `quotecheck` | 01_RAW/QC_LEDGER_QUOTE_CHECKS.json | every SUPERSESSION_LEDGER.md ORIGINAL_EXCERPT machine-verified as a whitespace-normalized substring of its named SOURCE_FILE (no fabricated quote, no misattributed quote) |

The script sets sys.dont_write_bytecode=True, reads the pinned EXE through a
section-table PE mapper (no offset==RVA assumption — same discipline as the R1
instruments), and writes only into this package's 01_RAW/.

## In-run deviations (honest record)

1. The battery's E4 check (slot-6 schema args @0x73758D) was first written
   with an 8-byte expectation and FAILED on the first run (measured
   "50 6a 00 6a 00 6a 01 6a" — the ninth byte "06" is the tag byte of the
   published 9-byte pin `50 6A 00 6A 00 6A 01 6A 06`). The check was corrected
   to the published 9-byte pin and the battery re-run: 27/27 PASS. No
   semantic expectation changed — the fix aligned the check width with the
   published pin; the FAIL and the fix are recorded here.
2. No other instrument deviation. No document was written after the manifest.
