# INPUT_IDENTITIES — PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

```text
RUN_ID      = PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007
RUN_CLASS   = RECORDS_AND_QC_MACHINERY_CORRECTION (correction-only; ZERO new science / ZERO new RE)
EXECUTOR    = pe-reconstruction (PE-MASTER bounded dispatch)
EXECUTED    = 2026-10-07/08 UTC (all timestamps below are UTC, physically measured)
```

This file records the identity of every input consumed by this run, as required by the
dispatch STEP 0/STEP 4. Every SIZE/SHA256 below was independently measured by this
executor (PowerShell `System.Security.Cryptography.SHA256` over the raw file bytes;
Python `hashlib` cross-used inside the scripts where noted). No chat-transcribed
number was trusted without physical re-measurement.

## 1. Dispatch contract identity (read in FULL before any action)

```text
PATH        = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_FULL_CONTRACT_REVIEW_EFECB205_20261007\OPENCODE_NC1_CORRECTION_REVIEWED.md
SIZE_BYTES  = 18981         (required: 18981)
SHA256      = D93E793CA0B9EBAA96D2D03F0D0BA31E3F2ED7C234BBBB4BC863631873AE35D3  (required: identical)
VERDICT     = MATCH
```

- First physical verification: 2026-10-08 ~05:31–05:32Z (immediately upon location of the
  contract file); re-measured in the consolidated identity sweep at 2026-10-08T05:34:17.405Z —
  both measurements identical.
- The contract was READ IN FULL (950 lines) BEFORE the preflight; RUN_ID, RUN_CLASS,
  EXPECTED_BASE_SHA, REPO_ROOT, SOURCE_PACKAGE and OUTPUT_ROOT were resolved from it and
  from the dispatch, not from chat numbers.
- Mismatch handling: none required (exact match; no BLOCKED_INPUT_IDENTITY condition occurred).

## 2. Mandatory Desktop inputs (contract §1; dispatch STEP 0)

### 2.1 Desktop REPORT.md

```text
PATH        = C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CORRECTION_DESKTOP_POST_AUDIT_57ECF350_20261007\REPORT.md
SIZE_BYTES  = 10543          (required: 10543)
SHA256      = 2324C31F173AF433A7C7A41FCE0CCA2674EEB1F62B4DCDD00F8B8972086E5771  (required: identical)
MEASURED    = 2026-10-08T05:32:13–15Z (preflight block) and 2026-10-08T05:34:17.405Z (identity sweep)
VERDICT     = MATCH
```

### 2.2 Desktop CONTROL_COUNTERCHECKS.json

```text
PATH        = C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CORRECTION_DESKTOP_POST_AUDIT_57ECF350_20261007\CONTROL_COUNTERCHECKS.json
SIZE_BYTES  = 46675          (required: 46675)
SHA256      = 2288CB39E357343C4A404F83D6327E5A628547C467D28869A2C34237C0090C00  (required: identical)
MEASURED    = 2026-10-08T05:32:13–15Z (preflight block) and 2026-10-08T05:34:17.405Z (identity sweep)
VERDICT     = MATCH
```

- READ-ONLY use: the `cases/sib_hidden_edi_write` record was transcribed (path+SHA cited
  in-file) into CONTROL_RESULTS_PRE.json `SOURCE_DESKTOP_MEASUREMENT`
  (EXPECTED=FAIL, PRODUCTION_CHECKER=PASS, INTERNAL_QC_CHECKER=PASS,
  REFERENCE_EDI_WRITE=0x0050A3E4, FALSE_PASS_REPRODUCED=YES), clearly labeled as the
  Desktop's measurement (post-audit of 57ecf350), NOT this executor's.
- The case's `bytes` field was used ONLY as a transcribed comparison constant to assert
  byte-identity of the constructed in-memory NC1 buffer with the authoritative synthetic
  counterexample (assert result: True).

## 3. READ-ONLY SOURCE_PACKAGE identity (never modified by this run)

```text
PATH (repo-relative) = docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/
EXISTS               = YES  (verified 2026-10-08T05:32:20.190Z preflight)
PHYSICAL FILES       = 27   (measured 2026-10-08T05:34:17.420Z; re-verified after the run: 27 — UNCHANGED)
SOURCE_PACKAGE_SHA   = 57ecf3506481e73ca27548ea02e4864904d9883a (the published package state, frozen at the base commit)
```

Old production checker (the correction's READ-ONLY predecessor; imported via importlib
for the EXECUTOR_REPRODUCTION — module-level inert, `run_and_write` NEVER invoked):

```text
PATH        = docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/ctrl4_exact_endpoint.py
SIZE_BYTES  = 20592
SHA256      = FDB5F16E6F9A6352030DD2F4D9523E1CAA0AB924F2112DDEC787CC7B3A84A330
MEASURED    = 2026-10-08T05:34:17.405Z and re-hashed by run_nc1_matrix.py at execution
```

## 4. Runtime identity

```text
PYTHON      = 3.12.10   (measured 2026-10-08T05:34:17.456Z)
HOST SHELL  = Windows PowerShell 5.1 (measurement host)
BYTECODE    = every python invocation used -B, and run_nc1_matrix.py sets sys.dont_write_bytecode
              before any import; post-run residue scan: __pycache__/.pyc = NONE in OUTPUT_ROOT and NONE
              in SOURCE_PACKAGE
```

## 5. Preflight queries and errors (fail-closed STEP 0 — all executed from REPO_ROOT)

```text
[2026-10-08T05:32:13.345Z]  git rev-parse HEAD
    -> 57ecf3506481e73ca27548ea02e4864904d9883a
[2026-10-08T05:32:13–14Z]   git fetch origin master
    -> FETCH_EXIT=0. stderr contained only the informational progress lines
       ("From https://github.com/SebastianKozlo/eudoria-clean", " * branch master -> FETCH_HEAD"),
       which PowerShell renders as a NativeCommandError record — NOT a fetch failure.
[2026-10-08T05:32:13–14Z]   git rev-parse origin/master   (after fetch)
    -> 57ecf3506481e73ca27548ea02e4864904d9883a
[2026-10-08T05:32:13–14Z]   git ls-remote origin master   (LIVE remote query, not cache)
    -> 57ecf3506481e73ca27548ea02e4864904d9883a  refs/heads/master     LSREMOTE_EXIT=0
[2026-10-08T05:32:14.700Z]  git rev-parse HEAD (recheck)
    -> 57ecf3506481e73ca27548ea02e4864904d9883a
[2026-10-08T05:34:17Z]      git remote get-url origin
    -> https://github.com/SebastianKozlo/eudoria-clean.git
```

- All three base-SHA queries (LOCAL_HEAD, origin/master, live remote master) equal
  EXPECTED_BASE_SHA 57ecf3506481e73ca27548ea02e4864904d9883a → PREFLIGHT PASS.
- Remote availability: AVAILABLE (live ls-remote succeeded).
- Errors: NONE. No BLOCKED_INPUT_IDENTITY, no BLOCKED_BASE_MISMATCH, no BLOCKED_EXTERNAL.

## 6. Fixture provenance (unchanged from the SOURCE_PACKAGE checker)

- The clean window buffer is the 0x42 bytes of WINDOW 0x0050A3B7..0x0050A3F8 exactly as
  published per-instruction in SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (verified
  there: instruction lengths, both rel8 targets, all four rel32 call targets, total length
  0x42 — re-verified by this run against the published FIXTURES.md F3 map in
  CONTROL_RESULTS_POST.json clean_window_full_decode_listing.boundary_regression = PASS).
- The corrected successor `03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py` carries the IDENTICAL
  fixture: byte-identity of its CLEAN_WINDOW with the old checker's CLEAN_WINDOW was verified
  programmatically (result: True; recorded in both CONTROL_RESULTS_*.json).
- NC1 counterexample: contract §4 authoritative synthetic replacement
  `8B 8C 24 8C 00 00 E8 BF AA BB CC 90` over the 12-byte span 0x0050A3DD..0x0050A3E8
  (total window stays 0x42). The constructed in-memory buffer is byte-identical to the Desktop
  CONTROL_COUNTERCHECKS.json `sib_hidden_edi_write` case bytes (verified programmatically:
  True; recorded in CONTROL_RESULTS_PRE.json and CONTROL_RESULTS_POST.json).
- ALL buffers of this run are SYNTHETIC / IN-MEMORY ONLY. The EXE was never read, opened or
  decoded; no source file, historical record or any file outside OUTPUT_ROOT was modified.
