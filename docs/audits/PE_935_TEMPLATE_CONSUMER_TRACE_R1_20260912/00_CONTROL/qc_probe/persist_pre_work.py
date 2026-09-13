#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PERSIST probe (pe-master-auditor, RUN_ID: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST):
PRE-WORK SNAPSHOT of the whole run package, taken BEFORE any F1-F4 correction.

Purpose: the byte-level "before" state for gate P4 (evidence untouchability)
and for the F2/F3 manifest rebuild (old rows preserved in this snapshot).

READ-ONLY w.r.t. every existing package file. Writes only:
  00_CONTROL\qc_probe\persist_pre_work_state.json
"""
import hashlib
import json
import os
import sys

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
OUT = os.path.join(RUN, "00_CONTROL", "qc_probe", "persist_pre_work_state.json")

files = {}
for dirpath, dirnames, filenames in os.walk(RUN):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, RUN).replace(os.sep, "\\")
        with open(p, "rb") as f:
            data = f.read()
        files[rel] = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()}

manifest_rel = "06_REPORT\\artifact_index.csv"
manifest_rows = []
with open(os.path.join(RUN, manifest_rel), "r", encoding="utf-8-sig", newline="") as f:
    lines = f.read().splitlines()
for ln in lines[1:]:
    if ln.strip():
        manifest_rows.append(ln)

state = {
    "probe": "persist_pre_work_state",
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST",
    "purpose": "pre-F1/F2/F3/F4 byte snapshot; P4 comparison basis",
    "package_file_count": len(files),
    "files": files,
    "manifest_data_rows_pre": len(manifest_rows),
    "manifest_rows_pre": manifest_rows,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print("package files snapshot: %d" % len(files))
print("manifest data rows (pre): %d" % len(manifest_rows))
sys.exit(0)
