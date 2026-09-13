# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S9 BYTE-VERIFY census call-sites + 0x70D17 check
# 1) Read raw bytes at each of the 25 lookup + 13 pump call-site VAs and compare
#    with the previous-run census bytes (raw-byte agreement control).
# 2) Data-level: does "460563.nif" exist in Models.bnt? (hardcoded 0x70D17 pump
#    caller FUN_0093be20). Scan BNT2 name index region.
# Writes: 01_RAW/S9_BYTE_VERIFY.json

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"

def va_to_file(va):
    if 0x00401000 <= va < 0x00A75000:
        return 4096 + (va - 0x00401000)
    if 0x00A75000 <= va < 0x00B6C000:
        return 6770688 + (va - 0x00A75000)
    return None

def main():
    data = open(EXE, "rb").read()
    prev = json.load(open(os.path.join(
        r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
        "01_RAW", "ghidra_output", "S10_LOOKUP_CALLERS.json")))["callers_of_0072f580"]
    prev2 = json.load(open(os.path.join(
        r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
        "01_RAW", "ghidra_output", "S20_MODEL_REQUEST_CALLERS.json")))["callers_of_006c9700"]

    res = {"lookup_25": [], "pump_13": [], "mismatches": 0}
    for rec in prev:
        va = int(rec["from_va"], 16)
        off = va_to_file(va)
        raw = " ".join("%02x" % b for b in data[off:off+5])
        ok = raw == rec["bytes"]
        if not ok:
            res["mismatches"] += 1
        res["lookup_25"].append({"va": rec["from_va"], "in_function": rec["in_function"],
                                 "census_bytes": rec["bytes"], "raw_bytes": raw, "match": ok})
    for rec in prev2:
        va = int(rec["from_va"], 16)
        off = va_to_file(va)
        raw = " ".join("%02x" % b for b in data[off:off+5])
        ok = raw == rec["bytes"]
        if not ok:
            res["mismatches"] += 1
        res["pump_13"].append({"va": rec["from_va"], "in_function": rec["in_function"],
                               "census_bytes": rec["bytes"], "raw_bytes": raw, "match": ok})

    # data check: 460563.nif in Models.bnt name table
    md = open(MODELS, "rb").read()
    targets = [b"460563.nif\x00", b"460563.nif\n", b"296445.nif\x00", b"460564.nif\x00"]
    data_hits = {}
    for t in targets:
        name = t.rstrip(b"\x00\n").decode()
        pos = md.find(t)
        cnt = 0
        first = pos
        p = pos
        while p >= 0:
            cnt += 1
            p = md.find(t, p + 1)
        data_hits[name] = {"first_offset": first, "count": cnt}
    res["models_bnt_name_check"] = data_hits

    with open(os.path.join(OUT, "S9_BYTE_VERIFY.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("S9_DONE lookup=%d pump=%d mismatches=%d" % (
        len(res["lookup_25"]), len(res["pump_13"]), res["mismatches"]))
    for k, v in data_hits.items():
        print("  %s: first=%s count=%d" % (k, v["first_offset"], v["count"]))

if __name__ == "__main__":
    main()
