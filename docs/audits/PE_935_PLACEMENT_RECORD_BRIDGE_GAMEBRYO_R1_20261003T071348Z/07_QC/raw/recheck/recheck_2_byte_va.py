#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 2 (AMEND-3 truth): OWN PE mapper (section table walk) -> byte read at
VA 0x005B6597 from the physical EXE. Verifies '68 D3 3E 00 00' (PUSH 0x3ED3)
and re-derives the following E8 rel32 CALL target (expect FUN_005B5F90).
Independent of the executor's and QC-round-1's tooling."""
import hashlib
import json
import os
import struct

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck2_byte_result.json")
EXPECT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECT_SIZE = 8015872

data = open(EXE, "rb").read()
sha = hashlib.sha256(data).hexdigest().upper()
assert len(data) == EXPECT_SIZE, "size %d != %d" % (len(data), EXPECT_SIZE)
assert sha == EXPECT_SHA, "sha %s mismatch" % sha

# --- own PE parse ---
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew + 4] == b"PE\0\0"
coff = e_lfanew + 4
machine, nsec, _ = struct.unpack_from("<HHI", data, coff)
opt_size = struct.unpack_from("<H", data, coff + 16)[0]
opt = coff + 20
magic = struct.unpack_from("<H", data, opt)[0]
assert magic == 0x10B, "not PE32 (magic 0x%X)" % magic
image_base = struct.unpack_from("<I", data, opt + 28)[0]
sec_tab = opt + opt_size
sections = []
for i in range(nsec):
    off = sec_tab + 40 * i
    name = data[off:off + 8].rstrip(b"\0").decode("latin-1")
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", data, off + 8)
    sections.append((name, vaddr, vsize, raddr, rsize))

def va_to_fo(va):
    rva = va - image_base
    for name, vaddr, vsize, raddr, rsize in sections:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr), name
    return None, None

res = {
    "exe_sha256": sha, "exe_size": len(data), "image_base": "0x%08X" % image_base,
    "sections": [(n, "0x%08X" % v, "0x%X" % vs, "0x%08X" % r, "0x%X" % rs)
                 for n, v, vs, r, rs in sections],
    "dll_characteristics": "0x%04X" % struct.unpack_from("<H", data, opt + 70)[0],
}

VA = 0x005B6597
fo, sec = va_to_fo(VA)
res["va"] = "0x%08X" % VA
res["file_offset"] = fo
res["section"] = sec
window = data[fo:fo + 10]
res["bytes_hex"] = " ".join("%02X" % b for b in window)
res["bytes_match_68_D3_3E_00_00"] = (window[:5] == bytes.fromhex("68 D3 3E 00 00".replace(" ", "")))
imm32 = struct.unpack_from("<I", data, fo + 1)[0]
res["push_imm32"] = "0x%08X" % imm32
res["push_imm32_dec"] = imm32
res["push_imm32_is_0x3ED3_16083"] = (imm32 == 0x3ED3 and imm32 == 16083)
# next instruction E8 rel32
assert window[5] == 0xE8, "byte at +5 is 0x%02X not E8" % window[5]
rel = struct.unpack_from("<i", data, fo + 6)[0]
target = VA + 5 + 5 + rel
res["call_rel32"] = rel
res["call_target"] = "0x%08X" % target
res["call_target_is_0x005B5F90"] = (target == 0x005B5F90)

# negative control: the pre-repair transcription '68 2D 3E 00 00' must NOT be the
# physical byte sequence; also count total PUSH 0x3ED3 sites in .text to
# confirm uniqueness claim of the E9a anchor context
text = None
for name, vaddr, vsize, raddr, rsize in sections:
    if name == ".text":
        text = (raddr, vaddr, rsize, vsize)
blob = data[text[0]:text[0] + text[2]]
pat = bytes.fromhex("68D33E0000")
sites = []
i = blob.find(pat)
while i != -1:
    sites.append("0x%08X" % (image_base + text[1] + i))
    i = blob.find(pat, i + 1)
res["push_0x3ED3_all_sites_in_text"] = sites
res["negative_control_2D"] = (window[1] != 0x2D)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
