#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MANIFEST_SHA256.csv generator (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002).
Covers all package files EXCEPT:
  - 06_REPORT\MANIFEST_SHA256.csv itself (manifest self-exclusion, L12 precedent: a
    manifest cannot contain its own hash);
  - 04_QC\ (reserved for the fresh internal-QC worker).
Origin column distinguishes EXECUTOR outputs from FROZEN formalization-time control
files. KNOWN-STALE NOTE: this manifest is generated before the QC round and the
PE-MASTER verdict; it is known-stale until the final regeneration after QC.
"""
import os
import hashlib
import csv
import datetime

ROOT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
OUT = os.path.join(ROOT, "06_REPORT", "MANIFEST_SHA256.csv")
FROZEN = {
    r"00_CONTROL\RUN_CONTRACT.md",
    r"00_control\RUN_CONTRACT.md".lower(),
    r"00_CONTROL\AUTHORIZATION_RECORD.md",
    r"00_CONTROL\PREFLIGHT_EXPECTED.md",
    r"00_CONTROL\FORMALIZER_NOTES.md",
    r"00_CONTROL\CONTRACT_FREEZE.json",
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

rows = []
count = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) != os.path.join(ROOT, "04_QC")]
    for name in sorted(filenames):
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, ROOT)
        if rel.lower() == r"06_report\manifest_sha256.csv".lower():
            continue  # manifest self-exclusion
        origin = "FROZEN_FORMALIZER" if rel in {f.lower() for f in FROZEN} or rel in FROZEN else "EXECUTOR"
        rows.append((rel.replace("\\", "/"), os.path.getsize(full), sha256(full), origin))
        count += 1

rows.sort()
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["file", "size_bytes", "sha256", "origin", "note"])
    for rel, size, sha, origin in rows:
        w.writerow([rel, size, sha, origin, ""])
    w.writerow([])
    w.writerow(["NOTE", "", "", "",
                "Manifest covers package files excluding 04_QC (reserved for QC) and this manifest itself "
                "(self-exclusion per L12 precedent). KNOWN-STALE until final regeneration after QC + PE-MASTER verdict. "
                "Generated %s Z" % datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")])
print("manifest rows:", count, "->", OUT)
