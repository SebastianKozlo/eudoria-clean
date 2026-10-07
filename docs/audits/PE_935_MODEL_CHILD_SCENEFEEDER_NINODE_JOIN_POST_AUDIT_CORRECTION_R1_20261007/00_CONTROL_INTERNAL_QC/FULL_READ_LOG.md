# FULL_READ_LOG — PE_935_MODEL_CHILD_SF_JOIN_CORRECTION_INTERNAL_QC_R1_20261007

Coverage algebra (L11): PACKAGE_FILES_READ = 17/17 FULL_READ (100% of the audited
correction package). SOURCE_RUN_PACKAGE = 49 files: blob-identity re-hash 49/49
(machine, full); content FULL_READ for the 21 files load-bearing for J1/J2/J3/§7/§10
(listed below); remaining 28 read as TARGETED (grep/machine parse) where a specific
record was needed; none of them gates a load-bearing conclusion of this QC without
a full read (the load-bearing records — ledgers, CLAIM_MATRIX, PRE_REGISTERED_
ANCHORS, FINAL_REPORT, HANDOFF, PE_MASTER_REVIEW, QC_REPORT, 10 of 11 raw files —
were fully read).

## FULL_READ (to EOF)

Correction package (17/17):
- CORRECTED_STATUS_ALGEBRA.md (124 lines)
- DESKTOP_FINDINGS_DISPOSITION.md (146)
- EDGE_BUDGET_RECONSTRUCTION.csv (77 lines: 6 header + header row + 70 data rows)
- FINAL_REPORT.md (162)
- GATE_COUNTEREXAMPLES.json (224)
- GOVERNANCE_DECISION.md (175)
- HANDOFF.md (107)
- INPUT_IDENTITIES.md (70)
- MANIFEST_SHA256.csv (19: 2 header comments + header + 16 rows)
- PE_MASTER_REVIEW.md (26, placeholder)
- QC_REPORT.md (95)
- QUALIFICATION_GATE_CORRECTED.py (598)
- SUPERSESSION.md (113)
- 03_SCRIPTS/gate_corrected_results.json (750)
- 03_SCRIPTS/make_manifest.py (81)
- 03_SCRIPTS/qc_correction.py (357)
- 03_SCRIPTS/qc_correction_results.json (128)

Governing inputs:
- OPENCODE_J1_J3_CORRECTION_REVIEWED.md (490 lines) — contract, full
- Desktop REPORT.md (121) + PRODUCTION_GATE_COUNTEREXAMPLES.json (699) — full

Source-run package (BASE 064b7f4; physical == blobs verified FIRST):
- EDGE_LEDGER.csv (7), FUNCTION_BUDGET.csv (9), CLAIM_MATRIX.csv (21),
  CANDIDATE_LEDGER.csv (5 rows; long CAND-4 line display-truncated by the reader,
  machine-parsed in full via csv.DictReader in my checks), PRE_REGISTERED_
  ANCHORS.md (171), FINAL_REPORT.md (199), QC_REPORT.md (160), HANDOFF.md (78),
  PE_MASTER_REVIEW.md (41), 00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md (368)
- 01_RAW: FUN_0050A310_DECODE.txt (107), FUN_007B5810_ORACLE_BYTE_PROOF.txt (105),
  FUN_00509850_FULL.txt (127), FUN_509x_SF_METHODS.txt (95), FUN_007BF500_DECODE.txt
  (65), FUN_00528E50_CONTINUATION.txt (84), FUN_008BD720_DECODE.txt (248),
  REPIN_ANCHOR_WINDOWS.txt (312)
- FUN_006A3930_CHAIN_REPIN.txt: E8-scan list + all disassembly windows read
  (154 lines); the 832-byte BYTES dump line displays truncated at 2000 chars —
  the missing-callsite verification was performed MACHINE-wise from the EXE at the
  published window VAs (results_j2_j3_package.json), so no conclusion rests on the
  truncated display.

## TARGETED (grep / machine parse; specific records)

- 00_CONTROL_INTERNAL_QC/HANDOFF_QC.md, FULL_READ_LOG.md (tail/95C0 + callee-list
  records), qc_independent_repins.py (line 420 tail-bytes read), qc_independent_
  repins_results.json (line 349 tail bytes), 03_SCRIPTS/build_ledgers.py (line 138
  CAND-4 PATH_CONDITIONS source), SF20_WRITER_CENSUS.txt / SF20_EXTERNAL_WRITER_
  SCAN.txt (census artifacts, not load-bearing for my checks), EVIDENCE_INDEX.md,
  INPUT_IDENTITIES.json/.md (source), 00_CONTROL_INTERNAL_QC remaining QC/gate
  scripts + results (referenced identities), source MANIFEST_SHA256.csv (row SHA
  cross-check for the historical gate identity).

## NOT_CHECKED (explicit; none gates a load-bearing conclusion of this QC)

- Actual remote master state — no network fetch was performed by this QC (origin/
  master cached ref == HEAD == BASE 064b7f4; remote equality is the persistence
  phase's terminal duty per contract §11).
- FUN_006C66D0 and FUN_007BF470 bodies — FORBIDDEN by the dispatch; remain
  undecoded; no new EXE regions opened by this QC (all reads at already-published
  pin VAs).
- Runtime anything; client execution; VFS/BNT/NIF payloads; ExtraData readback —
  out of scope.
- The executor's un-persisted terminal-handoff manifest re-hash (F-QC-3, P3) —
  covered by my own independent bijection re-hash.
- Byte-level untouchedness of the 6 foreign untracked roots (no baselines; only
  inventoried, untouched by this QC).
- The source run's historical qualification_gate.py was NOT re-read in full and NOT
  executed: its on-disk SHA256 matches the BASE manifest row and the Desktop-pinned
  EF2D8E1F… identity (my measurement), and the Desktop post-audit already executed
  and characterized it; the J1 correction was verified against the NEW gate.
- Prior-run materials referenced only as prior canon (LINK30, MICRO_R1, bridge,
  slot-17 canon, Gb12 sources) — inherited identities, not re-opened.
- The executor's fixture-construction provenance claim ("Desktop JSON not copied as
  fixture source") — not directly verifiable; covered functionally by my OWN
  independent recreation producing the contract-expected verdicts, and by the
  gate's ID-agnostic verdict logic.
