# -*- coding: utf-8 -*-
# f2_x87_table.py - G3-F2-X87 (a): full x87 comparison table for
# FUN_004C46C0 @0x004C4777-0x004C4790 (and the identical pattern in
# FUN_0085B3E0 @0x0085B426-0x0085B441).
#
# OWN decode of the instruction sequence (verified byte-level):
#   FLD [esp+0x18]   (z)          -> ST0=z
#   FLD [esp+0x44]   (h)          -> ST0=h, ST1=z
#   FCOM ST(1)       (D8 D1)      -> compare ST0(h) vs ST1(z)
#   FNSTSW AX        (DF E0)
#   FSTP ST(1)       (DD D9)      -> ST1:=ST0(h); pop -> ST0=h
#   TEST AH,0x41     (F6 C4 41)   -> mask C0(bit8->AH0)|C3(bit14->AH6)
#   JNE 0x4C4790     (75 06)      -> taken iff (C0|C3)!=0
#   FSTP [ESP+0x18]  (D9 5C 24 18)-> z' = h   (fall-through: h>z ordered)
#   ... 0x4C4790: FSTP ST(0) (DD D8) -> discard h; z' = z (memory bits)
#
# This module is a MODEL of the x87 instruction semantics (STATIC-ONLY;
# no processor measurement, no client). Bit-exact IEEE-754 handling.
#
# Semantics (Intel SDM, FCOM): compare ST0 with ST1:
#   ST0 > ST1: C0=0 C2=0 C3=0
#   ST0 < ST1: C0=1 C2=0 C3=0
#   ST0 == ST1: C0=0 C2=0 C3=1
#   unordered: C0=1 C2=1 C3=1  (+ IE flag; masked exceptions assumed)
# NOTE: +0 == -0 on x87 (equal); Inf comparisons are ordered.
# TEST AH,0x41 -> ZF=1 iff (C0|C3)==0; JNE taken iff ZF=0.

import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")


def bits_of(v):
    return struct.unpack("<I", struct.pack("<f", v))[0]


def classify(a, b):
    """x87 FCOM result for ST0=a vs ST1=b -> (C0, C2, C3)."""
    if a != a or b != b:          # NaN (either side) -> unordered
        return (1, 1, 1)
    if a > b:
        return (0, 0, 0)
    if a < b:
        return (1, 0, 0)
    return (0, 0, 1)              # equal (includes +0 == -0)


def row(name, z, h):
    C0, C2, C3 = classify(h, z)   # ST0=h, ST1=z
    ah = (C0 << 0) | (C2 << 2) | (C3 << 6)
    test_result = ah & 0x41       # C0|C3 in AH mask
    jne_taken = (test_result != 0)
    if jne_taken:
        zprime = bits_of(z)       # z' = z bits (h discarded)
        branch = "JNE->0x4C4790 (FSTP ST(0); discard h)"
        h_written = False
    else:
        zprime = bits_of(h)       # z' = h (written to [ESP+0x18])
        branch = "fall-through (FSTP [ESP+0x18] := h)"
        h_written = True
    return {
        "case": name,
        "z_bits": "0x%08X" % bits_of(z), "h_bits": "0x%08X" % bits_of(h),
        "z_value": z, "h_value": h,
        "C0": C0, "C2": C2, "C3": C3,
        "TEST_AH_0x41_nonzero": jne_taken,
        "branch": branch,
        "zprime_bits": "0x%08X" % zprime,
        "zprime_is_z_bits": (zprime == bits_of(z)),
        "zprime_is_h_bits": (zprime == bits_of(h)),
        "h_stored_to_zslot": h_written,
    }


PINF = float("inf")
NINF = float("-inf")
NAN = float("nan")
PZERO = 0.0
NZERO = -0.0

rows = []
# {z, h} x {equal, less, greater, unordered, +-Inf, +-0}
rows.append(row("z=5.0 h=10.0 (h>z)", 5.0, 10.0))
rows.append(row("z=5.0 h=5.0 (equal)", 5.0, 5.0))
rows.append(row("z=10.0 h=5.0 (h<z)", 10.0, 5.0))
rows.append(row("z=5.0 h=NaN (unordered)", 5.0, NAN))
rows.append(row("z=NaN h=5.0 (unordered)", NAN, 5.0))
rows.append(row("z=NaN h=NaN (unordered)", NAN, NAN))
rows.append(row("z=5.0 h=+Inf", 5.0, PINF))
rows.append(row("z=5.0 h=-Inf", 5.0, NINF))
rows.append(row("z=+Inf h=5.0", PINF, 5.0))
rows.append(row("z=-Inf h=5.0", NINF, 5.0))
rows.append(row("z=+Inf h=+Inf (equal)", PINF, PINF))
rows.append(row("z=+Inf h=-Inf", PINF, NINF))
rows.append(row("z=-Inf h=+Inf", NINF, PINF))
rows.append(row("z=-Inf h=-Inf (equal)", NINF, NINF))
rows.append(row("z=+0 h=+0 (equal)", PZERO, PZERO))
rows.append(row("z=-0 h=+0 (equal on x87!)", NZERO, PZERO))
rows.append(row("z=+0 h=-0 (equal on x87!)", PZERO, NZERO))
rows.append(row("z=-0 h=-0 (equal)", NZERO, NZERO))
rows.append(row("z=-0.0 h=+0.0 bit-distinction", NZERO, PZERO))
rows.append(row("z=-1.0 h=+0.0", -1.0, PZERO))
rows.append(row("z=+0.0 h=+1.0", PZERO, 1.0))

# Math.max comparison witness (for the contract's divergence claim):
# Math.max(z, NaN) = NaN in JS semantics; here z' = z bits.
# Math.max(-0, +0) = +0 (JS); here z=-0 h=+0 -> z' = -0 bits.
divergence = {
    "NaN(h)_case": "z'=z (bits of z) - DIVERGES from Math.max(z,NaN)=NaN",
    "NaN(z)_case": "z'=NaN (bits of z) - Math.max would also propagate NaN",
    "neg0_vs_pos0": "z=-0,h=+0: x87 equal -> z'=-0 bits; "
                    "Math.max(-0,+0)=+0 - BIT-LEVEL DIVERGENCE",
    "statement": "z'=h iff h>z ordered (C0=0,C3=0,C2=0); "
                 "otherwise z'=z bits unchanged. NOT equivalent to "
                 "Math.max for all bit patterns.",
}

out = {
    "witness_class": "MODEL_OF_INSTRUCTIONS (STATIC-ONLY; no processor "
                     "measurement, no client execution layer)",
    "pattern_sites": [
        "FUN_004C46C0 @0x004C4777-0x004C4790 (CREATE)",
        "FUN_0085B3E0 @0x0085B426-0x0085B441 (EXISTING)",
    ],
    "table": rows,
    "max_divergence": divergence,
}
with open(os.path.join(RAW, "F2_X87_TABLE.json"), "w") as f:
    json.dump(out, f, indent=1)
print("rows: %d" % len(rows))
for r in rows:
    print("%-34s C0=%d C2=%d C3=%d  z'=%s  h_stored=%s" % (
        r["case"], r["C0"], r["C2"], r["C3"], r["zprime_bits"],
        r["h_stored_to_zslot"]))
print("DONE -> 01_RAW/F2_X87_TABLE.json")
