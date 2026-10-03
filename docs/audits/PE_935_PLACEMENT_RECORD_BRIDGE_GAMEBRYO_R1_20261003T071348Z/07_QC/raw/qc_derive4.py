#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC_DERIVE4 — final probes.
P13 ASLR: DllCharacteristics dynamic-base bit.
P14 NiControllerSequence vtable imm32 byte-pin in ctor FUN_007796D0.
P15 Second SetName callsite context (0x009331CD) + first (0x0093338F).
P16 Context around JMP->reader @0x00452497 (which function contains it).
P17 Verify E9a byte-string claim "68 2D 3E 00 00" vs real bytes at 0x005B6597.
"""
import struct

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
dll_chars, = struct.unpack_from("<H", data, e_lfanew + 24 + 70)
nsec, = struct.unpack_from("<H", data, e_lfanew + 6)
secs = []
so = e_lfanew + 24 + opt_size
for i in range(nsec):
    o = so + i * 40
    vsz, vaddr, rsz, rptr = struct.unpack_from("<4I", data, o + 8)
    secs.append((data[o:o + 8].rstrip(b"\0").decode("latin-1"), vaddr, rsz, rptr))


def va2fo(va):
    rva = va - image_base
    for (nm, vaddr, rsz, rptr) in secs:
        if vaddr <= rva < vaddr + rsz:
            return rptr + (rva - vaddr)
    return None


def hx(b):
    return " ".join("%02X" % c for c in b)


R = {}
R["p13_dll_characteristics"] = "0x%04X" % dll_chars
R["p13_aslr_dynamic_base_bit_set"] = bool(dll_chars & 0x40)

# P14: NiControllerSequence ctor vtable imm32
fo = va2fo(0x007796D0)
win = data[fo:fo + 0x50]
R["p14_ctor_7796d0_first80"] = hx(win[:0x50])
found = None
for i in range(len(win) - 6):
    if win[i] == 0xC7 and (win[i + 1] & 0xC0) == 0x00:
        imm, = struct.unpack_from("<I", win, i + 2)
        if 0x00A00000 <= imm <= 0x00BFFFFF:
            found = {"site": "0x%08X" % (0x007796D0 + i), "imm32": "0x%08X" % imm}
            break
R["p14_vtable_imm32_in_ctor"] = found
# also look for MOV [reg],imm32 with C7 05 (MOV [mem],imm32)
if found is None:
    for i in range(len(win) - 6):
        if win[i] == 0xC7:
            imm, = struct.unpack_from("<I", win, i + 2 + (1 if (win[i+1] & 0xC0) else 0))
            R.setdefault("p14_alt", []).append((i, hex(imm)))

# P15: SetName contexts
for site in (0x009331CD, 0x0093338F):
    fo2 = va2fo(site - 12)
    R["p15_ctx_%08X" % site] = hx(data[fo2:fo2 + 32])

# P16: context of JMP->reader @0x00452497
fo3 = va2fo(0x00452480)
R["p16_jmp_context"] = hx(data[fo3:fo3 + 64])

# P17: bytes at 0x005B6597
fo4 = va2fo(0x005B6597)
R["p17_bytes_005B6597"] = hx(data[fo4:fo4 + 10])

# extra: verify E8a claim string VA and direct bytes of "Parameters\templates.vfs"
fo5 = va2fo(0x00A86D30)
R["p17_string_bytes"] = data[fo5:fo5 + 24].decode("latin-1", "replace")

import json
with open(PKG + r"\07_QC\raw\QC_DERIVATIONS4.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2)
print(json.dumps(R, indent=1))
