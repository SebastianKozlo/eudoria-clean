#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_M1_GATE_BISECT_R1 â€” WHICH orchestrator gate fails?
DR0-DR3 = the first 4 gates; record EVERY hit (the DR6 bits + timestamps) + the natural exit.
The last gate hit (while the next is never hit) = the failing gate = THE PREDICATE OWNER."""
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
OUT = os.path.join(RUN, "01_RAW", "GATE_BISECT_R1.json")
ENT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

# RUN 1: the first 4 gates (the orchestrator order)
GATES = [0x0048E7C0, 0x00415D70, 0x0041B4B0, 0x00416390]
DR7_ALL = 0x00000103 if False else 0x00000103  # L0|L1: see below
# 4 execute bps: L0|L1|L2|L3 = 0xF
DR7_4 = 0x0000000F

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
def _h(v):
    return v if isinstance(v, ctypes.c_void_p) else ctypes.c_void_p(v)


def x64_arm4(hthread):
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(_h(hthread), ctypes.byref(ctx)):
        raise OSError("x64Get: {}".format(ctypes.get_last_error()))
    ctx.Dr0 = GATES[0]
    ctx.Dr1 = GATES[1]
    ctx.Dr2 = GATES[2]
    ctx.Dr3 = GATES[3]
    ctx.Dr6 = 0
    ctx.Dr7 = DR7_4
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.SetThreadContext(_h(hthread), ctypes.byref(ctx)):
        raise OSError("x64Set: {}".format(ctypes.get_last_error()))


def x64_dr6(hthread):
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(_h(hthread), ctypes.byref(ctx)):
        return None
    return ctx.Dr6


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
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "00_CONTROL", "verify_sandbox.py")],
                       capture_output=True, text=True)
    try:
        ok = json.loads(r.stdout).get("verdict") == "PASS"
    except Exception:
        ok = False
    if not ok:
        print("verify FAIL")
        sys.exit(2)

    si = STARTUPINFO()
    pi = PROCESS_INFORMATION()
    cmdline = '"{}"'.format(TARGET).encode()
    if not k32.CreateProcessA(None, cmdline, None, None, False, 0x2, None,
                              WD.encode(), ctypes.byref(si), ctypes.byref(pi)):
        sys.exit(3)
    print("[spawn] pid={}".format(pi.dwProcessId))
    t0 = time.monotonic()

    record = {"gates": [hex(g) for g in GATES], "hits": [], "avs": [], "armed": 0,
              "exit_code": None, "window_closed_by": None}
    done = False
    ev = DEBUG_EVENT()

    while not done:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 1000):
            if time.monotonic() - t0 > 60:
                record["window_closed_by"] = "timeout"
                k32.TerminateProcess(_h(pi.hProcess), 1)
                break
            continue
        code = ev.dwDebugEventCode
        tid = ev.dwThreadId
        cont = 0x00010002  # DBG_CONTINUE

        if code == 3:
            hth = struct.unpack_from("<Q", ev.u, 16)[0]
            try:
                x64_arm4(_h(hth))
                record["armed"] += 1
            except OSError as ex:
                print("[arm-cp] FAIL", ex)
        elif code == 2:
            hth = struct.unpack_from("<Q", ev.u, 0)[0]
            try:
                x64_arm4(_h(hth))
                record["armed"] += 1
            except OSError as ex:
                pass
        elif code == 1:
            er = ctypes.cast(ctypes.byref(ev.u), ctypes.POINTER(EXCEPTION_RECORD)).contents
            ecode = er.ExceptionCode & 0xFFFFFFFF
            if ecode in (0x80000004, 0x4000001E, 0x4000001F):
                hth = k32.OpenThread(0x1FFFFF, False, tid)
                dr6 = x64_dr6(_h(hth))
                if dr6 and (dr6 & 0xF):
                    bits = dr6 & 0xF
                    for b in range(4):
                        if bits & (1 << b):
                            record["hits"].append({"gate": b, "va": hex(GATES[b]),
                                                    "t": round(time.monotonic() - t0, 3),
                                                    "tid": tid})
                            print("[GATE-{}] {} @t={:.3f}".format(b, hex(GATES[b]),
                                                                  time.monotonic() - t0))
                    # continue past (no kill!) â€” the re-arm: clear DR6 + resume
                    # (the harness-v3 lesson: RF+DR6-clear skip)
                    ctx64 = CONTEXT64_DR()
                    ctx64.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
                    k32.GetThreadContext(_h(hth), ctypes.byref(ctx64))
                    ctx64.Dr6 = 0
                    ctx64.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
                    k32.SetThreadContext(_h(hth), ctypes.byref(ctx64))
                k32.CloseHandle(_h(hth))
                # DBG_CONTINUE for the trap
            elif ecode == 0x80000003:
                pass
            elif ecode == 0xE06D7363:
                pass  # the routine C++ throw: continue
            elif ecode == 0xC0000005:
                # THE ACCESS VIOLATION â€” the failure mechanism! Capture + continue.
                hth = k32.OpenThread(0x1FFFFF, False, tid)
                ctx = CONTEXT32()
                ctx.ContextFlags = 0x1003F
                k32.Wow64GetThreadContext(_h(hth), ctypes.byref(ctx))
                rawbuf = (ctypes.c_byte * 0x400)()
                k32.ReadProcessMemory(_h(pi.hProcess), _h(ctx.Esp), rawbuf, 0x400, None)
                dvals = struct.unpack("<256I", bytes(rawbuf))
                cands = [{"off": hex(o * 4), "va": hex(v)}
                         for o, v in enumerate(dvals) if 0x00400000 <= v < 0x00C00000]
                if len(record["avs"]) < 40: record["avs"].append({"tid": tid, "code": hex(ecode),
                                "exc_addr": hex(er.ExceptionAddress & 0xFFFFFFFF),
                                "eip": hex(ctx.Eip), "eax": hex(ctx.Eax), "ebx": hex(ctx.Ebx),
                                "ecx": hex(ctx.Ecx), "edx": hex(ctx.Edx), "esi": hex(ctx.Esi),
                                "edi": hex(ctx.Edi), "esp": hex(ctx.Esp), "ebp": hex(ctx.Ebp),
                                "exc_info": [hex(x & 0xFFFFFFFF) for x in er.ExceptionInformation[:2]],
                                "stack_candidates": cands[:30],
                                "t": round(time.monotonic() - t0, 3)})
                print("[AV#{}] exc_addr={} eip={} t={}".format(
                    len(record["avs"])-1, record["avs"][-1]["exc_addr"], record["avs"][-1]["eip"], record["avs"][-1]["t"]))
                k32.CloseHandle(_h(hth))
                # DBG_CONTINUE: the client's own SEH handles it (the natural flow)
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
    hits = [h["gate"] for h in record["hits"]]
    print("[done] hits={} exit={} armed={} elapsed={}".format(
        hits, record["exit_code"], record["armed"], record["elapsed_s"]))


if __name__ == "__main__":
    main()





