#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""run_oracle_copy_r1.py — Run the gamebryo_oracle COPY (TOOLS/
gamebryo_oracle_r1; canonical tools/gamebryo_oracle READ_ONLY) against the
selected PE payloads (Work Package C, contract section 10).

Per payload (namespace separation per contract section 10):
  probe-version (gb12)  -> header + version/user-version gates
  inspect (gb12)        -> SOURCE_PREDICTED_ORIGINAL_VERDICT + RTTI table
                           validation (fail-closed: no object data past a
                           table miss in ordinary mode)
  inspect --full-decode  -> OUR_EXTENSION_CONTINUATION (continues past the
                           RTTI gate with closure-derived boundaries for
                           unknown blocks; NEVER original behavior)

CLI invocation of the COPY (oracle.py), each run recorded with argv, exit
code, stdout/stderr, timeout. Output JSONs -> 02_PE/raw/. No canonical tool
is executed or modified.
"""
import hashlib
import json
import os
import subprocess
import sys

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
HERE = os.path.dirname(os.path.abspath(__file__))
COPY = os.path.join(HERE, "gamebryo_oracle_r1")
ORACLE = os.path.join(COPY, "oracle.py")
OUT_ROOT = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = os.path.join(OUT_ROOT, "02_PE")
RAW = os.path.join(PE_OUT, "raw")
LOCAL_ROOT = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PAYLOAD_DIR = os.path.join(LOCAL_ROOT, "02_PE_payloads")
SELECTED = ["218757.nif", "496633.nif", "512126.nif", "423020.nif"]
TIMEOUT_S = 300
PY = sys.executable


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def run_cli(args, out_json):
    cmd = [PY, "-B", ORACLE] + args + ["--out", out_json]
    rec = {"command": cmd, "cwd": COPY, "timeout_s": TIMEOUT_S}
    try:
        p = subprocess.run(cmd, cwd=COPY, capture_output=True,
                           timeout=TIMEOUT_S, check=False)
        rec["exit_code"] = p.returncode
        rec["timeout"] = False
        rec["stdout_tail"] = p.stdout.decode("utf-8", errors="replace")[-2000:]
        rec["stderr_tail"] = p.stderr.decode("utf-8", errors="replace")[-2000:]
    except subprocess.TimeoutExpired:
        rec["exit_code"] = None
        rec["timeout"] = True
    return rec


def main():
    os.makedirs(RAW, exist_ok=True)
    cases = []
    for name in SELECTED:
        p = os.path.join(PAYLOAD_DIR, name)
        base = name.rsplit(".", 1)[0]
        ident = {"path": p, "size_bytes": os.path.getsize(p),
                 "sha256": sha256_file(p)}
        recs = {"payload": name, "input_identity": ident}
        # probe-version
        outp = os.path.join(RAW, "PE_%s.probe.json" % base)
        recs["probe_version"] = run_cli(["probe-version", p, "--adapter", "gb12"], outp)
        recs["probe_version"]["out_path"] = outp
        # inspect (ordinary)
        outi = os.path.join(RAW, "PE_%s.inspect.json" % base)
        recs["inspect_ordinary"] = run_cli(["inspect", p, "--adapter", "gb12"], outi)
        recs["inspect_ordinary"]["out_path"] = outi
        # inspect --full-decode
        outf = os.path.join(RAW, "PE_%s.inspect_full.json" % base)
        recs["inspect_full_decode"] = run_cli(
            ["inspect", p, "--adapter", "gb12", "--full-decode"], outf)
        recs["inspect_full_decode"]["out_path"] = outf
        cases.append(recs)
    result = {
        "run_id": RUN_ID,
        "stage": "S15_oracle_copy_execution",
        "tool_identity": {
            "canonical": "tools/gamebryo_oracle (READ_ONLY; never executed by "
                         "this run)",
            "copy": "TOOLS/gamebryo_oracle_r1 (byte-identical per-file copies; "
                    "identity recorded in SELECTION_AND_EXTRACTION_PROVENANCE"
                    " chain and re-verified below)",
            "copy_files_sha256": {},
        },
        "invocations": cases,
        "namespaces": {
            "SOURCE_PREDICTED_ORIGINAL_VERDICT": "inspect (ordinary mode) "
                "load_result + rtti_table_validation fields",
            "OUR_PARSER_RESULT": "probe-version + ordinary inspect measured "
                "header/gate fields (the source-derived reimplementation's "
                "own measurements)",
            "OUR_EXTENSION_CONTINUATION": "inspect --full-decode outputs "
                "(continues past the RTTI gate; never stock acceptance)",
        },
    }
    # record copy identity (all copied files, sorted relative paths)
    ids = {}
    for root, _dirs, files in os.walk(COPY):
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, COPY)
            ids[rel] = sha256_file(fp)
    result["tool_identity"]["copy_files_sha256"] = ids
    out = os.path.join(PE_OUT, "ORACLE_RUN_PROVENANCE.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    for c in cases:
        print("%-16s probe_exit=%s inspect_exit=%s full_exit=%s" % (
            c["payload"],
            c["probe_version"].get("exit_code"),
            c["inspect_ordinary"].get("exit_code"),
            c["inspect_full_decode"].get("exit_code")))


if __name__ == "__main__":
    main()
