# t02_hash_exe.py — streaming full SHA256 pass over the pinned original Entropia.exe.
# Counts bytes read; verifies pinned SIZE and SHA256 from RUN_CONFIG. No file copy;
# no content retained (hash only). Result recorded in the attempt entry + ledger.
import sys, os, hashlib, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t02_hash_exe.py"

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt", "--pass-index"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    pass_index = int(a["--pass-index"])
    tool_abs = os.path.abspath(__file__)
    exe_rel_cfg = cfg["original_exe"]["path"]
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        rc.new_attempt_dir(root, attempt_id)
        h = hashlib.sha256()
        bytes_read = 0
        with open(exe_rel_cfg, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
                bytes_read += len(b)
        sha = h.hexdigest().upper()
        size_expected = cfg["original_exe"]["size_bytes"]
        sha_expected = cfg["original_exe"]["sha256"]
        size_ok = (bytes_read == size_expected)
        sha_ok = (sha == sha_expected)
        status = "OK" if (size_ok and sha_ok) else "CRITICAL_MISMATCH"
        exit_code = 0 if (size_ok and sha_ok) else 2
        result = {"pass_index": pass_index, "bytes_read": bytes_read,
                  "size_expected": size_expected, "size_matches_pin": size_ok,
                  "sha256": sha, "sha_expected": sha_expected, "sha_matches_pin": sha_ok,
                  "status": status, "streaming": True, "content_retained": False}
        inputs_meta.append(rc.file_identity(exe_rel_cfg))
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
             "argv": argv, "kind": "ORIGINAL_EXE_FULL_HASH_PASS",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status != "FAILED" else err)
    print(stdout_text)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
