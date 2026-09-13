# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S17 (final Ghidra round): the "%s%d" name-formatter refs + .nif store instance refs.
#
# Candidates for the resolver last link:
#   "%s%d" @0x00A8AAEC - the id->name formatter
#   0x00AB0EA8 - the .nif store instance (from the loader-class record)
#   FUN_008251a0 (2nd queue caller), FUN_008286e0 (archive register from RM init)
# Writes: 01_RAW\ghidra_output\S17_*

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
    "phase": "S17_resolver_last_link",
    "script": "s17_resolver_last_link.py",
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
    with open(os.path.join(OUT_RAW, "S17_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S17_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


refs_ssd = refs_to(0x00A8AAEC, False)
refs_nifstore = refs_to(0x00AB0EA8, False)

FUNCS = [
    (0x008251a0, "queue2_008251a0"),
    (0x008286e0, "archreg_008286e0"),
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

# dump the referrers of "%s%d" (bounded 12)
seen = set()
for c in refs_ssd:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "SSDREF_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 15:
            break

# dump the referrers of the .nif store instance (bounded 8)
seen2 = set()
for c in refs_nifstore:
    if c.get("func_entry") and c["func_entry"] not in seen2:
        seen2.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "NIFSTORE_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 24:
            break

with open(os.path.join(OUT_RAW, "S17_REFS.json"), "w") as f:
    f.write(json.dumps({
        "exec": EXEC,
        "refs_to_pctspctd_00A8AAEC": refs_ssd,
        "refs_to_nifstore_00AB0EA8": refs_nifstore,
    }, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["ssd_ref_count"] = len(refs_ssd)
EXEC["nifstore_ref_count"] = len(refs_nifstore)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S17_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S17_DONE ssd_refs=%d nifstore_refs=%d" % (len(refs_ssd), len(refs_nifstore)))
for c in refs_ssd[:15]:
    print("  SSD %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
for c in refs_nifstore[:15]:
    print("  NIFSTORE %s [%s] in %s @%s" % (c["from_va"], c["ref_type"], c["in_function"], c["func_entry"]))
