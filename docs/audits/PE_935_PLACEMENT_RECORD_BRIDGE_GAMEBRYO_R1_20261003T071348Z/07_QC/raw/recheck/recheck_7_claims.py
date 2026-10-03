#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 7 (Task 6): untouched-claim presence/consistency check in the CURRENT
DRAFT_FINAL_REPORT.md. The repair round must not have altered any of these."""
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck7_claims.json")

with open(os.path.join(PKG, "06_REPORT", "DRAFT_FINAL_REPORT.md"), encoding="utf-8-sig") as f:
    txt = f.read()
norm = re.sub(r"\s+", " ", txt)

checks = {
    "RESULT_LEVEL = B (PARTIAL RESOURCE/SCENE CHAIN)": "RESULT_LEVEL = B (PARTIAL RESOURCE/SCENE CHAIN)",
    "MODEL_RESOURCE_EDGE = CONFIRMED": "MODEL_RESOURCE_EDGE = CONFIRMED for record 4508",
    "INSTANCE_IDENTITY world-instance NOT ESTABLISHED": "world-instance identity from a physical record NOT ESTABLISHED (CONTROL-2 FAIL -> UNKNOWN)",
    "PERSISTENT_PLACEMENT_EDGE = NOT ESTABLISHED": "PERSISTENT_PLACEMENT_EDGE = NOT ESTABLISHED",
    "MODEL_ID_RECOVERED = YES": "MODEL_ID_RECOVERED = YES",
    "PLACEMENT_XYZ_RECOVERED = NO": "PLACEMENT_XYZ_RECOVERED = NO",
    "962/962": "962/962",
    "113/113": "113/113",
    "FUNCTIONS_DETAILED 88 limit 120": "FUNCTIONS_DETAILED_COUNT = 88 (limit 120",
    "RECORDS_DETAILED 3 limit 3": "RECORDS_DETAILED_COUNT = 3",
    "3/3 oracle mechanisms": "3/3 oracle mechanisms",
    "3/3 records": "3/3 records",
    "COVERAGE census 45 breakdown": "45 = 19+10+4+8+4 census-target caller enumerations",
    "CROSSCHECKS 45 breakdown": "(45 target enumerations with denominators = 19+10+4+8+4)",
    "C2/C4/C5/C6/C8 denominators named": "C2/C4/C5/C6/C8 JSONs",
}
res = {k: (v in norm) for k, v in checks.items()}
res["count_962_962"] = norm.count("962/962")
res["count_113_113"] = norm.count("113/113")
res["count_88_of_120"] = norm.count("88/120") + norm.count("88 (limit 120")
res["count_45_breakdown"] = norm.count("19+10+4+8+4")
res["ALL_PRESENT"] = all(v for k, v in res.items() if k not in ("ALL_PRESENT",) and isinstance(v, bool))
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
