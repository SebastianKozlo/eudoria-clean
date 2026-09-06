# -*- coding: utf-8 -*-
# h4_orchestrator.py — the FULL decompile of FUN_004172a0 (the subsystem-init orchestrator).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_ORCHESTRATOR.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

f = fm.getFunctionAt(toAddr(0x004172A0))
lines.append("=== FUN_004172a0 (the subsystem-init orchestrator) FULL")
res = di.decompileFunction(f, 600, mon)
if res.decompileCompleted():
    lines.append(res.getDecompiledFunction().getC())
else:
    lines.append("(failed: {})".format(res.getErrorMessage()))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
