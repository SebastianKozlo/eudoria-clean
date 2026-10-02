# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 3: the class-20002 ArkObjectClass object: vtable 0xa86fe0, its virtual methods,
# the constructor callers, FUN_00958d90 (filename number-string), DAT_00b6c3d8 writers,
# and the load-driver chain (FUN_0070e810/FUN_0070ec20 internals).
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
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass3.py"}

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

def disasm(f, max_ins=800):
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

def dump(v, tag, do_decomp=True):
    f = fn_at(v)
    info = fn_info(f)
    if info is None:
        result.setdefault("missing", []).append({"va": "0x%X" % v, "tag": tag})
        return None
    with open(os.path.join(OUT_DIR, "PASS3_DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    if do_decomp:
        with open(os.path.join(OUT_DIR, "PASS3_DECOMP_%s.txt" % tag), "w") as fh:
            fh.write(decomp(f) or "")
    return info

def read_u32s(v, n):
    buf = jzeros(4 * n, "b")
    try:
        mem.getBytes(addr(v), buf)
    except:
        return None
    b = bytes(bytearray([x & 0xFF for x in buf]))
    return _s.unpack("<%dI" % n, b)

def read_ascii(v, n=64):
    buf = jzeros(n, "b")
    try:
        mem.getBytes(addr(v), buf)
    except:
        return None
    s = ""
    for x in buf:
        c = x & 0xFF
        if c == 0:
            break
        s += chr(c)
    return s

# ---- vtable at 0xa86fe0: dump entries until a non-code pointer ----
vt = read_u32s(0xA86FE0, 48)
result["vtable_0xa86fe0_raw"] = ["0x%X" % x for x in vt] if vt else None
result["vtable_0xa86fe0_functions"] = []
if vt:
    for i, p in enumerate(vt):
        info = fn_info(fn_at(p))
        if info is None:
            break
        result["vtable_0xa86fe0_functions"].append({"slot": i, "ptr": "0x%X" % p, "function": info})

# dump each virtual method
if vt:
    for i, p in enumerate(vt):
        info = fn_info(fn_at(p))
        if info is None:
            break
        dump(p, "VT_%02d_%s" % (i, info["name"]))

# ---- callers of the 3 imm32-site functions + vtable xrefs ----
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
    "FUN_0073a3f0": callers_of(0x73A3F0),
    "FUN_00738150": callers_of(0x738150),
    "FUN_0073fa30": callers_of(0x73FA30),
    "FUN_0094e890": callers_of(0x94E890),
}

def refs_to(v, limit=200):
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

result["refs_to_vtable_0xa86fe0"] = refs_to(0xA86FE0)
result["refs_to_DAT_00b6c3d8"] = refs_to(0xB6C3D8)

# ---- key functions ----
targets = {
    "FUN_00958d90": 0x958D90,   # string A builder (filename number?)
    "FUN_0094e890": 0x94E890,   # caller of FUN_0094e470
    "FUN_0094deb0": 0x94DEB0,   # sibling record-parse family
    "FUN_0094c520": 0x94C520,   # sibling record-parse family
    "FUN_0094e610": 0x94E610,   # sibling record-parse family
    "FUN_009518e0": 0x9518E0,   # sibling record-parse family
    "FUN_0070bfd0": 0x70BFD0,   # another id-enumerator user
    "FUN_006ec2d0": 0x6EC2D0,   # another id-enumerator user
    "FUN_007080c0": 0x7080C0,   # called by FUN_004172a0 (param dir loader)
    "FUN_00703d70": 0x703D70,   # class-object lookup (behind FUN_00703b80)
    "FUN_00703e80": 0x703E80,   # caller of FUN_0070c680
}
result["functions"] = {}
for tag, v in targets.items():
    info = dump(v, tag)
    if info:
        result["functions"][tag] = info

# .data around 0xB6C3D8 (wider) + the game-root path guess
result["data"] = {
    "at_0xB6C3D8_64B": " ".join("%02X" % (x & 0xFF) for x in (lambda b: b)(jzeros(0, "b")) ) if False else None,
}
buf = jzeros(64, "b")
try:
    mem.getBytes(addr(0xB6C3D8), buf)
    result["data"]["at_0xB6C3D8_64B"] = " ".join("%02X" % (x & 0xFF) for x in buf)
except Exception as e:
    result["data"]["at_0xB6C3D8_64B"] = "ERR"
result["data"]["ascii_0xB6C3F0"] = read_ascii(0xB6C3F0, 64)

with open(os.path.join(OUT_DIR, "PASS3_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA PASS3 DONE")
