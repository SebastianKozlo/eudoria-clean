# REDACTION_MAP - docs/audits/PE_935_BUILDING_PLACEMENT_5H_DEEP_POSTAUDIT_R1_20261019 (this publication commit)

Publication run: PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_PUBLICATION_RECEIPT_R1_20261019 (branch pub/pe935-model-pair-transport-qualification-r1).
This directory is the sanitized projection of the LOCAL postaudit run
`99_Audits\PE_935_BUILDING_PLACEMENT_5H_DEEP_POSTAUDIT_R1_20261019` (frozen input; never
modified by the publication phase).

## 1. Redactions applied to the published copies: NONE (ZERO-REDACTION PUBLICATION)

- All 19 files are BYTE-IDENTICAL to the local source files. For every file the published
  SIZE/SHA256 equals the local original (verified per file immediately after copying;
  the local source MANIFEST_SHA256.csv is itself published here as SOURCE METADATA -
  it documents the local original, it is NOT the bijection manifest of this public
  directory; the public bijection manifest of this commit is
  00_PUBLICATION/PUBLICATION_MANIFEST.csv).
- Content review of every staged file, classes checked: personal/absolute user paths
  (`X:\Users\...`), secrets/credential patterns, whole instruction listings
  (>20 consecutive instruction rows), raw listing-row density, game payload magic
  strings, binary payload blobs, base64 runs.
- Result: ZERO personal paths, ZERO secrets, ZERO payload files, ZERO whole listings.
  Short analytic instruction quotations (1-9 rows) inside REPORT.md/CLAIMS-like
  documents are citations, not listings, and are retained (same rule as the 2265ec6
  publication).

## 2. One scanner flag, adjudicated (full disclosure)

- `PUBLICATION_CONTENT_ADJUDICATION.json` matches the `C:\Users\...` heuristic once.
  Full read shows the match is the literal policy-example string "C:\Users\..." (no
  username, no real path) inside the adjudication text that itself documents the same
  false positive for the 2265ec6 publication. Adjudication: FALSE POSITIVE; file
  published byte-identical. No redaction needed (nothing personal is disclosed).

## 3. Content-review read modes (honest coverage statement)

- FULL READ to EOF (publication auditor): REPORT.md, HANDOFF.md, CLAIM_DISPOSITION.csv,
  STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv, ADMISSION_FINDINGS.json,
  CONTROL_AND_CLOCK.json, COUNTERMODELS.json, FINAL_SOURCE_RECHECK.json,
  NESTED_MANIFEST_RECHECK.json, PUBLICATION_CONTENT_ADJUDICATION.json,
  PUBLICATION_RECHECK.json, RAW_REDERIVATION.json, SOURCE_RECHECK.json,
  recheck_nested.py, audit_campaign.py, MANIFEST_SHA256.csv (18 rows).
- MECHANICAL FULL-BYTE SCAN + STRUCTURAL PARSE + BOUNDED INSPECTION (not a
  line-by-line human read): CHECKER_DIAGNOSTICS_V1.json (87,409 B) and INTEGRITY.json
  (60,155 B) - both are machine-generated manifest-checker outputs (file pins and
  schema diagnostics; no listing rows, no personal paths, verified by the mechanical
  scan over every byte plus JSON structure parse of parent/nested/pins/checker_revision
  keys). This is disclosed as BOUNDED_INSPECTION read mode for these two files.

## 4. Control files of this publication directory

- 00_PUBLICATION/: PUBLICATION_ALLOWLIST.csv (staged content inventory with per-file
  SHA256 and review result), EXCLUDED_ARTIFACTS.csv (zero exclusions for this source),
  this REDACTION_MAP.md, PUBLICATION_MANIFEST.csv (written LAST, self-excluded; covers
  this directory plus the two publication-level files AUDIT_NOTICE.md and
  AUDIT_ENTRYPOINT.md of this commit).
- EOL fidelity: repository-local git core.autocrlf=false, no .gitattributes; staged
  bytes are committed unchanged.