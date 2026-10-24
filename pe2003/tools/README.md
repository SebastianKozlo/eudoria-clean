# Tools — PE2003 public copies

Own-code tools of the R3 campaign, sanitized for publication: no secrets,
no embedded game data, no hard-coded private corpus paths (the pipeline takes
all paths as CLI parameters/config; the inspector and the ARK decoder always
took paths as arguments).

Dependency: Python 3 standard library only (no third-party packages).

## ark_vfs_decoder_f1.py

ARK (ZIP-clone, `AK` magic) archive decoder: local-header chain + central
directory + EOCD cross-check, per-member CRC32 verification, member
extraction with SHA256, full Volumes.ark structural dump. Negative tests 4/4
in the campaign. Qualified with the caveat documented in the file header
(the older skill parser's u32 name_len@26 read works only because
extra_len==0).

```
python ark_vfs_decoder_f1.py list       <ark> <out_csv>
python ark_vfs_decoder_f1.py extract    <ark> <outdir> <name> [<name>...]
python ark_vfs_decoder_f1.py verify-crc <ark>
python ark_vfs_decoder_f1.py volumes-dump <ark> <out_csv>
```

## pe2003_model_inspector.py

NIF 4.1.0.12 (0x0401000C) inspector: header, block census (inline
type-string chain), strict per-block field parse with explicit statuses
(FIELDS_CONFIRMED / PARTIAL_FIELDS_OPAQUE_TAIL / UNKNOWN_TYPE / TRUNCATED),
hierarchy, local + composed world transforms, materials, geometry
AABBs, extra data, footer cross-check, asset-role classification
(CO-NAMED / PLAUSIBLE / UNVERIFIED — no unproven labels). Empirical
single-instance fits carry UNVERIFIED_FIELD notes (fit_calibration).

```
python pe2003_model_inspector.py <file.nif> [--json out.json]
```

Campaign results: 296445.nif 155/155 blocks, 218757.nif 62/62 blocks, both
census-match + footer cross-check CONFIRMED; negative tests 5/5
(truncated/unsupported-version/garbage/empty/positive-control).

## pe2003_case_pipeline.py

End-to-end per-model pipeline: locate `{id}.nif` in Models.ark via the F1
decoder, extract, SHA256+CRC32 verify, explicit-reference scan (member names
in 4 ARK listings; U32LE+ASCII in decoded Scripts blobs; raw-payload
negative-control scans of Models/Scripts/Volumes), structure inspection via
the inspector, per-section status report. Textures.ark payload scan is
SKIPPED_SCOPE (member names only). Instance/transform candidates are
recorded UNVERIFIED — an explicit resource reference is NOT a placement claim.

PUBLIC COPY NOTE: the executed campaign tool had fixed private paths in its
CONFIG; this public copy is path-parameterized (analysis logic unchanged).
Executed-original SHA256:
D050627DBFCAE198FFE9AD9A9B14328E126D02C4B2D9D8CF9DA17F872359B38B.

```
python pe2003_case_pipeline.py 296445 \
    --ark-root <install Data dir> \
    --listings-dir <dir with the 4 *_ark_full_listing.csv> \
    --decoded-scripts-dir <dir with decoded Scripts blobs> \
    --f1-decoder ark_vfs_decoder_f1.py \
    --inspector pe2003_model_inspector.py \
    --extract-dir <out> --report-dir <out> --science-root <out>
# or: --config config.json with the same keys (ark_root, listings_dir, ...)
```

## Boundaries

- These tools expect the PRIVATE corpus (install Data tree, decoded Scripts
  blobs) which is NOT published here; you must have your own Project
  Entropia 2003 corpus. No game payloads are included in this repository.
- The decoded Scripts blobs consumed by the pipeline reference-scan stage are
  a read-only reuse of a prior canonical Blowfish-CBC decode; the decode
  itself is not part of this repository and no key material is published.
- Known limits (documented in the campaign): no third-parser cross-check
  available for NIF 4.1.0.12 NiArk* files (PyFFI cannot parse them);
  single-instance fitted field grammars carry UNVERIFIED_FIELD status.
