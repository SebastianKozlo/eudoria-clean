# -*- coding: utf-8 -*-
# p2_census.py - Phase 2 writer census.
# STATIC-ONLY. Own scan from the physical EXE:
#  (a) all direct CALL sites of FUN_004154F0 (manager getter);
#  (b) all direct reads of the singleton cell [0x00BA12E8];
#  (c) for each site, a post-site instruction window analyzed for writes to
#      [reg+0] / [reg+0x4C] / [reg+4] / [reg+0x50] / [reg+0x58] (manager fields);
#  (d) all direct CALL sites of FUN_00853A80 (Z provider consumers);
#  (e) all direct CALL sites of FUN_00755F90 (filter users).
# Raw scans are boundary-checked: each hit is disassembled from a window start
# and only instruction-aligned hits are counted (report includes raw count).

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
pe = core.PE(core.EXE_PATH)
md = Cs(CS_ARCH_X86, CS_MODE_32)

SINGLETON = 0x00BA12E8
GETTER = 0x004154F0
ZPROVIDER = 0x00853A80
FILTER = 0x00755F90


def text_off_of_va(va):
    return pe.text_va_to_off(va)


def va_of_text_off(off):
    return pe.text_va_start + off


def disasm_window(start_va, nbytes):
    b = pe.read_va(start_va, nbytes)
    out = []
    for ins in md.disasm(b, start_va):
        out.append((ins.address, ins.size, bytes(ins.bytes).hex(),
                    ins.mnemonic, ins.op_str))
    return out


def contains_at(text_off, pattern):
    return pe.text_raw[text_off:text_off + len(pattern)] == pattern


# --- (a) callers of FUN_004154F0 ----------------------------------------
call_sites = pe.calls_to(GETTER)
print("raw E8 sites targeting FUN_004154F0: %d" % len(call_sites))

# boundary-check: decode a window starting 32 bytes before each site and see
# whether the site VA appears as an instruction start
aligned = []
for off in call_sites:
    va = va_of_text_off(off)
    # try windows starting up to 16 bytes before
    ok = False
    for back in range(0, 17):
        w = disasm_window(va - back, back + 6)
        for (a, sz, hx, m, ops) in w:
            if a == va and m == "call":
                ok = True
                break
        if ok:
            break
    aligned.append({"va": hex(va), "aligned_call": ok})
n_aligned = sum(1 for a in aligned if a["aligned_call"])
print("instruction-aligned call sites: %d / %d" % (n_aligned, len(call_sites)))

# --- (b) singleton reads ------------------------------------------------
# encodings: A1 <addr32> (mov eax, moffs32); 8B 0D <addr32> (mov ecx, m);
# 8B 15 (mov edx), 8B 1D (mov ebx), 8B 2D (mov ebp), 8B 35 (mov esi),
# 8B 3D (mov edi)
pat_base = struct.pack("<I", SINGLETON)
patterns = {
    "mov eax, [0x00BA12E8]": b"\xA1" + pat_base,
    "mov ecx, [0x00BA12E8]": b"\x8B\x0D" + pat_base,
    "mov edx, [0x00BA12E8]": b"\x8B\x15" + pat_base,
    "mov ebx, [0x00BA12E8]": b"\x8B\x1D" + pat_base,
    "mov esi, [0x00BA12E8]": b"\x8B\x35" + pat_base,
    "mov edi, [0x00BA12E8]": b"\x8B\x3D" + pat_base,
    "cmp [0x00BA12E8], 0":  b"\x83\x3D" + pat_base + b"\x00",
    "mov [0x00BA12E8], eax": b"\xA3" + pat_base,
}
singleton_sites = {}
for name, pat in patterns.items():
    offs = pe.scan_text_bytes(pat)
    singleton_sites[name] = [hex(va_of_text_off(o)) for o in offs]
    print("singleton pattern %-24s: %d raw sites" % (name, len(offs)))

# --- (c) post-getter window write census --------------------------------
FIELD_WRITES = {}
# heuristic: for each aligned getter call site, decode 40 instructions after
# and record any "mov [reg], reg2" / "mov [reg+disp], reg2" (non-esp) where
# reg in {eax, ecx, edx, ebx, esi, edi} and the value flows from the call
# result (EAX). We record the write target offset.
for entry in aligned:
    if not entry["aligned_call"]:
        continue
    va = int(entry["va"], 16)
    w = disasm_window(va, 160)
    # find the call instruction, then track
    flow = []
    for (a, sz, hx, m, ops) in w:
        if m == "call":
            continue
        if m == "mov" and ops.startswith("dword ptr ["):
            # e.g. "dword ptr [eax], ecx" or "dword ptr [eax + 0x4c], edx"
            body = ops.split("]", 1)
            if len(body) == 2 and body[0].count("[") == 1:
                mem = body[0][body[0].index("[") + 1:].strip()
                src = body[1].strip().lstrip(",").strip()
                if mem.startswith("esp") or mem.startswith("ebp") or "+" in mem and mem.split("+")[0].strip() in ("esp", "ebp"):
                    continue
                base = mem.split("+")[0].strip()
                disp = 0
                if "+" in mem:
                    d = mem.split("+", 1)[1].strip().rstrip()
                    try:
                        disp = int(d, 16) if d.startswith("0x") else int(d)
                    except ValueError:
                        disp = -1
                flow.append({"at": hex(a), "base": base, "disp": disp,
                             "src": src})
    FIELD_WRITES[entry["va"]] = flow

# aggregate: writes with disp 0 / 0x4C / 0x50 / 0x58 / 4
interesting = {}
for site, flows in FIELD_WRITES.items():
    for fl in flows:
        if fl["disp"] in (0, 4, 0x4C, 0x50, 0x58):
            key = "disp_%s" % hex(fl["disp"])
            interesting.setdefault(key, []).append(
                {"site": site, "at": fl["at"], "base": fl["base"],
                 "src": fl["src"]})
print("\n--- post-getter writes to manager-like fields (heuristic) ---")
for k, v in sorted(interesting.items()):
    print("%s: %d sites" % (k, len(v)))
    for e in v[:60]:
        print("   getter@%s  write@%s  mov [%s%s], %s" %
              (e["site"], e["at"], e["base"],
               hex(e["disp"]) if e.get("disp") else "", e["src"]))

# --- (d) consumers of FUN_00853A80 --------------------------------------
z_sites = pe.calls_to(ZPROVIDER)
z_aligned = []
for off in z_sites:
    va = va_of_text_off(off)
    ok = False
    for back in range(0, 17):
        w = disasm_window(va - back, back + 6)
        for (a, sz, hx, m, ops) in w:
            if a == va and m == "call":
                ok = True
                break
        if ok:
            break
    z_aligned.append({"va": hex(va), "aligned": ok})
print("\nFUN_00853A80 raw E8 sites: %d; aligned: %d" % (
    len(z_sites), sum(1 for z in z_aligned if z["aligned"])))
for z in z_aligned:
    print("  %s aligned=%s" % (z["va"], z["aligned"]))

# --- (e) consumers of FUN_00755F90 --------------------------------------
f_sites = pe.calls_to(FILTER)
f_aligned = []
for off in f_sites:
    va = va_of_text_off(off)
    ok = False
    for back in range(0, 17):
        w = disasm_window(va - back, back + 6)
        for (a, sz, hx, m, ops) in w:
            if a == va and m == "call":
                ok = True
                break
        if ok:
            break
    f_aligned.append({"va": hex(va), "aligned": ok})
print("\nFUN_00755F90 raw E8 sites: %d; aligned: %d" % (
    len(f_sites), sum(1 for f in f_aligned if f["aligned"])))
for f in f_aligned:
    print("  %s aligned=%s" % (f["va"], f["aligned"]))

out = {
    "getter_call_sites": aligned,
    "singleton_sites": singleton_sites,
    "field_write_heuristic": {k: v for k, v in interesting.items()},
    "zprovider_sites": z_aligned,
    "filter_sites": f_aligned,
}
with open(os.path.join(RAW, "P2_CENSUS.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\nDONE -> 01_RAW/P2_CENSUS.json")
