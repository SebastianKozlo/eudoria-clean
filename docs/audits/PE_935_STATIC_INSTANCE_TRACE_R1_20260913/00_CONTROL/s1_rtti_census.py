# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S1 RTTI CENSUS (Z1)
# STATIC-ONLY raw scan of Entropia.exe .rdata for MSVC RTTI type-descriptor names.
# Type descriptor name strings: ".?AV<name>@" (class) / ".?AU<name>@" (struct).
# Census: ALL classes + keyword filter (Ark*, boost::, World/Sector/Cell/Zone/Region/
# Static/Object/Instance/Factory/Entity/Avatar/Item).
# Writes 01_RAW/S1_RTTI_CENSUS.json (+ keyword-filtered view printed).

import json
import os
import re

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

IMAGE_BASE = 0x00400000
# sections from S0
SECTIONS = [
    (".text",  0x00401000, 0x00A75000, 4096,      6766592),
    (".rdata", 0x00A75000, 0x00B6C000, 6770688,   1011712),
    (".data",  0x00B6C000, 0x00BA96E4, 7782400,   212992),
    (".tls",   0x00BAA000, 0x00BAB000, 7995392,   4096),
    (".rsrc",  0x00BAB000, 0x00BAF000, 7999488,   16384),
]

def va_of(file_off):
    for name, vs, ve, rp, rs in SECTIONS:
        if rp <= file_off < rp + rs:
            for n2, vs2, ve2, rp2, rs2 in SECTIONS:
                pass
            # invert: va = image_base + rva; rva = vaddr + (off - raw_ptr)
            rva = None
            if name == ".text": rva = 0x1000 + (file_off - 4096)
            elif name == ".rdata": rva = 0x675000 + (file_off - 6770688)
            elif name == ".data": rva = 0x76C000 + (file_off - 7782400)
            elif name == ".tls": rva = 0x7AA000 + (file_off - 7995392)
            elif name == ".rsrc": rva = 0x7AB000 + (file_off - 7999488)
            return IMAGE_BASE + rva
    return None

def section_of(va):
    for name, vs, ve, rp, rs in SECTIONS:
        if vs <= va < ve:
            return name
    return None

KEYWORDS = ["World", "Sector", "Cell", "Zone", "Region", "Static", "Object",
            "Instance", "Factory", "Entity", "Avatar", "Item"]

def main():
    data = open(EXE, "rb").read()
    hits = []
    for m in re.finditer(rb"\.\?A[UV][\x20-\x7e]+?\x00", data):
        off = m.start()
        raw = m.group()
        name = raw[:-1].decode("ascii", "replace")  # e.g. .?AVArkSector@@
        va = va_of(off)
        if va is None:
            continue
        hits.append({"va": "0x%08X" % va, "file_offset": off,
                     "section": section_of(va), "mangled": name})

    # dedupe (same name may appear multiple times; keep all VAs but count)
    from collections import Counter
    name_counts = Counter(h["mangled"] for h in hits)

    ark = [h for h in hits if ".?AVArk" in h["mangled"] or ".?AUArk" in h["mangled"]]
    boost = [h for h in hits if "boost" in h["mangled"].lower()]
    kw = {}
    for k in KEYWORDS:
        kw[k] = [h for h in hits if k.lower() in h["mangled"].lower()]

    out = {
        "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
        "stage": "S1_rtti_census",
        "total_type_descriptor_strings": len(hits),
        "unique_names": len(name_counts),
        "all_hits": hits,
        "ark_prefixed": ark,
        "boost_count": len(boost),
        "keyword_hits": kw,
    }
    with open(os.path.join(OUT, "S1_RTTI_CENSUS.json"), "w") as f:
        json.dump(out, f, indent=2)

    # CSV for humans
    with open(os.path.join(OUT, "S1_RTTI_CENSUS.csv"), "w") as f:
        f.write("va,section,mangled\n")
        for h in hits:
            f.write("%s,%s,%s\n" % (h["va"], h["section"], h["mangled"]))

    print("S1_DONE total=%d unique=%d ark=%d boost=%d" % (
        len(hits), len(name_counts), len(ark), len(boost)))
    print("--- Ark classes ---")
    for h in ark:
        print("%s  %s" % (h["va"], h["mangled"]))

if __name__ == "__main__":
    main()
