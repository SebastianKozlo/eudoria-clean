# C7 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Round 7: vector parsers (template lists) + attach internals (Gamebryo NiNode family)
# + emitter callers. Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C7_LISTS_AND_ATTACH.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C7_LISTS_AND_ATTACH.json"

DECOMP_TARGETS = [
    ("Z01_list1_init_00730b70", 0x00730B70),
    ("Z02_list2_init_00730970", 0x00730970),
    ("Z03_attach_impl_d60_00779d60", 0x00779D60),
    ("Z04_attach_impl_e20_00779e20", 0x00779E20),
    ("Z05_attach_impl_f80_00779f80", 0x00779F80),
    ("Z06_attach_impl_c80_00779c80", 0x00779C80),
    ("Z07_attach_impl_e70_00779e70", 0x00779E70),
    ("Z08_emitter_caller_006c3fe0", 0x006C3FE0),
    ("Z09_emitter_caller_006c4020", 0x006C4020),
    ("Z10_reader_per_record_00971ad0", 0x00971AD0),
    ("Z11_deserB_004c47f0", 0x004C47F0),
    ("Z12_movable_ctor_00703b80", 0x00703B80),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C7_lists_and_attach",
    "measured": {"decompilations": {}},
    "interpreted": {},
    "errors": [],
}

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
print("C7 written:", RESULT_PATH)
for (label, va) in DECOMP_TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
