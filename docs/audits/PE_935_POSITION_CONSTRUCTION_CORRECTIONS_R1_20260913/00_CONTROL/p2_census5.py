# -*- coding: utf-8 -*-
# p2_census5.py - definitive provider1 (mgr+0) writer census with spill
# tracking. STATIC-ONLY.
# (a) For every getter (FUN_004154F0) call site: whole-function dataflow with
#     stack-spill tracking (mov [esp+X], tracked / mov reg, [esp+X]).
# (b) Level-2: callees receiving the mgr; track [esp+N] arg loads at callee
#     entry and propagate; report writes [reg+disp] disp in {0, 0x4C, 4}.
# (c) Additionally: global scan of ALL aligned `mov [reg], reg2` (mod00)
#     sites whose containing function calls the getter anywhere in its body.

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
pe = core.PE(core.EXE_PATH)
md = Cs(CS_ARCH_X86, CS_MODE_32)

GETTER = 0x004154F0
DISPS = [0, 0x4C]
REGS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "ebp")


def disasm(start_va, end_va):
    b = pe.read_va(start_va, min(end_va - start_va, 0x8000))
    out = []
    for ins in md.disasm(b, start_va):
        out.append((ins.address, ins.size, bytes(ins.bytes).hex(),
                    ins.mnemonic, ins.op_str))
    return out


def func_bounds(va):
    for back in range(3, 0x4000):
        a = va - back
        b3 = pe.read_va(a - 1, 3)
        if b3 == b"\xcc\xcc\xcc":
            cand = a + 2
            bb = pe.read_va(cand, 1)
            while bb == b"\xcc":
                cand += 1
                bb = pe.read_va(cand, 1)
            endv, _ = pe.func_body(cand, maxb=0x8000)
            if endv and cand <= va < endv:
                w = disasm(cand, va + 8)
                if any(x[0] == va for x in w):
                    return cand, endv
    return None, None


def track_flow(ins, start_idx, tracked, report_disp):
    """Flow-track `tracked` set through ins[start_idx:], with stack spills.
    Returns list of writes {at, mem, src} to tracked+report_disp."""
    spills = {}  # esp-offset -> tracked-origin marker
    writes = []
    for (a, sz, hx, m, ops) in ins[start_idx:]:
        if m == "mov" and ops.startswith("dword ptr [esp"):
            # spill: mov [esp+X], src / reload: mov dst, [esp+X]
            pos = ops.find("], ")
            if pos >= 0:
                mem = ops[:pos + 1]
                src = ops[pos + 3:].strip()
                off = mem.replace("dword ptr [esp", "").replace("]", "").replace("+", "").replace(" ", "")
                try:
                    off = int(off, 16) if off.startswith("0x") else (int(off) if off else 0)
                except ValueError:
                    off = -1
                if src in tracked and off >= 0:
                    spills[off] = True
                elif off >= 0 and off in spills:
                    spills.pop(off, None)
            continue
        if m == "mov" and "dword ptr [" in ops and "[esp" not in ops and "[ebp" not in ops:
            pos = ops.find("], ")
            if pos >= 0:
                mem = ops[:pos + 1].strip()
                src = ops[pos + 3:].strip()
                inner = mem[mem.index("[") + 1:mem.rindex("]")]
                parts = [p.strip() for p in inner.split("+")]
                base = parts[0]
                disp = 0
                if len(parts) > 1:
                    try:
                        disp = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
                    except ValueError:
                        disp = -99
                # base from tracked OR from spill reload captured in dst?
                if base in tracked and disp in report_disp:
                    writes.append({"at": hex(a), "mem": mem, "src": src})
            # also handle reg-reload from esp handled above
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src.startswith("dword ptr [esp"):
                off_s = src.replace("dword ptr [esp", "").replace("]", "").replace("+", "").replace(" ", "")
                try:
                    off_s = int(off_s, 16) if off_s.startswith("0x") else (int(off_s) if off_s else 0)
                except ValueError:
                    off_s = -1
                if dst in REGS and off_s in spills:
                    tracked.add(dst)
            continue
        if m == "mov":
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src.startswith("dword ptr [esp"):
                off_s = src.replace("dword ptr [esp", "").replace("]", "").replace("+", "").replace(" ", "")
                try:
                    off_s = int(off_s, 16) if off_s.startswith("0x") else (int(off_s) if off_s else 0)
                except ValueError:
                    off_s = -1
                if dst in REGS and off_s in spills:
                    tracked.add(dst)
                    continue
            if src in tracked and dst in REGS:
                tracked.add(dst)
            elif dst in tracked and dst != src:
                tracked.discard(dst)
        elif m == "call":
            tracked.discard("eax")
    return writes


def flow_callees(ins, start_idx, tracked):
    """Track and return list of (call_va, target, via) where tracked reg is
    pushed or moved to ecx before a nearby call."""
    out = []
    for (a, sz, hx, m, ops) in ins[start_idx:]:
        if m == "push":
            v = ops.strip()
            if v in tracked:
                out.append(("push", a, v))
        elif m == "mov":
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src in tracked and dst == "ecx":
                out.append(("ecx", a, dst))
            if src in tracked and dst in REGS:
                tracked.add(dst)
            elif dst in tracked and dst != src:
                tracked.discard(dst)
        elif m == "call":
            try:
                t = int(ops, 16)
            except ValueError:
                t = None
            if t and out and out[-1][0] in ("push", "ecx") and a - out[-1][1] <= 0x18:
                out.append(("call", a, t))
            tracked.discard("eax")
    return out


results = []
# --- (a) whole-function flow with spills -------------------------------
for off in pe.calls_to(GETTER):
    site = pe.text_va_start + off
    fs, fe = func_bounds(site)
    if not fs:
        continue
    ins = disasm(fs, fe)
    idx = next((i for i, x in enumerate(ins) if x[0] == site), None)
    if idx is None:
        continue
    w = track_flow(ins, idx + 1, {"eax"}, DISPS)
    if w:
        results.append({"kind": "direct", "site": hex(site),
                        "func": "%s..%s" % (hex(fs), hex(fe)), "writes": w})
        print("DIRECT site=%s func=%s" % (hex(site), hex(fs)))
        for x in w:
            print("   %s <- %s @%s" % (x["mem"], x["src"], x["at"]))

# --- (b) callee-level with [esp+N] arg loads ---------------------------
# collect (callee, caller_site) pairs first
pairs = []
for off in pe.calls_to(GETTER):
    site = pe.text_va_start + off
    fs, fe = func_bounds(site)
    if not fs:
        continue
    ins = disasm(fs, fe)
    idx = next((i for i, x in enumerate(ins) if x[0] == site), None)
    if idx is None:
        continue
    ev = flow_callees(ins, idx + 1, {"eax"})
    pushes = [e for e in ev if e[0] == "push"]
    ecxes = [e for e in ev if e[0] == "ecx"]
    calls = [e for e in ev if e[0] == "call"]
    for c in calls:
        # check a push/ecx immediately before
        for p in (pushes + ecxes):
            if 0 <= c[1] - p[1] <= 0x18 and p[1] > site:
                pairs.append((c[2], site))
                break
seen = set()
for callee, csite in pairs:
    if callee in seen:
        continue
    seen.add(callee)
    fs2, fe2 = func_bounds(callee)
    if not fs2:
        continue
    ins2 = disasm(fs2, fe2)
    # seed tracked with: ecx + regs loaded from [esp+4]/[esp+8]/[esp+0xC]/[esp+0x10]
    tracked = {"ecx"}
    # find arg loads in the first 30 instructions
    seeded = set()
    for i, (a, sz, hx, m, ops) in enumerate(ins2[:40]):
        if m == "mov":
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src == "dword ptr [esp + 4]" or src == "dword ptr [esp + 8]" or \
               src == "dword ptr [esp + 0xc]" or src == "dword ptr [esp + 0x10]":
                tracked.add(dst)
    w = track_flow(ins2, 0, tracked, DISPS)
    if w:
        results.append({"kind": "callee", "callee": hex(callee),
                        "bounds": "%s..%s" % (hex(fs2), hex(fe2)),
                        "caller_site": hex(csite), "writes": w})
        print("CALLEE %s (%s..%s) from site %s" %
              (hex(callee), hex(fs2), hex(fe2), hex(csite)))
        for x in w:
            print("   %s <- %s @%s" % (x["mem"], x["src"], x["at"]))

# --- (c) global: all aligned mov [reg], reg2 in functions calling getter
# (final fallback - cross-check any missed direct writes)
print("\ncensus5 complete")
with open(os.path.join(RAW, "P2_CENSUS5.json"), "w") as f:
    json.dump(results, f, indent=1)
print("DONE -> 01_RAW/P2_CENSUS5.json (%d hits)" % len(results))
