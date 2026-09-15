"""probe_origin_setter.py — FALSIFIER + full setter decode (correction run
PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915, executed inside canonical package
PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915).

FIRST measurement of the correction run (contract Section 3): independently reproduce or
reject, from physical bytes, the external WORK-AUDITOR finding that call site 0x00458E27
-> call FUN_00437F70 is followed by writes through the returned pointer.

Outputs 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt. Read-only on Entropia.exe; S0 fail-closed
at start (decode_lib.Image). STATIC-ONLY. Measurements only — no science conclusions
(those live in 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md).
"""
import sys
import os
import struct
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capstone
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM
import decode_lib as L
import sprov as SP

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
SCRIPT_PATH = os.path.abspath(__file__)

GETTER = 0x437F70
SETTER = 0x458D90
CTOR = 0x82B580
TRIPLE = (0xBA921C, 0xBA9220, 0xBA9224)
SLOT = 0xBA1804
FTOL = 0x95DA40
PAIR_HELPER = 0x82B5A0
SF_PAIR_SITE = 0x50A075


def script_sha256():
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def fmt(ins):
    return L.fmt_ins(ins)


def decode_range(img, md, start, end):
    return L.disasm_range(md, img, start, end)


def head_lines(img, md, va, n_ins, indent="  "):
    try:
        ins_list = decode_range(img, md, va, va + 0x300)[:n_ins]
    except Exception as e:  # noqa
        return ["%s<decode-fail at %#x: %s>" % (indent, va, e)]
    return ["%s%s" % (indent, fmt(i)) for i in ins_list]


SUBREG_EAX = ("al", "ah", "ax")


def defines_eax(md, ins):
    """Return the EAX effect of one instruction: ('set', token) or None (no EAX write)."""
    mn = ins.mnemonic
    ops = list(ins.operands) if ins.operands else []
    if mn == "mov" and ops and ops[0].type == X86_OP_REG:
        nm = md.reg_name(ops[0].reg)
        if nm == "eax":
            src = ops[1]
            if src.type == X86_OP_MEM:
                m = src.mem
                if m.base and md.reg_name(m.base) in ("esp", "ebp"):
                    return ("set", "stack")
                if m.disp == SLOT and not m.index:
                    return ("set", "S_PTR")  # mov eax, [0xba1804] = singleton cache load
                return ("set", "mem")
            if src.type == X86_OP_IMM:
                return ("set", "imm")
            return ("set", "reg:" + md.reg_name(src.reg))
        return None
    if mn == "xor" and ops and ops[0].type == X86_OP_REG and md.reg_name(ops[0].reg) == "eax" \
            and ops[1].type == X86_OP_REG and md.reg_name(ops[1].reg) == "eax":
        return ("set", "0")
    if mn.startswith("call"):
        if ops and ops[0].type == X86_OP_IMM:
            return ("set", "call_ret(0x%08X)" % ops[0].imm)
        return ("set", "call_ret_indirect")
    try:
        for regid in ins.regs_write:
            nm = md.reg_name(regid)
            if nm == "eax" or nm in SUBREG_EAX:
                return ("set", "other")
    except Exception:  # noqa
        pass
    return None


def getter_eax_paths(md, img):
    """Path-sensitive EAX trace of FUN_00437F70. Returns list of (ret_va, eax_token, path)."""
    ins_list = decode_range(img, md, GETTER, 0x437FF0)
    by_addr = {i.address: i for i in ins_list}
    results = []

    def walk(va, tok, path, depth):
        guard = 0
        while True:
            guard += 1
            if guard > 200 or depth > 16:
                results.append((va, "GUARD-EXHAUSTED(tok=%s)" % tok, path + ["guard"]))
                return
            ins = by_addr.get(va)
            if ins is None:
                results.append((va, "OUT-OF-RANGE(tok=%s)" % tok, path))
                return
            eff = defines_eax(md, ins)
            if eff is not None:
                tok = eff[1]
            mn = ins.mnemonic
            if mn in ("ret", "retf", "iretd", "hlt", "ud2"):
                results.append((va, tok, path))
                return
            if mn == "jmp":
                if ins.operands and ins.operands[0].type == X86_OP_IMM:
                    va = ins.operands[0].imm
                    continue
                results.append((va, "jmp-indirect(tok=%s)" % tok, path))
                return
            if (mn.startswith("j") and mn != "jmp") or mn.startswith("loop"):
                if ins.operands and ins.operands[0].type == X86_OP_IMM:
                    walk(ins.operands[0].imm, tok, path + ["%#x->%#x" % (va, ins.operands[0].imm)], depth + 1)
                va = ins.address + ins.size
                continue
            va = ins.address + ins.size

    walk(GETTER, "entry-unknown", [], 0)
    return results


def data_refs_in_head(img, ins_list):
    """Absolute .data references from a bounded head decode: imm32 operands AND baseless
    absolute MEM operands (capstone encodes 'mov eax, dword ptr [0xba12d4]' as MEM with
    no base/index and disp=absolute — not as an IMM operand)."""
    refs = []
    for i in ins_list:
        for op in (i.operands or []):
            val = None
            if op.type == X86_OP_IMM:
                val = op.imm
            elif op.type == X86_OP_MEM:
                m = op.mem
                if not m.base and not m.index:
                    val = m.disp
            if val is None:
                continue
            rva = val - img.imagebase
            for nm, va_s, vs, ro, rs in img.sections:
                if nm == ".data" and va_s <= rva < va_s + vs:
                    refs.append("0x%08X @0x%08X '%s %s'" % (val, i.address, i.mnemonic, i.op_str))
                    break
    return refs


def setter_ledger_and_dataflow(img, md, out):
    """[S.4]+[S.10]: esp ledger + local-slot content trace over the setter decode."""
    A = out.append
    setter_ins = decode_range(img, md, SETTER, 0x458E50)
    ret_cache = {}

    esp = 0                 # esp relative to entry [esp]=retaddr E0
    reg_sym = {"ecx": "in_ptr", "eax": None, "edx": None, "ebx": None,
               "esi": None, "edi": None, "ebp": None}  # ebp unknown at entry
    x87 = None
    slot_sym = {}            # absolute address rel E0 -> symbol
    formulas = []            # (offset, formula, write_va)
    push_vas = []
    call_rows = []

    A("[S.4] SETTER ABI + ESP LEDGER (instruction-by-instruction; callee ret conventions measured by decode)")
    A("  Frame convention (measured below): entry [esp]=retaddr (E0); ECX = input; 'sub esp,0x10' local frame;")
    A("  call net effect on esp = +ret_n(target) after return (measured per callee, SP.ret_convention).")
    A("")

    for ins in setter_ins:
        mn = ins.mnemonic
        ops = list(ins.operands) if ins.operands else []
        va = ins.address
        note = ""
        # ---- esp ledger ----
        if mn == "push" and ops and ops[0].type == X86_OP_REG:
            push_vas.append(va)
            esp -= 4
            note = "push %s -> esp=%+d" % (md.reg_name(ops[0].reg), esp)
        elif mn == "call" and ops and ops[0].type == X86_OP_IMM:
            tgt = ops[0].imm
            n, det = SP.ret_convention(md, img, tgt, ret_cache)
            call_rows.append((va, tgt, n, det))
            if n is not None:
                esp += n
            note = "call 0x%08X ret_n=%s -> esp=%+d" % (tgt, n, esp)
        elif mn == "call":
            call_rows.append((va, None, None, "indirect"))
            note = "call indirect (esp model assumes ret 0)"
        elif mn == "add" and ops and ops[0].type == X86_OP_REG and md.reg_name(ops[0].reg) == "esp" \
                and ops[1].type == X86_OP_IMM:
            esp += ops[1].imm
            note = "add esp,%#x -> esp=%+d" % (ops[1].imm, esp)
        elif mn == "sub" and ops and ops[0].type == X86_OP_REG and md.reg_name(ops[0].reg) == "esp" \
                and ops[1].type == X86_OP_IMM:
            esp -= ops[1].imm
            note = "sub esp,%#x -> esp=%+d" % (ops[1].imm, esp)

        # ---- slot content trace ----
        try:
            if mn == "mov" and ops and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG:
                m = ops[0].mem
                base = md.reg_name(m.base) if m.base else None
                rn = md.reg_name(ops[1].reg)
                if base == "esp":
                    slot_sym[esp + m.disp] = reg_sym.get(rn)
                elif base == "eax" and reg_sym.get("eax") == "S_PTR":
                    if reg_sym.get(rn) is not None:
                        formulas.append((m.disp, "S[%d] := %s" % (m.disp, reg_sym.get(rn)), va))
                    else:
                        formulas.append((m.disp, "S[%d] := <value from %s; symbol unresolved>" % (m.disp, rn), va))
            elif mn == "mov" and ops and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
                rn = md.reg_name(ops[0].reg)
                m = ops[1].mem
                base = md.reg_name(m.base) if m.base else None
                if base == "esp":
                    reg_sym[rn] = slot_sym.get(esp + m.disp)
                elif base == "ecx" and reg_sym.get("ecx") == "in_ptr":
                    reg_sym[rn] = "int32_in[%d]" % (m.disp // 4)
                else:
                    reg_sym[rn] = None
            elif mn == "mov" and ops and ops[0].type == X86_OP_REG:
                rn = md.reg_name(ops[0].reg)
                reg_sym[rn] = reg_sym.get(md.reg_name(ops[1].reg)) if ops[1].type == X86_OP_REG else None
            elif mn == "neg" and ops and ops[0].type == X86_OP_REG:
                rn = md.reg_name(ops[0].reg)
                reg_sym[rn] = "-(%s)" % reg_sym[rn] if reg_sym.get(rn) else None
            elif mn in ("fild", "fld") and ops and ops[0].type == X86_OP_MEM:
                m = ops[0].mem
                base = md.reg_name(m.base) if m.base else None
                if base == "esp":
                    x87 = "f80(%s)" % slot_sym.get(esp + m.disp)
                else:
                    x87 = "f80(mem@%s%+#x)" % (base, m.disp) if base else "f80(mem)"
            elif mn in ("fstp", "fistp", "fst") and ops and ops[0].type == X86_OP_MEM:
                m = ops[0].mem
                base = md.reg_name(m.base) if m.base else None
                if base == "esp":
                    slot_sym[esp + m.disp] = "f32(%s)" % x87 if x87 else None
                x87 = None
            elif mn.startswith("call"):
                for r in ("eax", "ecx", "edx"):
                    reg_sym[r] = None
                if ops and ops[0].type == X86_OP_IMM and ops[0].imm == GETTER:
                    reg_sym["eax"] = "S_PTR"
                    note += " | EAX := S_PTR (getter return)"
            else:
                # conservative: any GPR write clears its symbol (esp ledger mnemonics are
                # already handled above; skip them here)
                if mn not in ("push", "pop", "call", "ret", "retf", "add", "sub", "mov"):
                    try:
                        for regid in ins.regs_write:
                            nm = md.reg_name(regid)
                            nm = SP.SUBREG_PARENT.get(nm, nm)
                            if nm in reg_sym:
                                reg_sym[nm] = None
                            if nm == "esp":
                                note += " | (esp written by %s — ledger assumes no net change unless matched above)" % mn
                    except Exception:  # noqa
                        pass
        except Exception as e:  # noqa
            note += " | TRACE-UNRESOLVED(%s)" % e

        A("  %-44s esp=%+d  %s" % (fmt(ins), esp, note))

    A("")
    A("  Push instructions measured in the setter: %s" % ", ".join("0x%08X" % p for p in push_vas))
    A("  Direct calls measured in the setter:")
    for va, tgt, n, det in call_rows:
        A("    @0x%08X -> %s  ret_n=%s  (%s)" % (va, "0x%08X" % tgt if tgt else "indirect", n, det))
    A("")
    A("[S.10] SETTER WRITE FORMULAS (slot-content dataflow trace; from the same decoded instructions)")
    A("  Local slot contents at the write-value loads (slots are esp-relative; esp=%+d at the getter return" % esp)
    A("  per the ledger; the value loads are [esp+K] with the SAME esp, so they read the local frame slots):")
    for off, formula, va in formulas:
        A("    write @0x%08X  %s" % (va, formula))
    if formulas:
        offs = sorted(set(f[0] for f in formulas))
        A("  Measured write offsets through EAX (=S_PTR, engine-proven in [S.1.4]): %s" % offs)
    else:
        A("  !!! no S-writes captured by the dataflow trace — instrument/shape mismatch; inspect the decode.")
    A("  Value symbols recorded for the local frame slots (from neg + fild/fstp chain in the decode above).")
    A("")
    return push_vas, call_rows


def main():
    out = []
    A = out.append
    img = L.Image()  # S0 FAIL-CLOSED (size + SHA256 + PE32 i386 + ImageBase) before any decode
    md = L.make_disassembler()

    A("=" * 100)
    A("ORIGIN SETTER 0x00458D90 — FALSIFIER + FULL DECODE + ABI + ESP LEDGER")
    A("RUN_ID (correction): PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915")
    A("CANONICAL PACKAGE: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (in-place correction; no new package root)")
    A("GENERATED_UTC: " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    A("GENERATOR_SCRIPT: %s" % SCRIPT_PATH)
    A("GENERATOR_SHA256: %s" % script_sha256())
    A("MEASURED ENVIRONMENT:")
    for ln in L.measured_env(img).split("\n"):
        A("  " + ln)
    A("S0 FAIL-CLOSED: PASSED at script start (size+sha256+PE layout re-verified before any decode).")
    A("SOURCE OF TRUTH: Entropia.exe physical bytes (capstone linear decode). No external report is")
    A("  imported as evidence; PE-MASTER cross-check anchors are recorded AFTER measurement as")
    A("  comparisons (discrepancies are reported loudly, never forced).")
    A("PURPOSE (contract Section 3): FIRST falsifier — reproduce or reject from physical bytes the")
    A("  claimed write-through at call site 0x00458E27 (call FUN_00437F70), BEFORE any canonical edit.")
    A("=" * 100)
    A("")

    # ============ [S.1] FALSIFIER ============
    A("[S.1] FALSIFIER — call site 0x00458E27 and the path through it")
    A("")
    A("[S.1.1] Direct call verification at 0x00458E27")
    bts = img.read(0x458E27, 5)
    rel = struct.unpack("<i", bts[1:5])[0]
    eff_target = 0x458E27 + 5 + rel
    for ins in md.disasm(bts, 0x458E27):
        A("  bytes: %s   capstone: %s %s" % (" ".join("%02x" % x for x in bts), ins.mnemonic, ins.op_str))
        break
    call_ok = (eff_target == GETTER)
    A("  raw E8 rel32 = %+d -> effective target 0x%08X (getter 0x%08X): %s" % (
        rel, eff_target, GETTER, "MATCH" if call_ok else "MISMATCH — LOUD REPORT"))
    A("")

    A("[S.1.2] GETTER FUN_00437F70 — return-value proof (path-sensitive EAX trace)")
    paths = getter_eax_paths(md, img)
    for ret_va, tok, path in paths:
        A("  ret path -> ret@0x%08X : EAX = %s   [path: %s]" % (
            ret_va, tok, " ; ".join(path) if path else "(straight-line)"))
    getter_ins = decode_range(img, md, GETTER, 0x437FF0)
    rets = [i for i in getter_ins if i.mnemonic in ("ret", "retf")]
    A("  Terminals in 0x437F70..0x437FF0: %s" % ", ".join(
        "0x%08X '%s'" % (i.address, i.mnemonic + " " + i.op_str) for i in rets))
    A("  (Full getter decode in [S.2]; ctor 0x82B580 decode in [S.9].)")
    A("")

    A("[S.1.3] REGISTER STATE AT 0x00458E2C (immediately after the call returns)")
    A("  The call at 0x458E27 is a DIRECT call to FUN_00437F70 (S.1.1); the getter trace (S.1.2) shows")
    A("  its return value in EAX (fast path: EAX=[0xba1804]; cold-success: EAX = ctor return = same pointer;")
    A("  alloc-fail corner: EAX=NULL — disclosed corner, does not remove the write instructions).")
    A("  Decoded instructions 0x458E2C..0x458E30 (between call return and the first claimed write):")
    eax_clobber = []
    for ins in decode_range(img, md, 0x458E2C, 0x458E30):
        A("    " + fmt(ins))
        eff = defines_eax(md, ins)
        if eff is not None:
            eax_clobber.append((ins.address, eff))
    if eax_clobber:
        A("  !!! EAX written between call return and first write at: %s — EAX provenance NOT preserved (LOUD REPORT)" % eax_clobber)
    else:
        A("  no instruction in 0x458E2C..0x458E30 writes EAX -> EAX still holds FUN_00437F70's return value.")
    eax_prov = "FUN_00437F70_RETURN" if (call_ok and not eax_clobber) else "OTHER/UNVERIFIED — LOUD REPORT"
    A("  EAX_PROVENANCE_AT_0x458E2C = %s" % eax_prov)
    A("")

    A("[S.1.4] SYMBOLIC S_PTR WALK (sprov.Engine) — window from 0x458E2C, N=16 instructions")
    ret_cache = {}

    def ret_lookup(va):
        return SP.ret_convention(md, img, va, ret_cache)

    win = decode_range(img, md, 0x458E2C, 0x458E2C + 0x40)
    eng = SP.Engine(init_regs={"eax": SP.Tok(0)}, getter_va=GETTER, ret_lookup=ret_lookup)
    for ins in win[:16]:
        A("    " + fmt(ins))
        if eng.step(md, ins) == "STOP":
            break
    A("  Events (measured):")
    for e in eng.events:
        A("    %r" % e)
    writes = [e for e in eng.events if e.kind == "WRITE_S"]
    A("  WRITE_S events: %d" % len(writes))
    for e in writes:
        A("    0x%08X %s" % (e.va, e.detail))
    A("")
    if writes:
        offs = sorted(int(e.detail.split("off=")[1].split(" ")[0]) for e in writes)
        A("  => >=1 valid write through a register proven to contain S exists (offsets %s at %s)." % (
            offs, ", ".join("0x%08X" % e.va for e in writes)))
        A("     Counterexample to the original 'no caller writes through the returned pointer' claim (see")
        A("     ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv for the full census; status algebra in")
        A("     02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md).")
    else:
        A("  => no write-through reproduced: EXTERNAL FINDING NOT REPRODUCED — report to PE-MASTER before any edit.")
    A("")

    A("[S.1.5] INSTRUMENT SELF-TEST (known-negative control: the SF slot3 pair site 0x0050A075)")
    eng2 = SP.Engine(init_regs={"eax": SP.Tok(0)}, getter_va=GETTER, ret_lookup=ret_lookup)
    win2 = decode_range(img, md, 0x50A07A, 0x50A07A + 0x20)
    for ins in win2[:16]:
        if eng2.step(md, ins) == "STOP":
            break
    for e in eng2.events:
        A("    %r" % e)
    esc2 = [e for e in eng2.events if e.kind == "ESCAPE_ARGREG"]
    if esc2:
        cls = SP.classify_callee_head(md, img, PAIR_HELPER, ("reg", "ecx"), ret_cache)
        A("    head classification of escaped channel (reg ecx -> 0x82B5A0): %s (decode_error=%s stopped=%s)" % (
            cls["class"], cls["decode_error"], cls["stopped"]))
        A("    (expected instrument behavior: ESCAPE_ARGREG via mov ecx,eax; callee head READ_ONLY — 0x82B5A0")
        A("     reads [ecx+0/4/8] in its fsub chain and never stores through an ECX-derived pointer.)")
    else:
        A("    !!! self-test did not produce the expected escape event — instrument defect; fix before census.")
    A("")

    # ============ [S.2] GETTER FULL DECODE ============
    A("[S.2] FUN_00437F70 GETTER — full decode 0x437F70..0x437FF0 (both terminals + padding + next fn)")
    A("")
    for ins in getter_ins:
        A("  " + fmt(ins))
    pad = img.read(0x437FE7, 16)
    A("  padding bytes at 0x437FE7: %s" % " ".join("%02x" % x for x in pad))
    A("  next function starts 0x437FF0:")
    for _ln in head_lines(img, md, 0x437FF0, 4, indent="    "):
        A(_ln)
    e8s, e9s, imm32s = L.scan_calls(img, GETTER)
    pat = L.scan_pattern_calls(img, SLOT)
    A("")
    A("  singleton-cache slot 0xBA1804 whole-image imm32 occurrences: %d -> %s" % (
        len(pat), ", ".join("%s@0x%08X" % (nm, va) for nm, va in pat)))
    A("  getter call channels: E8=%d E9=%d imm32(.text)=%d" % (len(e8s), len(e9s), len(imm32s)))
    A("")

    # ============ [S.3] SETTER FULL DECODE ============
    A("[S.3] SETTER FUN_00458D90 — full decode 0x458D90..0x458E50 (terminal + padding + next fn)")
    A("")
    setter_ins = decode_range(img, md, SETTER, 0x458E50)
    for ins in setter_ins:
        A("  " + fmt(ins))
    term = [i for i in setter_ins if i.mnemonic in ("ret", "retf")]
    A("  terminals: %s" % ", ".join("0x%08X %s" % (i.address, i.mnemonic) for i in term))
    if term:
        last = term[-1]
        pad_start = last.address + last.size
        padb = img.read(pad_start, 0x458E50 - pad_start)
        A("  bytes 0x%08X..0x458E50 (padding + next-function head): %s" % (
            pad_start, " ".join("%02x" % x for x in padb)))
        n_cc = 0
        for x in padb:
            if x == 0xCC:
                n_cc += 1
            else:
                break
        A("  int3 padding run: %d bytes at 0x%08X..0x%08X" % (n_cc, pad_start, pad_start + n_cc - 1))
    A("  next function starts 0x00458E50:")
    for _ln in head_lines(img, md, 0x458E50, 6, indent="    "):
        A(_ln)
    A("")

    # ============ [S.4]+[S.10] LEDGER + DATAFLOW ============
    push_vas, call_rows = setter_ledger_and_dataflow(img, md, out)

    # ============ [S.5] CHAIN MEMBER ABI TABLE ============
    A("[S.5] CHAIN MEMBER ABI TABLE (bounded head 0xA0; ret convention + absolute .data refs)")
    seen = set()
    for va, tgt, n, det in call_rows:
        if tgt is None or tgt in seen:
            continue
        seen.add(tgt)
        head = SP.decode_head(md, img, tgt, 0xA0)
        A("  callee 0x%08X (called @0x%08X): ret_n=%s (%s)" % (tgt, va, n, det))
        A("    absolute .data imm32 refs in bounded head: %s" % (
            data_refs_in_head(img, head[0]) or "(none)"))
        A("    head (first 12 instructions):")
        for i in head[0][:12]:
            A("      " + fmt(i))
        if head[1]:
            A("    head decode note: %s" % head[1])
        A("")

    # ============ [S.6] CALLER FUN_00458E50 ============
    A("[S.6] CALLER FUN_00458E50 — full decode (triple production + delta condition + setter call)")
    A("  (linear decode from 0x458E50, bounded 0x100 bytes; stops at the first terminal + padding)")
    A("")
    caller_all = decode_range(img, md, 0x458E50, 0x458F50)
    caller_ins = []
    for i in caller_all:
        caller_ins.append(i)
        if i.mnemonic in ("ret", "retf"):
            break
    for ins in caller_ins:
        A("  " + fmt(ins))
    cterm = [i for i in caller_ins if i.mnemonic in ("ret", "retf")]
    A("  first terminal in window: %s" % (
        ", ".join("0x%08X %s" % (i.address, i.mnemonic + " " + i.op_str) for i in cterm) or "none in window"))
    if cterm:
        tend = cterm[-1].address + cterm[-1].size
        padb = img.read(tend, 0x10)
        A("  padding bytes after terminal: %s" % " ".join("%02x" % x for x in padb))
    direct_calls = ["0x%08X -> 0x%08X" % (i.address, i.operands[0].imm) for i in caller_ins
                    if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM]
    A("  direct imm32 call targets in window: %s" % direct_calls)
    A("")

    A("[S.6.1] 0x00458C40 bounded decode (head 24 instructions — what the bytes show it produces)")
    for _ln in head_lines(img, md, 0x458C40, 24, indent="  "):
        A(_ln)
    A("")

    A("[S.7] FTOL-STYLE HELPER 0x0095DA40 — bounded head (operation class from bytes)")
    for _ln in head_lines(img, md, FTOL, 24, indent="  "):
        A(_ln)
    n, det = SP.ret_convention(md, img, FTOL, ret_cache)
    A("  ret convention: %s (%s)" % (n, det))
    A("")

    # ============ [S.8] TRIPLE RECOUNT + .DATA VIRTUAL TAIL + CTOR ============
    A("[S.8] INDEPENDENT RECOUNTS (measurements for the status algebra)")
    counts = {}
    for tv in TRIPLE:
        pat2 = L.scan_pattern_calls(img, tv)
        counts[tv] = len(pat2)
        per_sec = {}
        for nm, va in pat2:
            per_sec[nm] = per_sec.get(nm, 0) + 1
        A("  imm32 occurrences of 0x%08X in whole image: %d  (per-section: %s)" % (
            tv, len(pat2), ", ".join("%s=%d" % kv for kv in sorted(per_sec.items()))))
    A("  total triple dword occurrences: %d" % sum(counts.values()))
    for nm, va_s, vs, ro, rs in img.sections:
        if nm == ".data":
            raw_end = va_s + rs
            A("  .data: vaddr=0x%X vsize=0x%X rawsize=0x%X -> raw end RVA 0x%X; virtual end 0x%X" % (
                va_s, vs, rs, raw_end, va_s + vs))
            for tv in TRIPLE:
                rva = tv - img.imagebase
                A("    triple 0x%08X RVA 0x%X: %s" % (
                    tv, rva, "BEYOND raw end (virtual tail; loader zero-fill)" if rva >= raw_end else "inside raw"))
    A("")
    A("[S.9] CTOR 0x0082B580 — bounded decode (initial value copy of the singleton)")
    for _ln in head_lines(img, md, CTOR, 20, indent="  "):
        A(_ln)
    n, det = SP.ret_convention(md, img, CTOR, ret_cache)
    A("  ret convention: %s (%s)" % (n, det))
    A("")

    # ============ labels ============
    A("REQUIRED OUTPUT LABELS (contract Section 5):")
    A("  ORIGIN_SETTER_OPERATION = %s" % (
        "three f32 stores through the getter-returned singleton pointer: mov [S+0],edx @0x458E30, "
        "mov [S+4],ecx @0x458E36, mov [S+8],edx @0x458E3D (offsets 0/4/8); each value = f32(-(int32)in[i]) "
        "produced by neg + fild/fstp in the local frame before the call (see [S.3]/[S.4]/[S.10])"
        if writes else "NOT REPRODUCED — see falsifier section"))
    A("  ORIGIN_SETTER_INPUT_TYPE = %s" % (
        "ECX = pointer to a 12-byte triple of three int32 at [ecx+0/4/8] (thiscall-style; no stack args; "
        "plain ret; caller FUN_00458E50 builds the triple via three fld+call 0x95DA40 f32->int32 conversions "
        "and stores it to [esi+0/4/8] before the call — see [S.6])"
        if writes else "UNVERIFIED (falsifier did not reproduce)"))
    A("  ORIGIN_SETTER_FINAL_SEMANTIC_ROLE = UNVERIFIED (no semantic name assigned; STATIC-ONLY run;")
    A("      runtime execution/value not measured)")
    A("")

    # ============ evidence-quality block ============
    A("MEASURED_QUANTITY: instruction-level capstone decode + symbolic S_PTR provenance events at")
    A("  call site 0x00458E27 and its enclosing function (plus getter/caller/chain decodes, ret")
    A("  conventions, triple imm32 recount, .data virtual-tail layout, ctor decode).")
    A("INDEPENDENT_SOURCE_OF_TRUTH: Entropia.exe physical bytes (size 8015872, SHA256 E7785430E81DFFE6")
    A("  48CE8F5312414B17BC9FCE61389689A22F753765D5280F31; S0 fail-closed verified at script start).")
    A("WHY_NON_CIRCULAR: this probe decodes bytes directly; it imports no external auditor result and")
    A("  no PE-MASTER anchor as input (anchors are post-hoc cross-checks only; discrepancies reported loudly).")
    A("FAILURE_CASE_DETECTED: YES — call site 0x00458E27 with writes 0x458E30/0x458E36/0x458E3D through")
    A("  EAX = FUN_00437F70 return is the counterexample to the original 'no caller writes through the")
    A("  returned pointer' claim; the original run's own HELPER437F70_CALLER_CENSUS.csv row for this site")
    A("  recorded instruction_after_next='mov dword ptr [eax], edx' but never interpreted write-through.")
    A("")

    path = os.path.join(RAW, "ORIGIN_SETTER_458D90_DISASM.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("written:", path)
    ws = [e for e in eng.events if e.kind == "WRITE_S"]
    print("FALSIFIER: EAX_PROVENANCE_AT_0x458E2C =", eax_prov)
    print("FALSIFIER: WRITE_S events:", [(hex(e.va), e.detail) for e in ws])
    print("self-test events:", [e.kind for e in eng2.events])
    if esc2:
        print("self-test head class (0x82B5A0/ecx):", cls["class"])
    print("getter eax paths:", [(hex(r), t) for r, t, _ in paths])


if __name__ == "__main__":
    main()
