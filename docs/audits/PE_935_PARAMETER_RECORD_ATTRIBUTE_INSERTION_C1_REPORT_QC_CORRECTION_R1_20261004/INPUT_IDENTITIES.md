# INPUT_IDENTITIES — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

## ERA lock

- PRIMARY TARGET = PCG_9_3_5 / Entropia Universe 9.3.5 (pcg_install).
- No CD_2003 / JUL_2003 / EU10+ / DAoC / WAR data used anywhere in this run.

## Corpus identities (physically re-verified this run; read-only)

| Input | Path | Size (B) | SHA256 |
|---|---|---|---|
| Entropia.exe | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |
| templates.vfs | `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs` | 560,788 | BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 |

Both match the R1 package's pinned identities byte-for-byte (INPUT_IDENTITIES.md of
PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004). No source file was modified.

## MANDATORY INPUT: the independent Desktop post-audit (read fully; identities)

Base directory: `C:\Users\User\Documents\ChatGPT\PE\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_DESKTOP_POST_AUDIT_20261004\`

| File | Size (B) | SHA256 |
|---|---|---|
| REPORT.md | 11,672 | 015F3C885D09059B295D86CAFB7A28D1E8B19387797B73A3CE989F174FDB4A07 |
| QC_COUNTEREXAMPLE_SUMMARY.json | 434 | 1086C73C46E2494982390327172DA74F9D93028FF2F45047A05C1AFE0600FF47 |
| QC_COUNTEREXAMPLE_published_document.json | 3,746 | 2109FEA411AB7EE84C7BAF5B015254D3F8B9DE052C495A9C2CC47C346448FCE5 |
| QC_COUNTEREXAMPLE_deliberately_wrong_destination_document.json | 3,746 | 2109FEA411AB7EE84C7BAF5B015254D3F8B9DE052C495A9C2CC47C346448FCE5 |
| qc_counterexample.py | 1,718 | 0566530596FB1923508DECEE3917C49B2722AABD35A0ECB843F3D976515E2624 |
| REMOTE_FINAL_CHECK.json | 351 | 13721D5FE59C95F461670DBA487F69D16B150813EA77C70E2805BE72FCE609DB |

Key evidence property: the two QC_COUNTEREXAMPLE raw outputs are **byte-identical
(same SHA256)** — the published R1 QC (8/8 gates PASS) was literally invariant to the
Desktop's deliberate A/B destination-documentation swap of PARSER_CHAIN.md (private
copy; EXE/VFS unchanged). This falsifies the declared scope of the R1 QC-7 row
("parser raw↔decoded roundtrip ... with the byte-decoded destinations") and of the
PARSER_CHAIN.md claim "Destinations (verified in QC-7 ...)": QC-7 never read the
destination table or the destination instructions.

## Corrected target package (the R1 package; corrections applied per this order)

- `docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/` — the R1
  publication at parent commit 4c1205342abd1b051f72fab9932532b1f0ed86fe.
- Corrected files (ONLY the ordered C1/C2/P3 corrections; original evidence of every
  mistake preserved in SUPERSESSION_LEDGER.md + CORRECTED_DOC_DELTAS.md + git history):
  FINAL_REPORT.md, HANDOFF.md, PARSER_CHAIN.md, RECORD_A.md, RECORD_B.md,
  QC_REPORT.md, RECEIVER_INSERTION_CHAIN.md, PLACEMENT_CONSUMER_EDGE.md.
- NOT modified: 01_RAW/*, 03_SCRIPTS/*, PARAMETER_FILE_INVENTORY.csv, SELECTED_FILE.md,
  INPUT_IDENTITIES.md, COMMITTED_PACKAGE_MANIFEST_SHA256.csv (the R1 manifest is the
  historical record of the R1 publication's file states at 4c12053; the corrected
  files' new identities are carried by THIS package's manifest).

## Repo state

- BASE_SHA = 4c1205342abd1b051f72fab9932532b1f0ed86fe (local HEAD = local origin/master
  = actual remote master, re-verified by `git fetch` + `git rev-parse` + `git ls-remote`
  at run start; re-verified again immediately before the commit).
- Foreign untracked groups (untouched): docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/, PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/, PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.

## Desktop-report deviations found by this run's own byte verification

- Desktop REPORT.md cites the loader's ECX-preserve site as `@0x0072FA6C`. The pinned
  EXE bytes show `MOV [ESP+0x38],ECX` = `89 4C 24 38` starting at **0x0072FA6B**
  (0x0072FA6C is the ModRM byte, not the instruction start). The load-bearing semantic
  claim (the loader PRESERVES the incoming ECX and does NOT itself call the singleton)
  is byte-confirmed either way; only the cited start is corrected by one byte. This
  deviation is recorded here and in SUPERSESSION_LEDGER.md row S-P3-4.
- Desktop REPORT.md's B/C/FLD instruction starts (0x00730D14 / 0x00730D42 / 0x00730D69)
  and the class-selector/tag-6 chain pins (0x004C54C2 / 0x004C54CE / 0x004C551F /
  0x004C5523 / FUN_0070C180 rel32 / FUN_00452490 wrapper) were all independently
  re-verified from the pinned EXE bytes by this run (TQ2–TQ6 in
  01_RAW/QC_TARGETED.json; windows in 01_RAW/EXE_BYTE_PROOFS.json) — MATCH.
