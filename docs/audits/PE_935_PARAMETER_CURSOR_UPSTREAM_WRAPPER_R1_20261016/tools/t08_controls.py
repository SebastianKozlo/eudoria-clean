# t08_controls.py — bounded claims qualifier + the four contract controls (C1-C4).
# Controls operate on COPIES of the claims record (machine_checkable_claims from
# EVIDENCE.json), checked against the saved INSTRUCTION_ROSTER.json. No original
# buffers are modified; no synthetic x86 decode; no universal semantic verifier —
# only the four bounded predicates required by the contract.
# Each case (BASE + C1..C4) is executed as a SEPARATE child process whose real
# exit code is captured (required refusals: proper reason + nonzero exit).
import sys, os, copy, json, subprocess, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t08_controls.py"

NEUTRAL_VALUES = {"UNKNOWN", "NOT_ESTABLISHED", "NO", "NONE", "NOT_PERFORMED", "PENDING",
                  "PARTIAL", "NOT_ESTABLISHED_UNLESS_DIRECTLY_EVIDENCED_IN_SCOPE",
                  "UNVERIFIED_EXCEPT_SCOPED_WIDTH_AND_ADDRESS_FACTS",
                  "NOT_APPLICABLE_PRIVATE_RUN_NO_GIT_WRITE"}

ROLE_CLASS_FACT_RULES = {
    "function_argument_slot": {"allowed_fact_keys": ["mov_dst", "mov_dst8"]},
    "stack_argument_value_at_transfer": {"allowed_fact_keys": ["push_register"]},
    "thiscall_receiver_at_transfer": {"allowed_fact_keys": ["mov_dst"], "must_value": "ECX"},
    "entry_ecx_receiver_save": {"allowed_fact_keys": ["mov_dst"], "must_fact": ("mov_src", "ECX")},
}

def qualify(claims, roster_rows):
    # returns (verdict, reason, details)
    reasons = []
    head_map = {}
    for r in roster_rows:
        head_map[int(r["va"], 16)] = r
    # 1) structure
    for k in ("transfer_site", "head_anchors", "role_bindings", "opaque_preservations", "source_and_world"):
        if k not in claims:
            return ("REFUSED", "STRUCTURE_ERROR", {"missing_key": k})
    # 2) transfer site
    ts = claims["transfer_site"]
    tsv = int(ts["va"], 16)
    if tsv not in head_map:
        return ("REFUSED", "NOT_INSTRUCTION_HEAD",
                {"detail": "transfer_site va is not an instruction head in the roster", "va": ts["va"]})
    row = head_map[tsv]
    if row["raw_hex"].replace(" ", "").lower() != ts["raw_hex"].replace(" ", "").lower():
        return ("REFUSED", "RAW_MISMATCH", {"detail": "transfer_site raw does not match the roster row", "va": ts["va"]})
    if row["kind"] != ts["declared_transfer_kind"]:
        return ("REFUSED", "TRANSFER_FORM_MISMATCH",
                {"detail": "declared transfer kind differs from the roster row kind",
                 "declared": ts["declared_transfer_kind"], "roster": row["kind"]})
    rt = row["target"]["value"] if row.get("target") else None
    dt = ts.get("declared_target")
    if (rt or None) != (dt or None):
        return ("REFUSED", "TRANSFER_FORM_MISMATCH",
                {"detail": "declared target differs from the roster-recomputed target",
                 "declared": dt, "roster": rt})
    # 3) head anchors
    for h in claims["head_anchors"]:
        hv = int(h["va"], 16)
        if hv not in head_map:
            return ("REFUSED", "NOT_INSTRUCTION_HEAD",
                    {"detail": "head anchor va is not an instruction head", "va": h["va"]})
        if head_map[hv]["raw_hex"].replace(" ", "").lower() != h["raw_hex"].replace(" ", "").lower():
            return ("REFUSED", "RAW_MISMATCH", {"detail": "head anchor raw mismatch", "va": h["va"]})
    # 4) role bindings
    for b in claims["role_bindings"]:
        cv = int(b["carrier"]["va"], 16)
        if cv not in head_map:
            return ("REFUSED", "NOT_INSTRUCTION_HEAD",
                    {"detail": "role binding carrier va is not an instruction head", "symbol": b.get("symbol")})
        facts = head_map[cv].get("encoding_facts") or {}
        fk = b["carrier"]["fact_key"]
        ev = b["carrier"]["expected_value"]
        if facts.get(fk) != ev:
            return ("REFUSED", "ROLE_OR_SLOT_MISMATCH",
                    {"detail": "carrier fact does not equal the claimed slot/register",
                     "symbol": b.get("symbol"), "fact_key": fk,
                     "claims_expected": ev, "roster_fact": facts.get(fk)})
        rule = ROLE_CLASS_FACT_RULES.get(b["role_class"])
        if rule is None:
            return ("REFUSED", "ROLE_OR_SLOT_MISMATCH",
                    {"detail": "unknown role class", "role_class": b["role_class"]})
        if fk not in rule["allowed_fact_keys"]:
            return ("REFUSED", "ROLE_OR_SLOT_MISMATCH",
                    {"detail": "role class inconsistent with the carrier fact kind",
                     "role_class": b["role_class"], "fact_key": fk})
        if "must_value" in rule and ev != rule["must_value"]:
            return ("REFUSED", "ROLE_OR_SLOT_MISMATCH",
                    {"detail": "role class requires a different register value",
                     "role_class": b["role_class"], "expected_value": ev})
        if "must_fact" in rule:
            mk, mv = rule["must_fact"]
            if facts.get(mk) != mv:
                return ("REFUSED", "ROLE_OR_SLOT_MISMATCH",
                        {"detail": "role class requires an additional fact that does not hold",
                         "role_class": b["role_class"], "needed": {mk: mv}, "actual": facts.get(mk)})
    # 5) opaque preservations
    proofs = claims.get("byte_proofs") or {}
    for p in claims["opaque_preservations"]:
        if p.get("crosses_opaque_call"):
            st = p.get("status")
            if st == "CONFIRMED":
                pk = p.get("proof_key")
                if pk is None or pk not in proofs:
                    return ("REFUSED", "UNJUSTIFIED_OPAQUE_PRESERVATION",
                            {"detail": "unconditional CONFIRMED preservation across an opaque CALL without proof or ABI model",
                             "claim": p.get("claim")})
            elif st == "CONDITIONAL_ON_ABI_MODEL":
                if "ABI_MODEL" not in (p.get("requires") or []):
                    return ("REFUSED", "UNJUSTIFIED_OPAQUE_PRESERVATION",
                            {"detail": "CONDITIONAL_ON_ABI_MODEL without the ABI_MODEL requirement",
                             "claim": p.get("claim")})
            elif st != "NOT_ESTABLISHED":
                return ("REFUSED", "UNJUSTIFIED_OPAQUE_PRESERVATION",
                        {"detail": "unsupported preservation status across an opaque CALL",
                         "claim": p.get("claim"), "status": st})
    # 6) source and world
    for s in claims["source_and_world"]:
        if s["value"] not in NEUTRAL_VALUES and not s.get("evidence"):
            return ("REFUSED", "UNSUPPORTED_SOURCE_OR_WORLD_PROMOTION",
                    {"detail": "source/world value promoted without evidence",
                     "key": s["key"], "value": s["value"]})
    return ("ACCEPTED", None, {"checked": "transfer_site+anchors+roles+preservations+source/world"})

def child_main(argv):
    a = rc.parse_simple_args(argv, ["--config", "--child", "--case", "--claims"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    with open(rc.resolve_in_root(root, "decode/INSTRUCTION_ROSTER.json"), "r", encoding="utf-8") as f:
        roster = rc.strict_loads(f.read())
    with open(a["--claims"], "r", encoding="utf-8") as f:
        claims = rc.strict_loads(f.read())
    verdict, reason, details = qualify(claims, roster["instructions"])
    exit_code = 0 if verdict == "ACCEPTED" else 1
    out = rc.compact_dumps({"case": a["--case"], "verdict": verdict, "reason": reason,
                            "exit_code": exit_code, "details": details})
    print(out)
    return exit_code

def mutate(claims, case):
    m = copy.deepcopy(claims)
    if case == "C1":
        tsv = int(m["transfer_site"]["va"], 16)
        m["transfer_site"]["va"] = "0x%08X" % (tsv + 1)
        return m, "transfer_site moved to the interior byte (VA+1) of the actual transfer instruction"
    if case == "C2":
        idx = {}
        for i, b in enumerate(m["role_bindings"]):
            if b["symbol"] in ("C_at_parser", "O_at_parser"):
                idx[b["symbol"]] = i
        if "C_at_parser" not in idx or "O_at_parser" not in idx:
            raise RuntimeError("C2 mutation needs C_at_parser and O_at_parser bindings")
        i, j = idx["C_at_parser"], idx["O_at_parser"]
        m["role_bindings"][i]["carrier"], m["role_bindings"][j]["carrier"] = \
            m["role_bindings"][j]["carrier"], m["role_bindings"][i]["carrier"]
        return m, "C and O/receiver carriers (slots/registers) swapped against the established operands"
    if case == "C3":
        if not m["opaque_preservations"]:
            raise RuntimeError("C3 mutation needs an opaque_preservations entry")
        m["opaque_preservations"][0]["status"] = "CONFIRMED"
        m["opaque_preservations"][0]["requires"] = []
        m["opaque_preservations"][0]["proof_key"] = None
        return m, "preservation across the opaque helper CALL promoted to unconditional CONFIRMED without proof and without the ABI model"
    if case == "C4":
        hit = 0
        for s in m["source_and_world"]:
            if s["key"] == "CURSOR_SOURCE_MEDIUM":
                s["value"] = "FILE"; s["evidence"] = None; hit += 1
            if s["key"] == "WORLD_XYZ_RECOVERED":
                s["value"] = "YES"; s["evidence"] = None; hit += 1
        if hit < 2:
            raise RuntimeError("C4 mutation needs CURSOR_SOURCE_MEDIUM and WORLD_XYZ_RECOVERED entries")
        return m, "FILE promoted as established cursor source medium and XYZ as recovered, without separate proof"
    raise RuntimeError("unknown case %r" % case)

def main():
    argv = list(sys.argv)
    if "--child" in argv:
        return child_main(argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    tool_abs = os.path.abspath(__file__)
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    expected = {"C1": "NOT_INSTRUCTION_HEAD", "C2": "ROLE_OR_SLOT_MISMATCH",
                "C3": "UNJUSTIFIED_OPAQUE_PRESERVATION",
                "C4": "UNSUPPORTED_SOURCE_OR_WORLD_PROMOTION"}
    try:
        rc.new_attempt_dir(root, attempt_id)
        ev_abs = rc.resolve_in_root(root, "EVIDENCE.json")
        with open(ev_abs, "r", encoding="utf-8") as f:
            ev = rc.strict_loads(f.read())
        inputs_meta.append(rc.file_identity(ev_abs, "EVIDENCE.json"))
        claims = copy.deepcopy(ev["machine_checkable_claims"])
        cases = {}
        # BASE copy
        base_file = {"case": "BASE", "mutation_description": None, "claims": claims}
        o = rc.atomic_write_bytes(root, "controls/BASE_CASE.json", rc.strict_dumps(base_file).encode("utf-8"))
        outputs_meta.append(o)
        cases["BASE"] = "controls/BASE_CASE.json"
        for c in ("C1", "C2", "C3", "C4"):
            mut, desc = mutate(claims, c)
            mf = {"case": c, "mutation_description": desc, "claims": mut}
            o = rc.atomic_write_bytes(root, "controls/%s_MUTANT.json" % c, rc.strict_dumps(mf).encode("utf-8"))
            outputs_meta.append(o)
            cases[c] = "controls/%s_MUTANT.json" % c
        # run each case as a real child process; capture real exit codes
        outcomes = {}
        for c in ("BASE", "C1", "C2", "C3", "C4"):
            claims_abs = rc.resolve_in_root(root, cases[c])
            child_argv = [sys.executable, "-B", tool_abs, "--config", cfg["_config_abs"],
                          "--child", "--case", c, "--claims", claims_abs]
            pr = subprocess.run(child_argv, capture_output=True)
            stdout_text = pr.stdout.decode("utf-8", "replace")
            stderr_text = pr.stderr.decode("utf-8", "replace")
            try:
                parsed = rc.strict_loads(stdout_text.strip().splitlines()[-1]) if stdout_text.strip() else {}
            except BaseException:
                parsed = {}
            outcomes[c] = {"claims_file": cases[c], "argv": child_argv,
                           "exit_code": pr.returncode,
                           "verdict": parsed.get("verdict"), "reason": parsed.get("reason"),
                           "details": parsed.get("details"),
                           "child_stdout": stdout_text, "child_stderr": stderr_text}
        base_ok = (outcomes["BASE"]["exit_code"] == 0 and outcomes["BASE"]["verdict"] == "ACCEPTED")
        mutant_results = {}
        all_pass = base_ok
        for c in ("C1", "C2", "C3", "C4"):
            oc = outcomes[c]
            refused = (oc["exit_code"] != 0 and oc["verdict"] == "REFUSED" and oc["reason"] == expected[c])
            mutant_results[c] = {"outcome": "REFUSED" if refused else "UNEXPECTED",
                                 "reason": oc["reason"], "expected_reason": expected[c],
                                 "exit_code": oc["exit_code"], "control_pass": refused}
            all_pass = all_pass and refused
        for c in ("BASE", "C1", "C2", "C3", "C4"):
            o = rc.atomic_write_bytes(root, "controls/%s_RESULT.json" % c,
                                      rc.strict_dumps({"case": c, "result": outcomes[c]}).encode("utf-8"))
            outputs_meta.append(o)
        summary = {"control_cases": 4, "case_names": ["C1", "C2", "C3", "C4"],
                   "base_outcome": "ACCEPTED" if base_ok else "NOT_ACCEPTED",
                   "base_exit_code": outcomes["BASE"]["exit_code"],
                   "mutant_outcomes": mutant_results,
                   "qualifier_executions": 5, "procedural_attempts": 5, "retries": 0,
                   "all_control_pass": all_pass,
                   "semantics": "CONTROL_PASS = the required refusal for that specific counter-trial on a COPY of the claims record; not a falsification proof of the real hypothesis; not a universal validator"}
        summary["generated_utc"] = rc.utcnow_iso()
        o = rc.atomic_write_bytes(root, "controls/CONTROL_SUMMARY.json", rc.strict_dumps(summary).encode("utf-8"))
        outputs_meta.append(o)
        status = "OK" if all_pass else "CONTROL_FAILURE"
        exit_code = 0 if all_pass else 1
        result = {"base_outcome": summary["base_outcome"],
                  "mutant_outcomes": mutant_results, "all_control_pass": all_pass,
                  "qualifier_executions": 5, "status": status}
        t_end = rc.utcnow_iso()
    except SystemExit as e:
        raise e
    except BaseException as e:
        status = "FAILED"
        exit_code = 1
        err = "%s: %s" % (type(e).__name__, e)
        result = {"error": err, "traceback": traceback.format_exc()}
        t_end = rc.utcnow_iso()
    stdout_text = rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id, "status": status,
                                   "exit": exit_code, "result": result})
    entry = {"attempt_id": attempt_id, "tool": TOOL_REL,
             "tool_sha256": rc.sha256_file(tool_abs),
             "config": rc.file_identity(cfg["_config_abs"], "RUN_CONFIG.json"),
             "argv": argv, "kind": "CONTROLS_C1_C4",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status in ("OK", "CONTROL_FAILURE") else err)
    print(stdout_text)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
