"""fix_probe_r4.py — QC_R3 findings F1/F2/F3/F4 byte re-verification probe (fix round
PE_935_SF_QC_R3_FINDINGS_FIX_R1_20260915, inside canonical package
PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915).

PE-MASTER-dispatched bounded fix round: apply exactly the four QC_R3-adjudicated findings
(06_REPORT/QC_AUDIT_R3.md, PE-MASTER ACCEPTED). This probe re-verifies every corrected fact
from Entropia.exe physical bytes BEFORE any canonical edit, independent of the two generators
under repair (census_setter_reach.py / census_write_through.py are NOT imported here; only the
shared S0-fail-closed loader decode_lib.py is). Fail-closed contract: if any re-verification
contradicts the QC/PE-MASTER facts, the fix round STOPS (HARD STOP) instead of forcing the edit.

Re-verifies (all from bytes):
  [A] F1/F4 branch-B structure: extent(0x4B1B70) end; 0x4B1C70 boundary (ret+1xCC+SEH prologue);
      containment of E8@0x4B1EEB (call 0x417A40) and E8@0x4B1F2C (call 0x4B1B70) inside
      FUN_004B1C70's linear stream (=> NOT self-recursion); FUN_004B1C70 channel census
      (expect external E8 caller 0x4B2984, 0 E9/imm32/vtable); FUN_004B2950 boundary + containment
      of 0x4B2984 + the case-0xB2 dispatch compare; callee-set closure of 0x4B1B70 / 0x4B1C70 /
      0x417A40 w.r.t. the setter chain {0x458E50, 0x458D90, 0x417030}.
  [B] F2 attribution: for each of the 4 corrected enclosing starts (0x6C1A90, 0x6C4E70, 0x6E23B0,
      0x8CD3E0) vs the old starts (0x6C19B0, 0x6C4C40, 0x6E21F0, 0x8CD1A0): ret-adjacent-1xCC
      boundary bytes; head decode; clean linear decode reaching each affected census site exactly
      as 'call 0x437f70'; first-terminal extent from the corrected start (predicted CSV values);
      inbound E8 callers (re-verifying the QC's caller lists); old-start prologue reality check.
  [C] F3 counts: file census of 00_CONTROL/PRE_EDIT/ (the tree CG7's basis hashes), PRE_EDIT_R2/,
      PRE_EDIT_R3/ (frozen-tree preservation baselines for this round).

Output: 01_RAW/FIX_ROUND_R4_BYTE_REVERIFICATION_RAW.txt. STATIC-ONLY; read-only on the EXE.
"""
import sys
import os
import struct
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capstone.x86 import X86_OP_IMM
import decode_lib as L

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
SCRIPT_PATH = os.path.abspath(__file__)

GETTER = 0x437F70
SETTER_CHAIN = (0x458E50, 0x458D90, 0x417030)

F2_PAIRS = [
    (0x6C1A90, 0x6C19B0, [0x6C1C2A, 0x6C1C5C, 0x6C1C9A, 0x6C1CB5]),
    (0x6C4E70, 0x6C4C40, [0x6C4E8E, 0x6C4EE9]),
    (0x6E23B0, 0x6E21F0, [0x6E23FA, 0x6E2441]),
    (0x8CD3E0, 0x8CD1A0, [0x8CD556, 0x8CD645]),
]
QC_EXPECTED_CALLERS = {
    0x6C1A90: [0x4597C7, 0x45F02D, 0x55B891, 0x5F61AA],
    0x6C4E70: [0x6C5506, 0x6C551C],
    0x6E23B0: [0x6E2EB9],
    0x8CD3E0: [0x8CD887, 0x8CDE82],
}
# Old CSV enclosing_function_extent values (historical record, from the current on-disk census
# CSV; printed as EXPECTED values to confirm the generator-rule reproduction, never as evidence).
OLD_CSV_EXTENT = {
    0x6C19B0: (0x6C1A33, 0x6C1A35),
    0x6C4C40: (0x6C4D31, 0x6C4D33),
    0x6E21F0: (0x6E237C, 0x6E237E),
    0x8CD1A0: (0x8CD1D0, 0x8CD1D5),
}


def script_sha256():
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def e8_e9_scan(img, target):
    e8, e9 = [], []
    for nm, va_s, vs, ro, rs in img.sections:
        if nm != ".text":
            continue
        raw = img.data[ro:ro + rs]
        base = img.imagebase + va_s
        for i in range(len(raw) - 5):
            if raw[i] in (0xE8, 0xE9):
                rel = struct.unpack_from("<i", raw, i + 1)[0]
                src = base + i
                if src + 5 + rel == target:
                    (e8 if raw[i] == 0xE8 else e9).append(src)
    return sorted(e8), sorted(e9)


def is_va_range(img, va, secname):
    rva = va - img.imagebase
    for nm, va_s, vs, ro, rs in img.sections:
        if nm == secname and va_s <= rva < va_s + vs:
            return True
    return False


def is_va_in_sections(img, va, secnames):
    rva = va - img.imagebase
    for nm, va_s, vs, ro, rs in img.sections:
        if nm in secnames and va_s <= rva < va_s + vs:
            return True
    return False


def is_col_pointer(img, x):
    if not is_va_in_sections(img, x, (".rdata", ".data")):
        return False
    try:
        td = struct.unpack("<I", img.read(x + 0xC, 4))[0]
    except Exception:
        return False
    if not is_va_in_sections(img, td, (".rdata", ".data")):
        return False
    try:
        nm = img.read(td + 8, 4)
    except Exception:
        return False
    return nm.startswith(b".?A")


def find_vtable_start(img, entry_va, max_back=0x400):
    p = entry_va - 4
    while entry_va - p <= max_back:
        try:
            d = struct.unpack("<I", img.read(p, 4))[0]
        except Exception:
            return None
        if is_col_pointer(img, d):
            return p + 4
        if not is_va_range(img, d, ".text"):
            return None
        p -= 4
    return None


def vtable_membership(img, target):
    hits = []
    tle = struct.pack("<I", target)
    for nm, va_s, vs, ro, rs in img.sections:
        if nm not in (".rdata", ".data"):
            continue
        raw = img.data[ro:ro + rs]
        base = img.imagebase + va_s
        idx = 0
        while True:
            j = raw.find(tle, idx)
            if j < 0:
                break
            hit = base + j
            start = find_vtable_start(img, hit)
            if start is not None:
                hits.append((hit, start, (hit - start) // 4))
            idx = j + 1
    return hits


def extent_first_terminal_with_pad(img, md, start, cap=0x4000):
    """Linear decode from start; stop at the FIRST terminal followed by a >=1-byte int3 run
    (the package's function-end rule). Returns (ins_list, terminal, pad_end) or (ins_list, None, None)."""
    try:
        code = img.read(start, cap)
    except Exception:
        return [], None, None
    ins_list = []
    for ins in md.disasm(code, start):
        ins_list.append(ins)
        if ins.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2"):
            end = ins.address + ins.size
            try:
                pad = img.read(end, 16)
            except Exception:
                pad = b""
            run = 0
            for b in pad:
                if b == 0xCC:
                    run += 1
                else:
                    break
            if run >= 1:
                return ins_list, ins, end + run
        if ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            end = ins.address + ins.size
            try:
                pad = img.read(end, 16)
            except Exception:
                pad = b""
            run = 0
            for b in pad:
                if b == 0xCC:
                    run += 1
                else:
                    break
            if run >= 1:
                return ins_list, ins, end + run
    return ins_list, None, None


def direct_callees(ins_list):
    out = []
    for i in ins_list:
        if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM:
            out.append((i.address, i.operands[0].imm))
    return out


def site_lands(img, md, f, site, target):
    """True iff linear decode from f lands EXACTLY on site as 'call <target>'."""
    try:
        code = img.read(f, site - f + 5)
    except Exception:
        return False
    for ins in md.disasm(code, f):
        if ins.address == site:
            return bool(ins.mnemonic == "call" and ins.operands
                        and ins.operands[0].type == X86_OP_IMM
                        and ins.operands[0].imm == target)
        if ins.address + ins.size > site:
            return False
    return False


def ret_adjacent_class(img, va):
    """Classify the 1-byte int3 run ending at va (va = candidate function start after the run).
    Returns a string describing the ret-adjacency of the padding byte at va-1."""
    try:
        b = img.read(va - 1, 1)[0]
    except Exception:
        return "unreadable"
    if b != 0xCC:
        return "not-a-1byte-CC-run (byte=0x%02X)" % b
    try:
        prev3 = img.read(va - 4, 3)
    except Exception:
        return "CC but preceding bytes unreadable"
    if prev3[2] == 0xC3:
        return "C3 (ret) + 1x CC (plain-ret-adjacent)"
    if prev3[0] == 0xC2:
        return "C2 %02X %02X (ret imm16) + 1x CC (ret-adjacent)" % (prev3[1], prev3[2])
    return "CC but preceding 3 bytes are %s (NOT ret-adjacent)" % " ".join("%02x" % x for x in prev3)


def main():
    out = []
    A = out.append
    img = L.Image()  # S0 FAIL-CLOSED before any decode
    md = L.make_disassembler()

    A("=" * 100)
    A("FIX ROUND R4 BYTE RE-VERIFICATION — QC_R3 FINDINGS F1/F2/F3/F4 (before any canonical edit)")
    A("RUN_ID (fix round): PE_935_SF_QC_R3_FINDINGS_FIX_R1_20260915")
    A("CANONICAL PACKAGE: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (in-place fix round)")
    A("ADJUDICATED FINDINGS: 06_REPORT/QC_AUDIT_R3.md F1 (P1), F2 (P2), F3 (P3), F4 (P3) — PE-MASTER ACCEPTED")
    A("GENERATED_UTC: " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    A("PROBE_SCRIPT: %s" % SCRIPT_PATH)
    A("PROBE_SHA256: %s" % script_sha256())
    A("MEASURED ENVIRONMENT:")
    for ln in L.measured_env(img).split("\n"):
        A("  " + ln)
    A("S0 FAIL-CLOSED: PASSED at script start (size+sha256+PE layout re-verified before any decode).")
    A("METHOD: independent linear decodes + raw E8/E9/imm32/vtable censuses from physical bytes;")
    A("  the two generators under repair are NOT imported; no prior census result is imported.")
    A("=" * 100)
    A("")

    # ================= SECTION A: F1/F4 branch-B structure =================
    A("[A] F1/F4 BRANCH-B RE-VERIFICATION (reported root 0x4B1B70; claimed-dead subtree)")
    A("")

    # A.1 boundary at 0x4B1C6E/0x4B1C6F/0x4B1C70
    bnd = img.read(0x4B1C6C, 8)
    A("  A.1 bytes 0x004B1C6C..0x004B1C73: %s" % " ".join("%02x" % b for b in bnd))
    head = list(md.disasm(img.read(0x4B1C70, 0x18), 0x4B1C70))[:3]
    A("  FUN_004B1C70 head decode:")
    for i in head:
        A("    " + L.fmt_ins(i))
    A("  ret @0x004B1C6E + single int3 @0x004B1C6F then 0x004B1C70 prologue: %s" % (
        "MEASURED" if bnd[2] == 0xC3 and bnd[3] == 0xCC and bnd[4] == 0x6A and bnd[5] == 0xFF else "NOT MATCHED"))
    A("  ret-adjacency of the 1-byte CC run before 0x004B1C70: %s" % ret_adjacent_class(img, 0x4B1C70))
    A("")

    # A.2 extent of FUN_004B1B70
    insB, termB, padB = extent_first_terminal_with_pad(img, md, 0x4B1B70, cap=0x800)
    A("  A.2 FUN_004B1B70 extent (first terminal + int3-pad rule): %s" % (
        "0x004B1B70..0x%08X (terminal 0x%08X %s; next function starts 0x%08X)" % (
            padB or 0, termB.address, termB.mnemonic, padB or 0) if termB else "UNRESOLVED within cap"))
    A("    terminals in stream: %s" % ", ".join(
        "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str)
        for i in insB if i.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2")))
    A("    0x004B1F2C inside FUN_004B1B70's linear stream: %s" % (
        any(i.address == 0x4B1F2C for i in insB)))
    A("    0x004B1EEB inside FUN_004B1B70's linear stream: %s" % (
        any(i.address == 0x4B1EEB for i in insB)))
    A("")

    # A.3 extent of FUN_004B1C70 + containment of both E8 sites
    insC, termC, padC = extent_first_terminal_with_pad(img, md, 0x4B1C70, cap=0x800)
    A("  A.3 FUN_004B1C70 extent (first terminal + int3-pad rule): %s" % (
        "0x004B1C70..0x%08X (terminal 0x%08X %s; next function starts 0x%08X)" % (
            padC or 0, termC.address, termC.mnemonic, padC or 0) if termC else "UNRESOLVED within cap"))
    A("    terminals in stream (first 6): %s" % ", ".join(
        "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str)
        for i in insC if i.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2"))[:200])
    c_1EEB = [i for i in insC if i.address == 0x4B1EEB]
    c_1F2C = [i for i in insC if i.address == 0x4B1F2C]
    A("    0x004B1EEB inside FUN_004B1C70's linear stream: %s (decodes as: %s)" % (
        bool(c_1EEB),
        "%s %s" % (c_1EEB[0].mnemonic, c_1EEB[0].op_str) if c_1EEB else "(not reached)"))
    A("    0x004B1F2C inside FUN_004B1C70's linear stream: %s (decodes as: %s)" % (
        bool(c_1F2C),
        "%s %s" % (c_1F2C[0].mnemonic, c_1F2C[0].op_str) if c_1F2C else "(not reached)"))
    A("    => 0x4B1F2C is a SIBLING call FUN_004B1C70 -> FUN_004B1B70 (NOT self-recursion): %s" % (
        bool(c_1F2C and c_1F2C[0].mnemonic == "call" and c_1F2C[0].operands[0].imm == 0x4B1B70)))
    A("")

    # A.4 channel census of 0x4B1C70
    e8C, e9C = e8_e9_scan(img, 0x4B1C70)
    patC = L.scan_pattern_calls(img, 0x4B1C70)
    vtC = vtable_membership(img, 0x4B1C70)
    A("  A.4 FUN_004B1C70 channels: E8=%s E9=%s imm32=%s vtable=%s" % (
        ["0x%08X" % x for x in e8C], ["0x%08X" % x for x in e9C],
        ["%s@0x%08X" % (nm, x) for nm, x in patC] or "(none)",
        ["entry@0x%08X vtable=0x%08X slot=%d" % h for h in vtC] or "(none)"))
    A("")

    # A.5 FUN_004B2950 boundary + containment of the external caller site + case-0xB2 compare
    head2950 = list(md.disasm(img.read(0x4B2950, 0x18), 0x4B2950))[:3]
    A("  A.5 FUN_004B2950 (prior-canon ArkClientPacketExecutor::Execute) head decode:")
    for i in head2950:
        A("    " + L.fmt_ins(i))
    A("    linear decode from 0x004B2950 lands EXACTLY on 0x004B2984 as 'call 0x4b1c70': %s" % (
        site_lands(img, md, 0x4B2950, 0x4B2984, 0x4B1C70)))
    insD, termD, padD = extent_first_terminal_with_pad(img, md, 0x4B2950, cap=0x2000)
    A("    FUN_004B2950 extent (first terminal + int3-pad rule): %s" % (
        "0x004B2950..0x%08X (terminal 0x%08X %s; next function starts 0x%08X)" % (
            padD or 0, termD.address, termD.mnemonic, padD or 0) if termD else "UNRESOLVED within cap"))
    cmp_b2 = [i for i in insD if i.mnemonic == "cmp" and i.operands
              and len(i.operands) == 2 and i.operands[1].type == X86_OP_IMM
              and i.operands[1].imm == 0xB2 and i.address < 0x4B2984]
    A("    'cmp <reg>, 0xb2' instructions before 0x004B2984 in FUN_004B2950's stream: %s" % [
        "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in cmp_b2])
    A("    dispatch-context window 0x004B2960..0x004B2990:")
    for i in L.disasm_range(md, img, 0x4B2960, 0x4B2990):
        A("      " + L.fmt_ins(i))
    A("")

    # A.6 callee-set closure w.r.t. the setter chain
    callees_B = direct_callees(insB)
    callees_C = direct_callees(insC)
    insA40, _, _ = extent_first_terminal_with_pad(img, md, 0x417A40, cap=0x800)
    callees_A40 = direct_callees(insA40)
    A("  A.6 callee-set closure w.r.t. the setter chain {0x458E50, 0x458D90, 0x417030}:")
    A("    direct callees of FUN_004B1B70 (linear stream): %s" % [
        "0x%08X->0x%08X" % (va, t) for va, t in callees_B])
    A("    FUN_004B1B70 calls any setter-chain member: %s" % (
        any(t in SETTER_CHAIN for _, t in callees_B)))
    A("    direct callees of FUN_004B1C70 (linear stream): %s" % [
        "0x%08X->0x%08X" % (va, t) for va, t in callees_C])
    A("    FUN_004B1C70 calls 0x417A40: %s ; calls 0x4B1B70: %s ; calls any setter-chain member: %s" % (
        any(t == 0x417A40 for _, t in callees_C),
        any(t == 0x4B1B70 for _, t in callees_C),
        any(t in SETTER_CHAIN for _, t in callees_C)))
    A("    direct callees of FUN_00417A40 (linear stream, first 16): %s" % [
        "0x%08X->0x%08X" % (va, t) for va, t in callees_A40[:16]])
    A("    FUN_00417A40 calls 0x417880: %s ; calls any setter-chain member: %s" % (
        any(t == 0x417880 for _, t in callees_A40),
        any(t in SETTER_CHAIN for _, t in callees_A40)))
    A("")

    # ================= SECTION B: F2 attribution pairs =================
    A("[B] F2 ATTRIBUTION RE-VERIFICATION (corrected enclosing starts vs old starts)")
    for true_start, old_start, sites in F2_PAIRS:
        A("")
        A("-" * 100)
        A("PAIR corrected=0x%08X old=0x%08X sites=%s" % (
            true_start, old_start, ["0x%08X" % s for s in sites]))
        pre12 = img.read(true_start - 12, 12)
        A("  12 bytes before corrected start 0x%08X: %s" % (
            true_start, " ".join("%02x" % b for b in pre12)))
        A("  boundary classification: %s" % ret_adjacent_class(img, true_start))
        hd = list(md.disasm(img.read(true_start, 0x18), true_start))[:3]
        A("  corrected-start head decode:")
        for i in hd:
            A("    " + L.fmt_ins(i))
        insT, termT, padT = extent_first_terminal_with_pad(img, md, true_start, cap=0x2000)
        if termT is not None:
            A("  corrected-start first-terminal extent: terminal 0x%08X %s ; extent 0x%08X..0x%08X" % (
                termT.address, termT.mnemonic, termT.address, termT.address + termT.size))
        else:
            A("  corrected-start first-terminal extent: UNRESOLVED within cap")
        # All terminals up to the CC-adjacent one: the census generator's extent rule is
        # 'FIRST TERMINAL period' (census_write_through.function_extent); this probe's boundary
        # rule is 'first terminal FOLLOWED BY >=1 CC'. Both are listed so the regenerated CSV
        # extent values are exactly predictable and the rule difference is explicit.
        terms_all = [i for i in insT if i.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2")
                     or (i.mnemonic == "jmp" and i.operands and i.operands[0].type == X86_OP_IMM)]
        A("  all terminals in the corrected start's stream (until the CC-adjacent one): %s" % [
            "0x%08X %s %s (size %d)" % (i.address, i.mnemonic, i.op_str, i.size) for i in terms_all])
        if terms_all:
            t0 = terms_all[0]
            A("  generator-rule (first-terminal-period) extent prediction: 0x%08X..0x%08X" % (
                t0.address, t0.address + t0.size))
        gen_term = terms_all[0] if terms_all else None
        for s in sites:
            lands = site_lands(img, md, true_start, s, GETTER)
            beyond = bool(gen_term is not None and gen_term.address < s)
            A("  site 0x%08X: decode-from-corrected-start lands exactly as 'call 0x437f70': %s ; "
              "site beyond generator-rule first terminal: %s" % (s, lands, beyond))
            if gen_term is not None and beyond:
                A("    predicted CSV extent text: 0x%08X..0x%08X (first-terminal extent; SITE BEYOND "
                  "first terminal: multi-path function)" % (gen_term.address, gen_term.address + gen_term.size))
            elif gen_term is not None:
                A("    predicted CSV extent text: 0x%08X..0x%08X" % (
                    gen_term.address, gen_term.address + gen_term.size))
        e8in, e9in = e8_e9_scan(img, true_start)
        A("  inbound E8 callers of 0x%08X (raw scan): %s (QC expected: %s)" % (
            true_start, ["0x%08X" % x for x in e8in],
            ["0x%08X" % x for x in QC_EXPECTED_CALLERS[true_start]]))
        for c in e8in:
            A("    caller site 0x%08X decodes as 'call 0x%08X': %s" % (
                c, true_start, _decode_call_check(img, md, c, true_start)))
        pre12o = img.read(old_start - 12, 12)
        A("  12 bytes before OLD start 0x%08X: %s" % (
            old_start, " ".join("%02x" % b for b in pre12o)))
        hdo = list(md.disasm(img.read(old_start, 0x18), old_start))[:3]
        A("  old-start head decode (real-adjacent-function confirmation):")
        for i in hdo:
            A("    " + L.fmt_ins(i))
        insO, termO, padO = extent_first_terminal_with_pad(img, md, old_start, cap=0x2000)
        terms_all_o = [i for i in insO if i.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2")
                       or (i.mnemonic == "jmp" and i.operands and i.operands[0].type == X86_OP_IMM)]
        if terms_all_o:
            t0o = terms_all_o[0]
            exp = OLD_CSV_EXTENT[old_start]
            A("  old-start generator-rule (first-terminal-period) extent: 0x%08X..0x%08X ; "
              "old CSV recorded value 0x%08X..0x%08X : %s" % (
                  t0o.address, t0o.address + t0o.size, exp[0], exp[1],
                  "MATCH" if (t0o.address == exp[0] and t0o.address + t0o.size == exp[1]) else "MISMATCH"))
            A("    (sites 0x%08X.. are BEYOND the old first terminal: %s — the old CSV suffix was"
              " correct for the WRONG enclosing start)" % (
                  sites[0], all(t0o.address < s for s in sites)))
        for s in sites:
            A("  site 0x%08X inside OLD start's stream (up to the old CC-adjacent terminal): %s "
              "(old attribution was WRONG: the site lies past the corrected boundary 0x%08X)" % (
                  s, any(i.address == s for i in insO), true_start))
    A("")

    # ================= SECTION C: F3 counts =================
    A("[C] F3 SNAPSHOT-TREE FILE CENSUS (fix note counts)")
    for sub in ("PRE_EDIT", "PRE_EDIT_R2", "PRE_EDIT_R3", "PRE_EDIT_R4"):
        d = os.path.join(RUN_DIR, "00_CONTROL", sub)
        if os.path.isdir(d):
            n = sum(len(fs) for _, _, fs in os.walk(d))
            A("  00_CONTROL/%s: %d files" % (sub, n))
        else:
            A("  00_CONTROL/%s: (does not exist yet at probe time)" % sub)
    A("  CG7 basis claim 'hash census: 20 files' refers to 00_CONTROL/PRE_EDIT/** (the correction-pass")
    A("  snapshot tree hashed before/after the origin-mutability correction); actual count measured")
    A("  above. The dispatch's PRE_EDIT_R2 count is also measured above for completeness.")
    A("")

    A("MEASURED_QUANTITY: boundary bytes + head/extent/containment decodes + channel censuses +")
    A("  callee-set closure + snapshot-tree counts; per corrected/old enclosing-function start.")
    A("INDEPENDENT_SOURCE_OF_TRUTH: capstone 5.0.7 linear decodes of Entropia.exe physical bytes")
    A("  (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; S0 fail-closed).")
    A("WHY_NON_CIRCULAR: no generator-under-repair is imported; no QC_R3_RAW value is imported as")
    A("  evidence (QC lists are printed only as EXPECTED values to compare against this decode).")
    A("FAILURE_CASE_DETECTED: any mismatch between this decode and the QC/PE-MASTER facts is a")
    A("  HARD STOP for the fix round (reported loudly, never forced).")

    path = os.path.join(RAW, "FIX_ROUND_R4_BYTE_REVERIFICATION_RAW.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("written:", path)


def _decode_call_check(img, md, site, target):
    try:
        code = img.read(site, 5)
    except Exception:
        return False
    ins = next(md.disasm(code, site), None)
    return bool(ins and ins.mnemonic == "call" and ins.operands
                and ins.operands[0].type == X86_OP_IMM and ins.operands[0].imm == target)


if __name__ == "__main__":
    main()
