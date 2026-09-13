# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S18: the BNT2 store reader + load-by-name + ArkModelManagerMain ctor.
#
# From file scan: "BNT2\0" @0x00A9BF2C (single .rdata hit) - the BNT2 archive magic string.
# From S17: FUN_00799bf0 builds "%s%d" names and loads via FUN_00799930 (store this=[this+0x18]).
# From S16: FUN_006c0d50 creates ArkModelManagerMain (0x130 B); its ctor part = FUN_006c8f80.
# This round:
#   - ALL refs to "BNT2" @0x00A9BF2C -> the BNT2 reader functions -> decompile
#   - FUN_00799930 (load-by-name), FUN_00797520, FUN_0077c180
#   - callers of FUN_00799bf0
#   - FUN_006c8f80 (ArkModelManagerMain ctor - store refs)
#
# Writes: 01_RAW\ghidra_output\S18_*

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
    "phase": "S18_bnt2_store",
    "script": "s18_bnt2_store.py",
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
    with open(os.path.join(OUT_RAW, "S18_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S18_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


refs_bnt2 = refs_to(0x00A9BF2C, False)
FUNCS = [
    (0x00799930, "loadbyname_00799930"),
    (0x00797520, "sink2_00797520"),
    (0x0077c180, "sink3_0077c180"),
    (0x006c8f80, "amm_ctor_006c8f80"),
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

# BNT2-magic referencing functions -> dump
seen = set()
for c in refs_bnt2:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "BNT2_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 12:
            break

# callers of FUN_00799bf0 (the "%s%d"+load builder)
callers_bf0 = refs_to(0x00799bf0, True)
seen2 = set()
for c in callers_bf0:
    if c.get("func_entry") and c["func_entry"] not in seen2:
        seen2.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "BF0CALLER_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 20:
            break

with open(os.path.join(OUT_RAW, "S18_REFS.json"), "w") as f:
    f.write(json.dumps({
        "exec": EXEC,
        "refs_to_BNT2_magic_00A9BF2C": refs_bnt2,
        "callers_of_00799bf0": callers_bf0,
    }, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["bnt2_ref_count"] = len(refs_bnt2)
EXEC["bf0_caller_count"] = len(callers_bf0)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S18_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S18_DONE bnt2_refs=%d bf0_callers=%d" % (len(refs_bnt2), len(callers_bf0)))
for c in refs_bnt2[:12]:
    print("  BNT2 %s [%s] in %s @%s" % (c["from_va"], c["ref_type"], c["in_function"], c["func_entry"]))
for c in callers_bf0[:12]:
    print("  BF0 %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
