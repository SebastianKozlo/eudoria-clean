# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S3 ROUND-TRIP ID + 4508 PATTERN RAW BYTES
# Control required by contract: round-trip ID (pack->unpack) BEFORE pattern scans.
# Then: raw bytes at the 3 pattern VAs (0x0053270C, 0x00532769, 0x0083427E)
# + full .text imm32 scan for 4508 (0x119C) and 296445 (0x485FD) context dump.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def va_to_file(va):
    if 0x00401000 <= va < 0x00A75000:
        return 4096 + (va - 0x00401000)
    if 0x00A75000 <= va < 0x00B6C000:
        return 6770688 + (va - 0x00A75000)
    if 0x00B6C000 <= va < 0x00BA96E4:
        return 7782400 + (va - 0x00B6C000)
    return None

def main():
    data = open(EXE, "rb").read()

    # --- ROUND-TRIP (pack -> unpack) ---
    rt = {}
    for label, val in [("template_4508", 4508), ("model_A_296445", 296445),
                       ("sibling_4752", 4752), ("sibling_2249", 2249),
                       ("avatar_11769", 11769), ("avatar_11655", 11655),
                       ("avatar_11656", 11656), ("avatar_11657", 11657)]:
        packed_le = struct.pack("<I", val)
        packed_be = struct.pack(">I", val)
        unpacked_le = struct.unpack("<I", packed_le)[0]
        unpacked_be = struct.unpack(">I", packed_be)[0]
        ok = (unpacked_le == val and unpacked_be == val)
        rt[label] = {"value": val, "hex": "0x%08X" % val,
                     "le_bytes": " ".join("%02x" % b for b in packed_le),
                     "be_bytes": " ".join("%02x" % b for b in packed_be),
                     "roundtrip_ok": ok}
        assert ok, "round-trip failed for %s" % label

    # --- RAW BYTES at the 3 pattern VAs ---
    patterns = {}
    windows = {}
    for va in [0x0053270C, 0x00532769, 0x0083427E]:
        off = va_to_file(va)
        raw = data[off:off+16]
        patterns["0x%08X" % va] = {
            "file_offset": off,
            "bytes_at_va_hex": " ".join("%02x" % b for b in raw),
            "contains_4508_le_at_va": raw[:4] == struct.pack("<I", 4508),
        }
        w = data[off-32:off+48]
        windows["0x%08X" % va] = " ".join("%02x" % b for b in w)

    # --- FULL .text imm32 scan for 4508 LE + BE context (cheap, controlled) ---
    # scan aligned+unaligned 4-byte windows in .text for 9C 11 00 00 (LE) or 00 00 11 9C (BE)
    text_off, text_len = 4096, 6766592
    le_pat = struct.pack("<I", 4508)
    be_pat = struct.pack(">I", 4508)
    hits_le, hits_be = [], []
    i = text_off
    while True:
        i = data.find(le_pat, i, text_off + text_len)
        if i < 0: break
        hits_le.append(0x00401000 + (i - text_off))
        i += 1
    # separate loop for BE
    i = text_off
    while True:
        i = data.find(be_pat, i, text_off + text_len)
        if i < 0: break
        hits_be.append(0x00401000 + (i - text_off))
        i += 1
    # 296445 LE scan too (the A value)
    a_pat = struct.pack("<I", 296445)
    hits_a = []
    i = text_off
    while True:
        i = data.find(a_pat, i, text_off + text_len)
        if i < 0: break
        hits_a.append(0x00401000 + (i - text_off))
        i += 1

    out = {
        "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
        "stage": "S3_roundtrip_and_4508_raw",
        "roundtrip": rt,
        "pattern_vas": patterns,
        "pattern_windows_va_minus32_plus48": windows,
        "text_scan": {
            "4508_le_hits": ["0x%08X" % h for h in hits_le],
            "4508_be_hits": ["0x%08X" % h for h in hits_be],
            "296445_le_hits": ["0x%08X" % h for h in hits_a],
        },
    }
    with open(os.path.join(OUT, "S3_ROUNDTRIP_4508.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("S3_DONE roundtrip=OK(8/8)")
    print("4508 LE hits in .text:", len(hits_le), ["0x%08X" % h for h in hits_le])
    print("4508 BE hits in .text:", len(hits_be), ["0x%08X" % h for h in hits_be])
    print("296445 LE hits in .text:", len(hits_a), ["0x%08X" % h for h in hits_a])
    for k, v in patterns.items():
        print(k, v["bytes_at_va_hex"], "is_4508_at_va:", v["contains_4508_le_at_va"])

if __name__ == "__main__":
    main()
