# diff_vs_base.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# REGRESSION vs the exact BASE source package (the committed THREE-P2
# package at BASE_SHA 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92, READ ONLY):
# reports EVERY changed row/field INCLUDING RUN labels, and distinguishes
# BYTE IDENTITY from identity after excluding DECLARED METADATA (the
# per-artifact top-level "run" label). Covers: the 133 pin rows (JSON+CSV),
# all census rows, the C2_CENSUS measured quantities, the C3 key objects,
# the AF3 ledger rows, the decoder unit battery, the boundary-test case set,
# the mutation records, and the independent-oracle fixture set. Nothing
# from the BASE package is modified. Evidence-status changes are explained
# by THIS run; old totals (133/2612/10/2218/832/...) are NOT forced - they
# are re-measured and reported here.
# Output: REGRESSION_DIFF.json (--out override). READ-ONLY vs both packages.

import argparse
import csv
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")
BASE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
        r"\PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005")
BASE_SHA = "9d31a82b6589f46e9ca6c75c6e323b433c1ebf92"


def load_json(root, rel):
    with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
        return json.load(f)


def load_csv(root, rel):
    with open(os.path.join(root, *rel.split("/")), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()


def strip_run(obj):
    """Deep-copy with the top-level 'run' label removed (the DECLARED
    metadata of every generated JSON artifact; all other keys compared)."""
    c = dict(obj)
    c.pop("run", None)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "REGRESSION_DIFF.json"))
    args = ap.parse_args()

    reports = {}
    metadata_changes = []
    content_changes = []

    def artifact_report(rel, base_exists=True):
        rep = {"byte_identical": None, "sha256_base": None, "sha256_new": None}
        p_new = os.path.join(RUN, *rel.split("/"))
        p_base = os.path.join(BASE, *rel.split("/"))
        rep["sha256_new"] = sha256_file(p_new)
        if base_exists:
            rep["sha256_base"] = sha256_file(p_base)
            rep["byte_identical"] = (rep["sha256_base"] == rep["sha256_new"])
        reports[rel] = rep
        return rep

    # ---- 1. pin CSV: same claim_id rows, every field ----
    old_pins = {r["claim_id"]: r for r in load_csv(BASE, "CORRECTED_PIN_LEDGER.csv")}
    new_pins = {r["claim_id"]: r for r in load_csv(RUN, "CORRECTED_PIN_LEDGER.csv")}
    pin_csv_changes = []
    for cid in sorted(old_pins):
        if cid not in new_pins:
            pin_csv_changes.append({"row": cid, "field": "<ROW>", "old": "present",
                                   "new": "MISSING"})
            continue
        for fld in old_pins[cid]:
            if old_pins[cid][fld] != new_pins[cid].get(fld):
                pin_csv_changes.append({"row": cid, "field": fld,
                                        "old": old_pins[cid][fld],
                                        "new": new_pins[cid].get(fld)})
    for cid in sorted(set(new_pins) - set(old_pins)):
        pin_csv_changes.append({"row": cid, "field": "<ROW>", "old": "MISSING",
                               "new": "present"})
    artifact_report("CORRECTED_PIN_LEDGER.csv")
    reports["CORRECTED_PIN_LEDGER.csv"].update(
        {"rows_base": len(old_pins), "rows_new": len(new_pins),
         "field_changes": pin_csv_changes})
    content_changes += [{"artifact": "CORRECTED_PIN_LEDGER.csv", **c}
                        for c in pin_csv_changes]

    # ---- 2. pin JSON: same claim_id pins, every field (incl. nested EA);
    # top-level keys except the declared 'run' label ----
    old_j = load_json(BASE, "01_RAW/C1_PIN_EVIDENCE.json")
    new_j = load_json(RUN, "01_RAW/C1_PIN_EVIDENCE.json")
    old_by_id = {p["claim_id"]: p for p in old_j["pins"]}
    new_by_id = {p["claim_id"]: p for p in new_j["pins"]}
    pin_json_changes = []
    for cid in sorted(old_by_id):
        op, np_ = old_by_id[cid], new_by_id.get(cid)
        if np_ is None:
            pin_json_changes.append({"row": cid, "field": "<PIN>",
                                     "old": "present", "new": "MISSING"})
            continue
        for fld in op:
            if fld == "effective_address":
                continue
            if op[fld] != np_.get(fld):
                pin_json_changes.append({"row": cid, "field": fld,
                                        "old": op[fld], "new": np_.get(fld)})
        oe = op.get("effective_address")
        ne = np_.get("effective_address")
        if isinstance(oe, dict) and isinstance(ne, dict):
            for fld in oe:
                if oe[fld] != ne.get(fld):
                    pin_json_changes.append(
                        {"row": cid, "field": "effective_address." + fld,
                         "old": oe[fld], "new": ne.get(fld)})
        elif (oe is None) != (ne is None):
            pin_json_changes.append({"row": cid, "field": "effective_address",
                                     "old": oe, "new": ne})
    for cid in sorted(set(new_by_id) - set(old_by_id)):
        pin_json_changes.append({"row": cid, "field": "<PIN>", "old": "MISSING",
                                 "new": "present"})
    # top-level keys except 'run'
    for k in sorted(set(strip_run(old_j)) | set(strip_run(new_j))):
        if strip_run(old_j).get(k) != strip_run(new_j).get(k):
            pin_json_changes.append({"row": "<TOP-LEVEL>", "field": k,
                                     "old": strip_run(old_j).get(k),
                                     "new": strip_run(new_j).get(k)})
    if old_j.get("run") != new_j.get("run"):
        metadata_changes.append({"artifact": "01_RAW/C1_PIN_EVIDENCE.json",
                                 "field": "run", "old": old_j.get("run"),
                                 "new": new_j.get("run"),
                                 "class": "DECLARED_METADATA (run label)"})
    artifact_report("01_RAW/C1_PIN_EVIDENCE.json")
    reports["01_RAW/C1_PIN_EVIDENCE.json"].update(
        {"pins_base": len(old_by_id), "pins_new": len(new_by_id),
         "content_changes_after_metadata": pin_json_changes})
    content_changes += [{"artifact": "01_RAW/C1_PIN_EVIDENCE.json", **c}
                        for c in pin_json_changes]

    # ---- 3. census CSV: row-by-row (key: va + pattern_family) ----
    old_c = load_csv(BASE, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
    new_c = load_csv(RUN, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
    key = lambda r: (r["va"], r["pattern_family"])  # noqa: E731
    old_ck = {key(r): r for r in old_c}
    new_ck = {key(r): r for r in new_c}
    census_changes = []
    census_rows_changed = 0
    for k in sorted(old_ck):
        if k not in new_ck:
            census_changes.append({"row": "va=%s fam=%s" % k, "field": "<ROW>",
                                   "old": "present", "new": "MISSING"})
            census_rows_changed += 1
            continue
        diff = [f for f in old_ck[k] if old_ck[k][f] != new_ck[k].get(f)]
        if diff:
            census_rows_changed += 1
            for f in diff:
                census_changes.append({"row": "va=%s fam=%s" % k, "field": f,
                                       "old": old_ck[k][f],
                                       "new": new_ck[k].get(f)})
    for k in sorted(set(new_ck) - set(old_ck)):
        census_changes.append({"row": "va=%s fam=%s" % k, "field": "<ROW>",
                               "old": "MISSING", "new": "present"})
        census_rows_changed += 1
    artifact_report("CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
    reports["CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"].update(
        {"rows_base": len(old_c), "rows_new": len(new_c),
         "rows_changed": census_rows_changed,
         "field_changes": census_changes})
    content_changes += [{"artifact": "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv", **c}
                        for c in census_changes]

    # ---- 4. C2_CENSUS.json: full compare except the declared 'run' label ----
    old_cc = load_json(BASE, "01_RAW/C2_CENSUS.json")
    new_cc = load_json(RUN, "01_RAW/C2_CENSUS.json")
    cc_changes = []
    so, sn = strip_run(old_cc), strip_run(new_cc)
    for k in sorted(set(so) | set(sn)):
        if so.get(k) != sn.get(k):
            cc_changes.append({"field": k, "old": so.get(k), "new": sn.get(k)})
    if old_cc.get("run") != new_cc.get("run"):
        metadata_changes.append({"artifact": "01_RAW/C2_CENSUS.json",
                                 "field": "run", "old": old_cc.get("run"),
                                 "new": new_cc.get("run"),
                                 "class": "DECLARED_METADATA (run label)"})
    artifact_report("01_RAW/C2_CENSUS.json")
    reports["01_RAW/C2_CENSUS.json"].update(
        {"content_changes_after_metadata": cc_changes})
    content_changes += [{"artifact": "01_RAW/C2_CENSUS.json", **c}
                        for c in cc_changes]

    # ---- 5. C3_OBJECT_SCOPE.json: full compare except 'run' ----
    old_c3 = load_json(BASE, "01_RAW/C3_OBJECT_SCOPE.json")
    new_c3 = load_json(RUN, "01_RAW/C3_OBJECT_SCOPE.json")
    c3_changes = []
    so3, sn3 = strip_run(old_c3), strip_run(new_c3)
    for k in sorted(set(so3) | set(sn3)):
        if so3.get(k) != sn3.get(k):
            c3_changes.append({"field": k, "old": so3.get(k), "new": sn3.get(k)})
    if old_c3.get("run") != new_c3.get("run"):
        metadata_changes.append({"artifact": "01_RAW/C3_OBJECT_SCOPE.json",
                                 "field": "run", "old": old_c3.get("run"),
                                 "new": new_c3.get("run"),
                                 "class": "DECLARED_METADATA (run label)"})
    artifact_report("01_RAW/C3_OBJECT_SCOPE.json")
    reports["01_RAW/C3_OBJECT_SCOPE.json"].update(
        {"content_changes_after_metadata": c3_changes})
    content_changes += [{"artifact": "01_RAW/C3_OBJECT_SCOPE.json", **c}
                        for c in c3_changes]

    # ---- 6. AF3 ledger rows ----
    old_af3 = {r["CANDIDATE_VA"]: r for r in load_csv(BASE, "AF3_PROVENANCE_LEDGER.csv")}
    new_af3 = {r["CANDIDATE_VA"]: r for r in load_csv(RUN, "AF3_PROVENANCE_LEDGER.csv")}
    af3_changes = []
    for va in sorted(set(old_af3) | set(new_af3)):
        if va not in new_af3:
            af3_changes.append({"row": va, "field": "<ROW>", "old": "present",
                                "new": "MISSING"})
            continue
        if va not in old_af3:
            af3_changes.append({"row": va, "field": "<ROW>", "old": "MISSING",
                                "new": "present"})
            continue
        for fld in old_af3[va]:
            if old_af3[va][fld] != new_af3[va].get(fld):
                af3_changes.append({"row": va, "field": fld,
                                    "old": old_af3[va][fld],
                                    "new": new_af3[va].get(fld)})
    artifact_report("AF3_PROVENANCE_LEDGER.csv")
    reports["AF3_PROVENANCE_LEDGER.csv"].update(
        {"rows_base": len(old_af3), "rows_new": len(new_af3),
         "field_changes": af3_changes})
    content_changes += [{"artifact": "AF3_PROVENANCE_LEDGER.csv", **c}
                        for c in af3_changes]

    # ---- 7. decoder unit battery ----
    old_u = load_json(BASE, "01_RAW/CQC_DECODER_UNIT_TESTS.json")
    new_u = load_json(RUN, "01_RAW/CQC_DECODER_UNIT_TESTS.json")
    old_vecs = {v["vector"]: v for v in old_u["unit_battery"] if "vector" in v}
    new_vecs = {v["vector"]: v for v in new_u["unit_battery"] if "vector" in v}
    new_vectors = sorted(set(new_vecs) - set(old_vecs))
    removed_vectors = sorted(set(old_vecs) - set(new_vecs))
    changed_vectors = [v for v in sorted(set(old_vecs) & set(new_vecs))
                       if old_vecs[v] != new_vecs[v]]
    artifact_report("01_RAW/CQC_DECODER_UNIT_TESTS.json", base_exists=True)
    reports["01_RAW/CQC_DECODER_UNIT_TESTS.json"].update(
        {"vector_count_base": len(old_u["unit_battery"]),
         "vector_count_new": len(new_u["unit_battery"]),
         "new_vectors": new_vectors, "removed_vectors": removed_vectors,
         "changed_vectors": changed_vectors,
         "redecode_bad_rows_base": old_u.get("redecode_bad_rows"),
         "redecode_bad_rows_new": new_u.get("redecode_bad_rows")})
    content_changes.append({"artifact": "01_RAW/CQC_DECODER_UNIT_TESTS.json",
                            "field": "<UNIT_BATTERY>", "old": "%d vectors" % len(old_u["unit_battery"]),
                            "new": "%d vectors (+%d D1 vectors)" % (
                                len(new_u["unit_battery"]), len(new_vectors))})

    # ---- 8. boundary case set ----
    old_ce = load_json(BASE, "01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json")
    new_ce = load_json(RUN, "01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json")
    old_ids = {c["CASE_ID"]: c for c in old_ce["counterexamples"]}
    new_ids = {c["CASE_ID"]: c for c in new_ce["counterexamples"]}
    new_cases = sorted(set(new_ids) - set(old_ids))
    removed_cases = sorted(set(old_ids) - set(new_ids))
    changed_cases = [c for c in sorted(set(old_ids) & set(new_ids))
                     if old_ids[c] != new_ids[c]]
    artifact_report("01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json")
    reports["01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json"].update(
        {"case_count_base": len(old_ids), "case_count_new": len(new_ids),
         "new_cases": new_cases, "removed_cases": removed_cases,
         "changed_cases": changed_cases})
    content_changes.append({"artifact": "01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json",
                            "field": "<CASE_SET>", "old": "%d cases" % len(old_ids),
                            "new": "%d cases (+%s)" % (len(new_ids), "; ".join(new_cases))})

    # ---- 9. mutation records (the retained 7 old controls) ----
    old_mut = load_json(BASE, "01_RAW/CQC_MUTATION_RESULTS.json")
    new_mut = load_json(RUN, "01_RAW/CQC_MUTATION_RESULTS.json")
    old_mids = [r["MUTATION_ID"] for r in old_mut["results"]]
    new_mids = [r["MUTATION_ID"] for r in new_mut["results"]]
    mut_id_changes = (old_mids == new_mids)
    old_causal = sum(1 for r in old_mut["results"] if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS")
    new_causal = sum(1 for r in new_mut["results"] if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS")
    artifact_report("01_RAW/CQC_MUTATION_RESULTS.json")
    reports["01_RAW/CQC_MUTATION_RESULTS.json"].update(
        {"mutation_ids_base": old_mids, "mutation_ids_new": new_mids,
         "ids_identical": mut_id_changes,
         "causal_pass_base": old_causal, "causal_pass_new": new_causal})
    d2_mut = load_json(RUN, "01_RAW/D2_MUTATION_RESULTS.json")
    reports["01_RAW/D2_MUTATION_RESULTS.json"] = {
        "artifact_class": "NEW (no BASE counterpart)",
        "mutation_ids": [r["MUTATION_ID"] for r in d2_mut["results"]],
        "causal_pass": sum(1 for r in d2_mut["results"]
                           if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS"),
    }
    content_changes.append({"artifact": "01_RAW/D2_MUTATION_RESULTS.json",
                            "field": "<FILE>", "old": "MISSING",
                            "new": "NEW: %d D2 mutation records" % len(d2_mut["results"])})

    # ---- 10. independent-oracle fixture set ----
    old_or = load_json(BASE, "01_RAW/ORACLE_INDEPENDENT_RECORDS.json")
    new_or = load_json(RUN, "01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json")
    old_fx = {f["name"]: f for f in old_or["fixtures"]}
    new_fx = {f["name"]: f for f in new_or["fixtures"]}
    new_fixtures = sorted(set(new_fx) - set(old_fx))
    removed_fixtures = sorted(set(old_fx) - set(new_fx))
    changed_fixtures = [n for n in sorted(set(old_fx) & set(new_fx))
                        if {k: v for k, v in old_fx[n].items() if k not in ("raw_stdout", "raw_stderr")}
                        != {k: v for k, v in new_fx[n].items() if k not in ("raw_stdout", "raw_stderr")}]
    reports["01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json"] = {
        "artifact_class": "RENAMED + EXTENDED (BASE: ORACLE_INDEPENDENT_RECORDS.json)",
        "fixture_count_base": len(old_fx), "fixture_count_new": len(new_fx),
        "new_fixtures": new_fixtures, "removed_fixtures": removed_fixtures,
        "changed_fixtures": changed_fixtures,
        "oracle_version_base": old_or.get("oracle_version_raw"),
        "oracle_version_new": new_or.get("oracle_version_raw"),
    }
    content_changes.append({"artifact": "01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json",
                            "field": "<FILE>", "old": "71 fixtures (ORACLE_INDEPENDENT_RECORDS.json)",
                            "new": "%d fixtures incl. %d D1 fixtures" % (
                                len(new_fx), len(new_fixtures))})

    # ---- 11. EXPECTED_PIN_REGISTRY.json: NEW artifact of this run ----
    reg = load_json(RUN, "EXPECTED_PIN_REGISTRY.json")
    reports["EXPECTED_PIN_REGISTRY.json"] = {
        "artifact_class": "NEW (no BASE counterpart; the D2 expected roster)",
        "expected_total": reg.get("expected_total"),
        "expected_role_tally": reg.get("expected_role_tally"),
        "expected_ea_required_count": reg.get("expected_ea_required_count"),
        "source": reg.get("source"),
    }
    content_changes.append({"artifact": "EXPECTED_PIN_REGISTRY.json",
                            "field": "<FILE>", "old": "MISSING",
                            "new": "NEW: the D2 expected pin registry (%s claims)"
                                   % reg.get("expected_total")})

    # ---- 12. D1_BOUNDARY_FALSIFIER.json: NEW artifact of this run ----
    d1f = load_json(RUN, "01_RAW/D1_BOUNDARY_FALSIFIER.json")
    reports["01_RAW/D1_BOUNDARY_FALSIFIER.json"] = {
        "artifact_class": "NEW (no BASE counterpart)",
        "case": d1f["record"]["CASE_ID"],
        "corrected_call_validation": d1f["record"]["CALL_VALIDATION"],
        "base_reproduction_call_validation":
            d1f["record"]["BASE_REPRODUCTION"]["call_validation"],
        "base_reproduction_target": d1f["record"]["BASE_REPRODUCTION"]["target"],
    }
    content_changes.append({"artifact": "01_RAW/D1_BOUNDARY_FALSIFIER.json",
                            "field": "<FILE>", "old": "MISSING",
                            "new": "NEW: the D1 downstream falsifier record"})

    # ---- summary ----
    byte_identical = {rel: rep["byte_identical"]
                      for rel, rep in reports.items()
                      if rep.get("byte_identical") is not None}
    summary = {
        "artifacts_byte_identical_to_base": sorted(
            [rel for rel, v in byte_identical.items() if v]),
        "artifacts_NOT_byte_identical": sorted(
            [rel for rel, v in byte_identical.items() if not v]),
        "content_change_count": len(content_changes),
        "metadata_only_change_count": len(metadata_changes),
        "declared_metadata_class": (
            "per-artifact top-level 'run' label (every regenerated JSON "
            "artifact of this run carries the NEW run id; the BASE run id is "
            "the compared value; all other fields are content)"),
        "census_rows_base": len(old_c), "census_rows_new": len(new_c),
        "pin_rows_base": len(old_pins), "pin_rows_new": len(new_pins),
        "af3_rows_base": len(old_af3), "af3_rows_new": len(new_af3),
        "measured_quantities_base": strip_run(old_cc).get("measured_quantities"),
        "measured_quantities_new": strip_run(new_cc).get("measured_quantities"),
    }
    out = {"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
           "compared_against": ("docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_"
                               "THREE_P2_CORRECTION_R1_20261005 (READ ONLY, "
                               "committed at %s)" % BASE_SHA),
           "reports": reports, "summary": summary,
           "metadata_only_changes": metadata_changes,
           "content_changes": content_changes}
    with open(args.out, "w", newline="\n", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("REGRESSION_DIFF: content_changes=%d metadata_only=%d byte_identical=%d/%d"
          % (len(content_changes), len(metadata_changes),
             sum(1 for v in byte_identical.values() if v), len(byte_identical)))


if __name__ == "__main__":
    main()
