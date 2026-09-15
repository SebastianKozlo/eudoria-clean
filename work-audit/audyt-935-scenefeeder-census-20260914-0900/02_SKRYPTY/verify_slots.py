# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-scenefeeder-census-20260914-0900) — plik audytora
# -*- coding: utf-8 -*-
# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-scenefeeder-census-20260914-0900) — plik audytora
# Wlasna weryfikacja bajtowa: vtable SceneFeederObject + 6 slotow + thunk delete + positive control
import struct, sys
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
data = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
def rd(va, n): return data[va-0x400000:va-0x400000+n]
def u32(va): return struct.unpack("<I", rd(va, 4))[0]
res = []
def check(name, ok, d=""):
    res.append((name, ok)); print(("PASS " if ok else "FAIL ") + name + ((" | " + d) if d else ""))

# --- G2: vtable 0x00A7D458: 6 wpisow + granica dPVS ---
EXP = [0x0050A460, 0x005090A0, 0x005090B0, 0x0050A050, 0x005090C0, 0x00509580]
got = [u32(0x00A7D458 + 4*i) for i in range(6)]
check("VTABLE 6 wpisow == lista kontraktowa", got == EXP, str([hex(x) for x in got]))
boundary = u32(0x00A7D458 + 24)
check("GRANICA za vtable = dword 0x53565064 ('dPVS' LE)", boundary == 0x53565064, hex(boundary))
bts = rd(0x00A7D470, 4)
check("granica ASCII 'dPVS'", bts == b"dPVS", repr(bts))
# RTTI
col = u32(0x00A7D454)
td = u32(col + 0xC)
name = rd(td + 8, 48).split(b"\x00")[0].decode()
check("RTTI [0xA7D454] -> COL 0x00AA12B8 -> TD 0x00B78834 -> .?AVSceneFeederObject@@",
      col == 0x00AA12B8 and td == 0x00B78834 and name == ".?AVSceneFeederObject@@", name)

# --- sloty proste: LEA/RET ---
for va, exp, nm in [(0x005090A0, "8D 41 34 C3", "slot1 LEA EAX,[ECX+0x34]; RET"),
                    (0x005090B0, "8D 41 74 C3", "slot2 LEA EAX,[ECX+0x74]; RET"),
                    (0x005090C0, "8D 41 80 C3", "slot4 LEA EAX,[ECX+0x80]; RET")]:
    check("PIN " + nm, rd(va, 4) == bytes.fromhex(exp.replace(" ", "")), rd(va, 4).hex().upper())

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)

# --- slot 0: scalar deleting dtor @0x0050A460 ---
ops0 = list(md.disasm(rd(0x0050A460, 0x40), 0x0050A460))
s0 = ["%s %s" % (i.mnemonic, i.op_str) for i in ops0]
print("SLOT0 @0x50A460:", s0[:10])
calls0 = [(i.address, i.op_str) for i in ops0 if i.mnemonic == "call"]
print("  calls:", calls0)
has_dtor = any("0x50a240" in c[1] for c in calls0)
has_del = any("0x95d42a" in c[1] for c in calls0)
check("SLOT0 = scalar deleting dtor: call 0x50A240 + call 0x95D42A", has_dtor and has_del, str(calls0))

# --- thunk 0x95D42A: jmp [IAT] -> MSVCR80 operator delete ---
th = rd(0x0095D42A, 6)
check("THUNK 0x95D42A = FF 25 (jmp [import])", th[0] == 0xFF and th[1] == 0x25, th.hex().upper())
iat_va = struct.unpack("<I", th[2:6])[0]
# wlasny import-walk: znajdz MSVCR80 operator delete (??3@YAXPAX@Z)
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
opt = e_lfanew + 4 + 20
imagebase = struct.unpack_from("<I", data, opt + 28)[0]
imp_rva = struct.unpack_from("<I", data, opt + 96 + 8)[0]
def va2off(va):
    rva = va - 0x400000
    secs = [(".text",0x1000,0x674000,0x1000),(".rdata",0x675000,0xf7000,0x675000),(".data",0x76c000,0x34000,0x76c000)]
    for nm, sva, vsz, raw in secs:
        if sva <= rva < sva + vsz: return raw + (rva - sva)
    raise ValueError(hex(va))
found_del = None
desc = va2off(imagebase + imp_rva)
while True:
    oft, tds2, fwd, name_rva, ft = struct.unpack_from("<IIIII", data, desc)
    if oft == 0 and ft == 0: break
    dll = rd(imagebase + name_rva, 32).split(b"\x00")[0].decode()
    thunk = oft if oft else ft
    i = 0
    while True:
        t = struct.unpack_from("<I", data, va2off(imagebase + thunk) + i*4)[0]
        if t == 0: break
        if not (t & 0x80000000):
            iname = rd(imagebase + t + 2, 48).split(b"\x00")[0].decode("ascii", "replace")
            iat_slot = imagebase + ft + i*4
            if iname == "??3@YAXPAX@Z":  # operator delete
                found_del = (dll, iname, iat_slot)
        i += 1
    desc += 20
print("  import operator delete:", found_del, "| IAT-slot thunku:", hex(iat_va))
check("THUNK IAT slot == MSVCR80!operator delete", found_del is not None and found_del[2] == iat_va and "MSVCR80" in found_del[0].upper(),
      str(found_del))

# --- slot 5 @0x00509580: czyta [this+0x18], call 0x4150F0/0x8B71D0 ---
ops5 = list(md.disasm(rd(0x00509580, 0x40), 0x00509580))
s5 = ["%s %s" % (i.mnemonic, i.op_str) for i in ops5]
print("SLOT5 @0x509580:", s5[:12])
r18 = any("[ecx + 0x18]" in s for s in s5)
c4150F0 = any(i.mnemonic == "call" and "0x4150f0" in i.op_str for i in ops5)
c8B71D0 = any(i.mnemonic == "call" and "0x8b71d0" in i.op_str for i in ops5)
check("SLOT5 czyta [this+0x18] + call 0x4150F0 + call 0x8B71D0", r18 and c4150F0 and c8B71D0)

# --- slot 3 @0x0050A050: pelny dekod do pierwszego konca ---
ops3 = list(md.disasm(rd(0x0050A050, 0x100), 0x0050A050))
s3 = ["%s %s" % (i.mnemonic, i.op_str) for i in ops3]
print("SLOT3 @0x50A050 (pelne):")
for s in s3: print("   ", s)
