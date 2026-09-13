# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S14: the resource-manager registration FUN_0041dae0 (full) + pair-insert callers.
#
# From S13: {0x66, A} pairs are inserted into a requester-owned pair-keyed map (FUN_0043c700).
# The RM init FUN_0041dae0 references ".nif" x2, ".bvi" x2, ".amu", ".tdf", "Cache\", "models\" x2,
# TerrainImageCache1/2 - the loader registration. Full body needed (S5 decompile was stub).
#
# Writes: 01_RAW\ghidra_output\S14_*

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
    "phase": "S14_rm_registration",
    "script": "s14_rm_registration.py",
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
    with open(os.path.join(OUT_RAW, "S14_DISASM_%s.txt" % tag), "w") as f:
        f.write("\n".join(lines))
    return {"function": fn.getName(), "entry": "0x%08X" % fn.getEntryPoint().getOffset(),
            "instruction_count": len(lines)}


ifc = DecompInterface()
ifc.openProgram(currentProgram)


def decompile_to(fn, tag, timeout=300):
    if fn is None:
        return None
    res = ifc.decompileFunction(fn, timeout, monitor)
    if res.decompileCompleted():
        code = res.getDecompiledFunction().getC()
    else:
        code = "DECOMPILE_FAILED: " + str(res.getErrorMessage())
    with open(os.path.join(OUT_RAW, "S14_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


FUNCS = [
    (0x0041dae0, "rm_init_0041dae0"),
    (0x008bd720, "callback_008bd720"),
    (0x0043cb60, "helper_0043cb60"),
    (0x004b0980, "cache_user_004b0980"),
]

dumped = {}
for va_int, tag in FUNCS:
    info = dump_function(va_int, tag)
    fn = fm.getFunctionAt(toAddr(va_int)) or fm.getFunctionContaining(toAddr(va_int))
    if info:
        info["decompiled_to"] = decompile_to(fn, tag)
    else:
        info = {"function": None, "entry": "0x%08X" % va_int,
                "decompiled_to": decompile_to(fn, tag)}
    dumped[tag] = info

callers_pairinsert = refs_to(0x0043c700, True)
with open(os.path.join(OUT_RAW, "S14_PAIR_INSERT_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "callers_of_0043c700": callers_pairinsert}, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["pair_insert_caller_count"] = len(callers_pairinsert)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S14_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S14_DONE pair_insert_callers=%d" % len(callers_pairinsert))
for c in callers_pairinsert[:40]:
    print("  %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
