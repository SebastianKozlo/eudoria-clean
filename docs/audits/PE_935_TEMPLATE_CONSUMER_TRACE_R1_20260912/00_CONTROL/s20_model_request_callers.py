# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S20 (final): callers of FUN_006c9700 (the {0x66,id} model-request pump).
#
# Writes: 01_RAW\ghidra_output\S20_*

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
    "phase": "S20_model_request_callers",
    "script": "s20_model_request_callers.py",
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
    with open(os.path.join(OUT_RAW, "S20_DISASM_%s.txt" % tag), "w") as f:
        f.write("\n".join(lines))
    return {"function": fn.getName(), "entry": "0x%08X" % fn.getEntryPoint().getOffset(),
            "instruction_count": len(lines)}


ifc = DecompInterface()
ifc.openProgram(currentProgram)


def decompile_to(fn, tag):
    if fn is None:
        return None
    res = ifc.decompileFunction(fn, 240, monitor)
    if res.decompileCompleted():
        code = res.getDecompiledFunction().getC()
    else:
        code = "DECOMPILE_FAILED: " + str(res.getErrorMessage())
    with open(os.path.join(OUT_RAW, "S20_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


callers = refs_to(0x006c9700, True)
dumped = {}
seen = set()
for c in callers:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "MRQ_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 16:
            break

# also the full disasm of FUN_006c9700 itself (0x66 evidence)
info = dump_function(0x006c9700, "PUMP_006c9700")
dumped["PUMP_006c9700"] = info

with open(os.path.join(OUT_RAW, "S20_MODEL_REQUEST_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "callers_of_006c9700": callers}, indent=2))
EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["caller_count"] = len(callers)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S20_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S20_DONE callers_of_006c9700=%d" % len(callers))
for c in callers[:20]:
    print("  %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
