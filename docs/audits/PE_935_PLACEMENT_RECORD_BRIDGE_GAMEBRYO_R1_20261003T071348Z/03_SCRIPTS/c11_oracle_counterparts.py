# C11 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 11 (oracle closure): Entropia-side counterparts for the 3 Gamebryo mechanisms
# + NiNode vtable discovery via NiRTTI 0x00BA7218 + UpdateWorldData slot re-pin
# + FUN_006c4060 decompilation (hardcoded id2 arrays).
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C11_ORACLE_COUNTERPARTS.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C11_ORACLE_COUNTERPARTS.json"

DECOMP_TARGETS = [
    ("O01_ninode_ctor_007b6000", 0x007B6000),
    ("O02_setname_007b67e0", 0x007B67E0),
    ("O03_namedinst_007796d0", 0x007796D0),
    ("O04_emitter_caller_006c4060", 0x006C4060),
]

RTTI_NINODE = 0x00BA7218

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C11_oracle_counterparts",
    "measured": {"decompilations": {}, "rtti_refs": [], "vtable_discovery": {},
                 "update_world_data_window": []},
    "interpreted": {},
    "errors": [],
}

# 1. decompilations
di = DecompInterface()
di.openProgram(currentProgram)
try:
    for (label, va) in DECOMP_TARGETS:
        t = toAddr(va)
        func = getFunctionContaining(t)
        if func is None:
            result["measured"]["decompilations"][label] = {
                "va": "0x%08X" % va, "ok": False, "error": "no function"}
            continue
        res = di.decompileFunction(func, 180, ConsoleTaskMonitor())
        d = {"va": "0x%08X" % va,
             "function_entry": "0x%08X" % func.getEntryPoint().getOffset(),
             "function_name": func.getName()}
        if res.decompileCompleted():
            c = res.getDecompiledFunction().getC()
            d["ok"] = True
            d["c_line_count"] = len(c.split("\n"))
            d["c"] = c
        else:
            d["ok"] = False
            d["error"] = res.getErrorMessage()
        result["measured"]["decompilations"][label] = d
finally:
    di.dispose()

# 2. references to NiRTTI 0x00BA7218 (GetRTTI return) -> find the GetRTTI function
try:
    rtti_addr = toAddr(RTTI_NINODE)
    refs = getReferencesTo(rtti_addr)
    for ref in refs:
        frm = ref.getFromAddress()
        fn = getFunctionContaining(frm)
        result["measured"]["rtti_refs"].append({
            "from": "0x%08X" % frm.getOffset(),
            "ref_type": str(ref.getReferenceType()),
            "in_function": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None,
            "function_name": fn.getName() if fn else None,
        })
except Exception as e:
    result["errors"].append("rtti refs: %s" % str(e))

# 3. locate NiNode vtable: find data references TO the GetRTTI function (vtable slot 2)
try:
    getrtti_fn = None
    for r in result["measured"]["rtti_refs"]:
        if r["in_function"] and r["function_name"] and "GetRTTI" in r["function_name"]:
            getrtti_fn = r
    # fallback: any function referencing the RTTI constant and returning it
    # search data refs to each such function
    for r in result["measured"]["rtti_refs"]:
        if not r["in_function"]:
            continue
        fva = int(r["in_function"], 16)
        faddr = toAddr(fva)
        drefs = []
        for dref in getReferencesTo(faddr):
            if not dref.getReferenceType().isCall():
                drefs.append("0x%08X" % dref.getFromAddress().getOffset())
        if drefs:
            result["measured"]["vtable_discovery"].setdefault("data_refs_to_getrtti_fns", []).append({
                "function": r["in_function"], "name": r["function_name"], "data_refs": drefs})
except Exception as e:
    result["errors"].append("vtable discovery: %s" % str(e))

# 4. UpdateWorldData window: prior canon (NINODE_SLOT17) = vtable slot 27 of NiNode.
# We scan the discovered vtable data refs for a table whose slot 27 function contains
# the distinctive rep movsd x13 copying m_kLocal -> m_kWorld (+0x38 -> +0x6C).
try:
    listing = currentProgram.getListing()
    mem = currentProgram.getMemory()
    # read candidate vtables (data refs found above); for each, read slots 0..30
    cands = result["measured"]["vtable_discovery"].get("data_refs_to_getrtti_fns", [])
    tables = []
    for cand in cands:
        for dr in cand["data_refs"]:
            va = int(dr, 16)
            # a vtable slot 2 pointer equals the GetRTTI fn; check the table at va-8
            base = va - 8
            try:
                slots = []
                for i in range(31):
                    pv = mem.getInt(toAddr(base + i * 4)) & 0xFFFFFFFF
                    slots.append("0x%08X" % pv)
                if int(slots[2], 16) == int(cand["function"], 16):
                    tables.append({"vtable_base": "0x%08X" % base, "slots_0_30": slots})
            except Exception as e2:
                result["errors"].append("vtable read at 0x%08X: %s" % (base, str(e2)))
    result["measured"]["vtable_discovery"]["candidate_tables"] = tables
    # for each table, dump listing of slot 27 function (first 40 instructions)
    for tab in tables:
        slot27 = int(tab["slots_0_30"][27], 16)
        fn = getFunctionContaining(toAddr(slot27))
        if fn is None:
            continue
        ins_list = []
        it = listing.getInstructions(fn.getBody(), True)
        cnt = 0
        while it.hasNext() and cnt < 44:
            i = it.next()
            ins_list.append({
                "addr": "0x%08X" % i.getAddress().getOffset(),
                "bytes": " ".join("%02X" % (b & 0xFF) for b in i.getBytes()),
                "text": i.toString()})
            cnt += 1
        result["measured"]["update_world_data_window"].append({
            "vtable_base": tab["vtable_base"], "slot27": "0x%08X" % slot27,
            "function_entry": "0x%08X" % fn.getEntryPoint().getOffset(),
            "instructions": ins_list})
except Exception as e:
    result["errors"].append("update world data: %s" % str(e))

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C11 written:", RESULT_PATH)
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("rtti refs:", len(result["measured"]["rtti_refs"]))
print("tables:", len(result["measured"]["vtable_discovery"].get("candidate_tables", [])))
print("uwd windows:", len(result["measured"]["update_world_data_window"]))
print("errors:", result["errors"][:10])
