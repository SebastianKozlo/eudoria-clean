# -*- coding: utf-8 -*-
# F1 final pieces: RTTI of derived class vtables; string 0x00A7957B; ArkSurgeonObject
# ctor decode; third imm32 hit context; getter FUN_007CE1E0 caller census (receiver matrix).
# Output: 01_RAW/F1_RECEIVERS.json + F1_CTX3_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F1_receivers", "measured": {}, "errors": []}


def rtti_of_vtable(vt):
    col = pe.read_va32(vt - 4)
    if not col:
        return None
    td = pe.read_va32(col + 0xC)
    if not td:
        return None
    name_b = pe.read_va(td + 8, 96)
    if name_b is None:
        return None
    name = name_b[:name_b.find(b"\x00")].decode("ascii", "replace")
    return {"vtable": "0x%08X" % vt, "col": "0x%08X" % col, "td": "0x%08X" % td, "name": name}


res["measured"]["rtti_00A87034_class_of_DAT_00BA58CC"] = rtti_of_vtable(0x00A87034)

# string at 0x00A7957B
sb = pe.read_va(0x00A7957B, 64)
res["measured"]["string_00A7957B"] = {
    "hex": sb.hex(), "ascii": sb[:sb.find(b"\x00")].decode("ascii", "replace") if b"\x00" in sb else sb.decode("ascii", "replace")
}

# ArkSurgeonObject ctor FUN_007351E0: decode usage of DAT_00BA58CC + base ctor call
ob = pe.read_va(0x007351E0, 0x60)
res["measured"]["ctor_ArkSurgeonObject_007351E0_hex"] = ob.hex()

# third imm32 0x00A86850 hit 0x00516F0E — wide context
dump3 = pe.read_va(0x00516EC0, 0xC0)
res["measured"]["hit_00516F0E_wide_hex"] = dump3.hex()

# second ArkObjectClass vft store 0x0070D19A — context
dump4 = pe.read_va(0x0070D150, 0xC0)
res["measured"]["vtstore2_0070D19A_hex"] = dump4.hex()

# getter FUN_007CE1E0 direct caller census (raw E8 rel32)
sites = pe.calls_to(0x007CE1E0)
vas = ["0x%08X" % pe.text_off_to_va(o) for o in sites]
res["measured"]["getter_FUN_007CE1E0_direct_callers"] = {"count": len(sites), "call_sites": vas}

# getter D FUN_0048ADA0 direct callers (for F2 receiver contrast)
sites_d = pe.calls_to(0x0048ADA0)
vas_d = ["0x%08X" % pe.text_off_to_va(o) for o in sites_d]
res["measured"]["getterD_FUN_0048ADA0_direct_callers"] = {"count": len(sites_d), "call_sites": vas_d}

# function attribution for getter callers: nearest preceding CC CC CC
def func_start_off(va):
    off = pe.va_to_off(va)
    d = pe.data
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None

attr = []
for v in vas:
    st = func_start_off(int(v, 16))
    attr.append({"call_site": v, "func_start": ("0x%08X" % st) if st else None})
res["measured"]["getter_callers_attributed"] = attr

with open(os.path.join(OUT, "F1_RECEIVERS.json"), "w") as f:
    json.dump(res, f, indent=2)

def dump(name, va, n):
    with open(os.path.join(OUT, "F1_CTX3_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")

dump("CTOR_ARKSURGEON_007351E0", 0x007351E0, 0x60)
dump("HIT3_00516F0E", 0x00516EC0, 0xC0)
dump("VTSTORE2_0070D150", 0x0070D150, 0xC0)

print("rtti 0x00A87034:", res["measured"]["rtti_00A87034_class_of_DAT_00BA58CC"])
print("string 0x00A7957B:", res["measured"]["string_00A7957B"])
print("getter direct callers:", len(sites))
print("getterD direct callers:", len(sites_d))
