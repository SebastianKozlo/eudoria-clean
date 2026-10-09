# INPUT_IDENTITIES — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

All values MEASURED in this run's preflight (fail-closed). Any critical mismatch
would have meant BLOCKED before science or correction work. All hashes SHA256,
uppercase hex unless noted. Sizes in bytes.

## 1. Contract and run identity

| Item | Value | Status |
|---|---|---|
| CONTRACT path | `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md` | — |
| CONTRACT size / SHA256 | 16623 / `61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CBE36F36D3981` | MATCH (expected 16623 / 61AAA558…) |
| RUN_ID | `PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009` | — |
| RUN_CLASS | `MACHINERY_AND_CONTROL_CORRECTION` | — |
| FINDING under correction | CMO-C1 / P2 (Desktop post-audit of the source package) | — |

## 2. Repository state (fail-closed preflight)

| Item | Measured | Expected | Status |
|---|---|---|---|
| local HEAD | `34fc34749464de3e05527088ed46be9e215f1964` | `34fc347…` | MATCH |
| origin/master | `34fc34749464de3e05527088ed46be9e215f1964` | `34fc347…` | MATCH |
| actual remote master (live `git ls-remote origin master`) | `34fc34749464de3e05527088ed46be9e215f1964` | `34fc347…` | MATCH |
| tracked working tree | clean (zero modified/staged tracked files) | clean | PASS |
| OUTPUT_ROOT before work | ABSENT | absent | PASS (created only after preflight PASS) |

Foreign untracked census (recorded, LEFT INTACT, not part of this run):

```
docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/      (8 files)
docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/ (14 files)
docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/       (6 files incl. 1 .pyc)
docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/           (6 files)
docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/ (large foreign package)
experiments/                                                   (eu1030 experiments)
```

## 3. Target binary (READ-ONLY; re-pins of approved windows only)

| Item | Measured (preflight) | Expected | Status |
|---|---|---|---|
| EXE path | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | — | — |
| EXE size | 8015872 | 8015872 | MATCH |
| EXE SHA256 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` | same | MATCH |

EXE re-hash AFTER all EXE-touching work: recorded in POST_COUNTEREXAMPLES.json
(`exe_identity_post`); must equal the preflight value (acceptance gate 7).

## 4. Mandatory source inputs (at BASE 34fc347…; ALL identity-verified)

Source package root: `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/`

| File (repo-relative) | Size | SHA256 | Expected | Status |
|---|---|---|---|---|
| `…/03_SCRIPTS/repin_write_provenance.py` | 34043 | `45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931` | 34043 / 45120C91… | MATCH |
| `…/03_SCRIPTS/qc_remeasure.py` | 31970 | `4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A` | 31970 / 4E5426AE… | MATCH |
| `…/CONTROL_RESULTS.json` | 18509 | `9545D0D78881C29BC805EA3A05C8AA936D364256671D31A1AE907677A63DE2F8` | 18509 / 9545D0D7… | MATCH |
| `…/QC_RESULTS.json` | 31350 | `DE7DF210FAFA465E27D7A7C4410C9D9C44C9BAE1492B9FEDE2B3101F01BF0545` | 31350 / DE7DF210… | MATCH |

## 5. Contextual inputs (independently measured; identity recorded)

| File | Size | SHA256 | Role |
|---|---|---|---|
| `…/FINAL_REPORT.md` | 15589 | `FF5FDBD2F54F20E3026B5992F7BCC411B0572ADA249F157BA11CB441E1AC83E0` | source final report (read in full) |
| `…/CLAIM_MATRIX.csv` | 9721 | `1D32AADEFFAAA177DC9B48165B612F0D4882B29B7BFB27D03AD9AA62C425254D` | source claim matrix (read in full) |
| `…/MANIFEST_SHA256.csv` | 5368 | `5F1CAE01E98F4C0A317D70F51032DEBFB3D50CD5C7B38DF43042E7CE9E0310B5` | source manifest (read; format/coverage reference) |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` | 8339 | `DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845` | J3 SUPERSESSION (read in full; statuses carried verbatim) |
| `AUDIT_ENTRYPOINT.md` (repo root) | 269640 | `E707FCB7B52B8BDF27590063E2F5592A8E1925C025D3B1A8BFDE355384788644` | governance input (read; NOT written by this run) |

Notes:
- The source FINAL_REPORT/CLAIM_MATRIX/MANIFEST hashes measured here are also
  cross-checkable against the source package's own committed MANIFEST_SHA256.csv
  rows (ff5fdbd2…, 1d32aade…, and the manifest's self-exclusion convention) —
  consistent.
- The J3 SUPERSESSION.md identity equals the source CLAIM_MATRIX CL-08 pinned
  identity (DD11137A…) — consistent.
- The Desktop post-audit report/REPLAY_RESULTS of the independent Desktop audit are
  used ONLY as counterexample specifications (as permitted by the contract §2);
  no Desktop path is required or claimed to exist locally; no Desktop evidence is
  fabricated. The reproduction is this run's own PRE measurement.

## 6. Historical key evidence values (from the immutable source records; used as PRE expectations)

From source CONTROL_RESULTS.json (SHA256 9545D0D7…, verified above):

- W1 window: VA 0x0085B1A8, len 232, raw file offset 4567464; the committed W1 hex
  is re-verified byte-identically against this run's own physical EXE read (PRE
  gate W1_BYTE_IDENTITY).
- Boundary decode: instruction_count = 64; total_bytes = 224;
  reached_end_exact = true (0x0085B290).
- 0x0085B24D = `D9 E8` (fld1) — the mutation site.
- `ecx_writers_between_24B_and_27A = []` (the historical clean true-empty scan).
- Selected store 0x0085B281 = `89 4E 44` (mov [esi+0x44], ecx; 32-bit; raw offset
  4567681); copy triple 0x0085B281/0x0085B287/0x0085B28D; zero-init triple
  0x0085B1E4/0x0085B1E7/0x0085B1EC.
- Value chain pins: 0x0085B1DA `8B 7C 24 14`; 0x0085B24B `8B CF`; 0x0085B27A
  `E8 E1 B2 EE FF` (target recomputed 0x00746560); 0x0085B27F `8B 08`;
  accessor 0x00746560 `8D 41 08 C3`.
- Receiver chain pins: 0x0085B1B7 `8B F1`; 0x0085B1C1 `C7 06 4C 1E A9 00`;
  caller 0x00528E76 `8B F1`, 0x00528E8B `8B CE`, 0x00528E8D `E8 1E 23 33 00`
  (target recomputed 0x0085B1B0), 0x00528EA2 `C7 06 B0 DC A7 00`.
- RTTI: vtable 0x00A91E4C → COL 0x00AB33D0 → TD 0x00B7997C →
  `.?AVMovableObject@@`; vtable 0x00A7DCB0 → COL 0x00AA17CC → TD 0x00B79958 →
  `.?AVClientMovableObject@@` (both col_sig 0).

## 7. Executed-by list (this run's own writes; see PREREGISTRATION section 7)

This run writes ONLY under OUTPUT_ROOT
(`docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/`).
No source-package file, no EXE file, no AUDIT_ENTRYPOINT.md, no runtime file is
modified. No stage/commit/push in this phase (parent persistence phase).
