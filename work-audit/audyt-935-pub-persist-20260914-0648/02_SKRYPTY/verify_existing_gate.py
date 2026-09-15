# WORK-AUDIT header
# -*- coding: utf-8 -*-
# WORK-AUDIT — okno EXISTING FUN_0085B3E0: brak bramki wariantu PRZED korekta (claim RESEARCH_FINDINGS_WORKING §4)
import sys, struct
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
data = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
def rd(va, n): return data[va-0x400000:va-0x400000+n]
# pin: CALL FUN_00413440 @0x00853AE8
b = rd(0x00853AE8, 5)
rel = struct.unpack("<i", b[1:5])[0]
tgt = 0x00853AE8 + 5 + rel
print("E8 @0x853AE8:", b.hex().upper(), "-> target 0x%08X (claim 0x00413440):" % tgt, tgt == 0x00413440)
# okno EXISTING 0x85B3E0-0x85B460: wylistuj cmp i pozycje zapisu z'
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
ops = list(md.disasm(rd(0x0085B3E0, 0x80), 0x0085B3E0))
for i in ops:
    if i.address > 0x0085B460: break
    t = "%s %s" % (i.mnemonic, i.op_str)
    if i.mnemonic in ("cmp", "call", "fstp", "fld", "jne", "test") or "edi + 8" in t:
        print("  0x%08X  %s" % (i.address, t))
