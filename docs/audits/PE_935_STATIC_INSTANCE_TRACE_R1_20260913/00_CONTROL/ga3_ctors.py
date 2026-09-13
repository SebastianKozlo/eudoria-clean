# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA3: vtable entries + constructors (xrefs to vtable) + decompile key ctors.
# Input: 01_RAW/S4_RTTI_VTABLES.json (offline COL resolution).
# Writes: 01_RAW\ghidra_output\GA3_VTABLE_ENTRIES.json, GA3_CTOR_*.txt

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
VT_JSON = os.path.join(RUN_ROOT, "01_RAW", "S4_RTTI_VTABLES.json")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()

EXEC = {
    "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "phase": "GA3_vtable_entries_ctors",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

# classes whose ctors get decompiled
DECOMP_CTORS_FOR = [
    "ArkSceneObject", "ArkModelResourceInstanceRef", "ArkPortalCell",
    "WorldSubsystem", "ArkObject", "ArkObjectClass", "ArkClientObjectManagerImpl",
    "ArkObjectService", "ArkObjectCommander", "ArkRealWorldItem",
    "ArkInteractiveWorldObject", "ArkClientInteractiveWorldObjectImpl",
    "ArkClientDefaultObjectImpl", "NiNode", "NiAVObject",
    "ArkTerrainEditZoneFactory", "ArkTerrainEditZoneGroup",
    "ArkVegetationClimateFactory", "ArkVegetationClimate",
    "ArkTerrainPatchFactory", "ArkHeightFieldSource",
]

def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None

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

def disasm_func(fn, max_inst=500):
    out = []
    inst = listing.getInstructionAt(fn.getEntryPoint())
    if inst is None:
        inst = listing.getInstructionContaining(fn.getEntryPoint())
    n = 0
    while inst is not None and n < max_inst:
        out.append("0x%08X  %-28s %s" % (inst.getAddress().getOffset(),
                                         bytes_hex(inst) or "", inst.toString()))
        inst = inst.getNext()
        n += 1
    return "\n".join(out)

def read_vtable(va, n=40):
    out = []
    mem = currentProgram.getMemory()
    base = toAddr(va)
    for i in range(n):
        a = base.add(i * 4)
        try:
            fv = mem.getInt(a) & 0xFFFFFFFF
        except:
            break
        if fv == 0:
            break
        fn = fm.getFunctionContaining(toAddr(fv))
        out.append({
            "slot": i, "target": "0x%08X" % fv,
            "func": fn.getName() if fn else None,
        })
    return out

def xrefs_to(va, limit=30):
    res = []
    for r in rm.getReferencesTo(toAddr(va)):
        fa = r.getFromAddress()
        fn = fm.getFunctionContaining(fa)
        res.append({
            "from_va": "0x%08X" % fa.getOffset(),
            "ref_type": str(r.getReferenceType()),
            "in_function": fn.getName() if fn else None,
            "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None,
        })
        if len(res) >= limit:
            break
    return res

def main():
    vtdata = json.load(open(VT_JSON))["classes"]

    all_entries = {}
    ctor_funcs = {}
    for cls, rec in vtdata.items():
        cls_recs = []
        for v in rec.get("vtables", []):
            vt_va = int(v["vtable"], 16)
            entries = read_vtable(vt_va, 40)
            xr = xrefs_to(vt_va, 30)
            cls_recs.append({
                "vtable": v["vtable"], "col": v["col"],
                "entries": entries, "xrefs_to_vtable": xr,
            })
            for x in xr:
                if x.get("func_entry"):
                    ctor_funcs.setdefault(cls, set()).add(int(x["func_entry"], 16))
        all_entries[cls] = cls_recs

    with open(os.path.join(OUT_RAW, "GA3_VTABLE_ENTRIES.json"), "w") as f:
        json.dump({"exec": EXEC, "classes": all_entries}, f, indent=2)

    # decompile ctors for selected classes
    summary = {}
    for cls in DECOMP_CTORS_FOR:
        entries_v = ctor_funcs.get(cls, set())
        summary[cls] = ["0x%08X" % e for e in sorted(entries_v)]
        for e in sorted(entries_v)[:6]:
            fn = fm.getFunctionContaining(toAddr(e))
            if fn is None:
                continue
            c = decompile(fn)
            with open(os.path.join(OUT_RAW, "GA3_CTOR_%s_%08X.txt" % (cls, e)), "w") as f:
                f.write("// %s ctor-candidate @0x%08X body=%s\n" % (
                    cls, e, "0x%08X-0x%08X" % (fn.getBody().getMinAddress().getOffset(),
                                               fn.getBody().getMaxAddress().getOffset())))
                f.write((c or "// decompile failed")[:16000])
                f.write("\n\n---- DISASM (first 260) ----\n")
                f.write(disasm_func(fn, 260))

    with open(os.path.join(OUT_RAW, "GA3_CTOR_INDEX.json"), "w") as f:
        json.dump({"exec": EXEC, "ctor_xref_functions": summary}, f, indent=2)

    print("GA3_DONE classes=%d decomp_classes=%d" % (len(all_entries), len(summary)))

main()
