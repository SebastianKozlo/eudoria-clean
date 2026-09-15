# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy
# verify_link30_part4.py - RAW recompute, reason census, combined-offset, rep movsd, classifier deep-checks
import struct, sys, os, csv, json, re
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
def rtti_name(vt):
    col = rd32(vt - 4)
    colb = rd(col, 0x14)
    sig, offf, cd, ptd, pchd = struct.unpack("<IIIII", colb)
    tdb = rd(ptd, 0x48)
    nb = tdb[8:]
    z = nb.find(b"\x00")
    return nb[:z].decode()
# ============ H. RAW FILE RECOMPUTE ============
raw_p = os.path.join(PKG, "01_RAW", "SF30_WRITER_RAW.txt")
raw_lines = open(raw_p, encoding="utf-8").read().splitlines()
rep("H1 raw line count == 35086", len(raw_lines) == 35086, len(raw_lines))
blocks = [l for l in raw_lines if l.startswith("### ")]
rep("H2 raw candidate blocks == 3643", len(blocks) == 3643, len(blocks))
rep("H3 raw blocks unique == 3643", len(set(blocks)) == 3643)
whys = [l for l in raw_lines if l.startswith("    why: ")]
why_rej = Counter()
for l in whys:
    m = re.match(r"    why: (R-[A-Z\-]+):", l)
    if m:
        why_rej[m.group(1)] += 1
exp_rej = {"R-ESP": 2765, "R-STACK-PTR": 129, "R-CTOR-OTHER": 104, "R-ZERO": 18,
           "R-LEA-STACK": 3, "R-EBP-INHERITED": 2, "R-IMM-STATIC": 1, "R-CONT-FIELD": 1}
rep("H4 REJECTED reason census == R-ESP 2765/R-STACK-PTR 129/R-CTOR-OTHER 104/R-ZERO 18/R-LEA-STACK 3/R-EBP-INHERITED 2/R-IMM-STATIC 1/R-CONT-FIELD 1",
    dict(why_rej) == exp_rej, dict(why_rej))
rep("H5 sum reasons == 3023 and R-EBP-FRAME == 0", sum(why_rej.values()) == 3023 and why_rej.get("R-EBP-FRAME", 0) == 0, sum(why_rej.values()))
# classes in raw blocks == CSV classes, same order
csv_rows = list(csv.DictReader(open(os.path.join(PKG, "02_ANALYSIS", "SF30_WRITER_CENSUS.csv"), encoding="utf-8")))
raw_cls = [l.split("class=")[1] for l in raw_lines if l.startswith("    fn=")]
rep("H6 raw block classes == CSV classes in order", raw_cls == [r["classification"] for r in csv_rows])
# specific amended lines
l19 = raw_lines[18]; l20 = raw_lines[19]; l21 = raw_lines[20]
ok_lines = ("hit 0x00509369 -> store insn: 00509366" in l19 and "c7450058d4a700" in l19
            and "raw bytes at 00509366: c7450058d4a700" in l20
            and "hit 0x0050A26B -> store insn: 0050A269" in l21 and "c70658d4a700" in l21)
rep("H7 raw L19-21 == AMEND_LOG 4b (NEW hit-line format, true stores)", ok_lines, (l19[:80], l21[:80]))
rep("H8 raw L62 == amended FUN_005094C0 P2-1 string", "load @0x0052901A mov ecx,[esi+0xc0] + call @0x00529020" in raw_lines[61], raw_lines[61][:120])
ok83 = all(("hit 0x00509%02X -> store insn" % 2 in raw_lines[82] if False else True) for _ in [0])
l83_87 = raw_lines[82:87]
ok_fam = ("hit 0x00509002" in l83_87[0] and "c7012cd4a700" in l83_87[0]
          and "hit 0x0050904A" in l83_87[1] and "hit 0x0050A2EE" in l83_87[2]
          and "hit 0x008B92F9" in l83_87[3] and "hit 0x008B9519" in l83_87[4])
rep("H9 raw L83-87 == AMEND_LOG 4b fam42c NEW renders", ok_fam, l83_87[0][:80])
rep("H10 raw L150 == RUN header with Era", raw_lines[149] == "# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 \u00b7 Era: PCG_9_3_5 \u00b7 STATIC-ONLY", raw_lines[149])
rep("H11 raw header denominator/sweep lines (156-157)", "RAW CANDIDATE COUNT (denominator before classification): 3643" in raw_lines[155]
    and "instructions decoded in sweep: 2266698 ; sweep bad-byte restarts: 64" in raw_lines[156], (raw_lines[155][:70], raw_lines[156][:70]))
# coverage (iii) text + (iv)
rep("H12 raw coverage (iii) ZERO-combined text + stores list", "ZERO combined-disp" in "\n".join(raw_lines[100:126]))
rep("H13 raw coverage (iv) rep movsd lines 0x50945D/0x50946E + targets text",
    "0050945D" in raw_lines[120] and "0050946E" in raw_lines[121] and "[ebp+0x4C]" in raw_lines[123], (raw_lines[120:60+61][:40] if False else "L121-124 ok"))
# RTTI section in raw (07)
rep("H14 raw 07 link RTTI == .?AVNiNode@@, 47 entries, slot17 0x7B5390",
    "'\u002e?AVNiNode@@'" in raw_lines[136] and "47" in raw_lines[138] and "0x007B5390" in raw_lines[141], (raw_lines[136], raw_lines[141]))
# ============ I. COMBINED-OFFSET + REP MOVSD ============
# full .text write-disp in {0x34,0x3C,0x40,0x44,0x48,0xF0} superset, then check container fn ranges
comb = {0x34, 0x3C, 0x40, 0x44, 0x48, 0xF0}
md3 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md3.detail = True
tv = 0x401000
tr = d[text[4]:text[4]+text[3]]
hits = []
pos = 0
n = len(tr)
while pos < n:
    last_end = pos
    for ins in md3.disasm(memoryview(tr)[pos:], tv + pos):
        last_end = pos + (ins.address - (tv + pos)) + ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp in comb and (op.access & capstone.CS_AC_WRITE):
                hits.append(ins.address)
                break
    if last_end >= n:
        break
    pos = last_end + 1
cont_ranges = [(0x44D590, 0x44D590+0x1000), (0x528E50, 0x528E50+0x1000), (0x67B800, 0x67B800+0x1000),
               (0x67C7C0, 0x67C7C0+0x1000), (0x6A3930, 0x6A3930+0x1000)]
in_cont = [h for h in hits if any(a <= h < b for a, b in cont_ranges)]
rep("I1 combined-disp writes inside 5 container fns (superset, any base) == 0", len(in_cont) == 0, [hex(x) for x in in_cont[:10]])
# rep movsd in SF ctor 0x509330..0x5094C0
repes = []
va = 0x509330
while va < 0x5094C0:
    i = dis1(va)
    if i is None: break
    if i.bytes == b"\xf3\xa5":
        repes.append(va)
    va += i.size
rep("I2 exactly 2 rep movsd in ctor @0x50945D/@0x50946E", repes == [0x50945D, 0x50946E], [hex(x) for x in repes])
# edi defs before each rep movsd (scan ctor start..rep)
edi_defs = []
va = 0x509330
while va < 0x50945D:
    i = dis1(va)
    if i.op_str.startswith("edi,"):
        edi_defs.append((hex(va), i.mnemonic + " " + i.op_str))
    va += i.size
rep("I3 edi def before rep#1 == lea edi,[esp+0x18] @0x5093E0", ("0x5093e0" in [a for a, _ in edi_defs]) and edi_defs[-1][1].startswith("lea edi, dword ptr [esp + 0x18]") if edi_defs else False, edi_defs)
edi_defs2 = []
va = 0x509330
while va < 0x50946E:
    i = dis1(va)
    if i.op_str.startswith("edi,"):
        edi_defs2.append((hex(va), i.mnemonic + " " + i.op_str))
    va += i.size
ok4c = edi_defs2 and edi_defs2[-1][0] == "0x509462" and edi_defs2[-1][1].startswith("lea edi, dword ptr [ebp + 0x4c]")
rep("I4 edi def before rep#2 == lea edi,[ebp+0x4C] @0x509462", ok4c, edi_defs2)
# mov esi,0xb93c80 present?
found = False
va = 0x509330
while va < 0x50945D:
    i = dis1(va)
    if "0xb93c80" in i.op_str and i.mnemonic == "mov":
        found = True
        break
    va += i.size
rep("I5 mov esi,0xb93c80 (static source) present before rep#1", found)
