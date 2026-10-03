#!/usr/bin/env python3
# qc_reexecution.py -- SELF_CHECK_F2 QC re-execution for
# PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003.
#
# QC_SCOPE = SELF_CHECK_F2 (executor self-check; NO independent reviewer --
# this is NOT independent QC). Independence discipline: the EXPECTED
# results below were derived from (a) the pinned GB 1.2 source semantics
# (NiStream.cpp E955C36E: LoadHeader L303-360, LoadRTTI L412-449,
# LoadStream L506-635; GetObjectFromLinkID L245-256 debug-only assert;
# NiTArray.inl L136-139 unchecked GetAt; NiNode.cpp L861-888), (b) the
# 198-class SDM factory census (NiCamera registered, no adapter loader),
# (c) hand-built fixtures generated from the committed generator, and
# (d) the explicit F2 contract -- NEVER from the corrected code itself.
#
# Re-executes through the CLI (input identity, exact command, stdout,
# stderr, exit code, measured predicates) for the mandatory set:
#   VALID_SUPPORTED / REGISTERED_BUT_NOT_DECODED / INVALID_LINK / C1A / C1B
# plus: zero-vs-NOT_MEASURED distinctness, early-halt no-object-census,
# integrity-FAIL => TOOL-FAIL law, inspect exit semantics per F2, and the
# pre/post byte-identity of probe-version / compare / capabilities.

import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(PKG, "..", "..", ".."))
ORACLE = os.path.join(REPO, "tools", "gamebryo_oracle", "oracle.py")
GEN = os.path.join(PKG, "01_FIXTURES", "build_fixtures_f2.py")
# P3 hygiene: regenerated .nif fixtures stay OUTSIDE the published package
# root (repo-wide *.nif policy) -- the QC re-execution uses the run's
# EXTERNAL sandbox, never a package-local directory.
QC_DIR = (r"C:\Users\User\AppData\Local\Temp\opencode"
          r"\PE_GAMEBRYO_ORACLE_F2_20261003\sandbox\qc_rerun_fixtures")

FAILURES = []
RESULTS = {}


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print("[%s] %s %s" % (status, name, detail))
    if not cond:
        FAILURES.append(name)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def run_cli(nif, full=False):
    cmd = [sys.executable, ORACLE, "inspect", nif]
    if full:
        cmd.append("--full-decode")
    proc = subprocess.run(cmd, capture_output=True)
    with open(nif, "rb") as fh:
        data = fh.read()
    return {
        "input_identity": {"path": nif, "size": len(data),
                           "sha256": sha256_bytes(data)},
        "command_argv": cmd,
        "stdout_text": proc.stdout.decode("utf-8", "replace"),
        "stderr_text": proc.stderr.decode("utf-8", "replace"),
        "exit_code": proc.returncode,
    }


def parsed(rec):
    return json.loads(rec["stdout_text"])


def main():
    # ---- 0. regenerate fixtures from the COMMITTED generator ----------
    if os.path.isdir(QC_DIR):
        shutil.rmtree(QC_DIR)
    os.makedirs(QC_DIR)
    proc = subprocess.run([sys.executable, GEN, QC_DIR],
                          capture_output=True)
    check("qc_generator_regenerates", proc.returncode == 0,
          proc.stdout.decode("utf-8", "replace").strip().replace("\n", "; "))

    pins = {
        "fx_VALID_positive.nif": (167,
                                  "48B24BB5100F424ABB266A8D10BB1F6C57A854"
                                  "C1960B53A46C27FEB901436984"),
        "fx_REGNOTDEC_ninode_nicamera_ninode.nif": (285,
                                                    "87708915445AC5AF372E5"
                                                    "98D11BFD5F8E27D2B48"
                                                    "21F585A8A09546377C9D"
                                                    "5DFB"),
        "fx_INVALID_LINK_child_out_of_range.nif": (171,
                                                   "36672FA73C35782CC642B"
                                                   "049A5C31240F3C63A73"
                                                   "26D240923035D92147403"
                                                   "F91"),
        "fx_C1A_truncated_name_indexlike.nif": (94, "928A1447A3F6911DAD96"
                                                "495307AAA973401331862"
                                                "23AA3B4288CFB4E493A5FCF"),
        "fx_C1B_truncated_name_fake_body.nif": (196, "719A7EB36E9D2B80E648"
                                                "A03C39C1D5A164586D4AC15"
                                                "32F6F0ACE681FB1C382D6"),
    }
    for name, (size, sha) in sorted(pins.items()):
        with open(os.path.join(QC_DIR, name), "rb") as fh:
            d = fh.read()
        check("qc_pin_%s" % name, len(d) == size and
              sha256_bytes(d) == sha,
              "size=%d sha=%s" % (len(d), sha256_bytes(d)))

    # battery-fixture byte identity (the committed battery builds the
    # same bytes in-memory; the physical files must match)
    sys.path.insert(0, os.path.join(REPO, "tools", "gamebryo_oracle",
                                    "tests"))
    import test_gb12  # noqa: E402
    bf = test_gb12._f2_fixtures()
    with open(os.path.join(
            QC_DIR, "fx_VALID_positive.nif"), "rb") as fh:
        check("qc_battery_fixture_identity_VALID",
              fh.read() == bf["VALID"])
    with open(os.path.join(
            QC_DIR, "fx_REGNOTDEC_ninode_nicamera_ninode.nif"), "rb") as fh:
        check("qc_battery_fixture_identity_REGNOTDEC",
              fh.read() == bf["REGNOTDEC"])
    with open(os.path.join(
            QC_DIR, "fx_INVALID_LINK_child_out_of_range.nif"), "rb") as fh:
        check("qc_battery_fixture_identity_BADLINK",
              fh.read() == bf["BADLINK"])

    # independent registry census premise (NOT from the corrected code)
    sys.path.insert(0, os.path.join(REPO, "tools", "gamebryo_oracle",
                                    "adapters", "gb12"))
    import registry  # noqa: E402
    import gb12core  # noqa: E402
    check("qc_premise_nicamera_registered_not_loaded",
          registry.is_registered("NiCamera") is True and
          "NiCamera" not in gb12core.LOADERS and
          len(registry.GB12_REGISTERED_CLASSES) == 198 and
          len(gb12core.LOADERS) == 39,
          "NiCamera in 198-class factory census, absent from the 39 "
          "adapter LOADERS")

    # ---- 1. VALID_SUPPORTED -------------------------------------------
    rV = run_cli(os.path.join(QC_DIR, "fx_VALID_positive.nif"))
    jV = parsed(rV)
    RESULTS["VALID_SUPPORTED"] = rV
    check("qc_VALID_supported_pass",
          rV["exit_code"] == 0 and
          jV["load_result"]["accepted"] is True and
          jV["TOOL_VERDICT"] == "PASS" and
          jV["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
          jV["ADAPTER_INTEGRITY"] == "PASS" and
          jV["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "ACCEPTED" and
          rV["stderr_text"] == "",
          "exit=%d accepted=%s tool=%s coverage=%s integrity=%s source=%s"
          % (rV["exit_code"], jV["load_result"]["accepted"],
             jV["TOOL_VERDICT"], jV["ADAPTER_DECODE_COVERAGE"],
             jV["ADAPTER_INTEGRITY"],
             jV["SOURCE_PREDICTED_ORIGINAL_VERDICT"]))

    # ---- 2. REGISTERED_BUT_NOT_DECODED ---------------------------------
    rA = run_cli(os.path.join(
        QC_DIR, "fx_REGNOTDEC_ninode_nicamera_ninode.nif"))
    jA = parsed(rA)
    cA = jA["adapter_decode_coverage_counters"]
    RESULTS["REGISTERED_BUT_NOT_DECODED"] = rA
    check("qc_REGISTERED_BUT_NOT_DECODED_no_false_success",
          rA["exit_code"] != 0 and
          jA["load_result"]["accepted"] is False and
          jA["TOOL_VERDICT"] != "PASS" and
          jA["ADAPTER_DECODE_COVERAGE"] == "INCOMPLETE" and
          cA["registered_but_not_decoded_blocks"] == 1 and
          cA["semantically_decoded_blocks"] == 2 and
          cA["boundary_only_blocks"] == 1 and
          cA["header_num_blocks"] == 3 and
          jA["ADAPTER_INTEGRITY"] == "UNRESOLVED" and
          jA["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED" and
          cA.get("registered_but_not_decoded_classes") == ["NiCamera"] and
          registry.is_registered("NiCamera") is True,
          "exit=%d accepted=%s tool=%s coverage=%s rnd_blocks=%s "
          "factory_registration=YES (registry census) source=%s"
          % (rA["exit_code"], jA["load_result"]["accepted"],
             jA["TOOL_VERDICT"], jA["ADAPTER_DECODE_COVERAGE"],
             cA["registered_but_not_decoded_blocks"],
             jA["SOURCE_PREDICTED_ORIGINAL_VERDICT"]))

    # ---- 3. INVALID_LINK -----------------------------------------------
    rB = run_cli(os.path.join(
        QC_DIR, "fx_INVALID_LINK_child_out_of_range.nif"))
    jB = parsed(rB)
    iB = jB["adapter_integrity_checks"]
    RESULTS["INVALID_LINK"] = rB
    check("qc_INVALID_LINK_no_false_success",
          rB["exit_code"] != 0 and
          jB["load_result"]["accepted"] is False and
          jB["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
          iB["link_integrity"] == "FAIL" and
          iB["link_failure_count"] == 1 and
          jB["ADAPTER_INTEGRITY"] == "FAIL" and
          jB["TOOL_VERDICT"] == "FAIL" and
          jB["TOOL_VERDICT"] != "UNRESOLVED" and
          jB["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED" and
          any("LINK_FAILURE" in w for w in jB["warnings"]),
          "exit=%d accepted=%s coverage=%s links=%s integrity=%s tool=%s "
          "source=%s (known invalid link never UNRESOLVED)"
          % (rB["exit_code"], jB["load_result"]["accepted"],
             jB["ADAPTER_DECODE_COVERAGE"], iB["link_integrity"],
             jB["ADAPTER_INTEGRITY"], jB["TOOL_VERDICT"],
             jB["SOURCE_PREDICTED_ORIGINAL_VERDICT"]))

    # ---- 4/5. C1A / C1B (pinned F1-C1 regression bytes) ----------------
    for key, fname in (("C1A", "fx_C1A_truncated_name_indexlike.nif"),
                      ("C1B", "fx_C1B_truncated_name_fake_body.nif")):
        rec_o = run_cli(os.path.join(QC_DIR, fname))
        rec_f = run_cli(os.path.join(QC_DIR, fname), full=True)
        jo = parsed(rec_o)
        jf = parsed(rec_f)
        RESULTS["%s_ordinary" % key] = rec_o
        RESULTS["%s_full" % key] = rec_f
        check("qc_%s_ordinary_preserved" % key,
              rec_o["exit_code"] == 2 and
              jo["load_result"]["error_code"] == "RTTIError" and
              "RTTIError(NiDesktopFirstMissing)" in
              (jo["load_result"]["error"] or "") and
              jo["rtti_table_validation"]["names_read"] == 2 and
              jo["objects"] == [] and
              "object_reference_histogram" not in jo and
              "object_reference_census" not in jo,
              "exit=%d error=%r names_read=%s"
              % (rec_o["exit_code"], jo["load_result"]["error"],
                 jo["rtti_table_validation"]["names_read"]))
        cf = jf["adapter_decode_coverage_counters"]
        check("qc_%s_full_halt_and_not_measured_coverage" % key,
              rec_f["exit_code"] == 2 and
              jf["rtti_table_validation"]["extension_halt"].get(
                  "marker") == "STOP_AT_TABLE_FAILURE" and
              "RTTIError(NiDesktopFirstMissing)" in
              (jf["load_result"]["error"] or "") and
              jf["objects"] == [] and
              jf["ADAPTER_DECODE_COVERAGE"] == "NOT_MEASURED" and
              cf["semantically_decoded_blocks"] is None and
              cf["boundary_only_blocks"] is None and
              cf["registered_but_not_decoded_blocks"] is None and
              cf["unregistered_blocks"] is None and
              cf["unresolved_blocks"] is None and
              bool(cf["not_measured_reasons"]) and
              "object_reference_histogram" not in jf and
              "object_reference_census" not in jf and
              "object_groups" not in jf and
              jf["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
              jf["TOOL_VERDICT"] == "FAIL",
              "exit=%d marker=STOP_AT_TABLE_FAILURE objects=[] "
              "object-level counters null with reasons (never derived "
              "from the RTTI table); source=REJECTED tool=FAIL"
              % rec_f["exit_code"])

    # ---- 6. zero vs NOT_MEASURED never conflated ------------------------
    check("qc_zero_vs_not_measured_distinct",
          cA["unregistered_blocks"] == 0 and
          isinstance(cA["unregistered_blocks"], int) and
          cA["unresolved_blocks"] == 0 and
          isinstance(cA["unresolved_blocks"], int) and
          parsed(RESULTS["C1A_full"])
          ["adapter_decode_coverage_counters"]
          ["semantically_decoded_blocks"] is None and
          parsed(RESULTS["C1A_full"])
          ["adapter_decode_coverage_counters"]
          ["not_measured_reasons"].get(
              "semantically_decoded_blocks"),
          "REGNOTDEC measured zeros are int 0; C1A unknown counters are "
          "None with an explicit reason -- distinct representations")

    # ---- 7. integrity FAIL => TOOL FAIL law + exit semantics ------------
    check("qc_integrity_fail_implies_tool_fail",
          jB["ADAPTER_INTEGRITY"] == "FAIL" and
          jB["TOOL_VERDICT"] == "FAIL" and
          rB["exit_code"] != 0,
          "BADLINK: integrity=FAIL -> tool=FAIL -> exit!=0")
    exit_law = (rV["exit_code"] == 0) == (jV["TOOL_VERDICT"] == "PASS")
    for key in ("REGISTERED_BUT_NOT_DECODED", "C1A_ordinary",
                "C1A_full", "C1B_ordinary", "C1B_full"):
        rec = RESULTS[key]
        exit_law = exit_law and (
            (rec["exit_code"] == 0) ==
            (parsed(rec)["TOOL_VERDICT"] == "PASS"))
    check("qc_inspect_exit_zero_iff_tool_pass", exit_law,
          "for every re-executed record: exit==0 <=> TOOL_VERDICT==PASS "
          "(no default-success fallback)")

    # ---- 8. determinism of the re-execution -----------------------------
    det_ok = True
    for fname in ("fx_VALID_positive.nif",
                  "fx_REGNOTDEC_ninode_nicamera_ninode.nif",
                  "fx_INVALID_LINK_child_out_of_range.nif"):
        a = run_cli(os.path.join(QC_DIR, fname))
        b = run_cli(os.path.join(QC_DIR, fname))
        if a["stdout_text"] != b["stdout_text"] or \
                a["exit_code"] != b["exit_code"]:
            det_ok = False
    check("qc_determinism_reexecution", det_ok,
          "double re-execution: identical stdout + exit on all three "
          "core fixtures")

    # ---- 9. non-inspect CLI pre/post byte identity ----------------------
    snap = [("PRE_FIX_probe_version_fx_VALID.stdout",
             "POST_FIX_probe_version_fx_VALID.stdout"),
            ("PRE_FIX_capabilities_all.stdout",
             "POST_FIX_capabilities_all.stdout"),
            ("PRE_FIX_capabilities_gb12.stdout",
             "POST_FIX_capabilities_gb12.stdout"),
            ("PRE_FIX_compare_pinned.stdout",
             "POST_FIX_compare_pinned.stdout"),
            ("PRE_FIX_compare_internal_inspect.stdout",
             "POST_FIX_compare_internal_inspect.stdout")]
    same = True
    for pre, post in snap:
        with open(os.path.join(HERE, pre), "rb") as fh:
            pa = fh.read()
        with open(os.path.join(HERE, post), "rb") as fh:
            pb = fh.read()
        if pa != pb:
            same = False
    check("qc_non_inspect_cli_unchanged_pre_post", same,
          "probe-version / capabilities (all + gb12) / compare (pinned "
          "pair + internal-inspect pair) outputs byte-identical pre/post")

    # ---- persist --------------------------------------------------------
    out = {
        "QC_SCOPE": "SELF_CHECK_F2",
        "expected_results_derivation": (
            "pinned GB1.2 source semantics + registry census + the "
            "committed generator's pinned bytes + the explicit F2 "
            "contract; NEVER the corrected code"),
        "reexecuted": RESULTS,
        "failures": FAILURES,
    }
    with open(os.path.join(HERE, "QC_REEXECUTION_COUNTEREXAMPLES.json"),
              "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, sort_keys=False, ensure_ascii=True)
        fh.write("\n")
    print("QC_REEXECUTION: %d failures: %r" % (len(FAILURES), FAILURES))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
