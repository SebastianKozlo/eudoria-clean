# -*- coding: utf-8 -*-
# h4_gates.py — decompile ALL the orchestrator's gate functions + hunt the display init.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_GATES.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

GATES = [0x0048E7C0, 0x00415D70, 0x0041B4B0, 0x00416390, 0x00467E60,
         0x00459270, 0x0044C8E0, 0x004736C0, 0x00984610, 0x0043F060, 0x00418010]

for va in GATES:
    f = fm.getFunctionAt(toAddr(va))
    if f is None:
        lines.append("=== @0x{:x}: NO FUNCTION".format(va))
        continue
    lines.append("=== GATE @0x{:x} : {}".format(va, f.getName()))
    res = di.decompileFunction(f, 200, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
