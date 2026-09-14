# -*- coding: utf-8 -*-
# p2_census3.py - setter-method census.
# STATIC-ONLY. Scans .text for aligned `mov [reg+0x4C], reg2` and
# `mov [reg], reg2` (candidate manager setters), decodes the containing
# function, and reports those whose body looks like a small setter (<= 0x40
# bytes, writes the arg/derived value at +0 or +0x4C). Then finds callers of
# each setter and checks for the manager-getter + ECX pattern.
# Heuristic census - hits require manual verification (windows provided).

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

# MOV r/m32, r32 = 89 /r. [reg+0x4C]: ModRM = mod01, reg<<3, rm:
# eax(0):89 41 4C, ecx(1):89 49 4C, edx(2):89 51 4C, ebx(3):89 59 4C,
# ebp(5):89 6D 4C, esi(6):89 75 4C, edi(7):89 7D 4C
# (esp/ebp need SIB/disp forms; ebp uses 6D).
PATTERNS_4C = [b"\x89\x41\x4c", b"\x89\x49\x4c", b"\x89\x51\x4c",
               b"\x89\x59\x4c", b"\x89\x6d\x4c", b"\x89\x75\x4c",
               b"\x89\x7d\x4c"]
# MOV [reg], reg2 (mod00): eax:89 01, ecx:89 09, edx:89 11, ebx:89 19,
# ebp:89 2D (moffs! different), esi:89 06, edi:89 07
PATTERNS_0 = [b"\x89\x01", b"\x89\x09", b"\x89\x11", b"\x89\x19",
              b"\x89\x06", b"\x89\x07"]


def disasm_window(start_va, nbytes):
    b = pe.read_va(start_va, nbytes)
    out = []
    for ins in md.disasm(b, start_va):
        out.append((ins.address, ins.size, bytes(ins.bytes).hex(),
                    ins.mnemonic, ins.op_str))
    return out


def func_start_and_end(va):
    """Walk back to a CC CC CC boundary and validate."""
    for back in range(3, 0x4000):
        a = va - back
        b3 = pe.read_va(a - 1, 3)
        if b3 == b"\xcc\xcc\xcc":
            cand = a + 2
            bb = pe.read_va(cand, 1)
            while bb == b"\xcc":
                cand += 1
                bb = pe.read_va(cand, 1)
            endv, _ = pe.func_body(cand, maxb=0x3000)
            if endv and cand <= va < endv:
                w = disasm_window(cand, va - cand + 8)
                if any(x[0] == va for x in w):
                    return cand, endv
    return None, None


def find_func(va):
    cands = []
    for back in range(3, 0x4000):
        a = va - back
        b3 = pe.read_va(a - 1, 3)
        if b3 == b"\xcc\xcc\xcc":
            cand = a + 2
            bb = pe.read_va(cand, 1)
            while bb == b"\xcc":
                cand += 1
                bb = pe.read_va(cand, 1)
            endv, _ = pe.func_body(cand, maxb=0x3000)
            if endv and cand <= va < endv:
                w = disasm_window(cand, va - cand + 8)
                if any(x[0] == va for x in w):
                    cands.append((cand, endv))
    return cands


report = []
seen_4c = set()
for pat in PATTERNS_4C:
    for off in pe.scan_text_bytes(pat):
        va = pe.text_va_start + off
        if va in seen_4c:
            continue
        seen_4c.add(va)
        cands = find_func(va)
        for (fs, fe) in cands:
            size = fe - fs
            if size <= 0x60:  # small setter-like
                w = disasm_window(fs, size)
                txt = "\n".join("%08X %-8s %s" % (a, m, o) for (a, s, hx, m, o) in w)
                report.append({"kind": "mov [r+0x4C],r", "va": hex(va),
                               "func": "%s..%s" % (hex(fs), hex(fe)),
                               "size": size, "disasm": txt})
                print("0x4C-write @%s in %s..%s (%d B)" % (hex(va), hex(fs),
                                                          hex(fe), size))
                print(txt)
                print("---")

print("0x4C aligned small-function candidates: %d" % len(report))
with open(os.path.join(RAW, "P2_CENSUS3_4C.json"), "w") as f:
    json.dump(report, f, indent=1)
print("DONE -> 01_RAW/P2_CENSUS3_4C.json")
