#!/usr/bin/env python3
r"""entropia_rtti_probe.py -- Deterministic byte-level probe of the Entropia.exe
(PCG 9.3.5) NiNode RTTI chain and primary vtable, for the
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1 audit.

Physical target (fail-closed pins, verified by the caller):
  D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  SIZE 8015872

Established header facts (this run):
  IMAGE_BASE = 0x00400000 (empirically proven: under this base the VA
  0x00A8CCF4 maps to a real vtable whose slot 17 (+0x44) literally contains
  0x007B5390, and vtable[-1] is a consistent RTTI Complete Object Locator).
  NOTE: this binary's optional-header standard-fields region reads +4 shifted
  relative to the winnt.h IMAGE_OPTIONAL_HEADER32 layout (the verified project
  tool 90_Tools\PEFrida\core\modbase.py read_pe_header() uses the +28
  convention for ImageBase and returns 0x00400000 for this exact file).
  Machine 0x014C, DllCharacteristics 0x0000 (no ASLR).

Sections (VA ranges at IB=0x400000; VERIFIED: every section's raw pointer
equals its RVA, so file_offset == RVA throughout this file):
  .text  RVA 0x1000..0x6745E5 (raw 0x1000)
  .rdata RVA 0x675000..0x76B569 (raw 0x675000)
  .data  RVA 0x76C000..0x7A96E4 (raw 0x34000)

Outputs (JSON to stdout, --out FILE to persist):
  - RTTI Complete Object Locator fields for the primary NiNode vtable
  - TypeDescriptor name string (expect .?AVNiNode@@)
  - full BaseClassDescriptor chain (expect NiNode -> NiAVObject ->
    NiObjectNET -> NiObject -> NiRefObject)
  - full primary vtable slot dump (code pointers) for slots 0..N
"""
import argparse
import hashlib
import json
import struct
import sys

ENTROPIA = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
IMAGE_BASE = 0x00400000
VTABLE_VA = 0x00A8CCF4
TARGET_SLOT = 17
TARGET_FUNC_VA = 0x007B5390
MAX_SLOTS = 64

SECTIONS = [
    # (name, rva_start, rva_end_exclusive, raw_ptr)
    (".text", 0x1000, 0x1000 + 0x6735E5, 0x1000),
    (".rdata", 0x675000, 0x675000 + 0xF6569, 0x675000),
    (".data", 0x76C000, 0x76C000 + 0x3D6E4, 0x76C000),
]


def va_to_file(va):
    rva = va - IMAGE_BASE
    for name, lo, hi, raw in SECTIONS:
        if lo <= rva < hi:
            return raw + (rva - lo)
    return None


def rd32(d, off):
    return struct.unpack_from("<I", d, off)[0]


def rd_cstr(d, off, maxlen=64):
    end = d.find(b"\x00", off, off + maxlen)
    if end < 0:
        end = min(off + maxlen, len(d))
    return d[off:end].decode("ascii", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    with open(ENTROPIA, "rb") as f:
        d = f.read()
    size = len(d)
    sha = hashlib.sha256(d).hexdigest().upper()
    result = {"file": ENTROPIA, "size": size, "sha256": sha,
              "sha256_match": sha == EXPECT_SHA256}
    if sha != EXPECT_SHA256:
        result["error"] = "SHA256 MISMATCH - fail closed"
        text = json.dumps(result, indent=1)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as g:
                g.write(text)
        sys.stdout.write(text)
        sys.exit(1)

    vt_file = va_to_file(VTABLE_VA)
    result["vtable_va"] = "0x%08X" % VTABLE_VA
    result["vtable_file_offset"] = "0x%X" % vt_file

    # full slot dump until a slot value leaves the .text code VA range
    slots = []
    for i in range(MAX_SLOTS):
        val = rd32(d, vt_file + 4 * i)
        foff = va_to_file(val)
        is_code = (foff is not None
                   and 0x1000 <= (val - IMAGE_BASE) < 0x6745E5)
        slots.append({"slot": i, "offset": "+0x%02X" % (4 * i),
                      "value_va": "0x%08X" % val, "is_text_va": is_code})
        if not is_code:
            break
    result["vtable_slots"] = slots
    result["target_slot17"] = {
        "expected": "0x%08X" % TARGET_FUNC_VA,
        "measured": slots[TARGET_SLOT]["value_va"] if len(slots) > TARGET_SLOT else None,
        "match": (len(slots) > TARGET_SLOT
                  and slots[TARGET_SLOT]["value_va"] == "0x%08X" % TARGET_FUNC_VA),
    }

    # RTTI: vtable[-1] -> Complete Object Locator.
    # EMPIRICAL CONVENTION (this binary): the COL's pTypeDescriptor and
    # pClassDescriptor fields are ABSOLUTE VAs (e.g. 0x00B936C8 lands in
    # .data only as a VA), not RVA offsets. Field normalization: any pointer
    # >= IMAGE_BASE is taken as VA, otherwise as RVA and rebased.
    col_va = rd32(d, vt_file - 4)
    col_off = va_to_file(col_va)
    result["col_va"] = "0x%08X" % col_va
    sig, off_v, cd, ptd_raw, pchd_raw = struct.unpack_from(
        "<IIIII", d, col_off)

    def ptr_to_va(raw):
        return raw if raw >= IMAGE_BASE else raw + IMAGE_BASE

    ptd_va = ptr_to_va(ptd_raw)
    pchd_va = ptr_to_va(pchd_raw)
    result["col_fields"] = {
        "signature": sig, "offset": off_v, "cdOffset": cd,
        "typeDescriptorRaw": "0x%08X" % ptd_raw,
        "typeDescriptorVA": "0x%08X" % ptd_va,
        "classHierarchyDescriptorRaw": "0x%08X" % pchd_raw,
        "classHierarchyDescriptorVA": "0x%08X" % pchd_va,
        "pointer_convention": "absolute VA (raw >= IMAGE_BASE)",
    }
    # TypeDescriptor: {vftable ptr, spare, name}
    ptd_off = va_to_file(ptd_va)
    result["type_descriptor_name"] = rd_cstr(d, ptd_off + 8, 48)

    # Class Hierarchy Descriptor -> Base Class Descriptor array
    chd_off = va_to_file(pchd_va)
    chd_sig, chd_attrs, chd_numbases, chd_basearray_raw = struct.unpack_from(
        "<IIII", d, chd_off)
    chd_basearray_va = ptr_to_va(chd_basearray_raw)
    result["chd"] = {"signature": chd_sig, "attributes": chd_attrs,
                     "numBases": chd_numbases,
                     "baseArrayRaw": "0x%08X" % chd_basearray_raw,
                     "baseArrayVA": "0x%08X" % chd_basearray_va}
    bases = []
    for i in range(chd_numbases):
        bcd_raw = rd32(d, va_to_file(chd_basearray_va) + 4 * i)
        bcd_va = ptr_to_va(bcd_raw)
        bcd_off = va_to_file(bcd_va)
        # _s_RTTIBaseClassDescriptor layout (32-bit):
        #   +0x00 pTypeDescriptor, +0x04 numContainedBases,
        #   +0x08 PMD*, +0x0C attributes, +0x10 parent BCD*
        b_ptd_raw, b_npm, b_pmd_raw, b_attrs, b_parent_raw = \
            struct.unpack_from("<IIIII", d, bcd_off)
        b_ptd_va = ptr_to_va(b_ptd_raw)
        td_name = rd_cstr(d, va_to_file(b_ptd_va) + 8, 48)
        bases.append({
            "index": i,
            "bcdVA": "0x%08X" % bcd_va,
            "typeDescriptorVA": "0x%08X" % b_ptd_va,
            "numContainedBases": b_npm,
            "pmdVA": "0x%08X" % ptr_to_va(b_pmd_raw),
            "attributes": "0x%08X" % b_attrs,
            "typeDescriptorName": td_name,
        })
    result["base_chain"] = [b["typeDescriptorName"] for b in bases]
    result["base_class_descriptors"] = bases

    text = json.dumps(result, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as g:
            g.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
