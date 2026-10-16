# t00_write_doc.py — immutable document materializer.
# Moves the authored payload from <root>/_incoming/ into attempts/<NNNN>/payload_input.<ext>
# and materializes the final document under OUTPUT_ROOT with a serializer-measured
# generated_utc (json: injected field; text: {{GENERATED_UTC}} token replacement).
# Refuses an existing target file. Appends one ATTEMPT_LOG.jsonl line.
import sys, os, json, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t00_write_doc.py"

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt", "--kind", "--payload", "--target"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    kind = a["--kind"]
    payload_rel = a["--payload"].replace("\\", "/")
    target_rel = a["--target"].replace("\\", "/")
    tool_abs = os.path.abspath(__file__)
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        if kind not in ("json", "text"):
            raise ValueError("kind must be json or text")
        target_abs = rc.resolve_in_root(root, target_rel)
        if os.path.exists(target_abs):
            raise rc.RefuseExisting("target exists, refusing (immutable first-write only): %s" % target_rel)
        payload_abs = rc.resolve_in_root(root, payload_rel)
        if not os.path.isfile(payload_abs):
            raise rc.RefuseExisting("payload not found: %s" % payload_rel)
        with open(payload_abs, "rb") as f:
            payload_bytes = f.read()
        payload_ident = {"path": payload_rel, "size_bytes": len(payload_bytes),
                         "sha256": rc.sha256_bytes(payload_bytes)}
        rc.new_attempt_dir(root, attempt_id)
        ext = os.path.splitext(payload_rel)[1] or ".bin"
        payload_input_abs = rc.resolve_in_root(root, "attempts/%s/payload_input%s" % (attempt_id, ext))
        os.rename(payload_abs, payload_input_abs)
        inputs_meta.append(payload_ident)
        # prepare content first, then measure time at the moment of writing the prepared content
        if kind == "json":
            obj = rc.strict_loads(payload_bytes.decode("utf-8"))
            prepared = json.dumps(obj, indent=2, ensure_ascii=True, allow_nan=False)
        else:
            prepared = payload_bytes.decode("utf-8")
        generated_utc = rc.utcnow_iso()
        if kind == "json":
            obj["generated_utc"] = generated_utc
            obj["generated_by_tool"] = "t00_write_doc.py"
            obj["payload_sha256"] = payload_ident["sha256"]
            doc_bytes = rc.strict_dumps(obj).encode("utf-8")
        else:
            doc_text = prepared.replace("{{GENERATED_UTC}}", generated_utc)
            doc_bytes = doc_text.encode("utf-8")
        w = rc.atomic_write_bytes(root, target_rel, doc_bytes)
        outputs_meta.append(w)
        t_end = rc.utcnow_iso()
        result = {"target": w["path"], "size_bytes": w["size_bytes"], "sha256": w["sha256"],
                  "generated_utc": generated_utc, "kind": kind,
                  "payload_sha256": payload_ident["sha256"],
                  "token_replaced": ("{{GENERATED_UTC}}" in prepared) if kind == "text" else None}
        status = "OK"
        exit_code = 0
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
             "argv": argv, "kind": "DOC_MATERIALIZATION",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status == "OK" else err)
    print(rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id, "status": status,
                            "exit": exit_code, "result": result,
                            "ledger_prefix": prefix}))
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
