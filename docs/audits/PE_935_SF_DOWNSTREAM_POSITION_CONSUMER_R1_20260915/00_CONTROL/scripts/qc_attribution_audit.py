# -*- coding: utf-8 -*-
"""QC_R3 attribution audit: adjudicate function-start disagreements between
my hardened finder (1-byte-run-after-ret candidates) and the executor's
census attributions. STATIC-ONLY; S0 fail-closed.

For each disputed census site, compare two candidate starts (MINE vs the
executor's): bytes around each candidate, prologue decode, inbound E8/E9/
imm32 channels (real function starts are usually called; mid-function
boundaries are not), and whether the earlier candidate's clean decode
reaches the site.

Output: 00_CONTROL/QC_R3_RAW/QC_R3_ATTRIBUTION_AUDIT.txt
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qc_peutil as U

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW_DIR = os.path.join(PKG, "00_CONTROL", "QC_R3_RAW")
RAW_FILE = os.path.join(RAW_DIR, "QC_R3_ATTRIBUTION_AUDIT.txt")

# disputed (site, my_start, executor_start)
DISPUTES = [
    (0x006C1C2A, 0x006C1A90, 0x006C19B0),
    (0x006C1C5C, 0x006C1A90, 0x006C19B0),
    (0x006C1C9A, 0x006C1A90, 0x006C19B0),
    (0x006C1CB5, 0x006C1A90, 0x006C19B0),
    (0x006C4E8E, 0x006C4E70, 0x006C4C40),
    (0x006C4EE9, 0x006C4E70, 0x006C4C40),
    (0x006E23FA, 0x006E23B0, 0x006E21F0),
    (0x006E2441, 0x006E23B0, 0x006E21F0),
    (0x008CD556, 0x008CD3E0, 0x008CD1A0),
    (0x008CD645, 0x008CD3E0, 0x008CD1A0),
]


def inbound(data, sections, f):
    e8 = U.xfer_census(data, sections, f, 0xE8)
    e9 = U.xfer_census(data, sections, f, 0xE9)
    imm = U.imm32_census(data, sections, f)
    return e8, e9, imm


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = open(RAW_FILE, "w", encoding="utf-8", newline="\n")

    def W(s=""):
        out.write(s + "\n")

    data, sections = U.load_pinned()
    dis = U.Dis()
    W("S0 PIN OK: SIZE=%d SHA256=%s" % (U.EXPECT_SIZE, U.EXPECT_SHA256))
    pairs = sorted(set((m, e) for _s, m, e in DISPUTES))
    for mine, theirs in pairs:
        W("")
        W("=" * 78)
        W("CANDIDATE PAIR: mine=0x%08X  executor=0x%08X" % (mine, theirs))
        for label, cand in (("MINE", mine), ("EXECUTOR", theirs)):
            off, _s = U.va_to_off(sections, cand)
            W("  %s candidate 0x%08X:" % (label, cand))
            W("    bytes before: %s" % " ".join("%02X" % c for c in data[off - 12:off]))
            W("    bytes at:     %s" % " ".join("%02X" % c for c in data[off:off + 16]))
            insH, _r = dis.stream(data, sections, cand, 48, 6)
            for ins in insH:
                W("      " + U.fmt_ins(ins))
            e8, e9, imm = inbound(data, sections, cand)
            W("    inbound E8: %d %s" % (len(e8), ["0x%08X" % x for x in e8]))
            W("    inbound E9: %d %s" % (len(e9), ["0x%08X" % x for x in e9]))
            W("    imm32 data refs: %d %s" % (len(imm), [hex(v[1]) for v in imm]))
            for site_va in e8:
                st, ev = U.find_function_start(dis, data, sections, site_va)
                ok = U.decodes_to(dis, data, sections, site_va, site_va) if st is None else None
                ins_list, _r2 = dis.stream(data, sections, site_va, 8, 1)
                one = ins_list[0] if ins_list else None
                W("      inbound E8 site 0x%08X: boundary-in-fn=%s; decodes as: %s %s"
                  % (site_va, ("0x%08X" % st) if st else "UNRESOLVED",
                     one.mnemonic if one else "?", one.op_str if one else "?"))
            if mine != cand:
                reach = U.decodes_to(dis, data, sections, cand, mine)
                W("    clean decode from 0x%08X reaches my candidate 0x%08X: %s"
                  % (cand, mine, "YES (my candidate is a real boundary of the"
                     " same stream; if my candidate is NOT called anywhere, it"
                     " is likely a mid-function boundary)" if reach else "NO"))
        for _site, m, e in DISPUTES:
            if m == mine and e == theirs:
                r1 = U.decodes_to(dis, data, sections, mine, _site)
                r2 = U.decodes_to(dis, data, sections, theirs, _site)
                W("  site 0x%08X: decodes-to from mine=%s from executor=%s"
                  % (_site, "YES" if r1 else "NO", "YES" if r2 else "NO"))
    out.close()
    print("OK -> %s" % RAW_FILE)


if __name__ == "__main__":
    main()
