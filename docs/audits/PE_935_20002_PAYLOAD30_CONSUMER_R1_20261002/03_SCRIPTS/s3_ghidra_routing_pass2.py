# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Second pass: cursor/read primitives + class-family plumbing for the 20002.vfs parse chain.
# Outputs into 01_RAW\GHIDRA_ROUTING\ (PASS2_* files).
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass2.py (Ghidra headless postScript, pass 2)"}

def addr(v):
    return program.getAddressFactory().getAddress("0x%X" % v)

def fn_at(v):
    return fm.getFunctionContaining(addr(v))

def fn_info(f):
    if f is None:
        return None
    body = f.getBody()
    return {"name": f.getName(), "entry": "0x%X" % f.getEntryPoint().getOffset(),
            "body_min": "0x%X" % body.getMinAddress().getOffset(),
            "body_max": "0x%X" % body.getMaxAddress().getOffset(),
            "size": body.getMaxAddress().getOffset() - body.getMinAddress().getOffset() + 1}

def disasm(f, max_ins=600):
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

def dump(v, tag):
    f = fn_at(v)
    info = fn_info(f)
    if info is None:
        result.setdefault("missing", []).append({"va": "0x%X" % v, "tag": tag})
        return None
    with open(os.path.join(OUT_DIR, "PASS2_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    with open(os.path.join(OUT_DIR, "PASS2_DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(decomp(f) or "")
    return info

targets = {
    "FUN_004063d0": 0x4063D0,   # read u32 from cursor? (id check in FUN_00971ad0)
    "FUN_006b22d0": 0x6B22D0,   # node id getter
    "FUN_00971780": 0x971780,   # index lookup by id
    "FUN_00979d20": 0x979D20,   # node file offset getter
    "FUN_00746550": 0x746550,   # size getter (header/node)
    "FUN_0040e260": 0x40E260,   # read file bytes into cursor
    "FUN_009721d0": 0x9721D0,   # index node builder
    "FUN_00972280": 0x972280,   # index node builder (id==0 branch)
    "FUN_00979d00": 0x979D00,   # stride advance calc
    "FUN_00979cc0": 0x979CC0,   # index init (base param)
    "FUN_00979d30": 0x979D30,   # parse 16-byte header into reader state
    "FUN_004123d0": 0x4123D0,   # header id getter
    "FUN_0094e470": 0x94E470,   # caller of the record loop FUN_0094e1d0
    "FUN_0094b9e0": 0x94B9E0,   # filename part 1 (open chain)
    "FUN_0094ba00": 0x94BA00,   # filename part 2 (open chain)
    "FUN_00959060": 0x959060,   # element init (before FUN_0094bd30)
    "FUN_00972380": 0x972380,   # VFS reader object constructor
    "FUN_009724e0": 0x9724E0,   # id enumerator
    "FUN_009728d0": 0x9728D0,   # index count helper
    "FUN_00417eb0": 0x417EB0,   # position recorder (id==0 branch)
    "FUN_0094fc50": 0x94FC50,   # sibling family append
    "FUN_0040e160": 0x40E160,   # cursor alloc tag helper (seen in loop)
    "FUN_0040e180": 0x40E180,   # cursor free helper
    "FUN_008e0110": 0x8E0110,   # post-parse per-record call
    "FUN_0072fa30": 0x72FA30,   # FUN_00972df0 caller (templates family?)
}
result["functions"] = {}
for tag, v in targets.items():
    info = dump(v, tag)
    if info:
        result["functions"][tag] = info

# raw data at DAT_00b6c3d8 (used by the open filename chain) and DAT_00ba8df4/df8 region
from jarray import zeros as jzeros
def hexdump(v, n):
    buf = jzeros(n, "b")
    try:
        program.getMemory().getBytes(addr(v), buf)
    except:
        return "<READ_FAILED>"
    return " ".join("%02X" % (b & 0xFF) for b in buf)

result["data_dumps"] = {
    "DAT_00b6c3d8_16B": hexdump(0xB6C3D8, 16),
    "DAT_00ba8df0_32B": hexdump(0xBA8DF0, 32),
    "DAT_00b6c3d8_deref_target_if_pointer": None,
}
# DAT_00b6c3d8 likely holds a pointer; read it and dump the target
import struct as _s
buf = jzeros(4, "b")
try:
    program.getMemory().getBytes(addr(0xB6C3D8), buf)
    ptr = _s.unpack("<i", bytes(bytearray([b & 0xFF for b in buf])))[0]
    result["data_dumps"]["DAT_00b6c3d8_value_hex"] = "0x%X" % (ptr & 0xFFFFFFFF)
    if 0x400000 < (ptr & 0xFFFFFFFF) < 0xC00000:
        result["data_dumps"]["DAT_00b6c3d8_deref_target_if_pointer"] = hexdump(ptr & 0xFFFFFFFF, 96)
except Exception as e:
    result["data_dumps"]["DAT_00b6c3d8_value_hex"] = "ERR %s" % e

# callers/xrefs for the pass-2 family
def callers_of(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        if ref.getReferenceType().isCall():
            cf = fm.getFunctionContaining(ref.getFromAddress())
            out.append({"call_site": "0x%X" % ref.getFromAddress().getOffset(),
                        "caller": cf.getName() if cf else None,
                        "caller_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

result["callers"] = {}
for tag, v in [("FUN_0094e470", 0x94E470), ("FUN_0094b9e0", 0x94B9E0), ("FUN_0094ba00", 0x94BA00),
               ("FUN_004063d0", 0x4063D0), ("FUN_00959060", 0x959060), ("FUN_009724e0", 0x9724E0)]:
    result["callers"][tag] = callers_of(v)

def refs_to(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        cf = fm.getFunctionContaining(ref.getFromAddress())
        out.append({"from": "0x%X" % ref.getFromAddress().getOffset(),
                    "type": str(ref.getReferenceType()),
                    "in_function": cf.getName() if cf else None,
                    "in_function_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

result["refs_to_DAT_00ba8df4"] = refs_to(0xBA8DF4)
result["refs_to_DAT_00ba8df8"] = refs_to(0xBA8DF8)
result["refs_to_DAT_00ba8e1c"] = refs_to(0xBA8E1C)
result["refs_to_DAT_00ba8e18"] = refs_to(0xBA8E18)
result["refs_to_DAT_00b6c3d8"] = refs_to(0xB6C3D8)

with open(os.path.join(OUT_DIR, "PASS2_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS2 DONE -> %s" % OUT_DIR)
