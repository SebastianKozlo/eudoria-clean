# ghidra_post_decomp.py - Jython script for analyzeHeadless (Ghidra 11.2.1)
# PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913
# Decompiles: (a) all functions that call FUN_004154f0 (manager getter);
# (b) the Z-provider family region functions; (c) FUN_00853a80 consumers.
# Output: one .c file per function under the given output dir.
# STATIC-ONLY analysis of the already-imported Entropia.exe program.

import os

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913\01_RAW\DECOMP_P2"

# function entries to decompile (passed as containing functions of the sites)
SITES = [
    0x42bdd6, 0x42be12, 0x42be44, 0x42c19b, 0x442312, 0x44a925, 0x44a9ef,
    0x455cb3, 0x45ba6f, 0x45ba76, 0x45bf90, 0x46e604, 0x48d255, 0x48ef8f,
    0x4c47d3, 0x4c4853, 0x4c497a, 0x511375, 0x5219e7, 0x567662, 0x567a66,
    0x58e253, 0x5b629d, 0x5f587a, 0x5f603a, 0x5f6e7a, 0x5f7232, 0x67be1e,
    0x67ce5f, 0x846bec, 0x846c61, 0x84a129, 0x84a4b3, 0x857863, 0x85b41d,
    0x85b783, 0x85b848, 0x861491, 0x8614b0,
    # Z-provider siblings + consumers (containing functions)
    0x48c05b, 0x48c0a9, 0x48c0fb, 0x48c14d, 0x48c19f, 0x48c1e5, 0x48c22b,
    0x48c271, 0x48c2b7, 0x4c46c0, 0x4c47f0, 0x853a80, 0x853c3a, 0x853c6b,
    0x755f90, 0x7576d4, 0x7577d8, 0x850959, 0x96de27, 0x96df45, 0x96dfed,
    0x96e025,
    # direct extras for the run
    0x4154f0, 0x8550c0, 0x8553d0, 0x8544d0, 0x856190, 0x7453d0, 0x7343e0,
    0x745360, 0x730f60, 0x730f90, 0x730fb0, 0x730fd0, 0x797280, 0x6b22d0,
    0x528e50, 0x5247c0, 0x509330, 0x414130, 0x4c4640, 0x765930, 0x85b3e0,
    0x85b750, 0x85adb0, 0x412430, 0x4124b0, 0x412f10, 0x413590, 0x413460,
    0x8544d0,
]

fm = currentProgram.getFunctionManager()
af = currentProgram.getAddressFactory()
decomp = DecompInterface()
decomp.openProgram(currentProgram)
monitor = ConsoleTaskMonitor()

if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)
done = set()
count = 0
for site in SITES:
    addr = af.getAddress(hex(site))
    func = fm.getFunctionContaining(addr)
    if func is None:
        continue
    ep = func.getEntryPoint().getOffset()
    if ep in done:
        continue
    done.add(ep)
    res = decomp.decompileFunction(func, 120, monitor)
    name = "F%08X.c" % ep
    path = os.path.join(OUT_DIR, name)
    with open(path, "w") as f:
        f.write("// DECOMPILED (Ghidra 11.2.1) from Entropia.exe\n")
        f.write("// function entry %s (requested via site %s)\n" % (hex(ep), hex(site)))
        if res.decompileCompleted():
            f.write(res.getDecompiledFunction().getC())
        else:
            f.write("// DECOMPILE FAILED: %s\n" % res.getErrorMessage())
    count += 1

print("decompiled %d functions -> %s" % (count, OUT_DIR))
