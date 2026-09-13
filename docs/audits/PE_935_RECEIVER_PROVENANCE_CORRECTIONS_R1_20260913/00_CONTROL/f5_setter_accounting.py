# -*- coding: utf-8 -*-
# F5 — setter-caller accounting (15 functions calling FUN_00730f90) + ctor FUN_00730700
# 26 callers with/without setter calls. Identifies the 15th unaccounted function.
# Output: 01_RAW/F5_SETTER_ACCOUNTING.json

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
d = pe.data
res = {"stage": "F5_setter_accounting", "measured": {}, "errors": []}

ATTR_FUNCS = {
    0x00846840: "attr-pos-fetch", 0x008492C0: "attr-float-read",
    0x00845360: "attr-float-get", 0x008452D0: "attr-int-get",
    0x00854720: "attr-triple", 0x00843D60: "walker-init",
    0x0085B840: "walker-resolve", 0x008544D0: "resolver",
    0x00844020: "attr-check", 0x00845F70: "attr-SET",
}
SINGLETONS = {
    0x004143F0: "singleton_00BA1260", 0x004154F0: "singleton_00BA12E8",
    0x00415570: "singleton_00BA12EC",
}
SETTERS = {0x00730F90: "setter_pos", 0x00730FB0: "setter_rot",
           0x00730FD0: "setter_2p", 0x00730F60: "setter_init"}
CTOR = 0x00730700


def func_start(va):
    off = pe.va_to_off(va)
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None


def calls_in_func(start_va, maxb=0x8000):
    fend, fbody = pe.func_body(start_va, maxb)
    out = []
    for i in range(len(fbody) - 5):
        if fbody[i] == 0xE8:
            rel = struct.unpack_from("<i", fbody, i + 1)[0]
            t = start_va + i + 5 + rel
            if 0x00401000 <= t < 0x00A75000:
                out.append((start_va + i, t))
    return out, len(fbody)


# 1. census callers of FUN_00730f90 -> expect 15
f90_sites = pe.calls_to(0x00730F90)
f90_funcs = {}
for o in f90_sites:
    va = pe.text_off_to_va(o)
    st = func_start(va)
    f90_funcs.setdefault(st, []).append(va)
res["measured"]["FUN_00730f90_callers"] = {
    "count_sites": len(f90_sites), "count_funcs": len(f90_funcs),
    "funcs": {("0x%08X" % k): ["0x%08X" % v for v in v2] for k, v2 in f90_funcs.items()}}

# 2. classify the 15: direct attr calls?
classification = []
for st in sorted(f90_funcs):
    calls, size = calls_in_func(st)
    attr = sorted(set(t for a, t in calls if t in ATTR_FUNCS))
    sing = sorted(set(t for a, t in calls if t in SINGLETONS))
    setcalls = sorted(set(t for a, t in calls if t in SETTERS))
    classification.append({
        "func": "0x%08X" % st, "size": size,
        "direct_attr_calls": ["0x%08X" % t for t in attr],
        "singleton_calls": ["0x%08X" % t for t in sing],
        "setter_calls": ["0x%08X" % t for t in setcalls],
        "f90_sites": ["0x%08X" % v for v in f90_funcs[st]],
    })
res["measured"]["classification_15"] = classification

# 3. ctor FUN_00730700 callers (expect 26) + setter usage check
ctor_sites = pe.calls_to(CTOR)
ctor_funcs = {}
for o in ctor_sites:
    va = pe.text_off_to_va(o)
    st = func_start(va)
    ctor_funcs.setdefault(st, []).append(va)
rows = []
for st in sorted(ctor_funcs):
    calls, size = calls_in_func(st)
    setcalls = sorted(set(t for a, t in calls if t in SETTERS))
    rows.append({"func": "0x%08X" % st, "ctor_site": "0x%08X" % ctor_funcs[st][0],
                 "setter_calls": ["0x%08X" % t for t in setcalls],
                 "has_setters": len(setcalls) > 0})
res["measured"]["ctor_FUN_00730700_callers"] = {
    "count_sites": len(ctor_sites), "count_funcs": len(ctor_funcs), "rows": rows}
no_setters = [r["func"] for r in rows if not r["has_setters"]]
res["measured"]["ctor_callers_without_setters"] = no_setters

with open(os.path.join(OUT, "F5_SETTER_ACCOUNTING.json"), "w") as f:
    json.dump(res, f, indent=2)

print("FUN_00730f90: sites=%d funcs=%d" % (len(f90_sites), len(f90_funcs)))
print("ctor FUN_00730700: sites=%d funcs=%d, without setters: %d" % (
    len(ctor_sites), len(ctor_funcs), len(no_setters)))
print("no-setter funcs:", no_setters)
print()
for c in classification:
    direct = len(c["direct_attr_calls"]) > 0
    sing = len(c["singleton_calls"]) > 0
    print("%s attr=%s sing=%s setters=%s" % (
        c["func"], "Y" if direct else "-", "Y" if sing else "-",
        ",".join(hex(t)[2:] for t in [int(x, 16) for x in c["setter_calls"]])))
