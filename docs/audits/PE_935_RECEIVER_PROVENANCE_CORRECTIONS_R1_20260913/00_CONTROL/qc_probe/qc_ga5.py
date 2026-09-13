# -*- coding: utf-8 -*-
# QC GA5: own hash census of historical packages. Covers the executor's 7 + the
# 296445-ERRATA package. Compares my-now vs executor-before vs executor-after.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY (read-only hashing).
import hashlib, json, os, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import save_json

AUD = r"D:\Eudoria_Reconstruction\99_Audits"
RUN_ROOT = os.path.join(AUD, "PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913")

EXECUTOR_PACKAGES = {
    "RUN1_TEMPLATE_CONSUMER_TRACE": os.path.join(AUD, "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"),
    "RUN2_EXTERNAL_SOURCES_MATRIX": os.path.join(AUD, "PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913"),
    "RUN3_STATIC_INSTANCE_TRACE": os.path.join(AUD, "PE_935_STATIC_INSTANCE_TRACE_R1_20260913"),
    "RUN4_PLACEMENT_SOURCE_TRACE": os.path.join(AUD, "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"),
    "ROUND_CLOSURE": os.path.join(AUD, "PE_935_STATIC_PLACEMENT_ROUND1_20260913"),
    "JOIN_ERRATA_R2": os.path.join(AUD, "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"),
    "DESKTOP_AUDIT": os.path.join(AUD, "PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913"),
    "ERRATA_296445": os.path.join(AUD, "PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"),
}

def census(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for blk in iter(lambda: f.read(1 << 20), b""):
                    h.update(blk)
            files.append((rel, os.path.getsize(p), h.hexdigest().upper()))
    files.sort()
    comp = hashlib.sha256()
    for rel, sz, fh in files:
        comp.update(("%s|%d|%s\n" % (rel, sz, fh)).encode("utf-8"))
    return dict(file_count=len(files), total_bytes=sum(f[1] for f in files),
                composite_sha256=comp.hexdigest().upper())

before = json.load(open(os.path.join(RUN_ROOT, "01_RAW", "GA5_IMMUTABLE_CENSUS_before.json")))["packages"]
after = json.load(open(os.path.join(RUN_ROOT, "01_RAW", "GA5_IMMUTABLE_CENSUS_after.json")))["packages"]

R = {"packages": {}}
for name, root in sorted(EXECUTOR_PACKAGES.items()):
    mine = census(root)
    entry = dict(my_now=mine)
    if name in before:
        entry["executor_before"] = dict(composite=before[name]["composite_sha256"],
                                        files=before[name]["file_count"],
                                        bytes=before[name]["total_bytes"])
        entry["executor_after"] = dict(composite=after[name]["composite_sha256"],
                                       files=after[name]["file_count"],
                                       bytes=after[name]["total_bytes"])
        entry["compare"] = dict(
            my_now_vs_before=mine["composite_sha256"] == before[name]["composite_sha256"],
            my_now_vs_after=mine["composite_sha256"] == after[name]["composite_sha256"],
            before_vs_after=before[name]["composite_sha256"] == after[name]["composite_sha256"],
            counts=(mine["file_count"], before[name]["file_count"], after[name]["file_count"]))
    else:
        entry["note"] = "not in executor GA5 set (added by QC per task instruction)"
    R["packages"][name] = entry

R["summary"] = {}
for name, e in R["packages"].items():
    if "compare" in e:
        R["summary"][name] = e["compare"]
    else:
        R["summary"][name] = dict(file_count=e["my_now"]["file_count"],
                                  composite=e["my_now"]["composite_sha256"])

p = save_json("QC_GA5_IMMUTABLE.json", R)
print("saved", p)
for name, s in R["summary"].items():
    print(name, s)
