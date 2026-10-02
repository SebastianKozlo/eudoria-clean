#!/usr/bin/env python3
# QC-R4 regression harness (RUN_CONTRACT §3/§4/§5 of
# PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002).
# Builds the INVALID_VA fixture from the four canonical positive inputs
# (byte-for-byte copies + EXACTLY ONE surgical mutation), verifies the
# pre-mutation hashes against CONTRACT_FREEZE.json, machine-checks the
# single-change diff (byte level AND recursive JSON level), runs BOTH
# regressions as SUBPROCESS invocations of qc4_q1_pinverify.py (capturing
# each PID and exit code, PYTHONDONTWRITEBYTECODE=1), verifies the §4/§5
# expected values against the produced result JSONs (fail loudly on any
# mismatch - the expectations are NEVER adjusted to fit the results),
# verifies the input<->result-row bijection by identity sets in BOTH runs,
# and aggregates QC_R4_REGRESSIONS_SUMMARY.json with the §13 F1 machine
# fields. Exit 0 iff every check passed.
import sys
sys.dont_write_bytecode = True

import hashlib, json, os, subprocess

RUN_ID = "PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002"
ARTIFACTS = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]
SELECT_OLD = "0x00977807"
SELECT_NEW = "0xFFFFFFFF"
SELECT_BASELINE_INDEX = 74  # PE-MASTER baseline census (RUN_CONTRACT §5c)

REV_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.dirname(os.path.dirname(REV_ROOT))            # .../PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
RAW_CORR = os.path.join(PKG, "01_RAW", "DESKTOP_CORRECTION_R1")
QC_TOOLS = os.path.join(REV_ROOT, "qc_tools")
VALIDATOR = os.path.join(QC_TOOLS, "qc4_q1_pinverify.py")
FIXTURE_DIR = os.path.join(REV_ROOT, "FIXTURE_INVALID_VA")
FIXTURE_DIFF_PATH = os.path.join(FIXTURE_DIR, "FIXTURE_DIFF.json")
POS_DIR = os.path.join(REV_ROOT, "POSITIVE")
INV_DIR = os.path.join(REV_ROOT, "INVALID_VA")
POS_RESULT = os.path.join(POS_DIR, "QC_R4_PINVERIFY_POSITIVE_RESULT.json")
INV_RESULT = os.path.join(INV_DIR, "QC_R4_PINVERIFY_INVALID_VA_RESULT.json")
SUMMARY_PATH = os.path.join(REV_ROOT, "QC_R4_REGRESSIONS_SUMMARY.json")
FREEZE_PATH = os.path.join(PKG, "00_CONTROL", "QC_R4_CORRECTION_R1_20261002", "CONTRACT_FREEZE.json")

# ---- expected values (RUN_CONTRACT §4 / §5; NEVER adjusted to fit results)
EXPECT_POSITIVE = {
    "input_pin_count": 185, "processed_count": 185, "verified_ok": 185,
    "failed_count": 0, "error_count": 0, "mismatch_count": 0,
    "denominator": 185, "result_row_count": 185, "bijection_ok": True,
    "sem_total": 51, "sem_ok": 51, "extra_all_ok": True,
    "overall_ok": True, "exit_code": 0,
}
EXPECT_INVALID_VA = {
    "input_pin_count": 185, "processed_count": 185, "verified_ok": 184,
    "failed_count": 1, "error_count": 1, "mismatch_count": 0,
    "denominator": 185, "result_row_count": 185, "bijection_ok": True,
    "sem_total": 51, "sem_ok": 51, "extra_all_ok": True,
    "overall_ok": False, "exit_code_nonzero": True,
    "failed_row": {"pin_id": f"BRANCH_SELECTION_TRACE.json::pins[{SELECT_BASELINE_INDEX}]",
                   "source": "BRANCH_SELECTION_TRACE.json",
                   "va": SELECT_NEW, "error_retained": True},
}

FAILURES = []  # collected loud failures


def fail_loudly(msg):
    FAILURES.append(msg)
    print(f"[FAIL] {msg}")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def enumerate_pins(doc, name):
    """Mirror of the validator's pin enumeration (same qc3 loading semantics):
    returns [(pin_id, pin_dict), ...]."""
    out = []
    pins = doc.get("pins", [])
    array_path = "pins"
    if not pins and "entry_pins" in doc:
        pins = doc["entry_pins"]
        array_path = "entry_pins"
    for idx, p in enumerate(pins):
        out.append((f"{name}::{array_path}[{idx}]", p))
    for wsrc_key, wsrc in doc.get("width_sources", {}).items():
        for idx, wp in enumerate(wsrc.get("width_pins", [])):
            out.append((f"{name}::width_sources.{wsrc_key}.width_pins[{idx}]", wp))
    return out


def census_input_dir(inputs_dir):
    """Enumerate all input pins of a four-artifact input directory."""
    ids = []
    per_file = {}
    for a in ARTIFACTS:
        doc = load_json(os.path.join(inputs_dir, a))
        pins = enumerate_pins(doc, a)
        per_file[a] = len(pins)
        ids.extend(pid for (pid, _) in pins)
    return ids, per_file


def recursive_json_diff(a, b, path=""):
    """Recursive leaf diff of two parsed JSON values.
    Returns a list of {"path", "old", "new"} for every changed/added/removed leaf."""
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a.keys() | b.keys():
            child = f"{path}.{k}" if path else k
            if k not in a:
                diffs.append({"path": child, "old": None, "new": b[k], "change": "added"})
            elif k not in b:
                diffs.append({"path": child, "old": a[k], "new": None, "change": "removed"})
            else:
                diffs.extend(recursive_json_diff(a[k], b[k], child))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append({"path": path, "old": len(a), "new": len(b), "change": "list_length"})
        for i in range(min(len(a), len(b))):
            diffs.extend(recursive_json_diff(a[i], b[i], f"{path}[{i}]"))
    else:
        if a != b:
            diffs.append({"path": path, "old": a, "new": b, "change": "value"})
    return diffs


def build_fixture(freeze):
    """§5 fixture build (machine-checked, all steps mandatory). Returns a dict
    describing the fixture, or records loud failures."""
    print("== FIXTURE BUILD ==")
    os.makedirs(FIXTURE_DIR, exist_ok=True)
    pre_hashes = {}
    post_hashes = {}
    # a+b: copy all four positive inputs byte-for-byte; verify pre-mutation hashes
    for a in ARTIFACTS:
        src = os.path.join(RAW_CORR, a)
        dst = os.path.join(FIXTURE_DIR, a)
        with open(src, "rb") as f:
            data = f.read()
        with open(dst, "wb") as f:
            f.write(data)
        h = sha256_file(dst)
        expected = freeze["positive_input_sha256"][a]["sha256"].upper()
        if h != expected:
            fail_loudly(f"pre-mutation hash mismatch for {a}: fixture {h} != freeze {expected}")
        pre_hashes[a] = h
    print(f"pre-mutation hashes verified against CONTRACT_FREEZE.json: {len(pre_hashes)}/4")

    # c: selector - pins with va == "0x00977807" in the fixture BRANCH_SELECTION_TRACE.json
    fix_bst_path = os.path.join(FIXTURE_DIR, "BRANCH_SELECTION_TRACE.json")
    fix_doc = load_json(fix_bst_path)
    hits = [(i, p) for (i, p) in enumerate(fix_doc.get("pins", []))
            if isinstance(p, dict) and p.get("va") == SELECT_OLD]
    if len(hits) != 1:
        fail_loudly(f"selector matched {len(hits)} pins with va == {SELECT_OLD} "
                    f"(MUST be exactly 1); run FAILS before mutation")
        return None
    matched_index = hits[0][0]
    if matched_index != SELECT_BASELINE_INDEX:
        fail_loudly(f"selector matched index {matched_index} != baseline census index "
                    f"{SELECT_BASELINE_INDEX}; run FAILS before mutation")
        return None
    print(f"selector: exactly 1 pin with va == {SELECT_OLD} at pins[{matched_index}] (baseline census OK)")

    # d: mutate exactly that one field (surgical length-preserving byte splice)
    with open(fix_bst_path, "rb") as f:
        raw = f.read()
    lit_old = f'"va": "{SELECT_OLD}"'.encode("ascii")
    lit_new = f'"va": "{SELECT_NEW}"'.encode("ascii")
    n_lit = raw.count(lit_old)
    if n_lit != 1:
        fail_loudly(f'field literal {lit_old!r} occurs {n_lit} times (MUST be exactly 1); '
                    f"run FAILS before mutation")
        return None
    off = raw.find(lit_old)
    va_off = off + len('"va": "'.encode("ascii"))
    raw2 = raw[:off] + lit_new + raw[off + len(lit_old):]
    with open(fix_bst_path, "wb") as f:
        f.write(raw2)
    print(f"mutation applied: pins[{matched_index}].va {SELECT_OLD} -> {SELECT_NEW} "
          f"(byte offset {off}, length-preserving)")

    # e: machine-check the difference - byte level AND recursive JSON level.
    # The two 10-char VA strings share the "0x" prefix, so exactly the differing
    # characters (positions 2..9 = 8 bytes) change, contiguous, inside the va value.
    with open(fix_bst_path, "rb") as f:
        raw2 = f.read()
    byte_diff_positions = [i for i in range(len(raw)) if raw[i] != raw2[i]]
    expected_changed = [va_off + i for i in range(len(SELECT_OLD))
                        if SELECT_OLD[i] != SELECT_NEW[i]]
    byte_ok = (len(raw) == len(raw2)
              and byte_diff_positions == expected_changed)
    if not byte_ok:
        fail_loudly(f"byte-level diff is not exactly the changed characters of the single "
                    f"va value: expected {expected_changed}, measured {len(byte_diff_positions)} "
                    f"positions")
    can_doc = load_json(os.path.join(RAW_CORR, "BRANCH_SELECTION_TRACE.json"))
    fix_doc2 = load_json(fix_bst_path)
    leaf_diffs = recursive_json_diff(can_doc, fix_doc2)
    expected_leaf = {"path": f"pins[{matched_index}].va", "old": SELECT_OLD,
                     "new": SELECT_NEW, "change": "value"}
    leaf_ok = (len(leaf_diffs) == 1 and leaf_diffs[0] == expected_leaf)
    if not leaf_ok:
        fail_loudly(f"recursive JSON diff shows {len(leaf_diffs)} changed leaves, "
                    f"expected exactly 1 == {expected_leaf}: {leaf_diffs}")
    else:
        print(f"recursive JSON diff: exactly 1 changed leaf -> pins[{matched_index}].va "
              f"{SELECT_OLD} -> {SELECT_NEW}")

    # e (cont.): the other three fixture files remain hash-equal to the canonical ones
    other_identical = {}
    for a in ARTIFACTS:
        if a == "BRANCH_SELECTION_TRACE.json":
            continue
        same = sha256_file(os.path.join(FIXTURE_DIR, a)) == sha256_file(os.path.join(RAW_CORR, a))
        other_identical[a] = same
        if not same:
            fail_loudly(f"fixture file {a} is NOT byte-identical to the canonical input")
    for a in ARTIFACTS:
        post_hashes[a] = sha256_file(os.path.join(FIXTURE_DIR, a))

    # f: the fixture keeps all 185 input pin identities (value change, not structure)
    can_ids, can_per_file = census_input_dir(RAW_CORR)
    fix_ids, fix_per_file = census_input_dir(FIXTURE_DIR)
    ids_ok = (len(fix_ids) == 185
              and sorted(can_ids) == sorted(fix_ids)
              and can_per_file == fix_per_file)
    if not ids_ok:
        fail_loudly(f"fixture pin identity census broken: fixture {len(fix_ids)} ids, "
                    f"canonical {len(can_ids)}; per-file {fix_per_file} vs {can_per_file}")
    else:
        print(f"fixture pin census: {len(fix_ids)} pin identities, identical to canonical "
              f"(per-file {fix_per_file})")

    fixture_diff = {
        "run_id": RUN_ID,
        "canonical_inputs_dir": RAW_CORR,
        "fixture_dir": FIXTURE_DIR,
        "selector": {"field": "va", "old": SELECT_OLD, "new": SELECT_NEW,
                      "matched_count": len(hits), "matched_index": matched_index,
                      "baseline_census_index": SELECT_BASELINE_INDEX,
                      "exactly_one_ok": len(hits) == 1},
        "byte_level": {"same_length": len(raw) == len(raw2),
                       "va_value_offset": va_off,
                       "changed_byte_count": len(byte_diff_positions),
                       "changed_offset_start": byte_diff_positions[0] if byte_diff_positions else None,
                       "changed_offset_end_inclusive": byte_diff_positions[-1] if byte_diff_positions else None,
                       "changed_positions": byte_diff_positions,
                       "changed_positions_are_the_value_diff_chars": byte_diff_positions == expected_changed,
                       "old_chars": SELECT_OLD, "new_chars": SELECT_NEW,
                       "shared_prefix_chars": 2,
                       "single_field_splice_ok": byte_ok},
        "json_recursive_diff": {"changed_leaf_count": len(leaf_diffs),
                                "changed_leaves": leaf_diffs,
                                "exactly_one_changed_leaf_ok": leaf_ok},
        "other_files_byte_identical": other_identical,
        "pre_mutation_sha256": pre_hashes,
        "post_mutation_sha256": post_hashes,
        "fixture_pin_census": {"count": len(fix_ids),
                                "per_artifact": fix_per_file,
                                "pin_ids_identical_to_canonical": ids_ok},
    }
    with open(FIXTURE_DIFF_PATH, "w", encoding="utf-8") as f:
        json.dump(fixture_diff, f, indent=2)
    print(f"FIXTURE_DIFF.json written: {FIXTURE_DIFF_PATH}")
    return fixture_diff


def run_validator(label, inputs_dir, output_path):
    """Run qc4_q1_pinverify.py as a SUBPROCESS with PYTHONDONTWRITEBYTECODE=1,
    bounded timeout, PID + exit code captured independently."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, VALIDATOR, "--inputs", inputs_dir, "--output", output_path]
    print(f"== REGRESSION {label} ==\nsubprocess: {cmd}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, env=env, cwd=QC_TOOLS)
    pid = proc.pid
    timed_out = False
    try:
        out, err = proc.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        out, err = proc.communicate()
        fail_loudly(f"{label}: validator subprocess PID {pid} timed out after 600 s (killed)")
    exit_code = proc.returncode
    print(f"PID {pid} | exit code {exit_code}" + (" | TIMED OUT" if timed_out else ""))
    if err and err.strip():
        print(f"[stderr] {err.strip()[:2000]}")
    return {"pid": pid, "exit_code": exit_code, "timed_out": timed_out,
            "cmd": cmd, "stdout_tail": out.strip()[-2000:] if out else "",
            "stderr": (err or "").strip()[:2000]}


def verify_run(label, proc_info, result_path, inputs_dir, expected, negative):
    """Verify the §4/§5 expected values against the produced result JSON.
    Returns the measured values dict; records loud failures on any mismatch."""
    measured = {}
    if not os.path.isfile(result_path):
        fail_loudly(f"{label}: result JSON missing: {result_path}")
        return None
    res = load_json(result_path)
    c = res.get("census", {})
    sem = c.get("semantic_assertions", {})
    extra = c.get("extra_checks", {})
    measured = {
        "input_pin_count": c.get("input_pin_count"),
        "processed_count": c.get("processed_count"),
        "verified_ok": c.get("verified_ok"),
        "failed_count": c.get("failed_count"),
        "mismatch_count": c.get("mismatch_count"),
        "error_count": c.get("error_count"),
        "denominator": c.get("denominator"),
        "result_row_count": c.get("result_row_count"),
        "bijection_ok": c.get("bijection_ok"),
        "sem_total": sem.get("total"),
        "sem_ok": sem.get("ok"),
        "extra_all_ok": extra.get("all_required_ok"),
        "overall_ok": c.get("overall_ok"),
        "exit_code": proc_info["exit_code"],
    }
    # field-by-field expected-vs-measured (loud, no adjustment)
    field_map = [("input_pin_count", expected["input_pin_count"]),
                 ("processed_count", expected["processed_count"]),
                 ("verified_ok", expected["verified_ok"]),
                 ("failed_count", expected["failed_count"]),
                 ("error_count", expected["error_count"]),
                 ("mismatch_count", expected["mismatch_count"]),
                 ("denominator", expected["denominator"]),
                 ("result_row_count", expected["result_row_count"]),
                 ("bijection_ok", expected["bijection_ok"]),
                 ("sem_total", expected["sem_total"]),
                 ("sem_ok", expected["sem_ok"]),
                 ("extra_all_ok", expected["extra_all_ok"]),
                 ("overall_ok", expected["overall_ok"])]
    for field, exp in field_map:
        got = measured[field]
        status = "OK" if got == exp else "MISMATCH"
        print(f"  {label:10s} {field:18s} expected {exp!r:8} measured {got!r:8} {status}")
        if got != exp:
            fail_loudly(f"{label}: field {field} expected {exp!r}, measured {got!r}")
    # exit code
    if negative:
        if measured["exit_code"] == 0:
            fail_loudly(f"{label}: expected NONZERO exit code, measured 0")
        else:
            print(f"  {label:10s} exit_code           expected nonzero, measured {measured['exit_code']}! OK (successful negative regression)")
    else:
        if measured["exit_code"] != expected["exit_code"]:
            fail_loudly(f"{label}: expected exit code {expected['exit_code']}, measured {measured['exit_code']}")
    # exe identity must have been checked and OK in both runs
    if not res.get("exe_identity", {}).get("ok"):
        fail_loudly(f"{label}: exe_identity.ok is not True in the result JSON")
    if res.get("run_errors"):
        fail_loudly(f"{label}: run_errors present in a passing-config run: {res['run_errors']}")

    # independent bijection verification by identity sets (runner-side)
    input_ids, _per_file = census_input_dir(inputs_dir)
    row_ids = [r.get("pin_id") for r in res.get("pins", [])]
    bij = (len(input_ids) == len(set(input_ids))
           and len(row_ids) == len(set(row_ids))
           and len(input_ids) == len(row_ids)
           and set(input_ids) == set(row_ids))
    if not bij:
        fail_loudly(f"{label}: runner-side identity-set bijection FAILED "
                    f"(inputs {len(input_ids)}, rows {len(row_ids)})")
    else:
        print(f"  {label:10s} runner-side identity-set bijection OK ({len(input_ids)} inputs == {len(row_ids)} rows)")
    measured["runner_bijection_ok"] = bij

    # negative-run specifics: exactly one FAILED row with preserved identity
    if negative:
        failed_rows = [r for r in res.get("pins", []) if r.get("status") == "FAILED"]
        if len(failed_rows) != 1:
            fail_loudly(f"{label}: expected exactly 1 FAILED row, found {len(failed_rows)}")
        else:
            fr = failed_rows[0]
            exp_fr = expected["failed_row"]
            checks = [
                ("pin_id", fr.get("pin_id") == exp_fr["pin_id"]),
                ("source", fr.get("source") == exp_fr["source"]),
                ("va", fr.get("va") == exp_fr["va"]),
                ("error_retained", isinstance(fr.get("error"), str) and len(fr["error"]) > 0),
                ("ok_false", fr.get("ok") is False),
            ]
            for nm, ok in checks:
                print(f"  {label:10s} FAILED-row {nm:16s} {'OK' if ok else 'MISMATCH'}"
                      + ("" if ok else f" (measured {fr.get(nm)!r})"))
                if not ok:
                    fail_loudly(f"{label}: FAILED-row check {nm} failed: {fr}")
            measured["failed_row"] = {k: fr.get(k) for k in ("pin_id", "source", "va", "error", "status")}
    return measured


def main():
    print(f"RUN_ID: {RUN_ID}")
    print(f"revision root: {REV_ROOT}")
    if not os.path.isfile(VALIDATOR):
        fail_loudly(f"validator missing: {VALIDATOR}")
    if not os.path.isfile(FREEZE_PATH):
        fail_loudly(f"CONTRACT_FREEZE.json missing: {FREEZE_PATH}")
        freeze = {}
    else:
        freeze = load_json(FREEZE_PATH)
        if freeze.get("run_id") != RUN_ID:
            fail_loudly(f"CONTRACT_FREEZE.json run_id mismatch: {freeze.get('run_id')!r}")

    os.makedirs(POS_DIR, exist_ok=True)
    os.makedirs(INV_DIR, exist_ok=True)

    fixture_diff = build_fixture(freeze)

    # ---- run both regressions as subprocesses
    pos_proc = run_validator("POSITIVE", RAW_CORR, POS_RESULT)
    inv_proc = run_validator("INVALID_VA", FIXTURE_DIR, INV_RESULT)

    pos_meas = verify_run("POSITIVE", pos_proc, POS_RESULT, RAW_CORR,
                          EXPECT_POSITIVE, negative=False)
    inv_meas = verify_run("INVALID_VA", inv_proc, INV_RESULT, FIXTURE_DIR,
                          EXPECT_INVALID_VA, negative=True)

    positive_pass = (not FAILURES) if pos_meas else False  # refined below
    # per-run PASS predicates (§4/§5), computed independently of the printout
    def positive_pass_predicate(m, p):
        return (m is not None and p["exit_code"] == 0 and m["runner_bijection_ok"]
                and m["input_pin_count"] == 185 and m["processed_count"] == 185
                and m["verified_ok"] == 185 and m["failed_count"] == 0
                and m["error_count"] == 0 and m["mismatch_count"] == 0
                and m["denominator"] == 185 and m["result_row_count"] == 185
                and m["bijection_ok"] is True and m["sem_ok"] == 51 and m["sem_total"] == 51
                and m["extra_all_ok"] is True and m["overall_ok"] is True)

    def invalid_va_pass_predicate(m, p):
        base = (m is not None and p["exit_code"] != 0 and m["runner_bijection_ok"]
                and m["input_pin_count"] == 185 and m["processed_count"] == 185
                and m["verified_ok"] == 184 and m["failed_count"] == 1
                and m["error_count"] == 1 and m["mismatch_count"] == 0
                and m["denominator"] == 185 and m["result_row_count"] == 185
                and m["bijection_ok"] is True and m["sem_ok"] == 51 and m["sem_total"] == 51
                and m["extra_all_ok"] is True and m["overall_ok"] is False
                and m.get("failed_row", {}).get("pin_id")
                == EXPECT_INVALID_VA["failed_row"]["pin_id"])
        return base

    positive_pass = positive_pass_predicate(pos_meas, pos_proc)
    invalid_va_pass = invalid_va_pass_predicate(inv_meas, inv_proc)

    pos_input_hashes = {a: sha256_file(os.path.join(RAW_CORR, a)) for a in ARTIFACTS}
    inv_input_hashes = {a: sha256_file(os.path.join(FIXTURE_DIR, a)) for a in ARTIFACTS}
    validator_sha = sha256_file(VALIDATOR)

    summary = {
        "run_id": RUN_ID,
        "generated_by": "qc4_regression_runner.py (executor harness; PE-MASTER direct dispatch)",
        "expectation_source": "RUN_CONTRACT.md §4 (POSITIVE) / §5 (INVALID_VA) / §13 (machine fields)",
        "positive": {
            "INPUT_PIN_COUNT": pos_meas["input_pin_count"] if pos_meas else None,
            "PROCESSED_COUNT": pos_meas["processed_count"] if pos_meas else None,
            "VERIFIED_OK": pos_meas["verified_ok"] if pos_meas else None,
            "FAILED_COUNT": pos_meas["failed_count"] if pos_meas else None,
            "ERROR_COUNT": pos_meas["error_count"] if pos_meas else None,
            "MISMATCH_COUNT": pos_meas["mismatch_count"] if pos_meas else None,
            "DENOMINATOR": pos_meas["denominator"] if pos_meas else None,
            "RESULT_ROW_COUNT": pos_meas["result_row_count"] if pos_meas else None,
            "SEMANTIC_ASSERTIONS": {"TOTAL": pos_meas["sem_total"] if pos_meas else None,
                                    "OK": pos_meas["sem_ok"] if pos_meas else None},
            "EXTRA_CHECKS_ALL_REQUIRED_OK": pos_meas["extra_all_ok"] if pos_meas else None,
            "OVERALL_OK": pos_meas["overall_ok"] if pos_meas else None,
            "PROCESS_EXIT_CODE": pos_proc["exit_code"],
            "PROCESS_PID": pos_proc["pid"],
            "REGRESSION_PASS": positive_pass,
            "INPUT_RESULT_BIJECTION": pos_meas["runner_bijection_ok"] if pos_meas else False,
            "INPUT_HASHES": pos_input_hashes,
            "INPUTS_DIR": RAW_CORR,
            "RESULT_PATH": POS_RESULT,
            "RESULT_SHA256": sha256_file(POS_RESULT) if os.path.isfile(POS_RESULT) else None,
        },
        "invalid_va": {
            "INPUT_PIN_COUNT": inv_meas["input_pin_count"] if inv_meas else None,
            "PROCESSED_COUNT": inv_meas["processed_count"] if inv_meas else None,
            "VERIFIED_OK": inv_meas["verified_ok"] if inv_meas else None,
            "FAILED_COUNT": inv_meas["failed_count"] if inv_meas else None,
            "ERROR_COUNT": inv_meas["error_count"] if inv_meas else None,
            "MISMATCH_COUNT": inv_meas["mismatch_count"] if inv_meas else None,
            "DENOMINATOR": inv_meas["denominator"] if inv_meas else None,
            "RESULT_ROW_COUNT": inv_meas["result_row_count"] if inv_meas else None,
            "SEMANTIC_ASSERTIONS": {"TOTAL": inv_meas["sem_total"] if inv_meas else None,
                                    "OK": inv_meas["sem_ok"] if inv_meas else None},
            "EXTRA_CHECKS_ALL_REQUIRED_OK": inv_meas["extra_all_ok"] if inv_meas else None,
            "OVERALL_OK": inv_meas["overall_ok"] if inv_meas else None,
            "PROCESS_EXIT_CODE": inv_proc["exit_code"],
            "PROCESS_PID": inv_proc["pid"],
            "REGRESSION_PASS": invalid_va_pass,
            "INPUT_RESULT_BIJECTION": inv_meas["runner_bijection_ok"] if inv_meas else False,
            "FAILED_ROW": inv_meas.get("failed_row") if inv_meas else None,
            "INPUT_HASHES": inv_input_hashes,
            "INPUTS_DIR": FIXTURE_DIR,
            "RESULT_PATH": INV_RESULT,
            "RESULT_SHA256": sha256_file(INV_RESULT) if os.path.isfile(INV_RESULT) else None,
        },
        "FIXTURE_DIFF_PATH": FIXTURE_DIFF_PATH,
        "FIXTURE_DIFF_SHA256": sha256_file(FIXTURE_DIFF_PATH) if os.path.isfile(FIXTURE_DIFF_PATH) else None,
        "FIXTURE_SUMMARY": {
            "selector_exactly_one": fixture_diff["selector"]["exactly_one_ok"] if fixture_diff else False,
            "single_field_byte_splice_ok": fixture_diff["byte_level"]["single_field_splice_ok"] if fixture_diff else False,
            "exactly_one_changed_leaf_ok": fixture_diff["json_recursive_diff"]["exactly_one_changed_leaf_ok"] if fixture_diff else False,
            "other_files_byte_identical": fixture_diff["other_files_byte_identical"] if fixture_diff else None,
            "fixture_pin_census_count": fixture_diff["fixture_pin_census"]["count"] if fixture_diff else None,
            "pin_ids_identical_to_canonical": fixture_diff["fixture_pin_census"]["pin_ids_identical_to_canonical"] if fixture_diff else False,
        },
        "NEW_VALIDATOR_SOURCE_SHA256": validator_sha,
        "NEW_QC_REVISION_PATH": "04_QC\\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\\",
        "HARNESS_FAILURES": list(FAILURES),
        "OVERALL_REGRESSIONS_PASS": (positive_pass and invalid_va_pass and not FAILURES),
    }
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"== SUMMARY ==\nQC_R4_REGRESSIONS_SUMMARY.json written: {SUMMARY_PATH}")
    print(json.dumps({
        "POSITIVE_REGRESSION_PASS": positive_pass,
        "INVALID_VA_REGRESSION_PASS": invalid_va_pass,
        "HARNESS_FAILURES": len(FAILURES),
        "OVERALL_REGRESSIONS_PASS": summary["OVERALL_REGRESSIONS_PASS"]}, indent=2))
    sys.exit(0 if summary["OVERALL_REGRESSIONS_PASS"] else 1)


if __name__ == "__main__":
    main()
