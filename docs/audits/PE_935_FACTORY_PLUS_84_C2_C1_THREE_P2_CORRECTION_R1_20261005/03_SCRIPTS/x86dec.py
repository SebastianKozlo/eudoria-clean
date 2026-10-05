# x86dec.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005
# Shared corrected fail-closed 32-bit x86 instruction decoder.
# Copy lineage: C2 AF2 decoder + THIS run's P2-2/H1/H2 bounded hygiene
# corrections (Desktop post-audit PE_935_F84_C2_DESKTOP_POST_AUDIT_20261004
# findings C2-C2/P2 and the two bounded hygiene items H1/H2).
#
# THIS RUN'S CORRECTIONS vs the C2 decoder:
#   P2-2 (66 0F 8x near Jcc, BRANCH A): _2BYTE[0x80..0x8F] fixed 6-byte rel32
#      forms ignored the 66 operand-size override; in 32-bit mode 66 0F 8x is a
#      near Jcc rel16 (TOTAL length = prefixes + 2 opcode bytes + 2 rel16 = 5
#      with one prefix). The C2 decoder measured 7 for `66 0F 84 00 00`, so a
#      boundary stream landed on an E8 byte interior to the following MOV's
#      immediate and validate_direct_call fabricated a CALL edge
#      (TARGET 0x00A0000D on the NEW-G fixture). Fixed for the WHOLE
#      0x80..0x8F class: 66-prefixed near Jcc decode as rel16 (imm fields
#      recorded, rel16=True); 67-prefixed near Jcc REJECTED fail-closed (same
#      policy as the primary E8/E9 near branches); unprefixed 0F 8x rel32
#      unchanged (6 bytes). Independently oracle-checked against GNU objdump
#      (Binutils 2.44): `66 0f 84 00 00` = je rel16, length 5.
#   H1 (16-bit ModRM rm=7, bounded hygiene): REG16_ADDR_BASE mapped rm=7 to
#      "BP"; the correct 16-bit addressing table is rm=7 mod=0 [BX],
#      mod!=0 [BX+disp] (and rm=6 mod=0 [disp16], mod!=0 [BP+disp] - the rm=6
#      mod=0 case was already special-cased). The COMPLETE rm=0..7 table is
#      now correct and oracle-checked against GNU objdump (67 8B 07 =
#      mov eax,[bx], never [bp]). Lengths are UNCHANGED by this repair (base
#      register naming only), so no boundary stream shifts.
#   H2 (grouped-opcode validity, bounded hygiene): 0F BA and 0F 71/72/73
#      decoded EVERY ModRM.reg sub-opcode with a trailing imm8. Correction:
#      grouped-encoding validity is judged by opcode + ModRM.reg + ModRM.mod +
#      the relevant mandatory prefix, NOT by one shared reg whitelist:
#        * 0F BA: reg 4..7 (BT/BTS/BTR/BTC r/m,imm8) legal with ANY mod
#          (memory forms legal); reg 0..3 reserved -> REJECT fail-closed;
#        * 0F 71/72/73: the immediate-shift forms are REGISTER-ONLY
#          (mod must be 3, both MMX and SSE2; memory forms are invalid ->
#          REJECTED, never guessed as a valid immediate-shift instruction);
#          without 66: reg in {2,4,6} legal (MMX PSRLW/PSRAW/PSLLW,
#          PSRLD/PSRAD/PSLLD, PSRLQ/PSLLQ; 0F 73 reg {3,7} RESERVED without
#          66); with 66: reg in {2,4,6} legal (SSE2) and 66 0F 73 reg {3,7}
#          legal as PSRLDQ/PSLLDQ (mod=3 only) - these must NOT be
#          misreported as reserved; with F2/F3: no legal form -> REJECT;
#          reg {0,1,5} (and 7 for 71/72) reserved in every combination.
#      All legal/illegal controls below are oracle-checked against GNU
#      objdump (Binutils 2.44); (bad) verdicts are the oracle's REJECT.
#
# C2 CORRECTIONS vs the C1 decoder (each fixes a Desktop-post-audit AF2 finding):
#   1. SHUFPS-family length: 0F C6 /r ib takes a trailing imm8 (same for 0F C4
#      PINSRW / 0F C5 PEXTRW). The C1 table treated them as modrm-only (3-byte
#      0F C6 C0) and the SHUFPS imm8 could be promoted to CALL. Fixed: imm8 is
#      part of the instruction (0F C6 C0 xx = 4 bytes).
#   2. Address-size override (67) is decoded correctly for ModRM forms: the
#      16-bit addressing modes (rm=0..7, no SIB, disp16 for mod=2 / rm=6 mod=0)
#      are implemented. The C1 _parse_modrm IGNORED has67 and fabricated a
#      32-bit ModRM length (67 8B 06 84 00 -> 3 instead of the correct 5).
#   3. Operand-size-prefixed near branch: 66 E8 / 66 E9 decode as rel16 forms
#      (total length 1+1+2 with one prefix). The C1 REL32 handler ignored has66
#      and silently parsed 66 E8 as an ordinary five-byte E8 rel32.
#   4. Segment prefixes (26/2E/36/3E/64/65) are RECORDED on the instruction
#      (P3-A: FS:[0] SEH/TLS stores must be representable and separable from
#      [this+0] evidence). More than one segment prefix, or more than five
#      prefix bytes, is REJECTED fail-closed (the C1 loop silently stopped at
#      five prefixes and treated the sixth as an opcode).
#   5. TRUNCATION stays fail-closed (unchanged): if any byte of the instruction
#      lies outside the buffer, decode returns None (REJECT) - a length is
#      NEVER fabricated.
#   6. disp8/disp32 stay SIGNED (0x84 disp8 == -124 == -0x7C, never +0x84) and
#      full effective-address decode is kept (unchanged from C1).
# Unsupported encodings return None (DECODER_STATUS=REJECT/UNRESOLVED).
# Pure functions over byte buffers; this module opens no files.

import struct

REGS32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REGS8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
REGS16 = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]
# 16-bit addressing mode register roles (ModRM rm field, address-size 16)
# H1 CORRECTION: rm=7 is [BX]/[BX+disp] (C2 wrongly mapped it to "BP").
# Correct full table: rm=0 [BX+SI] 1 [BX+DI] 2 [BP+SI] 3 [BP+DI] 4 [SI]
# 5 [DI] 6 mod=0 [disp16] else [BP+disp] 7 mod=0 [BX] else [BX+disp].
REG16_ADDR_BASE = {0: "BX", 1: "BX", 2: "BP", 3: "BP", 4: "SI", 5: "DI", 6: "BP", 7: "BX"}
REG16_ADDR_INDEX = {0: "SI", 1: "DI", 2: "SI", 3: "DI", 4: None, 5: None, 6: None, 7: None}

# H2: grouped opcodes whose ModRM.reg selects the sub-encoding and whose
# trailing imm8 legality depends on (opcode, reg, mod, mandatory prefix).
_GROUP_IMM8_OPS = (0xBA, 0x71, 0x72, 0x73)


def _group_imm8_ok(op2, reg, mod, prefixes):
    """H2 grouped-encoding validity: True iff the sub-encoding selected by
    (opcode2, ModRM.reg, ModRM.mod, mandatory prefix) is a legal imm8 form.
    Reserved/invalid sub-opcodes -> False (REJECT fail-closed; the C2 decoder
    decoded every reg with its imm8). Oracle: GNU objdump Binutils 2.44
    ((bad) verdicts); see ORACLE_INDEPENDENT_RECORDS.json."""
    if op2 == 0xBA:
        # 0F BA /4 /5 /6 /7 = BT/BTS/BTR/BTC r/m,imm8 (memory forms legal);
        # reg 0..3 reserved
        return reg in (4, 5, 6, 7)
    if op2 in (0x71, 0x72, 0x73):
        # the immediate-shift forms are REGISTER-ONLY (mod must be 3)
        if mod != 3:
            return False
        if 0xF2 in prefixes or 0xF3 in prefixes:
            return False  # no legal F2/F3 form for these groups
        if 0x66 in prefixes:
            # SSE2: 71/72/73 reg {2,4,6}; 73 reg {3,7} = PSRLDQ/PSLLDQ
            return reg in (2, 4, 6) or (op2 == 0x73 and reg in (3, 7))
        # MMX: 71/72/73 reg {2,4,6}; 0F 73 reg {3,7} reserved without 66
        return reg in (2, 4, 6)
    return False

SEG_PREFIX = {0x26: "ES", 0x2E: "CS", 0x36: "SS", 0x3E: "DS", 0x64: "FS", 0x65: "GS"}
PFX_BYTES = {0x66, 0x67, 0xF0, 0xF2, 0xF3, 0x26, 0x2E, 0x36, 0x3E, 0x64, 0x65}


def s8(b):
    return b - 256 if (b & 0x80) else b


def s32(v):
    return v - (1 << 32) if (v & 0x80000000) else v


def _s16(v):
    return v - (1 << 16) if (v & 0x8000) else v


class Insn(object):
    __slots__ = ("start", "length", "prefixes", "has66", "has67", "segment",
                 "opcode", "opcode2", "mod", "reg", "rm", "memop", "ea_base",
                 "ea_index", "ea_scale", "ea16", "disp_width", "disp_raw",
                 "disp_signed", "imm_width", "imm_raw", "imm_signed",
                 "reg_name", "reg2_name", "rel16")

    def __init__(self):
        self.start = 0
        self.length = 0
        self.prefixes = []
        self.has66 = False
        self.has67 = False
        self.segment = None
        self.opcode = None
        self.opcode2 = None
        self.mod = None
        self.reg = None
        self.rm = None
        self.memop = False
        self.ea_base = None      # register number or None
        self.ea_index = None     # register number or None
        self.ea_scale = 1
        self.ea16 = False        # effective address uses 16-bit addressing (67)
        self.disp_width = 0
        self.disp_raw = None
        self.disp_signed = 0
        self.imm_width = 0
        self.imm_raw = None
        self.imm_signed = None
        self.reg_name = None
        self.reg2_name = None
        self.rel16 = False       # 66-prefixed E8/E9: near branch with rel16

    def ea_text(self):
        if not self.memop:
            return None
        regs = REGS16 if self.ea16 else REGS32
        if self.ea_base is None and self.ea_index is None:
            return "[%s]" % ("0x%08X" % self.disp_raw)
        parts = []
        if self.ea_base is not None:
            parts.append(regs[self.ea_base])
        if self.ea_index is not None:
            if self.ea_scale == 1:
                parts.append("%s" % regs[self.ea_index])
            else:
                parts.append("%s*%d" % (regs[self.ea_index], self.ea_scale))
        txt = "+".join(parts)
        if self.disp_signed == 0 and self.disp_width == 0:
            return "[%s]" % txt
        if self.disp_signed < 0:
            return "[%s-0x%X]" % (txt, -self.disp_signed)
        return "[%s+0x%X]" % (txt, self.disp_signed)

    def segment_qualified_ea_text(self):
        """EA text with the segment prefix explicit (P3-A disclosure)."""
        t = self.ea_text()
        if t is None:
            return None
        if self.segment:
            return "%s:%s" % (self.segment, t)
        return t


# ---------------- primary opcode table ----------------
# kind: ("F", n) fixed | ("M",) modrm | ("M8",) modrm+imm8 |
#       ("M32",) modrm+imm32 (imm16 with 66) | ("M8C",) modrm+imm8 if reg in 0..1 |
#       ("M32C",) modrm+imm32(16 w/66) if reg in 0..1 |
#       ("I8",) imm8 | ("I32",) imm32 (imm16 w/66) | ("MOFFS",) | ("REL32",)
_PRIMARY = {}
for _op in (0x00, 0x01, 0x02, 0x03, 0x08, 0x09, 0x0A, 0x0B, 0x10, 0x11, 0x12, 0x13,
            0x18, 0x19, 0x1A, 0x1B, 0x20, 0x21, 0x22, 0x23, 0x28, 0x29, 0x2A, 0x2B,
            0x30, 0x31, 0x32, 0x33, 0x38, 0x39, 0x3A, 0x3B, 0x62, 0x63, 0x84, 0x85,
            0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F,
            0xD0, 0xD1, 0xD2, 0xD3, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF,
            0xFE, 0xFF, 0xC4, 0xC5):
    _PRIMARY[_op] = ("M",)
for _op in (0x80, 0x82, 0x83, 0x6B, 0xC0, 0xC1, 0xC6):
    _PRIMARY[_op] = ("M8",)
for _op in (0x69, 0x81, 0xC7):
    _PRIMARY[_op] = ("M32",)
_PRIMARY[0xF6] = ("M8C",)
_PRIMARY[0xF7] = ("M32C",)
for _op in range(0x40, 0x50):
    _PRIMARY[_op] = ("F", 1)
for _op in range(0x50, 0x60):
    _PRIMARY[_op] = ("F", 1)
_PRIMARY[0x60] = ("F", 1)
_PRIMARY[0x61] = ("F", 1)
_PRIMARY[0x68] = ("I32",)
_PRIMARY[0x6A] = ("I8",)
for _op in range(0x6C, 0x70):
    _PRIMARY[_op] = ("F", 1)
for _op in range(0x70, 0x80):
    _PRIMARY[_op] = ("F", 2)
for _op in range(0x90, 0x9A):
    _PRIMARY[_op] = ("F", 1)
_PRIMARY[0x9B] = ("F", 1)
for _op in (0x9C, 0x9D, 0x9E, 0x9F):
    _PRIMARY[_op] = ("F", 1)
for _op in (0xA0, 0xA1, 0xA2, 0xA3):
    _PRIMARY[_op] = ("MOFFS",)
for _op in (0xA4, 0xA5, 0xA6, 0xA7, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF):
    _PRIMARY[_op] = ("F", 1)
_PRIMARY[0xA8] = ("I8",)
_PRIMARY[0xA9] = ("I32",)
for _op in range(0xB0, 0xB8):
    _PRIMARY[_op] = ("F", 2)
for _op in range(0xB8, 0xC0):
    _PRIMARY[_op] = ("I32",)
_PRIMARY[0xC2] = ("F", 3)
_PRIMARY[0xC3] = ("F", 1)
_PRIMARY[0xC8] = ("F", 4)
_PRIMARY[0xC9] = ("F", 1)
_PRIMARY[0xCA] = ("F", 3)
_PRIMARY[0xCB] = ("F", 1)
_PRIMARY[0xCC] = ("F", 1)
_PRIMARY[0xCD] = ("F", 2)
_PRIMARY[0xCE] = ("F", 1)
_PRIMARY[0xCF] = ("F", 1)
_PRIMARY[0xD4] = ("F", 2)
_PRIMARY[0xD5] = ("F", 2)
_PRIMARY[0xD6] = ("F", 1)
_PRIMARY[0xD7] = ("F", 1)
for _op in range(0xE0, 0xE8):
    _PRIMARY[_op] = ("F", 2)
_PRIMARY[0xE8] = ("REL32",)
_PRIMARY[0xE9] = ("REL32",)
_PRIMARY[0xEB] = ("F", 2)
for _op in (0xEC, 0xED, 0xEE, 0xEF):
    _PRIMARY[_op] = ("F", 1)
_PRIMARY[0xF4] = ("F", 1)
_PRIMARY[0xF5] = ("F", 1)
for _op in range(0xF8, 0xFE):
    _PRIMARY[_op] = ("F", 1)
# NOTE: 0x9A (CALL far) and 0xEA (JMP far) are deliberately NOT in the table:
# they are rejected fail-closed (their 16:32 operand layout is not required by
# this correction; rejecting is the contract-sanctioned fail-closed option).

# ---------------- two-byte (0F) opcode table ----------------
_2BYTE = {}
for _op in (0x00, 0x01, 0x02, 0x03):
    _2BYTE[_op] = ("M",)
_2BYTE[0x0B] = ("F", 2)
for _op in (0x0D, 0x18, 0x19, 0x1A, 0x1B, 0x1E, 0x1F):
    _2BYTE[_op] = ("M",)
for _op in range(0x20, 0x30):
    _2BYTE[_op] = ("M",)
for _op in range(0x30, 0x36):
    _2BYTE[_op] = ("F", 2)
for _op in range(0x40, 0x50):
    _2BYTE[_op] = ("M",)
for _op in range(0x50, 0x70):
    _2BYTE[_op] = ("M",)
_2BYTE[0x70] = ("M8",)
for _op in (0x71, 0x72, 0x73):
    _2BYTE[_op] = ("M8",)
for _op in range(0x74, 0x80):
    _2BYTE[_op] = ("M",)
for _op in range(0x80, 0x90):
    _2BYTE[_op] = ("F", 6)
for _op in range(0x90, 0xA0):
    _2BYTE[_op] = ("M",)
_2BYTE[0xA0] = ("F", 2)
_2BYTE[0xA1] = ("F", 2)
_2BYTE[0xA2] = ("F", 2)
_2BYTE[0xA3] = ("M",)
_2BYTE[0xA4] = ("M8",)
_2BYTE[0xA5] = ("M",)
_2BYTE[0xA8] = ("F", 2)
_2BYTE[0xA9] = ("F", 2)
_2BYTE[0xAA] = ("F", 2)
_2BYTE[0xAB] = ("M",)
_2BYTE[0xAC] = ("M8",)
_2BYTE[0xAD] = ("M",)
_2BYTE[0xAE] = ("M",)
_2BYTE[0xAF] = ("M",)
for _op in range(0xB0, 0xBA):
    _2BYTE[_op] = ("M",)
_2BYTE[0xBA] = ("M8",)
for _op in range(0xBB, 0xC0):
    _2BYTE[_op] = ("M",)
_2BYTE[0xC0] = ("M",)
_2BYTE[0xC1] = ("M",)
_2BYTE[0xC2] = ("M8",)
# AF2 class-B fix: 0F C4 PINSRW /r ib, 0F C5 PEXTRW /r ib and 0F C6 SHUFPS /r ib
# ALL carry a trailing imm8. The C1 table mapped C4/C5/C6 to modrm-only and the
# SHUFPS imm8 could be promoted to CALL (Desktop post-audit counterexample B).
_2BYTE[0xC4] = ("M8",)
_2BYTE[0xC5] = ("M8",)
_2BYTE[0xC6] = ("M8",)
for _op in range(0xC7, 0xC8):
    _2BYTE[_op] = ("M",)
for _op in range(0xC8, 0xD0):
    _2BYTE[_op] = ("F", 2)
for _op in range(0xD0, 0xF1):
    _2BYTE[_op] = ("M",)
for _op in range(0xF1, 0xF7):
    _2BYTE[_op] = ("M",)
_2BYTE[0xF7] = ("M",)
for _op in range(0xF8, 0x100):
    _2BYTE[_op] = ("M",)


def _parse_modrm32(buf, j):
    """32-bit-addressing ModRM(+SIB+disp) at buf[j]. dict or None (truncated)."""
    n = len(buf)
    if j >= n:
        return None
    m = buf[j]
    mod = m >> 6
    reg = (m >> 3) & 7
    rm = m & 7
    j += 1
    scale = 1
    index = None
    base = None
    disp_width = 0
    if mod != 3:
        if rm == 4:
            if j >= n:
                return None
            sib = buf[j]
            j += 1
            scale = 1 << (sib >> 6)
            index = (sib >> 3) & 7
            if index == 4:
                index = None
            base = sib & 7
            if mod == 0 and base == 5:
                base = None
                disp_width = 4
            elif mod == 1:
                disp_width = 1
            elif mod == 2:
                disp_width = 4
        else:
            if mod == 0:
                if rm == 5:
                    disp_width = 4  # [disp32] absolute: no base
                else:
                    base = rm
            elif mod == 1:
                base = rm
                disp_width = 1
            elif mod == 2:
                base = rm
                disp_width = 4
    disp_raw = None
    disp_signed = None
    if disp_width:
        if j + disp_width > n:
            return None
        if disp_width == 1:
            disp_raw = buf[j]
            disp_signed = s8(disp_raw)
        else:
            disp_raw = struct.unpack_from("<I", buf, j)[0]
            disp_signed = s32(disp_raw)
        j += disp_width
    return {"mod": mod, "reg": reg, "rm": rm, "scale": scale, "index": index,
            "base": base, "disp_width": disp_width, "disp_raw": disp_raw,
            "disp_signed": disp_signed, "after": j}


def _parse_modrm16(buf, j):
    """16-bit-addressing ModRM(+disp) at buf[j] (67 prefix active).
    AF2 class-C fix: the C1 decoder ignored has67 and fabricated a 32-bit
    ModRM length (67 8B 06 84 00 measured 3 instead of the correct 5).
    Correct 16-bit modes: rm=0 [BX+SI] 1 [BX+DI] 2 [BP+SI] 3 [BP+DI]
    4 [SI] 5 [DI] 6 mod0=[disp16] else [BP+disp] 7 mod0=[BX] else [BX+disp];
    mod=1 +disp8, mod=2 +disp16; NO SIB byte in 16-bit addressing.
    (H1: rm=7 is [BX]/[BX+disp]; the C2 table wrongly said [BP].)"""
    n = len(buf)
    if j >= n:
        return None
    m = buf[j]
    mod = m >> 6
    reg = (m >> 3) & 7
    rm = m & 7
    j += 1
    base = None
    index = None
    disp_width = 0
    if mod != 3:
        base = REG16_ADDR_BASE[rm]
        index = REG16_ADDR_INDEX[rm]
        if rm == 6 and mod == 0:
            base = None   # [disp16] absolute in 16-bit addressing
            disp_width = 2
        elif mod == 1:
            disp_width = 1
        elif mod == 2:
            disp_width = 2
    disp_raw = None
    disp_signed = None
    if disp_width:
        if j + disp_width > n:
            return None
        if disp_width == 1:
            disp_raw = buf[j]
            disp_signed = s8(disp_raw)
        else:
            disp_raw = struct.unpack_from("<H", buf, j)[0]
            disp_signed = _s16(disp_raw)
        j += disp_width
    return {"mod": mod, "reg": reg, "rm": rm, "scale": 1, "index": index,
            "base": base, "disp_width": disp_width, "disp_raw": disp_raw,
            "disp_signed": disp_signed, "after": j}


def _parse_modrm(buf, j, has67):
    if has67:
        return _parse_modrm16(buf, j)
    return _parse_modrm32(buf, j)


# 16-bit addressing base/index names are register NUMBERS into REGS16 via a
# dedicated map: we return name-keyed numbers by resolving to REGS16 indices.
def _reg16_num(name):
    return REGS16.index(name)


def decode(buf, i):
    """Decode one instruction at buf[i]. Returns Insn or None (UNKNOWN/TRUNCATED).
    Fail-closed: any unsupported/ambiguous encoding -> None; a length is never
    guessed and a byte inside an unsupported instruction is never exposed as an
    instruction start by this module."""
    n = len(buf)
    if i < 0 or i >= n:
        return None
    ins = Insn()
    ins.start = i
    j = i
    seg_seen = None
    while j < n and buf[j] in PFX_BYTES:
        if len(ins.prefixes) >= 5:
            return None  # more than 5 prefix bytes: reject fail-closed
        b = buf[j]
        ins.prefixes.append(b)
        if b == 0x66:
            ins.has66 = True
        elif b == 0x67:
            ins.has67 = True
        elif b in SEG_PREFIX:
            if seg_seen is not None:
                return None  # two segment prefixes: reject fail-closed
            seg_seen = SEG_PREFIX[b]
        j += 1
    ins.segment = seg_seen
    if j >= n:
        return None
    op = buf[j]
    if op == 0x0F:
        j += 1
        if j >= n:
            return None
        op2 = buf[j]
        if op2 not in _2BYTE:
            return None
        kind = _2BYTE[op2]
        ins.opcode = 0x0F
        ins.opcode2 = op2
        j += 1
    else:
        if op not in _PRIMARY:
            return None
        kind = _PRIMARY[op]
        ins.opcode = op
        j += 1
    kn = kind[0]
    if kn == "F":
        # kind[1] = TOTAL instruction length (opcode bytes included, prefixes
        # excluded): primary opcodes consume 1 byte, 0F-prefixed consume 2.
        # P2-2 BRANCH A: near Jcc 0F 80..8F with the 66 operand-size override
        # is a rel16 form in 32-bit mode (GNU objdump: 66 0f 84 00 00 = je
        # rel16, length 5), NOT the fixed 7-byte prefixed rel32 the C2 table
        # fabricated (which exposed interior data bytes as instruction starts
        # and fabricated CALL edges - Desktop post-audit NEW-G fixture).
        if ins.opcode == 0x0F and 0x80 <= op2 <= 0x8F:
            if ins.has67:
                return None  # address-size-prefixed near branch: reject (policy)
            if ins.has66:
                ins.rel16 = True
                j += 2
                if j > n:
                    return None
                ins.imm_width = 2
                ins.imm_raw = int.from_bytes(buf[j - 2:j], "little")
                ins.imm_signed = _s16(ins.imm_raw)
                ins.length = j - i
                return ins
        j += kind[1] - (2 if ins.opcode == 0x0F else 1)
        if j > n:
            return None
    elif kn == "REL32":
        if ins.has67:
            return None  # address-size-prefixed near branch: reject fail-closed
        if ins.has66:
            # AF2 class-D fix: 66 E8 / 66 E9 is a rel16 near branch
            # (CALL/JMP rel16), NOT an ordinary five-byte rel32.
            ins.rel16 = True
            j += 2
            if j > n:
                return None
            ins.imm_width = 2
            ins.imm_raw = int.from_bytes(buf[j - 2:j], "little")
            ins.imm_signed = _s16(ins.imm_raw)
        else:
            j += 4
            if j > n:
                return None
    elif kn == "MOFFS":
        if ins.has67 or ins.has66:
            return None  # 16-bit moffs forms: reject fail-closed
        j += 4
        if j > n:
            return None
        ins.memop = True
        ins.ea_base = None
        ins.ea_index = None
        ins.disp_width = 4
        ins.disp_raw = struct.unpack_from("<I", buf, j - 4)[0]
        ins.disp_signed = s32(ins.disp_raw)
    elif kn in ("I8", "I32"):
        w = 1 if kn == "I8" else (2 if ins.has66 else 4)
        if j + w > n:
            return None
        ins.imm_width = w
        ins.imm_raw = int.from_bytes(buf[j:j + w], "little")
        ins.imm_signed = s8(ins.imm_raw) if w == 1 else (
            _s16(ins.imm_raw) if w == 2 else s32(ins.imm_raw))
        j += w
    else:  # modrm-based
        mm = _parse_modrm(buf, j, ins.has67)
        if mm is None:
            return None
        ins.mod = mm["mod"]
        ins.reg = mm["reg"]
        ins.rm = mm["rm"]
        if ins.mod != 3:
            ins.memop = True
            ins.ea16 = ins.has67
            bn = mm["base"]
            ix = mm["index"]
            ins.ea_base = _reg16_num(bn) if (ins.has67 and bn is not None) else bn
            ins.ea_index = _reg16_num(ix) if (ins.has67 and ix is not None) else ix
            ins.ea_scale = mm["scale"]
            ins.disp_width = mm["disp_width"]
            ins.disp_raw = mm["disp_raw"] if mm["disp_width"] else 0
            ins.disp_signed = mm["disp_signed"] if mm["disp_width"] else 0
        j = mm["after"]
        if kn == "M8":
            if ins.opcode == 0x0F and ins.opcode2 in _GROUP_IMM8_OPS:
                # H2: grouped encodings (0F BA, 0F 71/72/73) judge validity by
                # opcode + ModRM.reg + ModRM.mod + mandatory prefix; reserved/
                # invalid sub-opcodes REJECT fail-closed (C2 decoded every reg
                # with the imm8). A REJECT never leaves a guessed length: the
                # undecodable byte is never exposed as an instruction start.
                if not _group_imm8_ok(ins.opcode2, mm["reg"], mm["mod"],
                                      ins.prefixes):
                    return None
            w = 1
        elif kn == "M32":
            w = 2 if ins.has66 else 4
        elif kn == "M8C":
            w = 1 if ins.reg in (0, 1) else 0
        elif kn == "M32C":
            w = (2 if ins.has66 else 4) if ins.reg in (0, 1) else 0
        else:
            w = 0
        if w:
            if j + w > n:
                return None
            ins.imm_width = w
            ins.imm_raw = int.from_bytes(buf[j:j + w], "little")
            ins.imm_signed = s8(ins.imm_raw) if w == 1 else (
                _s16(ins.imm_raw) if w == 2 else s32(ins.imm_raw))
            j += w
    if j > n:
        return None
    ins.length = j - i
    if ins.length <= 0:
        return None
    return ins


def decode_at(buf, i):
    """decode() alias for readability."""
    return decode(buf, i)


def call_operand_rel32(buf, i):
    """For a raw E8/E9 opcode at buf[i] with NO prefixes, return the signed
    rel32 read from buf[i+1..i+4] (bounds-checked) or None. This helper does NOT
    validate prefixes or boundaries; the only sanctioned promotion path is
    pebnd.validate_direct_call."""
    if i < 0 or i + 5 > len(buf) or buf[i] not in (0xE8, 0xE9):
        return None
    return s32(struct.unpack_from("<I", buf, i + 1)[0])
