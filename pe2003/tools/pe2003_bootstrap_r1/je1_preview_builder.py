#!/usr/bin/env python3
"""
je1_preview_builder.py — JOB PE2003R3-JE1 (Wave E3)
RUN: PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024

OWN tool for this run. Reads (never modifies):
  - PE42 Models.ark (archive SHA256 pinned below, verified before use)
  - 08_Local_Tools/pe2003_model_inspector.py (imported read-only as a module for
    NIF 4.1.0.12 block parsing — grammar grounding per its FIT_CALIBRATION)

Pipeline: in-memory ark member extraction (AK\\x03\\x04 ZIP-clone local chain,
F-111 layout) -> SHA256/CRC32 pin verification -> NIF parse (inspector module)
-> world transforms -> per-shape world-space geometry+material -> render JSON
-> self-contained Three.js r169 preview HTML (data inlined, no fetch).

All outputs under WORK_ROOT (data/je1, preview/). Never published.
Placement label SYNTHETIC_PREVIEW is baked into every HTML page and every JSON.
"""
import sys, os, json, struct, zlib, hashlib

RUN_ID = "PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024"
WORK_ROOT = r"D:\Eudoria_Reconstruction\PE2003\10_Campaigns\PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024"
ARK = (r"D:\Eudoria_Reconstruction\PE2003\02_Working_Install\PE2003_PE42_EN_80553A75"
       r"\program files\MindArk\Project Entropia\Data\Models\Models.ark")
INSPECTOR_DIR = r"D:\Eudoria_Reconstruction\PE2003\08_Local_Tools"
ARK_SHA256 = "F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62"
LOCAL_MAGIC = b'AK\x03\x04'

MODELS = {
    "296445": {"member": "296445.nif", "index": 1720, "size": 108876,
               "sha256": "656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862",
               "crc32_field": "CFAC1D3B",
               "expected": {"blocks": 155, "trishapes": 30, "vertices": 2415, "triangles": 1030}},
    "218757": {"member": "218757.nif", "index": 1189, "size": 56535,
               "sha256": "C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98",
               "crc32_field": "C40B12CA",
               "expected": {"blocks": 62, "trishapes": 14, "vertices": 1130, "triangles": 526}},
}
THREE_SHA256 = "0A3368C165EEA773490AEC7B77C22DE70E3EAC288503409256FDBF4D12578416"


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest().upper()


def read_u16(d, o):
    return struct.unpack_from('<H', d, o)[0]


def read_u32(d, o):
    return struct.unpack_from('<I', d, o)[0]


def scan_members(data):
    """Sequential AK local-header chain (F-111 standard-ZIP layout)."""
    entries, pos = [], 0
    while pos < len(data):
        if data[pos:pos + 4] != LOCAL_MAGIC:
            nxt = data.find(LOCAL_MAGIC, pos + 1)
            if nxt < 0:
                break
            pos = nxt
            continue
        crc = read_u32(data, pos + 14)
        comp = read_u32(data, pos + 18)
        uncomp = read_u32(data, pos + 22)
        name_len = read_u16(data, pos + 26)
        extra_len = read_u16(data, pos + 28)
        name_start = pos + 30
        data_start = name_start + name_len + extra_len
        name = data[name_start:name_start + name_len].decode('ascii', errors='replace')
        entries.append({'name': name, 'crc32': crc, 'size': comp, 'uncomp': uncomp,
                        'index': len(entries), 'data_offset': data_start})
        pos = data_start + comp
    return entries


def footer_carve(data, blocks, warnings):
    """Replicates inspector footer carve: last-block 8-byte tail = NIF footer."""
    last = blocks[-1]
    if last.get('parse_status') == 'MISALIGNED':
        rem = len(data) - 8
        nroots = read_u32(data, rem)
        if 1 <= nroots <= 64 and rem + 4 + 4 * nroots == len(data) \
                and last.get('parsed_end') == rem:
            last['data_end'] = rem
            last['parse_status'] = 'FIELDS_CONFIRMED'
            last.pop('parsed_end', None)
            last.pop('expected_end', None)
            if warnings and warnings[-1].startswith('block %d' % last['index']):
                warnings.pop()
    nroots = read_u32(data, len(data) - 8) if len(data) >= 8 else 0
    root_ref = read_u32(data, len(data) - 4) if len(data) >= 12 else -1
    return {'num_roots': nroots, 'root_ref': root_ref,
            'footer_bytes': 8, 'status': 'CONFIRMED' if 1 <= nroots <= 64 else 'UNVERIFIED'}


def build_render_model(nif_bytes, model_id):
    sys.path.insert(0, INSPECTOR_DIR)
    import pe2003_model_inspector as ins
    hdr = ins.parse_header(nif_bytes)
    blocks = ins.block_chain(nif_bytes, hdr)
    warnings = ins.parse_blocks(nif_bytes, blocks)
    footer = footer_carve(nif_bytes, blocks, warnings)
    parent, roots = ins.build_hierarchy(blocks)
    W = ins.world_transforms(blocks, parent, roots)
    mats_by_ref = {b['index']: b for b in blocks if b['type'] == 'NiMaterialProperty'}
    shapes_out = []
    tot_v = tot_t = 0
    for b in blocks:
        if b['type'] != 'NiTriShape':
            continue
        dref = b.get('data_ref', -1)
        d = blocks[dref] if 0 <= dref < len(blocks) and blocks[dref]['type'] == 'NiTriShapeData' else None
        if d is None or not d.get('has_vertices'):
            shapes_out.append({'block': b['index'], 'name': b.get('name', ''), 'error': 'NO_DATA'})
            continue
        Rm, T, S = W[b['index']]
        verts = []
        for p in d['vertices']:
            wp = [T[i] + S * sum(Rm[i][k] * p[k] for k in range(3)) for i in range(3)]
            verts.append([round(wp[0], 4), round(wp[2], 4), round(wp[1], 4)])  # NIF z-up -> three y-up
        tris = []
        r2 = ins.R(d and nif_bytes, 0)  # unused placeholder to keep import explicit
        # re-read triangles from parsed cache: inspector consumed them in-place
        tris = b.get('_triangles_cache') or []
        color, emissive, alpha = [0.7, 0.7, 0.7], [0, 0, 0], 1.0
        mat_names = []
        for pr in b.get('property_refs', []):
            pb = blocks[pr] if 0 <= pr < len(blocks) else None
            if pb is None:
                continue
            if pb['type'] == 'NiMaterialProperty':
                mat_names.append(pb.get('name', ''))
                if pb.get('diffuse'):
                    color = [round(max(0.0, min(1.0, c)), 4) for c in pb['diffuse']]
                if pb.get('emissive'):
                    emissive = [round(max(0.0, min(1.0, c)), 4) for c in pb['emissive']]
                if pb.get('material_alpha') is not None:
                    alpha = pb['material_alpha']
            elif pb['type'] == 'NiAlphaProperty':
                if pb.get('flags', 0) & 0x0001:
                    alpha = min(alpha, 0.6)
        shapes_out.append({
            'block': b['index'], 'name': b.get('name', ''),
            'num_vertices': d['num_vertices'], 'num_triangles': d['num_triangles'],
            'vertices': verts, 'triangles': tris,
            'material_names': mat_names, 'color': color,
            'emissive': emissive, 'opacity': round(alpha, 3),
        })
        tot_v += d['num_vertices']
        tot_t += d['num_triangles']
    census = {}
    for b in blocks:
        census[b['type']] = census.get(b['type'], 0) + 1
    return {
        'model_id': model_id,
        'header': {'header_string': hdr['header_string'], 'version': hdr['version_u32'],
                   'num_blocks': hdr['num_blocks']},
        'footer': footer, 'roots': roots,
        'block_census': census, 'parse_warnings': warnings,
        'misaligned_blocks': [b['index'] for b in blocks if b.get('parse_status') == 'MISALIGNED'],
        'num_shapes': len([s for s in shapes_out if 'error' not in s]),
        'total_vertices': tot_v, 'total_triangles': tot_t,
        'shapes': shapes_out,
        '_blocks_raw': blocks,
    }


def triangles_from_data(nif_bytes, blocks):
    """Second pass: re-parse NiTriShapeData triangle index arrays (the inspector
    does not cache them). Uses the same layout: after UV sets, u16 num_triangles,
    u32 num_triangle_points, then num_triangles x (u16,u16,u16)."""
    import pe2003_model_inspector as ins
    out = {}
    for b in blocks:
        if b['type'] != 'NiTriShape':
            continue
        dref = b.get('data_ref', -1)
        db = blocks[dref] if 0 <= dref < len(blocks) else None
        if db is None or db['type'] != 'NiTriShapeData' or not db.get('has_vertices'):
            continue
        r = ins.R(nif_bytes, db['data_offset'])
        nv = r.u16()
        if r.bool1():
            for _ in range(nv):
                r.vec3()
        if r.bool1():
            for _ in range(nv):
                r.vec3()
        r.vec3()
        r.f32()
        if r.bool1():
            for _ in range(nv):
                r.f32(); r.f32(); r.f32(); r.f32()
        nsets = r.u16() & 63
        for _s in range(nsets):
            for _v in range(nv):
                r.f32(); r.f32()
        nt = r.u16()
        r.u32()
        tris = [[r.u16(), r.u16(), r.u16()] for _ in range(nt)]
        valid = all(0 <= x < nv for t in tris for x in t)
        out[b['index']] = {'tris': tris, 'valid': valid, 'cursor': r.p,
                           'data_end': db['data_end']}
    return out


HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>SYNTHETIC_PREVIEW __MODEL_ID__</title>
<style>body{margin:0;overflow:hidden;background:#101418;font-family:monospace}
#hud{position:fixed;left:8px;top:8px;color:#9fe8ff;font-size:12px;z-index:10;
background:rgba(0,0,0,.55);padding:6px 10px;border:1px solid #2a4}</style></head>
<body>
<div id="hud">SYNTHETIC_PREVIEW &mdash; NOT HISTORICAL PLACEMENT &mdash; NOT RECOVERY<br>
PE42 Models.ark member __MODEL_ID__.nif &mdash; camera angle __ANGLE__<br>
<span id="statline">rendering...</span></div>
<script type="module">
import * as THREE from './vendor/three.module.js';
const MODEL = __MODEL_JSON__;
const params = new URLSearchParams(location.search);
const angleIdx = parseInt(params.get('angle') || '1', 10);
const ANGLES = [{az: 35, el: 22, name: 'angle1'}, {az: 210, el: 55, name: 'angle2'}];
const ang = ANGLES[(angleIdx - 1) % ANGLES.length];
const notrans = params.get('notrans') === '1';
const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(1);
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101418);
scene.add(new THREE.AmbientLight(0xffffff, 0.55));
const sun = new THREE.DirectionalLight(0xffffff, 1.6);
sun.position.set(60, 120, 40); scene.add(sun);
const sun2 = new THREE.DirectionalLight(0x8899bb, 0.5);
sun2.position.set(-60, 40, -80); scene.add(sun2);
const group = new THREE.Group(); scene.add(group);
let vTot = 0, tTot = 0, meshCount = 0;
for (const s of MODEL.shapes) {
  if (!s.vertices || !s.vertices.length) continue;
  const g = new THREE.BufferGeometry();
  const pos = new Float32Array(s.vertices.length * 3);
  s.vertices.forEach((v, i) => pos.set(v, i * 3));
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const idx = [];
  for (const t of s.triangles) idx.push(t[0], t[1], t[2]);
  g.setIndex(idx);
  g.computeVertexNormals();
  const m = new THREE.MeshStandardMaterial({
    color: new THREE.Color(...s.color), emissive: new THREE.Color(...s.emissive),
    transparent: notrans ? false : s.opacity < 1.0,
    opacity: notrans ? 1.0 : s.opacity,
    side: THREE.DoubleSide, forceSinglePass: true,
    roughness: 0.85, metalness: 0.05});
  const mesh = new THREE.Mesh(g, m);
  mesh.userData.shapeName = s.name;
  group.add(mesh);
  vTot += s.num_vertices; tTot += idx.length / 3; meshCount++;
}
const box = new THREE.Box3().setFromObject(group);
let idxSum = 0, posSum = 0, meshList = [];
group.traverse(o => { if (o.isMesh && o.geometry.index) {
  idxSum += o.geometry.index.count / 3;
  posSum += o.geometry.attributes.position.count;
  meshList.push({name: o.userData.shapeName, idx: o.geometry.index.count / 3});}});
window.__meshDebug = {idx_sum: idxSum, pos_sum: posSum, meshes: meshList.length};
const center = box.getCenter(new THREE.Vector3());
const size = box.getSize(new THREE.Vector3());
const radius = 0.5 * Math.max(size.x, size.y, size.z) || 1;
const dist = radius * 2.2;
const az = ang.az * Math.PI / 180, el = ang.el * Math.PI / 180;
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, radius * 0.01, radius * 100);
camera.position.set(
  center.x + dist * Math.cos(el) * Math.cos(az),
  center.y + dist * Math.sin(el),
  center.z + dist * Math.cos(el) * Math.sin(az));
camera.lookAt(center);
renderer.render(scene, camera);
// coverage: count non-background pixels on a downscaled readback
const c2 = document.createElement('canvas');
c2.width = 160; c2.height = Math.round(160 * innerHeight / innerWidth);
const ctx = c2.getContext('2d');
ctx.drawImage(renderer.domElement, 0, 0, c2.width, c2.height);
const px = ctx.getImageData(0, 0, c2.width, c2.height).data;
let covered = 0;
for (let i = 0; i < px.length; i += 4) {
  if (Math.abs(px[i] - 16) + Math.abs(px[i+1] - 20) + Math.abs(px[i+2] - 24) > 18) covered++;
}
const coverage = covered / (px.length / 4);
const info = renderer.info.render;
window.__renderStats = {
  model_id: MODEL.model_id, angle: angleIdx, angle_name: ang.name,
  meshes_rendered: meshCount,
  frame_triangles: info.triangles,
  draw_calls: info.calls,
  geometry_vertex_sum: window.__meshDebug.pos_sum,
  geometry_triangle_sum: window.__meshDebug.idx_sum,
  note_vertex_count: 'renderer.info.render.vertices was removed in three.js r158; vertex verification uses geometry attribute sums',
  pipeline_vertices_declared: vTot, pipeline_triangles_declared: tTot,
  parse_total_vertices: MODEL.total_vertices, parse_total_triangles: MODEL.total_triangles,
  pixel_coverage: Math.round(coverage * 10000) / 100,
  aabb_min: [round3(box.min.x), round3(box.min.y), round3(box.min.z)],
  aabb_max: [round3(box.max.x), round3(box.max.y), round3(box.max.z)],
  center: [round3(center.x), round3(center.y), round3(center.z)],
  label: 'SYNTHETIC_PREVIEW', ready: true,
  mesh_index_sum: window.__meshDebug.idx_sum, mesh_count_traversed: window.__meshDebug.meshes};
function round3(x){return Math.round(x*1000)/1000;}
document.getElementById('statline').textContent =
  'meshes=' + meshCount + ' tris=' + info.triangles + ' verts=' + info.vertices +
  ' coverage=' + window.__renderStats.pixel_coverage + '%' +
  ' | SYNTHETIC_PREVIEW angle ' + ang.name;
const pre = document.createElement('pre');
pre.id = 'statsjson';
pre.textContent = JSON.stringify(window.__renderStats);
pre.style.display = 'none';
document.body.appendChild(pre);
</script></body></html>
"""


def main():
    result = {'run': RUN_ID, 'tool': 'je1_preview_builder.py',
              'label': 'SYNTHETIC_PREVIEW', 'models': {}}
    ok = True
    ark_data = open(ARK, 'rb').read()
    ark_sha = sha256_hex(ark_data)
    if ark_sha != ARK_SHA256:
        print('FATAL archive sha mismatch', ark_sha)
        sys.exit(2)
    print('archive sha OK', ark_sha)
    members = scan_members(ark_data)
    by_name = {e['name']: e for e in members}
    for mid, spec in MODELS.items():
        e = by_name.get(spec['member'])
        checks = {
            'archive_sha256': ark_sha,
            'member_index': {'expected': spec['index'], 'actual': e['index'] if e else None,
                             'ok': bool(e and e['index'] == spec['index'])},
        }
        blob = ark_data[e['data_offset']:e['data_offset'] + e['size']] if e else b''
        checks['size'] = {'expected': spec['size'], 'actual': len(blob),
                          'ok': len(blob) == spec['size']}
        checks['sha256'] = {'expected': spec['sha256'], 'actual': sha256_hex(blob),
                            'ok': sha256_hex(blob) == spec['sha256']}
        crc = zlib.crc32(blob) & 0xFFFFFFFF
        checks['crc32'] = {'expected': spec['crc32_field'], 'actual': '%08X' % crc,
                           'ok': ('%08X' % crc) == spec['crc32_field']}
        all_ok = all(v['ok'] if isinstance(v, dict) else v for k, v in checks.items()
                     if k != 'archive_sha256')
        if not all_ok:
            print('FATAL pin check failed for', mid, json.dumps(checks))
            sys.exit(3)
        rm = build_render_model(blob, mid)
        tris = triangles_from_data(blob, rm.pop('_blocks_raw'))
        for s in rm['shapes']:
            t = tris.get(s['block'])
            if t:
                s['triangles'] = t['tris']
                s['triangles_index_valid'] = t['valid']
        exp = spec['expected']
        verify = {
            'blocks': {'expected': exp['blocks'], 'actual': rm['header']['num_blocks'],
                       'ok': rm['header']['num_blocks'] == exp['blocks']},
            'trishapes': {'expected': exp['trishapes'], 'actual': rm['num_shapes'],
                          'ok': rm['num_shapes'] == exp['trishapes']},
            'vertices': {'expected': exp['vertices'], 'actual': rm['total_vertices'],
                         'ok': rm['total_vertices'] == exp['vertices']},
            'triangles': {'expected': exp['triangles'], 'actual': rm['total_triangles'],
                          'ok': rm['total_triangles'] == exp['triangles']},
        }
        v_ok = all(v['ok'] for v in verify.values())
        print(mid, 'verify:', json.dumps(verify), '->', 'OK' if v_ok else 'MISMATCH')
        ok = ok and v_ok
        checks['nif_parse'] = {'warnings': rm['parse_warnings'],
                               'misaligned': rm['misaligned_blocks'],
                               'footer': rm['footer']}
        out_json = {'model_id': mid, 'label': 'SYNTHETIC_PREVIEW',
                    'nif_header': rm['header'], 'block_census': rm['block_census'],
                    'roots': rm['roots'], 'total_vertices': rm['total_vertices'],
                    'total_triangles': rm['total_triangles'],
                    'shapes': rm['shapes']}
        jpath = os.path.join(WORK_ROOT, 'data', 'je1', 'render_%s.json' % mid)
        with open(jpath, 'w', encoding='utf-8') as f:
            json.dump(out_json, f)
        html = HTML_TEMPLATE.replace('__MODEL_ID__', mid).replace('__ANGLE__', '1 or 2') \
            .replace('__MODEL_JSON__', json.dumps(out_json))
        hpath = os.path.join(WORK_ROOT, 'preview', 'preview_%s.html' % mid)
        with open(hpath, 'w', encoding='utf-8') as f:
            f.write(html)
        result['models'][mid] = {'pins': checks, 'verify_vs_parse_reports': verify,
                                 'render_json': jpath, 'html': hpath,
                                 'json_sha256': sha256_hex(open(jpath, 'rb').read())}
    result['three_module_sha256'] = THREE_SHA256
    spath = os.path.join(WORK_ROOT, 'data', 'je1', 'build_stats.json')
    with open(spath, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=1)
    print('BUILD', 'OK' if ok else 'FAILED', '->', spath)
    sys.exit(0 if ok else 4)


if __name__ == '__main__':
    main()
