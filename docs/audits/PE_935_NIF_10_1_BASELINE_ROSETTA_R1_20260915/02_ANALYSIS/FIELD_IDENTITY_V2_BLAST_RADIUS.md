# FIELD_IDENTITY_V2_BLAST_RADIUS — C6 correction regression (2026-09-16)

RUN: PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916.

INSTRUMENTS compared (the ONLY behavioral delta is the field-identity
model in `_fields_for`):
- OLD = frozen s06 WorldSliceValidator (bare-FIELD_NAME dedup;
  hypothesis sha 6DB2F1E37E900A2573FEE07B5945B5E25B438066EA0A26AF
  0841540C96693752 unchanged — executed read-only).
- V2 = s14 WorldSliceValidatorV2 (FIELD_IDENTITY_V2: occurrence-
  preserving effective field lists; conditional alternatives remain
  distinct until value-condition evaluation).

This is CORRECTION REGRESSION over the existing 2363 world-slice
files — NOT a new holdout. Evidence:
01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv (2,363 per-file rows)
+ 02_WORK/WORLD_SLICE_V2_AGGREGATE_SUMMARY.json (run-local).

## Denominator and algebra (executed, not extrapolated)

```text
denominator (slice files)            = 2,363
PASS  (V2 closure OK)                 = 2,343
FAIL  (V2 decode fail)                =    20
AMBIGUOUS                             =     0
INFRA_UNRESOLVED (timeout/killed)     =     0
PASS + FAIL + AMBIGUOUS + INFRA_UNRESOLVED = 2,363  (closes exactly)
```

Execution: single chunk, single process, 0 infrastructure stops
(infra_stop=0), wall-clock ~310 s for 2,363 files x 2 decoders; no
file was dropped, no timeout classified as parser failure.

## OLD vs V2 comparison (all 2,363 files)

```text
files_same_closure                    = 2,363  (100%)
files_newly_closing (old FAIL, v2 OK) =        0
files_newly_failing (old OK, v2 FAIL) =        0
files_ambiguous                       =        0
changed_boundaries                    =        0
changed_field_interpretations         =        0
```

- OLD re-executed now REPRODUCES the frozen run's recorded results
  bit-exactly: 2,343 closures; the same 20 blocked files
  (12 x ArkBlockError closure-search-exhausted + 8 x struct.error EOF
  — the AMEND-012 disclosed search-limitation set).
- V2 produces IDENTICAL closure, IDENTICAL per-block boundary arrays
  ([[__start__, __end__] per block] compared per file), IDENTICAL
  canonical per-block value fingerprints (sha256 of the sorted decoded
  block values) — for all 2,363 files.

## Interpretation

closure difference != automatically science correction — here there
IS NO closure difference. The in-slice frozen measurements (TRAIN
1,876/1,890, HOLDOUT 467/473, blocked 20, hypothesis sha, all census
numbers) remain VALID under the corrected instrument; F-14/F-16/F-17
verdicts that rest on in-slice closure measurements are UNAFFECTED.

This matches the schema-level prediction from the C2 census
(01_RAW/DUPLICATE_FIELD_IDENTITY_CENSUS.csv): the only LOAD-BEARING
duplicate-name groups whose types are PHYSICALLY OBSERVED in the PCG
corpus are NiSourceTexture, NiPSysData, NiMeshPSysData and
NiTriShapeData (all inheriting the NiGeometryData "Num Vertices"
group except NiSourceTexture):
- NiTriShapeData (in-slice, high count): the dedup SURVIVOR was the
  `cond "!NiPSysData"` occurrence, which is byte-correct for concrete
  NiTriShapeData — no in-slice effect (empirically confirmed: 0
  changed boundaries).
- NiSourceTexture / NiPSysData / NiMeshPSysData: NOT in the slice
  (the 45 NiSourceTexture blocks live in 5 non-slice files;
  particle-system data types are outside the slice by construction) —
  hence zero in-slice effect, and the defect's physical impact was
  LATENT, demonstrated on BABYLENGUIN (non-PE) and quantified on the
  PCG corpus in the C5 regression: 01_RAW/
  NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv — all 45 blocks PASS
  under V2 (44 EXTERNAL branch + 1 INTERNAL branch; next-block
  GroupID==0 verified after each), of which the 1 INTERNAL-branch
  block (204828.nif blk159, UE=0) is the one whose OLD-model decode
  would have mis-consumed the File Name bytes.
- The latent defect CLASS (lost same-name occurrences for value
  conditions) also covers the NiGeometryData "Num Vertices"
  [NiPSysData] alternative and the orphan compound TexSource "File
  Name" pair (TexSource is referenced by no niobject in HIST — zero
  reach); both are recorded in the census CSV for future work.

Full-corpus non-slice exposure (outside this correction's regression
denominators): the 2,475 non-slice v10.1 files were NOT re-decoded
here (out of the C6 scope); the C5 NiSourceTexture regression covers
the 5 files that physically contain NiSourceTexture blocks. The
NiPSysData-family latent defect remains UNREACHED by the frozen
decoder family by design (unsupported types) — a known limitation,
not a new finding.
