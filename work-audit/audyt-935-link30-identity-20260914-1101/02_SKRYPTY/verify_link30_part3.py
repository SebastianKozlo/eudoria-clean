# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy
# verify_link30_part3.py - FULL SWEEP reproduction + CSV + RAW recompute
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
# ============ F. FULL SWEEP (executor mechanics replicated independently) ============
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
text_va = 0x401000
text_bytes = d[text[4]:text[4]+text[3]]
candidates = []
n_decoded = 0
n_restarts = 0
mv = memoryview(text_bytes)
pos = 0
n = len(text_bytes)
while pos < n:
    last_end = pos
    for ins in md.disasm(mv[pos:], text_va + pos):
        n_decoded += 1
        last_end = pos + (ins.address - (text_va + pos)) + ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
                candidates.append(ins.address)
                break
    if last_end >= n:
        break
    pos = last_end + 1
    n_restarts += 1
rep("F1 sweep decoded == 2266698", n_decoded == 2266698, n_decoded)
rep("F2 sweep restarts == 64", n_restarts == 64, n_restarts)
rep("F3 raw candidates == 3643", len(candidates) == 3643, len(candidates))
# base-register distribution
md2 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md2.detail = True
def dis1(va):
    b = rd(va, 16)
    try:
        return next(md2.disasm(b, va))
    except StopIteration:
        return None
bc = Counter()
for va in candidates:
    ins = dis1(va)
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            bc[ins.reg_name(op.mem.base) if op.mem.base else "(none)"] += 1
            break
dist = dict(sorted(bc.items()))
exp_dist = {"eax": 80, "ebp": 25, "ebx": 24, "ecx": 30, "edi": 76, "edx": 6, "esi": 637, "esp": 2765}
rep("F4 base-register distribution exact", dist == exp_dist, dist)
# ============ G. CSV RECOMPUTE ============
rows = list(csv.DictReader(open(os.path.join(PKG, "02_ANALYSIS", "SF30_WRITER_CENSUS.csv"), encoding="utf-8")))
cls = Counter(r["classification"] for r in rows)
rep("G1 CSV rows == 3643", len(rows) == 3643, len(rows))
rep("G2 classes 2/618/3023/0", cls.get("PROVEN_SF30_WRITER") == 2 and cls.get("POSSIBLE_ALIAS") == 618
    and cls.get("REJECTED_ALIAS") == 3023 and cls.get("UNRESOLVED", 0) == 0, dict(cls))
vas = [r["writer_va"] for r in rows]
rep("G3 unique writer_va (no dups)", len(set(vas)) == 3643)
csv_vas = ["0x%08X" % v for v in candidates]
rep("G4 CSV order == my sweep candidate order", vas == csv_vas)
# every CSV instruction vs my own decode
mism = []
for r in rows:
    va = int(r["writer_va"], 16)
    ins = dis1(va)
    mine = "%s %s" % (ins.mnemonic, ins.op_str)
    if mine != r["instruction"]:
        mism.append((r["writer_va"], r["instruction"], mine))
rep("G5 all 3643 CSV instructions == my own decode", not mism, mism[:5])
prov = [r for r in rows if r["classification"] == "PROVEN_SF30_WRITER"]
rep("G6 PROVEN rows == 0x005093C3/0x0050A2D1 with exact instr+bytes",
    sorted(r["writer_va"] for r in prov) == ["0x005093C3", "0x0050A2D1"]
    and rd(0x5093C3, 3).hex() == "894530" and rd(0x50A2D1, 3).hex() == "895e30",
    [(r["writer_va"], r["instruction"], r["function_va"]) for r in prov])
fvas = set(r["function_va"] for r in rows)
rep("G7 distinct function_va == 2461, UNATTRIBUTED == 15",
    len(fvas) == 2461 and sum(1 for r in rows if r["function_va"] == "UNATTRIBUTED") == 15,
    (len(fvas), sum(1 for r in rows if r["function_va"] == "UNATTRIBUTED")))
# F_SF stats
F_SF = ["0x0044D590","0x0047CCF0","0x005090A0","0x005090B0","0x005090C0","0x00509330","0x005094C0",
        "0x005094E0","0x00509580","0x00509670","0x00509F00","0x0050A050","0x0050A240","0x0050A460",
        "0x005247C0","0x00528E50","0x0067B800","0x0067C7C0","0x006A3930"]
in_sf = [r for r in rows if r["function_va"] in F_SF]
c_in = Counter(r["classification"] for r in in_sf)
rep("G8 inside 19 F_SF: 2 PROVEN + 7 REJECTED + 0 POSSIBLE",
    c_in.get("PROVEN_SF30_WRITER") == 2 and c_in.get("REJECTED_ALIAS") == 7 and c_in.get("POSSIBLE_ALIAS", 0) == 0,
    dict(c_in))
poss = [r for r in rows if r["classification"] == "POSSIBLE_ALIAS"]
poss_fns = set(r["function_va"] for r in poss)
rep("G9 POSSIBLE 618 rows across 562 distinct functions", len(poss) == 618 and len(poss_fns) == 562,
    (len(poss), len(poss_fns)))
# 7 REJECTED inside F_SF: 6 esp + 1 container-field 0x44D5F0
rej_in = [(r["writer_va"], r["instruction"]) for r in in_sf if r["classification"] == "REJECTED_ALIAS"]
rep("G10 7 REJECTED inside F_SF incl 0x0044D5F0 mov [esi+0x30],edx", "0x0044D5F0" in [v for v, _ in rej_in], rej_in)
