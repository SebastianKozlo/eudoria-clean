# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora, NIE jest czescia pracy wykonawcy
# -*- coding: utf-8 -*-
# Wlasna weryfikacja bajtowa EXE (audytor Work-Audit) — czytanie tylko.
import struct, sys, hashlib
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
print("EXE size:", len(data))
print("EXE SHA256:", hashlib.sha256(data).hexdigest().upper())

# --- PE parse ---
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew+4] == b"PE\x00\x00"
coff = e_lfanew + 4
machine, nsec, tds, psym, nsym, optsize, chars = struct.unpack_from("<HHIIIHH", data, coff)
opt = coff + 20
magic = struct.unpack_from("<H", data, opt)[0]
imagebase = struct.unpack_from("<I", data, opt + 28)[0]
print("machine: 0x%04X (0x14C=x86)" % machine, "| nsec:", nsec, "| optMagic: 0x%04X (0x10B=PE32)" % magic, "| imageBase: 0x%08X" % imagebase)
sec_off = opt + optsize
sections = []
for i in range(nsec):
    off = sec_off + i * 40
    name = data[off:off+8].rstrip(b"\x00").decode()
    vsize, va, rsize, raw = struct.unpack_from("<IIII", data, off + 8)
    sections.append((name, va, vsize, raw, rsize))
    print("  SEC %-8s VA=0x%08X VSZ=0x%X RAW=0x%08X RSZ=0x%X" % (name, imagebase+va, vsize, raw, rsize))

def va2off(va):
    rva = va - imagebase
    for name, sva, vsize, raw, rsize in sections:
        if sva <= rva < sva + max(vsize, rsize):
            return raw + (rva - sva)
    raise ValueError("VA 0x%08X not mapped" % va)

def rd(va, n):
    return data[va2off(va):va2off(va)+n]

def u32(va): return struct.unpack("<I", rd(va, 4))[0]

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))

# --- byte pins ---
PINS = [
 (0x004C4780, "D1 DF E0 DD D9 F6 C4 41 75 06 D9 5C 24 18 EB 02", "D-1 window 0x4780-478F"),
 (0x00413440, "51 FF 15 64 50 A7 00 C3", "EnterCS thunk FUN_00413440"),
 (0x00413450, "51 FF 15 6C 50 A7 00 C3", "LeaveCS thunk FUN_00413450"),
 (0x00413340, "28 C2 08 00", "0x00413340 not-a-function-start"),
 (0x004C4767, "E8 84 0D F5 FF", "CALL FUN_004154F0"),
 (0x004C476E, "E8 0D F3 38 00", "CALL FUN_00853A80"),
 (0x004C4783, "DD D9", "FSTP ST(1)"),
 (0x004C4785, "F6 C4 41", "TEST AH,0x41"),
 (0x004C4788, "75 06", "JNE ->0x4790"),
 (0x004C478A, "D9 5C 24 18", "FSTP [ESP+0x18] (T-26)"),
 (0x004C478E, "EB 02", "JMP"),
 (0x004C4790, "DD D8", "FSTP ST(0) discard"),
 (0x004C4792, "68 28 01 00 00", "PUSH 0x128"),
 (0x004C47C1, "E8 8A 46 06 00", "CALL ctor FUN_00528E50"),
 (0x004C4878, "E8 D3 6E 39 00", "CALL guard FUN_0085B750"),
 (0x004C488A, "E8 51 6B 39 00", "CALL setpos FUN_0085B3E0"),
 (0x004C4896, "E8 15 65 39 00", "CALL rot FUN_0085ADB0"),
 (0x0085B41D, "E8 5E 86 FF FF", "EXISTING CALL FUN_00853A80"),
 (0x0085B437, "75 06", "EXISTING JNE"),
 (0x0085B439, "D9 5C 24 24", "EXISTING FSTP [ESP+0x24] @0x85B439 (poprawka A)"),
 (0x0085B43F, "DD D8", "EXISTING discard @0x85B43F"),
 (0x0085B4E9, "83 FE 64", "CMP ESI,0x64 (<=100)"),
 (0x00538BA9, "C7 06 30 F4 A7 00", "MOV [ESI],0xA7F430 (poprawka C)"),
 (0x00538BAF, "C7 46 04 20 F4 A7 00", "MOV [ESI+4],0xA7F420 koniec 0x538BB5"),
 (0x00509366, "C7 45 00 58 D4 A7 00", "MOV [EBP],0xA7D458 SF vtable"),
 (0x0085B1C1, "C7 01 4C 1E A9 00", "MOV [ECX],0xA91E4C MOBJ vtable"),
 (0x004C46F1, "83 FE 03", "CMP ESI,3"),
 (0x004C473D, "83 FE 06", "CMP ESI,6"),
 (0x004C4742, "83 FE 05", "CMP ESI,5"),
 (0x004C4747, "83 FE 04", "CMP ESI,4"),
 (0x004C474C, "83 FE 07", "CMP ESI,7"),
 (0x004C474F, "75 41", "JNE rel8=0x41 ->0x004C4792"),
 (0x00734597, "66 89 5F 24 5F 8B C6", "epilog1 MOV WORD [EDI+0x24],BX|POP EDI|MOV EAX,ESI"),
 (0x007345B0, "66 89 5F 24 5F 8B C6", "epilog2"),
 (0x004123D0, "8B 01 C3", "FUN_004123D0 MOV EAX,[ECX]"),
 (0x00746560, "8D 41 08 C3", "FUN_00746560 LEA EAX,[ECX+8]"),
 (0x00414130, "8B 41 74 C3", "FUN_00414130 MOV EAX,[ECX+0x74]"),
 (0x00853A50, "8B 44 24 04 89 01 C2 04 00", "FUN_00853A50 writer mgr1+0"),
]
for va, hexs, name in PINS:
    exp = bytes.fromhex(hexs.replace(" ", ""))
    got = rd(va, len(exp))
    check("PIN %s @0x%08X" % (name, va), got == exp, "got=%s" % got.hex().upper())

# --- rel32 call arithmetic (verify call targets) ---
CALLS = [(0x004C4767, 0x004154F0), (0x004C476E, 0x00853A80), (0x004C47C1, 0x00528E50),
         (0x004C4878, 0x0085B750), (0x004C488A, 0x0085B3E0), (0x004C4896, 0x0085ADB0),
         (0x0085B41D, 0x00853A80)]
for va, target in CALLS:
    b = rd(va, 5)
    rel = struct.unpack("<i", b[1:5])[0]
    tgt = va + 5 + rel
    check("CALLTARGET @0x%08X -> 0x%08X" % (va, tgt), b[0] == 0xE8 and tgt == target, "rel=0x%08X" % (rel & 0xFFFFFFFF))

# --- RTTI walks ---
RTTI = [
 (0x00A7F430, 0x00AA1920, 0x00B79A28, ".?AVMaTerrainManagerRuntime@@"),
 (0x00A7F420, 0x00AA1A34, 0x00B79A28, ".?AVMaTerrainManagerRuntime@@"),
 (0x00A7BA54, 0x00A9FB80, 0x00B717E0, ".?AVArkMoveSubsystem@@"),
 (0x00A7BA48, None,       0x00B717C0, ".?AVArkMoverInterface@@"),
 (0x00A7D458, 0x00AA12B8, 0x00B78834, ".?AVSceneFeederObject@@"),
 (0x00A91E4C, 0x00AB33D0, 0x00B7997C, ".?AVMovableObject@@"),
 (0x00A7DCB0, None,       0x00B79958, ".?AVClientMovableObject@@"),
]
for vt, ecol, etd, ename in RTTI:
    col = u32(vt - 4)
    td = u32(col + 0xC)
    nb = rd(td + 8, 64).split(b"\x00")[0].decode("ascii", "replace")
    ok = (ecol is None or col == ecol) and td == etd and nb == ename
    check("RTTI vtable 0x%08X -> COL 0x%08X -> TD 0x%08X = %s" % (vt, col, td, nb), ok)

# --- IAT walk ---
imp_rva = struct.unpack_from("<I", data, opt + 96 + 8)[0]  # data dir 1 (import)
found = {}
desc = va2off(imagebase + imp_rva)
while True:
    oft, tds2, fwd, name_rva, ft = struct.unpack_from("<IIIII", data, desc)
    if oft == 0 and ft == 0: break
    dll = rd(imagebase + name_rva, 32).split(b"\x00")[0].decode("ascii", "replace")
    thunk = oft if oft else ft
    i = 0
    while True:
        t = struct.unpack_from("<I", data, va2off(imagebase + thunk) + i*4)[0]
        if t == 0: break
        if not (t & 0x80000000):
            iname = rd(imagebase + t + 2, 48).split(b"\x00")[0].decode("ascii", "replace")
            iat_va = imagebase + ft + i*4
            if iname in ("EnterCriticalSection", "LeaveCriticalSection"):
                found[iname] = (dll, iat_va)
        i += 1
    desc += 20
for n, exp in (("EnterCriticalSection", 0x00A75064), ("LeaveCriticalSection", 0x00A7506C)):
    if n in found:
        dll, iat = found[n]
        check("IAT %s!%s @ 0x%08X" % (dll, n, iat), iat == exp and dll.lower().startswith("kernel32"))
    else:
        check("IAT %s found" % n, False, "not found in imports")

# --- data constants ---
import math
def f32(va): return struct.unpack("<f", rd(va, 4))[0]
def f64(va): return struct.unpack("<d", rd(va, 8))[0]
check("CONST 10.0f @0xA7B128", f32(0x00A7B128) == 10.0, str(f32(0x00A7B128)))
check("CONST -1000.0f @0xA7B270", f32(0x00A7B270) == -1000.0, str(f32(0x00A7B270)))
check("CONST 14.0 @0xA7B9F0", f64(0x00A7B9F0) == 14.0, str(f64(0x00A7B9F0)))
check("CONST 25.0 @0xA7AF88", f64(0x00A7AF88) == 25.0, str(f64(0x00A7AF88)))
b = rd(0x00A7AF80, 8)
qv = struct.unpack("<d", b)[0]
check("CONST drop-step @0xA7AF80 bits=0x3FB99999A0000000", struct.unpack("<Q", b)[0] == 0x3FB99999A0000000, "val=%r" % qv)
check("CONST drop-step value", qv == 0.100000001490116119384765625, repr(qv))
check("CONST -32767.0f @0xA7BA38", f32(0x00A7BA38) == -32767.0, str(f32(0x00A7BA38)))
check("CONST +32767.0f @0xA7BA3C", f32(0x00A7BA3C) == 32767.0, str(f32(0x00A7BA3C)))
check("CONST -500.0 @0xA7B098", f64(0x00A7B098) == -500.0, str(f64(0x00A7B098)))
check("CONST 0.5 @0xA79A08", f64(0x00A79A08) == 0.5, str(f64(0x00A79A08)))

# --- f32/f64 arithmetic claims ---
d = struct.unpack("<f", bytes.fromhex("42F9E1CB"))[0]
check("ARITH 0x42F9E1CB = 124.94100189208984", d == 124.94100189208984, repr(d))
step = struct.unpack("<d", bytes.fromhex("3FB99999A0000000"))[0]
check("ARITH step = 0.100000001490116119384765625", step == 0.100000001490116119384765625, repr(step))
check("ARITH kanoniczne f64 0.1 != 0x3FB99999A0000000", struct.unpack("<d", bytes.fromhex("3FB999999999999A"))[0] != step)

# --- FUN_0085B750 guard decode (warianty {2..7}, kolejnosc CMP 2/3/6/5/4/7) ---
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
code = rd(0x0085B750, 48)
ops = list(md.disasm(code, 0x0085B750))
seq = []
for ins in ops:
    if ins.mnemonic in ("cmp", "je", "xor", "ret", "mov") or ins.mnemonic.startswith("j"):
        seq.append("%s %s" % (ins.mnemonic, ins.op_str))
cmps = [s.split()[1] for s in seq if s.startswith("cmp ")]
print("GUARD FUN_0085B750 instr (pierwsze 20):", seq[:20])
check("GUARD cmp kolejnosc 2,3,6,5,4,7", cmps == ["eax, 2", "eax, 3", "eax, 6", "eax, 5", "eax, 4", "eax, 7"], str(cmps))

# --- FUN_005094C0 value-copy ---
code = rd(0x005094C0, 40)
ops2 = list(md.disasm(code, 0x005094C0))
txt = ["%s %s" % (i.mnemonic, i.op_str) for i in ops2]
print("FUN_005094C0:", txt)
w34 = any(i.mnemonic == "mov" and i.op_str.startswith("dword ptr [ecx + 0x34]") for i in ops2)
w38 = any(i.mnemonic == "mov" and i.op_str.startswith("dword ptr [ecx + 0x38]") for i in ops2)
w3c = any(i.mnemonic == "mov" and i.op_str.startswith("dword ptr [ecx + 0x3c]") for i in ops2)
b28 = any(i.mnemonic == "mov" and i.op_str == "byte ptr [ecx + 0x28], 1" for i in ops2)
r4 = any(i.mnemonic == "ret" and i.op_str == "4" for i in ops2)
check("FUN_005094C0 = 3xMOV [ECX+0x34/38/3C] + BYTE[ECX+0x28]=1 + RET 4", w34 and w38 and w3c and b28 and r4)

# --- census E8 boundary-checked (capstone linear sweep .text) ---
name, sva, vsize, raw, rsize = sections[0]
text = data[raw:raw+rsize]
md2 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md2.detail = True
targets = {0x004154F0: [], 0x00853A80: [], 0x00755F90: [], 0x004147F0: []}
calls_total = 0
for ins in md2.disasm(text, imagebase + sva):
    if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
        t = int(ins.op_str, 16)
        if t in targets:
            targets[t].append(ins.address)
        calls_total += 1
for t, lst in targets.items():
    print("CENSUS call sites -> 0x%08X : %d" % (t, len(lst)))
check("CENSUS FUN_004154F0 == 104 (claim 104/104)", len(targets[0x004154F0]) == 104, str(len(targets[0x004154F0])))
check("CENSUS FUN_00853A80 == 15 (claim 15)", len(targets[0x00853A80]) == 15, str(len(targets[0x00853A80])))
check("CENSUS FUN_00755F90 == 14 (claim 14)", len(targets[0x00755F90]) == 14, str(len(targets[0x00755F90])))
check("CENSUS FUN_004147F0 == 14 (claim 14)", len(targets[0x004147F0]) == 14, str(len(targets[0x004147F0])))
l = targets[0x00853A80]
print("FUN_00853A80 sites:", [hex(x) for x in l])
waves = [x for x in l if 0x0048C000 <= x <= 0x0048C300]
check("CENSUS FUN_00853A80 WAVES sites (FUN_0048BFF0) == 9", len(waves) == 9, str([hex(x) for x in waves]))
exp_sites = [0x004C476E, 0x0085B41D, 0x0048C05B, 0x0048C0A9, 0x0048C0FB, 0x0048C14D, 0x0048C19F, 0x0048C1E5, 0x0048C22B, 0x0048C271, 0x0048C2B7, 0x0044A925, 0x0044A9EF, 0x0045BA76, 0x0045BF90]
check("CENSUS FUN_00853A80 sites VA == lista z REPORT (15/15)", all(x in l for x in exp_sites) and len(l) == 15)

# --- D-1 window vs Desktop independent_hexdumps.txt:69 ---
try:
    hd = open(r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913\independent_hexdumps.txt", "r", encoding="utf-8", errors="replace").read().splitlines()
    line69 = hd[68]
    print("HEXDUMP line69:", line69[:160])
    hexes = []
    for tok in line69.replace("|", " ").split():
        if len(tok) == 2 and all(c in "0123456789abcdefABCDEF" for c in tok):
            hexes.append(tok)
    got = rd(0x004C4780, 16)
    check("D-1 window EXE == independent_hexdumps.txt:69", bytes(hexes[:16]) == got, "file=%s exe=%s" % (bytes(hexes[:16]).hex(), got.hex()))
except Exception as e:
    print("D-1 check error:", e)

print()
npass = sum(1 for _, ok, _ in results if ok)
nfail = sum(1 for _, ok, _ in results if not ok)
print("SUMMARY: %d PASS, %d FAIL" % (npass, nfail))
