# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 - shared core (own, independent)
# STATIC-ONLY (the client NEVER runs; nothing here is a runtime oracle result).
# Own PE parse from the PHYSICAL EXE; disassembly via capstone 5.0.7.
# Every VA cited by this run is derived through PE.va_to_off() from
# D:\Eudoria_Reconstruction\pcg_install\Entropia.exe. No prior-report value
# is used as decode input; pinned values below are EXPECTATIONS used
# fail-closed (assert), never as substitutes for measurement.

import hashlib
import struct
import sys

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone  # noqa: E402

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECTED_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECTED_SIZE = 8015872
EXPECTED_MACHINE = 0x014C      # IMAGE_FILE_MACHINE_I386
EXPECTED_OPT_MAGIC = 0x010B   # PE32
EXPECTED_IMAGE_BASE = 0x00400000

# Contract pins (EXPECTATIONS, all re-derived in-run before use):
SF_VTABLE_VA = 0x00A7D458                 # SceneFeederObject vtable (calibration target)
SF_RTTI_NAME_EXPECTED = ".?AVSceneFeederObject@@"
SF_CTOR_VA = 0x00509330                   # contract starting-point pin (re-derived below)
SF_CREATE_VA = 0x005247C0                 # creation chain pin (re-derived below)
PC_WINDOW_VA = 0x0050A050                 # positive-control function (slot 3)

_ACCESS = {1: "R", 2: "W", 3: "RW"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


class PE:
    """Own minimal PE parser + capstone wrapper. Fail-closed on identity."""

    def __init__(self, path=EXE_PATH, check_identity=True):
        self.path = path
        self.sha256 = sha256_file(path)
        self.size = len(open(path, "rb").read())
        if check_identity:
            assert self.sha256.upper() == EXPECTED_SHA256, "SHA mismatch"
            assert self.size == EXPECTED_SIZE, "size mismatch"
        d = open(path, "rb").read()
        self.data = d
        assert struct.unpack_from("<H", d, 0)[0] == 0x5A4D, "bad DOS magic"
        e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
        assert struct.unpack_from("<I", d, e_lfanew)[0] == 0x00004550, "bad PE sig"
        coff = e_lfanew + 4
        (self.machine, self.num_sections) = struct.unpack_from("<HH", d, coff)
        opt_size = struct.unpack_from("<H", d, coff + 16)[0]
        opt = coff + 20
        self.opt_magic = struct.unpack_from("<H", d, opt)[0]
        self.image_base = struct.unpack_from("<I", d, opt + 28)[0]
        self.entry_rva = struct.unpack_from("<I", d, opt + 16)[0]
        self.import_rva = struct.unpack_from("<I", d, opt + 96 + 8)[0]
        if check_identity:
            assert self.machine == EXPECTED_MACHINE
            assert self.opt_magic == EXPECTED_OPT_MAGIC
            assert self.image_base == EXPECTED_IMAGE_BASE
            # no-ASLR check: IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE (0x0040) clear
            dll_char = struct.unpack_from("<H", d, opt + 70)[0]
            assert dll_char & 0x0040 == 0, "ASLR flag set (pin says no ASLR)"
        sec_off = opt + opt_size
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
        assert self._text is not None, "no .text section"
        self.text_va_start = self._text["va_start"]
        self.text_va_end = self.text_va_start + self._text["rsize"]
        self.text_raw = d[self._text["rptr"]:self._text["rptr"] + self._text["rsize"]]
        self._md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self._md.detail = True
        self._imports = None

    # --- VA <-> file offset --------------------------------------------
    def va_to_off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + s["rsize"]:
                return s["rptr"] + (rva - s["vaddr"])
        return None

    def read_va(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            return None
        return self.data[off:off + n]

    def read_va32(self, va):
        b = self.read_va(va, 4)
        if not b or len(b) < 4:
            return None
        return struct.unpack("<I", b)[0]

    def section_of(self, va):
        for s in self.sections:
            if s["va_start"] <= va < s["va_end"]:
                return s["name"]
        return None

    def in_text(self, va):
        return self.text_va_start <= va < self.text_va_end

    # --- import table ----------------------------------------------------
    def imports(self):
        if self._imports is not None:
            return self._imports
        out = {}
        rva = self.import_rva
        d = self.data
        while True:
            off = self.va_to_off(self.image_base + rva)
            if off is None:
                break
            ilt, ts, fc, name_rva, iat_rva = struct.unpack_from("<IIIII", d, off)
            if ilt == 0 and name_rva == 0 and iat_rva == 0:
                break
            dll_off = self.va_to_off(self.image_base + name_rva)
            if dll_off is None:
                rva += 20
                continue
            dll = d[dll_off:d.index(b"\x00", dll_off)].decode("ascii", "replace")
            k = 0
            while True:
                iat_va = self.image_base + iat_rva + 4 * k
                o2 = self.va_to_off(iat_va)
                if o2 is None:
                    break
                val = struct.unpack_from("<I", d, o2)[0]
                if val == 0:
                    break
                if val & 0x80000000:
                    out[iat_va] = "%s.#%d" % (dll, val & 0xFFFF)
                else:
                    no = self.va_to_off(self.image_base + val + 2)
                    if no is not None:
                        nm = d[no:d.index(b"\x00", no)].decode("ascii", "replace")
                        out[iat_va] = "%s.%s" % (dll, nm)
                k += 1
            rva += 20
        self._imports = out
        return out

    def resolve_thunk(self, va):
        b = self.read_va(va, 6)
        if not b or b[0] != 0xFF or b[1] != 0x25:
            return None
        iat_va = struct.unpack_from("<I", b, 2)[0]
        return self.imports().get(iat_va, "IAT@0x%08X (unresolved)" % iat_va)

    # --- byte-pattern scans over .text ----------------------------------
    def scan_pattern(self, pat):
        """All .text offsets where byte pattern `pat` occurs; returns VAs."""
        out = []
        start = 0
        tr = self.text_raw
        while True:
            i = tr.find(pat, start)
            if i < 0:
                break
            out.append(self.text_va_start + i)
            start = i + 1
        return out

    def calls_to(self, target_va):
        """Direct CALL rel32 (E8) sites in .text whose target == target_va."""
        sites = []
        tr = self.text_raw
        base = self.text_va_start
        for i in range(len(tr) - 5):
            if tr[i] == 0xE8:
                rel = struct.unpack_from("<i", tr, i + 1)[0]
                if base + i + 5 + rel == target_va:
                    sites.append(base + i)
        return sites

    # --- disassembly ---------------------------------------------------
    def disasm_one(self, va):
        b = self.read_va(va, 16)
        if not b:
            return None
        try:
            ins = next(self._md.disasm(b, va))
        except StopIteration:
            return None
        rec = {"va": ins.address, "size": ins.size, "bytes": bytes(ins.bytes).hex(),
               "mnemonic": ins.mnemonic, "op_str": ins.op_str, "mem_ops": []}
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM:
                rec["mem_ops"].append({
                    "base": ins.reg_name(op.mem.base) if op.mem.base else "",
                    "index": ins.reg_name(op.mem.index) if op.mem.index else "",
                    "scale": op.mem.scale,
                    "disp": op.mem.disp,
                    "access": _ACCESS.get(op.access, "?"),
                })
        return rec

    def disasm_range(self, va, n):
        """Linear decode of up to n bytes starting at va (raw, no stops)."""
        out = []
        b = self.read_va(va, n)
        if not b:
            return out
        for ins in self._md.disasm(b, va):
            rec = self.disasm_one(ins.address)
            if rec is None:
                break
            out.append(rec)
        return out

    def _pad_run(self, va, byte):
        k = 0
        while k < 16:
            b = self.read_va(va + k, 1)
            if not b or b[0] != byte:
                break
            k += 1
        return k

    def derive_body(self, entry, max_bytes=0x2000):
        """Forward sweep from entry with MSVC-layout stop rules (see REPORT):
        aligned CC/90 padding, or RET-family at 16-alignment with no padding.
        Returns (instructions, body_end, (reason, stop_va))."""
        insns = []
        va = entry
        limit = entry + max_bytes
        stop = ("LIMIT", va)
        while va < limit:
            kcc = self._pad_run(va, 0xCC)
            if kcc >= 1 and ((va + kcc) % 16 == 0 or kcc >= 4):
                stop = ("CC_PAD", va)
                break
            k90 = self._pad_run(va, 0x90)
            if k90 >= 1 and ((va + k90) % 16 == 0 or k90 >= 4):
                stop = ("NOP_PAD", va)
                break
            if (insns and insns[-1]["mnemonic"].startswith("ret")
                    and va % 16 == 0 and kcc == 0 and k90 == 0):
                stop = ("RET_AT_ALIGN", va)
                break
            ins = self.disasm_one(va)
            if ins is None:
                stop = ("DISASM_FAIL", va)
                break
            insns.append(ins)
            va += ins["size"]
        body_end = insns[-1]["va"] + insns[-1]["size"] if insns else entry
        return insns, body_end, stop

    def find_function_start(self, va, max_back=0x2000):
        """Backward search for the containing function entry: nearest address E
        with E%16==0, preceded by >=1 int3/CC (or 90) pad byte, whose forward
        decode covers `va` without a stop before it. Heuristic (documented);
        classification never rests on it alone for PROVEN rows."""
        lo = va - max_back
        e = (lo + 15) & ~15
        best = None
        while e <= va:
            prev = self.read_va(e - 1, 1)
            if prev and prev[0] in (0xCC, 0x90):
                insns, _end, _stop = self.derive_body(e, (va - e) + 64)
                if insns and insns[-1]["va"] >= va:
                    # decode covered va (or reached its vicinity) from e
                    covered = any(i["va"] == va for i in insns)
                    if covered:
                        best = e
                        break
                    # re-scan: decode must not have stopped before va
                    last = insns[-1]
                    if _stop[0] == "LIMIT" and last["va"] + last["size"] > va:
                        best = e
                        break
            e += 16
        return best if best is not None else None

    # --- RTTI (MSVC 32-bit) --------------------------------------------
    def rtti_walk(self, vtable_va):
        """vtable[-1] -> RTTICompleteObjectLocator -> TypeDescriptor -> name.
        Every dword read from physical bytes via read_va32."""
        out = {"vtable_va": vtable_va, "col_ptr_va": vtable_va - 4,
               "col_va": self.read_va32(vtable_va - 4)}
        if out["col_va"] is None:
            out["error"] = "no COL pointer at vtable-4"
            return out
        col_raw = self.read_va(out["col_va"], 0x14)
        if not col_raw or len(col_raw) < 0x14:
            out["error"] = "COL read fail"
            return out
        sig, off, cd, ptd, pchd = struct.unpack("<IIIII", col_raw)
        out["col"] = {"signature": sig, "offset": off, "cd_offset": cd,
                      "p_type_descriptor": ptd, "p_class_hierarchy": pchd,
                      "raw": col_raw.hex()}
        if sig != 0:
            out["error"] = "COL signature != 0 (not 32-bit RTTI)"
            return out
        td_raw = self.read_va(ptd, 0x48)
        if td_raw is None:
            out["error"] = "TD read fail"
            return out
        name_field = td_raw[8:]
        z = name_field.find(b"\x00")
        name_bytes = name_field[:z] if z >= 0 else name_field
        out["td"] = {"va": ptd,
                     "vfptr": struct.unpack_from("<I", td_raw, 0)[0],
                     "spare": struct.unpack_from("<I", td_raw, 4)[0],
                     "name": name_bytes.decode("ascii", "replace"),
                     "name_raw_hex": name_bytes[:48].hex()}
        return out


def render(i):
    return "%08X  %-24s %-8s %s" % (i["va"], i["bytes"], i["mnemonic"], i["op_str"])


def hexdump(pe, va, n):
    off = pe.va_to_off(va)
    d = pe.data
    lines = []
    for i in range(0, n, 16):
        chunk = d[off + i:off + i + 16]
        lines.append("%08X  %-47s  %s" % (
            va + i, " ".join("%02X" % c for c in chunk),
            "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)))
    return "\n".join(lines)
