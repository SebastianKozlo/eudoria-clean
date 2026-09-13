# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S11 PORTALS.BNT census + .prt sample dump
# STATIC-ONLY, READ-ONLY on the original Portals.bnt.
# a) Parse the BNT2 index (known format: int32 StartOffset, 'BNT2', int32 numberOfFiles,
#    entries {name-until-0x0A, int32 size, int32 offset, int64 UNKNOWN}).
#    Calibrate the index layout from the actual bytes (scan for 'BNT2').
# b) List all .prt entries; verify the contract sample: entries with ids 505000-510000
#    + outliers 382811/422806/592739/592741.
# c) Hex-dump 6 sample .prt payloads (first 96 bytes) for structural decode against
#    the reader code (FUN_00852a30 byte-tag + FUN_00852750 u16/u32/f32 readers).

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
SRC = r"D:\Eudoria_Reconstruction\pcg_install\Data\Portals\Portals.bnt"

def main():
    data = open(SRC, "rb").read()
    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S11_portals_bnt_census",
        "file_size": len(data),
        "read_only": True,
    }

    # locate 'BNT2' occurrences
    bnt2_offs = []
    off = 0
    while True:
        off = data.find(b"BNT2", off)
        if off < 0:
            break
        bnt2_offs.append(off)
        off += 1
    result["bnt2_marker_offsets"] = bnt2_offs

    entries = []
    idx_off = None
    num_files = None
    # The index: [int32 StartOffset]['BNT2'][int32 numberOfFiles] then per entry:
    # name (zero-terminated... or 0x0A-terminated?), size, offset, (int64 unknown?)
    # Calibrate: parse from each BNT2 occurrence and validate against file size.
    for marker in bnt2_offs:
        try:
            start_ptr = struct.unpack_from("<i", data, marker - 4)[0]
            nfiles = struct.unpack_from("<i", data, marker + 4)[0]
        except:
            continue
        if not (0 < nfiles < 100000):
            continue
        # try entry layout A: name zero-terminated, then size, offset (no int64)
        # try entry layout B: name zero-terminated, size, offset, int64
        for layout in ("A_nul_term_szoff", "B_nul_term_szoff_i64"):
            pos = marker + 8
            parsed = []
            ok = True
            for i in range(nfiles):
                # name
                end = data.find(b"\x00", pos)
                if end < 0 or end - pos > 260:
                    ok = False
                    break
                name = data[pos:end].decode("ascii", "replace")
                pos = end + 1
                if layout.startswith("A"):
                    if pos + 8 > len(data):
                        ok = False
                        break
                    size, offset = struct.unpack_from("<ii", data, pos)
                    pos += 8
                else:
                    if pos + 16 > len(data):
                        ok = False
                        break
                    size, offset = struct.unpack_from("<ii", data, pos)
                    pos += 16
                parsed.append({"name": name, "size": size, "offset": offset})
            if ok and len(parsed) == nfiles:
                # validate: all offsets within file, names mostly .prt
                within = all(0 <= p["offset"] < len(data) and p["size"] >= 0 for p in parsed)
                prt_n = sum(1 for p in parsed if p["name"].endswith(".prt"))
                if within and prt_n >= nfiles * 0.5:
                    entries = parsed
                    idx_off = marker
                    num_files = nfiles
                    result["index_layout"] = layout
                    break
        if entries:
            break

    result["index_offset"] = idx_off
    result["num_files"] = num_files
    result["entries_count"] = len(entries)
    result["prt_count"] = sum(1 for e in entries if e["name"].endswith(".prt"))
    result["non_prt_entries"] = [e for e in entries if not e["name"].endswith(".prt")][:20]

    # size histogram of .prt
    prts = [e for e in entries if e["name"].endswith(".prt")]
    sizes = sorted(p["size"] for p in prts)
    result["prt_size_min"] = sizes[0] if sizes else None
    result["prt_size_max"] = sizes[-1] if sizes else None
    result["prt_size_median"] = sizes[len(sizes)//2] if sizes else None

    # sample: entries 505000-510000 (ids from filenames <id>.prt) + outliers
    def name_id(e):
        try:
            return int(e["name"].split(".")[0])
        except:
            return None
    sample = []
    want_range = list(range(505000, 510001))
    outliers = [382811, 422806, 592739, 592741]
    id_map = {}
    for e in prts:
        i = name_id(e)
        if i is not None:
            id_map[i] = e
    for i in want_range:
        if i in id_map:
            e = id_map[i]
            sample.append(e)
    for i in outliers:
        if i in id_map:
            sample.append(id_map[i])
        else:
            sample.append({"name": "%d.prt" % i, "missing": True})
    # also first/last entries for boundary checks
    result["sample_ids_found"] = [e.get("name") for e in sample]

    # hex-dump first 96 bytes of up to 6 found samples
    dumps = []
    for e in sample:
        if e.get("missing"):
            continue
        off = e["offset"]
        sz = e["size"]
        payload = data[off:off+min(sz, 96)]
        dumps.append({
            "name": e["name"], "size": e["size"], "offset": e["offset"],
            "head_hex": payload.hex(),
            "head_u16_le": [struct.unpack_from("<H", payload, o)[0] for o in range(0, min(len(payload), 32), 2)],
            "head_u32_le": [struct.unpack_from("<I", payload, o)[0] for o in range(0, min(len(payload), 32), 4)],
            "head_f32_le": [struct.unpack_from("<f", payload, o)[0] for o in range(0, min(len(payload), 32), 4)],
        })
    result["sample_dumps"] = dumps

    # finiteness control on the f32 interpretation of sample heads
    import math
    fin = []
    for d in dumps:
        for f in d["head_f32_le"]:
            fin.append(bool(math.isfinite(f)))
    result["sample_head_f32_finite_ratio"] = (sum(fin), len(fin))

    with open(os.path.join(OUT, "S11_PORTALS_BNT_CENSUS.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("bnt2 markers:", bnt2_offs)
    print("index layout:", result.get("index_layout"), "nfiles:", num_files,
          "prt:", result["prt_count"])
    print("sample found:", result["sample_ids_found"])
    print("prt size min/med/max:", result["prt_size_min"], result["prt_size_median"], result["prt_size_max"])

if __name__ == "__main__":
    main()
