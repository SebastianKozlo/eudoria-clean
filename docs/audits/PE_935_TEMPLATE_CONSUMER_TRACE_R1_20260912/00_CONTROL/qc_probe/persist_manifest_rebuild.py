#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PERSIST F2/F3 (pe-master-auditor, RUN_ID: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST):
artifact_index.csv manifest rebuild, per QC findings F2 (P3) + F3 (P3) + PE-MASTER order.

F2: remove the self-row (06_REPORT\artifact_index.csv,...) - a manifest cannot contain
    its own hash (L12 precedent; the row was stale by construction: 64694/B922E31C...
    vs actual 65003/00C6DB50... at QC time).
F3: add the missing row 06_REPORT\HANDOFF.md (hash from disk, post-F4 state).
Disclosure: rows of the 4 files intentionally changed by F1/F4
    (02_ANALYSIS\B_template_loading_chain.md, 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md,
     06_REPORT\00_FINAL_REPORT.md, 06_REPORT\STAGE_ACCEPTANCE_GATES.csv)
    are re-hashed to the post-correction state; leaving stale hashes would recreate
    the F2 defect class for deliberately changed files.

Encoding preserved: UTF-8 BOM + CRLF line endings (verified pre-work).
Writes: 06_REPORT\artifact_index.csv (rebuild) + persist_manifest_rebuild_result.json
"""
import hashlib
import json
import os
import sys

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
IDX = os.path.join(RUN, "06_REPORT", "artifact_index.csv")
OUT = os.path.join(RUN, "00_CONTROL", "qc_probe", "persist_manifest_rebuild_result.json")

SELF_ROW_PREFIX = "06_REPORT\\artifact_index.csv,"
UPDATED = [
    "02_ANALYSIS\\B_template_loading_chain.md",
    "03_EVIDENCE\\VA_EVIDENCE_REGISTRY.md",
    "06_REPORT\\00_FINAL_REPORT.md",
    "06_REPORT\\STAGE_ACCEPTANCE_GATES.csv",
]
NEW_ROW = "06_REPORT\\HANDOFF.md"

with open(IDX, "rb") as f:
    raw = f.read()
if not raw.startswith(b"\xef\xbb\xbf"):
    print("FATAL: manifest lost its UTF-8 BOM pre-check"); sys.exit(2)
text = raw.decode("utf-8-sig")
lines = text.split("\r\n")
if lines and lines[-1] == "":
    lines = lines[:-1]  # trailing CRLF produces an empty tail element
header, rows = lines[0], lines[1:]
res = {"probe": "persist_manifest_rebuild", "errors": [], "header": header,
       "rows_before": len(rows), "old_rows": {}, "removed_rows": [], "updated_rows": {}, "new_rows": {}}

# F2: remove self-row
kept = []
for ln in rows:
    if ln.startswith(SELF_ROW_PREFIX):
        res["removed_rows"].append(ln)
    else:
        kept.append(ln)
rows = kept

# re-hash rows for F1/F4-changed files + build the new HANDOFF row
def row_for(rel):
    p = os.path.join(RUN, *rel.split("\\"))
    with open(p, "rb") as f:
        data = f.read()
    return "%s,%d,%s" % (rel, len(data), hashlib.sha256(data).hexdigest().upper())

for rel in UPDATED:
    old = [ln for ln in rows if ln.startswith(rel + ",")]
    new = row_for(rel)
    res["updated_rows"][rel] = {"old": old[0] if old else None, "new": new}
    if not old:
        res["errors"].append("missing manifest row to update: %s" % rel)
    else:
        idx = rows.index(old[0])
        rows[idx] = new

# F3: add HANDOFF row if absent (idempotent: on re-run, re-hash the existing row instead)
existing_handoff = [ln for ln in rows if ln.startswith(NEW_ROW + ",")]
new_handoff = row_for(NEW_ROW)
if existing_handoff:
    res["new_rows"][NEW_ROW] = {"already_present": existing_handoff[0], "refreshed": new_handoff}
    rows[rows.index(existing_handoff[0])] = new_handoff
else:
    res["new_rows"][NEW_ROW] = new_handoff
    # case-insensitive sort position within the 06_REPORT block (00_FINAL_REPORT < HANDOFF < STAGE_ACCEPTANCE_GATES)
    insert_at = len(rows)
    for i, ln in enumerate(rows):
        if ln.lower() > new_handoff.lower():
            insert_at = i
            break
    rows.insert(insert_at, new_handoff)

# write back: BOM + CRLF, trailing CRLF
out_text = "\r\n".join([header] + rows) + "\r\n"
with open(IDX, "wb") as f:
    f.write(b"\xef\xbb\xbf" + out_text.encode("utf-8"))
res["rows_after"] = len(rows)

# verification pass: re-read, count, self-row absence, HANDOFF presence, all rows exist on disk
with open(IDX, "rb") as f:
    raw2 = f.read()
ok_bom = raw2.startswith(b"\xef\xbb\xbf")
text2 = raw2.decode("utf-8-sig")
lines2 = [ln for ln in text2.split("\r\n") if ln != ""]
header2, rows2 = lines2[0], lines2[1:]
res["verify"] = {
    "bom_preserved": ok_bom,
    "crlf_only": b"\n" not in raw2.replace(b"\r\n", b""),
    "rows_final": len(rows2),
    "self_row_absent": not any(ln.startswith(SELF_ROW_PREFIX) for ln in rows2),
    "handoff_row_present": any(ln.startswith(NEW_ROW + ",") for ln in rows2),
    "all_rows_exist_on_disk": all(os.path.exists(os.path.join(RUN, *ln.split(",", 1)[0].split("\\"))) for ln in rows2),
    "manifest_sha256_after": hashlib.sha256(raw2).hexdigest().upper(),
    "manifest_size_after": len(raw2),
}
for k, v in res["verify"].items():
    print("%-22s %s" % (k, v))
if not all([res["verify"]["bom_preserved"], res["verify"]["crlf_only"], res["verify"]["self_row_absent"],
            res["verify"]["handoff_row_present"], res["verify"]["all_rows_exist_on_disk"]]):
    res["errors"].append("verification failed: %r" % res["verify"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print("result -> %s" % OUT)
sys.exit(1 if res["errors"] else 0)
