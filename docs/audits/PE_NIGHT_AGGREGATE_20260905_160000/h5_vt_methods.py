# -*- coding: utf-8 -*-
# h5_vt_methods.py — the 3 DisplaySubsystem vtable methods.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_VT_METHODS.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

for va, lab in ((0x0048B0A0, "VT0_0048b0a0"), (0x0048B520, "VT1_0048b520"), (0x0048B0E0, "VT2_0048b0e0")):
    f = fm.getFunctionAt(toAddr(va))
    if f is None:
        lines.append("=== {}: NO FUNCTION".format(lab))
        continue
    lines.append("=== {} : {}".format(lab, f.getName()))
    res = di.decompileFunction(f, 400, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    subs = f.getCalledFunctions(mon)
    lines.append("callees: " + ", ".join("{}@{}".format(x.getName(), str(x.getEntryPoint())) for x in subs)[:700])
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
