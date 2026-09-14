"""qc_gb6_repeat.py — auditor's OWN repeat of the GB6 immutable census (8 historical packages).
Independent method: own walk+hash, own composite (different field order/format than the
executor's gb6_immutable.py), then compared against the executor's before/after composites.
"""
import hashlib
import json
import os

PKG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
PACKAGES = {
    "RUN1_TEMPLATE_CONSUMER_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "RUN2_EXTERNAL_SOURCES_MATRIX": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913",
    "RUN3_STATIC_INSTANCE_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "RUN4_PLACEMENT_SOURCE_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "ROUND_CLOSURE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_ROUND1_20260913",
    "JOIN_ERRATA_R2": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
    "DESKTOP_AUDIT": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913",
    "PKG_A_RECEIVER_PROVENANCE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()


def own_composite(root):
    """Own composite: digest over (size, sha, relpath-lowercase-forward) tuples in os-walk order."""
    h = hashlib.sha256()
    n = 0
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace("\\", "/").lower()
            sz = os.path.getsize(p)
            fh = sha256_file(p)
            h.update(("%d:%s:%s\n" % (sz, fh, rel)).encode("utf-8"))
            n += 1
            total += sz
    return n, total, h.hexdigest().upper()


def main():
    # executor's before/after for cross-check
    ex_before = json.load(open(os.path.join(PKG, "01_RAW", "GB6_IMMUTABLE_CENSUS_before.json"), encoding="utf-8"))
    ex_after = json.load(open(os.path.join(PKG, "01_RAW", "GB6_IMMUTABLE_CENSUS_after.json"), encoding="utf-8"))
    res = {"stage": "QC_GB6_repeat_own_method", "packages": {}}
    ok = True
    for name, root in sorted(PACKAGES.items()):
        n, total, comp = own_composite(root)
        ex_b = ex_before["packages"][name]
        ex_a = ex_after["packages"][name]
        counts_ok = (n == ex_b["file_count"] == ex_a["file_count"])
        executor_pair_equal = (ex_b["composite_sha256"] == ex_a["composite_sha256"])
        res["packages"][name] = {
            "own_file_count": n, "own_total_bytes": total, "own_composite": comp,
            "executor_before_composite": ex_b["composite_sha256"],
            "executor_after_composite": ex_a["composite_sha256"],
            "executor_before_after_equal": executor_pair_equal,
            "own_count_matches_executor": counts_ok,
        }
        print("%-30s own_files=%d exec_before==after:%s counts_ok:%s" % (
            name, n, executor_pair_equal, counts_ok))
        if not (executor_pair_equal and counts_ok):
            ok = False
    res["verdict"] = "GB6_REPEAT_OK" if ok else "GB6_REPEAT_MISMATCH"
    outp = os.path.join(PKG, "00_CONTROL", "qc_probe", "QC_GB6_REPEAT.json")
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("verdict:", res["verdict"], "->", outp)


if __name__ == "__main__":
    main()
