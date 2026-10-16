# t06_path_b.py — PATH_B sweep: imports the pinned x86dec_pinned.py BY EXPLICIT PATH
# (read-only import; no main; sys.dont_write_bytecode + python -B => no .pyc), then
# performs a SEQUENTIAL decode of the saved 82-B buffer from window entry offset 0.
# PATH_B is never fed PATH_A heads. All library fields are recorded verbatim
# (explicit nulls where the library records none); a decode()==None barrier STOPS
# the sweep (no resync). Writes decode/PATH_B_SWEEP.json.
import sys, os, importlib.util, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t06_path_b.py"

def record_insn(ins, buf, win_start):
    raw = buf[ins.start:ins.start + ins.length]
    return {
        "offset_in_window": ins.start,
        "va": "0x%08X" % (win_start + ins.start),
        "length": ins.length,
        "raw_hex": " ".join("%02x" % b for b in raw),
        "opcode_hex": ("0x%02X" % ins.opcode) if ins.opcode is not None else None,
        "opcode2_hex": ("0x%02X" % ins.opcode2) if ins.opcode2 is not None else None,
        "prefixes_hex": ["0x%02X" % p for p in ins.prefixes],
        "has66": ins.has66, "has67": ins.has67, "segment": ins.segment,
        "mod": ins.mod, "reg": ins.reg, "rm": ins.rm,
        "memop": ins.memop, "ea_text": ins.ea_text(),
        "disp_width": ins.disp_width,
        "disp_raw": ins.disp_raw,
        "disp_signed": ins.disp_signed,
        "imm_width": ins.imm_width, "imm_raw": ins.imm_raw, "imm_signed": ins.imm_signed,
        "rel16": ins.rel16
    }

def main():
    argv = list(sys.argv)
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
        lib_path = cfg["decoders"]["path_b"]["path"]
        lib_ident = rc.file_identity(lib_path)
        if lib_ident["size_bytes"] != cfg["decoders"]["path_b"]["size_bytes"] or \
           lib_ident["sha256"] != cfg["decoders"]["path_b"]["sha256"]:
            raise rc.CriticalMismatch("pinned PATH_B library identity mismatch before import")
        spec = importlib.util.spec_from_file_location("x86dec_pinned", lib_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        buf_abs = rc.resolve_in_root(root, "buffers/window_science_read1.bin")
        with open(buf_abs, "rb") as f:
            buf = f.read()
        inputs_meta.append(rc.file_identity(buf_abs, "buffers/window_science_read1.bin"))
        inputs_meta.append(lib_ident)
        win_start = int(cfg["window"]["start_va"], 16)
        rows = []
        applications = 0
        barrier = None
        i = 0
        n = len(buf)
        while i < n:
            ins = mod.decode(buf, i)
            applications += 1
            if ins is None:
                barrier = {"offset_in_window": i, "reason": "DECODE_RETURNED_NONE"}
                break
            rows.append(record_insn(ins, buf, win_start))
            i += ins.length
        reached_end = (barrier is None and i == n)
        out_obj = {
            "generated_by_tool": "t06_path_b.py",
            "source_buffer": "buffers/window_science_read1.bin",
            "library": {"path": lib_path, "size_bytes": lib_ident["size_bytes"],
                        "sha256": lib_ident["sha256"]},
            "sweep_mode": "sequential from window entry offset 0; never fed PATH_A heads",
            "decode_applications": applications,
            "instructions": rows,
            "barrier": barrier,
            "reached_window_end_exactly": reached_end,
            "window_size_bytes": n
        }
        out_obj["generated_utc"] = rc.utcnow_iso()
        o = rc.atomic_write_bytes(root, "decode/PATH_B_SWEEP.json", rc.strict_dumps(out_obj).encode("utf-8"))
        outputs_meta.append(o)
        result = {"decode_applications": applications, "instructions": len(rows),
                  "barrier": barrier, "reached_window_end_exactly": reached_end,
                  "output": o["path"], "output_sha256": o["sha256"], "status": "OK"}
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
             "argv": argv, "kind": "PATH_B_SEQUENTIAL_SWEEP",
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
