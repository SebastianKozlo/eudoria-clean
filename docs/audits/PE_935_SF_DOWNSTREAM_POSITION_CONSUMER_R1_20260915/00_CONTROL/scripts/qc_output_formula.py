# -*- coding: utf-8 -*-
"""QC_R3 probe: independent output-formula + origin-triple census.

Task PHASE 2 step 7, executed BEFORE reading the executor's correction
artifacts. STATIC-ONLY: binary never executed.

  7a. Re-verify from bytes: FUN_0082B5A0 computes
      out[i] = f32(f32(W[i]*K) - S[i]) with the qword constant
      K @ 0xA7B360 == 0x3F847AE140000000, and returns with `ret 8`.
  7b. Re-verify the origin-triple census denominator: whole-file imm32
      occurrences of 0x00BA921C / 0x00BA9220 / 0x00BA9224, decode-verified
      and classified (code operand vs data reference vs writer).

Output: 00_CONTROL/QC_R3_RAW/QC_R3_OUTPUT_FORMULA_RAW.txt
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
RAW_FILE = os.path.join(RAW_DIR, "QC_R3_OUTPUT_FORMULA_RAW.txt")

FORMULA_FN = 0x0082B5A0
K_VA = 0x00A7B360
K_EXPECT = 0x3F847AE140000000
TRIPLE = [0x00BA921C, 0x00BA9220, 0x00BA9224]
GETTER = 0x00437F70


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = open(RAW_FILE, "w", encoding="utf-8", newline="\n")

    def W(s=""):
        out.write(s + "\n")

    import capstone
    import platform
    W("QC_R3 INDEPENDENT OUTPUT FORMULA + TRIPLE CENSUS (qc_output_formula.py)")
    W("Mode: STATIC-ONLY. The client binary is never executed.")
    W("Python %s; capstone %s" % (platform.python_version(), capstone.__version__))
    data, sections = U.load_pinned()
    dis = U.Dis()
    W("S0 PIN OK: SIZE=%d SHA256=%s" % (U.EXPECT_SIZE, U.EXPECT_SHA256))

    W("")
    W("=" * 78)
    W("SECTION A: K CONSTANT @ 0x00A7B360")
    offK, secK = U.va_to_off(sections, K_VA)
    kval = struct.unpack_from("<Q", data, offK)[0]
    W("  raw qword at 0x00A7B360 = 0x%016X" % kval)
    W("  expected              = 0x%016X" % K_EXPECT)
    W("  MATCH: %s" % ("YES" if kval == K_EXPECT else "*** NO ***"))
    W("  as double: %.12g" % struct.unpack("<d", struct.pack("<Q", kval))[0])
    W("  as float32 of double mantissa bits: see QC_AUDIT_R3.md analysis")
    W("  context:")
    for i in range(-16, 24, 8):
        v = struct.unpack_from("<Q", data, offK + i)[0]
        W("    0x%08X : 0x%016X" % (K_VA + i, v))

    W("")
    W("=" * 78)
    W("SECTION B: FUN_0082B5A0 FULL DECODE")
    end, n_ins, reason = U.function_extent(dis, data, sections, FORMULA_FN)
    W("extent: 0x%08X .. 0x%08X (%d instructions, %s)" % (FORMULA_FN, end, n_ins, reason))
    fn_ins, _s = dis.stream(data, sections, FORMULA_FN, end - FORMULA_FN, 2000, detail=True)
    for ins in fn_ins:
        line = "  " + U.fmt_ins(ins)
        note = []
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            t = ins.operands[0].imm
            if t == GETTER:
                note.append("<<< GETTER 0x437F70")
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == 0 and op.mem.disp == K_VA:
                note.append("<<< K constant reference")
        if note:
            line += "   ; " + " ".join(note)
        W(line)
    last = fn_ins[-1] if fn_ins else None
    W("terminal instruction: %s %s" % (last.mnemonic, last.op_str) if last else "none")
    W("ret-8 check: %s" % ("PASS" if (last and last.mnemonic == "ret"
                                      and last.op_str == "8") else "SEE DECODE ABOVE"))

    W("")
    W("=" * 78)
    W("SECTION C: ORIGIN TRIPLE IMM32 CENSUS (whole file)")
    W("NOTE: classification collects ALL decode anchors (back 1..6); the")
    W("containing instruction is among the candidates. A DIRECT WRITE is")
    W("flagged when ANY anchored candidate instruction writes [addr].")
    for addr in TRIPLE:
        occ = U.imm32_census(data, sections, addr)
        W("")
        W("- 0x%08X: %d whole-file imm32 occurrences" % (addr, len(occ)))
        direct_writes = 0
        reads = 0
        pushes = 0
        other = 0
        unresolved = 0
        for _off, va, secname in occ:
            if secname in (".text",):
                cands = []
                start, _ev = U.find_function_start(dis, data, sections, va)
                if start is not None and start <= va:
                    ins_list, _st = dis.stream(data, sections, start,
                                               va - start + 16, 200000)
                    for ins in ins_list:
                        if ins.address <= va < ins.address + ins.size:
                            cands.append(("fn:0x%08X" % start, ins))
                            break
                        if ins.address > va:
                            break
                # multi-anchor collection: one-instruction decode per anchor;
                # later-byte invalidity does not veto a containing instruction
                seen = set()
                for back in range(1, 12):
                    s_va = va - back
                    s_off, _s2 = U.va_to_off(sections, s_va)
                    if s_off is None:
                        continue
                    one_list, _stop = dis.stream(data, sections, s_va, back + 16, 1)
                    if not one_list:
                        continue
                    ins = one_list[0]
                    if ins.address <= va < ins.address + ins.size:
                        key = (ins.address, ins.size)
                        if key not in seen:
                            seen.add(key)
                            cands.append(("anchor@0x%08X" % ins.address, ins))
                if not cands:
                    unresolved += 1
                    W("  0x%08X (%s): UNRESOLVED (no fn-start, no anchor)" % (va, secname))
                    continue
                # classify: check EVERY candidate for a direct write; describe
                # the SHORTEST anchored instruction (the moffs form is compact)
                cands.sort(key=lambda t: t[1].size)
                best_k, best = cands[0]
                is_write = False
                is_read = False
                is_push = False
                moffs = "dword ptr [0x%x]" % addr
                for _k, ins in cands:
                    parts = [p.strip() for p in ins.op_str.split(",")]
                    op0 = parts[0]
                    # DIRECT WRITE: dst operand is EXACTLY the moffs [addr]
                    # (excludes garbage [ecx + 0xba921c] pseudo-decodes)
                    if ins.mnemonic in ("mov", "fstp", "fistp", "add", "sub",
                                        "and", "or", "xor", "inc", "dec") \
                            and op0 == moffs:
                        is_write = True
                    # READ: a read-class instruction reads [addr]
                    if moffs in parts and \
                            ins.mnemonic in ("mov", "fld", "fild", "cmp"):
                        is_read = True
                    if ins.mnemonic == "push" and ("0x%x" % addr) in parts:
                        is_push = True
                if is_write:
                    direct_writes += 1
                    W("  0x%08X (%s): %s: %s %s  *** DIRECT WRITE ***"
                      % (va, secname, best_k, best.mnemonic, best.op_str))
                else:
                    kind = "READ" if is_read else ("ADDR-PUSH" if is_push else "OTHER")
                    if kind == "READ":
                        reads += 1
                    elif kind == "ADDR-PUSH":
                        pushes += 1
                    elif kind == "OTHER":
                        other += 1
                    W("  0x%08X (%s): %s: %s %s  [%s]"
                      % (va, secname, best_k, best.mnemonic, best.op_str, kind))
            else:
                W("  0x%08X (%s) [data]" % (va, secname))
        W("  SUMMARY for 0x%08X: occurrences=%d direct_writes=%d reads=%d"
          " addr_pushes=%d other=%d unresolved=%d"
          % (addr, len(occ), direct_writes, reads, pushes, other, unresolved))

    W("")
    W("=" * 78)
    W("SECTION E: SINGLETON CONSTRUCTOR 0x0082B580 (S initialization from triple?)")
    insC, stopC = dis.stream(data, sections, 0x0082B580, 0x60, 64)
    for ins in insC:
        W("  " + U.fmt_ins(ins))
    W("  stream stop: %s" % stopC)

    W("")
    W("=" * 78)
    W("SECTION D: STATIC BYTES OF THE TRIPLE 0x00BA921C..0x00BA9228")
    hexoff, secT = U.va_to_off(sections, 0x00BA921C)
    if hexoff is None:
        W("  0x00BA921C is NOT in raw file data; containing section: %s"
          % (secT["name"] if secT else "<unmapped>"))
        W("  -> virtual-only (bss-like): zero-initialized at load; no file bytes.")
        W("  section range: 0x%08X..0x%08X rawlen 0x%X"
          % (0x400000 + secT["vaddr"], 0x400000 + secT["vaddr"] + secT["vsize"],
             secT["rsize"]) if secT else "")
    else:
        blob = data[hexoff:hexoff + 12]
        W("  bytes: %s" % blob.hex())
        f0, f1, f2 = struct.unpack("<fff", blob)
        W("  as three float32 (static file rest values): %r %r %r" % (f0, f1, f2))
    W("  context 0x00BA9200..0x00BA9240 (if mapped):")
    for i in range(0, 0x40, 16):
        va = 0x00BA9200 + i
        off, s2 = U.va_to_off(sections, va)
        if off is None:
            W("  0x%08X  <virtual-only: no file bytes>" % va)
            continue
        chunk = data[off:off + 16]
        W("  0x%08X  %s" % (va, " ".join("%02X" % b for b in chunk)))

    out.close()
    print("OK -> %s" % RAW_FILE)


if __name__ == "__main__":
    main()
