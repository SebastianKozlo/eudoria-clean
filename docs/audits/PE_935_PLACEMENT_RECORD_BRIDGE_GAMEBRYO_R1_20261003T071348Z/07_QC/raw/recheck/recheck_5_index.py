#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 5 (artifact_index.csv): row count, schema, FULL rehash of every row
(path/size/sha256 vs disk), AMEND_LOG_R1.md row present, no 07_QC rows,
self-exclusion, physical file census (executor-owned = index + index itself)."""
import csv
import hashlib
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
IDX = os.path.join(PKG, "06_REPORT", "artifact_index.csv")
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck5_index.json")

with open(IDX, "rb") as f:
    head = f.read(4)
res = {"bom": head[:3] == b"\xef\xbb\xbf"}

with open(IDX, encoding="utf-8-sig", newline="") as f:
    rdr = csv.reader(f)
    header = next(rdr)
    rows = [r for r in rdr if any(c.strip() for c in r)]
res["header"] = header
res["row_count"] = len(rows)
res["expected_schema"] = ["relative_path", "size_bytes", "sha256"]
res["schema_ok"] = [h.strip() for h in header] == res["expected_schema"]

res["rows"] = []
issues = []
ok = 0
seen = set()
for r in rows:
    rel, size, sha = r[0].strip(), int(r[1]), r[2].strip().upper()
    role = ""
    p = os.path.join(PKG, *rel.replace("/", os.sep).split(os.sep))
    entry = {"path": rel, "role": role, "size": size, "sha256": sha}
    if rel in seen:
        issues.append("DUP: %s" % rel)
    seen.add(rel)
    if "07_QC" in rel.replace("\\", "/"):
        issues.append("QC-OWNED ROW IN INDEX: %s" % rel)
        entry["status"] = "QC_ROW_FORBIDDEN"
        res["rows"].append(entry)
        continue
    if not os.path.exists(p):
        issues.append("MISSING ON DISK: %s" % rel)
        entry["status"] = "MISSING"
        res["rows"].append(entry)
        continue
    st = os.stat(p)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
    if st.st_size == size and h == sha:
        ok += 1
        entry["status"] = "OK"
    else:
        issues.append("MISMATCH %s: idx_size=%d real=%d idx_sha=%s real_sha=%s" %
                      (rel, size, st.st_size, sha, h))
        entry["status"] = "MISMATCH"
    res["rows"].append(entry)

res["ok_rows"] = ok
res["issues"] = issues
res["amend_log_row_present"] = any("AMEND_LOG_R1.md" in r["path"] for r in res["rows"])
res["qc_rows_count"] = sum(1 for r in res["rows"] if r.get("status") == "QC_ROW_FORBIDDEN")
res["self_row_present"] = any("artifact_index.csv" in r["path"] for r in res["rows"])

# physical executor files (everything except 07_QC), separator-normalized
phys = []
for root, dirs, files in os.walk(PKG):
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), PKG).replace(os.sep, "/")
        if rel.startswith("07_QC"):
            continue
        phys.append(rel)
seen_norm = set(s.replace("\\", "/") for s in seen)
res["physical_executor_files"] = len(phys)
res["phys_not_in_index"] = sorted(set(phys) - seen_norm)
res["index_not_on_disk"] = sorted(set(s.replace("\\", "/") for s in seen_norm) - set(phys))
res["executor_total_with_index_self"] = len(phys)  # index itself included in walk
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
