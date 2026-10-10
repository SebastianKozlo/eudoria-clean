#!/usr/bin/env python3
"""QC DUTY 5 — independent block census of the extracted 218757.nif.

Fresh internal QC (pe-master-auditor). My OWN minimal NIF 10.1 header reader:
reads the header line, version, user version, block-type table, num blocks,
and the top-level group count. Then cross-checks the executor's parser output
(PE_218757.inspect_full.json): recounts semantically_decoded vs boundary_only
blocks from the parser's per-block records, and validates the 62+4/66 ceiling.
Read-only against all inputs.
"""
import json
import struct
import sys

NIF = ("D:/Eudoria_Reconstruction/99_Audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "02_PE_payloads/218757.nif")
INSPECT_FULL = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/"
                "audits/PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_"
                "20261009/02_PE/raw/PE_218757.inspect_full.json")
BLOCKMAP = ("D:/Eudoria_Reconstruction/99_Audits/"
            "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
            "02_PE_work/NIF101_BLOCKMAP_218757_R1.json")
OUT = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "00_CONTROL_INTERNAL_QC/q5_218757_block_census.json")

data = open(NIF, "rb").read()
res = {"input": NIF, "size": len(data)}


def rd_u32(off):
    return struct.unpack_from("<I", data, off)[0]


def rd_string(off):
    # NIF 10.1 string: u32 length + bytes (length incl. terminator)
    n = rd_u32(off)
    s = data[off + 4: off + 4 + n - 1].decode("ascii")
    return s, off + 4 + n


# header line
hdr_end = data.index(b"\x0A")
header_line = data[:hdr_end].decode("ascii")
res["header_line"] = header_line
p = hdr_end + 1
ver = rd_u32(p); p += 4
res["version_u32"] = ver
res["version"] = "%d.%d.%d.%d" % (ver >> 24 & 0xFF, ver >> 16 & 0xFF,
                                  ver >> 8 & 0xFF, ver & 0xFF)
# user version (>= 10.0.1.8 per NiStream.cpp:335)
uver = rd_u32(p); p += 4
res["user_version_u32"] = uver
# numObjects (u32) — NiStream.cpp:355-357 LoadHeader
num_blocks = rd_u32(p); p += 4
res["num_blocks_declared"] = num_blocks
# RTTI count (u16) — NiStream.cpp:414-415 LoadRTTI
num_types = struct.unpack_from("<H", data, p)[0]; p += 2
res["num_types"] = num_types
# RTTI strings: u32 length + exactly that many chars, NO terminator
# (NiStream.cpp:1142-1153 LoadRTTIString)
types = []
for _ in range(num_types):
    n = rd_u32(p)
    s = data[p + 4: p + 4 + n].decode("ascii")
    types.append(s)
    p += 4 + n
res["type_table"] = types
# block type indices: num_blocks x u16 — NiStream.cpp:436-444
type_idx = []
for i in range(num_blocks):
    ti = struct.unpack_from("<H", data, p)[0]
    type_idx.append(types[ti] if ti < num_types else f"OOB({ti})")
    p += 2
res["block_type_sequence"] = type_idx
from collections import Counter
res["block_type_census"] = dict(Counter(type_idx))
res["header_parse_end_offset"] = p
res["block_bodies_region_bytes"] = len(data) - p

# executor parser recount
inf = json.load(open(INSPECT_FULL, "r", encoding="utf-8"))


def find_blocks(obj, out):
    if isinstance(obj, dict):
        if "objects" in obj and isinstance(obj["objects"], list):
            out.extend(obj["objects"])
        for v in obj.values():
            find_blocks(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_blocks(v, out)


blocks = []
find_blocks(inf, blocks)
res["parser_full_json_objects_found"] = len(blocks)
status_counts = Counter()
semantic, boundary = [], []
for b in blocks:
    if b.get("status") == "UNREGISTERED_IN_GB12_FACTORY":
        boundary.append(b)
        status_counts["UNREGISTERED_IN_GB12_FACTORY (boundary-only)"] += 1
    elif "local_transform" in b or "name" in b:
        semantic.append(b)
        status_counts["semantic (decoded fields present)"] += 1
    else:
        status_counts["other"] += 1
res["parser_status_counts"] = dict(status_counts)
res["parser_semantic_count"] = len(semantic)
res["parser_boundary_only_count"] = len(boundary)
res["parser_semantic_types"] = dict(Counter(b["type"] for b in semantic))
res["parser_boundary_types"] = [b["type"] for b in boundary]

bm = json.load(open(BLOCKMAP, "r", encoding="utf-8"))
res["blockmap_top_keys"] = list(bm.keys())[:20] if isinstance(bm, dict) else type(bm).__name__
bm_blocks = []
find_blocks(bm, bm_blocks)
res["blockmap_objects_found"] = len(bm_blocks)
bm_types = Counter()
for b in bm_blocks:
    t = b.get("type") or b.get("class_name") or "?"
    bm_types[t] += 1
res["blockmap_type_counts"] = dict(bm_types)

# census verdict
declared = res["num_blocks_declared"]
ceiling_ok = (declared == 66
              and res["parser_semantic_count"] == 62
              and res["parser_boundary_only_count"] == 4)
res["census_verdict"] = ("62+4/66 CEILING REPRODUCED" if ceiling_ok
                         else "MISMATCH — see details")

print(json.dumps(res, indent=2))
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
sys.exit(0)
