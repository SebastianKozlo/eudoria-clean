# -*- coding: utf-8 -*-
# map_throw_sites.py — identify the functions containing 0x40943F, 0x40B6D4, 0x406E14 + decompile them.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_THROW_SITES.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

for va in (0x0040943F, 0x0040B6D4, 0x00406E14):
    f = fm.getFunctionContaining(toAddr(va))
    if f is None:
        lines.append("0x{:x}: NO FUNCTION".format(va))
        continue
    lines.append("=== the throw-site 0x{:x} is in {} @{}".format(va, f.getName(), f.getEntryPoint()))
    res = di.decompileFunction(f, 240, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed)")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
