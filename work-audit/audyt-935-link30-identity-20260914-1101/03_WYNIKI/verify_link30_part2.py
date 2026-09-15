# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy
# verify_link30_part2.py - RTTI walks, pattern scans, E8 censuses, full sweep, CSV+RAW recompute
import hashlib, struct, sys, os, csv, json, re
from collections import Counter
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
def rep(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))
d = open(EXE, "rb").read()
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
    name = d[o:o+8].rstrip(b"\x00").decode()
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
def rtti_walk(vt):
    col = rd32(vt - 4)
    colb = rd(col, 0x14)
    sig, offf, cd, ptd, pchd = struct.unpack("<IIIII", colb)
    tdb = rd(ptd, 0x48)
    vfptr, spare = struct.unpack_from("<II", tdb, 0)
    nb = tdb[8:]
    z = nb.find(b"\x00")
    return dict(col=col, sig=sig, off=offf, cd=cd, ptd=ptd, pchd=pchd,
                vfptr=vfptr, spare=spare, name=nb[:z].decode(), name_hex=nb[:z].hex())
# ============ D. RTTI WALKS ============
cal = rtti_walk(0x00A7D458)
ok_cal = (cal["col"] == 0x00AA12B8 and cal["sig"] == 0 and cal["ptd"] == 0x00B78834
          and cal["pchd"] == 0x00AA12CC and cal["vfptr"] == 0x00A98110 and cal["spare"] == 0
          and cal["name"] == ".?AVSceneFeederObject@@")
rep("D1 calibration chain == raw (COL 0xAA12B8, ptd 0xB78834, name .?AVSceneFeederObject@@)", ok_cal,
    (hex(cal["col"]), hex(cal["ptd"]), cal["name"]))
lk = rtti_walk(0x00A8CCF4)
ok_lk = (lk["col"] == 0x00AAEEC8 and lk["sig"] == 0 and lk["ptd"] == 0x00B936C8
         and lk["pchd"] == 0x00AAEEDC and lk["name"] == ".?AVNiNode@@"
         and lk["name_hex"] == "2e3f41564e694e6f64654040")
rep("D2 link chain == raw (COL 0xAAEEC8, ptd 0xB936C8, .?AVNiNode@@, name hex exact)", ok_lk,
    (hex(lk["col"]), hex(lk["ptd"]), lk["name"], lk["name_hex"]))
lk2 = rtti_walk(0x00A8CCE0)
rep("D3 secondary vtable 0xA8CCE0 -> .?AV?$NiTPointerList@PAVNiDynamicEffect@@@@",
    lk2["col"] == 0x00AAEE78 and lk2["ptd"] == 0x00B93694 and lk2["name"] == ".?AV?$NiTPointerList@PAVNiDynamicEffect@@@@",
    (hex(lk2["col"]), hex(lk2["ptd"]), lk2["name"]))
# P2-2 label check: TD+0x0C = name without .?AV prefix
tdb = rd(0x00B936C8, 0x30)
rep("D4 TD+0x0C starts with 'NiNode@@' (label-defect proof)", tdb[0x0C:0x0C+9] == b"NiNode@@", tdb[0x0C:0x18])
# SF vtable 6 slots + dPVS boundary
sfvt = [rd32(0x00A7D458 + 4*i) for i in range(6)]
rep("D5 SF vtable slots == [0x50A460,0x5090A0,0x5090B0,0x50A050,0x5090C0,0x509580]",
    sfvt == [0x50A460, 0x5090A0, 0x5090B0, 0x50A050, 0x5090C0, 0x509580], [hex(x) for x in sfvt])
rep("D6 SF vtable boundary dword 0xA7D470 == 0x53565064 (dPVS)", rd32(0xA7D470) == 0x53565064, hex(rd32(0xA7D470)))
# NiNode vtable extent 47 + slot17
n_slots = 0
va = 0x00A8CCF4
while True:
    v = rd32(va)
    if v is None or not (0x401000 <= v < 0x401000 + text[3]):
        break
    n_slots += 1
    va += 4
rep("D7 NiNode vtable extent == 47 code-pointer entries", n_slots == 47, n_slots)
vals = [rd32(0x00A8CCF4 + 4*k) for k in range(n_slots)]
rep("D8 0x7B6000 NOT among NiNode vtable entries", 0x7B6000 not in vals)
rep("D9 slot17 [0xA8CCF4+0x44]=[0xA8CD38] == 0x007B5390", rd32(0xA8CD38) == 0x7B5390, hex(rd32(0xA8CD38)))
rep("D10 TD section == .data, vtable/COL == .rdata", sec_of(0xB936C8) == ".data" and sec_of(0xA8CCF4) == ".rdata" and sec_of(0xAAEEC8) == ".rdata",
    (sec_of(0xA8CCF4), sec_of(0xAAEEC8), sec_of(0xB936C8)))

# ============ E. PATTERN + E8 SCANS ============
tr = d[text[4]:text[4]+text[3]]
tvs = 0x401000
def scan(pat):
    out = []
    i = 0
    while True:
        i = tr.find(pat, i)
        if i < 0: break
        out.append(tvs + i)
        i += 1
    return out
h458 = scan(struct.pack("<I", 0xA7D458))
rep("E1 imm32 0x00A7D458 in .text == exactly 2 (@0x509369, @0x50A26B)", h458 == [0x509369, 0x50A26B], [hex(x) for x in h458])
h330 = []
i = 0
pat330 = struct.pack("<I", 0x509330)
while True:
    i = d.find(pat330, i)
    if i < 0: break
    h330.append(i)
    i += 1
rep("E2 absolute dword 0x509330 in WHOLE file == 0", len(h330) == 0, len(h330))
def calls_to(t):
    sites = []
    for i in range(len(tr) - 5):
        if tr[i] == 0xE8:
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            if tvs + i + 5 + rel == t:
                sites.append(tvs + i)
    return sites
cc = sorted(calls_to(0x509330))
rep("E3 E8 -> 0x509330 == {0x47D043, 0x52480F}", cc == [0x47D043, 0x52480F], [hex(x) for x in cc])
cr = sorted(calls_to(0x5247C0))
exp = [0x44D625, 0x44D677, 0x44D6C8, 0x528FE1, 0x67B8A4, 0x67C864, 0x6A39ED]
rep("E4 E8 -> 0x5247C0 (create) == 7 callsites", cr == exp and len(cr) == 7, [hex(x) for x in cr])
c94 = calls_to(0x5094C0)
rep("E5 E8 -> 0x5094C0 == 15 callers", len(c94) == 15, len(c94))
c94e0 = calls_to(0x5094E0)
rep("E6 E8 -> 0x5094E0 includes 0x52482B", 0x52482B in c94e0, [hex(x) for x in c94e0])
c96 = calls_to(0x509670); c9f = calls_to(0x509F00)
rep("E7 E8 -> 0x509670 has 0x50A298; -> 0x509F00 has 0x50A2A9", 0x50A298 in c96 and 0x50A2A9 in c9f)
h42c = scan(struct.pack("<I", 0xA7D42C))
rep("E8 imm32 0xA7D42C hits == {0x509002,0x50904A,0x50A2EE,0x8B92F9,0x8B9519}",
    h42c == [0x509002, 0x50904A, 0x50A2EE, 0x8B92F9, 0x8B9519], [hex(x) for x in h42c])
h444 = scan(struct.pack("<I", 0xA7D444))
rep("E9 imm32 0xA7D444 hits == {0x509499,0x523DE1,0x5240D1,0x64B211}",
    h444 == [0x509499, 0x523DE1, 0x5240D1, 0x64B211], [hex(x) for x in h444])
# push eax between load and call at 3 non-adjacent sites
oks = []
for ld, cl in ((0x67B8E4, 0x67B8E8), (0x67C8A4, 0x67C8A8), (0x6A3A29, 0x6A3A2D)):
    gap = rd(ld + 3, cl - ld - 3)
    oks.append(gap.hex())
rep("E10 gaps load->call == single 'push eax' (50) x3", oks == ["50", "50", "50"], oks)

