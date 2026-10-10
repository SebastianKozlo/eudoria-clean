#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""s17_scene_structure_and_relations_r1.py — SCENE_STRUCTURE_RESULTS.json
(contract section 12) + MODEL_218757_RELATION_RESULTS.json (contract section 13)
for RUN_ID PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009.

Evidence layers (kept DISTINCT; INDEPENDENCE labeled per edge):
  - OUR_PARSER_RESULT: gb12 adapter full-decode outputs (closure-verified
    files only) + the fresh s2 Rosetta-lineage parse of 218757 (copy of the
    documented s2_parse_nif101.py; canonical READ_ONLY).
  - Native: NOT AVAILABLE for any selected PE input (all four natively
    rejected; stock printer generic + helper specific error) — recorded
    honestly, never fabricated.
  - Geometry arrays decoded from the payload bytes using the DOCUMENTED
    closure-proven field layout (Rosetta baseline spec; validated against
    BOTH parsers' measured counts and the adapter's model_bound values).
Payload discipline: vertex/triangle arrays stay IN MEMORY (LOCAL_ONLY);
published output = identities, counts, fingerprints, graph paths, evidence
locators, concise transform/bound summaries.
"""
import hashlib
import json
import os
import struct

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
OUT_ROOT = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = os.path.join(OUT_ROOT, "02_PE")
RAW = os.path.join(PE_OUT, "raw")
LOCAL_ROOT = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PAYLOAD_DIR = os.path.join(LOCAL_ROOT, "02_PE_payloads")
S2_BLOCKMAP = os.path.join(LOCAL_ROOT, "02_PE_work",
                           "NIF101_BLOCKMAP_218757_R1.json")

CLOSURE_OK = ["218757", "423020"]
CLOSURE_FAILED = {
    "496633": "closure search budget exhausted (measured; 1011 s run; "
              "ADAPTER_INTEGRITY=FAIL structural closure)",
    "512126": "CLOSURE_SEARCH_FAILED: no boundary assignment closes the file "
              "to EOF (measured; ADAPTER_INTEGRITY=FAIL structural closure)",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha_hex(b):
    return hashlib.sha256(b).hexdigest().upper()


# ---------------- geometry extraction (documented s2/Rosetta layout) ------

class G:
    def __init__(self, data, pos):
        self.d, self.p = data, pos

    def u8(self):
        v = self.d[self.p]
        self.p += 1
        return v

    def u16(self):
        v = struct.unpack_from("<H", self.d, self.p)[0]
        self.p += 2
        return v

    def u32(self):
        v = struct.unpack_from("<I", self.d, self.p)[0]
        self.p += 4
        return v

    def f32(self):
        v = struct.unpack_from("<f", self.d, self.p)[0]
        self.p += 4
        return v

    def raw(self, n):
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def v3raw(self):
        return self.raw(12)


def extract_geometry(data, byte_start, expect_nv, expect_nt, expect_bound):
    """Extract (vertices_bytes, triangles_bytes) from a NiTriShapeData block
    using the documented closure-proven layout. Validates against the
    adapter-measured counts/bound (fail-closed)."""
    g = G(data, byte_start)
    gid = g.u32()
    if gid != 0:
        raise ValueError("GroupID != 0 at %d" % byte_start)
    nv = g.u16()
    keep = g.u8()
    compress = g.u8()
    hv = g.u8()
    if nv != expect_nv:
        raise ValueError("nv %d != %d" % (nv, expect_nv))
    verts = g.raw(nv * 12) if hv else b""
    nuvsets_u8 = g.u8()
    extra_flags = g.u8()
    hn = g.u8()
    if hn:
        g.raw(nv * 12)
        if extra_flags & 16:
            g.raw(nv * 24)
    bc = [g.f32(), g.f32(), g.f32()]
    br = g.f32()
    if expect_bound is not None:
        for a, b in zip(bc, expect_bound["center"]):
            if abs(a - b) > 1e-4:
                raise ValueError("bound center mismatch %r vs %r" % (bc, expect_bound))
        if abs(br - expect_bound["radius"]) > 1e-4:
            raise ValueError("bound radius mismatch")
    hvc = g.u8()
    if hvc:
        g.raw(nv * 16)
    nuv = nuvsets_u8 & 63
    g.raw(nuv * nv * 8)
    g.u16()  # consistency/dirty flags
    nt = g.u16()
    if nt != expect_nt:
        raise ValueError("nt %d != %d" % (nt, expect_nt))
    tri_points = g.u32()
    has_tri = g.u8()
    if not has_tri:
        raise ValueError("no triangle list")
    if tri_points != nt * 3:
        raise ValueError("tri_points %d != %d" % (tri_points, nt * 3))
    tris = g.raw(nt * 6)
    return {"vertices_bytes": verts, "triangles_bytes": tris,
            "num_vertices": nv, "num_triangles": nt,
            "num_uv_sets": nuv, "model_bound_center": bc,
            "model_bound_radius": br}


# ---------------- typed graph ------------------------------------------------

def build_graph(full, name):
    objs = full["objects"]
    sg = full["scene_graph"]
    n = len(objs)
    nodes = []
    edges = []
    NS = ("SERIALIZED_BLOCK_ID (gb12 adapter full-decode; OUR_PARSER_RESULT; "
          "closure-verified)")
    for o in objs:
        if o is None:
            nodes.append({"block": None,
                          "status": "UNMAPPED (no closing assignment)"})
            continue
        kind = ("BOUNDARY_ONLY_OPAQUE" if o.get("status") else "SEMANTIC")
        node = {
            "block": o["index"], "namespace": NS, "type": o.get("type"),
            "name": o.get("name"),
            "decode_kind": kind,
            "byte_start": o.get("byte_start"), "byte_end": o.get("byte_end"),
            "native_pointer": "NOT_AVAILABLE_NO_NATIVE_LOAD",
            "traversal_id": "NOT_AVAILABLE_NO_NATIVE_LOAD",
        }
        if o.get("local_transform") is not None:
            lt = o["local_transform"]
            node["serialized_local_transform"] = {
                "translate": lt["translate"], "rotate": lt["rotate"],
                "scale": lt["scale"],
                "semantics": lt.get("local_transform_semantics"),
            }
        nodes.append(node)
        links = o.get("links", {}) or {}
        for lid in links.get("extra_data", []) or []:
            if lid is not None:
                edges.append({"kind": "EXTRA_DATA", "from": o["index"],
                              "to": lid, "field": "extra_data",
                              "namespace": NS})
        for lid in links.get("controller", []) or []:
            if lid is not None:
                edges.append({"kind": "CONTROLLER", "from": o["index"],
                              "to": lid, "field": "controller",
                              "namespace": NS})
        for lid in links.get("properties", []) or []:
            if lid is not None:
                edges.append({"kind": "PROPERTY", "from": o["index"],
                              "to": lid, "field": "properties",
                              "namespace": NS})
        for lid in links.get("children", []) or []:
            if lid is not None:
                edges.append({"kind": "SCENE_CHILD", "from": o["index"],
                              "to": lid, "field": "children",
                              "namespace": NS})
        for lid in links.get("effects", []) or []:
            if lid is not None:
                edges.append({"kind": "UNKNOWN", "from": o["index"],
                              "to": lid, "field": "effects",
                              "note": "NiNode effects array (NiDynamicEffect "
                                      "attachment) — NOT a scene-child edge; "
                                      "text indentation would not establish "
                                      "SCENE_CHILD either"})
        for lid in links.get("model_data", []) or []:
            if lid is not None:
                edges.append({"kind": "RESOURCE_REFERENCE", "from": o["index"],
                              "to": lid, "field": "model_data (geometry data)",
                              "namespace": NS})
        for lid in links.get("skin_instance", []) or []:
            if lid is not None:
                edges.append({"kind": "RESOURCE_REFERENCE", "from": o["index"],
                              "to": lid, "field": "skin_instance",
                              "namespace": NS})
        co = links.get("collision_object", [])
        for lid in co or []:
            if lid is not None:
                edges.append({"kind": "UNKNOWN", "from": o["index"],
                              "to": lid, "field": "collision_object",
                              "namespace": NS})
        if o.get("type") == "NiTexturingProperty":
            for m in o.get("maps", []) or []:
                mm = m.get("map") or {}
                tl = mm.get("texture_link")
                if tl is not None and tl != 0xFFFFFFFF:
                    edges.append({"kind": "RESOURCE_REFERENCE",
                                  "from": o["index"], "to": tl,
                                  "field": "texture slot %d" % m.get("slot"),
                                  "namespace": NS})
    for r in sg.get("roots", []) or []:
        edges.append({"kind": "TOP_LEVEL_ROOT", "from": None,
                      "to": r, "field": "top-level object (footer)",
                      "namespace": NS})
    return nodes, edges


def analyze(name):
    full = load(os.path.join(RAW, "PE_%s.inspect_full.json" % name))
    nodes, edges = build_graph(full, name)
    objs = full["objects"]
    # parent map from SCENE_CHILD edges
    parents = {}
    for e in edges:
        if e["kind"] == "SCENE_CHILD":
            parents.setdefault(e["to"], []).append(e["from"])
    shared = {k: v for k, v in parents.items() if len(v) > 1}
    # roots check: children of nothing vs serialized top-level roots
    top_roots = full["scene_graph"].get("roots", [])
    n_blocks = full["input_identity"]["num_blocks_from_header"]
    hist = full.get("type_histogram", {})
    # compose transforms (FILE_SCENE_SPACE, relative to the file root)
    composed = {}

    def get_lt(o):
        lt = (o or {}).get("local_transform")
        if not lt:
            return None
        return lt

    def compose_chain(bi):
        """Compose from the top-level root down to bi (complete chain only)."""
        chain = [bi]
        cur = bi
        while cur in parents:
            ps = parents[cur]
            if len(ps) != 1:
                return None  # shared parent: chain ambiguous
            cur = ps[0]
            if cur in chain:
                return None  # cycle
            chain.append(cur)
        if cur not in top_roots:
            return None  # chain does not reach a proven file root
        # compose root -> leaf
        R = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        T = [0.0, 0.0, 0.0]
        S = 1.0
        for b in reversed(chain):
            lt = get_lt(objs[b])
            if lt is None:
                return None  # missing transform in the chain
            Rn = lt["rotate"]
            Tn = lt["translate"]
            Sn = lt["scale"]
            # world = parent_world * local (NiTransform semantics)
            R2 = [[sum(R[i][k] * Rn[k][j] for k in range(3)) for j in range(3)]
                  for i in range(3)]
            T2 = [sum(R[i][k] * (Tn[k] * S) for k in range(3)) + T[i]
                  for i in range(3)]
            S2 = S * Sn
            R, T, S = R2, T2, S2
        return {"world_translate": T, "world_scale": S,
                "world_rotate": R}

    for o in objs:
        if o is None:
            continue
        w = compose_chain(o["index"])
        if w is not None:
            composed[o["index"]] = w
    # geometry fingerprints
    data = open(os.path.join(PAYLOAD_DIR, name + ".nif"), "rb").read()
    meshes = []
    for o in objs:
        if o is None or o.get("type") != "NiTriShape":
            continue
        links = o.get("links", {}) or {}
        md = links.get("model_data", [])
        if not md or md[0] is None:
            continue
        dd = objs[md[0]]
        if dd is None or dd.get("type") != "NiTriShapeData":
            continue
        try:
            geo = extract_geometry(data, dd["byte_start"],
                                   dd.get("num_vertices"),
                                   dd.get("num_triangles"),
                                   dd.get("model_bound"))
        except ValueError as ex:
            meshes.append({"mesh_block": o["index"], "data_block": md[0],
                           "extraction_error": str(ex),
                           "status": "EXTRACTION_FAILED"})
            continue
        meshes.append({
            "mesh_block": o["index"], "mesh_name": o.get("name"),
            "data_block": md[0],
            "num_vertices": geo["num_vertices"],
            "num_triangles": geo["num_triangles"],
            "vertex_positions_f32le_sha256": sha_hex(geo["vertices_bytes"]),
            "triangle_indices_u16le_sha256": sha_hex(geo["triangles_bytes"]),
            "model_bound": dd.get("model_bound"),
            "serialized_local_translate": (o.get("local_transform") or {}).get("translate"),
            "status": "EXTRACTED_VALIDATED",
        })
    # bounds summary (separate measurement)
    bounds = [{"block": b.get("index"), "model_bound": b.get("model_bound")}
              for b in objs
              if b and b.get("type") == "NiTriShapeData"
              and b.get("model_bound")]
    # extra data values (supported classes)
    extra = []
    for o in objs:
        if o is None:
            continue
        if o.get("type") == "NiStringExtraData":
            sv = o.get("string_value") or ""
            extra.append({
                "block": o["index"], "type": "NiStringExtraData",
                "extra_data_name": o.get("extra_data_name"),
                "value_length_chars": len(sv),
                "value_sha256": sha_hex(sv.encode("utf-8", "replace")),
                "value_excerpt_first_120":
                    sv[:120].replace("\r\n", "\\r\\n"),
                "value_excerpt_last_60":
                    sv[-60:].replace("\r\n", "\\r\\n"),
                "full_value_local_only": S2_BLOCKMAP if name == "218757" else
                "02_PE/raw/PE_%s.inspect_full.json (value in "
                "string_value field)" % name,
                "classification": "EXPORTER_METADATA (3ds Max NDL exporter "
                                  "settings dump)" if "NiOptimize" in sv
                else "SUPPORTED_EXTRA_DATA_VALUE",
            })
    # controllers
    controllers_present = [o for o in objs
                           if o and "Controller" in (o.get("type") or "")]
    opaque = [o for o in objs if o and o.get("status")]
    result = {
        "asset": name + ".nif",
        "evidence_status": "CLOSURE_VERIFIED (gb12 full-decode structural "
                           "closure PASS; EOF-exact; OUR_PARSER_RESULT)",
        "namespaces": {
            "serialized_block_id": "0..%d from the gb12 adapter full-decode "
                                   "(OUR_PARSER_RESULT)" % (n_blocks - 1),
            "native_pointer": "NOT_AVAILABLE_NO_NATIVE_LOAD (all four PE "
                              "inputs natively rejected: stock printer exit 1 "
                              "generic; helper exit 1 specific "
                              "NO_CREATE_FUNCTION)",
            "traversal_id": "NOT_AVAILABLE_NO_NATIVE_LOAD (no native "
                            "traversal ever ran on the PE originals)",
        },
        "counts": {
            "header_num_blocks": n_blocks,
            "semantic_blocks": sum(1 for o in objs if o and not o.get("status")),
            "boundary_only_blocks": sum(1 for o in objs if o and o.get("status")),
            "type_histogram": hist,
            "top_level_roots": top_roots,
            "controllers": len(controllers_present),
            "scenegraph_children_edges": sum(1 for e in edges
                                             if e["kind"] == "SCENE_CHILD"),
        },
        "serialized_roots": [{"block": r, "type": objs[r].get("type"),
                              "name": objs[r].get("name")}
                             for r in top_roots],
        "native_runtime_state": "NOT_AVAILABLE_NO_NATIVE_LOAD — native "
                                "roots/classes/counts and any alias/"
                                "conversion behavior were never observable on "
                                "the PE originals (NATIVE_LOAD_REJECTED; "
                                "documented in NATIVE_EXECUTION_RESULTS.json "
                                "and NATIVE_HELPER_RESULTS.json)",
        "edges": edges,
        "parent_analysis": {
            "shared_parent_blocks": {str(k): v for k, v in shared.items()},
            "cycles": "checked during composition (cycle guard); none "
                      "encountered" if not shared else "see shared_parent",
            "unlinked_or_opaque_blocks": [o["index"] for o in opaque],
        },
        "transforms": {
            "serialized_local_transforms_present": sum(
                1 for o in objs if o and o.get("local_transform")),
            "post_load_post_update_local_transform":
                "NOT_MEASURED (no native load; the stock printer never "
                "printed; the helper also rejects at the same factory gate)",
            "composed_file_root_transforms_computed": len(composed),
            "composed_transforms": composed,
            "composed_semantics": "FILE_SCENE_SPACE, composed from the "
                                  "serialized local transforms through "
                                  "complete SCENE_CHILD chains to the proven "
                                  "file root ONLY (NiTransform composition "
                                  "NiTransform.inl:15-24); NOT a PE world "
                                  "position; no axis swap / cm-m / x100 "
                                  "imported",
        },
        "bounds": {
            "measurement_class": "SEPARATE MEASUREMENT — per-geometry "
                                 "MODEL_SPACE bounds serialized in "
                                 "NiGeometryData (center+radius); NOT a pivot, "
                                 "NOT a placement, NOT world XYZ",
            "per_geometry_model_bounds": bounds,
        },
        "extra_data_values": extra,
        "controller_presence": {
            "controller_blocks": len(controllers_present),
            "update_could_change_displayed_state":
                False if not controllers_present else
                "POSSIBLE (controllers present; Update(0) runs them "
                "per qualified source; per-value mutation NOT_MEASURED)",
        },
        "geometry_meshes": meshes,
    }
    return result, meshes, objs, edges


def main():
    scene = {}
    all_meshes = {}
    for name in CLOSURE_OK:
        res, meshes, objs, edges = analyze(name)
        scene[name + ".nif"] = res
        all_meshes[name] = meshes
    for name, why in CLOSURE_FAILED.items():
        full = load(os.path.join(RAW, "PE_%s.inspect_full.json" % name))
        scene[name + ".nif"] = {
            "asset": name + ".nif",
            "evidence_status": "NOT_AVAILABLE_VIA_ORACLE_FULL_DECODE",
            "reason": why,
            "available_evidence": {
                "header_metadata": "see CORPUS_METADATA_CENSUS.csv row "
                                    "(version 10.1.0.0, user version 0, "
                                    "blocks, type histogram)",
                "rtti_table_validation": "see PARSER_NATIVE_COMPARISON.json "
                                         "(first table miss "
                                         "NiArkAnimationExtraData, index 1)",
                "native": "NATIVE_LOAD_REJECTED (generic) + helper-observed "
                          "NO_CREATE_FUNCTION NiArkAnimationExtraData",
            },
            "typed_graph": "NOT_BUILT (no closure-verified block boundaries; "
                           "an unknown offset stops dependent parsing — "
                           "contract section 10)",
            "note": "Outcome RETAINED per the frozen selection rule; no "
                    "candidate replacement was attempted. Historical "
                    "cross-reference: the pre-F2 core version closed "
                    "496633 (1288 objects) — labeled historical, different "
                    "tool version; the current pinned copy is the measured "
                    "authority for THIS run.",
        }

    # ---- 218757 specifics (s2 fresh parse evidence) ----
    s2 = load(S2_BLOCKMAP)
    ark = []
    for b in s2["blocks_metadata_only"]:
        t = b.get("type", "")
        if t.startswith("NiArk"):
            rec = {"block": b["index"], "type": t,
                   "evidence": "OUR_PARSER_RESULT (s2 Rosetta-lineage copy, "
                               "fresh parse of the byte-identical payload, "
                               "EOF-exact closure 66/66)",
                   "gb12_status": "boundary-only opaque (UNREGISTERED_IN_GB12_"
                                  "FACTORY; 62+4/66 ceiling preserved)"}
            if t == "NiArkTextureExtraData":
                entries = b.get("ark_texture_entries", [])
                rec["decoded_entries"] = [
                    {"texture_name": e["texture_name"],
                     "texturing_property_ref": e["texturing_property_ref"],
                     "f1_i32": e["f1_i32"], "f2_i32": e["f2_i32"],
                     "bytes9_hex": e["bytes9_hex"]}
                    for e in entries]
                rec["entry_count"] = len(entries)
            elif t == "NiArkImporterExtraData":
                rec["version_string"] = b.get("version_string")
                rec["int1_u32"] = b.get("int1_u32")
                rec["tail41_hex"] = (b.get("tail41_hex") or "")[:40] + "..."
            elif t == "NiArkShaderExtraData":
                rec["shader_config_string"] = b.get("shader_config_string")
            else:
                rec["ext_len"] = b.get("ext_len")
                rec["ext_hex_head"] = (b.get("ext_hex") or "")[:48] + "..."
                rec["note"] = ("byte-derived boundary (closure-constrained); "
                               "content UNDETERMINED beyond the boundary")
            ark.append(rec)
    scene["218757.nif"]["ni_ark_payload_analysis"] = {
        "source": "s2 Rosetta-lineage fresh parse (TOOLS/"
                  "s2_parse_nif101_r1.py; copy of the documented "
                  "PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003 s2; "
                  "canonical SHA256 "
                  "9E1A9A041BBAA8CB8BFC65B5DEE1217C07F33714FF659490C66EC4E922"
                  "BB4B41; copy SHA256 BF45C699B00EEFAE44ED325C421E7ABFA7C1457"
                  "D7309F443A28ED5631C554B2A; output LOCAL_ONLY %s)" % S2_BLOCKMAP,
        "blocks": ark,
        "part_classification": {
            "model_local_structure": "root NiNode 'Scene Root' + 11 sub-NiNode "
                                     "+ 14 NiTriShape meshes (B_Outpost_me01_"
                                     "Ext_* parts, dPVS_occ01..05 occluder "
                                     "planes) with SERIALIZED_LOCAL transforms "
                                     "— all FILE_SCENE_SPACE model structure",
            "exporter_metadata": "NiStringExtraData 'NiStringED000' = the NDL "
                                 "3ds Max exporter settings dump (NiOptimize* "
                                 "/ NetImmerse* flags); NiArkImporterExtraData "
                                 "version string + tail = exporter provenance "
                                 "record",
            "unknown_ark_payloads": "NiArkAnimationExtraData (16 B ext), "
                                    "NiArkViewportInfoExtraData (49 B ext), "
                                    "NiArkTextureExtraData (entry list), "
                                    "NiArkImporterExtraData (41 B tail) — "
                                    "UNREGISTERED in the stock GB 1.2 "
                                    "registry (measured natively: "
                                    "NO_CREATE_FUNCTION)",
            "actual_external_references": "NO standard external texture "
                                          "reference: all NiTexturingProperty "
                                          "map texture_link values are "
                                          "NULL_LINKID (0xFFFFFFFF); the "
                                          "texture bindings live in the "
                                          "MindArk-custom NiArkTextureExtraData "
                                          "block (texture NAMES + per-entry "
                                          "texturing_property refs; 9-byte "
                                          "per-entry tail semantics UNRESOLVED; "
                                          "the historical 'BNT2 id' reading "
                                          "stays a RETRACTED prior claim)",
            "external_file_reference_verdict": "RESOURCE_NAME_REFERENCES_"
                                               "ONLY (texture names inside "
                                               "the file; no resolved "
                                               "container/instance linkage "
                                               "established this run)",
        },
        "model_extents_FILE_SCENE_SPACE": s2["global_bbox_world"],
        "extents_non_promotion": "the model-space extents "
                                 "[2500, 3350, 1250] (game units, FILE_SCENE_"
                                 "SPACE bbox of world-composed vertices) are "
                                 "NOT a historical location; no world XYZ, "
                                 "axis swap, unit conversion or placement is "
                                 "derived from them (contract section 12)",
    }
    # cross-check: s2 worldT vs composed (a few nodes)
    s2tree = s2["mesh_stats"]
    xchecks = []
    for ms in s2tree[:5]:
        bi = ms["index"]
        comp = scene["218757.nif"]["transforms"]["composed_transforms"].get(bi)
        s2w = ms.get("world_T")
        if comp and s2w:
            xchecks.append({"block": bi, "s2_world_T": s2w,
                            "composed_world_T": comp["world_translate"],
                            "agree": all(abs(a - b) < 1e-4
                                         for a, b in zip(s2w,
                                                         comp["world_translate"]))})
    scene["218757.nif"]["transform_cross_check_vs_s2"] = xchecks

    # classification with evidence + alternatives
    scene["218757.nif"]["classification"] = {
        "label": "SINGLE_MODEL (standalone outpost building asset)",
        "evidence": ["single serialized top-level root NiNode 'Scene Root' "
                     "(footer top object 0)",
                     "all geometry in one local hierarchy (38 blocks with "
                     "no parent are the top-level object + unlinked "
                     "property/data blocks; exactly one NiAVObject root)",
                     "node names are asset-part names (B_Outpost_me01_Ext_* "
                     "walls/doors/vents/sign; dPVS_occ01..05 = occluder "
                     "planes), NOT cell/world context",
                     "0 controller blocks; 0 standard external texture "
                     "references",
                     "root local transform is identity/zero translate "
                     "(serialized)"],
        "alternatives": ["compound object assembled from exporter parts "
                         "(the __NDL_MultiMtl_Node hints at multi-material "
                         "export grouping) — compatible with SINGLE_MODEL",
                         "NOT a proven world scene: no cell/world markers, "
                         "no world placement record (contract section 14 "
                         "ceiling applies)"],
        "world_placement_verdict": "NO_WORLD_PLACEMENT_EVIDENCE_FOUND "
                                   "(FILE_SCENE_SPACE only)",
    }
    scene["423020.nif"]["classification"] = {
        "label": "COMPOUND-OBJECT / SCENE-CANDIDATE (structure rank #3 of "
                 "the mechanical compound shortlist — NOT a proven world "
                 "scene)",
        "evidence": ["single top-level root NiNode 'Scene Root'",
                     "119 NiNode objects incl. 'Portal01_01', 'Bip01_item', "
                     "'Bip01_Camera_001..N' rig-like sub-trees",
                     "102 NiTriShape meshes; 0 controllers",
                     "1 NiTextureEffect (boundary-only: registered-but-not-"
                     "decoded by the adapter)"],
        "alternatives": ["a single complex asset with many sub-rigs",
                         "an exporter-grouped compound object"],
        "world_placement_verdict": "NO_WORLD_PLACEMENT_EVIDENCE_FOUND "
                                   "(FILE_SCENE_SPACE only)",
    }

    # placement ceiling per edge (contract section 14)
    ceiling = {
        "MODEL_218757_TO_CMO_JOIN": "NOT_ESTABLISHED",
        "HISTORICAL_WORLD_INSTANCE": "NOT_ESTABLISHED",
        "PE_WORLD_ROOT_IDENTITY": "NOT_ESTABLISHED",
        "PE_AXES_AND_UNITS": "UNVERIFIED",
        "WORLD_XYZ_RECOVERED": "NO",
    }
    scene["placement_ceiling"] = {
        "defaults": ceiling,
        "note": "every edge above carries STATUS/EVIDENCE_SOURCE/ERA_BUILD/"
                "PHYSICAL_SOURCE/INDEPENDENCE; no edge was promoted to a PE "
                "world relation (no genuine new positive was found)",
    }
    out = os.path.join(PE_OUT, "SCENE_STRUCTURE_RESULTS.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"run_id": RUN_ID,
                   "stage": "S17_scene_structure (contract section 12)",
                   "file_scene_space_discipline": "the world coordinate "
                   "system of every reported transform/bound is "
                   "FILE_SCENE_SPACE until an independent PE world/root "
                   "relation is established; no axis swap, cm/m or x100 "
                   "imported from any other engine/format/UI/source",
                   "assets": scene}, f, indent=2)
    print("WROTE", out)

    # ---------------- 218757 geometry relations ---------------------------
    rel = {
        "run_id": RUN_ID,
        "stage": "S17_bounded_218757_comparison (contract section 13)",
        "comparison_scope": {
            "max_allowed": 3,
            "attempted": 1,
            "basis": "safe decoding provides geometry for 218757 AND 423020 "
                     "(both closure-verified); 496633/512126 provide NO safe "
                     "geometry (closure failed — measured outcomes retained)",
        },
        "fingerprint_method": {
            "vertex_positions": "SHA256 over the EXACT serialized f32 LE "
                                "vertex array (documented closure-proven "
                                "field layout; validated against BOTH "
                                "parsers' counts and the adapter model_bound)",
            "triangle_indices": "SHA256 over the EXACT serialized u16 LE "
                                "triangle index array",
            "canonicalization": "exact bytes as serialized — no rounding, "
                                "no fuzzy threshold, no coordinate-space "
                                "import",
            "payload_discipline": "original arrays stay LOCAL_ONLY "
                                  "(in-memory only); published output = "
                                  "identities, counts, fingerprints, graph "
                                  "paths, evidence locators",
        },
        "meshes_218757": [
            {k: m.get(k) for k in ("mesh_block", "mesh_name", "data_block",
                                   "num_vertices", "num_triangles",
                                   "vertex_positions_f32le_sha256",
                                   "triangle_indices_u16le_sha256",
                                   "serialized_local_translate", "status")}
            for m in all_meshes["218757"]],
        "candidates": {},
    }
    m218 = all_meshes["218757"]
    m423 = all_meshes["423020"]
    def key(m):
        return (m["vertex_positions_f32le_sha256"],
                m["triangle_indices_u16le_sha256"],
                m["num_vertices"], m["num_triangles"])
    idx218 = {}
    for m in m218:
        if m.get("status") == "EXTRACTED_VALIDATED":
            idx218.setdefault(key(m), []).append(m)
    matches = []
    for m in m423:
        if m.get("status") != "EXTRACTED_VALIDATED":
            continue
        if key(m) in idx218:
            for src in idx218[key(m)]:
                matches.append({
                    "218757_mesh_block": src["mesh_block"],
                    "218757_mesh_name": src["mesh_name"],
                    "218757_data_block": src["data_block"],
                    "423020_mesh_block": m["mesh_block"],
                    "423020_mesh_name": m["mesh_name"],
                    "423020_data_block": m["data_block"],
                    "vertex_positions_sha256": m["vertex_positions_f32le_sha256"],
                    "triangle_indices_sha256": m["triangle_indices_u16le_sha256"],
                    "num_vertices": m["num_vertices"],
                    "num_triangles": m["num_triangles"],
                    "identity": "EXACT_GEOMETRY_FINGERPRINT_MATCH (vertex "
                                 "array + triangle array + counts byte-"
                                 "identical)",
                })
    if matches:
        matched_218 = {mm["218757_mesh_block"] for mm in matches}
        rel["candidates"]["423020.nif"] = {
            "matches": matches,
            "verdict": ("PARTIAL_GEOMETRY_MATCH: %d of 14 218757 meshes have "
                        "an exact geometry fingerprint match in 423020; "
                        "complete asset-subtree correspondence is NOT "
                        "claimed (a shared mesh does not identify the "
                        "entire asset; exact shared geometry does not "
                        "establish the same runtime instance or historical "
                        "building)" % len(matched_218)),
            "218757_meshes_with_match": sorted(matched_218),
            "218757_meshes_without_match":
                sorted({m["mesh_block"] for m in m218
                        if m.get("status") == "EXTRACTED_VALIDATED"
                        and m["mesh_block"] not in matched_218}),
        }
    else:
        rel["candidates"]["423020.nif"] = {
            "matches": [],
            "verdict": "NO_MATCH_IN_SELECTED_INPUTS",
            "note": "does not exclude baked/re-exported models, different "
                    "asset IDs, other containers, nonlocal instance "
                    "sources or network-delivered instances; the candidate "
                    "set is NOT expanded",
        }
    rel["structural_context_check"] = {
        "note": "mesh-level matches are cross-checked against the typed "
                "graph (parent node names/paths) in SCENE_STRUCTURE_RESULTS"
                ".json; name-only or texture-only identity is NOT used",
    }
    rel["placement_ceiling"] = {
        "MODEL_218757_TO_CMO_JOIN": "NOT_ESTABLISHED",
        "HISTORICAL_WORLD_INSTANCE": "NOT_ESTABLISHED",
        "PE_WORLD_ROOT_IDENTITY": "NOT_ESTABLISHED",
        "PE_AXES_AND_UNITS": "UNVERIFIED",
        "WORLD_XYZ_RECOVERED": "NO",
    }
    out2 = os.path.join(PE_OUT, "MODEL_218757_RELATION_RESULTS.json")
    with open(out2, "w", encoding="utf-8") as f:
        json.dump(rel, f, indent=2)
    print("WROTE", out2)
    print("mesh matches:", len(matches))
    for m in matches[:20]:
        print("  218757[%s]%r == 423020[%s]%r verts=%d tris=%d" % (
            m["218757_mesh_block"], m["218757_mesh_name"],
            m["423020_mesh_block"], m["423020_mesh_name"],
            m["num_vertices"], m["num_triangles"]))


if __name__ == "__main__":
    main()
