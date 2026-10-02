# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Static-only analysis of the imported Entropia.exe (pinned identity verified outside by SHA256).
# Outputs into 01_RAW\GHIDRA_ROUTING\ of the run package.
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
mem = program.getMemory()

result = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "generator": "03_SCRIPTS/s3_ghidra_routing.py (Ghidra headless postScript)",
    "program_name": program.getName(),
    "program_path": str(program.getExecutablePath()),
    "image_base": "0x%X" % program.getImageBase().getOffset(),
    "language": str(program.getLanguageID()),
}

def addr(v):
    return program.getAddressFactory().getAddress("0x%X" % v)

def fn_at(v):
    f = fm.getFunctionContaining(addr(v))
    return f

def fn_info(f):
    if f is None:
        return None
    body = f.getBody()
    return {
        "name": f.getName(),
        "entry": "0x%X" % f.getEntryPoint().getOffset(),
        "body_min": "0x%X" % body.getMinAddress().getOffset(),
        "body_max": "0x%X" % body.getMaxAddress().getOffset(),
        "size": body.getMaxAddress().getOffset() - body.getMinAddress().getOffset() + 1,
    }

def disasm(f, max_ins=4000):
    out = []
    if f is None:
        return out
    it = listing.getInstructions(f.getBody(), True)
    n = 0
    for ins in it:
        out.append("%s  %s   %s" % (ins.getAddress().toString(), ins.getMnemonicString(),
                                     ins.toString().split(" ", 1)[1] if " " in ins.toString() else ""))
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

def callers_of(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        if ref.getReferenceType().isCall():
            cf = fm.getFunctionContaining(ref.getFromAddress())
            out.append({"call_site": "0x%X" % ref.getFromAddress().getOffset(),
                        "caller": cf.getName() if cf else None,
                        "caller_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

def refs_to(v):
    out = []
    for ref in rm.getReferencesTo(addr(v)):
        cf = fm.getFunctionContaining(ref.getFromAddress())
        out.append({"from": "0x%X" % ref.getFromAddress().getOffset(),
                    "type": str(ref.getReferenceType()),
                    "in_function": cf.getName() if cf else None,
                    "in_function_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None})
    return out

def dump_fn(v, tag):
    f = fn_at(v)
    info = fn_info(f)
    if info is None:
        result.setdefault("missing_functions", []).append({"requested_va": "0x%X" % v, "tag": tag})
        return None
    with open(os.path.join(OUT_DIR, "DISASM_%s.txt" % tag), "w") as fh:
        fh.write("\n".join(disasm(f)))
    c = decomp(f)
    with open(os.path.join(OUT_DIR, "DECOMP_%s.txt" % tag), "w") as fh:
        fh.write(c if c else "")
    info["decomp_file"] = "DECOMP_%s.txt" % tag
    info["disasm_file"] = "DISASM_%s.txt" % tag
    return info

result["imm32_0x4E22_sites"] = []
for v in (0x73819A, 0x73A442, 0x73FBCC):
    f = fn_at(v)
    site = {"imm_va": "0x%X" % v, "containing_function": fn_info(f)}
    ins = listing.getInstructionAt(addr(v - 4)) or listing.getInstructionAt(addr(v - 1)) or listing.getInstructionAt(addr(v - 5))
    ctx = []
    a = addr(v)
    # dump 10 instructions around the site
    it = listing.getInstructions(a.subtract(0x30), True)
    n = 0
    for i2 in it:
        ctx.append("%s  %s" % (i2.getAddress().toString(), i2.toString()))
        n += 1
        if n > 24 or i2.getAddress().getOffset() > v + 0x30:
            break
    site["context_disasm"] = ctx
    result["imm32_0x4E22_sites"].append(site)

# ---- function dumps: loader family + call targets + parser family ----
targets = {
    # lead family (contract S_B leads, LEADS_TO_REVERIFY)
    "FUN_0070e810": 0x70E810, "FUN_0070ec20": 0x70EC20, "FUN_00972df0": 0x972DF0,
    "FUN_00959090": 0x959090, "FUN_0094d9b0": 0x94D9B0, "FUN_0094bd30": 0x94BD30,
    "FUN_0094e1d0": 0x94E1D0, "FUN_0094e390": 0x94E390, "FUN_0094dfc0": 0x94DFC0,
    "FUN_0094f350": 0x94F350, "FUN_0094fe00": 0x94FE00, "FUN_00950010": 0x950010,
    "FUN_00950190": 0x950190, "FUN_004172a0": 0x4172A0, "FUN_0070c680": 0x70C680,
    "FUN_0070c3d0": 0x70C3D0,
    # cursor/read helpers
    "FUN_00412430": 0x412430, "FUN_0040de60": 0x40DE60, "FUN_00971ad0": 0x971AD0,
    "FUN_009724e0": 0x9724E0, "FUN_00401fd0": 0x401FD0, "FUN_00401e70": 0x401E70,
    "FUN_00417fa0": 0x417FA0, "FUN_00971660": 0x971660, "FUN_00972ad0": 0x972AD0,
    # imm32-site call targets (hand-decoded from raw bytes; to verify in Ghidra)
    "FUN_0070cf80": 0x70CF80, "FUN_00433b80": 0x433B80, "FUN_00703b80": 0x703B80,
}
result["functions"] = {}
for tag, v in targets.items():
    info = dump_fn(v, tag)
    if info:
        result["functions"][tag] = info

# ---- callers/xrefs census ----
result["callers"] = {}
for tag, v in [("FUN_0070cf80", 0x70CF80), ("FUN_00433b80", 0x433B80), ("FUN_00703b80", 0x703B80),
               ("FUN_0070e810", 0x70E810), ("FUN_0070ec20", 0x70EC20), ("FUN_0094e1d0", 0x94E1D0),
               ("FUN_0094bd30", 0x94BD30), ("FUN_00959090", 0x959090), ("FUN_0070c680", 0x70C680),
               ("FUN_00972df0", 0x972DF0), ("FUN_0094d9b0", 0x94D9B0), ("FUN_0094f350", 0x94F350),
               ("FUN_00950010", 0x950010)]:
    result["callers"][tag] = callers_of(v)

# ---- string/data references ----
result["refs_to_vfs_string_0xA86820"] = refs_to(0xA86820)
result["refs_to_mangle_20002_0xB8DBF5"] = refs_to(0xB8DBF5)
result["refs_to_mangle_20002_0xB8EDE4"] = refs_to(0xB8EDE4)
result["refs_to_mangle_20006_0xB8D89C"] = refs_to(0xB8D89C)
result["refs_to_DAT_00ba8df8"] = refs_to(0xBA8DF8)
result["refs_to_DAT_00ba8e1c"] = refs_to(0xBA8E1C)

# raw strings at the mangled-name addresses (for exact name recovery)
def ascii_at(v, maxlen=256):
    from jarray import zeros as jzeros
    buf = jzeros(maxlen, "b")
    try:
        mem.getBytes(addr(v), buf)
    except:
        return "<READ_FAILED>"
    s = ""
    for b in buf:
        c = (b & 0xFF)
        if c == 0:
            break
        s += chr(c)
    return s

result["strings"] = {
    "at_0xB8DBF5_context": ascii_at(0xB8DBF5 - 0x30, 256),
    "at_0xB8EDE4_context": ascii_at(0xB8EDE4 - 0x10, 256),
    "at_0xB8D89C_context": ascii_at(0xB8D89C - 0x10, 256),
    "vfs_string_0xA86820": ascii_at(0xA86820, 16),
}

with open(os.path.join(OUT_DIR, "ROUTING_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S3 GHIDRA DUMP DONE -> %s" % OUT_DIR)
