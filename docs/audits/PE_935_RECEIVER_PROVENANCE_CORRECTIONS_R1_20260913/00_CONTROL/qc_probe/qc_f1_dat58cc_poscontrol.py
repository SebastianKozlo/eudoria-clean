# -*- coding: utf-8 -*-
# QC F1-DAT_00BA58CC: census of imm32 0x00BA58CC in .text + writer verification.
# QC F1-POSITIVE-CONTROL: parser 89 47 08 @0x00730CE6 -> lookup FUN_0072F580 ->
# getter FUN_007CE1E0 @0x006C3F74 with ECX = record.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

# --- DAT_00BA58CC census (all imm32 hits in .text, every offset) ---
hits = b.scan_text_imm32(0x00BA58CC)
sites = [dict(file_off=h, va=hex(b.off2va(h)), ctx=b.rd(b.off2va(h) - 8, 20).hex())
         for h in hits]
R["imm32_00BA58CC_text"] = dict(count=len(hits), sites=sites)

# writer region FUN_0073D810: dump
R["writer_0073D810_dump"] = b.hexd(0x0073D810, 0xC0)
# store singleton @0x0073D882: A3 CC 58 BA 00
store = b.rd(0x0073D882, 5)
R["store_at_0073D882"] = dict(bytes=store.hex(),
                              is_mov_eax_mem=store == bytes.fromhex("A3CC58BA00"))
# init-check @0x0073D832: 83 3D CC 58 BA 00 00
cmp0 = b.rd(0x0073D832, 7)
R["cmp0_at_0073D832"] = dict(bytes=cmp0.hex(),
                             is_cmp_mem0=cmp0 == bytes.fromhex("83 3DCC58BA0000".replace(" ", "")))
# new(0x118) region: find PUSH 0x118 + CALL new
w = b.rd(0x0073D810, 0x80)
i118 = w.find(bytes.fromhex("6818010000"))
R["new_0x118"] = dict(at=hex(0x0073D810 + i118) if i118 >= 0 else None)
# ctor call inside writer: find E8 -> 0x0073AB60
calls_in_writer = []
o = 0
while True:
    o = w.find(b"\xE8", o)
    if o < 0 or o + 5 > len(w):
        break
    rel = struct.unpack_from("<i", w, o + 1)[0]
    tgt = 0x0073D810 + o + 5 + rel
    calls_in_writer.append(dict(at=hex(0x0073D810 + o), target=hex(tgt)))
    o += 1
R["writer_calls"] = calls_in_writer

# --- accessor FUN_0073C970 ---
acc = b.rd(0x0073C970, 8)
R["accessor_0073C970"] = dict(bytes=acc.hex(),
                              pattern_mov_eax_mem_ret=acc[:6].hex() + acc[6:7].hex())

# --- POSITIVE CONTROL: parser write + lookup + getter chain ---
R["parser_00730CE6"] = dict(region=b.hexd(0x00730CD0, 0x30),
                            write_894708=b.rd(0x00730CE6, 3).hex(),
                            is_mov_edi8_eax=b.rd(0x00730CE6, 3) == bytes.fromhex("894708"))
# bounds-check cursor family: 3B 4E 08 (CMP ECX,[ESI+8]) / 77 13 (JA)
R["cursor_bounds"] = dict(
    cmp_ecx_esi8=b.rd(0x00730CC0, 0x30).hex())
# lookup FUN_0072F580: dump
R["lookup_0072F580_dump"] = b.hexd(0x0072F580, 0x50)
# rb-find call inside lookup
lk = b.rd(0x0072F580, 0x50)
lk_calls = []
o = 0
while True:
    o = lk.find(b"\xE8", o)
    if o < 0 or o + 5 > len(lk):
        break
    rel = struct.unpack_from("<i", lk, o + 1)[0]
    tgt = 0x0072F580 + o + 5 + rel
    lk_calls.append(dict(at=hex(0x0072F580 + o), target=hex(tgt)))
    o += 1
R["lookup_calls"] = lk_calls
# hit+0x14 pattern in lookup: find 8B .. 14 (mov reg,[reg+0x14]) near end
R["lookup_hit_plus14_region"] = b.hexd(0x0072F5A8, 0x28)

# FUN_006C3F50: MOV ECX,EDI after lookup; getter call @0x006C3F74
R["f50_006C3F50_dump"] = b.hexd(0x006C3F40, 0x50)
call_at = b.rd(0x006C3F74, 5)
rel = struct.unpack_from("<i", call_at, 1)[0]
tgt = 0x006C3F74 + 5 + rel
R["getter_call_006C3F74"] = dict(bytes=call_at.hex(), target=hex(tgt),
                                  is_getter_A=(tgt == 0x007CE1E0))
# MOV ECX,EDI just before?
R["mov_ecx_edi_before_getter"] = dict(at=hex(0x006C3F74 - 2), bytes=b.rd(0x006C3F72, 2).hex())

# --- singletons for matrix rows 6 ---
for fn, glob, size in ((0x004143F0, 0x00BA1260, 0x4C), (0x004154F0, 0x00BA12E8, 0x8C),
                       (0x00415570, 0x00BA12EC, 0xCC)):
    d = b.rd(fn, 0x40)
    # pattern: MOV EAX,[global]; TEST EAX,EAX; JNZ ret; PUSH size; CALL new
    has_mov = d.find(bytes.fromhex("A1") + struct.pack("<I", glob))
    has_push_size = d.find(struct.pack("<BH", 0x6A, size)) if size < 0x80 else d.find(struct.pack("<BHI", 0x68, size, 0))
    R.setdefault("singletons", []).append(dict(fn=hex(fn), global_hex=hex(glob), size=hex(size),
                                               mov_global_at=hex(fn + has_mov) if has_mov >= 0 else None,
                                               push_size_at=hex(fn + has_push_size) if has_push_size >= 0 else None,
                                               dump=b.hexd(fn, 0x30)))

# queue-push FUN_00567B40: getter A on singleton 0x00BA1260 @0x00567B49/50
q = b.rd(0x00567B40, 0x30)
q_calls = []
o = 0
while True:
    o = q.find(b"\xE8", o)
    if o < 0 or o + 5 > len(q):
        break
    rel = struct.unpack_from("<i", q, o + 1)[0]
    tgt = 0x00567B40 + o + 5 + rel
    q_calls.append(dict(at=hex(0x00567B40 + o), target=hex(tgt)))
    o += 1
R["queuepush_00567B40"] = dict(dump=b.hexd(0x00567B40, 0x30), calls=q_calls)

p = save_json("QC_F1_DAT58CC_POSCONTROL.json", R)
print("saved", p)
print("DAT_00BA58CC count:", R["imm32_00BA58CC_text"]["count"])
for s in R["imm32_00BA58CC_text"]["sites"]:
    print("  ", s["va"], s["ctx"])
print("store @0x0073D882:", R["store_at_0073D882"])
print("cmp0 @0x0073D832:", R["cmp0_at_0073D832"], "new118:", R["new_0x118"])
print("writer calls:", R["writer_calls"])
print("parser write 894708 @0x00730CE6:", R["parser_00730CE6"]["is_mov_edi8_eax"])
print("lookup calls:", R["lookup_calls"])
print("getter call @0x006C3F74 ->", R["getter_call_006C3F74"])
print("mov ecx,edi @", R["mov_ecx_edi_before_getter"])
print("queuepush calls:", R["queuepush_00567B40"]["calls"])
print("accessor:", R["accessor_0073C970"])
