# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S2 STRING CENSUS (Z5 support)
# STATIC-ONLY raw scan of Entropia.exe for world/loader-relevant ASCII strings.
# Focus: Sector/Zone/World/Region/Cell/portal/TEZ/tdf/amu/prt/vegetation/terrain/
#        Parameters paths / .vfs / .pak / .xbc / file names.
# Writes 01_RAW/S2_STRING_CENSUS.json (+ filtered printout).

import json
import os
import re

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

IMAGE_BASE = 0x00400000

def va_of(file_off):
    if 4096 <= file_off < 4096 + 6766592:
        return IMAGE_BASE + 0x1000 + (file_off - 4096), ".text"
    if 6770688 <= file_off < 6770688 + 1011712:
        return IMAGE_BASE + 0x675000 + (file_off - 6770688), ".rdata"
    if 7782400 <= file_off < 7782400 + 212992:
        return IMAGE_BASE + 0x76C000 + (file_off - 7782400), ".data"
    if 7995392 <= file_off < 7995392 + 4096:
        return IMAGE_BASE + 0x7AA000 + (file_off - 7995392), ".tls"
    if 7999488 <= file_off < 7999488 + 16384:
        return IMAGE_BASE + 0x7AB000 + (file_off - 7999488), ".rsrc"
    return None, None

# all printable ASCII strings >= 4 chars
pat = re.compile(rb"[\x20-\x7e]{4,}")

INTEREST = [
    # Z5 loader keywords
    "sector", "zone", "region", "cell", "portal", "world", "terrain",
    "vegetation", "climate", "environment", "tezed", "tez", "tdf", "amu",
    "edit", "space", "scene", "placement", "position", "coordinate",
    "template", "hierarchy", "parameter", ".vfs", ".pak", ".xbc", ".bnt",
    ".prt", ".prt", ".nif", ".bvi", ".cfg", ".ini", ".dat",
    "data\\", "data/", "parameters", "models", "volumes", "strings",
    "sids", "materials", "objects", "planet",
]

def main():
    data = open(EXE, "rb").read()
    all_strings = []
    for m in pat.finditer(data):
        off = m.start()
        va, sec = va_of(off)
        if va is None:
            continue
        s = m.group().decode("ascii", "replace")
        all_strings.append({"va": "0x%08X" % va, "file_offset": off,
                            "section": sec, "text": s})

    # interesting subset (case-insensitive keyword match, token-ish boundaries)
    interesting = []
    for h in all_strings:
        low = h["text"].lower()
        for kw in INTEREST:
            if kw in low:
                h2 = dict(h)
                h2["matched"] = [k for k in INTEREST if k in low]
                interesting.append(h2)
                break

    out = {
        "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
        "stage": "S2_string_census",
        "total_strings": len(all_strings),
        "interesting_count": len(interesting),
        "interesting": interesting,
    }
    with open(os.path.join(OUT, "S2_STRING_CENSUS.json"), "w") as f:
        json.dump(out, f, indent=2)
    with open(os.path.join(OUT, "S2_STRING_CENSUS_ALL.txt"), "w") as f:
        for h in all_strings:
            f.write("%s %s %s\n" % (h["va"], h["section"], h["text"]))

    print("S2_DONE total=%d interesting=%d" % (len(all_strings), len(interesting)))

    # print focused groups
    def show(label, pred, limit=80):
        print("--- %s ---" % label)
        n = 0
        for h in interesting:
            if pred(h["text"]):
                print("  %s  %s" % (h["va"], h["text"][:120]))
                n += 1
                if n >= limit:
                    break

    show("sector/region/cell", lambda t: re.search(r"sector|region|cell", t, re.I))
    show("portal", lambda t: "portal" in t.lower())
    show("world", lambda t: "world" in t.lower())
    show("zone", lambda t: "zone" in t.lower())
    show("file-ext/prt/amu", lambda t: re.search(r"\.(prt|amu|tez|xbc|pak)\b|tezed", t, re.I))
    show("paths(Data)", lambda t: "data" in t.lower() and ("\\" in t or "/" in t))

if __name__ == "__main__":
    main()
