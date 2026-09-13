# -*- coding: utf-8 -*-
# FUN_006B4C50 full call-map + FUN_00772840/00772870 bodies decode.
# Output: 01_RAW/F1_BODYSET_CALLMAP.json + F1_CTX6_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F1_bodyset_callmap", "measured": {}, "errors": []}

NAMES = {
    0x007CE1E0: "getter_A(+8)", 0x006C22D0: "getter_C(+0xC)", 0x00746550: "getter_B(+4)",
    0x0048ADA0: "getter_D(+0x10)", 0x0072F580: "lookup_registry", 0x006C2840: "slot_table_getter_2840",
    0x006C2870: "slot_table_getter_2870", 0x006C9700: "pump_model", 0x0043A550: "idmapper_0043A550",
    0x00772840: "FUN_00772840", 0x00772870: "FUN_00772870",
    0x0040DE60: "cursor_0040de60", 0x00730CE6: "parser_A_store",
}

# full body of FUN_006B4C50
fend, fbody = pe.func_body(0x006B4C50, 0x800)
base = 0x006B4C50
calls = []
for i in range(len(fbody) - 5):
    if fbody[i] == 0xE8:
        rel = struct.unpack_from("<i", fbody, i + 1)[0]
        t = base + i + 5 + rel
        calls.append({"at": "0x%08X" % (base + i), "target": "0x%08X" % t,
                      "name": NAMES.get(t, "")})
res["measured"]["FUN_006B4C50_calls"] = {"body_size": len(fbody), "calls": calls}
res["measured"]["FUN_006B4C50_end"] = "0x%08X" % fend if fend else None

with open(os.path.join(OUT, "F1_BODYSET_CALLMAP.json"), "w") as f:
    json.dump(res, f, indent=2)


def dump(name, va, n):
    with open(os.path.join(OUT, "F1_CTX6_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")


dump("FUN_00772840", 0x00772840, 0x60)
dump("FUN_00772870", 0x00772870, 0x60)
dump("BODYSET_006B4C50_FULL", 0x006B4C50, min(len(fbody), 0x290))

print("body size:", len(fbody), "end:", res["measured"]["FUN_006B4C50_end"])
for c in calls:
    print("%s -> %s %s" % (c["at"], c["target"], c["name"]))
