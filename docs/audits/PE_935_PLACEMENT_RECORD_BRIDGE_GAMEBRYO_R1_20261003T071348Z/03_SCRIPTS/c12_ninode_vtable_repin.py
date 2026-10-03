#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C12 NINODE VTABLE RE-PIN - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
Re-pins the historical NINODE_SLOT17 anchors from RAW exe bytes (no Ghidra):
  1. NiNode::vftable VA from the ctor instruction at 0x007B6000 (MOV [reg], imm32).
  2. Dump vtable slots 0..46 (47 slots per NINODE_SLOT17 canon).
  3. Historical anchor re-pin: slot 17 (+0x44) == 0x007B5390 (GetObjByName-like,
     NINODE_SLOT17 run's anchor) - byte check.
  4. UpdateWorldData fingerprint: slot 27 (+0x6C) function probed for the
     'rep movsd' copy of m_kLocal (+0x38) -> m_kWorld (+0x6C) 52-byte transform.
Output: 01_RAW/C12_NINODE_VTABLE_REPIN.json
"""

import json
import os
import struct

RUN_ID = "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = os.path.join(PKG, "01_RAW", "C12_NINODE_VTABLE_REPIN.json")
EXPECTED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

CTOR_VA = 0x007B6000
NINODE_SLOT17_EXPECTED = 0x007B5390  # historical anchor (NINODE_SLOT17 run)
NUM_SLOTS = 47


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
    opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
    image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
    num_sections, = struct.unpack_from("<H", data, e_lfanew + 6)
    sec_off = e_lfanew + 24 + opt_size
    sections = []
    for i in range(num_sections):
        off = sec_off + i * 40
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<4I", data, off + 8)
        sections.append({"vaddr": vaddr, "rawsize": rawsize, "rawptr": rawptr})
    return data, {"image_base": image_base, "sections": sections}


def va_to_off(info, va):
    rva = va - info["image_base"]
    for s in info["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + s["rawsize"]:
            return s["rawptr"] + (rva - s["vaddr"])
    return None


def read_va(data, info, va, n):
    off = va_to_off(info, va)
    if off is None:
        return None
    return data[off:off + n]


def main():
    data, info = load_exe(EXE)
    sha = sha256_file(EXE)
    assert sha == EXPECTED_EXE_SHA256, "EXE identity mismatch"

    res = {"run_id": RUN_ID, "stage": "C12_ninode_vtable_repin",
           "measured": {"exe_sha256": sha, "ctor_window": {}, "vtable": {},
                        "historical_anchor_repin": {}, "update_world_data_probe": {}},
           "interpreted": {},
           "errors": []}

    # 1. ctor window raw bytes (first 64)
    ctor_raw = read_va(data, info, CTOR_VA, 64)
    res["measured"]["ctor_window"] = {
        "va": "0x%08X" % CTOR_VA,
        "bytes_hex": ctor_raw.hex(" "),
    }

    # find MOV dword ptr [reg], imm32: C7 01/02/03/06/07 imm32 within first 128 bytes
    # (verified manually in the ctor bytes: C7 06 F4 CC A8 00 = MOV [ESI], 0x00A8CCF4)
    ctor_raw = read_va(data, info, CTOR_VA, 128)
    vtable_va = None
    for i in range(0, 120):
        if ctor_raw[i] == 0xC7 and (ctor_raw[i + 1] & 0xC0) == 0x00:
            imm, = struct.unpack_from("<I", ctor_raw, i + 2)
            if 0x00A00000 <= imm <= 0x00BFFFFF:  # .rdata/.data range heuristic
                vtable_va = imm
                res["measured"]["ctor_window"]["vtable_imm32_site"] = "0x%08X" % (CTOR_VA + i)
                res["measured"]["ctor_window"]["vtable_imm32"] = "0x%08X" % imm
                res["measured"]["ctor_window"]["vtable_store_mnemonic"] = "MOV dword ptr [ESI], 0x%08X" % imm
                break

    if vtable_va is None:
        res["errors"].append("vtable imm32 not found in ctor window")
    else:
        # 2. dump vtable slots
        slots = []
        raw = read_va(data, info, vtable_va, NUM_SLOTS * 4)
        for i in range(NUM_SLOTS):
            pv, = struct.unpack_from("<I", raw, i * 4)
            slots.append("0x%08X" % pv)
        res["measured"]["vtable"] = {
            "va": "0x%08X" % vtable_va, "slot_count": NUM_SLOTS, "slots": slots,
            "slot17_plus0x44": slots[17], "slot27_plus0x6c": slots[27],
            "slot16_plus0x40": slots[16], "slot18_plus0x48": slots[18],
        }

        # 3. historical anchor re-pin: slot 17 == 0x007B5390
        slot17 = int(slots[17], 16)
        res["measured"]["historical_anchor_repin"] = {
            "claim": "NINODE_SLOT17: Entropia NiNode vtable slot 17 (+0x44) = 0x007B5390 "
                     "(GetObjByName-like recursive named-object lookup)",
            "expected_slot17": "0x%08X" % NINODE_SLOT17_EXPECTED,
            "actual_slot17": slots[17],
            "match": slot17 == NINODE_SLOT17_EXPECTED,
        }
        # byte check: 0x007B5390 prologue (push ebx; mov ebx,[esp+8]; push edi; push ebx...)
        p = read_va(data, info, NINODE_SLOT17_EXPECTED, 12)
        res["measured"]["historical_anchor_repin"]["slot17_function_bytes_12"] = p.hex(" ")

        # 4. UpdateWorldData probe: slot 27 function first 80 bytes - find rep movsd (F3 A5)
        slot27 = int(slots[27], 16)
        body = read_va(data, info, slot27, 160)
        rep_movsd_offsets = []
        for i in range(len(body) - 1):
            if body[i] == 0xF3 and body[i + 1] == 0xA5:
                rep_movsd_offsets.append(i)
        # count consecutive rep movsd (x13 expected)
        consec = 0
        for i in range(len(body) - 1):
            if body[i] == 0xF3 and body[i + 1] == 0xA5:
                j = i
                c = 0
                while j + 1 < len(body) and body[j] == 0xF3 and body[j + 1] == 0xA5:
                    c += 1
                    j += 2
                consec = max(consec, c)
        res["measured"]["update_world_data_probe"] = {
            "slot27_va": "0x%08X" % slot27,
            "first_24_bytes": body[:24].hex(" "),
            "rep_movsd_offsets_in_160B": rep_movsd_offsets,
            "max_consecutive_rep_movsd": consec,
            "expected_fingerprint": "rep movsd x13 copying 52-byte NiTransform "
                                    "m_kLocal(+0x38) -> m_kWorld(+0x6C)",
        }
        res["interpreted"]["update_world_data_fingerprint_present"] = bool(consec >= 10)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("C12 written:", OUT)
    print("vtable:", res["measured"].get("vtable", {}).get("va"))
    print("slot17:", res["measured"].get("vtable", {}).get("slot17_plus0x44"),
          "match:", res["measured"].get("historical_anchor_repin", {}).get("match"))
    print("slot27:", res["measured"].get("vtable", {}).get("slot27_plus0x6c"))
    print("uwd fingerprint:", res["interpreted"].get("update_world_data_fingerprint_present"))
    print("errors:", res["errors"])


if __name__ == "__main__":
    main()
