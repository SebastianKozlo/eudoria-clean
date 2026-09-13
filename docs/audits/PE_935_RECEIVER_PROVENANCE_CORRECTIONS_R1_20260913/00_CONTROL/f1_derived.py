# -*- coding: utf-8 -*-
# F1 derived-class machinery: vtable 0x00A87034 slots (ArkObjectClassImpl<ArkSurgeonObject,20035>),
# vft 0x00A86E4C RTTI (ArkSurgeonObject), per-class factory @~0x0073AC45 (calls ctor 0x007351E0),
# callers of that factory; base-factory virtual dispatch scan (FF 5x 04 patterns near
# MOV ECX,[class-global]).
# Output: 01_RAW/F1_DERIVED.json + F1_CTX4_*.txt

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
res = {"stage": "F1_derived", "measured": {}, "errors": []}


def rtti_of_vtable(vt):
    col = pe.read_va32(vt - 4)
    if not col:
        return None
    td = pe.read_va32(col + 0xC)
    if not td:
        return None
    name_b = pe.read_va(td + 8, 128)
    if name_b is None:
        return None
    name = name_b[:name_b.find(b"\x00")].decode("ascii", "replace")
    return {"vtable": "0x%08X" % vt, "col": "0x%08X" % col, "td": "0x%08X" % td, "name": name}


# vtable slots of ArkObjectClassImpl<ArkSurgeonObject,20035>
vt = 0x00A87034
slots = []
for i in range(6):
    v = pe.read_va32(vt + i * 4)
    slots.append({"slot": i, "va": "0x%08X" % (vt + i * 4), "target": ("0x%08X" % v) if v else None})
res["measured"]["vtable_00A87034_slots"] = slots
res["measured"]["rtti_00A86E4C_ArkSurgeonObject"] = rtti_of_vtable(0x00A86E4C)
res["measured"]["rtti_00A87034"] = rtti_of_vtable(0x00A87034)

# dump slot1 target body (per-class factory)
s1 = pe.read_va32(vt + 4)
if s1:
    res["measured"]["slot1_target"] = "0x%08X" % s1
    with open(os.path.join(OUT, "F1_CTX4_FACTORY_IMPL.txt"), "w") as f:
        f.write("slot1 of 0x00A87034 = 0x%08X\n" % s1)
        f.write(hexdump(pe, s1, 0x60) + "\n")
    # census callers of that per-class factory
    callers = pe.calls_to(s1)
    res["measured"]["callers_of_slot1_factory"] = {
        "factory": "0x%08X" % s1, "count": len(callers),
        "call_sites": ["0x%08X" % pe.text_off_to_va(o) for o in callers]}

# per-class factory that calls ctor 0x007351E0 (@0x0073AC45) — full function
def func_start(va):
    off = pe.va_to_off(va)
    d = pe.data
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None

st = func_start(0x0073AC45)
res["measured"]["factory_calling_ctor_007351E0"] = {"call_site": "0x0073AC45", "func_start": ("0x%08X" % st) if st else None}
if st:
    with open(os.path.join(OUT, "F1_CTX4_FACTORY_ARKSURGEON.txt"), "w") as f:
        f.write("function containing CALL ctor ArkSurgeonObject @0x0073AC45: start 0x%08X\n" % st)
        f.write(hexdump(pe, st, 0x80) + "\n")
    # census callers of THAT factory function
    callers2 = pe.calls_to(st)
    res["measured"]["callers_of_arkSurgeon_factory"] = {
        "factory": "0x%08X" % st, "count": len(callers2),
        "call_sites": ["0x%08X" % pe.text_off_to_va(o) for o in callers2]}

# base-factory virtual dispatch: scan .text for "8B 0D CC 58 BA 00" (MOV ECX,[DAT_00BA58CC])
# then check nearby FF 50/52 04-style virtual create calls
tr = pe.text_raw
pat = bytes.fromhex("8b0dcc58ba00")
hits = []
i = 0
while True:
    j = tr.find(pat, i)
    if j < 0:
        break
    hits.append(pe.text_off_to_va(j))
    i = j + 1
res["measured"]["mov_ecx_DAT00BA58CC_sites"] = ["0x%08X" % h for h in hits]

# callers of accessor FUN_0073C970 (returns [DAT_00BA58CC])
callers3 = pe.calls_to(0x0073C970)
res["measured"]["callers_of_accessor_0073C970"] = {
    "count": len(callers3), "call_sites": ["0x%08X" % pe.text_off_to_va(o) for o in callers3]}

with open(os.path.join(OUT, "F1_DERIVED.json"), "w") as f:
    json.dump(res, f, indent=2)

print(json.dumps(res["measured"], indent=1)[:3000])
