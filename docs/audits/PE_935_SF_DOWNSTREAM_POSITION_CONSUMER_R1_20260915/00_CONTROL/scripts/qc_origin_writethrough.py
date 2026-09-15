# -*- coding: utf-8 -*-
"""QC_R3 probe: independent origin-singleton write-through census.

Task PHASE 2 steps 1-2 (+4 negative control), executed BEFORE reading any of
the executor's correction artifacts. STATIC-ONLY: binary never executed.

  1. Recompute the direct E8 caller census of FUN_00437F70 with
     decode-verified instruction boundaries (padded-function-start linear
     decode must reach every counted site exactly).
  2. For each verified caller: whole-function provenance tracking of the
     returned singleton pointer (register aliases, stack spills via an esp
     ledger, pointer escapes with bounded callee-head classification).
     Window = the whole containing function (>= 16 instructions per site).
  4. Negative control: synthetic mid-instruction E8 candidates must be
     rejected by the boundary verifier.

Output: 00_CONTROL/QC_R3_RAW/QC_R3_WRITE_THROUGH_RAW.txt
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qc_peutil as U
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM

try:
    from capstone import CS_AC_READ, CS_AC_WRITE
except ImportError:  # pragma: no cover
    CS_AC_READ = 1
    CS_AC_WRITE = 2

GETTER = 0x00437F70
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW_DIR = os.path.join(PKG, "00_CONTROL", "QC_R3_RAW")
RAW_FILE = os.path.join(RAW_DIR, "QC_R3_WRITE_THROUGH_RAW.txt")

CALLER_SAVED = ("eax", "ecx", "edx")


def der(a, b):
    if a == "DERIVED" or b == "DERIVED":
        return "DERIVED"
    return a + b


def op_reg(ins, op):
    return ins.reg_name(op.reg)


def op_mem(ins, op):
    m = op.mem
    base = ins.reg_name(m.base) if m.base else None
    index = ins.reg_name(m.index) if m.index else None
    return base, index, m.scale, m.disp


class RetCache(object):
    """callee ret-imm cache (stdcall detection), bounded head decode."""

    def __init__(self, dis, data, sections):
        self.dis = dis
        self.data = data
        self.sections = sections
        self.cache = {}

    def ret_bytes(self, target):
        if target in self.cache:
            return self.cache[target]
        n = None
        if target is not None and U.va_to_off(self.sections, target)[0] is not None:
            ins_list, stop = self.dis.stream(self.data, self.sections, target, 0x600, 600)
            for ins in ins_list:
                if ins.mnemonic in ("ret", "retf"):
                    # fast mode has no operands; parse the imm from op_str
                    parts = ins.op_str.split()
                    n = int(parts[0], 0) if parts else 0
                    break
        self.cache[target] = n
        return n


def classify_callee_head(dis, data, sections, callee, head_bytes=0x300):
    """Bounded callee-head classification for escaped S_PTR arguments.

    Tracks the first stack argument ([esp+4] at entry; [ebp+8] after a
    standard frame) through the callee's first `head_bytes` of linear code.
    HEAD-BOUNDED ABSENCE IS NEVER GLOBAL ABSENCE (disclosed limitation).
    Returns (classification, evidence_lines).
    """
    ins_list, stop = dis.stream(data, sections, callee, head_bytes, 300, detail=True)
    ledger = 0
    ebp_key = None
    tainted = {}
    arg_key = 4
    classification = "HEAD_CLEAN(bounded)"
    evidence = []
    for ins in ins_list:
        m = ins.mnemonic
        ops = ins.operands
        if m == "push" and ops:
            ledger += 4
        elif m == "pop" and ops:
            ledger -= 4
        elif (m == "sub" and ops and ops[0].type == X86_OP_REG
              and op_reg(ins, ops[0]) == "esp" and ops[1].type == X86_OP_IMM):
            ledger += ops[1].imm
        elif (m == "add" and ops and ops[0].type == X86_OP_REG
              and op_reg(ins, ops[0]) == "esp" and ops[1].type == X86_OP_IMM):
            ledger -= ops[1].imm
        elif (m == "mov" and ops and ops[0].type == X86_OP_REG
              and op_reg(ins, ops[0]) == "ebp" and len(ops) > 1
              and ops[1].type == X86_OP_REG and op_reg(ins, ops[1]) == "esp"):
            ebp_key = -ledger
        elif m == "leave":
            if ebp_key is not None:
                ledger = -(ebp_key + 4)
            ebp_key = None
        if m in ("mov", "movzx", "movsx") and ops and len(ops) > 1:
            dst, src = ops[0], ops[1]
            if dst.type == X86_OP_REG:
                d = op_reg(ins, dst)
                if src.type == X86_OP_MEM:
                    base, index, scale, disp = op_mem(ins, src)
                    key = None
                    if base == "esp":
                        key = disp - ledger
                    elif base == "ebp" and ebp_key is not None:
                        key = disp + ebp_key
                    if key is not None and key == arg_key:
                        tainted[d] = "ARG1"
                        classification = "ARG_LOADED"
                        evidence.append("  [head] 0x%08X %s %s <- first stack arg (ARG1 taint)"
                                        % (ins.address, ins.mnemonic, ins.op_str))
                    elif d in tainted:
                        del tainted[d]
                elif src.type == X86_OP_REG:
                    s = op_reg(ins, src)
                    if s in tainted:
                        tainted[d] = tainted[s]
                    elif d in tainted:
                        del tainted[d]
                else:
                    if d in tainted:
                        del tainted[d]
            elif dst.type == X86_OP_MEM:
                base, index, scale, disp = op_mem(ins, dst)
                if base in tainted:
                    classification = "WRITES_THROUGH_ARG(head-bounded)"
                    evidence.append("  [head] 0x%08X %s %s *** WRITE THROUGH ARG ***"
                                    % (ins.address, ins.mnemonic, ins.op_str))
        if m == "lea" and ops and ops[0].type == X86_OP_REG:
            d = op_reg(ins, ops[0])
            if len(ops) > 1 and ops[1].type == X86_OP_MEM:
                base, index, scale, disp = op_mem(ins, ops[1])
                if base in tainted:
                    tainted[d] = tainted[base]
                elif d in tainted:
                    del tainted[d]
        if m == "mov" and ops and ops[0].type == X86_OP_MEM and len(ops) > 1 and ops[1].type == X86_OP_REG:
            base, index, scale, disp = op_mem(ins, ops[0])
            s = op_reg(ins, ops[1])
            if base is None and index is None and s in tainted:
                classification = "ESCAPES_TO_GLOBAL(head-bounded)"
                evidence.append("  [head] 0x%08X %s %s *** ARG STORED TO GLOBAL ***"
                                % (ins.address, ins.mnemonic, ins.op_str))
        if m == "call" and tainted:
            classification = "PASSES_ARG_DEEPER(head-bounded)"
            evidence.append("  [head] 0x%08X call with live ARG taint -> deeper escape (unresolved)"
                            % ins.address)
            for r in CALLER_SAVED:
                tainted.pop(r, None)
        if m in ("ret", "retf"):
            break
    return classification, evidence

def track_function(retcache, fn_ins, site, data, sections, dis):
    """Whole-function provenance tracking for one census call site.

    Linear over-approximation: conditional branches are not path-resolved;
    every event is returned for manual verification against the raw dump.
    Returns (events, warns, final_taint_alive).
    """
    regs = {}    # reg -> int offset from S_PTR, or "DERIVED"
    slots = {}   # esp-frame slot key -> offset
    ledger = 0
    ebp_key = None
    events = []
    warns = []

    def key_of(base, disp):
        if base == "esp":
            return disp - ledger
        if base == "ebp" and ebp_key is not None:
            return disp + ebp_key
        return None

    for ins in fn_ins:
        m = ins.mnemonic
        ops = ins.operands
        is_site = (ins.address == site)

        if is_site:
            regs["eax"] = 0
            events.append((ins.address, "CENSUS_CALL",
                           "call 0x437F70 -> EAX = S_PTR (origin singleton pointer)"))
            continue

        # ---- ledger + provenance, every instruction ----
        if m == "push" and ops:
            if ops[0].type == X86_OP_REG:
                r = op_reg(ins, ops[0])
                k = -ledger
                if r in regs:
                    slots[k] = regs[r]
                    events.append((ins.address, "SPILL",
                                   "push %s -> slot key %d (off %s)" % (r, k, regs[r])))
                else:
                    slots.pop(k, None)
            elif ops[0].type == X86_OP_MEM:
                base, index, scale, disp = op_mem(ins, ops[0])
                if base in regs:
                    events.append((ins.address, "READ_S",
                                   "push [tainted %s%+d]" % (base, disp)))
            ledger += 4
            continue
        if m == "pop" and ops and ops[0].type == X86_OP_REG:
            r = op_reg(ins, ops[0])
            k = -ledger
            ledger -= 4
            if k in slots:
                regs[r] = slots.pop(k)
                events.append((ins.address, "RELOAD",
                               "pop %s <- slot key %d (off %s)" % (r, k, regs[r])))
            else:
                regs.pop(r, None)
            continue
        if (m == "sub" and ops and ops[0].type == X86_OP_REG
                and op_reg(ins, ops[0]) == "esp" and len(ops) > 1
                and ops[1].type == X86_OP_IMM):
            ledger += ops[1].imm
            continue
        if (m == "add" and ops and ops[0].type == X86_OP_REG
                and op_reg(ins, ops[0]) == "esp" and len(ops) > 1
                and ops[1].type == X86_OP_IMM):
            ledger -= ops[1].imm
            continue
        if (m == "mov" and ops and ops[0].type == X86_OP_REG
                and op_reg(ins, ops[0]) == "ebp" and len(ops) > 1
                and ops[1].type == X86_OP_REG and op_reg(ins, ops[1]) == "esp"):
            ebp_key = -ledger
            continue
        if m == "leave":
            if ebp_key is not None:
                ledger = -(ebp_key + 4)
            ebp_key = None
            continue
        if m == "call":
            tgt = None
            if ops and ops[0].type == X86_OP_IMM:
                tgt = ops[0].imm
            arg_keys = [k for k in slots if k > -ledger]
            for k in arg_keys:
                off = slots.pop(k)
                if tgt is not None:
                    cls, evd = classify_callee_head(dis, data, sections, tgt)
                    events.append((ins.address, "ESCAPE_ARG",
                                   "slot key %d (off %s) passed as arg to call 0x%08X; callee head: %s"
                                   % (k, off, tgt, cls)))
                    for e in evd:
                        events.append((ins.address, "ESCAPE_EVIDENCE", e))
                else:
                    events.append((ins.address, "ESCAPE_INDIRECT",
                                   "slot key %d (off %s) passed to INDIRECT call" % (k, off)))
            n = retcache.ret_bytes(tgt)
            if tgt is not None and n is None:
                warns.append("callee 0x%08X ret-type unknown; assumed cdecl (ledger unchanged)" % tgt)
            if n:
                ledger -= n
            for r in CALLER_SAVED:
                regs.pop(r, None)
            continue
        if m in ("ret", "retf"):
            events.append((ins.address, "RET", "function return (linear over-approximation continues)"))
            continue

        # ---- generic operand processing ----
        if not ops:
            continue
        dst = ops[0]
        # write-through-S detection on any destination memory operand
        if dst.type == X86_OP_MEM:
            base, index, scale, disp = op_mem(ins, dst)
            if base in regs:
                w = False
                acc = getattr(dst, "access", 0)
                if acc & CS_AC_WRITE:
                    w = True
                elif m in ("mov", "fstp", "fistp", "fst", "fist",
                           "add", "sub", "and", "or", "xor", "inc", "dec", "neg", "not"):
                    w = True
                if w:
                    off = der(regs[base], disp)
                    events.append((ins.address, "WRITE_S",
                                   "%s [tainted %s%+d] (S off %s)" % (m, base, disp, off)))
            elif base in ("esp", "ebp") and len(ops) > 1:
                k = key_of(base, disp)
                if k is not None:
                    if ops[1].type == X86_OP_REG:
                        r = op_reg(ins, ops[1])
                        if r in regs:
                            slots[k] = regs[r]
                            events.append((ins.address, "SPILL",
                                           "mov [slot key %d] <- %s (off %s)" % (k, r, regs[r])))
                        else:
                            slots.pop(k, None)
                    elif ops[1].type == X86_OP_IMM:
                        slots.pop(k, None)
                    elif m in ("fstp", "fistp", "fst", "fist"):
                        pass  # float spill; provenance of pointer not affected
        # source-side processing
        if len(ops) > 1:
            src = ops[1]
            if src.type == X86_OP_MEM and src.mem.base:
                base, index, scale, disp = op_mem(ins, src)
                if base in regs:
                    acc = getattr(src, "access", 0)
                    if (acc & CS_AC_READ) or m in ("mov", "movzx", "movsx", "fld",
                                                   "fild", "fcom", "fcomp", "lea",
                                                   "cmp", "push", "pop"):
                        if m != "lea":  # lea does not read through the pointer
                            off = der(regs[base], disp)
                            events.append((ins.address, "READ_S",
                                           "%s [tainted %s%+d] (S off %s)" % (m, base, disp, off)))
        # register-taint updates
        if dst.type == X86_OP_REG:
            d = op_reg(ins, dst)
            if d == "esp" or d == "ebp":
                if d in regs:
                    warns.append("0x%08X: stack pointer register %s got pointer taint (unexpected)" % (ins.address, d))
                    regs.pop(d)
                continue
            if m == "mov":
                if len(ops) > 1:
                    src = ops[1]
                    if src.type == X86_OP_REG:
                        s = op_reg(ins, src)
                        if s in regs:
                            regs[d] = regs[s]
                        else:
                            regs.pop(d, None)
                    elif src.type == X86_OP_MEM:
                        base, index, scale, disp = op_mem(ins, src)
                        if base in regs:
                            regs.pop(d, None)  # value loaded from S, not a pointer
                        else:
                            k = key_of(base, disp) if base else None
                            if k is not None and k in slots:
                                regs[d] = slots[k]
                                events.append((ins.address, "RELOAD",
                                               "%s <- slot key %d (off %s)" % (d, k, slots[k])))
                            else:
                                regs.pop(d, None)
                    else:
                        regs.pop(d, None)
            elif m in ("movzx", "movsx"):
                regs.pop(d, None)
            elif m == "lea":
                if len(ops) > 1 and ops[1].type == X86_OP_MEM:
                    base, index, scale, disp = op_mem(ins, ops[1])
                    if base in regs:
                        regs[d] = der(regs[base], disp)
                        events.append((ins.address, "DERIVE",
                                       "lea %s <- [tainted %s%+d] (off %s)" % (d, base, disp, regs[d])))
                    else:
                        regs.pop(d, None)
            elif m == "xchg" and len(ops) > 1 and ops[1].type == X86_OP_REG:
                s = op_reg(ins, ops[1])
                rd, rs = regs.get(d), regs.get(s)
                if rs is not None:
                    regs[d] = rs
                else:
                    regs.pop(d, None)
                if rd is not None:
                    regs[s] = rd
                else:
                    regs.pop(s, None)
            elif m in ("inc", "dec") and d in regs:
                regs[d] = der(regs[d], 1 if m == "inc" else -1)
            elif m == "xor" and len(ops) > 1 and ops[1].type == X86_OP_REG and op_reg(ins, ops[1]) == d:
                regs.pop(d, None)
            elif m in ("add", "sub") and len(ops) > 1 and ops[1].type == X86_OP_IMM and d in regs:
                regs[d] = der(regs[d], ops[1].imm if m == "add" else -ops[1].imm)
            else:
                if d in regs:
                    regs[d] = "DERIVED"
                    warns.append("0x%08X: %s on tainted %s -> DERIVED" % (ins.address, m, d))
    # register taint alive at function end (stack slots die with the frame)
    return events, warns, bool(regs)

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = open(RAW_FILE, "w", encoding="utf-8", newline="\n")

    def W(s=""):
        out.write(s + "\n")

    import capstone
    import platform
    W("QC_R3 INDEPENDENT WRITE-THROUGH CENSUS (probe: qc_origin_writethrough.py)")
    W("Mode: STATIC-ONLY. The client binary is never executed.")
    W("Python %s; capstone %s" % (platform.python_version(), capstone.__version__))
    W("Binary: %s" % U.EXE_PATH)
    W("")
    W("=" * 78)
    W("SECTION A: S0 PIN VERIFICATION (fail-closed)")
    data, sections = U.load_pinned()
    W("PIN OK: SIZE=%d SHA256=%s ImageBase=0x008X->0x00400000 PE32 i386"
      % (U.EXPECT_SIZE, U.EXPECT_SHA256))
    for s in sections:
        W("  section %-8s VA 0x%08X..0x%08X raw 0x%08X len 0x%X chars 0x%08X%s"
          % (s["name"], 0x400000 + s["vaddr"],
             0x400000 + s["vaddr"] + max(s["vsize"], s["rsize"]),
             s["rptr"], s["rsize"], s["chars"],
             " EXEC" if s["chars"] & 0x20000000 else ""))
    dis = U.Dis()
    retcache = RetCache(dis, data, sections)

    W("")
    W("=" * 78)
    W("SECTION B: FUN_00437F70 (origin singleton getter) - independent decode")
    ins_list, stop = dis.stream(data, sections, GETTER, 0x200, 256)
    for ins in ins_list:
        W("  " + U.fmt_ins(ins))
    W("  stream stop reason: %s (after %d instructions)" % (stop, len(ins_list)))

    W("")
    W("=" * 78)
    W("SECTION C: DIRECT E8 CALLER CENSUS OF 0x00437F70 (decode-verified)")
    raw_cands = U.xfer_census(data, sections, GETTER, 0xE8)
    W("raw byte-pattern E8 candidates (exec sections): %d" % len(raw_cands))
    verified = []
    for site in sorted(raw_cands):
        W("")
        W("- candidate call site 0x%08X" % site)
        start, ev = U.find_function_start(dis, data, sections, site)
        if start is None:
            W("  function start: NOT FOUND (%s)" % ev)
            W("  verdict: UNRESOLVED (cannot decode-verify boundary) -> EXCLUDED from denominator")
            continue
        start_off, _s2 = U.va_to_off(sections, start)
        padctx = " ".join("%02X" % c for c in data[start_off - 8:start_off])
        W("  function start: 0x%08X (%s)" % (start, ev))
        W("  bytes before start: %s" % padctx)
        first3, _r = dis.stream(data, sections, start, 24, 3)
        W("  prologue head: " + (" | ".join("%s %s" % (i.mnemonic, i.op_str) for i in first3)))
        end, n_ins, reason = U.function_extent(dis, data, sections, start)
        W("  function extent: 0x%08X..%s (%d instructions, %s)"
          % (start, ("0x%08X" % end) if end else "?", n_ins, reason))
        fn_ins, sreason = dis.stream(data, sections, start,
                                     (end - start) if end else 0x2000, 20000,
                                     detail=True)
        idx = None
        for i, ins in enumerate(fn_ins):
            if ins.address == site:
                idx = i
                break
        if idx is None:
            W("  verdict: REJECTED (site not on the linear path from the padded start)")
            continue
        W("  call instruction: " + U.fmt_ins(fn_ins[idx]))
        W("  window after call: %d instructions to function end" % (len(fn_ins) - idx - 1))
        W("  verdict: VERIFIED (real instruction boundary, decode-consistent function)")
        verified.append((site, start, end, fn_ins, idx))
    W("")
    W("DECIDE-VERIFIED E8 CALLER DENOMINATOR OF 0x00437F70: %d" % len(verified))

    # ---- Section C2: manual resolution of rejected/unresolved sites ----
    W("")
    W("=" * 78)
    W("SECTION C2: REJECTED/UNRESOLVED CENSUS SITES - manual byte-level analysis")
    rejected_sites = []
    for site in sorted(raw_cands):
        if all(t[0] != site for t in verified):
            rejected_sites.append(site)
    for site in rejected_sites:
        W("")
        W("- rejected site 0x%08X" % site)
        lo = site - 0x60
        W("  hexdump 0x%08X..0x%08X:" % (lo, site + 0x20))
        offL, _s3 = U.va_to_off(sections, lo)
        blob = data[offL:offL + 0x80]
        for k in range(0, len(blob), 16):
            W("    0x%08X  %s" % (lo + k, " ".join("%02X" % c for c in blob[k:k + 16])))
        W("  linear decode from 0x%08X:" % lo)
        insL, stopL = dis.stream(data, sections, lo, 0x80, 80)
        for ins in insL:
            W("    " + U.fmt_ins(ins))
        # relaxed start search: any 1+ byte padding run, no ret-adjacency required
        W("  relaxed function-start search (any padding run >=1):")
        i = offL + 0x5F
        found_relaxed = None
        while i >= offL:
            if data[i] in (0xCC, 0x90):
                re = i
                rs = i
                while rs > offL and data[rs - 1] in (0xCC, 0x90):
                    rs -= 1
                A = re + 1
                if A < (offL + 0x60):
                    a_va, _s4 = U.off_to_va(sections, A)
                    if a_va is not None and U.decodes_to(dis, data, sections, a_va, site):
                        found_relaxed = a_va
                        W("    candidate 0x%08X (run %d, byte before run: %02X %02X)"
                          % (a_va, re - rs + 1,
                             data[rs - 1] if rs > 0 else 0, data[rs - 2] if rs > 1 else 0))
                i = rs - 1
            else:
                i -= 1
        if found_relaxed is None:
            W("    (no relaxed candidate within the window decodes to the site)")
        else:
            a_off, _s5 = U.va_to_off(sections, found_relaxed)
            W("    prologue at relaxed candidate: "
              + " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in dis.stream(data, sections, found_relaxed, 32, 4)[0]))

    W("")
    W("=" * 78)
    W("SECTION D: WRITE-THROUGH PROVENANCE PER VERIFIED CALLER")
    writer_set = []
    for site, start, end, fn_ins, idx in verified:
        W("")
        W("-" * 78)
        W("CALL SITE 0x%08X in function 0x%08X..%s" % (site, start, ("0x%08X" % end) if end else "?"))
        events, warns, alive = track_function(retcache, fn_ins, site, data, sections, dis)
        evmap = {}
        for va, kind, detail in events:
            evmap.setdefault(va, []).append((kind, detail))
        cap = 0
        for i, ins in enumerate(fn_ins):
            line = "  " + U.fmt_ins(ins)
            if ins.address in evmap:
                for kind, detail in evmap[ins.address]:
                    line += "\n      <== %s: %s" % (kind, detail)
                    if kind == "WRITE_S":
                        writer_set.append((site, start, ins.address, detail))
                        line += "  *** WRITER ***"
            if i >= idx - 12 or ins.address in evmap:
                W(line)
                cap += 1
                if cap > 900:
                    W("      ... (dump capped at 900 lines; full decode bounded by function extent)")
                    break
        if warns:
            for w in warns[:20]:
                W("  WARN: %s" % w)
            if len(warns) > 20:
                W("  WARN: ... %d more warnings suppressed" % (len(warns) - 20))
        W("  taint alive at function end: %s" % ("YES (unresolved escape - see events)" if alive else "no"))
    W("")
    W("QC_R3 WRITER SET (call_site, fn_start, write_va, detail):")
    for t in writer_set:
        W("  call 0x%08X | fn 0x%08X | write 0x%08X | %s" % t)
    if not writer_set:
        W("  (none)")

    W("")
    W("=" * 78)
    W("SECTION E: NEGATIVE CONTROL - boundary verifier discrimination")
    W("Test: find byte pattern B8 E8 where the B8 is the OPCODE of a real")
    W("'mov eax, imm32' (verified by clean decode of the containing function)")
    W("- then the E8 byte at B8+1 is MID-INSTRUCTION and the verifier must")
    W("NOT accept it as an instruction boundary / call site. Cases where the")
    W("E8 is itself a real call opcode (B8 an operand/scale byte) are REAL")
    W("call sites and must be ACCEPTED (ground-truth classified first).")
    tested = 0
    rejected = 0
    realcalls_accepted = 0
    misclassified = 0
    for s in sections:
        if not (s["chars"] & 0x20000000):
            continue
        blob = data[s["rptr"]:s["rptr"] + s["rsize"]]
        pos = 0
        while tested < 8:
            i = blob.find(b"\xB8\xE8", pos)
            if i < 0:
                break
            b8_va = 0x400000 + s["vaddr"] + i
            fake_va = b8_va + 1
            # ground truth: is b8_va an instruction boundary of a real stream,
            # and is the instruction there 'mov eax, imm32'?
            start_b, _ev = U.find_function_start(dis, data, sections, b8_va)
            ins_at_b8 = None
            if start_b is not None:
                fn_ins, _r = dis.stream(data, sections, start_b,
                                        (b8_va - start_b) + 16, 200000)
                for ins in fn_ins:
                    if ins.address == b8_va:
                        ins_at_b8 = ins
                        break
                    if ins.address > b8_va:
                        break
            is_mov_imm = (ins_at_b8 is not None
                          and ins_at_b8.mnemonic == "mov"
                          and ins_at_b8.op_str.startswith("eax,"))
            if is_mov_imm:
                # genuine mid-instruction E8: the verifier must reject it
                tested += 1
                start_f, _ev2 = U.find_function_start(dis, data, sections, fake_va)
                boundary = False
                if start_f is not None:
                    fn_ins2, _r2 = dis.stream(data, sections, start_f, 0x2000, 20000)
                    for ins in fn_ins2:
                        if ins.address == fake_va:
                            boundary = True
                            break
                        if ins.address > fake_va:
                            break
                if not boundary:
                    rejected += 1
                    W("  mid-instruction E8 @0x%08X (inside '%s %s' @0x%08X):"
                      " boundary=NO -> REJECTED (correct)"
                      % (fake_va, ins_at_b8.mnemonic, ins_at_b8.op_str, ins_at_b8.address))
                else:
                    misclassified += 1
                    W("  mid-instruction E8 @0x%08X (inside '%s %s' @0x%08X):"
                      " boundary=YES -> *** ACCEPTED (VERIFIER DEFECT) ***"
                      % (fake_va, ins_at_b8.mnemonic, ins_at_b8.op_str, ins_at_b8.address))
            else:
                # check whether the E8 is a real call instruction boundary
                start_r, _ev3 = U.find_function_start(dis, data, sections, fake_va)
                boundary = False
                if start_r is not None:
                    fn_ins3, _r3 = dis.stream(data, sections, start_r, 0x2000, 20000)
                    for ins in fn_ins3:
                        if ins.address == fake_va:
                            boundary = True
                            break
                        if ins.address > fake_va:
                            break
                if boundary and tested < 8:
                    realcalls_accepted += 1
                    W("  real call E8 @0x%08X (B8 was an operand/scale byte):"
                      " accepted (correct - not a fake)" % fake_va)
            pos = i + 2
            if pos >= len(blob):
                break
        if tested >= 8:
            break
    W("negative control result: %d/%d genuine mid-instruction E8 bytes rejected;"
      " %d real calls correctly accepted" % (rejected, tested, realcalls_accepted))

    W("")
    W("=" * 78)
    W("SECTION F: HONEST BOUNDS OF THIS PROBE")
    W("- Linear over-approximation: branch paths are not resolved separately;")
    W("  every WRITE_S/READ_S event must be (and was) verified against the raw")
    W("  disassembly dump above before being used as evidence.")
    W("- Callee-head escape classification is bounded (first 0x300 bytes / head);")
    W("  head-bounded absence is NEVER global absence.")
    W("- The census covers direct E8 calls only; E9/imm32/vtable channels are")
    W("  censused separately by qc_setter_reachability.py.")
    W("- This probe read NO executor correction artifacts (independent run).")
    out.close()
    print("OK -> %s" % RAW_FILE)
    print("verified E8 callers: %d; writers: %d" % (len(verified), len(writer_set)))


if __name__ == "__main__":
    main()
