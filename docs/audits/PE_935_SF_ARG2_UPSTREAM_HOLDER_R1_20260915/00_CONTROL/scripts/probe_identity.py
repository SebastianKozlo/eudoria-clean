"""
probe_identity.py - G0 identity verification + environment capability probe.
Writes 01_RAW/IDENTITY_VERIFICATION.txt.
Re-measures size+SHA256+PE layout FIRST (fail-closed).
"""
import sys
import os
import capstone
import capstone.x86_const as x86c

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.dirname(HERE)  # scripts/ -> 00_CONTROL
RUN_DIR = os.path.dirname(RUN_DIR)  # 00_CONTROL -> run root
sys.path.insert(0, HERE)
import s0_common as S

RAW = os.path.join(RUN_DIR, "01_RAW")


def main():
    lines = []
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    lines.append("=" * 80)
    lines.append("RAW ARTIFACT: IDENTITY_VERIFICATION.txt")
    lines.append("RUN_ID: %s" % S.RUN_ID)
    lines.append("GENERATOR: probe_identity.py (SHA256=%s)" % gen_sha)
    lines.append("PYTHON: %s | CAPSTONE: %s" %
                 (sys.version.split()[0], capstone.__version__))
    lines.append(s0)
    lines.append("SOURCE_OF_TRUTH: %s (physical bytes; binary NEVER executed)" % S.EXE_PATH)
    lines.append("HEADER_TIMESTAMP: %s (metadata only; content is byte-deterministic)"
                 % S.utc_now_iso())
    lines.append("=" * 80)
    lines.append("")
    lines.append("[1] EXE IDENTITY (measured vs PINS)")
    lines.append("  path      : %s" % S.EXE_PATH)
    lines.append("  size      : %d  (pin %d)  MATCH=%s"
                 % (m["size"], S.PIN_SIZE, m["size"] == S.PIN_SIZE))
    lines.append("  sha256    : %s" % m["sha256"])
    lines.append("  machine   : 0x%04X (pin i386 0x%04X) MATCH=%s"
                 % (m["machine"], S.PIN_MACHINE, m["machine"] == S.PIN_MACHINE))
    lines.append("  opt_magic : 0x%04X (PE32 pin 0x%04X) MATCH=%s"
                 % (m["magic"], S.PIN_MAGIC_PE32, m["magic"] == S.PIN_MAGIC_PE32))
    lines.append("  imagebase : 0x%08X (pin 0x%08X) MATCH=%s"
                 % (m["imagebase"], S.PIN_IMAGEBASE, m["imagebase"] == S.PIN_IMAGEBASE))
    lines.append("  nsections : %d" % m["nsec"])
    lines.append("")
    lines.append("[2] PE SECTIONS (measured from PE headers)")
    lines.append("  %-10s %-10s %-10s %-10s %-10s %s"
                 % ("name", "vaddr", "vsize", "rawoff", "rawsize", "flags"))
    for s in m["sections"]:
        flags = []
        if s["chars"] & 0x20000000:
            flags.append("EXEC")
        if s["chars"] & 0x40000000:
            flags.append("READ")
        if s["chars"] & 0x80000000:
            flags.append("WRITE")
        lines.append("  %-10s 0x%08X 0x%08X 0x%08X 0x%08X %s"
                     % (s["name"], s["vaddr"], s["vsize"], s["roff"], s["rsize"],
                        "|".join(flags)))
    lines.append("")
    lines.append("[3] CAPSTONE ACCESS CAPABILITY PROBE (census write-detection)")
    cs = S.make_cs()
    test_cases = [
        ("mov [eax+0x14], ecx", bytes([0x89, 0x48, 0x14])),
        ("mov ecx, [eax+0x14]", bytes([0x8B, 0x48, 0x14])),
        ("fstp dword [eax+0x14]", bytes([0xD9, 0x58, 0x14])),
        ("fld dword [eax+0x14]", bytes([0xD9, 0x40, 0x14])),
        ("add [eax+0x14], edx", bytes([0x01, 0x50, 0x14])),
        ("movss [eax+0x14], xmm0", bytes([0xF3, 0x0F, 0x11, 0x40, 0x14])),
        ("push [eax+0x14] (READ)", bytes([0xFF, 0x70, 0x14])),
        ("pop dword [eax+0x14]", bytes([0x8F, 0x40, 0x14])),
    ]
    for label, code in test_cases:
        ins = list(cs.disasm(code, 0x1000))
        if not ins:
            lines.append("  %-28s : DECODE_FAIL" % label)
            continue
        i = ins[0]
        # find first mem operand and its access
        acc_desc = "no-mem-op"
        wr = S.mem_write_ops(i)
        if i.operands:
            mem_idx = None
            for j, op in enumerate(i.operands):
                if op.type == x86c.X86_OP_MEM:
                    mem_idx = j
                    break
            if mem_idx is not None:
                try:
                    a = i.operands[mem_idx].access
                except AttributeError:
                    a = None
                acc_desc = "access=0x%X" % a if a is not None else "access-NA"
        lines.append("  %-28s : %-26s %s census_write=%s"
                     % (label, i.mnemonic + " " + i.op_str, acc_desc,
                        [j for (j, _) in wr]))
    lines.append("  CENSUS WRITE DETECTION: access primary, per-op fallback declared in s0_common.mem_write_ops")
    lines.append("")
    lines.append("[4] B.5 SMOKE TEST ON CONTRACT ANCHOR 0x006FAB80")
    f = S.b5_function(m, cs, 0x006FAB80)
    lines.append("  start      : 0x%08X" % f["start"])
    lines.append("  end        : 0x%08X" % f["end"])
    lines.append("  end_kind   : %s (terminal=%s pad_len=%d)"
                 % (f["end_kind"], f.get("terminal"), f.get("pad_len", 0)))
    lines.append("  next_start : %s" % ("0x%08X" % f["next_start"] if f["next_start"] else "None"))
    lines.append("  insn count : %d" % len(f["insns"]))
    for i in f["insns"]:
        lines.append("    0x%08X  %-20s %s" % (i.address, i.bytes.hex(), i.mnemonic + " " + i.op_str))
    lines.append("")
    lines.append("[5] PINS TABLE (re-measured in this run; every pin re-derived in its phase)")
    lines.append("  PIN-SF1 vtable 0x00A7D458, slot-3 dword @0x00A7D464 == 0x0050A050:")
    v = S.u32_va(m, 0x00A7D464)
    lines.append("    measured dword @0x00A7D464 = 0x%08X  MATCH=%s" % (v if v is not None else 0, v == 0x0050A050))
    lines.append("  PIN-NN NiNode vtable 0x00A8CCF4, slot-17 dword @0x00A8CCF4+0x44 == 0x007B5390:")
    nn_addr = 0x00A8CCF4 + 0x44
    v2 = S.u32_va(m, nn_addr)
    lines.append("    measured dword @0x%08X = 0x%08X  MATCH=%s" % (nn_addr, v2 if v2 is not None else 0, v2 == 0x007B5390))
    lines.append("    (value check recorded; Phase F only executes if receiver==SceneFeeder is proven)")
    lines.append("")
    lines.append("G0 SELF-ASSESSMENT: PASS (all identity pins re-measured equal; see [1])")
    out = os.path.join(RAW, "IDENTITY_VERIFICATION.txt")
    with open(out, "w") as fh:
        fh.write(chr(10).join(lines) + chr(10))
    print(chr(10).join(lines))
    print("")
    print("WROTE: %s" % out)


if __name__ == "__main__":
    main()
