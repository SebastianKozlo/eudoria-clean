# INPUT_IDENTITIES — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

All identities measured this run (Windows PowerShell 5.1 host side; WSL
PE-AI for gate execution). Every input was verified BEFORE any correction
work and re-verified after (see I9).

## I1. Authorizing contract (dispatch)

- Path: `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_BR_C1_CORRECTION_PROMPT_REVIEW_20261009\OPENCODE_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009.md`
- Size: 18566 B
- SHA256: `B30E807BFA24BC37A8FFC015D37B42EC96F72F47D8B6956AFA9512D09CDC1CE3`
- Read IN FULL before any action; measured bytes MATCH the human dispatch
  message. Authorization: the separate human message (2026-10-09) naming
  this exact contract and authorizing this correction-only run plus its
  allowlisted commit/fast-forward push. NEXT_EXPERIMENT_AUTHORIZED = NO.

## I2. Methodological input (predecessor contract, required reading)

- Path: `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_PROMPT_REVIEW_20261009\OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md`
- Size: 23187 B, SHA256 `773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07` — MATCH.

## I3. Desktop post-audit inputs (map to reproduce, not an oracle)

Under `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_SECOND_PASS_20261009\`:

| File | Size bytes | SHA256 | Match |
|---|---:|---|---|
| REPORT.md | 5843 | `FA6D8C437FC3767AF33C292924AFBF4180430DF3429EA7932A0CA23FA3658864` | MATCH |
| AUDIT_COUNTERCHECKS.json | 147780 | `60DE66C2F567550C49CC638B232575DEBA05C547228486B1CADE56BB3E38720A` | MATCH |
| SECOND_PASS_VERIFICATION.json | 894 | `7259B582010593A77DCBC8039F35F1A8A7202C5C3AC96D71D9ECEA89EBFF265D` | MATCH |

The Desktop verdict (POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS_IN_
MACHINERY_SCOPE; BR_C1 = CONFIRMED_OPEN_P2; 8 false-PASS outcomes) was used
as the defect MAP; the PRE reproduction below re-derived everything through
the ACTUAL predecessor gates. No Desktop expected verdict was fed into any
gate derivation.

## I4. Predecessor package (SOURCE_REPO_PATH, read-only)

`docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/` at
EXPECTED_BASE_SHA `2ac7cfa1dcb2e53e9c86985c18377de811d5b485`.

- Full before/after inventory: all 35 physical files hashed BEFORE any work
  and AFTER all work — 35/35 IDENTICAL (the driver records
  `source_package_unchanged: true` for every phase; see DRIVER_RUN_SUMMARY.json
  and the phase result files).
- All 35 physical files equal their committed Git blobs at BASE_SHA
  (git hash-object vs git ls-tree: 35/35 MATCH, 0 mismatches).
- Contract-pinned subset:

| File (relative) | Size bytes | SHA256 | Match |
|---|---:|---|---|
| MANIFEST_SHA256.csv | 8306 | `D37B5B575D250C8B7A958A9AF960A9FE43F8992B7EB621FED5118CAE44146CC0` | MATCH |
| 03_SCRIPTS/run_frame_bridge.py | 103544 | `0DB331D85526333EB91B12E480B4D57A7C32BE6FE0B0611B20E4938FA038268B` | MATCH |
| 03_SCRIPTS/qc_frame_bridge.py | 83103 | `EC9F3FBE152E7694B0E2540E1BB4F399994BBAB81CE8B33B64495B25A3CE1688` | MATCH |
| BRIDGE_PROVENANCE.json | 32219 | `ADBA8BF873A4BA41755DA7D5CFCF2AC80F2E5B6131E54BA1CB7BF44868947D9F` | MATCH |

- Predecessor physical file count: 35 (34 package files + MANIFEST_SHA256.csv
  is included in the 34? — measured: the predecessor has 35 physical package
  files; its manifest has 34 package rows plus one AUDIT_ENTRYPOINT row).
  Read in full this run: FINAL_REPORT, PREREGISTRATION, ARTIFACT_CONTROL_
  RESULTS, CONTROL_RESULTS, QC_RESULTS, QC_REPORT, HANDOFF, EVIDENCE_INDEX,
  SUPERSESSION_AND_STANDING, PE_MASTER_REVIEW, INPUT_IDENTITIES, both ledgers,
  CLAIM_MATRIX, WINDOW_IDENTITIES, both scripts, BRIDGE_PROVENANCE (all 35
  files walked and hashed; the load-bearing documents were read in full).

## I5. Package input copy

`01_INPUTS/BRIDGE_PROVENANCE.json` in THIS package is a byte-identical copy
of the predecessor input (SHA256 `ADBA8BF8...`, size 32219 B), explicitly
labeled a PREDECESSOR INPUT (not a fresh derivation of this run).

## I6. EXE (read-only original)

- Path: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
- Size: 8015872 B, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — MATCH (re-hashed before and after every driver phase; UNCHANGED).
- EXE inspection scope this run: whole-file hashing + the two EXISTING
  windows only — A `[0x00528E50,0x00528E92)` (66 B, raw 1216080, SHA256
  `F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85`) and
  B `[0x004C4792,0x004C47C6)` (52 B, raw 804754, SHA256
  `B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A`)
  — replay/verify of already-derived facts only (both windows re-read by
  the gates' identity checks and the byte-matrix helpers; every read
  verified against the pinned SHA256). No new region, function body,
  callee, xref or pointee exploration. PE-header/section mapping NOT
  re-derived this run (existing predecessor mapping consumed as-is; the
  gates verify raw offsets + window SHAs against the physical EXE bytes).

## I7. Tool identities

- Disassembler: GNU objdump (GNU Binutils for Debian) 2.44 via WSL PE-AI
  (kernel 6.18.33.2-microsoft-standard-WSL2), python3 3.13.5, `python3 -B`
  (no .pyc). The SAME disassembler as the predecessor run and as its QC —
  the same GNU objdump is NOT two independent disassemblers (honest; not
  claimed as a cross-disassembler check).

## I8. Environment / session origin

- Executor: OpenCode agent pe-reconstruction, model `nask-glm/glm-5-3`.
- Git triple at preflight: LOCAL_HEAD == origin/master == 2ac7cfa1dcb2e53e
  9c86985c18377de811d5b485 == EXPECTED_BASE_SHA. Foreign untracked paths
  recorded and UNTOUCHED: docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_
  20261001/, PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/, PE_935_P1_CLOSURE_EXTERNAL_
  QC_20260930/, PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
- Both proposed output paths ABSENT before the run (OUTPUT_ROOT and
  OUTPUT_REPO_PATH verified non-existent).

## I9. Post-work re-verification

After all correction/control/regression execution:
- EXE SHA256 UNCHANGED (`E7785430...`, measured after every phase).
- Predecessor source package: 35/35 files byte-identical to the before-run
  inventory (source_package_unchanged = true in DRIVER_RUN_SUMMARY.json).
- No writes to the predecessor package, no CLI main executed, no Desktop
  script executed; every driver write went to OUTPUT_ROOT (PACKAGE results,
  SCRATCH fixtures).
