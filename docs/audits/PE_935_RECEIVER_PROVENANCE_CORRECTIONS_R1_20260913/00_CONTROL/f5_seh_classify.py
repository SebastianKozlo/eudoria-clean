# -*- coding: utf-8 -*-
# F5b — SEH-anchored classification of the 15 setter-caller functions (callers of FUN_00730F90)
# and the 24 ctor-caller functions (FUN_00730700, Ghidra-attributed entries).
# The CC CC CC heuristic mis-attributes 4 functions (adjacent/no-padding or interior CC runs);
# SEH prologue anchoring (6A FF 68 xx xx xx 00 64 A1) is the corrected boundary method.
# Output: 01_RAW/F5_SEH_CLASSIFICATION.json

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F5_seh_classification", "measured": {}, "errors": []}

ATTR_FUNCS = {0x00846840: "attr-pos-fetch", 0x008492C0: "attr-float-read",
              0x00845360: "attr-float-get", 0x008452D0: "attr-int-get",
              0x00854720: "attr-triple", 0x00843D60: "walker-init",
              0x0085B840: "walker-resolve", 0x008544D0: "resolver",
              0x00844020: "attr-check", 0x00845F70: "attr-SET"}
SINGLETONS = {0x004143F0: "singleton_00BA1260", 0x004154F0: "singleton_00BA12E8",
              0x00415570: "singleton_00BA12EC"}
SETTERS = {0x00730F90: "f90", 0x00730FB0: "fb0", 0x00730FD0: "fd0", 0x00730F60: "f60"}


def seh_anchored_body(start):
    """Body bytes from Ghidra-attributed start (SEH prologue recorded informationally)
    to next CC CC CC."""
    b = pe.read_va(start, 2)
    seh = (b is not None and b[0] == 0x6A and b[1] == 0xFF)
    fend, fbody = pe.func_body(start, 0x10000)
    return len(fbody), fbody, seh


def classify(start):
    size, body, seh = seh_anchored_body(start)
    attr, sing, sett = set(), set(), set()
    for i in range(len(body) - 5):
        if body[i] == 0xE8:
            rel = struct.unpack_from("<i", body, i + 1)[0]
            t = start + i + 5 + rel
            if t in ATTR_FUNCS:
                attr.add(ATTR_FUNCS[t])
            elif t in SINGLETONS:
                sing.add(SINGLETONS[t])
            elif t in SETTERS:
                sett.add(SETTERS[t])
    return {"func": "0x%08X" % start, "size": size, "seh_prologue": seh,
            "direct_attr_calls": sorted(attr), "singleton_calls": sorted(sing),
            "setter_calls": sorted(sett)}


# 15 f90-caller functions (Ghidra attribution GHIDRA_FUNC_ATTR.json)
F90_FUNCS = [0x0050BED0, 0x00457CD0, 0x00459270, 0x00442190, 0x00567770, 0x00567170,
             0x00447630, 0x004B3A00, 0x0043A200, 0x004C47F0, 0x0046E790, 0x00488920,
             0x005B5F90, 0x0067BC90, 0x0067CCD0]
rows15 = [classify(v) for v in sorted(F90_FUNCS)]
res["measured"]["f90_caller_classification_15"] = rows15

direct = [r for r in rows15 if r["direct_attr_calls"]]
parametric = [r for r in rows15 if not r["direct_attr_calls"] and r["func"] != "0x0046E790"]
the15th = [r for r in rows15 if r["func"] == "0x0046E790"]
res["measured"]["summary_15"] = {
    "direct_attr_count": len(direct),
    "direct_attr_funcs": [r["func"] for r in direct],
    "parametric_count": len(parametric),
    "parametric_funcs": [r["func"] for r in parametric],
    "the_15th_unaccounted": the15th,
    "the_15th_status": ("FUN_0046E790: NO_DIRECT_ATTR_CALLS; calls singleton_00BA12E8 "
                        "(param-manager); setters f60/f90/fb0; value provenance UNTRACED"),
}

# ctor-caller functions (24, Ghidra) — setter usage with SEH anchoring
CTOR_FUNCS = [0x004C5BD0, 0x00511070, 0x0050CC70, 0x0050BAF0, 0x0072FA30, 0x00459270,
              0x004B9960, 0x0046AA90, 0x004FF620, 0x00567770, 0x006C80C0, 0x00447630,
              0x0050E490, 0x006C8000, 0x00456770, 0x00457C00, 0x00457E30, 0x004E3B70,
              0x0050C0C0, 0x0050D480, 0x0050FCF0, 0x005106A0, 0x0067BC90, 0x0067CCD0]
rows24 = [classify(v) for v in sorted(CTOR_FUNCS)]
res["measured"]["ctor_caller_classification_24"] = rows24
with_setters = [r["func"] for r in rows24 if r["setter_calls"]]
without = [r["func"] for r in rows24 if not r["setter_calls"]]
res["measured"]["summary_24"] = {
    "with_setters_count": len(with_setters), "with_setters": with_setters,
    "without_setters_count": len(without), "without_setters": without,
    "note": "ctor FUN_00730700: 26 call sites in 24 functions (Ghidra); without-setters = NOT_CHECKED",
}

with open(os.path.join(OUT, "F5_SEH_CLASSIFICATION.json"), "w") as f:
    json.dump(res, f, indent=2)

print("done")
print("15:", json.dumps(res["measured"]["summary_15"], indent=1))
print("24 without setters:", len(without), without)
