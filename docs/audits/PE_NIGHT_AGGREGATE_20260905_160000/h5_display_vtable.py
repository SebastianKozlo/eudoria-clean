# -*- coding: utf-8 -*-
# h5_display_vtable.py — the DisplaySubsystem::vftable methods + the DPVS::Library function census.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_H5_VTABLE.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
st = currentProgram.getSymbolTable()
listing = currentProgram.getListing()
lines = []

# (a) find the DisplaySubsystem::vftable symbol
syms = st.getSymbols("DisplaySubsystem::vftable")
vt_addr = None
for s in syms:
    lines.append("symbol: {} @{}".format(s.getName(), s.getAddress()))
    vt_addr = s.getAddress()

vtable_entries = []
if vt_addr is not None:
    lines.append("\n=== the vtable entries:")
    for i in range(20):
        try:
            ptr = listing.getInt(vt_addr.add(i * 4))
        except Exception:
            break
        if ptr == 0:
            break
        f = fm.getFunctionAt(toAddr(ptr))
        nm = f.getName() if f else "?"
        vtable_entries.append((i, ptr, nm))
        lines.append("  [{}] 0x{:08x}  {}".format(i, ptr, nm))


def dec(addr, label, limit=300):
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
    lines.append("")


# decompile the first 8 vtable methods (the init/open/enum candidates)
for i, ptr, nm in vtable_entries[:8]:
    dec(ptr, "VT[{}]".format(i), 300)

# (b) the DPVS-named functions census
lines.append("\n=== the DPVS-named functions:")
dpvs_funcs = []
for f in fm.getFunctions(True):
    n = f.getName()
    if "DPVS" in n:
        dpvs_funcs.append((str(f.getEntryPoint()), n))
for ep, n in sorted(dpvs_funcs):
    lines.append("  {}  {}".format(ep, n))

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
print("vtable entries: {}".format(vtable_entries[:8]))
print("DPVS funcs: {}".format(len(dpvs_funcs)))
