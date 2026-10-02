#!/usr/bin/env python3
# FRESH INTERNAL QC (Q2) - INDEPENDENT pin census with my OWN artifact reader.
# NOT a copy of the executor's enumerate logic: independent recursive walk of each
# artifact JSON under the contract loading rule (pins[] with entry_pins fallback,
# then width_sources.<key>.width_pins[]). Counts, va-selector hits and identities
# are measured from the raw JSON documents themselves.
import sys
sys.dont_write_bytecode = True

import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
RAW = os.path.join(PKG, "01_RAW", "DESKTOP_CORRECTION_R1")
OUT = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM",
                   "INTERNAL_QC", "Q2_INDEPENDENT_CENSUS_RESULT.json")

ARTIFACTS = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]
SELECT_VA = "0x00977807"


def load(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def my_census(doc):
    """My OWN reader of the contract loading rule. Returns (counts, identities)
    where identities are (array_path, index, va_or_None) tuples."""
    counts = {}
    identities = []

    # main array: pins[] if present and non-empty, else entry_pins[] fallback
    main = doc.get("pins")
    used = None
    if isinstance(main, list) and len(main) > 0:
        used = "pins"
    elif "entry_pins" in doc:
        main = doc.get("entry_pins")
        if isinstance(main, list):
            used = "entry_pins"
    if used is not None:
        counts[used] = len(main)
        for i in range(len(main)):
            entry = main[i]
            va = entry.get("va") if isinstance(entry, dict) else None
            identities.append((used, i, va))

    # width_sources.<key>.width_pins[]
    ws = doc.get("width_sources")
    if isinstance(ws, dict):
        for key in sorted(ws.keys()):
            holder = ws[key]
            wp = holder.get("width_pins") if isinstance(holder, dict) else None
            if isinstance(wp, list):
                apath = "width_sources.%s.width_pins" % key
                counts[apath] = len(wp)
                for i in range(len(wp)):
                    entry = wp[i]
                    va = entry.get("va") if isinstance(entry, dict) else None
                    identities.append((apath, i, va))
    return counts, identities


def main():
    result = {"q": "Q2_independent_pin_census",
              "reader": "fresh-QC own artifact reader (no executor code reused)",
              "per_artifact": {}, "totals": {}, "selector": {}}
    total = 0
    grand_ids = []
    for art in ARTIFACTS:
        doc = load(os.path.join(RAW, art))
        counts, identities = my_census(doc)
        n = len(identities)
        result["per_artifact"][art] = {
            "pin_count": n, "counts_by_array": counts,
            "array_paths": sorted(counts.keys()),
        }
        total += n
        for (apath, idx, va) in identities:
            grand_ids.append("%s::%s[%d]" % (art, apath, idx))

    result["totals"] = {
        "input_pin_count": total,
        "unique_identity_count": len(set(grand_ids)),
        "identities_unique": len(set(grand_ids)) == total,
        "expected_185": total == 185,
        "per_artifact_order": [result["per_artifact"][a]["pin_count"] for a in ARTIFACTS],
    }

    # selector: pins with va == "0x00977807" in BRANCH_SELECTION_TRACE.json
    bst = load(os.path.join(RAW, "BRANCH_SELECTION_TRACE.json"))
    counts, identities = my_census(bst)
    main_arr = bst.get("pins")
    if isinstance(main_arr, list) and len(main_arr) > 0:
        used = "pins"
    else:
        main_arr = bst.get("entry_pins")
        used = "entry_pins"
    hits = [(i, p.get("va")) for i, p in enumerate(main_arr)
            if isinstance(p, dict) and p.get("va") == SELECT_VA]
    # also check no OTHER va in the whole four-artifact pin set equals the selector
    all_vas = []
    for art in ARTIFACTS:
        doc = load(os.path.join(RAW, art))
        _c, ids = my_census(doc)
        for (apath, idx, va) in ids:
            if va == SELECT_VA:
                all_vas.append("%s::%s[%d]" % (art, apath, idx))
    result["selector"] = {
        "target_va": SELECT_VA,
        "artifact": "BRANCH_SELECTION_TRACE.json",
        "array_used": used,
        "hit_count": len(hits),
        "hit_indices": [h[0] for h in hits],
        "exactly_one_hit": len(hits) == 1,
        "hit_index_is_74": len(hits) == 1 and hits[0][0] == 74,
        "selector_hits_across_all_four_artifacts": all_vas,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    ok = (total == 185 and len(set(grand_ids)) == total and len(hits) == 1
          and hits[0][0] == 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
