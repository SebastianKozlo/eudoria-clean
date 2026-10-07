# FULL_READ_LOG — PE_935_CAND4_CHILD_ROOT_PROVENANCE_INTERNAL_QC_R2_20261007

READ_MODE = FULL_READ (entire file, to EOF) unless noted. All 28 package files
were read IN FULL by this QC session before any measurement. Line counts are
the actual file line counts.

## Package root (16 files)

| # | path | lines/bytes | mode |
|---|---|---|---|
| 1 | CLAIM_MATRIX.csv | 23 / 11,104 | FULL_READ |
| 2 | CONTROL_RESULTS.json | 106 / 5,480 | FULL_READ |
| 3 | EDGE_ACCOUNTING_LEDGER.csv | 100 / 19,965 | FULL_READ |
| 4 | EVIDENCE_INDEX.md | 56 / 4,694 | FULL_READ |
| 5 | FIELD_PRODUCER_LEDGER.csv | 12 / 3,817 | FULL_READ |
| 6 | FINAL_REPORT.md | 222 / 13,785 | FULL_READ |
| 7 | GETTER_DECODE.md | 98 / 6,375 | FULL_READ |
| 8 | GOVERNANCE_DECISION.md | 168 / 9,214 | FULL_READ |
| 9 | HANDOFF.md | 194 / 14,619 | FULL_READ |
| 10 | INPUT_IDENTITIES.md | 131 / 7,999 | FULL_READ |
| 11 | MANIFEST_SHA256.csv | 38 / 4,991 | FULL_READ |
| 12 | PE_MASTER_REVIEW.md | 29 / 1,699 | FULL_READ |
| 13 | POINTER_LINEAGE.csv | 9 / 3,605 | FULL_READ |
| 14 | PREREGISTRATION.md | 255 / 15,397 | FULL_READ |
| 15 | QC_INTERNAL_RESULTS.json | 99 / 3,885 | FULL_READ |
| 16 | QC_REPORT.md | 127 / 7,797 | FULL_READ |

## 01_RAW (9 files)

| # | path | lines/bytes | mode |
|---|---|---|---|
| 17 | FUN_006C0D50_CTOR_DECODE.txt | 67 / 4,782 | FULL_READ |
| 18 | FUN_006C66D0_GETTER_FULL.txt | 56 / 3,642 | FULL_READ |
| 19 | FUN_006C6780_INSTALLER_PARTIAL.txt | 101 / 7,930 | FULL_READ |
| 20 | FUN_006C6F60_PRODUCER_DECODE.txt | 102 / 8,468 | FULL_READ |
| 21 | FUN_006C8B20_LAZYINIT_DECODE.txt | 91 / 6,828 | FULL_READ |
| 22 | FUN_006C8F80_BASECTOR_DECODE.txt | 78 / 5,593 | FULL_READ |
| 23 | JOIN_WINDOW_50A3B7_REPIN.txt | 53 / 4,043 | FULL_READ |
| 24 | PINS_AND_REL32.txt | 96 / 7,274 | FULL_READ (56 pins + 23 rel32 ALL re-verified against the EXE) |
| 25 | VTABLE_RTTI_STRINGS.txt | 45 / 3,066 | FULL_READ |

## 03_SCRIPTS (3 files)

| # | path | lines/bytes | mode |
|---|---|---|---|
| 26 | make_manifest.py | 64 / 3,184 | FULL_READ |
| 27 | qc_controls.py | 216 / 13,137 | FULL_READ (every checker read; independently replicated) |
| 28 | qc_internal.py | 288 / 16,260 | FULL_READ (all 23 checks' logic read) |

## External inputs read in full by this QC

| path | bytes | mode |
|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md | 18,159 (375 lines) | FULL_READ (the governing contract) |

## Machine/measurement coverage (my own instruments)

- Own PE mapper + own byte reads: all 56 pins, all 23 rel32, 20 explicit chain pins, RTTI walks (3),
  vtable slots (4), string constants (4), 3 caller rel32s, 6 body extents (incl. CC padding + next
  entries), join window (22 instructions), 15 NEIGH/GAP-2/RV spot checks, CTRL_3 foreign accessor.
- Own sequential decoder walks: 6 bodies (0/1/2/5/13/5 CALLs = 26) + join window; listing-address subset
  verification vs all 6 raw decode files + the join window file (100%).
- Independent CSV census parse: EDGE_ACCOUNTING_LEDGER (65 rows), FIELD_PRODUCER_LEDGER (12),
  POINTER_LINEAGE (9), CLAIM_MATRIX (23), MANIFEST (27 rows), PINS_AND_REL32 (regex census: 56+23).
- Independent .NET re-hash: 27/27 manifest rows; encoding: all package files.
- Historical packages: 49 + 27 git-blob identity checks (BASE d65fa12e) + both aggregate SHA-256
  reconstructions (recipe independently derived and MATCHING).
- Repo/vermessen: git rev-parse/status/diff (HEAD == BASE; zero tracked modifications;
  AUDIT_ENTRYPOINT.md unmodified; 7 untracked roots inventoried: 1 this package + 6 foreign).
- Bounded oracle availability search (D:\ top-level; recursive *openmw* depth-2; gamebyroengine
  listing); Gb12 file re-hash (2 files).

## NOT_CHECKED / COVERAGE limits of this QC

- See QC_IND_REPORT.md "NOT_CHECKED by this QC (explicit)" — the unopened bodies, runtime, payloads,
  remote state beyond the BASE pin, and the 0x110 object's own bytes were not touched (QC opens no new
  science branches).
- The executor's PRIVATE scratch (C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CHILD_ROOT_...)
  was NOT read by this QC (it is not part of the package; the run's identity claims about it — decoder
  module SHA etc. — remain executor-attested; my own decoder made them non-load-bearing for the
  package's scientific claims).
- AUDIT_ENTRYPOINT.md was read only at head (12 lines) + verified UNMODIFIED via git (no full read —
  it is outside the audited package and untouched).
