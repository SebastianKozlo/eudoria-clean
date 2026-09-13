# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA6: decompile upward slice from instance-creator FUN_006cb6f0:
#   FUN_006cd850, FUN_006cd820 (callers), FUN_00489810, FUN_006c1570,
#   FUN_0043b6d0, FUN_005f6990, FUN_005f6850 + callers of those.
# Writes: 01_RAW\ghidra_output\GA6_PSEUDO_*.txt, GA6_CALLERS.json

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
    "phase": "GA6_upward_slice",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

TARGETS = [
    0x006CD850, 0x006CD820, 0x00489810, 0x006C1570,
    0x0043B6D0, 0x005F6990, 0x005F6850, 0x0093BE20,
    0x006CB370, 0x006CB020, 0x006F33A0, 0x0077C0B0,
]

CALLER_QUERIES = {
    "FUN_006cd850": 0x006CD850,
    "FUN_006cd820": 0x006CD820,
    "FUN_00489810": 0x00489810,
    "FUN_0093be20": 0x0093BE20,
    "FUN_005f6850": 0x005F6850,
    "FUN_005f6990": 0x005F6990,
}

def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None

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

def disasm_func(fn, max_inst=400):
    out = []
    inst = listing.getInstructionAt(fn.getEntryPoint())
    if inst is None:
        inst = listing.getInstructionContaining(fn.getEntryPoint())
    n = 0
    while inst is not None and n < max_inst:
        out.append("0x%08X  %-30s %s" % (inst.getAddress().getOffset(),
                                         bytes_hex(inst) or "", inst.toString()))
        inst = inst.getNext()
        n += 1
    return "\n".join(out)

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
        with open(os.path.join(OUT_RAW, "GA6_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:22000])
        if va in (0x006CD850, 0x006CD820, 0x006CB370, 0x0077C0B0):
            with open(os.path.join(OUT_RAW, "GA6_DISASM_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
                f.write(disasm_func(fn, 400))

    cq = {}
    for label, va in CALLER_QUERIES.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "GA6_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)

    print("GA6_DONE targets=%d" % len(TARGETS))

main()
