# -*- coding: utf-8 -*-
# Build artifact_index.csv (06_REPORT; no self-row per L12 precedent) and
# MANIFEST_SHA256.csv (package root; with MANIFEST_VALIDATION_ORDER section).
# Coverage: ALL package files EXCEPT 00_CONTROL\GHIDRA_LOCAL\ (project LOCAL-ONLY,
# covered by its own SHA manifests) and 00_CONTROL\__pycache__\ (build artifact).
# artifact_index excludes itself; MANIFEST excludes itself + artifact_index.csv
# (both generated in the same pass - ROUND precedent).
import hashlib, os, sys

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
PKG = "PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()

files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ("GHIDRA_LOCAL", "__pycache__")]
    for fn in sorted(filenames):
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        files.append((rel, os.path.getsize(p), sha256(p)))
files.sort()

# artifact_index.csv (06_REPORT) - exclude self
ai_path = os.path.join(ROOT, "06_REPORT", "artifact_index.csv")
n_ai = 0
with open(ai_path, "w", encoding="utf-8", newline="") as f:
    f.write("relative_path,size_bytes,sha256\n")
    for rel, sz, h in files:
        if rel == "06_REPORT/artifact_index.csv":
            continue
        f.write("%s,%d,%s\n" % (rel, sz, h))
        n_ai += 1
print("artifact_index.csv rows:", n_ai)

# MANIFEST_SHA256.csv (package root) - exclude self + artifact_index
mn_path = os.path.join(ROOT, "MANIFEST_SHA256.csv")
n_mn = 0
with open(mn_path, "w", encoding="utf-8", newline="") as f:
    f.write("path,sha256\n")
    for rel, sz, h in files:
        if rel in ("MANIFEST_SHA256.csv", "06_REPORT/artifact_index.csv"):
            continue
        f.write("%s\\%s,%s\n" % (PKG, rel.replace("/", "\\"), h))
        n_mn += 1
    f.write("# MANIFEST_VALIDATION_ORDER: the last correct-in-time manifest is BINDING for the files it covers; a closure manifest is binding for the files it covers.\n")
    f.write("# Discrepancies of earlier manifests vs files they no longer describe are DOCUMENTATION-class (not integrity-class). Concretes: RUN4 GHIDRA_LOCAL_MANIFEST_SHA256.csv described the PRE-ZS state (db.52/53) of the project that RUN4 itself later overwrote (db.63/64) - the RUN4 package integrity is governed by its closure manifest (49/49). The copy of the project in THIS package went through its own lifecycle: state at copy = db.63/64 (00_CONTROL\\GHIDRA_LOCAL_MANIFEST_AT_COPY.csv); after this run's two analyzeHeadless passes (-noanalysis, -process: rc1_ga_attrs.py + rc1_refcounts.py) the final state = db.67/68, governed by 00_CONTROL\\GHIDRA_LOCAL_MANIFEST_SHA256.csv (the shipping state). The two manifests differ ONLY in the .gbf lines.\n")
    f.write("# self-hash of MANIFEST_SHA256.csv is not embeddable; artifact_index.csv excluded (generated in the same pass); coverage: %d files (GHIDRA_LOCAL project LOCAL-ONLY under its own manifests; __pycache__ excluded as build artifact).\n" % n_mn)
    f.write("# evidence integrity (QC): 15 key executor evidence files hash-identical before/after the QC (03_EVIDENCE\\QC_REPORT.md section 10); GA5: 7 historical packages composite-hash before==after==now (03_EVIDENCE\\QC_GA5_IMMUTABLE.json); repo package docs/audits/PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912 untouched per git (HEAD==BASE, clean status).\n")
print("MANIFEST_SHA256.csv rows:", n_mn)
