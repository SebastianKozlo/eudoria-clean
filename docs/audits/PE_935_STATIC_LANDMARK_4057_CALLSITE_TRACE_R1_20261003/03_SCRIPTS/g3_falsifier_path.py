# -*- coding: utf-8 -*-
# G3 FALSIFIER-PATH DEEP-DIVE — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.
# Jython 2.7 (Ghidra 11.2.1). Existing fresh project LANDMARK4057 (sandbox copy).
#
# Contract Phase 5 (mandatory falsifier): measure the functions that directly
# consume the 4057 dataflow inside FUN_008DFCD0 (and the 886 sibling), plus the
# single caller of the containing function — all directly dependent on the
# anchored call-site (bounded; within NEW_PCG_FUNCTIONS_DETAILED_MAX):
#   E01 FUN_00414170  first consumer of 4057 inside FUN_008DFCD0 (string local + id + 12B struct)
#   E02 FUN_00821BB0  called on FUN_00414170's return; result stored on the object
#   E03 FUN_008DFB70  the [ESP+0xC8]-object method receiving the result (4057 path)
#   E04 FUN_008F01C0  the corresponding store method on the 886 path (mechanical only)
#   E05 FUN_0059BE70  the sole caller of FUN_00599D30 (containing-function context)
# Each: full byte-anchored listing + decompile + callers(callee counts) + callee
# targets. NO semantic naming (contract §10/§23).

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
OUT = SCRATCH + r"\g3_falsifier_path.json"

TARGETS = [
    ("E01_id_consumer_00414170", 0x00414170),
    ("E02_on_ret_00821bb0", 0x00821BB0),
    ("E03_store_008dfb70", 0x008DFB70),
    ("E04_store886_008f01c0", 0x008F01C0),
    ("E05_caller_0059be70", 0x0059BE70),
]

result = {
    "run_id": "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003",
    "stage": "G3_falsifier_path",
    "measured": {"functions": {}},
    "interpreted": {},
    "errors": [],
}
M = result["measured"]
listing = currentProgram.getListing()
fm = currentProgram.getFunctionManager()
di = DecompInterface()
di.openProgram(currentProgram)

try:
    for (label, va) in TARGETS:
        entry = toAddr(va)
        f = fm.getFunctionAt(entry)
        if f is None:
            f = fm.getFunctionContaining(entry)
        if f is None:
            M["functions"][label] = {"va": "0x%08X" % va, "found": False}
            result["errors"].append("%s: no function at 0x%08X" % (label, va))
            continue
        body = f.getBody()
        d = {
            "found": True, "va": "0x%08X" % va, "name": f.getName(),
            "entry": "0x%08X" % f.getEntryPoint().getOffset(),
            "body_start": "0x%08X" % body.getMinAddress().getOffset(),
            "body_end": "0x%08X" % body.getMaxAddress().getOffset(),
            "size_bytes": int(body.getNumAddresses()),
            "calling_convention": f.getCallingConventionName(),
            "signature": str(f.getSignature(True)),
            "parameters": [{"name": p.getName(), "type": str(p.getDataType()),
                           "storage": str(p.getVariableStorage())} for p in f.getParameters()],
        }
        ins = []
        it = listing.getInstructions(body, True)
        while it.hasNext():
            i = it.next()
            ins.append({"addr": "0x%08X" % i.getAddress().getOffset(),
                        "bytes": " ".join("%02X" % (b & 0xFF) for b in i.getBytes()),
                        "text": i.toString()})
        d["listing"] = ins
        d["listing_count"] = len(ins)
        res_d = di.decompileFunction(f, 180, ConsoleTaskMonitor())
        if res_d.decompileCompleted():
            d["decompile_ok"] = True
            d["decompile_c"] = res_d.getDecompiledFunction().getC()
        else:
            d["decompile_ok"] = False
            d["decompile_error"] = res_d.getErrorMessage()
        callers = []
        for r in getReferencesTo(f.getEntryPoint()):
            if r.getReferenceType().isCall():
                callers.append("0x%08X" % r.getFromAddress().getOffset())
        d["caller_call_sites_count"] = len(callers)
        d["caller_call_sites_first60"] = callers[:60]
        callees = []
        for i in ins:
            ii = listing.getInstructionAt(toAddr(int(i["addr"], 16)))
            if ii is None:
                continue
            if ii.getFlowType().isCall():
                for fl in ii.getFlows():
                    callees.append({"from": i["addr"], "target": "0x%08X" % fl.getOffset()})
        d["callee_targets"] = callees
        M["functions"][label] = d
        print("%s %s size=%s listing=%s callers=%s" % (label, d["entry"], d["size_bytes"],
                                                       d["listing_count"], len(callers)))
finally:
    di.dispose()

with open(OUT, "w") as fjson:
    json.dump(result, fjson, indent=2)
print("G3 written:", OUT)
print("errors:", result["errors"])
