# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA4: containing functions of S5 transform-write hits + caller chains of
# key creation functions + vtable 0x00A86E4C owners + targeted decompile.
# Writes: 01_RAW\ghidra_output\GA4_*.json/txt

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
S5_JSON = os.path.join(RUN_ROOT, "01_RAW", "S5_TRANSFORM_WRITES.json")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "phase": "GA4_hit_functions_callers",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None

def callers_of(va_int, limit=30):
    res = []
    addr = toAddr(va_int)
    fn = fm.getFunctionContaining(addr) or fm.getFunctionAt(addr)
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

def decompile(func, max_secs=90):
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

def func_info(va_int):
    fn = fm.getFunctionContaining(toAddr(va_int))
    if fn is None:
        fn = fm.getFunctionAt(toAddr(va_int))
    if fn is None:
        return None
    return {"name": fn.getName(),
            "entry": "0x%08X" % fn.getEntryPoint().getOffset(),
            "body": "0x%08X-0x%08X" % (fn.getBody().getMinAddress().getOffset(),
                                      fn.getBody().getMaxAddress().getOffset())}

def main():
    s5 = json.load(open(S5_JSON))["results"]

    # 1) containing functions of all hits
    hit_funcs = {}
    for bucket in ["local_translate_triples", "world_translate_triples",
                   "fstp_store_hits", "rotate_runs"]:
        for r in s5.get(bucket, []):
            va = int(r["first_store_va"] if "first_store_va" in r else r["va"], 16)
            fi = func_info(va)
            key = (fi["entry"] if fi else "NONE")
            hit_funcs.setdefault(key, {"func": fi, "hits": []})["hits"].append(
                {"bucket": bucket, "va": r.get("first_store_va") or r["va"]})

    with open(os.path.join(OUT_RAW, "GA4_HIT_FUNCTIONS.json"), "w") as f:
        json.dump({"exec": EXEC, "hit_functions": hit_funcs}, f, indent=2)

    # 2) callers of key creation functions
    key_callsites = {
        "ArkObject_ctor_00726e70": 0x00726E70,
        "complete_consumer_006b4c50": 0x006B4C50,
        "WorldSubsystem_ctor_0048d170": 0x0048D170,
        "WorldSubsystem_ctor2_0048e170": 0x0048E170,
        "template_loader_0072fa30": 0x0072FA30,
        "NIFloader_portals_006f1b90": 0x006F1B90,
        "reset_transform_006f2a?": 0x006F2AF0,
        "CWO_004c5580": 0x004C5580,
    }
    callers = {}
    for label, va in key_callsites.items():
        callers[label] = callers_of(va, 40)

    with open(os.path.join(OUT_RAW, "GA4_KEY_CALLERS.json"), "w") as f:
        json.dump({"exec": EXEC, "callers": callers}, f, indent=2)

    # 3) vtable 0x00A86E4C references (class at 0x00735226 ctor)
    vt_refs = []
    for r in rm.getReferencesTo(toAddr(0x00A86E4C)):
        fa = r.getFromAddress()
        fn = fm.getFunctionContaining(fa)
        vt_refs.append({"from_va": "0x%08X" % fa.getOffset(),
                        "in_function": fn.getName() if fn else None,
                        "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None})
    with open(os.path.join(OUT_RAW, "GA4_VT_A86E4C_REFS.json"), "w") as f:
        json.dump(vt_refs, f, indent=2)

    # 4) decompile containing functions of the most interesting hit functions
    #    (all unique) + the two ctor-side functions with vtable store
    seen = set()
    decomp_targets = []
    for key, rec in hit_funcs.items():
        if key == "NONE":
            continue
        if key not in seen:
            seen.add(key)
            decomp_targets.append(int(key, 16))
    # plus callers of ArkObject ctor (up to 12 decompiled)
    for c in callers.get("ArkObject_ctor_00726e70", [])[:12]:
        if c.get("func_entry"):
            fe = int(c["func_entry"], 16)
            if fe not in seen:
                seen.add(fe)
                decomp_targets.append(fe)

    for va in decomp_targets[:40]:
        fn = fm.getFunctionContaining(toAddr(va))
        if fn is None:
            continue
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "GA4_PSEUDO_%08X.txt" % fn.getEntryPoint().getOffset()), "w") as f:
            f.write("// body=%s\n" % ("0x%08X-0x%08X" % (
                fn.getBody().getMinAddress().getOffset(),
                fn.getBody().getMaxAddress().getOffset())))
            f.write((c or "// decompile failed")[:20000])

    print("GA4_DONE hit_funcs=%d targets=%d" % (len(hit_funcs), len(decomp_targets)))

main()
