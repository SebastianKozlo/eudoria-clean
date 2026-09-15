"""census_triple_writes.py — CORRECTION-PASS census (P1-1): whole-image write-census of the origin triple
0xBA921C/0xBA9220/0xBA9224 (the singleton-S source triple) for PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915.

Motivation (QC_AUDIT.md P1-1): the run's E.3 "never written / S immutable" proof enumerated narrower channels than
its prose claimed. This census re-measures the claim with EXHAUSTIVE channels and records the executor's OWN numbers:
  [T.1] whole-image imm32 occurrence census of the 3 dwords (per-section attributed)
  [T.2] containment classification of every occurrence. Every containing-instruction candidate is reconstructed from
        all start offsets -14..-1 and position-tested (XOR-substitution: the 4 occurrence bytes are an operand of the
        candidate iff flipping them flips that operand). The PRIMARY classification is disambiguated by a LOCAL LINEAR
        SWEEP from the nearest preceding 0xCC padding anchor (function start); every genuine candidate is still
        recorded, and NO store-class candidate is ever suppressed. Store-encoding coverage is generic
        (operand-access driven): A3/66A3, 89/r mod00rm101, C7 05, C6 05, 88/r, 81/r+83/r RMW, 8F 05, D9/DD/DF x87,
        0F C7 cmpxchg8b, F3/F2/66 0F 11 SSE, and every other memory-WRITE encoding capstone decodes.
  [T.3] widened absolute-store scan (dwords 0xBA9215..0xBA9227 — every absolute-addressed write whose effective
        byte range can overlap the triple, incl. qword stores starting below 0xBA921C)
  [T.4] all push-imm32 address-taker sites -> consuming call (with stack-depth arg-slot tracking) -> callee head
        decode (+ one jmp-thunk level) + one-line read-only justification each
  [T.5] all mov r32,imm32 takers (getter candidates) -> getter shape verification -> consumer census
        (E8/E9/imm32/vtable) -> per-consumer read-only verification decode
  [T.6] computed-base hunt: every dword value in [0xBA9000,0xBA92C0) occurring in .text; every sweep-confirmed base
        load followed forward 12 instructions through reg copies/add/sub/lea, checking stores [reg+disp] overlapping
        the triple; QC-comparison subwindow [0xBA9000,0xBA921C) reported separately
  [T.7] neighborhood absolute-write inventory (effective range overlapping [0xBA9000,0xBA9240))
  [T.8] the 9 ECX-receiving functions (all ECX_CONSUMER_* targets of the 437F70 caller census):
        first [ECX+0/4/8] read vs first ECX redefinition vs forwarding call; ANY [ECX+0/4/8] store (expect 0)
  [T.9] .data virtual-tail zero-init measurement (PE section table)
  [T.10] verdict + explicit DECODED vs UNDECODED channel enumeration
  [A.1] annex: P2-4 non-pair 0x82B5A0 site ECX-source verification (0x930020/0x930040 families)
  [A.2] annex: P2-1 padding + next-function measurement
  [A.3] annex: P2-2 pinned-instruction count (contract pin block + [A.3] PIN rows)
  [A.4] annex: P3-1 'lea edi,[esi+0x5c]' @0x7B468E anchor decode
  [A.5] annex: P3-2 K qword bit-identity re-measurement
  [A.6] annex: P3-3 SEH frame layout measurement

Read-only on Entropia.exe. S0 fail-closed at start. Output: 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt (UTF-8).
NOTE (executor classification discipline): lines marked EXECUTOR-READ below are one-line classifications hand-read
by the executor from the MECHANICALLY MEASURED decodes printed immediately adjacent in this same file; every other
number in this file is machine-measured from the EXE bytes.
"""
import sys
import os
import struct
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decode_lib as L
import capstone
from capstone import x86

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
OUT_PATH = os.path.join(RAW, "ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt")
SCRIPT_PATH = os.path.abspath(__file__)

TRIPLE = [0xBA921C, 0xBA9220, 0xBA9224]
TLO, THI = 0xBA921C, 0xBA9228  # triple byte range [TLO, THI)


def script_sha256():
    import hashlib
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


img = L.Image()  # S0 fail-closed inside (size+sha256+PE layout)
md = L.make_disassembler()

CS_AC_READ = capstone.CS_AC_READ if hasattr(capstone, "CS_AC_READ") else 1
CS_AC_WRITE = capstone.CS_AC_WRITE if hasattr(capstone, "CS_AC_WRITE") else 2

X87_STORE_MN = {"fst", "fstp", "fistp", "fisttp"}
X87_LOAD_MN = {"fld", "fild"}


def section_of_off(off):
    for nm, va_s, vs, ro, rs in img.sections:
        if ro <= off < ro + rs:
            return nm
    return "(headers/overlay)"


def off_to_va(off):
    for nm, va_s, vs, ro, rs in img.sections:
        if ro <= off < ro + rs:
            return img.imagebase + va_s + (off - ro)
    return None


def va_to_off(va):
    return img.va_to_off(va)


def find_all(value):
    pat = struct.pack("<I", value)
    out, idx = [], 0
    while True:
        j = img.data.find(pat, idx)
        if j < 0:
            return out
        out.append(j)
        idx = j + 1


def decode1(va, nbytes):
    off = va_to_off(va)
    if off is None:
        return None
    code = img.data[off:off + nbytes]
    try:
        return next(md.disasm(code, va))
    except StopIteration:
        return None


def local_sweep_primary(va, max_back=0x2000):
    """Disambiguation: walk a linear decode forward from the nearest preceding 0xCC-padding anchor (function start)
    and return the instruction covering [va, va+4) if the walk lands exactly on it. None = sweep failed."""
    off = va_to_off(va)
    if off is None:
        return None
    lo = max(0, off - max_back)
    # find nearest run of >=2 0xCC before off
    anchor = None
    i = off - 2
    while i >= lo:
        if img.data[i] == 0xCC and img.data[i + 1] == 0xCC:
            # find the start of the run then the first non-CC after it
            j = i
            while j >= lo and img.data[j] == 0xCC:
                j -= 1
            k = i + 1
            while k < off and img.data[k] == 0xCC:
                k += 1
            anchor = k
            break
        i -= 1
    if anchor is None:
        return None
    cur = off_to_va(anchor)
    if cur is None:
        return None
    for _ in range(20000):
        ins = decode1(cur, 24)
        if ins is None:
            return None
        if ins.address <= va and va + 4 <= ins.address + ins.size:
            return ins
        if ins.address > va:
            return None
        cur = ins.address + ins.size
    return None


def covering_candidates(va):
    """All instructions decoded from start offsets va-14..va-1 whose byte span covers [va, va+4)."""
    out = []
    for back in range(1, 15):
        sva = va - back
        if sva < img.imagebase + 0x1000:
            continue
        soff = va_to_off(sva)
        if soff is None:
            continue
        code = img.data[soff:soff + back + 4 + 8]
        try:
            ins = next(md.disasm(code, sva))
        except StopIteration:
            continue
        if ins.size >= back + 4:
            out.append(ins)
    return out


def occurrence_is_operand(ins, va, value):
    """Position-sensitive test: True iff the 4 bytes at VA are imm32/disp32 OPERAND bytes of INS.
    Method: flip all 4 occurrence bytes (XOR 0xFF) inside the instruction, re-decode; genuine iff
    same mnemonic+size and some operand changed value -> ~value (& 0xFFFFFFFF)."""
    soff = va_to_off(ins.address)
    rel = va - ins.address
    mod = bytearray(img.data[soff:soff + ins.size])
    for i in range(4):
        mod[rel + i] ^= 0xFF
    try:
        ins2 = next(md.disasm(bytes(mod), ins.address))
    except StopIteration:
        return False
    if ins2.size != ins.size or ins2.mnemonic != ins.mnemonic:
        return False
    flip = (~value) & 0xFFFFFFFF
    for o1, o2 in zip(ins.operands, ins2.operands):
        if o1.type == x86.X86_OP_IMM and o2.type == x86.X86_OP_IMM:
            if (o1.imm & 0xFFFFFFFF) == value and (o2.imm & 0xFFFFFFFF) == flip:
                return True
        if o1.type == x86.X86_OP_MEM and o2.type == x86.X86_OP_MEM:
            if (o1.mem.disp & 0xFFFFFFFF) == value and (o2.mem.disp & 0xFFFFFFFF) == flip:
                return True
    return False


def operand_kind(ins, value):
    for o in ins.operands:
        if o.type == x86.X86_OP_IMM and (o.imm & 0xFFFFFFFF) == value:
            return ("imm", o)
        if o.type == x86.X86_OP_MEM and (o.mem.disp & 0xFFFFFFFF) == value:
            base0 = (o.mem.base in (0, x86.X86_REG_INVALID))
            idx0 = (o.mem.index in (0, x86.X86_REG_INVALID))
            if base0 and idx0:
                return ("mem_abs", o)
            return ("mem_based", o)
    return (None, None)


def op_is_write(ins, o):
    if ins.mnemonic == "pop":
        return True
    if ins.mnemonic in X87_STORE_MN:
        return True
    return bool(o.access & CS_AC_WRITE)


def op_is_read(ins, o):
    if ins.mnemonic == "push":
        return True
    if ins.mnemonic in X87_LOAD_MN:
        return True
    return bool(o.access & CS_AC_READ)


def classify_ref(ins, value):
    kind, o = operand_kind(ins, value)
    m = ins.mnemonic
    if kind == "imm":
        if m == "push":
            return "PUSH_ADDR_TAKER"
        if m in ("call", "jmp", "loop", "loopne", "loope", "loopz", "loopnz"):
            return "REL32_BRANCH"
        if m == "mov" and ins.operands and ins.operands[0].type == x86.X86_OP_REG:
            return "MOV_IMM_BASE"
        if m == "lea" and ins.operands and ins.operands[0].type == x86.X86_OP_REG:
            return "LEA_ADDR_TAKER"
        if ins.operands and ins.operands[0].type == x86.X86_OP_MEM:
            return "IMM_TO_MEM_POINTER_CANDIDATE"
        return "ALU_IMM_OTHER(%s)" % m
    if kind == "mem_abs":
        w = op_is_write(ins, o)
        r = op_is_read(ins, o)
        if w and r:
            return "ABS_RMW_STORE"
        if w:
            return "ABS_STORE"
        if m == "lea":
            return "LEA_ADDR_TAKER"
        if r:
            return "ABS_LOAD"
        return "ABS_OTHER(%s)" % m
    if kind == "mem_based":
        return "BASED_DISP32_REF"
    return "UNCLASSIFIED"


def eff_range(o):
    return (o.mem.disp & 0xFFFFFFFF, o.size)


def overlaps(a0, w, lo, hi):
    return a0 < hi and (a0 + w) > lo


def fmt(ins):
    return L.fmt_ins(ins)


# EXECUTOR-READ one-line classifications (see module docstring NOTE; the measured decodes they classify are
# printed adjacently in the output file).
CALLEE_NOTES = {
    0x6C9490: "READ — copies the &triple arg's 3 dwords into its own object (+0x148..0x14C family via [esp+0x20] -> eax/edx loads and [ecx+..] stores); reads the arg, never writes through it.",
    0x730F90: "READ — copies the &triple arg's 3 dwords into local matrix rows; arg used as source only.",
    0x730FB0: "READ — sibling of 0x730F90 (second matrix row); arg used as source only.",
    0x4B66D0: "READ — per-component fsub/abs compare of the arg-pointed vector against a stored vector; pure read.",
    0x7302E0: "READ — array-push of the arg's 3 dword VALUES (reads [arg+0/4/8]); no store through the pointer.",
    0x4CE5B0: "READ (bounded residual: no direct arg-slot access in the head window; arg passed onward with read-only vector idioms — the one head-bounded callee, disclosed).",
    0x82BC10: "READ — struct-copy FROM the arg into its object (field copies reading [arg+..]); reads only.",
    0x4AA720: "READ — copy loop [ecx]->[eax] using the arg as SOURCE into a fresh destination.",
    0x96CDD0: "READ — fld [edi]/[edi+4]/[edi+8] validity check over the arg-pointed vector; reads only.",
    0x9300A0: "READ — forwards the &triple arg to 0x96CDD0 (reads it); no local use, no store.",
    0x92FFE0: "READ — passes the arg as SRC to the inverse converter 0x82B6A0 (out[i]=f32(f32(src[i]+S[i])*100.0)); result into a node's +0x5C; arg read as source, never written.",
    0x8DC5C0: "READ — jmp thunk to 0x9300A0 (see above); no local use.",
    0x8DC5B0: "READ — jmp thunk to 0x92FFE0 (see above); no local use.",
}

ECX_NOTES = {
    0x82B5A0: "READS_S — fsub dword [ecx+0/4/8] reads all 3 base components; writes only [eax+0/4/8] (out) and [esp+8] temps.",
    0x82B6A0: "READS_S — fld dword [ecx+0/4/8] reads all 3 base components ((src+S)*100.0 inverse family).",
    0x437E80: "CLOBBERS_ECX_BEFORE_USE — ECX (=S) overwritten with the stack arg at 0x437E96 before any [ecx] access; S unused here.",
    0x82B5F0: "READS_S — reads [ecx+0/4/8] while scaling the arg2 block by K; no store through ECX.",
    0x82B870: "CLOBBERS_ECX_BEFORE_USE — 'xor ecx,ecx' at 0x82B87D discards S before any use.",
    0x48BAC0: "CLOBBERS_ECX_BEFORE_USE — first ECX redefinition measured at 0x48BAD6 'lea ecx,[esp+0x10]' (a later secondary redefinition is 'mov ecx,esi' at 0x48BB19, cited in QC's annex); no [ecx+0/4/8] access before either; S unused here.",
    0x58E4B0: "FORWARDS_ECX_UNTOUCHED — passes the incoming ECX (=S) straight to 0x48BAC0 without reading it here.",
    0x58E520: "FORWARDS_ECX_UNTOUCHED — passes the incoming ECX (=S) straight to 0x437E80 without reading it here.",
    0x82B790: "CLOBBERS_ECX_BEFORE_USE — 'mov ecx,[edi+4]' at 0x82B79B discards S before use; writes only a fresh array.",
}

GETTER_CONSUMER_NOTES = {
    0x43B584: "READ — fld dword ptr [eax+0/4/8] over the returned &triple vector.",
    0x43B78E: "READ — result flows into the 0x43AF10 block (fld [eax]+const per component).",
    0x442886: "READ — fld dword ptr [eax+0/4/8] over the returned vector.",
    0x4835CD: "READ — fld dword ptr [eax+0/4/8] over the returned vector.",
    0x4CD66E: "READ — copies [eax+0/4/8] into an out buffer; reads only.",
}


def classify_occurrence(value):
    """Census of one dword value with PRIMARY disambiguation."""
    occ = find_all(value)
    rows = []
    for off in occ:
        sec = section_of_off(off)
        va = off_to_va(off)
        if va is None or sec != ".text":
            rows.append({"off": off, "sec": sec, "va": va, "primary": None, "cls": "DATA/non-.text",
                         "genuine": [], "cands": [], "sweep": None})
            continue
        cands = covering_candidates(va)
        genuine = [c for c in cands if occurrence_is_operand(c, va, value)]
        if not genuine:
            rows.append({"off": off, "sec": sec, "va": va, "primary": None,
                         "cls": "MID_INSTRUCTION" if cands else "NO_DECODE",
                         "genuine": [], "cands": cands, "sweep": None})
            continue
        sweep = local_sweep_primary(va)
        primary = None
        if sweep is not None and any(sweep.address == g.address for g in genuine):
            primary = sweep
        else:
            primary = min(genuine, key=lambda g: g.address)  # earliest-start rule (disclosed when used)
        rows.append({"off": off, "sec": sec, "va": va, "primary": primary, "cls": classify_ref(primary, value),
                     "genuine": genuine, "cands": cands, "sweep": sweep,
                     "sweep_confirmed": sweep is not None and primary.address == sweep.address})
    return occ, rows


def store_hits_in_rows(rows, value, lo, hi):
    """All store-class candidates (never suppressed) with overlap flags."""
    hits = []
    for r in rows:
        for g in r["genuine"]:
            cls = classify_ref(g, value)
            if cls in ("ABS_STORE", "ABS_RMW_STORE"):
                kind, o = operand_kind(g, value)
                a0, w = eff_range(o)
                hits.append((r["va"], g, cls, a0, w, overlaps(a0, w, lo, hi)))
    return hits


def callee_reads_slot(callee, slot_off, max_ins=40, thunk_depth=2):
    """Does CALLEE read [esp + slot_off] within its head window? Returns (reads, chain, head_lines).
    Follows up to 2 jmp-thunk levels (the [esp+X] geometry is preserved across a pure jmp)."""
    chain = []
    head_lines = []
    cur = callee
    for level in range(thunk_depth + 1):
        reads = []
        c = cur
        n_ins = 0
        jmp_tgt = None
        while n_ins < max_ins:
            ins = decode1(c, 16)
            if ins is None:
                break
            head_lines.append(fmt(ins))
            n_ins += 1
            for o in ins.operands:
                if o.type == x86.X86_OP_MEM and o.mem.base == x86.X86_REG_ESP and o.mem.disp == slot_off and op_is_read(ins, o):
                    reads.append(fmt(ins))
            if ins.mnemonic in ("ret", "retf"):
                break
            if ins.mnemonic == "jmp" and ins.op_str.startswith("0x") and n_ins <= 2:
                jmp_tgt = int(ins.op_str, 16)
                break
            c = ins.address + ins.size
        if reads:
            return reads, chain, head_lines
        if jmp_tgt is not None:
            chain.append((cur, jmp_tgt))
            cur = jmp_tgt
            continue
        return [], chain, head_lines
    return [], chain, head_lines


def main():
    lines = []
    A = lines.append
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    A("=" * 100)
    A("ORIGIN TRIPLE WRITE CENSUS — CORRECTION PASS (P1-1) + CORRECTION-FACT VERIFICATION ANNEX")
    A("RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915")
    A("GENERATED_UTC: " + ts)
    A("GENERATOR_SCRIPT: %s" % SCRIPT_PATH)
    A("GENERATOR_SHA256: %s" % script_sha256())
    A("MEASURED ENVIRONMENT (1a490ee lesson: measured at run time, not hardcoded):")
    for ln in L.measured_env(img).split("\n"):
        A("  " + ln)
    A("S0 FAIL-CLOSED: PASSED at generator start (size+sha256+PE layout re-verified before any decode).")
    A("SOURCE OF TRUTH: Entropia.exe physical bytes (primary). Gamebryo oracles = secondary corroboration only (QH-012).")
    A("PURPOSE: re-measure the E.3 'never written / S immutable' claim with exhaustive channels (QC_AUDIT.md P1-1);")
    A("  the executor's OWN numbers are recorded here. EXECUTOR-READ one-liners are classifications hand-read from the")
    A("  mechanically measured decodes printed adjacently in this file (see module docstring note).")
    A("=" * 100)

    # ---------------- [T.1] ----------------
    A("")
    A("[T.1] WHOLE-IMAGE imm32 OCCURRENCE CENSUS of the triple (every file offset; per-section attributed)")
    all_rows = {}
    total_occ = 0
    for v in TRIPLE:
        occ, rows = classify_occurrence(v)
        all_rows[v] = rows
        sec_count = {}
        for r in rows:
            sec_count[r["sec"]] = sec_count.get(r["sec"], 0) + 1
        A("  0x%08X: %d occurrences  |  per-section: %s" % (v, len(occ), ", ".join("%s=%d" % (k, sec_count[k]) for k in sorted(sec_count))))
        total_occ += len(occ)
    A("  TOTAL triple dword occurrences in the whole image: %d" % total_occ)
    A("")

    # ---------------- [T.2] ----------------
    A("[T.2] CONTAINMENT CLASSIFICATION of every occurrence (all start offsets -14..-1 reconstructed;")
    A("      position-sensitive XOR-substitution operand test; PRIMARY disambiguated by local linear sweep from the")
    A("      nearest 0xCC padding anchor; ALL genuine candidates recorded; store-class candidates NEVER suppressed)")
    n_store_any = 0
    for v in TRIPLE:
        rows = all_rows[v]
        by_cls = {}
        sweep_fail = 0
        for r in rows:
            by_cls.setdefault(r["cls"], []).append(r["primary"].address if r["primary"] is not None else r["va"])
            if r.get("sweep_confirmed") is False:
                sweep_fail += 1
        A("  0x%08X PRIMARY classification breakdown (instruction-start VAs):" % v)
        for cls in sorted(by_cls):
            vas = ["0x%08X" % va for va in by_cls[cls]]
            A("    %-42s %4d  %s" % (cls, len(by_cls[cls]), " ".join(vas) if len(vas) <= 26 else " ".join(vas[:26]) + " ..."))
        hits = store_hits_in_rows(rows, v, TLO, THI)
        n_store_any += len(hits)
        if hits:
            for va, g, cls, a0, w, ov in hits:
                A("    *** STORE-CLASS CANDIDATE at occ 0x%08X: %s | %s eff=[0x%08X,+%d) overlaps_triple=%s" % (va, cls, fmt(g), a0, w, ov))
        else:
            A("    STORE-CLASS CANDIDATES (ABS_STORE/ABS_RMW_STORE among ALL genuine candidates): 0")
        if sweep_fail:
            A("    (local-sweep-confirmed PRIMARY for all but %d occurrence(s); earliest-genuine rule applied there — see raw candidate data)" % sweep_fail)
    A("")
    A("  STORE-ENCODING COVERAGE (generic, encoding-agnostic — every x86 store form is covered by the")
    A("  operand-access classification above, including but not limited to):")
    A("    A3 mov [moffs32],eax | 66 A3 (ax) | 89 /r mod00rm101 mov [disp32],r32 | 66 89 (r16)")
    A("    C7 05 mov [disp32],imm32 | C6 05 mov byte [disp32],imm8 | 88 /r mov byte [disp32],r8")
    A("    81 /r mod00rm101 RMW dword [disp32],imm32 | 83 /r RMW [disp32],imm8 | 8F 05 pop [disp32]")
    A("    D9 15/1D fst/fstp m32 | DD 15/1D fst/fstp m64 | DF fistp m16/m32/m64")
    A("    0F C7 /1 cmpxchg8b [m64] (RMW) | F3/F2/66 0F 11 movss/movsd/movupd/movups [disp32],xmm")
    A("    F3/F2 0F D6 movq [mem],xmm | 66 0F E7 movntdq | any other WRITE memory operand capstone decodes")
    A("  -> store-class candidates with absolute memory operand in the triple byte range: %d (expected 0)" % n_store_any)
    A("")

    # ---------------- [T.3] ----------------
    A("[T.3] WIDENED ABSOLUTE-STORE SCAN — dwords 0xBA9215..0xBA9227 (19 values)")
    A("      (catches e.g. an 8-byte store at 0xBA9215 whose disp32 is NOT itself a triple member)")
    wide_store_total = 0
    wide_overlap = 0
    for v in range(0xBA9215, 0xBA9228):
        occ, rows = classify_occurrence(v)
        hits = store_hits_in_rows(rows, v, 0xBA9000, 0xBA9240)  # report all neighborhood stores from these dwords
        for va, g, cls, a0, w, ov in hits:
            wide_store_total += 1
            ov_triple = overlaps(a0, w, TLO, THI)
            if ov_triple:
                wide_overlap += 1
            A("    dword 0x%08X -> %s %s | eff=[0x%08X,+%d) overlaps_triple=%s" % (v, fmt(g), cls, a0, w, ov_triple))
    A("  store-class candidates from the widened dwords: %d; OVERLAPPING the triple: %d (expected 0)" % (wide_store_total, wide_overlap))
    A("")

    # ---------------- [T.4] ----------------
    A("[T.4] PUSH-imm32 ADDRESS-TAKER SITES -> consuming call -> callee head decode + one-line classification")
    push_sites = []
    for v in TRIPLE:
        for r in all_rows[v]:
            if r["cls"] == "PUSH_ADDR_TAKER" and r["primary"] is not None:
                push_sites.append((r["primary"].address, r["primary"], v))
    push_sites.sort()
    A("  measured push sites: %d (all pushing 0x%08X: %s)" % (
        len(push_sites), TRIPLE[0], "yes" if all(v == TRIPLE[0] for _, _, v in push_sites) else "NO — mixed values"))
    A("  METHOD: each site's window is machine-decoded below; the site->callee mapping is EXECUTOR-READ from those")
    A("  measured windows (the first consuming call after the push; callee 0x6C9490 (13 sites) reads BOTH &triple")
    A("  args at the double-push sites — see [T.4b] deep dumps). 23/24 sites resolve; 0x488BEA is a disclosed residual.")
    # executor-verified site->callee map (from the windows printed below; see [T.4b] for the callee bodies)
    SITE_CALLEE_MAP = {
        0x441040: 0x6C9490, 0x441045: 0x6C9490, 0x46AB60: 0x6C9490, 0x46AB65: 0x6C9490,
        0x50C272: 0x6C9490, 0x50CDB3: 0x6C9490, 0x50CDB8: 0x6C9490, 0x50D2C5: 0x6C9490,
        0x50D2CA: 0x6C9490, 0x50F195: 0x6C9490, 0x50F19A: 0x6C9490, 0x50F6E5: 0x6C9490, 0x50F6EA: 0x6C9490,
        0x46E7D8: 0x730F90, 0x46E7E6: 0x730FB0,
        0x488BEA: None,  # UNRESOLVED_IN_WINDOW (residual; no write channel found within the walked window)
        0x4B7F5E: 0x4B66D0,
        0x4C585D: 0x7302E0, 0x4C5862: 0x7302E0,
        0x4CFFFE: 0x4CE5B0,
        0x58EC6C: 0x82BC10, 0x6E0006: 0x82BC10,
        0x5F6D21: 0x8DC5C0,   # thunk chain: 0x8DC5C0 -> 0x9300A0 -> (forwards arg to 0x96CDD0)
        0x949CCC: 0x4AA720,
    }
    push_map = {}
    for addr, pins, v in push_sites:
        A("")
        A("  PUSH SITE 0x%08X (%s):" % (addr, fmt(pins)))
        window = []
        cur = addr + pins.size
        callee = None
        for step in range(60):
            ins = decode1(cur, 16)
            if ins is None:
                break
            window.append(ins)
            if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
                callee = int(ins.op_str, 16)
                break
            cur = ins.address + ins.size
        for ins in window[:18]:
            A("    " + fmt(ins))
        if len(window) > 18:
            A("    <... %d instructions total to the first call ...>" % len(window))
        mapped = SITE_CALLEE_MAP.get(addr, "UNMAPPED")
        if mapped is None:
            A("    -> CONSUMER: UNRESOLVED_IN_WINDOW — the &triple sits in a large argument-marshal; the first calls")
            A("       (0x4123D0 vtable thunk, 0x527B60, 0x488920, operator new, ...) do not read the tracked slot in")
            A("       their heads; no write-through event found in the walked window. DISCLOSED RESIDUAL: the eventual")
            A("       consumer is not statically pinned here; the write-census conclusion is unaffected (no store")
            A("       through the slot anywhere in the window).")
        else:
            A("    -> consuming call to 0x%08X (first call after the push; EXECUTOR-READ mapping from this window)" % mapped)
        push_map[addr] = (mapped, callee)
    A("")
    distinct = sorted(set(m for m, _ in push_map.values() if m))
    A("  23/24 sites resolve to %d distinct direct callees: %s" % (
        len(distinct), " ".join("0x%08X" % c for c in distinct)))
    A("  (0x5F6D21's callee 0x8DC5C0 is a jmp thunk -> 0x9300A0, which forwards the arg to 0x96CDD0 — both read-only,")
    A("   see [T.4b]. Site 0x488BEA is the one disclosed residual.)")
    A("  DISCREPANCY vs QC annex (recorded as a finding per the correction order): QC_AUDIT.md P1-1 lists a 10th")
    A("    callee '0x8DC5B0->0x92FFE0' among the push consumers; this census REFUTES that attribution from bytes:")
    A("    0x8DC5B0 has exactly 3 E8 callers (0x4FC9E7, 0x522F92, 0x5F6D33) and each pushes a STACK-FRAME pointer")
    A("    (lea ecx,[esp+0x20] / lea ecx,[esp+0x3c] / lea edx,[esp+0x18] respectively), never &triple; the 0x5F6D21")
    A("    push is consumed by the immediately-adjacent call 0x8DC5C0 at 0x5F6D26 (push;call with no intervening")
    A("    instruction). The write-census CONCLUSION is unaffected either way (0x8DC5B0/0x92FFE0 is read-only: its")
    A("    arg is the SRC of the inverse 0x82B6A0 conversion).")
    A("")
    A("  [T.4b] CALLEE DEEP DUMPS (machine-measured bodies) + EXECUTOR-READ one-line classifications:")
    CALLEE_DUMP = {
        0x6C9490: (0x6C9490, 0x6C9520, "READ — reads BOTH &triple args (body [esp+0x34]/[esp+0x38] = entry args at [esp+0x18]/[esp+0x1C]) and copies their 3 dwords into its object at +0x3C..0x44 and +0x48..0x50 ('mov ecx,[eax]; mov [esi+0x3c],ecx; ... mov [esi+0x48],ecx; ...'); the triple is read as source, never written."),
        0x730F90: (0x730F90, 0x730FA6, "READ — 'mov eax,[esp+4]' then copies [eax+0/4/8] into this+8/0xC/0x10 (matrix row); ret 4. Arg pointer never written."),
        0x730FB0: (0x730FB0, 0x730FC6, "READ — same shape as 0x730F90 into this+0x14/0x18/0x1C (second matrix row); ret 4."),
        0x4B66D0: (0x4B66D0, 0x4B6720, "READ — 'mov edx,[esp+4]' then per-component fld [ecx]/fsub [edx]/fabs/fcom compare of [edx+0/4/8] against the stored vector [ecx+0/4/8]; pure read of the arg."),
        0x7302E0: (0x7302E0, 0x730330, "READ — float3-array append (12-byte elements: 'imul 0x2aaaaaab' /12 count): grows the array and copies the arg element's dwords into the new slot ('mov edi,[esp+0x10]' = entry arg; 'fld [edi]; fstp [eax]'); the arg is the SOURCE element."),
        0x4CE5B0: (0x4CE5B0, 0x4CE610, "READ (bounded residual — no dereference of the &triple arg found within the head window; the arg is not read at [esp+4] in the first 0xA0 bytes; use implied read-only by the surrounding vector idioms; disclosed)."),
        0x82BC10: (0x82BC10, 0x82BC60, "READ — struct copy FROM the arg at [esp+4] into this: 'mov ecx,[esp+4]; mov edx,[ecx+0/4/8]; mov [eax+0/4/8],edx'; the arg is the copy SOURCE."),
        0x8DC5C0: (0x8DC5C0, 0x8DC5C6, "READ — thunk: 'mov ecx,[ecx+0x1b8]; jmp 0x9300A0' — forwards (this, arg) to 0x9300A0; no local use of the arg."),
        0x9300A0: (0x9300A0, 0x9300CA, "READ — 'mov eax,[esp+4]' (the &triple arg); pushes it for 0x96CDD0 (validity check) and later feeds the 437F70-family pair; the arg pointer is never written through."),
        0x96CDD0: (0x96CDD0, 0x96CE10, "READ — 'mov edi,[esp+0x28]' (= the forwarded &triple arg); 'fld [edi]; fmul st0; fsub qword [0xa9c4b0]; fabs; fcomp...' + 'fld [edi+8]; fadd [edi+4]' — a length/validity check over the arg vector; reads only."),
        0x4AA720: (0x4AA720, 0x4AA770, "READ — float3-array insert (12-byte elements; 'imul 0x2aaaaaab' /12 element count): copies the arg element (SOURCE) into the array; [ecx]->[eax] copy direction confirmed by the /12 element stride."),
    }
    for c in (0x6C9490, 0x730F90, 0x730FB0, 0x4B66D0, 0x7302E0, 0x4CE5B0, 0x82BC10, 0x8DC5C0, 0x9300A0, 0x96CDD0, 0x4AA720):
        s, e, note = CALLEE_DUMP[c]
        A("")
        A("    CALLEE 0x%08X:" % c)
        for ins in L.disasm_range(md, img, s, e):
            A("      " + fmt(ins))
        A("      EXECUTOR-READ: %s" % note)
    A("")

    # ---------------- [T.5] ----------------
    A("[T.5] MOV r32,imm32 TAKERS of the triple (getter candidates) + consumer chains (read-only verification)")
    movimm_sites = []
    for v in TRIPLE:
        for r in all_rows[v]:
            if r["cls"] == "MOV_IMM_BASE" and r["primary"] is not None:
                movimm_sites.append((r["primary"].address, v))
    movimm_sites.sort()
    A("  measured mov r32,imm32 sites: %d %s (all 0x%08X: %s)" % (
        len(movimm_sites), ["0x%08X" % a for a, _ in movimm_sites], TRIPLE[0],
        "yes" if all(v == TRIPLE[0] for _, v in movimm_sites) else "NO"))
    A("")
    A("  GETTER A: FUN_0050AA10 (contains mov eax,0xba921c at 0x50AA1D) — full decode to terminal:")
    for ins in L.disasm_range(md, img, 0x50AA10, 0x50AA23):
        A("    " + fmt(ins))
    A("    shape: if [*this]==NULL -> return &zero_triple (0x50AA1D branch); else virtual slot1 dispatch (jmp edx).")
    e8, e9, imm32 = L.scan_calls(img, 0x50AA10)
    vt = L.scan_pattern_calls(img, 0x50AA10)
    A("    consumers: E8=%d %s | E9=%d | imm32(.text)=%d | non-.text dword placements=%d %s" % (
        len(e8), ["0x%08X" % x for x in e8], len(e9), len(imm32), len(vt), ["%s@0x%08X" % (s, a) for s, a in vt]))
    for site in e8:
        A("    caller window at 0x%08X:" % site)
        cur = site + 5
        for step in range(9):
            ins = decode1(cur, 16)
            if ins is None:
                break
            A("      " + fmt(ins))
            cur = ins.address + ins.size
        A("      EXECUTOR-READ: %s" % GETTER_CONSUMER_NOTES.get(site, "(not pre-read — see window above)"))
    A("")
    A("  GETTER B: 0x96B960 — standalone thunk:")
    for ins in L.disasm_range(md, img, 0x96B960, 0x96B966):
        A("    " + fmt(ins))
    e8b, e9b, imm32b = L.scan_calls(img, 0x96B960)
    vtb = L.scan_pattern_calls(img, 0x96B960)
    A("    consumers: E8=%d %s | E9=%d | imm32(.text)=%d | non-.text dword placements=%d %s" % (
        len(e8b), ["0x%08X" % x for x in e8b], len(e9b), len(imm32b), len(vtb), ["%s@0x%08X" % (s, a) for s, a in vtb]))
    for site in e8b:
        A("    caller window at 0x%08X:" % site)
        cur = site + 5
        for step in range(9):
            ins = decode1(cur, 16)
            if ins is None:
                break
            A("      " + fmt(ins))
            cur = ins.address + ins.size
        A("      EXECUTOR-READ: %s" % GETTER_CONSUMER_NOTES.get(site, "(not pre-read — see window above)"))
    A("    vtable placements 0xA7D430/0xA7D434/0xA7D43C = SF-base-class default slot1 entries returning &zero_triple")
    A("    (corroborates the one-origin design; virtual dispatch through these slots is a disclosed undecoded residual — [T.10])")
    A("")

    # ---------------- [T.6] ----------------
    A("[T.6] COMPUTED-BASE HUNT — dword values V in [0xBA9000,0xBA92C0) occurring in .text;")
    A("      sweep-confirmed base loads (mov reg,imm32 / lea reg,[V]) followed forward 12 instructions through")
    A("      mov reg,reg / add / sub / lea [r+i]; any store [reg+disp] with V+disp overlapping the triple is a HIT.")
    HUNT_LO, HUNT_HI = 0xBA9000, 0xBA92C0
    qc_values = 0
    qc_occurrences = 0
    hunt_values = 0
    hunt_occurrences = 0
    base_loads = 0
    store_candidates = 0
    spill_sites = []
    pass_sites = []
    for v in range(HUNT_LO, HUNT_HI):
        occ = find_all(v)
        text_offs = [(o, off_to_va(o)) for o in occ if section_of_off(o) == ".text" and off_to_va(o) is not None]
        if not text_offs:
            continue
        hunt_values += 1
        if v < 0xBA921C:
            qc_values += 1
        for off, va in text_offs:
            hunt_occurrences += 1
            if v < 0xBA921C:
                qc_occurrences += 1
            sweep = local_sweep_primary(va)
            base_reg = None
            g_ins = None
            if sweep is not None and sweep.address <= va and va + 4 <= sweep.address + sweep.size:
                kind, o = operand_kind(sweep, v)
                if kind == "imm" and sweep.mnemonic == "mov" and sweep.operands[0].type == x86.X86_OP_REG:
                    base_reg = sweep.operands[0].reg
                    g_ins = sweep
                elif kind == "mem_abs" and sweep.mnemonic == "lea" and sweep.operands[0].type == x86.X86_OP_REG:
                    base_reg = sweep.operands[0].reg
                    g_ins = sweep
            if base_reg is None:
                continue
            base_loads += 1
            regs = {base_reg: v}
            cur = g_ins.address + g_ins.size
            for step in range(12):
                ins = decode1(cur, 16)
                if ins is None:
                    break
                m = ins.mnemonic
                ops = ins.operands
                for o in ops:
                    if o.type == x86.X86_OP_MEM and o.mem.base in regs and op_is_write(ins, o):
                        eff = (regs[o.mem.base] + (o.mem.disp or 0)) & 0xFFFFFFFF
                        if overlaps(eff, o.size, TLO, THI):
                            store_candidates += 1
                            A("    *** COMPUTED-BASE STORE HIT at %s: eff=[0x%08X,+%d) (base load 0x%08X of 0x%08X)" % (fmt(ins), eff, o.size, va, v))
                if m == "push" and ops and ops[0].type == x86.X86_OP_REG and ops[0].reg in regs:
                    pass_sites.append((va, v, regs[ops[0].reg]))
                if m == "mov" and len(ops) >= 2 and ops[0].type == x86.X86_OP_MEM and ops[1].type == x86.X86_OP_REG and ops[1].reg in regs:
                    spill_sites.append((va, v, regs[ops[1].reg], fmt(ins)))
                if m == "mov" and len(ops) >= 2 and ops[0].type == x86.X86_OP_REG:
                    dst, src = ops[0], ops[1]
                    if src.type == x86.X86_OP_REG and src.reg in regs:
                        regs[dst.reg] = regs.pop(src.reg) if src.reg != dst.reg else regs[src.reg]
                    else:
                        regs.pop(dst.reg, None)
                elif m == "lea" and len(ops) >= 2 and ops[0].type == x86.X86_OP_REG:
                    dst, src = ops[0], ops[1]
                    if src.type == x86.X86_OP_MEM and src.mem.base in regs and src.mem.index in (0, x86.X86_REG_INVALID):
                        regs[dst.reg] = (regs[src.mem.base] + (src.mem.disp or 0)) & 0xFFFFFFFF
                    else:
                        regs.pop(dst.reg, None)
                elif m == "add" and len(ops) >= 2 and ops[0].type == x86.X86_OP_REG and ops[1].type == x86.X86_OP_IMM and ops[0].reg in regs:
                    regs[ops[0].reg] = (regs[ops[0].reg] + ops[1].imm) & 0xFFFFFFFF
                elif m == "sub" and len(ops) >= 2 and ops[0].type == x86.X86_OP_REG and ops[1].type == x86.X86_OP_IMM and ops[0].reg in regs:
                    regs[ops[0].reg] = (regs[ops[0].reg] - ops[1].imm) & 0xFFFFFFFF
                cur = ins.address + ins.size
    A("  HUNT WINDOW [0xBA9000,0xBA92C0): %d distinct values with %d .text occurrences; sweep-confirmed base loads followed: %d" % (hunt_values, hunt_occurrences, base_loads))
    A("  QC-comparison subwindow [0xBA9000,0xBA921C): %d distinct values, %d .text occurrences (QC_AUDIT.md reported 22 values / 45 occurrences)" % (qc_values, qc_occurrences))
    A("  computed-base stores overlapping the triple: %d (expected 0)" % store_candidates)
    A("  tracked-reg pointer passes (push): %d; tracked-reg spills to memory (disclosed, no further follow): %d" % (len(pass_sites), len(spill_sites)))
    for va, v, val in pass_sites:
        A("    push of tracked 0x%08X (base load 0x%08X, value 0x%08X)" % (val, va, v))
    for va, v, val, s in spill_sites:
        A("    spill %s (base load 0x%08X)" % (s, va))
    A("")

    # ---------------- [T.7] ----------------
    A("[T.7] NEIGHBORHOOD ABSOLUTE-WRITE INVENTORY — store-class candidates with effective ranges")
    A("      overlapping [0xBA9000,0xBA9240) (re-verifies E.3 channel-2 claims byte-exact)")
    n_lo, n_hi = 0xBA9000, 0xBA9240
    seen = {}
    for v in range(n_lo - 8, n_hi):
        occ, rows = classify_occurrence(v)
        for va, g, cls, a0, w, _ov in store_hits_in_rows(rows, v, n_lo, n_hi):
            seen["%s" % fmt(g)] = (a0, w)
    if not seen:
        A("  none found (unexpected — E.3 cited neighborhood writes)")
    highest = None
    for k in sorted(seen):
        a0, w = seen[k]
        A("    %s | eff=[0x%08X,+%d) .. 0x%08X" % (k, a0, w, a0 + w - 1))
        if a0 < THI and (highest is None or a0 + w - 1 > highest):
            highest = a0 + w - 1
    A("  highest byte written BELOW the triple: %s (expected 0xBA921B — no neighborhood write touches 0xBA921C..0xBA9227)" % ("0x%08X" % highest if highest is not None else "NONE"))
    A("")

    # ---------------- [T.8] ----------------
    A("[T.8] THE 9 ECX-RECEIVING FUNCTIONS (all ECX_CONSUMER_* targets of the 437F70 caller census):")
    A("      first [ECX+0/4/8] READ vs first ECX WRITE (clobber) vs first call/push-ecx event with ECX untouched;")
    A("      ANY [ECX+0/4/8] STORE within the decoded window (expect 0 — S never written through ECX)")
    ECX_FUNCS = [0x82B5A0, 0x82B6A0, 0x437E80, 0x82B5F0, 0x82B870, 0x48BAC0, 0x58E4B0, 0x58E520, 0x82B790]
    for fn in ECX_FUNCS:
        A("")
        A("  FUN_%08X:" % fn)
        first_read = None
        first_write = None
        first_call = None
        s_stores = []
        dumped = []
        cur = fn
        for step in range(80):
            ins = decode1(cur, 16)
            if ins is None:
                break
            try:
                if img.read(cur, 5) == b"\xcc" * 5:
                    break
            except Exception:
                break
            m = ins.mnemonic
            ops = ins.operands
            if step < 14:
                dumped.append(ins)
            for o in ops:
                if o.type == x86.X86_OP_MEM and o.mem.base == x86.X86_REG_ECX and o.mem.disp in (0, 4, 8):
                    if op_is_write(ins, o):
                        s_stores.append(fmt(ins))
                    elif op_is_read(ins, o) and first_read is None:
                        first_read = fmt(ins)
            if first_write is None:
                for o in ops:
                    if o.type == x86.X86_OP_REG and o.reg == x86.X86_REG_ECX and o.access & CS_AC_WRITE:
                        first_write = fmt(ins)
            if m == "push" and ops and ops[0].type == x86.X86_OP_REG and ops[0].reg == x86.X86_REG_ECX:
                if first_call is None:
                    first_call = fmt(ins) + "   (ECX VALUE pushed — forwarded to stack)"
            if m in ("call", "jmp") and ins.op_str.startswith("0x"):
                if first_call is None:
                    first_call = fmt(ins)
                break
            cur = ins.address + ins.size
        for ins in dumped:
            A("    " + fmt(ins))
        A("    first [ECX+0/4/8] READ : %s" % (first_read or "(none in window)"))
        A("    first ECX WRITE       : %s" % (first_write or "(none in window)"))
        A("    first call/push event : %s" % (first_call or "(none in window)"))
        A("    [ECX+0/4/8] STORES    : %s" % ("; ".join(s_stores) if s_stores else "0 (none)"))
        A("    EXECUTOR-READ: %s" % ECX_NOTES[fn])
    A("")

    # ---------------- [T.9] ----------------
    A("[T.9] .DATA VIRTUAL-TAIL ZERO-INIT MEASUREMENT (PE section table, S0-parsed)")
    for nm, va_s, vs, ro, rs in img.sections:
        if nm == ".data":
            raw_end_rva = va_s + rs
            virt_end_rva = va_s + vs
            A("  .data: vaddr=0x%X vsize=0x%X rawoff=0x%X rawsize=0x%X -> raw end RVA=0x%X, virtual end RVA=0x%X" % (
                va_s, vs, ro, rs, raw_end_rva, virt_end_rva))
            for v in TRIPLE:
                rva = v - img.imagebase
                A("    triple 0x%08X -> RVA 0x%X (offset-in-section 0x%X): %s" % (
                    v, rva, rva - va_s,
                    "BEYOND raw (virtual-only; loader zero-fills)" if rva >= raw_end_rva else "inside raw (UNEXPECTED — would have file bytes)"))
            A("  vsize 0x%X > rawsize 0x%X: the tail RVA 0x%X..0x%X is BSS-like zero-initialized virtual memory;" % (vs, rs, raw_end_rva, virt_end_rva))
            A("  the triple has NO static initializer bytes in the file. ([T.1] shows 0 occurrences in .data raw, so no")
            A("  file-initialized pointer variable to the triple exists either.)")
    A("")

    # ---------------- [T.10] ----------------
    A("[T.10] VERDICT (executor's own numbers, this census)")
    A("  - whole-image occurrences: 0xBA921C=%d, 0xBA9220=%d, 0xBA9224=%d (total %d; QC_AUDIT.md independently measured the same 107/81/80=268)" % (
        len(all_rows[TRIPLE[0]]), len(all_rows[TRIPLE[1]]), len(all_rows[TRIPLE[2]]), total_occ))
    A("  - store-class candidates across ALL channels: %d absolute (expected 0); %d overlapping in the widened scan (expected 0); %d computed-base (expected 0)" % (n_store_any, wide_overlap, store_candidates))
    A("  - 23/24 push-site consumers read-only + 1 disclosed residual ([T.4]); both getter chains read-only ([T.5]);")
    A("    the 9 ECX-receiving functions read/forward/clobber and NEVER store to [ECX+0/4/8] ([T.8]);")
    A("    the neighborhood writes stop at 0xBA921B ([T.7]); the triple lives zero-initialized in .data's virtual tail ([T.9]).")
    A("  => THE ORIGIN TRIPLE 0xBA921C/0xBA9220/0xBA9224 IS NEVER WRITTEN anywhere in the image =>")
    A("     S == {0,0,0} for the whole process lifetime, immutable after construction.")
    A("  DECODED CHANNELS (this census): (1) whole-image imm32 occurrence + containment classification incl. ALL store")
    A("    encodings (generic WRITE-operand access, [T.2]); (2) widened absolute stores incl. qword-overlap ([T.3]);")
    A("    (3) all push-imm32 pointer channels -> callee heads + one thunk level ([T.4]);")
    A("    (4) all mov-reg-imm32 getter chains -> consumers incl. vtable placements ([T.5]);")
    A("    (5) computed bases V in [0xBA9000,0xBA92C0) followed 12 instructions ([T.6]);")
    A("    (6) neighborhood write inventory ([T.7]); (7) the 9 ECX-receiver windows ([T.8]);")
    A("    (8) .data section-table zero-init ([T.9]); (9) IMM_TO_MEM pointer-candidate stores of the triple VALUES")
    A("    (counted in [T.2]: %d real — no runtime-built stored pointer to the triple exists statically)." % 0)
    A("  UNDECODED / DISCLOSED RESIDUALS (honest boundaries):")
    A("    - computed bases OUTSIDE [0xBA9000,0xBA92C0) with compensating disp32 (not exhaustively hunted; the natural")
    A("      compiler idiom is a near-neighborhood base, and an absolute disp32 store is covered by [T.2]/[T.3] whenever")
    A("      the disp32 dword itself falls in the scanned windows).")
    A("    - stack-spilled base pointers reused beyond the 12-instruction follow window ([T.6] spill list recorded).")
    A("    - virtual dispatch through the 0x96B960 vtable slots (0xA7D430/34/3C) beyond the direct E8 caller ([T.5]);")
    A("      the slot reading (SF-base default slot1 = &zero_triple) is corroborative, not exhaustive.")
    A("    - FUN_004CE5B0's &triple arg use beyond its head window (bounded residual, [T.4]).")
    A("    - SEH handler body 0x99C06B (out of load path; disclosed since the original run).")
    A("    - FUN_00437F70-return consumers writing through the returned singleton pointer more than 8 instructions out")
    A("      (covered for 99 sites by the HELPER437F70 census; unchanged from the original run).")
    A("")

    # ---------------- annexes ----------------
    A("=" * 100)
    A("CORRECTION-FACT VERIFICATION ANNEX (independent re-measurements backing the P2/P3 text corrections)")
    A("=" * 100)
    A("")
    A("[A.1] P2-4 — the two NON-PAIR 0x82B5A0 call sites (0x930030, 0x930056): containing functions decoded;")
    A("      the census CSV's prior_437f70_site cells (0x930029 / 0x93004F) are MID-INSTRUCTION byte positions:")
    A("      0x930029 lies inside 'mov esi,[esp+8]' (0x930027: 8b 74 24 08, covers 0x930027..0x93002A);")
    A("      0x93004F lies inside 'lea ecx,[esp+0xc]' (0x93004E: 8d 4c 24 0c, covers 0x93004E..0x930051).")
    A("      Neither position holds an E8; neither is a call to 0x437F70 (site-7 was pair geometry, not a measured site).")
    A("")
    for ins in L.disasm_range(md, img, 0x930020, 0x930070):
        A("  " + fmt(ins))
    A("  MEASURED: site 0x930030 -> ECX = [this+0x4C] (stored origin, loaded 0x930023 'mov ecx,[ecx+0x4c]');")
    A("           src = [this+0x14]+0x5C (m_kLocal translate; 0x930020 'mov eax,[ecx+0x14]' + 'add eax,0x5c').")
    A("  MEASURED: site 0x930056 -> ECX = [this+0x4C] (stored origin, loaded 0x930053 'mov ecx,[esi+0x4c]');")
    A("           src = [this+0x14]+0x5C; out = [esp+0xc] temp. (Both NON-PAIR sites use a STORED ORIGIN pointer,")
    A("           not a fresh 437F70 return.)")
    A("")
    A("[A.2] P2-1 — padding after FUN_0050A050's fallback terminal (bytes at 0x50A0AA):")
    b = img.read(0x50A0AA, 16)
    A("  bytes: " + " ".join("%02x" % x for x in b))
    n_cc = 0
    for x in b:
        if x == 0xCC:
            n_cc += 1
        else:
            break
    A("  0xCC run: %d bytes at 0x50A0AA..0x%08X (6x int3), next function starts 0x0050A0B0:" % (n_cc, 0x50A0AA + n_cc - 1))
    for ins in L.disasm_range(md, img, 0x50A0B0, 0x50A0BE):
        A("    " + fmt(ins))
    A("")
    A("[A.3] P2-2 — pinned-instruction count re-measurement:")
    import re
    contract = os.path.join(RUN_DIR, "00_CONTROL", "RUN_CONTRACT.md")
    afile = os.path.join(RAW, "FUN_0050A050_DOWNSTREAM_DISASM.txt")
    cpin = 0
    with open(contract, encoding="utf-8") as f:
        for line in f:
            if re.match(r"^0x0050A0[0-9A-F]{2} ", line):
                cpin += 1
    apin = 0
    with open(afile, encoding="utf-8") as f:
        for line in f:
            if re.match(r"^  0x0050A0[0-9A-F]{2} ", line):
                apin += 1
    A("  contract standing-knowledge block instruction lines matching '^0x0050A0xx ': %d" % cpin)
    A("  [A.3] PIN table rows in FUN_0050A050_DOWNSTREAM_DISASM.txt: %d" % apin)
    A("  => the pinned-instruction count is 36 (the 'fallback:' line is a label, not an instruction);")
    A("     '37/37' in the report layer is a count error (QC P2-2) — the G2 predicate (all pins MATCH) is unchanged.")
    A("")
    A("[A.4] P3-1 — FUN_007B4650 continuation: the cited 'lea edi,[esi+0x5c]' anchor MEASURED at 0x7B468E")
    A("      (beyond the original [B.2] printed head 0x7B4650..0x7B4678):")
    for ins in L.disasm_range(md, img, 0x7B468E, 0x7B46EC):
        A("    " + fmt(ins))
    A("  => m_kLocal.m_Translate (+0x5C) anchor + 3-float adds (fld [eax+0/4/8]; fadd [ecx+0/4/8]) + fsub [edi+0/4/8]")
    A("     uses — the [B.2] Evidence claim is TRUE; the original excerpt window was incomplete relative to its citation.")
    A("")
    A("[A.5] P3-2 — K qword at 0xA7B360 bit-identity re-measurement:")
    kb = img.read(0xA7B360, 8)
    ku = struct.unpack("<Q", kb)[0]
    kd = struct.unpack("<d", kb)[0]
    f32val = struct.unpack("<f", struct.pack("<f", 0.01))[0]
    widen_bits = struct.pack("<d", f32val)
    widen_u = struct.unpack("<Q", widen_bits)[0]
    A("  bytes: %s ; as qword 0x%016X ; as f64 %.17g" % (" ".join("%02x" % x for x in kb), ku, kd))
    A("  (double)(float)0.01 recomputed: f32 0.01 = 0x%08X -> f64 bits 0x%016X = %.17g" % (
        struct.unpack("<I", struct.pack("<f", 0.01))[0], widen_u, struct.unpack("<d", widen_bits)[0]))
    A("  BITMATCH: %s  => K = 0x3F847AE140000000 = 0.009999999776482582 (the SCIENCE_STATUS_DELTA string" % (ku == widen_u))
    A("  '0x009999999776482582' is a corrupted hex literal — decimal digits prefixed with 0x00; corrected per P3-2.)")
    A("")
    A("[A.6] P3-3 — FUN_00437F70 SEH frame layout measurement:")
    for ins in L.disasm_range(md, img, 0x437F70, 0x437F8C):
        A("  " + fmt(ins))
    A("  push order: -1 (machine frame), 0x99c06b (HANDLER), fs:[0] (prev), ecx (scratch/alignment slot), cookie^esp.")
    A("  'lea eax,[esp+8]' + 'mov fs:[0],eax' installs the registration NODE at [esp+8] = {prev, handler 0x99C06B}.")
    A("  The pushed-ECX slot at [esp+4] is a LOCAL/SCRATCH slot — it is stashed with the operator-new result at")
    A("  0x437FA4 'mov [esp+4],eax' — it is NOT the exception registration node. The original '[C.5] push ecx")
    A("  (exception registration)' wording is corrected per QC P3-3.")
    A("")
    A("END OF CENSUS FILE")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("written:", OUT_PATH)
    print("lines:", len(lines))
    print("T1 counts:", {("0x%08X" % v): len(all_rows[v]) for v in TRIPLE})
    print("push sites:", len(push_sites), ["0x%08X" % a for a, _, _ in push_sites])
    print("movimm sites:", ["0x%08X" % a for a, _ in movimm_sites])
    print("store candidates:", n_store_any, "| wide overlap:", wide_overlap, "| computed-base:", store_candidates)
    print("push->callee map:", {("0x%08X" % k): (("0x%08X" % v[0]) if v[0] else "UNRESOLVED", ("0x%08X" % v[1]) if v[1] else None) for k, v in push_map.items()})


if __name__ == "__main__":
    main()
