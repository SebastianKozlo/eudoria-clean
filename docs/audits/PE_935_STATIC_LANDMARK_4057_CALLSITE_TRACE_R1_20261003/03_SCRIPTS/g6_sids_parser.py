# -*- coding: utf-8 -*-
# G6 SIDS PAYLOAD PARSER — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.
# Jython 2.7 (Ghidra 11.2.1). Existing fresh project LANDMARK4057 (sandbox copy).
#
# Contract primary question (semantic role of immediate 4057): the LAST
# unmeasured function on the 4057-consumption path — FUN_00821E70, the parser
# that fills the 0x1C string-table singleton's map from the sids.vfs record
# (called by FUN_00821FB0 after the VFS read). Measuring it identifies the
# map-key layout, which decides whether the composite key {section, 4057}
# corresponds to sids.vfs payload entry ids (the positive identification of
# 4057's semantic class) — bounded, directly on the measured path.
#
#   I01 FUN_00821E70 — sids payload -> map parser

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
OUT = SCRATCH + r"\g6_sids_parser.json"

TARGETS = [
    ("I01_sids_parser_00821e70", 0x00821E70),
]

TEMPLATE_MACHINERY = [0x0072F580, 0x0043A550, 0x0072FA30, 0x00730C90,
                      0x007CE1E0, 0x004D1430, 0x0072F8D0, 0x006C3F50, 0x008BD720]

result = {
    "run_id": "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003",
    "stage": "G6_sids_parser",
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
print("G6 written:", OUT)
print("errors:", result["errors"])
