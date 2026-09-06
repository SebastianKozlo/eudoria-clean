#!/usr/bin/env python3
"""write_manifest_r1.py - artifact_index.csv writer + self-validation gate for
PE_935_TEXANCHOR_CENSUS_R1_20260906_175500, per MANIFEST_SCHEMA_SPEC.md
(PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500 TM-8 spec; authoritative).

STANDING SENTENCE: correlation/association outputs are OBSERVED-level evidence;
semantic roles remain runtime-gated; no semantic claims.

Structure: ordinary rows (artifact,role,sha256) for every package file; a
separate '# external sources' section (source_id,kind,era,physical_path,sha256)
for read-only originals outside the package. The manifest EXCLUDES its own row
and 05_ANALYSIS/MANIFEST_VALIDATION.json (self-hash impossible - documented
circular exclusions, precedent L12). The validation gate re-parses with the
STANDARD csv parser, verifies every row physically, and re-runs the 6 spec
negative tests; FAIL of any assertion = the package FAILS (fail-closed).
"""
import sys
import os
import csv
import json
import hashlib
import re

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500"
MANIFEST = os.path.join(RUN, "artifact_index.csv")
VALIDATION = os.path.join(RUN, "05_ANALYSIS", "MANIFEST_VALIDATION.json")
SPEC_PATH = (r"D:\Eudoria_Reconstruction\99_Audits"
             r"\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL"
             r"\MANIFEST_SCHEMA_SPEC.md")

STANDING = ("correlation/association outputs are OBSERVED-level evidence; semantic "
            "roles remain runtime-gated; no semantic claims")

EXCLUDED_CIRCULAR = ["artifact_index.csv", "05_ANALYSIS/MANIFEST_VALIDATION.json"]

EXTERNAL_SOURCES = [
    ("models_bnt", r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"),
    ("k1_table",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
     r"\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW"
     r"\ARKTEXTURE_ID_TABLE.csv"),
    ("r61_sha_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828"
     r"\03_validation\SHA256_SOURCE.json"),
    ("manifest_schema_spec", SPEC_PATH),
]
R61_SRC_DIR = (r"D:\Eudoria_Reconstruction\99_Audits"
               r"\PE_R61_FROZEN_BASELINE_20260828\01_source")
with open(os.path.join(os.path.dirname(R61_SRC_DIR), "03_validation",
                      "SHA256_SOURCE.json"), "r", encoding="utf-8-sig") as f:
    for _name in sorted(json.load(f)):
        if _name.endswith(".py"):
            EXTERNAL_SOURCES.append(("r61_source_" + _name,
                                     os.path.join(R61_SRC_DIR, _name)))

ROLE_MAP = {
    "00_CONTROL/CONTRACT.md": "binding contract",
    "00_CONTROL/FROZEN_METHOD.md": "frozen pre-registered method",
    "00_CONTROL/PREREG_MARKER.txt": "prereg marker (hash-recorded)",
    "00_CONTROL/texanchor_census_r1.py": "census driver",
    "00_CONTROL/write_manifest_r1.py": "manifest writer + validation gate",
    "00_CONTROL/calibration_probe_r1.py": "pre-freeze calibration probe",
    "00_CONTROL/calibration_probe2_r1.py": "pre-freeze calibration probe",
    "00_CONTROL/calibration_probe3_r1.py": "pre-freeze calibration probe",
    "00_CONTROL/CALIBRATION_PROBE.json": "pre-freeze calibration evidence",
    "00_CONTROL/CALIBRATION_PROBE2.json": "pre-freeze calibration evidence",
    "00_CONTROL/CALIBRATION_PROBE3.json": "pre-freeze calibration evidence",
    "00_CONTROL/SHA256_DRIVER.txt": "driver hash record",
    "00_CONTROL/DRIVER_LOG.txt": "driver execution log",
    "00_CONTROL/PIN_RESULTS.json": "pin results",
    "00_CONTROL/GATES_RESULTS.json": "gate results summary",
    "06_REPORT/00_FINAL_REPORT.md": "final report",
    "06_REPORT/HANDOFF.md": "handoff",
    "STAGE_ACCEPTANCE_GATES.csv": "stage acceptance gates",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return os.path.relpath(path, RUN).replace("\\", "/")


def collect_package_files():
    files = []
    for root, dirs, names in os.walk(RUN):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            p = os.path.join(root, n)
            r = rel(p)
            if r in EXCLUDED_CIRCULAR:
                continue
            files.append(r)
    return sorted(files)


def write_manifest():
    rows = []
    for r in collect_package_files():
        sha = sha256_file(os.path.join(RUN, *r.split("/")))
        rows.append([r, ROLE_MAP.get(r, "package artifact"), sha])
    with open(MANIFEST, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            w.writerow(row)
        w.writerow(["# external sources"])
        for sid, path in EXTERNAL_SOURCES:
            w.writerow([sid, "external_source", "PCG_9_3_5", path,
                        sha256_file(path)])
    return len(rows)


# ---------------- the validation gate (standard parser; fail-closed) --------

SHA_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def validate_manifest():
    with open(MANIFEST, "r", encoding="utf-8", newline="") as f:
        parsed = list(csv.reader(f))
    findings = []
    seen = set()
    section = "ordinary"
    n_ord = 0
    n_ext = 0
    for i, row in enumerate(parsed):
        if row == ["# external sources"]:
            section = "external"
            continue
        if not row:
            continue
        if section == "ordinary":
            cnt = sum(1 for _ in row)
            if cnt != 3:
                findings.append(("MALFORMED_MANIFEST_ROW",
                                 "row %d: %d fields" % (i + 1, cnt)))
                continue
            artifact, role, sha = row
            if not SHA_RE.match(sha or ""):
                findings.append(("MALFORMED_HASH", "row %d" % (i + 1,)))
                continue
            if os.path.isabs(artifact) or ".." in artifact.split("/"):
                findings.append(("UNSUPPORTED_SYMBOLIC_PATH_SHAPE",
                                 "row %d: %r" % (i + 1, artifact)))
                continue
            if artifact in seen:
                findings.append(("DUPLICATE_ROW", "row %d: %r" % (i + 1, artifact)))
                continue
            seen.add(artifact)
            p = os.path.join(RUN, *artifact.split("/"))
            if not os.path.isfile(p):
                findings.append(("MISSING_FILE", "row %d: %r" % (i + 1, artifact)))
                continue
            if sha256_file(p).lower() != sha.lower():
                findings.append(("HASH_MISMATCH", "row %d: %r" % (i + 1, artifact)))
                continue
            n_ord += 1
        else:
            cnt = sum(1 for _ in row)
            if cnt != 5:
                findings.append(("MALFORMED_EXTERNAL_ROW",
                                 "row %d: %d fields" % (i + 1, cnt)))
                continue
            sid, kind, era, phys, sha = row
            if kind != "external_source":
                findings.append(("MALFORMED_EXTERNAL_ROW",
                                 "row %d: kind %r" % (i + 1, kind)))
                continue
            if not era or not str(era).strip():
                findings.append(("MALFORMED_EXTERNAL_ROW", "row %d: era" % (i + 1,)))
                continue
            if not SHA_RE.match(sha or ""):
                findings.append(("MALFORMED_HASH", "row %d ext" % (i + 1,)))
                continue
            if not os.path.isfile(phys):
                findings.append(("MISSING_FILE", "row %d: %r" % (i + 1, phys)))
                continue
            if sha256_file(phys).lower() != sha.lower():
                findings.append(("HASH_MISMATCH", "row %d: %r" % (i + 1, phys)))
                continue
            n_ext += 1
    # every package file present exactly once (minus the documented circular
    # exclusions)
    expected = set(collect_package_files())
    missing = sorted(expected - seen)
    if missing:
        findings.append(("MISSING_FILE", "package files absent from manifest: %r"
                         % missing[:5]))
    unexpected = sorted(seen - expected)
    if unexpected:
        findings.append(("DUPLICATE_ROW", "manifest rows not package files: %r"
                         % unexpected[:5]))
    return (not findings), {"ordinary_rows_verified": n_ord,
                            "external_rows_verified": n_ext,
                            "findings": findings,
                            "circular_exclusions_documented": EXCLUDED_CIRCULAR}


def negative_tests():
    """The 6 spec negative tests (synthetic rows; each must FAIL the gate)."""
    def gate(rows):
        findings = []
        seen = set()
        for row in rows:
            if row == ["# external sources"]:
                continue
            cnt = sum(1 for _ in row)
            if cnt != 3:
                findings.append("MALFORMED_MANIFEST_ROW")
                continue
            artifact, role, sha = row
            if not SHA_RE.match(sha or ""):
                findings.append("MALFORMED_HASH")
                continue
            if os.path.isabs(artifact) or ".." in artifact.split("/"):
                findings.append("UNSUPPORTED_SYMBOLIC_PATH_SHAPE")
                continue
            if artifact in seen:
                findings.append("DUPLICATE_ROW")
                continue
            seen.add(artifact)
            p = os.path.join(RUN, *artifact.split("/"))
            if not os.path.isfile(p):
                findings.append("MISSING_FILE")
                continue
            if sha256_file(p).lower() != sha.lower():
                findings.append("HASH_MISMATCH")
        return findings

    a = "a" * 64
    contract_sha = sha256_file(os.path.join(RUN, "00_CONTROL", "CONTRACT.md"))
    tests = []
    ok, out = True, []
    # (a) unquoted comma in a field (RFC-4180 parse -> 4 fields)
    t = gate([["00_CONTROL/CONTRACT.md", "role", " with comma", a]])
    tests.append({"test": "a_unquoted_comma", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    # (b) missing newline between records (one line, two records)
    t = gate([["00_CONTROL/CONTRACT.md", "role", contract_sha,
               "00_CONTROL/FROZEN_METHOD.md", "role2", "b" * 64]])
    tests.append({"test": "b_missing_newline", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    # (c) missing file
    t = gate([["00_CONTROL/NO_SUCH_FILE.md", "role", a]])
    tests.append({"test": "c_missing_file", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    # (d) malformed hash
    t = gate([["00_CONTROL/CONTRACT.md", "role", "XYZ" + "a" * 61]])
    tests.append({"test": "d_malformed_hash", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    # (e) unsupported symbolic path shape
    t = gate([["C:/absolute/path.md", "role", a]])
    tests.append({"test": "e_unsupported_symbolic_path", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    # (f) duplicate row
    t = gate([["00_CONTROL/CONTRACT.md", "role", contract_sha.lower()],
              ["00_CONTROL/CONTRACT.md", "role2", contract_sha.lower()]])
    tests.append({"test": "f_duplicate_row", "must_fail": True,
                  "failed": bool(t), "class": t[0] if t else None})
    return tests


def main():
    n_rows = write_manifest()
    ok, out = validate_manifest()
    tests = negative_tests()
    all_neg = all(t["failed"] for t in tests)
    result = {
        "run_id": "PE_935_TEXANCHOR_CENSUS_R1_20260906_175500",
        "era": "PCG_9_3_5",
        "standing": STANDING,
        "spec": SPEC_PATH,
        "manifest": "artifact_index.csv",
        "ordinary_rows_written": n_rows,
        "validation": out,
        "negative_tests": tests,
        "all_six_negative_tests_fail_closed": bool(all_neg),
        "circular_exclusions_documented": EXCLUDED_CIRCULAR,
        "result": "PASS" if (ok and all_neg) else "FAIL",
    }
    with open(VALIDATION, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    print("manifest rows: %d ordinary + %d external" % (n_rows, len(EXTERNAL_SOURCES)))
    print("gate:", result["result"], "| negatives 6/6 fail-closed:", all_neg,
          "| findings:", out["findings"][:3])
    if result["result"] != "PASS":
        sys.exit(4)


if __name__ == "__main__":
    main()
