# INPUT_IDENTITIES.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004

All identities physically verified at run time (2026-10-04, executor session).

## Pinned EXE (the audited binary — byte reads only; never launched)

| Field | Value | Verification |
|---|---|---|
| Path | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | read-only byte reads in c1/c2/c3/cqc |
| Size | 8,015,872 B | `Get-Item` + in-script `len(raw)` |
| SHA256 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` | `Get-FileHash` + in-script hashlib (c1/c2/c3/cqc re-hash) |
| Pinned match | PASS (size + SHA256 both exact) | contract pin re-verified |

## Repository / baseline (eudoria-clean)

| Field | Value | Verification |
|---|---|---|
| Repo | `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (remote `SebastianKlo/eudoria-clean`, branch master) | |
| BASE_SHA | `a0e176803aed23b19040d4310de1668efec4511f` | `git rev-parse HEAD`; `git rev-parse origin/master`; `git ls-remote origin master` (all three equal at dispatch and at pre-commit verification) |
| Untracked foreign paths (preserved, untouched) | `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`, `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/`, `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`, `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`, `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`, `experiments/` | `git status --porcelain` census matches the contract's declared foreign set exactly |
| SOURCE_PACKAGE (READ-ONLY historical) | `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/` | never modified; read only by the QC quotecheck |
| Output root | `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/` | verified NON-EXISTENT before the run (`Test-Path` = False); created fresh; never overwrites any historical package |

## PE image ground truth (own section-table mapper; no offset==RVA assumption)

| Field | Value |
|---|---|
| Image base | 0x00400000 |
| .text | VA 0x00401000, raw size 6,766,592 B |
| Machine | 0x014C (i386), 32-bit |

## Corrected instruments (03_SCRIPTS/)

| Script | Role | Outputs |
|---|---|---|
| `x86dec.py` | corrected fail-closed 32-bit x86 decoder (shared module; opens no files) | — |
| `pebnd.py` | PE loader + DECLARED trusted boundary machinery (T1 known entries, T2 CC-padding-delimited, T3 RET-delimited) + DIRECT CALL VALIDATION | — |
| `c1_pin_ledger.py` | F84-C1 authoritative same-VA pin ledger (133 records) | `CORRECTED_PIN_LEDGER.csv`, `01_RAW/C1_PIN_EVIDENCE.json` |
| `c2_census.py` | F84-C2 corrected census (byte-by-byte, 9 declared families) | `CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv`, `01_RAW/C2_CENSUS.json` |
| `c3_object_scope.py` | F84-C3 bounded machine vptr search + object-scope facts + P3 size pins | `01_RAW/C3_OBJECT_SCOPE.json` |
| `cqc_battery.py` | fresh QC gates Q1-Q14 + negative controls A-F + decoder unit battery + supersession quotecheck | `01_RAW/CQC_DECODER_UNIT_TESTS.json`, `01_RAW/CQC_NEGATIVE_CONTROLS.json`, `01_RAW/CQC_FINAL.json` |
| `make_manifest.py` | manifest generated LAST, self-excluded | `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` |

QC re-execution hygiene: every instrument accepts `--out`/`--csv` overrides
(defaults = this package), so an auditor re-run can redirect outputs instead
of overwriting committed evidence; reading the committed JSON/CSV is the
authoritative record of THIS run. `sys.dont_write_bytecode = True` in every
script (no `__pycache__`).

## Forbidden-input compliance (measured by corrected gate Q14)

The instruments open ONLY: the pinned EXE + package-internal files (CSV/JSON
they generated) + the READ-ONLY historical package files for the supersession
quotecheck. NO `.vfs` / `.bnt` / `.nif` / `.ark` / network input appears in
any instrument path census; templates.vfs was NOT opened; RECORD_A untouched;
no Model 194013 trace; no client execution.

## Run-time environment

- Executor host: Windows (local all-in-one environment), Python 3.12.10
  (`python` on PATH; `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`).
- No Ghidra, no client launch, no network, no VM SSH — STATIC-ONLY byte reads.
