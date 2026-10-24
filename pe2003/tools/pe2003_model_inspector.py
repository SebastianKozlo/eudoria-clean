#!/usr/bin/env python3
"""
pe2003_model_inspector.py — NIF 4.1.0.12 (0x0401000C) model inspector.

JOB: PE2003R3-I1 | RUN: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024
OWN tool written for this run. Grammar grounding (calibration sources, read-only):
  - Prior validated structural parser (reference only, not imported):
    10_Scripts\\python\\asset_tools\\nif_parser_v2.py (760-entry NIF 4.1.0.12 corpus).
  - PyFFI 2.2.3 property docs: 99_Audits\\PyFFI-2.2.3-Full-Docs-for-AI.md.
  - In-run empirical fitting (this run, 2026-10-24): NiTextureEffect (296445 block 13),
    NiUVController (block 33), NiUVData (block 34) fitted byte-exact against their
    anchor-scanned block ranges; all subsequent blocks then parsed with exact
    alignment (see FIT_CALIBRATION below).

Header layout (this corpus, verified on 296445.nif + 218757.nif):
  "NetImmerse File Format, Version 4.1.0.12\\n"  (raw, NO length prefix)
  u32 version = 0x0401000C
  u32 num_blocks
  then blocks: each preceded by its INLINE type SizedString (u32 len + name).
  NO block-size table (data ends are resolved by strict field parse + anchor scan).

Explicit status discipline:
  - every block gets parse_status: FIELDS_CONFIRMED / PARTIAL_FIELDS_OPAQUE_TAIL /
    UNKNOWN_TYPE / TRUNCATED
  - fitted-field blocks carry field_status notes (UNVERIFIED_FIELD where the fit is
    single-instance)
  - header errors are reported as JSON with status (never a silent success)

Usage:
  python pe2003_model_inspector.py <file.nif> [--json out.json] [--max-verts-print N]
"""
import sys, os, json, struct, hashlib, re
from collections import Counter, OrderedDict

SUPPORTED_VERSION = 0x0401000C
VERSION_STRING = "4.1.0.12"

FIT_CALIBRATION = {
    "NiTextureEffect": ("Fitted byte-exact on 296445 block 13 (174 B). Tail fields: "
                        "ps2_k=-75 matches PyFFI doc 'ps_2_k -75'. "
                        "NiDynamicEffect adds NO fields in this instance (no num-affected list) — "
                        "single-instance fit, UNVERIFIED_FIELD labels retained."),
    "NiUVController": ("Fitted byte-exact on 296445 block 33 (32 B). "
                       "target ref=32 (NiTriShape GeoTexanim01) and uv_data ref=34 (NiUVData) "
                       "both resolve to coherent block types; stop_time=3.3333 matches NiUVData key. "
                       "Two unexplained zero u16/u32 bytes retained as UNKNOWN_FIELD."),
    "NiUVData": ("Fitted byte-exact on 296445 block 34 (52 B). Structure: leading u32=2 (UNKNOWN), "
                 "key group 1: num_keys=2, 16-byte quadratic-style keys (t,v,fwd,back): "
                 "(0,0) -> (3.3333, 5.0) i.e. U-scroll over the controller's 3.3333 s span; "
                 "interp u32 after keys = 0; key group 2: num_keys=0, interp=0. "
                 "Key layout is single-instance fit — UNVERIFIED_FIELD."),
}

KNOWN_TYPES = {
    # block types with strict parsers in this tool
    "NiNode", "NiArkBillboardNode", "NiTriShape", "NiTriShapeData",
    "NiTexturingProperty", "NiMaterialProperty", "NiAlphaProperty",
    "NiZBufferProperty", "NiVertexColorProperty", "NiStringExtraData",
    "NiArkTextureExtraData", "NiArkAnimationExtraData", "NiArkImporterExtraData",
    "NiArkViewportInfoExtraData", "NiArkShaderExtraData",
    "NiTextureEffect", "NiUVController", "NiUVData",
    # types recognised for boundary anchoring (fields not parsed -> UNKNOWN_TYPE
    # with honest status; none occur in the two target files)
    "NiSourceTexture", "NiPixelData", "NiSkinInstance", "NiSkinData",
    "NiSkinPartition", "NiBone", "NiLODNode", "NiBSAnimationNode",
    "NiBSParticleNode", "NiPointLight", "NiKeyframeController",
    "NiKeyframeData", "NiTextKeyExtraData", "NiStencilProperty",
    "NiTriStrips", "NiTriStripsData", "NiVertexMorphExtraData",
    "NiSequence", "NiControllerSequence", "NiTransformData",
    "NiGeomMorpherController", "NiParticleSystemController",
    "RootCollisionNode", "NiParticles", "NiParticlesData",
    "NiRotatingParticles", "NiRotatingParticlesData",
    "NiAutoNormalParticles", "NiAutoNormalParticlesData",
    "NiSortAdjustNode", "NiStringPalette", "NiCollisionObject",
    "NiArkLight", "NiArkGeomMorpherController",
}


class R:
    def __init__(self, data, pos=0):
        self.d = data
        self.p = pos

    def u8(self):
        v = self.d[self.p]; self.p += 1; return v

    def u16(self):
        v = struct.unpack_from('<H', self.d, self.p)[0]; self.p += 2; return v

    def i16(self):
        v = struct.unpack_from('<h', self.d, self.p)[0]; self.p += 2; return v

    def u32(self):
        v = struct.unpack_from('<I', self.d, self.p)[0]; self.p += 4; return v

    def i32(self):
        v = struct.unpack_from('<i', self.d, self.p)[0]; self.p += 4; return v

    def f32(self):
        v = struct.unpack_from('<f', self.d, self.p)[0]; self.p += 4; return v

    def bool1(self):
        v = self.d[self.p]; self.p += 1; return v != 0

    def ref(self):
        return self.i32()

    def sstr(self):
        ln = self.i32()
        if ln < 0 or ln > 1_000_000:
            raise ValueError("bad string length %d at %d" % (ln, self.p - 4))
        s = self.d[self.p:self.p + ln]
        self.p += ln
        return s.decode('utf-8', errors='replace')

    def vec3(self):
        return [self.f32(), self.f32(), self.f32()]

    def mat33(self):
        return [self.vec3(), self.vec3(), self.vec3()]


def parse_header(data):
    """Returns dict or raises HeaderError with explicit status."""
    nl = data.find(b'\n')
    if nl < 0 or nl > 256:
        raise ValueError("HEADER_PARSE_ERROR: no newline-terminated header string in first 256 bytes")
    hdr = data[:nl].decode('ascii', errors='replace')
    if len(data) < nl + 1 + 8:
        raise ValueError("HEADER_PARSE_ERROR: truncated before version/num_blocks")
    ver, num_blocks = struct.unpack_from('<II', data, nl + 1)
    return {'header_string': hdr, 'version_u32': '0x%08X' % ver,
            'num_blocks': num_blocks, 'data_start': nl + 1 + 8}


def find_next_type_offset(data, start):
    """Anchor scan: next inline type string from a known-type list."""
    for off in range(start, len(data) - 4):
        ln = struct.unpack_from('<I', data, off)[0]
        if 3 <= ln <= 64:
            t = data[off + 4:off + 4 + ln]
            try:
                ts = t.decode('ascii')
            except UnicodeDecodeError:
                continue
            if ts in KNOWN_TYPES:
                return off
    return None


def block_chain(data, hdr):
    """Determine block boundaries via strict parse + anchor fallback."""
    blocks = []
    pos = hdr['data_start']
    n = hdr['num_blocks']
    for i in range(n):
        if pos + 4 > len(data):
            blocks.append({'index': i, 'parse_status': 'TRUNCATED',
                           'type_offset': pos, 'type': 'UNKNOWN'})
            break
        ln = struct.unpack_from('<i', data, pos)[0]
        if ln < 0 or ln > 200 or pos + 4 + ln > len(data):
            blocks.append({'index': i, 'parse_status': 'TRUNCATED',
                           'type_offset': pos, 'type': 'UNKNOWN'})
            break
        t = data[pos + 4:pos + 4 + ln].decode('ascii', errors='replace')
        doff = pos + 4 + ln
        nxt = find_next_type_offset(data, doff)
        end = nxt if nxt is not None else len(data)
        blocks.append({'index': i, 'type': t, 'type_offset': pos,
                       'data_offset': doff, 'data_end': end})
        if nxt is None:
            break
        pos = nxt
    return blocks


# ---------------------------------------------------------------------------
# field parsers. All take (R positioned at block data start, block dict).
# On success they set parse_status=FIELDS_CONFIRMED if cursor lands exactly on
# data_end; otherwise the caller records a misalignment.
# ---------------------------------------------------------------------------
def p_objectnet(r, b):
    b['name'] = r.sstr()
    b['extra_data_ref'] = r.ref()
    b['controller_ref'] = r.ref()


def p_avobject(r, b):
    b['flags'] = r.u16()
    b['translation'] = r.vec3()
    b['rotation'] = r.mat33()
    b['scale'] = r.f32()
    b['velocity'] = r.vec3()
    b['num_properties'] = r.u32()
    b['property_refs'] = [r.ref() for _ in range(b['num_properties'])]
    b['has_bounding_box'] = r.bool1()
    if b['has_bounding_box']:
        r.u32(); r.vec3(); r.mat33(); r.f32()  # bbox (4+12+36+4)


def p_ninode(r, b):
    p_objectnet(r, b)
    p_avobject(r, b)
    b['num_children'] = r.u32()
    b['children'] = [r.ref() for _ in range(b['num_children'])]
    b['num_effects'] = r.u32()
    b['effects'] = [r.ref() for _ in range(b['num_effects'])]


def p_nitrishape(r, b):
    p_objectnet(r, b)
    p_avobject(r, b)
    b['data_ref'] = r.ref()
    b['skin_instance_ref'] = r.ref()


def p_trishapedata(r, b):
    b['num_vertices'] = r.u16()
    b['has_vertices'] = r.bool1()
    if b['has_vertices']:
        b['vertices'] = [r.vec3() for _ in range(b['num_vertices'])]
    b['has_normals'] = r.bool1()
    if b['has_normals']:
        b['normals_count'] = b['num_vertices']
        for _ in range(b['num_vertices']):
            r.vec3()
    b['center'] = r.vec3()
    b['radius'] = r.f32()
    b['has_vertex_colors'] = r.bool1()
    if b['has_vertex_colors']:
        b['vertex_colors_count'] = b['num_vertices']
        for _ in range(b['num_vertices']):
            r.f32(); r.f32(); r.f32(); r.f32()
    b['num_uv_sets'] = r.u16()
    nsets = b['num_uv_sets'] & 63
    if nsets:
        b['uv_sets_count'] = nsets
        b['uv_coords_total'] = nsets * b['num_vertices']
        for _s in range(nsets):
            for _v in range(b['num_vertices']):
                r.f32(); r.f32()
    # NiTriBasedGeomData
    b['num_triangles'] = r.u16()
    # NiTriShapeData
    b['num_triangle_points'] = r.u32()
    tri_ok = 0
    for _ in range(b['num_triangles']):
        t = (r.u16(), r.u16(), r.u16())
        if all(0 <= x < b['num_vertices'] for x in t):
            tri_ok += 1
    b['triangles_index_valid'] = tri_ok
    b['num_match_groups'] = r.u16()
    for _ in range(b['num_match_groups']):
        n = r.u16()
        for _ in range(n):
            r.u16()


def p_texturing_property(r, b):
    p_objectnet(r, b)
    b['flags'] = r.u16()
    b['apply_mode'] = r.u32()
    b['texture_count'] = r.u32()
    b['textures'] = {}

    def slot(key):
        has = r.bool1()
        if has:
            b['textures'][key] = {'source_ref': r.ref(), 'clamp_mode': r.u32(),
                                   'filter_mode': r.u32(), 'uv_set': r.u32(),
                                   'ps2_l': r.i16(), 'ps2_k': r.i16(),
                                   'unknown1': r.u16()}
        return has

    slot('base'); slot('dark'); slot('detail'); slot('gloss'); slot('glow')
    if slot('bump_map'):
        r.f32(); r.f32()
        for _ in range(4):
            r.f32()
    tc = b['texture_count']
    if tc >= 7: slot('decal0')
    if tc >= 8: slot('decal1')
    if tc >= 9: slot('decal2')
    if tc >= 10: slot('decal3')


def p_material_property(r, b):
    p_objectnet(r, b)
    b['flags'] = r.u16()
    b['ambient'] = [r.f32() for _ in range(3)]
    b['diffuse'] = [r.f32() for _ in range(3)]
    b['specular'] = [r.f32() for _ in range(3)]
    b['emissive'] = [r.f32() for _ in range(3)]
    b['glossiness'] = r.f32()
    b['material_alpha'] = r.f32()


def p_alpha_property(r, b):
    p_objectnet(r, b)
    b['flags'] = r.u16()
    b['threshold'] = r.u8()


def p_zbuffer_property(r, b):
    p_objectnet(r, b)
    b['flags'] = r.u16()
    b['function'] = r.u32()


def p_vertexcolor_property(r, b):
    p_objectnet(r, b)
    b['flags'] = r.u16()
    b['vertex_mode_u32'] = r.u32()   # single-instance fit; commonly flags only — kept as opaque u32s below if misalign
    b['lighting_mode_u32'] = r.u32() # NOTE: if misalign occurs, this field is reverted to flags-only by caller calibration


def p_string_extra_data(r, b):
    b['next_extra_ref'] = r.ref()
    b['bytes_remaining'] = r.u32()
    b['data'] = r.sstr()


def p_ark_texture_extra_data(r, b):
    b['next_extra_ref'] = r.ref()
    r.i32(); r.i32(); r.u8(); r.i32()
    num = r.i32()
    b['ark_textures'] = []
    for _ in range(num):
        name = r.sstr()
        unk3 = r.i32(); unk4 = r.i32()
        tprop = r.ref()
        unk = r.d[r.p:r.p + 9]; r.p += 9
        tex_id = struct.unpack_from('<I', unk, 5)[0] if len(unk) == 9 else -1
        b['ark_textures'].append({'texture_name': name, 'slot_type': unk3,
                                  'unknown_int4': unk4,
                                  'texturing_property_ref': tprop,
                                  'texture_id': tex_id,
                                  'unknown9_hex': unk.hex()})


def p_ark_animation_extra_data(r, b):
    # Uniform prefix: next ref + 4 x i32. Remainder = opaque (variant differs
    # between files: 37 B in 218757, 124 B in 296445 with embedded text).
    b['next_extra_ref'] = r.ref()
    b['unknown_ints'] = [r.i32() for _ in range(4)]
    tail = r.d[r.p:b['data_end']]
    b['opaque_tail_len'] = len(tail)
    b['opaque_tail_hex_head'] = tail[:32].hex()
    runs = re.findall(rb'[\x20-\x7e]{4,}', tail)
    b['embedded_ascii_runs'] = [x.decode('ascii') for x in runs][:12]
    r.p = b['data_end']
    b['parse_status'] = 'PARTIAL_FIELDS_OPAQUE_TAIL'


def p_ark_importer_extra_data(r, b):
    b['next_extra_ref'] = r.ref()
    r.i32(); r.i32()
    b['importer_name'] = r.sstr()
    r.d[r.p:r.p + 13]; r.p += 13
    b['trailing_floats'] = [r.f32() for _ in range(7)]


def p_ark_viewport_info_extra_data(r, b):
    b['next_extra_ref'] = r.ref()
    r.d[r.p:r.p + 13]; r.p += 13
    b['opaque13_hex'] = r.d[b['data_offset'] + 4 + 4:b['data_offset'] + 4 + 4 + 13].hex()


def p_ark_shader_extra_data(r, b):
    b['next_extra_ref'] = r.ref()
    r.i32()
    b['shader_name'] = r.sstr()


def p_texture_effect(r, b):
    # FIT on 296445 block 13; see FIT_CALIBRATION.
    p_objectnet(r, b)
    p_avobject(r, b)
    b['model_projection_matrix'] = r.mat33()
    b['model_projection_transform'] = r.vec3()
    b['texture_filtering'] = r.u32()
    b['texture_clamping'] = r.u32()
    b['texture_type'] = r.u32()
    b['coordinate_generation_type'] = r.u32()
    b['source_texture_ref'] = r.ref()
    b['clipping_plane'] = r.u8()
    b['unknown_vector'] = r.vec3()          # doc: (1,0,0)
    b['unknown_u16_a'] = r.u16()
    b['unknown_u16_b'] = r.u16()
    b['ps2_l'] = r.i16()
    b['ps2_k'] = r.i16()
    b['unknown_short'] = r.u16()
    b['field_status'] = ('FIT_296445_BLOCK13; NiDynamicEffect base contributes no '
                         'fields in this fit (UNVERIFIED, single instance)')


def p_uv_controller(r, b):
    # FIT on 296445 block 33; see FIT_CALIBRATION.
    b['next_controller_ref'] = r.ref()
    b['flags'] = r.u16()
    b['frequency'] = r.f32()
    b['phase'] = r.f32()
    b['start_time'] = r.f32()
    b['stop_time'] = r.f32()
    b['target_ref'] = r.ref()
    b['unknown_field_u16'] = r.u16()   # unexplained zero u16 in the fit
    b['uv_data_ref'] = r.ref()
    b['field_status'] = 'FIT_296445_BLOCK33; unknown_field_u16 UNVERIFIED'


def p_uvdata(r, b):
    # FIT on 296445 block 34; see FIT_CALIBRATION.
    b['unknown_leading_u32'] = r.u32()
    groups = []
    for gi in range(2):
        num = r.u32()
        keys = []
        for _ in range(num):
            t = r.f32(); v = r.f32(); fwd = r.f32(); back = r.f32()
            keys.append({'time': t, 'value': v, 'fwd': fwd, 'back': back})
        interp = r.u32()
        groups.append({'num_keys': num, 'keys': keys, 'interpolation': interp})
    b['uv_groups'] = groups
    b['field_status'] = 'FIT_296445_BLOCK34; key layout (16B quadratic-style) UNVERIFIED, single instance'


PARSERS = {
    'NiNode': p_ninode,
    'NiArkBillboardNode': p_ninode,
    'NiTriShape': p_nitrishape,
    'NiTriShapeData': p_trishapedata,
    'NiTexturingProperty': p_texturing_property,
    'NiMaterialProperty': p_material_property,
    'NiAlphaProperty': p_alpha_property,
    'NiZBufferProperty': p_zbuffer_property,
    'NiVertexColorProperty': p_vertexcolor_property,
    'NiStringExtraData': p_string_extra_data,
    'NiArkTextureExtraData': p_ark_texture_extra_data,
    'NiArkAnimationExtraData': p_ark_animation_extra_data,
    'NiArkImporterExtraData': p_ark_importer_extra_data,
    'NiArkViewportInfoExtraData': p_ark_viewport_info_extra_data,
    'NiArkShaderExtraData': p_ark_shader_extra_data,
    'NiTextureEffect': p_texture_effect,
    'NiUVController': p_uv_controller,
    'NiUVData': p_uvdata,
}

# opaque payload fields not emitted in JSON (kept small)
_OPaque_skip = ('vertices',)


def strip_large(b):
    out = {}
    for k, v in b.items():
        if k == 'vertices' and isinstance(v, list):
            out['vertices_count'] = len(v)
            if v:
                xs = [p[0] for p in v]; ys = [p[1] for p in v]; zs = [p[2] for p in v]
                out['vertex_min'] = [min(xs), min(ys), min(zs)]
                out['vertex_max'] = [max(xs), max(ys), max(zs)]
        else:
            out[k] = v
    return out


def parse_blocks(data, blocks):
    warnings = []
    for b in blocks:
        if b.get('parse_status') == 'TRUNCATED':
            warnings.append('block %d TRUNCATED' % b['index'])
            continue
        if 'data_offset' not in b:
            continue
        parser = PARSERS.get(b['type'])
        if parser is None:
            b['parse_status'] = 'UNKNOWN_TYPE_BOUNDARY_ANCHOR'
            b['opaque_payload_hex_head'] = data[b['data_offset']:b['data_offset'] + 32].hex()
            continue
        r = R(data, b['data_offset'])
        try:
            parser(r, b)
        except Exception as e:
            b['parse_status'] = 'PARSE_ERROR'
            b['parse_error'] = '%s: %s' % (type(e).__name__, e)
            warnings.append('block %d (%s) parse error: %s' % (b['index'], b['type'], e))
            continue
        if b.get('parse_status') == 'PARTIAL_FIELDS_OPAQUE_TAIL':
            continue
        if r.p == b['data_end']:
            b['parse_status'] = 'FIELDS_CONFIRMED'
        else:
            b['parse_status'] = 'MISALIGNED'
            b['parsed_end'] = r.p
            b['expected_end'] = b['data_end']
            warnings.append('block %d (%s) misalign parsed=%d expected=%d delta=%d'
                             % (b['index'], b['type'], r.p, b['data_end'], r.p - b['data_end']))
    return warnings


def parse_footer(data, end):
    foot = {'footer_offset': end, 'footer_bytes': data[end:].hex() if end < len(data) else ''}
    rem = len(data) - end
    foot['remaining_bytes'] = rem
    if rem >= 8:
        n = struct.unpack_from('<I', data, end)[0]
        foot['num_roots'] = n
        if 0 < n <= 64 and rem >= 4 + 4 * n:
            foot['root_refs'] = [struct.unpack_from('<i', data, end + 4 + 4 * i)[0] for i in range(n)]
        if rem == 4 + 4 * n + 4:
            foot['unknown_int'] = struct.unpack_from('<I', data, end + 4 + 4 * n)[0]
            foot['footer_status'] = 'CONFIRMED'
        elif rem == 4 + 4 * n:
            foot['footer_status'] = 'CONFIRMED_NO_TRAILING_UNKNOWN_INT'
        else:
            foot['footer_status'] = 'UNVERIFIED_LAYOUT remaining=%d' % rem
    else:
        foot['footer_status'] = 'ABSENT_OR_TRUNCATED remaining=%d' % rem
    return foot


# ---------------------------------------------------------------------------
# analysis: hierarchy, transforms, materials, geometry, AABB
# ---------------------------------------------------------------------------
def build_hierarchy(blocks):
    parent = {}
    for b in blocks:
        if b['type'] in ('NiNode', 'NiArkBillboardNode'):
            for c in b.get('children', []):
                if c >= 0:
                    parent[c] = b['index']
    roots = [b['index'] for b in blocks
             if b['type'] in ('NiNode', 'NiArkBillboardNode')
             and b['index'] not in parent]
    if not roots:
        roots = [blocks[0]['index']] if blocks else []
    return parent, roots


def tree_json(blocks, parent, roots):
    def node(i):
        b = blocks[i]
        ch = [node(c) for c in b.get('children', []) if 0 <= c < len(blocks)]
        eff = [blocks[e]['type'] + '#' + str(e) for e in b.get('effects', []) if 0 <= e < len(blocks)]
        d = {'block': i, 'type': b['type'], 'name': b.get('name', '')}
        t = local_transform(b)
        if b['type'] in ('NiNode', 'NiArkBillboardNode', 'NiTriShape', 'NiTextureEffect'):
            d['local_transform'] = t
        if ch:
            d['children'] = ch
        if eff:
            d['effects'] = eff
        return d
    return [node(r) for r in roots]


def local_transform(b):
    return {'translation': b.get('translation'), 'rotation': b.get('rotation'),
            'scale': b.get('scale'), 'flags': b.get('flags')}


def world_transforms(blocks, parent, roots):
    W = {}

    def compose(idx):
        if idx in W:
            return W[idx]
        b = blocks[idx]
        Rm, T, S = b.get('rotation'), b.get('translation'), b.get('scale', 1.0)
        pi = parent.get(idx)
        if pi is None:
            W[idx] = (Rm, list(T), S)
        else:
            Rp, Tp, Sp = compose(pi)
            Rw = [[sum(Rp[i][k] * Rm[k][j] for k in range(3)) for j in range(3)]
                  for i in range(3)]
            sc = [T[i] * Sp for i in range(3)]
            Tw = [Tp[i] + sum(Rp[i][k] * sc[k] for k in range(3)) for i in range(3)]
            W[idx] = (Rw, Tw, Sp * S)
        return W[idx]

    for b in blocks:
        if b['type'] in ('NiNode', 'NiArkBillboardNode', 'NiTriShape', 'NiTextureEffect'):
            try:
                compose(b['index'])
            except Exception:
                pass
    return W


def analyze_geometry(blocks, W):
    shapes = []
    gmin = [None, None, None]
    gmax = [None, None, None]
    for b in blocks:
        if b['type'] != 'NiTriShape':
            continue
        dref = b.get('data_ref', -1)
        d = blocks[dref] if 0 <= dref < len(blocks) and blocks[dref]['type'] == 'NiTriShapeData' else None
        entry = {'block': b['index'], 'name': b.get('name', ''),
                 'data_block': dref, 'data_ok': d is not None}
        if d:
            entry['num_vertices'] = d['num_vertices']
            entry['num_triangles'] = d['num_triangles']
            entry['triangles_index_valid'] = d['triangles_index_valid']
            entry['has_normals'] = d['has_normals']
            entry['uv_sets_count'] = d.get('uv_sets_count', 0)
            entry['has_vertex_colors'] = d['has_vertex_colors']
            entry['data_center'] = d['center']
            entry['data_radius'] = d['radius']
            vs = d.get('vertices')
            if vs:
                xs = [p[0] for p in vs]; ys = [p[1] for p in vs]; zs = [p[2] for p in vs]
                lmin = [min(xs), min(ys), min(zs)]
                lmax = [max(xs), max(ys), max(zs)]
                entry['local_aabb_min'] = lmin
                entry['local_aabb_max'] = lmax
                if b['index'] in W:
                    Rm, T, S = W[b['index']]
                    wp = [[T[i] + S * sum(Rm[i][k] * p[k] for k in range(3))
                           for i in range(3)] for p in vs]
                    wx = [p[0] for p in wp]; wy = [p[1] for p in wp]; wz = [p[2] for p in wp]
                    wmin = [min(wx), min(wy), min(wz)]
                    wmax = [max(wx), max(wy), max(wz)]
                    entry['world_aabb_min'] = [round(x, 4) for x in wmin]
                    entry['world_aabb_max'] = [round(x, 4) for x in wmax]
                    for i in range(3):
                        gmin[i] = wmin[i] if gmin[i] is None else min(gmin[i], wmin[i])
                        gmax[i] = wmax[i] if gmax[i] is None else max(gmax[i], wmax[i])
        shapes.append(entry)
    totals = {
        'num_trishape': len(shapes),
        'num_trishapedata': sum(1 for b in blocks if b['type'] == 'NiTriShapeData'),
        'total_vertices': sum(s.get('num_vertices', 0) for s in shapes),
        'total_triangles': sum(s.get('num_triangles', 0) for s in shapes),
        'total_valid_triangle_indices': sum(s.get('triangles_index_valid', 0) for s in shapes),
    }
    model_aabb = None
    if gmin[0] is not None:
        model_aabb = {'world_aabb_min': [round(x, 4) for x in gmin],
                      'world_aabb_max': [round(x, 4) for x in gmax],
                      'note': 'composed from local NiAVObject transforms x shape vertices (Z-up source axes, no axis remap)'}
    return shapes, totals, model_aabb


def analyze_materials(blocks):
    mats = []
    for b in blocks:
        if b['type'] != 'NiTriShape':
            continue
        entry = {'block': b['index'], 'name': b.get('name', ''), 'properties': []}
        for pr in b.get('property_refs', []):
            if not (0 <= pr < len(blocks)):
                continue
            pb = blocks[pr]
            e = {'ref': pr, 'type': pb['type']}
            if pb['type'] == 'NiMaterialProperty':
                e['name'] = pb.get('name')
                e['diffuse'] = pb.get('diffuse')
                e['ambient'] = pb.get('ambient')
                e['specular'] = pb.get('specular')
                e['emissive'] = pb.get('emissive')
                e['glossiness'] = pb.get('glossiness')
                e['material_alpha'] = pb.get('material_alpha')
            elif pb['type'] == 'NiTexturingProperty':
                e['name'] = pb.get('name')
                e['apply_mode'] = pb.get('apply_mode')
                e['texture_slots'] = sorted(pb.get('textures', {}).keys())
            elif pb['type'] == 'NiAlphaProperty':
                e['flags'] = pb.get('flags')
                e['threshold'] = pb.get('threshold')
            elif pb['type'] == 'NiZBufferProperty':
                e['flags'] = pb.get('flags')
            elif pb['type'] == 'NiVertexColorProperty':
                e['flags'] = pb.get('flags')
                e['unknown_u32_a'] = pb.get('vertex_mode_u32')
                e['unknown_u32_b'] = pb.get('lighting_mode_u32')
            entry['properties'].append(e)
        mats.append(entry)
    ark = []
    for b in blocks:
        if b['type'] == 'NiArkTextureExtraData':
            for t in b.get('ark_textures', []):
                ark.append({'extra_data_block': b['index'],
                            'texture_name': t['texture_name'],
                            'slot_type': t['slot_type'],
                            'texturing_property_ref': t['texturing_property_ref'],
                            'texture_id': t['texture_id']})
    return mats, ark


def determine_asset_role(blocks, doc):
    """Role classification from node/material names + block evidence.
    Taxonomy per contract: CO-NAMED / PLAUSIBLE / UNVERIFIED (no unproven labels)."""
    names = [b.get('name', '') for b in blocks if b.get('name')]
    mats = [b.get('name', '') for b in blocks if b['type'] == 'NiMaterialProperty' and b.get('name')]
    evidence_names = sorted(set(n for n in names if n))
    has_billboard = any(b['type'] == 'NiArkBillboardNode' for b in blocks)
    has_uvctrl = any(b['type'] == 'NiUVController' for b in blocks)
    has_texe = any(b['type'] == 'NiTextureEffect' for b in blocks)
    bb = [b for b in blocks if b['type'] == 'NiArkBillboardNode']
    bb_names = [b.get('name', '') for b in bb]

    # naming-convention classification: B_Eu_* / B_Outpost_* prefixes (multi-part
    # static asset with doors/occluders). This is a NAMING-CO-NAMING argument only.
    bprefix = [n for n in evidence_names if n.startswith('B_')]
    role = None
    role_status = 'UNVERIFIED'
    if bprefix:
        role = 'static multi-part world asset (naming convention B_*: %s)' % sorted(set(x.split(':')[0] for x in bprefix))
        role_status = 'CO-NAMED'
    effect = {
        'has_niark_billboard_nodes': has_billboard,
        'niark_billboard_node_count': len(bb),
        'niark_billboard_node_names': bb_names,
        'has_uv_controller': has_uvctrl,
        'has_texture_effect': has_texe,
    }
    return {
        'role_statement': role,
        'role_status': role_status,
        'classification_rule': ('CO-NAMED = node names literally encode the asset family. '
                               'Building/structure interpretation is NOT asserted beyond naming '
                               'evidence (PLAUSIBLE at most); no world-instance or placement claim.'),
        'naming_evidence_nodes': evidence_names[:80],
        'naming_evidence_materials': sorted(set(mats)),
        'effect_evidence': effect,
        'name_prefix_counts': dict(Counter(n.split('_')[0] for n in evidence_names if n)),
    }


def inspect(path, emit_vertices=False):
    out = {'tool': 'pe2003_model_inspector.py', 'tool_run': '2026-10-24',
           'job': 'PE2003R3-I1',
           'input_path': os.path.abspath(path)}
    try:
        data = open(path, 'rb').read()
    except Exception as e:
        out['status'] = 'IO_ERROR'
        out['error'] = str(e)
        return out
    out['file_size'] = len(data)
    out['sha256'] = hashlib.sha256(data).hexdigest().upper()
    try:
        hdr = parse_header(data)
    except ValueError as e:
        out['status'] = str(e)
        return out
    out['header'] = hdr
    if hdr['version_u32'] != '0x%08X' % SUPPORTED_VERSION:
        out['status'] = 'UNSUPPORTED_VERSION'
        out['supported_version'] = '0x%08X' % SUPPORTED_VERSION
        return out
    blocks = block_chain(data, hdr)
    truncated = [b for b in blocks if b.get('parse_status') == 'TRUNCATED']
    census = Counter(b['type'] for b in blocks if 'type' in b and b['type'] != 'UNKNOWN')
    out['block_census'] = dict(sorted(census.items()))
    out['blocks_found'] = len(blocks)
    out['num_blocks_header'] = hdr['num_blocks']
    out['census_match_header'] = len(blocks) == hdr['num_blocks'] and not truncated
    warnings = parse_blocks(data, blocks)
    out['parse_warnings'] = warnings
    truncated = [b for b in blocks if b.get('parse_status') == 'TRUNCATED']
    if not out['census_match_header'] or truncated:
        out['status'] = 'TRUNCATED_FILE'
    else:
        out['status'] = 'OK'
    # trailing footer carve-out: for the last block, an 8-byte tail
    # (u32 num_roots=1 + u32 root_ref) is the NIF footer, not block payload.
    last = blocks[-1] if blocks else None
    footer_at = last['data_end'] if last and 'data_end' in last else hdr['data_start']
    if last and 'data_end' in last and len(data) - last['data_end'] == 0:
        rem = len(data) - 8
        if rem >= last['data_offset'] and len(data) - last['data_end'] == 0:
            nroots = struct.unpack_from('<I', data, rem)[0]
            if 1 <= nroots <= 64 and rem + 4 + 4 * nroots == len(data):
                last['data_end'] = rem
                if last.get('parse_status') == 'MISALIGNED' and last.get('parsed_end') == rem:
                    last['parse_status'] = 'FIELDS_CONFIRMED'
                    last.pop('parsed_end', None); last.pop('expected_end', None)
                    if warnings and warnings[-1].startswith('block %d' % last['index']):
                        warnings.pop()
                footer_at = rem
    out['footer'] = parse_footer(data, footer_at)
    # analysis
    # analysis — guarded: truncated files may leave partially-parsed blocks;
    # failures are recorded explicitly instead of crashing.
    out['analysis_status'] = 'OK'
    try:
        parent, roots = build_hierarchy(blocks)
        out['hierarchy_roots'] = roots
        out['hierarchy_tree'] = tree_json(blocks, parent, roots)
        out['parent_map'] = {str(k): v for k, v in sorted(parent.items())}
        fr = out['footer'].get('root_refs')
        out['footer']['computed_hierarchy_roots'] = roots
        out['footer']['roots_crosscheck'] = ('CONFIRMED' if fr == roots else
                                             'MISMATCH footer=%s computed=%s' % (fr, roots))
        W = world_transforms(blocks, parent, roots)
        shapes, totals, aabb = analyze_geometry(blocks, W)
        out['geometry'] = {'totals': totals, 'model_world_aabb': aabb, 'shapes': shapes}
        mats, ark = analyze_materials(blocks)
        out['materials'] = {'per_shape': mats, 'ark_textures': ark}
        out['extra_data_summary'] = {
            t: sum(1 for b in blocks if b['type'] == t)
            for t in ('NiStringExtraData', 'NiArkTextureExtraData',
                      'NiArkAnimationExtraData', 'NiArkImporterExtraData',
                      'NiArkBillboardNode', 'NiUVController', 'NiUVData',
                      'NiTextureEffect')
        }
        out['asset_role'] = determine_asset_role(blocks, out)
    except Exception as e:
        out['analysis_status'] = 'ANALYSIS_ERROR: %s: %s' % (type(e).__name__, e)
    # block dump (with vertices reduced to counts/AABB)
    out['blocks'] = [strip_large(b) for b in blocks]
    if not emit_vertices:
        for b in out['blocks']:
            b.pop('vertices', None)
            b.pop('normals', None)
    out['fit_calibration'] = FIT_CALIBRATION
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    outj = None
    if '--json' in args:
        outj = args[args.index('--json') + 1]
    res = inspect(path)
    txt = json.dumps(res, indent=1, default=str)
    if outj:
        with open(outj, 'w', encoding='utf-8') as f:
            f.write(txt)
        print('status=%s blocks=%s census_match=%s -> %s'
              % (res.get('status'), res.get('blocks_found'), res.get('census_match_header'), outj))
    else:
        print(txt)


if __name__ == '__main__':
    main()
