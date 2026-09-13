# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S9 template-field getter scan (offline)
# Template object layout (RUN-3): +0x04=B, +0x08=A, +0x0C=C, +0x10=D f32.
# Getters are 3-byte thiscall stubs: mov eax,[ecx+off]; ret  = 8B 41 <off> C3
# Float getter: fld dword [ecx+off]; ret              = D9 41 <off> C3
# Find ALL such stubs for offsets 0x04/0x08/0x0C/0x10 (and D9 41 10 C3 for f32-D),
# then Ghidra validates + census of callers.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [(".text", 0x00401000, 0x00A75000, 4096, 6766592)]

def file_to_va(off):
    for n, vs, ve, rp, rs in SECS:
        if rp <= off < rp + rs:
            return vs + (off - rp)
    return None

def main():
    data = open(EXE, "rb").read()
    rp, rs = SECS[0][3], SECS[0][4]
    out = {}
    # round-trip: construct the stub bytes, decode back
    rt = []
    for kind, tmpl in [("mov_stub", bytes([0x8B, 0x41, 0x10, 0xC3])),
                       ("fld_stub", bytes([0xD9, 0x41, 0x10, 0xC3]))]:
        b = tmpl
        assert struct.unpack("<4s", struct.pack("<4s", b))[0] == b
        rt.append(b.hex())
    out["_roundtrip"] = rt

    results = {}
    for off in (0x04, 0x08, 0x0C, 0x10):
        for kind, prefix in [("mov", bytes([0x8B, 0x41])), ("fld", bytes([0xD9, 0x41]))]:
            pat = prefix + bytes([off, 0xC3])
            hits = []
            start = rp
            while True:
                start = data.find(pat, start, rp + rs)
                if start < 0:
                    break
                hits.append({"va": "0x%08X" % file_to_va(start), "file_offset": start,
                             "bytes": pat.hex()})
                start += 1
            results["%s_getter_+0x%02X" % (kind, off)] = hits

    with open(os.path.join(OUT, "S9_GETTER_STUB_SCAN.json"), "w") as f:
        json.dump({"run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
                   "stage": "S9_getter_stub_scan_raw",
                   "note": ("Raw scan for 4-byte getter stubs. Every hit = candidate "
                            "function entry; Ghidra confirms function boundaries + callers."),
                   "hits": results}, f, indent=2)
    for k, v in results.items():
        print("%-24s %d  %s" % (k, len(v), " ".join(h["va"] for h in v)))

if __name__ == "__main__":
    main()
