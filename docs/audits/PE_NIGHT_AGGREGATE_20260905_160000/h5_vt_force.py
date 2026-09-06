# -*- coding: utf-8 -*-
# h5_vt_force.py — force-create + decompile the VT1/VT2 methods (0x48B520, 0x48B0E0).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_VT_FORCE.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []
af = currentProgram.getFunctionManager()

for va, lab in ((0x0048B520, "VT1_0048b520"), (0x0048B0E0, "VT2_0048b0e0"), (0x0048AF30, "DTOR-HELPER_0048af30")):
    f = af.getFunctionAt(toAddr(va))
    if f is None:
        tx = currentProgram.startTransaction("force")
        try:
            f = af.createFunction(toAddr(va), "FORCED_{:x}".format(va))
        finally:
            tx.dispose()
    if f is None:
        lines.append("=== {}: CREATE FAILED".format(lab))
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
