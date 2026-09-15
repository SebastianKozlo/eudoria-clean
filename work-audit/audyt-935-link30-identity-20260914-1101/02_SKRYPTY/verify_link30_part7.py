# WORK-AUDIT part7: global 0xb6c3d8 identity (R-IMM-STATIC soundness deep-dive)
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
text = [s for s in secs if s[0] == ".text"][0]
def off(va):
    rva = va - imgbase
    for name, vs, sva, rs, rp in secs:
        if sva <= rva < sva + rs:
            return rp + (rva - sva)
    return None
def rd(va, n):
    o = off(va)
    return d[o:o+n] if o is not None else None
def rd32(va):
    b = rd(va, 4)
    return struct.unpack("<I", b)[0] if b and len(b) == 4 else None
def sec_of(va):
    for name, vs, sva, rs, rp in secs:
        if imgbase + sva <= va < imgbase + sva + max(vs, rs):
            return name
    return None
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.detail = True
def dis1(va):
    b = rd(va, 16)
    try:
        return next(md.disasm(b, va))
    except StopIteration:
        return None
print("on-disk dword at 0x00B6C3D8 =", hex(rd32(0xb6c3d8) or 0), "| section:", sec_of(0xb6c3d8))
print("hexdump around:", rd(0xb6c3d0, 32).hex())
tr = d[text[4]:text[4]+text[3]]
tvs = 0x401000
addr = struct.pack("<I", 0xb6c3d8)
pats = {
  "mov [g], imm32 (c7 05)": bytes.fromhex("c705") + addr,
  "mov [g], eax (a3)": bytes.fromhex("a3") + addr,
  "mov [g], ecx (89 0d)": bytes.fromhex("890d") + addr,
  "mov [g], edx (89 15)": bytes.fromhex("8915") + addr,
  "mov [g], ebx (89 1d)": bytes.fromhex("891d") + addr,
  "mov [g], esp (89 25)": bytes.fromhex("8925") + addr,
  "mov [g], ebp (89 2d)": bytes.fromhex("892d") + addr,
  "mov [g], esi (89 35)": bytes.fromhex("8935") + addr,
  "mov [g], edi (89 3d)": bytes.fromhex("893d") + addr,
}
print("== WRITERS of [0xb6c3d8] ==")
total_w = 0
for label, p in pats.items():
    j = 0
    while True:
        j = tr.find(p, j)
        if j < 0: break
        ins = dis1(tvs + j)
        print("  %08X  %-24s %s %s" % (ins.address, label, ins.mnemonic, ins.op_str))
        j += 1
        total_w += 1
print("total direct writers:", total_w)
# also disp32 forms: mov [reg+disp] can't reach absolute; mov [base] with base=imm... skip.
# check: what do the READERS do with it (context of 2 readers)
print("== readers context (8b 0d/15/1d/35/3d/a1) ==")
rpats = [bytes.fromhex(x) + addr for x in ("a1","8b0d","8b15","8b1d","8b35","8b3d","8b05","8b2d")]
cnt = 0
for p in rpats:
    j = 0
    while cnt < 12:
        j = tr.find(p, j)
        if j < 0: break
        ins = dis1(tvs + j)
        nxt = dis1(ins.address + ins.size)
        print("  %08X  %s %s   ; next: %s %s" % (ins.address, ins.mnemonic, ins.op_str, nxt.mnemonic, nxt.op_str))
        j += 1
        cnt += 1
