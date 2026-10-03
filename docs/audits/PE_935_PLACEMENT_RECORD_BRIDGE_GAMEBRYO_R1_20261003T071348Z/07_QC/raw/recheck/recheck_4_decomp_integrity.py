#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 4 (INTEGRITY): compare EVERY decompile body copy in
07_QC/raw/decomp_dump/ (QC round-1 = pre-repair baseline, 88 files) against the
CURRENT 01_RAW JSON decompilation bodies. Whitespace-insensitive content
comparison (collapse all whitespace) — any wording/instruction/offset change
in any decompile body since QC round-1 is a mismatch."""
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
DDIR = os.path.join(PKG, "07_QC", "raw", "decomp_dump")
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck4_decomp_integrity.json")

def collapse(s):
    return re.sub(r"\s+", "", s)

cache = {}
def get_decomp(json_name, key):
    if json_name not in cache:
        with open(os.path.join(PKG, "01_RAW", json_name), encoding="utf-8-sig") as f:
            cache[json_name] = json.load(f)["measured"]["decompilations"]
    return cache[json_name].get(key)

files = sorted(os.listdir(DDIR))
res = {"dump_files": len(files), "match": 0, "mismatch": [], "missing_key": [], "extra_note": []}
for fn in files:
    if not fn.endswith(".c"):
        continue
    m = re.match(r"(\w+)__(\w+)\.c", fn)
    json_name, key = m.group(1) + ".json", m.group(2)
    with open(os.path.join(DDIR, fn), encoding="utf-8") as f:
        txt = f.read()
    # drop the '// source:' header line
    nl = txt.find("\n")
    header = txt[:nl]
    body = txt[nl + 1:]
    assert header.strip().startswith("// source:"), fn
    cur = get_decomp(json_name, key)
    if cur is None:
        res["missing_key"].append("%s :: %s" % (json_name, key))
        continue
    if collapse(body) == collapse(cur["c"]):
        res["match"] += 1
    else:
        res["mismatch"].append("%s :: %s (dump_len=%d cur_len=%d)" % (
            json_name, key, len(collapse(body)), len(collapse(cur["c"]))))

res["all_match"] = (res["match"] == len(files) and not res["missing_key"])
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
