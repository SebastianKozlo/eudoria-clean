"""
phase_b_rtti.py - PHASE B (G3): five class memberships re-derived from own bytes.
IMM32 thunk census -> vtable memberships -> RTTI/COL walks -> class map ->
vtable-store census (primary vs secondary) -> ctor/dtor identification ->
new-size evidence -> shared base hierarchy -> PIN-FIVE validation.
Writes 01_RAW/RTTI_COL_RAW.txt, 01_RAW/ARKANIMATION_VTABLE_MAP.csv,
01_RAW/VTABLE_INVENTORY.csv (feeds G7 negative control), 01_RAW/IMM32_THUNK_CENSUS.txt
(Phase D channel-2 raw).
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

THUNK = 0x006FAB80
SHARED_CTOR = 0x006FABA0
PIN_FIVE = [".?AVArkAnimationCyclic@@",
            ".?AVArkAnimationCyclicLinear@@",
            ".?AVArkAnimationCyclicSin@@",
            ".?AVArkAnimationDerivatives@@",
            ".?AVArkAnimationPredefined@@"]


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: RTTI_COL_RAW.txt (Phase B)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_b_rtti.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("SOURCE_OF_TRUTH: %s physical bytes (STATIC; NEVER executed)" % S.EXE_PATH)
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("=" * 80)
    L.append("")

    # ---- [B1] IMM32 whole-file census of the thunk VA
    occ = S.find_dword_occurrences(m, THUNK)
    L.append("[B1] IMM32 WHOLE-FILE CENSUS OF 0x%08X (raw for Phase D channel 2)" % THUNK)
    L.append("  total occurrences: %d" % len(occ))
    imm_rows = []
    for (off, va, aligned) in occ:
        sec = S.section_of_va(m, va) if va else None
        secn = sec["name"] if sec else "FILEHDR"
        imm_rows.append((off, va, aligned, secn))
        L.append("  file_off=0x%08X va=%s aligned4=%s section=%s"
                 % (off, ("0x%08X" % va) if va else "-", aligned, secn))
    L.append("")

    # vtable slot hits = aligned occurrences in pointer sections
    slot_hits = [(va) for (off, va, aligned, secn) in imm_rows
                 if va and aligned and secn in (".rdata", ".data")]
    L.append("  aligned data-section hits (candidate vtable slots): %d" % len(slot_hits))

    # ---- [B2] resolve each slot hit to its vtable + class
    L.append("")
    L.append("[B2] VTABLE MEMBERSHIP RESOLUTION (backward walk to COL; forward extent)")
    vtables = {}
    slot_map = {}
    unresolved = []
    for slot_va in slot_hits:
        vt = S.vtable_from_slot(m, slot_va)
        if vt is None:
            unresolved.append(slot_va)
            L.append("  slot 0x%08X: UNRESOLVED (no COL-backed vtable walk)" % slot_va)
            continue
        vstart = vt["vtable_start"]
        slot_map[slot_va] = (vstart, (slot_va - vstart) // 4, vt["class_name"])
        if vstart not in vtables:
            end, entries, stop = S.vtable_extent(m, vstart)
            chd = S.read_chd(m, vt["col"]["p_class_hierarchy"])
            vtables[vstart] = dict(info=vt, end=end, entries=entries,
                                   stop=stop, chd=chd)
    L.append("  unique COL-backed vtables containing the thunk: %d" % len(vtables))
    for vstart in sorted(vtables):
        v = vtables[vstart]
        L.append("  vtable 0x%08X class=%s extent=[0x%08X..0x%08X) slots=%d stop=%s"
                 % (vstart, v["info"]["class_name"], vstart, v["end"],
                    len(v["entries"]), v["stop"]))
        for (sv, (vv, so, cn)) in sorted(slot_map.items()):
            if vv == vstart:
                L.append("    thunk slot: 0x%08X ordinal=%d (class %s)" % (sv, so, cn))
        L.append("    COL: va=0x%08X sig=%d offset=%d cd=%d pTD=0x%08X pCHD=0x%08X"
                 % (v["info"]["col"]["va"], v["info"]["col"]["sig"],
                    v["info"]["col"]["offset"], v["info"]["col"]["cd_offset"],
                    v["info"]["col"]["p_type_descriptor"],
                    v["info"]["col"]["p_class_hierarchy"]))
        if v["chd"]:
            L.append("    CHD: va=0x%08X sig=%d attrs=%d num_bases=%d"
                     % (v["chd"]["va"], v["chd"]["sig"], v["chd"]["attributes"],
                        v["chd"]["num_bases"]))
            for b in v["chd"]["bases"]:
                L.append("      BCD: name=%-40s mdisp=0x%08X pdisp=0x%08X vdisp=0x%08X ncb=%d attrs=%d"
                         % (b["name"], b["mdisp"], b["pdisp"], b["vdisp"],
                            b["num_contained"], b["attributes"]))
        else:
            L.append("    CHD: UNREADABLE")
        L.append("    entries:")
        for i, e in enumerate(v["entries"]):
            mark = "  <-- FUN_006FAB80" if e == THUNK else ""
            L.append("      [%2d] 0x%08X%s" % (i, e, mark))
    if unresolved:
        L.append("  UNRESOLVED slot dwords: %s" % [hex(x) for x in unresolved])
    L.append("")

    # ---- [B4] PIN-FIVE validation
    L.append("[B4] PIN-FIVE VALIDATION (expected five classes; corrected count if needed)")
    found_names = set()
    for vstart, v in vtables.items():
        nm = v["info"]["class_name"]
        found_names.add(nm)
    for nm in PIN_FIVE:
        L.append("  expected %-40s PRESENT=%s" % (nm, nm in found_names))
    extra = sorted(found_names - set(PIN_FIVE))
    missing = sorted(nm for nm in PIN_FIVE if nm not in found_names)
    L.append("  extra classes with thunk membership: %s" % (extra if extra else "NONE"))
    L.append("  missing expected classes: %s" % (missing if missing else "NONE"))
    L.append("")

    # ---- [B5] build B.5 map with vtable-store collector
    vt_starts = set(vtables.keys())
    stores = []
    census_14 = []

    def collect(insn, fstart):
        ops = insn.operands
        if insn.mnemonic == "mov" and len(ops) == 2:
            if ops[0].type == S.x86c.X86_OP_MEM and ops[1].type == S.x86c.X86_OP_IMM:
                v = ops[1].imm & 0xFFFFFFFF
                if v in vt_starts:
                    stores.append((insn.address, v, insn.op_str, fstart))
        for (_i, op) in S.mem_write_ops(insn):
            if op.mem.disp == 0x14:
                census_14.append((insn.address, insn.mnemonic, insn.op_str, fstart))

    functions, calls, jmps, stats = S.build_text_map(m, cs, collect)
    L.append("[B5] B.5 MAP PASS (Phase B's independent derivation; Phase C re-derives)")
    L.append("  functions=%d calls=%d jmps=%d insns=%d" %
             (len(functions), len(calls), len(jmps), stats["insns"]))
    L.append("  end_kinds: pad=%d tight=%d oversized=%d desync=%d edge=%d" %
             (stats["pad_ends"], stats["tight_ends"], stats["oversized"],
              stats["resyncs"], stats["edge_ends"]))
    L.append("  vtable-store rows collected: %d" % len(stores))
    L.append("")

    # ---- [B6] vtable-store attribution per vtable
    L.append("[B6] VTABLE-STORE CENSUS (who writes each family vtable VA into memory)")
    for vstart in sorted(vtables):
        rows = [r for r in stores if r[1] == vstart]
        L.append("  vtable 0x%08X class=%s store-sites=%d"
                 % (vstart, vtables[vstart]["info"]["class_name"], len(rows)))
        for (iva, v, ostr, fstart) in rows:
            fn = S.func_containing(functions, iva)
            fkind = fn["end_kind"] if fn else "?"
            L.append("    store 0x%08X: %s [func 0x%08X..0x%08X %s]"
                     % (iva, ostr, fstart, fn["end"] if fn else 0, fkind))
    L.append("")

    # ---- [B7] E8 census to shared ctor 0x6FABA0 + containing functions
    L.append("[B7] E8 CENSUS TO SHARED CTOR 0x%08X (PIN-CTOR six sites re-derivation)" % SHARED_CTOR)
    ctor_sites = [(site, tgt) for (site, tgt) in calls if tgt == SHARED_CTOR]
    L.append("  direct E8 call sites: %d" % len(ctor_sites))
    site_funcs = {}
    for (site, _t) in ctor_sites:
        fn = S.func_containing(functions, site)
        fstart = fn["start"] if fn else None
        site_funcs.setdefault(fstart, []).append(site)
        L.append("    site 0x%08X  in function 0x%08X..0x%08X %s"
                 % (site, fstart, fn["end"] if fn else 0,
                    fn["end_kind"] if fn else "?"))
    L.append("")

    # ---- [B8] ctor candidates per vtable: storing function that E8-calls the shared ctor
    L.append("[B8] CLASS CONSTRUCTOR IDENTIFICATION (vtable-store + shared-ctor-call evidence)")
    class_ctor = {}
    for vstart in sorted(vtables):
        nm = vtables[vstart]["info"]["class_name"]
        rows = [r for r in stores if r[1] == vstart]
        cands = []
        for (iva, v, ostr, fstart) in rows:
            if fstart in site_funcs:
                cands.append((fstart, iva))
        class_ctor[vstart] = cands
        L.append("  class %-40s vtable 0x%08X ctor-candidates: %s"
                 % (nm, vstart,
                    [("func 0x%08X (store@0x%08X)" % (f, i)) for (f, i) in cands]
                    if cands else "NONE"))
    L.append("")

    # ---- [B9] new-size evidence at ctor call sites (object size where inferable)
    L.append("[B9] OBJECT-SIZE EVIDENCE (operator-new sizes before ctor calls)")
    imports = S.parse_imports(m)
    L.append("  imports parsed: %d IAT slots" % len(imports))
    new_thunks = {}
    for fstart in sorted(set(f for f in site_funcs if f is not None)):
        callers = [(site, tgt) for (site, tgt) in calls if tgt == fstart]
        L.append("  ctor func 0x%08X: direct E8 callers: %d" % (fstart, len(callers)))
        for (site, _t) in callers:
            # backward window 48 bytes: look for push imm; call X; add esp,4 / mov ecx
            fn = S.func_containing(functions, site)
            if fn is None:
                continue
            insns, _err = S.disasm_range(m, cs, fn["start"], fn["end"] - fn["start"])
            prior = [i for i in insns if site - 48 <= i.address < site]
            prior.reverse()
            for i in prior:
                if i.mnemonic == "push" and i.operands and \
                        i.operands[0].type == S.x86c.X86_OP_IMM:
                    nxt = [x for x in insns if x.address > i.address and x.address < site]
                    if nxt and nxt[0].mnemonic == "call" and nxt[0].operands \
                            and nxt[0].operands[0].type == S.x86c.X86_OP_IMM:
                        callee = nxt[0].operands[0].imm & 0xFFFFFFFF
                        tstr, iname = S.thunk_target_import(m, cs, imports, callee)
                        new_thunks.setdefault(callee, iname)
                        L.append("    caller-site 0x%08X: push 0x%X; call 0x%08X (%s) -> %s"
                                 % (site, i.operands[0].imm & 0xFFFFFFFF, callee,
                                    tstr, iname if iname else "?"))
                    break
    L.append("  new-thunk map: %s" % [(hex(k), new_thunks[k]) for k in new_thunks])
    L.append("")

    # ---- [B10] shared base class (common BCD lineage)
    L.append("[B10] SHARED BASE HIERARCHY (COL base-class descriptor walks)")
    common = None
    for vstart in sorted(vtables):
        v = vtables[vstart]
        if not v["chd"]:
            continue
        names = [b["name"] for b in v["chd"]["bases"]]
        L.append("  class %-40s lineage: %s" % (v["info"]["class_name"], " <- ".join(names[1:])))
        s = set(names[1:])
        common = s if common is None else (common & s)
    L.append("  common bases across all thunk-member classes: %s" % (sorted(common) if common else "NONE"))
    L.append("")

    # ---- [B11] vtable inventory (all COL-backed vtables; feeds G7)
    inv = S.vtable_inventory(m)
    L.append("[B11] VTABLE INVENTORY: %d COL-backed vtables found" % len(inv))
    L.append("  (full inventory written to 01_RAW/VTABLE_INVENTORY.csv)")
    L.append("")

    # write VTABLE_INVENTORY.csv
    inv_rows = ["class_name,col_va,col_offset,vtable_start,vtable_end,slot_count,slot3_value,stop_reason"]
    for r in inv:
        end, entries, stop = S.vtable_extent(m, r["vtable_start"])
        slot3 = entries[3] if len(entries) > 3 else 0
        inv_rows.append("%s,0x%08X,%d,0x%08X,0x%08X,%d,0x%08X,%s"
                        % (r["class_name"], r["col_va"], r["col"]["offset"],
                           r["vtable_start"], end, len(entries), slot3, stop))
    with open(os.path.join(RAW, "VTABLE_INVENTORY.csv"), "w") as f:
        f.write(chr(10).join(inv_rows) + chr(10))

    # write IMM32_THUNK_CENSUS.txt (raw for Phase D channel 2)
    imm_lines = []
    imm_lines.append("=" * 80)
    imm_lines.append("RAW ARTIFACT: IMM32_THUNK_CENSUS.txt (Phase D channel-2 raw, measured in Phase B pass)")
    imm_lines.append("RUN_ID: %s" % S.RUN_ID)
    imm_lines.append("GENERATOR: phase_b_rtti.py (SHA256=%s)" % gen_sha)
    imm_lines.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    imm_lines.append(s0)
    imm_lines.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    imm_lines.append("=" * 80)
    imm_lines.append("value=0x%08X total_occurrences=%d" % (THUNK, len(imm_rows)))
    for (off, va, aligned, secn) in imm_rows:
        cls = ""
        if va and va in slot_map:
            (vv, so, cn) = slot_map[va]
            cls = "VTABLE_SLOT vtable=0x%08X ordinal=%d class=%s" % (vv, so, cn)
        elif secn == ".text":
            cls = "TEXT_IMM (instruction immediate or mid-instruction bytes; Phase D verifies)"
        imm_lines.append("file_off=0x%08X va=%s aligned4=%s section=%s %s"
                         % (off, ("0x%08X" % va) if va else "-", aligned, secn, cls))
    with open(os.path.join(RAW, "IMM32_THUNK_CENSUS.txt"), "w") as f:
        f.write(chr(10).join(imm_lines) + chr(10))

    # write ARKANIMATION_VTABLE_MAP.csv
    csv_rows = ["class_name,col_va,col_offset,vtable_start,vtable_end,slot_count,thunk_slot_ordinal,thunk_slot_va,store_count,store_funcs,ctor_candidates,base_lineage"]
    for vstart in sorted(vtables):
        v = vtables[vstart]
        nm = v["info"]["class_name"]
        thunk_ord = ""
        thunk_va = ""
        for (sv, (vv, so, cn)) in slot_map.items():
            if vv == vstart:
                thunk_ord = so
                thunk_va = sv
        rows = [r for r in stores if r[1] == vstart]
        sf = " ".join("0x%08X" % r[0] for r in rows)
        cc = " ".join("0x%08X" % f for (f, i) in class_ctor.get(vstart, []))
        lineage = " <- ".join(b["name"] for b in v["chd"]["bases"][1:]) if v["chd"] else ""
        csv_rows.append("%s,0x%08X,%d,0x%08X,0x%08X,%d,%s,%s,%d,%s,%s,%s"
                        % (nm, v["info"]["col"]["va"], v["info"]["col"]["offset"],
                           vstart, v["end"], len(v["entries"]),
                           thunk_ord, thunk_va, len(rows), sf, cc, lineage))
    with open(os.path.join(RAW, "ARKANIMATION_VTABLE_MAP.csv"), "w") as f:
        f.write(chr(10).join(csv_rows) + chr(10))

    L.append("[B12] ARTIFACTS WRITTEN: RTTI_COL_RAW.txt, ARKANIMATION_VTABLE_MAP.csv,")
    L.append("       VTABLE_INVENTORY.csv, IMM32_THUNK_CENSUS.txt")
    out = os.path.join(RAW, "RTTI_COL_RAW.txt")
    with open(out, "w") as f:
        f.write(chr(10).join(L) + chr(10))
    print(chr(10).join(L))
    print("")
    print("WROTE: %s" % out)


if __name__ == "__main__":
    main()
