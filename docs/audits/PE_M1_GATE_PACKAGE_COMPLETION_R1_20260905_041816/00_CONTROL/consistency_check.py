#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# consistency_check.py -- PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816
#
# W5: THE FAIL-CLOSED INTERNAL-CONSISTENCY CHECK of the completed gate package.
# Checks (all must PASS; any failure => loud FAIL + non-zero exit + HARD STOP):
#   1. every SHA256 in EVIDENCE_MANIFEST.json re-hashed from the physical file;
#   2. every JSON in the package parses;
#   3. the CSV schemas match their generators (+ every file in the run's
#      artifact_index.csv re-hashed; the 2 documented exclusions);
#   4. the 57 repair-run artifact SHAs cross-checked against its artifact_index.csv;
#   5. the V3 copies in GATES\ hash-identical to the source V3;
#   6. append-only proofs: the frozen pre-append copies are byte-prefixes of the
#      current GATE_INDEX.md / GATES\AMENDMENTS.md;
#   7. the pre-existing files UNMODIFIED (REPORT_V1/V2, the old matrix copies,
#      the amendment records);
#   8. package completeness: the 5 promised files + the correction notes exist;
#   9. the W3/W4 citations present (14,104 / 103,073 / MASTER_ACCEPTED / 8 files
#      10 events / NOT_MEASURED) in the built files;
#  10. structure counts: 19 claims / 19 registry / 7 open / 8 originals;
#  11. no original payload committed: no committed file matches any original
#      payload SHA; all committed files are derived metadata (< 1 MB each).
#
# Output: 01_RAW\consistency_report.json (excluded from artifact_index.csv by
# the documented-exclusions rule, as is artifact_index.csv itself).

import hashlib
import json
import os
import re
import sys

RUN_ID = "PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816"
RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
GATE = os.path.join(REPO, r"docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE")
REPO_RUN = os.path.join(REPO, r"docs\audits\PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816")
REPAIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439"
M1TREE = r"D:\Eudoria_Reconstruction\99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1"
EVID = os.path.join(M1TREE, "03_EVIDENCE")

problems = []
checked = {"sha_rehash": 0, "json_parse": 0, "csv_rows": 0, "prefix": 0}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def req_hash(path, expected, what):
    checked["sha_rehash"] += 1
    if not os.path.isfile(path):
        problems.append("MISSING FILE (%s): %s" % (what, path))
        return None
    actual = sha256_file(path)
    if expected is not None and actual != expected.upper():
        problems.append("SHA MISMATCH (%s): %s expected %s got %s" % (what, path, expected, actual))
        return None
    return actual

def req_json(path, what):
    checked["json_parse"] += 1
    if not os.path.isfile(path):
        problems.append("MISSING JSON (%s): %s" % (what, path))
        return None
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        problems.append("JSON PARSE FAILURE (%s): %s :: %s" % (what, path, e))
        return None

def req_text(path, what):
    if not os.path.isfile(path):
        problems.append("MISSING FILE (%s): %s" % (what, path))
        return ""
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

# ---------------------------------------------------------------------------
# 0. load the manifest
# ---------------------------------------------------------------------------
man_path = os.path.join(GATE, "EVIDENCE_MANIFEST.json")
man = req_json(man_path, "the built manifest")
if man is None:
    print(json.dumps({"verdict": "FAIL", "problems": problems}, indent=1))
    sys.exit(1)

# ---------------------------------------------------------------------------
# 1. every SHA in the manifest re-hashed from the physical file
# ---------------------------------------------------------------------------
bf = man["built_from"]
req_hash(bf["M1_GATE_DELIVERABLE_MATRIX_V3.md"]["local_path"],
         bf["M1_GATE_DELIVERABLE_MATRIX_V3.md"]["sha256"], "built_from V3 md")
req_hash(bf["M1_GATE_DELIVERABLE_MATRIX_V3.json"]["local_path"],
         bf["M1_GATE_DELIVERABLE_MATRIX_V3.json"]["sha256"], "built_from V3 json")
req_hash(bf["DOMAIN_MANIFEST.json"]["local_path"],
         bf["DOMAIN_MANIFEST.json"]["sha256"], "built_from DOMAIN_MANIFEST")
req_hash(bf["repair_artifact_index_csv"]["local_path"],
         bf["repair_artifact_index_csv"]["sha256"], "built_from artifact_index.csv")
req_hash(bf["M1_LEDGER.md"]["local_path"],
         bf["M1_LEDGER.md"]["sha256"], "built_from ledger")
req_hash(os.path.join(M1TREE, r"02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md"),
         bf["old_matrix_frozen"]["sha256"], "built_from old matrix")
req_hash(os.path.join(REPO, r"docs\audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\PE_MASTER_REVIEW.md"),
         bf["PE_MASTER_REVIEW.md"]["sha256"], "built_from PE_MASTER_REVIEW")

for c in man["claims_19_rows"]:
    for s in c["sources"]:
        req_hash(s["local_path"], s["sha256"], "claim %s source %s" % (c["claim_id"], os.path.basename(s["local_path"])))
    for g in c["generator"]["repair_run_scripts"]:
        req_hash(os.path.join(REPAIR, g["path"]), g["sha256"], "claim %s generator script %s" % (c["claim_id"], g["path"]))
    req_hash(os.path.join(REPAIR, c["generator"]["v3_generator_script"]["path"]),
             c["generator"]["v3_generator_script"]["sha256"], "claim %s v3 generator script" % c["claim_id"])

for k, ev in man["this_run_evidence_repair_run"].items():
    req_hash(ev["path"], ev["sha256"], "repair evidence %s" % k)

for o in man["local_only_original_sources"]:
    req_hash(o["local_canonical_path"], o["sha256"], "original %s" % os.path.basename(o["local_canonical_path"]))

req_hash(os.path.join(REPO, r"docs\audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\PE_MASTER_REVIEW.md"),
         man["post_audit_confirmation"]["sha256"], "post_audit_confirmation PE_MASTER_REVIEW")

for cd in man["citation_defects"]:
    req_hash(os.path.join(EVID, cd["file"]), cd["physical_sha256"], "citation_defect physical")
    req_hash(os.path.join(REPO, cd["companion_repo_file"]["path"]),
             cd["companion_repo_file"]["sha256"], "citation_defect companion repo file")
    if cd["cited_sha_in_old_matrix_and_v3"] != cd["companion_repo_file"]["sha256"]:
        problems.append("citation_defect reconciliation broken: the cited SHA != the companion repo file SHA")

# the regression-sweep page hashes quoted by the manifest (V3 record) must re-verify
for pg in man["regression_sweep"]["pages"]:
    if pg["recorded"] != pg["fresh"] or pg["verdict"] != "MATCH":
        problems.append("regression_sweep page not MATCH: %s" % pg["page"])

# ---------------------------------------------------------------------------
# 2. every JSON in the package parses
# ---------------------------------------------------------------------------
for j in [os.path.join(GATE, "EVIDENCE_MANIFEST.json"),
          os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX.json"),
          os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX_V3.json"),
          os.path.join(GATE, r"GATES\AMENDMENT_ITER035_ROWS10_11.json"),
          os.path.join(GATE, r"GATES\AMENDMENT_ITER036_CLOSURE.json")]:
    req_json(j, "package JSON " + os.path.basename(j))

# ---------------------------------------------------------------------------
# 3. the 57 repair-run artifact SHAs cross-checked + this run's CSV schemas
# ---------------------------------------------------------------------------
art_path = os.path.join(REPAIR, "artifact_index.csv")
with open(art_path, "r", encoding="ascii") as f:
    lines = [ln.rstrip("\n") for ln in f if ln.strip()]
if lines[0] != "relative_path,sha256,bytes":
    problems.append("repair artifact_index.csv schema drift")
n57 = 0
for ln in lines[1:]:
    rp, s, b = ln.rsplit(",", 2)
    n57 += 1
    req_hash(os.path.join(REPAIR, rp), s, "repair artifact " + rp)
    if os.path.getsize(os.path.join(REPAIR, rp)) != int(b):
        problems.append("repair artifact size drift: " + rp)
if n57 != 57:
    problems.append("repair artifact_index.csv rows = %d (expected 57)" % n57)

# this run's STAGE_ACCEPTANCE_GATES.csv schema
sag = os.path.join(RUN_DIR, "STAGE_ACCEPTANCE_GATES.csv")
sag_txt = req_text(sag, "run STAGE_ACCEPTANCE_GATES.csv")
if not sag_txt.startswith("gate,status,evidence\n"):
    problems.append("run STAGE_ACCEPTANCE_GATES.csv schema drift")

# this run's artifact_index.csv: schema + re-hash everything listed
aidx = os.path.join(RUN_DIR, "artifact_index.csv")
with open(aidx, "r", encoding="utf-8") as f:
    alines = [ln.rstrip("\n") for ln in f if ln.strip()]
if alines[0] != "relative_path,sha256,bytes,origin":
    problems.append("run artifact_index.csv schema drift")
for ln in alines[1:]:
    rp, s, b, origin = ln.rsplit(",", 3)
    checked["csv_rows"] += 1
    if origin == "EXCLUDED":
        continue
    p = os.path.join(RUN_DIR, rp)
    req_hash(p, s, "run artifact " + rp)
    if os.path.isfile(p) and os.path.getsize(p) != int(b):
        problems.append("run artifact size drift: " + rp)
    # repo run-package copies must be hash-identical to the local originals
    if rp.upper().startswith("00_CONTROL") or rp.upper().startswith("05_ANALYSIS") or rp in ("REPORT.md", "HANDOFF.md", "STAGE_ACCEPTANCE_GATES.csv"):
        rp_repo = os.path.join(REPO_RUN, rp)
        req_hash(rp_repo, s, "repo run package copy " + rp)

# ---------------------------------------------------------------------------
# 4. the V3 copies hash-identical to the sources
# ---------------------------------------------------------------------------
for src, dst in [(os.path.join(REPAIR, r"05_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX_V3.md"),
                  os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX_V3.md")),
                 (os.path.join(REPAIR, r"05_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX_V3.json"),
                  os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX_V3.json"))]:
    checked["sha_rehash"] += 1
    if sha256_file(src) != sha256_file(dst):
        problems.append("V3 copy NOT hash-identical: " + dst)

# ---------------------------------------------------------------------------
# 5. append-only proofs (frozen pre-append copies are byte-prefixes)
# ---------------------------------------------------------------------------
for pre, cur in [(os.path.join(RUN_DIR, r"01_RAW\GATE_INDEX.md.pre"), os.path.join(GATE, "GATE_INDEX.md")),
                 (os.path.join(RUN_DIR, r"01_RAW\AMENDMENTS.md.pre"), os.path.join(GATE, r"GATES\AMENDMENTS.md"))]:
    checked["prefix"] += 1
    with open(pre, "rb") as f:
        pre_b = f.read()
    with open(cur, "rb") as f:
        cur_b = f.read()
    if not cur_b.startswith(pre_b):
        problems.append("APPEND-ONLY VIOLATION (the pre-append copy is not a byte-prefix): " + cur)

# ---------------------------------------------------------------------------
# 6. the pre-existing files UNMODIFIED
# ---------------------------------------------------------------------------
# append-live control mirrors in the repo run package must be byte-identical to the local finals
for rel in (r"00_CONTROL\sha256_control.txt",):
    loc = os.path.join(RUN_DIR, rel)
    rep = os.path.join(REPO_RUN, rel)
    checked["sha_rehash"] += 1
    if not (os.path.isfile(loc) and os.path.isfile(rep)):
        problems.append("append-live mirror missing: %s (local=%s repo=%s)" % (rel, os.path.isfile(loc), os.path.isfile(rep)))
    elif sha256_file(loc) != sha256_file(rep):
        problems.append("append-live mirror drift: " + rel)

OLD_EXPECTED = {
    os.path.join(GATE, "GATE_INDEX.md"): None,  # appended (prefix-proof above)
    os.path.join(GATE, "REPORT_V1_SUPERSEDED.md"): "4DAC73896CEAB8DC2AB0384A757098AE662CC5AEDCF49EB12D9AD4EFC8CA5B05",
    os.path.join(GATE, "REPORT_V2_REJUDGMENT.md"): "12AE3410E5C2663E0F945086F446EDA16F0F653106B1D5580E1857739E8C3415",
    os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX.md"): "F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1",
    os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX.json"): "F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928",
    os.path.join(GATE, r"GATES\AMENDMENT_ITER035_ROWS10_11.json"): "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385",
    os.path.join(GATE, r"GATES\AMENDMENT_ITER036_CLOSURE.json"): "CBBEEEB9DF345FA804FE79011AF23D0F685E2CE51582B472BB3709BB3D590AE1",
}
for p, e in OLD_EXPECTED.items():
    if e is not None:
        req_hash(p, e, "pre-existing file unmodified " + os.path.basename(p))

# the frozen old matrix copies must equal the M1-tree originals (they are copies)
for a, b in [(os.path.join(M1TREE, r"02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md"),
              os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX.md")),
             (os.path.join(M1TREE, r"02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.json"),
              os.path.join(GATE, r"GATES\M1_GATE_DELIVERABLE_MATRIX.json"))]:
    checked["sha_rehash"] += 1
    if sha256_file(a) != sha256_file(b):
        problems.append("frozen matrix copy drifted from the M1-tree original: " + b)

# ---------------------------------------------------------------------------
# 7. package completeness
# ---------------------------------------------------------------------------
for must in ["EVIDENCE_MANIFEST.json", "RETRACTIONS.md", "UNRESOLVED.md",
             "ROADMAP_MAPPING.md", "HANDOFF.md", "CORRECTION_NOTES.md",
             "GATE_INDEX.md", "REPORT_V1_SUPERSEDED.md", "REPORT_V2_REJUDGMENT.md",
             r"GATES\M1_GATE_DELIVERABLE_MATRIX_V3.md",
             r"GATES\M1_GATE_DELIVERABLE_MATRIX_V3.json"]:
    p = os.path.join(GATE, must)
    if not os.path.isfile(p) or os.path.getsize(p) == 0:
        problems.append("PACKAGE INCOMPLETE: missing/empty " + must)

# ---------------------------------------------------------------------------
# 8. the W3/W4 citations present in the built files
# ---------------------------------------------------------------------------
def ws(t):
    """normalize whitespace so citation needles survive markdown line-wrapping"""
    return re.sub(r"\s+", " ", t)

gate_index_txt = ws(req_text(os.path.join(GATE, "GATE_INDEX.md"), "GATE_INDEX"))
retr_txt = ws(req_text(os.path.join(GATE, "RETRACTIONS.md"), "RETRACTIONS"))
unres_txt = ws(req_text(os.path.join(GATE, "UNRESOLVED.md"), "UNRESOLVED"))
roadmap_txt = ws(req_text(os.path.join(GATE, "ROADMAP_MAPPING.md"), "ROADMAP_MAPPING"))
handoff_txt = ws(req_text(os.path.join(GATE, "HANDOFF.md"), "HANDOFF"))
notes_txt = ws(req_text(os.path.join(GATE, "CORRECTION_NOTES.md"), "CORRECTION_NOTES"))

cites = [
    ("14,104/229,376", [retr_txt, notes_txt, handoff_txt, unres_txt, gate_index_txt]),
    ("103,073/1,245,184", [retr_txt, notes_txt, handoff_txt, gate_index_txt]),
    ("NOT_MEASURED", [notes_txt, retr_txt]),
    ("8 files / 10 events", [notes_txt]),
    ("8 log FILES / 10 logged EVENTS", [retr_txt]),
    ("MASTER_ACCEPTED", [gate_index_txt, retr_txt, handoff_txt, notes_txt]),
    ("DD598152", [notes_txt, retr_txt, gate_index_txt]),
    ("F299C622", [notes_txt, retr_txt, gate_index_txt]),
]
for needle, texts in cites:
    if not any(needle in t for t in texts):
        problems.append("REQUIRED CITATION MISSING: %r (checked %d built files)" % (needle, len(texts)))

# the manifest's post-audit confirmation numbers must be internally consistent
pac = man["post_audit_confirmation"]["confirms"]
if pac["pc24_real_domain_lerp_sensitivity"]["value"] != "14104/229376":
    problems.append("manifest pc24 real-domain value drift: " + pac["pc24_real_domain_lerp_sensitivity"]["value"])
if pac["pc24_synthetic_domain_lerp_sensitivity_auditor_side"]["value"] != "103,073/1,245,184":
    problems.append("manifest pc24 synthetic-domain value drift")

# ---------------------------------------------------------------------------
# 9. structure counts
# ---------------------------------------------------------------------------
if len(man["claims_19_rows"]) != 19:
    problems.append("manifest claims = %d (expected 19)" % len(man["claims_19_rows"]))
if len(man["era_bounded_registry"]) != 19:
    problems.append("manifest registry = %d (expected 19)" % len(man["era_bounded_registry"]))
if len(man["known_open_v3"]) != 7:
    problems.append("manifest known_open_v3 = %d (expected 7)" % len(man["known_open_v3"]))
if len(man["local_only_original_sources"]) != 8:
    problems.append("manifest originals = %d (expected 8)" % len(man["local_only_original_sources"]))
if len(man["hygiene_correction_notes"]["findings"]) != 5:
    problems.append("manifest hygiene findings = %d (expected 5)" % len(man["hygiene_correction_notes"]["findings"]))
if len(man["citation_defects"]) != 1:
    problems.append("manifest citation_defects = %d (expected 1)" % len(man["citation_defects"]))

# every claim must carry the contract section-7 fields
for c in man["claims_19_rows"]:
    for field in ("sources", "generator", "measured_quantity_and_denominator",
                  "independent_source_of_truth", "why_non_circular",
                  "failure_case_detected", "dependencies", "limitations",
                  "v3_verdict", "era"):
        if not c.get(field):
            problems.append("claim %s missing field %s" % (c["claim_id"], field))

# ---------------------------------------------------------------------------
# 10. no original payload committed
# ---------------------------------------------------------------------------
PAYLOAD_SHAS = {o["sha256"] for o in man["local_only_original_sources"]}
committed = []
for root in (GATE, REPO_RUN):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            committed.append(os.path.join(dirpath, fn))
for p in committed:
    if os.path.getsize(p) > (1 << 20):
        problems.append("committed file > 1MB (payload suspicion): " + p)
    if sha256_file(p) in PAYLOAD_SHAS:
        problems.append("ORIGINAL PAYLOAD COMMITTED: " + p)

# ---------------------------------------------------------------------------
# verdict
# ---------------------------------------------------------------------------
report = {
    "run_id": RUN_ID,
    "verdict": "PASS" if not problems else "FAIL",
    "checks": {
        "sha_rehash_performed": checked["sha_rehash"],
        "json_files_parsed": checked["json_parse"],
        "csv_rows_verified": checked["csv_rows"],
        "append_only_prefix_proofs": checked["prefix"],
        "repair_artifacts_crosschecked": n57,
        "committed_files_scanned_for_payload": len(committed),
    },
    "problems": problems,
}
out = os.path.join(RUN_DIR, r"01_RAW\consistency_report.json")
with open(out, "w", encoding="ascii", newline="\n") as f:
    json.dump(report, f, indent=1)
    f.write("\n")

print(json.dumps(report, indent=1))
print("CONSISTENCY %s (%d re-hashes); report -> %s" % (report["verdict"], checked["sha_rehash"], out))
sys.exit(0 if not problems else 2)
