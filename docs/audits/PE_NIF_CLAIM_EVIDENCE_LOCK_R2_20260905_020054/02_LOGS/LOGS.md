# 02_LOGS — commands, execution history, errors and disposition
# PE-NIF-CLAIM-EVIDENCE-LOCK-R2 (all commands executed on the VM project tree)

## Tool versions
- Node.js v22.22.0 (control_r2.cjs, emit_r2_csvs.cjs; no external dependencies)
- Python 3.12.10 (run_gates.py — stdlib only: csv/base64/hashlib/struct/zlib)
- Windows PowerShell 5.1 (filesystem operations, hashing via Get-FileHash)
- git (repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; read-only during
  analysis: rev-parse / status only; the single authorized publication write is a
  bounded add/commit/push of ONLY docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_.../,
  with per-command -c http.sslBackend=openssl; no force; no global config change)

## Prompt integrity
- OPENCODE_R2_PROMPT.md SHA256 verified BEFORE execution and re-verified by gate
  R2G1: 46A2A99A9F1D03B4FE33F2FBFCA89D2440FD702188A3D020E9BF29A7A370E5ED (match).
- AUDIT_OUTPUT_ROOT did not exist at check time (Test-Path = False); created fresh
  with the required structure (00_CONTROL..06_REPORT + root files).

## Execution history (hash-after-last-edit discipline; hashes recorded in
## 00_CONTROL/SHA256_CONTROL.txt BEFORE each execution)
- control_r2.cjs (Node instrument):
  - EXECUTION 1 (hash 21F40C8E0DA21B444E7C2AE0DD14425BA6EFEE0BCCEDD7CBB4F2B9EB6D927EED):
    CRASHED at the R39 sidecar lookup — the R39 manifest's UTF-8 BOM was kept in the
    header-name derivation (head[0] = BOM+"artifact"), pathCol became -1 and every
    artifact_field was empty. No RECOUNTS.json written; sidecars from this execution
    were superseded. DISPOSITION: encoding-contract defect in the R2 instrument,
    fixed by stripping the BOM ONLY for header-name parsing (raw bytes untouched).
  - EXECUTION 2 (hash A1EDA2AE3E4D139B15346FD4C9065646B730648E5048100D2C716D0F73E18D79):
    COMPLETE. Era join 5422/5208/214/4/174; family unique files 214/9/214/3/214 +
    old-only 4/0/4/0/4; morph 29 occurrences in 3 files (13/13/3); R1-bug fixture
    reproduces R1 exactly; 10 candidates physically recomputed (nine exact-0 +
    crc32(payload) 3435/5596 + 3299/5426; R36 agreement 20/20); 12/12 sidecar byte
    reconstruction; R39 GAP role text round-trip equality; R1 lossy role confirmed.
  - EXECUTION 3 (hash recorded in SHA256_CONTROL.txt): after the R2G10 gate caught a
    22-field manifest-header-row sidecar entry (stray extra field); fixed to 21
    columns; RECOUNTS.json byte-identical (SHA 19718c95d90d6d314bb2528e0928ffccf120b8f15f57bad15a40fe0cfa026b25
    unchanged); all 12 sidecars re-emitted with the corrected layout.
- run_gates.py (Python independent checker + gate suite):
  - run 1 (content phase, hash 1C54E70852714E04346134F307C87FBF5954F5203ED9E69AC8259F9E3058078F
    before the fixes below): 5 EXECUTABLE FAILURES DETECTED (R2G10, R2G12, R2G13,
    R2G15, R2G16) — the suite demonstrably detects defects:
    (a) sidecar coverage math counted the manifest header row wrongly + the
        22-field header-row entry (fixed in control_r2.cjs exec 3 + coverage check);
    (b) synthetic-fixture assertion had a typo (asserted a substring that cannot
        occur in a correctly quoted row);
    (c) CLAIM_MATRIX tally expectation was wrong (correct emitted tally is
        CONFIRMED 16 / REJECTED 8);
    (d)(e) quote checks were line-wrap-blind (R1's report wraps "parsed by the R35
        validators" across lines) — whitespace-normalized checks added.
  - run 2 (content phase, final): 17/17 EXECUTABLE PASS, exit 0. TEST_RESULTS.json
    written. (HR-1..4 are HUMAN_REVIEWED rows with pass=null by design.)
  - run 3 (--phase final, executed after artifact_index.csv emission): re-runs all
    17 content gates from fresh recomputation + R2G18 (artifact integrity). Exit
    nonzero on any failure. Result recorded in TEST_RESULTS.json (final).
- emit_r2_csvs.cjs: emitted CLAIM_MATRIX.csv (24 rows), FINDING_DISPOSITIONS.csv
  (7 rows), SUPERSESSION_MAP.csv (18 rows) with strict RFC4180 quoting; re-run
  after the C2-E-02 source-hash fix (source_sha256 must be a real hash for R2G13).

## Read-only source operations
- Both Models.bnt containers: read-only parse (bounds checks), payload CRC32/
  adler32 recomputation, era join, family scan, candidate recount.
- R29-R40 run dirs: the 12 artifact_index.csv manifests (byte-accurate reads; the
  R39 manifest BOM preserved in raw_row_base64), R35 GRAMMAR_VALIDATION.json,
  R36 FIELD_D_TESTS.json + field_d_r36.py, R39 EDIT_PROPOSALS-derived counts via
  the R1 control output (read-only; no historical driver executed).
- R1 run dir: read-only (CONTROL_R1_RESULTS.json, CLAIM_MATRIX.csv, gates CSV,
  reports, sidecars, LOGS, SHA256_CONTROL.txt, generate_gates.cjs). R1 immutability
  re-verified by gate R2G17 (10 key hashes).
- Post-audit package: read-only (prompt, report, verify.py, verification.json).
- git repository: rev-parse HEAD / status (BASE_SHA c0c2f2fc captured; the only
  untracked path is another writer's docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/
  — untouched, excluded from the R2 commit).

## Errors encountered and disposition
1. exec-1 BOM crash (R39) — fixed (header-name derivation only); documented.
2. exec-3 sidecar 22-field header-row entry — caught by R2G10; fixed; documented.
3. Gate-suite self-corrections (coverage math, synthetic assertion typo, tally
   expectation, line-wrap-blind quote checks) — all caught by the suite itself
   failing; each fix documented above. The suite demonstrated it FAILS on real
   defects (that is the point of Area E).
4. No historical file, wiki file, canonical file, PE_AUTO_LOOP.json or shared tool
   was written. All writes are inside this run dir + the single authorized repo
   publication path.

## Runtime / game execution
- NOT RUN (04_RUNTIME/NOT_RUN.md). No PE.exe, no game, no emulator, no Ghidra,
  no historical driver executed.
