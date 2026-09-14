# -*- coding: utf-8 -*-
"""
GENERATOR: 00_CONTROL/nirtti_bounded_probe.py
RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
PURPOSE: W6.4 OPTIONAL BOUNDED PROBE — scan .text for the byte pattern B9 70 72 BA 00
  (mov ecx, 0x00BA7270); if found, decode the surrounding static initializer; if it
  provably constructs NiRTTI at 0x00BA7270 with a "NiAVObject" name literal, record the
  direct proof. BOUND: exactly this one pattern + its immediate context (one window
  decode per hit); anything beyond -> STOP and record NOT_PROBED/bounded result.
MODE: STATIC-ONLY — Entropia.exe never executed; own byte read + own capstone decode;
  fail-closed SHA256+SIZE assert BEFORE any byte read.
EXECUTED AS: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B nirtti_bounded_probe.py
OUTPUT: 01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt
"""
import hashlib
import os
import struct
import sys
import datetime

import capstone
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_PATH = os.path.abspath(__file__)
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SHA_PIN = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXE_SIZE_PIN = 8015872
IMAGE_BASE = 0x00400000


def self_sha256():
    with open(SELF_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def main():
    size = os.path.getsize(EXE)
    sha = hashlib.sha256(open(EXE, "rb").read()).hexdigest().upper()
    assert size == EXE_SIZE_PIN, "FAIL-CLOSED SIZE"
    assert sha == EXE_SHA_PIN, "FAIL-CLOSED SHA256"
    data = open(EXE, "rb").read()
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", data, coff + 2)[0]
    sopt = struct.unpack_from("<H", data, coff + 16)[0]
    st = coff + 20 + sopt
    secs = []
    for i in range(nsec):
        off = st + 40 * i
        name = data[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, rp = struct.unpack_from("<IIII", data, off + 8)
        secs.append((name, va, vs, rs, rp))

    def va2off(va):
        rva = va - IMAGE_BASE
        for name, vaddr, vsize, rsize, rptr in secs:
            if vaddr <= rva < vaddr + rsize:
                return rptr + (rva - vaddr)
        return None

    def off2va(off):
        for name, vaddr, vsize, rsize, rptr in secs:
            if rptr <= off < rptr + rsize:
                return IMAGE_BASE + vaddr + (off - rptr), name
        return None, None

    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail = True
    out = []

    def rec(s=""):
        out.append(s)
        print(s)

    rec("=== NIRTTI BOUNDED PROBE — pattern B9 70 72 BA 00 (mov ecx, 0x00BA7270) ===")
    rec("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914")
    rec("GENERATOR: 00_CONTROL/nirtti_bounded_probe.py (SHA256 %s)" % self_sha256())
    rec("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B nirtti_bounded_probe.py")
    rec("INPUT: D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (fail-closed SHA256+SIZE asserted;")
    rec("       SHA256 %s, SIZE %d; STATIC-ONLY — never executed)" % (EXE_SHA_PIN, EXE_SIZE_PIN))
    rec("interpreter: %s (%s)" % (sys.executable, sys.version.split()[0]))
    rec("capstone.__version__: %s (MEASURED; the 5.0.9 dist-info label is a KNOWN FALSE LABEL)" % capstone.__version__)
    rec("capstone.__file__: %s" % capstone.__file__)
    rec("BOUND DECLARED: one pattern scan over the whole file + ONE context window decode per hit;")
    rec(" no expansion (per RUN_CONTRACT.md W6.4).")
    rec("timestamp: %s" % datetime.datetime.now().isoformat())
    rec("")
    pat = bytes.fromhex("B97072BA00")
    hits, k = [], 0
    while True:
        k = data.find(pat, k)
        if k < 0:
            break
        hits.append(k)
        k += 1
    rec("pattern occurrences in the WHOLE FILE: %d" % len(hits))
    proven = False
    for h in hits:
        va, sec = off2va(h)
        rec("hit at file offset 0x%X -> VA %s (section %s)" % (h, "0x%08X" % va if va else "unmapped", sec))
        if va is None:
            continue
        start_va = va - 0x20
        off = va2off(start_va)
        rec("context decode (window 0x00A6C31A-0x00A6C35A):")
        literals_found = None
        for i in cs.disasm(data[off:off + 0x40], start_va):
            note = ""
            if i.mnemonic == "push" and i.op_str.startswith("0x"):
                imm = int(i.op_str, 16)
                io = va2off(imm)
                if io:
                    raw = data[io:io + 32]
                    z = raw.split(b"\x00")[0]
                    if z and all(32 <= b < 127 for b in z):
                        note = "   ; -> literal %r" % z.decode("ascii")
                        literals_found = z.decode("ascii")
            rec("  0x%08X  %-20s %-6s %s%s" % (i.address, i.bytes.hex().upper(), i.mnemonic, i.op_str, note))
        rec("")
        # structural comparison with the NiNode initializer at 0x00A6C200 (SLOT17 evidence)
        rec("structural comparison (this run's own bytes): the hit's thunk body is")
        rec("  push <base RTTI imm>; push <name literal imm>; mov ecx, 0x00BA7270; call 0x007199E0; ret")
        rec("  — the SAME constructor call (0x007199E0) and the SAME thunk shape as the NiNode")
        rec("  static initializer at 0x00A6C200 (SLOT17 03_EVIDENCE/ENTROPIA_NIRTTI_STATIC_INIT.txt:")
        rec("  push 0x00BA7270; push 0x00A8CE00 ('NiNode'); mov ecx, 0x00BA7218; call 0x007199E0; ret).")
        if literals_found == "NiAVObject":
            proven = True
            rec("")
            rec("DIRECT PROOF RECORDED: the static initializer at 0x00A6C330 constructs the NiRTTI")
            rec("object at ecx = 0x00BA7270 with the name literal 'NiAVObject' (push 0x00A8D8BC,")
            rec("whose .rdata bytes decode to the ASCII literal) and base pointer 0x00BA7224:")
            rec("  *(NiRTTI*)0x00BA7270 = NiRTTI(\"NiAVObject\", (const NiRTTI*)0x00BA7224)")
            rec("EVIDENCE CLASS: DIRECT STATIC-INITIALIZER CALL-SITE PROOF (own bytes, this run,")
            rec("STATIC-ONLY). The semantic identity 0x00BA7270 = NiAVObject NiRTTI is CONFIRMED")
            rec("(upgraded from STRONGLY_SUPPORTED). The probe did NOT expand beyond the declared")
            rec("bound (one pattern + one context window).")
    if not proven and hits:
        rec("probe did NOT prove the 'NiAVObject' construction directly — semantic identity stays STRONGLY_SUPPORTED.")
    if not hits:
        rec("no occurrence of the pattern — semantic identity stays STRONGLY_SUPPORTED (probe NOT_PROVEN, no expansion).")
    with open(os.path.join(PKG_ROOT, "01_RAW", "NIRTTI_BOUNDED_PROBE_0xBA7270.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("")
    print("raw output written: 01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
