# -*- coding: utf-8 -*-
# G1 CONTAINING-FUNCTION DUMP — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.
# Jython 2.7 (Ghidra 11.2.1). Fresh project LANDMARK4057 on a sandbox copy of
# Entropia.exe (hash-verified before import; original untouched).
#
# Contract Phase 3 (§10): full boundary of the function containing VA
# 0x0059AB12 — FUNCTION_START / FUNCTION_END / SIZE / CALLERS / CALLEES /
# calling-convention evidence / this-pointer evidence (decompile).
# No semantic function name is assigned before dataflow (contract §10).
#
# Output (LOCAL-ONLY scratch, then curated by pure-Python scripts into the
# package 01_RAW/): g1_callsite_dump.json
#   measured.anchor        instruction at 0x0059AB12 (bytes + text)
#   measured.function      entry/body/size/ABI/signature/parameters
#   measured.listing       every instruction of the body (addr/bytes/text)
#   measured.decompile     decompiled C (thiscall evidence; parameter roles)
#   measured.callers       call references to the entry (isCall-filtered)
#   measured.callees       CALL instructions in the body + resolved targets
#   measured.refs_to_anchor references to 0x0059AB12 itself
# All interpreted fields are added OUTSIDE Ghidra by the analysis layer; this
# script only measures.

import json

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
OUT = SCRATCH + r"\g1_callsite_dump.json"
ANCHOR = 0x0059AB12

result = {
    "run_id": "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003",
    "stage": "G1_containing_function",
    "measured": {},
    "interpreted": {},
    "errors": [],
}
M = result["measured"]

target = toAddr(ANCHOR)
listing = currentProgram.getListing()
fm = currentProgram.getFunctionManager()

# --- instruction at the anchor (Ghidra view; physical bytes cross-checked
# separately by s2 --crosscheck against the EXE via the own PE mapper)
ins_at = listing.getInstructionAt(target)
if ins_at is None:
    ins_at = listing.getInstructionContaining(target)
if ins_at is not None:
    M["anchor"] = {
        "va": "0x%08X" % ins_at.getAddress().getOffset(),
        "bytes": " ".join("%02X" % (b & 0xFF) for b in ins_at.getBytes()),
        "text": ins_at.toString(),
    }
else:
    M["anchor"] = {"va": "0x%08X" % ANCHOR, "bytes": None, "text": None,
                   "note": "no instruction defined at/containing anchor"}
    result["errors"].append("no instruction at anchor 0x0059AB12")

f = fm.getFunctionContaining(target)
if f is None:
    result["errors"].append("no function containing 0x0059AB12 in auto-analysis")
    # bounded fallback: diagnostic neighborhood dump (still no semantic claims)
    wstart = toAddr(ANCHOR - 0x200)
    wend = toAddr(ANCHOR + 0x200)
    ins = []
    it = listing.getInstructions(wstart, True)
    while it.hasNext():
        i = it.next()
        if i.getAddress().getOffset() > (ANCHOR + 0x200):
            break
        ins.append({"addr": "0x%08X" % i.getAddress().getOffset(),
                    "bytes": " ".join("%02X" % b for b in i.getBytes()),
                    "text": i.toString()})
    M["unowned_window"] = {"start": "0x%08X" % (ANCHOR - 0x200),
                           "end": "0x%08X" % (ANCHOR + 0x200), "instructions": ins}
    fb = fm.getFunctionBefore(target)
    fa = fm.getFunctionAfter(target)
    M["unowned_neighbors"] = {
        "function_before": (fb.getName() + "@0x%08X" % fb.getEntryPoint().getOffset()) if fb else None,
        "function_after": (fa.getName() + "@0x%08X" % fa.getEntryPoint().getOffset()) if fa else None,
    }
else:
    entry = f.getEntryPoint()
    body = f.getBody()
    bstart = body.getMinAddress().getOffset()
    bend = body.getMaxAddress().getOffset()
    params = []
    try:
        for p in f.getParameters():
            params.append({"name": p.getName(),
                           "type": str(p.getDataType()),
                           "storage": str(p.getVariableStorage())})
    except Exception as e:
        result["errors"].append("params: %s" % str(e))
    fd = {
        "found": True,
        "name": f.getName(),
        "entry": "0x%08X" % entry.getOffset(),
        "body_start": "0x%08X" % bstart,
        "body_end": "0x%08X" % bend,
        "size_bytes": int(body.getNumAddresses()),
        "calling_convention": f.getCallingConventionName(),
        "signature": str(f.getSignature(True)),
        "parameters": params,
    }
    M["function"] = fd

    # --- full listing of the body (byte-anchored: every instruction's raw bytes)
    ins = []
    it = listing.getInstructions(body, True)
    while it.hasNext():
        i = it.next()
        ins.append({"addr": "0x%08X" % i.getAddress().getOffset(),
                    "bytes": " ".join("%02X" % (b & 0xFF) for b in i.getBytes()),
                    "text": i.toString()})
    fd["listing"] = ins
    fd["listing_count"] = len(ins)

    # --- decompile (ABI / this-pointer / parameter-role evidence)
    di = DecompInterface()
    di.openProgram(currentProgram)
    try:
        res_d = di.decompileFunction(f, 180, ConsoleTaskMonitor())
        if res_d.decompileCompleted():
            fd["decompile_ok"] = True
            fd["decompile_c"] = res_d.getDecompiledFunction().getC()
        else:
            fd["decompile_ok"] = False
            fd["decompile_error"] = res_d.getErrorMessage()
    finally:
        di.dispose()

    # --- callers: references to the entry, isCall-filtered (skill rule)
    callers = []
    other_refs = []
    for r in getReferencesTo(entry):
        rt = r.getReferenceType()
        if rt.isCall():
            cfrom = r.getFromAddress()
            cf = fm.getFunctionContaining(cfrom)
            callers.append({"from": "0x%08X" % cfrom.getOffset(),
                            "caller_function": cf.getName() if cf else None,
                            "caller_entry": ("0x%08X" % cf.getEntryPoint().getOffset()) if cf else None,
                            "op_type": str(rt)})
        else:
            other_refs.append({"from": "0x%08X" % r.getFromAddress().getOffset(),
                               "op_type": str(rt)})
    M["callers"] = callers
    M["entry_other_refs"] = other_refs
    try:
        cfset = f.getCallingFunctions(monitor)
        M["caller_functions"] = [{"name": x.getName(),
                                   "entry": "0x%08X" % x.getEntryPoint().getOffset()} for x in cfset]
    except Exception as e:
        result["errors"].append("getCallingFunctions: %s" % str(e))

    # --- callees: CALL instructions inside the body (direct flows)
    callees = []
    for i in ins:
        ii = listing.getInstructionAt(toAddr(int(i["addr"], 16)))
        if ii is None:
            continue
        if ii.getFlowType().isCall():
            flows = ii.getFlows()
            tgts = []
            for fl in flows:
                tf = fm.getFunctionContaining(fl)
                tgts.append({"target": "0x%08X" % fl.getOffset(),
                             "target_name": tf.getName() if tf else None})
            if not tgts:
                tgts.append({"target": None,
                             "note": "indirect/unresolved call target"})
            callees.append({"call_va": i["addr"], "bytes": i["bytes"],
                             "text": i["text"], "targets": tgts})
    M["callees"] = callees

    # --- references to the anchor itself (mid-body refs, if any)
    ra = []
    for r in getReferencesTo(target):
        ra.append({"from": "0x%08X" % r.getFromAddress().getOffset(),
                    "op_type": str(r.getReferenceType())})
    M["refs_to_anchor"] = ra

with open(OUT, "w") as fjson:
    json.dump(result, fjson, indent=2)
print("G1 written:", OUT)
fd = M.get("function", {})
print("function found:", fd.get("found"), "entry:", fd.get("entry"),
      "body:", fd.get("body_start"), "-", fd.get("body_end"),
      "size:", fd.get("size_bytes"), "cc:", fd.get("calling_convention"))
print("listing_count:", fd.get("listing_count"), "callers:", len(M.get("callers", [])),
      "callees:", len(M.get("callees", [])))
print("anchor:", M.get("anchor"))
print("errors:", result["errors"])
