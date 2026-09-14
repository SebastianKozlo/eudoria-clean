# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - Ghidra postScript (Jython) GH3.
# Final batch: message-dispatch region (containing funcs of call sites),
# read-cursor ops (FUN_00752640/FUN_007527F0/FUN_00525AF0/FUN_00415470/
# FUN_007046A0), registry builder FUN_0072FA30 (VFS path), callers of the
# secondary insert funnels.

import json
import os
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913\01_RAW"
DEC_DIR = os.path.join(OUT_DIR, "DECOMP")

DECOMP = [
    0x00752640, 0x007527F0, 0x00525AF0, 0x00415470, 0x007046A0,
    0x0072FA30, 0x005B6890, 0x005B6370, 0x00846760, 0x0040DE60,
    0x00843D60, 0x00843DD0, 0x004148F0, 0x004C4640, 0x00765930,
    0x00509190, 0x0050A690,
]

CENSUS_TARGETS = {
    "funnel_FUN_0050BED0": 0x0050BED0,
    "funnel_FUN_00442190": 0x00442190,
    "funnel_FUN_00441910": 0x00441910,
    "funnel_FUN_004B3A00": 0x004B3A00,
    "keyproducer_FUN_00457930": 0x00457930,
    "placement_FUN_004C47F0": 0x004C47F0,
    "handler0x39_FUN_005B6370": 0x005B6370,
    "sender_FUN_005B6890": 0x005B6890,
    "parserA_FUN_00730C90": 0x00730C90,
    "registry_builder_FUN_0072FA30": 0x0072FA30,
    "composer2_FUN_008599A0": 0x008599A0,
}

CONTAINING = [0x004B198B, 0x004B1AC1, 0x004B1AD9, 0x004B2984, 0x004B1A16,
              0x00567D24, 0x0056836C, 0x00515345, 0x0058E0B7]


def main():
    prog = currentProgram
    fm = prog.getFunctionManager()
    af = prog.getAddressFactory()
    space = af.getDefaultAddressSpace()

    def addr(va):
        return space.getAddress(va)

    if not os.path.isdir(DEC_DIR):
        os.makedirs(DEC_DIR)

    res = {"stage": "GH3_decomp_census", "measured": {}, "errors": []}

    ifc = DecompInterface()
    ifc.openProgram(prog)
    mon = ConsoleTaskMonitor()

    # resolve containing functions first, then decompile them too
    cont = {}
    to_decompile = list(DECOMP)
    for va in CONTAINING:
        f = fm.getFunctionContaining(addr(va))
        rec = None
        if f is not None:
            rec = {"entry": "0x%08X" % f.getEntryPoint().getOffset(),
                   "name": f.getName(),
                   "body_size": f.getBody().getNumAddresses()}
            to_decompile.append(f.getEntryPoint().getOffset())
        cont["0x%08X" % va] = rec
    res["measured"]["function_containing"] = cont

    decomp_index = []
    seen = {}
    for va in to_decompile:
        f = fm.getFunctionContaining(addr(va))
        rec = {"requested": "0x%08X" % va}
        if f is None:
            rec["error"] = "no function containing VA"
            decomp_index.append(rec)
            continue
        entry = f.getEntryPoint().getOffset()
        rec["entry"] = "0x%08X" % entry
        rec["name"] = f.getName()
        rec["body_size"] = f.getBody().getNumAddresses()
        if entry in seen:
            rec["decompiled"] = seen[entry]
            decomp_index.append(rec)
            continue
        r = ifc.decompileFunction(f, 120, mon)
        if r.decompileCompleted():
            c = r.getDecompiledFunction().getC()
            fn = "F%08X.c" % entry
            with open(os.path.join(DEC_DIR, fn), "w") as fh:
                fh.write(c)
            rec["decompiled"] = fn
            seen[entry] = fn
        else:
            rec["error"] = "decompile failed: %s" % r.getErrorMessage()
            res["errors"].append("decomp fail 0x%08X" % entry)
        decomp_index.append(rec)
    res["measured"]["decomp_index"] = decomp_index

    census = {}
    for name, t in sorted(CENSUS_TARGETS.items()):
        refs = getReferencesTo(addr(t))
        lst = []
        for r in refs:
            if r.getReferenceType().isCall():
                f = fm.getFunctionContaining(r.getFromAddress())
                lst.append({
                    "call_site": "0x%08X" % r.getFromAddress().getOffset(),
                    "func": (f.getName() if f is not None else None),
                    "entry": ("0x%08X" % f.getEntryPoint().getOffset()) if f is not None else None})
        census[name] = {"count": len(lst), "sites": lst}
    res["measured"]["isCall_census"] = census

    with open(os.path.join(OUT_DIR, "GH3_DECOMP_CENSUS.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("GH3 done: decompiled=%d census=%d containing=%d" % (
        len(seen), len(census), len(cont)))


main()
