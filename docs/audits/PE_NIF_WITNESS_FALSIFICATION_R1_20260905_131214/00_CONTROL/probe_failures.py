#!/usr/bin/env python3
"""Probe failure details (encoding-safe)."""
import sys
import json
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source")
from pe_nif_reader import PENifReader  # noqa: E402

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_FALSIFICATION_R1_20260905_131214"
SB = RUN + r"\01_RAW\SANDBOX"
out = {}
for tag in ("MILD-2_424276", "MILD-3_500078", "SCRAMBLE-2_424276", "SCRAMBLE-3_500078"):
    raw = open(SB + "\\" + tag + ".bin", "rb").read()
    r = PENifReader().parse_bytes(raw, source_name=tag)
    rec = {"parse_status": getattr(r, "parse_status", None)}
    for k in dir(r):
        kl = k.lower()
        if any(w in kl for w in ("fail", "error")) and not k.startswith("_"):
            try:
                v = getattr(r, k)
            except Exception:
                continue
            if callable(v):
                continue
            try:
                json.dumps(v)
            except Exception:
                v = repr(v)
            rec[k] = v if isinstance(v, str) else json.loads(json.dumps(v, default=str))
    out[tag] = rec

with open(RUN + r"\01_RAW\FAILURE_DETAILS.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, default=str)
print(json.dumps(out, indent=1, default=str)[:2500])
