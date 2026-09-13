# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S9: the loader singleton (FUN_0043a550) + registry readers.
#
# From S8: FUN_00452490: EAX = FUN_0043a550(); ECX = EAX; JMP FUN_0072fa30.
# FUN_0043a550 = the loader-object getter/constructor (singleton?).
# This round:
#   - disasm + pseudo of FUN_0043a550
#   - all callers of FUN_0043a550 (who else gets the loader object -> registry readers!)
#   - dump each caller (bounded 24) disasm + pseudo
#   - also all references to DAT_00ba57ec (the read-size scratch global from 0072fa30)
#
# Writes: 01_RAW\ghidra_output\S9_*

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
    "phase": "S9_singleton_readers",
    "script": "s9_singleton_readers.py",
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
    with open(os.path.join(OUT_RAW, "S9_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S9_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


callers = refs_to(0x0043a550, True)
with open(os.path.join(OUT_RAW, "S9_SINGLETON_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "callers_of_0043a550": callers}, indent=2))

dumped = {}
info = dump_function(0x0043a550, "SINGLETON_0043a550")
fn = fm.getFunctionAt(toAddr(0x0043a550)) or fm.getFunctionContaining(toAddr(0x0043a550))
if info:
    info["decompiled_to"] = decompile_to(fn, "SINGLETON_0043a550")
dumped["SINGLETON_0043a550"] = info

seen = set()
for c in callers:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "CALLER_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 26:
            break

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["caller_count"] = len(callers)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S9_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S9_SINGLETON_READERS_DONE callers=%d" % len(callers))
for c in callers[:30]:
    print("  %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
