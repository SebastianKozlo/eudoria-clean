# -*- coding: utf-8 -*-
# disas_throw_context.py — the call targets at the two live frame sites + the thrower identification.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_THROW_DISAS.txt"
mon = ConsoleTaskMonitor()
listing = currentProgram.getListing()
fm = currentProgram.getFunctionManager()
di = DecompInterface()
di.openProgram(currentProgram)
lines = []

for site, label in ((0x0040943F, "FRAME-A"), (0x0040B6D4, "FRAME-B")):
    lines.append("=== {} @0x{:x}: the instructions around the return address".format(label, site))
    start = site - 24
    it = listing.getInstructions(toAddr(start), True)
    for ins in it:
        if ins.getAddress().getOffset() > site + 2:
            break
        f = fm.getFunctionContaining(ins.getAddress())
        fname = f.getName() + "@" + str(f.getEntryPoint()) if f else "?"
        lines.append("  {}  {}   [{}]".format(ins.getAddress(), ins, fname))

# the call TARGETS: whatever the call at site-5 points to
for site, label in ((0x0040943F, "A"), (0x0040B6D4, "B")):
    # find the call instruction whose fall-through == site
    ins = listing.getInstructionAt(toAddr(site - 5))
    if ins is None:
        ins = listing.getInstructionBefore(toAddr(site))
    if ins is not None and "CALL" in str(ins):
        tgt = ins.getFlows()
        lines.append("=== the call before {} @{} -> flows {}".format(label, ins.getAddress(), [str(x) for x in tgt]))
        for t in tgt:
            tf = fm.getFunctionAt(t)
            if tf is not None:
                lines.append("   TARGET FUNCTION: {} @{}".format(tf.getName(), tf.getEntryPoint()))
                res = di.decompileFunction(tf, 200, mon)
                if res.decompileCompleted():
                    c = res.getDecompiledFunction().getC()
                    lines.append(c[:2400])
                break

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
