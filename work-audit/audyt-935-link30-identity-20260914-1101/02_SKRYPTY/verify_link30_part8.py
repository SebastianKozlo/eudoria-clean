# WORK-AUDIT part8: context of the single writer 0x404C9D of global 0xb6c3d8
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
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.detail = True
print("== window 0x404C40..0x404CD0 ==")
b = rd(0x404C40, 0x90)
for i in md.disasm(b, 0x404C40):
    print("  %08X  %-22s %s %s" % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
