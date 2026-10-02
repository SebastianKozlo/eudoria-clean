# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 5: the ArkParameterArmor(20002) instance + record-parse path:
#   - FUN_00761540 (ArkParameterArmor instance ctor, 0x58 bytes) + its callers
#   - FUN_004b0980 (caller of FUN_00703e80 class-VFS open driver)
#   - FUN_006ec2d0 / FUN_0070bfd0 (id-enumerator thunks) + callers
#   - ALL refs to DAT_00ba5da8 (the ArkObjectClassImpl<ArkParameterArmor,20002> singleton)
#   - registration helpers: FUN_0070c150, FUN_0070bf10, FUN_00761570, FUN_0070e2f0, FUN_0070d170
#   - the other vtable factories: FUN_0073a5a0, FUN_0073a6b0, FUN_0073a7c0
#   - family-2 name strings: FUN_0094f230, FUN_0094f250, and their inner builders
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass5.py"}

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
    with open(os.path.join(OUT_DIR, "PASS5_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS5_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_00761540": 0x761540,   # ArkParameterArmor instance ctor (0x58 bytes)
    "FUN_004b0980": 0x4B0980,   # caller of FUN_00703e80
    "FUN_006ec2d0": 0x6EC2D0,   # thunk -> FUN_009724e0?
    "FUN_0070bfd0": 0x70BFD0,   # thunk -> FUN_009724e0?
    "FUN_0070c150": 0x70C150,
    "FUN_0070bf10": 0x70BF10,
    "FUN_00761570": 0x761570,   # class list registration
    "FUN_0070e2f0": 0x70E2F0,
    "FUN_0070d170": 0x70D170,   # base dtor helper
    "FUN_0073a5a0": 0x73A5A0,   # vtable factory 2
    "FUN_0073a6b0": 0x73A6B0,   # vtable factory 3
    "FUN_0073a7c0": 0x73A7C0,   # vtable factory 4
    "FUN_0094f230": 0x94F230,   # family-2 name part 1
    "FUN_0094f250": 0x94F250,   # family-2 name part 2
}
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
    "FUN_00761540": callers_of(0x761540),
    "FUN_006ec2d0": callers_of(0x6EC2D0),
    "FUN_0070bfd0": callers_of(0x70BFD0),
    "FUN_004b0980": callers_of(0x4B0980),
}

def refs_to(v, limit=300):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        cf = fm.getFunctionContaining(ref.getFromAddress())
        out.append({"from": "0x%X" % ref.getFromAddress().getOffset(),
                    "type": str(ref.getReferenceType()),
                    "in_function": cf.getName() if cf else None,
                    "in_function_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
        if len(out) >= limit:
            break
    return out

result["refs_to_DAT_00ba5da8"] = refs_to(0xBA5DA8)

with open(os.path.join(OUT_DIR, "PASS5_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS5 DONE")
