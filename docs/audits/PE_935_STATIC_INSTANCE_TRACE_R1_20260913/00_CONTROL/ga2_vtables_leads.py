# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA2: RTTI vtables + constructors for key classes (Ni* + Ark world/object)
#            + decompile CWO leads + NiAVObject GetViewerStrings field-offset oracle.
#
# A) For each class: find "::vftable" symbol (Ghidra RTTI naming); list vtable
#    function entries (bounded 32); xrefs to vtable (= ctors storing vftable).
# B) Decompile bounded: FUN_0050d480 (CWO logic), FUN_006f1b90 (portal defs),
#    FUN_00933310 (NetImmerseScene::Root), FUN_007c04f0 (NiAVObject::GetViewerStrings).
# C) Disasm FUN_007c04f0 fully (field offsets ground truth).
# Writes: 01_RAW\ghidra_output\GA2_*.json/txt

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()
st = currentProgram.getSymbolTable()

EXEC = {
    "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "phase": "GA2_vtables_and_leads",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

CLASSES = [
    "NiObjectNET", "NiAVObject", "NiNode", "NiCamera", "NiTriShape",
    "NiSwitchNode", "NiBillboardNode", "NiLODNode", "NiBSPNode",
    "ArkSceneObject", "ArkSceneObjectFactory", "ArkModelSource", "ArkModelInterface",
    "ArkPortalCell", "ArkPortalCellGraph", "ArkPortalPortal",
    "ArkPortalResourceItem", "ArkPortalResourceItemFactory", "ArkPortalIdGenerator",
    "ArkModelResourceInstanceRef", "ArkModelResourceItem", "ArkModelResourceItemFactory",
    "ArkRealWorldItem", "ArkRealWorldProvider",
    "ArkInteractiveWorldObject", "ArkClientInteractiveWorldObjectImpl",
    "ArkClientDefaultObjectImpl", "ArkObject", "ArkObjectClass", "ArkObjectClassInterface",
    "WorldSubsystem", "ArkClientDynamicObject", "ArkInstanceProxy", "ArkRefObject",
    "ArkVegetationClimate", "ArkTerrainEditZoneFactory", "ArkTerrainEditZoneGroup",
    "ArkTerrainPatchFactory", "ArkHeightFieldSource", "ArkVegetationClient",
    "ArkClientObjectManagerImpl", "ArkObjectService", "ArkObjectCommander",
]

DECOMP_TARGETS = [
    ("FUN_0050d480", 0x0050D480, 30000),
    ("FUN_006f1b90", 0x006F1B90, 20000),
    ("FUN_00933310", 0x00933310, 20000),
    ("FUN_007c04f0", 0x007C04F0, 30000),
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

def find_vftable(cls):
    # Ghidra RTTI naming: "ClassName::vftable" or mangled "??_7ClassName@@6B@"
    for sym in st.getSymbols(cls + "::vftable"):
        return sym
    # fallback: iterate all symbols with 'vftable' in name
    return None

def read_vtable(va, n=32):
    out = []
    base = toAddr(va)
    mem = currentProgram.getMemory()
    for i in range(n):
        a = base.add(i * 4)
        try:
            fv = mem.getInt(a) & 0xFFFFFFFF
        except:
            break
        fn = fm.getFunctionContaining(toAddr(fv))
        out.append({
            "slot": i,
            "target": "0x%08X" % fv,
            "func": fn.getName() if fn else None,
        })
    return out

def xrefs_to(va, only_calls=False, limit=40):
    res = []
    for r in rm.getReferencesTo(toAddr(va)):
        if only_calls and not r.getReferenceType().isCall():
            continue
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
    # ---------- A) vtables ----------
    vt_out = {}
    for cls in CLASSES:
        rec = {"class": cls}
        sym = find_vftable(cls)
        if sym is None:
            # try mangled search
            cands = []
            it = st.getSymbolIterator()
            for s in it:
                nm = s.getName()
                if "vftable" in nm and cls in nm:
                    cands.append((s.getName(), s.getAddress().getOffset()))
                    if len(cands) >= 5:
                        break
            rec["candidates"] = [{"name": n, "va": "0x%08X" % v} for n, v in cands]
            if cands:
                va = cands[0][1]
                rec["vftable_va"] = "0x%08X" % va
                rec["entries"] = read_vtable(va, 32)
                rec["xrefs_to_vftable"] = xrefs_to(va, False, 40)
        else:
            va = sym.getAddress().getOffset()
            rec["vftable_va"] = "0x%08X" % va
            rec["entries"] = read_vtable(va, 32)
            rec["xrefs_to_vftable"] = xrefs_to(va, False, 40)
        vt_out[cls] = rec
    with open(os.path.join(OUT_RAW, "GA2_VTABLES.json"), "w") as f:
        json.dump({"exec": EXEC, "vtables": vt_out}, f, indent=2)

    # ---------- B) decompile leads ----------
    for name, va, cap in DECOMP_TARGETS:
        fn = fm.getFunctionContaining(toAddr(va))
        if fn is None:
            fn = fm.getFunctionAt(toAddr(va))
        c = decompile(fn)
        with open(os.path.join(OUT_RAW, "GA2_PSEUDO_%s.txt" % name), "w") as f:
            f.write("// FUN @0x%08X  body=%s\n" % (
                va, ("0x%08X-0x%08X" % (fn.getBody().getMinAddress().getOffset(),
                                        fn.getBody().getMaxAddress().getOffset())) if fn else "NONE"))
            f.write((c or "// decompile failed")[:cap])

        # disasm bounded first 400 instructions
        with open(os.path.join(OUT_RAW, "GA2_DISASM_%s.txt" % name), "w") as f:
            if fn is None:
                f.write("// no function")
                continue
            inst = listing.getInstructionAt(fn.getEntryPoint())
            if inst is None:
                inst = listing.getInstructionContaining(fn.getEntryPoint())
            n = 0
            while inst is not None and n < 400:
                f.write("0x%08X  %-28s %s\n" % (
                    inst.getAddress().getOffset(), bytes_hex(inst) or "",
                    inst.toString()))
                inst = inst.getNext()
                n += 1

    print("GA2_DONE classes=%d decomp=%d" % (len(CLASSES), len(DECOMP_TARGETS)))

main()
