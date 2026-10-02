#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3 routing census, part 1: raw byte scan of the pinned Entropia.exe.
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002. Pure reader.

Scans (own PE section parser, no prior-tool code):
  - imm32 LE 0x00004E22 (=20002)  bytes 22 4E 00 00   [encoding verified in-run: 20002==0x4E22]
  - ASCII "20002"
  - ASCII "$0EOCC@" (MSVC mangling of template integer arg 20002; nibbles 4,E,2,2 -> E,O,C,C)
  - ASCII "$0EOCG@" (mangling of 20006 - calibration of the encoding rule in THIS binary)
  - all "$0EOC?" hits (family census)
Outputs 01_RAW\ROUTING_CENSUS_RAW.json
"""
import struct
import json
import hashlib

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\ROUTING_CENSUS_RAW.json"

with open(EXE, "rb") as f:
    data = f.read()
sha = hashlib.sha256(data).hexdigest().upper()

# ---- own PE32 section parser ----
assert data[:2] == b"MZ"
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
assert data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00"
machine, num_sections = struct.unpack_from("<HH", data, e_lfanew + 4)
opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
sec_off = e_lfanew + 24 + opt_size
sections = []
for i in range(num_sections):
    off = sec_off + i * 40
    name = data[off:off + 8].rstrip(b"\x00").decode("latin-1")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<4I", data, off + 8)
    sections.append({"name": name, "vsize": vsize, "vaddr": vaddr, "rawsize": rawsize, "rawptr": rawptr})

def foff_to_va(fo):
    for s in sections:
        if s["rawptr"] <= fo < s["rawptr"] + s["rawsize"]:
            return image_base + s["vaddr"] + (fo - s["rawptr"]), s["name"]
    return None, None

def find_all(pat):
    out = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0:
            break
        va, sec = foff_to_va(i)
        out.append({"file_offset": i, "va": ("0x%X" % va) if va else None, "section": sec,
                    "context_hex": data[max(0, i - 16):i + len(pat) + 16].hex()})
        start = i + 1
    return out

census = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "generator": "03_SCRIPTS/s3_exe_census.py",
    "exe_path": EXE,
    "exe_sha256": sha,
    "exe_size": len(data),
    "image_base": "0x%X" % image_base,
    "machine": "0x%X" % machine,
    "sections": sections,
    "encoding_verification": {
        "decimal_20002_to_hex": "0x4E22",
        "check": "0x4E22 == 4*4096 + 14*256 + 2*16 + 2 == 16384+3584+32+2 == 20002: TRUE",
        "u32_LE_bytes_of_0x00004E22": "22 4E 00 00",
        "msvc_mangling_rule": "template integer arg encoded as '$0' + nibbles a..p (a=0..p=15) most-significant-first + '@'",
        "mangling_of_20002": "nibbles 4,E,2,2 -> 'e','o','c','c' -> $0EOCC@",
        "mangling_of_20006_calibration": "nibbles 4,E,2,6 -> 'e','o','c','g' -> $0EOCG@",
        "vfs_payload_cross_check": "20002.vfs record payload u32@+0 == LE bytes 22 4E 00 00 == 20002 (measured S1)",
    },
    "scans": {},
}

hits_imm = find_all(b"\x22\x4e\x00\x00")
hits_str = find_all(b"20002")
hits_m20002 = find_all(b"$0EOCC@")
hits_m20006 = find_all(b"$0EOCG@")
# family census: all $0EOC? mangles
fam = {}
for m in (b"$0EOCA@", b"$0EOCB@", b"$0EOCC@", b"$0EOCD@", b"$0EOCE@", b"$0EOCF@",
          b"$0EOCG@", b"$0EOCH@", b"$0EOCI@", b"$0EOCJ@", b"$0EOCK@", b"$0EOCL@",
          b"$0EOCM@", b"$0EOCN@", b"$0EOCO@", b"$0EOCP@"):
    h = find_all(m)
    if h:
        fam[m.decode()] = h

census["scans"] = {
    "imm32_0x00004E22_LE_bytes_224E0000": {"count": len(hits_imm), "hits": hits_imm},
    "ascii_20002": {"count": len(hits_str), "hits": hits_str},
    "mangle_20002_$0EOCC@": {"count": len(hits_m20002), "hits": hits_m20002},
    "mangle_20006_$0EOCG@_calibration": {"count": len(hits_m20006), "hits": hits_m20006},
    "mangle_family_$0EOCx_count": {k: len(v) for k, v in fam.items()},
}

with open(OUT, "w") as f:
    json.dump(census, f, indent=2)

print("imm32 0x4E22 hits:", len(hits_imm))
for h in hits_imm:
    print("  fo=0x%X va=%s sec=%s ctx=%s" % (h["file_offset"], h["va"], h["section"], h["context_hex"]))
print("ascii '20002' hits:", len(hits_str))
for h in hits_str:
    print("  fo=0x%X va=%s sec=%s ctx=%s" % (h["file_offset"], h["va"], h["section"], h["context_hex"]))
print("mangle $0EOCC@ hits:", len(hits_m20002))
for h in hits_m20002:
    print("  fo=0x%X va=%s sec=%s ctx=%s" % (h["file_offset"], h["va"], h["section"], h["context_hex"]))
print("mangle $0EOCG@ (20006 calib) hits:", len(hits_m20006))
for h in hits_m20006[:5]:
    print("  fo=0x%X va=%s sec=%s ctx=%s" % (h["file_offset"], h["va"], h["section"], h["context_hex"]))
print("family:", {k: len(v) for k, v in fam.items()})
