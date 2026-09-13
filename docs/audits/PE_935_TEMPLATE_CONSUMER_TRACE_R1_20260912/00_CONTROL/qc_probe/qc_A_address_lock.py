#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe A (PE-MASTER-AUDITOR, INTERNAL_QC, fresh context) for run
PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912.

INDEPENDENT address-lock spot check. Own PE parsing (no pefile, no trust in the
executor's S3): DOS header -> e_lfanew -> PE sig -> COFF -> Optional header ->
section table. VA->file mapping built from scratch. Then raw-byte verification
of the load-bearing chain links claimed in 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md.

READ-ONLY on all inputs. Writes only:
00_CONTROL\qc_probe\qc_A_address_lock_result.json
"""
import hashlib
import json
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\qc_A_address_lock_result.json"

EXPECTED_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

with open(EXE, "rb") as f:
    blob = f.read()

res = {"probe": "qc_A_address_lock", "exe_size": len(blob), "checks": [], "errors": []}

sha = hashlib.sha256(blob).hexdigest().upper()
res["exe_sha256"] = sha
if sha != EXPECTED_SHA:
    res["errors"].append("EXE SHA mismatch: %s" % sha)
    print("[FAIL] EXE SHA mismatch")
    sys.exit(2)

# ---------------------------------------------------------------- own PE parse
if blob[:2] != b"MZ":
    res["errors"].append("no MZ")
    sys.exit(2)
e_lfanew = struct.unpack_from("<I", blob, 0x3C)[0]
if blob[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
    res["errors"].append("no PE sig at e_lfanew=%d" % e_lfanew)
    sys.exit(2)
coff = e_lfanew + 4
machine, num_sections, tds, _, _, size_opt, chars = struct.unpack_from("<HHIIIHH", blob, coff)
opt = coff + 20
magic = struct.unpack_from("<H", blob, opt)[0]
image_base = struct.unpack_from("<I", blob, opt + 28)[0]  # PE32: ImageBase @ opt+28
dll_chars = struct.unpack_from("<H", blob, opt + 70)[0]  # DllCharacteristics @ opt+70
sec_tab = opt + size_opt
sections = []
for i in range(num_sections):
    off = sec_tab + 40 * i
    name = blob[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", blob, off + 8)
    sections.append({"name": name, "vsize": vsize, "vaddr": vaddr, "rsize": rsize, "rptr": rptr})

res["pe"] = {
    "e_lfanew": e_lfanew, "machine": "%04X" % machine, "num_sections": num_sections,
    "magic": "%04X" % magic, "image_base": "%08X" % image_base,
    "dll_characteristics": "%04X" % dll_chars,
    "aslr_dynamic_base": bool(dll_chars & 0x40),
    "sections": [
        {"name": s["name"], "vsize": s["vsize"], "vaddr": "%08X" % s["vaddr"],
         "rsize": s["rsize"], "rptr": s["rptr"]} for s in sections],
}


def va_to_off(va):
    rva = va - image_base
    for s in sections:
        if s["vaddr"] <= rva < s["vaddr"] + s["vsize"]:
            delta = rva - s["vaddr"]
            if delta < s["rsize"]:
                return s["rptr"] + delta, s["name"]
            return None, s["name"] + " (bss/past-raw)"
    return None, None


def read_va(va, n):
    off, sec = va_to_off(va)
    if off is None:
        return None, sec
    return blob[off:off + n], sec


def cstr_va(va, maxlen=64):
    off, sec = va_to_off(va)
    if off is None:
        return None, sec
    end = blob.find(b"\x00", off, off + maxlen)
    if end < 0:
        return None, sec
    return blob[off:end].decode("ascii", "replace"), sec


def check(label, va, expected_hex, note=""):
    """Verify that the bytes at VA start with expected (hex string, '??' = wildcard)."""
    exp = expected_hex.split()
    n = len(exp)
    raw, sec = read_va(va, n)
    entry = {"label": label, "va": "%08X" % va, "section": sec,
             "expected": expected_hex, "note": note}
    if raw is None:
        entry["result"] = "FAIL"
        entry["reason"] = "VA not mappable to raw bytes (section: %s)" % sec
        entry["got"] = None
        res["errors"].append("unmappable VA %08X (%s)" % (va, label))
    else:
        got = raw.hex()
        entry["got"] = " ".join(got[i:i + 2] for i in range(0, len(got), 2))
        ok = True
        for k, e in enumerate(exp):
            if e == "??":
                continue
            if raw[k] != int(e, 16):
                ok = False
                break
        entry["result"] = "PASS" if ok else "FAIL"
        if not ok:
            res["errors"].append("byte mismatch at %08X (%s): expected %s got %s"
                                 % (va, label, expected_hex, entry["got"]))
    res["checks"].append(entry)
    print("[%s] %-46s VA %08X  %s" % (entry["result"], label, va, note))
    return entry


def check_str(label, va, expected_ascii):
    got, sec = cstr_va(va)
    entry = {"label": label, "va": "%08X" % va, "section": sec,
             "expected": expected_ascii, "got": got}
    entry["result"] = "PASS" if got == expected_ascii else "FAIL"
    if entry["result"] != "PASS":
        res["errors"].append("string mismatch at %08X (%s): expected %r got %r"
                             % (va, label, expected_ascii, got))
    res["checks"].append(entry)
    print("[%s] %-46s VA %08X  expected=%r got=%r" % (entry["result"], label, va, expected_ascii, got))
    return entry


print("== own PE header parse ==")
print("image_base=%08X sections=%d aslr=%s" % (image_base, num_sections, res["pe"]["aslr_dynamic_base"]))

# ------------------------------------------------ mandatory links (contract)
print("\n== mandatory address locks ==")
# 1) parser write A -> [EDI+0x08] @0x00730CE6  (MOV dword ptr [EDI+8],EAX)
check("parser A->+0x08 @0x00730CE6", 0x00730CE6, "89 47 08", "MOV [EDI+0x8],EAX")
# parser B->+0x04 @0x00730D14, C->+0x0C @0x00730D42, D f32 -> +0x10 @0x00730D70
check("parser B->+0x04 @0x00730D14", 0x00730D14, "89 47 04", "MOV [EDI+0x4],EAX")
check("parser C->+0x0C @0x00730D42", 0x00730D42, "89 47 0c", "MOV [EDI+0xC],EAX")
check("parser D f32 FSTP +0x10 @0x00730D70", 0x00730D70, "d9 5f 10", "FSTP [EDI+0x10]")
check("parser F u32 ->+0x2C @0x00730DB6", 0x00730DB6, "89 57 2c", "MOV [EDI+0x2C],EDX")
# 2) getter A @0x007CE1E0
check("getter A [ECX+0x08] @0x007CE1E0", 0x007CE1E0, "8b 41 08 c3", "MOV EAX,[ECX+8]; RET")
# 3) stride rule FUN_00979d00
check("stride head @0x00979D00", 0x00979D00, "8b 41 04 85 c0 74 14 8b 49 14 83 c0 0f 33 d2 f7 f1 83 c0 01 0f af c1 83 c0 f0 c3",
      "MOV EAX,[ECX+4];TEST;JZ;MOV ECX,[ECX+0x14];ADD EAX,0xF;XOR EDX,EDX;DIV ECX;ADD EAX,1;IMUL EAX,ECX;ADD EAX,-0x10;RET")
# 4) CRC-32 gate FUN_004063d0
check("crc32 head @0x004063D0", 0x004063D0, "81 ec 00 04 00 00 53 8b 9c 24 0c 04 00 00 56 57",
      "SUB ESP,0x400; PUSH EBX; MOV EBX,[ESP+0x40C]; PUSH ESI; PUSH EDI")
check("crc32 init ffffffff @0x0040640F", 0x0040640F, "83 c9 ff", "OR ECX,0xFFFFFFFF (init)")
check("crc32 loop body @0x00406416", 0x00406416, "0f b6 02 33 c1 25 ff 00 00 00 c1 e9 08 33 4c 84 0c 83 c2 01 83 ee 01 75 e7",
      "MOVZX EAX,[EDX];XOR EAX,ECX;AND EAX,0xFF;SHR ECX,8;XOR ECX,[ESP+EAX*4+0xC];...")
check("crc32 final NOT @0x00406430", 0x00406430, "f7 d1 5e 89 0b", "NOT ECX; POP ESI; MOV [EBX],ECX")
# 5) map insert FUN_0072f8d0
raw, sec = read_va(0x0072F8D0, 16)
print("[info] FUN_0072F8D0 section=%s bytes=%s" % (sec, raw.hex() if raw else None))
check("register/map insert prolog @0x0072F8D0", 0x0072F8D0, "55 8b ec", "STLport _Rb_tree insert prolog (PUSH EBP; MOV EBP,ESP)")
# insert key getter MOV EAX,[ECX] @0x004123D0
check("insert key getter @0x004123D0", 0x004123D0, "8b 01 c3", "MOV EAX,[ECX]; RET")
# 6) pump FUN_006c9700: local_14 = 0x66; need actual prolog; scan first 0x40 bytes for C7 44 24 xx 66 00 00 00
pump_raw, sec = read_va(0x006C9700, 0x40)
found_66 = None
if pump_raw:
    for i in range(len(pump_raw) - 8):
        if pump_raw[i] == 0xC7 and pump_raw[i + 1] == 0x44 and pump_raw[i + 2] == 0x24 \
                and pump_raw[i + 4] == 0x66 and pump_raw[i + 5] == 0x00:
            found_66 = 0x006C9700 + i
            break
entry = {"label": "pump type-const 0x66 @FUN_006c9700", "va": "006C9700", "section": sec,
         "scan_bytes": pump_raw.hex() if pump_raw else None, "mov_imm66_va": "%08X" % found_66 if found_66 else None,
         "expected": "C7 44 24 ?? 66 00 00 00 (MOV dword [ESP+x], 0x66)"}
entry["result"] = "PASS" if found_66 else "FAIL"
if not found_66:
    res["errors"].append("no MOV [ESP+x],0x66 pattern in first 0x40 bytes of FUN_006c9700")
res["checks"].append(entry)
print("[%s] %-46s VA %08X  mov-imm66 at %s" % (entry["result"], entry["label"], 0x006C9700, entry["mov_imm66_va"]))
# pump calls FUN_00415670 + FUN_00823c10: scan body for E8 rel32 = target
def scan_call(va_start, nbytes, target):
    raw, sec = read_va(va_start, nbytes)
    if raw is None:
        return None, sec
    for i in range(len(raw) - 5):
        if raw[i] == 0xE8:
            rel = struct.unpack_from("<i", raw, i + 1)[0]
            if va_start + i + 5 + rel == target:
                return va_start + i, sec
    return None, sec

c1, s1 = scan_call(0x006C9700, 0x100, 0x00415670)
c2, s2 = scan_call(0x006C9700, 0x100, 0x00823C10)
entry = {"label": "pump calls FUN_00415670/FUN_00823c10", "call_00415670_va": "%08X" % c1 if c1 else None,
         "call_00823c10_va": "%08X" % c2 if c2 else None}
entry["result"] = "PASS" if (c1 and c2) else "FAIL"
if entry["result"] != "PASS":
    res["errors"].append("pump call scan failed: FUN_00415670@%s FUN_00823c10@%s" % (c1, c2))
res["checks"].append(entry)
print("[%s] %-46s call15670@%s call823c10@%s" % (entry["result"], entry["label"], c1, c2))

# ------------------------------------------------ additional registry links
print("\n== additional registry links ==")
check("loader PUSH templates-path @0x0072FAAC", 0x0072FAAC, "68 30 6d a8 00", "PUSH 0xA86D30")
check("lookup sentinel @0x0072F5A5", 0x0072F5A5, "b8 00 58 ba 00", "MOV EAX,0xBA5800")
check("lookup value +0x14 @0x0072F59E", 0x0072F59E, "83 c0 14", "ADD EAX,0x14")
raw, sec = read_va(0x0072FCE0, 0x40)
val_bytes = raw.hex() if raw else None
val_ok = False
if raw:
    # find the CMP [ECX],0 / CMP [ECX+8],0 / CMP [ECX+4],0 / CMP [ECX+0xC],0 family
    pats = ["833900", "83790800", "83790400", "83790c00"]
    joined = raw.hex()
    val_ok = all(p in joined for p in pats)
entry = {"label": "validation CMP slots @0x0072FCE0", "va": "0072FCE0", "section": sec,
         "expected": "83 39 00 / 83 79 08 00 / 83 79 04 00 / 83 79 0c 00 all present",
         "got": val_bytes, "result": "PASS" if val_ok else "FAIL"}
if not val_ok:
    res["errors"].append("validation slot CMP family not all present @0x0072FCE0")
res["checks"].append(entry)
print("[%s] %-46s VA 0072FCE0 slot-CMPs=%s" % (entry["result"], entry["label"], val_ok))
check("singleton MOV EAX,[0xBA1824] @0x0043A550", 0x0043A550, "a1 24 18 ba 00", "registry singleton slot")
check("getter B [ECX+4] @0x00746550", 0x00746550, "8b 41 04 c3", "MOV EAX,[ECX+4]; RET")
check("getter C [ECX+0xC] @0x006B22D0", 0x006B22D0, "8b 41 0c c3", "MOV EAX,[ECX+0xC]; RET")
check("rec offset seek @0x00979D20", 0x00979D20, "8b 41 10 83 c0 10 c3", "MOV EAX,[ECX+0x10]; ADD EAX,0x10; RET")
# strings
check_str("string Parameters\\templates.vfs", 0x00A86D30, "Parameters\\templates.vfs")
check_str("string .nif", 0x00A7A774, ".nif")
check_str("string .bvi", 0x00A7A734, ".bvi")
check_str("string .tdf", 0x00A7A73C, ".tdf")
check_str("string .amu", 0x00A7A744, ".amu")
check_str("string .vfs", 0x00A86820, ".vfs")
check_str("string BNT2", 0x00A9BF2C, "BNT2")
# VFS magics: registry says "ArkVFS02" x2 @0x00A9C4D8/0x00A9C4E4 and "ArkVFS01" @0x00A9C4F0
check_str("string ArkVFS02 @0x00A9C4D8", 0x00A9C4D8, "ArkVFS02")
check_str("string ArkVFS02 @0x00A9C4E4", 0x00A9C4E4, "ArkVFS02")
check_str("string ArkVFS01 @0x00A9C4F0", 0x00A9C4F0, "ArkVFS01")

# consumer FUN_006b4c50: verify it calls FUN_007ce1e0 (getter A) and FUN_006c9700 (pump)
cA1, _ = scan_call(0x006B4C50, 0x300, 0x007CE1E0)
cP1, _ = scan_call(0x006B4C50, 0x300, 0x006C9700)
entry = {"label": "consumer FUN_006b4c50 calls getter+pump",
         "call_getter_A": "%08X" % cA1 if cA1 else None,
         "call_pump": "%08X" % cP1 if cP1 else None,
         "expected": "at least one CALL 007CE1E0 and one CALL 006C9700 in first 0x300 bytes"}
entry["result"] = "PASS" if (cA1 and cP1) else "FAIL"
if entry["result"] != "PASS":
    res["errors"].append("consumer call scan: getter@%s pump@%s" % (cA1, cP1))
res["checks"].append(entry)
print("[%s] %-46s getter@%s pump@%s" % (entry["result"], entry["label"], cA1, cP1))

# dispatcher FUN_00823c10: virtual-call pattern FF 55 04 (call [ebp+4]) or FF 50 04/FF 50 38 (call [eax+4]/[eax+0x38])
disp_raw, sec = read_va(0x00823C10, 0x200)
found_v4 = found_v38 = None
if disp_raw:
    for i in range(len(disp_raw) - 2):
        if disp_raw[i] == 0xFF and disp_raw[i + 1] == 0x50 and disp_raw[i + 2] == 0x04:
            found_v4 = 0x00823C10 + i
        if disp_raw[i] == 0xFF and disp_raw[i + 1] == 0x50 and disp_raw[i + 2] == 0x38:
            found_v38 = 0x00823C10 + i
entry = {"label": "dispatcher virtual calls [+4]/[+0x38] @0x00823C10",
         "call_vt4": "%08X" % found_v4 if found_v4 else None,
         "call_vt38": "%08X" % found_v38 if found_v38 else None}
entry["result"] = "PASS" if (found_v4 and found_v38) else "FAIL"
if entry["result"] != "PASS":
    res["errors"].append("dispatcher virtual call scan: vt4@%s vt38@%s" % (found_v4, found_v38))
res["checks"].append(entry)
print("[%s] %-46s vt+4@%s vt+38@%s" % (entry["result"], entry["label"], found_v4, found_v38))

# sentinel bss claim: 0x00BA5800 beyond .data raw end
data_sec = [s for s in sections if s["name"] == ".data"][0]
raw_end_va = image_base + data_sec["vaddr"] + data_sec["rsize"]
virt_end_va = image_base + data_sec["vaddr"] + data_sec["vsize"]
res["sentinel_check"] = {
    "data_raw_end_va": "%08X" % raw_end_va, "data_virtual_end_va": "%08X" % virt_end_va,
    "sentinel_va": "00BA5800",
    "sentinel_in_bss": raw_end_va <= 0x00BA5800 < virt_end_va,
    "claim": "sentinel 0x00BA5800 lies in .data bss (virtual beyond raw)"
}
print("[info] .data raw_end=%08X virt_end=%08X sentinel=00BA5800 in_bss=%s"
      % (raw_end_va, virt_end_va, res["sentinel_check"]["sentinel_in_bss"]))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)

n_pass = sum(1 for c in res["checks"] if c["result"] == "PASS")
n_fail = sum(1 for c in res["checks"] if c["result"] == "FAIL")
print("\n== SUMMARY: %d PASS, %d FAIL, errors=%d ==" % (n_pass, n_fail, len(res["errors"])))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if (n_fail or res["errors"]) else 0)
