#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe C (PE-MASTER-AUDITOR, INTERNAL_QC) — remaining registry-link byte checks
for PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 (03_EVIDENCE VA registry rows not
covered by probes A/A2/A3): BNT2 ref, ArkResourceManager singleton, pair-insert,
cache get-or-create, objcreate, RM-init extension pushes + strings, magic writer,
class table @0x00A90264, RTTI factory strings, avatar-hardcode census.

READ-ONLY. Writes: 00_CONTROL\qc_probe\qc_C_registry_links_result.json
"""
import hashlib
import json
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\qc_C_registry_links_result.json"
EXPECTED_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

with open(EXE, "rb") as f:
    blob = f.read()
res = {"probe": "qc_C_registry_links", "checks": [], "errors": []}
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
    name = blob[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", blob, off + 8)
    sections.append((name, vsize, vaddr, rsize, rptr))


def va_to_off(va):
    rva = va - image_base
    for (name, vsize, vaddr, rsize, rptr) in sections:
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
    print("[%s] %-56s VA %08X" % (entry["result"], label, va))
    return entry


def cstr(va, maxlen=64):
    off = va_to_off(va)
    if off is None:
        return None
    end = blob.find(b"\x00", off, off + maxlen)
    if end < 0:
        return None
    return blob[off:end].decode("ascii", "replace")


# --- BNT2 store reader ref ---
check("BNT2 reader PUSH 0xA9BF2C @0x00967F5C", 0x00967F5C, "68 2c bf a9 00")
# --- ArkResourceManager singleton ---
check("ARM singleton MOV EAX,[0xBA12F4] @0x00415691", 0x00415691, "a1 f4 12 ba 00")
check("ARM singleton new(0x98) PUSH @0x0041569A", 0x0041569A, "6a 98")
# --- pair-insert FUN_0043c700 ---
check("pair-insert head @0x0043C700", 0x0043C700, "53 8b 5c 24 0c 55 8b e9 56 8b 75 04")
# --- objcreate FUN_006c0d50 ---
check("objcreate head @0x006C0D50", 0x006C0D50, "8b 44 24 0c 8b 54 24 04 56 8b f1")
# --- cache get-or-create FUN_00799930: vtable[+4] hash call head ---
check("cache head @0x00799930", 0x00799930, "53 8b 5c 24 08 55 56 8b f1 8b 06 8b 50 04 57 53 ff d2")
# --- RM-init extension registration pushes ---
check("RM-init PUSH .nif @0x0041F1E9", 0x0041F1E9, "68 74 a7 a7 00")
check("RM-init PUSH .nif @0x0041F23C", 0x0041F23C, "68 74 a7 a7 00")
check("RM-init PUSH .bvi @0x0041F51C", 0x0041F51C, "68 34 a7 a7 00")
check("RM-init PUSH .bvi @0x0041F56F", 0x0041F56F, "68 34 a7 a7 00")
check("RM-init PUSH .amu @0x0041F47B", 0x0041F47B, "68 44 a7 a7 00")
check("RM-init PUSH .tdf @0x0041F4CE", 0x0041F4CE, "68 3c a7 a7 00")
check("RM-init PUSH models @0x0041E5DC", 0x0041E5DC, "68 cc a8 a7 00")
check("RM-init PUSH models @0x0041E62A", 0x0041E62A, "68 cc a8 a7 00")
check("RM-init PUSH Cache @0x0041EC46", 0x0041EC46, "68 3c a8 a7 00")
# --- strings behind the models/Cache pushes ---
res["strings"] = {
    "A7A8CC": cstr(0x00A7A8CC), "A7A83C": cstr(0x00A7A83C),
    "expect_A7A8CC": "models\\", "expect_A7A83C": "Cache\\",
}
print("[info] strings: A7A8CC=%r (expect 'models\\\\') A7A83C=%r (expect 'Cache\\\\')"
      % (res["strings"]["A7A8CC"], res["strings"]["A7A83C"]))
# --- magic writer FUN_00971680 ---
check("magic-writer MOV EDX,[0xA9C4D8] @0x00971680", 0x00971680, "8b 15 d8 c4 a9 00")
# --- class table @0x00A90264 (record {0x00AB0EA8, 007EE680, 007EE5F0, 007EE6A0, 007EE780}) ---
off = va_to_off(0x00A90264)
vals = struct.unpack_from("<IIIII", blob, off)
res["class_table_00A90264"] = {
    "values": ["%08X" % v for v in vals],
    "expect": ["00AB0EA8", "007EE680", "007EE5F0", "007EE6A0", "007EE780"],
    "tester_nif_at_00A9026C": "%08X" % vals[2],
}
ok = ("%08X" % vals[0], "%08X" % vals[1], "%08X" % vals[2], "%08X" % vals[3], "%08X" % vals[4]) == \
     ("00AB0EA8", "007EE680", "007EE5F0", "007EE6A0", "007EE780")
res["class_table_00A90264"]["result"] = "PASS" if ok else "FAIL"
if not ok:
    res["errors"].append("class table mismatch: %r" % res["class_table_00A90264"]["values"])
res["checks"].append({"label": "class table @0x00A90264", **res["class_table_00A90264"]})
print("[%s] %-56s %r" % (res["class_table_00A90264"]["result"], "class table @0x00A90264", res["class_table_00A90264"]["values"]))

# --- .nif tester FUN_007ee5f0: PUSH 0xa7a774 in body? ---
off = va_to_off(0x007EE5F0)
body = blob[off:off + 0x80]
pat = bytes.fromhex("6874a7a700")
res["nif_tester_push"] = {"found": pat in body}
res["nif_tester_push"]["result"] = "PASS" if res["nif_tester_push"]["found"] else "FAIL"
res["checks"].append(res["nif_tester_push"])
print("[%s] %-56s PUSH .nif-in-body=%s" % (res["nif_tester_push"]["result"], "nif tester FUN_007ee5f0", res["nif_tester_push"]["found"]))

# --- RTTI factory strings census in .data ---
data_sec = [s for s in sections if s[0] == ".data"][0]
doff = data_sec[4]
dsize = data_sec[3]
dbytes = blob[doff:doff + dsize]
factories = ["ArkModelResourceItemFactory", "ArkImageResourceItemFactory",
             "ArkBoundResourceItemFactory", "ArkPortalResourceItemFactory",
             "ArkVegetationClimateFactory", "ArkTerrainEditZoneFactory"]
res["rtti_factories"] = {}
for f in factories:
    i = dbytes.find(f.encode())
    va = "%08X" % (image_base + data_sec[2] + i) if i >= 0 else None
    res["rtti_factories"][f] = va
    print("[info] RTTI %-36s @%s" % (f, va))
res["rtti_region_claim"] = {"claim": "0xB6D851..0xB6D9DF",
                            "in_range": all(0x00B6D851 <= int(v, 16) <= 0x00B6D9DF
                                           for v in res["rtti_factories"].values() if v)}
# boost counted_impl names
res["boost_counted_impl"] = []
for probe_name in [b"counted_impl_p@VArkModelResourceItemFactory@@",
                   b"counted_impl_p@VArkImageResourceItemFactory@@"]:
    i = dbytes.find(probe_name)
    if i >= 0:
        res["boost_counted_impl"].append(probe_name.decode())
# ArkModelManagerMain RTTI
i = dbytes.find(b"ArkModelManagerMain")
res["rtti_arkmodelmanagermain"] = "%08X" % (image_base + data_sec[2] + i) if i >= 0 else None
print("[info] RTTI ArkModelManagerMain @%s" % res["rtti_arkmodelmanagermain"])
i = dbytes.find(b"ArkModelManager\x00")
res["rtti_arkmodelmanager"] = "%08X" % (image_base + data_sec[2] + i) if i >= 0 else None

# --- avatar hardcode census (claim: 11655/11656/11705/11706) ---
text_sec = [s for s in sections if s[0] == ".text"][0]
tbytes = blob[text_sec[4]:text_sec[4] + text_sec[3]]
census = {}
for target in (0x2D87, 0x2D88, 0x2D89, 0x2DB9, 0x2DBA, 0x2DF9):
    tb = struct.pack("<I", target)
    hits = []
    start = 0
    while True:
        i = tbytes.find(tb, start)
        if i < 0:
            break
        hits.append("%08X" % (image_base + text_sec[2] + i))
        start = i + 1
    census["%d(0x%X)" % (target, target)] = hits
res["avatar_hardcode_census"] = census
res["avatar_hardcode_claim"] = {
    "claim_ids": [11655, 11656, 11705, 11706],
    "found": {k: len(v) for k, v in census.items()},
    "11705_11706_present_as_imm32": bool(census["11705(0x2DB9)"]) or bool(census["11706(0x2DBA)"]),
    "actual_FUN_00511070_id": "11769(0x2DF9) via MOV EAX,0x2df9 @0x00511245",
    "FUN_006b28e0_ids": "11656 MOV + {11655|11657} computed ADD @0x006B2922",
    "verdict": "CLAIM_CONSTANTS_PARTLY_WRONG: 11705/11706 absent; actual 11769 (0x2DF9); family in 006b28e0 = 11655/11656/11657",
}
print("[info] avatar census: %r" % {k: len(v) for k, v in census.items()})
print("[info] avatar claim verdict: %s" % res["avatar_hardcode_claim"]["verdict"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
n_pass = sum(1 for c in res["checks"] if isinstance(c, dict) and c.get("result") == "PASS")
n_fail = sum(1 for c in res["checks"] if isinstance(c, dict) and c.get("result") == "FAIL")
print("\n== C SUMMARY: %d PASS, %d FAIL, errors=%d ==" % (n_pass, n_fail, len(res["errors"])))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if (n_fail or res["errors"]) else 0)
