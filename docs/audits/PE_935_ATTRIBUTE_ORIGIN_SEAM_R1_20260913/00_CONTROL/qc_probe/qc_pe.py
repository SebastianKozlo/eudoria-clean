"""qc_pe.py — PE-MASTER-AUDITOR own PE parser (independent; NOT a copy of executor pe_core).
Minimal PE32 reader: sections, VA<->file offset, byte reads, pattern scans, dword tables.
Used for OWN-BYTES verification in QC phase. Fail-closed.
"""
import struct
import hashlib
import sys

class PE:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as f:
            self.buf = f.read()
        self._parse()

    def _parse(self):
        b = self.buf
        if b[:2] != b"MZ":
            raise ValueError("not MZ")
        e_lfanew = struct.unpack_from("<I", b, 0x3C)[0]
        if b[e_lfanew:e_lfanew+4] != b"PE\x00\x00":
            raise ValueError("not PE")
        machine, num_sections, ts = struct.unpack_from("<HHI", b, e_lfanew + 4)
        opt_off = e_lfanew + 24
        magic = struct.unpack_from("<H", b, opt_off)[0]
        if magic != 0x10B:
            raise ValueError("not PE32 (magic=0x%X)" % magic)
        self.image_base = struct.unpack_from("<I", b, opt_off + 28)[0]
        dll_chars = struct.unpack_from("<H", b, opt_off + 70)[0]
        self.dll_characteristics = dll_chars
        self.aslr_enabled = bool(dll_chars & 0x0040)
        self.entry_rva = struct.unpack_from("<I", b, opt_off + 16)[0]
        sec_off = opt_off + struct.unpack_from("<H", b, e_lfanew + 20)[0]
        self.sections = []
        for i in range(num_sections):
            off = sec_off + 40 * i
            name = b[off:off+8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, va, rsize, rptr = struct.unpack_from("<IIII", b, off + 8)
            self.sections.append({
                "name": name, "va_start": self.image_base + va, "va_end": self.image_base + va + vsize,
                "virtual_size": vsize, "virtual_address_rva": va,
                "raw_ptr": rptr, "raw_size": rsize,
            })

    def sha256(self):
        return hashlib.sha256(self.buf).hexdigest().upper()

    def va_to_off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["virtual_address_rva"] <= rva < s["virtual_address_rva"] + s["virtual_size"]:
                if (rva - s["virtual_address_rva"]) < s["raw_size"]:
                    return s["raw_ptr"] + (rva - s["virtual_address_rva"])
                return None  # in virtual range but not backed by raw
        return None

    def section_of(self, va):
        for s in self.sections:
            if s["va_start"] <= va < s["va_end"]:
                return s["name"]
        return None

    def read(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            return None
        return self.buf[off:off+n]

    def u32(self, va):
        d = self.read(va, 4)
        return None if d is None or len(d) < 4 else struct.unpack("<I", d)[0]

    def u16(self, va):
        d = self.read(va, 2)
        return None if d is None or len(d) < 2 else struct.unpack("<H", d)[0]

    def u8(self, va):
        d = self.read(va, 1)
        return None if d is None or len(d) < 1 else d[0]

    def cstr(self, va, maxlen=256):
        off = self.va_to_off(va)
        if off is None:
            return None
        end = self.buf.find(b"\x00", off, off + maxlen)
        if end < 0:
            return None
        return self.buf[off:end].decode("ascii", "replace")

    def scan_dword(self, value, sections=None):
        """Scan raw section data for 4-byte LE dword == value. Returns list of VAs."""
        out = []
        target = struct.pack("<I", value)
        for s in self.sections:
            if sections and s["name"] not in sections:
                continue
            data = self.buf[s["raw_ptr"]:s["raw_ptr"] + s["raw_size"]]
            start = 0
            while True:
                i = data.find(target, start)
                if i < 0:
                    break
                out.append(s["va_start"] + i)
                start = i + 1
        return out

    def scan_pattern(self, pattern, sections=None):
        """Scan for an exact byte pattern (bytes). Returns list of VAs."""
        out = []
        for s in self.sections:
            if sections and s["name"] not in sections:
                continue
            data = self.buf[s["raw_ptr"]:s["raw_ptr"] + s["raw_size"]]
            start = 0
            while True:
                i = data.find(pattern, start)
                if i < 0:
                    break
                out.append(s["va_start"] + i)
                start = i + 1
        return out

    def scan_call_e8(self, target_va, sections=(".text",)):
        """Scan for E8 rel32 calls to target_va (direct calls). Returns call-site VAs."""
        out = []
        for s in self.sections:
            if s["name"] not in sections:
                continue
            base = s["va_start"]
            data = self.buf[s["raw_ptr"]:s["raw_ptr"] + s["raw_size"]]
            for i in range(len(data) - 5):
                if data[i] == 0xE8:
                    rel = struct.unpack_from("<i", data, i + 1)[0]
                    if base + i + 5 + rel == target_va:
                        out.append(base + i)
        return out

    def scan_jmp_e9(self, target_va, sections=(".text",)):
        out = []
        for s in self.sections:
            if s["name"] not in sections:
                continue
            base = s["va_start"]
            data = self.buf[s["raw_ptr"]:s["raw_ptr"] + s["raw_size"]]
            for i in range(len(data) - 5):
                if data[i] == 0xE9:
                    rel = struct.unpack_from("<i", data, i + 1)[0]
                    if base + i + 5 + rel == target_va:
                        out.append(base + i)
        return out

    def hexdump(self, va, n):
        d = self.read(va, n)
        if d is None:
            return None
        lines = []
        for i in range(0, len(d), 16):
            chunk = d[i:i+16]
            lines.append("%08X  %s  |%s|" % (
                va + i,
                " ".join("%02X" % c for c in chunk),
                "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)))
        return "\n".join(lines)


def rtti_chain(pe, vtable_va, max_slots=16, read_name=True):
    """Own vtable->COL->TD->name chain. Returns dict."""
    col_va = pe.u32(vtable_va - 4)
    res = {"vtable_va": vtable_va, "col_va": col_va}
    if col_va is None:
        return res
    # MSVC CompleteObjectLocator: +0 signature, +4 offset, +8 cdOffset, +0xC pTypeDescriptor, +0x10 pClassDescriptor
    sig = pe.u32(col_va)
    td_va = pe.u32(col_va + 0xC)
    res.update({"col_signature": sig, "td_va": td_va})
    if td_va is None:
        return res
    td_vft = pe.u32(td_va)          # type descriptor: +0 vftable ptr, +4 spare, +8 name
    res["td_name"] = pe.cstr(td_va + 8)
    res["td_name_bytes"] = pe.read(td_va + 8, 48)
    # vtable slots
    slots = []
    for i in range(max_slots):
        p = pe.u32(vtable_va + 4 * i)
        if p is None:
            break
        slots.append(p)
    res["vtable_slots"] = slots
    return res


def main():
    pe = PE(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
    print("sha256:", pe.sha256())
    print("image_base: 0x%08X aslr:%s entry_rva:0x%X" % (pe.image_base, pe.aslr_enabled, pe.entry_rva))
    for s in pe.sections:
        print("  %-6s VA 0x%08X-0x%08X raw 0x%X+0x%X" % (s["name"], s["va_start"], s["va_end"], s["raw_ptr"], s["raw_size"]))


if __name__ == "__main__":
    main()
