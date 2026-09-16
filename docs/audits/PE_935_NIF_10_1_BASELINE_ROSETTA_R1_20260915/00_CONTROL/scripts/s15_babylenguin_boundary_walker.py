#!/usr/bin/env python3
# s15_babylenguin_boundary_walker.py -- C1 INDEPENDENT BABYLENGUIN BYTE
# REPRODUCTION for PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916.
#
# SUPERSEDES TOOLING BEHAVIOR of s06_world_slice_validator.py for the
# NiSourceTexture duplicate "File Name" case (s06 dedups schema fields
# by bare display name and loses the "Use External == 0" File Name
# alternative). DOES NOT REWRITE HISTORICAL HOLDOUT evidence
# (s04/s06 bytes unchanged).
#
# METHOD (anti-circular, contract C1):
# - Fresh minimal byte walker. Uses ONLY the physical bytes of
#   BABYLENGUIN.NIF (SRC-08) and field sequences HAND-TRANSCRIBED from
#   the pinned Gamebryo 1.2 ENGINE SOURCE (SRC-06): NiStream.cpp
#   LoadHeader/LoadRTTI/LoadObjectGroups/LoadTopLevelObjects,
#   NiObject.cpp LoadBinary (per-block GroupID), NiObjectNET.cpp,
#   NiAVObject.cpp, NiNode.cpp, NiProperty.cpp, NiGeometry.cpp,
#   NiShader.cpp (Win32), NiZBufferProperty.cpp/.h,
#   NiVertexColorProperty.cpp/.h, NiTexturingProperty.cpp/.h
#   (Map/BumpMap/ShaderMap/NiTextureTransform), NiSourceTexture.cpp.
# - Does NOT use s04/s06 schema machinery, external audit scripts,
#   external report offsets, NifSkope, or any display-name dedup.
# - C1A: Has-Bump-Map-Texture VALUE condition implemented exactly as
#   the engine (BumpMap extras only when the slot bHasMap byte is
#   nonzero; VERSION CONDITION != VALUE CONDITION).
# - Negative controls (addendum E): walker must demonstrably FAIL on
#   (a) truncated input, (b) corrupted string length, (c) wrong version.
#
# Outputs: console trace + 01_RAW/BABYLENGUIN_BOUNDARY_REDERIVATION.csv
import csv
import hashlib
import os
import struct
import sys

PATH = r"D:\gamebyroengine\extracted\gb112_known_good\BABYLENGUIN.NIF"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(os.path.dirname(HERE), "..", "01_RAW",
                       "BABYLENGUIN_BOUNDARY_REDERIVATION.csv")

V = 0x0A010000
GROUPID_APPLIES = 0x05000006 <= V < 0x0A010072
BUMP_INDEX = 5  # NiTexturingProperty.h enum BASE..GLOW,BUMP

trace = []


class WalkFail(Exception):
    pass


class Cur:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def rec(self, field, fn, n, owner, method):
        start = self.pos
        if start + n > len(self.data):
            raise WalkFail("EOF at %s pos=%d need=%d" % (field, start, n))
        raw = self.data[start:start + n]
        val = fn(raw)
        self.pos += n
        trace.append({
            "field": field, "offset": start, "length": n,
            "hex": raw.hex(), "decoded_value": repr(val),
            "semantic_owner": owner, "source_method": method})
        return val

    def u8(self, field, owner, method):
        return self.rec(field, lambda b: b[0], 1, owner, method)

    def u16(self, field, owner, method):
        return self.rec(field, lambda b: struct.unpack("<H", b)[0], 2,
                        owner, method)

    def u32(self, field, owner, method):
        return self.rec(field, lambda b: struct.unpack("<I", b)[0], 4,
                        owner, method)

    def s16(self, field, owner, method):
        return self.rec(field, lambda b: struct.unpack("<h", b)[0], 2,
                        owner, method)

    def f32(self, field, owner, method):
        return self.rec(field, lambda b: struct.unpack("<f", b)[0], 4,
                        owner, method)

    def cstr(self, field, owner, method):
        # engine LoadCString: u32 length + raw bytes, no NUL
        ln = self.u32(field + ".len", owner, method + " LoadCString-len")
        if ln > (1 << 24):
            raise WalkFail("implausible string length %d at %s"
                           % (ln, field))
        rawb = self.rec(field + ".bytes",
                        lambda b: b.decode("latin-1"), ln, owner,
                        method + " LoadCString-bytes")
        return rawb, start if False else self.pos - ln


def walk_header(cur):
    # NiStream::LoadHeader L303-360 + LoadRTTI L412-449 +
    # LoadObjectGroups L470-487
    nl = cur.data.index(b"\n", cur.pos)
    line = cur.data[cur.pos:nl + 1]
    trace.append({"field": "header.header_string", "offset": cur.pos,
                  "length": nl + 1 - cur.pos,
                  "hex": line[:40].hex(),
                  "decoded_value": line.decode("ascii"),
                  "semantic_owner": "header",
                  "source_method": "engine:NiStream::LoadHeader GetLine"})
    cur.pos = nl + 1
    ver = cur.u32("header.version", "header",
                  "engine:NiStream::LoadHeader")
    if ver != V:
        raise WalkFail("not 10.1.0.0: 0x%08X" % ver)
    cur.u32("header.user_version", "header",
            "engine:NiStream::LoadHeader (v>=10.0.1.8)")
    nb = cur.u32("header.num_blocks", "header",
                 "engine:NiStream::LoadHeader")
    nbt = cur.u16("header.num_block_types", "header",
                  "engine:NiStream::LoadRTTI L414-415")
    names = []
    for i in range(nbt):
        nm, _ = cur.cstr("header.block_type[%d]" % i, "header",
                         "engine:NiStream::LoadRTTIString")
        names.append(nm)
    idx = []
    for i in range(nb):
        idx.append(cur.u16("header.block_type_index[%d]" % i, "header",
                           "engine:NiStream::LoadRTTI L436-444"))
    ng = cur.u32("header.num_groups", "header",
                 "engine:NiStream::LoadObjectGroups L473-474")
    for g in range(ng):
        cur.u32("header.group_size[%d]" % g, "header",
                "engine:NiStream::LoadObjectGroups L479-485")
    return {"num_blocks": nb, "types": names, "idx": idx}


def gid(cur, i, tname):
    # NiObject::LoadBinary L134-143: per-block GroupID before fields
    return cur.u32("block%d.%s.GroupID" % (i, tname),
                   "block%d(%s)" % (i, tname),
                   "engine:NiObject::LoadBinary")


def objectnet(cur, i, tname):
    # NiObjectNET::LoadBinary: LoadCString(name), extra list, controller
    cur.cstr("block%d.%s.Name" % (i, tname),
             "block%d(%s)" % (i, tname),
             "engine:NiObjectNET::LoadBinary")
    n = cur.u32("block%d.%s.NumExtraData" % (i, tname),
                "block%d(%s)" % (i, tname),
                "engine:NiObjectNET::ReadMultipleLinkIDs")
    if n > 4096:
        raise WalkFail("implausible extra count %d" % n)
    for k in range(n):
        cur.u32("block%d.%s.ExtraData[%d]" % (i, tname, k),
                "block%d(%s)" % (i, tname),
                "engine:NiObjectNET::ReadMultipleLinkIDs")
    cur.u32("block%d.%s.Controller" % (i, tname),
            "block%d(%s)" % (i, tname),
            "engine:NiObjectNET::ReadLinkID")


def avobject(cur, i, tname):
    # NiAVObject::LoadBinary @10.1: flags u16, translate, rotate,
    # scale, property list, collision ref
    objectnet(cur, i, tname)
    o = "block%d(%s)" % (i, tname)
    cur.u16("block%d.%s.Flags" % (i, tname), o,
            "engine:NiAVObject::LoadBinary m_uFlags u16")
    for f in ("X", "Y", "Z"):
        cur.f32("block%d.%s.Translation.%s" % (i, tname, f), o,
                "engine:NiAVObject::LoadBinary m_kLocal.m_Translate")
    for r in range(3):
        for c in range(3):
            cur.f32("block%d.%s.Rotation[%d][%d]" % (i, tname, r, c), o,
                    "engine:NiAVObject::LoadBinary m_kLocal.m_Rotate")
    cur.f32("block%d.%s.Scale" % (i, tname), o,
            "engine:NiAVObject::LoadBinary m_kLocal.m_fScale")
    np_ = cur.u32("block%d.%s.NumProperties" % (i, tname), o,
                  "engine:NiAVObject::LoadBinary ReadMultipleLinkIDs")
    if np_ > 4096:
        raise WalkFail("implausible property count %d" % np_)
    for k in range(np_):
        cur.u32("block%d.%s.Properties[%d]" % (i, tname, k), o,
                "engine:NiAVObject::LoadBinary ReadMultipleLinkIDs")
    cur.u32("block%d.%s.CollisionObject" % (i, tname), o,
            "engine:NiAVObject::LoadBinary ReadLinkID")


def read_map(cur, i, slot, kind):
    # Map::LoadBinary L838-867; BumpMap adds 6 floats (L931-941)
    o = "block%d(NiTexturingProperty).%s_map[%d]" % (i, kind, slot)
    p = "block%d.NiTexturingProperty.%s_map[%d]" % (i, kind, slot)
    cur.u32(p + ".Source", o, "engine:Map::LoadBinary ReadLinkID")
    cur.u32(p + ".ClampMode", o, "engine:Map::LoadBinary m_eClamp")
    cur.u32(p + ".FilterMode", o, "engine:Map::LoadBinary m_eFilter")
    cur.u32(p + ".TexCoord", o, "engine:Map::LoadBinary m_uiTexCoord")
    cur.s16(p + ".L", o, "engine:Map::LoadBinary m_sL")
    cur.s16(p + ".K", o, "engine:Map::LoadBinary m_sK")
    bt = cur.u8(p + ".HasTextureTransform", o,
                "engine:Map::LoadBinary bTextureTransform (v>=10.0.1.10)")
    if bt == 1:
        for f in ("U", "V"):
            cur.f32(p + ".Transform.Translation.%s" % f, o,
                    "engine:NiTextureTransform::LoadBinary m_kTranslate")
        for f in ("U", "V"):
            cur.f32(p + ".Transform.Scale.%s" % f, o,
                    "engine:NiTextureTransform::LoadBinary m_kScale")
        cur.f32(p + ".Transform.Rotation", o,
                "engine:NiTextureTransform::LoadBinary m_fRotate")
        cur.u32(p + ".Transform.Method", o,
                "engine:NiTextureTransform::LoadBinary m_eMethod")
        for f in ("U", "V"):
            cur.f32(p + ".Transform.Center.%s" % f, o,
                    "engine:NiTextureTransform::LoadBinary m_kCenter")
    if kind == "Bump":
        cur.f32(p + ".LumaScale", o, "engine:BumpMap::LoadBinary")
        cur.f32(p + ".LumaOffset", o, "engine:BumpMap::LoadBinary")
        for m in ("00", "01", "10", "11"):
            cur.f32(p + ".BumpMat%s" % m, o, "engine:BumpMap::LoadBinary")


def nitexturingproperty(cur, i):
    # NiTexturingProperty::LoadBinary L255-346: NiProperty chain,
    # ApplyMode, TextureCount, per-slot bHasMap + Map
    # (slot==BUMP_INDEX -> BumpMap), then shader maps.
    objectnet(cur, i, "NiTexturingProperty")
    o = "block%d(NiTexturingProperty)" % i
    p = "block%d.NiTexturingProperty" % i
    cur.u32(p + ".ApplyMode", o,
            "engine:NiTexturingProperty::LoadBinary m_eApply")
    cnt = cur.u32(p + ".TextureCount", o,
                  "engine:NiTexturingProperty::LoadBinary uiListSize")
    if cnt > 64:
        raise WalkFail("implausible texture count %d" % cnt)
    for slot in range(cnt):
        has = cur.u8("%s.slot[%d].HasMap" % (p, slot), o,
                     "engine:NiTexturingProperty::LoadBinary bHasMap")
        if has == 1:
            if slot == BUMP_INDEX:
                read_map(cur, i, slot, "Bump")
            else:
                read_map(cur, i, slot, "Std")
    ns = cur.u32(p + ".NumShaderMaps", o,
                 "engine:NiTexturingProperty::LoadBinary shader uiListSize")
    if ns > 64:
        raise WalkFail("implausible shader map count %d" % ns)
    for k in range(ns):
        has = cur.u8("%s.shader[%d].HasMap" % (p, k), o,
                     "engine:NiTexturingProperty shader loop bHasMap")
        if has == 1:
            read_map(cur, i, k, "Shader")
            cur.u32("block%d.NiTexturingProperty.shader[%d].ID" % (i, k),
                    o, "engine:ShaderMap::LoadBinary m_uiID")


def nitrishape(cur, i):
    # NiGeometry::LoadBinary: NiAVObject chain, Data ref, SkinInstance
    # ref, bShader(+NiShader name+implementation)
    avobject(cur, i, "NiTriShape")
    o = "block%d(NiTriShape)" % i
    p = "block%d.NiTriShape" % i
    cur.u32(p + ".Data", o, "engine:NiGeometry::LoadBinary m_spModelData")
    cur.u32(p + ".SkinInstance", o,
            "engine:NiGeometry::LoadBinary m_spSkinInstance")
    bsh = cur.u8(p + ".HasShader", o,
                 "engine:NiGeometry::LoadBinary bShader (v>=5.0.0.21)")
    if bsh == 1:
        cur.cstr(p + ".ShaderName", o,
                 "engine:NiShader::LoadBinary m_pszName")
        cur.u32(p + ".ShaderImplementation", o,
                "engine:NiShader::LoadBinary m_uiImplementation")


def ninode(cur, i):
    # NiNode::LoadBinary: NiAVObject chain, children list, effects list
    avobject(cur, i, "NiNode")
    o = "block%d(NiNode)" % i
    p = "block%d.NiNode" % i
    n = cur.u32(p + ".NumChildren", o,
                "engine:NiNode::LoadBinary ReadMultipleLinkIDs")
    if n > 4096:
        raise WalkFail("implausible child count %d" % n)
    for k in range(n):
        cur.u32("%s.Children[%d]" % (p, k), o,
                "engine:NiNode::LoadBinary ReadMultipleLinkIDs")
    m = cur.u32(p + ".NumEffects", o,
                "engine:NiNode::LoadBinary ReadMultipleLinkIDs")
    if m > 4096:
        raise WalkFail("implausible effect count %d" % m)
    for k in range(m):
        cur.u32("%s.Effects[%d]" % (p, k), o,
                "engine:NiNode::LoadBinary ReadMultipleLinkIDs")


def nizbuffer(cur, i):
    # NiZBufferProperty::LoadBinary @10.1: own u16 flags + Function
    objectnet(cur, i, "NiZBufferProperty")
    o = "block%d(NiZBufferProperty)" % i
    p = "block%d.NiZBufferProperty" % i
    cur.u16(p + ".Flags", o,
            "engine:NiZBufferProperty::LoadBinary m_uFlags u16")
    cur.u32(p + ".Function", o,
            "engine:NiZBufferProperty::LoadBinary m_eTest")


def nivertexcolor(cur, i):
    # NiVertexColorProperty::LoadBinary @10.1: own u16 flags + 2 enums
    objectnet(cur, i, "NiVertexColorProperty")
    o = "block%d(NiVertexColorProperty)" % i
    p = "block%d.NiVertexColorProperty" % i
    cur.u16(p + ".Flags", o,
            "engine:NiVertexColorProperty::LoadBinary m_uFlags u16")
    cur.u32(p + ".Source", o,
            "engine:NiVertexColorProperty::LoadBinary m_eSource")
    cur.u32(p + ".Lighting", o,
            "engine:NiVertexColorProperty::LoadBinary m_eLighting")


def nisourcetexture(cur, i):
    # NiSourceTexture::LoadBinary @10.1 (v>=10.0.1.4 path):
    # NiObjectNET chain, bExternal u8, filename CString (UNCONDITIONAL),
    # pixel-data link u32 (UNCONDITIONAL), PixelLayout, MipMapped,
    # AlphaFmt, bStatic u8. DirectRender needs v>=10.1.0.103 -> absent.
    objectnet(cur, i, "NiSourceTexture")
    o = "block%d(NiSourceTexture)" % i
    p = "block%d.NiSourceTexture" % i
    ue = cur.u8(p + ".UseExternal", o,
                "engine:NiSourceTexture::LoadBinary bExternalTexture")
    fn, fn_start = cur.cstr(
        p + ".FileName", o,
        "engine:NiSourceTexture::LoadBinary LoadCString(m_pcFilename)")
    cur.u32(p + ".PixelDataLink", o,
            "engine:NiSourceTexture::LoadBinary ReadLinkID")
    cur.u32(p + ".PixelLayout", o,
            "engine:NiSourceTexture::LoadBinary m_ePixelLayout")
    cur.u32(p + ".UseMipmaps", o,
            "engine:NiSourceTexture::LoadBinary m_eMipMapped")
    cur.u32(p + ".AlphaFormat", o,
            "engine:NiSourceTexture::LoadBinary m_eAlphaFmt")
    st = cur.u8(p + ".IsStatic", o,
                "engine:NiSourceTexture::LoadBinary bStatic")
    return {"use_external": ue, "file_name": fn, "is_static": st}


READERS = {
    "NiNode": ninode,
    "NiZBufferProperty": nizbuffer,
    "NiVertexColorProperty": nivertexcolor,
    "NiTriShape": nitrishape,
    "NiTexturingProperty": nitexturingproperty,
    "NiSourceTexture": nisourcetexture,
}



def walk(data, blocks_to_walk):
    """Walk header + blocks 0..N-1. Returns (info, per-block records)."""
    cur = Cur(data)
    hdr = walk_header(cur)
    if hdr["num_blocks"] <= max(blocks_to_walk):
        raise WalkFail("file too small for requested blocks")
    recs = {}
    for i in range(max(blocks_to_walk) + 1):
        tname = hdr["types"][hdr["idx"][i]]
        start = cur.pos
        g = gid(cur, i, tname)
        info = {"type": tname, "start": start, "gid_offset": start,
                "gid": g}
        if i in blocks_to_walk and tname in READERS:
            r = READERS[tname](cur, i)
            if isinstance(r, dict):
                info.update(r)
        elif tname not in READERS:
            raise WalkFail("no engine-transcribed reader for %s" % tname)
        info["end"] = cur.pos
        recs[i] = info
        # block boundary markers in the trace
        trace.append({"field": "BOUNDARY:block%d_start" % i,
                      "offset": start, "length": 0, "hex": "",
                      "decoded_value": "%s gid=%d" % (tname, g),
                      "semantic_owner": "block%d(%s)" % (i, tname),
                      "source_method": "walker-boundary"})
        trace.append({"field": "BOUNDARY:block%d_end" % i,
                      "offset": cur.pos, "length": 0, "hex": "",
                      "decoded_value": tname,
                      "semantic_owner": "block%d(%s)" % (i, tname),
                      "source_method": "walker-boundary"})
    # next block GroupID (block N where N = max+1)
    nb = max(blocks_to_walk) + 1
    tname = hdr["types"][hdr["idx"][nb]]
    goff = cur.pos
    g2 = cur.u32("block%d.%s.GroupID" % (nb, tname),
                 "block%d(%s)" % (nb, tname),
                 "engine:NiObject::LoadBinary")
    recs["next"] = {"index": nb, "type": tname,
                    "groupid_offset": goff, "groupid": g2}
    return hdr, recs


def negative_controls():
    """Walker must FAIL on corrupted inputs. Returns list of
    (name, expected_fail, got_fail, detail)."""
    data = open(PATH, "rb").read()
    results = []

    def expect_fail(name, payload, needle=None):
        ok = False
        detail = ""
        try:
            global trace
            trace_backup = trace[:]
            del trace[:]
            walk(payload, [0, 1, 2, 3, 4, 5, 6])
            detail = "WALKED WITHOUT FAILURE"
        except WalkFail as e:
            ok = True
            detail = "WalkFail: %s" % e
        except Exception as e:  # noqa: BLE001
            ok = True
            detail = "%s: %s" % (type(e).__name__, e)
        finally:
            trace[:] = trace_backup
        results.append((name, True, ok, detail))

    # NC-1: truncated input (cut before block 7's GroupID)
    expect_fail("NC_TRUNCATED_at_1500", data[:1500])
    # NC-2: corrupted string length (header block-type[0] length -> huge)
    bad = bytearray(data)
    # header line is 37 bytes; version u32 @37; uv @41; nb @45; nbt @49
    struct.pack_into("<I", bad, 53, 0x7F000000)
    expect_fail("NC_CORRUPTED_TYPESTR_LENGTH", bytes(bad))
    # NC-3: wrong version (patch Version u32 to 10.2.0.0)
    bad2 = bytearray(data)
    struct.pack_into("<I", bad2, 37, 0x0A020000)
    expect_fail("NC_WRONG_VERSION", bytes(bad2))
    return results


def main():
    data = open(PATH, "rb").read()
    print("file_size %d" % len(data))
    print("file_sha256 %s" % hashlib.sha256(data).hexdigest())
    hdr, recs = walk(data, [0, 1, 2, 3, 4, 5, 6])
    for i in range(7):
        r = recs[i]
        print("block%d %s start=%d gid_off=%d gid=%d end=%d"
              % (i, r["type"], r["start"], r["gid_offset"], r["gid"],
                 r["end"]))
    nxt = recs["next"]
    b6 = recs[6]
    b5 = recs[5]
    print("block5_end %d" % b5["end"])
    print("block6_start %d" % b6["start"])
    print("block6_end %d" % b6["end"])
    print("block6_use_external %d" % b6.get("use_external", -1))
    print("block6_file_name %r" % b6.get("file_name"))
    print("block6_is_static %d" % b6.get("is_static", -1))
    print("block7_type %s" % nxt["type"])
    print("block7_groupid_offset %d" % nxt["groupid_offset"])
    print("block7_groupid %d" % nxt["groupid"])
    # bytes at the OLD alleged offset (from the retracted claim):
    # 479309 = 0x0007504D. Find whether it occurs at all and where.
    needle = struct.pack("<I", 479309)
    hits = []
    pos = 0
    while True:
        p = data.find(needle, pos)
        if p < 0:
            break
        hits.append(p)
        pos = p + 1
    print("needle_479309_le_hits %s" % hits)
    for h in hits:
        trace.append({
            "field": "ADJUDICATION.needle_479309@%d" % h,
            "offset": h, "length": 4, "hex": needle.hex(),
            "decoded_value": "479309", "semantic_owner": "TBD",
            "source_method": "byte-search"})
    # negative controls
    ncs = negative_controls()
    all_ok = True
    for name, exp, got, detail in ncs:
        print("NC %s expected_fail=%s got_fail=%s :: %s"
              % (name, exp, got, detail))
        trace.append({
            "field": "NEGATIVE_CONTROL.%s" % name, "offset": -1,
            "length": 0, "hex": "", "decoded_value":
                "expected_fail=1 got_fail=%d detail=%s" % (1 if got else 0,
                                                           detail),
            "semantic_owner": "negative_control",
            "source_method": "corrupted-input probe"})
        if not got:
            all_ok = False
    # write CSV
    os.makedirs(os.path.dirname(os.path.abspath(OUT_CSV)), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "field", "offset", "length", "hex", "decoded_value",
            "semantic_owner", "source_method"])
        w.writeheader()
        for row in trace:
            w.writerow(row)
    print("csv_rows %d" % len(trace))
    print("csv_path %s" % os.path.abspath(OUT_CSV))
    print("NEGATIVE_CONTROLS_ALL_FAIL_AS_EXPECTED %s" % all_ok)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

