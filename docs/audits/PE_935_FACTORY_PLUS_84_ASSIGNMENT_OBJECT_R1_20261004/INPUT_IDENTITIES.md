# INPUT_IDENTITIES.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004

All identities physically verified at run time (2026-10-04, executor session).

## Pinned EXE (the audited binary)

| Field | Value | Verification |
|---|---|---|
| Path | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | direct byte reads only; never launched |
| Size | 8,015,872 B | `Get-Item` + in-script `len(raw)` |
| SHA256 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` | `Get-FileHash` + in-script hashlib (S1/S2/S3 re-hash) |
| Pinned match | PASS (size + SHA256 both exact) | contract pin re-verified |

## Repository / baseline (eudoria-clean)

| Field | Value | Verification |
|---|---|---|
| Repo | `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (remote `SebastianKlo/eudoria-clean`, branch master) | |
| BASE_SHA | `288c53cc6b2552bbf9dc41907677e3fa1b6ab56d` | `git rev-parse HEAD`; `git rev-parse origin/master`; `git ls-remote origin master` (all three equal at dispatch; re-verified pre-commit) |
| Untracked foreign paths (preserved, untouched) | `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`, `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/`, `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`, `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`, `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`, `experiments/` | `git status --porcelain` census matches the contract's declared foreign set exactly |
| Output root | `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/` | verified NON-EXISTENT before the run (`Test-Path` = False); created fresh; never overwrites any historical package |

## PE image ground truth (own section-table mapper; no offset==RVA assumption)

| Field | Value |
|---|---|
| Image base | 0x00400000 |
| .text | VA 0x00401000, raw size 6,766,592 B |
| .rdata | VA 0x00677000 (vaddr 6,770,688) |
| .data | VA 0x0076C400 |
| Machine | 0x014C (i386), 32-bit |

All instruction identities in this package are byte reads from the pinned EXE at
image-base-relative VAs; every rel32 call target is machine-computed
(`call_va + 5 + rel32`), never hand-quoted. The S1 anchor battery initially caught
31 real pin VA slips in the executor's hand-decode notes (off-by-1/2/4) and 1 case
comparison bug; every slip was corrected and the battery re-run to 0 failures
(01_RAW/S1_ANCHORS.json `pin_checks.failures = []`, `fail_count = 0`).

## Predecessor packages used as READ-ONLY canon inputs

| Package | Used for |
|---|---|
| `PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004` | the consumer chain context (FUN_0070DCF0/C FUN_0070DC20/FUN_009777F0 pins); the writer VA canon (0x00977810) |
| `PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004` | the factory identity canon (singleton 0x00BA590C, vtable 0x00A870C4, ctor FUN_0073B820, base-init FUN_0070CF80 zeroes +0x84 @0x0070D013); the Candidate-A consumer gate (manager mode {1,2}); the lazy-init chain pins |
| `PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004`, `PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004`, `PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004` | the canonical predecessor state fields this contract requires preserved (C1/C2/S1/RECORD_A/B, the store-identity QC chain) — not reopened |

No historical package file was modified. The 5 foreign untracked packages + `experiments/`
were not touched.

## Instruments (03_SCRIPTS/)

| Script | SHA256 (hash-after-final-edit, before its execution) |
|---|---|
| `s1_identify_and_anchors.py` | recorded in `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` (manifest generated LAST, self-excluded) |
| `s2_write_census.py` | same |
| `s3_deep_chain.py` | same |
| `s4_qc_battery.py` | same |

All scripts are READ-ONLY vs the pinned EXE and all originals; they write only into
this package's `01_RAW/`, the census CSV, and `QC_REPORT`-supporting JSON under
`01_RAW/`. `sys.dont_write_bytecode = True` in every script (no `__pycache__`).
The scripts accept no `--out` overrides — all output paths are fixed inside the
package (QC re-execution hygiene: an auditor re-running them overwrites only THIS
package's 01_RAW JSON/CSV, never a committed historical evidence file; for
git-historical queries the auditor passes an explicit commit / uses
`git show <BASE_SHA>:<path>`).

## Run-time environment

- Executor host: Windows (local all-in-one environment), Python 3.12.10
  (`C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`).
- No Ghidra, no client launch, no network, no VM SSH — STATIC-ONLY byte reads.
