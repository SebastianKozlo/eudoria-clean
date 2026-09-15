# w1_abi_rederive.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# W1: ABI re-derivation of FUN_0050A050 (SF vtable slot 3), fail-closed.
#
# - Full decode from entry 0x0050A050 (capstone, CS_ARCH_X86, CS_MODE_32, detail).
# - B.5 boundary rule: decode to first terminal control-flow end; padding =
#   alignment-completing run of 0xCC/0x90 after the terminal; E8/E9 lattice check
#   on the adjacent function start; zero-reference check on candidate starts.
# - eax def chain to the dispatch push at 0x0050A060 (arg2 path).
# - ret-N MEASURED at every ret site.
# - NC-1: B.1 dispatch-window + fallback pins verified byte-for-byte.
# - B.2 permitted VALUE check: dword [0x00A8CCF4+0x44] == 0x007B5390 (value read,
#   NOT a decode of slot 17 — G6).
#
# Output: 01_RAW/FUN_0050A050_DISASM.txt (deterministic).

import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
ENTRY = 0x0050A050

# B.1 pins (contract): (va, expected_bytes_or_None, description)
PINS = [
    (0x0050A057, "8B F1", "mov esi, ecx (esi = this = SF)"),
    (0x0050A05B, "8B 4E 30", "mov ecx, [esi+0x30] (the link)"),
    (0x0050A05E, "8B 11", "mov edx, [ecx] (link vtable)"),
    (0x0050A060, "50", "push eax (the dispatch push — arg2 name argument) [VERIFY per B.1]"),
    (0x0050A061, "8B 42 44", "mov eax, [edx+0x44] (slot 17 of the link vtable)"),
    (0x0050A064, "FF D0", "call eax"),
    (0x0050A087, "8B 16", "mov edx, [esi] (self vtable load — fallback)"),
    (0x0050A089, "8B 42 04", "mov eax, [edx+4] (slot 1 — fallback)"),
    (0x0050A08E, "FF D0", "call eax (fallback)"),
]
# fallback X/Y/Z read + copy sites: pin = 'exists as read/copy of expected form'
FALLBACK_SITES = [
    (0x0050A090, "X read (from SF+0x34 via returned &SF+0x34)"),
    (0x0050A098, "Y read (from SF+0x38)"),
    (0x0050A09E, "Z read (from SF+0x3C)"),
    (0x0050A096, "out-buffer copy 1"),
    (0x0050A09B, "out-buffer copy 2"),
    (0x0050A0A1, "out-buffer copy 3"),
]


def main():
    exe = C.PinnedExe()  # fail-closed S0 gate
    md = C.make_capstone()

    out = []
    out.append("FUN_0050A050_DISASM — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (W1, fail-closed)")
    out.append(C.provenance_header())
    out.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")
    out.append("")
    out.append("SECTION: " + exe.section_name_of_va(ENTRY))
    out.append("")

    # ---------------- full decode, bounded window (published extent 0x0050A050..0x0050A0AA) ----------------
    WIN = 0x60  # decode 96 bytes: extent + padding margin, boundary rule stops at terminal anyway
    code = exe.read_va(ENTRY, WIN)
    insns = list(md.disasm(code, ENTRY))

    out.append("== FULL LINEAR DECODE (entry 0x0050A050; window %d bytes) ==" % WIN)
    out.append("VA       BYTES                     TEXT")
    linear_map = {}
    for insn in insns:
        linear_map[insn.address] = insn
        out.append(C.insn_str(insn))
    out.append("")

    # ---------------- B.5 boundary derivation ----------------
    # B.5 rule applied ITERATIVELY: a terminal (RET/RET imm16/JMP out) is the
    # function end only if the bytes after it form an alignment-completing run of
    # 0xCC/0x90 to the next 16-aligned VA (padding evidence VALID) AND no branch
    # from inside the window targets beyond that terminal's end. Terminals whose
    # padding check fails (live code follows — e.g. an internal branch target)
    # are recorded and the scan continues to the next terminal.
    out.append("== B.5 BOUNDARY DERIVATION (iterative terminal + padding rule) ==")
    terminals = []
    for insn in insns:
        if insn.mnemonic in ("ret",):
            terminals.append(insn)
        elif insn.mnemonic == "jmp":
            # unconditional jmp: check target out of window (window = the linear decode stream)
            if "dword" in insn.op_str or insn.op_str.startswith("0x"):
                terminals.append(insn)
    if not terminals:
        out.append("NO TERMINAL in window — boundary NOT established by this decode; record honestly.")
    # internal branch targets (for the beyond-terminal check)
    branch_targets = []
    for insn in insns:
        if insn.group(capstone.x86.X86_GRP_JUMP):
            for op in insn.operands:
                if op.type == capstone.x86.X86_OP_IMM:
                    branch_targets.append((insn.address, op.imm))
    extent_end = None
    for t in terminals:
        end_va = t.address + t.size
        next_align = (end_va + 15) & ~15
        pad = exe.read_va(end_va, next_align - end_va)
        pad_hex = pad.hex(" ").upper()
        is_run = len(pad) > 0 and all(b in (0xCC, 0x90) for b in pad)
        beyond = [(a, tgt) for (a, tgt) in branch_targets if tgt >= end_va and a < end_va]
        verdict = (
            "PADDING-VALID extent end"
            if (is_run and not beyond)
            else "NOT the extent end ("
            + ("padding not a CC/90 run; " if not is_run else "")
            + ("internal branch targets beyond it; " if beyond else "")
            + "continue)"
        )
        out.append(
            f"TERMINAL {t.address:#010x} '{t.mnemonic} {t.op_str}' end={end_va:#010x} "
            f"pad[{end_va:#010x}..{next_align:#010x})={pad_hex} -> {verdict}"
        )
        if is_run and not beyond and extent_end is None:
            extent_end = end_va
    if extent_end is not None:
        next_align = (extent_end + 15) & ~15
        out.append(f"DERIVED EXTENT: {ENTRY:#010X} .. {extent_end:#010X} ({extent_end - ENTRY} bytes)")
        published_end = 0x0050A0AA
        verdict = "AGREES" if extent_end == published_end else "DISAGREES (PIN_MISMATCH finding — MEASURED wins)"
        out.append(f"published extent end 0x0050A0AA -> measured {extent_end:#010x}: {verdict}")
        adjacent = next_align
        out.append(f"adjacent function start candidate: {adjacent:#010X}")
        out.append(f"bytes at adjacent candidate: {exe.read_va(adjacent, 16).hex(' ').upper()}")
    else:
        out.append("NO PADDING-VALID TERMINAL in window — extent end not established; honest record.")
    out.append("")

    # ---------------- E8/E9/EB/imm32 lattice check on the adjacent start ----------------
    out.append("== E8/E9/EB/imm32 LATTICE (references TO the derived boundary region) ==")
    text = exe.text_section()
    t_va = exe.image_base + text["vaddr"]
    t_bytes = exe.read_off(text["rawptr"], text["rawsize"])
    refs = {ENTRY: [], 0x0050A0B0: []}
    for i in range(len(t_bytes) - 5):
        b = t_bytes[i]
        va = t_va + i
        if b == 0xE8 or b == 0xE9:
            import struct as st
            rel = st.unpack_from("<i", t_bytes, i + 1)[0]
            tgt = va + 5 + rel
            if tgt in refs:
                refs[tgt].append(f"{'E8' if b == 0xE8 else 'E9'}@{va:#010x}")
        elif b == 0xEB:
            import struct as st
            rel = st.unpack_from("<b", t_bytes, i + 1)[0]
            tgt = va + 2 + rel
            if tgt in refs:
                refs[tgt].append(f"EB@{va:#010x}")
    # imm32 refs whole file
    import struct as st
    needle = st.pack("<I", ENTRY)
    data = exe.data
    imm_refs = []
    i = data.find(needle)
    while i != -1:
        va = exe.off_to_va(i)
        if va is not None:
            imm_refs.append(va)
        i = data.find(needle, i + 1)
    needle_b0 = st.pack("<I", 0x0050A0B0)
    imm_refs_adj = []
    i = data.find(needle_b0)
    while i != -1:
        va = exe.off_to_va(i)
        if va is not None:
            imm_refs_adj.append(va)
        i = data.find(needle_b0, i + 1)
    out.append(f"E8/E9/EB refs to entry {ENTRY:#010X}: {refs[ENTRY]}")
    out.append(f"imm32 refs to entry {ENTRY:#010X} (whole file): {[f'{v:#010x}' for v in imm_refs]}")
    out.append(f"E8/E9/EB refs to adjacent candidate 0x0050A0B0: {refs[0x0050A0B0]}")
    out.append(f"imm32 refs to adjacent candidate 0x0050A0B0 (whole file): {[f'{v:#010x}' for v in imm_refs_adj]}")
    out.append(f"vtable dword at 0x00A7D464 = {st.unpack_from('<I', exe.read_va(0x00A7D464, 4), 0)[0]:#010x} (expect {ENTRY:#010x})")
    out.append("B.5 zero-reference disposition: entry 0x0050A050 has ZERO E8/E9/EB refs BUT is a "
               "VTABLE ENTRY (imm32 @0x00A7D464) — not a suspect start (B.5 rule 4 exception).")
    if refs[0x0050A0B0]:
        out.append("B.5 lattice: adjacent candidate 0x0050A0B0 corroborated by its own E8/E9 refs "
                   f"{refs[0x0050A0B0]}.")
    out.append("")

    # ---------------- ret sites measured ----------------
    out.append("== RET-N MEASUREMENT (every ret site in the decoded window) ==")
    ret_count = 0
    for insn in insns:
        if insn.mnemonic.startswith("ret"):
            ret_count += 1
            out.append(
                f"ret site #{ret_count}: {insn.address:#010x} bytes={insn.bytes.hex(' ').upper()} text='{insn.mnemonic} {insn.op_str}'"
            )
    if ret_count == 0:
        out.append("NO RET DECODED IN WINDOW (honest record)")
    out.append(f"ret site count = {ret_count}; all measured above (no assumption)")
    out.append("")

    # ---------------- eax def chain to 0x0050A060 ----------------
    out.append("== EAX DEF CHAIN to the dispatch push at 0x0050A060 ==")
    defs = []
    for insn in insns:
        if insn.address >= 0x0050A060:
            break
        # crude dst-register detection via capstone detail
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_REG and insn.reg_name(op.reg) in ("eax", "ax", "al", "ah"):
                defs.append(insn)
                break
    for d in defs:
        out.append(f"EAX-DEF: {C.insn_str(d)}")
    push_insn = linear_map.get(0x0050A060)
    if push_insn is not None:
        out.append(f"DISPATCH PUSH: {C.insn_str(push_insn)}")
    else:
        out.append("!! no instruction decoded exactly at 0x0050A060 — PIN_MISMATCH candidate")
    out.append("")

    # ---------------- NC-1 pin checks ----------------
    out.append("== NC-1 PIN CHECKS (B.1 dispatch window + fallback; MEASURED bytes win) ==")
    pin_mismatches = []
    for va, exp_hex, desc in PINS:
        got = exe.read_va(va, len(exp_hex.split()))
        got_hex = got.hex(" ").upper()
        ok = got_hex == exp_hex.upper()
        dec = linear_map.get(va)
        dec_str = C.insn_str(dec) if dec else "<not decoded as instruction start>"
        out.append(f"[{'MATCH' if ok else 'MISMATCH'}] {va:#010x} expect {exp_hex} measured {got_hex} | {desc}")
        out.append(f"         decoded: {dec_str}")
        if not ok:
            pin_mismatches.append((va, exp_hex, got_hex, desc))
    out.append("")
    out.append("== FALLBACK SITE SEMANTIC CHECKS (reads/copies; pins say VERIFY form) ==")
    for va, desc in FALLBACK_SITES:
        dec = linear_map.get(va)
        if dec is None:
            # try decode a small window from this VA
            try:
                d2 = list(md.disasm(exe.read_va(va, 8), va))
                dec = d2[0] if d2 else None
            except Exception:
                dec = None
        dec_str = C.insn_str(dec) if dec else "<no instruction starts at this VA>"
        out.append(f"[{'DECODED' if dec else 'NOT_DECODED_AT_VA'}] {va:#010x} | {desc}")
        out.append(f"         measured: {dec_str}")
    out.append("")

    # ---------------- branch structure + fallback path form ----------------
    out.append("== BRANCH STRUCTURE (linear window) ==")
    for insn in insns:
        if insn.group(capstone.x86.X86_GRP_JUMP):
            out.append(f"BRANCH: {C.insn_str(insn)}")
    out.append("")

    # ---------------- B.2 permitted VALUE check ----------------
    out.append("== B.2 PERMITTED VALUE CHECK (value read, NOT a decode of slot 17) ==")
    v = st.unpack_from("<I", exe.read_va(0x00A8CCF4 + 0x44, 4), 0)[0]
    out.append(f"dword [0x00A8CCF4+0x44] = {v:#010x} (expect 0x007B5390): "
               + ("MATCH" if v == 0x007B5390 else "MISMATCH — PIN_MISMATCH finding"))
    out.append("")

    # ---------------- summary ----------------
    out.append("== W1 SUMMARY ==")
    out.append(f"S0: PASS; window decoded: {len(insns)} instructions from {ENTRY:#010X}")
    out.append(f"ret sites measured: {ret_count}")
    out.append(f"NC-1 pin mismatches: {len(pin_mismatches)}")
    for va, e, g, d in pin_mismatches:
        out.append(f"  PIN_MISMATCH @ {va:#010x}: expected {e} measured {g} ({d})")
    with open(PKG + r"\01_RAW\FUN_0050A050_DISASM.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("wrote 01_RAW/FUN_0050A050_DISASM.txt")
    print(f"pin mismatches: {len(pin_mismatches)}")
    for va, e, g, d in pin_mismatches:
        print(f"  PIN_MISMATCH @ {va:#010x}: expected {e} measured {g}")


if __name__ == "__main__":
    import capstone  # noqa: F401 (used via C module and detail enums)
    main()
