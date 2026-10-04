# make_manifest.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# Manifest generated LAST: covers every physical file of THIS correction
# package PLUS the updated AUDIT_ENTRYPOINT.md, and is SELF-EXCLUDED (the
# manifest is never a row in itself). Bijection verified after writing:
# missing=0, extra=0, duplicates=0, size mismatches=0, SHA256 mismatches=0.

import csv
import hashlib
import os
import sys

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
MANIFEST = os.path.join(RUN, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")
ENTRYPOINT = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()


def main():
    scope = []
    for root, _dirs, files in os.walk(RUN):
        for fn in files:
            p = os.path.join(root, fn)
            if os.path.normpath(p) == os.path.normpath(MANIFEST):
                continue  # self-excluded
            scope.append(p)
    scope.append(ENTRYPOINT)

    rows = []
    for p in sorted(scope):
        rel = os.path.relpath(p, REPO).replace("\\", "/")
        sz = os.path.getsize(p)
        rows.append({"path": rel, "size_bytes": sz, "sha256": sha256(p)})

    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "size_bytes", "sha256"])
        for r in rows:
            w.writerow([r["path"], r["size_bytes"], r["sha256"]])

    # bijection verification (re-read from disk)
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        got = list(csv.DictReader(f))
    got_paths = [g["path"] for g in got]
    scope_rel = [os.path.relpath(p, REPO).replace("\\", "/") for p in scope]
    missing = sorted(set(scope_rel) - set(got_paths))
    extra = sorted(set(got_paths) - set(scope_rel))
    dups = sorted({p for p in got_paths if got_paths.count(p) > 1})
    size_mm = [g["path"] for g in got
               if os.path.getsize(os.path.join(REPO, g["path"].replace("/", "\\")))
               != int(g["size_bytes"])]
    sha_mm = [g["path"] for g in got
              if sha256(os.path.join(REPO, g["path"].replace("/", "\\"))) != g["sha256"].upper()]
    result = {"manifest_rows": len(rows),
               "scope_files": len(scope),
               "missing": missing, "extra": extra, "duplicates": dups,
               "size_mismatches": size_mm, "sha256_mismatches": sha_mm,
               "bijection_ok": (not missing and not extra and not dups
                                and not size_mm and not sha_mm)}
    print("manifest rows=%d scope=%d bijection_ok=%s" % (
        result["manifest_rows"], result["scope_files"], result["bijection_ok"]))
    if not result["bijection_ok"]:
        print("MISSING:", missing)
        print("EXTRA:", extra)
        print("DUPS:", dups)
        print("SIZE:", size_mm)
        print("SHA:", sha_mm)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
