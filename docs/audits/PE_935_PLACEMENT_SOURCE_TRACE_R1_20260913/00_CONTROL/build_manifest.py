# -*- coding: utf-8 -*-
# Build 03_EVIDENCE\MANIFEST_SHA256.csv for the run package (excluding GHIDRA_LOCAL bulk)
import csv
import hashlib
import os

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"

rows = []
for base, dirs, files in os.walk(RUN_ROOT):
    if "GHIDRA_LOCAL" in base:
        continue
    for fn in files:
        p = os.path.join(base, fn)
        rel = os.path.relpath(p, RUN_ROOT).replace("\\", "/")
        if rel == "03_EVIDENCE/MANIFEST_SHA256.csv":
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
        rows.append((rel, h, os.path.getsize(p)))

# also hash the control scripts
out = os.path.join(RUN_ROOT, "03_EVIDENCE", "MANIFEST_SHA256.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["relative_path", "sha256", "size_bytes"])
    for r in sorted(rows):
        w.writerow(r)
print("rows:", len(rows))

# script hashes for SCRIPT_SHA256.csv
scripts = []
ctrl = os.path.join(RUN_ROOT, "00_CONTROL")
for fn in sorted(os.listdir(ctrl)):
    if fn.endswith(".py"):
        p = os.path.join(ctrl, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
        scripts.append((fn, h))
out2 = os.path.join(ctrl, "SCRIPT_SHA256.csv")
with open(out2, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["script", "sha256"])
    for r in scripts:
        w.writerow(r)
print("scripts:", len(scripts))
