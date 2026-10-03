# -*- coding: utf-8 -*-
# G2 CALLEE DEEP-DIVE — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.
# Jython 2.7 (Ghidra 11.2.1). Runs on the existing fresh project LANDMARK4057
# (sandbox EXE copy; original untouched; listing bytes cross-checked vs the
# physical EXE by s2 --crosscheck).
#
# Contract Phase 4/5 (§11/§12): deep-dive of the functions DIRECTLY dependent
# on the call-site sequence at 0x0059AB12 (bounded; NEW_PCG_FUNCTIONS_DETAILED
# stays within the preregistered limit):
#   D01 FUN_008DFCD0  PRIMARY consumer of PUSH 4057 (thiscall, this=[ESP+0xC8])
#   D02 FUN_008F0780  consumer of PUSH 0x376 (886) in the same sequence
#   D03 FUN_008E7B80  producer of EAX used as this for the 886 call
#   D04 FUN_008DF3F0  immediately-preceding ctor call ([ESP+0xD0])
#   D05 FUN_008DF310  ctor candidate called earlier in the same local cluster
# For each: entry/body/size/ABI signature/parameters, full byte-anchored
# listing, decompiled C, callers (isCall-filtered refs, count + up to 60
# listed), callees (CALL targets). No semantic naming (contract §10).

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
OUT = SCRATCH + r"\g2_callee_deepdive.json"

TARGETS = [
    ("D01_consumer_008dfcd0", 0x008DFCD0),
    ("D02_consumer886_008f0780", 0x008F0780),
    ("D03_eax_producer_008e7b80", 0x008E7B80),
    ("D04_ctor_008df3f0", 0x008DF3F0),
    ("D05_ctor_008df310", 0x008DF310),
]

result = {
    "run_id": "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003",
    "stage": "G2_callee_deepdive",
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
            "found": True,
            "va": "0x%08X" % va,
            "name": f.getName(),
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
        # callers (isCall-filtered)
        callers = []
        for r in getReferencesTo(f.getEntryPoint()):
            if r.getReferenceType().isCall():
                callers.append("0x%08X" % r.getFromAddress().getOffset())
        d["caller_call_sites_count"] = len(callers)
        d["caller_call_sites_first60"] = callers[:60]
        # callees (direct call targets)
        callees = []
        for i in ins:
            ii = listing.getInstructionAt(toAddr(int(i["addr"], 16)))
            if ii is None:
                continue
            if ii.getFlowType().isCall():
                for fl in ii.getFlows():
                    callees.append({"from": i["addr"], "target": "0x%08X" % fl.getOffset()})
        d["callee_targets"] = callees
        # vtable stores inside the body (ctor evidence; RTTI walk is done outside)
        d["vtable_store_imms"] = []
        for i in ins:
            if "MOV dword ptr [E" in i["text"] and "0x00a" in i["text"].lower():
                d["vtable_store_imms"].append({"addr": i["addr"], "text": i["text"],
                                                "bytes": i["bytes"]})
        M["functions"][label] = d
        print("%s %s size=%s listing=%s callers=%s" % (label, d["entry"], d["size_bytes"],
                                                       d["listing_count"], len(callers)))
finally:
    di.dispose()

with open(OUT, "w") as fjson:
    json.dump(result, fjson, indent=2)
print("G2 written:", OUT)
print("errors:", result["errors"])
