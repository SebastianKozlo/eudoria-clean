# -*- coding: utf-8 -*-
# QC probe 2 — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# FRESH independent byte verification of every load-bearing cited VA.
# Written by the QC auditor (own implementation; only the capstone decoder
# library is shared with the executor). STATIC-ONLY: byte reads only.
# Output: 00_CONTROL/qc_probe/out_qc2_bytes.txt
import struct, sys, hashlib

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = []

def log(s=""):
    OUT.append(s)
    print(s)

# ---- own PE parser (fresh implementation) --------------------------------
data = open(EXE, "rb").read()
assert data[:2] == b"MZ"
lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[lfanew:lfanew+4] == b"PE\0\0"
mach, nsec = struct.unpack_from("<HH", data, lfanew + 4)
opt_off = lfanew + 24
magic = struct.unpack_from("<H", data, opt_off)[0]
imgbase = struct.unpack_from("<I", data, opt_off + 28)[0]
dllchar = struct.unpack_from("<H", data, opt_off + 70)[0]
sec_off = opt_off + struct.unpack_from("<H", data, lfanew + 20)[0]
SECS = []
for i in range(nsec):
    o = sec_off + 40 * i
    nm = data[o:o+8].rstrip(b"\0").decode()
    vs, va, rs, rp = struct.unpack_from("<IIII", data, o + 8)
    SECS.append((nm, va, vs, rs, rp))
log("== PE header (own walk) ==")
log("machine=0x%04X nsec=%d magic=0x%04X imgbase=0x%08X dllchar=0x%04X (DYNAMIC_BASE=%s)"
    % (mach, nsec, magic, imgbase, dllchar, "SET" if dllchar & 0x40 else "clear"))
sha = hashlib.sha256(data).hexdigest().upper()
log("sha256=%s size=%d" % (sha, len(data)))
assert sha == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
assert len(data) == 8015872 and mach == 0x14C and magic == 0x10B and imgbase == 0x400000

def off_of(va):
    rva = va - imgbase
    for nm, sva, vs, rs, rp in SECS:
        if sva <= rva < sva + rs:
            return rp + (rva - sva)
    return None

def rd(va, n):
    o = off_of(va)
    return None if o is None else data[o:o+n]

def rd32(va):
    b = rd(va, 4)
    return None if b is None or len(b) < 4 else struct.unpack("<I", b)[0]

def sec_of(va):
    rva = va - imgbase
    for nm, sva, vs, rs, rp in SECS:
        if sva <= rva < sva + max(vs, rs):
            return nm
    return None

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

def ins_at(va, n=16):
    b = rd(va, n)
    if b is None:
        return None
    try:
        i = next(md.disasm(b, va))
        return (i.address, i.size, i.bytes.hex(), i.mnemonic, i.op_str)
    except StopIteration:
        return None

def show(va, note="", expect=None):
    i = ins_at(va)
    if i is None:
        log("  %08X  <unreadable>  %s" % (va, note))
        return None
    ok = ""
    if expect is not None:
        ok = " OK" if i[2] == expect else (" MISMATCH(expected %s)" % expect)
    log("  %08X  %-14s %-8s %-40s%s  | %s" % (va, i[2], i[3], i[4], ok, note))
    return i

log("")
log("== C2: writer#1 chain (SF ctor FUN_00509330) ==")
show(0x00509330, "SF ctor entry")
show(0x00509357, "mov ebp,ecx (SF-this)", expect="8bec")
show(0x00509366, "mov [ebp],0xa7d458 (SF vtable store)", expect="c7450058d4a700")
show(0x00509376, "push 0x118", expect="6818010000")
show(0x005093A0, "call 0x95d3c4 (operator new)", expect="e81f404500")
show(0x005093A5, "add esp,4", expect="83c404")
show(0x005093AC, "cmp eax,ebx", expect="3bc3")
show(0x005093B5, "push ebx", expect="53")
show(0x005093B6, "mov ecx,eax", expect="8bc8")
show(0x005093B8, "call 0x7b6000 (block ctor)", expect="e843cc2a00")
show(0x005093BD, "jmp 0x5093c1", expect="eb02")
show(0x005093BF, "xor eax,eax", expect="33c0")
show(0x005093C1, "cmp eax,ebx", expect="3bc3")
show(0x005093C3, "WRITE1: mov [ebp+0x30],eax", expect="894530")
show(0x005093C6, "je", expect="7404")
show(0x005093C8, "refcount++ [eax+4]", expect="83400401")

log("")
log("== C2: block ctor FUN_007B6000 window 0x007B6020..0x007B60A8 ==")
va = 0x007B6020
while va < 0x007B60A8:
    i = ins_at(va)
    if i is None:
        break
    tag = ""
    if va == 0x007B6041:
        tag = "  <== VTABLE STORE [esi]=0x00A8CCF4"
    if va == 0x007B605E:
        tag = "  <== SECONDARY VTABLE STORE [esi+0xE0]=0x00A8CCE0"
    log("  %08X  %-14s %-8s %s%s" % (va, i[2], i[3], i[4], tag))
    va += i[1]

log("")
log("== C3: writer#2 chain (SF dtor body FUN_0050A240) ==")
show(0x0050A263, "mov esi,ecx", expect="8bf1")
show(0x0050A269, "mov [esi],0xa7d458", expect="c70658d4a700")
show(0x0050A272, "xor ebx,ebx (P2 source const 0)", expect="33db")
show(0x0050A2BD, "mov ecx,[esi+0x30]", expect="8b4e30")
show(0x0050A2C0, "cmp ecx,ebx", expect="3bcb")
show(0x0050A2C4, "refcount-- [ecx+4]", expect="834104ff")
show(0x0050A2C8, "jne 0x50a2d1", expect="7507")
show(0x0050A2CA, "mov eax,[ecx]", expect="8b01")
show(0x0050A2CC, "mov edx,[eax+4] (vtbl slot1)", expect="8b5004")
show(0x0050A2CF, "call edx", expect="ffd2")
show(0x0050A2D1, "WRITE2: mov [esi+0x30],ebx", expect="895e30")
show(0x0050A2D4, "mov ecx,[esi+0x30] (re-read)", expect="8b4e30")
# dtor body called from vtable slot 0 FUN_0050A460 with ecx=this
i = ins_at(0x0050A460)
log("  (slot0) FUN_0050A460 entry: %s %s %s" % (i[2], i[3], i[4]))
# find the call 0x50A240 inside FUN_0050A460
va = 0x0050A460
found = False
while va < 0x0050A560:
    i = ins_at(va)
    if i is None:
        break
    if i[3] == "call" and "0x50a240" in i[4]:
        log("  (slot0) %08X  %-14s %-8s %s   <== dtor body call with ecx=this" % (va, i[2], i[3], i[4]))
        found = True
        break
    va += i[1]
if not found:
    log("  (slot0) call 0x50A240 NOT FOUND in 0x50A460..0x50A560")

log("")
log("== C5: positive control window 0x0050A050..0x0050A07F ==")
va = 0x0050A050
while va < 0x0050A080:
    i = ins_at(va)
    if i is None:
        break
    tag = ""
    if va == 0x0050A057:
        tag = " <== (a) mov esi,ecx"
    if va == 0x0050A05B:
        tag = " <== (a) mov ecx,[esi+0x30]"
    if va == 0x0050A05E:
        tag = " <== (c) mov edx,[ecx]"
    if va == 0x0050A061:
        tag = " <== (c) mov eax,[edx+0x44]"
    if va == 0x0050A064:
        tag = " <== (c) call eax"
    if va == 0x0050A075:
        tag = " (window contains call 0x437f70 INSTRUCTION - window re-read allowed)"
    log("  %08X  %-14s %-8s %s%s" % (va, i[2], i[3], i[4], tag))
    va += i[1]
# ECX clobber between 0x50A05B and 0x50A064:
va = 0x0050A05E
clob = []
while va < 0x0050A064:
    i = ins_at(va)
    if i is None:
        break
    if i[4].startswith("ecx,") or (i[3] == "pop" and i[4] == "ecx"):
        clob.append(va)
    va += i[1]
log("  ECX-clobber insns in 0x50A05E..0x50A064: %s -> %s" % (clob, "FAIL" if clob else "NONE (PASS)"))

log("")
log("== C4: RTTI walks (own walker; every dword from physical bytes) ==")
def rtti(vt_va, tag):
    log("  -- %s: vtable 0x%08X (section %s)" % (tag, vt_va, sec_of(vt_va)))
    colptr = rd32(vt_va - 4)
    log("     [vtable-4] @0x%08X raw=%s -> COL 0x%08X" % (vt_va - 4, rd(vt_va - 4, 4).hex(), colptr))
    colraw = rd(colptr, 0x14)
    sig, off, cd, ptd, pchd = struct.unpack("<IIIII", colraw)
    log("     COL raw=%s sig=%d off=%d cd=%d ptd=0x%08X pchd=0x%08X" % (colraw.hex(), sig, off, cd, ptd, pchd))
    assert sig == 0
    vf, sp = struct.unpack("<II", rd(ptd, 8))
    nb = rd(ptd + 8, 48)
    z = nb.find(b"\0")
    name = nb[:z if z >= 0 else 48].decode("ascii", "replace")
    log("     TD 0x%08X vfptr=0x%08X spare=0x%08X" % (ptd, vf, sp))
    log("     TD+0x08 name bytes = %s" % nb[:z].hex())
    log("     name = %r" % name)
    # label check: bytes at TD+0x0C (what the contract label would read)
    log("     (label check) bytes at TD+0x0C = %r" % rd(ptd + 0x0C, 24))
    return name

n1 = rtti(0x00A7D458, "CALIBRATION SceneFeederObject")
log("     CALIBRATION expected '.?AVSceneFeederObject@@' -> %s" % ("PASS" if n1 == ".?AVSceneFeederObject@@" else "FAIL"))
n2 = rtti(0x00A8CCF4, "LINK object")
n3 = rtti(0x00A8CCE0, "SECONDARY embedded vtable")

log("")
log("== C4/C6: SF vtable slots 0..5 + NiNode vtable extent + slot17 ==")
for k in range(6):
    log("  SF vtable[%d] @0x%08X = 0x%08X" % (k, 0x00A7D458 + 4 * k, rd32(0x00A7D458 + 4 * k)))
cnt = 0
va = 0x00A8CCF4
while True:
    v = rd32(va)
    if v is None or not (0x00401000 <= v < 0x00A75000):
        break
    cnt += 1
    va += 4
log("  NiNode vtable code-pointer entries from 0x00A8CCF4: %d" % cnt)
log("  entry count includes 0x007B6000? %s" % ("YES" if any(rd32(0x00A8CCF4 + 4 * k) == 0x007B6000 for k in range(cnt)) else "NO"))
log("  slot17 [0x00A8CCF4+0x44]=[0x%08X] = 0x%08X" % (0x00A8CCF4 + 0x44, rd32(0x00A8CCF4 + 0x44)))
log("  slot17 in .text? %s" % ("YES" if 0x00401000 <= rd32(0x00A8CCF4 + 0x44) < 0x00A75000 else "NO"))

log("")
log("== C2 aux: imm32 0x00A7D458 byte pattern in .text (own scan) ==")
_text = None
for nm, sva, vs, rs, rp in SECS:
    if nm == ".text":
        _text = (sva, vs, rs, rp)
sva, vs, rs, rp = _text
tb = data[rp:rp + rs]
hits = []
start = 0
pat = bytes.fromhex("58d4a700")
while True:
    i = tb.find(pat, start)
    if i < 0:
        break
    hits.append(0x401000 + i)
    start = i + 1
log("  hits: %s" % ", ".join("0x%08X" % h for h in hits))
log("  (assert expects exactly [0x00509369, 0x0050A26B] per census.py)")

log("")
log("== C2 aux: E8 callsites census (own) ==")
def calls_to(target):
    res = []
    for i in range(len(tb) - 5):
        if tb[i] == 0xE8:
            rel = struct.unpack_from("<i", tb, i + 1)[0]
            if 0x401000 + i + 5 + rel == target:
                res.append(0x401000 + i)
    return res
log("  E8 -> 0x00509330 (SF ctor): %s" % ", ".join("0x%08X" % c for c in calls_to(0x00509330)))
cr = calls_to(0x005247C0)
log("  E8 -> 0x005247C0 (create fn): %s" % ", ".join("0x%08X" % c for c in cr))
abscount = 0
start = 0
apat = struct.pack("<I", 0x00509330)
while True:
    i = data.find(apat, start)
    if i < 0:
        break
    abscount += 1
    start = i + 1
log("  absolute dword 0x00509330 in WHOLE file: %d occurrences" % abscount)

log("")
log("== C9: SF durable-slot stores after each create callsite (own check) ==")
for c in cr:
    va = c + 5
    end = va + 0x20
    while va < end:
        i = ins_at(va)
        if i is None:
            break
        if i[3] == "mov" and "," in i[4]:
            dst, srcq = [x.strip() for x in i[4].split(",", 1)]
            if srcq == "eax" and dst.startswith("dword ptr [") and dst.endswith("]"):
                log("  callsite 0x%08X -> store 0x%08X: %s %s" % (c, va, i[3], i[4]))
                break
        va += i[1]

log("")
log("== coverage (ii): SF stack-slot holders ==")
show(0x0047D04A, "mov [esp+0x60],eax (SF spill, FUN_0047CCF0)", expect="89442460")
# scan FUN_005247C0 for a spill of esi to [esp+0x2c]
va = 0x005247C0
found2 = None
while va < 0x00524900:
    i = ins_at(va)
    if i is None:
        break
    if i[3] == "mov" and i[4].replace(" ", "") == "dword ptr [esp + 0x2c], esi":
        found2 = va
        log("  FUN_005247C0 spill at 0x%08X: %s %s" % (va, i[3], i[4]))
    va += i[1]
if found2 is None:
    log("  FUN_005247C0: no 'mov [esp+0x2c],esi' found in 0x5247C0..0x524900 - checking other spill forms")
    va = 0x005247C0
    while va < 0x00524900:
        i = ins_at(va)
        if i is None:
            break
        if "esp + 0x2c" in i[4] and i[3] == "mov":
            log("    candidate spill 0x%08X: %s %s" % (va, i[3], i[4]))
        va += i[1]

log("")
log("== coverage (iv): SF ctor rep movsd targets (own decode) ==")
va = 0x00509430
edi_def = {}
while va < 0x00509480:
    i = ins_at(va)
    if i is None:
        break
    if i[3] in ("movsd", "rep movsd") or (i[3] == "movsd" and "dword" in i[4]):
        log("  %08X  %-10s %-10s %s   (edi last def: %s)" % (va, i[2], i[3], i[4], edi_def.get("edi", "?")))
    if i[3] == "lea" and i[4].startswith("edi,"):
        edi_def["edi"] = "0x%08X lea %s" % (va, i[4])
    if i[3] == "mov" and i[4].startswith("edi,"):
        edi_def["edi"] = "0x%08X mov %s" % (va, i[4])
    va += i[1]

log("")
log("== C9 aux: SF re-receive example 0x00529020 ==")
show(0x00529020, "expected mov ecx,[esi+0xc0]", expect="8b8ec0000000")
va = 0x00529020
while va < 0x00529040:
    i = ins_at(va)
    if i is None:
        break
    if i[3] == "call":
        log("  %08X  %-14s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]

log("")
log("== REPORT C2 claim: 'ctor E8 callers = {0x0047D043, 0x0052480F}' creation paths new(0x98) ==")
show(0x005247E7, "push 0x98", expect="6898000000")
show(0x005247EC, "call 0x95d3c4", expect="e8d38b4300")
show(0x0052480F, "call 0x509330", expect="e81c4bfeff")
show(0x00524814, "mov esi,eax", expect="8bf0")
show(0x0047CFC6, "push 0x98 (chain b)", expect="6898000000")
show(0x0047CFDE, "call 0x95d3c4 (chain b)", expect="e8e1034e00")
show(0x0047D043, "call 0x509330 (chain b)", expect="e8e8c20800")
show(0x0047D048, "mov ebx,eax (chain b)", expect="8bd8")
# thunk identity: 0x95D3C4 -> jmp [IAT]
b = rd(0x95D3C4, 6)
iat = struct.unpack_from("<I", b, 2)[0] if b[0] == 0xFF and b[1] == 0x25 else None
log("  thunk 0x0095D3C4 bytes=%s -> IAT 0x%08X" % (b.hex(), iat))
# resolve the import name via own import-table walk
imp_rva = struct.unpack_from("<I", data, opt_off + 96 + 8)[0]
imp_off = off_of(imgbase + imp_rva)
resolved = None
o = imp_off
while True:
    ilt, ts, fc, namerva, iatrva = struct.unpack_from("<IIIII", data, o)
    if ilt == 0 and namerva == 0 and iatrva == 0:
        break
    dlloff = off_of(imgbase + namerva)
    dll = data[dlloff:data.index(b"\0", dlloff)].decode()
    k = 0
    while True:
        ent = struct.unpack_from("<I", data, off_of(imgbase + iatrva + 4 * k))[0]
        if ent == 0:
            break
        if imgbase + iatrva + 4 * k == iat:
            no = off_of(imgbase + ent + 2)
            nm = data[no:data.index(b"\0", no)].decode()
            resolved = "%s.%s" % (dll, nm)
            break
        k += 1
    o += 20
log("  IAT resolve: %s" % resolved)

open(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914\00_CONTROL\qc_probe\out_qc2_bytes.txt", "w").write("\n".join(OUT) + "\n")
log("")
log("QC2 DONE")
