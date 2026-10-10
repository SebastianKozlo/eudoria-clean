#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 PARSE NIF 10.1 — PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003 (Phase B).

Own decoder for 218757.nif (Gamebryo File Format, Version 10.1.0.0, 66 blocks),
implementing the project's NIF Rosetta canon:
  - framing: header line + version u32 + user version u32 + num_blocks u32 +
    num_block_types u16 + type table + type-index u16[] + num_groups u32(0) +
    blocks{GroupID u32(0) + payload} + TopObjects footer + EOF-exact
    (PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915/02_ANALYSIS/
    NIF_10_1_BASELINE_SPEC.md; per-block GroupID is the C-01 framing fact).
  - class layouts: closure-proven chains from the same spec
    (NiObjectNET/NiAVObject/NiNode/NiGeometry/NiGeometryData/NiTriShapeData/
    properties/NiExtraData v10 + MindArk extension matrix:
    NiArkTextureExtraData (count = (field2>>8)&0xFFFFFF),
    NiArkImporterExtraData (u32 + SS + 41B tail),
    NiArkShaderExtraData (u32 + SS),
    NiArkBillboardNode (NiNode + u16),
    NiArkViewportInfoExtraData / NiArkAnimationExtraData (variable ext ->
    byte-derived boundary via closure-constrained search, s06 method)).
  - boundary discipline: a variable-ext candidate is accepted ONLY if the
    whole file decodes to EOF-exact closure (backtracking search).

PAYLOAD DISCIPLINE: raw vertex/normal/uv/triangle arrays are kept IN MEMORY
ONLY (for bbox computation); the repo JSON stores per-block METADATA
(counts, transforms, names, refs, ext bounded hex windows) — no raw payload
arrays enter the repo.
Output: 01_RAW/NIF101_BLOCKMAP.json (metadata only) + console analysis.
"""
import json
import os
import struct
import sys
from collections import Counter

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 (s2 r1 copy; canonical s2 READ_ONLY in PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003)"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\02_PE_work\NIF101_BLOCKMAP_218757_R1.json"
NIF_PATH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\02_PE_payloads\218757.nif"

data = open(NIF_PATH, "rb").read()
N = len(data)
MAX_ATTEMPTS = 50000


class R:
    def __init__(s, d, p=0):
        s.d, s.p = d, p

    def u8(s):
        v = s.d[s.p]; s.p += 1; return v

    def i8(s):
        v = struct.unpack_from("<b", s.d, s.p)[0]; s.p += 1; return v

    def u16(s):
        v = struct.unpack_from("<H", s.d, s.p)[0]; s.p += 2; return v

    def i16(s):
        v = struct.unpack_from("<h", s.d, s.p)[0]; s.p += 2; return v

    def u32(s):
        v = struct.unpack_from("<I", s.d, s.p)[0]; s.p += 4; return v

    def i32(s):
        v = struct.unpack_from("<i", s.d, s.p)[0]; s.p += 4; return v

    def f32(s):
        v = struct.unpack_from("<f", s.d, s.p)[0]; s.p += 4; return v

    def raw(s, n):
        if s.p + n > N:
            raise ValueError("EOF at %d +%d" % (s.p, n))
        v = s.d[s.p:s.p + n]; s.p += n; return v

    def ss(s):
        ln = s.u32()
        if ln > (1 << 20):
            raise ValueError("SS too long %d" % ln)
        return s.raw(ln).decode("latin-1")

    def ref(s):
        v = s.i32()
        return None if v == -1 else v

    def v3(s):
        return [s.f32() for _ in range(3)]

    def m33(s):
        return [[s.f32() for _ in range(3)] for _ in range(3)]

    def c3(s):
        return [s.f32() for _ in range(3)]


def parse_header():
    nl = data.index(b"\x0A")
    line = data[:nl].decode("ascii")
    r = R(data, nl + 1)
    ver = r.u32()
    uv = r.u32()
    nb = r.u32()
    nbt = r.u16()
    types = [r.ss() for _ in range(nbt)]
    tidx = [r.u16() for _ in range(nb)]
    ng = r.u32()
    if ng != 0:
        raise SystemExit("nonzero groups unsupported")
    return {"header_line": line, "version_u32": "0x%08X" % ver,
            "user_version": uv, "num_blocks": nb, "num_block_types": nbt,
            "types": types, "type_index": tidx, "blocks_start": r.p}


HDR = parse_header()
TYPES = HDR["types"]
TIDX = HDR["type_index"]


def net(r, blk):
    blk["name"] = r.ss()
    n = r.u32()
    blk["extra_data_refs"] = [r.ref() for _ in range(n)]
    blk["controller_ref"] = r.ref()


def av(r, blk):
    blk["flags_u16"] = r.u16()
    blk["translation"] = r.v3()
    blk["rotation"] = r.m33()
    blk["scale"] = r.f32()
    n = r.u32()
    blk["property_refs"] = [r.ref() for _ in range(n)]
    blk["collision_object_ref"] = r.ref()


def node(r, blk):
    net(r, blk)
    av(r, blk)
    n = r.u32()
    blk["children"] = [r.ref() for _ in range(n)]
    ne = r.u32()
    blk["effects"] = [r.ref() for _ in range(ne)]


def texdesc(r):
    t = {"source_ref": r.ref(), "clamp_mode": r.u32(), "filter_mode": r.u32(),
         "uv_set": r.u32(), "ps2_l": r.i16(), "ps2_k": r.i16(),
         "has_texture_transform": r.u8()}
    if t["has_texture_transform"]:
        t["tt_translation"] = [r.f32(), r.f32()]
        t["tt_tiling"] = [r.f32(), r.f32()]
        t["tt_w_rotation"] = r.f32()
        t["tt_transform_type"] = r.u32()
        t["tt_center_offset"] = [r.f32(), r.f32()]
    return t


def geometry_data(r, blk):
    nv = r.u16()
    blk["num_vertices"] = nv
    blk["keep_flags_u8"] = r.u8()
    blk["compress_flags_u8"] = r.u8()
    hv = r.u8()
    blk["has_vertices"] = bool(hv)
    blk["_vertices"] = [r.v3() for _ in range(nv)] if hv else []
    blk["num_uv_sets_u8"] = r.u8()
    blk["extra_vectors_flags_u8"] = r.u8()
    hn = r.u8()
    blk["has_normals"] = bool(hn)
    if hn:
        blk["_normals"] = [r.v3() for _ in range(nv)]
        if blk["extra_vectors_flags_u8"] & 16:
            blk["_tangents"] = [r.v3() for _ in range(nv)]
            blk["_bitangents"] = [r.v3() for _ in range(nv)]
    blk["bound_center"] = r.v3()
    blk["bound_radius"] = r.f32()
    hvc = r.u8()
    blk["has_vertex_colors"] = bool(hvc)
    if hvc:
        blk["_colors"] = [[r.f32() for _ in range(4)] for _ in range(nv)]
    nuv = blk["num_uv_sets_u8"] & 63
    blk["uv_set_count"] = nuv
    blk["_uv_sets"] = [[[r.f32(), r.f32()] for _ in range(nv)] for _ in range(nuv)]
    blk["consistency_flags_u16"] = r.u16()


# ---- variable-ext Ark types handled by closure-constrained search ----
EXT_SEARCH = {"NiArkViewportInfoExtraData", "NiArkAnimationExtraData"}


def decode_standard(r, tname, blk):
    """Decode one block payload (after GroupID) for known standard types.
    Returns dict. Raises ValueError on desync/unknown type."""
    if tname in ("NiNode",):
        node(r, blk)
    elif tname in ("NiBillboardNode", "NiArkBillboardNode"):
        node(r, blk)
        blk["billboard_mode_u16"] = r.u16()
    elif tname == "NiSortAdjustNode":
        node(r, blk)
        blk["sorting_mode_u32"] = r.u32()
        blk["unknown_int2_i32"] = r.i32()
    elif tname == "NiTriShape":
        net(r, blk)
        av(r, blk)
        blk["data_ref"] = r.ref()
        blk["skin_instance_ref"] = r.ref()
        hs = r.u8()
        blk["has_shader_u8"] = hs
        if hs:
            blk["shader_name"] = r.ss()
            blk["shader_unknown_int"] = r.i32()
    elif tname == "NiTriShapeData":
        geometry_data(r, blk)
        nt = r.u16()
        blk["num_triangles"] = nt
        blk["num_triangle_points"] = r.u32()
        ht = r.u8()
        blk["has_triangles_u8"] = ht
        if ht:
            blk["_triangles"] = [[r.u16(), r.u16(), r.u16()] for _ in range(nt)]
        mg = r.u16()
        blk["num_match_groups"] = mg
        blk["_match_groups"] = []
        for _ in range(mg):
            gv = r.u16()
            blk["_match_groups"].append([r.u16() for _ in range(gv)])
    elif tname == "NiMaterialProperty":
        net(r, blk)
        blk["ambient"] = r.c3(); blk["diffuse"] = r.c3()
        blk["specular"] = r.c3(); blk["emissive"] = r.c3()
        blk["glossiness"] = r.f32(); blk["alpha"] = r.f32()
    elif tname == "NiTexturingProperty":
        # HIST 0.7.1.1 field order (BASELINE_TYPE_TABLE.csv rows 13-47):
        # Apply Mode u32; Texture Count u32; Has+TexDesc pairs Base, Dark,
        # Detail, Gloss, Glow, Bump, Decal0; Bump Luma Scale/Offset/Matrix22
        # (16 B) ONLY if Has Bump Map Texture; Decal1/2/3 only when
        # Texture Count >= 8/9/10; Num Shader Textures; ShaderTexDescs.
        net(r, blk)
        blk["apply_mode_u32"] = r.u32()
        tc = r.u32()
        blk["texture_count_u32"] = tc
        slot_defs = [("Base", True), ("Dark", True), ("Detail", True),
                     ("Gloss", True), ("Glow", True), ("Bump", True),
                     ("Decal0", True), ("Decal1", tc >= 8),
                     ("Decal2", tc >= 9), ("Decal3", tc >= 10)]
        slots = {}
        order = []
        for name, present in slot_defs:
            if not present:
                continue
            has = r.u8()
            if has:
                td = texdesc(r)
                td["slot_name"] = name
                slots[name] = td
                order.append(name)
        blk["texture_slots"] = slots
        blk["active_slots"] = order
        if slots.get("Bump") is not None:
            blk["bump_luma_scale"] = r.f32()
            blk["bump_luma_offset"] = r.f32()
            blk["bump_map_matrix22_4f32"] = [r.f32() for _ in range(4)]
        nst = r.u32()
        blk["num_shader_textures"] = nst
        if nst:
            blk["shader_texdescs"] = [texdesc(r) for _ in range(nst)]
    elif tname == "NiZBufferProperty":
        net(r, blk)
        blk["flags_u16"] = r.u16()
        blk["function_u32"] = r.u32()
    elif tname == "NiAlphaProperty":
        net(r, blk)
        blk["flags_u16"] = r.u16()
        blk["threshold_u8"] = r.u8()
    elif tname == "NiStencilProperty":
        net(r, blk)
        blk["stencil_enabled_u8"] = r.u8()
        blk["stencil_function_u32"] = r.u32()
        blk["stencil_ref_u32"] = r.u32()
        blk["stencil_mask_u32"] = r.u32()
        blk["fail_action_u32"] = r.u32()
        blk["zfail_action_u32"] = r.u32()
        blk["pass_action_u32"] = r.u32()
        blk["draw_mode_u32"] = r.u32()
    elif tname == "NiVertexColorProperty":
        net(r, blk)
        blk["flags_u16"] = r.u16()
        blk["vertex_mode_u32"] = r.u32()
        blk["lighting_mode_u32"] = r.u32()
    elif tname in ("NiSpecularProperty", "NiShadeProperty", "NiDitherProperty"):
        net(r, blk)
        blk["flags_u16"] = r.u16()
    elif tname == "NiFogProperty":
        net(r, blk)
        blk["flags_u16"] = r.u16()
        blk["fog_density_f32"] = r.f32()
        blk["fog_color_c3"] = r.c3()
    elif tname == "NiStringExtraData":
        # NiExtraData v10 base = NAME ONLY (baseline spec; no extra list /
        # controller — those are NiObjectNET fields, absent in NiExtraData)
        blk["name"] = r.ss()
        blk["string_data"] = r.ss()
    elif tname == "NiIntegerExtraData":
        blk["name"] = r.ss()
        blk["integer_data"] = r.u32()
    elif tname == "NiBooleanExtraData":
        blk["name"] = r.ss()
        blk["boolean_data"] = r.u8()
    elif tname == "NiSourceTexture":
        net(r, blk)
        ue = r.u8()
        blk["use_external_u8"] = ue
        blk["file_name"] = r.ss()
        blk["link_ref"] = r.ref()
        blk["pixel_layout_u32"] = r.u32()
        blk["use_mipmaps_u32"] = r.u32()
        blk["alpha_format_u32"] = r.u32()
        blk["is_static_u8"] = r.u8()
    elif tname == "NiArkTextureExtraData":
        blk["name"] = r.ss()
        blk["numfield_u32"] = r.u32()
        blk["field1_u32"] = r.u32()
        blk["field2_u32"] = r.u32()
        blk["pad_u8"] = r.u8()
        cnt = (blk["field2_u32"] >> 8) & 0xFFFFFF
        blk["entry_count_formula_field2shift8"] = cnt
        entries = []
        for _ in range(cnt):
            e = {"texture_name": r.ss(), "f1_i32": r.i32(), "f2_i32": r.i32(),
                 "texturing_property_ref": r.ref()}
            b9 = r.raw(9)
            e["bytes9_hex"] = b9.hex()
            e["bytes9_bnt2id_u32le1_priorclaim"] = struct.unpack_from("<I", b9, 1)[0]
            e["bytes9_u8_0"] = b9[0]; e["bytes9_u8_4"] = b9[4]; e["bytes9_u8_8"] = b9[8]
            entries.append(e)
        blk["ark_texture_entries"] = entries
    elif tname == "NiArkImporterExtraData":
        blk["name"] = r.ss()
        blk["int1_u32"] = r.u32()
        blk["version_string"] = r.ss()
        tail = r.raw(41)
        blk["tail41_hex"] = tail.hex()
        blk["tail41_header_u32s"] = list(struct.unpack_from("<III", tail, 0))
        blk["tail41_header_u8"] = tail[12]
        blk["tail41_bounds_7f32_priorclaim"] = [struct.unpack_from("<f", tail, 13 + 4 * k)[0] for k in range(7)]
    elif tname == "NiArkShaderExtraData":
        blk["name"] = r.ss()
        blk["int_u32"] = r.u32()
        blk["shader_config_string"] = r.ss()
    elif tname == "NiCollisionData":
        blk["target_ref"] = r.ref()
        blk["propagation_mode_u32"] = r.u32()
        blk["collision_mode_u32"] = r.u32()
        ua = r.u8()
        blk["use_abv_u8"] = ua
        if ua:
            ct = r.u32()
            bv = {"collision_type_u32": ct}
            if ct == 0:
                bv["center"] = r.v3(); bv["radius"] = r.f32()
            elif ct == 1:
                bv["center"] = r.v3(); bv["axis0"] = r.v3(); bv["axis1"] = r.v3()
                bv["axis2"] = r.v3(); bv["half_dims"] = r.v3()
            elif ct == 2:
                bv["a"] = r.v3(); bv["b"] = r.v3(); bv["radius"] = r.f32()
            else:
                raise ValueError("BV type %d unhandled" % ct)
            blk["bounding_volume"] = bv
    elif tname in ("NiPointLight", "NiSpotLight", "NiDirectionalLight", "NiAmbientLight"):
        net(r, blk)
        av(r, blk)
        na = r.u32()
        blk["affected_node_refs"] = [r.ref() for _ in range(na)]
        blk["dimmer_f32"] = r.f32()
        blk["ambient_c3"] = r.c3(); blk["diffuse_c3"] = r.c3(); blk["specular_c3"] = r.c3()
        if tname in ("NiPointLight", "NiSpotLight"):
            blk["attenuation_const"] = r.f32()
            blk["attenuation_linear"] = r.f32()
            blk["attenuation_quadratic"] = r.f32()
        if tname == "NiSpotLight":
            blk["cutoff_angle_f32"] = r.f32()
            blk["exponent_f32"] = r.f32()
    elif tname == "NiTextureEffect":
        net(r, blk)
        av(r, blk)
        na = r.u32()
        blk["affected_node_refs"] = [r.ref() for _ in range(na)]
        blk["model_projection_matrix"] = r.m33()
        blk["model_projection_translation"] = r.v3()
        blk["texture_filtering_u32"] = r.u32()
        blk["texture_clamping_u32"] = r.u32()
        blk["texture_type_u32"] = r.u32()
        blk["coord_generation_type_u32"] = r.u32()
        blk["source_texture_ref"] = r.ref()
        blk["clipping_plane_u8"] = r.u8()
        blk["unknown_vector"] = r.v3()
        blk["unknown_float"] = r.f32()
        blk["ps2_l"] = r.i16()
        blk["ps2_k"] = r.i16()
    else:
        raise ValueError("unhandled type %r" % tname)
    return blk


def ext_candidates(start):
    """Boundary candidates for a variable-ext Ark block end (s06 method,
    simplified): positions where u32==0 (next GroupID) followed by a
    plausible NiObjectNET name, plus footer positions."""
    cands = []
    window = min(N, start + 8192)
    pos = start
    scored = []
    while pos < window:
        if pos + 8 <= N:
            g, = struct.unpack_from("<I", data, pos)
            if g == 0:
                ln, = struct.unpack_from("<I", data, pos + 4)
                if ln <= 256 and pos + 8 + ln <= N:
                    nm = data[pos + 8:pos + 8 + ln]
                    if ln == 0:
                        scored.append((1, pos))
                    else:
                        pr = sum(1 for b in nm if 32 <= b < 127 or b == 0) / ln
                        if pr >= 0.8:
                            rank = 0 if 4 <= ln <= 64 else 1
                            scored.append((rank, pos))
        pos += 1
    # footer positions: u32 ntop with 0<=ntop<=num_blocks and p+4+4*ntop==N
    nb = HDR["num_blocks"]
    for p in range(start, min(start + 8192, N - 3)):
        c, = struct.unpack_from("<I", data, p)
        if 0 <= c <= nb and p + 4 + 4 * c == N:
            scored.append((0, p))
    scored.sort()
    seen = set()
    for rank, c in scored[:1024]:
        if c in seen:
            continue
        seen.add(c)
        cands.append(c)
    return cands


class Parse:
    def __init__(self):
        self.blocks = [None] * HDR["num_blocks"]
        self.attempts = 0
        self.decisions = []

    def decode_from(self, i, r):
        """Decode blocks i.. with backtracking over EXT_SEARCH blocks.
        Returns True iff full closure (all blocks + footer + EOF-exact)."""
        if i >= HDR["num_blocks"]:
            ntop = r.u32()
            tops = [r.i32() for _ in range(ntop)]
            if r.p != N:
                return False
            self.top_objects = tops
            self.num_top = ntop
            return True
        self.attempts += 1
        if self.attempts > MAX_ATTEMPTS:
            return False
        tname = TYPES[TIDX[i]]
        start = r.p
        gid = r.u32()
        if gid != 0:
            return False
        blk = {"index": i, "type": tname, "group_id": gid, "start": start}
        if tname in EXT_SEARCH:
            name_ln = r.u32()
            if name_ln > 256:
                return False
            blk["name"] = r.raw(name_ln).decode("latin-1")
            ext_start = r.p
            for cand in ext_candidates(ext_start):
                save = r.p
                if cand < ext_start or cand > N:
                    continue
                ext = data[ext_start:cand]
                blk2 = dict(blk)
                blk2["ext_len"] = len(ext)
                blk2["ext_hex"] = ext.hex()
                blk2["end"] = cand
                self.blocks[i] = blk2
                self.decisions.append((i, tname, ext_start, cand))
                r.p = cand
                if self.decode_from(i + 1, r):
                    return True
                self.blocks[i] = None
                self.decisions.pop()
                r.p = save
            return False
        else:
            try:
                decode_standard(r, tname, blk)
            except (ValueError, struct.error, IndexError):
                # A wrong ext-boundary upstream (or a desync here) must
                # FAIL THIS CANDIDATE so the search backtracks — NOT abort.
                return False
            blk["end"] = r.p
            self.blocks[i] = blk
            if self.decode_from(i + 1, r):
                return True
            self.blocks[i] = None
            return False


P = Parse()
r = R(data, HDR["blocks_start"])
ok = P.decode_from(0, r)
if not ok:
    raise SystemExit("CLOSURE_FAIL: no candidate set closed the file")
blocks = P.blocks

# ---------- analysis ----------
census = Counter(b["type"] for b in blocks)


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mat_vec(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]


def compose(parent, local):
    Rp, Tp, Sp = parent
    Rl, Tl, Sl = local
    return (mat_mul(Rp, Rl),
            [mat_vec(Rp, [Tl[i] * Sp for i in range(3)])[i] + Tp[i] for i in range(3)],
            Sp * Sl)


IDENT = ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 0], 1.0)

parents = {}
for b in blocks:
    for ch in b.get("children", []) or []:
        if ch is not None:
            parents[ch] = b["index"]

world = {}


def compute_world(i, parent_w):
    b = blocks[i]
    Rl = b.get("rotation", IDENT[0])
    Tl = b.get("translation", IDENT[1])
    Sl = b.get("scale", 1.0)
    w = compose(parent_w, (Rl, Tl, Sl))
    world[i] = w
    for ch in b.get("children", []) or []:
        if ch is not None:
            compute_world(ch, w)


roots = [i for i in range(len(blocks)) if i not in parents]
for rt in roots:
    compute_world(rt, IDENT)

# mesh stats + global bbox from world-composed vertices
mesh_stats = []
allmin = [1e30] * 3
allmax = [-1e30] * 3
rawmin = [1e30] * 3
rawmax = [-1e30] * 3
total_verts = 0
total_tris = 0
for b in blocks:
    if b["type"] == "NiTriShapeData":
        for v in b.get("_vertices", []):
            for k in range(3):
                rawmin[k] = min(rawmin[k], v[k])
                rawmax[k] = max(rawmax[k], v[k])
for b in blocks:
    if b["type"] == "NiTriShape":
        db = blocks[b["data_ref"]]
        verts = db.get("_vertices", [])
        Rm, Tm, Sm = world[b["index"]]
        mn = [1e30] * 3
        mx = [-1e30] * 3
        for v in verts:
            tv = [mat_vec(Rm, [v[i] * Sm for i in range(3)])[i] + Tm[i] for i in range(3)]
            for k in range(3):
                mn[k] = min(mn[k], tv[k])
                mx[k] = max(mx[k], tv[k])
                allmin[k] = min(allmin[k], tv[k])
                allmax[k] = max(allmax[k], tv[k])
        mesh_stats.append({
            "index": b["index"], "name": b.get("name"),
            "data_ref": b["data_ref"], "parent": parents.get(b["index"]),
            "num_vertices": db.get("num_vertices", 0),
            "num_triangles": db.get("num_triangles", 0),
            "uv_set_count": db.get("uv_set_count", 0),
            "local_T": b.get("translation"), "local_scale": b.get("scale"),
            "world_T": world[b["index"]][1], "world_scale": world[b["index"]][2],
            "bbox_local_min": mn if verts else None,
            "bbox_local_max": mx if verts else None,
            "property_refs": [p for p in (b.get("property_refs") or []) if p is not None],
            "extra_data_refs": [p for p in (b.get("extra_data_refs") or []) if p is not None],
        })
        total_verts += db.get("num_vertices", 0)
        total_tris += db.get("num_triangles", 0)

# texture references
texture_refs = []
for b in blocks:
    if b["type"] == "NiTexturingProperty":
        for slot_name, slot in (b.get("texture_slots") or {}).items():
            if slot.get("source_ref") is not None:
                src = blocks[slot["source_ref"]]
                fname = src.get("file_name") if src["type"] == "NiSourceTexture" else None
                texture_refs.append({
                    "texturing_property_block": b["index"], "slot": slot_name,
                    "source_texture_block": slot["source_ref"],
                    "source_block_type": src["type"],
                    "clamp": slot.get("clamp_mode"), "filter": slot.get("filter_mode"),
                    "uv_set": slot.get("uv_set"),
                    "has_texture_transform": slot.get("has_texture_transform"),
                    "file_name": fname})
    if b["type"] == "NiArkTextureExtraData":
        for e in b.get("ark_texture_entries", []):
            texture_refs.append({
                "ark_texture_block": b["index"], "ark_entry_name": e["texture_name"],
                "texturing_property_ref": e["texturing_property_ref"],
                "f1_i32": e["f1_i32"], "f2_i32": e["f2_i32"],
                "bnt2_id_priorclaim": e["bytes9_bnt2id_u32le1_priorclaim"],
                "bytes9_hex": e["bytes9_hex"]})

# node tree dump (names!)
tree_lines = []


def ptree(i, d=0):
    b = blocks[i]
    extra = ""
    if b["type"] == "NiTriShape":
        db = blocks[b["data_ref"]]
        extra = " -> data=%d verts=%d tris=%d" % (b["data_ref"], db.get("num_vertices", 0), db.get("num_triangles", 0))
    wT = world[i][1] if i in world else None
    wTs = (" worldT=[%s]" % ", ".join("%.2f" % x for x in wT)) if wT else ""
    tree_lines.append("  " * d + "[%d] %s %r T=%s S=%s%s%s" % (
        b["index"], b["type"], b.get("name", ""),
        ["%.2f" % x for x in b.get("translation", [])] if b.get("translation") is not None else None,
        b.get("scale"), wTs, extra))
    for ch in b.get("children", []) or []:
        if ch is not None:
            ptree(ch, d + 1)


for rt in roots:
    ptree(rt)

# strip raw arrays for repo output (payload discipline)
out_blocks = []
for b in blocks:
    ob = {k: v for k, v in b.items() if not k.startswith("_")}
    out_blocks.append(ob)

result = {
    "run_id": RUN_ID, "stage": "S2_parse_nif_101_phase_B",
    "source_path": NIF_PATH,
    "nif_header": HDR,
    "closure": {"ok": True, "num_blocks_decoded": len(blocks),
                "eof_exact": True, "top_objects": P.top_objects,
                "num_top_objects": P.num_top,
                "ext_search_decisions": [
                    {"block": i, "type": t, "ext_start": es, "ext_end": ee,
                     "ext_len": ee - es} for (i, t, es, ee) in P.decisions]},
    "block_census": dict(sorted(census.items(), key=lambda kv: -kv[1])),
    "roots": roots,
    "global_bbox_world": {"min": allmin, "max": allmax,
                          "extents": [allmax[k] - allmin[k] for k in range(3)]},
    "raw_vertex_extremes_untransformed": {"min": rawmin, "max": rawmax,
                                          "extents": [rawmax[k] - rawmin[k] for k in range(3)],
                                          "note": "union of RAW vertex arrays across all NiTriShapeData (no node transforms applied) — the quantity the NiArkImporterExtraData 41B tail floats correspond to per the 296445-errata prior claim"},
    "totals": {"vertices": total_verts, "triangles": total_tris,
               "meshes": len(mesh_stats)},
    "mesh_stats": mesh_stats,
    "texture_refs": texture_refs,
    "node_tree_dump": tree_lines,
    "blocks_metadata_only": out_blocks,
    "payload_discipline": "raw vertex/normal/uv/triangle arrays stripped; kept in-memory for bbox only",
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1)

print("S2 CLOSURE_OK blocks=%d types=%d attempts=%d" % (len(blocks), HDR["num_block_types"], P.attempts))
print("block census:", json.dumps(result["block_census"]))
print("top objects:", P.top_objects, "roots:", roots)
print("GLOBAL BBOX min:", ["%.3f" % x for x in allmin])
print("GLOBAL BBOX max:", ["%.3f" % x for x in allmax])
print("extents:", ["%.3f" % x for x in result["global_bbox_world"]["extents"]])
print("totals: verts=%d tris=%d meshes=%d" % (total_verts, total_tris, len(mesh_stats)))
print("\n--- NODE TREE ---")
print("\n".join(tree_lines))
print("\n--- TEXTURE REFS ---")
for t in texture_refs:
    print(json.dumps(t))
print("\n--- EXTRA DATA STRINGS ---")
for b in blocks:
    if b["type"] == "NiStringExtraData":
        print("block %d NiStringExtraData %r: %r" % (b["index"], b.get("name"), b.get("string_data")))
    if b["type"] == "NiArkShaderExtraData":
        print("block %d NiArkShaderExtraData %r: int=%d cfg=%r" % (b["index"], b.get("name"), b.get("int_u32"), b.get("shader_config_string")))
    if b["type"] == "NiArkImporterExtraData":
        print("block %d NiArkImporterExtraData %r: int1=%d ver=%r tail_bounds=%r" % (b["index"], b.get("name"), b.get("int1_u32"), b.get("version_string"), b.get("tail41_bounds_7f32_priorclaim")))
    if b["type"] == "NiArkAnimationExtraData":
        print("block %d NiArkAnimationExtraData %r: ext_len=%d ext_head_hex=%s" % (b["index"], b.get("name"), b.get("ext_len"), b.get("ext_hex", "")[:64]))
    if b["type"] == "NiArkViewportInfoExtraData":
        print("block %d NiArkViewportInfoExtraData %r: ext_len=%d ext_head_hex=%s" % (b["index"], b.get("name"), b.get("ext_len"), b.get("ext_hex", "")[:64]))
print("\nout ->", OUT)
