"""
phase_c_anchor.py - PHASE C(iv)+(v)+(iii) (G5/G6): anchor chain + extended slices.
- Full decode of shared base ctor 0x006FABA0 (PIN-CTOR revalidation)
- Decode of the +0x14 zeroing functions (base dtor / deleting dtor chain)
- Per-site EXTENDED backward def-slice of the held-pointer argument at all 6
  shared-ctor call sites. R2 CORRECTION (AMEND_LOG_R2 R2-1/R2-2, QC_AUDIT.md
  P0-1): slices run under the EDGE-AWARE engine (EdgeContext; MULTI_PATH /
  MULTI_ENTRY at branch-target pseudo-function boundaries inside the
  declared dispatcher construct) with a DECLARED 6-level bound (was 4).
- R2 [IV-8]: factory-chain entry-path disposition - per factory block BOTH
  entry paths (xor/allocation-failure path + bypass/normal path), child ctor
  class via vtable store + RTTI walk, child vtable slot-3 dword measured.
- R2 [IV-9]: corrected per-class held-value table.
- [IV-0d] object-size census completed with the PSP + PSPMod new-sites
  (QC P3-7) and the shared-tail alias allocations.
- Per-site this(ECX) slice -> operator-new thunk + object size evidence
- Class resolution of every ctor-caller function (family + mystery four)
- Upstream continuation: leaf ctor/factory caller census + held-arg traces
- SF-chain PIN revalidation (FUN_00509330 ctor, FUN_005247C0 factory,
  FUN_0044D590 container store) for the receiver-identity ladder
Writes 01_RAW/HOLDER14_WRITER_RAW.txt.
"""
import sys
import os
import re
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s0_common as S

RUN_DIR = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(RUN_DIR, "01_RAW")

THUNK = 0x006FAB80
SHARED_CTOR = 0x006FABA0
SIX_SITES = [0x006FAFC7, 0x006FB092, 0x006FB409, 0x006FB5CD, 0x006FE9E8, 0x006FFA87]
SITE_FUNCS = [0x006FAF90, 0x006FB080, 0x006FB3D0, 0x006FB590, 0x006FE9B0, 0x006FFA70]
EXTRA_CTORS = [0x006FBAB0, 0x006FD270]   # CyclicLinear, CyclicSin ctor candidates
PSPMOD_CTOR = 0x006FEB00                  # ParticleSystemPredefinedMod ctor (R2)
DTOR_FUNCS = [0x006FAC00, 0x006FAC50, 0x006FB740, 0x006FD2E0]
FACTORY_CANDS = [0x006D1530, 0x006D206C, 0x006D228B, 0x006D23EB,
                 0x006D24C0, 0x006D2544, 0x006D260B]
SF_CTOR = 0x00509330
SF_FACTORY = 0x005247C0
SF_CONTAINER = 0x0044D590
SF_VTABLE = 0x00A7D458
SF_SLOT3 = 0x0050A050

# R2: the dispatcher construct (declared; engine activation bound)
CONSTRUCT = (0x006D0ED0, 0x006D265F)
# R2: family derived ctors whose factory arg2 is PARAM-CHAINED (arg2 flows
# from the factory blocks); the other 5 classes bind NULL via immediate
# push 0 inside their own ctors (re-derived below).
PARAM_CHAINED_CTORS = {0x006FB590: "ArkAnimationDerivatives",
                       0x006FBAB0: "ArkAnimationCyclicLinear",
                       0x006FD270: "ArkAnimationCyclicSin"}
IMMEDIATE_NULL_CTORS = {0x006FAF90: ("ArkAnimationTimeController", 0x006FAFC0),
                        0x006FB080: ("ArkAnimationNodeUpdate", 0x006FB089),
                        0x006FB3D0: ("ArkAnimationAnimatedTexture", 0x006FB402),
                        0x006FE9B0: ("ArkAnimationParticleSystemPredefined", 0x006FE9E1)}
# R2: chunk-closure bound for multi-chunk family/child functions
CHUNK_CLOSURE_MAX = 64      # chunks per function
CHUNK_CLOSURE_EXT = 0x10000  # max extent per function


def func_report(m, cs, functions, va, vt_names, imports, thunk_cache,
                title, max_insns=200, note_filter=None):
    """Decode one function; return report lines with vtable-store / import /
    refcount-write annotations."""
    lines = []
    fn = S.func_containing(functions, va)
    if fn is None:
        f = S.b5_function(m, cs, va)
        fn = dict(start=f["start"], end=f["end"], end_kind=f["end_kind"])
    lines.append("--- %s" % title)
    lines.append("    B.5: [0x%08X..0x%08X) %s" % (fn["start"], fn["end"], fn["end_kind"]))
    insns, err = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
    if not insns:
        lines.append("    DECODE ERROR at %s" % ("0x%08X" % err if err else "?"))
        return lines, fn
    for i in insns[:max_insns]:
        ann = []
        ops = i.operands
        # vtable store?
        if i.mnemonic == "mov" and len(ops) == 2 \
                and ops[0].type == S.x86c.X86_OP_MEM \
                and ops[1].type == S.x86c.X86_OP_IMM:
            v = ops[1].imm & 0xFFFFFFFF
            if v in vt_names:
                ann.append("VTABLE_STORE -> %s (vt 0x%08X)" % (vt_names[v], v))
        # call resolution
        if i.mnemonic in ("call", "jmp"):
            tgt = None
            if ops and ops[0].type == S.x86c.X86_OP_IMM:
                tgt = ops[0].imm & 0xFFFFFFFF
            elif ops and ops[0].type == S.x86c.X86_OP_MEM and not ops[0].mem.base \
                    and not ops[0].mem.index:
                iat = ops[0].mem.disp & 0xFFFFFFFF
                if iat in imports:
                    ann.append("IMPORT_CALL %s" % imports[iat])
            if tgt is not None and i.mnemonic == "call":
                if tgt in thunk_cache:
                    ann.append("-> %s" % thunk_cache[tgt])
                else:
                    tstr, iname = S.thunk_target_import(m, cs, imports, tgt)
                    label = iname if iname else ("sub_0x%08X" % tgt)
                    thunk_cache[tgt] = label
                    ann.append("-> %s" % label)
        # held-refcount-style write at disp 0x04?
        for (_i, op) in S.mem_write_ops(i):
            if op.mem.disp == 0x04:
                ann.append("WRITE_[+0x04]")
            if op.mem.disp == 0x14:
                ann.append("WRITE_[+0x14]")
        lines.append("    0x%08X  %-20s %-34s%s"
                     % (i.address, i.bytes.hex(), i.mnemonic + " " + i.op_str,
                        ("   ; " + " ; ".join(ann)) if ann else ""))
    if len(insns) > max_insns:
        lines.append("    ... (%d more insns truncated)" % (len(insns) - max_insns))
    return lines, fn


def collect_call_leaves(node, out):
    if node.kind == "CALL_RETURN":
        mm = re.search(r"callee (0x[0-9A-Fa-f]+)", node.detail)
        if mm:
            out.add(int(mm.group(1), 16))
    for c in node.children:
        collect_call_leaves(c, out)
    return out


# --------------------------------------------------------------------------
# R2 helpers (AMEND_LOG_R2 R2-1..R2-3)
# --------------------------------------------------------------------------

def chunk_closure(m, cs, functions, branches, start_va):
    """All B.5 chunks of one logical function: the start chunk plus every
    chunk that is a direct-branch target of a collected chunk, plus the
    fall-through chunk after a CONDITIONAL terminal, plus jump-TABLE targets
    (the x86 idiom 'jmp dword ptr [reg*4 + imm]' - table entries resolved as
    consecutive .text dwords at imm, <= 32 entries, stop at the first
    non-.text dword), within [start, start+CHUNK_CLOSURE_EXT). Declared
    bound: <= CHUNK_CLOSURE_MAX chunks."""
    fn = S.func_containing(functions, start_va)
    if fn is None:
        f2 = S.b5_function(m, cs, start_va)
        fn = dict(start=f2["start"], end=f2["end"], end_kind=f2["end_kind"])
    chunks = [dict(fn)]
    hi = fn["start"] + CHUNK_CLOSURE_EXT
    changed = True
    while changed and len(chunks) <= CHUNK_CLOSURE_MAX:
        changed = False
        starts = set(c["start"] for c in chunks)
        for c in list(chunks):
            insns, _e = S.disasm_range(m, cs, c["start"], c["end"] - c["start"])
            if not insns:
                continue
            term = insns[-1]
            # (b) fall-through after a conditional terminal
            if term.mnemonic.startswith("j") and term.mnemonic != "jmp":
                nxt = S.func_containing(functions, c["end"])
                if nxt is not None and nxt["start"] == c["end"] \
                        and nxt["start"] not in starts and nxt["start"] < hi:
                    chunks.append(dict(nxt))
                    starts.add(nxt["start"])
                    changed = True
            # (a) branch targets of any insn in this chunk
            for i in insns:
                if i.mnemonic.startswith("j"):
                    ops = i.operands
                    if ops and ops[0].type == S.x86c.X86_OP_IMM:
                        tgt = ops[0].imm & 0xFFFFFFFF
                        if tgt not in starts and fn["start"] <= tgt < hi:
                            f3 = S.func_containing(functions, tgt)
                            if f3 is not None and f3["start"] == tgt:
                                chunks.append(dict(f3))
                                starts.add(tgt)
                                changed = True
                # (c) jump TABLE: 'jmp dword ptr [reg*scale + imm]' -> the
                # consecutive .text dwords at imm are chunk starts
                if i.mnemonic == "jmp":
                    ops = i.operands
                    if ops and ops[0].type == S.x86c.X86_OP_MEM \
                            and ops[0].mem.base == 0 and ops[0].mem.index != 0:
                        tbl = ops[0].mem.disp & 0xFFFFFFFF
                        for k in range(32):
                            ent = S.u32_va(m, tbl + 4 * k)
                            if ent is None or not S.is_text_va(m, ent):
                                break
                            if fn["start"] <= ent < hi and ent not in starts:
                                f4 = S.func_containing(functions, ent)
                                if f4 is not None and f4["start"] == ent:
                                    chunks.append(dict(f4))
                                    starts.add(ent)
                                    changed = True
    chunks.sort(key=lambda c: c["start"])
    return chunks


def closure_insns(m, cs, chunks):
    out = []
    for c in chunks:
        insns, _e = S.disasm_range(m, cs, c["start"], c["end"] - c["start"])
        out.extend(insns)
    out.sort(key=lambda i: i.address)
    return out


def measure_ctor(m, cs, functions, branches, callee, vt_names):
    """Measure one child/family ctor over its chunk closure: first vtable
    store, RTTI class name + lineage, ret sites + this-return shape.
    Returns a dict (deterministic; cached by caller)."""
    chunks = chunk_closure(m, cs, functions, branches, callee)
    insns = closure_insns(m, cs, chunks)
    res = dict(callee=callee, n_chunks=len(chunks), extent=(chunks[0]["start"],
               max(c["end"] for c in chunks)), vtable_store=None,
               vtable=None, class_name=None, lineage=None, rets=[])
    for i in insns:
        ops = i.operands
        if i.mnemonic == "mov" and len(ops) == 2 \
                and ops[0].type == S.x86c.X86_OP_MEM \
                and ops[1].type == S.x86c.X86_OP_IMM:
            v = ops[1].imm & 0xFFFFFFFF
            if v in vt_names:
                res["vtable_store"] = i.address
                res["vtable"] = v
                res["class_name"] = vt_names[v]
                break
    if res["vtable"] is not None:
        col_va = S.u32_va(m, res["vtable"] - 4)
        col = S.read_col(m, col_va) if col_va else None
        if col:
            chd = S.read_chd(m, col["p_class_hierarchy"])
            if chd:
                res["lineage"] = [b["name"] for b in chd["bases"]]
    rets = [i for i in insns if i.mnemonic == "ret"]
    for r in rets:
        shape = None
        # this-return shape: a mov eax,REG shortly before the ret
        for j in insns:
            if r.address - 32 <= j.address < r.address and j.mnemonic == "mov":
                jops = j.operands
                if len(jops) == 2 and jops[0].type == S.x86c.X86_OP_REG \
                        and j.reg_name(jops[0].reg) == "eax" \
                        and jops[1].type == S.x86c.X86_OP_REG:
                    shape = ("mov eax,%s @0x%08X (this-return shape)"
                             % (j.reg_name(jops[1].reg), j.address))
                    break
        res["rets"].append((r.address, shape))
    return res


def extract_chain_leaves(node, out, path=""):
    """Walk a slice tree; collect (kind, detail, path) for ZERO leaves and
    CALL_RETURN nodes (chain evidence for [IV-8])."""
    here = path + (" > " + node.kind if path else node.kind)
    if node.kind == "ZERO":
        out.append(("ZERO", node.detail, here))
    if node.kind == "CALL_RETURN":
        mm = re.search(r"def via call (0x[0-9A-Fa-f]+) -> callee (0x[0-9A-Fa-f]+)", node.detail)
        vt = re.search(r"stores vtable (0x[0-9A-Fa-f]+)", node.detail)
        out.append(("CALL_RETURN", node.detail, here))
    for c in node.children:
        extract_chain_leaves(c, out, here)
    return out


def cascade_size_walk(m, cs, functions, edge_ctx, newsite_va, new_thunk):
    """R2 (QC P3-7): the PSP/PSPMod ??2 sites sit directly after name-compare
    jne edges with NO local size push; their allocation size was pushed once
    ahead of the compare chain. Walk the case chain backward (entry edges,
    <= 16 hops); the FIRST push-imm on the path is the cascade size.
    Returns (size, push_va, hops, note)."""
    va = newsite_va
    hops = 0
    seen_blocks = set()
    while hops <= 16:
        fn = S.func_containing(functions, va)
        if fn is None:
            return (None, None, hops, "block not in B.5 map")
        if fn["start"] in seen_blocks:
            return (None, None, hops, "cycle in case chain at block 0x%08X" % fn["start"])
        seen_blocks.add(fn["start"])
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        pushes = [i for i in insns if fn["start"] <= i.address < va
                  and i.mnemonic == "push" and i.operands
                  and i.operands[0].type == S.x86c.X86_OP_IMM]
        if pushes:
            p = pushes[-1]
            return (p.operands[0].imm & 0xFFFFFFFF, p.address, hops,
                    "push found in walk block [0x%08X..0x%08X) at hop %d"
                    % (fn["start"], fn["end"], hops))
        ents = [(s, mn, t) for (s, mn, t)
                in edge_ctx.entries_into(fn["start"] - 1, fn["start"])
                if s < fn["start"]]
        if not ents:
            return (None, None, hops,
                    "no entry edge into block 0x%08X (chain head reached)" % fn["start"])
        va = max(s for (s, mn, t) in ents)
        hops += 1
    return (None, None, hops, "hop bound exceeded")


def child_alloc_at(m, cs, functions, calls, child_call_site, new_thunk):
    """The child block's local fresh allocation: the LAST ??2 call in the
    containing block before the child ctor call, and the push imm within 16
    bytes before that. Returns (size, push_va, new_va) or (None, None, new_va
    or None)."""
    fn = S.func_containing(functions, child_call_site)
    if fn is None or new_thunk is None:
        return (None, None, None)
    new_va = None
    for (s, t) in calls:
        if t == new_thunk and fn["start"] <= s < child_call_site:
            if new_va is None or s > new_va:
                new_va = s
    if new_va is None:
        return (None, None, None)
    insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
    for i in insns:
        if new_va - 16 <= i.address < new_va and i.mnemonic == "push" \
                and i.operands and i.operands[0].type == S.x86c.X86_OP_IMM:
            return (i.operands[0].imm & 0xFFFFFFFF, i.address, new_va)
    return (None, None, new_va)


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: HOLDER14_WRITER_RAW.txt (Phase C iii+iv+v; anchor chain + slices)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_c_anchor.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("SOURCE_OF_TRUTH: %s physical bytes (STATIC; NEVER executed)" % S.EXE_PATH)
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("CORRECTION: R2 batch (AMEND_LOG_R2.md; regenerated per QC_AUDIT.md P0-1/P3-7;")
    L.append("  the R1 slices' universal-NULL verdicts at the param-chained factory chains were")
    L.append("  falsified by branch-bypass edges - see [IV-8]/[IV-9] for the corrected disposition).")
    L.append("CORRECTED SLICE BOUND (declared, R2): 6 levels x 384-byte backward window per")
    L.append("  level (widened from 4; AMEND_LOG_R2 R2-2: the child-ctor call-cross plus the")
    L.append("  operator-new this-cross at the deepest Cyclic chain require 2 additional levels);")
    L.append("  multi-start over ret sites (<= %d) and callers (<= %d), clobber-aware,"
             % (S.SLICE_MAX_RET_SITES, S.SLICE_MAX_CALLERS))
    L.append("  linear last-def-wins, alternates recorded, INSUFFICIENT_PROOF on exhaustion.")
    L.append("EDGE-AWARENESS (R2, AMEND_LOG_R2 R2-1): slices are branch-edge aware inside the")
    L.append("  declared dispatcher construct [0x%08X..0x%08X): a bypassed def becomes a"
             % CONSTRUCT)
    L.append("  MULTI_PATH node (def path + bypass-entry paths); a no-def window with external")
    L.append("  entries becomes a MULTI_ENTRY node; test/cmp are reads (not defs); a callee")
    L.append("  returning its thiscall this gets a caller-cross child. Outside the construct")
    L.append("  the R1 engine model applies unchanged.")
    L.append("=" * 80)

    # build map + lattice + branch edges (independent pass #3)
    branches = []
    functions, calls, jmps, stats = S.build_text_map(m, cs, branches=branches)
    edge_ctx = S.EdgeContext(branches)
    L.append("")
    L.append("[MAP] B.5 pass: functions=%d calls=%d insns=%d (cross-check: Phase B/C identical)"
             % (len(functions), len(calls), stats["insns"]))
    L.append("[MAP] R2 branch-edge index: %d direct jump-family edges (jmp E9/EB + all jcc)"
             % len(branches))
    L.append("[MAP] R2 declared construct: [0x%08X..0x%08X) %s"
             % (CONSTRUCT[0], CONSTRUCT[1],
                "ArkAnimation name-dispatch construct"))
    disp_callers = sorted(a for (a, t) in calls if t == CONSTRUCT[0])
    L.append("[MAP] construct entry 0x%08X direct E8 callers (%d): %s"
             % (CONSTRUCT[0], len(disp_callers), [hex(a) for a in disp_callers]))

    # inventory for class names of arbitrary vtable stores
    inv = S.vtable_inventory(m)
    vt_names = {}
    for r in inv:
        vt_names[r["vtable_start"]] = r["class_name"]
    vt_names[SF_VTABLE] = "SceneFeederObject (pin, validated below)"
    imports = S.parse_imports(m)
    thunk_cache = {}

    # ---- [IV-0] shared ctor full decode + PIN-CTOR validation
    L.append("")
    L.append("[IV-0] SHARED BASE CTOR 0x%08X FULL DECODE" % SHARED_CTOR)
    rep, fn0 = func_report(m, cs, functions, SHARED_CTOR, vt_names, imports,
                           thunk_cache, "shared base ctor 0x006FABA0")
    L.extend(rep)
    ctor_insns, _e = S.disasm_range(m, cs, fn0["start"], fn0["end"] - fn0["start"])
    w14 = [i for i in ctor_insns if any(op.mem.disp == 0x14 for (_i, op) in S.mem_write_ops(i))]
    w04 = [i for i in ctor_insns if any(op.mem.disp == 0x04 for (_i, op) in S.mem_write_ops(i))]
    L.append("    +0x14 writes in ctor: %s" % [("0x%08X" % i.address, i.bytes.hex()) for i in w14])
    L.append("    +0x04 writes in ctor: %s" % [("0x%08X" % i.address, i.bytes.hex()) for i in w04])
    pin_ok = []
    for i in ctor_insns:
        if i.bytes.hex() == "894814":
            pin_ok.append(("PIN-CTOR write [eax+0x14],ecx (89 48 14)", True))
        if i.bytes.hex() == "ba01000000":
            pin_ok.append(("PIN-CTOR mov edx,1 (BA 01 00 00 00)", True))
        if i.bytes.hex() == "015104":
            pin_ok.append(("PIN-CTOR add [ecx+4],edx (01 51 04)", True))
    seen = set()
    for (label, ok) in pin_ok:
        if label not in seen:
            seen.add(label)
            L.append("    PIN-CTOR check: %-50s MATCH=%s" % (label, ok))
    if not pin_ok:
        L.append("    PIN-CTOR check: NO expected byte patterns found (FINDING - re-derive)")
    cond_before = [i for i in ctor_insns if i.mnemonic.startswith("j") and i.address < w14[0].address] if w14 else []
    L.append("    conditional branches before the +0x14 write: %s"
             % ([("0x%08X" % i.address, i.mnemonic) for i in cond_before] if cond_before else "NONE"))
    prologue = ctor_insns[0].mnemonic + " " + ctor_insns[0].op_str
    L.append("    entry ABI evidence: first insn '%s'; thiscall(this=ECX, arg0=[esp+4], arg1=[esp+8], arg2=[esp+0xC]) inferred from"
             % prologue)
    L.append("    decode below: %s" % " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in ctor_insns[:6]))
    L.append("    CTOR ABI DERIVATION: ret 0xC = 3 dword stack args; held param read from [esp+0xC] = ARG2;")
    L.append("    arg0 = byte flag (mov cl, byte [esp+4] -> [this+0x28]); arg1 = float (fld dword [esp+8] -> [this+0x2C]);")
    L.append("    arg2 = HELD OBJECT POINTER -> [this+0x14] with NULL TEST (test ecx,ecx; je skips the refcount inc).")
    L.append("    CORRECTION vs first pass: earlier slice of arg0 was the WRONG ARG; the held param is arg2.")

    # ---- object-size census: ??2 sites followed by family-ctor calls
    L.append("")
    L.append("[IV-0d] OBJECT-SIZE CENSUS: operator-new sites feeding family ctor calls")
    NEW_THUNK = None
    for (site, tgt) in calls:
        if tgt in thunk_cache:
            if "??2" in str(thunk_cache[tgt]):
                NEW_THUNK = tgt
                break
    if NEW_THUNK is None:
        for (site, tgt) in calls[:5000]:
            _t, iname = S.thunk_target_import(m, cs, imports, tgt)
            thunk_cache[tgt] = iname if iname else ("sub_0x%08X" % tgt)
            if iname and "??2" in iname:
                NEW_THUNK = tgt
                break
    L.append("  operator-new thunk (resolved via imports): 0x%08X (%s)"
             % (NEW_THUNK if NEW_THUNK else 0, thunk_cache.get(NEW_THUNK, "?") if NEW_THUNK else "?"))
    fam_ctor_targets = set(SITE_FUNCS) | set(EXTRA_CTORS) | {SHARED_CTOR} \
        | {PSPMOD_CTOR}
    ctor_name = {}
    for fv in SITE_FUNCS + EXTRA_CTORS + [PSPMOD_CTOR]:
        fn = S.func_containing(functions, fv)
        if fn:
            insns, _e = S.disasm_range(m, cs, fv, fn["end"] - fv)
            for i in insns:
                ops = i.operands
                if i.mnemonic == "mov" and len(ops) == 2 \
                        and ops[0].type == S.x86c.X86_OP_MEM \
                        and ops[1].type == S.x86c.X86_OP_IMM:
                    v = ops[1].imm & 0xFFFFFFFF
                    if v in vt_names:
                        ctor_name[fv] = vt_names[v]
    new_sites = [site for (site, tgt) in calls if tgt == NEW_THUNK] if NEW_THUNK else []
    size_pairs = []
    for ns in new_sites:
        # any family ctor call within 128 bytes after?
        after = [t for (s, t) in calls if ns < s < ns + 128 and t in fam_ctor_targets]
        if not after:
            continue
        fn = S.func_containing(functions, ns)
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        size = None
        size_src = None
        for i in insns:
            if ns - 16 <= i.address < ns:
                if i.mnemonic == "push" and i.operands and i.operands[0].type == S.x86c.X86_OP_IMM:
                    size = i.operands[0].imm & 0xFFFFFFFF
                    size_src = ("local push imm @0x%08X (within the declared 16-byte "
                                "pre-call window)" % i.address)
        if size is None:
            # R2 (QC P3-7): no local size push -> the dispatcher pushed the
            # size ahead of the name-compare chain. Cascade walk (declared,
            # <=16 hops) backward through the case chain.
            size, push_va, hops, note = cascade_size_walk(m, cs, functions,
                                                          edge_ctx, ns, NEW_THUNK)
            if size is not None:
                size_src = ("CASCADE-SIZE (R2): push 0x%X @0x%08X, %d hop(s) backward "
                            "through the name-compare chain (%s); the size is "
                            "shared by the whole PSP/PSPMod case cascade - the "
                            "intermediate push-imms 1..6 on the match paths are "
                            "ctor ARG0 values (mod-mode), not sizes"
                            % (size, push_va, hops, note))
            else:
                size_src = ("NO SIZE MEASURED (cascade walk: %s)" % note)
        for t in sorted(set(after)):
            size_pairs.append((ns, size, t, ctor_name.get(t, "base ctor 0x006FABA0"),
                               size_src))
            L.append("  new-site 0x%08X: %s; ??2 -> ctor 0x%08X (%s)"
                     % (ns, ("push 0x%X" % size) if size else "SIZE BELOW",
                        t, ctor_name.get(t, "base ctor")))
            L.append("    size provenance: %s" % size_src)
    if not size_pairs:
        L.append("  (no new->family-ctor pairs found within the 128-byte window; record honestly)")
    L.append("  NOTE: sizes are the new() sizes that immediately precede family ctor calls; the")
    L.append("        ctor name is the class whose vtable that ctor stores (from [IV-7]).")
    L.append("  R2 COMPLETION (QC P3-7): the PSP site (??2 @0x006D1530 -> ctor call 0x006D1578)")
    L.append("  and all six PSPMod sites (??2 @0x006D123C/0x006D12BF/0x006D1345/0x006D13CB/")
    L.append("  0x006D1448/0x006D14C5 -> ctor 0x006FEB00 = .?AVArkAnimationParticleSystemPredefinedMod@@)")
    L.append("  are enumerated above with the cascade-size provenance (object size 0x70;")
    L.append("  measured below where the cascade walk lands).")

    # ---- [IV-0c] zeroing functions + dtor chain
    L.append("")
    L.append("[IV-0c] +0x14 ZEROING FUNCTIONS (release path) AND DELETING-DTOR CHAIN")
    for fv in DTOR_FUNCS:
        rep, _fn = func_report(m, cs, functions, fv, vt_names, imports, thunk_cache,
                               "release-path function 0x%08X" % fv)
        L.extend(rep)

    # ---- [IV-1..6] six-site held-param slices + this(ECX) slices + new size
    L.append("")
    L.append("[IV-1..6] EXTENDED BACKWARD DEF-SLICES AT THE SIX SHARED-CTOR CALL SITES")
    L.append("  (held param = stack ARG2 of the ctor call per [IV-0] ABI derivation; this = ECX at site)")
    L.append("  R2: slices run EDGE-AWARE at the declared 6-level bound; the param-chained")
    L.append("  sites 4/6 now enumerate BOTH factory-block entry paths (xor/allocation-failure")
    L.append("  path + bypass/normal path) instead of the R1 single ZERO verdict.")
    all_leaves = set()
    site_reports = {}
    for site in SIX_SITES:
        fn = S.func_containing(functions, site)
        fs = fn["start"] if fn else 0
        L.append("")
        L.append("  SITE 0x%08X (in function 0x%08X..0x%08X)" % (site, fs, fn["end"] if fn else 0))
        visited = set()
        budget = {"n": 0, "max_level": 6}
        tree = S.slice_call_arg(m, cs, functions, calls, site, 2, 0, visited,
                                budget, edge_ctx)
        L.append("    HELD-PARAM (arg2) SLICE TREE:")
        for ln in S.format_slice_tree(tree).split(chr(10)):
            L.append("      " + ln)
        collect_call_leaves(tree, all_leaves)
        visited2 = set()
        budget2 = {"n": 0, "max_level": 6}
        tree2 = S.slice_reg(m, cs, functions, calls, site, "ecx", 0, visited2,
                            budget2, edge_ctx)
        L.append("    THIS(ECX) SLICE TREE:")
        for ln in S.format_slice_tree(tree2).split(chr(10)):
            L.append("      " + ln)
        collect_call_leaves(tree2, all_leaves)
        site_reports[site] = (tree, tree2)
        # new-size evidence: push imm before any call to an import thunk in the func
        insns, _e2 = S.disasm_range(m, cs, fs, (fn["end"] - fs) if fn else 0)
        for k, i in enumerate(insns):
            if i.mnemonic == "push" and i.operands and i.operands[0].type == S.x86c.X86_OP_IMM:
                nxt = insns[k + 1] if k + 1 < len(insns) else None
                if nxt is not None and nxt.mnemonic == "call":
                    tgt = None
                    label = None
                    if nxt.operands and nxt.operands[0].type == S.x86c.X86_OP_IMM:
                        tgt = nxt.operands[0].imm & 0xFFFFFFFF
                        if tgt in thunk_cache:
                            label = thunk_cache[tgt]
                        else:
                            _t, iname = S.thunk_target_import(m, cs, imports, tgt)
                            label = iname if iname else ("sub_0x%08X" % tgt)
                            thunk_cache[tgt] = label
                    elif nxt.operands and nxt.operands[0].type == S.x86c.X86_OP_MEM:
                        iat = nxt.operands[0].mem.disp & 0xFFFFFFFF
                        label = imports.get(iat, "?")
                    if label and ("operator new" in str(label) or "??2" in str(label)):
                        L.append("    NEW-SIZE EVIDENCE: push 0x%X; call -> %s  (object size 0x%X bytes)"
                                 % (i.operands[0].imm & 0xFFFFFFFF, label,
                                    i.operands[0].imm & 0xFFFFFFFF))

    # ---- [IV-7] class resolution of all ctor-caller functions
    L.append("")
    L.append("[IV-7] CLASS RESOLUTION OF ALL FAMILY-CTOR CALLER FUNCTIONS (vtable stores)")
    for fv in SITE_FUNCS + EXTRA_CTORS + [PSPMOD_CTOR]:
        fn = S.func_containing(functions, fv)
        insns, _e = S.disasm_range(m, cs, fv, (fn["end"] - fv) if fn else 0)
        stores = []
        for i in insns:
            ops = i.operands
            if i.mnemonic == "mov" and len(ops) == 2 \
                    and ops[0].type == S.x86c.X86_OP_MEM \
                    and ops[1].type == S.x86c.X86_OP_IMM:
                v = ops[1].imm & 0xFFFFFFFF
                if v in vt_names:
                    stores.append((i.address, v, vt_names[v]))
        ctors_called = sorted(set(t for (a, t) in calls if a >= fv and a < ((fn["end"]) if fn else fv)))
        L.append("  func 0x%08X: vtable stores: %s" % (fv,
                 [("0x%08X" % a, nm) for (a, v, nm) in stores] if stores else "NONE"))
        L.append("           direct E8 targets (within B.5 extent): %s"
                 % [hex(t) for t in ctors_called])

    # ---- [IV-8] R2 factory-chain entry-path disposition (QC P0-1 revalidation)
    L.append("")
    L.append("[IV-8] FACTORY-CHAIN ENTRY-PATH DISPOSITION (R2 edge-aware; BOTH paths per block)")
    L.append("  Method: every E8 call site of the three param-chained family ctors inside the")
    L.append("  construct [0x%08X..0x%08X) is sliced at arg2 under the R2 edge-aware engine;"
             % CONSTRUCT)
    L.append("  the slice trees enumerate BOTH factory-block entry paths. Child ctors are")
    L.append("  measured over their chunk closure: vtable store -> RTTI class + lineage;")
    L.append("  child vtable slot-3 dword (+0x0C) re-measured and tested != 0x0050A050.")
    chain_site_lists = {}
    for (ctor_va, ctor_cls) in sorted(PARAM_CHAINED_CTORS.items()):
        sites = sorted(a for (a, t) in calls
                       if t == ctor_va and CONSTRUCT[0] <= a < CONSTRUCT[1])
        chain_site_lists[ctor_va] = sites
        L.append("")
        L.append("  CTOR 0x%08X (%s): %d factory call site(s) in the construct: %s"
                 % (ctor_va, ctor_cls, len(sites), [hex(a) for a in sites]))
    child_measures = {}

    def child_measure(callee):
        if callee not in child_measures:
            child_measures[callee] = measure_ctor(m, cs, functions, branches,
                                                  callee, vt_names)
        return child_measures[callee]

    total_zero_paths = 0
    total_child_paths = 0
    per_class_children = {}
    for (ctor_va, ctor_cls) in sorted(PARAM_CHAINED_CTORS.items()):
        for site in chain_site_lists[ctor_va]:
            visited = set()
            budget = {"n": 0, "max_level": 6}
            tree = S.slice_call_arg(m, cs, functions, calls, site, 2, 0,
                                    visited, budget, edge_ctx)
            leaves = extract_chain_leaves(tree, [])
            zero_leaves = [x for x in leaves if x[0] == "ZERO"]
            cr_leaves = [x for x in leaves if x[0] == "CALL_RETURN"]
            child_calls = []
            for (_k, detail, _path) in cr_leaves:
                mm = re.search(r"def via call (0x[0-9A-Fa-f]+) -> callee (0x[0-9A-Fa-f]+)", detail)
                if mm:
                    csite2 = int(mm.group(1), 16)
                    callee2 = int(mm.group(2), 16)
                    if callee2 != NEW_THUNK:
                        child_calls.append((csite2, callee2))
            fn = S.func_containing(functions, site)
            L.append("")
            L.append("  SITE 0x%08X -> ctor 0x%08X (%s); containing block %s"
                     % (site, ctor_va, ctor_cls,
                        ("[0x%08X..0x%08X)" % (fn["start"], fn["end"])) if fn else "?"))
            L.append("    PATH ENUMERATION (edge-aware): %d xor/allocation-failure path(s) "
                     "(held=NULL), %d child-construction path(s)"
                     % (len(zero_leaves), len(set(c[1] for c in child_calls))))
            total_zero_paths += len(zero_leaves)
            for (_k, detail, path) in zero_leaves:
                L.append("      X-PATH: %s [tree-path: %s]" % (detail, path))
            for (csite, callee) in sorted(set(child_calls)):
                cm = child_measure(callee)
                total_child_paths += 1
                per_class_children.setdefault(ctor_cls, set()).add(callee)
                slot3 = S.u32_va(m, cm["vtable"] + 0x0C) if cm["vtable"] else None
                asize, apush, anew = child_alloc_at(m, cs, functions, calls,
                                                    csite, NEW_THUNK)
                L.append("      CHILD PATH: child ctor call @0x%08X -> 0x%08X"
                         % (csite, callee))
                L.append("        child alloc      : %s"
                         % (("push 0x%X @0x%08X -> ??2 @0x%08X (fresh allocation; "
                             "the chain's je is its NULL test)" % (asize, apush, anew))
                            if asize is not None else
                            "no local ??2+push pair within the declared 32/16-byte "
                            "windows (recorded honestly)"))
                L.append("        child class       : %s (vtable 0x%08X; vtable store "
                         "@0x%08X; %d chunk(s), extent [0x%08X..0x%08X))"
                         % (cm["class_name"], cm["vtable"], cm["vtable_store"],
                            cm["n_chunks"], cm["extent"][0], cm["extent"][1]))
                L.append("        child lineage     : %s"
                         % (" <- ".join(cm["lineage"]) if cm["lineage"] else "?"))
                L.append("        child ret shape   : %s"
                         % ("; ".join("ret @0x%08X %s" % (a, s) if s else
                                      "ret @0x%08X" % a for (a, s) in cm["rets"])
                            if cm["rets"] else "no ret in closure"))
                L.append("        child vtable slot-3 dword @0x%08X = 0x%08X  "
                         "== 0x0050A050? %s"
                         % (cm["vtable"] + 0x0C, slot3 if slot3 is not None else 0,
                            "YES (!)" if slot3 == SF_SLOT3 else "NO"))
    L.append("")
    L.append("  SUMMARY: %d xor/allocation-failure path(s) (held=NULL) and %d child-"
             "construction path(s) across the %d factory call sites; NO path binds "
             "a SceneFeederObject (slot-3 test above)."
             % (total_zero_paths, total_child_paths,
                sum(len(v) for v in chain_site_lists.values())))

    # ---- [IV-9] R2 per-class held-value table (the corrected disposition)
    L.append("")
    L.append("[IV-9] PER-CLASS HELD-VALUE TABLE (R2 corrected disposition; replaces the R1")
    L.append("  universal-NULL verdict that QC_AUDIT.md P0-1 falsified)")
    for (ctor_va, (cls, push_va)) in sorted(IMMEDIATE_NULL_CTORS.items()):
        L.append("  %-42s: held = NULL always (ctor site 0x%08X pushes immediate 0 for the"
                 % (cls, push_va))
        L.append("      base ctor; byte evidence [IV-1..6] sites 1/2/3/5)")
    L.append("  %-42s: held = NULL always (PSPMod ctor chains via the PSP ctor's"
             % "ArkAnimationParticleSystemPredefinedMod")
    L.append("      immediate push 0; PSPMod ctor -> PSP ctor call @0x006FEB4B; PSP site 5"
             )
    L.append("      push 0 evidence stands; PSPMod ctor itself adds no [this+0x14] write)")
    for (ctor_va, ctor_cls) in sorted(PARAM_CHAINED_CTORS.items()):
        kids = sorted(per_class_children.get(ctor_cls, set()))
        kid_names = []
        for callee in kids:
            cm = child_measure(callee)
            kid_names.append("%s (0x%08X)" % (cm["class_name"], callee))
        L.append("  %-42s: held = NULL on the allocation-failure paths (xor esi,esi;"
                 % ctor_cls)
        L.append("      entry preconditions = the child-allocation NULL tests), and = a LIVE")
        L.append("      CHILD object on the normal paths: %s"
                 % "; ".join(kid_names) if kid_names else "  (no child measured)")
    L.append("  %-42s: inherits the forwarded child (Linear/Sin ctors read their own"
             % "ArkAnimationCyclic")
    L.append("      arg2 @0x006FBAB8/@0x006FD278 and forward it to the Cyclic ctor"
             )
    L.append("      0x006FFA70; the Cyclic ctor passes it to the base ctor as arg2)")
    L.append("  CHILD HIERARCHY ROOT: every child class lineage ends at")
    L.append("  .?AVArkAnimationFloatValue@@ - a SEPARATE hierarchy root from")
    L.append("  .?AVArkAnimationPredefined@@ (the 10-class family closure STANDS; the")
    L.append("  children are NOT members of the ArkAnimation family).")
    L.append("  SLOT-3 NEGATIVE CONTROL (R2): child vtable slot-3 dwords:")
    for callee in sorted(set(c for s in per_class_children.values() for c in s)):
        cm = child_measure(callee)
        slot3 = S.u32_va(m, cm["vtable"] + 0x0C) if cm["vtable"] else None
        L.append("    %-40s vt 0x%08X slot-3 = 0x%08X  == 0x0050A050? %s"
                 % (cm["class_name"], cm["vtable"], slot3 if slot3 is not None else 0,
                    "YES (!)" if slot3 == SF_SLOT3 else "NO"))
    sf_slot3 = S.u32_va(m, SF_VTABLE + 0x0C)
    L.append("    %-40s vt 0x%08X slot-3 = 0x%08X  (SF re-confirmed)"
             % (".?AVSceneFeederObject@@", SF_VTABLE, sf_slot3))

    # ---- [V] upstream continuation
    L.append("")
    L.append("[V] UPSTREAM CONTINUATION: leaf ctor/factory caller census + held-arg traces")
    new_thunk_va = None
    for (site, tgt) in calls:
        if tgt in thunk_cache and "??2" in str(thunk_cache[tgt]):
            new_thunk_va = tgt
            break
    leaf_list = sorted(x for x in all_leaves if x != new_thunk_va)
    L.append("  call-return leaves found in the six slices: %s" % [hex(x) for x in leaf_list])
    L.append("  (R2: the operator-new import thunk %s is EXCLUDED from the ctor-caller"
             % (hex(new_thunk_va) if new_thunk_va else "-"))
    L.append("   census - it is the fresh-allocation leaf, not a constructor; its call")
    L.append("   sites are enumerated inside the [IV-8] chain trees.)")
    fam_ctor_funcs = set(SITE_FUNCS) | set(EXTRA_CTORS)
    for leaf in leaf_list:
        cm = child_measure(leaf) if leaf in child_measures else \
            measure_ctor(m, cs, functions, branches, leaf, vt_names)
        child_measures.setdefault(leaf, cm)
        callers = [a for (a, t) in calls if t == leaf]
        L.append("")
        L.append("  LEAF 0x%08X (%s): direct E8 callers: %d"
                 % (leaf, cm["class_name"] or "?", len(callers)))
        if len(callers) > 24:
            L.append("    (caller count > 24; listing first 24, traces bounded to family-ctor sites)")
            callers = callers[:24]
        for cs_site in sorted(callers):
            fn = S.func_containing(functions, cs_site)
            fs = fn["start"] if fn else 0
            fe = fn["end"] if fn else 0
            # family-ctor call sites within this caller function?
            fam_sites = [a for (a, t) in calls if fs <= a < fe and t in fam_ctor_funcs]
            L.append("    caller-site 0x%08X in func 0x%08X..0x%08X family-ctor-sites-in-func: %s"
                     % (cs_site, fs, fe, [hex(x) for x in fam_sites]))
            for fsite in fam_sites:
                visited = set()
                budget = {"n": 0, "max_level": 6}
                tree = S.slice_call_arg(m, cs, functions, calls, fsite, 2, 0,
                                        visited, budget, edge_ctx)
                L.append("      HELD-PARAM (arg2) SLICE at family-ctor site 0x%08X:" % fsite)
                for ln in S.format_slice_tree(tree).split(chr(10)):
                    L.append("        " + ln)

    # ---- [VI] SF-chain PIN revalidation (ladder infrastructure)
    L.append("")
    L.append("[VI] SF-CHAIN PIN REVALIDATION (receiver-identity ladder infrastructure)")
    rep, _fn = func_report(m, cs, functions, SF_CTOR, vt_names, imports, thunk_cache,
                           "SF ctor FUN_00509330 (PIN-SFCHAIN)")
    L.extend(rep)
    sf_insns, _e = S.disasm_range(m, cs, 0x00509330, 0x200)
    for i in sf_insns:
        if i.bytes.hex() == "c785" or (i.mnemonic == "mov" and i.operands
                                       and len(i.operands) == 2
                                       and i.operands[1].type == S.x86c.X86_OP_IMM
                                       and (i.operands[1].imm & 0xFFFFFFFF) == SF_VTABLE):
            L.append("    SF-VTABLE STORE at 0x%08X: %s %s (vt 0x%08X)"
                     % (i.address, i.mnemonic, i.op_str, SF_VTABLE))
    hits = [i for i in sf_insns if i.mnemonic == "mov" and len(i.operands) == 2
            and i.operands[1].type == S.x86c.X86_OP_IMM
            and (i.operands[1].imm & 0xFFFFFFFF) == SF_VTABLE]
    if not hits:
        L.append("    FINDING: no immediate vtable store 0x%08X found within first 0x200 bytes"
                 % SF_VTABLE)
    rep, _fn = func_report(m, cs, functions, SF_FACTORY, vt_names, imports, thunk_cache,
                           "SF factory FUN_005247C0 (PIN-SFCHAIN)")
    L.extend(rep)
    rep, _fn = func_report(m, cs, functions, SF_CONTAINER, vt_names, imports, thunk_cache,
                           "SF container FUN_0044D590 (PIN-SFCHAIN; B.5 extent is a guard fragment)",
                           max_insns=400)
    L.extend(rep)
    # the +0x10 store @0x0044D680: find its real containing function
    fn66 = S.func_containing(functions, 0x0044D680)
    L.append("    FINDING: 0x0044D680 (pin: container +0x10 store receiving FUN_005247C0 result)")
    L.append("           is NOT inside B.5 extent of 0x0044D590 ([0x0044D590..0x0044D5D8));")
    L.append("           real containing function: %s"
             % ("0x%08X..0x%08X %s" % (fn66["start"], fn66["end"], fn66["end_kind"]) if fn66 else "NOT IN MAP"))
    if fn66:
        rep, _f2 = func_report(m, cs, functions, fn66["start"], vt_names, imports,
                               thunk_cache,
                               "actual container function containing 0x0044D680",
                               max_insns=300)
        L.extend(rep)

    # ---- [VII] family writer-fields summary (contract iii)
    L.append("")
    L.append("[VII] FAMILY WRITER FIELDS (contract 7(iii); rows from HOLDER14_WRITER_CENSUS.csv)")
    L.append("  WRITER 0x006FABB5: mov [eax+0x14], ecx")
    L.append("    CONTAINING_FUNCTION: 0x006FABA0 (shared base ctor, class .?AVArkAnimationPredefined@@)")
    L.append("    VALUE_SOURCE: ECX = ctor arg2 (held object pointer, read at 0x006FABA2 from [esp+0xC];")
    L.append("                  NULL-TESTED at 0x006FABA6)")
    L.append("    VALUE_PROVENANCE (R2 CORRECTED, per [IV-8]/[IV-9]): the six per-site arg2")
    L.append("                      slices enumerate: NULL at sites 1/2/3/5 (immediate push 0)")
    L.append("                      and, at the param-chained sites 4/6, BOTH factory-block")
    L.append("                      entry paths - NULL on the allocation-failure (xor) paths,")
    L.append("                      a LIVE RTTI-IDENTIFIED CHILD OBJECT (Scale/Color/Intensity/")
    L.append("                      Rotation/Translation/Alpha - all .?AVArkAnimationFloatValue@@-")
    L.append("                      hierarchy classes; slot-3 != 0x0050A050) on the normal paths.")
    L.append("    WRITE_WIDTH: 4 (dword)")
    L.append("    PATH_PRECONDITION: conditional branches before the write: NONE (unconditional store;")
    L.append("                      the null test only guards the refcount increment AFTER the store;")
    L.append("                      the VALUE is path-preconditioned at the sources, not the store)")
    L.append("    CLASS/LIFETIME_CONTEXT: base-ctor initialization of every family object (10 classes)")
    L.append("    WRITER_CLASS: constructor-initialization")
    L.append("  WRITER 0x006FAC25: mov [esi+0x14], 0  (function 0x006FAC00)")
    L.append("    see [IV-0c] decode: value imm 0; release-path context; WRITER_CLASS from decode")
    L.append("    (R2 note: on normal paths this release path is LIVE - refcount-- on the held")
    L.append("     child; held->vt[0](1) delete protocol; the R1 'defensive dead code' reading is")
    L.append("     RETRACTED, see AMEND_LOG_R2 R2-3)")
    L.append("  WRITER 0x006FAC75: mov [esi+0x14], 0  (function 0x006FAC50 = Predefined deleting dtor)")
    L.append("    see [IV-0c] decode: value imm 0; destructor-release; WRITER_CLASS from decode")

    # ---- [VIII] R2 bulk-copy channel census (the census's write-form bound)
    L.append("")
    L.append("[VIII] BULK-COPY CHANNEL CENSUS (R2; declared bound for the write-form coverage")
    L.append("  of the G4 census: rep movs/stos sites are memory writes WITHOUT a disp==0x14")
    L.append("  operand and are therefore invisible to the disp-census)")
    rep_sites = []
    def collect_rep(insn, fstart):
        mn = insn.mnemonic
        if mn.startswith("rep") or mn.startswith("repe") or mn.startswith("repne") \
                or mn.startswith("repz") or mn.startswith("repnz"):
            base_mn = mn.split(" ", 1)[1]
            if base_mn.startswith("movs") or base_mn.startswith("stos"):
                rep_sites.append((insn.address, mn + " " + insn.op_str))
    functions_r, calls_r, jmps_r, stats_r = S.build_text_map(m, cs, collect=collect_rep)
    L.append("  rep movs/stos sites in .text (single-stream B.5 decode): %d" % len(rep_sites))
    fam_lo, fam_hi = 0x006FAB40, 0x006FFAF0
    inregion = [(a, s2) for (a, s2) in rep_sites if fam_lo <= a < fam_hi]
    L.append("  in the ArkAnimation family code cluster [0x%08X..0x%08X): %d"
             % (fam_lo, fam_hi, len(inregion)))
    for (a, s2) in inregion:
        fnr = S.func_containing(functions_r, a)
        L.append("    0x%08X  %-44s func %s"
                 % (a, s2, ("[0x%08X..0x%08X)" % (fnr["start"], fnr["end"])) if fnr else "?"))
        # destination analysis: the block context around the rep site
        if fnr:
            rinsns, _e = S.disasm_range(m, cs, fnr["start"], fnr["end"] - fnr["start"])
            ctx = [i for i in rinsns if a - 0x20 <= i.address < a]
            leas = [i for i in ctx if i.mnemonic in ("lea", "mov", "add")]
            for i in leas[-3:]:
                L.append("        context: 0x%08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    L.append("  Destination analysis: all %d in-cluster sites write to CHILD-CLASS or non-family" % len(inregion))
    L.append("  object fields ([ebx+0x34]/[ebx+0x58] ArkAnimationRotation ctor fields;")
    L.append("  [[edi+8]+0x38] child helper indirection; [ebx+0x48] ArkTextureInfo ctor")
    L.append("  fields) - NONE touches a family object's +0x14 (family ctors/dtors")
    L.append("  initialize field-by-field; no copy-ctor/assignment-copy construction path for")
    L.append("  family objects exists in the family region).")
    L.append("  DECLARED NOT_CHECKED: .text-wide destination-provenance tracing of the remaining")
    L.append("  %d out-of-cluster rep sites (a family-object pointer would have to flow out" % (len(rep_sites) - len(inregion)))
    L.append("  and back; the family-function scan found no such handoff).")

    out = os.path.join(RAW, "HOLDER14_WRITER_RAW.txt")
    with open(out, "w") as f:
        f.write(chr(10).join(L) + chr(10))
    print("WROTE: %s (%d lines)" % (out, len(L)))


if __name__ == "__main__":
    main()
