# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S11b PORTALS.BNT index parser (calibrated)
# Calibrated from raw bytes: footer = [int32 index_offset]['BNT2'] at EOF;
# index entries = {name until 0x0A, int32 size, int32 offset, int64 aux} x276.
# Lists all .prt entries, verifies contract samples, hex-dumps 6 samples.

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
    # footer
    assert data[size-4:] == b"BNT2", "footer BNT2 missing"
    index_start = struct.unpack_from("<i", data, size - 8)[0]
    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S11b_portals_index_calibrated",
        "file_size": size,
        "read_only": True,
        "index_start": index_start,
    }
    entries = []
    pos = index_start
    n = 0
    while pos < size - 8:
        end = data.find(b"\x0a", pos)
        if end < 0:
            break
        name = data[pos:end].decode("ascii", "replace")
        esz, eoff = struct.unpack_from("<ii", data, end + 1)
        aux = struct.unpack_from("<q", data, end + 9)[0]
        entries.append({"name": name, "size": esz, "offset": eoff, "aux": aux})
        pos = end + 17
        n += 1
    result["entries_count"] = len(entries)
    result["aux_lo_dwords"] = sorted(set(e["aux"] & 0xFFFFFFFF for e in entries))[:5]
    result["aux_hi_dwords"] = sorted(set((e["aux"] >> 32) & 0xFFFFFFFF for e in entries))[:5]

    prts = [e for e in entries if e["name"].endswith(".prt")]
    result["prt_count"] = len(prts)
    result["non_prt"] = [e["name"] for e in entries if not e["name"].endswith(".prt")]

    # boundary invariants (fail-closed):
    inv = []
    for e in entries:
        if not (0 <= e["offset"] <= index_start):
            inv.append({"name": e["name"], "offset": e["offset"], "why": "offset beyond index start"})
        if e["offset"] + e["size"] > index_start:
            inv.append({"name": e["name"], "why": "payload overlaps index"})
    result["boundary_violations"] = inv[:20]
    result["boundary_violations_count"] = len(inv)

    # name id map
    idmap = {}
    for e in prts:
        try:
            idmap[int(e["name"].split(".")[0])] = e
        except:
            pass
    result["id_count"] = len(idmap)
    ids = sorted(idmap)
    result["id_min"] = ids[0] if ids else None
    result["id_max"] = ids[-1] if ids else None

    # contract samples
    samples_wanted = list(range(505000, 510001)) + [382811, 422806, 592739, 592741]
    found = {}
    missing = []
    for i in samples_wanted:
        if i in idmap:
            found[i] = idmap[i]
        else:
            missing.append(i)
    result["wanted_range_found"] = sorted(k for k in found if 505000 <= k <= 510000)
    result["wanted_outliers_found"] = sorted(k for k in found if k in (382811, 422806, 592739, 592741))
    result["wanted_missing_count"] = len(missing)
    result["wanted_missing_first20"] = missing[:20]

    # hex dump 6 samples: first found in range, first outlier, smallest, largest
    dumps = []
    dump_ids = []
    in_range = [k for k in sorted(found) if 505000 <= k <= 510000]
    if in_range:
        dump_ids += in_range[:3]
    dump_ids += [k for k in (382811, 422806, 592739, 592741) if k in found][:3]
    for i in dump_ids[:6]:
        e = found[i]
        off, sz = e["offset"], e["size"]
        payload = data[off:off + min(sz, 96)]
        dumps.append({
            "id": i, "name": e["name"], "size": sz, "offset": off,
            "head_hex": payload.hex(),
            "u16_le_first16": [struct.unpack_from("<H", payload, o)[0] for o in range(0, min(len(payload), 32), 2)],
            "u32_le_first8": [struct.unpack_from("<I", payload, o)[0] for o in range(0, min(len(payload), 32), 4)],
            "f32_le_first8": [struct.unpack_from("<f", payload, o)[0] for o in range(0, min(len(payload), 32), 4)],
            "f32_finite": all(math.isfinite(f) for f in [struct.unpack_from("<f", payload, o)[0] for o in range(0, min(len(payload), 32), 4)]),
        })
    result["sample_dumps"] = dumps

    # prt size distribution
    sizes = sorted(e["size"] for e in prts)
    result["prt_size_min"] = sizes[0] if sizes else None
    result["prt_size_median"] = sizes[len(sizes)//2] if sizes else None
    result["prt_size_max"] = sizes[-1] if sizes else None

    with open(os.path.join(OUT, "S11B_PORTALS_INDEX.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("entries:", len(entries), "prt:", len(prts))
    print("range 505000-510000 found:", len(result["wanted_range_found"]), "of 1001")
    print("outliers found:", result["wanted_outliers_found"])
    print("missing (first 20):", result["wanted_missing_first20"])
    print("prt size min/med/max:", result["prt_size_min"], result["prt_size_median"], result["prt_size_max"])
    print("boundary violations:", result["boundary_violations_count"])

if __name__ == "__main__":
    main()
