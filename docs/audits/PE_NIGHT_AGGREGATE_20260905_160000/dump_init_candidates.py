# -*- coding: utf-8 -*-
# dump_init_candidates.py — the 7 pre-registry deep-init callees (one of them = the display failure).
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_INIT_CANDIDATES.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

CANDS = [(0x00728140, "C1-00728140"), (0x00797280, "C2-00797280"), (0x00743fd0, "C3-00743fd0"),
         (0x0092f7d0, "C4-0092f7d0"), (0x004061a0, "C5-004061a0"), (0x0070bf00, "C6-0070bf00"),
         (0x00409260, "C7-00409260")]


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


for va, lab in CANDS:
    f = dec(va, lab, 300)
    if f is not None:
        subs = f.getCalledFunctions(mon)
        lines.append("   callees: " + ", ".join("{}@{}".format(x.getName(), str(x.getEntryPoint())) for x in subs)[:800])

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
