# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 — TASK 1: map VALUE CLASS.
# (a) value ctor candidate FUN_0085B1B0 (vtable write 0x00A91E4C seen in
#     PKG_A region dump F2_CTX3_FUN_0085B190.txt) — full body bytes;
# (b) class identity via vtable -> COL -> TypeDescriptor (TD method, PKG_A);
# (c) ctor fields + caller census (raw E8/E9; Ghidra isCall cross-check in GH1);
# (d) vtable slot-0 uniqueness scan over all sections (other types sharing slot-0).
# STATIC-ONLY. Every VA -> pe_core mapping -> bytes.

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

VALUE_CTOR = 0x0085B1B0
VALUE_VTABLE = 0x00A91E4C
SUBCTOR = 0x007345BD

def calls_all(pe, target_va):
    """Direct CALL rel32 (E8) and JMP rel32 (E9) sites in .text targeting target_va."""
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
    """MSVC RTTI: [vtable-4] = COL; COL+0xC = TypeDescriptor ptr; TD+8 = name."""
    res = {"vtable_va": "0x%08X" % vtable_va}
    col = pe.read_va32(vtable_va - 4)
    res["col_ptr"] = "0x%08X" % col if col else None
    if col is None or pe.section_of(col) is None:
        res["error"] = "col not in sections"
        return res
    res["col_raw16"] = (pe.read_va(col, 16) or b"").hex()
    td = pe.read_va32(col + 0xC)
    res["td_ptr"] = "0x%08X" % td if td else None
    if td is None or pe.section_of(td) is None:
        res["error"] = "td not in sections"
        return res
    td_raw = pe.read_va(td, 0x60) or b""
    res["td_raw_0x60"] = td_raw.hex()
    name_off = 8
    end = td_raw.find(b"\x00", name_off)
    name_bytes = td_raw[name_off:end] if end > 0 else b""
    res["td_name_raw"] = name_bytes.hex()
    try:
        res["td_name"] = name_bytes.decode("ascii", "replace")
    except Exception:
        res["td_name"] = None
    return res

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T1_value_class", "measured": {}, "errors": []}

    # --- (a) full ctor body bytes ---
    m = res["measured"]
    m["value_ctor_FUN_0085B1B0_hexdump"] = hexdump(pe, VALUE_CTOR, 0xC0)
    m["subctor_FUN_007345BD_hexdump"] = hexdump(pe, SUBCTOR, 0x80)
    m["lock_helper_FUN_0085B190_hexdump"] = hexdump(pe, 0x0085B190, 0x20)
    m["lock_helper_FUN_0085B1A0_hexdump"] = hexdump(pe, 0x0085B1A0, 0x20)
    m["lock_target_FUN_00413440_hexdump"] = hexdump(pe, 0x00413440, 0x20)
    m["cs_init_FUN_004134F0_hexdump"] = hexdump(pe, 0x004134F0, 0x30)

    # --- (b) RTTI of value vtable ---
    m["value_vtable_rtti"] = rtti_name(pe, VALUE_VTABLE)

    # vtable slots 0..15
    slots = []
    for i in range(16):
        v = pe.read_va32(VALUE_VTABLE + 4 * i)
        slots.append({"slot": i, "addr": "0x%08X" % (VALUE_VTABLE + 4 * i),
                      "target": ("0x%08X" % v) if v else None,
                      "section": pe.section_of(v) if v else None})
    m["value_vtable_slots"] = slots
    m["value_vtable_raw"] = (pe.read_va(VALUE_VTABLE, 64) or b"").hex()

    # --- census: imm32 vtable in .text (vtable writes) ---
    hits = pe.scan_text_imm32(VALUE_VTABLE)
    imm_ctx = []
    for off in hits:
        va = pe.text_off_to_va(off)
        ctx_before = (pe.read_va(va - 10, 10) or b"").hex()
        ctx_after = (pe.read_va(va + 4, 6) or b"").hex()
        imm_ctx.append({"text_off": off, "va": "0x%08X" % va,
                        "bytes_before10": ctx_before, "bytes_after6": ctx_after})
    m["census_imm32_value_vtable_in_text"] = {
        "count": len(hits), "hits": imm_ctx}

    # --- (c) ctor caller census (raw) ---
    m["census_raw_calls_to_value_ctor"] = calls_all(pe, VALUE_CTOR)
    m["census_raw_calls_to_subctor_FUN_007345BD"] = calls_all(pe, SUBCTOR)

    # --- (d) slot-0 uniqueness: scan ALL sections for DWORD == slot0 target;
    #     validate candidate vtable bases by RTTI chain (COL -> TD -> name).
    slot0 = pe.read_va32(VALUE_VTABLE)
    m["value_vtable_slot0_target"] = "0x%08X" % slot0
    same_slot0 = []
    for s in pe.sections:
        raw = pe.data[s["rptr"]:s["rptr"] + s["rsize"]]
        pat = struct.pack("<I", slot0)
        start = 0
        while True:
            i = raw.find(pat, start)
            if i < 0:
                break
            va = s["va_start"] + i
            start = i + 1
            if va == VALUE_VTABLE:
                same_slot0.append({"va": "0x%08X" % va, "kind": "VALUE_VTABLE_ITSELF"})
                continue
            # candidate vtable base at va: check RTTI at va-4
            r = rtti_name(pe, va)
            entry = {"va": "0x%08X" % va, "section": s["name"]}
            if r.get("td_name"):
                entry["kind"] = "VTABLE_WITH_RTTI"
                entry["rtti"] = r
            else:
                entry["kind"] = "DWORD_HIT_NO_RTTI"
                entry["note"] = "not a vtable base (no COL/TD chain)"
            same_slot0.append(entry)
    m["census_slot0_same_target_all_sections"] = same_slot0

    # --- context: the whole ctor neighborhood region dump for offline reading
    with open(os.path.join(OUT, "T1_REGION_0085B100_0085B900.txt"), "w") as f:
        f.write(hexdump(pe, 0x0085B100, 0x800))

    with open(os.path.join(OUT, "T1_VALUE_CLASS.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("T1 done: rtti=%s" % m["value_vtable_rtti"].get("td_name"))
    print("  imm32 vtable hits in .text: %d" % len(hits))
    print("  raw calls to ctor: %d" % len(m["census_raw_calls_to_value_ctor"]))
    print("  raw calls to subctor: %d" % len(m["census_raw_calls_to_subctor_FUN_007345BD"]))
    print("  slot0 same-target hits: %d" % len(same_slot0))

if __name__ == "__main__":
    main()
