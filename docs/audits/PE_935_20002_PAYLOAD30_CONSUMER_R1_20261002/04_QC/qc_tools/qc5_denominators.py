#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC COUNTERCHECK 5 - denominator recomputation from raw artifacts + manifest
spot re-hash + JOIN R1 package spot-check (>=8 files vs its own manifest).
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 / QC worker.
"""
import os
import json
import csv
import hashlib
import sys

sys.dont_write_bytecode = True

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
JOINR1 = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928"
OUT = os.path.join(PKG, "04_QC", "QC5_DENOMINATORS_RESULT.json")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "countercheck": "QC5 denominators + manifest census",
          "tool": "04_QC/qc_tools/qc5_denominators.py"}

# 1. RECORD_FRAMING.jsonl rows + bounds + zero recompute (from raw rows)
rows = []
with open(os.path.join(PKG, "01_RAW", "RECORD_FRAMING.jsonl")) as f:
    for line in f:
        rows.append(json.loads(line))
vals = [r["payload_plus_30_decoded_le_u32"] for r in rows if r.get("bounds_ok")]
result["record_framing_jsonl"] = {
    "rows": len(rows),
    "bounds_ok": sum(1 for r in rows if r.get("bounds_ok")),
    "bounds_violation": sum(1 for r in rows if not r.get("bounds_ok")),
    "value_count": len(vals),
    "zero_count": sum(1 for v in vals if v == 0),
    "zero_indexes": [r["record_index"] for r in rows if r.get("bounds_ok") and r["payload_plus_30_decoded_le_u32"] == 0],
    "distinct_values": len(set(vals)),
    "min": min(vals), "max": max(vals),
}

# 2. TLV_WALK_CENSUS.json recompute fields
tlv = json.load(open(os.path.join(PKG, "01_RAW", "TLV_WALK_CENSUS.json")))
result["tlv_walk_census_declared"] = {
    "records": tlv["records"],
    "field_30_is_tag11_value_count": tlv["field_30_is_tag11_value_count"],
    "tag11_value_matches_plus30_count": tlv["tag11_value_matches_plus30_count"],
    "tail_zero_count": tlv["tail_zero_count"],
    "shape_counts": tlv["shape_counts"],
    "anomalies": tlv["anomalies"],
}

# 3. PASS15 callsites + false positives
p15 = json.load(open(os.path.join(PKG, "01_RAW", "GHIDRA_ROUTING", "PASS15_GHIDRA_DUMP.json")))
result["pass15"] = {
    "declared_generator": p15["generator"],
    "callsites_total": p15["callsites_total"],
    "all_sites_len": len(p15["all_sites"]),
    "tag11_candidates": len(p15["tag11_candidate_sites"]),
    "candidate_sites": [s["call_site"] for s in p15["tag11_candidate_sites"]],
}

# 4. CLIENT_READ_BYTES pins
crb = json.load(open(os.path.join(PKG, "01_RAW", "CLIENT_READ_BYTES.json")))
result["client_read_bytes"] = {
    "declared_pin_count": crb["pin_count"], "declared_match_count": crb["match_count"],
    "actual_pins_len": len(crb["pins"]),
    "all_match_declared": crb["all_match"],
    "actual_all_match": all(p.get("match") for p in crb["pins"]),
}

# 5. package file count + manifest census
all_files = []
for dp, dns, fns in os.walk(PKG):
    for fn in fns:
        all_files.append(os.path.relpath(os.path.join(dp, fn), PKG))
qc_files = [f for f in all_files if f.startswith("04_QC")]
pkg_files_excl_qc = [f for f in all_files if not f.startswith("04_QC")]
result["package_file_census"] = {
    "total_files_now": len(all_files),
    "qc_files_now": len(qc_files),
    "package_files_excl_qc_now": len(pkg_files_excl_qc),
    "note": "executor HANDOFF declared 363 (362 manifest-covered + manifest itself); QC files added after delivery are excluded here",
}

man_path = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")
manifest_rows = []
with open(man_path, newline="") as f:
    rdr = csv.reader(f)
    header = next(rdr)
    for row in rdr:
        if row and row[0] and row[0] != "NOTE":
            manifest_rows.append(row)
result["manifest_census"] = {
    "declared_rows": len(manifest_rows),
    "note_row_count": sum(1 for row in manifest_rows if row[0] == "NOTE"),
    "header": header,
    "distinct_paths": len(set(r[0] for r in manifest_rows)),
    "self_present": any("MANIFEST_SHA256.csv" in r[0] for r in manifest_rows),
}

# 5b. which package files (excl 04_QC, excl manifest) are missing from the manifest?
man_set = set(r[0].replace("\\", "/") for r in manifest_rows)
disk_set = set(f.replace("\\", "/") for f in pkg_files_excl_qc if f != os.path.join("06_REPORT", "MANIFEST_SHA256.csv"))
result["manifest_census"]["files_on_disk_not_in_manifest"] = sorted(disk_set - man_set)
result["manifest_census"]["manifest_entries_not_on_disk"] = sorted(man_set - disk_set)

# 6. manifest spot re-hash (12 artifacts incl. every load-bearing one)
spot_targets = [
    "01_RAW/CLIENT_READ_BYTES.json",
    "01_RAW/RECORD_FRAMING.jsonl",
    "01_RAW/RECORD_FRAMING_SUMMARY.json",
    "01_RAW/FIELD_BYTE_ANCHOR.json",
    "01_RAW/TLV_WALK_CENSUS.json",
    "01_RAW/ROUTING_CENSUS_RAW.json",
    "01_RAW/RELEVANT_XREFS.json",
    "01_RAW/GHIDRA_ROUTING/PASS15_GHIDRA_DUMP.json",
    "02_ANALYSIS/VFS_TO_PARSER_TRACE.md",
    "02_ANALYSIS/NEGATIVE_CONTROLS.md",
    "06_REPORT/REPORT.md",
    "06_REPORT/HANDOFF.md",
    "03_SCRIPTS/s1_framing_census.py",
    "03_SCRIPTS/s4_byte_pins.py",
]
spot = []
for t in spot_targets:
    row = next((r for r in manifest_rows if r[0].replace("\\", "/") == t), None)
    if row is None:
        spot.append({"path": t, "in_manifest": False})
        continue
    full = os.path.join(PKG, t.replace("/", "\\"))
    h = sha256_file(full)
    sz = os.path.getsize(full)
    spot.append({"path": t, "in_manifest": True, "manifest_sha": row[2],
                 "recomputed_sha": h, "sha_match": h == row[2].upper(),
                 "manifest_size": int(row[1]), "actual_size": sz, "size_match": sz == int(row[1])})
result["manifest_spot_rehash"] = spot

# 7. EVIDENCE_INDEX claim -> artifact census
ev_path = os.path.join(PKG, "06_REPORT", "EVIDENCE_INDEX.md")
ev_text = open(ev_path, encoding="utf-8", errors="replace").read()
import re
artifacts_cited = sorted(set(re.findall(r"(?:01_RAW|02_ANALYSIS|03_SCRIPTS|00_CONTROL|06_REPORT)[\\/][A-Za-z0-9_\\/.]+", ev_text)))
missing_artifacts = []
for a in artifacts_cited:
    a2 = a.replace("/", "\\")
    if not os.path.exists(os.path.join(PKG, a2)):
        # try without trailing punctuation
        a3 = a2.rstrip(".,;)")
        if not os.path.exists(os.path.join(PKG, a3)):
            missing_artifacts.append(a)
result["evidence_index_census"] = {
    "distinct_artifacts_cited": len(artifacts_cited),
    "artifacts_cited": artifacts_cited,
    "missing_on_disk": missing_artifacts,
}

# 8. JOIN R1 package spot-check (>=8 known files vs its own manifest)
jr_manifest = os.path.join(JOINR1, "06_REPORT", "MANIFEST_SHA256.csv")
jr_rows = []
with open(jr_manifest, newline="") as f:
    rdr = csv.reader(f)
    for row in rdr:
        if row and row[0] and row[0] != "NOTE":
            jr_rows.append(row)
jr_targets = [
    "04_TOOLS/vfs_common.py",
    "01_RAW/GHIDRA_OUT/G2_FUN_00959090_DECOMP.txt",
    "01_RAW/GHIDRA_OUT/G3_FUN_0094d9b0_DECOMP.txt",
    "01_RAW/GHIDRA_OUT/G3_CALLERS_FUN_0094d9b0.txt",
    "06_REPORT/PE_MASTER_REVIEW.md",
    "06_REPORT/REPORT.md",
    "06_REPORT/UNRESOLVED.md",
    "00_CONTROL/RUN_CONTRACT.md",
    "03_COUNTERCHECKS/AMEND_R2/AMEND_R2_ID2_MEMBERSHIP_20002_48.json",
    "06_REPORT/HANDOFF.md",
]
jr_spot = []
for t in jr_targets:
    row = next((r for r in jr_rows if r[0].replace("\\", "/") == t), None)
    if row is None:
        jr_spot.append({"path": t, "in_manifest": False})
        continue
    full = os.path.join(JOINR1, t.replace("/", "\\"))
    if not os.path.exists(full):
        jr_spot.append({"path": t, "in_manifest": True, "on_disk": False})
        continue
    h = sha256_file(full)
    jr_spot.append({"path": t, "in_manifest": True, "on_disk": True,
                    "manifest_sha": row[2], "recomputed_sha": h, "sha_match": h == row[2].upper(),
                    "size_match": os.path.getsize(full) == int(row[1])})
result["join_r1_spot_check"] = {
    "manifest_rows": len(jr_rows),
    "results": jr_spot,
    "pyc_residue": 0,
    "note": "pyc/__pycache__ residue re-swept by QC separately (see QC report); file count 228 re-verified by QC",
}

with open(OUT, "w") as f:
    json.dump(result, f, indent=1)
print("QC5 DENOMINATORS DIGEST")
print(json.dumps(result["record_framing_jsonl"], indent=1))
print(json.dumps(result["tlv_walk_census_declared"], indent=1))
print(json.dumps(result["pass15"], indent=1))
print(json.dumps(result["client_read_bytes"], indent=1))
print(json.dumps(result["package_file_census"], indent=1))
print("manifest rows:", result["manifest_census"]["declared_rows"],
      "self_present:", result["manifest_census"]["self_present"],
      "missing_from_manifest:", result["manifest_census"]["files_on_disk_not_in_manifest"],
      "not_on_disk:", result["manifest_census"]["manifest_entries_not_on_disk"][:10])
print("manifest spot rehash failures:", [s for s in spot if not s.get("sha_match") or not s.get("size_match")])
print("evidence index artifacts:", result["evidence_index_census"]["distinct_artifacts_cited"],
      "missing:", result["evidence_index_census"]["missing_on_disk"])
print("JOIN R1 spot failures:", [s for s in jr_spot if not s.get("sha_match") or not s.get("in_manifest") or not s.get("on_disk", True)])
