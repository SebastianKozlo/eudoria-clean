# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S6 FOURCC class-id scan (offline)
# The ArkObjectClassImpl<> template args are 4-char codes (EOEC/EODN/EODO/EOCP/FNMJ...).
# Scan .text/.rdata/.data for those 4-char codes as LE/BE dwords -> class-id registry
# tables / factory registrations. Raw scan = candidates; validated in Ghidra next.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [
    (".text", 0x00401000, 0x00A75000, 4096, 6766592),
    (".rdata", 0x00A75000, 0x00B6C000, 6770688, 1011712),
    (".data", 0x00B6C000, 0x00BA96E4, 7782400, 212992),
]

def file_to_va(off):
    for n, vs, ve, rp, rs in SECS:
        if rp <= off < rp + rs:
            return vs + (off - rp)
    return None

# class-ids from RTTI mangling (RUN 3 S1 census + this run)
CODES = {
    "ArkRealWorldItem": "EOEC",
    "ArkRealWorldProvider": "EOEB",
    "ArkInteractiveWorldObject": "FNMJ",
    "ArkParameterTransformation": "EODN",
    "ArkParameterContainer": "EODO",
    "ArkParameterSetObject": "EOCP",
    "ArkParameterServerLocal": "EODF",
    "ArkParameterServerGlobal": "EOEA",
    "ArkParameterCommon": "EOCG",
    "ArkParameterCreature": "EOCL",
    "ArkParameterAction": "EOCB",
    "ArkParameterBlueprint": "EOCH",
    "ArkParameterTool": "EODB",
    "ArkParameterMakeup": "EOEL",
    "ArkParameterScreen": "EOEF",
    "ArkParameterClothes": "EOCJ",
}

def main():
    data = open(EXE, "rb").read()
    out = {}
    for cls, code in CODES.items():
        le = struct.pack("<4s", code.encode("ascii"))
        be = struct.pack(">4s", code.encode("ascii"))
        rec = {}
        for tag, pat in [("LE_dword", le), ("BE_dword", be)]:
            hits = []
            for n, vs, ve, rp, rs in SECS:
                off = rp
                while True:
                    off = data.find(pat, off, rp + rs)
                    if off < 0:
                        break
                    hits.append({"va": "0x%08X" % file_to_va(off), "sec": n,
                                 "file_offset": off,
                                 "context_hex": data[max(0, off-8):off+12].hex()})
                    off += 1
            rec[tag] = hits
        out[cls] = rec

    # round-trip check
    rt_ok = all(struct.unpack("<4s", struct.pack("<4s", c.encode()))[0] == c.encode()
                for c in CODES.values())

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S6_fourcc_classid_scan_raw",
        "note": ("Raw scan of 4-char class-id codes as LE/BE dwords. Candidates only; "
                 "Ghidra must validate the containing instruction/table."),
        "roundtrip_ok": rt_ok,
        "summary": {cls: {"LE": len(r["LE_dword"]), "BE": len(r["BE_dword"])}
                    for cls, r in out.items()},
        "hits": out,
    }
    with open(os.path.join(OUT, "S6_FOURCC_CLASSID_SCAN.json"), "w") as f:
        json.dump(result, f, indent=2)
    for cls, s in result["summary"].items():
        print("%-32s LE=%d BE=%d" % (cls, s["LE"], s["BE"]))

if __name__ == "__main__":
    main()
