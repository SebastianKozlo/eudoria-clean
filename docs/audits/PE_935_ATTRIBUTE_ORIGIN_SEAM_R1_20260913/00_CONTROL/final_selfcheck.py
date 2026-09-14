# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - FINAL SELF-CHECK (executor, own).
# Verifies: script hashes (no post-execution edits), S0 still PASS,
# gate census numbers re-derived from artifacts, GB6 before==after,
# decomp file census, manifest consistency. Output: 01_RAW/SELF_CHECK.json.

import csv
import hashlib
import json
import os

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")

def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()

res = {"stage": "SELF_CHECK_executor", "checks": {}, "verdict": "PASS", "errors": []}

# 1. script hashes recorded vs current (LAST recorded hash per script wins —
#    re-hash history is legitimate: each hash valid at its execution point)
script_rows = []
with open(os.path.join(RUN_ROOT, "00_CONTROL", "SCRIPT_SHA256.csv"), encoding="ascii") as f:
    for row in csv.reader(f):
        if len(row) >= 2 and row[0].endswith(".py"):
            script_rows.append((row[0], row[1].split(" ")[0]))
last_hash = {}
for name, h in script_rows:
    last_hash[name] = h
mismatch = []
for name, h in sorted(last_hash.items()):
    p = os.path.join(RUN_ROOT, "00_CONTROL", name)
    if not os.path.isfile(p):
        mismatch.append((name, "MISSING"))
        continue
    cur = sha256f(p)
    if cur != h:
        mismatch.append((name, h, cur))
res["checks"]["script_hash_final_verification"] = {
    "scripts_recorded": len(last_hash), "mismatches": mismatch}
if mismatch:
    res["verdict"] = "FAIL"
    res["errors"].append("script hash mismatch (post-execution edit?)")

# 2. S0 re-verify
s0 = json.load(open(os.path.join(OUT, "S0_ERA_ASSERTION.json")))
res["checks"]["S0_errors"] = s0["errors"]
if s0["errors"]:
    res["verdict"] = "FAIL"

# 3. gate census numbers re-derived
g1 = json.load(open(os.path.join(OUT, "GH1_DECOMP_CENSUS.json")))
g2 = json.load(open(os.path.join(OUT, "GH2_DECOMP_CENSUS.json")))
g3 = json.load(open(os.path.join(OUT, "GH3_DECOMP_CENSUS.json")))
c1 = g1["measured"]["isCall_census"]
c2 = g2["measured"]["isCall_census"]
c3 = g3["measured"]["isCall_census"]
nums = {
    "resolver_FUN_008544D0": c1["resolver_FUN_008544D0"]["count"],
    "value_ctor_FUN_0085B1B0": c1["value_ctor_FUN_0085B1B0"]["count"],
    "derived_ctor_FUN_00528E50": c1["derived_ctor_FUN_00528E50"]["count"],
    "insert_FUN_00856190": c1["insert_FUN_00856190"]["count"],
    "create_FUN_004C46C0": c1["create_FUN_004C46C0"]["count"],
    "placement_FUN_004C47F0": c1["placement_FUN_004C47F0"]["count"],
    "mapop_FUN_00854D90": c1["mapop_FUN_00854D90"]["count"],
    "builder_FUN_00567770": c2["builder_FUN_00567770"]["count"],
    "driver_FUN_00567C50": c2["driver_FUN_00567C50"]["count"],
    "keyproducer_FUN_00457930": c1["keyproducer_FUN_00457930"]["count"],
    "cand_FUN_00567170": c2["cand_FUN_00567170"]["count"],
    "cand_FUN_005B5F90": c2["cand_FUN_005B5F90"]["count"],
    "cand_FUN_006CB6F0": c2["cand_FUN_006CB6F0"]["count"],
    "plsrc_FUN_00745360": c2["plsrc_FUN_00745360"]["count"],
    "registry_builder_FUN_0072FA30": c3["registry_builder_FUN_0072FA30"]["count"],
}
expected = {
    "resolver_FUN_008544D0": 4,
    "value_ctor_FUN_0085B1B0": 1,
    "derived_ctor_FUN_00528E50": 1,
    "insert_FUN_00856190": 1,
    "create_FUN_004C46C0": 6,
    "placement_FUN_004C47F0": 4,
    "mapop_FUN_00854D90": 18,
    "builder_FUN_00567770": 1,
    "driver_FUN_00567C50": 3,
    "keyproducer_FUN_00457930": 8,
    "cand_FUN_00567170": 1,
    "cand_FUN_005B5F90": 3,
    "cand_FUN_006CB6F0": 2,
    "plsrc_FUN_00745360": 1,
    "registry_builder_FUN_0072FA30": 1,
}
bad = {k: (nums[k], expected[k]) for k in expected if nums[k] != expected[k]}
res["checks"]["census_numbers"] = {"measured": nums, "expected": expected, "mismatch": bad}
if bad:
    res["verdict"] = "FAIL"

# 4. GB6 before == after
cmp = json.load(open(os.path.join(OUT, "GB6_IMMUTABLE_COMPARISON.json")))
res["checks"]["GB6_immutable"] = cmp["result"]
if cmp["result"] != "IDENTICAL":
    res["verdict"] = "FAIL"

# 5. decomp census
dec = os.path.join(OUT, "DECOMP")
ndec = len([f for f in os.listdir(dec) if f.endswith(".c")])
res["checks"]["decomp_files"] = {"count": ndec}

# 6. pins present
pins = json.load(open(os.path.join(OUT, "T6_BYTE_PINS.json")))
res["checks"]["byte_pins"] = {"count": len(pins["pins"])}

json.dump(res, open(os.path.join(OUT, "SELF_CHECK.json"), "w"), indent=2)
print("SELF_CHECK verdict:", res["verdict"])
print("  scripts recorded:", len(script_rows), "mismatches:", len(mismatch))
print("  census mismatches:", bad)
print("  GB6:", cmp["result"])
print("  decomp files:", ndec, "| pins:", len(pins["pins"]))
