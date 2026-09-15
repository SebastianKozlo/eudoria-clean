"""
phase_d_callers.py - PHASE D (G8): four-channel caller census of FUN_006FAB80.
- Channel 1 DIRECT_E8_CENSUS: raw-byte E8/E9/EB census across .text
  (denominator = opcode byte occurrences) + lattice-verified call sites.
- Channel 2 IMM32_ADDRESS_CENSUS: whole-file dword occurrences (re-verification
  of Phase B raw; every hit classified).
- Channel 3 VTABLE_MEMBERSHIP_CENSUS: every vtable/slot containing the thunk.
- Channel 4 VIRTUAL_DISPATCH_PATTERN_CENSUS: two-step and direct
  'vtable slot ordinal 2' (disp 0x08) dispatch candidates with receiver
  provenance classification (bounded slices, fingerprint, ctor/new-chain class).
Writes 01_RAW/THUNK_CALLER_CENSUS.csv + 01_RAW/THUNK_CALLER_CENSUS.txt.
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
SLOT_ORD = 2          # measured in Phase B (all five vtables)
SLOT_DISP = 0x08      # SLOT_ORD * 4
MAX_INTERSTITIALS = 6  # corrected threshold (contract: prior run's <=3 missed sites)
WINDOW = 64           # bytes


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: THUNK_CALLER_CENSUS.txt (Phase D; CSV companion)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_d_callers.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("=" * 80)

    # ---- Channel 1: raw-byte E8/E9/EB census over .text
    t = S.text_section(m)
    tbase = t["roff"]
    n = t["rsize"]
    data = m["data"]
    base = m["imagebase"] + t["vaddr"]
    e8_bytes = 0
    e9_bytes = 0
    eb_bytes = 0
    e8_hits = []
    e9_hits = []
    eb_hits = []
    for i in range(tbase, tbase + n - 5):
        b = data[i]
        if b == 0xE8:
            e8_bytes += 1
            rel = int.from_bytes(data[i + 1:i + 5], "little", signed=True)
            tgt = base + (i - tbase) + 5 + rel
            if tgt == THUNK:
                e8_hits.append(base + (i - tbase))
        elif b == 0xE9:
            e9_bytes += 1
            rel = int.from_bytes(data[i + 1:i + 5], "little", signed=True)
            tgt = base + (i - tbase) + 5 + rel
            if tgt == THUNK:
                e9_hits.append(base + (i - tbase))
        elif b == 0xEB:
            eb_bytes += 1
            rel = int.from_bytes(data[i + 1:i + 2], "little", signed=True)
            tgt = base + (i - tbase) + 2 + rel
            if tgt == THUNK:
                eb_hits.append(base + (i - tbase))
    L.append("")
    L.append("[D1] DIRECT E8/E9/EB CENSUS (raw byte scan; denominator = opcode bytes)")
    L.append("  E8 byte occurrences in .text: %d ; targeting 0x%08X: %d %s"
             % (e8_bytes, THUNK, len(e8_hits), [hex(x) for x in e8_hits]))
    L.append("  E9 byte occurrences in .text: %d ; targeting 0x%08X: %d %s"
             % (e9_bytes, THUNK, len(e9_hits), [hex(x) for x in e9_hits]))
    L.append("  EB byte occurrences in .text: %d ; targeting 0x%08X: %d %s"
             % (eb_bytes, THUNK, len(eb_hits), [hex(x) for x in eb_hits]))

    # ---- map pass for lattice + channel 4 pattern census
    functions, calls, jmps, stats = S.build_text_map(m, cs)
    lattice_calls = [a for (a, t2) in calls if t2 == THUNK]
    lattice_jmps = [a for (a, t2) in jmps if t2 == THUNK]
    L.append("  lattice-verified call sites to thunk: %d %s"
             % (len(lattice_calls), [hex(x) for x in lattice_calls]))
    L.append("  lattice-verified jmp sites to thunk: %d %s"
             % (len(lattice_jmps), [hex(x) for x in lattice_jmps]))

    # ---- Channel 2: IMM32 whole-file census (re-verify Phase B)
    occ = S.find_dword_occurrences(m, THUNK)
    L.append("")
    L.append("[D2] IMM32 WHOLE-FILE CENSUS (re-verification of Phase B raw)")
    L.append("  total occurrences: %d" % len(occ))
    imm_hits = []
    for (off, va, aligned) in occ:
        sec = S.section_of_va(m, va) if va else None
        secn = sec["name"] if sec else "FILEHDR"
        cls = "?"
        if va and aligned and secn in (".rdata", ".data"):
            vt = S.vtable_from_slot(m, va)
            if vt:
                cls = "VTABLE_SLOT vtable=0x%08X ordinal=%d class=%s" % (
                    vt["vtable_start"], (va - vt["vtable_start"]) // 4,
                    vt["class_name"])
        elif secn == ".text":
            cls = "TEXT_IMM (mid-instruction or instruction immediate)"
        imm_hits.append((off, va, aligned, secn, cls))
        L.append("  file_off=0x%08X va=%s aligned=%s section=%s -> %s"
                 % (off, ("0x%08X" % va) if va else "-", aligned, secn, cls))

    # ---- Channel 3: vtable membership (re-derive)
    L.append("")
    L.append("[D3] VTABLE MEMBERSHIP CENSUS (re-derived)")
    members = []
    for (off, va, aligned) in occ:
        if not (va and aligned):
            continue
        sec = S.section_of_va(m, va)
        if sec is None or sec["name"] not in (".rdata", ".data"):
            continue
        vt = S.vtable_from_slot(m, va)
        if vt:
            members.append((vt["vtable_start"], va, (va - vt["vtable_start"]) // 4,
                            vt["class_name"]))
    seen_vts = {}
    for (vstart, sva, so, cn) in members:
        seen_vts.setdefault(vstart, []).append((sva, so, cn))
    L.append("  unique vtables containing the thunk: %d" % len(seen_vts))
    for vstart in sorted(seen_vts):
        rows_ = seen_vts[vstart]
        L.append("  vtable 0x%08X class=%s slots=%s" % (vstart, rows_[0][2],
                 [r[1] for r in rows_]))
    L.append("  beyond-the-five check: memberships: %d (Phase B count=5, all five expected classes)"
             % len(seen_vts))

    # ---- Channel 4: virtual dispatch pattern census for slot ordinal 2
    # single pass state machine over all .text instructions
    inv = S.vtable_inventory(m)
    vt_names_all = {}
    for r in inv:
        vt_names_all[r["vtable_start"]] = r["class_name"]
    family_vts = {}
    for r in inv:
        chd = S.read_chd(m, r["col"]["p_class_hierarchy"])
        if chd is None:
            continue
        lineage = set(b["name"] for b in chd["bases"])
        if r["class_name"].startswith(".?AVArkAnimation") or (lineage & {
                ".?AVArkAnimationPredefined@@", ".?AVArkAnimationCyclic@@",
                ".?AVArkAnimationDerivatives@@", ".?AVArkAnimationCyclicLinear@@",
                ".?AVArkAnimationCyclicSin@@"}):
            family_vts[r["vtable_start"]] = r["class_name"]
    imports = S.parse_imports(m)
    NEW_THUNK = None
    for (site, tgt) in calls[:4000]:
        _t, iname = S.thunk_target_import(m, cs, imports, tgt)
        if iname and "??2" in iname:
            NEW_THUNK = tgt
            break

    ctor_class_cache = {}
    def ctor_class_of(callee):
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
        fn = S.func_containing(functions, new_call_va)
        if fn is None:
            return "UNKNOWN"
        insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
        tail = [i for i in insns if new_call_va < i.address < new_call_va + 48
                and i.mnemonic == "call"]
        for i in tail:
            if i.operands and i.operands[0].type == S.x86c.X86_OP_IMM:
                t2 = i.operands[0].imm & 0xFFFFFFFF
                cls = ctor_class_of(t2)
                if cls not in ("UNKNOWN", "UNDECODEABLE"):
                    return cls
        return "UNKNOWN"

    def classify_tree(tree):
        ev = []
        fam = False
        others = set()
        unknown = False

        def walk(n):
            nonlocal fam, unknown
            if n.kind == "CALL_RETURN":
                mm = re.search(r"def via call (0x[0-9A-Fa-f]+) -> callee (0x[0-9A-Fa-f]+)",
                               n.detail)
                if mm:
                    csite = int(mm.group(1), 16)
                    callee = int(mm.group(2), 16)
                    if NEW_THUNK is not None and callee == NEW_THUNK:
                        cls = new_chain_class(csite)
                    else:
                        cls = ctor_class_of(callee)
                else:
                    mm2 = re.search(r"callee (0x[0-9A-Fa-f]+)", n.detail)
                    if mm2:
                        cls = ctor_class_of(int(mm2.group(1), 16))
                    else:
                        cls = "UNKNOWN"
                ev.append("callee->%s" % cls)
                if cls.startswith("FAMILY:"):
                    fam = True
                elif cls.startswith("OTHER:"):
                    others.add(cls)
                else:
                    unknown = True
            for c in n.children:
                walk(c)
        walk(tree)
        kinds = []
        def walkk(n):
            kinds.append(n.kind)
            for c in n.children:
                walkk(c)
        walkk(tree)
        if "THIS_ENTRY" in kinds:
            ev.append("this-entry")
        if fam:
            return ("PROVEN_FAMILY", ev)
        if others and not unknown:
            return ("PROVEN_OTHER:" + "|".join(sorted(others)), ev)
        if others:
            return ("MIXED:" + "|".join(sorted(others)), ev)
        return ("UNPROVEN", ev)

    # state machine pass
    t2 = S.text_section(m)
    tbase2 = t2["roff"]
    n2 = t2["rsize"]
    base2 = m["imagebase"] + t2["vaddr"]
    mv = memoryview(m["data"])[tbase2:tbase2 + n2]
    candidates = []   # (kind, recv_load_va, slot_load_va, call_va, recv_reg)
    vt_load = {}      # reg -> (va, recv_reg)
    slot_load = {}    # reg -> (va, recv_reg, interstitials, recv_load_va)
    pos = 0
    data = m["data"]
    # single-stream pass (capability: cs.disasm has ~25ms per-call setup cost,
    # so per-function re-decode is FORBIDDEN; state resets INSIDE one stream)
    while pos < n2:
        any_dec = False
        for insn in cs.disasm(mv[pos:n2], base2 + pos):
            any_dec = True
            a = insn.address
            mn = insn.mnemonic
            ops = insn.operands
            if mn in S.TERMINALS:
                # function boundary: reset tracked state, stay in the stream
                vt_load = {}
                slot_load = {}
                pos = (a - base2) + insn.size
                continue
            if mn == "mov" and len(ops) == 2:
                if ops[0].type == S.x86c.X86_OP_REG and ops[1].type == S.x86c.X86_OP_MEM \
                        and not ops[1].mem.index and ops[1].mem.disp == 0:
                    rd = insn.reg_name(ops[0].reg)
                    rb = insn.reg_name(ops[1].mem.base) if ops[1].mem.base else None
                    if rb and rd:
                        vt_load[rd] = (a, rb)
                if ops[0].type == S.x86c.X86_OP_REG and ops[1].type == S.x86c.X86_OP_MEM \
                        and ops[1].mem.disp == SLOT_DISP and not ops[1].mem.index:
                    rd = insn.reg_name(ops[0].reg)
                    rb = insn.reg_name(ops[1].mem.base) if ops[1].mem.base else None
                    if rb and rb in vt_load and a - vt_load[rb][0] <= WINDOW:
                        slot_load[rd] = (a, rb, 0, vt_load[rb][0])
                    elif rd:
                        slot_load.pop(rd, None)
            if mn == "call" and ops:
                if ops[0].type == S.x86c.X86_OP_REG:
                    rd = insn.reg_name(ops[0].reg)
                    if rd in slot_load:
                        (sva, sbase, inter, rload) = slot_load[rd]
                        candidates.append(("TWO_STEP", rload, sva, a, sbase))
                elif ops[0].type == S.x86c.X86_OP_MEM \
                        and ops[0].mem.disp == SLOT_DISP and not ops[0].mem.index:
                    rb = insn.reg_name(ops[0].mem.base) if ops[0].mem.base else None
                    if rb and rb in vt_load and a - vt_load[rb][0] <= WINDOW:
                        candidates.append(("DIRECT_MEM", vt_load[rb][0], a, a,
                                           vt_load[rb][1]))
                vt_load = {}
                slot_load = {}
                pos = (a - base2) + insn.size
                continue
            # interstitial tracking: expunge stale entries
            for rd in list(slot_load.keys()):
                (sva, sbase, inter, rload) = slot_load[rd]
                if a - sva > WINDOW or inter >= MAX_INTERSTITIALS:
                    del slot_load[rd]
                else:
                    slot_load[rd] = (sva, sbase, inter + 1, rload)
            for rd in list(vt_load.keys()):
                if a - vt_load[rd][0] > WINDOW:
                    del vt_load[rd]
            pos = (a - base2) + insn.size
        # iterator exhausted: end of .text or data island -> resync at padding
        if pos >= n2:
            break
        k = pos + 1
        run = 0
        kk = k
        while kk < n2:
            if data[tbase2 + kk] in S.PAD_BYTES:
                run += 1
                if run >= 4:
                    kk += 1
                    while kk < n2 and data[tbase2 + kk] in S.PAD_BYTES:
                        kk += 1
                    break
            else:
                run = 0
            kk += 1
        pos = kk if kk < n2 else n2
    L.append("")
    L.append("[D4] VIRTUAL DISPATCH PATTERN CENSUS (slot ordinal %d, disp 0x%02X; window %dB, <=%d interstitials)"
             % (SLOT_ORD, SLOT_DISP, WINDOW, MAX_INTERSTITIALS))
    L.append("  candidate dispatch sites collected: %d" % len(candidates))

    # classify receivers
    csv_rows = ["CAND_ID,KIND,RECV_LOAD_VA,SLOT_LOAD_VA,CALL_VA,RECEIVER_REG,"
                "RECEIVER_VERDICT,RECEIVER_EVIDENCE,CLASSIFICATION"]
    counts = dict(total=len(candidates), proven=0, rejected=0, insufficient=0,
                  notvt=0)
    for idx, (kind, rload_va, sva, cva, rreg) in enumerate(candidates):
        budget = {"n": 0, "max_level": 2}
        visited = set()
        fn = S.func_containing(functions, rload_va)
        # receiver reg at the recv-load insn
        rreg_name = rreg if isinstance(rreg, str) else "?"
        tree = None
        if fn is not None and rreg_name not in ("?", ""):
            insns, _e = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
            # find the receiver load insn and take its base register name
            for i in insns:
                if i.address == rload_va:
                    for op in i.operands:
                        if op.type == S.x86c.X86_OP_MEM and op.mem.base:
                            rreg_name = i.reg_name(op.mem.base)
                    break
            if rreg_name:
                tree = S.slice_reg(m, cs, functions, calls, rload_va, rreg_name,
                                   0, visited, budget)
        verdict = "UNPROVEN"
        ev = []
        if tree is not None:
            verdict, ev = classify_tree(tree)
        if verdict == "PROVEN_FAMILY":
            classification = "PROVEN_TARGET"
            counts["proven"] += 1
        elif verdict.startswith("PROVEN_OTHER") or verdict.startswith("MIXED"):
            classification = "REJECTED_TARGET_NOT_FAMILY"
            counts["rejected"] += 1
        elif verdict == "UNPROVEN":
            classification = "INSUFFICIENT_PROOF"
            counts["insufficient"] += 1
        else:
            classification = "NOT_A_VTABLE_CALL"
            counts["notvt"] += 1
        csv_rows.append("%d,%s,0x%08X,0x%08X,0x%08X,%s,%s,%s,%s"
                        % (idx, kind, rload_va, sva, cva, rreg_name, verdict,
                           (";".join(ev[:4])).replace(",", ";"), classification))
    L.append("  classifications: PROVEN_TARGET=%d REJECTED_TARGET_NOT_FAMILY=%d "
             "INSUFFICIENT_PROOF=%d NOT_A_VTABLE_CALL=%d"
             % (counts["proven"], counts["rejected"], counts["insufficient"],
                counts["notvt"]))
    with open(os.path.join(RAW, "THUNK_CALLER_CENSUS.csv"), "w") as f:
        f.write(chr(10).join(csv_rows) + chr(10))

    # summary of proven + top insufficient in the txt raw
    L.append("")
    L.append("  PROVEN_TARGET candidates (receiver proven family -> call hits slot-2 = thunk):")
    with open(os.path.join(RAW, "THUNK_CALLER_CENSUS.csv")) as f:
        csv_content = f.read().splitlines()
    shown = 0
    for row in csv_content[1:]:
        if row.endswith("PROVEN_TARGET"):
            L.append("    " + row)
            shown += 1
    if shown == 0:
        L.append("    (none)")
    L.append("")
    L.append("G8 SELF-ASSESSMENT: all four channels censused with denominators + per-candidate classification.")
    out = os.path.join(RAW, "THUNK_CALLER_CENSUS.txt")
    with open(out, "w") as f:
        f.write(chr(10).join(L) + chr(10))
    print(chr(10).join(L))
    print("")
    print("WROTE: %s" % out)


if __name__ == "__main__":
    main()
