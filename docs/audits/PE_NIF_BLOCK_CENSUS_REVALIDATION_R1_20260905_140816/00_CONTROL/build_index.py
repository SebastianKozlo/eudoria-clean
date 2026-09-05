#!/usr/bin/env python3
"""artifact_index builder for RUN-F (real SHA-256; self-exclusion documented)."""
import os
import hashlib

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_BLOCK_CENSUS_REVALIDATION_R1_20260905_140816"


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
    for fn in sorted(files):
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, RUN).replace("\\", "/")
        if rel == "artifact_index.csv":
            continue
        rows.append((rel, sha(p)))
with open(os.path.join(RUN, "artifact_index.csv"), "w") as f:
    f.write("artifact,sha256,publication_scope\n")
    for rel, h in rows:
        f.write(f"{rel},{h},PUBLISHED\n")
print(f"artifact_index: {len(rows)} rows (self-exclusion documented)")
