# C8 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 8 (final Ghidra round): caller census of the emitter/driver top callers
# + decompilation of the remaining construction/attribute helpers.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C8_TOP_SOURCES.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C8_TOP_SOURCES.json"

CENSUS_TARGETS = [
    ("P01_emitter_arr_006c3fe0", 0x006C3FE0),
    ("P02_emitter_arr_006c4020", 0x006C4020),
    ("P03_driver_00468910", 0x00468910),
    ("P04_driver_004b18d0", 0x004B18D0),
]

DECOMP_TARGETS = [
    ("Q01_driver_00468910", 0x00468910),
    ("Q02_driver_004b18d0", 0x004B18D0),
    ("Q03_ctor3_005666e0", 0x005666E0),
    ("Q04_slotgetter_007333e0", 0x007333E0),
    ("Q05_attr_id2_00844660", 0x00844660),
    ("Q06_attr_float_00745690", 0x00745690),
    ("Q07_z10_helper_00746550", 0x00746550),
    ("Q08_posgen_helper_00565ab0", 0x00565AB0),
    ("Q09_attr_flag_009768d0", 0x009768D0),
    ("Q10_attr_flag_00844020", 0x00844020),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C8_top_sources",
    "measured": {"census": {}, "decompilations": {}},
    "interpreted": {},
    "errors": [],
}

for (label, va) in CENSUS_TARGETS:
    entry = {"va": "0x%08X" % va, "callsites": 0, "unique_callers": 0,
             "caller_list": [], "function_found": False}
    try:
        t = toAddr(va)
        func = getFunctionContaining(t)
        if func is None:
            entry["note"] = "no function containing VA"
            result["measured"]["census"][label] = entry
            continue
        fentry = func.getEntryPoint()
        entry["function_found"] = True
        entry["function_entry"] = "0x%08X" % fentry.getOffset()
        entry["function_name"] = func.getName()
        callers = {}
        for ref in getReferencesTo(fentry):
            if ref.getReferenceType().isCall():
                entry["callsites"] += 1
                caller = getFunctionContaining(ref.getFromAddress())
                if caller is not None:
                    ck = "0x%08X" % caller.getEntryPoint().getOffset()
                    rec = callers.setdefault(ck, {
                        "caller_entry": ck, "caller_name": caller.getName(),
                        "callsite_count": 0, "callsites": []})
                    rec["callsite_count"] += 1
                    rec["callsites"].append("0x%08X" % ref.getFromAddress().getOffset())
                else:
                    entry.setdefault("callsites_without_function", []).append(
                        "0x%08X" % ref.getFromAddress().getOffset())
        entry["unique_callers"] = len(callers)
        entry["caller_list"] = sorted(callers.values(),
                                      key=lambda r: (-r["callsite_count"], r["caller_entry"]))
        result["measured"]["census"][label] = entry
    except Exception as e:
        result["errors"].append("census %s: %s" % (label, str(e)))
        result["measured"]["census"][label] = entry

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
             "function_name": func.getName(),
             "body_size": int(func.getBody().getNumAddresses())}
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

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C8 written:", RESULT_PATH)
for (label, va) in CENSUS_TARGETS:
    c = result["measured"]["census"].get(label, {})
    print("%s 0x%08X sites=%s callers=%s" % (label, va, c.get("callsites"), c.get("unique_callers")))
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
