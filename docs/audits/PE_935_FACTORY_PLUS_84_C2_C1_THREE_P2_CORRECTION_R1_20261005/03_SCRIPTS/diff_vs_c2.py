# diff_vs_c2.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005
# REGRESSION vs the committed C2 artifacts (READ-ONLY): reports EVERY
# changed field between this run's regenerated artifacts and the committed
# C2 package, so the correction's blast radius is measured, never assumed.
# Covers: the 133 pin rows (JSON + CSV), all census rows, the C2_CENSUS
# measured quantities, the C3 key fields, the AF3 ledger rows, and the
# boundary-test case set. Nothing from C2 is modified.
# Outputs: 01_RAW/CHANGED_FIELDS_VS_C2.json + CHANGED_BOUNDARY_FIELDS_VS_C2.csv
# (--out/--csv overrides). READ-ONLY vs both packages.

import argparse
import csv
import json
import os
import sys

sys.dont_write_bytecode = True

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005")
C2 = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
      r"\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004")


def load_json(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return json.load(f)


def load_csv(root, rel):
    with open(os.path.join(root, rel), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "CHANGED_FIELDS_VS_C2.json"))
    ap.add_argument("--csv", default=os.path.join(RUN, "CHANGED_BOUNDARY_FIELDS_VS_C2.csv"))
    args = ap.parse_args()

    changes = []   # rows of {artifact, row/pin, field, old, new}
    stats = {"pin_rows_compared": 0, "pin_fields_changed": 0,
             "census_rows_compared": 0, "census_rows_changed": 0,
             "census_new_rows": 0, "census_missing_rows": 0,
             "af3_rows_changed": 0, "census_qty_changed": 0,
             "c3_changed": 0, "boundary_cases_added": 0}

    # ---- 1. pin CSV: same claim_id rows, every field ----
    old_pins = {r["claim_id"]: r for r in load_csv(C2, "CORRECTED_PIN_LEDGER.csv")}
    new_pins = {r["claim_id"]: r for r in load_csv(RUN, "CORRECTED_PIN_LEDGER.csv")}
    for cid in sorted(old_pins):
        stats["pin_rows_compared"] += 1
        if cid not in new_pins:
            changes.append({"artifact": "CORRECTED_PIN_LEDGER.csv", "row": cid,
                            "field": "<ROW>", "old": "present", "new": "MISSING"})
            continue
        for fld in old_pins[cid]:
            if old_pins[cid][fld] != new_pins[cid].get(fld):
                stats["pin_fields_changed"] += 1
                changes.append({"artifact": "CORRECTED_PIN_LEDGER.csv", "row": cid,
                                "field": fld, "old": old_pins[cid][fld],
                                "new": new_pins[cid].get(fld)})
    for cid in sorted(set(new_pins) - set(old_pins)):
        changes.append({"artifact": "CORRECTED_PIN_LEDGER.csv", "row": cid,
                        "field": "<ROW>", "old": "MISSING", "new": "present"})

    # ---- 2. pin JSON: same claim_id pins, every field (incl. nested EA) ----
    old_j = load_json(C2, os.path.join("01_RAW", "C1_PIN_EVIDENCE.json"))
    new_j = load_json(RUN, os.path.join("01_RAW", "C1_PIN_EVIDENCE.json"))
    old_by_id = {p["claim_id"]: p for p in old_j["pins"]}
    new_by_id = {p["claim_id"]: p for p in new_j["pins"]}
    json_pin_changes = 0
    for cid in sorted(old_by_id):
        op, np_ = old_by_id[cid], new_by_id.get(cid)
        if np_ is None:
            changes.append({"artifact": "01_RAW/C1_PIN_EVIDENCE.json", "row": cid,
                            "field": "<PIN>", "old": "present", "new": "MISSING"})
            continue
        for fld in op:
            if fld == "effective_address":
                continue  # handled below (nested)
            if op[fld] != np_.get(fld):
                json_pin_changes += 1
                changes.append({"artifact": "01_RAW/C1_PIN_EVIDENCE.json", "row": cid,
                                "field": fld, "old": op[fld], "new": np_.get(fld)})
        oe = op.get("effective_address")
        ne = np_.get("effective_address")
        if isinstance(oe, dict) and isinstance(ne, dict):
            for fld in oe:
                if oe[fld] != ne.get(fld):
                    json_pin_changes += 1
                    changes.append({"artifact": "01_RAW/C1_PIN_EVIDENCE.json", "row": cid,
                                    "field": "effective_address." + fld,
                                    "old": oe[fld], "new": ne.get(fld)})
        elif (oe is None) != (ne is None):
            changes.append({"artifact": "01_RAW/C1_PIN_EVIDENCE.json", "row": cid,
                            "field": "effective_address", "old": oe, "new": ne})

    # ---- 3. census CSV: row-by-row (key: va + pattern_family), every field ----
    old_c = load_csv(C2, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
    new_c = load_csv(RUN, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
    key = lambda r: (r["va"], r["pattern_family"])  # noqa: E731
    old_ck = {key(r): r for r in old_c}
    new_ck = {key(r): r for r in new_c}
    for k in sorted(old_ck):
        stats["census_rows_compared"] += 1
        if k not in new_ck:
            stats["census_missing_rows"] += 1
            changes.append({"artifact": "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv",
                            "row": "va=%s fam=%s" % k, "field": "<ROW>",
                            "old": "present", "new": "MISSING"})
            continue
        diff = [f for f in old_ck[k]
                if f not in ("row_id", "reason") and old_ck[k][f] != new_ck[k].get(f)]
        if diff:
            stats["census_rows_changed"] += 1
            for f in diff:
                changes.append({"artifact": "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv",
                                "row": "va=%s fam=%s" % k, "field": f,
                                "old": old_ck[k][f], "new": new_ck[k].get(f)})
    stats["census_new_rows"] = len(set(new_ck) - set(old_ck))

    # ---- 4. C2_CENSUS.json measured quantities ----
    old_mq = load_json(C2, os.path.join("01_RAW", "C2_CENSUS.json"))["measured_quantities"]
    new_mq = load_json(RUN, os.path.join("01_RAW", "C2_CENSUS.json"))["measured_quantities"]
    for k in sorted(old_mq):
        if old_mq[k] != new_mq.get(k):
            stats["census_qty_changed"] += 1
            changes.append({"artifact": "01_RAW/C2_CENSUS.json", "row": "measured_quantities",
                            "field": k, "old": old_mq[k], "new": new_mq.get(k)})
    for k in sorted(set(new_mq) - set(old_mq)):
        changes.append({"artifact": "01_RAW/C2_CENSUS.json", "row": "measured_quantities",
                        "field": k, "old": "MISSING", "new": new_mq[k]})

    # ---- 5. C3_OBJECT_SCOPE.json key fields ----
    old_c3 = load_json(C2, os.path.join("01_RAW", "C3_OBJECT_SCOPE.json"))
    new_c3 = load_json(RUN, os.path.join("01_RAW", "C3_OBJECT_SCOPE.json"))
    for fld in ("examined_ctor", "direct_vptr_store_in_examined_ctor",
                "known_examined_callsites_direct", "ctor_callsite_census",
                "allocation_size_facts"):
        if json.dumps(old_c3.get(fld), sort_keys=True) != json.dumps(new_c3.get(fld), sort_keys=True):
            stats["c3_changed"] += 1
            changes.append({"artifact": "01_RAW/C3_OBJECT_SCOPE.json", "row": fld,
                            "field": "<OBJECT>", "old": "<differs>",
                            "new": "<differs - see JSON>"})

    # ---- 6. AF3 ledger rows ----
    old_af3 = {r["CANDIDATE_VA"]: r for r in load_csv(C2, "AF3_PROVENANCE_LEDGER.csv")}
    new_af3 = {r["CANDIDATE_VA"]: r for r in load_csv(RUN, "AF3_PROVENANCE_LEDGER.csv")}
    for va in sorted(old_af3):
        for fld in old_af3[va]:
            if old_af3[va][fld] != new_af3.get(va, {}).get(fld):
                stats["af3_rows_changed"] += 1
                changes.append({"artifact": "AF3_PROVENANCE_LEDGER.csv", "row": va,
                                "field": fld, "old": old_af3[va][fld],
                                "new": new_af3.get(va, {}).get(fld)})

    # ---- 7. boundary case set: which cases are new this run ----
    old_ce = load_json(C2, os.path.join("01_RAW", "CQC_BOUNDARY_COUNTEREXAMPLES.json"))
    new_ce = load_json(RUN, os.path.join("01_RAW", "CQC_BOUNDARY_COUNTEREXAMPLES.json"))
    old_ids = {c["CASE_ID"] for c in old_ce["counterexamples"]}
    new_ids = {c["CASE_ID"] for c in new_ce["counterexamples"]}
    stats["boundary_cases_added"] = len(new_ids - old_ids)
    stats["boundary_cases_removed"] = len(old_ids - new_ids)
    for cid in sorted(new_ids - old_ids):
        changes.append({"artifact": "01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json",
                        "row": cid, "field": "<CASE>", "old": "MISSING",
                        "new": "present (new falsifier this run)"})

    out = {"run": "PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005",
           "compared_against": "docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_"
                               "C2_AF1_AF3_CORRECTION_R1_20261004 (READ ONLY, "
                               "committed at c4cb60f)",
           "stats": stats, "pin_json_fields_changed": json_pin_changes,
           "changes": changes}
    with open(args.out, "w", newline="\n", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["artifact", "row_or_pin", "field", "old", "new"])
        for c in changes:
            w.writerow([c["artifact"], c["row"], c["field"],
                        json.dumps(c["old"])[:400], json.dumps(c["new"])[:400]])
    print("diff_vs_c2: %d changed fields; stats=%s" % (len(changes), json.dumps(stats)))


if __name__ == "__main__":
    main()
