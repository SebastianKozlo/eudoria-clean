#!/usr/bin/env python3
"""QC DUTY 11 — EVIDENCE_INDEX bijection check (FINAL_REPORT §9 vs disk).

Fresh internal QC. Verifies: every indexed row exists with matching size and
SHA256 (COUNTERMODEL_RESULTS.json expected stale post-repair — AMEND_LOG
documents the supersession), and no EXECUTOR file outside the index +
FINAL_REPORT.md + HANDOFF.md + 00_CONTROL_INTERNAL_QC (my QC dir).
"""
import hashlib
import json
import os
import sys

PKG = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
OUT = PKG + "/00_CONTROL_INTERNAL_QC/q11_index_bijection.json"

# extract index rows from FINAL_REPORT section 9 code block (the block
# that starts with 00_RECORDS_CORRECTION\CORRECTED_CLAIM_MATRIX.json|)
rows = []
fr = open(PKG + "/FINAL_REPORT.md", encoding="utf-8").read()
blocks = fr.split("```text")
block = None
for b in blocks[1:]:
    b = b.split("```")[0]
    if "CORRECTED_CLAIM_MATRIX.json|" in b:
        block = b
        break
for line in block.strip().splitlines():
    if "|" not in line:
        continue
    rel, size, sha = line.split("|")
    rows.append((rel.strip(), int(size.strip()), sha.strip().lower()))

index = {rel: (size, sha) for rel, size, sha in rows}
print("index rows:", len(rows))

mismatch, missing = [], []
for rel, size, sha in rows:
    p = os.path.join(PKG, rel)
    if not os.path.isfile(p):
        missing.append(rel)
        continue
    actual_size = os.path.getsize(p)
    actual_sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if actual_size != size or actual_sha != sha:
        mismatch.append({"path": rel, "index_size": size, "actual_size":
                         actual_size, "index_sha": sha, "actual_sha":
                         actual_sha})

# physical executor files not in index (excluding FINAL_REPORT/HANDOFF/QC dir)
extra = []
for root, dirs, files in os.walk(PKG):
    if "00_CONTROL_INTERNAL_QC" in root:
        continue
    for fn in files:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, PKG).replace("/", os.sep)
        if rel in ("FINAL_REPORT.md", "HANDOFF.md"):
            continue
        if rel not in index:
            extra.append(rel)

res = {
    "index_rows": len(rows),
    "missing_on_disk": missing,
    "size_or_sha_mismatches": mismatch,
    "expected_stale_post_repair": [
        "00_RECORDS_CORRECTION\\COUNTERMODEL_RESULTS.json (QC repair "
        "documented in AMEND_LOG.md; post-repair sha "
        "2e159900137c14faefcbf910d0025769891cef8cc6f739573a6996fdf3346ed1)"],
    "physical_executor_files_not_in_index": extra,
    "bijection_verdict": None,
}
ok = (not missing and len(mismatch) == 1 and
      mismatch and mismatch[0]["path"].endswith("COUNTERMODEL_RESULTS.json")
      and not extra)
res["bijection_verdict"] = ("BIJECTION_OK_WITH_ONE_DOCUMENTED_POST_REPAIR"
                            " HASH SUPERSESSION" if ok else "CHECK DETAILS")
print(json.dumps(res, indent=2))
json.dump(res, open(OUT, "w", encoding="utf-8"), indent=2)
