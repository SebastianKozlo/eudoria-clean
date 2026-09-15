#!/usr/bin/env python3
"""s05_crosscheck_parser_manifest.py — G2 parser-output echo cross-check.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (§2 sanctioned AFTER census).

The INDEPENDENT census already exists (s03 output). This script compares it
per-file with pcg953_nif_manifest.csv (R61 parser output) and reports
MATCH / MISMATCH / PARSER_MISCLASSIFICATION. The manifest is NEVER an input
to census construction; this is a one-way post-hoc comparison.

Also proves non-echo: scanner result for a scrambled payload differs from
manifest (NC-ECHO negative control) — a corrupted copy of one file is
re-scanned by the independent scanner; the scanner must NOT reproduce the
parser manifest row for that file.
"""
import csv
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE, LOCAL_OUT, REPO_RAW  # noqa: E402
from s03_type_census import scan_101_header  # noqa: E402

MANIFEST = (r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif'
            r'\corpus\pcg953_nif_manifest.csv')


def main():
    mine = json.load(open(
        LOCAL_OUT + r'\02_WORK\pcg953_type_histograms_independent.json',
        encoding='utf-8'))
    parser_rows = {}
    with open(MANIFEST, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['version'] == '10.1.0.0':
                parser_rows[row['name']] = {
                    'num_blocks': int(row['num_blocks']),
                    'histogram': json.loads(row['block_histogram']),
                }
    files_compared = 0
    files_match = 0
    mismatches = []
    type_totals_mine = {}
    type_totals_parser = {}
    for name, m in mine.items():
        files_compared += 1
        p = parser_rows.get(name)
        if p is None:
            mismatches.append({'name': name, 'kind': 'MANIFEST_MISSING'})
            continue
        ph = p['histogram']
        mine_nb = m['num_blocks']
        match = (mine_nb == p['num_blocks'] and
                set(m['type_counts'].items()) == set(
                    (k, v) for k, v in ph.items()))
        if match:
            files_match += 1
        else:
            diffs = {}
            allk = set(m['type_counts']) | set(ph)
            for k in sorted(allk):
                a = m['type_counts'].get(k, 0)
                b = ph.get(k, 0)
                if a != b:
                    diffs[k] = f'independent={a},parser={b}'
            if mine_nb != p['num_blocks']:
                diffs['NUM_BLOCKS'] = (f'independent={mine_nb},'
                                       f'parser={p["num_blocks"]}')
            mismatches.append({'name': name, 'kind': 'COUNT_DIFF',
                               'diffs': diffs})
        for k, v in m['type_counts'].items():
            type_totals_mine[k] = type_totals_mine.get(k, 0) + v
        for k, v in ph.items():
            type_totals_parser[k] = type_totals_parser.get(k, 0) + v
    # per-type totals diff
    type_total_diffs = {}
    for k in sorted(set(type_totals_mine) | set(type_totals_parser)):
        a = type_totals_mine.get(k, 0)
        b = type_totals_parser.get(k, 0)
        if a != b:
            type_total_diffs[k] = {'independent': a, 'parser': b}

    # NC-ECHO negative controls: corrupt HEADER regions of payload copies and
    # re-scan with the independent scanner. The scanner reads ONLY bytes; if
    # it were echoing the manifest, corrupted inputs would still "succeed"
    # with the manifest row. Each control MUST fail the scanner (L19).
    walk = walk_bnt2(ARCHIVE)
    e0 = walk['entries'][0]
    with open(ARCHIVE, 'rb') as f:
        f.seek(e0['offset'])
        data0 = bytearray(f.read(e0['size']))

    controls = []

    def run_ctrl(name, mutator):
        d = bytearray(data0)
        mutator(d)
        try:
            scan_101_header(bytes(d))
            actual = 'SCAN_PASSED_UNEXPECTEDLY'
        except ValueError as ex:
            actual = 'SCAN_FAILED(' + str(ex).split(':')[0] + ')'
        controls.append({'control': name, 'expected': 'SCAN_FAILED*',
                         'actual': actual,
                         'pass': actual.startswith('SCAN_FAILED')})

    def corrupt_version(d):
        d[39:43] = struct.pack('<I', 0xDEADBEEF)

    def corrupt_index_oob(d):
        # blocks_start region: first GroupID is at blocks_start-4; corrupt the
        # LAST array entry instead: find array end via a clean scan
        h = scan_101_header(bytes(data0))
        # type index array ends at h['blocks_start'] - 4 (NumGroups) - 4*N
        # simplest: corrupt NumBlockTypes count to 0xFFFF (sanity fail)
        nl = bytes(d).find(b'\x0A')
        pos = nl + 1 + 4 + 4 + 4
        d[pos:pos + 2] = struct.pack('<H', 0xFFFF)

    def corrupt_numblocks(d):
        nl = bytes(d).find(b'\x0A')
        pos = nl + 1 + 4 + 4
        d[pos:pos + 4] = struct.pack('<I', 0x7FFFFFFF)

    def truncate_mid_header(d):
        del d[60:]

    run_ctrl('NC_ECHO_VERSION_CORRUPT', corrupt_version)
    run_ctrl('NC_ECHO_NUMBLOCKTYPES_CORRUPT', corrupt_index_oob)
    run_ctrl('NC_ECHO_NUMBLOCKS_CORRUPT', corrupt_numblocks)
    run_ctrl('NC_ECHO_TRUNCATE_HEADER', truncate_mid_header)
    echo_pass = all(c['pass'] for c in controls)
    out = {
        'files_compared': files_compared,
        'files_match': files_match,
        'mismatch_count': len(mismatches),
        'mismatch_examples': mismatches[:25],
        'type_total_diffs': type_total_diffs,
        'nc_echo_controls': controls,
        'nc_echo_all_pass': echo_pass,
        'verdict': ('MANIFEST_MATCHES_INDEPENDENT_CENSUS'
                    if files_match == files_compared and
                    not type_total_diffs else
                    'MISMATCH_SEE_DETAILS'),
    }
    os.makedirs(LOCAL_OUT + r'\02_WORK', exist_ok=True)
    with open(LOCAL_OUT + r'\02_WORK\PARSER_MANIFEST_CROSSCHECK.json', 'w',
              encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
