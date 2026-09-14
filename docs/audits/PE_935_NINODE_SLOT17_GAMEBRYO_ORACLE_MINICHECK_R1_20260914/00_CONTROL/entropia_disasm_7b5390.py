#!/usr/bin/env python3
r"""entropia_disasm_7b5390.py -- Deterministic capstone disassembly of
Entropia.exe (PCG 9.3.5) function 0x007B5390 (NiNode primary vtable
0x00A8CCF4 slot 17 / +0x44), for the
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1 audit.

Physical target (fail-closed pin, verified by caller):
  D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  SIZE 8015872
  IMAGE_BASE 0x00400000, file_offset == RVA for all sections (verified by
  entropia_rtti_probe.py section table), so VA 0x007B5390 -> file 0x3B5390.

Behavior: linear sweep from FUNC_START. Stops at the first RET/CDET-family
instruction that is followed by padding (0xCC) or another prologue preceded by
padding, bounded by MAX_BYTES. Emits:
  - address, raw bytes (hex), mnemonic, operands
  - call/jmp targets resolved to VA
  - boundary context: 16 bytes before FUNC_START and after the end, so the
    auditor can verify the function start is a real boundary.

Pure capstone 5.x (measured 5.0.7 on this host) + stdlib. Deterministic.
"""
import argparse
import hashlib
import json
import sys

import capstone

ENTROPIA = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
IMAGE_BASE = 0x00400000
FUNC_VA = 0x007B5390
TEXT_RVA_LO = 0x1000
TEXT_RVA_HI = 0x6745E5  # exclusive end
MAX_BYTES = 0x800

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = False


def va_to_off(va):
    rva = va - IMAGE_BASE
    if TEXT_RVA_LO <= rva < TEXT_RVA_HI:
        return rva  # raw == rva in this binary (verified in probe)
    return None


def is_padding(d, off, n):
    """True if n bytes at off are all 0xCC (int3) or 0x90 (nop) padding."""
    seg = d[off:off + n]
    return len(seg) == n and all(b in (0xCC, 0x90) for b in seg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="0x007B5390")
    ap.add_argument("--max", type=str, default=None,
                    help="hex byte cap override, e.g. 0x100")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    start_va = int(args.start, 16)
    max_bytes = int(args.max, 16) if args.max else MAX_BYTES

    with open(ENTROPIA, "rb") as f:
        d = f.read()
    sha = hashlib.sha256(d).hexdigest().upper()
    if sha != EXPECT_SHA256:
        sys.stderr.write("SHA256 MISMATCH: %s -- fail closed\n" % sha)
        sys.exit(1)

    off = va_to_off(start_va)
    if off is None:
        sys.stderr.write("start VA not in .text\n")
        sys.exit(1)

    lines = []
    lines.append("TARGET: %s" % ENTROPIA)
    lines.append("SHA256: %s (PIN OK)" % sha)
    lines.append("IMAGE_BASE: 0x%08X  file_offset==RVA (probe-verified)" % IMAGE_BASE)
    lines.append("FUNC_VA: 0x%08X  file_off: 0x%X" % (start_va, off))
    pre = d[off - 16:off]
    lines.append("CONTEXT_PRE_16: %s" % pre.hex(" "))
    lines.append("")

    end_off = None
    code = d[off:off + max_bytes]
    for ins in md.disasm(code, start_va):
        raw = " ".join("%02X" % b for b in ins.bytes)
        lines.append("%08X  %-23s %-8s %s" % (ins.address, raw, ins.mnemonic,
                                              ins.op_str))
        # stop condition: RET that is followed by >=2 padding bytes or a
        # tight function boundary (ret + 0xCC)
        nxt = off + (ins.address - start_va) + ins.size
        if ins.mnemonic in ("ret", "retn") and is_padding(d, nxt, 2):
            end_off = nxt
            lines.append("")
            post = d[end_off:end_off + 16]
            lines.append("CONTEXT_POST_END(0x%08X)_16: %s" % (end_off, post.hex(" ")))
            break
    if end_off is None:
        lines.append("(no ret+padding boundary within cap)")

    text = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as g:
            g.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
