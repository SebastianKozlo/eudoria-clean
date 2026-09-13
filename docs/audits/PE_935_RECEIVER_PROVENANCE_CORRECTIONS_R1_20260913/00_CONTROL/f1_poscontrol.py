# -*- coding: utf-8 -*-
# F1(d) positive control: templates.vfs record receiver chain from own bytes.
# (1) parser A read @0x00730CE6 (+0x08 into template object);
# (2) lookup FUN_0072F580 body;
# (3) FUN_006B4C50 getter call sites with ECX provenance;
# (4) FUN_006C3F50 emitter {0x66,A} getter site;
# (5) FUN_00567170 getter site provenance.
# Output: 01_RAW/F1_POSCONTROL.json + F1_CTX5_*.txt

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
res = {"stage": "F1_poscontrol", "measured": {}, "errors": []}


def dump(name, va, n):
    with open(os.path.join(OUT, "F1_CTX5_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")
    return pe.read_va(va, n)


# 1. parser A read @0x00730CE6 — context window
dump("PARSER_A_READ_00730CE6", 0x00730CB0, 0x80)

# 2. lookup FUN_0072F580 — full body (to first CC CC CC)
fend, fbody = pe.func_body(0x0072F580, 0x100)
res["measured"]["lookup_FUN_0072F580"] = {"entry": "0x0072F580", "size": len(fbody), "hex_head": fbody[:64].hex()}
dump("LOOKUP_0072F580", 0x0072F580, min(len(fbody), 0x100))

# 3. FUN_006B4C50: find CALL -> FUN_007CE1E0 sites inside its body
fend2, fbody2 = pe.func_body(0x006B4C50, 0x400)
sites = []
base = 0x006B4C50
for i in range(len(fbody2) - 5):
    if fbody2[i] == 0xE8:
        rel = struct.unpack_from("<i", fbody2, i + 1)[0]
        t = base + i + 5 + rel
        if t == 0x007CE1E0:
            sites.append("0x%08X" % (base + i))
res["measured"]["FUN_006B4C50_getter_sites"] = {"count": len(sites), "sites": sites}
dump("BODYSET_006B4C50", 0x006B4C50, min(len(fbody2), 0x300))

# 3b. FUN_006C2840/006C2870 slot-table getters (return the record)
for va in (0x006C2840, 0x006C2870):
    fendx, fbodyx = pe.func_body(va, 0x80)
    dump("SLOTGETTER_%08X" % va, va, min(len(fbodyx), 0x80))

# 4. FUN_006C3F50 emitter: getter site
fend3, fbody3 = pe.func_body(0x006C3F50, 0x200)
sites3 = []
for i in range(len(fbody3) - 5):
    if fbody3[i] == 0xE8:
        rel = struct.unpack_from("<i", fbody3, i + 1)[0]
        t = 0x006C3F50 + i + 5 + rel
        if t == 0x007CE1E0:
            sites3.append("0x%08X" % (0x006C3F50 + i))
res["measured"]["FUN_006C3F50_getter_sites"] = {"count": len(sites3), "sites": sites3}
dump("EMITTER_006C3F50", 0x006C3F50, min(len(fbody3), 0x180))

# 5. FUN_00567170: getter site + provenance
fend4, fbody4 = pe.func_body(0x00567170, 0x400)
sites4 = []
for i in range(len(fbody4) - 5):
    if fbody4[i] == 0xE8:
        rel = struct.unpack_from("<i", fbody4, i + 1)[0]
        t = 0x00567170 + i + 5 + rel
        if t == 0x007CE1E0:
            sites4.append("0x%08X" % (0x00567170 + i))
res["measured"]["FUN_00567170_getter_sites"] = {"count": len(sites4), "sites": sites4}
dump("REG567170_00567170", 0x00567170, min(len(fbody4), 0x400))

with open(os.path.join(OUT, "F1_POSCONTROL.json"), "w") as f:
    json.dump(res, f, indent=2)

print("done")
print("FUN_006B4C50 getter sites:", sites)
print("FUN_006C3F50 getter sites:", sites3)
print("FUN_00567170 getter sites:", sites4)
print("lookup size:", len(fbody), "bodyset size:", len(fbody2))
