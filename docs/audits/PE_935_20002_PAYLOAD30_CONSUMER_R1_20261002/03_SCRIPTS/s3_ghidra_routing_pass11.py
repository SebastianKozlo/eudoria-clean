# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 11: the TLV schema + value reader:
#   FUN_0070c180 (tag -> descriptor {+4 type?, +8 field index}) and its table,
#   FUN_0075f660 (cursor + dest -> read one value) - THE payload+0x30 READ.
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass11.py"}

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
    with open(os.path.join(OUT_DIR, "PASS11_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS11_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_0070c180": 0x70C180,   # tag -> descriptor
    "FUN_0075f660": 0x75F660,   # value reader (cursor, dest)
    "FUN_0075f5c0": 0x75F5C0,   # trait registration (schema link)
    "FUN_0075f6c0": 0x75F6C0,
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

result["callers"] = {"FUN_0070c180": callers_of(0x70C180), "FUN_0075f660": callers_of(0x75F660)}

with open(os.path.join(OUT_DIR, "PASS11_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS11 DONE")
