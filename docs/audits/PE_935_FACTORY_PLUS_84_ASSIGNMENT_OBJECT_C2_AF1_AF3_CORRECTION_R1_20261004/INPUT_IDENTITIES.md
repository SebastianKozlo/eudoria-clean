# INPUT_IDENTITIES.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004

All identities physically verified at run time (2026-10-04, executor session).
This is the C2 package's own INPUT_IDENTITIES. P3-C: the repository-owner typo
in the SOURCE_PACKAGE's INPUT_IDENTITIES is corrected HERE to the actual
canonical remote identity `SebastianKozlo/eudoria-clean` (verified this run
via `git remote get-url origin`); the historical file itself is READ-ONLY and
was NOT modified (the exact old->new wording is recorded in
SUPERSESSION_LEDGER.md S-C2-12).

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
| Repo | `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (remote `SebastianKozlo/eudoria-clean`, branch master) | `git remote get-url origin` = `https://github.com/SebastianKozlo/eudoria-clean.git` |
| BASE_SHA | `535e1a00fe793299dea7fc639e552560a6ac633b` | `git rev-parse HEAD`; `git rev-parse origin/master`; `git ls-remote origin master` (all three equal at dispatch preflight and at the pre-commit persistence check) |
| Untracked foreign paths (preserved, untouched) | `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`, `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/`, `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`, `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`, `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`, `experiments/` | `git status --porcelain` census matches the contract's declared foreign set exactly |
| SOURCE_PACKAGE (READ-ONLY historical) | `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/` | never modified; read for re-measurement baselines + the supersession quotecheck |
| Originating Desktop post-audit (READ-ONLY input) | `C:\Users\User\Documents\ChatGPT\PE\PE_935_FACTORY_PLUS_84_C1_DESKTOP_POST_AUDIT_20261004\REPORT.md` (15,908 B, SHA256 `DE533D49AEFD5B4ACAB5AE681B427B764D2A0D7BB2FAB41636671D97748A065F`) | the authoritative AF1/AF2/AF3 + P3-A/P3-B/P3-C finding definitions; re-hashed byte-identical to the contract pin |
| Output root | `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/` | verified NON-EXISTENT before the run (`Test-Path` = False); created fresh; never overwrites any historical package |

## PE image ground truth (own section-table mapper; no offset==RVA assumption)

| Field | Value |
|---|---|
| Image base | 0x00400000 |
| .text | VA 0x00401000, raw size 6,766,592 B |
| Machine | 0x014C (i386), 32-bit |

## Corrected instruments (03_SCRIPTS/)

| Script | Role | Outputs |
|---|---|---|
| `x86dec.py` | corrected fail-closed 32-bit x86 decoder; AF2 class-B/C/D fixes (0F C4/C5/C6 imm8; 67-prefix 16-bit ModRM; 66 E8/E9 rel16); segment prefixes recorded (P3-A); >5 prefixes / double segment prefix / unsupported far branches REJECTED | — |
| `pebnd.py` | PE loader + AF2-corrected boundary machinery: strong anchors only (KNOWN_FUNCTION_ENTRY with recorded ANCHOR_VA/ANCHOR_CLASS/EXISTING_PHYSICAL_EVIDENCE/EVIDENCE_SOURCE/EVIDENCE_STATUS), heuristic starts recorded but NEVER confirming, proven mid-instruction coverage REFUTES, corrected DIRECT CALL VALIDATION | — |
| `c1_pin_ledger.py` | F84-C1 authoritative same-VA pin ledger re-validation (133 preserved records, corrected machinery) | `CORRECTED_PIN_LEDGER.csv`, `01_RAW/C1_PIN_EVIDENCE.json` |
| `c2_census.py` | F84-C2 corrected census regeneration (byte grammar preserved; strong-anchor boundary policy; AF3-downgraded layout controls; derived family count) | `CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv`, `01_RAW/C2_CENSUS.json`, `AF3_PROVENANCE_LEDGER.csv` |
| `c3_object_scope.py` | F84-C3 object-scope facts with P3-A segment-aware store census | `01_RAW/C3_OBJECT_SCOPE.json` |
| `cqc_battery.py` | production QC Q1–Q14 (artifact-field re-derivation from the EXE) + causal mutation harness M1–M4 + AF3/Q8 + AF2 boundary counterexamples A–E | `01_RAW/CQC_DECODER_UNIT_TESTS.json`, `01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json`, `01_RAW/CQC_MUTATION_RESULTS.json`, `01_RAW/CQC_FINAL.json`, `AF1_MUTATION_MATRIX.csv`, `AF2_BOUNDARY_TEST_MATRIX.csv` |
| `make_manifest.py` | manifest generated LAST, self-excluded, bijection-verified + HANDOFF row-count consistency check | `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` |

QC re-execution hygiene: every instrument accepts `--out`/`--csv`/`--pkg-root`
overrides (defaults = this package), so an auditor re-run can redirect outputs
instead of overwriting committed evidence; reading the committed JSON/CSV is
the authoritative record of THIS run. `sys.dont_write_bytecode = True` in every
script (no `__pycache__`).

## Forbidden-input compliance (measured by the Q14 gate)

The instruments open ONLY: the pinned EXE + package-internal files (CSV/JSON
they generated) + the READ-ONLY historical C1 package files for the
supersession quotecheck + the final documents (report word checks). NO `.vfs` /
`.bnt` / `.nif` / `.ark` / network input appears in any instrument path census;
templates.vfs was NOT opened; RECORD_A untouched; no Model 194013 trace; no
client execution; no new function-discovery sweep; no class atlas.

## Run-time environment

- Executor host: Windows (local all-in-one environment), Python 3.12.10
  (`python` on PATH; `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`).
- No Ghidra, no client launch, no network, no VM SSH — STATIC-ONLY byte reads.
