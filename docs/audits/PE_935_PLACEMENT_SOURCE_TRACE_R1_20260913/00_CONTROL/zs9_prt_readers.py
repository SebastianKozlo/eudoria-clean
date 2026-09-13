# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS9 (final): portal .prt reader bodies (FUN_00852750/FUN_00852bf0/FUN_00852d60,
# FUN_00851e80/FUN_00852110/FUN_00850C50/FUN_00852A30-neighbours) + FUN_0085aff0 +
# FUN_004b2a20 (distance gate) + FUN_00719b40/00719b20 (queue readers 0xa8) +
# FUN_00570480 (the 0x110 singleton ctor) + disasm of FUN_00852750 full body.
# Writes: 01_RAW\ghidra_output\ZS9_*.txt/.json

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
    "phase": "ZS9_prt_readers",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x00852750, 0x00852BF0, 0x00852D60, 0x00851E80, 0x00852110,
    0x00850C50, 0x00852A30, 0x0085AFF0, 0x004B2A20, 0x0085B0A0, 0x0085B0B0,
    0x00719B40, 0x00719B20, 0x00570480, 0x00852740,
]

DISASM_WINDOWS = [
    ("FUN_00852750_full", 0x00852750, 0x00852900),
]

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

def disasm_window(start_va, end_va):
    lines = []
    addr = toAddr(start_va)
    end = toAddr(end_va)
    while addr is not None and addr.getOffset() <= end.getOffset():
        ins = listing.getInstructionAt(addr)
        if ins is not None:
            lines.append("0x%08X  %-46s" % (addr.getOffset(), str(ins)))
        addr = addr.next()
    return lines

def main():
    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS9_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS9_A_done %d" % len(DECOMPILE))

    for label, s, e in DISASM_WINDOWS:
        lines = disasm_window(s, e)
        with open(os.path.join(OUT_RAW, "ZS9_DISASM_%s.txt" % label), "w") as f:
            f.write("\n".join(lines))
    print("ZS9_B_done")

    print("ZS9_DONE")

main()
