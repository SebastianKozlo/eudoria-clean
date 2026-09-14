# -*- coding: utf-8 -*-
# p2_census4.py - two-level writer census.
# STATIC-ONLY. Level 1: at each getter (FUN_004154F0) call site, track the
# manager register; record calls where the tracked register is passed (push
# tracked / mov ecx,tracked / mov edx,tracked) to callee T. Level 2: decode
# each callee T and report writes to [reg+disp] (disp in {0,4,0x4C,0x50,0x58})
# where reg is a plausible manager alias (ecx at entry / propagated args).
# All hits reported with windows for manual verification.

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
DISPS = [0, 4, 0x4C, 0x50, 0x58]
REGS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "ebp")


def disasm(start_va, end_va):
    b = pe.read_va(start_va, min(end_va - start_va, 0x4000))
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
            endv, _ = pe.func_body(cand, maxb=0x4000)
            if endv and cand <= va < endv:
                w = disasm(cand, va + 8)
                if any(x[0] == va for x in w):
                    return cand, endv
    return None, None


# --- Level 1: collect callees receiving the manager ---------------------
callee_sites = {}  # callee_va -> list of (caller_site, caller_func)
for off in pe.calls_to(GETTER):
    site = pe.text_va_start + off
    fs, fe = func_bounds(site)
    if not fs:
        continue
    ins = disasm(fs, fe)
    idx = next((i for i, x in enumerate(ins) if x[0] == site), None)
    if idx is None:
        continue
    tracked = {"eax"}
    for (a, sz, hx, m, ops) in ins[idx + 1:]:
        if m == "mov":
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src in tracked and dst in REGS:
                tracked.add(dst)
            elif dst in tracked and dst != src:
                tracked.discard(dst)
        elif m == "push":
            val = ops.strip()
            if val in tracked:
                # find the following call target
                for (a2, s2, h2, m2, o2) in ins:
                    if a2 > a and m2 == "call" and a2 <= a + 0x20:
                        # parse target from o2 (capstone: "0x....")
                        try:
                            t = int(o2, 16)
                        except ValueError:
                            t = None
                        if t:
                            callee_sites.setdefault(t, []).append(
                                (hex(a), "%s..%s" % (hex(fs), hex(fe))))
                        break
        elif m == "mov" and ops.startswith("ecx, "):
            pass
        if m == "mov" and ops.split(",")[0].strip() == "ecx" and \
                ops.split(",")[1].strip() in tracked:
            for (a2, s2, h2, m2, o2) in ins:
                if a2 > a and m2 == "call" and a2 <= a + 0x10:
                    try:
                        t = int(o2, 16)
                    except ValueError:
                        t = None
                    if t:
                        callee_sites.setdefault(t, []).append(
                            (hex(a), "%s..%s" % (hex(fs), hex(fe))))
                    break
        if m == "call":
            tracked.discard("eax")

print("level-1: %d distinct callees receive the mgr pointer" % len(callee_sites))

# --- Level 2: scan each callee for manager-field writes -----------------
hits = []
for callee, callers in sorted(callee_sites.items()):
    fs, fe = func_bounds(callee)
    if not fs:
        continue
    ins = disasm(fs, fe)
    # track: ecx at entry = possible mgr (thiscall), arg1 at [esp+4] after
    # entry. Propagate movs.
    tracked = {"ecx"}
    local_writes = []
    for (a, sz, hx, m, ops) in ins:
        if m == "mov" and ops.startswith("dword ptr [") and "]" in ops:
            pos = ops.find("], ")
            if pos >= 0:
                mem = ops[:pos + 1].strip()
                if "esp" not in mem and "ebp" not in mem:
                    inner = mem[mem.index("[") + 1:mem.rindex("]")]
                    parts = [p.strip() for p in inner.split("+")]
                    base = parts[0]
                    disp = 0
                    if len(parts) > 1:
                        try:
                            disp = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
                        except ValueError:
                            disp = -99
                    if base in tracked and disp in DISPS:
                        local_writes.append({"at": hex(a), "mem": mem,
                                             "src": ops[pos + 3:].strip()})
        elif m == "mov":
            dst, _, src = ops.partition(", ")
            dst, src = dst.strip(), src.strip()
            if src in tracked and dst in REGS:
                tracked.add(dst)
            elif dst in tracked and dst != src:
                tracked.discard(dst)
        elif m == "call":
            tracked.discard("eax")
    if local_writes:
        hits.append({"callee": hex(callee), "bounds": "%s..%s" % (hex(fs), hex(fe)),
                     "callers": callers, "writes": local_writes})
        print("callee %s (%s..%s) callers=%d" % (hex(callee), hex(fs),
                                                 hex(fe), len(callers)))
        for w in local_writes:
            print("   WRITE %s <- %s @%s" % (w["mem"], w["src"], w["at"]))
        for c in callers[:6]:
            print("   from %s in %s" % c)

print("\nlevel-2 hits: %d" % len(hits))
with open(os.path.join(RAW, "P2_CENSUS4.json"), "w") as f:
    json.dump(hits, f, indent=1)
print("DONE -> 01_RAW/P2_CENSUS4.json")
