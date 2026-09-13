# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS8: FUN_0040de60 call-site immediate classification (cursor advance args),
#            sibling queue dispatchers, FUN_00464370 (0xa2), FUN_00490010 hub.
# Writes: 01_RAW\ghidra_output\ZS8_*.txt/.json

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
    "phase": "ZS8_cursor_immediates",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x0042B180, 0x004587E0, 0x00539DE0, 0x00622920,
    0x00464370, 0x00490010, 0x0075FF20, 0x00414370, 0x004143F0,
    0x0048E740, 0x005B47F0, 0x005B4720, 0x005B5070, 0x004B0AB0,
]

CURSOR_FN = 0x0040DE60

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

def classify_cursor_calls():
    """For every CALL to FUN_0040de60, record the call-site instruction and the
    preceding window to identify the advance argument (immediate or register)."""
    res = []
    fn = fm.getFunctionAt(toAddr(CURSOR_FN))
    if fn is None:
        return res
    for r in rm.getReferencesTo(fn.getEntryPoint()):
        if not r.getReferenceType().isCall():
            continue
        fa = r.getFromAddress()
        ins = listing.getInstructionAt(fa)
        fn2 = fm.getFunctionContaining(fa)
        # window: 4 instructions before
        win = []
        addr = fa
        for _ in range(5):
            prev = listing.getInstructionBefore(addr)
            if prev is None:
                break
            addr = prev.getAddress()
            win.insert(0, "0x%08X  %s" % (prev.getAddress().getOffset(), str(prev)))
        res.append({
            "call_va": "0x%08X" % fa.getOffset(),
            "call_instruction": str(ins) if ins else None,
            "in_function": fn2.getName() if fn2 else None,
            "func_entry": ("0x%08X" % fn2.getEntryPoint().getOffset()) if fn2 else None,
            "prev_window": win,
        })
    return res

def main():
    rows = classify_cursor_calls()
    with open(os.path.join(OUT_RAW, "ZS8_CURSOR_CALL_SITES.json"), "w") as f:
        json.dump({"exec": EXEC, "count": len(rows), "sites": rows}, f, indent=2)
    print("ZS8_A_done %d cursor calls" % len(rows))

    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS8_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS8_B_done %d" % len(DECOMPILE))

    print("ZS8_DONE")

main()
