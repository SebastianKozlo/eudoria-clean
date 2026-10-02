# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 14: the generic value GETTERS (readers of instance value_array[desc.field]):
# decompile the accessor family around FUN_00726450/90/0x726d10/0x726f00/0x726b50/0x726c00,
# and census the getter callers that pass the immediate tag 0x11 (=17).
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
rm = program.getReferenceManager()

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass14.py"}

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

def decomp(f, timeout=120):
    ifc = DecompInterface()
    ifc.openProgram(program)
    try:
        r = ifc.decompileFunction(f, timeout, monitor)
        if r.decompileCompleted():
            return r.getDecompiledFunction().getC()
        return "DECOMP_FAILED: %s" % r.getErrorMessage()
    finally:
        ifc.dispose()

# 1. decompile the getter candidates
getters = {
    "FUN_00726450": 0x726450,
    "FUN_00726490": 0x726490,
    "FUN_00726d10": 0x726D10,
    "FUN_00726f00": 0x726F00,
    "FUN_00726b50": 0x726B50,
    "FUN_00726c00": 0x726C00,
    "FUN_00726560": 0x726560,
    "FUN_00726510": 0x726510,
    "FUN_007275a0": 0x7275A0,
    "FUN_00727480": 0x727480,
    "FUN_00727e90": 0x727E90,
    "FUN_00727f10": 0x727F10,
    "FUN_00727110": 0x727110,
    "FUN_00726d70": 0x726D70,
}
result["getters"] = {}
for tag, v in getters.items():
    f = fn_at(v)
    info = fn_info(f)
    if info is None:
        result["getters"][tag] = None
        continue
    c = decomp(f)
    result["getters"][tag] = {"info": info, "decomp": (c or "")[:1800]}

# 2. for each getter with direct callers, census callsites passing the immediate 0x11
def callers_of(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        if ref.getReferenceType().isCall():
            cf = fm.getFunctionContaining(ref.getFromAddress())
            out.append({"call_site": "0x%X" % ref.getFromAddress().getOffset(),
                        "caller": cf.getName() if cf else None,
                        "caller_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

result["getter_callers"] = {}
for tag, v in getters.items():
    result["getter_callers"][tag] = callers_of(v)

# 3. examine the instruction before each getter call for the tag argument 0x11
def arg_context(v):
    sites = []
    for ref in rm.getReferencesTo(addr(v)):
        if not ref.getReferenceType().isCall():
            continue
        from_a = ref.getFromAddress()
        ctx = []
        prev = from_a.subtract(0x18)
        ins_iter = listing.getInstructions(prev, True)
        for ins in ins_iter:
            if ins.getAddress().getOffset() > from_a.getOffset():
                break
            ctx.append("%s %s" % (ins.getAddress().toString(), ins.toString()))
        sites.append({"call_site": "0x%X" % from_a.getOffset(),
                      "ctx": ctx[-8:]})
    return sites

result["getter_call_arg_context"] = {}
for tag, v in getters.items():
    result["getter_call_arg_context"][tag] = arg_context(v)

with open(os.path.join(OUT_DIR, "PASS14_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS14 DONE")
