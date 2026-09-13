# -*- coding: utf-8 -*-
# F1 writer/caller context dumps: DAT_00BA58CC writer function, ArkObjectClass ctor
# callers (registration functions), third vtable imm32 hit, second ArkObject vft store,
# ArkSurgeonObject ctor FUN_007351E0 full body.
# Output: 01_RAW/F1_CTX_*.txt (hexdumps) + F1_CTX_INDEX.json

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
index = []

def dump(name, va, n):
    with open(os.path.join(OUT, "F1_CTX_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")
    index.append({"name": name, "va": "0x%08X" % va, "n": n})

# 1. third imm32 0x00A86850 hit (0x00516F0E) context
dump("HIT_00516F0E", 0x00516EC0, 0xC0)

# 2. second ArkObjectClass vft store (~0x0070D19A) — dump around it
dump("VTSTORE2_0070D190", 0x0070D150, 0xC0)

# 3. second ArkObject vft store (~0x00726F2A)
dump("VTSTORE_ARKOBJ_00726F2A", 0x00726EF0, 0xC0)

# 4. registration function containing ctor call @0x00739BCD (find start: scan back for CC CC CC)
def func_start(va):
    off = pe.va_to_off(va)
    d = pe.data
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None

for label, site in (("REG_00739BCD", 0x00739BCD),
                    ("REG_0073ED2D", 0x0073ED2D),
                    ("REG_007107F8", 0x007107F8),
                    ("REG_007262B7", 0x007262B7),
                    ("REG_0072AE7D", 0x0072AE7D),
                    ("REG_007621DA", 0x007621DA),
                    ("REG_0076240D", 0x0076240D)):
    st = func_start(site)
    if st:
        dump(label, st, min(0x140, site + 0x20 - st))

# 5. DAT_00BA58CC writer function (site 0x0073D882)
st = func_start(0x0073D882)
if st:
    dump("WRITER_DAT00BA58CC", st, 0x0073D940 - st)

# 6. ArkSurgeonObject ctor FUN_007351E0 full body
dump("CTOR_ARKSURGEONOBJECT_007351E0", 0x007351E0, 0x100)

# 7. getter accessor FUN containing 0x0073C970 (MOV EAX,[0x00BA58CC]; RET)
st2 = func_start(0x0073C970)
if st2:
    dump("GETTER_DAT00BA58CC_0073C970", st2, 0x30)

with open(os.path.join(OUT, "F1_CTX_INDEX.json"), "w") as f:
    json.dump({"regions": index}, f, indent=2)

print("F1_CTX done:", len(index), "regions")
for r in index:
    print("  %-28s 0x%08X +%d" % (r["name"], r["va"], r["n"]))
