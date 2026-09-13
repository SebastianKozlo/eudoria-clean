# -*- coding: utf-8 -*-
# F1 census: (1) imm32 0x00A86850 (ArkObjectClass vtable) xrefs in .text;
# (2) direct CALL callers of ctor ArkObjectClass FUN_0070CF80 and factory FUN_0070BF50;
# (3) imm32 0x00BA58CC (DAT_00BA58CC) xrefs + write classification;
# (4) RTTI of ArkObject vtable 0x00A86B48; (5) imm32 0x00A86B48 xrefs.
# Output: 01_RAW/F1_CENSUS.json

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, u32

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F1_census", "measured": {}, "errors": []}


def rtti_of_vtable(vt):
    col = pe.read_va32(vt - 4)
    if not col:
        return None
    td = pe.read_va32(col + 0xC)
    if not td:
        return None
    name_b = pe.read_va(td + 8, 64)
    if name_b is None:
        return None
    name = name_b[:name_b.find(b"\x00")].decode("ascii", "replace")
    return {"vtable": "0x%08X" % vt, "col": "0x%08X" % col, "td": "0x%08X" % td, "name": name}


res["measured"]["rtti"] = {
    "0x00A86850": rtti_of_vtable(0x00A86850),
    "0x00A86B48": rtti_of_vtable(0x00A86B48),
}


def classify_imm32_hit(text_off):
    """Classify an imm32 hit by its preceding opcode bytes (instruction-context)."""
    tr = pe.text_raw
    va = pe.text_off_to_va(text_off)
    rec = {"va": "0x%08X" % va, "text_off": text_off}
    # look back for known encodings referencing imm32
    if text_off >= 1 and tr[text_off - 1] == 0xC7 and text_off >= 2 and tr[text_off - 2] in (0x05, 0x06, 0x07):
        rec["type"] = "MOV [imm/disp],imm32 (C7 /0)"  # vft write form C7 06 <imm32>
        rec["bytes_around"] = tr[text_off - 2:text_off + 6].hex()
    elif text_off >= 1 and tr[text_off - 1] in (0x05, 0x06, 0x07, 0x3D, 0x2D, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D, 0xA1, 0xA3):
        rec["type"] = "alu/mov with imm32 addr/val (opcode %02X)" % tr[text_off - 1]
        rec["bytes_around"] = tr[text_off - 1:text_off + 5].hex()
    elif text_off >= 1 and tr[text_off - 1] == 0x68:
        rec["type"] = "PUSH imm32 (68)"
        rec["bytes_around"] = tr[text_off - 1:text_off + 5].hex()
    elif text_off >= 2 and tr[text_off - 2] in (0xFF, 0x8B, 0x89, 0xC7, 0x3B, 0x39, 0x8D, 0x03, 0x0B, 0x13, 0x1B, 0x23, 0x2B, 0x33, 0x3B, 0xA1, 0xA3, 0x99, 0xB8, 0xB9, 0xBA, 0xBB, 0xBE, 0xBF):
        rec["type"] = "group2 (modrm disp32?)"
        rec["bytes_around"] = tr[text_off - 4:text_off + 6].hex()
    else:
        rec["type"] = "OTHER/disp32-or-mid-instruction"
        rec["bytes_around"] = tr[text_off - 4:text_off + 6].hex()
    return rec


for label, value in (("vtable_00A86850", 0x00A86850),
                     ("vtable_00A86B48", 0x00A86B48),
                     ("DAT_00BA58CC", 0x00BA58CC)):
    offs = pe.scan_text_imm32(value)
    recs = [classify_imm32_hit(o) for o in offs]
    res["measured"]["imm32_%s" % label] = {"count": len(offs), "hits": recs}

# direct CALL callers of key functions
for label, target in (("ctor_ArkObjectClass_0070CF80", 0x0070CF80),
                      ("factory_0070BF50", 0x0070BF50),
                      ("ctor_ArkObject_00726E70", 0x00726E70),
                      ("ctor_ArkSurgeonObject_007351E0", 0x007351E0)):
    sites = pe.calls_to(target)
    vas = ["0x%08X" % pe.text_off_to_va(o) for o in sites]
    res["measured"]["callers_%s" % label] = {"count": len(sites), "call_sites": vas}

# E9 JMP rel32 to ctor FUN_0070CF80 (tail-jump pattern) — catches jump-based calls
for label, target in (("ctor_ArkObjectClass_0070CF80", 0x0070CF80),
                      ("factory_0070BF50", 0x0070BF50)):
    tr = pe.text_raw
    jsites = []
    for i in range(len(tr) - 5):
        if tr[i] == 0xE9:
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            if pe.text_va_start + i + 5 + rel == target:
                jsites.append("0x%08X" % (pe.text_va_start + i))
    res["measured"]["jmp_callers_%s" % label] = {"count": len(jsites), "sites": jsites}

# non-.text xrefs: scan .rdata/.data raw for the imm32 values (vtable references in data,
# e.g. other vtables/RTTI/COL structures)
for label, value in (("rdata_scan_00A86850", 0x00A86850),
                     ("rdata_scan_00BA58CC", 0x00BA58CC),
                     ("data_scan_00A86850", 0x00A86850),
                     ("data_scan_00BA58CC", 0x00BA58CC)):
    secname = ".rdata" if label.startswith("rdata") else ".data"
    for s in pe.sections:
        if s["name"] == secname:
            raw = pe.data[s["rptr"]:s["rptr"] + s["rsize"]]
            pat = struct.pack("<I", value)
            hits = []
            start = 0
            while True:
                i = raw.find(pat, start)
                if i < 0:
                    break
                hits.append("0x%08X" % (s["va_start"] + i))
                start = i + 1
            res["measured"][label] = {"count": len(hits), "hits": hits}

with open(os.path.join(OUT, "F1_CENSUS.json"), "w") as f:
    json.dump(res, f, indent=2)

print("F1_CENSUS done")
for k, v in res["measured"].items():
    if isinstance(v, dict) and "count" in v:
        print("%-42s count=%d" % (k, v["count"]))
    elif k == "rtti":
        for kk, vv in v.items():
            print("rtti", kk, "->", vv)
