#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC-R2 TOOL 2 (fresh QC worker, round 2; own PE32 parser; NO code shared with
the executor's 03_SCRIPTS or round-1's qc_tools):

BYTE-FACT SPOT-CHECKS against the pinned Entropia.exe
(E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8,015,872 B)
— the PE-MASTER-adjudicated facts behind the AMEND-R1 C1 wording, verified
independently here:

  F1. bytes at VA 0x70E4AD == 68 58 68 A8 00   (PUSH 0xA86858 — "textures")
  F2. byte  at VA 0x70E4AC == 50                (PUSH EAX; round-1 probe VA was one byte early)
  F3. ASCII "textures" + NUL at VA 0xA86858
  F4. ASCII "EnvironmentZones" + NUL at VA 0xA9808C
  F5. EnvironmentZones code reference (C1 text says "sole code ref @0x958DCE"):
      F5a bytes at 0x958DCE == 8C 80 A9 00 (the imm32 of the PUSH; round-1/QC4 cited
          this VA — it is the OPERAND address, not the instruction address)
      F5b bytes at 0x958DCD == 68 8C 80 A9 00 (the actual PUSH 0xA9808C instruction)
      F5c whole-.text census of PUSH pattern 68 8C 80 A9 00 == exactly 1 site
          ("sole code ref" TRUE; instruction VA = 0x958DCD)
      F5d whole-.text census of raw imm32 pattern 8C 80 A9 00 == exactly 1 site
  F6. PUSH ".vfs"(0xA86820) @0x70C40E == 68 20 68 A8 00 (FUN_0070c680 pin, C1 text)
  F7. MOV EAX,[ECX+8] @0x70C3FC == 8B 41 08     (FUN_0070c680 pin, C1 text)
  F8. MOV [ESI+0x84],EAX @0x70C71E == 89 86 84 00 00 00 (reader store; base
      register is ESI per the package's own CLIENT_READ_BYTES.json pin 0x70C71E)
  F9. CALL rel32 @0x70E866 -> FUN_0070e470      (C1 text)
  F10. CALL rel32 @0x70E8B6 -> FUN_00972df0     (open call, C1 text)
  F11. CALL rel32 @0x70C742 -> FUN_00972df0     (FUN_0070c680 open pin, C1 text)
  F12. whole-.text E8 census of calls to FUN_0040e900 (itoa): exactly 5 sites,
       NONE inside [0x70E810, 0x70E928] (C1 text: "exactly 5 call sites ...
       NONE inside FUN_0070E810's window")
  F13. hex window 0x70E4A0..0x70E4C0 dumped for the instruction-boundary record
"""
import hashlib
import json
import os
import struct

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
ROOT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"


def parse_pe(data):
    if data[:2] != b"MZ":
        raise ValueError("no MZ")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        raise ValueError("no PE sig")
    coff = e_lfanew + 4
    machine, num_sections, _ts, _psym, _nsym, opt_size, characteristics = struct.unpack_from(
        "<HHIIIHH", data, coff)
    opt = coff + 20
    magic = struct.unpack_from("<H", data, opt)[0]
    if magic != 0x10B:
        raise ValueError("not PE32: magic=%#x" % magic)
    image_base = struct.unpack_from("<I", data, opt + 28)[0]
    sect_align = struct.unpack_from("<I", data, opt + 32)[0]
    file_align = struct.unpack_from("<I", data, opt + 36)[0]
    sections = []
    soff = opt + opt_size
    for i in range(num_sections):
        name = data[soff:soff + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, soff + 8)
        sections.append({"name": name, "vsize": vsize, "vaddr": vaddr,
                         "rawsize": rawsize, "rawptr": rawptr})
        soff += 40
    return {"machine": machine, "image_base": image_base, "sections": sections,
            "section_alignment": sect_align, "file_alignment": file_align}


def va_to_fo(pe, va):
    rva = va - pe["image_base"]
    for s in pe["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            if rva - s["vaddr"] >= s["rawsize"]:
                raise ValueError("VA %#x in section %s but beyond raw data" % (va, s["name"]))
            return s["vaddr"] and (rva - s["vaddr"] + s["rawptr"])
    raise ValueError("VA %#x in no section" % va)


def rd(pe, data, va, n):
    fo = va_to_fo(pe, va)
    return data[fo:fo + n]


def hexs(b):
    return " ".join("%02X" % c for c in b)


def main():
    with open(EXE, "rb") as fh:
        data = fh.read()
    identity = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()}
    pe = parse_pe(data)
    out = {"tool": "q2r2_bytefacts.py", "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
           "qc_round": 2, "exe_identity": identity,
           "pe": {"machine": "%#x" % pe["machine"], "image_base": "%#x" % pe["image_base"],
                  "section_alignment": pe["section_alignment"], "file_alignment": pe["file_alignment"],
                  "sections": pe["sections"]},
           "checks": {}, "windows": {}}

    ok = True
    checks = out["checks"]

    # F1/F2: PUSH 0xA86858 at 0x70E4AD; PUSH EAX (50) at 0x70E4AC
    b_ad = rd(pe, data, 0x70E4AD, 5)
    b_ac = rd(pe, data, 0x70E4AC, 1)
    checks["F1_bytes_at_0x70E4AD"] = {"expected": "68 58 68 A8 00", "got": hexs(b_ad),
                                      "pass": b_ad == bytes.fromhex("68 58 68 A8 00")}
    checks["F2_byte_at_0x70E4AC"] = {"expected": "50", "got": hexs(b_ac), "pass": b_ac == b"\x50"}
    # the imm32 of the PUSH: LE 58 68 A8 00 == 0xA86858
    checks["F1b_imm32_decode"] = {"value": "%#x" % struct.unpack("<I", b_ad[1:5])[0],
                                  "pass": struct.unpack("<I", b_ad[1:5])[0] == 0xA86858}

    # F3/F4: strings
    s_tex = rd(pe, data, 0xA86858, 16)
    s_ez = rd(pe, data, 0xA9808C, 24)
    checks["F3_string_at_0xA86858"] = {"expected_prefix": "textures", "got": s_tex.split(b"\x00")[0].decode("ascii", "replace"),
                                       "raw": hexs(s_tex[:12]),
                                       "pass": s_tex.startswith(b"textures\x00")}
    checks["F4_string_at_0xA9808C"] = {"expected_prefix": "EnvironmentZones",
                                       "got": s_ez.split(b"\x00")[0].decode("ascii", "replace"),
                                       "raw": hexs(s_ez[:20]),
                                       "pass": s_ez.startswith(b"EnvironmentZones\x00")}

    # F5a/F5b: EnvironmentZones code reference bytes
    b_imm = rd(pe, data, 0x958DCE, 4)
    b_ins = rd(pe, data, 0x958DCD, 5)
    checks["F5a_imm32_at_0x958DCE"] = {"expected": "8C 80 A9 00", "got": hexs(b_imm),
                                       "pass": b_imm == bytes.fromhex("8C 80 A9 00"),
                                       "note": "round-1 QC4 cited this OPERAND VA as the ref VA"}
    checks["F5b_push_at_0x958DCD"] = {"expected": "68 8C 80 A9 00", "got": hexs(b_ins),
                                      "pass": b_ins == bytes.fromhex("68 8C 80 A9 00"),
                                      "note": "the actual PUSH 0xA9808C instruction (one byte earlier than 0x958DCE)"}

    # F6: PUSH ".vfs" 0xA86820 @0x70C40E
    b = rd(pe, data, 0x70C40E, 5)
    checks["F6_push_.vfs_at_0x70C40E"] = {"expected": "68 20 68 A8 00", "got": hexs(b),
                                          "pass": b == bytes.fromhex("68 20 68 A8 00")}

    # F7: MOV EAX,[ECX+8] @0x70C3FC
    b = rd(pe, data, 0x70C3FC, 3)
    checks["F7_mov_eax_ecx8_at_0x70C3FC"] = {"expected": "8B 41 08", "got": hexs(b),
                                             "pass": b == bytes.fromhex("8B 41 08")}

    # F8: MOV [ESI+0x84],EAX @0x70C71E (base register ESI — per the package's own
    # CLIENT_READ_BYTES.json pin: original_bytes_hex 898684000000, claim
    # "MOV dword [ESI+0x84],EAX - store the 20002.vfs VFS reader on the class object")
    b = rd(pe, data, 0x70C71E, 6)
    checks["F8_mov_esi84_eax_at_0x70C71E"] = {"expected": "89 86 84 00 00 00", "got": hexs(b),
                                              "pass": b == bytes.fromhex("89 86 84 00 00 00"),
                                              "note": "matches the package pin (ESI base); disp32 == +0x84 as claimed"}

    # F9/F10/F11: E8 rel32 call targets
    for tag, va, target in (("F9_call_0x70E470_at_0x70E866", 0x70E866, 0x70E470),
                            ("F10_call_0x972DF0_at_0x70E8B6", 0x70E8B6, 0x972DF0),
                            ("F11_call_0x972DF0_at_0x70C742", 0x70C742, 0x972DF0)):
        b = rd(pe, data, va, 5)
        tgt = va + 5 + struct.unpack("<i", b[1:5])[0]
        checks[tag] = {"bytes": hexs(b), "decoded_target": "%#x" % tgt,
                       "pass": b[0] == 0xE8 and tgt == target}

    # F12: whole-.text E8 census of calls to FUN_0040e900
    text = None
    for s in pe["sections"]:
        if s["name"] == ".text":
            text = s
            break
    sites = []
    raw = data[text["rawptr"]:text["rawptr"] + text["rawsize"]]
    for i in range(len(raw) - 5):
        if raw[i] == 0xE8:
            site_va = pe["image_base"] + text["vaddr"] + i
            tgt = site_va + 5 + struct.unpack_from("<i", raw, i + 1)[0]
            if tgt == 0x40E900:
                sites.append(site_va)
    in_window = [hex(s) for s in sites if 0x70E810 <= s <= 0x70E928]
    checks["F12_itoa_FUN_0040e900_call_census"] = {
        "text_section": {"vaddr": "%#x" % text["vaddr"], "rawsize": text["rawsize"]},
        "expected_site_count": 5, "got_site_count": len(sites),
        "sites": ["%#x" % s for s in sites],
        "expected_in_window_0x70E810_0x70E928": 0, "got_in_window": in_window,
        "pass": len(sites) == 5 and not in_window}

    # F13: window dump 0x70E4A0..0x70E4C0 (instruction-boundary record)
    w = rd(pe, data, 0x70E4A0, 33)
    out["windows"]["0x70E4A0..0x70E4C0"] = hexs(w)

    # F5c/F5d: EnvironmentZones sole-code-ref censuses (whole .text)
    pat_ins = bytes.fromhex("68 8C 80 A9 00")
    ins_sites = []
    pat_imm = bytes.fromhex("8C 80 A9 00")
    imm_sites = []
    for i in range(len(raw) - 5):
        if raw[i:i + 5] == pat_ins:
            ins_sites.append(pe["image_base"] + text["vaddr"] + i)
        if raw[i:i + 4] == pat_imm:
            imm_sites.append(pe["image_base"] + text["vaddr"] + i)
    checks["F5c_push_pattern_census"] = {"pattern": "68 8C 80 A9 00",
                                         "sites": ["%#x" % s for s in ins_sites],
                                         "expected_count": 1,
                                         "pass": len(ins_sites) == 1 and ins_sites[0] == 0x958DCD,
                                         "note": "'sole code ref' claim of C1 text is TRUE; instruction VA 0x958DCD"}
    checks["F5d_imm32_pattern_census"] = {"pattern": "8C 80 A9 00",
                                         "sites": ["%#x" % s for s in imm_sites],
                                         "expected_count": 1,
                                         "pass": len(imm_sites) == 1 and imm_sites[0] == 0x958DCE}

    # F15: sole-PUSH census for "textures" (C1: "the PUSH imm32 0xA86858 is at 0x70E4AD")
    pat_tex = bytes.fromhex("68 58 68 A8 00")
    tex_sites = [pe["image_base"] + text["vaddr"] + i
                 for i in range(len(raw) - 5) if raw[i:i + 5] == pat_tex]
    checks["F15_push_0xA86858_census"] = {"pattern": "68 58 68 A8 00",
                                          "sites": ["%#x" % s for s in tex_sites],
                                          "expected_count": 1,
                                          "pass": len(tex_sites) == 1 and tex_sites[0] == 0x70E4AD}

    # F16: PUSH ".vfs" (0xA86820) census (observation; the two sites cited in the
    # package's texts (0x70C40E, 0x70E886) must be present; more sites are expected
    # because several VFS-loader families share the ".vfs" string — no "sole" claim exists)
    pat_vfs = bytes.fromhex("68 20 68 A8 00")
    vfs_sites = [pe["image_base"] + text["vaddr"] + i
                 for i in range(len(raw) - 5) if raw[i:i + 5] == pat_vfs]
    checks["F16_push_.vfs_census"] = {"pattern": "68 20 68 A8 00",
                                     "sites": ["%#x" % s for s in vfs_sites],
                                     "cited_sites_present": [s in vfs_sites for s in (0x70C40E, 0x70E886)],
                                     "pass": 0x70C40E in vfs_sites and 0x70E886 in vfs_sites}

    # F17/F18: the {1,0x80,8} open-params MOV stores cited by the old item-6 text
    # and the JOIN R1 pin (C7 44 24 1C 80 00 00 00 @0x70E841, 8-byte instruction)
    b17 = rd(pe, data, 0x70E839, 8)
    b18 = rd(pe, data, 0x70E841, 8)
    checks["F17_mov_esp18_1_at_0x70E839"] = {"expected": "C7 44 24 18 01 00 00 00", "got": hexs(b17),
                                            "pass": b17 == bytes.fromhex("C7 44 24 18 01 00 00 00")}
    checks["F18_mov_esp1c_80_at_0x70E841"] = {"expected": "C7 44 24 1C 80 00 00 00", "got": hexs(b18),
                                              "pass": b18 == bytes.fromhex("C7 44 24 1C 80 00 00 00"),
                                              "note": "JOIN R1's 6-byte 'C7 44 24 1C 80 00' citation was a truncated transcription of this 8-byte MOV (round-1 QC4b already noted this)"}

    # per-round-1 revalidation predicate residue: DECOMP_FUN_0070e810.txt contains "textures"
    decomp = os.path.join(ROOT, "01_RAW", "GHIDRA_ROUTING", "DECOMP_FUN_0070e810.txt")
    with open(decomp, "r", encoding="utf-8", errors="replace") as fh:
        decomp_text = fh.read()
    p4 = os.path.join(ROOT, "01_RAW", "GHIDRA_ROUTING", "PASS4_DECOMP_FUN_0070e470.txt")
    with open(p4, "r", encoding="utf-8", errors="replace") as fh:
        p4_text = fh.read()
    checks["F14_round1_predicate_clause4_observation"] = {
        "decomp_FUN_0070e810_contains_textures": "textures" in decomp_text,
        "PASS4_DECOMP_FUN_0070e470_contains_textures": "textures" in p4_text,
        "round1_clause4_verdict": "FALSE_AS_WORDED",
        "note": "round-1 P2-1 predicate clause 4 said DECOMP_FUN_0070e810.txt contains "
                "'textures' and '(All four verified true by QC)'. The literal lives in "
                "PASS4_DECOMP_FUN_0070e470.txt (line 45) + the .rdata string + the byte pins; "
                "DECOMP/DISASM_FUN_0070e810.txt show the FUN_0070e470 call, '.vfs' concat "
                "(DAT_00a86820) and {1,0x80,8} stores, with NO itoa call. Observation only; "
                "recorded for the round-1 report's historical record.",
        "observed": True}

    ok = all(c.get("pass", True) for c in checks.values())
    out["OVERALL_PASS"] = ok

    path = os.path.join(ROOT, "04_QC", "QC_R2_BYTEFACTS_RESULT.json")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({"exe_identity": identity, "checks": checks,
                      "window_70E4A0": out["windows"]["0x70E4A0..0x70E4C0"],
                      "OVERALL_PASS": ok}, indent=1))


if __name__ == "__main__":
    main()
