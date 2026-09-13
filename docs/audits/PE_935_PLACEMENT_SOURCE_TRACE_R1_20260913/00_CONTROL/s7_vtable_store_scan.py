# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S7 VTABLE-STORE ctor scan (offline)
# Find the ctors by scanning .text for stores of the vtable pointer constants
# (the `MOV [reg], vtable` instruction embeds the vtable VA as imm32):
#   ArkParameterContainer   0x00A8784C
#   ArkParameterTransformation 0x00A877DC
#   ArkParameterSetObject   0x00A87260
#   ArkRealWorldItem       0x00A873D8
#   ArkRealWorldProvider   0x00A878F4
#   ArkInteractiveWorldObject 0x00A86C68
#   ArkObject              0x00A86B48
#   ArkPacketDecoder       0x00A91A6C
#   ArkStaticPacket        0x00A91A44
#   ArkCommunicator         0x00A91A4C
#   ArkClientPacketExecutor 0x00A7C1FC
#   ArkPortalResourceItem   0x00A91D04
#   ArkPortalCell           0x00A91CF8
#   ArkObjectService        0x00A7BF9C
#   ArkObjectCommander      0x00A7BFCC
#   ArkClientObjectManagerImpl 0x00A7C028 / 0x00A7C0A0
# Validated in Ghidra (instruction + function).

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [
    (".text", 0x00401000, 0x00A75000, 4096, 6766592),
]

def file_to_va(off):
    for n, vs, ve, rp, rs in SECS:
        if rp <= off < rp + rs:
            return vs + (off - rp)
    return None

VTABLES = {
    "ArkParameterContainer": 0x00A8784C,
    "ArkParameterTransformation": 0x00A877DC,
    "ArkParameterSetObject": 0x00A87260,
    "ArkParameterCommon": 0x00A86F2C,
    "ArkRealWorldItem": 0x00A873D8,
    "ArkRealWorldProvider": 0x00A878F4,
    "ArkInteractiveWorldObject": 0x00A86C68,
    "ArkObject": 0x00A86B48,
    "ArkObjectClass": 0x00A86850,
    "ArkPacketDecoder": 0x00A91A6C,
    "ArkStaticPacket": 0x00A91A44,
    "ArkPacket": 0x00A91A30,
    "ArkCommunicator": 0x00A91A4C,
    "ArkClientPacketExecutor": 0x00A7C1FC,
    "ArkPortalResourceItem": 0x00A91D04,
    "ArkPortalCell": 0x00A91CF8,
    "ArkPortalCellGraph": 0x00A91CB4,
    "ArkObjectService": 0x00A7BF9C,
    "ArkObjectCommander": 0x00A7BFCC,
    "ArkClientObjectManagerImpl_v1": 0x00A7C028,
    "ArkClientObjectManagerImpl_v2": 0x00A7C0A0,
}

def main():
    data = open(EXE, "rb").read()
    out = {}
    for cls, vt in VTABLES.items():
        pat = struct.pack("<I", vt)
        hits = []
        off = SECS[0][3]
        while True:
            off = data.find(pat, off, SECS[0][3] + SECS[0][4])
            if off < 0:
                break
            hits.append({
                "va": "0x%08X" % file_to_va(off),
                "file_offset": off,
                "window_hex": data[max(0, off-8):off+12].hex(),
            })
            off += 1
        out[cls] = hits

    rt_ok = True
    for cls, vt in VTABLES.items():
        if struct.unpack("<I", struct.pack("<I", vt))[0] != vt:
            rt_ok = False

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S7_vtable_store_scan_raw",
        "note": ("Raw scan of .text for the vtable VA as imm32 (ctor vtable stores + any "
                 "direct references). Candidates; Ghidra validates instruction+function."),
        "roundtrip_ok": rt_ok,
        "hits": out,
    }
    with open(os.path.join(OUT, "S7_VTABLE_STORE_SCAN.json"), "w") as f:
        json.dump(result, f, indent=2)
    for cls, hits in out.items():
        print("%-32s hits=%d %s" % (cls, len(hits), " ".join(h["va"] for h in hits[:8])))

if __name__ == "__main__":
    main()
