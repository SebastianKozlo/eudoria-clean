# t05_path_a.py — PATH_A full sweep: GNU objdump 2.44 (WSL /usr/bin/objdump) over the
# SAVED buffer buffers/window_science_read1.bin, accessed via /mnt/d passthrough
# (NO copy into WSL /tmp or home). Counts as one PATH_A full sweep. Captures the real
# argv, version, exit code; writes decode/PATH_A_SWEEP.txt.
import sys, os, subprocess, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t05_path_a.py"

def wsl_mount_path(root_abs, win_path):
    # D:\foo\bar -> /mnt/d/foo/bar
    p = os.path.abspath(win_path)
    drive = p[0]
    rest = p[2:].replace("\\", "/")
    return "/mnt/%s%s" % (drive.lower(), rest)

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
        buf_abs = rc.resolve_in_root(root, "buffers/window_science_read1.bin")
        with open(buf_abs, "rb") as f:
            buf = f.read()
        inputs_meta.append(rc.file_identity(buf_abs, "buffers/window_science_read1.bin"))
        mount = wsl_mount_path(root, buf_abs)
        adjust = cfg["window"]["start_va"]
        od_argv = ["wsl", "-e", "/usr/bin/objdump", "-D", "-b", "binary", "-m", "i386",
                   "-M", "intel", "--adjust-vma=%s" % adjust, mount]
        ver_argv = ["wsl", "-e", "/usr/bin/objdump", "--version"]
        ver = subprocess.run(ver_argv, capture_output=True)
        version_first = ver.stdout.decode("utf-8", "replace").splitlines()[0] if ver.stdout else ""
        pr = subprocess.run(od_argv, capture_output=True)
        od_exit = pr.returncode
        od_stdout = pr.stdout.decode("utf-8", "replace")
        od_stderr = pr.stderr.decode("utf-8", "replace")
        if od_exit != 0:
            raise rc.CriticalMismatch("objdump sweep exit=%d stderr=%r" % (od_exit, od_stderr[:500]))
        sweep = rc.atomic_write_bytes(root, "decode/PATH_A_SWEEP.txt",
                                      pr.stdout)  # raw objdump bytes as emitted
        outputs_meta.append(sweep)
        result = {"argv": od_argv, "version": version_first,
                  "objdump_exit": od_exit,
                  "sweeps_used": 1, "sweeps_limit": cfg["budgets"]["MAX_PATH_A_FULL_SWEEPS"],
                  "output_size_bytes": sweep["size_bytes"], "output_sha256": sweep["sha256"],
                  "stderr_len": len(pr.stderr),
                  "mount_path": mount, "status": "OK"}
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
             "argv": argv, "kind": "PATH_A_FULL_SWEEP",
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
