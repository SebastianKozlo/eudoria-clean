# -*- coding: utf-8 -*-
# QC F1-ABI: independent reconstruction of the vtable 0x00A86850 chain
# (factory -> ctor ArkObjectClass -> ctor ArkObject -> getter) from raw bytes.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY. Own mapping (qc_core.Bin).
import struct, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

R["pe"] = dict(sha256=b.sha256, size=b.size, image_base=hex(b.image_base),
               dllchars=hex(b.dllchars), machine=hex(b.machine), nsec=b.num_sections,
               entry=hex(b.image_base + b.entry_rva),
               sections=[dict(name=s["name"], va=hex(s["va_lo"]), vsz=s["vsz"], rsz=s["rsz"],
                              exec=bool(s["chars"] & 0x20000000)) for s in b.sections])

# --- 1. vtable 0x00A86850 slots ---
VT = 0x00A86850
slot0 = b.u32va(VT); slot1 = b.u32va(VT + 4)
R["vtable_00A86850"] = dict(slot0=hex(slot0), slot1=hex(slot1),
                            raw=b.rd(VT, 16).hex())
check_vt = (slot0 == 0x0073F230 and slot1 == 0x0070BF50)

# --- 2. RTTI chain: vtable-4 -> COL -> TD -> name ---
col = b.u32va(VT - 4)
td = b.u32va(col + 0xC) if col else None
td_name_off = b.va2off(td) + 8 if td else None
name = b.cstr(td + 8, 128) if td else None
spare = b.u32va(td + 4) if td else None  # TD: vftable-ptr, spare, name
R["rtti_chain"] = dict(col_va=hex(col), td_va=hex(td) if td else None,
                       td_spare=hex(spare) if spare else None,
                       name=name,
                       td_name_bytes=b.rd(td + 8, 24).hex() if td else None)
check_rtti = (col == 0x00AA7F28 and td == 0x00B8D068 and name == ".?AVArkObjectClass@@")

# --- 3. factory FUN_0070BF50 ---
FAC = 0x0070BF50
fac = b.rd(FAC, 0x40)
R["factory_0070BF50_hexdump"] = b.hexd(FAC, 0x40)
# expected sequence
def find_seq(buf, seq):
    i = buf.find(seq)
    return i if i >= 0 else None
seq_mov_esi_ecx = bytes.fromhex("8BF1")
seq_push58 = bytes.fromhex("6A58")
fac_calls = []
i = 0
while True:
    i = fac.find(b"\xE8", i)
    if i < 0 or i + 5 > len(fac):
        break
    rel = struct.unpack_from("<i", fac, i + 1)[0]
    tgt = FAC + i + 5 + rel
    fac_calls.append(dict(at=hex(FAC + i), target=hex(tgt)))
    i += 1
R["factory_0070BF50"] = dict(
    bytes=fac.hex(),
    mov_esi_ecx_at=hex(FAC + find_seq(fac, seq_mov_esi_ecx)) if find_seq(fac, seq_mov_esi_ecx) is not None else None,
    push_58_at=hex(FAC + find_seq(fac, seq_push58)) if find_seq(fac, seq_push58) is not None else None,
    rel32_calls=fac_calls,
)
# decode the tail: expect 8B4C241C (MOV ECX,[ESP+1C]), 51 (PUSH ECX), 56 (PUSH ESI),
# 8BC8 (MOV ECX,EAX), E8.. (CALL 0x00726E70), C20400 (RET 4)
tail = fac[0x18:0x30]
call_at_96 = b.rd(0x0070BF96, 5)
rel96 = struct.unpack_from("<i", call_at_96, 1)[0]
tgt96 = 0x0070BF96 + 5 + rel96
R["factory_args"] = dict(
    bytes_18_30=tail.hex(),
    call_0070BF96=call_at_96.hex(), call_0070BF96_target=hex(tgt96),
    ret=b.rd(0x0070BF9B, 3).hex(),
    push_esi_before_call=fac[0x18:0x1A + 2].hex(),
)
check_fac = (tgt96 == 0x00726E70 and call_at_96[0] == 0xE8)
# find PUSH ESI (56) immediately preceding CALL site at 0x96
pre = fac[0x96 - FAC - 2: 0x96 - FAC]
R["factory_args"]["bytes_before_call"] = fac[0x96 - FAC - 4:0x96 - FAC].hex()

# --- 4. ctor ArkObjectClass FUN_0070CF80 ---
CT1 = 0x0070CF80
c1 = b.rd(CT1, 0x60)
R["ctor_class_0070CF80_hexdump"] = b.hexd(CT1, 0x60)
vft_write_at = 0x0070CFB6
store8_at = 0x0070CFC1
R["ctor_class_0070CF80"] = dict(
    entry_args_read=b.rd(CT1, 8).hex(),
    mov_ebp_esp28_at=None, vft_write=b.rd(vft_write_at, 6).hex(),
    store_plus8=b.rd(store8_at, 3).hex(),
    pushcount_note="count pushes in prologue to validate [ESP+0x28]=arg1",
)
# hand-decode prologue: collect push/pop until the mov ebp
# find MOV EBP,[ESP+0x28] = 8B 6C 24 28
p = c1.find(bytes.fromhex("8B6C2428"))
R["ctor_class_0070CF80"]["mov_ebp_esp28_at"] = hex(CT1 + p) if p >= 0 else None
R["ctor_class_0070CF80"]["prologue_bytes"] = c1[:p + 4].hex() if p >= 0 else None
# verify vft write C7 06 50 68 A8 00 at 0x0070CFB6
w = b.rd(vft_write_at, 6)
check_vftwrite = (w == bytes.fromhex("C7065068A800"))
# verify MOV [ESI+8],EBP = 89 6E 08 at 0x0070CFC1
s8 = b.rd(store8_at, 3)
check_store8 = (s8 == bytes.fromhex("896E08"))

# --- 5. ctor ArkObject FUN_00726E70 ---
CT2 = 0x00726E70
c2 = b.rd(CT2, 0x60)
R["ctor_arkobject_00726E70_hexdump"] = b.hexd(CT2, 0x60)
p2 = c2.find(bytes.fromhex("8B5C2424"))
R["ctor_arkobject_00726E70"] = dict(
    mov_ebx_esp24_at=hex(CT2 + p2) if p2 >= 0 else None,
    prologue_bytes=c2[:p2 + 4].hex() if p2 >= 0 else None,
)
lea_ecx_esi8_at = 0x00726E9E
vft2_at = 0x00726EA1
call_getter_at = 0x00726EB7
store28_at = 0x00726EBC
cg = b.rd(call_getter_at, 5)
relg = struct.unpack_from("<i", cg, 1)[0]
tg = call_getter_at + 5 + relg
R["ctor_arkobject_00726E70"].update(dict(
    lea_ecx_esi8=b.rd(lea_ecx_esi8_at, 3).hex(),
    vft_write=b.rd(vft2_at, 6).hex(),
    vft_value=hex(struct.unpack("<I", b.rd(vft2_at + 2, 4))[0]),
    store_plus4=b.rd(0x00726EA7, 3).hex(),
    call_at_726EB7=cg.hex(), call_target=hex(tg),
    store_plus28=b.rd(store28_at, 3).hex(),
    ret=b.rd(0x00726EC0, 3).hex() if b.rd(0x00726EC0, 1) == b"\xC2" else b.rd(0x00726EC0, 6).hex(),
    bytes_9E_C0=b.rd(0x00726E9E, 0x22).hex(),
))
check_ct2 = (b.rd(lea_ecx_esi8_at, 3) == bytes.fromhex("8D4E08")
             and b.rd(vft2_at, 6) == bytes.fromhex("C706486BA800")
             and tg == 0x007CE1E0
             and b.rd(store28_at, 3) == bytes.fromhex("894628"))

# --- 6. getter FUN_007CE1E0 ---
G = 0x007CE1E0
g = b.rd(G, 4)
R["getter_007CE1E0"] = dict(bytes=g.hex())
check_getter = (g == bytes.fromhex("8B4108C3"))

# --- 7. RTTI of ArkObject vtable 0x00A86B48 (row 3 of matrix) ---
VT2 = 0x00A86B48
col2 = b.u32va(VT2 - 4)
td2 = b.u32va(col2 + 0xC)
name2 = b.cstr(td2 + 8, 128)
R["arkobject_rtti"] = dict(vtable=hex(VT2), col=hex(col2), td=hex(td2), name=name2)

R["checks"] = dict(vtable=check_vt, rtti=check_rtti, factory_call_726E70=check_fac,
                  ctor_class_vftwrite=check_vftwrite, ctor_class_store8=check_store8,
                  ctor_arkobject_chain=check_ct2, getter=check_getter)

p = save_json("QC_F1_ABI.json", R)
print("saved", p)
for k, v in R["checks"].items():
    print(("PASS " if v else "FAIL "), k)
print("vtable slots:", R["vtable_00A86850"])
print("rtti:", R["rtti_chain"])
print("factory calls:", fac_calls)
print("ctor_class prologue:", R["ctor_class_0070CF80"]["prologue_bytes"])
print("ctor_arkobject prologue:", R["ctor_arkobject_00726E70"]["prologue_bytes"])
print("arkobject rtti:", R["arkobject_rtti"])
