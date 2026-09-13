# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S6: the template record parser + registration chain.
#
# From S5: FUN_0072fa30 (templates.vfs loader) loop calls:
#   FUN_00971ad0 (record read) -> FUN_00730700 -> FUN_00730c90 (PARSE) ->
#   FUN_004123d0 -> FUN_005670a0 -> FUN_0072f8d0 (REGISTER)
# This round decompiles + disassembles that callee chain (the A/B/C/D/E/F consumers)
# plus the VFS read/stride/CRC helpers needed for the VA-locked chain.
#
# Writes: 01_RAW\ghidra_output\S6_DISASM_<tag>.txt / S6_PSEUDO_<tag>.txt / S6_DUMP_INDEX.json

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
    "phase": "S6_parser_chain",
    "script": "s6_parser_chain.py",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

FUNCS = [
    (0x00730c90, "parse_00730c90"),
    (0x0072f8d0, "register_0072f8d0"),
    (0x00730700, "helper_00730700"),
    (0x00730730, "helper_00730730"),
    (0x004123d0, "helper_004123d0"),
    (0x005670a0, "postparse_005670a0"),
    (0x0040e160, "helper_0040e160"),
    (0x0040e180, "helper_0040e180"),
    (0x00979d00, "stride_00979d00"),
    (0x00972280, "idxnode_00972280"),
    (0x009721d0, "idxnode_009721d0"),
    (0x00971780, "reclookup_00971780"),
    (0x00746550, "helper_00746550"),
    (0x006b22d0, "crc_006b22d0"),
    (0x004063d0, "helper_004063d0"),
    (0x00979d20, "recoffset_00979d20"),
    (0x00979cc0, "helper_00979cc0"),
    (0x00979ce0, "helper_00979ce0"),
    (0x00979d30, "helper_00979d30"),
    (0x00408b60, "strcmp_00408b60"),
    (0x009728d0, "helper_009728d0"),
    (0x009729d0, "helper_009729d0"),
    (0x00417eb0, "helper_00417eb0"),
    (0x0040de60, "helper_0040de60"),
    (0x0040de00, "helper_0040de00"),
    (0x00412430, "helper_00412430"),
    (0x00413440, "helper_00413440"),
    (0x00413450, "helper_00413450"),
    (0x004023c0, "helper_004023c0"),
    (0x00404c30, "helper_00404c30"),
    (0x00401e70, "pathjoin_00401e70"),
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
    with open(os.path.join(OUT_RAW, "S6_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S6_PSEUDO_%s.txt" % tag), "w") as f:
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
with open(os.path.join(OUT_RAW, "S6_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S6_PARSER_CHAIN_DONE")
for tag, info in dump_info.items():
    print("  %-22s entry=%-10s instr=%s" % (tag, info.get("entry"), info.get("instruction_count")))
