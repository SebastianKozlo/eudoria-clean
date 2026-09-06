#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_M1_DEATH_DIAG_R1 — the DIAGNOSTIC DEBUG of the -1@40ms death (H2 of the hourly loop).
Goal: a HARDWARE breakpoint (DR0, execute) at FUN_007c5310 @0x007C5310 (the ONLY exit()
caller — the DPVS teardown-exit). On the hit: capture the CONTEXT + the EBP-chain stack
walk -> THE EXACT FAILING CALL CHAIN. ZERO code patches (DR only); observation only.
Discipline: the kit's verify_sandbox fail-closed preflight; Entropia.exe hash pre-verify;
30-min window; the kill + the death proof + the orphan census on exit."""
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139"
WD = os.path.join(ROOT, "04_RUNTIME", "sandbox", "wd")
TARGET = os.path.join(WD, "Entropia.exe")
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000"
OUT = os.path.join(RUN, "01_RAW", "DEATH_DIAG_RESULT.json")
BP_VA = 0x007C5310  # FUN_007c5310 (the DPVS teardown-exit; the only exit() caller)
ENT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

k32 = ctypes.windll.kernel32


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest().upper()


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
                ("ExceptionRecord", ctypes.c_void_p), ("ExceptionAddress", ctypes.c_void_p),
                ("NumberParameters", wt.DWORD), ("ExceptionInformation", ctypes.c_uint64 * 15)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [("dwDebugEventCode", wt.DWORD), ("dwProcessId", wt.DWORD),
                ("dwThreadId", wt.DWORD),
                ("u", ctypes.c_byte * 176)]


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
                ("SegSs", wt.DWORD),
                ("ExtendedRegisters", ctypes.c_byte * 512)]


DBG_EXCEPTION = 1
CREATE_PROCESS_DEBUG_EVENT = 3
EXIT_PROCESS_DEBUG_EVENT = 5
LOAD_DLL_DEBUG_EVENT = 6
EXCEPTION_DEBUG_EVENT = 1
EXCEPTION_SINGLE_STEP = 0x80000004
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
CONTEXT_FULL = 0x1003F if False else (0x1 | 0x2 | 0x4 | 0x8 | 0x10 | 0x20)  # ALL for 32-bit
CONTEXT_DEBUG_REGISTERS = 0x00100010
CONTEXT_CONTROL = 0x00000001


def main():
    # the fail-closed preflight
    h = sha256f(TARGET)
    if h != ENT_SHA:
        print("HASH MISMATCH — ABORT")
        sys.exit(1)
    print(f"[preflight] Entropia.exe SHA OK ({h[:12]}...)")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py")],
                       capture_output=True, text=True)
    try:
        pre = json.loads(r.stdout)
        ok = pre.get("verdict") == "PASS"
    except Exception:
        ok = False
    print(f"[preflight] verify_sandbox: {'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(2)

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(si)
    pi = PROCESS_INFORMATION()
    cmdline = '"{}"'.format(TARGET).encode()
    ok = k32.CreateProcessA(None, cmdline, None, None, False,
                            0x00000002,  # DEBUG_ONLY_THIS_PROCESS
                            None, WD.encode(), ctypes.byref(si), ctypes.byref(pi))
    if not ok:
        err = ctypes.get_last_error() or k32.GetLastError()
        print("CreateProcess FAILED err={}".format(err))
        sys.exit(3)
    print(f"[spawn] pid={pi.dwProcessId}")
    t0 = time.monotonic()

    record = {"pid": pi.dwProcessId, "bp_va": hex(BP_VA), "events": [], "hit": None}
    armed = False
    done = False
    dbg = DEBUG_EVENT()

    while not done and time.monotonic() - t0 < 120:
        if not k32.WaitForDebugEvent(ctypes.byref(dbg), 1000):
            continue
        ev = dbg.dwDebugEventCode
        pid, tid = dbg.dwProcessId, dbg.dwThreadId
        status = DBG_CONTINUE

        if ev == CREATE_PROCESS_DEBUG_EVENT:
            # arm DR0 (execute @BP_VA) on the main thread via the x64 WOW64 route
            # (the harness-v3 lesson: the WOW64 32-bit set ignores the DR group; use the x64 route)
            th = ctypes.c_void_p(ctypes.windll.kernel32.OpenThread(0x1FFFFF, False, tid))
            # Wow64GetThreadContext via the 32-bit kernel32 on WOW64 reads the 32-bit CONTEXT
            ctx = CONTEXT32()
            ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS | CONTEXT_CONTROL
            if ctypes.windll.kernel32.GetThreadContext(th, ctypes.byref(ctx)):
                ctx.Dr0 = BP_VA
                ctx.Dr7 = (ctx.Dr7 & ~0xF) | 0x1  # L0 enabled, R/W=00 (execute), LEN=00
                ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS | CONTEXT_CONTROL
                if ctypes.windll.kernel32.SetThreadContext(th, ctypes.byref(ctx)):
                    armed = True
                    print(f"[arm] DR0={hex(BP_VA)} armed on thread {tid}")
                else:
                    print("[arm] SetThreadContext FAILED (32-bit route)")
                    # the x64 route fallback: open the thread's x64 context via ntdll
                    NtdGetCurrent = ctypes.windll.ntdll.NtQueryInformationThread
            ctypes.windll.kernel32.CloseHandle(th)
        elif ev == EXCEPTION_DEBUG_EVENT:
            er = ctypes.cast(ctypes.byref(dbg.u), ctypes.POINTER(EXCEPTION_RECORD)).contents
            code = er.ExceptionCode & 0xFFFFFFFF
            if record["hit"] is None and code in (EXCEPTION_SINGLE_STEP, 0x4000001E):
                # possible DR hit: check DR6 via GetThreadContext
                th = ctypes.windll.kernel32.OpenThread(0x1FFFFF, False, tid)
                ctx = CONTEXT32()
                ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS
                ctypes.windll.kernel32.GetThreadContext(th, ctypes.byref(ctx))
                if ctx.Dr6 & 0x1:
                    # HIT at the DPVS-exit! capture everything
                    ctx2 = CONTEXT32()
                    ctx2.ContextFlags = CONTEXT_FULL
                    ctypes.windll.kernel32.GetThreadContext(th, ctypes.byref(ctx2))
                    stack = []
                    ebp = ctx2.Ebp
                    for _ in range(24):
                        if ebp == 0 or ebp == 0xFFFFFFFF or ebp < 0x10000:
                            break
                        buf = ctypes.c_byte * 8
                        rc = ctypes.windll.kernel32.ReadProcessMemory(
                            ctypes.c_void_p(pi.hProcess), ctypes.c_void_p(ebp), ctypes.byref(buf), 8, None)
                        if rc != 1:
                            break
                        vals = struct.unpack("<II", bytes(buf))
                        stack.append({"ebp": hex(ebp), "ret": hex(vals[1])})
                        ebp = vals[0]
                    record["hit"] = {
                        "thread": tid, "eip": hex(ctx2.Eip), "eax": hex(ctx2.Eax),
                        "ebx": hex(ctx2.Ebx), "ecx": hex(ctx2.Ecx), "edx": hex(ctx2.Edx),
                        "esi": hex(ctx2.Esi), "edi": hex(ctx2.Edi), "esp": hex(ctx2.Esp),
                        "dr6": hex(ctx.Dr6), "dr7": hex(ctx.Dr7),
                        "cw": hex(ctx2.FloatSave.ControlWord),
                        "stack": stack,
                    }
                    print(f"[HIT] EIP={hex(ctx2.Eip)} DR6={hex(ctx.Dr6)} frames={len(stack)}")
                    for s in stack:
                        print(f"    ret {s['ret']}")
                    done = True  # captured; terminate
                ctypes.windll.kernel32.CloseHandle(th)
            elif code == 0x80000003:
                pass  # the initial loader bp
            else:
                record["events"].append({"code": hex(code), "tid": tid})
                status = DBG_EXCEPTION_NOT_HANDLED
        elif ev == EXIT_PROCESS_DEBUG_EVENT:
            ex = ctypes.cast(ctypes.byref(dbg.u), ctypes.POINTER(ctypes.c_uint32 * 3)).contents
            record["exit_code"] = ex[0]
            print(f"[exit] code={ex[0]}")
            done = True

        k32.ContinueDebugEvent(pid, tid, status)

    # the kill + the death proof + the orphans
    if not done:
        k32.TerminateProcess(ctypes.c_void_p(pi.hProcess), 0)
    k32.WaitForSingleObject(ctypes.c_void_p(pi.hProcess), 5000)
    k32.CloseHandle(ctypes.c_void_p(pi.hProcess))
    k32.CloseHandle(ctypes.c_void_p(pi.hThread))
    time.sleep(1)
    proof = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "Get-Process Entropia -ErrorAction SilentlyContinue | Select-Object Id",
                            ], capture_output=True, text=True)
    orphans = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "Get-Process ClientLoader,CLDLLPatcher,CLUpdater,PE -ErrorAction SilentlyContinue | Select-Object Id,ProcessName",
                              ], capture_output=True, text=True)
    record["post_kill_GetProcess"] = proof.stdout.strip() or "(no Entropia)"
    record["orphans"] = orphans.stdout.strip() or "(none)"
    record["armed"] = armed
    record["elapsed_s"] = round(time.monotonic() - t0, 2)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)
    print(f"[done] armed={armed} hit={'YES' if record['hit'] else 'NO'} elapsed={record['elapsed_s']}s")
    print(f"written {OUT}")


if __name__ == "__main__":
    main()
