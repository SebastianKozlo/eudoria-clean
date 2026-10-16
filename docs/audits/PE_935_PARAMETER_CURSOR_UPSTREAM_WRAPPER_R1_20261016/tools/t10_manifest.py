# t10_manifest.py — final census materializer.
# Normal mode: (1) fail-stop strict re-validation of every package .json/.jsonl;
# (2) artifact_index.csv (dynamic census of every file existing at index-write time
# except artifact_index.csv itself; its own sha is NOT written into the index - the
# scope is stated in the scope_note column of every row); (3) this attempt's capture
# (manifest identity null+UNKNOWN - it does not exist yet, disclosed); (4) the FINAL
# ledger append (the ledger physically closes here); (5) MANIFEST_SHA256.csv written
# as the ABSOLUTE LAST package file from the final census minus itself (full bijection,
# zero exclusions, zero sampling). The manifest's own SIZE/SHA are printed to the
# console (reported OUTSIDE the package) and never written into the package.
# --verify-only mode: read-only full re-hash/bijection verification; writes NOTHING.
import sys, os, csv, io, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t10_manifest.py"

def walk_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            ap = os.path.join(dirpath, fn)
            rel = os.path.relpath(ap, root).replace("\\", "/")
            out.append(rel)
    return sorted(out)

def strict_validate_all(root):
    rows = []
    ok = True
    for rel in walk_files(root):
        if rel.endswith(".json"):
            try:
                with open(rc.resolve_in_root(root, rel), "r", encoding="utf-8") as f:
                    rc.strict_loads(f.read())
                rows.append({"path": rel, "format": "json", "parse": "PASS"})
            except BaseException as e:
                ok = False
                rows.append({"path": rel, "format": "json", "parse": "FAIL", "error": str(e)})
        elif rel.endswith(".jsonl"):
            try:
                with open(rc.resolve_in_root(root, rel), "r", encoding="utf-8") as f:
                    n = 0
                    for line in f:
                        if line.strip():
                            rc.strict_loads(line)
                            n += 1
                rows.append({"path": rel, "format": "jsonl", "parse": "PASS", "lines": n})
            except BaseException as e:
                ok = False
                rows.append({"path": rel, "format": "jsonl", "parse": "FAIL", "error": str(e)})
    return ok, rows

def census(root, exclude):
    files = walk_files(root)
    rows = []
    for rel in files:
        if rel in exclude:
            continue
        ap = rc.resolve_in_root(root, rel)
        rows.append({"relative_path": rel, "size_bytes": os.path.getsize(ap),
                     "sha256": rc.sha256_file(ap)})
    return rows

def verify_only(cfg, root):
    mabs = rc.resolve_in_root(root, "MANIFEST_SHA256.csv")
    if not os.path.isfile(mabs):
        print(rc.compact_dumps({"mode": "verify-only", "error": "MANIFEST_SHA256.csv absent"}))
        return 1
    with open(mabs, "r", encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f)
        mrows = list(rd)
    mpaths = set(r["relative_path"] for r in mrows)
    disk = set(walk_files(root))
    disk_minus_manifest = disk - {"MANIFEST_SHA256.csv"}
    bijection_ok = (mpaths == disk_minus_manifest)
    diffs = {"missing_from_manifest": sorted(disk_minus_manifest - mpaths),
             "extra_in_manifest": sorted(mpaths - disk_minus_manifest)}
    errors = []
    for r in mrows:
        ap = rc.resolve_in_root(root, r["relative_path"])
        if not os.path.isfile(ap):
            errors.append({"path": r["relative_path"], "error": "absent"})
            continue
        if os.path.getsize(ap) != int(r["size_bytes"]):
            errors.append({"path": r["relative_path"], "error": "size mismatch"})
            continue
        if rc.sha256_file(ap) != r["sha256"]:
            errors.append({"path": r["relative_path"], "error": "sha mismatch"})
    ok = bijection_ok and not errors
    report = {"mode": "verify-only", "manifest_rows": len(mrows),
              "physical_files": len(disk), "bijection_ok": bijection_ok,
              "diffs": diffs if not bijection_ok else None,
              "rehash_errors": errors, "all_ok": ok,
              "manifest_identity": {"size_bytes": os.path.getsize(mabs), "sha256": rc.sha256_file(mabs)}}
    print(rc.compact_dumps(report))
    return 0 if ok else 1

def main():
    argv = list(sys.argv)
    if "--verify-only" in argv:
        cfg = rc.load_config(argv[argv.index("--verify-only") + 1] if len(argv) > argv.index("--verify-only") + 1 else argv[argv.index("--config") + 1])
        return verify_only(cfg, cfg["_output_root_abs"])
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
    try:
        rc.new_attempt_dir(root, attempt_id)
        # (1) fail-stop strict JSON validation of the complete package
        vok, vrows = strict_validate_all(root)
        if not vok:
            raise rc.CriticalMismatch("strict JSON validation failed before manifest")
        # (2) artifact_index.csv (census at index-write time, excluding itself)
        idx_rows = census(root, exclude={"artifact_index.csv"})
        scope_note = ("census at artifact_index write time; covers every file then existing EXCEPT "
                      "artifact_index.csv itself; its own sha256 is not written into the index; "
                      "MANIFEST_SHA256.csv (written afterwards) is the binding full bijection")
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["relative_path", "size_bytes", "sha256", "scope_note"])
        for r in idx_rows:
            w.writerow([r["relative_path"], r["size_bytes"], r["sha256"], scope_note])
        o_idx = rc.atomic_write_bytes(root, "artifact_index.csv", buf.getvalue().encode("utf-8"))
        outputs_meta.append(o_idx)
        # (3) this attempt's capture BEFORE the manifest (so the manifest covers it);
        #     manifest identity is null+UNKNOWN (it does not exist yet - disclosed)
        pre_result = {"artifact_index_rows": len(idx_rows),
                      "manifest_identity": {"size_bytes": None, "sha256": None,
                                            "status": "UNKNOWN_NOT_YET_WRITTEN_DISCLOSED"},
                      "validation_rows": len(vrows),
                      "note": "MANIFEST_SHA256.csv is written by THIS run as the ABSOLUTE LAST package file; its SIZE/SHA are reported in the terminal message only"}
        # (4) FINAL ledger append, then (5) the manifest from the final census
        stdout_pre = rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id,
                                       "pre_manifest": pre_result})
        entry = {"attempt_id": attempt_id, "tool": TOOL_REL,
                 "tool_sha256": rc.sha256_file(tool_abs),
                 "config": rc.file_identity(cfg["_config_abs"], "RUN_CONFIG.json"),
                 "argv": argv, "kind": "ARTIFACT_INDEX_AND_MANIFEST",
                 "t_start_utc": t_start, "t_end_utc": rc.utcnow_iso(),
                 "status": "PRE_MANIFEST_OK", "exit_code": None,
                 "inputs": inputs_meta, "outputs": outputs_meta,
                 "result": pre_result}
        prefix = rc.ledger_prefix_state(root)
        entry["ledger_prefix"] = prefix
        outs = rc.capture_attempt(root, attempt_id, entry, stdout_pre, "")
        rc.ledger_append(root, entry)
        # (5) manifest: final census minus itself
        m_rows = census(root, exclude={"MANIFEST_SHA256.csv"})
        mbuf = io.StringIO()
        mw = csv.writer(mbuf, lineterminator="\n")
        mw.writerow(["relative_path", "size_bytes", "sha256"])
        for r in m_rows:
            mw.writerow([r["relative_path"], r["size_bytes"], r["sha256"]])
        mabs = rc.resolve_in_root(root, "MANIFEST_SHA256.csv")
        fd = os.open(mabs, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, mbuf.getvalue().encode("utf-8"))
        finally:
            os.close(fd)
        m_ident = {"size_bytes": os.path.getsize(mabs), "sha256": rc.sha256_file(mabs)}
        result = {"artifact_index_rows": len(idx_rows), "manifest_rows": len(m_rows),
                  "manifest_identity": m_ident,
                  "note": "manifest covers every physical file except itself; zero exclusions, zero sampling; manifest is the LAST package write"}
        status = "OK"
        exit_code = 0
        t_end = rc.utcnow_iso()
    except SystemExit as e:
        raise e
    except rc.CriticalMismatch as e:
        status = "CRITICAL_MISMATCH"
        exit_code = 2
        err = "CriticalMismatch: %s" % e
        result = {"error": err, "status": status}
        t_end = rc.utcnow_iso()
    except BaseException as e:
        status = "FAILED"
        exit_code = 1
        err = "%s: %s" % (type(e).__name__, e)
        result = {"error": err, "traceback": traceback.format_exc()}
        t_end = rc.utcnow_iso()
    print(rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id, "status": status,
                            "exit": exit_code, "result": result}))
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
