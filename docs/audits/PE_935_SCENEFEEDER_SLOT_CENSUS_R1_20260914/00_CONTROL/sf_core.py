# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 - shared core (own, independent)
# STATIC-ONLY. Own PE parse; disassembly listing via capstone 5.0.7 (measured)
# (interpreter: D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe).
# Every VA cited in this run is derived through PE.va_to_off() from the
# PHYSICAL EXE at D:\Eudoria_Reconstruction\pcg_install\Entropia.exe.
# No prior-report values are used as decode input; the contract pin values
# below are EXPECTATIONS used fail-closed (assert), never as substitutes
# for measurement.

import struct

import capstone

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECTED_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECTED_SIZE = 8015872
EXPECTED_MACHINE = 0x014C      # IMAGE_FILE_MACHINE_I386
EXPECTED_OPT_MAGIC = 0x010B   # PE32
EXPECTED_IMAGE_BASE = 0x00400000

VTABLE_VA = 0x00A7D458        # contract pin: SceneFeederObject vtable (to be verified)
EXPECTED_RTTI_NAME = ".?AVSceneFeederObject@@"

# The six contract slots (to be verified as vtable entries from the physical EXE)
SIX_FUNCS = [
    0x0050A460,
    0x005090A0,
    0x005090B0,
    0x0050A050,
    0x005090C0,
    0x00509580,
]

POSITIVE_CONTROL_VA = 0x005094C0
POSITIVE_CONTROL_WINDOW = 0x40
# Contract-expected byte pattern for the positive-control window
# (verified by re-derivation, never trusted blindly):
#   mov eax,[esp+4]; mov edx,[eax]; mov [ecx+0x34],edx;
#   mov edx,[eax+4]; mov [ecx+0x38],edx; mov eax,[eax+8]; mov [ecx+0x3C],eax;
#   mov byte [ecx+0x28],1; ret 4
POSITIVE_CONTROL_EXPECTED = bytes.fromhex(
    "8B442404"   # mov eax, dword ptr [esp + 4]
    "8B10"       # mov edx, dword ptr [eax]
    "895134"     # mov dword ptr [ecx + 0x34], edx
    "8B5004"     # mov edx, dword ptr [eax + 4]
    "895138"     # mov dword ptr [ecx + 0x38], edx
    "8B4008"     # mov eax, dword ptr [eax + 8]
    "89413C"     # mov dword ptr [ecx + 0x3C], eax
    "C6412801"   # mov byte ptr [ecx + 0x28], 1
    "C20400"     # ret 4
)

# SceneFeeder position field offsets of interest
SF_FIELD_DISPS = (0x30, 0x34, 0x38, 0x3C)

_ACCESS = {1: "R", 2: "W", 3: "RW"}


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
        self.num_dirs = struct.unpack_from("<I", d, opt + 92)[0]
        self.image_base = struct.unpack_from("<I", d, opt + 28)[0]
        self.entry_rva = struct.unpack_from("<I", d, opt + 16)[0]
        # data directory 1 = Import Table
        self.import_rva = struct.unpack_from("<I", d, opt + 96 + 1 * 8)[0]
        self.import_size = struct.unpack_from("<I", d, opt + 96 + 1 * 8 + 4)[0]
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

    def in_text(self, va):
        return self.text_va_start <= va < self.text_va_end

    # --- import table (for one-hop thunk resolution) --------------------
    def imports(self):
        """Map IAT slot VA -> 'DllName.FunctionName'. Lazy, one pass."""
        if self._imports is not None:
            return self._imports
        out = {}
        if self.import_rva == 0:
            self._imports = out
            return out
        rva = self.import_rva
        d = self.data
        while True:
            try:
                ilt, ts, fc, name_rva, iat_rva = struct.unpack_from("<IIIII", d, self.va_to_off(self.image_base + rva))
            except (TypeError, struct.error):
                break
            if ilt == 0 and name_rva == 0 and iat_rva == 0:
                break
            dll_off = self.va_to_off(self.image_base + name_rva)
            if dll_off is None:
                rva += 20
                continue
            dll = d[dll_off:d.index(b"\x00", dll_off)].decode("ascii", "replace")
            # walk the IAT in parallel (thunks may be bound: IAT holds VAs)
            k = 0
            while True:
                iat_va = self.image_base + iat_rva + 4 * k
                off = self.va_to_off(iat_va)
                if off is None:
                    break
                val = struct.unpack_from("<I", d, off)[0]
                if val == 0:
                    break
                if val & 0x80000000:  # ordinal import
                    out[iat_va] = "%s.#%d" % (dll, val & 0xFFFF)
                else:
                    no = self.va_to_off(self.image_base + val + 2)  # skip hint
                    if no is not None:
                        nm = d[no:d.index(b"\x00", no)].decode("ascii", "replace")
                        out[iat_va] = "%s.%s" % (dll, nm)
                k += 1
            rva += 20
        self._imports = out
        return out

    def resolve_thunk(self, va):
        """If VA is `FF 25 xx` (jmp dword ptr [IAT]) resolve the import name."""
        b = self.read_va(va, 6)
        if b is None or b[0] != 0xFF or b[1] != 0x25:
            return None
        iat_va = struct.unpack_from("<I", b, 2)[0]
        return self.imports().get(iat_va, "IAT@0x%08X (unresolved)" % iat_va)

    # --- scanning ------------------------------------------------------
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

    def jumps_to(self, target_va):
        """Direct JMP rel32 (E9) sites in .text whose target == target_va."""
        sites = []
        tr = self.text_raw
        base = self.text_va_start
        for i in range(len(tr) - 5):
            if tr[i] == 0xE9:
                rel = struct.unpack_from("<i", tr, i + 1)[0]
                if base + i + 5 + rel == target_va:
                    sites.append(base + i)
        return sites

    # --- disassembly ---------------------------------------------------
    def disasm_one(self, va):
        """Disassemble exactly one instruction at VA. None if invalid."""
        b = self.read_va(va, 16)
        if not b:
            return None
        try:
            ins = next(self._md.disasm(b, va))
        except StopIteration:
            return None
        rec = {
            "va": ins.address,
            "size": ins.size,
            "bytes": bytes(ins.bytes).hex(),
            "mnemonic": ins.mnemonic,
            "op_str": ins.op_str,
            "mem_ops": [],
        }
        if ins.mnemonic in ("call", "jmp"):
            for op in ins.operands:
                if op.type == capstone.x86.X86_OP_IMM:
                    rec["imm"] = op.imm
                    break
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

    # --- function body derivation --------------------------------------
    def _pad_run(self, va, byte):
        k = 0
        while k < 16:
            b = self.read_va(va + k, 1)
            if not b or b[0] != byte:
                break
            k += 1
        return k

    def derive_body(self, entry, next_known=None, max_bytes=0x2000):
        """Linear sweep from entry. MSVC layout observed in this binary:
        every function is 16-byte aligned; inter-function padding (CC, in
        one observed case a 2-byte CC run) always completes to the next
        16-byte boundary. Stop rules (in priority order):
          1. va >= next_known (another known function entry VA)
          2. CC run at va with (va+k)%16==0 (aligned CC padding) or k>=4
          3. 90 run at va with (va+k)%16==0 (aligned NOP padding) or k>=4
          4. previous insn was RET-family AND va%16==0 AND no padding bytes
             (tight adjacency: next function starts at the aligned VA)
          5. read/disasm failure or hard limit
        body_end = end of the LAST real instruction (padding excluded).
        Returns (instructions, body_end, (reason, stop_va))."""
        insns = []
        va = entry
        limit = entry + max_bytes
        stop = ("LIMIT", va)
        while va < limit:
            if next_known is not None and va >= next_known:
                stop = ("NEXT_KNOWN_ENTRY", va)
                break
            kcc = self._pad_run(va, 0xCC)
            if kcc >= 1 and ((va + kcc) % 16 == 0 or kcc >= 4):
                stop = ("CC_PAD_ALIGN" if (va + kcc) % 16 == 0 else "CC_PAD_RUN", va)
                break
            k90 = self._pad_run(va, 0x90)
            if k90 >= 1 and ((va + k90) % 16 == 0 or k90 >= 4):
                stop = ("NOP_PAD_ALIGN" if (va + k90) % 16 == 0 else "NOP_PAD_RUN", va)
                break
            if (insns and insns[-1]["mnemonic"].startswith("ret")
                    and va % 16 == 0 and kcc == 0 and k90 == 0):
                stop = ("RET_AT_ALIGN_TIGHT", va)
                break
            ins = self.disasm_one(va)
            if ins is None:
                stop = ("DISASM_FAIL", va)
                break
            insns.append(ins)
            va += ins["size"]
        body_end = insns[-1]["va"] + insns[-1]["size"] if insns else entry
        return insns, body_end, stop

    # --- RTTI (MSVC 32-bit) --------------------------------------------
    def rtti_walk(self, vtable_va):
        """vtable[-1] -> RTTICompleteObjectLocator -> TypeDescriptor -> name."""
        col_va = self.read_va32(vtable_va - 4)
        out = {"vtable_va": vtable_va, "col_ptr_va": vtable_va - 4, "col_va": col_va}
        if col_va is None:
            out["error"] = "no COL pointer at vtable-4"
            return out
        col_raw = self.read_va(col_va, 0x14)
        if col_raw is None or len(col_raw) < 0x14:
            out["error"] = "COL read fail"
            return out
        sig, off, cd, ptd, pchd = struct.unpack("<IIIII", col_raw)
        out["col"] = {
            "signature": sig, "offset": off, "cd_offset": cd,
            "p_type_descriptor": ptd, "p_class_hierarchy": pchd,
            "raw": col_raw.hex(),
        }
        td_raw = self.read_va(ptd, 0x48)
        if td_raw is None:
            out["error"] = "TD read fail"
            return out
        name_field = td_raw[8:]
        z = name_field.find(b"\x00")
        name_bytes = name_field[:z] if z >= 0 else name_field
        out["td"] = {
            "va": ptd,
            "vfptr": struct.unpack_from("<I", td_raw, 0)[0],
            "spare": struct.unpack_from("<I", td_raw, 4)[0],
            "name": name_bytes.decode("ascii", "replace"),
            "name_raw_hex": name_bytes[:40].hex(),
        }
        return out


def render_insn(i):
    return "%08X  %-26s %-7s %s" % (i["va"], i["bytes"], i["mnemonic"], i["op_str"])


def hexdump(pe, va, n):
    off = pe.va_to_off(va)
    d = pe.data
    lines = []
    for i in range(0, n, 16):
        chunk = d[off + i:off + i + 16]
        lines.append("%08X  %-47s  %s" % (
            va + i,
            " ".join("%02X" % c for c in chunk),
            "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)))
    return "\n".join(lines)


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()
