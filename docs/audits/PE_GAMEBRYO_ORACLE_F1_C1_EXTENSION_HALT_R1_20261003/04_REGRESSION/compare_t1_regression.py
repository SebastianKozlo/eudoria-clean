#!/usr/bin/env python3
# compare_t1_regression.py -- T1/218757 deep regression comparison for
# PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003.
#
# Compares the COMPLETE objects[] of the post-F1-C1-fix T1 --full-decode
# oracle output against the PINNED baseline published by
# PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (committed artifact, produced on the
# pre-F1 code base abc3f8f; the F1 run PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_
# R1_20261003 @ 60a73d9 already verified 66/66 identity -- this run re-proves
# it for the F1-C1 fix).
#
# DEEP-IDENTICAL means: every field of every record compared recursively
# (values, names/types/status, local transforms, links, byte_start,
# byte_end, byte_size and ALL other recorded fields). "62 known + 4
# opaque/boundary-only" is the interpretation LABEL and is preserved as
# such -- 66/66 record identity is NOT promoted to 66 semantic decodes
# (the 4 opaque records are boundary-only: status
# UNREGISTERED_IN_GB12_FACTORY with closure-derived boundaries).
#
# Usage:
#   python compare_t1_regression.py <pinned_baseline.json> <post_fix_run1.json> <post_fix_run2.json>

import hashlib
import json
import sys


def deep_diff(a, b, path=""):
    diffs = []
    if type(a) is not type(b):
        diffs.append("%s: TYPE %r != %r" % (path, type(a).__name__,
                                            type(b).__name__))
        return diffs
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                diffs.append("%s.%s: only in POST_FIX" % (path, k))
            elif k not in b:
                diffs.append("%s.%s: only in BASELINE" % (path, k))
            else:
                diffs.extend(deep_diff(a[k], b[k], "%s.%s" % (path, k)))
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append("%s: LEN %d != %d" % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            diffs.extend(deep_diff(x, y, "%s[%d]" % (path, i)))
    else:
        if a != b:
            diffs.append("%s: %r != %r" % (path, a, b))
    return diffs


def main():
    baseline_p, run1_p, run2_p = sys.argv[1], sys.argv[2], sys.argv[3]
    base = json.load(open(baseline_p, encoding="utf-8"))
    r1 = json.load(open(run1_p, encoding="utf-8"))
    r2 = json.load(open(run2_p, encoding="utf-8"))

    out = {
        "comparison_schema": "gamebryo_oracle_f1c1_run/t1_regression@1.0",
        "pinned_baseline": {
            "path": baseline_p,
            "sha256": hashlib.sha256(
                open(baseline_p, "rb").read()).hexdigest().upper(),
        },
        "post_fix_run1": {
            "path": run1_p,
            "sha256": hashlib.sha256(
                open(run1_p, "rb").read()).hexdigest().upper(),
        },
        "post_fix_run2_determinism": {
            "path": run2_p,
            "sha256": hashlib.sha256(
                open(run2_p, "rb").read()).hexdigest().upper(),
            "byte_identical_to_run1": open(run1_p, "rb").read() ==
                                      open(run2_p, "rb").read(),
        },
        "input_identity_match": (
            base["input_identity"]["size"] == r1["input_identity"]["size"] and
            base["input_identity"]["sha256"] ==
            r1["input_identity"]["sha256"]),
        "input_sha256": base["input_identity"]["sha256"],
    }

    objs_b = base["objects"]
    objs_1 = r1["objects"]
    n = len(objs_b)
    per_record = []
    all_identical = len(objs_b) == len(objs_1)
    if all_identical:
        for i in range(n):
            d = deep_diff(objs_b[i], objs_1[i], "objects[%d]" % i)
            per_record.append({
                "index": i,
                "type": objs_b[i].get("type") if objs_b[i] else None,
                "deep_identical": not d,
                "field_count_baseline": len(objs_b[i]) if objs_b[i] else 0,
                "diffs": d[:20],
            })
            all_identical = all_identical and not d
    else:
        per_record.append({"index": None, "deep_identical": False,
                           "diffs": ["objects length %d != %d" %
                                     (len(objs_b), len(objs_1))]})

    opaque_b = [o for o in objs_b if o and o.get("status")]
    known_b = [o for o in objs_b if o and not o.get("status")]
    opaque_1 = [o for o in objs_1 if o and o.get("status")]
    known_1 = [o for o in objs_1 if o and not o.get("status")]

    out["objects"] = {
        "count_baseline": n,
        "count_post_fix": len(objs_1),
        "all_66_deep_identical": all_identical,
        "per_record_deep_identical_count": sum(
            1 for r in per_record if r.get("deep_identical")),
        "opaque_boundary_only_baseline": len(opaque_b),
        "opaque_boundary_only_post_fix": len(opaque_1),
        "known_semantically_decoded_baseline": len(known_b),
        "known_semantically_decoded_post_fix": len(known_1),
        "interpretation_label": ("62 known semantically decoded records + "
                                 "4 opaque/boundary-only records (PRESERVED; "
                                 "66/66 record identity is NOT 66 semantic "
                                 "decodes)"),
        "per_record": per_record,
    }

    out["verdict_fields"] = {
        "load_result_baseline": base["load_result"],
        "load_result_post_fix": r1["load_result"],
        "first_rtti_miss": r1["rtti_table_validation"]["first_rtti_miss"],
        "first_miss_table_index":
            r1["rtti_table_validation"]["first_miss_table_index"],
        "source_predicted_verdict":
            r1["rtti_table_validation"]["source_predicted_verdict"],
        "full_table_read":
            r1["rtti_table_validation"]["full_table_read"],
        "roots": r1["scene_graph"]["roots"],
        "extension_halt_key_absent_on_t1_path":
            "extension_halt" not in r1,
        "warnings_count": len(r1["warnings"]),
        "decode_continued_after_rtti_gate":
            r1["decode_continued_after_rtti_gate"],
    }

    ok = (out["input_identity_match"] and
          all_identical and n == 66 and len(opaque_1) == 4 and
          len(known_1) == 62 and
          r1["rtti_table_validation"]["first_rtti_miss"] ==
          "NiArkAnimationExtraData" and
          r1["rtti_table_validation"]["first_miss_table_index"] == 1 and
          r1["rtti_table_validation"]["source_predicted_verdict"] ==
          "REJECTED" and
          out["post_fix_run2_determinism"]["byte_identical_to_run1"])
    out["T1_66_OBJECT_RECORD_DEEP_REGRESSION"] = "PASS" if (
        all_identical and n == 66) else "FAIL"
    out["T1_62_KNOWN_4_OPAQUE"] = "PRESERVED" if (
        len(known_1) == 62 and len(opaque_1) == 4) else "REGRESSION"
    out["VERDICT"] = "PASS" if ok else "FAIL"
    print(json.dumps(out, indent=1, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
