#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PERSIST gates P1-P4 (pe-master-auditor, RUN_ID: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST).
Fail-closed, asserted. Reads the run package + pre-work snapshot; writes only:
  00_CONTROL\qc_probe\persist_gates_result.json

P1  phrase census: executor-documentation layer *.md/*.csv = 0 hits "11705"/"11706";
    "11769" present; the .text recalibration evidence lives in persist_p1_recalibration_result.json
    (imm32 f9 2d 00 00 = exactly 1 hit @0x00511245/46). Data/audit layers reported explicitly.
P2  artifact_index.csv: disk census == manifest (scope defined below); no self-row;
    HANDOFF.md row present; all rows re-hashed.
P3  ghidra_output dump census == numbers written into FINAL_REPORT/HANDOFF (212/224/31/1=468).
P4  full-package untouchability vs persist_pre_work_state.json:
    exactly the 7 intended files changed (F1 x3, F4 x2, manifest, QC_REPORT append);
    everything else byte-identical; qc_probe == QC_PROBE_SHA256.txt; GHIDRA_LOCAL == its manifest.
"""
import hashlib
import json
import os
import sys

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
PRE = os.path.join(RUN, "00_CONTROL", "qc_probe", "persist_pre_work_state.json")
OUT = os.path.join(RUN, "00_CONTROL", "qc_probe", "persist_gates_result.json")

INTENDED_CHANGED = {
    "02_ANALYSIS\\B_template_loading_chain.md": "F1",
    "03_EVIDENCE\\VA_EVIDENCE_REGISTRY.md": "F1",
    "06_REPORT\\STAGE_ACCEPTANCE_GATES.csv": "F1",
    "06_REPORT\\00_FINAL_REPORT.md": "F4",
    "06_REPORT\\HANDOFF.md": "F4",
    "06_REPORT\\artifact_index.csv": "F2/F3 rebuild",
    "06_REPORT\\QC_REPORT.md": "POST-QC append (authorized)",
}
KEY_EVIDENCE_11 = [
    "01_RAW\\S1_ANCHOR_RESULT.json", "01_RAW\\S2_TRUE_WALK_RESULT.json", "01_RAW\\S3_PE_HEADER.json",
    "01_RAW\\S2_TEMPLATES_TRUE_WALK.csv", "01_RAW\\S4B_RAW_HITS.json",
    "02_ANALYSIS\\A_record_definition.md", "02_ANALYSIS\\B_template_loading_chain.md",
    "02_ANALYSIS\\C_transform_source_and_D_placement.md",
    "03_EVIDENCE\\VA_EVIDENCE_REGISTRY.md",
    "06_REPORT\\00_FINAL_REPORT.md", "06_REPORT\\STAGE_ACCEPTANCE_GATES.csv",
]
DOC_LAYER = [
    "02_ANALYSIS\\A_record_definition.md", "02_ANALYSIS\\B_template_loading_chain.md",
    "02_ANALYSIS\\C_transform_source_and_D_placement.md", "03_EVIDENCE\\VA_EVIDENCE_REGISTRY.md",
    "06_REPORT\\00_FINAL_REPORT.md", "06_REPORT\\STAGE_ACCEPTANCE_GATES.csv",
    "06_REPORT\\HANDOFF.md", "06_REPORT\\GHIDRA_LOCAL_COPY_MANIFEST.txt",
]

res = {"probe": "persist_gates_P1_P4", "errors": [], "gates": {}}


def sha_of(rel):
    with open(os.path.join(RUN, *rel.split("\\")), "rb") as f:
        data = f.read()
    return len(data), hashlib.sha256(data).hexdigest().upper()


# ---------------- P1: phrase census ----------------
p1 = {"executor_doc_layer": {}, "data_layer_01_RAW": {}, "audit_layer": {}, "other_txt_00_CONTROL": {},
      "ghidra_output_csv": {}}


def count_phrases(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            t = f.read()
    except OSError as e:
        return {"error": str(e)}
    return {"11705": t.count("11705"), "11706": t.count("11706"), "11769": t.count("11769")}


for rel in DOC_LAYER:
    p1["executor_doc_layer"][rel] = count_phrases(os.path.join(RUN, *rel.split("\\")))
for rel in ["01_RAW\\S1_TEMPLATES_BLOCK_CENSUS.csv", "01_RAW\\S2_TEMPLATES_TRUE_WALK.csv"]:
    p1["data_layer_01_RAW"][rel] = count_phrases(os.path.join(RUN, *rel.split("\\")))
for rel in ["06_REPORT\\QC_REPORT.md", "06_REPORT\\PE_MASTER_REVIEW.md"]:
    p1["audit_layer"][rel] = count_phrases(os.path.join(RUN, *rel.split("\\")))
gh = os.path.join(RUN, "01_RAW", "ghidra_output")
gh_csv = [fn for fn in os.listdir(gh) if fn.lower().endswith(".csv")]
for fn in gh_csv:
    p1["ghidra_output_csv"]["01_RAW\\ghidra_output\\" + fn] = count_phrases(os.path.join(gh, fn))
ctrl = os.path.join(RUN, "00_CONTROL")
for fn in os.listdir(ctrl):
    p = os.path.join(ctrl, fn)
    if os.path.isfile(p) and fn.lower().endswith(".txt"):
        p1["other_txt_00_CONTROL"]["00_CONTROL\\" + fn] = count_phrases(p)

doc_hits = sum(v.get("11705", 0) + v.get("11706", 0) for v in p1["executor_doc_layer"].values())
doc_11769 = sum(v.get("11769", 0) for v in p1["executor_doc_layer"].values())
p1["predicate"] = {
    "executor_doc_11705_11706_hits": doc_hits,
    "executor_doc_11769_hits": doc_11769,
    "pass": doc_hits == 0 and doc_11769 >= 3,
}
res["gates"]["P1"] = p1
print("[P1] doc-layer 11705/11706 hits=%d, 11769 hits=%d -> %s"
      % (doc_hits, doc_11769, "PASS" if p1["predicate"]["pass"] else "FAIL"))
if not p1["predicate"]["pass"]:
    res["errors"].append("P1 failed: %r" % p1["predicate"])

# ---------------- P2: manifest census ----------------
with open(os.path.join(RUN, "06_REPORT", "artifact_index.csv"), "rb") as f:
    raw = f.read()
assert raw.startswith(b"\xef\xbb\xbf"), "manifest BOM lost"
rows = [ln for ln in raw.decode("utf-8-sig").split("\r\n") if ln != ""]
header, mrows = rows[0], rows[1:]
mpaths = [ln.split(",", 1)[0] for ln in mrows]

disk = []
for dirpath, dirnames, filenames in os.walk(RUN):
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), RUN).replace(os.sep, "\\")
        disk.append(rel)
EXCLUDE = lambda rel: (
    rel.startswith("00_CONTROL\\GHIDRA_LOCAL\\")
    or rel.startswith("00_CONTROL\\qc_probe\\")
    or rel in ("06_REPORT\\QC_REPORT.md", "06_REPORT\\PE_MASTER_REVIEW.md",
               "06_REPORT\\GHIDRA_LOCAL_COPY_MANIFEST.txt", "06_REPORT\\artifact_index.csv")
)
census = sorted(r for r in disk if not EXCLUDE(r))
p2 = {
    "manifest_rows": len(mrows),
    "disk_census_scope": census,
    "disk_census_count": len(census),
    "census_minus_manifest": sorted(set(census) - set(mpaths)),
    "manifest_minus_census": sorted(set(mpaths) - set(census)),
    "self_row_present": any(r.startswith("06_REPORT\\artifact_index.csv,") for r in mrows),
    "handoff_row_present": "06_REPORT\\HANDOFF.md" in mpaths,
}
# full re-hash of every manifest row (truthfulness + untouchability)
rehash_bad = []
for ln in mrows:
    parts = ln.split(",")
    rel, size_s, sha_s = parts[0], parts[1], parts[2]
    try:
        size, sha = sha_of(rel)
        if str(size) != size_s or sha != sha_s:
            rehash_bad.append({"path": rel, "claim": [size_s, sha_s], "actual": [size, sha]})
    except OSError as e:
        rehash_bad.append({"path": rel, "error": str(e)})
p2["manifest_rehash_mismatches"] = rehash_bad
p2["predicate"] = {
    "census_eq_manifest": p2["disk_census_count"] == len(mrows)
                          and not p2["census_minus_manifest"] and not p2["manifest_minus_census"],
    "no_self_row": not p2["self_row_present"],
    "handoff_in_manifest": p2["handoff_row_present"],
    "all_rows_hash_ok": not rehash_bad,
}
p2["predicate"]["pass"] = all(p2["predicate"][k] for k in
                              ("census_eq_manifest", "no_self_row", "handoff_in_manifest", "all_rows_hash_ok"))
res["gates"]["P2"] = {k: v for k, v in p2.items() if k != "disk_census_scope"}
print("[P2] manifest rows=%d census=%d selfRow=%s handoff=%s rehashBad=%d -> %s"
      % (len(mrows), len(census), p2["self_row_present"], p2["handoff_row_present"], len(rehash_bad),
         "PASS" if p2["predicate"]["pass"] else "FAIL"))
if not p2["predicate"]["pass"]:
    res["errors"].append("P2 failed: %r" % {k: p2["predicate"][k] for k in p2["predicate"] if k != "pass"})

# ---------------- P3: dump census ----------------
dis = pseudo = js = csvs = other = 0
for fn in os.listdir(gh):
    b = os.path.basename(fn)
    low = b.lower()
    if "_disasm_" in low:
        dis += 1
    elif "_pseudo_" in low or low.endswith("_pseudo.txt"):
        pseudo += 1
    elif low.endswith(".json"):
        js += 1
    elif low.endswith(".csv"):
        csvs += 1
    else:
        other += 1
total_gh = len(os.listdir(gh))
fr = open(os.path.join(RUN, "06_REPORT", "00_FINAL_REPORT.md"), "r", encoding="utf-8").read()
ho = open(os.path.join(RUN, "06_REPORT", "HANDOFF.md"), "r", encoding="utf-8").read()
p3 = {
    "ghidra_output_files": total_gh, "disasm": dis, "pseudo": pseudo, "json": js, "csv": csvs, "other": other,
    "final_report_has_212_224_31_1_468": all(s in fr for s in ["212× DISASM", "224× PSEUDO", "31× JSON", "1× CSV", "468 plików"]),
    "handoff_has_212_224_31_1_468": all(s in ho for s in ["212× DISASM", "224× PSEUDO", "31× JSON", "1× CSV", "468 plików"]),
    "final_report_old_61_48_absent": ("61× DISASM" not in fr) and ("48× PSEUDO" not in fr),
    "handoff_old_61_48_absent": ("61× DISASM" not in ho) and ("48× PSEUDO" not in ho),
}
p3["predicate"] = {
    "pass": total_gh == 468 and dis == 212 and pseudo == 224 and js == 31 and csvs == 1 and other == 0
            and p3["final_report_has_212_224_31_1_468"] and p3["handoff_has_212_224_31_1_468"]
            and p3["final_report_old_61_48_absent"] and p3["handoff_old_61_48_absent"],
}
res["gates"]["P3"] = p3
print("[P3] ghidra_output %d = %d DISASM + %d PSEUDO + %d JSON + %d CSV + %d other -> %s"
      % (total_gh, dis, pseudo, js, csvs, other, "PASS" if p3["predicate"]["pass"] else "FAIL"))
if not p3["predicate"]["pass"]:
    res["errors"].append("P3 failed: %r" % p3)

# ---------------- P4: full-package untouchability ----------------
pre = json.load(open(PRE, "r", encoding="utf-8"))
pre_files = pre["files"]
changed, unchanged_ok, missing, new_files = [], [], [], []
for rel, meta in pre_files.items():
    p = os.path.join(RUN, *rel.split("\\"))
    if not os.path.exists(p):
        missing.append(rel)
        continue
    size, sha = sha_of(rel)
    if sha != meta["sha256"] or size != meta["size"]:
        changed.append({"path": rel, "intended": rel in INTENDED_CHANGED,
                        "pre": [meta["size"], meta["sha256"]], "post": [size, sha]})
    else:
        unchanged_ok.append(rel)
new_files = sorted(r for r in disk if r not in pre_files)
unintended = [c for c in changed if not c["intended"]]
p4 = {
    "pre_work_files": len(pre_files),
    "unchanged": len(unchanged_ok),
    "changed_total": len(changed),
    "changed_intended": [c["path"] for c in changed if c["intended"]],
    "changed_unintended": [c["path"] for c in unintended],
    "missing_on_disk": missing,
    "new_files_since_snapshot": new_files,
    "key_evidence_11": {},
}
for rel in KEY_EVIDENCE_11:
    pre_meta = pre_files.get(rel)
    size, sha = sha_of(rel)
    p4["key_evidence_11"][rel] = {
        "pre_sha": pre_meta["sha256"], "post_sha": sha,
        "status": "UNCHANGED" if sha == pre_meta["sha256"] else "CHANGED_INTENDED(" + INTENDED_CHANGED[rel] + ")"
                  if rel in INTENDED_CHANGED else "CHANGED_UNINTENDED",
    }
# qc_probe QC layer vs QC_PROBE_SHA256.txt (file is UTF-8 with BOM -> utf-8-sig)
qc_pins = {}
for ln in open(os.path.join(RUN, "00_CONTROL", "qc_probe", "QC_PROBE_SHA256.txt"), "r", encoding="utf-8-sig"):
    parts = ln.strip().split(",")
    if len(parts) == 3 and parts[1].lstrip("-").isdigit() and int(parts[1]) > 0:
        qc_pins[parts[0]] = (int(parts[1]), parts[2])
qc_bad = []
for name, (size_p, sha_p) in qc_pins.items():
    rel = "00_CONTROL\\qc_probe\\" + name
    size, sha = sha_of(rel)
    if size != size_p or sha != sha_p:
        qc_bad.append({"path": rel, "pin": [size_p, sha_p], "actual": [size, sha]})
p4["qc_probe_pins_checked"] = len(qc_pins)
p4["qc_probe_pin_mismatches"] = qc_bad
# QC_REPORT pre-work hash vs the QC_PROBE_SHA256.txt note row (pin 4A2EADDB...)
qc_report_pre = pre_files["06_REPORT\\QC_REPORT.md"]["sha256"]
p4["qc_report_pre_work_hash"] = qc_report_pre
p4["qc_report_pre_matches_qc_pin"] = qc_report_pre == "4A2EADDBB87158F8F9C11F9E66D229A470DDEBF13CF06EAB32EB93D76C37271E"
# GHIDRA_LOCAL vs its manifest
gl_bad = []
gl_rows = 0
for ln in open(os.path.join(RUN, "06_REPORT", "GHIDRA_LOCAL_COPY_MANIFEST.txt"), "r", encoding="utf-8"):
    parts = ln.strip().split(",")
    if len(parts) == 3 and parts[1].lstrip("-").isdigit():
        gl_rows += 1
        rel, size_p, sha_p = parts[0], int(parts[1]), parts[2]
        size, sha = sha_of(rel)
        if size != size_p or sha != sha_p:
            gl_bad.append({"path": rel, "claim": [size_p, sha_p], "actual": [size, sha]})
p4["ghidra_local_rows"] = gl_rows
p4["ghidra_local_mismatches"] = gl_bad
p4["predicate"] = {
    "only_intended_changed": not unintended and not missing,
    "key_evidence_7_unchanged": all(v["status"] == "UNCHANGED" for k, v in p4["key_evidence_11"].items()
                                    if v["status"] != "CHANGED_INTENDED(F1)" and v["status"] != "CHANGED_INTENDED(F4)"
                                    and "CHANGED" not in v["status"]),
    "key_evidence_4_changed_intended": all(v["status"].startswith("CHANGED_INTENDED") for k, v in p4["key_evidence_11"].items()
                                           if k in ("02_ANALYSIS\\B_template_loading_chain.md", "03_EVIDENCE\\VA_EVIDENCE_REGISTRY.md",
                                                    "06_REPORT\\00_FINAL_REPORT.md", "06_REPORT\\STAGE_ACCEPTANCE_GATES.csv")),
    "qc_probe_pins_ok": not qc_bad,
    "ghidra_local_ok": not gl_bad,
    "qc_report_pre_pin_ok": p4["qc_report_pre_matches_qc_pin"],
}
p4["predicate"]["key_evidence_7_unchanged"] = all(
    v["status"] == "UNCHANGED" for k, v in p4["key_evidence_11"].items() if k in (
        "01_RAW\\S1_ANCHOR_RESULT.json", "01_RAW\\S2_TRUE_WALK_RESULT.json", "01_RAW\\S3_PE_HEADER.json",
        "01_RAW\\S2_TEMPLATES_TRUE_WALK.csv", "01_RAW\\S4B_RAW_HITS.json",
        "02_ANALYSIS\\A_record_definition.md", "02_ANALYSIS\\C_transform_source_and_D_placement.md"))
p4["predicate"]["pass"] = all(v for k, v in p4["predicate"].items() if k != "pass")
res["gates"]["P4"] = p4
print("[P4] pre=%d unchanged=%d changed=%d (intended=%d unintended=%d) new=%d qcPinsBad=%d glBad=%d -> %s"
      % (len(pre_files), len(unchanged_ok), len(changed), len(p4["changed_intended"]), len(unintended),
         len(new_files), len(qc_bad), len(gl_bad), "PASS" if p4["predicate"]["pass"] else "FAIL"))
if not p4["predicate"]["pass"]:
    res["errors"].append("P4 failed: %r" % {k: p4["predicate"][k] for k in p4["predicate"] if k != "pass"})

# hashes of the PERSIST-produced/changed files for the record
record = {}
for rel in ["06_REPORT\\PE_MASTER_REVIEW.md", "06_REPORT\\QC_REPORT.md", "06_REPORT\\artifact_index.csv",
            "00_CONTROL\\qc_probe\\persist_gates.py"]:
    try:
        record[rel] = list(sha_of(rel))
    except OSError:
        record[rel] = None
res["persist_record_hashes"] = record

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print("result -> %s" % OUT)
print("== PERSIST GATES SUMMARY: %s (errors=%d) ==" % ("ALL_PASS" if not res["errors"] else "FAIL", len(res["errors"])))
sys.exit(1 if res["errors"] else 0)
