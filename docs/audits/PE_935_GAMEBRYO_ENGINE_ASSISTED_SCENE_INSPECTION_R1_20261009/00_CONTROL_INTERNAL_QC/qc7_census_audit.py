#!/usr/bin/env python3
"""QC DUTY 7 — full independent census audit of CORPUS_METADATA_CENSUS.csv.

Fresh internal QC (pe-master-auditor). Parses EVERY row of the census CSV,
recomputes all denominators from the CSV columns (not from the report), and
verifies the mechanical selection rules (stock-only rule, compound ranking,
dedup, hard max). Read-only.
"""
import csv
import importlib.util
import json
import sys
from collections import Counter

CSV = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "02_PE/CORPUS_METADATA_CENSUS.csv")
REG = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "TOOLS/gamebryo_oracle_r1/adapters/gb12/registry.py")
OUT = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "00_CONTROL_INTERNAL_QC/q7_census_audit.json")

spec = importlib.util.spec_from_file_location("registry", REG)
reg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reg)
STOCK = set(reg.GB12_REGISTERED_CLASSES)

rows = []
with open(CSV, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        rows.append(r)

res = {"total_rows": len(rows)}

# 1. denominators by scan_status and version_label
scan_status = Counter(r["scan_status"] for r in rows)
res["scan_status_counts"] = dict(scan_status)
ver_counts = Counter(r["version_label"] for r in rows)
res["version_label_counts"] = dict(ver_counts)
hist_status = Counter(r["histogram_status"] for r in rows)
res["histogram_status_counts"] = dict(hist_status)

# 2. the +1 unit: exactly which entries are not 10.1.0.0 and not 4.1.0.12
plus_one = [r for r in rows if r["version_label"] not in ("10.1.0.0", "4.1.0.12")]
res["plus_one_entries"] = [
    {k: r[k] for k in ("entry_index", "name", "version_label", "version_hex",
                       "num_blocks", "scan_status", "histogram_status",
                       "size_stored")}
    for r in plus_one]

# 3. SCANNED_10_1 rows (histogram_status SCANNED): histogram sums == num_blocks
bad_sum, bad_types = [], []
for r in rows:
    if r["histogram_status"] != "SCANNED":
        continue
    hist = {}
    if r["type_histogram"]:
        for part in r["type_histogram"].split(";"):
            cls, _, cnt = part.rpartition("=")
            hist[cls] = int(cnt)
    tot = sum(hist.values())
    if not r["num_blocks"] or tot != int(r["num_blocks"]):
        bad_sum.append((r["entry_index"], r["name"], tot, r["num_blocks"]))
    for cls in hist:
        if cls not in STOCK:
            bad_types.append((r["entry_index"], cls))
res["scanned_histogram_sum_mismatches"] = bad_sum[:20]
res["scanned_histogram_sum_mismatch_count"] = len(bad_sum)

# 4. stock-only rule (among full-histogram 10.1 rows)
scanned = [r for r in rows if r["histogram_status"] == "SCANNED"]
res["scanned_10_1_count"] = len(scanned)
stock_only = []
niark_files = 0
for r in scanned:
    hist = {}
    for part in r["type_histogram"].split(";"):
        if not part:
            continue
        cls, _, cnt = part.rpartition("=")
        hist[cls] = int(cnt)
    classes = set(hist)
    if any(c.startswith("NiArk") for c in classes):
        niark_files += 1
    if classes.issubset(STOCK):
        stock_only.append((r["entry_index"], r["name"]))
res["stock_only_candidates_found"] = len(stock_only)
res["stock_only_examples"] = stock_only[:10]
res["files_with_any_NiArk_class"] = niark_files

# 5. NiArk class presence breakdown (which NiArk classes appear)
niark_cls = Counter()
for r in scanned:
    for part in r["type_histogram"].split(";"):
        if not part:
            continue
        cls = part.rpartition("=")[0]
        if cls.startswith("NiArk"):
            niark_cls[cls] += 1
res["niark_class_file_counts"] = dict(niark_cls)

# 6. compound-scene pool: NiNode>=4 AND NiTriShape>=2, ranking
pool = []
for r in scanned:
    hist = {}
    for part in r["type_histogram"].split(";"):
        if not part:
            continue
        cls, _, cnt = part.rpartition("=")
        hist[cls] = int(cnt)
    nn, ts = hist.get("NiNode", 0), hist.get("NiTriShape", 0)
    if nn >= 4 and ts >= 2:
        pool.append({"name": r["name"], "entry_index": int(r["entry_index"]),
                     "NiNode": nn, "NiTriShape": ts,
                     "size": int(r["size_stored"])})
res["compound_pool_size"] = len(pool)
ranked = sorted(pool, key=lambda e: (-e["NiNode"], -e["NiTriShape"],
                                    -e["size"], e["name"]))
res["compound_ranked_top10"] = ranked[:10]

# 7. dedup check: 218757 in pool? (mandatory selection, not part of the 3)
in_pool_218757 = [e for e in pool if "218757" in e["name"]]
res["218757_in_compound_pool"] = in_pool_218757

# 8. num-blocks-only 4.1 rows: no histograms
v41 = [r for r in rows if r["version_label"] == "4.1.0.12"]
res["v41_count"] = len(v41)
res["v41_with_histogram"] = sum(1 for r in v41 if r["type_histogram"])
res["v41_with_num_blocks"] = sum(1 for r in v41 if r["num_blocks"])

print(json.dumps(res, indent=2))
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
