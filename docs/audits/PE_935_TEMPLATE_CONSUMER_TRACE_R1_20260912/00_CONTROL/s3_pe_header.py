#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_TEMPLATE_CONSUMER_TRACE_R1 - Stage 3: PE header ground truth for Entropia.exe (EU 9.3.5).

Pure-struct parse (no pefile dependency): DOS header, PE signature, COFF header,
optional header (PE32), section table. Emits the VA<->file-offset mapping used by
every later stage (all VAs cited in this run must derive through this mapping).

Outputs: 01_RAW\S3_PE_HEADER.json
"""
import hashlib
import json
import os
import struct
import sys

RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECTED_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

measured = {}
errors = []

with open(EXE, "rb") as f:
    data = f.read()

sha = hashlib.sha256(data).hexdigest().upper()
measured["sha256"] = sha
measured["file_size"] = len(data)
if sha != EXPECTED_SHA:
    errors.append("SHA mismatch: %s" % sha)
    print(json.dumps({"measured": measured, "errors": errors}, indent=2))
    sys.exit(2)

# DOS header
dos_magic, = struct.unpack_from("<H", data, 0)
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
measured["dos_magic"] = "%04X" % dos_magic
measured["e_lfanew"] = e_lfanew

# PE signature + COFF
pe_sig, = struct.unpack_from("<I", data, e_lfanew)
machine, num_sections, time_date, ptr_symtab, num_syms, size_opt, characteristics = struct.unpack_from(
    "<HHIIIHH", data, e_lfanew + 4)
measured["pe_signature"] = "%08X" % pe_sig
measured["machine"] = "%04X" % machine
measured["num_sections"] = num_sections
measured["time_date_stamp"] = time_date
measured["size_optional_header"] = size_opt
measured["characteristics"] = "%04X" % characteristics

# Optional header (PE32)
opt_off = e_lfanew + 4 + 20
opt_magic, = struct.unpack_from("<H", data, opt_off)
measured["optional_header_magic"] = "%04X" % opt_magic
major_link, minor_link, size_code, size_init, size_uninit, entry_rva, base_code, base_data = struct.unpack_from(
    "<BBIIIIII", data, opt_off + 2)
image_base, = struct.unpack_from("<I", data, opt_off + 28)
section_align, file_align = struct.unpack_from("<II", data, opt_off + 32)
dll_chars, = struct.unpack_from("<H", data, opt_off + 70)
num_rva_sizes, = struct.unpack_from("<I", data, opt_off + 92)
measured["linker_version"] = "%d.%d" % (major_link, minor_link)
measured["size_of_code"] = size_code
measured["entry_point_rva"] = "%08X" % entry_rva
measured["base_of_code_rva"] = "%08X" % base_code
measured["base_of_data_rva"] = "%08X" % base_data
measured["image_base"] = "%08X" % image_base
measured["section_alignment"] = section_align
measured["file_alignment"] = file_align
measured["dll_characteristics"] = "%04X" % dll_chars
measured["aslr_enabled"] = bool(dll_chars & 0x0040)
measured["num_rva_and_sizes"] = num_rva_sizes

# Section table
sec_off = opt_off + size_opt
sections = []
for i in range(num_sections):
    o = sec_off + i * 40
    name = data[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, o + 8)
    chars, = struct.unpack_from("<I", data, o + 36)
    sections.append({
        "name": name,
        "virtual_size": vsize, "virtual_address_rva": "%08X" % vaddr,
        "raw_size": rawsize, "raw_ptr": rawptr,
        "va_start": "%08X" % (image_base + vaddr),
        "va_end": "%08X" % (image_base + vaddr + max(vsize, rawsize)),
        "characteristics": "%08X" % chars,
    })
measured["sections"] = sections

# VA<->file offset mapping helper (recorded as data)
def va_to_file(va):
    rva = va - image_base
    for s in sections:
        vaddr = int(s["virtual_address_rva"], 16)
        vsize = max(s["virtual_size"], s["raw_size"])
        if vaddr <= rva < vaddr + vsize:
            delta = rva - vaddr
            fp = s["raw_ptr"] + delta if delta < s["raw_size"] else None
            return fp, s["name"]
    return None, None

# self-test: entry point
ep_fp, ep_sec = va_to_file(image_base + entry_rva)
measured["entry_va"] = "%08X" % (image_base + entry_rva)
measured["entry_file_offset"] = ep_fp
measured["entry_section"] = ep_sec
if ep_fp is None or ep_sec != ".text":
    errors.append("entry point mapping unexpected: %s" % ep_sec)

# spot checks for later use
checks = {
    "FUN_0094e470_from_CONT_R2": 0x0094e470,
    "DAT_00BA12F4_from_CONT_R2": 0x00BA12F4,
    "const_00A7AF88_from_CONT_R2": 0x00A7AF88,
}
spot = {}
for k, va in checks.items():
    fp, sec = va_to_file(va)
    spot[k] = {"va": "%08X" % va, "file_offset": fp, "section": sec}
measured["prior_lead_spot_checks"] = spot

# Data directories (first 16)
dirs = []
dd_off = opt_off + 96
names = ["Export", "Import", "Resource", "Exception", "Security", "Basereloc",
         "Debug", "Arch", "GlobalPtr", "TLS", "LoadConfig", "BoundImport", "IAT",
         "DelayImport", "CLR", "Reserved"]
for i in range(num_rva_sizes if num_rva_sizes < 16 else 16):
    rva, size = struct.unpack_from("<II", data, dd_off + i * 8)
    dirs.append({"name": names[i], "rva": "%08X" % rva, "size": size})
measured["data_directories"] = dirs

result = {"run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912", "stage": "S3_pe_header",
          "era": "EU 9.3.5 (pcg_install)", "measured": measured,
          "interpreted": {
              "mapping_rule": "VA = image_base + RVA; file_offset = section.raw_ptr + (RVA - section.virt_addr) "
                              "while (RVA - virt_addr) < raw_size. Every later VA citation must derive through this table.",
              "aslr_note": "dll_characteristics bit 0x40 (DYNAMIC_BASE) = %s - VA stability for static analysis."
                           % measured["aslr_enabled"],
          }, "errors": errors}
out = os.path.join(RUN_DIR, "01_RAW", "S3_PE_HEADER.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
if errors:
    sys.exit(1)
print("[S3] PE HEADER GROUND TRUTH OK")
