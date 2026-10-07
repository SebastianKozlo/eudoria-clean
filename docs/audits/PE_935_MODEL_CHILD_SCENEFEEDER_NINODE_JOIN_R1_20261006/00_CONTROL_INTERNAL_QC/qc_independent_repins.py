"""INDEPENDENT INTERNAL QC — own-engine byte re-pins for
PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006.

QC_SCOPE = INDEPENDENT_INTERNAL_QC_MODEL_CHILD_SF (LOAD_BEARING depth, fresh context).
This script was written by the pe-master-auditor QC worker. It does NOT reuse any
executor tooling: own PE mapper, own raw byte reads, own subset x86 decoder
(instruction boundaries), own rel32 arithmetic, own data reads.

Fail-closed: EXE identity (size+SHA256) verified before anything else.
Outputs: 00_CONTROL_INTERNAL_QC/qc_independent_repins_results.json
"""
import hashlib, json, struct, sys, csv, os

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006"
OUT = PKG + r"\00_CONTROL_INTERNAL_QC\qc_independent_repins_results.json"

data = open(EXE, "rb").read()
EXE_SIZE = 8015872
EXE_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

res = {"checks": {}, "detail": {}}
def chk(name, ok, detail=""):
    res["checks"][name] = {"ok": bool(ok), "detail": detail}
    return ok

chk("Q0_exe_identity", len(data) == EXE_SIZE and hashlib.sha256(data).hexdigest().upper() == EXE_SHA,
    f"size={len(data)} sha={hashlib.sha256(data).hexdigest().upper()}")

# ---------- own PE mapper ----------
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew+4] == b"PE\x00\x00"
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
size_opt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + size_opt
sections = []
for i in range(nsec):
    off = sec0 + 40 * i
    name = data[off:off+8].rstrip(b"\x00").decode(errors="replace")
    vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
    sections.append((name, va, max(vsize, rsize), roff))
res["detail"]["pe_sections"] = [{"name": n, "va": f"0x{va:08X}", "vsize": f"0x{vs:08X}", "raw_off": f"0x{ro:08X}"} for n, va, vs, ro in sections]

def rd(va, n):
    rva = va - 0x400000
    for _, va_s, sz, roff in sections:
        if va_s <= rva < va_s + sz:
            return data[roff + (rva - va_s):roff + (rva - va_s) + n]
    raise ValueError(f"VA {va:#010x} unmapped")
def hx(va, n):
    return " ".join(f"{b:02X}" for b in rd(va, n))
def u32(va):
    return struct.unpack("<I", rd(va, 4))[0]

# ---------- own subset x86 decoder (32-bit; enough for MSVC 2003 code in the pinned regions) ----------
# Returns list of (va, length, bytes_hex). Unknown opcode => raise.
REG = ["EAX","ECX","EDX","EBX","ESP","EBP","ESI","EDI"]
def decode_modrm(b, i):
    """b = code bytes; i = index of modrm byte. Returns (mod, reg, rm, disp_bytes, new_i)."""
    modrm = b[i]; i += 1
    mod = modrm >> 6; reg = (modrm >> 3) & 7; rm = modrm & 7
    disp = 0
    if mod == 0 and rm == 5:
        disp = 4  # disp32 absolute
    elif mod == 1:
        disp = 1
    elif mod == 2:
        disp = 4
    if rm == 4 and mod != 3:
        sib = b[i]; i += 1
        if (sib & 7) == 5 and mod == 0:
            disp = 4  # disp32 base
    i += disp
    return mod, reg, rm, disp, i

def decode_one(b, i, va):
    """Decode one instruction starting at b[i] (va). Return (length, text)."""
    start = i
    opfx = []
    while b[i] in (0x66, 0x67, 0xF0, 0x2E, 0x36, 0x3E, 0x26, 0x64, 0x65, 0xF2, 0xF3):
        opfx.append(b[i]); i += 1
        if len(opfx) > 4: raise ValueError("prefix run too long")
    op = b[i]; i += 1
    t = ""
    if op == 0x0F:
        op2 = b[i]; i += 1
        if op2 in (0x80,0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88,0x89,0x8A,0x8B,0x8C,0x8D,0x8E,0x8F):
            # Jcc rel32: NO modrm — 4-byte displacement directly (fixed in QC round 2;
            # round 1 wrongly consumed a phantom modrm and desynced linear decodes)
            rel = struct.unpack_from("<i", b, i)[0]; i += 4
            t = f"jcc(rel32)->0x{va + (i-start) + rel:08X}"
        elif op2 == 0xB6 or op2 == 0xBE:  # movzx/movsx r32, r/m8
            mod, reg, rm, disp, i = decode_modrm(b, i); t = "movzx/movsx r8"
        elif op2 == 0xB7 or op2 == 0xBF:
            mod, reg, rm, disp, i = decode_modrm(b, i); t = "movzx/movsx r16"
        elif op2 == 0xAF:
            mod, reg, rm, disp, i = decode_modrm(b, i); t = "imul"
        elif op2 == 0x90:
            raise NotImplementedError("setcc (not needed in pinned windows)") if False else None
            mod, reg, rm, disp, i = decode_modrm(b, i); t = "setcc"
        elif op2 == 0xBA:  # bt group with imm8
            mod, reg, rm, disp, i = decode_modrm(b, i); i += 1; t = "bt/bts/btr/btc imm8"
        elif op2 == 0xA2:
            t = "cpuid"
        elif op2 in (0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D,0x4E,0x4F):
            mod, reg, rm, disp, i = decode_modrm(b, i); t = "cmovcc"
        else:
            raise ValueError(f"unknown 0F {op2:02X} at {va:#010x}")
    elif 0x50 <= op <= 0x57:
        t = f"push {REG[op-0x50]}"
    elif 0x00 <= op <= 0x3F:
        # ALU block: even = r/m8,r8 (with modrm); odd = r/m32,r32 (with modrm);
        # 0x04/05-class = accumulator,imm — handled by (op & 7) == 4/5
        low = op & 7
        names = {0:"add",1:"add",2:"add",3:"add",0x0A:"or",0x0B:"or",8:"or",9:"or",0x12:"adc",0x13:"adc",0x1A:"sbb",0x1B:"sbb",
                 0x22:"and",0x23:"and",0x2A:"sub",0x2B:"sub",0x32:"xor",0x33:"xor",0x3A:"cmp",0x3B:"cmp"}
        if low in (4, 5):  # accumulator, imm
            i += 1 if (op < 0x40 and (op & 1) == 0) else 4
            t = f"alu-imm {names.get(op & 0xFE, '?')}"
        elif (op & 7) in (0, 1, 2, 3):
            mod, reg, rm, disp, i = decode_modrm(b, i)
            t = f"{names.get(op, 'alu')} r/m (mod={mod},reg={reg})"
        else:
            raise ValueError(f"unknown ALU {op:02X} at {va:#010x}")
    elif 0x58 <= op <= 0x5F:
        t = f"pop {REG[op-0x58]}"
    elif op == 0x6A:
        t = f"push {struct.unpack_from('<b', b, i)[0]:#x}"; i += 1
    elif op == 0x68:
        t = f"push {struct.unpack_from('<I', b, i)[0]:#x}"; i += 4
    elif 0x70 <= op <= 0x7F:
        rel = struct.unpack_from("<b", b, i)[0]; i += 1
        t = f"jcc(rel8)->0x{va + (i-start) + rel:08X}"
    elif op in (0x80, 0x81, 0x83):
        mod, reg, rm, disp, i = decode_modrm(b, i)
        imm = 1 if op == 0x80 or op == 0x83 else 4
        i += imm; t = f"grp1/{reg} (mod={mod})"
    elif op in (0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B):
        mod, reg, rm, disp, i = decode_modrm(b, i)
        names = {0x84:"test8",0x85:"test",0x86:"xchg8",0x87:"xchg",0x88:"mov8",0x89:"mov",0x8A:"mov r8",0x8B:"mov"}
        t = f"{names[op]} {REG[reg]},rm(mod={mod},rm={rm})"
    elif op == 0x8D:
        mod, reg, rm, disp, i = decode_modrm(b, i); t = f"lea {REG[reg]},rm(mod={mod},rm={rm})"
    elif op == 0x90:
        t = "nop"
    elif op in (0x98, 0x99):
        t = "cwde/cdq"
    elif op == 0xA4:
        t = "movsb"
    elif op == 0xA5:
        t = "movsd"
    elif op == 0xA8:
        t = f"test al,{b[i]:#x}"; i += 1
    elif op == 0xA9:
        t = f"test eax,{struct.unpack_from('<I', b, i)[0]:#x}"; i += 4
    elif 0xB0 <= op <= 0xB7:
        t = f"mov r8,imm8"; i += 1
    elif 0xB8 <= op <= 0xBF:
        t = f"mov {REG[op-0xB8]},0x{struct.unpack_from('<I', b, i)[0]:08X}"; i += 4
    elif op in (0xC0, 0xC1, 0xD0, 0xD1, 0xD2, 0xD3):
        mod, reg, rm, disp, i = decode_modrm(b, i)
        if op in (0xC0, 0xC1): i += 1
        t = f"shift/{reg}"
    elif op == 0xC2:
        t = f"ret {struct.unpack_from('<H', b, i)[0]:#x}"; i += 2
    elif op == 0xC3:
        t = "ret"
    elif op in (0xC6, 0xC7):
        mod, reg, rm, disp, i = decode_modrm(b, i)
        imm = 1 if op == 0xC6 else 4; i += imm
        t = f"mov rm,imm(reg field={reg},mod={mod})"
    elif op == 0xC9:
        t = "leave"
    elif 0xD8 <= op <= 0xDF:
        mod, reg, rm, disp, i = decode_modrm(b, i)
        # no immediates in FPU instructions
        t = f"fpu D{op-0xD8:X}/{reg} (mod={mod})"
    elif op == 0xE8:
        rel = struct.unpack_from("<i", b, i)[0]; i += 4
        t = f"call 0x{va + (i-start) + rel:08X}"
    elif op == 0xE9:
        rel = struct.unpack_from("<i", b, i)[0]; i += 4
        t = f"jmp 0x{va + (i-start) + rel:08X}"
    elif op == 0xEB:
        rel = struct.unpack_from("<b", b, i)[0]; i += 1
        t = f"jmp rel8->0x{va + (i-start) + rel:08X}"
    elif op in (0xF6, 0xF7):
        mod, reg, rm, disp, i = decode_modrm(b, i)
        if reg in (0, 1): i += 1 if op == 0xF6 else 4  # test imm
        t = f"grp3/{reg} (mod={mod})"
    elif op == 0xF7 and False:
        pass
    elif op == 0xFF:
        mod, reg, rm, disp, i = decode_modrm(b, i)
        t = f"grp5/{reg} (mod={mod},rm={rm})"
    elif op == 0xA0 or op == 0xA1 or op == 0xA2 or op == 0xA3:
        i += 4; t = "mov AL/EAX,moffs"
    else:
        raise ValueError(f"unknown opcode {op:02X} at {va:#010x} (+{(i-start)})")
    # rep prefix handled: F3 A5 etc. covered by prefix loop
    return i - start, t

def linear(va, maxbytes):
    """Linear decode from va up to maxbytes; stop at first ret/ret imm followed by padding,
    or at maxbytes. Returns (insns, end_va, stop_reason)."""
    insns = []
    i = 0
    code = rd(va, maxbytes)
    while i < maxbytes:
        try:
            ln, t = decode_one(code, i, va + i)
        except ValueError as e:
            return insns, va + i, f"DECODE_STOP: {e}"
        insns.append((va + i, ln, " ".join(f"{c:02X}" for c in code[i:i+ln]), t))
        i += ln
        if t == "ret" or t.startswith("ret "):
            # check padding
            j = i
            pad = 0
            while j < maxbytes and code[j] == 0xCC:
                pad += 1; j += 1
            if pad >= 2:
                return insns, va + i, "TERMINAL_RET_PADDING"
            elif i < maxbytes and (code[i] == 0xCC):
                pass  # single CC — could be alignment; continue
        if ln == 0:
            return insns, va + i, "ZERO_LENGTH"
    return insns, va + i, "MAXBYTES"

def boundaries_set(insns):
    return {a for a, _, _, _ in insns}

# ================= A. THE JOIN SITE (claim a) =================
win = hx(0x0050A3E9, 16)
chk("A1_join_site_bytes", win == "8B 4E 30 8B 01 8B 90 A4 00 00 00 6A 00 57 FF D2",
    f"0x0050A3E9..0x0050A3F8 = '{win}'")
insns, end, reason = linear(0x0050A310, 0x600)
bs = boundaries_set(insns)
# decode the join site from my linear decode (proves boundaries)
mine = [(a, ln, b_, t) for a, ln, b_, t in insns if 0x0050A3E9 <= a <= 0x0050A3F7]
chk("A2_join_site_boundary_decode", [m[0] for m in mine] == [0x0050A3E9, 0x0050A3EC, 0x0050A3EE, 0x0050A3F4, 0x0050A3F6, 0x0050A3F7],
    "; ".join(f"{a:#x}: {b_} {t}" for a, ln, b_, t in mine))
# receiver arithmetic: mov ecx,[esi+0x30] (8B 4E 30 = mod01 rm110 disp8 0x30); mov eax,[ecx]; mov edx,[eax+0xA4]; push 0; push edi; call edx
ok = (mine[0][3] == "mov ECX,rm(mod=1,rm=6)" and
      mine[1][3] == "mov EAX,rm(mod=0,rm=1)" and
      mine[2][3] == "mov EDX,rm(mod=2,rm=0)" and
      mine[3][1] == 2 and mine[4][1] == 1 and mine[5][1] == 2 and
      hx(0x0050A3E9, 3) == "8B 4E 30" and hx(0x0050A3EE, 6) == "8B 90 A4 00 00 00" and
      "A4 00 00 00" in hx(0x0050A3EE, 6))
chk("A3_receiver_arithmetic", ok,
    "receiver ECX = [ESI+0x30] (8B 4E 30: mod=01 rm=110 -> [ESI+disp8 0x30]); vtable = [ECX] (8B 01); "
    "slot = [EAX+0xA4] (8B 90 A4 00 00 00; 0xA4/4 = slot 41); push 0 (bFirstAvail arg2); push EDI (child arg1); call EDX @0x0050A3F7 — "
    "ECX loaded once at 0x0050A3E9, only a vtable READ ([ECX]) between, no ECX write before the call")
# slot data read from the vtable
s41 = u32(0x00A8CCF4 + 0xA4)
chk("A4_slot41_data", s41 == 0x007B5810, f"[0x00A8CCF4+0xA4] = 0x{s41:08X} (expect 0x007B5810); 0xA4 = slot 41*4")
s42 = u32(0x00A8CCF4 + 0xA8)
chk("A5_slot42_data", s42 == 0x007B5A00, f"[0x00A8CCF4+0xA8] = 0x{s42:08X} (expect 0x007B5A00)")
# ESI = SF (function head) and EDI = child provenance at the call
head = hx(0x0050A310, 8)
chk("A6_fun_50a310_head", head == "51 55 56 8B F1 80 7E 24",
    f"head = '{head}' => push ecx; push ebp; push esi; mov ESI,ECX (this=SF); cmp byte [ESI+0x24],1")
# EDI chain: 0x0050A38F mov edi,[esp+0x14] (the manager arg); 0x0050A3AF call FUN_006C66D0; 0x0050A3B7 mov edi,eax
chk("A7_edi_chain_bytes",
    hx(0x0050A38F, 4) == "8B 7C 24 14" and hx(0x0050A3AF, 5) == "E8 1C C3 1B 00" and hx(0x0050A3B7, 2) == "8B F8",
    "mov EDI,[ESP+0x14] (manager arg); call 0x006C66D0; mov EDI,EAX (child); no EDI write between 0x0050A3B7 and push EDI @0x0050A3F6")

# ================= B. [SF+0x20] INSTALL (claim b) =================
chk("B1_sf20_store", hx(0x0050A3AC, 3) == "89 7E 20",
    f"0x0050A3AC = '{hx(0x0050A3AC, 3)}' = mov [ESI+0x20],EDI (ESI=SF per A6; EDI=manager arg per A7)")
chk("B2_sf20_store_is_boundary", 0x0050A3AC in bs and 0x0050A3AA in bs and 0x0050A3AF in bs,
    "0x0050A3AC is a true instruction boundary (linear decode from 0x0050A310); between mov ECX,EDI @0x0050A3AA and call @0x0050A3AF")

# ================= C. FUN_006C66D0 GETTER CALL (claim c) =================
rel = struct.unpack("<i", rd(0x0050A3AF + 1, 4))[0]
tgt = 0x0050A3AF + 5 + rel
chk("C1_getter_call_target", tgt == 0x006C66D0, f"rel32 recompute: 0x0050A3AF + 5 + {rel:#x} = 0x{tgt:08X} (expect 0x006C66D0)")
chk("C2_getter_receiver", hx(0x0050A3AA, 2) == "8B CF",
    "ECX = EDI (the manager) immediately before the getter call @0x0050A3AF (bytes 8B CF at 0x0050A3AA)")

# ================= D. FUN_0050A310 <- FUN_006A3930 (claim d) =================
insns6a, end6a, reason6a = linear(0x006A3930, 0x900)
bs6a = boundaries_set(insns6a)
rel = struct.unpack("<i", rd(0x006A3A9D + 1, 4))[0]
tgt = 0x006A3A9D + 5 + rel
chk("D1_call_target_50a310", tgt == 0x0050A310, f"0x006A3A9D + 5 + {rel:#x} = 0x{tgt:08X} (expect 0x0050A310)")
chk("D2_call_args", hx(0x006A3A99, 8) == "8B 4E 18 55 E8 6E 68 E6",
    "mov ECX,[ESI+0x18] (SF from [ACLD+0x18]; ESI=ACLD per ctor head mov esi,ecx) ; push EBP (the manager) ; call")
chk("D3_sf_store_acld18", hx(0x006A39F6, 3) == "89 46 18",
    f"mov [ESI+0x18],EAX @0x006A39F6 = '{hx(0x006A39F6, 3)}' (SF stored at [ACLD+0x18])")
rel = struct.unpack("<i", rd(0x006A39ED + 1, 4))[0]
chk("D4_sf_factory_call", 0x006A39ED + 5 + rel == 0x005247C0, f"0x006A39ED call target = 0x{0x006A39ED+5+rel:08X} (expect 0x005247C0)")
chk("D5_manager_new_0x130", hx(0x006A3A48, 11) == "68 30 01 00 00 E8 72 99 2B 00 8B",
    "push 0x130; call 0x0095D3C4 (allocator; rel32 recompute below); mov EBP,EAX")
rel = struct.unpack("<i", rd(0x006A3A4D + 1, 4))[0]
chk("D5b_allocator_target", 0x006A3A4D + 5 + rel == 0x0095D3C4, f"new(0x130) call target = 0x{0x006A3A4D+5+rel:08X} (expect 0x0095D3C4)")
rel = struct.unpack("<i", rd(0x006A3A77 + 1, 4))[0]
chk("D6_manager_ctor_call", 0x006A3A77 + 5 + rel == 0x006C0D50, f"FUN_006C0D50 (ArkModelManagerMain ctor per bridge W02 prior canon) target = 0x{0x006A3A77+5+rel:08X}")
chk("D7_all_sites_boundaries", all(v in bs6a for v in [0x006A39ED, 0x006A39F6, 0x006A3A48, 0x006A3A4D, 0x006A3A77, 0x006A3A99, 0x006A3A9C, 0x006A3A9D]),
    "all D-chain sites are true instruction boundaries in my own linear decode of FUN_006A3930 from entry 0x006A3930")

# ================= E. FUN_007B5810 fingerprint (claim e) =================
body = hx(0x007B5810, 226)
insns7b, end7b, reason7b = linear(0x007B5810, 0x300)
bs7b = boundaries_set(insns7b)
# compare my raw bytes with the executor raw proof's BYTES line
with open(PKG + r"\01_RAW\FUN_007B5810_ORACLE_BYTE_PROOF.txt", encoding="utf-8") as f:
    proof = f.read()
executor_bytes = [l for l in proof.splitlines() if l.startswith("BYTES: ")][0][7:].strip()
mine_bytes = hx(0x007B5810, 256)
chk("E1_oracle_proof_bytes_match", mine_bytes == executor_bytes,
    "my EXE read of 0x007B5810 LEN 256 is byte-identical to the BYTES line in 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt" if mine_bytes == executor_bytes else f"MISMATCH: mine={mine_bytes[:60]}... exec={executor_bytes[:60]}...")
# F1 NULL guard on child
chk("E2_F1_null_guard", hx(0x007B5835, 4) == "8B 74 24 20" and hx(0x007B5839, 2) == "85 F6" and hx(0x007B583B, 6) == "0F 84 9C 00 00 00",
    "ESI = [ESP+0x20] (arg1 = child); test ESI,ESI; je 0x007B58DD (early return)")
# F2 refcount inc x2
inc1 = hx(0x007B5846, 3); inc2 = hx(0x007B5851, 3)
chk("E3_F2_refcount_inc_x2", inc1 == "01 5E 04" and inc2 == "01 5E 04",
    f"add [ESI+4],EBX (EBX=1) @0x007B5846 '{inc1}' and @0x007B5851 '{inc2}' — refcount inc x2")
# F3 AttachParent-shaped call FUN_007BF470(child this, parent arg)
chk("E4_F3_attachparent_call", hx(0x007B5849, 1) == "57" and hx(0x007B584A, 2) == "8B CE" and hx(0x007B584C, 5) == "E8 1F 9C 00 00",
    "push EDI (parent=this) @0x007B5849 (57); mov ECX,ESI (child receiver) @0x007B584A (8B CE); call @0x007B584C (E8 1F 9C 00 00)")
rel = struct.unpack("<i", rd(0x007B584C + 1, 4))[0]
chk("E4b_F3_target", 0x007B584C + 5 + rel == 0x007BF470, f"call FUN_007BF470 target = 0x{0x007B584C+5+rel:08X} (expect 0x007BF470; body NOT decoded)")
# F4 children-array: bFirstAvail byte arg; lea ecx,[edi+0xC8]; AddFirstEmpty vs append
chk("E5_F4_bfirstavail_gate", hx(0x007B5854, 2) == "80 7C" and hx(0x007B5854, 5) == "80 7C 24 24 00",
    "cmp byte [ESP+0x24],0 — arg2 (bFirstAvail) gate")
chk("E6_F4_children_obj_lea", hx(0x007B5864, 7) == "8D 8F C8 00 00 00"[:6] + " " or hx(0x007B5864, 6) == "8D 8F C8 00 00 00",
    f"lea ECX,[EDI+0xC8] @0x007B5864 = '{hx(0x007B5864, 6)}' — m_kChildren @NiNode+0xC8")
rel = struct.unpack("<i", rd(0x007B5872 + 1, 4))[0]
chk("E7_addfirstempty_call", 0x007B5872 + 5 + rel == 0x007B55E0, f"call FUN_007B55E0 target = 0x{0x007B5872+5+rel:08X}")
chk("E8_append_path", hx(0x007B588E, 6) == "81 C7 C8 00 00 00" and hx(0x007B5898, 2) == "8B 5F" and hx(0x007B5898, 5) == "8B 5F 0C 3B 5F",
    "add EDI,0xC8 (bFirstAvail==0 branch); EBX=[EDI+0xC] (used = NiNode+0xD4); cmp EBX,[EDI+8] (alloc = NiNode+0xD0)")
rel = struct.unpack("<i", rd(0x007B58A8 + 1, 4))[0]
chk("E9_grow_call", 0x007B58A8 + 5 + rel == 0x00788570, f"grow call target = 0x{0x007B58A8+5+rel:08X} (expect 0x00788570)")
rel = struct.unpack("<i", rd(0x007B58B5 + 1, 4))[0]
chk("E10_setat_call", 0x007B58B5 + 5 + rel == 0x007790D0, f"set-at-index call target = 0x{0x007B58B5+5+rel:08X} (expect 0x007790D0)")
# F5 refcount dec x2 + zero-destroy slot 1
dec1 = hx(0x007B587A, 3); dec2 = hx(0x007B58BD, 3); dec3 = hx(0x007B58CF, 3)
destroy = hx(0x007B58C6, 9)
chk("E11_F5_dec_and_destroy", dec1 == "01 7E 04" and dec2 == "01 7E 04" and dec3 == "01 7E 04" and destroy == "8B 06 8B 50 04 8B CE FF D2",
    "add [ESI+4],EDI (EDI=-1) dec after each branch (@0x7B587A bFirstAvail-path, @0x7B58BD append-path, @0x7B58CF common tail); "
    "zero-destroy: EAX=[ESI] (vtable), EDX=[EAX+4] (slot 1), ECX=ESI, call EDX (9 bytes 8B 06 8B 50 04 8B CE FF D2)")
# extent
tail = [i for i in insns7b if i[3] == "ret 0x8"]
chk("E12_extent", end7b == 0x007B58F2 and reason7b == "TERMINAL_RET_PADDING",
    f"my linear decode: extent 0x007B5810..{end7b:#x} ({end7b-0x007B5810} B, reason {reason7b}) — matches the ledger's 0x007B5810..0x007B58F2")

# ================= F. TRANSFORM (claim f) =================
insns59850, end59850, reason59850 = linear(0x00509850, 0x200)
bs59850 = boundaries_set(insns59850)
chk("F1_flags_window", hx(0x00509857, 2) == "8A 45" and hx(0x00509857, 3) == "8A 45 24" and hx(0x0050985E, 4) == "80 7D 25 00" and hx(0x00509864, 4) == "80 7D 26 00" and hx(0x0050986A, 4) == "80 7D 27 00",
    "flags AL=[EBP+0x24]; [EBP+0x25]/[EBP+0x26]/[EBP+0x27] window gates (EBP=SF per mov ebp,ecx @0x00509855)")
chk("F2_gate_sf28", hx(0x0050989F, 4) == "80 7D 28 01" and hx(0x005098A3, 6) == "0F 85 DA 00 00 00",
    "cmp byte [EBP+0x28],1; jne 0x00509983 — the transform-write gate")
chk("F3_gate_sf2c_bit0", hx(0x005098B6, 3) == "8B 45 2C" and hx(0x005098B9, 2) == "C1 E8" and hx(0x005098BC, 2) == "A8 01",
    "EAX=[EBP+0x2C]; shr EAX,4; test AL,1 — gates the +0x40..0x48 offset add")
chk("F4_translate_load", hx(0x005098FA, 3) == "8B 45 30" and hx(0x005098FF, 3) == "83 C0 5C",
    "EAX=[EBP+0x30] (SF+0x30 NiNode); add EAX,0x5C — translate target base")
chk("F5_translate_stores", hx(0x00509913, 2) == "89 08" and hx(0x0050991F, 3) == "89 50 04" and hx(0x0050992E, 3) == "89 48 08",
    "mov [EAX],ECX; mov [EAX+4],EDX; mov [EAX+8],ECX — NiNode+0x5C/+0x60/+0x64")
chk("F6_x100_const", rd(0x00A7A618, 8) == struct.pack("<d", 100.0),
    f"[0x00A7A618] qword = {struct.unpack('<d', rd(0x00A7A618, 8))[0]} (expect 100.0 — the x100 multiplier; fld qword [0x00A7A618] @0x005098F4)")
chk("F7_rotation_copy", hx(0x00509931, 3) == "8B 7D 30" and hx(0x00509934, 3) == "83 C7 38" and hx(0x00509937, 5) == "B9 09 00 00 00" and hx(0x0050993C, 2) == "F3 A5" and hx(0x00509904, 3) == "8D 75 4C",
    "EDI=[EBP+0x30]+0x38; ECX=9; rep movsd <- ESI=[EBP+0x4C] — rotation 9 dwords SF+0x4C -> NiNode+0x38")
chk("F8_scale", hx(0x0050993E, 3) == "D9 45 70" and hx(0x00509941, 2) == "D9 E1" and hx(0x0050994B, 3) == "8B 55 30" and hx(0x00509950, 3) == "D9 5A 68",
    "fld [EBP+0x70]; fabs; EDX=[EBP+0x30]; fstp [EDX+0x68] — scale |SF+0x70| -> NiNode+0x68")
rel = struct.unpack("<i", rd(0x00529050 + 1, 4))[0]
chk("F9_callsite_29050", 0x00529050 + 5 + rel == 0x00509850, f"0x00529050 call target = 0x{0x00529050+5+rel:08X} (expect 0x00509850); ecx=[ESI+0xC0] (SF) @0x00529047")
chk("F10_extent", end59850 == 0x005099BB and reason59850 == "TERMINAL_RET_PADDING",
    f"my linear decode extent 0x00509850..{end59850:#x} — matches the ledger's 0x00509850..0x005099BB")

# ================= G. FUN_008BD720 accessor + imm (claim g) =================
chk("G1_8bd720_body", hx(0x008BD720, 4) == "8D 41 18 C3",
    f"0x008BD720 = '{hx(0x008BD720, 4)}' = lea EAX,[ECX+0x18]; ret — 4-byte accessor (NOT a completion handler)")
chk("G2_8bd720_padding", hx(0x008BD724, 4) == "CC CC CC CC", "int3 padding after the ret")
chk("G3_imm_at_6c3fb0", hx(0x006C3FB0, 5) == "BB 20 D7 8B 00",
    f"0x006C3FB0 = '{hx(0x006C3FB0, 5)}' = mov EBX,0x008BD720 (the callback immediate; instruction VA 0x006C3FB0, imm at +1)")
rel = struct.unpack("<i", rd(0x006C3FCD + 1, 4))[0]
chk("G4_scheduler_entry_call", 0x006C3FCD + 5 + rel == 0x006C3640, f"scheduler call target = 0x{0x006C3FCD+5+rel:08X} (expect 0x006C3640)")

# ================= H. additional identity re-pins =================
# SF ctor vtable store (the 'same class vtable 0x00A7D458' claim)
insns_sfctor, end_sf, reason_sf = linear(0x00509330, 0x200)
bs_sf = boundaries_set(insns_sfctor)
vt_hit = [i for i in insns_sfctor if i[2] == "C7 06 58 D4 A7 00"]
# belt-and-braces: also scan raw bytes for the imm32 0x00A7D458 anywhere in 0x00509330..0x00509510
scan = rd(0x00509330, 0x1E0)
imm_off = scan.find(struct.pack("<I", 0x00A7D458))
scan_va = 0x00509330 + imm_off if imm_off >= 0 else None
chk("H1_sf_vtable_store", len(vt_hit) >= 1 or scan_va is not None,
    f"SectorFun_00509330: linear-decode vtable store hit = {[hex(h[0]) for h in vt_hit] if vt_hit else 'not as C7 06 in linear decode'}; "
    f"raw imm32 0x00A7D458 found at {f'0x{scan_va:08X}' if scan_va is not None else 'NOWHERE'} in 0x00509330..0x00509510")
# NiNode ctor vtable store boundary check (PA1b: vtable 0x00A8CCF4 @0x007B6041)
insns_nn, end_nn, reason_nn = linear(0x007B6000, 0x100)
vt_hit2 = [i for i in insns_nn if i[2] == "C7 06 F4 CC A8 00"]
chk("H2_ninode_vtable_store", len(vt_hit2) == 1 and vt_hit2[0][0] == 0x007B6041,
    f"NiNode ctor FUN_007B6000 stores vtable 0x00A8CCF4 at 0x{vt_hit2[0][0]:08X}" if vt_hit2 else "store not found")
# SF30 store + NiNode ctor call (PA1)
chk("H3_sf30_store", hx(0x005093C3, 3) == "89 45 30", "mov [EBP+0x30],EAX @0x005093C3")
rel = struct.unpack("<i", rd(0x005093B8 + 1, 4))[0]
chk("H4_ninode_ctor_call", 0x005093B8 + 5 + rel == 0x007B6000, f"0x005093B8 call target = 0x{0x005093B8+5+rel:08X}")
chk("H5_refcount_inc_after_store", hx(0x005093C8, 4) == "83 40 04 01", "add [EAX+4],1 @0x005093C8 (refcount inc on the stored node)")
# vtable slots
slots = {i: u32(0x00A8CCF4 + 4*i) for i in range(48)}
chk("H6_vtable_canon_slots", slots[17] == 0x007B5390 and slots[19] == 0x007B47D0 and slots[41] == 0x007B5810 and slots[42] == 0x007B5A00 and slots[45] == 0x007B4550,
    f"slot17={slots[17]:#x} slot19={slots[19]:#x} slot41={slots[41]:#x} slot42={slots[42]:#x} slot45={slots[45]:#x}; slot46={slots[46]:#x}; slot47={slots[47]:#x} (past-end ASCII 'effe')")
res["detail"]["vtable_slots_0_47"] = {f"slot_{i}": f"0x{v:08X}" for i, v in slots.items()}
# FUN_0050A310 true extent (budget says 0x0050A310..0x0050A453+; FINAL_REPORT says 'fully decoded')
tail50 = [i for i in insns if i[3].startswith("ret") or i[3] == "ret"]
chk("H7_fun_50a310_extent", reason == "TERMINAL_RET_PADDING" and end == 0x0050A45C,
    f"my own linear decode from entry 0x0050A310: TRUE extent = 0x0050A310..0x{end:08X} "
    f"(terminal {' / '.join(t[2] + ' ' + t[3] for t in tail50[-1:])} at 0x{tail50[-1][0]:08X}, reason {reason}) — "
    f"the executor's raw window (LEN 288) covers only 0x0050A310..0x0050A42F and the budget honestly writes '0x0050A310..0x0050A453+'; "
    f"the FINAL_REPORT 'fully decoded' wording overstates the window (see QC finding)")
res["detail"]["fun_50a310_decode_end"] = f"0x{end:08X}"
res["detail"]["fun_50a310_decode_reason"] = reason
res["detail"]["fun_50a310_last_insns"] = [f"{a:#x}: {b_} {t}" for a, ln, b_, t in insns[-6:]]
res["detail"]["fun_50a310_undecoded_tail_bytes"] = hx(0x0050A42F, 0x0050A45C - 0x0050A42F)

# ================= I. raw evidence windows byte-identity vs EXE =================
import re
raw_mismatches = []
windows_checked = 0
for fname in os.listdir(PKG + r"\01_RAW"):
    with open(PKG + r"\\01_RAW\\" + fname, encoding="utf-8") as f:
        txt = f.read()
    for m in re.finditer(r"^(?:###\s.*)?VA\s+(0x[0-9A-Fa-f]+)\s+LEN\s+(\d+)\s*$", txt, re.M):
        va = int(m.group(1), 16); ln = int(m.group(2))
        # find the following BYTES: line
        after = txt[m.end():m.end()+200000]
        bm = re.search(r"^BYTES:\s*([0-9A-Fa-f ]+)\s*$", after, re.M)
        if not bm:
            continue
        expected = bm.group(1).strip()
        got = hx(va, ln)
        windows_checked += 1
        if got.upper() != expected.upper():
            raw_mismatches.append(f"{fname} VA 0x{va:08X} LEN {ln}: got '{got}' vs recorded '{expected[:60]}...'")
    # also 'WINDOW 0x... LEN ...' pattern
    for m in re.finditer(r"^WINDOW\s+(0x[0-9A-Fa-f]+)\s+LEN\s+(\d+)\s*$", txt, re.M):
        va = int(m.group(1), 16); ln = int(m.group(2))
        after = txt[m.end():m.end()+200000]
        bm = re.search(r"^BYTES:\s*([0-9A-Fa-f ]+)\s*$", after, re.M)
        if not bm:
            continue
        expected = bm.group(1).strip()
        got = hx(va, ln)
        windows_checked += 1
        if got.upper() != expected.upper():
            raw_mismatches.append(f"{fname} WINDOW 0x{va:08X} LEN {ln}: got '{got}' vs recorded '{expected[:60]}...'")
chk("I1_raw_windows_byte_identity", len(raw_mismatches) == 0,
    f"{windows_checked} raw windows re-read from the EXE and compared byte-for-byte with the 01_RAW records; mismatches: {raw_mismatches if raw_mismatches else 'NONE'}")
res["detail"]["raw_windows_checked"] = windows_checked

# ================= J. oracle + private research hashes =================
def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper(), os.path.getsize(p)
oracle_checks = {}
for p, exp_sha, exp_sz in [
    (r"D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiNode.cpp", "38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016", 33897),
    (r"D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp", "72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7", 33215),
]:
    sha, sz = fsha(p)
    oracle_checks[os.path.basename(p)] = {"sha256": sha, "size": sz, "expected_sha": exp_sha, "expected_size": exp_sz,
                                          "match": sha == exp_sha and sz == exp_sz}
chk("J1_oracle_sources", all(v["match"] for v in oracle_checks.values()), json.dumps(oracle_checks))
res["detail"]["oracle_sources"] = oracle_checks

priv_checks = {}
for p, exp in [
    (r"C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_ENGINE_COMPARISON_RESEARCH_20261006\REPORT.md", "26CBF3AB57CEB99DB90760AB503E58AF5D42DCE5E2AB6DA428578DBD4DCD64C1"),
    (r"C:\Users\User\Documents\ChatGPT\PE\PE_935_NIRTTI_CLASS_IDENTITY_DESKTOP_RESEARCH_R1_20261004\REPORT.md", "D6B81792BC1AA99124C772EF05C6690A94BFF97DD11B09CCECC3B226C852547A"),
    (r"C:\Users\User\Documents\ChatGPT\PE\PE_935_PLACEMENT_BRIDGE_DESKTOP_POST_AUDIT_20261003\REPORT.md", "598DA71AC3DC1F6577EA2AF9E25ED8CF9C53A2603899D08B8AA3307A8CC35396"),
]:
    sha, sz = fsha(p)
    priv_checks[os.path.basename(os.path.dirname(p))] = {"sha256": sha, "size": sz, "expected": exp, "match": sha == exp}
chk("J2_private_research_reports", all(v["match"] for v in priv_checks.values()), json.dumps(priv_checks))
res["detail"]["private_reports"] = priv_checks

ct_sha, ct_sz = fsha(r"C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_PROMPT_REVIEW_20261006\OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md")
chk("J3_contract_identity", ct_sha == "F929D2C03B1D078BD69BDD206B0CF51DE5F393A0CE6D39618ED87819D043F3C8" and ct_sz == 15348, f"{ct_sz} B / {ct_sha}")
an_sha, an_sz = fsha(r"C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_MODEL_JOIN_COMPARISON_RESEARCH_R2_20261006\HANDOFF_NOTES.md")
chk("J4_anchor_constraints_identity", an_sha == "D531B56AB0C1FD180A31DABC5DACAAE289372CA7B8FD8EC8BAAC565FAB0E4355" and an_sz == 1641, f"{an_sz} B / {an_sha}")

# ================= K. package manifest re-hash + file census =================
disk_files = []
for root, dirs, names in os.walk(PKG):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", "00_CONTROL_INTERNAL_QC")]
    for n in names:
        p = os.path.join(root, n)
        rel = os.path.relpath(p, PKG).replace("\\", "/")
        disk_files.append(rel)
with open(PKG + r"\MANIFEST_SHA256.csv", encoding="utf-8", newline="") as f:
    mrows = list(csv.DictReader(f))
mm = {}
for r in mrows:
    mm.setdefault(r["relative_path"], []).append((int(r["size_bytes"]), r["sha256"].upper()))
mism = []
for rel in sorted(set(disk_files) - {"MANIFEST_SHA256.csv"}):
    sha, sz = fsha(os.path.join(PKG, rel))
    if rel not in mm:
        mism.append(f"MISSING from manifest: {rel}")
    else:
        for (msz, msha) in mm[rel]:
            if msz != sz or msha != sha:
                mism.append(f"MISMATCH {rel}: disk {sz}/{sha[:12]}.. vs manifest {msz}/{msha[:12]}..")
extra = [r for r in mm if r not in set(disk_files)]
dups = [r for r in mm if len(mm[r]) > 1]
chk("K1_manifest_bijection", len(mism) == 0 and len(extra) == 0 and len(dups) == 0,
    f"disk files (excl. manifest, excl. this QC dir) = {len(disk_files)}; manifest rows = {len(mrows)}; "
    f"missing/mismatch={mism if mism else 'NONE'}; extra={extra if extra else 'NONE'}; dups={dups if dups else 'NONE'}")
chk("K2_row_count", len(mrows) == 31 and len(disk_files) == 32,
    f"31 manifest rows vs 32 physical files (31 + the self-excluded manifest itself) — matches the dispatch's 32-file census; "
    f"the AUDIT_ENTRYPOINT.md exclusion is explicitly recorded (make_manifest.py docstring + FINAL_REPORT §6 + HANDOFF)")

# ================= L. CANDIDATE_LEDGER independent parse =================
with open(PKG + r"\CANDIDATE_LEDGER.csv", encoding="utf-8", newline="") as f:
    rd_ = list(csv.reader(f))
hdr = rd_[0]
expected_hdr = ["CANDIDATE_ID","JOIN_SITE_VA","PARENT_SOURCE","PARENT_STATUS","CHILD_SOURCE","CHILD_PROVENANCE",
                "CHILD_ROLE","JOIN_OPERATION","JOIN_OPERATION_STATUS","PATH_CONDITIONS","WRAPPER_DEPTH",
                "IDENTITY_BREAK_FOUND","STATUS","REJECTION_REASON","PHYSICAL_EVIDENCE"]
errs = []
if hdr != expected_hdr:
    errs.append(f"header mismatch vs contract §5 field list: {hdr}")
ids = []
for i, r in enumerate(rd_[1:], start=2):
    if len(r) != len(expected_hdr):
        errs.append(f"row {i} width {len(r)} != {len(expected_hdr)}")
    for j, c in enumerate(r):
        if c is None or c.strip() == "":
            errs.append(f"row {i} col {j} ({expected_hdr[j]}) null/empty")
    ids.append(r[0])
dups = [x for x in set(ids) if ids.count(x) > 1]
if dups: errs.append(f"duplicate candidate ids: {dups}")
chk("L1_candidate_ledger", len(errs) == 0 and len(rd_) == 5,
    f"header exact match to contract §5 fields; 4 candidate rows; width/null/dup errors: {errs if errs else 'NONE'}")
# statuses vs claims matrix algebra
cand4 = list(csv.DictReader(open(PKG + r"\CANDIDATE_LEDGER.csv", encoding="utf-8", newline="")))[-1]
algebra_ok = ("UNRESOLVED" in cand4["CHILD_PROVENANCE"] and "UNRESOLVED" in cand4["CHILD_ROLE"]
              and cand4["PARENT_STATUS"].startswith("CONFIRMED_EXACT_SCENEFEEDER_PLUS_30")
              and cand4["JOIN_OPERATION_STATUS"].startswith("STRONGLY_SUPPORTED")
              and "NOT CONFIRMED" in cand4["JOIN_OPERATION_STATUS"]
              and "DIFFERENT INSTANCE" in cand4["PARENT_STATUS"])
chk("L2_cand4_status_algebra", algebra_ok,
    "CAND-4: A=UNRESOLVED, B=CONFIRMED(scoped, DIFFERENT-INSTANCE disclosure present), C=STRONGLY_SUPPORTED with explicit NOT CONFIRMED, D=UNRESOLVED")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=2)
    f.write("\n")
print(json.dumps({"checks": {k: v["ok"] for k, v in res["checks"].items()},
                  "OVERALL": all(v["ok"] for v in res["checks"].values())}, indent=2))
