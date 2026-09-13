# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS7: cursor-advance FUN_0040de60 caller census (queue producers/readers),
#            + decompile FUN_0040de60, FUN_007527f0, FUN_0040e0d0, FUN_004b0df0,
#              FUN_0040af70/0040af80 (runnable base), FUN_004b1c70-family,
#              FUN_00839a50 (0xFE chunk decoder), FUN_008351e0 (packet ctor3 ctx),
#              FUN_00833fe0, FUN_00464370-family checkers.
# Writes: 01_RAW\ghidra_output\ZS7_*.txt/.json

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
    "phase": "ZS7_cursor_family",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x0040DE60, 0x007527F0, 0x0040E0D0, 0x004B0DF0,
    0x0040AF70, 0x0040AF80, 0x00839A50, 0x008351E0,
    0x00833FE0, 0x00836700, 0x008366B0, 0x00832000,
    0x00401260, 0x00401360, 0x004023C0, 0x00404C30,
]

CALLERS_OF = {
    "FUN_0040de60_cursor_advance": 0x0040DE60,
    "FUN_007527f0_queue_typecheck": 0x007527F0,
    "FUN_00839a50_chunk_decoder": 0x00839A50,
    "FUN_008351e0_packet_ctor3_ctx": 0x008351E0,
    "FUN_00833fe0": 0x00833FE0,
    "FUN_004b0df0": 0x004B0DF0,
    "FUN_0040e0d0": 0x0040E0D0,
    "FUN_00401260": 0x00401260,
    "FUN_00401360": 0x00401360,
    "FUN_004023c0": 0x004023C0,
    "FUN_00404c30": 0x00404C30,
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

def callers_of(va_int, limit=200):
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
        with open(os.path.join(OUT_RAW, "ZS7_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS7_A_done %d" % len(DECOMPILE))

    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS7_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS7_B_done")

    print("ZS7_DONE")

main()
