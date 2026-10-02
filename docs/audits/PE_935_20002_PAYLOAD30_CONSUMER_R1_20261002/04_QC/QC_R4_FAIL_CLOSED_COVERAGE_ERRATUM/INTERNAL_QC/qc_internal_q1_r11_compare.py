#!/usr/bin/env python3
# FRESH INTERNAL QC (Q1/R11 rigor + Q7/G5 hygiene) - machine comparison of the
# semantic blocks of qc3_q1_pinverify.py vs qc4_q1_pinverify.py. v2 with the
# corrected extraction predicates (line-slice verify_pin; blank-line-normalized
# sec_for_fo; unique-key counting for extra checks - the debug run
# qc_internal_debug_extract.py established the earlier three flags were
# extraction artifacts, not source differences).
import sys
sys.dont_write_bytecode = True

import datetime
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC3 = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION", "qc_tools", "qc3_q1_pinverify.py")
QC4 = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM", "qc_tools", "qc4_q1_pinverify.py")
REV = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
OUT = os.path.join(REV, "INTERNAL_QC", "Q1_R11_MACHINE_COMPARISON_RESULT.json")

result = {"q": "Q1_R11_machine_comparison_and_G5_hygiene",
          "version": 2,
          "prior_run_note": ("the first run of qc_internal_q1_r11_compare.py flagged "
                             "verify_pin/sec_for_fo/extra-count; debug run "
                             "qc_internal_debug_extract.py proved all three were "
                             "extraction artifacts; this v2 re-measures correctly")}

with open(QC3, encoding="utf-8") as f:
    l3 = f.read().splitlines()
with open(QC4, encoding="utf-8") as f:
    l4 = f.read().splitlines()
qc3 = "\n".join(l3)
qc4 = "\n".join(l4)

w3 = re.findall(r'dump_window\("([^"]+)", (0x[0-9A-Fa-f]+), (0x[0-9A-Fa-f]+)\)', qc3)
w4 = re.findall(r'dump_window\("([^"]+)", (0x[0-9A-Fa-f]+), (0x[0-9A-Fa-f]+)\)', qc4)
result["semantic_windows"] = {"qc3_count": len(w3), "qc4_count": len(w4),
                              "identical_name_and_ranges": w3 == w4,
                              "count_is_19": len(w4) == 19}

a3 = re.findall(r'assert_sem\("([^"]+)"', qc3)
a4 = re.findall(r'assert_sem\("([^"]+)"', qc4)
result["semantic_assertions"] = {"qc3_count": len(a3), "qc4_count": len(a4),
                                 "identical_names_and_order": a3 == a4,
                                 "count_is_51": len(a4) == 51}

# verify_pin by exact line slices (established by the full source reads):
# qc3 L24-L45 (1-based), qc4 L97-L118 (1-based)
v3 = l3[23:45]
v4 = l4[96:118]
result["verify_pin_body"] = {"qc3_lines": "L24-L45", "qc4_lines": "L97-L118",
                             "identical": v3 == v4}

# sec_for_fo normalized (blank-line spacing differs: qc3 1 blank, qc4 2 blanks)
def norm(lines):
    while lines and lines[-1].strip() == "":
        lines = lines[:-1]
    return lines
s3n = norm(l3[17:23])
s4n = norm(l4[89:96])
result["sec_for_fo"] = {"qc3_lines": "L18-L22", "qc4_lines": "L90-L94",
                        "identical_normalized": s3n == s4n,
                        "only_blank_line_spacing_differs":
                            [x for x in l3[17:23] if x.strip()] == [x for x in l4[89:96] if x.strip()]}

e3 = re.findall(r'extra\["([^"]+)"\] =', qc3)
e4 = re.findall(r'extra\["([^"]+)"\] =', qc4)
result["extra_check_keys"] = {"qc3_occurrences": e3, "qc4_occurrences": e4,
                              "identical_occurrences": e3 == e4,
                              "qc3_unique_keys": sorted(set(e3)),
                              "qc4_unique_keys": sorted(set(e4)),
                              "unique_count_is_7": len(set(e4)) == 7,
                              "note": ("FUN_00412c50_head appears at try AND except "
                                       "assignment sites in BOTH files identically")}

result["bss_tail_note_present_in_both"] = ("load-time BSS-style zeros" in qc3
                                            and "load-time BSS-style zeros" in qc4)

# ---- G5 hygiene: binary/payload scan of the whole QC-R4 revision tree
scan = []
for root, dirs, files in os.walk(REV):
    for name in files:
        p = os.path.join(root, name)
        with open(p, "rb") as f:
            data = f.read()
        entry = {"rel": os.path.relpath(p, REV), "size": len(data),
                 "nul_bytes": data.count(b"\x00"), "mz": data[:2] == b"MZ"}
        entry["binary_suspect"] = (entry["nul_bytes"] > 0 or entry["mz"]
                                  or len(data) > 300000)
        scan.append(entry)
result["revision_tree_payload_scan"] = {
    "file_count": len(scan),
    "any_mz": any(x["mz"] for x in scan),
    "any_nul_bytes": any(x["nul_bytes"] > 0 for x in scan),
    "any_binary_suspect": any(x["binary_suspect"] for x in scan),
    "largest_file": max(scan, key=lambda x: x["size"])["rel"],
    "files": scan,
}

# ---- G5 hygiene: mtimes of the 5 pre-existing untracked groups
groups = ["docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001",
          "docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914",
          "docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930",
          "docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928",
          "experiments"]
mtime_info = {}
for g in groups:
    gp = os.path.join(REPO, *g.split("/"))
    newest = None
    count = 0
    for root, dirs, files in os.walk(gp):
        for name in files:
            p = os.path.join(root, name)
            count += 1
            mt = os.path.getmtime(p)
            if newest is None or mt > newest:
                newest = mt
    mtime_info[g] = {"file_count": count,
                     "newest_mtime_utc_iso": datetime.datetime.fromtimestamp(
                         newest, datetime.timezone.utc).isoformat() if newest else None}
result["untracked_groups_mtime"] = mtime_info
result["untracked_groups_untouched_assessment"] = {
    g: (info["newest_mtime_utc_iso"] is not None and
        datetime.datetime.fromisoformat(info["newest_mtime_utc_iso"])
        < datetime.datetime(2026, 10, 2, 23, 0, 0, tzinfo=datetime.timezone.utc))
    for g, info in mtime_info.items()
}

ok = (result["semantic_windows"]["identical_name_and_ranges"]
      and result["semantic_windows"]["count_is_19"]
      and result["semantic_assertions"]["identical_names_and_order"]
      and result["semantic_assertions"]["count_is_51"]
      and result["verify_pin_body"]["identical"]
      and result["sec_for_fo"]["identical_normalized"]
      and result["sec_for_fo"]["only_blank_line_spacing_differs"]
      and result["extra_check_keys"]["identical_occurrences"]
      and result["extra_check_keys"]["unique_count_is_7"]
      and result["bss_tail_note_present_in_both"]
      and not result["revision_tree_payload_scan"]["any_binary_suspect"])
result["overall_r11_and_g5_scan"] = ok

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
console = dict(result)
console["revision_tree_payload_scan"]["files"] = "(see JSON)"
console["extra_check_keys"]["qc3_occurrences"] = "(see JSON)"
console["extra_check_keys"]["qc4_occurrences"] = "(see JSON)"
print(json.dumps(console, indent=2, default=str))
sys.exit(0 if ok else 1)
