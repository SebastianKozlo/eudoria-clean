# x86dec.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# Shared corrected 32-bit x86 instruction decoder (F84-C2 repair).
#
# CORRECTION vs the historical s2_write_census.py mini decoder:
#   1. mod=0 with SIB (rm==4) is decoded (SIB + optional base=5 disp32).
#   2. 66-prefixed immediate widths are correct (66 B8 imm16 -> total length 4).
#   3. TRUNCATION is fail-closed: if any byte of the instruction lies outside the
#      buffer, decode returns None (REJECT) - a length is NEVER fabricated.
#   4. disp8 is SIGNED (raw 0x84 == -124 == -0x7C, never +0x84).
#   5. Full effective-address decode: base_register, index_register, scale,
#      raw_displacement, signed_displacement, effective_displacement.
#   6. Unsupported encodings return None (DECODER_STATUS=UNRESOLVED).
# Pure functions over byte buffers; this module opens no files.

import struct

REGS32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REGS8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
REGS16 = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]

PFX_BYTES = {0x66, 0x67, 0xF0, 0xF2, 0xF3, 0x26, 0x2E, 0x36, 0x3E, 0x64, 0x65}


def s8(b):
    return b - 256 if (b & 0x80) else b


def s32(v):
    return v - (1 << 32) if (v & 0x80000000) else v


def _s16(v):
    return v - (1 << 16) if (v & 0x8000) else v


class Insn(object):
    __slots__ = ("start", "length", "prefixes", "has66", "has67", "opcode",
                 "opcode2", "mod", "reg", "rm", "memop", "ea_base", "ea_index",
                 "ea_scale", "disp_width", "disp_raw", "disp_signed",
                 "imm_width", "imm_raw", "imm_signed", "reg_name", "reg2_name")

    def __init__(self):
        self.start = 0
        self.length = 0
        self.prefixes = []
        self.has66 = False
        self.has67 = False
        self.opcode = None
        self.opcode2 = None
        self.mod = None
        self.reg = None
        self.rm = None
        self.memop = False
        self.ea_base = None      # register number or None
        self.ea_index = None     # register number or None
        self.ea_scale = 1
        self.disp_width = 0
        self.disp_raw = None
        self.disp_signed = 0
        self.imm_width = 0
        self.imm_raw = None
        self.imm_signed = None
        self.reg_name = None
        self.reg2_name = None

    def ea_text(self):
        if not self.memop:
            return None
        if self.ea_base is None and self.ea_index is None:
            return "[0x%08X]" % self.disp_raw
        parts = []
        if self.ea_base is not None:
            parts.append(REGS32[self.ea_base])
        if self.ea_index is not None:
            if self.ea_scale == 1:
                parts.append("%s" % REGS32[self.ea_index])
            else:
                parts.append("%s*%d" % (REGS32[self.ea_index], self.ea_scale))
        txt = "+".join(parts)
        if self.disp_signed == 0 and self.disp_width == 0:
            return "[%s]" % txt
        if self.disp_signed < 0:
            return "[%s-0x%X]" % (txt, -self.disp_signed)
        return "[%s+0x%X]" % (txt, self.disp_signed)


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
for _op in range(0xC3, 0xC8):
    _2BYTE[_op] = ("M",)
_2BYTE[0xC7] = ("M",)
for _op in range(0xC8, 0xD0):
    _2BYTE[_op] = ("F", 2)
for _op in range(0xD0, 0xF1):
    _2BYTE[_op] = ("M",)
for _op in range(0xF1, 0xF7):
    _2BYTE[_op] = ("M",)
_2BYTE[0xF7] = ("M",)
for _op in range(0xF8, 0x100):
    _2BYTE[_op] = ("M",)


def _parse_modrm(buf, j, has67):
    """Parse ModRM(+SIB+disp) at buf[j]. Returns dict or None (truncated/unknown)."""
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


def decode(buf, i):
    """Decode one instruction at buf[i]. Returns Insn or None (UNKNOWN/TRUNCATED)."""
    n = len(buf)
    if i < 0 or i >= n:
        return None
    ins = Insn()
    ins.start = i
    j = i
    while j < n and buf[j] in PFX_BYTES and len(ins.prefixes) < 5:
        b = buf[j]
        ins.prefixes.append(b)
        if b == 0x66:
            ins.has66 = True
        elif b == 0x67:
            ins.has67 = True
        j += 1
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
        j += kind[1] - (2 if ins.opcode == 0x0F else 1)
        if j > n:
            return None
    elif kn == "REL32":
        if ins.has67:
            return None  # 16-bit rel addressing unsupported -> fail-closed
        j += 4
        if j > n:
            return None
    elif kn == "MOFFS":
        if ins.has67:
            return None
        j += 4
        if j > n:
            return None
        ins.memop = True
        ins.ea_base = None
        ins.ea_index = None
        if j - 4 + 4 <= n:
            ins.disp_width = 4
            ins.disp_raw = struct.unpack_from("<I", buf, j - 4)[0]
            ins.disp_signed = s32(ins.disp_raw)
        else:
            return None
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
            ins.ea_base = mm["base"]
            ins.ea_index = mm["index"]
            ins.ea_scale = mm["scale"]
            ins.disp_width = mm["disp_width"]
            ins.disp_raw = mm["disp_raw"] if mm["disp_width"] else 0
            ins.disp_signed = mm["disp_signed"] if mm["disp_width"] else 0
        j = mm["after"]
        if kn == "M8":
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
    rel32 read from buf[i+1..i+4] (bounds-checked) or None."""
    if i < 0 or i + 5 > len(buf) or buf[i] not in (0xE8, 0xE9):
        return None
    return s32(struct.unpack_from("<I", buf, i + 1)[0])
