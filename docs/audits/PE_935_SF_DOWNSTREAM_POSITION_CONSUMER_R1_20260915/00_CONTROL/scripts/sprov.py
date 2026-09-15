"""sprov.py — deterministic symbolic provenance engine for the origin-singleton write-through census.

NEW instrument of correction run PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915.
Read-only on the EXE. Emits MEASUREMENTS (events, states) only; NO science conclusions.

Tracked token: S_PTR = the pointer returned by FUN_00437F70 (getter of the origin singleton).
A token carries a delta: token value == S + delta (address-alias tracking through
lea / add / sub / inc / dec). delta == 0 is the exact singleton pointer.

Engine rules (deterministic, conservative — provenance is never guessed):
  - register copies preserve tokens (mov reg,reg; xchg reg,reg).
  - address arithmetic on a token adjusts its delta (lea/add/sub/inc/dec with imm).
  - any other value transform (xor/and-not-self/or-diff/not/neg/shifts/imul/cmov/zero-ext/...)
    CLEARS the register's token (conservative loss).
  - esp-relative stack slots are tracked by a constant ledger (key = address - esp_at_window_start).
    push/pop/add esp,imm/sub esp,imm update the ledger; token slots that fall below esp are
    discarded (SLOT_DEAD events).
  - ebp-relative loads/stores and esp-indexed addressing are AMBIGUOUS (event recorded, never
    guessed).
  - 'or r,r' / 'and r,r' (same reg) and 'test' preserve the token (flag-only idioms).
  - at a call: tokens in EAX/ECX/EDX or in stack-arg positions (slots at address >= current esp)
    are recorded as ESCAPE events (arg-position slots may be leftover-vs-intentional; the
    callee-head analysis decides); EAX/ECX/EDX tokens are then cleared (caller-saved clobber);
    EBX/EBP/ESI/EDI tokens survive calls (callee-saved convention, disclosed as a convention).
  - at a call to FUN_00437F70 itself, EAX := token(S,0) (getter return; proven by the decode in
    probe_origin_setter.py, not assumed here — the caller passes getter_va).
  - esp effect of a call: +ret_n(target) measured by decode_ret_convention() (cached); unknown
    or indirect targets mark the esp model uncertain (event recorded).
  - writes through an S-derived pointer (mov [reg+disp],src / fstp [reg+disp] / xchg / string
    stores with an EDI-derived base) emit WRITE_S events with the resolved offset delta+disp.
  - reads through an S-derived pointer emit READ_S events (informational).
  - 8/16-bit subregister writes clear the parent 32-bit register's token (partial corruption).
  - capstone regs_write is a safety net (default handler) for unhandled mnemonics.

The engine NEVER emits dispositions; classification lives in the census script (mechanical
aggregation over events, taxonomy fixed by contract Section 4).
"""
import capstone
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM

CALLER_SAVED = ("eax", "ecx", "edx")
GP_REGS = ("eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi")

# 8/16-bit subregisters -> parent (a partial write corrupts the tracked 32-bit value)
SUBREG_PARENT = {
    "al": "eax", "ah": "eax", "ax": "eax",
    "cl": "ecx", "ch": "ecx", "cx": "ecx",
    "dl": "edx", "dh": "edx", "dx": "edx",
    "bl": "ebx", "bh": "ebx", "bx": "ebx",
    "sil": "esi", "si": "esi",
    "dil": "edi", "di": "edi",
    "spl": "esp", "sp": "esp",
    "bpl": "ebp", "bp": "ebp",
}

TERM_MNEMONICS = ("ret", "retf", "iretd", "hlt", "ud2", "int3")
STRING_STORE_MN = ("movsb", "movsw", "movsd", "stosb", "stosw", "stosd")
STRING_READ_MN = ("lods", "scasb", "scasw", "scasd", "cmpsb", "cmpsw", "cmpsd", "lodsb", "lodsw", "lodsd")


class Tok:
    """Symbolic value == S + delta (S = origin singleton pointer).

    gen: token generation. gen == 0 marks tokens derived from the walk's INITIAL seed
    (the census site's own getter return); gen > 0 marks tokens re-established by an
    IN-WINDOW call to the getter (a different census site, which owns their fate).
    Copies and address aliases preserve gen; only a fresh getter return bumps it.
    """
    __slots__ = ("delta", "gen")

    def __init__(self, delta=0, gen=0):
        self.delta = delta
        self.gen = gen

    def copy(self):
        return Tok(self.delta, self.gen)

    def __repr__(self):
        if self.delta == 0:
            return "S"
        return "S%+#x" % self.delta


class Ev:
    """One measured event (deterministic)."""
    __slots__ = ("va", "kind", "detail")

    def __init__(self, va, kind, detail=""):
        self.va = va
        self.kind = kind
        self.detail = detail

    def __repr__(self):
        return "0x%08X %s %s" % (self.va, self.kind, self.detail)


class Engine:
    """Symbolic walker. init_regs maps reg name -> Tok (initial provenance).

    ret_lookup: optional callable(va) -> (n, detail) measuring the callee's ret convention
    (arg bytes popped). If given, the esp ledger of each direct call is updated by +n after
    return; unknown conventions mark the esp model uncertain.
    """

    def __init__(self, init_regs=None, getter_va=0x437F70, ret_lookup=None):
        self.regs = {r: None for r in GP_REGS}
        if init_regs:
            for r, t in init_regs.items():
                self.regs[r] = t.copy() if isinstance(t, Tok) else t
        self.slots = {}          # key (addr - esp0) -> Tok (only S tokens tracked)
        self.esp_delta = 0       # current esp == esp0 - esp_delta
        self.events = []
        self.getter_va = getter_va
        self.ret_lookup = ret_lookup
        self.esp_uncertain = False
        self.stopped = None      # (mnemonic, va, extra) when a STOP signal fired
        self._gen_counter = 0   # bumped by in-window getter returns (gen > 0 = other site's token)

    # ---------------- helpers ----------------
    def ev(self, va, kind, detail=""):
        self.events.append(Ev(va, kind, detail))

    def _mem(self, md, op):
        """(base_name|None, index_name|None, scale, disp) of a MEM operand."""
        m = op.mem
        base = md.reg_name(m.base) if m.base else None
        index = md.reg_name(m.index) if m.index else None
        return base, index, m.scale, m.disp

    def _slot_key(self, disp):
        return disp - self.esp_delta

    def _discard_dead_slots(self, cause_va, cause):
        """Remove token slots whose address fell below esp (popped/discarded)."""
        dead = [k for k in self.slots if k < -self.esp_delta]
        for k in sorted(dead):
            self.ev(cause_va, "SLOT_DEAD", "key=%d cause=%s" % (k, cause))
            del self.slots[k]

    # ---------------- main step ----------------
    def step(self, md, ins):
        """Process one instruction. Returns 'STOP' if the walk must halt."""
        mn = ins.mnemonic
        ops = list(ins.operands) if ins.operands else []
        va = ins.address

        # --- terminals ---
        if mn in TERM_MNEMONICS:
            live_regs = [r for r in GP_REGS if isinstance(self.regs[r], Tok)]
            if live_regs:
                self.ev(va, "ESCAPE_AT_TERMINAL", "live regs: %s" % ",".join(live_regs))
            for k in list(self.slots):
                self.ev(va, "SLOT_DEAD", "key=%d cause=frame-abandoned-at-terminal" % k)
            self.slots.clear()
            self.ev(va, "TERMINAL", mn)
            self.stopped = (mn, va, "")
            return "STOP"

        # --- unconditional jmp: control leaves the linear window ---
        if mn == "jmp":
            tgt = ""
            if ops and ops[0].type == X86_OP_IMM:
                tgt = "0x%08X" % ops[0].imm
            live = [r for r in GP_REGS if isinstance(self.regs[r], Tok)]
            live += ["slot%d" % k for k in self.slots]
            self.ev(va, "UNCOND_JMP", "target=%s live=%s" % (tgt, ",".join(live) or "-"))
            self.stopped = (mn, va, tgt)
            return "STOP"

        # --- conditional branches: fall-through continues; taken path unexamined (event) ---
        if (mn.startswith("j") and mn != "jmp") or mn.startswith("loop") or mn == "jecxz":
            live = [r for r in GP_REGS if isinstance(self.regs[r], Tok)]
            live += ["slot%d" % k for k in self.slots]
            tgt = "0x%08X" % ops[0].imm if ops and ops[0].type == X86_OP_IMM else "reg/mem"
            self.ev(va, "BRANCH", "%s->%s live=%s" % (mn, tgt, ",".join(live) or "-"))
            return None

        # --- mov ---
        if mn == "mov":
            dst, src = ops[0], ops[1]
            if dst.type == X86_OP_REG:
                r = md.reg_name(dst.reg)
                if src.type == X86_OP_REG:
                    st = self.regs.get(md.reg_name(src.reg))
                    self.regs[r] = st.copy() if isinstance(st, Tok) else None
                elif src.type == X86_OP_MEM:
                    base, index, scale, disp = self._mem(md, src)
                    if base == "esp" and index is None:
                        key = self._slot_key(disp)
                        tok = self.slots.get(key)
                        if isinstance(tok, Tok):
                            self.regs[r] = tok.copy()
                            self.ev(va, "RELOAD", "reg=%s from slot key=%d" % (r, key))
                        else:
                            self.regs[r] = None
                    elif base == "ebp" and index is None:
                        self.regs[r] = None
                        if self.slots:
                            self.ev(va, "AMBIG_EBP_LOAD", "reg=%s (ebp-relative; esp slots live)" % r)
                    else:
                        btok = self.regs.get(base) if base else None
                        if isinstance(btok, Tok):
                            self.ev(va, "READ_S", "reg=%s <- [S%+#x]" % (r, btok.delta + disp))
                        self.regs[r] = None
                else:  # IMM
                    self.regs[r] = None
                return None
            if dst.type == X86_OP_MEM:
                base, index, scale, disp = self._mem(md, dst)
                btok = self.regs.get(base) if base else None
                if isinstance(btok, Tok):
                    off = btok.delta + disp
                    if src.type == X86_OP_REG:
                        srcprov = repr(self.regs.get(md.reg_name(src.reg))) if isinstance(
                            self.regs.get(md.reg_name(src.reg)), Tok) else md.reg_name(src.reg)
                    else:
                        srcprov = "imm" if src.type == X86_OP_IMM else "mem"
                    self.ev(va, "WRITE_S", "off=%d value=%s" % (off, srcprov))
                    return None
                if base == "esp" and index is None:
                    key = self._slot_key(disp)
                    if key in self.slots:
                        self.ev(va, "SPILL_OVERWRITTEN", "slot key=%d" % key)
                        del self.slots[key]
                    if src.type == X86_OP_REG:
                        st = self.regs.get(md.reg_name(src.reg))
                        if isinstance(st, Tok):
                            self.slots[key] = st.copy()
                            self.ev(va, "SPILL", "reg=%s -> slot key=%d" % (md.reg_name(src.reg), key))
                    elif src.type == X86_OP_MEM:
                        sbase, sindex, sscale, sdisp = self._mem(md, src)
                        if sbase == "esp" and sindex is None:
                            stok = self.slots.get(self._slot_key(sdisp))
                            if isinstance(stok, Tok):
                                self.slots[key] = stok.copy()
                                self.ev(va, "SPILL_COPY", "slot key=%d -> slot key=%d" % (self._slot_key(sdisp), key))
                    return None
                if base == "ebp" and index is None:
                    if src.type == X86_OP_REG:
                        st = self.regs.get(md.reg_name(src.reg))
                        if isinstance(st, Tok):
                            self.ev(va, "SPILL_UNKNOWN_EBP", "reg=%s -> [ebp%+#x] (untracked slot)" % (md.reg_name(src.reg), disp))
                    return None
                # store into another object: pointer escape
                if src.type == X86_OP_REG:
                    st = self.regs.get(md.reg_name(src.reg))
                    if isinstance(st, Tok):
                        self.ev(va, "ESCAPE_STORE", "reg=%s -> [%s%+#x]" % (md.reg_name(src.reg), base, disp))
                return None
            return None

        # --- lea ---
        if mn == "lea":
            dst = ops[0]
            r = md.reg_name(dst.reg)
            base, index, scale, disp = self._mem(md, ops[1])
            btok = self.regs.get(base) if base else None
            if isinstance(btok, Tok) and index is None:
                nt = btok.copy()
                nt.delta = btok.delta + disp
                self.regs[r] = nt
                return None
            if base == "esp" and index is None:
                self.ev(va, "STACK_ADDR_LEA", "reg=%s = &slot key=%d (address-of; not slot content)" % (r, self._slot_key(disp)))
                self.regs[r] = None
                return None
            if index is not None and base == "esp":
                self.ev(va, "AMBIG_STACK", "esp-indexed lea")
                self.regs[r] = None
                return None
            self.regs[r] = None
            return None

        # --- push ---
        if mn == "push":
            self.esp_delta += 4
            key = -self.esp_delta
            src = ops[0]
            if src.type == X86_OP_REG:
                st = self.regs.get(md.reg_name(src.reg))
                if isinstance(st, Tok):
                    self.slots[key] = st.copy()
                    self.ev(va, "SPILL_PUSH", "reg=%s -> slot key=%d" % (md.reg_name(src.reg), key))
            elif src.type == X86_OP_MEM:
                base, index, scale, disp = self._mem(md, src)
                if base == "esp" and index is None:
                    tok = self.slots.get(self._slot_key(disp))
                    if isinstance(tok, Tok):
                        self.slots[key] = tok.copy()
                        self.ev(va, "STACK_COPY", "slot key=%d -> slot key=%d" % (self._slot_key(disp), key))
                elif isinstance(self.regs.get(base) if base else None, Tok):
                    self.ev(va, "READ_S", "push <- [S%+#x]" % (self.regs[base].delta + disp))
            return None

        # --- pop ---
        if mn == "pop":
            key = -self.esp_delta
            tok = self.slots.get(key)
            self.esp_delta -= 4
            if key in self.slots:
                del self.slots[key]
            if ops[0].type == X86_OP_REG:
                r = md.reg_name(ops[0].reg)
                if r == "esp":
                    # pop esp = stack pivot: model invalid
                    self.slots.clear()
                    self.esp_uncertain = True
                    self.ev(va, "ESP_PIVOT", "pop esp")
                    return None
                if isinstance(tok, Tok):
                    self.regs[r] = tok.copy()
                    self.ev(va, "RELOAD_POP", "reg=%s from slot key=%d" % (r, key))
                else:
                    self.regs[r] = None
            return None

        # --- add / sub / inc / dec (esp ledger + address-alias arithmetic) ---
        if mn in ("add", "sub", "inc", "dec"):
            r = md.reg_name(ops[0].reg) if ops and ops[0].type == X86_OP_REG else None
            if r == "esp":
                if mn == "add" and ops[1].type == X86_OP_IMM:
                    self.esp_delta -= ops[1].imm
                    self._discard_dead_slots(va, "add esp,%#x" % ops[1].imm)
                elif mn == "sub" and ops[1].type == X86_OP_IMM:
                    self.esp_delta += ops[1].imm
                elif mn == "inc":
                    self.esp_uncertain = True
                    self.ev(va, "ESP_UNCERTAIN", "inc esp")
                elif mn == "dec":
                    self.esp_uncertain = True
                    self.ev(va, "ESP_UNCERTAIN", "dec esp")
                else:
                    self.esp_uncertain = True
                    self.ev(va, "ESP_UNCERTAIN", "%s esp,reg/mem" % mn)
                return None
            if r is not None and isinstance(self.regs[r], Tok):
                if mn == "add" and ops[1].type == X86_OP_IMM:
                    self.regs[r].delta += ops[1].imm
                    return None
                if mn == "sub" and ops[1].type == X86_OP_IMM:
                    self.regs[r].delta -= ops[1].imm
                    return None
                if mn == "inc":
                    self.regs[r].delta += 1
                    return None
                if mn == "dec":
                    self.regs[r].delta -= 1
                    return None
                self.regs[r] = None
                return None
            return None

        # --- xchg ---
        if mn == "xchg":
            a, b = ops[0], ops[1]
            if a.type == X86_OP_REG and b.type == X86_OP_REG:
                ra, rb = md.reg_name(a.reg), md.reg_name(b.reg)
                self.regs[ra], self.regs[rb] = self.regs.get(rb), self.regs.get(ra)
                return None
            # xchg with memory through an S-derived base = write through S
            for op, other in ((a, b), (b, a)):
                if op.type == X86_OP_MEM:
                    base, index, scale, disp = self._mem(md, op)
                    btok = self.regs.get(base) if base else None
                    if isinstance(btok, Tok):
                        self.ev(va, "WRITE_S", "off=%d value=xchg(%s)" % (btok.delta + disp, "reg" if other.type == X86_OP_REG else "mem"))
                        return None
            return None

        # --- flag-only / preserving idioms ---
        if mn in ("test", "cmp", "fcom", "fcomp", "fcompp", "fucom", "fucomp", "fucompp"):
            return None
        if mn in ("or", "and") and ops and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG \
                and md.reg_name(ops[0].reg) == md.reg_name(ops[1].reg):
            return None  # 'or eax,eax' / 'and eax,eax' preserve the value

        # --- x87 loads/stores ---
        if mn.startswith("fld") or mn.startswith("fild") or mn.startswith("fbld"):
            if ops and ops[0].type == X86_OP_MEM:
                base, index, scale, disp = self._mem(md, ops[0])
                btok = self.regs.get(base) if base else None
                if isinstance(btok, Tok):
                    self.ev(va, "READ_S", "x87 <- [S%+#x]" % (btok.delta + disp))
                elif base == "esp" and index is None:
                    key = self._slot_key(disp)
                    if key in self.slots:
                        self.ev(va, "SPILL_OVERWRITTEN", "slot key=%d by x87 reload-read" % key)
            return None
        if mn.startswith("fst") or mn.startswith("fist") or mn.startswith("fbst"):
            if ops and ops[0].type == X86_OP_MEM:
                base, index, scale, disp = self._mem(md, ops[0])
                btok = self.regs.get(base) if base else None
                if isinstance(btok, Tok):
                    self.ev(va, "WRITE_S", "off=%d value=x87" % (btok.delta + disp))
                    return None
                if base == "esp" and index is None:
                    key = self._slot_key(disp)
                    if key in self.slots:
                        self.ev(va, "SPILL_OVERWRITTEN", "slot key=%d by x87 store" % key)
                        del self.slots[key]
                elif base == "ebp" and index is None:
                    pass  # ebp slot store; untracked (no S token involved unless src reg... x87 store has no GPR src)
            return None
        if mn.startswith("f") :
            # remaining x87 arith with a mem operand: read-side
            for op in ops:
                if op.type == X86_OP_MEM:
                    base, index, scale, disp = self._mem(md, op)
                    btok = self.regs.get(base) if base else None
                    if isinstance(btok, Tok):
                        self.ev(va, "READ_S", "x87-arith <- [S%+#x]" % (btok.delta + disp))
                    elif base == "esp" and index is None:
                        key = self._slot_key(disp)
                        if key in self.slots and mn not in ("fst", "fstp"):
                            self.ev(va, "SPILL_TOUCHED", "slot key=%d read by %s" % (key, mn))
            return None

        # --- string ops ---
        if mn in STRING_STORE_MN:
            ditok = self.regs.get("edi")
            if isinstance(ditok, Tok):
                self.ev(va, "WRITE_S", "off=%d value=string-store(%s) count=ECX/DF-dependent" % (ditok.delta, mn))
            return None
        if mn in STRING_READ_MN:
            for reg in ("esi", "edi"):
                tok = self.regs.get(reg)
                if isinstance(tok, Tok):
                    self.ev(va, "READ_S", "%s-based string read at [S%+#x]" % (reg, tok.delta))
            return None

        # --- call ---
        if mn == "call":
            target = None
            if ops and ops[0].type == X86_OP_IMM:
                target = ops[0].imm
            # escape detection: caller-saved arg regs
            for r in CALLER_SAVED:
                if isinstance(self.regs[r], Tok):
                    self.ev(va, "ESCAPE_ARGREG", "reg=%s -> callee 0x%08X" % (r, target if target is not None else 0))
            # escape detection: token slots in stack-arg positions (address >= current esp).
            # The slot at address == esp becomes the callee's FIRST stack arg ([esp+4] at callee
            # entry); each +4 above that shifts the callee-entry key by +4.
            for k in sorted(self.slots):
                if k >= -self.esp_delta:
                    self.ev(va, "ESCAPE_STACKARG", "slot key=%d callee_arg_key=%d -> callee 0x%08X" % (
                        k, k + self.esp_delta + 4, target if target is not None else 0))
            # caller-saved clobber
            for r in CALLER_SAVED:
                self.regs[r] = None
            if target is not None and target == self.getter_va:
                self._gen_counter += 1
                self.regs["eax"] = Tok(0, self._gen_counter)
                self.ev(va, "GETTER_RETURN", "eax := S_PTR (gen=%d)" % self._gen_counter)
            elif target is None:
                self.esp_uncertain = True
                self.ev(va, "ESP_UNCERTAIN", "indirect call: esp model assumes cdecl ret 0")
            else:
                if self.ret_lookup is not None:
                    n, detail = self.ret_lookup(target)
                    if n is None:
                        self.esp_uncertain = True
                        self.ev(va, "ESP_UNCERTAIN", "call 0x%08X: ret convention unknown (%s)" % (target, detail))
                    else:
                        self.esp_delta -= n
                        self.ev(va, "CALL_RET_N", "call 0x%08X ret_n=%d (%s)" % (target, n, detail))
                        self._discard_dead_slots(va, "callee ret %d" % n)
            return None

        # --- leave / enter: stack pivot ---
        if mn in ("leave", "enter"):
            self.slots.clear()
            self.esp_uncertain = True
            self.regs["ebp"] = None
            self.ev(va, "ESP_PIVOT", mn)
            return None

        # --- default: conservative net (capstone regs_write) ---
        handled_regs = set()
        try:
            for regid in ins.regs_write:
                nm = md.reg_name(regid)
                nm = SUBREG_PARENT.get(nm, nm)
                if nm in GP_REGS:
                    handled_regs.add(nm)
        except Exception:
            pass
        for nm in handled_regs:
            self.regs[nm] = None
            if nm == "esp":
                self.esp_uncertain = True
                self.ev(va, "ESP_UNCERTAIN", "regs_write esp in %s" % mn)
        return None


def decode_head(md, img, va, size):
    """Linear decode of `size` bytes from va (bounded head). Returns (ins_list, error|None)."""
    try:
        code = img.read(va, size)
    except Exception as e:  # noqa
        return [], "read-fail:%s" % e
    out = []
    for ins in md.disasm(code, va):
        out.append(ins)
    if not out:
        return [], "decode-empty"
    covered = out[-1].address + out[-1].size - va
    if covered < size:
        # capstone stopped early (invalid bytes)
        return out, "decode-stopped-at-%#x" % (va + covered)
    return out, None


def ret_convention(md, img, va, cache, max_bytes=0x400, jmp_depth=8):
    """Measure the ret convention of the function starting at va.

    Returns (n, detail): n = arg bytes popped (0 for plain ret), or None if unknown/ambiguous.
    Extent rule (measured, deterministic): collect ret-family instructions of THIS function only;
    the function ends at its LAST terminal followed by an int3 (0xCC) padding run — decoding stops
    there so rets of FOLLOWING functions are never mixed in (the 0x82B5A0 lesson: a fixed 0x400-byte
    head window overran the 0x50-byte function and produced a bogus 'mixed ret conventions' verdict).
    Follows unconditional jmp-thunks (e.g. IAT-style local thunks) up to jmp_depth.
    """
    key = va
    if key in cache:
        return cache[key]
    seen = 0
    cur = va
    detail = ""
    while True:
        ins_list, err = decode_head(md, img, cur, max_bytes)
        if err and not ins_list:
            cache[key] = (None, "head-decode-fail@%#x: %s" % (cur, err))
            return cache[key]
        rets = []
        jmp_target = None
        extent_end = None
        for ins in ins_list:
            if extent_end is not None and ins.address >= extent_end:
                break
            if ins.mnemonic in ("int3", "hlt", "ud2", "iretd"):
                # padding / hard-stop marker: this function's code has ended
                break
            if ins.mnemonic in ("ret", "retf"):
                n = 0
                if ins.mnemonic == "ret" and ins.operands and ins.operands[0].type == X86_OP_IMM:
                    n = ins.operands[0].imm
                elif ins.mnemonic == "retf" and len(ins.operands) >= 1 and ins.operands[0].type == X86_OP_IMM:
                    n = ins.operands[0].imm
                rets.append((ins.address, n))
                # extent check: int3 padding run after this terminal = function end
                end = ins.address + ins.size
                try:
                    pad = img.read(end, 16)
                except Exception:  # noqa
                    pad = b""
                run = 0
                for b in pad:
                    if b == 0xCC:
                        run += 1
                    else:
                        break
                if run >= 2:
                    extent_end = end + run
            elif ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X86_OP_IMM:
                jmp_target = ins.operands[0].imm
                break
        if rets:
            ns = set(n for _, n in rets)
            if len(ns) == 1:
                detail = "ret %d at %s (all %d rets agree; extent ended at %#x or window end)" % (
                    ns.pop(), ",".join("0x%08X" % a for a, _ in rets), len(rets),
                    extent_end if extent_end is not None else (cur + max_bytes))
                cache[key] = (rets[0][1], detail)
                return cache[key]
            cache[key] = (None, "mixed ret conventions: %s" % rets)
            return cache[key]
        if jmp_target is not None and seen < jmp_depth:
            seen += 1
            detail += "jmp-thunk %#x -> " % cur
            cur = jmp_target
            continue
        cache[key] = (None, "no-ret-in-bounded-head@%#x" % cur)
        return cache[key]


def classify_callee_head(md, img, callee_va, channel, ret_cache, head_bytes=0xA0, getter_va=0x437F70):
    """Bounded callee-head analysis of one escaped pointer channel.

    channel: ('reg', 'ecx') — the escaped pointer arrives in that register (thiscall/fastcall);
             ('stack', key) — the escaped pointer sits at callee-entry stack key `key`
             (key 4 = [esp+4] = first stack arg, key 8 = second, ...).
    Returns dict(class=..., events=[...], decode_error=..., stopped=..., token_live=...).
    Classes (fixed taxonomy): READ_ONLY / WRITE_THROUGH / FORWARDED /
    NOT_USED_IN_CHECKED_HEAD / INSUFFICIENT_PROOF_HEAD_BOUND.
    Mechanical aggregation over engine events only; no science conclusions.
    """
    eng = Engine(getter_va=getter_va)
    if channel[0] == "reg":
        eng.regs[channel[1]] = Tok(0)
    else:
        eng.slots[channel[1]] = Tok(0)
    ins_list, err = decode_head(md, img, callee_va, head_bytes)
    stopped = False
    for ins in ins_list:
        if eng.step(md, ins) == "STOP":
            stopped = True
            break
    write = [e for e in eng.events if e.kind == "WRITE_S"]
    escapes = [e for e in eng.events if e.kind in ("ESCAPE_ARGREG", "ESCAPE_STACKARG", "ESCAPE_STORE")]
    reads = [e for e in eng.events if e.kind == "READ_S"]
    ambig = [e for e in eng.events if e.kind in ("AMBIG_EBP_LOAD", "AMBIG_STACK")]
    token_live = any(isinstance(t, Tok) for t in eng.regs.values()) or bool(eng.slots)
    token_derived = bool(write or escapes or reads) or any(
        e.kind in ("SPILL", "SPILL_PUSH", "RELOAD", "RELOAD_POP", "SPILL_COPY")
        for e in eng.events)
    # clobbered_before_use: the channel's token vanished by value-overwrite without any
    # token-derived event (register channels: callee overwrote the arg register without reading
    # it; stack channels: the slot was overwritten/dropped). The escaped value is then DEAD
    # inside the callee — a non-effective escape channel (not an unresolved deeper use).
    clobbered_before_use = (not token_derived) and (not token_live)
    if write:
        cls = "WRITE_THROUGH"
    elif escapes:
        cls = "FORWARDED"
    elif reads:
        cls = "READ_ONLY"
    elif ambig:
        cls = "INSUFFICIENT_PROOF_HEAD_BOUND"
    else:
        cls = "NOT_USED_IN_CHECKED_HEAD"
    if err is not None and cls in ("NOT_USED_IN_CHECKED_HEAD",) and not stopped:
        # decode stopped before covering the fixed head and the channel was never referenced:
        # absence cannot be claimed over unchecked bytes
        cls = "INSUFFICIENT_PROOF_HEAD_BOUND"
    token_live = any(isinstance(t, Tok) for t in eng.regs.values()) or bool(eng.slots)
    return {
        "class": cls,
        "events": eng.events,
        "decode_error": err,
        "stopped": stopped,
        "token_live": token_live,
        "clobbered_before_use": clobbered_before_use,
    }
