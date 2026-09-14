# -*- coding: utf-8 -*-
# QC probe 1 — COUNTER_ARITHMETIC (independent recount of every printed count)
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# Output: 00_CONTROL/qc_probe/out_qc1_counters.txt
import csv, hashlib, json, os, re, struct, sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
OUT = []

def log(s=""):
    OUT.append(s)
    print(s)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

log("== QC1 COUNTER_ARITHMETIC (own recount) ==")

# --- package file census -----------------------------------------------------
pkg_files = []
for root, _d, files in os.walk(PKG):
    for f in files:
        pkg_files.append(os.path.relpath(os.path.join(root, f), PKG).replace("\\", "/"))
qc_probe_files = [f for f in pkg_files if f.startswith("00_CONTROL/qc_probe/")]
executor_files = [f for f in pkg_files if not f.startswith("00_CONTROL/qc_probe/")]
log("package files now on disk: %d (executor package: %d; QC probe files: %d)"
    % (len(pkg_files), len(executor_files), len(qc_probe_files)))
log("executor files: %s" % ", ".join(sorted(executor_files)))

# --- manifest verification (C11) ---------------------------------------------
man_path = os.path.join(PKG, "06_REPORT/MANIFEST_SHA256.csv")
man = list(csv.reader(open(man_path)))
man_head, man_rows = man[0], man[1:]
log("")
log("== MANIFEST ==")
log("manifest data rows: %d (header: %s)" % (len(man_rows), ",".join(man_head)))
expected_rows = len(executor_files) - 1  # minus the manifest itself (L12 self-exclusion)
log("expected rows = executor files (%d) - manifest itself (1) = %d -> %s"
    % (len(executor_files), expected_rows, "MATCH" if len(man_rows) == expected_rows else "MISMATCH"))
log("manifest self-exclusion held: %s" % ("YES" if not any(r[0] == "06_REPORT/MANIFEST_SHA256.csv" for r in man_rows) else "NO (self listed!)"))
bad = []
listed = set()
for rel, h in [(r[0], r[1]) for r in man_rows]:
    listed.add(rel)
    actual = sha(os.path.join(PKG, rel))
    if actual != h:
        bad.append((rel, h, actual))
missing = sorted(set(executor_files) - listed - {"06_REPORT/MANIFEST_SHA256.csv"})
extra = sorted(listed - set(executor_files))
log("hash mismatches: %d %s" % (len(bad), bad if bad else ""))
log("executor files not in manifest: %s" % (missing if missing else "none"))
log("manifest rows not on disk: %s" % (extra if extra else "none"))

# --- script SHA table (C11) ----------------------------------------------------
log("")
log("== SCRIPT_SHA256 ==")
scr = list(csv.reader(open(os.path.join(PKG, "00_CONTROL/SCRIPT_SHA256.csv"))))
bad2 = []
for rel, role, h in scr[1:]:
    actual = sha(os.path.join(PKG, "00_CONTROL", rel))
    log("  %-18s %s %s" % (rel, "OK" if actual == h else "MISMATCH", ""))
    if actual != h:
        bad2.append(rel)
log("script hash mismatches: %s" % (bad2 if bad2 else "none"))
# scripts present in 00_CONTROL vs table:
ctrl_files = sorted(f for f in executor_files if f.startswith("00_CONTROL/") and f.endswith(".py"))
log("00_CONTROL python scripts on disk: %s" % ctrl_files)
log("script table covers: %s" % [r[0] for r in scr[1:]])

# --- CSV recount (C1/C10) ------------------------------------------------------
log("")
log("== CENSUS CSV recount (own parse) ==")
rows = list(csv.DictReader(open(os.path.join(PKG, "02_ANALYSIS/SF30_WRITER_CENSUS.csv"))))
from collections import Counter
cc = Counter(r["classification"] for r in rows)
log("CSV data rows: %d" % len(rows))
log("class counts: %s" % dict(cc))
log("sum check: %d" % sum(cc.values()))
log("PERVEN rows: %s" % sorted(r["writer_va"] for r in rows if r["classification"] == "PROVEN_SF30_WRITER"))
log("UNRESOLVED rows: %d" % cc.get("UNRESOLVED", 0))
# claimed numbers:
CLAIM = {"PROVEN_SF30_WRITER": 2, "POSSIBLE_ALIAS": 618, "REJECTED_ALIAS": 3023, "UNRESOLVED": 0}
log("claim match (2/618/3023/0, total 3643): %s" % ("PASS" if dict(cc) == CLAIM and len(rows) == 3643 else "FAIL"))

# unique writer_va check
vas = [r["writer_va"] for r in rows]
log("unique writer_va: %d (dups: %s)" % (len(set(vas)), len(vas) - len(set(vas))))
# function attribution census
fn_counter = Counter(r["function_va"] for r in rows)
log("distinct function_va values: %d; UNATTRIBUTED rows: %d" % (len(fn_counter), fn_counter.get("UNATTRIBUTED", 0)))

# --- raw file block count (C1) -------------------------------------------------
log("")
log("== RAW FILE ==")
raw = open(os.path.join(PKG, "01_RAW/SF30_WRITER_RAW.txt"), encoding="utf-8", errors="replace").read()
blocks = re.findall(r"^### (0x[0-9A-F]{8})", raw, re.M)
log("per-candidate '###' blocks: %d" % len(blocks))
log("blocks unique: %d" % len(set(blocks)))
csv_vas = set(vas)
blk_vas = set(blocks)
log("CSV rows without raw block: %d" % len(csv_vas - blk_vas))
log("raw blocks without CSV row: %d" % len(blk_vas - csv_vas))
# ordering: raw blocks are in sweep order; CSV too?
log("same order raw vs csv: %s" % ("YES" if blocks == vas else "NO"))
# raw header denominator
m = re.search(r"RAW CANDIDATE COUNT \(denominator before classification\): (\d+)", raw)
log("raw header denominator: %s" % (m.group(1) if m else "NOT FOUND"))
m2 = re.search(r"instructions decoded in sweep: (\d+) ; sweep bad-byte restarts: (\d+)", raw)
log("raw header sweep stats: decoded=%s restarts=%s" % (m2.group(1), m2.group(2)) if m2 else "NOT FOUND")
m3 = re.search(r"raw candidate base-register distribution: (.+)", raw)
log("base-register distribution: %s" % (m3.group(1) if m3 else "NOT FOUND"))

# --- state json cross-check -----------------------------------------------------
st = json.load(open(os.path.join(PKG, "00_CONTROL/census_state.json")))
log("")
log("== census_state.json ==")
log("raw_candidate_count=%s sweep_instructions=%s" % (st["raw_candidate_count"], st["sweep_instructions"]))
log("classification_counts=%s" % st["classification_counts"])
log("state == CSV recount: %s" % (st["raw_candidate_count"] == len(rows) and st["classification_counts"] == {k: v for k, v in cc.items() if v}))

# --- prior-run reference hashes (SOURCE_IDENTITIES) -----------------------------
log("")
log("== prior-run reference hashes ==")
ids = json.load(open(os.path.join(PKG, "00_CONTROL/SOURCE_IDENTITIES.json")))
for k, v in ids["prior_run_references_used_as_starting_points_only"].items():
    if isinstance(v, dict) and "sha256" in v:
        actual = sha(os.path.join(REPO, v["path"]))
        log("  %-55s recorded=%s.. actual=%s.. %s" % (k, v["sha256"][:16], actual[:16], "OK" if actual == v["sha256"] else "MISMATCH"))

# --- REPORT/HANDOFF number consistency -----------------------------------------
log("")
log("== REPORT/HANDOFF printed numbers ==")
rep = open(os.path.join(PKG, "06_REPORT/REPORT.md"), encoding="utf-8").read()
han = open(os.path.join(PKG, "06_REPORT/HANDOFF.md"), encoding="utf-8").read()
for pat, where in [
    (r"3643", "3643 denominator"),
    (r"2,266,698|2266698", "swept instructions"),
    (r"618", "POSSIBLE 618"),
    (r"3023", "REJECTED 3023"),
    (r"0x005093C3", "writer1"),
    (r"0x0050A2D1", "writer2"),
    (r"\.\?AVNiNode@@", "RTTI name"),
    (r"0x007B5390", "slot17 value"),
]:
    log("  %-28s REPORT:%-3s HANDOFF:%-3s" % (where, "yes" if re.search(pat, rep) else "no", "yes" if re.search(pat, han) else "no"))

open(os.path.join(PKG, "00_CONTROL/qc_probe/out_qc1_counters.txt"), "w").write("\n".join(OUT) + "\n")
log("")
log("QC1 DONE")
