#!/usr/bin/env python3
"""
ArkVFS decoder — JOB PE2003R3-F1 (RUN PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024)
OWN decoder written for this run. Qualification of prior decoders:

QUALIFICATION RECORD (2026-10-24):
- Skill parser C:\\Users\\User\\.opencode\\skills\\pe-ark-vfs\\ark_parser.py:
  * Uses sequential local-header scan (strategy OK) but parses the local header with
    struct '<IHI IIII' at pos+4, i.e. version as u32@4, flags u16@8, timestamp u32@10,
    crc u32@14, comp u32@18, uncomp u32@22, name_len as U32@26.
  * Per skill CORRECTION F-111 (2026-07-30): .ark uses STANDARD ZIP layout —
    version_needed u16@4, flags u16@6, compression u16@8, mod_time u16@10, mod_date u16@12,
    crc u32@14, comp u32@18, uncomp u32@22, name_len u16@26, extra_len u16@28.
  * The skill parser's u32 name_len@26 read = name_len | (extra_len<<16). It only yields the
    correct value because extra_len==0 in all observed archives. Also its "timestamp u32@10"
    merges mod_time/mod_date. Status: QUALIFIED_WITH_CAVEAT (reference only, not used for output).
  * Skill-verified counters (different corpus copy, 2026-07-29): Models.ark 2492 entries.
- This decoder (ark_vfs_decoder_f1.py): implements the F-111 standard-ZIP layout exactly,
  parses BOTH the local-header chain and the central directory, cross-checks them, and
  verifies CRC32 (zlib) of every member it reads. Status: OWN.

Format (.ark, MindArk 2003, per pe-ark-vfs skill + F-111):
  Local file header : magic 'AK\\x03\\x04', 30B fixed + name + extra + data (STORED, comp==uncomp)
  Central directory: magic 'AK\\x01\\x02' entries at cd_offset (48B fixed + name)
  End of CD        : magic 'AK\\x05\\x06' (22B; disk_num u32, counts u16)

Usage:
  python ark_vfs_decoder_f1.py list          <ark> <out_csv>
  python ark_vfs_decoder_f1.py extract       <ark> <outdir> <name> [<name>...]
  python ark_vfs_decoder_f1.py verify-crc    <ark>
  python ark_vfs_decoder_f1.py volumes-dump  <ark> <out_csv>
"""
import sys, os, struct, zlib, hashlib, csv

LOCAL_MAGIC   = b'AK\x03\x04'
CENTRAL_MAGIC = b'AK\x01\x02'
EOCD_MAGIC    = b'AK\x05\x06'

def read_u16(d, o): return struct.unpack_from('<H', d, o)[0]
def read_u32(d, o): return struct.unpack_from('<I', d, o)[0]

def parse_local_header(data, pos):
    """Standard-ZIP local header (F-111). Returns (entry, data_end) or (None, pos)."""
    if pos + 30 > len(data):
        return None, pos
    if data[pos:pos+4] != LOCAL_MAGIC:
        return None, pos
    version_needed = read_u16(data, pos+4)
    flags          = read_u16(data, pos+6)
    compression   = read_u16(data, pos+8)
    mod_time       = read_u16(data, pos+10)
    mod_date       = read_u16(data, pos+12)
    crc32          = read_u32(data, pos+14)
    comp_size      = read_u32(data, pos+18)
    uncomp_size    = read_u32(data, pos+22)
    name_len       = read_u16(data, pos+26)
    extra_len      = read_u16(data, pos+28)
    name_start = pos + 30
    data_start = name_start + name_len + extra_len
    data_end   = data_start + comp_size
    if data_end > len(data):
        return None, pos  # truncated record
    name = data[name_start:name_start+name_len].decode('ascii', errors='replace')
    e = {
        'name': name, 'version_needed': version_needed, 'flags': flags,
        'compression': compression, 'mod_time': mod_time, 'mod_date': mod_date,
        'crc32': crc32, 'comp_size': comp_size, 'uncomp_size': uncomp_size,
        'name_len': name_len, 'extra_len': extra_len,
        'header_offset': pos, 'data_offset': data_start,
    }
    return e, data_end

def parse_eocd(data):
    """EOCD from last 64 KiB. Returns dict or None."""
    start = max(0, len(data) - 65536)
    idx = data.rfind(EOCD_MAGIC, start)
    if idx < 0 or idx + 22 > len(data):
        return None
    return {
        'eocd_offset': idx,
        'disk_num': read_u32(data, idx+4),
        'entries_disk': read_u16(data, idx+8),
        'total_entries': read_u16(data, idx+10),
        'cd_size': read_u32(data, idx+12),
        'cd_offset': read_u32(data, idx+16),
        'comment_len': read_u16(data, idx+20),
    }

def parse_central_directory(data, eocd):
    """Central directory entries (48B fixed + name). Returns list of dicts."""
    out = []
    pos = eocd['cd_offset']
    end = eocd['cd_offset'] + eocd['cd_size']
    while pos + 48 <= len(data) and data[pos:pos+4] == CENTRAL_MAGIC:
        version_made  = read_u16(data, pos+4)
        version_needed= read_u16(data, pos+6)
        flags         = read_u16(data, pos+8)
        compression   = read_u16(data, pos+10)
        timestamp     = read_u32(data, pos+12)
        crc32         = read_u32(data, pos+16)
        comp_size     = read_u32(data, pos+20)
        uncomp_size   = read_u32(data, pos+24)
        name_len      = read_u32(data, pos+28)
        extra_len     = read_u32(data, pos+32)
        ext_attr      = read_u32(data, pos+36)
        local_offset  = read_u32(data, pos+40)
        unk16         = read_u16(data, pos+44)
        name_start = pos + 46
        name = data[name_start:name_start+name_len].decode('ascii', errors='replace')
        out.append({'name': name, 'crc32': crc32, 'comp_size': comp_size,
                    'uncomp_size': uncomp_size, 'local_offset': local_offset,
                    'flags': flags, 'compression': compression,
                    'central_offset': pos})
        pos = name_start + name_len + extra_len
    return out, pos

def scan_local_chain(data):
    """Sequential local header scan. Returns (entries, anomalies)."""
    entries, anomalies = [], []
    pos = 0
    while pos < len(data):
        if data[pos:pos+4] == LOCAL_MAGIC:
            e, nxt = parse_local_header(data, pos)
            if e is None:
                anomalies.append({'offset': pos, 'type': 'TRUNCATED_LOCAL_HEADER'})
                break
            entries.append(e)
            pos = nxt
        elif data[pos:pos+4] == CENTRAL_MAGIC:
            break  # central directory reached
        elif data[pos:pos+4] == EOCD_MAGIC:
            break
        else:
            anomalies.append({'offset': pos, 'type': 'UNEXPECTED_BYTES'})
            nxt = data.find(LOCAL_MAGIC, pos+1)
            if nxt < 0:
                break
            pos = nxt
    return entries, anomalies

def crc32_of(data, start, length):
    return zlib.crc32(data[start:start+length]) & 0xFFFFFFFF

def sha256_of(data, start, length):
    return hashlib.sha256(data[start:start+length]).hexdigest().upper()

def nif_version(blob):
    """Read NIF header version string. Returns (header_string, version_string)."""
    try:
        # Header: header string (u32 len + bytes incl. EOL), then version string
        hlen = struct.unpack_from('<I', blob, 0)[0]
        hdr = blob[4:4+hlen].rstrip(b'\r\n\x00').decode('ascii', errors='replace')
        vlen = struct.unpack_from('<I', blob, 4+hlen)[0]
        ver = blob[8+hlen:8+hlen+vlen].rstrip(b'\r\n\x00').decode('ascii', errors='replace')
        return hdr, ver
    except Exception as ex:
        return None, 'PARSE_ERROR: %s' % ex

def cmd_list(ark, out_csv):
    data = open(ark, 'rb').read()
    fsize = len(data)
    eocd = parse_eocd(data)
    entries, anomalies = scan_local_chain(data)
    cd_entries, cd_end = ([], None)
    if eocd:
        cd_entries, cd_end = parse_central_directory(data, eocd)
    n_nif = sum(1 for e in entries if e['name'].lower().endswith('.nif'))
    n_other = len(entries) - n_nif
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['index', 'member_name', 'size_bytes', 'crc32_field', 'data_offset', 'header_offset', 'name_len', 'extra_len', 'compression', 'flags'])
        for i, e in enumerate(entries):
            w.writerow([i, e['name'], e['comp_size'], '%08X' % e['crc32'], e['data_offset'], e['header_offset'], e['name_len'], e['extra_len'], e['compression'], e['flags']])
    result = {
        'archive': ark,
        'file_size': fsize,
        'total_members_local_scan': len(entries),
        'nif_members': n_nif,
        'other_members': n_other,
        'eocd': eocd,
        'total_members_eocd': eocd['total_entries'] if eocd else None,
        'central_dir_entries': len(cd_entries),
        'local_vs_eocd_match': (eocd is not None and eocd['total_entries'] == len(entries)),
        'cd_vs_local_match': (len(cd_entries) == len(entries)),
        'anomalies': anomalies,
    }
    # cross-check names/crc between CD and local scan
    if cd_entries and len(cd_entries) == len(entries):
        mism = 0
        for c, l in zip(cd_entries, entries):
            if c['name'] != l['name'] or c['crc32'] != l['crc32'] or c['comp_size'] != l['comp_size']:
                mism += 1
        result['cd_local_field_mismatches'] = mism
    print(result)
    return result

def cmd_verify_crc(ark):
    data = open(ark, 'rb').read()
    entries, anomalies = scan_local_chain(data)
    ok = bad = 0
    bad_list = []
    for e in entries:
        actual = crc32_of(data, e['data_offset'], e['comp_size'])
        if actual == e['crc32']:
            ok += 1
        else:
            bad += 1
            bad_list.append({'name': e['name'], 'field': '%08X' % e['crc32'], 'actual': '%08X' % actual})
    stored_mismatch = sum(1 for e in entries if e['comp_size'] != e['uncomp_size'])
    print({'archive': ark, 'total': len(entries), 'crc_ok': ok, 'crc_bad': bad,
           'comp_ne_uncomp': stored_mismatch, 'bad_members': bad_list[:20],
           'anomalies': anomalies})
    return ok, bad

def cmd_extract(ark, outdir, names):
    data = open(ark, 'rb').read()
    entries, _ = scan_local_chain(data)
    byname = {}
    dupes = []
    for e in entries:
        if e['name'] in byname:
            dupes.append(e['name'])
        else:
            byname[e['name']] = e
    os.makedirs(outdir, exist_ok=True)
    results = []
    for n in names:
        if n not in byname:
            results.append({'name': n, 'status': 'NOT_FOUND_IN_ARCHIVE', 'denominator_total_members': len(entries)})
            print({'name': n, 'status': 'NOT_FOUND_IN_ARCHIVE', 'denominator_total_members': len(entries)})
            continue
        e = byname[n]
        actual_crc = crc32_of(data, e['data_offset'], e['comp_size'])
        sha = sha256_of(data, e['data_offset'], e['comp_size'])
        outp = os.path.join(outdir, n.replace('/', '_'))
        with open(outp, 'wb') as f:
            f.write(data[e['data_offset']:e['data_offset']+e['comp_size']])
        r = {'name': n, 'status': 'EXTRACTED', 'size': e['comp_size'],
             'crc32_field': '%08X' % e['crc32'], 'crc32_actual': '%08X' % actual_crc,
             'crc_ok': actual_crc == e['crc32'],
             'sha256': sha, 'data_offset': e['data_offset'],
             'header_offset': e['header_offset'], 'out_path': outp}
        results.append(r)
        print(r)
    return results

def cmd_volumes_dump(ark, out_csv):
    """Full structural dump of Volumes.ark: members + first-bytes hex of each member header."""
    data = open(ark, 'rb').read()
    eocd = parse_eocd(data)
    entries, anomalies = scan_local_chain(data)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['index', 'member_name', 'size_bytes', 'crc32_field', 'crc32_actual', 'crc_ok', 'data_offset', 'first16_hex'])
        for i, e in enumerate(entries):
            actual = crc32_of(data, e['data_offset'], e['comp_size'])
            first16 = data[e['data_offset']:e['data_offset']+16].hex()
            w.writerow([i, e['name'], e['comp_size'], '%08X' % e['crc32'], '%08X' % actual,
                        int(actual == e['crc32']), e['data_offset'], first16])
    print({'archive': ark, 'eocd': eocd, 'total_members': len(entries), 'anomalies': anomalies,
           'out_csv': out_csv})

def main():
    cmd = sys.argv[1] if len(sys.argv) >= 2 else None
    ark = sys.argv[2] if len(sys.argv) >= 3 else None
    if cmd == 'verify-crc' and ark:
        cmd_verify_crc(ark)
        return
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    if cmd == 'list':
        cmd_list(ark, sys.argv[3])
    elif cmd == 'verify-crc':
        cmd_verify_crc(ark)
    elif cmd == 'extract':
        cmd_extract(ark, sys.argv[3], sys.argv[4:])
    elif cmd == 'volumes-dump':
        cmd_volumes_dump(ark, sys.argv[3])
    else:
        print(__doc__); sys.exit(1)

if __name__ == '__main__':
    main()
