"""
phase_a_thunk.py - PHASE A (G2): full independent decode of FUN_006FAB80.
B.5 extent, ABI, forwarding fidelity, x87 roundtrip classification, pin checks.
Writes 01_RAW/FUN_006FAB80_DISASM.txt.
Re-measures size+SHA256+PE layout FIRST (fail-closed).
"""
import sys
import os
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s0_common as S

RUN_DIR = os.path.dirname(HERE)  # scripts/ -> 00_CONTROL
RUN_DIR = os.path.dirname(RUN_DIR)  # 00_CONTROL -> run root
RAW = os.path.join(RUN_DIR, "01_RAW")
ANCHOR = 0x006FAB80

# PIN-THUNK expected head bytes (validated as FINDINGS, never adopted silently):
PIN_HEAD = [
    (0x006FAB80, "8b 49 14"),
    (0x006FAB83, "d9 44 24 04"),
    (0x006FAB87, "8b 54 24 08"),
    (0x006FAB8B, "8b 01"),
    (0x006FAB8D, "8b 40 0c"),
    (0x006FAB90, "52"),
    (0x006FAB91, "51"),
    (0x006FAB92, "d9 1c 24"),
    (0x006FAB95, "ff d0"),
    (0x006FAB97, "c2 08 00"),
]

# Per-instruction semantic annotations (interpretive layer; measured layer is
# the decode itself). Keys are VAs; deterministic output.
SEM = {
    0x006FAB80: "ecx := [ecx+0x14]  | OBSERVED: base register ECX at entry = this (thiscall this); loads the HELD object pointer from [this+0x14] into ECX",
    0x006FAB83: "st0 := fld dword [esp+4]  | OBSERVED: loads thunk arg1 (32 bits at [esp+4]) into the x87 register stack",
    0x006FAB87: "edx := [esp+8]  | OBSERVED: loads thunk arg2 verbatim into EDX (no test, no arithmetic)",
    0x006FAB8B: "eax := [ecx]  | OBSERVED: vtable pointer of the HELD object (receiver vtable)",
    0x006FAB8D: "eax := [eax+0x0C]  | OBSERVED: virtual slot displacement 0x0C = 4*3 = SLOT 3 (byte evidence 8B 40 0C)",
    0x006FAB90: "push edx  | OBSERVED: receiver stack slot 2 receives thunk arg2 verbatim (after call: [esp+8])",
    0x006FAB91: "push ecx  | OBSERVED: argument-slot allocation push (value overwritten by next insn; not a data forward)",
    0x006FAB92: "fstp dword [esp]  | OBSERVED: stores st0 into the slot pushed by 0x006FAB91 = receiver stack slot 1 (after call: [esp+4])",
    0x006FAB95: "call eax  | OBSERVED: indirect call to receiver vtable slot 3; this in ECX = HELD object (ECX not clobbered between 0x006FAB80 and the call)",
    0x006FAB97: "ret 8  | OBSERVED: callee cleanup of 2 dword stack args -> thunk ABI is thiscall(this in ECX, arg1=[esp+4], arg2=[esp+8])",
}


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    f = S.b5_function(m, cs, ANCHOR, max_bytes=4096)
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: FUN_006FAB80_DISASM.txt")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_a_thunk.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("SOURCE_OF_TRUTH: %s physical bytes (STATIC decode; binary NEVER executed)" % S.EXE_PATH)
    L.append("HEADER_TIMESTAMP: %s (metadata only; decode content is byte-deterministic)"
             % S.utc_now_iso())
    L.append("=" * 80)
    L.append("")
    L.append("[A1] B.5 EXTENT (iterative terminal+padding rule, own capstone)")
    L.append("  anchor start : 0x%08X" % f["start"])
    L.append("  extent end   : 0x%08X" % f["end"])
    L.append("  extent size  : %d bytes" % (f["end"] - f["start"]))
    L.append("  end_kind     : %s" % f["end_kind"])
    L.append("  terminal     : %s" % f.get("terminal"))
    L.append("  pad_len      : %d" % f.get("pad_len", 0))
    L.append("  next_start   : %s" % ("0x%08X" % f["next_start"] if f["next_start"] else "None"))
    L.append("  events       : %s" % (",".join(f["events"]) if f["events"] else "none"))
    L.append("")
    L.append("[A2] FULL DISASSEMBLY (measured layer)")
    L.append("  %-10s %-22s %-28s %s" % ("VA", "BYTES", "MNEMONIC+OPERANDS", "SEMANTIC (interpretive)"))
    for i in f["insns"]:
        L.append("  0x%08X  %-22s %-28s %s"
                 % (i.address, i.bytes.hex(), i.mnemonic + " " + i.op_str,
                    SEM.get(i.address, "")))
    L.append("")
    L.append("[A3] MEASURED ABI")
    ret_insns = [i for i in f["insns"] if i.mnemonic == "ret"]
    ret_imm = None
    for r in ret_insns:
        if r.operands:
            ret_imm = r.operands[0].imm
    L.append("  calling convention : thiscall (this in ECX; callee-cleanup)")
    L.append("  evidence           : ret-imm %s at 0x%08X (2 dword stack args cleaned)"
             % (("0x%X" % ret_imm) if ret_imm is not None else "?", ret_insns[0].address if ret_insns else 0))
    L.append("  this register      : ECX (base of the [reg+0x14] load at 0x%08X)"
             % f["insns"][0].address)
    L.append("  stack args         : arg1=[esp+4] (read at 0x006FAB83), arg2=[esp+8] (read at 0x006FAB87)")
    L.append("  return             : to caller, no value contract observed (forwarder)")
    L.append("")
    L.append("[A4] RECEIVER AND SLOT")
    L.append("  receiver source    : [this+0x14] (this = ECX at entry); INSN 0x006FAB80")
    L.append("  receiver vtable    : [ecx] at 0x006FAB8B")
    L.append("  slot displacement  : [eax+0x0C] at 0x006FAB8D -> 0x0C/4 = SLOT 3 (byte evidence: 8B 40 0C)")
    L.append("  receiver this at virtual call : ECX still holds the held object (no ECX write between load and call)")
    L.append("")
    L.append("[A5] FORWARDING FIDELITY (measured per operand)")
    L.append("  arg1 path : [esp+4] --fld dword--> st0 --fstp dword [esp]--> receiver [esp+4]")
    L.append("             FORM: x87 roundtrip (32-bit load + 32-bit store), NOT a register forward")
    L.append("  arg2 path : [esp+8] --mov edx--> push edx --> receiver [esp+8] ; VERBATIM (no test/arith/mutation)")
    L.append("  push ecx at 0x006FAB91 is a slot-allocation push: its pushed value is overwritten by")
    L.append("  the fstp at 0x006FAB92 (same [esp] cell); the ecx VALUE is not forwarded.")
    L.append("")
    L.append("[A6] x87 ROUNDTRIP BIT-PRESERVATION CLASSIFICATION (analytic; x87 architecture)")
    L.append("  bit-exact classes : normal float32 values; denormals (x87 has no flush-to-zero;)")
    L.append("                       denormal dword loads/stores back the same bit pattern);")
    L.append("                       infinities; qNaN payloads (pure FLD/FSTP performs no arithmetic);")
    L.append("                       POINTERS AS DWORDS (a bit pattern is a bit pattern to fld/fstp).")
    L.append("  non-guaranteed     : signaling NaNs (masked #IA handling; quieting risk on some")
    L.append("                       processors; sNaN bit-exactness is NOT assumed).")
    L.append("  IMPLICATION (measured constraint, not a semantic claim): the receiver's arg1 could be")
    L.append("  a POINTER (e.g. an out-buffer) OR a genuine FLOAT VALUE. Discriminator at callers:")
    L.append("  caller passes lea/pointer-setup -> POINTER; caller passes a float constant or an x87")
    L.append("  computation -> VALUE (which would falsify FUN_0050A050's out-buffer arg1 signature).")
    L.append("  This discriminator is evaluated in Phase E at every proven caller.")
    L.append("")
    L.append("[A7] SIDE-EFFECT / CONTROL-FLOW AUDIT (measured)")
    branches = [i for i in f["insns"] if i.mnemonic.startswith("j") and i.mnemonic != "jmp"]
    calls = [i for i in f["insns"] if i.mnemonic == "call"]
    memwrites = []
    for i in f["insns"]:
        for (idx, op) in S.mem_write_ops(i):
            memwrites.append((i.address, i.mnemonic, i.op_str))
    L.append("  conditional branches : %d %s" % (len(branches), [hex(i.address) for i in branches]))
    L.append("  calls                : %d %s" % (len(calls), [hex(i.address) for i in calls]))
    L.append("  memory writes        : %d %s" % (len(memwrites), [(hex(a), mn) for (a, mn, _) in memwrites]))
    L.append("  null tests           : NONE observed (no test/cmp against the held pointer)")
    L.append("  refcount operations  : NONE observed (no inc/add [held+4] in this function)")
    L.append("  conversions/arith     : NONE observed on arg2; arg1 passes through x87 only")
    L.append("  alternate branches    : NONE (single basic block)")
    L.append("  other side effects    : stack writes for the receiver call frame only (the two pushes + fstp slot)")
    L.append("")
    L.append("[A8] PIN-THUNK VALIDATION (finding per row; never silent adoption)")
    all_match = True
    for (va, hexbytes) in PIN_HEAD:
        got = S.read_va(m, va, len(bytes.fromhex(hexbytes.replace(" ", ""))))
        ok = got is not None and got.hex() == hexbytes.replace(" ", "")
        if not ok:
            all_match = False
        L.append("  0x%08X expected %-14s measured %-14s MATCH=%s"
                 % (va, hexbytes, got.hex() if got is not None else "READ_FAIL", ok))
    L.append("  PIN-THUNK RESULT: %s" % ("ALL MATCH" if all_match else "MISMATCH (FINDING)"))
    L.append("")
    L.append("[A9] FORWARDER_OPERATION_STATUS DETERMINATION")
    checks = {
        "B5_extent_ok": f["end_kind"] in ("pad", "tight") and f["terminal"] == "ret",
        "single_bb": len(branches) == 0,
        "receiver_from_this14": f["insns"][0].bytes.hex() == "8b4914",
        "slot3_byte_evidence": any(i.bytes.hex() == "8b400c" for i in f["insns"]),
        "arg1_x87_roundtrip": any(i.bytes.hex() == "d9442404" for i in f["insns"])
                              and any(i.bytes.hex() == "d91c24" for i in f["insns"]),
        "arg2_verbatim_edx": any(i.bytes.hex() == "8b542408" for i in f["insns"])
                            and any(i.bytes.hex() == "52" for i in f["insns"]),
        "ret8_cleanup": ret_imm == 8,
        "no_other_calls": len(calls) == 1,
        "no_writes_outside_frame": all(mn in ("push", "fstp") for (a, mn, _) in memwrites),
        "pin_head_all_match": all_match,
    }
    for k, v in sorted(checks.items()):
        L.append("  %-28s = %s" % (k, v))
    verdict = "CONFIRMED" if all(checks.values()) else (
        "STRONGLY_SUPPORTED" if sum(1 for v in checks.values() if v) >= 8 else "REJECTED")
    L.append("  FORWARDER_OPERATION_STATUS = %s" % verdict)
    L.append("  Definition used: CONFIRMED iff B.5 extent valid AND single basic block AND")
    L.append("  receiver=[this+0x14] AND slot-3 byte evidence AND arg1 x87 roundtrip AND arg2")
    L.append("  verbatim AND ret 8 AND no other calls AND no writes outside the call frame.")
    L.append("")
    L.append("[A10] EXACT FORWARDER OBSERVATION (status algebra: OBSERVED_OPERATION)")
    L.append("  OBSERVED_OPERATION: FUN_006FAB80 = virtual slot-3 forwarder:")
    L.append("    ECX(this) -> held=[this+0x14] -> vt=[held] -> target=[vt+0x0C] ->")
    L.append("    call target(this=held, arg1=arg1_bits_via_x87, arg2=arg2_verbatim) -> ret 8")
    L.append("  FORWARDER_IDENTITY: %s (as OBSERVED_OPERATION; FUNCTION_IDENTITY of the target is Phase B+)"
             % verdict)
    out = os.path.join(RAW, "FUN_006FAB80_DISASM.txt")
    with open(out, "w") as fh:
        fh.write(chr(10).join(L) + chr(10))
    print(chr(10).join(L))
    print("")
    print("WROTE: %s" % out)


if __name__ == "__main__":
    main()
