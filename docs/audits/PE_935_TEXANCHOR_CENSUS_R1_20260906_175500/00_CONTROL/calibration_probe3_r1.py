#!/usr/bin/env python3
"""Calibration probe 3 (full corpus, READ-ONLY): name-convention census.

Answers, BEFORE the method freeze:
 1. NiTriShape name formats corpus-wide: ':<digits>' suffix vs '_' vs plain.
 2. NiMaterialProperty non-empty name rate + formats.
 3. Per-entry OBSERVED resolution rates under BOTH readings:
    (i)  EXACT membership of the mesh-part in U = {NiTriShape names} U
         {NiMaterialProperty names} (as exposed by the frozen R61 parser);
    (ii) COLON-BRIDGE membership: mesh_part == u.replace(':','_') for some
         u in U (the 3ds Max multi-material separator convention).
 4. Slot column vs suffix agreement (full census).
Writes 00_CONTROL/CALIBRATION_PROBE3.json. No census outputs.
"""
import sys
import os
import csv
import json
import struct
import re
import hashlib
from collections import Counter

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA256 = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
K1_TABLE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW"
            r"\ARKTEXTURE_ID_TABLE.csv")
R61_SRC = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = (r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828"
                r"\03_validation\SHA256_SOURCE.json")

COLON_TAIL = re.compile(r":\d+$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    for name, sha in locked.items():
        if name.endswith(".py"):
            assert sha256_file(os.path.join(R61_SRC, name)).lower() == str(sha).lower()
    assert sha256_file(MODELS_BNT).lower() == MODELS_SHA256

    fs = os.path.getsize(MODELS_BNT)
    with open(MODELS_BNT, "rb") as f:
        f.seek(fs - 8)
        footer = f.read(8)
    istart = struct.unpack_from("<I", footer, 0)[0]
    assert footer[4:8] == b"BNT2"
    with open(MODELS_BNT, "rb") as f:
        f.seek(istart)
        idx = f.read(fs - 8 - istart)
    count = struct.unpack_from("<I", idx, 0)[0]
    assert count == 5596
    pos = 4
    entries = []
    for i in range(count):
        ne = pos
        while idx[ne] != 0x0A:
            ne += 1
        name = idx[pos:ne].decode("ascii")
        size, off = struct.unpack_from("<II", idx, ne + 1)
        entries.append((name, size, off))
        pos = ne + 17
    assert pos == len(idx)

    rows = list(csv.DictReader(open(K1_TABLE, encoding="utf-8")))
    assert len(rows) == 24508
    k1_by_file = {}
    for r in rows:
        k1_by_file.setdefault(r["nif"], []).append(r)

    sys.path.insert(0, R61_SRC)
    from pe_nif_reader import PENifReader
    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    reader = PENifReader()

    tri_fmt = Counter()
    mat_nonempty = 0
    mat_total = 0
    mat_fmt = Counter()
    n_exact = 0
    n_bridge = 0
    n_either = 0
    n_entries = 0
    n_slot_ok = 0
    bridge_examples = []
    miss_examples = []
    files_with_universe_empty = 0
    universe_sizes = []
    for name, size, off in entries:
        res = reader.parse_bytes(data[off:off + size], source_name=name)
        if res.parse_status != "PASS":
            continue
        uni = set()
        uni_bridge = set()
        for b in res.blocks:
            if b.block_type == "NiTriShape":
                nm = (b.fields or {}).get("name") or ""
                if COLON_TAIL.search(nm):
                    tri_fmt["colon_tail"] += 1
                elif nm:
                    tri_fmt["plain_or_underscore"] += 1
                else:
                    tri_fmt["empty"] += 1
                if nm:
                    uni.add(nm)
                    uni_bridge.add(nm.replace(":", "_"))
            elif b.block_type == "NiMaterialProperty":
                nm = (b.fields or {}).get("name") or ""
                mat_total += 1
                if nm:
                    mat_nonempty += 1
                    if COLON_TAIL.search(nm):
                        mat_fmt["colon_tail"] += 1
                    else:
                        mat_fmt["other"] += 1
                    uni.add(nm)
                    uni_bridge.add(nm.replace(":", "_"))
        if name in k1_by_file:
            universe_sizes.append(len(uni))
            if not uni:
                files_with_universe_empty += 1
            for r in k1_by_file[name]:
                n_entries += 1
                en = r["name"]
                if "_" in en:
                    mesh_part, suffix = en.rsplit("_", 1)
                else:
                    mesh_part, suffix = en, ""
                ex = mesh_part in uni
                br = mesh_part in uni_bridge
                if suffix == r["slot"]:
                    n_slot_ok += 1
                if ex:
                    n_exact += 1
                if br:
                    n_bridge += 1
                if ex or br:
                    n_either += 1
                    if len(bridge_examples) < 10:
                        bridge_examples.append(
                            {"nif": name, "entry": en, "mesh_part": mesh_part,
                             "mode": "exact" if ex else "bridge"})
                elif len(miss_examples) < 10:
                    miss_examples.append(
                        {"nif": name, "entry": en, "mesh_part": mesh_part,
                         "universe_head": sorted(uni)[:8]})

    out = {
        "era": "PCG_9_3_5",
        "entries": n_entries,
        "nitrishape_name_formats": dict(tri_fmt),
        "nimaterialproperty": {"total": mat_total, "nonempty": mat_nonempty,
                               "formats": dict(mat_fmt)},
        "exact_membership_resolutions": n_exact,
        "colon_bridge_resolutions": n_bridge,
        "either_resolutions": n_either,
        "slot_vs_suffix_agreements": n_slot_ok,
        "entry_bearing_files": len(universe_sizes),
        "files_with_empty_universe": files_with_universe_empty,
        "universe_size_mean": (sum(universe_sizes) / len(universe_sizes))
        if universe_sizes else None,
        "bridge_examples": bridge_examples,
        "miss_examples": miss_examples,
    }
    with open(os.path.join(RUN, "00_CONTROL", "CALIBRATION_PROBE3.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("miss_examples", "bridge_examples")},
                     indent=1))
    print("bridge examples:", json.dumps(bridge_examples[:6], indent=1))
    print("miss examples:", json.dumps(miss_examples[:4], indent=1)[:1200])


if __name__ == "__main__":
    main()
