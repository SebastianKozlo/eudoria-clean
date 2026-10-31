#!/usr/bin/env python3
"""RUN Stage D — TYPE0 field statistics f7/f8/f9 across the FULL corpus (1686 files).

Measures: per-field zero/non-zero, and value quantization (multiples of pi/36).
Writes 01_RAW/TYPE0_FIELD_STATS.json. Read-only on Volumes.bnt.
"""
import struct, json, os, math, collections

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
data = open(BNT, "rb").read()
n = len(data)
idx = struct.unpack_from("<I", data, n - 8)[0]
pos = idx
cnt = struct.unpack_from("<I", data, pos)[0]
pos += 4
files = 0
for _ in range(cnt):
    nl = data.index(b"\x0a", pos)
    name = data[pos:nl].decode()
    pos = nl + 1
    packed, off, c, d = struct.unpack_from("<IIII", data, pos)
    pos += 16
    if name.endswith(".bvi") and data[off] == 0 and data[off + 1] == 0:
        k = struct.unpack_from("<H", data, off + 2)[0]
        if 4 + k * 36 == packed:
            files += 1

stats = collections.Counter()
f9vals = collections.Counter()
f8vals = collections.Counter()
f7_nonzero_max = 0.0
records = 0
# re-walk
pos = idx + 4
for _ in range(cnt):
    nl = data.index(b"\x0a", pos)
    name = data[pos:nl].decode()
    pos = nl + 1
    packed, off, c, d = struct.unpack_from("<IIII", data, pos)
    pos += 16
    if not (name.endswith(".bvi") and data[off] == 0 and data[off + 1] == 0):
        continue
    k = struct.unpack_from("<H", data, off + 2)[0]
    if 4 + k * 36 != packed:
        continue
    for i in range(k):
        f1, f2, f3, f4, f5, f6, f7, f8, f9 = struct.unpack_from("<9f", data, off + 4 + i * 36)
        records += 1
        if f7 == 0:
            stats["f7_zero"] += 1
        else:
            stats["f7_nonzero"] += 1
            f7_nonzero_max = max(f7_nonzero_max, abs(f7))
        if f8 == 0 or f8 == 0.0 and math.copysign(1, f8) < 0:
            stats["f8_zero_or_negzero"] += 1
        else:
            stats["f8_other"] += 1
            f8vals[round(f8, 6)] += 1
        f9vals[round(f9, 6)] += 1
out = {
    "run": "PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031",
    "measure": "TYPE0 f7/f8/f9 full-corpus statistics",
    "type0_files": files,
    "type0_records": records,
    "stats": dict(stats),
    "f7_nonzero_max_abs": f7_nonzero_max,
    "f8_top_values": f8vals.most_common(12),
    "f9_top_values": f9vals.most_common(15),
    "pi_over_36": math.pi / 36,
}
with open(os.path.join(RUN, "01_RAW", "TYPE0_FIELD_STATS.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps(out, indent=1)[:1200])
