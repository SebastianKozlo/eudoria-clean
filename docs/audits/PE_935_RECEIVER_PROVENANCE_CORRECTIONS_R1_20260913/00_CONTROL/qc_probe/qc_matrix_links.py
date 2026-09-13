# -*- coding: utf-8 -*-
# QC receiver-matrix remaining links:
#  - FUN_006B4C50 body-set getter calls @0x006B4C82/0x006B4C93 (row 1, avatar body-set)
#  - 0x38B0 branch: CMP EDI,0x38B0 + virtual call [vft+0xC] (row 4 layout claim)
#  - FUN_006FA8B0 ctor: vft @0x006FA8BD (+0xD), item @+8 (row 5, errata M-1)
#  - FUN_00468910: LEA ECX,[ESP+0x1C] @0x00468D84 + getter D @0x00468D88; 12-site census (row 7)
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, json
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

# --- FUN_006B4C50 region ---
R["f6b4c50_dump"] = b.hexd(0x006B4C50, 0x60)
c1 = b.rd(0x006B4C82, 5); c2 = b.rd(0x006B4C93, 5)
t1 = 0x006B4C82 + 5 + struct.unpack_from("<i", c1, 1)[0]
t2 = 0x006B4C93 + 5 + struct.unpack_from("<i", c2, 1)[0]
R["f6b4c50_getter_calls"] = dict(at_82=hex(t1), at_93=hex(t2),
                                 both_getterA=(t1 == 0x007CE1E0 and t2 == 0x007CE1E0),
                                 b1=c1.hex(), b2=c2.hex())

# --- 0x38B0 branch: CMP EDI,0x38B0 @0x00855792; virtual call [vft+0xC]? ---
R["branch_38B0_dump"] = b.hexd(0x00855790, 0x50)
w = b.rd(0x00855796, 0x40)
ff = []
o = 0
while o < len(w) - 2:
    if w[o] == 0xFF and (w[o + 1] & 0x38) == 0x10:  # FF /2 = call r/m
        ff.append(dict(at=hex(0x00855796 + o), modrm=hex(w[o + 1])))
    o += 1
R["branch_38B0_indirect_calls"] = ff

# --- FUN_006FA8B0: ctor AMRIR ---
R["f6fa8b0_dump"] = b.hexd(0x006FA8B0, 0x20)
R["f6fa8b0"] = dict(
    vft_at_0x006FA8BD=b.rd(0x006FA8BD, 6).hex(),
    is_c7_00_vft=b.rd(0x006FA8BD, 6) == bytes.fromhex("C700B864A800"),
    byte_at_0x006FA8BC=b.rd(0x006FA8BC, 1).hex(),
    item_plus8=b.rd(0x006FA8C3, 3).hex(),
    is_89_48_08=b.rd(0x006FA8C3, 3) == bytes.fromhex("894808"),
    ret=b.rd(0x006FA8C6, 3).hex())

# --- FUN_00468910: receiver = local record [ESP+0x1C] ---
R["f468910_spot"] = dict(dump=b.hexd(0x00468D80, 0x30),
                         lea_at_0x00468D84=b.rd(0x00468D84, 4).hex(),
                         is_lea_ecx_esp1c=b.rd(0x00468D84, 4) == bytes.fromhex("8D4C241C"),
                         call_at_0x00468D88=b.rd(0x00468D88, 5).hex())
cd = b.rd(0x00468D88, 5)
tgt = 0x00468D88 + 5 + struct.unpack_from("<i", cd, 1)[0]
R["f468910_spot"]["call_target"] = hex(tgt)
R["f468910_spot"]["is_getterD"] = (tgt == 0x0048ADA0)

# --- 12-site census of getter D in FUN_00468910 ---
claimed = [0x00468D88, 0x00468DA4, 0x004692BC, 0x004692D7, 0x004692F2, 0x0046930D,
           0x004694BE, 0x004694D9, 0x004694F0, 0x00469A7D, 0x00469AF0, 0x00469B0D]
mine = [s["site_va"] for s in b.calls(0x0048ADA0, 0xE8)]
mine_in_468910 = [hex(x) for x in mine if 0x00468910 <= x < 0x0046A100]
R["getterD_in_FUN_00468910"] = dict(
    claimed=[hex(x) for x in claimed],
    mine_in_range=mine_in_468910,
    mine_total_in_function=len(mine_in_468910),
    match=(sorted(claimed) == sorted(mine_in_468910)))
# how many in the union of this range?
R["getterD_in_FUN_00468910"]["mine_all_near"] = [hex(x) for x in mine if 0x00468910 <= x < 0x0046A100]

# --- RUN3 E.2: builder record @ESP+0xB4 — spot check the claimed region is at least
# consistent with the executor's dump F1_CTX5_REG567170_00567170 (we only verify presence
# of record-register pattern in FUN_00567770; detailed layout belongs to RUN3, out of scope) ---
R["f567770_head"] = b.hexd(0x00567770, 0x30)

p = save_json("QC_MATRIX_LINKS.json", R)
print("saved", p)
print("6B4C50 getter calls:", R["f6b4c50_getter_calls"])
print("38B0 indirect calls:", ff)
print("6FA8B0:", R["f6fa8b0"])
print("468910:", R["f468910_spot"])
print("getterD in FUN_00468910:", R["getterD_in_FUN_00468910"])
