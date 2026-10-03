#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 1 (AMEND-1/AMEND-2 truth): independent recount of census-target caller
enumerations from the CURRENT 01_RAW JSONs, plus consistency vs the QC-round-1
pre-repair dump (07_QC/raw/CENSUS_TARGETS_DUMP.txt / C2_TARGETS_DUMP.txt).
No executor code reused; own parsing only."""
import json
import os
import re
import sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RAW = os.path.join(PKG, "01_RAW")
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck1_census_result.json")

res = {}

def load(name):
    with open(os.path.join(RAW, name), encoding="utf-8-sig") as f:
        return json.load(f)

# --- own counts from CURRENT raw JSONs ---
c2 = load("C2_CALLER_CENSUS.json")
targets = c2["measured"]["targets"]
if isinstance(targets, dict):
    c2_keys = sorted(targets.keys())
    c2_n = len(c2_keys)
else:
    c2_keys = [t.get("label", "?") for t in targets]
    c2_n = len(c2_keys)
res["c2_target_count"] = c2_n
res["c2_census_denominator_field"] = c2["measured"].get("census_denominator")
res["c2_target_keys"] = c2_keys

counts = {}
for name in ("C4_CONSTRUCTION_TRACE", "C5_LAYOUT_AND_DRIVERS",
             "C6_DRIVER_SOURCES", "C8_TOP_SOURCES"):
    j = load(name + ".json")
    census = j["measured"]["census"]
    keys = sorted(census.keys())
    counts[name] = {"n": len(keys), "keys": keys}
res["censuses"] = counts

total = c2_n + sum(v["n"] for v in counts.values())
res["TOTAL_census_target_enumerations"] = total
res["expected_45"] = (total == 45)
res["breakdown"] = "C2=%d + C4=%d + C5=%d + C6=%d + C8=%d" % (
    c2_n, counts["C4_CONSTRUCTION_TRACE"]["n"],
    counts["C5_LAYOUT_AND_DRIVERS"]["n"], counts["C6_DRIVER_SOURCES"]["n"],
    counts["C8_TOP_SOURCES"]["n"])

# --- negative control: the OLD wrong breakdown "19+10+8+4+4+8+4+12" must not
#     reconstruct from any countable structure (per-target decomp lists differ) ---
# decompilations in C4/C5/C6/C8 and C2/C3 for comparison (these are NOT census)
dec = {}
for name in ("C2_CALLER_CENSUS", "C3_DECOMP", "C4_CONSTRUCTION_TRACE",
             "C5_LAYOUT_AND_DRIVERS", "C6_DRIVER_SOURCES", "C7_LISTS_AND_ATTACH",
             "C8_TOP_SOURCES", "C11_ORACLE_COUNTERPARTS"):
    try:
        j = load(name + ".json")
        d = j["measured"].get("decompilations")
        dec[name] = sorted(d.keys()) if isinstance(d, dict) else "LIST:%d" % len(d)
    except Exception as e:
        dec[name] = "ERR:%s" % e
res["decompilation_key_counts"] = {k: (len(v) if isinstance(v, list) else len(v))
                                   for k, v in dec.items() if isinstance(v, (list, dict))}

# --- consistency vs QC-round-1 pre-repair dump (CENSUS_TARGETS_DUMP.txt) ---
dump_path = os.path.join(PKG, "07_QC", "raw", "CENSUS_TARGETS_DUMP.txt")
qc_census = {}
with open(dump_path, encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(\w+\.json) :: (\w+) :: (.*) :: callers=(.*)", line.strip())
        if m:
            qc_census.setdefault(m.group(1), {})[m.group(2)] = {"meta": m.group(3), "callers": m.group(4)}
res["qc_round1_dump_census_counts"] = {k: len(v) for k, v in qc_census.items()}

# compare current census meta vs QC dump meta (key fields)
mismatches = []
for name, entries in qc_census.items():
    j = load(name)
    census = j["measured"]["census"]
    for label, qcdata in entries.items():
        if label not in census:
            mismatches.append("MISSING in current %s: %s" % (name, label))
            continue
        cur = census[label]
        # compare load-bearing fields
        for field in ("callsites", "unique_callers", "function_entry"):
            qv = re.search(r"'%s': ([0-9]+)" % field, qcdata["meta"])
            if qv and int(qv.group(1)) != int(cur[field]):
                mismatches.append("%s/%s %s: qc=%s cur=%s" % (name, label, field, qv.group(1), cur[field]))
        qcallers = re.findall(r"0x([0-9A-Fa-f]{8})\((\d+) sites\)", qcdata["callers"])
        cur_callers = cur.get("callers")
        if isinstance(cur_callers, dict):
            cur_pairs = sorted((k.upper(), v.get("callsite_count", len(v.get("callsites", []))))
                               for k, v in cur_callers.items())
        elif isinstance(cur_callers, list):
            cur_pairs = sorted((str(c.get("caller_entry", "")).upper(),
                                c.get("callsite_count", len(c.get("callsites", []))))
                               for c in cur_callers)
        else:
            cur_pairs = None
        qc_pairs = sorted((("0x" + a).upper(), int(b)) for a, b in qcallers)
        if cur_pairs is not None and qc_pairs != cur_pairs:
            mismatches.append("%s/%s caller_list differs: qc=%r cur=%r" % (name, label, qc_pairs, cur_pairs))
res["census_vs_qc_round1_dump_mismatches"] = mismatches

# --- C2 targets vs QC-round-1 pre-repair dump (C2_TARGETS_DUMP.txt meta fields) ---
c2dump = os.path.join(PKG, "07_QC", "raw", "C2_TARGETS_DUMP.txt")
c2_qc = {}
with open(c2dump, encoding="utf-8") as f:
    txt = f.read()
for m in re.finditer(r"^(\w+) :: meta=\{(.+?)\}", txt, re.M):
    label, meta = m.group(1), m.group(2)
    c2_qc[label] = dict(re.findall(r"'(\w+)': '([^']*)'", meta))
c2_mism = []
cur_targets = c2["measured"]["targets"]
cur_t = cur_targets if isinstance(cur_targets, dict) else {t.get("label"): t for t in cur_targets}
for label, qcmeta in c2_qc.items():
    if label not in cur_t:
        c2_mism.append("MISSING in current C2: %s" % label)
        continue
    cur = cur_t[label]
    for field in ("callsites", "unique_callers", "function_entry"):
        if field in qcmeta and qcmeta[field] != str(cur.get(field)):
            c2_mism.append("C2/%s %s qc=%s cur=%s" % (label, field, qcmeta[field], cur.get(field)))
res["c2_vs_qc_round1_dump_label_count"] = len(c2_qc)
res["c2_vs_qc_round1_dump_mismatches"] = c2_mism

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("c2_target_keys", "censuses", "decompilation_key_counts")}, indent=1))
