# make_manifest.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
# Generates COMMITTED_PACKAGE_MANIFEST_SHA256.csv LAST (self-excluded):
# scope = every physical file of THIS package (docs/audits/PE_935_FACTORY_PLUS_84_
# ASSIGNMENT_OBJECT_R1_20261004/) EXCEPT the manifest itself, plus the updated
# AUDIT_ENTRYPOINT.md. Columns: rel_path, size_bytes, sha256. Real csv module.
import sys, os, csv, hashlib

sys.dont_write_bytecode = True

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits",
                   "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004")
MANIFEST_NAME = "COMMITTED_PACKAGE_MANIFEST_SHA256.csv"

def main():
    rows = []
    for root, dirs, files in os.walk(PKG):
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, REPO).replace("\\", "/")
            if rel == "docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/" + MANIFEST_NAME:
                continue  # self-excluded
            data = open(full, "rb").read()
            rows.append([rel, len(data), hashlib.sha256(data).hexdigest()])
    # the updated AUDIT_ENTRYPOINT.md
    ep = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")
    data = open(ep, "rb").read()
    rows.append(["AUDIT_ENTRYPOINT.md", len(data), hashlib.sha256(data).hexdigest()])
    rows.sort(key=lambda r: r[0])
    # bijection sanity: no duplicates
    seen = set()
    for r in rows:
        assert r[0] not in seen, "duplicate row: " + r[0]
        seen.add(r[0])
    out_path = os.path.join(PKG, MANIFEST_NAME)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rel_path", "size_bytes", "sha256"])
        for r in rows:
            w.writerow(r)
    print("manifest written: %d rows (self-excluded)" % len(rows))

if __name__ == "__main__":
    main()
