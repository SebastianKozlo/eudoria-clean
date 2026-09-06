# -*- coding: utf-8 -*-
# h4_display_init.py — the DisplaySubsystem init: FUN_007c5410 + FUN_0048adf0 (the display query owner).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DISPLAY_INIT.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

for va, lab in ((0x007C5410, "DISPLAY-INIT-A_007c5410"), (0x0048ADF0, "DISPLAY-INIT-B_0048adf0")):
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
    if f is not None:
        subs = f.getCalledFunctions(mon)
        lines.append("callees: " + ", ".join("{}@{}".format(x.getName(), str(x.getEntryPoint())) for x in subs)[:800])
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
