# -*- coding: utf-8 -*-
# QC F2: selector branch 0x4E38 decode + jump table 0x00855BB4 + getter-D branch
# separation @0x008556DF + queue-push D sites in FUN_00567C50.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

# --- branch region dump ---
R["branch_008557C0_dump"] = b.hexd(0x008557C0, 0x80)

# hand-verify expected instruction bytes at claimed VAs
exp = {
    "CMP_EAX_4E38":  (0x008557DD, bytes.fromhex("3D384E0000"), "CMP EAX,0x4E38"),
    "JNZ_default":   (0x008557E2, bytes.fromhex("0F858E000000"), "JNZ +0x8E -> 0x00855876"),
    "LEA_EDX_38":    (0x008557E8, bytes.fromhex("8D542438"), "LEA EDX,[ESP+0x38]"),
    "PUSH_EDX":      (0x008557EC, bytes.fromhex("52"), "PUSH EDX"),
    "LEA_ECX_1C":    (0x008557ED, bytes.fromhex("8D4C241C"), "LEA ECX,[ESP+0x1C]"),
    "CALL_0085B860": (0x008557F1, bytes.fromhex("E86A600000"), "CALL FUN_0085B860"),
    "MOV_ECX_EAXind": (0x008557F6, bytes.fromhex("8B08"), "MOV ECX,[EAX]"),
    "CALL_getter":   (0x008557FD, bytes.fromhex("E8DE89F7FF"), "CALL FUN_007CE1E0"),
    "MOV_ECX_38":    (0x00855802, bytes.fromhex("8B4C2438"), "MOV ECX,[ESP+0x38]"),
    "MOV_ESI_EAX":   (0x00855806, bytes.fromhex("8BF0"), "MOV ESI,EAX"),
    "LEA_EAX_ESIm4": (0x00855811, bytes.fromhex("8D46FC"), "LEA EAX,[ESI-4]"),
    "CMP_EAX_3":     (0x00855814, bytes.fromhex("83F803"), "CMP EAX,3"),
    "JA_default":    (0x00855817, bytes.fromhex("7723"), "JA +0x23 -> 0x0085583C"),
    "JMP_jt":        (0x00855819, bytes.fromhex("FF2485B45B8500"), "JMP [EAX*4+0x00855BB4]"),
}
R["branch_checks"] = {}
for name, (va, bs, desc) in exp.items():
    actual = b.rd(va, len(bs))
    R["branch_checks"][name] = dict(va=hex(va), expected=bs.hex(), actual=(actual.hex() if actual else None),
                                    match=(actual == bs), desc=desc)
    print(("PASS " if actual == bs else "FAIL "), name, hex(va), actual.hex() if actual else None)

# computed CALL target for 0x008557F1 and 0x008557FD
c1 = b.rd(0x008557F1, 5)
t1 = 0x008557F1 + 5 + struct.unpack_from("<i", c1, 1)[0]
c2 = b.rd(0x008557FD, 5)
t2 = 0x008557FD + 5 + struct.unpack_from("<i", c2, 1)[0]
R["call_targets"] = dict(call_008557F1=hex(t1), call_008557FD=hex(t2))
print("call @557F1 ->", hex(t1), " call @557FD ->", hex(t2))

# --- jump table 0x00855BB4: 4 entries ---
jt = []
for i in range(4):
    v = b.u32va(0x00855BB4 + i * 4)
    jt.append(hex(v))
R["jump_table_00855BB4"] = jt
print("jump table:", jt)

# --- decode the 4 target blocks (what value goes to [ESP+0x1C]) ---
blocks = {}
for label, va in (("t0_00855834", 0x00855834), ("t2_00855820", 0x00855820), ("t3_0085582A", 0x0085582A)):
    blocks[label] = b.rd(va, 16).hex()
R["blocks"] = blocks
print("blocks:", blocks)

# --- getter D branch @0x008556DF: verify CALL FUN_0048ADA0 there and show context ---
R["getterD_008556DF"] = dict(
    call_bytes=b.rd(0x008556DF, 5).hex(),
    target=hex(0x008556DF + 5 + struct.unpack_from("<i", b.rd(0x008556DF, 5), 1)[0]),
    context=b.hexd(0x00855690, 0x70))
# is 0x008556DF inside the SAME switch? dump the region between 0x00855780 and 0x008557DD
R["pre_branch_dump"] = b.hexd(0x00855780, 0x60)
# find the switch dispatch around: look for CMP EAX,0x... series before 0x008557DD
# dump the branch for 0x38B0 mentioned in matrix row 4 (virtual call [vft+0xC])
i38b0 = None
w = b.rd(0x008553D0, 0x800)
for i in range(len(w) - 4):
    if w[i:i+3] == bytes.fromhex("3DB03800"):
        i38b0 = 0x008553D0 + i
        break
R["cmp_38B0_at"] = hex(i38b0) if i38b0 else None
if i38b0:
    R["cmp_38B0_region"] = b.hexd(i38b0, 0x50)

# --- FUN_00567C50: getter D calls @0x00567D16/@0x00567D46/@0x00567F72 + pushes after ---
R["f50_00567C50_dump"] = b.hexd(0x00567C90, 0x40)
for name, va in (("getterD1_00567D16", 0x00567D16), ("getterD2_00567D46", 0x00567D46),
                 ("getterD3_00567F72", 0x00567F72)):
    cb = b.rd(va, 5)
    if cb and cb[0] == 0xE8:
        tgt = va + 5 + struct.unpack_from("<i", cb, 1)[0]
        R[name] = dict(bytes=cb.hex(), target=hex(tgt),
                       is_getterD=(tgt == 0x0048ADA0),
                       ctx=b.hexd(va - 12, 0x24))
    else:
        R[name] = dict(bytes=cb.hex() if cb else None, note="no E8 at VA")
# verify pushes after getterD1/2: CALL FUN_00567B40 @0x00567D24 / 0x00567D54
for name, va in (("push1_00567D24", 0x00567D24), ("push2_00567D54", 0x00567D54)):
    cb = b.rd(va, 5)
    tgt = va + 5 + struct.unpack_from("<i", cb, 1)[0]
    R[name] = dict(bytes=cb.hex(), target=hex(tgt), is_queue_push=(tgt == 0x00567B40))
# verify arg1 read: MOV ESI,[ESP+0xEC] @0x00567C93? and MOV ECX,ESI before getterD calls
R["arg1_reads"] = dict(
    mov_esi_espec_ec_00567C93=b.rd(0x00567C93, 6).hex(),
    region_00567C90=b.hexd(0x00567C90, 0x10))
# MOV ECX,ESI (8B CE / 8B C6?) right before each getter D call
R["ecx_before_getterD"] = dict(
    before_d1=b.hexd(0x00567D16 - 6, 6),
    before_d2=b.hexd(0x00567D46 - 6, 6),
    before_d3=b.hexd(0x00567F72 - 6, 6))

# --- walker FUN_0085B860: verify structure (*out=[walker+0]; lock [value+4] if !=0) ---
R["walker_0085B860_dump"] = b.hexd(0x0085B860, 0x5B)

# --- resolver FUN_008544D0: MOV ESI,[EAX+8] @0x008544F9 ---
R["resolver_008544D0_dump"] = b.hexd(0x008544D0, 0x40)
R["resolver_mov_esi_eax8"] = dict(at=hex(0x008544F9), bytes=b.rd(0x008544F9, 3).hex(),
                                  match=b.rd(0x008544F9, 3) == bytes.fromhex("8B7008"))

p = save_json("QC_F2_SELECTOR.json", R)
print("saved", p)
for k, v in R["branch_checks"].items():
    print(("PASS " if v["match"] else "FAIL "), k)
print("jump_table:", R["jump_table_00855BB4"])
print("blocks:", R["blocks"])
print("getterD @556DF:", R["getterD_008556DF"]["target"], "bytes", R["getterD_008556DF"]["call_bytes"])
print("getterD1:", R["getterD1_00567D16"].get("is_getterD"), R["getterD1_00567D16"].get("target"))
print("getterD2:", R["getterD2_00567D46"].get("is_getterD"), R["getterD2_00567D46"].get("target"))
print("getterD3:", R["getterD3_00567F72"].get("is_getterD"), R["getterD3_00567F72"].get("target"))
print("push1:", R["push1_00567D24"])
print("push2:", R["push2_00567D54"])
print("resolver mov:", R["resolver_mov_esi_eax8"])
