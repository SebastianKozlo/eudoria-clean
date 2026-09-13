# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA7: final upward closure - FUN_006bf2e0, FUN_006cdd80, FUN_005ae230,
# FUN_005f6c70 + their callers (who drives the visual placement).
# Writes: 01_RAW\ghidra_output\GA7_PSEUDO_*.txt, GA7_CALLERS.json

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "phase": "GA7_final_closure",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

TARGETS = [0x006BF2E0, 0x006CDD80, 0x005AE230, 0x005F6C70, 0x006CD580, 0x006CD4E0]
CALLER_QUERIES = {
    "FUN_006bf2e0": 0x006BF2E0,
    "FUN_006cdd80": 0x006CDD80,
    "FUN_005ae230": 0x005AE230,
    "FUN_005f6c70": 0x005F6C70,
}

def decompile(func, max_secs=120):
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

def callers_of(va_int, limit=40):
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
    for va in TARGETS:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "GA7_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:22000])

    cq = {}
    for label, va in CALLER_QUERIES.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "GA7_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)

    print("GA7_DONE targets=%d" % len(TARGETS))

main()
