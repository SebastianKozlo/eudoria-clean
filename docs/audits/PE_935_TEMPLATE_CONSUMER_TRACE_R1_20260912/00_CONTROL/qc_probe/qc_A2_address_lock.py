#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe A2 (PE-MASTER-AUDITOR, INTERNAL_QC) — supplementary byte checks for
PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912, resolving the 4 unresolved spots
from probe A with the executor's EXACT claimed instruction bytes (from the
dump files), verified against the raw binary.

READ-ONLY on inputs. Writes: 00_CONTROL\qc_probe\qc_A2_address_lock_result.json
"""
import hashlib
import json
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\qc_A2_address_lock_result.json"
EXPECTED_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

with open(EXE, "rb") as f:
    blob = f.read()
res = {"probe": "qc_A2_address_lock", "checks": [], "errors": []}
sha = hashlib.sha256(blob).hexdigest().upper()
res["exe_sha256"] = sha
if sha != EXPECTED_SHA:
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
              "got": raw.hex() if raw is not None else None,
              "result": "PASS" if ok else "FAIL"}
    if not ok:
        res["errors"].append("mismatch %s @%08X" % (label, va))
    res["checks"].append(entry)
    print("[%s] %-52s VA %08X" % (entry["result"], label, va))
    return entry


def count_calls(va_start, nbytes, target):
    off = va_to_off(va_start)
    raw = blob[off:off + nbytes]
    hits = []
    for i in range(len(raw) - 5):
        if raw[i] == 0xE8:
            rel = struct.unpack_from("<i", raw, i + 1)[0]
            if va_start + i + 5 + rel == target:
                hits.append(va_start + i)
    return hits


# --- pump FUN_006c9700: exact claimed instruction sequence (dump S20/S19) ---
check("pump MOV [ESP+0x20],0x66 @0x006C973A", 0x006C973A, "c7 44 24 20 66 00 00 00")
check("pump MOV [ESP+0x24],EAX(id) @0x006C9742", 0x006C9742, "89 44 24 24")
check("pump CALL FUN_00415670 @0x006C9746", 0x006C9746, "e8 25 bf d4 ff")
check("pump CALL FUN_00823c10 @0x006C974D", 0x006C974D, "e8 be a4 15 00")

# --- dispatcher FUN_00823c10: provider node+0x24 -> vtable[+4] and [+0x38] ---
check("dispatcher MOV ECX,[EDI+0x24] @0x00823C6C", 0x00823C6C, "8b 4f 24")
check("dispatcher vtable[+4] load+call @0x00823C75", 0x00823C75, "8b 01 8b 50 04 ff d2")
check("dispatcher vtable[+0x38] load+call @0x00823C7F", 0x00823C7F, "8b 01 8b 50 38 55 ff d2")

# --- singleton FUN_0043a550: slot DAT_00ba1824 instruction inside function ---
check("singleton MOV EAX,[0x00BA1824] @0x0043A571", 0x0043A571, "a1 24 18 ba 00")
check("singleton store MOV [0x00BA1824],EAX @0x0043A59B", 0x0043A59B, "a3 24 18 ba 00")
check("singleton new(0x18) PUSH @0x0043A57A", 0x0043A57A, "6a 18")
check("singleton ctor CALL FUN_0052a260 @0x0043A596", 0x0043A596, "e8 c5 fc 0e 00")

# --- map insert FUN_0072f8d0 head (dump-consistent) ---
check("insert head PUSH EBX;MOV EBX,[ESP+0xC] @0x0072F8D0", 0x0072F8D0, "53 8b 5c 24 0c 55 56 8b f1 8b 6e 04 85 ed 57 8b fe")
check("insert key CMP EAX,[EBP+0x10] @0x0072F8E7", 0x0072F8E7, "3b 45 10")

# --- consumer FUN_006b4c50: verify BOTH getter+pump call counts (claim x2 each) ---
g = count_calls(0x006B4C50, 0x600, 0x007CE1E0)
p = count_calls(0x006B4C50, 0x600, 0x006C9700)
entry = {"label": "consumer FUN_006b4c50 call census (window 0x600)",
         "getter_007ce1e0_calls": ["%08X" % x for x in g],
         "pump_006c9700_calls": ["%08X" % x for x in p],
         "claim": "getter x2, pump x2"}
entry["result"] = "PASS" if (len(g) >= 2 and len(p) >= 2) else "FAIL"
if entry["result"] != "PASS":
    res["errors"].append("consumer census: getter=%d pump=%d (claim x2 each)" % (len(g), len(p)))
res["checks"].append(entry)
print("[%s] %-52s getter x%d pump x%d" % (entry["result"], entry["label"], len(g), len(p)))

# --- avatar variant FUN_0043eae0 calls getter A (claim CALL 007ce1e0 @0x0043EBA5) ---
check("avatar-factory CALL FUN_007ce1e0 @0x0043EBA5", 0x0043EBA5, "e8 36 d3 39 00")

# --- lookup FUN_0072f580: RB-tree find FUN_004d1430 + value=node+0x14 + sentinel ---
check("lookup head @0x0072F580", 0x0072F580, "55 8b ec 51 51 53 56 57")
finds = count_calls(0x0072F580, 0x100, 0x004D1430)
entry = {"label": "lookup calls RB-find FUN_004d1430", "sites": ["%08X" % x for x in finds]}
entry["result"] = "PASS" if finds else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s sites=%s" % (entry["result"], entry["label"], entry["sites"]))

# --- loader FUN_0072fa30 calls FUN_00972df0? (claim: loader -> open VFS) ---
finds = count_calls(0x0072FA30, 0x200, 0x00972DF0)
entry = {"label": "loader FUN_0072fa30 calls FUN_00972df0", "sites": ["%08X" % x for x in finds]}
entry["result"] = "PASS" if finds else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s sites=%s" % (entry["result"], entry["label"], entry["sites"]))

# --- VFS open FUN_00972df0 calls str-eq FUN_00408b60 twice + index FUN_00972ad0 ---
e1 = count_calls(0x00972DF0, 0x300, 0x00408B60)
e2 = count_calls(0x00972DF0, 0x300, 0x00972AD0)
entry = {"label": "VFS open calls strcmp x2 + indexwalk", "strcmp_sites": ["%08X" % x for x in e1],
         "indexwalk_sites": ["%08X" % x for x in e2]}
entry["result"] = "PASS" if (len(e1) >= 2 and e2) else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s strcmp=%d indexwalk=%d" % (entry["result"], entry["label"], len(e1), len(e2)))

# --- record read FUN_00971ad0 calls CRC FUN_004063d0 + compare-helper FUN_006b22d0 ---
r1 = count_calls(0x00971AD0, 0x200, 0x004063D0)
r2 = count_calls(0x00971AD0, 0x200, 0x006B22D0)
entry = {"label": "record read calls CRC32 + getterC-as-helper",
         "crc_sites": ["%08X" % x for x in r1], "helper_sites": ["%08X" % x for x in r2]}
entry["result"] = "PASS" if (r1 and r2) else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s crc=%s helper=%s" % (entry["result"], entry["label"], entry["crc_sites"], entry["helper_sites"]))

# --- parser FUN_00730c90 calls subparsers 00730b70/00730970 ---
s1 = count_calls(0x00730C90, 0x200, 0x00730B70)
s2 = count_calls(0x00730C90, 0x200, 0x00730970)
entry = {"label": "parser calls subparsers (strings/u32 lists)",
         "sub1": ["%08X" % x for x in s1], "sub2": ["%08X" % x for x in s2]}
entry["result"] = "PASS" if (s1 and s2) else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s sub1=%s sub2=%s" % (entry["result"], entry["label"], entry["sub1"], entry["sub2"]))

# --- ctor FUN_00730700: FLDZ/FSTP [EAX+0x10] claim ---
off = va_to_off(0x00730700)
raw = blob[off:off + 0x100]
seq = bytes.fromhex("d9eed95810")  # FLDZ; FSTP [EAX+0x10]
entry = {"label": "ctor FLDZ;FSTP [EAX+0x10] in FUN_00730700 first 0x100",
         "found": seq in raw}
entry["result"] = "PASS" if entry["found"] else "FAIL"
res["checks"].append(entry)
print("[%s] %-52s FLDZ/FSTP+0x10=%s" % (entry["result"], entry["label"], entry["found"]))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)

n_pass = sum(1 for c in res["checks"] if c["result"] == "PASS")
n_fail = sum(1 for c in res["checks"] if c["result"] == "FAIL")
print("\n== A2 SUMMARY: %d PASS, %d FAIL ==" % (n_pass, n_fail))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if n_fail else 0)
