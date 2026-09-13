# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S12: FUN_00414670 (the A-field recipient in FUN_00511070) + .nif tester data-refs.
#
# From S10/S11: FUN_00511070: lookup(hardcoded avatar template id) -> FUN_007ce1e0 (get A)
#               -> PUSH A; CALL FUN_00414670 (with [ESI] value and another id).
# This round:
#   - disasm + pseudo of FUN_00414670 + ITS callers
#   - disasm + pseudo of FUN_004c5580 (also calls the singleton)
#   - disasm + pseudo of FUN_00737c20, FUN_008e0110, FUN_00843dd0, FUN_007291f0, FUN_0048ada0
#   - ALL references (any type) to FUN_007ee5f0 (".nif" tester) - data refs = dispatch tables
#   - ALL references (any type) to 0x00A7A774 (the ".nif" string) - already have from S5 but re-check
#
# Writes: 01_RAW\ghidra_output\S12_*

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
    "phase": "S12_a_recipient",
    "script": "s12_a_recipient.py",
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
        d = listing.getDataAt(fa) or listing.getDataContaining(fa)
        out.append({
            "from_va": "0x%08X" % fa.getOffset(),
            "ref_type": str(r.getReferenceType()),
            "in_function": fn.getName() if fn else None,
            "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None,
            "mnemonic": inst.getMnemonicString() if inst else None,
            "bytes": bytes_hex(inst) if inst else None,
            "data_at": (str(d.getValue()) if (d is not None and d.hasStringValue()) else None),
            "data_type": str(d.getDataType()) if d is not None else None,
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
    with open(os.path.join(OUT_RAW, "S12_DISASM_%s.txt" % tag), "w") as f:
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
    with open(os.path.join(OUT_RAW, "S12_PSEUDO_%s.txt" % tag), "w") as f:
        f.write(code)
    return tag


FUNCS = [
    (0x00414670, "arecip_00414670"),
    (0x004c5580, "consumer_004c5580"),
    (0x00737c20, "checker_00737c20"),
    (0x008e0110, "helper_008e0110"),
    (0x00843dd0, "helper_00843dd0"),
    (0x007291f0, "helper_007291f0"),
    (0x0048ada0, "helper_0048ada0"),
    (0x006ea810, "helper_006ea810"),
    (0x0050caf0, "helper_0050caf0"),
    (0x00414670 + 0, "arecip_dup_skip"),
]
FUNCS = FUNCS[:-1]

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

callers_arecip = refs_to(0x00414670, True)
nif_tester_refs = refs_to(0x007ee5f0, False)
nif_string_refs = refs_to(0x00A7A774, False)

# dump callers of FUN_00414670 (bounded 20)
seen = set()
for c in callers_arecip:
    if c.get("func_entry") and c["func_entry"] not in seen:
        seen.add(c["func_entry"])
        va = int(c["func_entry"], 16)
        tag = "ARECIPCALLER_%08X" % va
        info = dump_function(va, tag)
        fn2 = fm.getFunctionAt(toAddr(va)) or fm.getFunctionContaining(toAddr(va))
        if info:
            info["decompiled_to"] = decompile_to(fn2, tag)
        else:
            info = {"function": None, "entry": c["func_entry"],
                    "decompiled_to": decompile_to(fn2, tag)}
        dumped[tag] = info
        if len(dumped) > 32:
            break

with open(os.path.join(OUT_RAW, "S12_A_RECIPIENT_REFS.json"), "w") as f:
    f.write(json.dumps({
        "exec": EXEC,
        "callers_of_00414670": callers_arecip,
        "all_refs_to_007ee5f0_nif_tester": nif_tester_refs,
        "all_refs_to_nif_string_00A7A774": nif_string_refs,
    }, indent=2))

EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
EXEC["callers_of_00414670_count"] = len(callers_arecip)
EXEC["dumps"] = dumped
with open(os.path.join(OUT_RAW, "S12_DUMP_INDEX.json"), "w") as f:
    f.write(json.dumps({"exec": EXEC}, indent=2))
print("S12_DONE callers_of_00414670=%d nif_tester_refs=%d" % (len(callers_arecip), len(nif_tester_refs)))
