# make_manifest.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# Manifest generated LAST: covers every physical file of THIS correction
# package PLUS AUDIT_ENTRYPOINT.md (at its CURRENT BASE state: this executor
# run does NOT edit the entrypoint - the PE-MASTER persistence phase adds the
# run row and MUST then regenerate/re-verify this manifest per the standing
# contract), and is SELF-EXCLUDED (the manifest is never a row in itself).
# Bijection verified after writing:
# missing=0, extra=0, duplicates=0, size mismatches=0, SHA256 mismatches=0.
# Additionally verifies that HANDOFF.md's declared MANIFEST_ROW_COUNT equals
# the actually measured row count (the HANDOFF precedes the manifest; its
# manifest fields must match the verified bijection).

import csv
import hashlib
import os
import re
import sys

sys.dont_write_bytecode = True

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")
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
    # HANDOFF consistency: the HANDOFF (written BEFORE the manifest) declares
    # the manifest row count; verify it equals the measured count.
    handoff_path = os.path.join(RUN, "HANDOFF.md")
    if os.path.exists(handoff_path):
        content = open(handoff_path, encoding="utf-8").read()
        m = re.search(r"MANIFEST_ROW_COUNT\s*=\s*(\d+)", content)
        if m:
            declared = int(m.group(1))
            result["handoff_declared_manifest_row_count"] = declared
            result["handoff_consistent"] = (declared == len(rows))
        else:
            result["handoff_consistent"] = "NO_DECLARATION_FOUND"
    print("manifest rows=%d scope=%d bijection_ok=%s handoff_consistent=%s" % (
        result["manifest_rows"], result["scope_files"], result["bijection_ok"],
        result.get("handoff_consistent")))
    if not result["bijection_ok"]:
        print("MISSING:", missing)
        print("EXTRA:", extra)
        print("DUPS:", dups)
        print("SIZE:", size_mm)
        print("SHA:", sha_mm)
        raise SystemExit(1)
    if result.get("handoff_consistent") is not True:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
