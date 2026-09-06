# -*- coding: utf-8 -*-
# dump_exit_hunt.py — (a) all callers of the exit() import thunk; (b) decompile the 6 init functions.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.symbol import RefType

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_EXIT_HUNT.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
lines = []

# (a) find the exit() thunk function + its callers
exit_funcs = []
for f in fm.getFunctions(True):
    if f.getName() == "exit":
        exit_funcs.append(f)
lines.append("exit thunks found: {}".format(len(exit_funcs)))
callers = set()
refmgr = currentProgram.getReferenceManager()
for ef in exit_funcs:
    lines.append("thunk: {} @{}".format(ef.getName(), ef.getEntryPoint()))
    for ref in refmgr.getReferencesTo(ef.getEntryPoint()):
        if ref.getReferenceType().isCall():
            src = ref.getFromAddress()
            sf = fm.getFunctionContaining(src)
            if sf is not None:
                callers.add((sf.getName(), str(sf.getEntryPoint())))
lines.append("exit() callers ({}):".format(len(callers)))
for n, ep in sorted(callers, key=lambda x: x[1]):
    lines.append("   -> {} @{}".format(n, ep))


def dec(addr, label, limit=240):
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


# (b) the 6 init functions from WinMain
for va, lab in ((0x00406ec0, "INIT-1"), (0x00406a70, "INIT-2"), (0x00406560, "INIT-3"),
                (0x00402e90, "CREATE-OBJ"), (0x00404e50, "INIT-5"), (0x004055f0, "RUN")):
    dec(va, lab, 300)

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
