#!/usr/bin/env python3
# s16_field_identity_mechanism_repro.py -- executed negative control
# for PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (contracts
# C2/C4 + addendum E quality discipline).
#
# Executes BOTH field-identity models on the same physical bytes
# (BABYLENGUIN.NIF block 6, the duplicate-name case that WOULD be
# collapsed by the old model and is NOT by v2):
#   OLD  = frozen s06 SchemaDecoder._fields_for (bare-name dedup)
#   V2   = s14 SchemaDecoderV2._fields_for (occurrence-preserving)
#
# Expected (derived independently in C1 by s15 walker, engine truth):
#   OLD: block 6 boundary lands at 1498; the u32 read there as
#        "block 7 GroupID" = 479309 (filename tail 'MP' + low bytes of
#        the pixel-data link 7) -- FALSE positive reproduced.
#   V2:  block 6 consumes the File Name[Use External == 0] branch and
#        ends at 1517; block 7 GroupID = 0 at offset 1517.
#
# Output: 01_RAW/FIELD_IDENTITY_V2_NEGATIVE_CONTROL.csv
import csv
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, Cursor, ArkBlockError)
from s14_world_slice_validator_fieldidentity_v2 import (  # noqa: E402
    WorldSliceValidatorV2)
from s04_nifxml_baseline import Unresolved  # noqa: E402

PATH = r"D:\gamebyroengine\extracted\gb112_known_good\BABYLENGUIN.NIF"
REPO_RAW = os.path.join(os.path.dirname(HERE), "..", "01_RAW")


def sequential_until_block7(validator_cls, data):
    """s08-style sequential decode; returns dict:
    {per-block boundaries, error_at, error_msg, block7_gid_offset,
     block7_gid}."""
    v = validator_cls()
    cur = Cursor(data)
    hdr = v.parse_header(cur)
    blocks = []
    err = None
    b7_off = None
    b7_gid = None
    i = 0
    for i in range(hdr['num_blocks']):
        tname = hdr['types'][hdr['idx'][i]]
        start = cur.pos
        gid = cur.u32()
        if i == 7:
            b7_off = start
            b7_gid = gid
            break  # only block 7's GroupID offset/value is needed
        if gid != 0:
            err = ('block %d GroupID=%d at offset %d'
                   % (i, gid, start))
            break
        if tname not in v.dec.s.objects:
            err = 'unsupported type %s (block %d)' % (tname, i)
            break
        blk = v.dec.decode_block(cur, tname)
        blk['__type__'] = tname
        blk['__start__'] = start
        blk['__end__'] = cur.pos
        blocks.append(blk)
        if i >= 7:
            break
    else:
        i = hdr['num_blocks']
    return {'blocks': blocks, 'error': err,
            'block7_gid_offset': b7_off, 'block7_gid': b7_gid,
            'last_block_index': len(blocks) - 1,
            'last_block_end': blocks[-1]['__end__'] if blocks else None,
            'last_block_type': blocks[-1]['__type__'] if blocks else None}


def fields_for_nisourcetexture(validator_cls):
    v = validator_cls()
    return v.dec._fields_for('NiSourceTexture')


def main():
    data = open(PATH, 'rb').read()
    rows = []

    old = sequential_until_block7(WorldSliceValidator, data)
    v2 = sequential_until_block7(WorldSliceValidatorV2, data)

    b6_old = [b for b in old['blocks'] if b['__type__'] ==
              'NiSourceTexture']
    b6_v2 = [b for b in v2['blocks'] if b['__type__'] ==
             'NiSourceTexture']
    old_b6 = b6_old[0] if b6_old else None
    v2_b6 = b6_v2[0] if b6_v2 else None

    rows.append({
        'probe': 'OLD_MODEL', 'aspect': 'block6_end_offset',
        'value': str(old_b6['__end__'] if old_b6 else 'N/A'),
        'expected': '1498 (mis-derived: File Name[UE==0] lost)',
        'status': ('REPRODUCED' if old_b6 and old_b6['__end__'] == 1498
                   else 'MISMATCH')})
    rows.append({
        'probe': 'OLD_MODEL', 'aspect': 'block7_gid_offset_and_value',
        'value': '%s@%s' % (old['block7_gid'], old['block7_gid_offset']),
        'expected': '479309@1498 (false read of filename+link bytes)',
        'status': ('REPRODUCED' if old['block7_gid'] == 479309 and
                   old['block7_gid_offset'] == 1498 else 'MISMATCH')})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'block6_end_offset',
        'value': str(v2_b6['__end__'] if v2_b6 else 'N/A'),
        'expected': '1517 (File Name[UE==0] consumed; engine truth)',
        'status': ('PASS' if v2_b6 and v2_b6['__end__'] == 1517
                   else 'MISMATCH')})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'block7_gid_offset_and_value',
        'value': '%s@%s' % (v2['block7_gid'], v2['block7_gid_offset']),
        'expected': '0@1517 (true NiPixelData GroupID)',
        'status': ('PASS' if v2['block7_gid'] == 0 and
                   v2['block7_gid_offset'] == 1517 else 'MISMATCH')})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'block6_file_name_value',
        'value': repr(v2_b6.get('File Name')) if v2_b6 else 'N/A',
        'expected': "'LEN-SKIN_02.BMP'",
        'status': 'PASS' if v2_b6 and v2_b6.get('File Name') ==
        'LEN-SKIN_02.BMP' else 'MISMATCH'})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'block6_use_external',
        'value': str(v2_b6.get('Use External')) if v2_b6 else 'N/A',
        'expected': '0 (internal pixel data)',
        'status': 'PASS' if v2_b6 and v2_b6.get('Use External') == 0
                  else 'MISMATCH'})

    # field lists: old vs v2 for NiSourceTexture
    old_fields = fields_for_nisourcetexture(WorldSliceValidator)
    v2_fields = fields_for_nisourcetexture(WorldSliceValidatorV2)
    old_names = [(o, f['name'], f.get('cond')) for o, f in old_fields]
    v2_names = [(o, f['name'], f.get('cond')) for o, f in v2_fields]
    rows.append({
        'probe': 'OLD_MODEL', 'aspect': 'nisourcetexture_file_name_occurrences',
        'value': str(sum(1 for _, n, _ in old_names if n == 'File Name')),
        'expected': '1 (collapsed; UE==0 alternative lost)',
        'status': 'REPRODUCED' if sum(1 for _, n, _ in old_names
                                      if n == 'File Name') == 1
                  else 'MISMATCH'})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'nisourcetexture_file_name_occurrences',
        'value': str(sum(1 for _, n, _ in v2_names if n == 'File Name')),
        'expected': '2 (both conditional alternatives preserved)',
        'status': 'PASS' if sum(1 for _, n, _ in v2_names
                                if n == 'File Name') == 2 else 'MISMATCH'})
    rows.append({
        'probe': 'V2_MODEL', 'aspect': 'v2_field_list_dump',
        'value': '; '.join('%s.%s[cond=%s]' % (o, n, c) for
                           o, n, c in v2_names),
        'expected': 'both File Name occurrences present in schema order',
        'status': 'INFO'})

    out = os.path.join(REPO_RAW, 'FIELD_IDENTITY_V2_NEGATIVE_CONTROL.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['probe', 'aspect', 'value',
                                         'expected', 'status'])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    for r in rows:
        print('%s %s = %r [%s]' % (r['probe'], r['aspect'], r['value'],
                                   r['status']))
    fails = [r for r in rows if r['status'] == 'MISMATCH']
    print('csv %s rows=%d mismatches=%d' % (out, len(rows), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
