> PUBLIC SANITIZED PROJECTION: this is the public copy of the sealed private run REPORT. Content is unchanged except (1) UTF-8 mojibake artifacts (double-encoded em-dashes/quotes) were normalized and (2) private absolute paths are retained deliberately as descriptive provenance references. No game payloads, keys or dumps are included.

# REPORT.md — Campaign report: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024 | Assembly JOB: PE2003R3-A1 (FAMILY Q) | Date: 2026-10-24
Author role: executor-assembler (pe-reconstruction worker). This report assembles existing R3 artifacts only — no new binary/game-data reads were performed in A1.

## 1. Executive summary per model

| Field | 296445 | 218757 |
|---|---|---|
| SAME_MODEL_2003_vs_935 | IDENTICAL_BYTES (3-way: ARK == manifest row == M1B3; 108 876 B / 656795D8… / NIF 4.1.0.12 / 155 blocks) | VARIANT_SAME_ID (2003-ARK C13D0873… / 56 535 B / 4.1.0.12 / 62 blocks vs 9.3.5 3E8A22C2… / 57 316 B / 10.1.0.0; manifest row = 9.3.5 payload) |
| Definition | Scripts.ark 4508.obj.dec â†’ IDs 296445+296446 (E18 byte-verified) | Scripts.ark 4057.obj.dec â†’ IDs 218757+218758 (E18 byte-verified) |
| Paired volume | 296446.bvi (1008 B, 21Ã—48 B, CRC 27EE4229) | 218758.bvi (864 B, 18Ã—48 B, CRC 5DD32B83; W1 discovery) |
| Role | CO-NAMED B_Eu_Slum_Building_b047_01 + lens-flare effect rig (7 billboards, texture effect, UV anim); building-class PLAUSIBLE (naming only) | CO-NAMED B_Outpost_me01 (plain mesh 14/1130/526); outpost-exterior PLAUSIBLE (naming only) |
| Loader chain | mountâ†’manager 0x5E7974â†’open_nif 0x520EE0â†’reader FUN_00464F30â†’NIF 0x522010â†’0x5B7170â†’wrapper 0x5EBC1C — all CONFIRMED; definitionâ†’open static-negative (E20) | same COMMON chain; per-model divergence only in the ID constant |
| Spawn/transform | frame 0x06 (BE envelope, LE f32 Ã—3) â†’ FUN_004688d0 â†’ avatar 0x118B â†’ FUN_005030c0 â†’ scene Ã—100.0 — CONFIRMED | same COMMON mechanism |
| Orientation | 3Ã—3 ROW-MAJOR row-vector (vÂ·M) at obj+0x2C; consumers FUN_004193f0 + FUN_00419090; live source UNVERIFIED | same |
| Local locations | NONE (install/Volumes/Scripts/Models negatives with denominators) | NONE (same) |
| TRANSFORM_SOURCE | NETWORK_RUNTIME_ONLY | NETWORK_RUNTIME_ONLY |
| AUTHENTIC_INSTANCE_COUNT (offline) | 0 | 0 |
| PLACEMENT_VERDICT | MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS | same |
| Verdict artifacts | `MODEL_296445_PLACEMENT_VERDICT.json` | `MODEL_218757_PLACEMENT_VERDICT.json` |

## 2. Sources / corpus

- PRIMARY corpus: **PE42_EN_80553A75** — pe42_en.exe installer (CAB MSZip, 80553A75…), 711 files extracted (841 093 330 B), every file hashed into `INSTALL_MANIFEST.csv`. Client = PE.exe 53A6F341… (Project Entropia 4.02.0000 Commercial Open Trial, UPX 1.20, 2003-01-30) — IDENTICAL_BYTES to PE_CD.exe; upx -d product IDENTICAL_BYTES to PE2_unpacked_out.exe 56178993… (the build used for all static RE). Evidence: `PE2003\01_Source_Manifests\{SOURCE_CATALOG,BUILD_IDENTITY,MEDIA_INTEGRITY,BINARY_PROVENANCE_GRAPH}.json`; `PACKETS\R1A\RUN_REPORT_R1A.md`.
- Comparative: ISO NOV2003 (media DEGRADED — 7z exit 2; member ProjectEntropia.zip PASS 4AB9AD40…; inner PE_PCG.exe NSIS_EXTRACT_BLOCKED at block #40); ARK corpus byte-identical across 3 physical copies (PE42 install / 01_Original_Files\ARK / pcg2003_install — after the F1 non-existence claim was rejected by the master's direct hash, ADMISSION seq 5); 50.bnt TWO versions (8E43CD14 vs A6E59EE0 — era split, undecoded).

## 3. Science (what the campaign established)

1. **Loader chain (CONFIRMED)**: archive mount â†’ resource manager (vtable 0x5E7974; 4 open slots nif/bvi/tga/dds; member name = `sprintf("%d")` + extension) â†’ shared ark member reader FUN_00464F30 (hash+CRC gate) â†’ dedicated NIF deserializer (0x522010â†’0x5B7170 "NetI" branch) â†’ root wrapper (0x5EBC1C). Scripts.ark ingest (Blowfish-CBC) â†’ DLOB parse â†’ linker EXTN patch â†’ VM engine trees (E01-E17). Evidence: `RESOURCE_INSTANCE_JOIN_2003.csv`.
2. **Definition binding (CONFIRMED data-side)**: 4508.obj.dec and 4057.obj.dec carry the four model IDs as u32 immediates inside an identical `FEDE <0x14> <id_nif> FDAC <0x14> FEEB <0x08>` attach-resource-pair macro (E18); type-idâ†’definition lookup CONFIRMED (FUN_00441230, 33-callsite census, W3-08).
3. **The one open edge (E08/E20/R3-06)**: definitionâ†’open has **NO static consumer** on build 56178993 — 0 direct callers (verified 3Ã—), 0 qualified virtual dispatch sites (censuses 5776 indirect CALLs / 576444 instructions, multiple pattern variants), holders only via the WinMain stack client; SFO/0x415xxx candidate REJECTED-PRECISELY (scene-node bookkeeping); no 0x7700xxxx interpreter in .text (E19; partial revision: 0x7fffec7x ARE consumed). Best-supported model: bytecode-driven open executed server-side or via a non-token path; next edge DYNAMIC ONLY. Evidence: `PACKETS\R3JOB\RUN_REPORT_R3JOB.md`; `TARGET_CLASS_2003.json`.
4. **Spawn (CONFIRMED)**: network frame type 0x06 â†’ frame dispatcher FUN_005bc5a0 (12 types) â†’ wire parser FUN_00528a40 â†’ engine slot +0x18 FUN_004688d0 â†’ operator_new(0x118) avatar (vtable 0x5E4628) â†’ init chain â†’ scene attach. W2's missing consumer edge closed. Evidence: `OBJECT_LIFECYCLE_2003.json`; JOIN W3-01..W3-03.
5. **Transform rules (CONFIRMED)**: position = 3Ã— f32 LITTLE-ENDIAN inside a BIG-ENDIAN envelope; Ã—100.0 (0x42C80000) storage multiplier at scene attach (obj+0x50/54/58); orientation = 9 f32 3Ã—3 ROW-MAJOR row-vector (vÂ·M, DirectX-style) proven from consumer math; world-compose FUN_004193f0 + dPVS FUN_00419090; live orientation source UNVERIFIED (W3-11). Evidence: `TRANSFORM_DATAFLOW_2003.csv`; `MODEL_*_TRANSFORM_RULES.md`; `AXIS_AND_TERRAIN_CALIBRATION.json`.
6. **Class correction (W2â†’W3)**: 0x5E49B8 (0x54 B) = camera-record class, NOT the instance holder; the 0x488xxx transform consumers operate on the avatar class 0x5E4628. Original rows preserved (append-only). Evidence: JOIN W3-12.
7. **Placement source (NEGATIVE local + CONFIRMED mechanism)**: install = 5 containers + 650 sounds + data.ini only; Volumes.ark 831/831 negative; Scripts static placement NOT_EXISTS corpus-wide (R10 canon); Models local-only â†’ **instance data is NETWORK/RUNTIME ONLY**; authentic locations NOT recoverable from the local 2003 corpus. Evidence: `PLACEMENT_SOURCE_MATRIX.csv`; `MODEL_*_PLACEMENT_VERDICT.json`.
8. **Era discipline**: manifest_2003.csv = MIXED_CORPUS_LOCATOR (row 218757 = 9.3.5 payload — CS06 confirmed physically); no cross-era ID/offset/VA/instance transfer; 9.3.5 relations used only as oracles. Evidence: `CROSS_BUILD_COMPARISON.csv`; `CLAIM_SUPERSESSION.csv`.

## 4. Tools

- `pe2003_model_inspector.py` (SHA 68FDFD21…) — NIF 4.1.0.12 inspector; 155/155 + 62/62 blocks, census match, footer cross-check CONFIRMED; negative tests 5/5.
- `pe2003_case_pipeline.py` (SHA D050627D…) — end-to-end per-model pipeline (locate/extract/verify/references/inspect/report); both models CONFIRMED; explicit NOT_FOUND negative control (296446, denominator 2492).
- `ark_vfs_decoder_f1.py` (SHA 4576965A…) — qualified ARK decoder (reused, not rewritten); negative tests 4/4.
- REPRODUCE_*.md files record the actually executed commands. Evidence: `IMPLEMENTED_TOOLS.json`; `TEST_RESULTS.json`; `REPRODUCE_MODEL_*.md`.

## 5. QC status

**QC_OUTCOME=QC_PARTIAL->QC_CLOSED_AFTER_MASTER_DISPOSITIONS (35/37 PASS; F-01 MASTER-CLR-12, F-02 QC-CLR-11, F-03 MASTER-CLR-13, F-04 fixed, F-05 noted; see QC_FINDINGS.json + PACKETS\QC\QC_REPORT.md; same-model-family disclosure applies)** — this A1 package has NOT yet passed independent QC. `QC_FINDINGS.json` and `MANIFEST_SHA256.csv` are produced by master/QC outside this job. SELF_CHECK (labelled SELF_CHECK, not an independent audit) is recorded in Â§9.

## 6. Obligations

`OBLIGATION_COVERAGE.csv`: O1-O14 all ANSWERED except **O9 = PENDING** (QC/publication by master; this job by design) and **O8 = PARTIAL** (wire-level units/axes answered; world calibration UNANSWERABLE without an anchor; terrain not decoded). Each row carries an evidence path and gap.

## 7. Limits / census

- 11 native Task attempts used of 96 (NATIVE_TASK_CENSUS.json; includes the S1 empty-delivery retry).
- Honest accounting: per-job decompile counts are LOWER_BOUNDs; untracked totals marked UNMEASURED (`BODY_AND_EXPOSURE_LEDGER.json`); I/O consolidated in `READ_AND_IO_LEDGER.jsonl` (22 entries).
- Denominators of the decisive negatives: install file census; Volumes.ark 831 members / 7032 records; Scripts 1936 decoded corpus-wide; Models 2492 members; static censuses 5776 indirect CALL sites / 576444 instructions.
- Not done in this campaign (recorded, not silently omitted): 218757 cross-variant structural diff; terrain decode (both 50.bnt versions catalogued only); Textures.ark member-level extraction; Blowfish re-decode of Scripts (canon reuse); any dynamic/client-run work.

## 8. Pre-existing matrix integrity check (task 17 — verified in this job, not modified)

- `RESOURCE_INSTANCE_JOIN_2003.csv` — 40 lines / 39 edge rows (E01-E21, W3-01..12, R3-01..06); header intact; parsable; backups .bak_r2/.r3bak/.w3bak present. NOT modified by A1.
- `RECORD_LAYOUT_2003.csv` — 79 lines; header intact; parsable; backups .r3bak/.w3bak present. NOT modified by A1.
- `TRANSFORM_DATAFLOW_2003.csv` — 50 lines / 49 data rows; header intact; parsable; backups .w1bak/.w3bak/.r3bak present. NOT modified by A1.
- `PLACEMENT_SOURCE_MATRIX.csv` — 7 lines / 6 matrix rows (M1-M6); header intact; parsable; no backup variants (single-version file). NOT modified by A1.
- JSON artifacts re-validated: all SCIENCE_ROOT JSON files parse (ConvertFrom-Json) including the 10 JSON files written by this job.

## 9. SELF_CHECK (labelled SELF_CHECK — not an independent MASTER audit)

- [x] P1: all 19 assigned deliverables exist and parse (CSV via structured parse, JSON strict, JSONL line-wise) — validation command output retained below in Â§11.
- [x] P2: both CASE files and both PLACEMENT_VERDICT files carry the full status blocks SAME_MODEL / ROLE / JOIN / SOURCE / COUNT / VERDICT.
- [x] P3: every claim in every written file carries an evidence path or an explicit UNVERIFIED/REJECTED/UNMEASURED status; no invented numbers; placement NOT described as reconstructed anywhere.
- [x] P4: OBLIGATION_COVERAGE.csv covers O1-O14 with status + evidence + gap.
- [x] No new binary/data reads (contract scope); writes limited to SCIENCE_ROOT deliverables; pre-existing matrix files untouched (Â§8).
- [x] No nested Tasks; no PE_MASTER_LOOP_STATE; no Git operations (publication not assigned); no MANIFEST_SHA256.csv / QC_FINDINGS.json created (reserved to master/QC).
- [x] Negative controls preserved and cited (F1 4/4 + NOT_FOUND; I1 5/5 + NOT_FOUND; R3JOB census negative control; R10 sensitivity control).
- [x] Corrections ledgered (CORRECTION_LEDGER.json CLR-01..CLR-10) with original rows preserved.

## 10. Publication

**PUBLICATION_STATUS=EXECUTED_POST_SEAL (authoritative record: RECEIPT_ROOT\PUBLICATION_RESULT.json; public projection pe2003/ in eudoria-clean; this REPORT sealed before publication — publication adds no new science)** — to be completed by the master (QC outcome + publication status + MANIFEST_SHA256.csv).

## 11. Parse validation (executed in-run, output verbatim)

Command: see HANDOFF.md Â§E (Import-Csv / ConvertFrom-Json over every CSV/JSON/JSONL deliverable + pre-existing matrices).

```
CSV OK MODEL_296445_INSTANCE_CANDIDATES.csv rows=9
CSV OK MODEL_218757_INSTANCE_CANDIDATES.csv rows=11
CSV OK CROSS_BUILD_COMPARISON.csv rows=10
CSV OK RESOURCE_CATALOG.csv rows=18
CSV OK OBLIGATION_COVERAGE.csv rows=14
CSV OK STAGE_ACCEPTANCE_GATES.csv rows=13
CSV OK RECONSTRUCTION_MATRIX_2003.csv rows=15
CSV OK RESOURCE_INSTANCE_JOIN_2003.csv rows=39
CSV OK RECORD_LAYOUT_2003.csv rows=78
CSV OK TRANSFORM_DATAFLOW_2003.csv rows=49
CSV OK PLACEMENT_SOURCE_MATRIX.csv rows=6
CSV OK HISTORICAL_INSTANCE_CANDIDATES.csv rows=6
JSON OK MODEL_296445_LOAD_TRACE.json
JSON OK MODEL_218757_LOAD_TRACE.json
JSON OK MODEL_296445_PLACEMENT_VERDICT.json
JSON OK MODEL_218757_PLACEMENT_VERDICT.json
JSON OK AXIS_AND_TERRAIN_CALIBRATION.json
JSON OK FRONTIER.json
JSON OK FIRST_MISSING_EDGE.json
JSON OK BODY_AND_EXPOSURE_LEDGER.json
JSON OK CORRECTION_LEDGER.json
JSON OK TARGET_CLASS_2003.json
JSON OK OBJECT_LIFECYCLE_2003.json
JSON OK MODEL_296445_LOCATION_SEARCH.json
JSON OK MODEL_218757_LOCATION_SEARCH.json
JSONL OK READ_AND_IO_LEDGER.jsonl lines=22
FAIL=0
```

(Note: REPORT.md Â§8 line counts are total file lines = data rows + header; Import-Csv reports data rows — both views consistent.)

## 12. Frontier

`FRONTIER.json`: (a) PEFrida dynamic capture of a real model open (FIRST_MISSING_EDGE — `FIRST_MISSING_EDGE.json`: definitionâ†’open for a real instance, DYNAMIC-ONLY); (b) live orientation source; (c) server-side bytecode/instance data model; (d) PCG demo NSIS payload recovery; (e) terrain 50.bnt era split decode.

