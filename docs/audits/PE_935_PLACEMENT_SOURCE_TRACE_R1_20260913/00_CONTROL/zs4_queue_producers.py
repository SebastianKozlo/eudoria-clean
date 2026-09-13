# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS4: message-queue producers/consumers (H1 vs H3 discriminator).
#  A) Decompile: queue enqueue/drain, executor registration, static-packet creator,
#     requester family (0048f930/0048fcc0/0048fe60 - attr writers on CWO),
#     the 0x6a4-family checkers (00845650 etc.), deferred-exec internals.
#  B) Callers of: enqueue point FUN_004b1890, static packet creator FUN_008310d0,
#     queue-extractors FUN_00752700/FUN_00752640, FUN_004b1b70, FUN_0042bc20 (gate),
#     FUN_004641f0 (from 00567c50 chain), FUN_005b6370, FUN_00567b40.
# Writes: 01_RAW\ghidra_output\ZS4_*.txt/.json

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
    "phase": "ZS4_queue_producers",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x004B1890, 0x004B1B70, 0x004B2270, 0x004B1C70, 0x0042BC20,
    0x0048F930, 0x0048FCC0, 0x0048FE60,
    0x008310D0, 0x00845650, 0x004641F0,
    0x00567B40, 0x00752700, 0x00752640,
    0x004B1210, 0x004B07E0, 0x004B0860,
    0x0050CC70, 0x0050BAF0, 0x004FF620, 0x004C5BD0, 0x005106A0, 0x0050FCF0, 0x0050C0C0,
    0x004E3B70,
]

CALLERS_OF = {
    "FUN_004b1890_enqueue": 0x004B1890,
    "FUN_008310d0_staticpacket_creator": 0x008310D0,
    "FUN_00752700_queue_extract_t1": 0x00752700,
    "FUN_00752640_queue_extract_t2": 0x00752640,
    "FUN_004b1b70_queue_drain": 0x004B1B70,
    "FUN_0042bc20_gate": 0x0042BC20,
    "FUN_004641f0": 0x004641F0,
    "FUN_00567b40": 0x00567B40,
    "FUN_0048f930": 0x0048F930,
    "FUN_0048fcc0": 0x0048FCC0,
    "FUN_0048fe60": 0x0048FE60,
    "FUN_004b2270": 0x004B2270,
    "FUN_005b47f0": 0x005B47F0,
    "FUN_00464370": 0x00464370,
    "FUN_005712e0": 0x005712E0,
    "FUN_0042b180": 0x0042B180,
    "FUN_00622920": 0x00622920,
    "FUN_00539de0": 0x00539DE0,
    "FUN_004587e0": 0x004587E0,
    "FUN_0048ecc0": 0x0048ECC0,
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

def callers_of(va_int, limit=80):
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
        with open(os.path.join(OUT_RAW, "ZS4_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS4_A_done %d" % len(DECOMPILE))

    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS4_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS4_B_done")

    print("ZS4_DONE")

main()
