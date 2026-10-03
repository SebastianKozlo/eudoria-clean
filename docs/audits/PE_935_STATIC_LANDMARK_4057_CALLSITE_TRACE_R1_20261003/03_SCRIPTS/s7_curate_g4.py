#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S7 CURATE G4 + FALSIFIER REACH-CHECK —
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
1. Curates g4_terminal_consumer.json into 01_RAW/G4_TERMINAL_CONSUMER.json
   (+ per-target plain-text decompiles).
2. Falsifier reach-check over ALL functions measured across g1/g2/g3/g4:
   for every measured function, check its direct CALL targets against the
   template machinery set (registry lookup FUN_0072F580, registry getter
   FUN_0043A550, reader FUN_0072FA30, parse FUN_00730C90, A-getter
   FUN_007CE1E0, mapfind FUN_004D1430, RB-insert FUN_0072F8D0) and the
   model-request pair emitter (FUN_006C3F50) / scheduler callback
   (FUN_008BD720). Writes 01_RAW/FALSIFIER_REACH_CHECK.json and prints it.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s7_curate_g4.py
"""

import json
import os

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"

TEMPLATE_MACHINERY = {
    0x0072F580: "registry_lookup",
    0x0043A550: "registry_singleton_getter",
    0x0072FA30: "templates_reader",
    0x00730C90: "template_parse",
    0x007CE1E0: "A_getter",
    0x004D1430: "rbtree_mapfind",
    0x0072F8D0: "rbtree_insert",
    0x006C3F50: "model_request_pair_emitter",
    0x008BD720: "scheduler_callback",
    0x0072FE30: "template_list2_out",
}


def main():
    with open(os.path.join(SCRATCH, "g4_terminal_consumer.json"), "r") as f:
        g4 = json.load(f)
    os.makedirs(RAWDIR, exist_ok=True)
    with open(os.path.join(RAWDIR, "G4_TERMINAL_CONSUMER.json"), "w", encoding="utf-8") as f:
        json.dump({"run_id": RUN_ID, "stage": "G4_curated_terminal_consumer",
                   "source": {
                       "ghidra": "11.2.1 PUBLIC (analyzeHeadless; fresh project LANDMARK4057)",
                       "target": "sandbox copy of D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (SHA256 E7785430... pinned)",
                       "postscript": "03_SCRIPTS/g4_terminal_consumer.py (hash in 03_SCRIPTS/SCRIPT_SHA256.csv)"},
                   "measured": g4.get("measured", {}),
                   "interpreted": g4.get("interpreted", {}),
                   "errors": g4.get("errors", [])}, f, indent=2)

    fns4 = g4.get("measured", {}).get("functions", {})
    for label, d in sorted(fns4.items()):
        va = d.get("entry", d.get("va", "0")).replace("0x", "")
        with open(os.path.join(RAWDIR, "G4_DECOMPILE_%s_%s.c" % (label, va)), "w", encoding="utf-8") as f:
            f.write("// %s decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)\n" % label)
            f.write("// listing + callers + callees: 01_RAW/G4_TERMINAL_CONSUMER.json\n")
            f.write((d.get("decompile_c") or "") if d.get("decompile_ok") else
                    "// decompile failed: %s\n" % d.get("decompile_error"))
        print("=" * 100)
        print("### %s @%s size=%s cc=%s sig=%s" % (label, d.get("entry"), d.get("size_bytes"),
                                                 d.get("calling_convention"), d.get("signature")))
        print("params:", d.get("parameters"))
        print("callers_count:", d.get("caller_call_sites_count"))
        print("template_machinery_direct_hits:", d.get("template_machinery_direct_hits"))
        print("--- listing ---")
        for i in d.get("listing", []):
            print("%s  %-24s %s" % (i["addr"], i["bytes"], i["text"]))
        if d.get("decompile_ok"):
            print("--- decompile ---")
            print(d.get("decompile_c"))
        print()

    # ---- falsifier reach-check over ALL measured functions (g1/g2/g3/g4)
    per_function = {}
    srcs = [
        ("g1", os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json")),
        ("g2", os.path.join(RAWDIR, "G2_CALLEE_DEEPDIVE.json")),
        ("g3", os.path.join(RAWDIR, "G3_FALSIFIER_PATH.json")),
        ("g4", os.path.join(RAWDIR, "G4_TERMINAL_CONSUMER.json")),
    ]
    for (tag, path) in srcs:
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            data = json.load(f)
        if tag == "g1":
            fnd = data.get("measured", {}).get("function", {})
            items = [("G1_FUN_00599d30", fnd)] if fnd.get("found") else []
            items += [("G1_%s" % d.get("va"), d) for d in [data["measured"].get("function", {})]]
        else:
            items = sorted((("G%d_%s" % (2 if tag == "g2" else 3 if tag == "g3" else 4, lab), d)
                            for lab, d in data.get("measured", {}).get("functions", {}).items()))
        for (key, d) in items:
            if not isinstance(d, dict) or "callee_targets" not in d:
                # g1 function dump keeps callees under measured.callees (call sites)
                continue
            hits = []
            for c in d.get("callee_targets", []):
                tv = c.get("target")
                if tv is None:
                    continue
                tvi = int(tv, 16)
                if tvi in TEMPLATE_MACHINERY:
                    hits.append({"from": c.get("from"), "target": tv,
                                 "role": TEMPLATE_MACHINERY[tvi]})
            per_function[key] = {
                "entry": d.get("entry"), "name": d.get("name"),
                "direct_template_machinery_hits": hits,
            }
    # g1 special: the containing function's callees live in measured.callees
    with open(os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json"), "r") as f:
        g1d = json.load(f)
    g1c = g1d.get("measured", {}).get("callees", [])
    hits = []
    for c in g1c:
        for t in c.get("targets", []):
            tv = t.get("target")
            if tv is None:
                continue
            tvi = int(tv, 16)
            if tvi in TEMPLATE_MACHINERY:
                hits.append({"from": c.get("call_va"), "target": tv,
                             "role": TEMPLATE_MACHINERY[tvi]})
    per_function["G1_FUN_00599d30"] = {
        "entry": "0x00599D30", "name": "FUN_00599d30",
        "direct_template_machinery_hits": hits,
        "note": "177 call sites checked (01_RAW/CALL_XREF_CENSUS.json)"}

    reach = {
        "run_id": RUN_ID,
        "stage": "S7_falsifier_reach_check",
        "measured": {
            "template_machinery_va_set": {("0x%08X" % k): v for k, v in TEMPLATE_MACHINERY.items()},
            "per_function": per_function,
            "total_functions_checked": len(per_function),
        },
        "interpreted": {
            "TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS": sum(
                len(v["direct_template_machinery_hits"]) for v in per_function.values()),
            "pin_provenance": {
                "reach_check": {
                    "MEASURED_QUANTITY": "direct CALL targets of every function measured this run, tested against the template machinery VA set (canon: TRACE_EDGE_BLOCKS E1-E3 chain)",
                    "INDEPENDENT_SOURCE_OF_TRUTH": "the callee lists are Ghidra-resolved direct CALL flows from the byte-verified listings (g1: 951/951 byte-verified; g2-g4: same pipeline)",
                    "WHY_NON_CIRCULAR": "the machinery VA set is fixed canon (registry lookup 0x0072F580 etc.), not derived from this run's search; a hit would be reported as measured, not inferred",
                    "FAILURE_CASE_DETECTED": "if 4057's chain reached the registry lookup, FUN_008dfcd0/FUN_00821bb0/FUN_00821760 would show 0x0072F580/0x0043A550 as direct callees — none found would falsify the template-id hypothesis for this call-site"},
            },
        },
        "errors": [],
    }
    with open(os.path.join(RAWDIR, "FALSIFIER_REACH_CHECK.json"), "w", encoding="utf-8") as f:
        json.dump(reach, f, indent=2)
    print("=" * 100)
    print("FALSIFIER REACH-CHECK over", len(per_function), "functions:")
    for k, v in sorted(per_function.items()):
        print("  %-34s hits=%d" % (k, len(v["direct_template_machinery_hits"])))
    print("TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS:",
          reach["interpreted"]["TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS"])


if __name__ == "__main__":
    main()
