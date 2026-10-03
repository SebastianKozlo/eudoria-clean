#!/usr/bin/env python3
# e2_our_decoder.py -- OUR decoder side for the E2 comparison (G-CMP-1).
#
# DECODER IDENTITY (pinned): the audited FIELD_IDENTITY_V2 lineage from
# PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (READ-ONLY import; nothing in
# that package is modified): s14_world_slice_validator_fieldidentity_v2.py
# (sha256 464D07E5203A8BA1D95ED1B3A5B94C6A932A8AABF979903490C893DD94293C04)
# which subclasses s06_world_slice_validator.py (sha256 51AC25406DF00F3A1EED
# 79E6573C779733FC1F95696EE045CE1C27202767BBC0) -> SchemaDecoderV2 with the
# occurrence-preserving field list (FIELD_IDENTITY_V2; s13_schema_field_
# identity_v2.py sha256 E3368507FCA5E9FDAE2AEADC1F9A55137DAEE242FBBDB5F4100
# 27C64455B4893 defines the identity model). The schema source is the pinned
# nifxml historical 0.7.1.1 (loaded by s04_nifxml_baseline.HIST). The decoder
# is a NIF 10.1.0.0 specialist: files of other versions fail closed.
#
# Output: canonical OUR-side JSON per T (see adapters/compare/adapter.py).

import json
import os
import sys

ROSETTA = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
           r"\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\00_CONTROL\scripts")
sys.path.insert(0, ROSETTA)

import hashlib  # noqa: E402


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


SCRIPTS = {
    "s14_world_slice_validator_fieldidentity_v2.py": None,
    "s06_world_slice_validator.py": None,
    "s04_nifxml_baseline.py": None,
    "s13_schema_field_identity_v2.py": None,
}
for name in SCRIPTS:
    p = os.path.join(ROSETTA, name)
    SCRIPTS[name] = _sha(p)

from s14_world_slice_validator_fieldidentity_v2 import (  # noqa: E402
    WorldSliceValidatorV2)


def _link(v):
    """nifxml Ref/Ptr i32 (-1 = null) -> int | None."""
    if v is None:
        return None
    if isinstance(v, list):
        return [None if (x == -1 or x == 0xFFFFFFFF) else x for x in v]
    if v == -1 or v == 0xFFFFFFFF:
        return None
    return v


def canonical(path):
    with open(path, "rb") as fh:
        data = fh.read()
    out = {
        "schema": "our_decoder_result@1.0",
        "decoder_identity": {
            "lineage": "FIELD_IDENTITY_V2 (SchemaDecoderV2 occurrence-"
                      "preserving field list; s13 identity model)",
            "scripts": SCRIPTS,
            "imported_read_only": True,
            "schema_source": "nifxml historical 0.7.1.1 (s04 HIST pin)",
        },
        "input_identity": {
            "path": os.path.abspath(path),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest().upper(),
            "nif_version": "10.1.0.0-specialist decoder (other versions "
                           "fail closed)",
        },
        "parse": {"accepted": False, "error": None},
        "num_blocks": None,
        "top_objects": [],
        "blocks": [],
        "scene_graph": {"roots": [], "edges": []},
        "controllers": [],
        "properties": [],
        "textures": [],
        "warnings": [],
    }
    nl = data.find(b"\x0a")
    if 0 < nl <= 128:
        out["input_identity"]["header"] = data[:nl].decode("latin-1")
        import struct
        if len(data) >= nl + 5:
            (v,) = struct.unpack("<I", data[nl + 1:nl + 5])
            out["input_identity"]["nif_version"] = "%d.%d.%d.%d" % (
                (v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF)
    try:
        v = WorldSliceValidatorV2()
        res = v.decode_file(data)
    except Exception as e:  # noqa: BLE001 -- fail-closed, recorded
        out["parse"]["error"] = "%s: %s" % (type(e).__name__, e)
        return out
    out["parse"]["accepted"] = True
    out["num_blocks"] = res["num_blocks"]
    out["top_objects"] = res["top_objects"]
    out["scene_graph"]["roots"] = res["top_objects"]
    blocks = []
    for b in res["blocks"]:
        if b is None:
            continue
        t = b.get("__type__")
        cb = {
            "index": None,  # assigned below in block order
            "type": t,
            "byte_start": b.get("__start__"),
            "byte_end": b.get("__end__"),
            "status": "decoded",
            "name": b.get("Name"),
        }
        if b.get("__decision__") is not None:
            cb["boundary_method"] = "ark_byte_search (closure-constrained; " \
                                    "s06 ark_candidates)"
        if "Translation" in b:
            rot = b.get("Rotation")
            cb["local_transform"] = {
                "translate": b.get("Translation"),
                "rotate": rot,
                "scale": b.get("Scale"),
            }
        if "Children" in b:
            kids = _link(b.get("Children") or [])
            cb["links"] = {"children": kids}
        if "Property List" in b:
            cb.setdefault("links", {})["properties"] = _link(
                b.get("Property List") or [])
        if "Extra Data List" in b:
            cb.setdefault("links", {})["extra_data"] = _link(
                b.get("Extra Data List") or [])
        if "Controller" in b:
            cb.setdefault("links", {})["controller"] = _link(
                b.get("Controller"))
        if "Data" in b:
            cb.setdefault("links", {})["model_data"] = _link(b.get("Data"))
        for k_src, k_dst in (("Num Vertices", "num_vertices"),
                             ("Num Triangles", "num_triangles"),
                             ("Has Normals", "has_normals")):
            if k_src in b:
                cb[k_dst] = b.get(k_src)
        if "Num UV Sets" in b:
            cb["num_texture_sets"] = b.get("Num UV Sets")
        elif "Num Texture Sets" in b:
            cb["num_texture_sets"] = b.get("Num Texture Sets")
        if "Bounding Volume" in b:
            bv = b.get("Bounding Volume") or {}
            cb["model_bound"] = {
                "center": bv.get("Center"),
                "radius": bv.get("Radius"),
                "semantics": "MODEL_SPACE serialized NiGeometryData bound",
            }
        if "File Name" in b:
            cb["filename"] = b.get("File Name")
        if t and t.endswith("Property"):
            out["properties"].append({"index": None, "type": t,
                                      "name": b.get("Name")})
        if t and (t.endswith("Controller")):
            out["controllers"].append({
                "index": None, "type": t,
                "target": (_link(b.get("Target")) if b.get("Target") is not
                           None else None)})
        if t in ("NiSourceTexture", "NiTexture"):
            out["textures"].append({"index": None, "type": t,
                                    "filename": b.get("File Name")})
        blocks.append(cb)
    for i, cb in enumerate(blocks):
        cb["index"] = i
        if cb["type"] == "NiNode":
            for c in (cb.get("links", {}).get("children") or []):
                if isinstance(c, int):
                    out["scene_graph"]["edges"].append(
                        {"parent": i, "child": c, "field": "children"})
    for e in out["controllers"] + out["properties"] + out["textures"]:
        # resolve by position: find the block with same type occurrence order
        e["index"] = next((b["index"] for b in blocks
                          if b["index"] >= (e.get("index") or 0) and
                          b["type"] == e["type"]), None)
    # fix controller/property/texture indices deterministically: match by
    # the n-th block of that type
    counters = {}
    for b in blocks:
        counters.setdefault(b["type"], []).append(b["index"])
    for e in out["controllers"] + out["properties"] + out["textures"]:
        lst = counters.get(e["type"], [])
        # order of append matches block order
        e["index"] = lst[len([x for x in out["controllers"] +
                              out["properties"] + out["textures"]
                              if x["type"] == e["type"] and
                              x["index"] is None])] if lst else None
    # simpler deterministic fix: assign by occurrence
    seen = {}
    for e in out["controllers"] + out["properties"] + out["textures"]:
        n = seen.get(e["type"], 0)
        lst = counters.get(e["type"], [])
        e["index"] = lst[n] if n < len(lst) else None
        seen[e["type"]] = n + 1
    out["blocks"] = blocks
    out["warnings"].append("our decoder is a 10.1.0.0 specialist; block "
                           "indices are 0-based LoadBinary order (GroupID "
                           "framing per s06, gid==0 PE invariant)")
    return out


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    result = canonical(src)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1)
        fh.write("\n")
    print("%s: accepted=%s blocks=%s error=%r" %
           (os.path.basename(src), result["parse"]["accepted"],
            result["num_blocks"], result["parse"]["error"]))
