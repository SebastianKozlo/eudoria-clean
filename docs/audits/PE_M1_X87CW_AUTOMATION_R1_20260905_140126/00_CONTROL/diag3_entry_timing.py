#!/usr/bin/env python3
"""diag3_entry_timing.py — when does notepad's ENTRY execute relative to the
initial breakpoint + does DR6.B0 ever record a hardware match?
The empirical timing isolation: event-by-event with elapsed times."""
import ctypes
import importlib.util
import time

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126"
spec = importlib.util.spec_from_file_location("h", ROOT + r"\00_CONTROL\x87cw_harness.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
k32 = m.k32

target = r"C:\Windows\SysWOW64\notepad.exe"
ib, entry_rva = m.pe_entry_and_base(target)
print(f"[d3] ImageBase=0x{ib:08X} entryRVA=0x{entry_rva:X}", flush=True)

pi = m.spawn(target, r"C:\Windows\SysWOW64")
ev = m.DEBUG_EVENT()
t0 = time.monotonic()
n = 0
base = None
bp_count = 0
armed_at = None
last_dr6 = None
while time.monotonic() - t0 < 15:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
        continue
    n += 1
    code = ev.dwDebugEventCode
    el = time.monotonic() - t0
    if code == 3:
        base = ev.CreateProcessInfo.lpBaseOfImage & 0xFFFFFFFF
        print(f"[d3] #{n} CREATE_PROCESS base=0x{base:08X} t={el:.2f}s", flush=True)
    elif code == 1:
        exr = ev.Exception.ExceptionRecord
        xc = exr.ExceptionCode & 0xFFFFFFFF
        xa = exr.ExceptionAddress & 0xFFFFFFFF
        ht = m.OpenThread(ev.dwThreadId)
        c32 = m.get_context(ht)
        label = {0x80000003: "BREAKPOINT", 0x80000004: "SINGLE_STEP"}.get(xc, hex(xc))
        print(f"[d3] #{n} EXC {label} addr=0x{xa:08X} eip=0x{c32.Eip:08X} t={el:.2f}s", flush=True)
        if xc == 0x80000003:
            bp_count += 1
            if armed_at is None:
                entry_va = (base + entry_rva) & 0xFFFFFFFF if base else None
                rv = m.arm_hw_bps(ht, addr0=entry_va, addr1=None)
                armed_at = el
                print(f"[d3]      ARMED at t={el:.2f}s DR0->0x{entry_va:08X} "
                      f"verify={ {k: hex(v) for k, v in rv.items()} }", flush=True)
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
    elif code == 5:
        print(f"[d3] #{n} EXIT_PROCESS t={el:.2f}s (bp_count={bp_count}, armed_at={armed_at})", flush=True)
        # the final DR6 read (on any thread handle we can still query)
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
        break
    elif code in (2, 4):  # CREATE_THREAD / EXIT_THREAD
        pass  # quiet
    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
    # sample DR6 periodically after arming
    if armed_at is not None and n % 20 == 0:
        try:
            ht = m.OpenThread(pi.dwThreadId)
            c = m.CONTEXT64_DR()
            c.ContextFlags = m.CONTEXT_AMD64 | m.CONTEXT64_DEBUG_REGISTERS
            k32.GetThreadContext(ht, ctypes.byref(c))
            last_dr6 = c.Dr6
            print(f"[d3]      DR6 sample @#{n}: 0x{c.Dr6:x} Dr0=0x{c.Dr0:x} t={el:.2f}s", flush=True)
            k32.CloseHandle(ht)
        except OSError:
            pass

if armed_at is None:
    print("[d3] never armed (no initial breakpoint)", flush=True)
else:
    print(f"[d3] RESULT: armed_at={armed_at:.2f}s; final exit; bp_count={bp_count}; "
          f"last_dr6={hex(last_dr6) if last_dr6 is not None else 'not sampled'}", flush=True)
k32.TerminateProcess(pi.hProcess, 0)
k32.WaitForSingleObject(pi.hProcess, 5000)
