#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3 CURATE G1 — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Curates the LOCAL-ONLY Ghidra scratch dump (g1_callsite_dump.json, produced by
03_SCRIPTS/g1_dump_callsite.py in the fresh project LANDMARK4057 on the
sandbox EXE copy) into the repo package evidence files:
  01_RAW/G1_FUNCTION_DUMP.json    full function dump (metadata + anchor +
                                   callers + callees + refs + full listing +
                                   decompiled C)
  01_RAW/CALL_XREF_CENSUS.json     curated call/xref census (contract 01_RAW)
  01_RAW/G1_DECOMPILE_00599D30.c   plain-text decompilation (readable paging)
Also prints the anchor-neighborhood listing for immediate analysis.

Byte integrity: every listing byte pair is independently cross-checked
against the physical EXE by 03_SCRIPTS/s2_callsite_rawpin.py --crosscheck
(own PE mapper; result recorded in 01_RAW/RAW_BYTE_PINS.json).

Interpreter: python 3.12.10 (local Windows). Invoke:
  python 03_SCRIPTS/s3_curate_g1.py
"""

import json
import os

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
G1 = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\g1_callsite_dump.json"
ANCHOR = 0x0059AB12


def main():
    with open(G1, "r") as f:
        g1 = json.load(f)
    M = g1.get("measured", {})
    fn = M.get("function", {})
    os.makedirs(RAWDIR, exist_ok=True)

    # ---- G1_FUNCTION_DUMP.json (curated full dump)
    dump = {
        "run_id": RUN_ID,
        "stage": "G1_curated_function_dump",
        "source": {
            "ghidra": "11.2.1 PUBLIC (analyzeHeadless; fresh project LANDMARK4057)",
            "target": "sandbox copy of D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (SHA256 E7785430... pinned; hash-verified before import)",
            "postscript": "03_SCRIPTS/g1_dump_callsite.py (hash recorded in 03_SCRIPTS/SCRIPT_SHA256.csv)",
            "byte_crosscheck": "01_RAW/RAW_BYTE_PINS.json (s2 --crosscheck; own PE mapper vs physical EXE)",
        },
        "measured": M,
        "errors": g1.get("errors", []),
    }
    with open(os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json"), "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2)

    # ---- CALL_XREF_CENSUS.json (curated census)
    callers = M.get("callers", [])
    caller_fns = M.get("caller_functions", [])
    callees = M.get("callees", [])
    uniq_targets = set()
    indirect = 0
    for c in callees:
        for t in c.get("targets", []):
            if t.get("target") is None:
                indirect += 1
            else:
                uniq_targets.add(t["target"])
    census = {
        "run_id": RUN_ID,
        "stage": "S3_call_xref_census",
        "measured": {
            "function": {k: fn.get(k) for k in ("found", "name", "entry", "body_start",
                                                "body_end", "size_bytes", "calling_convention",
                                                "signature", "parameters", "listing_count")},
            "callers_isCall_refs": callers,
            "caller_functions": caller_fns,
            "entry_other_refs": M.get("entry_other_refs", []),
            "callees_call_sites": callees,
            "refs_to_anchor": M.get("refs_to_anchor", []),
            "callee_summary": {
                "call_sites": len(callees),
                "unique_direct_targets": len(uniq_targets),
                "unresolved_indirect_calls": indirect,
            },
        },
        "interpreted": {
            "FUNCTION_START": fn.get("entry"),
            "FUNCTION_END": fn.get("body_end"),
            "SIZE_BYTES": fn.get("size_bytes"),
            "CALLER_COUNT": len(callers),
            "CALLEE_CALL_SITE_COUNT": len(callees),
            "NOTE": "interpreted fields are mechanical summaries of measured refs; no semantic role assigned (contract Phase 3 forbids naming before dataflow)",
            "pin_provenance": {
                "xref_census": {
                    "MEASURED_QUANTITY": "call references to the function entry (isCall-filtered) and CALL instructions inside the body with their resolved targets",
                    "INDEPENDENT_SOURCE_OF_TRUTH": "Ghidra 11.2.1 reference analysis on the sandbox copy (imported EXE byte-identical to the pinned build); listing byte integrity independently cross-checked vs the physical EXE by s2 --crosscheck",
                    "WHY_NON_CIRCULAR": "census derives from code references only (isCall filter per the pe-ghidra-re skill rule); no name/number/structural matching is used to classify anything",
                    "FAILURE_CASE_DETECTED": "a missed call edge would appear as an undefined-region callsite (prior-run calibration: 18 defined + 7 undefined on a calibration target); indirect calls are counted as unresolved, never guessed"},
            },
        },
        "errors": g1.get("errors", []),
    }
    with open(os.path.join(RAWDIR, "CALL_XREF_CENSUS.json"), "w", encoding="utf-8") as f:
        json.dump(census, f, indent=2)

    # ---- plain-text decompile for analysis paging
    dec = fn.get("decompile_c") or ""
    with open(os.path.join(RAWDIR, "G1_DECOMPILE_00599D30.c"), "w", encoding="utf-8") as f:
        f.write("// decompiled FUN_00599D30 (Ghidra 11.2.1, fresh project, sandbox copy of the pinned EXE)\n")
        f.write("// byte integrity: 01_RAW/RAW_BYTE_PINS.json g1_byte_crosscheck; listing: 01_RAW/G1_FUNCTION_DUMP.json\n")
        f.write(dec)

    # ---- immediate analysis prints: anchor neighborhood + calls near anchor
    print("function:", fn.get("entry"), "-", fn.get("body_end"), "size", fn.get("size_bytes"),
          "cc", fn.get("calling_convention"), "params", [(p.get("name"), p.get("type")) for p in fn.get("parameters", [])])
    print("signature:", fn.get("signature"))
    print("callers:", callers)
    print("caller_functions:", caller_fns)
    listing = fn.get("listing", [])
    print("=== listing window anchor-0x30 .. anchor+0x40 ===")
    for ins in listing:
        a = int(ins["addr"], 16)
        if ANCHOR - 0x30 <= a <= ANCHOR + 0x40:
            print("%s  %-20s  %s" % (ins["addr"], ins["bytes"], ins["text"]))
    print("=== CALL sites within anchor-0x100 .. anchor+0x100 ===")
    for c in M.get("callees", []):
        a = int(c["call_va"], 16)
        if ANCHOR - 0x100 <= a <= ANCHOR + 0x100:
            print("%s  %-24s %s -> %s" % (c["call_va"], c["bytes"], c["text"], c["targets"]))
    print("=== refs_to_anchor:", M.get("refs_to_anchor"))
    print("=== callee summary:", census["measured"]["callee_summary"])


if __name__ == "__main__":
    main()
