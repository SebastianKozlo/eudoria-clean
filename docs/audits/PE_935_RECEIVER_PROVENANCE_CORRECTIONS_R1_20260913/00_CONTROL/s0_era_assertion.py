# -*- coding: utf-8 -*-
# PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 — S0 ERA ASSERTION (independent)
# STATIC-ONLY. Fail-closed on BOTH inputs: Entropia.exe + templates.vfs.
# Mismatch -> exit 1 (HARD STOP), no downstream work.

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"

EXPECT = {
    "exe": {
        "sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
        "size": 8015872,
        "image_base": 0x00400000,
    },
    "templates_vfs": {
        "sha256": "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77",
        "size": 560788,
    },
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()

def main():
    errs = []

    vfs_data = open(VFS, "rb").read()
    vfs_sha = hashlib.sha256(vfs_data).hexdigest().upper()
    vfs_size = len(vfs_data)
    if vfs_size != EXPECT["templates_vfs"]["size"]:
        errs.append("templates.vfs size %d != %d" % (vfs_size, EXPECT["templates_vfs"]["size"]))
    if vfs_sha != EXPECT["templates_vfs"]["sha256"]:
        errs.append("templates.vfs sha %s != %s" % (vfs_sha, EXPECT["templates_vfs"]["sha256"]))

    pe = PE(EXE)
    size = len(pe.data)
    sha = sha256_file(EXE)
    if size != EXPECT["exe"]["size"]:
        errs.append("exe size %d != %d" % (size, EXPECT["exe"]["size"]))
    if sha != EXPECT["exe"]["sha256"]:
        errs.append("exe sha %s != %s" % (sha, EXPECT["exe"]["sha256"]))
    if pe.image_base != EXPECT["exe"]["image_base"]:
        errs.append("image_base 0x%08X" % pe.image_base)
    if pe.aslr:
        errs.append("ASLR ENABLED (dll_chars 0x%04X)" % pe.dll_chars)

    spot = {}
    checks = [
        ("entry@0x0095DA11", 0x0095DA11, 5626385, ".text"),
        ("string_Parameters_templates.vfs@0x00A86D30", 0x00A86D30, 6843696, ".rdata"),
        ("vtable_ArkObjectClass@0x00A86850", 0x00A86850, None, ".rdata"),
        ("TD_ArkObjectClass@0x00B8D068", 0x00B8D068, None, ".data"),
        ("getter_A_FUN_007CE1E0", 0x007CE1E0, None, ".text"),
        ("getter_D_FUN_0048ADA0", 0x0048ADA0, None, ".text"),
        ("jumptable_00855BB4", 0x00855BB4, None, ".text"),
        ("DAT_00BA58CC", 0x00BA58CC, None, ".data"),
    ]
    for label, va, exp_off, exp_sec in checks:
        off = pe.va_to_off(va)
        sec = pe.section_of(va)
        rec = {"va": "0x%08X" % va, "file_offset": off, "section": sec,
               "raw_bytes_at_offset": None}
        if off is not None:
            rec["raw_bytes_at_offset"] = pe.data[off:off + 16].hex()
        if off is not None and exp_off is not None and off != exp_off:
            errs.append("spot %s: offset %d != %d" % (label, off, exp_off))
        if sec != exp_sec:
            errs.append("spot %s: section %s != %s" % (label, sec, exp_sec))
        spot[label] = rec

    result = {
        "run_id": "PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
        "stage": "S0_era_assertion",
        "measured": {
            "exe": {
                "path": EXE, "sha256": sha, "file_size": size,
                "e_lfanew": pe.e_lfanew, "machine": "0x%04X" % pe.machine,
                "num_sections": pe.num_sections,
                "time_date_stamp": pe.timestamp,
                "image_base": "0x%08X" % pe.image_base,
                "dll_characteristics": "0x%04X" % pe.dll_chars,
                "aslr_enabled": pe.aslr,
                "entry_rva": "0x%08X" % pe.entry_rva,
                "sections": [
                    {"name": s["name"], "va_start": "0x%08X" % s["va_start"],
                     "va_end": "0x%08X" % s["va_end"], "raw_ptr": s["rptr"],
                     "raw_size": s["rsize"], "virtual_size": s["vsize"],
                     "virtual_address_rva": "0x%06X" % s["vaddr"]}
                    for s in pe.sections
                ],
                "spot_checks": spot,
            },
            "templates_vfs": {
                "path": VFS, "sha256": vfs_sha, "file_size": vfs_size,
            },
        },
        "mapping_rule": ("VA = image_base + RVA; file_offset = section.raw_ptr + "
                         "(RVA - section.virtual_address_rva) while within raw_size. "
                         "Every VA cited in this run must derive through pe_core.PE."),
        "errors": errs,
    }
    with open(os.path.join(OUT, "S0_ERA_ASSERTION.json"), "w") as f:
        json.dump(result, f, indent=2)

    if errs:
        print("S0_FAIL", errs)
        sys.exit(1)
    print("S0_PASS exe_sha=%s vfs_sha=%s" % (sha, vfs_sha))

if __name__ == "__main__":
    main()
