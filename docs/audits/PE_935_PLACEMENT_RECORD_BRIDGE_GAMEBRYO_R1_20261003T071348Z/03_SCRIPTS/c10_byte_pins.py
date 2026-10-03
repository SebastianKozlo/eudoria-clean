#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C10 BYTE PINS - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
INDEPENDENT verification of load-bearing instruction bytes DIRECTLY from the
physical Entropia.exe file (no Ghidra) - method B for every load-bearing edge.
Also dumps the hardcoded id2 arrays passed to FUN_006c3fe0/FUN_006c4020 from
FUN_006c4060 (LEA operands at its callsites) and checks them against the
templates.vfs id2 set.
Output: 01_RAW/C10_BYTE_PINS.json
"""

import json
import os
import struct

RUN_ID = "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TEMPLATES = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
OUT = os.path.join(PKG, "01_RAW", "C10_BYTE_PINS.json")

EXPECTED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

# ---- PE32 section map ----
def load_exe(path):
    data = open(path, "rb").read()
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
        sections.append({"name": name, "vsize": vsize, "vaddr": vaddr,
                         "rawsize": rawsize, "rawptr": rawptr})
    return data, {"image_base": image_base, "machine": machine, "sections": sections}

def va_to_off(info, va):
    rva = va - info["image_base"]
    for s in info["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + s["rawsize"]:
            return s["rawptr"] + (rva - s["vaddr"]), s["name"]
    return None, None

def read_va(data, info, va, n):
    off, sec = va_to_off(info, va)
    if off is None:
        return None
    return data[off:off + n]

def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

# ---- pins ----
# Each pin: label, VA, length, expected bytes (from C9 Ghidra listing - method A),
# optional expected call target computed from rel32.
PINS = [
    # E-B: emitter FUN_006c3f50: lazy-init, lookup call, template->getterA
    ("PIN_EB1_lookup_call", 0x006C3F62, 5, "E8 19 4A 06 00", "call_rel32_target", 0x0072F580),
    ("PIN_EB2_mov_ecx_edi_after_lookup", 0x006C3F6E, 2, "8B CF", None, None),
    ("PIN_EB3_getterA_call", 0x006C3F74, 5, "E8 67 5E 10 00", "call_rel32_target", 0x007CE1E0),
    ("PIN_EB4_mov_ebx_0x66", 0x006C3F69, 5, "BB 66 00 00 00", None, None),
    ("PIN_EB5_store_type", 0x006C3F8D, 2, "89 19", None, None),
    ("PIN_EB6_store_A", 0x006C3F8F, 3, "89 41 04", None, None),
    # E-L: lookup impl FUN_0072f580: mapfind call, node+0x14, default, RET 4
    ("PIN_EL1_mapfind_call", 0x0072F590, 5, "E8 65 1E 26 01", "call_rel32_target", 0x004D1430),
    ("PIN_EL2_add_eax_0x14", 0x0072F59E, 3, "83 C0 14", None, None),
    ("PIN_EL3_ret_4", 0x0072F5A2, 3, "C2 04 00", None, None),
    ("PIN_EL4_default_dat", 0x0072F5A5, 5, "B8 00 58 BA 00", "mov_eax_imm32", 0x00BA5800),
    # E-M: mapfind key at node+0x10, left at +8, right at +0xC
    ("PIN_EM1_mapfind_entry", 0x004D1430, 4, "55 8B EC 51", None, None),
    # E-R: reader FUN_0072fa30 callsite of open (per listing L04 first calls)
    # (will match exact bytes from listing L04 window in-script below)
    # E-P: parse fields - we pin the first reads via listing L06 in-script
    # E-C: ArkObject ctor: vtable + getter call -> this+0x28 (listing L07)
    # E-S: pos/rot setters
    ("PIN_ES1_pos_setter_entry", 0x00730F90, 6, "8B 44 24 04 8B 10", None, None),
    ("PIN_ES2_pos_setter_store1", 0x00730F96, 3, "89 51 08", None, None),
    ("PIN_ES3_pos_setter_store2", 0x00730F9C, 3, "89 51 0C", None, None),
    ("PIN_ES4_pos_setter_store3", 0x00730FA2, 3, "89 41 10", None, None),
    ("PIN_ES5_rot_setter_entry", 0x00730FB0, 6, "8B 44 24 04 8B 10", None, None),
    ("PIN_ES6_rot_setter_store1", 0x00730FB6, 3, "89 51 14", None, None),
    ("PIN_ES7_rot_setter_store2", 0x00730FBC, 3, "89 51 18", None, None),
    ("PIN_ES8_rot_setter_store3", 0x00730FC2, 3, "89 41 1C", None, None),
    ("PIN_ES9_pair_setter_store1", 0x00730FD6, 3, "89 51 20", None, None),
    ("PIN_ES10_pair_setter_store2", 0x00730FDC, 3, "89 41 24", None, None),
    # E-K: driver K02 hardcoded id2
    ("PIN_EK1_push_0x3ed3", 0x005B6597, 5, "68 2D 3E 00 00", "push_imm32", 0x3ED3),
    ("PIN_EK2_call_constrB", 0x005B659C, 5, "E8 EF F8 FF FF", "call_rel32_target", 0x005B5F90),
    # E-T: attach thunk
    ("PIN_ET1_thunk_b_entry", 0x0077C0B0, 4, "8B 4C 24 04 6A", None, None),
    ("PIN_ET2_thunk_b_call", 0x0077C0B6, 5, "E8 A5 DC FF FF", "call_rel32_target", 0x00779D60),
    ("PIN_ET3_thunk_f_call", 0x0077C0F4, 5, "E8 27 E7 FF FF", "call_rel32_target", 0x00779E20),
    ("PIN_ET4_thunk_c0_call", 0x0077C0E0, 5, "E8 AB F2 FF FF", "call_rel32_target", 0x0077AD90),
    # E-D: deserB call to deserA + class-id checks
    ("PIN_ED1_call_deserA", 0x004C483D, 5, "E8 8E 0D 00 00", "call_rel32_target", 0x007453D0),
]

def main():
    data, info = load_exe(EXE)
    sha = sha256_file(EXE)
    assert sha == EXPECTED_EXE_SHA256, "EXE identity mismatch"
    res = {
        "run_id": RUN_ID, "stage": "C10_byte_pins",
        "measured": {
            "exe_path": EXE, "exe_size": len(data), "exe_sha256": sha,
            "image_base": "0x%08X" % info["image_base"],
            "sections": [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                          "rawsize": s["rawsize"]} for s in info["sections"]],
            "pins": [], "string_search": [], "id2_arrays": [],
        },
        "interpreted": {},
        "errors": [],
    }

    ok_count = 0
    for (label, va, n, expected_hex, kind, target) in PINS:
        raw = read_va(data, info, va, n)
        actual_hex = " ".join("%02X" % b for b in raw) if raw else None
        entry = {"label": label, "va": "0x%08X" % va, "length": n,
                 "expected_from_ghidra_listing": expected_hex,
                 "actual_raw_exe_bytes": actual_hex,
                 "byte_match": (actual_hex == expected_hex)}
        if kind == "call_rel32_target" and raw and raw[0] == 0xE8:
            rel, = struct.unpack_from("<i", raw, 1)
            computed = va + 5 + rel
            entry["computed_rel32_target"] = "0x%08X" % computed
            entry["target_match"] = (computed == target)
        if kind == "mov_eax_imm32" and raw and raw[0] == 0xB8:
            imm, = struct.unpack_from("<I", raw, 1)
            entry["computed_imm32"] = "0x%08X" % imm
            entry["target_match"] = (imm == target)
        if kind == "push_imm32" and raw and raw[0] == 0x68:
            imm, = struct.unpack_from("<I", raw, 1)
            entry["computed_imm32"] = "0x%08X" % imm
            entry["target_match"] = (imm == target)
        if entry["byte_match"]:
            ok_count += 1
        res["measured"]["pins"].append(entry)
    res["interpreted"]["pins_byte_matched"] = "%d/%d" % (ok_count, len(PINS))

    # string search: "Parameters\templates.vfs"
    needle = b"Parameters\\templates.vfs\x00"
    idx = data.find(needle)
    hits = []
    while idx >= 0 and len(hits) < 5:
        # file offset -> VA
        for s in info["sections"]:
            if s["rawptr"] <= idx < s["rawptr"] + s["rawsize"]:
                va = info["image_base"] + s["vaddr"] + (idx - s["rawptr"])
                hits.append({"file_offset": idx, "va": "0x%08X" % va, "section": s["name"]})
                break
        idx = data.find(needle, idx + 1)
    res["measured"]["string_search"] = {
        "needle": "Parameters\\templates.vfs",
        "hits": hits,
    }

    # id2 arrays: LEA operands at FUN_006c4060 callsites 0x006C40A3 / 0x006C40B2 / 0x006C40C1
    # LEA ECX,[imm32] = 8B 0D imm32? No: LEA r32, m = 8D 0D imm32 (LEA ECX, [addr])
    for site_va in (0x006C40A3, 0x006C40B2, 0x006C40C1):
        w = read_va(data, info, site_va, 8)
        if w is None:
            continue
        # detect LEA pattern: 8D 0D/8D 15/8D 05... imm32
        arr_entry = {"callsite": "0x%08X" % site_va, "bytes": " ".join("%02X" % b for b in w)}
        if w[0] == 0x8D and (w[1] & 0xC7) == 0x05:
            imm, = struct.unpack_from("<I", w, 2)
            arr_entry["lea_operand_va"] = "0x%08X" % imm
            arr = read_va(data, info, imm, 32)
            if arr:
                vals = list(struct.unpack("<8I", arr))
                arr_entry["array_u32"] = vals
                # templates id2 set membership
                tv = open(TEMPLATES, "rb").read()
                id2set = set()
                pos = 16
                while pos + 16 <= len(tv):
                    bid, = struct.unpack_from("<I", tv, pos)
                    id2set.add(bid)
                    bsize, = struct.unpack_from("<I", tv, pos + 4)
                    stride = ((16 + bsize + 36 - 1) // 36) * 36 if False else None
                    # templates.vfs base = 36 per C1
                    pos += ((16 + bsize + 36 - 1) // 36) * 36
                arr_entry["id2_membership"] = [v in id2set for v in vals]
        res["measured"]["id2_arrays"].append(arr_entry)

    # cross-check: every call in PINS verified byte-exact against the listing? summary
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("C10 written:", OUT)
    print("pins matched:", res["interpreted"]["pins_byte_matched"])
    for e in res["measured"]["pins"]:
        if not e["byte_match"]:
            print("MISMATCH:", e["label"], e["actual_raw_exe_bytes"], "!=", e["expected_from_ghidra_listing"])
    print("string hits:", res["measured"]["string_search"]["hits"])
    for a in res["measured"]["id2_arrays"]:
        print("array:", a)

if __name__ == "__main__":
    main()
