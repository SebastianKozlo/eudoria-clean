# INPUT_IDENTITIES — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

Executor phase: pe-reconstruction (bounded worker under direct PE-MASTER
dispatch; NO_NESTED_TASKS). Every identity below was MEASURED in this session
by the executor before the dependent action; all hex digests are uppercase.

## 0. The frozen contract (the authorization instrument)

```text
path     = C:\Users\User\Downloads\OPENCODE_PLUS4_RESIDUAL_CORRECTION_R1_20261008.md
size     = 23137 bytes (measured, matches the dispatched expectation)
sha256   = 2634BA31C4002B636E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969
lines    = 172 LF-terminated lines (the file ends with LF; a naive split on
           LF yields 173 elements including the empty tail element — the
           full line count is 172)
read     = IN FULL, first to last line, BEFORE any work (RUN_CLASS
           RECORDS_AND_QC_MACHINERY_CORRECTION; correction-only)
modified = NO (the contract file was not touched by this run)
```

## 1. Repository preflight (fail-closed; performed BEFORE OUTPUT_ROOT creation)

```text
EXPECTED_BASE_SHA = 0b94c487ba11869b811aada188bfabaf8972728a
git rev-parse HEAD                                  -> 0b94c487ba11869b811aada188bfabaf8972728a
git fetch origin; git rev-parse origin/master       -> 0b94c487ba11869b811aada188bfabaf8972728a
git ls-remote origin refs/heads/master (live)       -> 0b94c487ba11869b811aada188bfabaf8972728a
triple-BASE verdict                                 -> PASS (all three equal, no fuzzy
                                                       short-SHA comparison)
tracked dirty changes at preflight                  -> NONE (git status --porcelain=v1
                                                       showed only foreign UNTRACKED
                                                       paths)
OUTPUT_ROOT existed at preflight                    -> NO (Test-Path = False; created
                                                       only after the preflight PASS)
reset/amend/rebase/cherry-pick/force-push/auto-merge -> NONE performed
```

Foreign untracked paths recorded at preflight (left INTACT, untouched):

```text
docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
experiments/
```

## 2. Desktop adversarial corpus (REQUIRED physical local file)

```text
path    = C:\Users\User\Documents\ChatGPT\PE\PE_PLUS4_CORRECTION_DESKTOP_POST_AUDIT_0B94C48_20261008\ADVERSARIAL_COUNTERCHECKS.json
size    = 16079 bytes (measured; matches the contract expectation)
sha256  = 62646637C323E0BAEAD371A0AE979D1F92DD2752B60C9D402E70A5A8FA38837B
lines   = 649
read    = parsed and READ IN FULL before work (9 cases: 2 partial-overlap
          false-passes, 2 PE32-boundary false-passes, 4 truncation escapes,
          1 wrong-callsite false pass 86/86 with the full result listing)
REPORT.md note = the Desktop directory has NO REPORT.md; none was required,
          invented or synthesized (the governing findings are restated in
          the contract §§2–5)
```

## 3. Physical PCG source identity (READ ONLY)

```text
path    = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
size    = 8015872 bytes (measured; matches the contract expectation)
sha256  = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
rehash  = BEFORE all reads (preflight) and AGAIN after all controls
          (the POST runner records exe_after_post unchanged = true; the
          executor independently re-hashed after the final run — see §7)
policy  = reads limited to the contract classes (PE headers, the pinned
          byte/rel32/COL/TypeDescriptor/name/string ranges, the 5 W-ctor
          bytes); NO disassembly expansion, NO new RE, no committed
          proprietary bytes beyond small pins/provenance
```

## 4. SOURCE_RUN package census (READ_ONLY, at BASE 0b94c48)

Physical Git tree comparison (`git ls-tree -r --long HEAD` on the package
path) and a physical working-tree hash of EVERY file — both methods agree:
**22 physical files** (the package numbers are not treated as truth without
this physical comparison). Source manifest Git blob SHA1 verified:
`git ls-tree` shows MANIFEST_SHA256.csv = blob
`60e8318e90a76e6d0a85365d9080a89f33bdd1bf` — MATCHES the contract pin.

All ten load-bearing pinned rows verified SIZE+SHA256 (contract §1.4):

| pin | size | sha256 (measured) | verdict |
|---|---|---|---|
| ACTIVE_CORRECTED_PINS.json | 4835 | 64C64DA9D59CEEC25C72D1890C89E38935BB21530D8E3ED8B90537B98705001F | MATCH |
| 03_SCRIPTS/checker_plus4_successor.py | 30167 | F50DDC40F4780FB4431C8B08808F3A5E74DBECD91398A1AC0977556744FBAF45 | MATCH |
| 03_SCRIPTS/qc_countercheck.py | 40309 | 11957F40F7D067E4E422D86E630599142AFBB073F843CEBDB92216E382CB0870 | MATCH |
| 03_SCRIPTS/run_correction_controls.py | 39340 | 18F5B0459F03B07CD46E63BB3D61D7380F7F40735885BB9377E2A6AB81ACF5C3 | MATCH |
| CORRECTED_CLAIM_MATRIX.csv | 9388 | BDEBB76270FB2E49138CDBDEB634A8904C00ABC821FCBC0002F6B6C0BCACD8A5 | MATCH |
| SUPERSESSION_LEDGER.csv | 21592 | 11DAFC8E4A9600D3D7A10B1C147BAED7FA09F517A894592404B35448F9160B3E | MATCH |
| MAPPER_RESULTS.json | 14941 | A7690860F9519B9F48BF834813B242EC6CB8A1097032323F2F89E97D796BAE9F | MATCH |
| REGRESSION_RESULTS.json | 6607 | A9642BB669514D2AE0B6ABC8EECDA30A863CDA384F904671A05D66D530A481E1 | MATCH |
| QC_RESULTS.json | 23334 | 1185FCB64D345A73ED56D7A58F1A4806BC657E63B81CFF918D9E900A36E84DBD | MATCH |
| AUDIT_ENTRYPOINT.md (repo root) | 263460 | 87FF331453E5643407C7428B6C43EE6898A22E33379AF2EC3812A01ADD287C01 | MATCH |

Full 22-file census (working-tree hash; sizes agree with the Git tree):

| path (under the package) | size | sha256 |
|---|---|---|
| 00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_RAW.json | 14793 | 2037509BCD3EC0C76163DBB320A06BD9C98CB04769960EAB017DF026EFFC23BE |
| 03_SCRIPTS/checker_plus4_successor.py | 30167 | F50DDC40F4780FB4431C8B08808F3A5E74DBECD91398A1AC0977556744FBAF45 |
| 03_SCRIPTS/qc_countercheck.py | 40309 | 11957F40F7D067E4E422D86E630599142AFBB073F843CEBDB92216E382CB0870 |
| 03_SCRIPTS/run_correction_controls.py | 39340 | 18F5B0459F03B07CD46E63BB3D61D7380F7F40735885BB9377E2A6AB81ACF5C3 |
| ACTIVE_CORRECTED_PINS.json | 4835 | 64C64DA9D59CEEC25C72D1890C89E38935BB21530D8E3ED8B90537B98705001F |
| AUTHORIZATION_RECORD.md | 4711 | 24C9E1F6C426CD6E1DE4121F48A293748671012370988D85D568DA59E2319C9F |
| BODY_SCOPE_REASSESSMENT.csv | 3305 | FDD375AB420EDA21F7DB3669E167C600A50B705006CA92C431C8C52F4979FCCD |
| CORRECTED_CLAIM_MATRIX.csv | 9388 | BDEBB76270FB2E49138CDBDEB634A8904C00ABC821FCBC0002F6B6C0BCACD8A5 |
| EVIDENCE_INDEX.md | 10302 | 9AA73FB932AA41A54D2EFFD395D82919C6CE783CAB9B0EE10DFD9929F7641C8D |
| FINAL_REPORT.md | 20529 | A7EFB83583F1FD41AD996A1C1BD51C836F750275802007370A55B1082DFE028D |
| HANDOFF.md | 9696 | 37FB6C62594032F17C34BCA24E13CCBD752BDC45E4C158C48169F8902DDB7E37 |
| HISTORICAL_SCOPE_REASSESSMENT.csv | 12048 | 481E6DAD6EC1289874F80D3721A0D51AFC776B074879C0219BDEA2595D4FD807 |
| INPUT_IDENTITIES.md | 11683 | 7B79EF1B462C901E56F750FDF18C7CC17C8E6258FA92B7356EE0BAC173903144 |
| LOGICAL_CONTROL_RESULTS.json | 2444 | 41EAB34F022F318CBFE3261E5D3E001F76A0549B0D9B70A1F4C2740F03E81F3F |
| MANIFEST_SHA256.csv | 6149 | 4FF0046F111548E14806EAB063BC7C7A7801E33FA00DF0F62235586DA4CC7B76 |
| MAPPER_RESULTS.json | 14941 | A7690860F9519B9F48BF834813B242EC6CB8A1097032323F2F89E97D796BAE9F |
| PE_MASTER_REVIEW.md | 6151 | 08D76CEA4E95A85BDC00EC2F324E74EB5D9A2BC63C00216CFBD4B7EEABDF5DB2 |
| QC_REPORT.md | 11449 | D79DEC9DA7B015FCC184ABCCD9456AE708155EEFE60ADDDE0BF41BFE4F16C1F6 |
| QC_RESULTS.json | 23334 | 1185FCB64D345A73ED56D7A58F1A4806BC657E63B81CFF918D9E900A36E84DBD |
| REGRESSION_RESULTS.json | 6607 | A9642BB669514D2AE0B6ABC8EECDA30A863CDA384F904671A05D66D530A481E1 |
| SOURCE_STATE_AND_FINDINGS.md | 16073 | 1744FC2A674A5A68C6510F6832B2CE34D8803B884F28970C57390F24C8306C73 |
| SUPERSESSION_LEDGER.csv | 21592 | 11DAFC8E4A9600D3D7A10B1C147BAED7FA09F517A894592404B35448F9160B3E |

Historical checker used by the 80-ID regression (READ_ONLY AST parse,
never executed):

```text
path   = docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/03_SCRIPTS/checker_plus4.py
size   = 12749 bytes
sha256 = F58D2DB36106006BA2CBF931DC9CFED872E9C5E22C5484E86462568B985AB7E8 (matches the pin)
```

## 5. Physical EXE headers measured (contract §2 read class)

```text
e_lfanew = 0x120; machine = 0x14C; nsec = 5; SizeOfOptionalHeader = 0xE0;
Magic = 0x10B (PE32); ImageBase = 0x00400000 (== pin)
sections (RVA/vsize/roff/rsize/member_end):
  .text  0x00001000 / 0x6735E5 / 0x1000  / 0x674000 / 0x675000
  .rdata 0x00675000 / 0xF6569  / 0x675000 / 0xF7000  / 0x76C000
  .data  0x0076C000 / 0x3D6E4  / 0x76C000 / 0x34000  / 0x7A96E4
  .tls   0x007AA000 / 0xA      / 0x7A0000 / 0x1000   / 0x7AB000
  .rsrc  0x007AB000 / 0x3C54   / 0x7A1000 / 0x4000   / 0x7AF000
no two section membership intervals overlap (verified by independent
arithmetic); the gap between .data member_end 0x7A96E4 and .tls 0x7AA000 is
covered by no section (a read there classifies UNMAPPED)
```

## 6. PRE/POST execution identities (00_PRE/ and 00_POST/ run headers)

```text
PRE stamp  = 20261009T035439Z (v1 = the EXACT SOURCE checker imported via
             importlib; QC = the historical QCPE AST-EXTRACTED from the
             SOURCE qc_countercheck.py — executed definitions only:
             QC_RAW/QC_BSS/QC_UNMAPPED/QC_REJECT constants, QCReadError,
             QCPE, make_minipe, sha256_bytes, sha256_file, parse_hex,
             _try_read; main() and every other top-level statement NEVER
             executed)
POST stamp = 20261009T035844Z (production = checker_plus4_successor_v2.py;
             post_qc columns: the historical QCPE v1 recorded for
             continuity AND the fixed independent QC honestly marked
             DEFERRED_TO_QC_PHASE — the fresh QC worker is a separate
             parent phase)
superseded POST attempts kept as authentic negative evidence:
  20261009T035645Z (crashed at the P2-B probe fixture — runner KeyError;
                    two partial files kept)
  20261009T035712Z (crashed in the boundary assembly — tuple-index runner
                    bug; full raws, no final assembly)
  20261009T035717Z (crashed in the boundary assembly — missing-geometry
                    runner bug; full raws, no final assembly)
  20261009T035740Z (completed but carried two runner case-design defects —
                    superseded by the corrected run; files kept)
source checker / qc / pins JSON re-verified UNCHANGED after both phases
(sha256 equal to the §4 pins)
```

## 7. Final identity re-verification (executor self-check, after all controls)

```text
EXE after everything   : 8015872 bytes /
                          E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (unchanged)
SOURCE_RUN 22 files    : re-hashed after all controls — all identical to §4
ACTIVE_CORRECTED_PINS.json : 64C64DA9D59CEEC25C72D1890C89E38935BB21530D8E3ED8B90537B98705001F (unchanged)
AUDIT_ENTRYPOINT.md    : 263460 / 87FF331453E5643407C7428B6C43EE6898A22E33379AF2EC3812A01ADD287C01 (unchanged; NOT edited by this phase)
__pycache__ / .pyc     : NONE (python -B everywhere; verified by directory scan)
```
