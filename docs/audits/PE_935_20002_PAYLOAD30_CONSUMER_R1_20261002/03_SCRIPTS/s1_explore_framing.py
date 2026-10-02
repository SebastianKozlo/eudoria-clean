#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1 explore: derive 20002.vfs record framing from physical bytes (executor in-run, RUN_ID
PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002). Pure reader; never modifies originals.

Generator of this artifact: 03_SCRIPTS\s1_explore_framing.py (this file).
"""
import struct

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"

data = open(VFS, "rb").read()
print("size", len(data), "=", hex(len(data)))
print("magic", data[:8])
base = struct.unpack_from("<I", data, 8)[0]
print("u32@+8 (base candidate) =", base)
print("u32@+12 =", struct.unpack_from("<I", data, 12)[0])

# If the file is 16-byte global header + N records of stride 128:
print("size-16 =", len(data) - 16, "; /128 =", (len(data) - 16) / 128.0)

for pos in (16, 144, 272, 400, 528, 656, 784, 912):
    h = data[pos:pos + 16]
    a, b, c, d = struct.unpack_from("<IIII", h, 0)
    h4 = struct.unpack_from("<4H", h, 0)
    print(f"hdr@{pos}: {h.hex(' ')}")
    print(f"   <IIII>: 0x{a:X} ({a}), {b}, {c}, 0x{d:X}")
    print(f"   <4H>: {h4}")
    print(f"   payload[+16:+16+112]: {data[pos+16:pos+32].hex(' ')} ... {data[pos+112:pos+128].hex(' ')}")
