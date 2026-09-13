# -*- coding: utf-8 -*-
# F2 — FUN_00567C50 caller-argument provenance + full getter-D/getter-A receiver table.
# For each claim in Z4 §2 (D consumers): establish the ECX receiver provenance.
# Output: 01_RAW/F2_DCLAIMS.json

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
res = {"stage": "F2_dclaims", "measured": {}, "errors": []}


def calls_in_body(base_va, size):
    out = []
    tr = pe.text_raw
    off = pe.text_va_to_off(base_va)
    for i in range(size - 5):
        if tr[off + i] == 0xE8:
            rel = struct.unpack_from("<i", tr, off + i + 1)[0]
            t = base_va + i + 5 + rel
            if pe.text_va_start <= t < 0x00A75000:
                out.append({"at": "0x%08X" % (base_va + i), "target": "0x%08X" % t})
    return out


# 1. census of all direct callers of getter D (FUN_0048ADA0) with containing functions
d_sites = pe.calls_to(0x0048ADA0)
d = pe.data


def func_start(va):
    off = pe.va_to_off(va)
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None


dcall = []
for o in d_sites:
    va = pe.text_off_to_va(o)
    dcall.append({"call_site": "0x%08X" % va, "func_start": ("0x%08X" % func_start(va)) if func_start(va) else None})
res["measured"]["getterD_116_callers_attributed"] = {"count": len(dcall), "sites": dcall}

# 2. FUN_00567C50 callers: the 3 sites — argument provenance via preceding bytes
for label, site in (("FUN_005b72c0@0x005B7567", 0x005B7567),
                    ("FUN_0058db50@0x0058E0B7", 0x0058E0B7),
                    ("FUN_00514ef0@0x00515345", 0x00515345)):
    b = pe.read_va(site - 0x18, 0x18 + 5)
    res["measured"]["caller_ctx_%s" % label] = {
        "window_hex": b.hex(),
        "note": "bytes before CALL FUN_00567C50; census E8 anchor at site"}

# 3. In FUN_00567C50: the receiver of getter-D sites = ESI = [ESP+0xEC] (first stack arg)
#    verify the head MOV ESI,[ESP+0xEC] bytes
b2 = pe.read_va(0x00567C93, 7)
res["measured"]["FUN_00567C50_ESI_load"] = {"va": "0x00567C93", "hex": b2.hex(),
                                            "decode": "MOV ESI,[ESP+0xEC] (first stack arg)"}

# 4. census: which functions call getter D AND are in Z4's claimed families:
#    FUN_00468910 x5, FUN_00567c50 x2(+1 more at 0x00567F72), FUN_00861390 f32 (getter 0x00861240)
f32_sites = pe.calls_to(0x00861240)
f32call = []
for o in f32_sites:
    va = pe.text_off_to_va(o)
    f32call.append({"call_site": "0x%08X" % va, "func_start": ("0x%08X" % func_start(va)) if func_start(va) else None})
res["measured"]["getterDf32_00861240_callers"] = {"count": len(f32call), "sites": f32call}

# 5. check Z4 claim "FUN_00861390 ×2 (f32-D)": census callers of 0x00861240 within FUN_00861390
in_861390 = [x for x in f32call if x["func_start"] == "0x00861390"]
res["measured"]["getterDf32_in_FUN_00861390"] = in_861390

# 6. FUN_00468910 getter-D sites (claimed x5)
in_468910 = [x for x in dcall if x["func_start"] == "0x00468910"]
res["measured"]["getterD_in_FUN_00468910"] = in_468910

with open(os.path.join(OUT, "F2_DCLAIMS.json"), "w") as f:
    json.dump(res, f, indent=2)

print("done")
print("getterD in FUN_00468910:", len(in_468910), in_468910)
print("getterDf32 in FUN_00861390:", len(in_861390), in_861390)
print("getterDf32 callers:", len(f32call), f32call)
