# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - T2d: node allocators + value+0x74 origin.
# FUN_00854D90 path1 alloc = FUN_00851610(&key, bucket, key), path2 = FUN_00854260(key).
# Dump both + FUN_00855ee0 (rehash) + the ctor calls that fill value+0x74/+0x78.
# Also decode exact targets of calls inside FUN_00528E50 (ClientMovableObject ctor).
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
    ("node_alloc_path1_FUN_00851610", 0x00851610, 0x100),
    ("node_alloc_path2_FUN_00854260", 0x00854260, 0xC0),
    ("rehash_FUN_00855ee0", 0x00855EE0, 0x120),
    ("ctor_derived_FUN_00528E50", 0x00528E50, 0x230),
]

def calls_in(pe, start, length):
    out = []
    b = pe.read_va(start, length) or b""
    for i in range(len(b) - 5):
        if b[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", b, i + 1)[0]
            t = start + i + 5 + rel
            out.append({"op": "E8" if b[i] == 0xE8 else "E9",
                        "site_va": "0x%08X" % (start + i),
                        "target": "0x%08X" % t})
    return out

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T2d_node_alloc", "measured": {}, "errors": []}
    m = res["measured"]
    for name, va, ln in DUMPS:
        m["hex_" + name] = hexdump(pe, va, ln)
        m["edges_" + name] = calls_in(pe, va, ln)
    with open(os.path.join(OUT, "T2D_NODE_ALLOC.json"), "w") as f:
        json.dump(res, f, indent=2)
    # readable dumps
    dst = os.path.join(OUT, "T2D_HEX")
    if not os.path.isdir(dst):
        os.makedirs(dst)
    for k, v in m.items():
        if k.startswith("hex_"):
            with open(os.path.join(dst, k[4:] + ".txt"), "w") as f:
                f.write(v)
    print("T2d done")
    for k, v in m.items():
        if k.startswith("edges_"):
            print(k)
            for e in v:
                print("   %s @%s -> %s" % (e["op"], e["site_va"], e["target"]))

if __name__ == "__main__":
    main()
