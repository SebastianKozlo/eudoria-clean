#!/usr/bin/env python3
"""diag_one_cycle.py — one instrumented session against SysWOW64\\notepad.exe:
prints every debug event + the arming + whether the DR0 entry-hit arrives.
Isolates: (1) the init breakpoint; (2) the base resolve; (3) the DR arming; (4) the hit."""
import ctypes
import importlib.util
import sys
import time

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126"
spec = importlib.util.spec_from_file_location("h", ROOT + r"\00_CONTROL\x87cw_harness.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
k32 = m.k32

target = r"C:\Windows\SysWOW64\notepad.exe"
ib, entry = m.pe_entry_and_base(target)
bp_va = (ib + entry) & 0xFFFFFFFF
print(f"[diag] ImageBase=0x{ib:08X} entryRVA=0x{entry:X} -> DR0 VA = 0x{bp_va:08X}", flush=True)

pi = m.spawn(target, r"C:\Windows\SysWOW64")
print(f"[diag] spawned pid={pi.dwProcessId} tid={pi.dwThreadId}", flush=True)

ev = m.DEBUG_EVENT()
armed = False
init_seen = 0
t0 = time.monotonic()
while time.monotonic() - t0 < 25:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
        continue
    code = ev.dwDebugEventCode
    if code == 1:  # EXCEPTION
        exr = ev.Exception.ExceptionRecord
        xc = exr.ExceptionCode & 0xFFFFFFFF
        xa = exr.ExceptionAddress & 0xFFFFFFFF
        ht = m.OpenThread(ev.dwThreadId)
        ctx = m.get_context(ht)
        print(f"[diag] EXCEPTION code=0x{xc:08X} addr=0x{xa:08X} eip=0x{ctx.Eip:08X} "
              f"cw=0x{ctx.FloatSave.ControlWord & 0xFFFF:04X}", flush=True)
        if xc == 0x80000003:  # breakpoint
            init_seen += 1
            if not armed:
                m.arm_hw_bps(ht, addr0=bp_va, addr1=None)
                v = m.get_context(ht)
                print(f"[diag] ARMED DR0=0x{v.Dr0:08X} DR7=0x{v.Dr7:08X} "
                      f"(after set, expect DR0=0x{bp_va:08X} DR7=0x00000401)", flush=True)
                armed = True
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
        elif xc == 0x80000004:  # single step
            if ctx.Eip == bp_va:
                print(f"[diag] *** DR HIT at entry! eip=0x{ctx.Eip:08X} "
                      f"cw=0x{ctx.FloatSave.ControlWord & 0xFFFF:04X} ***", flush=True)
            else:
                print(f"[diag] single-step foreign eip=0x{ctx.Eip:08X}", flush=True)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
        else:
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_EXCEPTION_NOT_HANDLED)
        k32.CloseHandle(ht)
        if armed and ctx.Eip == bp_va:
            print("[diag] terminating after the hit", flush=True)
            k32.TerminateProcess(pi.hProcess, 0)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
            break
    else:
        if code in (3, 5, 6):
            extra = ""
            if code == 3:
                b = m.actual_main_base(pi.hProcess)
                extra = f" base=0x{b:08X}" if b else " base=?"
            print(f"[diag] event={code}{extra}", flush=True)
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
    if code == 5:
        print("[diag] EXIT_PROCESS seen", flush=True)
        break

if not armed:
    print("[diag] RESULT: the initial breakpoint NEVER arrived", flush=True)
k32.TerminateProcess(pi.hProcess, 0)
k32.WaitForSingleObject(pi.hProcess, 5000)
ec = ctypes.c_uint()
k32.GetExitCodeProcess(pi.hProcess, ctypes.byref(ec))
print(f"[diag] done. exit_code={ec.value}", flush=True)
