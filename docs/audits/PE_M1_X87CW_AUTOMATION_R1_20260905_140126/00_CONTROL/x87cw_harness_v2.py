#!/usr/bin/env python3
"""x87cw_harness_v2.py — the Win32 debug harness, SECOND REVISION, built from
the empirically-proven facts of the diag1-4 series:
  FACT1: the 32-bit CW/EIP read = Wow64GetThreadContext (the plain GetThreadContext
         from the 64-bit host = ERROR_NOACCESS/garbage).
  FACT2: the DR set = the 64-bit CONTEXT route (the WOW64 32-bit set ignores the DR group).
  FACT3: the DR trap DOES fire (DR6.B0=1) and is delivered (observed) as a first-chance
         exception whose ExceptionAddress == the armed VA (the delivery code varied:
         0x80000004 / 0x4000001e observed) -> the hit discriminator = the ADDRESS,
         not the exception code.
  FACT4: arming at the initial breakpoint has a timing race vs the entry (diag4: an
         armed run with no trap events) -> ARM AT CREATE_PROCESS (the earliest possible;
         the main thread handle from the event).
  FACT5: after a hit, continuing with DBG_CONTINUE without clearing the trap state
         re-traps the same instruction (the diag3 storm) -> set RF (Resume Flag) in
         EFLAGS + clear DR6, verified; the fallback = disarm-singlestep-rearm.
The observation contract: DR registers + context reads only. ZERO target-code
execution, ZERO memory writes, ZERO code patches.
"""
import argparse
import ctypes
import json
import os
import sys
import time
from datetime import datetime, timezone

spec_dir = os.path.dirname(os.path.abspath(__file__))
import importlib.util
_h = importlib.util.spec_from_file_location("h", os.path.join(spec_dir, "x87cw_harness.py"))
H = importlib.util.module_from_spec(_h)
_h.loader.exec_module(H)
k32 = H.k32

RF = 0x00010000  # EFLAGS Resume Flag


def x64_write(hthread, dr0=None, dr1=None, dr7=None, eflags_or=None, clear_dr6=False):
    """The 64-bit-context write route (FACT2)."""
    ctx = H.CONTEXT64_DR()
    ctx.ContextFlags = H.CONTEXT_AMD64 | H.CONTEXT64_DEBUG_REGISTERS
    if not k32.GetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"x64Get(DR) failed: {ctypes.get_last_error()}")
    if dr0 is not None:
        ctx.Dr0 = dr0
    if dr1 is not None:
        ctx.Dr1 = dr1
    if dr7 is not None:
        ctx.Dr7 = dr7
    if clear_dr6:
        ctx.Dr6 = 0
    ctx.ContextFlags = H.CONTEXT_AMD64 | H.CONTEXT64_DEBUG_REGISTERS
    if not k32.SetThreadContext(hthread, ctypes.byref(ctx)):
        raise OSError(f"x64Set(DR) failed: {ctypes.get_last_error()}")


def set_resume_flag(hthread):
    """RF via the 32-bit context (verified by readback; the fallback = disarm)."""
    c = H.get_context(hthread)
    c.EFlags |= RF
    H.set_context(hthread, c)
    v = H.get_context(hthread)
    return bool(v.EFlags & RF)


def run_session(target, workdir, sites, n_per_site, window_s, mode, out_state):
    ts = lambda: datetime.now(timezone.utc).isoformat()
    image_base, entry_rva = H.pe_entry_and_base(target)
    pi = H.spawn(target, workdir)
    pid = pi.dwProcessId
    st = {"mode": mode, "target": target, "pid": pid, "started_at": ts(),
          "pe_image_base": f"0x{image_base:08X}",
          "hits": {nm: 0 for nm, _ in sites}, "lines": [], "events": [],
          "exception_census": {}}
    base = None
    armed_vas = {}
    done = False
    armed = False
    init_cw_done = False
    t0 = time.monotonic()
    ev = H.DEBUG_EVENT()
    while not done:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 1000):
            if time.monotonic() - t0 > window_s:
                st["window_closed_by"] = "timeout_no_events"
                break
            continue
        if time.monotonic() - t0 > window_s:
            st["window_closed_by"] = "timeout"
            k32.TerminateProcess(pi.hProcess, 1)
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, H.DBG_CONTINUE)
            break
        code = ev.dwDebugEventCode
        cont = H.DBG_CONTINUE
        if code == 3:  # CREATE_PROCESS: base + the EARLIEST arming (FACT4)
            base = ev.CreateProcessInfo.lpBaseOfImage & 0xFFFFFFFF
            delta = base - image_base
            st["actual_base"] = f"0x{base:08X}"
            st["base_relocated"] = bool(delta)
            st["debug_event_start_address"] = f"0x{ev.CreateProcessInfo.lpStartAddress & 0xFFFFFFFF:08X}"
            ht = ev.CreateProcessInfo.hThread
            if ht:
                x64_write(ctypes.c_void_p(ht),
                          dr0=(sites[0][1] + delta) & 0xFFFFFFFF if len(sites) > 0 else None,
                          dr1=(sites[1][1] + delta) & 0xFFFFFFFF if len(sites) > 1 else None,
                          dr7=0x00000403 if len(sites) > 1 else 0x00000401,
                          clear_dr6=True)
                armed_vas = {(v + delta) & 0xFFFFFFFF: nm for nm, v in sites}
                st["bp_addresses"] = {nm: f"0x{v:08X}" for v, nm in armed_vas.items()}
                armed = True
        elif code == 1:
            exr = ev.Exception.ExceptionRecord
            xc = exr.ExceptionCode & 0xFFFFFFFF
            xa = exr.ExceptionAddress & 0xFFFFFFFF
            st["exception_census"][f"0x{xc:08X}"] = \
                st["exception_census"].get(f"0x{xc:08X}", 0) + 1
            ht = H.OpenThread(ev.dwThreadId)
            if xc == H.EXCEPTION_BREAKPOINT and not init_cw_done:
                c = H.get_context(ht)
                cw = c.FloatSave.ControlWord
                st["init_cw_hex"] = f"0x{cw & 0xFFFF:04X}"
                st["init_cw_decode"] = H.cw_decode(cw)
                init_cw_done = True
                cont = H.DBG_CONTINUE
            elif armed and (xa in armed_vas):
                c = H.get_context(ht)
                eip = c.Eip
                if eip in armed_vas:  # the authoritative EIP match
                    nm = armed_vas[eip]
                    cw = c.FloatSave.ControlWord
                    st["hits"][nm] += 1
                    line = H.jsonl_line(st["hits"][nm], 1, nm,
                                        st["bp_addresses"][nm], eip, pid,
                                        cw, "win32_context_read", ts())
                    st["lines"].append(line)
                    st["events"].append({
                        "hit": st["hits"][nm], "site": nm, "eip": f"0x{eip:08X}",
                        "ControlWord": f"0x{cw & 0xFFFF:04X}",
                        "Dr6_before_clear": None, "exception_code": f"0x{xc:08X}",
                        "first_chance": ev.Exception.dwFirstChance})
                    # FACT5: skip the re-trap: RF + DR6 clear; the fallback = disarm
                    rf_ok = set_resume_flag(ht)
                    x64_write(ht, clear_dr6=True)
                    if not rf_ok:
                        # the disarm fallback: L0/L1 off now; the single-step
                        # over happens naturally on continue (the instruction
                        # executes once), then re-arm at the next debug event
                        x64_write(ht, dr7=0x0)
                        st.setdefault("rf_fallbacks", []).append(st["hits"][nm])
                    if all(v >= n_per_site for v in st["hits"].values()):
                        st["window_closed_by"] = "n_hits_captured"
                        k32.TerminateProcess(pi.hProcess, 0)
                        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, H.DBG_CONTINUE)
                        k32.CloseHandle(ht)
                        done = True
                        continue
                    cont = H.DBG_CONTINUE
                else:
                    # the ExceptionAddress matches but EIP does not: a curiosity
                    # (the wow64 stub address); pass through NOT_HANDLED
                    cont = H.DBG_EXCEPTION_NOT_HANDLED
            else:
                cont = H.DBG_EXCEPTION_NOT_HANDLED
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)
            k32.CloseHandle(ht)
            continue
        elif code == 5:
            st["window_closed_by"] = "target_exit"
            st["target_exit_recorded"] = True
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, H.DBG_CONTINUE)

    # ---- drain the debug events so the termination can complete (the debug
    # port holds the process until the debugger consumes the EXIT event) ----
    t_drain = time.monotonic()
    while time.monotonic() - t_drain < 5:
        if not k32.WaitForDebugEvent(ctypes.byref(ev), 500):
            continue
        if ev.dwDebugEventCode == 5:
            st["drained_exit_event"] = True
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, H.DBG_CONTINUE)
            break
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, H.DBG_CONTINUE)

    # ---- the independent exit proof ----
    if not st.get("target_exit_recorded"):
        k32.TerminateProcess(pi.hProcess, 0)
    wh = ctypes.c_uint()
    k32.WaitForSingleObject(pi.hProcess, 10000)
    k32.GetExitCodeProcess(pi.hProcess, ctypes.byref(wh))
    st["exit_code"] = wh.value
    st["process_gone"] = bool(k32.WaitForSingleObject(pi.hProcess, 0) == 0)
    desc = H.descendants(pid)
    alive = {}
    for cpid, name in desc.items():
        h = k32.OpenProcess(0x1000, False, cpid)
        if h:
            ec = ctypes.c_uint()
            k32.GetExitCodeProcess(h, ctypes.byref(ec))
            alive[cpid] = {"name": name, "exit_code": ec.value,
                           "alive": ec.value == 259}
            k32.CloseHandle(h)
    st["child_census"] = alive
    st["active_orphans"] = [f"{p}({v['name']})" for p, v in alive.items() if v["alive"]]
    st["finished_at"] = ts()
    k32.CloseHandle(pi.hProcess)
    k32.CloseHandle(pi.hThread)
    out_state.update(st)
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["qualify", "measure"])
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--window-seconds", type=int, default=1800)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    out_jsonl = os.path.join(a.outdir, "cw_capture.jsonl")
    out_raw = os.path.join(a.outdir, "raw_context_log.jsonl")
    out_sess = os.path.join(a.outdir, "harness_session.json")

    if a.mode == "qualify":
        results = []
        sites = [("SYNTHETIC_ENTRY", None)]  # the entry VA computed per cycle from the base
        for i in range(1, 11):
            ib, entry_rva = H.pe_entry_and_base(a.target)
            st = {}
            run_session(a.target, a.workdir,
                        [("SYNTHETIC_ENTRY", (ib + entry_rva) & 0xFFFFFFFF)],
                        1, min(a.window_seconds, 90), "qualify", st)
            ok = (st["hits"].get("SYNTHETIC_ENTRY", 0) >= 1
                  and st.get("init_cw_hex")
                  and st.get("process_gone")
                  and not st.get("active_orphans"))
            results.append({"cycle": i, "ok": ok, "cw": st.get("init_cw_hex"),
                            "hit_cw": [l for l in st.get("lines", [])][:1],
                            "hits": st["hits"], "exit_code": st.get("exit_code"),
                            "orphans": st.get("active_orphans"),
                            "window": st.get("window_closed_by"),
                            "base": st.get("actual_base")})
            with open(out_raw, "a", encoding="utf-8") as f:
                f.write(json.dumps(st) + "\n")
        passed = sum(1 for r in results if r["ok"])
        verdict = "QUALIFIED_10_10" if passed == 10 else f"QUALIFICATION_FAILED_{passed}_of_10"
        summary = {"mode": "qualify", "cycles": 10, "passed": passed,
                   "verdict": verdict, "results": results}
        with open(out_sess, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(json.dumps({"verdict": verdict, "passed": passed, "of": 10}))
        sys.exit(0 if passed == 10 else 1)

    sites = [("FDIV_0x0098CE5A", 0x0098CE5A), ("FLD_0x0095B2BC", 0x0095B2BC)]
    st = {}
    run_session(a.target, a.workdir, sites, 10, a.window_seconds, "measure", st)
    with open(out_jsonl, "a", encoding="utf-8") as f:
        for ln in st["lines"]:
            f.write(ln + "\n")
    with open(out_raw, "a", encoding="utf-8") as f:
        f.write(json.dumps(st) + "\n")
    complete = all(v >= 10 for v in st["hits"].values())
    st["verdict_status"] = ("CAPTURE_COMPLETE" if complete else
                            f"OPEN-INCOMPLETE_{json.dumps(st['hits'])}")
    with open(out_sess, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(json.dumps({"status": st["verdict_status"], "hits": st["hits"],
                      "window": st.get("window_closed_by"),
                      "orphans": st.get("active_orphans")}))
    sys.exit(0 if complete else 1)


if __name__ == "__main__":
    main()
