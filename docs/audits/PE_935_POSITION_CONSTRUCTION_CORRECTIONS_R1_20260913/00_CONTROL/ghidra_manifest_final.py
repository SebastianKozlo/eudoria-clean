# ghidra_manifest_final.py - save the FINAL manifest of THIS run's
# GHIDRA_LOCAL copy (after the analyzeHeadless tours).
# STATIC-ONLY.

import csv
import hashlib
import os

root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "GHIDRA_LOCAL")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "GHIDRA_LOCAL_MANIFEST_final.csv")

rows = []
for dirpath, dirnames, filenames in os.walk(root):
    for fn in sorted(filenames):
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, root).replace("\\", "/")
        h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
        rows.append((h, rel, str(os.path.getsize(p))))
rows.sort(key=lambda r: r[1])
with open(out, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["sha256", "relpath", "size"])
    for r in rows:
        w.writerow(r)
print("rows:", len(rows))
for r in rows:
    print("  %s  %s  %s" % (r[0][:16], r[1], r[2]))
