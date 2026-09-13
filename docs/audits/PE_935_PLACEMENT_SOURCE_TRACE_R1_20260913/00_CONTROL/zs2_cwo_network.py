# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS2: upward chain + network + portals + bind hunt v2 + disasm windows.
#  A) Decompile: callers of FUN_00567c50 (3), builder-family callers, attr-ID user
#     functions, param loader upward chain, create-methods of the class-id factories,
#     packet/communicator ctor-containing functions, portal ctor-containing functions.
#  B) Callers-of: the upward chain nodes, create methods, parameter loaders.
#  C) Function-containing: vtable-store sites (from S7) -> ctor functions.
#  D) Bind hunt v2: TD->COL->vtable->xrefs via getInt-aligned scan (fixed).
#  E) Disasm windows (raw VA evidence): FUN_00567770 setter call region,
#     FUN_00567c50 call site, FUN_00846840 walker region.
# Writes: 01_RAW\ghidra_output\ZS2_*.txt/.json

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
mem = currentProgram.getMemory()

EXEC = {
    "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "phase": "ZS2_upward_network_portals",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

DECOMPILE = [
    # upward chain of the placement-record builder
    0x0058DB50, 0x005B72C0, 0x00514EF0,          # callers of FUN_00567c50
    0x005B6370,                                    # caller of builder FUN_005b5f90
    0x00567B40,                                    # FUN_00567170 caller (in FUN_00567c50)
    0x00566100, 0x00565AB0, 0x00566CE0, 0x00566D20, 0x005666E0,  # FUN_00567c50 siblings
    # attribute-ID user functions (S5-validated)
    0x006BD1B0, 0x006BD330, 0x006BD4F0,
    0x00846430, 0x00847270, 0x0043F4B0, 0x005146B0,
    # attribute requesters
    0x00468910, 0x005B6890, 0x00626020, 0x004387A0,
    # walker internals + FUN_008553d0 helpers
    0x008544D0, 0x00413590, 0x00844880, 0x00844130, 0x00843D60, 0x00843DD0,
    0x00417EF0, 0x0085AD50, 0x00792B20, 0x0085B020, 0x0085B750, 0x006B22D0,
    0x00417EA0, 0x00415570, 0x008599A0, 0x0085A9F0, 0x00858BA0, 0x0085B1B0,
    0x0085AFD0, 0x00860EE0, 0x00860F60, 0x00861210, 0x00861230, 0x0072FD10,
    # state checkers
    0x009768D0, 0x00978A10,
    # parameter loader upward chain
    0x0094DFC0, 0x0094FE00,
    # create methods (slot1 of ArkObjectClassImpl) + base create
    0x0073A160, 0x00739E30, 0x0073A9E0, 0x0073AAF0, 0x0073A8D0, 0x0073B040,
    0x0070BF50,
    # FUN_00567c50 misc callees
    0x0050A7D0, 0x006C8CB0, 0x0048ADA0, 0x00414670, 0x00729EB0, 0x00401260,
    0x004151F0, 0x00866140, 0x00866E50, 0x005C2760, 0x0042BDB0, 0x0072D9F0,
    0x004AC4B0, 0x0041360,
]

CALLERS_OF = {
    "FUN_0058db50": 0x0058DB50,
    "FUN_005b72c0": 0x005B72C0,
    "FUN_00514ef0": 0x00514EF0,
    "FUN_005b6370": 0x005B6370,
    "FUN_0094dfc0": 0x0094DFC0,
    "FUN_0094fe00": 0x0094FE00,
    "FUN_0073a160_create_ParamContainer": 0x0073A160,
    "FUN_00739e30_create_ParamTransformation": 0x00739E30,
    "FUN_0073a9e0_create_RealWorldItem": 0x0073A9E0,
    "FUN_0073aaf0_create_RealWorldProvider": 0x0073AAF0,
    "FUN_0073a8d0_create_InteractiveWorldObject": 0x0073A8D0,
    "FUN_0073b040_create_ParamSetObject": 0x0073B040,
    "FUN_0070bf50_create_ArkObject": 0x0070BF50,
    "FUN_00835660_PacketDecoder_slot0": 0x00835660,
    "FUN_004b1210_ClientPacketExecutor_s0": 0x004B1210,
    "FUN_004b2950_ClientPacketExecutor_s1": 0x004B2950,
}

# vtable-store sites from S7 -> find containing function (ctor)
CONTAINING = [
    0x0074FFC8,   # ArkRealWorldItem vtable store
    0x00830083, 0x00831608, 0x00834F90,   # ArkStaticPacket
    0x0082FA22, 0x0082FD6A, 0x00831663,   # ArkPacket
    0x0083552F, 0x0083574E,               # ArkPacketDecoder
    0x004B105B, 0x004B1626,               # ArkClientPacketExecutor
    0x00852ACB, 0x00852B3A,               # ArkPortalResourceItem
    0x00851EB7, 0x0085213D,               # ArkPortalCell
    0x0084CE57, 0x0084E8BE,               # ArkPortalCellGraph
    0x004A9BA5, 0x004A9BE2, 0x004A9BDB, 0x004A9BB4, 0x004A9BAD, 0x004A9BE8,  # managers
]

# disasm windows for VA-locked evidence
DISASM_WINDOWS = [
    ("FUN_00567770_setter_calls", 0x00567860, 0x00567960),
    ("FUN_00567c50_call_00567770", 0x00568330, 0x00568390),
    ("FUN_00846840_walker_region", 0x00846850, 0x00846900),
    ("FUN_00567770_attr_reads", 0x00567770, 0x00567860),
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

def callers_of(va_int, limit=60):
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

def func_of(va_int):
    fn = fm.getFunctionContaining(toAddr(va_int))
    if fn is None:
        return None, None
    return fn.getName(), "0x%08X" % fn.getEntryPoint().getOffset()

def disasm_window(label, start_va, end_va):
    lines = []
    addr = toAddr(start_va)
    end = toAddr(end_va)
    while addr is not None and addr.getOffset() <= end.getOffset():
        ins = listing.getInstructionAt(addr)
        if ins is not None:
            fn, fe = func_of(addr.getOffset())
            lines.append("0x%08X  %-40s" % (addr.getOffset(), str(ins)))
        addr = addr.next()
    return lines

def scan_dword_aligned(value, block_names):
    # dword-aligned scan using getInt over block
    hits = []
    for block in mem.getBlocks():
        if block.getName() not in block_names:
            continue
        start = block.getStart().getOffset()
        size = block.getSize()
        for off in range(0, size - 3, 4):
            try:
                v = mem.getInt(toAddr(start + off)) & 0xFFFFFFFF
            except:
                continue
            if v == value:
                hits.append(start + off)
    return hits

def hunt_binds():
    tds = {
        "bind_mf0_ArkClientWorldObjectManager": 0x00B6F920,
        "bind_mf1_ArkClientWorldObjectManager": 0x00B6F9C0,
        "bind_free_CWOData_ArkClientWorldObjectLogic": 0x00B78CC0,
    }
    result = {}
    for label, td in tds.items():
        rec = {"td": "0x%08X" % td}
        col_hits = scan_dword_aligned(td, [".data", ".rdata"])
        rec["col_pointer_hits"] = ["0x%08X" % h for h in col_hits]
        vts = []
        for p in col_hits:
            col = p - 0x0C
            for q in scan_dword_aligned(col, [".data", ".rdata"]):
                vts.append(q + 4)
        rec["bind_vtables"] = ["0x%08X" % v for v in vts]
        sites = []
        for vt in vts:
            for r in rm.getReferencesTo(toAddr(vt)):
                fa = r.getFromAddress()
                fn2, fe2 = func_of(fa.getOffset())
                sites.append({"ref_from": "0x%08X" % fa.getOffset(),
                              "in_function": fn2, "func_entry": fe2,
                              "bind_vtable": "0x%08X" % vt})
        rec["construction_sites"] = sites
        result[label] = rec
    return result

def main():
    # A) decompile
    for va in DECOMPILE:
        fn = fm.getFunctionContaining(toAddr(va)) or fm.getFunctionAt(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "ZS2_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:24000])
    print("ZS2_A_done %d" % len(DECOMPILE))

    # B) callers
    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS2_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS2_B_done")

    # C) containing functions of vtable-store sites
    cont = []
    for va in CONTAINING:
        fn, fe = func_of(va)
        ins = listing.getInstructionContaining(toAddr(va))
        cont.append({"store_va": "0x%08X" % va, "in_function": fn,
                     "func_entry": fe, "instruction": str(ins) if ins else None})
    with open(os.path.join(OUT_RAW, "ZS2_VTABLESTORE_CONTAINING.json"), "w") as f:
        json.dump({"exec": EXEC, "sites": cont}, f, indent=2)
    print("ZS2_C_done")

    # D) bind hunt v2
    binds = {}
    try:
        binds = hunt_binds()
    except Exception as e:
        binds = {"error": str(e)}
    with open(os.path.join(OUT_RAW, "ZS2_BIND_HUNT.json"), "w") as f:
        json.dump({"exec": EXEC, "binds": binds}, f, indent=2)
    print("ZS2_D_done")

    # E) disasm windows
    for label, s, e in DISASM_WINDOWS:
        lines = disasm_window(label, s, e)
        with open(os.path.join(OUT_RAW, "ZS2_DISASM_%s.txt" % label), "w") as f:
            f.write("\n".join(lines))
    print("ZS2_E_done")

    print("ZS2_DONE")

main()
