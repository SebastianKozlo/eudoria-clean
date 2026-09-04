# Corpus manifests

## `pcg953_nif_manifest.csv` — PCG 9.3.5 era

Machine-generated inventory of **every NIF** (5,596 rows) in the PCG_9_3_5
corpus (`pcg_install\Data\Models\Models.bnt`, SHA256 `c950a8c2...`). One row
per file; produced by parsing each NIF with the frozen R61 parser (5596/5596
PASS). Full column reference:
[../10-containers-corpus.md](../10-containers-corpus.md).

## `manifest_2003.csv` — 2003 EU-runtime era

Same schema, applied to the extracted 2003 corpus (5,426 rows, 5426/5426
PASS — the R61 canon corpus). Enables era-labeled per-file comparison;
combined with the era-drift census (96.05% byte-identical), any column can
be diffed across eras. Provenance:
`99_Audits\PE_NIF_2003_MANIFEST_R12_20260904_132950\`
(driver SHA256 `8B15EECF...`, hashed before execution).

## Evidence chain (reproduce before trusting)

- 9.3.5 corpus audit: `99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907` (100% parse closure)
- 9.3.5 deep dump: `99_Audits\PE_PCG935_NIF_DEEP_DUMP_R1_20260904_114352`
- 2003 manifest: `99_Audits\PE_NIF_2003_MANIFEST_R12_20260904_132950`
- Era drift: `99_Audits\PE_NIF_ERA_DRIFT_R2_20260904_115051`

These files are DERIVED DOCUMENTATION (regenerable), not corpus bytes —
per the repo git contract, original game files never enter version control.

