# -*- coding: utf-8 -*-
# h4_ctors.py — the orchestrator's unexplored ctors (the display-init candidates).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_CTORS.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

CTORS = [0x004926E0, 0x0048AEF0, 0x0048E170, 0x0048EF00, 0x00418C20,
         0x00418570, 0x004A9BA0, 0x00419390, 0x004123D0]

for va in CTORS:
    f = fm.getFunctionAt(toAddr(va))
    if f is None:
        lines.append("=== @0x{:x}: NO FUNCTION".format(va))
        continue
    lines.append("=== CTOR @0x{:x} : {}".format(va, f.getName()))
    res = di.decompileFunction(f, 250, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
