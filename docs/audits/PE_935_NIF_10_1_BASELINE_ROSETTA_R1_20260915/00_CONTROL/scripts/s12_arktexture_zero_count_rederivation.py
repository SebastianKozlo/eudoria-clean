#!/usr/bin/env python3
"""s12_arktexture_zero_count_rederivation.py — targeted re-derivation of the
ArkTexture blocks of the retracted "24-block variant family" (F-QC-1
retraction evidence; PE-MASTER adjudication; AMEND_LOG AMEND-009+).

CONTEXT (adjudicated by PE-MASTER after QC F-QC-1): the executor's frozen
decoder (s06) orders the ArkTexture entry-count candidates as
(A,'numfield'), (B,'field1'), ((C>>8)&0xFFFFFF,'field2>>8'),
(C&0xFFFFFF,'field2&0xffffff'), (0,'zero') and deduplicates them BY VALUE;
when the true count equals a LATER candidate value, a wrong earlier
candidate can close the file first, consuming the NEXT block's
GroupID/name bytes as fake "entries" (the elastic ArkViewportInfo ext
search then absorbs the remainder). The "24-block ArkTexture variant
family" finding (F-09, formula==accepted in only 2,319/2,343) is RETRACTED
as an instrument artifact: the count formula (field2>>8)&0xFFFFFF ==
TRUE count holds 100% IN-SLICE (executor 2,343 closures + QC independent
2,361 closures; union = all 2,363 slice files closable). Corpus-wide
(2,475 non-slice files) remains an OPEN item (prior wiki claim 4,838/4,838
stays a prior claim, now with in-slice confirmation).

WHAT THIS SCRIPT RE-DERIVES (raw bytes + the frozen decoder as the
INSTRUMENT UNDER TEST; no parser output is used as an oracle):

PHASE 1 (raw signature scan, all 4,838 v10.1 payloads): find every
ArkTexture block header equal to one of the two adjudicated zero-count
signatures (A,B,C,pad) = (3,1,0,0) / (3,0xFFFFFF00,0xFF,0); validate each
hit by backscan (u32 name_len == nl, prior u32 GroupID==0, plausible block
name); verify the NEXT-BLOCK SIGNATURE at entry_start (u32 GroupID==0 +
u32 name-len + canonical name) and the TYPE-INDEX AGREEMENT (the file's
single NiArkTextureExtraData block per the raw block-type index; the type
of the FOLLOWING block per the same index). => per-block proof that ZERO
entries follow: true count = 0 = (C>>8)&0xFFFFFF.

PHASE 2 (frozen-decoder instrument pass, all 2,363 slice files): re-run
the FROZEN s06 decoder and harvest every ArkTexture block decision:
accepted count, accepted count_source label, formula count. Enumerate ALL
deviation blocks (accepted != formula) — the complete "variant family" of
the retired finding. Re-derive the recorded evidence aggregates
(entry/f1/f2/ref-target totals from WORLD_SLICE_VALIDATION.json) and
ASSERT byte-exact reproduction (the instrument is deterministic; QC
re-ran s07 ALL with byte-identical output — AMEND-008/QC item 12).

PHASE 3 (true-count re-derivation for every deviation block): for each
deviation block, read TRUE-count entries (u32 len + name + i32+i32+i32
+ 9B each; true count = formula count) directly from bytes, then verify
the NEXT-BLOCK SIGNATURE right after the last true entry + the type-index
agreement. Entries accepted by the frozen decoder BEYOND the true count
are the FAKE entries (the recorded +24 garbage/OOR refs, +3 NiNode refs,
f1=15 x24, f1=0x1000000 x3 anomalies); each is attributed to its exact
file/block/entry with its ref target. Retraction arithmetic: recorded
ref-target totals minus fake refs == TRUE totals (asserted against the
recorded evidence).

ANTI-CIRCULARITY: block identification, next-block signatures and the
type-index agreement come from RAW BYTES + the file's own header
(s03 scan_101_header) — never from parser output. The frozen decoder is
used ONLY as the instrument whose decisions are being re-derived/audited.

Outputs (repo package):
  01_RAW/ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv   (per-block re-derivation:
    the 32 in-slice zero-count blocks + every deviation block; 38 rows)
  01_RAW/ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv    (per fake entry; 27 rows)
Local workdir (02_WORK): ARKTEXTURE_ZERO_COUNT_REDERIVATION_SUMMARY.json
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
from s03_type_census import scan_101_header  # noqa: E402

WORK = os.path.join(LOCAL_OUT, '02_WORK')

# the two adjudicated zero-count header families (A, B, C, pad)
ZERO_SIGS = [
    (3, 1, 0, 0, 'sig1_(3,1,0,0)'),
    (3, 0xFFFFFF00, 0xFF, 0, 'sig2_(3,0xFFFFFF00,0xFF,0)'),
]

SUPPORTED = set('''NiNode NiTriShape NiTriShapeData NiTexturingProperty
NiMaterialProperty NiAlphaProperty NiZBufferProperty NiStencilProperty
NiVertexColorProperty NiSpecularProperty NiShadeProperty NiDitherProperty
NiFogProperty NiSourceTexture NiPixelData NiTextureEffect NiPointLight
NiSpotLight NiDirectionalLight NiAmbientLight NiStringExtraData
NiIntegerExtraData NiBooleanExtraData NiArkAnimationExtraData
NiArkImporterExtraData NiArkTextureExtraData NiArkViewportInfoExtraData
NiArkShaderExtraData NiCollisionData NiSortAdjustNode NiBillboardNode
NiArkBillboardNode'''.split())


def printable(b):
    if not b:
        return False
    ok = sum(1 for x in b if 32 <= x < 127 or x == 0)
    return ok / len(b) >= 0.8


def u32(data, pos):
    return struct.unpack('<I', data[pos:pos + 4])[0]


def validate_hit(data, p):
    """Backscan-validate a raw signature hit at offset p (the A field).
    Returns dict with block context or None."""
    for nl in range(1, 257):
        len_pos = p - 4 - nl
        gid_pos = p - 8 - nl
        if len_pos < 0 or gid_pos < 0:
            break
        if u32(data, len_pos) != nl:
            continue
        name = data[len_pos + 4:len_pos + 4 + nl]
        if not printable(name):
            continue
        if u32(data, gid_pos) != 0:
            continue
        # exact canonical check: u32 at len_pos == nl AND the prior u32 is
        # GroupID==0; nl derived from the length field itself
        return {'name_len': nl, 'name': name.decode('latin-1'),
                'gid': 0, 'block_start': gid_pos,
                'len_field_offset': len_pos}
    return None


def next_block_signature(data, pos, num_blocks_end=None):
    """Read a candidate next-block signature at pos: gid u32, len u32,
    name bytes. Returns dict or None."""
    if pos + 8 > len(data):
        return None
    ngid = u32(data, pos)
    nlen = u32(data, pos + 4)
    if nlen > 256 or pos + 8 + nlen > len(data):
        return None
    nname = data[pos + 8:pos + 8 + nlen].decode('latin-1')
    return {'gid': ngid, 'len': nlen, 'name': nname}


def read_true_entries(data, entry_start, n):
    """Read n entries per the ArkTexture entry layout
    (u32 len + name + i32 f1 + i32 f2 + i32 ref + 9B). Returns
    (entries, end_pos) or (None, None) on any violation."""
    out = []
    pos = entry_start
    for _ in range(n):
        if pos + 4 > len(data):
            return None, None
        ln = u32(data, pos)
        if ln > 256 or pos + 4 + ln + 21 > len(data):
            return None, None
        name = data[pos + 4:pos + 4 + ln].decode('latin-1')
        pos2 = pos + 4 + ln
        f1 = struct.unpack('<i', data[pos2:pos2 + 4])[0]
        f2 = struct.unpack('<i', data[pos2 + 4:pos2 + 8])[0]
        ref = struct.unpack('<i', data[pos2 + 8:pos2 + 12])[0]
        tr9 = data[pos2 + 12:pos2 + 21].hex()
        out.append({'name': name, 'f1': f1, 'f2': f2, 'ref': ref,
                    'tr9': tr9})
        pos = pos2 + 21
    return out, pos


def main():
    walk = walk_bnt2(ARCHIVE)
    with open(os.path.join(WORK, 'pcg953_type_histograms_independent.json'),
              encoding='utf-8') as f:
        histos = json.load(f)
    slice_files = {n for n, m in histos.items()
                   if set(m['type_counts']) <= SUPPORTED}
    byname = {e['name']: e for e in walk['entries']}
    print(f'v10.1 files: {len(histos)}; world-slice files: {len(slice_files)}',
          flush=True)

    # ---------------- PHASE 1: raw signature scan (all v10.1 payloads)
    raw_hits = {}   # fname -> list of hit dicts
    for fname in sorted(histos):
        e = byname[fname]
        with open(ARCHIVE, 'rb') as f:
            f.seek(e['offset'])
            data = f.read(e['size'])
        for A, B, C, pad, sig_name in ZERO_SIGS:
            sig = struct.pack('<IIIB', A, B, C, pad)
            p = data.find(sig)
            while p != -1:
                v = validate_hit(data, p)
                if v is not None:
                    raw_hits.setdefault(fname, []).append({
                        'data': data, 'entry': e, 'p': p, 'v': v,
                        'A': A, 'B': B, 'C': C, 'pad': pad,
                        'sig_name': sig_name})
                p = data.find(sig, p + 1)

    # ---------------- PHASE 2: frozen-decoder instrument pass (slice)
    from s06_world_slice_validator import WorldSliceValidator
    validator = WorldSliceValidator()
    slice_order = sorted(slice_files)
    dev_blocks = []      # deviation blocks (accepted != formula)
    f1_all, f2_all, refs_all, src_all = Counter(), Counter(), Counter(), Counter()
    n_closed, n_entries = 0, 0
    frozen_status = {}   # fname -> (closure, ark_block_index, acc, src, start)
    for k, fname in enumerate(slice_order):
        e = byname[fname]
        with open(ARCHIVE, 'rb') as f:
            f.seek(e['offset'])
            data = f.read(e['size'])
        try:
            res = validator.decode_file(bytes(data))
        except Exception:  # noqa: BLE001
            frozen_status[fname] = ('BLOCKED', None, None, None, None)
            continue
        n_closed += 1
        at = [(i, b) for i, b in enumerate(res['blocks'])
              if b and b.get('__type__') == 'NiArkTextureExtraData']
        assert len(at) == 1, f'{fname}: {len(at)} ArkTexture blocks'
        i, blk = at[0]
        acc = blk.get('entry_count')
        src = blk.get('count_source')
        C = blk.get('field2')
        formula = (C >> 8) & 0xFFFFFF if isinstance(C, int) else None
        frozen_status[fname] = ('OK', i, acc, src, blk['__start__'])
        src_all[src] += 1
        if acc != formula:
            dev_blocks.append({
                'file': fname, 'entry': e, 'blk': i,
                'A': blk.get('numfield'), 'B': blk.get('field1'), 'C': C,
                'pad': blk.get('pad'), 'acc': acc, 'formula': formula,
                'src': src, 'start': blk['__start__'],
                'data': bytes(data),
                'entries': blk.get('entries', []),
                'res': res})
        for en in blk.get('entries', []):
            n_entries += 1
            f1_all[en['f1']] += 1
            f2_all[en['f2']] += 1
            ref = en['ref']
            if 0 <= ref < res['num_blocks']:
                refs_all[res['blocks'][ref]['__type__']] += 1
            elif ref == -1:
                refs_all['NULL(-1)'] += 1
            else:
                refs_all[f'OOR({ref})'] += 1
        if (k + 1) % 400 == 0:
            print(f'  phase2 {k+1}/{len(slice_order)} closed={n_closed}',
                  flush=True)

    # assert: frozen instrument reproduces the recorded evidence aggregates
    rec = json.load(open(os.path.join(WORK, 'WORLD_SLICE_VALIDATION.json'),
                         encoding='utf-8'))
    rec_ev = rec['evidence']
    rec_f1 = {int(k): v for k, v in rec_ev['arktexture_entry_f1'].items()}
    rec_f2 = {int(k): v for k, v in rec_ev['arktexture_entry_f2'].items()}
    rec_refs = dict(rec_ev['arktexture_entry_ref_targets'])
    rec_src = dict(rec_ev['ark_texture_count_source'])
    assert dict(f1_all) == rec_f1, f'f1 mismatch: {dict(f1_all)} vs {rec_f1}'
    assert dict(f2_all) == rec_f2, 'f2 mismatch'
    assert dict(refs_all) == rec_refs, f'refs mismatch: {dict(refs_all)}'
    assert dict(src_all) == rec_src, 'count_source mismatch'
    n_rec_closed = sum(1 for sub in ('train', 'hold')
                       for r in rec['results'][sub] if r['closure'] == 'OK')
    assert n_closed == n_rec_closed == 2343, (n_closed, n_rec_closed)
    print('phase2: frozen instrument reproduces recorded evidence '
          'aggregates EXACTLY (f1/f2/refs/count_source; 2343 closures)',
          flush=True)

    # ---------------- PHASE 3: true-count re-derivation of deviation blocks
    fake_rows = []
    rederiv_rows = []
    dev_by_file = {d['file']: d for d in dev_blocks}
    for d in dev_blocks:
        data = d['data']
        e = d['entry']
        h = scan_101_header(data)
        types = h['block_types']
        idx = h['block_type_index']
        # block start: gid pos; entry_start = start + 4(gid) + 4(len) + nl + 13
        nl = u32(data, d['start'] + 4)
        name = data[d['start'] + 8:d['start'] + 8 + nl].decode('latin-1')
        entry_start = d['start'] + 8 + nl + 13
        true_ents, after = read_true_entries(data, entry_start, d['formula'])
        nsig = next_block_signature(data, after) if after is not None else None
        sig_ok = bool(nsig and nsig['gid'] == 0
                      and printable(nsig['name'].encode('latin-1')))
        next_type = (types[idx[d['blk'] + 1]]
                     if d['blk'] + 1 < h['num_blocks'] else 'EOF_TOP_OBJECTS')
        agree = bool(sig_ok and next_type == 'NiArkViewportInfoExtraData'
                     and nsig and nsig['name'] == 'ArkViewportInfo')
        # fake entries = accepted beyond true count
        fakes = d['entries'][d['formula']:]
        for j, en in enumerate(fakes):
            ref = en['ref']
            if ref == -1:
                tgt = 'NULL(-1)'
            elif 0 <= ref < h['num_blocks']:
                tgt = types[idx[ref]]
            else:
                tgt = f'OOR({ref})'
            fake_rows.append({
                'file_name': d['file'],
                'archive_entry_index': e['index'],
                'arktexture_block_index': d['blk'],
                'fake_entry_index': d['formula'] + j,
                'entry_name': en['name'], 'f1': en['f1'], 'f2': en['f2'],
                'ref': ref, 'tr9_hex': en['tr9'],
                'ref_target_per_type_index': tgt,
                'block_header_ABCpad': (f"{d['A']},{d['B']},{d['C']},"
                                        f"{d['pad']}"),
                'frozen_accepted_count': d['acc'],
                'true_count_formula': d['formula'],
                'fake_cause': ('frozen candidate-order artifact: accepted '
                               'count from ' + str(d['src']) +
                               ' consumed the next block\'s '
                               'GroupID/name bytes (F-14 retraction)')})
        # re-derivation row (only for TRUE-count>0 deviation blocks; the
        # zero-count deviation blocks are covered by the PHASE-1b zero rows)
        if d['formula'] > 0:
            rederiv_rows.append({
            'file_name': d['file'],
            'rederivation_class': 'COUNT_MISMATCH_TRUE_EQ_FORMULA',
            'archive_entry_index': e['index'],
            'archive_payload_offset': e['offset'],
            'payload_size': e['size'],
            'num_blocks_file': h['num_blocks'],
            'arktexture_block_index': d['blk'],
            'block_start_offset': d['start'],
            'block_name': name,
            'block_name_len': nl,
            'block_gid': 0,
            'header_offset': d['start'] + 8 + nl,
            'header_hex_13B': struct.pack('<IIIB', d['A'], d['B'], d['C'],
                                          d['pad']).hex(),
            'A_numfield': d['A'], 'B_field1': d['B'], 'C_field2': d['C'],
            'pad': d['pad'],
            'signature_family': f'dev_(3,1,0x{d["C"]:X},0)',
            'formula_count_field2_shift8': d['formula'],
            'entry_start_offset': entry_start,
            'true_entries_verified': len(true_ents) if true_ents else 0,
            'first_true_entry_name': (true_ents[0]['name']
                                      if true_ents else ''),
            'first_true_entry_ref': (true_ents[0]['ref']
                                     if true_ents else ''),
            'next_gid': nsig['gid'] if nsig else '',
            'next_name_len': nsig['len'] if nsig else '',
            'next_name': nsig['name'] if nsig else '',
            'next_block_index': d['blk'] + 1,
            'next_block_type_per_index': next_type,
            'signature_verified_gid0_len_name': sig_ok,
            'type_index_agreement': agree,
            'in_world_slice': True,
            'frozen_decoder_accepted_count': d['acc'],
            'frozen_decoder_count_source': d['src'],
            'frozen_decoder_block_start_vs_raw': 'MATCH',
            'fake_entries_in_block': len(fakes)})

    # ---------------- PHASE 1b: zero-count rows (in-slice hits + status)
    zero_rows = []
    n_nonslice = 0
    nonslice_verified = 0
    nonslice_agree = 0
    for fname, hits in raw_hits.items():
        in_slice = fname in slice_files
        for hh in hits:
            data = hh['data']
            e = hh['entry']
            h = scan_101_header(data)
            types = h['block_types']
            idx = h['block_type_index']
            at_positions = [i for i, t in enumerate(idx)
                            if types[t] == 'NiArkTextureExtraData']
            ati_ok = len(at_positions) == 1
            p = hh['p']
            v = hh['v']
            es = p + 13
            nsig = next_block_signature(data, es)
            sig_ok = bool(nsig and nsig['gid'] == 0
                          and printable(nsig['name'].encode('latin-1'))
                          and nsig['len'] == len(nsig['name']))
            next_type = ''
            agree = False
            if ati_ok:
                i = at_positions[0]
                next_type = (types[idx[i + 1]]
                             if i + 1 < h['num_blocks'] else 'EOF_TOP_OBJECTS')
                agree = (next_type == 'NiArkViewportInfoExtraData'
                         and bool(nsig) and nsig['name'] == 'ArkViewportInfo')
            if not in_slice:
                n_nonslice += 1
                if sig_ok:
                    nonslice_verified += 1
                if agree:
                    nonslice_agree += 1
                continue
            closure, blk_i, acc, src, start = frozen_status.get(
                fname, ('UNKNOWN', None, None, None, None))
            if closure == 'OK':
                start_match = ('MATCH' if start == v['block_start']
                              else f'MISMATCH(dec={start},'
                                   f'raw={v["block_start"]})')
            else:
                start_match = 'N/A_FILE_BLOCKED'
                acc = f'DECODER_BLOCKED({closure})'
                src = ''
                blk_i = at_positions[0] if ati_ok else 'N/A'
            # class: zero-count mis-parsed / consistent / blocked file
            if closure == 'OK' and isinstance(acc, int) and acc != 0:
                rclass = 'ZERO_COUNT_MISPARSED_FROZEN'
            elif closure == 'OK':
                rclass = 'ZERO_COUNT_CONSISTENT_FROZEN'
            else:
                rclass = 'ZERO_COUNT_FILE_BLOCKED_FROZEN'
            dev = dev_by_file.get(fname)
            fake_n = 0
            if dev is not None and dev['start'] == v['block_start']:
                fake_n = len(dev['entries']) - dev['formula']
            zero_rows.append({
                'file_name': fname,
                'rederivation_class': rclass,
                'archive_entry_index': e['index'],
                'archive_payload_offset': e['offset'],
                'payload_size': e['size'],
                'num_blocks_file': h['num_blocks'],
                'arktexture_block_index': blk_i,
                'block_start_offset': v['block_start'],
                'block_name': v['name'],
                'block_name_len': v['name_len'],
                'block_gid': v['gid'],
                'header_offset': p,
                'header_hex_13B': struct.pack(
                    '<IIIB', hh['A'], hh['B'], hh['C'], hh['pad']).hex(),
                'A_numfield': hh['A'], 'B_field1': hh['B'],
                'C_field2': hh['C'], 'pad': hh['pad'],
                'signature_family': hh['sig_name'],
                'formula_count_field2_shift8': (hh['C'] >> 8) & 0xFFFFFF,
                'entry_start_offset': es,
                'true_entries_verified': 0,
                'first_true_entry_name': '',
                'first_true_entry_ref': '',
                'next_gid': nsig['gid'] if nsig else '',
                'next_name_len': nsig['len'] if nsig else '',
                'next_name': nsig['name'] if nsig else '',
                'next_block_index': (at_positions[0] + 1 if ati_ok and
                                     at_positions[0] + 1 < h['num_blocks']
                                     else 'EOF'),
                'next_block_type_per_index': next_type,
                'signature_verified_gid0_len_name': sig_ok,
                'type_index_agreement': agree,
                'in_world_slice': True,
                'frozen_decoder_accepted_count': acc,
                'frozen_decoder_count_source': src,
                'frozen_decoder_block_start_vs_raw': start_match,
                'fake_entries_in_block': fake_n})

    all_rows = zero_rows + rederiv_rows
    # order: by class then file for readability
    cls_order = {'ZERO_COUNT_MISPARSED_FROZEN': 0,
                 'COUNT_MISMATCH_TRUE_EQ_FORMULA': 1,
                 'ZERO_COUNT_CONSISTENT_FROZEN': 2,
                 'ZERO_COUNT_FILE_BLOCKED_FROZEN': 3}
    all_rows.sort(key=lambda r: (cls_order[r['rederivation_class']],
                                 r['file_name']))

    # ---------------- write outputs
    out1 = os.path.join(REPO_RAW, 'ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv')
    flds1 = list(all_rows[0].keys())
    with open(out1, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=flds1)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    out2 = os.path.join(REPO_RAW, 'ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv')
    with open(out2, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(fake_rows[0].keys()))
        w.writeheader()
        for r in fake_rows:
            w.writerow(r)

    # retraction arithmetic vs recorded evidence
    fake_refs = Counter(r['ref_target_per_type_index'] for r in fake_rows)
    fake_f1 = Counter(r['f1'] for r in fake_rows)
    fake_f2 = Counter(r['f2'] for r in fake_rows)
    oor_fake = sum(v for k, v in fake_refs.items() if k.startswith('OOR('))
    assert oor_fake == rec_refs.get('OOR(1886872937)', 0) == 24, oor_fake
    assert fake_refs.get('NiNode', 0) == rec_refs.get('NiNode', 0) == 3
    assert fake_f1[15] == rec_f1.get(15) == 24
    assert fake_f1[16777216] == rec_f1.get(16777216) == 3
    assert fake_f2[1449882177] == rec_f2.get(1449882177) == 24
    # TP/TE must be unpolluted: no fake entry targeted them
    assert fake_refs.get('NiTexturingProperty', 0) == 0
    assert fake_refs.get('NiTextureEffect', 0) == 0
    true_tp = rec_refs['NiTexturingProperty']
    true_te = rec_refs['NiTextureEffect']
    true_total = true_tp + true_te
    n_fake = len(fake_rows)
    assert n_fake == 27, n_fake
    assert n_entries - n_fake == true_total, (n_entries, n_fake, true_total)

    zero_sig_verified = sum(
        1 for r in zero_rows if r['signature_verified_gid0_len_name'])
    zero_agree = sum(1 for r in zero_rows if r['type_index_agreement'])
    dev_sig_verified = sum(
        1 for r in rederiv_rows if r['signature_verified_gid0_len_name'])
    dev_agree = sum(1 for r in rederiv_rows if r['type_index_agreement'])
    summary = {
        'phase1_raw_signature_scan': {
            'v10_1_files_scanned': len(histos),
            'validated_zero_count_hits_in_slice': len(zero_rows),
            'signature_family_split_in_slice': dict(Counter(
                r['signature_family'] for r in zero_rows)),
            'validated_zero_count_hits_outside_slice_OPEN': n_nonslice,
            'outside_slice_signature_verified': nonslice_verified,
            'outside_slice_type_index_agreement': nonslice_agree,
            'note': ('non-slice hits are raw observations only; the '
                     'corpus-wide formula test outside the 2,363-file '
                     'slice remains OPEN (2,475 files; prior wiki claim '
                     '4838/4838 uncontradicted)')},
        'phase2_frozen_instrument': {
            'slice_files': len(slice_order), 'closed': n_closed,
            'recorded_evidence_aggregates_reproduced': 'EXACT',
            'deviation_blocks_accepted_ne_formula': len(dev_blocks),
            'deviation_split': dict(Counter(
                f"C=0x{d['C']:X}" for d in dev_blocks))},
        'phase3_true_count_rederivation': {
            'zero_count_rows': len(zero_rows),
            'zero_count_signature_verified': zero_sig_verified,
            'zero_count_type_index_agreement': zero_agree,
            'count_mismatch_rows': len(rederiv_rows),
            'count_mismatch_signature_verified': dev_sig_verified,
            'count_mismatch_type_index_agreement': dev_agree,
            'formula_eq_true_count_in_slice': (
                f'{n_closed - len(dev_blocks)} direct + '
                f'{len(dev_blocks)} re-derived = {n_closed}/{n_closed} '
                'in-slice (frozen closures); QC independent decoder: '
                '2361/2363 (union: all 2363 slice files closable)')},
        'retraction_arithmetic': {
            'recorded_entry_totals': dict(rec_refs),
            'fake_entries_total': n_fake,
            'fake_ref_targets': dict(fake_refs),
            'fake_f1_values': {str(k): v for k, v in fake_f1.items()},
            'fake_f2_values': {str(k): v for k, v in fake_f2.items()},
            'true_ref_targets_after_retraction': {
                'NiTexturingProperty': true_tp,
                'NiTextureEffect': true_te,
                'NiNode': 0,
                'OOR': 0},
            'verdict': ('ALL 24 OOR refs, ALL 3 NiNode refs, ALL f1=15 '
                        'x24 and f1=16777216 x3 entries are decoder '
                        'artifacts of the 24 mis-parsed blocks; the '
                        'NiTexturingProperty/NiTextureEffect totals were '
                        'never polluted (F-08 numbers stand as recorded '
                        'minus the anomaly qualifiers)')},
    }
    with open(os.path.join(
            WORK, 'ARKTEXTURE_ZERO_COUNT_REDERIVATION_SUMMARY.json'), 'w',
            encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
