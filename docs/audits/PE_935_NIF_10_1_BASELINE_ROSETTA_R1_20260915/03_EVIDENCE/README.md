# EVIDENCE — PE_935_NIF_10_1_BASELINE_ROSETTA_R1

## How to re-derive any load-bearing claim (bytes → script → output)

- Corpus anchor (G0/G1): run s01_bnt2_walk.py --walk <Models.bnt> and
  s02_nif_version_scan.py; expect 5596 entries and 4838/757/1 versions
  (NIF_VERSION_CENSUS.csv; BNT2_WALK_SUMMARY.json).
- Type census (G5): run s03_type_census.py THEN s11_census_labels.py
  (baseline-labeling pass; F-QC-3 provenance normalization, AMEND-011);
  expect 76 types / 364,062 blocks and a byte-reproducible packaged
  ENTROPIA_NIF_10_1_TYPE_CENSUS.csv (measurement rows = s03 output;
  baseline_type_present column regenerated from BASELINE_TYPE_TABLE.csv;
  TYPE_CENSUS_SUMMARY.json in 99_Audits workdir).
- Parser-echo cross-check (G2): run s05_crosscheck_parser_manifest.py;
  expect 4838/4838 MATCH + 4/4 NC-ECHO controls.
- Baseline (G4): run s04_nifxml_baseline.py; BASELINE_TYPE_TABLE.csv.
- Closure validation (G6/G7): run s07_full_validation.py ALL with the
  FROZEN s06+s04 (hypothesis_sha 6DB2F1E3...); expect TRAIN 1876/1890,
  HOLDOUT 467/473 (WORLD_SLICE_VALIDATION.json; HOLDOUT_RESULTS.csv).
- Cross-publisher (§14): run s08_cross_publisher_test.py; EE2 lodtest
  CLOSURE_OK (CROSS_PUBLISHER_TEST.json).
- Matrices (G8-G10): run s09_matrices.py.
- ArkTexture zero-count re-derivation (F-14 retraction evidence,
  AMEND-009): run s12_arktexture_zero_count_rederivation.py; expect 32
  in-slice zero-count blocks (25x(3,1,0,0) + 7x(3,0xFFFFFF00,0xFF,0)) +
  24 deviation blocks (18 zero-count + 6 true-count-1/2), 27 fake
  entries, and byte-exact reproduction of the recorded ArkTexture
  evidence aggregates (ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv;
  ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv; summary JSON in the workdir).
- Provenance: run s10_provenance.py (regenerates this chain; any later
  edit requires an AMEND_LOG_R1.md entry per §20/§21).

## Where the raw intermediates live (NOT in the repo)

D:\Eudoria_Reconstruction\99_Audits\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\02_WORK\
— per-entry version data, independent type histograms, validation JSON
(includes ~per-file type lists), crosscheck + cross-publisher JSONs.
No proprietary payloads in the repo; raw NIF bytes never leave the corpus
archive except as in-memory reads by the scripts.
