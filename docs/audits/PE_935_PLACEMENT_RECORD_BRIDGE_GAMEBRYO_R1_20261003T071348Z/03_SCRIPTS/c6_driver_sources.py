# C6 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 6: (a) caller census for construction drivers + unexamined lookup consumers;
# (b) decompilations: position generator, attach functions, dynamic factory, consumers.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C6_DRIVER_SOURCES.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C6_DRIVER_SOURCES.json"

CENSUS_TARGETS = [
    ("N01_emitter_006c3f50", 0x006C3F50),
    ("N02_dynfactory_006a34a0", 0x006A34A0),
    ("N03_driver2_00521770", 0x00521770),
    ("N04_driver3a_00514ef0", 0x00514EF0),
    ("N05_driver3b_0058db50", 0x0058DB50),
    ("N06_driver3c_005b72c0", 0x005B72C0),
    ("N07_consumer_006baa20", 0x006BAA20),
    ("N08_consumer_004e68a0", 0x004E68A0),
]

DECOMP_TARGETS = [
    ("Y01_posgen_00566100", 0x00566100),
    ("Y02_param_pos_00844130", 0x00844130),
    ("Y03_0048ada0", 0x0048ADA0),
    ("Y04_dynfactory_006a34a0", 0x006A34A0),
    ("Y05_driver2_00521770", 0x00521770),
    ("Y06_lazygetter_007376a0", 0x007376A0),
    ("Y07_consumer_006baa20", 0x006BAA20),
    ("Y08_consumer_004e68a0", 0x004E68A0),
    ("Y09_attach_b_0077c0b0", 0x0077C0B0),
    ("Y10_attach_f_0077c0f0", 0x0077C0F0),
    ("Y11_attach_120_0077c120", 0x0077C120),
    ("Y12_attach_090_0077c090", 0x0077C090),
    ("Y13_attach_100_0077c100", 0x0077C100),
    ("Y14_visual_005100d0", 0x005100D0),
    ("Y15_visual_0050a690", 0x0050A690),
    ("Y16_visual_006d0990", 0x006D0990),
    ("Y17_visual_00509570", 0x00509570),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C6_driver_sources",
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
print("C6 written:", RESULT_PATH)
for (label, va) in CENSUS_TARGETS:
    c = result["measured"]["census"].get(label, {})
    print("%s 0x%08X sites=%s callers=%s" % (label, va, c.get("callsites"), c.get("unique_callers")))
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
