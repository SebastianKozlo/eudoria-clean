#!/usr/bin/env python3
"""The TEZ 48-byte record layout — the empirical per-slot census."""
import struct

SRC = r"D:\Eudoria_Reconstruction\pcg_install\Data\TerrainEditZones\TerrainEditZones.bnt"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\TEZ_SLOT_CENSUS.txt"

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

recs = []
for nm, sz, off in entries:
    p = d[off:off + sz]
    if len(p) < 3:
        continue
    rt = p[0]
    rc = struct.unpack_from("<H", p, 1)[0]
    if len(p) != 3 + rc * 48:
        continue
    for i in range(rc):
        recs.append(struct.unpack_from("<12I", p, 3 + i * 48))

print(f"records: {len(recs)}")
lines = [f"records: {len(recs)} (12 u32 slots each)"]
lines.append("\n=== per-slot statistics (as u32) ===")
for slot in range(12):
    vals = [r[slot] for r in recs]
    u = sorted(set(vals))
    lines.append(f"slot{slot:02}: min={min(vals):>12} max={max(vals):>12} uniq={len(u):>5} "
                 f"| as_float_range=[{struct.pack('<I', min(vals) and min(vals) or 0)}]" if False else
                 f"slot{slot:02}: min={min(vals):>12} max={max(vals):>12} uniq={len(u):>5} sample={u[:6]}")

# the float interpretation of plausible slots
lines.append("\n=== per-slot as float (the plausible-coord slots) ===")
import math
for slot in range(12):
    fvals = []
    for r in recs:
        b = struct.pack("<I", r[slot])
        f = struct.unpack("<f", b)[0]
        if not math.isnan(f) and abs(f) < 1.0e9:
            fvals.append(f)
    if fvals:
        lines.append(f"slot{slot:02}: float min={min(fvals):.2f} max={max(fvals):.2f} "
                     f"int-like={sum(1 for v in fvals if v == int(v))}/{len(fvals)}")

# the raw hex of 3 records
lines.append("\n=== 3 raw records ===")
for r in recs[:3]:
    lines.append(struct.pack("<12I", *r).hex(" "))

print("\n".join(lines))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
