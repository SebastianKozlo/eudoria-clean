# INPUT_IDENTITIES — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

## ERA lock

- PRIMARY TARGET = PCG_9_3_5 / Entropia Universe 9.3.5 (pcg_install).
- No CD_2003 / JUL_2003 / EU10+ / DAoC / WAR data used anywhere in this run.

## Corpus identities (physically re-verified this run; read-only)

| Input | Path | Size (B) | SHA256 |
|---|---|---|---|
| Entropia.exe | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |
| templates.vfs (SELECTED_FILE) | `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs` | 560,788 | BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 |

- Entropia.exe: image base 0x00400000 (PE32, ASLR OFF — section table read by this run's
  own mapper `s2_exe_windows.py`; no offset==RVA assumption).
- templates.vfs: magic "ArkVFS02"; verified against the pinned identity in
  ERRATA_R4 (PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913) and BRIDGE R1 PREFLIGHT —
  byte-identical corpus confirmed.
- All 27 Data\Parameters files hashed in `PARAMETER_FILE_INVENTORY.csv` (Phase A).

## Repo state

- BASE_SHA = 780cc4e442ec2bef7e4e0880b9ffee22a39e302c (local HEAD = local origin/master =
  actual remote master, re-verified by `git ls-remote` at run start and again
  immediately before the commit).
- Foreign untracked groups (untouched): docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/, PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/, PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.

## Historical packages used as evidence context (READ-ONLY; not modified)

- PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 (mandatory: HANDOFF.md SHA 90F17EFF...,
  ERRATA_R4.md SHA 8B28BCC6... — both re-hashed at run start, MATCH).
- PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 (REPORT.md, Z2_cwo_chain.md — the FUN_004c5580
  "arg 0x4E26" observation and the driver/queue-push canon).
- PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z (E1–E12 trace blocks, C1 census,
  C2 caller census, R05/R06 decompiles — cited where re-verified).
- PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003 (F-D1..F-D4 corrections; ABI
  registry_this.FUN_0072F580(id2)).
- PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (context only; no 20xxx file was opened in detail).

## Mandatory historical boundaries honored

1. MOVABLE channel preserved as historical knowledge; not re-proved; not generalized to statics.
2. 0xB9 does not deserialize position on the audited path — not contradicted; not investigated.
3. Upstream of the movable cursor NOT investigated this run.
4. The movable channel does not establish static placement sources — no transfer attempted.
5. DEFINITION/CLASS/PARAMETER REGISTRY kept separate from RUNTIME INSTANCE/VALUE MAP —
   the selected container is classified DEFINITION_REGISTRY (see RECEIVER_INSERTION_CHAIN.md).
6. PUSH 4057 @0x0059AB12 / ArkRepairUI not used.
