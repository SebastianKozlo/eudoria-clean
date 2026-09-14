# -*- coding: utf-8 -*-
# Extract readable hexdumps from T2C JSON.
import json
import os

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
SRC = os.path.join(RUN_ROOT, "01_RAW", "T2C_INSERT_HELPER.json")
DST = os.path.join(RUN_ROOT, "01_RAW", "T2C_HEX")

with open(SRC) as f:
    data = json.load(f)
os.makedirs(DST, exist_ok=True)
for k, v in data["measured"].items():
    if k.startswith("hex_") and isinstance(v, str):
        with open(os.path.join(DST, k[4:] + ".txt"), "w") as f:
            f.write(v)
        print(k[4:] + ".txt")
print("done")
