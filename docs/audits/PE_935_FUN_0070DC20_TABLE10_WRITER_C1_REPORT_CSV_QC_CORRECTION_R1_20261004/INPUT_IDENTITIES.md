# INPUT_IDENTITIES — PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004

## Baseline identity (verified at preflight and re-verified by the QC gate Q1)

| Item | Value | Verification |
|---|---|---|
| local HEAD | 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 | `git rev-parse HEAD` |
| local origin/master | 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 | `git rev-parse origin/master` after `git fetch` |
| actual remote master | 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 | `git ls-remote origin master` |
| BASE_SHA (contract pin) | 4627d385b3f77f18bc2af5c02ed1f25182ec9fa5 | MATCH — no BASE_DIVERGENCE |
| tracked dirty paths | NONE | `git status --porcelain`: only the 5 foreign untracked PE_935_* dirs + experiments/ + this new package |
| foreign untracked (untouched) | docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001, docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003, docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914, docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930, docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928, experiments/ | read-only; not staged; not in manifest |
| output root | docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004/ | verified NON-EXISTENT before first write; created fresh |

## Pinned EXE identity (used ONLY for the two P3 VA-correction byte re-reads; re-verified by QC gates Q10/Q11)

| Item | Value |
|---|---|
| Path | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe |
| Size | 8,015,872 bytes |
| SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |
| EXE byte reads in this run | EXACTLY 4 windows (16 bytes total): the corrected fail-path VA (6 B), the superseded fail-path VA probe (2 B), the corrected component-vtable-store VA (6 B), the superseded component-vtable-store VA probe (2 B) — all inside 03_SCRIPTS/qc_table10_writer_c1.py; no other EXE access |

## Historical source package (READ-ONLY; identities re-measured by QC gate Q1 and cross-checked against this table)

Historical package: docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004 (published at BASE 4627d385; its own BASE was 2bfb0f23). All rows below are byte-identical to the BASE commit content (tracked + clean; disk == commit because core.autocrlf=false).

| Historical source file (READ-ONLY) | Size bytes | SHA256 |
|---|---|---|
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FINAL_REPORT.md | 10619 | 00E39DE03272F846D98BFDEBE0AB5F738059AF29CED749752C1D1E42C3C60EB2 |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/HANDOFF.md | 4784 | 49087E4F0DEA175090D526FA566F0379544C44663C1674E766E83FE49F0DEE45 |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/QC_REPORT.md | 8011 | 6B1230B1013DC09A4CB5332089C5B33157D324EE292D71EF97AFB0A35E9AEDC9 |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/INPUT_IDENTITIES.md | 5294 | AF71E6BC6C181F175B95FF23720656D9F65225D11ABA4DD3FF6759F0FFA89B86 |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/FUNCTION_LEDGER.csv | 2816 | 9E1AD7650CB229B024B4178DF9F310DDEBD4883BDB77515DA7A2236D09CEB2CF |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/WRITER_CHAIN.csv | 3854 | 78ED1585C9BE1F96216D20B23D9FA6442AC66BDF5AC6F38E70CD086D40589D91 |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/01_RAW/S5_QC_BATTERY.json | 19266 | 8F35A5B54BA1BDFC407256E905514BE69B8EA65497331676AF2A6B89F86964BB |
| docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/03_SCRIPTS/s5_qc_battery.py | 22014 | D7CB376DF0D64D35AA2F10F2AF62E618D38F77D8370A0DF6A6E111A1E56371A3 |

## Corrected CSV artifacts (generated in THIS package by the W2 serialization repair; measured identities recorded by QC gate Q1)

| Artifact | Serialization |
|---|---|
| CORRECTED_FUNCTION_LEDGER.csv | Python csv.writer, encoding="utf-8", newline="", LF line terminator; 7-column header; 8 data rows; logical content = historical content except the authorized F-1 change (P3-A fail-path VA, record S-7) |
| CORRECTED_WRITER_CHAIN.csv | Python csv.writer, encoding="utf-8", newline="", LF line terminator; 6-column header; 26 data rows; logical content = historical content except the authorized F-2 change (W3 storage-identity scope wording, record S-5) |

Reconstruction method (auditable in 03_SCRIPTS/qc_table10_writer_c1.py):
the historical files are naive comma-split text; every field before the
final free-text field is comma-free (asserted per row), the final field(s)
are recovered by re-joining the tail pieces, and the byte-accounting
assertion ",".join(logical_fields) == original_line proves the
reconstruction loses nothing. The corrected CSVs re-serialize those logical
fields with standard CSV quoting. The chain's operation/structural_identity
boundary uses per-row piece counts recorded in the QC script, verified by
balanced-delimiter invariants and the same join round-trip.

## Instrument identity

| Script | Output | Purpose |
|---|---|---|
| 03_SCRIPTS/qc_table10_writer_c1.py | 01_RAW/QC_LEDGER_BUDGET.json, 01_RAW/QC_CSV_STRICT.json, 01_RAW/QC_VALUE_SCOPE.json, 01_RAW/QC_NEGATIVE_CONTROLS.json | the targeted correction QC battery (Q1-Q14 + AUX quotecheck); READ-ONLY against the repo/EXE except its four 01_RAW JSON outputs |

No proprietary binaries/corpora are included in this package; the only
original-binary-derived content is the 16 bytes of the four P3 pin windows
recorded as measured evidence in 01_RAW/QC_VALUE_SCOPE.json.
