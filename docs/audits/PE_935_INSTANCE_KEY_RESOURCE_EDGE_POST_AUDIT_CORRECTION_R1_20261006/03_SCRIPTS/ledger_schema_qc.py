#!/usr/bin/env python3
"""ledger_schema_qc.py — fail-closed machine-readable schema QC for the two
CORRECTED ledgers of PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006.

Contract sections 6-8:
- separate explicit schemas for FUNCTION_LEDGER_CORRECTED.csv (10 cols, NO STATUS
  column) and EDGE_LEDGER_CORRECTED.csv (11 cols, STATUS + CITED separated);
- exact headers/order/width; no duplicate headers or primary IDs; zero
  DictReader extra/null-key/missing cells; identity/source separation;
- CITED_PHYSICAL_SOURCE non-empty and either explicitly UNKNOWN/NOT_CHECKED or
  referencing >=1 EXISTING artifact of the READ-ONLY source package
  (mechanical traceability of the reconstructed fields to permitted evidence);
- EDGE STATUS vocabulary + swap detection (evidence path cannot pass as STATUS;
  a STATUS token cannot pass as CITED_PHYSICAL_SOURCE);
- mutation mode MUT-A/MUT-B (per table) and MUT-C (EDGE only) run the SAME
  production validators on TEMP COPIES (never the clean ledgers) and record the
  exact failed predicates.

This checker does NOT prove PCG semantics or physical provenance beyond the
CSV schema + artifact-existence layer (contract section 7 disclaimer). It never
consults the manifest or Git state: a mutation rejection is caused only by the
schema predicates.

Exit codes: 0 = all requested checks PASS (check mode) / all mutants REJECTED
(mutate mode); 2 = at least one FAIL. No default-success fallback.
"""
import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DEFAULT_SOURCE_PACKAGE = os.path.join(
    REPO_ROOT, "docs", "audits", "PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006")

FUNCTION_HEADER = [
    "ORD", "FUNCTION_ID", "EXTENT", "BUDGET_ROLE", "FUNCTION_IDENTITY",
    "IDENTITY_EVIDENCE", "OBSERVED_OPERATION", "FINAL_SEMANTIC_ROLE",
    "HISTORICAL_INPUT_AVAILABILITY", "CITED_PHYSICAL_SOURCE",
]
EDGE_HEADER = [
    "EDGE_ID", "KIND", "SITE_OR_SOURCE", "INSTRUCTION_VA", "INSTRUCTION_BYTES",
    "TARGET_OR_DESTINATION_ARITHMETIC", "FIELD_REGISTER_VALUE",
    "RECEIVER_PROOF", "PATH_CONDITIONS", "STATUS", "CITED_PHYSICAL_SOURCE",
]

# Explicitly declared allowed STATUS vocabulary (EDGE ledger only). A STATUS is
# valid iff it starts with one of these head tokens.
STATUS_VOCABULARY = [
    "UNRESOLVED_IN_BUDGET",
    "NON-CANONICAL LEAD",
    "EDGE RECORDED",
    "CONFIRMED",
    "UNRESOLVED",
    "UNKNOWN",
    "NOT_CHECKED",
]
STATUS_HEAD_RE = re.compile(
    r"^(CONFIRMED|UNRESOLVED_IN_BUDGET|UNRESOLVED|EDGE RECORDED|NON-CANONICAL LEAD|UNKNOWN|NOT_CHECKED)\b")

# Evidence-path shape: directory prefixes / file extensions. A STATUS cell
# matching this shape is an evidence path masquerading as a status (FAIL).
EVIDENCE_PATH_RE = re.compile(
    r"01_RAW/|00_CONTROL_INTERNAL_QC/|03_SCRIPTS/|\.txt\b|\.json\b|\.csv\b|\.py\b|\.md\b")

# Cited-artifact tokens (source-package physical evidence) -> relative paths.
CITED_ARTIFACTS = {
    "BYTE_WINDOWS.txt": "01_RAW/BYTE_WINDOWS.txt",
    "E8_CENSUS.json": "01_RAW/E8_CENSUS.json",
    "GETTER_PIN.txt": "01_RAW/GETTER_PIN.txt",
    "GETTER_PIN.json": "01_RAW/GETTER_PIN.json",
    "GHIDRA_VERIFY.json": "01_RAW/GHIDRA_VERIFY.json",
    "GHIDRA_DISASM_WINDOWS.txt": "01_RAW/GHIDRA_DISASM_WINDOWS.txt",
    "GHIDRA_DECOMPILES.txt": "01_RAW/GHIDRA_DECOMPILES.txt",
    "GovernanceWriteTime.txt": "01_RAW/GovernanceWriteTime.txt",
    "QC_CONTROLS.json": "01_RAW/QC_CONTROLS.json",
    "RTTI_PROBES.json": "01_RAW/RTTI_PROBES.json",
    "QC_GATES.csv": "00_CONTROL_INTERNAL_QC/QC_GATES.csv",
    "QC_REPORT_INTERNAL.md": "00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md",
    "CALLSITE_SHORTLIST.csv": "CALLSITE_SHORTLIST.csv",
    "FINAL_REPORT.md": "FINAL_REPORT.md",
    "QC_REPORT.md": "QC_REPORT.md",
    "FUNCTION_LEDGER.csv": "FUNCTION_LEDGER.csv",
    "EDGE_LEDGER.csv": "EDGE_LEDGER.csv",
}
CITED_TOKEN_RE = re.compile("|".join(re.escape(k) for k in CITED_ARTIFACTS))

EXPLICIT_EMPTY_VALUES = {"UNKNOWN", "NOT_CHECKED"}


def fail(results, code, detail, row=None):
    results["failures"].append({"check": code, "row": row, "detail": detail})


def check_ledger(path, schema_name, source_package):
    """Run ALL production schema predicates on one ledger file.

    Returns a dict with per-check booleans, the failure list and the verdict.
    The SAME function is used for the clean ledgers and for every mutant.
    """
    results = {
        "schema": schema_name,
        "file": os.path.basename(path),
        "header": [],
        "data_row_count": 0,
        "row_widths": [],
        "checks": {},
        "failures": [],
    }
    ok = True

    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(results, "NO_BOM", "file starts with a UTF-8 BOM")
        results["checks"]["NO_BOM"] = False
    else:
        results["checks"]["NO_BOM"] = True
    if b"\r\n" in raw:
        fail(results, "LF_ONLY", "file contains CRLF bytes")
        results["checks"]["LF_ONLY"] = False
    else:
        results["checks"]["LF_ONLY"] = True

    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    header = schema = FUNCTION_HEADER if schema_name == "FUNCTION" else EDGE_HEADER
    if not rows:
        fail(results, "FILE_NONEMPTY", "no rows at all")
        results["checks"]["FILE_NONEMPTY"] = False
        results["verdict"] = "FAIL"
        return results
    results["header"] = rows[0]

    # 1. exact header names and order (+ no duplicate header names)
    hdr_ok = rows[0] == schema
    if not hdr_ok:
        fail(results, "HEADER_EXACT", "header %r != schema %r" % (rows[0], schema))
    if len(set(rows[0])) != len(rows[0]):
        hdr_ok = False
        fail(results, "HEADER_NO_DUPLICATES", "duplicate header name present")
    results["checks"]["HEADER_EXACT_AND_UNIQUE"] = hdr_ok

    # 2. FUNCTION ledger must NOT have a STATUS column
    if schema_name == "FUNCTION":
        no_status = "STATUS" not in rows[0]
        if not no_status:
            fail(results, "FUNCTION_NO_STATUS_COLUMN",
                 "FUNCTION ledger has a STATUS column (forbidden)")
        results["checks"]["FUNCTION_NO_STATUS_COLUMN"] = no_status

    data = [r for r in rows[1:] if r]
    results["data_row_count"] = len(data)
    widths = sorted(set(len(r) for r in data))
    results["row_widths"] = widths
    width_ok = all(len(r) == len(schema) for r in data)
    if not width_ok:
        fail(results, "ROW_WIDTH_EXACT",
             "row widths %r != %d" % (widths, len(schema)))
    results["checks"]["ROW_WIDTH_EXACT"] = width_ok

    # 3+4. DictReader layer: no extra (restkey), no missing (None) cells
    with open(path, "r", encoding="utf-8", newline="") as fh:
        dr = csv.DictReader(fh, restkey="__EXTRA__", restval=None)
        dict_rows = list(dr)
        fieldnames = dr.fieldnames
    extra_null_fail = False
    for i, r in enumerate(dict_rows):
        if "__EXTRA__" in r:
            extra_null_fail = True
            fail(results, "DICTREADER_NO_EXTRA_CELLS",
                 "row %d has overflow cells %r" % (i + 2, r["__EXTRA__"]),
                 row=i + 2)
        for k, v in r.items():
            if k == "__EXTRA__":
                continue
            if v is None:
                extra_null_fail = True
                fail(results, "DICTREADER_NO_MISSING_CELLS",
                     "row %d missing cell for %s" % (i + 2, k), row=i + 2)
    if fieldnames != schema:
        extra_null_fail = True
        fail(results, "DICTREADER_FIELDNAMES", "DictReader fieldnames != schema")
    results["checks"]["DICTREADER_NO_EXTRA_NO_MISSING"] = not extra_null_fail

    # 5. no duplicate primary IDs
    pk = "ORD" if schema_name == "FUNCTION" else "EDGE_ID"
    seen = {}
    dup = False
    for i, r in enumerate(data):
        if not r:
            continue
        key = r[schema.index(pk)]
        if key in seen:
            dup = True
            fail(results, "PRIMARY_ID_UNIQUE",
                 "duplicate %s %r (rows %d and %d)" % (pk, key, seen[key], i + 2))
        else:
            seen[key] = i + 2
    results["checks"]["PRIMARY_ID_UNIQUE"] = not dup

    # 6. no empty required cells
    empty_fail = False
    for i, r in enumerate(data):
        if len(r) != len(schema):
            continue  # already failed by width
        for j, col in enumerate(schema):
            if r[j] is None or str(r[j]).strip() == "":
                empty_fail = True
                fail(results, "NO_EMPTY_REQUIRED_CELLS",
                     "row %d column %s is empty" % (i + 2, col), row=i + 2)
    results["checks"]["NO_EMPTY_REQUIRED_CELLS"] = not empty_fail

    # 7. identity/source separation (both tables)
    sep_fail = False
    idx = {c: schema.index(c) for c in schema}
    for i, r in enumerate(data):
        if len(r) != len(schema):
            continue
        if schema_name == "FUNCTION":
            a, b, c = (r[idx["FUNCTION_IDENTITY"]], r[idx["IDENTITY_EVIDENCE"]],
                       r[idx["CITED_PHYSICAL_SOURCE"]])
            if a == b or b == c or a == c:
                sep_fail = True
                fail(results, "IDENTITY_SOURCE_SEPARATION",
                     "row %d: identity/evidence/cited fields collide" % (i + 2),
                     row=i + 2)
        else:
            s, c = r[idx["STATUS"]], r[idx["CITED_PHYSICAL_SOURCE"]]
            if s == c:
                sep_fail = True
                fail(results, "IDENTITY_SOURCE_SEPARATION",
                     "row %d: STATUS == CITED_PHYSICAL_SOURCE" % (i + 2), row=i + 2)
    results["checks"]["IDENTITY_SOURCE_SEPARATION"] = not sep_fail

    # 8. CITED_PHYSICAL_SOURCE: non-empty; explicit UNKNOWN/NOT_CHECKED allowed;
    #    else must cite >=1 EXISTING source-package artifact (traceability).
    cited_fail = False
    for i, r in enumerate(data):
        if len(r) != len(schema):
            continue
        cited = r[idx["CITED_PHYSICAL_SOURCE"]].strip()
        if cited in EXPLICIT_EMPTY_VALUES:
            continue
        tokens = set(CITED_TOKEN_RE.findall(cited))
        if not tokens:
            cited_fail = True
            fail(results, "CITED_EXISTING_ARTIFACT",
                 "row %d: CITED_PHYSICAL_SOURCE cites no known artifact" % (i + 2),
                 row=i + 2)
            continue
        for t in sorted(tokens):
            rel = CITED_ARTIFACTS[t]
            full = os.path.join(source_package, rel.replace("/", os.sep))
            if not os.path.isfile(full):
                cited_fail = True
                fail(results, "CITED_EXISTING_ARTIFACT",
                     "row %d: cited artifact missing on disk: %s" % (i + 2, rel),
                     row=i + 2)
    results["checks"]["CITED_EXISTING_ARTIFACT"] = not cited_fail

    # 9. EDGE-only semantic gates
    if schema_name == "EDGE":
        vocab_fail = path_fail = swap_fail = False
        for i, r in enumerate(data):
            if len(r) != len(schema):
                continue
            status = r[idx["STATUS"]].strip()
            cited = r[idx["CITED_PHYSICAL_SOURCE"]].strip()
            if not STATUS_HEAD_RE.match(status):
                vocab_fail = True
                fail(results, "STATUS_VOCABULARY",
                     "row %d: STATUS %r outside the declared vocabulary" %
                     (i + 2, status[:60]), row=i + 2)
            if EVIDENCE_PATH_RE.search(status):
                path_fail = True
                fail(results, "STATUS_NOT_EVIDENCE_PATH",
                     "row %d: an evidence path cannot pass as STATUS: %r" %
                     (i + 2, status[:60]), row=i + 2)
            if cited not in EXPLICIT_EMPTY_VALUES and STATUS_HEAD_RE.match(cited):
                swap_fail = True
                fail(results, "CITED_NOT_STATUS_TOKEN",
                     "row %d: a STATUS token cannot pass as CITED_PHYSICAL_SOURCE: %r"
                     % (i + 2, cited[:60]), row=i + 2)
        results["checks"]["STATUS_VOCABULARY"] = not vocab_fail
        results["checks"]["STATUS_NOT_EVIDENCE_PATH"] = not path_fail
        results["checks"]["CITED_NOT_STATUS_TOKEN"] = not swap_fail

    # 10. FUNCTION prose-field meanings (own meanings; edge enum NOT applied)
    if schema_name == "FUNCTION":
        prose_cols = ["FUNCTION_IDENTITY", "IDENTITY_EVIDENCE",
                      "OBSERVED_OPERATION", "FINAL_SEMANTIC_ROLE",
                      "HISTORICAL_INPUT_AVAILABILITY"]
        prose_fail = False
        for i, r in enumerate(data):
            if len(r) != len(schema):
                continue
            for col in prose_cols:
                v = r[idx[col]].strip()
                if v == "":
                    prose_fail = True
                    fail(results, "FUNCTION_PROSE_FIELDS_NONEMPTY",
                         "row %d: %s empty" % (i + 2, col), row=i + 2)
        results["checks"]["FUNCTION_PROSE_FIELDS_NONEMPTY"] = not prose_fail

    results["verdict"] = "PASS" if not results["failures"] else "FAIL"
    return results


def run_check(args):
    function_res = check_ledger(args.function, "FUNCTION", args.source)
    edge_res = check_ledger(args.edge, "EDGE", args.source)
    overall = "PASS" if (function_res["verdict"] == "PASS"
                         and edge_res["verdict"] == "PASS") else "FAIL"
    out = {
        "run": "LEDGER_SCHEMA_QC",
        "mode": "check",
        "source_package": os.path.relpath(args.source, REPO_ROOT).replace("\\", "/"),
        "function_ledger": function_res,
        "edge_ledger": edge_res,
        "overall": overall,
    }
    payload = json.dumps(out, indent=1)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload + "\n")
        print("JSON ->", args.json)
    print("FUNCTION_LEDGER_SCHEMA = %s" % function_res["verdict"])
    print("EDGE_LEDGER_SCHEMA = %s" % edge_res["verdict"])
    print("OVERALL = %s" % overall)
    for res in (function_res, edge_res):
        for f in res["failures"]:
            print("FAIL %s %s row=%s %s" % (res["schema"], f["check"], f["row"],
                                            f["detail"][:160]))
    return 0 if overall == "PASS" else 2


def load_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerows(rows)


def apply_mutation(rows, schema_name, kind):
    """Return (mutated rows, mutated row id). Row index 1 = first data row."""
    mutated = [list(r) for r in rows]
    idx = 1  # first data row (ORD=1 / E-GETTER) — not chosen to force PASS
    rid = mutated[idx][0]
    if kind == "MUT_A_EXTRA_CELL":
        mutated[idx].append("__MUT_EXTRA_CELL__")
    elif kind == "MUT_B_MISSING_CELL":
        mutated[idx].pop()
    elif kind == "MUT_C_STATUS_SWAP":
        header = FUNCTION_HEADER if schema_name == "FUNCTION" else EDGE_HEADER
        si = header.index("STATUS")
        ci = header.index("CITED_PHYSICAL_SOURCE")
        mutated[idx][si], mutated[idx][ci] = mutated[idx][ci], mutated[idx][si]
    else:
        raise ValueError(kind)
    return mutated, rid


def run_mutate(args):
    mutations = [
        ("MUT_A_FUNCTION", args.function, "FUNCTION", "MUT_A_EXTRA_CELL",
         "SCHEMA_GATE"),
        ("MUT_A_EDGE", args.edge, "EDGE", "MUT_A_EXTRA_CELL", "SCHEMA_GATE"),
        ("MUT_B_FUNCTION", args.function, "FUNCTION", "MUT_B_MISSING_CELL",
         "SCHEMA_GATE"),
        ("MUT_B_EDGE", args.edge, "EDGE", "MUT_B_MISSING_CELL", "SCHEMA_GATE"),
        ("MUT_C_EDGE", args.edge, "EDGE", "MUT_C_STATUS_SWAP",
         "SEMANTIC_SCHEMA_GATE"),
    ]
    # clean baselines (the SAME production validator, clean tables)
    clean_f = check_ledger(args.function, "FUNCTION", args.source)
    clean_e = check_ledger(args.edge, "EDGE", args.source)
    tmpdir = tempfile.mkdtemp(prefix="pe935c_mut_")
    records = []
    all_rejected = True
    try:
        for mid, path, schema_name, kind, gate in mutations:
            rows = load_rows(path)
            mutated, rid = apply_mutation(rows, schema_name, kind)
            tmp_path = os.path.join(tmpdir, "%s_%s" % (mid, os.path.basename(path)))
            write_rows(tmp_path, mutated)
            res = check_ledger(tmp_path, schema_name, args.source)
            baseline = (clean_f if schema_name == "FUNCTION" else clean_e)["verdict"]
            rejected = res["verdict"] == "FAIL"
            failed_predicates = sorted(set(f["check"] for f in res["failures"]))
            records.append({
                "mutation_id": mid,
                "table": schema_name + "_LEDGER",
                "gate": gate,
                "mutation": ("introduce one extra CSV cell" if kind == "MUT_A_EXTRA_CELL"
                             else "remove one required cell" if kind == "MUT_B_MISSING_CELL"
                             else "swap STATUS and CITED_PHYSICAL_SOURCE (width preserved)"),
                "mutated_row_primary_id": rid,
                "clean_baseline_result": baseline,
                "mutated_result": res["verdict"],
                "mutant_rejected_by_production_validator": rejected,
                "exact_failed_predicates": failed_predicates,
                "verdict": "CAUSAL_FAIL" if (rejected and baseline == "PASS")
                           else ("UNEXPECTED_MUTANT_PASS" if not rejected
                                 else "BASELINE_NOT_PASS"),
            })
            if not rejected or baseline != "PASS":
                all_rejected = False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    out = {
        "run": "LEDGER_SCHEMA_QC",
        "mode": "mutate",
        "temp_copies": "created under a system temp dir and DELETED after each "
                       "measurement; the clean corrected ledgers were never "
                       "modified (mutants are copies only)",
        "clean_function_verdict": clean_f["verdict"],
        "clean_edge_verdict": clean_e["verdict"],
        "mutations": records,
        "all_mutants_causally_rejected": all_rejected,
    }
    payload = json.dumps(out, indent=1)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload + "\n")
        print("JSON ->", args.json)
    for r in records:
        print("%s table=%s row=%s clean=%s mutated=%s predicates=%s verdict=%s" % (
            r["mutation_id"], r["table"], r["mutated_row_primary_id"],
            r["clean_baseline_result"], r["mutated_result"],
            ",".join(r["exact_failed_predicates"]) or "-", r["verdict"]))
    print("ALL_MUTANTS_CAUSALLY_REJECTED = %s" % all_rejected)
    return 0 if all_rejected else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="validate the two corrected ledgers")
    c.add_argument("--function", required=True)
    c.add_argument("--edge", required=True)
    c.add_argument("--source", default=DEFAULT_SOURCE_PACKAGE)
    c.add_argument("--json")

    m = sub.add_parser("mutate", help="causal mutation tests on TEMP COPIES")
    m.add_argument("--function", required=True)
    m.add_argument("--edge", required=True)
    m.add_argument("--source", default=DEFAULT_SOURCE_PACKAGE)
    m.add_argument("--json")

    args = ap.parse_args()
    if args.cmd == "check":
        return run_check(args)
    return run_mutate(args)


if __name__ == "__main__":
    sys.exit(main())
