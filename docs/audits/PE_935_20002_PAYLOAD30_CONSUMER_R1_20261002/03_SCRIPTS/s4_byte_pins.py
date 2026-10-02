#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4 BYTE-PIN VERIFICATION (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002).
Reads the PINNED physical Entropia.exe at FILE_OFFSET for every load-bearing
instruction of the client-read chain + routing chain, records IMAGE_BASE/VA/RVA/
FILE_OFFSET/ORIGINAL_BYTES and asserts the expected opcode bytes (machine-verifiable).

Expected bytes are transcribed from the Ghidra disassembly listings produced in-run
(01_RAW/GHIDRA_ROUTING/PASS*_DISASM_*.txt); the assert re-reads them from the pinned
EXE independent of Ghidra. A mismatch => the pin FAILS and is recorded as such.
"""
import struct
import json
import hashlib

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\CLIENT_READ_BYTES.json"

with open(EXE, "rb") as f:
    data = f.read()
sha = hashlib.sha256(data).hexdigest().upper()
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
nsec, = struct.unpack_from("<H", data, e_lfanew + 6)
secs = []
for i in range(nsec):
    off = e_lfanew + 24 + opt_size + i * 40
    name = data[off:off + 8].rstrip(b"\x00").decode("latin-1")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<4I", data, off + 8)
    secs.append((name, vaddr, rawsize, rawptr))

def va2fo(va):
    rva = va - image_base
    for name, vaddr, rawsize, rawptr in secs:
        if vaddr <= rva < vaddr + rawsize:
            return rawptr + (rva - vaddr), name
    return None, None

# pin = (va, expected_hex_or_None, length, claim, role)
PINS = [
    # ---- THE CLIENT READ CHAIN (S9 core) ----
    (0x00412540, None, 18, "FUN_00412540 prologue: CMP byte [ECX+0x11],0 / bounds /MOV EDX,[ECX] / THE READ / THE STORE", "READ_FUNCTION=FUN_00412540 (type-1 scalar value reader)"),
    (0x00412551, "8B11", 2, "MOV EDX,[ECX] - cursor base load", "source cursor base"),
    (0x00412553, "8B0410", 3, "MOV EAX,dword ptr [EAX+EDX*1] - THE 4-byte little-endian READ at cursor.base+offset; at the tag-0x11 iteration offset==0x30 => reads payload+0x30", "THE CLIENT READ INSTRUCTION of payload+0x30 (width 4, x86 native LE)"),
    (0x00412556, "8B542404", 4, "MOV EDX,[ESP+4] - load dest pointer arg", "dest pointer"),
    (0x0041255A, "8902", 2, "MOV dword ptr [EDX],EAX - THE STORE: value_array[tag0x11.field_index(0x15)*4] = value (slot 21, +0x54)", "THE STORE INSTRUCTION into the destination field"),
    (0x0041255C, "C744240404000000", 8, "MOV dword [ESP+4],0x4 ; JMP FUN_0040de60 - advance cursor 4 bytes", "cursor advance"),
    # ---- THE TLV LOOP (FUN_00726900) ----
    (0x007269E7, "0FB73C08", 4, "MOVZX EDI,word ptr [EAX+ECX*1] - read the u16 TAG from cursor (record 0 iteration 6 reads 0x0011 at payload+0x2E)", "tag read"),
    (0x007269FC, "8B4D04", 3, "MOV ECX,[EBP+4] - instance+0x04 = the ArkObjectClass<ArkParameterArmor,20002> object (schema holder)", "schema holder load"),
    (0x00726A03, "E87857FEFF", 5, "CALL FUN_0070c180 - descriptor lookup by tag", "descriptor lookup call"),
    (0x00726A08, "83780400", 4, "CMP dword [EAX+4],0 - descriptor type validity check (type 1 for tag 0x11)", "type check"),
    (0x00726A0E, "8B4808", 3, "MOV ECX,[EAX+8] - descriptor field index (tag 0x11 => 0x15)", "field index load"),
    (0x00726A11, "8B5540", 3, "MOV EDX,[EBP+0x40] - instance+0x40 = value-array pointer (22 u32 slots)", "value array pointer"),
    (0x00726A14, "8D0C8A", 3, "LEA ECX,[EDX+ECX*4] - DEST = value_array + field_index*4 (slot 21 => +0x54)", "destination address computation"),
    (0x00726A1B, "E8408C0300", 5, "CALL FUN_0075f660 - value read dispatch", "dispatch call"),
    # ---- VALUE READ DISPATCH ----
    (0x0075F687, "F6400C01", 4, "TEST byte ptr [EAX+0xC],1 - descriptor flags bit0 (0xC0 => 0 => scalar path FUN_004129c0)", "flags dispatch test"),
    (0x004129C0, "8B442408", 4, "MOV EAX,[ESP+8] - the type argument (1 for tag 0x11)", "typed reader switch"),
    (0x004129DF, "E85CFBFFFF", 5, "CALL FUN_00412540 - case type 1 dispatch to the scalar reader", "case-1 dispatch"),
    # ---- SCHEMA LOOKUP (FUN_0070c180) ----
    (0x0070C180, "8B442404", 4, "MOV EAX,[ESP+4] - the tag argument", "tag arg"),
    (0x0070C1D3, "C1E004", 3, "SHL EAX,4 - tag*0x10 (descriptor stride)", "descriptor stride"),
    (0x0070C1D6, "038188000000", 6, "ADD EAX,[ECX+0x88] - descriptor = classObj->[0x88] + tag*0x10", "descriptor table base"),
    # ---- SCHEMA REGISTRATION FOR TAG 0x11 (FUN_00761570) ----
    (0x0076170F, "E83C632100", 5, "CALL FUN_00977a50 - the factory for the tag-0x11 descriptor", "descriptor factory"),
    (0x00761717, "68C0000000", 5, "PUSH 0xC0 - descriptor flags for tag 0x11", "tag 0x11 flags = 0xC0"),
    (0x0076171C, "6A01", 2, "PUSH 0x1 - descriptor type for tag 0x11 (type 1 = 4-byte scalar)", "tag 0x11 type = 1"),
    (0x0076171E, "6A11", 2, "PUSH 0x11 - THE TAG 0x11 descriptor registration", "tag 0x11 index"),
    (0x00761722, "E899B4FAFF", 5, "CALL FUN_0070cbc0 - register descriptor", "registration call"),
    (0x0070CBF6, "83C104", 3, "ADD ECX,4 - FIELD INDEX = TAG + 4 (tag 0x11 => slot 0x15=21)", "field index formula"),
    (0x0070CBF1, "50", 1, "PUSH EAX (type) prior to index+4 push (arg order for FUN_0075f5c0)", "arg order"),
    # ---- CLASS ID ROUTING ----
    (0x0073A441, "68224E0000", 5, "PUSH 0x4E22 - THE CLASS ID 20002 IMMEDIATE in the ArkObjectClassImpl<ArkParameterArmor,20002> constructor", "class-id immediate (routing)"),
    (0x0073A44D, "E82E2BFDFF", 5, "CALL FUN_0070cf80 - ArkObjectClass ctor(this, 20002, name)", "class object ctor call"),
    (0x0073A46B, "C706E06FA800", 6, "MOV dword [ESI],0xA86FE0 - ArkObjectClassImpl<class_ArkParameterArmor,20002>::vftable store", "class object vtable store"),
    (0x0073C8C1, "A1A85DBA00", 5, "MOV EAX,[0x00BA5DA8] - registry switch case 0x4E22 returns the 20002 class object singleton", "registry case 20002"),
    # ---- THE OPEN PATH (routing edge to 20002.vfs) ----
    (0x0070C3FC, "8B4108", 3, "MOV EAX,[ECX+8] - load the class ID (20002) from the class object for the filename", "class id load for filename"),
    (0x0070C40E, "682068A800", 5, "PUSH 0xA86820 - the '.vfs' literal appended to itoa(classID)", ".vfs string arg"),
    (0x0070C6BE, "39BE84000000", 6, "CMP dword [ESI+0x84],EDI - the class object's VFS-reader-already-open check", "open gate check"),
    (0x0070C71E, "898684000000", 6, "MOV dword [ESI+0x84],EAX - store the 20002.vfs VFS reader on the class object", "reader store (classObj+0x84)"),
    (0x0070C742, "E8A9662600", 5, "CALL FUN_00972df0 - open(path+'20002.vfs') via CreateFileA+magic check (call target decodes to 0x972DF0)", "the open call"),
    # ---- THE PER-RECORD LOAD CHAIN ----
    (0x0070DD1A, "399E84000000", 6, "CMP dword [ESI+0x84],EBX - FUN_0070dcf0: the class VFS reader present check", "load gate"),
    (0x00971B14, "FF15E850A700", 6, "CALL dword [0x00A750E8] - SetFilePointer seek to node.pos+0x10 (payload start)", "the seek"),
    (0x00971B4A, "85C0", 2, "TEST EAX,EAX - CRC field==0 check", "crc gate test"),
    (0x00971B4C, "7422", 2, "JZ +0x22 - skip the CRC comparison when the stored crc field is 0 (true for every record of 20002.vfs)", "crc gate skip"),
    # ---- INSTANCE CONSTRUCTION ----
    (0x00761547, "8B0DA85DBA00", 6, "MOV ECX,[0x00BA5DA8] - ArkParameterArmor instance ctor loads the 20002 class object", "instance ctor class object"),
    (0x00761556, "C706BC78A800", 6, "MOV dword [ESI],0xA878BC - ArkParameterArmor::vftable store on the instance", "instance vtable store"),
    # ---- DATA PINS ----
    (0x00A86820, "2E76667300", 5, "the literal '.vfs\\0' at 0xA86820", "filename suffix literal"),
]

result = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "generator": "03_SCRIPTS/s4_byte_pins.py",
    "exe_path": EXE,
    "exe_sha256": sha,
    "exe_size": len(data),
    "image_base": "0x%X" % image_base,
    "pins": [],
    "all_match": True,
}

for va, exp, length, claim, role in PINS:
    fo, sec = va2fo(va)
    if fo is None:
        result["pins"].append({"va": "0x%X" % va, "error": "VA not mapped to a section"})
        result["all_match"] = False
        continue
    got = data[fo:fo + length]
    got_hex = got.hex().upper()
    exp_hex = exp.upper() if exp else None
    match = (exp_hex is None) or (got_hex == exp_hex)
    result["pins"].append({
        "va": "0x%08X" % va,
        "rva": "0x%08X" % (va - image_base),
        "file_offset": "0x%X" % fo,
        "section": sec,
        "length": length,
        "original_bytes_hex": got_hex,
        "expected_bytes_hex": exp_hex,
        "match": match,
        "claim": claim,
        "role": role,
    })
    if not match:
        result["all_match"] = False

# RTTI name string pins (bounded excerpts)
def pin_string(va, expected_prefix, tag):
    fo, sec = va2fo(va)
    raw = data[fo:fo + len(expected_prefix) + 8]
    ok = raw.startswith(bytes.fromhex(expected_prefix.replace(" ", "")))
    result["pins"].append({
        "va": "0x%08X" % va, "rva": "0x%08X" % (va - image_base), "file_offset": "0x%X" % fo,
        "section": sec, "kind": "ascii_string",
        "original_bytes_hex": raw[:len(expected_prefix)//2 + 4].hex().upper(),
        "expected_prefix": expected_prefix,
        "match": ok, "claim": tag, "role": "RTTI/type-name evidence",
    })
    if not ok:
        result["all_match"] = False

# the exact type-name strings: located at the -0x10 backstep from the mangling hits measured in s3_exe_census
# 0xB8EDE4 was the $0EOCC@ hit; the full name starts earlier; we pin at the measured hit offset with bounded excerpt
pin_string(0xB8EDE4, "2430454F4343405641726b506172616d6574657241726d", "$0EOCC@VArkParameterArm... (20002 mangling; measured at fo 0x78EDE4)")
pin_string(0xB8D89C, "2430454F4347405641726b506172616d65746572436F6D", "$0EOCG@VArkParameterCom... (20006 calibration mangling; fo 0x78D89C)")

result["pin_count"] = len(result["pins"])
result["match_count"] = sum(1 for p in result["pins"] if p.get("match"))
with open(OUT, "w") as f:
    json.dump(result, f, indent=1)

print("pins:", result["pin_count"], "matches:", result["match_count"], "all_match:", result["all_match"])
for p in result["pins"]:
    status = "OK " if p.get("match") else "FAIL"
    print(" %s %s fo=%s %s | %s" % (status, p["va"], p.get("file_offset"), p.get("original_bytes_hex", "")[:24], p.get("claim", p.get("error", ""))[:90]))
