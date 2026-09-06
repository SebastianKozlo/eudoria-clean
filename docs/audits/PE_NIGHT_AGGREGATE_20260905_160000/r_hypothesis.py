#!/usr/bin/env python3
"""The R-channel hypothesis test: is R a DERIVED HEIGHT encoding?
H0: R = round(a + b * h) for the texels where R != 93 (the sea constant).
Test: linear regression + the exact-match count."""
import struct

SRC = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841\01_RAW\global_height_429259.tga"
raw = open(SRC, "rb").read()
W = H = 257
pts = []
for i in range(W * H):
    b = raw[18 + i * 3: 18 + i * 3 + 3]
    pts.append((b[0], b[1], b[2]))  # B, G, R

hs = [((b << 8) | g) / 256.0 for b, g, r in pts]
rs = [r for b, g, r in pts]

# the regression over R != 93
sub = [(h, r) for h, r in zip(hs, rs) if r != 93]
n = len(sub)
mh = sum(h for h, r in sub) / n
mr = sum(r for h, r in sub) / n
b_num = sum((h - mh) * (r - mr) for h, r in sub)
b_den = sum((h - mh) ** 2 for h, r in sub)
slope = b_num / b_den
intercept = mr - slope * mh
print(f"R != 93: n={n}; R = {intercept:.3f} + {slope:.4f} * h")
exact = sum(1 for h, r in sub if abs((intercept + slope * h) - r) < 0.5)
print(f"exact(<0.5) matches: {exact}/{n} = {100*exact/n:.1f}%")

# the integer-form test: R = C - B? (the raw-byte relation)
import collections
rel_cnt = collections.Counter()
for B, G, R in pts:
    rel_cnt[(R + B)] += 1
top = rel_cnt.most_common(8)
print("R+B top values:", top)

rel_cnt2 = collections.Counter()
for B, G, R in pts:
    rel_cnt2[(R - B)] += 1
print("R-B top values:", rel_cnt2.most_common(8))

# Q3 (the constant-93 quadrant): its heights?
q3 = []
for i, (B, G, R) in enumerate(pts):
    x = i % W
    y = i // W
    if x >= W // 2 and y >= H // 2:
        q3.append(((B << 8 | G) / 256.0, R))
qh = [h for h, r in q3]
print(f"Q3: n={len(q3)}, R uniq={len(set(r for h,r in q3))}, height range {min(qh):.1f}..{max(qh):.1f}, land(>0)={sum(1 for h in qh if h>0)}/{len(q3)}")
