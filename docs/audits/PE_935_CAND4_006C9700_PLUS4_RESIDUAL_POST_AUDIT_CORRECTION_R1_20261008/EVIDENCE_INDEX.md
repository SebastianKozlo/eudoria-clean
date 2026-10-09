# EVIDENCE_INDEX — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

Index of every evidence file/category in the package, with its role in the
run. All paths are repo-relative under
`docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/`
unless stated otherwise. Physical census: 75 files before this persistence
phase (executor 66 + QC 9) + the 5 files written by this persistence phase
(PE_MASTER_REVIEW.md, FINAL_REPORT.md, EVIDENCE_INDEX.md, HANDOFF.md,
MANIFEST_SHA256.csv) = 80 physical package files at commit time; every file
is hashed in MANIFEST_SHA256.csv (which excludes only itself, by documented
design) and AUDIT_ENTRYPOINT.md carries one additional manifest row.

## External physical evidence (NOT in the repo; local-only)

| evidence | identity | role |
|---|---|---|
| C:\Users\User\Downloads\OPENCODE_PLUS4_RESIDUAL_CORRECTION_R1_20261008.md | 23137 B / SHA256 2634BA31C4002B636E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969 (172 lines) | the frozen human-authorized execution contract; read IN FULL by executor, QC and PE-MASTER |
| C:\Users\User\Documents\ChatGPT\PE\PE_PLUS4_CORRECTION_DESKTOP_POST_AUDIT_0B94C48_20261008\ADVERSARIAL_COUNTERCHECKS.json | 16079 B / SHA256 62646637C323E0BAEAD371A0AE979D1F92DD2752B60C9D402E70A5A8FA38837B (649 lines, 9 cases) | the SOURCE Desktop adversarial corpus: 2 partial-overlap false-passes, 2 PE32-boundary false-passes, 4 truncation escapes, 1 wrong-callsite false pass (86/86). NO REPORT.md exists in that directory; none was invented |
| D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | the READ_ONLY physical target; rehashed before all reads and after all controls by executor AND QC (unchanged); reads limited to pins/rel32/RTTI/strings/COL/TD/name ranges + the 5 W-ctor bytes; never executed; never committed |

## Package root (12 files at commit time)

| file | role |
|---|---|
| AUTHORIZATION_RECORD.md | the bounded authority and permission limits of this one correction run (contract §7) |
| INPUT_IDENTITIES.md | measured identities: contract, BASE triple-check, Desktop corpus, EXE, SOURCE_RUN 22-file census, 10 load-bearing pins, PRE/POST execution identities, final re-verification |
| SOURCE_STATE_AND_FINDINGS.md | the source state (READ_ONLY), the four finding dispositions with this run's corrections, regression summary, HISTORICAL_FIRST_QC_PRE disclosure, executor self-corrections, standing ceilings |
| MAPPER_BOUNDARY_RESULTS.json | P2-A/P2-B machine-readable classifications: all 39 boundary cases (geometry, expected/observed v1/v2 classifications, exception classes, returned bytes, oracle rationale, negative finding) + header_positive_intact + oracle discipline |
| REGRESSION_RESULTS.json | the 80+6+1 regression: complete 80-ID set, table identity, RECW-old 6, NEW identity check 1, separate denominators 80/6/1=87, MC1–MC6, W-record mutation gates, prior RAW/BSS controls, wrong-callsite mutants, PRE false-pass record, clean scratch copy, verdict PASS |
| CORRECTED_CLAIM_MATRIX.csv | P2-C NEW ACTIVE claim matrix (22 physical rows): scoped R_W_SEPARATENESS, explicit unknown rows T_NOT_EQUAL_W_AT_LATER_USE / R_NOT_EQUAL_T_AT_LATER_USE, preserved ceilings, SCOPE_BUDGET_RECORDS (floor 17/bodies 5/edge 12, FAIL) |
| SUPERSESSION_LEDGER.csv | P2-C supersession records RS-1..RS-8: RS-1 retraction (a), RS-2 supersession of the active 'R != T', RS-3 the 10-location dependency census, RS-4 prior-supersession confirmation, RS-5/RS-6/RS-7 the P2-A/P2-B/P3 dispositions, RS-8 standing statuses + HISTORICAL_FIRST_QC_PRE + runner self-corrections |
| QC_REPORT.md | the fresh-context internal QC report: origin statement, method, 10 duty results, QC self-tooling fixes, final identity re-verification, coverage/NOT_CHECKED, open findings F-QC-1, verdict PASS |
| QC_RESULTS.json | the QC's machine-readable results: every duty's own measurements (18/18 P2-A; 9/9 P2-B; P3 mutant re-executions W1/W2/W3 86/87 each failing exactly the identity gate; clean 87/87 both loader paths; own W byte pin read; own 80/80; records re-adjudication; RS-3 census re-verification; spot verifications; PRE immutability), identities and verdict PASS |
| PE_MASTER_REVIEW.md | PE-MASTER MASTER_AUDIT verdict MASTER_ACCEPTED_ADVISORY (written in the persistence phase from the PE-MASTER-supplied verbatim text) |
| FINAL_REPORT.md | this run's terminal report (persistence phase) |
| EVIDENCE_INDEX.md | this index (persistence phase) |
| HANDOFF.md | the contract §8 mandatory final response fields (persistence phase) |
| MANIFEST_SHA256.csv | generated LAST: every physical file under the package EXCEPT the manifest itself, plus AUDIT_ENTRYPOINT.md; self-exclusion documented |

## 00_PRE/ — 11 files: the falsifier demonstrations (IMMUTABLE)

Run stamp 20261009T035439Z; every file matches its SHA256 index (QC-verified
0 mismatches); never overwritten.

| file | role |
|---|---|
| PRE_20261009T035439Z_RUN_HEADER.json | PRE execution identity: exact source scripts, import/AST-extraction discipline, EXE identity |
| PRE_20261009T035439Z_SHA256_INDEX.json | the PRE immutability index (10 files; self-excluded by design) |
| PRE_20261009T035439Z_BASELINE_CLEAN.json | PRE clean baseline on the ORIGINAL checker (86/86) |
| PRE_20261009T035439Z_CONTROLS_RAW.json | PRE MC/RAW/BSS control behavior of the source implementations |
| PRE_20261009T035439Z_HEADER_P2B_RAW.json | P2-B PRE: raw struct.error escapes on 0x98/0x99/0xB4/0xB7 (+probes) — byte-identical messages with the Desktop |
| PRE_20261009T035439Z_MAPPER_P2A_RAW.json | P2-A PRE: the four Desktop mapper false-passes reproduced on BOTH historical implementations with byte parity (`41 41 41 41` RAW_BACKED) |
| PRE_20261009T035439Z_WRONG_CALLSITE_P3_RAW.json | P3 PRE: the wrong-callsite mutant false-PASSES 86/86 through the ORIGINAL checker's NORMAL loader path; W2 honest negative |
| scratch/CLEAN_copy_20261009T035439Z.json | PRE scratch fixture: byte-identical copy of the SOURCE record |
| scratch/W1_wrong_callsite_20261009T035439Z.json | PRE scratch fixture: W1 teleport to 0x006C97D8 (E8 93 F7 01 00, +0x1F793, 0x006E8F70) |
| scratch/W2_wrong_record_id_20261009T035439Z.json | PRE scratch fixture: W2 RECORD_ID-only mutant |
| scratch/W3_generality_callsite_20261009T035439Z.json | PRE scratch fixture: W3 generality teleport to 0x006CB7CF |

## 00_POST/ — 46 files: post-fix controls incl. superseded stamps

Final corrected stamp 20261009T035844Z (39/39 boundary case-PASS, 87/87
clean baseline, regression PASS) + FOUR superseded stamps KEPT as authentic
negative evidence (035645Z partial-crash; 035712Z and 035717Z
assembly-crash; 035740Z completed-but-superseded with two disclosed
case-design defects). Per stamp: BASELINE_CLEAN, CONTROLS_RAW,
HEADER_P2B_RAW, MAPPER_P2A_RAW, REGRESSION_RAW, WRONG_CALLSITE_P3_RAW (the
final two stamps also RUN_HEADER + SHA256_INDEX; the crash stamps keep what
was physically produced). scratch/: CLEAN copy, W1, W2, W3 per stamp — the
mutant replays run on the REAL pinned EXE, never on a mutated source JSON or
mutated EXE.

## 00_CONTROL_INTERNAL_QC/ — 6 files: the QC's own raw evidence

| file | role |
|---|---|
| QC_COUNTERCHECK_V2_RAW.json | the QC's machine-readable raw output for all 10 duties (its own QCPEv2 measurements, oracles, non-circularity rationales, failure cases) |
| QC_ATTEMPTS_LOG.md | the authentic attempts log: attempts 1–2 failed before producing evidence (the two disclosed self-tooling fixes); attempt 3 is the completed QC run — kept as negative evidence per contract §6 |
| scratch/QC_CLEAN_copy.json | the QC's own clean scratch fixture |
| scratch/QC_W1_wrong_callsite.json | the QC's own W1 scratch fixture (normal loader path replay) |
| scratch/QC_W2_wrong_record_id.json | the QC's own W2 scratch fixture |
| scratch/QC_W3_generality_callsite.json | the QC's own W3 scratch fixture |

## 03_SCRIPTS/ — 3 files: the corrected machinery

| file | role |
|---|---|
| checker_plus4_successor_v2.py | the fixed PRODUCTION checker v2 (38568 B / SHA256 80EBEE27883AA61173737590FB822B3503B4658CDA511B4B690F8E75B6B64E62; 776 lines): half-open VA intervals, ANY-intersection fail-closed matching, staged constructor checks, the NEW identity gate RECW:W_RECORD_IDENTITY with the non-mutatable CANONICAL_RECORD_IDENTITY registry; the 80 historical gates unchanged |
| qc_countercheck_v2.py | the QC's OWN independent fixed QC implementation (89938 B / SHA256 F57988BC7DB255E70C0EEE7E6B3A7BD4C3F2045078233C90FD81F499B5AF4402; 1778 lines; class QCPEv2; NOT a re-export of the production classifier) |
| run_residual_controls.py | the executor's control runner (1794 lines): synthetic tests, production gate execution, mutant replays, dedicated PRE/POST paths, oracle interval arithmetic |

## Historical READ_ONLY sources cited by this package (never modified)

- docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/
  — the SOURCE_RUN (22/22 byte-identical at BASE; manifest blob
  60e8318e90a76e6d0a85365d9080a89f33bdd1bf), incl. the original
  checker_plus4_successor.py (30167 B / F50DDC40…), qc_countercheck.py
  (40309 B / 11957F40…), run_correction_controls.py (39340 B / 18F5B045…),
  ACTIVE_CORRECTED_PINS.json (4835 B / 64C64DA9…), and its historical
  CORRECTED_CLAIM_MATRIX.csv / SUPERSESSION_LEDGER.csv (the P2-C retraction
  targets, now superseded by RS-1/RS-2).
- docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/03_SCRIPTS/
  checker_plus4.py — the historical PROVENANCE checker (12749 B /
  F58D2DB3…) used READ_ONLY via AST parse for the 80-ID regression tables.
- AUDIT_ENTRYPOINT.md (repo root) — amended by THIS persistence phase: one
  new newest-first LATEST RUNS row for this run + the line-32 annotation
  extension withdrawing the "R!=T" standing use per RS-2 (F-QC-1). No other
  row touched.

## Evidence-integrity rules

- PRE is immutable and never overwritten by POST; superseded POST stamps are
  preserved negative evidence, not garbage.
- Every essential PASS in MAPPER_BOUNDARY_RESULTS.json / QC_RESULTS.json
  records MEASURED_QUANTITY, INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR
  and FAILURE_CASE_DETECTED.
- Replay of production is never counted as an independent oracle; expected
  classifications come from the runners' own interval arithmetic.
- MANIFEST_SHA256.csv is generated LAST and excludes only itself; its rows
  are re-verified (bijection, size, SHA256, duplicates, extras, missing)
  before commit.
