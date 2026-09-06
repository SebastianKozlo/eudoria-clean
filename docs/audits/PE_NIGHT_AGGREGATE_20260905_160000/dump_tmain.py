# -*- coding: utf-8 -*-
# dump_tmain.py — decompile ___tmainCRTStartup, find the WinMain call, dump the chain.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_TMAIN_WINMAIN.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []


def dec(addr, label, limit=180):
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


tmain = fm.getFunctionAt(toAddr(0x0095D750))
lines.append("=== ___tmainCRTStartup @0x0095d750")
res = di.decompileFunction(tmain, 120, mon)
if res.decompileCompleted():
    lines.append(res.getDecompiledFunction().getC())
called = tmain.getCalledFunctions(mon)
lines.append("tmain calls {} functions:".format(len(called)))
for cf in sorted(called, key=lambda x: str(x.getEntryPoint())):
    lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))

# WinMain = the largest non-CRT callee (heuristic: the callee with the most body bytes)
best = None
best_size = -1
for cf in called:
    n = cf.getName()
    if n.startswith("___") or n.startswith("_RTC") or n.startswith("__"):
        continue
    body = cf.getBody()
    sz = body.getNumAddresses()
    lines.append("   candidate {} @{} size={}".format(n, cf.getEntryPoint(), sz))
    if sz > best_size:
        best_size = sz
        best = cf

if best is not None:
    lines.append("WINMAIN-CANDIDATE = {} @{} (size {})".format(best.getName(), best.getEntryPoint(), best_size))
    wf = dec(int(str(best.getEntryPoint()), 16), "WINMAIN", 300)
    if wf is not None:
        subs = wf.getCalledFunctions(mon)
        lines.append("WinMain calls {} functions:".format(len(subs)))
        for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
            lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
