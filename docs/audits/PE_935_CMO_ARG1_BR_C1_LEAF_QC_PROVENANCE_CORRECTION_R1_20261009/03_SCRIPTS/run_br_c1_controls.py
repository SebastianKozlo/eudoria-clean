#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_br_c1_controls.py — driver for the correction run
PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009.

Runs under WSL PE-AI (python3 -B). All writes are redirected into this
run's OUTPUT_ROOT: results into PACKAGE, fixtures/mutated copies into
SCRATCH. The predecessor source package and the EXE are READ-ONLY inputs.
The old CLI mains are never invoked; the gate functions are imported as
modules and called as isolated functions with explicit arguments.

Phases:
  pre        — the ACTUAL predecessor gates (imported unmodified from
               SOURCE_PKG/03_SCRIPTS) on the 7 fixed cases (CLEAN, AC1,
               AC2, BR1-BR4). Expected: defect reproduction (BR1-BR4 pass
               both gates = 8 false-PASS outcomes).
  post       — the corrected gates (PACKAGE/03_SCRIPTS copies) on the same
               7 fixed cases (14 outcomes) plus additional single-field
               controls (one per FIELD_CHECK_COVERAGE representation),
               representative missing-field / wrong-type / malformed-expr
               controls; clean final validation uses the same gates.
  regression — the UNCHANGED existing 12-case production byte matrix
               (run_case/EXPECTED/MUTATIONS/derive_*) and 12-case QC byte
               matrix (run_matrix/EXP/MUT/derive_*), all writes in SCRATCH.

The driver never delegates the QC verdict to production or vice versa; it
only records both outcomes. It is not a validator of the facts itself.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback

RUN_ID = "PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009"
PREDECESSOR_RUN_ID = "PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------- case builders

def apply_set(prov, dotted, value):
    cur = prov
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value


def apply_del(prov, dotted):
    cur = prov
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur[p]
    del cur[parts[-1]]


FIXED_CASES = {
    "CLEAN": [],
    "AC1": [("phase_b.nonnull_path.arg1.value_kind", "STACK_READ"),
            ("phase_b.nonnull_path.arg1.value_expr", "MEM(T+0x8)")],
    "AC2": [("phase_a.source_slot.slot_expr_from_E", "[E+0x8]"),
            ("phase_a.source_slot.slot_delta_from_E", 8)],
    "BR1": [("phase_b.nonnull_path.call.target", "0x00528E51"),
            ("phase_b.nonnull_path.call.target_recomputed", "0x00528E51"),
            ("phase_b.nonnull_path.call.bridge_valid", False)],
    "BR2": [("phase_b.nonnull_path.arg1.slot_delta_T0", -12),
            ("phase_b.nonnull_path.arg_slot_deltas.arg1", -12),
            ("bridge.b_arg1_slot", "[T-0xc]")],
    "BR3": [("bridge.b_arg1_value_kind", "STACK_READ"),
            ("bridge.b_arg1_value_expr", "MEM(T+0x8)"),
            ("bridge.cross_call_value_expr", "MEM(T+0x8)")],
    "BR4": [("phase_b.null_path.call_reached", True),
            ("phase_b.null_path.je_taken", False)],
}

# one single-field mutation per FIELD_CHECK_COVERAGE representation
SINGLE_FIELD_MUTATIONS = {
    "SF-C1-1":  ("phase_b.nonnull_path.call.va", "0x004C47C2"),
    "SF-C1-2":  ("phase_b.nonnull_path.call.target", "0x00528E51"),
    "SF-C1-3":  ("phase_b.nonnull_path.call.target_recomputed", "0x00528E51"),
    "SF-C1-4":  ("phase_b.nonnull_path.call.bridge_valid", False),
    "SF-C2-1":  ("phase_b.nonnull_path.arg1.slot_delta_T0", -12),
    "SF-C2-2":  ("phase_b.nonnull_path.arg_slot_deltas.arg1", -12),
    "SF-C2-3":  ("bridge.b_arg1_slot", "[T-0xc]"),
    "SF-C2-4":  ("bridge.a_source_slot_from_T", "[T-0xc]"),
    "SF-C2-5":  ("bridge.E_delta_from_T", -16),
    "SF-C2-6":  ("phase_b.nonnull_path.call.esp_before_call_delta_T0", -12),
    "SF-C2-7":  ("phase_b.nonnull_path.call.callee_entry_esp_delta_T0", -16),
    "SF-C2-8":  ("phase_a.source_slot.slot_expr_from_E", "[E+0x8]"),
    "SF-C2-9":  ("phase_a.source_slot.slot_delta_from_E", 8),
    "SF-C3-1":  ("phase_b.nonnull_path.arg1.value_kind", "STACK_READ"),
    "SF-C3-2":  ("phase_b.nonnull_path.arg1.value_expr", "MEM(T+0x8)"),
    "SF-C3-3":  ("phase_b.nonnull_path.arg1.value_delta", 12),
    "SF-C3-4":  ("phase_b.nonnull_path.arg_slots.arg1.kind", "STACK_READ"),
    "SF-C3-5":  ("phase_b.nonnull_path.arg_slots.arg1.expr", "T0+0xc (computed)"),
    "SF-C3-6":  ("phase_b.nonnull_path.arg_slots.arg1.delta", 12),
    "SF-C3-7":  ("bridge.b_arg1_value_kind", "STACK_READ"),
    "SF-C3-8":  ("bridge.b_arg1_value_expr", "MEM(T+0x8)"),
    "SF-C3-9":  ("bridge.cross_call_value_expr", "MEM(T+0x8)"),
    "SF-C3-10": ("bridge.a_delivered_value_kind", "ADDRESS"),
    "SF-C3-11": ("phase_a.delivery.arg1_value_kind", "ADDRESS"),
    "SF-C3-12": ("phase_a.delivery.arg1_value_expr", "MEM(T+0x8)"),
    "SF-C4-1":  ("phase_b.null_path.branch_va", "0x004C47AE"),
    "SF-C4-2":  ("phase_b.null_path.branch_mnemonic", "jne"),
    "SF-C4-3":  ("phase_b.null_path.exit_va", "0x004C47CC"),
    "SF-C4-4":  ("phase_b.null_path.exit_inside_window", True),
    "SF-C4-5":  ("phase_b.null_path.je_taken", False),
    "SF-C4-6":  ("phase_b.null_path.unconditional_exit", True),
    "SF-C4-7":  ("phase_b.null_path.call_reached", True),
}

MISSING_FIELD_CASES = {
    "MISS-1": "phase_b.nonnull_path.call.target",
    "MISS-2": "phase_b.null_path.je_taken",
    "MISS-3": "bridge.b_arg1_value_kind",
    "MISS-4": "phase_b.nonnull_path.arg_slot_deltas.arg1",
}

WRONG_TYPE_CASES = {
    "TYPE-1": ("phase_b.nonnull_path.call.bridge_valid", "true"),
    "TYPE-2": ("bridge.E_delta_from_T", "-20"),
    "TYPE-3": ("phase_b.null_path.je_taken", 1),
    "TYPE-4": ("phase_b.nonnull_path.arg1.value_delta", "8"),
    "TYPE-5": ("phase_b.nonnull_path.arg1.slot_delta_T0", True),
}

MALFORMED_EXPR_CASES = {
    "MALF-1": ("bridge.b_arg1_slot", "T-0x10"),
    "MALF-2": ("bridge.cross_call_value_expr", "ADDRESS(T+0x8"),
}

# expected failing predicate names per case (the fact predicate under test;
# a hash/manifest/identity-side failure, crash or unrelated predicate
# failure is NOT a successful rejection of the changed fact)
EXPECTED_FAILING = {
    "AC1":    {"P": ["PROV-B-ARG1-KIND", "PROV-B-LEA-EXPR",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
               "Q": ["PROV-B-KIND", "PROV-B-LEA",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "AC2":    {"P": ["PROV-A-SLOT"], "Q": ["PROV-A-SLOT"]},
    "BR1":    {"P": ["PROV-BR11-CALL-TARGET", "PROV-BR11-TARGET-RECOMPUTED",
                     "PROV-BR11-BRIDGE-VALID"],
               "Q": ["QC-BR11-CALL-TARGET", "QC-BR11-TARGET-RECOMPUTED",
                     "QC-BR11-BRIDGE-VALID"]},
    "BR2":    {"P": ["PROV-BR12-ARG1-SLOT-DELTA",
                     "PROV-BR12-ARG-SLOT-DELTAS-ARG1",
                     "PROV-BR12-B-ARG1-SLOT", "PROV-BR12-SLOT-RELATION"],
               "Q": ["QC-BR12-ARG1-SLOT-DELTA",
                     "QC-BR12-ARG-SLOT-DELTAS-ARG1", "QC-BR12-B-ARG1-SLOT",
                     "QC-BR12-SLOT-RELATION"]},
    "BR3":    {"P": ["PROV-BR13-B-ARG1-VALUE-KIND",
                     "PROV-BR13-B-ARG1-VALUE-EXPR",
                     "PROV-BR13-CROSSCALL-VALUE-EXPR",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
               "Q": ["QC-BR13-B-ARG1-VALUE-KIND",
                     "QC-BR13-B-ARG1-VALUE-EXPR",
                     "QC-BR13-CROSSCALL-VALUE-EXPR",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "BR4":    {"P": ["PROV-BR14-NULL-CALL-REACHED", "PROV-BR14-NULL-JE-TAKEN"],
               "Q": ["QC-BR14-NULL-CALL-REACHED", "QC-BR14-NULL-JE-TAKEN"]},
    "SF-C1-1":  {"P": ["PROV-BR11-CALL-VA"], "Q": ["QC-BR11-CALL-VA"]},
    "SF-C1-2":  {"P": ["PROV-BR11-CALL-TARGET"], "Q": ["QC-BR11-CALL-TARGET"]},
    "SF-C1-3":  {"P": ["PROV-BR11-TARGET-RECOMPUTED"],
                 "Q": ["QC-BR11-TARGET-RECOMPUTED"]},
    "SF-C1-4":  {"P": ["PROV-BR11-BRIDGE-VALID"],
                 "Q": ["QC-BR11-BRIDGE-VALID"]},
    "SF-C2-1":  {"P": ["PROV-BR12-ARG1-SLOT-DELTA", "PROV-BR12-SLOT-RELATION"],
                 "Q": ["QC-BR12-ARG1-SLOT-DELTA", "QC-BR12-SLOT-RELATION"]},
    "SF-C2-2":  {"P": ["PROV-BR12-ARG-SLOT-DELTAS-ARG1"],
                 "Q": ["QC-BR12-ARG-SLOT-DELTAS-ARG1"]},
    "SF-C2-3":  {"P": ["PROV-BR12-B-ARG1-SLOT"], "Q": ["QC-BR12-B-ARG1-SLOT"]},
    "SF-C2-4":  {"P": ["PROV-BRIDGE-SLOT"], "Q": ["PROV-BRIDGE-SLOT"]},
    "SF-C2-5":  {"P": ["PROV-BR12-E-DELTA-FROM-T", "PROV-BR12-SLOT-RELATION"],
                 "Q": ["QC-BR12-E-DELTA-FROM-T", "QC-BR12-SLOT-RELATION"]},
    "SF-C2-6":  {"P": ["PROV-BR12-ESP-BEFORE-CALL-DELTA"],
                 "Q": ["QC-BR12-ESP-BEFORE-CALL-DELTA"]},
    "SF-C2-7":  {"P": ["PROV-BR12-CALLEE-ENTRY-DELTA"],
                 "Q": ["QC-BR12-CALLEE-ENTRY-DELTA"]},
    "SF-C2-8":  {"P": ["PROV-A-SLOT"], "Q": ["PROV-A-SLOT"]},
    "SF-C2-9":  {"P": ["PROV-A-SLOT"], "Q": ["PROV-A-SLOT"]},
    "SF-C3-1":  {"P": ["PROV-B-ARG1-KIND", "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["PROV-B-KIND", "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-2":  {"P": ["PROV-B-LEA-EXPR", "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["PROV-B-LEA", "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-3":  {"P": ["PROV-BR13-ARG1-VALUE-DELTA"],
                 "Q": ["QC-BR13-ARG1-VALUE-DELTA"]},
    "SF-C3-4":  {"P": ["PROV-BR13-ARGSLOT-ARG1-KIND",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["QC-BR13-ARGSLOT-ARG1-KIND",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-5":  {"P": ["PROV-BR13-ARGSLOT-ARG1-EXPR"],
                 "Q": ["QC-BR13-ARGSLOT-ARG1-EXPR"]},
    "SF-C3-6":  {"P": ["PROV-BR13-ARGSLOT-ARG1-DELTA"],
                 "Q": ["QC-BR13-ARGSLOT-ARG1-DELTA"]},
    "SF-C3-7":  {"P": ["PROV-BR13-B-ARG1-VALUE-KIND",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["QC-BR13-B-ARG1-VALUE-KIND",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-8":  {"P": ["PROV-BR13-B-ARG1-VALUE-EXPR",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["QC-BR13-B-ARG1-VALUE-EXPR",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-9":  {"P": ["PROV-BR13-CROSSCALL-VALUE-EXPR",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["QC-BR13-CROSSCALL-VALUE-EXPR",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "SF-C3-10": {"P": ["PROV-BR13-A-DELIVERED-KIND"],
                 "Q": ["QC-BR13-A-DELIVERED-KIND"]},
    "SF-C3-11": {"P": ["PROV-BR13-A-DELIVERY-KIND"],
                 "Q": ["QC-BR13-A-DELIVERY-KIND"]},
    "SF-C3-12": {"P": ["PROV-BR13-A-DELIVERY-EXPR"],
                 "Q": ["QC-BR13-A-DELIVERY-EXPR"]},
    "SF-C4-1":  {"P": ["PROV-BR14-NULL-BRANCH-VA"],
                 "Q": ["QC-BR14-NULL-BRANCH-VA"]},
    "SF-C4-2":  {"P": ["PROV-BR14-NULL-BRANCH-MNEMONIC"],
                 "Q": ["QC-BR14-NULL-BRANCH-MNEMONIC"]},
    "SF-C4-3":  {"P": ["PROV-BR14-NULL-EXIT-VA"],
                 "Q": ["QC-BR14-NULL-EXIT-VA"]},
    "SF-C4-4":  {"P": ["PROV-BR14-NULL-EXIT-INSIDE"],
                 "Q": ["QC-BR14-NULL-EXIT-INSIDE"]},
    "SF-C4-5":  {"P": ["PROV-BR14-NULL-JE-TAKEN"],
                 "Q": ["QC-BR14-NULL-JE-TAKEN"]},
    "SF-C4-6":  {"P": ["PROV-BR14-NULL-UNCONDITIONAL"],
                 "Q": ["QC-BR14-NULL-UNCONDITIONAL"]},
    "SF-C4-7":  {"P": ["PROV-BR14-NULL-CALL-REACHED"],
                 "Q": ["QC-BR14-NULL-CALL-REACHED"]},
    "MISS-1":   {"P": ["PROV-BR11-CALL-TARGET"],
                 "Q": ["QC-BR11-CALL-TARGET"]},
    "MISS-2":   {"P": ["PROV-BR14-NULL-JE-TAKEN"],
                 "Q": ["QC-BR14-NULL-JE-TAKEN"]},
    "MISS-3":   {"P": ["PROV-BR13-B-ARG1-VALUE-KIND",
                     "PROV-BR13-PARALLEL-CONSISTENCY"],
                 "Q": ["QC-BR13-B-ARG1-VALUE-KIND",
                     "QC-BR13-PARALLEL-CONSISTENCY"]},
    "MISS-4":   {"P": ["PROV-BR12-ARG-SLOT-DELTAS-ARG1"],
                 "Q": ["QC-BR12-ARG-SLOT-DELTAS-ARG1"]},
    "TYPE-1":   {"P": ["PROV-BR11-BRIDGE-VALID"],
                 "Q": ["QC-BR11-BRIDGE-VALID"]},
    "TYPE-2":   {"P": ["PROV-BR12-E-DELTA-FROM-T", "PROV-BR12-SLOT-RELATION"],
                 "Q": ["QC-BR12-E-DELTA-FROM-T", "QC-BR12-SLOT-RELATION"]},
    "TYPE-3":   {"P": ["PROV-BR14-NULL-JE-TAKEN"],
                 "Q": ["QC-BR14-NULL-JE-TAKEN"]},
    "TYPE-4":   {"P": ["PROV-BR13-ARG1-VALUE-DELTA"],
                 "Q": ["QC-BR13-ARG1-VALUE-DELTA"]},
    "TYPE-5":   {"P": ["PROV-BR12-ARG1-SLOT-DELTA", "PROV-BR12-SLOT-RELATION"],
                 "Q": ["QC-BR12-ARG1-SLOT-DELTA", "QC-BR12-SLOT-RELATION"]},
    "MALF-1":   {"P": ["PROV-BR12-B-ARG1-SLOT"],
                 "Q": ["QC-BR12-B-ARG1-SLOT"]},
    "MALF-2":   {"P": ["PROV-BR13-CROSSCALL-VALUE-EXPR"],
                 "Q": ["QC-BR13-CROSSCALL-VALUE-EXPR"]},
}


def build_case(prov_clean, case, scratch, phase):
    """Deep-copy the clean provenance and apply the case mutation.
    CLEAN returns (None, no copy) — the gate reads the package original."""
    if case == "CLEAN":
        return None, []
    prov = copy.deepcopy(prov_clean)
    notes = []
    if case in FIXED_CASES:
        for dotted, value in FIXED_CASES[case]:
            apply_set(prov, dotted, value)
            notes.append("%s=%r" % (dotted, value))
    elif case in SINGLE_FIELD_MUTATIONS:
        dotted, value = SINGLE_FIELD_MUTATIONS[case]
        apply_set(prov, dotted, value)
        notes.append("%s=%r (single-field; all other representations left "
                     "clean)" % (dotted, value))
    elif case in MISSING_FIELD_CASES:
        dotted = MISSING_FIELD_CASES[case]
        apply_del(prov, dotted)
        notes.append("DELETE %s (missing field)" % dotted)
    elif case in WRONG_TYPE_CASES:
        dotted, value = WRONG_TYPE_CASES[case]
        apply_set(prov, dotted, value)
        notes.append("%s=%r (wrong native JSON type)" % (dotted, value))
    elif case in MALFORMED_EXPR_CASES:
        dotted, value = MALFORMED_EXPR_CASES[case]
        apply_set(prov, dotted, value)
        notes.append("%s=%r (malformed supported expression)" % (dotted,
                                                                value))
    else:
        raise ValueError("unknown case " + case)
    os.makedirs(os.path.join(scratch, "prov"), exist_ok=True)
    path = os.path.join(scratch, "prov", "%s_%s.json" % (phase, case))
    with open(path, "w") as fh:
        json.dump(prov, fh, indent=2)
    return path, notes


# --------------------------------------------------------------- gate wrappers

HASH_SIDE_PREFIXES = ("WID-", "EFL-", "CSL-")


def run_prod_gate(mod, source_pkg, prov_path):
    """Call the production gate_artifacts with explicit arguments. Returns a
    result record; never lets an exception escape silently."""
    call = {"function": "gate_artifacts", "repo_out": source_pkg,
            "prov_path_override": prov_path}
    try:
        checks, verdict = mod.gate_artifacts(source_pkg,
                                             prov_path_override=prov_path)
        failing = [c["check"] for c in checks if not c["pass"]]
        diags = [c.get("diagnostic") for c in checks
                 if not c["pass"] and "diagnostic" in c]
        rec = {"call": call, "verdict": verdict, "exception": None,
              "all_checks_count": len(checks),
              "pass_count": sum(1 for c in checks if c["pass"]),
              "failing_checks": failing,
              "hash_side_failures": [c for c in failing
                                     if c.startswith(HASH_SIDE_PREFIXES)],
              "brc1_diagnostics": diags,
              "checks": checks}
        return rec
    except Exception:
        rec = {"call": call, "verdict": "EXCEPTION", "exception":
               traceback.format_exc(limit=12), "failing_checks": [],
               "hash_side_failures": [], "brc1_diagnostics": []}
        return rec


def run_qc_gate(mod, source_pkg, prov_path):
    """Call the QC gate with explicit arguments (WORK routed to scratch by
    the caller via module attribute patch)."""
    call = {"function": "gate", "pkg": source_pkg, "prov_override":
            prov_path}
    try:
        checks, verdict = mod.gate(source_pkg, prov_override=prov_path)
        failing = [c["check"] for c in checks if not c["ok"]]
        diags = [c.get("diagnostic") for c in checks
                 if not c["ok"] and "diagnostic" in c]
        rec = {"call": call, "verdict": verdict, "exception": None,
              "all_checks_count": len(checks),
              "pass_count": sum(1 for c in checks if c["ok"]),
              "failing_checks": failing,
              "hash_side_failures": [c for c in failing
                                     if c.startswith(HASH_SIDE_PREFIXES)],
              "brc1_diagnostics": diags,
              "checks": checks}
        return rec
    except Exception:
        rec = {"call": call, "verdict": "EXCEPTION", "exception":
               traceback.format_exc(limit=12), "failing_checks": [],
               "hash_side_failures": [], "brc1_diagnostics": []}
        return rec


def evaluate_case(case, gate, rec, expect_reject):
    """Classify one gate outcome. A rejection is a SUCCESSFUL rejection only
    if the verdict is REJECTED, no hash/identity-side check failed, and the
    expected BR-C1 fact predicate(s) are among the failing checks."""
    exp = EXPECTED_FAILING.get(case, {}).get("P" if gate == "PRODUCTION"
                                            else "Q", [])
    rec["expected_failing_predicates"] = exp
    if case == "CLEAN":
        ok = (rec["verdict"] == "PASS" and rec["pass_count"]
              == rec["all_checks_count"])
        rec["outcome"] = "CLEAN_PASS_OK" if ok else "CLEAN_FAIL_UNEXPECTED"
        return ok
    if expect_reject:
        ok = (rec["verdict"] == "REJECTED"
              and not rec["hash_side_failures"]
              and rec["exception"] is None
              and bool(set(exp) & set(rec["failing_checks"])))
    else:
        # PRE phase: the predecessor gate is expected to be defective
        ok = (rec["verdict"] in ("PASS", "REJECTED")
              and rec["exception"] is None)
    rec["outcome"] = ("REJECTION_OK" if ok else
                      ("REJECTED" if rec["verdict"] == "REJECTED"
                       else rec["verdict"]))
    return ok


# --------------------------------------------------------------- phases

def phase_pre(args, prov_clean, prov_sha):
    print("[pre] loading ACTUAL predecessor gates ...")
    prod = load_module(os.path.join(args.source_pkg, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_pre")
    qc = load_module(os.path.join(args.source_pkg, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_pre")
    qc_wd = os.path.join(args.scratch, "qc_work", "pre")
    os.makedirs(qc_wd, exist_ok=True)
    qc.WORK = qc_wd
    rec = {
        "phase": "PRE",
        "description": "ACTUAL predecessor gates (imported unmodified from "
                       "the source package at BASE_SHA) on the 7 fixed "
                       "cases; deep-copied JSON loaded through their normal "
                       "provenance override",
        "source_pkg": args.source_pkg,
        "predecessor_module_sha256": {
            "run_frame_bridge.py":
                sha256_file(os.path.join(args.source_pkg, "03_SCRIPTS",
                                         "run_frame_bridge.py")),
            "qc_frame_bridge.py":
                sha256_file(os.path.join(args.source_pkg, "03_SCRIPTS",
                                         "qc_frame_bridge.py"))},
        "clean_provenance_sha256": prov_sha,
        "cases": {},
    }
    for case in ["CLEAN", "AC1", "AC2", "BR1", "BR2", "BR3", "BR4"]:
        prov_path, notes = build_case(prov_clean, case, args.scratch, "pre")
        c = {"mutation_fields": notes,
             "prov_copy": (sha256_file(prov_path)
                           if prov_path else "PACKAGE_ORIGINAL")}
        pr = run_prod_gate(prod, args.source_pkg, prov_path)
        qr = run_qc_gate(qc, args.source_pkg, prov_path)
        evaluate_case(case, "PRODUCTION", pr, expect_reject=False)
        evaluate_case(case, "QC", qr, expect_reject=False)
        c["production"] = pr
        c["qc"] = qr
        rec["cases"][case] = c
        print("  %-5s PROD=%s QC=%s" % (case, pr["verdict"], qr["verdict"]))
    br_pass = sum(1 for b in ("BR1", "BR2", "BR3", "BR4")
                  if rec["cases"][b]["production"]["verdict"] == "PASS"
                  and rec["cases"][b]["qc"]["verdict"] == "PASS")
    clean_ok = (rec["cases"]["CLEAN"]["production"]["verdict"] == "PASS"
                and rec["cases"]["CLEAN"]["qc"]["verdict"] == "PASS")
    ac_rej = sum(1 for a in ("AC1", "AC2")
                 if rec["cases"][a]["production"]["verdict"] == "REJECTED"
                 and rec["cases"][a]["qc"]["verdict"] == "REJECTED")
    rec["pre_reproduction"] = {
        "clean_pass_both_gates": clean_ok,
        "ac1_ac2_rejected_both_gates": ac_rej,
        "br1_br4_false_pass_both_gates": br_pass,
        "defect_reproduced": bool(clean_ok and ac_rej == 2 and br_pass == 4),
        "false_pass_outcomes": br_pass * 2,
    }
    return rec, prod, qc


def phase_post(args, prov_clean, prov_sha):
    print("[post] loading corrected gates ...")
    prod = load_module(os.path.join(args.package, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_post")
    qc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_post")
    qc_wd = os.path.join(args.scratch, "qc_work", "post")
    os.makedirs(qc_wd, exist_ok=True)
    qc.WORK = qc_wd
    rec = {
        "phase": "POST",
        "description": "corrected gates on the fixed 7-case matrix (14 "
                       "outcomes) + additional single-field / missing-field / "
                       "wrong-type / malformed-expr controls through the "
                       "SAME gates; clean final validation uses the same "
                       "gate functions",
        "source_pkg": args.source_pkg,
        "corrected_module_sha256": {
            "run_frame_bridge.py":
                sha256_file(os.path.join(args.package, "03_SCRIPTS",
                                         "run_frame_bridge.py")),
            "qc_frame_bridge.py":
                sha256_file(os.path.join(args.package, "03_SCRIPTS",
                                         "qc_frame_bridge.py"))},
        "clean_provenance_sha256": prov_sha,
        "fixed_cases": {},
        "additional_cases": {},
    }
    fixed_ok = 0
    fixed_total = 0
    for case in ["CLEAN", "AC1", "AC2", "BR1", "BR2", "BR3", "BR4"]:
        prov_path, notes = build_case(prov_clean, case, args.scratch, "post")
        c = {"mutation_fields": notes,
             "prov_copy": (sha256_file(prov_path)
                           if prov_path else "PACKAGE_ORIGINAL")}
        pr = run_prod_gate(prod, args.source_pkg, prov_path)
        qr = run_qc_gate(qc, args.source_pkg, prov_path)
        okp = evaluate_case(case, "PRODUCTION", pr, expect_reject=True)
        okq = evaluate_case(case, "QC", qr, expect_reject=True)
        c["production"] = pr
        c["qc"] = qr
        rec["fixed_cases"][case] = c
        fixed_total += 2
        fixed_ok += int(okp) + int(okq)
        print("  %-5s PROD=%s(%s) QC=%s(%s)"
              % (case, pr["verdict"], pr["outcome"], qr["verdict"],
                 qr["outcome"]))
    rec["fixed_matrix"] = {"expected_outcomes": fixed_total,
                           "correct_outcomes": fixed_ok}
    # additional controls
    add_cases = (["SF-%s" % i for i in
                  ["C1-1", "C1-2", "C1-3", "C1-4",
                   "C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7",
                   "C2-8", "C2-9",
                   "C3-1", "C3-2", "C3-3", "C3-4", "C3-5", "C3-6", "C3-7",
                   "C3-8", "C3-9", "C3-10", "C3-11", "C3-12",
                   "C4-1", "C4-2", "C4-3", "C4-4", "C4-5", "C4-6", "C4-7"]]
                 + ["MISS-1", "MISS-2", "MISS-3", "MISS-4",
                    "TYPE-1", "TYPE-2", "TYPE-3", "TYPE-4", "TYPE-5",
                    "MALF-1", "MALF-2"])
    add_ok = 0
    add_total = 0
    for case in add_cases:
        prov_path, notes = build_case(prov_clean, case, args.scratch, "post")
        c = {"mutation_fields": notes,
             "prov_copy": sha256_file(prov_path)}
        pr = run_prod_gate(prod, args.source_pkg, prov_path)
        qr = run_qc_gate(qc, args.source_pkg, prov_path)
        okp = evaluate_case(case, "PRODUCTION", pr, expect_reject=True)
        okq = evaluate_case(case, "QC", qr, expect_reject=True)
        c["production"] = {k: pr[k] for k in
                           ("call", "verdict", "exception",
                            "all_checks_count", "pass_count",
                            "failing_checks", "hash_side_failures",
                            "brc1_diagnostics", "expected_failing_predicates",
                            "outcome")}
        c["qc"] = {k: qr[k] for k in
                   ("call", "verdict", "exception", "all_checks_count",
                    "pass_count", "failing_checks", "hash_side_failures",
                    "brc1_diagnostics", "expected_failing_predicates",
                    "outcome")}
        rec["additional_cases"][case] = c
        add_total += 2
        add_ok += int(okp) + int(okq)
        print("  %-8s PROD=%s QC=%s ok=%d"
              % (case, pr["verdict"], qr["verdict"], int(okp) + int(okq)))
    rec["additional_matrix"] = {"cases": len(add_cases),
                               "outcomes": add_total,
                               "correct_outcomes": add_ok,
                               "single_field_cases": 32,
                               "missing_field_cases": 4,
                               "wrong_type_cases": 5,
                               "malformed_expr_cases": 2}
    # clean final validation re-run (same gates; no override)
    pr = run_prod_gate(prod, args.source_pkg, None)
    qr = run_qc_gate(qc, args.source_pkg, None)
    rec["clean_final_validation"] = {
        "production_verdict": pr["verdict"],
        "production_checks": pr["all_checks_count"],
        "production_failing": pr["failing_checks"],
        "qc_verdict": qr["verdict"],
        "qc_checks": qr["all_checks_count"],
        "qc_failing": qr["failing_checks"],
    }
    print("[post] clean final: PROD=%s (%d checks) QC=%s (%d checks)"
          % (pr["verdict"], pr["all_checks_count"], qr["verdict"],
             qr["all_checks_count"]))
    return rec, prod, qc


def phase_regression(args):
    print("[regression] 12-case production + 12-case QC byte matrix ...")
    prod = load_module(os.path.join(args.package, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_reg")
    qc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_reg")
    prod_pre = load_module(os.path.join(args.source_pkg, "03_SCRIPTS",
                                       "run_frame_bridge.py"), "prod_reg_pre")
    qc_pre = load_module(os.path.join(args.source_pkg, "03_SCRIPTS",
                                     "qc_frame_bridge.py"), "qc_reg_pre")
    # unchanged-helper preservation proofs (mechanical, no re-derivation)
    preserved = {
        "production_EXPECTED_identical": prod.EXPECTED == prod_pre.EXPECTED,
        "production_MUTATIONS_identical": prod.MUTATIONS == prod_pre.MUTATIONS,
        "production_CASE_ORDER_identical": prod.CASE_ORDER == prod_pre.CASE_ORDER,
        "qc_EXP_identical": qc.EXP == qc_pre.EXP,
        "qc_MUT_identical": qc.MUT == qc_pre.MUT,
        "qc_CASE_ORDER_identical": qc.CASE_ORDER == qc_pre.CASE_ORDER,
    }
    exe_sha_before = sha256_file(prod.EXE_PATH)
    ver, rc = prod.objdump_version()
    tool_header = "Tool: %s\n" % ver
    reg_out = os.path.join(args.scratch, "reg_prod_out")
    reg_work = os.path.join(args.scratch, "reg_prod_work")
    os.makedirs(os.path.join(reg_out, "01_RAW", "CONTROLS"), exist_ok=True)
    os.makedirs(reg_work, exist_ok=True)
    prod_cases = []
    for case in prod.CASE_ORDER:
        crec = prod.run_case(case, reg_out, reg_work, tool_header)
        prod_cases.append(crec)
        print("  PROD %-22s %s" % (case, crec["verdict"]))
    qc_wd = os.path.join(args.scratch, "qc_work", "reg")
    os.makedirs(qc_wd, exist_ok=True)
    qc.WORK = qc_wd
    qc_cases = qc.run_matrix()
    for crec in qc_cases:
        print("  QC   %-22s %s" % (crec["case"], crec["verdict"]))
    exe_sha_after = sha256_file(prod.EXE_PATH)
    n_prod_pass = sum(1 for c in prod_cases if c["verdict"] == "CONTROL_PASS")
    n_qc_pass = sum(1 for c in qc_cases if c["verdict"] == "CONTROL_PASS")
    # M5/M7 arg1-unchanged / other-channel-changed verification (reported
    # alongside; derived from the recorded case facts)
    def prod_facts(case):
        for c in prod_cases:
            if c["case"] == case:
                return c.get("derived_facts", {})
        return {}
    clean_facts = prod_facts("B_CLEAN_NONNULL")
    m5 = prod_facts("M5_B_EARLY_PUSH_ORDER")
    m7 = prod_facts("M7_B_RECEIVER_ONLY")
    m5_check = {
        "arg1_kind_unchanged": (m5.get("arg1_kind")
                                == clean_facts.get("arg1_kind")),
        "arg1_expr_unchanged": (m5.get("arg1_expr")
                                == clean_facts.get("arg1_expr")),
        "arg1_slot_unchanged": (m5.get("arg1_slot_delta")
                                == clean_facts.get("arg1_slot_delta")),
        "arg3_changed_vs_clean": (m5.get("arg3_expr")
                                   != clean_facts.get("arg3_expr")),
        "arg4_changed_vs_clean": (m5.get("arg4_expr")
                                   != clean_facts.get("arg4_expr")),
        "arg3_is_clean_arg4": (m5.get("arg3_expr")
                               == clean_facts.get("arg4_expr")),
        "arg4_is_clean_arg3": (m5.get("arg4_expr")
                               == clean_facts.get("arg3_expr")),
    }
    m7_check = {
        "arg1_kind_unchanged": (m7.get("arg1_kind")
                                == clean_facts.get("arg1_kind")),
        "arg1_expr_unchanged": (m7.get("arg1_expr")
                                == clean_facts.get("arg1_expr")),
        "arg1_slot_unchanged": (m7.get("arg1_slot_delta")
                                == clean_facts.get("arg1_slot_delta")),
        "receiver_changed_vs_clean": (m7.get("receiver_kind")
                                      != clean_facts.get("receiver_kind")),
    }
    def qc_derived(case):
        for c in qc_cases:
            if c["case"] == case:
                return c.get("derived", {})
        return {}
    qc_clean, qc_m5, qc_m7 = (qc_derived("B_CLEAN_NONNULL"),
                              qc_derived("M5_B_EARLY_PUSH_ORDER"),
                              qc_derived("M7_B_RECEIVER_ONLY"))
    qc_m5_check = {
        "arg1_kind_unchanged": (qc_m5.get("arg1_kind")
                                == qc_clean.get("arg1_kind")),
        "arg1_slot_unchanged": (qc_m5.get("arg1_slot")
                                == qc_clean.get("arg1_slot")),
        "arg3_swapped": (qc_m5.get("aslots", {}).get("a3")
                         == qc_clean.get("aslots", {}).get("a4")),
        "arg4_swapped": (qc_m5.get("aslots", {}).get("a4")
                         == qc_clean.get("aslots", {}).get("a3")),
    }
    qc_m7_check = {
        "arg1_kind_unchanged": (qc_m7.get("arg1_kind")
                                == qc_clean.get("arg1_kind")),
        "arg1_slot_unchanged": (qc_m7.get("arg1_slot")
                                == qc_clean.get("arg1_slot")),
        "receiver_changed_vs_clean": (qc_m7.get("recv_kind")
                                      != qc_clean.get("recv_kind")),
    }
    rec = {
        "phase": "REGRESSION",
        "description": "re-execution of the UNCHANGED existing 12-case "
                       "production byte matrix (run_case/EXPECTED/MUTATIONS) "
                       "and 12-case QC byte matrix (run_matrix/EXP/MUT) "
                       "through the corrected copies' preserved helpers; "
                       "all writes redirected to SCRATCH",
        "tool": {"name": ver, "rc": rc},
        "exe_sha256_before": exe_sha_before,
        "exe_sha256_after": exe_sha_after,
        "exe_unchanged": (exe_sha_before == exe_sha_after
                          == prod.EXE_SHA256),
        "unchanged_helper_preservation": preserved,
        "production_cases": [{k: c[k] for k in
                              ("case", "window", "input_kind", "mutation",
                               "fixture", "objdump", "decode",
                               "derived_facts", "expected_text", "checks",
                               "verdict")} for c in prod_cases],
        "qc_cases": qc_cases,
        "summary": {
            "production_control_pass": n_prod_pass,
            "production_total": len(prod_cases),
            "qc_control_pass": n_qc_pass,
            "qc_total": len(qc_cases),
            "required_byte_matrix": "correct outcomes / 24",
            "correct_outcomes": n_prod_pass + n_qc_pass,
            "m5_production": m5_check,
            "m7_production": m7_check,
            "m5_qc": qc_m5_check,
            "m7_qc": qc_m7_check,
        },
        "scratch_paths": {"production_raw_out": reg_out,
                          "production_work": reg_work,
                          "qc_work": qc_wd},
    }
    return rec


# --------------------------------------------------------------- coverage CSV

FIELD_CHECK_COVERAGE = [
    # (field_id, relation, persisted_field_path, production_check, qc_check,
    #  single_field_case, evidence, why_non_circular)
    ("F-C1-1", "BR-C1.1", "phase_b.nonnull_path.call.va",
     "PROV-BR11-CALL-VA", "QC-BR11-CALL-VA", "SF-C1-1",
     "decoded window-B stream (persisted objdump text verified against the "
     "physical EXE window bytes by SHA256)",
     "the pinned callsite VA comes from the decoded instruction stream, "
     "not from the JSON field under test"),
    ("F-C1-2", "BR-C1.1", "phase_b.nonnull_path.call.target",
     "PROV-BR11-CALL-TARGET", "QC-BR11-CALL-TARGET", "SF-C1-2",
     "rel32 recompute of the physical call instruction bytes at "
     "0x004C47C1 (e8 8a 46 06 00)",
     "the expected target is recomputed from bytes; a persisted wrong "
     "target (BR1/SF-C1-2) is rejected without following it"),
    ("F-C1-3", "BR-C1.1", "phase_b.nonnull_path.call.target_recomputed",
     "PROV-BR11-TARGET-RECOMPUTED", "QC-BR11-TARGET-RECOMPUTED", "SF-C1-3",
     "same rel32 recompute; both exported target fields must match it",
     "duplicate target claims are each compared to the byte-derived value, "
     "not only to each other"),
    ("F-C1-4", "BR-C1.1", "phase_b.nonnull_path.call.bridge_valid",
     "PROV-BR11-BRIDGE-VALID", "QC-BR11-BRIDGE-VALID", "SF-C1-4",
     "derived bridge predicate: rel32 target == window-A entry 0x00528E50",
     "JSON boolean compared to the derived predicate with native type "
     "enforcement; string 'true' rejected (TYPE-1)"),
    ("F-C2-1", "BR-C1.2", "phase_b.nonnull_path.arg1.slot_delta_T0",
     "PROV-BR12-ARG1-SLOT-DELTA", "QC-BR12-ARG1-SLOT-DELTA", "SF-C2-1",
     "independent arithmetic ESP walk over the decoded window-B stream: "
     "ESP at the bridge call minus ESP at the T pivot = -0x10",
     "expected delta derived from the walk, never from the JSON; JSON "
     "booleans rejected as integers (TYPE-5)"),
    ("F-C2-2", "BR-C1.2", "phase_b.nonnull_path.arg_slot_deltas.arg1",
     "PROV-BR12-ARG-SLOT-DELTAS-ARG1", "QC-BR12-ARG-SLOT-DELTAS-ARG1",
     "SF-C2-2", "same walk-derived slot delta",
     "parallel slot claim compared individually to the walk-derived value"),
    ("F-C2-3", "BR-C1.2", "bridge.b_arg1_slot",
     "PROV-BR12-B-ARG1-SLOT", "QC-BR12-B-ARG1-SLOT", "SF-C2-3",
     "walk-derived slot delta formatted as [T-0x10]",
     "expression compared to the derived slot expression; malformed form "
     "rejected (MALF-1)"),
    ("F-C2-4", "BR-C1.2", "bridge.a_source_slot_from_T",
     "PROV-BRIDGE-SLOT", "PROV-BRIDGE-SLOT", "SF-C2-4",
     "derived join: E delta + A entry delta = -0x14 + 4 = -0x10, equal to "
     "the B-side prepared slot",
     "the slot-address identity [E+4]==[T-0x10] is derived from both "
     "sides of the join, not read from the JSON"),
    ("F-C2-5", "BR-C1.2", "bridge.E_delta_from_T",
     "PROV-BR12-E-DELTA-FROM-T", "QC-BR12-E-DELTA-FROM-T", "SF-C2-5",
     "walk-derived callee-entry ESP delta (ESP before the call minus the "
     "hardware return push) = -0x14",
     "expected E delta derived from the walk + AS1 call semantics"),
    ("F-C2-6", "BR-C1.2", "phase_b.nonnull_path.call."
     "esp_before_call_delta_T0", "PROV-BR12-ESP-BEFORE-CALL-DELTA",
     "QC-BR12-ESP-BEFORE-CALL-DELTA", "SF-C2-6",
     "same walk: ESP at the bridge call = T-0x10",
     "cross-checked with the same walk used for the slot delta"),
    ("F-C2-7", "BR-C1.2", "phase_b.nonnull_path.call."
     "callee_entry_esp_delta_T0", "PROV-BR12-CALLEE-ENTRY-DELTA",
     "QC-BR12-CALLEE-ENTRY-DELTA", "SF-C2-7",
     "same walk: callee-entry ESP = T-0x14",
     "cross-checked with the same walk used for the E delta"),
    ("F-C2-8", "BR-C1.2", "phase_a.source_slot.slot_expr_from_E",
     "PROV-A-SLOT", "PROV-A-SLOT", "SF-C2-8",
     "A-side derivation: source-load displacement byte 0x3C + S=E-0x38 "
     "from the A-window walk -> [E+0x4]",
     "the A entry slot [E+4] is re-derived from bytes; AC2/SF-C2-8 "
     "rejected"),
    ("F-C2-9", "BR-C1.2", "phase_a.source_slot.slot_delta_from_E",
     "PROV-A-SLOT", "PROV-A-SLOT", "SF-C2-9",
     "same A-side derivation (delta 4)",
     "delta re-derived from the displacement byte and the ESP chain"),
    ("F-C2-R", "BR-C1.2", "(relation) E_delta_from_T + 4 == arg1 "
     "slot_delta_T0 (entry slot [E+4] == [T-0x10])",
     "PROV-BR12-SLOT-RELATION", "QC-BR12-SLOT-RELATION", "SF-C2-5",
     "derived relation: walk-derived E delta + walk-derived A entry delta "
     "== walk-derived B slot delta; persisted claims must satisfy the same "
     "relation",
     "the relation is derived from the walk on both sides of the join, "
     "not by comparing duplicate claims to each other only"),
    ("F-C3-1", "BR-C1.3", "phase_b.nonnull_path.arg1.value_kind",
     "PROV-B-ARG1-KIND", "PROV-B-KIND", "SF-C3-1",
     "opcode byte of the instruction at 0x004C47BA (8d = LEA -> ADDRESS; "
     "8b = MOV -> STACK_READ)",
     "kind derived from the physical opcode byte, not from the JSON; "
     "AC1/SF-C3-1 rejected"),
    ("F-C3-2", "BR-C1.3", "phase_b.nonnull_path.arg1.value_expr",
     "PROV-B-LEA-EXPR", "PROV-B-LEA", "SF-C3-2",
     "LEA displacement byte 0x14 + walk ESP at the LEA (T-0xC) -> "
     "ADDRESS(T+0x8)",
     "pointer value derived from bytes; the clean pointer is "
     "ADDRESS(T+8), never MEM(T+8)"),
    ("F-C3-3", "BR-C1.3", "phase_b.nonnull_path.arg1.value_delta",
     "PROV-BR13-ARG1-VALUE-DELTA", "QC-BR13-ARG1-VALUE-DELTA", "SF-C3-3",
     "same LEA derivation (delta 8); native JSON integer enforced",
     "delta derived from the LEA displacement + ESP chain"),
    ("F-C3-4", "BR-C1.3", "phase_b.nonnull_path.arg_slots.arg1.kind",
     "PROV-BR13-ARGSLOT-ARG1-KIND", "QC-BR13-ARGSLOT-ARG1-KIND", "SF-C3-4",
     "same opcode-derived kind",
     "parallel kind claim compared individually to the opcode-derived kind"),
    ("F-C3-5", "BR-C1.3", "phase_b.nonnull_path.arg_slots.arg1.expr",
     "PROV-BR13-ARGSLOT-ARG1-EXPR", "QC-BR13-ARGSLOT-ARG1-EXPR", "SF-C3-5",
     "same LEA-derived delta 8, in the finite documented 'T0+0x8 "
     "(computed)' form (suffix explicitly normalized)",
     "the documented form is normalized to the derived delta; a different "
     "delta is rejected"),
    ("F-C3-6", "BR-C1.3", "phase_b.nonnull_path.arg_slots.arg1.delta",
     "PROV-BR13-ARGSLOT-ARG1-DELTA", "QC-BR13-ARGSLOT-ARG1-DELTA", "SF-C3-6",
     "same LEA derivation (delta 8)",
     "parallel delta claim compared individually to the derivation"),
    ("F-C3-7", "BR-C1.3", "bridge.b_arg1_value_kind",
     "PROV-BR13-B-ARG1-VALUE-KIND", "QC-BR13-B-ARG1-VALUE-KIND", "SF-C3-7",
     "same opcode-derived kind (individual check; OR-fallback removed)",
     "the bridge summary kind is no longer masked by the first "
     "representation; BR3/SF-C3-7 rejected"),
    ("F-C3-8", "BR-C1.3", "bridge.b_arg1_value_expr",
     "PROV-BR13-B-ARG1-VALUE-EXPR", "QC-BR13-B-ARG1-VALUE-EXPR", "SF-C3-8",
     "same LEA-derived pointer value ADDRESS(T+0x8) (individual check)",
     "the bridge summary expr is no longer masked by the first "
     "representation; BR3/SF-C3-8 rejected"),
    ("F-C3-9", "BR-C1.3", "bridge.cross_call_value_expr",
     "PROV-BR13-CROSSCALL-VALUE-EXPR", "QC-BR13-CROSSCALL-VALUE-EXPR",
     "SF-C3-9", "same LEA-derived pointer value (individual check)",
     "cross-call summary compared individually; malformed form rejected "
     "(MALF-2)"),
    ("F-C3-10", "BR-C1.3", "bridge.a_delivered_value_kind",
     "PROV-BR13-A-DELIVERED-KIND", "QC-BR13-A-DELIVERED-KIND", "SF-C3-10",
     "A-side derivation: the delivered value is the STACK_READ of the "
     "joined argument slot [E+4] at 0x00528E84",
     "A's STACK_READ is validated as the argument-slot load (the "
     "transmitted pointer), never reclassified as a B-side pointee read"),
    ("F-C3-11", "BR-C1.3", "phase_a.delivery.arg1_value_kind",
     "PROV-BR13-A-DELIVERY-KIND", "QC-BR13-A-DELIVERY-KIND", "SF-C3-11",
     "same A-side derivation",
     "kind derived from the A-window load, not from the JSON"),
    ("F-C3-12", "BR-C1.3", "phase_a.delivery.arg1_value_expr",
     "PROV-BR13-A-DELIVERY-EXPR", "QC-BR13-A-DELIVERY-EXPR", "SF-C3-12",
     "A-side derivation: MEM(E+0x4)@0x00528E84 (the argument-slot load)",
     "expr re-derived from the load slot + pinned load VA"),
    ("F-C3-P", "BR-C1.3", "(consistency) arg1.value_kind == arg_slots.arg1."
     "kind == bridge.b_arg1_value_kind; arg1.value_expr == b_arg1_value_expr "
     "== cross_call_value_expr",
     "PROV-BR13-PARALLEL-CONSISTENCY", "QC-BR13-PARALLEL-CONSISTENCY",
     "SF-C3-7", "LEA/opcode-derived kind + LEA-derived pointer value",
     "all parallel representations must agree with the derivation AND with "
     "each other; a contradictory parallel representation cannot be hidden "
     "by a fallback"),
    ("F-C4-1", "BR-C1.4", "phase_b.null_path.branch_va",
     "PROV-BR14-NULL-BRANCH-VA", "QC-BR14-NULL-BRANCH-VA", "SF-C4-1",
     "decoded branch instruction at 0x004C47AD in the persisted objdump "
     "text (verified against the physical window bytes)",
     "branch VA derived from the decoded stream"),
    ("F-C4-2", "BR-C1.4", "phase_b.null_path.branch_mnemonic",
     "PROV-BR14-NULL-BRANCH-MNEMONIC", "QC-BR14-NULL-BRANCH-MNEMONIC",
     "SF-C4-2", "decoded instruction mnemonic 'je' (opcode 0x74)",
     "mnemonic derived from the decoded stream"),
    ("F-C4-3", "BR-C1.4", "phase_b.null_path.exit_va",
     "PROV-BR14-NULL-EXIT-VA", "QC-BR14-NULL-EXIT-VA", "SF-C4-3",
     "decoded JE target 0x4c47c8 -> 0x004C47C8 (unopened; no later-behavior "
     "claim)",
     "exit VA derived from the decoded JE operands"),
    ("F-C4-4", "BR-C1.4", "phase_b.null_path.exit_inside_window",
     "PROV-BR14-NULL-EXIT-INSIDE", "QC-BR14-NULL-EXIT-INSIDE", "SF-C4-4",
     "window-B interval [0x004C4792,0x004C47C6): 0x004C47C8 lies outside",
     "derived from the decoded target and the window interval; native JSON "
     "boolean enforced"),
    ("F-C4-5", "BR-C1.4", "phase_b.null_path.je_taken",
     "PROV-BR14-NULL-JE-TAKEN", "QC-BR14-NULL-JE-TAKEN", "SF-C4-5",
     "B-window branch derivation: TEST EAX,EAX sets ZF:=(EAX==0) with no "
     "intervening flag writer -> for EAX==0, JE is taken",
     "derived from the TEST/JE semantics + flag-writer census; native JSON "
     "boolean enforced (int 1 rejected: TYPE-3)"),
    ("F-C4-6", "BR-C1.4", "phase_b.null_path.unconditional_exit",
     "PROV-BR14-NULL-UNCONDITIONAL", "QC-BR14-NULL-UNCONDITIONAL", "SF-C4-6",
     "opcode byte 0x74 = conditional Jcc (0xEB would be JMP)",
     "conditionality derived from the physical opcode byte"),
    ("F-C4-7", "BR-C1.4", "phase_b.null_path.call_reached",
     "PROV-BR14-NULL-CALL-REACHED", "QC-BR14-NULL-CALL-REACHED", "SF-C4-7",
     "taken branch transfers to 0x004C47C8 OUTSIDE window B before CALL "
     "0x004C47C1 -> the CALL is not reached on the null path",
     "derived from the decoded JE target vs the window interval; native "
     "JSON boolean enforced"),
]


def write_coverage_csv(path, prov_clean, post_rec):
    """FIELD_CHECK_COVERAGE.csv with the measured clean values, the derived
    expected values (extracted from the clean POST gate results) and the
    single-field control outcome for each representation."""
    # collect actual/derived from the clean POST production gate checks
    clean_checks = {}
    if "clean_final_validation" in post_rec:
        # re-derive from fixed_cases CLEAN (has full checks)
        cl = post_rec["fixed_cases"]["CLEAN"]["production"]["checks"]
        clean_checks = {c["check"]: c for c in cl}
    clq = post_rec["fixed_cases"]["CLEAN"]["qc"]["checks"]
    clean_checks_q = {c["check"]: c for c in clq}
    add = post_rec["additional_cases"]

    def val_at(path):
        cur = prov_clean
        for p in path.split("."):
            cur = cur[p]
        return cur

    rows = []
    for (fid, rel, fpath, pchk, qchk, sf, evid, why) in FIELD_CHECK_COVERAGE:
        is_rel = fpath.startswith("(")
        actual = ("(derived relation)" if is_rel
                 else json.dumps(val_at(fpath)))
        pc = clean_checks.get(pchk, {})
        qc = clean_checks_q.get(qchk, {})
        sf_rec = add.get(sf, {})
        sf_prod = sf_rec.get("production", {})
        sf_qc = sf_rec.get("qc", {})
        sf_out = ("PROD=%s QC=%s" % (sf_prod.get("outcome"),
                                    sf_qc.get("outcome")))
        rows.append({
            "FIELD_ID": fid,
            "RELATION": rel,
            "PERSISTED_FIELD_PATH": fpath,
            "ACTUAL_PERSISTED_VALUE": actual,
            "DERIVED_EXPECTED_VALUE": json.dumps(pc.get("actual",
                                             qc.get("actual"))),
            "EVIDENCE_SOURCE": evid,
            "WHY_NON_CIRCULAR": why,
            "PRODUCTION_CHECK_NAME": pchk,
            "QC_CHECK_NAME": qchk,
            "FAILURE_CASE_DETECTED": "%s (%s)" % (sf, sf_out),
            "GATE_VERDICT_CLEAN_POST": ("PASS" if pc.get("pass") in (True,)
                                        and qc.get("ok") in (True,)
                                        else "FAIL"),
        })
    import csv as _csv
    with open(path, "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


# --------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="BR-C1 artifact-validation "
                                "correction driver")
    ap.add_argument("--source-pkg", required=True)
    ap.add_argument("--package", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--phase", default="all",
                    choices=["pre", "post", "regression", "all"])
    args = ap.parse_args()
    for p in ("source_pkg", "package", "scratch"):
        setattr(args, p, os.path.abspath(getattr(args, p)))

    prov_path = os.path.join(args.source_pkg, "BRIDGE_PROVENANCE.json")
    prov_clean = json.load(open(prov_path))
    prov_sha = sha256_file(prov_path)

    source_inventory_before = {}
    for root, _dirs, files in os.walk(args.source_pkg):
        for f in files:
            fp = os.path.join(root, f)
            source_inventory_before[os.path.relpath(fp, args.source_pkg)] = \
                sha256_file(fp)

    exe = "/mnt/d/Eudoria_Reconstruction/pcg_install/Entropia.exe"
    exe_sha_before = sha256_file(exe)

    results = {"run_id": RUN_ID,
               "driver": os.path.abspath(__file__),
               "source_pkg": args.source_pkg,
               "package": args.package,
               "scratch": args.scratch,
               "clean_provenance_sha256": prov_sha,
               "exe_sha256_before": exe_sha_before,
               "started_utc": __import__("datetime").datetime.now(
                   __import__("datetime").timezone.utc).isoformat()}

    pre_rec = post_rec = reg_rec = None
    if args.phase in ("pre", "all"):
        pre_rec, _p, _q = phase_pre(args, prov_clean, prov_sha)
        with open(os.path.join(args.package, "PRE_ARTIFACT_RESULTS.json"),
                  "w") as fh:
            json.dump(pre_rec, fh, indent=2)
        print("[pre] PRE_REPRODUCTION: %s" % json.dumps(
            pre_rec["pre_reproduction"]))
    if args.phase in ("post", "all"):
        post_rec, _p, _q = phase_post(args, prov_clean, prov_sha)
        with open(os.path.join(args.package, "POST_ARTIFACT_RESULTS.json"),
                  "w") as fh:
            json.dump(post_rec, fh, indent=2)
        n = write_coverage_csv(os.path.join(args.package,
                                           "FIELD_CHECK_COVERAGE.csv"),
                               prov_clean, post_rec)
        print("[post] FIELD_CHECK_COVERAGE rows: %d" % n)
    if args.phase in ("regression", "all"):
        reg_rec = phase_regression(args)
        with open(os.path.join(args.package, "REGRESSION_RESULTS.json"),
                  "w") as fh:
            json.dump(reg_rec, fh, indent=2)
        print("[regression] summary: %s" % json.dumps(
            {k: v for k, v in reg_rec["summary"].items()
             if not k.startswith("m5") and not k.startswith("m7")}))

    exe_sha_after = sha256_file(exe)
    results["exe_sha256_after"] = exe_sha_after
    results["exe_unchanged"] = (exe_sha_before == exe_sha_after)
    source_inventory_after = {}
    for root, _dirs, files in os.walk(args.source_pkg):
        for f in files:
            fp = os.path.join(root, f)
            source_inventory_after[os.path.relpath(fp, args.source_pkg)] = \
                sha256_file(fp)
    results["source_package_unchanged"] = (source_inventory_before
                                           == source_inventory_after)
    results["source_package_file_count"] = len(source_inventory_after)
    results["finished_utc"] = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).isoformat()
    with open(os.path.join(args.package, "DRIVER_RUN_SUMMARY.json"),
              "w") as fh:
        json.dump(results, fh, indent=2)
    print("[done] exe_unchanged=%s source_package_unchanged=%s"
          % (results["exe_unchanged"], results["source_package_unchanged"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
