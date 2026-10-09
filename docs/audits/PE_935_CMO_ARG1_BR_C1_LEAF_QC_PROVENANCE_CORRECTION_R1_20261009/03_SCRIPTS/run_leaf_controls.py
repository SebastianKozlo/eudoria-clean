#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_leaf_controls.py — bounded driver for the correction run
PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009.

Runs under WSL PE-AI (python3 -B). All writes are redirected into this run's
OUTPUT_ROOT: result files into PACKAGE, fixtures/mutated copies into
SCRATCH. The source correction package (the direct predecessor of the two
corrected gates), the original bridge package (whose persisted artifacts the
ordinary gates re-read) and the EXE are READ-ONLY inputs. No historical CLI
main is ever invoked; the gate functions are imported as modules and called
as isolated functions with explicit arguments. The driver never delegates a
verdict between gates; it only records both outcomes. It is not a validator
of the facts itself.

Phases:
  pre — the ACTUAL ordinary gates of the SOURCE CORRECTION PACKAGE (imported
        UNMODIFIED from --predecessor-pkg/03_SCRIPTS) on the four PRE leaf
        cases (PRE-CLEAN, PRE-FLOAT, PRE-DELETE-EXPR, PRE-DELETE-DELTA),
        preregistered as the residual reproduction: FLOAT false-PASS in both
        gates (wrong declared integer type accepted), DELETE -> KeyError in
        both gates (an EXCEPTION is not a successful semantic rejection).
        Raw exceptions are preserved verbatim. PRE is never rewritten.
  post — the corrected copies (PACKAGE/03_SCRIPTS) on: the new LF matrix
        (8 cases x 2 gates = 16 outcomes), the unchanged fixed 7-case matrix
        (14 outcomes) and the unchanged published additional controls
        (43 cases / 86 outcomes) — all case definitions are IMPORTED from the
        preserved run_br_c1_controls.py (byte-identical to the published
        driver), never re-typed; clean final validation through the same
        corrected gates; AST/source comparison of the corrected modules vs
        the source correction package modules (only gate_artifacts()/gate()
        changed + the new QC-local E-slot helpers).
  regression — the UNCHANGED existing 12-case production byte matrix and
        12-case QC byte matrix through the corrected copies' PRESERVED
        helpers (all writes in SCRATCH) + M5/M7 arg1-retention checks +
        unchanged-definition preservation proofs.
"""

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback

RUN_ID = "PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009"
PREDECESSOR_RUN_ID = "PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009"
BRIDGE_RUN_ID = "PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009"

SLOT_LEAF_BASE = "phase_a.source_slot"


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


def utcnow_iso():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def inventory(root):
    inv = {}
    for r, _dirs, files in os.walk(root):
        for f in files:
            fp = os.path.join(r, f)
            inv[os.path.relpath(fp, root).replace("\\", "/")] = \
                [os.path.getsize(fp), sha256_file(fp)]
    return inv


# ------------------------------------------------------- leaf case builders
#
# The LF/PRE cases touch ONLY the two tested leaves of phase_a.source_slot.
# Every mutated copy is a deep copy of the clean provenance written to
# SCRATCH/prov/ (outside Git) and passed to the gates through their ordinary
# provenance override — exactly like the predecessor artifact controls.

LEAF_EXPR = SLOT_LEAF_BASE + ".slot_expr_from_E"
LEAF_DELTA = SLOT_LEAF_BASE + ".slot_delta_from_E"

LF_CASES = {
    "LF-CLEAN":        ("NONE", None),
    "LF-FLOAT":        ("SET", (LEAF_DELTA, 4.0)),
    "LF-BOOL":         ("SET", (LEAF_DELTA, True)),
    "LF-MISSING-DELTA": ("DEL", LEAF_DELTA),
    "LF-MISSING-EXPR": ("DEL", LEAF_EXPR),
    "LF-NULL-EXPR":    ("SET", (LEAF_EXPR, None)),
    "LF-WRONG-DELTA":  ("SET", (LEAF_DELTA, 5)),
    "LF-WRONG-EXPR":   ("SET", (LEAF_EXPR, "[E+0x8]")),
}

PRE_LEAF_CASES = {
    "PRE-CLEAN":          ("NONE", None),
    "PRE-FLOAT":          ("SET", (LEAF_DELTA, 4.0)),
    "PRE-DELETE-EXPR":   ("DEL", LEAF_EXPR),
    "PRE-DELETE-DELTA":  ("DEL", LEAF_DELTA),
}

# preregistered PRE observations (PREREGISTRATION.md section 3)
PRE_EXPECTED = {
    "PRE-CLEAN": "PASS",
    "PRE-FLOAT": "PASS (false-PASS: wrong declared integer type accepted)",
    "PRE-DELETE-EXPR": "KeyError",
    "PRE-DELETE-DELTA": "KeyError",
}

# required POST in each ordinary gate (PREREGISTRATION.md section 4):
# (required_verdict, leaf under test, required diagnostic class)
LF_EXPECTED = {
    "LF-CLEAN":         ("PASS", None, None),
    "LF-FLOAT":         ("REJECTED", "delta", "WRONG_TYPE"),
    "LF-BOOL":          ("REJECTED", "delta", "WRONG_TYPE"),
    "LF-MISSING-DELTA": ("REJECTED", "delta", "MISSING_FIELD"),
    "LF-MISSING-EXPR":  ("REJECTED", "expr", "MISSING_FIELD"),
    "LF-NULL-EXPR":     ("REJECTED", "expr", "WRONG_TYPE"),
    "LF-WRONG-DELTA":   ("REJECTED", "delta", "VALUE_MISMATCH"),
    "LF-WRONG-EXPR":    ("REJECTED", "expr", "VALUE_MISMATCH"),
}

# named typed-leaf predicates per gate + the preserved aggregate conjunction
LEAF_PREDICATES = {
    "PRODUCTION": {"expr": "PROV-A-SLOT-EXPR", "delta": "PROV-A-SLOT-DELTA"},
    "QC":         {"expr": "QC-A-SLOT-EXPR", "delta": "QC-A-SLOT-DELTA"},
}
AGGREGATE_PREDICATE = "PROV-A-SLOT"


def build_leaf_case(prov_clean, case, spec, scratch, phase):
    """Deep-copy the clean provenance, apply ONLY the indicated leaf
    mutation, write the copy to SCRATCH and return its path."""
    kind, payload = spec
    if kind == "NONE":
        return None, []
    prov = copy.deepcopy(prov_clean)
    if kind == "SET":
        dotted, value = payload
        cur = prov
        parts = dotted.split(".")
        for p in parts[:-1]:
            cur = cur[p]
        cur[parts[-1]] = value
        notes = ["%s=%r (only this leaf changed)" % (dotted, value)]
    elif kind == "DEL":
        dotted = payload
        cur = prov
        parts = dotted.split(".")
        for p in parts[:-1]:
            cur = cur[p]
        del cur[parts[-1]]
        notes = ["DELETE %s (only this leaf deleted)" % dotted]
    else:
        raise ValueError("unknown leaf case kind " + kind)
    os.makedirs(os.path.join(scratch, "prov"), exist_ok=True)
    path = os.path.join(scratch, "prov", "%s_%s.json" % (phase, case))
    with open(path, "w") as fh:
        json.dump(prov, fh, indent=2)
    return path, notes


# ------------------------------------------------------- gate invocation

def run_gate_raw(mod, gate, pkg, prov_path):
    """Call one ordinary gate as an isolated function with explicit
    arguments; never let an exception escape silently — record it VERBATIM
    (full raw traceback) so PRE residuals are preserved exactly."""
    call = {"function": "gate_artifacts" if gate == "PRODUCTION" else "gate",
            "pkg": pkg,
            "prov_override": prov_path}
    try:
        if gate == "PRODUCTION":
            checks, verdict = mod.gate_artifacts(pkg,
                                                prov_path_override=prov_path)
        else:
            checks, verdict = mod.gate(pkg, prov_override=prov_path)
        failing = [c["check"] for c in checks
                   if not c["pass" if gate == "PRODUCTION" else "ok"]]
        diags = {c["check"]: c.get("diagnostic")
                 for c in checks
                 if not c["pass" if gate == "PRODUCTION" else "ok"]
                 and "diagnostic" in c}
        return {"call": call, "verdict": verdict, "exception": None,
                "exception_type": None, "exception_repr": None,
                "traceback": None,
                "all_checks_count": len(checks),
                "pass_count": sum(1 for c in checks
                                  if c["pass" if gate == "PRODUCTION"
                                       else "ok"]),
                "failing_checks": failing,
                "hash_side_failures": [c for c in failing
                                       if c.startswith(("WID-", "EFL-",
                                                        "CSL-"))],
                "brc1_diagnostics": diags,
                "checks": checks}
    except Exception as exc:
        return {"call": call, "verdict": "EXCEPTION",
                "exception": traceback.format_exc(),
                "exception_type": type(exc).__name__,
                "exception_repr": repr(exc),
                "traceback": traceback.format_exc(),
                "all_checks_count": None,
                "pass_count": None,
                "failing_checks": None,
                "hash_side_failures": None,
                "brc1_diagnostics": None,
                "checks": None}


def leaf_diagnostic(rec, predicate, ok_key):
    for c in rec["checks"] or []:
        if c.get("check") == predicate and not c[ok_key]:
            return c.get("diagnostic")
    return None


def evaluate_lf_case(case, gate, rec):
    """Classify one LF outcome against the preregistered requirement:
    correct verdict, the correct named typed-leaf predicate, the correct
    named diagnostic on the exact tested leaf, no uncaught exception, no
    hash/manifest-side failure, and NO failing check outside the slot path
    (no unrelated failure, not even as a co-reason)."""
    ok_key = "pass" if gate == "PRODUCTION" else "ok"
    req_verdict, leaf, diag_class = LF_EXPECTED[case]
    pred = LEAF_PREDICATES[gate]
    out = {"gate": gate,
           "required_verdict": req_verdict,
           "required_leaf": leaf,
           "required_diagnostic_class": diag_class,
           "exception": rec["exception"] is not None,
           "verdict": rec["verdict"],
           "all_checks_count": rec["all_checks_count"],
           "pass_count": rec["pass_count"],
           "failing_checks": rec["failing_checks"],
           "hash_side_failures": rec["hash_side_failures"]}
    if req_verdict == "PASS":
        ok = (rec["verdict"] == "PASS"
              and rec["exception"] is None
              and rec["pass_count"] == rec["all_checks_count"])
        out["outcome"] = "CLEAN_PASS_OK" if ok else "CLEAN_FAIL_UNEXPECTED"
        out["ok"] = ok
        return ok, out
    leaf_name = LEAF_EXPR if leaf == "expr" else LEAF_DELTA
    leaf_pred = pred["expr"] if leaf == "expr" else pred["delta"]
    out["required_leaf_predicate"] = leaf_pred
    diag = leaf_diagnostic(rec, leaf_pred, ok_key)
    out["leaf_diagnostic"] = diag
    allowed = {leaf_pred, AGGREGATE_PREDICATE}
    out["unrelated_failing_checks"] = ([c for c in rec["failing_checks"]
                                       if c not in allowed] if
                                      rec["failing_checks"] else None)
    # the diagnostic must name the exact tested leaf path in the helpers'
    # documented format: "MISSING_FIELD:<dotted>" exactly (the helpers emit
    # no detail suffix for a missing field), or "<class>:<dotted>:<detail>"
    # for the other classes.
    if diag_class == "MISSING_FIELD":
        diag_ok = (diag is not None
                   and diag == "MISSING_FIELD:" + leaf_name)
    else:
        diag_ok = (diag is not None
                   and diag.startswith(diag_class + ":" + leaf_name + ":"))
    out["leaf_diagnostic_ok"] = diag_ok
    ok = (rec["verdict"] == "REJECTED"
          and rec["exception"] is None
          and rec["failing_checks"] is not None
          and leaf_pred in rec["failing_checks"]
          and not rec["hash_side_failures"]
          and set(rec["failing_checks"]) <= allowed
          and diag_ok)
    out["outcome"] = ("REJECTION_OK" if ok else
                      ("REJECTED_UNEXPECTED_DETAIL" if ok is False and
                       rec["verdict"] == "REJECTED" else
                       "NOT_REJECTED_AS_REQUIRED"))
    out["ok"] = ok
    return ok, out


# ------------------------------------------------------- phases

def phase_pre(args, rbc, prov_clean, prov_sha):
    print("[pre] ACTUAL source-correction-package gates (unmodified) ...")
    prod = load_module(os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_pre_leaf")
    qc = load_module(os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_pre_leaf")
    qc_wd = os.path.join(args.scratch, "qc_work", "pre")
    os.makedirs(qc_wd, exist_ok=True)
    qc.WORK = qc_wd
    rec = {
        "phase": "PRE",
        "run_id": RUN_ID,
        "description": "the ACTUAL unmodified ordinary gates of the source "
                       "correction package (BASE a7b1dc0) on the four "
                       "preregistered PRE leaf cases; deep-copied JSON "
                       "loaded through their ordinary provenance override; "
                       "all temporary writes redirected to SCRATCH; no "
                       "historical CLI main invoked",
        "predecessor_pkg": args.predecessor_pkg,
        "evidence_pkg": args.evidence_pkg,
        "predecessor_module_sha256": {
            "run_frame_bridge.py": sha256_file(
                os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                             "run_frame_bridge.py")),
            "qc_frame_bridge.py": sha256_file(
                os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                             "qc_frame_bridge.py"))},
        "clean_provenance_sha256": prov_sha,
        "preregistered_expectations": PRE_EXPECTED,
        "exe_sha256": sha256_file(prod.EXE_PATH),
        "started_utc": utcnow_iso(),
        "cases": {},
    }
    for case, spec in PRE_LEAF_CASES.items():
        prov_path, notes = build_leaf_case(prov_clean, case, spec,
                                           args.scratch, "pre")
        c = {"mutation": notes,
             "prov_copy": (sha256_file(prov_path) if prov_path
                           else "EVIDENCE_PACKAGE_ORIGINAL"),
             "preregistered_expectation": PRE_EXPECTED[case]}
        pr = run_gate_raw(prod, "PRODUCTION", args.evidence_pkg, prov_path)
        qr = run_gate_raw(qc, "QC", args.evidence_pkg, prov_path)
        for gate, r in (("production", pr), ("qc", qr)):
            observed = r["verdict"]
            if r["verdict"] == "EXCEPTION":
                observed = "%s (%s)" % (r["exception_type"],
                                        r["exception_repr"])
            r["observed"] = observed
            exp = PRE_EXPECTED[case]
            if exp.startswith("PASS"):
                r["matches_preregistration"] = (r["verdict"] == "PASS")
            else:
                r["matches_preregistration"] = (r["verdict"] == "EXCEPTION"
                                                and r["exception_type"]
                                                == exp)
        c["production"] = pr
        c["qc"] = qr
        rec["cases"][case] = c
        print("  %-18s PROD=%s QC=%s" % (case, pr["verdict"], qr["verdict"]))
    cases = rec["cases"]
    rec["pre_residual_reproduction"] = {
        "clean_pass_both_gates":
            cases["PRE-CLEAN"]["production"]["verdict"] == "PASS"
            and cases["PRE-CLEAN"]["qc"]["verdict"] == "PASS",
        "float_false_pass_both_gates":
            cases["PRE-FLOAT"]["production"]["verdict"] == "PASS"
            and cases["PRE-FLOAT"]["qc"]["verdict"] == "PASS",
        "delete_expr_exception_both_gates":
            cases["PRE-DELETE-EXPR"]["production"]["verdict"] == "EXCEPTION"
            and cases["PRE-DELETE-EXPR"]["qc"]["verdict"] == "EXCEPTION",
        "delete_expr_exception_type":
            [cases["PRE-DELETE-EXPR"]["production"]["exception_type"],
             cases["PRE-DELETE-EXPR"]["qc"]["exception_type"]],
        "delete_delta_exception_both_gates":
            cases["PRE-DELETE-DELTA"]["production"]["verdict"] == "EXCEPTION"
            and cases["PRE-DELETE-DELTA"]["qc"]["verdict"] == "EXCEPTION",
        "delete_delta_exception_type":
            [cases["PRE-DELETE-DELTA"]["production"]["exception_type"],
             cases["PRE-DELETE-DELTA"]["qc"]["exception_type"]],
    }
    rr = rec["pre_residual_reproduction"]
    rec["pre_residual_reproduction"]["residual_reproduced"] = bool(
        rr["clean_pass_both_gates"]
        and rr["float_false_pass_both_gates"]
        and rr["delete_expr_exception_both_gates"]
        and rr["delete_delta_exception_both_gates"])
    rec["exe_sha256_after"] = sha256_file(prod.EXE_PATH)
    rec["exe_unchanged"] = rec["exe_sha256"] == rec["exe_sha256_after"]
    rec["finished_utc"] = utcnow_iso()
    print("[pre] residual_reproduced=%s"
          % rec["pre_residual_reproduction"]["residual_reproduced"])
    return rec


def ast_top_level(path):
    """Map of top-level function name -> ast.dump, plus top-level assignment
    line -> ast.dump (module constants), for the mechanical
    only-the-gate-changed proof."""
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    fns = {}
    assigns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            fns[node.name] = ast.dump(node)
        elif isinstance(node, ast.Assign):
            tgts = ",".join(getattr(t, "id", getattr(t, "attr", "?"))
                            for t in node.targets)
            assigns[tgts] = ast.dump(node)
    return fns, assigns


def ast_comparison(args):
    """Corrected copies vs the source correction package: the ONLY changed
    existing function may be gate_artifacts (production) / gate (QC); the QC
    file may ADD the qc-local E-slot helpers; all top-level constants must be
    AST-identical."""
    out = {}
    for fname, gate_name, allowed_changed, allowed_added in (
            ("run_frame_bridge.py", "gate_artifacts", ["gate_artifacts"], []),
            ("qc_frame_bridge.py", "gate", ["gate"],
             sorted(["qc_eslot_expr", "qc_check_eslot_expr"]))):
        corr = os.path.join(args.package, "03_SCRIPTS", fname)
        pred = os.path.join(args.predecessor_pkg, "03_SCRIPTS", fname)
        fns_c, asg_c = ast_top_level(corr)
        fns_p, asg_p = ast_top_level(pred)
        changed = sorted(n for n in fns_c
                         if n in fns_p and fns_c[n] != fns_p[n])
        added = sorted(n for n in fns_c if n not in fns_p)
        removed = sorted(n for n in fns_p if n not in fns_c)
        asg_changed = sorted(k for k in asg_c
                            if k in asg_p and asg_c[k] != asg_p[k])
        asg_added = sorted(k for k in asg_c if k not in asg_p)
        asg_removed = sorted(k for k in asg_p if k not in asg_c)
        out[fname] = {
            "changed_functions": changed,
            "added_functions": added,
            "removed_functions": removed,
            "changed_top_level_assignments": asg_changed,
            "added_top_level_assignments": asg_added,
            "removed_top_level_assignments": asg_removed,
            "as_expected": (changed == allowed_changed
                            and added == allowed_added
                            and removed == []
                            and asg_changed == [] and asg_added == []
                            and asg_removed == []),
        }
    return out


def phase_post(args, rbc, prov_clean, prov_sha):
    print("[post] corrected gates: LF matrix + fixed + additional ...")
    prod = load_module(os.path.join(args.package, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_post_leaf")
    qc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_post_leaf")
    qc_wd = os.path.join(args.scratch, "qc_work", "post")
    os.makedirs(qc_wd, exist_ok=True)
    qc.WORK = qc_wd
    rec = {
        "phase": "POST",
        "run_id": RUN_ID,
        "description": "corrected copies on the new LF matrix (16 outcomes), "
                       "the unchanged fixed 7-case matrix (14) and the "
                       "unchanged published additional controls (43 cases / "
                       "86 outcomes, definitions imported from the "
                       "preserved run_br_c1_controls.py); clean final "
                       "validation through the SAME corrected gates",
        "evidence_pkg": args.evidence_pkg,
        "predecessor_pkg": args.predecessor_pkg,
        "corrected_module_sha256": {
            "run_frame_bridge.py": sha256_file(
                os.path.join(args.package, "03_SCRIPTS",
                             "run_frame_bridge.py")),
            "qc_frame_bridge.py": sha256_file(
                os.path.join(args.package, "03_SCRIPTS",
                             "qc_frame_bridge.py"))},
        "preserved_driver_module_sha256": sha256_file(
            os.path.join(args.package, "03_SCRIPTS",
                          "run_br_c1_controls.py")),
        "clean_provenance_sha256": prov_sha,
        "exe_sha256": sha256_file(prod.EXE_PATH),
        "started_utc": utcnow_iso(),
        "lf_cases": {},
    }
    # --- LF matrix -----------------------------------------------------
    lf_ok = 0
    lf_total = 0
    for case, spec in LF_CASES.items():
        prov_path, notes = build_leaf_case(prov_clean, case, spec,
                                           args.scratch, "post")
        c = {"mutation": notes,
             "prov_copy": (sha256_file(prov_path) if prov_path
                           else "EVIDENCE_PACKAGE_ORIGINAL")}
        pr = run_gate_raw(prod, "PRODUCTION", args.evidence_pkg, prov_path)
        qr = run_gate_raw(qc, "QC", args.evidence_pkg, prov_path)
        okp, ep = evaluate_lf_case(case, "PRODUCTION", pr)
        okq, eq = evaluate_lf_case(case, "QC", qr)
        c["production"] = ep
        c["qc"] = eq
        rec["lf_cases"][case] = c
        lf_total += 2
        lf_ok += int(okp) + int(okq)
        print("  %-16s PROD=%s(%s) QC=%s(%s)"
              % (case, pr["verdict"], ep["outcome"], qr["verdict"],
                 eq["outcome"]))
    rec["lf_matrix"] = {"cases": len(LF_CASES), "outcomes": lf_total,
                        "correct_outcomes": lf_ok}
    # --- fixed matrix (unchanged definitions from the preserved driver) --
    fixed_ok = 0
    fixed_total = 0
    rec["fixed_cases"] = {}
    for case in ["CLEAN", "AC1", "AC2", "BR1", "BR2", "BR3", "BR4"]:
        prov_path, notes = rbc.build_case(prov_clean, case, args.scratch,
                                          "post")
        c = {"mutation_fields": notes,
             "prov_copy": (sha256_file(prov_path) if prov_path
                           else "EVIDENCE_PACKAGE_ORIGINAL")}
        pr = rbc.run_prod_gate(prod, args.evidence_pkg, prov_path)
        qr = rbc.run_qc_gate(qc, args.evidence_pkg, prov_path)
        okp = rbc.evaluate_case(case, "PRODUCTION", pr, expect_reject=True)
        okq = rbc.evaluate_case(case, "QC", qr, expect_reject=True)
        c["production"] = {k: pr[k] for k in
                           ("call", "verdict", "exception",
                            "all_checks_count", "pass_count",
                            "failing_checks", "hash_side_failures",
                            "brc1_diagnostics", "outcome")}
        c["qc"] = {k: qr[k] for k in
                   ("call", "verdict", "exception", "all_checks_count",
                    "pass_count", "failing_checks", "hash_side_failures",
                    "brc1_diagnostics", "outcome")}
        c["production"]["expected_failing_predicates"] = \
            pr["expected_failing_predicates"]
        c["qc"]["expected_failing_predicates"] = \
            qr["expected_failing_predicates"]
        rec["fixed_cases"][case] = c
        fixed_total += 2
        fixed_ok += int(okp) + int(okq)
        print("  %-5s PROD=%s(%s) QC=%s(%s)"
              % (case, pr["verdict"], pr["outcome"], qr["verdict"],
                 qr["outcome"]))
    rec["fixed_matrix"] = {"expected_outcomes": fixed_total,
                           "correct_outcomes": fixed_ok}
    # --- additional controls (unchanged definitions) --------------------
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
    rec["additional_cases"] = {}
    for case in add_cases:
        prov_path, notes = rbc.build_case(prov_clean, case, args.scratch,
                                           "post")
        c = {"mutation_fields": notes,
             "prov_copy": sha256_file(prov_path)}
        pr = rbc.run_prod_gate(prod, args.evidence_pkg, prov_path)
        qr = rbc.run_qc_gate(qc, args.evidence_pkg, prov_path)
        okp = rbc.evaluate_case(case, "PRODUCTION", pr, expect_reject=True)
        okq = rbc.evaluate_case(case, "QC", qr, expect_reject=True)
        c["production"] = {k: pr[k] for k in
                           ("call", "verdict", "exception",
                            "all_checks_count", "pass_count",
                            "failing_checks", "hash_side_failures",
                            "brc1_diagnostics", "outcome")}
        c["qc"] = {k: qr[k] for k in
                   ("call", "verdict", "exception", "all_checks_count",
                    "pass_count", "failing_checks", "hash_side_failures",
                    "brc1_diagnostics", "outcome")}
        c["production"]["expected_failing_predicates"] = \
            pr["expected_failing_predicates"]
        c["qc"]["expected_failing_predicates"] = \
            qr["expected_failing_predicates"]
        rec["additional_cases"][case] = c
        add_total += 2
        add_ok += int(okp) + int(okq)
        print("  %-8s PROD=%s QC=%s ok=%d"
              % (case, pr["verdict"], qr["verdict"], int(okp) + int(okq)))
    rec["additional_matrix"] = {
        "cases": len(add_cases), "outcomes": add_total,
        "correct_outcomes": add_ok,
        "single_field_cases": 32, "missing_field_cases": 4,
        "wrong_type_cases": 5, "malformed_expr_cases": 2,
        "note": "case definitions imported unchanged from the preserved "
                "run_br_c1_controls.py; SF-C2-8/SF-C2-9 still satisfy the "
                "preserved expected predicate PROV-A-SLOT (the aggregate "
                "conjunction) and now also fail the named typed-leaf "
                "predicates"}
    # --- clean final validation (same gates, no override) ---------------
    pr = run_gate_raw(prod, "PRODUCTION", args.evidence_pkg, None)
    qr = run_gate_raw(qc, "QC", args.evidence_pkg, None)
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
    # --- AST/source comparison (mechanical only-the-gate-changed proof) --
    rec["ast_comparison"] = ast_comparison(args)
    print("[post] ast_comparison as_expected=%s"
          % all(v["as_expected"] for v in rec["ast_comparison"].values()))
    rec["exe_sha256_after"] = sha256_file(prod.EXE_PATH)
    rec["exe_unchanged"] = rec["exe_sha256"] == rec["exe_sha256_after"]
    rec["finished_utc"] = utcnow_iso()
    return rec


def phase_regression(args, rbc, prov_clean, prov_sha):
    print("[regression] 12-case production + 12-case QC byte matrix ...")
    prod = load_module(os.path.join(args.package, "03_SCRIPTS",
                                    "run_frame_bridge.py"), "prod_reg_leaf")
    qc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                  "qc_frame_bridge.py"), "qc_reg_leaf")
    prod_pre = load_module(os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                                        "run_frame_bridge.py"),
                           "prod_reg_leaf_pre")
    qc_pre = load_module(os.path.join(args.predecessor_pkg, "03_SCRIPTS",
                                      "qc_frame_bridge.py"),
                         "qc_reg_leaf_pre")
    preserved = {
        "production_EXPECTED_identical": prod.EXPECTED == prod_pre.EXPECTED,
        "production_MUTATIONS_identical": prod.MUTATIONS == prod_pre.MUTATIONS,
        "production_CASE_ORDER_identical":
            prod.CASE_ORDER == prod_pre.CASE_ORDER,
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
        "run_id": RUN_ID,
        "description": "re-execution of the UNCHANGED existing 12-case "
                       "production byte matrix (run_case/EXPECTED/MUTATIONS) "
                       "and 12-case QC byte matrix (run_matrix/EXP/MUT) "
                       "through the corrected copies' PRESERVED helpers; "
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
        "started_utc": utcnow_iso(),
        "finished_utc": utcnow_iso(),
    }
    return rec


# ------------------------------------------------------- coverage CSV
#
# Same 34-row table as the published driver (imported unchanged), with the
# two source_slot leaf rows now pointing at the named typed-leaf predicates
# of the corrected gates (the aggregate PROV-A-SLOT remains as the
# conjunction; rows F-C2-8/F-C2-9 reference the leaf checks). The delta row's
# DERIVED_EXPECTED_VALUE is the leaf check's derived value (4), fixing the
# predecessor's display-only artifact recorded as F-QC-2 there.

LEAF_CHECK_NAME_OVERRIDES = {
    "F-C2-8": ("PROV-A-SLOT-EXPR", "QC-A-SLOT-EXPR"),
    "F-C2-9": ("PROV-A-SLOT-DELTA", "QC-A-SLOT-DELTA"),
}


def write_coverage_csv(path, rbc, prov_clean, post_rec):
    """34-row FIELD_CHECK_COVERAGE.csv: the unchanged published table
    (imported from the preserved driver) with the two source_slot leaf rows
    re-pointed at the named typed-leaf predicates of the corrected gates.
    DERIVED_EXPECTED_VALUE comes from the clean final validation's own
    check records (production 'actual' column); the delta row therefore
    shows the derived delta 4 (fixing the predecessor's display-only
    artifact recorded there as F-QC-2)."""
    coverage = rbc.FIELD_CHECK_COVERAGE
    add = post_rec["additional_cases"]
    clean_full = post_rec["clean_final_validation_checks"]
    prod_clean_map = {c["check"]: c for c in clean_full["production"]}
    qc_clean_map = {c["check"]: c for c in clean_full["qc"]}

    def val_at(p):
        cur = prov_clean
        for part in p.split("."):
            cur = cur[part]
        return cur

    rows = []
    for (fid, rel, fpath, pchk, qchk, sf, evid, why) in coverage:
        is_rel = fpath.startswith("(")
        actual = ("(derived relation)" if is_rel
                  else json.dumps(val_at(fpath)))
        if fid in LEAF_CHECK_NAME_OVERRIDES:
            pchk, qchk = LEAF_CHECK_NAME_OVERRIDES[fid]
        pc = prod_clean_map.get(pchk, {})
        qc = qc_clean_map.get(qchk, {})
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
    ap = argparse.ArgumentParser(description="BR-C1 leaf-field + QC "
                                "provenance correction driver")
    ap.add_argument("--evidence-pkg", required=True,
                    help="original bridge package (read-only artifacts the "
                         "ordinary gates re-read)")
    ap.add_argument("--predecessor-pkg", required=True,
                    help="source correction package (PRE gates; AST "
                         "comparison and preservation baseline)")
    ap.add_argument("--package", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--phase", default="all",
                    choices=["pre", "post", "regression", "all"])
    args = ap.parse_args()
    for p in ("evidence_pkg", "predecessor_pkg", "package", "scratch"):
        setattr(args, p, os.path.abspath(getattr(args, p)))

    # the preserved published driver (byte-identical copy) supplies the
    # unchanged fixed/additional case definitions
    rbc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                   "run_br_c1_controls.py"),
                      "rbc_preserved")

    prov_path = os.path.join(args.evidence_pkg, "BRIDGE_PROVENANCE.json")
    prov_clean = json.load(open(prov_path))
    prov_sha = sha256_file(prov_path)

    inv_before = {
        "evidence_pkg": inventory(args.evidence_pkg),
        "predecessor_pkg": inventory(args.predecessor_pkg),
    }

    if args.phase in ("pre", "all"):
        pre_rec = phase_pre(args, rbc, prov_clean, prov_sha)
        with open(os.path.join(args.package, "PRE_LEAF_RESULTS.json"),
                  "w") as fh:
            json.dump(pre_rec, fh, indent=2)
        print("[pre] written PRE_LEAF_RESULTS.json")
    if args.phase in ("post", "all"):
        post_rec = phase_post(args, rbc, prov_clean, prov_sha)
        # record the full clean check lists for the coverage CSV (the
        # clean final validation through the same corrected gates)
        prod = load_module(os.path.join(args.package, "03_SCRIPTS",
                                        "run_frame_bridge.py"),
                           "prod_cfv")
        qc = load_module(os.path.join(args.package, "03_SCRIPTS",
                                      "qc_frame_bridge.py"), "qc_cfv")
        qc_wd = os.path.join(args.scratch, "qc_work", "cfv")
        os.makedirs(qc_wd, exist_ok=True)
        qc.WORK = qc_wd
        pr = run_gate_raw(prod, "PRODUCTION", args.evidence_pkg, None)
        qr = run_gate_raw(qc, "QC", args.evidence_pkg, None)
        post_rec["clean_final_validation_checks"] = {
            "production": pr["checks"], "qc": qr["checks"]}
        with open(os.path.join(args.package, "POST_LEAF_RESULTS.json"),
                  "w") as fh:
            json.dump(post_rec, fh, indent=2)
        n = write_coverage_csv(os.path.join(args.package,
                                           "FIELD_CHECK_COVERAGE.csv"),
                               rbc, prov_clean, post_rec)
        print("[post] written POST_LEAF_RESULTS.json; FIELD_CHECK_COVERAGE "
              "rows: %d" % n)
    if args.phase in ("regression", "all"):
        reg_rec = phase_regression(args, rbc, prov_clean, prov_sha)
        with open(os.path.join(args.package, "REGRESSION_RESULTS.json"),
                  "w") as fh:
            json.dump(reg_rec, fh, indent=2)
        print("[regression] written REGRESSION_RESULTS.json")

    inv_after = {
        "evidence_pkg": inventory(args.evidence_pkg),
        "predecessor_pkg": inventory(args.predecessor_pkg),
    }
    print("[done] evidence_pkg_unchanged=%s predecessor_pkg_unchanged=%s"
          % (inv_before["evidence_pkg"] == inv_after["evidence_pkg"],
             inv_before["predecessor_pkg"] == inv_after["predecessor_pkg"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
