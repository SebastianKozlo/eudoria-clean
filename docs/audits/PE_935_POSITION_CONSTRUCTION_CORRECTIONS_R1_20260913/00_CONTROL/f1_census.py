# -*- coding: utf-8 -*-
# f1_census.py - F1 consumer census for the 0x28 structure (dst+00..dst+24).
# STATIC-ONLY.
# (a) Callers of FUN_007343E0 (the structure reader) and FUN_007453D0 (the
#     f90 deserializer): which functions, and do they READ the record fields
#     +0x0C..+0x30 afterwards?
# (b) Callers of FUN_007345C0 (zero-init of the structure) - who embeds the
#     structure in which objects (dst+04 resolution support).
# (c) FUN_00734220/FUN_00734240/FUN_00734260 - the instance-side structure
#     writers - decode them (fields written) and find their callers.

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
pe = core.PE(core.EXE_PATH)
md = Cs(CS_ARCH_X86, CS_MODE_32)


def disasm(va, n):
    b = pe.read_va(va, n)
    return list(md.disasm(b, va))


def func_bounds(va):
    for back in range(3, 0x4000):
        a = va - back
        b3 = pe.read_va(a - 1, 3)
        if b3 == b"\xcc\xcc\xcc":
            cand = a + 2
            bb = pe.read_va(cand, 1)
            while bb == b"\xcc":
                cand += 1
                bb = pe.read_va(cand, 1)
            endv, _ = pe.func_body(cand, maxb=0x8000)
            if endv and cand <= va < endv:
                w = disasm(cand, va - cand + 8)
                if any(x.address == va for x in w):
                    return cand, endv
    return None, None


out = {}

# --- (a) callers of FUN_007343E0 / FUN_007453D0 -------------------------
for target, name in ((0x007343E0, "FUN_007343E0_structure_reader"),
                    (0x007453D0, "FUN_007453D0_f90_deserializer"),
                    (0x007345C0, "FUN_007345C0_zero_init")):
    sites = pe.calls_to(target)
    callers = []
    for off in sites:
        va = pe.text_va_start + off
        fs, fe = func_bounds(va)
        callers.append({"site": hex(va),
                        "func": "%s..%s" % (hex(fs), hex(fe)) if fs else "?"})
    out[name] = {"count": len(sites), "callers": callers}
    print("%s: %d call sites" % (name, len(sites)))
    for c in callers:
        print("   %s in %s" % (c["site"], c["func"]))

# --- (c) structure writers FUN_00734220/40/60 ---------------------------
print()
for fn in (0x00734220, 0x00734240, 0x00734260):
    end, body = pe.func_body(fn, maxb=0x60)
    txt = pe.disasm_lines(fn, len(body))
    print("=== FUN_%08X (%s) ===" % (fn, hex(end) if end else "-"))
    print(txt)
    sites = pe.calls_to(fn)
    print("  callers: %s" % [hex(pe.text_va_start + o) for o in sites])
    out["FUN_%08X" % fn] = {"disasm": txt,
                            "callers": [hex(pe.text_va_start + o)
                                        for o in sites]}
    print()

with open(os.path.join(RAW, "F1_CONSUMER_CENSUS.json"), "w") as f:
    json.dump(out, f, indent=1)
print("DONE -> 01_RAW/F1_CONSUMER_CENSUS.json")
