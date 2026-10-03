#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC helper 4: full artifact_index.csv verification (all rows, all hashes)."""
import csv
import hashlib
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
IDX = os.path.join(PKG, "06_REPORT", "artifact_index.csv")

rows = list(csv.DictReader(open(IDX, encoding="utf-8-sig")))
# also detect BOM
raw_head = open(IDX, "rb").read(4)
print("BOM check:", raw_head.hex(" "))
result = {"rows": len(rows), "issues": [], "ok": 0}
seen = set()
for r in rows:
    rel = r["relative_path"]
    size = int(r["size_bytes"])
    sha = r["sha256"].strip().upper()
    if rel in seen:
        result["issues"].append("DUP: %s" % rel)
    seen.add(rel)
    p = os.path.join(PKG, rel)
    if not os.path.exists(p):
        result["issues"].append("MISSING FILE: %s" % rel)
        continue
    st = os.stat(p)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
    ok_size = (st.st_size == size)
    ok_hash = (h == sha)
    if ok_size and ok_hash:
        result["ok"] += 1
    else:
        result["issues"].append("MISMATCH %s: idx_size=%d real=%d idx_sha_ok=%s" %
                                (rel, size, st.st_size, ok_hash))

# physical files vs index
phys = []
for root, dirs, files in os.walk(PKG):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), PKG)
        if rel.startswith("07_QC"):
            continue  # QC's own files, added after the executor's close
        phys.append(rel)
missing_from_index = [p for p in phys if p not in seen]
extra_in_index = [p for p in seen if p not in phys]
result["physical_files_no_qc"] = len(phys)
result["missing_from_index"] = missing_from_index
result["extra_in_index"] = extra_in_index

out = os.path.join(PKG, "07_QC", "raw", "ARTIFACT_INDEX_CHECK.json")
with open(out, "w", encoding="utf-8") as f:
    import json
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=1))
