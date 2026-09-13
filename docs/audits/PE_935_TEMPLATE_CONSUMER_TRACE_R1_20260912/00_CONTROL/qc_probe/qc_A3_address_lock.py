#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe A3 — final resolution of the 3 remaining sequences (executor dump bytes
vs raw binary): avatar getter call, lookup head, ctor FLDZ/FSTP with interleaved
MOV/XOR. Plus avatar {0x66,A} pair build instruction.
READ-ONLY. Writes: 00_CONTROL\qc_probe\qc_A3_address_lock_result.json
"""
import hashlib
import json
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\qc_A3_address_lock_result.json"
EXPECTED_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

with open(EXE, "rb") as f:
    blob = f.read()
res = {"probe": "qc_A3_address_lock", "checks": [], "errors": []}
if hashlib.sha256(blob).hexdigest().upper() != EXPECTED_SHA:
    res["errors"].append("EXE SHA mismatch")
    sys.exit(2)

e_lfanew = struct.unpack_from("<I", blob, 0x3C)[0]
coff = e_lfanew + 4
num_sections = struct.unpack_from("<H", blob, coff + 2)[0]
size_opt = struct.unpack_from("<H", blob, coff + 16)[0]
opt = coff + 20
image_base = struct.unpack_from("<I", blob, opt + 28)[0]
sec_tab = opt + size_opt
sections = []
for i in range(num_sections):
    off = sec_tab + 40 * i
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", blob, off + 8)
    sections.append((vsize, vaddr, rsize, rptr))


def va_to_off(va):
    rva = va - image_base
    for (vsize, vaddr, rsize, rptr) in sections:
        if vaddr <= rva < vaddr + vsize and (rva - vaddr) < rsize:
            return rptr + (rva - vaddr)
    return None


def check(label, va, expected_hex):
    exp = expected_hex.split()
    off = va_to_off(va)
    raw = blob[off:off + len(exp)] if off is not None else None
    ok = raw is not None and all(e == "??" or raw[k] == int(e, 16) for k, e in enumerate(exp))
    entry = {"label": label, "va": "%08X" % va, "expected": expected_hex,
              "got": raw.hex() if raw is not None else None, "result": "PASS" if ok else "FAIL"}
    if not ok:
        res["errors"].append("mismatch %s @%08X" % (label, va))
    res["checks"].append(entry)
    print("[%s] %-52s VA %08X" % (entry["result"], label, va))
    return entry


# avatar factory: pair build MOV [ESP+0x10],0x66 then CALL getter A then pair-insert
check("avatar MOV [ESP+0x10],0x66 @0x0043EB9D", 0x0043EB9D, "c7 44 24 10 66 00 00 00")
check("avatar CALL FUN_007ce1e0 @0x0043EBA5", 0x0043EBA5, "e8 36 f6 38 00")
# lookup head (PUSH ECX; PUSH ESI; MOV ESI,ECX)
check("lookup head @0x0072F580", 0x0072F580, "51 56 8b f1")
# ctor FLDZ; MOV EAX,ECX; XOR ECX,ECX; FSTP [EAX+0x10]
check("ctor FLDZ/.../FSTP[+0x10] @0x00730700", 0x00730700, "d9 ee 8b c1 33 c9 d9 58 10")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
n_pass = sum(1 for c in res["checks"] if c["result"] == "PASS")
n_fail = sum(1 for c in res["checks"] if c["result"] == "FAIL")
print("\n== A3 SUMMARY: %d PASS, %d FAIL ==" % (n_pass, n_fail))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if n_fail else 0)
