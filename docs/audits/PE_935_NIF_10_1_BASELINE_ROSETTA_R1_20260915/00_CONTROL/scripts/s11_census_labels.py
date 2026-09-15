#!/usr/bin/env python3
"""s11_census_labels.py — regenerate the baseline_type_present labeling
column of 01_RAW/ENTROPIA_NIF_10_1_TYPE_CENSUS.csv from the packaged s04
output (01_RAW/BASELINE_TYPE_TABLE.csv). (F-QC-3 provenance
normalization; PE-MASTER adjudication; AMEND_LOG AMEND-009+.)

CONTEXT: the packaged s03_type_census.py writes 'PENDING_BASELINE' into
the census column baseline_type_present (s03 L190) — the MEASUREMENT
columns (type_name/blocks/files/min/max/examples/scanner_status) are s03's
physical output, while the baseline-labeling column is a SEPARATE pass.
The packaged census CSV carried the final labels (YES_HIST /
NO_MOD_SCHEMA) from an undisclosed post-s03 edit (disclosed by QC as
AMEND-007/F-QC-3; PE-MASTER adjudicated normalization via this script).

REGENERATION RULE (byte-reproduces the packaged values — verified against
all 76 census rows):
  YES_HIST      iff BASELINE_TYPE_TABLE.csv contains at least one row with
                SOURCE_ORACLE == NIFXML_HIST_0_7_1_1 for this TYPE_NAME
                with APPLIES_TO_10_1_0_0 == True
  NO_MOD_SCHEMA otherwise (type not applicable-defined in the HIST
                baseline table — the two observed UNDEFINED_IN_SCHEMA
                placeholders NiArkBillboardNode + NiVertexMorphExtraData)
Label-semantics note: YES_HIST = defined-and-10.1-applicable in the
HISTORICAL schema (the run's primary baseline oracle, which contains the
5 NiArk ExtraData stubs); the NO_MOD_SCHEMA label (pre-existing, kept
byte-identical) marks types absent from the applicable HIST baseline; both
labeled types are also absent from the MODERN schema (BASELINE_GEN_SUMMARY
observed_not_in_mod_schema includes all 7 Ark/Morph types).

PIPELINE: s03_type_census.py -> s11_census_labels.py produces the packaged
census CSV byte-reproducibly (measurement rows identical to s03's output;
labeling column from BASELINE_TYPE_TABLE.csv).

USAGE:
  python s11_census_labels.py --check   (default; verify byte-identity of
                                         the packaged CSV vs regeneration;
                                         exit 0 = identical, 1 = drift)
  python s11_census_labels.py --write   (rewrite the column in place)
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s02_nif_version_scan import REPO_RAW  # noqa: E402

CENSUS = os.path.join(REPO_RAW, 'ENTROPIA_NIF_10_1_TYPE_CENSUS.csv')
TABLE = os.path.join(REPO_RAW, 'BASELINE_TYPE_TABLE.csv')


def hist_defined_types():
    """Types with >=1 HIST row applicable to 10.1.0.0 (s04 output)."""
    defined = set()
    with open(TABLE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if (row['SOURCE_ORACLE'] == 'NIFXML_HIST_0_7_1_1'
                    and row['APPLIES_TO_10_1_0_0'] == 'True'):
                defined.add(row['TYPE_NAME'])
    return defined


def regenerate(dry_run=True):
    defined = hist_defined_types()
    with open(CENSUS, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    header = rows[0]
    col = header.index('baseline_type_present')
    n_yes = n_no = n_other = 0
    changed = []
    for r in rows[1:]:
        want = 'YES_HIST' if r[0] in defined else 'NO_MOD_SCHEMA'
        if r[col] != want:
            changed.append((r[0], r[col], want))
        if want == 'YES_HIST':
            n_yes += 1
        else:
            n_no += 1
    # byte-exactness check: re-serialize and compare against the file bytes
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    for r in rows[1:]:
        rr = list(r)
        rr[col] = 'YES_HIST' if rr[0] in defined else 'NO_MOD_SCHEMA'
        w.writerow(rr)
    regen_bytes = (','.join(header) + '\r\n' + buf.getvalue()).encode('utf-8')
    with open(CENSUS, 'rb') as f:
        packaged_bytes = f.read()
    identical = regen_bytes == packaged_bytes
    return {'identical': identical, 'n_rows': len(rows) - 1,
            'n_yes_hist': n_yes, 'n_no_mod_schema': n_no,
            'label_drift': changed}


def main():
    mode = '--write' if '--write' in sys.argv else '--check'
    res = regenerate()
    print(f'census rows: {res["n_rows"]}; YES_HIST {res["n_yes_hist"]}; '
          f'NO_MOD_SCHEMA {res["n_no_mod_schema"]}')
    if res['label_drift']:
        print('LABEL DRIFT (packaged vs regeneration rule):')
        for t, old, new in res['label_drift']:
            print(f'  {t}: {old} -> {new}')
    if mode == '--write':
        if not res['identical']:
            # apply the regenerated column by full rewrite from the rule
            defined = hist_defined_types()
            with open(CENSUS, newline='', encoding='utf-8') as f:
                rows = list(csv.reader(f))
            col = rows[0].index('baseline_type_present')
            with open(CENSUS, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(rows[0])
                for r in rows[1:]:
                    rr = list(r)
                    rr[col] = ('YES_HIST' if rr[0] in defined
                               else 'NO_MOD_SCHEMA')
                    w.writerow(rr)
            print('REWRITTEN.')
        else:
            print('already byte-identical; no write needed.')
        return 0
    print('BYTE-IDENTICAL' if res['identical'] else 'BYTE MISMATCH')
    return 0 if res['identical'] else 1


if __name__ == '__main__':
    sys.exit(main())
