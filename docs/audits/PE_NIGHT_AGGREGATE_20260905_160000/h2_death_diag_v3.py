#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_M1_DEATH_DIAG_R1 v3 â€” the 3-breakpoint diagnostic (H2).
DR0 = 0x00402910 (the message loop â€” runs only if the deep-init returned TRUE)
DR1 = 0x00417030 (the LOOP-STEP â€” the engine tick)
DR2 = 0x007C5310 (the DPVS teardown-exit â€” the only exit() caller)
All execute @ the function entries. On the FIRST hit: the full CONTEXT + the
EBP-chain stack walk -> the failing-chain discrimination. x64 DR route; every
thread; zero code patches; kill + proof + orphans."""
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
OUT = os.path.join(RUN, "01_RAW", "DEATH_DIAG_V3_RESULT.json")
BP0 = 0x00402910
BP1 = 0x00417030
BP2 = 0x007C5310
DR7_ALL = 0x00000107  # L0|L1|L2, R/W=00 LEN=00 (execute) for all three
ENT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

k32 = ctypes.windll.kernel32


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


def _h(v):
    return v if isinstance(v, ctypes.c_void_p) else ctypes.c_void_p(v)


def x64_arm(hthread):
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(_h(hthread), ctypes.byref(ctx)):
        raise OSError("x64Get: {}".format(ctypes.get_last_error()))
    ctx.Dr0 = BP0
    ctx.Dr1 = BP1
    ctx.Dr2 = BP2
    ctx.Dr6 = 0
    ctx.Dr7 = DR7_ALL
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.SetThreadContext(_h(hthread), ctypes.byref(ctx)):
        raise OSError("x64Set: {}".format(ctypes.get_last_error()))


def x64_dr6(hthread):
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(_h(hthread), ctypes.byref(ctx)):
        return None
    return ctx.Dr6, ctx.Dr7


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
        print("HASH MISMATCH")
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "00_Control".replace("Control", "CONTROL"),
                                                       "verify_sandbox.py")],
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
    pi = PROCESS_INFORMATION()
    cmdline = '"{}"'.format(TARGET).encode()
    ok = k32.CreateProcessA(None, cmdline, None, None, False, 0x2, None,
                            WD.encode(), ctypes.byref(si), ctypes.byref(pi))
    if not ok:
        print("CreateProcess FAILED", k32.GetLastError())
        sys.exit(3)
    print("[spawn] pid={}".format(pi.dwProcessId))
    t0 = time.monotonic()

    record = {"pid": pi.dwProcessId, "bps": [hex(BP0), hex(BP1), hex(BP2)],
              "hit": None, "armed": 0, "exception_events": [], "exit_code": None,
              "window_closed_by": None}
    modules = []  # (base, name) from LOAD_DLL
    done = False
    ev = DEBUG_EVENT()
    BPS = {1: "MSG_LOOP_00402910", 2: "LOOP_STEP_00417030", 4: "DPVS_EXIT_007C5310"}

    while not done:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 1000):
            if time.monotonic() - t0 > 120:
                record["window_closed_by"] = "timeout_no_events"
                break
            continue
        if time.monotonic() - t0 > 120:
            record["window_closed_by"] = "timeout"
            k32.TerminateProcess(_h(pi.hProcess), 1)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, 0x00010002)
            break
        code = ev.dwDebugEventCode
        tid = ev.dwThreadId
        cont = 0x00010002

        if code == 3:  # CREATE_PROCESS: hThread at u+8 (hFile,hProcess,hThread)
            hth = struct.unpack_from("<Q", ev.u, 16)[0]  # hFile@0,hProcess@8,hThread@16 (64-bit handles)
            try:
                x64_arm(_h(hth))
                record["armed"] += 1
            except OSError as ex:
                print("[arm-cp] FAILED:", ex)
        elif code == 2:  # CREATE_THREAD: hThread at u+0
            hth = struct.unpack_from("<Q", ev.u, 0)[0]  # hThread@0 (64-bit handle)
            try:
                x64_arm(_h(hth))
                record["armed"] += 1
            except OSError as ex:
                print("[arm-ct] FAILED:", ex)
        elif code == 1:  # EXCEPTION
            er = ctypes.cast(ctypes.byref(ev.u), ctypes.POINTER(EXCEPTION_RECORD)).contents
            ecode = er.ExceptionCode & 0xFFFFFFFF
            if record["hit"] is None and ecode in (0x80000004, 0x4000001E, 0x4000001F):
                hth = k32.OpenThread(0x1FFFFF, False, tid)
                dr = x64_dr6(_h(hth))
                if dr and (dr[0] & 0x7):
                    bit = dr[0] & 0x7
                    ctx = CONTEXT32()
                    ctx.ContextFlags = 0x1003F  # i386 CONTEXT_FULL
                    k32.Wow64GetThreadContext(_h(hth), ctypes.byref(ctx))
                    stack = []
                    ebp = ctx.Ebp
                    for _ in range(24):
                        if not (0x10000 < ebp < 0x7FF00000000):
                            break
                        buf = (ctypes.c_byte * 8)()
                        rc = k32.ReadProcessMemory(_h(pi.hProcess), _h(ebp), buf, 8, None)
                        if rc != 1:
                            break
                        v = struct.unpack("<II", bytes(buf))
                        stack.append({"ebp": hex(ebp), "ret": hex(v[1])})
                        ebp = v[0]
                    record["hit"] = {"which": BPS.get(bit, "?dr6=" + hex(dr[0])),
                                     "thread": tid, "eip": hex(ctx.Eip),
                                     "eax": hex(ctx.Eax), "ebx": hex(ctx.Ebx),
                                     "ecx": hex(ctx.Ecx), "edx": hex(ctx.Edx),
                                     "esi": hex(ctx.Esi), "edi": hex(ctx.Edi),
                                     "esp": hex(ctx.Esp), "dr6": hex(dr[0]),
                                     "cw": hex(ctx.FloatSave.ControlWord),
                                     "stack": stack}
                    print("[HIT-BP] {} @{} EIP={} DR6={} frames={}".format(
                        BPS.get(bit, "?"), tid, hex(ctx.Eip), hex(dr[0]), len(stack)))
                    for s in stack:
                        print("    ret {}".format(s["ret"]))
                    done = True
                k32.CloseHandle(_h(hth))
            elif ecode == 0xE06D7363 and record.get("cpp_throw") is None:
                # THE C++ EXCEPTION (the display-init failure mechanism!): capture
                # the THROW-SITE stack = the failing call chain; then CONTINUE
                # (the client's own handler catches it -> the controlled exit).
                hth = k32.OpenThread(0x1FFFFF, False, tid)
                ctx = CONTEXT32()
                ctx.ContextFlags = 0x1003F  # i386 CONTEXT_FULL
                k32.Wow64GetThreadContext(_h(hth), ctypes.byref(ctx))
                stack = []
                ebp = ctx.Ebp
                for _ in range(28):
                    if not (0x10000 < ebp < 0x7FF00000000):
                        break
                    buf = (ctypes.c_byte * 8)()
                    rc = k32.ReadProcessMemory(_h(pi.hProcess), _h(ebp), buf, 8, None)
                    if rc != 1:
                        break
                    v = struct.unpack("<II", bytes(buf))
                    stack.append({"ebp": hex(ebp), "ret": hex(v[1])})
                    ebp = v[0]
                record["cpp_throw"] = {"thread": tid, "eip": hex(ctx.Eip),
                                      "eax": hex(ctx.Eax), "ebx": hex(ctx.Ebx),
                                      "ecx": hex(ctx.Ecx), "edx": hex(ctx.Edx),
                                      "esi": hex(ctx.Esi), "edi": hex(ctx.Edi),
                                      "esp": hex(ctx.Esp),
                                      "cw": hex(ctx.FloatSave.ControlWord),
                                      "stack": stack}
                # the RAW STACK SCAN: the client's return addresses (the exe range)
                rawbuf = (ctypes.c_byte * 0x800)()
                rc = k32.ReadProcessMemory(_h(pi.hProcess), _h(ctx.Esp), rawbuf, 0x800, None)
                candidates = []
                if rc == 1:
                    dvals = struct.unpack("<512I", bytes(rawbuf))
                    for off, v in enumerate(dvals):
                        tag = None
                        if 0x00400000 <= v < 0x00C00000:
                            tag = "exe"
                        else:
                            for mb in modules:
                                if mb and mb <= v < mb + 0x4000000:
                                    tag = "dll@0x{:x}".format(mb)
                                    break
                        if tag:
                            candidates.append({"esp_off": hex(off * 4), "va": hex(v), "mod": tag})
                record["cpp_throw"]["modules_loaded"] = len(modules)
                record["cpp_throw"]["raw_scan"] = candidates[:60]
                print("[C++THROW] EIP={} tid={} frames={} raw_candidates={}".format(
                    hex(ctx.Eip), tid, len(stack), len(candidates)))
                for s in stack:
                    print("    ret {}".format(s["ret"]))
                print("  raw scan (the exe-range dwords on the stack):")
                for c in candidates[:24]:
                    print("    {} @{}".format(c["va"], c["esp_off"]))
                k32.CloseHandle(_h(hth))
                # DBG_CONTINUE (the first chance: let the client's handler run)
            elif ecode == 0x80000003:
                pass
            else:
                record["exception_events"].append({"code": hex(ecode), "tid": tid})
                cont = 0x80010001
        elif code == 6:  # LOAD_DLL: hFile@0, lpBaseOfImage@16 (64-bit union)
            base = struct.unpack_from("<Q", ev.u, 8)[0]  # hFile@0(8), lpBaseOfImage@8
            # the name: query the file handle is complex; just record the base
            modules.append(base)
        elif code == 5:  # EXIT_PROCESS
            record["exit_code"] = struct.unpack_from("<i", ev.u, 0)[0]
            print("[exit] code={}".format(record["exit_code"]))
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
    orph = subprocess.run(["powershell", "-NoProfile", "-Command",
                           "Get-Process ClientLoader,CLDLLPatcher,CLUpdater,PE -ErrorAction SilentlyContinue"],
                          capture_output=True, text=True)
    record["post_kill"] = "clean" if not proof.stdout.strip() else proof.stdout
    record["orphans"] = "clean" if not orph.stdout.strip() else orph.stdout
    record["elapsed_s"] = round(time.monotonic() - t0, 2)
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2)
    print("[done] hit={} exit={} armed={} elapsed={}s".format(
        record["hit"]["which"] if record["hit"] else "NO",
        record["exit_code"], record["armed"], record["elapsed_s"]))


if __name__ == "__main__":
    main()








