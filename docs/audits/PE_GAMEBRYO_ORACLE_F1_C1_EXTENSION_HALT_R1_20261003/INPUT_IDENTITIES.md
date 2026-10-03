# INPUT_IDENTITIES — PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003

All SHA256 values below were measured this run with `Get-FileHash` /
hashlib on the physical bytes. Sizes in bytes.

## Source oracle (pinned)

| input | path | size | SHA256 | verified |
|---|---|---:|---|---|
| GB 1.2.2 NiStream.cpp (the RTTI-table semantics source) | `D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp` | 38,458 | `E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25` | at run start (matches the pinned contract SHA; L70 `MAX_RTTI_LEN = 256` + L1150 `assert(uiLength > 0 && uiLength < MAX_RTTI_LEN)` re-read this run) |

## Desktop findings source (read-only context; the F1-C1 fix spec)

| input | path | SHA256 |
|---|---|---|
| Desktop post-audit REPORT.md (audited commit 60a73d9; finding F1-C1/P2 used as the fix spec; verdict REQUIRE_CORRECTIONS) | `C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_ORACLE_F1_DESKTOP_POST_AUDIT_20261003\REPORT.md` | `6BD89E93DBD07E8336AD545B287EC68B4DC3EE0C57F589E05C4CB9115FB9205F` |

## Synthetic fixtures (OUR bytes; built by 01_FIXTURES/build_fixtures_c1.py)

REPO POLICY NOTE: the repo-wide `.gitignore` excludes `*.nif` by design
(zero NIF files are tracked anywhere in the repo; the published
PE_GAMEBRYO_ORACLE_TOOL and F1_RTTI_CORRECTION runs followed the same
convention). The three synthetic fixtures below are therefore NOT committed
to the repo; the committed `01_FIXTURES/build_fixtures_c1.py` regenerates
them DETERMINISTICALLY byte-identically (the SIZE + SHA256 below are the
verification pins), and physical copies are preserved in this run's
external sandbox: `D:\Eudoria_Reconstruction\99_Audits\
PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003\sandbox\01_FIXTURES\`.
During the run the fixtures were executed from the package directory
`01_FIXTURES\` (the raw-test records' `command` fields reference those
execution-time paths). All fixtures are 100% OUR OWN synthetic bytes;
zero proprietary content.

| fixture | size | SHA256 | role |
|---|---:|---|---|
| `fx_C1A_truncated_name_indexlike.nif` | 94 | `928A1447A3F6911DAD96495307AAA97340133186223AA3B4288CFB4E493A5FCF` | counterexample class A — truncated later RTTI name + index-like leftover bytes. Byte-identical to the Desktop auditor's own counterexample 1 (`truncated_name_remaining_index2_bounded127.nif`, 94 B / SHA `928A1447...` per the Desktop report): both were constructed from the same pinned-source description (NiNode, NiDesktopFirstMissing, third name length 127, 2 leftover bytes `02 00`), cross-validating the byte construction against the independent auditor's fixture. PRE-FIX full-decode: IndexError traceback, empty stdout, exit 1 (raw: `02_RAW_TESTS/PRE_FIX_C1A_full_decode.RECORD.json`). |
| `fx_C1B_truncated_name_fake_body.nif` | 196 | `719A7EB36E9D2B80E648A03C39C1D5A164586D4AC1532F6F0ACE681FB1C382D6` | counterexample class B — truncated later RTTI name + fake-body-like leftover bytes. Byte-identical to the Desktop auditor's own counterexample 2 (`truncated_name_remaining_fake_body_bounded127.nif`, 196 B / SHA `719A7EB3...` per the Desktop report). PRE-FIX full-decode: spurious NiNode object + histogram/census/groups/roots=[0] reconstructed out of the unfinished name's bytes (raw: `02_RAW_TESTS/PRE_FIX_C1B_full_decode.RECORD.json`). |
| `fx_F_truncated_later_name.nif` | 79 | `B171020E150D3E425296585FA1ECBAFB5569136358FFBC8DDEDCC46C11A4102F` | byte-identical regeneration of the published F1-run fixture F (same SIZE + SHA256 as the `PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003` INPUT_IDENTITIES pin); used only for THIS run's F-fixture --full-decode delta record (the halt now happens AT the table failure instead of at the object-index stage) without touching the historical package. |

Fixture derivation basis (independent of the adapter under correction):
pinned NiStream.cpp LoadHeader L303-360 / LoadRTTI L412-449 /
LoadRTTIString L1145-1153 (u32 length + bytes) / L70 + L1150
(`0 < uiLength < MAX_RTTI_LEN=256` — the declared length 127 is
source-valid) / LoadObjectGroups L470-487 / LoadTopLevelObjects L367-385;
NiObject.cpp GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114; NiObjectNET.cpp /
NiAVObject.cpp / NiNode.cpp per-class field sequences for 10.1.0.0.
Registry assumptions verified this run: "NiNode" IS registered (198-class
SDM census), "NiDesktopFirstMissing" is NOT registered (synthetic name).

## Real payload (T1 regression; read-only sandbox of the published run)

| input | path | size | SHA256 | pin match |
|---|---|---:|---|---|
| 218757.nif (T1) | `D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads\218757.nif` | 57,316 | `3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36` | byte-identical to the contract pin (T1 PHYSICAL IDENTITY verified at run start); only READ, never modified |
| T1 copy for the mutation-control battery (temp, outside repo) | `C:\Users\User\AppData\Local\Temp\opencode\f1c1_run\218757_copy.nif` | 57,316 | `3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36` | same bytes as above |

## Regression comparison baselines (committed artifacts)

| input | path | role |
|---|---|---|
| `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/T_runs/inspect_T1_gb12_full.json` (71,733 B, SHA256 `E86AAAB65CFF26FC11E07E81DF403C6E0C26922FC72BD001C3BC0FB0ABDF77B9`) | published T1 full-decode oracle result — the pinned `objects[]` deep-regression baseline for the 66-record comparison |
| `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/T_runs/inspect_T1_gb12_orig.json` | published T1 ordinary-mode oracle result — the ordinary-mode verdict baseline |
| `docs/audits/PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003/02_RAW_TESTS/AFTER_FIX_G_T1_218757_full_decode.RECORD.json` | the 60a73d9-era T1 full-decode CLI record — the whole-JSON byte-identity baseline (stronger than objects[]: the F1-C1 fix adds ZERO output on non-halt paths) |
| `docs/audits/PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003/02_RAW_TESTS/AFTER_FIX_G_T1_218757_ordinary.RECORD.json` | the 60a73d9-era T1 ordinary-mode CLI record — ordinary-mode byte-identity baseline |

## Code identity

| item | value |
|---|---|
| BASE_SHA | `60a73d9b0cc438b2cf71eed827b28f2806fc03e5` (local HEAD = local origin/master = actual remote master, verified at run start; re-verified before push) |
| Modified tool files (the F1-C1 change set) | `tools/gamebryo_oracle/gb12core.py`, `tools/gamebryo_oracle/schemas/oracle_result.schema.json`, `tools/gamebryo_oracle/tests/test_gb12.py`, `tools/gamebryo_oracle/README.md` |
| Registry | `tools/gamebryo_oracle/adapters/gb12/registry.py` — UNCHANGED (not in the modified set; verified via git status) |
| Legacy inline-RTTI layout (< 5.0.0.1) | NOT migrated (gb12core.py diff hunk map: 4 hunks, all inside the b_new RTTI region + the header doc block; no hunks in the legacy branch, index stage, groups read, body decode, presolver or link phase) |
| Historical package `PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003` | READ-ONLY (not modified by this run; the fx_F fixture was REGENERATED byte-identically in THIS package instead of touching the historical one) |
