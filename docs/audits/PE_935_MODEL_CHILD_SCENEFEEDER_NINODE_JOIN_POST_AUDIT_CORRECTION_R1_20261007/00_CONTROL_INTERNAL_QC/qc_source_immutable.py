# qc_source_immutable.py — INDEPENDENT re-hash of the SOURCE_RUN_PACKAGE (read-only QC).
# PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007
# Internal QC worker: pe-master-auditor (fresh context, NO_NESTED_TASKS).
#
# Purpose: verify the historical source package at BASE 064b7f4 is IMMUTABLE:
#   - enumerate its files via `git ls-tree -r BASE` (the authoritative BASE blobs);
#   - recompute the git blob SHA-1 of every PHYSICAL file (own code, hashlib sha1 of
#     b"blob <len>\x00" + bytes) and compare with the BASE blob ids;
#   - recompute the package aggregate SHA256 (sorted "path sha256" lines digest)
#     and compare with the executor-recorded value ab21cbc3...;
#   - specifically re-verify 01_RAW/FUN_00509850_FULL.txt (the J3 physical record);
#   - verify the historical qualification_gate.py SHA256 equals the EF2D8E1F... identity
#     (the gate the Desktop executed) — READ-ONLY reference, never executed for verdicts here.
# No writes outside 00_CONTROL_INTERNAL_QC. No new RE. Read-only.
import hashlib
import os
import subprocess
import sys

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
SRC_PREFIX = "docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/"
BASE = "064b7f4aa4f3961f1a44212b2423e298eb51c291"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_source_immutable.json")

res = {"files": [], "counts": {}, "checks": {}}

out = subprocess.run(["git", "ls-tree", "-r", BASE, "--", SRC_PREFIX],
                     cwd=REPO, capture_output=True, text=True)
if out.returncode != 0:
    print("git ls-tree failed: " + out.stderr)
    sys.exit(2)
blob_rows = []
for line in out.stdout.splitlines():
    if not line.strip():
        continue
    meta, path = line.split("\t")
    _mode, typ, gsha = meta.split()
    assert typ == "blob"
    blob_rows.append((path, gsha))

mismatch = []
missing = []
digest_lines = []
for path, gsha in blob_rows:
    fp = os.path.join(REPO, *path.split("/"))
    if not os.path.isfile(fp):
        missing.append(path)
        continue
    b = open(fp, "rb").read()
    bsha = hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()
    sha256 = hashlib.sha256(b).hexdigest()
    ok = (bsha == gsha)
    if not ok:
        mismatch.append(path)
    digest_lines.append(path + " " + sha256)
    res["files"].append({"path": path, "git_blob_sha1_base": gsha,
                         "physical_blob_sha1": bsha, "sha256": sha256,
                         "size": len(b), "identical": ok})

agg = hashlib.sha256(("\n".join(sorted(digest_lines)) + "\n").encode()).hexdigest()
res["counts"] = {
    "base_blob_rows": len(blob_rows),
    "physical_files": len(digest_lines),
    "missing": missing,
    "blob_mismatches": mismatch,
    "aggregate_sha256": agg,
}
res["checks"] = {
    "count_is_49": len(blob_rows) == 49,
    "all_physical_present": not missing,
    "all_blobs_identical": not mismatch,
    "aggregate_matches_executor_record":
        agg == "ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b",
}

# J3a focus file + the historical gate identity (read-only reference checks)
f509850 = os.path.join(REPO, *("docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/"
                               "01_RAW/FUN_00509850_FULL.txt").split("/"))
b = open(f509850, "rb").read()
gate = os.path.join(REPO, *("docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/"
                            "03_SCRIPTS/qualification_gate.py").split("/"))
gb = open(gate, "rb").read()
res["checks"]["fun_00509850_full_identical_to_base_blob"] = any(
    f["path"].endswith("01_RAW/FUN_00509850_FULL.txt") and f["identical"] for f in res["files"])
res["checks"]["historical_gate_sha256_ef2d8e1f"] = \
    hashlib.sha256(gb).hexdigest().upper() == \
    "EF2D8E1F01D63BD004CC8F4087BDBC8194F51EACC38579DC0B2AC2FCDCC400AD"
res["checks"]["historical_pe_master_review_identical"] = any(
    f["path"].endswith("PE_MASTER_REVIEW.md") and f["identical"] for f in res["files"])

overall = all(res["checks"].values())
res["OVERALL"] = "PASS" if overall else "FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    import json
    json.dump(res, fh, indent=2)
    fh.write("\n")
print("files=%d missing=%d blob_mismatch=%d agg=%s OVERALL=%s"
      % (len(blob_rows), len(missing), len(mismatch), agg[:12], res["OVERALL"]))
