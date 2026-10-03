#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC_DERIVE2 — targeted falsification probes for fresh QC of
PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z.

Probe targets (each answers a specific attempt-to-break question):
  P1  callback 0x008BD720: is it byte-pinned ANYWHERE in .text as an imm32
      (PUSH 68 imm32 / MOV B8+r imm32 / MOV [esp+d] C7 44 24 imm32)? Where?
  P2  reader FUN_0072FA30: who references it? E8 CALL, E9 JMP, any imm32
      reference in .text (function-table entry)?
  P3  dispatcher FUN_004B18D0: which immediates 0xA2..0xC7 appear in a
      WIDER window (0x004B18D0..+0x2000), incl. SUB forms (2D/83 E8)?
  P4  scene root: is "NetImmerseScene::Root" VA 0x00A972FC pushed near
      SetName callsites 0x009331CD / 0x0093338F? new(0x118)+ctor at R17?
  P5  emitter tail: bytes 0x006C3F50..0x006C4120 decoded scan for
      scheduler call & callback imm32.
  P6  FUN_006C3640: prologue + first calls (scheduler candidate).
  P7  ID2 arrays of Z08/Z09 (FUN_006C3FE0/FUN_006C4020/FUN_006C4060):
      dump 0x006C3FE0..0x006C4120 to see the emitter array callers.
"""

import struct
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = os.path.join(PKG, "07_QC", "raw", "QC_DERIVATIONS2.json")

R = {"p1_callback_refs": [], "p2_reader_refs": [], "p3_dispatcher": [],
     "p4_scene_root": {}, "p5_emitter_tail": "", "p6_sched_3640": "",
     "p7_array_callers": "", "errors": []}

data = open(EXE, "rb").read()
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
nsec, = struct.unpack_from("<H", data, e_lfanew + 6)
secs = []
so = e_lfanew + 24 + opt_size
for i in range(nsec):
    o = so + i * 40
    vsz, vaddr, rsz, rptr = struct.unpack_from("<4I", data, o + 8)
    secs.append((data[o:o + 8].rstrip(b"\0").decode(), vaddr, rsz, rptr))


def va2fo(va):
    rva = va - image_base
    for (nm, vaddr, rsz, rptr) in secs:
        if vaddr <= rva < vaddr + rsz:
            return rptr + (rva - vaddr)
    return None


def fo2va(fo):
    for (nm, vaddr, rsz, rptr) in secs:
        if rptr <= fo < rptr + rsz:
            return image_base + vaddr + (fo - rptr)
    return None


def hx(b):
    return " ".join("%02X" % c for c in b)


text = None
for s in secs:
    if s[0] == ".text":
        text = s
nm, vaddr, rsz, rptr = text
base_va = image_base + vaddr
seg = data[rptr:rptr + rsz]

# ---- P1: any imm32 == 0x008BD720 in .text
needle = struct.pack("<I", 0x008BD720)
i = seg.find(needle)
while i >= 0:
    va = base_va + i
    ctx = seg[max(0, i - 4):i + 8]
    R["p1_callback_refs"].append({"va_of_imm32": "0x%08X" % va,
                                   "preceding_opcode": "0x%02X" % seg[i - 1] if i > 0 else None,
                                   "context_hex": hx(ctx)})
    i = seg.find(needle, i + 1)

# ---- P2: reader refs: E8/E9 to 0x0072FA30 and imm32 references
rdr = 0x0072FA30
refs = {"call_e8": [], "jmp_e9": [], "imm32": []}
for i in range(len(seg) - 5):
    if seg[i] == 0xE8:
        rel, = struct.unpack_from("<i", seg, i + 1)
        if base_va + i + 5 + rel == rdr:
            refs["call_e8"].append("0x%08X" % (base_va + i))
    if seg[i] == 0xE9:
        rel, = struct.unpack_from("<i", seg, i + 1)
        if base_va + i + 5 + rel == rdr:
            refs["jmp_e9"].append("0x%08X" % (base_va + i))
n2 = struct.pack("<I", rdr)
i = seg.find(n2)
while i >= 0:
    refs["imm32"].append({"va": "0x%08X" % (base_va + i),
                          "prev_op": "0x%02X" % seg[i - 1] if i else None,
                          "ctx": hx(seg[max(0, i - 6):i + 6])})
    i = seg.find(n2, i + 1)
R["p2_reader_refs"] = refs

# ---- P3: dispatcher wide scan for message-type immediates 0xA2..0xC7
lo, hi = 0xA2, 0xC7
hits = []
start = 0x004B18D0
wlen = 0x2000
fo = va2fo(start)
win = data[fo:fo + wlen]
for i in range(len(win) - 5):
    b0 = win[i]
    if b0 == 0x3D:  # CMP EAX, imm32
        imm, = struct.unpack_from("<I", win, i + 1)
        if lo <= imm <= hi:
            hits.append(("cmp_eax_i32", "0x%08X" % (start + i), imm))
    if b0 == 0x81 and 0xF8 <= (win[i + 1] if i + 1 < len(win) else 0) <= 0xFF:
        imm, = struct.unpack_from("<I", win, i + 2)
        if lo <= imm <= hi:
            hits.append(("cmp_r_i32", "0x%08X" % (start + i), imm))
    if b0 == 0x83 and 0xF8 <= (win[i + 1] if i + 1 < len(win) else 0) <= 0xFF:
        imm = win[i + 2] if i + 2 < len(win) else 0
        if lo <= imm <= hi:
            hits.append(("cmp_r_i8", "0x%08X" % (start + i), imm))
    if b0 == 0x2D:  # SUB EAX, imm32
        imm, = struct.unpack_from("<I", win, i + 1)
        if lo <= imm <= hi:
            hits.append(("sub_eax_i32", "0x%08X" % (start + i), imm))
    if b0 == 0x83 and (win[i + 1] if i + 1 < len(win) else 0) == 0xE8:
        imm = win[i + 2] if i + 2 < len(win) else 0
        if lo <= imm <= hi:
            hits.append(("sub_eax_i8", "0x%08X" % (start + i), imm))
    if b0 == 0x68:  # PUSH imm32
        imm, = struct.unpack_from("<I", win, i + 1)
        if lo <= imm <= hi:
            hits.append(("push_i32", "0x%08X" % (start + i), imm))
    if b0 == 0x6A:  # PUSH imm8
        imm = win[i + 1] if i + 1 < len(win) else 0
        if lo <= imm <= hi:
            hits.append(("push_i8", "0x%08X" % (start + i), imm))
    if b0 == 0x66 and win[i + 1] == 0x3D if i + 1 < len(win) else False:
        imm, = struct.unpack_from("<H", win, i + 2)
        if lo <= imm <= hi:
            hits.append(("cmp_ax_i16", "0x%08X" % (start + i), imm))
R["p3_dispatcher"] = hits[:80]

# ---- P4: scene root SetName sites
for site in (0x009331CD, 0x0093338F):
    fo = va2fo(site - 16)
    R["p4_scene_root"]["ctx_%08X" % site] = hx(data[fo:fo + 32])
# find PUSH 0xA972FC (68 FC 72 A9 00) anywhere in .text
n3 = struct.pack("<B I", 0x68, 0x00A972FC)
i = seg.find(n3)
push_sites = []
while i >= 0 and len(push_sites) < 12:
    push_sites.append("0x%08X" % (base_va + i))
    i = seg.find(n3, i + 1)
R["p4_scene_root"]["push_scene_root_sites"] = push_sites
# new(0x118) push (68 18 01 00 00) near 0x00933310
n4 = struct.pack("<B I", 0x68, 0x118)
i = seg.find(n4)
sites118 = []
while i >= 0 and len(sites118) < 40:
    sites118.append("0x%08X" % (base_va + i))
    i = seg.find(n4, i + 1)
R["p4_scene_root"]["push_0x118_sites"] = sites118

# ---- P5: emitter tail 0x006C3FA0..0x006C4130
fo = va2fo(0x006C3FA0)
R["p5_emitter_tail"] = hx(data[fo:fo + 0x190])

# ---- P6: FUN_006C3640 prologue
fo = va2fo(0x006C3640)
R["p6_sched_3640"] = hx(data[fo:fo + 0x80])

# ---- P7: array callers region
fo = va2fo(0x006C3FE0)
R["p7_array_callers"] = hx(data[fo:fo + 0x140])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2)
print("QC_DERIVE2 written:", OUT)
print("P1 callback refs:", len(R["p1_callback_refs"]))
for r in R["p1_callback_refs"][:12]:
    print("  ", r)
print("P2 reader refs:", refs)
print("P3 dispatcher hits:", len(R["p3_dispatcher"]))
for h in R["p3_dispatcher"][:30]:
    print("  ", h)
print("P4 push scene-root sites:", push_sites)
print("P4 push 0x118 sites:", sites118)
