# -*- coding: utf-8 -*-
# dump_loop.py — FUN_00402910 (the message loop) + FUN_00417030 (the loop step) + FUN_004172a0 + FUN_00401360.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_LOOP.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []


def dec(addr, label, limit=400):
    f = fm.getFunctionAt(toAddr(addr))
    if f is None:
        lines.append("=== {} @0x{:x}: NO FUNCTION".format(label, addr))
        return None
    lines.append("=== {} @0x{:x} : {}".format(label, addr, f.getName()))
    res = di.decompileFunction(f, limit, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    return f


f17030 = dec(0x00417030, "LOOP-STEP-00417030", 400)
dec(0x004172a0, "HELPER-004172a0", 200)
dec(0x00401360, "ERR-00401360", 200)
dec(0x00402910, "MSG-LOOP-00402910", 200)
if f17030 is not None:
    subs = f17030.getCalledFunctions(mon)
    lines.append("LOOP-STEP callees: " + ", ".join("{}@{}".format(x.getName(), str(x.getEntryPoint())) for x in subs)[:1200])

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
