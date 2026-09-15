# -*- coding: utf-8 -*-
# WORK-AUDIT — slot 3: dokladne adresy instrukcji vs piny z komunikatu
import sys
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
data = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
def rd(va, n): return data[va-0x400000:va-0x400000+n]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
print("=== slot 4 @0x5090C0 (pelne bajty) ===")
b = rd(0x005090C0, 8)
print("bytes:", b.hex().upper())
print("=== slot 3 @0x50A050 z adresami (do 0x50A0AA) ===")
ops = list(md.disasm(rd(0x0050A050, 0x60), 0x0050A050))
for i in ops:
    if i.address > 0x0050A0AA: break
    print("  0x%08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))
pins = {0x50A05B: "czyta +0x30 (link)", 0x50A064: "vcall [EDX+0x44] slot17", 0x50A090: "odczyt X", 0x50A098: "odczyt Y", 0x50A09E: "odczyt Z", 0x50A096: "kopia X do arg1", 0x50A09B: "kopia Y", 0x50A0A1: "kopia Z"}
ops_by_va = {i.address: i for i in ops}
for va, desc in pins.items():
    o = ops_by_va.get(va)
    print("PIN 0x%08X (%s): %s" % (va, desc, ("%s %s" % (o.mnemonic, o.op_str)) if o else "BRAK INSTRUKCJI NA TYM VA"))
