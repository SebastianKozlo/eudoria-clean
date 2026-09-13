# -*- coding: utf-8 -*-
# F2c — OWN full walk of templates.vfs (ArkVFS02): stride = ceil((16+size)/base)*base,
# base = header u32@0x08. Verify ver==1 + CRC32 for every record. Read record 4508
# D@file+0x20 (=payload+0x10), E@+0x24, A@+0x14. Independent re-parse.
# Output: 01_RAW/F2_T4508_WALK.json

import json
import os
import struct
import sys
import zlib

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"

vfs = open(VFS, "rb").read()
res = {"stage": "F2_t4508_walk", "measured": {}, "errors": []}

magic = vfs[:8]
assert magic == b"ArkVFS02", "bad magic %r" % magic
base = struct.unpack_from("<I", vfs, 8)[0]
one = struct.unpack_from("<I", vfs, 12)[0]
res["measured"]["header"] = {"magic": magic.decode(), "stride_base": base, "u32_at_0c": one}

pos = 16
n = 0
crc_fail = 0
rec_4508 = None
records_count = 0
stop_reason = None
while pos + 16 <= len(vfs):
    bid, bsize, bver, bcrc = struct.unpack_from("<IIII", vfs, pos)
    if bver != 1:
        stop_reason = "ver!=1 @%d (id=%d)" % (pos, bid)
        break
    if pos + 16 + bsize > len(vfs):
        stop_reason = "truncated @%d" % pos
        break
    payload = vfs[pos + 16: pos + 16 + bsize]
    if (zlib.crc32(payload) & 0xFFFFFFFF) != bcrc:
        crc_fail += 1
    if bid == 4508:
        rec_4508 = {
            "file_offset": pos, "size": bsize, "ver": bver,
            "crc32_field": "0x%08X" % bcrc,
            "crc32_calc": "0x%08X" % (zlib.crc32(payload) & 0xFFFFFFFF),
            "crc_ok": (zlib.crc32(payload) & 0xFFFFFFFF) == bcrc,
        }
        if bsize >= 28:
            id2, A, B, C = struct.unpack_from("<IIII", vfs, pos + 16)
            Dbits = struct.unpack_from("<I", vfs, pos + 0x20)[0]
            Ebits = struct.unpack_from("<I", vfs, pos + 0x24)[0]
            rec_4508.update({
                "id2": id2, "A": A, "B": B, "C": C,
                "D_file_offset": pos + 0x20,
                "D_bits": "0x%08X" % Dbits,
                "D_f32": struct.unpack("<f", struct.pack("<I", Dbits))[0],
                "E_bits": "0x%08X" % Ebits,
                "E_f32": struct.unpack("<f", struct.pack("<I", Ebits))[0],
                "F_u32": struct.unpack_from("<I", vfs, pos + 0x28)[0],
            })
    stride = ((16 + bsize + base - 1) // base) * base
    pos += stride
    n += 1

records_count = n
if pos >= len(vfs) or pos + 16 > len(vfs):
    stop_reason = stop_reason or "EOF"

res["measured"]["walk"] = {
    "records": records_count, "crc_fail": crc_fail,
    "stop_reason": stop_reason or "EOF",
    "end_offset": pos, "file_size": len(vfs),
    "record_4508": rec_4508,
}
exp = {"D_bits": "0x42F9E1CB", "D_f32": 124.94100189208984, "A": 296445}
if rec_4508:
    ok_bits = rec_4508["D_bits"].upper() == "0X42F9E1CB"
    ok_f32 = abs(rec_4508["D_f32"] - exp["D_f32"]) < 1e-9
    ok_A = rec_4508["A"] == exp["A"]
    res["measured"]["verification_vs_claims"] = {
        "D_bits_match": ok_bits, "D_f32_match": ok_f32, "A_equals_296445": ok_A}
    if not (ok_bits and ok_f32):
        res["errors"].append("D mismatch: %s / %r" % (rec_4508["D_bits"], rec_4508["D_f32"]))

with open(os.path.join(OUT, "F2_T4508_WALK.json"), "w") as f:
    json.dump(res, f, indent=2)

print(json.dumps(res["measured"]["walk"], indent=1))
print("verification:", res["measured"].get("verification_vs_claims"))
