# byte_windows.py - raw byte window dumps (own evidence, independent of Ghidra).
# Windows for the budgeted functions of the micro-run. Output: 01_RAW/BYTE_WINDOWS.txt

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe935k_core import Exe, hexs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_RAW")
os.makedirs(OUT, exist_ok=True)

WINDOWS = [
    ("F00401360_receiver_getter", 0x00401360, 0x80),
    ("F005247C0_edge1", 0x005247C0, 0xC0),
    ("F00509330_edge2_sfctor", 0x00509330, 0x140),
    ("F00856190_mapinsert_full", 0x00856190, 0x80),
    ("F00528E50_ctor_prologue", 0x00528E50, 0x60),
    ("F0085B1B0_basector_keystore", 0x0085B1F0, 0x40),
    ("W00459fd0_callsite", 0x0045A070, 0x50),
    # Record-repair F2 (internal QC PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006,
    # finding F2): the three windows cited by EDGE_LEDGER (E-E2-EXTRADATA/E-E2-REG/E-XD/E-GB2)
    # and FUNCTION_LEDGER (rows 4/7/8) were missing from BYTE_WINDOWS.txt; they are now
    # persisted here as regular script-generated windows (byte read from the pinned EXE).
    ("SF_ctor_tail", 0x00509470, 0x50),
    ("F0064B1E0_head", 0x0064B1E0, 0x30),
    ("F004157B0_head", 0x004157B0, 0x30),
]

ex = Exe()
lines = []
for name, va, size in WINDOWS:
    data = ex.read(va, size)
    lines.append("=== %s : VA 0x%08X..0x%08X ===" % (name, va, va + size - 1))
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        lines.append("0x%08X  %-48s  %s" % (va + i, hexs(chunk).ljust(48),
                                           "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)))
    lines.append("")

out = os.path.join(OUT, "BYTE_WINDOWS.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote %s (%d lines)" % (out, len(lines)))
