# -*- coding: utf-8 -*-
# dump_deepinit.py — FUN_00405150 (the deep init) + FUN_00402fd0 (check-1) + their callees.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DEEPINIT_00405150.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []


def dec(addr, label, limit=300):
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


f51 = dec(0x00405150, "DEEP-INIT", 400)
dec(0x00402fd0, "CHECK-1", 200)
dec(0x00402910, "MAIN-RUN-ENTRY", 200)
if f51 is not None:
    subs = f51.getCalledFunctions(mon)
    lines.append("DEEP-INIT calls {} functions:".format(len(subs)))
    for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
        lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
