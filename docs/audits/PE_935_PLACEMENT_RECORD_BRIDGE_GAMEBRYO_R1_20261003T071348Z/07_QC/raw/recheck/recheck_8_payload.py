#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 8 (payload discipline) over the WHOLE package INCLUDING 07_QC/.
Checks:
 1. extension census — forbidden: .exe .dll .vfs .bnt .bvi .ark .nif .tga .cpp .h .lib .zip ...
 2. binary-content sniff — any file whose non-whitespace byte mass is largely
    non-textual (binary payload indicator);
 3. long embedded hex/base64 blobs (>2048 continuous hex chars = potential raw
    payload dumps; short hex instruction extracts are allowed derived evidence);
 4. total size census per directory."""
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck8_payload.json")

FORBIDDEN_EXT = {".exe", ".dll", ".vfs", ".bnt", ".bvi", ".ark", ".nif", ".tga",
                 ".cpp", ".h", ".hpp", ".lib", ".obj", ".zip", ".7z", ".cab",
                 ".msi", ".bin", ".pak", ".dds", ".bmp", ".png", ".jpg"}

ext_census = {}
binary_suspects = []
hex_blobs = []
size_census = {}
n_files = 0
for root, dirs, files in os.walk(PKG):
    rel_dir = os.path.relpath(root, PKG)
    size_census[rel_dir] = size_census.get(rel_dir, 0)
    for fn in files:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, PKG).replace(os.sep, "/")
        n_files += 1
        ext = os.path.splitext(fn)[1].lower()
        ext_census[ext] = ext_census.get(ext, 0) + 1
        size = os.path.getsize(p)
        size_census[rel_dir] += size
        if ext in FORBIDDEN_EXT:
            binary_suspects.append({"file": rel, "reason": "forbidden extension %s" % ext})
            continue
        data = open(p, "rb").read()
        # binary sniff: count non-text control bytes (excluding tab/lf/cr/ff)
        nontext = sum(1 for b in data if b < 9 or (13 < b < 32) or b == 127)
        if size and nontext / size > 0.02:
            binary_suspects.append({"file": rel, "reason": "nontext_ratio=%.3f" % (nontext / size)})
        # long continuous hex blobs (raw payload dump indicator)
        txt = data.decode("utf-8", errors="ignore")
        for m in re.finditer(r"[0-9A-Fa-f]{2048,}", txt):
            hex_blobs.append({"file": rel, "at": m.start(), "len": len(m.group(0))})
        for m in re.finditer(r"[A-Za-z0-9+/]{4096,}={0,2}", txt):
            if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", m.group(0)) and len(m.group(0)) % 4 == 0:
                hex_blobs.append({"file": rel, "at": m.start(), "len": len(m.group(0)), "kind": "base64?"})

res = {"files_total": n_files, "ext_census": ext_census,
       "binary_suspects": binary_suspects, "hex_blobs_over_2048": hex_blobs,
       "size_census_bytes": size_census,
       "total_package_bytes": sum(size_census.values())}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "size_census_bytes"}, indent=1))
