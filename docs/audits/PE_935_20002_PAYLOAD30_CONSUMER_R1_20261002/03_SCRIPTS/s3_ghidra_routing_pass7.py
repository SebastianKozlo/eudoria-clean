# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 7: FUN_0070de10 (create-instance-on-miss - candidate factory+parse bridge),
# the ArkParameterArmor instance vtable at 0xA878BC + its methods, the map lookup, and
# the FUN_0070e100 callers.
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass7.py"}

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

def disasm(f, max_ins=1500):
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

def decomp(f, timeout=240):
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
    with open(os.path.join(OUT_DIR, "PASS7_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS7_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_0070de10": 0x70DE10,   # create-instance-on-miss (factory + parse bridge candidate)
    "FUN_004d1430": 0x4D1430,   # instance map lookup
    "FUN_0070e1f0": 0x70E1F0,   # FUN_0070e100 caller family
    "FUN_00704550": 0x704550,
    "FUN_007046a0": 0x7046A0,
    "FUN_00705f90": 0x705F90,
    "FUN_00415470": 0x415470,   # global state check
    "FUN_0040e900": 0x40E900,   # itoa (re-dump for pass7 completeness)
}
result["functions"] = {}
for tag, v in targets.items():
    info = dump(v, tag)
    if info:
        result["functions"][tag] = info

def read_u32s(v, n):
    buf = jzeros(4 * n, "b")
    try:
        mem.getBytes(addr(v), buf)
    except:
        return None
    b = bytes(bytearray([x & 0xFF for x in buf]))
    return _s.unpack("<%dI" % n, b)

# ArkParameterArmor instance vtable at 0xA878BC
vt = read_u32s(0xA878BC, 40)
result["vtable_0xa878bc_raw"] = ["0x%X" % x for x in vt] if vt else None
result["vtable_0xa878bc_functions"] = []
if vt:
    for i, p in enumerate(vt):
        info = fn_info(fn_at(p))
        if info is None:
            break
        result["vtable_0xa878bc_functions"].append({"slot": i, "ptr": "0x%X" % p, "function": info})
        dump(p, "IVT_%02d_%s" % (i, info["name"]))

def callers_of(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        if ref.getReferenceType().isCall():
            cf = fm.getFunctionContaining(ref.getFromAddress())
            out.append({"call_site": "0x%X" % ref.getFromAddress().getOffset(),
                        "caller": cf.getName() if cf else None,
                        "caller_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

result["callers"] = {
    "FUN_0070de10": callers_of(0x70DE10),
    "FUN_0070e100": callers_of(0x70E100),
    "FUN_00971ad0": callers_of(0x971AD0),
    "FUN_00412430": callers_of(0x412430),
}

with open(os.path.join(OUT_DIR, "PASS7_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS7 DONE")
