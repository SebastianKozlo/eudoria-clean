# -*- coding: utf-8 -*-
# PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 — shared PE core (independent)
# STATIC-ONLY. Own PE parse (no external deps). VA<->file-offset via section table.
# Every VA cited in this run must be derived through pe_core.PE.va_to_off().

import struct


class PE:
    def __init__(self, path):
        self.path = path
        self.data = open(path, "rb").read()
        d = self.data
        self.dos_magic = struct.unpack_from("<H", d, 0)[0]
        assert self.dos_magic == 0x5A4D, "bad DOS magic"
        self.e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
        self.pe_sig = struct.unpack_from("<I", d, self.e_lfanew)[0]
        assert self.pe_sig == 0x00004550, "bad PE signature"
        coff = self.e_lfanew + 4
        (self.machine, self.num_sections, self.timestamp) = struct.unpack_from("<HHI", d, coff)
        self.opt_size = struct.unpack_from("<H", d, coff + 16)[0]
        opt = coff + 20
        self.opt_magic = struct.unpack_from("<H", d, opt)[0]
        self.image_base = struct.unpack_from("<I", d, opt + 28)[0]
        self.dll_chars = struct.unpack_from("<H", d, opt + 70)[0]
        self.aslr = bool(self.dll_chars & 0x0040)
        self.entry_rva = struct.unpack_from("<I", d, opt + 16)[0]
        sec_off = opt + self.opt_size
        self.sections = []
        for i in range(self.num_sections):
            o = sec_off + i * 40
            name = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", d, o + 8)
            self.sections.append({
                "name": name, "vsize": vsize, "vaddr": vaddr,
                "rsize": rsize, "rptr": rptr,
                "va_start": self.image_base + vaddr,
                "va_end": self.image_base + vaddr + max(vsize, rsize),
            })
        self._text = None
        for s in self.sections:
            if s["name"] == ".text":
                self._text = s
        self.text_raw = d[self._text["rptr"]:self._text["rptr"] + self._text["rsize"]]
        self.text_va_start = self._text["va_start"]

    def va_to_off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + s["rsize"]:
                return s["rptr"] + (rva - s["vaddr"])
        return None

    def off_to_va(self, off):
        for s in self.sections:
            if s["rptr"] <= off < s["rptr"] + s["rsize"]:
                return self.image_base + s["vaddr"] + (off - s["rptr"])
        return None

    def read_va(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            return None
        return self.data[off:off + n]

    def read_va32(self, va):
        b = self.read_va(va, 4)
        if b is None or len(b) < 4:
            return None
        return struct.unpack("<I", b)[0]

    def section_of(self, va):
        for s in self.sections:
            if s["va_start"] <= va < s["va_end"]:
                return s["name"]
        return None

    def text_off_to_va(self, text_off):
        """text_off = offset within self.text_raw -> VA"""
        return self.text_va_start + text_off

    def text_va_to_off(self, va):
        """VA -> offset within self.text_raw (None if outside .text)"""
        if self.text_va_start <= va < self.text_va_start + len(self.text_raw):
            return va - self.text_va_start
        return None

    def scan_text_imm32(self, value):
        """All offsets in .text where LE u32 == value (raw byte scan, every offset)."""
        pat = struct.pack("<I", value)
        out = []
        start = 0
        while True:
            i = self.text_raw.find(pat, start)
            if i < 0:
                break
            out.append(i)
            start = i + 1
        return out  # offsets within text_raw; use text_off_to_va()

    def scan_text_bytes(self, pat):
        out = []
        start = 0
        while True:
            i = self.text_raw.find(pat, start)
            if i < 0:
                break
            out.append(i)
            start = i + 1
        return out

    def calls_to(self, target_va):
        """Direct CALL rel32 sites in .text whose target == target_va.
        Returns list of (call_site_text_off). Note: raw E8 scan, candidate
        sites must be filtered for instruction boundaries where needed."""
        sites = []
        tr = self.text_raw
        base = self.text_va_start
        for i in range(len(tr) - 5):
            if tr[i] == 0xE8:
                rel = struct.unpack_from("<i", tr, i + 1)[0]
                t = base + i + 5 + rel
                if t == target_va:
                    sites.append(i)
        return sites

    def func_body(self, entry_va, maxb=0x20000):
        """Function body bytes: from entry to first CC CC CC run (heuristic),
        bounded by maxb. Returns (end_va, bytes)."""
        off = self.va_to_off(entry_va)
        if off is None:
            return None, b""
        end = off
        d = self.data
        limit = off + maxb
        while end + 3 < len(d) and end < limit:
            if d[end] == 0xCC and d[end + 1] == 0xCC and d[end + 2] == 0xCC:
                break
            end += 1
        return self.off_to_va(end), d[off:end]

    def disasm_region(self, va, n):
        """Raw hex of region [va, va+n) — for byte pinning."""
        b = self.read_va(va, n)
        return b.hex() if b is not None else None


def hexdump(pe, va, n):
    off = pe.va_to_off(va)
    d = pe.data
    lines = []
    for i in range(0, n, 16):
        chunk = d[off + i:off + i + 16]
        va_i = va + i
        lines.append("%08X  %-47s  %s" % (
            va_i,
            " ".join("%02X" % c for c in chunk),
            "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)))
    return "\n".join(lines)


def u16(b, o):
    return struct.unpack_from("<H", b, o)[0]


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def i32(b, o):
    return struct.unpack_from("<i", b, o)[0]


def f32bits(bits):
    return struct.unpack("<f", struct.pack("<I", bits))[0]
