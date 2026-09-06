#!/usr/bin/env python3
"""THE R-CHANNEL ROLE in the 257x257 global height texture (429259).
Known: height = ((B<<8|G)/256 - 128)*5 m (N-4/RUN-3, independently re-verified).
The R channel = an unknown second field (min 42, max 255, 179 unique).
THE QUESTION: is R a class/palette mask, a derived value, or another grid?"""
import struct
from collections import Counter

SRC = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841\01_RAW\global_height_429259.tga"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\R_CHANNEL_ANALYSIS.txt"

raw = open(SRC, "rb").read()
W = H = 257
px = []
for i in range(W * H):
    b = raw[18 + i * 3: 18 + i * 3 + 3]
    px.append((b[0], b[1], b[2]))  # B, G, R (TGA BGR)

rs = [p[2] for p in px]
bs = [p[0] for p in px]
gs = [p[1] for p in px]

lines = []
lines.append(f"R: min={min(rs)} max={max(rs)} unique={len(set(rs))}")
cnt = Counter(rs)
lines.append("R top-20 values: " + ", ".join(f"{v}x{c}" for v, c in cnt.most_common(20)))

# correlation: is R a function of the height (B,G)?
# test: R == clamp(height-derived)?
hs = [((b << 8) | g) / 256.0 for b, g in zip(bs, gs)]
import math
# Pearson r between R and the height
n = len(rs)
mr = sum(rs) / n
mh = sum(hs) / n
cov = sum((r - mr) * (h - mh) for r, h in zip(rs, hs)) / n
sr = math.sqrt(sum((r - mr) ** 2 for r in rs) / n)
sh = math.sqrt(sum((h - mh) ** 2 for h in hs) / n)
lines.append(f"Pearson(R, height) = {cov / (sr * sh):.4f}")

# is R constant per 2x2 block (a 129x129 grid upsampled)?
blocks_const = 0
blocks_total = 0
for y in range(0, H - 1, 2):
    for x in range(0, W - 1, 2):
        vals = {px[y * W + x][2], px[y * W + x + 1][2], px[(y + 1) * W + x][2], px[(y + 1) * W + x + 1][2]}
        blocks_total += 1
        if len(vals) == 1:
            blocks_const += 1
lines.append(f"2x2-constant blocks: {blocks_const}/{blocks_total} ({100*blocks_const/blocks_total:.1f}%)")

# the row-profile: R per row (min/max/mean)
lines.append("\nrow profile (first 12 rows): ")
for y in range(12):
    row = [px[y * W + x][2] for x in range(W)]
    lines.append(f"  row{y:3}: min={min(row)} max={max(row)} mean={sum(row)/W:.1f} uniq={len(set(row))}")

# the value-classification: how many distinct LOW-value classes (a palette?)
low = [v for v in rs if v < 128]
lines.append(f"\nR values <128: {len(low)} ({100*len(low)/len(rs):.1f}%); unique: {len(set(low))}")

# quadrant analysis: the R distribution per world quadrant
def qr(x, y):
    return (1 if x >= W // 2 else 0) + (2 if y >= H // 2 else 0)


from collections import defaultdict
qd = defaultdict(list)
for i, (b, g, r) in enumerate(px):
    qd[qr(i % W, i // W)].append(r)
for q in sorted(qd):
    v = qd[q]
    lines.append(f"quadrant {q}: R min={min(v)} max={max(v)} mean={sum(v)/len(v):.1f} uniq={len(set(v))}")

print("\n".join(lines))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
