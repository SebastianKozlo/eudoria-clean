# C5 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 5: template-object layout decode (parser/alloc/insert) + construction drivers.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C5_LAYOUT_AND_DRIVERS.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C5_LAYOUT_AND_DRIVERS.json"

CENSUS_TARGETS = [
    ("M01_driver_k01_00567b40", 0x00567B40),
    ("M02_driver_k02_005b6370", 0x005B6370),
    ("M03_driver_k03_00567c50", 0x00567C50),
    ("M04_driver_k04_006a2f60", 0x006A2F60),
]

DECOMP_TARGETS = [
    ("X01_parse_fields_00730c90", 0x00730C90),
    ("X02_alloc_004123d0", 0x004123D0),
    ("X03_insert_0072f8d0", 0x0072F8D0),
    ("X04_list1_copy_00566f80", 0x00566F80),
    ("X05_list2_copy_00525da0", 0x00525DA0),
    ("X06_driver_k01_00567b40", 0x00567B40),
    ("X07_driver_k02_005b6370", 0x005B6370),
    ("X08_driver_k03_00567c50", 0x00567C50),
    ("X09_driver_k04_006a2f60", 0x006A2F60),
    ("X10_visual_helper_006c8f80", 0x006C8F80),
    ("X11_prelookup_helper_0043a550", 0x0043A550),
    ("X12_valid_check_0072fce0", 0x0072FCE0),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C5_layout_and_drivers",
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
print("C5 written:", RESULT_PATH)
for (label, va) in CENSUS_TARGETS:
    c = result["measured"]["census"].get(label, {})
    print("%s 0x%08X sites=%s callers=%s" % (label, va, c.get("callsites"), c.get("unique_callers")))
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
