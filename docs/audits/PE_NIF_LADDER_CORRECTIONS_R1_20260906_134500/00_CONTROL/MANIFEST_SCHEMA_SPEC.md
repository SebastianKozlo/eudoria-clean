# MANIFEST_SCHEMA_SPEC.md — artifact_index.csv for all run packages (authoritative from 2026-09-06)
Origin: PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500 TM-8 (post-audit F4: the K2/K3 manifests were malformed).

## Ordinary rows (package files)
Columns: artifact,role,sha256 (exactly 3 fields).
- Written by a proper RFC-4180 CSV writer: fields quoted whenever they contain a comma, quote or newline; one record per line; never concatenated records.
- artifact = a path RELATIVE to the run package root (forward slashes); the file MUST exist in the package.
- sha256 = exactly 64 hex characters; MUST equal the physical hash of the file.
- The manifest EXCLUDES its own row (self-hash impossible — documented precedent).
- Duplicates forbidden: each artifact path exactly once.

## Symbolic external-source rows (originals NOT in the package)
Never mixed into ordinary rows. A SEPARATE section after a comment line "# external sources":
Columns: source_id,kind,era,physical_path,sha256
- kind = external_source; era = the era label (e.g. PCG_9_3_5 / 2003); physical_path = the full local path of the read-only original; sha256 = 64-hex of the physical file.

## Validation gate (machine-checkable; every run asserts it before commit)
1. Parse with a STANDARD CSV parser (no custom splitting).
2. Assert every ordinary row has exactly 3 fields; sha256 matches ^[0-9a-fA-F]{64}$; the artifact path exists in the package; the physical hash equals the row.
3. Assert no duplicate artifact paths; no missing files; every external-source row matches its sub-schema.
4. Negative tests (unit-tested once per run with synthetic fixtures, each must FAIL the gate): (a) unquoted comma in a field; (b) missing newline between records; (c) missing file; (d) malformed hash; (e) unsupported symbolic path shape; (f) duplicate row.
FAIL of any assertion = the package FAILS (fail-closed).
