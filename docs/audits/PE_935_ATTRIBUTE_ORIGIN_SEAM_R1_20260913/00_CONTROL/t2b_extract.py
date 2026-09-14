# -*- coding: utf-8 -*-
# Extract readable hexdumps + edges from T2B JSON.
import json
import os

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
SRC = os.path.join(RUN_ROOT, "01_RAW", "T2B_DERIVED_INSERT_HUNT.json")
DST = os.path.join(RUN_ROOT, "01_RAW", "T2B_HEX")

with open(SRC) as f:
    data = json.load(f)

os.makedirs(DST, exist_ok=True)
m = data["measured"]
for k, v in m.items():
    if k.startswith("hex_") and isinstance(v, str):
        with open(os.path.join(DST, k[4:] + ".txt"), "w") as f:
            f.write(v)
        print(k)
for e in m.get("derived_ctor_callers", []):
    fn = e.get("func_start", "").replace("0x", "")
    if "hexdump" in e:
        with open(os.path.join(DST, "CALLER_%s_hexdump.txt" % fn), "w") as f:
            f.write(e["hexdump"])
        print("CALLER_%s_hexdump.txt" % fn)
    if "call_edges" in e:
        with open(os.path.join(DST, "CALLER_%s_edges.txt" % fn), "w") as f:
            for x in e["call_edges"]:
                f.write("%s @%s -> %s\n" % (x["op"], x["site_va"], x["target"]))
        print("CALLER_%s_edges.txt" % fn)
    if "callers_of_this" in e:
        with open(os.path.join(DST, "CALLER_%s_callers.txt" % fn), "w") as f:
            for x in e["callers_of_this"]:
                f.write("%s @%s\n" % (x["op"], x["site_va"]))
        print("CALLER_%s_callers.txt" % fn)
print("done")
