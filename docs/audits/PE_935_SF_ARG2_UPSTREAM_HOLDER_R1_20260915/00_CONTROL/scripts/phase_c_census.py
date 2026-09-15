"""
phase_c_census.py - PHASE C (i)+(ii) (G4): full-.text [mem+0x14] WRITE census.
Single-stream B.5 pass (same engine as Phase B, independently re-derived),
census of every memory-WRITE operand with displacement 0x14, per-row function
attribution and family classification.
Writes 01_RAW/HOLDER14_WRITER_CENSUS.csv, 01_RAW/HOLDER14_CENSUS_SUMMARY.txt,
01_RAW/B5_FUNCTION_MAP.csv.
Re-measures size+SHA256+PE layout FIRST (fail-closed).
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
SLICE_MAX_CALLERS_X = 16


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()

    # ---- independent re-derivation of the five thunk-member vtables
    occ = S.find_dword_occurrences(m, THUNK)
    slot_hits = [va for (off, va, aligned) in occ
                 if va and aligned and S.section_of_va(m, va)
                 and S.section_of_va(m, va)["name"] in (".rdata", ".data")]
    five_vts = {}
    for slot_va in slot_hits:
        vt = S.vtable_from_slot(m, slot_va)
        if vt:
            five_vts[vt["vtable_start"]] = vt["class_name"]
    core_names = set(five_vts.values())

    # ---- family classes: all inventory classes whose lineage intersects the five
    inv = S.vtable_inventory(m)
    vt_names_all = {}
    for r in inv:
        vt_names_all[r["vtable_start"]] = r["class_name"]
    name_to_vts = {}
    for r in inv:
        name_to_vts.setdefault(r["class_name"], []).append(r["vtable_start"])
    family_vts = {}   # vtable_start -> class name
    for r in inv:
        chd = S.read_chd(m, r["col"]["p_class_hierarchy"])
        if chd is None:
            continue
        lineage = set(b["name"] for b in chd["bases"])
        if r["class_name"] in core_names or (lineage & core_names):
            family_vts[r["vtable_start"]] = r["class_name"]

    # ---- census + store collection + lattice in ONE map pass
    census = []
    vt_set = set(family_vts.keys())
    stores = []

    def collect(insn, fstart):
        ops = insn.operands
        if insn.mnemonic == "mov" and len(ops) == 2:
            if ops[0].type == S.x86c.X86_OP_MEM and ops[1].type == S.x86c.X86_OP_IMM:
                v = ops[1].imm & 0xFFFFFFFF
                if v in vt_set:
                    stores.append((insn.address, v, insn.op_str, fstart))

    branches = []
    functions, calls, jmps, stats = S.build_text_map(m, cs, collect=collect,
                                                     census_14=census,
                                                     branches=branches)

    # ---- family function set
    famfuncs = {}   # func_va -> reason/class
    for vstart, cname in family_vts.items():
        end, entries, stop = S.vtable_extent(m, vstart)
        for e in entries:
            famfuncs.setdefault(e, "vtable slot of %s (vt 0x%08X)" % (cname, vstart))
    famfuncs.setdefault(SHARED_CTOR, "shared base ctor (ArkAnimationPredefined)")

    # vtable-store functions (ctor/dtor of family classes)
    for (iva, v, ostr, fstart) in stores:
        famfuncs.setdefault(fstart, "stores family vtable 0x%08X (%s)"
                            % (v, family_vts.get(v, "?")))

    # six shared-ctor call sites re-derivation + containing functions
    ctor_sites = [(a, t) for (a, t) in calls if t == SHARED_CTOR]
    site_funcs = set()
    for (site, _t) in ctor_sites:
        fn = S.func_containing(functions, site)
        if fn:
            site_funcs.add(fn["start"])
            famfuncs.setdefault(fn["start"],
                                "E8-calls shared ctor at 0x%08X" % site)

    # callers of family ctor functions (one level: factory/lifetime context)
    ctor_func_starts = set(f for f in site_funcs)
    ctor_callers = set()
    for (site, tgt) in calls:
        if tgt in ctor_func_starts:
            fn = S.func_containing(functions, site)
            if fn and fn["start"] not in famfuncs:
                ctor_callers.add((fn["start"], site))

    # R2 (QC P3-2): COMPLETE family-ctor caller census. Family ctor functions
    # = the six shared-ctor base callers + family functions that call another
    # family ctor (chained ctors: CyclicLinear/CyclicSin via Cyclic;
    # ParticleSystemPredefinedMod via PSP), discovered to a fixpoint.
    fam_ctor_funcs = set(site_funcs)
    for _ in range(8):
        grown = False
        for (site, tgt) in calls:
            if tgt in fam_ctor_funcs:
                fn = S.func_containing(functions, site)
                if fn and fn["start"] in famfuncs \
                        and fn["start"] not in fam_ctor_funcs:
                    fam_ctor_funcs.add(fn["start"])
                    grown = True
        if not grown:
            break
    ctor_class_name = {}
    for fv in sorted(fam_ctor_funcs):
        fn = S.func_containing(functions, fv)
        if not fn:
            continue
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        for i in insns:
            ops = i.operands
            if i.mnemonic == "mov" and len(ops) == 2 \
                    and ops[0].type == S.x86c.X86_OP_MEM \
                    and ops[1].type == S.x86c.X86_OP_IMM:
                v = ops[1].imm & 0xFFFFFFFF
                if v in family_vts:
                    ctor_class_name[fv] = family_vts[v]
                    break

    # reverse lattice: caller->callee map for hints
    callers_of = {}
    for (site, tgt) in calls:
        fn = S.func_containing(functions, site)
        if fn:
            callers_of.setdefault(tgt, set()).add(fn["start"])

    # ---- classify rows
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: HOLDER14_CENSUS_SUMMARY.txt (Phase C i+ii)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_c_census.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("=" * 80)
    L.append("")
    L.append("[C0] B.5 MAP PASS (independent re-derivation; cross-check vs Phase B)")
    L.append("  functions=%d calls=%d jmps=%d insns=%d" %
             (len(functions), len(calls), len(jmps), stats["insns"]))
    L.append("  end_kinds: pad=%d tight=%d oversized=%d desync=%d edge=%d pad_insns=%d"
             % (stats["pad_ends"], stats["tight_ends"], stats["oversized"],
                stats["resyncs"], stats["edge_ends"], stats["pad_insns"]))
    L.append("")
    L.append("[C1] THUNK-MEMBER VTABLES (re-derived): %d" % len(five_vts))
    for vstart, nm in sorted(five_vts.items()):
        L.append("  0x%08X %s" % (vstart, nm))
    L.append("")
    L.append("[C2] FAMILY CLASSES (core five + inventory lineage closure): %d classes"
             % len(set(family_vts.values())))
    for vstart in sorted(family_vts):
        L.append("  vt 0x%08X %s" % (vstart, family_vts[vstart]))
    L.append("")
    L.append("[C3] SHARED-CTOR E8 SITES (re-derived): %d" % len(ctor_sites))
    for (site, _t) in sorted(ctor_sites):
        L.append("  0x%08X" % site)
    L.append("")
    L.append("[C4] FAMILY-CTOR CALLER CENSUS (R2 COMPLETE; QC P3-2 fix: every")
    L.append("    direct E8 call site of every family ctor function, with the")
    L.append("    containing function and its context class - not a partial list)")
    for fv in sorted(fam_ctor_funcs):
        sites = sorted(a for (a, t) in calls if t == fv)
        L.append("  ctor 0x%08X (%s): %d direct E8 call site(s)"
                 % (fv, ctor_class_name.get(fv, "?"), len(sites)))
        for site in sites:
            fn = S.func_containing(functions, site)
            fs = fn["start"] if fn else 0
            if fs in famfuncs and fs != fv:
                ctx = "FAMILY-INTERNAL (caller 0x%08X is itself a family function)" % fs
            elif fs in famfuncs and fs == fv:
                ctx = "FAMILY-INTERNAL (self-recursion?; recorded honestly)"
            else:
                ctx = ("NON-FAMILY caller function 0x%08X (factory/lifetime "
                       "context)" % fs)
            L.append("    call site 0x%08X in func %s" % (site, ctx))
    L.append("")

    # classification loop (criterion (a) = enclosing function; criterion (b) =
    # written base's def provably flows from family construction within the
    # declared bound: per-row base-def slice + family-vtable fingerprint scan)

    def vt_fingerprint(fn, breg):
        """(b2) family-vtable fingerprint: does this function store a family
        vtable VA into [breg+0]? Returns (va, class) or None."""
        if fn is None or breg == "":
            return None
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        for i in insns:
            ops = i.operands
            if i.mnemonic == "mov" and len(ops) == 2 \
                    and ops[0].type == S.x86c.X86_OP_MEM \
                    and ops[1].type == S.x86c.X86_OP_IMM:
                wkey = S.mem_key_of(i, ops[0])
                if wkey[0] == breg and wkey[1] is None and wkey[3] == 0:
                    v = ops[1].imm & 0xFFFFFFFF
                    if v in family_vts:
                        return (i.address, family_vts[v])
        return None

    def collect_call_leaves(node, out):
        if node.kind == "CALL_RETURN":
            mm = re.search(r"def via call (0x[0-9A-Fa-f]+) -> callee (0x[0-9A-Fa-f]+)",
                           node.detail)
            if mm:
                out.append((int(mm.group(1), 16), int(mm.group(2), 16))
                           )
        if node.kind == "CALL_RETURN" and not mm:
            mm2 = re.search(r"callee (0x[0-9A-Fa-f]+)", node.detail)
            if mm2:
                out.append((0, int(mm2.group(1), 16)))
        for c in node.children:
            collect_call_leaves(c, out)
        return out

    ctor_class_cache = {}
    def ctor_class_of(callee):
        """Resolve the class whose (sub)object a constructor/function produces:
        first vtable-store immediate in the function, matched against the
        vtable inventory. Cached per callee."""
        if callee in ctor_class_cache:
            return ctor_class_cache[callee]
        res = "UNKNOWN"
        f = S.b5_function(m, cs, callee, max_bytes=8192)
        if not f["insns"]:
            res = "UNDECODEABLE"
        else:
            for i in f["insns"]:
                ops = i.operands
                if i.mnemonic == "mov" and len(ops) == 2 \
                        and ops[0].type == S.x86c.X86_OP_MEM \
                        and ops[1].type == S.x86c.X86_OP_IMM:
                    v = ops[1].imm & 0xFFFFFFFF
                    if v in family_vts:
                        res = "FAMILY:" + family_vts[v]
                        break
                    if v in vt_names_all:
                        res = "OTHER:" + vt_names_all[v]
                        break
        ctor_class_cache[callee] = res
        return res

    def new_chain_class(new_call_va):
        """operator-new chain: first E8 call within 48 bytes after the new
        call whose target is a class ctor (vtable store) -> class."""
        fn = S.func_containing(functions, new_call_va)
        if fn is None:
            return "UNKNOWN"
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        tail = [i for i in insns if new_call_va < i.address < new_call_va + 48
                and i.mnemonic == "call"]
        for i in tail:
            if i.operands and i.operands[0].type == S.x86c.X86_OP_IMM:
                t = i.operands[0].imm & 0xFFFFFFFF
                cls = ctor_class_of(t)
                if cls not in ("UNKNOWN", "UNDECODEABLE"):
                    return cls
        return "UNKNOWN"

    NEW_THUNK = None
    imports = S.parse_imports(m)
    for (site, tgt) in calls[:4000]:
        _t, iname = S.thunk_target_import(m, cs, imports, tgt)
        if iname and "??2" in iname:
            NEW_THUNK = tgt
            break

    def leaves_classify(tree, depth_budget=1):
        """Classify a base/value slice tree: returns (verdict, evidence list).
        verdict in PROVEN_FAMILY / PROVEN_OTHER(<class>) / UNPROVEN."""
        ev = []
        leaves = collect_call_leaves(tree, [])
        fam = False
        others = set()
        unknown = False
        for (csite, callee) in leaves:
            if NEW_THUNK is not None and callee == NEW_THUNK:
                cls = new_chain_class(csite)
                ev.append("new-chain@0x%08X -> %s" % (csite, cls))
                if cls.startswith("FAMILY:"):
                    fam = True
                elif cls.startswith("OTHER:"):
                    others.add(cls)
                else:
                    unknown = True
                continue
            cls = ctor_class_of(callee)
            ev.append("callee 0x%08X -> %s" % (callee, cls))
            if cls.startswith("FAMILY:"):
                fam = True
            elif cls.startswith("OTHER:"):
                others.add(cls)
            else:
                unknown = True
        kinds = []
        def walk(n):
            kinds.append(n.kind)
            for c in n.children:
                walk(c)
        walk(tree)
        if "THIS_ENTRY" in kinds:
            ev.append("this-entry(thiscall this)")
        if "PARAM" in kinds:
            ev.append("param-caller-cross")
        if fam:
            return ("PROVEN_FAMILY", ev)
        if others and not unknown:
            return ("PROVEN_OTHER:" + "|".join(sorted(others)), ev)
        if others:
            return ("MIXED_OTHER_UNKNOWN:" + "|".join(sorted(others)), ev)
        return ("UNPROVEN", ev)

    def this_cross(func_start, level, visited, budget):
        """Caller census + ECX def slices for a thiscall method whose this
        register reached function entry undef."""
        out = []
        callers = [site for (site, tgt) in calls if tgt == func_start]
        if not callers:
            return [("UNPROVEN", ["no-direct-callers (virtual-only or indirect)"])]
        if len(callers) > SLICE_MAX_CALLERS_X:
            return [("UNPROVEN", ["too-many-callers:%d" % len(callers)])]
        for site in callers:
            t = S.slice_reg(m, cs, functions, calls, site, "ecx", level,
                            visited, budget)
            verdict, ev = leaves_classify(t)
            out.append((verdict, ["caller-site 0x%08X" % site] + ev))
        return out

    def deep_base_verdict(fn, va, breg):
        """Phase-2 criterion-(b): deep base slice + this-cross + class leaves.
        Returns (verdict, results, tree) - the tree carries the leaf kinds for
        the R2 [C8] histogram (QC P2-2 fix)."""
        budget = {"n": 0, "max_level": 3}
        visited = set()
        tree = S.slice_reg(m, cs, functions, calls, va, breg, 0, visited, budget)
        verdict, ev = leaves_classify(tree)
        results = [(verdict, ev)]
        kinds = []
        def walk(n):
            kinds.append(n.kind)
            for c in n.children:
                walk(c)
        walk(tree)
        if "THIS_ENTRY" in kinds and fn is not None:
            for (vx, ex) in this_cross(fn["start"], 1, visited, budget):
                results.append((vx, ["this-cross"] + ex))
        # aggregate
        fam = any(v == "PROVEN_FAMILY" for (v, _) in results)
        others = set()
        unknown = False
        for (v, _) in results:
            if v.startswith("PROVEN_OTHER:") or v.startswith("MIXED"):
                for part in v.split(":", 1)[1].split("|"):
                    if part:
                        others.add(part)
            if v == "UNPROVEN":
                unknown = True
        if fam:
            return ("PROVEN_FAMILY", results, tree)
        if others and not unknown:
            return ("PROVEN_OTHER:" + "|".join(sorted(others)), results, tree)
        return ("UNPROVEN", results, tree)

    def tree_leaf_kinds(node, out):
        if not node.children:
            out.append(node.kind)
        else:
            for c in node.children:
                tree_leaf_kinds(c, out)
        return out

    def tree_has_kind(node, kind):
        if node.kind == kind:
            return True
        return any(tree_has_kind(c, kind) for c in node.children)

    def primary_leaf_class(tree):
        """R2 declared classification rule for the [C8] histogram (QC P2-2):
        if the base-def tree crossed to callers (any PARAM node), the row is
        PARAM_CHAIN; else the row's class is the FIRST leaf kind in
        depth-first order. Sums to the NON_FAMILY row count by construction."""
        if tree_has_kind(tree, "PARAM"):
            return "PARAM_CHAIN"
        kinds = []
        tree_leaf_kinds(tree, kinds)
        return kinds[0] if kinds else "EMPTY"

    rows = []
    counts = dict(total=0, stack_frame=0, absolute=0, sib=0, reg_indirect=0,
                  family=0, family_by_a=0, family_by_b=0, non_family=0,
                  unknown=0, no_func=0)
    family_row_details = []
    # R2 [C8] histogram accumulators (QC P2-2 fix)
    leaf_hist = {}
    leaf_hist_rows = []
    # R2: edge-aware context for the FAMILY-row VALUE provenance slices (the
    # criterion-b deep slices for NON-family rows stay on the R1 model so the
    # census classifications remain byte-identical to the QC-verified R1 pass)
    edge_ctx = S.EdgeContext(branches)
    for (va, mn, op_str, bhex, fstart, width, breg, ireg, scale) in census:
        counts["total"] += 1
        fn = S.func_containing(functions, va)
        if fn is None:
            counts["no_func"] += 1
        if breg in ("esp", "ebp"):
            counts["stack_frame"] += 1
            cat = "STACK_FRAME"
        elif breg == "":
            counts["absolute"] += 1
            cat = "ABSOLUTE"
        elif ireg != "":
            counts["sib"] += 1
            cat = "SIB"
        else:
            counts["reg_indirect"] += 1
            cat = "REG_INDIRECT"
        # find the write operand + source operand for writer fields
        src_desc = ""
        write_insn = None
        if fn is not None:
            insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
            for i in insns:
                if i.address == va:
                    write_insn = i
                    break
        if write_insn is not None:
            ops = write_insn.operands
            for k, op in enumerate(ops):
                if op.type == S.x86c.X86_OP_MEM and op.mem.disp == 0x14 \
                        and k in [x[0] for x in S.mem_write_ops(write_insn)]:
                    if k + 1 < len(ops) and ops[k + 1].type == S.x86c.X86_OP_REG:
                        src_desc = "reg:" + write_insn.reg_name(ops[k + 1].reg)
                    elif k + 1 < len(ops) and ops[k + 1].type == S.x86c.X86_OP_IMM:
                        src_desc = "imm:0x%08X" % (ops[k + 1].imm & 0xFFFFFFFF)
                    elif k + 1 < len(ops) and ops[k + 1].type == S.x86c.X86_OP_MEM:
                        src_desc = "mem:" + S._key_str(S.mem_key_of(write_insn, ops[k + 1]))
                    else:
                        src_desc = "?"
        if fn is None:
            cls = "UNKNOWN_CONTEXT"
            reason = "row VA not inside any B.5-mapped function (padding/desync)"
            counts["unknown"] += 1
            crit = ""
        elif cat in ("STACK_FRAME", "ABSOLUTE", "SIB"):
            cls = "EXCLUDED_FORM"
            reason = ("base is esp/ebp (stack-frame write)" if cat == "STACK_FRAME"
                      else ("absolute address" if cat == "ABSOLUTE"
                            else "SIB/indexed form (enumerated separately)"))
            crit = ""
        elif fn["start"] in famfuncs:
            cls = "FAMILY_CONTEXT_PROVEN"
            reason = famfuncs[fn["start"]]
            crit = "ENCLOSING_FAMILY_FUNCTION"
            counts["family"] += 1
            counts["family_by_a"] += 1
        else:
            # criterion (b): per-row base proof (phase 1 fingerprint + phase 2
            # deep slice with this-cross, caller-cross, ctor/new-chain classing)
            fp = vt_fingerprint(fn, breg)
            if fp is not None:
                cls = "FAMILY_CONTEXT_PROVEN"
                reason = ("criterion (b): base reg '%s' receives family vtable store "
                          "at 0x%08X (%s) in same function" % (breg, fp[0], fp[1]))
                crit = "BASE_VTABLE_FINGERPRINT"
                counts["family"] += 1
                counts["family_by_b"] += 1
            else:
                verdict, results, btree = deep_base_verdict(fn, va, breg)
                hist_class = primary_leaf_class(btree)
                leaf_hist[hist_class] = leaf_hist.get(hist_class, 0) + 1
                leaf_hist_rows.append((va, hist_class))
                if verdict == "PROVEN_FAMILY":
                    cls = "FAMILY_CONTEXT_PROVEN"
                    crit = "BASE_DEF_FLOWS_FROM_FAMILY_CONSTRUCTION"
                    ev_txt = "; ".join(x for (v, e) in results[:3] for x in e[:4])
                    reason = ("criterion (b): base-def deep slice proves family "
                              "construction [%s]" % ev_txt[:300])
                    counts["family"] += 1
                    counts["family_by_b"] += 1
                else:
                    cls = "NON_FAMILY_OUT_OF_SCOPE"
                    crit = ""
                    ev_txt = "; ".join(x for (v, e) in results[:2] for x in e[:3])
                    reason = ("base-def verdict %s [%s]"
                              % (verdict, ev_txt[:240]))
                    counts["non_family"] += 1
        rows.append((va, mn, op_str, bhex, fstart, width, breg, ireg, scale,
                     cat, cls, reason, crit))
        if cls == "FAMILY_CONTEXT_PROVEN":
            # writer fields (contract 7(iii)) + VALUE provenance slice
            # R2: the VALUE slice runs EDGE-AWARE (the 0x006FABB5 value
            # provenance crosses into the dispatcher construct; the R2
            # engine enumerates the factory-block paths there)
            vbudget = {"n": 0, "max_level": 6}
            vvisited = set()
            vtree = None
            if src_desc.startswith("reg:"):
                vtree = S.slice_reg(m, cs, functions, calls, va,
                                    src_desc[4:], 0, vvisited, vbudget,
                                    edge_ctx)
            elif src_desc.startswith("mem:"):
                if write_insn is not None:
                    for k, op in enumerate(write_insn.operands):
                        if op.type == S.x86c.X86_OP_MEM and op.mem.disp != 0x14 \
                                and k > 0:
                            vtree = S.slice_mem(m, cs, functions, calls, va,
                                                S.mem_key_of(write_insn, op),
                                                0, vvisited, vbudget,
                                                edge_ctx)
                            break
            elif src_desc.startswith("imm:"):
                vtree = S.SliceNode("IMMEDIATE", src_desc, 0, "")
            vverdict = "NOT_SLICED"
            vev = []
            if vtree is not None:
                vverdict, vev = leaves_classify(vtree)
            cond = []
            if fn is not None:
                insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
                cond = [i for i in insns if va - 32 <= i.address < va
                        and i.mnemonic.startswith("j") and i.mnemonic != "jmp"]
            family_row_details.append((va, mn, op_str, fstart, src_desc, width,
                                       [hex(x.address) + ":" + x.mnemonic for x in cond],
                                       cls, crit, reason, vverdict, vev))

    L.append("[C5] CENSUS DENOMINATORS AND CLASSIFICATION COUNTS")
    L.append("  denominator (all mem-WRITE disp==0x14 rows in .text): %d" % counts["total"])
    L.append("  base-register categories: REG_INDIRECT=%d STACK_FRAME=%d SIB=%d ABSOLUTE=%d"
             % (counts["reg_indirect"], counts["stack_frame"], counts["sib"], counts["absolute"]))
    L.append("  classifications: FAMILY_CONTEXT_PROVEN=%d (criterion a=%d, criterion b=%d)"
             % (counts["family"], counts["family_by_a"], counts["family_by_b"]))
    L.append("                    NON_FAMILY_OUT_OF_SCOPE=%d UNKNOWN_CONTEXT=%d"
             % (counts["non_family"], counts["unknown"]))
    L.append("  criterion (b) method (phase 2, applied to every non-criterion-a row):")
    L.append("  family-vtable fingerprint scan on the base register in the containing")
    L.append("  function + base-def backward slice (levels<=3, 384-byte window,")
    L.append("  clobber-aware, caller-cross + this-cross via ECX caller slices,")
    L.append("  constructor class resolution incl. operator-new chains).")
    L.append("")
    L.append("[C6] ALL FAMILY_CONTEXT_PROVEN ROWS (full writer fields; contract 7(iii))")
    for (va, mn, op_str, fstart, src_desc, width, cond, cls, crit, reason,
         vverdict, vev) in family_row_details:
        L.append("  WRITER_VA 0x%08X: %s %s" % (va, mn, op_str))
        L.append("    CONTAINING_FUNCTION: 0x%08X" % fstart)
        L.append("    VALUE_SOURCE: %s" % (src_desc if src_desc else "(see anchor raw)"))
        L.append("    WRITE_WIDTH: %d" % width)
        L.append("    PATH_PRECONDITION: cond-branches in 32B before row: %s"
                 % (cond if cond else "NONE"))
        L.append("    CLASS/LIFETIME_CONTEXT: %s" % reason)
        L.append("    CRITERION: %s" % crit)
        L.append("    VALUE_PROVENANCE_VERDICT: %s" % vverdict)
        if vev:
            L.append("    VALUE_PROVENANCE_EVIDENCE: %s"
                     % "; ".join(x for x in vev[:8]))
    L.append("")
    L.append("[C7] UNKNOWN_CONTEXT ROWS (attribution failures - honesty list)")
    unk = [r for r in rows if r[10] == "UNKNOWN_CONTEXT"]
    if not unk:
        L.append("  none")
    for r in unk:
        L.append("  0x%08X %-8s %-34s" % (r[0], r[1], r[2]))

    # ---- [C8] R2 leaf-verdict histogram over the NON_FAMILY rows (QC P2-2 fix:
    # the R1 printed breakdown summed to 1,892 instead of 1,895; this one is
    # regenerated from the same per-row base-def slices the classification used)
    L.append("")
    L.append("[C8] LEAF-VERDICT HISTOGRAM over the %d NON_FAMILY rows (R2;" % counts["non_family"])
    L.append("  declared rule: PARAM_CHAIN if the base-def slice crossed to callers")
    L.append("  (any PARAM node in the tree); else the FIRST leaf kind in")
    L.append("  depth-first order of the row's base-def slice tree; the R1 model")
    L.append("  applies (criterion-b slices are not edge-aware))")
    hist_total = 0
    for cls2 in sorted(leaf_hist):
        L.append("    %-16s = %d rows" % (cls2, leaf_hist[cls2]))
        hist_total += leaf_hist[cls2]
    L.append("    TOTAL            = %d rows == NON_FAMILY_OUT_OF_SCOPE count: %s"
             % (hist_total, hist_total == counts["non_family"]))
    L.append("  (R1 AMEND_LOG note: the R1 development-pass breakdown printed in")
    L.append("   HOLDER14_PROVENANCE.md summed to 1,892; the R2 regeneration is")
    L.append("   authoritative and sums to the declared 1,895 by construction.)")

    # ---- write CSV
    hdr = ("ROW_VA,MNEMONIC,OP_STR,BYTES,FUNC_START,FUNC_WIDTH,WIDTH,BASE_REG,INDEX_REG,"
           "SCALE,MEM_CATEGORY,CLASSIFICATION,CLASSIFICATION_REASON,CRITERION")
    lines = [hdr]
    for r in rows:
        fn = S.func_containing(functions, r[0])
        lines.append("0x%08X,%s,%s,%s,0x%08X,%d,%d,%s,%s,%d,%s,%s,%s,%s"
                     % (r[0], r[1], r[2].replace(",", ";"), r[3], r[4],
                        (fn["end"] - fn["start"]) if fn else 0, r[5], r[6],
                        r[7], r[8], r[9], r[10], r[11].replace(",", ";").replace(";", ";"), r[12]))
    with open(os.path.join(RAW, "HOLDER14_WRITER_CENSUS.csv"), "w") as f:
        f.write(chr(10).join(lines) + chr(10))

    # ---- write B.5 function map
    mlines = ["FUNC_START,FUNC_END,END_KIND"]
    for fn in functions:
        mlines.append("0x%08X,0x%08X,%s" % (fn["start"], fn["end"], fn["end_kind"]))
    with open(os.path.join(RAW, "B5_FUNCTION_MAP.csv"), "w") as f:
        f.write(chr(10).join(mlines) + chr(10))

    with open(os.path.join(RAW, "HOLDER14_CENSUS_SUMMARY.txt"), "w") as f:
        f.write(chr(10).join(L) + chr(10))
    print(chr(10).join(L[:40]))
    print("...")
    print("WROTE: HOLDER14_WRITER_CENSUS.csv (%d rows), HOLDER14_CENSUS_SUMMARY.txt, B5_FUNCTION_MAP.csv (%d funcs)"
          % (len(rows), len(functions)))


if __name__ == "__main__":
    main()
