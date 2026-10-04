# s6_make_manifest.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Generates COMMITTED_PACKAGE_MANIFEST_SHA256.csv LAST.
# Scope = the committed files in this package minus the manifest itself.
# Header: relative_path,size_bytes,sha256. Self-excluded per the L12 precedent.
import sys, os, hashlib, csv
sys.dont_write_bytecode = True

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
MANIFEST_NAME = "COMMITTED_PACKAGE_MANIFEST_SHA256.csv"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    rows = []
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in sorted(files):
            if name == MANIFEST_NAME:
                continue  # self-excluded
            full = os.path.join(root, name)
            rel = os.path.relpath(full, REPO).replace("\\", "/")
            rows.append((rel, os.path.getsize(full), sha256_file(full)))
    rows.sort()
    out = os.path.join(PKG, MANIFEST_NAME)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["relative_path", "size_bytes", "sha256"])
        for r in rows:
            w.writerow(list(r))
    # bijection self-check: every listed file exists; every package file (minus
    # the manifest and any __pycache__) is listed exactly once
    listed = {r[0] for r in rows}
    on_disk = set()
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            if name == MANIFEST_NAME:
                continue
            full = os.path.join(root, name)
            on_disk.add(os.path.relpath(full, REPO).replace("\\", "/"))
    ok = listed == on_disk and len(listed) == len(rows)
    print("manifest rows:", len(rows), "| bijection_ok:", ok)
    if not ok:
        print("missing:", on_disk - listed, "| extra:", listed - on_disk)
        sys.exit(1)

if __name__ == "__main__":
    main()
