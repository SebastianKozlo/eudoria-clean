# -*- coding: utf-8 -*-
# QC final links: coincidence @0x00516F0E (mid-instruction imm32 0x00A86850),
# censuses imm32 (0x00A86850/0x00A86B48/0x00BA5D9C), f32-D sites FUN_00861390,
# slot-getters FUN_006C2840/006C2870 -> table 0x00A858B4 -> FUN_0043A550 -> lookup.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

# --- coincidence @0x00516F0E ---
R["hit_00516F0E_dump"] = b.hexd(0x00516F00, 0x30)
w = b.rd(0x00516F00, 0x30)
# decode: expected PUSH EAX (50) then PUSH imm8 0xA8 (6A A8) then... (68 A8 00 00 00??)
# executor: PUSH EAX `50` + PUSH 0xA8 `68 A8 00 00 00`?? -> their claim: bytes at hit are
# the tail of 'PUSH 0xA8' style encoding; verify the imm32 pattern lands mid-instruction
R["hit_00516F0E_bytes"] = w.hex()

# --- imm32 censuses ---
for name, val in (("vtable_ArkObjectClass_0x00A86850", 0x00A86850),
                  ("vtable_ArkObject_0x00A86B48", 0x00A86B48),
                  ("DAT_00BA5D9C", 0x00BA5D9C)):
    hits = b.scan_text_imm32(val)
    R[name] = dict(count=len(hits), sites=[hex(b.off2va(h)) for h in hits])

# --- f32-D getter FUN_00861240 sites inside FUN_00861390 ---
mine = [s["site_va"] for s in b.calls(0x00861240, 0xE8)]
in_861390 = [hex(x) for x in mine if 0x00861390 <= x < 0x00863000]
R["f32D_FUN_00861390"] = dict(claimed=["0x861b49", "0x861eeb"], mine=in_861390,
                              total_f32D_sites=len(mine))

# --- slot getters FUN_006C2840 / FUN_006C2870 ---
R["slot_getters"] = {}
for fn in (0x006C2840, 0x006C2870):
    d = b.rd(fn, 0x1C)
    # expect: MOV EAX,[ECX]; ... MOV ECX,[table+...]?? per executor: C -> tabela 0x00A858B4 ->
    # FUN_0043A550 -> lookup; dump + find calls
    calls = []
    o = 0
    while True:
        o = d.find(b"\xE8", o)
        if o < 0 or o + 5 > len(d):
            break
        t = fn + o + 5 + struct.unpack_from("<i", d, o + 1)[0]
        calls.append(dict(at=hex(fn + o), target=hex(t)))
        o += 1
    R["slot_getters"][hex(fn)] = dict(dump=b.hexd(fn, 0x1C), calls=calls,
                                     bytes=d.hex())

# --- table 0x00A858B4 content ---
R["table_00A858B4"] = [hex(b.u32va(0x00A858B4 + i * 4)) for i in range(6)]

# --- DAT_00BA5D9C writer (matrix row 2: ArkObjectClassImpl<ArkParameterContainer,20030>
#     writer FUN_0073CF50) ---
hits = [b.off2va(h) for h in b.scan_text_imm32(0x00BA5D9C)]
R["DAT_00BA5D9C_sites"] = [hex(x) for x in hits]
# find the writer: which function contains the store (C7 05 / A3)?
for va in hits:
    d = b.rd(va - 8, 16)
    if d and (b"A3" in d[:2] or d[:1] == b"\xC7"):
        pass  # just record context
R["DAT_00BA5D9C_ctx"] = [b.rd(b.off2va(h) - 10, 24).hex() for h in b.scan_text_imm32(0x00BA5D9C)]

p = save_json("QC_FINAL_LINKS.json", R)
print("saved", p)
print("hit_00516F0E:", R["hit_00516F0E_dump"])
print("0x00A86850 census:", R["vtable_ArkObjectClass_0x00A86850"])
print("0x00A86B48 census:", R["vtable_ArkObject_0x00A86B48"])
print("0x00BA5D9C census:", R["DAT_00BA5D9C"])
print("f32D in 00861390:", R["f32D_FUN_00861390"])
print("slot getters:", json.dumps(R["slot_getters"], indent=1))
print("table 0x00A858B4:", R["table_00A858B4"])
