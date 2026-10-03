#!/usr/bin/env python3
# compare adapter -- oracle vs OUR decoder structural comparison.
#
# Implements order s11: the 19-item comparison list with statuses in the
# closed set {MATCH, MISMATCH, NOT_AVAILABLE_IN_ORACLE,
# NOT_AVAILABLE_IN_OUR_DECODER, SEMANTICALLY_UNRESOLVED}.
#
# FLOAT POLICY (G-CMP-1/G-CMP-2): serialized fields are compared BIT-EXACT
# (both sides read the same file bytes); where a side stores a float it must
# be the exact float32 value. COMPUTED world transforms are computed on BOTH
# sides from the identical serialized local transforms via the identical
# documented formula (NiTransform::operator*, Win32\NiTransform.inl L15-24;
# UpdateWorldData, NiAVObject_Win32.cpp L22-31) and then compared bit-exact;
# no tolerance is applied anywhere, and none may be widened to manufacture
# MATCH.
#
# ORACLE_MODE of the produced comparison: MIXED (the oracle side may be a
# SOURCE_DERIVED_REIMPLEMENTATION output, the ours side is OUR decoder).

import json

ADAPTER_ID = "compare"
ORACLE_MODE = "MIXED"
ERA_CATEGORY = "OUR_TOOL"

ITEMS = [
    "block_count", "object_count", "type_histogram", "object_ordering",
    "names", "parent_child_edges", "local_transforms", "world_transforms",
    "geometry_count", "vertex_counts", "triangle_counts", "uv_sets",
    "normals", "bounding_volumes", "controllers", "properties",
    "texture_references", "unknown_blocks", "parse_failures",
]


def _ft_eq(a, b):
    """Bit-exact compare of serialized float values (int or float)."""
    return a == b


def _blocks_by_index(side):
    out = {}
    for b in side.get("blocks", []):
        out[b.get("index")] = b
    return out


def compare(oracle_json, our_json):
    """oracle_json/our_json: dicts in the canonical forms produced by the
    gb12 adapter (full-decode) and by our FIELD_IDENTITY_V2 runner."""
    oracle = oracle_json
    ours = our_json
    result = {
        "schema": "gamebryo_oracle/comparison_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "float_policy": ("serialized fields bit-exact; computed world "
                         "transforms computed identically on both sides from "
                         "identical serialized locals (NiTransform::operator* "
                         "L15-24 + UpdateWorldData L22-31), then bit-exact; "
                         "no tolerance applied"),
        "oracle_identity": {
            "adapter": oracle.get("adapter"),
            "ORACLE_MODE": oracle.get("ORACLE_MODE"),
            "loader_source_identity": oracle.get("oracle", {}).get(
                "loader_source_identity"),
            "input_sha256": oracle.get("input_identity", {}).get("sha256"),
            "decode_continued_after_rtti_gate": oracle.get(
                "decode_continued_after_rtti_gate"),
        },
        "our_decoder_identity": ours.get("decoder_identity"),
        "input_identity_check": {
            "oracle_sha256": oracle.get("input_identity", {}).get("sha256"),
            "our_sha256": ours.get("input_identity", {}).get("sha256"),
            "same_input": (oracle.get("input_identity", {}).get("sha256") ==
                           ours.get("input_identity", {}).get("sha256")),
        },
        "items": {},
    }
    items = result["items"]
    result["summary"] = {}
    ob = oracle.get("objects", [])
    ub = ours.get("blocks", [])
    o_dec = {o.get("index"): o for o in ob if o is not None}
    u_dec = {b.get("index"): b for b in ub}

    # PARSE-AWARE STATUS: if a side failed to parse, its data-dependent items
    # are NOT_AVAILABLE on that side (never a spurious MISMATCH vs empty).
    our_failed = not ours.get("parse", {}).get("accepted", False)
    oracle_no_blocks = (not ob) and not oracle.get(
        "decode_continued_after_rtti_gate", False)

    def _na_items(detail):
        out = {}
        for k in ITEMS:
            out[k] = {"status": "NOT_AVAILABLE", "detail": detail}
        return out

    if our_failed and oracle_no_blocks:
        na = _na_items(
            "NEITHER side produced block data: oracle=%r; our=%r" %
            (oracle.get("load_result", {}).get("error"),
             ours.get("parse", {}).get("error")))
        for k in ITEMS:
            items[k] = na[k]
        items["input_identity_check"] = result["input_identity_check"]
        items["parse_failures"] = {
            "status": "MATCH" if (oracle.get("load_result", {}).get(
                "accepted") is False and our_failed) else "MISMATCH",
            "oracle": {"accepted": oracle.get("load_result", {}).get(
                "accepted"), "error": oracle.get("load_result", {}).get(
                "error")},
            "our": {"accepted": False,
                    "error": ours.get("parse", {}).get("error")},
            "note": "both sides failed; the reasons differ (oracle: original "
                    "GB 1.2 semantics; our: FIELD_IDENTITY_V2 decoder limits)"}
        result["summary"]["counts"] = {
            s: sum(1 for v in items.values()
                   if isinstance(v, dict) and v.get("status") == s)
            for s in ("MATCH", "MISMATCH", "NOT_AVAILABLE_IN_ORACLE",
                      "NOT_AVAILABLE_IN_OUR_DECODER",
                      "SEMANTICALLY_UNRESOLVED", "NOT_AVAILABLE")}
        return result
    if our_failed:
        detail = ("our decoder failed: %r" % ours.get("parse", {}).get(
            "error"))
        for k in ("block_count", "object_count", "type_histogram",
                  "object_ordering", "names", "parent_child_edges",
                  "local_transforms", "world_transforms", "geometry_count",
                  "vertex_counts", "triangle_counts", "uv_sets", "normals",
                  "bounding_volumes", "controllers", "properties",
                  "texture_references"):
            items[k] = {"status": "NOT_AVAILABLE_IN_OUR_DECODER",
                        "detail": detail}
    if oracle_no_blocks:
        detail = ("oracle produced no block data (original verdict: %r); "
                  "oracle-side header data compared below where present"
                  % oracle.get("load_result", {}).get("error"))
        for k in ("object_count", "names", "parent_child_edges",
                  "local_transforms", "world_transforms", "geometry_count",
                  "vertex_counts", "triangle_counts", "uv_sets", "normals",
                  "bounding_volumes", "controllers", "properties",
                  "texture_references", "unknown_blocks"):
            items[k] = {"status": "NOT_AVAILABLE_IN_ORACLE",
                        "detail": detail}

    # 1/2. block count / object count
    ocount = oracle.get("input_identity", {}).get("num_blocks_from_header")
    ucount = ours.get("num_blocks")
    items["block_count"] = _st(ocount, ucount)
    items["object_count"] = _st(
        len([o for o in ob if o is not None]),
        len(ub), note="oracle counts decoded blocks (unknown runs recorded "
                      "as boundary-only blocks)")

    # 3. type histogram
    oh = oracle.get("type_histogram", {})
    uh = {}
    for b in ub:
        t = b.get("type")
        uh[t] = uh.get(t, 0) + 1
    items["type_histogram"] = _st(oh, uh)

    # 4. object ordering (type sequence)
    oord = [o.get("type") for o in ob if o is not None]
    uord = [b.get("type") for b in ub]
    items["object_ordering"] = _st(oord, uord)

    # 5. names (per-block, decoded blocks only on the oracle side)
    onames = {i: o.get("name") for i, o in o_dec.items()
              if o.get("status") is None}
    unames = {i: b.get("name") for i, b in u_dec.items()
              if b.get("status") in (None, "decoded")}
    items["names"] = _st(onames, unames)

    # 6. parent-child edges
    oedges = sorted(tuple(sorted(e.items())) for e in
                    oracle.get("scene_graph", {}).get("edges", []))
    uedges = sorted(tuple(sorted(e.items())) for e in
                    ours.get("scene_graph", {}).get("edges", []))
    items["parent_child_edges"] = _st(oedges, uedges)

    # 7. local transforms (bit-exact)
    mism = []
    compared = 0
    for i, o in o_dec.items():
        if o.get("status") is not None or "local_transform" not in o:
            continue
        u = u_dec.get(i)
        if u is None or "local_transform" not in u:
            mism.append("block %d: local transform not available on our "
                        "side" % i)
            continue
        compared += 1
        if not _transform_eq(o["local_transform"], u["local_transform"]):
            mism.append("block %d: local transform mismatch" % i)
    items["local_transforms"] = _st_pairs(compared, mism)

    # 8. world transforms (computed identically both sides; bit-exact)
    try:
        om = _world_transforms(o_dec, oracle.get("scene_graph", {}).get("edges", []))
        um = _world_transforms(u_dec, ours.get("scene_graph", {}).get("edges", []))
        wmism = []
        wcomp = 0
        for i in om:
            if i not in um:
                continue
            wcomp += 1
            if not _transform_eq(om[i], um[i]):
                wmism.append("block %d: world transform mismatch" % i)
        items["world_transforms"] = _st_pairs(
            wcomp, wmism,
            note="computed on both sides from identical serialized locals via the "
                 "identical formula (see float_policy); no independent oracle "
                 "computation exists")
    except Exception as e:  # noqa: BLE001 -- honest, never a fake MATCH
        items["world_transforms"] = {
            "status": "SEMANTICALLY_UNRESOLVED",
            "detail": "world-transform computation failed: %r" % e}

    # 9. geometry count
    og = sum(1 for o in o_dec.values() if o.get("type") == "NiTriShape")
    ug = sum(1 for b in u_dec.values() if b.get("type") == "NiTriShape")
    items["geometry_count"] = _st(og, ug)

    # 10-13. per-geometry counts (join through the geometry -> data link)
    def _geom_stats(dec, data_field):
        stats = {}
        for i, o in dec.items():
            if o.get("type") != "NiTriShape":
                continue
            dl = (o.get("links", {}) or o.get("data_links", {})
                  ).get(data_field, [None])
            if isinstance(dl, int):
                dl = [dl]
            di = dl[0] if dl and isinstance(dl[0], int) else None
            d = dec.get(di) if di is not None else None
            stats[i] = {
                "data_block": di,
                "num_vertices": (d or {}).get("num_vertices"),
                "num_triangles": (d or {}).get("num_triangles"),
                "uv_sets": (d or {}).get("num_texture_sets"),
                "has_normals": (d or {}).get("has_normals"),
                "model_bound": (d or {}).get("model_bound"),
            }
        return stats
    ostats = _geom_stats(o_dec, "model_data")
    ustats = _geom_stats(u_dec, "model_data")
    for key, field in (("vertex_counts", "num_vertices"),
                       ("triangle_counts", "num_triangles"),
                       ("uv_sets", "uv_sets"),
                       ("normals", "has_normals"),
                       ("bounding_volumes", "model_bound")):
        mism = []
        comp = 0
        for i in ostats:
            if i not in ustats:
                continue
            comp += 1
            if ostats[i].get(field) != ustats[i].get(field):
                mism.append("geometry %d: %s oracle=%r our=%r" %
                            (i, field, ostats[i].get(field),
                             ustats[i].get(field)))
        items[key] = _st_pairs(comp, mism)

    # 14. controllers
    oc = oracle.get("controllers", [])
    uc = ours.get("controllers", [])
    items["controllers"] = _st(
        [{"index": c.get("index"), "type": c.get("type"),
          "target": c.get("target")} for c in oc],
        [{"index": c.get("index"), "type": c.get("type"),
          "target": c.get("target")} for c in uc])

    # 15. properties
    items["properties"] = _st(
        [{"index": p.get("index"), "type": p.get("type")}
         for p in oracle.get("properties", [])],
        [{"index": p.get("index"), "type": p.get("type")}
         for p in ours.get("properties", [])])

    # 16. texture references
    items["texture_references"] = _st(
        [{"index": t.get("index"), "filename": t.get("filename")}
         for t in oracle.get("textures", [])],
        [{"index": t.get("index"), "filename": t.get("filename")}
         for t in ours.get("textures", [])])

    # 17. unknown blocks (oracle: unknowns; ours: decoded or unknown)
    ounk = sorted(set(u.get("class") for u in oracle.get("unknowns", [])))
    uunk = sorted(set(b.get("type") for b in ub
                      if b.get("status") not in (None, "decoded")))
    if ounk and not uunk:
        items["unknown_blocks"] = {
            "status": "NOT_AVAILABLE_IN_OUR_DECODER",
            "detail": "oracle reports unknowns %r; our decoder reports none"
                      % ounk}
    elif uunk and not ounk:
        items["unknown_blocks"] = {
            "status": "NOT_AVAILABLE_IN_ORACLE",
            "detail": "our decoder decodes %r (or reports unknown) which the "
                      "oracle could not decode" % uunk}
    else:
        items["unknown_blocks"] = {
            "status": "SEMANTICALLY_UNRESOLVED" if ounk != uunk else "MATCH",
            "detail": "oracle unknowns=%r; our unknown/undecoded=%r; the "
                      "oracle records UNREGISTERED classes as unknown by "
                      "ORIGINAL GB 1.2 semantics while our decoder decodes "
                      "MindArk NiArk* via byte-derived boundaries -- "
                      "neither side's 'unknown' set is comparable as "
                      "equality" % (ounk, uunk)}

    # 18. parse failures
    items["parse_failures"] = _st(
        {"accepted": oracle.get("load_result", {}).get("accepted"),
         "error": oracle.get("load_result", {}).get("error")},
        {"accepted": ours.get("parse", {}).get("accepted"),
         "error": ours.get("parse", {}).get("error")},
        note="statuses differ BY DESIGN for NiArk* files: the oracle reports "
             "the ORIGINAL fail-closed RTTIError verdict (+partial "
             "continuation in full-decode), our decoder accepts; this is the "
             "primary finding, not a defect")

    result["summary"] = {
        "counts": {s: sum(1 for v in items.values()
                          if isinstance(v, dict) and v.get("status") == s)
                   for s in ("MATCH", "MISMATCH", "NOT_AVAILABLE_IN_ORACLE",
                             "NOT_AVAILABLE_IN_OUR_DECODER",
                             "SEMANTICALLY_UNRESOLVED", "NOT_AVAILABLE")},
    }
    # PARSE-AWARE FINAL PASS (applied last so it wins over the structural
    # comparisons): when a side failed to parse, its data-dependent items
    # are NOT_AVAILABLE on that side -- never a spurious MISMATCH vs empty.
    our_failed = not ours.get("parse", {}).get("accepted", False)
    oracle_no_blocks = (not [o for o in ob if o is not None]) and not oracle.get(
        "decode_continued_after_rtti_gate", False)
    if our_failed:
        detail = ("our decoder failed: %r" % ours.get("parse", {}).get(
            "error"))
        for k in ("block_count", "object_count", "type_histogram",
                  "object_ordering", "names", "parent_child_edges",
                  "local_transforms", "world_transforms", "geometry_count",
                  "vertex_counts", "triangle_counts", "uv_sets", "normals",
                  "bounding_volumes", "controllers", "properties",
                  "texture_references", "unknown_blocks"):
            items[k] = {"status": "NOT_AVAILABLE_IN_OUR_DECODER",
                        "detail": detail}
    if oracle_no_blocks:
        detail = ("oracle produced no block data (original verdict: %r); "
                  "oracle-side header data retained in block_count/"
                  "type_histogram where available"
                  % oracle.get("load_result", {}).get("error"))
        for k in ("object_count", "names", "parent_child_edges",
                  "local_transforms", "world_transforms", "geometry_count",
                  "vertex_counts", "triangle_counts", "uv_sets", "normals",
                  "bounding_volumes", "controllers", "properties",
                  "texture_references", "unknown_blocks"):
            items[k] = {"status": "NOT_AVAILABLE_IN_ORACLE",
                        "detail": detail}
    if our_failed or oracle_no_blocks:
        result["summary"] = {
            "counts": {s: sum(1 for v in items.values()
                              if isinstance(v, dict) and
                              v.get("status") == s)
                       for s in ("MATCH", "MISMATCH",
                                 "NOT_AVAILABLE_IN_ORACLE",
                                 "NOT_AVAILABLE_IN_OUR_DECODER",
                                 "SEMANTICALLY_UNRESOLVED", "NOT_AVAILABLE")},
        }
    return result


def _st(a, b, note=None):
    out = {"status": "MATCH" if a == b else "MISMATCH",
           "oracle": a, "our": b}
    if note:
        out["note"] = note
    return out


def _st_pairs(compared, mism, note=None):
    if compared == 0 and mism:
        return {"status": "MISMATCH", "detail": mism, "compared": 0}
    if not mism:
        out = {"status": "MATCH", "compared": compared}
        if note:
            out["note"] = note
        return out
    return {"status": "MISMATCH", "compared": compared, "detail": mism}


def _transform_eq(a, b):
    if set(a.keys()) != set(b.keys()):
        return False
    if a.get("translate") != b.get("translate"):
        return False
    if a.get("scale") != b.get("scale"):
        return False
    ra, rb = a.get("rotate"), b.get("rotate")
    if ra != rb:
        return False
    return True


def _world_transforms(blocks, edges):
    """Compute COMPUTED_WORLD_TRANSFORM per UpdateWorldData semantics
    (NiAVObject_Win32.cpp L22-31: m_kWorld = parent->m_kWorld * m_kLocal,
    else m_kWorld = m_kLocal; NiTransform::operator* Win32 inl L15-24:
    scale=sa*sb, rotate=Ra*Rb, translate=ta + sa*(Ra*tb))."""
    parent = {}
    for e in edges:
        c = e.get("child")
        p = e.get("parent")
        if isinstance(c, int) and c not in parent:
            parent[c] = p
    worlds = {}
    ident = [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
             [0.0, 0.0, 0.0], 1.0]  # [rotate, translate, scale]

    def local_of(i):
        b = blocks.get(i)
        if b is None:
            return None
        lt = b.get("local_transform")
        if lt is None:
            return None
        return [lt["rotate"], lt["translate"], lt["scale"]]

    def mul(a, b):
        ra, ta, sa = a
        rb, tb, sb = b
        rot = _matmul(ra, rb)
        tr = [ta[c] + sa * sum(ra[c][k] * tb[k] for k in range(3))
              for c in range(3)]
        return [rot, tr, sa * sb]

    def compute(i, seen=None):
        if i in worlds:
            return worlds[i]
        seen = seen or set()
        if i in seen:
            return None
        loc = local_of(i)
        if loc is None:
            return None
        p = parent.get(i)
        if p is None:
            w = loc
        else:
            pw = compute(p, seen | {i})
            if pw is None:
                return None
            w = mul(pw, loc)
        worlds[i] = w
        return w

    for i in blocks:
        if blocks[i].get("local_transform") is not None:
            compute(i)
    return {i: {"rotate": w[0], "translate": w[1], "scale": w[2]}
            for i, w in worlds.items()}


def _matmul(a, b):
    out = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s = 0.0
            for k in range(3):
                s += a[i][k] * b[k][j]
            out[i][j] = s
    return out


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
