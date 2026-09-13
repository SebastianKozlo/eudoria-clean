# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S13: the event emitter + builder around FUN_0043eae0 (the A-consumer factory).
#
# From S12: FUN_0043eae0 = factory: lookup(id) -> validity -> get A (FUN_007ce1e0) ->
#            emit {0x66, A} via FUN_0043c700; main builder FUN_0043e5b0 with constant 0x8BD720;
#            FUN_0040b070(TemplateObject, 0x8BD720).
# This round:
#   - FUN_0043c700 (event emitter), FUN_0043e5b0 (builder), FUN_0040b070
#   - data/type at 0x008BD720 (what is the hardcoded pointer?)
#   - FUN_0050d8c0 (the request mechanism from FUN_00511070)
#   - FUN_004154f0 + FUN_008553d0 (the tail path of 00511070)
#   - FUN_0043c5a0-family: also dump FUN_0043c400, FUN_0043c0d0 for emitter context
#
# Writes: 01_RAW\ghidra_output\S13_*

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

EXEC = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "phase": "S13_emitter_builder",
    "script": "s13_emitter_builder.py",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}


def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None


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
    with open(os.path.join(OUT_RAW, "S13_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S13_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


FUNCS = [
    (0x0043c700, "emitter_0043c700"),
    (0x0043e5b0, "builder_0043e5b0"),
    (0x0040b070, "helper_0040b070"),
    (0x0050d8c0, "request_0050d8c0"),
    (0x004154f0, "singleton3_004154f0"),
    (0x008553d0, "helper_008553d0"),
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

# inspect data at 0x008BD720
addr = toAddr(0x008BD720)
d = listing.getDataAt(addr) or listing.getDataContaining(addr)
bytes_at = None
try:
    mem = currentProgram.getMemory()
    b = bytearray(16)
    mem.getBytes(addr, b)
    bytes_at = " ".join("%02x" % (x & 0xFF) for x in b)
except:
    bytes_at = None
d8bd720 = {
    "address": "0x008BD720",
    "data_type": str(d.getDataType()) if d is not None else None,
    "value_repr": (str(d.getValue()) if (d is not None and d.hasStringValue()) else None),
    "bytes_16": bytes_at,
    "in_function": (lambda fn: fn.getName() if fn else None)(fm.getFunctionContaining(addr)),
    "references_to": [],
}
from ghidra.program.model.address import AddressSet  # noqa
for r in currentProgram.getReferenceManager().getReferencesTo(addr):
    fa = r.getFromAddress()
    fn2 = fm.getFunctionContaining(fa)
    d8bd720["references_to"].append({
        "from_va": "0x%08X" % fa.getOffset(),
        "ref_type": str(r.getReferenceType()),
        "in_function": fn2.getName() if fn2 else None,
        "func_entry": ("0x%08X" % fn2.getEntryPoint().getOffset()) if fn2 else None,
    })

with open(os.path.join(OUT_RAW, "S13_DATA_8BD720.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "data": d8bd720}, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S13_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S13_DONE")
print(json.dumps(d8bd720, indent=1)[:1200])
