#!/usr/bin/env python3
"""
pe2003_case_pipeline.py — end-to-end case pipeline for PE 2003 models
(JOB PE2003R3-I1, RUN PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024).

PUBLIC PROJECTION NOTICE: this is the sanitized public copy of the campaign
tool. The original run used fixed private paths; here every path is a required
CLI parameter (--config or individual flags). No private corpus path, key or
game payload is embedded in this file. Logic is unchanged relative to the
executed tool (SHA256 of the executed original:
D050627DBFCAE198FFE9AD9A9B14328E126D02C4B2D9D8CF9DA17F872359B38B — this
public copy therefore differs in bytes only in the path-parameterization
plumbing, not in analysis behavior).

Flow per model ID (contract §0E):
  (a) open Models.ark with the qualified F1 decoder (ark_vfs_decoder_f1.py)
  (b) locate member {id}.nif
  (c) extract to --extract-dir
  (d) SHA256 + CRC32 verification against the archive member fields
  (e) explicit-reference scan:
        * member names in all 4 ARK listings (Models/Textures/Scripts/Volumes)
        * U32LE + ASCII of the ID in decoded Scripts blobs (prior
          canonical decode — REUSED, not re-decoded)
        * U32LE + ASCII in raw member payloads of Models.ark, Scripts.ark,
          Volumes.ark (negative-control layer; Textures.ark payload scan is
          SKIPPED_SCOPE — member names only)
  (f) instance/transform candidates: decoded-script U32LE hits are recorded as
      CANDIDATE_EXPLICIT_REFERENCE with status UNVERIFIED — per standing rules
      an explicit resource reference is NOT a world instance/placement claim.
  (g) structure inspection via pe2003_model_inspector.py ->
      --science-root\MODEL_{id}_NIF_STRUCTURE.json + embedded summary
  (h) emit run_{id}_report.json with per-section status
      (CONFIRMED / UNVERIFIED / UNAVAILABLE / NOT_FOUND / SKIPPED_SCOPE).

Usage:
  python pe2003_case_pipeline.py [model_id ...] --config CONFIG.json
  python pe2003_case_pipeline.py 296445 \
      --ark-root <...>\Data --listings-dir <dir> \
      --decoded-scripts-dir <dir> --f1-decoder ark_vfs_decoder_f1.py \
      --inspector pe2003_model_inspector.py \
      --extract-dir <dir> --report-dir <dir> --science-root <dir>

Config JSON keys mirror the long flags below (same names, underscores).
"""
import os, sys, json, csv, struct, hashlib, zlib, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def build_config(args):
    cfg = {
        "ark_root": args.ark_root,
        "listings_dir": args.listings_dir,
        "decoded_scripts_dir": args.decoded_scripts_dir,
        "f1_decoder": args.f1_decoder,
        "inspector": args.inspector,
        "extract_dir": args.extract_dir,
        "report_dir": args.report_dir,
        "science_root": args.science_root,
        "ark_names": {
            "Models.ark": os.path.join("Models", "Models.ark"),
            "Scripts.ark": os.path.join("Scripts", "Scripts.ark"),
            "Textures.ark": os.path.join("Textures", "Textures.ark"),
            "Volumes.ark": os.path.join("Volumes", "Volumes.ark"),
        },
        "listing_files": {
            "Models.ark": "Models_ark_full_listing.csv",
            "Scripts.ark": "Scripts_ark_full_listing.csv",
            "Textures.ark": "Textures_ark_full_listing.csv",
            "Volumes.ark": "Volumes_ark_full_listing.csv",
        },
    }
    missing = [k for k, v in cfg.items() if v is None]
    if missing:
        raise SystemExit("ERROR: missing required path parameters: %s\n%s"
                         % (", ".join(missing), __doc__))
    return cfg


CONFIG = None  # set in main()


def load_f1():
    sys.path.insert(0, os.path.dirname(CONFIG["f1_decoder"]))
    import ark_vfs_decoder_f1 as f1
    return f1


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def read_listing(ark_name):
    p = os.path.join(CONFIG["listings_dir"], CONFIG["listing_files"][ark_name])
    rows = []
    with open(p, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows.append({
                'index': int(row['index']),
                'name': row['member_name'],
                'size': int(row['size_bytes']),
                'crc32_field': row['crc32_field'],
                'data_offset': int(row['data_offset']),
            })
    return rows


def member_name_refs(model_id, listings):
    """Explicit member-name references of the ID across all 4 ARK listings."""
    out = []
    sid = str(model_id)
    for ark_name, rows in listings.items():
        for r in rows:
            base = os.path.basename(r['name'])
            stem = os.path.splitext(base)[0]
            if stem == sid:
                out.append({'container': ark_name, 'member': base,
                            'index': r['index'], 'size': r['size'],
                            'crc32_field': r['crc32_field'],
                            'data_offset': r['data_offset']})
    return out


def scan_payloads(ark_path, listings, model_id, exclude_member=None):
    """U32LE + ASCII scan of raw member payloads for the ID."""
    pat_u32 = struct.pack('<I', model_id)
    pat_a = str(model_id).encode('ascii')
    data = open(ark_path, 'rb').read()
    hits = []
    scanned = 0
    for r in listings:
        if r['name'] == exclude_member:
            continue
        seg = data[r['data_offset']:r['data_offset'] + r['size']]
        scanned += 1
        for pat, kind in ((pat_u32, 'U32LE'), (pat_a, 'ASCII')):
            off = seg.find(pat)
            while off >= 0:
                ctx = seg[max(0, off - 16):off + 20]
                hits.append({'container': os.path.basename(ark_path),
                             'member': r['name'], 'kind': kind,
                             'offset_in_member': off,
                             'context_hex': ctx.hex()})
                off = seg.find(pat, off + 1)
    return hits, scanned


def scan_decoded_scripts(model_id):
    """U32LE + ASCII scan of the decoded Scripts blobs (reused prior dump)."""
    d = CONFIG['decoded_scripts_dir']
    pat_u32 = struct.pack('<I', model_id)
    pat_a = str(model_id).encode('ascii')
    hits, scanned = [], 0
    if not os.path.isdir(d):
        return None, 0, 'UNAVAILABLE'
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            continue
        blob = open(p, 'rb').read()
        scanned += 1
        for pat, kind in ((pat_u32, 'U32LE'), (pat_a, 'ASCII')):
            off = blob.find(pat)
            while off >= 0:
                ctx = blob[max(0, off - 16):off + 20]
                hits.append({'blob': fn, 'kind': kind, 'offset': off,
                             'context_hex': ctx.hex(),
                             'context_ascii': ''.join(chr(c) if 32 <= c < 127 else '.'
                                                     for c in ctx)})
                off = blob.find(pat, off + 1)
    return hits, scanned, 'CONFIRMED' if scanned else 'UNAVAILABLE'


def run_case(model_id, f1, listings):
    rep = {'model_id': model_id, 'job': 'PE2003R3-I1',
           'run': 'PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024',
           'source_identity': 'PE42 Models.ark 2003 corpus (SCIENCE_ROOT R3)'}
    models_path = os.path.join(CONFIG['ark_root'], CONFIG['ark_names']['Models.ark'])
    # (a)+(b) locate
    data = open(models_path, 'rb').read()
    entries, _ = f1.scan_local_chain(data)
    byname = {e['name']: (i, e) for i, e in enumerate(entries)}
    member = '%d.nif' % model_id
    if member not in byname:
        rep['locate'] = {'status': 'NOT_FOUND', 'member': member,
                         'denominator': len(entries)}
        rep['overall'] = 'JOB_NONPASS_NOT_FOUND'
        return rep
    idx, e = byname[member]
    rep['locate'] = {'status': 'CONFIRMED', 'member': member, 'index': idx,
                     'size': e['comp_size'], 'crc32_field': '%08X' % e['crc32'],
                     'data_offset': e['data_offset'],
                     'archive_sha256': sha256_bytes(open(models_path, 'rb').read())}
    # (c) extract
    os.makedirs(CONFIG['extract_dir'], exist_ok=True)
    outp = os.path.join(CONFIG['extract_dir'], member)
    blob = data[e['data_offset']:e['data_offset'] + e['comp_size']]
    open(outp, 'wb').write(blob)
    # (d) hash + crc
    crc_actual = zlib.crc32(blob) & 0xFFFFFFFF
    rep['extract'] = {'status': 'CONFIRMED', 'out_path': outp,
                      'size': len(blob),
                      'sha256': sha256_bytes(blob),
                      'crc32_actual': '%08X' % crc_actual,
                      'crc_ok': crc_actual == e['crc32']}
    # (e) references
    rep['member_name_references'] = {
        'status': 'CONFIRMED',
        'hits': member_name_refs(model_id, listings)}
    # decoded scripts
    hits, scanned, st = scan_decoded_scripts(model_id)
    rep['decoded_scripts_scan'] = {
        'status': st, 'blobs_scanned': scanned, 'hits': hits or []}
    # raw payload scans (negative-control layer)
    raw = {}
    for ark_name in ('Models.ark', 'Scripts.ark', 'Volumes.ark'):
        h, n = scan_payloads(os.path.join(CONFIG['ark_root'], CONFIG['ark_names'][ark_name]),
                             listings[ark_name], model_id,
                             exclude_member=(member if ark_name == 'Models.ark' else None))
        raw[ark_name] = {'members_scanned': n,
                         'hits': [x for x in h if x['kind'] == 'U32LE'][:50],
                         'ascii_hits_total': sum(1 for x in h if x['kind'] == 'ASCII'),
                         'u32le_hits_total': sum(1 for x in h if x['kind'] == 'U32LE'),
                         'status': 'CONFIRMED'}
    rep['raw_payload_scan'] = raw
    rep['textures_payload_scan'] = {'status': 'SKIPPED_SCOPE',
                                    'note': 'Textures.ark payload scan out of F1 scope; member names scanned only'}
    # (f) instance/transform candidates
    cands = []
    for h in (hits or []):
        if h['kind'] == 'U32LE':
            cands.append({'source': 'decoded_scripts:' + h['blob'],
                          'offset': h['offset'],
                          'value_u32': '0x%08X' % model_id,
                          'context_hex': h['context_hex'],
                          'status': 'UNVERIFIED',
                          'note': 'explicit resource-ID reference in a decoded '
                                  'ArkScript constant-pool-like region; NOT a proven '
                                  'world instance, transform or placement record'})
    # BVI sibling co-occurrence (documented in F1 for 296446)
    sib = member_name_refs(model_id + 1, listings)
    if sib:
        for s in sib:
            s['note'] = ('sibling-ID member (id+1) co-occurrence; pairing with the '
                         'model NOT PROVEN (BVI = local collision volume)')
            s['status'] = 'UNVERIFIED'
    rep['instance_transform_candidates'] = {'status': 'UNVERIFIED',
                                            'candidates': cands,
                                            'sibling_members': sib}
    # (g) structure
    structure_json = os.path.join(CONFIG['science_root'],
                                  'MODEL_%d_NIF_STRUCTURE.json' % model_id)
    p = subprocess.run([PY, CONFIG['inspector'], outp, '--json', structure_json],
                       capture_output=True, text=True, timeout=300)
    try:
        struct_summary = json.load(open(structure_json, encoding='utf-8'))
        rep['structure'] = {
            'status': 'CONFIRMED' if struct_summary.get('status') == 'OK' else
                      struct_summary.get('status'),
            'inspector_returncode': p.returncode,
            'structure_json': structure_json,
            'sha256': struct_summary.get('sha256'),
            'blocks': struct_summary.get('blocks_found'),
            'census_match_header': struct_summary.get('census_match_header'),
            'block_census': struct_summary.get('block_census'),
            'parse_warnings': struct_summary.get('parse_warnings'),
            'footer_crosscheck': struct_summary.get('footer', {}).get('roots_crosscheck'),
            'geometry_totals': struct_summary.get('geometry', {}).get('totals'),
            'asset_role': struct_summary.get('asset_role', {}).get('role_statement'),
            'asset_role_status': struct_summary.get('asset_role', {}).get('role_status')}
    except Exception as ex:
        rep['structure'] = {'status': 'UNAVAILABLE', 'error': str(ex),
                            'stderr': p.stderr[:300]}
    # (h) overall
    ok = (rep['locate']['status'] == 'CONFIRMED'
          and rep['extract']['crc_ok']
          and rep['structure'].get('status') == 'CONFIRMED')
    rep['overall'] = 'CONFIRMED' if ok else 'JOB_PARTIAL'
    return rep


def main():
    ap = argparse.ArgumentParser(description="PE2003 model case pipeline (public, path-parameterized)")
    ap.add_argument('ids', nargs='*', type=int, help="model ids, e.g. 296445 218757")
    ap.add_argument('--config', help="JSON config with the path keys (alternative to flags)")
    ap.add_argument('--ark-root', help="root of the extracted install Data\\ directory (contains Models/Scripts/Textures/Volumes)")
    ap.add_argument('--listings-dir', help="directory with the 4 *_ark_full_listing.csv files")
    ap.add_argument('--decoded-scripts-dir', help="directory with decoded Scripts blobs (read-only reuse)")
    ap.add_argument('--f1-decoder', help="path to ark_vfs_decoder_f1.py")
    ap.add_argument('--inspector', help="path to pe2003_model_inspector.py")
    ap.add_argument('--extract-dir', help="extraction output dir")
    ap.add_argument('--report-dir', help="report output dir")
    ap.add_argument('--science-root', help="dir for MODEL_*_NIF_STRUCTURE.json output")
    args = ap.parse_args()

    if args.config:
        j = json.load(open(args.config, encoding='utf-8'))
        for k in ('ark_root', 'listings_dir', 'decoded_scripts_dir', 'f1_decoder',
                  'inspector', 'extract_dir', 'report_dir', 'science_root'):
            if getattr(args, k, None) is None:
                setattr(args, k, j.get(k))
    global CONFIG
    CONFIG = build_config(args)
    f1 = load_f1()
    listings = {ark: read_listing(ark) for ark in CONFIG['listing_files']}
    ids = args.ids or [296445, 218757]
    for mid in ids:
        rep = run_case(mid, f1, listings)
        outp = os.path.join(CONFIG['report_dir'], 'run_%d_report.json' % mid)
        with open(outp, 'w', encoding='utf-8') as f:
            json.dump(rep, f, indent=1)
        print('model %d -> %s | overall=%s blocks=%s' %
              (mid, outp, rep.get('overall'), rep.get('structure', {}).get('blocks')))


if __name__ == '__main__':
    main()
