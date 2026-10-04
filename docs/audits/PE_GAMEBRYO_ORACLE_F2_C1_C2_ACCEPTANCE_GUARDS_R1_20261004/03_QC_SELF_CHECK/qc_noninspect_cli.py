#!/usr/bin/env python3
# qc_noninspect_cli.py -- non-inspect CLI semantics preservation QC for
# PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004.
#
# probe-version / compare / capabilities exit semantics and behavior must
# be UNCHANGED by the F2-C1/C2 correction (F3 stays OPEN; compare is NOT
# fixed here). Evidence: byte-identical stdout, byte-identical stderr and
# identical exit codes for the same command pair executed against
#   PRE  = the pristine d497b44d tool bytes (extracted via
#          `git cat-file -p d497b44d:<path>`, byte-faithful; SHA256
#          recorded below by the runner) and
#   POST = the corrected worktree tool bytes.
#
# Command set (mirrors the F2 QC pair set):
#   probe-version fx_VALID
#   capabilities            (all adapters)
#   capabilities --adapter gb12
#   compare fx_VALID --our-parser qc_our.json --oracle-result
#       <pinned historical PRE_FIX_oracle_result_fx_VALID.json>
#   compare fx_VALID --our-parser qc_our.json     (internal inspect pair)
#
# Usage:
#   python qc_noninspect_cli.py <prebase_tools_root> <repo_tools_root>
#       <fixtures_dir> <our_parser_json> <pinned_oracle_result_json>
#       <outdir>
#
# The our-parser JSON is hand-built OUR data (qc_compare_inputs.py
# pattern); the pinned oracle result is the F2 package's published
# PRE_FIX_oracle_result_fx_VALID.json (read-only historical input).

import hashlib
import json
import os
import subprocess
import sys

CMDS = [
    ("probe_version_fx_VALID", ["probe-version", "<NIF>"]),
    ("capabilities_all", ["capabilities"]),
    ("capabilities_gb12", ["capabilities", "--adapter", "gb12"]),
    ("compare_pinned",
     ["compare", "<NIF>", "--our-parser", "<OUR>",
      "--oracle-result", "<PINNED>"]),
    ("compare_internal_inspect", ["compare", "<NIF>", "--our-parser",
                                  "<OUR>"]),
]


def run(tree, argv):
    oracle = os.path.join(tree, "tools", "gamebryo_oracle", "oracle.py")
    proc = subprocess.run([sys.executable, oracle] + argv,
                          capture_output=True)
    return (proc.stdout, proc.stderr, proc.returncode,
            hashlib.sha256(open(oracle, "rb").read()).hexdigest().upper())


def main():
    (pre_tree, post_tree, fixtures, our_json, pinned, outdir) = sys.argv[1:7]
    nif = os.path.join(fixtures, "fx_VALID_user_version_0_root_0.nif")
    os.makedirs(outdir, exist_ok=True)
    failures = []

    def check(name, cond, detail=""):
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
        if not cond:
            failures.append(name)

    with open(nif, "rb") as fh:
        nif_sha = hashlib.sha256(fh.read()).hexdigest().upper()
    check("qc_input_valid_fixture_pinned",
          nif_sha.startswith("48B24BB5100F424ABB266A8D10BB1F6C57A854C1"),
          "fx_VALID sha256=%s" % nif_sha)

    for label, tmpl in CMDS:
        argv = []
        for tok in tmpl:
            argv.append({"<NIF>": nif, "<OUR>": our_json,
                         "<PINNED>": pinned}.get(tok, tok))
        po, pe, pr, psha = run(pre_tree, argv)
        qo, qe, qr, qsha = run(post_tree, argv)
        # raw record (deterministic; no wall-clock)
        rec = {
            "command": "python tools/gamebryo_oracle/oracle.py " +
                       " ".join(tmpl),
            "argv": argv,
            "pre": {"stdout_bytes": po.decode("utf-8", "replace"),
                    "stderr_bytes": pe.decode("utf-8", "replace"),
                    "exit_code": pr,
                    "oracle_py_sha256": psha},
            "post": {"stdout_bytes": qo.decode("utf-8", "replace"),
                     "stderr_bytes": qe.decode("utf-8", "replace"),
                     "exit_code": qr,
                     "oracle_py_sha256": qsha},
            "byte_identical": {
                "stdout": po == qo, "stderr": pe == qe,
                "exit_code": pr == qr},
        }
        with open(os.path.join(outdir, "%s.json" % label), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(rec, fh, indent=1, sort_keys=False, ensure_ascii=True)
            fh.write("\n")
        check("qc_%s_byte_identical_pre_post" % label,
              po == qo and pe == qe and pr == qr,
              "stdout=%s stderr=%s exit=%s/%s"
              % (len(po) == len(qo), pe == qe, pr, qr))

    print("QC_NONINSPECT: %d failures: %r" % (len(failures), failures))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
