# -*- coding: utf-8 -*-
# PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 - shared core (own, independent)
# STATIC-ONLY. Own PE parse (no external deps beyond capstone for disasm listing).
# Every VA cited in this run must be derived through PE.va_to_off() from the
# PHYSICAL EXE at D:\Eudoria_Reconstruction\pcg_install\Entropia.exe.
# Desktop hexdumps are a DERIVED layer - never a decode source (contract S-note 1).

import struct

try:
    import capstone
    HAS_CAPSTONE = True
except ImportError:
    HAS_CAPSTONE = False


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

    # --- VA <-> file offset --------------------------------------------
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

    def read_va_u16(self, va):
        b = self.read_va(va, 2)
        if b is None or len(b) < 2:
            return None
        return struct.unpack("<H", b)[0]

    def section_of(self, va):
        for s in self.sections:
            if s["va_start"] <= va < s["va_end"]:
                return s["name"]
        return None

    # --- scanning ------------------------------------------------------
    def scan_text_bytes(self, pat):
        """All VAs in .text where the byte pattern occurs (raw scan, every offset).
        Returns text_off list; convert with text_off_to_va()."""
        out = []
        start = 0
        tr = self.text_raw
        while True:
            i = tr.find(pat, start)
            if i < 0:
                break
            out.append(i)
            start = i + 1
        return out

    def text_off_to_va(self, text_off):
        return self.text_va_start + text_off

    def text_va_to_off(self, va):
        if self.text_va_start <= va < self.text_va_start + len(self.text_raw):
            return va - self.text_va_start
        return None

    def calls_to(self, target_va):
        """Direct CALL rel32 (E8) sites in .text whose target == target_va.
        Raw scan; candidates must be boundary-checked where needed."""
        sites = []
        tr = self.text_raw
        base = self.text_va_start
        for i in range(len(tr) - 5):
            if tr[i] == 0xE8:
                rel = struct.unpack_from("<i", tr, i + 1)[0]
                if base + i + 5 + rel == target_va:
                    sites.append(i)
        return sites

    def jumps_to(self, target_va):
        """Direct JMP rel32 (E9) sites in .text whose target == target_va."""
        sites = []
        tr = self.text_raw
        base = self.text_va_start
        for i in range(len(tr) - 5):
            if tr[i] == 0xE9:
                rel = struct.unpack_from("<i", tr, i + 1)[0]
                if base + i + 5 + rel == target_va:
                    sites.append(i)
        return sites

    # --- boundaries ----------------------------------------------------
    def func_body(self, entry_va, maxb=0x20000):
        """Function body bytes: from entry to first CC CC CC run (heuristic)."""
        off = self.va_to_off(entry_va)
        if off is None:
            return None, b""
        end = off
        d = self.data
        limit = min(off + maxb, len(d) - 3)
        while end < limit:
            if d[end] == 0xCC and d[end + 1] == 0xCC and d[end + 2] == 0xCC:
                break
            end += 1
        return self.off_to_va(end), d[off:end]

    # --- disassembly (capstone) ---------------------------------------
    def disasm(self, va, size, mode=4):
        """Linear capstone disassembly of [va, va+size).
        Returns list of dicts: va, size, bytes(hex), mnemonic, op_str."""
        assert HAS_CAPSTONE, "capstone required"
        b = self.read_va(va, size)
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        md.detail = False
        out = []
        for ins in md.disasm(b, va):
            out.append({
                "va": ins.address, "size": ins.size,
                "bytes": bytes(ins.bytes).hex(),
                "mnemonic": ins.mnemonic, "op_str": ins.op_str,
            })
        return out

    def disasm_lines(self, va, size):
        """Disassembly rendered as text lines 'VA  BYTES  MNEMONIC OPS'."""
        lines = []
        for i in self.disasm(va, size):
            lines.append("%08X  %-24s %-8s %s" % (
                i["va"], i["bytes"], i["mnemonic"], i["op_str"]))
        return "\n".join(lines)

    def disasm_until(self, va, max_bytes=0x800, stop_mnemonics=("ret", "int3")):
        """Linear disasm until a stop mnemonic (first layer only)."""
        b = self.read_va(va, max_bytes)
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        out = []
        for ins in md.disasm(b, va):
            out.append({
                "va": ins.address, "size": ins.size,
                "bytes": bytes(ins.bytes).hex(),
                "mnemonic": ins.mnemonic, "op_str": ins.op_str,
            })
            if ins.mnemonic in stop_mnemonics:
                break
        return out


def hexdump_lines(pe, va, n):
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


def bits_of_f32(value):
    return struct.unpack("<I", struct.pack("<f", value))[0]


# --- canonical paths for this run ---------------------------------------
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS_PATH = (r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters"
            r"\templates.vfs")

# Contract-pinned identities (RUN_CONTRACT.md section 1)
CONTRACT = {
    "exe_sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "exe_size": 8015872,
    "vfs_sha256": "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77",
    "vfs_size": 560788,
    "image_base": 0x00400000,
    "text_rva": 0x1000,
    "text_raw": 0x1000,
}
