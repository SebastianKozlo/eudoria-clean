#!/usr/bin/env python3
"""Calibration probe 2: per-block-type name dump for a handful of K1 files.
READ-ONLY. Distinguishes NiTriShape names from NiMaterialProperty names."""
import sys
import os
import csv
import json
import struct

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
K1_TABLE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW"
            r"\ARKTEXTURE_ID_TABLE.csv")
R61_SRC = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"


def main():
    sys.path.insert(0, R61_SRC)
    from pe_nif_reader import PENifReader

    fs = os.path.getsize(MODELS_BNT)
    with open(MODELS_BNT, "rb") as f:
        f.seek(fs - 8)
        footer = f.read(8)
    istart = struct.unpack_from("<I", footer, 0)[0]
    with open(MODELS_BNT, "rb") as f:
        f.seek(istart)
        idx = f.read(fs - 8 - istart)
    count = struct.unpack_from("<I", idx, 0)[0]
    pos = 4
    entries = {}
    for i in range(count):
        ne = pos
        while idx[ne] != 0x0A:
            ne += 1
        name = idx[pos:ne].decode("ascii")
        size, off = struct.unpack_from("<II", idx, ne + 1)
        entries[name] = (size, off)
        pos = ne + 17

    rows = list(csv.DictReader(open(K1_TABLE, encoding="utf-8")))
    k1_names = {}
    for r in rows:
        k1_names.setdefault(r["nif"], []).append(r["name"])

    targets = ["505775.nif", "508326.nif", "52555.nif", "425247.nif"]
    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    reader = PENifReader()
    out = {}
    for t in targets:
        size, off = entries[t]
        res = reader.parse_bytes(data[off:off + size], source_name=t)
        dump = []
        for b in res.blocks:
            fld = b.fields or {}
            nm = fld.get("name")
            if b.block_type in ("NiTriShape", "NiMaterialProperty", "NiNode",
                                "NiTexturingProperty"):
                dump.append({"block_index": b.block_index,
                             "type": b.block_type, "name": nm})
        out[t] = {"version": res.version_string,
                  "k1_entry_names": k1_names.get(t, [])[:14],
                  "name_bearing_blocks": dump[:24]}
    with open(os.path.join(RUN, "00_CONTROL", "CALIBRATION_PROBE2.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for t in targets:
        print("==", t, out[t]["version"])
        for d in out[t]["name_bearing_blocks"][:14]:
            print("   ", d["block_index"], d["type"], repr(d["name"]))
        print("   K1 names:", out[t]["k1_entry_names"][:8])


if __name__ == "__main__":
    main()
