# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 — TASK 2c: insert helper decode.
# FUN_004C46C0 (create ClientMovableObject from record+variant) calls:
#   FUN_00853A80 (after 1st mgr-getter, with 2 floats on stack)
#   FUN_00856190 (after ctor, with new object)  <- INSERT candidate
# Dump both + neighbors + callers census of FUN_004C46C0 / FUN_004C47F0.
# STATIC-ONLY.

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ID = "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

DUMPS = [
    ("insert_candidate_FUN_00856190", 0x00856190, 0x180),
    ("candidate_FUN_00853A80", 0x00853A80, 0x100),
    ("candidate_FUN_00853A50", 0x00853A50, 0x40),
    ("FUN_004C4640", 0x004C4640, 0x80),
    ("FUN_00797280", 0x00797280, 0x40),
    ("FUN_00765930", 0x00765930, 0x40),
    ("FUN_00856100", 0x00856100, 0x100),
    ("region_00856140_00856400", 0x00856140, 0x2C0),
]

CENSUS = {
    "FUN_004C46C0": 0x004C46C0,
    "FUN_004C47F0": 0x004C47F0,
    "FUN_00856190": 0x00856190,
    "FUN_00853A80": 0x00853A80,
    "FUN_00853A50": 0x00853A50,
    "FUN_00856100": 0x00856100,
}

def calls_all(pe, target_va):
    out = []
    tr = pe.text_raw
    base = pe.text_va_start
    for i in range(len(tr) - 5):
        if tr[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            t = base + i + 5 + rel
            if t == target_va:
                out.append({"op": "E8" if tr[i] == 0xE8 else "E9",
                            "site_va": "0x%08X" % (base + i)})
    return out

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T2c_insert_helper", "measured": {}, "errors": []}
    m = res["measured"]
    for name, va, ln in DUMPS:
        m["hex_" + name] = hexdump(pe, va, ln)
    for name, t in sorted(CENSUS.items()):
        m["census_" + name] = calls_all(pe, t)

    with open(os.path.join(OUT, "T2C_INSERT_HELPER.json"), "w") as f:
        json.dump(res, f, indent=2)

    print("T2c done.")
    for name, t in sorted(CENSUS.items()):
        print("  %-16s %d raw calls" % (name, len(m["census_" + name])))
        for c in m["census_" + name]:
            print("      %s @%s" % (c["op"], c["site_va"]))

if __name__ == "__main__":
    main()
