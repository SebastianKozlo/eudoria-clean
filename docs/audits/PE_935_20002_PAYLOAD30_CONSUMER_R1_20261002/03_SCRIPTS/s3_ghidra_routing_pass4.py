# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 4: complete the routing chain for 20002.vfs:
#   - class-object machinery: FUN_0073d1f0 (20002 ctor caller), FUN_0073c870 (registry lookup),
#     FUN_0070e100 (method on found object), FUN_0070bf40/FUN_0070cc80 (capacity checks),
#     FUN_00703cd0 (per-class check), callers of FUN_00703e80, FUN_0040e900 (itoa)
#   - family loaders in FUN_0094e890's call series: FUN_00938b00, FUN_009510d0, FUN_00938b80,
#     FUN_009518e0, FUN_0094b910, FUN_0095a2c0, FUN_0094bf40 (+ FUN_0094e470 chain)
#   - the two vtable methods of the 20002 object: FUN_0073c330, FUN_0073a490
#   - FUN_0048e4f0 (the caller of FUN_0094e890)
#   - FUN_0070e470 / FUN_00416030 / FUN_004160a0 / FUN_00417fa0 (startup arg strings)
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass4.py"}

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

def disasm(f, max_ins=900):
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

def decomp(f, timeout=180):
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
    with open(os.path.join(OUT_DIR, "PASS4_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS4_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_0073d1f0": 0x73D1F0,   # caller of the 20002 ctor FUN_0073a3f0
    "FUN_0073c870": 0x73C870,   # registry lookup (used by FUN_00703d70)
    "FUN_0070e100": 0x70E100,   # method on found class object
    "FUN_0070bf40": 0x70BF40,   # capacity check
    "FUN_0070cc80": 0x70CC80,   # capacity check 2
    "FUN_00703cd0": 0x703CD0,   # per-class check in FUN_00703e80 loop
    "FUN_0040e900": 0x40E900,   # itoa (class ID -> string)
    "FUN_0070e470": 0x70E470,   # string s2 in FUN_0070e810 filename
    "FUN_00416030": 0x416030,   # startup: returns object for FUN_0070ec20
    "FUN_004160a0": 0x4160A0,   # startup: returns object for FUN_0070e810
    "FUN_00417fa0": 0x417FA0,   # startup: "Parameters\\" string
    "FUN_0048e4f0": 0x48E4F0,   # caller of FUN_0094e890
    "FUN_00938b00": 0x938B00,   # family driver 1
    "FUN_009510d0": 0x9510D0,   # family driver 2
    "FUN_00938b80": 0x938B80,   # family driver 3
    "FUN_0094b910": 0x94B910,   # family driver 5
    "FUN_0095a2c0": 0x95A2C0,   # family driver 6
    "FUN_0094bf40": 0x94BF40,   # family driver 7
    "FUN_0073c330": 0x73C330,   # 20002 vtable slot 0
    "FUN_0073a490": 0x73A490,   # 20002 vtable slot 1
    "FUN_0070e810b": 0x70E470,  # dup guard
}
del targets["FUN_0070e810b"]
result["functions"] = {}
for tag, v in targets.items():
    info = dump(v, tag)
    if info:
        result["functions"][tag] = info

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
    "FUN_00703e80": callers_of(0x703E80),
    "FUN_0070c680": callers_of(0x70C680),
    "FUN_0073c870": callers_of(0x73C870),
    "FUN_0070e100": callers_of(0x70E100),
    "FUN_0073d1f0": callers_of(0x73D1F0),
    "FUN_009518e0": callers_of(0x9518E0),
    "FUN_0094e610": callers_of(0x94E610),
    "FUN_0094deb0": callers_of(0x94DEB0),
    "FUN_0094c520": callers_of(0x94C520),
    "FUN_0040e900": callers_of(0x40E900),
    "FUN_0073a490": callers_of(0x73A490),
}

with open(os.path.join(OUT_DIR, "PASS4_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS4 DONE")
