# build_manifests.py - build artifact_index.csv + MANIFEST_SHA256.csv
# for THIS run package. MANIFEST has NO self-row (precedens L12); covers all
# package files EXCEPT the two manifest files themselves and the GHIDRA_LOCAL
# project (LOCAL-ONLY per phase-B precedent, kept under its own manifests).
# Deterministic (sorted paths, no timestamps).

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, ".."))

EXCLUDE_DIRS = {"__pycache__"}
SELF_NAMES = {"MANIFEST_SHA256.csv", "artifact_index.csv"}


def sha_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


rows = []
for dp, dns, fns in os.walk(PKG):
    dns[:] = sorted(d for d in dns if d not in EXCLUDE_DIRS)
    rel_dir = os.path.relpath(dp, PKG)
    if rel_dir.split(os.sep)[0] == "00_CONTROL" and \
            "GHIDRA_LOCAL" in rel_dir:
        continue  # local-only, own manifests exist
    for fn in sorted(fns):
        if fn in SELF_NAMES and rel_dir == "06_REPORT":
            continue
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, PKG).replace("\\", "/")
        rows.append((rel, os.path.getsize(p), sha_of(p)))

rows.sort(key=lambda r: r[0])

with open(os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv"), "w",
          newline="") as f:
    f.write("path,sha256\r\n")
    for rel, size, h in rows:
        f.write("%s,%s\r\n" % (rel, h))

with open(os.path.join(PKG, "06_REPORT", "artifact_index.csv"), "w",
          newline="") as f:
    f.write("relpath,size_bytes,sha256\r\n")
    for rel, size, h in rows:
        f.write("%s,%d,%s\r\n" % (rel, size, h))

print("manifest rows: %d" % len(rows))
for rel, size, h in rows:
    print("  %-70s %8d  %s" % (rel, size, h[:16]))
