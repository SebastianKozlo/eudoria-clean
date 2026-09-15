# sf_arg2_common.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# Shared S0 fail-closed identity gate + PE mapping + provenance header.
#
# STATIC-ONLY run: Entropia.exe is NEVER executed. This module only READS bytes.
#
# FAIL-CLOSED RULE (RUN_CONTRACT G0/H): every importing script must construct
# PinnedExe() BEFORE any analysis byte read. The ONLY reads performed before the
# gate is the identity read itself (whole-file SHA256 + PE header sanity fields);
# if identity fails, the constructor raises SourceIdentityFail and no analysis
# read can ever happen (all analysis reads go through read_va/read_off, which
# assert the gate). This is the fail-closed SHA256+SIZE assert before any byte
# read required by the contract.
#
# Provenance convention (contract H): measured at run time, never assumed:
#   python version + path, capstone __version__ + __file__.
#   (The 5.0.9 dist-info label is a known false label; trust the measured
#    capstone.__version__. At formalize time: 5.0.7 at
#    D:\Eudoria_Reconstruction\10_Scripts\python_env\Lib\site-packages\capstone\__init__.py)

import hashlib
import struct
import sys

import capstone

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PIN_SIZE = 8015872
PIN_SHA256_UPPER = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PIN_MACHINE = 0x014C
PIN_OPT_MAGIC = 0x010B
PIN_IMAGE_BASE = 0x00400000


class SourceIdentityFail(Exception):
    pass


def provenance_header():
    return (
        "PROVENANCE (measured at run time, not assumed):\n"
        f"  python_version : {sys.version}\n"
        f"  python_exe     : {sys.executable}\n"
        f"  capstone_version : {capstone.__version__}\n"
        f"  capstone_file    : {capstone.__file__}\n"
    )


class PinnedExe:
    """Fail-closed pinned EXE reader. Identity asserted in __init__."""

    def __init__(self, path=EXE_PATH):
        with open(path, "rb") as f:
            data = f.read()
        # ---- identity reads (the verification read itself) ----
        self.path = path
        self.size = len(data)
        self.sha256 = hashlib.sha256(data).hexdigest().upper()
        if self.size != PIN_SIZE:
            raise SourceIdentityFail(
                f"SOURCE_IDENTITY_FAIL size: measured {self.size} != pin {PIN_SIZE}"
            )
        if self.sha256 != PIN_SHA256_UPPER:
            raise SourceIdentityFail(
                f"SOURCE_IDENTITY_FAIL sha256: measured {self.sha256} != pin {PIN_SHA256_UPPER}"
            )
        # ---- PE32 sanity ----
        if data[:2] != b"MZ":
            raise SourceIdentityFail("SOURCE_IDENTITY_FAIL: no MZ magic")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew : e_lfanew + 4] != b"PE\x00\x00":
            raise SourceIdentityFail("SOURCE_IDENTITY_FAIL: no PE signature")
        machine = struct.unpack_from("<H", data, e_lfanew + 4)[0]
        if machine != PIN_MACHINE:
            raise SourceIdentityFail(
                f"SOURCE_IDENTITY_FAIL machine: {machine:#06x} != {PIN_MACHINE:#06x}"
            )
        opt_off = e_lfanew + 24
        magic = struct.unpack_from("<H", data, opt_off)[0]
        if magic != PIN_OPT_MAGIC:
            raise SourceIdentityFail(
                f"SOURCE_IDENTITY_FAIL opt_magic: {magic:#06x} != {PIN_OPT_MAGIC:#06x}"
            )
        image_base = struct.unpack_from("<I", data, opt_off + 28)[0]
        if image_base != PIN_IMAGE_BASE:
            raise SourceIdentityFail(
                f"SOURCE_IDENTITY_FAIL image_base: {image_base:#010x} != {PIN_IMAGE_BASE:#010x}"
            )
        # ---- sections ----
        num_sections = struct.unpack_from("<H", data, e_lfanew + 6)[0]
        opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
        sec_off = e_lfanew + 24 + opt_size
        self.sections = []
        for i in range(num_sections):
            off = sec_off + i * 40
            name = data[off : off + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append(
                {"name": name, "vaddr": vaddr, "vsize": vsize, "rawptr": rawptr, "rawsize": rawsize}
            )
        self.e_lfanew = e_lfanew
        self.machine = machine
        self.image_base = image_base
        self._gate_passed = True
        # gate passed: analysis reads now allowed
        self.data = data

    # ---------------- mapping ----------------
    def section_of_rva(self, rva):
        for s in self.sections:
            span = max(s["vsize"], s["rawsize"])
            if s["vaddr"] <= rva < s["vaddr"] + span:
                return s
        return None

    def va_to_off(self, va):
        if not getattr(self, "_gate_passed", False):
            raise SourceIdentityFail("gate not passed; analysis read refused")
        rva = va - self.image_base
        s = self.section_of_rva(rva)
        if s is None:
            return None
        delta = rva - s["vaddr"]
        if delta >= s["rawsize"]:
            return None  # virtual-only tail (e.g. .bss): no file bytes
        return s["rawptr"] + delta

    def off_to_va(self, off):
        for s in self.sections:
            if s["rawptr"] <= off < s["rawptr"] + s["rawsize"]:
                return self.image_base + s["vaddr"] + (off - s["rawptr"])
        return None

    def section_name_of_va(self, va):
        s = self.section_of_rva(va - self.image_base)
        return s["name"] if s else "<none>"

    # ---------------- gated analysis reads ----------------
    def read_va(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            raise ValueError(f"VA {va:#010x} has no file bytes")
        return self.data[off : off + n]

    def read_off(self, off, n):
        if not getattr(self, "_gate_passed", False):
            raise SourceIdentityFail("gate not passed; analysis read refused")
        return self.data[off : off + n]

    def text_section(self):
        for s in self.sections:
            if s["name"] == ".text":
                return s
        raise SourceIdentityFail("no .text section")


def make_capstone():
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    return md


def insn_str(insn):
    """VA + bytes + mnemonic + operands, single line."""
    b = " ".join(f"{x:02X}" for x in insn.bytes)
    return f"{insn.address:08X}  {b:<24}  {insn.mnemonic} {insn.op_str}".rstrip()
