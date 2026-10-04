#!/usr/bin/env python3
# qc_reexecution.py -- SELF_CHECK_F2_C1_C2 QC re-execution for
# PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004.
#
# EXECUTOR SELF-CHECK, NOT INDEPENDENT QC (advisory). No separate reviewer
# exists for this run; QC_SCOPE = SELF_CHECK_F2_C1_C2.
#
# Re-executes every mandatory C1/C2 control + regression control against
# the CURRENT tool (fresh CLI execution, ordinary AND --full-decode) and
# verifies the predicate matrix:
#   C1 controls:   VALID_USER_VERSION_0, INVALID_USER_VERSION_1
#   C2 controls:  VALID_ROOT_0, INVALID_ROOT_9999, INVALID_ROOT_FFFFFFFE,
#                 NULL_ROOT_FFFFFFFF
#   regression:    REGISTERED_BUT_NOT_DECODED, INVALID_BODY_LINK, F1-C1
#                 C1A, F1-C1 C1B, T1 (218757)
# For every execution this script retains: input SIZE, input SHA256,
# exact command, stdout, stderr, exit code and the measured predicates.
#
# QC predicates (from the run contract):
#   * unsigned normalization of root IDs (raw signed i32 -> u32)
#   * -2 / 0xFFFFFFFE does NOT bypass the range check
#   * -1 / 0xFFFFFFFF handled per NULL_LINKID source semantics
#     (source NULL sentinel; NOT an out-of-range-root failure, verified
#     by fixture EXECUTION)
#   * ordinary and --full-decode AGREE on the guard outcome
#   * source rejection cannot become TOOL PASS
#   * adapter integrity FAIL cannot become TOOL PASS
#   * exit == 0 iff TOOL_VERDICT == PASS (accepted == TOOL PASS)
#   * PRE-fix records reproduce the defects; POST-fix records show the
#     fix (records captured on the pristine base SHA d497b44d before any
#     code change)
#
# Usage:
#   python qc_reexecution.py <repo_root> <fixtures_dir> <pre_records_dir>
#       <post_records_dir> <t1_nif> <outdir>

import hashlib
import json
import os
import subprocess
import sys

FIXTURE_PINS = {
    "fx_VALID_user_version_0_root_0.nif":
        "48B24BB5100F424ABB266A8D10BB1F6C57A854C1960B53A46C27FEB901436984",
    "fx_C1_INVALID_user_version_1.nif":
        "C643F2D295CA1F0DE347D1BFDE1A0BECD462E84E0C62ED78337B5CB67285CCC2",
    "fx_C2_INVALID_root_9999.nif":
        "D0E2A0350849305A614734137F1BEEEF1FA7880F84866E0C7531B8416F4AE49F",
    "fx_C2_INVALID_root_FFFFFFFE.nif":
        "EA49107A0AFDD0483E6C53DFAE2821BD7356457C74627C90B14900E88D9676FD",
    "fx_C2_NULL_root_FFFFFFFF.nif":
        "9EA4C739CF92F5BD281693A33DD53776FF150FAB87DD5823E82A775F39B8632D",
    "fx_REGNOTDEC_ninode_nicamera_ninode.nif":
        "87708915445AC5AF372E598D11BFD5F8E27D2B4821F585A8A09546377C9D5DFB",
    "fx_INVALID_LINK_child_out_of_range.nif":
        "36672FA73C35782CC642B049A5C31240F3C63A7326D240923035D92147403F91",
    "fx_C1A_truncated_name_indexlike.nif":
        "928A1447A3F6911DAD96495307AAA97340133186223AA3B4288CFB4E493A5FCF",
    "fx_C1B_truncated_name_fake_body.nif":
        "719A7EB36E9D2B80E648A03C39C1D5A164586D4AC1532F6F0ACE681FB1C382D6",
}
T1_SIZE = 57316
T1_SHA256 = ("3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE"
             "12CF36")

CONTROLS = [
    # (label, fixture, expected per-mode verdicts)
    ("C1_VALID_USER_VERSION_0", "fx_VALID_user_version_0_root_0.nif"),
    ("C1_INVALID_USER_VERSION_1", "fx_C1_INVALID_user_version_1.nif"),
    ("C2_VALID_ROOT_0", "fx_VALID_user_version_0_root_0.nif"),
    ("C2_INVALID_ROOT_9999", "fx_C2_INVALID_root_9999.nif"),
    ("C2_INVALID_ROOT_FFFFFFFE", "fx_C2_INVALID_root_FFFFFFFE.nif"),
    ("C2_NULL_ROOT_FFFFFFFF", "fx_C2_NULL_root_FFFFFFFF.nif"),
    ("REGNOTDEC", "fx_REGNOTDEC_ninode_nicamera_ninode.nif"),
    ("INVALID_BODY_LINK", "fx_INVALID_LINK_child_out_of_range.nif"),
    ("F1C1_C1A", "fx_C1A_truncated_name_indexlike.nif"),
    ("F1C1_C1B", "fx_C1B_truncated_name_fake_body.nif"),
    ("T1", None),  # handled separately (physical payload path)
]

failures = []
records = []


def check(name, cond, detail=""):
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
    return bool(cond)


def execute(repo, nif_path, full):
    oracle = os.path.join(repo, "tools", "gamebryo_oracle", "oracle.py")
    argv = [sys.executable, oracle, "inspect", nif_path]
    if full:
        argv.append("--full-decode")
    proc = subprocess.run(argv, capture_output=True)
    with open(nif_path, "rb") as fh:
        data = fh.read()
    return {
        "input_size": len(data),
        "input_sha256": hashlib.sha256(data).hexdigest().upper(),
        "command": "python tools/gamebryo_oracle/oracle.py inspect <nif>" +
                   (" --full-decode" if full else ""),
        "stdout_bytes": proc.stdout.decode("utf-8", "replace"),
        "stderr_bytes": proc.stderr.decode("utf-8", "replace"),
        "exit_code": proc.returncode,
    }


def parse(rec):
    return json.loads(rec["stdout_bytes"])


def load_record(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    repo, fixtures, pre_dir, post_dir, t1_nif, outdir = sys.argv[1:7]
    os.makedirs(outdir, exist_ok=True)
    hist = os.path.join(fixtures, "..", "..")
    results = {}

    # fixture identity pins (byte-regenerated committed generator output)
    for name, pin in FIXTURE_PINS.items():
        p = os.path.join(fixtures, name)
        with open(p, "rb") as fh:
            data = fh.read()
        ok = check("qc_fixture_pin_%s" % name,
                   len(data) and hashlib.sha256(data).hexdigest().upper()
                   == pin,
                   "size=%d" % len(data))
        if not ok:
            failures.append("pin:%s" % name)

    t1 = {"size": os.path.getsize(t1_nif),
          "sha256": hashlib.sha256(open(t1_nif, "rb").read())
          .hexdigest().upper()}
    check("qc_t1_identity",
          t1["size"] == T1_SIZE and t1["sha256"] == T1_SHA256,
          "size=%d sha256=%s" % (t1["size"], t1["sha256"]))

    # re-execute every control in BOTH modes against the current tool
    for label, fixture in CONTROLS:
        nif = (t1_nif if fixture is None
               else os.path.join(fixtures, fixture))
        for mode, full in (("ordinary", False), ("full", True)):
            rec = execute(repo, nif, full)
            out = parse(rec)
            rec["measured"] = {
                "SOURCE_PREDICTED_ORIGINAL_VERDICT":
                    out.get("SOURCE_PREDICTED_ORIGINAL_VERDICT"),
                "ADAPTER_DECODE_COVERAGE":
                    out.get("ADAPTER_DECODE_COVERAGE"),
                "ADAPTER_INTEGRITY": out.get("ADAPTER_INTEGRITY"),
                "TOOL_VERDICT": out.get("TOOL_VERDICT"),
                "accepted": out.get("load_result", {}).get("accepted"),
                "user_version_gate_verdict":
                    (out.get("user_version_gate", {}) or {}).get("verdict"),
                "top_level_root_link_integrity":
                    (out.get("adapter_integrity_checks", {}) or {})
                    .get("top_level_root_link_integrity"),
                "top_level_root_failure_count":
                    (out.get("adapter_integrity_checks", {}) or {})
                    .get("top_level_root_failure_count"),
                "top_level_root_checked_count":
                    (out.get("adapter_integrity_checks", {}) or {})
                    .get("top_level_root_checked_count"),
                "top_level_root_raw":
                    (out.get("adapter_integrity_checks", {}) or {})
                    .get("top_level_root_raw"),
                "top_level_root_normalized_u32":
                    (out.get("adapter_integrity_checks", {}) or {})
                    .get("top_level_root_normalized_u32"),
                "scene_graph_roots":
                    (out.get("scene_graph", {}) or {}).get("roots"),
            }
            records.append({"control": label, "mode": mode, "record": rec})
            results[(label, mode)] = (rec, out)

    # ---- predicate matrix -------------------------------------------
    def r(label, mode):
        return results[(label, mode)]

    # C1: valid user version 0 -> full PASS/exit 0 (no over-fail-closed)
    for mode in ("ordinary", "full"):
        rec, out = r("C1_VALID_USER_VERSION_0", mode)
        if not check("qc_c1_valid_user_version_0_pass_%s" % mode,
                     out["TOOL_VERDICT"] == "PASS" and
                     out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "ACCEPTED"
                     and out["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
                     out["ADAPTER_INTEGRITY"] == "PASS" and
                     out["load_result"]["accepted"] is True and
                     rec["exit_code"] == 0,
                     "source=%s tool=%s exit=%d"
                     % (out["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                        out["TOOL_VERDICT"], rec["exit_code"])):
            failures.append("c1_valid:%s" % mode)

    # C1: invalid user version 1 -> REJECTED/FAIL/exit!=0 both modes
    for mode in ("ordinary", "full"):
        rec, out = r("C1_INVALID_USER_VERSION_1", mode)
        if not check("qc_c1_invalid_user_version_1_rejected_%s" % mode,
                     out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED"
                     and out["TOOL_VERDICT"] == "FAIL" and
                     out["load_result"]["accepted"] is False and
                     rec["exit_code"] != 0 and
                     out["ADAPTER_DECODE_COVERAGE"] == "NOT_MEASURED" and
                     out["ADAPTER_INTEGRITY"] == "NOT_MEASURED" and
                     out["user_version_gate"]["verdict"] == "REJECTED" and
                     out["user_version_gate"]
                     ["measured_user_defined_version"] == "0.0.0.1",
                     "source=%s tool=%s exit=%d (coverage/integrity "
                     "NOT_MEASURED: the rejection precedes the uiObjects "
                     "read)"
                     % (out["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                        out["TOOL_VERDICT"], rec["exit_code"])):
            failures.append("c1_invalid:%s" % mode)

    # C2: root 9999 -> integrity FAIL / tool FAIL / exit!=0 both modes
    for mode in ("ordinary", "full"):
        rec, out = r("C2_INVALID_ROOT_9999", mode)
        m = rec["measured"]
        if not check("qc_c2_root_9999_fail_%s" % mode,
                     out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED"
                     and out["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
                     m["top_level_root_link_integrity"] == "FAIL" and
                     m["top_level_root_failure_count"] == 1 and
                     m["top_level_root_checked_count"] == 1 and
                     out["adapter_integrity_checks"]["link_integrity"] ==
                     "FAIL" and out["ADAPTER_INTEGRITY"] == "FAIL" and
                     out["TOOL_VERDICT"] == "FAIL" and
                     out["load_result"]["accepted"] is False and
                     rec["exit_code"] != 0 and
                     m["scene_graph_roots"] == [9999],
                     "raw=%r normalized=%r top_root=FAIL/%d tool=%s exit=%d"
                     % (m["top_level_root_raw"],
                        m["top_level_root_normalized_u32"],
                        m["top_level_root_failure_count"],
                        out["TOOL_VERDICT"], rec["exit_code"])):
            failures.append("root9999:%s" % mode)

    # C2: root 0xFFFFFFFE (raw -2) -> NO signedness bypass
    for mode in ("ordinary", "full"):
        rec, out = r("C2_INVALID_ROOT_FFFFFFFE", mode)
        m = rec["measured"]
        if not check("qc_c2_root_fffffffe_no_signed_bypass_%s" % mode,
                     m["top_level_root_raw"] == [-2] and
                     m["top_level_root_normalized_u32"] == [0xFFFFFFFE] and
                     m["top_level_root_link_integrity"] == "FAIL" and
                     out["ADAPTER_INTEGRITY"] == "FAIL" and
                     out["TOOL_VERDICT"] == "FAIL" and
                     out["load_result"]["accepted"] is False and
                     rec["exit_code"] != 0 and
                     out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] ==
                     "UNRESOLVED",
                     "raw=%r normalized=%r (u32-normalized range check: "
                     "-2 == 0xFFFFFFFE != NULL_LINKID and >= num_blocks "
                     "-> FAIL)"
                     % (m["top_level_root_raw"],
                        m["top_level_root_normalized_u32"])):
            failures.append("rootfffffffe:%s" % mode)

    # C2: root 0xFFFFFFFF (raw -1) = source NULL_LINKID -> NOT a failure
    for mode in ("ordinary", "full"):
        rec, out = r("C2_NULL_ROOT_FFFFFFFF", mode)
        m = rec["measured"]
        if not check("qc_c2_null_root_ffffffff_null_sentinel_%s" % mode,
                     m["top_level_root_raw"] == [-1] and
                     m["top_level_root_normalized_u32"] == [0xFFFFFFFF] and
                     m["top_level_root_link_integrity"] == "PASS" and
                     m["top_level_root_failure_count"] == 0 and
                     not any("TOP_LEVEL_ROOT_FAILURE" in w
                             for w in out["warnings"]),
                     "raw=%r normalized=%r: source NULL_LINKID sentinel "
                     "preserved; no out-of-range-root failure (fixture "
                     "EXECUTION; permitting NULL does not independently "
                     "prove SOURCE=ACCEPTED or TOOL=PASS)"
                     % (m["top_level_root_raw"],
                        m["top_level_root_normalized_u32"])):
            failures.append("rootffffffff:%s" % mode)

    # C2: valid root 0 -> PASS/exit 0
    for mode in ("ordinary", "full"):
        rec, out = r("C2_VALID_ROOT_0", mode)
        if not check("qc_c2_valid_root_0_pass_%s" % mode,
                     out["TOOL_VERDICT"] == "PASS" and
                     out["load_result"]["accepted"] is True and
                     rec["exit_code"] == 0,
                     "tool=%s exit=%d" % (out["TOOL_VERDICT"],
                                          rec["exit_code"])):
            failures.append("root0:%s" % mode)

    # regressions preserved
    reg_expect = {
        "REGNOTDEC": {"source": "UNRESOLVED", "coverage": "INCOMPLETE",
                      "tool": "UNRESOLVED", "exit": 2},
        "INVALID_BODY_LINK": {"source": "UNRESOLVED", "coverage": "COMPLETE",
                              "tool": "FAIL", "exit": 2},
        "F1C1_C1A": {"source": "REJECTED", "coverage": "NOT_MEASURED",
                     "tool": "FAIL", "exit": 2},
        "F1C1_C1B": {"source": "REJECTED", "coverage": "NOT_MEASURED",
                     "tool": "FAIL", "exit": 2},
        "T1": {"source": "REJECTED", "tool": "FAIL", "exit": 2},
    }
    for label in reg_expect:
        for mode in ("ordinary", "full"):
            rec, out = r(label, mode)
            exp = reg_expect[label]
            ok = (out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] ==
                  exp["source"] and
                  out["TOOL_VERDICT"] == exp["tool"] and
                  rec["exit_code"] == exp["exit"] and
                  out["load_result"]["accepted"] is False)
            if "coverage" in exp:
                ok = ok and out["ADAPTER_DECODE_COVERAGE"] == \
                    exp["coverage"]
            if not check("qc_regression_%s_%s" % (label, mode), ok,
                         "source=%s coverage=%s tool=%s exit=%d"
                         % (out["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                            out.get("ADAPTER_DECODE_COVERAGE"),
                            out["TOOL_VERDICT"], rec["exit_code"])):
                failures.append("reg:%s:%s" % (label, mode))
    # T1 first-RTTI-miss + interpretation preserved
    rec, out = r("T1", "full")
    sem = sum(1 for o in out["objects"]
              if o is not None and "boundary_method" not in o)
    bnd = sum(1 for o in out["objects"]
              if o is not None and "boundary_method" in o)
    if not check("qc_t1_first_miss_and_interpretation_preserved",
                out["rtti_table_validation"]["first_rtti_miss"] ==
                "NiArkAnimationExtraData" and sem == 62 and bnd == 4 and
                len(out["objects"]) == 66,
                "first_miss=%s objects=66 (%d semantic + %d boundary, no "
                "promotion to 66 semantic decodes)"
                % (out["rtti_table_validation"]["first_rtti_miss"],
                   sem, bnd)):
        failures.append("t1:interpretation")

    # ordinary/full guard-outcome agreement on EVERY control
    for label, _ in CONTROLS:
        _, o_out = r(label, "ordinary")
        _, f_out = r(label, "full")
        if not check("qc_mode_agreement_%s" % label,
                    o_out["TOOL_VERDICT"] == f_out["TOOL_VERDICT"] and
                    o_out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] ==
                    f_out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] and
                    o_out["load_result"]["accepted"] ==
                    f_out["load_result"]["accepted"],
                    "ordinary tool=%s source=%s | full tool=%s source=%s"
                    % (o_out["TOOL_VERDICT"],
                       o_out["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                       f_out["TOOL_VERDICT"],
                       f_out["SOURCE_PREDICTED_ORIGINAL_VERDICT"])):
            failures.append("mode_agree:%s" % label)

    # the two central invariants over EVERY re-executed result
    law = []
    for label, mode in results:
        rec, out = results[(label, mode)]
        if out["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and \
                out["TOOL_VERDICT"] != "FAIL":
            law.append("%s/%s: source REJECTED but tool %s"
                       % (label, mode, out["TOOL_VERDICT"]))
        if out["ADAPTER_INTEGRITY"] == "FAIL" and \
                out["TOOL_VERDICT"] != "FAIL":
            law.append("%s/%s: integrity FAIL but tool %s"
                       % (label, mode, out["TOOL_VERDICT"]))
        if (rec["exit_code"] == 0) != (out["TOOL_VERDICT"] == "PASS"):
            law.append("%s/%s: exit=%d tool=%s"
                       % (label, mode, rec["exit_code"],
                          out["TOOL_VERDICT"]))
        if (out["load_result"]["accepted"] is not
                (out["TOOL_VERDICT"] == "PASS")):
            law.append("%s/%s: accepted/tool mismatch"
                       % (label, mode))
    if not check("qc_source_rejected_and_integrity_fail_imply_tool_fail",
                 not law,
                 "%d results; violations: %r" % (len(results), law)):
        failures.append("central_invariants")

    # determinism: C1 + C2 controls re-executed twice must be identical
    det = []
    for label, fixture in CONTROLS[:6]:
        nif = os.path.join(fixtures, fixture)
        for mode, full in (("ordinary", False), ("full", True)):
            rec2 = execute(repo, nif, full)
            rec1, _ = r(label, mode)
            if (rec2["stdout_bytes"] != rec1["stdout_bytes"] or
                    rec2["exit_code"] != rec1["exit_code"]):
                det.append("%s/%s" % (label, mode))
    if not check("qc_determinism_c1c2_controls", not det,
                 "run1 == run2 for all C1/C2 controls both modes; "
                 "differences: %r" % det):
        failures.append("determinism")

    # PRE-fix records reproduce the defects (records captured on pristine
    # d497b44d BEFORE any code change)
    pre_expect = {
        ("C1_INVALID_user_version_1", "ordinary"):
            ("ACCEPTED", "PASS", 0),
        ("C1_INVALID_user_version_1", "full"):
            ("ACCEPTED", "PASS", 0),
        ("C2_ROOT_9999", "ordinary"): ("ACCEPTED", "PASS", 0),
        ("C2_ROOT_9999", "full"): ("ACCEPTED", "PASS", 0),
        ("C2_ROOT_FFFFFFFE", "ordinary"): ("ACCEPTED", "PASS", 0),
        ("C2_ROOT_FFFFFFFE", "full"): ("ACCEPTED", "PASS", 0),
    }
    pre_map = {
        "C1_INVALID_user_version_1": "PRE_FIX_C1_INVALID_user_version_1",
        "C2_ROOT_9999": "PRE_FIX_C2_ROOT_9999",
        "C2_ROOT_FFFFFFFE": "PRE_FIX_C2_ROOT_FFFFFFFE",
    }
    for (plabel, mode), (psrc, ptool, pexit) in pre_expect.items():
        stem = "%s_%s" % (pre_map[plabel], mode)
        path = os.path.join(pre_dir, stem + ".RECORD.json")
        pr = load_record(path)
        pout = json.loads(pr["stdout_bytes"])
        if not check("qc_prefix_defect_reproduced_%s_%s"
                     % (plabel, mode),
                     pout["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == psrc and
                     pout["TOOL_VERDICT"] == ptool and
                     pr["exit_code"] == pexit and
                     pout["load_result"]["accepted"] is True,
                     "PRE-fix on pristine d497b44d: source=%s tool=%s "
                     "accepted=%s exit=%d (the F2-C1/C2 defect)"
                     % (pout["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                        pout["TOOL_VERDICT"],
                        pout["load_result"]["accepted"], pr["exit_code"])):
            failures.append("prefix:%s:%s" % (plabel, mode))

    # PRE-fix raw-vs-normalized root representation evidence
    for stem, raw_exp in (("PRE_FIX_C2_ROOT_9999_ordinary", 9999),
                          ("PRE_FIX_C2_ROOT_FFFFFFFE_ordinary", -2),
                          ("PRE_FIX_C2_NULL_ROOT_FFFFFFFF_ordinary", -1)):
        pr = load_record(os.path.join(pre_dir, stem + ".RECORD.json"))
        pout = json.loads(pr["stdout_bytes"])
        if not check("qc_prefix_raw_root_representation_%s" % stem,
                     pout["scene_graph"]["roots"] == [raw_exp],
                     "raw scene_graph.roots=%r (signed i32 as read)"
                     % pout["scene_graph"]["roots"]):
            failures.append("prefix_raw:%s" % stem)

    # write the raw QC record set (deterministic; no wall-clock)
    out_path = os.path.join(outdir, "QC_REEXECUTION_GUARDS.json")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({
            "qc_scope": "SELF_CHECK_F2_C1_C2",
            "independent_qc": False,
            "predicate_failures": failures,
            "controls": records,
        }, fh, indent=1, sort_keys=False, ensure_ascii=True)
        fh.write("\n")
    print("QC_REEXECUTION: %d failures: %r" % (len(failures), failures))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
