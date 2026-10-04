# s2_write_census.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
# Purpose (PHASE A): bounded static census of every .text instruction form capable of
# writing factory+0x84 (dword write forms MOV [reg+0x84],reg / MOV [reg+0x84],imm32,
# including SIB and disp32 encodings), plus the read/CMP forms and LEA-wrapper stores
# as natural negative controls. For every hit: instruction-boundary verification
# (anchor-decode from a padding-delimited function start + multi-start greedy decode),
# base-register extraction, containing-function attribution, and a mechanical
# classification pass. READ-ONLY vs the pinned EXE. Own PE mapper + own mini
# x86 length decoder (fail-closed on unknown opcodes).
# Output: 01_RAW/S2_CENSUS.json + FACTORY_PLUS_84_WRITE_CENSUS.csv (real csv module)
import sys, os, json, struct, csv, hashlib

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

REGS = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REGS8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]

# known functions (entry -> label) used for containment attribution
KNOWN = {
    0x0070DCF0: "FUN_0070DCF0_consumer_record_reader",
    0x0070CF80: "FUN_0070CF80_factory_base_ctor",
    0x0070C680: "FUN_0070C680_stream_attach_setter",
    0x00703E80: "FUN_00703E80_bulk_attach_loop",
    0x004B0980: "FUN_004B0980_attach_driver",
    0x00707FB0: "FUN_00707FB0_register_factory",
    0x007080C0: "FUN_007080C0_manager_mode_and_class_enum",
    0x00972380: "FUN_00972380_stream_ctor",
    0x00703CD0: "FUN_00703CD0_manager_mode_cond",
    0x0070CC80: "FUN_0070CC80_slot_predicate_scan",
    0x00707E50: "FUN_00707E50_manager_ctor",
    0x00415470: "FUN_00415470_manager_getter",
    0x0073C870: "FUN_0073C870_class_dispatcher",
    0x0073C8D8: "FUN_0073C8D8_factory20006_getter",
    0x0073B820: "FUN_0073B820_factory20006_ctor",
    0x0073B8C0: "FUN_0073B8C0_factory20006_create_component",
    0x0073C6C0: "FUN_0073C6C0_factory20006_dtor",
    0x0070D990: "FUN_0070D990_component_creator",
    0x0070DC20: "FUN_0070DC20_record_apply",
    0x0070DE10: "FUN_0070DE10_cache_miss_creator",
    0x0070E100: "FUN_0070E100_component_get_or_create",
    0x0070C150: "FUN_0070C150_factory_finalize",
    0x0070BF10: "FUN_0070BF10_ready_flag_reader",
    0x0070BF20: "FUN_0070BF20_flag_or_setter",
    0x0070BF40: "FUN_0070BF40_flag_bit_test",
    0x0070C180: "FUN_0070C180_slot_addr_getter",
    0x007374F0: "FUN_007374F0_schema_init",
    0x0070CBC0: "FUN_0070CBC0_slot_add",
    0x0070E2F0: "FUN_0070E2F0_factory_vec_init",
    0x0071B820: "FUN_0071B820_UNKNOWN",
    0x00971AD0: "FUN_00971AD0_record_reader",
    0x00971650: "FUN_00971650_stream_advance",
    0x0070BFD0: "FUN_0070BFD0_stream_bridge_method",
}

def load_text(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    IB = struct.unpack_from("<I", d, opt + 28)[0]
    sec0 = opt + opt_size
    for i in range(nsec):
        s = sec0 + 40 * i
        name = d[s:s+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        if name == ".text":
            return d, IB, IB + vaddr, d[rawptr:rawptr+rawsize]
    raise SystemExit

# ---------------- mini x86 length decoder (bounded, fail-closed) ----------------
def insn_len(blob, i):
    """Return the instruction length at blob[i] or None if unknown.
    Covers the common 32-bit subset; fail-closed otherwise."""
    n = len(blob)
    if i >= n:
        return None
    b0 = blob[i]
    # prefixes
    pfx = 0
    while b0 in (0x66, 0x67, 0xF2, 0xF3, 0x64, 0x65, 0x36, 0x2E, 0x3E, 0x26):
        pfx += 1
        i += 1
        if i >= n:
            return None
        b0 = blob[i]
    def modrm_len(j):
        if j >= n:
            return None
        m = blob[j]
        mod = m >> 6
        rm = m & 7
        L = 1
        if mod == 0 and rm == 5:
            L += 4
        elif mod == 1:
            L += 1
            if rm == 4:
                L += 1
        elif mod == 2:
            L += 4
            if rm == 4:
                L += 1
        elif mod == 3:
            pass
        return L
    L = None
    if b0 in (0x00, 0x01, 0x02, 0x03, 0x08, 0x09, 0x0A, 0x0B,
              0x10, 0x11, 0x12, 0x13, 0x18, 0x19, 0x1A, 0x1B,
              0x20, 0x21, 0x22, 0x23, 0x28, 0x29, 0x2A, 0x2B,
              0x30, 0x31, 0x32, 0x33, 0x38, 0x39, 0x3A, 0x3B,
              0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B,
              0x8D, 0x8F, 0x62, 0x63):
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        if b0 in (0x80, 0x81, 0x83, 0x69, 0x6B, 0xC0, 0xC1):
            il = 1 if b0 in (0x80, 0x83, 0x6B, 0xC0, 0xC1) else 4
            L = 1 + ml + il
        else:
            L = 1 + ml
    elif 0x40 <= b0 <= 0x4F or 0x50 <= b0 <= 0x5F or b0 in (0x90, 0x98, 0x99, 0x9B,
          0xC2, 0xC3, 0xCC, 0xCE, 0xCF, 0xF4, 0xF5, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD):
        L = 1
        if b0 in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
                  0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F):
            L = 1
        if b0 in (0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
                  0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F):
            L = 1
        if b0 in (0xC2,):
            L = 3
        if b0 in (0x90, 0x98, 0x99, 0x9B, 0xC3, 0xCC, 0xCE, 0xCF, 0xF4, 0xF5,
                  0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD):
            L = 1
    elif b0 == 0x68:
        L = 5
    elif b0 == 0x6A:
        L = 2
    elif 0x70 <= b0 <= 0x7F:
        L = 2
    elif b0 == 0xEB:
        L = 2
    elif b0 in (0xE8, 0xE9):
        L = 5
    elif b0 in (0xE0, 0xE1, 0xE2, 0xE3):
        L = 2
    elif b0 == 0xC6:
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        L = 1 + ml + 1
    elif b0 == 0xC7:
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        L = 1 + ml + 4
    elif b0 in (0xA0, 0xA1, 0xA2, 0xA3):
        L = 5
    elif 0xA4 <= b0 <= 0xA7 or 0xAA <= b0 <= 0xAF:
        L = 1
    elif 0xB0 <= b0 <= 0xB7:
        L = 2
    elif 0xB8 <= b0 <= 0xBF:
        L = 5
    elif b0 == 0xC9:
        L = 1
    elif b0 == 0xCD:
        L = 2
    elif b0 in (0xD0, 0xD1, 0xD2, 0xD3):
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        L = 1 + ml
    elif 0xD8 <= b0 <= 0xDF:
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        L = 1 + ml
        # FPU with disp only - modrm covers
    elif b0 in (0xF6, 0xF7):
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        sub = (blob[i+1] >> 3) & 7
        il = 0
        if b0 == 0xF6 and sub in (0, 1):
            il = 1
        if b0 == 0xF7 and sub in (0, 1):
            il = 4
        L = 1 + ml + il
    elif b0 in (0xFE, 0xFF):
        ml = modrm_len(i + 1)
        if ml is None:
            return None
        L = 1 + ml
    elif b0 == 0x0F:
        if i + 1 >= n:
            return None
        b1 = blob[i+1]
        if 0x80 <= b1 <= 0x8F:
            L = 6
        elif 0x90 <= b1 <= 0x9F:
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 2 + ml
        elif b1 in (0xA4, 0xAC):  # shld/shrd imm8
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 3 + ml
        elif b1 in (0xA5, 0xAD):
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 2 + ml
        elif b1 in (0xAF, 0xB6, 0xB7, 0xBE, 0xBF, 0xB0, 0xB1, 0xB2, 0xB3,
                    0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
                    0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F,
                    0xB2, 0xB3, 0xBC, 0xBD):
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 2 + ml
        elif b1 in (0x1E, 0x1F, 0x0D, 0x18, 0x19, 0x1A, 0x1B):
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 2 + ml
        elif b1 == 0x05:
            L = 8
        elif b1 == 0x0B:
            L = 3
        elif b1 == 0x00:
            ml = modrm_len(i + 2)
            if ml is None:
                return None
            L = 2 + ml
        else:
            return None
    elif b0 in (0xF1,):
        L = 1
    else:
        return None
    if L is None:
        return None
    return pfx + L

# ---------------- boundary verification ----------------
def find_function_start(TEXT, TVA, va, max_back=0x600):
    """Nearest preceding CC-padding-delimited code start (>=2 CC bytes) plus known anchors."""
    lo = max(0, va - TVA - max_back)
    hi = va - TVA
    best = None
    i = hi - 2
    # scan backward for the last CC-run end before va
    j = hi - 1
    while j >= lo:
        if TEXT[j] == 0xCC and TEXT[j-1] == 0xCC:
            k = j + 1
            best = TVA + k
            break
        j -= 1
    known_best = None
    for entry in KNOWN:
        if entry <= va and (known_best is None or entry > known_best):
            known_best = entry
    return best, known_best

def anchor_decode(TEXT, TVA, start, target):
    """Linear greedy decode from start; return True if it lands exactly on target."""
    i = start - TVA
    t = target - TVA
    steps = 0
    while i < t and steps < 4096:
        L = insn_len(TEXT, i)
        if L is None or L <= 0:
            return False
        if TEXT[i] in (0xC3, 0xC2) and i + L <= t:
            return False  # a RET before the target - no fall-through
        if TEXT[i] == 0xCC:
            return False
        i += L
        steps += 1
    return i == t

def multi_start(TEXT, TVA, target, lookback=32):
    """Try decode paths from every start in [target-lookback, target-1].
    Return (ok, start_used) - a valid path must land exactly on target,
    contain >= 2 instructions before it, and contain no RET/CC before it."""
    t = target - TVA
    best_start = None
    for s in range(max(0, t - lookback), t):
        i = s
        ok = True
        cnt = 0
        while i < t:
            L = insn_len(TEXT, i)
            if L is None or L <= 0:
                ok = False
                break
            if TEXT[i] in (0xC3, 0xC2, 0xCC):
                ok = False
                break
            i += L
            cnt += 1
            if cnt > 40:
                ok = False
                break
        if ok and i == t and cnt >= 1:
            best_start = TVA + s
            # prefer the earliest plausible start that yields >=2 instructions
            if cnt >= 2:
                return True, TVA + s
    return (best_start is not None), best_start

# ---------------- provenance tags ----------------
def provenance_tags(TEXT, TVA, func_start, hit_va, base_reg):
    """Window-level backward tags for the base register of the hit."""
    tags = []
    lo = func_start - TVA if func_start else max(0, hit_va - TVA - 0x80)
    hi = hit_va - TVA
    win = TEXT[lo:hi]
    # singleton loads
    for gva, label in ((0x00BA590C, "LOAD_FACTORY_SINGLETON_00BA590C"),
                       (0x00BA12E4, "LOAD_MANAGER_SINGLETON_00BA12E4")):
        pat = struct.pack("<I", gva)
        k = 0
        while True:
            idx = win.find(pat, k)
            if idx == -1:
                break
            tags.append({"tag": label, "at": "0x%08X" % (TVA + lo + idx - 1)})
            k = idx + 1
    # this-call pattern near the function start: 8B F1 / 8B F9 / 8B FE / 8B FD (MOV r32,ECX)
    if func_start is not None:
        head = TEXT[func_start - TVA: func_start - TVA + 0x20]
        for off in range(0, len(head) - 1):
            if head[off] == 0x8B and head[off+1] in (0xF1, 0xF9, 0xFE, 0xFD, 0xF8, 0xFA, 0xFB, 0xFC, 0xF0, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7):
                dst = (head[off+1] >> 3) & 7
                tags.append({"tag": "THISCALL_MOV_r32_ECX_at_entry+%d dst=%s" % (off, REGS[dst]),
                             "at": "0x%08X" % (func_start + off)})
                break
        # stack frame check: 55 8B EC = EBP frame
        if head[:3] == b"\x55\x8B\xEC":
            tags.append({"tag": "EBP_FRAME_PROLOGUE", "at": "0x%08X" % func_start})
    return tags

def main():
    d, IB, TVA, TEXT = load_text(EXE)
    N = len(TEXT)
    out = {"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004", "stage": "S2",
           "exe_sha256": hashlib.sha256(open(EXE, "rb").read()).hexdigest(),
           "text_size": N, "text_va": "0x%08X" % TVA}

    hits = []

    def emit(form, va, desc, base, src, extra=None):
        row = {"form": form, "va": va, "desc": desc, "base": base, "src": src}
        if extra:
            row.update(extra)
        hits.append(row)

    # ---------- T1: raw pattern scan ----------
    i = 0
    while i < N:
        b0 = TEXT[i]
        if b0 == 0x89 or b0 == 0x8B or b0 == 0x39 or b0 == 0x8D:
            modrm = TEXT[i+1]
            mod = modrm >> 6
            rm = modrm & 7
            regf = REGS[(modrm >> 3) & 7]
            isS = (rm == 4)
            for (m_exp, dispbytes, dlen, formname) in (
                (1, b"\x84", 1, "MOD01_disp8"), (2, b"\x84\x00\x00\x00", 4, "MOD10_disp32")):
                if mod != m_exp:
                    continue
                if isS:
                    ok = (TEXT[i+3:i+3+dlen] == dispbytes[:dlen])
                    if ok:
                        sib = TEXT[i+2]
                        breg = REGS[sib & 7]
                        ireg = REGS[(sib >> 3) & 7]
                        va = TVA + i
                        mn = {0x89: "MOV", 0x8B: "MOV", 0x39: "CMP", 0x8D: "LEA"}[b0]
                        if b0 in (0x89, 0x39):
                            desc = "%s [%s+%s*%d+0x84],%s" % (mn, breg, ireg, 1 << (sib >> 6), regf)
                        else:
                            desc = "%s %s,[%s+%s*%d+0x84]" % (mn, regf, breg, ireg, 1 << (sib >> 6))
                        emit("%02X_%s_SIB" % (b0, formname), va, desc, breg,
                             regf if b0 == 0x89 else "read")
                        i += 3 + dlen
                        break
                else:
                    ok = (TEXT[i+2:i+2+dlen] == dispbytes[:dlen])
                    if ok:
                        va = TVA + i
                        mn = {0x89: "MOV", 0x8B: "MOV", 0x39: "CMP", 0x8D: "LEA"}[b0]
                        if b0 == 0x89:
                            desc = "MOV [%s+0x84],%s" % (REGS[rm], regf)
                        elif b0 == 0x39:
                            desc = "CMP [%s+0x84],%s" % (REGS[rm], regf)
                        elif b0 == 0x8B:
                            desc = "MOV %s,[%s+0x84]" % (regf, REGS[rm])
                        else:
                            desc = "LEA %s,[%s+0x84]" % (regf, REGS[rm])
                        emit("%02X_%s" % (b0, formname), va, desc, REGS[rm],
                             regf if b0 == 0x89 else "read")
                        i += 2 + dlen
                        break
        elif b0 == 0xC7:
            modrm = TEXT[i+1]
            mod = modrm >> 6
            rm = modrm & 7
            if ((modrm >> 3) & 7) == 0:
                if mod == 1:
                    if rm == 4:
                        if i + 3 < N and TEXT[i+3] == 0x84:
                            imm = struct.unpack_from("<I", TEXT, i+4)[0]
                            sib = TEXT[i+2]
                            emit("C7_MOD01_SIB", TVA + i,
                                 "MOV [%s+%s*%d+0x84],0x%X" % (REGS[sib & 7], REGS[(sib>>3)&7], 1 << (sib>>6), imm),
                                 REGS[sib & 7], "imm32=0x%X" % imm)
                            i += 8
                            continue
                    elif TEXT[i+2] == 0x84:
                        imm = struct.unpack_from("<I", TEXT, i+3)[0]
                        emit("C7_MOD01", TVA + i, "MOV [%s+0x84],0x%X" % (REGS[rm], imm),
                             REGS[rm], "imm32=0x%X" % imm)
                        i += 7
                        continue
                elif mod == 2:
                    if rm == 4:
                        if TEXT[i+3:i+7] == b"\x84\x00\x00\x00":
                            imm = struct.unpack_from("<I", TEXT, i+7)[0]
                            sib = TEXT[i+2]
                            emit("C7_MOD10_SIB", TVA + i,
                                 "MOV [%s+%s*%d+0x84],0x%X" % (REGS[sib & 7], REGS[(sib>>3)&7], 1 << (sib>>6), imm),
                                 REGS[sib & 7], "imm32=0x%X" % imm)
                            i += 11
                            continue
                    elif TEXT[i+2:i+6] == b"\x84\x00\x00\x00":
                        imm = struct.unpack_from("<I", TEXT, i+6)[0]
                        emit("C7_MOD10", TVA + i, "MOV [%s+0x84],0x%X" % (REGS[rm], imm),
                             REGS[rm], "imm32=0x%X" % imm)
                        i += 10
                        continue
        # partial-width write forms: 88 /r (MOV r/m8,r8), C6 /0 imm8, 66-prefixed word forms
        elif b0 == 0x88:
            modrm = TEXT[i+1]
            mod = modrm >> 6
            rm = modrm & 7
            if mod == 1:
                if rm == 4 and i + 3 < N and TEXT[i+3] == 0x84:
                    emit("88_MOD01_SIB_BYTE", TVA + i,
                         "MOV BYTE [%s*+0x84],%s" % (REGS[TEXT[i+2] & 7], REGS8[(modrm >> 3) & 7]),
                         REGS[TEXT[i+2] & 7], "byte")
                    i += 4
                    continue
                elif rm != 4 and TEXT[i+2] == 0x84:
                    emit("88_MOD01_BYTE", TVA + i, "MOV BYTE [%s+0x84],%s" % (REGS[rm], REGS8[(modrm >> 3) & 7]),
                         REGS[rm], "byte")
                    i += 3
                    continue
            elif mod == 2:
                if rm == 4 and TEXT[i+3:i+7] == b"\x84\x00\x00\x00":
                    emit("88_MOD10_SIB_BYTE", TVA + i, "MOV BYTE [...+0x84],r8",
                         REGS[TEXT[i+2] & 7], "byte")
                    i += 7
                    continue
                elif rm != 4 and TEXT[i+2:i+6] == b"\x84\x00\x00\x00":
                    emit("88_MOD10_BYTE", TVA + i, "MOV BYTE [%s+0x84],%s" % (REGS[rm], REGS8[(modrm >> 3) & 7]),
                         REGS[rm], "byte")
                    i += 6
                    continue
        elif b0 == 0xC6:
            modrm = TEXT[i+1]
            mod = modrm >> 6
            rm = modrm & 7
            if ((modrm >> 3) & 7) == 0:
                if mod == 1:
                    if rm == 4 and i + 3 < N and TEXT[i+3] == 0x84:
                        emit("C6_MOD01_SIB_BYTE", TVA + i, "MOV BYTE [...+0x84],imm8",
                             REGS[TEXT[i+2] & 7], "imm8=0x%02X" % TEXT[i+4])
                        i += 5
                        continue
                    elif rm != 4 and TEXT[i+2] == 0x84:
                        emit("C6_MOD01_BYTE", TVA + i, "MOV BYTE [%s+0x84],imm8" % REGS[rm],
                             REGS[rm], "imm8=0x%02X" % TEXT[i+3])
                        i += 4
                        continue
                elif mod == 2:
                    if rm == 4 and TEXT[i+3:i+7] == b"\x84\x00\x00\x00":
                        emit("C6_MOD10_SIB_BYTE", TVA + i, "MOV BYTE [...+0x84],imm8",
                             REGS[TEXT[i+2] & 7], "imm8=0x%02X" % TEXT[i+7])
                        i += 8
                        continue
                    elif rm != 4 and TEXT[i+2:i+6] == b"\x84\x00\x00\x00":
                        emit("C6_MOD10_BYTE", TVA + i, "MOV BYTE [%s+0x84],imm8" % REGS[rm],
                             REGS[rm], "imm8=0x%02X" % TEXT[i+6])
                        i += 7
                        continue
        # 66-prefixed word forms: 66 89 / 66 C7 with disp 0x84
        elif b0 == 0x66 and i + 1 < N and TEXT[i+1] in (0x89, 0xC7):
            op2 = TEXT[i+1]
            modrm = TEXT[i+2] if i + 2 < N else 0
            mod = modrm >> 6
            rm = modrm & 7
            if op2 == 0x89 and mod == 1 and rm != 4 and TEXT[i+3] == 0x84:
                emit("6689_MOD01_WORD", TVA + i, "MOV WORD [%s+0x84],%s" % (REGS[rm], REGS[(modrm >> 3) & 7]),
                     REGS[rm], "word")
                i += 4
                continue
            if op2 == 0x89 and mod == 2 and rm != 4 and TEXT[i+3:i+7] == b"\x84\x00\x00\x00":
                emit("6689_MOD10_WORD", TVA + i, "MOV WORD [%s+0x84],%s" % (REGS[rm], REGS[(modrm >> 3) & 7]),
                     REGS[rm], "word")
                i += 7
                continue
            if op2 == 0xC7 and mod == 1 and rm != 4 and ((modrm >> 3) & 7) == 0 and TEXT[i+3] == 0x84:
                emit("66C7_MOD01_WORD", TVA + i, "MOV WORD [%s+0x84],imm16" % REGS[rm], REGS[rm], "imm16")
                i += 8
                continue
            if op2 == 0xC7 and mod == 2 and rm != 4 and ((modrm >> 3) & 7) == 0 and TEXT[i+3:i+7] == b"\x84\x00\x00\x00":
                emit("66C7_MOD10_WORD", TVA + i, "MOV WORD [%s+0x84],imm16" % REGS[rm], REGS[rm], "imm16")
                i += 11
                continue
        i += 1

    # note: REGS8 is defined at module level
    out["raw_hit_count"] = len(hits)

    # ---------- T2/T3: boundary + containment + provenance ----------
    MAX_EXTENT = 0x1000  # a known entry only contains hits within a plausible extent
    for h in hits:
        va = h["va"]
        pad_start, known_start = find_function_start(TEXT, TVA, va)
        anchor_ok = False
        anchor_start = None
        for st in (known_start, pad_start):
            if st is not None and st <= va and va - st <= MAX_EXTENT:
                if anchor_decode(TEXT, TVA, st, va):
                    anchor_ok = True
                    anchor_start = st
                    break
        ms_ok, ms_start = multi_start(TEXT, TVA, va)
        h["boundary"] = {
            "anchor_verified": anchor_ok,
            "anchor_start": "0x%08X" % anchor_start if anchor_start else None,
            "multi_start_verified": bool(ms_ok),
            "multi_start_used": "0x%08X" % ms_start if ms_start else None,
            "verified": bool(anchor_ok or ms_ok),
        }
        # containment: nearest plausible start (known entry OR padding boundary)
        cands = []
        if known_start is not None and known_start <= va and va - known_start <= MAX_EXTENT:
            cands.append(("known", known_start))
        if pad_start is not None and pad_start <= va and va - pad_start <= MAX_EXTENT:
            cands.append(("pad", pad_start))
        label = None
        used_start = None
        if cands:
            kind, st = max(cands, key=lambda c: c[1])
            used_start = st
            if kind == "known":
                label = KNOWN[st]
        h["containing_function"] = {
            "known_entry": "0x%08X" % known_start if known_start else None,
            "known_label": label,
            "attributed_start": "0x%08X" % used_start if used_start else None,
            "padding_delimited_start": "0x%08X" % pad_start if pad_start else None,
        }
        base = h["base"]
        fstart = h["containing_function"]["attributed_start"]
        fstart = int(fstart, 16) if fstart else None
        h["provenance_tags"] = provenance_tags(TEXT, TVA, fstart, va, base)
        h["window_bytes"] = TEXT[va - TVA - 24: va - TVA + 16].hex(" ")

    # ---------- T4: mechanical classification ----------
    def classify(h):
        form = h["form"]
        va = h["va"]
        base = h["base"]
        bver = h["boundary"]["verified"]
        tags = [t["tag"] for t in h["provenance_tags"]]
        # read forms -> NOT_A_WRITE
        if form.startswith("8B") or form.startswith("39"):
            role = ""
            if va in (0x0070DD1A,):
                role = " consumer gate CMP (FUN_0070DCF0)"
            elif va in (0x0070DD6A, 0x0070DD7E):
                role = " consumer stream load (FUN_0070DCF0)"
            elif va == 0x0070C6BE:
                role = " setter entry guard CMP (FUN_0070C680)"
            elif va == 0x0070BFD0:
                role = " stream bridge method load (FUN_0070BFD0)"
            return ("NOT_A_WRITE", "REJECTED_READ_NOT_WRITE",
                    "read/CMP form with displacement 0x84; no memory write occurs" + role)
        if not bver:
            return ("NOT_A_WRITE", "REJECTED_UNRELATED_OFFSET",
                    "raw byte-pattern occurrence not at a verified instruction start "
                    "(part of another instruction's immediate/displacement); not an instruction")
        # partial width
        if "BYTE" in form or "WORD" in form:
            return ("UNRESOLVED", "REJECTED_UNRELATED_OFFSET",
                    "partial-width (byte/word) store at +0x84; cannot fully assign the "
                    "dword pointer member at factory+0x84 (dword member per the base ctor "
                    "store @0x0070D013 and the setter store @0x0070C71E)")
        # stack-relative
        if base in ("ESP", "EBP"):
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "stack-relative slot; the factory object is heap-allocated (new 0x118 "
                    "@0x0073E2CC lazy-init); a stack slot cannot be the factory's +0x84 member")
        # the two confirmed factory-family writes
        if va == 0x0070D013:
            return ("INITIALIZATION_NULL", "CONFIRMED_FACTORY_PLUS_84_WRITE",
                    "FUN_0070CF80 factory base ctor: MOV [ESI+0x84],EBX with EBX=0 (XOR EBX,EBX "
                    "@0x0070CFBC); executes during construction of every factory class incl. "
                    "20006 (derived ctor FUN_0073B820 CALL FUN_0070CF80 @0x0073B87D); "
                    "prior-canon pin re-verified")
        if va == 0x0070C71E:
            return ("NONNULL_ASSIGNMENT", "CONFIRMED_FACTORY_PLUS_84_WRITE",
                    "FUN_0070C680 stream-attach setter: MOV [ESI+0x84],EAX with ESI=this and EAX="
                    "new(0xA4)-object constructed by FUN_00972380 (CALL @0x0070C715) or 0 on "
                    "allocation failure (XOR EAX,EAX @0x0070C71C); entry guard CMP [ESI+0x84],EDI "
                    "@0x0070C6BE makes the store conditional on the member being NULL at entry")
        # known-object containment
        lbl = h["containing_function"]["known_label"]
        if lbl == "FUN_00707E50_manager_ctor" and form.startswith("8D"):
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "LEA+store wrapper to manager+0x84 inside FUN_00707E50 (the manager ctor; "
                    "inline RB-tree init at manager+0x84); the manager class (0x100 B, singleton "
                    "0x00BA12E4) is distinct from the factory class (0x118 B, singleton 0x00BA590C)")
        if h["form"].startswith("8D"):
            return ("UNRESOLVED", "UNRESOLVED",
                    "LEA reg,[reg+0x84]; no store-through-reg linked within the bounded window; "
                    "wrapper-setter form not confirmed")
        # hand-verified window-evidence rejections (layout/value evidence inside the
        # bounded window; each documented with its window bytes in 01_RAW/S2_CENSUS.json)
        if va == 0x0074955A:
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "sibling-class ctor: window shows the SAME base written at +0x7C/+0x80/+0x84 "
                    "as dwords but +0x88/+0x89 as BYTES (88 9E 88 / 88 9E 89); the factory class "
                    "layout has a DWORD slot-array vector at +0x88 (begin) with end at +0x8C "
                    "(FUN_0070E2F0/FUN_0070C180 canon) - class-layout mismatch, different object")
        if va == 0x0075138F:
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "window shows LEA ECX,[ESI+0x88] + a helper CALL = a synchronization object "
                    "initialized at this class's +0x88; the factory class has its slot-array "
                    "vector at +0x88 (dword begin/end, FUN_0070E2F0 canon) - class-layout "
                    "mismatch, different object")
        if va == 0x007196AA:
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "window shows static globals 0x00BA921C/0x00BA9220/0x00BA9224 copied into "
                    "+0x84/+0x88/+0x8C of the base object; the factory ctor writes +0x84 from a "
                    "zeroed register (EBX=0) and its +0x88 is a vector built by FUN_0070E2F0 - "
                    "different init grammar, different object")
        if va == 0x006D4F88:
            return ("UNRESOLVED", "REJECTED_WRONG_OBJECT",
                    "large-class ctor: window shows +0x84 written from ESI where ESI was loaded "
                    "with the immediate 4 (BE 04 00 00 00) and dozens of members initialized "
                    "from ECX/ESI in the same ctor; a factory +0x84 is never assigned the integer "
                    "4; different object")
        # everything else: unresolved at window level
        return ("UNRESOLVED", "UNRESOLVED",
                "boundary-verified non-stack dword write to [reg+0x84]; base-register identity "
                "not resolved to any factory object within the window-level provenance bound; "
                "not established as a factory+0x84 write (no claim made)")

    for h in hits:
        wc, cl, reason = classify(h)
        h["write_class"] = wc
        h["classification"] = cl
        h["reason"] = reason

    # LEA-wrapper linkage: find LEA reg,[base+0x84] followed by MOV [reg],src within 16 bytes
    lea_rows = [h for h in hits if h["form"].startswith("8D")]
    for lr in lea_rows:
        dst_reg = lr["desc"].split()[1].rstrip(",")
        regnum = REGS.index(dst_reg) if dst_reg in REGS else -1
        if regnum < 0:
            continue
        lo = lr["va"] - TVA + 3
        if lr["form"].endswith("disp32"):
            lo = lr["va"] - TVA + 6
        end = min(N, lo + 24)
        j = lo
        while j < end:
            if TEXT[j] == 0x89 and ((TEXT[j+1] >> 3) & 7) == regnum and (TEXT[j+1] >> 6) == 0 and (TEXT[j+1] & 7) != 4:
                lr["lea_linked_store"] = {"at": "0x%08X" % (TVA + j),
                                          "desc": "MOV [%s],%s" % (dst_reg, REGS[TEXT[j+1] & 7])}
                break
            if TEXT[j] == 0x89 and ((TEXT[j+1] >> 3) & 7) == regnum and (TEXT[j+1] >> 6) != 3 and (TEXT[j+1] & 7) == regnum:
                pass
            L = insn_len(TEXT, j)
            if L is None:
                break
            j += L
    # classify linked LEA rows as wrapper candidates
    for h in hits:
        if h["form"].startswith("8D") and "lea_linked_store" in h:
            base = h["base"]
            if base in ("ESP", "EBP"):
                h["write_class"] = "UNRESOLVED"
                h["classification"] = "REJECTED_WRONG_OBJECT"
                h["reason"] = ("LEA+store wrapper to a stack-relative +0x84 slot; "
                               "stack slot, not the heap factory member")
            else:
                h["write_class"] = "UNRESOLVED"
                h["classification"] = "UNRESOLVED"
                h["reason"] = ("LEA+store wrapper candidate: LEA reg,[%s+0x84] then a store "
                               "through reg at %s; base object identity not resolved to the "
                               "factory within the window bound" % (base, h["lea_linked_store"]["at"]))

    # ---- stats ----
    stats = {}
    for h in hits:
        stats.setdefault(h["classification"], 0)
        stats[h["classification"]] += 1
    form_stats = {}
    for h in hits:
        form_stats.setdefault(h["form"], 0)
        form_stats[h["form"]] += 1
    dword_write_candidates = [h for h in hits if h["form"].startswith(("89", "C7"))]
    nonstack = [h for h in dword_write_candidates if h["base"] not in ("ESP", "EBP")]
    out["census_stats"] = {
        "raw_hits": len(hits),
        "by_form": form_stats,
        "by_classification": stats,
        "dword_write_form_hits": len(dword_write_candidates),
        "dword_write_nonstack_base": len(nonstack),
        "boundary_verified_writes": len([h for h in dword_write_candidates if h["boundary"]["verified"]]),
        "boundary_verified_nonstack_writes": len([h for h in nonstack if h["boundary"]["verified"]]),
        "confirmed_factory_writes": len([h for h in hits if h["classification"] == "CONFIRMED_FACTORY_PLUS_84_WRITE"]),
    }
    with open(os.path.join(RUN, "01_RAW", "S2_CENSUS.json"), "w", newline="\n") as f:
        out["hits"] = hits
        json.dump(out, f, indent=1)

    # ---- CSV (real csv module) ----
    csv_path = os.path.join(RUN, "FACTORY_PLUS_84_WRITE_CENSUS.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate", "va", "instruction", "base_identity", "source_operand",
                    "caller_context", "write_class", "classification", "reason"])
        for h in hits:
            w.writerow([
                "%s@0x%08X" % (h["form"], h["va"]),
                "0x%08X" % h["va"],
                h["desc"],
                h["base"] + (" (boundary-verified)" if h["boundary"]["verified"] else " (boundary-unverified)"),
                h["src"],
                (h["containing_function"]["known_label"] or
                 ("entry~" + h["containing_function"]["attributed_start"] if h["containing_function"]["attributed_start"] else "unknown")),
                h["write_class"],
                h["classification"],
                h["reason"],
            ])
    print("S2 done. raw=%d dword_writes=%d nonstack=%d confirmed=%d csv=%s"
          % (len(hits), len(dword_write_candidates), len(nonstack),
             out["census_stats"]["confirmed_factory_writes"], csv_path))

if __name__ == "__main__":
    main()
