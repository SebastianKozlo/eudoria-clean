#!/usr/bin/env python3
# QC-R3 Q4: BEFORE-copy verification (each BEFORE copy must equal the STARTING MANIFEST row for
# its path = the frozen pre-correction bytes) + AMEND_LOG content verification.
import hashlib, json, os, re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")
BEFORE = os.path.join(PKG, "00_CONTROL", "DESKTOP_CORRECTION_R1", "BEFORE")
MANIFEST = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

# starting manifest rows (frozen reference)
rows = {}
with open(MANIFEST, "r", encoding="utf-8-sig") as f:
    for ln in f.read().splitlines()[1:]:
        if not ln.strip() or ln.startswith("NOTE"):
            continue
        parts = ln.split(",")
        rows[parts[0]] = {"size": int(parts[1]), "sha": parts[2].upper()}

res = {"q": "Q4_before_copies", "copies": {}, "census": {}}
before_files = []
for root, dirs, files in os.walk(BEFORE):
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), BEFORE).replace("\\", "/")
        before_files.append(rel)
before_files.sort()

ok_count = 0
for rel in before_files:
    if rel == "BEFORE_COPIES_INDEX.json":
        continue  # the index itself (not a BEFORE copy)
    p = os.path.join(BEFORE, *rel.split("/"))
    sz = os.path.getsize(p)
    sh = sha256_file(p)
    # the mirrored original path inside the package:
    orig_rel = rel
    row = rows.get(orig_rel)
    match = row is not None and row["sha"] == sh and row["size"] == sz
    res["copies"][rel] = {
        "before_size": sz, "before_sha256": sh,
        "starting_manifest_row": ({"size": row["size"], "sha256": row["sha"]} if row else None),
        "equals_starting_manifest": match,
    }
    ok_count += 1 if match else 0

res["census"] = {
    "before_copy_count": len([r for r in before_files if r != "BEFORE_COPIES_INDEX.json"]),
    "all_equal_starting_manifest": ok_count == len([r for r in before_files if r != "BEFORE_COPIES_INDEX.json"]),
    "mismatches": [k for k, v in res["copies"].items() if not v["equals_starting_manifest"]],
}

# ---- BEFORE_COPIES_INDEX.json consistency: its rows must match the actual BEFORE files
idx_path = os.path.join(BEFORE, "BEFORE_COPIES_INDEX.json")
with open(idx_path, "r", encoding="utf-8-sig") as f:
    idx = json.load(f)
idx_res = {"index_type": type(idx).__name__, "entries": 0, "entries_ok": 0, "problems": []}
entries = idx if isinstance(idx, list) else idx.get("copies", idx.get("before_copies", []))
if isinstance(idx, dict) and not entries:
    # maybe dict-of-path->data
    entries = [{"path": k, **v} if isinstance(v, dict) else {"path": k, "sha256": v} for k, v in idx.items() if k not in ("run_id", "artifact", "note")]
for e in entries:
    if not isinstance(e, dict):
        idx_res["problems"].append({"entry": e, "issue": "malformed entry (not a dict)"})
        continue
    rel = str(e.get("path") or e.get("relative_path") or "").replace("\\", "/")
    if not rel:
        idx_res["problems"].append({"entry": e, "issue": "malformed entry (no path/relative_path)"})
        continue
    # normalize: index may store package-relative or BEFORE-relative paths
    rel_norm = rel
    for prefix in ("00_CONTROL/DESKTOP_CORRECTION_R1/BEFORE/",):
        if rel_norm.startswith(prefix):
            rel_norm = rel_norm[len(prefix):]
    p = os.path.join(BEFORE, *rel_norm.split("/"))
    if not os.path.isfile(p):
        idx_res["problems"].append({"entry": e, "issue": "BEFORE file missing on disk"})
        continue
    sh = sha256_file(p)
    sz = os.path.getsize(p)
    idx_res["entries"] += 1
    claimed_sha = (e.get("sha256") or e.get("before_sha256") or "").upper()
    claimed_size = e.get("size_bytes", e.get("size"))
    if claimed_sha == sh and (claimed_size is None or claimed_size == sz):
        idx_res["entries_ok"] += 1
    else:
        idx_res["problems"].append({"entry": e, "on_disk": {"size": sz, "sha256": sh},
                                     "issue": "index row != disk file"})
res["before_copies_index"] = idx_res

# ---- AMEND_LOG content verification
amend_path = os.path.join(PKG, "06_REPORT", "AMEND_LOG_DESKTOP_CORRECTION_R1.md")
with open(amend_path, "r", encoding="utf-8-sig") as f:
    amend = f.read()
checks = {
    "has_desktop_finding": ("desktop" in amend.lower() and "finding" in amend.lower()),
    "has_superseded_claim": "superseded" in amend.lower() and ("00412540" in amend or "412553" in amend),
    "has_before_after_pairs": bool(re.search(r"BEFORE.*AFTER", amend, re.I) or ("BEFORE/AFTER" in amend)),
    "has_branch_selection_correction": "branch" in amend.lower() and "selection" in amend.lower(),
    "has_remaining_unknowns": "unknown" in amend.lower(),
    "has_affected_dependency_set": ("dependency" in amend.lower() or "affected" in amend.lower()),
    "has_lesson_line": "correct instruction bytes != proven selected execution/parser path" in amend,
    "has_qc1_qc2_superseded_conclusion": ("QC round 1" in amend or "QC1" in amend or "QC round" in amend) and ("superseded" in amend.lower()),
    "has_contradiction_census": "contradiction" in amend.lower(),
}
# BEFORE/AFTER pairs (path+size+SHA) matching disk: parse SHA256 mentions
sha_mentions = re.findall(r"\b([0-9A-Fa-f]{64})\b", amend)
size_sha_pairs = re.findall(r"(\d{2,6})\s*B?[^A-Za-z0-9]{0,40}?([0-9A-Fa-f]{64})", amend)
checks["has_sha256_pairs"] = len(sha_mentions) >= 20
res["amend_log"] = {"path": "06_REPORT/AMEND_LOG_DESKTOP_CORRECTION_R1.md",
                    "size": os.path.getsize(amend_path),
                    "sha256": sha256_file(amend_path),
                    "checks": checks,
                    "sha_mention_count": len(sha_mentions),
                    "all_checks_pass": all(checks.values())}

# every SHA256 mentioned in the AMEND_LOG that corresponds to a BEFORE path or a current file must be verifiable:
# verify that for the 10 corrected docs, the AMEND_LOG mentions BOTH a BEFORE sha and an AFTER sha,
# where BEFORE sha == starting manifest row and AFTER sha == current disk file.
pair_checks = []
for rel, v in res["copies"].items():
    cur = os.path.join(PKG, *rel.split("/"))
    cur_sha = sha256_file(cur)
    cur_size = os.path.getsize(cur)
    before_sha = v["before_sha256"]
    found_before = before_sha.upper() in [m.upper() for m in sha_mentions]
    found_after = cur_sha.upper() in [m.upper() for m in sha_mentions]
    pair_checks.append({"path": rel, "before_sha_in_log": found_before,
                        "after_sha_in_log": found_after,
                        "before_equals_manifest": v["equals_starting_manifest"]})
res["amend_log"]["pair_verification"] = pair_checks
res["amend_log"]["all_pairs_verified"] = all(pc["before_sha_in_log"] and pc["after_sha_in_log"] and pc["before_equals_manifest"] for pc in pair_checks)

out = os.path.join(QC_DIR, "QC_R3_BEFORE_COPIES_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps({"census": res["census"], "index": {k: v for k, v in idx_res.items() if k != 'problems'},
                  "index_problems": idx_res["problems"],
                  "amend_checks": checks, "amend_all_pass": res["amend_log"]["all_checks_pass"],
                  "all_pairs_verified": res["amend_log"]["all_pairs_verified"],
                  "pair_failures": [pc for pc in pair_checks if not (pc["before_sha_in_log"] and pc["after_sha_in_log"])]}, indent=2))
