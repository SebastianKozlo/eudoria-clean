#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_M1_AVCAPTURE_R1 (H6) — capture the REAL crash AV (the failing instruction).
THE LESSONS APPLIED:
- the loader-AV noise filter: capture ONLY the AVs whose EIP is in the Entropia image
  (0x400000..0xC00000) — the loader noise lives in KERNELBASE;
- the time window checked EVERY iteration (the H5 hang root cause: the check only ran
  when WaitForDebugEvent timed out — with the event storm it never fired);
- the AV-storm cap;
- on the capture: the full context + the raw stack (the exe-range candidates) + KILL.
"""
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import struct
import subprocess
import sys
import time

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139"
WD = os.path.join(ROOT, "04_RUNTIME", "sandbox", "wd")
TARGET = os.path.join(WD, "Entropia.exe")
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000"
OUT = os.path.join(RUN, "01_RAW", "AV_CAPTURE_R1.json")
ENT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
WINDOW = 90.0

k32 = ctypes.windll.kernel32


class FLOATING_SAVE_AREA(ctypes.Structure):
    _fields_ = [("ControlWord", wt.DWORD), ("StatusWord", wt.DWORD),
                ("TagWord", wt.DWORD), ("ErrorOffset", wt.DWORD),
                ("ErrorSelector", wt.DWORD), ("DataOffset", wt.DWORD),
                ("DataSelector", wt.DWORD), ("RegisterArea", ctypes.c_byte * 80),
                ("Cr0NpxState", wt.DWORD)]


class CONTEXT32(ctypes.Structure):
    _fields_ = [("ContextFlags", wt.DWORD),
                ("Dr0", wt.DWORD), ("Dr1", wt.DWORD), ("Dr2", wt.DWORD),
                ("Dr3", wt.DWORD), ("Dr6", wt.DWORD), ("Dr7", wt.DWORD),
                ("FloatSave", FLOATING_SAVE_AREA),
                ("SegGs", wt.DWORD), ("SegFs", wt.DWORD), ("SegEs", wt.DWORD),
                ("SegDs", wt.DWORD), ("Edi", wt.DWORD), ("Esi", wt.DWORD),
                ("Ebx", wt.DWORD), ("Edx", wt.DWORD), ("Ecx", wt.DWORD),
                ("Eax", wt.DWORD), ("Ebp", wt.DWORD), ("Eip", wt.DWORD),
                ("SegCs", wt.DWORD), ("EFlags", wt.DWORD), ("Esp", wt.DWORD),
                ("SegSs", wt.DWORD), ("ExtendedRegisters", ctypes.c_byte * 512)]


class STARTUPINFO(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("lpReserved", wt.LPSTR), ("lpDesktop", wt.LPSTR),
                ("lpTitle", wt.LPSTR), ("dwX", wt.DWORD), ("dwY", wt.DWORD),
                ("dwXSize", wt.DWORD), ("dwYSize", wt.DWORD), ("dwXCountChars", wt.DWORD),
                ("dwYCountChars", wt.DWORD), ("dwFillAttribute", wt.DWORD),
                ("dwFlags", wt.DWORD), ("wShowWindow", wt.WORD), ("cbReserved2", wt.WORD),
                ("lpReserved2", ctypes.c_void_p), ("hStdInput", wt.HANDLE),
                ("hStdOutput", wt.HANDLE), ("hStdError", wt.HANDLE)]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", wt.HANDLE), ("hThread", wt.HANDLE),
                ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD)]


class EXCEPTION_RECORD(ctypes.Structure):
    _fields_ = [("ExceptionCode", wt.DWORD), ("ExceptionFlags", wt.DWORD),
                ("ExceptionRecord", wt.DWORD), ("ExceptionAddress", wt.DWORD),
                ("NumberParameters", wt.DWORD),
                ("ExceptionInformation", ctypes.c_uint64 * 15)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [("dwDebugEventCode", wt.DWORD), ("dwProcessId", wt.DWORD),
                ("dwThreadId", wt.DWORD), ("_pad", wt.DWORD),
                ("u", ctypes.c_byte * 176)]


def _h(v):
    return v if isinstance(v, ctypes.c_void_p) else ctypes.c_void_p(v)


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest().upper()


def main():
    if sha256f(TARGET) != ENT_SHA:
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py")],
                       capture_output=True, text=True)
    try:
        ok = json.loads(r.stdout).get("verdict") == "PASS"
    except Exception:
        ok = False
    if not ok:
        sys.exit(2)

    si = STARTUPINFO()
    pi = PROCESS_INFORMATION()
    if not k32.CreateProcessA(None, '"{}"'.format(TARGET).encode(), None, None, False,
                              0x2, None, WD.encode(), ctypes.byref(si), ctypes.byref(pi)):
        sys.exit(3)
    print("[spawn] pid={}".format(pi.dwProcessId))
    t0 = time.monotonic()

    record = {"loader_avs": 0, "real_avs": [], "cpp_throws": 0, "exit_code": None,
              "window_closed_by": None, "events": 0}
    done = False
    ev = DEBUG_EVENT()
    av_budget = 500

    while not done:
        # THE WINDOW CHECK EVERY ITERATION (the H5 hang lesson)
        if time.monotonic() - t0 > WINDOW:
            record["window_closed_by"] = "timeout"
            k32.TerminateProcess(_h(pi.hProcess), 1)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, 0x00010002)
            break
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
            continue
        record["events"] += 1
        code = ev.dwDebugEventCode
        tid = ev.dwThreadId
        cont = 0x00010002  # DBG_CONTINUE

        if code == 1:
            er = ctypes.cast(ctypes.byref(ev.u), ctypes.POINTER(EXCEPTION_RECORD)).contents
            ecode = er.ExceptionCode & 0xFFFFFFFF
            exc_addr = er.ExceptionAddress & 0xFFFFFFFF
            if ecode == 0xC0000005:
                av_budget -= 1
                if exc_addr == 0 or not (0x00400000 <= exc_addr < 0x00C00000):
                    # NOTE: the AV's EIP matters, not the exc_addr; peek at the context
                    hth = k32.OpenThread(0x1FFFFF, False, tid)
                    ctx = CONTEXT32()
                    ctx.ContextFlags = 0x1003F
                    k32.Wow64GetThreadContext(_h(hth), ctypes.byref(ctx))
                    k32.CloseHandle(_h(hth))
                    if 0x00400000 <= ctx.Eip < 0x00C00000:
                        # THE REAL CRASH (the EIP in the client image)!
                        rawbuf = (ctypes.c_byte * 0x400)()
                        k32.ReadProcessMemory(_h(pi.hProcess), _h(ctx.Esp), rawbuf, 0x400, None)
                        dvals = struct.unpack("<256I", bytes(rawbuf))
                        cands = [{"off": hex(o * 4), "va": hex(v)}
                                 for o, v in enumerate(dvals) if 0x00400000 <= v < 0x00C00000]
                        rec = {"tid": tid, "exc_addr": hex(exc_addr),
                               "eip": hex(ctx.Eip), "eax": hex(ctx.Eax),
                               "ebx": hex(ctx.Ebx), "ecx": hex(ctx.Ecx), "edx": hex(ctx.Edx),
                               "esi": hex(ctx.Esi), "edi": hex(ctx.Edi),
                               "esp": hex(ctx.Esp), "ebp": hex(ctx.Ebp),
                               "cw": hex(ctx.FloatSave.ControlWord),
                               "exc_info": [hex(x & 0xFFFFFFFF) for x in er.ExceptionInformation[:2]],
                               "stack_candidates": cands[:40],
                               "t": round(time.monotonic() - t0, 3)}
                        record["real_avs"].append(rec)
                        print("[REAL-AV] eip={} exc_addr={} info={} t={}".format(
                            rec["eip"], rec["exc_addr"], rec["exc_info"], rec["t"]))
                        for c in cands[:16]:
                            print("    stack {}".format(c["va"]))
                        if len(record["real_avs"]) >= 2:
                            done = True  # captured — terminate
                    else:
                        record["loader_avs"] += 1
                else:
                    record["loader_avs"] += 1
                if av_budget <= 0:
                    cont = 0x80010001  # break the storm
            elif ecode == 0x80000003:
                pass
            elif ecode == 0xE06D7363:
                record["cpp_throws"] += 1
            else:
                cont = 0x80010001
        elif code == 5:
            record["exit_code"] = struct.unpack_from("<i", ev.u, 0)[0]
            print("[exit] {}".format(record["exit_code"]))
            done = True

        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)

    k32.TerminateProcess(_h(pi.hProcess), 0)
    k32.WaitForSingleObject(_h(pi.hProcess), 5000)
    k32.CloseHandle(_h(pi.hProcess))
    k32.CloseHandle(_h(pi.hThread))
    time.sleep(1)
    proof = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "Get-Process Entropia -ErrorAction SilentlyContinue"],
                           capture_output=True, text=True)
    record["post_kill"] = "clean" if not proof.stdout.strip() else proof.stdout
    record["elapsed_s"] = round(time.monotonic() - t0, 2)
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)
    print("[done] loader_avs={} real={} cpp={} exit={} events={} elapsed={}".format(
        record["loader_avs"], len(record["real_avs"]), record["cpp_throws"],
        record["exit_code"], record["events"], record["elapsed_s"]))


if __name__ == "__main__":
    main()
