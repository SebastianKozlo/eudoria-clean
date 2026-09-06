#!/usr/bin/env python3
"""The EXPANDED CELLSTREAM NEGATIVES — the grid-shape scan over ALL the local 9.3.5
containers (completing RUN-4's Parameters/Textures-only scan).
The targets: the 65x65 climate grid (4,225 B) + the 129x129 detail grids (16,641 B)
+ the +16B-header variants + the .tga (18B-header) variants."""
import os
import struct

ROOT = r"D:\Eudoria_Reconstruction\pcg_install\Data"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\EXPANDED_GRID_NEGATIVES.txt"

GRIDS = {"65x65": 4225, "129x129": 16641}
VARIANTS = [0, 16, 18, 12]  # raw / ArkVFS-header / TGA-header / ?

lines = []
total_containers = 0
total_entries = 0
hits = []

for dirpath, dirs, files in os.walk(ROOT):
    for fn in files:
        p = os.path.join(dirpath, fn)
        low = fn.lower()
        if not low.endswith(".bnt"):
            # the raw files: direct size checks
            n = os.path.getsize(p)
            for glabel, g in GRIDS.items():
                for v in VARIANTS:
                    if n == g + v:
                        hits.append((p, n, glabel, f"raw+{v}"))
            continue
        total_containers += 1
        try:
            d = open(p, "rb").read()
        except OSError:
            continue
        fs = len(d)
        if fs < 16:
            continue
        istart = struct.unpack_from("<I", d, fs - 8)[0]
        if not (0 < istart < fs):
            continue
        count = struct.unpack_from("<I", d, istart)[0]
        if count <= 0 or istart + 4 + count * 21 > fs:
            continue
        pos = istart + 4
        for _ in range(count):
            ne = pos
            while ne < fs and d[ne] != 0x0A:
                ne += 1
            nm = d[pos:ne].decode("ascii", "replace")
            sz, off = struct.unpack_from("<II", d, ne + 1)
            for glabel, g in GRIDS.items():
                for v in VARIANTS:
                    if sz == g + v:
                        hits.append((p + " :: " + nm, sz, glabel, f"bnt-entry+{v}"))
            pos = ne + 17
            total_entries += 1

lines.append(f"containers scanned: {total_containers}; entries scanned: {total_entries}")
lines.append(f"GRID HITS: {len(hits)}")
for h in hits[:20]:
    lines.append(f"  {h}")

print("\n".join(lines))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
