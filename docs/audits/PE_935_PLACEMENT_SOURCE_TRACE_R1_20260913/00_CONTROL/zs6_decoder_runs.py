# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS6: communicator/decoder Run methods (network->message bridge),
#            FUN_00419dd0 (executor creation), FUN_004b2950 call-window disasm,
#            0xB9-message producer hunt (xrefs to constant 0xb9 as PUSH/CMP around
#            executor calls), plus the remaining queue object (FUN_004b1c70 family).
# Writes: 01_RAW\ghidra_output\ZS6_*.txt/.json

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
    "phase": "ZS6_decoder_runs",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    0x0082FD30, 0x0082FD10, 0x00834ED0, 0x00834EC0, 0x00834F00,
    0x00419DD0, 0x00833030, 0x0082FC80, 0x0082FCC0, 0x0082FC20,
    0x004B1C70, 0x004B2270, 0x00830830, 0x0082F8D0, 0x00830FA0,
    0x00839A50, 0x00836700, 0x008366B0, 0x00832000,
]

CALLERS_OF = {
    "FUN_00834ed0_run_frame": 0x00834ED0,
    "FUN_00834ec0_run_shared": 0x00834EC0,
    "FUN_00834f00_run_packetobj": 0x00834F00,
    "FUN_0082fd30_run_comm": 0x0082FD30,
    "FUN_00833030_comm_slot0": 0x00833030,
    "FUN_00419dd0_executor_creator": 0x00419DD0,
    "FUN_004b1c70_drain_0xb2": 0x004B1C70,
    "FUN_0082fc80": 0x0082FC80,
    "FUN_0082fcc0": 0x0082FCC0,
}

DISASM_WINDOWS = [
    ("FUN_004b2950_full", 0x004B2950, 0x004B29E4),
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

def disasm_window(start_va, end_va):
    lines = []
    addr = toAddr(start_va)
    end = toAddr(end_va)
    while addr is not None and addr.getOffset() <= end.getOffset():
        ins = listing.getInstructionAt(addr)
        if ins is not None:
            lines.append("0x%08X  %-44s" % (addr.getOffset(), str(ins)))
        addr = addr.next()
    return lines

def main():
    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS6_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS6_A_done %d" % len(DECOMPILE))

    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS6_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS6_B_done")

    for label, s, e in DISASM_WINDOWS:
        lines = disasm_window(s, e)
        with open(os.path.join(OUT_RAW, "ZS6_DISASM_%s.txt" % label), "w") as f:
            f.write("\n".join(lines))
    print("ZS6_C_done")

    print("ZS6_DONE")

main()
