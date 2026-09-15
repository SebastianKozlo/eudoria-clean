#!/usr/bin/env python3
"""s07_full_validation.py — full corpus validation for the world slice.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (§8, §9, §10, G6, G7).

Split discipline (§10):
- Candidate files (only supported world-slice types) sorted by payload SHA256
  (from NIF_VERSION_CENSUS.csv — independent identity).
- TRAIN = first 80%; HOLDOUT = last 20%.
- The discovery file 505775.nif (used to debug the decoder during development)
  is FORCED into TRAIN regardless of sort position (disclosed).
- Hypothesis = the decoder code + schema baseline; frozen before holdout run
  (SCRIPT_SHA256 recorded as hypothesis_sha).

Per file: full-file closure decode. Per type: closure-pass accounting.
Evidence captured per block (for §9 field validation):
- ref target block types (link roles), string encodings, enum value
  distributions, layout-variant decisions, Ark boundary decisions.
"""
import csv
import hashlib
import json
import os
import struct
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE, LOCAL_OUT, REPO_RAW  # noqa: E402
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, ArkBlockError)
from s04_nifxml_baseline import Unresolved  # noqa: E402

SUPPORTED = set('''NiNode NiTriShape NiTriShapeData NiTexturingProperty
NiMaterialProperty NiAlphaProperty NiZBufferProperty NiStencilProperty
NiVertexColorProperty NiSpecularProperty NiShadeProperty NiDitherProperty
NiFogProperty NiSourceTexture NiPixelData NiTextureEffect NiPointLight
NiSpotLight NiDirectionalLight NiAmbientLight NiStringExtraData
NiIntegerExtraData NiBooleanExtraData NiArkAnimationExtraData
NiArkImporterExtraData NiArkTextureExtraData NiArkViewportInfoExtraData
NiArkShaderExtraData NiCollisionData NiSortAdjustNode NiBillboardNode
NiArkBillboardNode'''.split())


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    split = sys.argv[1] if len(sys.argv) > 1 else 'ALL'
    v = WorldSliceValidator()
    walk = walk_bnt2(ARCHIVE)
    # identity from the independent version census
    sha_by_name = {}
    with open(os.path.join(REPO_RAW, 'NIF_VERSION_CENSUS.csv'),
              newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sha_by_name[row['name']] = row['sha256_stored']
    histos = json.load(open(
        LOCAL_OUT + r'\02_WORK\pcg953_type_histograms_independent.json',
        encoding='utf-8'))
    cands = []
    for e in walk['entries']:
        m = histos.get(e['name'])
        if m is None:
            continue
        if set(m['type_counts']) <= SUPPORTED:
            cands.append(e)
    cands.sort(key=lambda e: (sha_by_name.get(e['name'], ''), e['name']))
    n = len(cands)
    train_n = int(n * 0.8)
    train_set = set(c['name'] for c in cands[:train_n])
    hold_set = set(c['name'] for c in cands[train_n:])
    if '505775.nif' in hold_set:
        hold_set.discard('505775.nif')
        train_set.add('505775.nif')
    print(f'candidates={n} train={len(train_set)} holdout={len(hold_set)}')

    results = {'train': [], 'hold': []}
    evidence = {
        'layout_variant': defaultdict(Counter),
        'ark_importer_tail': Counter(),
        'ark_texture_count_source': Counter(),
        'ark_anim_ext_len': Counter(),
        'ark_viewport_ext_len': Counter(),
        'ark_billboard_mode': Counter(),
        'apply_mode_values': Counter(),
        'num_uv_sets_values': Counter(),
        'extra_vectors_flags_values': Counter(),
        'consistency_flags_values': Counter(),
        'has_shader_values': Counter(),
        'arktexture_entry_ref_targets': Counter(),
        'arktexture_entry_f1': Counter(),
        'arktexture_entry_f2': Counter(),
        'arktexture_entry_ref_range': Counter(),
        'arktexture_trailing': [],
        'sourcetext_use_external': Counter(),
        'sourcetext_unknown_link_targets': Counter(),
        'top_object_types': Counter(),
        'node_flags': Counter(),
        'material_alpha_range': Counter(),
        'texture_count_values': Counter(),
        'importer_int1': Counter(),
        'importer_version_strings': Counter(),
        'string_encoding_issues': Counter(),
        'ref_out_of_range': Counter(),
    }
    hypothesis_files = [os.path.join(HERE, 's06_world_slice_validator.py'),
                        os.path.join(HERE, 's04_nifxml_baseline.py')]
    hypothesis_sha = hashlib.sha256()
    for hf in hypothesis_files:
        hypothesis_sha.update(open(hf, 'rb').read())
    hypothesis_sha = hypothesis_sha.hexdigest().upper()
    t0 = time.time()
    processed = 0
    with open(ARCHIVE, 'rb') as f:
        for e in cands:
            subset = ('train' if e['name'] in train_set else
                      'hold' if e['name'] in hold_set else None)
            if subset is None:
                continue
            if split != 'ALL' and subset != split:
                continue
            f.seek(e['offset'])
            data = f.read(e['size'])
            rec = {'name': e['name'], 'subset': subset,
                   'sha256': sha_by_name.get(e['name'], '')}
            try:
                res = v.decode_file(data)
                rec['closure'] = 'OK'
                rec['num_blocks'] = res['num_blocks']
                rec['tops'] = len(res['top_objects'])
                rec['attempts'] = res.get('attempts', 0)
                # ---- evidence harvesting ----
                types = []
                for i, blk in enumerate(res['blocks']):
                    t = blk['__type__']
                    types.append(t)
                    if '__layout_variant__' in blk:
                        evidence['layout_variant'][t][
                            blk['__layout_variant__']] += 1
                    d = blk.get('__decision__')
                    if isinstance(d, dict):
                        if d.get('kind') == 'importer':
                            evidence['ark_importer_tail'][d['tail']] += 1
                            evidence['importer_int1'][blk.get('int1')] += 1
                            evidence['importer_version_strings'][
                                blk.get('version_string')] += 1
                        elif d.get('kind') == 'texture':
                            evidence['ark_texture_count_source'][
                                d['count_source']] += 1
                        elif d.get('kind') == 'ext':
                            if t == 'NiArkAnimationExtraData':
                                evidence['ark_anim_ext_len'][
                                    blk.get('ext_len')] += 1
                            else:
                                evidence['ark_viewport_ext_len'][
                                    blk.get('ext_len')] += 1
                        elif d.get('kind') == 'arkbillboard':
                            evidence['ark_billboard_mode'][
                                blk.get('mode_style')] += 1
                    if t == 'NiTexturingProperty':
                        am = blk.get('Apply Mode')
                        evidence['apply_mode_values'][am] += 1
                        evidence['texture_count_values'][
                            blk.get('Texture Count')] += 1
                    if t == 'NiTriShapeData':
                        evidence['num_uv_sets_values'][
                            blk.get('Num UV Sets')] += 1
                        evidence['extra_vectors_flags_values'][
                            blk.get('Extra Vectors Flags')] += 1
                        evidence['consistency_flags_values'][
                            blk.get('Consistency Flags')] += 1
                    if t == 'NiTriShape':
                        evidence['has_shader_values'][
                            blk.get('Has Shader')] += 1
                    if t == 'NiNode':
                        evidence['node_flags'][blk.get('Flags')] += 1
                    if t == 'NiArkTextureExtraData':
                        for en in blk.get('entries', []):
                            evidence['arktexture_entry_f1'][en['f1']] += 1
                            evidence['arktexture_entry_f2'][en['f2']] += 1
                            ref = en['ref']
                            if 0 <= ref < res['num_blocks']:
                                tgt = res['blocks'][ref]['__type__']
                                evidence['arktexture_entry_ref_targets'][
                                    tgt] += 1
                            elif ref == -1:
                                evidence['arktexture_entry_ref_targets'][
                                    'NULL(-1)'] += 1
                            else:
                                evidence['arktexture_entry_ref_targets'][
                                    f'OOR({ref})'] += 1
                            if len(evidence['arktexture_trailing']) < 200:
                                evidence['arktexture_trailing'].append(
                                    en['tr9'])
                    if t == 'NiSourceTexture':
                        evidence['sourcetext_use_external'][
                            blk.get('Use External')] += 1
                        ul = blk.get('Unknown Link')
                        if isinstance(ul, int) and 0 <= ul < res['num_blocks']:
                            evidence['sourcetext_unknown_link_targets'][
                                res['blocks'][ul]['__type__']] += 1
                        elif ul == -1:
                            evidence['sourcetext_unknown_link_targets'][
                                'NULL(-1)'] += 1
                # top objects + ref range check
                for tref in res['top_objects']:
                    if 0 <= tref < res['num_blocks']:
                        evidence['top_object_types'][
                            res['blocks'][tref]['__type__']] += 1
                    elif tref != -1:
                        evidence['ref_out_of_range'][
                            f'top:{tref}'] += 1
                # generic ref-range check for NET/AV/geometry blocks
                for i, blk in enumerate(res['blocks']):
                    for key, val in blk.items():
                        if key.startswith('__'):
                            continue
                        if key in ('Children', 'Effects', 'Extra Data List',
                                   'Properties', 'Affected Nodes',
                                   'Affected Node List Pointers'):
                            for r in (val or []):
                                if not (r == -1 or 0 <= r < res['num_blocks']):
                                    evidence['ref_out_of_range'][
                                        f'{blk["__type__"]}.{key}:{r}'] += 1
                        if key in ('Controller', 'Data', 'Skin Instance',
                                   'Collision Object', 'Next Controller',
                                   'Target', 'Texture Data', 'Palette'):
                            if not (val == -1 or 0 <= val < res['num_blocks']):
                                evidence['ref_out_of_range'][
                                    f'{blk["__type__"]}.{key}:{val}'] += 1
                rec['types'] = types
            except (ArkBlockError, Unresolved, struct.error, ValueError,
                    IndexError) as ex:
                rec['closure'] = f'FAIL:{str(ex)[:120]}'
                rec['num_blocks'] = None
            results[subset].append(rec)
            processed += 1
            if processed % 100 == 0:
                print(f'  {processed} files, {time.time()-t0:.0f}s',
                      flush=True)
    out_dir = LOCAL_OUT + r'\02_WORK'
    out_path = out_dir + r'\WORLD_SLICE_VALIDATION.json'
    prior = None
    if os.path.exists(out_path):
        try:
            prior = json.load(open(out_path, encoding='utf-8'))
        except Exception:
            prior = None
    merged = {'train': [], 'hold': []}
    if prior:
        for k in merged:
            merged[k] = prior.get('results', prior).get(k, [])
    # replace only the subset(s) produced by THIS invocation
    for k in results:
        if results[k]:
            merged[k] = results[k]
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'results': merged,
                   'evidence': {k: (dict(v) if isinstance(v, Counter)
                                    else (dict(v) if isinstance(v, defaultdict)
                                          else v))
                                for k, v in evidence.items()},
                   'hypothesis_sha': hypothesis_sha,
                   'n_candidates': n, 'train_n': len(train_set),
                   'holdout_n': len(hold_set)}, f, indent=1)
    # summary
    for subset in ('train', 'hold'):
        rs = results[subset]
        ok = sum(1 for r in rs if r['closure'] == 'OK')
        print(f'{subset}: {ok}/{len(rs)} closure OK '
              f'({100*ok/len(rs):.1f}%)' if rs else f'{subset}: empty')
    print(f'hypothesis_sha={hypothesis_sha}')
    print(f'total time {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
