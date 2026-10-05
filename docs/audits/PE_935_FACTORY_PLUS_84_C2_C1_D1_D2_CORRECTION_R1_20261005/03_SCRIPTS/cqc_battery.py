# cqc_battery.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# Fresh production QC for the D1/D2 correction package (Desktop post-audit
# PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005, verdict REQUIRE_CORRECTIONS,
# findings D1/P2 + D2/P2; the THREE-P2 repairs P2-1/P2-2/P2-3/H1/H2 are
# PRESERVED and reproduced as controls).
#
# THIS RUN'S REPAIRS vs the THREE-P2 battery:
#   D1 (decoder, in x86dec.py - this battery MEASURES it): 0F 73 /4 accepted
#      by the shared {2,4,6} reg whitelist in both MMX and SSE2 forms.
#      The corrected decoder uses PER-OPCODE legal-reg tables (0F 71/72:
#      {2,4,6}/{2,4,6}; 0F 73: {2,6}/{2,3,6,7}). This battery adds the two
#      D1 negative unit vectors (`0F 73 E0 02`, `66 0F 73 E0 02` -> REJECT),
#      the six contract legal controls, and the MANDATORY downstream
#      falsifier `0F 73 E0 02 E8 05 00 00 00 C3` with a synthetic strong
#      entry at the first byte: the invalid initial instruction must STOP
#      justified sequential decoding, so the E8 at +4 must NOT receive
#      CALL_VALIDATION=PASS or a promoted target. The THREE-P2 defect is
#      reproduced BEFORE/AFTER through the committed BASE modules
#      (READ-ONLY import; measured in 01_RAW/D1_BOUNDARY_FALSIFIER.json).
#   D2 (gate_q2, HERE): the THREE-P2 Q2 iterated only the JSON's supplied
#      pins, decided EA applicability solely from the mutable JSON field
#      `pin.kind == 'mem'`, and trusted `pin_totals.fail_count == 0` - so a
#      relabelled kind, a removed EA object, a DELETED load-bearing pin or a
#      DUPLICATED/EXTRA claim all still passed. CORRECTED Q2 binds the
#      expected pin universe to the BASE-pinned
#      03_SCRIPTS/c1_pin_ledger.py::PINS roster, re-extracted IN-RUN from
#      the BASE Git blob (ast literal evaluation - no historical code is
#      executed; see pin_roster.py), and requires:
#        * JSON claim multiset == CSV claim multiset == expected roster
#          multiset (each expected claim EXACTLY ONCE; missing/extra/
#          duplicate = FAIL - bidirectional, not count-only);
#        * claim_id + instruction_va + declared kind(role) agreement with
#          the roster per claim (role mapping explicit against PINS, never
#          derived from the checked artifacts);
#        * declared totals agreement: pin_totals.total_pins == roster
#          cardinality == measured JSON/CSV row counts; status_tally ==
#          the CSV-recomputed tally; fail_count == 0 (carried);
#        * EA applicability derived from the EXPECTED role (kind mutation
#          FAILS the role check AND cannot disable EA validation);
#        * the persisted EXPECTED_PIN_REGISTRY.json must equal the
#          in-run git-derived roster (registry tamper = FAIL);
#        * the EXE-derived EA is additionally cross-checked against the
#          roster's pinned expect_ea spec (base/index/scale/displacement).
#      The carried effective_address EXE re-derivation (46 mem pins,
#      M5/M6 detection, missing-EA rejection) is preserved verbatim.
#   D2 (gate_q3, HERE): the CSV operand_kind is no longer trusted as a
#      role oracle - Q3 verifies every row's operand_kind against the
#      EXE-derived kind (generator convention: imm overrides the mem class
#      for mem+imm forms) and checks row membership/VA against the roster.
#   Mutations: the inherited M1/M2/M3/M4 + AF3/Q8 (compound) + M5/M6 are
#   RETAINED (7 causal controls, each UNMUTATED=PASS -> MUTATED=FAIL
#   through the SAME production gate) + 8 NEW D2 completeness controls
#   (D2-M1..D2-M8: the two mandatory compound kind+EA removals, the two
#   whole-pin deletions, the JSON duplicate, the JSON extra, the CSV extra
#   and the synchronized JSON+CSV omission with adjusted declared totals -
#   all must flip clean Q2 PASS -> mutated Q2 FAIL with no substitute
#   failure; exact semantic deltas, before/after artifact hashes and
#   per-mutation input-hash censuses persisted).
#   NEW-F/NEW-G/REAL-REFUTE boundary fixtures (incl. the order-permutation
#   proofs and the cached+uncached crosscheck) are REPRODUCED unchanged.
#
# AF1 REPAIR vs the C1 battery (Desktop post-audit finding AF1/P2): the C1
# battery tested its own synthetic constants (CONTROL A/D fixtures) and did not
# validate the ACTUAL committed artifacts' load-bearing fields (C1 JSON
# opcode_bytes, CSV measured_operand, C3 store collection, census boundary
# anchors were all mutable without detection). THIS battery validates the
# actual generated package artifacts against fresh EXE re-derivation:
#   Q2  C1 pin JSON integrity vs EXE re-derivation INCL. effective_address
#       [M1 + M5 + M6 mutation gates]
#   Q3  pin CSV full-row re-derivation (measured_operand incl.)  [M2 gate]
#   Q4  decoder unit battery (corrected length rules) + census re-decode
#   Q5  AF2 boundary counterexamples A-E + NEW-F/NEW-G + REAL-REFUTE +
#       coverage-order permutation proofs + census boundary discipline
#   Q6  census boundary-anchor integrity per row  [M4 gate]
#   Q7  AF3 provenance discipline + ledger/census identity chains  [AF3 gate]
#   Q8  P3-A segment-semantics store census re-derivation  [M3 gate]
#   Q9  census arithmetic re-summed from the emitted CSV
#   Q10 known stores physical re-pin
#   Q11 factory identity/enumeration from measured evidence (+ CONTROL B)
#   Q12 object structural identity
#   Q13 P3-B declared-family metadata agreement (derived, not hard-coded)
#   Q14 forbidden scope + nonclaims + supersession quotecheck (docs mode)
#   MUT  causal mutation harness: a TEMPORARY COPY of the ACTUAL final
#        artifact is mutated on disk (temp dir outside the repo) and routed
#        through the SAME production gate; UNMUTATED=PASS and MUTATED=FAIL
#        is required for causality. No corrupted copy is persisted as a
#        canonical artifact; only before/after values + causal results.
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
import importlib.util
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402
import c2_census as c2mod  # noqa: E402  (family table import for P3-B)
import pin_roster  # noqa: E402  (D2: the expected pin universe, BASE-pinned)

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")
SOURCE_PACKAGE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
                  r"\PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005")
C1_PACKAGE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
              r"\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "9d31a82b6589f46e9ca6c75c6e323b433c1ebf92"
EXPECTED_PIN_REGISTRY = os.path.join(RUN, "EXPECTED_PIN_REGISTRY.json")
BASE_COMMIT_MESSAGE_VERBATIM = os.path.join(RUN, "01_RAW", "BASE_COMMIT_MESSAGE_VERBATIM.txt")

# P2-3: the EXACT field set the corrected gate_q2 covers for the JSON pins'
# effective_address object (the C2 "re-derives every C1-JSON pin field" and
# "re-derived field-by-field" wordings are superseded; a JSON pin field
# outside this set is NOT claimed as validated by Q2).
Q2_EFFECTIVE_ADDRESS_COVERAGE = (
    "effective_address present/memop state (D2: required iff the EXPECTED "
    "ROSTER role is mem AND the EXE decode at the pin VA succeeds with "
    "memop=True; must be ABSENT otherwise - applicability is driven by the "
    "pinned expected role, never by the mutable JSON kind); operand_width; "
    "segment; base_register; index_register; scale; raw_displacement "
    "(displacement width enforced through the NONE-vs-value derivation; "
    "derived width recorded per pin); signed_displacement; "
    "effective_displacement; address_provenance_status (EXE decode + "
    "boundary/function context: entry this-flow); PLUS the D2 spec "
    "cross-check of the EXE-derived EA against the roster's pinned "
    "expect_ea (base/index/scale/displacement)"
)

# D2: the pin-universe coverage of the corrected gate Q2 (the Desktop D2
# defect: the THREE-P2 Q2 iterated only the JSON's supplied pins, decided
# EA applicability from the mutable JSON kind, and trusted the declared
# fail_count - a removed load-bearing pin, a relabelled kind or a
# duplicated claim all passed).
Q2_PIN_UNIVERSE_COVERAGE = (
    "expected roster = BASE-pinned 03_SCRIPTS/c1_pin_ledger.py::PINS "
    "(Git blob of BASE_SHA, ast literal extraction - no historical code "
    "executed; re-derived IN-RUN by pin_roster.expected_from_git(), never "
    "taken from the checked artifacts); JSON claim multiset == CSV claim "
    "multiset == expected roster multiset (each expected claim EXACTLY "
    "ONCE; missing/extra/duplicate = FAIL, bidirectional); claim_id + "
    "instruction_va + declared kind(role) agreement per claim; declared "
    "totals agreement (total_pins == roster cardinality == measured JSON "
    "count == measured CSV count; status_tally == CSV-recomputed tally; "
    "fail_count == 0); EA applicability from the EXPECTED role; "
    "EXPECTED_PIN_REGISTRY.json == git-derived roster (registry tamper = FAIL)"
)

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


# ============ Q2 [M1 + M5 + M6 + D2]: pin JSON integrity + D2 pin universe ============
def gate_q2(pkg, ctx):
    """D2-CORRECTED Q2. Binds the expected pin universe to the BASE-pinned
    PINS roster (re-derived IN-RUN from the BASE Git blob by pin_roster - no
    historical code executed) BEFORE any per-pin derivation: missing/extra/
    duplicate claims, address/role disagreements, declared-total
    disagreements and EXPECTED_PIN_REGISTRY tamper all FAIL independently,
    and the carried EXE re-derivation (opcode_bytes, instruction_length,
    boundary_status/source, effective_address for every EXPECTED mem-role
    pin - the established Q2/Q3 pattern, NOT a JSON-to-JSON comparison) is
    preserved. EA applicability is decided by the EXPECTED role, so a
    mutated JSON kind can neither pass the role check nor disable EA
    validation. Secondary consistency: JSON EA fields vs the CSV row's
    separately-serialized measured_operand."""
    q2 = {"json_pins": len(pkg["c1"]["pins"]), "mismatches": [],
          "json_csv_inconsistencies": [],
          "effective_address_coverage": Q2_EFFECTIVE_ADDRESS_COVERAGE,
          "pin_universe_coverage": Q2_PIN_UNIVERSE_COVERAGE,
          "ea_pins_checked": 0, "derived_ea_pins": 0,
          "d2_pin_universe": {}}
    # ---- D2: the expected roster, re-derived in-run from the BASE Git blob ----
    try:
        roster = pin_roster.expected_from_git()
    except Exception as e:  # fail-closed: no roster -> every claim unverifiable
        q2["mismatches"].append({"claim": "<ROSTER>", "field": "expected_roster",
                                 "json": "UNAVAILABLE", "derived": str(e)})
        roster = {}
    q2["d2_roster_source"] = pin_roster.roster_identity() if roster else None
    q2["d2_pin_universe"]["expected_claims"] = len(roster)
    # the persisted EXPECTED_PIN_REGISTRY.json must EQUAL the git-derived roster
    if os.path.exists(EXPECTED_PIN_REGISTRY):
        try:
            with open(EXPECTED_PIN_REGISTRY, encoding="utf-8") as f:
                reg_on_disk = json.load(f)
        except Exception as e:
            reg_on_disk = None
            q2["mismatches"].append({"claim": "<REGISTRY>",
                                     "field": "EXPECTED_PIN_REGISTRY.json",
                                     "json": "unreadable", "derived": str(e)})
        if reg_on_disk is not None:
            reg_pins = {p.get("claim_id"): p for p in reg_on_disk.get("pins", [])}
            if set(reg_pins) != set(roster):
                q2["mismatches"].append({"claim": "<REGISTRY>",
                                        "field": "registry claim set",
                                        "json": sorted(set(reg_pins) ^ set(roster))[:8],
                                        "derived": "registry == git-derived roster"})
            else:
                for rcid, rex in roster.items():
                    rp = reg_pins[rcid]
                    rv = rp.get("va")
                    rv = int(rv, 16) if isinstance(rv, str) else rv
                    if rv != rex["va"] or rp.get("role") != rex["role"]:
                        q2["mismatches"].append({"claim": rcid,
                                                "field": "registry va/role",
                                                "json": (rp.get("va"), rp.get("role")),
                                                "derived": ("0x%08X" % rex["va"], rex["role"])})
    else:
        q2["mismatches"].append({"claim": "<REGISTRY>",
                                 "field": "EXPECTED_PIN_REGISTRY.json",
                                 "json": "MISSING",
                                 "derived": "required (D2 roster artifact)"})
    # ---- D2: bidirectional claim multiset checks (JSON + CSV) ----
    json_ids = [p.get("claim_id") for p in pkg["c1"]["pins"]]
    json_counter = Counter(json_ids)
    dup_json = sorted([c for c, n in json_counter.items() if n > 1])
    missing_json = sorted(set(roster) - set(json_counter))
    extra_json = sorted(set(json_counter) - set(roster))
    csv_ids = [r.get("claim_id") for r in pkg["pins"]]
    csv_counter = Counter(csv_ids)
    dup_csv = sorted([c for c, n in csv_counter.items() if n > 1])
    missing_csv = sorted(set(roster) - set(csv_counter))
    extra_csv = sorted(set(csv_counter) - set(roster))
    uni = q2["d2_pin_universe"]
    uni.update({"json_claim_count": len(json_ids),
                "csv_claim_count": len(csv_ids),
                "json_duplicates": dup_json, "json_missing": missing_json,
                "json_extra": extra_json, "csv_duplicates": dup_csv,
                "csv_missing": missing_csv, "csv_extra": extra_csv})
    if dup_json:
        q2["mismatches"].append({"claim": dup_json[0],
                                 "field": "pin claim multiplicity (JSON)",
                                 "json": "DUPLICATE claim_id",
                                 "derived": "each expected claim EXACTLY ONCE"})
    if missing_json:
        q2["mismatches"].append({"claim": missing_json[0],
                                 "field": "pin presence (JSON)",
                                 "json": "MISSING",
                                 "derived": "expected roster requires this claim"})
    if extra_json:
        q2["mismatches"].append({"claim": extra_json[0],
                                 "field": "pin presence (JSON)",
                                 "json": "EXTRA (not in the expected roster)",
                                 "derived": "no claim outside the roster"})
    if dup_csv:
        q2["mismatches"].append({"claim": dup_csv[0],
                                 "field": "pin claim multiplicity (CSV)",
                                 "json": "DUPLICATE claim_id",
                                 "derived": "each expected claim EXACTLY ONCE"})
    if missing_csv:
        q2["mismatches"].append({"claim": missing_csv[0],
                                 "field": "pin presence (CSV)",
                                 "json": "MISSING",
                                 "derived": "CSV claim multiset == expected roster"})
    if extra_csv:
        q2["mismatches"].append({"claim": extra_csv[0],
                                 "field": "pin presence (CSV)",
                                 "json": "EXTRA (not in the expected roster)",
                                 "derived": "CSV claim multiset == expected roster"})
    # ---- D2: declared totals agreement (measured, not trusted) ----
    declared = pkg["c1"].get("pin_totals") or {}
    uni["declared_total_pins"] = declared.get("total_pins")
    uni["declared_fail_count"] = declared.get("fail_count")
    if declared.get("total_pins") != len(roster):
        q2["mismatches"].append({"claim": "<TOTALS>",
                                 "field": "pin_totals.total_pins",
                                 "json": declared.get("total_pins"),
                                 "derived": len(roster)})
    if declared.get("fail_count") != 0:
        q2["mismatches"].append({"claim": "<TOTALS>",
                                 "field": "pin_totals.fail_count",
                                 "json": declared.get("fail_count"), "derived": 0})
    measured_tally = Counter(r["status"] for r in pkg["pins"])
    declared_tally = declared.get("status_tally") or {}
    uni["measured_csv_status_tally"] = dict(measured_tally)
    if {k: int(v) for k, v in declared_tally.items()} != dict(measured_tally):
        q2["mismatches"].append({"claim": "<TOTALS>",
                                 "field": "pin_totals.status_tally",
                                 "json": declared_tally,
                                 "derived": dict(measured_tally)})
    csv_by_id = {p["claim_id"]: p for p in pkg["pins"]}
    for pin in pkg["c1"]["pins"]:
        cid = pin["claim_id"]
        expected = roster.get(cid)
        if expected is None:
            continue  # an extra claim: already recorded by the multiset check
        exp_role = expected["role"]
        va = expected["va"]
        if int(pin.get("instruction_va", "0x0"), 16) != va:
            q2["mismatches"].append({"claim": cid, "field": "instruction_va",
                                     "json": pin.get("instruction_va"),
                                     "derived": "0x%08X" % va})
        if pin.get("kind") != exp_role:
            q2["mismatches"].append({"claim": cid,
                                     "field": "kind (role vs EXPECTED roster)",
                                     "json": pin.get("kind"), "derived": exp_role})
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
        # ---- D2/P2-3: effective_address re-derivation (M5/M6 detection);
        # applicability is decided by the EXPECTED roster role (never by the
        # mutable JSON kind: a kind mutation FAILS the role check above AND
        # cannot disable the EA validation here) ----
        ea_required = (exp_role == "mem")
        if ea_required:
            q2["ea_pins_checked"] += 1
        if ea_required and ins is None:
            q2["mismatches"].append({"claim": cid, "field": "effective_address",
                                     "json": "present",
                                     "derived": "UNDECODABLE - required re-derivation impossible"})
        elif ea_required and not ins.memop:
            q2["mismatches"].append({"claim": cid, "field": "effective_address",
                                     "json": pin.get("effective_address"),
                                     "derived": "kind=mem but EXE decode has no memory operand"})
        elif ea_required:
            ea = pin.get("effective_address")
            if not isinstance(ea, dict):
                q2["mismatches"].append({"claim": cid, "field": "effective_address",
                                         "json": ea,
                                         "derived": "REQUIRED (semantically applicable, missing)"})
            else:
                q2["derived_ea_pins"] += 1
                derived_ea = {
                    "operand_width": 32 if not ins.has66 else 16,
                    "segment": ins.segment,
                    "base_register": x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else None,
                    "index_register": x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else None,
                    "scale": ins.ea_scale,
                    "raw_displacement": ("0x%08X" % ins.disp_raw) if ins.disp_width else "NONE",
                    "signed_displacement": ins.disp_signed if ins.disp_width else 0,
                    "effective_displacement": ins.disp_signed if ins.disp_width else 0,
                }
                # address_provenance_status: independently re-derived from the
                # EXE + boundary/function context (entry this-flow)
                derived_ea["address_provenance_status"] = ctx.pin_provenance(
                    ins, bstatus, bsrc, bstart)
                # D2 spec cross-check: the EXE-derived EA must ALSO agree
                # with the roster's pinned expect_ea spec (base/index/scale/
                # displacement) - the expected roster binds the artifacts,
                # the EXE binds the physics; a disagreement of EITHER side
                # is a FAIL, never silently resolved
                spec = expected.get("expect_ea")
                if spec is not None:
                    eb, ei, esc, ed = spec
                    if eb is None and ei is None:
                        spec_ok = (ins.ea_base is None and ins.ea_index is None
                                   and ins.disp_raw == ed)
                    else:
                        spec_ok = (derived_ea["base_register"] == eb
                                   and derived_ea["index_register"] == ei
                                   and ins.ea_scale == esc
                                   and ins.disp_signed == ed)
                    if not spec_ok:
                        q2["mismatches"].append(
                            {"claim": cid,
                             "field": "effective_address vs roster expect_ea spec",
                             "json": "EXE-derived EA %s" % derived_ea,
                             "derived": "pinned spec %s" % (spec,)})
                for fld, dval in derived_ea.items():
                    if fld not in ea:
                        q2["mismatches"].append({"claim": cid, "field": "effective_address." + fld,
                                                 "json": "MISSING (semantically required)",
                                                 "derived": dval})
                    elif ea[fld] != dval:
                        q2["mismatches"].append({"claim": cid,
                                                 "field": "effective_address." + fld,
                                                 "json": ea[fld], "derived": dval})
        else:
            # not semantically applicable (EXPECTED role != mem): the pin must
            # NOT carry an EA object
            if "effective_address" in pin:
                q2["mismatches"].append({"claim": cid, "field": "effective_address",
                                         "json": "present",
                                         "derived": "NOT APPLICABLE (expected role=%s "
                                                    "per the roster; JSON kind=%s)"
                                                    % (exp_role, pin.get("kind"))})
        # JSON <-> CSV consistency for the same claim
        row = csv_by_id.get(cid)
        if row is None:
            q2["json_csv_inconsistencies"].append({"claim": cid, "why": "no CSV row"})
            continue
        if row["opcode_bytes"] != (pin.get("opcode_bytes") or ""):
            q2["json_csv_inconsistencies"].append({"claim": cid, "field": "opcode_bytes"})
        if row["boundary_status"] != (pin.get("boundary_status") or ""):
            q2["json_csv_inconsistencies"].append({"claim": cid, "field": "boundary_status"})
        # P2-3 secondary consistency: JSON EA fields vs the CSV row's
        # separately-serialized measured_operand representation. Only the
        # CSV rows that actually CARRY the EA representation participate
        # ("base=...;index=...;prov=..." pipe form): mem+imm pins (C7/C6
        # stores, etc.) serialize the IMMEDIATE form in measured_operand by
        # the generator's design (their operand_kind is the imm class), so
        # the CSV provides no EA representation for them - their JSON EA is
        # still fully validated against the EXE decode by the primary check.
        if ea_required and isinstance(pin.get("effective_address"), dict) \
                and "measured_operand" in row:
            mo = row["measured_operand"]
            jea = pin["effective_address"]
            if "base=" in mo:
                for fld, needle in (
                        ("base_register", "base=%s;" % jea.get("base_register")),
                        ("index_register", "index=%s;" % jea.get("index_register")),
                        ("scale", "scale=%s;" % jea.get("scale")),
                        ("raw_displacement", "raw=%s;" % jea.get("raw_displacement")),
                        ("signed_displacement", "signed=%s;" % jea.get("signed_displacement")),
                        ("effective_displacement", "effective=%s;" % jea.get("effective_displacement")),
                        ("address_provenance_status", "prov=%s" % jea.get("address_provenance_status"))):
                    if needle not in mo:
                        q2["json_csv_inconsistencies"].append(
                            {"claim": cid, "field": "effective_address.%s vs CSV measured_operand" % fld,
                             "json": needle, "csv": mo})
    q2["ok"] = (not q2["mismatches"] and not q2["json_csv_inconsistencies"]
                and declared.get("fail_count") == 0
                and len(json_ids) == len(roster) and len(csv_ids) == len(roster))
    return ("PASS" if q2["ok"] else "FAIL"), q2


# ============ Q3 [M2]: pin CSV full-row re-derivation ============
def gate_q3(pkg, ctx):
    q3 = {"rows": len(pkg["pins"]), "mismatches": []}

    def mm(cid, field, got, exp):
        q3["mismatches"].append({"claim": cid, "field": field,
                                 "csv": got, "derived": exp})

    # D2: the CSV operand_kind is no longer a trusted role oracle - every
    # row's kind is re-derived from the EXE decode (generator convention:
    # an immediate OVERRIDES the mem class for mem+imm forms such as
    # C7/C6/83 stores; a mem pin with disp serializes mem32/mem8/mem0;
    # call rows are rel32; declassified rows carry no operand claim) and
    # cross-checked against the EXPECTED roster role.
    q3_roster = pin_roster.expected_from_git()

    def derived_operand_kind(ins, role):
        if role == "call":
            return "rel32"
        if role == "declassified":
            return "none"
        if ins is None:
            return None
        if ins.imm_width:
            return "imm%d" % (ins.imm_width * 8)
        if ins.memop:
            if ins.disp_width == 4:
                return "mem32"
            if ins.disp_width == 1:
                return "mem8"
            return "mem0"
        return "none"

    for p in pkg["pins"]:
        cid = p["claim_id"]
        va = int(p["instruction_va"], 16)
        off = va - ctx.tva
        ins = x86dec.decode(ctx.text, off) if 0 <= off < len(ctx.text) else None
        # ---- D2: roster membership + VA agreement + EXE-derived kind ----
        exp3 = q3_roster.get(cid)
        if exp3 is None:
            mm(cid, "claim_id (roster membership)", cid,
               "no CSV claim outside the expected roster")
        else:
            if va != exp3["va"]:
                mm(cid, "instruction_va (roster agreement)",
                   p["instruction_va"], "0x%08X" % exp3["va"])
            dk = derived_operand_kind(ins, exp3["role"])
            if dk is not None and p["operand_kind"] != dk:
                mm(cid, "operand_kind (EXE-derived)", p["operand_kind"], dk)
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
    # ---- P2-2 (BRANCH A): 66 0F 8x near Jcc rel16 (independently oracle-checked
    # vs GNU objdump Binutils 2.44; the C2 table measured 7 for the rel16 form
    # and fabricated a CALL edge from interior data - Desktop NEW-G) ----
    ("0F 84 00 00 00 00 90", 6, "P2-2: ordinary 0F 84 rel32 near Jcc (unprefixed) = 6 bytes"),
    ("66 0F 84 00 00 90", 5, "P2-2 branch A: 66 0F 84 rel16 near Jcc = 5 bytes (C2 measured 7; objdump je rel16 5)"),
    ("66 0F 8F 00 00 90", 5, "P2-2 branch A: 66 0F 8F rel16 (JG) = 5 bytes - whole 0x80..0x8F class"),
    ("67 0F 84 00 00 00 00", "REJECT", "P2-2: 67-prefixed near Jcc -> fail-closed reject (same policy as 67 E8/E9)"),
    # ---- H1: 16-bit addressing rm table (oracle-checked; lengths unchanged by
    # the repair - base register naming only) ----
    ("67 8B 07 90", 3, "H1: 67 8B 07 = MOV EAX,[BX] (rm=7 mod=0 is [BX], C2 wrongly said [BP])"),
    ("67 8B 47 05 90", 4, "H1: 67 8B 47 05 = MOV EAX,[BX+0x5] (rm=7 mod=1 is [BX+disp])"),
    ("67 8B 46 05 90", 4, "H1: 67 8B 46 05 = MOV EAX,[BP+0x5] (rm=6 mod!=0 is [BP+disp])"),
    ("67 8B 06 34 12 90", 5, "H1: 67 8B 06 disp16 = MOV EAX,[0x1234] (rm=6 mod=0 absolute)"),
    # ---- H2: grouped-opcode validity (oracle-checked; reserved/invalid
    # sub-opcodes REJECT fail-closed, legal imm8 forms decode) ----
    ("0F BA E0 05 90", 4, "H2 positive: 0F BA /4 BT EAX,imm8 (reg 4..7 legal)"),
    ("0F BA 6D 00 05 90", 5, "H2 positive: 0F BA /5 BTS [EBP+0],imm8 (memory forms legal for 0F BA)"),
    ("0F BA C0 05 90", "REJECT", "H2 negative: 0F BA /0 reserved -> fail-closed"),
    ("0F BA C1 05 90", "REJECT", "H2 negative: 0F BA /1 reserved -> fail-closed"),
    ("0F BA C2 05 90", "REJECT", "H2 negative: 0F BA /2 reserved -> fail-closed"),
    ("0F BA C3 05 90", "REJECT", "H2 negative: 0F BA /3 reserved -> fail-closed"),
    ("0F 71 D0 02 90", 4, "H2 positive: 0F 71 /2 PSRLW mm,imm8 (MMX reg {2,4,6} legal, mod=3)"),
    ("0F 71 E2 02 90", 4, "H2 positive: 0F 71 /4 PSRAW mm,imm8"),
    ("0F 71 F0 02 90", 4, "H2 positive: 0F 71 /6 PSLLW mm,imm8"),
    ("0F 72 D0 02 90", 4, "H2 positive: 0F 72 /2 PSRLD mm,imm8"),
    ("0F 73 D0 02 90", 4, "H2 positive: 0F 73 /2 PSRLQ mm,imm8"),
    ("0F 73 F0 02 90", 4, "H2 positive: 0F 73 /6 PSLLQ mm,imm8"),
    ("66 0F 71 D0 02 90", 5, "H2 positive: 66 0F 71 /2 PSRLW xmm,imm8 (SSE2, mod=3)"),
    ("66 0F 72 D0 02 90", 5, "H2 positive: 66 0F 72 /2 PSRLD xmm,imm8 (SSE2)"),
    ("66 0F 73 DB 03 90", 5, "H2 positive: 66 0F 73 /3 PSRLDQ xmm,imm8 (mod=3 - legal, NOT reserved)"),
    ("66 0F 73 FB 03 90", 5, "H2 positive: 66 0F 73 /7 PSLLDQ xmm,imm8 (mod=3 - legal, NOT reserved)"),
    ("0F 71 C8 02 90", "REJECT", "H2 negative: 0F 71 /1 reserved in every prefix combination"),
    ("0F 71 D8 02 90", "REJECT", "H2 negative: 0F 71 /3 reserved (MMX)"),
    ("0F 71 E8 02 90", "REJECT", "H2 negative: 0F 71 /5 reserved"),
    ("0F 71 F8 02 90", "REJECT", "H2 negative: 0F 71 /7 reserved (only 0F 73 /3,/7 with 66 are PSRLDQ/PSLLDQ)"),
    ("0F 73 D8 02 90", "REJECT", "H2 negative: 0F 73 /3 without 66 is reserved (PSRLDQ requires the 66 form)"),
    ("0F 73 F8 02 90", "REJECT", "H2 negative: 0F 73 /7 without 66 is reserved (PSLLDQ requires the 66 form)"),
    ("66 0F 71 C8 02 90", "REJECT", "H2 negative: 66 does not make 0F 71 /1 legal"),
    ("0F 71 00 02 90", "REJECT", "H2 negative: MMX imm-shift memory form (mod!=3) - invalid, never guessed as a shift"),
    ("66 0F 71 00 02 90", "REJECT", "H2 negative: SSE2 imm-shift memory form (mod!=3) - invalid"),
    ("66 0F 73 5B 00 03 90", "REJECT", "H2 negative: 66 0F 73 /3 PSRLDQ memory form (mod!=3) - invalid"),
    ("66 0F 73 7B 00 03 90", "REJECT", "H2 negative: 66 0F 73 /7 PSLLDQ memory form (mod!=3) - invalid"),
    ("F3 0F 71 D0 02 90", "REJECT", "H2 negative: F3-prefixed imm-shift group - no legal form"),
    ("F2 0F 71 D0 02 90", "REJECT", "H2 negative: F2-prefixed imm-shift group - no legal form"),
    # ---- D1 (0F 73 /4 per-opcode tables; oracle-checked vs GNU objdump
    # Binutils 2.44: the two negative forms return (bad); the THREE-P2
    # decoder ACCEPTED both via the shared {2,4,6} whitelist - Desktop
    # post-audit PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005 finding D1) ----
    ("0F 71 E0 02 90", 4, "D1 legal control: 0F 71 /4 PSRAW mm0,imm8 (mod=3; reg 4 STAYS legal for 0F 71)"),
    ("0F 72 E0 02 90", 4, "D1 legal control: 0F 72 /4 PSRAD mm0,imm8 (mod=3; reg 4 STAYS legal for 0F 72)"),
    ("0F 73 E0 02 90", "REJECT", "D1 NEGATIVE: 0F 73 /4 WITHOUT 66 is reserved (no PSRADQ exists; only /2,/6 legal) - the THREE-P2 decoder decoded it (length 4)"),
    ("66 0F 73 E0 02 90", "REJECT", "D1 NEGATIVE: 66 0F 73 /4 WITH 66 is reserved (SSE2 73 forms are /2,/3,/6,/7 only) - the THREE-P2 SSE2 branch retained /4"),
    ("0F 73 D0 02 90", 4, "D1 legal control: 0F 73 /2 PSRLQ mm0,imm8 (register form stays legal)"),
    ("0F 73 F0 02 90", 4, "D1 legal control: 0F 73 /6 PSLLQ mm0,imm8 (register form stays legal)"),
    ("66 0F 73 D8 02 90", 5, "D1 legal control: 66 0F 73 /3 PSRLDQ xmm0,imm8 (mod=3 legal - NOT misreported as reserved)"),
    ("66 0F 73 F8 02 90", 5, "D1 legal control: 66 0F 73 /7 PSLLDQ (reg 7 selects the operation, rm=0 -> xmm0 destination; mod=3 legal - NOT misreported as reserved)"),
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
    # P2-2 spot check: 66 0F 84 near Jcc decodes as rel16 with the operand recorded
    ins_jcc = x86dec.decode(bytes.fromhex("660F840000"), 0)
    unit.append({"vector": "66 0F 84 00 00", "rel16": ins_jcc.rel16,
                 "length": ins_jcc.length if ins_jcc else None,
                 "imm_raw": ("0x%04X" % ins_jcc.imm_raw) if ins_jcc else None,
                 "expected_length": 5, "expected_imm_raw": "0x0000",
                 "ok": bool(ins_jcc and ins_jcc.rel16 and ins_jcc.length == 5
                            and ins_jcc.imm_raw == 0),
                 "note": "P2-2 branch A: 66-prefixed near Jcc = rel16 form, operand recorded (objdump: je rel16, 5 B)"})
    # H1 spot checks: 16-bit addressing base register names (oracle-checked)
    ins_bx = x86dec.decode(bytes.fromhex("678B07"), 0)
    unit.append({"vector": "67 8B 07", "ea16": ins_bx.ea16,
                 "base_register": x86dec.REGS16[ins_bx.ea_base] if ins_bx and ins_bx.ea_base is not None else None,
                 "expected_base_register": "BX",
                 "ok": bool(ins_bx and ins_bx.ea16 and x86dec.REGS16[ins_bx.ea_base] == "BX"),
                 "note": "H1: rm=7 mod=0 in 16-bit addressing is [BX] (C2 said [BP]; objdump: mov eax,[bx])"})
    ins_bx2 = x86dec.decode(bytes.fromhex("678B4705"), 0)
    unit.append({"vector": "67 8B 47 05", "ea16": ins_bx2.ea16,
                 "base_register": x86dec.REGS16[ins_bx2.ea_base] if ins_bx2 and ins_bx2.ea_base is not None else None,
                 "expected_base_register": "BX",
                 "ok": bool(ins_bx2 and ins_bx2.ea16 and x86dec.REGS16[ins_bx2.ea_base] == "BX"),
                 "note": "H1: rm=7 mod=1 in 16-bit addressing is [BX+disp] (objdump: mov eax,[bx+0x5])"})
    ins_bp = x86dec.decode(bytes.fromhex("678B4605"), 0)
    unit.append({"vector": "67 8B 46 05", "ea16": ins_bp.ea16,
                 "base_register": x86dec.REGS16[ins_bp.ea_base] if ins_bp and ins_bp.ea_base is not None else None,
                 "expected_base_register": "BP",
                 "ok": bool(ins_bp and ins_bp.ea16 and x86dec.REGS16[ins_bp.ea_base] == "BP"),
                 "note": "H1: rm=6 mod!=0 stays [BP+disp] (objdump: mov eax,[bp+0x5])"})
    ins_abs = x86dec.decode(bytes.fromhex("678B063412"), 0)
    unit.append({"vector": "67 8B 06 34 12", "ea16": ins_abs.ea16,
                 "base_register": None if (ins_abs and ins_abs.ea_base is None) else "UNEXPECTED",
                 "disp_raw": ("0x%04X" % ins_abs.disp_raw) if ins_abs else None,
                 "expected_disp_raw": "0x1234",
                 "ok": bool(ins_abs and ins_abs.ea16 and ins_abs.ea_base is None
                            and ins_abs.ea_index is None and ins_abs.disp_raw == 0x1234),
                 "note": "H1: rm=6 mod=0 stays the [disp16] absolute form (objdump: mov eax,ds:0x1234)"})
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


# ---- D1: READ-ONLY BASE (THREE-P2) module pair for the before/after
# measurement. The BASE modules are imported as data-instruments from their
# committed package path (nothing under the historical package is modified;
# sys.dont_write_bytecode is set so no __pycache__ is created there); the
# file identities are recorded in the falsifier record.
def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()


def _load_base_module_pair():
    """Load the committed BASE (THREE-P2) x86dec+pebnd pair under isolated
    module names so its pebnd binds to the BASE x86dec (the defect carrier).
    The corrected modules imported by this battery are untouched."""
    base_dir = os.path.join(SOURCE_PACKAGE, "03_SCRIPTS")
    x_path = os.path.join(base_dir, "x86dec.py")
    b_path = os.path.join(base_dir, "pebnd.py")
    saved = sys.modules.get("x86dec")
    try:
        spec_x = importlib.util.spec_from_file_location("x86dec", x_path)
        mod_x = importlib.util.module_from_spec(spec_x)
        sys.modules["x86dec"] = mod_x
        spec_x.loader.exec_module(mod_x)
        spec_b = importlib.util.spec_from_file_location("pebnd_base", b_path)
        mod_b = importlib.util.module_from_spec(spec_b)
        spec_b.loader.exec_module(mod_b)
        ids = {
            "base_x86dec_path": x_path,
            "base_x86dec_sha256": _sha256_file(x_path),
            "base_pebnd_path": b_path,
            "base_pebnd_sha256": _sha256_file(b_path),
            "note": ("READ-ONLY import of the committed BASE modules "
                     "(no historical file modified; bytecode writes "
                     "disabled)"),
        }
        return mod_b, ids
    finally:
        if saved is not None:
            sys.modules["x86dec"] = saved
        else:
            sys.modules.pop("x86dec", None)


# ============ Q5: AF2 boundary counterexamples + discipline sweep ============
def gate_q5(pkg, ctx):
    ce = []
    SYN_BASE = 0x00A00000

    def stream_boundaries(buf, base, entry_off, past_off):
        """Decode stream boundaries (list of '+a..+b' offsets) from a single
        synthetic anchor until past past_off (for MEASURED_BOUNDARIES)."""
        out = []
        i = entry_off
        steps = 0
        while i < len(buf) and i <= past_off and steps < 256:
            if buf[i] == 0xCC:
                break
            ins = x86dec.decode(buf, i)
            if ins is None or ins.length <= 0:
                break
            out.append("+%d..+%d" % (i, i + ins.length))
            i += ins.length
            steps += 1
        return out

    def add_case(case_id, hexstr, entry_off, cand_off, exp_decode, exp_promo,
                 c1_defect, exp_status="REFUTED_MID_INSTRUCTION",
                 failure_condition=None):
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
            "ANCHORS": ("0x%08X" % (SYN_BASE + entry_off)) if entry_off is not None else "",
            "MEASURED_BOUNDARIES": (stream_boundaries(buf, SYN_BASE, entry_off,
                                                      cand_off + 8)
                                    if entry_off is not None else []),
            "FAILURE_CONDITION_DETECTED": (failure_condition or
                                           ("candidate E8 byte covered as "
                                            "operand/interior data of a proven "
                                            "anchor decode" if brefuted else "")),
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
             "its target", exp_status="CONFIRMED",
             failure_condition="none expected - positive control (an aligned "
                                "E8 rel32 at a strong-anchor boundary promotes)")

    # ---- NEW-G (P2-2 falsifier): 66 0F 84 near Jcc rel16 ----
    # Independent oracle (GNU objdump Binutils 2.44, verbatim in
    # 01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json): first instruction
    # `66 0f 84 00 00` = je rel16, length 5; then MOV at +5..+10.
    # The C2 decoder measured 7, so its anchor stream landed on the E8 at +7
    # (interior to the MOV immediate) and fabricated CALL_VALIDATION=PASS
    # with TARGET 0x00A0000D. BRANCH A requirement: first instruction = 5
    # bytes; the E8 at +7 is interior -> REFUTED_MID_INSTRUCTION;
    # INTERNAL_E8_PROMOTED = NO. (REPRODUCED this run as a carried control.)
    newg = add_case("NEW_G_66_0F_84_false_E8", "66 0F 84 00 00 B8 00 E8 01 00 00 00 C3", 0, 7,
                    "first instruction = 66 0F 84 rel16 JE length 5 (oracle-"
                    "verified); E8 at +7 lies interior to the following "
                    "MOV EAX,0x0001E800 (+5..+10)",
                    "NO_PROMOTION",
                    "C2: _2BYTE[0x80..0x8F] fixed 6-byte rel32 forms ignored "
                    "the 66 operand-size override, measured 7, landed the "
                    "anchor stream on the interior E8 at +7 and PROMOTED a "
                    "fabricated CALL edge (CALL_VALIDATION=PASS, target "
                    "0x00A0000D) from a data byte")
    newg["INTERNAL_E8_PROMOTED"] = "NO"
    newg["INDEPENDENT_ORACLE"] = ("GNU objdump (GNU Binutils for Debian) 2.44: "
                                  "`66 0f 84 00 00  je 0x5` (5 bytes) - raw "
                                  "record in 01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json")
    newg["test_passed"] = (newg["BOUNDARY_STATUS"] == "REFUTED_MID_INSTRUCTION"
                           and newg["CALL_VALIDATION"] != "PASS")

    # ---- NEW-F (P2-1 falsifier): unordered extents / anchor conflict ----
    # `B8 00 E8 01 00 00 00 90 CC`, anchor A = start+0 (its MOV EAX,imm32
    # covers +0..+5, so the E8 at +2 is IMMEDIATE DATA), anchor B = start+2
    # (lands exactly on the E8). Correct policy result: UNRESOLVED /
    # ANCHOR_CONFLICT, CALL_VALIDATION != PASS, TARGET NOT_PROMOTED.
    # The C2 cache's unordered early-break could hide A's coverage and let
    # B's exact landing yield CONFIRMED -> FALSE CALL promotion.
    fbuf = bytes.fromhex("B800E80100000090CC")
    fentries = {SYN_BASE + 0: "TEST_ANCHOR_A", SYN_BASE + 2: "TEST_ANCHOR_B"}
    fcand = SYN_BASE + 2
    # cached path (the P2-1 defect was in the cache)
    fcache = pebnd._BoundaryCache(fbuf, SYN_BASE, entries=fentries)
    fst, fsrc, fstart, frefuted = pebnd.boundary_confirm(
        fbuf, SYN_BASE, fcand, cache=fcache, entries=fentries)
    fcv = pebnd.validate_direct_call(fbuf, SYN_BASE, fcand, cache=fcache,
                                     entries=fentries)
    # uncached path
    fst2, fsrc2, fstart2, frefuted2 = pebnd.boundary_confirm(
        fbuf, SYN_BASE, fcand, cache=None, entries=fentries)
    fcv2 = pebnd.validate_direct_call(fbuf, SYN_BASE, fcand, cache=None,
                                      entries=fentries)
    # order-permutation proofs (P2-1): the SAME cached extents, inserted/
    # iterated in EVERY permutation and in randomized orders, must NEVER
    # change the coverage result (the scan sorts its input).
    import hashlib as _h
    import itertools as _it
    import random as _rnd
    extA = list(fcache.extents(SYN_BASE + 0))
    extB = list(fcache.extents(SYN_BASE + 2))
    perm_records = []
    perm_ok = True
    allA = list(_it.permutations(extA))
    for idx, p in enumerate(allA):
        r = pebnd.covers_mid_instruction(p, 2)
        perm_records.append({"stream": "A", "permutation_index": idx,
                             "order": list(p), "target_offset": 2,
                             "covers_mid": r, "expected": True})
        perm_ok = perm_ok and (r is True)
    rngf = _rnd.Random(20261005)
    for idx in range(50):
        p = extA[:]
        rngf.shuffle(p)
        r = pebnd.covers_mid_instruction(p, 2)
        perm_records.append({"stream": "A", "permutation_index": "shuffle_%d" % idx,
                             "order_sha256": _h.sha256(repr(p).encode()).hexdigest()[:16],
                             "order_len": len(p), "target_offset": 2,
                             "covers_mid": r, "expected": True})
        perm_ok = perm_ok and (r is True)
    for idx, p in enumerate(_it.permutations(extB)):
        r = pebnd.covers_mid_instruction(p, 2)
        perm_records.append({"stream": "B", "permutation_index": idx,
                             "order": list(p), "target_offset": 2,
                             "covers_mid": r, "expected": False})
        perm_ok = perm_ok and (r is False)
    # real-EXE stream permutation proof: the production anchor 0x004B0980
    # stream (75 extents) - the two driver-pin targets must be covered in
    # EVERY randomized insertion order
    ext_real = list(ctx.cache.extents(0x004B0980))
    real_targets = [0x004B0A02 - ctx.tva, 0x004B0A21 - ctx.tva,
                    0x004B0A1E - ctx.tva]  # the last is a TRUE landing (never covered)
    real_perm_ok = {t: True for t in range(len(real_targets))}
    baseline = {t: pebnd.covers_mid_instruction(ext_real, real_targets[t])
                for t in range(len(real_targets))}
    for idx in range(50):
        p = ext_real[:]
        rngf.shuffle(p)
        for t in range(len(real_targets)):
            r = pebnd.covers_mid_instruction(p, real_targets[t])
            real_perm_ok[t] = real_perm_ok[t] and (r == baseline[t])
        perm_records.append({"stream": "REAL_0x004B0980",
                             "permutation_index": "shuffle_%d" % idx,
                             "order_sha256": _h.sha256(repr(p).encode()).hexdigest()[:16],
                             "order_len": len(p),
                             "targets_covered": {str(real_targets[t]):
                                                 pebnd.covers_mid_instruction(p, real_targets[t])
                                                 for t in range(len(real_targets))},
                             "all_match_baseline": all(real_perm_ok.values())})
    newf_rec = {
        "CASE_ID": "NEW_F_unordered_extents_anchor_conflict",
        "BYTES": "B8 00 E8 01 00 00 00 90 CC",
        "START_OFFSET": "anchorA=+0;anchorB=+2",
        "CANDIDATE_OFFSET": 2,
        "EXPECTED_DECODE": ("stream A: MOV EAX,0x0001E800 covers +0..+5 "
                            "(the E8 at +2 is immediate data); stream B: "
                            "E8 01 00 00 00 lands exactly at +2"),
        "ACTUAL_DECODE": "boundary %s (source=%s)" % (fst, fsrc),
        "EXPECTED_CALL_PROMOTION": "NO_PROMOTION",
        "ACTUAL_CALL_PROMOTION": ("PROMOTED->0x%08X" % fcv["target"]) if fcv["target"]
                                  else ("NONE(%s)" % fcv["call_validation"]),
        "BOUNDARY_SOURCE": fsrc,
        "BOUNDARY_STATUS": fst,
        "C1_DEFECT_NOTE": ("C2: _BoundaryCache stored extents as a SET and "
                           "covers_mid_instruction early-broke at a >= "
                           "target_off over UNORDERED iteration; A's coverage "
                           "of the E8 was lost and B's exact landing could "
                           "yield CONFIRMED -> CALL_VALIDATION=PASS, target "
                           "0x00A00008 - a FALSE CALL promotion from the "
                           "anchor-conflict suppression"),
        "CALL_VALIDATION": fcv["call_validation"],
        "ANCHORS": "0x%08X, 0x%08X" % (SYN_BASE + 0, SYN_BASE + 2),
        "MEASURED_BOUNDARIES": {"stream_A": stream_boundaries(fbuf, SYN_BASE, 0, 10),
                                "stream_B": stream_boundaries(fbuf, SYN_BASE, 2, 10)},
        "FAILURE_CONDITION_DETECTED": ("anchor conflict: one stream covers the "
                                       "candidate mid-instruction while another "
                                       "lands exactly on it -> UNRESOLVED, "
                                       "never a promotion"),
        "UNCACHED_CROSSCHECK": {"boundary_status": fst2, "boundary_source": fsrc2,
                                "call_validation": fcv2["call_validation"],
                                "target": ("0x%08X" % fcv2["target"]) if fcv2["target"] else None,
                                "matches_cached": (fst == fst2 and fsrc == fsrc2
                                                  and fcv["call_validation"] == fcv2["call_validation"])},
        "ORDER_PERMUTATION_PROOFS": {
            "synthetic_permutations_tested": len(allA) + 50,
            "synthetic_all_expected": perm_ok,
            "real_stream_permutations_tested": 50,
            "real_stream_all_match_baseline": all(real_perm_ok.values()),
            "real_stream_baseline": {str(real_targets[t]): baseline[t]
                                     for t in range(len(real_targets))},
            "records": perm_records,
        },
        "test_passed": (fst == "UNRESOLVED" and fsrc == "ANCHOR_CONFLICT"
                        and fcv["call_validation"] != "PASS" and fcv["target"] is None
                        and fst2 == "UNRESOLVED" and fsrc2 == "ANCHOR_CONFLICT"
                        and fcv2["target"] is None
                        and perm_ok and all(real_perm_ok.values())),
    }
    ce.append(newf_rec)

    # ---- D1 (0F 73 /4 downstream falsifier): the invalid initial
    # instruction must STOP justified sequential decoding; the E8 at +4
    # must NOT receive CALL_VALIDATION=PASS or a promoted target ----
    d1buf = bytes.fromhex("0F 73 E0 02 E8 05 00 00 00 C3")
    d1entries = {SYN_BASE + 0: "TEST_D1_TRUE_ENTRY"}
    d1cand = SYN_BASE + 4
    dst, dsrc, dstart, drefuted = pebnd.boundary_confirm(
        d1buf, SYN_BASE, d1cand, cache=None, entries=d1entries)
    dcv = pebnd.validate_direct_call(d1buf, SYN_BASE, d1cand, cache=None,
                                     entries=d1entries)
    # BEFORE: the same bytes through the committed BASE (THREE-P2) modules
    # (READ-ONLY import; the defect is MEASURED, not asserted)
    base_pebnd, base_ids = _load_base_module_pair()
    bst, bsrcv, bstartv, brefv = base_pebnd.boundary_confirm(
        d1buf, SYN_BASE, d1cand, cache=None, entries=d1entries)
    bcv = base_pebnd.validate_direct_call(d1buf, SYN_BASE, d1cand, cache=None,
                                          entries=d1entries)
    # honest scope measurement: do the D1-relevant byte patterns occur in
    # the pinned EXE .text at all? (synthetic fixtures are NOT evidence of
    # PCG occurrence; this census measures it; boundary-relevant overlap
    # with anchor decode streams is checked only when a raw hit exists)
    d1_text = {"pattern_0F73_mod3_reg4": 0, "pattern_66_0F73_mod3_reg4": 0,
               "occurrence_in_anchor_decode_streams": "NOT_CHECKED (zero raw "
               "occurrences)"}
    n_text = len(ctx.text)
    for i in range(n_text - 3):
        if ctx.text[i] == 0x0F and ctx.text[i + 1] == 0x73:
            m = ctx.text[i + 2]
            if (m >> 6) == 3 and ((m >> 3) & 7) == 4:
                d1_text["pattern_0F73_mod3_reg4"] += 1
        if (ctx.text[i] == 0x66 and i + 3 < n_text
                and ctx.text[i + 1] == 0x0F and ctx.text[i + 2] == 0x73):
            m = ctx.text[i + 3]
            if (m >> 6) == 3 and ((m >> 3) & 7) == 4:
                d1_text["pattern_66_0F73_mod3_reg4"] += 1
    if d1_text["pattern_0F73_mod3_reg4"] or d1_text["pattern_66_0F73_mod3_reg4"]:
        hits_in_streams = 0
        for anchor in pebnd.KNOWN_ENTRIES:
            for (a, b) in ctx.cache.extents(anchor):
                for i in range(a, b):
                    if i + 3 < n_text:
                        m = ctx.text[i + 2] if ctx.text[i] == 0x0F and ctx.text[i + 1] == 0x73 else None
                        if m is not None and (m >> 6) == 3 and ((m >> 3) & 7) == 4:
                            hits_in_streams += 1
                        if ctx.text[i] == 0x66 and ctx.text[i + 1] == 0x0F and ctx.text[i + 2] == 0x73:
                            m2 = ctx.text[i + 3]
                            if (m2 >> 6) == 3 and ((m2 >> 3) & 7) == 4:
                                hits_in_streams += 1
        d1_text["occurrence_in_anchor_decode_streams"] = hits_in_streams
    d1_rec = {
        "CASE_ID": "D1_0F73_4_DOWNSTREAM_FALSIFIER",
        "BYTES": "0F 73 E0 02 E8 05 00 00 00 C3",
        "START_OFFSET": 0,
        "CANDIDATE_OFFSET": 4,
        "EXPECTED_DECODE": ("the first instruction 0F 73 E0 02 is an INVALID "
                            "0F 73 /4 encoding (reserved in both MMX and SSE2 "
                            "classes; independent oracle GNU objdump returns "
                            "(bad)) - a justified sequential decode MUST stop "
                            "at it; there is NO justified instruction "
                            "continuity through the first opcode to the E8 at "
                            "+4 (the D1 per-opcode repair makes the decoder "
                            "REJECT it; the stream aborts at offset 0)"),
        "ACTUAL_DECODE": ("boundary %s (source=%s) - the sequential decode "
                          "aborted at the invalid first instruction"
                          % (dst, dsrc)),
        "EXPECTED_CALL_PROMOTION": "NO_PROMOTION",
        "ACTUAL_CALL_PROMOTION": ("PROMOTED->0x%08X" % dcv["target"]) if dcv["target"]
                                  else ("NONE(%s)" % dcv["call_validation"]),
        "BOUNDARY_SOURCE": dsrc,
        "BOUNDARY_STATUS": dst,
        "C1_DEFECT_NOTE": ("THREE-P2 (BASE) measured outcome, reproduced "
                           "in-run through the committed BASE modules "
                           "(READ-ONLY import; identities recorded below): "
                           "boundary %s (source=%s), CALL_VALIDATION=%s%s - "
                           "the BASE decoder decoded the invalid 0F 73 /4 "
                           "form as a 4-byte instruction, the anchor stream "
                           "advanced onto the E8 at +4 and boundary-"
                           "certified it with an UNEARNED "
                           "CALL_VALIDATION=PASS and a promoted target"
                           % (bst, bsrcv, bcv["call_validation"],
                              (" target=0x%08X" % bcv["target"]) if bcv["target"] else "")),
        "CALL_VALIDATION": dcv["call_validation"],
        "ANCHORS": "0x%08X" % (SYN_BASE + 0),
        "MEASURED_BOUNDARIES": ["NONE - the sequential decode aborted at the "
                                "invalid first instruction (offset 0)"],
        "FAILURE_CONDITION_DETECTED": ("invalid grouped-opcode initial "
                                       "instruction followed by E8 data: "
                                       "decoding the invalid form as valid "
                                       "grants unearned boundary continuity "
                                       "to the E8 (an unsafe boundary-"
                                       "certification path for reuse)"),
        "BASE_REPRODUCTION": {
            "boundary_status": bst, "boundary_source": bsrcv,
            "call_validation": bcv["call_validation"],
            "target": ("0x%08X" % bcv["target"]) if bcv["target"] else None,
            "base_module_identities": base_ids,
        },
        "TEXT_PATTERN_CENSUS": d1_text,
        "SYNTHETIC_FIXTURE_NOTE": ("synthetic bytes - NOT evidence that this "
                                   "pattern occurs in PCG; the .text census "
                                   "field measures actual occurrence; the "
                                   "census/pin regression is measured "
                                   "separately in REGRESSION_DIFF.json"),
        "test_passed": (dst != "CONFIRMED" and dcv["call_validation"] != "PASS"
                        and dcv["target"] is None
                        and bst == "CONFIRMED" and bcv["call_validation"] == "PASS"
                        and bcv["target"] is not None),
    }
    ce.append(d1_rec)
    d1_falsifier_record = d1_rec

    # ---- REAL-REFUTE: the two real driver pins re-derive REFUTED_MID_INSTRUCTION ----
    for rr_va, interior_note in (
            (0x004B0A02, "interior to `BB 01 00 00 00` MOV EBX,1 @0x004B0A01"),
            (0x004B0A21, "interior to `E8 4D 14 F5 FF` the real CALL @0x004B0A1E")):
        rb, rbs, rbst, rbref = pebnd.boundary_confirm(ctx.text, ctx.tva, rr_va, ctx.cache)
        rcv = pebnd.validate_direct_call(ctx.text, ctx.tva, rr_va, ctx.cache)
        rrow_off = rr_va - ctx.tva
        w0 = rrow_off - 6
        win = ctx.text[w0:w0 + 14]
        ce.append({
            "CASE_ID": "REAL_REFUTE_0x%08X" % rr_va,
            "BYTES": win.hex(" ").upper(),
            "START_OFFSET": ("0x%08X (production anchor FUN_004B0980, "
                            "PRIOR_CANON_ANCHOR_INPUT)" % 0x004B0980),
            "CANDIDATE_OFFSET": "0x%08X" % rr_va,
            "EXPECTED_DECODE": ("the pin VA %s is %s; the correct boundary "
                                "result is REFUTED_MID_INSTRUCTION with "
                                "refuted_by=0x004B0980 (the C2 cache missed "
                                "the covering extent and left the pin "
                                "UNRESOLVED/HEURISTIC_START_CANDIDATE)"
                                % ("0x%08X" % rr_va, interior_note)),
            "ACTUAL_DECODE": ("covered mid-instruction by proven decode from "
                              "anchor 0x%08X" % rbref) if rbref else
                             ("boundary %s (source=%s)" % (rb, rbs)),
            "EXPECTED_CALL_PROMOTION": "NO_PROMOTION",
            "ACTUAL_CALL_PROMOTION": ("PROMOTED->0x%08X" % rcv["target"]) if rcv["target"]
                                      else ("NONE(%s)" % rcv["call_validation"]),
            "BOUNDARY_SOURCE": rbs,
            "BOUNDARY_STATUS": rb,
            "C1_DEFECT_NOTE": ("C2 committed boundary: UNRESOLVED / "
                                "HEURISTIC_START_CANDIDATE / refuted_by=none "
                                "(the unordered-extents underclaim); the "
                                "DECLASSIFIED_NOT_A_CALL ledger status is "
                                "unchanged - the declassification as not-a-CALL "
                                "remains correct, now with the stronger "
                                "proven reason"),
            "CALL_VALIDATION": rcv["call_validation"],
            "ANCHORS": "0x004B0980",
            "MEASURED_BOUNDARIES": ["0x%08X..0x%08X" % (ctx.tva + a, ctx.tva + b)
                                    for (a, b) in ctx.cache.extents(0x004B0980)
                                    if a <= (rr_va - ctx.tva) + 1 <= b + 1
                                    and abs(a - (rr_va - ctx.tva)) <= 8],
            "FAILURE_CONDITION_DETECTED": ("unordered-extents coverage underclaim: "
                                           "the pin is interior data on the "
                                           "0x004B0980 proven decode path"),
            "REFUTED_BY": ("0x%08X" % rbref) if rbref else None,
            "test_passed": (rb == "REFUTED_MID_INSTRUCTION" and rbs == "KNOWN_FUNCTION_ENTRY"
                            and rbref == 0x004B0980 and rcv["target"] is None),
        })

    # real-EXE positive controls (production anchors)
    real_pos = []
    for va, exp_t in ((0x0070C715, 0x00972380), (0x0070DD75, 0x00971AD0),
                      (0x0070C742, 0x00972DF0)):
        cv = pebnd.validate_direct_call(ctx.text, ctx.tva, va, ctx.cache)
        rb, rbs, rbst, rbref = pebnd.boundary_confirm(ctx.text, ctx.tva, va, ctx.cache)
        off = va - ctx.tva
        real_pos.append({"va": "0x%08X" % va, "call_validation": cv["call_validation"],
                         "boundary_source": cv["boundary_source"],
                         "target": ("0x%08X" % cv["target"]) if cv["target"] else None,
                         "expected_target": "0x%08X" % exp_t,
                         "ok": cv["call_validation"] == "PASS" and cv["target"] == exp_t})
        ce.append({
            "CASE_ID": "REAL_positive_call_0x%08X" % va,
            "BYTES": ctx.text[off:off + 5].hex(" ").upper(),
            "START_OFFSET": ("0x%08X (production anchor; PRIOR_CANON_ANCHOR_INPUT)"
                             % rbst) if rbst else "",
            "CANDIDATE_OFFSET": "0x%08X" % va,
            "EXPECTED_DECODE": ("ordinary unprefixed E8 rel32 at a strong-anchor-"
                               "confirmed boundary; target 0x%08X" % exp_t),
            "ACTUAL_DECODE": "boundary %s (source=%s, start=0x%08X)"
                             % (rb, rbs, rbst) if rbst else
                             ("boundary %s (source=%s)" % (rb, rbs)),
            "EXPECTED_CALL_PROMOTION": "PROMOTE",
            "ACTUAL_CALL_PROMOTION": ("PROMOTED->0x%08X" % cv["target"]) if cv["target"]
                                      else ("NONE(%s)" % cv["call_validation"]),
            "BOUNDARY_SOURCE": rbs,
            "BOUNDARY_STATUS": rb,
            "C1_DEFECT_NOTE": ("regression control: the P2-1/P2-2/H1/H2 repairs "
                              "must NOT untrack the three current real positive "
                              "CALL controls"),
            "CALL_VALIDATION": cv["call_validation"],
            "ANCHORS": ("0x%08X" % rbst) if rbst else "",
            "MEASURED_BOUNDARIES": ["0x%08X..0x%08X" % (ctx.tva + a, ctx.tva + b)
                                    for (a, b) in ctx.cache.extents(rbst)
                                    if abs(a - off) <= 8] if rbst else [],
            "FAILURE_CONDITION_DETECTED": "none expected - positive control",
            "test_passed": (cv["call_validation"] == "PASS" and cv["target"] == exp_t
                            and rb == "CONFIRMED"),
        })

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
          "d1_falsifier_record": d1_falsifier_record,
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
        "FACTORY_PLUS_84_ASSIGNMENT_CORE = PRESERVED_CONFIRMED_STATIC_CONDITIONAL",
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
        "ARK_ESTATE_INSTRUCTION_START_VA = 0x0075136E",
        "ARK_ESTATE_IMMEDIATE_LOCATION_VA = 0x00751370",
        "PRIOR_CANON_ANCHOR_INPUT",
        # ---- THIS RUN's D1/D2 correction statuses (measured, not inherited) ----
        "D1_H2_0F73_4_STATUS = CORRECTED_PER_OPCODE_LEGAL_REG_TABLES",
        "D1_INVALID_FIXTURES = 2/2_REJECTED",
        "D1_DOWNSTREAM_CALL_STATUS = CORRECTED_NO_PASS_NO_PROMOTION_NOT_VERIFIED",
        "D2_PINSET_STATUS = CORRECTED_ROSTER_BOUND_BIDIRECTIONAL_MULTISET",
        "D2_ROLE_APPLICABILITY_STATUS = CORRECTED_EXPECTED_ROLE_DRIVEN_EA",
        "P2_1_BOUNDARY_CACHE = PRESERVED_CORRECTED_SORTED_EXTENTS (REPRODUCED_THIS_RUN)",
        "P2_2_66_0F8X_NEAR_JCC = PRESERVED_CORRECTED_BRANCH_A_REL16 (REPRODUCED_THIS_RUN)",
        "P2_3_Q2_EFFECTIVE_ADDRESS = PRESERVED_CORRECTED_RE_DERIVED_FROM_EXE (D2_EXTENDS)",
        "H1_REG16_RM7 = PRESERVED_CORRECTED_BX_TABLE (REPRODUCED_THIS_RUN)",
        "H2_GROUP_OPCODES = CORRECTED_PER_OPCODE_VALIDITY_TABLES",
        "Q2_EFFECTIVE_ADDRESS_FIELDS = effective_address present/memop state; "
        "operand_width; segment; base_register; index_register; scale; "
        "raw_displacement; signed_displacement; effective_displacement; "
        "address_provenance_status",
        "OLD_MUTATION_TOTAL = 7",
        "D2_NEW_MUTATION_TOTAL = 8",
        "MUTATION_TOTAL = 15",
        "NEW_F_INTERNAL_E8_PROMOTED = NO",
        "NEW_G_INTERNAL_E8_PROMOTED = NO",
        "D1_INTERNAL_E8_PROMOTED = NO",
        # ---- phase semantics of THIS executor run (persistence by the
        # PE-MASTER phase: review verdict, entrypoint row, commit/push) ----
        "PE_MASTER_REVIEW_PERFORMED_BY_THIS_RUN = NO",
        "AUDIT_ENTRYPOINT_MODIFIED = NO",
        "COMMIT_OR_PUSH_PERFORMED = NO",
        "MANIFEST_PREPARED_FOR_PERSISTENCE_PHASE = YES",
        "NEXT_EXPERIMENT_AUTHORIZED = NO",
    ]
    missing = [s for s in required if s not in fr]
    if missing:
        fail("missing required strings in FINAL_REPORT: %s" % missing)
    # superseded-phrase sweep (historical overclaims must not reappear)
    forbidden_phrases = ["ASSIGNED_OBJECT_VTABLE = NONE", "NON-POLYMORPHIC",
                         "non-polymorphic", "vtable_store_found",
                         "all methods direct-called", "0xA4 bytes (280)",
                         "declared_families\": 10", "declared_families = 10",
                         # ---- superseded wordings carried from C2 (active
                         # surfaces must not reuse them) ----
                         "re-derives every C1-JSON pin field",
                         "re-derived field-by-field",
                         "promotion-safe",
                         "safe for promotion",
                         "underclaim-only",
                         # ---- THIS RUN's retractions of the THREE-P2 BASE
                         # claims (D1/D2): they may appear ONLY as ledger
                         # ORIGINAL_EXCERPT quotes, never as active claims ----
                         "H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY",
                         "the repair is COMPLETE for the three P2 + H1 + H2",
                         "No defect was found that could not be fixed",
                         "for every pin where semantically applicable",
                         "complete H2 closure",
                         "complete Q2 JSON closure",
                         "unrestricted dependent reuse",
                         "no remaining blocker"]
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
    # NEW_SUPERSESSION_RECORD_COUNT = the number of S-* ledger RECORDS
    # (headers), measured independently of the excerpt-line count (records may
    # carry multiple ORIGINAL_EXCERPT lines). THIS run's ledger uses the
    # S-D1-*/S-D2-*/S-CM-*/S-AUD-* prefixes.
    record_headers = re.findall(
        r"^## (S-(?:D1|D2|CM|AUD)-\d+)", led, re.M)
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
    # P3-C: the repository-owner typo correction (carried from C2; the
    # historical source with the typo is the C1 INPUT_IDENTITIES - READ ONLY)
    old_text = "SebastianKlo/eudoria-clean"
    new_text = "SebastianKozlo/eudoria-clean"
    src_ident = open(os.path.join(C1_PACKAGE, "INPUT_IDENTITIES.md"),
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
    # commit-message verbatim fidelity: THIS run's supersession ledger quotes
    # the IMMUTABLE historical BASE (THREE-P2) commit message at 9d31a82
    # (history is not edited); the verbatim copy under 01_RAW must equal the
    # actual git object at BASE_SHA (machine-checked here, not trusted)
    cm_path = BASE_COMMIT_MESSAGE_VERBATIM
    try:
        cm_disk = open(cm_path, encoding="utf-8").read()
        cm_git = subprocess.check_output(
            ["git", "log", "-1", "--format=%B", BASE_SHA],
            cwd=REPO).decode("utf-8", errors="replace")
        cm_ok = cm_disk.strip() == cm_git.strip()
    except Exception as e:
        cm_ok = False
        q14["commit_message_verbatim_error"] = str(e)
    q14["commit_message_verbatim_fidelity"] = cm_ok
    if not cm_ok:
        fail("BASE_COMMIT_MESSAGE_VERBATIM.txt does not match git log -1 BASE_SHA")
    # required package files (the D1/D2 contract's package list; CQC_FINAL.json
    # is the battery's own LAST output and is verified by the manifest +
    # HANDOFF declarations instead)
    required_files = [
        "INPUT_IDENTITIES.md", "GENERATION_RECORD.md", "FINAL_REPORT.md",
        "QC_REPORT.md", "EVIDENCE_INDEX.md", "PE_MASTER_REVIEW.md",
        "HANDOFF.md", "SUPERSESSION_LEDGER.md", "REGRESSION_DIFF.json",
        "EXPECTED_PIN_REGISTRY.json", "CORRECTED_PIN_LEDGER.csv",
        "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv",
        "AF3_PROVENANCE_LEDGER.csv",
        os.path.join("01_RAW", "C1_PIN_EVIDENCE.json"),
        os.path.join("01_RAW", "C2_CENSUS.json"),
        os.path.join("01_RAW", "C3_OBJECT_SCOPE.json"),
        os.path.join("01_RAW", "CQC_MUTATION_RESULTS.json"),
        os.path.join("01_RAW", "D1_INDEPENDENT_ORACLE_RECORDS.json"),
        os.path.join("01_RAW", "D1_BOUNDARY_FALSIFIER.json"),
        os.path.join("01_RAW", "D2_MUTATION_RESULTS.json"),
        os.path.join("01_RAW", "BASE_COMMIT_MESSAGE_VERBATIM.txt"),
    ]
    missing_files = [rf for rf in required_files
                     if not os.path.exists(os.path.join(RUN, rf))]
    q14["required_files_missing"] = missing_files
    if missing_files:
        fail("required package files missing: %s" % missing_files)
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
    tmp = tempfile.mkdtemp(prefix="p2fix_mut_", suffix="_out")
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

        def af3_compound(rows):
            # COMPOUND mutation (all changed fields listed; never called a
            # one-field mutation): the manager PROVEN row loses its identity
            # edge, identified object, identity evidence AND the
            # address-provenance support (candidate bytes unchanged)
            for r in rows:
                if (r["CANDIDATE_VA"] == "0x00707EC0"
                        and r["FINAL_CLASSIFICATION"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"):
                    r["IDENTITY_EDGE"] = ""
                    r["IDENTIFIED_OBJECT"] = ""
                    r["IDENTITY_EVIDENCE"] = ""
                    r["ADDRESS_PROVENANCE_STATUS"] = "UNRESOLVED"
            return rows

        def m5(obj):
            # P2-3 causal mutation M5: THE_STORE_plus_84 JSON
            # effective_address.base_register ESI -> EAX (the Desktop
            # post-audit's first undetected corruption)
            for p in obj["pins"]:
                if p["claim_id"] == "THE_STORE_plus_84":
                    p["effective_address"]["base_register"] = "EAX"
            return obj

        def m6(obj):
            # P2-3 causal mutation M6: THE_STORE_plus_84 JSON
            # effective_address.address_provenance_status -> a fake
            # known-function provenance (THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE)
            for p in obj["pins"]:
                if p["claim_id"] == "THE_STORE_plus_84":
                    p["effective_address"]["address_provenance_status"] = \
                        "THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE"
            return obj

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
             ("", "AF3_PROVENANCE_LEDGER.csv"), af3_compound, "Q7",
             "COMPOUND (all changed fields listed, NOT one-field): the manager "
             "PROVEN row's IDENTITY_EDGE='' + IDENTIFIED_OBJECT='' + "
             "IDENTITY_EVIDENCE='' + ADDRESS_PROVENANCE_STATUS='UNRESOLVED' "
             "(candidate bytes unchanged)"),
            ("M5", "01_RAW/C1_PIN_EVIDENCE.json",
             ("01_RAW", "C1_PIN_EVIDENCE.json"), m5, "Q2",
             "P2-3: THE_STORE_plus_84 effective_address.base_register ESI -> EAX "
             "(the JSON field the C2 Q2 did not re-derive)"),
            ("M6", "01_RAW/C1_PIN_EVIDENCE.json",
             ("01_RAW", "C1_PIN_EVIDENCE.json"), m6, "Q2",
             "P2-3: THE_STORE_plus_84 effective_address.address_provenance_status -> "
             "THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE (fake provenance)"),
        ]
        gates = {"Q2": gate_q2, "Q3": gate_q3, "Q6": gate_q6, "Q7": gate_q7,
                 "Q8": gate_q8}
        # exact before/after VALUES per mutation (measured from the production
        # package before the run; the mutated copies are temporary)
        MUT_BEFORE_AFTER = {
            "M1": {"before": "stream_ctor_entry.opcode_bytes = '6A FF'",
                   "after": "stream_ctor_entry.opcode_bytes = 'EB FF'"},
            "M2": {"before": "slotpred_callback_MOV_EAX_imm32.measured_operand = "
                             "'0x70BEF0 (7388912)'",
                   "after": "'0x70BEF0B8 (118482808)'"},
            "M3": {"before": "examined_ctor.offset_zero_stores = [3 measured stores]",
                   "after": "[] (collection removed)"},
            "M4": {"before": "census[0x0070DD1A].containing_function = "
                             "'FUN_0070DCF0_consumer_record_reader'",
                   "after": "'entry~0xDEADBEEF'"},
            "AF3/Q8": {"before": "manager row: IDENTITY_EDGE=<machine-checked this "
                                 "flow chain>; IDENTIFIED_OBJECT=<the MANAGER "
                                 "object...>; IDENTITY_EVIDENCE=<entry this-flow + "
                                 "singleton census + prior canon>; "
                                 "ADDRESS_PROVENANCE_STATUS="
                                 "'THIS_OF_KNOWN_FUNCTION:FUN_00707E50_manager_ctor'",
                       "after": "IDENTITY_EDGE=''; IDENTIFIED_OBJECT=''; "
                                "IDENTITY_EVIDENCE=''; "
                                "ADDRESS_PROVENANCE_STATUS='UNRESOLVED' (ALL FOUR "
                                "fields changed - compound)"},
            "M5": {"before": "THE_STORE_plus_84.effective_address.base_register = 'ESI'",
                   "after": "'EAX'"},
            "M6": {"before": "THE_STORE_plus_84.effective_address."
                             "address_provenance_status = "
                             "'THIS_OF_KNOWN_FUNCTION:FUN_0070C680_stream_attach_setter'",
                   "after": "'THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE'"},
        }
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
            # persist the EXACT failing predicates measured on the MUTATED run
            failing = []
            for key in ("mismatches", "failures"):
                for m in (det.get(key) or []):
                    failing.append(m if isinstance(m, dict) else {"why": m})
            # persist exact before/after VALUES for the mutated field
            before_after = MUT_BEFORE_AFTER.get(mid, {})
            rec = {
                "MUTATION_ID": mid,
                "MUTATED_ARTIFACT": label,
                "FIELD": desc,
                "BEFORE": "clean committed artifact (production package)",
                "AFTER": "temporary mutated copy at %s (deleted after the test; "
                         "never persisted as a canonical artifact)" % pkg_root,
                "BEFORE_VALUE": before_after.get("before"),
                "AFTER_VALUE": before_after.get("after"),
                "FAILING_PREDICATES": failing,
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


# ============================ D2 MUTATION HARNESS ============================
# The D2 completeness controls (Desktop finding D2/P2). Each case mutates an
# ISOLATED TEMP COPY of the ACTUAL newly generated C1 JSON/CSV (same EXE,
# same loader, same production gate_q2) and must flip clean Q2 PASS ->
# mutated Q2 FAIL with NO substitute failure from a manifest, Git baseline
# or another gate. Exact semantic deltas, before/after artifact hashes and a
# per-case input-hash census (proving the unrelated inputs are byte-identical
# to the production package) are persisted in 01_RAW/D2_MUTATION_RESULTS.json.
D2_MUT_TMP_BASE = r"C:\Users\User\AppData\Local\Temp\opencode\d1d2_mut"


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()


def _pkg_input_census(pkg_root, rels):
    return {rel: _sha256_file(os.path.join(pkg_root, *rel.split("/")))
            for rel in rels}


def run_d2_mutations(ctx, prod_pkg, gate_results):
    results = []
    os.makedirs(D2_MUT_TMP_BASE, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="d1d2_pkg_", dir=D2_MUT_TMP_BASE)
    input_rels = sorted(
        [name if not sub else (sub + "/" + name)
         for (sub, name, _k) in MUTATABLE.values()]
        + ["01_RAW/C2_CENSUS.json"])
    production_census = _pkg_input_census(RUN, input_rels)
    try:
        def build_pkg_root(mid):
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
            return pkg_root

        def load_j(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)

        def save_j(p, obj):
            with open(p, "w", newline="\n", encoding="utf-8") as f:
                json.dump(obj, f, indent=1)

        def load_c(p):
            with open(p, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
                fields = list(rows[0].keys()) if rows else []
            return rows, fields

        def save_c(p, rows, fields):
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                for r in rows:
                    w.writerow(r)

        def apply_d2(mid, pkg_root):
            jpath = os.path.join(pkg_root, "01_RAW", "C1_PIN_EVIDENCE.json")
            cpath = os.path.join(pkg_root, "CORRECTED_PIN_LEDGER.csv")
            if mid == "D2-M1":
                obj = load_j(jpath)
                for p in obj["pins"]:
                    if p["claim_id"] == "THE_STORE_plus_84":
                        p["kind"] = "code_entry"
                        del p["effective_address"]
                save_j(jpath, obj)
                return ("COMPOUND TWO-FIELD mutation: THE_STORE_plus_84 JSON "
                        "kind mem->code_entry AND its effective_address "
                        "object removed (EA validation must remain enforced "
                        "by the EXPECTED roster role)",
                        "kind='mem'; effective_address present",
                        "kind='code_entry'; effective_address ABSENT",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M2":
                obj = load_j(jpath)
                obj["pins"] = [p for p in obj["pins"]
                               if p["claim_id"] != "THE_STORE_plus_84"]
                save_j(jpath, obj)
                return ("whole-pin deletion: the ENTIRE THE_STORE_plus_84 "
                        "JSON pin removed (CSV and declared totals "
                        "unchanged - the load-bearing pin must still be "
                        "missed by Q2)",
                        "THE_STORE_plus_84 present (133 JSON pins)",
                        "THE_STORE_plus_84 ABSENT (132 JSON pins)",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M3":
                obj = load_j(jpath)
                for p in obj["pins"]:
                    if p["claim_id"] == "stream_ctor_buffer_store":
                        p["kind"] = "code_entry"
                        del p["effective_address"]
                save_j(jpath, obj)
                return ("COMPOUND TWO-FIELD mutation: "
                        "stream_ctor_buffer_store JSON kind mem->code_entry "
                        "AND its effective_address object removed (the "
                        "second load-bearing constructor pin)",
                        "kind='mem'; effective_address present",
                        "kind='code_entry'; effective_address ABSENT",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M4":
                obj = load_j(jpath)
                obj["pins"] = [p for p in obj["pins"]
                               if p["claim_id"] != "stream_ctor_buffer_store"]
                save_j(jpath, obj)
                return ("whole-pin deletion: the ENTIRE "
                        "stream_ctor_buffer_store JSON pin removed (CSV "
                        "and declared totals unchanged)",
                        "stream_ctor_buffer_store present (133 JSON pins)",
                        "stream_ctor_buffer_store ABSENT (132 JSON pins)",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M5":
                obj = load_j(jpath)
                dup = None
                for p in obj["pins"]:
                    if p["claim_id"] == "THE_STORE_plus_84":
                        dup = copy.deepcopy(p)
                        break
                obj["pins"].append(dup)
                save_j(jpath, obj)
                return ("duplicate-claim protection: an EXACT duplicate of "
                        "the THE_STORE_plus_84 JSON pin appended (same "
                        "claim_id twice; multiplicity must FAIL, not just "
                        "count)",
                        "THE_STORE_plus_84 occurs once",
                        "THE_STORE_plus_84 occurs twice (exact duplicate)",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M6":
                obj = load_j(jpath)
                clone = None
                for p in obj["pins"]:
                    if p["claim_id"] == "THE_STORE_plus_84":
                        clone = copy.deepcopy(p)
                        break
                clone["claim_id"] = "FAKE_EXTRA_PIN_0xDEADBEEF"
                obj["pins"].append(clone)
                save_j(jpath, obj)
                return ("extra-claim protection (JSON): a foreign pin "
                        "claim_id NOT in the expected roster appended "
                        "(cloned from THE_STORE_plus_84)",
                        "133 JSON claims, all in the roster",
                        "134 JSON claims incl. FAKE_EXTRA_PIN_0xDEADBEEF",
                        ["01_RAW/C1_PIN_EVIDENCE.json"])
            if mid == "D2-M7":
                rows, fields = load_c(cpath)
                clone = dict(rows[0])
                clone["claim_id"] = "FAKE_EXTRA_CSV_ROW_0xDEADBEEF"
                rows.append(clone)
                save_c(cpath, rows, fields)
                return ("extra-claim protection (CSV): a foreign CSV row "
                        "claim_id NOT in the expected roster appended "
                        "(JSON unchanged)",
                        "133 CSV claims, all in the roster",
                        "134 CSV claims incl. FAKE_EXTRA_CSV_ROW_0xDEADBEEF",
                        ["CORRECTED_PIN_LEDGER.csv"])
            if mid == "D2-M8":
                obj = load_j(jpath)
                obj["pins"] = [p for p in obj["pins"]
                               if p["claim_id"] != "THE_STORE_plus_84"]
                obj["pin_totals"]["total_pins"] = len(obj["pins"])
                if "VALIDATED" in obj["pin_totals"]["status_tally"]:
                    obj["pin_totals"]["status_tally"]["VALIDATED"] -= 1
                save_j(jpath, obj)
                rows, fields = load_c(cpath)
                rows = [r for r in rows if r["claim_id"] != "THE_STORE_plus_84"]
                save_c(cpath, rows, fields)
                return ("synchronized JSON+CSV omission with INTERNALLY "
                        "CONSISTENT adjusted declared totals (132/132, "
                        "tally adjusted): the pin disappears from BOTH "
                        "artifacts and the declared totals no longer "
                        "contradict the content - it must still FAIL "
                        "against the SEPARATELY PINNED expected roster "
                        "(cardinality is a coverage contract, not a "
                        "padding target)",
                        "THE_STORE_plus_84 present in JSON+CSV; declared "
                        "total 133",
                        "THE_STORE_plus_84 absent from JSON+CSV; declared "
                        "total 132 (internally consistent)",
                        ["01_RAW/C1_PIN_EVIDENCE.json",
                         "CORRECTED_PIN_LEDGER.csv"])
            raise SystemExit("unknown D2 mutation %s" % mid)

        D2_META = {
            "D2-M1": "COMPOUND_KIND_CHANGE_PLUS_EA_REMOVAL (mandatory)",
            "D2-M2": "ENTIRE_PIN_DELETION_JSON (mandatory)",
            "D2-M3": "COMPOUND_KIND_CHANGE_PLUS_EA_REMOVAL (mandatory)",
            "D2-M4": "ENTIRE_PIN_DELETION_JSON (mandatory)",
            "D2-M5": "DUPLICATE_CLAIM_PROTECTION",
            "D2-M6": "EXTRA_CLAIM_PROTECTION_JSON",
            "D2-M7": "EXTRA_CLAIM_PROTECTION_CSV",
            "D2-M8": "SYNCHRONIZED_JSON_CSV_OMISSION",
        }
        for mid in ("D2-M1", "D2-M2", "D2-M3", "D2-M4",
                    "D2-M5", "D2-M6", "D2-M7", "D2-M8"):
            pkg_root = build_pkg_root(mid)
            delta, before, after, mutated_rels = apply_d2(mid, pkg_root)
            temp_census = _pkg_input_census(pkg_root, input_rels)
            artifact_hashes = {}
            for rel in mutated_rels:
                artifact_hashes[rel] = {
                    "clean_production_sha256": production_census.get(rel),
                    "mutated_temp_sha256": temp_census.get(rel),
                    "changed": production_census.get(rel) != temp_census.get(rel)}
            census_check = {rel: {"production_sha256": production_census.get(rel),
                                  "temp_sha256": temp_census.get(rel),
                                  "byte_identical_to_production":
                                      production_census.get(rel) == temp_census.get(rel)}
                            for rel in input_rels}
            mut_pkg = load_pkg(pkg_root)
            st, det = gate_q2(mut_pkg, ctx)
            unmut_status = gate_results.get("Q2")
            failing = []
            for key in ("mismatches", "json_csv_inconsistencies"):
                for m in (det.get(key) or []):
                    failing.append(m if isinstance(m, dict) else {"why": m})
            results.append({
                "MUTATION_ID": mid,
                "MUTATION_CLASS": D2_META[mid],
                "MUTATED_ARTIFACTS": mutated_rels,
                "SEMANTIC_DELTA": delta,
                "BEFORE_VALUE": before,
                "AFTER_VALUE": after,
                "ARTIFACT_HASHES": artifact_hashes,
                "INPUT_HASH_CENSUS": census_check,
                "INPUT_CENSUS_SUMMARY": {
                    "inputs_total": len(input_rels),
                    "inputs_byte_identical": sum(
                        1 for c in census_check.values()
                        if c["byte_identical_to_production"]),
                    "inputs_changed": [rel for rel, c in census_check.items()
                                       if not c["byte_identical_to_production"]]},
                "FAILING_PREDICATES": failing,
                "PRODUCTION_GATE_ID": "Q2",
                "UNMUTATED_RESULT": unmut_status,
                "MUTATED_RESULT": st,
                "EXPECTED_CAUSALITY": "UNMUTATED=PASS -> MUTATED=FAIL",
                "ACTUAL_CAUSALITY": ("CAUSAL_PASS" if (unmut_status == "PASS"
                                                      and st == "FAIL")
                                     else "NOT_CAUSAL"),
                "SUBSTITUTE_FAILURE_CHECK": ("the failure is the production "
                                            "gate_q2's own predicate list "
                                            "above (pin-universe/role/EA "
                                            "checks against the pinned EXE "
                                            "and roster); no manifest, no "
                                            "Git baseline, no other gate "
                                            "participates in this check"),
                "IDENTITY_PRESERVED_BETWEEN_EXECUTIONS": (
                    "EXE identity: pinned %s / %d bytes re-hashed by the "
                    "loader at both executions; expected roster: re-derived "
                    "in-run from the SAME BASE Git blob; unrelated inputs: "
                    "byte-identical to the production package per the "
                    "INPUT_HASH_CENSUS; gate implementation: the SAME "
                    "gate_q2 function object executed for both results"
                    % (pebnd.PINNED_EXE_SHA256[:12], pebnd.PINNED_EXE_SIZE)),
                "TEMP_TREE": pkg_root,
            })
    finally:
        # delete ONLY this run's scratch (verified under the task-specific
        # D2_MUT_TMP_BASE; never anything inside the repo)
        if os.path.abspath(tmp).startswith(os.path.abspath(D2_MUT_TMP_BASE)):
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
    ap.add_argument("--out-d2mut", default=os.path.join(RUN, "01_RAW", "D2_MUTATION_RESULTS.json"))
    ap.add_argument("--out-d1-falsifier", default=os.path.join(RUN, "01_RAW", "D1_BOUNDARY_FALSIFIER.json"))
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
    d2_mut_results = run_d2_mutations(ctx, pkg, gate_results)
    with open(args.out_mut, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
                    "mutation_discipline": ("the RETAINED seven M1-M4 + AF3/Q8 "
                                           "(compound, all changed fields listed) "
                                           "+ M5/M6 controls: the SAME production "
                                           "gate must show UNMUTATED=PASS and "
                                           "MUTATED=FAIL; the mutation target is a "
                                           "TEMPORARY COPY of the ACTUAL final "
                                           "artifact (never a fixture, never the "
                                           "canonical committed artifact; temp "
                                           "tree OUTSIDE the repo, deleted after "
                                           "the run); corrupted copies are never "
                                           "persisted; exact before/after values "
                                           "and failing predicates recorded per "
                                           "mutation. The eight NEW D2 completeness "
                                           "controls are persisted separately in "
                                           "01_RAW/D2_MUTATION_RESULTS.json"),
                    "results": mut_results}, f, indent=1)
    with open(args.out_d2mut, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
                    "d2_mutation_discipline": ("D2 completeness controls (NOT new "
                                              "science): each case mutates an "
                                              "ISOLATED TEMP COPY of the ACTUAL "
                                              "newly generated C1 JSON/CSV "
                                              "(same pinned EXE, same production "
                                              "loader, same production gate_q2) "
                                              "and must flip clean Q2 PASS -> "
                                              "mutated Q2 FAIL through the "
                                              "gate's OWN pin-universe/role/EA "
                                              "predicates (no manifest, no Git "
                                              "baseline, no other gate); exact "
                                              "semantic deltas, before/after "
                                              "artifact hashes and per-case "
                                              "input-hash censuses proving the "
                                              "unrelated inputs byte-identical"),
                    "results": d2_mut_results}, f, indent=1)
    with open(args.out_d1_falsifier, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
                    "falsifier_discipline": ("MANDATORY downstream falsifier "
                                            "(D1): synthetic bytes, synthetic "
                                            "strong entry at the first byte; "
                                            "the invalid initial instruction "
                                            "must STOP justified sequential "
                                            "decoding; the E8 at offset +4 "
                                            "must NOT receive "
                                            "CALL_VALIDATION=PASS or a "
                                            "promoted target; the VA/fixture "
                                            "is never special-cased; the "
                                            "BEFORE outcome is MEASURED "
                                            "in-run through the committed "
                                            "BASE (THREE-P2) modules"),
                    "record": gates["Q5"][1]["d1_falsifier_record"],
                    "production_gate": "Q5 (boundary test matrix case "
                                       "D1_0F73_4_DOWNSTREAM_FALSIFIER)"}, f, indent=1)
    with open(args.out_af1_matrix, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["MUTATION_ID", "MUTATION_CLASS", "MUTATED_ARTIFACT", "FIELD",
                    "BEFORE", "BEFORE_VALUE", "AFTER", "AFTER_VALUE",
                    "PRODUCTION_GATE_ID", "UNMUTATED_RESULT", "MUTATED_RESULT",
                    "EXPECTED_CAUSALITY", "ACTUAL_CAUSALITY",
                    "FAILING_PREDICATE_COUNT"])
        for r in mut_results:
            w.writerow([r["MUTATION_ID"], "RETAINED_CONTROL",
                        r["MUTATED_ARTIFACT"], r["FIELD"],
                        r["BEFORE"], r.get("BEFORE_VALUE"),
                        r["AFTER"], r.get("AFTER_VALUE"), r["PRODUCTION_GATE_ID"],
                        r["UNMUTATED_RESULT"], r["MUTATED_RESULT"],
                        r["EXPECTED_CAUSALITY"], r["ACTUAL_CAUSALITY"],
                        len(r.get("FAILING_PREDICATES") or [])])
        for r in d2_mut_results:
            w.writerow([r["MUTATION_ID"], r["MUTATION_CLASS"],
                        "; ".join(r["MUTATED_ARTIFACTS"]), r["SEMANTIC_DELTA"],
                        "clean committed artifact (production package)",
                        r.get("BEFORE_VALUE"),
                        "temporary mutated copy at %s (deleted after the test; "
                        "never persisted as a canonical artifact)" % r["TEMP_TREE"],
                        r.get("AFTER_VALUE"), r["PRODUCTION_GATE_ID"],
                        r["UNMUTATED_RESULT"], r["MUTATED_RESULT"],
                        r["EXPECTED_CAUSALITY"], r["ACTUAL_CAUSALITY"],
                        len(r.get("FAILING_PREDICATES") or [])])

    # decoder unit battery + boundary counterexamples persisted
    with open(args.out_decoder, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
                   "unit_battery": gates["Q4"][1]["unit_battery"],
                   "unit_battery_ok": gates["Q4"][1]["unit_battery_ok"],
                   "redecode_bad_rows": gates["Q4"][1]["redecode_bad_rows"],
                   "coverage_windows": gates["Q4"][1]["coverage_windows"]}, f, indent=1)
    with open(args.out_counter, "w", newline="\n") as f:
        json.dump({"run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
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
                    "ANCHORS", "EXPECTED_DECODE", "MEASURED_BOUNDARIES",
                    "ACTUAL_DECODE", "EXPECTED_CALL_PROMOTION",
                    "ACTUAL_CALL_PROMOTION", "BOUNDARY_SOURCE", "BOUNDARY_STATUS",
                    "CALL_VALIDATION", "REFUTED_BY", "FAILURE_CONDITION_DETECTED",
                    "C1_DEFECT_NOTE"])
        for c in gates["Q5"][1]["counterexamples"]:
            mb = c.get("MEASURED_BOUNDARIES")
            mb_txt = ";".join(mb) if isinstance(mb, list) else json.dumps(mb)
            w.writerow([c["CASE_ID"], c["BYTES"], c["START_OFFSET"],
                        c["CANDIDATE_OFFSET"], c.get("ANCHORS", ""),
                        c["EXPECTED_DECODE"], mb_txt,
                        c["ACTUAL_DECODE"], c["EXPECTED_CALL_PROMOTION"],
                        c["ACTUAL_CALL_PROMOTION"], c["BOUNDARY_SOURCE"],
                        c["BOUNDARY_STATUS"], c.get("CALL_VALIDATION", ""),
                        c.get("REFUTED_BY", ""),
                        c.get("FAILURE_CONDITION_DETECTED", ""),
                        c["C1_DEFECT_NOTE"]])

    # docs gates
    if args.mode == "docs":
        gates["Q14"] = gate_q14(pkg, ctx)

    gate_status = {k: v[0] for k, v in gates.items()}
    mutation_ok = all(r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS" for r in mut_results)
    d2_mutation_ok = all(r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS" for r in d2_mut_results)
    qc_pass = (all(s == "PASS" for s in gate_status.values())
               and mutation_ok and d2_mutation_ok)

    final = {
        "run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
        "qc_scope": "SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION",
        "qc_author": ("executor self-QC (pe-reconstruction worker session; "
                      "NOT an independent audit; the independent Desktop "
                      "post-audit of the published commit remains a separate "
                      "human-relayed step)"),
        "mode": args.mode,
        "gates": gate_status,
        "gate_details": {k: v[1] for k, v in gates.items()},
        "mutation_results_summary": {
            "MUTATION_TEST_COUNT": len(mut_results) + len(d2_mut_results),
            "OLD_MUTATION_TOTAL": len(mut_results),
            "OLD_MUTATION_CAUSAL_PASS_COUNT": sum(
                1 for r in mut_results if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS"),
            "D2_NEW_MUTATION_TOTAL": len(d2_mut_results),
            "D2_NEW_MUTATION_CAUSAL_PASS_COUNT": sum(
                1 for r in d2_mut_results if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS"),
            "MUTATION_CAUSAL_PASS_COUNT": sum(
                1 for r in mut_results + d2_mut_results
                if r["ACTUAL_CAUSALITY"] == "CAUSAL_PASS"),
            "MUTATION_CAUSAL_FAIL_COUNT": sum(
                1 for r in mut_results + d2_mut_results
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
        len(mut_results) + len(d2_mut_results), final["QC_VERDICT"]))


if __name__ == "__main__":
    main()
