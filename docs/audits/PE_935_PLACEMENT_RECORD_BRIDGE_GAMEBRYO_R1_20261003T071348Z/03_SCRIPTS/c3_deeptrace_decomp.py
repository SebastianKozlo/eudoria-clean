# C3 DEEP-TRACE DECOMPILATIONS - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# FAMILY-T selected (SELECTION.md). One Ghidra round; decompiles the trace functions.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C3_DECOMP.json

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C3_DECOMP.json"

TARGETS = [
    ("R01_reader_0072fa30", 0x0072FA30),      # templates.vfs record reader
    ("R02_mapfind_004d1430", 0x004D1430),      # RB-tree find helper (lookup helper)
    ("R03_lookup2x_006c2bb0", 0x006C2BB0),     # 2x lookup caller (model machinery)
    ("R04_emitter_006c3f50", 0x006C3F50),      # {0x66=MODEL,A} pair emitter
    ("R05_other_00567170", 0x00567170),       # OTHER-class lookup caller
    ("R06_other_005b5f90", 0x005B5F90),       # OTHER-class lookup caller
    ("R07_other_00733490", 0x00733490),       # OTHER-class lookup caller
    ("R08_other_00848ea0", 0x00848EA0),       # OTHER-class lookup caller (attr family)
    ("R09_other_006a3930", 0x006A3930),       # OTHER-class lookup caller
    ("R10_other_006baa20", 0x006BAA20),       # OTHER-class lookup caller
    ("R11_instcreator_006cb6f0", 0x006CB6F0), # model instance creator
    ("R12_namedinst_006cb020", 0x006CB020),   # named instance builder
    ("R13_pendingattach_006cb3c0", 0x006CB3C0),  # pending-attach processor
    ("R14_register_006f33a0", 0x006F33A0),    # named-instance registration
    ("R15_update_006cd850", 0x006CD850),      # calls instance creator + pending attach
    ("R16_attach_006cb4c0", 0x006CB4C0),     # calls pending attach
    ("R17_sceneroot_00933310", 0x00933310),  # scene root area (NetImmerseScene::Root)
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C3_deeptrace_decomp",
    "measured": {"decompilations": {}},
    "interpreted": {},
    "errors": [],
}

di = DecompInterface()
di.openProgram(currentProgram)
try:
    for (label, va) in TARGETS:
        t = toAddr(va)
        func = getFunctionContaining(t)
        if func is None:
            result["measured"]["decompilations"][label] = {
                "va": "0x%08X" % va, "ok": False, "error": "no function"}
            continue
        res = di.decompileFunction(func, 180, ConsoleTaskMonitor())
        entry_d = {"va": "0x%08X" % va,
                   "function_entry": "0x%08X" % func.getEntryPoint().getOffset(),
                   "function_name": func.getName(),
                   "body_size": int(func.getBody().getNumAddresses())}
        if res.decompileCompleted():
            c = res.getDecompiledFunction().getC()
            entry_d["ok"] = True
            entry_d["c_line_count"] = len(c.split("\n"))
            entry_d["c"] = c
        else:
            entry_d["ok"] = False
            entry_d["error"] = res.getErrorMessage()
        result["measured"]["decompilations"][label] = entry_d
finally:
    di.dispose()

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C3 written:", RESULT_PATH)
for (label, va) in TARGETS:
    d = result["measured"]["decompilations"].get(label, {})
    print("%s 0x%08X ok=%s lines=%s" % (label, va, d.get("ok"), d.get("c_line_count")))
print("errors:", result["errors"])
