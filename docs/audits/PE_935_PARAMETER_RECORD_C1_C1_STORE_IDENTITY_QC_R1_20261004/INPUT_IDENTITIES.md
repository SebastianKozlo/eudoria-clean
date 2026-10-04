# INPUT_IDENTITIES — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004

Every identity below was measured by this run (binary reads; SHA256
upper-case hex). The pinned EXE/VFS are READ-ONLY inputs; no original file was
modified by this run.

## Corpus pins (READ-ONLY)

| Input | Path | Size (bytes) | SHA256 |
|---|---|---|---|
| Pinned client EXE | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | 8,015,872 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (== the dispatch pin; PE-MASTER byte-verified at dispatch; re-verified by this run) |
| templates.vfs | `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs` | 560,788 | `BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77` (== the C1-correction package pin; re-verified) |

PE mapper (this run's own, section-table-driven; image base 0x00400000;
`.text` VA 0x1000 / raw 0x1000): all instruction reads use VA→file-offset
translation; no offset==RVA assumption.

## Six oracle pins (PE-MASTER-pinned at dispatch; independently byte-verified
## by this run from the pinned EXE)

| Pin | VA | Expected bytes | Actual (this run) |
|---|---|---|---|
| id2 store (MOV [EDI],EAX) | 0x00730CB6 | 89 07 | 89 07 ✓ |
| A store (MOV [EDI+0x08],EAX) | 0x00730CE6 | 89 47 08 | 89 47 08 ✓ |
| B store (MOV [EDI+0x04],EAX) | 0x00730D14 | 89 47 04 | 89 47 04 ✓ |
| C store (MOV [EDI+0x0C],EAX) | 0x00730D42 | 89 47 0C | 89 47 0C ✓ |
| D FLD (FLD [EDX+EAX]) | 0x00730D69 | D9 04 10 | D9 04 10 ✓ |
| D FSTP (FSTP [EDI+0x10]) | 0x00730D70 | D9 5F 10 | D9 5F 10 ✓ |

The runtime byte-backing (verify_oracle) additionally pins the normal-path
reads (8B 04 10 @0x00730CAB / 0x00730CDF / 0x00730D0D / 0x00730D3B; FLD
@0x00730D69) and the strictly-increasing store VA order —
01_RAW/ORACLE_EVIDENCE.json.

## Instruments

| Instrument | Path | Size | SHA256 |
|---|---|---|---|
| BASE historical verifier (imported READ-ONLY for the defect reproduction; byte-identical to its publication at 97bdf95 — `git status` confirmed no tracked-file modification) | `docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004/03_SCRIPTS/qc_targeted.py` | 32,092 | `CB4587C19ACBD4B7B9DE798A598251D63D97C0DE0CDB5BF80CC09BAA98E734E8` |
| THIS run's corrected instrument | `docs/audits/PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004/03_SCRIPTS/qc_targeted_c1c1.py` | 64,225 | `D1F935FD451AC494F2447DF9C24232BA1057FEE405365006400EEC3854FFA9D9` |

No `__pycache__` was created in the historical package (verified;
`sys.dont_write_bytecode = True` set before the read-only import).

## Tested document (the document under test for TQ2)

- Canonical destination-table document:
  `docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/PARSER_CHAIN.md`
  — 6,704 bytes, SHA256 `6BA91A1FB6181DE8CAFD4CC9A863254C69136FA074291BECD151B5758AB3EEE0`
  (LF line endings, 102 lines; UNMODIFIED by this run).
- The QC also reads the 7 other top-level R1 docs (PLACEMENT_CONSUMER_EDGE.md,
  FINAL_REPORT.md, HANDOFF.md, QC_REPORT.md, RECEIVER_INSERTION_CHAIN.md,
  RECORD_A.md, RECORD_B.md) — all UNMODIFIED.

## Private mutation documents (temp copies; canonical files untouched;
## newline-preserved — the unmutated private copy is byte-identical to the
## canonical disk file, proving the pipeline is content-neutral)

| Case | SHA256 | Note |
|---|---|---|
| canonical private copy (battery negative control) | `6BA91A1FB6181DE8CAFD4CC9A863254C69136FA074291BECD151B5758AB3EEE0` | byte-identical to the canonical disk file |
| mutant A (destination-cell-only swap) | `0AEC1DB4FC646E487FCEE2ECA159B79B6A1DF805ACD7D67B6FC9D112F4DF31A0` | differs from canonical only in the two destination cells |
| mutant B (destination+displacement swap, old VAs) | `2901BD5747831DF8713252187C425F498A1601B186812242B180C9CF340F2C27` | differs from canonical only in the two dest+disp cells |
| mutant C (destination+displacement+REAL STORE VA swap) | `7C0809CD59198CF38413DA962E4AB90974BA94E50631F90D815090D2ADF68C28` | the SAME byte-identical document used for the BASE false-PASS reproduction and the POST-FIX battery |

Mutant rows (exact text):

- Mutant C: `| payload[1] (A) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |`
  and `| payload[2] (B) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |`
  (canonical rows: `| payload[1] (A) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |`
  and `| payload[2] (B) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |`).
- Mutants A/B row texts: recorded verbatim in
  `01_RAW/QC_MUTATION_BATTERY_POST_FIX.json` (cases "mutantA_destination_cell_only"
  / "mutantB_destination_disp_old_va", field "mutated_rows").

## Repository identity

- BASE_SHA (verified at run start): local HEAD == local origin/master ==
  actual remote master (git ls-remote) == `97bdf959cb742490a0e974bddf5a2dd25f93f5f7`.
- The actual remote master is re-verified immediately before the publication
  commit; any change ⇒ PERSISTENCE_BLOCKED_REMOTE_CHANGED (contract HARD STOP).
- Foreign untracked paths present at BASE (NOT touched by this run):
  `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`,
  `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/`,
  `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`,
  `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`,
  `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`,
  `experiments/`.
- Committed by this run (path-limited git add ONLY; never `git add .`):
  the new package `docs/audits/PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004/`
  and one AUDIT_ENTRYPOINT.md row. No historical package file was modified.

## Proprietary-byte census (honest scope)

No complete original proprietary binary/payload FILES were committed. Bounded
original byte windows / payload excerpts used as forensic evidence ARE present
(01_RAW/ORACLE_EVIDENCE.json byte windows of FUN_00730C90; the six instruction
pins) — the same class of bounded evidence already published by the historical
packages; no NEW proprietary payload beyond those bounded instruction windows.
