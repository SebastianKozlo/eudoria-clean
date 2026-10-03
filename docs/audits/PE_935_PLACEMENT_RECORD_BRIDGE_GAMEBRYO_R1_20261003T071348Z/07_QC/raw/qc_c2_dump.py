#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC helper: dump C2_CALLER_CENSUS structure + verify census denominators."""
import json
import os
import sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
j = json.load(open(os.path.join(PKG, "01_RAW", "C2_CALLER_CENSUS.json"), encoding="utf-8"))
out = []


def walk(d, pfx=""):
    for k, v in d.items():
        if isinstance(v, dict):
            out.append("%s%s (dict, %d keys)" % (pfx, k, len(v)))
            if pfx.count(".") < 1:
                walk(v, pfx + k + ".")
        elif isinstance(v, list):
            out.append("%s%s (list, %d) head=%s" % (pfx, k, len(v), v[:6]))
        else:
            out.append("%s%s = %s" % (pfx, k, str(v)[:160]))


walk(j)
txt = "\n".join(out)
with open(os.path.join(PKG, "07_QC", "raw", "C2_STRUCTURE_DUMP.txt"), "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[:12000])
