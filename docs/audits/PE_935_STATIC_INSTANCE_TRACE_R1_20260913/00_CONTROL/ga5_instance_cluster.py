# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA5: decompile the instance-creation cluster + CWO cluster + WorldSubsystem.
# Targets: model-instance area (006cb3c0/006cb6f0), complete-consumer caller
# 006b9970, CWO callers (004c5bd0..005106a0), WorldSubsystem (004172a0/0048e290),
# ArkClientObjectManagerImpl vtable methods (004a9c00/006077c0/004a9dd0/004a9870/
# 004ab6f0/004aae10/004abb70), plus callers of FUN_006cb3c0 and FUN_006cb6f0.
# Writes: 01_RAW\ghidra_output\GA5_PSEUDO_*.txt, GA5_CALLERS.json

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
    "phase": "GA5_instance_cluster",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

TARGETS = [
    0x006CB3C0, 0x006CB6F0, 0x006B9970,
    0x004C5BD0, 0x0050BAF0, 0x004FF620, 0x00567770,
    0x004E3B70, 0x0050C0C0, 0x0050FCF0, 0x005106A0,
    0x004172A0, 0x0048E290, 0x0048E2B0,
    0x004A9C00, 0x006077C0, 0x004A9DD0, 0x004A9870,
    0x004AB6F0, 0x004AAE10, 0x004ABB70,
    0x004A9BA0, 0x004A9BD0,
]

CALLER_QUERIES = {
    "FUN_006cb3c0": 0x006CB3C0,
    "FUN_006cb6f0": 0x006CB6F0,
    "FUN_006b9970": 0x006B9970,
    "FUN_004c5bd0": 0x004C5BD0,
    "FUN_0048e2b0": 0x0048E2B0,
    "FUN_0048e290": 0x0048E290,
    "FUN_006077c0": 0x006077C0,
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

def disasm_func(fn, max_inst=700):
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
        with open(os.path.join(OUT_RAW, "GA5_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])

    cq = {}
    for label, va in CALLER_QUERIES.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "GA5_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)

    # disasm of the model-instance pair for byte-level evidence
    for va in [0x006CB3C0, 0x006CB6F0, 0x006F2AF0]:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        with open(os.path.join(OUT_RAW, "GA5_DISASM_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write(disasm_func(fn, 700))

    print("GA5_DONE targets=%d" % len(TARGETS))

main()
