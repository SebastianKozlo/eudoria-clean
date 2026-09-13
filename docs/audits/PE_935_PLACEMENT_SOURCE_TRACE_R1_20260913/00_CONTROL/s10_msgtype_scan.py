# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S10 message-type 0xB9 producer scan (offline)
# The executor dispatch (FUN_004b18d0) switch handles message types 0xA2..0xC6;
# case 0xB9 drives the placement-record builder chain (FUN_005b72c0).
# Scan .text for LE dwords 0x000000B9 (PUSH 0xb9 = 68 B9 00 00 00; MOV [esp+X],0xb9 =
# C7 xx xx B9 00 00 00) -> producers of message type 185.
# Raw scan = candidates; Ghidra validates instructions.

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

def main():
    data = open(EXE, "rb").read()
    out = {}
    for key, value in [("msg_0xB9_185", 0xB9),
                       ("msg_0xB2_178", 0xB2),
                       ("negative_0x3C9_never", 0x3C9)]:
        pat = struct.pack("<I", value)
        hits = []
        for n, vs, ve, rp, rs in SECS:
            off = rp
            while True:
                off = data.find(pat, off, rp + rs)
                if off < 0:
                    break
                hits.append({
                    "va": "0x%08X" % file_to_va(off), "sec": n,
                    "file_offset": off,
                    "window": data[max(0, off-8):off+12].hex(),
                })
                off += 1
        out[key] = hits
    rt_ok = all(struct.unpack("<I", struct.pack("<I", v))[0] == v for v in (0xB9, 0xB2, 0x3C9))
    with open(os.path.join(OUT, "S10_MSGTYPE_SCAN.json"), "w") as f:
        json.dump({"run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
                   "stage": "S10_msgtype_scan_raw",
                   "roundtrip_ok": rt_ok,
                   "hits": out}, f, indent=2)
    for k, v in out.items():
        print("%-26s total=%d text=%d" % (k, len(v), sum(1 for h in v if h["sec"] == ".text")))

if __name__ == "__main__":
    main()
