# -*- coding: utf-8 -*-
# F2 — FUN_008553D0 full call map + walker-init identification.
# Also dump FUN_0085B190, FUN_004154F0, FUN_008454D0, FUN_00843D60 heads.
# Output: 01_RAW/F2_CALLMAP.json + F2_CTX3_*.txt

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
res = {"stage": "F2_callmap", "measured": {}, "errors": []}

NAMES = {
    0x007CE1E0: "getter_A(+8)", 0x0048ADA0: "getter_D(+0x10)",
    0x0085B840: "walker_resolve", 0x0085B860: "walker_current",
    0x00843D60: "walker_init_00843d60", 0x008454D0: "resolver_008544d0",
    0x004154F0: "singleton_004154f0", 0x0085B190: "walker_next_0085b190",
    0x008599A0: "FUN_008599a0", 0x0085B1A0: "walker_dtor_0085b1a0",
    0x00415570: "FUN_00415570",
}

fend, fbody = pe.func_body(0x008553D0, 0x2000)
base = 0x008553D0
calls = []
for i in range(len(fbody) - 5):
    if fbody[i] == 0xE8:
        rel = struct.unpack_from("<i", fbody, i + 1)[0]
        t = base + i + 5 + rel
        calls.append({"at": "0x%08X" % (base + i), "target": "0x%08X" % t,
                      "name": NAMES.get(t, "")})
res["measured"]["FUN_008553D0_calls"] = {"body_size": len(fbody), "end": "0x%08X" % fend, "calls": calls}

# preceding-2-bytes for walker calls: what LEA ECX setup precedes FUN_00843D60/0085B840 calls
with open(os.path.join(OUT, "F2_CALLMAP.json"), "w") as f:
    json.dump(res, f, indent=2)


def dump(name, va, n):
    with open(os.path.join(OUT, "F2_CTX3_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")


for va, n in ((0x0085B190, 0x60), (0x004154F0, 0x40), (0x008454D0, 0x80), (0x00843D60, 0xC0)):
    dump("FUN_%08X" % va, va, n)

print("body:", len(fbody), "end:", "0x%08X" % fend)
for c in calls:
    print("%s -> %s %s" % (c["at"], c["target"], c["name"]))
