# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - T4: message-handler dispatch proof.
# Scan whole binary for imm32/dword values == drive-handler VAs (FUN_005B72C0,
# FUN_0058DB50, FUN_00514EF0, FUN_004C47F0-caller handlers) to find the
# dispatch-table registrations. Also imm32 of 0xB9/0x23A/0x3DC8 contexts.
# STATIC-ONLY.

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

HANDLERS = {
    "FUN_005B72C0": 0x005B72C0,
    "FUN_0058DB50": 0x0058DB50,
    "FUN_00514EF0": 0x00514EF0,
    "FUN_004C47F0": 0x004C47F0,
    "FUN_00567C50": 0x00567C50,
    "FUN_00567770": 0x00567770,
    "FUN_004574F0": 0x004574F0,
    "FUN_004B0AB0": 0x004B0AB0,
    "FUN_004B1670": 0x004B1670,
    "FUN_004B1C70": 0x004B1C70,
}

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T4_handler_dispatch", "measured": {}, "errors": []}
    m = res["measured"]

    for name, va in sorted(HANDLERS.items()):
        hits = []
        for s in pe.sections:
            raw = pe.data[s["rptr"]:s["rptr"] + s["rsize"]]
            pat = struct.pack("<I", va)
            start = 0
            while True:
                i = raw.find(pat, start)
                if i < 0:
                    break
                hit_va = s["va_start"] + i
                start = i + 1
                hits.append({"section": s["name"], "va": "0x%08X" % hit_va,
                             "ctx_before8": (pe.read_va(hit_va - 8, 8) or b"").hex(),
                             "ctx_after8": (pe.read_va(hit_va + 4, 8) or b"").hex()})
        m["imm32_census_" + name] = {"target_va": "0x%08X" % va, "count": len(hits), "hits": hits}

    # also scan for E8/E9 call sites of the three drives (raw)
    def calls_all(target_va):
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

    for name, va in sorted(HANDLERS.items()):
        m["raw_calls_" + name] = calls_all(va)

    with open(os.path.join(OUT, "T4_HANDLER_DISPATCH.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("T4 done")
    for name in sorted(HANDLERS):
        c = m["imm32_census_" + name]
        r = m["raw_calls_" + name]
        print("  %-12s imm32=%d rawcalls=%d" % (name, c["count"], len(r)))
        for h in c["hits"]:
            print("      [%s] %s before=%s after=%s" % (h["section"], h["va"], h["ctx_before8"], h["ctx_after8"]))
        for cc in r:
            print("      call %s @%s" % (cc["op"], cc["site_va"]))

if __name__ == "__main__":
    main()
