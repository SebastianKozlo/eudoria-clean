# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S5: xref enrichment for the S4b string hits + fresh decompiles of lead functions.
#
# For every requested VA (string starts / key addresses):
#   - all references TO that VA: from-instruction VA, ref type, containing function,
#     mnemonic, instruction bytes
# For every unique referencing function + the CONT-R1 lead functions
# (FUN_00971ad0 record-read, FUN_00972ad0 index build, FUN_0094bd30 parser,
#  FUN_00959090 field walk - leads to RE-ESTABLISH in this run, not citable canon):
#   - full disassembly listing + decompiled pseudocode (this run's own artifacts).
#
# Writes: 01_RAW\ghidra_output\S5_XREF_ENRICHMENT.json
#         01_RAW\ghidra_output\S5_DISASM_FUN_<va>.txt / S5_PSEUDO_FUN_<va>.txt
# READ-ONLY on the program.

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
rm = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
mem = currentProgram.getMemory()

EXEC = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "phase": "S5_xref_enrichment",
    "script": "s5_xref_enrichment.py",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

# ---- targets: S4b key string VAs (string starts, verified from S4B_RAW_HITS.json) ----
TARGETS = {
    "magic_ArkVFS02_1": 0x00A9C4D8,
    "magic_ArkVFS02_2": 0x00A9C4E4,
    "magic_ArkVFS01": 0x00A9C4F0,
    "path_templates_vfs": 0x00A86D30,
    "path_hierarchy_vfs": 0x00A87C58,
    "path_Materials_vfs": 0x00A85F34,
    "path_sids_vfs_lower": 0x00A915FB,
    "ext_vfs": 0x00A86820,
    "ext_nif": 0x00A7A774,
    "ext_bvi": 0x00A7A734,
    "ext_tdf": 0x00A7A73C,
    "ext_amu": 0x00A7A744,
    "TerrainImageCache1": 0x00A7A824,
    "TerrainImageCache2": 0x00A7A80C,
    "dir_models": 0x00A7A8CC,
    "dir_Cache": 0x00A7A83C,
}

LEAD_FUNCS = [0x00971ad0, 0x00972ad0, 0x0094bd30, 0x00959090]


def jdump(name, obj):
    p = os.path.join(OUT_RAW, name)
    f = open(p, "w")
    f.write(json.dumps(obj, indent=2))
    f.close()
    return p


def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None


census = {}
referencing_funcs = {}
for name, va in TARGETS.items():
    addr = toAddr(va)
    d = listing.getDataAt(addr)
    dval = None
    if d is not None and d.hasStringValue():
        dval = str(d.getValue())
    refs = rm.getReferencesTo(addr)
    lst = []
    for r in refs:
        fa = r.getFromAddress()
        fn = fm.getFunctionContaining(fa)
        inst = listing.getInstructionAt(fa)
        if inst is None:
            inst = listing.getInstructionContaining(fa)
        rec = {
            "from_va": "0x%08X" % fa.getOffset(),
            "ref_type": str(r.getReferenceType()),
            "in_function": fn.getName() if fn is not None else None,
            "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn is not None else None,
            "mnemonic": inst.getMnemonicString() if inst is not None else None,
            "bytes": bytes_hex(inst) if inst is not None else None,
        }
        lst.append(rec)
        if fn is not None:
            referencing_funcs["0x%08X" % fn.getEntryPoint().getOffset()] = fn.getName()
    census[name] = {"target_va": "0x%08X" % va, "ghidra_string": dval,
                    "reference_count": len(lst), "references": lst}

jdump("S5_XREF_ENRICHMENT.json", {"census": census, "exec": EXEC})

# ---- disassembly + pseudocode dumps ----
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
    with open(os.path.join(OUT_RAW, "S5_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S5_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


dump_info = {}
for va_int in LEAD_FUNCS:
    tag = "LEAD_%08X" % va_int
    dump_info[tag] = dump_function(va_int, tag)
    fn = fm.getFunctionAt(toAddr(va_int)) or fm.getFunctionContaining(toAddr(va_int))
    dump_info[tag]["decompiled_to"] = decompile_to(fn, tag)

# decompile the string-referencing functions (top 20 to bound the run)
ref_list = sorted(referencing_funcs.keys())
dump_info["referencing_function_entries"] = ref_list
for i, entry_hex in enumerate(ref_list[:20]):
    va_int = int(entry_hex, 16)
    tag = "REF_%08X" % va_int
    fn = fm.getFunctionAt(toAddr(va_int)) or fm.getFunctionContaining(toAddr(va_int))
    dump_info[tag] = {"function": fn.getName() if fn else None,
                      "entry": entry_hex,
                      "decompiled_to": decompile_to(fn, tag)}

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["dumps"] = dump_info
jdump("S5_DUMP_INDEX.json", {"exec": EXEC})
print("S5_XREF_ENRICHMENT_DONE")
for name, c in census.items():
    print("  %-22s refs=%d" % (name, c["reference_count"]))
print("  referencing_funcs=%d" % len(referencing_funcs))
