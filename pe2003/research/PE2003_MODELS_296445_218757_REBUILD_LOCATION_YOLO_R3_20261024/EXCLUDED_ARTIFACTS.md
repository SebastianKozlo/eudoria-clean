# EXCLUDED_ARTIFACTS — what was NOT published and why

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Sanitization policy: own documentation, hashes, offsets/VAs, structural
facts and own path-parameterized code ARE published; the items below are
NOT, with reasons.

## Excluded by class (proprietary / payload / private-provenance)

| Class | Examples (descriptive only) | Reason |
|---|---|---|
| Game binaries & installers | PE.exe, PE_CD.exe, PE2_unpacked_out.exe, PE_PCG.exe, pe42_en.exe, ISO, MSI | proprietary software; local-only rule |
| Game data payloads | Models.ark / Textures.ark / Scripts.ark / Volumes.ark and all members; 296445.nif, 218757.nif, 296446.bvi, 218758.bvi, extracted copies; 50.bnt both versions | game data; local-only rule |
| Decoded Scripts blobs | the 1937-blob decoded corpus (4508.obj.dec, 4057.obj.dec, …) | game data (decoded payload); local-only rule |
| Raw listings / dumps | *_ark_full_listing.csv (4), Volumes_ark_structure_dump.csv, INSTALL_MANIFEST.csv, w*_dump*.txt, r3_dump*.txt, raw disassembly / decompile exports | member listings reveal corpus contents; dumps are raw proprietary data |
| Keys / crypto material | Blowfish key material, per-connection key derivations | secrets; local-only rule |
| QC temp copies & internal evidence | isolated tool re-execution outputs, own-code parse outputs, hash transcripts | transient internal evidence; results summarized in QC_AND_PROCESS_SUMMARY.md instead |
| DB / config / env / authoring prompts | campaign CONTRACT.md, dispatch ledgers, prompt files | private process/provenance data |
| Private control/science files not required for the public projection | NATIVE_TASK_CENSUS.json, ROLE_LEDGER.json, ADMISSION_EVENTS.jsonl, BODY_AND_EXPOSURE_LEDGER.json, READ_AND_IO_LEDGER.jsonl, STAGE_ACCEPTANCE_GATES.csv, MANIFEST_SHA256.csv, QC_FINDINGS.json, PACKETS\* (12 job dirs + QC dir), CORRECTION_LEDGER.json, CLAIM_SUPERSESSION.csv, KNOWLEDGE_935_SYNTHESIS.md, METHOD_935_TO_2003_REPLAY.csv, HISTORY_INVENTORY.csv, HISTORICAL_INSTANCE_CANDIDATES.csv, OBJECT_LIFECYCLE_2003.json, TARGET_CLASS_2003.json, AXIS_AND_TERRAIN_CALIBRATION.json, RECORD_LAYOUT_2003.csv, TRANSFORM_DATAFLOW_2003.csv, PLACEMENT_SOURCE_MATRIX.csv, RESOURCE_INSTANCE_JOIN_2003.csv, RECONSTRUCTION_MATRIX_2003.csv, RESOURCE_CATALOG.csv, OBLIGATION_COVERAGE.csv, CROSS_BUILD_COMPARISON.csv, MODEL_*_LOAD_TRACE.json, MODEL_*_LOCATION_SEARCH.json, MODEL_*_NIF_STRUCTURE.json, MODEL_*_PLACEMENT_VERDICT.json, MODEL_*_INSTANCE_CANDIDATES.csv, MODEL_*_TRANSFORM_RULES.md, REPRODUCE_MODEL_*.md, FIRST_MISSING_EDGE.json, TEST_RESULTS.json, run_*_report.json, tests\* | full science packages remain private; the public projection publishes the sanitized REPORT/HANDOFF copies + condensed summaries (DERIVED_CLAIMS, TRANSFORM_AND_MODEL_JOIN, PLACEMENT_STATUS, FORMAT_COVERAGE, BUILD_IDENTITY_SUMMARY, PUBLIC_SOURCE_SUMMARY, QC_AND_PROCESS_SUMMARY, NEXT_FRONTIER) |
| Tests directory | tests\run_negative_tests.py + fixtures + results | fixtures are crafted copies of game payloads; results summarized in tools/README.md |

## Schemas

No custom schema files (JSON Schema / ksy / hexpat) were authored by this
campaign — the `schemas/` directory is intentionally omitted; the empirical
format facts live in `docs/formats.md` and the tool sources.

## Disclosure

- The published REPORT.md/HANDOFF.md are sanitized copies of the sealed
  private originals (mojibake normalized; a public-projection header
  prepended); their content otherwise reflects the sealed run package.
- The published tools are the campaign's own code: ark_vfs_decoder_f1.py and
  pe2003_model_inspector.py are byte-identical copies;
  pe2003_case_pipeline.py is a path-parameterized public copy (analysis
  logic unchanged; executed-original SHA256 recorded in tools/README.md).
