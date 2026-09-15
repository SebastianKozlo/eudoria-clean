# WORK-AUDIT part10: SLOT17 body pins spot-verify + loop-state search
import struct, sys
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
d = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
e = struct.unpack_from("<I", d, 0x3C)[0]
coff = e + 4
optsz = struct.unpack_from("<H", d, coff + 16)[0]
opt = coff + 20
imgbase = struct.unpack_from("<I", d, opt + 28)[0]
nsec = struct.unpack_from("<H", d, coff + 2)[0]
secs = []
so = opt + optsz
for i in range(nsec):
    o = so + i * 40
    name = d[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
    vs, va, rs, rp = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, vs, va, rs, rp))
def off(va):
    rva = va - imgbase
    for name, vs, sva, rs, rp in secs:
        if sva <= rva < sva + rs:
            return rp + (rva - sva)
    return None
def rd(va, n):
    o = off(va)
    return d[o:o+n] if o is not None else None
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
print("== SLOT17 body 0x7B5390.. ==")
b = rd(0x7B5390, 0x18)
for i in md.disasm(b, 0x7B5390):
    print("  %08X  %-12s %s %s" % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
print("first-call target check: 0x7B5399 + 5 + rel32")
rel = struct.unpack_from("<i", rd(0x7B5399+1, 4), 0)[0]
print("  target = 0x%08X (claim 0x7BF220)" % (0x7B5399 + 5 + rel))
print("== target window 0x7BF220 ==")
b2 = rd(0x7BF220, 0x40)
cnt = 0
for i in md.disasm(b2, 0x7BF220):
    print("  %08X  %-10s %s %s" % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
    cnt += 1
    if cnt > 12: break
