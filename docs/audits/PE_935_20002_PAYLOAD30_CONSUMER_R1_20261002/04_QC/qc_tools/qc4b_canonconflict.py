#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC COUNTERCHECK 4b - follow-up probes for the canon-conflict question:
  A. FUN_0070e470's "textures" literal: locate the referenced string VA inside
     FUN_0070e470's body (PUSH imm32 pointing at a 'textures\\0' string) - proves
     FUN_0070e810's filename part A = 'textures' from raw bytes (no Ghidra).
  B. Call edges: callers of FUN_0094b9e0 (filename part A 'EnvironmentZones'),
     callers of FUN_0094e470 (family driver's driver), callers of FUN_0094e390.
  C. JOIN R1 claim-5 pins re-verified from bytes:
     - 83 42 04 58 @0x94D9F5 (ADD dword [EDX+4],0x58 - the 0x58-B array append)
     - the pinned window @0x70E841 (already measured: C7 44 24 1C 80 00 00 00)
  D. "Data\\Parameters" style strings in the binary + code refs near the family.
"""
import struct
import json
import os
import sys

sys.dont_write_bytecode = True

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
OUT = os.path.join(PKG, "04_QC", "QC4B_CANONCONFLICT_PROBE.json")

exe = open(EXE, "rb").read()
e_lfanew, = struct.unpack_from("<I", exe, 0x3C)
opt_size, = struct.unpack_from("<H", exe, e_lfanew + 20)
nsec, = struct.unpack_from("<H", exe, e_lfanew + 6)
image_base, = struct.unpack_from("<I", exe, e_lfanew + 24 + 28)
secs = []
for i in range(nsec):
    off = e_lfanew + 24 + opt_size + i * 40
    name = exe[off:off + 8].rstrip(b"\x00").decode("latin-1")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<4I", exe, off + 8)
    secs.append((name, vaddr, rawsize, rawptr))
TEXT = next(s for s in secs if s[0] == ".text")

def va2fo(va):
    rva = va - image_base
    for name, vaddr, rawsize, rawptr in secs:
        if vaddr <= rva < vaddr + rawsize:
            return rawptr + (rva - vaddr)
    return None

def fo2va(fo):
    for name, vaddr, rawsize, rawptr in secs:
        if rawptr <= fo < rawptr + rawsize:
            return image_base + vaddr + (fo - rawptr), name
    return None, None

def call_sites(target_va, lo_va=None, hi_va=None):
    sites = []
    lo = va2fo(lo_va) if lo_va else TEXT[3]
    if hi_va is not None:
        hi = va2fo(hi_va) - 5
    else:
        hi = TEXT[3] + TEXT[2] - 5
    i = lo
    while i <= hi:
        if exe[i] == 0xE8:
            rel = struct.unpack_from("<i", exe, i + 1)[0]
            va_here = fo2va(i)[0]
            tgt = va_here + 5 + rel
            if tgt == target_va:
                sites.append({"site_va": "0x%X" % va_here})
        i += 1
    return sites

def imm32_refs_to_string(string_bytes, search_va_range=None):
    """Find code sites that PUSH/IMM32 a pointer to the given string."""
    hits = []
    start = 0
    str_vas = []
    while True:
        i = exe.find(string_bytes, start)
        if i < 0:
            break
        va, sec = fo2va(i)
        if va:
            str_vas.append((va, sec, i))
        start = i + 1
    for va, sec, fo in str_vas:
        needle = struct.pack("<I", va)
        lo = TEXT[3]
        hi = TEXT[3] + TEXT[2] - 4
        j = lo
        while j <= hi:
            if exe[j:j + 4] == needle:
                code_va = fo2va(j)[0]
                if search_va_range:
                    if not (search_va_range[0] <= code_va < search_va_range[1]):
                        j += 1
                        continue
                hits.append({"string": string_bytes.decode("latin-1"), "string_va": "0x%X" % va,
                             "string_section": sec, "code_ref_va": "0x%X" % code_va,
                             "ref_bytes_ctx": exe[va2fo(code_va) - 2:va2fo(code_va) + 8].hex().upper()})
            j += 1
    return hits, str_vas

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "countercheck": "QC4b canon-conflict probe",
          "tool": "04_QC/qc_tools/qc4b_canonconflict.py"}

# A. 'textures' literal referenced from FUN_0070e470's body (0x70E470..0x70E4B0)
tex_refs, tex_str_vas = imm32_refs_to_string(b"textures\x00", search_va_range=(0x70E470, 0x70E4C0))
result["A_textures_literal_in_FUN_0070e470"] = {
    "refs_within_70E470_70E4C0": tex_refs,
    "note": "if non-empty, FUN_0070e470 constructs 'textures' (byte-proven), hence FUN_0070e810 (which calls FUN_0070e470 at 0x70E866) builds a 'textures....vfs' filename",
}

# B. family edges
result["B_family_edges"] = {
    "callers_of_FUN_0094b9e0": call_sites(0x94B9E0),
    "callers_of_FUN_0094e470": call_sites(0x94E470),
    "callers_of_FUN_0094e390": call_sites(0x94E390),
    "callers_of_FUN_004172A0": call_sites(0x4172A0),
}

# C. JOIN R1 claim-5 pins
fo = va2fo(0x94D9F5)
result["C_join_r1_pins"] = {
    "at_0x94D9F5_measured": exe[fo:fo + 3].hex().upper(),
    "at_0x94D9F5_expected_join_r1": "834204 58 (83 42 04 58 = ADD dword [EDX+4],0x58)",
    "pin_ok": exe[fo:fo + 3].hex().upper() == "834204",
    "at_0x70E841_measured_8_bytes": exe[va2fo(0x70E841):va2fo(0x70E841) + 8].hex().upper(),
    "note": "JOIN R1 cited 'C7 44 24 1C 80 00' (6 bytes); the physical instruction is 8 bytes C7 44 24 1C 80 00 00 00 = MOV dword [ESP+0x1C],0x80 - same instruction, truncated transcription",
}

# D. 'EnvironmentZones' callers chain completeness + 'Data\\Parameters' strings
ez_refs, ez_vas = imm32_refs_to_string(b"EnvironmentZones\x00")
result["D_environmentzones_refs_all"] = ez_refs
# locate strings like 'Data\Parameters\' and 'Parameters\'
param_hits = []
for probe in (b"Data\\Parameters\\\x00", b"Parameters\\\x00", b"Parameters\\\templates.vfs\x00"):
    s = 0
    while True:
        i = exe.find(probe, s)
        if i < 0:
            break
        va, sec = fo2va(i)
        param_hits.append({"string": probe.decode("latin-1"), "va": ("0x%X" % va) if va else None,
                           "section": sec, "file_offset": i})
        s = i + 1
result["D_parameter_path_strings"] = param_hits[:40]

with open(OUT, "w") as f:
    json.dump(result, f, indent=1)
print("QC4B CANON CONFLICT PROBE")
print(json.dumps(result["A_textures_literal_in_FUN_0070e470"], indent=1))
print(json.dumps(result["B_family_edges"], indent=1))
print(json.dumps(result["C_join_r1_pins"], indent=1))
print("EnvironmentZones refs (all):", json.dumps(result["D_environmentzones_refs_all"], indent=1))
print("Parameters strings:", json.dumps(result["D_parameter_path_strings"][:12], indent=1))
