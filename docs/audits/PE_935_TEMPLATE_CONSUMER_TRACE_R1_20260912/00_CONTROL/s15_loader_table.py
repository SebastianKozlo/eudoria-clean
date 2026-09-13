# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S15: the loader-class pointer table @0x00A9026C + the RM pair-queue processors.
#
# From S12: the .nif extension tester FUN_007ee5f0 is referenced ONLY from 0x00A9026C
# (pointer[4] DATA) - a dispatch/vtable containing extension testers/loaders.
# From S14: pair-insert ({type,value}) callers in the 0082xxxx RM family:
# FUN_008237d0, FUN_00826360, FUN_008284d0 - the pending-queue processors.
#
# This round:
#   - dump 64 pointers around 0x00A9026C; resolve each to function/data name
#   - decompile FUN_008237d0, FUN_00826360, FUN_008284d0
#   - find all references to the table region start
#
# Writes: 01_RAW\ghidra_output\S15_*

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
mem = currentProgram.getMemory()

EXEC = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "phase": "S15_loader_table",
    "script": "s15_loader_table.py",
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
    with open(os.path.join(OUT_RAW, "S15_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S15_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


import struct

TABLE_CENTER = 0x00A9026C
SPAN = 0x100  # dump 4 bytes * 64 entries around
table_dump = []
base = TABLE_CENTER - 0x80
try:
    for i in range(64):
        va = base + i * 4
        b = bytearray(4)
        mem.getBytes(toAddr(va), b)
        val = (b[3] << 24) & 0xFF000000 | (b[2] << 16) & 0xFF0000 | (b[1] << 8) & 0xFF00 | (b[0] & 0xFF)
        fn = fm.getFunctionAt(toAddr(val))
        d = listing.getDataAt(toAddr(val))
        table_dump.append({
            "slot_va": "0x%08X" % va,
            "value": "0x%08X" % val,
            "function": fn.getName() if fn else None,
            "data_type": str(d.getDataType()) if d is not None else None,
            "data_repr": (str(d.getValue()) if (d is not None and d.hasStringValue()) else None),
        })
except Exception as e:
    table_dump.append({"error": str(e)})

FUNCS = [
    (0x008237d0, "queue_008237d0"),
    (0x00826360, "queue_00826360"),
    (0x008284d0, "queue_008284d0"),
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

with open(os.path.join(OUT_RAW, "S15_LOADER_TABLE.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC, "table_dump": table_dump, "dumps": dumped}, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S15_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S15_DONE")
for t in table_dump:
    print("  %s -> %s %s %s" % (t.get("slot_va"), t.get("value"), t.get("function"), t.get("data_repr") or ""))
