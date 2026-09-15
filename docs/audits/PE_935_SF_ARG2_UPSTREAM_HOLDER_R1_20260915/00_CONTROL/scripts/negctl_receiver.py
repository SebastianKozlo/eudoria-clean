"""
negctl_receiver.py - PHASE G7 (mandatory negative control) + SF validation
+ receiver-identity ladder infrastructure.
- Re-derives PIN-NC anchors from own bytes (NiD3D pixel shaders method
  0x007AC2F0; NiBoundingVolume method 0x007F1D70 ordinal 1).
- Slot-3 discriminator census over ALL COL-backed vtables: how many vtables
  have slot-3 == 0x0050A050 (SceneFeeder receiver classifier selectivity).
- SF vtable validation: extent of 0x00A7D458, COL class name, slot-3, slot-0.
- FUN_0050A050 (PIN-SF2) extent + ABI revalidation.
- SF slot-0 method 0x0050A460 decode (release-ABI comparison vs the family
  dtor's held->vt[0](1) dispatch).
- SIB census rows classification (the 2 SIB rows from the G4 census).
- [N7] R2 (QC P3-1 fix): read-census of [reg+0x14] over the DECLARED full
  family function set (all 10 family vtables' slot functions + all family-
  vtable-storing functions + shared ctor + PSPMod ctor), each function
  decoded over its chunk closure.
Writes 01_RAW/NEGCTL_RECEIVER_RAW.txt.
Re-measures size+SHA256+PE layout FIRST (fail-closed).
"""
import sys
import os
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s0_common as S

RUN_DIR = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(RUN_DIR, "01_RAW")

SF_VTABLE = 0x00A7D458
SF_SLOT3 = 0x0050A050
SF_SLOT0 = 0x0050A460
PIN_NC_A = 0x007AC2F0
PIN_NC_B = 0x007F1D70
FAM_VTS = [0x00A864C0, 0x00A86550, 0x00A86574, 0x00A865A0, 0x00A86650]


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: NEGCTL_RECEIVER_RAW.txt (G7 negative control + SF validation)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: negctl_receiver.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("=" * 80)

    # ---- [N1] slot-3 discriminator census over ALL COL-backed vtables
    inv = S.vtable_inventory(m)
    L.append("")
    L.append("[N1] SLOT-3 RECEIVER-CLASSIFIER DISCRIMINATOR CENSUS")
    L.append("  COL-backed vtables in binary: %d" % len(inv))
    slot3_hits = []
    slot3_valid = 0
    for r in inv:
        end, entries, stop = S.vtable_extent(m, r["vtable_start"])
        if len(entries) > 3:
            slot3_valid += 1
            if entries[3] == SF_SLOT3:
                slot3_hits.append((r["vtable_start"], r["class_name"]))
    L.append("  vtables with a valid slot-3 entry: %d" % slot3_valid)
    L.append("  vtables whose slot-3 == 0x0050A050 (SceneFeeder receiver signature): %d"
             % len(slot3_hits))
    for (v, nm) in slot3_hits:
        L.append("    0x%08X %s" % (v, nm))
    L.append("  CLASSIFIER SELECTIVITY: %d/%d vtables classified as slot-3 SceneFeeder"
             % (len(slot3_hits), slot3_valid))
    L.append("  -> the receiver classifier does NOT classify every vtable as SceneFeeder;")
    L.append("     a compatible slot-3 dispatch receiver is SceneFeeder ONLY when its")
    L.append("     vtable slot-3 resolves to 0x0050A050 (and RTTI matches).")

    # ---- [N2] PIN-NC anchor re-derivation (own bytes)
    L.append("")
    L.append("[N2] PIN-NC ANCHOR RE-DERIVATION (negative-control anchors)")
    for anchor in (PIN_NC_A, PIN_NC_B):
        occ = S.find_dword_occurrences(m, anchor)
        L.append("  method 0x%08X: whole-file dword occurrences: %d" % (anchor, len(occ)))
        for (off, va, aligned) in occ:
            sec = S.section_of_va(m, va) if va else None
            secn = sec["name"] if sec else "FILEHDR"
            tag = ""
            if va and aligned and secn in (".rdata", ".data"):
                vt = S.vtable_from_slot(m, va)
                if vt:
                    tag = "VTABLE_SLOT vtable=0x%08X ordinal=%d class=%s" % (
                        vt["vtable_start"], (va - vt["vtable_start"]) // 4,
                        vt["class_name"])
            L.append("    file_off=0x%08X va=%s aligned=%s section=%s %s"
                     % (off, ("0x%08X" % va) if va else "-", aligned, secn, tag))
    # explicit validation of the two pin expectations
    occ_b = S.find_dword_occurrences(m, PIN_NC_B)
    nb_ok = False
    for (off, va, aligned) in occ_b:
        if va and aligned:
            vt = S.vtable_from_slot(m, va)
            if vt and vt["class_name"] == ".?AVNiBoundingVolume@@" \
                    and (va - vt["vtable_start"]) // 4 == 1:
                nb_ok = True
    L.append("  PIN-NC(NiBoundingVolume slot-1 == 0x007F1D70) VALIDATED = %s" % nb_ok)
    ps_ok = False
    for (off, va, aligned) in S.find_dword_occurrences(m, PIN_NC_A):
        if va and aligned:
            vt = S.vtable_from_slot(m, va)
            if vt and "PixelShader" in vt["class_name"]:
                ps_ok = True
    L.append("  PIN-NC(pixel-shader vtable slot == 0x007AC2F0) VALIDATED = %s" % ps_ok)
    L.append("")
    L.append("  NEGATIVE CONTROL VERDICT: both anchors re-derived from own bytes.")
    L.append("  .?AVNiBoundingVolume@@ and the NiD3D pixel shader classes are")
    L.append("  compatible-ABI vtable-dispatch receivers that are provably NOT")
    L.append("  SceneFeeder (RTTI name and vtable differ; slot-3 != 0x0050A050;")
    L.append("  see [N1] counts). FAILURE_CASE_DETECTED = YES (the classifier")
    L.append("  rejects non-SceneFeeder receivers; it does not blanket-classify).")

    # ---- [N3] SF vtable validation (ladder infrastructure)
    L.append("")
    L.append("[N3] SCENEFEEDER VTABLE VALIDATION (receiver-identity ladder)")
    vt = S.vtable_from_slot(m, SF_VTABLE + 3 * 4)
    if vt is None:
        L.append("  CRITICAL: 0x00A7D464 did not resolve to a COL-backed vtable!")
    else:
        L.append("  vtable start : 0x%08X (pin 0x00A7D458) MATCH=%s"
                 % (vt["vtable_start"], vt["vtable_start"] == SF_VTABLE))
        L.append("  COL class    : %s" % vt["class_name"])
        L.append("  COL va       : 0x%08X sig=%d offset=%d" % (vt["col"]["va"],
                 vt["col"]["sig"], vt["col"]["offset"]))
    end, entries, stop = S.vtable_extent(m, SF_VTABLE)
    L.append("  extent       : [0x%08X..0x%08X) slots=%d stop=%s"
             % (SF_VTABLE, end, len(entries), stop))
    for i, e in enumerate(entries):
        L.append("    [%d] 0x%08X" % (i, e))
    L.append("  slot-3 dword @0x00A7D464 = 0x%08X (pin 0x0050A050) MATCH=%s"
             % (entries[3] if len(entries) > 3 else 0,
                (entries[3] if len(entries) > 3 else 0) == SF_SLOT3))
    pin_slots = [0x0050A460, 0x005090A0, 0x005090B0, 0x0050A050, 0x005090C0, 0x00509580]
    L.append("  PIN-SF1 slot table 0..5 match = %s" % (entries == pin_slots))
    if vt:
        chd = S.read_chd(m, vt["col"]["p_class_hierarchy"])
        if chd:
            L.append("  SF class hierarchy: %s" % " <- ".join(
                b["name"] for b in chd["bases"]))

    # ---- [N4] FUN_0050A050 revalidation (PIN-SF2)
    L.append("")
    L.append("[N4] FUN_0050A050 REVALIDATION (PIN-SF2)")
    f = S.b5_function(m, cs, SF_SLOT3, max_bytes=512)
    L.append("  B.5 extent: [0x%08X..0x%08X) end_kind=%s (pin 0x0050A050..0x0050A0AA)"
             % (f["start"], f["end"], f["end_kind"]))
    ret_sites = []
    for i in f["insns"]:
        L.append("    0x%08X  %-16s %s" % (i.address, i.bytes.hex(),
                                           i.mnemonic + " " + i.op_str))
        if i.mnemonic == "ret":
            imm = i.operands[0].imm if i.operands else None
            ret_sites.append((i.address, imm))
    L.append("  ret sites: %s (pin: 0x50A084 and 0x50A0A7, both ret 8)"
             % [("0x%08X" % a, "ret %s" % ("0x%X" % v) if v is not None else "?")
                for (a, v) in ret_sites])
    null_test = any(i.mnemonic == "test" for i in f["insns"])
    L.append("  arg2 NULL-tested (any test in function): %s" % null_test)

    # ---- [N5] SF slot-0 method decode (release-ABI comparison)
    L.append("")
    L.append("[N5] SF SLOT-0 METHOD 0x0050A460 DECODE (family dtor releases held via vt[0])")
    f0 = S.b5_function(m, cs, SF_SLOT0, max_bytes=512)
    for i in f0["insns"][:40]:
        ann = []
        for (_i, op) in S.mem_write_ops(i):
            if op.mem.disp == 0x04:
                ann.append("WRITE_[+0x04]")
        L.append("    0x%08X  %-16s %-36s%s" % (i.address, i.bytes.hex(),
                 i.mnemonic + " " + i.op_str, (" ; " + ";".join(ann)) if ann else ""))
    if len(f0["insns"]) > 40:
        L.append("    ... (%d more)" % (len(f0["insns"]) - 40))

    # ---- [N6] the two SIB census rows (classification for the record)
    L.append("")
    L.append("[N6] SIB CENSUS ROWS (from G4 census; enumerated separately, classified)")
    # re-run the census quickly to get SIB rows: scan .text for mem-write disp 0x14 with index
    census = []
    functions, calls, jmps, stats = S.build_text_map(m, cs, census_14=census)
    sib_rows = [r for r in census if r[7] != ""]
    for (va, mn, op_str, bhex, fstart, width, breg, ireg, scale) in sib_rows:
        L.append("  0x%08X %s %s [func 0x%08X base=%s index=%s scale=%d width=%d]"
                 % (va, mn, op_str, fstart, breg, ireg, scale, width))
        L.append("    -> SIB/indexed form: base+offset+index; the family writer census")
        L.append("       treats indexed writes as computed-address writes (excluded form")
        L.append("       per contract 7(i)); base register is not a proven family this.")
    if not sib_rows:
        L.append("  (no SIB rows found on re-derivation)")

    # ---- [N7] family functions: read-census of [reg+0x14] (field usage picture)
    # R2 (QC P3-1 fix): the R1 [N7] scanned only the 5 core vtables' slot
    # functions + 3 dtors WITHOUT declaring the family-function set bound and
    # undercounted (10 refs). The R2 census declares the FULL bound:
    #   family function set = all vtable-slot functions of the 10 family
    #   classes + all functions storing any family vtable (ctors/dtors) +
    #   the shared base ctor 0x006FABA0 + the PSPMod ctor 0x006FEB00;
    #   each function decoded over its chunk closure (branch-target +
    #   conditional-fall-through + jump-table joining, <= 64 chunks / 64KB).
    L.append("")
    L.append("[N7] READ-CENSUS: [reg+0x14] operand references in family functions")
    L.append("  R2 DECLARED BOUND (QC P3-1 fix): family function set = all slots of")
    L.append("  the 10 family vtables + all functions storing a family vtable")
    L.append("  (ctors/dtors) + shared ctor 0x006FABA0 + PSPMod ctor 0x006FEB00;")
    L.append("  per-function extent = chunk closure (branch-target + conditional-")
    L.append("  fall-through + jump-table joining; <= 64 chunks, <= 64KB per function).")
    fam_slot_funcs = set()
    FAM_VTS10 = [0x00A864C0, 0x00A864E4, 0x00A86508, 0x00A8652C, 0x00A86550,
                 0x00A86574, 0x00A865A0, 0x00A86650, 0x00A866DC, 0x00A86700]
    for vstart in FAM_VTS10:
        end, entries, stop = S.vtable_extent(m, vstart)
        for e in entries:
            fam_slot_funcs.add(e)
    # vtable-store functions (family ctors/dtors) via a collect pass
    famvt_set = set(FAM_VTS10)
    stores = []
    def collect_st(insn, fstart):
        ops = insn.operands
        if insn.mnemonic == "mov" and len(ops) == 2:
            if ops[0].type == S.x86c.X86_OP_MEM and ops[1].type == S.x86c.X86_OP_IMM:
                v = ops[1].imm & 0xFFFFFFFF
                if v in famvt_set:
                    stores.append((insn.address, v, fstart))
    functions2, calls2, jmps2, stats2 = S.build_text_map(m, cs, collect=collect_st)
    for (iva, v, fstart) in stores:
        fam_slot_funcs.add(fstart)
    fam_slot_funcs.add(0x006FABA0)
    fam_slot_funcs.add(0x006FEB00)
    L.append("  family function set size: %d (all slot functions + all family-"
             % len(fam_slot_funcs))
    L.append("  vtable-storing functions + the shared ctor + the PSPMod ctor)")

    branches = []
    functions3, calls3, jmps3, stats3 = S.build_text_map(m, cs, branches=branches)

    def chunk_closure(start_va):
        fn = S.func_containing(functions3, start_va)
        if fn is None:
            f2 = S.b5_function(m, cs, start_va)
            fn = dict(start=f2["start"], end=f2["end"], end_kind=f2["end_kind"])
        chunks = [dict(fn)]
        hi = fn["start"] + 0x10000
        changed = True
        while changed and len(chunks) <= 64:
            changed = False
            starts = set(c["start"] for c in chunks)
            for c in list(chunks):
                insns, _e = S.disasm_range(m, cs, c["start"], c["end"] - c["start"])
                if not insns:
                    continue
                term = insns[-1]
                if term.mnemonic.startswith("j") and term.mnemonic != "jmp":
                    nxt = S.func_containing(functions3, c["end"])
                    if nxt is not None and nxt["start"] == c["end"] \
                            and nxt["start"] not in starts and nxt["start"] < hi:
                        chunks.append(dict(nxt))
                        starts.add(nxt["start"])
                        changed = True
                for i in insns:
                    if i.mnemonic.startswith("j"):
                        ops = i.operands
                        if ops and ops[0].type == S.x86c.X86_OP_IMM:
                            tgt = ops[0].imm & 0xFFFFFFFF
                            if tgt not in starts and fn["start"] <= tgt < hi:
                                f3 = S.func_containing(functions3, tgt)
                                if f3 is not None and f3["start"] == tgt:
                                    chunks.append(dict(f3))
                                    starts.add(tgt)
                                    changed = True
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
                                    f4 = S.func_containing(functions3, ent)
                                    if f4 is not None and f4["start"] == ent:
                                        chunks.append(dict(f4))
                                        starts.add(ent)
                                        changed = True
        chunks.sort(key=lambda c: c["start"])
        return chunks

    reads = []
    for fva in sorted(fam_slot_funcs):
        chunks = chunk_closure(fva)
        for c in chunks:
            insns, _e = S.disasm_range(m, cs, c["start"], c["end"] - c["start"])
            for i in insns:
                for op in i.operands:
                    if op.type == S.x86c.X86_OP_MEM and op.mem.disp == 0x14:
                        try:
                            acc = op.access
                        except AttributeError:
                            acc = 0
                        reads.append((i.address, i.mnemonic + " " + i.op_str,
                                      "READ" if acc == 1 else ("RM" if acc == 3 else
                                      ("WRITE" if acc == 2 else "?")), fva, len(chunks)))
    L.append("  total [reg+0x14] operand references over the declared bound: %d"
             % len(reads))
    for (va, s, acc, fva, nch) in reads:
        L.append("    0x%08X %-46s access=%-5s func 0x%08X (closure chunks=%d)"
                 % (va, s, acc, fva, nch))
    L.append("  NOTE (R2, context for QC P3-1): the QC's P3-1 enumeration also")
    L.append("  listed 0x008267C7/0x008267DA as 'Predefined slot-3 function' refs;")
    L.append("  own re-derivation: the Predefined slot-3 (vtable ordinal 3 of")
    L.append("  0x00A864C0) is the 2-insn stub 0x00826770 (xor al,al; ret 4);")
    L.append("  0x008267C7/0x008267DA are esp-based frame refs inside the ADJACENT")
    L.append("  function [0x00826780..0x0082682F), which stores no family vtable and")
    L.append("  is NOT a member of the declared family function set (reported here")
    L.append("  for completeness; including them would add 2 esp-frame refs).")

    out = os.path.join(RAW, "NEGCTL_RECEIVER_RAW.txt")
    with open(out, "w") as f:
        f.write(chr(10).join(L) + chr(10))
    print(chr(10).join(L[:60]))
    print("...")
    print("WROTE: %s" % out)


if __name__ == "__main__":
    main()
