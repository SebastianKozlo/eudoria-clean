# -*- coding: utf-8 -*-
# Extract hexdump fields from T2 JSON into separate .txt files for reading.
import json
import os

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
SRC = os.path.join(RUN_ROOT, "01_RAW", "T2_INSERT_SEAM.json")
DST = os.path.join(RUN_ROOT, "01_RAW", "T2_HEX")

with open(SRC) as f:
    data = json.load(f)

os.makedirs(DST, exist_ok=True)
m = data["measured"]
for k, v in m.items():
    if k.startswith("hex_"):
        name = k[4:] + ".txt"
        with open(os.path.join(DST, name), "w") as f:
            f.write(v)
        print(name)
# call edges of the insert function -> txt
if "caller_call_edges" in m:
    with open(os.path.join(DST, "INSERT_FUN_00528E50_call_edges.txt"), "w") as f:
        for e in m["caller_call_edges"]:
            f.write("%s @%s -> %s\n" % (e["op"], e["site_va"], e["target"]))
    print("INSERT_FUN_00528E50_call_edges.txt")
print("done")
