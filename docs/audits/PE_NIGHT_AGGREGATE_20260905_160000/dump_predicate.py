# -*- coding: utf-8 -*-
# dump_predicate.py — FUN_00746550 (THE display predicate) + its callees (2 levels).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_PREDICATE_00746550.txt"
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


fp = dec(0x00746550, "PREDICATE", 400)
if fp is not None:
    subs = fp.getCalledFunctions(mon)
    lines.append("PREDICATE calls {} functions:".format(len(subs)))
    for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
        lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))
    # 2nd level: decompile the non-external callees
    for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
        ep = str(cf.getEntryPoint())
        n = cf.getName()
        if not ep.startswith("EXTERNAL") and not n.startswith("stlp_std") and not n.startswith("DPVS"):
            f2 = fm.getFunctionAt(cf.getEntryPoint())
            if f2 is not None:
                s2 = f2.getCalledFunctions(mon)
                lines.append("   callees of {} @{}: {}".format(n, ep, [str(x.getEntryPoint()) for x in s2][:12]))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
