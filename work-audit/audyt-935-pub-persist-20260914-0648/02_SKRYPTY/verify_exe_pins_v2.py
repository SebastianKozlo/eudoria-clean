# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora
# -*- coding: utf-8 -*-
# v2 — poprawki bledow wlasnych + dodatkowe piny (audytor Work-Audit)
import struct, sys, hashlib
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
machine, nsec, tds, psym, nsym, optsize, chars = struct.unpack_from("<HHIIIHH", data, coff)
opt = coff + 20
imagebase = struct.unpack_from("<I", data, opt + 28)[0]
sec_off = opt + optsize
sections = []
for i in range(nsec):
    off = sec_off + i * 40
    name = data[off:off+8].rstrip(b"\x00").decode()
    vsize, va, rsize, raw = struct.unpack_from("<IIII", data, off + 8)
    sections.append((name, va, vsize, raw, rsize))
def va2off(va):
    rva = va - imagebase
    for name, sva, vsize, raw, rsize in sections:
        if sva <= rva < sva + max(vsize, rsize):
            return raw + (rva - sva)
    raise ValueError("VA 0x%08X unmapped" % va)
def rd(va, n): return data[va2off(va):va2off(va)+n]
results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))

# --- ARITH poprawione (kolejnosc bajtow LE!) ---
d = struct.unpack("<f", bytes.fromhex("CBE1F942"))[0]
check("ARITH 0x42F9E1CB = 124.94100189208984", d == 124.94100189208984, repr(d))
step = struct.unpack("<d", bytes.fromhex("000000A09999B93F"))[0]
check("ARITH step 0x3FB99999A0000000 = 0.100000001490116119384765625", step == 0.100000001490116119384765625, repr(step))
check("ARITH step != kanoniczne f64 0.1", step != 0.1)
check("ARITH kanoniczne f64 0.1 = 0x3FB999999999999A", struct.unpack("<Q", struct.pack("<d", 0.1))[0] == 0x3FB999999999999A)

# --- dodatkowe piny x87 CREATE sciezki ---
PINS2 = [
 (0x004C4773, "D9 5C 24 44", "FSTP [ESP+0x44] (h)"),
 (0x004C4777, "D9 44 24 18", "FLD [ESP+0x18] (z)"),
 (0x004C477B, "D9 44 24 44", "FLD [ESP+0x44] (h)"),
 (0x004C477F, "D8 D1", "FCOM ST(1)"),
 (0x004C4781, "DF E0", "FNSTSW AX"),
 (0x0085B1C1, "C7 06 4C 1E A9 00", "MOV [ESI],0xA91E4C (MOBJ vtable write @0x85B1C1)"),
 (0x00853AAD, "D9 EE", "FLDZ fallback filter-fail"),
 (0x00853B50, "D9 EE", "FLDZ fallback provider1-NULL"),
 (0x00934586, "D9 EE", "FLDZ fallback [this+8]-NULL"),
]
for va, hexs, name in PINS2:
    exp = bytes.fromhex(hexs.replace(" ", ""))
    check("PIN2 %s @0x%08X" % (name, va), rd(va, len(exp)) == exp, "got=%s" % rd(va, len(exp)).hex().upper())

# --- GUARD kolejnosc (poprawione parsowanie) ---
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
ops = list(md.disasm(rd(0x0085B750, 48), 0x0085B750))
seq = ["%s %s" % (i.mnemonic, i.op_str) for i in ops]
expected_seq = ["mov eax, dword ptr [ecx + 8]", "cmp eax, 2", "je 0x85b774", "cmp eax, 3", "je 0x85b774",
                "cmp eax, 6", "je 0x85b774", "cmp eax, 5", "je 0x85b774", "cmp eax, 4", "je 0x85b774",
                "cmp eax, 7", "je 0x85b774", "xor eax, eax", "ret"]
check("GUARD FUN_0085B750 sekwencja == {2,3,6,5,4,7}+XOR+RET", seq[:15] == expected_seq, str(seq[:15]))

# --- FUN_00755F90 AABB 6x FCOMPP ---
ops2 = list(md.disasm(rd(0x00755F90, 400), 0x00755F90))
fcompp = [i for i in ops2 if i.mnemonic == "fcompp"]
check("FILTER FUN_00755F90 zawiera 6x FCOMPP (AABB 3 osie x2 brzegi)", len(fcompp) == 6, str(len(fcompp)))
ret8 = [i for i in ops2 if i.mnemonic == "ret" and i.op_str == "8"]
check("FILTER RET 8 (C2 08 00)", len(ret8) >= 1)

# --- FUN_00936A60 cell formula: SHL ESI,0x10 / AND EAX,0xFFFF / OR EAX,ESI ---
ops3 = list(md.disasm(rd(0x00936A60, 700), 0x00936A60))
t3 = ["%s %s" % (i.mnemonic, i.op_str) for i in ops3]
has_shl = any(s.startswith("shl") and s.endswith("esi, 0x10") for s in t3)
has_and = any(s == "and eax, 0xffff" for s in t3)
has_or = any(s == "or eax, esi" for s in t3)
check("CELL formula SHL ESI,0x10 / AND EAX,0xFFFF / OR EAX,ESI", has_shl and has_and and has_or,
      "shl=%s and=%s or=%s" % (has_shl, has_and, has_or))

# --- FCHS w FUN_00936B10 ---
ops4 = list(md.disasm(rd(0x00936B10, 600), 0x00936B10))
fchs = [i.address for i in ops4 if i.mnemonic == "fchs"]
check("FCHS obecny w FUN_00936B10 (negacja wyniku)", len(fchs) >= 1, str([hex(a) for a in fchs]))

# --- FUN_0040DE60 advance ---
ops5 = list(md.disasm(rd(0x0040DE60, 64), 0x0040DE60))
t5 = ["%s %s" % (i.mnemonic, i.op_str) for i in ops5]
check("ADVANCE FUN_0040DE60 = ADD [ECX+0xC],EAX ... MOV BYTE [ECX+0x11],0 ... RET 4",
      t5[0] == "add dword ptr [ecx + 0xc], eax" and any("byte ptr [ecx + 0x11], 0" in s for s in t5) and any(s == "ret 4" for s in t5), str(t5[:8]))

# --- CENSUS v2: capstone skipdata, linear sweep .text ---
name, sva, vsize, raw, rsize = sections[0]
text = data[raw:raw+rsize]
md2 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md2.skipdata = True
targets = {0x004154F0: [], 0x00853A80: [], 0x00755F90: [], 0x004147F0: []}
ncall = 0
for ins in md2.disasm(text, imagebase + sva):
    if ins.mnemonic == "call":
        ncall += 1
        try:
            t = int(ins.op_str, 16)
        except ValueError:
            continue
        if t in targets: targets[t].append(ins.address)
print("linear sweep: total call instrukcji (do pliku raw .text):", ncall)
for t, lst in targets.items():
    print("CENSUS call sites -> 0x%08X : %d" % (t, len(lst)))
check("CENSUS FUN_004154F0 == 104 (claim 104/104)", len(targets[0x004154F0]) == 104, str(len(targets[0x004154F0])))
check("CENSUS FUN_00853A80 == 15 (claim 15)", len(targets[0x00853A80]) == 15, str(len(targets[0x00853A80])))
check("CENSUS FUN_00755F90 == 14 (claim 14)", len(targets[0x00755F90]) == 14, str(len(targets[0x00755F90])))
check("CENSUS FUN_004147F0 == 14 (claim 14)", len(targets[0x004147F0]) == 14, str(len(targets[0x004147F0])))
l = targets[0x00853A80]
waves = [x for x in l if 0x0048C000 <= x <= 0x0048C300]
check("CENSUS FUN_00853A80 WAVES (FUN_0048BFF0) == 9", len(waves) == 9, str([hex(x) for x in waves]))
exp_sites = [0x004C476E, 0x0085B41D, 0x0048C05B, 0x0048C0A9, 0x0048C0FB, 0x0048C14D, 0x0048C19F, 0x0048C1E5, 0x0048C22B, 0x0048C271, 0x0048C2B7, 0x0044A925, 0x0044A9EF, 0x0045BA76, 0x0045BF90]
check("CENSUS FUN_00853A80 sites == lista REPORT 15/15", all(x in l for x in exp_sites) and len(l) == 15, str([hex(x) for x in l]))

# --- D-1: EXE window vs independent_hexdumps.txt:69 (poprawione) ---
hd = open(r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913\independent_hexdumps.txt", "r", encoding="utf-8", errors="replace").read().splitlines()
line69 = hd[68]
hexes = [t for t in line69.replace("|", " ").replace("0x004C4780", "").split() if len(t) == 2 and all(c in "0123456789abcdefABCDEF" for c in t)]
fb = bytes.fromhex("".join(hexes[:16]))
got = rd(0x004C4780, 16)
check("D-1 window EXE == independent_hexdumps.txt:69", fb == got, "file=%s exe=%s" % (fb.hex(), got.hex()))

print()
print("SUMMARY v2: %d PASS, %d FAIL" % (sum(1 for _, ok, _ in results if ok), sum(1 for _, ok, _ in results if not ok)))
