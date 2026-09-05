#!/usr/bin/env python3
"""x87cw_harness.py — Backend E of the x87 CW AUTOMATION_FEASIBILITY bake-off.
A headless Win32 Debug API harness (no GUI, no debugger attach, no target-code
execution, no code patching): CreateProcess(DEBUG_ONLY_THIS_PROCESS) +
hardware execute breakpoints via DR0/DR1 + GetThreadContext ->
CONTEXT_FLOATING_SAVE_AREA.ControlWord. THE observation-only instrument.
PE_M1_X87CW_AUTOMATION_R1_20260905_140126 | the PE-MASTER AUTOMATION_FEASIBILITY
order (B/C/D bake-off failed empirically; E authorized by the order's own ladder).

MODES:
  qualify            10 spawn-cycles against C:\\Windows\\SysWOW64\\notepad.exe
                     (the harmless synthetic target); DR bp at (ImageBase+entry);
                     PASS = 10/10 cycles with a CW read + a clean exit proof each.
  measure            the real measurement: the sandbox Entropia.exe; DR0=0x0098CE5A,
                     DR1=0x0095B2BC (the canon VAs, module-base-verified at the
                     initial bp; delta-shifted if relocated); N=10 hits/site; the aux
                     init-CW read at the initial breakpoint; the bounded 30-min
                     window; TerminateProcess + WaitForSingleObject +
                     GetExitCodeProcess (the independent exit proof) + the child/
                     orphan census (the liveness discipline, profile section 14).

OUTPUT: <outdir>\\cw_capture.jsonl (the 16-field lines, machine-written,
capture_method=win32_context_read) + <outdir>\\raw_context_log.jsonl (the full
FLOATING_SAVE_AREA per hit — the evidence corpus) + <outdir>\\harness_session.json
(the liveness/exit proofs + the summary). EXIT 0 = completed per the gate;
non-zero = the W4-style failure class in the JSON + stderr.
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import json
import os
import struct
import sys
import time
from datetime import datetime, timezone

# ---------------- Win32 constants ----------------
DEBUG_ONLY_THIS_PROCESS = 0x00000002
INFINITE = 0xFFFFFFFF
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
EXCEPTION_BREAKPOINT = 0x80000003
EXCEPTION_SINGLE_STEP = 0x80000004
CREATE_PROCESS_DEBUG_EVENT = 3
EXCEPTION_DEBUG_EVENT = 1
EXIT_PROCESS_DEBUG_EVENT = 5
LOAD_DLL_DEBUG_EVENT = 6
CONTEXT_i386 = 0x00010000
CONTEXT_CONTROL = 0x00000001
CONTEXT_INTEGER = 0x00000002
CONTEXT_FLOATING_POINT = 0x00000008
CONTEXT_DEBUG_REGISTERS = 0x00000100
CONTEXT_FULL_X86 = CONTEXT_i386 | CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT | CONTEXT_DEBUG_REGISTERS
TH32CS_SNAPPROCESS = 0x00000002
LIST_MODULES_32BIT = 0x01

k32 = ctypes.WinDLL("kernel32", use_last_error=True)

# ---------------- x86 CONTEXT (the WOW64 target's context) ----------------
class FLOATING_SAVE_AREA(ctypes.Structure):
    _fields_ = [("ControlWord", ctypes.c_uint), ("StatusWord", ctypes.c_uint),
                ("TagWord", ctypes.c_uint), ("ErrorOffset", ctypes.c_uint),
                ("ErrorSelector", ctypes.c_uint), ("DataOffset", ctypes.c_uint),
                ("DataSelector", ctypes.c_uint),
                ("RegisterArea", ctypes.c_ubyte * 80),
                ("Cr0NpxState", ctypes.c_uint)]

class CONTEXT_x86(ctypes.Structure):
    _pack_ = 16  # the x86 CONTEXT alignment (the OS requires this packing)
    _fields_ = [("ContextFlags", ctypes.c_uint),
                ("Dr0", ctypes.c_uint), ("Dr1", ctypes.c_uint),
                ("Dr2", ctypes.c_uint), ("Dr3", ctypes.c_uint),
                ("Dr6", ctypes.c_uint), ("Dr7", ctypes.c_uint),
                ("FloatSave", FLOATING_SAVE_AREA),
                ("SegGs", ctypes.c_uint), ("SegFs", ctypes.c_uint),
                ("SegEs", ctypes.c_uint), ("SegDs", ctypes.c_uint),
                ("Edi", ctypes.c_uint), ("Esi", ctypes.c_uint),
                ("Ebx", ctypes.c_uint), ("Edx", ctypes.c_uint),
                ("Ecx", ctypes.c_uint), ("Eax", ctypes.c_uint),
                ("Ebp", ctypes.c_uint), ("Eip", ctypes.c_uint),
                ("SegCs", ctypes.c_uint), ("EFlags", ctypes.c_uint),
                ("Esp", ctypes.c_uint), ("SegSs", ctypes.c_uint),
                ("ExtendedRegisters", ctypes.c_ubyte * 512)]

class EXCEPTION_RECORD32(ctypes.Structure):
    _fields_ = [("ExceptionCode", ctypes.c_uint), ("ExceptionFlags", ctypes.c_uint),
                ("ExceptionRecord", ctypes.c_uint64), ("ExceptionAddress", ctypes.c_uint64),
                ("NumberParameters", ctypes.c_uint),
                ("ExceptionInformation", ctypes.c_uint64 * 15)]

class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [("ExceptionRecord", EXCEPTION_RECORD32), ("dwFirstChance", ctypes.c_uint)]

class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [("hFile", ctypes.c_void_p), ("hProcess", ctypes.c_void_p),
                ("hThread", ctypes.c_void_p),
                ("lpBaseOfImage", ctypes.c_uint64),
                ("dwDebugInfoFileOffset", ctypes.c_uint),
                ("nDebugInfoSize", ctypes.c_uint),
                ("lpThreadLocalBase", ctypes.c_uint64),
                ("lpStartAddress", ctypes.c_uint64)]

class DEBUG_EVENT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("Exception", EXCEPTION_DEBUG_INFO),
                    ("CreateProcessInfo", CREATE_PROCESS_DEBUG_INFO),
                    ("raw", ctypes.c_ubyte * 160)]
    _anonymous_ = ("u",)
    _fields_ = [("dwDebugEventCode", ctypes.c_uint), ("dwProcessId", ctypes.c_uint),
                ("dwThreadId", ctypes.c_uint), ("u", _U)]

class STARTUPINFOA(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_uint), ("lpReserved", ctypes.c_char_p),
                ("lpDesktop", ctypes.c_char_p), ("lpTitle", ctypes.c_char_p),
                ("dwX", ctypes.c_uint), ("dwY", ctypes.c_uint),
                ("dwXSize", ctypes.c_uint), ("dwYSize", ctypes.c_uint),
                ("dwXCountChars", ctypes.c_uint), ("dwYCountChars", ctypes.c_uint),
                ("dwFillAttribute", ctypes.c_uint), ("dwFlags", ctypes.c_uint),
                ("wShowWindow", ctypes.c_ushort), ("cbReserved2", ctypes.c_ushort),
                ("lpReserved2", ctypes.c_void_p),
                ("hStdInput", ctypes.c_void_p), ("hStdOutput", ctypes.c_void_p),
                ("hStdError", ctypes.c_void_p)]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", ctypes.c_void_p), ("hThread", ctypes.c_void_p),
                ("dwProcessId", ctypes.c_uint), ("dwThreadId", ctypes.c_uint)]

class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_uint), ("cntUsage", ctypes.c_uint),
                ("th32ProcessID", ctypes.c_uint),
                ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                ("th32ModuleID", ctypes.c_uint), ("cntThreads", ctypes.c_uint),
                ("th32ParentProcessID", ctypes.c_uint), ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", ctypes.c_uint), ("szExeFile", ctypes.c_wchar * 260)]


def OpenThread(tid):
    THREAD_ALL_ACCESS = 0x1F03FF
    return k32.OpenThread(THREAD_ALL_ACCESS, False, tid)


def get_context(hthread):
    """A 64-bit host reading a WOW64 (32-bit) thread's context MUST use
    Wow64GetThreadContext with the 32-bit CONTEXT layout (empirically proven:
    the plain GetThreadContext route returns ERROR_NOACCESS 998 / zeroed data)."""
    ctx = CONTEXT_x86()
    ctx.ContextFlags = CONTEXT_FULL_X86
    if not k32.Wow64GetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"Wow64GetThreadContext failed: {ctypes.get_last_error()}")
    return ctx


def set_context(hthread, ctx):
    if not k32.Wow64SetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"Wow64SetThreadContext failed: {ctypes.get_last_error()}")


class CONTEXT64_DR(ctypes.Structure):
    """The x64 CONTEXT (debug-registers group only). The WOW64 thread's DR0-DR7
    are the REAL hardware debug registers (shared) — settable via the 64-bit
    SetThreadContext; the 32-bit VA fits zero-extended."""
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


def arm_hw_bps(hthread, addr0=None, addr1=None):
    """Set DR0/DR1 (execute, 1 byte) via the 64-bit CONTEXT route: the WOW64
    32-bit set path empirically ignores the debug-register group."""
    ctx = CONTEXT64_DR()
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"GetThreadContext(x64/DR) failed: {ctypes.get_last_error()}")
    if addr0:
        ctx.Dr0 = addr0
    if addr1:
        ctx.Dr1 = addr1
    ctx.Dr7 = 0x00000403 if (addr0 and addr1) else (0x00000401 if addr0 else 0x00000402)
    ctx.ContextFlags = CONTEXT_AMD64 | CONTEXT64_DEBUG_REGISTERS
    if not k32.SetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"SetThreadContext(x64/DR) failed: {ctypes.get_last_error()}")
    # verify through the 32-bit read (the authoritative check)
    c32 = get_context(hthread)
    return {"Dr0": c32.Dr0, "Dr7": c32.Dr7}


def cw_decode(cw):
    full = format(cw & 0xFFFF, "016b")
    pc_bits, rc_bits = full[6:8], full[4:6]
    pc = {"00": "24-bit single", "01": "reserved", "10": "53-bit double",
          "11": "64-bit extended"}[pc_bits]
    rc = {"00": "nearest-even", "01": "down", "10": "up", "11": "truncate"}[rc_bits]
    return {"pc_bits": pc_bits, "pc_decoded": pc, "rc_bits": rc_bits,
            "rc_decoded": rc, "exception_masks_bits": full[10:16],
            "cw_full_binary": full}


def pe_entry_and_base(path):
    """Read ImageBase + AddressOfEntryPoint from the PE32 header."""
    with open(path, "rb") as f:
        dos = f.read(0x40)
        e_lfanew = struct.unpack_from("<I", dos, 0x3C)[0]
        f.seek(e_lfanew)
        sig = f.read(4)
        assert sig == b"PE\0\0", "not a PE file"
        coff = f.read(20)
        machine = struct.unpack_from("<H", coff, 0)[0]
        assert machine == 0x14C, f"not a 32-bit PE (machine=0x{machine:04X})"
        opt_size = struct.unpack_from("<H", coff, 16)[0]
        opt = f.read(opt_size)
        magic = struct.unpack_from("<H", opt, 0)[0]
        assert magic == 0x10B, f"not PE32 optional header (magic=0x{magic:04X})"
        entry_rva = struct.unpack_from("<I", opt, 16)[0]
        image_base = struct.unpack_from("<I", opt, 28)[0]
    return image_base, entry_rva


def actual_main_base(hproc):
    """The loaded main-module base via EnumProcessModulesEx (32-bit modules)."""
    hMods = (ctypes.c_void_p * 1024)()
    cbNeeded = ctypes.c_uint()
    psapi = ctypes.WinDLL("psapi")
    ok = psapi.EnumProcessModulesEx(hproc, hMods, ctypes.sizeof(hMods),
                                    ctypes.byref(cbNeeded), LIST_MODULES_32BIT)
    if not ok:
        return None
    n = cbNeeded.value // ctypes.sizeof(ctypes.c_void_p)
    if n == 0:
        return None
    base = hMods[0] & 0xFFFFFFFF
    return base


def spawn(target, workdir):
    si = STARTUPINFOA()
    si.cb = ctypes.sizeof(si)
    pi = PROCESS_INFORMATION()
    cmdline = f'"{target}"'.encode()
    ok = k32.CreateProcessA(None, cmdline, None, None, False,
                           DEBUG_ONLY_THIS_PROCESS,
                           None, workdir.encode(), ctypes.byref(si), ctypes.byref(pi))
    if not ok:
        raise OSError(f"CreateProcess failed: {ctypes.get_last_error()}")
    return pi


def descendants(root_pid):
    """The process-tree census (for the orphan check)."""
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe = PROCESSENTRY32W()
    pe.dwSize = ctypes.sizeof(pe)
    procs = {}
    if k32.Process32FirstW(snap, ctypes.byref(pe)):
        while True:
            procs[pe.th32ProcessID] = (pe.th32ParentProcessID, pe.szExeFile)
            if not k32.Process32NextW(snap, ctypes.byref(pe)):
                break
    k32.CloseHandle(snap)
    # walk descendants
    desc, frontier = set(), {root_pid}
    while frontier:
        nxt = {p for p, (par, _) in procs.items() if par in frontier and p not in desc}
        desc |= nxt
        frontier = nxt
    return {p: procs[p][1] for p in desc if p in procs}


def jsonl_line(hit_index, attempt, site, bp_va, eip, pid, cw, method, ts):
    d = cw_decode(cw)
    return json.dumps({"hit_index": hit_index, "attempt": attempt, "site": site,
                       "bp_va": bp_va, "eip": f"0x{eip:08X}", "pid": pid,
                       "cw_hex": f"0x{cw & 0xFFFF:04X}", **d,
                       "capture_method": method, "screenshot": None,
                       "timestamp": ts}, ensure_ascii=False)


def run_session(target, workdir, outdir, sites, n_per_site, window_s, mode):
    """One full debug session. sites = {name: va}; returns the summary dict."""
    ts = lambda: datetime.now(timezone.utc).isoformat()
    image_base, entry_rva = pe_entry_and_base(target)
    pi = spawn(target, workdir)
    pid = pi.dwProcessId
    state = {"mode": mode, "target": target, "pid": pid,
             "pe_image_base": f"0x{image_base:08X}", "started_at": ts(),
             "events": [], "hits": {k: 0 for k in sites}, "lines": []}
    base = None
    hit_count = 0
    done = False
    t0 = time.monotonic()
    ev = DEBUG_EVENT()
    init_cw_done = False
    while not done:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 1000):
            if time.monotonic() - t0 > window_s:
                state["window_closed_by"] = "timeout_no_events"
                break
            continue
        code = ev.dwDebugEventCode
        if time.monotonic() - t0 > window_s:
            state["window_closed_by"] = "timeout"
            k32.TerminateProcess(pi.hProcess, 1)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)
            break
        if code == CREATE_PROCESS_DEBUG_EVENT:
            base = ev.CreateProcessInfo.lpBaseOfImage & 0xFFFFFFFF
            state["actual_base"] = f"0x{base:08X}" if base else "UNKNOWN"
            state["debug_event_start_address"] = f"0x{ev.CreateProcessInfo.lpStartAddress & 0xFFFFFFFF:08X}"
            delta = (base - image_base) if base else 0
            state["base_delta"] = f"0x{delta & 0xFFFFFFFF:08X}"
            state["base_relocated"] = bool(delta)
        elif code == EXCEPTION_DEBUG_EVENT:
            exr = ev.Exception.ExceptionRecord
            code_ex = exr.ExceptionCode & 0xFFFFFFFF
            eaddr = exr.ExceptionAddress & 0xFFFFFFFF
            ht = OpenThread(ev.dwThreadId)
            if code_ex == EXCEPTION_BREAKPOINT:
                # the initial breakpoint: the aux init-CW read (design W2.3)
                if not init_cw_done:
                    ctx = get_context(ht)
                    cw = ctx.FloatSave.ControlWord
                    state["init_cw_hex"] = f"0x{cw & 0xFFFF:04X}"
                    state["init_cw_decode"] = cw_decode(cw)
                    init_cw_done = True
                    # arm the hardware breakpoints (delta-shifted per S2)
                    d = (base - image_base) if base else 0
                    a = [(nm, (va + d) & 0xFFFFFFFF) for nm, va in sites.items()]
                    arm_hw_bps(ht, a[0][1] if len(a) > 0 else None,
                               a[1][1] if len(a) > 1 else None)
                    state["bp_addresses"] = {nm: f"0x{v:08X}" for nm, v in a}
                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)
                k32.CloseHandle(ht)
                continue
            elif code_ex == EXCEPTION_SINGLE_STEP and init_cw_done:
                ctx = get_context(ht)
                eip = ctx.Eip
                inv = {va + ((base - image_base) if base else 0): nm
                       for nm, va in sites.items()}
                if eip in inv:
                    nm = inv[eip]
                    cw = ctx.FloatSave.ControlWord
                    hit_count += 1
                    state["hits"][nm] += 1
                    line = jsonl_line(state["hits"][nm], 1, nm,
                                      state["bp_addresses"][nm], eip, pid,
                                      cw, "win32_context_read", ts())
                    state["lines"].append(line)
                    # raw context corpus
                    state["events"].append({
                        "hit": hit_count, "site": nm, "eip": f"0x{eip:08X}",
                        "ControlWord": f"0x{cw & 0xFFFF:04X}",
                        "StatusWord": f"0x{ctx.FloatSave.StatusWord & 0xFFFF:04X}",
                        "TagWord": f"0x{ctx.FloatSave.TagWord & 0xFFFF:04X}",
                        "Dr0": f"0x{ctx.Dr0:08X}", "Dr1": f"0x{ctx.Dr1:08X}",
                        "Dr6": f"0x{ctx.Dr6:08X}", "Dr7": f"0x{ctx.Dr7:08X}",
                        "EFlags": f"0x{ctx.EFlags:08X}"})
                    if all(v >= n_per_site for v in state["hits"].values()):
                        state["window_closed_by"] = "n_hits_captured"
                        k32.TerminateProcess(pi.hProcess, 0)
                        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)
                        k32.CloseHandle(ht)
                        done = True
                        continue
                    # our DR hit, series continuing: continue quietly
                    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)
                    k32.CloseHandle(ht)
                    continue
                else:
                    # a foreign single-step (the target's own trap-flag use):
                    # pass it through - never swallow the target's own exceptions
                    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId,
                                           DBG_EXCEPTION_NOT_HANDLED)
                    k32.CloseHandle(ht)
                    continue
            else:
                # not our event: let the app handle it (first-chance pass-through)
                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId,
                                       DBG_EXCEPTION_NOT_HANDLED)
                k32.CloseHandle(ht)
                continue
        elif code == EXIT_PROCESS_DEBUG_EVENT:
            state["window_closed_by"] = "target_exit"
            state["target_exit_recorded"] = True
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)
            break
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, DBG_CONTINUE)

    # ---- the independent exit proof (profile section 14) ----
    if not state.get("target_exit_recorded"):
        k32.TerminateProcess(pi.hProcess, 0)
    wh = ctypes.c_uint()
    k32.WaitForSingleObject(pi.hProcess, 10000)
    k32.GetExitCodeProcess(pi.hProcess, ctypes.byref(wh))
    state["exit_code"] = wh.value
    gone = k32.WaitForSingleObject(pi.hProcess, 0) == 0  # signaled => terminated
    state["process_gone"] = bool(gone)
    # ---- the orphan census (ACTIVE_ORPHANED check) ----
    desc = descendants(pid)
    alive = {}
    hp = k32.OpenProcess(0x1000, False, 0)  # PROCESS_QUERY_LIMITED_INFORMATION probe
    for cpid, name in desc.items():
        h = k32.OpenProcess(0x1000, False, cpid)
        if h:
            ec = ctypes.c_uint()
            k32.GetExitCodeProcess(h, ctypes.byref(ec))
            alive[cpid] = {"name": name, "exit_code": ec.value,
                           "alive": ec.value == 259}
            k32.CloseHandle(h)
    state["child_census"] = alive
    state["active_orphans"] = [f"{p}({v['name']})" for p, v in alive.items() if v["alive"]]
    state["finished_at"] = ts()
    k32.CloseHandle(pi.hProcess)
    k32.CloseHandle(pi.hThread)
    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["qualify", "measure"])
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--window-seconds", type=int, default=1800)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    out_jsonl = os.path.join(args.outdir, "cw_capture.jsonl")
    out_raw = os.path.join(args.outdir, "raw_context_log.jsonl")
    out_sess = os.path.join(args.outdir, "harness_session.json")

    if args.mode == "qualify":
        # 10 spawn-cycles against the synthetic target; DR0 at ImageBase+entry
        ib, entry = pe_entry_and_base(args.target)
        sites = {"SYNTHETIC_ENTRY": (ib + entry) & 0xFFFFFFFF}
        results = []
        for i in range(1, 11):
            st = run_session(args.target, args.workdir, args.outdir, sites,
                            1, min(args.window_seconds, 120), "qualify")
            ok = (st["hits"].get("SYNTHETIC_ENTRY", 0) >= 1
                  and st.get("init_cw_hex")
                  and st.get("process_gone")
                  and not st.get("active_orphans"))
            results.append({"cycle": i, "ok": ok,
                            "cw": st.get("init_cw_hex"),
                            "hits": st["hits"],
                            "exit_code": st.get("exit_code"),
                            "orphans": st.get("active_orphans")})
            with open(out_raw, "a", encoding="utf-8") as f:
                f.write(json.dumps(st) + "\n")
        passed = sum(1 for r in results if r["ok"])
        summary = {"mode": "qualify", "cycles": 10, "passed": passed,
                   "verdict": "QUALIFIED_10_10" if passed == 10 else
                              f"QUALIFICATION_FAILED_{passed}_of_10",
                   "results": results}
        with open(out_sess, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(json.dumps({"verdict": summary["verdict"], "passed": passed, "of": 10}))
        sys.exit(0 if passed == 10 else 1)

    # measure mode: the canon sites
    sites = {"FDIV_0x0098CE5A": 0x0098CE5A, "FLD_0x0095B2BC": 0x0095B2BC}
    st = run_session(args.target, args.workdir, args.outdir, sites, 10,
                     args.window_seconds, "measure")
    with open(out_jsonl, "a", encoding="utf-8") as f:
        for ln in st["lines"]:
            f.write(ln + "\n")
    with open(out_raw, "a", encoding="utf-8") as f:
        f.write(json.dumps(st) + "\n")
    complete = all(v >= 10 for v in st["hits"].values())
    st["verdict_status"] = ("CAPTURE_COMPLETE" if complete
                            else f"OPEN-INCOMPLETE_{json.dumps(st['hits'])}")
    with open(out_sess, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(json.dumps({"status": st["verdict_status"], "hits": st["hits"],
                      "window": st.get("window_closed_by"),
                      "orphans": st.get("active_orphans")}))
    sys.exit(0 if complete else 1)


if __name__ == "__main__":
    main()
