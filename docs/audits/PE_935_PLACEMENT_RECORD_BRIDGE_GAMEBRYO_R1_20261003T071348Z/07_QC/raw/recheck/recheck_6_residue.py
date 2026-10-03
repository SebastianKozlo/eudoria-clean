#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 6 (residue sweep, whitespace-normalized) + RE-QC 7 (untouched claims).
Sweeps ALL executor-owned files for the pre-repair residue phrases:
  '69 census', '= 69' (census-target context), '68 2D', 'flag-2 slots',
  'flag-2 branch executes lookup'.
Whitespace normalization: every whitespace run (space/tab/CRLF/LF) -> ' '.
Every hit is reported with file, line number and context so live residue is
distinguishable from documented BEFORE-state quotes in AMEND_LOG_R1.md."""
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck6_residue.json")
EXEC_DIRS = ("00_CONTROL", "01_RAW", "02_ANALYSIS", "03_SCRIPTS", "04_CONTROLS",
             "05_ORACLE", "06_REPORT")

PHRASES = ["69 census", "= 69", "68 2D", "flag-2 slots",
           "flag-2 branch executes lookup"]

res = {p: [] for p in PHRASES}
files_swept = 0
for d in EXEC_DIRS:
    dp = os.path.join(PKG, d)
    for root, _, files in os.walk(dp):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, PKG)
            files_swept += 1
            with open(p, encoding="utf-8-sig", errors="replace") as f:
                lines = f.read().splitlines()
            for ln, line in enumerate(lines, 1):
                norm = re.sub(r"\s+", " ", line).strip()
                for ph in PHRASES:
                    if ph.lower() in norm.lower():
                        res[ph].append({"file": rel.replace(os.sep, "/"),
                                        "line": ln, "text": norm[:180]})

summary = {}
for ph in PHRASES:
    per_file = {}
    for h in res[ph]:
        per_file.setdefault(h["file"], []).append(h["line"])
    summary[ph] = {"total": len(res[ph]), "per_file": {k: v for k, v in per_file.items()}}

out = {"files_swept": files_swept, "summary": summary, "hits": res}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(json.dumps(summary, indent=1))
