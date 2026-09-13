# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS3: attribute setter/getter census + queue extractors + network ctors +
#            portal readers + D-field getter callers + disasm windows.
# Writes: 01_RAW\ghidra_output\ZS3_*.txt/.json

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "phase": "ZS3_setter_network_portals_Dgetter",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    # attribute set/get core
    0x00845F70, 0x00854A20, 0x008452D0, 0x00845360, 0x0050DD60,
    # D/C getter stubs + float D getter
    0x0048ADA0, 0x00861240, 0x006B22D0,
    # queue extractors + processor
    0x007527F0, 0x00752700, 0x00752640, 0x004B18D0,
    # parameter loader upward + VFS reader + store ctor
    0x0094E1D0, 0x0094E390, 0x00972DF0, 0x00972380,
    # network ctors
    0x00830030, 0x00831530, 0x00834F30, 0x00835500, 0x00835700,
    0x004B1030, 0x004B15F0, 0x0082FA20, 0x0082FD60,
    # portal ctors (Z3 readers)
    0x00852A90, 0x00852B10, 0x00851E80, 0x00852110, 0x0084CE20, 0x0084E890,
    # CWO-deriver record creators
    0x00730E50, 0x00730B30, 0x007302E0,
    # misc from FUN_00468910
    0x0075FF20, 0x0040BFE0,
    # 0x42/0x39 requester internals
    0x005B6890,
]

CALLERS_OF = {
    "FUN_00845f70_attr_setter": 0x00845F70,
    "FUN_008452d0_attr_get_int": 0x008452D0,
    "FUN_00845360_attr_get_float": 0x00845360,
    "FUN_004387a0_set6a5": 0x004387A0,
    "FUN_008553d0_constructor_walker": 0x008553D0,
    "FUN_0048ada0_getter_D_plus0x10": 0x0048ADA0,
    "FUN_00861240_getter_f32_plus0x10": 0x00861240,
    "FUN_006b22d0_getter_C_plus0x0c": 0x006B22D0,
    "FUN_004b18d0_queue_processor": 0x004B18D0,
    "FUN_00830030_staticpacket_ctor": 0x00830030,
    "FUN_00835500_packetdecoder_ctor": 0x00835500,
    "FUN_004b1030_clientpacketexecutor_ctor": 0x004B1030,
    "FUN_00852a90_portalresourceitem_ctor": 0x00852A90,
    "FUN_00852b10_portalresourceitem_ctor2": 0x00852B10,
    "FUN_0041b870_portalfactory_slot0": 0x0041B870,
    "FUN_0050dd60": 0x0050DD60,
    "FUN_005b6890_requester": 0x005B6890,
    "FUN_004c5480_cwoderiver_entry": 0x004C5480,
    "FUN_007527f0_queue_typecheck": 0x007527F0,
    "FUN_0072a580": 0x0072A580,
}

DISASM_WINDOWS = [
    ("FUN_00468910_region_0058db50_and_6a4", 0x00469280, 0x00469580),
    ("FUN_0058db50_call_00567c50", 0x0058E060, 0x0058E0D0),
    ("FUN_00847270_switch_6a4_6a8", 0x00847270, 0x008472D0),
    ("FUN_004387a0_set_6a5", 0x004387A0, 0x00438800),
]

def decompile(func, max_secs=150):
    if func is None:
        return None
    di = DecompInterface()
    di.openProgram(currentProgram)
    try:
        res = di.decompileFunction(func, max_secs, monitor)
        if res.decompileCompleted():
            return res.getDecompiledFunction().getC()
    except:
        return None
    finally:
        di.dispose()

def callers_of(va_int, limit=80):
    res = []
    fn = fm.getFunctionContaining(toAddr(va_int)) or fm.getFunctionAt(toAddr(va_int))
    if fn is not None:
        for r in rm.getReferencesTo(fn.getEntryPoint()):
            if r.getReferenceType().isCall():
                fa = r.getFromAddress()
                fn2 = fm.getFunctionContaining(fa)
                res.append({
                    "from_va": "0x%08X" % fa.getOffset(),
                    "in_function": fn2.getName() if fn2 else None,
                    "func_entry": ("0x%08X" % fn2.getEntryPoint().getOffset()) if fn2 else None,
                })
                if len(res) >= limit:
                    break
    return res

def disasm_window(start_va, end_va):
    lines = []
    addr = toAddr(start_va)
    end = toAddr(end_va)
    while addr is not None and addr.getOffset() <= end.getOffset():
        ins = listing.getInstructionAt(addr)
        if ins is not None:
            lines.append("0x%08X  %-44s" % (addr.getOffset(), str(ins)))
        addr = addr.next()
    return lines

def main():
    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS3_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS3_A_done %d" % len(DECOMPILE))

    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS3_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS3_B_done")

    for label, s, e in DISASM_WINDOWS:
        lines = disasm_window(s, e)
        with open(os.path.join(OUT_RAW, "ZS3_DISASM_%s.txt" % label), "w") as f:
            f.write("\n".join(lines))
    print("ZS3_C_done")

    print("ZS3_DONE")

main()
