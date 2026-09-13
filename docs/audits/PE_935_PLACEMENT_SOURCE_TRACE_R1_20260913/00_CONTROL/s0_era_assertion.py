# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S0 ERA ASSERTION (independent)
# STATIC-ONLY. Verifies: SHA256, file size, DOS/PE headers, sections, ASLR off,
# VA<->file-offset mapping rules. Writes 01_RAW/S0_ERA_ASSERTION.json.
# Fail-closed: any mismatch -> exit 1, no downstream work.

import hashlib
import json
import os
import struct
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

EXPECT_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECT_SIZE = 8015872
EXPECT_IMAGE_BASE = 0x00400000

def main():
    data = open(EXE, "rb").read()
    size = len(data)
    sha = hashlib.sha256(data).hexdigest().upper()

    errs = []
    if size != EXPECT_SIZE:
        errs.append("size %d != %d" % (size, EXPECT_SIZE))
    if sha != EXPECT_SHA256:
        errs.append("sha %s != %s" % (sha, EXPECT_SHA256))

    dos_magic = struct.unpack_from("<H", data, 0)[0]
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if dos_magic != 0x5A4D:
        errs.append("dos_magic %04X" % dos_magic)
    pe_sig = struct.unpack_from("<I", data, e_lfanew)[0]
    if pe_sig != 0x00004550:
        errs.append("pe_sig %08X" % pe_sig)
    coff = e_lfanew + 4
    machine, num_sections, timestamp = struct.unpack_from("<HHI", data, coff)
    opt_size = struct.unpack_from("<H", data, coff + 16)[0]
    opt = coff + 20
    opt_magic = struct.unpack_from("<H", data, opt)[0]
    image_base = struct.unpack_from("<I", data, opt + 28)[0]
    dll_chars = struct.unpack_from("<H", data, opt + 70)[0]
    aslr = bool(dll_chars & 0x0040)
    if image_base != EXPECT_IMAGE_BASE:
        errs.append("image_base %08X" % image_base)
    if aslr:
        errs.append("ASLR ENABLED (dll_chars %04X)" % dll_chars)

    sec_off = opt + opt_size
    sections = []
    for i in range(num_sections):
        o = sec_off + i * 40
        name = data[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, o + 8)
        sections.append({
            "name": name, "virtual_size": vsize, "virtual_address_rva": vaddr,
            "raw_size": rsize, "raw_ptr": rptr,
            "va_start": image_base + vaddr,
            "va_end": image_base + vaddr + max(vsize, rsize),
        })

    def va_to_file(va):
        rva = va - image_base
        for s in sections:
            if s["virtual_address_rva"] <= rva < s["virtual_address_rva"] + s["raw_size"]:
                return s["raw_ptr"] + (rva - s["virtual_address_rva"])
        return None

    spot = {}
    checks = [
        # (label, va, expected_file_offset or None, expected_section)
        ("entry@0x0095DA11", 0x0095DA11, 5626385, ".text"),
        ("string_Parameters_templates.vfs@0x00A86D30", 0x00A86D30, None, ".rdata"),
        ("RTTI_ArkParameterContainer@0x00B8ED14", 0x00B8ED14, None, ".data"),
        ("RTTI_ArkPacketDecoder@0x00B96F70", 0x00B96F70, None, ".data"),
        ("FUN_00846840_entry", 0x00846840, None, ".text"),
        ("string_portals.bnt@0x00A7A7CC", 0x00A7A7CC, None, ".rdata"),
    ]
    for label, va, exp_off, exp_sec in checks:
        off = va_to_file(va)
        sec = None
        for s in sections:
            if s["va_start"] <= va < s["va_end"]:
                sec = s["name"]
        rec = {"va": "0x%08X" % va, "file_offset": (None if off is None else off),
               "section": sec, "raw_bytes_at_offset": None}
        if off is not None:
            rec["raw_bytes_at_offset"] = data[off:off+16].hex()
        if off is not None and exp_off is not None and off != exp_off:
            errs.append("spot %s: offset %d != %d" % (label, off, exp_off))
        if sec != exp_sec:
            errs.append("spot %s: section %s != %s" % (label, sec, exp_sec))
        spot[label] = rec

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S0_era_assertion",
        "measured": {
            "sha256": sha, "file_size": size, "e_lfanew": e_lfanew,
            "machine": "0x%04X" % machine, "num_sections": num_sections,
            "time_date_stamp": timestamp, "image_base": "0x%08X" % image_base,
            "dll_characteristics": "0x%04X" % dll_chars, "aslr_enabled": aslr,
            "sections": [
                {"name": s["name"], "va_start": "0x%08X" % s["va_start"],
                 "va_end": "0x%08X" % s["va_end"], "raw_ptr": s["raw_ptr"],
                 "raw_size": s["raw_size"], "virtual_size": s["virtual_size"],
                 "virtual_address_rva": "0x%06X" % s["virtual_address_rva"]}
                for s in sections
            ],
            "spot_checks": spot,
        },
        "mapping_rule": ("VA = image_base + RVA; file_offset = section.raw_ptr + "
                         "(RVA - section.virtual_address_rva) while within raw_size. "
                         "Every VA cited in this run must derive through this table."),
        "errors": errs,
    }
    with open(os.path.join(OUT, "S0_ERA_ASSERTION.json"), "w") as f:
        json.dump(result, f, indent=2)

    if errs:
        print("S0_FAIL", errs)
        sys.exit(1)
    print("S0_PASS sha=%s size=%d image_base=0x%08X aslr=%s sections=%d"
          % (sha, size, image_base, aslr, num_sections))

if __name__ == "__main__":
    main()
