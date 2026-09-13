# -*- coding: utf-8 -*-
# F1 — ABI reconstruction from raw bytes (independent decode).
# Chain: vtable 0x00A86850 -> COL -> TD (.?AVArkObjectClass@@) -> factory FUN_0070BF50
#        -> new(0x58) -> ctor ArkObject FUN_00726E70 -> getter FUN_007CE1E0 (+8)
#        -> store [obj+0x28]. Plus ctor ArkObjectClass FUN_0070CF80 (vft, [class+8]=EBP).
# Output: 01_RAW/F1_ABI_BYTES.json + 01_RAW/F1_HEX_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump, u32

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F1_abi_bytes", "measured": {}, "errors": []}


def region(name, va, n):
    b = pe.read_va(va, n)
    res["measured"][name] = {
        "va": "0x%08X" % va, "n": n, "hex": b.hex() if b else None,
        "file_offset": pe.va_to_off(va), "section": pe.section_of(va),
    }
    with open(os.path.join(OUT, "F1_HEX_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")
    return b


# --- 1. RTTI chain: vtable 0x00A86850 ---
VT = 0x00A86850
vt_bytes = region("VTABLE_00A86850", VT, 32)
slot0 = u32(vt_bytes, 0)
slot1 = u32(vt_bytes, 4)
res["measured"]["vtable_slots"] = {
    "va": "0x%08X" % VT, "slot0_0x00": "0x%08X" % slot0, "slot1_0x04": "0x%08X" % slot1,
}
if slot1 != 0x0070BF50:
    res["errors"].append("slot1 %08X != 0070BF50" % slot1)

# vtable-4 -> COL
col_ptr = pe.read_va32(VT - 4)
res["measured"]["vtable_minus4_COL_ptr"] = "0x%08X" % col_ptr if col_ptr else None
# COL+0 -> TD ptr (MSVC RTTICompleteObjectLocator: +0 signature, +4 offset, +8 ctorOffset,
# +0xC pTypeDescriptor, +0x10 pClassDescriptor)
td_from_col = pe.read_va32(col_ptr + 0xC) if col_ptr else None
col_sig = pe.read_va32(col_ptr) if col_ptr else None
res["measured"]["COL_fields"] = {
    "col_va": "0x%08X" % col_ptr,
    "signature": "0x%08X" % col_sig if col_sig else None,
    "pTypeDescriptor_col_plus_C": "0x%08X" % td_from_col if td_from_col else None,
    "class_hierarchy_col_plus_10": "0x%08X" % pe.read_va32(col_ptr + 0x10) if col_ptr else None,
    "self_ptr_col_plus_C_expected": None,
}
# TD dump: 0x00B8D068 expected; MSVC TypeDescriptor: +0 pVFTable, +4 spare, +8 name
td_va = td_from_col
td_bytes = region("TYPE_DESCRIPTOR_ArkObjectClass", td_va, 48)
td_name = td_bytes[0x08:td_bytes.find(b"\x00", 0x08)].decode("ascii", "replace")
res["measured"]["TD_name"] = {"td_va": "0x%08X" % td_va, "name": td_name}
if td_name != ".?AVArkObjectClass@@":
    res["errors"].append("TD name %r != .?AVArkObjectClass@@" % td_name)

# --- 2. Factory FUN_0070BF50 full body ---
FACT = 0x0070BF50
fend, fbody = pe.func_body(FACT, 0x100)
res["measured"]["factory_FUN_0070BF50"] = {
    "entry": "0x%08X" % FACT, "end": "0x%08X" % fend if fend else None,
    "size": len(fbody), "hex": fbody.hex(),
}
region("FACTORY_0070BF50", FACT, len(fbody) if len(fbody) < 0x100 else 0x100)

# --- 3. ctor ArkObjectClass FUN_0070CF80 full body ---
CTC = 0x0070CF80
cend, cbody = pe.func_body(CTC, 0x100)
res["measured"]["ctor_ArkObjectClass_FUN_0070CF80"] = {
    "entry": "0x%08X" % CTC, "end": "0x%08X" % cend if cend else None,
    "size": len(cbody), "hex": cbody.hex(),
}
region("CTOR_ARKOBJECTCLASS_0070CF80", CTC, len(cbody) if len(cbody) < 0x100 else 0x100)

# --- 4. ctor ArkObject FUN_00726E70 full body ---
OBJ = 0x00726E70
oend, obody = pe.func_body(OBJ, 0x100)
res["measured"]["ctor_ArkObject_FUN_00726E70"] = {
    "entry": "0x%08X" % OBJ, "end": "0x%08X" % oend if oend else None,
    "size": len(obody), "hex": obody.hex(),
}
region("CTOR_ARKOBJECT_00726E70", OBJ, len(obody) if len(obody) < 0x100 else 0x100)

# --- 5. getter FUN_007CE1E0 ---
GET = 0x007CE1E0
gb = pe.read_va(GET, 8)
res["measured"]["getter_FUN_007CE1E0"] = {"va": "0x%08X" % GET, "hex": gb.hex()}
region("GETTER_007CE1E0", GET, 8)
if gb.hex() != "8b4108c3" + gb[4:8].hex()[:8]:
    pass  # only first 4 bytes matter
if gb[:4].hex() != "8b4108c3":
    res["errors"].append("getter bytes %s != 8b4108c3" % gb[:4].hex())

# --- 6. contract pins: exact bytes at pinned VAs ---
pins = {
    # va, expected bytes (prefix), label
    0x0070BF96: (None, "factory CALL FUN_00726E70 site"),
    0x0070CFB6: ("c7065068a800", "ctor ArkObjectClass vft write MOV [ESI],0x00A86850"),
    0x0070CFC1: ("896e08", "ctor ArkObjectClass MOV [ESI+8],EBP"),
    0x00726EA1: ("c706486ba800", "ctor ArkObject vft write MOV [ESI],0x00A86B48"),
    0x00726EB7: (None, "ctor ArkObject CALL FUN_007CE1E0 site"),
    0x00726EBC: ("894628", "ctor ArkObject MOV [ESI+0x28],EAX"),
}
pin_res = {}
for va, (exp, label) in pins.items():
    b = pe.read_va(va, 16)
    rec = {"va": "0x%08X" % va, "label": label, "hex": b.hex() if b else None,
           "file_offset": pe.va_to_off(va)}
    if exp is not None:
        rec["expected_prefix"] = exp
        rec["prefix_match"] = (b.hex().startswith(exp)) if b else False
        if not rec["prefix_match"]:
            res["errors"].append("pin %s mismatch: %s" % (label, b.hex() if b else None))
    pin_res["0x%08X" % va] = rec
res["measured"]["contract_pins"] = pin_res

# CALL rel32 decode for the two CALL sites
for site, label in ((0x0070BF96, "factory_CALL_00726E70"), (0x00726EB7, "ctor_CALL_007CE1E0")):
    b = pe.read_va(site, 5)
    if b and b[0] == 0xE8:
        rel = struct.unpack("<i", b[1:5])[0]
        tgt = site + 5 + rel
        res["measured"][label] = {"site": "0x%08X" % site, "rel32": "0x%08X" % (rel & 0xFFFFFFFF),
                                  "target": "0x%08X" % tgt}
    else:
        res["errors"].append("%s: opcode %s != E8" % (label, b.hex() if b else None))

with open(os.path.join(OUT, "F1_ABI_BYTES.json"), "w") as f:
    json.dump(res, f, indent=2)

print("F1_ABI done; errors:", res["errors"])
for k in ("vtable_slots", "vtable_minus4_COL_ptr", "TD_name",
          "factory_CALL_00726E70", "ctor_CALL_007CE1E0"):
    print(k, "=", res["measured"].get(k))
