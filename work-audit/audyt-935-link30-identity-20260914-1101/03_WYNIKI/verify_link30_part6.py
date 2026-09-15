# WORK-AUDIT part6: R-IMM-STATIC deep dive (0x40525B) + container body boundaries
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
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.detail = True
def dis1(va):
    b = rd(va, 16)
    try:
        return next(md.disasm(b, va))
    except StopIteration:
        return None
def diswin(va, n):
    b = rd(va, n)
    return list(md.disasm(b, va))
print("== window 0x405230..0x405270 ==")
for i in diswin(0x405230, 0x40):
    print("  %08X  %-20s %s %s" % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
# who writes global 0xb6c3d8?
tr = d[text[4]:text[4]+text[3]]
tvs = 0x401000
print("== writers of [0xb6c3d8] ==")
import re
pats = [bytes.fromhex("c705") + struct.pack("<I", 0xb6c3d8),  # mov [addr], imm
        bytes.fromhex("a3") + struct.pack("<I", 0xb6c3d8),    # mov [addr], eax
        ]
for regop in ("890d", "8915", "891d", "8935", "893d", "892d", "8905", "8915"):
    pats.append(bytes.fromhex(regop) + struct.pack("<I", 0xb6c3d8))
i = 0
while True:
    found = False
    for p in pats:
        i = tr.find(p, i)
        if i >= 0:
            ins = dis1(tvs + i)
            print("  %08X  %s %s" % (ins.address, ins.mnemonic, ins.op_str))
            i += 1
            found = True
            break
    if not found:
        break
# sorted unique
print("== readers (loads) sample ==")
cnt = 0
for p in [bytes.fromhex("a1") + struct.pack("<I", 0xb6c3d8)]:
    j = 0
    while cnt < 8:
        j = tr.find(p, j)
        if j < 0: break
        ins = dis1(tvs + j)
        print("  %08X  %s %s" % (ins.address, ins.mnemonic, ins.op_str))
        j += 1
        cnt += 1
# container body ends
def pad_run(va, byte):
    k = 0
    while k < 16:
        b = rd(va + k, 1)
        if not b or b[0] != byte:
            break
        k += 1
    return k
def derive_body(entry, max_bytes=0x2000):
    insns = []
    va = entry
    limit = entry + max_bytes
    stop = None
    while va < limit:
        kcc = pad_run(va, 0xCC)
        if kcc >= 1 and ((va + kcc) % 16 == 0 or kcc >= 4):
            stop = ("CC", va); break
        k90 = pad_run(va, 0x90)
        if k90 >= 1 and ((va + k90) % 16 == 0 or k90 >= 4):
            stop = ("90", va); break
        if insns and insns[-1].mnemonic.startswith("ret") and va % 16 == 0 and kcc == 0 and k90 == 0:
            stop = ("RET_ALIGN", va); break
        i = dis1(va)
        if i is None:
            stop = ("FAIL", va); break
        insns.append(i)
        va += i.size
    return insns, stop
for fn in (0x44D590, 0x528E50, 0x67B800, 0x67C7C0, 0x6A3930):
    body, stop = derive_body(fn)
    end = body[-1].address + body[-1].size if body else fn
    print("body %08X..%08X stop=%s len=%d" % (fn, end, stop, end - fn))
