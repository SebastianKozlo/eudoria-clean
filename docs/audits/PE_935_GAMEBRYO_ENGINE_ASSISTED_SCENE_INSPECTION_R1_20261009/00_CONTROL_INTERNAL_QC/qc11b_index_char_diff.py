#!/usr/bin/env python3
"""QC11b — char-level diff of FINAL_REPORT §9 index SHA strings vs disk hashes."""
import hashlib
import os

PKG = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")

fr = open(PKG + "/FINAL_REPORT.md", encoding="utf-8").read()
blocks = fr.split("```text")
block = None
for b in blocks[1:]:
    b = b.split("```")[0]
    if "CORRECTED_CLAIM_MATRIX.json|" in b:
        block = b
        break

for line in block.strip().splitlines():
    if "|" not in line:
        continue
    parts = line.split("|")
    if len(parts) != 3:
        print("ODD PARTS:", repr(line))
        continue
    rel, size, sha = parts
    p = os.path.join(PKG, rel.strip())
    if not os.path.isfile(p):
        print("MISSING:", rel.strip())
        continue
    actual = hashlib.sha256(open(p, "rb").read()).hexdigest()
    idx = sha.strip()
    if idx.lower() != actual:
        print("---", rel.strip())
        print("  index repr :", repr(idx))
        print("  actual repr:", repr(actual))
        print("  lengths: index", len(idx), "actual", len(actual))
        n = min(len(idx), len(actual))
        diffpos = [i for i in range(n) if idx[i].lower() != actual[i]]
        print("  diff positions (within common len):", diffpos)
        for i in diffpos:
            print(f"    pos {i}: index {idx[i]!r} actual {actual[i]!r}")
