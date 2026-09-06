# -*- coding: utf-8 -*-
# h5_dss_methods.py — the DisplaySubsystem vtable methods (0x48B0A0 / 0x48B520 / 0x48B0E0).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DSS_METHODS.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
refmgr = currentProgram.getReferenceManager()
lines = []

for va, lab in ((0x0048B0A0, "DSS-vt0"), (0x0048B520, "DSS-vt1"), (0x0048B0E0, "DSS-vt2")):
    f = fm.getFunctionAt(toAddr(va))
    if f is None:
        lines.append("=== {}: NO FUNCTION".format(lab))
        continue
    lines.append("=== {} : {} @{}".format(lab, f.getName(), f.getEntryPoint()))
    res = di.decompileFunction(f, 400, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    # the callers of this method
    callers = set()
    for ref in refmgr.getReferencesTo(f.getEntryPoint()):
        sf = fm.getFunctionContaining(ref.getFromAddress())
        if sf is not None:
            callers.add(sf.getName() + "@" + str(sf.getEntryPoint()))
    lines.append("callers: {}".format(sorted(callers))[:1200] if False else "callers: " + ", ".join(sorted(callers)))
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
