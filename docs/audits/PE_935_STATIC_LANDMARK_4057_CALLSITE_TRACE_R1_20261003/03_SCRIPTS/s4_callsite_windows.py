#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4 CALL-SITE DATAFLOW WINDOWS + IMMEDIATE CENSUS —
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

From the byte-verified Ghidra listing of FUN_00599D30 (01_RAW/G1_FUNCTION_DUMP.json;
951/951 instructions byte-identical to the physical EXE per 01_RAW/RAW_BYTE_PINS.json):
  1. extract every CALL site to FUN_008DFCD0 and FUN_008F0780 inside the function,
     each with its bounded preceding window (the this-object setup + pushed
     immediates) — the per-site dataflow skeleton (Phase 4);
  2. census of EVERY immediate pushed/stored inside the whole containing function
     (CONTROL-2 unrelated-immediate control material);
  3. locate the anchor site among them (PUSH 0xfd9 -> CALL 0x008dfcd0 @0x0059AB1E).

Interpreter: python 3.12.10 (local Windows). Invoke:
  python 03_SCRIPTS/s4_callsite_windows.py
Output: 01_RAW/CALLSITE_DATAFLOW_WINDOWS.json (UTF-8).
"""

import json
import os
import re

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
SRC = os.path.join(RAWDIR, "G1_FUNCTION_DUMP.json")
OUT = os.path.join(RAWDIR, "CALLSITE_DATAFLOW_WINDOWS.json")
ANCHOR = 0x0059AB12
CONSUMERS = {0x008DFCD0: "FUN_008dfcd0", 0x008F0780: "FUN_008f0780"}
WINDOW_BACK = 0x30  # bytes of preceding context per site (instruction-granular)


def main():
    with open(SRC, "r") as f:
        g1 = json.load(f)
    listing = g1["measured"]["function"]["listing"]
    ins = [(int(i["addr"], 16), i["bytes"], i["text"]) for i in listing]
    ins.sort()

    # ---- direct call sites to the two consumers (from flows resolved in g1 census)
    census = g1["measured"].get("callees", [])
    sites = []
    for c in census:
        for t in c.get("targets", []):
            tg = t.get("target")
            if tg is None:
                continue
            tgv = int(tg, 16)
            if tgv in CONSUMERS:
                sites.append({"call_va": int(c["call_va"], 16),
                              "call_bytes": c["bytes"], "call_text": c["text"],
                              "target": tgv, "target_name": CONSUMERS[tgv]})
    sites.sort(key=lambda s: s["call_va"])

    # ---- per-site windows: all instructions with addr in (call_va - WINDOW_BACK, call_va]
    for s in sites:
        pre = [i for i in ins if s["call_va"] - WINDOW_BACK <= i[0] <= s["call_va"]]
        s["window"] = [{"addr": "0x%08X" % a, "bytes": b, "text": t} for (a, b, t) in pre]
        # mechanical extraction of the directly-preceding PUSH imm32 and ECX setup
        push_imm = None
        for (a, b, t) in reversed(pre[:-1] if pre else []):
            m = re.match(r"PUSH 0x([0-9a-f]+)", t)
            if m:
                push_imm = int(m.group(1), 16)
                break
        ecx_src = None
        for (a, b, t) in reversed(pre[:-1] if pre else []):
            if t.startswith("LEA ECX,") or t.startswith("MOV ECX,") or t == "MOV ECX,EAX" or t.startswith("MOV ECX,"):
                ecx_src = t
                break
        s["nearest_preceding_push_imm"] = push_imm
        s["nearest_preceding_ecx_setup"] = ecx_src
        s["is_anchor_site"] = (s["call_va"] == 0x0059AB1E)

    # ---- CONTROL-2 material: census of ALL immediates in the containing function
    imm_push = []
    imm_other = []
    for (a, b, t) in ins:
        m = re.match(r"PUSH 0x([0-9a-f]+)", t)
        if m:
            imm_push.append({"addr": "0x%08X" % a, "bytes": b, "text": t,
                             "value": int(m.group(1), 16)})
            continue
        m2 = re.search(r"0x([0-9a-f]{5,8})", t)
        if m2 and ("MOV" in t and "ptr" not in t):
            # immediate moves into registers/locals (bounded heuristic, listing-derived)
            imm_other.append({"addr": "0x%08X" % a, "bytes": b, "text": t,
                              "value": int(m2.group(1), 16)})
    imm_push_values = sorted(set(x["value"] for x in imm_push))

    out = {
        "run_id": RUN_ID,
        "stage": "S4_callsite_dataflow_windows",
        "measured": {
            "function": {"entry": "0x00599D30", "body_end": "0x0059AC88",
                        "listing_count": len(ins),
                        "byte_integrity": "951/951 vs physical EXE (01_RAW/RAW_BYTE_PINS.json)"},
            "consumer_call_sites": [
                {"target": "0x%08X" % s["target"], "target_name": s["target_name"],
                 "call_va": "0x%08X" % s["call_va"], "call_bytes": s["call_bytes"],
                 "nearest_preceding_push_imm": s["nearest_preceding_push_imm"],
                 "nearest_preceding_ecx_setup": s["nearest_preceding_ecx_setup"],
                 "is_anchor_site": s["is_anchor_site"],
                 "window": s["window"]}
                for s in sites],
            "immediate_census_function_wide": {
                "push_imm32_instructions": imm_push,
                "push_imm32_unique_values": imm_push_values,
                "other_imm_moves": imm_other,
            },
        },
        "interpreted": {
            "NOTE": "nearest_preceding_push_imm/ecx_setup are mechanical extractions from the byte-verified listing (last PUSH imm32 / last ECX setup before the call); they are NOT a claim about which value is consumed — the call-site window itself is the evidence",
            "pin_provenance": {
                "call_site_windows": {
                    "MEASURED_QUANTITY": "per-call-site preceding instruction windows (this-setup + pushed immediates) for every CALL to FUN_008dfcd0 / FUN_008f0780 inside FUN_00599D30",
                    "INDEPENDENT_SOURCE_OF_TRUTH": "the byte-verified listing of FUN_00599D30 (Ghidra 11.2.1; 951/951 instructions byte-identical to the physical EXE via this run's own PE mapper)",
                    "WHY_NON_CIRCULAR": "windows are extracted from raw listing records; no decompiler prose involved; the PUSH 4057 hypothesis is only a search needle, every site is extracted identically (no cherry-picking)",
                    "FAILURE_CASE_DETECTED": "if the anchor's PUSH 0xfd9 were NOT the argument of its nearest following CALL (e.g., consumed by a different call or overwritten), the window would show it; mis-serialized listing would fail the s2 crosscheck"},
            },
        },
        "errors": [],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("S4 written:", OUT)
    print("call sites to consumers:", len(sites))
    for s in sites:
        print("  CALL %s @%s  push_imm=%s  ecx=%s%s" % (
            s["target_name"], "0x%08X" % s["call_va"],
            hex(s["nearest_preceding_push_imm"]) if s["nearest_preceding_push_imm"] is not None else None,
            s["nearest_preceding_ecx_setup"],
            "   <-- ANCHOR (PUSH 4057)" if s["is_anchor_site"] else ""))
    print("push imm32 unique values (%d):" % len(imm_push_values),
          [hex(v) for v in imm_push_values])


if __name__ == "__main__":
    main()
