#!/usr/bin/env python3
"""s10_provenance.py — final provenance generation (canonical order §21).

1. SCRIPT_SHA256.csv  (scripts in 00_CONTROL/scripts/)
2. 03_EVIDENCE/README.md
3. 03_EVIDENCE/EVIDENCE_INDEX.csv  (every package file except MANIFEST)
4. 06_REPORT/MANIFEST_SHA256.csv    (every package file incl. evidence index;
   SELF-EXCLUSION L12: MANIFEST_SHA256.csv does not hash itself)
Then re-hash every listed file; zero missing; zero stale.
"""
import csv
import hashlib
import os

PKG = (r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
       r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def all_files():
    out = []
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
        for fn in files:
            if fn.endswith('.pyc'):
                continue
            out.append(os.path.join(root, fn))
    return sorted(out)


def rel(p):
    return os.path.relpath(p, PKG).replace('\\', '/')


def main():
    files = all_files()
    # 1. scripts
    scripts = [p for p in files if p.startswith(
        os.path.join(PKG, '00_CONTROL', 'scripts'))]
    with open(os.path.join(PKG, '00_CONTROL', 'SCRIPT_SHA256.csv'), 'w',
              newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['script_name', 'sha256', 'bytes'])
        for p in scripts:
            w.writerow([rel(p), sha256(p), os.path.getsize(p)])
    # 2. evidence README
    evreadme = os.path.join(PKG, '03_EVIDENCE', 'README.md')
    with open(evreadme, 'w', encoding='utf-8') as f:
        f.write(EVIDENCE_README)
    # 3. evidence index (everything except MANIFEST itself)
    files = all_files()
    idx_rows = []
    for p in files:
        rp = rel(p)
        if rp in ('06_REPORT/MANIFEST_SHA256.csv',
                  '03_EVIDENCE/README.md',
                  '03_EVIDENCE/EVIDENCE_INDEX.csv'):
            continue
        idx_rows.append((rp, sha256(p), os.path.getsize(p)))
    with open(os.path.join(PKG, '03_EVIDENCE', 'EVIDENCE_INDEX.csv'), 'w',
              newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['path', 'sha256', 'bytes', 'role'])
        for rp, h, b in idx_rows:
            role = ('CONTROL' if rp.startswith('00_CONTROL') else
                    'RAW_EVIDENCE' if rp.startswith('01_RAW') else
                    'ANALYSIS' if rp.startswith('02_ANALYSIS') else
                    'EVIDENCE_INDEX_INPUT' if rp.startswith('03_EVIDENCE')
                    else 'REPORT' if rp.startswith('06_REPORT') else 'OTHER')
            w.writerow([rp, h, b, role])
    # 4. manifest (every file except the manifest itself — L12 self-exclusion)
    files = all_files()
    man = os.path.join(PKG, '06_REPORT', 'MANIFEST_SHA256.csv')
    rows = []
    for p in files:
        if os.path.abspath(p) == os.path.abspath(man):
            continue
        rows.append((rel(p), sha256(p), os.path.getsize(p)))
    with open(man, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['path', 'sha256', 'bytes'])
        for rp, h, b in rows:
            w.writerow([rp, h, b])
    # verification pass: rehash everything listed
    missing, stale = [], []
    listed = {rp: h for rp, h, b in rows}
    for p in all_files():
        rp = rel(p)
        if rp == '06_REPORT/MANIFEST_SHA256.csv':
            continue
        if rp not in listed:
            missing.append(rp)
        elif listed[rp] != sha256(p):
            stale.append(rp)
    print(f'files={len(all_files())} manifest_rows={len(rows)} '
          f'missing={missing} stale={stale}')


EVIDENCE_README = """# EVIDENCE — PE_935_NIF_10_1_BASELINE_ROSETTA_R1

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

D:\\Eudoria_Reconstruction\\99_Audits\\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\\02_WORK\\
— per-entry version data, independent type histograms, validation JSON
(includes ~per-file type lists), crosscheck + cross-publisher JSONs.
No proprietary payloads in the repo; raw NIF bytes never leave the corpus
archive except as in-memory reads by the scripts.
"""


if __name__ == '__main__':
    main()
