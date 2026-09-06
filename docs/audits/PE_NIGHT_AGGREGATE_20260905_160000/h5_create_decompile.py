# -*- coding: utf-8 -*-
# h5_create_decompile.py — create functions at the un-analyzed DisplaySubsystem addresses + decompile.
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.app.cmd.disassemble import DisassembleCommand

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\GHIDRA_DSS_CREATED.txt"
mon = ConsoleTaskMonitor()
di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
lines = []

TARGETS = [0x0048B110, 0x0048B520, 0x0048B0E0, 0x0048B0A0]

for va in TARGETS:
    a = toAddr(va)
    f = fm.getFunctionAt(a)
    if f is None:
        # disassemble first then create
        cmd = DisassembleCommand(a, None, True)
        cmd.applyTo(currentProgram, mon)
        c2 = CreateFunctionCmd(a)
        c2.applyTo(currentProgram, mon)
        f = fm.getFunctionAt(a)
    if f is None:
        lines.append("=== @0x{:x}: CREATE FAILED".format(va))
        continue
    lines.append("=== @0x{:x} : {} (size {})".format(va, f.getName(), f.getBody().getNumAddresses()))
    res = di.decompileFunction(f, 400, mon)
    if res.decompileCompleted():
        lines.append(res.getDecompiledFunction().getC())
    else:
        lines.append("(decompile failed: {})".format(res.getErrorMessage()))
    lines.append("")

open(OUT, "w").write("\n".join(lines))
print("written " + OUT)
