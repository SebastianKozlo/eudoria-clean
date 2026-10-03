# C2 CALLER CENSUS - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Machine census: CALL xrefs to load-bearing chain functions of the PCG 9.3.5 client
# (Entropia.exe, image base 0x00400000, ASLR off). Jython 2.7 (Ghidra 11.2.1).
# Census denominator: the 19 target functions listed below.
# Also decompiles 4 functions needed for the family-selection step.
# Output: 01_RAW/C2_CALLER_CENSUS.json in the run package.

import json
import time

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C2_CALLER_CENSUS.json"

# census targets (VAs; Entropia.exe 9.3.5)
TARGETS = [
    ("T01_template_registry_lookup", 0x0072F580),
    ("T02_templates_vfs_reader", 0x0072FA30),
    ("T03_arkobject_factory_vt1", 0x0070BF50),
    ("T04_arkobject_ctor", 0x00726E70),
    ("T05_model_request_pump", 0x006C9700),
    ("T06_model_instance_creator", 0x006CB6F0),
    ("T07_named_instance_builder", 0x006CB020),
    ("T08_template_to_placement_record", 0x004C5580),
    ("T09_pending_attach_processor", 0x006CB3C0),
    ("T10_getter_A", 0x007CE1E0),
    ("T11_placement_record_deser_A", 0x007453D0),
    ("T12_placement_record_deser_B", 0x004C47F0),
    ("T13_attr_tree_getter", 0x00846840),
    ("T14_placement_builder_from_attrs", 0x00567770),
    ("T15_pos_setter", 0x00730F90),
    ("T16_rot_setter", 0x00730FB0),
    ("T17_thirdd_setter", 0x00730FD0),
    ("T18_record_setter_init", 0x00730F60),
    ("T19_v20002_selected_reader", 0x009777F0),
]

DECOMPILE = [
    ("D01", 0x0072F580),
    ("D02", 0x004C5580),
    ("D03", 0x00726E70),
    ("D04", 0x0070BF50),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C2_caller_census",
    "measured": {"program_name": None, "image_base": None, "census_denominator": len(TARGETS),
                 "targets": {}, "decompilations": {}},
    "interpreted": {},
    "errors": [],
}

try:
    result["measured"]["program_name"] = currentProgram.getName()
    result["measured"]["image_base"] = "0x%08X" % currentProgram.getImageBase().getOffset()
except Exception as e:
    result["errors"].append("program_read: %s: %s" % (type(e).__name__, str(e)))

for (label, va) in TARGETS:
    entry = {
        "va": "0x%08X" % va,
        "function_found": False,
        "callsites": 0,
        "unique_callers": 0,
        "caller_list": [],
        "noncall_refs": 0,
    }
    try:
        t = toAddr(va)
        func = getFunctionContaining(t)
        if func is None:
            entry["note"] = "no function containing VA"
            result["measured"]["targets"][label] = entry
            continue
        fentry = func.getEntryPoint()
        entry["function_found"] = True
        entry["function_entry"] = "0x%08X" % fentry.getOffset()
        entry["target_is_entry"] = bool(fentry.getOffset() == va)
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
                result["errors"].append("ref_proc %s: %s: %s" % (label, type(e).__name__, str(e)))
        entry["unique_callers"] = len(callers)
        entry["caller_list"] = sorted(callers.values(),
                                      key=lambda r: (-r["callsite_count"], r["caller_entry"]))
        result["measured"]["targets"][label] = entry
    except Exception as e:
        result["errors"].append("target %s: %s: %s" % (label, type(e).__name__, str(e)))
        result["measured"]["targets"][label] = entry

# decompilations for the selection step
try:
    di = DecompInterface()
    di.openProgram(currentProgram)
    for (label, va) in DECOMPILE:
        t = toAddr(va)
        func = getFunctionContaining(t)
        if func is None:
            result["measured"]["decompilations"][label] = {"va": "0x%08X" % va, "ok": False,
                                                           "error": "no function"}
            continue
        res = di.decompileFunction(func, 180, ConsoleTaskMonitor())
        if res.decompileCompleted():
            c = res.getDecompiledFunction().getC()
            result["measured"]["decompilations"][label] = {
                "va": "0x%08X" % va,
                "function_entry": "0x%08X" % func.getEntryPoint().getOffset(),
                "ok": True, "c_line_count": len(c.split("\n")), "c": c}
        else:
            result["measured"]["decompilations"][label] = {
                "va": "0x%08X" % va, "ok": False, "error": res.getErrorMessage()}
    di.dispose()
except Exception as e:
    result["errors"].append("decompiler: %s: %s" % (type(e).__name__, str(e)))

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C2 census written:", RESULT_PATH)
for (label, va) in TARGETS:
    t = result["measured"]["targets"].get(label, {})
    print("%s 0x%08X callsites=%s callers=%s" % (label, va, t.get("callsites"), t.get("unique_callers")))
print("errors:", result["errors"])
