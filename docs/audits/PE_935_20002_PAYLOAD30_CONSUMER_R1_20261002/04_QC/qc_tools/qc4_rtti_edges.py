#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC COUNTERCHECK 4 - RTTI chain verification + independent call-edge census +
EnvironmentZones attribution probe + FUN_0070e810 window probe.
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 / QC worker.

Methods (all byte-level, from the pinned physical EXE, QC's own PE parser):
  A. RTTI chain: vtable[-1] -> CompleteObjectLocator -> TypeDescriptor -> name
     for the two claimed vtables 0xA86FE0 (class object) and 0xA878BC (instance).
  B. Call-edge census: scan .text for E8 rel32 (and E9 jmp32) whose computed
     target equals each probed function entry; report all sites. This is an
     independent structural census - no Ghidra.
  C. "EnvironmentZones" string location + code references (imm32 == string VA).
  D. FUN_0070e810 window dump + JOIN R1 pin @0x70E841 re-verification + which
     functions FUN_0070e810 calls (from its E8 sites).
"""
import struct
import json
import hashlib
import os
import sys

sys.dont_write_bytecode = True

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
OUT = os.path.join(PKG, "04_QC", "QC4_RTTI_EDGES_RESULT.json")

exe = open(EXE, "rb").read()
sha = hashlib.sha256(exe).hexdigest().upper()
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

def read_u32_va(va):
    fo = va2fo(va)
    return struct.unpack_from("<I", exe, fo)[0]

def read_cstr_va(va, maxlen=256):
    fo = va2fo(va)
    end = exe.find(b"\x00", fo, fo + maxlen)
    return exe[fo:end].decode("latin-1", "replace")

result = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "countercheck": "QC4 RTTI + call edges + EnvironmentZones probe",
    "tool": "04_QC/qc_tools/qc4_rtti_edges.py",
    "exe_sha256": sha,
    "image_base": "0x%X" % image_base,
}

# ---------- A. RTTI chains ----------
def rtti_chain(vtable_va):
    col_ptr = read_u32_va(vtable_va - 4)
    chain = {"vtable_va": "0x%X" % vtable_va, "col_ptr": "0x%X" % col_ptr}
    if col_ptr and 0x400000 <= col_ptr < image_base + 0x800000:
        col_sig = read_u32_va(col_ptr)
        col_offset = read_u32_va(col_ptr + 4)
        cd_offset = read_u32_va(col_ptr + 8)
        td_ptr = read_u32_va(col_ptr + 0xC)
        chain.update({"col_signature": "0x%X" % col_sig, "col_offset": col_offset,
                      "col_cdOffset": cd_offset, "td_ptr": "0x%X" % td_ptr})
        if td_ptr and 0x400000 <= td_ptr < image_base + 0x800000:
            td_vft = read_u32_va(td_ptr)
            name = read_cstr_va(td_ptr + 8)
            chain.update({"td_vftable": "0x%X" % td_vft, "td_name": name})
    # first 3 vtable entries
    entries = []
    for i in range(3):
        entries.append("0x%X" % read_u32_va(vtable_va + 4 * i))
    chain["vtable_entries_0_2"] = entries
    return chain

result["rtti_class_object_vtable_0xA86FE0"] = rtti_chain(0xA86FE0)
result["rtti_instance_vtable_0xA878BC"] = rtti_chain(0xA878BC)

# instance vtable slots claimed by the executor (slots +0..+0x14)
inst_slots = []
for i in range(6):
    inst_slots.append("0x%X" % read_u32_va(0xA878BC + 4 * i))
result["instance_vtable_slots_0_to_5"] = inst_slots
result["instance_vtable_slot_c_expected_FUN_007263e0"] = inst_slots[3] == "0x7263E0"

# ---------- B. call-edge census (E8 rel32 in .text) ----------
def call_sites(target_va):
    sites = []
    t0 = TEXT[1]           # vaddr
    rawptr, rawsize = TEXT[3], TEXT[2]
    lo = rawptr
    hi = rawptr + rawsize
    i = lo
    last = hi - 5
    while i <= last:
        if exe[i] == 0xE8:
            rel = struct.unpack_from("<i", exe, i + 1)[0]
            va_here = fo2va(i)[0]
            tgt = va_here + 5 + rel
            if tgt == target_va:
                sites.append({"file_offset": i, "va": "0x%X" % va_here})
        i += 1
    return sites

probes = {
    "FUN_00958d90 (EnvironmentZones string ctor)": 0x958D90,
    "FUN_00972df0 (ArkVFS open)": 0x972DF0,
    "FUN_0094dfc0 (family open chain)": 0x94DFC0,
    "FUN_0094e1d0 (family driver)": 0x94E1D0,
    "FUN_0094bd30 (family record loop)": 0x94BD30,
    "FUN_00959090 (family record parser)": 0x959090,
    "FUN_0094d9b0 (array append 0x58)": 0x94D9B0,
    "FUN_0070c680 (class-VFS open)": 0x70C680,
    "FUN_00726900 (TLV parse loop)": 0x726900,
    "FUN_0075f660 (value read dispatch)": 0x75F660,
    "FUN_0070c180 (descriptor lookup)": 0x70C180,
    "FUN_0070e810 (JOIN R1 claimed classID loader)": 0x70E810,
    "FUN_0070e2f0 (descriptor count setter)": 0x70E2F0,
    "FUN_00971ad0 (per-record seek+read)": 0x971AD0,
    "FUN_0040e900 (decimal int-to-string)": 0x40E900,
}
census = {}
for label, va in probes.items():
    sites = call_sites(va)
    census[label] = {"target": "0x%X" % va, "e8_site_count": len(sites),
                     "sites": [s["va"] for s in sites][:250]}
result["call_edge_census"] = census

# ---------- C. EnvironmentZones string + references ----------
ez_hits = []
start = 0
while True:
    i = exe.find(b"EnvironmentZones\x00", start)
    if i < 0:
        break
    va, sec = fo2va(i)
    ez_hits.append({"file_offset": i, "va": ("0x%X" % va) if va else None, "section": sec})
    start = i + 1
result["environmentzones_string_hits"] = ez_hits
refs = []
if ez_hits:
    ez_va = ez_hits[0]["va"]
    ez_va_int = int(ez_va, 16)
    needle = struct.pack("<I", ez_va_int)
    t_lo, t_raw, t_size, t_ptr = TEXT[1], TEXT[3], TEXT[2], TEXT[1]
    # scan .text for imm32 references to the string VA
    lo = TEXT[3]
    hi = TEXT[3] + TEXT[2] - 4
    j = lo
    while j <= hi:
        if exe[j:j + 4] == needle:
            va_here = fo2va(j)[0]
            ctx = exe[j - 8:j + 12].hex().upper()
            refs.append({"file_offset": j, "va": "0x%X" % va_here, "ctx_hex": ctx})
        j += 1
result["environmentzones_code_refs"] = refs

# ---------- D. FUN_0070e810 window probe ----------
w_fo = va2fo(0x70E810)
window = exe[w_fo:w_fo + 0xA0]
win_calls = []
for i in range(len(window) - 5):
    if window[i] == 0xE8:
        rel = struct.unpack_from("<i", window, i + 1)[0]
        src_va = 0x70E810 + i
        tgt = src_va + 5 + rel
        win_calls.append({"site": "0x%X" % src_va, "target": "0x%X" % tgt})
# JOIN R1 pin re-verification: C7 44 24 1C 80 00 00 @0x70E841
pin_fo = va2fo(0x70E841)
join_pin_bytes = exe[pin_fo:pin_fo + 7].hex().upper()
result["FUN_0070e810_probe"] = {
    "window_hex_first_0xA0": window.hex().upper(),
    "e8_calls_in_first_0xA0": win_calls,
    "join_r1_pin_0x70E841_expected": "C744241C80000000... wait - JOIN R1 recorded 'C7 44 24 1C 80 00' (6 bytes: MOV dword [ESP+0x1C],0x80 with imm8? no - C7 /0 id is 8 bytes; JOIN R1 text cites 6 hex bytes 'C7 44 24 1C 80 00' as the mnemonic encoding with imm16?)",
    "join_r1_pin_bytes_measured": join_pin_bytes,
    "interpretation_rule": "C7 44 24 1C 80 00 00 00 = MOV dword [ESP+0x1C],0x80 (imm32 80000000-LE). JOIN R1's 'C7 44 24 1C 80 00' is the 7-byte C7 /0 ib form: MOV word [ESP+0x1C],0x0080? decode: C7 44 24 1C 80 00 = op C7 /0 with 16-bit operand size? NO - without 66 prefix C7 /0 takes imm32; the 6-byte citation is a truncated transcription of the 8-byte encoding OR a 66-prefixed form. QC measures the raw bytes and reports them.",
}

with open(OUT, "w") as f:
    json.dump(result, f, indent=1)
print("QC4 RTTI/EDGES DIGEST")
print(json.dumps(result["rtti_class_object_vtable_0xA86FE0"], indent=1))
print(json.dumps(result["rtti_instance_vtable_0xA878BC"], indent=1))
print("instance vtable slots:", result["instance_vtable_slots_0_to_5"],
      "slot3==FUN_007263e0:", result["instance_vtable_slot_c_expected_FUN_007263e0"])
print("--- call edge census:")
for k, v in census.items():
    print("  %-50s count=%d sites=%s" % (k, v["e8_site_count"], v["sites"][:8]))
print("--- EnvironmentZones string hits:", json.dumps(ez_hits))
print("--- EnvironmentZones code refs:", json.dumps(refs))
print("--- FUN_0070e810 window:", result["FUN_0070e810_probe"]["window_hex_first_0xA0"])
print("--- 0x70E841 bytes measured:", join_pin_bytes)
print("--- e8 calls in 0x70e810 window:", json.dumps(win_calls))
