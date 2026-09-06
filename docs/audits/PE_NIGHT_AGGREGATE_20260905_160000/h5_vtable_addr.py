# -*- coding: utf-8 -*-
# h5_vtable_addr.py — get the DisplaySubsystem::vftable address from the ctor's disassembly.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_VTABLE2.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
lines = []

# disassemble the ctor 0x48aef0 to find the vtable offset store
it = listing.getInstructions(toAddr(0x0048AEF0), True)
vt_addr = None
for ins in it:
    lines.append("{}  {}".format(ins.getAddress(), ins))
    if str(ins).startswith("MOV") and "dword ptr [E" in str(ins).upper():
        # the first store = the vtable
        refs = ins.getFlows()
        for r in refs:
            vt_addr = r
            break
        break

lines.append("\nthe vtable address = {}".format(vt_addr))

if vt_addr is not None:
    lines.append("=== the vtable entries:")
    entries = []
    for i in range(24):
        try:
            ptr = listing.getInt(toAddr(vt_addr.getOffset() + i * 4))
        except Exception as ex:
            lines.append("read fail: {}".format(ex))
            break
        if ptr == 0:
            break
        f = fm.getFunctionAt(toAddr(ptr))
        nm = f.getName() if f else "?"
        entries.append((i, ptr, nm))
        lines.append("  [{}] 0x{:08x}  {}".format(i, ptr, nm))
    # decompile the first 10 methods
    for i, ptr, nm in entries[:10]:
        f = fm.getFunctionAt(toAddr(ptr))
        if f is None:
            continue
        lines.append("\n=== VT[{}] @0x{:x} : {}".format(i, ptr, f.getName()))
        res = di.decompileFunction(f, 260, mon)
        if res.decompileCompleted():
            lines.append(res.getDecompiledFunction().getC())
        else:
            lines.append("(decompile failed)")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
