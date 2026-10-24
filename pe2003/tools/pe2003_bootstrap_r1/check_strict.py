#!/usr/bin/env python3
"""check_strict.py -- strict CSV/JSON/JSONL validator (Wave A, F08/F09 classes).

Checks (per file):
  CSV : duplicate header names; every data-row width == header width;
        sha-named columns must be 64-hex digests or empty (never prose);
        count-named columns must not hold booleans ("True"/"False");
        if expected/actual/match columns exist, match must equal
        (serialized expected == serialized actual).
  JSON: strict parse with duplicate-key REJECTION; recursive walk:
        same sha/count/match rules; booleans are real bools in JSON.
  JSONL: each line is strict JSON (same walk).

Exit code 0 iff every checked file PASSes (selftest failures also nonzero).
Usage:
  python check_strict.py --selftest            # 6 unit tests, must all PASS
  python check_strict.py <root_dir> [out.json] # walk *.csv/*.json/*.jsonl
Self-exclusion: a file named CHECKER_RESULTS.json is skipped (it is this
checker's own output; validating it inside its own generation is circular).
"""
import csv, io, json, os, re, sys

SHA_KEY = re.compile(r"^(sha256|sha256_.+|.+_sha256)$", re.I)
SHA_VAL = re.compile(r"^[0-9a-fA-F]{64}$")
CNT_KEY = re.compile(r"^(n_[a-z0-9_]+|num_[a-z0-9_]+|number_[a-z0-9_]+|.*count(er)?s?|.*_total|total|tally[a-z0-9_]*)$", re.I)

def err(li, msg):
    li.append(msg); return li

def check_match_consistency(d, where, errors):
    if all(k in d for k in ("expected", "actual")) and "match" in d:
        m = d["match"]
        eq = json.dumps(d["expected"], sort_keys=True) == json.dumps(d["actual"], sort_keys=True)
        if not isinstance(m, bool):
            err(errors, "%s: match is not a boolean (%r)" % (where, m))
        elif m != eq:
            err(errors, "%s: match=%s but serialized expected==actual is %s (F09 defect class)" % (where, m, eq))

def walk_json(obj, where, errors):
    if isinstance(obj, dict):
        for k, v in obj.items():
            w = "%s.%s" % (where, k)
            if SHA_KEY.match(k):
                if v is None or v == "":
                    continue  # empty = not applicable (allowed, documented)
                if not isinstance(v, str) or not SHA_VAL.match(v):
                    err(errors, "%s: sha-named key holds non-64-hex value (text-not-SHA): %r" % (w, str(v)[:60]))
            if CNT_KEY.match(k) and isinstance(v, bool):
                err(errors, "%s: count-named key holds a boolean (bool-as-counter)" % w)
            walk_json(v, w, errors)
        check_match_consistency(obj, where, errors)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_json(v, "%s[%d]" % (where, i), errors)

def no_dup_keys(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("duplicate key in JSON object: %r" % k)
        d[k] = v
    return d

def strict_json(text, errors, where):
    try:
        return json.loads(text, object_pairs_hook=no_dup_keys)
    except ValueError as e:
        err(errors, "%s: strict JSON parse failed: %s" % (where, e))
        return None

def check_csv(path, res):
    errors = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        return err(errors, "empty CSV (no header)")
    header = rows[0]
    if len(set(header)) != len(header):
        seen = set()
        for h in header:
            if h in seen: err(errors, "duplicate header field: %r" % h)
            seen.add(h)
    sha_cols = [i for i, h in enumerate(header) if SHA_KEY.match(h)]
    cnt_cols = [i for i, h in enumerate(header) if CNT_KEY.match(h)]
    has_match = all(h in header for h in ("expected", "actual")) and "match" in header
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(header):
            err(errors, "row %d: width %d != header width %d" % (n, len(r), len(header)))
            continue
        for i in sha_cols:
            v = r[i]
            if v != "" and not SHA_VAL.match(v):
                err(errors, "row %d col %r: not a 64-hex digest (text-not-SHA): %r" % (n, header[i], v[:60]))
        for i in cnt_cols:
            if r[i].strip().lower() in ("true", "false"):
                err(errors, "row %d col %r: boolean in count column (bool-as-counter)" % (n, header[i]))
        if has_match:
            try: m = json.loads(r[header.index("match")].strip().lower())
            except Exception: m = None
            eq = r[header.index("expected")] == r[header.index("actual")]
            if isinstance(m, bool) and m != eq:
                err(errors, "row %d: match=%s but expected==actual is %s" % (n, m, eq))
    res["rows"] = len(rows) - 1
    return errors

def check_json_any(path, res):
    errors = []
    text = open(path, "r", encoding="utf-8-sig").read()
    if path.lower().endswith(".jsonl"):
        n = 0
        for ln, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            obj = strict_json(line, errors, "line %d" % ln)
            if obj is not None: walk_json(obj, "L%d" % ln, errors)
            n += 1
        res["lines"] = n
    else:
        obj = strict_json(text, errors, "root")
        if obj is not None: walk_json(obj, "$", errors)
        res["items"] = 1 if obj is not None else 0
    return errors

def check_file(path):
    res = {"path": path, "kind": os.path.splitext(path)[1].lower().lstrip(".")}
    if path.lower().endswith(".csv"):
        errors = check_csv(path, res)
    else:
        errors = check_json_any(path, res)
    res["status"] = "PASS" if not errors else "FAIL"
    res["errors"] = errors[:20]
    if len(errors) > 20: res["errors_truncated"] = True
    return res

# ---------------- selftest ----------------
def selftest():
    import tempfile
    t = tempfile.mkdtemp(prefix="check_strict_selftest_")
    P = lambda n: os.path.join(t, n)
    results = []
    def expect(name, must_fail, build):
        p = P(name)
        build(p)
        r = check_file(p)
        failed = r["status"] == "FAIL"
        ok = (failed == must_fail)
        results.append({"case": name, "expect": "FAIL" if must_fail else "PASS",
                        "got": r["status"], "status": "PASS" if ok else "FAIL",
                        "first_error": r["errors"][0] if r["errors"] else ""})
    def w(p, s): open(p, "w", newline="", encoding="utf-8").write(s)
    expect("01_valid.csv", False, lambda p: w(p, "a,sha256,b\n1," + "0"*64 + ",x\n2," + "1"*64 + ",y\n"))
    expect("02_bad_width.csv", True, lambda p: w(p, "a,b,c\n1,2\n"))
    expect("03_dup_key.json", True, lambda p: w(p, '{"a":1,"a":2}'))
    expect("04_bool_counter.json", True, lambda p: w(p, '{"n_members": true}'))
    expect("05_match_lie.json", True, lambda p: w(p, '{"expected":"X","actual":"Y","match":true}'))
    expect("06_text_as_sha.json", True, lambda p: w(p, '{"sha256": "the hash is 561789 (verified earlier)"}'))
    # extra positives: dup header, honest match=false
    expect("07_dup_header.csv", True, lambda p: w(p, "a,a\n1,2\n"))
    expect("08_match_honest_false.json", False, lambda p: w(p, '{"expected":"X","actual":"Y","match":false}'))
    return results

def main(argv):
    if "--selftest" in argv:
        res = selftest()
        allp = all(x["status"] == "PASS" for x in res)
        for x in res:
            print("%-28s expect=%s got=%s -> %s %s" % (x["case"], x["expect"], x["got"], x["status"], x["first_error"]))
        print("SELFTEST:", "PASS (all cases behave as required)" if allp else "FAIL")
        return 0 if allp else 1
    if len(argv) < 2:
        print(__doc__); return 2
    root = argv[0]
    outp = argv[1] if len(argv) > 1 else None
    files = []
    for dirp, _, names in os.walk(root):
        for n in sorted(names):
            if n.lower().endswith((".csv", ".json", ".jsonl")):
                if n == "CHECKER_RESULTS.json":
                    continue  # self-exclusion (this checker's own output)
                files.append(os.path.join(dirp, n))
    files.sort()
    results = [check_file(p) for p in files]
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    doc = {
        "run_id": "PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024",
        "checker": os.path.abspath(__file__),
        "checker_sha256": __import__("hashlib").sha256(open(__file__, "rb").read()).hexdigest().upper(),
        "scope": "ALL *.csv/*.json/*.jsonl deliverables in SCIENCE_ROOT (this run); CHECKER_RESULTS.json self-excluded (generated by this run of the checker)",
        "selftest": selftest(),
        "files": results,
        "summary": {"n_files": len(results), "n_pass": n_pass,
                    "n_fail": len(results) - n_pass,
                    "status": "PASS" if n_pass == len(results) else "FAIL"},
    }
    js = json.dumps(doc, indent=1, ensure_ascii=False)
    if outp:
        with open(outp, "w", encoding="utf-8") as f:
            f.write(js)
    for r in results:
        print("%-4s %-52s rows/items=%s" % (r["status"], os.path.basename(r["path"]),
              r.get("rows", r.get("lines", r.get("items", "-")))))
        for e in r["errors"][:3]:
            print("      ! " + e)
    print("SUMMARY:", doc["summary"])
    if outp: print("->", outp)
    return 0 if doc["summary"]["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
