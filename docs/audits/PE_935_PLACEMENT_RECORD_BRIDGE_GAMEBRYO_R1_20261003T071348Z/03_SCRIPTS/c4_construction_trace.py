# C4 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 4: (a) caller census for construction-path functions; (b) decompilation wave 2.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C4_CONSTRUCTION_TRACE.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C4_CONSTRUCTION_TRACE.json"

CENSUS_TARGETS = [
    ("K01_placement_constr_A_00567170", 0x00567170),
    ("K02_placement_constr_B_005b5f90", 0x005B5F90),
    ("K03_attr_placement_builder_00567770", 0x00567770),
    ("K04_arkclientlocaldynamic_ctor_006a3930", 0x006A3930),
    ("K05_base_object_builder_004c5580", 0x004C5580),
    ("K06_post_lookup_helper_005670a0", 0x005670A0),
    ("K07_visual_ctor_006c0d50", 0x006C0D50),
    ("K08_pos_compute_006c1f90", 0x006C1F90),
    ("K09_template_out_0072fe30", 0x0072FE30),
    ("K10_visual_check_006c4200", 0x006C4200),
]

DECOMP_TARGETS = [
    ("W01_helper_005670a0", 0x005670A0),
    ("W02_visual_ctor_006c0d50", 0x006C0D50),
    ("W03_pos_compute_006c1f90", 0x006C1F90),
    ("W04_template_out_0072fe30", 0x0072FE30),
    ("W05_visual_check_006c4200", 0x006C4200),
    ("W06_attr_builder_00567770", 0x00567770),
    ("W07_ctor_base_006a3bd0", 0x006A3BD0),
    ("W08_deserA_007453d0", 0x007453D0),
    ("W09_record_init_00730f60", 0x00730F60),
    ("W10_register_00457930", 0x00457930),
    ("W11_firstcall_004c5bd0", 0x004C5BD0),
    ("W12_firstcall_004e3b70", 0x004E3B70),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C4_construction_trace",
    "measured": {"census": {}, "decompilations": {}},
    "interpreted": {},
    "errors": [],
}

for (label, va) in CENSUS_TARGETS:
    entry = {"va": "0x%08X" % va, "callsites": 0, "unique_callers": 0,
             "caller_list": [], "noncall_refs": 0, "function_found": False}
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
        entry["body_size"] = int(func.getBody().getNumAddresses())
        callers = {}
        for ref in getReferencesTo(fentry):
            try:
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
                else:
                    entry["noncall_refs"] += 1
            except Exception as e:
                result["errors"].append("ref %s: %s" % (label, str(e)))
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

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C4 written:", RESULT_PATH)
for (label, va) in CENSUS_TARGETS:
    c = result["measured"]["census"].get(label, {})
    print("%s 0x%08X sites=%s callers=%s" % (label, va, c.get("callsites"), c.get("unique_callers")))
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
