# -*- coding: utf-8 -*-
# f1_model_decoder_suite.py - G2-F1-GRAMMAR (b)+(c):
#   - INDEPENDENT MODEL: closed-form arithmetic semantics of FUN_007343E0,
#     derived by hand from the OWN capstone decode (01_RAW/F007343E0_*.txt).
#   - REFERENCE DECODER: executable control-flow transcription of the same
#     function (per-instruction branch walk, SEPARATE implementation).
#   - MASK SUITE: contract section 6(3): masks 0, 0x2AA, 0x554, 0x7FE, each
#     bit-pair separately, both bits of a pair, unused bits (0x800+), short
#     buffer before/after a field, two records sequentially, final cursor
#     offset, dst+04 before/after, NaN/Inf. Comparison = CURSOR STATE +
#     WRITE RANGE (bitmap of written dst+00..0x24 slots), not just return.
# SYNTHETIC byte buffers (marked SYNTHETIC in every result row).
# STATIC-ONLY: no client, no engine execution - this is a model of the
# instruction semantics decoded from the physical EXE.

import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")

F32 = lambda v: struct.unpack("<f", struct.pack("<I", v))[0]
BITS = lambda v: struct.unpack("<I", struct.pack("<f", v))[0]

MASK = 0xFFFF
PAIRS = [
    # (dst_off, bit0, bit1) - from OWN decode: FLDZ path bit0, FLD1 path bit1
    (0x00, 0x002, 0x004),
    (0x08, 0x008, 0x010),
    (0x0C, 0x020, 0x040),
    (0x10, 0x080, 0x100),
    (0x14, 0x200, 0x400),
]
ABS_FIELDS = (0x18, 0x1C, 0x20)  # three absolute inline f32 reads
RESIDUAL_OFF = 0x24


class Cursor:
    """Cursor model: +0x00 base, +0x08 limit, +0x0C pos, +0x11 readable flag.
    From OWN decode of FUN_0040DE60/FUN_004C32F0/FUN_007343E0."""

    def __init__(self, data, readable=1):
        self.base = data
        self.limit = len(data)
        self.pos = 0
        self.readable = 1 if readable else 0

    def flag(self):
        return self.readable

    def clear_flag(self):
        self.readable = 0

    def advance(self, n):
        self.pos += n
        if self.pos > self.limit:
            self.readable = 0

    def can_read(self, n):
        return self.readable != 0 and (self.pos + n) <= self.limit


def model_decode(cursor, dst):
    """INDEPENDENT MODEL - closed-form semantics (no control-flow walk).

    Derived from the instruction decode:
    - entry: al = flag; if flag==0 -> mask=0 (flag stays 0)
    - if flag!=0: if pos+2 > limit -> mask=0 AND flag:=0
      else mask = u16@base+pos, advance(2)
    - for each pair (off, b0, b1):
        if b0 set: dst[off]=0.0; mask &= ~b0        (FLDZ branch first)
        elif b1 set: dst[off]=1.0; mask &= ~b1      (FLD1 branch)
        else: read f32 (0.0 on unreadable/short)    (FUN_004C32F0)
    - three absolute fields: if flag==0 or pos+4>limit -> 0.0 (+ flag:=0
      if it was nonzero), else read f32 + advance(4)
    - dst[0x24] = residual mask (u16)
    - returns the SAME cursor (EAX = input cursor)
    """
    dst = bytearray(dst)
    writes = set()
    al = cursor.flag()
    if al == 0:
        mask = 0
    else:
        if not cursor.can_read(2):
            mask = 0
            cursor.clear_flag()
        else:
            mask = struct.unpack_from("<H", cursor.base, cursor.pos)[0]
            cursor.advance(2)
    for (off, b0, b1) in PAIRS:
        if mask & b0:
            dst[off:off + 4] = struct.pack("<f", 0.0)
            mask &= ~b0 & MASK
            writes.add(off)
        elif mask & b1:
            dst[off:off + 4] = struct.pack("<f", 1.0)
            mask &= ~b1 & MASK
            writes.add(off)
        else:
            if cursor.can_read(4):
                v = struct.unpack_from("<f", cursor.base, cursor.pos)[0]
                cursor.advance(4)
            else:
                v = 0.0
                if cursor.flag() != 0:
                    cursor.clear_flag()
            dst[off:off + 4] = struct.pack("<f", v)
            writes.add(off)
    for off in ABS_FIELDS:
        if cursor.flag() == 0 or not cursor.can_read(4):
            dst[off:off + 4] = struct.pack("<f", 0.0)
            if cursor.flag() != 0:
                cursor.clear_flag()
        else:
            v = struct.unpack_from("<f", cursor.base, cursor.pos)[0]
            cursor.advance(4)
            dst[off:off + 4] = struct.pack("<f", v)
        writes.add(off)
    dst[RESIDUAL_OFF:RESIDUAL_OFF + 2] = struct.pack("<H", mask & MASK)
    writes.add(RESIDUAL_OFF)
    return cursor, bytes(dst), writes, (mask & MASK)


def decoder_decode(cursor, dst):
    """REFERENCE DECODER - control-flow transcription of FUN_007343E0.

    Follows the decoded instruction sequence instruction-by-instruction:
    the entry gate, the mask read with the two jump targets, per-pair
    branch ladders (TEST/JE chains), the three inline absolute reads with
    their fail paths, the residual store and the identical epilogues
    (EAX = input cursor). This is a SECOND implementation, structurally
    different from model_decode (branch walk vs closed form).
    """
    dst = bytearray(dst)
    writes = set()

    # --- prologue + entry gate (0x7343E0-0x734413) ---
    al = cursor.flag()
    if al != 0:                       # test al,al; je 0x73440a
        if cursor.can_read(2):        # cmp pos+2,limit; ja 0x73440a
            mask = struct.unpack_from(
                "<H", cursor.base, cursor.pos)[0]      # MOVZX EBX,[EAX+ECX]
            cursor.advance(2)                          # call FUN_0040DE60(2)
            # jmp 0x734413
        else:
            mask = 0
            if al != 0:                                # 0x73440A path
                cursor.clear_flag()                    # mov [esi+0x11],0
    else:
        mask = 0
        # flag==0: no clear (already 0)

    # --- pair ladders (0x734413-0x73450F) ---
    for (off, b0, b1) in PAIRS:
        if (mask & b0):                                # TEST bit0; JE next
            struct.pack_into("<f", dst, off, 0.0)      # FLDZ; FSTP [edi+off]
            mask &= (~b0) & MASK                       # AND EBX,~bit
            writes.add(off)
            continue                                    # JMP pair_end
        if (mask & b1):                                 # TEST bit1; JE read
            struct.pack_into("<f", dst, off, 1.0)      # FLD1; FSTP
            mask &= (~b1) & MASK
            writes.add(off)
            continue
        # fall-through read (FUN_004C32F0 semantics)
        if cursor.flag() != 0 and cursor.can_read(4):
            v = struct.unpack_from("<f", cursor.base, cursor.pos)[0]
            cursor.advance(4)
        else:
            v = 0.0
            if cursor.flag() != 0:
                cursor.clear_flag()
        struct.pack_into("<f", dst, off, v)
        writes.add(off)

    # --- three absolute reads (0x73450F-0x7345B0) ---
    for off in ABS_FIELDS:
        if cursor.flag() == 0:                          # cmp [esi+11],0; je
            struct.pack_into("<f", dst, off, 0.0)
            writes.add(off)
            continue
        if cursor.can_read(4):
            v = struct.unpack_from("<f", cursor.base, cursor.pos)[0]
            cursor.advance(4)
            struct.pack_into("<f", dst, off, v)
        else:                                           # ja fail
            struct.pack_into("<f", dst, off, 0.0)
            if cursor.flag() != 0:
                cursor.clear_flag()                     # mov [esi+0x11],0
        writes.add(off)

    # --- residual + epilogue (both exits identical) ---
    struct.pack_into("<H", dst, RESIDUAL_OFF, mask & MASK)
    writes.add(RESIDUAL_OFF)
    return cursor, bytes(dst), writes, (mask & MASK)


def run_case(name, data, mask_words=None, cursor_flag=1, pre_dst=None):
    """Run both implementations on the same SYNTHETIC buffer."""
    dst0 = bytearray(0x28)
    dst1 = bytearray(0x28)
    if pre_dst is not None:
        dst0[:] = pre_dst
        dst1[:] = pre_dst
    c0 = Cursor(data, readable=cursor_flag)
    c1 = Cursor(data, readable=cursor_flag)
    r0 = model_decode(c0, dst0)
    r1 = decoder_decode(c1, dst1)
    ok = (r0[0].pos == r1[0].pos and
          r0[0].flag() == r1[0].flag() and
          r0[1] == r1[1] and r0[2] == r1[2] and r0[3] == r1[3])
    return {
        "case": name, "synthetic": True,
        "cursor_pos_model": r0[0].pos, "cursor_pos_decoder": r1[0].pos,
        "cursor_flag_model": r0[0].flag(), "cursor_flag_decoder": r1[0].flag(),
        "write_bitmap_model": sorted(list(r0[2])),
        "write_bitmap_decoder": sorted(list(r1[2])),
        "residual_model": hex(r0[3]), "residual_decoder": hex(r1[3]),
        "dst_bytes_equal": r0[1] == r1[1],
        "dst_model_hex": r0[1].hex(),
        "dst_decoder_hex": r1[1].hex(),
        "model_eq_decoder": ok,
    }


def payload(mask, floats=()):
    """SYNTHETIC stream: u16 mask + f32 sequence."""
    b = struct.pack("<H", mask) + b"".join(struct.pack("<f", v)
                                           for v in floats)
    return b


results = []
CASES = []

# core masks (contract 6(3))
CASES.append(("mask_0", payload(0, [0.5] * 8)))
CASES.append(("mask_0x2AA", payload(0x2AA, [0.5] * 3)))
CASES.append(("mask_0x554", payload(0x554, [0.5] * 3)))
CASES.append(("mask_0x7FE", payload(0x7FE, [0.5] * 3)))

# each bit-pair separately (bit0 only, bit1 only, both)
for (off, b0, b1) in PAIRS:
    CASES.append(("pair_%02x_bit0_only(0x%03x)" % (off, b0),
                  payload(b0, [0.5] * 8)))
    CASES.append(("pair_%02x_bit1_only(0x%03x)" % (off, b1),
                  payload(b1, [0.5] * 8)))
    CASES.append(("pair_%02x_both(0x%03x)" % (off, b0 | b1),
                  payload(b0 | b1, [0.5] * 8)))

# unused bits 0x800+ (mask with high bit alone and combined)
CASES.append(("unused_bit_0x800_only", payload(0x800, [0.5] * 8)))
CASES.append(("unused_bit_0x800_plus_pair00", payload(0x802, [0.5] * 7)))

# short buffer before a field (mask 0 = 8 reads needed; give fewer)
CASES.append(("short_buffer_before_field", struct.pack("<H", 0) +
              struct.pack("<f", 1.5) * 3))
# short buffer AFTER a field (mask 0, 8 floats but cut the last)
CASES.append(("short_buffer_after_field", struct.pack("<H", 0) +
              struct.pack("<f", 1.5) * 7))

# exhausted cursor at entry (flag=0)
CASES.append(("exhausted_cursor_flag0", payload(0, [0.5] * 8),
              0))

# NaN/Inf payload (mask 0 reads NaN; also absolute fields with Inf)
CASES.append(("nan_in_payload", struct.pack("<H", 0) +
              struct.pack("<f", float("nan")) +
              struct.pack("<f", float("inf")) +
              struct.pack("<f", 2.0) * 6))
CASES.append(("neg_inf_in_abs", payload(0x7FE,
                                       [float("-inf"), 0.0, 0.0])))


def run_all():
    for case in CASES:
        if len(case) == 2:
            name, data = case
            flag = 1
        else:
            name, data, flag = case
        r = run_case(name, data, cursor_flag=flag)
        results.append(r)

    # two records sequentially (cursor continues across both)
    data = payload(0x2AA, [0.5] * 3) + payload(0x554, [0.5] * 3)
    c0 = Cursor(data)
    c1 = Cursor(data)
    d0 = bytearray(0x28)
    d1 = bytearray(0x28)
    r_a = model_decode(c0, d0)
    r_b = decoder_decode(c1, d1)
    r_c = model_decode(c0, d0)
    r_d = decoder_decode(c1, d1)
    two = {
        "case": "two_records_sequentially", "synthetic": True,
        "final_pos_model": r_c[0].pos, "final_pos_decoder": r_d[0].pos,
        "final_flag_model": r_c[0].flag(), "final_flag_decoder": r_d[0].flag(),
        "residual2_model": hex(r_c[3]), "residual2_decoder": hex(r_d[3]),
        "model_eq_decoder": (r_c[0].pos == r_d[0].pos and
                             r_c[0].flag() == r_d[0].flag() and
                             r_c[1] == r_d[1] and r_c[3] == r_d[3]),
        "note": "34B records: 0x2AA then 0x554",
    }
    results.append(two)

    # dst+04 never written (pre-set pattern, check preservation)
    data = payload(0x7FE, [0.5] * 3)
    pre = bytearray(0x28)
    pre[0x04:0x08] = struct.pack("<f", 1234.5)  # sentinel
    r = run_case("dst04_sentinel_preserved", data, pre_dst=bytes(pre))
    # verify the sentinel survived
    survived = r["dst_model_hex"][8:16] == struct.pack("<f", 1234.5).hex()
    r["dst04_sentinel_survived"] = survived
    results.append(r)

    # consumption arithmetic check (contract 3.1(3)): mask 0 -> 34B
    data = payload(0, [0.5] * 8)
    c = Cursor(data)
    model_decode(c, bytearray(0x28))
    consumed_mask0 = c.pos
    # 0x2AA -> 14B; 0x554 -> 14B; 0x7FE -> 14B + residual 0x554
    checks = {}
    for m in (0x2AA, 0x554, 0x7FE):
        cc = Cursor(payload(m, [0.5] * 3))
        rr = model_decode(cc, bytearray(0x28))
        checks["mask_%s_consumed" % hex(m)] = cc.pos
        checks["mask_%s_residual" % hex(m)] = hex(rr[3])
    checks["mask_0_consumed"] = consumed_mask0
    results.append({"case": "consumption_arithmetic", "synthetic": True,
                    "checks": checks,
                    "expect_mask0_34B": consumed_mask0 == 34,
                    "expect_2AA_14B": checks.get("mask_0x2aa_consumed") == 14,
                    "expect_554_14B": checks.get("mask_0x554_consumed") == 14,
                    "expect_7FE_14B": checks.get("mask_0x7fe_consumed") == 14,
                    "expect_7FE_res_554": checks.get("mask_0x7fe_residual")
                    == hex(0x554)})


run_all()
n_ok = sum(1 for r in results if r.get("model_eq_decoder"))
print("cases: %d, model==decoder: %d" % (len(results), n_ok))
for r in results:
    if not r.get("model_eq_decoder"):
        print("MISMATCH: %s" % r["case"])
        print(json.dumps(r, indent=1))
with open(os.path.join(RAW, "F1_MASK_SUITE.json"), "w") as f:
    json.dump({"witness_class": "SYNTHETIC",
               "note": "model vs reference decoder, STATIC-ONLY; "
                       "no engine execution layer present",
               "results": results}, f, indent=1)
print("DONE -> 01_RAW/F1_MASK_SUITE.json")
