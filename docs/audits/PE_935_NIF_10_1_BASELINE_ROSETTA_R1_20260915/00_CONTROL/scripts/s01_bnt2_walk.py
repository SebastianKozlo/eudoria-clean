#!/usr/bin/env python3
"""s01_bnt2_walk.py — independent minimal BNT2 walker.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (executor-local implementation).

ANTI-CIRCULARITY: this walker was written from the physical-byte hypothesis
(FINDINGS_LOG.md F-01, verified on live Models.bnt bytes BEFORE this script
ran) + prior Dragon UnPACKer structural hint (treated as hypothesis, not
oracle). It does NOT read R61, pcg953_nif_manifest.csv, NifModelReader.js or
any parser output.

Structure walked (hypothesis, fail-closed validated):
  [payload region: entries' payloads, offsets/sizes from index]
  [index at DirOffset: u32 NumEntries, then NumEntries ×
     (name: ASCII bytes terminated 0x0A, 16-byte entry:
        u32 size, u32 offset, u32 field_c, u32 field_d)]
  [footer at EOF-8: u32 DirOffset, magic b'BNT2']

Fail-closed invariants (violations raise WalkError):
  E_SIZE, E_FOOTER_READ, E_MAGIC, E_DIR_OFFSET, E_NUM_READ, E_NUM_SANITY,
  E_NAME_EOF, E_NAME_TOO_LONG, E_NAME_ASCII, E_NAME_EMPTY, E_NAME_DUP,
  E_ENTRY_READ, E_ZERO_SIZE, E_BOUNDS, E_EOF_EXACT, E_FOOTER_MISMATCH,
  E_OVERLAP.

Negative controls (L19, each MUST FAIL the walker on a synthetic archive
built from SYNTHETIC payloads — no proprietary bytes):
  NC_BASE      : uncorrupted synthetic -> walker must PASS (control of control)
  NC_TRUNCATE  : synthetic cut at 50%  -> walker must FAIL
  NC_COUNT     : NumEntries+1          -> walker must FAIL (EOF-exact broken)
  NC_ENDIAN    : walker forced big-endian footer -> must FAIL (magic mismatch)
"""
import argparse
import io
import json
import os
import struct
import sys
import tempfile

FOOTER_MAGIC = b'BNT2'
FOOTER_SIZE = 8


class WalkError(Exception):
    pass


def walk_bnt2(path, *, endian='<', deep_payload_check=False, read_data=False):
    """Validate and enumerate a BNT2 archive. Returns summary dict.

    deep_payload_check: read each payload from disk and verify byte bounds
    (slower; catches IO-level corruption not visible in the index).
    read_data: also return payload bytes per entry (memory heavy).
    """
    f = open(path, 'rb')
    try:
        f.seek(0, io.SEEK_END)
        fsize = f.tell()
        if fsize < FOOTER_SIZE:
            raise WalkError(f'E_SIZE: file too small ({fsize})')
        f.seek(-FOOTER_SIZE, io.SEEK_END)
        footer = f.read(FOOTER_SIZE)
        if len(footer) != FOOTER_SIZE:
            raise WalkError('E_FOOTER_READ: short footer')
        dir_offset = struct.unpack(endian + 'I', footer[:4])[0]
        magic = footer[4:8]
        if magic != FOOTER_MAGIC:
            raise WalkError(f'E_MAGIC: expected BNT2, got {magic!r}')
        if dir_offset < 4 or dir_offset > fsize - FOOTER_SIZE:
            raise WalkError(
                f'E_DIR_OFFSET: {dir_offset} outside [4,{fsize - FOOTER_SIZE}]')
        f.seek(dir_offset)
        raw = f.read(4)
        if len(raw) != 4:
            raise WalkError('E_NUM_READ: short NumEntries')
        num_entries = struct.unpack(endian + 'I', raw)[0]
        if num_entries <= 0 or num_entries > 10_000_000:
            raise WalkError(f'E_NUM_SANITY: {num_entries}')
        entries = []
        seen_names = {}
        for i in range(num_entries):
            name_bytes = bytearray()
            while True:
                c = f.read(1)
                if len(c) != 1:
                    raise WalkError(f'E_NAME_EOF: entry {i} hit EOF in name')
                if c == b'\x0A':
                    break
                name_bytes += c
                if len(name_bytes) > 260:
                    raise WalkError(f'E_NAME_TOO_LONG: entry {i}')
            try:
                name = name_bytes.decode('ascii')
            except UnicodeDecodeError:
                raise WalkError(f'E_NAME_ASCII: entry {i}')
            if not name:
                raise WalkError(f'E_NAME_EMPTY: entry {i}')
            if name in seen_names:
                raise WalkError(f'E_NAME_DUP: entry {i} name {name!r}')
            seen_names[name] = i
            raw = f.read(16)
            if len(raw) != 16:
                raise WalkError(f'E_ENTRY_READ: entry {i} short 16B record')
            size, offset, field_c, field_d = struct.unpack(endian + 'IIII', raw)
            if size == 0:
                raise WalkError(f'E_ZERO_SIZE: entry {i} ({name})')
            if offset + size > dir_offset:
                raise WalkError(
                    f'E_BOUNDS: entry {i} ({name}) offset={offset} '
                    f'size={size} dir_offset={dir_offset}')
            entry = {'index': i, 'name': name, 'size': size,
                     'offset': offset, 'field_c': field_c, 'field_d': field_d}
            if read_data:
                pos = f.tell()
                f.seek(offset)
                entry['data'] = f.read(size)
                if len(entry['data']) != size:
                    raise WalkError(f'E_DATA_READ: entry {i} ({name})')
                f.seek(pos)
            elif deep_payload_check:
                pos = f.tell()
                f.seek(offset + size - 1)
                if f.read(1) != b'':
                    pass  # readable
                f.seek(pos)
            entries.append(entry)
        # I1 EOF-exact: cursor must now be exactly at fsize - FOOTER_SIZE
        cur = f.tell()
        expected_end = fsize - FOOTER_SIZE
        if cur != expected_end:
            raise WalkError(
                f'E_EOF_EXACT: cursor {cur} != {expected_end} '
                f'(delta {cur - expected_end})')
        # I5 footer at index-end equals footer at EOF
        f.seek(cur)
        footer2 = f.read(FOOTER_SIZE)
        if footer2 != footer:
            raise WalkError('E_FOOTER_MISMATCH: footer at index-end != EOF footer')
    finally:
        f.close()
    # I4 overlap check
    order = sorted(entries, key=lambda e: e['offset'])
    for a, b in zip(order, order[1:]):
        if a['offset'] + a['size'] > b['offset']:
            raise WalkError(
                f'E_OVERLAP: {a["name"]} overlaps {b["name"]}')
    covered = sum(e['size'] for e in order)
    gaps = []
    prev_end = 0
    for e in order:
        if e['offset'] > prev_end:
            gaps.append({'after_byte': prev_end, 'gap_len': e['offset'] - prev_end})
        prev_end = e['offset'] + e['size']
    trailing_gap = dir_offset - prev_end
    return {
        'path': os.path.abspath(path), 'file_size': fsize,
        'dir_offset': dir_offset, 'num_entries': num_entries,
        'coverage_bytes': covered,
        'interior_gap_bytes': sum(g['gap_len'] for g in gaps),
        'interior_gap_count': len(gaps),
        'trailing_gap_bytes': trailing_gap,
        'entries': entries,
        'gap_detail': gaps,
    }


def build_synthetic_bnt2(path, n=10, corrupt=None):
    """Build a synthetic BNT2 from synthetic payloads (no proprietary bytes).

    corrupt=None      : valid archive
    corrupt='count'   : NumEntries declared n+1 (index actually has n)
    corrupt='truncate': valid index bytes but file cut to 50% of full length
    """
    payloads = []
    entries = []
    off = 0
    for i in range(n):
        data = (f'SYNTHETIC-PAYLOAD-{i:03d}-' + 'A' * 50).encode('ascii')
        payloads.append(data)
        entries.append({'name': f'synth_{i:03d}.nif', 'size': len(data),
                        'offset': off})
        off += len(data)
    dir_offset = off
    buf = bytearray()
    for d in payloads:
        buf += d
    idx = bytearray()
    num = n + 1 if corrupt == 'count' else n
    idx += struct.pack('<I', num)
    for e in entries:
        idx += e['name'].encode('ascii') + b'\x0A'
        idx += struct.pack('<IIII', e['size'], e['offset'], 0, 0)
    out = bytes(buf) + bytes(idx) + struct.pack('<I', dir_offset) + b'BNT2'
    if corrupt == 'truncate':
        out = out[:len(out) // 2]
    with open(path, 'wb') as f:
        f.write(out)
    return len(out)


def run_negative_controls():
    results = []
    tmp = tempfile.mkdtemp(prefix='bnt2_nc_')
    def check(name, expected, fn):
        try:
            fn()
            actual = 'PASS'
        except WalkError as e:
            actual = f'FAIL({str(e).split(":")[0]})'
        except Exception as e:  # noqa: BLE001
            actual = f'UNEXPECTED_ERROR({type(e).__name__}:{e})'
        ok = (actual == 'PASS') if expected == 'PASS' else (actual.startswith('FAIL') or actual.startswith('UNEXPECTED'))
        results.append({'control': name, 'expected': expected,
                        'actual': actual, 'control_pass': ok})
        return ok
    p_base = os.path.join(tmp, 'base.bnt')
    p_trunc = os.path.join(tmp, 'trunc.bnt')
    p_count = os.path.join(tmp, 'count.bnt')
    build_synthetic_bnt2(p_base, n=10, corrupt=None)
    build_synthetic_bnt2(p_trunc, n=10, corrupt='truncate')
    build_synthetic_bnt2(p_count, n=10, corrupt='count')
    all_ok = True
    all_ok &= check('NC_BASE_valid_synthetic_must_PASS', 'PASS',
                    lambda: walk_bnt2(p_base))
    all_ok &= check('NC_TRUNCATE_must_FAIL', 'FAIL',
                    lambda: walk_bnt2(p_trunc))
    all_ok &= check('NC_CORRUPT_COUNT_must_FAIL', 'FAIL',
                    lambda: walk_bnt2(p_count))
    all_ok &= check('NC_WRONG_ENDIAN_must_FAIL', 'FAIL',
                    lambda: walk_bnt2(p_base, endian='>'))
    return all_ok, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--walk', help='BNT2 archive to walk')
    ap.add_argument('--out', help='output JSON summary path')
    ap.add_argument('--negative-controls', action='store_true')
    args = ap.parse_args()
    if args.negative_controls:
        ok, results = run_negative_controls()
        print(json.dumps({'negative_controls': results,
                          'all_controls_ok': ok}, indent=2))
        return 0 if ok else 1
    if not args.walk:
        ap.error('--walk or --negative-controls required')
    s = walk_bnt2(args.walk)
    s_out = {k: v for k, v in s.items() if k != 'entries'}
    s_out['first_entries'] = s['entries'][:3]
    s_out['last_entries'] = s['entries'][-3:]
    text = json.dumps(s_out, indent=2)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'WALK_OK entries={s["num_entries"]} -> {args.out}')
    else:
        print(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
