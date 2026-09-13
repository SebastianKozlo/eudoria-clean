# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS10 (closure): callers of FUN_00468910 (the CWO update engine),
# ALL references (not only calls) to FUN_00514ef0 / FUN_005b72c0 / FUN_00468910 /
# FUN_00567c50 (function-pointer tables / dispatch registration),
# FUN_00841920 body, FUN_00490310 body, FUN_004b0ab0/004b1670 (0xc6/199 handlers).
# Writes: 01_RAW\ghidra_output\ZS10_*.txt/.json

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "phase": "ZS10_closure",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x00841920, 0x00490310, 0x004B0AB0, 0x004B1670, 0x004641F0,
]

ALL_REFS_OF = {
    "FUN_00514ef0": 0x00514EF0,
    "FUN_005b72c0": 0x005B72C0,
    "FUN_00468910": 0x00468910,
    "FUN_00567c50": 0x00567C50,
    "FUN_0058db50": 0x0058DB50,
}

CALLERS_OF = {
    "FUN_00468910_cwo_update": 0x00468910,
    "FUN_00490310": 0x00490310,
}

def decompile(func, max_secs=150):
    if func is None:
        return None
    di = DecompInterface()
    di.openProgram(currentProgram)
    try:
        res = di.decompileFunction(func, max_secs, monitor)
        if res.decompileCompleted():
            return res.getDecompiledFunction().getC()
    except:
        return None
    finally:
        di.dispose()

def all_refs(va_int, limit=60):
    res = []
    fn = fm.getFunctionAt(toAddr(va_int))
    if fn is None:
        return res
    for r in rm.getReferencesTo(fn.getEntryPoint()):
        fa = r.getFromAddress()
        fn2 = fm.getFunctionContaining(fa)
        res.append({
            "from_va": "0x%08X" % fa.getOffset(),
            "type": str(r.getReferenceType()),
            "in_function": fn2.getName() if fn2 else None,
            "func_entry": ("0x%08X" % fn2.getEntryPoint().getOffset()) if fn2 else None,
            "is_call": r.getReferenceType().isCall(),
        })
        if len(res) >= limit:
            break
    return res

def callers_of(va_int, limit=60):
    res = []
    fn = fm.getFunctionContaining(toAddr(va_int)) or fm.getFunctionAt(toAddr(va_int))
    if fn is not None:
        for r in rm.getReferencesTo(fn.getEntryPoint()):
            if r.getReferenceType().isCall():
                fa = r.getFromAddress()
                fn2 = fm.getFunctionContaining(fa)
                res.append({
                    "from_va": "0x%08X" % fa.getOffset(),
                    "in_function": fn2.getName() if fn2 else None,
                    "func_entry": ("0x%08X" % fn2.getEntryPoint().getOffset()) if fn2 else None,
                })
                if len(res) >= limit:
                    break
    return res

def main():
    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS10_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS10_A_done %d" % len(DECOMPILE))

    ar = {}
    for label, va in ALL_REFS_OF.items():
        ar[label] = all_refs(va)
    with open(os.path.join(OUT_RAW, "ZS10_ALL_REFS.json"), "w") as f:
        json.dump({"exec": EXEC, "all_refs": ar}, f, indent=2)
    print("ZS10_B_done")

    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS10_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS10_C_done")

    print("ZS10_DONE")

main()
