#!/usr/bin/env python3
# qc_reexecution.py -- SELF_CHECK_F1_C1 QC re-execution for
# PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003.
#
# Re-executes BOTH mandatory counterexample classes against the FINAL code
# through the ORACLE CLI (subprocess, independent of the in-memory battery)
# and verifies every POST-FIX requirement of the contract:
#   - accepted=false, error_code=RTTIError, first_rtti_miss = the EARLIER
#     miss, full_table_read=false, extension halted (STOP_AT_TABLE_FAILURE),
#     objects=[], no object_reference_histogram, no object_reference_census,
#     structured JSON emitted, exit != 0;
#   - STOP_AT_TABLE_FAILURE distinguishable from
#     CONTINUE_FROM_UNKNOWN_OFFSET (no continuation artifacts at all);
#   - ordinary-mode semantics UNCHANGED (ordinary outputs byte-identical
#     pre/post fix on the same fixture bytes);
#   - the in-memory battery fixtures == the package-generator physical
#     files (byte identity, SIZE+SHA256);
#   - the PRE-FIX raw records demonstrate the defect classes (C1A
#     traceback/IndexError with lost JSON; C1B spurious object).
#
# QC_SCOPE = SELF_CHECK_F1_C1 (no independent reviewer available; this is
# the executor's own re-execution, NOT independent QC).
#
# Usage (from the repo root):
#   python docs/audits/PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003/\
# 03_QC_SELF_CHECK/qc_reexecution.py

import hashlib
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
PKG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FIXDIR = os.path.join(PKG, "01_FIXTURES")
RAWDIR = os.path.join(PKG, "02_RAW_TESTS")
QCDIR = os.path.join(PKG, "03_QC_SELF_CHECK")
ORACLE = os.path.join(REPO, "tools", "gamebryo_oracle", "oracle.py")

CHECKS = []


def check(name, cond, detail=""):
    CHECKS.append({"check": name, "pass": bool(cond), "detail": detail})
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))


def run_cli(nif, full):
    cmd = [sys.executable, ORACLE, "inspect", nif]
    if full:
        cmd.append("--full-decode")
    p = subprocess.run(cmd, capture_output=True)
    return {
        "exit_code": p.returncode,
        "stdout": p.stdout.decode("utf-8", "replace"),
        "stderr": p.stderr.decode("utf-8", "replace"),
    }


def main():
    out = {
        "qc_scope": "SELF_CHECK_F1_C1",
        "note": "executor self-check re-execution; NOT independent QC",
    }

    # ---- 1. battery fixture bytes == package generator files ----------
    sys.path.insert(0, os.path.join(REPO, "tools", "gamebryo_oracle",
                                    "tests"))
    import test_gb12  # noqa: E402
    fx = test_gb12._f1c1_fixtures()
    for key, fname in (("C1A", "fx_C1A_truncated_name_indexlike.nif"),
                      ("C1B", "fx_C1B_truncated_name_fake_body.nif")):
        phys = open(os.path.join(FIXDIR, fname), "rb").read()
        check("fixture_bytes_%s_battery_eq_generator" % key,
              fx[key] == phys,
              "size=%d sha256=%s" % (len(phys),
                                     hashlib.sha256(phys).hexdigest().upper()))

    # ---- 2. counterexample POST-FIX re-execution (CLI) ----------------
    for key, fname in (("C1A", "fx_C1A_truncated_name_indexlike.nif"),
                       ("C1B", "fx_C1B_truncated_name_fake_body.nif")):
        nif = os.path.join(FIXDIR, fname)
        ro = run_cli(nif, False)
        rf = run_cli(nif, True)
        jo = json.loads(ro["stdout"])
        jf = json.loads(rf["stdout"])
        tv = jf["rtti_table_validation"]
        halt = tv.get("extension_halt", {})
        check("ce_%s_full_structured_json_emitted_exit_ne0" % key,
              rf["exit_code"] != 0 and jf["schema"].startswith(
                  "gamebryo_oracle/oracle_result"),
              "exit=%d" % rf["exit_code"])
        check("ce_%s_full_verdict" % key,
              jf["load_result"]["accepted"] is False and
              jf["load_result"]["error_code"] == "RTTIError" and
              "RTTIError(NiDesktopFirstMissing)" in
              jf["load_result"]["error"],
              "error=%r" % jf["load_result"]["error"])
        check("ce_%s_full_keeps_earlier_miss_and_table_state" % key,
              tv["first_rtti_miss"] == "NiDesktopFirstMissing" and
              tv["first_miss_table_index"] == 1 and
              tv["names_read"] == 2 and
              tv["full_table_read"] is False and
              tv["source_predicted_verdict"] == "REJECTED",
              "first=%r@%d names_read=%d" % (
                  tv["first_rtti_miss"], tv["first_miss_table_index"],
                  tv["names_read"]))
        check("ce_%s_full_halt_marker" % key,
              halt.get("marker") == "STOP_AT_TABLE_FAILURE" and
              halt.get("table_boundary_determined") is False and
              jf.get("extension_halt") == "STOP_AT_TABLE_FAILURE" and
              "NOT CONTINUE_FROM_UNKNOWN_OFFSET" in
              halt.get("continuation", ""),
              "marker=%r" % halt.get("marker"))
        check("ce_%s_full_no_object_data_read" % key,
              jf["objects"] == [] and
              "object_reference_histogram" not in jf and
              "object_reference_census" not in jf and
              "object_groups" not in jf and
              jf["type_histogram"] == {} and
              jf["scene_graph"]["roots"] == [] and
              "object_count_check" not in jf,
              "objects/histogram/census/groups/roots/count_check absent")
        check("ce_%s_full_no_index_stage_continuation" % key,
              not any("EXTENDED_INSPECTION_HALTED" in w
                      for w in jf["warnings"]) and
              any("EXTENDED_TABLE_READ_FAILED" in w
                  for w in jf["warnings"]) and
              any("EXTENSION_HALT: STOP_AT_TABLE_FAILURE" in w
                  for w in jf["warnings"]),
              "no index-stage halt warning; table-failure halt present")
        check("ce_%s_ordinary_unchanged" % key,
              jo["load_result"]["error_code"] == "RTTIError" and
              jo["objects"] == [] and
              "extension_halt" not in jo and
              "extension_halt" not in jo["rtti_table_validation"] and
              ro["exit_code"] != 0,
              "ordinary stops at the first miss; no halt markers")

    # ---- 3. ordinary outputs byte-identical pre/post fix ---------------
    for key in ("C1A", "C1B"):
        pre = json.load(open(os.path.join(
            RAWDIR, "PRE_FIX_%s_ordinary.RECORD.json" % key),
            encoding="utf-8"))
        post = json.load(open(os.path.join(
            RAWDIR, "POST_FIX_%s_ordinary.RECORD.json" % key),
            encoding="utf-8"))
        same = (pre["stdout_bytes"] == post["stdout_bytes"] and
                pre["exit_code"] == post["exit_code"])
        check("ce_%s_ordinary_bytes_identical_pre_post_fix" % key, same,
              "exit pre=%d post=%d" % (pre["exit_code"],
                                       post["exit_code"]))

    # ---- 4. PRE-FIX records demonstrate the defect classes ------------
    preA = json.load(open(os.path.join(
        RAWDIR, "PRE_FIX_C1A_full_decode.RECORD.json"), encoding="utf-8"))
    check("prefix_C1A_traceback_reproduced",
          preA["exit_code"] == 1 and preA["stdout_bytes"] == "" and
          "IndexError" in preA["stderr_bytes"] and
          "type_names[ix]" in preA["stderr_bytes"],
          "exit=1, empty stdout, IndexError at type_names[ix]")
    preB = json.load(open(os.path.join(
        RAWDIR, "PRE_FIX_C1B_full_decode.RECORD.json"), encoding="utf-8"))
    jb = json.loads(preB["stdout_bytes"])
    check("prefix_C1B_spurious_object_reproduced",
          preB["exit_code"] == 2 and len(jb["objects"]) == 1 and
          jb["objects"][0]["type"] == "NiNode" and
          jb["scene_graph"]["roots"] == [0] and
          "object_reference_histogram" in jb and
          "object_reference_census" in jb and
          "object_groups" in jb,
          "spurious NiNode + histogram/census/groups/roots from the "
          "unfinished name bytes")

    # ---- 5. fixture F delta (expected, F1-C1-justified) ----------------
    postF = json.load(open(os.path.join(
        RAWDIR, "POST_FIX_F_full_decode.RECORD.json"), encoding="utf-8"))
    jf = json.loads(postF["stdout_bytes"])
    check("fx_F_full_now_halts_at_table_failure",
          postF["exit_code"] == 2 and
          jf["rtti_table_validation"]["extension_halt"]["marker"] ==
          "STOP_AT_TABLE_FAILURE" and
          jf["load_result"]["error_code"] == "RTTIError" and
          jf["rtti_table_validation"]["first_rtti_miss"] == "NiXyzzyx" and
          jf["objects"] == [],
          "F fixture full-decode halts at the table failure (pre-C1: "
          "index-stage halt after reading at EOF from the unknown "
          "boundary)")

    out["checks"] = CHECKS
    out["all_pass"] = all(c["pass"] for c in CHECKS)
    out["QC_VERDICT"] = ("SELF_CHECK_QC_PASS" if out["all_pass"]
                         else "SELF_CHECK_QC_FAIL")
    dest = os.path.join(QCDIR, "QC_REEXECUTION_COUNTEREXAMPLES.json")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("QC_VERDICT=%s (%d checks)" % (out["QC_VERDICT"], len(CHECKS)))
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
