# -*- coding: utf-8 -*-
# GA5-IMMUTABLE: census of historical package hashes (before/after).
# Per package: file count, total bytes, composite SHA256 over sorted file records.
# Zero-change expected between BEFORE and AFTER runs.
# Output: 01_RAW/GA5_IMMUTABLE_CENSUS_{before,after}.json + comparison

import hashlib
import json
import os
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")

PACKAGES = {
    "RUN1_TEMPLATE_CONSUMER_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "RUN2_EXTERNAL_SOURCES_MATRIX": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913",
    "RUN3_STATIC_INSTANCE_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "RUN4_PLACEMENT_SOURCE_TRACE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "ROUND_CLOSURE": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_ROUND1_20260913",
    "JOIN_ERRATA_R2": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
    "DESKTOP_AUDIT": r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913",
}


def census(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for blk in iter(lambda: f.read(1 << 20), b""):
                    h.update(blk)
            sz = os.path.getsize(p)
            files.append((rel, sz, h.hexdigest().upper()))
    files.sort()
    composite = hashlib.sha256()
    for rel, sz, fh in files:
        composite.update(("%s|%d|%s\n" % (rel, sz, fh)).encode("utf-8"))
    return {"file_count": len(files),
            "total_bytes": sum(f[1] for f in files),
            "composite_sha256": composite.hexdigest().upper(),
            "files": [{"path": r, "size": s, "sha256": h} for r, s, h in files]}


def main():
    when = sys.argv[1] if len(sys.argv) > 1 else "before"
    res = {"stage": "GA5_immutable_census", "phase": when, "packages": {}}
    for name, root in sorted(PACKAGES.items()):
        res["packages"][name] = census(root)
    with open(os.path.join(OUT, "GA5_IMMUTABLE_CENSUS_%s.json" % when), "w") as f:
        json.dump(res, f, indent=2)
    print("GA5 census (%s):" % when)
    for name, r in res["packages"].items():
        print("  %-30s files=%d bytes=%d composite=%s" % (
            name, r["file_count"], r["total_bytes"], r["composite_sha256"][:16]))


if __name__ == "__main__":
    main()
