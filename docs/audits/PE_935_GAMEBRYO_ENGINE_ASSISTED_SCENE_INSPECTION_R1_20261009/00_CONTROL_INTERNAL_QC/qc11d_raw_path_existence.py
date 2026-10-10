#!/usr/bin/env python3
"""QC11d — verify every absolute path referenced in the executor's evidence
JSONs exists on disk (raw logs, oracle JSONs, payload paths, input paths)."""
import json
import os
import re

PKG = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")

jsons = []
for sub in ["01_SDK", "02_PE", "00_RECORDS_CORRECTION"]:
    for root, dirs, files in os.walk(os.path.join(PKG, sub)):
        for fn in files:
            if fn.endswith(".json"):
                jsons.append(os.path.join(root, fn))

paths = set()
pat = re.compile(r'[A-Z]:\\\\[^"\\] (?:\\\\[^"\\])*'.replace(" ", ""))
# simpler: match escaped windows paths in the JSON text
pat = re.compile(r'[A-Z]:\\\\(?:[^"\\\\]|\\\\\\\\)*')
for j in jsons:
    text = open(j, encoding="utf-8").read()
    for m in pat.finditer(text):
        raw = m.group(0)
        p = raw.replace("\\\\", "\\")
        paths.add(p)

# also plain single-backslash paths inside plain string fields
pat2 = re.compile(r'"[A-Z]:\\\\[^"]+"')
for j in jsons:
    text = open(j, encoding="utf-8").read()
    for m in pat2.finditer(text):
        p = m.group(0)[1:-1].replace("\\\\", "\\")
        paths.add(p)

missing, present = [], 0
for p in sorted(paths):
    if os.path.exists(p):
        present += 1
    else:
        missing.append(p)

print("referenced absolute paths found:", len(paths))
print("present:", present)
print("missing:", len(missing))
for m in missing:
    print("  MISSING:", m)
