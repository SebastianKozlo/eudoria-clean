# -*- coding: utf-8 -*-
# dump_gate.py — decompile FUN_00407270 (THE display gate) + its callees (the predicate).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_GATE_00407270.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []


def dec(addr, label, limit=240):
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


g = dec(0x00407270, "THE-GATE-FUN_00407270", 300)
if g is not None:
    subs = g.getCalledFunctions(mon)
    lines.append("gate calls {} functions:".format(len(subs)))
    for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
        lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))
        # decompile each callee too (the predicate lives one level down)
    for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
        ep = str(cf.getEntryPoint())
        if not ep.startswith("EXTERNAL") and not cf.getName().startswith("stlp_std"):
            dec(int(ep, 16), "GATE-CALLEE", 240)

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
