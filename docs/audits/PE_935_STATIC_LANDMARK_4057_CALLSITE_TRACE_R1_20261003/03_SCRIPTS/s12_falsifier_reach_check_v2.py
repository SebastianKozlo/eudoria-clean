#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S12 FALSIFIER REACH-CHECK V2 (R1 AMEND) -
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Bounded R1 repair-round generator (findings F-P2-1 + F-P3-5).
NO new science: reads ONLY the curated 01_RAW JSON artifacts committed by the
original run (no Ghidra, no scratch, no binary access).

1. Regenerates 01_RAW/FALSIFIER_REACH_CHECK.json (schema-compatible with the
   s7/s8 lineage) over ALL 18 measured functions (g1..g6), recording the single
   generic-machinery hit - the SHARED GENERIC mapfind FUN_004D1430 called at
   0x00823C57 inside FUN_00823C10 (string-table manager map @[mgr+4], singleton
   DAT_00BA12F4) - classified NOT a template-registry edge. Totals are
   row-consistent by construction: 18 functions checked; 1 generic-machinery
   hit; 0 template-registry edges.
2. Regenerates 03_SCRIPTS/SCRIPT_SHA256.csv: UTF-8 WITHOUT BOM, no blank
   lines, single trailing newline, hashes recomputed AFTER all final script
   edits (now includes the two scripts added by this R1 round: s12 + s13).

Supersedes: the s7_curate_g4.py-written 13-function artifact (stage S7; the
only version that actually shipped in the original package) and the
never-landed s8_curate_g5.py regeneration. Science statuses unchanged.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s12_falsifier_reach_check_v2.py
"""

import hashlib
import json
import os

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))

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
REGISTRY_EDGE_VAS = set(TEMPLATE_MACHINERY) - {0x004D1430}

SOURCES = [
    ("G2", "G2_CALLEE_DEEPDIVE.json"),
    ("G3", "G3_FALSIFIER_PATH.json"),
    ("G4", "G4_TERMINAL_CONSUMER.json"),
    ("G5", "G5_LOOKUP_CLOSURE.json"),
    ("G6", "G6_SIDS_PARSER.json"),
]

HIT_CLASSIFICATION = {
    "classification": "GENERIC_SHARED_MAP_FIND__NOT_A_TEMPLATE_REGISTRY_EDGE",
    "reason": (
        "the call walks the string-table 0x98-manager's own RB-tree map "
        "@[mgr+4] (singleton DAT_00BA12F4, getter FUN_00415670) with a "
        "composite key {section_object, 4057} and string values; the template "
        "registry tree DAT_00BA1824 is a DIFFERENT singleton, referenced only "
        "inside getter FUN_0043A550, which is called by nothing on the 4057 "
        "path; FUN_0072F580 (the only independently proven template-id "
        "consumer) is not called anywhere on the path; FUN_004D1430 is the "
        "shared generic STL RB-tree mapfind primitive (the registry lookup "
        "FUN_0072F580 itself calls it)"
    ),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(name):
    with open(os.path.join(RAW, name), "r", encoding="utf-8") as f:
        return json.load(f)


def hits_from_callee_targets(callee_targets):
    hits = []
    for c in (callee_targets or []):
        tv = c.get("target")
        if tv is None:
            continue
        tvi = int(tv, 16)
        if tvi in TEMPLATE_MACHINERY:
            hits.append({"from": c.get("from"), "target": tv,
                         "role": TEMPLATE_MACHINERY[tvi]})
    return hits


def main():
    per_function = {}

    # G1: containing function; its callees live under measured.callees
    g1 = load_json("G1_FUNCTION_DUMP.json")
    fnd = g1.get("measured", {}).get("function", {})
    hits = []
    for c in g1.get("measured", {}).get("callees", []):
        for t in c.get("targets", []):
            tv = t.get("target")
            if tv is None:
                continue
            tvi = int(tv, 16)
            if tvi in TEMPLATE_MACHINERY:
                hits.append({"from": c.get("call_va"), "target": tv,
                             "role": TEMPLATE_MACHINERY[tvi]})
    per_function["G1_FUN_00599d30"] = {
        "entry": fnd.get("entry"), "name": fnd.get("name"),
        "direct_template_machinery_hits": hits,
        "note": "177 call sites checked (01_RAW/CALL_XREF_CENSUS.json)",
    }

    # G2..G6: measured.functions with callee_targets
    for tag, name in SOURCES:
        d = load_json(name)
        for label, v in sorted(d.get("measured", {}).get("functions", {}).items()):
            per_function["%s_%s" % (tag, label)] = {
                "entry": v.get("entry"), "name": v.get("name"),
                "direct_template_machinery_hits":
                    hits_from_callee_targets(v.get("callee_targets")),
            }

    # embed the classification on every recorded hit row
    for row in per_function.values():
        for h in row["direct_template_machinery_hits"]:
            h.update(HIT_CLASSIFICATION)

    # row-consistency assertions (fail closed)
    assert len(per_function) == 18, "expected 18 functions, got %d" % len(per_function)
    all_hits = [(k, h) for k, row in per_function.items()
                for h in row["direct_template_machinery_hits"]]
    assert len(all_hits) == 1, "expected exactly 1 machinery hit, got %d" % len(all_hits)
    hk, hh = all_hits[0]
    assert hk == "G5_H03_extract_00823c10", "unexpected hit function %s" % hk
    assert hh["from"] == "0x00823C57" and hh["target"] == "0x004D1430", "unexpected hit %r" % hh
    registry_edges = [(k, h) for k, row in per_function.items()
                      for h in row["direct_template_machinery_hits"]
                      if int(h["target"], 16) in REGISTRY_EDGE_VAS]
    assert len(registry_edges) == 0, "registry edges must be 0"

    census = {}
    for k in per_function:
        tag = k.split("_", 1)[0]
        census[tag] = census.get(tag, 0) + 1

    reach = {
        "run_id": RUN_ID,
        "stage": "S12_falsifier_reach_check_g1_to_g6_amend_r1",
        "measured": {
            "template_machinery_va_set": dict(
                ("0x%08X" % k, v) for k, v in sorted(TEMPLATE_MACHINERY.items())),
            "per_function": per_function,
            "per_function_census": census,
            "total_functions_checked": len(per_function),
            "supersedes": (
                "the s7_curate_g4.py-written FALSIFIER_REACH_CHECK.json (stage "
                "S7_falsifier_reach_check; 13 functions = g1..g4 + the "
                "containing function; the only version that actually shipped "
                "in the original package) and the never-landed s8_curate_g5.py "
                "g1..g5 regeneration; the g6 function (FUN_00821e70) was never "
                "in the artifact before this R1 regeneration"
            ),
        },
        "interpreted": {
            "TOTAL_FUNCTIONS_CHECKED": len(per_function),
            "TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS": len(all_hits),
            "TOTAL_GENERIC_MACHINERY_HITS": len(all_hits),
            "TOTAL_TEMPLATE_REGISTRY_EDGES": len(registry_edges),
            "SINGLE_HIT": {
                "function": "G5_H03_extract_00823c10 (FUN_00823C10, the 0x98-manager extract)",
                "from": "0x00823C57",
                "target": "0x004D1430",
            },
            "NOTE_ON_FUN_004D1430": (
                "FUN_004D1430 is the GENERIC STL RB-tree mapfind primitive "
                "shared by many maps (the template registry lookup FUN_0072F580 "
                "itself calls it). A hit of 0x004D1430 does NOT establish a "
                "template-registry edge: the registry identity edge requires "
                "FUN_0072F580 (the thiscall wrapper over the registry singleton "
                "DAT_00BA1824 via getter FUN_0043A550). In the measured chain "
                "the tree walked by FUN_00823C10 belongs to the string-table "
                "manager singleton (0x98 object at DAT_00BA12F4 via FUN_00415670) "
                "with a composite key {section_object, 4057} and string values, "
                "NOT the template registry."
            ),
            "qc_cross_check": (
                "04_QC/TARGETED_QC_REPORT.md Q8 independently measured the same "
                "single in-window machinery hit (FUN_004D1430 @0x00823C57 inside "
                "FUN_00823C10) over all 18 measured-function windows, with ZERO "
                "template-registry edges - executor + QC agreement"
            ),
            "pin_provenance": {
                "reach_check": {
                    "MEASURED_QUANTITY": "direct CALL targets of every function measured this run (g1..g6 = 18 functions), tested against the fixed canon template-machinery VA set",
                    "INDEPENDENT_SOURCE_OF_TRUTH": "the callee lists are Ghidra-resolved direct CALL flows from the byte-verified listings committed in 01_RAW (g1: 951/951 byte-verified vs the physical EXE; g2-g6: same pipeline)",
                    "WHY_NON_CIRCULAR": "the machinery VA set is fixed canon (TRACE_EDGE_BLOCKS E1-E3 chain), not derived from this run's search; hits are reported as measured, not inferred",
                    "FAILURE_CASE_DETECTED": "if 4057's chain reached the registry, FUN_008dfcd0 / FUN_00821bb0 / FUN_00821760 / FUN_00415670 / FUN_00823c10 / FUN_008dfb70 would show FUN_0072F580 / FUN_0043A550 as direct callees - none found, which falsifies the template-id hypothesis for this call-site (the mandatory falsifier fired)",
                }
            },
            "amend_provenance": {
                "round": "R1 (2026-10-03) - the single authorized QC repair round (contract clause QC_REPAIR_ROUNDS_MAX = 1)",
                "finding": "F-P2-1 (04_QC/TARGETED_QC_REPORT.md) + F-P3-5",
                "generator": "03_SCRIPTS/s12_falsifier_reach_check_v2.py (hash in 03_SCRIPTS/SCRIPT_SHA256.csv)",
                "log": "05_REPORT/AMEND_LOG_R1.md",
                "science_statuses_unchanged": "IMMEDIATE_4057_IS_TEMPLATE_ID = REJECTED_FOR_THIS_CALLSITE; MANDATORY_FALSIFIER_RESULT = FAIL_NUMERIC_COINCIDENCE; LANDMARK_TRACE_LEVEL = 0 (all unchanged)",
                "no_new_science": "reads only the curated 01_RAW JSON artifacts already committed by the original run; no new measurement",
            },
        },
        "errors": [],
    }

    out_path = os.path.join(RAW, "FALSIFIER_REACH_CHECK.json")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        json.dump(reach, f, indent=2)
        f.write("\n")
    print("FALSIFIER_REACH_CHECK.json regenerated:", out_path)
    print("total_functions_checked:", reach["measured"]["total_functions_checked"])
    print("TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS:", reach["interpreted"]["TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS"])
    print("TOTAL_TEMPLATE_REGISTRY_EDGES:", reach["interpreted"]["TOTAL_TEMPLATE_REGISTRY_EDGES"])

    # ---- SCRIPT_SHA256.csv regeneration (F-P3-5): no BOM, no blank lines
    scripts = sorted(fn for fn in os.listdir(HERE) if fn.endswith(".py"))
    lines = ["script,sha256"]
    for s in scripts:
        lines.append("%s,%s" % (s, sha256_file(os.path.join(HERE, s))))
    content = "\n".join(lines) + "\n"
    csv_path = os.path.join(HERE, "SCRIPT_SHA256.csv")
    with open(csv_path, "wb") as f:
        f.write(content.encode("utf-8"))
    print("SCRIPT_SHA256.csv regenerated:", csv_path, "rows:", len(lines) - 1)


if __name__ == "__main__":
    main()
