# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 13: the typed value readers (FUN_00412540 type1, FUN_00412500 type2, FUN_004099c0 type4,
# FUN_0040e020 type3), the descriptor setter FUN_0070cbc0, value-array init FUN_0075f6d0/FUN_00412c50,
# and the instance vtable slot 3 (+0xC) nested reader for ArkParameterArmor.
# @category PE_935_20002
import json
import os
import struct as _s
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from jarray import zeros as jzeros

OUT_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\GHIDRA_ROUTING"
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

monitor = ConsoleTaskMonitor()
program = currentProgram
fm = program.getFunctionManager()
listing = program.getListing()
rm = program.getReferenceManager()
mem = program.getMemory()

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass13.py"}

def addr(v):
    return program.getAddressFactory().getAddress("0x%X" % v)

def fn_at(v):
    return fm.getFunctionContaining(addr(v))

def fn_info(f):
    if f is None:
        return None
    body = f.getBody()
    return {"name": f.getName(), "entry": "0x%X" % f.getEntryPoint().getOffset(),
            "size": body.getMaxAddress().getOffset() - body.getMinAddress().getOffset() + 1}

def disasm(f, max_ins=3000):
    out = []
    if f is None:
        return out
    it = listing.getInstructions(f.getBody(), True)
    n = 0
    for ins in it:
        out.append("%s  %s" % (ins.getAddress().toString(), ins.toString()))
        n += 1
        if n >= max_ins:
            break
    return out

def decomp(f, timeout=300):
    ifc = DecompInterface()
    ifc.openProgram(program)
    try:
        r = ifc.decompileFunction(f, timeout, monitor)
        if r.decompileCompleted():
            return r.getDecompiledFunction().getC()
        return "DECOMP_FAILED: %s" % r.getErrorMessage()
    finally:
        ifc.dispose()

def dump(v, tag):
    f = fn_at(v)
    info = fn_info(f)
    if info is None:
        result.setdefault("missing", []).append({"va": "0x%X" % v, "tag": tag})
        return None
    with open(os.path.join(OUT_DIR, "PASS13_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS13_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_00412540": 0x412540,   # type-1 reader (tags 0xD,0xE,0x10,0x11)
    "FUN_00412500": 0x412500,   # type-2 reader (tags 7, 0xC)
    "FUN_004099c0": 0x4099C0,   # type-4 reader (tag 1)
    "FUN_0040e020": 0x40E020,   # type-3 reader
    "FUN_0070cbc0": 0x70CBC0,   # descriptor setter (field index mapping)
    "FUN_0075f6d0": 0x75F6D0,   # value-slot init
    "FUN_00412c50": 0x412C50,   # value-array alloc
    "FUN_0070bf20": 0x70BF20,
    "FUN_0070e2f0": 0x70E2F0,   # count setter (0x12)
}
result["functions"] = {}
for tag, v in targets.items():
    info = dump(v, tag)
    if info:
        result["functions"][tag] = info

# ArkParameterArmor instance vtable 0xA878BC slot dump was done in pass7 - fetch slot 3 (+0xC)
d7 = None
try:
    with open(os.path.join(OUT_DIR, "PASS7_GHIDRA_DUMP.json")) as fh:
        d7 = json.load(fh)
    result["arkparametararmor_ivt"] = d7.get("vtable_0xa878bc_functions")
except Exception as e:
    result["arkparametararmor_ivt"] = "ERR %s" % e

with open(os.path.join(OUT_DIR, "PASS13_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS13 DONE")
