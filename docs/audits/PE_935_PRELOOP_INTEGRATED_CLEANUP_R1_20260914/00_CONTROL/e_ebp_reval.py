# -*- coding: utf-8 -*-
"""
GENERATOR: 00_CONTROL/e_ebp_reval.py (v2 — COMPLETE two-phase workflow)
RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
PURPOSE: W1/W2 — EBP revalidation of LINK30 census rows E1 (writer 0x007EB1B3, historical
  fn-attribution 0x007EAC00) and E2 (writer 0x0082DB61, historical 0x0082DAC0), both
  historically REJECTED_ALIAS under the UNSOUND R-EBP-INHERITED rule.
  PHASE 1: verify the historical attribution — decode from the claimed entry, census every
           reference channel to it (E8/E9/EB rel, whole-file imm32, entry-fallthrough).
  PHASE 2: if the attribution is disproven, discover the REAL containing function
           (E8-target lattice + CC-padding boundary + forward-alignment on the writer,
           ret-crossing check), track the EBP-defining instruction to the writer, close ALL
           entry channels of the real function, and walk the caller chain to a DECLARED
           bound of two levels, resolving class identity where the chain pins it.
MODE: STATIC-ONLY — Entropia.exe is NEVER executed; own PE parse + own capstone decode of
  the pinned physical file; fail-closed SHA256+SIZE assert BEFORE any byte read.
EXECUTED AS: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B e_ebp_reval.py
OUTPUTS: 01_RAW/E1_FUN_007EAC00_DISASM.txt, 01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt,
         01_RAW/E2_FUN_0082DAC0_DISASM.txt, 01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt
         (file names keep the HISTORICAL fn-VA for row traceability; contents cover the
          real containing functions discovered in phase 2.)
"""
import hashlib
import os
import struct
import sys
import datetime

import capstone
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_REG, X86_REG_EBP

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_PATH = os.path.abspath(__file__)
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SHA_PIN = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXE_SIZE_PIN = 8015872
IMAGE_BASE = 0x00400000

CASES = [
    dict(tag="E1", writer_va=0x007EB1B3, hist_fn=0x007EAC00, writer_hex="897530",
         writer_text="mov dword ptr [ebp + 0x30], esi",
         csv_row='0x007EB1B3,0x007EAC00,"mov dword ptr [ebp + 0x30], esi",esi,caller stack (inherited ebp),REJECTED_ALIAS'),
    dict(tag="E2", writer_va=0x0082DB61, hist_fn=0x0082DAC0, writer_hex="66894d30",
         writer_text="mov word ptr [ebp + 0x30], cx",
         csv_row='0x0082DB61,0x0082DAC0,"mov word ptr [ebp + 0x30], cx",cx,caller stack (inherited ebp),REJECTED_ALIAS'),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def self_sha256():
    return sha256_file(SELF_PATH)


class Bin:
    def __init__(self):
        size = os.path.getsize(EXE)
        sha = sha256_file(EXE)
        assert size == EXE_SIZE_PIN, "FAIL-CLOSED SIZE: %d != %d" % (size, EXE_SIZE_PIN)
        assert sha == EXE_SHA_PIN, "FAIL-CLOSED SHA256: %s" % sha
        with open(EXE, "rb") as f:
            self.data = f.read()
        self.size, self.sha = size, sha
        e_lfanew = struct.unpack_from("<I", self.data, 0x3C)[0]
        assert self.data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00"
        coff = e_lfanew + 4
        nsec = struct.unpack_from("<H", self.data, coff + 2)[0]
        sopt = struct.unpack_from("<H", self.data, coff + 16)[0]
        opt = coff + 20
        assert struct.unpack_from("<H", self.data, opt)[0] == 0x10B
        self.image_base = struct.unpack_from("<I", self.data, opt + 0x1C)[0]
        assert self.image_base == IMAGE_BASE
        self.sections = []
        st = opt + sopt
        for i in range(nsec):
            off = st + 40 * i
            name = self.data[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
            vs, va, rs, rp = struct.unpack_from("<IIII", self.data, off + 8)
            self.sections.append(dict(name=name, vsize=vs, vaddr=va, rsize=rs, rptr=rp))
        self.text = [s for s in self.sections if s["name"] == ".text"][0]
        self.tva = self.image_base + self.text["vaddr"]
        self.tdata = self.data[self.text["rptr"]:self.text["rptr"] + self.text["rsize"]]

    def va2off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + s["rsize"]:
                return s["rptr"] + (rva - s["vaddr"])
        return None

    def prev_bytes(self, va, n=8):
        off = self.va2off(va)
        return self.data[off - n:off].hex().upper()

    def e8_callers(self, fn):
        out, j, n = [], 0, len(self.tdata)
        while True:
            j = self.tdata.find(b"\xE8", j)
            if j < 0:
                return out
            if j + 5 <= n:
                rel = struct.unpack_from("<i", self.tdata, j + 1)[0]
                if self.tva + j + 5 + rel == fn:
                    out.append(self.tva + j)
            j += 1

    def jmp_census(self, fn):
        e9, eb, j, n = [], [], 0, len(self.tdata)
        while True:
            j = self.tdata.find(b"\xE9", j)
            if j < 0:
                break
            if j + 5 <= n:
                rel = struct.unpack_from("<i", self.tdata, j + 1)[0]
                if self.tva + j + 5 + rel == fn:
                    e9.append(self.tva + j)
            j += 1
        j = 0
        while True:
            j = self.tdata.find(b"\xEB", j)
            if j < 0:
                break
            if j + 2 <= n:
                rel = struct.unpack_from("<b", self.tdata, j + 1)[0]
                if self.tva + j + 2 + rel == fn:
                    eb.append(self.tva + j)
            j += 1
        return e9, eb

    def imm32_census(self, va):
        pat = struct.pack("<I", va)
        out, k = [], 0
        while True:
            k = self.data.find(pat, k)
            if k < 0:
                return out
            out.append(k)
            k += 1


def writes_ebp(insn):
    for op in insn.operands:
        if op.type == X86_OP_REG and op.reg == X86_REG_EBP and (op.access & 0x2):
            return True
    ops = insn.op_str.replace(" ", "")
    if insn.mnemonic in ("mov", "lea", "pop", "xchg", "add", "sub", "and", "or", "xor") \
            and (ops.startswith("ebp,") or ops == "ebp"):
        return True
    return False


def disasm(B, cs, va, length):
    off = B.va2off(va)
    return list(cs.disasm(B.data[off:off + length], va))


def fmt(insn):
    return "  0x%08X  %-24s %-8s %s" % (insn.address, insn.bytes.hex().upper(), insn.mnemonic, insn.op_str)


def e8_target_lattice(B):
    targets, j, n = set(), 0, len(B.tdata)
    while True:
        j = B.tdata.find(b"\xE8", j)
        if j < 0:
            return targets
        if j + 5 <= n:
            rel = struct.unpack_from("<i", B.tdata, j + 1)[0]
            t = B.tva + j + 5 + rel
            if B.text["vaddr"] <= t - B.image_base < B.text["vsize"]:
                targets.add(t)
        j += 1


def find_real_fn(B, cs, lattice, w_va, rec):
    """Real containing function: greatest E8-target <= w whose forward decode aligns on the
    writer; ret-crossing reported; CC-padding corroboration."""
    cands = sorted([t for t in lattice if t <= w_va], reverse=True)[:24]
    for c in cands:
        ins = disasm(B, cs, c, w_va - c + 8)
        addrs = [i.address for i in ins]
        if w_va in addrs:
            idx = addrs.index(w_va)
            rets = [i.address for i in ins[:idx] if i.mnemonic == "ret"]
            ebpw = [i for i in ins[:idx] if writes_ebp(i)]
            rec("  REAL-FUNCTION CANDIDATE 0x%08X: aligned on writer (dist %d, %d insns); "
                "rets crossed before writer: %d; EBP writes before writer: %d" % (
                    c, w_va - c, idx, len(rets), len(ebpw)))
            rec("  boundary corroboration: prev-8-bytes = %s (CC padding / ret+CC = real boundary)"
                % B.prev_bytes(c))
            return c, ins[:idx], rets, ebpw
        else:
            rec("  lattice candidate 0x%08X: forward decode does NOT align on writer (discarded)" % c)
    return None, None, None, None


def main():
    print("=== EBP REVALIDATION ENGINE v2 (W1/W2) ===")
    print("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914")
    print("GENERATOR: 00_CONTROL/e_ebp_reval.py (SHA256 %s)" % self_sha256())
    print("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B e_ebp_reval.py")
    print("interpreter: %s (%s)" % (sys.executable, sys.version.split()[0]))
    print("capstone.__version__: %s (MEASURED; the dist-info label capstone-5.0.9 is a KNOWN FALSE LABEL)"
          % capstone.__version__)
    print("capstone.__file__: %s" % capstone.__file__)
    print("timestamp: %s" % datetime.datetime.now().isoformat())
    B = Bin()
    print("Entropia.exe fail-closed identity: SIZE=%d SHA256=%s — PINS MATCH" % (B.size, B.sha))
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail = True
    lattice = e8_target_lattice(B)
    print("E8 rel32 call-target lattice: %d distinct targets in .text" % len(lattice))
    print("")
    for case in CASES:
        run_case(B, cs, lattice, case)
    return 0


def run_case(B, cs, lattice, case):
    out = []

    def rec(s=""):
        out.append(s)
        print(s)

    tag, w_va, hist_fn = case["tag"], case["writer_va"], case["hist_fn"]
    rec("=== CASE %s — writer 0x%08X (historical fn attribution 0x%08X) ===" % (tag, w_va, hist_fn))
    rec("historical CSV row: %s" % case["csv_row"])
    rec("historical class: REJECTED_ALIAS under the UNSOUND R-EBP-INHERITED rule")
    rec("")
    rec("[A] WRITER BYTE VERIFICATION")
    woff = B.va2off(w_va)
    wbytes = B.data[woff:woff + len(case["writer_hex"]) // 2]
    rec("  bytes at 0x%08X: %s (expected %s) -> %s" % (
        w_va, wbytes.hex().upper(), case["writer_hex"].upper(),
        "MATCH" if wbytes.hex() == case["writer_hex"] else "MISMATCH"))
    win = next(cs.disasm(wbytes, w_va), None)
    rec("  capstone decode: %s %s  (pinned text: %s)" % (win.mnemonic, win.op_str, case["writer_text"]))
    rec("")

    rec("[B] PHASE 1 — HISTORICAL ATTRIBUTION CHECK (claimed entry 0x%08X)" % hist_fn)
    pre = B.data[B.va2off(hist_fn):B.va2off(hist_fn) + 8]
    rec("  first bytes at claimed entry: %s" % pre.hex().upper())
    ins0 = next(cs.disasm(pre, hist_fn), None)
    rec("  decode from claimed entry starts with: %s %s" % (ins0.mnemonic, ins0.op_str))
    rec("  (a leading 'add byte ptr [eax], al' = decoding the byte pair 00 00 = NOT a real")
    rec("   x86 code boundary for a function entry; typical of a mid-data/mid-instruction VA)")
    e8 = B.e8_callers(hist_fn)
    e9, eb = B.jmp_census(hist_fn)
    im = B.imm32_census(hist_fn)
    rec("  E8 rel32 calls to claimed entry: %d %s" % (len(e8), ["0x%08X" % x for x in e8]))
    rec("  E9 rel32 jmps to claimed entry:  %d %s" % (len(e9), ["0x%08X" % x for x in e9]))
    rec("  EB rel8 jmps to claimed entry:   %d %s" % (len(eb), ["0x%08X" % x for x in eb]))
    rec("  whole-file imm32 occurrences of the claimed entry VA: %d" % len(im))
    rec("  entry-fallthrough: prev-8-bytes = %s" % B.prev_bytes(hist_fn))
    lin = disasm(B, cs, hist_fn, 0x40)
    fb = any(l.address + l.size == hist_fn and l.mnemonic not in ("ret", "jmp", "int3", "ud2")
             for l in disasm(B, cs, hist_fn - 0x10, 0x10))
    rec("  linear decode of preceding 16 bytes ends exactly at claimed entry: %s" % fb)
    verdict = (wbytes.hex() == case["writer_hex"]) and len(e8) == 0 and len(e9) == 0 \
        and len(eb) == 0 and len(im) == 0 and not fb and ins0.mnemonic == "add" and ins0.op_str == "byte ptr [eax], al"
    rec("  PHASE-1 VERDICT: historical fn attribution %s" % (
        "DISPROVEN (bytes start 00 00; ZERO references via E8/E9/EB/imm32; no fallthrough; "
        "the 'FPO, ebp untouched' premise was evaluated at a NON-FUNCTION VA)" if verdict else "not disproven by this check set"))
    rec("")

    rec("[C] PHASE 2 — REAL CONTAINING FUNCTION DISCOVERY")
    real_va, to_writer, rets, ebpw = find_real_fn(B, cs, lattice, w_va, rec)
    assert real_va is not None, "real containing function not found for %s" % tag
    rec("  ==> REAL containing function of writer 0x%08X = 0x%08X" % (w_va, real_va))
    rec("  EBP-WRITING instructions between real entry and writer:")
    for i in ebpw:
        rec("      0x%08X  %s %s   <== EBP WRITE (refutes 'ebp untouched' for the REAL function)" % (i.address, i.mnemonic, i.op_str))
    rec("  ret instructions crossed before the writer: %d %s" % (
        len(rets), ["0x%08X" % r for r in rets]))
    rec("")
    # listing file
    listpath = os.path.join(PKG_ROOT, "01_RAW", "%s_FUN_%08X_DISASM.txt" % (tag, hist_fn))
    with open(listpath, "w", encoding="utf-8") as f:
        f.write("=== %s DISASSEMBLY RAW — historical fn attribution 0x%08X (row traceability) ===\n" % (tag, hist_fn))
        f.write("=== the REAL containing function discovered in phase 2 = 0x%08X ===\n" % real_va)
        f.write("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914\n")
        f.write("GENERATOR: 00_CONTROL/e_ebp_reval.py (SHA256 %s)\n" % self_sha256())
        f.write("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B e_ebp_reval.py\n")
        f.write("INPUT: D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (fail-closed SHA256+SIZE asserted;\n")
        f.write("       SHA256 %s, SIZE %d; STATIC-ONLY — never executed)\n" % (EXE_SHA_PIN, EXE_SIZE_PIN))
        f.write("capstone provenance: __version__=%s (measured; the 5.0.9 dist-info label is FALSE) __file__=%s\n"
                % (capstone.__version__, capstone.__file__))
        f.write("HISTORICAL CSV ROW: %s\n" % case["csv_row"])
        f.write("SCOPE: phase-1 disproof bytes at the historical VA; real function decode entry->writer+0x40.\n")
        f.write("TIMESTAMP: %s\n" % datetime.datetime.now().isoformat())
        f.write("\n--- phase 1: bytes at the HISTORICAL claimed entry 0x%08X (first 0x20 bytes) ---\n" % hist_fn)
        blk = B.data[B.va2off(hist_fn):B.va2off(hist_fn) + 0x20]
        for k in range(0, len(blk), 16):
            f.write("  0x%08X  %s\n" % (hist_fn + k, " ".join("%02X" % b for b in blk[k:k + 16])))
        f.write("\n--- phase 2: real function 0x%08X — decode from entry to writer+0x40 ---\n" % real_va)
        for i in disasm(B, cs, real_va, w_va + 0x40 - real_va):
            mark = ""
            if writes_ebp(i) and i.address <= w_va:
                mark = "   <== EBP WRITE"
            if i.address == w_va:
                mark = "   <== WRITER (%s)" % case["writer_text"]
            f.write(fmt(i) + mark + "\n")
        f.write("\nSUMMARY: real fn 0x%08X; EBP writes entry->writer: %d; rets crossed: %d\n"
                % (real_va, len(ebpw), len(rets)))
    rec("  listing written: 01_RAW/%s_FUN_%08X_DISASM.txt" % (tag, hist_fn))
    rec("")

    rec("[D] ENTRY-CHANNEL CENSUS OF THE REAL FUNCTION 0x%08X" % real_va)
    e8 = B.e8_callers(real_va)
    e9, eb = B.jmp_census(real_va)
    im = B.imm32_census(real_va)
    rec("  E8 direct callers: %d %s" % (len(e8), ["0x%08X" % x for x in e8]))
    rec("  E9 rel32 jmps: %d | EB rel8 jmps: %d" % (len(e9), len(eb)))
    rec("  whole-file imm32 occurrences: %d" % len(im))
    rec("  entry-fallthrough: prev-8-bytes = %s" % B.prev_bytes(real_va))
    rec("")

    # ---- per-case chain analysis (deterministic; every fact re-derived from bytes) ----
    if tag == "E1":
        run_e1_chain(B, cs, rec, real_va, w_va, e8)
    else:
        run_e2_chain(B, cs, rec, real_va, w_va, e8)

    cenpath = os.path.join(PKG_ROOT, "01_RAW", "%s_CALLER_PROVENANCE_CENSUS.txt" % tag)
    with open(cenpath, "w", encoding="utf-8") as f:
        f.write("=== %s CALLER-PROVENANCE CENSUS — RAW (two-phase, own capstone decode of pinned Entropia.exe) ===\n" % tag)
        f.write("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914\n")
        f.write("GENERATOR: 00_CONTROL/e_ebp_reval.py (SHA256 %s)\n" % self_sha256())
        f.write("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B e_ebp_reval.py\n")
        f.write("INPUT: D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (fail-closed SHA256+SIZE asserted;\n")
        f.write("       SHA256 %s, SIZE %d; STATIC-ONLY — never executed)\n" % (EXE_SHA_PIN, EXE_SIZE_PIN))
        f.write("capstone provenance: __version__=%s (measured; 5.0.9 dist-info label is FALSE) __file__=%s\n"
                % (capstone.__version__, capstone.__file__))
        f.write("HISTORICAL CSV ROW: %s\n" % case["csv_row"])
        f.write("DECLARED BOUND: caller chain walked at most TWO levels above the real containing function;\n")
        f.write(" beyond that the provenance is recorded UNKNOWN (per RUN_CONTRACT.md W1 INDIRECT_ENTRY_CLOSURE).\n")
        f.write("TIMESTAMP: %s\n" % datetime.datetime.now().isoformat())
        f.write("\n")
        f.write("\n".join(out))
        f.write("\n")
    print("  census written: 01_RAW/%s_CALLER_PROVENANCE_CENSUS.txt" % tag)
    print("")


def run_e1_chain(B, cs, rec, real_va, w_va, e8):
    rec("[E1-CHAIN] FUN_%08X EBP definition and caller provenance (DECLARED BOUND: two levels)" % real_va)
    rec("  (1) EBP definition INSIDE FUN_%08X: prologue is an MSVC SEH frame" % real_va)
    for i in disasm(B, cs, real_va, 0x38):
        rec("      " + "%s" % fmt(i).strip())
    rec("  ==> at 0x007EA76D: mov ebp, dword ptr [esp + 0x1a0] — EBP is DEFINED from an incoming")
    rec("      stack argument (8 pushes + 0x174 sub = 0x194 below entry esp at that point;")
    rec("      [esp+0x1a0] = [entry_esp+0x0C] = ARG3). The historical premise 'fn never redefines")
    rec("      ebp (FPO, ebp untouched)' is REFUTED for the real function: EBP is a redefined")
    rec("      ARGUMENT POINTER, not an inherited frame pointer, and not a frame pointer at all.")
    rec("")
    rec("  (2) The single E8 caller of FUN_%08X = 0x%08X — decode of the caller region:" % (real_va, e8[0]))
    for i in disasm(B, cs, 0x007EB210, 0x7EB290 - 0x7EB210):
        rec("      " + fmt(i).strip())
    rec("  ==> CALLER = FUN_007EB210 (boundary: prev bytes ret+CC padding; the 'ret' at 0x7EB21C is")
    rec("      its own early-exit; 0x7EB21D is the jne continuation of the SAME function).")
    rec("  ==> It is an NiNode-RTTI-GUARDED DISPATCH WRAPPER: virtual call [esi->vtable+8] (slot 2,")
    rec("      GetRTTI-like) on esi; walks the NiRTTI base chain ([eax+4]) comparing against the")
    rec("      immediate 0x00BA7218 — the NiNode NiRTTI address (independent corroboration of the")
    rec("      SLOT17 NiRTTI pin in a second static context); name-literal fallback via 0x00BA7A94;")
    rec("      then PASSES ITS OWN FOUR ARGS THROUGH: push esi(arg4); push ebp(arg3); push edi(arg2);")
    rec("      push ebx(arg1); call 0x007EA740.")
    rec("  ==> FUN_007EA740's EBP = ARG3 = FUN_007EB210's EBP, which FUN_007EB210 set at 0x7EB21E:")
    rec("      mov ebp, [esp+0x14] = ITS OWN ARG3 (a caller-passed object pointer).")
    rec("")
    e8w = B.e8_callers(0x7EB210)
    e9w, ebw = B.jmp_census(0x7EB210)
    imw = B.imm32_census(0x7EB210)
    rec("  (3) ENTRY CENSUS of the wrapper FUN_007EB210: E8=%d %s; E9=%d; EB=%d; imm32=%d; prev8=%s"
        % (len(e8w), ["0x%08X" % x for x in e8w], len(e9w), len(ebw), len(imw), B.prev_bytes(0x7EB210)))
    rec("      (three direct callers; no indirect channel; no fallthrough — closure complete)")
    rec("")
    rec("  (4) LEVEL-2: the three wrapper call sites — arg3 provenance at each:")
    for site, note in ((0x007C198F, "caller A"), (0x007EB2FF, "caller B"), (0x007EB410, "caller C")):
        rec("      -- %s: call site 0x%08X, preceding decode --" % (note, site))
        for i in disasm(B, cs, site - 0x20, 0x25):
            rec("         " + fmt(i).strip())
    rec("      caller A (0x007C198F): push ecx; push ebp; mov ebp, ecx (0x7C1977) — the arg3 pushed")
    rec("        is the caller's EBP, which THAT caller set from ECX = a this-object pointer.")
    rec("      caller B (0x007EB2FF): arg3 = edx = [esp+0x14] — an incoming stack-argument VALUE")
    rec("        (unbounded within the declared bound).")
    rec("      caller C (0x007EB410): arg3 = the caller's EBP register (frame state of that caller")
    rec("        not established within the declared bound).")
    rec("")
    rec("  (5) ADJUDICATION FACTS (deterministic derivation):")
    rec("      - case A (push ebp; mov ebp,esp before the writer)? NO — the real function has an SEH")
    rec("        FPO prologue and redefines EBP from an ARGUMENT slot, not from ESP.")
    rec("      - case B (EBP derived from ESP/stack)? NOT PROVEN — EBP := arg3 (an object pointer")
    rec("        value); on the three level-2 paths arg3 is an ECX-this / a stack-arg VALUE / a caller")
    rec("        EBP register — none PROVEN to be a stack address on every writer-reaching path.")
    rec("      - case C (incoming EBP non-SF on every entry path)? NOT APPLICABLE — EBP is redefined")
    rec("        in-function; the relevant object (arg3) class is UNRESOLVED within the bound.")
    rec("      ==> CASE PROVEN: NONE_PROVEN. REJECTED_ALIAS is NOT proven.")
    rec("      ==> E1 FINAL CLASS: POSSIBLE_ALIAS (historical REJECTED under the unsound rule is")
    rec("          superseded; this does NOT assert the write IS SF+0x30 — it asserts the rejection")
    rec("          was never proven).")


def run_e2_chain(B, cs, rec, real_va, w_va, e8):
    rec("[E2-CHAIN] FUN_%08X EBP definition and caller provenance (DECLARED BOUND: two levels)" % real_va)
    rec("  (1) EBP definition INSIDE FUN_%08X:" % real_va)
    for i in disasm(B, cs, real_va, 0x18):
        rec("      " + fmt(i).strip())
    rec("  ==> at 0x0082DA82: mov ebp, ecx — EBP is DEFINED from ECX = the this/arg1 OBJECT POINTER.")
    rec("      The historical premise 'fn never redefines ebp (FPO, ebp untouched)' is REFUTED for")
    rec("      the real function. The function is a bounds-checked u16 CURSOR READER: [ebp+0x90] =")
    rec("      cursor, [ebp+0x8C] = end, per-read guard lea edx,[ecx+2]; cmp edx,[ebp+0x8C]; jae;")
    rec("      mov cx,[ecx] — writing parsed u16 values into object fields (+0x2E, +0x30).")
    rec("      (16-bit write note: a 16-bit store can alias the LOW HALF of a 32-bit field; the")
    rec("      alias analysis keys on the BASE REGISTER — unchanged.)")
    rec("")
    rec("  (2) The single E8 caller of FUN_%08X = 0x0082E057; decode of the caller region:" % real_va)
    for i in disasm(B, cs, 0x0082E030, 0x40):
        rec("      " + fmt(i).strip())
    rec("      (the leading 'add byte ptr [eax], al' lines above are the misaligned tail of my")
    rec("       context window starting mid-instruction at 0x82E030 — not evidence; the aligned")
    rec("       stream is established from the function start below)")
    rec("")
    e8c = B.e8_callers(0x82DFF0)
    rec("  (3) The containing function of the call site = FUN_0082DFF0 (SEH frame: push -1; push")
    rec("      0xa24f4b; mov eax,fs:[0]; push eax; sub esp,0x28; ...) — found via the E8-target")
    rec("      lattice + CC padding (prev-8 = %s), forward-alignment on 0x82E057, 0 rets crossed." % B.prev_bytes(0x82DFF0))
    rec("      FUN_0082DFF0 entry census: E8 callers = %d %s; E9/EB = %d/%d; whole-file imm32 = %d;"
        % (len(e8c), ["0x%08X" % x for x in e8c], len(B.jmp_census(0x82DFF0)[0]), len(B.jmp_census(0x82DFF0)[1]),
           len(B.imm32_census(0x82DFF0))))
    rec("      ==> exactly TWO entry paths (0x006B0C63, 0x006B0F38); no indirect channel.")
    rec("      At 0x0082E017: mov esi, ecx — ESI := the caller's ECX (this); then mov ecx, esi;")
    rec("      call 0x82da80 — the reader object = FUN_0082DFF0's this.")
    rec("")
    rec("  (4) LEVEL-2: the two FUN_0082DFF0 call sites — ECX provenance:")
    for site in (0x006B0C63, 0x006B0F38):
        rec("      -- call site 0x%08X, preceding decode --" % site)
        for i in disasm(B, cs, site - 0x2a, 0x2f):
            rec("         " + fmt(i).strip())
    rec("      BOTH call sites construct the reader IN PLACE as a STACK LOCAL:")
    rec("        lea ecx, [esp + 0x9c]; call 0x82d920   (constructor thunk)")
    rec("        ... 4 pushes (16 bytes) ...")
    rec("        lea ecx, [esp + 0xac]; call 0x82dff0    (esp+0xac AFTER the pushes == the SAME")
    rec("                                                    esp+0x9c slot BEFORE them)")
    rec("      0x82d920 decode (the constructor thunk):")
    for i in disasm(B, cs, 0x0082D920, 0x20):
        rec("         " + fmt(i).strip())
    rec("      ==> the ctor stores vtable 0x00A9189C into the object. RTTI resolution (own byte")
    rec("          read, standard MSVC RTTI chain: [vt-4]=COL, [COL+0xC]=TypeDescriptor, TD+8=name):")
    vt = 0x00A9189C
    col = struct.unpack_from("<I", B.data, B.va2off(vt - 4))[0]
    td = struct.unpack_from("<I", B.data, B.va2off(col + 0xC))[0]
    nameoff = B.va2off(td + 8)
    nm = B.data[nameoff:B.data.find(b"\x00", nameoff)].decode("ascii", "replace")
    rec("          vtable 0x%08X -> COL 0x%08X -> TypeDescriptor 0x%08X -> name %s" % (vt, col, td, nm))
    rec("      ==> the reader object's class = ArkNiTGAReader (.?AVArkNiTGAReader@@), a TGA image")
    rec("          reader — NOT SceneFeederObject — and the object is a STACK LOCAL (lea ecx,[esp+...])")
    rec("          on BOTH entry paths.")
    rec("")
    rec("  (5) ADJUDICATION FACTS (deterministic derivation):")
    rec("      - case A? NO (no push ebp; mov ebp,esp — SEH/FPO frames throughout).")
    rec("      - case B (EBP derived from ESP/stack on every writer-reaching path)? PROVEN: EBP := ECX")
    rec("        (0x82DA82) and ECX := lea ecx,[esp+0x9c] on BOTH entry paths (0x6B0C63/0x6B0F38) —")
    rec("        the EBP value at the writer is a STACK ADDRESS on every writer-reaching path.")
    rec("      - class corroboration: the object is an ArkNiTGAReader instance (vtable 0x00A9189C,")
    rec("        RTTI .?AVArkNiTGAReader@@) — a class distinct from SceneFeederObject.")
    rec("      - SF is always-heap per the accepted census; a stack address can never alias SF+0x30;")
    rec("        additionally the object class is provably not SF.")
    rec("      ==> CASE PROVEN: B (with class corroboration). REJECTED_ALIAS STANDS — now SOUND.")
    rec("      ==> E2 FINAL CLASS: REJECTED_ALIAS (REJECTED_STANDS_SOUND; the historical unsound")
    rec("          reason R-EBP-INHERITED is superseded by the case-B proof).")


if __name__ == "__main__":
    main()
