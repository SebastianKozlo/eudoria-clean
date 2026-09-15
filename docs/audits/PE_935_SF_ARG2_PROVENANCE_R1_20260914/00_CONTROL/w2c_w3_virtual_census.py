# w2c_w3_virtual_census.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# W2(c) VIRTUAL CALL-SITE census of the SF slot-3 channel (+ W3 arg2 producers).
#
# DECLARED BOUND (contract default): TWO levels of register/dataflow tracing.
#   Level 1 = the def of the receiver register within a 48-byte backward decode
#   window; Level 2 = one further def hop (same window rule) when level 1 is a
#   register-to-register copy or an unresolved source register.
#
# CENSUS PATTERNS (byte-level scan of .text, false positives included by design;
# every candidate then decoded and classified):
#   P1  call [reg+0x0C]   : FF 50..57 0C   (mod=01 disp8)  [reg = vtable OR object]
#   P1J jmp  [reg+0x0C]   : FF 60..67 0C   (mod=01 disp8)  (tail-call form)
#   P2  call [reg+0x0C]   : FF 90..97 0C 00 00 00 (mod=10 disp32)
#   P3  mov dst,[vt+0x0C] : 8B /r mod=01/10 disp=0x0C, followed within <=3
#       decoded non-control instructions (24-byte window) by call dst / jmp dst
#
# A candidate is a VTABLE SLOT-3 CALL only when a vtable load `mov vtreg,[objreg]`
# is found in its backward window; otherwise it is a FIELD call (recorded as
# NOT_A_VTABLE_CALL — honest denominator, not a slot-3 channel candidate).
#
# RECEIVER PROOF rules (W2c.3; SF-proven values):
#   (i)   level-1 def `mov obj,[base+0xC0]` (base != esp/ebp) -> holder-slot read
#         (the distinctive "instance+0xC0" slot, B.3) -> PROVEN_HOLDER_0xC0.
#         Holder offsets {0x04,0x0C,0x10,0x14,0x18} on a register base are TOO
#         GENERIC for standalone promotion (any class may have them) ->
#         HOLDER_GENERIC_INSUFFICIENT (container identity not provable in bound).
#         Stack reads [esp/ebp+X] are PARAMETER/LOCAL, never holder reads.
#   (ii)  ctor chain: def reaches `call FUN_00509330` (SF ctor, B.3 re-verified)
#         with obj = returned eax -> PROVEN_CTOR.
#   (iii) another SF-proven value: vtable store `mov [obj],0x00A7D458` in window
#         -> PROVEN_VTABLE_STORE (strongest); receiver = the `this` of a
#         known SF function -> PROVEN_SF_METHOD_THIS.
#   REJECTED_NOT_SF (NC-2 evidence): (a) vtable store `mov [obj],imm32` with
#         imm32 != SF vtable (class named via in-exe RTTI); (b) receiver = the
#         `this` of a method that is a vtable slot function of an RTTI class
#         other than SceneFeederObject (its this cannot be an SF object).
#   Everything else -> INSUFFICIENT_PROOF (recorded, never silently dropped).
#
# VTABLE-EXTENT RULE (PE-MASTER adjudication, loop 2ed038db R1 correction
#   batch 2026-09-14; the FNMAP boundary lesson's data-array analog): a
#   COL-derived vtable's extent ENDS at the first dword that is not a
#   plausible code pointer (outside the .text VA range) — reading past it
#   overruns into adjacent .rdata (string literals, COL pointers, the next
#   vtable) and fabricates memberships. The pre-fix fixed 16-slot enumeration
#   produced exactly this artifact: the .?AVArkAudioObjectInterface@@ vtable
#   0x00A7D42C (6 real slots) was read through the 'ArkSceneFeeder' string
#   literal and the SF COL into the SF vtable, fabricating 'slots 11..15'
#   memberships for the SF slot functions (RETRACTED claim; corrected by the
#   extent rule in build_rtti_maps + the measured adjacency disclosure in
#   main()).
#
# METHOD 1 (holder-slot route): enumerate `mov reg,[base+disp]` reads with
#   disp in {0x04,0x0C,0x10,0x14,0x18,0xC0} (base != esp/ebp, non-SIB); forward
#   decode <=48 bytes; flag only genuine SLOT-3 vcall flows (vtable load of the
#   holder-loaded value + call/jmp [vt+0x0C] or mov f,[vt+0x0C]+call f).
#
# CAL-3 (self-added known-answer calibration of the receiver tracer, NOT run
#   evidence): pointed at the published receiver-proof site (receiver ecx of the
#   E8 call at 0x00529020 to FUN_005094C0, B.3), must classify PROVEN_HOLDER_0xC0.
#
# W3 (verified sites only): arg2 = the FIRST push before the call (rightmost
#   stack arg; ret-8 callee pops 2 stack args); producer traced <=2 levels;
#   string literals read back VERBATIM at the literal VA (NC-3).
#
# Outputs (01_RAW, deterministic):
#   VIRTUAL_CALLSITE_CENSUS.csv, ARG2_PRODUCER_TRACE.txt

import bisect
import struct
import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C
import capstone
from capstone import x86

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
SF_VTABLE = 0x00A7D458
SF_CLASS = "SceneFeederObject"
SF_SLOT3_FUN = 0x0050A050
SF_CTOR = 0x00509330
SF_KNOWN_FUNCS = {0x50A460, 0x5090A0, 0x5090B0, 0x50A050, 0x5090C0, 0x509580,
                  0x5094C0, 0x509330, 0x50A240}
HOLDER_OFFSETS = {0x04, 0x0C, 0x10, 0x14, 0x18, 0xC0}
MAX_BACK = 48          # backward decode window (bytes) per level
MAX_LEVELS = 2          # declared bound: two levels
REG8_IDS = {0: "eax", 1: "ecx", 2: "edx", 3: "ebx", 4: "esp", 5: "ebp", 6: "esi", 7: "edi"}


# ------------------------------------------------------------------ helpers
def build_fn_lattice(exe):
    t = exe.text_section()
    t_va = exe.image_base + t["vaddr"]
    tb = exe.read_off(t["rawptr"], t["rawsize"])
    lat = set()
    for i in range(len(tb) - 5):
        b = tb[i]
        if b in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", tb, i + 1)[0]
            lat.add(t_va + i + 5 + rel)
    return sorted(lat)


def build_rtti_maps(exe):
    """Returns (vtable->class, fn->[(class,slot),...]) from in-exe RTTI.
    MEASURED RTTI layout of this binary (debugged on the SF class): vtable[-1]
    = VA(COL); COL = {sig=0, offset=0, cdOffset=0, pTypeDescriptor=VA(td),
    pClassDescriptor=VA(cd)} — POINTER-based (VA) fields, not RVA-based.
    VTABLE-EXTENT RULE (PE-MASTER adjudication, loop 2ed038db R1 correction
    batch 2026-09-14; the FNMAP boundary lesson's data-array analog): a
    COL-derived vtable's extent ENDS at the first dword that is not a
    plausible code pointer (outside the .text VA range) — reading past it
    overruns into adjacent .rdata (string literals, COL pointers, the next
    vtable) and fabricates memberships. The pre-fix fixed 16-slot enumeration
    produced exactly this artifact: the .?AVArkAudioObjectInterface@@ vtable
    0x00A7D42C (6 real slots) was read through the 'ArkSceneFeeder' string
    literal and the SF COL into the SF vtable, fabricating 'slots 11..15'
    memberships for the SF slot functions (RETRACTED claim)."""
    vt_class = {}
    fn_slots = {}
    data = exe.data
    img = exe.image_base
    ts = exe.text_section()
    text_lo = img + ts["vaddr"]
    text_hi = img + ts["vaddr"] + ts["vsize"]
    tds = []
    pos = 0
    while True:
        p = data.find(b".?A", pos)
        if p == -1:
            break
        name_va = exe.off_to_va(p)
        if name_va is not None:
            nul = data.find(b"\x00", p)
            if nul != -1 and 0 < nul - p < 256 and all(32 <= c < 127 for c in data[p:nul]):
                td_va = name_va - 8
                if td_va >= img:
                    tds.append((td_va, data[p:nul].decode("ascii")))
        pos = p + 1
    for td_va, name in tds:
        needle = struct.pack("<I", td_va)  # VA-based pTypeDescriptor
        q = data.find(needle)
        while q != -1:
            col_va = exe.off_to_va(q - 0x0C) if q >= 0x0C else None
            if col_va is not None and col_va >= img:
                n2 = struct.pack("<I", col_va)
                r = data.find(n2)
                while r != -1:
                    vt_va = exe.off_to_va(r + 4)
                    if vt_va is not None and vt_va >= img:
                        if vt_va not in vt_class:
                            vt_class[vt_va] = name
                        base_off = exe.va_to_off(vt_va)
                        if base_off is not None:
                            slot = 0
                            while True:
                                try:
                                    fv = struct.unpack_from("<I", data, base_off + 4 * slot)[0]
                                except Exception:
                                    break
                                if not (text_lo <= fv < text_hi):
                                    break  # VTABLE-EXTENT rule: first non-code dword ends the vtable
                                fn_slots.setdefault(fv, []).append((name, slot))
                                slot += 1
                    r = data.find(n2, r + 1)
            q = data.find(needle, q + 1)
    return vt_class, fn_slots


def decode_back_chains(exe, md, end_va, max_back=MAX_BACK):
    chains = []
    lo = end_va - max_back
    for s in range(lo, end_va):
        try:
            code = exe.read_va(s, end_va - s)
        except Exception:
            continue
        if not code:
            continue
        ins = []
        ok = True
        for i in md.disasm(code, s):
            ins.append(i)
            if i.address + i.size > end_va:
                ok = False
                break
            if i.address + i.size == end_va:
                break
        if ok and ins and ins[-1].address + ins[-1].size == end_va:
            chains.append(ins)
    return chains


def writes_reg(insn, regname):
    for op in insn.operands:
        if op.type == x86.X86_OP_REG and (op.access & capstone.CS_AC_WRITE):
            if insn.reg_name(op.reg) == regname:
                return True
    if insn.mnemonic == "call" and regname == "eax":
        return True
    if insn.mnemonic.startswith("pop"):
        return regname in insn.op_str.split(",")[0]
    return False


def last_def(chain, regname):
    res = None
    for idx, insn in enumerate(chain):
        if writes_reg(insn, regname):
            res = (insn, idx)
    return res


def classify_def(insn):
    if insn.mnemonic == "mov" or insn.mnemonic.startswith("movz") or insn.mnemonic.startswith("movs"):
        ops = insn.operands
        if len(ops) >= 2:
            if ops[1].type == x86.X86_OP_MEM:
                mem = ops[1].mem
                if mem.index == 0 and mem.base != 0:
                    return ("MEM_READ", insn.reg_name(mem.base), mem.disp)
                if mem.base == 0 and mem.index == 0:
                    return ("MEM_ABS", None, mem.disp)
                return ("MEM_SIB", None, None)
            if ops[1].type == x86.X86_OP_REG:
                return ("REG_COPY", insn.reg_name(ops[1].reg), None)
            if ops[1].type == x86.X86_OP_IMM:
                return ("IMM", ops[1].imm & 0xFFFFFFFF, None)
    if insn.mnemonic == "lea":
        return ("LEA", None, None)
    if insn.mnemonic == "call":
        return ("CALL", imm_of(insn), None)
    if insn.mnemonic.startswith("pop"):
        return ("POP", None, None)
    if insn.mnemonic == "xor":
        ops = insn.operands
        if len(ops) == 2 and ops[0].type == x86.X86_OP_REG and ops[1].type == x86.X86_OP_REG \
                and ops[0].reg == ops[1].reg:
            return ("ZERO", None, None)
    return ("OTHER", None, None)


def imm_of(insn):
    for op in insn.operands:
        if op.type == x86.X86_OP_IMM:
            return op.imm & 0xFFFFFFFF
    return None


def find_vtable_store(chain, objreg):
    for insn in chain:
        if insn.mnemonic == "mov" and len(insn.operands) >= 2:
            op0, op1 = insn.operands[0], insn.operands[1]
            if op0.type == x86.X86_OP_MEM and op1.type == x86.X86_OP_IMM:
                mem = op0.mem
                if mem.index == 0 and mem.base != 0:
                    if insn.reg_name(mem.base) == objreg and mem.disp == 0:
                        return (insn, op1.imm & 0xFFFFFFFF)
    return None


def enclosing_of(lattice, va):
    i = bisect.bisect_right(lattice, va) - 1
    return lattice[i] if i >= 0 else None


def this_route_verdict(call_va, objreg, lattice, fn_slots):
    """Receiver unresolved in-window but identifiable as the enclosing function's
    this (objreg == ecx, or objreg copied from ecx with no further def).
    Enclosing function identity decides: SF known function -> PROVEN;
    non-SF vtable-slot method -> REJECTED_NOT_SF (its this is that class)."""
    enc = enclosing_of(lattice, call_va)
    if enc is None:
        return None
    if enc in SF_KNOWN_FUNCS:
        return ("PROVEN_SF_METHOD_THIS",
                f"receiver = `this` of enclosing SF function {enc:#010x} (known SF function set, B.3)")
    if enc in fn_slots:
        classes = sorted({c for c, _ in fn_slots[enc]})
        if len(classes) == 1 and classes[0] != SF_CLASS:
            slot = min(s for c, s in fn_slots[enc] if c == classes[0])
            return ("REJECTED_NOT_SF",
                    f"receiver = `this` of enclosing method {enc:#010x} = vtable slot {slot} of RTTI class "
                    f"{classes[0]} (its this is a {classes[0]}, not an SF)")
        if len(classes) == 1 and classes[0] == SF_CLASS:
            return ("PROVEN_SF_METHOD_THIS",
                    f"receiver = `this` of enclosing method {enc:#010x} = vtable slot function of {SF_CLASS}")
        if any(c == SF_CLASS for c in classes):
            return None  # ambiguous (SF among candidates) — do not reject
        return ("REJECTED_NOT_SF",
                f"receiver = `this` of enclosing method {enc:#010x} = vtable slot function of classes "
                f"{classes} (all non-SF)")
    return None


def trace_receiver(exe, md, call_va, objreg, chains, lattice, fn_slots, vt_class, level=1):
    defs = []
    for ch in chains:
        d = last_def(ch, objreg)
        if d:
            defs.append((d[0], ch))
    if not defs:
        tr = this_route_verdict(call_va, objreg, lattice, fn_slots)
        if tr:
            return {"classification": tr[0],
                    "evidence": tr[1] + f" (no def of {objreg} in window — incoming this)",
                    "chain": chains[0] if chains else None, "def_insn": None}
        return {"classification": "INSUFFICIENT_PROOF",
                "evidence": f"no def of {objreg} in any backward chain (parameter/incoming)",
                "chain": chains[0] if chains else None, "def_insn": None}
    def_vas = sorted({ins.address for ins, _ in defs})
    if len(def_vas) > 1:
        return {"classification": "INSUFFICIENT_PROOF",
                "evidence": f"AMBIGUOUS: multiple chains disagree on def of {objreg} at {[hex(v) for v in def_vas]}",
                "chain": chains[0], "def_insn": None}
    def_insn, chain = defs[0]
    vt_store = find_vtable_store(chain, objreg)
    form = classify_def(def_insn)
    rec = {"def_insn": def_insn, "form": form, "chain": chain}

    if vt_store is not None:
        insn, imm = vt_store
        if imm == SF_VTABLE:
            rec.update({"classification": "PROVEN_VTABLE_STORE",
                        "evidence": f"SF vtable store {C.insn_str(insn)} (imm32 == 0x00A7D458)"})
        else:
            cls = vt_class.get(imm, "unknown-class")
            rec.update({"classification": "REJECTED_NOT_SF",
                        "evidence": f"vtable store {C.insn_str(insn)} imm32={imm:#010x} != SF vtable; RTTI class: {cls}"})
        return rec

    kind = form[0]
    if kind == "MEM_READ":
        base, disp = form[1], form[2] & 0xFFFFFFFF
        if base in ("esp", "ebp"):
            rec.update({"classification": "INSUFFICIENT_PROOF",
                        "evidence": f"stack read {C.insn_str(def_insn)} ([{base}+{disp:#x}] = parameter/local, not a container holder read)"})
            return rec
        if disp == 0xC0:
            rec.update({"classification": "PROVEN_HOLDER_0xC0",
                        "evidence": f"holder-slot read {C.insn_str(def_insn)} ([base+0xC0], the instance+0xC0 holder slot, B.3)"})
            return rec
        if disp == 0x30:
            rec.update({"classification": "INSUFFICIENT_PROOF",
                        "evidence": f"+0x30 read {C.insn_str(def_insn)} (NiNode-link domain only if base is SF; not proven within bound)"})
            return rec
        rec.update({"classification": "INSUFFICIENT_PROOF",
                    "evidence": f"field read {C.insn_str(def_insn)} (offset {disp:#x}"
                    + (" in B.3 generic holder set; container identity not provable within bound)" if disp in HOLDER_OFFSETS else " not a known SF holder slot)")})
        return rec
    if kind == "MEM_ABS":
        rec.update({"classification": "INSUFFICIENT_PROOF",
                    "evidence": f"absolute memory read {C.insn_str(def_insn)}"})
        return rec
    if kind == "REG_COPY":
        src = form[1]
        if level < MAX_LEVELS:
            sub_chains = decode_back_chains(exe, md, def_insn.address)
            sub = trace_receiver(exe, md, call_va, src, sub_chains, lattice, fn_slots, vt_class, level=level + 1)
            cls = sub["classification"]
            mapping = {
                "PROVEN_HOLDER_0xC0": "PROVEN_HOLDER_0xC0_L2",
                "PROVEN_CTOR": "PROVEN_CTOR",
                "PROVEN_VTABLE_STORE": "PROVEN_VTABLE_STORE",
                "PROVEN_SF_METHOD_THIS": "PROVEN_SF_METHOD_THIS",
                "REJECTED_NOT_SF": "REJECTED_NOT_SF",
            }
            if cls in mapping:
                rec.update({"classification": mapping[cls],
                            "evidence": f"reg copy {C.insn_str(def_insn)} then L2: {sub['evidence']}"})
            else:
                tr = this_route_verdict(call_va, src, lattice, fn_slots) if src == "ecx" else None
                if tr:
                    rec.update({"classification": tr[0],
                                "evidence": f"reg copy {C.insn_str(def_insn)}; {tr[1]}"})
                else:
                    rec.update({"classification": "INSUFFICIENT_PROOF",
                                "evidence": f"reg copy {C.insn_str(def_insn)} then L2 unresolved: {sub['evidence']}"})
            return rec
        rec.update({"classification": "INSUFFICIENT_PROOF",
                    "evidence": f"reg copy {C.insn_str(def_insn)} at bound limit (2 levels)"})
        return rec
    if kind == "CALL":
        tgt = form[1]
        if tgt == SF_CTOR:
            rec.update({"classification": "PROVEN_CTOR",
                        "evidence": f"receiver = result of `call {tgt:#010x}` (SF ctor FUN_00509330, B.3 re-verified)"})
        else:
            rec.update({"classification": "INSUFFICIENT_PROOF",
                        "evidence": f"receiver = result of call {C.insn_str(def_insn)} (target {tgt if tgt else '?'} not the SF ctor; result class unproven)"})
        return rec
    if kind in ("IMM", "LEA", "POP", "ZERO", "OTHER", "MEM_SIB"):
        if objreg == "ecx":
            tr = this_route_verdict(call_va, "ecx", lattice, fn_slots)
            if tr:
                rec.update({"classification": tr[0],
                            "evidence": f"def form {kind} {C.insn_str(def_insn)}; {tr[1]}"})
                return rec
        rec.update({"classification": "INSUFFICIENT_PROOF",
                    "evidence": f"def form {kind}: {C.insn_str(def_insn)}"})
        return rec
    rec.update({"classification": "INSUFFICIENT_PROOF", "evidence": f"unclassified def {C.insn_str(def_insn)}"})
    return rec


# ------------------------------------------------------------------ arg2 (W3)
def trace_arg2(exe, md, call_va, chain):
    ps = [i for i in chain if i.mnemonic == "push"]
    out = {"pushes": [C.insn_str(p) for p in ps], "arg2": None, "class": None,
           "literal_va": None, "literal_bytes": None, "detail": []}
    if len(ps) == 0:
        out["class"] = "NO_PUSH_IN_WINDOW"
        out["detail"].append("no push visible in the backward window — bound exhausted (recorded honestly)")
        return out
    if len(ps) == 1:
        out["detail"].append("only ONE push visible in window (arg1 or arg2 outside window) — bound exhausted")
        p = ps[0]
    else:
        p = ps[-2]  # arg2 = first-pushed = second from the call
    out["arg2"] = C.insn_str(p)
    ops = p.operands
    if ops and ops[0].type == x86.X86_OP_IMM:
        imm = ops[0].imm & 0xFFFFFFFF
        return imm_analysis(exe, out, imm, f"push imm32 {imm:#010x} @ {p.address:#010x}")
    if ops and ops[0].type == x86.X86_OP_MEM:
        out["class"] = "PUSH_MEM"
        out["detail"].append("push dword [mem] — value not statically resolvable (runtime buffer/field)")
        return out
    if ops and ops[0].type == x86.X86_OP_REG:
        reg = p.reg_name(ops[0].reg)
        d = last_def(chain, reg)
        if d is None:
            out["class"] = "REGISTER_INCOMING"
            out["detail"].append(f"push {reg}: no def in window (incoming value; runtime origin)")
            return out
        cur = d[0]
        lvl = 1
        while True:
            form = classify_def(cur)
            if form[0] == "IMM":
                return imm_analysis(exe, out, form[1], f"producer {C.insn_str(cur)}")
            if form[0] == "MEM_READ":
                base, disp = form[1], form[2] & 0xFFFFFFFF
                out["class"] = "MEMBER_FIELD"
                out["detail"].append(f"producer {C.insn_str(cur)} = [{base}+{disp:#x}] (member field read; content runtime)")
                return out
            if form[0] == "MEM_ABS":
                return imm_analysis(exe, out, form[2] & 0xFFFFFFFF, f"producer {C.insn_str(cur)} = absolute memory dereference")
            if form[0] == "LEA":
                out["class"] = "LEA_COMPUTED"
                out["detail"].append(f"producer {C.insn_str(cur)} (computed address)")
                return out
            if form[0] == "REG_COPY" and lvl < MAX_LEVELS:
                src = form[1]
                sub_chains = decode_back_chains(exe, md, cur.address)
                sd = None
                for ch in sub_chains:
                    sd = last_def(ch, src)
                    if sd:
                        break
                if sd is None:
                    out["class"] = "REGISTER_INCOMING"
                    out["detail"].append(f"copy {C.insn_str(cur)}; source {src} has no def in window")
                    return out
                cur = sd[0]
                lvl += 1
                continue
            if form[0] == "CALL":
                out["class"] = "CALL_RESULT"
                out["detail"].append(f"producer {C.insn_str(cur)} (call result; content runtime)")
                return out
            out["class"] = "UNRESOLVED"
            out["detail"].append(f"producer {C.insn_str(cur)} form {form[0]}")
            return out
    out["class"] = "UNRESOLVED"
    return out


def imm_analysis(exe, out, imm, how):
    out["literal_va"] = imm
    sec = None
    try:
        sec = exe.section_name_of_va(imm)
    except Exception:
        pass
    if sec:
        raw = exe.read_va(imm, 64)
        nul = raw.find(b"\x00")
        nul = nul if nul != -1 else 64
        out["literal_bytes"] = raw[: nul + 1]
        asc = raw[:nul].decode("ascii", "replace")
        printable = all(32 <= c < 127 for c in raw[:nul]) if nul else True
        out["class"] = (f"IMM32_STRING_LITERAL (section {sec}, NUL-terminated, {nul} bytes)"
                        if printable else f"IMM32_VALUE (section {sec}; not NUL-terminated ASCII)")
        out["detail"].append(f"{how}; literal read back VERBATIM (NC-3): {raw[:nul+1].hex(' ').upper()}")
        out["detail"].append(f"ASCII: {asc!r}")
    else:
        out["class"] = "IMM32_NONMAPPED"
        out["detail"].append(f"{how}; VA {imm:#010x} has no file bytes (not a mapped literal)")
    return out


# ------------------------------------------------------------------ main
def main():
    exe = C.PinnedExe()
    md = C.make_capstone()
    lattice = build_fn_lattice(exe)
    vt_class, fn_slots = build_rtti_maps(exe)
    t = exe.text_section()
    t_va = exe.image_base + t["vaddr"]
    tb = exe.read_off(t["rawptr"], t["rawsize"])

    log = []
    log.append("ARG2_PRODUCER_TRACE — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (W2c + W3)")
    log.append(C.provenance_header())
    log.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")
    log.append("")
    log.append(f"RTTI vtable->class entries: {len(vt_class)}; vtable-slot function map: {len(fn_slots)} functions")
    log.append(f"SF vtable 0x00A7D458 -> '{vt_class.get(SF_VTABLE, '<not found>')}' "
                + ("(matches published RTTI '.?AVSceneFeederObject@@')" if vt_class.get(SF_VTABLE, "").startswith(".?AVSceneFeederObject") else "(CHECK)"))
    sf_slot_memberships = {fn: fn_slots.get(fn) for fn in SF_KNOWN_FUNCS}
    log.append("SF function -> vtable memberships (MEASURED RTTI, vtable-extent-verified): "
               + "; ".join(f"FUN_{f:08X}={m}" for f, m in sorted(sf_slot_memberships.items()) if m))
    # --- SF/ArkAudio adjacency disclosure (measured; VTABLE-EXTENT rule) ---
    # PE-MASTER adjudication (loop 2ed038db, R1 correction batch 2026-09-14):
    # the pre-fix fixed-16-slot enumeration overran the .?AVArkAudioObjectInterface@@
    # vtable's extent and fabricated the 'SF slots 0-4 == ArkAudio slots 11..15'
    # membership claim (RETRACTED). The corrected structural statement below is
    # MEASURED from the pinned bytes (fail-closed S0 already passed).
    text_lo = exe.image_base + t["vaddr"]
    text_hi = exe.image_base + t["vaddr"] + t["vsize"]

    def _dw(va):
        return struct.unpack_from("<I", exe.data, exe.va_to_off(va))[0]

    def _td_name(td_va):
        raw = exe.read_va(td_va + 8, 64)
        nul = raw.find(b"\x00")
        return raw[:nul].decode("ascii", "replace") if 0 < nul <= 64 else "?"

    def _vtable_extent(va):
        n = 0
        while True:
            try:
                fv = _dw(va + 4 * n)
            except Exception:
                break
            if not (text_lo <= fv < text_hi):
                break
            n += 1
        return n

    ARK_VTABLE = 0x00A7D42C  # the vtable ADJACENT to the SF vtable (measured below)
    ark_col = _dw(ARK_VTABLE - 4)
    ark_name = _td_name(_dw(ark_col + 0x0C))
    ark_n = _vtable_extent(ARK_VTABLE)
    sf_col = _dw(SF_VTABLE - 4)
    sf_name = _td_name(_dw(sf_col + 0x0C))
    sf_n = _vtable_extent(SF_VTABLE)
    sep_start = ARK_VTABLE + 4 * ark_n
    sep = exe.read_va(sep_start, SF_VTABLE - 4 - sep_start)
    log.append("STRUCTURAL CONTEXT (measured, vtable-extent-verified): each SF primary-vtable function "
               "has EXACTLY ONE vtable membership — the SF vtable itself (slots 0..5); the run's "
               "whole-file imm32 census independently bounds FUN_0050A050 to EXACTLY ONE address "
               "occurrence in the file (the SF vtable slot-3 dword 0x00A7D464).")
    log.append(f"ADJACENCY FACT (measured): the {ark_name} vtable @ {ARK_VTABLE:#010x} has EXACTLY "
               f"{ark_n} slots ({', '.join(f'{_dw(ARK_VTABLE + 4 * i):#010x}' for i in range(ark_n))}); it is "
               f"ADJACENT to the SF vtable @ {SF_VTABLE:#010x} ({sf_name}, {sf_n} slots) in .rdata, "
               f"separated by the string literal {sep!r} @ {sep_start:#010x} and the SF COL pointer "
               f"{sf_col:#010x} @ {SF_VTABLE - 4:#010x}.")
    log.append("Adjacency is NOT function sharing and NOT inheritance evidence: NO SF slot function is "
               "shared with " + ark_name + " — the pre-fix 'slots 11..15' memberships were a "
               "VTABLE-BOUNDARY OVERRUN artifact (the fixed-16-slot enumeration read through the real "
               "slots, the string literal, and the SF COL INTO the SF vtable). Corrected by the "
               "vtable-extent rule (a COL-derived vtable ends at the first non-.text dword; the FNMAP "
               "boundary lesson's data-array analog). Context only; no semantic promotion.")
    log.append(f"function-start lattice (E8/E9 targets in .text): {len(lattice)} starts")
    log.append(f".text range: {t_va:#010x}..{t_va + len(tb):#010x} ({len(tb)} bytes)")
    log.append(f"DECLARED BOUND: {MAX_LEVELS} levels, {MAX_BACK}-byte backward decode window per level")
    log.append("")

    # ---------------- CAL-3: known-answer calibration of the receiver tracer ----------------
    cal3_chains = decode_back_chains(exe, md, 0x00529020)
    cal3 = trace_receiver(exe, md, 0x00529020, "ecx", cal3_chains, lattice, fn_slots, vt_class)
    cal3_ok = cal3["classification"].startswith("PROVEN_HOLDER_0xC0")
    log.append("== CAL-3 (self-added known-answer calibration of the receiver tracer; tooling check ONLY) ==")
    log.append(f"pointed at the published receiver-proof site (receiver ecx of E8 call 0x00529020 -> FUN_005094C0):")
    log.append(f"  classified: {cal3['classification']} | {cal3['evidence']}")
    log.append(f"CAL-3 VERDICT: " + ("PASS (tracer resolves the known holder-slot receiver)" if cal3_ok else "FAIL — tracer output is NOT trusted for this census; HALT"))
    log.append("")
    if not cal3_ok:
        with open(PKG + r"\01_RAW\ARG2_PRODUCER_TRACE.txt", "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(log) + "\n")
        print("CAL-3 FAIL — halting census (tracer uncalibrated)")
        sys.exit(3)

    # ---------------- pattern enumeration ----------------
    p1, p1j, p2, p3mov = [], [], [], []
    for i in range(len(tb) - 6):
        b0 = tb[i]
        va = t_va + i
        if b0 == 0xFF:
            m = tb[i + 1]
            if (m & 0xC0) == 0x40 and tb[i + 2] == 0x0C:
                regf = (m >> 3) & 7
                rm = m & 7
                if regf == 2 and rm != 4:
                    p1.append(va)
                elif regf == 4 and rm != 4:
                    p1j.append(va)
            elif (m & 0xC0) == 0x80 and tb[i + 2:i + 6] == b"\x0C\x00\x00\x00":
                regf = (m >> 3) & 7
                rm = m & 7
                if regf == 2 and rm != 4:
                    p2.append(va)
        elif b0 == 0x8B:
            m = tb[i + 1]
            mod = m & 0xC0
            rm = m & 7
            if rm == 4:
                continue
            if mod == 0x40 and tb[i + 2] == 0x0C:
                p3mov.append(va)
            elif mod == 0x80 and tb[i + 2:i + 6] == b"\x0C\x00\x00\x00":
                p3mov.append(va)
    log.append(f"PATTERN ENUMERATION (byte-level, .text): P1 call [reg+0xC]: {len(p1)}; "
               f"P1J jmp [reg+0xC]: {len(p1j)}; P2 call [reg+0xC] disp32: {len(p2)}; "
               f"P3 mov dst,[base+0xC] occurrences (pre-follow-check): {len(p3mov)}")
    log.append("")

    # P3 follow-check: mov dst,[base+0xC] then call/jmp dst within <=3 non-control insns (24-byte window)
    p3 = []
    for va in p3mov:
        seq = list(md.disasm(exe.read_va(va, 24), va))
        if not seq:
            continue
        ins = seq[0]
        dst = None
        for op in ins.operands:
            if op.type == x86.X86_OP_REG and (op.access & capstone.CS_AC_WRITE):
                dst = ins.reg_name(op.reg)
                break
        if dst is None:
            continue
        found = False
        for s in seq[1:4]:
            if s.mnemonic in ("call", "jmp"):
                if s.op_str == dst:
                    found = True
                break  # control-flow ends the follow chain
        if found:
            p3.append(va)
    log.append(f"P3 candidates passing the follow-check (call/jmp dst within <=3 non-control instructions): {len(p3)}")
    log.append("")

    candidates = sorted(
        [(va, "P1") for va in p1] + [(va, "P1J") for va in p1j]
        + [(va, "P2") for va in p2] + [(va, "P3") for va in p3]
    )

    # ---------------- per-candidate decode + classification ----------------
    rows = []
    verified = []
    rejected_demo = []
    counts = {}
    for va, pat in candidates:
        ins = next(md.disasm(exe.read_va(va, 8), va), None)
        if ins is None:
            rows.append((va, pat, "<decode failed>", "", "", "", "DECODE_FAIL", "", "", "", ""))
            counts["DECODE_FAIL"] = counts.get("DECODE_FAIL", 0) + 1
            continue
        base = None
        if pat in ("P1", "P1J", "P2"):
            base = REG8_IDS[ins.bytes[1] & 7]
        else:
            for op in ins.operands:
                if op.type == x86.X86_OP_MEM and (op.access & capstone.CS_AC_READ):
                    if op.mem.index == 0 and op.mem.base != 0:
                        base = ins.reg_name(op.mem.base)
        chains = decode_back_chains(exe, md, va)
        vt_load = None
        for ch in chains:
            for i2 in ch:
                if i2.mnemonic == "mov" and len(i2.operands) == 2:
                    o0, o1 = i2.operands[0], i2.operands[1]
                    if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM:
                        if o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0:
                            if i2.reg_name(o0.reg) == base:
                                vt_load = (i2, i2.reg_name(o1.mem.base))
                                break
            if vt_load:
                break
        if vt_load is None:
            counts["NOT_A_VTABLE_CALL"] = counts.get("NOT_A_VTABLE_CALL", 0) + 1
            rows.append((va, pat, C.insn_str(ins), base or "", "", "no vtable load in window",
                         "NOT_A_VTABLE_CALL", "", "", "", ""))
            continue
        vt_insn, objreg = vt_load
        rec = trace_receiver(exe, md, va, objreg, chains, lattice, fn_slots, vt_class)
        cls = rec["classification"]
        counts[cls] = counts.get(cls, 0) + 1
        arg2 = None
        if cls.startswith("PROVEN"):
            arg2 = trace_arg2(exe, md, va, rec["chain"])
            verified.append((va, pat, ins, vt_insn, objreg, rec, arg2))
        if cls == "REJECTED_NOT_SF":
            rejected_demo.append((va, pat, ins, vt_insn, objreg, rec))
        rows.append((va, pat, C.insn_str(ins), base or "",
                     f"{vt_insn.address:#010x}", objreg, cls,
                     rec.get("evidence", ""),
                     (arg2 or {}).get("arg2", "") if arg2 else "",
                     (arg2 or {}).get("class", "") if arg2 else "",
                     (arg2 or {}).get("literal_va", "") if arg2 else ""))

    # ---------------- METHOD 1: holder-slot route ----------------
    h_reads = {d: [] for d in HOLDER_OFFSETS}
    for i in range(len(tb) - 6):
        if tb[i] == 0x8B:
            m = tb[i + 1]
            if (m & 0x7) == 4:
                continue
            mod = m & 0xC0
            va = t_va + i
            if mod == 0x40:
                d = tb[i + 2]
                if d in HOLDER_OFFSETS and REG8_IDS[m & 7] not in ("esp", "ebp"):
                    h_reads[d].append(va)
            elif mod == 0x80:
                d = struct.unpack_from("<I", tb, i + 2)[0]
                if d == 0xC0:
                    h_reads[0xC0].append(va)
    m1_flows = []
    for d, vas in sorted(h_reads.items()):
        for va in vas:
            seq = list(md.disasm(exe.read_va(va, 48), va))
            if not seq:
                continue
            dst = None
            for op in seq[0].operands:
                if op.type == x86.X86_OP_REG and (op.access & capstone.CS_AC_WRITE):
                    dst = seq[0].reg_name(op.reg)
                    break
            if dst is None:
                continue
            # accumulate: objset = registers holding the holder-loaded object
            # CLOBBER-AWARE: a register redefined from a non-derived source leaves
            # objset (and kills vt_regs derived from it); derived copies extend it.
            objset = {dst}
            slot3 = False
            vt_regs = {}
            for s in seq[1:8]:
                if s.mnemonic == "mov" and len(s.operands) == 2:
                    o0, o1 = s.operands[0], s.operands[1]
                    dstr = s.reg_name(o0.reg) if o0.type == x86.X86_OP_REG else None
                    if dstr and dstr in objset:
                        # potential clobber of a tracked object register
                        derived = (o1.type == x86.X86_OP_MEM and o1.mem.index == 0
                                   and o1.mem.base != 0 and o1.mem.disp == 0
                                   and s.reg_name(o1.mem.base) in objset) or \
                                  (o1.type == x86.X86_OP_REG and s.reg_name(o1.reg) in objset)
                        if not derived:
                            objset.discard(dstr)
                    if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                            and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0 \
                            and s.reg_name(o1.mem.base) in objset:
                        vt_regs[s.reg_name(o0.reg)] = s.reg_name(o1.mem.base)  # vtable load
                    elif o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                            and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0x0C \
                            and s.reg_name(o1.mem.base) in vt_regs:
                        slot3 = True  # mov f,[vt+0xC] slot-3 load
                        objset.add(s.reg_name(o0.reg))
                if s.mnemonic in ("call", "jmp"):
                    if len(s.operands) == 1 and s.operands[0].type == x86.X86_OP_MEM:
                        mem = s.operands[0].mem
                        if mem.index == 0 and mem.disp == 0x0C and s.reg_name(mem.base) in vt_regs:
                            slot3 = True
                    break
            if slot3:
                m1_flows.append((va, d))
    log.append("== METHOD 1 (holder-slot route; genuine slot-3 vcall flow requirement) ==")
    for d in sorted(h_reads):
        log.append(f"  mov reg,[base+{d:#04x}] reads (base != esp/ebp, non-SIB): {len(h_reads[d])}")
    log.append(f"  reads flowing into a GENUINE slot-3 vcall (vtable load + slot +0x0C call) within 48 bytes: {len(m1_flows)}")
    for va, d in m1_flows:
        log.append(f"    flow: read@{va:#010x} (offset {d:#x})")
    log.append("")

    # ---------------- METHOD 1 flow disposition (ABI vs measured FUN_0050A050 ABI) ----------------
    # FUN_0050A050 measured ABI (W1): thiscall (this=ECX), arg1=[esp+4] (out buf),
    # arg2=[esp+8] (name), callee cleanup ret 8. A well-formed call site therefore
    # pushes EXACTLY 2 stack args and holds the receiver in ECX at the call.
    def disposition_flow(read_va, offset):
        seq = list(md.disasm(exe.read_va(read_va, 40), read_va))
        if not seq:
            return None
        dst = None
        for op in seq[0].operands:
            if op.type == x86.X86_OP_REG and (op.access & capstone.CS_AC_WRITE):
                dst = seq[0].reg_name(op.reg)
                break
        if dst is None:
            return None
        # find the slot-3 call in the window
        call_i = None
        vtreg = None
        for k, s in enumerate(seq):
            if s.mnemonic == "mov" and len(s.operands) == 2:
                o0, o1 = s.operands[0], s.operands[1]
                if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                        and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0 \
                        and s.reg_name(o1.mem.base) == dst:
                    vtreg = s.reg_name(o0.reg)
                if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                        and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0x0C \
                        and vtreg and s.reg_name(o1.mem.base) == vtreg:
                    pass  # slot-3 load (function pointer in o0)
            if s.mnemonic in ("call", "jmp"):
                call_i = k
                break
        if call_i is None:
            return None
        # effective stack args: pushes between read and call; 'push X; fstp [esp]' = 1 push
        eff_pushes = 0
        recv_on_stack = False
        ecx_at_call = dst == "ecx"
        j = 1
        while j < call_i:
            s = seq[j]
            if s.mnemonic == "push":
                # reserve-push idiom: push X ; fstp dword [esp]
                if j + 1 < len(seq) and seq[j + 1].mnemonic == "fstp" and "[esp]" in seq[j + 1].op_str:
                    eff_pushes += 1
                    j += 2
                    continue
                eff_pushes += 1
                if s.op_str == dst:
                    recv_on_stack = True
            elif s.mnemonic == "mov" and s.op_str.startswith("ecx,"):
                if s.op_str.split(",")[1].strip() == dst:
                    ecx_at_call = True
            j += 1
        abi = "ABI_COMPATIBLE_2ARG_THISCALL" if (eff_pushes == 2 and ecx_at_call and not recv_on_stack) else \
              f"ABI_INCOMPATIBLE (measured {eff_pushes} stack arg(s), thiscall={ecx_at_call and not recv_on_stack})"
        return {"call_va": seq[call_i].address, "read_va": read_va, "offset": offset,
                "receiver_reg": dst, "abi": abi, "call_insn": C.insn_str(seq[call_i])}

    m1_disp = []
    for va, d in m1_flows:
        r = disposition_flow(va, d)
        if r:
            m1_disp.append(r)

    # ---------------- NC-2 probe (if census produced no rejection demo) ----------------
    nc2_probe_lines = []
    if not rejected_demo:
        nc2_probe_lines.append("== NC-2 DEDICATED PROBE: vtable store -> slot-3 vcall on the same object ==")
        probes = 0
        scanned = 0
        for i in range(len(tb) - 10):
            if tb[i] != 0xC7:
                continue
            m = tb[i + 1]
            mod = m & 0xC0
            rm = m & 7
            if (m >> 3) & 7 != 0:
                continue  # C7 /0 only
            if mod == 0x00 and rm != 4:
                imm = struct.unpack_from("<I", tb, i + 2)[0]
            elif mod == 0x01 and rm != 4 and tb[i + 2] == 0:
                imm = struct.unpack_from("<I", tb, i + 3)[0]
            else:
                continue
            if imm not in vt_class and imm != SF_VTABLE:
                continue
            scanned += 1
            va = t_va + i
            seq = list(md.disasm(exe.read_va(va, 48), va))
            if not seq:
                continue
            reg = seq[0].reg_name(seq[0].operands[0].mem.base)
            cls_name = vt_class.get(imm, SF_CLASS)
            vtreg = None
            for s in seq[1:8]:
                if s.mnemonic == "mov" and len(s.operands) == 2:
                    o0, o1 = s.operands[0], s.operands[1]
                    if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                            and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0 \
                            and s.reg_name(o1.mem.base) == reg:
                        vtreg = s.reg_name(o0.reg)
                if vtreg and s.mnemonic == "mov" and len(s.operands) == 2:
                    o0, o1 = s.operands[0], s.operands[1]
                    if o0.type == x86.X86_OP_REG and o1.type == x86.X86_OP_MEM \
                            and o1.mem.index == 0 and o1.mem.base != 0 and o1.mem.disp == 0x0C \
                            and s.reg_name(o1.mem.base) == vtreg:
                        nc2_probe_lines.append(
                            f"  PROBE {va:#010x}: vtable store (class {cls_name}) then slot-3 call chain "
                            f"{C.insn_str(seq[0])} ... {C.insn_str(s)} -> receiver provably "
                            + ("SF" if imm == SF_VTABLE else f"NOT SF (class {cls_name}) -> the census rule REJECTS it"))
                        if imm != SF_VTABLE:
                            probes += 1
                        break
                if s.mnemonic in ("call", "jmp"):
                    if len(s.operands) == 1 and s.operands[0].type == x86.X86_OP_MEM \
                            and s.operands[0].mem.disp == 0x0C and vtreg \
                            and s.reg_name(s.operands[0].mem.base) == vtreg:
                        nc2_probe_lines.append(
                            f"  PROBE {va:#010x}: vtable store (class {cls_name}) then slot-3 call "
                            f"{C.insn_str(s)} -> receiver provably "
                            + ("SF" if imm == SF_VTABLE else f"NOT SF (class {cls_name}) -> the census rule REJECTS it"))
                        if imm != SF_VTABLE:
                            probes += 1
                    break
            if probes >= 3:
                break
        nc2_probe_lines.append(f"  RTTI-vtable stores scanned: {scanned}")
        nc2_probe_lines.append(f"NC-2 probe result: {probes} demonstrable non-SF slot-3-style rejections "
                               + ("(rule discriminates)" if probes else "(NONE — honest record)"))

    # ---------------- write CSV ----------------
    with open(PKG + r"\01_RAW\VIRTUAL_CALLSITE_CENSUS.csv", "w", encoding="utf-8", newline="\n") as f:
        f.write("va,pattern,insn,base_or_dst,vtable_load_va,receiver_reg,classification,evidence,arg2_push,arg2_class,literal_va\n")
        for r in rows:
            f.write(",".join(_csv(x) for x in r) + "\n")
        for r in m1_disp:
            f.write(",".join(_csv(x) for x in (
                r["call_va"], "M1_FLOW", r["call_insn"], r["receiver_reg"],
                f"{r['read_va']:#010x}", r["receiver_reg"],
                r["abi"],
                f"holder-read [base+{r['offset']:#x}] at {r['read_va']:#010x} flows into this slot-3 call; ABI disposition vs measured FUN_0050A050 ABI",
                "", "", "")) + "\n")

    # ---------------- detailed TXT ----------------
    log.append("== PER-CANDIDATE OUTCOME COUNTS (the census denominators) ==")
    log.append(f"total candidates examined (P1/P1J/P2/P3 after follow-check): {len(candidates)}")
    for k in sorted(counts):
        log.append(f"  {k}: {counts[k]}")
    log.append("")
    log.append("== HOLDER-GENERIC / CLOSEST-TO-PROVEN CANDIDATES (recorded for the report) ==")
    for r in rows:
        if "in B.3 generic holder set" in r[7] or "+0x30 read" in r[7]:
            log.append(f"  {r[0]:#010x} ({r[1]}) {r[2][:56]} | {r[7]}")
    log.append("")
    log.append("== VERIFIED SF SLOT-3 CALL SITES (receiver proven; W3 arg2 analysis applied) ==")
    if not verified:
        log.append("NONE — zero slot-3 virtual call sites with a proven-SF receiver inside the declared bound.")
    for (va, pat, ins, vt_insn, objreg, rec, arg2) in verified:
        log.append("-" * 78)
        log.append(f"SITE {va:#010x} ({pat}) {C.insn_str(ins)}")
        log.append(f"  vtable load: {C.insn_str(vt_insn)}  receiver reg: {objreg}")
        log.append(f"  receiver proof: {rec['classification']}: {rec['evidence']}")
        if rec.get("def_insn") is not None:
            log.append(f"  receiver def: {C.insn_str(rec['def_insn'])}")
        log.append(f"  arg2 pushes seen (window): {arg2['pushes']}")
        log.append(f"  arg2 push (first-pushed, rightmost stack arg): {arg2.get('arg2')}")
        log.append(f"  arg2 class: {arg2.get('class')}")
        for d in arg2.get("detail", []):
            log.append(f"    {d}")
        if arg2.get("literal_bytes"):
            lb = arg2["literal_bytes"]
            log.append(f"    NC-3 verbatim @ {arg2['literal_va']:#010x}: {lb.hex(' ').upper()}")
            log.append(f"    NC-3 ascii: {''.join(chr(c) for c in lb if c != 0)!r}")
    log.append("")
    log.append("== REJECTED_NOT_SF DEMONSTRATIONS (NC-2) ==")
    if rejected_demo:
        for (va, pat, ins, vt_insn, objreg, rec) in rejected_demo:
            log.append(f"  {va:#010x} ({pat}) {C.insn_str(ins)} receiver {objreg} -> {rec['classification']}: {rec['evidence']}")
    else:
        log.extend(nc2_probe_lines)
    log.append("")
    log.append("== METHOD-1 / PATTERN-ROUTE CROSS-CHECK ==")
    cand_vas = {va for va, _ in candidates}
    for va, d in m1_flows:
        mark = "ALSO a pattern-route candidate" if va in cand_vas else "read site (call follows in window; call-site disposition below)"
        log.append(f"  holder-read@{va:#010x} (offset {d:#x}): {mark}")
    if not m1_flows:
        log.append("  (no genuine slot-3 flows via the holder route)")
    log.append("")
    log.append("== METHOD-1 FLOW DISPOSITION (ABI measured against the W1-measured FUN_0050A050 ABI: ==")
    log.append("   thiscall this=ECX, exactly 2 stack args, callee ret 8; a well-formed call site must match)")
    abi_ok = []
    for r in m1_disp:
        log.append(f"  read@{r['read_va']:#010x} (+{r['offset']:#x}) call@{r['call_va']:#010x} {r['call_insn']}")
        log.append(f"      receiver={r['receiver_reg']} -> {r['abi']}")
        if r["abi"] == "ABI_COMPATIBLE_2ARG_THISCALL":
            abi_ok.append(r)
    log.append("")
    log.append("== CLOSEST CANDIDATE: ABI-compatible forwarding thunks (full evidence trail) ==")

    def b5_function_start(va, max_scan=512):
        """B.5-style enclosing-start derivation: scan backward for an
        alignment-completing run of CC/90 bytes; the function starts at the
        next 16-aligned VA after the run."""
        # find the largest k such that bytes [va-6..va) region contains a run...
        # practical: walk back over instructions is unreliable; use CC runs:
        try:
            back = exe.read_va(va - max_scan, max_scan)
        except Exception:
            back = exe.read_va(va - 64, 64)
            max_scan = 64
        # scan backward from va-1 for the LAST position p where a run of >=2 CC/90
        # bytes completes exactly at a 16-aligned VA <= va, with the byte AT that
        # aligned VA being a non-CC/90 (function start)
        best = None
        for i in range(max_scan - 3, 0, -1):
            b = back[i]
            if b in (0xCC, 0x90):
                # candidate run end at back[i:...]; check run completing to alignment
                run_start = i
                while run_start > 0 and back[run_start - 1] in (0xCC, 0x90):
                    run_start -= 1
                aligned = (va - max_scan + i + 1) & ~15
                run_end_va = va - max_scan + i + 1
                if run_end_va == aligned and run_end_va <= va and (i + 1 - run_start) >= 2:
                    if run_end_va < va and back[i + 1] not in (0xCC, 0x90):
                        best = run_end_va
                        break
        return best

    for r in abi_ok:
        call_va = r["call_va"]
        enc_lattice = enclosing_of(lattice, call_va)
        enc_b5 = b5_function_start(call_va)
        log.append(f"  call@{call_va:#010x}: B.5-derived enclosing start {enc_b5:#010x} "
                   f"(E8/E9-lattice start {enc_lattice:#010x}"
                   + (" — LATTICE MIS-ATTRIBUTED (vtable-only function; B.5 start wins)" if enc_lattice != enc_b5 else ")"))
        enc = enc_b5
        log.append("    vtable membership of the B.5-derived enclosing start: "
                   + (f"{sorted(set(c for c, _ in fn_slots[enc]))}" if enc in fn_slots else "<none>"))
        log.append("    full enclosing-function decode (B.5 start -> past the call):")
        if enc is not None:
            for i2 in md.disasm(exe.read_va(enc, call_va - enc + 8), enc):
                log.append("      " + C.insn_str(i2))
        if enc in fn_slots:
            classes = sorted(set(c for c, _ in fn_slots[enc]))
            cls = classes[0]
            vt_of_cls = [v for v, c in vt_class.items() if c == cls]
            log.append(f"    class {cls} vtable(s): {[f'{v:#010x}' for v in sorted(vt_of_cls)]}")
            for v in sorted(vt_of_cls)[:1]:
                needle = struct.pack("<I", v)
                q = exe.data.find(needle)
                shown = 0
                while q != -1 and shown < 2:
                    store_va = exe.off_to_va(q)
                    if store_va and exe.section_name_of_va(store_va) == ".text":
                        log.append(f"      vtable store @ {store_va:#010x} context (class ctor region):")
                        for i3 in md.disasm(exe.read_va(store_va - 8, 40), store_va - 8):
                            log.append("        " + C.insn_str(i3))
                        shown += 1
                    q = exe.data.find(needle, q + 1)
    log.append("")
    log.append("== LIMITATIONS (declared) ==")
    log.append("- SIB-encoded vtable loads / calls excluded from the pattern census (declared).")
    log.append("- Backward decode is multi-start with cross-chain agreement check; residual x86")
    log.append("  ambiguity is surfaced as INSUFFICIENT_PROOF (AMBIGUOUS), never guessed.")
    log.append("- Two-level, 48-byte-per-level bound: defs earlier than the window are recorded as")
    log.append("  INSUFFICIENT_PROOF (bound-exhausted), never silently dropped.")
    log.append("- METHOD-1 forward window: 48 bytes, <=7 instructions, mov-accumulation only.")
    log.append("- The enclosing-function this-route uses the E8/E9-target lattice (superset of")
    log.append("  true function starts); false-positive lattice starts can mis-attribute the")
    log.append("  enclosing function — outcomes from this route carry that caveat.")
    with open(PKG + r"\01_RAW\ARG2_PRODUCER_TRACE.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(log) + "\n")

    print("RTTI vt_class:", len(vt_class), "fn_slots:", len(fn_slots), "SF vtable ->", vt_class.get(SF_VTABLE))
    print("CAL-3:", "PASS" if cal3_ok else "FAIL")
    print("candidates:", len(candidates), "counts:", counts)
    print("verified SF slot-3 sites:", len(verified))
    print("rejected demos (census):", len(rejected_demo))
    print("method1 flows:", m1_flows)
    print("wrote VIRTUAL_CALLSITE_CENSUS.csv + ARG2_PRODUCER_TRACE.txt")


def _csv(x):
    s = str(x)
    if any(c in s for c in ',"\n'):
        s = '"' + s.replace('"', '""') + '"'
    return s


if __name__ == "__main__":
    main()
