# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S8: callers of the template loader + node layout + registry lookup discovery.
#
# From S7: FUN_0072fa30 loads templates.vfs into a loader-owned RB-tree map
# (insert via FUN_0072f8d0 with this=loader object; key = id2 = obj+0x00).
# This round:
#   - all CALL references TO 0x0072fa30 (who invokes the loader; where the loader obj lives)
#   - all CALL references TO 0x00766a00 (hierarchy loader, comparison)
#   - dump FUN_0072f7f0 (tree node allocator: node layout key/value)
#   - references TO FUN_0072f8d0-family lookup helpers: STLport _Rb_tree find/lower_bound
#     is inlined mostly; instead: callers of the loader get decompiled.
#   - dump every caller of 0072fa30 + hierarchy caller (disasm + pseudo)
#
# Writes: 01_RAW\ghidra_output\S8_*.{json,txt}

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "phase": "S8_loader_callers",
    "script": "s8_loader_callers.py",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}


def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None


def refs_to(va_int, calls_only):
    addr = toAddr(va_int)
    out = []
    for r in rm.getReferencesTo(addr):
        if calls_only and not r.getReferenceType().isCall():
            continue
        fa = r.getFromAddress()
        fn = fm.getFunctionContaining(fa)
        inst = listing.getInstructionAt(fa) or listing.getInstructionContaining(fa)
        out.append({
            "from_va": "0x%08X" % fa.getOffset(),
            "ref_type": str(r.getReferenceType()),
            "in_function": fn.getName() if fn else None,
            "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None,
            "mnemonic": inst.getMnemonicString() if inst else None,
            "bytes": bytes_hex(inst) if inst else None,
        })
    return out


def dump_function(va_int, tag):
    fn = fm.getFunctionAt(toAddr(va_int)) or fm.getFunctionContaining(toAddr(va_int))
    if fn is None:
        return None
    lines = []
    end = fn.getBody().getMaxAddress()
    it = listing.getInstructions(fn.getEntryPoint(), True)
    for inst in it:
        ia = inst.getAddress()
        if ia.getOffset() > end.getOffset():
            break
        lines.append("%08X  %-32s  %s" % (ia.getOffset(), bytes_hex(inst) or "", inst.toString()))
    with open(os.path.join(OUT_RAW, "S8_DISASM_%s.txt" % tag), "w") as f:
        f.write("\n".join(lines))
    return {"function": fn.getName(), "entry": "0x%08X" % fn.getEntryPoint().getOffset(),
            "instruction_count": len(lines)}


ifc = DecompInterface()
ifc.openProgram(currentProgram)


def decompile_to(fn, tag):
    if fn is None:
        return None
    res = ifc.decompileFunction(fn, 180, monitor)
    if res.decompileCompleted():
        code = res.getDecompiledFunction().getC()
    else:
        code = "DECOMPILE_FAILED: " + str(res.getErrorMessage())
    with open(os.path.join(OUT_RAW, "S8_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


callers_72fa30 = refs_to(0x0072fa30, True)
callers_766a00 = refs_to(0x00766a00, True)
callers_72f8d0 = refs_to(0x0072f8d0, False)  # any refs to the insert (sibling users?)

result = {
    "callers_of_0072fa30": callers_72fa30,
    "callers_of_00766a00": callers_766a00,
    "refs_to_0072f8d0": callers_72f8d0,
}
with open(os.path.join(OUT_RAW, "S8_LOADER_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "result": result}, indent=2))

# dump the callers (bounded)
dumped = {}
seen = set()
for c in callers_72fa30 + callers_766a00:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "CALLER_%08X" % va
        info = dump_function(va, tag)
        fn = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn, tag)}
        dumped[tag] = info

# node allocator
info = dump_function(0x0072f7f0, "NODEALLOC_0072f7f0")
fn = fm.getFunctionAt(toAddr(0x0072f7f0)) or fm.getFunctionContaining(toAddr(0x0072f7f0))
info["decompiled_to"] = decompile_to(fn, "NODEALLOC_0072f7f0")
dumped["NODEALLOC_0072f7f0"] = info

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S8_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S8_LOADER_CALLERS_DONE")
print("  callers_of_0072fa30=%d callers_of_00766a00=%d refs_to_0072f8d0=%d" % (
    len(callers_72fa30), len(callers_766a00), len(callers_72f8d0)))
