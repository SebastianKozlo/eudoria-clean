# pe935k_core.py - run-local PE walk core for PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006
# Minimal PE32 header parse + section map + VA<->file-offset mapping + byte reads.
# Everything re-derived from the pinned EXE; nothing inherited is trusted as input.
# STATIC-ONLY: byte reads only, no execution of any target code.

import struct

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE_BYTES = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"


class Exe:
    def __init__(self, path=EXE_PATH):
        with open(path, "rb") as f:
            self.raw = f.read()
        if len(self.raw) != EXE_SIZE_BYTES:
            raise ValueError("EXE size mismatch: %d" % len(self.raw))
        e_lfanew = struct.unpack_from("<I", self.raw, 0x3C)[0]
        if self.raw[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise ValueError("bad PE magic")
        coff = e_lfanew + 4
        machine, nsec, _, _, _, opt_size, _ = struct.unpack_from("<HHIIIHH", self.raw, coff)
        if machine != 0x14C:
            raise ValueError("not i386: 0x%X" % machine)
        opt = coff + 20
        magic = struct.unpack_from("<H", self.raw, opt)[0]
        if magic != 0x10B:
            raise ValueError("not PE32: 0x%X" % magic)
        self.image_base = struct.unpack_from("<I", self.raw, opt + 28)[0]
        self.size_of_image = struct.unpack_from("<I", self.raw, opt + 56)[0]
        dll_char = struct.unpack_from("<H", self.raw, opt + 70)[0]
        self.aslr = bool(dll_char & 0x40)
        self.sections = []
        sec_off = opt + opt_size
        for i in range(nsec):
            o = sec_off + i * 40
            name = self.raw[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", self.raw, o + 8)
            self.sections.append({
                "name": name, "virtual_size": vsize, "virtual_address": vaddr,
                "raw_size": rsize, "raw_pointer": raddr,
            })

    def section_of_va(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["virtual_address"] <= rva < s["virtual_address"] + max(s["virtual_size"], s["raw_size"]):
                return s
        return None

    def va_to_off(self, va):
        s = self.section_of_va(va)
        if s is None:
            return None
        rva = va - self.image_base
        if rva - s["virtual_address"] >= s["raw_size"]:
            return None  # virtual-only tail
        return s["raw_pointer"] + (rva - s["virtual_address"])

    def read(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            return None
        return self.raw[off:off + n]

    def u32(self, va):
        off = self.va_to_off(va)
        if off is None:
            return None
        return struct.unpack_from("<I", self.raw, off)[0]

    def text_range(self):
        for s in self.sections:
            if s["name"] == ".text":
                return (self.image_base + s["virtual_address"],
                        self.image_base + s["virtual_address"] + s["raw_size"])
        raise ValueError("no .text")


def e8_target(call_va, rel32):
    # call_va = VA of the E8 opcode byte; rel32 = signed displacement dword
    r = rel32 if rel32 < 0x80000000 else rel32 - 0x100000000
    return (call_va + 5 + r) & 0xFFFFFFFF


def hexs(b):
    return " ".join("%02X" % c for c in b)
