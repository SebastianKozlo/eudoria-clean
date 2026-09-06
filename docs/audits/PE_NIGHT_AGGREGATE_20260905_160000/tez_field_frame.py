#!/usr/bin/env python3
"""THE TEZ<->FIELD FRAME RELATION (the georef open bound #2).
The TEZ records: [u8 type][u16 count][count x 48-byte records] (prior-verified layout,
171 files, 1,015 records). The world-space floats go up to 2^19-1 = 524,287.
THE QUESTION: where do the TEZ rectangle coordinates actually sit relative to the
GLOBAL FIELD frame (-65,536..+65,536, span 131,072)? Read-only, era 9.3.5."""
import struct

SRC = r"D:\Eudoria_Reconstruction\pcg_install\Data\TerrainEditZones\TerrainEditZones.bnt"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\TEZ_FIELD_FRAME.txt"

d = open(SRC, "rb").read()
fs = len(d)
istart = struct.unpack_from("<I", d, fs - 8)[0]
count = struct.unpack_from("<I", d, istart)[0]
entries = []
pos = istart + 4
for _ in range(count):
    ne = pos
    while d[ne] != 0x0A:
        ne += 1
    nm = d[pos:ne].decode("ascii", "replace")
    sz, off = struct.unpack_from("<II", d, ne + 1)
    entries.append((nm, sz, off))
    pos = ne + 17
print(f"entries: {len(entries)}")

records = []
layout_fails = 0
for nm, sz, off in entries:
    payload = d[off:off + sz]
    if len(payload) < 3:
        continue
    rtype = payload[0]
    rcount = struct.unpack_from("<H", payload, 1)[0]
    expected = 3 + rcount * 48
    if len(payload) != expected:
        layout_fails += 1
        continue
    for i in range(rcount):
        rec = payload[3 + i * 48: 3 + (i + 1) * 48]
        # the floats: decode all 12 f32 of the 48-byte record
        floats = struct.unpack_from("<12f", rec, 0)
        records.append((nm, rtype, floats))

print(f"records parsed: {len(records)}; layout fails: {layout_fails}")

# the coordinate analysis: identify which floats are the coords (X0/Z0/X1/Z1)
# heuristic: the first 4 floats of each record = the rect (prior: X0,Z0,X1,Z1)
import math

valid = 0
xs, zs = [], []
heights = []
for nm, rtype, f in records:
    x0, z0, x1, z1 = f[0], f[1], f[2], f[3]
    # sanity: rect-ness
    if all(not math.isnan(v) and abs(v) < 2.0e6 for v in (x0, z0, x1, z1)) and x1 >= x0 and z1 >= z0:
        valid += 1
        xs.extend([x0, x1])
        zs.extend([z0, z1])
        heights.append(f[4])

lines = [f"records: {len(records)}; rect-valid (first-4-floats): {valid}",
         f"X range: {min(xs):.1f} .. {max(xs):.1f}" if xs else "no X",
         f"Z range: {min(zs):.1f} .. {max(zs):.1f}" if zs else "no Z",
         f"height(f[4]) range: {min(heights):.1f} .. {max(heights):.1f}" if heights else ""]

# the frame tests
tests = {
    "inside field (-65,536..+65,536)": lambda v: -65536 - 1 <= v <= 65536 + 1,
    "inside 0..2^19 (524,288)": lambda v: 0 <= v <= 524288,
    "inside 0..131,072": lambda v: 0 <= v <= 131072,
    "inside -2^18..+2^18 (±262,144)": lambda v: -262144 <= v <= 262144,
}
for label, pred in tests.items():
    fx = sum(1 for v in xs if pred(v))
    fz = sum(1 for v in zs if pred(v))
    lines.append(f"{label}: X {fx}/{len(xs)} ({100*fx/max(1,len(xs)):.1f}%), Z {fz}/{len(zs)} ({100*fz/max(1,len(zs)):.1f}%)")

# the field-frame fit: if the TEZ world = the SAME 131,072-unit world, the rects
# would fit the -65,536..+65,536 frame. If they fit 0..524,288 -> a different frame.
# also: the centroid
if xs:
    lines.append(f"X centroid: {sum(xs)/len(xs):.1f}; Z centroid: {sum(zs)/len(zs):.1f}")

# the per-record-type census
from collections import Counter
tc = Counter(r[1] for r in records)
lines.append(f"record types: {dict(tc)}")

print("\n".join(str(x) for x in lines))
open(OUT, "w", encoding="utf-8").write("\n".join(str(x) for x in lines))
