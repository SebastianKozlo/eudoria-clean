#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C10v2 BYTE PINS - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
Method A = Ghidra listing (C9_LISTING_WINDOWS.json). Method B = raw bytes read
directly from the physical Entropia.exe by this script's own PE mapper + x86
rel32 decoder (no Ghidra involved).
- Signed-byte normalization: Ghidra Jython printed bytes >0x7F as negative hex
  ("-18" == 0xE8); this script normalizes both sides to unsigned hex.
- For every CALL (E8 rel32) instruction in the windows, computes the target from
  RAW bytes and compares with the listing's CALL target text.
- Pins the "Parameters\templates.vfs" string VA.
Output: 01_RAW/C10V2_BYTE_CROSSCHECK.json
"""

import json
import os
import re
import struct

RUN_ID = "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
L9 = os.path.join(PKG, "01_RAW", "C9_LISTING_WINDOWS.json")
OUT = os.path.join(PKG, "01_RAW", "C10V2_BYTE_CROSSCHECK.json")
EXPECTED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_exe(path):
    data = open(path, "rb").read()
    assert data[:2] == b"MZ"
    e_lfanew, = struct.unpack_from("<I", data, 0x3C)
    assert data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00"
    opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
    image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
    num_sections, = struct.unpack_from("<H", data, e_lfanew + 6)
    sec_off = e_lfanew + 24 + opt_size
    sections = []
    for i in range(num_sections):
        off = sec_off + i * 40
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<4I", data, off + 8)
        sections.append({"name": data[off:off+8].rstrip(b"\x00").decode(),
                         "vaddr": vaddr, "rawsize": rawsize, "rawptr": rawptr})
    return data, {"image_base": image_base, "sections": sections}


def va_to_off(info, va):
    rva = va - info["image_base"]
    for s in info["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + s["rawsize"]:
            return s["rawptr"] + (rva - s["vaddr"])
    return None


def norm_bytes(hexstr):
    """Normalize a Ghidra signed-hex byte string ('-18 19 -4A') to unsigned ('E8 19 B6')."""
    out = []
    for tok in hexstr.split():
        v = int(tok, 16)
        if v < 0:
            v = v & 0xFF
        out.append("%02X" % v)
    return " ".join(out)


def main():
    data, info = load_exe(EXE)
    sha = sha256_file(EXE)
    assert sha == EXPECTED_EXE_SHA256, "EXE identity mismatch"
    l9 = json.load(open(L9, "r", encoding="utf-8"))

    res = {"run_id": RUN_ID, "stage": "C10v2_byte_crosscheck",
           "measured": {"exe_sha256": sha,
                        "windows": [], "call_targets": [],
                        "string_pin": None},
           "interpreted": {},
           "errors": []}

    total_ins = 0
    byte_match_ins = 0
    call_checks = []

    for wlabel, w in l9["measured"]["windows"].items():
        for ins in w["instructions"]:
            va = int(ins["addr"], 16)
            listing_bytes = norm_bytes(ins["bytes"])
            n = len(listing_bytes.split())
            off = va_to_off(info, va)
            if off is None:
                res["errors"].append("no mapping for %s" % ins["addr"])
                continue
            raw = data[off:off + n]
            raw_hex = " ".join("%02X" % b for b in raw)
            total_ins += 1
            match = (raw_hex == listing_bytes)
            if match:
                byte_match_ins += 1
            else:
                res["errors"].append("BYTE MISMATCH %s @%s listing=%s raw=%s" %
                                     (wlabel, ins["addr"], listing_bytes, raw_hex))
            # CALL rel32 target crosscheck
            if raw and raw[0] == 0xE8 and n >= 5:
                rel, = struct.unpack_from("<i", raw, 1)
                computed = va + 5 + rel
                m = re.search(r"CALL\s+(0x[0-9a-fA-F]+)", ins["text"])
                if m:
                    listed = int(m.group(1), 16)
                    call_checks.append({
                        "addr": "0x%08X" % va, "raw_target": "0x%08X" % computed,
                        "listing_target": "0x%08X" % listed,
                        "match": computed == listed,
                        "listing_text": ins["text"],
                    })
            # MOV/PUSH imm32 pattern crosscheck (B8 imm32, 68 imm32)
            if raw and n >= 5 and raw[0] in (0xB8, 0x68):
                imm, = struct.unpack_from("<I", raw, 1)
                m = re.search(r"0x([0-9a-fA-F]+)", ins["text"])
                if m:
                    listed = int(m.group(1), 16)
                    if listed == imm:
                        call_checks.append({
                            "addr": "0x%08X" % va, "raw_imm32": "0x%08X" % imm,
                            "listing_imm32": "0x%08X" % listed, "match": True,
                            "listing_text": ins["text"]})

    res["measured"]["windows"] = {"instructions_compared": total_ins,
                                  "instructions_byte_identical": byte_match_ins}
    res["measured"]["call_targets"] = call_checks

    # string pin
    needle = b"Parameters\\templates.vfs\x00"
    idx = data.find(needle)
    if idx >= 0:
        for s in info["sections"]:
            if s["rawptr"] <= idx < s["rawptr"] + s["rawsize"]:
                va = info["image_base"] + s["vaddr"] + (idx - s["rawptr"])
                res["measured"]["string_pin"] = {
                    "file_offset": idx, "va": "0x%08X" % va, "section": s["name"],
                    "content": "Parameters\\templates.vfs"}
                break

    res["interpreted"]["listing_vs_raw_bytes"] = "%d/%d identical" % (byte_match_ins, total_ins)
    ok_calls = sum(1 for c in call_checks if c["match"])
    res["interpreted"]["call_and_imm_targets_crosschecked"] = "%d/%d match" % (ok_calls, len(call_checks))

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("C10v2 written:", OUT)
    print("listing_vs_raw:", res["interpreted"]["listing_vs_raw_bytes"])
    print("call targets:", res["interpreted"]["call_and_imm_targets_crosschecked"])
    for e in res["errors"][:20]:
        print("ERR:", e)
    print("string:", res["measured"]["string_pin"])


if __name__ == "__main__":
    main()
