#!/usr/bin/env python3
# QC-R3 own PE32 parser + targeted x86-32 decoder (fresh independent QC tool; no executor code).
"""Minimal PE32 parser and x86 (32-bit) instruction decoder sufficient for the pinned windows.
Written from scratch for QC_R3 (pe-master-auditor fresh session). Covers the opcode subset
used by the Entropia.exe code under audit; unknown opcodes raise DecodeError (fail-closed)."""
import struct

class DecodeError(Exception):
    pass

REG32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REG8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
REG16 = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]

class PE32:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.data = f.read()
        b = self.data
        if b[0:2] != b"MZ":
            raise ValueError("no MZ")
        e_lfanew = struct.unpack_from("<I", b, 0x3C)[0]
        if b[e_lfanew:e_lfanew+4] != b"PE\x00\x00":
            raise ValueError("no PE sig")
        coff = e_lfanew + 4
        self.machine, self.num_sections = struct.unpack_from("<HH", b, coff)
        (self.size_opt,) = struct.unpack_from("<H", b, coff + 16)
        opt = coff + 20
        magic = struct.unpack_from("<H", b, opt)[0]
        if magic != 0x10B:
            raise ValueError(f"not PE32 magic {magic:#x}")
        self.image_base = struct.unpack_from("<I", b, opt + 28)[0]
        (self.sect_align, self.file_align) = struct.unpack_from("<II", b, opt + 32)
        sec_tbl = opt + self.size_opt
        self.sections = []
        for i in range(self.num_sections):
            off = sec_tbl + 40 * i
            name = b[off:off+8].rstrip(b"\x00").decode("ascii", "replace")
            (vsize,) = struct.unpack_from("<I", b, off + 8)
            (va,) = struct.unpack_from("<I", b, off + 12)
            (rsize,) = struct.unpack_from("<I", b, off + 16)
            (fo,) = struct.unpack_from("<I", b, off + 20)
            (chars,) = struct.unpack_from("<I", b, off + 36)
            self.sections.append({"name": name, "vsize": vsize, "va": va, "rsize": rsize,
                                  "fo": fo, "chars": chars})
        self.dos_stub = None

    def va_to_fo(self, va):
        rva = va - self.image_base
        return self.rva_to_fo(rva)

    def rva_to_fo(self, rva):
        for s in self.sections:
            lo = s["va"]
            hi = s["va"] + max(s["vsize"], s["rsize"])
            if lo <= rva < hi:
                fo = rva - s["va"] + s["fo"]
                if fo < s["fo"] + s["rsize"]:
                    return fo
                return None  # in virtual size only
        return None

    def fo_to_va(self, fo):
        for s in self.sections:
            if s["fo"] <= fo < s["fo"] + s["rsize"]:
                return self.image_base + s["va"] + (fo - s["fo"])
        return None

    def read_va(self, va, n):
        fo = self.va_to_fo(va)
        if fo is None:
            raise DecodeError(f"VA {va:#x} not mapped to file")
        return self.data[fo:fo+n]

    def u32_at_va(self, va):
        return struct.unpack("<I", self.read_va(va, 4))[0]

class Decoded:
    __slots__ = ("va", "bytes", "mnemonic", "operands", "length", "target")
    def __init__(self, va, bs, mn, ops, length, target=None):
        self.va = va; self.bytes = bs; self.mnemonic = mn; self.operands = ops
        self.length = length; self.target = target
    def __repr__(self):
        return f"{self.va:#010x}: {self.bytes.hex():<24} {self.mnemonic} {','.join(self.operands)}"

# group opcodes
G1 = ["ADD", "OR", "ADC", "SBB", "AND", "SUB", "XOR", "CMP"]
G2 = ["ROL", "ROR", "RCL", "RCR", "SHL", "SHR", "SAL", "SAR"]
G3_8 = {0: "TEST", 2: "NOT", 3: "NEG", 4: "MUL", 5: "IMUL", 6: "DIV", 7: "IDIV"}
G5 = {0: "INC", 1: "DEC", 2: "CALL", 4: "JMP", 6: "PUSH"}
JCC = ["JO", "JNO", "JB", "JAE", "JE", "JNE", "JBE", "JA", "JS", "JNS", "JP", "JNP",
       "JL", "JGE", "JLE", "JG"]
SETCC = JCC  # same conditions
SIZES = {0: "byte", 1: "word", 2: "dword"}

def decode_modrm(b, i, opsize=2):
    """Return (reg, rm_text, new_i, disp) using bytes b starting at index i."""
    modrm = b[i]; i += 1
    mod = modrm >> 6; reg = (modrm >> 3) & 7; rm = modrm & 7
    size = SIZES[opsize]
    disp = 0
    if mod == 3:
        if opsize == 0:
            return reg, REG8[rm], i, 0, rm
        if opsize == 1:
            return reg, REG16[rm], i, 0, rm
        return reg, REG32[rm], i, 0, rm
    if rm == 4 and mod != 3:  # SIB
        sib = b[i]; i += 1
        scale = 1 << (sib >> 6)
        index = (sib >> 3) & 7
        base = sib & 7
        parts = []
        breg = None
        if mod == 0 and base == 5:
            disp = struct.unpack_from("<i", b, i)[0]; i += 4
        else:
            breg = REG32[base]
            parts.append(breg)
        if index != 4:
            sc = f"*{scale}" if scale > 1 else ""
            parts.append(REG32[index] + sc)
        if mod == 1:
            disp = struct.unpack_from("<b", b, i)[0]; i += 1
        elif mod == 2:
            disp = struct.unpack_from("<i", b, i)[0]; i += 4
        if disp or not parts:
            parts.append(f"{disp:#x}" if disp >= 0 else f"-{-disp:#x}")
        txt = f"{size} ptr [{'+'.join(parts)}]"
        return reg, txt, i, disp, None
    else:
        if mod == 0 and rm == 5:
            disp = struct.unpack_from("<I", b, i)[0]; i += 4
            txt = f"{size} ptr [{disp:#010x}]"
        else:
            if mod == 1:
                disp = struct.unpack_from("<b", b, i)[0]; i += 1
            elif mod == 2:
                disp = struct.unpack_from("<i", b, i)[0]; i += 4
            base_txt = REG32[rm]
            if disp != 0:
                txt = f"{size} ptr [{base_txt}{f'+{disp:#x}' if disp > 0 else f'-{-disp:#x}'}]"
            else:
                txt = f"{size} ptr [{base_txt}]"
        return reg, txt, i, disp, None

def decode_one(b, va):
    """Decode one instruction at va from bytes b (starting index 0).
    Returns Decoded. Raises DecodeError for unknown opcodes (fail-closed)."""
    i = 0
    prefix = ""
    opsize = 2  # dword
    addr_prefix = False
    seg = None
    while True:
        p = b[i]
        if p == 0x66:
            prefix = "word "; opsize = 1; i += 1
        elif p == 0x67:
            addr_prefix = True; i += 1
        elif p in (0x2E, 0x3E, 0x26, 0x36):
            seg = "seg"; i += 1
        elif p == 0x64:
            seg = "FS"; i += 1
        elif p == 0x65:
            seg = "GS"; i += 1
        elif p in (0xF2, 0xF3):
            prefix = "rep "; i += 1
        else:
            break
    start = i
    op = b[i]; i += 1
    def fin(mn, ops, ln, target=None):
        return Decoded(va, b[:ln], mn, ops, ln, target)
    # ---- 0x0F two-byte opcodes
    if op == 0x0F:
        op2 = b[i]; i += 1
        if 0x80 <= op2 <= 0x8F:  # Jcc rel32
            rel = struct.unpack_from("<i", b, i)[0]; i += 4
            mn = JCC[(op2 - 0x80) & 0xF]
            tgt = va + (i - start) + 0  # note: start offset math below
            # target computed from end of instruction: va + total_len + rel
            total = i
            tgt = va + total + rel
            return fin(mn, [f"{tgt:#010x}"], total, tgt)
        if 0x90 <= op2 <= 0x9F:  # SETcc r/m8
            reg, rm, i, disp, _ = decode_modrm(b, i, 0)
            mn = "SET" + JCC[(op2 - 0x90) & 0xF][1:]
            return fin(mn, [rm], i)
        if 0x40 <= op2 <= 0x4F:  # CMOVcc
            reg, rm, i, disp, _ = decode_modrm(b, i, 2)
            mn = "CMOV" + JCC[(op2 - 0x40) & 0xF][1:]
            return fin(mn, [REG32[reg], rm], i)
        if op2 == 0xB6 or op2 == 0xB7 or op2 == 0xBE or op2 == 0xBF:
            reg, rm, i, disp, _ = decode_modrm(b, i, 1 if op2 in (0xB7, 0xBF) else 0)
            mn = "MOVZX" if op2 in (0xB6, 0xB7) else "MOVSX"
            src_op = 1 if op2 in (0xB7, 0xBF) else 0
            # re-decode rm with proper size for register form
            return fin(mn, [REG32[reg], rm], i)
        if op2 == 0xAF:  # IMUL r32, r/m32
            reg, rm, i, disp, _ = decode_modrm(b, i, 2)
            return fin("IMUL", [REG32[reg], rm], i)
        if op2 == 0xB0 or op2 == 0xB1:  # CMPXCHG
            reg, rm, i, disp, _ = decode_modrm(b, i, 0 if op2 == 0xB0 else 2)
            return fin("CMPXCHG", [rm, REG8[reg] if op2 == 0xB0 else REG32[reg]], i)
        if op2 == 0xC0 or op2 == 0xC1:  # XADD
            sz = 0 if op2 == 0xC0 else 2
            reg, rm, i, disp, _ = decode_modrm(b, i, sz)
            return fin("XADD", [rm, REG8[reg] if sz == 0 else REG32[reg]], i)
        if 0xC8 <= op2 <= 0xCF:
            return fin("BSWAP", [REG32[op2 - 0xC8]], i)
        if op2 == 0xA2:
            return fin("CPUID", [], i)
        if op2 == 0x05:
            return fin("SYSCALL", [], i)
        if op2 == 0x0B:
            return fin("UD2", [], i)
        if op2 == 0x1E:
            # endbr/nop hints
            return fin("0F1E_hint", [], i + 3 if len(b) > i + 2 else i)
        raise DecodeError(f"unknown 0F {op2:#04x} at {va:#x}")
    # ---- Jcc rel8
    if 0x70 <= op <= 0x7F:
        rel = struct.unpack_from("<b", b, i)[0]; i += 1
        tgt = va + i + rel
        return fin(JCC[op - 0x70], [f"{tgt:#010x}"], i, tgt)
    # ---- PUSH/POP r32
    if 0x50 <= op <= 0x57:
        return fin("PUSH", [REG32[op - 0x50]], i)
    if 0x58 <= op <= 0x5F:
        return fin("POP", [REG32[op - 0x58]], i)
    # ---- INC/DEC r32 (40-4F)
    if 0x40 <= op <= 0x47:
        return fin("INC", [REG32[op - 0x40]], i)
    if 0x48 <= op <= 0x4F:
        return fin("DEC", [REG32[op - 0x48]], i)
    # ---- ALU binary ops 00-3D
    def alu_names(o):
        if o <= 0x05: return G1[0]
        if o <= 0x0D: return G1[1]
        if o <= 0x15: return G1[2]
        if o <= 0x1D: return G1[3]
        if o <= 0x25: return G1[4]
        if o <= 0x2D: return G1[5]
        if o <= 0x35: return G1[6]
        return G1[7]
    if op in (0x00, 0x01, 0x02, 0x03, 0x04, 0x05,
              0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D,
              0x10, 0x11, 0x12, 0x13, 0x14, 0x15,
              0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D,
              0x20, 0x21, 0x22, 0x23, 0x24, 0x25,
              0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D,
              0x30, 0x31, 0x32, 0x33, 0x34, 0x35,
              0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D):
        base = op & 0xF8
        mn = alu_names(op)
        low = op & 7
        if low == 0:  # op r/m8, r8
            reg, rm, i, disp, _ = decode_modrm(b, i, 0)
            return fin(mn, [rm, REG8[reg]], i)
        if low == 1:  # op r/m32, r32
            reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
            regn = REG32[reg] if opsize == 2 else REG16[reg]
            return fin(mn, [rm, regn], i)
        if low == 2:  # op r8, r/m8
            reg, rm, i, disp, _ = decode_modrm(b, i, 0)
            return fin(mn, [REG8[reg], rm], i)
        if low == 3:  # op r32, r/m32
            reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
            regn = REG32[reg] if opsize == 2 else REG16[reg]
            return fin(mn, [regn, rm], i)
        if low == 4:  # op AL, imm8
            imm = b[i]; i += 1
            return fin(mn, ["AL", f"{imm:#x}"], i)
        if low == 5:  # op eAX, imm
            if opsize == 1 or (op == 0x66 and False):
                imm = struct.unpack_from("<H", b, i)[0]; i += 2
                return fin(mn, ["AX", f"{imm:#x}"], i)
            imm = struct.unpack_from("<I", b, i)[0]; i += 4
            return fin(mn, ["EAX", f"{imm:#x}"], i)
        raise DecodeError(f"alu low {low}")
    # ---- group1
    if op in (0x80, 0x81, 0x83):
        sz = {0x80: 0, 0x81: 2, 0x83: 2}[op]
        reg, rm, i, disp, _ = decode_modrm(b, i, sz)
        if op == 0x81:
            imm = struct.unpack_from("<I", b, i)[0]; i += 4
        else:
            imm = struct.unpack_from("<b", b, i)[0]; i += 1
        return fin(G1[reg], [rm, f"{imm:#x}"], i)
    # ---- TEST
    if op == 0x84:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        return fin("TEST", [rm, REG8[reg]], i)
    if op == 0x85:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        regn = REG32[reg] if opsize == 2 else REG16[reg]
        return fin("TEST", [rm, regn], i)
    if op == 0x86 or op == 0x87:
        sz = 0 if op == 0x86 else opsize
        reg, rm, i, disp, _ = decode_modrm(b, i, sz)
        regn = REG8[reg] if sz == 0 else (REG32[reg] if opsize == 2 else REG16[reg])
        return fin("XCHG", [rm, regn], i)
    # ---- MOV
    if op == 0x88:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        return fin("MOV", [rm, REG8[reg]], i)
    if op == 0x89:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        regn = REG32[reg] if opsize == 2 else REG16[reg]
        return fin("MOV", [rm, regn], i)
    if op == 0x8A:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        return fin("MOV", [REG8[reg], rm], i)
    if op == 0x8B:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        regn = REG32[reg] if opsize == 2 else REG16[reg]
        return fin("MOV", [regn, rm], i)
    if op == 0x8C:  # MOV r/m16, Sreg
        reg, rm, i, disp, _ = decode_modrm(b, i, 1)
        return fin("MOV", [rm, "SREG"], i)
    if op == 0x8D:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        regn = REG32[reg] if opsize == 2 else REG16[reg]
        return fin("LEA", [regn, rm], i)
    if op == 0x8F:  # POP r/m
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        return fin("POP", [rm], i)
    if op == 0x90:
        return fin("NOP", [], i)
    if 0x91 <= op <= 0x97:
        return fin("XCHG", ["EAX", REG32[op - 0x90]], i)
    if op == 0x98:
        return fin("CWDE", [], i)
    if op == 0x99:
        return fin("CDQ", [], i)
    if op == 0x9C:
        return fin("PUSHFD", [], i)
    if op == 0x9D:
        return fin("POPFD", [], i)
    if op == 0xA4:
        return fin("MOVSB", [], i)
    if op == 0xA5:
        return fin("MOVSD", [], i)
    if op == 0xA6:
        return fin("CMPSB", [], i)
    if op == 0xA7:
        return fin("CMPSD", [], i)
    if op == 0xAA:
        return fin("STOSB", [], i)
    if op == 0xAB:
        return fin("STOSD", [], i)
    if op == 0xAC:
        return fin("LODSB", [], i)
    if op == 0xAD:
        return fin("LODSD", [], i)
    if op == 0xA8:
        imm = b[i]; i += 1
        return fin("TEST", ["AL", f"{imm:#x}"], i)
    if op == 0xA9:
        imm = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("TEST", ["EAX", f"{imm:#x}"], i)
    if op == 0xA0:
        addr = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", ["AL", f"[{addr:#x}]"], i)
    if op == 0xA1:
        addr = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", ["EAX", f"dword ptr [{addr:#x}]"], i)
    if op == 0xA2:
        addr = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", [f"[{addr:#x}]", "AL"], i)
    if op == 0xA3:
        addr = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", [f"dword ptr [{addr:#x}]", "EAX"], i)
    # ---- MOV r, imm
    if 0xB0 <= op <= 0xB7:
        imm = b[i]; i += 1
        return fin("MOV", [REG8[op - 0xB0], f"{imm:#x}"], i)
    if 0xB8 <= op <= 0xBF:
        imm = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", [REG32[op - 0xB8], f"{imm:#010x}"], i)
    # ---- shifts group2
    if op in (0xC0, 0xC1, 0xD0, 0xD1, 0xD2, 0xD3):
        sz = 0 if op in (0xC0, 0xD0, 0xD2) else 2
        reg, rm, i, disp, _ = decode_modrm(b, i, sz)
        if op in (0xC0, 0xC1):
            imm = b[i]; i += 1
            return fin(G2[reg], [rm, f"{imm:#x}"], i)
        if op in (0xD0, 0xD1):
            return fin(G2[reg], [rm, "1"], i)
        return fin(G2[reg], [rm, "CL"], i)
    # ---- RET
    if op == 0xC2:
        imm = struct.unpack_from("<H", b, i)[0]; i += 2
        return fin("RET", [f"{imm}"], i)
    if op == 0xC3:
        return fin("RET", [], i)
    # ---- MOV r/m, imm (C6/C7)
    if op == 0xC6:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        imm = b[i]; i += 1
        return fin("MOV", [rm, f"{imm:#x}"], i)
    if op == 0xC7:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        imm = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("MOV", [rm, f"{imm:#010x}"], i)
    if op == 0xC9:
        return fin("LEAVE", [], i)
    if op == 0xCC:
        return fin("INT3", [], i)
    if op == 0xCD:
        imm = b[i]; i += 1
        return fin("INT", [f"{imm:#x}"], i)
    # ---- group3 F6/F7
    if op == 0xF6:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        mn = G3_8.get(reg)
        if mn == "TEST":
            imm = b[i]; i += 1
            return fin("TEST", [rm, f"{imm:#x}"], i)
        if mn:
            return fin(mn, [rm], i)
        raise DecodeError(f"F6 reg {reg}")
    if op == 0xF7:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        mn = G3_8.get(reg)
        if mn == "TEST":
            imm = struct.unpack_from("<I", b, i)[0]; i += 4
            return fin("TEST", [rm, f"{imm:#x}"], i)
        if mn:
            return fin(mn, [rm], i)
        raise DecodeError(f"F7 reg {reg}")
    # ---- misc
    if op == 0xF8: return fin("CLC", [], i)
    if op == 0xF9: return fin("STC", [], i)
    if op == 0xFC: return fin("CLD", [], i)
    if op == 0xFD: return fin("STD", [], i)
    if op == 0xF4: return fin("HLT", [], i)
    if op == 0xF5: return fin("CMC", [], i)
    # ---- 0x60/0x61 PUSHA/POPA
    if op == 0x60: return fin("PUSHA", [], i)
    if op == 0x61: return fin("POPA", [], i)
    # ---- 0x68/0x6A PUSH imm
    if op == 0x68:
        imm = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("PUSH", [f"{imm:#x}"], i)
    if op == 0x69:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        imm = struct.unpack_from("<I", b, i)[0]; i += 4
        return fin("IMUL", [REG32[reg], rm, f"{imm:#x}"], i)
    if op == 0x6A:
        imm = struct.unpack_from("<b", b, i)[0]; i += 1
        return fin("PUSH", [f"{imm:#x}"], i)
    if op == 0x6B:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        imm = struct.unpack_from("<b", b, i)[0]; i += 1
        return fin("IMUL", [REG32[reg], rm, f"{imm:#x}"], i)
    # ---- E8/E9/EB
    if op == 0xE8:
        rel = struct.unpack_from("<i", b, i)[0]; i += 4
        tgt = va + i + rel
        return fin("CALL", [f"{tgt:#010x}"], i, tgt)
    if op == 0xE9:
        rel = struct.unpack_from("<i", b, i)[0]; i += 4
        tgt = va + i + rel
        return fin("JMP", [f"{tgt:#010x}"], i, tgt)
    if op == 0xEB:
        rel = struct.unpack_from("<b", b, i)[0]; i += 1
        tgt = va + i + rel
        return fin("JMP", [f"{tgt:#010x}"], i, tgt)
    # ---- segment pushes (06/07 etc.) legacy
    if op in (0x06, 0x0E, 0x16, 0x1E):
        return fin("PUSH_SEG", [], i)
    if op in (0x07, 0x17, 0x1F):
        return fin("POP_SEG", [], i)
    # ---- FPU D8-DF (x87): modrm-decoded, mnemonic recorded generically
    if 0xD8 <= op <= 0xDF:
        reg, rm, i, disp, _ = decode_modrm(b, i, 2)
        return fin(f"FPU_{op:02X}_{reg}", [rm], i)
    # ---- group4 FE (INC/DEC r/m8)
    if op == 0xFE:
        reg, rm, i, disp, _ = decode_modrm(b, i, 0)
        return fin("INC" if reg == 0 else "DEC", [rm], i)
    # ---- group5 FF
    if op == 0xFF:
        reg, rm, i, disp, _ = decode_modrm(b, i, opsize)
        mn = G5.get(reg)
        if mn is None:
            raise DecodeError(f"FF reg {reg}")
        return fin(mn, [rm], i)
    raise DecodeError(f"unknown opcode {op:#04x} at {va:#x}")

def disasm_range(pe, va_start, va_end):
    """Decode instructions in [va_start, va_end)."""
    out = []
    va = va_start
    while va < va_end:
        bs = pe.read_va(va, 16)
        try:
            ins = decode_one(bs, va)
        except DecodeError as e:
            out.append((va, bs[:8], f"DECODE_ERROR: {e}", [], None))
            va += 1  # attempt resync (caller inspects)
            continue
        out.append(ins)
        va += ins.length
    return out

def find_func_end(pe, va_start, max_bytes=256):
    """Decode until unconditional control transfer (RET/JMP) - heuristic function scanner."""
    va = va_start
    ins_list = []
    while va < va_start + max_bytes:
        bs = pe.read_va(va, 16)
        ins = decode_one(bs, va)
        ins_list.append(ins)
        va += ins.length
        if ins.mnemonic in ("RET",) or (ins.mnemonic == "JMP" and ins.target is not None):
            break
    return ins_list
