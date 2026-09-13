# -*- coding: utf-8 -*-
# QC probe core — pe-master-auditor INTERNAL_QC, PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913
# OWN implementation, written from scratch for this QC. NOT derived from the executor's
# pe_core.py (which was only READ for audit). STATIC-ONLY.
import struct, hashlib, json, sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\03_EVIDENCE"


class Bin:
    """Minimal independent PE reader. VA->file offset via section table.
    Sections resolved by scanning the COFF section array directly."""

    def __init__(self, path):
        with open(path, "rb") as f:
            self.raw = f.read()
        self.path = path
        self.size = len(self.raw)
        self.sha256 = hashlib.sha256(self.raw).hexdigest().upper()
        b = self.raw
        assert b[0:2] == b"MZ", "DOS magic"
        pe_off = struct.unpack_from("<I", b, 0x3C)[0]
        assert b[pe_off:pe_off + 4] == b"PE\x00\x00", "PE sig"
        mach, nsec, tstamp = struct.unpack_from("<HHI", b, pe_off + 4)
        noptsz = struct.unpack_from("<H", b, pe_off + 20)[0]  # COFF+16 == pe+20
        opt = pe_off + 24
        magic = struct.unpack_from("<H", b, opt)[0]
        assert magic == 0x10B, "PE32 expected"
        self.image_base = struct.unpack_from("<I", b, opt + 28)[0]
        self.dllchars = struct.unpack_from("<H", b, opt + 70)[0]
        self.entry_rva = struct.unpack_from("<I", b, opt + 16)[0]
        self.machine = mach
        self.num_sections = nsec
        self.timestamp = tstamp
        secarr = opt + noptsz
        self.sections = []
        for i in range(nsec):
            o = secarr + i * 40
            nm = b[o:o + 8].split(b"\x00")[0].decode("ascii", "replace")
            vsz, va, rsz, rptr = struct.unpack_from("<IIII", b, o + 8)
            chars = struct.unpack_from("<I", b, o + 36)[0]
            self.sections.append(dict(name=nm, vsz=vsz, rva=va, rsz=rsz, rptr=rptr,
                                       chars=chars,
                                       va_lo=self.image_base + va,
                                       va_hi=self.image_base + va + max(vsz, rsz)))
        # executable section(s)
        self.exec_sections = [s for s in self.sections if s["chars"] & 0x20000000]
        # build one flat executable byte image for raw scans (text normally single)
        self.text = next(s for s in self.sections if s["name"] == ".text")

    def va2off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["rva"] <= rva < s["rva"] + s["rsz"]:
                return s["rptr"] + (rva - s["rva"])
        return None

    def rd(self, va, n):
        o = self.va2off(va)
        if o is None:
            return None
        return self.raw[o:o + n]

    def u32va(self, va):
        x = self.rd(va, 4)
        return None if x is None or len(x) < 4 else struct.unpack("<I", x)[0]

    def u32(self, off):
        return struct.unpack_from("<I", self.raw, off)[0]

    def cstr(self, va, maxlen=256):
        o = self.va2off(va)
        if o is None:
            return None
        end = self.raw.find(b"\x00", o, o + maxlen)
        return self.raw[o:end].decode("ascii", "replace")

    def scan_all_imm32(self, value):
        """Raw scan for LE u32 == value over EVERY byte offset of the WHOLE file.
        Returns list of file offsets."""
        pat = struct.pack("<I", value)
        out = []
        i = self.raw.find(pat)
        while i >= 0:
            out.append(i)
            i = self.raw.find(pat, i + 1)
        return out

    def scan_text_imm32(self, value):
        s = self.text
        pat = struct.pack("<I", value)
        out = []
        i = self.raw.find(pat, s["rptr"])
        while i >= 0:
            if i >= s["rptr"] + s["rsz"]:
                break
            out.append(i)
            i = self.raw.find(pat, i + 1)
        return out  # file offsets; va = image_base + rva where off->rva

    def off2va(self, off):
        for s in self.sections:
            if s["rptr"] <= off < s["rptr"] + s["rsz"]:
                return self.image_base + s["rva"] + (off - s["rptr"])
        return None

    def calls(self, target_va, opcode=0xE8):
        """Direct rel32 CALL (E8) / JMP (E9) sites across ALL executable sections,
        every byte offset (raw). Returns list of dicts with site VA and target."""
        res = []
        for s in self.exec_sections:
            base_va = self.image_base + s["rva"]
            lo, hi = s["rptr"], s["rptr"] + s["rsz"]
            for off in range(lo, hi - 5):
                if self.raw[off] != opcode:
                    continue
                rel = struct.unpack_from("<i", self.raw, off + 1)[0]
                t = base_va + (off - lo) + 5 + rel
                if t == target_va:
                    res.append(dict(site_va=self.off2va(off), file_off=off, section=s["name"]))
        return res

    def hexd(self, va, n):
        o = self.va2off(va)
        lines = []
        for i in range(0, n, 16):
            ch = self.raw[o + i:o + i + 16]
            if not ch:
                break
            lines.append("%08X  %-47s  %s" % (va + i,
                                              " ".join("%02X" % c for c in ch),
                                              "".join(chr(c) if 32 <= c < 127 else "." for c in ch)))
        return "\n".join(lines)


def f32(bits):
    return struct.unpack("<f", struct.pack("<I", bits))[0]


def save_json(name, obj):
    import os
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    return p
