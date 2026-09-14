# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 - finalize: gates, manifest,
# scope census, source identities. Every count recomputed FROM the CSV rows
# and raw artifacts (COUNTER_ARITHMETIC); nothing hand-typed.

import csv
import hashlib
import json
import os
import subprocess
import sys

BASE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
sys.path.insert(0, BASE + r"\00_CONTROL")
import sf30_core as C  # noqa: E402


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


# ---------- G0: source + base ------------------------------------------------
git_head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip()
git_origin = subprocess.check_output(
    ["git", "rev-parse", "origin/master"], cwd=REPO).decode().strip()
git_remote = subprocess.check_output(
    ["git", "ls-remote", "origin", "master"], cwd=REPO).decode().strip().split()[0]
git_status = subprocess.check_output(
    ["git", "status", "--short"], cwd=REPO).decode().strip().splitlines()
BASE_SHA = "1a490eed4ca2b295e78cd3cf851a08ac9c93930b"
pe = C.PE()  # fail-closed asserts on SHA/size/PE facts
exe_ok = (pe.sha256.upper() == C.EXPECTED_SHA256 and pe.size == C.EXPECTED_SIZE)
base_ok = (git_head == BASE_SHA and git_origin == BASE_SHA and git_remote == BASE_SHA)
# Dirty-path policy: by design the executor creates this run's package on disk
# (git mutations forbidden), so the package dir itself is an EXPECTED untracked
# path. Allowed untracked set: foreign experiments/ + this run's package dir.
allowed_untracked = {
    "?? experiments/",
    "?? docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/",
}
dirty_ok = (set(l.strip() for l in git_status) <= allowed_untracked)
G0 = exe_ok and base_ok and dirty_ok

# ---------- G1: positive control ----------------------------------------------
pc_txt = open(BASE + r"\01_RAW\POSITIVE_CONTROL_0050A050.txt", encoding="utf-8").read()
pc_ok = ("8bf1" in pc_txt and "8b4e30" in pc_txt and "8b11" in pc_txt
         and "8b4244" in pc_txt and "ffd0" in pc_txt
         and "ECX modified in window: NO - PASS" in pc_txt
         and "POSITIVE_CONTROL = PASS" in pc_txt)
# independent re-measure (not from the text file - from bytes again):
i_a = pe.disasm_one(0x0050A057)
i_b = pe.disasm_one(0x0050A05B)
i_c = pe.disasm_one(0x0050A064)
pc_ok = pc_ok and i_a["bytes"] == "8bf1" and i_b["bytes"] == "8b4e30" and i_c["bytes"] == "ffd0"
G1 = pc_ok

# ---------- G2: census completeness -------------------------------------------
rows = list(csv.DictReader(open(BASE + r"\02_ANALYSIS\SF30_WRITER_CENSUS.csv")))
from collections import Counter
cls_counts = Counter(r["classification"] for r in rows)
allowed = {"PROVEN_SF30_WRITER", "POSSIBLE_ALIAS", "REJECTED_ALIAS", "UNRESOLVED"}
vocab_ok = all(r["classification"] in allowed for r in rows)
raw_txt = open(BASE + r"\01_RAW\SF30_WRITER_RAW.txt", encoding="utf-8").read()
denom = None
for line in raw_txt.splitlines():
    if line.startswith("# RAW CANDIDATE COUNT"):
        denom = int(line.split(":")[1].strip())
enum_doc_ok = ("linear capstone sweep of full .text" in raw_txt
               and "WRITE mem-operand disp==0x30" in raw_txt)
state = json.load(open(BASE + r"\00_CONTROL\census_state.json"))
denom_csv = len(rows)
counts_match = (denom == denom_csv == state["raw_candidate_count"]
                and dict(cls_counts) == {k: v for k, v in
                                         state["classification_counts"].items()}
                and sum(cls_counts.values()) == len(rows))
cov_ok = ("(i) register-held SF-this" in raw_txt and "(ii) SF pointer held in a stack slot"
          in raw_txt and "(iii) combined-offset" in raw_txt and "(iv) bulk-init" in raw_txt)
G2 = vocab_ok and enum_doc_ok and counts_match and cov_ok and (denom_csv > 0)

# ---------- G3: provenance ------------------------------------------------------
prov = open(BASE + r"\02_ANALYSIS\SF30_PROVENANCE.md", encoding="utf-8").read()
proven_vas = sorted(r["writer_va"] for r in rows if r["classification"] == "PROVEN_SF30_WRITER")
g3_ok = True
for va in proven_vas:
    if va not in prov:
        g3_ok = False
g3_ok = g3_ok and ("SOURCE_PROVENANCE per PROVEN writer" in prov
                   and "RESOLVED (allocation->ctor->stored)" in prov)
G3 = g3_ok

# ---------- G4: type identity ---------------------------------------------------
rtti_txt = open(BASE + r"\01_RAW\SF30_RTTI_RAW.txt", encoding="utf-8").read()
g4_ok = ("CALIBRATION PASS = YES" in rtti_txt and ".?AVSceneFeederObject@@" in rtti_txt
         and "name verbatim = '.?AVNiNode@@'" in rtti_txt
          and "TD+0x08 name bytes (raw) = 2e3f41564e694e6f64654040" in rtti_txt
         and "slot-17 dword VALUE = 0x007B5390" in rtti_txt
         and "RECORDED ONLY" in rtti_txt and "NOT decoded" in rtti_txt)
# independent byte re-walk (calibration + link), fail-closed:
cal = pe.rtti_walk(0x00A7D458)
lk = pe.rtti_walk(0x00A8CCF4)
g4_ok = (g4_ok and cal["td"]["name"] == ".?AVSceneFeederObject@@"
         and lk["td"]["name"] == ".?AVNiNode@@")
G4 = g4_ok

# ---------- G5: scope held ------------------------------------------------------
# Executor set only: the QC additions (00_CONTROL/qc_probe/ probe scripts+outputs
# and 06_REPORT/QC_AUDIT_R1.md) are the QC's OWN record, were added AFTER the
# executor's original finalize run, and stay UNTOUCHED by this amendment
# (QC_AUDIT_R1.md section 9 convention: "outside the executor's manifest").
# They are therefore excluded from this gate census and from the manifest,
# exactly as at the original finalize run (when they did not exist). Measured
# reason (amend R1): the QC probe outputs quote the forbidden labels verbatim
# inside their own scope-census artifacts, which would trip THIS gate's substring
# detector on foreign content that is not this run's package (7 trip lines
# measured, incl. 2 in QC_AUDIT_R1.md's own wrapped sentences).
package_files = []
for root, _dirs, files in os.walk(BASE):
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, BASE)
        if rel.startswith("00_CONTROL" + os.sep + "qc_probe" + os.sep):
            continue
        if rel == os.path.join("06_REPORT", "QC_AUDIT_R1.md"):
            continue
        package_files.append(p)
FORBIDDEN_CLAIMS = ("MODEL_BRIDGE_CONFIRMED", "TRANSFORM_TO_MODEL")
claim_hits = []
for p in package_files:
    if p.endswith((".md", ".txt", ".csv", ".json")):
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for k in FORBIDDEN_CLAIMS:
            for line in t.splitlines():
                if k in line:
                    neg = ("NOT_DEMONSTRATED" in line or "not made" in line.lower()
                           or "no " in line.lower() or "NOT " in line
                           or "remains" in line.lower() or "zero" in line.lower())
                    if not neg:
                        claim_hits.append((os.path.relpath(p, BASE), line.strip()))
# no disassembly of the slot-17 target or the two forbidden callees may exist:
g5_scan_ok = True
for p in package_files:
    if p.endswith(".txt"):
        t = open(p, encoding="utf-8", errors="replace").read()
        # a decode of 0x007B5390 would produce listing headers with its VA as a start
        if "### 0x007B5390" in t or "derive_body(0x007B5390" in t or "FUN_007B5390:" in t:
            g5_scan_ok = False
G5 = (len(claim_hits) == 0) and g5_scan_ok

# gate census of candidate rows falling inside forbidden-function ranges
# (denominator entries only - no dissection):
def fn_range(start):
    body, end, _ = pe.derive_body(start)
    return start, end
forb_ranges = [fn_range(0x00437F70), fn_range(0x0082B5A0), fn_range(0x007B5390)]
in_forbidden = []
for r in rows:
    va = int(r["writer_va"], 16)
    for (s, e) in forb_ranges:
        if s <= va <= e:
            in_forbidden.append((r["writer_va"], s))

# ---------- write STAGE_ACCEPTANCE_GATES.csv -----------------------------------
GATES = [
    ("G0-SOURCE-BASE", G0,
     "EXE SHA+size==pins AND HEAD==origin/master==ls-remote==BASE_SHA AND dirty paths "
     "limited to foreign untracked experiments/ plus this run's own untracked package "
     "dir (created by the executor; git mutations forbidden)",
     "EXE sha=%s size=%d; HEAD=%s origin=%s remote=%s; dirty=%d lines (%s)"
     % (pe.sha256[:16], pe.size, git_head[:12], git_origin[:12], git_remote[:12],
        len(git_status), "; ".join(git_status))),
    ("G1-POSITIVE-CONTROL", G1,
     "0x50A05B window bytes + receiver chain measured exactly as specified",
     "measured: 0x50A057=8BF1 0x50A05B=8B4E30 0x50A05E=8B11 0x50A061=8B4244 0x50A064=FFD0; "
     "ECX unmodified between; receiver of call == [ESI+0x30]==[SF+0x30]"),
    ("G2-CENSUS-COMPLETENESS", G2,
     "(a) enumeration rule+range+raw denominator documented; (b) every candidate has a "
     "4-class row; (c) counts recomputed from CSV equal report counts; (d) coverage "
     "classes (i)-(iv) each scanned or declared",
     "raw denominator=%d (raw file == CSV rows == state json); counts %s; enum rule "
     "documented; coverage (i)-(iv) present in raw"
     % (denom, dict(cls_counts))),
    ("G3-PROVENANCE", G3,
     "every PROVEN_SF30_WRITER has a creation/receipt-level chain with VA+byte "
     "evidence, or per-edge SOURCE_PROVENANCE=UNRESOLVED",
     "PROVEN writers %s; both chains in SF30_PROVENANCE.md with hop tables; no "
     "UNRESOLVED edges needed (both RESOLVED)" % proven_vas),
    ("G4-TYPE-IDENTITY", G4,
     "RTTI chain byte-confirmed from physical EXE with calibration PASS on the known "
     "SceneFeederObject name first, or NO_VTABLE/UNKNOWN declared with reason",
     "calibration reproduced '.?AVSceneFeederObject@@'; link walk 0x00A8CCF4 -> COL "
     "0x00AAEEC8 -> TD 0x00B936C8 -> '.?AVNiNode@@'; re-walked independently at gate time"),
    ("G5-SCOPE-HELD", G5,
     "no slot-17 decode, no 0x437F70/0x82B5A0 analysis, no MODEL_BRIDGE/"
     "TRANSFORM_TO_MODEL claim in the package",
     "claim-context occurrences of forbidden labels: %d; slot-17 decode listings: 0; "
     "note: %d census denominator rows fall inside forbidden-function VA ranges "
     "(mechanical scan entries classified by receiver form only, no dissection)"
     % (len(claim_hits), len(in_forbidden))),
]
with open(BASE + r"\06_REPORT\STAGE_ACCEPTANCE_GATES.csv", "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["gate", "verdict", "pass_predicate", "raw_evidence"])
    for g, v, pred, ev in GATES:
        wr.writerow([g, "PASS" if v else "FAIL", pred, ev])

# ---------- write SOURCE_IDENTITIES.json ----------------------------------------
source_ids = {
    "run_id": "PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914",
    "era": "PCG_9_3_5",
    "mode": "STATIC-ONLY (the client never ran; no game binary process launched; "
            "byte-reading scripts only)",
    "repo": {
        "path": REPO,
        "base_sha_pinned": BASE_SHA,
        "head_measured": git_head,
        "origin_master_measured": git_origin,
        "ls_remote_master_measured": git_remote,
        "status_short": git_status,
        "git_mutations_by_executor": "NONE (no add/commit/push/stage; publication is a "
                                      "separate later step by pe-master-auditor)",
    },
    "exe": {
        "path": C.EXE_PATH,
        "sha256_measured": pe.sha256.upper(),
        "sha256_pinned": C.EXPECTED_SHA256,
        "size_measured": pe.size,
        "size_pinned": C.EXPECTED_SIZE,
        "machine": "0x%04X (i386)" % pe.machine,
        "opt_magic": "0x%04X (PE32)" % pe.opt_magic,
        "image_base": "0x%08X" % pe.image_base,
        "aslr": "no (IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE clear, measured)",
    },
    "prior_run_references_used_as_starting_points_only": {
        "note": "every fact re-derived from physical bytes in-run; prior-run values used "
                "only as fail-closed expectations",
        "PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914_REPORT": {
            "path": "docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/06_REPORT/REPORT.md",
            "sha256": sha256_file(os.path.join(REPO, "docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/06_REPORT/REPORT.md")),
        },
        "PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914_SLOT_DISASSEMBLY": {
            "path": "docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/01_RAW/SLOT_DISASSEMBLY.txt",
            "sha256": sha256_file(os.path.join(REPO, "docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/01_RAW/SLOT_DISASSEMBLY.txt")),
        },
        "PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913_REPORT": {
            "path": "docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md",
            "sha256": sha256_file(os.path.join(REPO, "docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md")),
        },
    },
    "administrative_correction_carried": "committed state of "
        "PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 is 27 package files, 26 manifest rows + "
        "manifest self (L12 self-exclusion precedent), 28 commit paths incl. "
        "AUDIT_ENTRYPOINT.md; the old figures '26 package files / 25 manifest rows' are "
        "superseded and not used here",
}
with open(BASE + r"\00_CONTROL\SOURCE_IDENTITIES.json", "w") as f:
    json.dump(source_ids, f, indent=1)

# ---------- SCRIPT_SHA256.csv -----------------------------------------------------
scripts = ["sf30_core.py", "census.py", "finalize.py", "census_state.json"]
with open(BASE + r"\00_CONTROL\SCRIPT_SHA256.csv", "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["script", "role", "sha256"])
    roles = {
        "sf30_core.py": "own PE parser + capstone decode + RTTI walker (fail-closed identity asserts)",
        "census.py": "Tasks A/B/C + positive control: enumeration, classification, provenance, RTTI",
        "finalize.py": "gates, scope census, source identities, manifests (this script)",
        "census_state.json": "script-emitted census state (machine-readable, recomputed by finalize)",
    }
    for s in scripts:
        wr.writerow([s, roles[s], sha256_file(os.path.join(BASE, "00_CONTROL", s))])

# ---------- MANIFEST_SHA256.csv (self-exclusion per L12 precedent) ------------------
manifest_path = BASE + r"\06_REPORT\MANIFEST_SHA256.csv"
manifest_rows = []
for p in sorted(package_files):
    rel = os.path.relpath(p, BASE)
    if rel == os.path.relpath(manifest_path, BASE):
        continue  # L12 self-exclusion precedent: rows = package files minus the manifest itself
    manifest_rows.append((rel.replace("\\", "/"), sha256_file(p)))
with open(manifest_path, "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["file", "sha256"])
    for rel, h in manifest_rows:
        wr.writerow([rel, h])

print("FINALIZE OK")
print("G0..G5:", [g for g, v, _, _ in GATES], "=", [bool(v) for _, v, _, _ in GATES])
print("denominator:", denom, "counts:", dict(cls_counts))
print("manifest rows:", len(manifest_rows), "(manifest itself excluded)")
print("claim_hits:", claim_hits)
print("candidates inside forbidden fn ranges (denominator-only):", len(in_forbidden))
for x in in_forbidden[:10]:
    print("   ", x)
