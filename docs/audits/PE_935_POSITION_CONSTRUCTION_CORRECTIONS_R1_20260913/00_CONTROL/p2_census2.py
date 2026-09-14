# -*- coding: utf-8 -*-
# p2_census2.py - full-function dataflow writer census.
# STATIC-ONLY. For every aligned call site of FUN_004154F0 (mgr1 getter) and
# FUN_00415570 (mgr2 getter): decode the containing function, track register
# flow of the returned pointer (EAX -> mov rX,eax -> mov rY,rX), and report any
# memory writes [rX+disp] / [rX] with disp in {0,4,0x4C,0x50,0x58,0x54,0x44,0x48}
# through tracked registers. This is a heuristic census: hits need manual
# verification against the disassembly (reported with VA windows).

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

GETTERS = [0x004154F0, 0x00415570]
TRACKED_DISPS = [0, 4, 0x44, 0x48, 0x4C, 0x50, 0x54, 0x58]


def func_range(va):
    end, _ = pe.func_body(va, maxb=0x3000)
    return end


def disasm_full(start_va, end_va):
    b = pe.read_va(start_va, end_va - start_va)
    out = []
    for ins in md.disasm(b, start_va):
        out.append((ins.address, ins.size, bytes(ins.bytes).hex(),
                    ins.mnemonic, ins.op_str))
    return out


results = []
for getter in GETTERS:
    sites = pe.calls_to(getter)
    for off in sites:
        site_va = pe.text_va_start + off
        # function start heuristic: walk back to CC CC CC preceded boundary
        start_va = site_va
        max_back = 0x4000
        found_start = None
        # find a CC CC CC run before site and take the byte after it
        back_va = site_va
        for back in range(3, max_back):
            a = site_va - back
            b3 = pe.read_va(a - 1, 3)
            if b3 == b"\xcc\xcc\xcc":
                # candidate start = a+2 (skip the CC run; find first non-CC)
                cand = a + 2
                bb = pe.read_va(cand, 1)
                while bb == b"\xcc":
                    cand += 1
                    bb = pe.read_va(cand, 1)
                # verify: decoding from cand reaches site_va exactly
                endv = func_range(cand)
                if endv and cand <= site_va < endv:
                    # check the site is instruction-aligned from cand
                    w = disasm_full(cand, site_va + 8)
                    if any(x[0] == site_va for x in w):
                        found_start = cand
                        break
        if found_start is None:
            continue
        end_va = func_range(found_start)
        if not end_va:
            continue
        ins = disasm_full(found_start, end_va)
        # locate the call site index
        idx = None
        for i, x in enumerate(ins):
            if x[0] == site_va:
                idx = i
                break
        if idx is None:
            continue
        # dataflow track from call result
        tracked = {"eax"}  # registers possibly holding mgr
        hits = []
        for (a, sz, hx, m, ops) in ins[idx + 1:]:
            if m == "mov" and ops.startswith("dword ptr ["):
                pos = ops.find("], ")
                if pos < 0:
                    continue
                mem = ops[:pos + 1].strip()
                src = ops[pos + 3:].strip()
                if "esp" in mem or "ebp" in mem:
                    pass
                else:
                    inner = mem[mem.index("[") + 1:mem.rindex("]")]
                    parts = [p.strip() for p in inner.split("+")]
                    base = parts[0] if parts else ""
                    disp = 0
                    if len(parts) > 1:
                        try:
                            disp = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
                        except ValueError:
                            disp = -99
                    if base in tracked and disp in TRACKED_DISPS:
                        hits.append({"at": hex(a), "mem": mem, "src": src,
                                     "disp": disp})
            elif m == "mov":
                # mov dst, src -- track propagation
                dst, _, src = ops.partition(", ")
                dst = dst.strip()
                src = src.strip()
                if src in tracked and dst in ("eax", "ebx", "ecx", "edx",
                                             "esi", "edi"):
                    tracked.add(dst)
                elif dst in tracked and dst != src:
                    # dst overwritten by non-tracked value
                    tracked.discard(dst)
            elif m in ("call",):
                # EAX clobbered by call
                tracked.discard("eax")
        if hits:
            results.append({
                "getter": hex(getter), "site": hex(site_va),
                "func_start": hex(found_start), "func_end": hex(end_va),
                "hits": hits,
            })
            print("getter@%s func %s..%s" % (hex(site_va), hex(found_start),
                                             hex(end_va)))
            for h in hits:
                print("   WRITE %s <- %s @%s (disp=%s)" %
                      (h["mem"], h["src"], h["at"], hex(h["disp"])))

with open(os.path.join(RAW, "P2_CENSUS2.json"), "w") as f:
    json.dump(results, f, indent=1)
print("DONE -> 01_RAW/P2_CENSUS2.json (%d functions with hits)" % len(results))
