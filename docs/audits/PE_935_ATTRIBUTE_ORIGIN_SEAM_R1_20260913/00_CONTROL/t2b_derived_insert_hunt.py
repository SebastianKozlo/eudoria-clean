# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 — TASK 2b: derived value class + insert hunt.
# FUN_00528E50 = derived ctor (base MovableObject ctor + vtable 0x00A7DCB0).
# Census its callers -> insert seam. RTTI of 0x00A7DCB0. Hash-map ctor decode.
# STATIC-ONLY.

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ID = "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

DERIVED_CTOR = 0x00528E50
DERIVED_VTABLE = 0x00A7DCB0

def calls_all(pe, target_va):
    out = []
    tr = pe.text_raw
    base = pe.text_va_start
    for i in range(len(tr) - 5):
        if tr[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            t = base + i + 5 + rel
            if t == target_va:
                out.append({"op": "E8" if tr[i] == 0xE8 else "E9",
                            "site_va": "0x%08X" % (base + i)})
    return out

def rtti_name(pe, vtable_va):
    res = {"vtable_va": "0x%08X" % vtable_va}
    col = pe.read_va32(vtable_va - 4)
    res["col_ptr"] = ("0x%08X" % col) if col else None
    if col is None or pe.section_of(col) is None:
        res["error"] = "col not in sections"
        return res
    res["col_raw16"] = (pe.read_va(col, 16) or b"").hex()
    td = pe.read_va32(col + 0xC)
    res["td_ptr"] = ("0x%08X" % td) if td else None
    if td is None or pe.section_of(td) is None:
        res["error"] = "td not in sections"
        return res
    td_raw = pe.read_va(td, 0x60) or b""
    res["td_raw_0x60"] = td_raw.hex()
    end = td_raw.find(b"\x00", 8)
    nb = td_raw[8:end] if end > 0 else b""
    res["td_name_raw"] = nb.hex()
    res["td_name"] = nb.decode("ascii", "replace")
    return res

def find_func_start(pe, va, back_max=0x2000):
    off = pe.va_to_off(va)
    d = pe.data
    lo = max(off - back_max, 0)
    i = off
    while i > lo:
        if d[i] == 0xCC and d[i - 1] == 0xCC and d[i - 2] == 0xCC:
            j = i
            while d[j - 1] == 0xCC and j > lo:
                j -= 1
            k = i + 1
            while d[k] == 0xCC:
                k += 1
            return pe.off_to_va(k)
        i -= 1
    return None

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T2b_derived_insert_hunt", "measured": {}, "errors": []}
    m = res["measured"]

    # RTTI of derived vtable
    m["derived_vtable_rtti"] = rtti_name(pe, DERIVED_VTABLE)
    m["derived_vtable_raw"] = (pe.read_va(DERIVED_VTABLE, 64) or b"").hex()
    slots = []
    for i in range(16):
        v = pe.read_va32(DERIVED_VTABLE + 4 * i)
        slots.append({"slot": i, "target": ("0x%08X" % v) if v else None,
                      "section": pe.section_of(v) if v else None})
    m["derived_vtable_slots"] = slots

    # census: vtable writes of derived vtable in .text
    hits = pe.scan_text_imm32(DERIVED_VTABLE)
    ctx = []
    for off in hits:
        va = pe.text_off_to_va(off)
        ctx.append({"va": "0x%08X" % va,
                    "before10": (pe.read_va(va - 10, 10) or b"").hex(),
                    "after6": (pe.read_va(va + 4, 6) or b"").hex()})
    m["census_imm32_derived_vtable"] = {"count": len(hits), "hits": ctx}

    # census: callers of derived ctor
    m["census_raw_calls_to_derived_ctor"] = calls_all(pe, DERIVED_CTOR)

    # for each caller site: function start + full hexdump + call edges
    callers = []
    for c in m["census_raw_calls_to_derived_ctor"]:
        site = int(c["site_va"], 16)
        fs = find_func_start(pe, site)
        entry = {"call_site": c["site_va"], "op": c["op"],
                 "func_start": ("0x%08X" % fs) if fs else None}
        if fs:
            end_va, body = pe.func_body(fs, maxb=0x6000)
            entry["body_end"] = ("0x%08X" % end_va) if end_va else None
            entry["body_size"] = len(body)
            edges = []
            for i in range(len(body) - 5):
                if body[i] in (0xE8, 0xE9):
                    rel = struct.unpack_from("<i", body, i + 1)[0]
                    t = fs + i + 5 + rel
                    edges.append({"op": "E8" if body[i] == 0xE8 else "E9",
                                  "site_va": "0x%08X" % (fs + i),
                                  "target": "0x%08X" % t})
            entry["call_edges"] = edges
            entry["hexdump"] = hexdump(pe, fs, min(len(body) + 32, 0x3000))
            # census who calls THIS function
            entry["callers_of_this"] = calls_all(pe, fs)
        callers.append(entry)
    m["derived_ctor_callers"] = callers

    # hash-map ctor decode dump
    m["hex_hashmap_ctor_FUN_00854C00"] = hexdump(pe, 0x00854C00, 0x100)
    # insert hunt: region after find
    m["hex_region_00971C00_00972600"] = hexdump(pe, 0x00971C00, 0xA00)
    # writer target of FUN_00845F70 (approx 0x005275E0) — find exact start
    wt = find_func_start(pe, 0x005275E6)
    m["writer_target_func_start"] = ("0x%08X" % wt) if wt else None
    if wt:
        m["hex_writer_target"] = hexdump(pe, wt, 0x200)

    with open(os.path.join(OUT, "T2B_DERIVED_INSERT_HUNT.json"), "w") as f:
        json.dump(res, f, indent=2)

    print("T2b done.")
    print("  derived rtti:", m["derived_vtable_rtti"].get("td_name"))
    print("  derived vtable imm32 hits:", len(hits))
    print("  raw calls to derived ctor:", len(m["census_raw_calls_to_derived_ctor"]))
    for e in callers:
        print("    site %s -> func %s size=%s callers=%d" % (
            e["call_site"], e.get("func_start"), e.get("body_size"),
            len(e.get("callers_of_this", []))))
    print("  writer_target_func_start:", m["writer_target_func_start"])

if __name__ == "__main__":
    main()
