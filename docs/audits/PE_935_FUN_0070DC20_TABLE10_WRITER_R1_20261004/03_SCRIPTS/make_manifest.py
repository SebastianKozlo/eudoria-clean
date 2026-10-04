# make_manifest.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose: generate COMMITTED_PACKAGE_MANIFEST_SHA256.csv (LAST, self-
# excluded). Scope = ALL physical files of this package + the updated
# AUDIT_ENTRYPOINT.md. Header: relative_path,size_bytes,sha256.
# Bijection is verified by the run output (count + re-read check).
import os, hashlib

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join("docs", "audits", "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004")
MANIFEST = os.path.join(PKG, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    rows = []
    for root, dirs, files in os.walk(os.path.join(REPO, PKG)):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, REPO).replace("\\", "/")
            if rel == os.path.join(PKG, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv").replace("\\", "/"):
                continue  # self-excluded
            rows.append((rel, os.path.getsize(full), sha256(full)))
    # the updated entrypoint
    ep = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")
    rows.append(("AUDIT_ENTRYPOINT.md", os.path.getsize(ep), sha256(ep)))
    with open(os.path.join(REPO, MANIFEST), "w", newline="\n") as f:
        f.write("relative_path,size_bytes,sha256\n")
        for rel, sz, h in rows:
            f.write("%s,%d,%s\n" % (rel, sz, h))
    # bijection self-check
    with open(os.path.join(REPO, MANIFEST), "r") as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    hdr = lines[0]
    body = lines[1:]
    assert hdr == "relative_path,size_bytes,sha256", hdr
    seen = set()
    for ln in body:
        p, s, h = ln.rsplit(",", 2)
        assert p not in seen, "duplicate: %s" % p
        seen.add(p)
        full = os.path.join(REPO, p.replace("/", "\\"))
        assert os.path.getsize(full) == int(s), p
        assert sha256(full) == h, p
    expected = set(r[0] for r in rows)
    assert seen == expected, (seen ^ expected)
    print("manifest rows: %d (self-excluded); bijection verified; no missing/extra/duplicate"
          % len(body))

if __name__ == "__main__":
    main()
