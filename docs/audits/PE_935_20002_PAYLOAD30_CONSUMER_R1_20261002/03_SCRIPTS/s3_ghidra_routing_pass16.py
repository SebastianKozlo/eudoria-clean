# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 16 (final): FUN_0070c680 disasm+decomp (the "<classID>.vfs" open site on the class object).
# @category PE_935_20002
import json
import os
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\GHIDRA_ROUTING"
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

monitor = ConsoleTaskMonitor()
program = currentProgram
fm = program.getFunctionManager()
listing = program.getListing()

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass16.py"}

def addr(v):
    return program.getAddressFactory().getAddress("0x%X" % v)

f = fm.getFunctionContaining(addr(0x70C680))
body = f.getBody()
lines = []
it = listing.getInstructions(body, True)
for ins in it:
    lines.append("%s  %s" % (ins.getAddress().toString(), ins.toString()))
with open(os.path.join(OUT_DIR, "PASS16_DISASM_FUN_0070c680.txt"), "w") as fh:
    fh.write("\n".join(lines))
ifc = DecompInterface()
ifc.openProgram(program)
r = ifc.decompileFunction(f, 240, monitor)
with open(os.path.join(OUT_DIR, "PASS16_DECOMP_FUN_0070c680.txt"), "w") as fh:
    fh.write(r.getDecompiledFunction().getC() if r.decompileCompleted() else "FAIL")
ifc.dispose()
result["ok"] = True
with open(os.path.join(OUT_DIR, "PASS16_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("PASS16 DONE")
