# -*- coding: utf-8 -*-
"""
GENERATOR: 00_CONTROL/ebp_alias_classifier.py
RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
PURPOSE: W3 â€” the deterministic checker implementing EBP CLASSIFIER RULE V2
  (02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md). Given a function instruction stream and a
  writer of the form [ebp+disp], reg, it classifies the row:
    REJECTED_ALIAS  only when case A / B / C is PROVEN (rule V2);
    POSSIBLE_ALIAS  otherwise (UNKNOWN live-in EBP is NEVER structural-REJECTED just
                    because EBP is untouched).
  The caller-provenance proofs (case B/C) are supplied as structured evidence inputs;
  the checker never invents them.
EXECUTED AS:
  D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B ebp_alias_classifier.py
  (workdir 00_CONTROL/) â€” runs the MANDATORY negative test + positive control and writes
  01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt (raw program output).
TOOLCHAIN PROVENANCE: interpreter + capstone measured dynamically, recorded in output.
NOTE: capstone is used ONLY to decode fixture streams; no game binary is read or executed
  by this script (the fixtures are synthetic byte sequences defined inline).
"""
import os
import sys
import datetime

import capstone
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_REG, X86_REG_EBP, X86_REG_ESP

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_PATH = os.path.abspath(__file__)


def self_sha256():
    import hashlib
    with open(SELF_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def writes_ebp(insn):
    for op in insn.operands:
        if op.type == X86_OP_REG and op.reg == X86_REG_EBP and (op.access & 0x2):
            return True
    ops = insn.op_str.replace(" ", "")
    if insn.mnemonic in ("mov", "lea", "pop", "xchg", "add", "sub", "and", "or", "xor") \
            and (ops.startswith("ebp,") or ops == "ebp"):
        return True
    return False


def ebp_from_esp(insn):
    """True if the instruction derives EBP from ESP (case B core)."""
    if insn.mnemonic == "mov" and insn.op_str.replace(" ", ")").startswith("ebp,esp"):
        return True
    if insn.mnemonic == "lea" and "esp" in insn.op_str.split(",")[1] and insn.op_str.replace(" ", "") .startswith("ebp,[esp"):
        return True
    return False


def classify(stream_bytes, writer_index, base_va=0x00400000, provenance=None):
    """stream_bytes: bytes of the function from its entry; writer_index: byte offset of
    the writer insn. provenance: optional dict with caller-closure proofs:
      {'ebp_source': 'arg', 'stack_derivation_on_all_paths': bool,
       'class_distinct_from_SF_proven': bool, 'frame_construction_all_paths': bool}
    Returns (classification, reason, case_proven, details list)."""
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail = True
    details = []
    insns = list(cs.disasm(stream_bytes, base_va))
    if not insns:
        return "ERROR", "empty stream", "NONE_PROVEN", ["decode produced no instructions"]
    # locate writer: the instruction whose byte range covers writer_index
    writer = None
    ebp_writes = []
    frame_construction = False
    esp_derivation = False
    for i in insns:
        if (i.address - base_va) <= writer_index < (i.address - base_va) + i.size:
            writer = i
        if writes_ebp(i) and (writer is None or (i.address - base_va) < writer_index):
            ebp_writes.append((i.address, "%s %s" % (i.mnemonic, i.op_str)))
            if i.mnemonic == "push":
                pass
            if ebp_from_esp(i):
                esp_derivation = True
        # frame construction = push ebp followed immediately by mov ebp, esp
    # frame construction check on the decoded pair
    for k in range(len(insns) - 1):
        if insns[k].mnemonic == "push" and insns[k].op_str == "ebp" \
                and insns[k + 1].mnemonic == "mov" and insns[k + 1].op_str.replace(" ", "") == "ebp,esp":
            if writer is None or (insns[k].address - base_va) < writer_index:
                frame_construction = True
    if writer is None:
        return "ERROR", "writer offset not covered by decode", "NONE_PROVEN", details
    details.append("writer @0x%08X: %s %s" % (writer.address, writer.mnemonic, writer.op_str))
    details.append("EBP-writing instructions before the writer: %d %s"
                   % (len(ebp_writes), ebp_writes or ""))

    if frame_construction:
        return ("REJECTED_ALIAS",
                "case A PROVEN: push ebp; mov ebp,esp before the writer â€” EBP is the "
                "function's own frame pointer = a stack address; SF is always-heap so "
                "[ebp+disp] can never alias SF+0x30",
                "A", details)
    if esp_derivation:
        return ("REJECTED_ALIAS",
                "case B PROVEN: EBP explicitly derived from ESP before the writer â€” "
                "stack address; SF is always-heap",
                "B", details)
    if ebp_writes:
        # EBP redefined from a non-ESP source: REJECTED only with caller-closure proof
        if provenance and provenance.get("stack_derivation_on_all_paths"):
            return ("REJECTED_ALIAS",
                    "case B PROVEN via caller closure: EBP := argument register, and that "
                    "register is proven to hold a stack address (esp-derived) on every "
                    "entry path within the declared bound",
                    "B", details)
        if provenance and provenance.get("class_distinct_from_SF_proven"):
            return ("REJECTED_ALIAS",
                    "case C PROVEN: the EBP-base object is proven (class identity, every "
                    "entry path) to be of a class distinct from SceneFeederObject",
                    "C", details)
        return ("POSSIBLE_ALIAS",
                "EBP is REDEFINED in-function from a non-ESP source (argument/register) "
                "with UNPROVEN provenance â€” REJECTED is not proven (rule V2)",
                "NONE_PROVEN", details)
    # EBP untouched in-function: live-in value is UNKNOWN
    if provenance and provenance.get("frame_construction_all_paths"):
        return ("REJECTED_ALIAS",
                "case C PROVEN via caller closure: every reachable caller holds a live "
                "standard frame pointer at its call site, so incoming EBP is a stack "
                "address on every entry path",
                "C", details)
    return ("POSSIBLE_ALIAS",
            "UNKNOWN LIVE-IN EBP (never redefined in-function): rule V2 forbids "
            "structural REJECTED solely because EBP is untouched â€” EBP is callee-saved "
            "and may carry arbitrary caller state; default POSSIBLE_ALIAS",
            "NONE_PROVEN", details)


def run_tests():
    out = []

    def rec(s=""):
        out.append(s)
        print(s)

    rec("=== EBP CLASSIFIER RULE V2 â€” MANDATORY TEST OUTPUTS (RAW PROGRAM OUTPUT) ===")
    rec("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914")
    rec("GENERATOR: 00_CONTROL/ebp_alias_classifier.py (SHA256 %s)" % self_sha256())
    rec("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B ebp_alias_classifier.py")
    rec("interpreter: %s (%s)" % (sys.executable, sys.version.split()[0]))
    rec("capstone.__version__: %s (MEASURED; the 5.0.9 dist-info label is a KNOWN FALSE LABEL)"
        % capstone.__version__)
    rec("capstone.__file__: %s" % capstone.__file__)
    rec("timestamp: %s" % datetime.datetime.now().isoformat())
    rec("")
    rec("--- TEST 1: MANDATORY NEGATIVE TEST (SYNTHETIC_FIXTURE) ---")
    rec("FIXTURE (SYNTHETIC_FIXTURE â€” synthetic bytes defined inline in the checker;")
    rec("        NEVER claimed to be Entropia bytes):")
    rec("  function stream (7 bytes):")
    rec("    53                push ebx            (a callee-saved push â€” EBP NOT touched)")
    rec("    56                push esi")
    rec("    8B D9             mov ebx, ecx        (arbitrary work, EBP NOT touched)")
    rec("    89 75 30          mov dword ptr [ebp + 0x30], esi   <- THE WRITER (offset 5)")
    rec("  precondition: incoming EBP value UNKNOWN (nothing in the stream defines it)")
    # bytes: 53 56 8B D9 89 75 30
    neg_bytes = bytes.fromhex("53568BD9897530")
    rec("  fixture hex: %s" % neg_bytes.hex().upper())
    cls, reason, case, details = classify(neg_bytes, writer_index=5)
    for d in details:
        rec("    detail: %s" % d)
    rec("  CLASSIFIER OUTPUT: %s" % cls)
    rec("  CASE: %s" % case)
    rec("  REASON: %s" % reason)
    rec("  REQUIRED: POSSIBLE_ALIAS -> %s" % ("PASS" if cls == "POSSIBLE_ALIAS" else "FAIL â€” CLEANUP FAILS (G8)"))
    rec("")
    rec("--- TEST 2: POSITIVE CONTROL (sound case A) ---")
    rec("FIXTURE (SYNTHETIC_FIXTURE): push ebp; mov ebp,esp; mov dword ptr [ebp+0x30], eax")
    pos_bytes = bytes.fromhex("558BEC894530")
    rec("  fixture hex: %s" % pos_bytes.hex().upper())
    cls2, reason2, case2, details2 = classify(pos_bytes, writer_index=3)
    for d in details2:
        rec("    detail: %s" % d)
    rec("  CLASSIFIER OUTPUT: %s" % cls2)
    rec("  CASE: %s" % case2)
    rec("  REASON: %s" % reason2)
    rec("  REQUIRED: REJECTED_ALIAS -> %s" % ("PASS" if cls2 == "REJECTED_ALIAS" else "FAIL â€” checker broken (G8)"))
    rec("")
    ok = (cls == "POSSIBLE_ALIAS") and (cls2 == "REJECTED_ALIAS")
    rec("G8 SELF-VERDICT: %s" % ("BOTH TESTS PASS" if ok else "AT LEAST ONE TEST FAILED"))
    with open(os.path.join(PKG_ROOT, "01_RAW", "EBP_CLASSIFIER_TEST_OUTPUTS.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("")
    print("raw outputs written: 01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run_tests())

