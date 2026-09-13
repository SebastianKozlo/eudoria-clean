#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_TEMPLATE_CONSUMER_TRACE_R1 - Stage 4b: file-based raw pattern scan -> VA list.

The Ghidra Memory.findBytes hex-pattern overload produced 0 hits (instrument defect,
diagnosed against direct file scan which found the patterns). This stage does the raw
scan on the physical file (read-only), maps file offsets -> VA via the S3 section
table, extracts the containing null-terminated string, and emits the hit table that
the Ghidra enrichment postscript (s5) consumes.

Outputs: 01_RAW\S4B_RAW_HITS.json
"""
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

with open(EXE, "rb") as f:
    data = f.read()

# S3 section table (recomputed here from the file - no cross-run citation)
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
num_sections, = struct.unpack_from("<H", data, e_lfanew + 6)
size_opt, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 4 + 20 + 28)
sections = []
sec_off = e_lfanew + 4 + 20 + size_opt
for i in range(num_sections):
    o = sec_off + i * 40
    name = data[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, o + 8)
    sections.append({"name": name, "vsize": vsize, "vaddr": vaddr,
                     "rawsize": rawsize, "rawptr": rawptr})


def file_off_to_va(off):
    for s in sections:
        if s["rawptr"] <= off < s["rawptr"] + s["rawsize"]:
            return image_base + s["vaddr"] + (off - s["rawptr"]), s["name"]
    return None, None


def containing_string(off):
    """Walk back to NUL, walk forward to NUL; return (start_off, bytes)."""
    start = off
    while start > 0 and data[start - 1] != 0:
        start -= 1
    end = off
    while end < len(data) and data[end] != 0:
        end += 1
    return start, data[start:end]


PATTERNS = [
    "ArkVFS02", "ArkVFS01", "ArkVFS",
    "templates.vfs", "hierarchy.vfs", "Parameters\\", ".vfs",
    "TerrainImageCache",
    ".nif", ".bvi", ".tdf", ".tga", ".jpg", ".dat", ".dds",
    ".tez", ".vcl", ".prt", ".amu", ".mp3", ".wav",
    "models.bnt", "volumes.bnt", "textures.bnt", "terrain.bnt",
    "Cache\\", "massive\\", "video\\",
    "models", "hierarchy", "templates",
]

hits = []
for pat in PATTERNS:
    pb = pat.encode("ascii")
    for m in re.finditer(re.escape(pb), data):
        off = m.start()
        va, sec = file_off_to_va(off)
        if va is None:
            continue  # outside mapped raw (should not happen for .rdata strings)
        s_off, s_bytes = containing_string(off)
        s_va, s_sec = file_off_to_va(s_off)
        hits.append({
            "pattern": pat,
            "file_offset": off,
            "va": "0x%08X" % va,
            "section": sec,
            "string_start_file_offset": s_off,
            "string_start_va": ("0x%08X" % s_va) if s_va else None,
            "containing_string": s_bytes.decode("ascii", "replace"),
        })

result = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "stage": "S4b_raw_hits",
    "era": "EU 9.3.5 (pcg_install)",
    "image_base": "0x%08X" % image_base,
    "sections": sections,
    "hit_count": len(hits),
    "hits": hits,
}
out = os.path.join(RUN_DIR, "01_RAW", "S4B_RAW_HITS.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

# compact summary per pattern
from collections import Counter
c = Counter(h["pattern"] for h in hits)
print(json.dumps(dict(c), indent=2))
print("\n=== KEY HITS (full paths + magic + extensions) ===")
for h in hits:
    if h["pattern"] in ("ArkVFS02", "ArkVFS01", "templates.vfs", "hierarchy.vfs", "TerrainImageCache") or \
       h["pattern"].startswith(".") and len(h["pattern"]) == 4:
        print("%-20s va=%-10s str=%r" % (h["pattern"], h["va"], h["containing_string"][:64]))
print("\n[S4b] %d hits -> %s" % (len(hits), out))
