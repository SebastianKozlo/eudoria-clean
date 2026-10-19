# REDACTION_MAP - docs/audits/PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019 (this publication commit)

Publication run: PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_PUBLICATION_RECEIPT_R1_20261019 (branch pub/pe935-model-pair-transport-qualification-r1).
This directory is the sanitized projection of the SEALED qualification run
`99_Audits\PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019` (sealed root;
read-only input; never modified by the publication phase). Sealed root
MANIFEST_SHA256.csv = 11,717 B / SHA256
97E468A4B4D8D03270AF164526922887CDE28A3B9D63AEFD50265A97A5B234D5 (111 rows, self-excluded;
re-verified physically during this publication: all 112 files of the sealed tree match
their manifest rows).

## 1. Redactions applied to the published copies: NONE (ZERO-REDACTION PUBLICATION)

- All 62 published files are BYTE-IDENTICAL to the sealed originals: root (7),
  8 science packages x 6 (48), reviews/QC_R2 (7). For every file the published
  SIZE/SHA256 equals the sealed-manifest row of the source (verified per file
  immediately after copying).
- The copied MANIFEST_SHA256.csv files (root + 8 packages + QC_R2) are SOURCE
  METADATA: they document the sealed local originals and are NOT bijection manifests
  of this public directory; the public bijection manifest of this commit is
  00_PUBLICATION/PUBLICATION_MANIFEST.csv.
- Content review of every staged file, classes checked: personal/absolute user paths
  (`X:\Users\...`), secrets/credential patterns, whole instruction listings
  (>20 consecutive instruction rows), raw listing-row density, game payload magic
  strings, binary payload blobs, base64 runs.
- Result: ZERO personal paths, ZERO secrets, ZERO payload files, ZERO whole listings.
  The published reports reference the local raw extracts by pin hash only - kept as
  published.

## 2. Publication-scope decisions (per parent contract section 12)

- `reviews/QC_R2/RUN_STARTED.json` IS published: the contract states "RUN_STARTED.json
  files are publishable only inside QC_R2", so this is the only RUN_STARTED.json in the
  projection. It contains run/scope/role metadata only (no personal paths; the host
  label "WINDEV2407EVAL" is a lab machine identifier already cited in the published
  sealed REPORT.md).
- `packages/P01_DIRECT_R3/RUN_STARTED.json` is EXCLUDED under that same rule.
- ALL extracts\ files (11) stay local: whole saved listing extracts; cited by SIZE/SHA
  in EXCLUDED_ARTIFACTS.csv and referenced in the published reports by pin hash only.
- The CONTROL plane (13 events + 10 plans + 11 requests) stays local: parent control
  plane, not part of the authorized projection; each cited by SIZE/SHA in
  EXCLUDED_ARTIFACTS.csv.
- P01_EXEC_R1 and P01_EXEC_R2 attempt archives stay local: incomplete child attempts
  (empty task results; only CONTRACT.json + RUN_STARTED.json + one extract each),
  each file cited by SIZE/SHA in EXCLUDED_ARTIFACTS.csv.

## 3. Content-review read modes (honest coverage statement)

- FULL READ to EOF (publication auditor): all 7 root files; all 48 package files
  (REPORT/HANDOFF/STAGE_ACCEPTANCE_GATES/CLAIMS/artifact_index/MANIFEST x 8 packages);
  all 7 reviews/QC_R2 files (REPORT, RECHECKS.json, HANDOFF,
  STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv, MANIFEST_SHA256.csv, RUN_STARTED.json).
- MECHANICAL FULL-BYTE SCAN (every byte of every staged file) for the excluded-content
  classes above; no staged file is a raw listing, payload, or binary.
- The excluded files (extracts, CONTROL, attempt archives) were pinned by SIZE/SHA and
  NOT content-published; their exclusion reasons are in EXCLUDED_ARTIFACTS.csv.

## 4. Control files of this publication directory

- 00_PUBLICATION/: PUBLICATION_ALLOWLIST.csv (staged content inventory with per-file
  SHA256 and review result), EXCLUDED_ARTIFACTS.csv (50 exclusions, each cited by
  SIZE/SHA), this REDACTION_MAP.md, PUBLICATION_MANIFEST.csv (written LAST,
  self-excluded; covers this directory plus the two publication-level files
  AUDIT_NOTICE.md and AUDIT_ENTRYPOINT.md of this commit).
- EOL fidelity: repository-local git core.autocrlf=false, no .gitattributes; staged
  bytes are committed unchanged.