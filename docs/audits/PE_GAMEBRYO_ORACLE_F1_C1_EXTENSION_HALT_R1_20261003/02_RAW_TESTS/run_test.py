#!/usr/bin/env python3
# run_test.py -- raw test/QC record runner for
# PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003.
#
# Executes a recorded command against tools/gamebryo_oracle/oracle.py and
# writes a raw record: input identity, exact command line, stdout bytes,
# stderr bytes, exit code. Deterministic records; no wall-clock data enters
# the record payload (only the record filename carries the run label).
#
# Adapted from the committed runner of
# PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003 (same record schema).
#
# Usage:
#   python run_test.py <record_path_stem> <nif_path> [--full-decode]
#
# Writes <stem>.RECORD.json containing everything; the CLI JSON is kept as
# the stdout payload verbatim.

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ORACLE = os.path.join(REPO, "tools", "gamebryo_oracle", "oracle.py")


def main():
    stem = sys.argv[1]
    nif = os.path.abspath(sys.argv[2])
    full = "--full-decode" in sys.argv[3:]
    with open(nif, "rb") as fh:
        data = fh.read()
    cmd = [sys.executable, ORACLE, "inspect", nif]
    if full:
        cmd.append("--full-decode")
    proc = subprocess.run(cmd, capture_output=True)
    rec = {
        "record_schema": "gamebryo_oracle_f1c1_run/raw_record@1.0",
        "input_identity": {
            "path": nif,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest().upper(),
        },
        "command": " ".join(
            ["python", os.path.relpath(ORACLE, REPO).replace("\\", "/"),
             "inspect", os.path.relpath(nif, REPO).replace("\\", "/")]
            + (["--full-decode"] if full else [])),
        "command_argv": cmd,
        "stdout_bytes": proc.stdout.decode("utf-8", "replace"),
        "stderr_bytes": proc.stderr.decode("utf-8", "replace"),
        "exit_code": proc.returncode,
    }
    out = stem + ".RECORD.json"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, sort_keys=False, ensure_ascii=True)
        fh.write("\n")
    print("%s exit=%d" % (os.path.basename(out), proc.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
