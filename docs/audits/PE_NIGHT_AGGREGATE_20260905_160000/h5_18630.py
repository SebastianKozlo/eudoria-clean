# -*- coding: utf-8 -*-
# h5_18630.py — FUN_00418630 (the 0x160-object's inner ctor — the last big unknown).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_18630.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

f = fm.getFunctionAt(toAddr(0x00418630))
if f is None:
    lines.append("no function at 0x418630")
else:
    res = di.decompileFunction(f, 500, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    subs = f.getCalledFunctions(mon)
    lines.append("\ncallees: " + ", ".join("{}@{}".format(x.getName(), str(x.getEntryPoint())) for x in subs)[:900])

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
