"""qc_ind_decoder.py — PE-MASTER-AUDITOR independent QC, part 2.

OWN sequential x86-32 decoder (table-driven, written here from scratch — no
capstone, no executor tooling) for the six opened bodies, the §7 join window
and the neighbor spot checks. Purposes:

 1. verify each body's EXTENT claim (terminal RET + CC padding + aligned next
    entry) from raw bytes;
 2. enumerate every CALL instruction inside the six analyzed extents with my
    OWN instruction-boundary walk (mid-instruction E8 impossible) — the
    independent edge-census basis;
 3. verify the §7 join window (0x0050A3B7..0x0050A3F8) is CLEAN of EDI writes
    between mov edi,eax and push edi (own decode);
 4. verify the raw records' disassembly listings at instruction-start level;
 5. spot-verify the NEIGH/GAP-2 window claims (FUN_006C8BB0's callsites, the
    getter neighbor callsite, CTRL_3's foreign accessor 0x006C0EE0).
"""
import struct

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

with open(EXE_PATH, "rb") as f:
    EXE = f.read()

REGS = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REGS8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]

# own VA->offset map (same as part 1, repeated self-contained)
e_lfanew = struct.unpack_from("<I", EXE, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", EXE, coff + 2)[0]
opt = coff + 20
opt_size = struct.unpack_from("<H", EXE, coff + 16)[0]
image_base = struct.unpack_from("<I", EXE, opt + 28)[0]
sectab = opt + opt_size
SECTIONS = []
for i in range(nsec):
    off = sectab + 40 * i
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", EXE, off + 8)
    SECTIONS.append((vaddr, vsize, rawsize, rawptr))


def va_to_off(va):
    rva = va - image_base
    for vaddr, vsize, rawsize, rawptr in SECTIONS:
        if vaddr <= rva < vaddr + max(vsize, rawsize):
            return rawptr + (rva - vaddr)
    raise ValueError(f"unmapped VA {va:#x}")


def rd(va, n):
    off = va_to_off(va)
    return EXE[off:off + n]


class Decoded:
    def __init__(self, va, nbytes, text, writes, reads, is_call, call_target):
        self.va, self.n, self.text = va, nbytes, text
        self.writes, self.reads = writes, reads
        self.is_call, self.call_target = is_call, call_target


def modrm_info(code, i):
    """Decode ModRM at code[i]; returns (mod, reg, rm, size_after_modrm, rm_text,
    mem_rm) — handles the x86 mod00 rm=101 [disp32] special case."""
    m = code[i]
    mod, reg, rm = m >> 6, (m >> 3) & 7, m & 7
    extra = 0
    disp = 0
    if mod == 0 and rm == 5:
        disp = struct.unpack_from("<i", code, i + 1)[0]
        rm_text = f"[0x{disp & 0xFFFFFFFF:08X}]"
        extra = 4
        return mod, reg, rm, extra, rm_text, True, disp
    if mod == 1:
        disp = struct.unpack_from("<b", code, i + 1)[0]
        extra = 1
    elif mod == 2:
        disp = struct.unpack_from("<i", code, i + 1)[0]
        extra = 4
    if mod == 3:
        rm_text = REGS[rm]
        return mod, reg, rm, extra, rm_text, False, 0
    if rm == 4:  # SIB — SIB byte is at i+1 (after ModRM), disp at i+2
        sib = code[i + 1]
        i2 = i + 2
        scale = sib >> 6
        index = (sib >> 3) & 7
        base = sib & 7
        scale_f = {0: 1, 1: 2, 2: 4, 3: 8}[scale]
        idx_txt = REGS[index] if index != 4 else None
        if mod == 0 and base == 5:
            disp = struct.unpack_from("<i", code, i2)[0]
            i2 += 4
            base_txt = None
        else:
            base_txt = REGS[base]
            if mod == 1:
                disp = struct.unpack_from("<b", code, i2)[0]
                i2 += 1
            elif mod == 2:
                disp = struct.unpack_from("<i", code, i2)[0]
                i2 += 4
            else:
                disp = 0
        parts = []
        if base_txt:
            parts.append(base_txt)
        if idx_txt:
            parts.append(f"{idx_txt}*{scale_f}")
        if disp or not parts:
            parts.append(f"{disp:#x}")
        rm_text = "[" + " + ".join(parts) + "]"
        return mod, reg, rm, i2 - i - 1, rm_text, True, disp  # extra = bytes AFTER the ModRM byte (SIB+disp)
    base = REGS[rm]
    if disp:
        rm_text = f"[{base}+{disp:#x}]"
    else:
        rm_text = f"[{base}]"
    return mod, reg, rm, extra, rm_text, True, disp


def decode_one(code, va):
    """Decode ONE instruction at va. Returns Decoded or raises."""
    i = 0
    pfx = None
    if code[i] == 0x64:
        pfx = "fs:"
        i += 1
    op = code[i]
    i += 1
    writes, reads = [], []

    def W(r):
        writes.append(r)

    def R(r):
        reads.append(r)

    if op == 0x0F:
        op2 = code[i]
        i += 1
        if op2 in (0x84, 0x85):  # jcc rel32
            rel = struct.unpack_from("<i", code, i)[0]
            i += 4
            tgt = va + i + rel
            return Decoded(va, i, f"jcc 0x{tgt:08x}", [], [], False, None)
        if op2 == 0x95:  # setne r/m8
            mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
            i += 1 + extra
            if not mem:
                W(rm_text if mod == 3 else "mem")
            return Decoded(va, i, f"setne {rm_text}", writes, reads, False, None)
        raise NotImplementedError(f"0F {op2:02x} not in audited set @0x{va:08x}")
    if op == 0x80:  # group1 r/m8, imm8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        grp = ["add", "or", "adc", "sbb", "and", "sub", "xor", "cmp"][reg]
        imm = code[i]
        i += 1
        if not mem:
            W(rm_text)
        return Decoded(va, i, f"{grp} byte {rm_text}, {imm}", writes, reads, False, None)
    if op in range(0x50, 0x58):  # push r32
        r = REGS[op - 0x50]
        W("ESP")
        R(r)
        return Decoded(va, i, f"push {r}", writes, reads, False, None)
    if op in range(0x58, 0x60):  # pop r32
        r = REGS[op - 0x58]
        W("ESP")
        W(r)
        return Decoded(va, i, f"pop {r}", writes, reads, False, None)
    if op == 0x68:  # push imm32
        imm = struct.unpack_from("<I", code, i)[0]
        i += 4
        W("ESP")
        return Decoded(va, i, f"push 0x{imm:08x}", writes, reads, False, None)
    if op == 0x6A:  # push imm8
        imm = struct.unpack_from("<b", code, i)[0]
        i += 1
        W("ESP")
        return Decoded(va, i, f"push {imm}", writes, reads, False, None)
    if op == 0x83:  # group1 r/m32, imm8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        grp = ["add", "or", "adc", "sbb", "and", "sub", "xor", "cmp"][reg]
        imm = struct.unpack_from("<b", code, i)[0]
        i += 1
        if not mem:
            W(rm_text)
        return Decoded(va, i, f"{grp} {rm_text}, {imm}", writes, reads, False, None)
    if op in (0x84, 0x85, 0x38, 0x39, 0x3B):  # test/cmp — ModRM only, no immediate
        names = {0x84: "test", 0x85: "test", 0x38: "cmp", 0x39: "cmp", 0x3B: "cmp"}
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"{names[op]} {rm_text}, {REGS[reg]}", [], [], False, None)
    if op in (0x01, 0x33, 0x89, 0x88, 0x8A, 0x8B, 0x3B, 0x39):  # covered above partly
        pass
    if op == 0x01:  # add r/m32, r32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        if not mem:
            W(rm_text)
        return Decoded(va, i, f"add {rm_text}, {REGS[reg]}", writes, reads, False, None)
    if op in (0x74, 0x75, 0x76, 0x77, 0x72, 0x73, 0x7C, 0x7D, 0x7E, 0x7F):
        names = {0x74: "je", 0x75: "jne", 0x76: "jbe", 0x77: "ja", 0x72: "jb",
                 0x73: "jae", 0x7C: "jl", 0x7D: "jge", 0x7E: "jle", 0x7F: "jg"}
        rel = struct.unpack_from("<b", code, i)[0]
        i += 1
        tgt = va + i + rel
        return Decoded(va, i, f"{names[op]} 0x{tgt:08x}", [], [], False, None)
    if op == 0xEB:  # jmp rel8
        rel = struct.unpack_from("<b", code, i)[0]
        i += 1
        tgt = va + i + rel
        return Decoded(va, i, f"jmp 0x{tgt:08x}", [], [], False, None)
    if op in (0x88, 0x89, 0x8A, 0x8B):  # mov variants
        names = {0x88: "mov", 0x89: "mov", 0x8A: "mov", 0x8B: "mov"}
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        if op in (0x88, 0x89):  # r/m <- reg
            if not mem:
                W(rm_text)
            else:
                writes.append("mem")
            R(REGS[reg])
            return Decoded(va, i, f"mov {rm_text}, {REGS[reg]}", writes, reads, False, None)
        else:  # reg <- r/m
            W(REGS[reg])
            if mem:
                reads.append("mem")
            else:
                R(rm_text)
            return Decoded(va, i, f"mov {REGS[reg]}, {rm_text}", writes, reads, False, None)
    if op == 0x8D:  # lea
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        W(REGS[reg])
        return Decoded(va, i, f"lea {REGS[reg]}, {rm_text}", writes, reads, False, None)
    if op == 0xA1:  # mov eax, [moffs32] (with optional fs prefix)
        moffs = struct.unpack_from("<I", code, i)[0]
        i += 4
        W("EAX")
        reads.append("mem")
        return Decoded(va, i, f"mov eax, {pfx or ''}[0x{moffs:08x}]", writes, reads, False, None)
    if op == 0xA3:  # mov [moffs32], eax
        moffs = struct.unpack_from("<I", code, i)[0]
        i += 4
        W("mem")
        R("EAX")
        return Decoded(va, i, f"mov {pfx or ''}[0x{moffs:08x}], eax", writes, reads, False, None)
    if 0xB0 <= op <= 0xB7:  # mov r8, imm8
        imm = code[i]
        i += 1
        return Decoded(va, i, f"mov r8, {imm}", [], [], False, None)
    if 0xB8 <= op <= 0xBF:  # mov r32, imm32
        r = REGS[op - 0xB8]
        imm = struct.unpack_from("<I", code, i)[0]
        i += 4
        W(r)
        return Decoded(va, i, f"mov {r}, 0x{imm:08x}", writes, reads, False, None)
    if op == 0xC2:  # ret imm16
        imm = struct.unpack_from("<H", code, i)[0]
        i += 2
        return Decoded(va, i, f"ret {imm:#x}", [], [], False, None)
    if op == 0xC3:
        return Decoded(va, i, "ret", [], [], False, None)
    if op == 0xC6:  # mov r/m8, imm8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        imm = code[i]
        i += 1
        if mem:
            W("mem")
        else:
            W(rm_text)
        return Decoded(va, i, f"mov byte {rm_text}, {imm}", writes, reads, False, None)
    if op == 0xC7:  # mov r/m32, imm32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        imm = struct.unpack_from("<I", code, i)[0]
        i += 4
        if mem:
            W("mem")
        else:
            W(rm_text)
        return Decoded(va, i, f"mov {rm_text}, 0x{imm:08x}", writes, reads, False, None)
    if op == 0xCC:
        return Decoded(va, i, "int3", [], [], False, None)
    if op == 0xE8:  # call rel32
        rel = struct.unpack_from("<i", code, i)[0]
        i += 4
        tgt = va + i + rel
        W("ESP")
        return Decoded(va, i, f"call 0x{tgt:08x}", writes, reads, True, tgt)
    if op == 0x33:  # xor r32, r/m32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        W(REGS[reg])
        return Decoded(va, i, f"xor {REGS[reg]}, {rm_text}", writes, reads, False, None)
    if op == 0xFF:  # group5 — /2 call, /4 jmp, /6 push
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        if reg == 2:
            W("ESP")
            return Decoded(va, i, f"call {rm_text}", writes, reads, True, "INDIRECT")
        if reg == 6:
            W("ESP")
            return Decoded(va, i, f"push {rm_text}", writes, reads, False, None)
        if reg == 4:
            return Decoded(va, i, f"jmp {rm_text}", [], [], False, None)
        raise NotImplementedError(f"FF /{reg} not in audited set @0x{va:08x}")
    if op == 0x85 and False:
        pass
    if op == 0x85:  # test r/m32, r32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"test {rm_text}, {REGS[reg]}", [], [], False, None)
    if op == 0x3B:  # cmp r32, r/m32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"cmp {REGS[reg]}, {rm_text}", [], [], False, None)
    if op == 0x39:  # cmp r/m32, r32
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"cmp {rm_text}, {REGS[reg]}", [], [], False, None)
    if op == 0x38:  # cmp r/m8, r8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"cmp byte {rm_text}, r8", [], [], False, None)
    if op == 0x84:  # test r/m8, r8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"test byte {rm_text}, r8", [], [], False, None)
    if op == 0x8A:  # mov r8, r/m8
        mod, reg, rm, extra, rm_text, mem, _ = modrm_info(code, i)
        i += 1 + extra
        return Decoded(va, i, f"mov r8, {rm_text}", [], [], False, None)
    if op == 0x64 and False:
        pass
    raise NotImplementedError(f"opcode {op:02x} not in audited set @0x{va:08x}")


def walk(va, length, allow_truncated_tail=False, tail_expect=None):
    """Sequential own decode of [va, va+length). Returns (ins_list, tail_bytes).
    If allow_truncated_tail: an undecodable trailing partial instruction is kept
    as raw tail bytes (verified against tail_expect) instead of aborting."""
    code = rd(va, length)
    out = []
    p = 0
    while p < length:
        try:
            d = decode_one(code[p:], va + p)
        except (NotImplementedError, struct.error) as e:
            if allow_truncated_tail and p + 6 >= length:
                tail = code[p:]
                return out, tail
            raise
        out.append(d)
        p += d.n
    return out, b""


def fmt_ins(d):
    return f"0x{d.va:08x}  {d.text}"


# ---------------------------------------------------------------- 1+2+4: six bodies
BODIES = [
    ("FUN_006C66D0", 0x006C66D0, 4, "C3", "0x006C66E0"),
    ("FUN_006C0D50", 0x006C0D50, 0x006C0DAE - 0x006C0D50, "C2", "0x006C0DB0"),
    ("FUN_006C8F80", 0x006C8F80, 0x006C9036 - 0x006C8F80, "C2", "0x006C9040"),
    ("FUN_006C8B20", 0x006C8B20, 0x006C8BAA - 0x006C8B20, "C3", "0x006C8BB0"),
    ("FUN_006C6F60", 0x006C6F60, 0x006C7072 - 0x006C6F60, "C3", "0x006C7080"),
    ("FUN_006C6780", 0x006C6780, 0x006C6848 - 0x006C6780, None, None),  # PARTIAL window
]

results = []
total_calls = 0
call_list = []
for name, va, ln, ret_kind, nxt in BODIES:
    partial = name == "FUN_006C6780"
    if partial:
        ins, tail = walk(va, ln, allow_truncated_tail=True)
        results.append((f"{name}-window-tail", tail == bytes([0x0F, 0x84, 0xBE, 0x00]),
                        f"truncated tail bytes 0x{va+ln-len(tail):08X}..0x{va+ln-1:08X} = {tail.hex(' ').upper()} "
                        f"(expect 0F 84 BE 00 — leading bytes of a jcc rel32; window ends mid-instruction, extent UNRESOLVED — matches the record's honest PARTIAL claim)"))
    else:
        ins, tail = walk(va, ln)
    texts = [fmt_ins(d) for d in ins]
    calls = [d for d in ins if d.is_call]
    total_calls += len(calls)
    for c in calls:
        call_list.append((name, c))
    last = ins[-1]
    if ret_kind:
        # terminal RET + CC padding + aligned next entry
        pad_start = va + ln
        pad = rd(pad_start, 16)
        n_cc = 0
        while pad[n_cc] == 0xCC:
            n_cc += 1
        nxt_bytes = rd(pad_start + n_cc, 4)
        ext_ok = last.text.startswith("ret") and n_cc >= 1 and (pad_start + n_cc) == int(nxt, 16)
        results.append((f"{name}-extent", ext_ok,
                        f"terminal '{last.text}' @0x{last.va:08x}; CC pad {n_cc}B 0x{pad_start:08X}..0x{pad_start+n_cc-1:08X}; "
                        f"next entry 0x{pad_start+n_cc:08X} (expect {nxt}) first bytes {nxt_bytes.hex(' ').upper()}"))
    results.append((f"{name}-own-decode", True,
                    f"{len(ins)} instructions decoded; {len(calls)} CALLs: " +
                    "; ".join(f"0x{c.va:08X}->{c.call_target}" if c.call_target != 'INDIRECT' else f"0x{c.va:08X}->indirect" for c in calls)))

print("=== BODIES (own sequential decode) ===")
for cid, ok, d in results:
    print(("PASS " if ok else "FAIL ") + cid + ": " + d)
print(f"TOTAL CALL instructions in the 6 analyzed extents (own walk): {total_calls}")
print()

# ---------------------------------------------------------------- 3: join window EDI-clean
WIN_VA, WIN_LEN = 0x0050A3B7, 0x42
win, _ = walk(WIN_VA, WIN_LEN)
edi_writes = [d for d in win if "EDI" in d.writes]
head = win[0]
pushes = [d for d in win if d.text.upper() == "PUSH EDI"]
calls_in_win = [d for d in win if d.is_call]
print("=== JOIN WINDOW 0x0050A3B7..0x0050A3F8 (own decode) ===")
for d in win:
    print("  " + fmt_ins(d) + ("   <EDI WRITE>" if "EDI" in d.writes else ""))
head_ok = head.text == "mov EDI, EAX"
push_at_f6 = any(d.va == 0x0050A3F6 for d in pushes)
push_at_d7 = any(d.va == 0x0050A3D7 for d in pushes)
clean_ok = head_ok and not edi_writes[1:] and push_at_f6
print(("PASS " if head_ok else "FAIL ") + f"QC-E1-join-head: first instruction = '{head.text}'")
print(("PASS " if not edi_writes[1:] else "FAIL ") +
      f"QC-E2-join-edi-clean: EDI-writing instructions in window = {[f'0x{d.va:08x} {d.text}' for d in edi_writes]} (expect ONLY the head)")
print(("PASS " if push_at_f6 and push_at_d7 else "FAIL ") +
      f"QC-E3-join-push-edi: push EDI @0x0050A3D7 (arg of FUN_0050A1E0) and @0x0050A3F6 (THE join child argument) both present")
print(f"    intervening CALLs in window: {[f'0x{c.va:08X}' for c in calls_in_win]}")
print()

# ---------------------------------------------------------------- 5: neighbor spot checks
print("=== NEIGHBOR / GAP-2 / CTRL_3 spot checks (own decode) ===")
# FUN_006C8BB0 window continuation claims (GAP-2): 0x006C8C0F -> 0x004066D0; 0x006C8C52 -> 0x0072FCE0
b0f = rd(0x006C8C0F, 5)
b52 = rd(0x006C8C52, 5)
t0f = 0x006C8C0F + 5 + struct.unpack("<i", b0f[1:5])[0]
t52 = 0x006C8C52 + 5 + struct.unpack("<i", b52[1:5])[0]
print(("PASS " if b0f[0] == 0xE8 and t0f == 0x004066D0 else "FAIL ") +
      f"QC-G1-NEIGH-22: E8 @0x006C8C0F -> 0x{t0f:08X} (expect 0x004066D0)")
print(("PASS " if b52[0] == 0xE8 and t52 == 0x0072FCE0 else "FAIL ") +
      f"QC-G2-NEIGH-24: E8 @0x006C8C52 -> 0x{t52:08X} (expect 0x0072FCE0)")
# NEIGH-21: indirect vtable dispatch @0x006C8C02
b02 = rd(0x006C8C02, 2)
print(("PASS " if b02[0] == 0xFF and (b02[1] & 0x38) == 0x10 else "FAIL ") +
      f"QC-G3-NEIGH-21: FF /2 @0x006C8C02 = {b02.hex(' ').upper()} (indirect call)")
# NEIGH-23: indirect call eax @0x006C8C34
b34 = rd(0x006C8C34, 2)
print(("PASS " if b34[0] == 0xFF and b34[1] == 0xD0 else "FAIL ") +
      f"QC-G4-NEIGH-23: FF D0 @0x006C8C34 = {b34.hex(' ').upper()} (call eax)")
# NEIGH-01: getter-neighbor body 0x006C66E0's callsite 0x006C66F4 -> 0x006E9A70
bf4 = rd(0x006C66F4, 5)
tf4 = 0x006C66F4 + 5 + struct.unpack("<i", bf4[1:5])[0]
print(("PASS " if bf4[0] == 0xE8 and tf4 == 0x006E9A70 else "FAIL ") +
      f"QC-G5-NEIGH-01: E8 @0x006C66F4 -> 0x{tf4:08X} (expect 0x006E9A70)")
# NEIGH-09: getter callsite in unopened body 0x006C0EF0 @0x006C0F49
b49 = rd(0x006C0F49, 5)
t49 = 0x006C0F49 + 5 + struct.unpack("<i", b49[1:5])[0]
print(("PASS " if b49[0] == 0xE8 and t49 == 0x006C66D0 else "FAIL ") +
      f"QC-G6-NEIGH-09: E8 @0x006C0F49 -> 0x{t49:08X} (expect 0x006C66D0 — a getter callsite in a NEVER-opened body)")
# CTRL_3 foreign accessor: 0x006C0EE0 must be mov eax,[ecx+0x120] (mod=10, disp32)
be0 = rd(0x006C0EE0, 6)
m = be0[1]
print(("PASS " if be0[0] == 0x8B and (m >> 6) == 2 and REGS[(m >> 3) & 7] == "EAX" and REGS[m & 7] == "ECX"
       and struct.unpack_from('<I', be0, 2)[0] == 0x120 else "FAIL ") +
      f"QC-G7-CTRL3-foreign-accessor: @0x006C0EE0 = {be0.hex(' ').upper()} = mov eax,[ecx+0x120] (foreign field, NOT +0x68)")
# NEIGH-06: neighbor 0x006C0E70 setter +0x118 with slot-0 release dispatch @0x006C0E83
b70 = rd(0x006C0E70, 0x18)
slot0_ok = (list(b70[:0x11]) == [0x56, 0x8B, 0xF1, 0x8B, 0x8E, 0x18, 0x01, 0x00, 0x00, 0x85, 0xC9, 0x74, 0x16,
                                 0x8B, 0x01, 0x8B, 0x10] and list(b70[0x13:0x15]) == [0xFF, 0xD2])
print(("PASS " if slot0_ok else "FAIL ") +
      f"QC-G8-NEIGH-06: @0x006C0E70 = {b70.hex(' ').upper()} — reads [esi+0x118], non-NULL -> vtable SLOT 0 (8B 10) release dispatch call edx @0x006C0E83 (raw-visible note verified; no analysis claimed by the run)")
# NEIGH-11: 0x006C0FD0 (vtable slot 2 target) raw window: new(0x68) @0x006C0FF8 -> 0x0095D3C4
bf8 = rd(0x006C0FF8, 5)
tf8 = 0x006C0FF8 + 5 + struct.unpack("<i", bf8[1:5])[0]
print(("PASS " if bf8[0] == 0xE8 and tf8 == 0x0095D3C4 else "FAIL ") +
      f"QC-G9-NEIGH-11: E8 @0x006C0FF8 -> 0x{tf8:08X} (expect 0x0095D3C4 — unopened neighbor body)")

# RV-01 callsite 0x006C8B82 -> 0x006C7B40
b82 = rd(0x006C8B82, 5)
t82 = 0x006C8B82 + 5 + struct.unpack("<i", b82[1:5])[0]
print(("PASS " if b82[0] == 0xE8 and t82 == 0x006C7B40 else "FAIL ") +
      f"QC-G10-RV-01: E8 @0x006C8B82 -> 0x{t82:08X} (expect 0x006C7B40)")

# FUN_006C8BB0 second-caller check (NEIGH-15/16: body 0x006C9040 calls 8B20/8BB0)
bb4 = rd(0x006C90B4, 5)
bbd = rd(0x006C90BD, 5)
tb4 = 0x006C90B4 + 5 + struct.unpack("<i", bb4[1:5])[0]
tbd = 0x006C90BD + 5 + struct.unpack("<i", bbd[1:5])[0]
print(("PASS " if bb4[0] == 0xE8 and tb4 == 0x006C8B20 else "FAIL ") +
      f"QC-G11-NEIGH-15: E8 @0x006C90B4 -> 0x{tb4:08X} (expect 0x006C8B20)")
print(("PASS " if bbd[0] == 0xE8 and tbd == 0x006C8BB0 else "FAIL ") +
      f"QC-G12-NEIGH-16: E8 @0x006C90BD -> 0x{tbd:08X} (expect 0x006C8BB0)")

# NEIGH-25..27: producer neighbor body 0x006C7080: 0x006C70CE indirect, 0x006C70DE -> 0x006C69A0, 0x006C70EA -> 0x006C69A0
bce = rd(0x006C70CE, 2)
bde = rd(0x006C70DE, 5)
tde = 0x006C70DE + 5 + struct.unpack("<i", bde[1:5])[0]
bea = rd(0x006C70EA, 5)
tea = 0x006C70EA + 5 + struct.unpack("<i", bea[1:5])[0]
print(("PASS " if bce[0] == 0xFF else "FAIL ") + f"QC-G13-NEIGH-25: FF dispatch @0x006C70CE = {bce.hex(' ').upper()}")
print(("PASS " if bde[0] == 0xE8 and tde == 0x006C69A0 else "FAIL ") + f"QC-G14-NEIGH-26: E8 @0x006C70DE -> 0x{tde:08X}")
print(("PASS " if bea[0] == 0xE8 and tea == 0x006C69A0 else "FAIL ") + f"QC-G15-NEIGH-27: E8 @0x006C70EA -> 0x{tea:08X}")

print()
print("PART2 DONE")

# ---------------------------------------------------------------- 6: raw-record listing addresses vs own walk
import re
import json
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007"
RAWS = {
    "FUN_006C66D0": ("01_RAW\\FUN_006C66D0_GETTER_FULL.txt", 0x006C66D0, 4),
    "FUN_006C0D50": ("01_RAW\\FUN_006C0D50_CTOR_DECODE.txt", 0x006C0D50, 0x006C0DAE - 0x006C0D50),
    "FUN_006C8F80": ("01_RAW\\FUN_006C8F80_BASECTOR_DECODE.txt", 0x006C8F80, 0x006C9036 - 0x006C8F80),
    "FUN_006C8B20": ("01_RAW\\FUN_006C8B20_LAZYINIT_DECODE.txt", 0x006C8B20, 0x006C8BAA - 0x006C8B20),
    "FUN_006C6F60": ("01_RAW\\FUN_006C6F60_PRODUCER_DECODE.txt", 0x006C6F60, 0x006C7072 - 0x006C6F60),
    "FUN_006C6780": ("01_RAW\\FUN_006C6780_INSTALLER_PARTIAL.txt", 0x006C6780, 0x006C6848 - 0x006C6780),
}
print()
print("=== RAW-RECORD LISTING ADDRESSES vs OWN WALK (subset verification) ===")
all_ok = True
for name, (rel, va, ln) in RAWS.items():
    txt = open(PKG + "\\" + rel, encoding="utf-8").read()
    addrs = set(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{8})\s+[0-9A-F]{2}", txt))
    if name == "FUN_006C6780":
        ins, tail = walk(va, ln, allow_truncated_tail=True)
    else:
        ins, _ = walk(va, ln)
        tail = b""
    my_starts = set(d.va for d in ins)
    if tail:
        my_starts.add(va + ln - len(tail))  # the truncated tail start (listed by the record as mid-instruction)
    bad = sorted(a for a in addrs if va <= a < va + ln and a not in my_starts)
    ok = not bad
    all_ok = all_ok and ok
    print(("PASS " if ok else "FAIL ") + f"QC-H-{name}: {len(addrs)} listing addresses in file; "
          f"{'all within-extent ones are instruction starts in MY OWN walk' if ok else 'MISALIGNED: ' + str([hex(b) for b in bad])}")

# join window listing vs walk
txt = open(PKG + r"\01_RAW\JOIN_WINDOW_50A3B7_REPIN.txt", encoding="utf-8").read()
addrs = set(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{8})\s+[0-9A-F]{2}", txt))
my_starts = set(d.va for d in win)
bad = sorted(a for a in addrs if a not in my_starts)
print(("PASS " if not bad else "FAIL ") +
      f"QC-H-join-window: {len(addrs)} listing addresses; misaligned: {[hex(b) for b in bad] if bad else 'NONE'}")

out = {"bodies_total_calls_own_walk": total_calls, "listing_subset_ok": all_ok and not bad,
       "walk_call_vas": {name: [c.va for c in call_list if False] for name in []}}
# save the per-body call VA sets (the authoritative own-walk census)
per_body = {}
for name, va, ln, ret_kind, nxt in BODIES:
    if name == "FUN_006C6780":
        ins, _ = walk(va, ln, allow_truncated_tail=True)
    else:
        ins, _ = walk(va, ln)
    per_body[name] = sorted(d.va for d in ins if d.is_call)
out["walk_call_vas"] = per_body
with open(PKG + r"\00_CONTROL_INTERNAL_QC\qc_ind_decoder_results.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
