#!/usr/bin/env python3
"""s03_type_census.py — physical NIF 10.1.0.0 type census (independent).

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (§6, G5).

ANTI-CIRCULARITY: census is built ONLY from physical bytes of Models.bnt via
run-local s01 walker + this run's header decoder (engine-source-informed:
HeaderString line, Version u32, UserVersion u32, NumBlocks u32, NumBlockTypes
u16, BlockTypes SizedString[], BlockTypeIndex u16[NumBlocks], NumGroups u32,
GroupSize u32[NumGroups]). NOT from R61, NOT from pcg953_nif_manifest.csv,
NOT from NifModelReader.js.

Fail-closed per file (any violation -> FAIL row, file excluded from census,
counted in PHYSICAL_SCAN_FAILURES):
  header too small, no newline, bad ascii, wrong version for this scanner,
  array index >= numblocktypes, blocktype-name length out of [1,256],
  short read anywhere.

Denominator integrity: SCANNED + FAILED == 4838 (the 10.1 files).
"""
import csv
import json
import os
import struct
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE, LOCAL_OUT, REPO_RAW  # noqa: E402

V10 = 0x0A010000


def scan_101_header(data):
    """Parse the 10.1 header through NumGroups. Return dict or raise."""
    if len(data) < 12:
        raise ValueError('E_TOO_SMALL')
    nl = data.find(b'\x0A')
    if nl < 0 or nl > 256:
        raise ValueError('E_NO_HEADER_NEWLINE')
    hs = data[:nl].decode('ascii')
    pos = nl + 1
    if pos + 4 > len(data):
        raise ValueError('E_SHORT_VERSION')
    version = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    if version != V10:
        raise ValueError(f'E_NOT_10_1:{version:08X}')
    if pos + 4 > len(data):
        raise ValueError('E_SHORT_USERVER')
    user_version = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    if pos + 4 > len(data):
        raise ValueError('E_SHORT_NUMBLOCKS')
    num_blocks = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    if num_blocks > 1_000_000:
        raise ValueError(f'E_NUMBLOCKS_SANITY:{num_blocks}')
    if pos + 2 > len(data):
        raise ValueError('E_SHORT_NUMBLOCKTYPES')
    num_block_types = struct.unpack('<H', data[pos:pos + 2])[0]
    pos += 2
    if num_block_types == 0 or num_block_types > 4096:
        raise ValueError(f'E_NUMBLOCKTYPES_SANITY:{num_block_types}')
    names = []
    for i in range(num_block_types):
        if pos + 4 > len(data):
            raise ValueError(f'E_SHORT_TYPELEN:{i}')
        ln = struct.unpack('<I', data[pos:pos + 4])[0]
        pos += 4
        if not 1 <= ln <= 256:
            raise ValueError(f'E_TYPELEN_RANGE:{i}:{ln}')
        if pos + ln > len(data):
            raise ValueError(f'E_SHORT_TYPE:{i}')
        nm = data[pos:pos + ln].decode('ascii')
        pos += ln
        names.append(nm)
    idx = []
    for i in range(num_blocks):
        if pos + 2 > len(data):
            raise ValueError(f'E_SHORT_IDX:{i}')
        t = struct.unpack('<H', data[pos:pos + 2])[0]
        pos += 2
        if t >= num_block_types:
            raise ValueError(f'E_IDX_OOB:{i}:{t}>={num_block_types}')
        idx.append(t)
    if pos + 4 > len(data):
        raise ValueError('E_SHORT_NUMGROUPS')
    num_groups = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    if num_groups > 1_000_000:
        raise ValueError(f'E_NUMGROUPS_SANITY:{num_groups}')
    group_sizes = []
    for i in range(num_groups):
        if pos + 4 > len(data):
            raise ValueError(f'E_SHORT_GROUPSIZE:{i}')
        group_sizes.append(struct.unpack('<I', data[pos:pos + 4])[0])
        pos += 4
    first_group_id = None
    if num_blocks > 0:
        if pos + 4 > len(data):
            raise ValueError('E_SHORT_GROUPID0')
        first_group_id = struct.unpack('<I', data[pos:pos + 4])[0]
        pos += 4
    return {
        'header_string': hs, 'version': version, 'user_version': user_version,
        'num_blocks': num_blocks, 'num_block_types': num_block_types,
        'block_types': names, 'block_type_index': idx,
        'num_groups': num_groups, 'group_sizes': group_sizes,
        'first_block_group_id': first_group_id, 'blocks_start': pos,
    }


def main():
    walk = walk_bnt2(ARCHIVE)
    type_stats = {}      # type_name -> {blocks, files, min_b, max_b, examples}
    per_file = []
    failures = []
    scanned = 0
    total_blocks = 0
    user_versions = Counter()
    num_groups_dist = Counter()
    group_id_first_dist = Counter()
    name_histos = {}
    with open(ARCHIVE, 'rb') as f:
        for e in walk['entries']:
            f.seek(e['offset'])
            data = f.read(e['size'])
            if len(data) != e['size']:
                failures.append({'entry_index': e['index'], 'name': e['name'],
                                 'reason': 'E_PAYLOAD_READ',
                                 'detail': 'type-scan'})
                continue
            nl = data.find(b'\x0A')
            ver = None
            if nl >= 0 and nl + 5 <= len(data):
                ver = struct.unpack('<I', data[nl + 1:nl + 5])[0]
            if ver != V10:
                continue  # cross-version diagnostic files: out of census scope
            try:
                h = scan_101_header(data)
            except ValueError as ex:
                failures.append({'entry_index': e['index'], 'name': e['name'],
                                 'reason': 'E_TYPE_SCAN:' + str(ex),
                                 'detail': f'v={ver:08X}'})
                continue
            scanned += 1
            counts = Counter(h['block_types'][t] for t in h['block_type_index'])
            total_blocks += h['num_blocks']
            user_versions[h['user_version']] += 1
            num_groups_dist[h['num_groups']] += 1
            group_id_first_dist[h['first_block_group_id']] += 1
            for tn, c in counts.items():
                st = type_stats.setdefault(tn, {'blocks': 0, 'files': 0,
                                                'min_b': None, 'max_b': 0,
                                                'examples': []})
                st['blocks'] += c
                st['files'] += 1
                st['min_b'] = c if st['min_b'] is None else min(st['min_b'], c)
                st['max_b'] = max(st['max_b'], c)
                if len(st['examples']) < 5:
                    st['examples'].append(e['name'])
            name_histos[e['name']] = {
                'num_blocks': h['num_blocks'],
                'num_block_types': h['num_block_types'],
                'type_counts': dict(counts),
                'num_groups': h['num_groups'],
                'user_version': h['user_version'],
                'first_block_group_id': h['first_block_group_id'],
                'blocks_start': h['blocks_start'],
                'header_string': h['header_string'],
            }
            per_file.append(e['name'])
    os.makedirs(LOCAL_OUT + r'\02_WORK', exist_ok=True)
    with open(LOCAL_OUT + r'\02_WORK\pcg953_type_histograms_independent.json',
              'w', encoding='utf-8') as f:
        json.dump(name_histos, f, indent=1)
    # census CSV
    csv_path = os.path.join(REPO_RAW, 'ENTROPIA_NIF_10_1_TYPE_CENSUS.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['type_name', 'blocks', 'files', 'min_blocks_per_file',
                    'max_blocks_per_file', 'baseline_type_present',
                    'example_files', 'scanner_status'])
        for tn in sorted(type_stats, key=lambda k: -type_stats[k]['blocks']):
            st = type_stats[tn]
            w.writerow([tn, st['blocks'], st['files'], st['min_b'],
                        st['max_b'], 'PENDING_BASELINE',
                        ';'.join(st['examples']), 'SCANNED'])
    # append type-scan failures to PHYSICAL_SCAN_FAILURES.csv
    fail_path = os.path.join(REPO_RAW, 'PHYSICAL_SCAN_FAILURES.csv')
    with open(fail_path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['entry_index', 'name', 'reason',
                                          'detail'])
        for r in failures:
            w.writerow(r)
    summary = {
        'scanned_10_1_files': scanned,
        'type_scan_failures': len(failures),
        'denominator_integrity': scanned + len(failures),
        'distinct_type_names': len(type_stats),
        'total_blocks': total_blocks,
        'user_version_dist': dict(user_versions),
        'num_groups_dist': dict(num_groups_dist),
        'first_block_group_id_dist': dict(group_id_first_dist),
        'failures': failures,
    }
    with open(LOCAL_OUT + r'\02_WORK\TYPE_CENSUS_SUMMARY.json', 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({k: v for k, v in summary.items() if k != 'failures'},
                     indent=2))
    print(f'TOP20 types:')
    for tn in sorted(type_stats, key=lambda k: -type_stats[k]['blocks'])[:20]:
        st = type_stats[tn]
        print(f'  {tn:38s} blocks={st["blocks"]:8d} files={st["files"]:5d}')


if __name__ == '__main__':
    main()
