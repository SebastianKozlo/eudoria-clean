#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1 explore 2: dump complete payloads of selected records (records 0, 1, 2, 1014, 1015).
Executor in-run, RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002. Pure reader.
"""
import struct

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
data = open(VFS, "rb").read()
BASE = 128
STRIDE = 128

def rec(i):
    frame = 16 + i * STRIDE
    rid, size, ver, crc = struct.unpack_from("<IIII", data, frame)
    pstart = frame + 16
    return frame, rid, size, ver, crc, pstart, data[pstart:pstart + size]

for i in (0, 1, 2, 1013, 1014, 1015, 1365):
    frame, rid, size, ver, crc, pstart, p = rec(i)
    print(f"=== record {i}: frame={frame} id=0x{rid:08X} size={size} ver={ver} crc=0x{crc:X} payload_start={pstart}")
    for off in range(0, len(p), 16):
        chunk = p[off:off + 16]
        print(f"  +{off:02X}: {chunk.hex(' ')}")
    # +0x30 field
    if len(p) >= 0x34:
        v30 = struct.unpack_from("<I", p, 0x30)[0]
        v2c = struct.unpack_from("<I", p, 0x2C)[0]
        v34 = struct.unpack_from("<I", p, 0x34)[0] if len(p) >= 0x38 else None
        print(f"  +0x2C u32 LE = {v2c} (0x{v2C:X})" if False else f"  +0x2C u32 LE = {v2c} (0x{v2c:X})")
        print(f"  +0x30 u32 LE = {v30} (0x{v30:X})")
        if v34 is not None:
            print(f"  +0x34 u32 LE = {v34} (0x{v34:X})")
        print(f"  +0x30 raw bytes: {p[0x30:0x34].hex(' ')}")
