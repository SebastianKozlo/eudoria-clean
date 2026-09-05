#!/usr/bin/env python3
"""Build artifact_index.csv (REAL SHA-256, sandbox = LOCAL_ONLY identity metadata)."""
import os
import hashlib

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_FALSIFICATION_R1_20260905_131214"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


rows = []
for root, dirs, files in os.walk(RUN):
    dirs[:] = [d for d in dirs if d not in ("SANDBOX",)]
    for fn in sorted(files):
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, RUN).replace("\\", "/")
        if rel == "artifact_index.csv":
            continue  # self-exclusion documented
        role = "package file"
        if rel.startswith("00_CONTROL/"):
            role = "control/driver (hash-after-last-edit recorded in SHA256_DRIVER.txt)"
        elif rel.startswith("01_RAW/"):
            role = "raw results (LOCAL run tree; publication excludes SANDBOX payloads)"
        elif rel.startswith("05_ANALYSIS/"):
            role = "analysis (verdicts)"
        elif rel.startswith("06_REPORT/"):
            role = "final report"
        rows.append((rel, role, sha(p)))
sb = os.path.join(RUN, "01_RAW", "SANDBOX")
for fn in sorted(os.listdir(sb)):
    p = os.path.join(sb, fn)
    rel = "01_RAW/SANDBOX/" + fn
    size = os.path.getsize(p)
    rows.append((rel, f"LOCAL_ONLY sandbox variant (NOT published; identity metadata only; {size} B)", sha(p)))

with open(os.path.join(RUN, "artifact_index.csv"), "w") as f:
    f.write("artifact,role,sha256,publication_scope\n")
    for rel, role, h in rows:
        scope = "LOCAL_ONLY" if "SANDBOX" in rel else "PUBLISHED"
        f.write(f"{rel},{role},{h},{scope}\n")
print(f"artifact_index: {len(rows)} rows ({sum(1 for r in rows if r[0].startswith('01_RAW/SANDBOX'))} LOCAL_ONLY sandbox)")
