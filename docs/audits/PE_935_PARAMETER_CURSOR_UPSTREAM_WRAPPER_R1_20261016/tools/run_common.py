# run_common.py — shared helpers for RUN PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016
# Every tool receives --config <abs path to RUN_CONFIG.json>. The config file must
# physically reside in the OUTPUT_ROOT it declares (verified). OUTPUT_ROOT is NEVER
# built from cwd, the contract directory or Path(__file__).parent. All writes resolve
# under OUTPUT_ROOT; paths outside are refused. Existing files are refused
# (O_CREAT|O_EXCL atomic create). The only appendable file is ATTEMPT_LOG.jsonl,
# with prefix size+sha256 measured BEFORE each append and recorded in the appended
# line itself (entry.json and the ledger line carry identical content).
import sys, os, json, hashlib, datetime

class RefuseExisting(Exception): pass
class RefuseOutsideRoot(Exception): pass
class ConfigError(Exception): pass
class CriticalMismatch(Exception): pass

def utcnow_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds")

def _reject_constant(x):
    raise ValueError("JSON constant not allowed (NaN/Infinity rejected): %r" % (x,))

def _pairs_hook(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("duplicate key in JSON object: %r" % (k,))
        d[k] = v
    return d

def strict_loads(text):
    return json.loads(text, parse_constant=_reject_constant, object_pairs_hook=_pairs_hook)

def strict_dumps(obj):
    return json.dumps(obj, indent=2, ensure_ascii=True, allow_nan=False) + "\n"

def compact_dumps(obj):
    return json.dumps(obj, ensure_ascii=True, allow_nan=False, separators=(",", ":"))

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest().upper()

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest().upper()

def load_config(config_path):
    ap = os.path.abspath(config_path)
    with open(ap, "r", encoding="utf-8") as f:
        cfg = strict_loads(f.read())
    if "output_root" not in cfg:
        raise ConfigError("config has no output_root")
    root = os.path.abspath(cfg["output_root"])
    if os.path.dirname(ap).lower() != root.lower():
        raise ConfigError("config file must physically reside in the output_root it declares")
    cfg["_output_root_abs"] = root
    cfg["_config_abs"] = ap
    return cfg

def resolve_in_root(root, relpath):
    p = os.path.abspath(os.path.join(root, relpath))
    r = os.path.abspath(root)
    if not (p.lower() == r.lower() or p.lower().startswith(r.lower() + os.sep)):
        raise RefuseOutsideRoot("refusing path outside OUTPUT_ROOT: %r" % (relpath,))
    return p

def atomic_write_bytes(root, relpath, data):
    p = resolve_in_root(root, relpath)
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    rel_norm = relpath.replace("\\", "/")
    return {"path": rel_norm, "size_bytes": len(data), "sha256": sha256_bytes(data)}

def atomic_write_text(root, relpath, text):
    return atomic_write_bytes(root, relpath, text.encode("utf-8"))

def file_identity(abs_path, rel=None):
    return {"path": (rel if rel is not None else abs_path),
            "size_bytes": os.path.getsize(abs_path),
            "sha256": sha256_file(abs_path)}

def ledger_prefix_state(root):
    lp = resolve_in_root(root, "ATTEMPT_LOG.jsonl")
    if os.path.exists(lp):
        with open(lp, "rb") as f:
            prefix_bytes = f.read()
        return {"size_bytes": len(prefix_bytes),
                "sha256": sha256_bytes(prefix_bytes),
                "existed_before_append": True}
    return {"size_bytes": 0, "sha256": None,
            "existed_before_append": False,
            "note": "FIRST_APPEND_FILE_ABSENT"}

def ledger_append(root, entry):
    lp = resolve_in_root(root, "ATTEMPT_LOG.jsonl")
    line = compact_dumps(entry) + "\n"
    with open(lp, "ab") as f:
        f.write(line.encode("utf-8"))

def new_attempt_dir(root, attempt_id):
    adir = resolve_in_root(root, os.path.join("attempts", attempt_id))
    if os.path.isdir(adir):
        raise RefuseExisting("attempt dir already exists: %s" % attempt_id)
    os.makedirs(adir)
    return adir

def capture_attempt(root, attempt_id, entry_dict, stdout_text, stderr_text):
    # writes stdout.txt and stderr.txt first, then entry.json referencing them
    rel_stdout = ("attempts/%s/stdout.txt" % attempt_id)
    rel_stderr = ("attempts/%s/stderr.txt" % attempt_id)
    rel_entry = ("attempts/%s/entry.json" % attempt_id)
    o1 = atomic_write_text(root, rel_stdout, stdout_text)
    o2 = atomic_write_text(root, rel_stderr, stderr_text)
    entry_dict["capture_files"] = [o1, o2]
    o3 = atomic_write_text(root, rel_entry, strict_dumps(entry_dict))
    return [o1, o2, o3]

def finalize(root, attempt_id, entry_dict, stdout_text, stderr_text):
    # 1) measure ledger prefix BEFORE append; 2) embed in entry; 3) capture; 4) append.
    prefix = ledger_prefix_state(root)
    entry_dict["ledger_prefix"] = prefix
    outs = capture_attempt(root, attempt_id, entry_dict, stdout_text, stderr_text)
    ledger_append(root, entry_dict)
    return outs, prefix

def parse_simple_args(argv, required):
    out = {k: None for k in required}
    i = 1
    while i < len(argv):
        k = argv[i]
        if k in out and i + 1 < len(argv):
            out[k] = argv[i + 1]
            i += 2
        else:
            raise SystemExit("ARG_ERROR: unknown or incomplete argument %r (required: %s)" % (k, ", ".join(required)))
    for k, v in out.items():
        if v is None:
            raise SystemExit("ARG_ERROR: missing %s" % k)
    return out
