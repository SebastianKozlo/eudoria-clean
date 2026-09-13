# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S16: loader-class methods (the .nif record + neighbors) + the id->path resolver.
#
# From S15: loader-class descriptor records in .rdata around 0x00A9024C..0x00A902DC:
#   rec#1 {0x00AB0E5C, 007EE530, 007D30F0, 007EE3C0, 007EE480, 007EE360}
#   rec#2 {0x00AB0EA8, 007EE680, 007EE5F0(.nif tester), 007EE6A0, 007EE780}  <- NIF LOADER CLASS
#   rec#3 {0x00AB0EF4, 007EEBB0, 00984610, 007EEAB0, 007EEAF0}
#   rec#4 {0x00AB0F40, 007EFDE0, 007EFCB0, 007F0470, 007F0130}
# This round decompiles all loader methods + the ".vfs" id->path builder FUN_0094fe00
# (the resolver mechanism) + FUN_006c2bb0 (B/C getter candidate) + callers of FUN_008237d0
# (the queue API) + FUN_006c0d50 (0x130-object creator from the avatar path).
#
# Writes: 01_RAW\ghidra_output\S16_*

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
    "phase": "S16_loader_methods",
    "script": "s16_loader_methods.py",
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
    with open(os.path.join(OUT_RAW, "S16_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S16_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


FUNCS = [
    (0x007EE680, "nif1_007EE680"),
    (0x007EE6A0, "nif3_007EE6A0"),
    (0x007EE780, "nif4_007EE780"),
    (0x007EE530, "cls1a_007EE530"),
    (0x007D30F0, "cls1b_007D30F0"),
    (0x007EE3C0, "cls1c_007EE3C0"),
    (0x007EE480, "cls1d_007EE480"),
    (0x007EE360, "cls1e_007EE360"),
    (0x007EEBB0, "cls3a_007EEBB0"),
    (0x00984610, "cls3b_00984610"),
    (0x007EEAB0, "cls3c_007EEAB0"),
    (0x007EEAF0, "cls3d_007EEAF0"),
    (0x007EFDE0, "cls4a_007EFDE0"),
    (0x007EFCB0, "cls4b_007EFCB0"),
    (0x007F0470, "cls4c_007F0470"),
    (0x007F0130, "cls4d_007F0130"),
    (0x0094fe00, "vfspath_0094fe00"),
    (0x006c2bb0, "bcgetter_006c2bb0"),
    (0x006c0d50, "objcreate_006c0d50"),
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

callers_queue = refs_to(0x008237d0, True)
with open(os.path.join(OUT_RAW, "S16_QUEUE_API_CALLERS.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "callers_of_008237d0": callers_queue}, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["callers_of_008237d0_count"] = len(callers_queue)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S16_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S16_DONE queue_callers=%d" % len(callers_queue))
for c in callers_queue[:30]:
    print("  %s in %s @%s" % (c["from_va"], c["in_function"], c["func_entry"]))
