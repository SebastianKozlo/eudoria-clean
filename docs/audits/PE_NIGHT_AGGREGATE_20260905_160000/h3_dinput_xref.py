# -*- coding: utf-8 -*-
# h3_dinput_xref.py — find the DirectInput8Create call site + decompile the caller chain.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.symbol import RefType

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DINPUT_XREF.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
refmgr = currentProgram.getReferenceManager()
lines = []

# find all DINPUT8 import thunks
thunks = []
for f in fm.getFunctions(True):
    if "DirectInput8Create" in f.getName():
        thunks.append(f)
        lines.append("thunk: {} @{}".format(f.getName(), f.getEntryPoint()))

callers = set()
for tf in thunks:
    for ref in refmgr.getReferencesTo(tf.getEntryPoint()):
        rt = ref.getReferenceType()
        sf = fm.getFunctionContaining(ref.getFromAddress())
        lines.append("ref to thunk: {} from {} (type {})".format(rt, ref.getFromAddress(),
                     sf.getName() + "@" + str(sf.getEntryPoint()) if sf else "?"))
        if sf is not None:
            callers.add((sf.getName(), str(sf.getEntryPoint())))

lines.append("\ncallers: {}".format(sorted(callers)))


def dec(addr, label, limit=400):
    f = fm.getFunctionAt(toAddr(addr))
    if f is None:
        lines.append("=== {} @0x{:x}: NO FUNCTION".format(label, addr))
        return
    lines.append("=== {} @0x{:x} : {}".format(label, addr, f.getName()))
    res = di.decompileFunction(f, limit, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))


for n, ep in sorted(callers, key=lambda x: x[1])[:4]:
    dec(int(ep, 16), "DINPUT-CALLER-" + n, 400)

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
print("\n".join(lines[:60]))
