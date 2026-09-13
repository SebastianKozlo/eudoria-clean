# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S5 IMMEDIATE SCAN (offline, raw bytes)
# STATIC-ONLY. Scans .text for little-endian dword occurrences of the placement
# attribute IDs (0x6A4/0x6A5/0x6A8/0x6A9), the param-set constellation (0x4E26,
# 20001..20043, 24007), and record IDs seen in FUN_00567770 (0x1bdc, 0x1bde, 0x85, 0x86).
# Raw scan = candidates ONLY; every hit is validated in Ghidra (instruction containing
# the byte offset) before any claim. Also scans .rdata/.data for the same values as
# reference tables (context, not instruction claims).
# Round-trip check: pack->unpack of all scanned values BEFORE the scan.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

IMAGE_BASE = 0x00400000
SECS = [
    (".text", 0x00401000, 0x00A75000, 4096, 6766592),
    (".rdata", 0x00A75000, 0x00B6C000, 6770688, 1011712),
    (".data", 0x00B6C000, 0x00BA96E4, 7782400, 212992),
]

VALUES = {
    "attr_pos_0x6A4": 0x6A4,
    "attr_pos_0x6A5": 0x6A5,
    "attr_pos_0x6A8": 0x6A8,
    "attr_pos_0x6A9": 0x6A9,
    "attr_0x6A6_0x6A7_neighbours": None,  # probed below as a pair
    "paramset_0x4E26_20006": 0x4E26,
    "paramset_20006_dec": 20006,
    "vfs_20001": 20001,
    "vfs_20002": 20002,
    "vfs_20005": 20005,
    "vfs_20007": 20007,
    "vfs_24007": 24007,
    "rec_0x1bdc_7132": 0x1bdc,
    "rec_0x1bde_7134": 0x1bde,
    "small_0x85_133": 0x85,
    "small_0x86_134": 0x86,
    # negative control: a value that should NOT occur as dword in .text
    "negative_0x66AA_never": 0x66AA,
}

def va_to_file(va):
    for n, vs, ve, rp, rs in SECS:
        if vs <= va < ve:
            return rp + (va - vs)
    return None

def file_to_va(off):
    for n, vs, ve, rp, rs in SECS:
        if rp <= off < rp + rs:
            return vs + (off - rp)
    return None

def main():
    data = open(EXE, "rb").read()

    # ROUND-TRIP: pack->unpack of every value (LE), and of the pack/unpack of the
    # float-bit pair used in FUN_00567770 (local_10c[0]=float bits 0x1bdc check)
    rt = {}
    for k, v in VALUES.items():
        if v is None:
            continue
        packed = struct.pack("<I", v)
        unpacked = struct.unpack("<I", packed)[0]
        rt[k] = {"packed_hex": packed.hex(), "roundtrip_ok": (unpacked == v)}
    # float-bit roundtrip: 0x1bdc as denormal float bits -> value -> bits
    fv = struct.unpack("<f", struct.pack("<I", 0x1bdc))[0]
    fb = struct.unpack("<I", struct.pack("<f", fv))[0]
    rt["float_bits_0x1bdc"] = {"float_repr": fv, "bits_back": "0x%08X" % fb,
                               "roundtrip_ok": (fb == 0x1bdc)}
    # 124.941 (template 4508 D field) -> bits
    fd = struct.unpack("<I", struct.pack("<f", 124.941))[0]
    rt["D_4508_124941_bits"] = "0x%08X" % fd
    failed_rt = [k for k, v in rt.items() if isinstance(v, dict) and "roundtrip_ok" in v and not v["roundtrip_ok"]]
    if failed_rt:
        raise SystemExit("ROUNDTRIP FAIL %s" % failed_rt)

    hits = {}
    for k, v in VALUES.items():
        if v is None:
            # neighbour probe: 0x6A6 and 0x6A7 (IDs between the position/rotation attrs)
            sub = {}
            for v2, k2 in [(0x6A6, "attr_0x6A6"), (0x6A7, "attr_0x6A7"), (0x6A3, "attr_0x6A3"),
                           (0x6AA, "attr_0x6AA"), (0x6AB, "attr_0x6AB")]:
                pat = struct.pack("<I", v2)
                lst = []
                for n, vs, ve, rp, rs in SECS:
                    if n != ".text":
                        continue
                    off = rp
                    while True:
                        off = data.find(pat, off, rp + rs)
                        if off < 0:
                            break
                        lst.append({"va": "0x%08X" % file_to_va(off), "sec": n})
                        off += 1
                sub[k2] = lst
            hits["neighbours"] = sub
            continue
        pat = struct.pack("<I", v)
        lst = []
        for n, vs, ve, rp, rs in SECS:
            off = rp
            while True:
                off = data.find(pat, off, rp + rs)
                if off < 0:
                    break
                va = file_to_va(off)
                lst.append({
                    "va": "0x%08X" % va,
                    "sec": n,
                    "file_offset": off,
                    "context_hex": data[max(0, off-8):off+12].hex(),
                })
                off += 1
        hits[k] = lst

    # split .text hits (instruction candidates) from data hits (tables)
    summary = {}
    for k, lst in hits.items():
        if k == "neighbours":
            summary[k] = {k2: len(v2) for k2, v2 in lst.items()}
            continue
        text_n = sum(1 for h in lst if h["sec"] == ".text")
        summary[k] = {"total": len(lst), "text_candidates": text_n,
                      "data_or_rdata": len(lst) - text_n}

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S5_immediate_scan_raw",
        "note": ("Raw byte scan of LE dwords. TEXT hits = instruction candidates ONLY "
                 "(must be validated in Ghidra against the containing instruction). "
                 "DATA/RDATA hits = table references. No claim is made from this file alone."),
        "roundtrip": rt,
        "summary": summary,
        "hits": hits,
    }
    with open(os.path.join(OUT, "S5_IMMEDIATE_SCAN.json"), "w") as f:
        json.dump(result, f, indent=2)

    for k, s in summary.items():
        if k == "neighbours":
            print("neighbours:", s)
            continue
        print("%-28s total=%4d text=%4d data=%d" % (k, s["total"], s["text_candidates"], s["data_or_rdata"]))

if __name__ == "__main__":
    main()
