# -*- coding: utf-8 -*-
# F2b — templates.vfs structure walk (own parser, ArkVFS02): locate record 4508,
# read D@payload+0x10; verify bits 0x42F9E1CB / f32 124.94100189208984.
# Also decode selector target blocks 0x00855820/0x0085582A/0x00855834.
# Output: 01_RAW/F2_T4508.json + F2_CTX2_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump, f32bits

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

vfs = open(VFS, "rb").read()
res = {"stage": "F2_t4508", "measured": {}, "errors": []}

# header
hdr = vfs[:64]
res["measured"]["header_hex_64"] = hdr.hex()

# find record 4508: try simple contiguous record walk guesses.
# First: scan all offsets where u32 == 4508 (LE) AND check surroundings
pat = struct.pack("<I", 4508)
hits = []
i = 0
while True:
    j = vfs.find(pat, i)
    if j < 0:
        break
    hits.append(j)
    i = j + 1
res["measured"]["u32_4508_raw_hits"] = hits

# scan for D bits 0x42F9E1CB
patd = struct.pack("<I", 0x42F9E1CB)
dhits = []
i = 0
while True:
    j = vfs.find(patd, i)
    if j < 0:
        break
    dhits.append(j)
    i = j + 1
res["measured"]["bits_42F9E1CB_hits"] = dhits

# for each D-bit hit, dump context: preceding 32 bytes, the u32 id candidates
ctx = []
for j in dhits:
    rec = {"offset": j, "context_hex_prev32": vfs[j-32:j].hex(),
           "at_plus_minus": vfs[j-16:j+16].hex()}
    # candidate record starts: j-0x10 would make D at payload+0x10 if record starts at j-0x10
    for cand in (j - 0x10, j - 0x14, j - 0x18, j - 0x0C, j - 0x08):
        if cand >= 0:
            id_at_cand = struct.unpack_from("<I", vfs, cand)[0]
            rec.setdefault("candidates", []).append(
                {"record_start_if": cand, "id_u32": id_at_cand})
    ctx.append(rec)
res["measured"]["D_contexts"] = ctx

# Also verify the RUN4-claimed file offset 96528: what record contains it? dump around
res["measured"]["around_offset_96528"] = {
    "prev64_hex": vfs[96464:96528].hex(),
    "at64_hex": vfs[96528:96592].hex(),
}

# ArkVFS02 header parse attempt: magic?
res["measured"]["first16_hex"] = vfs[:16].hex()

with open(os.path.join(OUT, "F2_T4508.json"), "w") as f:
    json.dump(res, f, indent=2)

print("4508 raw hits:", hits)
print("D-bit hits:", dhits)
print("first16:", vfs[:16].hex())
