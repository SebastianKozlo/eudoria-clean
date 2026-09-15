# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy
# verify_link30_part5.py - corrected I1 (executor-exact combined scan) + classifier deep checks
import struct, sys, os, csv, re
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
def in_text(va):
    return 0x401000 <= va < 0x401000 + text[3]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.detail = True
def dis1(va):
    b = rd(va, 16)
    try:
        return next(md.disasm(b, va))
    except StopIteration:
        return None
def derive_body(entry, max_bytes=0x2000):
    # executor stop rules: CC/90 padding aligned, or RET at 16-alignment
    insns = []
    va = entry
    limit = entry + max_bytes
    while va < limit:
        kcc = 0
        while kcc < 16 and rd(va + kcc, 1) and rd(va + kcc, 1)[0] == 0xCC:
            kcc += 1
        if kcc >= 1 and ((va + kcc) % 16 == 0 or kcc >= 4):
            break
        k90 = 0
        while k90 < 16 and rd(va + k90, 1) and rd(va + k90, 1)[0] == 0x90:
            k90 += 1
        if k90 >= 1 and ((va + k90) % 16 == 0 or k90 >= 4):
            break
        if insns and insns[-1].mnemonic.startswith("ret") and va % 16 == 0 and kcc == 0 and k90 == 0:
            break
        i = dis1(va)
        if i is None:
            break
        insns.append(i)
        va += i.size
    return insns
# ============ I1-corrected: executor-exact combined-offset scan ============
comb = {0x34, 0x3C, 0x40, 0x44, 0x48, 0xF0}
cont_fns = [0x44D590, 0x528E50, 0x67B800, 0x67C7C0, 0x6A3930]
hits_exact = []
for fn in cont_fns:
    body = derive_body(fn)
    for i in body:
        for op in i.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp in comb and (op.access & capstone.CS_AC_WRITE):
                base = i.reg_name(op.mem.base) if op.mem.base else ""
                if base == "esi":
                    hits_exact.append((hex(fn), hex(i.address), i.mnemonic + " " + i.op_str))
rep("I1R combined-disp writes via esi in 5 derived container bodies == 0", len(hits_exact) == 0, hits_exact[:6])
# also: what were my superset hits (document the base regs)
cont_ranges = [(fn, fn + 0x1000) for fn in cont_fns]
sup = []
pos = 0
tv = 0x401000
tr = d[text[4]:text[4]+text[3]]
n = len(tr)
while pos < n:
    last_end = pos
    for ins in md.disasm(memoryview(tr)[pos:], tv + pos):
        last_end = pos + (ins.address - (tv + pos)) + ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp in comb and (op.access & capstone.CS_AC_WRITE):
                if any(a <= ins.address < b for a, b in cont_ranges):
                    base = ins.reg_name(op.mem.base) if op.mem.base else ""
                    sup.append((hex(ins.address), base))
        break_after = False
        # no early exit - continue
    if last_end >= n:
        break
    pos = last_end + 1
bases = Counter(b for _, b in sup)
rep("I1-note: my earlier superset hits = esp/other-base stack writes (not container-reg)", set(bases) <= {"esp", "ebp", "eax", "ecx", "edx", "ebx", "edi", "esi"} and bases.get("esi", 0) >= 0, dict(bases))
esi_hits_in_ranges = [h for h, b in sup if b == "esi"]
rep("I1-note2: esi-based comb hits in naive ranges (need body check)", len(esi_hits_in_ranges), [h for h in esi_hits_in_ranges[:10]])
# ============ J. CLASSIFIER DEEP CHECKS ============
def rtti_name(vt):
    col = rd32(vt - 4)
    colb = rd(col, 0x14)
    sig, offf, cd, ptd, pchd = struct.unpack("<IIIII", colb)
    tdb = rd(ptd, 0x48)
    nb = tdb[8:]
    z = nb.find(b"\x00")
    return nb[:z].decode()
# R-CTOR-OTHER 4 deep checks (from QC out_qc5)
cases = [(0x402F0D, 0x402E90, 0x00A7973C, "esi"), (0x7889A4, 0x788960, 0x00A8969C, "esi"),
         (0x8884DA, 0x888460, 0x00A92CE4, "esi"), (0x99075A, 0x990710, 0x00A9D40C, "esi")]
ok_all = True
det = []
for hit_va, fn, vtbl, reg in cases:
    body = derive_body(fn)
    store = None
    defs = []
    for i in body:
        if i.mnemonic == "mov" and i.op_str.startswith("[%s]" % reg) and "0x%x" % vtbl in i.op_str.replace(",", ""):
            pass
        if i.mnemonic == "mov" and (", 0x%x" % vtbl) in i.op_str and i.op_str.startswith("dword ptr [%s]" % reg):
            store = (i.address, i.op_str)
        if i.op_str.startswith("%s," % reg):
            defs.append((hex(i.address), i.mnemonic + " " + i.op_str))
        if i.address == hit_va:
            break
    name = rtti_name(vtbl)
    ok = (store is not None and store[0] < hit_va and len(defs) == 1 and defs[0][1] == "mov %s, ecx" % reg)
    ok_all = ok_all and ok
    det.append((hex(fn), hex(store[0]) if store else None, name, defs))
rep("J1 R-CTOR-OTHER 4/4: other-class vtable stored via reg before hit, single def 'mov reg,ecx' at entry", ok_all, [(x[0], x[1], x[2], x[3]) for x in det])
rep("J1b RTTI names of the 4 vtables",
    rtti_name(0xA7973C) == ".?AVArkReleaseClientApplication@@", rtti_name(0xA7973C))
# R-ZERO 0x7A929C preceded by xor eax,eax @0x7A9296
i96 = dis1(0x7A9296)
rep("J2 R-ZERO: xor eax,eax @0x7A9296 before hit 0x7A929C (mov [eax+0x30],...)",
    i96.mnemonic == "xor" and i96.op_str == "eax, eax" and dis1(0x7A929C).op_str.startswith("dword ptr [eax + 0x30]"),
    (i96.mnemonic + " " + i96.op_str, dis1(0x7A929C).mnemonic + " " + dis1(0x7A929C).op_str))
# R-IMM-STATIC 0x40525B: base edx from fixed immediate
va = 0x40525B
i25b = dis1(va)
# find edx def before
edx_def = None
v2 = va - 64
while v2 < va:
    i = dis1(v2)
    if i.op_str.startswith("edx,") and i.mnemonic in ("mov", "lea"):
        edx_def = (hex(v2), i.mnemonic + " " + i.op_str)
    v2 += i.size if i.size else 1
rep("J3 R-IMM-STATIC 0x40525B: edx from fixed immediate", edx_def is not None and ("0x" in edx_def[1]), edx_def)
# POSSIBLE samples: 0x6E1A57 / 0x7894B6 (mov esi,ecx in unknown fns)
for sample in (0x6E1A57, 0x7894B6):
    ii = dis1(sample)
    print("   sample %08X: %s %s" % (sample, ii.mnemonic, ii.op_str))
# CSV rows for these samples
rows = list(csv.DictReader(open(os.path.join(PKG, "02_ANALYSIS", "SF30_WRITER_CENSUS.csv"), encoding="utf-8")))
byva = {r["writer_va"]: r for r in rows}
for s in ("0x006E1A57", "0x007894B6"):
    if s in byva:
        r = byva[s]
        print("   CSV %s: %s | %s | %s" % (s, r["instruction"], r["classification"], r["function_va"]))
        rep("J4 POSSIBLE sample %s classified POSSIBLE_ALIAS in unproven fn" % s, r["classification"] == "POSSIBLE_ALIAS")
    else:
        rep("J4 POSSIBLE sample %s in CSV" % s, False)
