# amend_r1_reverify.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# R1 AMENDMENT BATCH (PE-MASTER loop 2ed038db-5d2e-4e7e-b679-2d29bf57501a,
# adjudicated correction 2026-09-14). Re-derives EVERY pin of the PE-MASTER
# adjudication finding from the pinned Entropia.exe (fail-closed S0 first),
# reproduces the pre-fix VTABLE-BOUNDARY OVERRUN artifact from the same bytes,
# re-derives the corrected (vtable-extent-verified) state, re-derives the
# corrected method-1 aggregate from the package's own raw, verifies the FIX-5
# instruction bytes, and asserts the R1 immutability set (all raws other than
# the regenerated ARG2_PRODUCER_TRACE.txt byte-identical to their pre-batch
# MANIFEST_SHA256.csv rows; all scripts other than the fixed
# w2c_w3_virtual_census.py unchanged; the immutable inputs unchanged).
#
# STATIC-ONLY: Entropia.exe is NEVER executed; this script only READS bytes.
# Deterministic: no wall-clock, sorted iteration where order matters.
#
# Output: 01_RAW/AMEND_R1_PIN_REVERIFICATION.txt

import hashlib
import struct
import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C
import capstone

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
SF_VTABLE = 0x00A7D458
ARK_VTABLE = 0x00A7D42C
ARK_COL_PTR_VA = 0x00A7D428
SF_COL_PTR_VA = SF_VTABLE - 4
SF_SLOT3_FUN = 0x0050A050
SF_KNOWN_SLOT_FUNCS = {0x50A460: 0, 0x5090A0: 1, 0x5090B0: 2, 0x50A050: 3,
                       0x5090C0: 4, 0x509580: 5}
POSTFIX_SCRIPT_SHA256 = "576A37D09C18958BD5CB841AB22CE6D8B1CCC807CD8A678DEF7525E4CF94B40B"
POSTFIX_TRACE_SHA256 = "10AA922952A0A8AE3280EED55BBB48F928A39A44DD153FC39B442DBD6455655F"
PREBATCH_TRACE_SHA256 = "FD10AABD5294987F0386402671DBE118098515C4606E1F0B97C8FFB68FCFDBC6"
PREBATCH_CSV_SHA256 = "7B74CB5D04E13D692207760A6DA40AD3FB3840AAB7502B457685AB2DF9EE8009"


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def main():
    out = []
    out.append("AMEND_R1_PIN_REVERIFICATION — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (R1 amendment batch)")
    out.append(C.provenance_header())

    # ---------------- S0 fail-closed ----------------
    exe = C.PinnedExe()
    out.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")
    img = exe.image_base
    ts = exe.text_section()
    text_lo = img + ts["vaddr"]
    text_hi = img + ts["vaddr"] + ts["vsize"]
    data = exe.data
    out.append(f".text VA range (vsize-based, the extent-rule bound): {text_lo:#010x}..{text_hi:#010x}")
    out.append("")

    def dw(va):
        return struct.unpack_from("<I", data, exe.va_to_off(va))[0]

    def td_name(td_va):
        raw = exe.read_va(td_va + 8, 64)
        nul = raw.find(b"\x00")
        return raw[:nul].decode("ascii", "replace") if 0 < nul <= 64 else "?"

    def vtable_extent(va):
        n = 0
        while True:
            try:
                fv = dw(va + 4 * n)
            except Exception:
                break
            if not (text_lo <= fv < text_hi):
                break
            n += 1
        return n

    # ---------------- PE-MASTER adjudication pins (re-derived) ----------------
    out.append("== PIN SET 1: the .?AVArkAudioObjectInterface@@ vtable (PE-MASTER adjudication) ==")
    ark_col = dw(ARK_COL_PTR_VA)
    out.append(f"[{ARK_COL_PTR_VA:#010x}] = {ark_col:#010x}   (COL pointer at vtable[-1]; pin 0x00AA1270: "
               + ("MATCH" if ark_col == 0x00AA1270 else "MISMATCH"))
    ark_ptd = dw(ark_col + 0x0C)
    out.append(f"COL+0x0C pTypeDescriptor = {ark_ptd:#010x}   (pin 0x00B7880C: "
               + ("MATCH" if ark_ptd == 0x00B7880C else "MISMATCH"))
    aname = td_name(ark_ptd)
    out.append(f"TD name = {aname!r}   (pin '.?AVArkAudioObjectInterface@@': "
               + ("MATCH" if aname == ".?AVArkAudioObjectInterface@@" else "MISMATCH"))
    ark_n = vtable_extent(ARK_VTABLE)
    ark_vals = [dw(ARK_VTABLE + 4 * i) for i in range(ark_n)]
    out.append(f"vtable extent @ {ARK_VTABLE:#010x}: EXACTLY {ark_n} slots (pin 6: "
               + ("MATCH" if ark_n == 6 else "MISMATCH") + f"); slots: "
               + "; ".join(f"slot {i} @ {ARK_VTABLE + 4 * i:#010x} = {v:#010x}" for i, v in enumerate(ark_vals)))
    pin_ark = [0x00509040, 0x0096B960, 0x0096B960, 0x00509010, 0x0096B960, 0x007E19D0]
    out.append("slot-value pin [0x00509040, 0x0096B960, 0x0096B960, 0x00509010, 0x0096B960, 0x007E19D0]: "
               + ("MATCH" if ark_vals == pin_ark else "MISMATCH"))
    out.append("")

    out.append("== PIN SET 2: the 'ArkSceneFeeder' separator + the SF COL + the SF vtable ==")
    sep_start = ARK_VTABLE + 4 * ark_n
    sep = exe.read_va(sep_start, SF_COL_PTR_VA - sep_start)
    out.append(f"bytes @ {sep_start:#010x}..{SF_COL_PTR_VA - 1:#010x}: {sep.hex(' ').upper()}  reads: {sep!r}")
    out.append("pin 'ArkSceneFeeder\\0' bytes 41 72 6B 53 63 65 6E 65 46 65 65 64 65 72 00 (+pad 00): "
               + ("MATCH" if sep == b"ArkSceneFeeder\x00\x00" else "MISMATCH"))
    sf_col = dw(SF_COL_PTR_VA)
    out.append(f"[{SF_COL_PTR_VA:#010x}] = {sf_col:#010x}   (SF COL pointer; pin 0x00AA12B8: "
               + ("MATCH" if sf_col == 0x00AA12B8 else "MISMATCH"))
    sf_ptd = dw(sf_col + 0x0C)
    sname = td_name(sf_ptd)
    out.append(f"SF COL+0x0C pTypeDescriptor = {sf_ptd:#010x}; TD name = {sname!r}   (pin '.?AVSceneFeederObject@@': "
               + ("MATCH" if sname == ".?AVSceneFeederObject@@" else "MISMATCH"))
    sf_n = vtable_extent(SF_VTABLE)
    sf_vals = [dw(SF_VTABLE + 4 * i) for i in range(sf_n)]
    out.append(f"SF vtable extent @ {SF_VTABLE:#010x}: EXACTLY {sf_n} slots; slots: "
               + "; ".join(f"slot {i} @ {SF_VTABLE + 4 * i:#010x} = {v:#010x}" for i, v in enumerate(sf_vals)))
    pin_sf = [0x0050A460, 0x005090A0, 0x005090B0, 0x0050A050, 0x005090C0, 0x00509580]
    out.append("slot-value pin [0x0050A460, 0x005090A0, 0x005090B0, 0x0050A050, 0x005090C0, 0x00509580]: "
               + ("MATCH" if sf_vals == pin_sf else "MISMATCH"))
    after = dw(SF_VTABLE + 4 * sf_n)
    out.append(f"first dword past the SF vtable @ {SF_VTABLE + 4 * sf_n:#010x} = {after:#010x} "
               f"(in .text: {text_lo <= after < text_hi} — extent rule ends the vtable here)")
    out.append("")

    out.append("== PIN SET 3: the imm32 census bound (exactly-one address occurrence) ==")
    needle = struct.pack("<I", SF_SLOT3_FUN)
    hits = []
    pos = 0
    while True:
        p = data.find(needle, pos)
        if p == -1:
            break
        hits.append((p, exe.off_to_va(p)))
        pos = p + 1
    out.append(f"whole-file LE-dword census of {SF_SLOT3_FUN:#010x}: hit count = {len(hits)}"
               + (f"; hit: " + "; ".join(f"off={o:#010x} VA={v:#010x} ({exe.section_name_of_va(v)})" for o, v in hits)))
    out.append("pin EXACTLY 1 hit at 0x00A7D464: "
               + ("MATCH" if len(hits) == 1 and hits[0][1] == 0x00A7D464 else "MISMATCH")
               + " — function-pointer sharing is EXCLUDED by the run's own evidence")
    out.append("")

    out.append("== PIN SET 4: the pre-fix 'slots 11..15' overrun arithmetic (artifact re-derivation) ==")
    for i in range(5):
        va = SF_VTABLE + 4 * i
        fake = (va - ARK_VTABLE) // 4
        out.append(f"  SF slot-{i} dword @ {va:#010x}: ({va:#010x} - {ARK_VTABLE:#010x})/4 = {fake}")
    out.append("== the pre-fix fixed-16-slot enumeration view of the ArkAudio vtable (the DEFECT, reproduced) ==")
    for slot in range(16):
        va = ARK_VTABLE + 4 * slot
        fv = dw(va)
        in_text = text_lo <= fv < text_hi
        loose = img <= fv < img + 0x10000000
        tag = "real slot" if slot < 6 else ("STRING bytes" if 6 <= slot <= 9 else
               ("SF COL pointer" if slot == 10 else "SF VTABLE slot " + str(slot - 11)))
        out.append(f"  slot {slot:2d} @ {va:#010x} = {fv:#010x}  in_text={in_text}  pre-fix-loose-check-accepted={loose}  -> {tag}")
    out.append("the pre-fix rule (img <= fv < img+0x10000000, NO break on non-hit) read through the 6 real slots,")
    out.append("the 'ArkSceneFeeder' string bytes (slots 6-9 — ALL rejected by the loose range check too:")
    out.append("slots 6-8 exceed img+0x10000000; slot 9 falls below img), the SF COL pointer (slot 10, ACCEPTED),")
    out.append("and the SF vtable slots 0-4 (slots 11-15, ACCEPTED) — the fabricated memberships")
    out.append("('ArkAudioObjectInterface', 10..15) are VTABLE-BOUNDARY OVERRUN artifacts.")
    out.append("")

    out.append("== PIN SET 5: corrected memberships (vtable-extent rule) vs pre-fix (loose 16-slot rule) ==")

    def build_fn_slots(extent_rule):
        fn_slots = {}
        tds = []
        pos = 0
        while True:
            p = data.find(b".?A", pos)
            if p == -1:
                break
            name_va = exe.off_to_va(p)
            if name_va is not None:
                nul = data.find(b"\x00", p)
                if nul != -1 and 0 < nul - p < 256 and all(32 <= c < 127 for c in data[p:nul]):
                    td_va = name_va - 8
                    if td_va >= img:
                        tds.append((td_va, data[p:nul].decode("ascii")))
            pos = p + 1
        for td_va, name in tds:
            needle2 = struct.pack("<I", td_va)
            q = data.find(needle2)
            while q != -1:
                col_va = exe.off_to_va(q - 0x0C) if q >= 0x0C else None
                if col_va is not None and col_va >= img:
                    n2 = struct.pack("<I", col_va)
                    r = data.find(n2)
                    while r != -1:
                        vt_va = exe.off_to_va(r + 4)
                        if vt_va is not None and vt_va >= img:
                            base_off = exe.va_to_off(vt_va)
                            if base_off is not None:
                                if extent_rule:
                                    slot = 0
                                    while True:
                                        try:
                                            fv = struct.unpack_from("<I", data, base_off + 4 * slot)[0]
                                        except Exception:
                                            break
                                        if not (text_lo <= fv < text_hi):
                                            break
                                        fn_slots.setdefault(fv, []).append((name, slot))
                                        slot += 1
                                else:
                                    for slot in range(16):
                                        try:
                                            fv = struct.unpack_from("<I", data, base_off + 4 * slot)[0]
                                        except Exception:
                                            break
                                        if img <= fv < img + 0x10000000:
                                            fn_slots.setdefault(fv, []).append((name, slot))
                        r = data.find(n2, r + 1)
                q = data.find(needle2, q + 1)
        return fn_slots

    pre = build_fn_slots(False)
    post = build_fn_slots(True)
    out.append(f"fn_slots map size: pre-fix={len(pre)}; post-fix (extent rule)={len(post)}")
    for fn, slot in sorted(SF_KNOWN_SLOT_FUNCS.items()):
        p_m = sorted(pre.get(fn, []))
        q_m = sorted(post.get(fn, []))
        one_each = q_m == [(".?AVSceneFeederObject@@", slot)]
        out.append(f"  FUN_{fn:08X}: pre={p_m}; post={q_m}   exactly-one-membership: "
                   + ("MATCH (the SF vtable itself, slot " + str(slot) + ")" if one_each else "MISMATCH"))
    out.append("")
    out.append("== the extent fix's downstream consequences (recorded for PE-MASTER; NOT adjudicated) ==")
    for enc in (0x007AC2F0, 0x007F1D70, 0x006FAB80):
        pc = sorted({c for c, _ in pre.get(enc, [])})
        qc = sorted({c for c, _ in post.get(enc, [])})
        out.append(f"  {enc:#010x}: pre-fix classes ({len(pc)}) = {pc}")
        out.append(f"  {enc:#010x}: post-fix classes ({len(qc)}) = {qc}")
        if len(qc) == 1:
            sl = sorted(s for c, s in post[enc])
            out.append(f"    -> extent-verified single class {qc[0]} (slots {sl})")
    out.append("")

    out.append("== PIN SET 6: the corrected method-1 aggregate (re-derived from the package raw) ==")
    import re as _re
    buckets = {}
    with open(PKG + r"\01_RAW\ARG2_PRODUCER_TRACE.txt", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            m = _re.match(r"mov reg,\[base\+0x([0-9a-f]+)\] reads \(base != esp/ebp, non-SIB\): (\d+)$", s)
            if m:
                buckets["+0x" + m.group(1)] = int(m.group(2))
    for k in sorted(buckets, key=lambda x: int(x, 16)):
        out.append(f"  bucket {k}: {buckets[k]}")
    total = sum(buckets.values())
    out.append(f"  SUM = {total}   (QC P1-QC-1 pin 25,905: " + ("MATCH" if total == 25905 else "MISMATCH") + ")")
    out.append("")

    out.append("== PIN SET 7: FIX-5 instruction bytes (the refcount-increment paraphrase correction) ==")
    ctor = exe.read_va(0x006FABA0, 40)
    out.append(f"bytes @ 0x006FABA0 (40B): {ctor.hex(' ').upper()}")
    i_mov_edx = ctor.find(b"\xBA\x01\x00\x00\x00")
    ok = i_mov_edx != -1 and ctor[i_mov_edx + 5:i_mov_edx + 7] == b"\x74\x03" \
        and ctor[i_mov_edx + 7:i_mov_edx + 10] == b"\x01\x51\x04"
    out.append("pin 'mov edx,1' (BA 01 00 00 00) + 'je +3' (74 03) + 'add [ecx+4],edx' (01 51 04): "
               + ("MATCH — the increment is via edx, NOT an immediate (P3-QC-3; the analysis paraphrase is corrected)" if ok else "MISMATCH"))
    out.append("")

    out.append("== R1 FILE STATE (script-computed SHA256 at reverify run time) ==")
    out.append(f"  00_Control/w2c_w3_virtual_census.py (post-fix):  {sha256_file(PKG + chr(92) + r'00_Control\w2c_w3_virtual_census.py')}")
    out.append("    pin (post-fix generator): " + POSTFIX_SCRIPT_SHA256)
    out.append(f"  01_RAW/ARG2_PRODUCER_TRACE.txt (regenerated):    {sha256_file(PKG + chr(92) + r'01_RAW\ARG2_PRODUCER_TRACE.txt')}")
    out.append("    pin (regenerated trace): " + POSTFIX_TRACE_SHA256)
    out.append(f"  01_RAW/ARG2_PRODUCER_TRACE.txt pre-batch was:    {PREBATCH_TRACE_SHA256}")
    out.append(f"  01_RAW/VIRTUAL_CALLSITE_CENSUS.csv (RETAINED):   {sha256_file(PKG + chr(92) + r'01_RAW\VIRTUAL_CALLSITE_CENSUS.csv')}")
    out.append("    pin (pre-batch CSV, byte-identical per the batch freeze): " + PREBATCH_CSV_SHA256)
    for doc in [r"02_ANALYSIS\ARG2_ANALYSIS.md", r"02_ANALYSIS\SCIENCE_STATUS_DELTA.csv",
                r"03_EVIDENCE\EVIDENCE_INDEX.csv", r"06_REPORT\REPORT.md",
                r"06_REPORT\HANDOFF.md", r"06_REPORT\STAGE_ACCEPTANCE_GATES.csv"]:
        out.append(f"  {doc}: {sha256_file(PKG + chr(92) + doc)}")
    out.append("")

    out.append("== R1 IMMUTABILITY ASSERT (vs the pre-batch MANIFEST_SHA256.csv rows) ==")
    manifest = {}
    with open(PKG + r"\06_REPORT\MANIFEST_SHA256.csv", encoding="utf-8") as f:
        next(f)
        for line in f:
            line = line.strip()
            if line:
                p, h = line.split(",", 1)
                manifest[p] = h
    expected_changed = {"01_RAW/ARG2_PRODUCER_TRACE.txt", "00_CONTROL/w2c_w3_virtual_census.py"}
    amend_docs = {"02_ANALYSIS/ARG2_ANALYSIS.md", "02_ANALYSIS/SCIENCE_STATUS_DELTA.csv", "03_EVIDENCE/EVIDENCE_INDEX.csv", "06_REPORT/REPORT.md", "06_REPORT/HANDOFF.md", "06_REPORT/STAGE_ACCEPTANCE_GATES.csv", "00_CONTROL/SCRIPT_SHA256.csv", "06_REPORT/MANIFEST_SHA256.csv"}
    fails = 0
    for path in sorted(manifest):
        h_disk = sha256_file(PKG + "\\" + path)
        if path in expected_changed:
            verdict = "CHANGED-BY-DESIGN (regenerated/fixed; see AMEND_LOG_R1.md)"
            ok_i = h_disk == (POSTFIX_TRACE_SHA256 if path.endswith("ARG2_PRODUCER_TRACE.txt") else POSTFIX_SCRIPT_SHA256)
            if not ok_i:
                verdict = "UNEXPECTED-VALUE"
                fails += 1
        elif path in amend_docs:
            verdict = "EDITED-BY-DESIGN (R1 document corrections; see AMEND_LOG_R1.md)"
        else:
            ok_i = h_disk == manifest[path]
            verdict = "UNCHANGED" if ok_i else "MUTATED (!)"
            if not ok_i:
                fails += 1
        out.append(f"  {'OK ' if '(!)' not in verdict and verdict != 'UNEXPECTED-VALUE' else 'FAIL'} {path}: {verdict}")
    out.append(f"IMMUTABILITY ASSERT: " + ("PASS (all non-amended files byte-identical to their pre-batch rows)"
                if fails == 0 else f"FAIL ({fails} unexpected mutations)"))
    out.append("")
    out.append("QC_AUDIT.md is NOT covered by MANIFEST_SHA256.csv (by design, per the QC session's note);")
    out.append("its byte-identity is asserted in the amendment record against its pre-batch hash.")
    out.append("")

    with open(PKG + r"\01_RAW\AMEND_R1_PIN_REVERIFICATION.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("wrote 01_RAW/AMEND_R1_PIN_REVERIFICATION.txt")
    print("immutability fails:", fails)


if __name__ == "__main__":
    main()
