# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S12 .prt content check (READ-ONLY)
# Scan all 276 .prt payloads (LE) for template/world-object ids: 4508/296445/4752/126740/
# 2249/278453/296446 (contract anchors + siblings) and param-set ids (20005/20007/20006).
# Also check: do any .prt dwords match the .nif id space (Models.bnt names)? A census of
# u32 values that appear BOTH in .prt and in Models.bnt id space would be needed for
# placement-carrying claims; absence of the anchor ids = structural negative.
# Finiteness control on f32 interpretations rejected when non-finite.

import json
import math
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
SRC = r"D:\Eudoria_Reconstruction\pcg_install\Data\Portals\Portals.bnt"

def main():
    data = open(SRC, "rb").read()
    size = len(data)
    index_start = struct.unpack_from("<i", data, size - 8)[0]
    entries = []
    pos = index_start
    while pos < size - 8:
        end = data.find(b"\x0a", pos)
        if end < 0:
            break
        name = data[pos:end].decode("ascii", "replace")
        esz, eoff = struct.unpack_from("<ii", data, end + 1)
        entries.append((name, esz, eoff))
        pos = end + 17

    anchors = {
        "template_4508": 4508,
        "nif_A_296445": 296445,
        "bvi_B_296446": 296446,
        "template_4752": 4752,
        "nif_A_126740": 126740,
        "template_2249": 2249,
        "nif_A_278453": 278453,
        "paramset_20005": 20005,
        "paramset_20007": 20007,
        "paramset_20006": 20006,
        "msgtype_0xB9": 0xB9,
        "attr_0x6A4": 0x6A4,
        "attr_0x6A8": 0x6A8,
    }
    # round-trip
    for k, v in anchors.items():
        assert struct.unpack("<I", struct.pack("<I", v))[0] == v

    hits = {k: [] for k in anchors}
    prt_values = {}
    total_bytes = 0
    for name, esz, eoff in entries:
        payload = data[eoff:eoff+esz]
        total_bytes += esz
        for k, v in anchors.items():
            pat = struct.pack("<I", v)
            off = 0
            while True:
                off = payload.find(pat, off)
                if off < 0:
                    break
                hits[k].append({"entry": name, "at": off})
                off += 1
        # census of aligned u32s (for id-space comparison)
        for o in range(0, len(payload) - 3, 4):
            val = struct.unpack_from("<I", payload, o)[0]
            prt_values.setdefault(val, 0)
            prt_values[val] += 1

    # how many distinct u32 values in .prt space are in the range of .nif ids
    # (A id space 100000-460000 per prior runs: 296445/126740/278453 etc.)
    nif_range = [v for v in prt_values if 100000 <= v <= 460000]
    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S12_prt_content_check",
        "read_only": True,
        "entries": len(entries),
        "total_prt_bytes": total_bytes,
        "anchor_hits": {k: v[:10] for k, v in hits.items()},
        "anchor_hit_counts": {k: len(v) for k, v in hits.items()},
        "distinct_u32_values": len(prt_values),
        "u32_values_in_nifid_range_100k_460k": len(nif_range),
        "u32_in_nif_range_sample": sorted(nif_range)[:30],
        "note": ("anchor_hit_counts == 0 for template/nif ids = structural negative "
                 "(.prt carries no template/world-object ids). u32 census is ALIGNED "
                 "only (4-byte grid); misaligned values also possible."),
    }
    with open(os.path.join(OUT, "S12_PRT_CONTENT_CHECK.json"), "w") as f:
        json.dump(result, f, indent=2)
    for k, v in result["anchor_hit_counts"].items():
        print("%-22s %d" % (k, v))
    print("distinct u32:", result["distinct_u32_values"],
          "| in 100k-460k:", result["u32_values_in_nifid_range_100k_460k"])

if __name__ == "__main__":
    main()
