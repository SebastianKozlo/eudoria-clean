# -*- coding: utf-8 -*-
# h5_vtable_read.py — read the DisplaySubsystem vtable @0xA7B988 + decompile the methods.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_VTABLE3.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
lines = []

VT = 0x00A7B988
entries = []
for i in range(24):
    try:
        ptr = listing.getInt(toAddr(VT + i * 4))
    except Exception:
        break
    if ptr == 0 or ptr < 0x400000 or ptr > 0xC00000:
        break
    f = fm.getFunctionAt(toAddr(ptr))
    nm = f.getName() if f else "?"
    entries.append((i, ptr, nm))
    lines.append("VT[{}] = 0x{:08x}  {}".format(i, ptr, nm))

for i, ptr, nm in entries[:12]:
    f = fm.getFunctionAt(toAddr(ptr))
    if f is None:
        continue
    lines.append("\n=== VT[{}] @0x{:x} : {}".format(i, ptr, f.getName()))
    res = di.decompileFunction(f, 280, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed)")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
print("\n".join(lines[:30]))
