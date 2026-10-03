#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC helper 2: dump C2 targets detail + census counts + decompilations."""
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
j = json.load(open(os.path.join(PKG, "01_RAW", "C2_CALLER_CENSUS.json"), encoding="utf-8"))
lines = []
t = j["measured"]["targets"]
for k, v in t.items():
    if isinstance(v, dict):
        meta = {kk: vv for kk, vv in v.items() if not isinstance(vv, (list, dict))}
        lists = {kk: len(vv) for kk, vv in v.items() if isinstance(vv, list)}
        lines.append("%s :: meta=%s lists=%s" % (k, meta, lists))
        # print caller site lists fully for key targets
        for kk, vv in v.items():
            if isinstance(vv, list) and kk in ("call_sites", "callers", "sites",
                                              "unique_callers", "caller_sites"):
                lines.append("    %s (%d): %s" % (kk, len(vv),
                             ", ".join(str(x) for x in vv[:40])))
            if isinstance(vv, list) and kk not in ("call_sites", "callers", "sites",
                                                   "unique_callers", "caller_sites"):
                lines.append("    %s (%d): %s" % (kk, len(vv),
                             ", ".join(str(x) for x in vv[:40])))
dec = j["measured"]["decompilations"]
for k, v in dec.items():
    lines.append("DECOMP %s entry=%s ok=%s c_lines=%s" % (
        k, v.get("function_entry"), v.get("ok"), v.get("c_line_count")))
    # write full C
    p = os.path.join(PKG, "07_QC", "raw", "decomp_dump", "C2_CALLER_CENSUS__" + k + ".c")
    with open(p, "w", encoding="utf-8") as f:
        f.write("// source: C2_CALLER_CENSUS.json :: %s\n" % k)
        f.write(v.get("c", ""))

txt = "\n".join(lines)
with open(os.path.join(PKG, "07_QC", "raw", "C2_TARGETS_DUMP.txt"), "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[:20000])
