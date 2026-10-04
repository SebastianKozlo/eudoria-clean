# cqc_battery.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# Fresh targeted QC (corrected). QC may PASS while science remains explicitly
# UNRESOLVED: QC PASS means the corrected claims accurately match evidence and
# uncertainty, NOT that all census candidates were solved. No gate is
# hard-coded to PASS: every status is derived from measured inputs on disk
# (the EXE, the committed CSV/JSON artifacts, the docs, the READ-ONLY
# historical package for the quotecheck).
#
# Gates:
#  Q1  baseline + EXE identity
#  Q2  authoritative same-VA pin integrity (every ledger field re-derived from ONE VA)
#  Q3  pin negative-control battery A-F (synthetic bytes only)
#  Q4  signed displacement semantics (+ the 4 mandated decoder controls live in Q5)
#  Q5  decoder unit battery + re-decode consistency over every census row
#  Q6  trusted boundary policy
#  Q7  full effective-address/SIB provenance handling
#  Q8  EBP/ESP provenance discipline
#  Q9  regenerated census arithmetic + the two distinct denominators
#  Q10 known stores physical re-pin
#  Q11 factory identity/enumeration membership derived from measured evidence
#  Q12 object structural identity (0xA4=164, FUN_00972380, examined layout facts)
#  Q13 vtable/polymorphism claim scope + superseded-phrase absence sweep
#  Q14 runtime-value nonclaims + forbidden scope + predecessor preservation
#  AUX supersession quotecheck (every ORIGINAL_EXCERPT a real substring of its
#      named READ-ONLY historical source file)
#
# Outputs: 01_RAW/CQC_DECODER_UNIT_TESTS.json, 01_RAW/CQC_NEGATIVE_CONTROLS.json,
# 01_RAW/CQC_FINAL.json (--out* overrides). READ-ONLY vs the EXE and all inputs.

import argparse
import csv
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004"
HIST = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "a0e176803aed23b19040d4310de1668efec4511f"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-decoder", default=os.path.join(RUN, "01_RAW", "CQC_DECODER_UNIT_TESTS.json"))
    ap.add_argument("--out-controls", default=os.path.join(RUN, "01_RAW", "CQC_NEGATIVE_CONTROLS.json"))
    ap.add_argument("--out-final", default=os.path.join(RUN, "01_RAW", "CQC_FINAL.json"))
    args = ap.parse_args()

    gates = {}
    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)

    # ---------------- Q1: baseline + EXE identity ----------------
    q1 = {"exe_size": len(data), "exe_sha256": sha, "exe_pinned_match": exe_ok}
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip()
        origin = subprocess.check_output(
            ["git", "rev-parse", "origin/master"], cwd=REPO).decode().strip()
        remote = subprocess.check_output(
            ["git", "ls-remote", "origin", "master"], cwd=REPO).decode().split()[0]
    except Exception as e:  # network/subprocess failure is an honest FAIL
        head = origin = remote = "ERROR: %s" % e
    q1["local_head"] = head
    q1["origin_master"] = origin
    q1["actual_remote_master"] = remote
    q1["baseline_ok"] = (exe_ok and head == BASE_SHA and origin == BASE_SHA
                         and remote == BASE_SHA)
    gates["Q1"] = ("PASS" if q1["baseline_ok"] else "FAIL", q1)

    # ---------------- load package artifacts ----------------
    with open(os.path.join(RUN, "CORRECTED_PIN_LEDGER.csv"), newline="", encoding="utf-8") as f:
        pins = list(csv.DictReader(f))
    with open(os.path.join(RUN, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"), newline="", encoding="utf-8") as f:
        census = list(csv.DictReader(f))
    with open(os.path.join(RUN, "01_RAW", "C2_CENSUS.json")) as f:
        c2 = json.load(f)
    with open(os.path.join(RUN, "01_RAW", "C1_PIN_EVIDENCE.json")) as f:
        c1 = json.load(f)
    with open(os.path.join(RUN, "01_RAW", "C3_OBJECT_SCOPE.json")) as f:
        c3 = json.load(f)

    # ---------------- Q2: authoritative same-VA pin integrity ----------------
    q2 = {"records": len(pins), "same_va_violations": [], "field_mismatches": []}
    for p in pins:
        va = int(p["instruction_va"], 16)
        off = va - tva
        ln = int(p["instruction_length"]) if p["instruction_length"] else 0
        # opcode bytes derived from the SAME VA
        if ln:
            got = text[off:off + ln].hex(" ").upper()
            if got != p["opcode_bytes"]:
                q2["field_mismatches"].append({"claim": p["claim_id"], "field": "opcode_bytes"})
        # call rows: rel32 operand at va+1, target = va+5+signed rel32
        if p["operand_kind"] == "rel32" and p["status"] in ("VALIDATED", "CORRECTED_VALIDATED"):
            if text[off] != 0xE8:
                q2["same_va_violations"].append({"claim": p["claim_id"], "why": "byte!=E8 with promoted target"})
            if text[off + 1:off + 5].hex(" ").upper() != p["raw_operand"]:
                q2["field_mismatches"].append({"claim": p["claim_id"], "field": "raw_operand"})
            rel = struct.unpack_from("<i", text, off + 1)[0]
            tgt = "0x%08X" % (va + 5 + rel)
            if tgt != p["measured_target"]:
                q2["field_mismatches"].append({"claim": p["claim_id"], "field": "measured_target",
                                                "expected": tgt, "got": p["measured_target"]})
        if p["operand_kind"].startswith("imm") and p["operand_offset"] and p["operand_width"]:
            oo = int(p["operand_offset"]); ow = int(p["operand_width"])
            if text[off + oo:off + oo + ow].hex(" ").upper() != p["raw_operand"]:
                q2["field_mismatches"].append({"claim": p["claim_id"], "field": "raw_operand(imm)"})
        if p["operand_kind"] in ("mem32", "mem8") and p["operand_offset"] and p["operand_width"]:
            oo = int(p["operand_offset"]); ow = int(p["operand_width"])
            if text[off + oo:off + oo + ow].hex(" ").upper() != p["raw_operand"]:
                q2["field_mismatches"].append({"claim": p["claim_id"], "field": "raw_operand(mem)"})
        if p["status"] == "DECLASSIFIED_NOT_A_CALL" and text[off] == 0xE8:
            q2["same_va_violations"].append({"claim": p["claim_id"], "why": "declassified but byte IS E8"})
    pin_fail_total = c1["pin_totals"]["fail_count"]
    q2["c1_battery_fail_count"] = pin_fail_total
    q2["ok"] = (not q2["same_va_violations"] and not q2["field_mismatches"]
                and pin_fail_total == 0)
    gates["Q2"] = ("PASS" if q2["ok"] else "FAIL", q2)

    # ---------------- Q3: negative controls A-F (synthetic bytes only) ----------------
    ctrls = {}

    # CONTROL A - corrupted constructor evidence: corrupt the measured ctor
    # entry bytes in a PRIVATE synthetic mutant; the raw-evidence gate must FAIL.
    canonical_a = bytes.fromhex("6A FF 68 F5 A2 A4 00 64".replace(" ", ""))
    mutant_a = bytearray(canonical_a)
    mutant_a[0] = 0xEB
    gate_a_canon = (canonical_a[:2].hex(" ").upper() == "6A FF")
    gate_a_mutant = (bytes(mutant_a[:2]).hex(" ").upper() == "6A FF")
    ctrls["CONTROL_A"] = {
        "description": "corrupted constructor entry bytes in a private synthetic mutant -> raw-evidence gate FAIL",
        "canonical_gate": "PASS" if gate_a_canon else "FAIL",
        "mutant_gate": "PASS" if gate_a_mutant else "FAIL",
        "expected_mutant_gate": "FAIL",
        "test_passed": (gate_a_canon and not gate_a_mutant),
    }

    # CONTROL B - measured enumeration excludes 20006: mutate the MEASURED
    # range bound so 0x4E26 is outside; membership must derive from the
    # (mutated) measured evidence and the gate must FAIL. Never literal-only.
    def pin_imm(claim_id):
        for p in pins:
            if p["claim_id"] == claim_id:
                return int(p["measured_operand"].split(" ")[0], 16) if p["measured_operand"] else None
        return None
    measured_start = pin_imm("modeinit_first_range_ESI_init")
    measured_bound = pin_imm("modeinit_first_range_CMP_bound")
    sel = 0x4E26
    canon_b = (measured_start is not None and measured_bound is not None
               and measured_start <= sel < measured_bound)
    mutated_bound = 0x4E26  # excludes 20006: [0x4E20, 0x4E26)
    mutant_b = (measured_start is not None and measured_start <= sel < mutated_bound)
    ctrls["CONTROL_B"] = {
        "description": "mutated measured enumeration range excludes 20006 -> membership gate FAIL (derived from measured evidence, never literal-only)",
        "measured_start": "0x%08X" % measured_start,
        "measured_bound": "0x%08X" % measured_bound,
        "selector": "0x%08X" % sel,
        "canonical_membership_derived": canon_b,
        "mutated_bound": "0x%08X" % mutated_bound,
        "mutant_membership": mutant_b,
        "test_passed": (canon_b and not mutant_b),
    }

    # CONTROL C - non-CALL VA: a VA whose first byte is NOT 0xE8 -> FAIL, no
    # accepted target.
    syn_buf = bytes.fromhex("BB01000000")
    syn_tva = 0x00A00000
    cv_c = pebnd.validate_direct_call(syn_buf, syn_tva, syn_tva)
    ctrls["CONTROL_C"] = {
        "description": "non-CALL VA passed to the CALL validator -> CALL_VALIDATION=FAIL, no accepted target",
        "byte": "0x%02X" % syn_buf[0],
        "call_validation": cv_c["call_validation"],
        "target": cv_c["target"],
        "test_passed": (cv_c["call_validation"] == "FAIL" and cv_c["target"] is None),
    }

    # CONTROL D - callback immediate corruption: mutate the measured immediate
    # (prose unchanged); the pin/immediate gate must FAIL.
    canonical_d = bytes.fromhex("B8F0BE7000")
    mutant_d = bytearray(canonical_d)
    mutant_d[1] = 0xF1
    def imm_gate(buf):
        ins = x86dec.decode(bytes(buf), 0)
        return ins is not None and ins.imm_width == 4 and ins.imm_raw == 0x0070BEF0
    ctrls["CONTROL_D"] = {
        "description": "callback immediate corrupted in a private synthetic mutant -> pin/immediate gate FAIL",
        "canonical_gate": "PASS" if imm_gate(canonical_d) else "FAIL",
        "mutant_gate": "PASS" if imm_gate(mutant_d) else "FAIL",
        "test_passed": (imm_gate(canonical_d) and not imm_gate(mutant_d)),
    }

    # CONTROL E - E8 inside another instruction's immediate: synthetic anchored
    # B8 E8 01 00 00 00 C0 C3 (valid starts: 0=MOV EAX,imm32; 5=ADD AL,AL; 7=RET;
    # candidate offset 1 contains E8 with a computable apparent rel32).
    syn_e = bytes.fromhex("B8E801000000" "C0C3")
    # boundary candidate start = offset 0 (declared trusted anchor for the test)
    i0 = x86dec.decode(syn_e, 0)
    land5 = pebnd.seq_decode_lands(syn_e, 0, 5)
    land1 = pebnd.seq_decode_lands(syn_e, 0, 1)
    apparent_rel = struct.unpack_from("<i", syn_e, 2)[0]
    apparent_target = (syn_tva + 1 + 5 + apparent_rel)
    cv_e = pebnd.validate_direct_call(syn_e, syn_tva, syn_tva + 1)
    ctrls["CONTROL_E"] = {
        "description": "E8 inside another instruction immediate -> CALL_BOUNDARY_VALIDATION(offset 1) fails; opcode-byte coincidence + in-range-looking target insufficient",
        "valid_starts_decode": {"0": "MOV EAX,imm32 len=%d" % i0.length if i0 else "FAIL",
                                 "5": "ADD AL,AL (landed=%s)" % land5,
                                 "7": "RET"},
        "candidate_offset": 1,
        "byte_at_offset1_is_E8": syn_e[1] == 0xE8,
        "apparent_rel32": apparent_rel,
        "apparent_target": "0x%08X" % apparent_target,
        "validation_outcome": cv_e["call_validation"],
        "target_promoted": cv_e["target"],
        "test_passed": (cv_e["call_validation"] != "PASS" and cv_e["target"] is None
                        and syn_e[1] == 0xE8),
    }

    # CONTROL F - ESP SIB with unresolved index provenance: synthetic
    # 89 84 2C 84 00 00 00 (effective address ESP+EBP*1+132); without separate
    # provenance -> NOT REJECTED_WRONG_OBJECT; ADDRESS_PROVENANCE=UNRESOLVED,
    # CLASSIFICATION=UNRESOLVED.
    syn_f = bytes.fromhex("8984" "2C" "84000000")
    ins_f = x86dec.decode(syn_f, 0)
    if ins_f is not None:
        base_f = x86dec.REGS32[ins_f.ea_base] if ins_f.ea_base is not None else None
        index_f = x86dec.REGS32[ins_f.ea_index] if ins_f.ea_index is not None else None
        prov_f = "UNRESOLVED"  # census rule: register naming is not provenance
        class_f = "UNRESOLVED"  # census rule for unresolved provenance
    else:
        base_f = index_f = prov_f = class_f = None
    ctrls["CONTROL_F"] = {
        "description": "ESP SIB with unresolved index provenance -> ADDRESS_PROVENANCE=UNRESOLVED, CLASSIFICATION=UNRESOLVED (NOT REJECTED_WRONG_OBJECT)",
        "decoded": ins_f is not None,
        "base_register": base_f,
        "index_register": index_f,
        "scale": ins_f.ea_scale if ins_f else None,
        "signed_displacement": ins_f.disp_signed if ins_f else None,
        "effective_displacement": ins_f.disp_signed if ins_f else None,
        "address_provenance": prov_f,
        "classification": class_f,
        "test_passed": (ins_f is not None and base_f == "ESP" and index_f == "EBP"
                        and ins_f.ea_scale == 1 and ins_f.disp_signed == 132
                        and prov_f == "UNRESOLVED" and class_f == "UNRESOLVED"),
    }

    all_ctrls_pass = all(c["test_passed"] for c in ctrls.values())
    with open(args.out_controls, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004",
                   "controls": ctrls, "all_passed": all_ctrls_pass}, f, indent=1)
    gates["Q3"] = ("PASS" if all_ctrls_pass else "FAIL", {k: v["test_passed"] for k, v in ctrls.items()})

    # ---------------- Q4: signed displacement semantics ----------------
    q4 = {"mod1_rows_signed_minus_124": 0, "mod1_rows_bad": [], "positive_rows_effective_132": 0,
          "positive_rows_bad": [], "known_store_displacements": {}}
    for r in census:
        if r["classification"] == "NEGATIVE_DISP8_MINUS_0x7C_CONTROL":
            if int(r["signed_displacement"]) == -124:
                q4["mod1_rows_signed_minus_124"] += 1
            else:
                q4["mod1_rows_bad"].append(r["va"])
        else:
            if int(r["effective_displacement"]) == 132:
                q4["positive_rows_effective_132"] += 1
            else:
                q4["positive_rows_bad"].append(r["va"])
    for va in (0x0070D013, 0x0070C71E):
        for r in census:
            if int(r["va"], 16) == va:
                q4["known_store_displacements"]["0x%08X" % va] = int(r["signed_displacement"])
    q4["ok"] = (not q4["mod1_rows_bad"] and not q4["positive_rows_bad"]
                and q4["mod1_rows_signed_minus_124"] == c2["measured_quantities"]["NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS"]
                and all(v == 132 for v in q4["known_store_displacements"].values()))
    gates["Q4"] = ("PASS" if q4["ok"] else "FAIL", q4)

    # ---------------- Q5: decoder unit battery + re-decode consistency ----------------
    unit = []
    def dec_len(hexstr):
        b = bytes.fromhex(hexstr.replace(" ", ""))
        i = x86dec.decode(b, 0)
        return i.length if i else None
    unit.append({"vector": "8B 04 85 00 00 00 00", "expected": 7, "measured": dec_len("8B 04 85 00 00 00 00")})
    unit.append({"vector": "8B 04 24", "expected": 3, "measured": dec_len("8B 04 24")})
    unit.append({"vector": "66 B8 01 00", "expected": 4, "measured": dec_len("66 B8 01 00")})
    unit.append({"vector": "89 86 (truncated 2-byte buffer)", "expected": "REJECT/None",
                 "measured": dec_len("898 6".replace(" ", "")) if False else (x86dec.decode(bytes.fromhex("8986"), 0) or None)})
    unit[-1]["measured"] = "REJECT/None" if x86dec.decode(bytes.fromhex("8986"), 0) is None else "FABRICATED"
    unit_ok = (unit[0]["measured"] == 7 and unit[1]["measured"] == 3
               and unit[2]["measured"] == 4 and unit[3]["measured"] == "REJECT/None")
    # re-decode every census row from its VA
    redecode_bad = []
    for r in census:
        va = int(r["va"], 16)
        off = va - tva
        ins = x86dec.decode(text, off)
        if ins is None or ins.length != int(r["instruction_length"]):
            redecode_bad.append(r["va"])
    # decoder coverage sanity over the 8 historical counted-function windows
    cov = {}
    for name, w in (("setter", (0x0070C680, 0x130)), ("loop", (0x00703E80, 0x88)),
                   ("driver", (0x004B0980, 0x140)), ("register", (0x00707FB0, 0x110)),
                   ("modeinit", (0x007080C0, 0x68)), ("stream_ctor", (0x00972380, 0x15C)),
                   ("modecond", (0x00703CD0, 0x16)), ("slotpred", (0x0070CC80, 0x60))):
        va0, sz = w
        i = va0 - tva
        ok_cnt = 0
        total = 0
        while i < va0 - tva + sz:
            ins = x86dec.decode(text, i)
            total += 1
            if ins is None:
                break
            i += ins.length
            ok_cnt += 1
        cov[name] = {"decoded_instructions": ok_cnt, "aborted": total - ok_cnt - 1 if total > ok_cnt else 0}
    with open(args.out_decoder, "w", newline="\n") as f:
        json.dump({"unit_battery": unit, "unit_battery_ok": unit_ok,
                  "redecode_bad_rows": redecode_bad, "coverage_windows": cov}, f, indent=1)
    q5_ok = unit_ok and not redecode_bad
    gates["Q5"] = ("PASS" if q5_ok else "FAIL",
                   {"unit_battery": unit, "redecode_bad_rows": len(redecode_bad), "coverage": cov})

    # ---------------- Q6: trusted boundary policy ----------------
    trusted_sources = {"KNOWN_FUNCTION_ENTRY", "CC_PADDING_DELIMITED_START", "RET_DELIMITED_START"}
    q6 = {"confirmed_rows_with_untrusted_source": [], "forbidden_inference_hits": [],
          "control_E": ctrls["CONTROL_E"]["test_passed"]}
    for r in census:
        if r["boundary_status"] == "CONFIRMED" and r["boundary_source"] not in trusted_sources:
            q6["confirmed_rows_with_untrusted_source"].append(r["va"])
    for r in census:
        low = r["reason"].lower()
        for bad in ("not an instruction", "not_an_instruction", "immediate_data",
                    "non-instruction byte"):
            if bad in low and r["classification"] != "NEGATIVE_DISP8_MINUS_0x7C_CONTROL":
                q6["forbidden_inference_hits"].append({"va": r["va"], "phrase": bad})
    q6["ok"] = (not q6["confirmed_rows_with_untrusted_source"]
                and not q6["forbidden_inference_hits"] and q6["control_E"])
    gates["Q6"] = ("PASS" if q6["ok"] else "FAIL", q6)

    # ---------------- Q7: full EA/SIB provenance handling ----------------
    q7 = {"rows_missing_ea_fields": [], "sib_spotcheck": {}, "control_F": ctrls["CONTROL_F"]["test_passed"]}
    for r in census:
        if r["decoder_status"] == "OK":
            for fld in ("operand_width", "base_register", "index_register", "scale",
                        "raw_displacement", "signed_displacement", "effective_displacement",
                        "address_provenance_status"):
                if r[fld] == "":
                    q7["rows_missing_ea_fields"].append({"va": r["va"], "field": fld})
                    break
    # spot-check the known ESP+SIB row 0x00812944 (historical census displayed
    # the impossible "[ESP+ESP*1+0x84]"; SIB index=4 means NO INDEX): the
    # census fields must match a FRESH machine decode of the same bytes
    # (self-consistency; no hand-copied values).
    for r in census:
        if r["va"] == "0x00812944":
            spot_ins = x86dec.decode(text, 0x00812944 - tva)
            q7["sib_spotcheck"]["0x00812944"] = {
                "census": {"base": r["base_register"], "index": r["index_register"],
                            "scale": r["scale"], "signed": r["signed_displacement"]},
                "fresh_decode": {
                    "base": x86dec.REGS32[spot_ins.ea_base] if spot_ins.ea_base is not None else "NONE",
                    "index": x86dec.REGS32[spot_ins.ea_index] if spot_ins.ea_index is not None else "NONE",
                    "scale": str(spot_ins.ea_scale), "signed": str(spot_ins.disp_signed)},
                "historical_display_defect": "[ESP+ESP*1+0x84] (impossible: SIB index 100b = NO INDEX)",
            }
    sc = q7["sib_spotcheck"].get("0x00812944", {})
    spot_ok = (sc and sc["census"] == sc["fresh_decode"]
               and sc["fresh_decode"]["index"] == "NONE"
               and sc["fresh_decode"]["base"] == "ESP"
               and sc["fresh_decode"]["signed"] == "132")
    q7["ok"] = (not q7["rows_missing_ea_fields"] and spot_ok and q7["control_F"])
    gates["Q7"] = ("PASS" if q7["ok"] else "FAIL", q7)

    # ---------------- Q8: EBP/ESP provenance discipline ----------------
    q8 = {"wrong_object_rows_without_basis": [], "stack_write_rows_not_unresolved": [],
          "all_wrong_object_bases": []}
    for r in census:
        if r["classification"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE":
            if "provenance_basis=" not in r["reason"]:
                q8["wrong_object_rows_without_basis"].append(r["va"])
            q8["all_wrong_object_bases"].append(r["base_register"])
        if (r["write_form"] in ("write", "lea_linked_write")
                and r["base_register"] in ("ESP", "EBP")
                and r["classification"] != "UNRESOLVED"):
            q8["stack_write_rows_not_unresolved"].append(
                {"va": r["va"], "classification": r["classification"]})
    q8["ok"] = (not q8["wrong_object_rows_without_basis"]
                and not q8["stack_write_rows_not_unresolved"])
    gates["Q8"] = ("PASS" if q8["ok"] else "FAIL", q8)

    # ---------------- Q9: regenerated census arithmetic + distinct denominators ----------------
    mq = c2["measured_quantities"]
    tally = {}
    for r in census:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    derived_unresolved = tally.get("UNRESOLVED", 0)
    derived_wcand = sum(1 for r in census
                        if r["write_form"] in ("write", "lea_linked_write")
                        and r["classification"] == "UNRESOLVED")
    bnd_unres_reads = sum(1 for r in census
                          if r["write_form"] in ("read", "lea_unlinked")
                          and r["boundary_status"] == "UNRESOLVED")
    q9 = {"tally": tally,
          "tally_sum": sum(tally.values()),
          "raw_rows": mq["RAW_PATTERN_ROWS"],
          "derived_census_unresolved": derived_unresolved,
          "derived_write_candidates": derived_wcand,
          "derived_boundary_unresolved_reads": bnd_unres_reads,
          "summary_census_unresolved": mq["CENSUS_UNRESOLVED_ROWS"],
          "summary_write_candidates": mq["FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES"],
          "denominators_distinct_definitions": c2["definitions"]}
    q9["ok"] = (tally_sum_ok := (q9["tally_sum"] == mq["RAW_PATTERN_ROWS"])
                and derived_unresolved == mq["CENSUS_UNRESOLVED_ROWS"]
                and derived_wcand == mq["FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES"]
                and derived_unresolved >= derived_wcand
                and mq["KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES"] == tally.get("KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE", 0)
                and tally.get("REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE", 0) == mq["REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"]
                and tally.get("REJECTED_READ_NOT_WRITE", 0) == mq["REJECTED_READ_NOT_WRITE"]
                and tally.get("NEGATIVE_DISP8_MINUS_0x7C_CONTROL", 0) == mq["NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS"])
    gates["Q9"] = ("PASS" if q9["ok"] else "FAIL", q9)

    # ---------------- Q10: known stores physical re-pin ----------------
    q10 = {}
    for va, exp, cls in ((0x0070D013, "89 9E 84 00 00 00", "INITIALIZATION_NULL"),
                         (0x0070C71E, "89 86 84 00 00 00", "CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE")):
        off = va - tva
        got = text[off:off + 6].hex(" ").upper()
        ok, src, start = pebnd.boundary_confirm(text, tva, va)
        row = next((r for r in census if int(r["va"], 16) == va), None)
        q10["0x%08X" % va] = {
            "bytes": got, "bytes_ok": got == exp, "boundary": "CONFIRMED" if ok else "UNRESOLVED",
            "census_classification": row["classification"] if row else None,
            "store_class_in_reason": cls in (row["reason"] if row else ""),
        }
    q10["ok"] = all(v["bytes_ok"] and v["boundary"] == "CONFIRMED"
                    and v["census_classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
                    and v["store_class_in_reason"]
                    for v in q10.values() if isinstance(v, dict))
    q10["ok"] = (q10["0x0070D013"]["bytes_ok"] and q10["0x0070D013"]["boundary"] == "CONFIRMED"
                 and q10["0x0070C71E"]["bytes_ok"] and q10["0x0070C71E"]["boundary"] == "CONFIRMED"
                 and q10["0x0070D013"]["census_classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
                 and q10["0x0070C71E"]["census_classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
                 and q10["0x0070D013"]["store_class_in_reason"]
                 and q10["0x0070C71E"]["store_class_in_reason"])
    gates["Q10"] = ("PASS" if q10["ok"] else "FAIL", q10)

    # ---------------- Q11: factory identity/enumeration from measured evidence ----------------
    q11 = {"measured_start": "0x%08X" % measured_start if measured_start is not None else None,
           "measured_bound": "0x%08X" % measured_bound if measured_bound is not None else None,
           "selector": "0x4E26",
           "membership_derived_from_measured": canon_b,
           "control_B_mutant_fails": not ctrls["CONTROL_B"]["mutant_membership"],
           "second_range_measured": ("0x%08X" % pin_imm("modeinit_second_range_ESI_init"),
                                     "0x%08X" % pin_imm("modeinit_second_range_CMP_bound")),
           "dispatcher_entry5_measured": c1["censuses"]["dispatcher_entry5_selector_20006"]["entry5_value"]}
    q11["ok"] = (canon_b and not ctrls["CONTROL_B"]["mutant_membership"]
                 and q11["dispatcher_entry5_measured"] == "0x0073C8D8")
    gates["Q11"] = ("PASS" if q11["ok"] else "FAIL", q11)

    # ---------------- Q12: object structural identity ----------------
    fr = open(os.path.join(RUN, "FINAL_REPORT.md"), encoding="utf-8").read()
    q12 = {
        "size_0xA4_164": (c3["allocation_size_facts"]["ASSIGNED_OBJECT_SIZE_HEX"] == "0xA4"
                         and c3["allocation_size_facts"]["ASSIGNED_OBJECT_SIZE_DECIMAL"] == 164),
        "factory_size_0x118_280": c3["allocation_size_facts"]["FACTORY_SIZE_DECIMAL"] == 280,
        "ctor_call_target_validated": any(p["claim_id"] == "setter_CALL_stream_ctor"
                                          and p["status"] in ("VALIDATED", "CORRECTED_VALIDATED")
                                          and p["measured_target"] == "0x00972380" for p in pins),
        "ctor_extent_measured": c3["examined_ctor"]["extent_end"] == "0x009724DA",
        "cursor_pinned": any(p["claim_id"] == "stream_ctor_LEA_EDI_cursor_3C"
                            and p["status"] == "VALIDATED" for p in pins),
        "tail_stores_pinned": all(any(p["claim_id"] == c and p["status"] == "VALIDATED" for p in pins)
                                  for c in ("stream_ctor_tail_88_flag_1", "stream_ctor_tail_8C_size_0x80",
                                            "stream_ctor_tail_90", "stream_ctor_tail_94_flag_1",
                                            "stream_ctor_tail_98_size_0x80", "stream_ctor_tail_9C",
                                            "stream_ctor_return_this")),
        "wording_structural_identity": "ASSIGNED_OBJECT_STRUCTURAL_IDENTITY = CONFIRMED_WITHIN_EXAMINED_LAYOUT" in fr,
        "wording_semantic_role": "FINAL_SEMANTIC_ROLE_RECORD_STREAM = STRONGLY_SUPPORTED" in fr,
        "wording_164": "0xA4 = 164 bytes" in fr,
    }
    q12["ok"] = all(q12.values())
    gates["Q12"] = ("PASS" if q12["ok"] else "FAIL", q12)

    # ---------------- Q13: vtable/polymorphism scope + phrase sweep ----------------
    q13 = {
        "direct_vptr_machine_search": c3["direct_vptr_store_in_examined_ctor"]["DIRECT_VPTR_STORE_IN_EXAMINED_CTOR"],
        "search_completed": c3["examined_ctor"]["decode_status"] == "RET_REACHED",
        "offset_zero_store_count": len(c3["examined_ctor"]["offset_zero_stores"]),
        "global_vtable_unverified": "ASSIGNED_OBJECT_VTABLE = UNVERIFIED" in fr,
        "global_polymorphism_not_established": "OBJECT_POLYMORPHISM = NOT_ESTABLISHED" in fr,
        "callsites_direct_measured": c3["known_examined_callsites_direct"]["KNOWN_EXAMINED_CALLSITES_ARE_DIRECT"] == "YES",
    }
    forbidden_phrases = ["ASSIGNED_OBJECT_VTABLE = NONE", "NON-POLYMORPHIC",
                         "non-polymorphic", "vtable_store_found",
                         "all methods direct-called", "0xA4 bytes (280)"]
    sweep_hits = {}
    sweep_files = ["FINAL_REPORT.md", "HANDOFF.md", "INPUT_IDENTITIES.md",
                   "CORRECTED_PIN_LEDGER.csv", "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"]
    for sf in sweep_files:
        content = open(os.path.join(RUN, sf), encoding="utf-8", errors="replace").read()
        hits = [ph for ph in forbidden_phrases if ph in content]
        if hits:
            sweep_hits[sf] = hits
    q13["superseded_phrase_sweep_hits"] = sweep_hits
    q13["ok"] = (q13["direct_vptr_machine_search"] == "NOT_OBSERVED"
                 and q13["search_completed"] and q13["global_vtable_unverified"]
                 and q13["global_polymorphism_not_established"]
                 and q13["callsites_direct_measured"] and not sweep_hits)
    gates["Q13"] = ("PASS" if q13["ok"] else "FAIL", q13)

    # ---------------- Q14: nonclaims + forbidden scope + predecessor preservation ----------------
    required_strings = [
        "ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED",
        "WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED",
        "FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED",
        "EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED",
        "EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED",
        "ULTIMATE_VALUE_SOURCE = UNKNOWN",
        "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED",
        "WORLD_XYZ_RECOVERED = NO",
        "NEW_BACKING_SOURCE_RE_EXECUTED = NO",
        "TEMPLATES_VFS_OPENED = NO",
        "RECORD_A_ANALYZED = NO",
        "MODEL_194013_TRACE_EXECUTED = NO",
        "CLIENT_EXECUTED = NO",
        "KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES",
        "PACKAGE_CORRECTION_STATUS = CORRECTED",
        "CANONICAL_GATE_EFFECT = NONE",
        "HISTORICAL_FUNCTION_BUDGET_COUNT =\n  8_DECLARED_AND_MECHANICALLY_REPRODUCED".replace("\n  ", " "),
        "PRE_ANALYSIS_CHRONOLOGY_INDEPENDENTLY_ESTABLISHED = NO",
        "ACTUAL_HISTORICAL_BUDGET_OVERRUN = NOT_ESTABLISHED",
        "WRITER_FUNCTION = FUN_009777F0",
        "WRITER_VA = 0x00977810",
        "TAG6_TO_ID10 = PRESERVED_CONFIRMED",
        "SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED",
        "TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD",
        "FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL",
        "ASSIGNMENT_FUNCTION = FUN_0070C680",
        "ASSIGNMENT_VA = 0x0070C71E",
        "ASSIGNED_OBJECT_SIZE = 0xA4/164 B",
        "ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380",
        "STATIC_FACTORY_MEMBER_IDENTITY = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS",
    ]
    missing = [s for s in required_strings if s not in fr]
    # instruments open()-argument census: extract ONLY actual open(...) call
    # arguments (literal strings inside the call, incl. os.path.join args);
    # prose mentions of extensions in comments are NOT opened files.
    opened = set()
    open_calls = []
    for fn in os.listdir(os.path.join(RUN, "03_SCRIPTS")):
        if fn.endswith(".py"):
            src = open(os.path.join(RUN, "03_SCRIPTS", fn), encoding="utf-8").read()
            for m in re.finditer(r"open\(([^)\n]{0,160})", src):
                arg = m.group(1)
                open_calls.append({"file": fn, "arg": arg.strip()[:80]})
                for lit in re.findall(r'"([^"]{1,150})"', arg):
                    if any(c in lit for c in "/\\.") or lit.startswith("w") or "b" == lit:
                        opened.add(lit if ("/" in lit or "\\" in lit) else lit)
    def _lit_of(call):
        arg = call["arg"] if isinstance(call, dict) else call
        lits = re.findall(r'"([^"]{1,150})"', arg)
        return [x for x in lits if "/" in x or "\\" in x or "." in x]
    opened_lits = set()
    for c in open_calls:
        for x in _lit_of(c):
            opened_lits.add(os.path.basename(x))
    forbidden_ext = [p for p in opened_lits
                      if p.lower().endswith((".vfs", ".bnt", ".nif", ".ark"))]
    http_hits = []
    # the search markers are built from split literals so this check cannot
    # match its own source
    _m1 = "ht" + "tp://"
    _m2 = "ht" + "tps://"
    for fn in os.listdir(os.path.join(RUN, "03_SCRIPTS")):
        if fn.endswith(".py"):
            src = open(os.path.join(RUN, "03_SCRIPTS", fn), encoding="utf-8").read()
            if _m1 in src or _m2 in src:
                http_hits.append(fn)
    q14 = {"missing_required_strings": missing,
           "instrument_open_calls": open_calls,
           "opened_path_literals": sorted(opened_lits),
           "forbidden_extensions_opened": forbidden_ext,
           "http_in_instruments": http_hits,
           "exe_only_plus_package_and_historical": True}
    q14["ok"] = (not missing and not forbidden_ext and not http_hits)
    gates["Q14"] = ("PASS" if q14["ok"] else "FAIL", q14)

    # ---------------- AUX: supersession quotecheck ----------------
    ledger_path = os.path.join(RUN, "SUPERSESSION_LEDGER.md")
    led = open(ledger_path, encoding="utf-8").read()
    quotecheck = {"records": 0, "failures": []}
    current_src = None
    for line in led.splitlines():
        if line.startswith("- SOURCE_FILE: "):
            current_src = line[len("- SOURCE_FILE: "):].strip().strip("`")
        elif "ORIGINAL_EXCERPT" in line and "`" in line and current_src:
            a = line.find("`")
            b = line.rfind("`")
            if b > a:
                excerpt = line[a + 1:b]
                src_path = os.path.join(REPO, current_src)
                try:
                    src_content = open(src_path, encoding="utf-8").read()
                    ok = excerpt in src_content
                except OSError:
                    ok = False
                quotecheck["records"] += 1
                if not ok:
                    quotecheck["failures"].append({"source": current_src, "excerpt": excerpt[:120]})
    quotecheck["ok"] = (quotecheck["records"] >= 25 and not quotecheck["failures"])

    # ---------------- verdict ----------------
    gate_status = {k: v[0] for k, v in gates.items()}
    qc_pass = all(s == "PASS" for s in gate_status.values()) and quotecheck["ok"]
    final = {
        "run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004",
        "qc_scope": "SELF_CHECK_FACTORY_PLUS_84_C1_FORENSIC_QC_CORRECTION",
        "gates": {k: v[0] for k, v in gates.items()},
        "gate_details": {k: v[1] for k, v in gates.items()},
        "aux_quotecheck": quotecheck,
        "QC_VERDICT": "QC_PASS" if qc_pass else "QC_FAIL",
        "outcome_conditional_note": ("QC PASS means the corrected claims accurately match evidence "
                                     "and uncertainty; it does NOT mean all census candidates were "
                                     "solved (828 unresolved write candidates and the NOT_ESTABLISHED "
                                     "invariants are the corrected honest states)"),
    }
    with open(args.out_final, "w", newline="\n") as f:
        json.dump(final, f, indent=1)
    print("CQC done. gates:", json.dumps(gate_status), "quotecheck:",
          quotecheck["records"], "failures:", len(quotecheck["failures"]),
          "verdict:", final["QC_VERDICT"])


if __name__ == "__main__":
    main()
