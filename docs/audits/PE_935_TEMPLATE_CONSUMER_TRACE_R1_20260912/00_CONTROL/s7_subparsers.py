# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S7: sub-parsers of the template record + node/registry details.
#
# From S6: FUN_00730c90 parses template payload -> object {id2@+0,A@+8,B@+4,C@+0xC,D_f32@+0x10,
# sub1@+0x14 via FUN_00730b70, sub2@+0x20 via FUN_00730970, u32@+0x2C}; registry = RB-tree insert
# (FUN_0072f8d0) with node allocator FUN_0072f7f0; copy ctors FUN_00566f80 (sub1), FUN_00525da0 (sub2).
# This round: those sub-parsers/ctors + the file-read helper FUN_0040e260 + CRC table init FUN_00406110
# + full disasm of FUN_0072fa30 (this-arg chain) and index node builders.
#
# Writes: 01_RAW\ghidra_output\S7_DISASM_<tag>.txt / S7_PSEUDO_<tag>.txt / S7_DUMP_INDEX.json

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
    "phase": "S7_subparsers",
    "script": "s7_subparsers.py",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

FUNCS = [
    (0x00730b70, "subparser1_00730b70"),
    (0x00730970, "subparser2_00730970"),
    (0x00566f80, "copyctor1_00566f80"),
    (0x00525da0, "copyctor2_00525da0"),
    (0x0072f7f0, "nodealloc_0072f7f0"),
    (0x0072fa30, "loader_0072fa30"),
    (0x0040e260, "fileread_0040e260"),
    (0x00406110, "crctable_00406110"),
    (0x00972280, "idxnode_00972280"),
    (0x009721d0, "idxnode_009721d0"),
    (0x00972ad0, "indexwalk_00972ad0"),
    (0x00971780, "reclookup_00971780"),
]


def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None


def dump_function(va_int, tag):
    fn = fm.getFunctionAt(toAddr(va_int))
    if fn is None:
        fn = fm.getFunctionContaining(toAddr(va_int))
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
    with open(os.path.join(OUT_RAW, "S7_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S7_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


dump_info = {}
for va_int, tag in FUNCS:
    info = dump_function(va_int, tag)
    fn = fm.getFunctionAt(toAddr(va_int)) or fm.getFunctionContaining(toAddr(va_int))
    if info:
        info["decompiled_to"] = decompile_to(fn, tag)
    else:
        info = {"function": None, "entry": "0x%08X" % va_int,
                "decompiled_to": decompile_to(fn, tag)}
    dump_info[tag] = info

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["dumps"] = dump_info
with open(os.path.join(OUT_RAW, "S7_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S7_SUBPARSERS_DONE")
for tag, info in dump_info.items():
    print("  %-24s entry=%-10s instr=%s" % (tag, info.get("entry"), info.get("instruction_count")))
