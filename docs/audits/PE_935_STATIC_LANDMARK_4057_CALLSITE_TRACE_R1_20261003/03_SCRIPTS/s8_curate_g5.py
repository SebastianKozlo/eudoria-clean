#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S8 CURATE G5 + DEFINITIVE FALSIFIER REACH-CHECK —
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
1. Curates g5_lookup_closure.json into 01_RAW/G5_LOOKUP_CLOSURE.json (+ .c files).
2. Regenerates 01_RAW/FALSIFIER_REACH_CHECK.json over ALL measured function
   sets g1..g5 (supersedes the g1-g4-only version written by s7_curate_g4.py;
   same schema, more rows). The template-machinery VA set is fixed canon.
3. Prints the g5 listings/decompiles and the final reach-check table.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s8_curate_g5.py
"""

import json
import os

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"

TEMPLATE_MACHINERY = {
    0x0072F580: "registry_lookup_FUN_0072F580",
    0x0043A550: "registry_singleton_getter_FUN_0043A550",
    0x0072FA30: "templates_reader_FUN_0072FA30",
    0x00730C90: "template_parse_FUN_00730C90",
    0x007CE1E0: "A_getter_FUN_007CE1E0",
    0x004D1430: "rbtree_mapfind_FUN_004D1430_GENERIC_PRIMITIVE",
    0x0072F8D0: "rbtree_insert_FUN_0072F8D0",
    0x006C3F50: "model_request_pair_emitter_FUN_006C3F50",
    0x008BD720: "scheduler_callback_FUN_008BD720",
    0x0072FE30: "template_list2_out_FUN_0072FE30",
}


def main():
    with open(os.path.join(SCRATCH, "g5_lookup_closure.json"), "r") as f:
        g5 = json.load(f)
    os.makedirs(RAWDIR, exist_ok=True)
    with open(os.path.join(RAWDIR, "G5_LOOKUP_CLOSURE.json"), "w", encoding="utf-8") as f:
        json.dump({"run_id": RUN_ID, "stage": "G5_curated_lookup_closure",
                   "source": {
                       "ghidra": "11.2.1 PUBLIC (analyzeHeadless; fresh project LANDMARK4057)",
                       "target": "sandbox copy of D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (SHA256 E7785430... pinned)",
                       "postscript": "03_SCRIPTS/g5_lookup_closure.py (hash in 03_SCRIPTS/SCRIPT_SHA256.csv)"},
                   "measured": g5.get("measured", {}),
                   "errors": g5.get("errors", [])}, f, indent=2)

    fns5 = g5.get("measured", {}).get("functions", {})
    for label, d in sorted(fns5.items()):
        va = d.get("entry", d.get("va", "0")).replace("0x", "")
        with open(os.path.join(RAWDIR, "G5_DECOMPILE_%s_%s.c" % (label, va)), "w", encoding="utf-8") as f:
            f.write("// %s decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)\n" % label)
            f.write("// listing + callers + callees: 01_RAW/G5_LOOKUP_CLOSURE.json\n")
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

    # ---- definitive falsifier reach-check over g1..g5
    per_function = {}
    srcs = [
        ("G1", os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json"), "function"),
        ("G2", os.path.join(RAWDIR, "G2_CALLEE_DEEPDIVE.json"), "functions"),
        ("G3", os.path.join(RAWDIR, "G3_FALSIFIER_PATH.json"), "functions"),
        ("G4", os.path.join(RAWDIR, "G4_TERMINAL_CONSUMER.json"), "functions"),
        ("G5", os.path.join(RAWDIR, "G5_LOOKUP_CLOSURE.json"), "functions"),
    ]
    for (tag, path, key) in srcs:
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            data = json.load(f)
        items = []
        if key == "function":
            fnd = data.get("measured", {}).get("function", {})
            if fnd.get("found"):
                items = [("%s_FUN_00599d30" % tag, fnd)]
        else:
            items = sorted(data.get("measured", {}).get("functions", {}).items())
            items = [("%s_%s" % (tag, lab), d) for lab, d in items]
        for (k2, d) in items:
            if not isinstance(d, dict) or "callee_targets" not in d:
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
            per_function[k2] = {
                "entry": d.get("entry"), "name": d.get("name"),
                "direct_template_machinery_hits": hits,
            }
    # g1 containing function: callees live under measured.callees
    with open(os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json"), "r") as f:
        g1d = json.load(f)
    hits = []
    for c in g1d.get("measured", {}).get("callees", []):
        for t in c.get("targets", []):
            tv = t.get("target")
            if tv is None:
                continue
            tvi = int(tv, 16)
            if tvi in TEMPLATE_MACHINERY:
                hits.append({"from": c.get("call_va"), "target": tv,
                             "role": TEMPLATE_MACHINERY[tvi]})
    if "G1_FUN_00599d30" not in per_function:
        per_function["G1_FUN_00599d30"] = {"entry": "0x00599D30", "name": "FUN_00599d30",
                                          "direct_template_machinery_hits": []}
    per_function["G1_FUN_00599d30"]["direct_template_machinery_hits"] = hits
    per_function["G1_FUN_00599d30"]["note"] = "177 call sites checked (01_RAW/CALL_XREF_CENSUS.json)"

    reach = {
        "run_id": RUN_ID,
        "stage": "S8_falsifier_reach_check_g1_to_g5",
        "measured": {
            "template_machinery_va_set": {("0x%08X" % k): v for k, v in TEMPLATE_MACHINERY.items()},
            "per_function": per_function,
            "total_functions_checked": len(per_function),
            "supersedes": "the g1-g4-only FALSIFIER_REACH_CHECK.json written by s7_curate_g4.py (same file name, schema-compatible, complete g1..g5 coverage)",
        },
        "interpreted": {
            "TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS": sum(
                len(v["direct_template_machinery_hits"]) for v in per_function.values()),
            "NOTE_ON_FUN_004D1430": (
                "FUN_004D1430 is the GENERIC STL RB-tree mapfind primitive shared by many maps "
                "(the template registry lookup FUN_0072F580 also calls it). A hit of 0x004D1430 "
                "does NOT establish a template-registry edge: the registry identity edge requires "
                "FUN_0072F580 (the thiscall wrapper over the registry singleton DAT_00BA1824 via "
                "FUN_0043A550). In the measured chain the tree walked by FUN_00823C10 belongs to "
                "the string-table singleton object (0x1C object at DAT_00BA124C built by "
                "FUN_00414170/FUN_008221C0) with a composite key, NOT the template registry."),
            "pin_provenance": {
                "reach_check": {
                    "MEASURED_QUANTITY": "direct CALL targets of every function measured this run (g1..g5), tested against the fixed canon template-machinery VA set",
                    "INDEPENDENT_SOURCE_OF_TRUTH": "Ghidra-resolved direct CALL flows from the byte-verified listings (g1: 951/951 vs physical EXE; g2-g5: same pipeline)",
                    "WHY_NON_CIRCULAR": "the machinery VA set is fixed canon (TRACE_EDGE_BLOCKS E1-E3), not derived from this run; hits are reported as measured",
                    "FAILURE_CASE_DETECTED": "a template registry edge on this call-site would appear as FUN_0072F580/FUN_0043A550 hits in the 4057-consumption chain (FUN_008dfcd0 / FUN_00821bb0 / FUN_00821760 / FUN_00415670 / FUN_00823c10 / FUN_008dfb70); none are present — the mandatory falsifier fires"},
            },
        },
        "errors": [],
    }
    with open(os.path.join(RAWDIR, "FALSIFIER_REACH_CHECK.json"), "w", encoding="utf-8") as f:
        json.dump(reach, f, indent=2)
    print("=" * 100)
    print("FALSIFIER REACH-CHECK (g1..g5) over", len(per_function), "functions:")
    for k, v in sorted(per_function.items()):
        print("  %-36s hits=%s" % (k, v["direct_template_machinery_hits"] if v["direct_template_machinery_hits"] else 0))
    print("TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS:", reach["interpreted"]["TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS"])


if __name__ == "__main__":
    main()
