#!/usr/bin/env python3
# -*- coding: ascii -*-
# payload_scan_final_v4_1.py - W3 (the FINAL): the payload scan over 100% of the
# FINAL commit set. The commit set = the 5 modified gate-package repo files +
# the ENTIRE repo mirror tree (which contains byte-identical copies of the run's
# 00_Control + 01_RAW + REPORT.md + HANDOFF.md + the two CSVs) + the run-local
# originals (scanned directly - the mirror copies verified identical by hash).
# Scan method (stronger than the R2's head-512): every file is FULLY read -
# hit on ANY NUL byte, a proprietary binary magic (BNT2 / BNT\x02 / AK), a
# zero-prefixed stream, or a failed UTF-8 text decode (every committed file must
# be text - identity metadata only, zero proprietary payloads).
# SELF-REFERENCE EXCLUSION (documented, the established convention - cf. the
# R2's artifact_index.csv "a file cannot hash itself"): the scan report's OWN
# final bytes are the only unscanned bytes in the commit set; its content class
# = pure-ASCII JSON serialized by this script (the serializer guarantees
# ASCII-only output). The report's mirror copy is created by this script
# immediately after this serialization (shutil.copyfile - byte-identical).
# The artifact_index.csv row for this report (SHA computable only post-write)
# is appended by this script - the documented post-index convention.
import hashlib
import json
import os
import shutil
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RUN_ID = "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528"
MIRROR = os.path.join(REPO, "docs", "audits", RUN_ID)
REPO_GATE = os.path.join(REPO, "docs", "audits", "PE_MILESTONE_1_WORLD_SURFACE_R1_GATE")
REPORT_PATH = os.path.join(RAW, "payload_scan_final_v4_1.json")

REPO_GATE_FILES = [
    os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json"),
    os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md"),
    os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json"),
    os.path.join(REPO_GATE, "GATE_INDEX.md"),
    os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def scan_file(path):
    """return (ok, reason): ok = text, no binary magics, no NUL, decodable UTF-8."""
    data = open(path, "rb").read()
    if data[:4] in (b"BNT2", b"BNT\x02"):
        return False, "proprietary BNT magic"
    if data[:2] == b"AK":
        return False, "ArkVFS AK magic"
    if data[:3] == b"\x00\x00\x0a":
        return False, "zero-prefixed stream"
    if b"\x00" in data:
        return False, "NUL byte at offset %d" % data.find(b"\x00")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as e:
        return False, "not UTF-8 text (%s)" % e
    return True, "text (%d bytes, utf-8-decodable, no binary magics)" % len(data)


def main():
    scanned = []
    bad = []
    seen = set()

    def add(path, group):
        if path in seen:
            return
        seen.add(path)
        ok, reason = scan_file(path)
        scanned.append({"group": group, "path": path, "bytes": os.path.getsize(path),
                        "sha256": sha256_file(path), "verdict": "CLEAN" if ok else "HIT",
                        "detail": reason})
        if not ok:
            bad.append(scanned[-1])

    # (1) the 5 modified gate-package repo files
    for p in REPO_GATE_FILES:
        add(p, "repo_gate_package")
    # (2) the ENTIRE mirror tree (every file)
    for dirpath, dirnames, filenames in os.walk(MIRROR):
        for fn in sorted(filenames):
            add(os.path.join(dirpath, fn), "mirror")
    # (3) the run-local originals (00_CONTROL + 01_RAW + 05_ANALYSIS + 06_REPORT)
    for sub in ("00_CONTROL", "01_RAW", "05_ANALYSIS", "06_REPORT"):
        d = os.path.join(RUN_ROOT, sub)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames if x != "__pycache__"]
            for fn in sorted(filenames):
                if fn.endswith(".pyc"):
                    continue
                add(os.path.join(dirpath, fn), "run_local")
    # mirror-copy fidelity: the run-local 00_Control/01_RAW originals == the mirror copies (hash-verified)
    copy_mismatch = []
    for sub in ("00_Control", "01_RAW"):
        for fn in sorted(os.listdir(os.path.join(RUN_ROOT, sub))):
            a = os.path.join(RUN_ROOT, sub, fn)
            b = os.path.join(MIRROR, sub, fn)
            if os.path.isfile(a):
                if not os.path.isfile(b) or sha256_file(a) != sha256_file(b):
                    copy_mismatch.append(fn)
    if copy_mismatch:
        raise SystemExit("HARD STOP: mirror copies != the run-local originals: %r" % copy_mismatch)

    report = {
        "run_id": RUN_ID,
        "work_item": "W3 final - the payload scan over 100% of the FINAL commit set",
        "method": ("every file FULLY read: hit on any NUL byte / proprietary binary magic (BNT2, BNT\\x02, AK) / "
                   "zero-prefixed stream / failed UTF-8 decode. Identity metadata only - zero proprietary payloads."),
        "commit_set_coverage": ("the 5 modified gate-package repo files + the ENTIRE mirror tree + the run-local "
                                "originals (the mirror copies hash-verified identical to the originals) = %d unique files scanned"
                                % len(scanned)),
        "self_reference_exclusion": ("this report's own final bytes (run-local + the mirror copy) are the only "
                                     "unscanned bytes in the commit set - the established a-file-cannot-scan-itself "
                                     "convention (cf. the R2's artifact_index.csv); its content class = pure-ASCII "
                                     "JSON serialized by this script; the artifact_index row for it is appended "
                                     "post-write by this script (the documented post-index convention)"),
        "files": scanned,
        "counts": {"scanned": len(scanned), "clean": len(scanned) - len(bad), "hits": len(bad)},
        "verdict": "PASS" if not bad else "FAIL",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(REPORT_PATH, "w", encoding="ascii", newline="") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    # the mirror copy (byte-identical; created by this script immediately after the serialization)
    shutil.copyfile(REPORT_PATH, os.path.join(MIRROR, "01_RAW", "payload_scan_final_v4_1.json"))
    # the artifact_index row (the SHA computable only post-write; replaces the PENDING row)
    index_path = os.path.join(MIRROR, "artifact_index.csv")
    lines = open(index_path, "r", encoding="ascii", newline="").read().split("\r\n")
    out = []
    for ln in lines:
        if "payload_scan_final_v4_1.json (post-index artifact)" in ln:
            out.append("%s,%d,%s" % ("mirror/01_RAW/payload_scan_final_v4_1.json",
                                     os.path.getsize(REPORT_PATH), sha256_file(REPORT_PATH)))
        else:
            out.append(ln)
    open(index_path, "w", encoding="ascii", newline="").write("\r\n".join(out))

    print("FINAL PAYLOAD SCAN: %s (%d files scanned; %d clean; %d hits)"
          % (report["verdict"], len(scanned), len(scanned) - len(bad), len(bad)))
    for b in bad:
        print("  HIT:", b["path"], "-", b["detail"])
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
