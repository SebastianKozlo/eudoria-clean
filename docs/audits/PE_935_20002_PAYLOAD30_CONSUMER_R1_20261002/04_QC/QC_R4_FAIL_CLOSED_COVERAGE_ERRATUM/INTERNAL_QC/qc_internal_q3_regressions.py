#!/usr/bin/env python3
# FRESH INTERNAL QC (Q3) - re-execute BOTH regressions by running the repaired
# validator as a SUBPROCESS with MY OWN output paths under INTERNAL_QC\.
# Never touches the executor's POSITIVE\/INVALID_VA\ results.
# Then compares census values (value level) against the executor's committed
# result JSONs and verifies the identity-set bijection with my OWN reader.
import sys
sys.dont_write_bytecode = True

import json
import os
import subprocess

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
REV = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM")
VALIDATOR = os.path.join(REV, "qc_tools", "qc4_q1_pinverify.py")
RAW = os.path.join(PKG, "01_RAW", "DESKTOP_CORRECTION_R1")
FIXTURE = os.path.join(REV, "FIXTURE_INVALID_VA")
IQ = os.path.join(REV, "INTERNAL_QC")
MY_POS = os.path.join(IQ, "Q3A_MY_POSITIVE_RESULT.json")
MY_INV = os.path.join(IQ, "Q3B_MY_INVALID_VA_RESULT.json")
EXEC_POS = os.path.join(REV, "POSITIVE", "QC_R4_PINVERIFY_POSITIVE_RESULT.json")
EXEC_INV = os.path.join(REV, "INVALID_VA", "QC_R4_PINVERIFY_INVALID_VA_RESULT.json")
OUT = os.path.join(IQ, "Q3_REGRESSION_REEXECUTION_RESULT.json")

ARTIFACTS = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]


def load(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def my_input_ids(inputs_dir):
    """My OWN reader (same as Q2): enumerate pin identities of a 4-artifact dir."""
    ids = []
    for art in ARTIFACTS:
        doc = load(os.path.join(inputs_dir, art))
        main = doc.get("pins")
        used = None
        if isinstance(main, list) and len(main) > 0:
            used = "pins"
        elif "entry_pins" in doc:
            main = doc.get("entry_pins")
            if isinstance(main, list):
                used = "entry_pins"
        if used is not None:
            for i in range(len(main)):
                ids.append("%s::%s[%d]" % (art, used, i))
        ws = doc.get("width_sources")
        if isinstance(ws, dict):
            for key in sorted(ws.keys()):
                wp = ws[key].get("width_pins") if isinstance(ws[key], dict) else None
                if isinstance(wp, list):
                    for i in range(len(wp)):
                        ids.append("%s::width_sources.%s.width_pins[%d]" % (art, key, i))
    return ids


def bijection(ids, rows):
    row_ids = [r.get("pin_id") for r in rows]
    return {
        "input_count": len(ids),
        "row_count": len(row_ids),
        "input_ids_unique": len(ids) == len(set(ids)),
        "row_ids_unique": len(row_ids) == len(set(row_ids)),
        "counts_equal": len(ids) == len(row_ids),
        "sets_equal": set(ids) == set(row_ids),
        "bijection_ok": (len(ids) == len(set(ids)) and len(row_ids) == len(set(row_ids))
                         and len(ids) == len(row_ids) and set(ids) == set(row_ids)),
    }


def run(label, inputs_dir, output_path):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, VALIDATOR, "--inputs", inputs_dir, "--output", output_path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, env=env)
    pid = proc.pid
    out, err = proc.communicate(timeout=600)
    return {"label": label, "pid": pid, "exit_code": proc.returncode,
            "cmd": cmd, "stdout_tail": (out or "").strip()[-1500:],
            "stderr": (err or "").strip()[:1500]}


def census_of(res):
    c = res.get("census", {})
    sem = c.get("semantic_assertions", {})
    ext = c.get("extra_checks", {})
    return {
        "input_pin_count": c.get("input_pin_count"),
        "processed_count": c.get("processed_count"),
        "verified_ok": c.get("verified_ok"),
        "failed_count": c.get("failed_count"),
        "mismatch_count": c.get("mismatch_count"),
        "error_count": c.get("error_count"),
        "denominator": c.get("denominator"),
        "result_row_count": c.get("result_row_count"),
        "bijection_ok": c.get("bijection_ok"),
        "sem_total": sem.get("total"),
        "sem_ok": sem.get("ok"),
        "sem_failed_list": sem.get("failed_list"),
        "extra_all_required_ok": ext.get("all_required_ok"),
        "extra_required_count": ext.get("required_count"),
        "extra_failed_list": ext.get("failed_list"),
        "overall_ok": c.get("overall_ok"),
        "exe_identity_ok": res.get("exe_identity", {}).get("ok"),
        "exe_measured_sha256": res.get("exe_identity", {}).get("measured_sha256"),
        "run_errors_count": len(res.get("run_errors", [])),
        "run_errors": res.get("run_errors", []),
        "errors_list_count": len(res.get("errors", [])),
    }


def main():
    result = {"q": "Q3_regression_reexecution"}

    pos_proc = run("POSITIVE", RAW, MY_POS)
    inv_proc = run("INVALID_VA", FIXTURE, MY_INV)
    result["my_processes"] = {"positive": pos_proc, "invalid_va": inv_proc}

    my_pos = load(MY_POS)
    my_inv = load(MY_INV)
    exec_pos = load(EXEC_POS)
    exec_inv = load(EXEC_INV)

    pos_census = census_of(my_pos)
    inv_census = census_of(my_inv)
    result["my_positive_census"] = pos_census
    result["my_invalid_va_census"] = inv_census

    # --- expected predicates (contract §4 / §5) on MY OWN re-execution
    pos_expected_ok = (
        pos_proc["exit_code"] == 0
        and pos_census["input_pin_count"] == 185
        and pos_census["processed_count"] == 185
        and pos_census["verified_ok"] == 185
        and pos_census["failed_count"] == 0
        and pos_census["error_count"] == 0
        and pos_census["mismatch_count"] == 0
        and pos_census["denominator"] == 185
        and pos_census["result_row_count"] == 185
        and pos_census["bijection_ok"] is True
        and pos_census["sem_ok"] == 51 and pos_census["sem_total"] == 51
        and pos_census["extra_all_required_ok"] is True
        and pos_census["overall_ok"] is True
        and pos_census["exe_identity_ok"] is True
        and pos_census["run_errors_count"] == 0
    )
    inv_failed_rows = [r for r in my_inv.get("pins", []) if r.get("status") == "FAILED"]
    inv_failed_row = inv_failed_rows[0] if len(inv_failed_rows) == 1 else None
    inv_expected_ok = (
        inv_proc["exit_code"] != 0
        and inv_census["input_pin_count"] == 185
        and inv_census["processed_count"] == 185
        and inv_census["verified_ok"] == 184
        and inv_census["failed_count"] == 1
        and inv_census["error_count"] == 1
        and inv_census["mismatch_count"] == 0
        and inv_census["denominator"] == 185
        and inv_census["result_row_count"] == 185
        and inv_census["bijection_ok"] is True
        and inv_census["sem_ok"] == 51 and inv_census["sem_total"] == 51
        and inv_census["extra_all_required_ok"] is True
        and inv_census["overall_ok"] is False
        and inv_census["exe_identity_ok"] is True
        and inv_census["run_errors_count"] == 0
        and len(inv_failed_rows) == 1
        and inv_failed_row is not None
        and inv_failed_row.get("pin_id") == "BRANCH_SELECTION_TRACE.json::pins[74]"
        and inv_failed_row.get("source") == "BRANCH_SELECTION_TRACE.json"
        and inv_failed_row.get("va") == "0xFFFFFFFF"
        and isinstance(inv_failed_row.get("error"), str)
        and len(inv_failed_row["error"]) > 0
        and inv_failed_row.get("ok") is False
    )
    result["my_positive_regression_pass"] = pos_expected_ok
    result["my_invalid_va_regression_pass"] = inv_expected_ok
    result["my_invalid_va_failed_row"] = {k: inv_failed_row.get(k) for k in
                                          ("pin_id", "source", "va", "status", "ok", "error")} if inv_failed_row else None

    # --- my OWN identity-set bijection (gate R4-G4) in BOTH my re-executions
    raw_ids = my_input_ids(RAW)
    fix_ids = my_input_ids(FIXTURE)
    result["my_bijection_positive"] = bijection(raw_ids, my_pos.get("pins", []))
    result["my_bijection_invalid_va"] = bijection(fix_ids, my_inv.get("pins", []))
    # also against the EXECUTOR's committed rows (same identity sets)
    result["executor_bijection_positive"] = bijection(raw_ids, exec_pos.get("pins", []))
    result["executor_bijection_invalid_va"] = bijection(fix_ids, exec_inv.get("pins", []))

    # --- value-level comparison my re-execution vs executor committed results
    def value_cmp(mine, theirs):
        m = census_of(mine)
        t = census_of(theirs)
        diffs = {}
        for k in m:
            if k in ("sem_failed_list", "extra_failed_list", "run_errors"):
                continue
            if m[k] != t.get(k):
                diffs[k] = {"mine": m[k], "executor": t.get(k)}
        return diffs
    result["value_diffs_positive"] = value_cmp(my_pos, exec_pos)
    result["value_diffs_invalid_va"] = value_cmp(my_inv, exec_inv)

    # executor FAILED row details (for the record)
    exec_failed_rows = [r for r in exec_inv.get("pins", []) if r.get("status") == "FAILED"]
    result["executor_failed_rows"] = [{k: r.get(k) for k in
                                       ("pin_id", "source", "va", "status", "ok", "error")}
                                      for r in exec_failed_rows]

    overall = (pos_expected_ok and inv_expected_ok
               and result["my_bijection_positive"]["bijection_ok"]
               and result["my_bijection_invalid_va"]["bijection_ok"]
               and not result["value_diffs_positive"]
               and not result["value_diffs_invalid_va"])
    result["overall_q3"] = overall

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    # compact console summary
    print(json.dumps({
        "positive": {"exit": pos_proc["exit_code"], "census": pos_census,
                     "pass": pos_expected_ok},
        "invalid_va": {"exit": inv_proc["exit_code"], "census": inv_census,
                       "pass": inv_expected_ok,
                       "failed_row": result["my_invalid_va_failed_row"]},
        "my_bijection_positive": result["my_bijection_positive"],
        "my_bijection_invalid_va": result["my_bijection_invalid_va"],
        "value_diffs_positive": result["value_diffs_positive"],
        "value_diffs_invalid_va": result["value_diffs_invalid_va"],
        "overall_q3": overall}, indent=2))
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
