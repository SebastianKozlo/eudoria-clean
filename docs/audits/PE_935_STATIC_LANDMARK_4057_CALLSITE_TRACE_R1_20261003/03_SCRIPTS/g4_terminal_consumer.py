# -*- coding: utf-8 -*-
# G4 TERMINAL CONSUMER + SINGLETON IDENTITY —
# PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.
# Jython 2.7 (Ghidra 11.2.1). Existing fresh project LANDMARK4057 (sandbox copy).
#
# Contract Phase 5 (mandatory falsifier), final step: measure the TERMINAL
# consumer of 4057 inside the anchored chain:
#   F01 FUN_00821760  singleton->FUN_00821760(0, id, &out) — the id->string
#                      resolver called by FUN_00821BB0 with 4057 as arg2
#   F02 FUN_008221C0   ctor of the 0x1C singleton object @0x00BA124C created
#                      by FUN_00414170 (singleton class identity evidence)
# Also records, for every function dumped across g1..g4, whether any direct
# callee belongs to the template machinery set (registry lookup FUN_0072F580,
# registry getter FUN_0043A550, reader FUN_0072FA30, parse FUN_00730C90,
# A-getter FUN_007CE1E0, mapfind FUN_004D1430, RB-insert FUN_0072F8D0) —
# the falsifier reach-check artifact.

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
OUT = SCRATCH + r"\g4_terminal_consumer.json"

TARGETS = [
    ("F01_id_to_string_00821760", 0x00821760),
    ("F02_singleton_ctor_008221c0", 0x008221C0),
]

TEMPLATE_MACHINERY = [0x0072F580, 0x0043A550, 0x0072FA30, 0x00730C90,
                      0x007CE1E0, 0x004D1430, 0x0072F8D0]

result = {
    "run_id": "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003",
    "stage": "G4_terminal_consumer",
    "measured": {"functions": {}},
    "interpreted": {"template_machinery_direct_callee_hits": {}},
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
        hits = []
        for i in ins:
            ii = listing.getInstructionAt(toAddr(int(i["addr"], 16)))
            if ii is None:
                continue
            if ii.getFlowType().isCall():
                for fl in ii.getFlows():
                    tva = fl.getOffset()
                    callees.append({"from": i["addr"], "target": "0x%08X" % tva})
                    if tva in TEMPLATE_MACHINERY:
                        hits.append({"from": i["addr"], "target": "0x%08X" % tva})
        d["callee_targets"] = callees
        d["template_machinery_direct_hits"] = hits
        M["functions"][label] = d
        print("%s %s size=%s listing=%s callers=%s machinery_hits=%s" % (
            label, d["entry"], d["size_bytes"], d["listing_count"], len(callers), hits))
finally:
    di.dispose()

with open(OUT, "w") as fjson:
    json.dump(result, fjson, indent=2)
print("G4 written:", OUT)
print("errors:", result["errors"])
