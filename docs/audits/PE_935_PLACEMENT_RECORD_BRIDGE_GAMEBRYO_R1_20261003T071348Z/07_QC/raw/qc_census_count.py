#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC helper 3: count census targets in C4/C5/C6/C8 + C2, verify the
'19+10+8+4+4+8+4+12 = 69 census-target' claim and the '45' NOT_CHECKED number."""
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
total = 0
for fn in ("C2_CALLER_CENSUS.json", "C4_CONSTRUCTION_TRACE.json",
           "C5_LAYOUT_AND_DRIVERS.json", "C6_DRIVER_SOURCES.json",
           "C8_TOP_SOURCES.json"):
    j = json.load(open(os.path.join(PKG, "01_RAW", fn), encoding="utf-8"))
    m = j.get("measured", {})
    cen = m.get("census")
    if fn == "C2_CALLER_CENSUS.json":
        n = len(m.get("targets", {}))
        print("%s targets=%d" % (fn, n))
        total += n
    elif cen is not None:
        if isinstance(cen, dict):
            keys = list(cen.keys())
            print("%s census dict keys=%d: %s" % (fn, len(keys), keys[:30]))
            total += len(keys)
        elif isinstance(cen, list):
            print("%s census list len=%d" % (fn, len(cen)))
            total += len(cen)
    else:
        print("%s NO census key; measured keys=%s" % (fn, list(m.keys())))
print("TOTAL census targets:", total)
