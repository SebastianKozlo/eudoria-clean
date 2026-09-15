#!/usr/bin/env python3
"""s02_nif_version_scan.py — independent NIF version census for Models.bnt.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915.

ANTI-CIRCULARITY: reads ONLY physical Models.bnt bytes via the run-local
s01 walker. Does NOT consult pcg953_nif_manifest.csv, R61, NifModelReader.js,
or docs claims (docs/nif/README.md denominators are compared only AFTER the
independent census exists, as a cross-check).

Per entry: locate payload (offset,size), read, detect zlib compression,
parse NIF header: HeaderString (0x0A-terminated ASCII line) + Version u32 LE.
Version classification (from physical bytes only):
  0x0A010000 -> 10.1.0.0 | 0x0401000C -> 4.1.0.12 | 0x04000002 -> 4.0.0.2
  anything else -> OTHER:<hex> (recorded; census must classify every entry)
Header-string/version-u32 text cross-check recorded as text_version_match.

FAIL-CLOSED: any entry whose header cannot be parsed is recorded in the
failures CSV with a reason; census integrity: SCANNED + FAILED == entries.
"""
import csv
import hashlib
import json
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402

ARCHIVE = r'D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt'
LOCAL_OUT = (r'D:\Eudoria_Reconstruction\99_Audits'
             r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915')
REPO_RAW = (r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
            r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\01_RAW')

KNOWN = {0x0A010000: '10.1.0.0', 0x0401000C: '4.1.0.12', 0x04000002: '4.0.0.2'}
ZLIB_MAGICS = (b'\x78\x01', b'\x78\x5E', b'\x78\x9C', b'\x78\xDA')


def parse_nif_header(data):
    """Return (header_string, version_u32, err). HeaderString is a line."""
    if len(data) < 8:
        return None, None, 'E_TOO_SMALL'
    nl = data.find(b'\x0A')
    if nl < 0 or nl > 256:
        return None, None, 'E_NO_HEADER_NEWLINE'
    try:
        hs = data[:nl].decode('ascii')
    except UnicodeDecodeError:
        return None, None, 'E_HEADER_ASCII'
    pos = nl + 1
    if pos + 4 > len(data):
        return None, None, 'E_SHORT_VERSION'
    version = struct.unpack('<I', data[pos:pos + 4])[0]
    return hs, version, None


def main():
    walk = walk_bnt2(ARCHIVE)
    entries = walk['entries']
    with open(ARCHIVE, 'rb') as f:
        rows = []
        failures = []
        counts = {}
        for e in entries:
            f.seek(e['offset'])
            raw = f.read(e['size'])
            if len(raw) != e['size']:
                failures.append({'entry_index': e['index'], 'name': e['name'],
                                 'reason': 'E_PAYLOAD_READ',
                                 'detail': f'{len(raw)}/{e["size"]}'})
                continue
            sha_raw = hashlib.sha256(raw).hexdigest().upper()
            compression = 'raw'
            data = raw
            if raw[:2] in ZLIB_MAGICS:
                try:
                    data = zlib.decompress(raw)
                    compression = 'zlib'
                except zlib.error as zerr:
                    hs, ver, err = parse_nif_header(raw)
                    if err is None and ver in KNOWN:
                        compression = 'raw(suspicious-zlib-magic:%s)' % zerr
                    else:
                        failures.append({'entry_index': e['index'],
                                         'name': e['name'],
                                         'reason': 'E_ZLIB_DECOMPRESS',
                                         'detail': str(zerr)})
                        continue
            sha_plain = (hashlib.sha256(data).hexdigest().upper()
                         if compression == 'zlib' else sha_raw)
            hs, ver, err = parse_nif_header(data)
            if err is not None:
                failures.append({'entry_index': e['index'], 'name': e['name'],
                                 'reason': err, 'detail': f'comp={compression}'})
                continue
            label = KNOWN.get(ver, 'OTHER')
            # header-string version text cross-check
            tv_match = ''
            for tok in ('Version ',):
                if tok in hs:
                    tv_match = hs.split(tok, 1)[1].strip()
                    break
            tv_ok = ''
            if label != 'OTHER' and tv_match:
                tv_ok = 'MATCH' if tv_match == label else 'MISMATCH'
            counts[label] = counts.get(label, 0) + 1
            rows.append({
                'entry_index': e['index'], 'name': e['name'],
                'size_stored': e['size'], 'offset': e['offset'],
                'size_plain': len(data),
                'compression': compression,
                'sha256_stored': sha_raw, 'sha256_plain': sha_plain,
                'header_string': hs,
                'version_hex': f'0x{ver:08X}',
                'version_label': label,
                'header_version_text': tv_match,
                'text_version_match': tv_ok,
                'field_c': f'0x{e["field_c"]:08X}',
                'field_d': f'0x{e["field_d"]:08X}',
                'scan_status': 'SCANNED',
            })
    os.makedirs(LOCAL_OUT + r'\02_WORK', exist_ok=True)
    with open(LOCAL_OUT + r'\02_WORK\per_entry_versions.json', 'w',
              encoding='utf-8') as f:
        json.dump(rows, f, indent=1)
    # census CSV (repo)
    csv_path = os.path.join(REPO_RAW, 'NIF_VERSION_CENSUS.csv')
    cols = ['entry_index', 'name', 'size_stored', 'offset', 'size_plain',
            'compression', 'sha256_stored', 'sha256_plain', 'header_string',
            'version_hex', 'version_label', 'header_version_text',
            'text_version_match', 'field_c', 'field_d', 'scan_status']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})
    fail_path = os.path.join(REPO_RAW, 'PHYSICAL_SCAN_FAILURES.csv')
    with open(fail_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['entry_index', 'name', 'reason',
                                          'detail'])
        w.writeheader()
        for r in failures:
            w.writerow(r)
    total = walk['num_entries']
    summary = {
        'archive': ARCHIVE,
        'archive_sha256_remeasure_note': 'S0 pinned externally; see RUN_CONTRACT',
        'entries': total, 'scanned': len(rows), 'failed': len(failures),
        'integrity_ok': len(rows) + len(failures) == total,
        'version_counts': counts,
        'compression_counts': {},
        'text_version_mismatches': sum(
            1 for r in rows if r['text_version_match'] == 'MISMATCH'),
        'failures': failures,
    }
    for r in rows:
        key = r['compression']
        summary['compression_counts'][key] = (
            summary['compression_counts'].get(key, 0) + 1)
    os.makedirs(REPO_RAW, exist_ok=True)
    with open(os.path.join(REPO_RAW, 'BNT2_WALK_SUMMARY.json'), 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({k: summary[k] for k in
                      ('entries', 'scanned', 'failed', 'integrity_ok',
                       'version_counts', 'compression_counts',
                       'text_version_mismatches')}, indent=2))


if __name__ == '__main__':
    main()
