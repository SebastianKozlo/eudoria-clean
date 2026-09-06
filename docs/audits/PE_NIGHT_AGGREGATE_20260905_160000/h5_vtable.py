# -*- coding: utf-8 -*-
# h5_vtable.py — the DisplaySubsystem::vftable: locate, dump entries, decompile the methods.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DISPLAYSUBSYSTEM_VTABLE.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
st = currentProgram.getSymbolTable()
listing = currentProgram.getListing()
lines = []

# 1) find the vftable symbol
vtaddr = None
for s in st.getAllSymbols(True):
    if "DisplaySubsystem::vftable" in str(s.getName()):
        vtaddr = s.getAddress()
        lines.append("vftable symbol: {} @{}".format(s.getName(), vtaddr))
        break

if vtaddr is None:
    # fallback: find the ctor's first store — search for the label at the data
    # where FUN_0048aef0's *param_1 = X
    lines.append("symbol not found; searching the listing for 'DisplaySubsystem'")
    addr = currentProgram.getMemory().getMinAddress()
    it = listing.getDefinedData(True)
    for d in it:
        if "DisplaySubsystem" in str(d.getLabel()):
            lines.append("data label: {} @{}".format(d.getLabel(), d.getAddress()))
            vtaddr = d.getAddress()
            break

if vtaddr is not None:
    # 2) dump the vtable entries (the function pointers)
    import ghidra.program.model.address as gaddr
    entries = []
    a = vtaddr
    for i in range(12):
        val = listing.getInt(a)
        if val == 0:
            break
        va = gaddr.Address(toAddr(val).getOffset()) if False else toAddr(val)
        f = fm.getFunctionAt(va)
        entries.append((i, val, f))
        a = a.add(4)
        lines.append("vtable[{}] = 0x{:08x} -> {}".format(i, val & 0xFFFFFFFF,
                    f.getName() + "@" + str(f.getEntryPoint()) if f else "?"))
    # 3) decompile the first 8 methods
    for i, val, f in entries[:8]:
        if f is None:
            continue
        lines.append("=== METHOD vtable[{}] : {} @{}".format(i, f.getName(), f.getEntryPoint()))
        res = di.decompileFunction(f, 300, mon)
        if res.decompileCompleted():
            lines.append(res.getDecompiledFunction().getC())
        else:
            lines.append("(decompile failed: {})".format(res.getErrorMessage()))
        lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
print("\n".join(lines[:40]))
