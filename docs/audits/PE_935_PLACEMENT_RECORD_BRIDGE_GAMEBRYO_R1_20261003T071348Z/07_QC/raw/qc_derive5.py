#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QC_DERIVE5 — independent MSVC RTTI chain verification for
NiControllerSequence vftable 0x00A889C8 (R-1 falsifier) and
NiNode vftable 0x00A8CCF4 + ArkObject + ArkAnimationModelPart::AnimSeqPair.
No Ghidra: raw PE mapping + RTTI structure walk."""
import struct

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
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
    secs.append((data[o:o + 8].rstrip(b"\0").decode("latin-1"), vaddr, rsz, rptr))


def va2fo(va):
    rva = va - image_base
    for (nm, vaddr, rsz, rptr) in secs:
        if vaddr <= rva < vaddr + rsz:
            return rptr + (rva - vaddr)
    return None


def u32(va):
    fo = va2fo(va)
    if fo is None:
        return None
    return struct.unpack_from("<I", data, fo)[0]


def cstr(va, maxlen=64):
    fo = va2fo(va)
    if fo is None:
        return None
    out = b""
    for i in range(maxlen):
        b = data[fo + i]
        if b == 0:
            break
        out += bytes([b])
    return out.decode("latin-1", "replace")


def rtti_name(vftable_va):
    col = u32(vftable_va - 4)
    if col is None or not (0x00400000 <= col < 0x00C00000):
        return None, None
    sig = u32(col)
    ptd = u32(col + 0xC)
    if ptd is None or not (0x00400000 <= ptd < 0x00C00000):
        return None, None
    nm = cstr(ptd + 8)
    return nm, {"col_va": "0x%08X" % col, "col_sig": sig,
                "type_desc_va": "0x%08X" % ptd}


res = {}
for label, vt in (("NiControllerSequence?", 0x00A889C8),
                  ("NiNode?", 0x00A8CCF4),
                  ("ArkObject?", None),
                  ("AnimSeqPair?", None)):
    if vt is None:
        continue
    nm, meta = rtti_name(vt)
    res[label] = {"vftable": "0x%08X" % vt, "rtti_name": nm, "meta": meta}

# also resolve vftable imm32 from ArkObject ctor (C7 05/06/07/45..) — from
# decomp D03 *param_1_00 = ArkObject::vftable; find C7 45 00 imm32 in FUN_00726E70
fo = va2fo(0x00726E70)
win = data[fo:fo + 0x60]
for i in range(len(win) - 6):
    if win[i] == 0xC7 and (win[i + 1] & 0xC0) == 0x00:
        imm, = struct.unpack_from("<I", win, i + 2)
        if 0x00A00000 <= imm <= 0x00BFFFFF:
            nm, meta = rtti_name(imm)
            res["ArkObject_ctor_store"] = {"site": "0x%08X" % (0x00726E70 + i),
                                           "vftable": "0x%08X" % imm,
                                           "rtti_name": nm}
            break

# AnimSeqPair from R14: *puVar3 = ArkAnimationModelPart::AnimSeqPair::vftable
# ctor vtable store unknown VA; skip — not load-bearing.

# NiControllerSequence RTTI name via type descriptor string search:
idx = data.find(b"NiControllerSequence")
res["string_search_nics"] = idx

import json
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
with open(PKG + r"\07_QC\raw\QC_DERIVATIONS5.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps(res, indent=1))
