#!/usr/bin/env python3
"""diag2_dr_route.py — isolate the DR-setting route on a WOW64 thread:
x64-Get, x64-Set, x64-Get, Wow64-Get — each with the return code + last error."""
import ctypes
import importlib.util
import time

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126"
spec = importlib.util.spec_from_file_location("h", ROOT + r"\00_CONTROL\x87cw_harness.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
k32 = m.k32

target = r"C:\Windows\SysWOW64\notepad.exe"
ib, entry = m.pe_entry_and_base(target)
bp_va = (ib + entry) & 0xFFFFFFFF
print(f"[d2] bp_va=0x{bp_va:08X}", flush=True)

pi = m.spawn(target, r"C:\Windows\SysWOW64")
ev = m.DEBUG_EVENT()
armed = False
t0 = time.monotonic()
while time.monotonic() - t0 < 20:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
        continue
    code = ev.dwDebugEventCode
    if code == 1 and not armed:
        exr = ev.Exception.ExceptionRecord
        if (exr.ExceptionCode & 0xFFFFFFFF) == 0x80000003:
            ht = m.OpenThread(ev.dwThreadId)
            # 1) x64 GET
            ctx = m.CONTEXT64_DR()
            ctx.ContextFlags = m.CONTEXT_AMD64 | m.CONTEXT64_DEBUG_REGISTERS
            r1 = k32.GetThreadContext(ht, ctypes.byref(ctx))
            e1 = ctypes.get_last_error()
            print(f"[d2] x64GET rc={r1} err={e1} Dr0={ctx.Dr0:#x} Dr7={ctx.Dr7:#x}", flush=True)
            # 2) x64 SET
            ctx.Dr0 = bp_va
            ctx.Dr7 = 0x00000401
            ctx.ContextFlags = m.CONTEXT_AMD64 | m.CONTEXT64_DEBUG_REGISTERS
            r2 = k32.SetThreadContext(ht, ctypes.byref(ctx))
            e2 = ctypes.get_last_error()
            print(f"[d2] x64SET rc={r2} err={e2}", flush=True)
            # 3) x64 GET again
            ctx2 = m.CONTEXT64_DR()
            ctx2.ContextFlags = m.CONTEXT_AMD64 | m.CONTEXT64_DEBUG_REGISTERS
            r3 = k32.GetThreadContext(ht, ctypes.byref(ctx2))
            e3 = ctypes.get_last_error()
            print(f"[d2] x64GET2 rc={r3} err={e3} Dr0={ctx2.Dr0:#x} Dr7={ctx2.Dr7:#x}", flush=True)
            # 4) Wow64 GET (the 32-bit view)
            c32 = m.get_context(ht)
            print(f"[d2] wow64GET Dr0={c32.Dr0:#010x} Dr7={c32.Dr7:#010x} "
                  f"cw={c32.FloatSave.ControlWord & 0xFFFF:#06x} eip={c32.Eip:#010x}", flush=True)
            armed = True
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
            k32.CloseHandle(ht)
            continue
        elif (exr.ExceptionCode & 0xFFFFFFFF) == 0x80000004:
            ht = m.OpenThread(ev.dwThreadId)
            c32 = m.get_context(ht)
            hit = " *** DR HIT ***" if c32.Eip == bp_va else ""
            print(f"[d2] SINGLE_STEP eip={c32.Eip:#010x} cw={c32.FloatSave.ControlWord & 0xFFFF:#06x}{hit}", flush=True)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
            k32.CloseHandle(ht)
            if hit:
                break
            continue
    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId,
                           m.DBG_CONTINUE if code != 1 else m.DBG_EXCEPTION_NOT_HANDLED)
k32.TerminateProcess(pi.hProcess, 0)
k32.WaitForSingleObject(pi.hProcess, 5000)
print("[d2] done", flush=True)
