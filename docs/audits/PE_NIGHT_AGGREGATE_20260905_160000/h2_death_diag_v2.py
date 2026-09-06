#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_M1_DEATH_DIAG_R1 v2 â€” the DIAGNOSTIC DEBUG of the -1 death (H2).
The v3-harness discipline applied: the x64 DR-write route (FACT2: the WOW64 32-bit
set IGNORES the DR group), armed on EVERY thread (CREATE_PROCESS + CREATE_THREAD),
DR0 = execute @0x007C5310 (FUN_007c5310, the ONLY exit() caller). On the hit:
the full CONTEXT + the EBP-chain stack walk = THE EXACT FAILING CALL CHAIN.
ZERO code patches; observation only; kill + death proof + orphan census."""
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
OUT = os.path.join(RUN, "01_RAW", "DEATH_DIAG_V2_RESULT.json")
BP0 = 0x00402910  # the message loop (runs only if the deep-init returned TRUE)`nBP1 = 0x00417030  # the LOOP-STEP (the engine tick)`nBP2 = 0x007C5310  # the DPVS teardown-exit (the only exit() caller)
ENT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

k32 = ctypes.windll.kernel32

# ---- the x64 CONTEXT (debug-registers group) per the v3 harness ----


class CONTEXT64_DR(ctypes.Structure):
    _pack_ = 16
    _fields_ = [("P1Home", ctypes.c_uint64), ("P2Home", ctypes.c_uint64),
                ("P3Home", ctypes.c_uint64), ("P4Home", ctypes.c_uint64),
                ("P5Home", ctypes.c_uint64), ("P6Home", ctypes.c_uint64),
                ("ContextFlags", ctypes.c_uint), ("MxCsr", ctypes.c_uint),
                ("SegCs", ctypes.c_ushort), ("SegDs", ctypes.c_ushort),
                ("SegEs", ctypes.c_ushort), ("SegFs", ctypes.c_ushort),
                ("SegGs", ctypes.c_ushort), ("SegSs", ctypes.c_ushort),
                ("EFlags", ctypes.c_uint),
                ("Dr0", ctypes.c_uint64), ("Dr1", ctypes.c_uint64),
                ("Dr2", ctypes.c_uint64), ("Dr3", ctypes.c_uint64),
                ("Dr6", ctypes.c_uint64), ("Dr7", ctypes.c_uint64),
                ("pad", ctypes.c_ubyte * (0x4D0 - 0x78))]


CONTEXT_AMD64 = 0x00100000
CONTEXT64_DEBUG_REGISTERS = 0x00000010


def _as_handle(h):
    return h if isinstance(h, ctypes.c_void_p) else ctypes.c_void_p(h)


def x64_arm(hthread, dr0, dr1=None, dr2=None, dr7=1, clear_dr6=True):
    hth = _as_handle(hthread)
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(hth, ctypes.byref(ctx)):
        raise OSError("x64Get failed: {}".format(ctypes.get_last_error()))
    ctx.Dr0 = dr0
    ctx.Dr7 = dr7
    if clear_dr6:
        ctx.Dr6 = 0
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.SetThreadContext(hth, ctypes.byref(ctx)):
        raise OSError("x64Set failed: {}".format(ctypes.get_last_error()))


def x64_read_dr6(hthread):
    hth = _as_handle(hthread)
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(hth, ctypes.byref(ctx)):
        return None
    return ctx.Dr6, ctx.Dr7, ctx.Dr0


# ---- the 32-bit CONTEXT for the register/stack capture ----


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
    _fields_ = [("hProcess", wt.DWORD), ("hThread", wt.DWORD),
                ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD)]


class EXCEPTION_RECORD(ctypes.Structure):
    _fields_ = [("ExceptionCode", wt.DWORD), ("ExceptionFlags", wt.DWORD),
                ("ExceptionRecord", wt.DWORD), ("ExceptionAddress", wt.DWORD),
                ("NumberParameters", wt.DWORD),
                ("ExceptionInformation", ctypes.c_uint64 * 15)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [("dwDebugEventCode", wt.DWORD), ("dwProcessId", wt.DWORD),
                ("dwThreadId", wt.DWORD), ("u", ctypes.c_byte * 176)]


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
    h = sha256f(TARGET)
    if h != ENT_SHA:
        print("HASH MISMATCH")
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py")],
                       capture_output=True, text=True)
    ok = False
    try:
        ok = json.loads(r.stdout).get("verdict") == "PASS"
    except Exception:
        pass
    print("[preflight] hash OK; verify:", "PASS" if ok else "FAIL")
    if not ok:
        sys.exit(2)

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    pi = PROCESS_INFORMATION()
    cmdline = '"{}"'.format(TARGET).encode()
    ok = k32.CreateProcessA(None, cmdline, None, None, False, 0x2, None,
                            WD.encode(), ctypes.byref(si), ctypes.byref(pi))
    if not ok:
        print("CreateProcess FAILED", k32.GetLastError())
        sys.exit(3)
    print("[spawn] pid={} tid={}".format(pi.dwProcessId, pi.dwThreadId))
    t0 = time.monotonic()

    record = {"pid": pi.dwProcessId, "bp_va": hex(BP_VA), "hit": None,
              "armed_threads": [], "exception_events": [], "exit_code": None,
              "window_closed_by": None}
    done = False
    armed = set()
    ev = DEBUG_EVENT()

    while not done:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 1000):
            if time.monotonic() - t0 > 120:
                record["window_closed_by"] = "timeout_no_events"
                break
            continue
        if time.monotonic() - t0 > 120:
            record["window_closed_by"] = "timeout"
            k32.TerminateProcess(ctypes.c_void_p(pi.hProcess), 1)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, 0x00010002)
            break
        code = ev.dwDebugEventCode
        tid = ev.dwThreadId
        cont = 0x00010002  # DBG_CONTINUE

        if code == 3:  # CREATE_PROCESS
            hth = struct.unpack_from("<I", ev.u, 4)[0]  # hThread at u+4
            try:
                x64_arm(ctypes.c_void_p(hth), BP_VA)
                armed.add(tid)
                record["armed_threads"].append({"tid": tid, "via": "CREATE_PROCESS"})
                print("[arm] thread {} DR0={:#x}".format(tid, BP_VA))
            except OSError as ex:
                print("[arm] FAILED:", ex)
        elif code == 2:  # CREATE_THREAD
            hth = struct.unpack_from("<I", ev.u, 4)[0]
            try:
                x64_arm(ctypes.c_void_p(hth), BP_VA)
                armed.add(tid)
                record["armed_threads"].append({"tid": tid, "via": "CREATE_THREAD"})
                print("[arm] thread {} (new)".format(tid))
            except OSError as ex:
                print("[arm-new] FAILED:", ex)
        elif code == 1:  # EXCEPTION
            er = ctypes.cast(ctypes.byref(ev.u), ctypes.POINTER(EXCEPTION_RECORD)).contents
            ecode = er.ExceptionCode & 0xFFFFFFFF
            if record["hit"] is None and ecode in (0x80000004, 0x4000001E):
                hth = k32.OpenThread(0x1FFFFF, False, tid)
                dr = x64_read_dr6(ctypes.c_void_p(hth))
                if dr and (dr[0] & 0x1):
                    ctx = CONTEXT32()
                    ctx.ContextFlags = 0x1F  # full-ish
                    k32.GetThreadContext(ctypes.c_void_p(hth), ctypes.byref(ctx))
                    stack = []
                    ebp = ctx.Ebp
                    for _ in range(24):
                        if not (0x10000 < ebp < 0x800000000000):
                            break
                        buf = (ctypes.c_byte * 8)()
                        rc = k32.ReadProcessMemory(ctypes.c_void_p(pi.hProcess),
                                                   ctypes.c_void_p(ebp), ctypes.byref(buf), 8, None)
                        if rc != 1:
                            break
                        v = struct.unpack("<II", bytes(buf))
                        stack.append({"ebp": hex(ebp), "ret": hex(v[1])})
                        ebp = v[0]
                    record["hit"] = {"thread": tid, "eip": hex(ctx.Eip),
                                     "eax": hex(ctx.Eax), "ebx": hex(ctx.Ebx),
                                     "ecx": hex(ctx.Ecx), "edx": hex(ctx.Edx),
                                     "esi": hex(ctx.Esi), "edi": hex(ctx.Edi),
                                     "esp": hex(ctx.Esp), "dr6": hex(dr[0]),
                                     "cw": hex(ctx.FloatSave.ControlWord),
                                     "stack": stack}
                    print("[HIT] EIP={} DR6={} frames={}".format(hex(ctx.Eip), hex(dr[0]), len(stack)))
                    for s in stack:
                        print("    ret {}".format(s["ret"]))
                    done = True
                k32.CloseHandle(ctypes.c_void_p(hth))
            elif ecode == 0x80000003:
                pass  # the loader bp
            else:
                record["exception_events"].append({"code": hex(ecode), "tid": tid,
                                                   "addr": hex(er.ExceptionAddress & 0xFFFFFFFF)})
                cont = 0x80010001  # NOT_HANDLED for the app's own exceptions
        elif code == 5:  # EXIT_PROCESS
            record["exit_code"] = struct.unpack_from("<i", ev.u, 0)[0]
            print("[exit] code={}".format(record["exit_code"]))
            done = True

        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)

    # cleanup: kill + proof + orphans
    k32.TerminateProcess(ctypes.c_void_p(pi.hProcess), 0)
    k32.WaitForSingleObject(ctypes.c_void_p(pi.hProcess), 5000)
    k32.CloseHandle(ctypes.c_void_p(pi.hProcess))
    k32.CloseHandle(ctypes.c_void_p(pi.hThread))
    time.sleep(1)
    proof = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "Get-Process Entropia -ErrorAction SilentlyContinue"],
                           capture_output=True, text=True)
    orph = subprocess.run(["powershell", "-NoProfile", "-Command",
                           "Get-Process ClientLoader,CLDLLPatcher,CLUpdater,PE -ErrorAction SilentlyContinue"],
                          capture_output=True, text=True)
    record["post_kill"] = "clean" if not proof.stdout.strip() else proof.stdout
    record["orphans"] = "clean" if not orph.stdout.strip() else orph.stdout
    record["elapsed_s"] = round(time.monotonic() - t0, 2)
    record["armed_count"] = len(armed)

    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)
    print("[done] hit={} exit={} armed={} elapsed={}s".format(
        "YES" if record["hit"] else "NO", record["exit_code"], len(armed), record["elapsed_s"]))


if __name__ == "__main__":
    main()


