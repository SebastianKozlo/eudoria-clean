#!/usr/bin/env python3
# FRESH INTERNAL QC (Q5 support) - manifest census + full row re-hash +
# physical package file census + beyond-manifest list + __pycache__ check.
import sys
sys.dont_write_bytecode = True

import csv
import hashlib
import io
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
MANIFEST = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")
REV = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM")
IQ = os.path.join(REV, "INTERNAL_QC")
OUT = os.path.join(IQ, "Q5_MANIFEST_AND_PACKAGE_CENSUS_RESULT.json")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    result = {"q": "Q5_manifest_and_package_census"}

    with open(MANIFEST, "r", encoding="utf-8-sig", newline="") as f:
        raw_lines = f.read().splitlines()
    result["manifest_raw_line_count"] = len(raw_lines)
    header = raw_lines[0]
    note_rows = [l for l in raw_lines if l.startswith("NOTE") or l.startswith('"NOTE')]
    blank_rows = [l for l in raw_lines if l.strip() == ""]
    data_rows = [l for l in raw_lines[1:]
                 if l.strip() != "" and not l.startswith("NOTE") and not l.startswith('"NOTE')]
    result["manifest_structure"] = {
        "header_line": header,
        "header_count": 1,
        "data_row_count": len(data_rows),
        "blank_row_count": len(blank_rows),
        "note_row_count": len(note_rows),
        "note_rows": note_rows,
        "self_excluded_manifest_sha_row_present": any("MANIFEST_SHA256.csv" in l for l in data_rows),
        "structure_1plus436plus1plus1": (len(raw_lines) == 439 and len(data_rows) == 436
                                         and len(blank_rows) == 1 and len(note_rows) == 1),
    }

    # parse every data row as exactly 5 CSV fields
    bad_rows = []
    rows = []
    for i, l in enumerate(data_rows):
        parsed = next(csv.reader(io.StringIO(l)))
        if len(parsed) != 5:
            bad_rows.append({"line_no": i + 2, "field_count": len(parsed), "line": l[:120]})
        rows.append(parsed)
    result["manifest_5_field_parse"] = {
        "all_rows_exactly_5_fields": len(bad_rows) == 0,
        "bad_row_count": len(bad_rows),
        "bad_rows": bad_rows[:10],
    }

    # re-hash every manifest row against disk (size + SHA256)
    mismatches = []
    missing = []
    for (rel, size_s, sha_s, algo, note) in rows:
        p = os.path.join(PKG, *rel.replace("/", "\\").split("\\"))
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        sz = os.path.getsize(p)
        sh = sha256_file(p)
        if str(sz) != size_s.strip() or sh != sha_s.strip().upper():
            mismatches.append({"rel": rel, "manifest_size": size_s, "disk_size": sz,
                              "manifest_sha": sha_s, "disk_sha": sh})
    result["manifest_row_rehash"] = {
        "row_count": len(rows),
        "match_count": len(rows) - len(mismatches) - len(missing),
        "mismatch_count": len(mismatches),
        "missing_count": len(missing),
        "mismatches": mismatches[:10],
        "missing": missing[:10],
        "all_436_match": (len(rows) == 436 and len(mismatches) == 0 and len(missing) == 0),
    }

    # physical package file census
    disk_files = []
    for root, dirs, files in os.walk(PKG):
        for name in files:
            p = os.path.join(root, name)
            disk_files.append(os.path.relpath(p, PKG))
    manifest_rels = set(r[0].replace("/", "\\") for r in rows)
    beyond = sorted(set(disk_files) - manifest_rels)
    # the manifest file itself is self-excluded by design (NOTE row);
    # "beyond the manifest" in the executor's census sense excludes it:
    beyond_minus_manifest_self = [f for f in beyond if f != os.path.join("06_REPORT", "MANIFEST_SHA256.csv")]
    result["package_census"] = {
        "disk_file_count": len(disk_files),
        "manifest_row_count": len(rows),
        "beyond_manifest_incl_manifest_self": len(beyond),
        "beyond_manifest_files": beyond,
        "beyond_minus_manifest_self_count": len(beyond_minus_manifest_self),
        "expected_beyond_at_executor_close": 17,
        # beyond at executor close = beyond_now - my INTERNAL_QC files (mine are later)
        "internal_qc_files_of_mine": sorted(f for f in beyond if f.startswith("04_QC\\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\\INTERNAL_QC")),
        "beyond_at_executor_close_recomputed": len(beyond_minus_manifest_self)
        - len([f for f in beyond if f.startswith("04_QC\\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\\INTERNAL_QC")]),
        "beyond_at_executor_close_is_17": (len(beyond_minus_manifest_self)
        - len([f for f in beyond if f.startswith("04_QC\\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\\INTERNAL_QC")])) == 17,
    }

    # __pycache__ anywhere under package
    pyc = []
    for root, dirs, files in os.walk(PKG):
        if os.path.basename(root) == "__pycache__":
            pyc.append(root)
    result["pycache_dirs"] = pyc
    result["pycache_count"] = len(pyc)

    ok = (result["manifest_structure"]["data_row_count"] == 436
          and result["manifest_structure"]["structure_1plus436plus1plus1"]
          and result["manifest_5_field_parse"]["all_rows_exactly_5_fields"]
          and result["manifest_row_rehash"]["all_436_match"]
          and len(pyc) == 0
          and result["package_census"]["beyond_at_executor_close_is_17"])
    result["overall_q5_manifest"] = ok

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 25 else v[:25] + ["..."])
                      for k, v in result.items()}, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
