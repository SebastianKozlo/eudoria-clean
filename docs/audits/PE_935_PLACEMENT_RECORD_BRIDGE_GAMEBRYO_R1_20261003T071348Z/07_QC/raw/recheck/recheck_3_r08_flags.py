#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 3 (AMEND-4/AMEND-5 truth): verify the R08 (FUN_00848EA0) decompile
branch structure in the CURRENT 01_RAW/C3_DECOMP.json with own text slicing:
- FUN_00745540(1) == TRUE branch (the else of the outer if) must contain:
  id2 property read FUN_00844660 -> lazy-init FUN_0043a550 -> lookup FUN_0072f580
  -> valid-check FUN_0072fce0 -> FUN_0072fe30 (list2->3xvec3) -> attr float
  FUN_00745690 -> lerp FUN_006c1f90 -> vec3 store to slot (FUN_007333e0 result).
- FUN_00745540(2) == TRUE branch (nested inside flag1-FALSE) must contain the
  per-slot stores u16@+0xC and float@+0x10 (and NOT the lookup/lerp chain).
Also reads Q05 (FUN_00844660) body to confirm the id2 source chain (class 20006
property tag 6) that the corrected E9(c) sentence attributes to flag-1 slots."""
import json
import os
import re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck3_r08_flags_result.json")

with open(os.path.join(PKG, "01_RAW", "C3_DECOMP.json"), encoding="utf-8-sig") as f:
    j = json.load(f)
body = j["measured"]["decompilations"]["R08_other_00848ea0"]["c"]
meta = {k: j["measured"]["decompilations"]["R08_other_00848ea0"][k]
        for k in ("function_entry", "va", "body_size", "function_name")}
res = {"r08_meta": meta}

# locate the outer flag test
m = body.find("FUN_00745540(1)")
assert m != -1
# the do-loop body: from first FUN_00745540(1) call to "while (uVar10 < 3)"
loop_start = m
loop_end = body.find("while (uVar10 < 3)")
loop = body[loop_start:loop_end]

# outer if (flag1 false -> nested flag2):
if_pos = loop.find("if (cVar1 == '\\0') {")
assert if_pos != -1, "outer if not found"
# brace-match to find the end of the flag1-FALSE block, then 'else'
depth = 0
i = if_pos + len("if (cVar1 == '\\0') {") - 1  # at '{'
start_false = i + 1
while True:
    ch = loop[i]
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            break
    i += 1
false_block = loop[start_false:i]
else_pos = loop.find("else", i)
assert else_pos != -1
# else block: from its '{' brace-matched to end of loop body
j2 = loop.find("{", else_pos)
depth = 0
i = j2
while i < len(loop):
    ch = loop[i]
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            break
    i += 1
true_block = loop[j2 + 1:i]

flag1_false = false_block          # contains the FUN_00745540(2) nested test
flag1_true = true_block            # the ELSE of the outer if

res["flag1_true_block_size"] = len(flag1_true)
res["flag1_false_block_size"] = len(flag1_false)

# in flag-1-TRUE (else of outer if): the id2/lookup/lerp chain
chain_ids = ["FUN_00844660", "FUN_0043a550", "FUN_0072f580", "FUN_0072fce0",
             "FUN_0072fe30", "FUN_00745690", "FUN_006c1f90", "FUN_007333e0",
             "_DAT_00a7b25c"]
res["flag1_true_contains"] = {fn: (fn in flag1_true) for fn in chain_ids}
res["flag1_true_vec3_store"] = ("*puVar6 = local_60" in flag1_true
                                and "puVar6[1] = local_5c" in flag1_true
                                and "puVar6[2] = local_58" in flag1_true)
# the id2/lerp chain must NOT be in the flag-2 nested path
nested = flag1_false
res["flag2_nested_present"] = ("FUN_00745540(2)" in nested)
res["flag2_nested_contains_u16_store"] = ("*(uint *)(iVar4 + 0xc) = uVar9" in nested)
res["flag2_nested_contains_float_store"] = ("*(float *)(iVar4 + 0x10) = local_68" in nested)
for fn in ("FUN_00844660", "FUN_0072f580", "FUN_0072fe30", "FUN_006c1f90"):
    res["flag2_nested_contains_%s" % fn] = (fn in nested)

# loop bounds: 3 slots
res["loop_bound_3"] = ("uVar10 < 3" in loop)
res["slot_getter"] = ("FUN_007333e0" in loop)

# verdicts
res["VERDICT_flag1_id2_lerp_path"] = all(
    res["flag1_true_contains"][fn] for fn in
    ("FUN_00844660", "FUN_0043a550", "FUN_0072f580", "FUN_0072fce0",
     "FUN_0072fe30", "FUN_00745690", "FUN_006c1f90")) and res["flag1_true_vec3_store"]
res["VERDICT_flag2_u16_float_stores"] = (res["flag2_nested_contains_u16_store"]
                                         and res["flag2_nested_contains_float_store"]
                                         and not any(
                                             res["flag2_nested_contains_%s" % fn]
                                             for fn in ("FUN_00844660", "FUN_0072f580",
                                                        "FUN_0072fe30", "FUN_006c1f90")))

# --- Q05 body (id2 source) from CURRENT C8_TOP_SOURCES.json ---
with open(os.path.join(PKG, "01_RAW", "C8_TOP_SOURCES.json"), encoding="utf-8-sig") as f:
    c8 = json.load(f)
q5 = c8["measured"]["decompilations"]["Q05_attr_id2_00844660"]
res["q05_body"] = q5["c"]
res["q05_has_class_20006"] = ("0x4e26" in q5["c"].lower())
res["q05_tag6_chain"] = ("FUN_007376a0" in q5["c"].lower() and "FUN_0070c180" in q5["c"].lower())

# --- W03/W04 lerp+gate presence (corrected sentence cites them) ---
with open(os.path.join(PKG, "01_RAW", "C4_CONSTRUCTION_TRACE.json"), encoding="utf-8-sig") as f:
    c4 = json.load(f)
w03 = c4["measured"]["decompilations"]["W03_pos_compute_006c1f90"]["c"]
res["w03_lerp_shape"] = ("b[i] - a[i]" in w03.replace(" ", "")) or ("b[i]-a[i]" in w03.replace(" ", ""))
w04 = c4["measured"]["decompilations"]["W04_template_out_0072fe30"]["c"]
res["w04_gate_0x24"] = ("0x24" in w04)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "q05_body"}, indent=1))
