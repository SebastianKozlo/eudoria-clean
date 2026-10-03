# INPUT_IDENTITIES — PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003

All SHA256 values below were measured this run with `Get-FileHash` /
hashlib on the physical bytes. Sizes in bytes.

## Source oracle (pinned)

| input | path | size | SHA256 | verified |
|---|---|---:|---|---|
| GB 1.2.2 NiStream.cpp (the F1 semantics source) | `D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp` | 38,458 | `E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25` | at run start (matches contract pin) and re-verified at run end |

## Desktop findings source (read-only context; F1 fix spec, F2-F7 context only)

| input | path | SHA256 |
|---|---|---|
| Desktop post-audit REPORT.md (audited run PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 @ abc3f8f6; F1 finding used as the fix spec) | `C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_ORACLE_TOOL_DESKTOP_POST_AUDIT_20261003\REPORT.md` | `ECE2D4522CD18F37F52A084C7B1EAEAFAFAA8FE36A03ED6CC10CFB7639788193` |
| Desktop counterexample fixture (cross-validation reference; NOT copied — our own fx_B is byte-identical) | `...\COUNTERCHECKS\unused_unregistered_rtti.nif` | `BEDE862DC14BB84153392E409362C75BF1C78920C7C5A13721ED365CE38EEA09` |
| Desktop registered-only baseline fixture (cross-validation reference; our fx_A is byte-identical) | `...\COUNTERCHECKS\synthetic_valid_node.nif` | `48B24BB5100F424ABB266A8D10BB1F6C57A854C1960B53A46C27FEB901436984` |

## Synthetic fixtures (OUR bytes; built by 01_FIXTURES/build_fixtures.py)

REPO POLICY NOTE: the repo-wide `.gitignore` excludes `*.nif` by design
(zero NIF files are tracked anywhere in the repo; the published
PE_GAMEBRYO_ORACLE_TOOL run followed the same convention). The six
synthetic fixtures below are therefore NOT committed to the repo; the
committed `01_FIXTURES/build_fixtures.py` regenerates them
DETERMINISTICALLY byte-identically (the SHAs below are the verification
pins), and physical copies are preserved in this run's external sandbox:
`D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003\sandbox\01_FIXTURES\`.
During the run the fixtures were executed from the package directory
`01_FIXTURES\` (the raw-test records' `command` fields reference those
execution-time paths). All fixtures are 100% OUR OWN synthetic bytes; zero
proprietary content.

| fixture | size | SHA256 | role |
|---|---:|---|---|
| `fx_A_registered_only.nif` | 167 | `48B24BB5100F424ABB266A8D10BB1F6C57A854C1960B53A46C27FEB901436984` | test A registered-only baseline (byte-identical to the Desktop's independent fixture) |
| `fx_B_unused_unregistered.nif` | 179 | `BEDE862DC14BB84153392E409362C75BF1C78920C7C5A13721ED365CE38EEA09` | test B — the F1 counterexample (byte-identical to the Desktop's independent fixture) |
| `fx_C1_trailing_unknown_run.nif` | 196 | `F9BFA6A6227F78E027B34EA7D3D89FA52FBBEDC9DF6A369BD7FED40301952F0E` | table-vs-object-order with a TRAILING unknown run: documents the PRE-EXISTING presolver boundary crash (Desktop F4 territory, out of scope; exits 1 both pre- and post-fix under --full-decode); the minimal regression input for a future F4 fix |
| `fx_C2_table_vs_object_order.nif` | 286 | `3FFCA2BDC4B215B9B3E4ECEED5AC1DB97F17F4C77E10D6790498C8A29C257649` | test C — first miss by TABLE order, object order meets NiQuuxzyx first; middle unknown run (standard shape; full-decode extension works) |
| `fx_E_incomplete_indices.nif` | 179 | `CEE7ABF48A0A992261095CA3C080E2E3C7E3CD45AC357C0726AA0ADBFEF03EC6` | test E — unused first table miss + incomplete later object indices |
| `fx_F_truncated_later_name.nif` | 79 | `B171020E150D3E425296585FA1ECBAFB5569136358FFBC8DDEDCC46C11A4102F` | test F — first table miss + truncated later RTTI name |

## Real payload (test G; read-only sandbox of the published run)

| input | path | size | SHA256 | pin match |
|---|---|---:|---|---|
| 218757.nif (T1) | `D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads\218757.nif` | 57,316 | `3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36` | byte-identical to the published run pin (inspect_T1_gb12_full.json input_identity) |
| T1 copy for the mutation-control battery (temp, outside repo) | `C:\Users\User\AppData\Local\Temp\opencode\f1_run\218757_copy.nif` | 57,316 | `3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36` | same bytes as above |

## Regression comparison baselines (committed artifacts of the published run)

| input | path | role |
|---|---|---|
| `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/T_runs/inspect_T1_gb12_full.json` | published T1 full-decode oracle result (66/66 decoded, rtti_gate, histogram, transforms) — the byte-value regression baseline for test G |
| `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/T_runs/inspect_T1_gb12_orig.json` | published T1 ordinary-mode oracle result — the ordinary-mode metadata comparison baseline |

## Code identity

| item | value |
|---|---|
| BASE_SHA (run start = run end for the base) | `abc3f8f6f9e35dd8aebbe2cfe525d710e4338acd` (local HEAD = local origin/master = actual remote master, verified at dispatch and re-verified before push) |
| Modified tool files (the F1 change set) | `tools/gamebryo_oracle/gb12core.py`, `tools/gamebryo_oracle/schemas/oracle_result.schema.json`, `tools/gamebryo_oracle/tests/test_gb12.py`, `tools/gamebryo_oracle/README.md` |
| Registry | `tools/gamebryo_oracle/adapters/gb12/registry.py` — UNCHANGED (verified via empty `git diff`) |
| Legacy inline-RTTI layout (< 5.0.0.1) | NOT migrated (verified via the diff hunk map: no hunks outside the b_new block + doc blocks) |
