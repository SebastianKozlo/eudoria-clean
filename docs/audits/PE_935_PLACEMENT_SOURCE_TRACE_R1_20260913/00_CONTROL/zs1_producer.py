# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython 2) - RUN PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913
# STAGE ZS1: attribute-container producer slice.
#  A) Decompile: walker family + upward chain (FUN_00567c50) + singleton ctors +
#     CWO-deriver helpers + parameter-class vtable slot0 methods + packet/communicator
#     vtable methods + portal reader methods.
#  B) Callers-of census for the chain functions.
#  C) S5 immediate-hit validation: every .text raw hit -> containing instruction,
#     function, disasm window (proves instruction boundary; raw hits alone claim nothing).
#  D) Bind-object hunting: COL->vtable->xrefs for the ArkClientWorldObjectManager/
#     CWOData bind type descriptors -> construction sites (member function pointers).
# Writes: 01_RAW\ghidra_output\ZS1_*.txt/.json

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()
mem = currentProgram.getMemory()

EXEC = {
    "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "phase": "ZS1_attribute_producer",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

# ---- A) decompile targets ------------------------------------------------
DECOMPILE = [
    # upward chain of the placement-record builder
    0x00567C50,                     # sole caller of FUN_00567770
    0x004576E0,                     # ctor of 0x178 singleton (DAT_00ba1288 via FUN_004148f0)
    # attribute walker family (readers)
    0x0085B840, 0x0085B860, 0x0085ACB0, 0x0085B1A0, 0x0085B050, 0x0085B190, 0x0085AC50,
    # helpers used by the fetchers
    0x004123D0, 0x00413440, 0x00413450, 0x00971780,
    # singleton + accessors
    0x008550C0, 0x008553D0, 0x00844AE0, 0x00853A50, 0x00844020,
    # FUN_00457930 helpers
    0x00414770, 0x00446800, 0x00567030, 0x00855DC0, 0x0059F0D0, 0x0050A690, 0x00509190, 0x006C4200,
    # matrix helpers used by FUN_00567770/FUN_00846840
    0x0096C920, 0x0096CDD0,
    # CWO-deriver + getters
    0x004C5580, 0x00733340, 0x00746550, 0x007CE1E0,
    # record ctor
    0x00730700, 0x00730730,
    # parameter-class slot0 (class-specific virtual)
    0x00761230, 0x00760FE0, 0x00745EA0,
    # network family virtuals
    0x00835660, 0x0082FD60, 0x00833030, 0x00834ED0, 0x00834EC0,
    0x004B1210, 0x004B2950, 0x004A9810,
    # portal family (Z3 reader candidates)
    0x0041B870, 0x0084B270, 0x0084EC00, 0x0084E7F0, 0x0084D650, 0x0084D750, 0x0084C2C0,
    0x00850C50, 0x00852A30, 0x00852B80,
    # parameter file loaders ("Data\Parameters\" xrefs from RUN 3 Z5)
    0x0094BA00, 0x0094F250,
]

# ---- B) callers of -------------------------------------------------------
CALLERS_OF = {
    "FUN_00567c50": 0x00567C50,
    "FUN_00846840_attrpos": 0x00846840,
    "FUN_00854720_attrtriple": 0x00854720,
    "FUN_004154f0_singleton8c": 0x004154F0,
    "FUN_00567170_builder": 0x00567170,
    "FUN_005b5f90_builder": 0x005B5F90,
    "FUN_004c5580_cwoderiver": 0x004C5580,
    "FUN_00746550_getterfamily": 0x00746550,
    "FUN_007ce1e0_getterA": 0x007CE1E0,
    "FUN_008550c0_singletonctor": 0x008550C0,
    "FUN_00730700_recctor": 0x00730700,
    "FUN_00761230_paramcontainer_slot0": 0x00761230,
    "FUN_00760FE0_paramtransf_slot0": 0x00760FE0,
    "FUN_0094ba00_paramloader": 0x0094BA00,
    "FUN_0094f250_paramloader": 0x0094F250,
}

def decompile(func, max_secs=120):
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

def func_entry(va_int):
    fn = fm.getFunctionContaining(toAddr(va_int)) or fm.getFunctionAt(toAddr(va_int))
    if fn is None:
        return None, None
    return fn.getName(), "0x%08X" % fn.getEntryPoint().getOffset()

# ---- C) S5 hit validation --------------------------------------------------
def validate_s5():
    p = os.path.join(RUN_ROOT, "01_RAW", "S5_IMMEDIATE_SCAN.json")
    if not os.path.isfile(p):
        return {"error": "S5 file missing"}
    d = json.load(open(p))
    out = {}
    decomp_extra = []
    for key, lst in d.get("hits", {}).items():
        if key == "neighbours":
            sub = {}
            for k2, v2 in lst.items():
                rows = []
                for h in v2:
                    if h.get("sec") != ".text":
                        continue
                    va = int(h["va"], 16)
                    instr = listing.getInstructionContaining(toAddr(va))
                    fn, fe = func_entry(va)
                    rows.append({
                        "va": h["va"],
                        "in_instruction": str(instr) if instr else None,
                        "function": fn, "func_entry": fe,
                    })
                sub[k2] = rows
            out["neighbours"] = sub
            continue
        rows = []
        for h in lst:
            if h.get("sec") != ".text":
                continue
            va = int(h["va"], 16)
            instr = listing.getInstructionContaining(toAddr(va))
            fn, fe = func_entry(va)
            rows.append({
                "va": h["va"],
                "in_instruction": str(instr) if instr else None,
                "function": fn, "func_entry": fe,
            })
            if rows[-1]["in_instruction"] is None:
                rows[-1]["note"] = "NO INSTRUCTION AT/OVER THIS BYTE (not an instruction candidate)"
        out[key] = rows
    return out

# ---- D) bind-object hunting ------------------------------------------------
def dword_at(va_int):
    return mem.getInt(toAddr(va_int)) & 0xFFFFFFFF

def hunt_binds():
    # bind type descriptors (string VA - 8 = TD)
    tds = {
        "bind_mf0_ArkClientWorldObjectManager": 0x00B6F920,
        "bind_mf1_ArkClientWorldObjectManager": 0x00B6F9C0,
        "bind_free_CWOData_ArkClientWorldObjectLogic": 0x00B78CC0,
    }
    result = {}
    # scan .data and .rdata for COL pointers == TD
    # Ghidra: iterate over memory blocks .data/.rdata and find dwords == value
    def scan_dwords(value, block_names, max_hits=20):
        hits = []
        for block in mem.getBlocks():
            if block.getName() not in block_names:
                continue
            start = block.getStart()
            end = block.getEnd()
            addr = start
            cnt = 0
            # use findBytes? For dwords iterate by 4 is too slow in Java loop via Jython
            # -> use ReferenceManager? Not all dwords are referenced.
            # Fallback: read block bytes in chunks and scan in Python.
            data = block.getBytes(start, block.getSize()).tostring() if hasattr(block.getBytes(start, block.getSize()), 'tostring') else None
            return_data = []
            try:
                size = block.getSize()
                ba = jarray.zeros(size, 'b')  # noqa: F821 (jython jarray)
                block.getBytes(start, ba)
                data = ba.tostring()
            except:
                return []
            import struct as _s
            pat = _s.pack("<i", value)
            off = 0
            while True:
                idx = data.find(pat, off)
                if idx < 0:
                    break
                return_data.append(start.getOffset() + idx)
                off = idx + 1
                if len(return_data) >= max_hits:
                    break
            hits = return_data
        return hits

    for label, td in tds.items():
        rec = {"td": "0x%08X" % td}
        col_hits = scan_dwords(td, [".data", ".rdata"])
        rec["col_pointer_hits"] = ["0x%08X" % h for h in col_hits]
        vts = []
        for p in col_hits:
            col = p - 0x0C
            for q in scan_dwords(col, [".data", ".rdata"]):
                vt = q + 4
                vts.append(vt)
        rec["bind_vtables"] = ["0x%08X" % v for v in vts]
        # xrefs to bind vtables -> construction sites
        sites = []
        for vt in vts:
            fn, fe = func_entry(vt)
            for r in rm.getReferencesTo(toAddr(vt)):
                fa = r.getFromAddress()
                fn2, fe2 = func_entry(fa.getOffset())
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
        with open(os.path.join(OUT_RAW, "ZS1_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:20000])
    print("ZS1_A_done %d targets" % len(DECOMPILE))

    # B) callers
    cq = {}
    for label, va in CALLERS_OF.items():
        cq[label] = callers_of(va)
    with open(os.path.join(OUT_RAW, "ZS1_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": cq}, f, indent=2)
    print("ZS1_B_done")

    # C) S5 validation
    s5 = validate_s5()
    with open(os.path.join(OUT_RAW, "ZS1_S5_VALIDATION.json"), "w") as f:
        json.dump(s5, f, indent=2)
    print("ZS1_C_done")

    # D) binds
    binds = {}
    try:
        binds = hunt_binds()
    except Exception as e:
        binds = {"error": str(e)}
    with open(os.path.join(OUT_RAW, "ZS1_BIND_HUNT.json"), "w") as f:
        json.dump({"exec": EXEC, "binds": binds}, f, indent=2)
    print("ZS1_D_done")

    print("ZS1_DONE")

main()
