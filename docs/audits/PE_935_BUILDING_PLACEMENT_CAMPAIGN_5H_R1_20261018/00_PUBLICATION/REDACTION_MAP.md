# REDACTION_MAP — PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_R1 (this publication commit)

RUN_ID (publication): PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_RECEIPT_R1_20261018
Authoring run: contract §14 variant (b) — the sealed campaign root
`99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018` is FROZEN (read-only;
parent MANIFEST.json SHA256 ec012e1be55a597ba7501c19dec5423d027aab00d04568c6e999033439cf04f8);
this commit publishes a SANITIZED PROJECTION from a fresh worktree created at the fetched
origin/master.

## 1. Redactions applied to the published copies: NONE

- Every staged file was opened and scanned byte-by-byte for: personal/absolute user paths
  (`X:\Users\...`), secrets/credential patterns (api key, password, secret key, bearer,
  authorization), long hex-dump lines, base64 runs (>=120 chars), raw HTTP log lines,
  raw listing-row density (address+mnemonic rows as primary content), game payload magic
  strings (NetImmerse/Gamebryo file-format headers), control/binary bytes and UTF-8
  validity.
- Result: ZERO `C:\Users\...`-style personal paths exist in any staged file (verified over
  all 285 files of the sealed campaign tree and all 9 files of the postaudit tree; the
  published subset inherits this). Project-internal absolute paths
  (`D:\Eudoria_Reconstruction\...`) are retained deliberately: they are provenance
  pointers already present throughout the repository's published audit history and are
  not personal paths.
- Result: no secrets, no credential material, no raw HTTP logs, no payload magic, no
  base64 payload reproductions in any staged file.
- Therefore the published copies are BYTE-IDENTICAL to the sealed originals
  (verified per file by SHA256 immediately after copying; inventory in
  PUBLICATION_ALLOWLIST.csv). No content was edited, truncated or reworded in the
  projection. No file with raw listing rows as primary content is staged (see
  EXCLUDED_ARTIFACTS.csv).

## 2. One scanner flag, adjudicated (full disclosure)

- `reviews\P04_QC_R1\RECHECK_NOTES.json` triggered the base64-run heuristic once. Full
  read of the file shows the match is a slash-separated inventory of un-admitted callee
  addresses ("85BFA0/85C280/862850/..." — 160 chars of hex tokens), i.e. analytic QC
  prose, NOT base64-encoded payload. Adjudication: FALSE POSITIVE; file published as-is.

## 3. Content-review read modes (honest coverage statement)

- MECHANICAL FULL-BYTE SCAN: every staged file (see PUB_SCAN methodology; classes as in
  section 1).
- FULL HUMAN READ (read to EOF by the publication auditor): campaign root REPORT.md,
  HANDOFF.md, GATES.json, MANIFEST.json (parent), BODY_ADMISSION_EVENTS.jsonl;
  packages/P04 extract-review set `reviews/P04_QC_R1/RECHECK_NOTES.json`; the excluded
  candidate `packages/P09_EXEC_R1/NAVIGATION_CENSUS.txt` (read to adjudicate its
  exclusion class); the whole postaudit REPORT.md, artifact_index.csv and
  MANIFEST_SHA256.csv; the sealed Q-run REPORT.md (source of the public summary); this
  run's authored SUMMARY.md.
- REPRESENTATIVE SPOT READS validating every remaining file class against the scanner:
  packages/P01_EXEC_R1/CLAIMS.json (claims class), packages/P06_EXEC_R1/REPORT.md
  (package report class), reviews/P01_QC_R1/QC_REPORT.md (QC report class),
  BODY_ADMISSION_LEDGER.json and CAMPAIGN_ARTIFACT_INDEX.csv (ledger/index classes).
  All other staged files are small analytic JSON/CSV metadata (CONTRACT, RUN_STARTED,
  COUNTERS, GATES, BARRIER_BACKLOG, SOURCE_PINS, MEMORY_AND_IDENTITY, artifact_index,
  MANIFEST, COUNTERS_RECHECK, RECHECK_NOTES) machine-validated by the scan classes.
- §14 rule as applied: analytic prose containing SHORT address/mnemonic/offset quotes
  is allowed (these appear inside REPORT/CLAIMS/QC documents and are citations, not
  listings); files that ARE raw listing excerpts (extracts\*.txt, EXTRACT_*.txt) and
  tools are excluded (EXCLUDED_ARTIFACTS.csv).

## 4. Control files of this publication

- This folder (`00_PUBLICATION/`): PUBLICATION_ALLOWLIST.csv (staged content inventory
  with per-file SHA256 and review result), EXCLUDED_ARTIFACTS.csv (everything kept
  local, with reasons), this REDACTION_MAP.md.
- PUBLICATION_MANIFEST.json (written LAST, self-excluded, covering every file of this
  publication commit including this folder, the public summary folder, the postaudit
  projection and the AUDIT_ENTRYPOINT.md edit).
- EOL fidelity: the repository-local git config has core.autocrlf=false (overriding the
  global true) and there is no .gitattributes; staged bytes are committed unchanged
  (CRLF files remain CRLF, LF remain LF).

## 5. What is NOT in this publication (by design)

- The sealed Q package (PE_935_CAND4_Q_CTOR_ARGUMENT_SAVED_R1_20261018) — only the
  corrected public summary is published.
- The remaining postaudit files (6 of 9) — the frozen postaudit package stays local.
- Campaign raw extracts (25 files), tools (3), CONTROL plane (43), FINAL_STOP.json,
  and four analytic-adjacent files outside the dispatch's authorized list
  (ANALYSIS_NOTES.md, CHECKED_SOURCES.json, NAVIGATION_CENSUS.txt, EXTRACT_META.json).
- No executable, DLL, BNT/ARK/VFS/NIF corpus, installer, or any game payload.
