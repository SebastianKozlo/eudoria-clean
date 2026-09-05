#!/usr/bin/env python3
"""diag4_control_and_bytes.py — the A/B control: (A) NO DR armed: does notepad
run clean? (B) the bytes at the entry + the storm record detail (first-chance,
ExceptionInformation) + the RF-based continue test."""
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


def control_run(seconds=6):
    """No DR armed - the control."""
    pi = m.spawn(target, r"C:\Windows\SysWOW64")
    ev = m.DEBUG_EVENT()
    counts = {}
    t0 = time.monotonic()
    while time.monotonic() - t0 < seconds:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
            continue
        code = ev.dwDebugEventCode
        if code == 1:
            xc = ev.Exception.ExceptionRecord.ExceptionCode & 0xFFFFFFFF
            counts[hex(xc)] = counts.get(hex(xc), 0) + 1
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId,
                               m.DBG_CONTINUE if code != 1 else m.DBG_EXCEPTION_NOT_HANDLED)
        if code == 5:
            break
    k32.TerminateProcess(pi.hProcess, 0)
    k32.WaitForSingleObject(pi.hProcess, 5000)
    return counts


def storm_run(seconds=6):
    """DR armed + the storm detail + the RF-continue test."""
    pi = m.spawn(target, r"C:\Windows\SysWOW64")
    ev = m.DEBUG_EVENT()
    base = None
    armed = False
    storm = []
    rf_tested = False
    t0 = time.monotonic()
    while time.monotonic() - t0 < seconds:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
            continue
        code = ev.dwDebugEventCode
        if code == 3:
            base = ev.CreateProcessInfo.lpBaseOfImage & 0xFFFFFFFF
        elif code == 1:
            exr = ev.Exception.ExceptionRecord
            xc = exr.ExceptionCode & 0xFFFFFFFF
            xa = exr.ExceptionAddress & 0xFFFFFFFF
            entry_va = (base + entry_rva) & 0xFFFFFFFF if base else None
            ht = m.OpenThread(ev.dwThreadId)
            c32 = m.get_context(ht)
            if xc == 0x80000003 and not armed:
                m.arm_hw_bps(ht, addr0=entry_va, addr1=None)
                armed = True
                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
            elif xa == entry_va and len(storm) < 8:
                storm.append({"code": hex(xc), "eip": hex(c32.Eip),
                              "first_chance": ev.Exception.dwFirstChance,
                              "info0": exr.ExceptionInformation[0],
                              "cw": hex(c32.FloatSave.ControlWord & 0xFFFF),
                              "dr6_x64": None})
                if len(storm) == 1:
                    # the byte dump at the entry
                    buf = ctypes.create_string_buffer(16)
                    nread = ctypes.c_size_t()
                    ok = k32.ReadProcessMemory(pi.hProcess, ctypes.c_void_p(entry_va),
                                               buf, 16, ctypes.byref(nread))
                    print(f"[d4] ENTRY BYTES @0x{entry_va:08X}: "
                          f"{buf.raw[:nread.value].hex(' ') if ok else 'READ FAIL'}", flush=True)
                # the RF test: set the Resume Flag in EFlags (0x10000) via the
                # 32-bit context + clear DR6, then continue
                c32.EFlags |= 0x00010000
                m.set_context(ht, c32)
                # verify the write stuck
                c32v = m.get_context(ht)
                storm[-1]["eflags_after"] = hex(c32v.EFlags)
                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
                if len(storm) == 8:
                    rf_tested = True
            else:
                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId,
                                       m.DBG_CONTINUE if xa != entry_va else m.DBG_CONTINUE)
            k32.CloseHandle(ht)
            if rf_tested:
                break
        else:
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, m.DBG_CONTINUE)
    k32.TerminateProcess(pi.hProcess, 0)
    k32.WaitForSingleObject(pi.hProcess, 5000)
    return storm


print("[d4] CONTROL (no DR):", flush=True)
cc = control_run()
print(f"[d4] control exception counts over 6s: {cc}", flush=True)
print("[d4] STORM RUN (DR armed, RF-continue test):", flush=True)
st = storm_run()
for s in st:
    print(f"[d4] storm: {s}", flush=True)
print(f"[d4] storm records: {len(st)}; rf_effective = "
      f"{len(st) < 8}", flush=True)
