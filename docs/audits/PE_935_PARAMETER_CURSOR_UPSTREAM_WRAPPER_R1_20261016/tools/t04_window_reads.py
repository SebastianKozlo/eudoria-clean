# t04_window_reads.py — the two permitted original-code window reads (82 B each) at the
# mechanically derived file offset (from records/pe32_mapping.json; NO re-derivation, no
# third read on any harness failure, no prefix read, no read past RET, no neighbourhood
# scan). Saves both buffers separately BEFORE analysis and checks byte agreement.
import sys, os, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t04_window_reads.py"

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    tool_abs = os.path.abspath(__file__)
    exe_path = cfg["original_exe"]["path"]
    win_size = cfg["window"]["size_bytes"]
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        rc.new_attempt_dir(root, attempt_id)
        mapping_abs = rc.resolve_in_root(root, "records/pe32_mapping.json")
        with open(mapping_abs, "r", encoding="utf-8") as f:
            mapping = rc.strict_loads(f.read())
        inputs_meta.append(rc.file_identity(mapping_abs, "records/pe32_mapping.json"))
        file_offset = mapping["derived_file_offset_decimal"]
        b1 = None
        b2 = None
        with open(exe_path, "rb") as f:
            f.seek(file_offset)
            b1 = f.read(win_size)
        with open(exe_path, "rb") as f:
            f.seek(file_offset)
            b2 = f.read(win_size)
        inputs_meta.append({"path": exe_path,
                            "note": "two window reads of %d B at derived offset (read1+read2)" % win_size,
                            "size_bytes": len(b1) + len(b2),
                            "sha256": rc.sha256_bytes(b1 + b2)})
        if len(b1) != win_size or len(b2) != win_size:
            raise rc.CriticalMismatch("window read short: %d / %d" % (len(b1), len(b2)))
        agree = (b1 == b2)
        w1 = rc.atomic_write_bytes(root, "buffers/window_science_read1.bin", b1)
        w2 = rc.atomic_write_bytes(root, "buffers/window_science_read2.bin", b2)
        outputs_meta.extend([w1, w2])
        if not agree:
            raise rc.CriticalMismatch("the two 82-B window reads DISAGREE byte-wise")
        result = {"file_offset": "0x%08X" % file_offset, "window_size": win_size,
                  "read1_size": len(b1), "read2_size": len(b2),
                  "read1_sha256": w1["sha256"], "read2_sha256": w2["sha256"],
                  "buffers_byte_identical": agree, "status": "OK",
                  "outputs": [w1["path"], w2["path"]]}
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
             "argv": argv, "kind": "ORIGINAL_CODE_WINDOW_READS",
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
