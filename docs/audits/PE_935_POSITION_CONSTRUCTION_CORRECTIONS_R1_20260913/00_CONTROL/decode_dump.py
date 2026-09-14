# -*- coding: utf-8 -*-
# PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 - primary decode dumper
# STATIC-ONLY. Dumps OWN capstone disassembly + hexdumps of all contract-relevant
# regions from the PHYSICAL EXE. Output: 01_RAW/F*_*.txt + hexdumps.
# This is the executor's primary decode layer (Desktop hexdumps NOT used here).

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
os.makedirs(RAW, exist_ok=True)

pe = core.PE(core.EXE_PATH)

# --- decode targets -----------------------------------------------------
# (label, entry_va, max_bytes) - body bounded by CC CC CC heuristic
FUNCTIONS = [
    ("F007343E0_STRUCTURE_MASK", 0x007343E0, 0x400),
    ("F007453D0_DESERIALIZER", 0x007453D0, 0x300),
    ("F007345C0_ZERO_INIT", 0x007345C0, 0x100),
    ("F004C32F0_READ_F32", 0x004C32F0, 0x100),
    ("F0040DE60_ADVANCE", 0x0040DE60, 0x100),
    ("F00412430_READ_VEC3", 0x00412430, 0x100),
    ("F004C46C0_CREATE", 0x004C46C0, 0x400),
    ("F004C47F0_PROCESSOR", 0x004C47F0, 0x400),
    ("F004154F0_MANAGER_GET", 0x004154F0, 0x100),
    ("F00853A80_Z_PROVIDER", 0x00853A80, 0x300),
    ("F00755F90_FILTER", 0x00755F90, 0x200),
    ("F00413340_SESI50", 0x00413340, 0x100),
    ("F0085B3E0_SET_POS_EXISTING", 0x0085B3E0, 0x100),
    ("F0085B750_GUARD", 0x0085B750, 0x100),
    ("F0085ADB0_ROTATION", 0x0085ADB0, 0x100),
    ("F00528E50_CTOR_MOBJ", 0x00528E50, 0x400),
    ("F005247C0_SUBC0_A", 0x005247C0, 0x200),
    ("F00509330_SUBC0_B", 0x00509330, 0x200),
    ("F00414130_KEY_LOOKUP", 0x00414130, 0x100),
    ("F004C4640_STR_SINGLETON", 0x004C4640, 0x100),
    ("F00765930_STR_PTR", 0x00765930, 0x100),
    ("F004124D0_ADJACENT", 0x004124D0, 0x100),
    ("F0085B6A0_SLOT3", 0x0085B6A0, 0x100),
]

index = []
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
    index.append({"label": label, "entry": hex(va),
                  "end_detected": hex(end_va) if end_va else None,
                  "size": len(body), "out": os.path.basename(out_path)})
    print("%-28s entry=%08X end=%s size=%d" %
          (label, va, hex(end_va) if end_va else "-", len(body)))

# --- hexdumps (pin windows) --------------------------------------------
HEXDUMPS = [
    ("X004C4770_479F_D1_WINDOW", 0x004C4770, 0x30),
    ("X004C4740_479F_VARIANT_CHAIN", 0x004C4740, 0x60),
    ("X004C4840_489B_EXISTING_CONDS", 0x004C4840, 0x5C),
    ("X007453E0_4560_CALLER_REGION", 0x007453E0, 0x180),
    ("X00853A80_53C0_PROVIDER_FULL", 0x00853A80, 0x180),
]
for label, va, n in HEXDUMPS:
    out_path = os.path.join(RAW, label + ".txt")
    with open(out_path, "w") as f:
        f.write("# OWN HEXDUMP from physical EXE (no derivative layer)\n")
        f.write("# window %08X..%08X\n" % (va, va + n - 1))
        f.write(core.hexdump_lines(pe, va, n) + "\n")
    index.append({"label": label, "window": "%08X..%08X" % (va, va + n - 1),
                  "out": os.path.basename(out_path)})
    print("hexdump %-28s %08X..%08X" % (label, va, va + n - 1))

with open(os.path.join(RAW, "DECODE_INDEX.json"), "w") as f:
    json.dump(index, f, indent=1)
print("DONE -> 01_RAW/DECODE_INDEX.json")
