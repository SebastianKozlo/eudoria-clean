#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC-R2 TOOL 1 (fresh QC worker, round 2; NO code shared with the executor's
03_SCRIPTS or with round-1's qc_tools):

DIFF CENSUS + BEFORE/AFTER PROVENANCE for the AMEND-R1 verification of
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002.

Duties covered (from the QC-R2 dispatch):
  2. DIFF CENSUS: hash EVERY file in the package (outside 04_QC) and compare
     against 06_REPORT\MANIFEST_SHA256.csv (363 file rows + NOTE row).
     EXPECTED: exactly 7 mismatches (C1..C7 AFTER hashes), 356 matches,
     0 missing; PLUS the new file 06_REPORT\AMEND_LOG_R1.md (not in the
     delivery manifest) and the manifest itself (self-excluded).
  3. BEFORE-STATE PROVENANCE: for each C1..C7 the BEFORE size+SHA256 recorded
     in AMEND_LOG_R1.md must equal the delivery-manifest row.
  6. UNCHANGED-FILE SPOT CONFIRMATION: >=10 load-bearing unchanged files
     re-hashed (subsumed: the census re-hashes ALL files; the 10 named files
     are reported explicitly).
Also verifies the dispatch's AFTER size/SHA for C1..C7 and C8, and the
package file-count algebra (365 outside 04_QC = 363 manifest-covered + 1
manifest + 1 new AMEND_LOG; 14 inside 04_QC untouched by AMEND-R1).
"""
import csv
import hashlib
import json
import os
import sys

ROOT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
MANIFEST_REL = "06_REPORT/MANIFEST_SHA256.csv"
AMEND_LOG_REL = "06_REPORT/AMEND_LOG_R1.md"

# Dispatch-declared AFTER identities (C1..C7) and BEFORE identities as
# recorded in AMEND_LOG_R1.md (transcribed here as expected constants so the
# comparison is machine-checkable against BOTH the manifest and disk):
CHANGED = {
    "02_ANALYSIS/BLAST_RADIUS.md": {
        "before": (4678, "3190ECA35FB125728650FB80F7D0AD8188827DD9A92B6FE03502BE875DCE7E72"),
        "after": (6061, "3971527CF395E802FCC4407E65505374A55B8B16085421CD7C20F21E685A53A9"),
        "qc": "P2-1 (C1)"},
    "06_REPORT/EVIDENCE_INDEX.md": {
        "before": (6429, "E7183B9EDE04F788094782BC856CA468E2522D20CC10675F38A858342340AB58"),
        "after": (6579, "E59CBDD2867332BB038F1C39A428CB5FA32A9DA016EF5F3F289CBA8C750E545B"),
        "qc": "P2-1 (C2)"},
    "01_RAW/GHIDRA_ROUTING/PASS15_GHIDRA_DUMP.json": {
        "before": (92827, "1764D73716ADB73E1990DD37667051E7D82B139F7D195B7FD76610771546EB9D"),
        "after": (92828, "B90667D3CAF2DB25E51847C38962451D125C0CC39D70482590CFE9A911C1CFCD"),
        "qc": "P3-1 (C3)"},
    "01_RAW/RELEVANT_XREFS.json": {
        "before": (6127, "849DCEE7BFADA5D308FD948B363B294DE31AF5D89566B969BCF311B93405F387"),
        "after": (6184, "A0028A1933B30EA654DDDBF942138BB01B8FA468B7F2AB71A199FD196767DBF0"),
        "qc": "P3-2 (C4)"},
    "01_RAW/RECORD_FRAMING_SUMMARY.json": {
        "before": (136502, "32044BC133A846BA607D00D58E4BF4E4A6FF861338E61EDBA581ADCE0524E976"),
        "after": (136567, "8088120BA352D3BE632C0A042E51B28BC989A203CFC7FB2D7460708E2EFF52C3"),
        "qc": "P3-3 (C5)"},
    "06_REPORT/HANDOFF.md": {
        "before": (8797, "3FEFEBDB4B8936265AB3EA9127385A4FFE0ABA7823ACDF4B9681D6AC3D0306E8"),
        "after": (8939, "1865DA3295A91CC55DA67AC2E342F8ACC482731B458498E94808B558D573164B"),
        "qc": "P3-4 (C6)"},
    "06_REPORT/REPORT.md": {
        "before": (9944, "460AC8ABBE84C113F3C6AC159BAD3EDA4F0DDA0A00ECBE381EF24B2B183AA279"),
        "after": (10159, "B29BDB8E3E4CC140CD71C856B5B409A9D81252608EC7BD200EE708849CE2DF62"),
        "qc": "post-QC governance fill (C7)"},
}
NEW_FILE = {"path": AMEND_LOG_REL,
            "expected": (16978, "02A60AE9A562F1C2380023262EBAE9A3B66ACBA7AC0DA7A40934504CBF436943")}

SPOT_LOAD_BEARING = [
    "00_CONTROL/RUN_CONTRACT.md",
    "00_CONTROL/PREFLIGHT.md",
    "01_RAW/CLIENT_READ_BYTES.json",
    "01_RAW/RECORD_FRAMING.jsonl",
    "01_RAW/TLV_WALK_CENSUS.json",
    "01_RAW/FIELD_BYTE_ANCHOR.json",
    "01_RAW/ROUTING_CENSUS_RAW.json",
    "01_RAW/CROSSVALIDATION_vfs_common.json",
    "02_ANALYSIS/NEGATIVE_CONTROLS.md",
    "02_ANALYSIS/SEMANTIC_ASSESSMENT.md",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    result = {"tool": "q2r1_diff_census.py", "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
              "qc_round": 2, "scope": "AMEND-R1 verification"}

    manifest_path = os.path.join(ROOT, MANIFEST_REL.replace("/", os.sep))
    with open(manifest_path, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))

    header = rows[0]
    result["manifest_header"] = header
    problems = []
    if header != ["file", "size_bytes", "sha256", "origin", "note"]:
        problems.append("manifest header unexpected: %r" % header)

    file_rows = {}
    note_rows = 0
    malformed = []
    for r in rows[1:]:
        if not r:
            continue
        if r[0] == "NOTE":
            note_rows += 1
            continue
        if len(r) != 5:
            malformed.append(r[:2])
            continue
        path, size_s, sha, origin, note = [x.strip() for x in r]
        file_rows[path] = {"size": int(size_s), "sha256": sha.upper(), "origin": origin, "note": note}

    result["manifest_file_rows"] = len(file_rows)
    result["manifest_note_rows"] = note_rows
    result["manifest_malformed_rows"] = malformed
    if len(file_rows) != 363:
        problems.append("manifest file-row count != 363: %d" % len(file_rows))
    if note_rows != 1:
        problems.append("manifest NOTE-row count != 1: %d" % note_rows)

    # --- disk walk (exclude 04_QC entirely) ---
    disk = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        parts = [] if rel_dir == "." else rel_dir.split(os.sep)
        if parts and parts[0] == "04_QC":
            dirnames[:] = []
            continue
        for name in filenames:
            rel = os.path.join(rel_dir, name) if rel_dir != "." else name
            rel = rel.replace(os.sep, "/")
            full = os.path.join(dirpath, name)
            disk[rel] = {"size": os.path.getsize(full), "sha256": sha256_file(full)}

    # 04_QC census (read-only count; AMEND-R1 claims 14 files, untouched by it)
    qc_count = 0
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "04_QC")):
        qc_count += len(filenames)
    result["files_outside_04_qc"] = len(disk)
    result["files_inside_04_qc"] = qc_count

    # --- compare manifest -> disk ---
    matches, mismatches, missing = [], [], {}
    for path, meta in file_rows.items():
        if path not in disk:
            missing.append(path)
            continue
        d = disk[path]
        if d["size"] == meta["size"] and d["sha256"] == meta["sha256"]:
            matches.append(path)
        else:
            mismatches.append(path)

    result["manifest_vs_disk"] = {
        "matches": len(matches), "mismatches": sorted(mismatches), "missing": sorted(missing)}

    # extras: disk files not covered by manifest
    extras = sorted(set(disk) - set(file_rows))
    result["disk_files_not_in_manifest"] = extras

    # --- diff-census expectation (dispatch duty 2) ---
    exp_mismatch = set(CHANGED)
    got_mismatch = set(mismatches)
    census_ok = (got_mismatch == exp_mismatch)
    result["diff_census_expectation"] = {
        "expected_mismatches": sorted(exp_mismatch),
        "got_mismatches": sorted(got_mismatch),
        "expected_matches": 356, "got_matches": len(matches),
        "expected_missing": 0, "got_missing": len(missing),
        "expected_new_files_not_in_manifest": [MANIFEST_REL, AMEND_LOG_REL],
        "got_new_files_not_in_manifest": extras,
        "PASS": census_ok and len(matches) == 356 and len(missing) == 0
                and set(extras) == {MANIFEST_REL, AMEND_LOG_REL}}

    # --- BEFORE/AFTER provenance per changed file ---
    prov = {}
    for path, spec in CHANGED.items():
        mrow = file_rows.get(path)
        d = disk.get(path)
        prov[path] = {
            "qc_finding": spec["qc"],
            "before_in_amend_log": {"size": spec["before"][0], "sha256": spec["before"][1]},
            "before_in_manifest": {"size": mrow["size"], "sha256": mrow["sha256"]} if mrow else None,
            "before_provenance_ok": bool(mrow) and (mrow["size"], mrow["sha256"]) == spec["before"],
            "after_dispatch": {"size": spec["after"][0], "sha256": spec["after"][1]},
            "after_disk": {"size": d["size"], "sha256": d["sha256"]} if d else None,
            "after_ok": bool(d) and (d["size"], d["sha256"]) == spec["after"],
        }
    result["before_after_provenance"] = prov

    # --- new file C8 identity ---
    d = disk.get(AMEND_LOG_REL)
    result["new_file_C8"] = {
        "path": AMEND_LOG_REL,
        "expected": {"size": NEW_FILE["expected"][0], "sha256": NEW_FILE["expected"][1]},
        "disk": {"size": d["size"], "sha256": d["sha256"]} if d else None,
        "ok": bool(d) and (d["size"], d["sha256"]) == NEW_FILE["expected"]}

    # --- spot confirmation of load-bearing unchanged files ---
    spot = {}
    for path in SPOT_LOAD_BEARING:
        mrow = file_rows.get(path)
        d = disk.get(path)
        ok = bool(mrow) and bool(d) and mrow["size"] == d["size"] and mrow["sha256"] == d["sha256"]
        spot[path] = {"manifest": (mrow["size"], mrow["sha256"]) if mrow else None,
                      "disk": (d["size"], d["sha256"]) if d else None, "match": ok}
    result["spot_load_bearing"] = spot

    # --- file-count algebra (AMEND_LOG SC6) ---
    expected_outside = 364 + 1  # 364 delivery + new log
    result["file_count_algebra"] = {
        "expected_outside_04_qc": expected_outside, "measured_outside_04_qc": len(disk),
        "expected_inside_04_qc_amend_claim": 14, "measured_inside_04_qc": qc_count,
        "ok": len(disk) == expected_outside}

    result["problems"] = problems
    result["OVERALL_PASS"] = (census_ok and len(matches) == 356 and len(missing) == 0
                              and set(extras) == {MANIFEST_REL, AMEND_LOG_REL}
                              and all(v["before_provenance_ok"] and v["after_ok"] for v in prov.values())
                              and result["new_file_C8"]["ok"]
                              and all(v["match"] for v in spot.values())
                              and result["file_count_algebra"]["ok"]
                              and not problems)

    out = os.path.join(ROOT, "04_QC", "QC_R2_DIFF_CENSUS_RESULT.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != "before_after_provenance"
                      and k != "spot_load_bearing"}, indent=1)[:4000])
    print("OVERALL_PASS =", result["OVERALL_PASS"])


if __name__ == "__main__":
    main()
