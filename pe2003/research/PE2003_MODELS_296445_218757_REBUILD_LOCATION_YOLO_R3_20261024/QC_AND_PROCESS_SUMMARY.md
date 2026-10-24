# QC_AND_PROCESS_SUMMARY — quality control and process of campaign R3 (sanitized)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.

## QC outcome

**QC_PARTIAL → QC_CLOSED_AFTER_MASTER_DISPOSITIONS** (35/37 checks PASS;
source: private `QC_FINDINGS.json`, QC run PE2003R3_QC_DISKAUDIT_R1_20261024).

Independence disclosure: QC ran in the SAME GLM model family as the executor —
NOT model-independent; procedural independence only: every load-bearing claim
was re-derived from physical bytes/files (own-code ARK parse, re-hashing, tool
re-execution in an isolated copy, own byte-level binary decode), never from
executor narrative.

## QC areas

- **Q_SOURCE (7 checks PASS)**: physical re-hash of both NIFs, Models.ark
  (3 copies), PE.exe/PE_CD.exe, installer, unpacked build, ISO/ZIP; manifest
  consistency; container-vs-payload status separation.
- **Q_FORMAT (8 checks, 1 P3 finding)**: isolated re-runs of the pipeline on
  both models + the explicit NOT_FOUND negative control (296446, denominator
  2492); independent re-derivation of member indices/CRCs from Models.ark
  with QC's own ZIP-chain parser; own header reads (155/62 blocks, 0x0401000C);
  negative tests 5/5; machine-parseability of all CSV/JSON/JSONL. Finding
  F-05 (P3): the REPORT's "all parse (ConvertFrom-Json)" wording overstates a
  PS 5.1-specific quirk for the two large NIF_STRUCTURE JSONs (valid under
  strict Python) — NOTED.
- **Q_SCIENCE (6 checks PASS)**: QC byte-level decode of open_nif sprintf
  construction, manager vtable slots, frame-0x06 dispatcher switch, ×100.0
  constant, the row-vector (v·M) orientation math; cross-file consistency
  (no file claims a confirmed definition→open).
- **Q_WORLD (5 checks PASS)**: denominators physically re-counted;
  definitions carry no positional floats; Volumes 831 corpus; no
  "reconstructed" placement claim anywhere.
- **Q_ACCOUNT (7 checks, findings F-01/F-03/F-04)**: tool SHA pins re-hashed
  and matching; ledgers honest (LOWER_BOUND/UNMEASURED); F-01 (P2) native
  Task attempt-count inconsistency (13 census entries vs used=12 vs REPORT
  "11 of 96" vs ROLE_LEDGER 0) — REQUIRED_MASTER_DECISION, closed by
  MASTER-CLR-12 (canonical: 12 worker-job attempts + A1 assembly + QC);
  F-03 (P3) superseded F1 claim in a private file left without an inline
  marker (outside QC allowlist; MASTER-CLR-13); F-04 (P3) census schema
  irregularity — NOTED.
- **CROSS (4 checks; F-02)**: obligations backed by real evidence (O9
  pending by design); COMMON-no-promotion rule honored literally;
  F-02 (P2) stale METHOD_935_TO_2003_REPLAY status column FIXED_BY_QC
  (43 rows re-derived from raw evidence, 7 honestly left UNVERIFIED; logged
  QC-CLR-11; re-validated); cross-build/supersession consistency PASS.

Counts: 37 checks total — 35 PASS, 1 FAIL (F-01 accounting), 1 PARTIAL
(F-02 fixed); findings 5 (0×P0, 0×P1, 2×P2, 3×P3).

## Process facts

- 14 task campaign waves (FAMILY caps respected: H1/10, S2/10, F1/10, R4/18,
  W3/24, I1/8, Q1/16); worker jobs in PACKETS (F1, H1, I1, R1A, R1B, R2,
  R3JOB, S1, S1B, W1, W2, W3) + the A1 assembly job + QC.
- STATIC_ONLY corpus discipline: no client runtime, no debugger, no original
  game mutation; per-job decompile counts are LOWER_BOUNDs, untracked totals
  explicitly UNMEASURED; I/O ledgered.
- Corrections ledgered append-only (CLR-01..CLR-10 + QC-CLR-11) with original
  rows preserved (incl. the W2 class-identity correction and the F1
  non-existence claim rejected with evidence).
- Reproduction: actually-executed commands with input SHAs for both models;
  negative controls (tool 4/4 + inspector 5/5 + NOT_FOUND + census machinery
  negative control + R10 float-scan positive sensitivity).

## Limits

- Same-model-family QC (disclosed above).
- The campaign's A1 report predates QC; the authoritative QC/publication
  record is this package + the master's publication receipt
  (PUBLICATION_RESULT.json, private receipt root).
- O9 (QC + publication) closed by the QC + this publication, under master
  dispositions; standing remains ADVISORY_PENDING_EXTERNAL_POSTAUDIT,
  CANONICAL_GATE_EFFECT=NONE.
