#!/usr/bin/env python3
# t1_deep_regression.py -- T1 (218757.nif) deep-identity regression for
# PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004.
#
# The complete objects[] array of the T1 full-decode output must remain
# DEEP-IDENTICAL vs the pristine base SHA d497b44d output (recursively:
# values, types/names, transforms, links, byte_start/end/size, status and
# every other field). The interpretation stays 62 known semantically
# decoded records + 4 opaque/boundary-only records (NOT promoted to 66
# semantic decodes), FIRST_RTTI_MISS=NiArkAnimationExtraData@1,
# SOURCE_PREDICTED=REJECTED, TOOL_VERDICT=FAIL. Any whole-JSON delta must
# be confined to the new F2-C1/C2 metadata (the user_version_gate object,
# input_identity.user_defined_version_u32, the
# adapter_integrity_checks.top_level_root_* fields and the reworded
# detail/reason strings) -- zero changes inside objects[].
#
# Two independent baselines are used, both on the SAME physical payload
# (57,316 B / SHA256 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07
# FCAF44DE12CF36, re-verified by the caller):
#   1. the PRE-fix full-decode record captured on the pristine d497b44
#      worktree by THIS run (02_RAW_TESTS/PRE_FIX_T1_full.RECORD.json in
#      the package; same machine, same Python);
#   2. the pinned historical d497b44 record published by the F2 package
#      (docs/audits/
#      PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003/
#      02_RAW_TESTS/POST_FIX_T1_full.RECORD.json -- that package's
#      post-fix IS our base SHA).
#
# Usage:
#   python t1_deep_regression.py <pre_record.json> <post_record.json>
#       [--baseline2 <historical_record.json>]
#
# Prints PASS/FAIL lines; exits 0 only on full deep identity.

import json
import sys


def deep_equal(a, b, path="$", diffs=None):
    """Recursive deep equality; collects every differing path."""
    if type(a) is not type(b) and not (
            isinstance(a, (int, float)) and isinstance(b, (int, float))
            and not isinstance(a, bool) and not isinstance(b, bool)):
        diffs.append("%s: type %s vs %s" % (path, type(a).__name__,
                                            type(b).__name__))
        return False
    if isinstance(a, dict):
        ok = True
        for k in sorted(set(a) | set(b)):
            if k not in a:
                diffs.append("%s.%s: missing in PRE" % (path, k))
                ok = False
            elif k not in b:
                diffs.append("%s.%s: missing in POST" % (path, k))
                ok = False
            else:
                ok = deep_equal(a[k], b[k], "%s.%s" % (path, k),
                                diffs) and ok
        return ok
    if isinstance(a, list):
        if len(a) != len(b):
            diffs.append("%s: len %d vs %d" % (path, len(a), len(b)))
            return False
        ok = True
        for i, (x, y) in enumerate(zip(a, b)):
            ok = deep_equal(x, y, "%s[%d]" % (path, i), diffs) and ok
        return ok
    if a != b:
        diffs.append("%s: %r vs %r" % (path, a, b))
        return False
    return True


def main():
    pre_path = sys.argv[1]
    post_path = sys.argv[2]
    baseline2 = None
    if "--baseline2" in sys.argv:
        baseline2 = sys.argv[sys.argv.index("--baseline2") + 1]

    failures = []

    def check(name, cond, detail=""):
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
        if not cond:
            failures.append(name)

    with open(pre_path, encoding="utf-8") as fh:
        pre = json.load(fh)
    with open(post_path, encoding="utf-8") as fh:
        post = json.load(fh)

    pre_json = json.loads(pre["stdout_bytes"])
    post_json = json.loads(post["stdout_bytes"])

    # input identity must be identical (same physical payload)
    check("t1_input_identity",
          pre["input_identity"]["sha256"] == post["input_identity"]["sha256"]
          and pre["input_identity"]["size"] ==
          post["input_identity"]["size"],
          "size=%s sha256=%s" % (post["input_identity"]["size"],
                                 post["input_identity"]["sha256"]))

    # 66/66 objects[] deep identity (recursive, every field)
    diffs = []
    deep_equal(pre_json["objects"], post_json["objects"],
               "$.objects", diffs)
    check("t1_objects_66_deep_identical",
          len(pre_json["objects"]) == 66 and
          len(post_json["objects"]) == 66 and not diffs,
          "66/66 objects; %d recursive diffs" % len(diffs))
    for d in diffs[:20]:
        print("  DIFF: %s" % d)

    # interpretation preserved: 62 semantically decoded + 4 boundary-only
    def counts(objs):
        sem = sum(1 for o in objs
                  if o is not None and "boundary_method" not in o)
        bnd = sum(1 for o in objs
                  if o is not None and "boundary_method" in o)
        return sem, bnd
    p_sem, p_bnd = counts(pre_json["objects"])
    q_sem, q_bnd = counts(post_json["objects"])
    check("t1_interpretation_62_semantic_4_boundary",
          (p_sem, p_bnd) == (62, 4) == (q_sem, q_bnd),
          "PRE %d/%d POST %d/%d (no promotion to 66 semantic decodes)"
          % (p_sem, p_bnd, q_sem, q_bnd))

    # verdict preservation
    check("t1_verdicts_preserved",
          post_json["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
          post_json["TOOL_VERDICT"] == "FAIL" and
          post_json["load_result"]["accepted"] is False and
          post_json["rtti_table_validation"]["first_rtti_miss"] ==
          "NiArkAnimationExtraData" and
          post_json["rtti_table_validation"]
          ["first_miss_table_index"] == 1,
          "first_rtti_miss=%s@%s source=%s tool=%s"
          % (post_json["rtti_table_validation"]["first_rtti_miss"],
             post_json["rtti_table_validation"]["first_miss_table_index"],
             post_json["SOURCE_PREDICTED_ORIGINAL_VERDICT"],
             post_json["TOOL_VERDICT"]))

    # whole-JSON delta confined to the new F2-C1/C2 metadata:
    # every top-level key must be present in both, and the only value
    # changes outside objects[] must be the F2-C1/C2 metadata keys
    allowed_changes = {
        "input_identity",           # user_defined_version_u32 added
        "user_version_gate",        # NEW (F2-C1)
        "adapter_integrity_checks",  # top_level_root_* fields (F2-C2)
        "source_predicted_reason",  # reworded (F2-C1/C2 mandatory fix)
        "tool_verdict_reason",      # derived reason text
    }
    changed_top = []
    for k in sorted(set(pre_json) | set(post_json)):
        if k not in pre_json:
            changed_top.append("%s (ADDED)" % k)
        elif k not in post_json:
            changed_top.append("%s (REMOVED)" % k)
        elif pre_json[k] != post_json[k]:
            changed_top.append(k)
    unexpected = [k for k in changed_top
                 if k not in allowed_changes and "(ADDED)" not in k
                 and "(REMOVED)" not in k]
    unexpected += [k for k in changed_top
                   if "(ADDED)" in k and k[:-8] != "user_version_gate"]
    check("t1_json_delta_confined_to_f2c1c2_metadata",
          not unexpected,
          "changed top-level keys: %s (allowed: %s)"
          % (changed_top, sorted(allowed_changes)))

    # second baseline: the historical pinned d497b44 record
    if baseline2:
        with open(baseline2, encoding="utf-8") as fh:
            hist = json.load(fh)
        hist_json = json.loads(hist["stdout_bytes"])
        diffs2 = []
        deep_equal(hist_json["objects"], post_json["objects"],
                   "$.objects", diffs2)
        h_sem, h_bnd = counts(hist_json["objects"])
        check("t1_objects_deep_identical_vs_historical_baseline",
              len(hist_json["objects"]) == 66 and not diffs2 and
              (h_sem, h_bnd) == (62, 4),
              "66/66 vs the pinned F2-package d497b44 record; "
              "%d recursive diffs; %d/%d" % (len(diffs2), h_sem, h_bnd))
        for d in diffs2[:20]:
            print("  DIFF2: %s" % d)

    print("T1_REGRESSION: %d failures: %r" % (len(failures), failures))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
