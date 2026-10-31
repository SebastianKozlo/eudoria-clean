# AMEND_LOG — PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 (PERSIST_PUBLISH)

RUN_ID: PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031
PARENT_LOOP: 75db9418-2d3e-4e05-9799-eeb4c3f63955
WORKER: pe-master-auditor (PERSIST_PUBLISH, bounded prose corrections authorized by PE-MASTER)
BASE_SHA: dc6f1961125596dba9f3156371fb427a90881436 (== HEAD before and during the run; verified)

Scope of this log: ONLY the administrative/prose corrections explicitly
authorized by PE-MASTER for this persistence, plus the persistence artifacts
themselves. Raw evidence (01_RAW/, 02_ANALYSIS/, tools/, 00_CONTROL/qc_probe/)
was NOT modified. No executor measurement was altered; corrections below fix
reporting arithmetic/labels only, and each preserves the measured values.

## Authorized prose corrections (P3)

### AMEND-1: REPORT.md §4 coverage algebra
- FILE: 04_REPORT/REPORT.md
- DEFECT: coverage sentence double-counted a subset — "dual-decoded (4) +
  header-censused (1850) + header-unclassified (15 ... 1851 zdekodowane
  wyłącznie na poziomie nagłówka)" mixed overlapping counters (1850 + 15
  overlapped; the trailing "1851" restated a different decomposition).
- CORRECTION: 1865 total = 4 dual-decoded + 1861 header-only (of which 15
  header-unclassified); sums no longer double-count subsets; rest of the
  paragraph preserved (payload-level dual decode 4/1865; full payload
  structure 3/4; TYPE1 tail open).
- MEASURED VALUES: unchanged (4 / 1861 / 15 / 1865 / 0 missing).
- BEFORE_SHA256: 8C8E320E50725A8B6CE489EACFEBB77E648FFE26F113CF68B3851B309B6F52A6
- AFTER_SHA256:  0F740871D7E5A9D1F73012468C2C1D190467E48B310698FFCC95E198A23EB86E

### AMEND-2: STAGE_ACCEPTANCE_GATES.csv G3 negative-control counter label
- FILE: STAGE_ACCEPTANCE_GATES.csv (row G3_DUAL_DECODE_AGREEMENT, evidence column)
- DEFECT: the label "12/12 negative controls fail on both decoders" counted
  per-decoder (12 controls per decoder), while the run executed 24 total
  negative controls (verified in raw DECODE_A.json / DECODE_B.json by QC and
  PE-MASTER).
- CORRECTION: "negative controls EXECUTED 24 = 2 decoders x 4 samples x 3
  controls, all FAIL with recorded output on both decoders (the previous
  '12/12' label was per-decoder; total executions are 24, result of the gate
  unchanged)". Gate RESULT column unchanged: PASS.
- MEASURED VALUES: unchanged (24 executed negatives, all FAIL with recorded
  output).
- BEFORE_SHA256: 72B2845C6F634170D35E01E1F9E401C09CD179D8CD7292BA37B5EBC84E8584F3
- AFTER_SHA256:  BF034AB74BE66B2CC18D5BC4F62CF4930D41501D6648836F35F64A951987D54E

## Persistence artifacts (new, no BEFORE state)

- 04_REPORT/PE_MASTER_REVIEW.md — PE-MASTER verdict persisted VERBATIM
  (byte-frozen between BEGIN/END markers) + persistence-worker verification
  appendix.
- artifact_index.csv — regenerated LAST from a fresh disk census over the
  FINAL package state (full bijection; self-excluded per the manifest
  self-exclusion precedent — a manifest cannot contain its own hash).
- AUDIT_ENTRYPOINT.md — ONE newest-first LATEST RUNS row added for this run
  (verified `git numstat`: exactly 1 insertion, 0 deletions in that file);
  no prior row removed (L07).

## Disclosure: proprietary payload exclusion from the commit

- 01_RAW/samples/*.bvi.bin (4 files: 105624 / 506044 / 506237 / 584781) are
  RAW .bvi payload bytes extracted from the proprietary Volumes.bnt corpus.
  Per the worker contract §6 and the explicit PE-MASTER staging instruction
  (no .bnt/.bvi/.nif bytes in staging), these files are NOT staged and NOT
  committed. They remain LOCAL-ONLY forensic evidence on disk; their SHA256,
  size and provenance are recorded in artifact_index.csv and
  01_RAW/samples/SAMPLE_MANIFEST.json so the committed package references
  them honestly. The hexdump transcriptions (*.bvi.hexdump.txt) ARE text
  forensic metadata and ARE committed.

## NOT modified

- 01_RAW/, 02_ANALYSIS/, tools/, 00_CONTROL/qc_probe/, 00_CONTROL/
  HANDOFF_CONTRACT.md, 00_CONTROL/PRE_DISPATCH_QC.md: byte-identical to the
  executor's final state (their rows in the regenerated artifact_index.csv
  match the pre-persistence hashes of the original artifact_index.csv).
- compat/, src/, and all files outside docs/audits/PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031/
  and AUDIT_ENTRYPOINT.md: untouched.
