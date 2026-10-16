# t09_close.py — post-science closure verification:
# (1) the second full streaming EXE hash (pass 2/2), compared to pass 1 (from
#     SOURCE_READS.json) and to the pin;
# (2) re-hash of the contract + INPUT_PINS + all 12 pinned input copies;
# (3) strict parse of every package .json/.jsonl (duplicate keys, NaN, Infinity
#     rejected);
# (4) machine check of the typed standing block (contract section 11 ini block
#     vs EVIDENCE.json typed_final_status_block).
# Writes records/SOURCE_UNCHANGED.json, records/JSON_VALIDATION.json,
# records/STANDING_CHECK.json. Critical EXE identity mismatch halts (exit 2).
import sys, os, hashlib, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t09_close.py"

def parse_standing_block(contract_text):
    idx = contract_text.find("Nowy typed standing:")
    if idx < 0:
        raise rc.CriticalMismatch("contract standing block marker not found")
    i2 = contract_text.find("```ini", idx)
    i3 = contract_text.find("```", i2 + 6)
    if i2 < 0 or i3 < 0:
        raise rc.CriticalMismatch("contract standing block fences not found")
    block = contract_text[i2 + 6:i3]
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    tool_abs = os.path.abspath(__file__)
    exe_path = cfg["original_exe"]["path"]
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        rc.new_attempt_dir(root, attempt_id)
        # (1) second full EXE hash
        h = hashlib.sha256()
        bytes_read = 0
        with open(exe_path, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
                bytes_read += len(b)
        pass2_sha = h.hexdigest().upper()
        sr_abs = rc.resolve_in_root(root, "SOURCE_READS.json")
        with open(sr_abs, "r", encoding="utf-8") as f:
            sr = rc.strict_loads(f.read())
        pass1_sha = None
        for ev in sr["reads"]:
            if ev.get("kind") == "FULL_EXE_SHA256_STREAMING_PASS" and ev.get("pass_index") == 1:
                pass1_sha = ev["sha256"]
        pin_sha = cfg["original_exe"]["sha256"]
        exe_ok = (pass2_sha == pin_sha and pass1_sha == pass2_sha and bytes_read == cfg["original_exe"]["size_bytes"])
        if not exe_ok:
            raise rc.CriticalMismatch("EXE identity mismatch at close: pass2=%s pass1=%s pin=%s" % (pass2_sha, pass1_sha, pin_sha))
        # (2) re-hash inputs + pins + contract
        rehash = []
        rehash_ok = True
        for label, path in (("CONTRACT", cfg["contract"]["path"]), ("INPUT_PINS", cfg["input_pins"]["path"])):
            ident = rc.file_identity(path)
            ok = (ident["size_bytes"] == (cfg["contract"]["size_bytes"] if label == "CONTRACT" else cfg["input_pins"]["size_bytes"]) and
                  ident["sha256"] == (cfg["contract"]["sha256"] if label == "CONTRACT" else cfg["input_pins"]["sha256"]))
            rehash.append({"label": label, "path": path, "size_bytes": ident["size_bytes"], "sha256": ident["sha256"], "matches_pin": ok})
            rehash_ok = rehash_ok and ok
        with open(cfg["input_pins"]["path"], "r", encoding="utf-8") as f:
            pins = rc.strict_loads(f.read())
        for fe in pins["files"]:
            ap = os.path.join(cfg["authoring_root"], fe["relative_path"])
            ident = rc.file_identity(ap, fe["relative_path"])
            ok = (ident["size_bytes"] == fe["size_bytes"] and ident["sha256"] == fe["sha256"])
            rehash.append({"label": "INPUT", "path": fe["relative_path"], "size_bytes": ident["size_bytes"], "sha256": ident["sha256"], "matches_pin": ok})
            rehash_ok = rehash_ok and ok
        if len(pins["files"]) != cfg["input_pins"]["mandatory_input_count"]:
            raise rc.CriticalMismatch("input pins count mismatch")
        # (3) strict parse of all package .json/.jsonl present at this moment
        validation_rows = []
        validation_ok = True
        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                ap = os.path.join(dirpath, fn)
                rel = os.path.relpath(ap, root).replace("\\", "/")
                if fn.endswith(".json"):
                    try:
                        with open(ap, "r", encoding="utf-8") as f:
                            rc.strict_loads(f.read())
                        validation_rows.append({"path": rel, "format": "json", "parse": "PASS"})
                    except BaseException as e:
                        validation_ok = False
                        validation_rows.append({"path": rel, "format": "json", "parse": "FAIL", "error": "%s: %s" % (type(e).__name__, e)})
                elif fn.endswith(".jsonl"):
                    try:
                        with open(ap, "r", encoding="utf-8") as f:
                            nlines = 0
                            for line in f:
                                if line.strip():
                                    rc.strict_loads(line)
                                    nlines += 1
                        validation_rows.append({"path": rel, "format": "jsonl", "parse": "PASS", "lines": nlines})
                    except BaseException as e:
                        validation_ok = False
                        validation_rows.append({"path": rel, "format": "jsonl", "parse": "FAIL", "error": "%s: %s" % (type(e).__name__, e)})
        if not validation_ok:
            raise rc.CriticalMismatch("package JSON validation failed at close (see JSON_VALIDATION.json rows)")
        # (4) standing check vs the contract ini block
        with open(cfg["contract"]["path"], "r", encoding="utf-8") as f:
            contract_text = f.read()
        cblock = parse_standing_block(contract_text)
        ev_abs = rc.resolve_in_root(root, "EVIDENCE.json")
        with open(ev_abs, "r", encoding="utf-8") as f:
            ev = rc.strict_loads(f.read())
        eblock = ev["typed_final_status_block"]
        keys_c = sorted(cblock.keys())
        keys_e = sorted(eblock.keys())
        exact = (keys_c == keys_e and all(cblock[k] == eblock[k] for k in keys_c))
        if not exact:
            raise rc.CriticalMismatch("standing block does not match the contract section 11 block")
        # write the three records
        su = {"generated_by_tool": "t09_close.py",
              "exe": {"pass2_sha256": pass2_sha, "pass1_sha256": pass1_sha, "pin_sha256": pin_sha,
                      "pass2_bytes_read": bytes_read, "identity_matches_pin": exe_ok,
                      "pass1_equals_pass2": (pass1_sha == pass2_sha)},
              "inputs_rehash": rehash, "inputs_rehash_all_match": rehash_ok,
              "status": "OK"}
        su["generated_utc"] = rc.utcnow_iso()
        o1 = rc.atomic_write_bytes(root, "records/SOURCE_UNCHANGED.json", rc.strict_dumps(su).encode("utf-8"))
        jv = {"generated_by_tool": "t09_close.py",
              "validated_at_this_stage": validation_rows,
              "note": "every package .json/.jsonl present at t09 time; strict parse rejects duplicate keys and NaN/Infinity; t10 re-validates the complete set (including files written after this stage) before writing the manifest",
              "all_pass": validation_ok, "status": "OK" if validation_ok else "FAIL"}
        jv["generated_utc"] = rc.utcnow_iso()
        o2 = rc.atomic_write_bytes(root, "records/JSON_VALIDATION.json", rc.strict_dumps(jv).encode("utf-8"))
        sc = {"generated_by_tool": "t09_close.py",
              "contract_block_keys": len(cblock), "evidence_block_keys": len(eblock),
              "exact_match": exact,
              "contract_block": cblock,
              "source": "OPENCODE_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1.md section 'Nowy typed standing:' ini block, parsed and compared key-by-key against EVIDENCE.json typed_final_status_block",
              "status": "OK" if exact else "FAIL"}
        sc["generated_utc"] = rc.utcnow_iso()
        o3 = rc.atomic_write_bytes(root, "records/STANDING_CHECK.json", rc.strict_dumps(sc).encode("utf-8"))
        outputs_meta.extend([o1, o2, o3])
        result = {"exe_identity": su["exe"], "inputs_rehash_all_match": rehash_ok,
                  "json_validation_all_pass": validation_ok,
                  "json_files_validated": len(validation_rows),
                  "standing_exact_match": exact, "standing_keys": len(cblock),
                  "outputs": [o1["path"], o2["path"], o3["path"]], "status": "OK"}
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
    stdout_text = rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id, "status": status,
                                   "exit": exit_code, "result": result})
    entry = {"attempt_id": attempt_id, "tool": TOOL_REL,
             "tool_sha256": rc.sha256_file(tool_abs),
             "config": rc.file_identity(cfg["_config_abs"], "RUN_CONFIG.json"),
             "argv": argv, "kind": "CLOSE_VERIFICATION",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status == "OK" else err)
    print(stdout_text)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
