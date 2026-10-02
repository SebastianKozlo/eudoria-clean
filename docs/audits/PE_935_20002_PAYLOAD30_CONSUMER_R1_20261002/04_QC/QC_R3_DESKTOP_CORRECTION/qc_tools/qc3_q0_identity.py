#!/usr/bin/env python3
# QC-R3 Q0: identity + starting-manifest vs disk census (fresh independent QC tool; no executor code)
# Writes QC_R3_Q0_IDENTITY_RESULT.json next to the package 04_QC/QC_R3_DESKTOP_CORRECTION dir.
import hashlib, json, os, sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
CONTRACT = os.path.join(PKG, "00_CONTROL", "DESKTOP_CORRECTION_R1", "CORRECTION_RUN_CONTRACT.md")
MANIFEST = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")

PIN = {
    "contract_sha256": "1E592EBC056FD4110EB8151C92872DDBEF744755FF3AAB50C1A87CAFFABFE557",
    "exe_sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "exe_size": 8015872,
    "vfs_sha256": "C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4",
    "vfs_size": 174864,
    "manifest_sha256": "CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF",
    "manifest_size": 50698,
    "base_sha": "9203b6d1ad5025f4158d5165863594132aaac49f",
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

res = {"q": "Q0", "pin_checks": {}, "manifest_census": {}, "protected_files": {}, "errors": []}

def pin_check(name, path, sha, size=None):
    ok_path = os.path.isfile(path)
    s = sha256_file(path) if ok_path else None
    sz = os.path.getsize(path) if ok_path else None
    entry = {"exists": ok_path, "measured_sha256": s, "pinned_sha256": sha,
             "sha_match": (s == sha) if ok_path else False,
             "measured_size": sz, "pinned_size": size,
             "size_match": (sz == size) if (ok_path and size is not None) else None}
    res["pin_checks"][name] = entry
    return entry["sha_match"]

pin_check("contract", CONTRACT, PIN["contract_sha256"])
pin_check("exe", EXE, PIN["exe_sha256"], PIN["exe_size"])
pin_check("vfs", VFS, PIN["vfs_sha256"], PIN["vfs_size"])
pin_check("starting_manifest", MANIFEST, PIN["manifest_sha256"], PIN["manifest_size"])

# HEAD check is done by the caller (git) - we record the pinned value only.
res["pin_checks"]["head_base_sha"] = {"pinned": PIN["base_sha"], "verified_by": "git rev-parse HEAD (run separately)"}

# ---- parse starting manifest (frozen reference; still byte-unchanged => parse of current bytes == parse of frozen bytes)
rows = []
with open(MANIFEST, "r", encoding="utf-8-sig") as f:
    lines = f.read().splitlines()
header = lines[0].split(",")
assert header[:4] == ["file", "size_bytes", "sha256", "origin"], f"unexpected header: {header}"
for ln in lines[1:]:
    if not ln.strip():
        continue
    if ln.startswith("NOTE,,,,") or ln.startswith("NOTE,"):
        res["manifest_census"]["note_row"] = ln
        continue
    parts = ln.split(",")
    # note fields may contain commas; data rows have file,size,sha,origin[,note]
    rows.append({"rel": parts[0], "size": int(parts[1]), "sha": parts[2].upper(), "origin": parts[3],
                 "note": ",".join(parts[4:]) if len(parts) > 4 else ""})

res["manifest_census"]["data_row_count"] = len(rows)
res["manifest_census"]["total_text_lines"] = len(lines)

# ---- compare each manifest row with the CURRENT disk file
identical, changed, missing, mismatched_size_only = [], [], [], []
for r in rows:
    p = os.path.join(PKG, *r["rel"].split("/"))
    if not os.path.isfile(p):
        missing.append(r["rel"])
        continue
    sz = os.path.getsize(p)
    s = sha256_file(p)
    if s == r["sha"]:
        identical.append(r["rel"])
    else:
        rec = {"rel": r["rel"], "manifest_sha": r["sha"], "disk_sha": s,
               "manifest_size": r["size"], "disk_size": sz}
        changed.append(rec)

res["manifest_census"]["identical_count"] = len(identical)
res["manifest_census"]["changed_count"] = len(changed)
res["manifest_census"]["missing_count"] = len(missing)
res["manifest_census"]["changed_files"] = changed
res["manifest_census"]["missing_files"] = missing

# ---- files on disk NOT in manifest (delta; includes manifest itself by self-exclusion + new correction artifacts)
on_disk = set()
for root, dirs, files in os.walk(PKG):
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), PKG).replace("\\", "/")
        on_disk.add(rel)
manifest_set = set(r["rel"] for r in rows)
new_files = sorted(on_disk - manifest_set - {"06_REPORT/MANIFEST_SHA256.csv"})
res["manifest_census"]["disk_file_total"] = len(on_disk)
res["manifest_census"]["new_files_not_in_manifest"] = new_files
res["manifest_census"]["new_file_count"] = len(new_files)
# note: my own QC_R3 writes are inside QC dir - count them separately at end of this run

# ---- protected files: must be byte-unchanged (identical per manifest rows above)
protected = [
    "01_RAW/CLIENT_READ_BYTES.json",
    "04_QC/QC_REPORT.md",
    "04_QC/QC1_REPARSE_RESULT.json",
    "04_QC/QC2_PINVERIFY_RESULT.json",
    "04_QC/QC3_NEGCONTROLS_RESULT.json",
    "04_QC/QC4B_CANONCONFLICT_PROBE.json",
    "04_QC/QC4_RTTI_EDGES_RESULT.json",
    "04_QC/QC5_DENOMINATORS_RESULT.json",
    "04_QC/QC_COUNTERCHECK_INDEX.md",
    "04_QC/QC_R2_BYTEFACTS_RESULT.json",
    "04_QC/QC_R2_DIFF_CENSUS_RESULT.json",
    "04_QC/QC_R2_SPAN_CHECK_RESULT.json",
    "04_QC/QC_R2_TARGETED_REPORT.md",
    "04_QC/QC_R2_VFS_WALK_RESULT.json",
    "04_QC/qc_tools",
    "00_CONTROL/RUN_CONTRACT.md",
    "00_CONTROL/CONTRACT_FREEZE.json",
    "00_CONTROL/DESKTOP_CORRECTION_R1/CORRECTION_RUN_CONTRACT.md",
    "00_CONTROL/DESKTOP_CORRECTION_R1/CORRECTION_CONTRACT_FREEZE.json",
    "00_CONTROL/DESKTOP_CORRECTION_R1/PRE_CORRECTION_STATE.md",
    "06_REPORT/PE_MASTER_REVIEW.md",
    "06_REPORT/MANIFEST_SHA256.csv",
]
prot_res = {}
for pr in protected:
    if pr.endswith("qc_tools") or pr.endswith("/"):
        # directory protection: check no manifest-listed file under it changed
        sub = [r["rel"] for r in rows if r["rel"].startswith(pr + "/")]
        ok = all(r["rel"] in identical for r in rows if r["rel"].startswith(pr + "/"))
        prot_res[pr] = {"protected_file_count": len(sub), "all_unchanged": ok}
    else:
        row = next((r for r in rows if r["rel"] == pr), None)
        if row is None:
            prot_res[pr] = {"in_manifest": False, "status": "NOT_IN_MANIFEST"}
        else:
            prot_res[pr] = {"in_manifest": True, "unchanged": row["rel"] in identical,
                            "manifest_sha": row["sha"],
                            "disk_sha": sha256_file(os.path.join(PKG, *pr.split("/")))}
res["protected_files"] = prot_res

out = os.path.join(QC_DIR, "QC_R3_Q0_IDENTITY_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps({"identical": len(identical), "changed": len(changed), "missing": len(missing),
                  "changed_files": [c["rel"] for c in changed],
                  "new_files": len(new_files), "disk_total": len(on_disk),
                  "protected_all_ok": all(
                      (v.get("unchanged") if "unchanged" in v else v.get("all_unchanged"))
                      for v in prot_res.values())}, indent=2))
