# -*- coding: utf-8 -*-
# dump_fatal.py — FUN_007c5310 (the only exit() caller) + ITS callers.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_FATAL_007C5310.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
refmgr = currentProgram.getReferenceManager()
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


f5310 = dec(0x007C5310, "FATAL-EXIT", 300)
if f5310 is not None:
    callers = set()
    for ref in refmgr.getReferencesTo(f5310.getEntryPoint()):
        if ref.getReferenceType().isCall():
            sf = fm.getFunctionContaining(ref.getFromAddress())
            if sf is not None:
                callers.add((sf.getName(), str(sf.getEntryPoint())))
    lines.append("FUN_007c5310 callers ({}):".format(len(callers)))
    for n, ep in sorted(callers, key=lambda x: x[1]):
        lines.append("   -> {} @{}".format(n, ep))
    # decompile each caller (bounded to 24)
    for n, ep in sorted(callers, key=lambda x: x[1])[:24]:
        dec(int(ep, 16), "FATAL-CALLER-" + n, 200)

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
