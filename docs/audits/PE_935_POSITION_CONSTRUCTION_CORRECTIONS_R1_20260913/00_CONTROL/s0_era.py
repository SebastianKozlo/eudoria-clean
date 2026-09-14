# -*- coding: utf-8 -*-
# PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 - S0 / G1-ERA fail-closed
# STATIC-ONLY. Verifies: SHA256+size of both originals vs contract; PE32 base
# 0x00400000; ASLR OFF; .text RVA/Raw 0x1000; >=10 spot-check VA->offset with
# pinned byte expectations from the contract (own independent pins).
# Exit 1 (no downstream) on any mismatch.

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "01_RAW", "S0_ERA_ASSERTION.json")

result = {
    "run": "PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913",
    "gate": "G1-ERA",
    "tool": "s0_era.py (own PE parse + own spot-checks)",
    "exe": core.EXE_PATH,
    "vfs": core.VFS_PATH,
}


def sha_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


fails = []

# --- 1. SHA + size -------------------------------------------------------
exe_sha = sha_of(core.EXE_PATH)
exe_size = os.path.getsize(core.EXE_PATH)
vfs_sha = sha_of(core.VFS_PATH)
vfs_size = os.path.getsize(core.VFS_PATH)

result["exe_sha256_measured"] = exe_sha
result["exe_size_measured"] = exe_size
result["vfs_sha256_measured"] = vfs_sha
result["vfs_size_measured"] = vfs_size

if exe_sha != core.CONTRACT["exe_sha256"]:
    fails.append("EXE SHA mismatch")
if exe_size != core.CONTRACT["exe_size"]:
    fails.append("EXE size mismatch")
if vfs_sha != core.CONTRACT["vfs_sha256"]:
    fails.append("VFS SHA mismatch")
if vfs_size != core.CONTRACT["vfs_size"]:
    fails.append("VFS size mismatch")

# --- 2. PE32 identity ----------------------------------------------------
pe = core.PE(core.EXE_PATH)
result["machine"] = hex(pe.machine)
result["num_sections"] = pe.num_sections
result["image_base"] = hex(pe.image_base)
result["dll_chars"] = hex(pe.dll_chars)
result["aslr"] = pe.aslr
result["opt_magic"] = hex(pe.opt_magic)
result["sections"] = [
    {"name": s["name"], "vaddr": hex(s["vaddr"]), "vsize": hex(s["vsize"]),
     "rptr": hex(s["rptr"]), "rsize": hex(s["rsize"])}
    for s in pe.sections
]

if pe.machine != 0x014C:
    fails.append("not PE32 i386")
if pe.opt_magic != 0x10B:
    fails.append("not PE32 (magic 0x10B)")
if pe.image_base != core.CONTRACT["image_base"]:
    fails.append("image base != 0x00400000")
if pe.aslr:
    fails.append("ASLR ON (expected OFF)")

text = None
for s in pe.sections:
    if s["name"] == ".text":
        text = s
if text is None:
    fails.append("no .text section")
else:
    if text["vaddr"] != core.CONTRACT["text_rva"]:
        fails.append(".text RVA != 0x1000")
    if text["rptr"] != core.CONTRACT["text_raw"]:
        fails.append(".text Raw != 0x1000")

# --- 3. >=10 spot-check VA->offset with pinned byte expectations ---------
# Pins: contract section 12 (AUDITOR_EXPECTATION) - decoded INDEPENDENTLY here
# by reading the physical EXE at the mapped offset. This is the executor's own
# spot-check, not a copy of the pins: a mismatch fails closed below.
SPOTS = [
    # (VA, expected bytes hex, label)
    (0x004C4767, "e8840df5ff", "CALL FUN_004154F0 (manager) - pin 12.2"),
    (0x004C476E, "e80df33800", "CALL FUN_00853A80 (Z provider) - pin 12.2"),
    (0x004C477F, "d8d1", "FCOM ST(1) - pin 12.2"),
    (0x004C4781, "dfe0", "FSTSW AX - pin 12.2"),
    (0x004C4783, "ddd9", "FSTP ST(1) - pin 12.2"),
    (0x004C4785, "f6c441", "TEST AH,0x41 - pin 12.2"),
    (0x004C4788, "7506", "JNE +6 -> 0x004C4790 - pin 12.2"),
    (0x004C478A, "d95c2418", "FSTP [ESP+0x18] - pin 12.2 (T-26 core)"),
    (0x004C478E, "eb02", "JMP +2 -> 0x004C4792 - pin 12.2"),
    (0x004C4792, "6828010000", "PUSH 0x128 - pin 12.2"),
    (0x004C47C1, "e88a460600", "CALL ctor FUN_00528E50 - pin 12.2"),
    (0x004C4871, "8b4214", "MOV EAX,[EDX+0x14] - pin 12.3 (D-2)"),
    (0x004C4874, "ffd0", "CALL EAX (slot +0x14) - pin 12.3 (D-2)"),
    (0x004C4878, "e8d36e3900", "CALL FUN_0085B750 (guard) - pin 12.3"),
    (0x004C488A, "e8516b3900", "CALL FUN_0085B3E0 (set-pos EXISTING) - pin 12.3"),
    (0x004C4896, "e815653900", "CALL FUN_0085ADB0 (rotation) - pin 12.3"),
    (0x00745414, "8d570c", "LEA EDX,[EDI+0x0C] - pin 12.1 (dst=rec+0x0C)"),
]

spot_results = []
for va, expect_hex, label in SPOTS:
    off = pe.va_to_off(va)
    got = pe.read_va(va, len(expect_hex) // 2)
    got_hex = got.hex() if got is not None else None
    ok = (off is not None) and (got_hex == expect_hex)
    spot_results.append({
        "va": hex(va), "file_offset": hex(off) if off is not None else None,
        "expected": expect_hex, "measured": got_hex, "ok": ok, "label": label,
    })
    if not ok:
        fails.append("spot-check FAIL @%s (%s): expected %s got %s" %
                     (hex(va), label, expect_hex, got_hex))

result["spot_checks"] = spot_results
result["spot_check_count"] = len(spot_results)
result["spot_check_pass"] = sum(1 for s in spot_results if s["ok"])

# VA->offset mapping sanity: monotonic mapping in .text
offs = [pe.va_to_off(va) for va, _, _ in SPOTS]
result["va_offset_pairs"] = [
    {"va": hex(v), "off": hex(o)} for v, o in zip([s[0] for s in SPOTS], offs)
]
# delta VA == delta offset for same-section VAs (RVA 0x1000 == Raw 0x1000)
va0, off0 = SPOTS[0][0], offs[0]
map_ok = all(
    pe.va_to_off(v) == off0 + (v - va0) for v, _, _ in SPOTS
    if pe.section_of(v) == pe.section_of(va0)
)
result["linear_mapping_in_text"] = map_ok
if not map_ok:
    fails.append("VA->offset mapping not linear within .text")

result["fails"] = fails
result["status"] = "PASS" if not fails else "FAIL"
result["fail_closed"] = result["status"] == "FAIL"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)

print(json.dumps({"status": result["status"], "fails": fails,
                  "spots_pass": "%d/%d" % (result["spot_check_pass"],
                                           result["spot_check_count"])},
                 indent=1))
sys.exit(0 if not fails else 1)
