# w2_censuses.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# W2 (a) E8/E9/EB direct-call census of .text targeting FUN_0050A050 (+ CAL-2
#     known-answer: same machinery pointed at FUN_005247C0 must find 7 sites).
# W2 (b) whole-file imm32 (LE dword) census of 0x0050A050 (+ NC-4 vtable-entry
#     pin; + CAL-1 known-answer: same scanner pointed at 0x00A7D458 must
#     reproduce the ctor/dtor vtable stores 0x00509366 / 0x0050A269).
# B.3 re-verification (fail-closed pins, from bytes): holder-slot reader example
#     0x0052901A + call 0x5094C0 @0x00529020; SF ctor FUN_00509330 E8 callers;
#     vtable imm32 stores; [SF+0x30] writers 0x005093C3 / 0x0050A2D1; holder
#     writer-function start bytes.
#
# Outputs (01_RAW, deterministic):
#   CENSUS_E8_DIRECT.txt, CENSUS_IMM32_0050A050.txt, B3_PIN_REVERIFICATION.txt

import struct
import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
TARGET_FUN = 0x0050A050
SF_VTABLE = 0x00A7D458
SF_VTABLE_SLOT3_DWORD_VA = 0x00A7D464  # [0x00A7D458 + 0x0C]


def e8_census(exe, target, label):
    """Scan rule: EVERY byte position of .text where the byte is 0xE8/0xE9/0xEB
    is treated as a potential jmp/call opcode; target = va + insn_len + rel.
    Includes operand-byte false positives by design (census rule recorded)."""
    text = exe.text_section()
    t_va = exe.image_base + text["vaddr"]
    t_bytes = exe.read_off(text["rawptr"], text["rawsize"])
    e8_total = 0
    e8_hits, e9_hits, eb_hits = [], [], []
    for i in range(len(t_bytes) - 5):
        b = t_bytes[i]
        va = t_va + i
        if b == 0xE8:
            e8_total += 1
            rel = struct.unpack_from("<i", t_bytes, i + 1)[0]
            if va + 5 + rel == target:
                e8_hits.append(va)
        elif b == 0xE9:
            rel = struct.unpack_from("<i", t_bytes, i + 1)[0]
            if va + 5 + rel == target:
                e9_hits.append(va)
        elif b == 0xEB:
            rel = struct.unpack_from("<b", t_bytes, i + 1)[0]
            if va + 2 + rel == target:
                eb_hits.append(va)
    return {
        "label": label,
        "text_va_start": t_va,
        "text_va_end": t_va + text["rawsize"],
        "text_bytes_scanned": text["rawsize"],
        "e8_total": e8_total,
        "e8_hits": e8_hits,
        "e9_hits": e9_hits,
        "eb_hits": eb_hits,
    }


def imm32_census(exe, dword):
    """Scan rule: EVERY byte position of the WHOLE FILE is tested for the LE
    encoding of dword (no alignment requirement)."""
    needle = struct.pack("<I", dword)
    data = exe.data
    hits = []
    i = data.find(needle)
    while i != -1:
        va = exe.off_to_va(i)
        hits.append((i, va))
        i = data.find(needle, i + 1)
    return hits


def main():
    exe = C.PinnedExe()
    md = C.make_capstone()

    prov = C.provenance_header()
    s0 = f"S0: PASS (sha256 {exe.sha256}, size {exe.size})"

    # ---------------- (a) E8/E9/EB census ----------------
    e8r = e8_census(exe, TARGET_FUN, "FUN_0050A050")
    cal2 = e8_census(exe, 0x005247C0, "FUN_005247C0 (CAL-2 known answer: expect 7 E8 sites)")
    ctor = e8_census(exe, 0x00509330, "FUN_00509330 (B.3: expect E8 callers {0x0047D043, 0x0052480F})")
    lines = []
    lines.append("CENSUS_E8_DIRECT — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (W2a)")
    lines.append(prov)
    lines.append(s0)
    lines.append("")
    lines.append("SCAN RULE: every byte position of .text where the byte is 0xE8 (call rel32),")
    lines.append("0xE9 (jmp rel32) or 0xEB (jmp rel8) is treated as a potential opcode; target =")
    lines.append("va + insn_len + rel. Byte-level scan (operand-byte false positives included by")
    lines.append("design; this is a census denominator, not a decode).")
    lines.append("")
    for r in (e8r, cal2, ctor):
        lines.append(f"== target {r['label']} ==")
        lines.append(f".text range: {r['text_va_start']:#010x}..{r['text_va_end']:#010x} "
                     f"({r['text_bytes_scanned']} bytes scanned)")
        lines.append(f"total E8 byte occurrences in .text (denominator): {r['e8_total']}")
        lines.append(f"E8 matches to target: {len(r['e8_hits'])} -> {[f'{v:#010x}' for v in r['e8_hits']]}")
        lines.append(f"E9 (jmp rel32) matches to target: {len(r['e9_hits'])} -> {[f'{v:#010x}' for v in r['e9_hits']]}")
        lines.append(f"EB (jmp rel8) matches to target: {len(r['eb_hits'])} -> {[f'{v:#010x}' for v in r['eb_hits']]}")
        lines.append("")
    lines.append("CAL-2 VERDICT: " + (
        "PASS — 7 E8 call sites found" if len(cal2["e8_hits"]) == 7 else
        f"FAIL — found {len(cal2['e8_hits'])} (expected 7)"))
    cal2_site_bytes = []
    for v in sorted(cal2["e8_hits"]):
        ins = next(md.disasm(exe.read_va(v, 8), v), None)
        cal2_site_bytes.append(C.insn_str(ins) if ins else f"{v:#010x} <decode failed>")
    lines.append("CAL-2 measured call-site instructions:")
    lines.extend("  " + b for b in cal2_site_bytes)
    lines.append("")
    lines.append("B.3 ctor-caller check: " + (
        "MATCH {0x0047D043, 0x0052480F}"
        if sorted(ctor["e8_hits"]) == [0x0047D043, 0x0052480F]
        else f"MEASURED {sorted(hex(v) for v in ctor['e8_hits'])} vs pin {{0x0047D043, 0x0052480F}} — PIN_MISMATCH finding if different"))
    lines.append("")
    with open(PKG + r"\01_RAW\CENSUS_E8_DIRECT.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    # ---------------- (b) imm32 census ----------------
    hits = imm32_census(exe, TARGET_FUN)
    cal1 = imm32_census(exe, SF_VTABLE)
    m = []
    m.append("CENSUS_IMM32_0050A050 — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (W2b)")
    m.append(prov)
    m.append(s0)
    m.append("")
    m.append("SCAN RULE: every byte position of the WHOLE FILE is tested for the little-endian")
    m.append("dword encoding of the target (byte-level, no alignment requirement); every hit is")
    m.append("mapped file-offset -> VA (+ section) when the offset lies in a mapped section raw range.")
    m.append("")
    m.append(f"== LE dword {TARGET_FUN:#010x} (bytes {struct.pack('<I', TARGET_FUN).hex(' ').upper()}) whole-file census ==")
    m.append(f"hit count: {len(hits)} (published expectation: exactly 1, at the vtable dword {SF_VTABLE_SLOT3_DWORD_VA:#010x})")
    for off, va in hits:
        if va is None:
            m.append(f"  file_off={off:#010x} VA=<none: outside section raw ranges> section=<header/unmapped>")
        else:
            m.append(f"  file_off={off:#010x} VA={va:#010x} section={exe.section_name_of_va(va)}")
    va_set = [va for _, va in hits if va is not None]
    nc4 = exe.read_va(SF_VTABLE_SLOT3_DWORD_VA, 4)
    nc4_val = struct.unpack("<I", nc4)[0]
    m.append(f"NC-4 vtable-entry pin: dword at {SF_VTABLE_SLOT3_DWORD_VA:#010x} measured {nc4_val:#010x} "
             + ("== 0x0050A050 MATCH" if nc4_val == TARGET_FUN else "MISMATCH"))
    m.append("")
    m.append(f"== CAL-1 known-answer: same scanner pointed at SF vtable {SF_VTABLE:#010x} (bytes {struct.pack('<I', SF_VTABLE).hex(' ').upper()}) ==")
    m.append(f"hit count: {len(cal1)}")
    for off, va in sorted(cal1, key=lambda x: (x[1] is None, x[1] or 0)):
        if va is None:
            m.append(f"  file_off={off:#010x} VA=<none> section=<header/unmapped>")
        else:
            m.append(f"  file_off={off:#010x} VA={va:#010x} section={exe.section_name_of_va(va)}")
    # calibration acceptance: a hit within the store instructions at 0x00509366 / 0x0050A269
    def hits_in(va_lo, span):
        return [va for _, va in cal1 if va is not None and va_lo <= va < va_lo + span]
    h1 = hits_in(0x00509366, 6)
    h2 = hits_in(0x0050A269, 6)
    m.append(f"CAL-1 hits within ctor store instruction [0x00509366..0x0050936C): {h1}")
    m.append(f"CAL-1 hits within dtor store instruction [0x0050A269..0x0050A26F): {h2}")
    m.append("CAL-1 VERDICT: " + ("PASS — both published stores reproduced" if h1 and h2 else
                                 "FAIL — one or both known-answer stores not reproduced"))
    m.append("")
    m.append("measured store instructions:")
    for va in (0x00509366, 0x0050A269):
        ins = next(md.disasm(exe.read_va(va, 10), va), None)
        m.append(f"  {C.insn_str(ins) if ins else f'{va:#010x} <decode failed>'}")
    m.append("")
    with open(PKG + r"\01_RAW\CENSUS_IMM32_0050A050.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(m) + "\n")

    # ---------------- B.3 re-verification ----------------
    b = []
    b.append("B3_PIN_REVERIFICATION — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (W2 starting points, from bytes)")
    b.append(prov)
    b.append(s0)
    b.append("")
    b.append("== holder-slot reader example (LINK30 C9 published receiver proof) ==")
    for va in (0x0052901A, 0x00529020):
        ins = next(md.disasm(exe.read_va(va, 10), va), None)
        b.append(f"  {C.insn_str(ins) if ins else f'{va:#010x} <decode failed>'}")
    exp_reader = exe.read_va(0x0052901A, 6).hex(" ").upper()
    b.append(f"  reader pin: 0x0052901A expect '8B 8E C0 00 00 00' (mov ecx,[esi+0xC0]) measured {exp_reader} "
             + ("MATCH" if exp_reader == "8B 8E C0 00 00 00" else "MISMATCH"))
    if exp_reader == "8B 8E C0 00 00 00":
        pass
    # call target check at 0x00529020
    call_bytes = exe.read_va(0x00529020, 5)
    rel = struct.unpack_from("<i", call_bytes, 1)[0]
    tgt = 0x00529020 + 5 + rel
    b.append(f"  call at 0x00529020: bytes {call_bytes.hex(' ').upper()} -> target {tgt:#010x} "
             + ("== 0x005094C0 MATCH" if tgt == 0x005094C0 else "MISMATCH"))
    b.append("")
    b.append("== SF ctor FUN_00509330 E8 callers (B.3 pin {0x0047D043, 0x0052480F}) ==")
    b.append(f"  measured: {[f'{v:#010x}' for v in sorted(ctor['e8_hits'])]}")
    for v in sorted(ctor["e8_hits"]):
        ins = next(md.disasm(exe.read_va(v, 8), v), None)
        b.append(f"  caller site: {C.insn_str(ins) if ins else f'{v:#010x} <decode failed>'}")
    b.append("")
    b.append("== vtable imm32 stores (from CAL-1) ==")
    for va in (0x00509366, 0x0050A269):
        ins = next(md.disasm(exe.read_va(va, 10), va), None)
        b.append(f"  {C.insn_str(ins) if ins else f'{va:#010x} <decode failed>'}")
    b.append("")
    b.append("== [SF+0x30] writer pins (B.3: 0x005093C3 ctor, 0x0050A2D1 dtor body FUN_0050A240) ==")
    for va in (0x005093C3, 0x0050A2D1):
        ins = next(md.disasm(exe.read_va(va, 10), va), None)
        b.append(f"  {C.insn_str(ins) if ins else f'{va:#010x} <decode failed>'}")
    b.append("")
    b.append("== holder-slot writer functions (B.3 labels; start-bytes existence record only —")
    b.append("   deep writer verification NOT claimed this run; bound declared in the report) ==")
    for fva, note in (
        (0x0044D590, "writer of container+0x0C/+0x10/+0x14"),
        (0x00528E50, "writer of container+0xC0 (the instance+0xC0 slot)"),
        (0x0067B800, "writer of container+0x04"),
        (0x0067C7C0, "writer of container+0x04"),
        (0x006A3930, "writer of container+0x18"),
    ):
        d = list(md.disasm(exe.read_va(fva, 16), fva))
        b.append(f"  FUN_{fva:08X} ({note}): entry bytes {exe.read_va(fva, 8).hex(' ').upper()}")
        for ins in d[:3]:
            b.append("    " + C.insn_str(ins))
    b.append("")
    with open(PKG + r"\01_RAW\B3_PIN_REVERIFICATION.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(b) + "\n")

    print("W2a E8 census:", e8r["e8_total"], "E8 bytes scanned; matches to 0x0050A050:", len(e8r["e8_hits"]))
    print("CAL-2:", "PASS" if len(cal2["e8_hits"]) == 7 else f"FAIL ({len(cal2['e8_hits'])})")
    print("W2b imm32 census hits:", len(hits), "->", [f"{va:#x}" if va else f"off{o:#x}" for o, va in hits])
    print("CAL-1:", "PASS" if h1 and h2 else "FAIL")
    print("NC-4:", "MATCH" if nc4_val == TARGET_FUN else "MISMATCH")
    print("wrote 01_RAW/CENSUS_E8_DIRECT.txt, CENSUS_IMM32_0050A050.txt, B3_PIN_REVERIFICATION.txt")


if __name__ == "__main__":
    main()
