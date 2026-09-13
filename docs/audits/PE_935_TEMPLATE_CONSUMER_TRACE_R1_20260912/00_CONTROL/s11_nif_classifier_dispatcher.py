# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S11: the .nif extension testers + A-classifier + resource dispatcher chain.
#
# From S10: registry consumers found but the direct A->model-open link still open.
# Leads: FUN_007ee5f0 = stricmp(x, ".nif") extension tester (callers = .nif users);
#        FUN_006b28e0 reads [input+0x8] and calls FUN_006c1d40(value) - classifier on an +0x08 field;
#        FUN_00823c10 = resource-resolution dispatcher (CONT R1 lead, re-establish in THIS binary);
#        FUN_006ba110 = its layer-applier context (CONT R1 lead);
#        FUN_006baa20 = calls both singleton and lookup (full body needed);
#        FUN_0072fce0/007ce1e0/00730f60 = template-object helpers.
#
# Writes: 01_RAW\ghidra_output\S11_*

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
    "phase": "S11_nif_classifier_dispatcher",
    "script": "s11_nif_classifier_dispatcher.py",
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
    with open(os.path.join(OUT_RAW, "S11_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S11_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


callers_nif = refs_to(0x007ee5f0, True)

FUNCS = [
    (0x0072fce0, "valid_0072fce0"),
    (0x007ce1e0, "getter_007ce1e0"),
    (0x00730f60, "postcopy_00730f60"),
    (0x006c1d40, "classifier_006c1d40"),
    (0x00823c10, "dispatcher_00823c10"),
    (0x006ba110, "layerapply_006ba110"),
    (0x006baa20, "consumer_006baa20"),
    (0x00415670, "singleton2_00415670"),
    (0x004d1430, "rbfind_004d1430"),
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

# callers of the .nif tester
seen = set()
for c in callers_nif:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "NIFCALLER_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 22:
            break

with open(os.path.join(OUT_RAW, "S11_NIF_TESTER_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "callers_of_007ee5f0": callers_nif}, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["nif_caller_count"] = len(callers_nif)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S11_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S11_DONE nif_callers=%d" % len(callers_nif))
for c in callers_nif[:30]:
    print("  %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
