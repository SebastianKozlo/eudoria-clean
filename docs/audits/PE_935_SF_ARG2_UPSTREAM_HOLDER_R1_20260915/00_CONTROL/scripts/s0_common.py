"""
s0_common.py - shared S0 identity + PE + RTTI + B.5 boundary + backward-slice engine
RUN: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
Contract: docs/audits/PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915/00_CONTROL/RUN_CONTRACT.md
Source of truth: D:/Eudoria_Reconstruction/pcg_install/Entropia.exe physical bytes
(NEVER executed; STATIC-ONLY run).

G0 FAIL-CLOSED: require_identity() re-measures size+SHA256+PE layout and raises
IdentityError on any pin mismatch. Every generator script calls it FIRST.

B.5 ITERATIVE TERMINAL+PADDING RULE (formalized for this run from the contract):
  - A function START is: (a) a supplied anchor VA, or (b) the first non-padding byte
    following a padding run that follows a control terminal, or (c) the byte
    immediately after a control terminal when no padding follows (TIGHT boundary).
  - Padding run = consecutive bytes each equal to 0xCC or 0x90.
  - CONTROL TERMINAL = ret / ret imm16 / jmp (all forms) / retf / iretd / hlt / ud2 / int3
    (standalone CC is padding in this binary, not a mid-code instruction).
  - EXTENT = [start, end of first terminal]; iterate to the next start.
  - Decode failure = DESYNC: scan forward for a padding run of >= 4 pad bytes,
    resume after it, record a RESYNC event.
  - Attribution: a row belongs to the latest function start at or before it.

BACKWARD DEF-SLICE (declared bound, contract 7(iv)):
  - WINDOW = 384 bytes backward per level; LEVELS = 4 (each memory-deref,
    call-cross, or caller-cross hop consumes a level; register renames and
    pointer adjustments stay on the same level). A budget's 'max_level' may
    tighten or widen the per-use level bound (widening is DECLARED by the
    invoking generator; see AMEND_LOG_R2 R2-2: the corrected anchor slices
    use 6 levels - the child-ctor call-cross plus operator-new this-cross at
    the deepest Cyclic chain require 2 additional levels).
  - Linear last-def-wins, clobber-aware (calls clobber caller-saved regs);
    alternate earlier defs recorded as ALTERNATE_DEF notes; cmovcc recorded
    as AMBIGUOUS_DEF and scan continues.
  - Multi-start across callee ret-sites (<= 8) and callers (<= 16).
  - Leaves: IMMEDIATE / LEA_ADDR / ZERO / POP / THIS_ENTRY / ENTRY_STATE /
    PARAM(argN, caller-cross) / CALL_RETURN(callee) / OPAQUE_CALL /
    X87_STORE / NARROW_SOURCE / OTHER_WRITE / BOUND_EXHAUSTED / DESYNC /
    NO_FUNCTION / TOO_MANY_CALLERS / CYCLE / BUDGET_EXHAUSTED.
  - INSUFFICIENT_PROOF is recorded on exhaustion; never guessed.

R2 ENGINE FIX (AMEND_LOG_R2 R2-1; QC_AUDIT.md P0-1) - BRANCH-EDGE
AWARENESS, opt-in via edge_ctx (EdgeContext):
  - R1 defect: pseudo-function starts inside name-dispatch constructs are
    branch targets (je -> start = allocation-failure path; jmp -> start+N
    bypasses the first instruction(s)); the R1 function-entry assumption
    read the conditional xor at the block start as the universal register
    def, reporting ZERO where the normal path carries a live child object.
  - Fix: with edge_ctx, a bypassed def becomes a MULTI_PATH node (def path
    + one child per forward-flowing bypass entry, sliced at the entry
    source, same level); a window with no def but external entries becomes
    a MULTI_ENTRY node (one child per entry source); a callee returning its
    thiscall this gets a caller-cross child. Activation is bounded to uses
    inside DECLARED_CONSTRUCTS; all R1 call sites (edge_ctx=None default)
    behave exactly as before.
"""
import hashlib
import struct
import datetime
import capstone
import capstone.x86_const as x86c
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

EXE_PATH = "D:/Eudoria_Reconstruction/pcg_install/Entropia.exe"
PIN_SIZE = 8015872
PIN_SHA256_HEX = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PIN_IMAGEBASE = 0x00400000
PIN_MACHINE = 0x014C
PIN_MAGIC_PE32 = 0x010B
RUN_ID = "PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915"

PAD_BYTES = (0xCC, 0x90)
TERMINALS = ("ret", "jmp", "retf", "iretd", "iret", "hlt", "ud2", "int3")
CALLER_SAVED = ("eax", "ecx", "edx")

SLICE_WINDOW = 384
SLICE_MAX_LEVELS = 4
SLICE_MAX_RET_SITES = 8
SLICE_MAX_CALLERS = 16
SLICE_BUDGET = 64

# ---------------------------------------------------------------------------
# R2 ENGINE FIX (AMEND_LOG_R2 R2-1; QC_AUDIT.md P0-1): branch-edge awareness.
# The R1 slice engine assumed every B.5 pseudo-function start is a true
# function entry (registers fresh at entry; callers == E8 callers). Inside
# name-dispatch constructs this is FALSE: pseudo-function starts are branch
# TARGETS (a conditional je lands at the start = the allocation-failure
# path) and skip-offset entries (an unconditional jmp lands at start+N,
# N>0, BYPASSING the first instruction(s)). The R1 engine therefore read
# the conditional xor at the block start as the universal register def and
# reported ZERO where the normal path carries a live child object.
#
# Edge-awareness is ACTIVATED ONLY for uses whose containing B.5 function
# lies inside a DECLARED CONSTRUCT extent (bounded fix; outside constructs
# the R1 model applies unchanged, preserving all R1-verified slices).
# ---------------------------------------------------------------------------

DECLARED_CONSTRUCTS = [
    (0x006D0ED0, 0x006D265F,
     "ArkAnimation name-dispatch construct (entry 0x006D0ED0, 3 direct E8 "
     "callers 0x0058EFD6/0x0058F19F/0x006D2B1C; factory blocks 0x006D1xxx-"
     "0x006D2xxx; tail begins 0x006D265F)"),
]

# Declared engine bound: edge enumeration covers direct branch edges (E9/EB
# jmp + jcc) whose target lies in the queried range and whose SOURCE is at a
# LOWER address than the bypassed def / window start (forward-flowing
# edges). Backward (loop) edges with source above the use are not
# enumerated (same causal model as R1; declared bound).
import bisect as _bisect


class EdgeContext(object):
    """Branch-edge index for edge-aware backward slices (R2 engine fix).
    branches: list of (src_va, mnemonic, target_va) collected by
    build_text_map(..., branches=[...])."""

    def __init__(self, branches, constructs=None):
        self.by_target = {}
        for (src, mn, tgt) in branches:
            self.by_target.setdefault(tgt, []).append((src, mn))
        self.targets_sorted = sorted(self.by_target)
        for k in self.by_target:
            self.by_target[k].sort()
        self.constructs = constructs if constructs is not None \
            else DECLARED_CONSTRUCTS

    def entries_into(self, lo, hi):
        """Direct branch edges with target in (lo, hi], sorted by
        (target, source). lo EXCLUSIVE, hi INCLUSIVE."""
        out = []
        i = _bisect.bisect_right(self.targets_sorted, lo)
        j = _bisect.bisect_right(self.targets_sorted, hi)
        for k in range(i, j):
            tgt = self.targets_sorted[k]
            for (src, mn) in self.by_target[tgt]:
                out.append((src, mn, tgt))
        out.sort(key=lambda e: (e[2], e[0]))
        return out

    def is_active_for(self, fn_start):
        """Edge-awareness activation: containing function inside a declared
        construct extent (bounded fix)."""
        for (c0, c1, _desc) in self.constructs:
            if c0 <= fn_start < c1:
                return True
        return False


def _fwd_entries(edge_ctx, lo, hi):
    """Edges with target in (lo, hi] AND source < lo (forward-flowing
    external entries only; internal/loop sources excluded by the declared
    bound)."""
    return [(s, mn, t) for (s, mn, t) in edge_ctx.entries_into(lo, hi)
            if s < lo]


class IdentityError(Exception):
    pass


# ---------------------------------------------------------------- identity (G0)

def measure_exe():
    with open(EXE_PATH, "rb") as f:
        data = f.read()
    if data[:2] != b"MZ":
        raise IdentityError("no MZ signature")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew + 2] != b"PE":
        raise IdentityError("no PE signature")
    if data[e_lfanew + 2] != 0 or data[e_lfanew + 3] != 0:
        raise IdentityError("bad PE signature")
    machine, nsec, timestamp = struct.unpack_from("<HHI", data, e_lfanew + 4)
    sizeofopt = struct.unpack_from("<H", data, e_lfanew + 20)[0]
    opt_off = e_lfanew + 24
    magic = struct.unpack_from("<H", data, opt_off)[0]
    imagebase = struct.unpack_from("<I", data, opt_off + 28)[0]
    secs = []
    so = opt_off + sizeofopt
    for _ in range(nsec):
        raw = data[so:so + 40]
        nb = raw[:8]
        cut = nb.find(0)
        name = nb[:cut if cut >= 0 else 8].decode("ascii", "replace")
        vsize, vaddr, rsize, roff = struct.unpack_from("<IIII", raw, 8)
        chars = struct.unpack_from("<I", raw, 36)[0]
        secs.append(dict(name=name, vsize=vsize, vaddr=vaddr, rsize=rsize,
                         roff=roff, chars=chars))
        so += 40
    return dict(data=data, size=len(data),
                sha256=hashlib.sha256(data).hexdigest().upper(),
                machine=machine, nsec=nsec, timestamp=timestamp,
                magic=magic, imagebase=imagebase, sections=secs,
                e_lfanew=e_lfanew)


def s0_line(m):
    return ("S0 PASS: SIZE=%d SHA256=%s PE32 i386 ImageBase=0x%08X"
            % (m["size"], m["sha256"], m["imagebase"]))


def require_identity():
    m = measure_exe()
    errs = []
    if m["size"] != PIN_SIZE:
        errs.append("SIZE %d != PIN %d" % (m["size"], PIN_SIZE))
    if m["sha256"] != PIN_SHA256_HEX:
        errs.append("SHA256 %s != PIN %s" % (m["sha256"], PIN_SHA256_HEX))
    if m["machine"] != PIN_MACHINE:
        errs.append("MACHINE 0x%04X != PIN i386" % m["machine"])
    if m["magic"] != PIN_MAGIC_PE32:
        errs.append("OPT_MAGIC 0x%04X != PE32" % m["magic"])
    if m["imagebase"] != PIN_IMAGEBASE:
        errs.append("IMAGEBASE 0x%08X != PIN 0x%08X" % (m["imagebase"], PIN_IMAGEBASE))
    if errs:
        raise IdentityError("IDENTITY MISMATCH (HARD STOP): " + "; ".join(errs))
    return m, s0_line(m)


# ---------------------------------------------------------------- PE helpers

def section_of_rva(m, rva):
    for s in m["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
            return s
    return None


def section_of_va(m, va):
    return section_of_rva(m, va - m["imagebase"])


def va_to_off(m, va):
    s = section_of_va(m, va)
    if s is None:
        return None
    return s["roff"] + (va - m["imagebase"] - s["vaddr"])


def off_to_va(m, off):
    for s in m["sections"]:
        if s["roff"] <= off < s["roff"] + s["rsize"]:
            return m["imagebase"] + s["vaddr"] + (off - s["roff"])
    return None


def read_va(m, va, n):
    o = va_to_off(m, va)
    if o is None:
        return None
    return m["data"][o:o + n]


def u32_va(m, va):
    b = read_va(m, va, 4)
    if b is None or len(b) < 4:
        return None
    return struct.unpack("<I", b)[0]


def cstr_va(m, va, maxlen=512):
    o = va_to_off(m, va)
    if o is None:
        return None
    end = m["data"].find(0, o, o + maxlen)
    if end < 0:
        return None
    raw = m["data"][o:end]
    if any(c < 0x20 or c > 0x7E for c in raw):
        return None
    return raw.decode("ascii")


def is_exec_section(m, va):
    s = section_of_va(m, va)
    return s is not None and bool(s["chars"] & 0x20000000)


def is_text_va(m, va):
    s = section_of_va(m, va)
    return s is not None and s["name"] == ".text"


def text_section(m):
    for s in m["sections"]:
        if s["name"] == ".text":
            return s
    raise IdentityError("no .text section")


def make_cs():
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail = True
    return cs


def disasm_range(m, cs, va, limit_bytes):
    """Decode instructions from va; returns (insns, err_pos_va).
    err_pos_va = position of first undecodable byte (None if fully decoded).
    Uses a per-process decode cache keyed (va, limit) - capability note:
    cs.disasm() has ~25-35ms fixed per-call setup cost in capstone 5.0.7
    python, so repeated window decodes of the same function are cached."""
    key = (va, limit_bytes)
    cache = m.setdefault("_decode_cache", {})
    if key in cache:
        return cache[key]
    off = va_to_off(m, va)
    if off is None:
        return [], va
    end_off = min(off + limit_bytes, len(m["data"]))
    mv = memoryview(m["data"])[off:end_off]
    insns = []
    last = va
    for insn in cs.disasm(mv, va):
        insns.append(insn)
        last = insn.address + insn.size
    if last == va:
        result = ([], va)
    elif last < va + (end_off - off):
        result = (insns, last)
    else:
        result = (insns, None)
    if len(cache) > 4096:
        cache.clear()
    cache[key] = result
    return result


# ---------------------------------------------------------------- B.5 single function

def b5_function(m, cs, start_va, max_bytes=32768):
    """B.5 extent of one function anchored at start_va."""
    insns, err = disasm_range(m, cs, start_va, max_bytes)
    if not insns:
        return dict(start=start_va, end=start_va, end_kind="error", terminal=None,
                    pad_len=0, next_start=None, insns=[],
                    events=["DECODE_ERROR_AT_0x%08X" % (err if err else start_va)])
    term = None
    for insn in insns:
        if insn.mnemonic in TERMINALS:
            term = insn
            break
    data = m["data"]
    if term is None:
        end = insns[-1].address + insns[-1].size
        if err is not None:
            return dict(start=start_va, end=end, end_kind="error", terminal=None,
                        pad_len=0, next_start=None, insns=insns,
                        events=["NO_TERMINAL_DECODE_ERR_0x%08X" % err])
        return dict(start=start_va, end=end, end_kind="no_terminal", terminal=None,
                    pad_len=0, next_start=None, insns=insns,
                    events=["NO_TERMINAL_WITHIN_%d_BYTES" % max_bytes])
    end = term.address + term.size
    term_off = va_to_off(m, end)
    i = term_off
    while i < len(data) and data[i] in PAD_BYTES:
        i += 1
    pad_len = i - term_off
    kept = insns[: insns.index(term) + 1]
    return dict(start=start_va, end=end, end_kind="pad" if pad_len else "tight",
                terminal=term.mnemonic, pad_len=pad_len,
                next_start=off_to_va(m, i) if pad_len else end,
                insns=kept, events=[])


# ---------------------------------------------------------------- B.5 full .text map

def build_text_map(m, cs, collect=None, census_14=None, max_func_bytes=262144,
                   branches=None):
    """Single-stream B.5 pass over .text (one capstone iterator per region;
    capability note: cs.disasm() has ~25-35ms fixed per-call setup cost in
    capstone 5.0.7 python, so per-function calls are FORBIDDEN in loops).
    Returns (functions, calls, jmps, stats):
      functions: list of dict(start, end, end_kind) sorted by start
      calls: list of (insn_va, target_va) for direct E8 calls
      jmps: list of (insn_va, target_va) for direct E9/EB jumps
      stats: counters dict
    collect: callable(insn, func_start_va) called per CODE instruction
             (padding instructions are NOT collected).
    census_14: optional list; rows for every memory-WRITE operand with
             displacement 0x14 are appended as
             (va, mnemonic, op_str, bytes_hex, func_start, width, base, index, scale).
    branches: optional list; R2 engine fix (AMEND_LOG_R2 R2-1): every direct
             jump-family instruction (E9/EB jmp + ALL conditional jcc with
             IMM targets) is appended as (insn_va, mnemonic, target_va).
             Default None = R1 behavior (branch edges not collected)."""
    t = text_section(m)
    base = m["imagebase"] + t["vaddr"]
    n = t["rsize"]
    data = m["data"]
    tbase = t["roff"]
    mv = memoryview(data)[tbase:tbase + n]
    functions = []
    calls = []
    jmps = []
    stats = dict(pad_ends=0, tight_ends=0, resyncs=0, oversized=0,
                decode_errors=0, insns=0, edge_ends=0, pad_insns=0,
                max_func=0)
    anchor = 0
    while anchor < n:
        state = "code"       # or "pad"
        cur_start = None
        stop_pos = anchor
        any_dec = False
        for insn in cs.disasm(mv[anchor:n], base + anchor):
            any_dec = True
            off = insn.address - base
            end_off = off + insn.size
            stop_pos = end_off
            mn = insn.mnemonic
            if state == "pad":
                if mn == "int3" or mn == "nop":
                    stats["pad_insns"] += 1
                    continue
                state = "code"
                cur_start = None
            if cur_start is None:
                cur_start = off
            if end_off - cur_start > max_func_bytes:
                functions.append(dict(start=base + cur_start, end=base + off,
                                      end_kind="oversized"))
                stats["oversized"] += 1
                cur_start = off
            if collect is not None:
                collect(insn, base + cur_start)
            if census_14 is not None:
                ops = insn.operands
                hit = False
                for op in ops:
                    if op.type == x86c.X86_OP_MEM and op.mem.disp == 0x14:
                        hit = True
                        break
                if hit:
                    for (_oi, wop) in mem_write_ops(insn):
                        if wop.mem.disp == 0x14:
                            breg = insn.reg_name(wop.mem.base) if wop.mem.base else ""
                            ireg = insn.reg_name(wop.mem.index) if wop.mem.index else ""
                            census_14.append((insn.address, mn, insn.op_str,
                                              insn.bytes.hex(), base + cur_start,
                                              wop.size, breg, ireg,
                                              wop.mem.scale))
            stats["insns"] += 1
            if mn in ("call", "jmp"):
                ops = insn.operands
                if ops and ops[0].type == x86c.X86_OP_IMM:
                    tgt = ops[0].imm & 0xFFFFFFFF
                    if mn == "call":
                        calls.append((insn.address, tgt))
                    else:
                        jmps.append((insn.address, tgt))
            if branches is not None and mn.startswith("j"):
                ops = insn.operands
                if ops and ops[0].type == x86c.X86_OP_IMM:
                    branches.append((insn.address, mn, ops[0].imm & 0xFFFFFFFF))
            if mn in TERMINALS:
                j = end_off
                while j < n and data[tbase + j] in PAD_BYTES:
                    j += 1
                pad_len = j - end_off
                functions.append(dict(start=base + cur_start, end=base + end_off,
                                      end_kind=("pad" if pad_len else "tight")))
                if pad_len:
                    stats["pad_ends"] += 1
                    state = "pad"
                else:
                    stats["tight_ends"] += 1
                    state = "code"
                cur_start = None
        if stop_pos >= n:
            if cur_start is not None and any_dec and state == "code":
                functions.append(dict(start=base + cur_start, end=base + stop_pos,
                                      end_kind="edge"))
                stats["edge_ends"] += 1
            anchor = n
            break
        # iterator stopped at invalid bytes (data island)
        stats["decode_errors"] += 1
        stats["resyncs"] += 1
        if cur_start is not None:
            functions.append(dict(start=base + cur_start, end=base + stop_pos,
                                  end_kind="desync"))
        k = stop_pos + 1 if any_dec else anchor + 1
        run = 0
        while k < n:
            if data[tbase + k] in PAD_BYTES:
                run += 1
                if run >= 4:
                    k += 1
                    while k < n and data[tbase + k] in PAD_BYTES:
                        k += 1
                    break
            else:
                run = 0
            k += 1
        anchor = k if k < n else n
    for f in functions:
        if f["end"] - f["start"] > stats["max_func"]:
            stats["max_func"] = f["end"] - f["start"]
    return functions, calls, jmps, stats


def func_containing(functions, va):
    """Binary search: function whose [start, end) contains va. None if not found."""
    lo, hi = 0, len(functions)
    while lo < hi:
        mid = (lo + hi) // 2
        if functions[mid]["start"] <= va:
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    if idx >= 0:
        f = functions[idx]
        if f["start"] <= va < f["end"]:
            return f
    return None


# ---------------------------------------------------------------- RTTI walkers
# 32-bit MSVC RTTI: pointer-based VA fields, COL signature 0 (re-derived here).

def read_col(m, col_va):
    sig = u32_va(m, col_va)
    off = u32_va(m, col_va + 4)
    cd = u32_va(m, col_va + 8)
    ptd = u32_va(m, col_va + 12)
    pchd = u32_va(m, col_va + 16)
    if sig is None or ptd is None or pchd is None:
        return None
    return dict(va=col_va, sig=sig, offset=off, cd_offset=cd,
                p_type_descriptor=ptd, p_class_hierarchy=pchd)


def read_type_descriptor_name(m, td_va):
    name = cstr_va(m, td_va + 8)
    if name is None or not name.startswith(".?"):
        return None
    return name


def read_chd(m, chd_va):
    sig = u32_va(m, chd_va)
    attrs = u32_va(m, chd_va + 4)
    num = u32_va(m, chd_va + 8)
    parr = u32_va(m, chd_va + 12)
    if sig is None or num is None or parr is None or num == 0 or num > 64:
        return None
    bcds = []
    for i in range(num):
        bcd_va = u32_va(m, parr + 4 * i)
        if bcd_va is None:
            return None
        ptd = u32_va(m, bcd_va)
        ncb = u32_va(m, bcd_va + 4)
        mdisp = u32_va(m, bcd_va + 8)
        pdisp = u32_va(m, bcd_va + 12)
        vdisp = u32_va(m, bcd_va + 16)
        battrs = u32_va(m, bcd_va + 20)
        nm = read_type_descriptor_name(m, ptd)
        bcds.append(dict(bcd_va=bcd_va, p_type_descriptor=ptd, name=nm,
                         num_contained=ncb, mdisp=mdisp, pdisp=pdisp,
                         vdisp=vdisp, attributes=battrs))
    return dict(va=chd_va, sig=sig, attributes=attrs, num_bases=num,
                p_base_array=parr, bases=bcds)


# ---------------------------------------------------------------- vtable utilities

def vtable_from_slot(m, slot_va, max_back=1024):
    """Given the VA of a dword that is a vtable member, walk back to the vtable
    start. Returns dict(vtable_start, col_va, col, class_name, slots_before)
    or None."""
    d = slot_va
    for _ in range(max_back):
        p = d - 4
        val = u32_va(m, p)
        if val is None:
            return None
        if is_text_va(m, val) and va_to_off(m, val) is not None:
            d = p
            continue
        col = read_col(m, val)
        if col is not None and col["sig"] == 0:
            nm = read_type_descriptor_name(m, col["p_type_descriptor"])
            if nm:
                start = p + 4
                if start > slot_va:
                    return None
                return dict(vtable_start=start, col_va=val, col=col,
                            class_name=nm, slots_before=(slot_va - start) // 4)
        return None
    return None


def vtable_extent(m, vtable_start, max_slots=512):
    """Extent: consecutive .text code dwords from vtable_start.
    Returns (end_va, entries, stop_reason)."""
    entries = []
    va = vtable_start
    while len(entries) < max_slots:
        val = u32_va(m, va)
        if val is None:
            return va, entries, "edge"
        if not is_text_va(m, val):
            extra = ""
            if is_exec_section(m, val):
                extra = " (EXEC non-.text: %s)" % section_of_va(m, val)["name"]
            return va, entries, ("non_code:" + hex(val) + extra)
        entries.append(val)
        va += 4
    return va, entries, "max"


# ---------------------------------------------------------------- operand helpers


WRITE0_MNEMONICS = ("mov", "add", "or", "adc", "sbb", "and", "sub", "xor", "xchg",
                    "inc", "dec", "not", "neg", "pop", "bts", "btr", "btc",
                    "cmpxchg", "rol", "ror", "rcl", "rcr", "shl", "sal",
                    "shr", "sar")
X87_STORE_MNEMONICS = ("fst", "fstp", "fisttp", "fist", "fistp")


def mem_write_ops(insn):
    """List of (index, op) of MEM operands written by this instruction.
    ARCHITECTURAL OVERRIDE (capability probe finding, IDENTITY_VERIFICATION.txt
    [3]): capstone 5.0.7 x86 access misreports x87 STORE forms (fstp [mem])
    as READ=0x1; x87 stores ALWAYS write their mem operand, so
    X87_STORE_MNEMONICS are forced to WRITE before any access check.
    Otherwise capstone access is primary (2=WRITE, 1=READ, 3=RM);
    access==0/NA falls back to the declared conservative WRITE0 map."""
    out = []
    for i, op in enumerate(insn.operands):
        if op.type != x86c.X86_OP_MEM:
            continue
        if insn.mnemonic in X87_STORE_MNEMONICS:
            out.append((i, op))
            continue
        acc = None
        try:
            acc = op.access
        except AttributeError:
            acc = None
        if acc is not None and acc != 0:
            if acc & 2:
                out.append((i, op))
            continue
        mn = insn.mnemonic
        if mn.startswith("mov") and mn not in ("movzx", "movsx", "movsxd") \
                and i == 0:
            out.append((i, op))
            continue
        if mn in WRITE0_MNEMONICS and i == 0:
            out.append((i, op))
    return out


def mem_key_of(insn, op):
    base = insn.reg_name(op.mem.base) if op.mem.base else None
    idx = insn.reg_name(op.mem.index) if op.mem.index else None
    scale = op.mem.scale
    return (base, idx, scale, op.mem.disp)


# ---------------------------------------------------------------- backward slice

class SliceNode(object):
    def __init__(self, kind, detail, level, context):
        self.kind = kind
        self.detail = detail
        self.level = level
        self.context = context
        self.children = []


def _fmt(n, depth=0):
    lines = []
    pad = "  " * depth
    lines.append("%s[L%d] %s: %s" % (pad, n.level, n.kind, n.detail))
    for c in n.children:
        lines.extend(_fmt(c, depth + 1))
    return lines


def format_slice_tree(root):
    return chr(10).join(_fmt(root))


def _window_before(m, cs, functions, va):
    fn = func_containing(functions, va)
    if fn is None:
        return None, None
    insns, err = disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
    if err is not None and not insns:
        return fn, None
    win_lo = max(fn["start"], va - SLICE_WINDOW)
    window = [i for i in insns if win_lo <= i.address < va]
    window.reverse()
    return fn, window


def _classify_reg_def(m, cs, functions, calls, insn, reg, level,
                      visited, budget, edge_ctx):
    """Classify one full-width register def (the R1 classification, factored
    out so the R2 edge-aware wrapper can wrap it in a MULTI_PATH node).
    Returns the classification child node, or None for a no-op def
    (mov reg,reg) which lets the caller continue scanning."""
    mn = insn.mnemonic
    ops = insn.operands
    if mn == "mov":
        src = ops[1]
        if src.type == x86c.X86_OP_IMM:
            return SliceNode("IMMEDIATE",
                "imm 0x%08X at 0x%08X" % (src.imm & 0xFFFFFFFF, insn.address), level, "")
        if src.type == x86c.X86_OP_REG:
            reg2 = insn.reg_name(src.reg)
            if reg2 == reg:
                return None
            child = slice_reg(m, cs, functions, calls, insn.address, reg2,
                              level, visited, budget, edge_ctx)
            child.detail = ("reg rename %s <- %s at 0x%08X" % (reg, reg2, insn.address))
            return child
        if src.type == x86c.X86_OP_MEM:
            key = mem_key_of(insn, src)
            child = slice_mem(m, cs, functions, calls, insn.address, key,
                              level + 1, visited, budget, edge_ctx)
            child.detail = ("load %s <- mem%s at 0x%08X"
                            % (reg, _key_str(key), insn.address))
            return child
    if mn == "lea":
        op = ops[1]
        key = mem_key_of(insn, op)
        base_s = key[0] if key[0] else "abs"
        return SliceNode("LEA_ADDR",
            "lea %s <- [%s%+d] at 0x%08X" % (reg, base_s, key[3], insn.address), level, "")
    if mn == "pop":
        return SliceNode("POP", "pop %s at 0x%08X" % (reg, insn.address), level, "")
    if mn in ("add", "sub") and ops[1].type == x86c.X86_OP_IMM:
        child = slice_reg(m, cs, functions, calls, insn.address, reg,
                          level, visited, budget, edge_ctx)
        child.detail = ("%s %s, 0x%X at 0x%08X (pointer-adjust; tracking base)"
                        % (mn, reg, ops[1].imm & 0xFFFFFFFF, insn.address))
        return child
    if mn in ("and", "or", "xor") and ops[1].type == x86c.X86_OP_REG \
            and insn.reg_name(ops[1].reg) == reg:
        return SliceNode("ZERO", "%s %s, %s at 0x%08X (zero)"
                        % (mn, reg, reg, insn.address), level, "")
    if mn.startswith("cmov"):
        return SliceNode("AMBIGUOUS_DEF",
            "%s defines %s at 0x%08X (conditional; scanning further)" % (mn, reg, insn.address), level, "")
    if mn in ("movzx", "movsx"):
        return SliceNode("NARROW_SOURCE",
            "%s defines %s from narrow source at 0x%08X" % (mn, reg, insn.address), level, "")
    return SliceNode("OTHER_WRITE",
        "%s writes %s at 0x%08X" % (mn, reg, insn.address), level, "")


def slice_reg(m, cs, functions, calls, va, reg, level, visited, budget,
              edge_ctx=None):
    """Backward def-slice of a 32-bit register at va (va = address of the use).
    budget may carry 'max_level' to tighten the declared 4-level bound.
    edge_ctx (R2 ENGINE FIX, AMEND_LOG_R2 R2-1; QC_AUDIT.md P0-1): when
    provided, the slice runs under the R2 ENGINE MODEL:
      - test/cmp are READS everywhere (they write flags only; the R1 model
        misclassified them as OTHER_WRITE defs, terminating chains at
        allocation tests before the defining call);
      - BRANCH-EDGE AWARENESS inside declared constructs: when a register
        def D is found, direct branch edges (jcc/E9/EB) with target in
        (D.address, va] and source < D.address BYPASS D: the slice becomes a
        MULTI_PATH node with the def's own path (annotated with its entry
        preconditions) plus one child per distinct bypass entry, sliced at
        the entry's source (same level; cycle- and budget-guarded); when NO
        def exists in the window, external entries into [fn.start, va] make
        the window a branch-target entry set (one child per entry source,
        plus the conditional-terminal fall-through path); a callee whose
        return value traces to its thiscall THIS at entry gets a
        caller-cross child (ECX at the call site).
    With edge_ctx=None (the default at every R1 call site) the R1 model
    applies UNCHANGED."""
    if level > budget.get("max_level", SLICE_MAX_LEVELS):
        return SliceNode("BOUND_EXHAUSTED", "level>%d (declared budget cap)"
                         % budget.get("max_level", SLICE_MAX_LEVELS), level, "")
    node = SliceNode("REG", "track %s used at 0x%08X" % (reg, va), level, "")
    fn, window = _window_before(m, cs, functions, va)
    if fn is None:
        node.children.append(SliceNode("NO_FUNCTION", "va 0x%08X not in a B.5 function" % va, level, ""))
        return node
    if window is None:
        node.children.append(SliceNode("DESYNC", "function 0x%08X decode error" % fn["start"], level, ""))
        return node
    active = edge_ctx is not None and edge_ctx.is_active_for(fn["start"])
    node.detail = ("track %s used at 0x%08X in func 0x%08X window[%08X..%08X)"
                   % (reg, va, fn["start"], max(fn["start"], va - SLICE_WINDOW), va))
    for insn in window:
        if edge_ctx is not None and insn.mnemonic in ("test", "cmp"):
            # R2 engine model (active whenever edge_ctx is passed, i.e. the
            # caller opted into the R2 model; R1 call sites with edge_ctx=None
            # keep the R1 behavior): test/cmp READ their register operands
            # (they write flags only); the R1 model misclassified them as
            # OTHER_WRITE defs, terminating chains at allocation tests
            # before the defining call or the arg load.
            continue
        if insn.mnemonic == "push":
            # push REG reads the register; it does NOT define it
            continue
        if insn.mnemonic == "call":
            if reg in CALLER_SAVED:
                ops = insn.operands
                if ops and ops[0].type == x86c.X86_OP_IMM:
                    callee = ops[0].imm & 0xFFFFFFFF
                    key = ("ret", callee)
                    if key in visited:
                        outcome = budget.get("ret_outcome", {}).get(callee)
                        if outcome == "NO_RET":
                            node.children.append(SliceNode("ALLOCATION_REVISIT",
                                "callee 0x%08X (operator-new-style import thunk, "
                                "no ret in B.5 extent) already traced in this "
                                "slice; this call site is a DISTINCT fresh "
                                "allocation of the same leaf class" % callee, level, ""))
                            return node
                        node.children.append(SliceNode("CYCLE", "callee 0x%08X already visited" % callee, level, ""))
                        return node
                    visited.add(key)
                    budget["n"] += 1
                    if budget["n"] > SLICE_BUDGET:
                        node.children.append(SliceNode("BUDGET_EXHAUSTED", "path budget exceeded", level, ""))
                        return node
                    child = trace_callee_return(m, cs, functions, calls, callee,
                                                level + 1, visited, budget,
                                                edge_ctx=edge_ctx,
                                                call_site=insn.address)
                    outcome_kind = child.kind
                    if child.children:
                        outcome_kind = child.children[0].kind
                    budget.setdefault("ret_outcome", {})[callee] = outcome_kind
                    child.detail = ("def via call 0x%08X -> callee 0x%08X (caller-saved %s) | %s"
                                    % (insn.address, callee, reg, child.detail))
                    node.children.append(child)
                    return node
                node.children.append(SliceNode("OPAQUE_CALL",
                    "indirect call clobbers %s at 0x%08X" % (reg, insn.address), level, ""))
                return node
            continue
        if not _writes_reg_full(insn, reg):
            if _writes_reg_partial(insn, reg):
                node.children.append(SliceNode("PARTIAL_NOTE",
                    "%s partial-writes %s at 0x%08X" % (insn.mnemonic, reg, insn.address), level, ""))
            continue
        # full-width def of reg found at insn
        if active:
            bypasses = _fwd_entries(edge_ctx, insn.address, va)
            if bypasses:
                # R2: the def is PATH-PRECONDITIONED (branch-target block or
                # bypassed by skip-offset entries). Enumerate BOTH paths.
                mp = SliceNode("MULTI_PATH",
                    "def '%s %s' at 0x%08X is path-preconditioned: %d bypass "
                    "entr%s land in (def, use] (R2 edge-aware; AMEND_LOG_R2 R2-1)"
                    % (insn.mnemonic, reg, insn.address, len(bypasses),
                       "y" if len(bypasses) == 1 else "ies"), level, "")
                pre = [(s, mn, t) for (s, mn, t)
                       in edge_ctx.entries_into(fn["start"] - 1, insn.address)
                       if s < fn["start"]]
                defchild = _classify_reg_def(m, cs, functions, calls, insn, reg,
                                             level, visited, budget, edge_ctx)
                if defchild is None:
                    # no-op def (mov reg,reg): def cannot be the last def after
                    # all - record honestly and keep the bypass paths.
                    defchild = SliceNode("NOOP_DEF",
                        "mov %s, %s at 0x%08X (no-op def)" % (reg, reg, insn.address), level, "")
                else:
                    defchild.detail = ("PATH_DEF (def at 0x%08X; entry precondition%s: "
                                       "%s) | %s"
                                       % (insn.address,
                                          "s" if pre else "",
                                          ", ".join("%s @0x%08X -> 0x%08X" % (mn, s, t)
                                                    for (s, mn, t) in pre) if pre
                                          else "enters at/before the def",
                                          defchild.detail))
                mp.children.append(defchild)
                seen_src = set()
                for (src, mn, tgt) in bypasses:
                    if src in seen_src:
                        continue
                    seen_src.add(src)
                    bkey = ("bypass", src, reg)
                    bseen = budget.setdefault("bypass_seen", set())
                    if bkey in bseen:
                        mp.children.append(SliceNode("CYCLE",
                            "bypass source 0x%08X already visited" % src, level, ""))
                        continue
                    bseen.add(bkey)
                    budget["n"] += 1
                    if budget["n"] > SLICE_BUDGET:
                        mp.children.append(SliceNode("BUDGET_EXHAUSTED",
                            "path budget exceeded", level, ""))
                        break
                    bchild = slice_reg(m, cs, functions, calls, src, reg,
                                       level, visited, budget, edge_ctx)
                    bchild.detail = ("PATH_BYPASS (entry %s @0x%08X -> 0x%08X bypasses "
                                     "the def at 0x%08X; value flows from the entry "
                                     "source) | %s"
                                     % (mn, src, tgt, insn.address, bchild.detail))
                    mp.children.append(bchild)
                node.children.append(mp)
                return node
        child = _classify_reg_def(m, cs, functions, calls, insn, reg,
                                  level, visited, budget, edge_ctx)
        if child is None:
            continue
        node.children.append(child)
        return node
    # no def within window
    if active:
        entries = [(s, mn, t) for (s, mn, t)
                   in edge_ctx.entries_into(fn["start"] - 1, va)
                   if s < fn["start"]]
        # tight FALL-THROUGH path: if the previous B.5 chunk ends exactly at
        # fn.start with a CONDITIONAL terminal, control can fall through
        # into this pseudo-function (the R1 model missed this path).
        fallthrough_term = None
        p0 = func_containing(functions, fn["start"] - 1)
        if p0 is not None and p0["end"] == fn["start"]:
            insns0, _e0 = disasm_range(m, cs, p0["start"],
                                       p0["end"] - p0["start"])
            if insns0 and insns0[-1].mnemonic.startswith("j") \
                    and insns0[-1].mnemonic != "jmp":
                fallthrough_term = insns0[-1]
        if entries or fallthrough_term is not None:
            npaths = len(entries) + (1 if fallthrough_term is not None else 0)
            me = SliceNode("MULTI_ENTRY",
                "no def of %s in window; the window is an entry set: %d external "
                "branch entr%s + %s into [block start, use] (R2 edge-aware; "
                "AMEND_LOG_R2 R2-1)"
                % (reg, len(entries), "y" if len(entries) == 1 else "ies",
                   "1 conditional fall-through path"
                   if fallthrough_term is not None else "0 fall-through paths"), level, "")
            seen_src = set()
            for (src, mn, tgt) in entries:
                if src in seen_src:
                    continue
                seen_src.add(src)
                ekey = ("bypass", src, reg)
                eseen = budget.setdefault("bypass_seen", set())
                if ekey in eseen:
                    me.children.append(SliceNode("CYCLE",
                        "entry source 0x%08X already visited" % src, level, ""))
                    continue
                eseen.add(ekey)
                budget["n"] += 1
                if budget["n"] > SLICE_BUDGET:
                    me.children.append(SliceNode("BUDGET_EXHAUSTED",
                        "path budget exceeded", level, ""))
                    break
                echild = slice_reg(m, cs, functions, calls, src, reg,
                                   level, visited, budget, edge_ctx)
                echild.detail = ("ENTRY_PATH (entry %s @0x%08X -> 0x%08X; value flows "
                                 "from the entry source; no def between entry and "
                                 "use) | %s"
                                 % (mn, src, tgt, echild.detail))
                me.children.append(echild)
            if fallthrough_term is not None and budget["n"] <= SLICE_BUDGET:
                fkey = ("bypass", fallthrough_term.address, reg)
                fseen = budget.setdefault("bypass_seen", set())
                if fkey in fseen:
                    me.children.append(SliceNode("CYCLE",
                        "fall-through source 0x%08X already visited"
                        % fallthrough_term.address, level, ""))
                else:
                    fseen.add(fkey)
                    budget["n"] += 1
                    fchild = slice_reg(m, cs, functions, calls,
                                       fallthrough_term.address, reg,
                                       level, visited, budget, edge_ctx)
                    fchild.detail = ("FALLTHROUGH_PATH (previous chunk ends with "
                                     "conditional %s @0x%08X; the fall-through "
                                     "path enters this block at its start) | %s"
                                     % (fallthrough_term.mnemonic,
                                        fallthrough_term.address, fchild.detail))
                    me.children.append(fchild)
            node.children.append(me)
            return node
    if reg == "ecx":
        node.children.append(SliceNode("THIS_ENTRY",
            "ecx undef in func 0x%08X before 0x%08X: thiscall this at function entry" % (fn["start"], va), level, ""))
        return node
    node.children.append(SliceNode("BOUND_EXHAUSTED",
        "no full-width def of %s within %d-byte window in func 0x%08X" % (reg, SLICE_WINDOW, fn["start"]), level, ""))
    return node


def _key_str(key):
    base, idx, scale, disp = key
    s = "[" + (base if base else "?")
    if idx:
        s += "+" + idx
        if scale > 1:
            s += "*%d" % scale
    s += "%+d]" % disp
    return s


def insn_reg_name_safe(insn, op):
    try:
        if op.type == x86c.X86_OP_REG:
            return insn.reg_name(op.reg)
    except Exception:
        pass
    return None


def _writes_reg_full(insn, reg):
    ops = insn.operands
    if not ops:
        return False
    op0 = ops[0]
    if op0.type == x86c.X86_OP_REG and op0.size == 4:
        return insn.reg_name(op0.reg) == reg
    return False


def _writes_reg_partial(insn, reg):
    LOWMAP = {"al": "eax", "bl": "ebx", "cl": "ecx", "dl": "edx",
              "ah": "eax", "bh": "ebx", "ch": "ecx", "dh": "edx",
              "ax": "eax", "bx": "ebx", "cx": "ecx", "dx": "edx",
              "si": "esi", "di": "edi", "bp": "ebp", "sp": "esp"}
    ops = insn.operands
    if not ops:
        return False
    op0 = ops[0]
    if op0.type == x86c.X86_OP_REG and op0.size in (1, 2):
        return LOWMAP.get(insn.reg_name(op0.reg)) == reg
    return False


def slice_mem(m, cs, functions, calls, va, key, level, visited, budget,
              edge_ctx=None):
    """Backward def-slice of a memory cell (base, disp) READ at va.
    key = (base_name, index_name, scale, disp).
    budget may carry 'max_level' to tighten the declared 4-level bound.
    edge_ctx: R2 pass-through (see slice_reg)."""
    base, idx, scale, disp = key
    if level > budget.get("max_level", SLICE_MAX_LEVELS):
        return SliceNode("BOUND_EXHAUSTED", "level>%d (declared budget cap)"
                         % budget.get("max_level", SLICE_MAX_LEVELS), level, "")
    node = SliceNode("MEM", "track cell %s read at 0x%08X" % (_key_str(key), va), level, "")
    fn, window = _window_before(m, cs, functions, va)
    if fn is None:
        node.children.append(SliceNode("NO_FUNCTION", "va 0x%08X not in a B.5 function" % va, level, ""))
        return node
    if window is None:
        node.children.append(SliceNode("DESYNC", "function 0x%08X decode error" % fn["start"], level, ""))
        return node
    node.detail = ("track cell %s read at 0x%08X in func 0x%08X window[%08X..%08X)"
                   % (_key_str(key), va, fn["start"], max(fn["start"], va - SLICE_WINDOW), va))
    for insn in window:
        wops = mem_write_ops(insn)
        for (_i, wop) in wops:
            wkey = mem_key_of(insn, wop)
            if wkey == key:
                mn = insn.mnemonic
                ops = insn.operands
                if mn == "mov":
                    src = ops[1]
                    if src.type == x86c.X86_OP_IMM:
                        node.children.append(SliceNode("IMMEDIATE",
                            "store imm 0x%08X to %s at 0x%08X"
                            % (src.imm & 0xFFFFFFFF, _key_str(key), insn.address), level, ""))
                        return node
                    if src.type == x86c.X86_OP_REG:
                        reg2 = insn.reg_name(src.reg)
                        child = slice_reg(m, cs, functions, calls, insn.address,
                                          reg2, level, visited, budget, edge_ctx)
                        child.detail = ("store %s <- %s at 0x%08X"
                                        % (_key_str(key), reg2, insn.address))
                        node.children.append(child)
                        return node
                    if src.type == x86c.X86_OP_MEM:
                        node.children.append(SliceNode("OTHER_WRITE",
                            "mem-to-mem via %s at 0x%08X" % (mn, insn.address), level, ""))
                        return node
                if mn in ("fst", "fstp"):
                    node.children.append(SliceNode("X87_STORE",
                        "%s to %s at 0x%08X" % (mn, _key_str(key), insn.address), level, ""))
                    return node
                if mn == "pop":
                    node.children.append(SliceNode("POP",
                        "pop %s at 0x%08X" % (_key_str(key), insn.address), level, ""))
                    return node
                node.children.append(SliceNode("OTHER_WRITE",
                    "%s writes %s at 0x%08X" % (mn, _key_str(key), insn.address), level, ""))
                return node
        # alias risk note: lea reg, [key] present but not a direct writer
        if insn.mnemonic == "lea" and len(insn.operands) > 1 \
                and insn.operands[1].type == x86c.X86_OP_MEM \
                and mem_key_of(insn, insn.operands[1]) == key:
            node.children.append(SliceNode("ALIAS_RISK_NOTE",
                "lea to %s at 0x%08X (alias writes not tracked)" % (_key_str(key), insn.address), level, ""))
    # no direct writer found in window: classify the cell
    if base == "ebp" and disp > 0 and disp % 4 == 0 and disp >= 8:
        arg_index = (disp - 8) // 4
        budget["n"] += 1
        if budget["n"] > SLICE_BUDGET:
            node.children.append(SliceNode("BUDGET_EXHAUSTED", "path budget exceeded", level, ""))
            return node
        child = slice_param(m, cs, functions, calls, fn["start"], arg_index,
                            level + 1, visited, budget, edge_ctx)
        child.detail = "cell %s = stack arg %d of func 0x%08X (caller-cross)" % (_key_str(key), arg_index, fn["start"])
        node.children.append(child)
        return node
    if base == "esp" and disp >= 4 and disp % 4 == 0:
        # esp-relative read: stack ARG if the read sits near function entry with
        # a linearly tracked esp delta (declared heuristic: prologue push/pop and
        # sub/add esp tracked; ANY call/ret/esp-rewrite before the read -> refuse).
        all_insns, _err = disasm_range(m, cs, fn["start"], 0x100000)
        prefix = [i for i in all_insns if i.address < va]
        delta = 0
        ok_track = True
        for i in prefix:
            mn = i.mnemonic
            ops = i.operands
            if mn == "push":
                delta += 4
            elif mn == "pop":
                delta -= 4
            elif mn in ("call", "ret", "iretd", "jmp", "leave", "enter", "hlt",
                        "int3", "ud2", "retf"):
                ok_track = False
                break
            elif mn == "sub" and ops and ops[0].type == x86c.X86_OP_REG \
                    and insn_reg_name_safe(i, ops[0]) == "esp" \
                    and len(ops) > 1 and ops[1].type == x86c.X86_OP_IMM:
                delta += ops[1].imm
            elif mn == "add" and ops and ops[0].type == x86c.X86_OP_REG \
                    and insn_reg_name_safe(i, ops[0]) == "esp" \
                    and len(ops) > 1 and ops[1].type == x86c.X86_OP_IMM:
                delta -= ops[1].imm
            elif ops and ops[0].type == x86c.X86_OP_REG \
                    and insn_reg_name_safe(i, ops[0]) == "esp" \
                    and mn not in ("cmp", "test", "push", "pop"):
                ok_track = False
                break
        if ok_track:
            eff = disp - delta
            if eff >= 4 and eff % 4 == 0:
                arg_index = (eff - 4) // 4
                budget["n"] += 1
                if budget["n"] > SLICE_BUDGET:
                    node.children.append(SliceNode("BUDGET_EXHAUSTED", "path budget exceeded", level, ""))
                    return node
                child = slice_param(m, cs, functions, calls, fn["start"], arg_index,
                                    level + 1, visited, budget, edge_ctx)
                child.detail = ("cell %s at esp-delta %d = stack arg %d of func 0x%08X (esp-entry param heuristic)"
                               % (_key_str(key), delta, arg_index, fn["start"]))
                node.children.append(child)
                return node
        node.children.append(SliceNode("BOUND_EXHAUSTED",
            "esp-relative cell %s with untracked delta (frame cell)" % _key_str(key), level, ""))
        return node
    if base in ("esp", "ebp"):
        node.children.append(SliceNode("BOUND_EXHAUSTED",
            "no direct writer of %s within window (frame cell)" % _key_str(key), level, ""))
        return node
    node.children.append(SliceNode("BOUND_EXHAUSTED",
        "no direct writer of %s within window in func 0x%08X" % (_key_str(key), fn["start"]), level, ""))
    return node


def _tree_has_leaf_kind(node, kind):
    if not node.children:
        return node.kind == kind
    return any(_tree_has_leaf_kind(c, kind) for c in node.children)


def _first_vtable_store(m, cs, fn):
    """First mov [mem], imm in the function whose imm looks like a vtable
    pointer (points at .rdata/.data). Returns (insn_va, imm) or None."""
    insns, err = disasm_range(m, cs, fn["start"], min(fn["end"] - fn["start"],
                                                      8192))
    for i in insns:
        ops = i.operands
        if i.mnemonic == "mov" and len(ops) == 2 \
                and ops[0].type == x86c.X86_OP_MEM and ops[1].type == x86c.X86_OP_IMM:
            v = ops[1].imm & 0xFFFFFFFF
            s = section_of_va(m, v)
            if s is not None and s["name"] in (".rdata", ".data"):
                return (i.address, v)
    return None


def trace_callee_return(m, cs, functions, calls, callee, level, visited,
                        budget, edge_ctx=None, call_site=None):
    """Trace what a direct callee returns in EAX (multi-start over ret sites).
    R2 additions (AMEND_LOG_R2 R2-1; active only when edge_ctx is provided,
    preserving all R1 call sites' behavior):
      - the node is annotated with the callee's first vtable store (class
        identity evidence for constructor call-return leaves);
      - when a ret-site EAX slice terminates at THIS_ENTRY (the callee
        returns its thiscall this), a CALLER-CROSS child slices ECX at the
        call site (call_site must be provided) so the object's provenance
        (e.g. the operator-new allocation) is carried."""
    node = SliceNode("CALL_RETURN", "callee 0x%08X return value" % callee, level, "")
    fn = func_containing(functions, callee)
    if fn is None:
        f2 = b5_function(m, cs, callee)
        if f2["end_kind"] in ("error", "no_terminal"):
            node.children.append(SliceNode("CALLEE_UNDECODEABLE",
                "callee 0x%08X not in map and not B.5-decodable" % callee, level, ""))
            return node
        fn = dict(start=f2["start"], end=f2["end"], end_kind=f2["end_kind"])
    if edge_ctx is not None:
        vts = _first_vtable_store(m, cs, fn)
        if vts is not None:
            node.detail = ("callee 0x%08X return value; callee stores vtable "
                           "0x%08X @0x%08X (class-identity evidence)" % (callee, vts[1], vts[0]))
    insns, err = disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
    if err is not None and not insns:
        node.children.append(SliceNode("DESYNC", "callee decode error", level, ""))
        return node
    rets = [i for i in insns if i.mnemonic == "ret"]
    if not rets:
        node.children.append(SliceNode("NO_RET", "callee has no ret in B.5 extent", level, ""))
        return node
    if len(rets) > SLICE_MAX_RET_SITES:
        node.children.append(SliceNode("TOO_MANY_RET_SITES", "%d ret sites" % len(rets), level, ""))
        return node
    for r in rets:
        child = slice_reg(m, cs, functions, calls, r.address, "eax",
                          level, visited, budget, edge_ctx)
        child.detail = "eax at ret site 0x%08X of callee 0x%08X" % (r.address, callee)
        node.children.append(child)
        if edge_ctx is not None and call_site is not None \
                and _tree_has_leaf_kind(child, "THIS_ENTRY"):
            xchild = slice_reg(m, cs, functions, calls, call_site, "ecx",
                               level, visited, budget, edge_ctx)
            xchild.detail = ("THIS-CROSS: callee returns its thiscall this; "
                             "caller ECX at call site 0x%08X" % call_site)
            child.children.append(xchild)
    return node


def slice_call_arg(m, cs, functions, calls, site_va, arg_index, level, visited,
                   budget, edge_ctx=None):
    """Reconstruct and slice the arg_index-th (0-based) STACK argument of the
    call instruction at site_va. Handles contiguous push sequences and
    [esp+K] write forms; stops at esp-modifying instructions or intervening
    calls (stack-state breakers, recorded honestly).
    edge_ctx: R2 pass-through (see slice_reg)."""
    cnode = SliceNode("CALLSITE_ARG",
                      "arg %d of call at 0x%08X" % (arg_index, site_va), level, "")
    fn, window = _window_before(m, cs, functions, site_va)
    if fn is None or window is None:
        cnode.children.append(SliceNode("NO_FUNCTION",
            "call site 0x%08X not in a B.5-mapped function" % site_va, level, ""))
        return cnode
    pushes_seen = 0
    found = None
    for insn in window:
        mn = insn.mnemonic
        if mn == "call":
            cnode.children.append(SliceNode("BOUND_EXHAUSTED",
                "intervening call at 0x%08X breaks esp state" % insn.address, level, ""))
            found = "stop"
            break
        if mn == "push":
            if pushes_seen == arg_index:
                ops = insn.operands
                if ops and ops[0].type == x86c.X86_OP_REG:
                    r = insn.reg_name(ops[0].reg)
                    child = slice_reg(m, cs, functions, calls, insn.address, r,
                                      level, visited, budget, edge_ctx)
                    child.detail = "arg %d = %s (pushed at 0x%08X)" % (arg_index, r, insn.address)
                    cnode.children.append(child)
                elif ops and ops[0].type == x86c.X86_OP_IMM:
                    cnode.children.append(SliceNode("IMMEDIATE",
                        "arg %d = imm 0x%08X (pushed at 0x%08X)"
                        % (arg_index, ops[0].imm & 0xFFFFFFFF, insn.address), level, ""))
                elif ops and ops[0].type == x86c.X86_OP_MEM:
                    key = mem_key_of(insn, ops[0])
                    child = slice_mem(m, cs, functions, calls, insn.address, key,
                                      level + 1, visited, budget, edge_ctx)
                    child.detail = "arg %d = mem%s (pushed at 0x%08X)" % (arg_index, _key_str(key), insn.address)
                    cnode.children.append(child)
                found = "ok"
                break
            pushes_seen += 1
            continue
        if mn == "pop":
            cnode.children.append(SliceNode("BOUND_EXHAUSTED",
                "pop at 0x%08X breaks esp state" % insn.address, level, ""))
            found = "stop"
            break
        if mn == "mov":
            ops = insn.operands
            if len(ops) == 2 and ops[0].type == x86c.X86_OP_MEM \
                    and ops[1].type in (x86c.X86_OP_REG, x86c.X86_OP_IMM):
                wkey = mem_key_of(insn, ops[0])
                if wkey[0] == "esp" and wkey[1] is None and wkey[2] == 1:
                    slot = (wkey[3] // 4) + pushes_seen
                    if wkey[3] % 4 == 0 and slot == arg_index:
                        if ops[1].type == x86c.X86_OP_REG:
                            r = insn.reg_name(ops[1].reg)
                            child = slice_reg(m, cs, functions, calls, insn.address, r,
                                              level, visited, budget, edge_ctx)
                            child.detail = "arg %d via [esp+0x%X] = %s at 0x%08X" % (arg_index, wkey[3], r, insn.address)
                            cnode.children.append(child)
                        else:
                            cnode.children.append(SliceNode("IMMEDIATE",
                                "arg %d via [esp+0x%X] = imm 0x%08X at 0x%08X"
                                % (arg_index, wkey[3], ops[1].imm & 0xFFFFFFFF, insn.address), level, ""))
                        found = "ok"
                        break
            if len(ops) == 2 and ops[0].type == x86c.X86_OP_REG \
                    and insn.reg_name(ops[0].reg) == "esp":
                cnode.children.append(SliceNode("BOUND_EXHAUSTED",
                    "esp rewritten at 0x%08X" % insn.address, level, ""))
                found = "stop"
                break
            continue
        if mn in ("add", "sub") and insn.operands \
                and insn.operands[0].type == x86c.X86_OP_REG \
                and insn.reg_name(insn.operands[0].reg) == "esp":
            cnode.children.append(SliceNode("BOUND_EXHAUSTED",
                "esp adjusted at 0x%08X" % insn.address, level, ""))
            found = "stop"
            break
    if found is None:
        cnode.children.append(SliceNode("BOUND_EXHAUSTED",
            "arg %d source not found in %d-byte backward window at site 0x%08X"
            % (arg_index, SLICE_WINDOW, site_va), level, ""))
    return cnode


def slice_param(m, cs, functions, calls, func_start, arg_index, level, visited,
                budget, edge_ctx=None):
    """Trace stack argument arg_index (0-based) of function func_start into its
    direct callers (caller-cross).
    edge_ctx: R2 pass-through (see slice_reg)."""
    node = SliceNode("PARAM", "arg %d of func 0x%08X" % (arg_index, func_start), level, "")
    callers = [site for (site, tgt) in calls if tgt == func_start]
    if not callers:
        node.children.append(SliceNode("NO_DIRECT_CALLERS",
            "no direct E8 callers of 0x%08X in lattice" % func_start, level, ""))
        return node
    if len(callers) > SLICE_MAX_CALLERS:
        node.children.append(SliceNode("TOO_MANY_CALLERS",
            "%d direct callers (bound %d)" % (len(callers), SLICE_MAX_CALLERS), level, ""))
        return node
    for site in callers:
        cnode = slice_call_arg(m, cs, functions, calls, site, arg_index,
                               level, visited, budget, edge_ctx)
        cnode.detail = "caller site 0x%08X -> func 0x%08X" % (site, func_start)
        node.children.append(cnode)
    return node


def find_dword_occurrences(m, value):
    """All file offsets whose 4-byte LE equals value. Returns list of
    (offset, va_or_None, aligned4_bool)."""
    pat = struct.pack("<I", value)
    data = m["data"]
    out = []
    pos = 0
    while True:
        i = data.find(pat, pos)
        if i < 0:
            break
        out.append((i, off_to_va(m, i), (i % 4 == 0)))
        pos = i + 1
    return out


# ---------------------------------------------------------------- imports

def parse_imports(m):
    """Parse the import directory (PE32). Returns dict {iat_slot_va: name}.
    IAT slot VA = imagebase + FirstThunk_rva + 4*i (the slot a
    'jmp/call dword ptr [X]' thunk dereferences)."""
    opt_off = m["e_lfanew"] + 24
    imp_rva = struct.unpack_from("<I", m["data"], opt_off + 96 + 8)[0]
    if imp_rva == 0:
        return {}
    out = {}
    desc_va = m["imagebase"] + imp_rva
    for k in range(4096):
        d = read_va(m, desc_va + 20 * k, 20)
        if d is None or len(d) < 20:
            break
        oft, _ts, _fwd, name_rva, first_thunk = struct.unpack_from("<IIIII", d, 0)
        if oft == 0 and first_thunk == 0 and name_rva == 0:
            break
        thunk_rva = oft if oft else first_thunk
        i = 0
        while i < 65536:
            tv = u32_va(m, m["imagebase"] + thunk_rva + 4 * i)
            if tv is None or tv == 0:
                break
            slot_va = m["imagebase"] + first_thunk + 4 * i
            if tv & 0x80000000:
                out[slot_va] = "ORDINAL_%d" % (tv & 0xFFFF)
            else:
                nm = cstr_va(m, m["imagebase"] + tv + 2, 256)
                out[slot_va] = nm if nm else "?"
            i += 1
    return out


def thunk_target_import(m, cs, imports, thunk_va):
    """Decode a small function at thunk_va; if it is 'jmp dword ptr [X]' or
    'jmp [X]' / 'call [X]', resolve X via imports. Returns (insn_str, name)."""
    f = b5_function(m, cs, thunk_va, max_bytes=64)
    if not f["insns"]:
        return (None, None)
    i = f["insns"][0]
    s = i.mnemonic + " " + i.op_str
    for op in i.operands:
        if op.type == x86c.X86_OP_MEM and op.mem.base == 0 and op.mem.index == 0:
            tgt = op.mem.disp & 0xFFFFFFFF
            if tgt in imports:
                return (s, imports[tgt])
            return (s, None)
    return (s, None)


# ---------------------------------------------------------------- COL/vtable inventory

def vtable_inventory(m):
    """Scan .rdata/.data (4-aligned) for COL-pointer dwords; validate that the
    following dwords are .text code pointers. Returns list of dicts
    {col_va, col, class_name, vtable_start} sorted by vtable_start."""
    out = []
    seen = set()
    for s in m["sections"]:
        if s["name"] not in (".rdata", ".data"):
            continue
        start = s["roff"]
        end = s["roff"] + s["rsize"]
        for off in range(start, end - 4, 4):
            val = struct.unpack_from("<I", m["data"], off)[0]
            if val < m["imagebase"]:
                continue
            col = read_col(m, val)
            if col is None or col["sig"] != 0:
                continue
            nm = read_type_descriptor_name(m, col["p_type_descriptor"])
            if not nm:
                continue
            vstart_va = m["imagebase"] + (off - s["roff"]) + s["vaddr"] + 4
            first = u32_va(m, vstart_va)
            if first is None or not is_text_va(m, first):
                continue
            if vstart_va in seen:
                continue
            seen.add(vstart_va)
            out.append(dict(col_va=val, col=col, class_name=nm,
                            vtable_start=vstart_va))
    out.sort(key=lambda r: r["vtable_start"])
    return out


def script_self_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def utc_now_iso():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
