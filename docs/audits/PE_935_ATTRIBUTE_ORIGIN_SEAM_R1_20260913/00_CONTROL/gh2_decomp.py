# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - Ghidra postScript (Jython) GH2.
# Second batch: ID gen, node allocators (pair copy proof), placement record
# source (FUN_00745360), registry lookups, callers of creator/placement,
# model-instance family, composer dispatch targets + isCall censuses.

import json
import os
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from jarray import zeros as jzeros

OUT_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913\01_RAW"
DEC_DIR = os.path.join(OUT_DIR, "DECOMP")

DECOMP = [
    0x004123D0, 0x00797280,
    0x00851610, 0x00854260,
    0x00567B40, 0x00567030, 0x00843D60, 0x00843DD0, 0x00855DC0,
    0x0043A550, 0x0072F580, 0x0096C630,
    0x00745360, 0x007453D0, 0x005247C0, 0x0085B120,
    0x004C4640, 0x00765930,
    0x008599A0, 0x00415570, 0x0085A9F0,
    0x0050BED0, 0x00456F40, 0x00442190, 0x00441910, 0x004B3A00,
    0x004574F0, 0x004B0AB0, 0x004B1670, 0x004B1C70, 0x004C4A10,
    0x006CB370, 0x006FA8B0,
    0x0085AD50, 0x0085ACB0, 0x0085B020, 0x00792B20,
    0x00752700,
    0x005275E0,
]

CENSUS_TARGETS = {
    "builder_FUN_00567770": 0x00567770,
    "driver_FUN_00567C50": 0x00567C50,
    "keywalker_FUN_00846840": 0x00846840,
    "cand_FUN_00567170": 0x00567170,
    "cand_FUN_005B5F90": 0x005B5F90,
    "cand_FUN_006CB6F0": 0x006CB6F0,
    "resolvercaller_FUN_004C4A10": 0x004C4A10,
    "idgen_FUN_004123D0": 0x004123D0,
    "idreg_FUN_00797280": 0x00797280,
    "rb_lookup_FUN_0072F580": 0x0072F580,
    "slotgetter_FUN_0043A550": 0x0043A550,
    "plsrc_FUN_00745360": 0x00745360,
    "plchk_FUN_007453D0": 0x007453D0,
    "lookup2_FUN_005247C0": 0x005247C0,
    "cbreg_FUN_00567030": 0x00567030,
    "queuepush_FUN_00567B40": 0x00567B40,
    "reccopy_FUN_004148F0": 0x004148F0,
    "ctor_FUN_00730700": 0x00730700,
    "composer2_FUN_008599A0": 0x008599A0,
    "singleton2getter_FUN_00415570": 0x00415570,
    "walkerinit_FUN_0085B840": 0x0085B840,
}

CONTAINING = [0x00972D22, 0x005678DC, 0x00457D16, 0x00457D67, 0x009730C6]


def main():
    prog = currentProgram
    fm = prog.getFunctionManager()
    af = prog.getAddressFactory()
    space = af.getDefaultAddressSpace()

    def addr(va):
        return space.getAddress(va)

    if not os.path.isdir(DEC_DIR):
        os.makedirs(DEC_DIR)

    res = {"stage": "GH2_decomp_census", "measured": {}, "errors": []}

    anchor_data = {}
    for va in [0x004123D0, 0x00745360, 0x00854260, 0x004C4A10]:
        buf = jzeros(16, "b")
        prog.getMemory().getBytes(addr(va), buf)
        anchor_data["0x%08X" % va] = "".join("%02X" % (x & 0xFF) for x in buf)
    res["measured"]["anchor_bytes"] = anchor_data

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

    cont = {}
    for va in CONTAINING:
        f = fm.getFunctionContaining(addr(va))
        cont["0x%08X" % va] = ({"entry": "0x%08X" % f.getEntryPoint().getOffset(),
                                "name": f.getName()} if f is not None else None)
    res["measured"]["function_containing"] = cont

    with open(os.path.join(OUT_DIR, "GH2_DECOMP_CENSUS.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("GH2 done: decompiled=%d census=%d containing=%d" % (
        len(seen), len(census), len(cont)))


main()
