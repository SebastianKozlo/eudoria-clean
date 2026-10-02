# pe_parse.py — independent PE32 parser for the DESKTOP_CORRECTION_R1 run
# RUN_ID: PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002
# Scope: parse the pinned Entropia.exe PE headers (DOS/COFF/Optional/Sections),
#        provide VA->RVA->file-offset conversion and raw byte reads.
#        NO assumptions: offset != RVA unless a section table entry says so.
#        This file is self-contained; imports only stdlib. Static analysis only.
import sys
sys.dont_write_bytecode = True  # prior __pycache__ incident class — never write bytecode
import struct
import hashlib

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_EXPECTED_SIZE = 8015872
EXE_EXPECTED_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"


class PE32:
    def __init__(self, path=EXE_PATH, verify=True):
        with open(path, "rb") as f:
            self.raw = f.read()
        self.path = path
        self.size = len(self.raw)
        if verify:
            h = hashlib.sha256(self.raw).hexdigest().upper()
            if self.size != EXE_EXPECTED_SIZE or h != EXE_EXPECTED_SHA256:
                raise RuntimeError("EXE identity mismatch: size=%d sha=%s" % (self.size, h))
            self.sha256 = h
        else:
            self.sha256 = hashlib.sha256(self.raw).hexdigest().upper()
        self._parse()

    def _parse(self):
        r = self.raw
        # DOS header
        if r[0:2] != b"MZ":
            raise RuntimeError("no MZ")
        e_lfanew = struct.unpack_from("<I", r, 0x3C)[0]
        self.e_lfanew = e_lfanew
        # PE signature
        if r[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise RuntimeError("no PE signature at e_lfanew=0x%X" % e_lfanew)
        coff = e_lfanew + 4
        (self.machine, self.num_sections, self.timestamp, self.ptr_symtab,
         self.num_syms, self.size_opt, self.characteristics) = struct.unpack_from("<HHIIIHH", r, coff)
        opt = coff + 20
        self.magic = struct.unpack_from("<H", r, opt)[0]
        if self.magic != 0x10B:
            raise RuntimeError("not PE32 (magic=0x%X)" % self.magic)
        (self.linker_major, self.linker_minor) = struct.unpack_from("<BB", r, opt + 2)
        self.size_of_code, self.size_of_init_data, self.size_of_uninit_data = struct.unpack_from("<III", r, opt + 4)
        self.entry_point_rva = struct.unpack_from("<I", r, opt + 16)[0]
        self.base_of_code = struct.unpack_from("<I", r, opt + 20)[0]
        self.base_of_data = struct.unpack_from("<I", r, opt + 24)[0]
        self.image_base = struct.unpack_from("<I", r, opt + 28)[0]
        self.section_alignment = struct.unpack_from("<I", r, opt + 32)[0]
        self.file_alignment = struct.unpack_from("<I", r, opt + 36)[0]
        self.size_of_image = struct.unpack_from("<I", r, opt + 56)[0]
        self.size_of_headers = struct.unpack_from("<I", r, opt + 60)[0]
        # Data directories (PE32: 16 entries of 8 bytes, starting at opt+96)
        self.data_directories = []
        for i in range(16):
            rva, size = struct.unpack_from("<II", r, opt + 96 + i * 8)
            self.data_directories.append((rva, size))
        # Section table
        sect = opt + self.size_opt
        self.sections = []
        for i in range(self.num_sections):
            off = sect + i * 40
            name = r[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
            (vsize, vaddr, rawsize, rawptr) = struct.unpack_from("<IIII", r, off + 8)
            (relocs, linenum, nreloc, nlinenum, chars) = struct.unpack_from("<IIHHI", r, off + 24)
            self.sections.append({
                "index": i, "name": name, "virtual_size": vsize, "virtual_address": vaddr,
                "raw_size": rawsize, "raw_pointer": rawptr,
                "characteristics": chars,
            })

    def section_of_rva(self, rva):
        for s in self.sections:
            span = max(s["virtual_size"], s["raw_size"])
            if s["virtual_address"] <= rva < s["virtual_address"] + span:
                return s
        return None

    def rva_to_fo(self, rva, length=1):
        """RVA -> file offset via the section table (no offset==RVA assumption)."""
        s = self.section_of_rva(rva)
        if s is None:
            raise RuntimeError("RVA 0x%X not in any section" % rva)
        if s["raw_pointer"] == 0:
            raise RuntimeError("RVA 0x%X in header-only section %s" % (rva, s["name"]))
        delta = rva - s["virtual_address"]
        fo = s["raw_pointer"] + delta
        if delta + length > s["raw_size"]:
            raise RuntimeError("read beyond raw size of section %s (rva=0x%X len=%d)" % (s["name"], rva, length))
        return fo

    def va_to_fo(self, va, length=1):
        rva = va - self.image_base
        return self.rva_to_fo(rva, length)

    def read_va(self, va, length):
        fo = self.va_to_fo(va, length)
        return self.raw[fo:fo + length]

    def read_u32_va(self, va):
        return struct.unpack("<I", self.read_va(va, 4))[0]

    def pin(self, va, length, section=None):
        """Return a pin dict: va/rva/file_offset/section/length/bytes_hex."""
        rva = va - self.image_base
        fo = self.va_to_fo(va, length)
        if section is None:
            s = self.section_of_rva(rva)
            section = s["name"] if s else "?"
        return {
            "va": "0x%08X" % va,
            "rva": "0x%08X" % rva,
            "file_offset": "0x%08X" % fo,
            "section": section,
            "length": length,
            "original_bytes_hex": self.raw[fo:fo + length].hex().upper(),
        }

    def header_summary(self):
        return {
            "exe_path": self.path,
            "exe_size": self.size,
            "exe_sha256": self.sha256,
            "e_lfanew": "0x%X" % self.e_lfanew,
            "machine": "0x%04X" % self.machine,
            "num_sections": self.num_sections,
            "magic": "0x%X" % self.magic,
            "linker_version": "%d.%d" % (self.linker_major, self.linker_minor),
            "entry_point_rva": "0x%X" % self.entry_point_rva,
            "image_base": "0x%X" % self.image_base,
            "section_alignment": "0x%X" % self.section_alignment,
            "file_alignment": "0x%X" % self.file_alignment,
            "size_of_image": "0x%X" % self.size_of_image,
            "size_of_headers": "0x%X" % self.size_of_headers,
            "sections": [
                {
                    "name": s["name"],
                    "virtual_address": "0x%08X" % s["virtual_address"],
                    "virtual_size": "0x%X" % s["virtual_size"],
                    "raw_pointer": "0x%08X" % s["raw_pointer"],
                    "raw_size": "0x%X" % s["raw_size"],
                    "characteristics": "0x%08X" % s["characteristics"],
                    "va_start": "0x%08X" % (self.image_base + s["virtual_address"]),
                }
                for s in self.sections
            ],
        }


if __name__ == "__main__":
    import json
    pe = PE32()
    print(json.dumps(pe.header_summary(), indent=1))
