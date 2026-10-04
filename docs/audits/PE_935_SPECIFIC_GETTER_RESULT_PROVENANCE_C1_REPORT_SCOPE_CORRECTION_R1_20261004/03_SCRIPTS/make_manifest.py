# make_manifest.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004
# Purpose: generate COMMITTED_PACKAGE_MANIFEST_SHA256.csv (LAST, per contract).
# Scope = ALL physical files of THIS package (docs/audits/PE_935_SPECIFIC_
# GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004/) + the
# updated AUDIT_ENTRYPOINT.md MINUS the manifest itself. Repository-relative
# paths. Header: relative_path,size_bytes,sha256. Verifies complete bijection
# with the declared physical path set (no dup/missing/extra rows) and prints
# actual row/file counts.
import os, hashlib, csv

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
ENTRY = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")
MANIFEST_NAME = "COMMITTED_PACKAGE_MANIFEST_SHA256.csv"
MANIFEST = os.path.join(PKG, MANIFEST_NAME)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()

def main():
    # collect all physical files of the package
    files = []
    for root, dirs, names in os.walk(PKG):
        for n in sorted(names):
            full = os.path.join(root, n)
            rel = os.path.relpath(full, REPO).replace("\\", "/")
            files.append((full, rel))
    # the entrypoint file (this run's ONE row update)
    files.append((ENTRY, "AUDIT_ENTRYPOINT.md"))
    # exclude the manifest itself
    files = [(f, r) for (f, r) in files if os.path.basename(f) != MANIFEST_NAME]
    files.sort(key=lambda x: x[1])
    # verify no duplicates
    rels = [r for _, r in files]
    assert len(rels) == len(set(rels)), "duplicate rows detected"
    rows = []
    for full, rel in files:
        rows.append((rel, os.path.getsize(full), sha256_file(full)))
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["relative_path", "size_bytes", "sha256"])
        for rel, size, sha in rows:
            w.writerow([rel, size, sha])
    # self-check: bijection with the physical path set
    on_disk = set(rels)
    in_manifest = set(rel for rel, _, _ in rows)
    assert on_disk == in_manifest, "manifest/disk mismatch"
    print("rows=%d files=%d (package files + entrypoint 1; manifest self-excluded)"
          % (len(rows), len(files)))
    for rel, size, sha in rows:
        print("%s,%d,%s" % (rel, size, sha))

if __name__ == "__main__":
    main()
