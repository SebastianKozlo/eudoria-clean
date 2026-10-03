#!/usr/bin/env python3
# compare_t1_regression.py -- T1/218757 targeted F2 regression for
# PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003.
#
# Verifies on the pinned T1 payload (SIZE 57316 / SHA256 3E8A22C2...,
# read-only, NEVER committed):
#   1. input identity == the pinned SIZE + SHA256 (else BLOCKED_T1_IDENTITY)
#   2. POST-FIX full-decode objects[] is 66/66 DEEP-IDENTICAL to the
#      accepted baseline state (the PRE-FIX ee60930 full-decode result):
#      every field recursively compared (values, transforms, links,
#      byte_start/end/size, status, type/name, everything else)
#   3. interpretation label preserved exactly: 62 known semantically
#      decoded records + 4 opaque/boundary-only records -- NEVER promoted
#      to 66 semantic decodes
#   4. F2 axes for T1 full-decode: SOURCE_PREDICTED_ORIGINAL_VERDICT=
#      REJECTED, TOOL_VERDICT != PASS (FAIL), coverage INCOMPLETE with
#      measured counters (66 header / 62 semantic / 4 boundary / 4
#      unregistered / 0 registered-but-not-decoded)
#   5. F2 axes for T1 ordinary: early RTTI halt -- object-level counters
#      NOT_MEASURED/null (NEVER derived from the RTTI table),
#      FIRST_RTTI_MISS=NiArkAnimationExtraData@1 preserved,
#      SOURCE_PREDICTED=REJECTED, TOOL_VERDICT=FAIL
#   6. determinism: POST run1 == POST run2 (whole JSON)

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

T1_PATH = (r"D:\Eudoria_Reconstruction\99_Audits"
           r"\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads"
           r"\218757.nif")
T1_SIZE = 57316
T1_SHA256 = ("3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE1"
             "2CF36")

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print("[%s] %s %s" % (status, name, detail))
    if not cond:
        FAILURES.append(name)


def deep_diff(a, b, path="$"):
    """Recursive structural difference list between two JSON values."""
    out = []
    if type(a) is not type(b):
        out.append("%s: type %s != %s" % (path, type(a).__name__,
                                          type(b).__name__))
        return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append("%s.%s: only in POST" % (path, k))
            elif k not in b:
                out.append("%s.%s: only in PRE" % (path, k))
            else:
                out.extend(deep_diff(a[k], b[k], "%s.%s" % (path, k)))
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append("%s: len %d != %d" % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(deep_diff(x, y, "%s[%d]" % (path, i)))
    else:
        if a != b:
            out.append("%s: %r != %r" % (path, a, b))
    return out


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    # 1. pinned input identity
    with open(T1_PATH, "rb") as fh:
        data = fh.read()
    sha = hashlib.sha256(data).hexdigest().upper()
    check("t1_identity_pinned", len(data) == T1_SIZE and sha == T1_SHA256,
          "size=%d sha256=%s" % (len(data), sha))
    if len(data) != T1_SIZE or sha != T1_SHA256:
        print("BLOCKED_T1_IDENTITY")
        return 1

    pre_full = load(os.path.join(HERE, "T1_gb12_full_PRE_FIX_run1.json"))
    post1 = load(os.path.join(HERE, "T1_gb12_full_POST_FIX_run1.json"))
    post2 = load(os.path.join(HERE, "T1_gb12_full_POST_FIX_run2.json"))
    post_ord = load(os.path.join(HERE, "T1_gb12_ordinary_POST_FIX.json"))

    # 2/3. objects[] deep identity 66/66
    pre_objs = pre_full["objects"]
    post_objs = post1["objects"]
    check("t1_full_objects_66",
          len(pre_objs) == 66 and len(post_objs) == 66,
          "pre=%d post=%d" % (len(pre_objs), len(post_objs)))
    diffs = []
    for i, (a, b) in enumerate(zip(pre_objs, post_objs)):
        d = deep_diff(a, b, "$.objects[%d]" % i)
        diffs.extend(d)
    check("t1_full_objects_deep_identical", not diffs,
          "diffs=%s" % (diffs[:5] if diffs else "NONE"))
    sem = sum(1 for o in post_objs
              if o is not None and "boundary_method" not in o)
    bnd = sum(1 for o in post_objs
              if o is not None and "boundary_method" in o)
    check("t1_interpretation_label_preserved",
          sem == 62 and bnd == 4 and
          post1["rtti_table_validation"]["first_rtti_miss"] ==
          "NiArkAnimationExtraData" and
          post1["rtti_table_validation"]["source_predicted_verdict"] ==
          "REJECTED",
          "62 known semantically decoded + 4 opaque/boundary-only "
          "(NOT promoted to 66 semantic decodes); first_rtti_miss=%s@%s"
          % (post1["rtti_table_validation"]["first_rtti_miss"],
             post1["rtti_table_validation"]["first_miss_table_index"]))

    # 4. F2 axes, full-decode
    c = post1["adapter_decode_coverage_counters"]
    ic = post1["adapter_integrity_checks"]
    check("t1_full_f2_axes",
          post1["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
          post1["TOOL_VERDICT"] != "PASS" and
          post1["TOOL_VERDICT"] == "FAIL" and
          post1["ADAPTER_DECODE_COVERAGE"] == "INCOMPLETE" and
          c["header_num_blocks"] == 66 and
          c["semantically_decoded_blocks"] == 62 and
          c["boundary_only_blocks"] == 4 and
          c["unregistered_blocks"] == 4 and
          c["registered_but_not_decoded_blocks"] == 0 and
          c["unresolved_blocks"] == 0 and
          post1["load_result"]["accepted"] is False,
          "SRC=%s COV=%s TOOL=%s counters=%s" % (
              post1["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
              post1["ADAPTER_DECODE_COVERAGE"], post1["TOOL_VERDICT"],
              {k: c[k] for k in ("header_num_blocks",
                                 "semantically_decoded_blocks",
                                 "boundary_only_blocks",
                                 "unregistered_blocks",
                                 "registered_but_not_decoded_blocks")}))
    check("t1_full_integrity_partial_link_measure",
          post1["ADAPTER_INTEGRITY"] == "UNRESOLVED" and
          ic["object_count_consistency"] == "PASS" and
          ic["structural_closure"] == "PASS" and
          ic["link_integrity"] == "UNRESOLVED" and
          ic["link_measured_blocks"] == 62 and
          ic["link_failure_count"] == 0,
          "integrity=%s (62/66 blocks' links measured; 4 boundary-only "
          "blocks contribute no link list)"
          % post1["ADAPTER_INTEGRITY"])

    # 5. ordinary mode: early RTTI halt, counters NOT_MEASURED/null
    co = post_ord["adapter_decode_coverage_counters"]
    check("t1_ordinary_f2_early_halt_not_measured",
          post_ord["rtti_table_validation"]["first_rtti_miss"] ==
          "NiArkAnimationExtraData" and
          post_ord["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
          post_ord["TOOL_VERDICT"] == "FAIL" and
          post_ord["ADAPTER_DECODE_COVERAGE"] == "NOT_MEASURED" and
          co["semantically_decoded_blocks"] is None and
          co["boundary_only_blocks"] is None and
          co["registered_but_not_decoded_blocks"] is None and
          co["unregistered_blocks"] is None and
          co["unresolved_blocks"] is None and
          co["header_num_blocks"] == 66 and
          bool(co["not_measured_reasons"]) and
          post_ord["objects"] == [],
          "object-level counters null with reasons (never derived from "
          "the RTTI table); header_num_blocks measured from the header")

    # 6. determinism: post run1 == run2 (whole JSON)
    j1 = json.dumps(post1, sort_keys=True)
    j2 = json.dumps(post2, sort_keys=True)
    check("t1_full_post_run1_equals_run2", j1 == j2,
          "whole-JSON deterministic")

    # whole-JSON delta vs PRE: every difference must be F2 metadata ONLY
    # (the new axis keys + accepted_semantics); ZERO differences allowed
    # anywhere inside objects[] (already deep-checked above)
    top = deep_diff(pre_full, post1)
    obj_diffs = [d for d in top if d.startswith("$.objects")]
    allowed = ("$.SOURCE_", "$.ADAPTER_", "$.TOOL_VERDICT",
               "$.tool_verdict_reason", "$.source_predicted_reason",
               "$.adapter_decode_coverage_counters",
               "$.adapter_integrity_checks",
               "$.load_result.accepted_semantics")
    bad_meta = [d for d in top
                if not d.startswith("$.objects")
                and not d.startswith(allowed)]
    check("t1_whole_json_delta_f2_metadata_only",
          not obj_diffs and not bad_meta,
          "total=%d objects_diffs=%d non_f2_meta_diffs=%d sample=%s"
          % (len(top), len(obj_diffs), len(bad_meta),
             sorted(d.split(":")[0] for d in top)[:8]))

    print("T1_REGRESSION: %d failures: %r" % (len(FAILURES), FAILURES))
    with open(os.path.join(HERE, "T1_REGRESSION_COMPARISON.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump({
            "t1_identity": {"size": len(data), "sha256": sha},
            "objects_deep_identical": not diffs,
            "objects_count": {"pre": len(pre_objs), "post": len(post_objs)},
            "semantic_vs_boundary": {"semantic": sem, "boundary": bnd},
            "f2_full": {
                "SOURCE_PREDICTED_ORIGINAL_VERDICT":
                    post1["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                "ADAPTER_DECODE_COVERAGE": post1["ADAPTER_DECODE_COVERAGE"],
                "counters": {k: c[k] for k in (
                    "header_num_blocks", "semantically_decoded_blocks",
                    "boundary_only_blocks", "unregistered_blocks",
                    "registered_but_not_decoded_blocks",
                    "unresolved_blocks")},
                "ADAPTER_INTEGRITY": post1["ADAPTER_INTEGRITY"],
                "integrity_checks": ic,
                "TOOL_VERDICT": post1["TOOL_VERDICT"],
                "accepted": post1["load_result"]["accepted"],
            },
            "f2_ordinary": {
                "SOURCE_PREDICTED_ORIGINAL_VERDICT":
                    post_ord["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
                "ADAPTER_DECODE_COVERAGE":
                    post_ord["ADAPTER_DECODE_COVERAGE"],
                "counters": co,
                "TOOL_VERDICT": post_ord["TOOL_VERDICT"],
                "first_rtti_miss":
                    post_ord["rtti_table_validation"]["first_rtti_miss"],
                "objects_empty": post_ord["objects"] == [],
            },
            "determinism_run1_run2": j1 == j2,
            "whole_json_delta_paths": sorted(d.split(":")[0] for d in top),
            "failures": FAILURES,
        }, fh, indent=1, sort_keys=False, ensure_ascii=True)
        fh.write("\n")
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
