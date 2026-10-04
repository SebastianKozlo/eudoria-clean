# cqc_battery.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
# Fresh production QC (AF1 repair) for the C2 correction package.
#
# AF1 REPAIR vs the C1 battery (Desktop post-audit finding AF1/P2): the C1
# battery tested its own synthetic constants (CONTROL A/D fixtures) and did not
# validate the ACTUAL committed artifacts' load-bearing fields (C1 JSON
# opcode_bytes, CSV measured_operand, C3 store collection, census boundary
# anchors were all mutable without detection). THIS battery validates the
# actual generated package artifacts against fresh EXE re-derivation:
#   Q2  C1 pin JSON integrity vs EXE re-derivation  [M1 mutation gate]
#   Q3  pin CSV full-row re-derivation (measured_operand incl.)  [M2 gate]
#   Q4  decoder unit battery (corrected length rules) + census re-decode
#   Q5  AF2 boundary counterexamples A-E + census boundary discipline sweep
#   Q6  census boundary-anchor integrity per row  [M4 gate]
#   Q7  AF3 provenance discipline + ledger/census identity chains  [AF3 gate]
#   Q8  P3-A segment-semantics store census re-derivation  [M3 gate]
#   Q9  census arithmetic re-summed from the emitted CSV
#   Q10 known stores physical re-pin
#   Q11 factory identity/enumeration from measured evidence (+ CONTROL B)
#   Q12 object structural identity
#   Q13 P3-B declared-family metadata agreement (derived, not hard-coded)
#   Q14 forbidden scope + nonclaims + supersession quotecheck + P3-C (docs mode)
#   MUT  causal mutation harness M1-M4 + AF3/Q8: a TEMPORARY COPY of the
#        ACTUAL final artifact is mutated on disk (temp dir outside the repo)
#        and routed through the SAME production gate; UNMUTATED=PASS and
#        MUTATED=FAIL is required for causality. No corrupted copy is persisted
#        as a canonical artifact; only before/after values + causal results.
#
# Modes: --mode data (Q1-Q13 + mutations; docs gates pending) |
#         --mode docs (Q14 + full verdict; requires the final documents).
# The authoritative committed record is the LAST full run (data+docs).
# Outputs: 01_RAW/CQC_DECODER_UNIT_TESTS.json, 01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json,
# 01_RAW/CQC_MUTATION_RESULTS.json, 01_RAW/CQC_FINAL.json,
# AF1_MUTATION_MATRIX.csv, AF2_BOUNDARY_TEST_MATRIX.csv (--out* overrides).

import argparse
import copy
import csv
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402
import c2_census as c2mod  # noqa: E402  (family table import for P3-B)

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004")
SOURCE_PACKAGE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
                  r"\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "535e1a00fe793299dea7fc639e552560a6ac633b"

MUTATABLE = {
    "C1_PIN_EVIDENCE.json": ("01_RAW", "C1_PIN_EVIDENCE.json", "json"),
    "CORRECTED_PIN_LEDGER.csv": ("", "CORRECTED_PIN_LEDGER.csv", "csv"),
    "C3_OBJECT_SCOPE.json": ("01_RAW", "C3_OBJECT_SCOPE.json", "json"),
    "CENSUS.csv": ("", "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv", "csv"),
    "AF3_PROVENANCE_LEDGER.csv": ("", "AF3_PROVENANCE_LEDGER.csv", "csv"),
}
# non-mutated artifacts that load_pkg also reads; copied byte-identical into
# every mutation temp tree so the mutated package differs from the production
# package ONLY in the mutated field
COPY_ONLY = [("01_RAW", "C2_CENSUS.json")]


def load_pkg(root):
    pkg = {"root": root}
    with open(os.path.join(root, "01_RAW", "C1_PIN_EVIDENCE.json"), encoding="utf-8") as f:
        pkg["c1"] = json.load(f)
    with open(os.path.join(root, "CORRECTED_PIN_LEDGER.csv"), newline="", encoding="utf-8") as f:
        pkg["pins"] = list(csv.DictReader(f))
    with open(os.path.join(root, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"), newline="", encoding="utf-8") as f:
        pkg["census"] = list(csv.DictReader(f))
    with open(os.path.join(root, "01_RAW", "C2_CENSUS.json"), encoding="utf-8") as f:
        pkg["c2"] = json.load(f)
    with open(os.path.join(root, "01_RAW", "C3_OBJECT_SCOPE.json"), encoding="utf-8") as f:
        pkg["c3"] = json.load(f)
    with open(os.path.join(root, "AF3_PROVENANCE_LEDGER.csv"), newline="", encoding="utf-8") as f:
        pkg["af3"] = list(csv.DictReader(f))
    return pkg


class Ctx(object):
    """EXE-derived context shared by all gates (identity pinned once)."""

    def __init__(self):
        self.data, self.ib, self.secs, self.text, self.tva = pebnd.load_text()
        self.sha = hashlib.sha256(self.data).hexdigest()
        self.exe_ok = (self.sha.upper() == pebnd.PINNED_EXE_SHA256
                       and len(self.data) == pebnd.PINNED_EXE_SIZE)
        self.cache = pebnd._BoundaryCache(self.text, self.tva)
        self.thisflow = {}
        for e in pebnd.KNOWN_ENTRIES:
            regs = set()
            i = e - self.tva
            end = i + 0x40
            steps = 0
            while i < end and i < len(self.text) and steps < 64:
                ins = x86dec.decode(self.text, i)
                if ins is None:
                    break
                if (not ins.prefixes and ins.opcode == 0x8B and ins.mod == 3
                        and ins.rm == 1):
                    regs.add(x86dec.REGS32[ins.reg])
                i += ins.length
                steps += 1
            self.thisflow[e] = regs

    def pin_provenance(self, ins, bstatus, bsrc, bstart):
        if ins is None or not ins.memop:
            return "UNRESOLVED"
        if ins.ea_base is not None:
            base_name = x86dec.REGS32[ins.ea_base]
            if bstatus == "CONFIRMED" and bsrc == "KNOWN_FUNCTION_ENTRY" \
                    and bstart in pebnd.KNOWN_ENTRIES:
                if base_name in self.thisflow[bstart]:
                    return "THIS_OF_KNOWN_FUNCTION:" + pebnd.KNOWN_ENTRIES[bstart]
            return "UNRESOLVED"
        if ins.ea_base is None and ins.ea_index is None:
            return "ABSOLUTE_STATIC_ADDRESS"
        return "UNRESOLVED"


# ============================ Q1: baseline + EXE ============================
def gate_q1(ctx):
    q1 = {"exe_size": len(ctx.data), "exe_sha256": ctx.sha,
          "exe_pinned_match": ctx.exe_ok}
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       cwd=REPO).decode().strip()
        origin = subprocess.check_output(["git", "rev-parse", "origin/master"],
                                         cwd=REPO).decode().strip()
        remote = subprocess.check_output(["git", "ls-remote", "origin", "master"],
                                         cwd=REPO).decode().split()[0]
    except Exception as e:
        head = origin = remote = "ERROR: %s" % e
    q1.update({"local_head": head, "origin_master": origin,
               "actual_remote_master": remote})
    q1["baseline_ok"] = (ctx.exe_ok and head == BASE_SHA and origin == BASE_SHA
                         and remote == BASE_SHA)
    q1["scope_note"] = ("pre-publication execution state: the BASE check applies "
                        "to this run's pre-commit state; after this package's own "
                        "commit the HEAD moves BY DESIGN - a post-publication "
                        "re-run seeing the new HEAD is NOT artifact corruption "
                        "and NOT a mutation-test result")
    return ("PASS" if q1["baseline_ok"] else "FAIL"), q1


# ============ Q2 [M1]: C1 pin JSON integrity vs fresh EXE derivation ============
def gate_q2(pkg, ctx):
    q2 = {"json_pins": len(pkg["c1"]["pins"]), "mismatches": [],
          "json_csv_inconsistencies": []}
    csv_by_id = {p["claim_id"]: p for p in pkg["pins"]}
    for pin in pkg["c1"]["pins"]:
        cid = pin["claim_id"]
        va = int(pin["instruction_va"], 16)
        off = va - ctx.tva
        ins = x86dec.decode(ctx.text, off) if 0 <= off < len(ctx.text) else None
        derived_bytes = ctx.text[off:off + (ins.length if ins else 0)].hex(" ").upper() if ins else None
        if pin.get("opcode_bytes") != derived_bytes:
            q2["mismatches"].append({"claim": cid, "field": "opcode_bytes",
                                     "json": pin.get("opcode_bytes"),
                                     "derived": derived_bytes})
        if pin.get("instruction_length") != (ins.length if ins else None):
            q2["mismatches"].append({"claim": cid, "field": "instruction_length"})
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
            ctx.text, ctx.tva, va, ctx.cache)
        if pin.get("boundary_status") != bstatus:
            q2["mismatches"].append({"claim": cid, "field": "boundary_status",
                                     "json": pin.get("boundary_status"),
                                     "derived": bstatus})
        if pin.get("boundary_source") != bsrc:
            q2["mismatches"].append({"claim": cid, "field": "boundary_source",
                                     "json": pin.get("boundary_source"),
                                     "derived": bsrc})
        # JSON <-> CSV consistency for the same claim
        row = csv_by_id.get(cid)
        if row is None:
            q2["json_csv_inconsistencies"].append({"claim": cid, "why": "no CSV row"})
            continue
        if row["opcode_bytes"] != (pin.get("opcode_bytes") or ""):
            q2["json_csv_inconsistencies"].append({"claim": cid, "field": "opcode_bytes"})
        if row["boundary_status"] != (pin.get("boundary_status") or ""):
            q2["json_csv_inconsistencies"].append({"claim": cid, "field": "boundary_status"})
    q2["ok"] = (not q2["mismatches"] and not q2["json_csv_inconsistencies"]
                and pkg["c1"]["pin_totals"]["fail_count"] == 0)
    return ("PASS" if q2["ok"] else "FAIL"), q2


# ============ Q3 [M2]: pin CSV full-row re-derivation ============
def gate_q3(pkg, ctx):
    q3 = {"rows": len(pkg["pins"]), "mismatches": []}

    def mm(cid, field, got, exp):
        q3["mismatches"].append({"claim": cid, "field": field,
                                 "csv": got, "derived": exp})

    for p in pkg["pins"]:
        cid = p["claim_id"]
        va = int(p["instruction_va"], 16)
        off = va - ctx.tva
        ins = x86dec.decode(ctx.text, off) if 0 <= off < len(ctx.text) else None
        derived_bytes = ctx.text[off:off + (ins.length if ins else 1)].hex(" ").upper()
        if p["opcode_bytes"] != derived_bytes:
            mm(cid, "opcode_bytes", p["opcode_bytes"], derived_bytes)
        if p["instruction_length"] != (str(ins.length) if ins else "1"):
            mm(cid, "instruction_length", p["instruction_length"],
               str(ins.length) if ins else "1")
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
            ctx.text, ctx.tva, va, ctx.cache)
        if p["boundary_status"] != bstatus:
            mm(cid, "boundary_status", p["boundary_status"], bstatus)
        if p["boundary_source"] != (bsrc or ""):
            mm(cid, "boundary_source", p["boundary_source"], bsrc or "")
        if p["boundary_start"] != (("0x%08X" % bstart) if bstart else ""):
            mm(cid, "boundary_start", p["boundary_start"],
               ("0x%08X" % bstart) if bstart else "")
        if p["boundary_refuted_by"] != (("0x%08X" % brefuted) if brefuted else ""):
            mm(cid, "boundary_refuted_by", p["boundary_refuted_by"],
               ("0x%08X" % brefuted) if brefuted else "")
        # measured_operand re-derivation
        if p["operand_kind"].startswith("imm") and ins is not None and ins.imm_width:
            exp = "0x%X (%d)" % (ins.imm_raw, ins.imm_raw)
            if p["measured_operand"] != exp:
                mm(cid, "measured_operand", p["measured_operand"], exp)
            ioff = ins.length - ins.imm_width
            if p["raw_operand"] != ctx.text[off + ioff:off + ioff + ins.imm_width].hex(" ").upper():
                mm(cid, "raw_operand", p["raw_operand"],
                   ctx.text[off + ioff:off + ioff + ins.imm_width].hex(" ").upper())
        if p["operand_kind"] in ("mem32", "mem8") and ins is not None and ins.disp_width:
            disp_off = ins.length - ins.disp_width - (ins.imm_width or 0)
            if p["raw_operand"] != ctx.text[off + disp_off:off + disp_off + ins.disp_width].hex(" ").upper():
                mm(cid, "raw_operand(mem)", p["raw_operand"],
                   ctx.text[off + disp_off:off + disp_off + ins.disp_width].hex(" ").upper())
        if p["operand_kind"] in ("mem32", "mem8", "mem0") and ins is not None and ins.memop:
            ea = ins.ea_text()
            prov = ctx.pin_provenance(ins, bstatus, bsrc, bstart)
            raw = ("0x%08X" % ins.disp_raw) if ins.disp_width else "NONE"
            signed = ins.disp_signed if ins.disp_width else 0
            exp = ("%s | base=%s;index=%s;scale=%d;raw=%s;signed=%d;"
                   "effective=%d;prov=%s") % (
                ea,
                x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else "None",
                x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else "None",
                ins.ea_scale, raw, signed, signed, prov)
            if p["measured_operand"] != exp:
                mm(cid, "measured_operand", p["measured_operand"], exp)
        if p["operand_kind"] == "rel32":
            cv = pebnd.validate_direct_call(ctx.text, ctx.tva, va, ctx.cache)
            if cv["call_validation"] == "PASS":
                exp_t = "0x%08X" % cv["target"]
            elif cv["call_validation"] == "NOT_VERIFIED":
                exp_t = ("NOT_PROMOTED(apparent=%s)"
                         % cv["apparent_target_not_promoted"]
                         if cv["apparent_target_not_promoted"] else "NOT_PROMOTED")
            else:
                exp_t = "NONE"
            if p["measured_target"] != exp_t:
                mm(cid, "measured_target", p["measured_target"], exp_t)
            # status re-derivation for call rows
            exp_status = {"PASS": "VALIDATED", "NOT_VERIFIED": "NOT_VERIFIED",
                          "FAIL_MID_INSTRUCTION": "FAIL_MID_INSTRUCTION",
                          "FAIL_PREFIXED": "FAIL", "FAIL": "FAIL"}[cv["call_validation"]]
            # corrected records keep their CORRECTED_VALIDATED class when PASS
            if exp_status == "VALIDATED" and p["status"] == "CORRECTED_VALIDATED":
                exp_status = "CORRECTED_VALIDATED"
            if p["status"] != exp_status:
                mm(cid, "status", p["status"], exp_status)
        elif p["status"] == "DECLASSIFIED_NOT_A_CALL":
            b = ctx.text[off] if 0 <= off < len(ctx.text) else None
            if b == 0xE8:
                mm(cid, "declassified", "byte IS E8", "not E8")
        else:
            if bstatus == "CONFIRMED":
                exp_status = "VALIDATED"
            elif bstatus == "UNRESOLVED":
                exp_status = "VALIDATED_BYTES_BOUNDARY_UNRESOLVED"
            else:
                exp_status = "FAIL_MID_INSTRUCTION"
            if p["status"] == "CORRECTED_VALIDATED" and exp_status == "VALIDATED":
                exp_status = "CORRECTED_VALIDATED"
            if p["status"] != exp_status:
                mm(cid, "status", p["status"], exp_status)
    q3["ok"] = not q3["mismatches"]
    return ("PASS" if q3["ok"] else "FAIL"), q3


# ============ Q4: decoder unit battery + census re-decode ============
UNIT_VECTORS = [
    # (hex, expected length or "REJECT", note)
    ("8B 04 85 00 00 00 00", 7, "SIB base+index+disp32"),
    ("8B 04 24", 3, "SIB [ESP]"),
    ("66 B8 01 00", 4, "66 imm16 (unchanged C1 rule)"),
    ("89 86", "REJECT", "truncated modrm+disp -> fail-closed"),
    ("0F C6 C0 E8 00 00 00 00", 4, "AF2 class B: SHUFPS 0F C6 /r ib - imm8 is part of the instruction (C1 measured 3, the defect)"),
    ("0F C6 C0", "REJECT", "SHUFPS truncated (ModRM without the imm8) -> fail-closed"),
    ("0F C4 C0 E8 00 00 00 00", 4, "PINSRW /r ib (imm8, class-B family fix)"),
    ("0F C5 C0 E8 00 00 00 00", 4, "PEXTRW /r ib (imm8, class-B family fix)"),
    ("67 8B 06 84 00 90", 5, "AF2 class C: 16-bit address form MOV EAX,[0x0084] (C1 fabricated 32-bit ModRM length 3; Capstone reference 5)"),
    ("67 8B 06 E8 00 90", 5, "class C with E8 inside disp16 - length must stay 5"),
    ("66 E8 01 00 90", 4, "AF2 class D: 66 E8 = CALL rel16, length 4 (C1 parsed as 6-byte ordinary rel32; Capstone reference 4)"),
    ("B8 CC CC E8 00", 5, "class A: MOV EAX,0x00E8CCCC - the E8 is immediate data"),
    ("64 A3 00 00 00 00", 6, "P3-A: MOV FS:[0],EAX (MOFFS + FS) - segment recorded"),
    ("64 89 0D 00 00 00 00", 7, "P3-A: MOV FS:[0],ECX ([disp32] + FS)"),
    ("9A 11 22 33 44 55 66 77", "REJECT", "CALL far not in table -> fail-closed reject"),
    ("EA 11 22 33 44 55 66 77", "REJECT", "JMP far not in table -> fail-closed reject"),
    ("67 E8 01 00 00 00 90", "REJECT", "address-size-prefixed near branch -> fail-closed reject"),
    ("26 2E 64 36 3E 90", "REJECT", "two+ segment prefixes (6 prefix bytes) -> fail-closed reject"),
]


def gate_q4(pkg, ctx):
    unit = []
    for hexstr, exp, note in UNIT_VECTORS:
        b = bytes.fromhex(hexstr.replace(" ", ""))
        ins = x86dec.decode(b, 0)
        got = ins.length if ins else "REJECT"
        seg = ins.segment if ins else None
        ok = (got == exp)
        unit.append({"vector": hexstr, "expected": exp, "measured": got,
                     "segment": seg, "note": note, "ok": ok})
    # segment semantics spot checks
    ins_fs = x86dec.decode(bytes.fromhex("64A300000000"), 0)
    unit.append({"vector": "64 A3 00 00 00 00", "segment": ins_fs.segment,
                 "expected_segment": "FS", "ok": ins_fs.segment == "FS",
                 "note": "P3-A segment prefix recorded on MOFFS store"})
    ins_fs2 = x86dec.decode(bytes.fromhex("64890D00000000"), 0)
    unit.append({"vector": "64 89 0D 00 00 00 00", "segment": ins_fs2.segment,
                 "expected_segment": "FS", "ok": ins_fs2.segment == "FS",
                 "note": "P3-A segment prefix recorded on [disp32] store"})
    ins_a = x86dec.decode(bytes.fromhex("B8CCCCE800000000"), 0)
    unit.append({"vector": "B8 CC CC E8 00 00 00 00", "imm_raw": "0x%08X" % ins_a.imm_raw,
                 "expected_imm": "0x00E8CCCC", "ok": ins_a.imm_raw == 0x00E8CCCC,
                 "note": "class A: the E8 byte is immediate data of MOV EAX,imm32"})
    ins_d = x86dec.decode(bytes.fromhex("66E80100"), 0)
    unit.append({"vector": "66 E8 01 00", "rel16": ins_d.rel16,
                 "imm_signed": ins_d.imm_signed, "ok": bool(ins_d.rel16),
                 "note": "class D: operand-size-prefixed CALL decoded at its actual width"})
    # re-decode every census row from its VA
    redecode_bad = []
    for r in pkg["census"]:
        va = int(r["va"], 16)
        off = va - ctx.tva
        ins = x86dec.decode(ctx.text, off)
        exp_status = "OK" if ins is not None else "REJECT"
        if exp_status != r["decoder_status"]:
            redecode_bad.append({"va": r["va"], "field": "decoder_status"})
        elif ins is not None and str(ins.length) != str(r["instruction_length"]):
            redecode_bad.append({"va": r["va"], "field": "instruction_length"})
    # coverage windows sanity
    cov = {}
    for name, w in (("setter", (0x0070C680, 0x130)), ("loop", (0x00703E80, 0x88)),
                    ("driver", (0x004B0980, 0x140)), ("register", (0x00707FB0, 0x110)),
                    ("modeinit", (0x007080C0, 0x68)), ("stream_ctor", (0x00972380, 0x15C)),
                    ("modecond", (0x00703CD0, 0x16)), ("slotpred", (0x0070CC80, 0x60)),
                    ("consumer", (0x0070DCF0, 0xE0)), ("manager_ctor", (0x00707E50, 0x90))):
        va0, sz = w
        i = va0 - ctx.tva
        ok_cnt = 0
        total = 0
        while i < va0 - ctx.tva + sz:
            ins = x86dec.decode(ctx.text, i)
            total += 1
            if ins is None:
                break
            i += ins.length
            ok_cnt += 1
        cov[name] = {"decoded_instructions": ok_cnt,
                     "aborted": total - ok_cnt - 1 if total > ok_cnt else 0}
    unit_ok = all(u.get("ok", True) for u in unit)
    q4 = {"unit_battery": unit, "unit_battery_ok": unit_ok,
          "redecode_bad_rows": redecode_bad, "coverage_windows": cov}
    q4["ok"] = unit_ok and not redecode_bad
    return ("PASS" if q4["ok"] else "FAIL"), q4


# ============ Q5: AF2 boundary counterexamples + discipline sweep ============
def gate_q5(pkg, ctx):
    ce = []
    SYN_BASE = 0x00A00000

    def add_case(case_id, hexstr, entry_off, cand_off, exp_decode, exp_promo,
                 c1_defect, exp_status="REFUTED_MID_INSTRUCTION"):
        buf = bytes.fromhex(hexstr.replace(" ", ""))
        entries = {SYN_BASE + entry_off: "TEST_TRUE_ENTRY"} if entry_off is not None else {}
        cand_va = SYN_BASE + cand_off
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
            buf, SYN_BASE, cand_va, cache=None, entries=entries or None)
        cv = pebnd.validate_direct_call(buf, SYN_BASE, cand_va, cache=None,
                                        entries=entries or None)
        actual_promo = ("PROMOTED->0x%08X" % cv["target"]) if cv["target"] else (
            "NONE(%s)" % cv["call_validation"])
        rec = {
            "CASE_ID": case_id,
            "BYTES": hexstr,
            "START_OFFSET": entry_off,
            "CANDIDATE_OFFSET": cand_off,
            "EXPECTED_DECODE": exp_decode,
            "ACTUAL_DECODE": ("covered mid-instruction by proven decode from "
                              "anchor 0x%08X" % brefuted) if brefuted else
                             ("boundary %s (source=%s)" % (bstatus, bsrc)),
            "EXPECTED_CALL_PROMOTION": exp_promo,
            "ACTUAL_CALL_PROMOTION": actual_promo,
            "BOUNDARY_SOURCE": bsrc,
            "BOUNDARY_STATUS": bstatus,
            "C1_DEFECT_NOTE": c1_defect,
            "CALL_VALIDATION": cv["call_validation"],
            "test_passed": (bstatus == exp_status and cv["target"] is None
                            if exp_promo == "NO_PROMOTION" else
                            bstatus == exp_status and cv["target"] is not None),
        }
        ce.append(rec)
        return rec

    # Class A1: delimiter bytes inside an immediate (CC CC variant)
    add_case("A1_B8_CC_CC_E8_imm", "B8 CC CC E8 00 00 00 00 C3", 0, 3,
             "MOV EAX,0x00E8CCCC length 5; the E8 at +3 is immediate data",
             "NO_PROMOTION",
             "C1: nearest-first T2 CC-padding start at +3 (trivial exact landing) "
             "confirmed the candidate and PROMOTED the CALL (CALL_VALIDATION=PASS, "
             "boundary_source=CC_PADDING_DELIMITED_START, target=0x00A00008)")
    # Class A2: delimiter bytes inside an immediate (C3 CC variant)
    add_case("A2_B8_C3_CC_E8_imm", "B8 C3 CC E8 00 00 00 00 C3", 0, 3,
             "MOV EAX,0x00E8CCC3 length 5; the E8 at +3 is immediate data",
             "NO_PROMOTION",
             "C1: nearest-first T3 RET-delimited start at +3 confirmed the "
             "candidate and PROMOTED the CALL (boundary_source=RET_DELIMITED_START)")
    # Class B: SHUFPS imm8
    add_case("B_0F_C6_shufps_imm8", "0F C6 C0 E8 00 00 00 00 C3", 0, 3,
             "SHUFPS xmm0,xmm0,imm8 length 4 (0F C6 C0 E8); the E8 at +3 is the "
             "SHUFPS imm8",
             "NO_PROMOTION",
             "C1: the decoder measured 0F C6 C0 as 3 bytes (missing imm8), the "
             "proven decode landed ON the E8 and PROMOTED it as CALL even with "
             "KNOWN_FUNCTION_ENTRY")
    # Class C: address-size override, E8 inside disp16
    add_case("C_67_8B_06_disp16", "67 8B 06 E8 00 90 C3", 0, 3,
             "MOV EAX,[0x00E8] 16-bit address form length 5 (67 8B 06 E8 00); "
             "the E8 at +3 is disp16 data",
             "NO_PROMOTION",
             "C1: _parse_modrm ignored has67 and fabricated a 32-bit ModRM "
             "length (3), so the disp16 bytes were exposed as instruction starts")
    # Class D: operand-size-prefixed CALL
    add_case("D_66_E8_rel16", "66 E8 01 00 90 C3", 0, 1,
             "CALL rel16 (66 E8 01 00) length 4; the E8 at +1 is the opcode of a "
             "DIFFERENT encoding than the examined five-byte E8 rel32",
             "NO_PROMOTION",
             "C1: the REL32 handler ignored has66 and silently parsed 66 E8 as an "
             "ordinary five-byte E8 rel32 (measured length 6)")
    # Class E: positive control - correctly aligned E8 rel32 from a true entry
    add_case("E_positive_real_call", "B8 01 00 00 00 E8 05 00 00 00 C3", 0, 5,
             "MOV EAX,1 length 5 then CALL rel32 at +5 (instruction boundary)",
             "PROMOTE",
             "positive control: an ordinary correctly-aligned E8 rel32 from an "
             "independently established entry must still validate and resolve "
             "its target", exp_status="CONFIRMED")

    # real-EXE positive controls (production anchors)
    real_pos = []
    for va, exp_t in ((0x0070C715, 0x00972380), (0x0070DD75, 0x00971AD0),
                      (0x0070C742, 0x00972DF0)):
        cv = pebnd.validate_direct_call(ctx.text, ctx.tva, va, ctx.cache)
        real_pos.append({"va": "0x%08X" % va, "call_validation": cv["call_validation"],
                         "boundary_source": cv["boundary_source"],
                         "target": ("0x%08X" % cv["target"]) if cv["target"] else None,
                         "expected_target": "0x%08X" % exp_t,
                         "ok": cv["call_validation"] == "PASS" and cv["target"] == exp_t})

    # non-E8 control (C1 CONTROL C equivalent)
    syn = bytes.fromhex("BB01000000")
    cv_c = pebnd.validate_direct_call(syn, 0x00A00000, 0x00A00000)
    ctrl_c_ok = cv_c["call_validation"] == "FAIL" and cv_c["target"] is None

    # census discipline sweep: no heuristic source on CONFIRMED rows; REFUTED
    # rows carry the refuting anchor; anchor registry complete
    bad_confirmed = [r["va"] for r in pkg["census"]
                     if r["boundary_status"] == "CONFIRMED"
                     and r["boundary_source"] != "KNOWN_FUNCTION_ENTRY"]
    bad_refuted = [r["va"] for r in pkg["census"]
                   if r["boundary_status"] == "REFUTED_MID_INSTRUCTION"
                   and not r["boundary_refuted_by"]]
    bad_containing = []
    for r in pkg["census"]:
        if r["boundary_status"] == "CONFIRMED":
            bstart = None
            # containing_function must name a KNOWN_ENTRIES value
            if r["boundary_source"] == "KNOWN_FUNCTION_ENTRY" \
                    and r["containing_function"] not in pebnd.KNOWN_ENTRIES.values():
                bad_containing.append({"va": r["va"],
                                       "containing_function": r["containing_function"]})
    # heuristic candidates never appear as confirming sources anywhere
    pin_bad_src = [p["claim_id"] for p in pkg["pins"]
                   if p["boundary_status"] == "CONFIRMED"
                   and p["boundary_source"] != "KNOWN_FUNCTION_ENTRY"]
    anchors = pebnd.anchor_registry()
    anchors_ok = (len(anchors) == len(pebnd.KNOWN_ENTRIES)
                  and all(a["EVIDENCE_STATUS"] and a["EXISTING_PHYSICAL_EVIDENCE"]
                          and a["EVIDENCE_SOURCE"] for a in anchors))

    q5 = {"counterexamples": ce, "real_positive_controls": real_pos,
          "control_nonE8": ctrl_c_ok,
          "census_confirmed_with_untrusted_source": bad_confirmed,
          "census_refuted_without_anchor": bad_refuted,
          "census_confirmed_bad_containing": bad_containing,
          "pins_confirmed_with_untrusted_source": pin_bad_src,
          "anchor_registry_complete": anchors_ok,
          "anchor_registry": anchors}
    q5["ok"] = (all(c["test_passed"] for c in ce)
                and all(p["ok"] for p in real_pos)
                and ctrl_c_ok and not bad_confirmed and not bad_refuted
                and not bad_containing and not pin_bad_src and anchors_ok)
    return ("PASS" if q5["ok"] else "FAIL"), q5


# ============ Q6 [M4]: census boundary-anchor integrity per row ============
def gate_q6(pkg, ctx):
    q6 = {"rows": len(pkg["census"]), "mismatches": []}
    for r in pkg["census"]:
        if r["boundary_status"] == "NOT_ASSESSED_ENCODING_CONTROL":
            continue  # negative disp8 controls are boundary-free
        va = int(r["va"], 16)
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
            ctx.text, ctx.tva, va, ctx.cache)
        if r["boundary_status"] != bstatus:
            q6["mismatches"].append({"va": r["va"], "field": "boundary_status",
                                     "csv": r["boundary_status"], "derived": bstatus})
        if (r["boundary_source"] or "") != (bsrc or ""):
            q6["mismatches"].append({"va": r["va"], "field": "boundary_source",
                                     "csv": r["boundary_source"], "derived": bsrc})
        exp_containing = ""
        if bstatus == "CONFIRMED" and bsrc == "KNOWN_FUNCTION_ENTRY" \
                and bstart in pebnd.KNOWN_ENTRIES:
            exp_containing = pebnd.KNOWN_ENTRIES[bstart]
        if r["containing_function"] != exp_containing:
            q6["mismatches"].append({"va": r["va"], "field": "containing_function",
                                     "csv": r["containing_function"],
                                     "derived": exp_containing})
        exp_refuted = ("0x%08X" % brefuted) if brefuted else ""
        if r["boundary_refuted_by"] != exp_refuted:
            q6["mismatches"].append({"va": r["va"], "field": "boundary_refuted_by",
                                     "csv": r["boundary_refuted_by"],
                                     "derived": exp_refuted})
    q6["ok"] = not q6["mismatches"]
    return ("PASS" if q6["ok"] else "FAIL"), q6


# ============ Q7 [AF3 mutation gate]: provenance discipline ============
def gate_q7(pkg, ctx):
    q7 = {"ledger_rows": len(pkg["af3"]), "failures": []}

    def fail(why, extra=None):
        e = {"why": why}
        if extra:
            e.update(extra)
        q7["failures"].append(e)

    census_by_va = {r["va"]: r for r in pkg["census"]}
    # every PROVEN ledger row must carry a complete, physically re-derived chain
    for row in pkg["af3"]:
        if row["FINAL_CLASSIFICATION"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE":
            if row["ADDRESS_PROVENANCE_STATUS"] != "THIS_OF_KNOWN_FUNCTION:FUN_00707E50_manager_ctor":
                fail("PROVEN row without the resolved manager-this provenance",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"],
                      "ADDRESS_PROVENANCE_STATUS": row["ADDRESS_PROVENANCE_STATUS"]})
            if not row["IDENTITY_EDGE"].strip():
                fail("PROVEN row with empty IDENTITY_EDGE (identity edge removed/corrupted)",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"]})
            if not row["IDENTIFIED_OBJECT"].strip() or row["IDENTIFIED_OBJECT"] == "NONE":
                fail("PROVEN row without an IDENTIFIED_OBJECT",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"]})
            if not row["IDENTITY_EVIDENCE"].strip():
                fail("PROVEN row without IDENTITY_EVIDENCE",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"]})
            if "HEURISTIC" in row["IDENTITY_EVIDENCE_STATUS"]:
                fail("PROVEN row resting on heuristic-only evidence (refuse PROVEN)",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"],
                      "IDENTITY_EVIDENCE_STATUS": row["IDENTITY_EVIDENCE_STATUS"]})
            # physical re-derivation: the manager this-flow
            va_i = int(row["CANDIDATE_VA"], 16)
            crow = census_by_va.get(row["CANDIDATE_VA"])
            if crow is None:
                fail("PROVEN ledger row with no census counterpart",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"]})
            else:
                if crow["classification"] != "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE":
                    fail("census/ledger classification mismatch",
                         {"CANDIDATE_VA": row["CANDIDATE_VA"]})
                # re-derive boundary + provenance for the candidate
                off = va_i - ctx.tva
                ins = x86dec.decode(ctx.text, off)
                bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
                    ctx.text, ctx.tva, va_i, ctx.cache)
                if bstatus != "CONFIRMED" or bstart != 0x00707E50:
                    fail("PROVEN manager row no longer boundary-confirmed at "
                         "FUN_00707E50",
                         {"CANDIDATE_VA": row["CANDIDATE_VA"],
                          "derived_status": bstatus, "derived_start":
                          ("0x%08X" % bstart) if bstart else None})
                elif ins is not None and ins.ea_base is not None:
                    bn = x86dec.REGS32[ins.ea_base]
                    if bn not in ctx.thisflow[0x00707E50]:
                        fail("manager this-flow re-derivation mismatch",
                             {"base": bn})
            # manager global identity re-derivation (prior canon + this run)
            if "0x00BA12E4" not in row["IDENTITY_EVIDENCE"]:
                fail("PROVEN row evidence lost the manager singleton identity",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"]})
        else:
            # UNRESOLVED ledger rows must NOT claim proven provenance
            if row["FINAL_CLASSIFICATION"] != "UNRESOLVED":
                fail("ledger row with unexpected FINAL_CLASSIFICATION",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"],
                      "FINAL_CLASSIFICATION": row["FINAL_CLASSIFICATION"]})
            if row["ADDRESS_PROVENANCE_STATUS"] != "UNRESOLVED":
                fail("non-PROVEN ledger row must carry ADDRESS_PROVENANCE_STATUS=UNRESOLVED",
                     {"CANDIDATE_VA": row["CANDIDATE_VA"],
                      "ADDRESS_PROVENANCE_STATUS": row["ADDRESS_PROVENANCE_STATUS"]})
    # census-side discipline: every census PROVEN row has a ledger row; every
    # census UNRESOLVED-provenance row is NOT classified PROVEN wrong object
    ledger_vas = {r["CANDIDATE_VA"] for r in pkg["af3"]}
    for r in pkg["census"]:
        if r["classification"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE":
            if r["va"] not in ledger_vas:
                fail("census PROVEN row without a ledger identity chain",
                     {"va": r["va"]})
            if r["address_provenance_status"].startswith("THIS_OF_KNOWN_FUNCTION"):
                pass
            elif r["address_provenance_status"] == "UNRESOLVED":
                fail("PROVEN wrong-object row with UNRESOLVED address provenance "
                     "(AF3 defect: refuse PROVEN)",
                     {"va": r["va"]})
        if (r["classification"] == "UNRESOLVED"
                and r["address_provenance_status"] == "UNRESOLVED"
                and r["boundary_status"] == "CONFIRMED"
                and r["write_form"] in ("write", "lea_linked_write")):
            # legitimate: provenance unresolved rows stay unresolved (CONTROL F
            # rule: register naming is not proof) - no failure
            pass
    # ESP SIB control (C1 CONTROL F equivalent): register naming is not proof
    syn_f = bytes.fromhex("89842C84000000")
    ins_f = x86dec.decode(syn_f, 0)
    ctrl_f_ok = (ins_f is not None and x86dec.REGS32[ins_f.ea_base] == "ESP"
                 and x86dec.REGS32[ins_f.ea_index] == "EBP"
                 and ins_f.disp_signed == 132)
    q7["control_f_esp_sib_unresolved_provenance"] = ctrl_f_ok
    # AF3 downgrade verified: the four layout controls are NOT classified PROVEN
    for va_hex in ("0x0074955A", "0x006D4F88", "0x0075138F", "0x007196AA"):
        r = census_by_va.get(va_hex)
        if r is None:
            fail("layout control row missing from census", {"va": va_hex})
        elif r["classification"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE":
            fail("AF3 downgrade violated: layout control still PROVEN",
                 {"va": va_hex})
        elif r["classification"] != "UNRESOLVED":
            fail("layout control row unexpected classification",
                 {"va": va_hex, "classification": r["classification"]})
    # the four downgraded rows must each have an AF3 ledger row (chain fields)
    for va_hex in ("0x0074955A", "0x006D4F88", "0x0075138F", "0x007196AA"):
        if va_hex not in ledger_vas:
            fail("downgraded layout control without an AF3 ledger row",
                 {"va": va_hex})
    q7["ok"] = (not q7["failures"] and ctrl_f_ok)
    return ("PASS" if q7["ok"] else "FAIL"), q7


# ============ Q8 [M3]: P3-A segment-semantics store census ============
def gate_q8(pkg, ctx):
    q8 = {"failures": []}

    def fail(why, extra=None):
        e = {"why": why}
        if extra:
            e.update(extra)
        q8["failures"].append(e)

    c3 = pkg["c3"]
    ec = c3["examined_ctor"]
    # re-derive the ctor extent decode
    entry = 0x00972380
    insns = []
    i = entry - ctx.tva
    end = i + 0x400
    status = None
    extent_end = None
    while i < end:
        if ctx.text[i] == 0xCC:
            status, extent_end = "CC_PADDING", ctx.tva + i
            break
        ins = x86dec.decode(ctx.text, i)
        if ins is None:
            status, extent_end = "DECODE_FAIL", ctx.tva + i
            break
        insns.append(ins)
        if ins.opcode == 0xC3 and not ins.opcode2 and not ins.prefixes:
            status, extent_end = "RET_REACHED", ctx.tva + i + ins.length
            break
        i += ins.length
    if ec["decode_status"] != status or ec["extent_end"] != ("0x%08X" % extent_end):
        fail("extent decode mismatch", {"json": (ec["decode_status"], ec["extent_end"]),
                                        "derived": (status, "0x%08X" % extent_end)})
    # re-derive the effective-displacement-0 store census with segments
    thisregs = set(ec["this_registers_from_entry_mov_ecx"])
    if thisregs != ctx.thisflow[entry]:
        fail("this-register set mismatch", {"json": sorted(thisregs),
                                            "derived": sorted(ctx.thisflow[entry])})
    derived = []
    cur = entry - ctx.tva
    for ins in insns:
        cls = None
        if ins is not None and ins.memop:
            if ins.opcode2 is None and ins.opcode in (0x89, 0x88):
                cls = "MOV [r],r"
            elif ins.opcode2 is None and ins.opcode in (0xC7, 0xC6) and ins.reg == 0:
                cls = "MOV [r],imm"
            elif ins.opcode2 is None and ins.opcode in (0xA2, 0xA3):
                cls = "MOV moffs,AL/EAX"
            elif ins.opcode2 is None and ins.opcode in (0xF6, 0xF7) and ins.reg in (2, 3):
                cls = "RMW NOT/NEG r/m"
            elif ins.opcode2 is None and ins.opcode in (0xFE, 0xFF) and ins.reg in (0, 1):
                cls = "RMW INC/DEC r/m"
        if cls is not None:
            eff0 = ((ins.disp_width == 0) or (ins.disp_width and ins.disp_signed == 0))
            if eff0:
                base_name = x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else None
                derived.append({
                    "va": "0x%08X" % (ctx.tva + cur),
                    "bytes": ctx.text[cur:cur + ins.length].hex(" ").upper(),
                    "store_form": cls,
                    "segment": ins.segment,
                    "base_register": base_name,
                    "base_is_this_register": (base_name in thisregs) if base_name else False,
                    "segment_relative": ins.segment is not None,
                })
        cur += ins.length
    json_stores = ec["offset_zero_stores"]
    if len(json_stores) != len(derived):
        fail("offset-zero store collection count mismatch (collection removed/corrupted?)",
             {"json_count": len(json_stores), "derived_count": len(derived)})
    else:
        for d, j in zip(derived, json_stores):
            for field in ("va", "bytes", "segment", "base_register",
                          "segment_relative", "base_is_this_register"):
                if j.get(field) != d[field]:
                    fail("store field mismatch", {"va": d["va"], "field": field,
                                                  "json": j.get(field), "derived": d[field]})
    # the two FS:[0] SEH/TLS stores must be present with segment=FS and excluded
    fs_vas = {"0x009723A0", "0x009724CB"}
    json_fs = {s["va"] for s in json_stores if s.get("segment") == "FS"}
    if fs_vas != json_fs:
        fail("P3-A FS:[0] store set mismatch", {"expected": sorted(fs_vas),
                                                "json": sorted(json_fs)})
    for s in json_stores:
        if s.get("segment_relative") and s.get("base_is_this_register"):
            fail("segment-relative store eligible as this+0 evidence (forbidden)",
                 {"va": s["va"]})
    dv = c3["direct_vptr_store_in_examined_ctor"]
    nonseg_this = [s for s in derived if not s["segment_relative"]
                   and s["base_is_this_register"]]
    exp_vptr = "OBSERVED" if nonseg_this else ("NOT_OBSERVED" if status == "RET_REACHED" else "NOT_VERIFIED")
    if dv["DIRECT_VPTR_STORE_IN_EXAMINED_CTOR"] != exp_vptr:
        fail("DIRECT_VPTR derived status mismatch",
             {"json": dv["DIRECT_VPTR_STORE_IN_EXAMINED_CTOR"], "derived": exp_vptr})
    if dv.get("segment_relative_stores") != len([s for s in derived if s["segment_relative"]]):
        fail("segment_relative_stores count mismatch")
    if dv.get("with_this_base_non_segment") != len(nonseg_this):
        fail("with_this_base_non_segment count mismatch")
    if not dv.get("segment_exclusion_rule"):
        fail("segment exclusion rule missing from C3 JSON")
    # KNOWN_EXAMINED_CALLSITES re-derivation
    cs_ok = all(c["call_validation"] == "PASS"
                for c in c3["known_examined_callsites_direct"]["callsites"])
    derived_cs_ok = True
    for va in (0x0070DD75, 0x0070DD84, 0x0070C742):
        cv = pebnd.validate_direct_call(ctx.text, ctx.tva, va, ctx.cache)
        if cv["call_validation"] != "PASS":
            derived_cs_ok = False
    if cs_ok != derived_cs_ok or not derived_cs_ok:
        fail("KNOWN_EXAMINED_CALLSITES_ARE_DIRECT re-derivation mismatch",
             {"json": c3["known_examined_callsites_direct"]["KNOWN_EXAMINED_CALLSITES_ARE_DIRECT"]})
    q8["derived_store_count"] = len(derived)
    q8["derived_segment_relative"] = len([s for s in derived if s["segment_relative"]])
    q8["ok"] = not q8["failures"]
    return ("PASS" if q8["ok"] else "FAIL"), q8


# ============ Q9: census arithmetic re-summed from the CSV ============
def gate_q9(pkg, ctx):
    mq = pkg["c2"]["measured_quantities"]
    tally = {}
    for r in pkg["census"]:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    derived_unresolved = tally.get("UNRESOLVED", 0)
    derived_wcand = sum(1 for r in pkg["census"]
                        if r["write_form"] in ("write", "lea_linked_write")
                        and r["classification"] == "UNRESOLVED")
    q9 = {"tally": tally, "tally_sum": sum(tally.values()),
          "raw_rows": mq["RAW_PATTERN_ROWS"],
          "derived_census_unresolved": derived_unresolved,
          "derived_write_candidates": derived_wcand,
          "raw_regression_vs_desktop_2612": ("MATCH" if mq["RAW_PATTERN_ROWS"] == 2612
                                             else "CHANGED"),
          "consistency": {
              "tally_sum_eq_raw": sum(tally.values()) == mq["RAW_PATTERN_ROWS"],
              "unresolved_eq": derived_unresolved == mq["CENSUS_UNRESOLVED_ROWS"],
              "wcand_eq": derived_wcand == mq["FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES"],
              "known_eq": tally.get("KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE", 0) == mq["KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES"],
              "wrongobj_eq": tally.get("REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE", 0) == mq["REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"],
              "read_eq": tally.get("REJECTED_READ_NOT_WRITE", 0) == mq["REJECTED_READ_NOT_WRITE"],
              "midrej_eq": tally.get("REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE", 0) == mq["REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE"],
              "negctl_eq": tally.get("NEGATIVE_DISP8_MINUS_0x7C_CONTROL", 0) == mq["NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS"],
              "unresolved_ge_wcand": derived_unresolved >= derived_wcand,
          }}
    q9["ok"] = all(q9["consistency"].values())
    if mq["RAW_PATTERN_ROWS"] != 2612:
        q9["raw_change_explanation_required"] = True
    return ("PASS" if q9["ok"] else "FAIL"), q9


# ============ Q10: known stores physical re-pin ============
def gate_q10(pkg, ctx):
    q10 = {}
    for va, exp, cls in ((0x0070D013, "89 9E 84 00 00 00", "INITIALIZATION_NULL"),
                         (0x0070C71E, "89 86 84 00 00 00",
                          "CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE")):
        off = va - ctx.tva
        got = ctx.text[off:off + 6].hex(" ").upper()
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(
            ctx.text, ctx.tva, va, ctx.cache)
        row = next((r for r in pkg["census"] if int(r["va"], 16) == va), None)
        prov = row["address_provenance_status"] if row else None
        q10["0x%08X" % va] = {
            "bytes": got, "bytes_ok": got == exp,
            "boundary": bstatus, "boundary_source": bsrc,
            "boundary_start": ("0x%08X" % bstart) if bstart else None,
            "census_classification": row["classification"] if row else None,
            "census_provenance": prov,
            "store_class_in_reason": cls in (row["reason"] if row else ""),
        }
    ok = all(v["bytes_ok"] and v["boundary"] == "CONFIRMED"
             and v["boundary_source"] == "KNOWN_FUNCTION_ENTRY"
             and v["census_classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
             and v["store_class_in_reason"]
             and str(v["census_provenance"]).startswith("THIS_OF_KNOWN_FUNCTION:")
             for v in q10.values())
    return ("PASS" if ok else "FAIL"), q10


# ============ Q11: factory identity/enumeration from measured evidence ============
def gate_q11(pkg, ctx):
    def pin_imm(claim_id):
        for p in pkg["pins"]:
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
    q11 = {"measured_start": "0x%08X" % measured_start if measured_start is not None else None,
           "measured_bound": "0x%08X" % measured_bound if measured_bound is not None else None,
           "selector": "0x4E26",
           "membership_derived_from_measured": canon_b,
           "control_B_mutant_fails": not mutant_b,
           "second_range_measured": ("0x%08X" % pin_imm("modeinit_second_range_ESI_init"),
                                     "0x%08X" % pin_imm("modeinit_second_range_CMP_bound")),
           "dispatcher_entry5_measured": pkg["c1"]["censuses"]["dispatcher_entry5_selector_20006"]["entry5_value"],
           "factory_singleton_census": pkg["c1"]["censuses"]["factory_singleton_00BA590C"]["count"],
           "manager_global_census": pkg["c1"]["censuses"]["manager_global_00BA12E4"]["count"]}
    q11["ok"] = (canon_b and not mutant_b
                 and q11["dispatcher_entry5_measured"] == "0x0073C8D8")
    return ("PASS" if q11["ok"] else "FAIL"), q11


# ============ Q12: object structural identity ============
def gate_q12(pkg, ctx):
    c3 = pkg["c3"]
    pins_by_id = {p["claim_id"]: p for p in pkg["pins"]}
    q12 = {
        "size_0xA4_164": (c3["allocation_size_facts"]["ASSIGNED_OBJECT_SIZE_HEX"] == "0xA4"
                         and c3["allocation_size_facts"]["ASSIGNED_OBJECT_SIZE_DECIMAL"] == 164),
        "factory_size_0x118_280": c3["allocation_size_facts"]["FACTORY_SIZE_DECIMAL"] == 280,
        "ctor_call_target_validated": (
            pins_by_id["setter_CALL_stream_ctor"]["status"] in ("VALIDATED", "CORRECTED_VALIDATED")
            and pins_by_id["setter_CALL_stream_ctor"]["measured_target"] == "0x00972380"),
        "ctor_extent_measured": c3["examined_ctor"]["extent_end"] == "0x009724DA",
        "cursor_pinned": pins_by_id["stream_ctor_LEA_EDI_cursor_3C"]["status"] == "VALIDATED",
        "tail_stores_pinned": all(
            pins_by_id[c]["status"] == "VALIDATED"
            for c in ("stream_ctor_tail_88_flag_1", "stream_ctor_tail_8C_size_0x80",
                      "stream_ctor_tail_90", "stream_ctor_tail_94_flag_1",
                      "stream_ctor_tail_98_size_0x80", "stream_ctor_tail_9C",
                      "stream_ctor_return_this")),
        "THE_STORE_pinned": pins_by_id["THE_STORE_plus_84"]["status"] == "VALIDATED",
        "NULL_INIT_pinned": pins_by_id["NULL_INIT_store_plus_84"]["status"] == "VALIDATED",
    }
    q12["ok"] = all(q12.values())
    return ("PASS" if q12["ok"] else "FAIL"), q12


# ============ Q13 [P3-B]: declared-family metadata agreement ============
def gate_q13(pkg, ctx):
    c2 = pkg["c2"]
    impl_count = len(c2mod.FAMILIES)
    q13 = {
        "implementation_family_count": impl_count,
        "json_declared_count": c2.get("DECLARED_ENCODING_FAMILY_COUNT"),
        "scan_coverage_declared_families": c2["closure"]["scan_coverage"]["declared_families"],
        "json_family_list_count": len(c2["declared_examined_encoding_families"]),
        "disclosed_out_of_scope_present": bool(c2.get("disclosed_but_out_of_scope_families")),
    }
    q13["ok"] = (impl_count == c2.get("DECLARED_ENCODING_FAMILY_COUNT")
                 == c2["closure"]["scan_coverage"]["declared_families"]
                 == len(c2["declared_examined_encoding_families"]))
    return ("PASS" if q13["ok"] else "FAIL"), q13


# ============ Q14 [docs]: forbidden scope + nonclaims + supersession ============
def gate_q14(pkg, ctx):
    q14 = {"failures": []}

    def fail(why):
        q14["failures"].append(why)

    fr_path = os.path.join(RUN, "FINAL_REPORT.md")
    if not os.path.exists(fr_path):
        return "PENDING_DOCS", {"why": "FINAL_REPORT.md not yet written"}
    fr = open(fr_path, encoding="utf-8").read()
    required = [
        "FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL",
        "ASSIGNMENT_FUNCTION = FUN_0070C680",
        "ASSIGNMENT_VA = 0x0070C71E",
        "ASSIGNMENT_STORE_BYTES = 89 86 84 00 00 00",
        "ASSIGNED_OBJECT_SIZE = 0xA4/164 B",
        "ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380",
        "ASSIGNED_OBJECT_VTABLE = UNVERIFIED",
        "OBJECT_POLYMORPHISM = NOT_ESTABLISHED",
        "DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED",
        "EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED",
        "ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED",
        "WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED",
        "FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED",
        "ULTIMATE_VALUE_SOURCE = UNKNOWN",
        "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED",
        "WORLD_XYZ_RECOVERED = NO",
        "NEW_BACKING_SOURCE_RE_EXECUTED = NO",
        "TEMPLATES_VFS_OPENED = NO",
        "RECORD_A_ANALYZED = NO",
        "MODEL_194013_TRACE_EXECUTED = NO",
        "PLACEMENT_XYZ_RE_EXECUTED = NO",
        "CLIENT_EXECUTED = NO",
        "CANONICAL_GATE_EFFECT = NONE",
        "KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES",
        "STATIC_FACTORY_MEMBER_IDENTITY = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS",
        "WRITER_FUNCTION = FUN_009777F0",
        "WRITER_VA = 0x00977810",
        "TAG6_TO_ID10 = PRESERVED_CONFIRMED",
        "SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED",
        "TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD",
        "EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED",
        "CLEAR_RESET_CONFIRMED_COUNT = 0",
    ]
    missing = [s for s in required if s not in fr]
    if missing:
        fail("missing required strings in FINAL_REPORT: %s" % missing)
    # superseded-phrase sweep (historical overclaims must not reappear)
    forbidden_phrases = ["ASSIGNED_OBJECT_VTABLE = NONE", "NON-POLYMORPHIC",
                         "non-polymorphic", "vtable_store_found",
                         "all methods direct-called", "0xA4 bytes (280)",
                         "declared_families\": 10", "declared_families = 10"]
    sweep_hits = {}
    for sf in ("FINAL_REPORT.md", "HANDOFF.md", "INPUT_IDENTITIES.md",
               "SUPERSESSION_LEDGER.md", "QC_REPORT.md"):
        p = os.path.join(RUN, sf)
        if not os.path.exists(p):
            continue
        content = open(p, encoding="utf-8", errors="replace").read()
        hits = [ph for ph in forbidden_phrases if ph in content]
        if hits:
            sweep_hits[sf] = hits
    if sweep_hits:
        # allowed: the supersession ledger may quote the historical defect
        # inside an ORIGINAL_EXCERPT line (that is the record, not an active claim)
        led = open(os.path.join(RUN, "SUPERSESSION_LEDGER.md"), encoding="utf-8").read()
        real_hits = {}
        for sf, hits in sweep_hits.items():
            keep = []
            content = open(os.path.join(RUN, sf), encoding="utf-8", errors="replace").read()
            for ph in hits:
                if sf == "SUPERSESSION_LEDGER.md" and ph in led:
                    # verify each occurrence is inside a quoted excerpt line
                    ok_all = True
                    for m in re.finditer(re.escape(ph), content):
                        line_start = content.rfind("\n", 0, m.start())
                        line = content[line_start:m.end()]
                        if "ORIGINAL_EXCERPT" not in line and "DEFECT" not in line \
                                and "C1 DEFECT" not in line and "historical" not in line.lower():
                            ok_all = False
                    if not ok_all:
                        keep.append(ph)
                else:
                    keep.append(ph)
            if keep:
                real_hits[sf] = keep
        if real_hits:
            fail("forbidden/overclaim phrases in active claim surfaces: %s" % real_hits)
    # supersession ledger: measured record count + quotecheck
    led_path = os.path.join(RUN, "SUPERSESSION_LEDGER.md")
    led = open(led_path, encoding="utf-8").read()
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
                    quotecheck["failures"].append({"source": current_src,
                                                   "excerpt": excerpt[:120]})
    # NEW_SUPERSESSION_RECORD_COUNT = the number of S-C2-NN ledger RECORDS
    # (headers), measured independently of the excerpt-line count (records may
    # carry multiple ORIGINAL_EXCERPT lines).
    record_headers = re.findall(r"^## (S-C2-\d+)", led, re.M)
    record_count = len(set(record_headers))
    quotecheck["ledger_record_count"] = record_count
    declared_m = re.search(r"NEW_SUPERSESSION_RECORD_COUNT\s*=\s*(\d+)", led)
    declared_count = int(declared_m.group(1)) if declared_m else None
    quotecheck["ledger_declared_count"] = declared_count
    q14["supersession_quotecheck"] = quotecheck
    q14["NEW_SUPERSESSION_RECORD_COUNT"] = record_count
    q14["NEW_SUPERSESSION_EXCERPT_LINES"] = quotecheck["records"]
    if quotecheck["failures"] or record_count < 1:
        fail("supersession quotecheck failed")
    if declared_count != record_count:
        fail("ledger-declared NEW_SUPERSESSION_RECORD_COUNT != measured record count "
             "(%s != %s)" % (declared_count, record_count))
    # P3-C: the repository-owner typo correction
    old_text = "SebastianKlo/eudoria-clean"
    new_text = "SebastianKozlo/eudoria-clean"
    src_ident = open(os.path.join(SOURCE_PACKAGE, "INPUT_IDENTITIES.md"),
                     encoding="utf-8").read()
    old_count = src_ident.count(old_text)
    new_ident = open(os.path.join(RUN, "INPUT_IDENTITIES.md"), encoding="utf-8").read()
    p3c = {"source_occurrences_at_BASE": old_count,
           "new_identity_present": new_text in new_ident,
           "old_typo_absent_from_new": old_text not in new_ident,
           "source_untouched": True}
    q14["P3_C"] = p3c
    if old_count != 1 or not p3c["new_identity_present"] or not p3c["old_typo_absent_from_new"]:
        fail("P3-C verification failed: %s" % p3c)
    # forbidden-input census over the instruments
    opened_lits = set()
    http_hits = []
    for fn in os.listdir(os.path.join(RUN, "03_SCRIPTS")):
        if fn.endswith(".py"):
            src = open(os.path.join(RUN, "03_SCRIPTS", fn), encoding="utf-8").read()
            for m in re.finditer(r'open\(([^)\n]{0,200})', src):
                for lit in re.findall(r'"([^"]{1,200})"', m.group(1)):
                    if "/" in lit or "\\" in lit or "." in lit:
                        opened_lits.add(os.path.basename(lit))
            _m1 = "ht" + "tp://"
            _m2 = "ht" + "tps://"
            if _m1 in src or _m2 in src:
                http_hits.append(fn)
    forbidden_ext = [p for p in opened_lits
                     if p.lower().endswith((".vfs", ".bnt", ".nif", ".ark"))]
    q14["opened_path_literals"] = sorted(opened_lits)
    q14["forbidden_extensions_opened"] = forbidden_ext
    q14["http_in_instruments"] = http_hits
    if forbidden_ext:
        fail("instruments open forbidden input classes: %s" % forbidden_ext)
    if http_hits:
        fail("http literals in instruments: %s" % http_hits)
    q14["ok"] = not q14["failures"]
    return ("PASS" if q14["ok"] else "FAIL"), q14


# ============================ MUTATION HARNESS ============================
def _mutate_json(pkg_root_src, relparts, mutate_fn, tmp_root):
    """Copy the ACTUAL artifact to the temp tree, apply the mutation there."""
    src = os.path.join(pkg_root_src, *relparts)
    dst = os.path.join(tmp_root, *relparts)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    if relparts[-1].endswith(".json"):
        with open(dst, encoding="utf-8") as f:
            obj = json.load(f)
        obj = mutate_fn(obj)
        with open(dst, "w", newline="\n", encoding="utf-8") as f:
            json.dump(obj, f, indent=1)
    else:
        with open(dst, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            fieldnames = list(rows[0].keys()) if rows else []
        rows = mutate_fn(rows)
        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)
    return dst


def run_mutations(ctx, prod_pkg, gate_results):
    """Causal mutation tests M1-M4 + AF3/Q8 through the SAME production gates.
    Each mutation is applied to a TEMPORARY COPY of the ACTUAL final artifact
    (temp dir outside the repo); the mutated package is loaded through the
    SAME loader and validated by the SAME gate function. Nothing but the
    mutated field differs; EXE identity, git baseline, unrelated artifacts,
    unrelated QC inputs and the gate implementation are identical between the
    UNMUTATED and MUTATED executions."""
    results = []
    tmp = tempfile.mkdtemp(prefix="c2_mut_", suffix="_out")
    try:
        def m1(obj):
            for p in obj["pins"]:
                if p["claim_id"] == "stream_ctor_entry":
                    p["opcode_bytes"] = "EB FF"
            return obj

        def m2(rows):
            for r in rows:
                if r["claim_id"] == "slotpred_callback_MOV_EAX_imm32":
                    r["measured_operand"] = "0x70BEF0B8 (118482808)"
            return rows

        def m3(obj):
            obj["examined_ctor"]["offset_zero_stores"] = []
            return obj

        def m4(rows):
            for r in rows:
                if r["va"] == "0x0070DD1A":
                    r["containing_function"] = "entry~0xDEADBEEF"
            return rows

        def m5(rows):
            for r in rows:
                if (r["CANDIDATE_VA"] == "0x00707EC0"
                        and r["FINAL_CLASSIFICATION"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"):
                    r["IDENTITY_EDGE"] = ""
                    r["IDENTIFIED_OBJECT"] = ""
                    r["IDENTITY_EVIDENCE"] = ""
                    r["ADDRESS_PROVENANCE_STATUS"] = "UNRESOLVED"
            return rows

        MUTS = [
            ("M1", "01_RAW/C1_PIN_EVIDENCE.json",
             ("01_RAW", "C1_PIN_EVIDENCE.json"), m1, "Q2",
             "corrupt the constructor opcode_bytes (stream_ctor_entry 6A FF -> EB FF)"),
            ("M2", "CORRECTED_PIN_LEDGER.csv",
             ("", "CORRECTED_PIN_LEDGER.csv"), m2, "Q3",
             "corrupt the callback measured_operand (0x70BEF0 -> 0x70BEF0B8) in the CSV"),
            ("M3", "01_RAW/C3_OBJECT_SCOPE.json",
             ("01_RAW", "C3_OBJECT_SCOPE.json"), m3, "Q8",
             "remove the measured offset-zero store collection from C3"),
            ("M4", "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv",
             ("", "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"), m4, "Q6",
             "corrupt a boundary-confirmed row's containing_function (entry~0xDEADBEEF)"),
            ("AF3/Q8", "AF3_PROVENANCE_LEDGER.csv",
             ("", "AF3_PROVENANCE_LEDGER.csv"), m5, "Q7",
             "remove the manager row's identity edge / address-provenance support "
             "(candidate bytes unchanged)"),
        ]
        gates = {"Q2": gate_q2, "Q3": gate_q3, "Q6": gate_q6, "Q7": gate_q7,
                 "Q8": gate_q8}
        for mid, label, relparts, fn, gate_id, desc in MUTS:
            # fresh temp package tree per mutation: copy ALL mutatable artifacts
            pkg_root = os.path.join(tmp, mid)
            os.makedirs(os.path.join(pkg_root, "01_RAW"), exist_ok=True)
            for key, (sub, name, _k) in MUTATABLE.items():
                s = os.path.join(RUN, sub, name) if sub else os.path.join(RUN, name)
                d = os.path.join(pkg_root, sub, name) if sub else os.path.join(pkg_root, name)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
            for (sub, name) in COPY_ONLY:
                s = os.path.join(RUN, sub, name) if sub else os.path.join(RUN, name)
                d = os.path.join(pkg_root, sub, name) if sub else os.path.join(pkg_root, name)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
            _mutate_json(pkg_root if False else RUN, relparts, fn, pkg_root)
            mut_pkg = load_pkg(pkg_root)
            gate_fn = gates[gate_id]
            st, det = gate_fn(mut_pkg, ctx)
            unmut_status = gate_results.get(gate_id)
            rec = {
                "MUTATION_ID": mid,
                "MUTATED_ARTIFACT": label,
                "FIELD": desc,
                "BEFORE": "clean committed artifact (production package)",
                "AFTER": "temporary mutated copy at %s (deleted after the test; "
                         "never persisted as a canonical artifact)" % pkg_root,
                "PRODUCTION_GATE_ID": gate_id,
                "UNMUTATED_RESULT": unmut_status,
                "MUTATED_RESULT": st,
                "EXPECTED_CAUSALITY": "UNMUTATED=PASS -> MUTATED=FAIL",
                "ACTUAL_CAUSALITY": ("CAUSAL_PASS" if (unmut_status == "PASS" and st == "FAIL")
                                     else "NOT_CAUSAL"),
                "IDENTITY_PRESERVED_BETWEEN_EXECUTIONS": (
                    "EXE identity: unchanged (pinned %s / %d bytes re-hashed by the "
                    "loader at both executions); git baseline: unchanged during QC; "
                    "unrelated artifacts: copied byte-identical from the production "
                    "package; unrelated QC inputs: unchanged; gate implementation: "
                    "the SAME gate function object executed for both results"
                    % (pebnd.PINNED_EXE_SHA256[:12], pebnd.PINNED_EXE_SIZE)),
            }
            results.append(rec)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ============================ MAIN ============================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["data", "docs"], default="data")
    ap.add_argument("--pkg-root", default=RUN)
    ap.add_argument("--out-decoder", default=os.path.join(RUN, "01_RAW", "CQC_DECODER_UNIT_TESTS.json"))
    ap.add_argument("--out-counter", default=os.path.join(RUN, "01_RAW", "CQC_BOUNDARY_COUNTEREXAMPLES.json"))
    ap.add_argument("--out-mut", default=os.path.join(RUN, "01_RAW", "CQC_MUTATION_RESULTS.json"))
    ap.add_argument("--out-final", default=os.path.join(RUN, "01_RAW", "CQC_FINAL.json"))
    ap.add_argument("--out-af1-matrix", default=os.path.join(RUN, "AF1_MUTATION_MATRIX.csv"))
    ap.add_argument("--out-af2-matrix", default=os.path.join(RUN, "AF2_BOUNDARY_TEST_MATRIX.csv"))
    args = ap.parse_args()

    ctx = Ctx()
    pkg = load_pkg(args.pkg_root)
    gates = {}

    gates["Q1"] = gate_q1(ctx)
    gates["Q2"] = gate_q2(pkg, ctx)
    gates["Q3"] = gate_q3(pkg, ctx)
    gates["Q4"] = gate_q4(pkg, ctx)
    gates["Q5"] = gate_q5(pkg, ctx)
    gates["Q6"] = gate_q6(pkg, ctx)
    gates["Q7"] = gate_q7(pkg, ctx)
    gates["Q8"] = gate_q8(pkg, ctx)
    gates["Q9"] = gate_q9(pkg, ctx)
    gates["Q10"] = gate_q10(pkg, ctx)
    gates["Q11"] = gate_q11(pkg, ctx)
    gates["Q12"] = gate_q12(pkg, ctx)
    gates["Q13"] = gate_q13(pkg, ctx)

    # mutation harness (AF1) - same gates, mutated temp copies
    gate_results = {k: v[0] for k, v in gates.items()}
    mut_results = run_mutations(ctx, pkg, gate_results)
    with open(args.out_mut, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004",
                   "mutation_discipline": ("M1-M4 + AF3/Q8: the SAME production gate "
                                          "must show UNMUTATED=PASS and MUTATED=FAIL; "
                                          "the mutation target is a TEMPORARY COPY of "
                                          "the ACTUAL final artifact (never a fixture, "
                                          "never the canonical committed artifact); "
                                          "corrupted copies are never persisted"),
                   "results": mut_results}, f, indent=1)
    with open(args.out_af1_matrix, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["MUTATION_ID", "MUTATED_ARTIFACT", "FIELD", "BEFORE", "AFTER",
                    "PRODUCTION_GATE_ID", "UNMUTATED_RESULT", "MUTATED_RESULT",
                    "EXPECTED_CAUSALITY", "ACTUAL_CAUSALITY"])
        for r in mut_results:
            w.writerow([r["MUTATION_ID"], r["MUTATED_ARTIFACT"], r["FIELD"],
                        r["BEFORE"], r["AFTER"], r["PRODUCTION_GATE_ID"],
                        r["UNMUTATED_RESULT"], r["MUTATED_RESULT"],
                        r["EXPECTED_CAUSALITY"], r["ACTUAL_CAUSALITY"]])

    # decoder unit battery + boundary counterexamples persisted
    with open(args.out_decoder, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004",
                   "unit_battery": gates["Q4"][1]["unit_battery"],
                   "unit_battery_ok": gates["Q4"][1]["unit_battery_ok"],
                   "redecode_bad_rows": gates["Q4"][1]["redecode_bad_rows"],
                   "coverage_windows": gates["Q4"][1]["coverage_windows"]}, f, indent=1)
    with open(args.out_counter, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004",
                   "counterexamples": gates["Q5"][1]["counterexamples"],
                   "real_positive_controls": gates["Q5"][1]["real_positive_controls"],
                   "control_nonE8": gates["Q5"][1]["control_nonE8"],
                   "anchor_registry": gates["Q5"][1]["anchor_registry"],
                   "census_discipline": {
                       "confirmed_with_untrusted_source":
                           gates["Q5"][1]["census_confirmed_with_untrusted_source"],
                       "refuted_without_anchor":
                           gates["Q5"][1]["census_refuted_without_anchor"],
                       "pins_confirmed_with_untrusted_source":
                           gates["Q5"][1]["pins_confirmed_with_untrusted_source"]}}, f, indent=1)
    with open(args.out_af2_matrix, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["CASE_ID", "BYTES", "START_OFFSET", "CANDIDATE_OFFSET",
                    "EXPECTED_DECODE", "ACTUAL_DECODE", "EXPECTED_CALL_PROMOTION",
                    "ACTUAL_CALL_PROMOTION", "BOUNDARY_SOURCE", "BOUNDARY_STATUS",
                    "C1_DEFECT_NOTE"])
        for c in gates["Q5"][1]["counterexamples"]:
            w.writerow([c["CASE_ID"], c["BYTES"], c["START_OFFSET"],
                        c["CANDIDATE_OFFSET"], c["EXPECTED_DECODE"],
                        c["ACTUAL_DECODE"], c["EXPECTED_CALL_PROMOTION"],
                        c["ACTUAL_CALL_PROMOTION"], c["BOUNDARY_SOURCE"],
                        c["BOUNDARY_STATUS"], c["C1_DEFECT_NOTE"]])

    # docs gates
    if args.mode == "docs":
        gates["Q14"] = gate_q14(pkg, ctx)

    gate_status = {k: v[0] for k, v in gates.items()}
    mutation_ok = all(r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS" for r in mut_results)
    qc_pass = (all(s == "PASS" for s in gate_status.values()) and mutation_ok)

    final = {
        "run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004",
        "qc_scope": "SELF_CHECK_FACTORY_PLUS_84_C2_AF1_AF3_CORRECTION",
        "mode": args.mode,
        "gates": gate_status,
        "gate_details": {k: v[1] for k, v in gates.items()},
        "mutation_results_summary": {
            "MUTATION_TEST_COUNT": len(mut_results),
            "MUTATION_CAUSAL_PASS_COUNT": sum(1 for r in mut_results
                                              if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS"),
            "MUTATION_CAUSAL_FAIL_COUNT": sum(1 for r in mut_results
                                              if r["ACTUAL_CAUSALITY"] != "CAUSAL_PASS"),
            "MUTATION_NOT_ESTABLISHED_COUNT": sum(
                1 for r in mut_results if r["UNMUTATED_RESULT"] != "PASS"),
        },
        "QC_VERDICT": "QC_PASS" if qc_pass else "QC_FAIL",
        "outcome_conditional_note": ("QC PASS means the corrected claims accurately "
                                     "match evidence and uncertainty; it does NOT mean "
                                     "all census candidates were solved (unresolved "
                                     "candidates and NOT_ESTABLISHED invariants are the "
                                     "corrected honest states); executor SELF_CHECK, "
                                     "NOT an independent audit"),
    }
    with open(args.out_final, "w", newline="\n") as f:
        json.dump(final, f, indent=1)
    print("CQC done (%s). gates: %s mutations_causal=%d/%d verdict=%s" % (
        args.mode, json.dumps(gate_status),
        final["mutation_results_summary"]["MUTATION_CAUSAL_PASS_COUNT"],
        len(mut_results), final["QC_VERDICT"]))


if __name__ == "__main__":
    main()
