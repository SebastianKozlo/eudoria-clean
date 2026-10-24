> PUBLIC SANITIZED PROJECTION: this is the public copy of the sealed private run REPORT. Content is unchanged except (1) UTF-8 mojibake artifacts (double-encoded em-dashes/quotes) were normalized and (2) private absolute paths are retained deliberately as descriptive provenance references. No game payloads, keys or dumps are included.

# HANDOFF.md — PE2003R3-A1 assembly handoff

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024 | JOB: PE2003R3-A1 (FAMILY Q) | Date: 2026-10-24
SCIENCE_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024\

## A. Artifacts created by this job (A1)

| # | Deliverable (relative to SCIENCE_ROOT) | Task |
|---|---|---|
| 1 | MODEL_296445_CASE.md | 1 |
| 2 | MODEL_218757_CASE.md | 1 |
| 3 | MODEL_296445_LOAD_TRACE.json | 2 |
| 4 | MODEL_218757_LOAD_TRACE.json | 2 |
| 5 | MODEL_296445_INSTANCE_CANDIDATES.csv | 3 |
| 6 | MODEL_218757_INSTANCE_CANDIDATES.csv | 3 |
| 7 | MODEL_296445_TRANSFORM_RULES.md | 4 |
| 8 | MODEL_218757_TRANSFORM_RULES.md | 4 |
| 9 | MODEL_296445_PLACEMENT_VERDICT.json | 5 |
| 10 | MODEL_218757_PLACEMENT_VERDICT.json | 5 |
| 11 | TWO_MODEL_COMPARISON.md | 6 |
| 12 | CROSS_BUILD_COMPARISON.csv | 7 |
| 13 | AXIS_AND_TERRAIN_CALIBRATION.json | 8 |
| 14 | RESOURCE_CATALOG.csv | 9 |
| 15 | OBLIGATION_COVERAGE.csv | 10 |
| 16 | FRONTIER.json + FIRST_MISSING_EDGE.json | 11 |
| 17 | STAGE_ACCEPTANCE_GATES.csv | 12 |
| 18 | READ_AND_IO_LEDGER.jsonl | 13 |
| 19 | BODY_AND_EXPOSURE_LEDGER.json | 14 |
| 20 | CORRECTION_LEDGER.json | 15 |
| 21 | RECONSTRUCTION_MATRIX_2003.csv | 16 |
| 22 | REPORT.md | 18 |
| 23 | HANDOFF.md (this file) | 19 |

## B. Pre-existing artifacts verified for existence/integrity (task 17) — NOT modified

- RESOURCE_INSTANCE_JOIN_2003.csv (39 edges; backups .bak_r2/.r3bak/.w3bak)
- RECORD_LAYOUT_2003.csv (backups .r3bak/.w3bak)
- TRANSFORM_DATAFLOW_2003.csv (backups .w1bak/.w3bak/.r3bak)
- PLACEMENT_SOURCE_MATRIX.csv (single version)
- Plus (read, reused, unmodified): TARGET_CLASS_2003.json, OBJECT_LIFECYCLE_2003.json, MODEL_*_LOCATION_SEARCH.json (+ .w3bak), MODEL_*_NIF_STRUCTURE.json, HISTORICAL_INSTANCE_CANDIDATES.csv, TEST_RESULTS.json, IMPLEMENTED_TOOLS.json, CLAIM_SUPERSESSION.csv, KNOWLEDGE_935_SYNTHESIS.md, METHOD_935_TO_2003_REPLAY.csv, HISTORY_INVENTORY.csv, REPRODUCE_MODEL_*.md, ROLE_LEDGER.json, NATIVE_TASK_CENSUS.json, ADMISSION_EVENTS.jsonl, all PACKETS\* run reports and dumps.

## C. External evidence roots referenced (read-only)

- PE2003\01_Source_Manifests\{SOURCE_CATALOG, BUILD_IDENTITY, MEDIA_INTEGRITY, BINARY_PROVENANCE_GRAPH}.json + INSTALL_MANIFEST.csv
- PE2003\03_Archives_and_Decoders\ (decoder + 4 listings + structure dump)
- PE2003\04_Binary_Analysis\ (BINARY_IDENTITY.json, IMPORTS_CENSUS.json, PE2_HEADER_MAP.json, postScripts + SHA records, Ghidra logs)
- PE2003\06_Models_and_Materials\ (TARGET_MODEL_IDENTITY.json, TARGET_ASSET_PAIR.json, MODEL_*_RESOURCE_REFERENCES.csv, extracted NIFs)
- PE2003\07_World_and_Placement\W1\ (DLOB structure decode)
- PE2003\08_Local_Tools\ (inspector, pipeline, run_*_report.json, tests)
- PE2003\09_Research\ (F1, R1B, R2, R3, W1, W2, I1 notes)

## D. PASS predicate self-assessment (A1)

- P1 (all 19 items exist + parseable): PASS (validation command below; output recorded in REPORT.md §11).
- P2 (both cases carry full SAME_MODEL/ROLE/JOIN/SOURCE/COUNT/VERDICT blocks): PASS.
- P3 (no claim without evidence path or UNVERIFIED/REJECTED status): PASS (self-walk performed over all written files).
- P4 (OBLIGATION_COVERAGE complete O1-O14 with evidence): PASS (O9=PENDING by design; O8=PARTIAL honestly).
- RUN_STATUS: JOB_COMPLETE (pending independent QC by master; O9/PENDING_QC, publication PENDING_PUBLICATION).

## E. Validation command (for reproduction of the P1 parse check)

powershell -Command " cd 'D:\Eudoria_Reconstruction\99_Audits\PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024';
  $csv = 'MODEL_296445_INSTANCE_CANDIDATES.csv','MODEL_218757_INSTANCE_CANDIDATES.csv','CROSS_BUILD_COMPARISON.csv','RESOURCE_CATALOG.csv','OBLIGATION_COVERAGE.csv','STAGE_ACCEPTANCE_GATES.csv','RECONSTRUCTION_MATRIX_2003.csv','RESOURCE_INSTANCE_JOIN_2003.csv','RECORD_LAYOUT_2003.csv','TRANSFORM_DATAFLOW_2003.csv','PLACEMENT_SOURCE_MATRIX.csv';
  foreach ($f in $csv) { $r = Import-Csv $f; Write-Host ('CSV OK ' + $f + ' rows=' + $r.Count) };
  $json = 'MODEL_296445_LOAD_TRACE.json','MODEL_218757_LOAD_TRACE.json','MODEL_296445_PLACEMENT_VERDICT.json','MODEL_218757_PLACEMENT_VERDICT.json','AXIS_AND_TERRAIN_CALIBRATION.json','FRONTIER.json','FIRST_MISSING_EDGE.json','BODY_AND_EXPOSURE_LEDGER.json','CORRECTION_LEDGER.json';
  foreach ($f in $json) { Get-Content $f -Raw | ConvertFrom-Json | Out-Null; Write-Host ('JSON OK ' + $f) };
  $i=0; Get-Content READ_AND_IO_LEDGER.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null; $i++ }; Write-Host ('JSONL OK READ_AND_IO_LEDGER.jsonl lines=' + $i) "

## F. Resume instruction

If this run is resumed or audited: (1) verify the 23 A1 files above against §A (existence + parse per §E); (2) independent QC should counter-check claims against the evidence paths embedded in each file (all paths are absolute or SCIENCE_ROOT-relative and were verified to exist in this run); (3) master produces MANIFEST_SHA256.csv and QC_FINDINGS.json (not this job); (4) the single open science edge is FIRST_MISSING_EDGE.json (definition→open for a real instance — dynamic-only); do NOT re-run static censuses on build 56178993 for this edge (exhausted per E20/R3-03/R3-06); (5) terrain work requires explicit authorization (50.bnt era split; see FRONTIER.json item e).
