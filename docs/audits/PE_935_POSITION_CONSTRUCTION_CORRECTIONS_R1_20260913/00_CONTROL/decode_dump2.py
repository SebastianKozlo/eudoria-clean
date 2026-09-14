# -*- coding: utf-8 -*-
# decode_dump2.py - second decode wave (F2/P2 support functions)
# STATIC-ONLY. Own capstone decode from the physical EXE.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
pe = core.PE(core.EXE_PATH)

FUNCTIONS = [
    ("F00413440_LOCK_ACQUIRE", 0x00413440, 0x60),
    ("F00413450_LOCK_RELEASE", 0x00413450, 0x60),
    ("F004134F0_LOCK_FAMILY", 0x004134F0, 0x100),
    ("F004123D0_CURSOR_FAMILY", 0x004123D0, 0x100),
    ("F00412B0_PARAMPAIR", 0x00412B0, 0x100),
    ("F008550C0_MANAGER_CTOR", 0x008550C0, 0x200),
    ("F008553D0_SELECTOR", 0x008553D0, 0x100),
    ("F008544D0_RESOLVER", 0x008544D0, 0x100),
    ("F00856190_INSERT", 0x00856190, 0x100),
    ("F00745360_REC_CTOR", 0x00745360, 0x100),
    ("F00730F60_PLACE_CTOR", 0x00730F60, 0x100),
    ("F00730F90_PLACE_POS", 0x00730F90, 0x100),
    ("F00730FB0_PLACE_ROT", 0x00730FB0, 0x100),
    ("F00730FD0_PLACE_PSET", 0x00730FD0, 0x100),
    ("F00797280_PLACE_X2", 0x00797280, 0x100),
    ("F006B22D0_MOBJ_UPDATE", 0x006B22D0, 0x200),
    ("F008E0110_REC_DTOR", 0x008E0110, 0x100),
    ("F00746560_CTOR_COPY", 0x00746560, 0x100),
]

for label, va, mx in FUNCTIONS:
    end_va, body = pe.func_body(va, maxb=mx)
    txt = pe.disasm_lines(va, len(body)) if body else "NO BYTES"
    out_path = os.path.join(RAW, label + ".txt")
    with open(out_path, "w") as f:
        f.write("# OWN DECODE (capstone x86-32) from physical EXE\n")
        f.write("# entry=%08X end_detected=%s size=%d\n" %
                (va, hex(end_va) if end_va else "None", len(body)))
        f.write("# file=%s\n" % core.EXE_PATH)
        f.write(txt + "\n")
    print("%-28s entry=%08X end=%s size=%d" %
          (label, va, hex(end_va) if end_va else "-", len(body)))
print("DONE")
