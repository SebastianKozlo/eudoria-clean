#!/usr/bin/env python3
"""live_test.py — NIGHT ORDER #2 item #2: the LIVE test WITHOUT the debugger.
A plain spawn of the sandbox Entropia.exe (working dir = wd) + the REAL
liveness monitoring for >=300s: Get-Process + the threads + the CPU cycles
cyclically (NEVER a spin/timeout on a PID — the F-B4 lesson). The record:
every sample; the outcome; if dead -> the exit code + the diagnosis; if alive
-> the kill + the death proof + the orphan census."""
import ctypes
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

import importlib.util
ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139"
spec = importlib.util.spec_from_file_location("h", os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

WD = os.path.join(ROOT, "04_RUNTIME", "sandbox", "wd")
TARGET = os.path.join(WD, "Entropia.exe")
OUTDIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test"
os.makedirs(OUTDIR, exist_ok=True)


def ts():
    return datetime.now(timezone.utc).isoformat()


def main():
    # the fail-closed pre-flight (the standing discipline)
    import subprocess as sp
    r = sp.run([sys.executable, os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py")],
               capture_output=True, text=True)
    pre = json.loads(r.stdout)
    record = {"run_id": "PE_M1_X87CW_AUTOMATION_R1_20260905_140126",
              "item": "#2 LIVE TEST (no debugger)", "started_at": ts(),
              "preflight_verify": pre}
    if r.returncode != 0:
        record["verdict"] = "ABORT_PREFLIGHT"
        json.dump(record, open(os.path.join(OUTDIR, "live_test_record.json"), "w"), indent=2)
        print(json.dumps({"verdict": "ABORT_PREFLIGHT", "pre": pre}))
        sys.exit(2)

    # the plain spawn (NO debugger flags)
    t0 = time.monotonic()
    proc = subprocess.Popen([TARGET], cwd=WD)
    pid = proc.pid
    record["pid"] = pid
    samples = []
    dead_at = None
    while time.monotonic() - t0 < 300:
        time.sleep(10)
        el = round(time.monotonic() - t0, 1)
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 f"$p = Get-Process -Id {pid} -ErrorAction Stop; "
                 f"\"threads=$($p.Threads.Count) cpu=$([math]::Round($p.TotalProcessorTime.TotalSeconds,2)) "
                 f"ws=$([math]::Round($p.WorkingSet64/1MB,1)) win=$($p.MainWindowTitle)\""],
                capture_output=True, text=True, timeout=15)
            if out.returncode == 0:
                samples.append({"t": el, "alive": True, "data": out.stdout.strip()})
            else:
                # the process is GONE: the independent proof via the Popen poll
                rc = proc.poll()
                dead_at = el
                samples.append({"t": el, "alive": False, "popen_rc": rc})
                break
        except Exception as e:
            samples.append({"t": el, "error": str(e)})
    alive_end = dead_at is None
    record["samples"] = samples
    if alive_end:
        # the kill + the death proof + the orphan census
        proc.kill()
        try:
            rc = proc.wait(timeout=10)
        except Exception:
            rc = None
        gone = subprocess.run(["powershell", "-NoProfile", "-Command",
                               f"try {{ Get-Process -Id {pid} -ErrorAction Stop | Out-Null; 'ALIVE' }} catch {{ 'GONE' }}"],
                              capture_output=True, text=True).stdout.strip()
        record["kill"] = {"returncode": rc, "os_proof": gone}
        # the orphan census (ClientLoader/CLDLLPatcher/CLUpdater + any children)
        census = subprocess.run(["powershell", "-NoProfile", "-Command",
                                 "Get-Process ClientLoader,CLDLLPatcher,CLUpdater,Entropia -ErrorAction SilentlyContinue | Select-Object Id,ProcessName | ConvertTo-Json -Compress"],
                                capture_output=True, text=True).stdout.strip()
        record["post_kill_process_census"] = census
        record["verdict"] = "LIVE_300S" if len(samples) >= 25 else "LIVE_PARTIAL"
    else:
        record["verdict"] = f"DEAD_AT_{dead_at}s"
    record["finished_at"] = ts()
    json.dump(record, open(os.path.join(OUTDIR, "live_test_record.json"), "w"), indent=2)
    print(json.dumps({"verdict": record["verdict"], "pid": pid,
                      "samples": len(samples),
                      "last": samples[-1] if samples else None}))
    sys.exit(0 if alive_end else 1)


if __name__ == "__main__":
    main()
