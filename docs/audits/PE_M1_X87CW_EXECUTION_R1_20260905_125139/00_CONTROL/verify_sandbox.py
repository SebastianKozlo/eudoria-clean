#!/usr/bin/env python3
"""verify_sandbox.py — the FAIL-CLOSED pre-launch sandbox verification for
PE_M1_X87CW_EXECUTION_R1_20260905_125139 (KROK A kit).
Run BEFORE any operator launch. Any mismatch => EXIT NON-ZERO + the abort record.
Per the design W3.1.4/W4.7: NO session proceeds on an unverified copy.
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139"
SB = os.path.join(RUN_ROOT, "04_RUNTIME", "sandbox")
ABORT_RECORD = os.path.join(RUN_ROOT, "01_RAW", "sandbox_verify_record.json")

ENTROPIA_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
ENTROPIA_SIZE = 8015872
X32DBG_SHA = "822028F0755DBA773E445EAF57FDB3DBA84C9550AC7BDAD2AFA449912B5FBA41"
REQUIRED_DLLS = ["binkw32.dll", "d3d8.dll", "dbghelp.dll", "dpvs.dll", "ijl15.dll",
                 "NxCooking.dll", "PhysXCore.dll", "PhysXLoader.dll",
                 "stlport.5.1.dll", "stlport_vc645.dll", "wmasf.dll", "wmvcore.dll"]
REQUIRED_EXES = ["ClientLoader.exe", "CLDLLPatcher.exe", "CLUpdater.exe", "PE.exe"]
REQUIRED_DATA_COUNT_MIN = 1818  # the source census


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    checks = []
    ok = True

    def check(name, cond, detail):
        nonlocal ok
        if not cond:
            ok = False
        checks.append({"check": name, "pass": bool(cond), "detail": detail})

    e = os.path.join(SB, "wd", "Entropia.exe")
    if os.path.isfile(e):
        h, s = sha256(e), os.path.getsize(e)
        check("entropia_sha", h == ENTROPIA_SHA, h)
        check("entropia_size", s == ENTROPIA_SIZE, str(s))
    else:
        check("entropia_exists", False, e)

    x = os.path.join(SB, "x32dbg", "x32", "x32dbg.exe")
    if os.path.isfile(x):
        check("x32dbg_sha", sha256(x) == X32DBG_SHA, sha256(x))
    else:
        check("x32dbg_exists", False, x)

    for dll in REQUIRED_DLLS:
        check(f"dll_{dll}", os.path.isfile(os.path.join(SB, "wd", dll)), dll)
    for exe in REQUIRED_EXES:
        check(f"exe_{exe}", os.path.isfile(os.path.join(SB, "wd", exe)), exe)

    data_dir = os.path.join(SB, "wd", "Data")
    if os.path.isdir(data_dir):
        n = sum(len(fs) for _, _, fs in os.walk(data_dir))
        check("data_file_count", n >= REQUIRED_DATA_COUNT_MIN, f"{n} files")
    else:
        check("data_exists", False, data_dir)

    record = {
        "run_id": "PE_M1_X87CW_EXECUTION_R1_20260905_125139",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASS" if ok else "ABORT",
        "abort_class": None if ok else "SANDBOX_HASH_MISMATCH (W4.7)",
        "instruction": "PASS => the operator MAY launch. ABORT => NO launch; re-copy + re-verify.",
        "checks": checks,
    }
    with open(ABORT_RECORD, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    print(json.dumps({"verdict": record["verdict"], "checks": len(checks),
                      "failed": [c["check"] for c in checks if not c["pass"]]}))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
