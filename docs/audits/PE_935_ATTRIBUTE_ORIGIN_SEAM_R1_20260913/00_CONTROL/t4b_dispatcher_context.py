# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - T4b: dispatcher callers + drive-C
# vtable RTTI + FUN_00514EF0 context. STATIC-ONLY.

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE

RUN_ID = "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"


def rtti_name(pe, vtable_va):
    res = {"vtable_va": "0x%08X" % vtable_va}
    col = pe.read_va32(vtable_va - 4)
    res["col_ptr"] = ("0x%08X" % col) if col else None
    if col is None or pe.section_of(col) is None:
        res["error"] = "col not in sections"
        return res
    td = pe.read_va32(col + 0xC)
    if td is None or pe.section_of(td) is None:
        res["error"] = "td not in sections"
        return res
    td_raw = pe.read_va(td, 0x60) or b""
    end = td_raw.find(b"\x00", 8)
    res["td_name"] = td_raw[8:end].decode("ascii", "replace")
    return res


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


def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T4b_dispatcher_context", "measured": {}, "errors": []}
    m = res["measured"]

    # the vtable containing FUN_00514EF0 (drive C) - find its base + RTTI:
    # scan .rdata backwards from 0x00A7D778 for a plausible vtable base with COL
    target_slot_va = 0x00A7D778
    candidates = []
    for back in range(0, 0x100, 4):
        vt = target_slot_va - back
        r = rtti_name(pe, vt)
        if r.get("td_name") and ".?AV" in r["td_name"]:
            candidates.append({"vtable_base": "0x%08X" % vt, "slot_index": back // 4,
                               "rtti": r})
    m["driveC_vtable_rtti_candidates"] = candidates

    # raw callers
    for name, va in [("dispatcher_FUN_004B18D0", 0x004B18D0),
                    ("dispatcher2_FUN_004B2950", 0x004B2950),
                    ("registryinit_FUN_00452490", 0x00452490),
                    ("sender_FUN_005B6890", 0x005B6890)]:
        m["raw_calls_" + name] = calls_all(pe, va)
        # imm32 census (dispatch table entries are data refs)
        hits = []
        for s in pe.sections:
            raw = pe.data[s["rptr"]:s["rptr"] + s["rsize"]]
            pat = struct.pack("<I", va)
            start = 0
            while True:
                i = raw.find(pat, start)
                if i < 0:
                    break
                hits.append({"section": s["name"],
                             "va": "0x%08X" % (s["va_start"] + i)})
                start = i + 1
        m["imm32_" + name] = hits

    with open(os.path.join(OUT, "T4B_DISPATCHER_CONTEXT.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("T4b done")
    for c in candidates:
        print("  vtable 0x%s slot %d: %s" % (c["vtable_base"][2:], c["slot_index"], c["rtti"]["td_name"]))
    for name in ["dispatcher_FUN_004B18D0", "dispatcher2_FUN_004B2950",
                 "registryinit_FUN_00452490", "sender_FUN_005B6890"]:
        print("  %s: raw=%d imm32=%d" % (name, len(m["raw_calls_" + name]), len(m["imm32_" + name])))
        for h in m["imm32_" + name]:
            print("     [%s] %s" % (h["section"], h["va"]))

if __name__ == "__main__":
    main()
