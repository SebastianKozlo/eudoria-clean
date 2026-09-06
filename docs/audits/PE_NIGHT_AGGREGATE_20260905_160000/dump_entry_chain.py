# -*- coding: utf-8 -*-
# dump_entry_chain.py — Ghidra headless post-script (Jython 2.7 compatible: no f-strings)
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_WINMAIN_CHAIN.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()

lines = []


def decompile_and_log(addr, label):
    f = fm.getFunctionAt(addr)
    if f is None:
        lines.append("=== {} @{}: NO FUNCTION".format(label, addr))
        return None
    lines.append("=== {} @{} : {}".format(label, addr, f.getName()))
    res = di.decompileFunction(f, 120, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    return f


entry = toAddr(0x0095DA11)
ef = decompile_and_log(entry, "CRT-ENTRY")

winmain = None
if ef is not None:
    called = ef.getCalledFunctions(mon)
    lines.append("entry calls {} functions:".format(len(called)))
    for cf in called:
        lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))
    best = None
    for cf in called:
        if cf.getName().find("WinMain") >= 0:
            best = cf
    if best is None and len(called) > 0:
        for cf in sorted(called, key=lambda x: str(x.getEntryPoint())):
            n = cf.getName()
            if n.startswith("FUN_"):
                best = cf
                break
    winmain = best

if winmain is not None:
    wf = decompile_and_log(winmain.getEntryPoint(), "WINMAIN-CANDIDATE")
    if wf is not None:
        subs = wf.getCalledFunctions(mon)
        lines.append("WinMain calls {} functions:".format(len(subs)))
        for cf in sorted(subs, key=lambda x: str(x.getEntryPoint())):
            lines.append("   -> {} @{}".format(cf.getName(), cf.getEntryPoint()))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
