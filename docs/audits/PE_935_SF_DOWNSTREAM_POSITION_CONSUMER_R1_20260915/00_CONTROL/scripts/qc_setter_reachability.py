# -*- coding: utf-8 -*-
"""QC_R3 probe: independent origin setter decode + reachability re-derivation.

Task PHASE 2 steps 3, 5, 6, executed BEFORE reading the executor's
correction artifacts. STATIC-ONLY: binary never executed.

  3. Decode the setter at 0x00458D90 (extent, ABI, call to 0x437F70 at
     0x458E27, the three S writes, arithmetic before each write, esp
     ledger naming the stack slots that feed the writes, input types at
     [ecx+0/4/8], return behavior, EAX provenance at 0x458E2C).
  5. Re-derive both reported reachability branches and the true static
     chain (E8/E9/imm32/vtable channels, function extents, message loop
     0x402910, delta-condition 0x458EE2, ftol 0x95DA40 usage).
  6. Additional-channel census (direct references to the singleton slot
     0xBA1804 and other potential S writers).

Output: 00_CONTROL/QC_R3_RAW/QC_R3_REACHABILITY_RAW.txt
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qc_peutil as U
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW_DIR = os.path.join(PKG, "00_CONTROL", "QC_R3_RAW")
RAW_FILE = os.path.join(RAW_DIR, "QC_R3_REACHABILITY_RAW.txt")

SETTER = 0x00458D90
GETTER = 0x00437F70
SETTER_CALLER = 0x00458E50
FTOL = 0x0095DA40
MSGLOOP = 0x00402910

CHAIN = [SETTER, SETTER_CALLER, 0x00417030, 0x00416FD0, 0x00417880,
         0x00514EF0, 0x00417A40, 0x004B1B70, 0x004B1C70, 0x4172A0, GETTER]


def annotated_decode(dis, data, sections, start, end, watch=None, W=lambda s: None,
                     ledger_annotate=True):
    """Decode [start,end) and write disassembly with esp-ledger annotation.

    Tracks push/pop/sub/add esp + stdcall call cleanup; names [esp+X]/[ebp+Y]
    slot keys; highlights watched instructions.
    """
    ledger = 0
    ebp_key = None
    fn_ins, stop = dis.stream(data, sections, start, end - start, 4000, detail=True)
    retcache = {}
    for ins in fn_ins:
        m = ins.mnemonic
        line = "  " + U.fmt_ins(ins)
        notes = []
        if ledger_annotate:
            notes.append("esp_off=%d" % (-ledger))
            for op in ins.operands:
                if op.type == X86_OP_MEM:
                    base = ins.reg_name(op.mem.base) if op.mem.base else None
                    if base == "esp":
                        k = op.mem.disp - ledger
                        notes.append("[esp%+d]->slot%d" % (op.mem.disp, k))
                    elif base == "ebp" and ebp_key is not None:
                        notes.append("[ebp%+d]->slot%d" % (op.mem.disp, op.mem.disp + ebp_key))
        if watch and ins.address in watch:
            notes.append("<<< " + watch[ins.address])
        if notes:
            line += "   ; " + " ".join(notes)
        W(line)
        # ledger maintenance
        if m == "push" and ins.operands:
            ledger += 4
        elif m == "pop" and ins.operands:
            ledger -= 4
        elif (m == "sub" and len(ins.operands) > 1 and ins.operands[0].type == X86_OP_REG
              and ins.reg_name(ins.operands[0].reg) == "esp"):
            ledger += ins.operands[1].imm
        elif (m == "add" and len(ins.operands) > 1 and ins.operands[0].type == X86_OP_REG
              and ins.reg_name(ins.operands[0].reg) == "esp"):
            ledger -= ins.operands[1].imm
        elif m == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            tgt = ins.operands[0].imm
            if tgt not in retcache:
                head, _s = dis.stream(data, sections, tgt, 0x600, 600)
                nb = None
                for h in head:
                    if h.mnemonic in ("ret", "retf"):
                        parts = h.op_str.split()
                        nb = int(parts[0], 0) if parts else 0
                        break
                retcache[tgt] = nb
            nb = retcache[tgt]
            if nb:
                ledger -= nb
        elif (m == "mov" and len(ins.operands) > 1
              and ins.operands[0].type == X86_OP_REG
              and ins.reg_name(ins.operands[0].reg) == "ebp"
              and ins.operands[1].type == X86_OP_REG
              and ins.reg_name(ins.operands[1].reg) == "esp"):
            ebp_key = -ledger
        elif m == "leave":
            if ebp_key is not None:
                ledger = -(ebp_key + 4)
            ebp_key = None
    return fn_ins

def census_report(dis, data, sections, W, targets=None):
    """E8/E9 inbound census + whole-file imm32 references for CHAIN functions."""
    W("")
    W("=" * 78)
    W("SECTION D: INBOUND CHANNEL CENSUS (E8 / E9 / imm32 data refs)")
    for f in (targets or CHAIN):
        W("")
        W("- function 0x%08X" % f)
        e8 = U.xfer_census(data, sections, f, 0xE8)
        e9 = U.xfer_census(data, sections, f, 0xE9)
        W("  raw E8 (call) candidates: %d -> %s" % (len(e8), ["0x%08X" % x for x in e8]))
        for site in sorted(e8):
            start, ev = U.find_function_start(dis, data, sections, site)
            if start is None:
                W("    site 0x%08X: boundary UNRESOLVED (%s)" % (site, ev))
            else:
                W("    site 0x%08X: VERIFIED boundary; containing function starts 0x%08X"
                  % (site, start))
        W("  raw E9 (jmp) candidates: %d -> %s" % (len(e9), ["0x%08X" % x for x in e9]))
        for site in sorted(e9):
            start, ev = U.find_function_start(dis, data, sections, site)
            if start is None:
                W("    site 0x%08X: boundary UNRESOLVED (%s)" % (site, ev))
            else:
                W("    site 0x%08X: VERIFIED boundary; containing function starts 0x%08X"
                  % (site, start))
        occ = U.imm32_census(data, sections, f)
        W("  whole-file imm32 occurrences of this address: %d" % len(occ))
        for _off, va, secname in occ:
            if secname in (".text",):
                ins, cls = U.classify_occurrence(dis, data, sections, va)
                if ins is not None:
                    W("    0x%08X (%s): instruction 0x%08X: %s %s"
                      % (va, secname, ins.address, ins.mnemonic, ins.op_str))
                else:
                    W("    0x%08X (%s): %s" % (va, secname, cls))
            else:
                W("    0x%08X (%s) [data reference - potential vtable/pointer slot]"
                  % (va, secname))


def hexdump(data, sections, va, n, W):
    off, _s = U.va_to_off(sections, va)
    blob = data[off:off + n]
    for i in range(0, len(blob), 16):
        chunk = blob[i:i + 16]
        hexs = " ".join("%02X" % b for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        W("  0x%08X  %-47s  %s" % (va + i, hexs, asc))


def dword_dump(data, sections, va, n, W, label=""):
    W("  dword dump 0x%08X..0x%08X %s" % (va, va + n - 1, label))
    for a in range(va, va + n, 4):
        off, _s = U.va_to_off(sections, a)
        if off is None:
            W("    0x%08X <unmapped>" % a)
            continue
        v = struct.unpack_from("<I", data, off)[0]
        W("    0x%08X : 0x%08X" % (a, v))


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = open(RAW_FILE, "w", encoding="utf-8", newline="\n")

    def W(s=""):
        out.write(s + "\n")

    import capstone
    import platform
    W("QC_R3 INDEPENDENT SETTER + REACHABILITY PROBE (qc_setter_reachability.py)")
    W("Mode: STATIC-ONLY. The client binary is never executed.")
    W("Python %s; capstone %s" % (platform.python_version(), capstone.__version__))
    data, sections = U.load_pinned()
    dis = U.Dis()
    W("S0 PIN OK: SIZE=%d SHA256=%s" % (U.EXPECT_SIZE, U.EXPECT_SHA256))

    # ---------------- SECTION B: setter decode ----------------
    W("")
    W("=" * 78)
    W("SECTION B: ORIGIN SETTER 0x00458D90 - full decode (esp ledger annotated)")
    end, n_ins, reason = U.function_extent(dis, data, sections, SETTER)
    W("extent: 0x%08X .. 0x%08X (%d instructions, %s)" % (SETTER, end, n_ins, reason))
    watch = {}
    fn_ins, _stop = dis.stream(data, sections, SETTER, end - SETTER, 4000, detail=True)
    for ins in fn_ins:
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM \
                and ins.operands[0].imm == GETTER:
            watch[ins.address] = "CALL TO ORIGIN GETTER 0x437F70"
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base:
                b = ins.reg_name(op.mem.base)
                d = op.mem.disp
                if b == "ecx" and d in (0, 4, 8) and ins.mnemonic != "call":
                    watch.setdefault(ins.address,
                                     "INPUT READ [ecx%+d]" % d)
        if ins.address == 0x00458E2C:
            watch[ins.address] = "EAX_PROVENANCE point: state of EAX here"
        if 0x458ED0 <= ins.address <= 0x458F00:
            watch.setdefault(ins.address, "delta-condition region")
    annotated_decode(dis, data, sections, SETTER, end, watch=watch, W=W)

    W("")
    W("SECTION B2: SETTER SEMANTICS SUMMARY (derived from the decode above)")
    W("  (see QC_AUDIT_R3.md for the narrative; this raw file carries the bytes)")

    # ---------------- SECTION C: boundary 0x416FD0 / 0x417030 ----------------
    W("")
    W("=" * 78)
    W("SECTION C: BOUNDARY QUESTION - 0x416FD0 extent vs next function 0x417030")
    endC, nC, reasonC = U.function_extent(dis, data, sections, 0x00416FD0)
    W("function_extent(0x00416FD0): end 0x%08X (%d ins, %s)" % (endC, nC, reasonC))
    W("last instructions of the function ending near 0x41702C:")
    fnC, _s = dis.stream(data, sections, 0x00417000, 0x40, 32)
    for ins in fnC:
        W("  " + U.fmt_ins(ins))
    W("raw bytes 0x00417018..0x00417040:")
    hexdump(data, sections, 0x00417018, 0x28, W)
    W("decode starting exactly at 0x00417030:")
    fnD, _s = dis.stream(data, sections, 0x00417030, 0x60, 24)
    for ins in fnD:
        W("  " + U.fmt_ins(ins))
    W("decode starting exactly at 0x0041702D (claimed dispatch anchor):")
    fnX, stopX = dis.stream(data, sections, 0x0041702D, 0x20, 8)
    if stopX == "invalid" and not fnX:
        W("  <no instruction decodes at 0x0041702D>")
    for ins in fnX:
        W("  " + U.fmt_ins(ins))
    W("decode starting exactly at 0x0041702C:")
    fnY, _s = dis.stream(data, sections, 0x0041702C, 0x20, 8)
    for ins in fnY:
        W("  " + U.fmt_ins(ins))

    # ---------------- SECTION D: inbound censuses ----------------
    census_report(dis, data, sections, W)

    # ---------------- SECTION E: vtables and data ----------------
    W("")
    W("=" * 78)
    W("SECTION E: VTABLE / DATA READS")
    W("vtable region 0x00A7D764 (slot k at 0xA7D764+4k):")
    dword_dump(data, sections, 0x00A7D764, 0x40, W, label="(claimed vtable)")
    W("slot5 @ 0x00A7D778 -> see dword dump above")
    W("context bytes 0x00A7D750..0x00A7D7B0:")
    hexdump(data, sections, 0x00A7D750, 0x60, W)
    W("")
    W("region 0x00A7A240..0x00A7A290 (claimed to contain a 'vtable' at 0xA7A244):")
    dword_dump(data, sections, 0x00A7A240, 0x50, W, label="")
    W("context bytes 0x00A7A230..0x00A7A2A0:")
    hexdump(data, sections, 0x00A7A230, 0x70, W)
    W("")
    W("COL global 0x00AA1304:")
    dword_dump(data, sections, 0x00AA1304, 0x10, W, label="(COL)")
    W("context bytes 0x00AA12F0..0x00AA1320:")
    hexdump(data, sections, 0x00AA12F0, 0x30, W)
    W("")
    W("K constant qword @ 0x00A7B360:")
    offK, _s = U.va_to_off(sections, 0x00A7B360)
    W("  raw qword = 0x%016X" % struct.unpack_from("<Q", data, offK)[0])
    dK = struct.unpack_from("<Q", data, offK)[0]
    W("  double value = %.10g" % struct.unpack("<d", struct.pack("<Q", dK))[0])
    W("context bytes 0x00A7B350..0x00A7B380:")
    hexdump(data, sections, 0x00A7B350, 0x30, W)
    W("")
    W("origin singleton slot 0x00BA1804 (static file value):")
    offS, secS = U.va_to_off(sections, 0x00BA1804)
    if offS is None:
        W("  NOT in raw file data; containing section: %s (virtual tail: zero-initialized at load)"
          % (secS["name"] if secS else "<unmapped>"))
        W("  -> the singleton slot has NO static initializer bytes; it is populated at runtime.")
    else:
        W("  static dword = 0x%08X" % struct.unpack_from("<I", data, offS)[0])
    W("context bytes 0x00BA17F0..0x00BA1820 (if mapped):")
    offC2, _s = U.va_to_off(sections, 0x00BA17F0)
    if offC2 is not None:
        hexdump(data, sections, 0x00BA17F0, 0x30, W)
    else:
        W("  <virtual-only: no file bytes>")
    W("")
    W("SECTION E2: DIRECT REFERENCES TO THE SINGLETON SLOT 0x00BA1804")
    occ = U.imm32_census(data, sections, 0x00BA1804)
    W("whole-file imm32 occurrences: %d" % len(occ))
    for _off, va, secname in occ:
        if secname in (".text",):
            ins, cls = U.classify_occurrence(dis, data, sections, va)
            if ins is not None:
                start, _ev = U.find_function_start(dis, data, sections, ins.address)
                W("  0x%08X (%s) instruction 0x%08X in 0x%08X: %s %s"
                  % (va, secname, ins.address, start or 0, ins.mnemonic, ins.op_str))
            else:
                W("  0x%08X (%s) %s" % (va, secname, cls))
        else:
            W("  0x%08X (%s) [data]" % (va, secname))

    # ---------------- SECTION F: message loop ----------------
    W("")
    W("=" * 78)
    W("SECTION F: MESSAGE LOOP 0x00402910")
    fnM, _s = dis.stream(data, sections, 0x00402910, 0x120, 200)
    for ins in fnM:
        line = "  " + U.fmt_ins(ins)
        if ins.address == 0x0040296F:
            line += "   ; <<< claimed tick call"
        W(line)
    W("(loop head / back-edge determination in QC_AUDIT_R3.md from the bytes above)")

    # ---------------- SECTION G: branch B functions ----------------
    W("")
    W("=" * 78)
    W("SECTION G: BRANCH B FUNCTIONS 0x00417A40 AND 0x004B1B70")
    W("0x00417A40 decode (first 0x100 bytes):")
    fnA, _s = dis.stream(data, sections, 0x00417A40, 0x100, 128, detail=True)
    for ins in fnA:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM \
                and ins.operands[0].imm == SETTER:
            line += "   ; <<< CALL TO SETTER 0x458D90"
        W(line)
    W("")
    W("0x004B1B70 linear decode through 0x004B1F40 (self-recursion check):")
    fnB, _s = dis.stream(data, sections, 0x004B1B70, (0x004B1F40 - 0x004B1B70 + 0x20), 1200, detail=True)
    for ins in fnB:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM \
                and ins.operands[0].imm == 0x00417A40:
            line += "   ; <<< CALL TO 0x417A40"
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM \
                and ins.operands[0].imm == 0x004B1B70:
            line += "   ; <<< SELF-RECURSIVE CALL"
        W(line)
        if ins.address > 0x004B1F38:
            break

    # ---------------- SECTION H: setter caller 0x458E50 ----------------
    W("")
    W("=" * 78)
    W("SECTION H: 0x00458E50 (setter caller) - decode")
    endH, nH, reasonH = U.function_extent(dis, data, sections, 0x00458E50)
    W("extent: 0x00458E50 .. 0x%08X (%d ins, %s)" % (endH, nH, reasonH))
    fnH, _s = dis.stream(data, sections, 0x00458E50, endH - 0x00458E50, 2000, detail=True)
    for ins in fnH:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            t = ins.operands[0].imm
            if t == FTOL:
                line += "   ; <<< ftol 0x95DA40"
            elif t == SETTER:
                line += "   ; <<< SETTER 0x458D90"
            elif t == GETTER:
                line += "   ; <<< GETTER 0x437F70"
        W(line)

    # ---------------- SECTION I: chain boundary resolution ----------------
    W("")
    W("=" * 78)
    W("SECTION I: CHAIN BOUNDARY RESOLUTION (branch A/B attribution questions)")
    W("")
    W("I.1: is 0x00417880 a function start, and is 0x004178CF inside it?")
    startU, evU = U.find_function_start(dis, data, sections, 0x00417880)
    W("  find_function_start(0x00417880) = %s (%s)"
      % (("0x%08X" % startU) if startU else "NONE", evU))
    insU, _s = dis.stream(data, sections, 0x00417870, 0x80, 64)
    for ins in insU:
        W("    " + U.fmt_ins(ins))
    endU, nU, rU = U.function_extent(dis, data, sections, 0x00417880)
    W("  function_extent(0x00417880) = end 0x%08X (%d ins, %s)" % (endU, nU, rU))
    W("")
    W("I.2: does the 0x00417880 function contain 0x004178CF / 0x00417972?")
    W("  0x004178CF is inside 0x00417880's extent: %s"
      % ("YES" if (endU and 0x00417880 <= 0x004178CF < endU) else "NO"))
    W("  0x00417972 (E8 caller of 0x416FD0) inside: %s"
      % ("YES" if (endU and 0x00417972 < endU) else "NO"))
    W("")
    W("I.3: 0x00514EF0 extent vs 0x005159CB / 0x005159E5:")
    endV, nV, rV = U.function_extent(dis, data, sections, 0x00514EF0)
    W("  function_extent(0x00514EF0) = end 0x%08X (%d ins, %s)" % (endV, nV, rV))
    W("  0x005159CB inside 0x00514EF0's extent: %s"
      % ("YES" if (endV and 0x005159CB < endV) else "NO"))
    W("  0x005159E5 (E8 caller of 0x417880) inside: %s"
      % ("YES" if (endV and 0x005159E5 < endV) else "NO"))
    insV, _s = dis.stream(data, sections, 0x005159A0, 0x60, 32)
    for ins in insV:
        W("    " + U.fmt_ins(ins))
    W("")
    W("I.4: 0x004B1C70 (candidate true branch-B parent) start + 0x004B1B70 end:")
    endW_, nW_, rW_ = U.function_extent(dis, data, sections, 0x004B1B70)
    W("  function_extent(0x004B1B70) = end 0x%08X (%d ins, %s)" % (endW_, nW_, rW_))
    startW, evW = U.find_function_start(dis, data, sections, 0x004B1C70)
    W("  find_function_start(0x004B1C70) = %s (%s)"
      % (("0x%08X" % startW) if startW else "NONE", evW))
    insW, _s = dis.stream(data, sections, 0x004B1C60, 0x30, 24)
    for ins in insW:
        W("    " + U.fmt_ins(ins))
    W("")
    W("I.5: attribution of the two branch-B E8 sites (hardened finder):")
    for site in (0x004B1EEB, 0x004B1F2C):
        st, ev = U.find_function_start(dis, data, sections, site)
        W("  site 0x%08X -> containing function %s (%s)"
          % (site, ("0x%08X" % st) if st else "NONE", ev))

    # ---------------- SECTION J: 0x416FD0 outbound calls ----------------
    W("")
    W("=" * 78)
    W("SECTION J: 0x00416FD0 OUTBOUND DIRECT CALLS (branch A subtree bound)")
    endK, nK, rK = U.function_extent(dis, data, sections, 0x00416FD0)
    W("  extent 0x00416FD0..0x%08X (%d ins, %s)" % (endK, nK, rK))
    fnK, _s = dis.stream(data, sections, 0x00416FD0, endK - 0x00416FD0, 200, detail=True)
    for ins in fnK:
        line = "    " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            line += "   ; -> 0x%08X" % ins.operands[0].imm
            if ins.operands[0].imm in (SETTER, SETTER_CALLER, 0x00417030, GETTER):
                line += "   *** CHAIN TARGET ***"
        W(line)
    W("  (branch A claim requires 0x416FD0 -> 0x458E50; check the call list above)")

    # ---------------- SECTION K: guard chain inside 0x417030 + message-loop caller ----------------
    W("")
    W("=" * 78)
    W("SECTION K: GUARD WINDOW INSIDE 0x00417030 + MESSAGE-LOOP CALLER VERIFICATION")
    W("K.1 decode window 0x00417190..0x004171C0 + skip target 0x00417216:")
    insK, _s = dis.stream(data, sections, 0x00417190, 0x30, 24, detail=True)
    for ins in insK:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            line += "   ; -> 0x%08X" % ins.operands[0].imm
        W(line)
    W("  skip target:")
    insK2, _s2 = dis.stream(data, sections, 0x00417216, 0x18, 8, detail=True)
    for ins in insK2:
        W("  " + U.fmt_ins(ins))
    W("K.2 0x00458E50's guard (call 0x4143f0 -> 0x7ce1e0 -> test eax -> je skip) re-check:")
    insK3, _s3 = dis.stream(data, sections, 0x00458E56, 0x18, 8, detail=True)
    for ins in insK3:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            line += "   ; -> 0x%08X" % ins.operands[0].imm
        W(line)
    W("K.3 message-loop inbound caller 0x0040563A verification:")
    insK4, _s4 = dis.stream(data, sections, 0x00405630, 0x20, 12, detail=True)
    for ins in insK4:
        line = "  " + U.fmt_ins(ins)
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            line += "   ; -> 0x%08X" % ins.operands[0].imm
        W(line)
    stK, evK = U.find_function_start(dis, data, sections, 0x0040563A)
    W("  containing function of 0x0040563A: %s (%s)"
      % (("0x%08X" % stK) if stK else "NONE", evK))
    W("K.4 0x42bc20 bounded head (guard callee):")
    insK5, _s5 = dis.stream(data, sections, 0x0042bc20, 0x40, 16, detail=True)
    for ins in insK5:
        W("  " + U.fmt_ins(ins))

    out.close()
    print("OK -> %s" % RAW_FILE)


if __name__ == "__main__":
    main()
