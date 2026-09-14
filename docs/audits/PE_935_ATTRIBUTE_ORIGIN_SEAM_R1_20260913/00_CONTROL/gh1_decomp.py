# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - Ghidra postScript (Jython) GH1.
# 1) Decompile full bodies of target functions to 01_RAW/DECOMP/*.c
# 2) isCall census for seam targets (authoritative Ghidra attribution)
# 3) program identity: bytes at anchor VAs (compare vs pe_core post-run)

import json
import os
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from jarray import zeros as jzeros

OUT_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913\01_RAW"
DEC_DIR = os.path.join(OUT_DIR, "DECOMP")

DECOMP = [
    0x008550C0, 0x00854C00, 0x008544D0, 0x00854520, 0x00971780,
    0x00856090, 0x00854D90, 0x00414130, 0x00856190, 0x004154F0,
    0x00853A80, 0x00853A50,
    0x0085B1B0, 0x00528E50, 0x0085B7F0, 0x0085B3A0, 0x0085B190,
    0x00413440, 0x004134F0, 0x007345C0, 0x0085B840, 0x0085B860,
    0x0085B880, 0x008E0110, 0x0085B0F0, 0x0085B010, 0x0085B330,
    0x0085B6A0, 0x0085B5E0, 0x0085B640, 0x0085B750, 0x0085B3E0,
    0x0085ADB0, 0x006B22D0,
    0x004C46C0, 0x004C47F0, 0x004C4640, 0x00797280, 0x00765930,
    0x008553D0, 0x00845F70, 0x005275E0, 0x00856100,
    0x00457930,
    0x00567770, 0x00567C50, 0x00567170, 0x005B5F90, 0x006CB6F0,
    0x00468910, 0x0058DB50, 0x005B72C0, 0x00514EF0, 0x00846840,
    0x00730C90, 0x0094BD30, 0x0094F350, 0x00972DF0, 0x00752700,
    0x00752740, 0x009719D0,
    0x00730F60, 0x00730F90, 0x00730FB0, 0x00730FD0,
    0x00745360, 0x007453D0,
]

CENSUS_TARGETS = {
    "resolver_FUN_008544D0": 0x008544D0,
    "mgr_getter_FUN_004154F0": 0x004154F0,
    "selector_FUN_008553D0": 0x008553D0,
    "value_ctor_FUN_0085B1B0": 0x0085B1B0,
    "derived_ctor_FUN_00528E50": 0x00528E50,
    "create_FUN_004C46C0": 0x004C46C0,
    "placement_FUN_004C47F0": 0x004C47F0,
    "insert_FUN_00856190": 0x00856190,
    "mapop_FUN_00856090": 0x00856090,
    "mapop_FUN_00854D90": 0x00854D90,
    "mapop_FUN_00854C00": 0x00854C00,
    "find_FUN_00971780": 0x00971780,
    "keyproducer_FUN_00457930": 0x00457930,
    "attr_writer_FUN_00845F70": 0x00845F70,
    "walker_FUN_0085B840": 0x0085B840,
    "walker_FUN_0085B860": 0x0085B860,
    "parser_A_FUN_00730C90": 0x00730C90,
    "parser_B_FUN_0094BD30": 0x0094BD30,
    "parser_C_FUN_0094F350": 0x0094F350,
    "vfs_reader_FUN_00972DF0": 0x00972DF0,
    "readcursor_FUN_00752700": 0x00752700,
    "readcursor_FUN_00752740": 0x00752740,
    "setter_FUN_00730F60": 0x00730F60,
    "setter_FUN_00730F90": 0x00730F90,
    "setter_FUN_00730FB0": 0x00730FB0,
    "setter_FUN_00730FD0": 0x00730FD0,
}

ANCHORS = [0x007CE1E0, 0x0085B1C3, 0x00A91E4C, 0x0095D3C4, 0x008550C0,
           0x004154F0, 0x008544D0, 0x00971780, 0x004C46C0, 0x00856090]


def main():
    prog = currentProgram
    fm = prog.getFunctionManager()
    af = prog.getAddressFactory()
    space = af.getDefaultAddressSpace()

    def addr(va):
        return space.getAddress(va)

    if not os.path.isdir(DEC_DIR):
        os.makedirs(DEC_DIR)

    res = {"stage": "GH1_decomp_census", "measured": {}, "errors": []}

    anchor_data = {}
    for va in ANCHORS:
        buf = jzeros(16, "b")
        prog.getMemory().getBytes(addr(va), buf)
        anchor_data["0x%08X" % va] = "".join("%02X" % (x & 0xFF) for x in buf)
    res["measured"]["program_name"] = prog.getName()
    res["measured"]["anchor_bytes"] = anchor_data
    try:
        res["measured"]["program_exec_path"] = prog.getExecutablePath()
    except:
        res["measured"]["program_exec_path"] = None

    ifc = DecompInterface()
    ifc.openProgram(prog)
    mon = ConsoleTaskMonitor()
    decomp_index = []
    seen = {}
    for va in DECOMP:
        f = fm.getFunctionContaining(addr(va))
        rec = {"requested": "0x%08X" % va}
        if f is None:
            rec["error"] = "no function containing VA"
            decomp_index.append(rec)
            res["errors"].append("no function at 0x%08X" % va)
            continue
        entry = f.getEntryPoint().getOffset()
        rec["entry"] = "0x%08X" % entry
        rec["name"] = f.getName()
        rec["body_size"] = f.getBody().getNumAddresses()
        if entry in seen:
            rec["decompiled"] = seen[entry]
            decomp_index.append(rec)
            continue
        r = ifc.decompileFunction(f, 120, mon)
        if r.decompileCompleted():
            c = r.getDecompiledFunction().getC()
            fn = "F%08X.c" % entry
            with open(os.path.join(DEC_DIR, fn), "w") as fh:
                fh.write(c)
            rec["decompiled"] = fn
            seen[entry] = fn
        else:
            rec["error"] = "decompile failed: %s" % r.getErrorMessage()
            res["errors"].append("decomp fail 0x%08X" % entry)
        decomp_index.append(rec)
    res["measured"]["decomp_index"] = decomp_index

    census = {}
    for name, t in sorted(CENSUS_TARGETS.items()):
        refs = getReferencesTo(addr(t))
        lst = []
        for r in refs:
            if r.getReferenceType().isCall():
                f = fm.getFunctionContaining(r.getFromAddress())
                lst.append({
                    "call_site": "0x%08X" % r.getFromAddress().getOffset(),
                    "func": (f.getName() if f is not None else None),
                    "entry": ("0x%08X" % f.getEntryPoint().getOffset()) if f is not None else None})
        census[name] = {"count": len(lst), "sites": lst}
    res["measured"]["isCall_census"] = census

    with open(os.path.join(OUT_DIR, "GH1_DECOMP_CENSUS.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("GH1 done: decompiled=%d census_targets=%d" % (len(seen), len(census)))


main()
