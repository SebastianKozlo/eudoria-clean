#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC helper 5: dump per-target census denominators from C4/C5/C6/C8."""
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
out = []
for fn in ("C4_CONSTRUCTION_TRACE.json", "C5_LAYOUT_AND_DRIVERS.json",
           "C6_DRIVER_SOURCES.json", "C8_TOP_SOURCES.json"):
    j = json.load(open(os.path.join(PKG, "01_RAW", fn), encoding="utf-8"))
    cen = j["measured"].get("census", {})
    for k, v in cen.items():
        if isinstance(v, dict):
            meta = {kk: vv for kk, vv in v.items() if not isinstance(vv, (list, dict))}
            cl = v.get("caller_list", [])
            callers = []
            for c in cl:
                if isinstance(c, dict):
                    callers.append("%s(%d sites)" % (c.get("caller_entry"),
                                                     c.get("callsite_count", len(c.get("callsites", [])))))
                else:
                    callers.append(str(c))
            out.append("%s :: %s :: %s :: callers=%s" % (fn, k, meta, "; ".join(callers)))
        else:
            out.append("%s :: %s :: %s" % (fn, k, str(v)[:200]))

txt = "\n".join(out)
p = os.path.join(PKG, "07_QC", "raw", "CENSUS_TARGETS_DUMP.txt")
with open(p, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt)
